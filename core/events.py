"""Thread-safe, typed event distribution with explicit delivery semantics."""

from __future__ import annotations

import asyncio
from collections import deque
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
import fnmatch
import logging
from threading import RLock
from time import perf_counter, time
from typing import Any


@dataclass(frozen=True, slots=True)
class Event:
    name: str
    payload: dict[str, Any]


EventHandler = Callable[[Event], None | Awaitable[None]]
EventFilter = Callable[[Event], bool]


@dataclass(frozen=True, slots=True)
class _Subscription:
    pattern: str
    handler: EventHandler
    priority: int
    event_filter: EventFilter | None

@dataclass(frozen=True, slots=True)
class EventDelivery:
    """Read-only diagnostic record; payloads are deliberately omitted."""
    name: str
    timestamp: float
    subscriber_count: int
    duration_ms: float
    priority: int
    error: str | None = None


class EventBus:
    """An in-process bus; async delivery never executes work on a UI caller."""
    def __init__(self, *, history_size: int = 256, logger: logging.Logger | None = None) -> None:
        if history_size < 1:
            raise ValueError("history_size must be positive")
        self._subscriptions: list[_Subscription] = []
        self._history: deque[Event] = deque(maxlen=history_size)
        self._sticky: dict[str, Event] = {}
        self._deliveries: deque[EventDelivery] = deque(maxlen=history_size)
        self._logger = logger or logging.getLogger("jochen_x.events")
        self._lock = RLock()

    def subscribe(self, event_name: str, handler: EventHandler, *, priority: int = 0,
                  event_filter: EventFilter | None = None,
                  receive_sticky: bool = True) -> Callable[[], None]:
        subscription = _Subscription(event_name, handler, priority, event_filter)
        with self._lock:
            self._subscriptions.append(subscription)
            sticky = tuple(
                event
                for name, event in self._sticky.items()
                if fnmatch.fnmatchcase(name, event_name)
            )
        if receive_sticky:
            for event in sticky:
                if event_filter is None or event_filter(event):
                    result = handler(event)
                    if asyncio.iscoroutine(result):
                        result.close()
                        raise TypeError("async handlers require publish_async")

        def unsubscribe() -> None:
            with self._lock:
                if subscription in self._subscriptions:
                    self._subscriptions.remove(subscription)
        return unsubscribe

    def publish(self, event: Event, *, sticky: bool = False) -> None:
        """Synchronously notify synchronous handlers in priority order."""
        handlers = self._record_and_select(event, sticky)
        started = perf_counter()
        error = None
        try:
            for subscription in handlers:
                result = subscription.handler(event)
                if asyncio.iscoroutine(result):
                    result.close()
                    raise TypeError("async handlers require publish_async")
        except Exception as exception:
            error = type(exception).__name__
            raise
        finally:
            self._record_delivery(event, handlers, started, error)
        self._logger.debug("event.published", extra={"context": {"event": event.name}})

    async def publish_async(self, event: Event, *, sticky: bool = False) -> None:
        """Deliver handlers as asyncio tasks, yielding before potentially expensive work."""
        handlers = self._record_and_select(event, sticky)
        started = perf_counter()
        async def invoke(subscription: _Subscription) -> None:
            result = subscription.handler(event)
            if asyncio.iscoroutine(result):
                await result
        try:
            await asyncio.gather(*(invoke(item) for item in handlers))
        except Exception as exception:
            self._record_delivery(event, handlers, started, type(exception).__name__)
            raise
        self._record_delivery(event, handlers, started, None)
        self._logger.debug("event.published_async", extra={"context": {"event": event.name}})

    def history(self) -> tuple[Event, ...]:
        with self._lock:
            return tuple(self._history)

    def delivery_history(self) -> tuple[EventDelivery, ...]:
        """Return payload-free event-monitor data without exposing subscribers."""
        with self._lock:
            return tuple(self._deliveries)

    def _record_delivery(
        self, event: Event, handlers: tuple[_Subscription, ...], started: float, error: str | None
    ) -> None:
        with self._lock:
            self._deliveries.append(EventDelivery(
                event.name,
                time(),
                len(handlers),
                (perf_counter() - started) * 1_000,
                max((item.priority for item in handlers), default=0),
                error,
            ))

    def _record_and_select(self, event: Event, sticky: bool) -> tuple[_Subscription, ...]:
        with self._lock:
            self._history.append(event)
            if sticky:
                self._sticky[event.name] = event
            selected = [
                item
                for item in self._subscriptions
                if fnmatch.fnmatchcase(event.name, item.pattern)
                and (item.event_filter is None or item.event_filter(event))
            ]
        return tuple(sorted(selected, key=lambda item: item.priority, reverse=True))
