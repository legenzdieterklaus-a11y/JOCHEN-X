"""Integration tests for EventBus with real handlers and runtime events."""

from __future__ import annotations

import threading
import time
from collections.abc import Generator

import pytest

from jochen_x.core.events.bus import EventBus
from jochen_x.core.types.events import (
    ComponentStartedEvent,
    ComponentStoppedEvent,
    DeadLetterEvent,
    EventHandler,
    HealthStatusChangedEvent,
    RecoveryInitiatedEvent,
    RuntimeEvent,
    RuntimeStateChangedEvent,
    SecurityViolationEvent,
)
from jochen_x.core.types.health_status import HealthStatus
from jochen_x.core.types.recovery_level import RecoveryLevel
from jochen_x.core.types.runtime_state import RuntimeState

EXPECTED_CATCH_ALL_COUNT = 3
EXPECTED_RESTART_CYCLES = 3
EXPECTED_DRAIN_COUNT = 50
EXPECTED_FIFO_COUNT = 20
EXPECTED_THROUGHPUT_COUNT = 400


@pytest.fixture
def bus() -> Generator[EventBus]:
    eb = EventBus()
    eb.initialize()
    eb.start()
    yield eb
    if eb.is_running():
        eb.stop()


# ===========================================================================
# Real event type tests
# ===========================================================================


class TestRealEventTypes:
    def test_runtime_state_changed_event(self, bus: EventBus) -> None:
        received: list[RuntimeStateChangedEvent] = []

        def handler(event: RuntimeEvent) -> None:
            if isinstance(event, RuntimeStateChangedEvent):
                received.append(event)

        bus.subscribe(RuntimeStateChangedEvent, handler)
        bus.publish(
            RuntimeStateChangedEvent(
                source="RuntimeHost",
                old_state=RuntimeState.CREATED,
                new_state=RuntimeState.BOOTSTRAPPING,
            )
        )
        time.sleep(0.1)

        assert len(received) == 1
        assert received[0].old_state == RuntimeState.CREATED
        assert received[0].new_state == RuntimeState.BOOTSTRAPPING

    def test_health_status_changed_event(self, bus: EventBus) -> None:
        received: list[HealthStatusChangedEvent] = []

        def handler(event: RuntimeEvent) -> None:
            if isinstance(event, HealthStatusChangedEvent):
                received.append(event)

        bus.subscribe(HealthStatusChangedEvent, handler)
        bus.publish(
            HealthStatusChangedEvent(
                source="HealthMonitor",
                component_name="WorkerPool",
                old_status=HealthStatus.HEALTHY,
                new_status=HealthStatus.DEGRADED,
            )
        )
        time.sleep(0.1)

        assert len(received) == 1
        assert received[0].component_name == "WorkerPool"

    def test_security_violation_event(self, bus: EventBus) -> None:
        received: list[SecurityViolationEvent] = []

        def handler(event: RuntimeEvent) -> None:
            if isinstance(event, SecurityViolationEvent):
                received.append(event)

        bus.subscribe(SecurityViolationEvent, handler)
        bus.publish(
            SecurityViolationEvent(
                source="SecurityManager",
                violation_type="PERMISSION_DENIED",
                details="Attempted unauthorized access",
                component_name="PluginX",
            )
        )
        time.sleep(0.1)

        assert len(received) == 1
        assert received[0].violation_type == "PERMISSION_DENIED"

    def test_recovery_initiated_event(self, bus: EventBus) -> None:
        received: list[RecoveryInitiatedEvent] = []

        def handler(event: RuntimeEvent) -> None:
            if isinstance(event, RecoveryInitiatedEvent):
                received.append(event)

        bus.subscribe(RecoveryInitiatedEvent, handler)
        bus.publish(
            RecoveryInitiatedEvent(
                source="RecoveryHandler",
                component_name="Scheduler",
                level=RecoveryLevel.COMPONENT_RETRY,
                reason="Health check failure",
            )
        )
        time.sleep(0.1)

        assert len(received) == 1
        assert received[0].level == RecoveryLevel.COMPONENT_RETRY


# ===========================================================================
# Cross-component communication
# ===========================================================================


class TestCrossComponentCommunication:
    def test_multiple_subscribers_different_types(self, bus: EventBus) -> None:
        health_events: list[RuntimeEvent] = []
        state_events: list[RuntimeEvent] = []

        def health_handler(event: RuntimeEvent) -> None:
            health_events.append(event)

        def state_handler(event: RuntimeEvent) -> None:
            state_events.append(event)

        bus.subscribe(HealthStatusChangedEvent, health_handler)
        bus.subscribe(RuntimeStateChangedEvent, state_handler)

        bus.publish(
            HealthStatusChangedEvent(
                source="HealthMonitor",
                component_name="EventBus",
                old_status=HealthStatus.UNKNOWN,
                new_status=HealthStatus.HEALTHY,
            )
        )
        bus.publish(
            RuntimeStateChangedEvent(
                source="RuntimeHost",
                old_state=RuntimeState.READY,
                new_state=RuntimeState.STARTING,
            )
        )

        time.sleep(0.15)

        assert len(health_events) == 1
        assert len(state_events) == 1

    def test_catch_all_handler_receives_everything(self, bus: EventBus) -> None:
        all_events: list[RuntimeEvent] = []

        def catch_all(event: RuntimeEvent) -> None:
            all_events.append(event)

        bus.subscribe(RuntimeEvent, catch_all)

        bus.publish(ComponentStartedEvent(source="test", component_name="A"))
        bus.publish(ComponentStoppedEvent(source="test", component_name="B"))
        bus.publish(
            HealthStatusChangedEvent(
                source="test",
                component_name="C",
                old_status=HealthStatus.HEALTHY,
                new_status=HealthStatus.UNHEALTHY,
            )
        )

        time.sleep(0.15)

        assert len(all_events) == EXPECTED_CATCH_ALL_COUNT

    def test_event_chain_reaction(self, bus: EventBus) -> None:
        chain: list[str] = []

        def component_started_handler(event: RuntimeEvent) -> None:
            if isinstance(event, ComponentStartedEvent):
                chain.append(f"started:{event.component_name}")
                bus.publish(
                    HealthStatusChangedEvent(
                        source="test",
                        component_name=event.component_name,
                        old_status=HealthStatus.UNKNOWN,
                        new_status=HealthStatus.HEALTHY,
                    )
                )

        def health_handler(event: RuntimeEvent) -> None:
            if isinstance(event, HealthStatusChangedEvent):
                chain.append(f"healthy:{event.component_name}")

        bus.subscribe(ComponentStartedEvent, component_started_handler)
        bus.subscribe(HealthStatusChangedEvent, health_handler)

        bus.publish(
            ComponentStartedEvent(source="test", component_name="WorkerPool")
        )
        time.sleep(0.2)

        assert "started:WorkerPool" in chain
        assert "healthy:WorkerPool" in chain


# ===========================================================================
# Dead-letter queue integration
# ===========================================================================


class TestDeadLetterIntegration:
    def test_all_handlers_fail_creates_dead_letter(self, bus: EventBus) -> None:
        def failing_1(_event: RuntimeEvent) -> None:
            msg = "fail_1"
            raise RuntimeError(msg)

        def failing_2(_event: RuntimeEvent) -> None:
            msg = "fail_2"
            raise RuntimeError(msg)

        bus.subscribe(ComponentStartedEvent, failing_1, priority=10)
        bus.subscribe(ComponentStartedEvent, failing_2, priority=1)

        bus.publish(ComponentStartedEvent(source="test", component_name="X"))
        time.sleep(0.15)

        dead = bus.get_dead_letters()
        assert len(dead) >= 1
        assert all(isinstance(d, DeadLetterEvent) for d in dead)

    def test_partial_handler_failure(self, bus: EventBus) -> None:
        received: list[RuntimeEvent] = []

        def good_handler(event: RuntimeEvent) -> None:
            received.append(event)

        def bad_handler(_event: RuntimeEvent) -> None:
            msg = "boom"
            raise RuntimeError(msg)

        bus.subscribe(ComponentStartedEvent, bad_handler, priority=10)
        bus.subscribe(ComponentStartedEvent, good_handler, priority=1)

        bus.publish(ComponentStartedEvent(source="test", component_name="Y"))
        time.sleep(0.15)

        assert len(received) == 1
        dead = bus.get_dead_letters()
        assert len(dead) >= 1


# ===========================================================================
# Lifecycle integration
# ===========================================================================


class TestLifecycleIntegration:
    def test_full_lifecycle(self) -> None:
        eb = EventBus()
        eb.initialize()

        handler_called = threading.Event()

        def handler(_event: RuntimeEvent) -> None:
            handler_called.set()

        eb.subscribe(ComponentStartedEvent, handler)
        eb.start()
        eb.publish(ComponentStartedEvent(source="test", component_name="A"))
        assert handler_called.wait(timeout=1.0)
        eb.stop()
        assert not eb.is_running()

    def test_restart_cycle(self) -> None:
        eb = EventBus()
        received: list[RuntimeEvent] = []

        def handler(event: RuntimeEvent) -> None:
            received.append(event)

        eb.subscribe(ComponentStartedEvent, handler)

        for _ in range(EXPECTED_RESTART_CYCLES):
            eb.initialize()
            eb.start()
            eb.publish(
                ComponentStartedEvent(source="test", component_name="Z")
            )
            time.sleep(0.1)
            eb.stop()

        assert len(received) == EXPECTED_RESTART_CYCLES

    def test_stop_drains_queue(self) -> None:
        eb = EventBus()
        eb.initialize()

        received: list[RuntimeEvent] = []

        def handler(event: RuntimeEvent) -> None:
            received.append(event)

        eb.subscribe(ComponentStartedEvent, handler)
        eb.start()

        for i in range(EXPECTED_DRAIN_COUNT):
            eb.publish(
                ComponentStartedEvent(
                    source="test", component_name=f"comp_{i}"
                )
            )

        eb.stop()
        assert len(received) == EXPECTED_DRAIN_COUNT


# ===========================================================================
# Deterministic ordering tests
# ===========================================================================


class TestDeterministicOrdering:
    def test_fifo_within_same_priority(self, bus: EventBus) -> None:
        order: list[int] = []
        lock = threading.Lock()

        def handler(event: RuntimeEvent) -> None:
            if isinstance(event, ComponentStartedEvent):
                with lock:
                    order.append(int(event.component_name))

        bus.subscribe(ComponentStartedEvent, handler)

        for i in range(EXPECTED_FIFO_COUNT):
            bus.publish(
                ComponentStartedEvent(source="test", component_name=str(i))
            )

        time.sleep(0.3)
        assert order == list(range(EXPECTED_FIFO_COUNT))

    def test_priority_across_handlers(self, bus: EventBus) -> None:
        order: list[str] = []
        lock = threading.Lock()

        def make_handler(name: str) -> EventHandler:
            def h(_event: RuntimeEvent) -> None:
                with lock:
                    order.append(name)
            return h

        bus.subscribe(ComponentStartedEvent, make_handler("low"), priority=1)
        bus.subscribe(ComponentStartedEvent, make_handler("mid"), priority=5)
        bus.subscribe(ComponentStartedEvent, make_handler("high"), priority=10)

        bus.publish(ComponentStartedEvent(source="test", component_name="x"))
        time.sleep(0.1)

        assert order == ["high", "mid", "low"]


# ===========================================================================
# Thread safety under load
# ===========================================================================


class TestThreadSafetyUnderLoad:
    def test_high_throughput(self, bus: EventBus) -> None:
        counter = {"value": 0}
        lock = threading.Lock()

        def handler(_event: RuntimeEvent) -> None:
            with lock:
                counter["value"] += 1

        bus.subscribe(ComponentStartedEvent, handler)
        errors: list[Exception] = []

        def publish_batch(count: int) -> None:
            try:
                for _ in range(count):
                    bus.publish(
                        ComponentStartedEvent(
                            source="test", component_name="perf"
                        )
                    )
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=publish_batch, args=(100,))
            for _ in range(4)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        time.sleep(1.0)

        assert not errors
        assert counter["value"] == EXPECTED_THROUGHPUT_COUNT
