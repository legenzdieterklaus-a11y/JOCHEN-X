"""Event handler registry with priority-based ordering.

The ``HandlerRegistry`` manages handler subscriptions per event type
with support for runtime registration/deregistration and priority-based
dispatch ordering.  All operations are thread-safe.
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock

from jochen_x.core.types.events import EventHandler, RuntimeEvent

__all__ = [
    "HandlerEntry",
    "HandlerRegistry",
]


@dataclass(frozen=True, slots=True)
class HandlerEntry:
    """A registered handler with its dispatch priority.

    Handlers with higher priority values are invoked first.
    Within the same priority, insertion order is preserved.

    Args:
        handler: The callable that processes events.
        priority: Dispatch priority (higher runs first).
        insertion_order: Monotonically increasing counter for
            deterministic ordering within the same priority.

    """

    handler: EventHandler
    priority: int
    insertion_order: int


def _sort_key(entry: HandlerEntry) -> tuple[int, int]:
    """Return a sort key that orders higher priority first, then by insertion order."""
    return (-entry.priority, entry.insertion_order)


class HandlerRegistry:
    """Thread-safe registry of event handlers grouped by event type.

    Supports subscription and unsubscription at any time, including
    during event dispatch.  Snapshot-based iteration ensures that
    mutations during dispatch do not corrupt the handler list.

    Args:
        No arguments required.

    """

    def __init__(self) -> None:
        """Initialise an empty handler registry."""
        self._lock: RLock = RLock()
        self._handlers: dict[type[RuntimeEvent], list[HandlerEntry]] = {}
        self._insertion_counter: int = 0

    def subscribe(
        self,
        event_type: type[RuntimeEvent],
        handler: EventHandler,
        *,
        priority: int = 0,
    ) -> None:
        """Register a handler for a specific event type.

        Args:
            event_type: The event type to subscribe to.
            handler: Callable that will receive matching events.
            priority: Handler priority (higher values run first).

        """
        with self._lock:
            entries = self._handlers.get(event_type)
            if entries is None:
                entries = []
                self._handlers[event_type] = entries

            for entry in entries:
                if entry.handler is handler:
                    return

            self._insertion_counter += 1
            entry = HandlerEntry(
                handler=handler,
                priority=priority,
                insertion_order=self._insertion_counter,
            )
            entries.append(entry)
            entries.sort(key=_sort_key)

    def unsubscribe(
        self,
        event_type: type[RuntimeEvent],
        handler: EventHandler,
    ) -> None:
        """Remove a handler subscription for a specific event type.

        No-op if the handler is not currently subscribed.

        Args:
            event_type: The event type to unsubscribe from.
            handler: The handler to remove.

        """
        with self._lock:
            entries = self._handlers.get(event_type)
            if entries is None:
                return
            self._handlers[event_type] = [
                e for e in entries if e.handler is not handler
            ]
            if not self._handlers[event_type]:
                del self._handlers[event_type]

    def get_handlers(
        self,
        event_type: type[RuntimeEvent],
    ) -> list[HandlerEntry]:
        """Return a snapshot of handlers for an event type and its bases.

        Handlers are collected from the exact event type and all of its
        base classes up to (but not including) ``RuntimeEvent`` itself
        when no handlers are registered for ``RuntimeEvent``.  If
        handlers are registered for ``RuntimeEvent``, they are included
        as catch-all handlers.

        The returned list is a snapshot — safe to iterate while the
        registry is being mutated by other threads.

        Args:
            event_type: The event type to look up handlers for.

        Returns:
            A sorted list of handler entries (priority descending,
            insertion order ascending).

        """
        with self._lock:
            collected: list[HandlerEntry] = []
            seen_handlers: set[int] = set()

            for cls in event_type.__mro__:
                if cls is object:
                    continue
                if not issubclass(cls, RuntimeEvent):
                    continue
                entries = self._handlers.get(cls)
                if entries is not None:
                    for entry in entries:
                        handler_id = id(entry.handler)
                        if handler_id not in seen_handlers:
                            seen_handlers.add(handler_id)
                            collected.append(entry)

            collected.sort(key=_sort_key)
            return list(collected)

    def has_handlers(self, event_type: type[RuntimeEvent]) -> bool:
        """Check whether any handlers are registered for an event type.

        Checks the exact type and its base hierarchy.

        Args:
            event_type: The event type to check.

        Returns:
            True if at least one handler is registered.

        """
        with self._lock:
            for cls in event_type.__mro__:
                if cls is object:
                    continue
                if not issubclass(cls, RuntimeEvent):
                    continue
                entries = self._handlers.get(cls)
                if entries:
                    return True
            return False

    def get_registered_types(self) -> list[type[RuntimeEvent]]:
        """Return all event types that have at least one handler.

        Returns:
            List of event types with registered handlers.

        """
        with self._lock:
            return [t for t, entries in self._handlers.items() if entries]

    def clear(self) -> None:
        """Remove all handler registrations."""
        with self._lock:
            self._handlers.clear()
            self._insertion_counter = 0

    def handler_count(self) -> int:
        """Return the total number of handler registrations.

        Returns:
            Total count across all event types.

        """
        with self._lock:
            return sum(len(entries) for entries in self._handlers.values())
