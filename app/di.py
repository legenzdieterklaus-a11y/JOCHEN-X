"""Dependency-injection surface for the application foundation.

The core :class:`core.registry.ServiceRegistry` already provides typed
registration, constructor injection, singleton/scoped/transient lifetimes,
circular-dependency detection, and validation. This module adds the two pieces
the application foundation requires on top of it without modifying the core
container:

* :class:`ServiceProvider` - a narrow, read-only resolution facade that keeps
  callers from abusing the registry as a mutable service locator.
* :class:`Disposable` / :class:`DisposableRegistry` - deterministic,
  reverse-order cleanup of resources the host owns.
"""

from __future__ import annotations

import logging
from typing import Protocol, TypeVar, runtime_checkable

from core.registry import ServiceRegistry, ServiceScope

T = TypeVar("T")


@runtime_checkable
class Disposable(Protocol):
    """A resource that releases its underlying handles when disposed."""

    def dispose(self) -> None:
        """Release the resource. Implementations must be idempotent."""
        ...


class ServiceProvider:
    """Read-only resolution facade over a :class:`ServiceRegistry`.

    Exposing only resolution (not registration) keeps consumers decoupled from
    composition and prevents service-locator abuse across the application.
    """

    def __init__(self, registry: ServiceRegistry) -> None:
        """Wrap an already-composed registry.

        Args:
            registry: The composition-root registry to resolve services from.
        """
        self._registry = registry

    def get(self, key: type[T]) -> T:
        """Resolve a required service, raising ``LookupError`` if unregistered."""
        return self._registry.get(key)

    def get_optional(self, key: type[T]) -> T | None:
        """Resolve a service or return ``None`` when it is not registered."""
        try:
            return self._registry.get(key)
        except LookupError:
            return None

    def create_scope(self) -> ServiceScope:
        """Create a disposable resolution scope for scoped services."""
        return self._registry.create_scope()


class DisposableRegistry:
    """Owns a stack of disposables and releases them in reverse order."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Create an empty registry.

        Args:
            logger: Optional logger used to report disposal failures.
        """
        self._logger = logger or logging.getLogger("jochen_x.di")
        self._disposables: list[Disposable] = []

    def register(self, disposable: T) -> T:
        """Register a disposable for later cleanup and return it unchanged.

        Args:
            disposable: An object implementing the :class:`Disposable` protocol.

        Returns:
            The same object, to allow fluent registration at creation sites.

        Raises:
            TypeError: If the object does not implement ``dispose``.
        """
        if not isinstance(disposable, Disposable):
            raise TypeError(f"Object is not disposable: {type(disposable).__name__}")
        self._disposables.append(disposable)
        return disposable

    def dispose_all(self) -> None:
        """Dispose every registered resource in reverse registration order.

        Each disposal is guarded so a single failure never prevents the rest of
        the resources from being released.
        """
        while self._disposables:
            disposable = self._disposables.pop()
            try:
                disposable.dispose()
            except Exception as error:  # cleanup must never raise to the caller
                self._logger.error(
                    "dispose.failed",
                    extra={"context": {"type": type(disposable).__name__, "error": str(error)}},
                )
