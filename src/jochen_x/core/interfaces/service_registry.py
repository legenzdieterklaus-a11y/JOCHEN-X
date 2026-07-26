"""Service registry protocol for centralised service management."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Protocol, TypeVar, runtime_checkable

__all__ = ["IServiceRegistry"]

T = TypeVar("T")


@runtime_checkable
class IServiceRegistry(Protocol):
    """Protocol for the centralised service registry.

    The service registry manages registration, lookup, and lifecycle
    of all runtime services.  Access is thread-safe.
    """

    def register(self, interface: type[T], implementation: T) -> None:
        """Register an implementation for a given interface.

        Args:
            interface: The protocol/interface type to register under.
            implementation: The concrete implementation to register.

        Raises:
            InputValidationError: If the interface is already registered.

        """
        ...

    def resolve(self, interface: type[T]) -> T:
        """Resolve a service by its interface type.

        Args:
            interface: The protocol/interface type to look up.

        Returns:
            The registered implementation.

        Raises:
            JochenXError: If no implementation is registered for the
                given interface.

        """
        ...

    def has(self, interface: type[Any]) -> bool:
        """Check whether a service is registered for the given interface.

        Args:
            interface: The protocol/interface type to check.

        Returns:
            ``True`` if an implementation is registered, ``False``
            otherwise.

        """
        ...

    def get_registered_interfaces(self) -> Sequence[type[Any]]:
        """Return all currently registered interface types.

        Returns:
            A sequence of registered interface types.

        """
        ...
