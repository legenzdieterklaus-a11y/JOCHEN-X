"""Unit tests for the StateMachine."""

from __future__ import annotations

import threading

import pytest

from jochen_x.core.exceptions.lifecycle import IllegalStateTransitionError
from jochen_x.core.observability.audit import AuditLog
from jochen_x.core.observability.logging import StructuredLogger
from jochen_x.core.runtime.host import _NullEventBus
from jochen_x.core.runtime.state_machine import StateMachine
from jochen_x.core.types.health_status import HealthStatus
from jochen_x.core.types.runtime_state import RuntimeState

THREAD_COUNT = 50


@pytest.fixture
def sm() -> StateMachine:
    logger = StructuredLogger()
    logger.initialize()
    logger.start()
    machine = StateMachine(
        event_bus=_NullEventBus(),
        audit_log=AuditLog(),
        logger=logger,
    )
    yield machine  # type: ignore[misc]
    logger.stop()


class TestStateMachineInit:
    def test_initial_state_is_created(self, sm: StateMachine) -> None:
        assert sm.state == RuntimeState.CREATED

    def test_correlation_id_is_set(self, sm: StateMachine) -> None:
        assert sm.correlation_id != ""

    def test_component_name(self, sm: StateMachine) -> None:
        assert sm.get_component_name() == "StateMachine"


class TestStateMachineTransitions:
    def test_valid_transition_created_to_bootstrapping(
        self, sm: StateMachine,
    ) -> None:
        sm.transition(RuntimeState.BOOTSTRAPPING)
        assert sm.state == RuntimeState.BOOTSTRAPPING

    def test_full_lifecycle_happy_path(self, sm: StateMachine) -> None:
        sm.transition(RuntimeState.BOOTSTRAPPING)
        sm.transition(RuntimeState.INITIALIZING)
        sm.transition(RuntimeState.READY)
        sm.transition(RuntimeState.STARTING)
        sm.transition(RuntimeState.RUNNING)
        sm.transition(RuntimeState.PAUSED)
        sm.transition(RuntimeState.RUNNING)
        sm.transition(RuntimeState.STOPPING)
        sm.transition(RuntimeState.STOPPED)
        sm.transition(RuntimeState.SHUTDOWN)
        assert sm.state == RuntimeState.SHUTDOWN

    def test_stopped_to_starting_restart(self, sm: StateMachine) -> None:
        sm.transition(RuntimeState.BOOTSTRAPPING)
        sm.transition(RuntimeState.INITIALIZING)
        sm.transition(RuntimeState.READY)
        sm.transition(RuntimeState.STARTING)
        sm.transition(RuntimeState.RUNNING)
        sm.transition(RuntimeState.STOPPING)
        sm.transition(RuntimeState.STOPPED)
        sm.transition(RuntimeState.STARTING)
        assert sm.state == RuntimeState.STARTING

    def test_invalid_transition_raises(self, sm: StateMachine) -> None:
        with pytest.raises(IllegalStateTransitionError):
            sm.transition(RuntimeState.RUNNING)

    def test_invalid_skip_state_raises(self, sm: StateMachine) -> None:
        sm.transition(RuntimeState.BOOTSTRAPPING)
        with pytest.raises(IllegalStateTransitionError):
            sm.transition(RuntimeState.READY)

    def test_cannot_leave_shutdown(self, sm: StateMachine) -> None:
        sm.transition(RuntimeState.BOOTSTRAPPING)
        sm.transition(RuntimeState.INITIALIZING)
        sm.transition(RuntimeState.READY)
        sm.transition(RuntimeState.STARTING)
        sm.transition(RuntimeState.RUNNING)
        sm.transition(RuntimeState.STOPPING)
        sm.transition(RuntimeState.STOPPED)
        sm.transition(RuntimeState.SHUTDOWN)
        with pytest.raises(IllegalStateTransitionError):
            sm.transition(RuntimeState.CREATED)

    def test_paused_to_stopping(self, sm: StateMachine) -> None:
        sm.transition(RuntimeState.BOOTSTRAPPING)
        sm.transition(RuntimeState.INITIALIZING)
        sm.transition(RuntimeState.READY)
        sm.transition(RuntimeState.STARTING)
        sm.transition(RuntimeState.RUNNING)
        sm.transition(RuntimeState.PAUSED)
        sm.transition(RuntimeState.STOPPING)
        assert sm.state == RuntimeState.STOPPING


class TestStateMachineFail:
    def test_fail_from_created(self, sm: StateMachine) -> None:
        sm.fail()
        assert sm.state == RuntimeState.FAILED

    def test_fail_from_running(self, sm: StateMachine) -> None:
        sm.transition(RuntimeState.BOOTSTRAPPING)
        sm.transition(RuntimeState.INITIALIZING)
        sm.transition(RuntimeState.READY)
        sm.transition(RuntimeState.STARTING)
        sm.transition(RuntimeState.RUNNING)
        sm.fail()
        assert sm.state == RuntimeState.FAILED

    def test_fail_from_shutdown_raises(self, sm: StateMachine) -> None:
        sm.transition(RuntimeState.BOOTSTRAPPING)
        sm.transition(RuntimeState.INITIALIZING)
        sm.transition(RuntimeState.READY)
        sm.transition(RuntimeState.STARTING)
        sm.transition(RuntimeState.RUNNING)
        sm.transition(RuntimeState.STOPPING)
        sm.transition(RuntimeState.STOPPED)
        sm.transition(RuntimeState.SHUTDOWN)
        with pytest.raises(IllegalStateTransitionError):
            sm.fail()

    def test_recover_from_failed_to_bootstrapping(
        self, sm: StateMachine,
    ) -> None:
        sm.fail()
        sm.transition(RuntimeState.BOOTSTRAPPING)
        assert sm.state == RuntimeState.BOOTSTRAPPING

    def test_recover_from_failed_to_starting(
        self, sm: StateMachine,
    ) -> None:
        sm.fail()
        sm.transition(RuntimeState.STARTING)
        assert sm.state == RuntimeState.STARTING


class TestStateMachineHealth:
    def test_health_unknown_in_created(self, sm: StateMachine) -> None:
        assert sm.check_health() == HealthStatus.UNKNOWN

    def test_health_healthy_in_running(self, sm: StateMachine) -> None:
        sm.transition(RuntimeState.BOOTSTRAPPING)
        sm.transition(RuntimeState.INITIALIZING)
        sm.transition(RuntimeState.READY)
        sm.transition(RuntimeState.STARTING)
        sm.transition(RuntimeState.RUNNING)
        assert sm.check_health() == HealthStatus.HEALTHY

    def test_health_degraded_in_paused(self, sm: StateMachine) -> None:
        sm.transition(RuntimeState.BOOTSTRAPPING)
        sm.transition(RuntimeState.INITIALIZING)
        sm.transition(RuntimeState.READY)
        sm.transition(RuntimeState.STARTING)
        sm.transition(RuntimeState.RUNNING)
        sm.transition(RuntimeState.PAUSED)
        assert sm.check_health() == HealthStatus.DEGRADED

    def test_health_degraded_in_ready(self, sm: StateMachine) -> None:
        sm.transition(RuntimeState.BOOTSTRAPPING)
        sm.transition(RuntimeState.INITIALIZING)
        sm.transition(RuntimeState.READY)
        assert sm.check_health() == HealthStatus.DEGRADED

    def test_health_unhealthy_in_failed(self, sm: StateMachine) -> None:
        sm.fail()
        assert sm.check_health() == HealthStatus.UNHEALTHY


class TestStateMachineCorrelation:
    def test_reset_correlation_id(self, sm: StateMachine) -> None:
        old_id = sm.correlation_id
        new_id = sm.reset_correlation_id()
        assert new_id != old_id
        assert sm.correlation_id == new_id


class TestStateMachineThreadSafety:
    def test_concurrent_transitions_no_crash(
        self, sm: StateMachine,
    ) -> None:
        sm.transition(RuntimeState.BOOTSTRAPPING)
        sm.transition(RuntimeState.INITIALIZING)
        sm.transition(RuntimeState.READY)
        sm.transition(RuntimeState.STARTING)
        sm.transition(RuntimeState.RUNNING)

        errors: list[Exception] = []
        barrier = threading.Barrier(THREAD_COUNT)

        def toggle(idx: int) -> None:
            barrier.wait()
            try:
                if idx % 2 == 0:
                    sm.transition(RuntimeState.PAUSED)
                else:
                    sm.transition(RuntimeState.STOPPING)
            except IllegalStateTransitionError:
                pass
            except Exception as exc:
                errors.append(exc)

        threads = [
            threading.Thread(target=toggle, args=(i,))
            for i in range(THREAD_COUNT)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=5)

        assert not errors
        assert sm.state in (
            RuntimeState.RUNNING,
            RuntimeState.PAUSED,
            RuntimeState.STOPPING,
        )
