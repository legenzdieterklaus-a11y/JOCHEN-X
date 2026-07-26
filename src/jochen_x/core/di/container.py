"""Lightweight dependency injection container with lifetime management."""

from __future__ import annotations

import threading
from collections.abc import Callable, Sequence
from types import TracebackType
from typing import Any, Self, TypeVar

from jochen_x.core.di.provider import ServiceProvider
from jochen_x.core.di.scope import ServiceScope
from jochen_x.core.exceptions.base import JochenXError
from jochen_x.core.exceptions.security import InputValidationError

__all__ = [
    "CircularDependencyError",
    "DIContainer",
    "DuplicateRegistrationError",
    "ScopeError",
    "ScopedContainer",
    "ServiceNotRegisteredError",
]

T = TypeVar("T")

_COMPONENT_NAME = "DIContainer"


# ---------------------------------------------------------------------------
# DI-specific exceptions
# ---------------------------------------------------------------------------


class CircularDependencyError(JochenXError):
    """A circular dependency was detected during service resolution.

    Args:
        chain: Human-readable dependency chain showing the cycle
            (e.g. ``"A -> B -> C -> A"``).
        correlation_id: Correlation ID for cross-component tracing.

    """

    def __init__(
        self,
        chain: str,
        *,
        correlation_id: str = "",
    ) -> None:
        """Initialise with the full dependency chain."""
        self.chain: str = chain
        super().__init__(
            f"Circular dependency detected: {chain}",
            correlation_id=correlation_id,
            component=_COMPONENT_NAME,
        )


class ServiceNotRegisteredError(JochenXError):
    """No service is registered for the requested interface.

    Args:
        interface: The interface type that was requested.
        correlation_id: Correlation ID for cross-component tracing.

    """

    def __init__(
        self,
        interface: type[Any],
        *,
        correlation_id: str = "",
    ) -> None:
        """Initialise with the unregistered interface."""
        self.requested_interface: type[Any] = interface
        super().__init__(
            f"No service registered for interface '{interface.__qualname__}'",
            correlation_id=correlation_id,
            component=_COMPONENT_NAME,
        )


class DuplicateRegistrationError(JochenXError):
    """An interface was registered more than once without prior reset.

    Args:
        interface: The interface type that is already registered.
        correlation_id: Correlation ID for cross-component tracing.

    """

    def __init__(
        self,
        interface: type[Any],
        *,
        correlation_id: str = "",
    ) -> None:
        """Initialise with the duplicate interface."""
        self.duplicate_interface: type[Any] = interface
        super().__init__(
            f"Interface '{interface.__qualname__}' is already registered",
            correlation_id=correlation_id,
            component=_COMPONENT_NAME,
        )


class ScopeError(JochenXError):
    """A scope-related constraint was violated.

    Raised when a ``SCOPED`` service is resolved outside a scope context
    or when a disposed scope is used.

    Args:
        message: Human-readable error description.
        correlation_id: Correlation ID for cross-component tracing.

    """

    def __init__(
        self,
        message: str,
        *,
        correlation_id: str = "",
    ) -> None:
        """Initialise with the violation details."""
        super().__init__(
            message,
            correlation_id=correlation_id,
            component=_COMPONENT_NAME,
        )


# ---------------------------------------------------------------------------
# Thread-local resolution stack
# ---------------------------------------------------------------------------


class _ResolvingLocal(threading.local):
    """Thread-local storage for the circular-dependency detection stack.

    Each thread gets its own empty stack via ``__init__`` which
    ``threading.local`` calls automatically per-thread.
    """

    stack: list[type[Any]]

    def __init__(self) -> None:
        super().__init__()
        self.stack = []


# ---------------------------------------------------------------------------
# DI Container
# ---------------------------------------------------------------------------


class DIContainer:
    """Lightweight dependency injection container.

    Supports three service lifetimes: ``SINGLETON`` (one instance per
    container), ``TRANSIENT`` (new instance per resolution), and
    ``SCOPED`` (one instance per scope context).

    All operations are thread-safe.  Circular dependencies are detected
    at resolution time with descriptive error messages showing the full
    dependency chain.

    Example::

        container = DIContainer()
        container.register(ILogger, lambda: ConsoleLogger(), ServiceScope.SINGLETON)
        logger = container.resolve(ILogger)

    """

    __slots__ = ("_lock", "_providers", "_resolving")

    def __init__(self) -> None:
        """Initialise an empty container."""
        self._providers: dict[type[Any], ServiceProvider] = {}
        self._lock: threading.RLock = threading.RLock()
        self._resolving: _ResolvingLocal = _ResolvingLocal()

    # -- Registration -------------------------------------------------------

    def register(
        self,
        interface: type[Any],
        factory: Callable[[], Any],
        scope: ServiceScope = ServiceScope.SINGLETON,
    ) -> None:
        """Register a factory for a given interface type.

        The factory is not called at registration time; instances are
        created lazily on first resolution.

        Args:
            interface: The protocol/interface type to register under.
            factory: A zero-argument callable that creates the service.
            scope: Lifetime scope for the registration.

        Raises:
            InputValidationError: If *interface* is not a type,
                *factory* is not callable, or *scope* is not a
                ``ServiceScope``.
            DuplicateRegistrationError: If *interface* is already
                registered.

        """
        if not isinstance(interface, type):
            field = "interface"
            reason = f"Expected a type, got {type(interface).__name__}"
            raise InputValidationError(field, reason, component=_COMPONENT_NAME)
        if not callable(factory):
            field = "factory"
            reason = "Factory must be callable"
            raise InputValidationError(field, reason, component=_COMPONENT_NAME)
        if not isinstance(scope, ServiceScope):
            field = "scope"
            reason = f"Expected ServiceScope, got {type(scope).__name__}"
            raise InputValidationError(field, reason, component=_COMPONENT_NAME)

        with self._lock:
            if interface in self._providers:
                raise DuplicateRegistrationError(interface)
            self._providers[interface] = ServiceProvider(interface, factory, scope)

    # -- Resolution ---------------------------------------------------------

    def resolve(self, interface: type[T]) -> T:
        """Resolve a service by its interface type.

        For ``SINGLETON`` scope the same instance is returned on every
        call.  For ``TRANSIENT`` scope a new instance is created each
        time.  ``SCOPED`` services cannot be resolved directly; use
        ``create_scope`` instead.

        Args:
            interface: The protocol/interface type to resolve.

        Returns:
            The service instance.

        Raises:
            ServiceNotRegisteredError: If no factory is registered for
                *interface*.
            CircularDependencyError: If a dependency cycle is detected.
            ScopeError: If *interface* has ``SCOPED`` lifetime.

        """
        provider = self._get_provider(interface)

        if provider.scope == ServiceScope.SCOPED:
            msg = (
                f"Cannot resolve scoped service '{interface.__qualname__}' "
                f"outside of a scope context — use create_scope()"
            )
            raise ScopeError(msg)

        return self._resolve_with_cycle_check(interface, provider)  # type: ignore[no-any-return]

    # -- Query --------------------------------------------------------------

    def has(self, interface: type[Any]) -> bool:
        """Check whether a factory is registered for *interface*.

        Args:
            interface: The protocol/interface type to check.

        Returns:
            ``True`` if a factory is registered, ``False`` otherwise.

        """
        with self._lock:
            return interface in self._providers

    def get_registered_interfaces(self) -> Sequence[type[Any]]:
        """Return all currently registered interface types.

        Returns:
            A sequence of registered interface types.

        """
        with self._lock:
            return list(self._providers.keys())

    # -- Scope --------------------------------------------------------------

    def create_scope(self) -> ScopedContainer:
        """Create a new scoped container for ``SCOPED`` services.

        The returned container should be used as a context manager::

            with container.create_scope() as scope:
                service = scope.resolve(IScopedService)

        Returns:
            A new scoped container bound to this parent container.

        """
        return ScopedContainer(self)

    # -- Lifecycle ----------------------------------------------------------

    def reset(self) -> None:
        """Clear all registrations and cached singleton instances.

        After calling this the container is empty and ready for fresh
        registrations.
        """
        with self._lock:
            for provider in self._providers.values():
                provider.reset_singleton()
            self._providers.clear()

    # -- Internal -----------------------------------------------------------

    def _get_provider(self, interface: type[Any]) -> ServiceProvider:
        """Look up the provider for *interface*.

        Args:
            interface: The interface type to look up.

        Returns:
            The registered service provider.

        Raises:
            ServiceNotRegisteredError: If no provider is registered.

        """
        with self._lock:
            provider = self._providers.get(interface)
        if provider is None:
            raise ServiceNotRegisteredError(interface)
        return provider

    def _resolve_with_cycle_check(
        self,
        interface: type[Any],
        provider: ServiceProvider,
    ) -> Any:
        """Resolve *provider* while guarding against circular dependencies.

        Uses a thread-local resolution stack.  If *interface* already
        appears on the stack a ``CircularDependencyError`` is raised
        with a human-readable chain.

        Args:
            interface: The interface being resolved.
            provider: The provider to create the instance from.

        Returns:
            The resolved service instance.

        Raises:
            CircularDependencyError: If a dependency cycle is detected.

        """
        stack = self._resolving.stack

        if interface in stack:
            cycle_start = stack.index(interface)
            cycle_types = stack[cycle_start:]
            chain = " -> ".join(t.__qualname__ for t in cycle_types)
            chain += f" -> {interface.__qualname__}"
            raise CircularDependencyError(chain)

        stack.append(interface)
        try:
            return provider.create_instance()
        finally:
            stack.pop()


# ---------------------------------------------------------------------------
# Scoped Container
# ---------------------------------------------------------------------------


class ScopedContainer:
    """Scoped container for resolving ``SCOPED`` lifetime services.

    ``SCOPED`` services are cached within this container's lifetime and
    shared across all resolutions in the same scope.  ``SINGLETON``
    services are delegated to the parent container.  ``TRANSIENT``
    services always create a new instance.

    Use as a context manager to ensure proper cleanup::

        with container.create_scope() as scope:
            svc = scope.resolve(IScopedService)

    Args:
        parent: The parent ``DIContainer`` that holds the registrations.

    """

    __slots__ = ("_disposed", "_lock", "_parent", "_scoped_instances")

    def __init__(self, parent: DIContainer) -> None:
        """Initialise the scoped container bound to *parent*."""
        self._parent: DIContainer = parent
        self._scoped_instances: dict[type[Any], Any] = {}
        self._lock: threading.Lock = threading.Lock()
        self._disposed: bool = False

    def resolve(self, interface: type[T]) -> T:
        """Resolve a service by its interface type within this scope.

        Args:
            interface: The protocol/interface type to resolve.

        Returns:
            The service instance.

        Raises:
            ScopeError: If this scope has been disposed.
            ServiceNotRegisteredError: If no factory is registered.
            CircularDependencyError: If a dependency cycle is detected.

        """
        if self._disposed:
            msg = "Cannot resolve from a disposed scope"
            raise ScopeError(msg)

        provider = self._parent._get_provider(interface)  # noqa: SLF001
        resolve = self._parent._resolve_with_cycle_check  # noqa: SLF001

        if provider.scope in (ServiceScope.SINGLETON, ServiceScope.TRANSIENT):
            return resolve(interface, provider)  # type: ignore[no-any-return]

        # SCOPED — check cache (fast path)
        with self._lock:
            if interface in self._scoped_instances:
                return self._scoped_instances[interface]  # type: ignore[no-any-return]

        # Create outside the lock to avoid deadlocks if the factory
        # resolves further scoped services.
        instance: Any = resolve(interface, provider)

        with self._lock:
            return self._scoped_instances.setdefault(interface, instance)  # type: ignore[no-any-return]

    def has(self, interface: type[Any]) -> bool:
        """Check whether a factory is registered in the parent container.

        Args:
            interface: The protocol/interface type to check.

        Returns:
            ``True`` if a factory is registered, ``False`` otherwise.

        """
        return self._parent.has(interface)

    def dispose(self) -> None:
        """Dispose this scope, clearing all cached scoped instances.

        After disposal no further resolutions are allowed from this
        scope.
        """
        self._disposed = True
        with self._lock:
            self._scoped_instances.clear()

    def __enter__(self) -> Self:
        """Enter the scope context."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the scope context and dispose cached instances."""
        self.dispose()
