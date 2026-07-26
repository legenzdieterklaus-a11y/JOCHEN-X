"""Unit tests for the EventBus subsystem."""

from __future__ import annotations

import threading
import time
from collections.abc import Generator
from dataclasses import dataclass

import pytest

from jochen_x.core.events.bus import EventBus
from jochen_x.core.events.handler import HandlerEntry, HandlerRegistry
from jochen_x.core.events.types import EventBusError, EventPublishError
from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.interfaces.event_bus import IEventBus
from jochen_x.core.types.events import (
    ComponentStartedEvent,
    DeadLetterEvent,
    EventHandler,
    RuntimeEvent,
)

# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------

EXPECTED_THREAD_COUNT = 400
EXPECTED_CONCURRENT_EVENTS = 200
EXPECTED_ORDERED_COUNT = 20
EXPECTED_TWO = 2
EXPECTED_PRIORITY = 5
EXPECTED_DL_LIMIT = 3


@dataclass(frozen=True, kw_only=True, slots=True)
class _TestEvent(RuntimeEvent):
    """Event subclass for testing."""

    payload: str = "test"


@dataclass(frozen=True, kw_only=True, slots=True)
class _DerivedTestEvent(_TestEvent):
    """Derived event for hierarchy tests."""

    extra: str = "derived"


def _noop_handler(_event: RuntimeEvent) -> None:
    pass


def _make_noop() -> EventHandler:
    def _handler(_event: RuntimeEvent) -> None:
        pass
    return _handler


@pytest.fixture
def registry() -> HandlerRegistry:
    return HandlerRegistry()


@pytest.fixture
def bus() -> Generator[EventBus]:
    eb = EventBus()
    eb.initialize()
    eb.start()
    yield eb
    if eb.is_running():
        eb.stop()


@pytest.fixture
def stopped_bus() -> EventBus:
    return EventBus()


# ===========================================================================
# HandlerEntry tests
# ===========================================================================


class TestHandlerEntry:
    def test_creation(self) -> None:
        entry = HandlerEntry(
            handler=_noop_handler,
            priority=EXPECTED_PRIORITY,
            insertion_order=1,
        )
        assert entry.handler is _noop_handler
        assert entry.priority == EXPECTED_PRIORITY
        assert entry.insertion_order == 1

    def test_frozen(self) -> None:
        entry = HandlerEntry(handler=_noop_handler, priority=0, insertion_order=1)
        with pytest.raises(AttributeError):
            entry.priority = 10  # type: ignore[misc]


# ===========================================================================
# HandlerRegistry tests
# ===========================================================================


class TestHandlerRegistry:
    def test_subscribe_and_get_handlers(self, registry: HandlerRegistry) -> None:
        registry.subscribe(_TestEvent, _noop_handler)
        entries = registry.get_handlers(_TestEvent)
        assert len(entries) == 1
        assert entries[0].handler is _noop_handler

    def test_subscribe_duplicate_ignored(self, registry: HandlerRegistry) -> None:
        registry.subscribe(_TestEvent, _noop_handler)
        registry.subscribe(_TestEvent, _noop_handler)
        assert registry.handler_count() == 1

    def test_unsubscribe(self, registry: HandlerRegistry) -> None:
        registry.subscribe(_TestEvent, _noop_handler)
        registry.unsubscribe(_TestEvent, _noop_handler)
        assert registry.get_handlers(_TestEvent) == []

    def test_unsubscribe_unknown_noop(self, registry: HandlerRegistry) -> None:
        registry.unsubscribe(_TestEvent, _noop_handler)

    def test_priority_ordering(self, registry: HandlerRegistry) -> None:
        h_low = _make_noop()
        h_mid = _make_noop()
        h_high = _make_noop()

        registry.subscribe(_TestEvent, h_low, priority=1)
        registry.subscribe(_TestEvent, h_mid, priority=5)
        registry.subscribe(_TestEvent, h_high, priority=10)

        entries = registry.get_handlers(_TestEvent)
        assert entries[0].handler is h_high
        assert entries[1].handler is h_mid
        assert entries[2].handler is h_low

    def test_same_priority_insertion_order(self, registry: HandlerRegistry) -> None:
        h1 = _make_noop()
        h2 = _make_noop()
        h3 = _make_noop()

        registry.subscribe(_TestEvent, h1, priority=0)
        registry.subscribe(_TestEvent, h2, priority=0)
        registry.subscribe(_TestEvent, h3, priority=0)

        entries = registry.get_handlers(_TestEvent)
        assert entries[0].handler is h1
        assert entries[1].handler is h2
        assert entries[2].handler is h3

    def test_base_type_handlers_receive_derived_events(
        self, registry: HandlerRegistry
    ) -> None:
        registry.subscribe(_TestEvent, _noop_handler)
        entries = registry.get_handlers(_DerivedTestEvent)
        assert len(entries) == 1
        assert entries[0].handler is _noop_handler

    def test_runtime_event_handler_catches_all(
        self, registry: HandlerRegistry
    ) -> None:
        registry.subscribe(RuntimeEvent, _noop_handler)
        entries = registry.get_handlers(_TestEvent)
        assert len(entries) == 1

    def test_has_handlers(self, registry: HandlerRegistry) -> None:
        assert not registry.has_handlers(_TestEvent)
        registry.subscribe(_TestEvent, _noop_handler)
        assert registry.has_handlers(_TestEvent)

    def test_has_handlers_via_hierarchy(self, registry: HandlerRegistry) -> None:
        registry.subscribe(RuntimeEvent, _noop_handler)
        assert registry.has_handlers(_TestEvent)

    def test_get_registered_types(self, registry: HandlerRegistry) -> None:
        h1 = _make_noop()
        h2 = _make_noop()
        registry.subscribe(_TestEvent, h1)
        registry.subscribe(ComponentStartedEvent, h2)
        types = registry.get_registered_types()
        assert set(types) == {_TestEvent, ComponentStartedEvent}

    def test_clear(self, registry: HandlerRegistry) -> None:
        registry.subscribe(_TestEvent, _noop_handler)
        registry.clear()
        assert registry.handler_count() == 0
        assert registry.get_handlers(_TestEvent) == []

    def test_handler_count(self, registry: HandlerRegistry) -> None:
        h1 = _make_noop()
        h2 = _make_noop()
        registry.subscribe(_TestEvent, h1)
        registry.subscribe(ComponentStartedEvent, h2)
        assert registry.handler_count() == EXPECTED_TWO

    def test_get_handlers_no_duplicates_in_hierarchy(
        self, registry: HandlerRegistry
    ) -> None:
        registry.subscribe(_TestEvent, _noop_handler)
        registry.subscribe(RuntimeEvent, _noop_handler)
        entries = registry.get_handlers(_TestEvent)
        handlers = [e.handler for e in entries]
        assert handlers.count(_noop_handler) == 1

    def test_thread_safety_concurrent_subscribe(
        self, registry: HandlerRegistry
    ) -> None:
        errors: list[Exception] = []

        def subscribe_many(start: int) -> None:
            try:
                for i in range(100):
                    def _h(_event: RuntimeEvent, _idx: int = i + start) -> None:
                        pass
                    registry.subscribe(_TestEvent, _h)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=subscribe_many, args=(i * 100,))
            for i in range(4)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert registry.handler_count() == EXPECTED_THREAD_COUNT


# ===========================================================================
# EventBus construction tests
# ===========================================================================


class TestEventBusConstruction:
    def test_default_construction(self) -> None:
        eb = EventBus()
        assert not eb.is_running()
        assert eb.get_queue_size() == 0
        assert eb.get_dead_letter_count() == 0

    def test_custom_capacities(self) -> None:
        eb = EventBus(queue_capacity=100, dead_letter_capacity=50)
        assert not eb.is_running()

    def test_invalid_queue_capacity(self) -> None:
        with pytest.raises(InputValidationError) as exc_info:
            EventBus(queue_capacity=0)
        assert "queue_capacity" in str(exc_info.value)

    def test_negative_dead_letter_capacity(self) -> None:
        with pytest.raises(InputValidationError) as exc_info:
            EventBus(dead_letter_capacity=-1)
        assert "dead_letter_capacity" in str(exc_info.value)


# ===========================================================================
# EventBus lifecycle tests
# ===========================================================================


class TestEventBusLifecycle:
    def test_initialize_start_stop(self) -> None:
        eb = EventBus()
        eb.initialize()
        eb.start()
        assert eb.is_running()
        eb.stop()
        assert not eb.is_running()

    def test_double_start_raises(self) -> None:
        eb = EventBus()
        eb.initialize()
        eb.start()
        with pytest.raises(EventBusError):
            eb.start()
        eb.stop()

    def test_stop_before_start_raises(self) -> None:
        eb = EventBus()
        with pytest.raises(EventBusError):
            eb.stop()

    def test_double_stop_raises(self) -> None:
        eb = EventBus()
        eb.initialize()
        eb.start()
        eb.stop()
        with pytest.raises(EventBusError):
            eb.stop()

    def test_reinitialize_after_stop(self) -> None:
        eb = EventBus()
        eb.initialize()
        eb.start()
        eb.stop()
        eb.initialize()
        eb.start()
        assert eb.is_running()
        eb.stop()

    def test_initialize_while_running_raises(self) -> None:
        eb = EventBus()
        eb.initialize()
        eb.start()
        with pytest.raises(EventBusError):
            eb.initialize()
        eb.stop()


# ===========================================================================
# EventBus subscribe/unsubscribe tests
# ===========================================================================


class TestEventBusSubscription:
    def test_subscribe_valid(self, bus: EventBus) -> None:
        bus.subscribe(_TestEvent, _noop_handler)
        assert bus.get_handler_count() == 1

    def test_subscribe_invalid_event_type(self, bus: EventBus) -> None:
        with pytest.raises(InputValidationError) as exc_info:
            bus.subscribe(str, _noop_handler)  # type: ignore[arg-type]
        assert "event_type" in str(exc_info.value)

    def test_subscribe_non_callable_handler(self, bus: EventBus) -> None:
        with pytest.raises(InputValidationError) as exc_info:
            bus.subscribe(_TestEvent, "not_callable")  # type: ignore[arg-type]
        assert "handler" in str(exc_info.value)

    def test_unsubscribe(self, bus: EventBus) -> None:
        bus.subscribe(_TestEvent, _noop_handler)
        bus.unsubscribe(_TestEvent, _noop_handler)
        assert bus.get_handler_count() == 0

    def test_unsubscribe_unknown_noop(self, bus: EventBus) -> None:
        bus.unsubscribe(_TestEvent, _noop_handler)

    def test_subscribe_before_start(self) -> None:
        eb = EventBus()
        eb.subscribe(_TestEvent, _noop_handler)
        assert eb.get_handler_count() == 1


# ===========================================================================
# EventBus publish tests
# ===========================================================================


class TestEventBusPublish:
    def test_publish_delivers_to_handler(self, bus: EventBus) -> None:
        received: list[RuntimeEvent] = []

        def handler(event: RuntimeEvent) -> None:
            received.append(event)

        bus.subscribe(_TestEvent, handler)

        event = _TestEvent(source="test")
        bus.publish(event)
        time.sleep(0.1)

        assert len(received) == 1
        assert received[0] is event

    def test_publish_to_base_type_handler(self, bus: EventBus) -> None:
        received: list[RuntimeEvent] = []

        def handler(event: RuntimeEvent) -> None:
            received.append(event)

        bus.subscribe(RuntimeEvent, handler)
        bus.publish(_TestEvent(source="test"))
        time.sleep(0.1)

        assert len(received) == 1

    def test_publish_derived_to_parent_handler(self, bus: EventBus) -> None:
        received: list[RuntimeEvent] = []

        def handler(event: RuntimeEvent) -> None:
            received.append(event)

        bus.subscribe(_TestEvent, handler)

        event = _DerivedTestEvent(source="test", extra="hello")
        bus.publish(event)
        time.sleep(0.1)

        assert len(received) == 1
        assert isinstance(received[0], _DerivedTestEvent)

    def test_publish_when_not_running_raises(self, stopped_bus: EventBus) -> None:
        event = _TestEvent(source="test")
        with pytest.raises(EventPublishError):
            stopped_bus.publish(event)

    def test_publish_non_event_raises(self, bus: EventBus) -> None:
        with pytest.raises(InputValidationError):
            bus.publish("not_an_event")  # type: ignore[arg-type]

    def test_publish_priority_order(self, bus: EventBus) -> None:
        order: list[str] = []

        def h_low(_event: RuntimeEvent) -> None:
            order.append("low")

        def h_high(_event: RuntimeEvent) -> None:
            order.append("high")

        bus.subscribe(_TestEvent, h_low, priority=1)
        bus.subscribe(_TestEvent, h_high, priority=10)

        bus.publish(_TestEvent(source="test"))
        time.sleep(0.1)

        assert order == ["high", "low"]

    def test_publish_same_priority_insertion_order(self, bus: EventBus) -> None:
        order: list[int] = []

        def make_handler(idx: int) -> EventHandler:
            def h(_event: RuntimeEvent) -> None:
                order.append(idx)
            return h

        for i in range(5):
            bus.subscribe(_TestEvent, make_handler(i), priority=0)

        bus.publish(_TestEvent(source="test"))
        time.sleep(0.1)

        assert order == [0, 1, 2, 3, 4]

    def test_publish_multiple_events_order(self, bus: EventBus) -> None:
        received: list[str] = []

        def handler(event: RuntimeEvent) -> None:
            if isinstance(event, _TestEvent):
                received.append(event.payload)

        bus.subscribe(_TestEvent, handler)

        for i in range(10):
            bus.publish(_TestEvent(source="test", payload=str(i)))

        time.sleep(0.2)
        assert received == [str(i) for i in range(10)]


# ===========================================================================
# Dead-letter queue tests
# ===========================================================================


class TestDeadLetterQueue:
    def test_no_handler_goes_to_dead_letter(self, bus: EventBus) -> None:
        bus.publish(_TestEvent(source="test"))
        time.sleep(0.1)

        dead = bus.get_dead_letters()
        assert len(dead) == 1
        assert dead[0].original_event_type == "_TestEvent"
        assert "No handlers" in dead[0].error_message

    def test_handler_exception_creates_dead_letter(self, bus: EventBus) -> None:
        def failing_handler(_event: RuntimeEvent) -> None:
            msg = "handler boom"
            raise ValueError(msg)

        bus.subscribe(_TestEvent, failing_handler)
        bus.publish(_TestEvent(source="test"))
        time.sleep(0.1)

        dead = bus.get_dead_letters()
        assert len(dead) == 1
        assert "handler boom" in dead[0].error_message

    def test_one_handler_fails_others_still_called(self, bus: EventBus) -> None:
        received: list[RuntimeEvent] = []

        def failing_handler(_event: RuntimeEvent) -> None:
            msg = "fail"
            raise ValueError(msg)

        def good_handler(event: RuntimeEvent) -> None:
            received.append(event)

        bus.subscribe(_TestEvent, failing_handler, priority=10)
        bus.subscribe(_TestEvent, good_handler, priority=1)

        bus.publish(_TestEvent(source="test"))
        time.sleep(0.1)

        assert len(received) == 1

    def test_clear_dead_letters(self, bus: EventBus) -> None:
        bus.publish(_TestEvent(source="test"))
        time.sleep(0.1)

        bus.clear_dead_letters()
        assert bus.get_dead_letter_count() == 0

    def test_dead_letter_capacity_limit(self) -> None:
        eb = EventBus(dead_letter_capacity=3)
        eb.initialize()
        eb.start()

        for _ in range(5):
            eb.publish(_TestEvent(source="test"))

        time.sleep(0.2)
        dead = eb.get_dead_letters()
        assert len(dead) <= EXPECTED_DL_LIMIT
        eb.stop()

    def test_dead_letter_event_not_dead_lettered_again(self, bus: EventBus) -> None:
        dead_letter = DeadLetterEvent(
            original_event_id="abc",
            original_event_type="SomeEvent",
            handler_name="",
            error_message="test",
            source="test",
        )
        bus.publish(dead_letter)
        time.sleep(0.1)

        assert bus.get_dead_letter_count() == 0


# ===========================================================================
# Handler mutation during dispatch tests
# ===========================================================================


class TestHandlerMutationDuringDispatch:
    def test_handler_subscribes_during_dispatch(self, bus: EventBus) -> None:
        late_received: list[RuntimeEvent] = []

        def late_handler(event: RuntimeEvent) -> None:
            late_received.append(event)

        def subscribing_handler(_event: RuntimeEvent) -> None:
            bus.subscribe(ComponentStartedEvent, late_handler)

        bus.subscribe(_TestEvent, subscribing_handler)
        bus.publish(_TestEvent(source="test"))
        time.sleep(0.1)

        bus.publish(ComponentStartedEvent(source="test", component_name="x"))
        time.sleep(0.1)

        assert len(late_received) == 1

    def test_handler_unsubscribes_during_dispatch(self, bus: EventBus) -> None:
        call_count = 0

        def self_unsubscribing_handler(_event: RuntimeEvent) -> None:
            nonlocal call_count
            call_count += 1
            bus.unsubscribe(_TestEvent, self_unsubscribing_handler)

        bus.subscribe(_TestEvent, self_unsubscribing_handler)
        bus.publish(_TestEvent(source="test"))
        bus.publish(_TestEvent(source="test"))
        time.sleep(0.2)

        assert call_count == 1


# ===========================================================================
# Queue overflow tests
# ===========================================================================


class TestQueueOverflow:
    def test_overflow_drops_oldest(self) -> None:
        eb = EventBus(queue_capacity=2)
        eb.initialize()

        received: list[str] = []
        barrier = threading.Event()

        def slow_handler(event: RuntimeEvent) -> None:
            barrier.wait(timeout=5.0)
            if isinstance(event, _TestEvent):
                received.append(event.payload)

        eb.subscribe(_TestEvent, slow_handler)
        eb.start()

        eb.publish(_TestEvent(source="test", payload="first"))
        time.sleep(0.05)
        eb.publish(_TestEvent(source="test", payload="second"))
        eb.publish(_TestEvent(source="test", payload="third"))
        eb.publish(_TestEvent(source="test", payload="fourth"))

        barrier.set()
        time.sleep(0.3)

        assert eb.get_dead_letter_count() >= 1
        eb.stop()


# ===========================================================================
# Thread safety tests
# ===========================================================================


class TestThreadSafety:
    def test_concurrent_publish(self, bus: EventBus) -> None:
        received: list[RuntimeEvent] = []
        lock = threading.Lock()

        def handler(event: RuntimeEvent) -> None:
            with lock:
                received.append(event)

        bus.subscribe(_TestEvent, handler)

        errors: list[Exception] = []

        def publish_many() -> None:
            try:
                for _ in range(50):
                    bus.publish(_TestEvent(source="test"))
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=publish_many) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        time.sleep(0.5)

        assert not errors
        assert len(received) == EXPECTED_CONCURRENT_EVENTS

    def test_concurrent_subscribe_unsubscribe(self, bus: EventBus) -> None:
        errors: list[Exception] = []

        def subscribe_task() -> None:
            try:
                for _ in range(50):
                    h = _make_noop()
                    bus.subscribe(_TestEvent, h)
                    bus.unsubscribe(_TestEvent, h)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=subscribe_task) for _ in range(4)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors

    def test_concurrent_publish_and_subscribe(self, bus: EventBus) -> None:
        errors: list[Exception] = []

        def publish_task() -> None:
            try:
                for _ in range(50):
                    bus.publish(_TestEvent(source="test"))
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        def subscribe_task() -> None:
            try:
                for _ in range(50):
                    h = _make_noop()
                    bus.subscribe(_TestEvent, h)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=publish_task),
            threading.Thread(target=subscribe_task),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        time.sleep(0.3)
        assert not errors


# ===========================================================================
# Graceful shutdown tests
# ===========================================================================

EXPECTED_SHUTDOWN_EVENTS = 2
EXPECTED_DRAIN_EVENTS = 20


class TestGracefulShutdown:
    def test_stop_processes_remaining_events(self) -> None:
        received: list[RuntimeEvent] = []
        barrier = threading.Event()

        def blocking_handler(event: RuntimeEvent) -> None:
            barrier.wait(timeout=5.0)
            received.append(event)

        eb = EventBus()
        eb.initialize()
        eb.subscribe(_TestEvent, blocking_handler)
        eb.start()

        eb.publish(_TestEvent(source="test", payload="a"))
        eb.publish(_TestEvent(source="test", payload="b"))
        time.sleep(0.05)

        barrier.set()
        eb.stop()

        assert len(received) == EXPECTED_SHUTDOWN_EVENTS

    def test_stop_empties_queue(self) -> None:
        received: list[RuntimeEvent] = []

        def handler(event: RuntimeEvent) -> None:
            received.append(event)

        eb = EventBus()
        eb.initialize()
        eb.subscribe(_TestEvent, handler)
        eb.start()

        for i in range(EXPECTED_DRAIN_EVENTS):
            eb.publish(_TestEvent(source="test", payload=str(i)))

        eb.stop()
        assert len(received) == EXPECTED_DRAIN_EVENTS
        assert eb.get_queue_size() == 0


# ===========================================================================
# Introspection tests
# ===========================================================================


class TestIntrospection:
    def test_get_handler_count(self, bus: EventBus) -> None:
        assert bus.get_handler_count() == 0
        bus.subscribe(_TestEvent, _noop_handler)
        assert bus.get_handler_count() == 1

    def test_get_queue_size(self, bus: EventBus) -> None:
        assert bus.get_queue_size() == 0

    def test_get_dead_letter_count(self, bus: EventBus) -> None:
        assert bus.get_dead_letter_count() == 0

    def test_is_running(self, bus: EventBus) -> None:
        assert bus.is_running()


# ===========================================================================
# IEventBus protocol compliance test
# ===========================================================================


class TestProtocolCompliance:
    def test_event_bus_implements_ieventbus(self) -> None:
        eb = EventBus()
        assert isinstance(eb, IEventBus)

    def test_event_bus_has_lifecycle_methods(self) -> None:
        eb = EventBus()
        assert hasattr(eb, "initialize")
        assert hasattr(eb, "start")
        assert hasattr(eb, "stop")
