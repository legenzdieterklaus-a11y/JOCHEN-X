"""Explicit composition container with lifetimes, scopes, and validation."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from enum import StrEnum
import inspect
from threading import RLock
from typing import Any, TypeVar, get_type_hints
from dataclasses import dataclass

T = TypeVar("T")
Factory = Callable[..., Any]


class Lifetime(StrEnum):
    SINGLETON = "singleton"
    TRANSIENT = "transient"
    SCOPED = "scoped"


class CircularDependencyError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ServiceDescriptor:
    key: str
    lifetime: Lifetime
    initialized: bool
    dependencies: tuple[str, ...]
    service_type: str = ""
    available_since: str = "registration"


_MISSING = object()


class _Registration:
    def __init__(
        self,
        factory: Factory,
        lifetime: Lifetime,
        *,
        service_type: str = "",
        available_since: str = "registration",
    ) -> None:
        self.factory = factory
        self.lifetime = lifetime
        self.instance = _MISSING
        self.service_type = service_type
        self.available_since = available_since


class ServiceScope:
    def __init__(self, container: "ServiceRegistry") -> None:
        self._container = container
        self._instances: dict[type[Any], Any] = {}
        self._closed = False

    def get(self, key: type[T]) -> T:
        if self._closed:
            raise RuntimeError("Scope is closed")
        return self._container._resolve(key, self, ())

    def close(self) -> None:
        self._closed = True
        self._instances.clear()

    def __enter__(self) -> "ServiceScope":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class ServiceRegistry:
    """Composition-root container. Registrations are typed and resolved lazily."""

    def __init__(self) -> None:
        self._registrations: dict[type[Any], _Registration] = {}
        self._lock = RLock()

    def register(self, key: type[T], service: T, *, available_since: str = "registration") -> None:
        self.register_factory(
            key,
            lambda: service,
            lifetime=Lifetime.SINGLETON,
            service_type=type(service).__name__,
            available_since=available_since,
        )
        self._registrations[key].instance = service

    def register_factory(
        self,
        key: type[T],
        factory: Callable[..., T],
        *,
        lifetime: Lifetime = Lifetime.SINGLETON,
        service_type: str | None = None,
        available_since: str | None = None,
    ) -> None:
        resolved_type = service_type or (
            factory.__name__ if inspect.isclass(factory) else key.__name__
        )
        with self._lock:
            if key in self._registrations:
                raise ValueError(f"Service already registered: {key.__name__}")
            self._registrations[key] = _Registration(
                factory,
                lifetime,
                service_type=resolved_type,
                available_since=available_since or "on_first_resolve",
            )

    def register_type(
        self, key: type[T], implementation: type[T], *, lifetime: Lifetime = Lifetime.SINGLETON
    ) -> None:
        self.register_factory(
            key, implementation, lifetime=lifetime, service_type=implementation.__name__
        )

    def get(self, key: type[T]) -> T:
        return self._resolve(key, None, ())

    def create_scope(self) -> ServiceScope:
        return ServiceScope(self)

    def validate(self) -> None:
        for key in tuple(self._registrations):
            self._resolve(key, None, ())

    def descriptors(self) -> tuple[ServiceDescriptor, ...]:
        """Return safe metadata for diagnostics without exposing registrations."""
        with self._lock:
            return tuple(
                self._describe(key, registration)
                for key, registration in self._registrations.items()
            )

    def describe(self, key: type[Any]) -> ServiceDescriptor:
        """Return the description of a single registered service.

        The description covers name, service type, and availability point.

        Raises:
            LookupError: If no service is registered under ``key``.
        """
        with self._lock:
            try:
                registration = self._registrations[key]
            except KeyError as error:
                raise LookupError(f"Service not registered: {key.__name__}") from error
            return self._describe(key, registration)

    @staticmethod
    def _describe(key: type[Any], registration: _Registration) -> ServiceDescriptor:
        signature = inspect.signature(registration.factory)
        dependencies = tuple(
            parameter.annotation.__name__
            if isinstance(parameter.annotation, type)
            else str(parameter.annotation)
            for parameter in signature.parameters.values()
            if parameter.kind not in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD)
            and parameter.annotation is not inspect.Parameter.empty
        )
        return ServiceDescriptor(
            key.__name__,
            registration.lifetime,
            registration.instance is not _MISSING,
            dependencies,
            registration.service_type,
            registration.available_since,
        )

    def _resolve(
        self, key: type[T], scope: ServiceScope | None, trail: tuple[type[Any], ...]
    ) -> T:
        if key in trail:
            raise CircularDependencyError(
                " -> ".join(item.__name__ for item in (*trail, key))
            )
        try:
            registration = self._registrations[key]
        except KeyError as error:
            raise LookupError(f"Service not registered: {key.__name__}") from error
        store: dict[type[Any], Any] | None = None
        if registration.lifetime is Lifetime.SINGLETON:
            store = {key: registration.instance}
        elif registration.lifetime is Lifetime.SCOPED:
            if scope is None:
                raise RuntimeError(f"Scoped service requires a scope: {key.__name__}")
            store = scope._instances
        if store is not None and key in store and store[key] is not _MISSING:
            return store[key]
        instance = self._construct(registration.factory, scope, (*trail, key))
        if store is not None:
            if registration.lifetime is Lifetime.SINGLETON:
                registration.instance = instance
            else:
                store[key] = instance
        return instance

    def _construct(
        self, factory: Factory, scope: ServiceScope | None, trail: tuple[type[Any], ...]
    ) -> Any:
        signature = inspect.signature(factory)
        hints = get_type_hints(factory.__init__ if inspect.isclass(factory) else factory)
        args = []
        for parameter in signature.parameters.values():
            if parameter.kind in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD):
                continue
            dependency = hints.get(parameter.name, parameter.annotation)
            if dependency is inspect.Parameter.empty:
                if parameter.default is inspect.Parameter.empty:
                    raise TypeError(f"Untyped dependency: {parameter.name}")
                continue
            try:
                args.append(self._resolve(dependency, scope, trail))
            except LookupError:
                if parameter.default is inspect.Parameter.empty:
                    raise
        return factory(*args)

    def __iter__(self) -> Iterator[object]:
        return iter(
            self._resolve(key, None, ())
            for key, value in self._registrations.items()
            if value.lifetime is Lifetime.SINGLETON
        )
