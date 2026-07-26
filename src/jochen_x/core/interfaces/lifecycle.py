"""Lifecycle protocol for components with managed start/stop behaviour."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

__all__ = ["ILifecycle"]


@runtime_checkable
class ILifecycle(Protocol):
    """Protocol for components with managed lifecycle.

    Every runtime component that requires ordered initialisation,
    startup, and shutdown implements this protocol.  The runtime host
    calls these methods in deterministic order during bootstrap and
    shutdown sequences.
    """

    def initialize(self) -> None:
        """Initialise the component.

        Called once during the bootstrap sequence.  The component must
        be ready for ``start`` after this method returns.

        Raises:
            JochenXError: If initialisation fails.

        """
        ...

    def start(self) -> None:
        """Start the component.

        Called after all components have been initialised.

        Raises:
            JochenXError: If the component fails to start.

        """
        ...

    def stop(self) -> None:
        """Stop the component gracefully.

        Called during the shutdown sequence in reverse bootstrap order.
        Must complete all in-flight work before returning.

        Raises:
            JochenXError: If the component fails to stop cleanly.

        """
        ...
