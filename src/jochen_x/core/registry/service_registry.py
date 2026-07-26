"""Central service registry with lifecycle management.

The ``ServiceRegistry`` is the single source of truth for all runtime
services.  It provides thread-safe registration, lookup by interface
type, and coordinated lifecycle management for services that implement
the ``ILifecycle`` protocol.
"""

from __future__ import annotations

import contextlib
import threading
from collections.abc import Sequence
from typing import Any, TypeVar

from jochen_x.core.exceptions.base import JochenXError
from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.interfaces.lifecycle import ILifecycle

__all__ = [
    "ServiceNotFoundError",
    "ServiceRegistry",
]

T = TypeVar("T")

_COMPONENT_NAME = "ServiceRegistry"
_FIELD_INTERFACE = "interface"
_FIELD_IMPLEMENTATION = "implementation"
_REASON_NOT_A_TYPE = "Expected a type, got {actual}"
_REASON_NONE_IMPL = "Implementation must not be None"
_REASON_ALREADY_REGISTERED = "Interface '{name}' is already registered"


class ServiceNotFoundError(JochenXError):
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


def _validate_interface(interface: Any) -> None:
    """Raise ``InputValidationError`` if *interface* is not a type."""
    if not isinstance(interface, type):
        reason = _REASON_NOT_A_TYPE.format(actual=type(interface).__name__)
        raise InputValidationError(
            _FIELD_INTERFACE,
            reason,
            component=_COMPONENT_NAME,
        )


class ServiceRegistry:
    """Central registry for all runtime services.

    Manages registration, lookup, and lifecycle of runtime services.
    Services are registered under their protocol/interface type and
    retrieved by the same type.  Registration order is preserved and
    used for deterministic lifecycle management.

    Services that implement ``ILifecycle`` receive coordinated
    ``start`` and ``stop`` calls.  ``start`` is called in registration
    order, ``stop`` in reverse registration order.

    All operations are thread-safe.

    Example::

        registry = ServiceRegistry()
        registry.register(ILogger, console_logger)
        logger = registry.resolve(ILogger)

    """

    __slots__ = ("_lock", "_services", "_started")

    def __init__(self) -> None:
        """Initialise an empty service registry."""
        self._services: dict[type[Any], Any] = {}
        self._lock: threading.RLock = threading.RLock()
        self._started: bool = False

    # -- IServiceRegistry protocol ------------------------------------------

    def register(self, interface: type[T], implementation: T) -> None:
        """Register an implementation for a given interface.

        Args:
            interface: The protocol/interface type to register under.
            implementation: The concrete instance to register.

        Raises:
            InputValidationError: If *interface* is not a type,
                *implementation* is ``None``, or *interface* is already
                registered.

        """
        _validate_interface(interface)
        if implementation is None:
            raise InputValidationError(
                _FIELD_IMPLEMENTATION,
                _REASON_NONE_IMPL,
                component=_COMPONENT_NAME,
            )

        with self._lock:
            if interface in self._services:
                reason = _REASON_ALREADY_REGISTERED.format(
                    name=interface.__qualname__,
                )
                raise InputValidationError(
                    _FIELD_INTERFACE,
                    reason,
                    component=_COMPONENT_NAME,
                )
            self._services[interface] = implementation

    def resolve(self, interface: type[T]) -> T:
        """Resolve a service by its interface type.

        Args:
            interface: The protocol/interface type to look up.

        Returns:
            The registered implementation.

        Raises:
            InputValidationError: If *interface* is not a type.
            ServiceNotFoundError: If no implementation is registered
                for the given interface.

        """
        _validate_interface(interface)

        with self._lock:
            implementation = self._services.get(interface)

        if implementation is None:
            raise ServiceNotFoundError(interface)

        return implementation  # type: ignore[no-any-return]

    def has(self, interface: type[Any]) -> bool:
        """Check whether a service is registered for the given interface.

        Args:
            interface: The protocol/interface type to check.

        Returns:
            ``True`` if an implementation is registered, ``False``
            otherwise.

        """
        with self._lock:
            return interface in self._services

    def get_registered_interfaces(self) -> Sequence[type[Any]]:
        """Return all currently registered interface types.

        Returns:
            A sequence of registered interface types in registration
            order.

        """
        with self._lock:
            return list(self._services.keys())

    # -- Lifecycle management -----------------------------------------------

    def unregister(self, interface: type[Any]) -> None:
        """Remove a service registration.

        If the service implements ``ILifecycle`` and the registry has
        been started, the service is stopped before removal.

        Args:
            interface: The protocol/interface type to unregister.

        Raises:
            InputValidationError: If *interface* is not a type.
            ServiceNotFoundError: If no implementation is registered
                for the given interface.

        """
        _validate_interface(interface)

        with self._lock:
            if interface not in self._services:
                raise ServiceNotFoundError(interface)
            implementation = self._services.pop(interface)

        with self._lock:
            was_started = self._started
        if was_started and isinstance(implementation, ILifecycle):
            implementation.stop()

    def initialize(self) -> None:
        """Initialise the service registry.

        Called once during the bootstrap sequence.  Prepares the
        registry for service registration and lifecycle management.
        """

    def start(self) -> None:
        """Start all registered services that implement ``ILifecycle``.

        Services are started in registration order.  If a service
        fails to start, previously started services are stopped in
        reverse order before the error propagates.

        Raises:
            JochenXError: If any service fails to start.

        """
        with self._lock:
            lifecycle_services: list[tuple[type[Any], ILifecycle]] = [
                (iface, impl)
                for iface, impl in self._services.items()
                if isinstance(impl, ILifecycle)
            ]

        started: list[ILifecycle] = []
        try:
            for _iface, service in lifecycle_services:
                service.start()
                started.append(service)
        except Exception:
            for svc in reversed(started):
                with contextlib.suppress(Exception):
                    svc.stop()
            raise

        with self._lock:
            self._started = True

    def stop(self) -> None:
        """Stop all registered services that implement ``ILifecycle``.

        Services are stopped in reverse registration order.  Errors
        during individual service stops are collected; all services
        are stopped regardless of individual failures.  If any
        service failed to stop, the first error is re-raised after
        all services have been stopped.

        Raises:
            JochenXError: If any service fails to stop (after all
                services have been attempted).

        """
        with self._lock:
            lifecycle_services: list[ILifecycle] = [
                impl
                for impl in self._services.values()
                if isinstance(impl, ILifecycle)
            ]

        first_error: Exception | None = None
        for service in reversed(lifecycle_services):
            try:
                service.stop()
            except Exception as exc:  # noqa: BLE001
                if first_error is None:
                    first_error = exc

        with self._lock:
            self._started = False

        if first_error is not None:
            raise first_error

    def reset(self) -> None:
        """Clear all registrations.

        If the registry has been started, all lifecycle services are
        stopped first.  After calling this the registry is empty.
        """
        with self._lock:
            needs_stop = self._started
        if needs_stop:
            self.stop()
        with self._lock:
            self._services.clear()
