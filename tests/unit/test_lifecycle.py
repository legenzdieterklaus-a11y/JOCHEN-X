"""Unit tests for the LifecycleManager."""

from __future__ import annotations

import pytest

from jochen_x.core.exceptions.lifecycle import IllegalStateTransitionError
from jochen_x.core.observability.audit import AuditLog
from jochen_x.core.observability.logging import StructuredLogger
from jochen_x.core.runtime.host import _NullEventBus
from jochen_x.core.runtime.lifecycle import LifecycleManager
from jochen_x.core.types.health_status import HealthStatus
from jochen_x.core.types.runtime_state import RuntimeState


@pytest.fixture
def lm() -> LifecycleManager:
    logger = StructuredLogger()
    logger.initialize()
    logger.start()
    mgr = LifecycleManager(
        event_bus=_NullEventBus(),
        audit_log=AuditLog(),
        logger=logger,
    )
    yield mgr  # type: ignore[misc]
    logger.stop()


class TestLifecycleManagerInit:
    def test_initial_state_is_created(self, lm: LifecycleManager) -> None:
        assert lm.state == RuntimeState.CREATED

    def test_component_name(self, lm: LifecycleManager) -> None:
        assert lm.get_component_name() == "LifecycleManager"

    def test_correlation_id_set(self, lm: LifecycleManager) -> None:
        assert lm.correlation_id != ""

    def test_state_machine_accessible(self, lm: LifecycleManager) -> None:
        assert lm.state_machine is not None


class TestLifecycleBootstrap:
    def test_begin_bootstrap(self, lm: LifecycleManager) -> None:
        lm.begin_bootstrap()
        assert lm.state == RuntimeState.BOOTSTRAPPING

    def test_complete_bootstrap(self, lm: LifecycleManager) -> None:
        lm.begin_bootstrap()
        lm.complete_bootstrap()
        assert lm.state == RuntimeState.INITIALIZING

    def test_complete_initialization(self, lm: LifecycleManager) -> None:
        lm.begin_bootstrap()
        lm.complete_bootstrap()
        lm.complete_initialization()
        assert lm.state == RuntimeState.READY


class TestLifecycleStart:
    def test_begin_and_complete_start(self, lm: LifecycleManager) -> None:
        lm.begin_bootstrap()
        lm.complete_bootstrap()
        lm.complete_initialization()
        lm.begin_start()
        assert lm.state == RuntimeState.STARTING
        lm.complete_start()
        assert lm.state == RuntimeState.RUNNING


class TestLifecyclePauseResume:
    def test_pause_and_resume(self, lm: LifecycleManager) -> None:
        lm.begin_bootstrap()
        lm.complete_bootstrap()
        lm.complete_initialization()
        lm.begin_start()
        lm.complete_start()
        lm.pause()
        assert lm.state == RuntimeState.PAUSED
        lm.resume()
        assert lm.state == RuntimeState.RUNNING

    def test_pause_from_wrong_state_raises(
        self, lm: LifecycleManager,
    ) -> None:
        with pytest.raises(IllegalStateTransitionError):
            lm.pause()


class TestLifecycleStop:
    def test_begin_and_complete_stop(self, lm: LifecycleManager) -> None:
        lm.begin_bootstrap()
        lm.complete_bootstrap()
        lm.complete_initialization()
        lm.begin_start()
        lm.complete_start()
        lm.begin_stop()
        assert lm.state == RuntimeState.STOPPING
        lm.complete_stop()
        assert lm.state == RuntimeState.STOPPED

    def test_shutdown(self, lm: LifecycleManager) -> None:
        lm.begin_bootstrap()
        lm.complete_bootstrap()
        lm.complete_initialization()
        lm.begin_start()
        lm.complete_start()
        lm.begin_stop()
        lm.complete_stop()
        lm.shutdown()
        assert lm.state == RuntimeState.SHUTDOWN


class TestLifecycleFail:
    def test_fail_transitions_to_failed(self, lm: LifecycleManager) -> None:
        lm.fail()
        assert lm.state == RuntimeState.FAILED


class TestLifecycleRecovery:
    def test_recover_bootstrap(self, lm: LifecycleManager) -> None:
        lm.fail()
        old_corr = lm.correlation_id
        lm.recover_bootstrap()
        assert lm.state == RuntimeState.BOOTSTRAPPING
        assert lm.correlation_id != old_corr

    def test_recover_start(self, lm: LifecycleManager) -> None:
        lm.fail()
        old_corr = lm.correlation_id
        lm.recover_start()
        assert lm.state == RuntimeState.STARTING
        assert lm.correlation_id != old_corr


class TestLifecycleHealth:
    def test_health_delegates_to_state_machine(
        self, lm: LifecycleManager,
    ) -> None:
        assert lm.check_health() == HealthStatus.UNKNOWN
        lm.begin_bootstrap()
        lm.complete_bootstrap()
        lm.complete_initialization()
        lm.begin_start()
        lm.complete_start()
        assert lm.check_health() == HealthStatus.HEALTHY
