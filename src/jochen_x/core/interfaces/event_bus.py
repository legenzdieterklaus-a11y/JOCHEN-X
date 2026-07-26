"""Event bus protocol for typed, asynchronous event distribution."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from jochen_x.core.types.events import EventHandler, RuntimeEvent

__all__ = ["IEventBus"]


@runtime_checkable
class IEventBus(Protocol):
    """Protocol for the runtime event bus.

    The event bus distributes typed events asynchronously to registered
    handlers.  It supports handler registration and deregistration at
    runtime, event prioritisation, and a dead-letter queue for
    undeliverable events.

    All operations are thread-safe.
    """

    def publish(self, event: RuntimeEvent) -> None:
        """Publish an event to all matching handlers.

        Handlers are matched by event type.  A handler registered for
        a base event type receives events of all derived types.

        Args:
            event: The event to publish.

        Raises:
            JochenXError: If the bus is not operational.

        """
        ...

    def subscribe(
        self,
        event_type: type[RuntimeEvent],
        handler: EventHandler,
        *,
        priority: int = 0,
    ) -> None:
        """Subscribe a handler to events of the given type.

        Args:
            event_type: The event type to subscribe to.
            handler: Callable that will receive matching events.
            priority: Handler priority (higher values run first).

        Raises:
            InputValidationError: If event_type or handler is invalid.

        """
        ...

    def unsubscribe(
        self,
        event_type: type[RuntimeEvent],
        handler: EventHandler,
    ) -> None:
        """Unsubscribe a handler from events of the given type.

        No-op if the handler is not currently subscribed.

        Args:
            event_type: The event type to unsubscribe from.
            handler: The handler to remove.

        """
        ...
