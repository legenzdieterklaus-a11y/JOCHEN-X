"""Service provider for managing service creation and lifetime caching."""

from __future__ import annotations

from collections.abc import Callable
from threading import Lock
from typing import Any

from jochen_x.core.di.scope import ServiceScope

__all__ = ["ServiceProvider"]

_UNSET: object = object()


class ServiceProvider:
    """Wraps a factory callable with scope metadata and singleton caching.

    For ``SINGLETON`` scope, the provider uses double-checked locking to
    guarantee that exactly one instance is created across all threads.
    The singleton is created lazily on first resolution.

    For ``TRANSIENT`` and ``SCOPED`` scopes, every call to
    ``create_instance`` invokes the factory.  Scoped caching is managed
    externally by ``ScopedContainer``.

    Args:
        interface: The protocol/interface type this provider serves.
        factory: A zero-argument callable that creates a service instance.
        scope: The lifetime scope for created instances.

    """

    __slots__ = ("_factory", "_interface", "_lock", "_scope", "_singleton_instance")

    def __init__(
        self,
        interface: type[Any],
        factory: Callable[[], Any],
        scope: ServiceScope,
    ) -> None:
        """Initialise the provider with its factory and scope."""
        self._interface: type[Any] = interface
        self._factory: Callable[[], Any] = factory
        self._scope: ServiceScope = scope
        self._singleton_instance: Any = _UNSET
        self._lock: Lock = Lock()

    @property
    def interface(self) -> type[Any]:
        """The interface type this provider is registered for."""
        return self._interface

    @property
    def scope(self) -> ServiceScope:
        """The lifetime scope for this provider."""
        return self._scope

    def create_instance(self) -> Any:
        """Create or return a cached service instance.

        For ``SINGLETON`` scope, uses double-checked locking so that the
        factory is invoked at most once.  If the factory raises, no
        instance is cached and subsequent calls will retry.

        For ``TRANSIENT`` and ``SCOPED`` scopes, the factory is invoked
        on every call.

        Returns:
            A service instance produced by the factory.

        """
        if self._scope == ServiceScope.SINGLETON:
            if self._singleton_instance is not _UNSET:
                return self._singleton_instance
            with self._lock:
                if self._singleton_instance is not _UNSET:
                    return self._singleton_instance
                instance: Any = self._factory()
                self._singleton_instance = instance
                return instance
        return self._factory()

    def reset_singleton(self) -> None:
        """Clear the cached singleton instance.

        After calling this method the next resolution will invoke the
        factory again.  Has no effect for non-singleton scopes.
        """
        with self._lock:
            self._singleton_instance = _UNSET
