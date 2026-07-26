"""EventBus implementation for typed, asynchronous event distribution.

The ``EventBus`` is the central mechanism for inter-component
communication within the JOCHEN X Core Runtime.  It distributes
typed events asynchronously to registered handlers, supports
priority-based dispatch, and maintains a dead-letter queue for
events that could not be delivered.

All operations are thread-safe.  Handlers may subscribe or
unsubscribe during event dispatch without corrupting the bus.
"""

from __future__ import annotations

from collections import deque
from enum import Enum, unique
from threading import Condition, RLock, Thread

from jochen_x.core.events.handler import HandlerRegistry
from jochen_x.core.events.types import EventBusError, EventPublishError
from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.types.events import (
    DeadLetterEvent,
    EventHandler,
    RuntimeEvent,
)

__all__ = ["EventBus"]

DEFAULT_QUEUE_CAPACITY = 10_000
DEFAULT_DEAD_LETTER_CAPACITY = 1_000

_FIELD_QUEUE_CAPACITY = "queue_capacity"
_FIELD_DEAD_LETTER_CAPACITY = "dead_letter_capacity"
_FIELD_EVENT = "event"
_FIELD_EVENT_TYPE = "event_type"
_FIELD_HANDLER = "handler"
_REASON_MIN_ONE = "must be at least 1"
_REASON_NOT_NEGATIVE = "must not be negative"
_REASON_NOT_CALLABLE = "must be callable"


@unique
class _BusState(Enum):
    """Internal lifecycle states of the EventBus."""

    CREATED = "CREATED"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"


def _state_msg(action: str, state: _BusState) -> str:
    """Build an error message for illegal state transitions."""
    return f"Cannot {action} EventBus in state {state.value}"


class EventBus:
    """Asynchronous, priority-based event bus with dead-letter queue.

    The EventBus processes events on a dedicated background thread,
    ensuring that event publishing never blocks the caller beyond
    queue insertion.  Handlers are invoked in priority order (higher
    values first); within the same priority, insertion order is
    preserved.

    Events that cannot be delivered — either because no handler is
    registered or because all handlers fail — are placed into the
    dead-letter queue.

    Args:
        queue_capacity: Maximum number of events in the dispatch
            queue.  Oldest events are dropped when exceeded.
        dead_letter_capacity: Maximum number of events retained
            in the dead-letter queue.

    """

    def __init__(
        self,
        *,
        queue_capacity: int = DEFAULT_QUEUE_CAPACITY,
        dead_letter_capacity: int = DEFAULT_DEAD_LETTER_CAPACITY,
    ) -> None:
        """Initialise the EventBus in CREATED state."""
        if queue_capacity < 1:
            raise InputValidationError(
                _FIELD_QUEUE_CAPACITY,
                _REASON_MIN_ONE,
                component="EventBus",
            )
        if dead_letter_capacity < 0:
            raise InputValidationError(
                _FIELD_DEAD_LETTER_CAPACITY,
                _REASON_NOT_NEGATIVE,
                component="EventBus",
            )

        self._queue_capacity: int = queue_capacity
        self._dead_letter_capacity: int = dead_letter_capacity

        self._registry: HandlerRegistry = HandlerRegistry()
        self._queue: deque[RuntimeEvent] = deque()
        self._dead_letters: deque[DeadLetterEvent] = deque(
            maxlen=dead_letter_capacity if dead_letter_capacity > 0 else None,
        )

        self._lock: RLock = RLock()
        self._condition: Condition = Condition(self._lock)
        self._state: _BusState = _BusState.CREATED
        self._dispatch_thread: Thread | None = None

    # ------------------------------------------------------------------
    # ILifecycle
    # ------------------------------------------------------------------

    def initialize(self) -> None:
        """Initialise the EventBus.

        Prepares internal structures.  Must be called before ``start``.

        Raises:
            EventBusError: If the bus is not in CREATED or STOPPED state.

        """
        with self._lock:
            if self._state not in (_BusState.CREATED, _BusState.STOPPED):
                msg = _state_msg("initialise", self._state)
                raise EventBusError(msg)
            self._queue.clear()
            self._state = _BusState.CREATED

    def start(self) -> None:
        """Start the background dispatch thread.

        Raises:
            EventBusError: If the bus is not in CREATED state.

        """
        with self._lock:
            if self._state != _BusState.CREATED:
                msg = _state_msg("start", self._state)
                raise EventBusError(msg)
            self._state = _BusState.RUNNING
            self._dispatch_thread = Thread(
                target=self._dispatch_loop,
                name="EventBus-Dispatch",
                daemon=True,
            )
            self._dispatch_thread.start()

    def stop(self) -> None:
        """Stop the EventBus and process remaining events.

        Blocks until all queued events have been dispatched and the
        background thread has terminated.

        Raises:
            EventBusError: If the bus is not in RUNNING state.

        """
        thread: Thread | None = None
        with self._lock:
            if self._state != _BusState.RUNNING:
                msg = _state_msg("stop", self._state)
                raise EventBusError(msg)
            self._state = _BusState.STOPPING
            self._condition.notify_all()
            thread = self._dispatch_thread

        if thread is not None:
            thread.join(timeout=30.0)

        with self._lock:
            self._state = _BusState.STOPPED
            self._dispatch_thread = None

    # ------------------------------------------------------------------
    # IEventBus
    # ------------------------------------------------------------------

    def publish(self, event: RuntimeEvent) -> None:
        """Publish an event to all matching handlers.

        The event is enqueued for asynchronous dispatch on the
        background thread.  If the queue is at capacity, the oldest
        event is dropped and a ``DeadLetterEvent`` is created for it.

        Args:
            event: The event to publish.

        Raises:
            InputValidationError: If event is not a RuntimeEvent.
            EventPublishError: If the bus is not operational.

        """
        if not isinstance(event, RuntimeEvent):
            reason = f"expected RuntimeEvent, got {type(event).__name__}"
            raise InputValidationError(
                _FIELD_EVENT,
                reason,
                component="EventBus",
            )

        with self._lock:
            if self._state != _BusState.RUNNING:
                msg = f"EventBus is not operational (state={self._state.value})"
                raise EventPublishError(msg)

            if len(self._queue) >= self._queue_capacity:
                dropped = self._queue.popleft()
                self._record_dead_letter(
                    dropped,
                    handler_name="",
                    error_message="Event dropped: dispatch queue overflow",
                )

            self._queue.append(event)
            self._condition.notify()

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
        if not isinstance(event_type, type) or not issubclass(
            event_type, RuntimeEvent
        ):
            reason = f"must be a subclass of RuntimeEvent, got {event_type!r}"
            raise InputValidationError(
                _FIELD_EVENT_TYPE,
                reason,
                component="EventBus",
            )
        if not callable(handler):
            raise InputValidationError(
                _FIELD_HANDLER,
                _REASON_NOT_CALLABLE,
                component="EventBus",
            )

        self._registry.subscribe(event_type, handler, priority=priority)

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
        self._registry.unsubscribe(event_type, handler)

    # ------------------------------------------------------------------
    # Dead-letter queue access
    # ------------------------------------------------------------------

    def get_dead_letters(self) -> list[DeadLetterEvent]:
        """Return a snapshot of the dead-letter queue.

        Returns:
            List of dead-letter events, oldest first.

        """
        with self._lock:
            return list(self._dead_letters)

    def clear_dead_letters(self) -> None:
        """Clear the dead-letter queue."""
        with self._lock:
            self._dead_letters.clear()

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def get_handler_count(self) -> int:
        """Return the total number of handler registrations.

        Returns:
            Total handler count across all event types.

        """
        return self._registry.handler_count()

    def get_queue_size(self) -> int:
        """Return the current number of events in the dispatch queue.

        Returns:
            Number of pending events.

        """
        with self._lock:
            return len(self._queue)

    def get_dead_letter_count(self) -> int:
        """Return the number of events in the dead-letter queue.

        Returns:
            Dead-letter count.

        """
        with self._lock:
            return len(self._dead_letters)

    def is_running(self) -> bool:
        """Check whether the EventBus is currently operational.

        Returns:
            True if the bus is in RUNNING state.

        """
        with self._lock:
            return self._state == _BusState.RUNNING

    # ------------------------------------------------------------------
    # Internal dispatch
    # ------------------------------------------------------------------

    def _dispatch_loop(self) -> None:
        """Background loop that processes events from the queue.

        Runs until the state transitions to STOPPING and the queue
        is empty.  Uses a condition variable to avoid busy-waiting.
        """
        while True:
            event: RuntimeEvent | None = None

            with self._lock:
                while not self._queue and self._state == _BusState.RUNNING:
                    self._condition.wait()

                if self._queue:
                    event = self._queue.popleft()
                elif self._state != _BusState.RUNNING:
                    return

            if event is not None:
                self._dispatch_event(event)

    def _dispatch_event(self, event: RuntimeEvent) -> None:
        """Dispatch a single event to all matching handlers.

        Handler exceptions are caught individually — one handler's
        failure does not prevent other handlers from receiving the
        event.  If no handlers are found, or if all handlers fail,
        the event is placed into the dead-letter queue.

        Args:
            event: The event to dispatch.

        """
        entries = self._registry.get_handlers(type(event))

        if not entries:
            if not isinstance(event, DeadLetterEvent):
                self._record_dead_letter(
                    event,
                    handler_name="",
                    error_message="No handlers registered for event type",
                )
            return

        all_failed = True
        for entry in entries:
            try:
                entry.handler(event)
                all_failed = False
            except Exception as exc:  # noqa: BLE001
                handler_name = getattr(
                    entry.handler, "__qualname__",
                    getattr(entry.handler, "__name__", repr(entry.handler)),
                )
                if not isinstance(event, DeadLetterEvent):
                    self._record_dead_letter(
                        event,
                        handler_name=handler_name,
                        error_message=str(exc),
                    )

        if all_failed and not isinstance(event, DeadLetterEvent):
            pass

    def _record_dead_letter(
        self,
        event: RuntimeEvent,
        *,
        handler_name: str,
        error_message: str,
    ) -> None:
        """Record an undeliverable event in the dead-letter queue.

        Args:
            event: The original undeliverable event.
            handler_name: Name of the handler that failed (empty
                if no handler was found).
            error_message: Description of the failure.

        """
        dead_letter = DeadLetterEvent(
            original_event_id=event.event_id,
            original_event_type=type(event).__name__,
            handler_name=handler_name,
            error_message=error_message,
            source="EventBus",
        )

        with self._lock:
            self._dead_letters.append(dead_letter)
