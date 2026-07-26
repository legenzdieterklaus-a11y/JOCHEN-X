"""Recovery scenario tests covering escalation flows and edge cases."""

from __future__ import annotations

import threading
from collections.abc import Sequence

from jochen_x.core.interfaces.logging import ILogger
from jochen_x.core.recovery.handler import RecoveryHandler
from jochen_x.core.recovery.levels import RecoveryLevelConfig
from jochen_x.core.recovery.strategy import IRecoveryStrategy
from jochen_x.core.types.events import (
    RecoveryCompletedEvent,
    RecoveryEscalatedEvent,
    RecoveryInitiatedEvent,
    RuntimeEvent,
)
from jochen_x.core.types.recovery_level import RecoveryLevel
from jochen_x.core.types.severity import LogSeverity

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _FakeLogger:
    """Minimal ILogger for tests."""

    def __init__(self) -> None:
        self.messages: list[tuple[LogSeverity, str]] = []

    def log(
        self,
        severity: LogSeverity,
        message: str,
        *,
        component: str = "",
        correlation_id: str = "",
    ) -> None:
        self.messages.append((severity, message))

    def debug(
        self, message: str, *,
        component: str = "", correlation_id: str = "",
    ) -> None:
        self.log(LogSeverity.DEBUG, message)

    def info(
        self, message: str, *,
        component: str = "", correlation_id: str = "",
    ) -> None:
        self.log(LogSeverity.INFO, message)

    def warning(
        self, message: str, *,
        component: str = "", correlation_id: str = "",
    ) -> None:
        self.log(LogSeverity.WARNING, message)

    def error(
        self, message: str, *,
        component: str = "", correlation_id: str = "",
    ) -> None:
        self.log(LogSeverity.ERROR, message)

    def critical(
        self, message: str, *,
        component: str = "", correlation_id: str = "",
    ) -> None:
        self.log(LogSeverity.CRITICAL, message)


class _FakeEventBus:
    """Minimal IEventBus for tests."""

    def __init__(self) -> None:
        self.published: list[RuntimeEvent] = []

    def publish(self, event: RuntimeEvent) -> None:
        self.published.append(event)

    def subscribe(
        self,
        event_type: type[RuntimeEvent],
        handler: object,
        *,
        priority: int = 0,
    ) -> None:
        pass

    def unsubscribe(
        self,
        event_type: type[RuntimeEvent],
        handler: object,
    ) -> None:
        pass


class _FakeAuditLog:
    """Minimal IAuditLog for tests."""

    def __init__(self) -> None:
        self.recorded: list[RuntimeEvent] = []

    def record(self, event: RuntimeEvent) -> None:
        self.recorded.append(event)

    def get_entries(
        self, *, limit: int = 100, offset: int = 0,
    ) -> Sequence[RuntimeEvent]:
        return self.recorded[offset:offset + limit]

    def verify_integrity(self) -> bool:
        return True


class _CountingStrategy:
    """Strategy that fails N times then succeeds."""

    def __init__(
        self, level: RecoveryLevel, *, fail_count: int = 0,
    ) -> None:
        self._level = level
        self._fail_count = fail_count
        self._call_count = 0
        self._lock = threading.Lock()

    @property
    def level(self) -> RecoveryLevel:
        return self._level

    @property
    def call_count(self) -> int:
        with self._lock:
            return self._call_count

    def execute(
        self,
        error: Exception,
        component: str,
        *,
        logger: ILogger,
    ) -> bool:
        with self._lock:
            self._call_count += 1
            return self._call_count > self._fail_count


class _AlwaysFailStrategy:
    """Strategy that always fails."""

    def __init__(self, level: RecoveryLevel) -> None:
        self._level = level

    @property
    def level(self) -> RecoveryLevel:
        return self._level

    def execute(
        self,
        error: Exception,
        component: str,
        *,
        logger: ILogger,
    ) -> bool:
        return False


def _make_handler(
    *,
    strategies: (
        dict[RecoveryLevel, IRecoveryStrategy] | None
    ) = None,
    configs: (
        dict[RecoveryLevel, RecoveryLevelConfig] | None
    ) = None,
) -> tuple[
    RecoveryHandler, _FakeEventBus, _FakeAuditLog, _FakeLogger
]:
    event_bus = _FakeEventBus()
    audit_log = _FakeAuditLog()
    logger = _FakeLogger()
    handler = RecoveryHandler(
        event_bus=event_bus,
        audit_log=audit_log,
        logger=logger,
        level_configs=configs,
        strategies=strategies,
    )
    handler.initialize()
    handler.start()
    return handler, event_bus, audit_log, logger


# ---------------------------------------------------------------------------
# Scenario tests
# ---------------------------------------------------------------------------


class TestFullEscalationScenario:
    """Test full escalation from Level 1 to Level 4."""

    def test_escalation_through_all_levels(self) -> None:
        """Verify escalation proceeds L1 -> L2 -> L3 -> L4."""
        all_failing: dict[
            RecoveryLevel, IRecoveryStrategy
        ] = {
            level: _AlwaysFailStrategy(level)
            for level in RecoveryLevel
        }
        configs = {
            level: RecoveryLevelConfig(
                level=level,
                max_retries=1,
                cooldown_seconds=0.0,
            )
            for level in RecoveryLevel
        }
        handler, event_bus, audit_log, _ = _make_handler(
            strategies=all_failing,
            configs=configs,
        )
        result = handler.handle_error(
            RuntimeError("critical failure"),
            component="TestComponent",
            level=RecoveryLevel.COMPONENT_RETRY,
        )
        assert result is False

        escalated = [
            e for e in event_bus.published
            if isinstance(e, RecoveryEscalatedEvent)
        ]
        assert len(escalated) == 3
        assert escalated[0].from_level == (
            RecoveryLevel.COMPONENT_RETRY
        )
        assert escalated[0].to_level == (
            RecoveryLevel.COMPONENT_RESTART
        )
        assert escalated[1].from_level == (
            RecoveryLevel.COMPONENT_RESTART
        )
        assert escalated[1].to_level == (
            RecoveryLevel.SERVICE_RESTART
        )
        assert escalated[2].from_level == (
            RecoveryLevel.SERVICE_RESTART
        )
        assert escalated[2].to_level == (
            RecoveryLevel.RUNTIME_RESTART
        )

        initiated = [
            e for e in event_bus.published
            if isinstance(e, RecoveryInitiatedEvent)
        ]
        assert len(initiated) == 4

        for evt in initiated:
            assert any(
                a.event_id == evt.event_id
                for a in audit_log.recorded
            )

    def test_escalation_stops_at_successful_level(self) -> None:
        """Recovery stops escalating when a level succeeds."""
        retry_level = RecoveryLevel.COMPONENT_RETRY
        restart_level = RecoveryLevel.COMPONENT_RESTART
        retry_fail = _AlwaysFailStrategy(retry_level)
        restart_ok = _CountingStrategy(restart_level)
        configs = {
            retry_level: RecoveryLevelConfig(
                level=retry_level,
                max_retries=1,
                cooldown_seconds=0.0,
            ),
        }
        handler, event_bus, _, _ = _make_handler(
            strategies={
                retry_level: retry_fail,
                restart_level: restart_ok,
            },
            configs=configs,
        )
        result = handler.handle_error(
            RuntimeError("partial failure"),
            component="comp",
        )
        assert result is True
        assert restart_ok.call_count == 1

        escalated = [
            e for e in event_bus.published
            if isinstance(e, RecoveryEscalatedEvent)
        ]
        assert len(escalated) == 1
        assert escalated[0].to_level == restart_level


class TestRetryExhaustion:
    """Test that retries exhaust before escalation."""

    def test_retries_exhausted_before_escalation(self) -> None:
        level = RecoveryLevel.COMPONENT_RETRY
        counter = _CountingStrategy(level, fail_count=2)
        configs = {
            level: RecoveryLevelConfig(
                level=level,
                max_retries=3,
                cooldown_seconds=0.0,
            ),
        }
        handler, _, _, _ = _make_handler(
            strategies={level: counter},
            configs=configs,
        )
        result = handler.handle_error(
            RuntimeError("flaky"), component="comp",
        )
        assert result is True


class TestAuditIntegration:
    """Verify all recovery events are audit-logged."""

    def test_all_events_audited(self) -> None:
        handler, _, audit_log, _ = _make_handler()
        handler.handle_error(
            RuntimeError("test"), component="comp",
        )

        recovery_events = [
            e for e in audit_log.recorded
            if isinstance(
                e,
                (RecoveryInitiatedEvent, RecoveryCompletedEvent),
            )
        ]
        assert len(recovery_events) >= 2

    def test_escalation_audited(self) -> None:
        all_failing: dict[
            RecoveryLevel, IRecoveryStrategy
        ] = {
            level: _AlwaysFailStrategy(level)
            for level in RecoveryLevel
        }
        configs = {
            level: RecoveryLevelConfig(
                level=level,
                max_retries=1,
                cooldown_seconds=0.0,
            )
            for level in RecoveryLevel
        }
        handler, _, audit_log, _ = _make_handler(
            strategies=all_failing, configs=configs,
        )
        handler.handle_error(
            RuntimeError("fail"), component="comp",
        )

        escalation_events = [
            e for e in audit_log.recorded
            if isinstance(e, RecoveryEscalatedEvent)
        ]
        assert len(escalation_events) == 3


class TestResetAfterRecovery:
    """Verify state reset after successful recovery."""

    def test_reset_allows_fresh_retries(self) -> None:
        handler, _, _, _ = _make_handler()
        level = RecoveryLevel.COMPONENT_RETRY
        handler.handle_error(
            RuntimeError("first"), component="comp",
        )
        assert handler.get_attempt_count("comp", level) == 1
        handler.reset("comp")
        assert handler.get_attempt_count("comp", level) == 0
        handler.handle_error(
            RuntimeError("second"), component="comp",
        )
        assert handler.get_attempt_count("comp", level) == 1


class TestNoDataLoss:
    """Verify recovery does not cause data loss."""

    def test_event_bus_events_preserved(self) -> None:
        handler, event_bus, _, _ = _make_handler()
        initial_count = len(event_bus.published)
        handler.handle_error(
            RuntimeError("test"), component="comp",
        )
        assert len(event_bus.published) > initial_count

    def test_audit_entries_preserved(self) -> None:
        handler, _, audit_log, _ = _make_handler()
        initial_count = len(audit_log.recorded)
        handler.handle_error(
            RuntimeError("test"), component="comp",
        )
        assert len(audit_log.recorded) > initial_count


class TestDeterministicBehavior:
    """Verify recovery is deterministic."""

    def test_same_input_same_escalation_path(self) -> None:
        for _ in range(3):
            all_failing: dict[
                RecoveryLevel, IRecoveryStrategy
            ] = {
                level: _AlwaysFailStrategy(level)
                for level in RecoveryLevel
            }
            configs = {
                level: RecoveryLevelConfig(
                    level=level,
                    max_retries=1,
                    cooldown_seconds=0.0,
                )
                for level in RecoveryLevel
            }
            handler, event_bus, _, _ = _make_handler(
                strategies=all_failing, configs=configs,
            )
            result = handler.handle_error(
                RuntimeError("fail"), component="comp",
            )
            assert result is False
            escalated = [
                e for e in event_bus.published
                if isinstance(e, RecoveryEscalatedEvent)
            ]
            assert len(escalated) == 3


class TestNoEndlessLoop:
    """Verify recovery cannot enter an infinite loop."""

    def test_max_escalation_terminates(self) -> None:
        all_failing: dict[
            RecoveryLevel, IRecoveryStrategy
        ] = {
            level: _AlwaysFailStrategy(level)
            for level in RecoveryLevel
        }
        configs = {
            level: RecoveryLevelConfig(
                level=level,
                max_retries=1,
                cooldown_seconds=0.0,
            )
            for level in RecoveryLevel
        }
        handler, _, _, _ = _make_handler(
            strategies=all_failing, configs=configs,
        )
        result = handler.handle_error(
            RuntimeError("fail"), component="comp",
        )
        assert result is False

    def test_reentrant_protection(self) -> None:
        handler, _, _, _ = _make_handler()
        with handler._lock:
            handler._recovery_in_progress["comp"] = True
        result = handler.handle_error(
            RuntimeError("x"), component="comp",
        )
        assert result is False
        with handler._lock:
            handler._recovery_in_progress["comp"] = False


class TestMultiComponentIsolation:
    """Verify recovery state is isolated per component."""

    def test_independent_component_state(self) -> None:
        handler, _, _, _ = _make_handler()
        level = RecoveryLevel.COMPONENT_RETRY
        handler.handle_error(
            RuntimeError("a"), component="comp_a",
        )
        handler.handle_error(
            RuntimeError("b"), component="comp_b",
        )
        assert handler.get_attempt_count("comp_a", level) == 1
        assert handler.get_attempt_count("comp_b", level) == 1
        handler.reset("comp_a")
        assert handler.get_attempt_count("comp_a", level) == 0
        assert handler.get_attempt_count("comp_b", level) == 1


class TestConcurrentRecovery:
    """Verify thread safety under concurrent requests."""

    def test_concurrent_different_components(self) -> None:
        handler, _, _, _ = _make_handler()
        errors: list[Exception] = []
        results: list[bool] = []
        lock = threading.Lock()

        def worker(comp: str) -> None:
            try:
                r = handler.handle_error(
                    RuntimeError("err"), component=comp,
                )
                with lock:
                    results.append(r)
            except Exception as exc:
                with lock:
                    errors.append(exc)

        threads = [
            threading.Thread(
                target=worker,
                args=(f"comp-{i}",),
            )
            for i in range(16)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert len(results) == 16
        assert all(results)
