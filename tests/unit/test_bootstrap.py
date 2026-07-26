"""Unit tests for the BootstrapSequence."""

from __future__ import annotations

import pytest

from jochen_x.core.exceptions.bootstrap import BootstrapStepError
from jochen_x.core.observability.audit import AuditLog
from jochen_x.core.observability.logging import StructuredLogger
from jochen_x.core.runtime.bootstrap import (
    BOOTSTRAP_STEP_NAMES,
    SHUTDOWN_STEP_NAMES,
    BootstrapSequence,
    BootstrapStep,
)
from jochen_x.core.runtime.host import _NullEventBus
from jochen_x.core.types.health_status import HealthStatus

EXPECTED_STEP_COUNT = 9


@pytest.fixture
def logger() -> StructuredLogger:
    lg = StructuredLogger()
    lg.initialize()
    lg.start()
    yield lg  # type: ignore[misc]
    lg.stop()


@pytest.fixture
def bs(logger: StructuredLogger) -> BootstrapSequence:
    return BootstrapSequence(
        event_bus=_NullEventBus(),
        audit_log=AuditLog(),
        logger=logger,
        correlation_id="test-corr-id",
    )


class TestBootstrapStepNames:
    def test_step_count(self) -> None:
        assert len(BOOTSTRAP_STEP_NAMES) == EXPECTED_STEP_COUNT

    def test_shutdown_is_reverse(self) -> None:
        assert list(reversed(BOOTSTRAP_STEP_NAMES)) == SHUTDOWN_STEP_NAMES

    def test_first_step_is_environment(self) -> None:
        assert BOOTSTRAP_STEP_NAMES[0] == "Environment"

    def test_last_step_is_health_check(self) -> None:
        assert BOOTSTRAP_STEP_NAMES[-1] == "HealthCheck"


class TestBootstrapStep:
    def test_frozen_dataclass(self) -> None:
        step = BootstrapStep(name="test", execute=lambda: None)
        assert step.name == "test"
        with pytest.raises(AttributeError):
            step.name = "changed"  # type: ignore[misc]


class TestBootstrapSequenceExecute:
    def test_execute_all_steps(self, bs: BootstrapSequence) -> None:
        executed: list[str] = []

        for name in BOOTSTRAP_STEP_NAMES:
            bs.register_bootstrap_step(name, lambda n=name: executed.append(n))

        bs.execute_bootstrap()

        assert executed == BOOTSTRAP_STEP_NAMES
        assert bs.completed_bootstrap_steps == BOOTSTRAP_STEP_NAMES

    def test_fail_fast_on_error(self, bs: BootstrapSequence) -> None:
        executed: list[str] = []

        bs.register_bootstrap_step("ok", lambda: executed.append("ok"))
        bs.register_bootstrap_step(
            "fail", lambda: (_ for _ in ()).throw(RuntimeError("boom")),
        )
        bs.register_bootstrap_step("after", lambda: executed.append("after"))

        with pytest.raises(BootstrapStepError) as exc_info:
            bs.execute_bootstrap()

        assert exc_info.value.step_name == "fail"
        assert exc_info.value.step_index == 1
        assert "after" not in executed

    def test_empty_bootstrap(self, bs: BootstrapSequence) -> None:
        bs.execute_bootstrap()
        assert bs.completed_bootstrap_steps == []


class TestShutdownSequenceExecute:
    def test_best_effort_continues_on_error(
        self, bs: BootstrapSequence,
    ) -> None:
        executed: list[str] = []

        bs.register_shutdown_step("first", lambda: executed.append("first"))

        def fail_step() -> None:
            msg = "shutdown error"
            raise RuntimeError(msg)

        bs.register_shutdown_step("fail", fail_step)
        bs.register_shutdown_step("last", lambda: executed.append("last"))

        errors = bs.execute_shutdown()

        assert len(errors) == 1
        assert "first" in executed
        assert "last" in executed

    def test_no_errors_on_clean_shutdown(
        self, bs: BootstrapSequence,
    ) -> None:
        bs.register_shutdown_step("a", lambda: None)
        bs.register_shutdown_step("b", lambda: None)
        errors = bs.execute_shutdown()
        assert errors == []
        assert bs.completed_shutdown_steps == ["a", "b"]


class TestBootstrapSequenceReset:
    def test_reset_clears_steps(self, bs: BootstrapSequence) -> None:
        bs.register_bootstrap_step("test", lambda: None)
        bs.register_shutdown_step("test", lambda: None)
        bs.reset()
        bs.execute_bootstrap()
        assert bs.completed_bootstrap_steps == []


class TestBootstrapSequenceCorrelation:
    def test_set_correlation_id(self, bs: BootstrapSequence) -> None:
        bs.set_correlation_id("new-id")
        assert bs._correlation_id == "new-id"


class TestBootstrapSequenceHealth:
    def test_health_unknown_when_no_steps(
        self, bs: BootstrapSequence,
    ) -> None:
        assert bs.check_health() == HealthStatus.UNKNOWN

    def test_health_healthy_when_all_complete(
        self, bs: BootstrapSequence,
    ) -> None:
        bs.register_bootstrap_step("a", lambda: None)
        bs.register_bootstrap_step("b", lambda: None)
        bs.execute_bootstrap()
        assert bs.check_health() == HealthStatus.HEALTHY

    def test_component_name(self, bs: BootstrapSequence) -> None:
        assert bs.get_component_name() == "BootstrapSequence"
