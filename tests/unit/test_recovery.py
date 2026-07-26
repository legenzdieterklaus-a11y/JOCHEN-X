"""Unit tests for the recovery subsystem."""

from __future__ import annotations

import threading
from collections.abc import Sequence
from datetime import UTC, datetime, timedelta

import pytest

from jochen_x.core.exceptions.base import JochenXError
from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.interfaces.logging import ILogger
from jochen_x.core.recovery.handler import RecoveryHandler
from jochen_x.core.recovery.levels import (
    RecoveryLevelConfig,
    RecoveryLevelRegistry,
)
from jochen_x.core.recovery.strategy import (
    ComponentRestartStrategy,
    ComponentRetryStrategy,
    IRecoveryStrategy,
    RuntimeRestartStrategy,
    ServiceRestartStrategy,
)
from jochen_x.core.types.events import (
    RecoveryCompletedEvent,
    RecoveryEscalatedEvent,
    RecoveryInitiatedEvent,
    RuntimeEvent,
)
from jochen_x.core.types.health_status import HealthStatus
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
        self.log(LogSeverity.DEBUG, message, component=component)

    def info(
        self, message: str, *,
        component: str = "", correlation_id: str = "",
    ) -> None:
        self.log(LogSeverity.INFO, message, component=component)

    def warning(
        self, message: str, *,
        component: str = "", correlation_id: str = "",
    ) -> None:
        self.log(LogSeverity.WARNING, message, component=component)

    def error(
        self, message: str, *,
        component: str = "", correlation_id: str = "",
    ) -> None:
        self.log(LogSeverity.ERROR, message, component=component)

    def critical(
        self, message: str, *,
        component: str = "", correlation_id: str = "",
    ) -> None:
        self.log(LogSeverity.CRITICAL, message, component=component)


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


class _FailingStrategy:
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


# ---------------------------------------------------------------------------
# RecoveryLevelConfig tests
# ---------------------------------------------------------------------------


class TestRecoveryLevelConfig:
    """Tests for RecoveryLevelConfig dataclass."""

    def test_valid_config(self) -> None:
        config = RecoveryLevelConfig(
            level=RecoveryLevel.COMPONENT_RETRY,
            max_retries=3,
            cooldown_seconds=1.0,
        )
        assert config.level == RecoveryLevel.COMPONENT_RETRY
        assert config.max_retries == 3
        assert config.cooldown_seconds == 1.0

    def test_invalid_max_retries_zero(self) -> None:
        with pytest.raises(InputValidationError):
            RecoveryLevelConfig(
                level=RecoveryLevel.COMPONENT_RETRY,
                max_retries=0,
                cooldown_seconds=1.0,
            )

    def test_invalid_max_retries_negative(self) -> None:
        with pytest.raises(InputValidationError):
            RecoveryLevelConfig(
                level=RecoveryLevel.COMPONENT_RETRY,
                max_retries=-1,
                cooldown_seconds=1.0,
            )

    def test_invalid_cooldown_negative(self) -> None:
        with pytest.raises(InputValidationError):
            RecoveryLevelConfig(
                level=RecoveryLevel.COMPONENT_RETRY,
                max_retries=1,
                cooldown_seconds=-1.0,
            )

    def test_cooldown_zero_is_valid(self) -> None:
        config = RecoveryLevelConfig(
            level=RecoveryLevel.COMPONENT_RETRY,
            max_retries=1,
            cooldown_seconds=0.0,
        )
        assert config.cooldown_seconds == 0.0

    def test_invalid_circuit_breaker_threshold(self) -> None:
        with pytest.raises(InputValidationError):
            RecoveryLevelConfig(
                level=RecoveryLevel.COMPONENT_RETRY,
                max_retries=1,
                cooldown_seconds=1.0,
                circuit_breaker_threshold=0,
            )

    def test_invalid_circuit_breaker_window(self) -> None:
        with pytest.raises(InputValidationError):
            RecoveryLevelConfig(
                level=RecoveryLevel.COMPONENT_RETRY,
                max_retries=1,
                cooldown_seconds=1.0,
                circuit_breaker_window_seconds=0.0,
            )

    def test_frozen(self) -> None:
        config = RecoveryLevelConfig(
            level=RecoveryLevel.COMPONENT_RETRY,
            max_retries=3,
            cooldown_seconds=1.0,
        )
        with pytest.raises(AttributeError):
            config.max_retries = 5  # type: ignore[misc]


# ---------------------------------------------------------------------------
# RecoveryLevelRegistry tests
# ---------------------------------------------------------------------------


class TestRecoveryLevelRegistry:
    """Tests for RecoveryLevelRegistry."""

    def test_default_configs(self) -> None:
        registry = RecoveryLevelRegistry()
        for level in RecoveryLevel:
            config = registry.get_config(level)
            assert config.level == level
            assert config.max_retries >= 1

    def test_custom_config(self) -> None:
        custom = {
            RecoveryLevel.COMPONENT_RETRY: RecoveryLevelConfig(
                level=RecoveryLevel.COMPONENT_RETRY,
                max_retries=10,
                cooldown_seconds=0.5,
            ),
        }
        registry = RecoveryLevelRegistry(configs=custom)
        retry_cfg = registry.get_config(
            RecoveryLevel.COMPONENT_RETRY,
        )
        assert retry_cfg.max_retries == 10
        restart_cfg = registry.get_config(
            RecoveryLevel.COMPONENT_RESTART,
        )
        assert restart_cfg.max_retries > 0

    def test_record_attempt_and_count(self) -> None:
        registry = RecoveryLevelRegistry()
        level = RecoveryLevel.COMPONENT_RETRY
        assert registry.get_attempt_count("comp", level) == 0
        registry.record_attempt("comp", level)
        assert registry.get_attempt_count("comp", level) == 1

    def test_has_retries_remaining(self) -> None:
        config = {
            RecoveryLevel.COMPONENT_RETRY: RecoveryLevelConfig(
                level=RecoveryLevel.COMPONENT_RETRY,
                max_retries=2,
                cooldown_seconds=0.0,
            ),
        }
        registry = RecoveryLevelRegistry(configs=config)
        level = RecoveryLevel.COMPONENT_RETRY
        assert registry.has_retries_remaining("c", level)
        registry.record_attempt("c", level)
        assert registry.has_retries_remaining("c", level)
        registry.record_attempt("c", level)
        assert not registry.has_retries_remaining("c", level)

    def test_cooldown(self) -> None:
        config = {
            RecoveryLevel.COMPONENT_RETRY: RecoveryLevelConfig(
                level=RecoveryLevel.COMPONENT_RETRY,
                max_retries=5,
                cooldown_seconds=10.0,
            ),
        }
        registry = RecoveryLevelRegistry(configs=config)
        now = datetime.now(UTC)
        level = RecoveryLevel.COMPONENT_RETRY
        registry.record_attempt("c", level, now=now)
        assert registry.is_cooldown_active("c", level, now=now)
        future = now + timedelta(seconds=11)
        assert not registry.is_cooldown_active(
            "c", level, now=future,
        )

    def test_cooldown_not_active_without_attempt(self) -> None:
        registry = RecoveryLevelRegistry()
        level = RecoveryLevel.COMPONENT_RETRY
        assert not registry.is_cooldown_active("c", level)

    def test_circuit_breaker(self) -> None:
        config = {
            RecoveryLevel.COMPONENT_RETRY: RecoveryLevelConfig(
                level=RecoveryLevel.COMPONENT_RETRY,
                max_retries=10,
                cooldown_seconds=0.0,
                circuit_breaker_threshold=3,
                circuit_breaker_window_seconds=60.0,
            ),
        }
        registry = RecoveryLevelRegistry(configs=config)
        now = datetime.now(UTC)
        level = RecoveryLevel.COMPONENT_RETRY
        assert not registry.is_circuit_open("c", level, now=now)
        for i in range(3):
            ts = now + timedelta(seconds=i)
            registry.record_failure("c", level, now=ts)
        check_ts = now + timedelta(seconds=3)
        assert registry.is_circuit_open("c", level, now=check_ts)

    def test_circuit_breaker_window_expiry(self) -> None:
        config = {
            RecoveryLevel.COMPONENT_RETRY: RecoveryLevelConfig(
                level=RecoveryLevel.COMPONENT_RETRY,
                max_retries=10,
                cooldown_seconds=0.0,
                circuit_breaker_threshold=3,
                circuit_breaker_window_seconds=10.0,
            ),
        }
        registry = RecoveryLevelRegistry(configs=config)
        now = datetime.now(UTC)
        level = RecoveryLevel.COMPONENT_RETRY
        for _i in range(3):
            registry.record_failure("c", level, now=now)
        assert registry.is_circuit_open("c", level, now=now)
        future = now + timedelta(seconds=11)
        assert not registry.is_circuit_open(
            "c", level, now=future,
        )

    def test_reset_component(self) -> None:
        registry = RecoveryLevelRegistry()
        level = RecoveryLevel.COMPONENT_RETRY
        registry.record_attempt("c", level)
        registry.record_failure("c", level)
        registry.reset_component("c")
        assert registry.get_attempt_count("c", level) == 0
        assert not registry.is_circuit_open("c", level)

    def test_reset_all(self) -> None:
        registry = RecoveryLevelRegistry()
        registry.record_attempt(
            "a", RecoveryLevel.COMPONENT_RETRY,
        )
        registry.record_attempt(
            "b", RecoveryLevel.COMPONENT_RESTART,
        )
        registry.reset_all()
        count_a = registry.get_attempt_count(
            "a", RecoveryLevel.COMPONENT_RETRY,
        )
        count_b = registry.get_attempt_count(
            "b", RecoveryLevel.COMPONENT_RESTART,
        )
        assert count_a == 0
        assert count_b == 0

    def test_thread_safety(self) -> None:
        registry = RecoveryLevelRegistry()
        errors: list[Exception] = []
        level = RecoveryLevel.COMPONENT_RETRY

        def worker() -> None:
            try:
                for _ in range(100):
                    registry.record_attempt("c", level)
                    registry.has_retries_remaining("c", level)
                    registry.is_cooldown_active("c", level)
            except Exception as exc:
                errors.append(exc)

        threads = [
            threading.Thread(target=worker) for _ in range(4)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert not errors


# ---------------------------------------------------------------------------
# Strategy tests
# ---------------------------------------------------------------------------


class TestStrategies:
    """Tests for recovery strategy implementations."""

    def test_component_retry_strategy(self) -> None:
        strategy = ComponentRetryStrategy()
        assert strategy.level == RecoveryLevel.COMPONENT_RETRY
        logger = _FakeLogger()
        result = strategy.execute(
            RuntimeError("test"), "comp", logger=logger,
        )
        assert result is True
        assert len(logger.messages) == 1

    def test_component_restart_strategy(self) -> None:
        strategy = ComponentRestartStrategy()
        assert strategy.level == RecoveryLevel.COMPONENT_RESTART
        logger = _FakeLogger()
        result = strategy.execute(
            RuntimeError("test"), "comp", logger=logger,
        )
        assert result is True

    def test_service_restart_strategy(self) -> None:
        strategy = ServiceRestartStrategy()
        assert strategy.level == RecoveryLevel.SERVICE_RESTART
        logger = _FakeLogger()
        result = strategy.execute(
            RuntimeError("test"), "comp", logger=logger,
        )
        assert result is True

    def test_runtime_restart_strategy(self) -> None:
        strategy = RuntimeRestartStrategy()
        assert strategy.level == RecoveryLevel.RUNTIME_RESTART
        logger = _FakeLogger()
        result = strategy.execute(
            RuntimeError("test"), "comp", logger=logger,
        )
        assert result is True

    def test_protocol_compliance(self) -> None:
        strategies: list[IRecoveryStrategy] = [
            ComponentRetryStrategy(),
            ComponentRestartStrategy(),
            ServiceRestartStrategy(),
            RuntimeRestartStrategy(),
        ]
        for s in strategies:
            assert isinstance(s, IRecoveryStrategy)


# ---------------------------------------------------------------------------
# RecoveryHandler tests
# ---------------------------------------------------------------------------


def _make_handler(
    *,
    strategies: (
        dict[RecoveryLevel, IRecoveryStrategy] | None
    ) = None,
    level_configs: (
        dict[RecoveryLevel, RecoveryLevelConfig] | None
    ) = None,
) -> tuple[
    RecoveryHandler, _FakeEventBus, _FakeAuditLog, _FakeLogger
]:
    """Create a handler with fake dependencies."""
    event_bus = _FakeEventBus()
    audit_log = _FakeAuditLog()
    logger = _FakeLogger()
    handler = RecoveryHandler(
        event_bus=event_bus,
        audit_log=audit_log,
        logger=logger,
        level_configs=level_configs,
        strategies=strategies,
    )
    return handler, event_bus, audit_log, logger


class TestRecoveryHandlerLifecycle:
    """Tests for RecoveryHandler lifecycle."""

    def test_initialize(self) -> None:
        handler, *_ = _make_handler()
        handler.initialize()
        assert handler.check_health() == HealthStatus.DEGRADED

    def test_double_initialize_raises(self) -> None:
        handler, *_ = _make_handler()
        handler.initialize()
        with pytest.raises(JochenXError):
            handler.initialize()

    def test_start_without_initialize_raises(self) -> None:
        handler, *_ = _make_handler()
        with pytest.raises(JochenXError):
            handler.start()

    def test_start(self) -> None:
        handler, *_ = _make_handler()
        handler.initialize()
        handler.start()
        assert handler.check_health() == HealthStatus.HEALTHY

    def test_double_start_raises(self) -> None:
        handler, *_ = _make_handler()
        handler.initialize()
        handler.start()
        with pytest.raises(JochenXError):
            handler.start()

    def test_stop(self) -> None:
        handler, *_ = _make_handler()
        handler.initialize()
        handler.start()
        handler.stop()
        assert handler.check_health() == HealthStatus.UNHEALTHY

    def test_stop_idempotent(self) -> None:
        handler, *_ = _make_handler()
        handler.stop()
        handler.stop()
        assert handler.check_health() == HealthStatus.UNHEALTHY

    def test_component_name(self) -> None:
        handler, *_ = _make_handler()
        assert handler.get_component_name() == "RecoveryHandler"


class TestRecoveryHandlerErrors:
    """Tests for handle_error method."""

    def test_handle_error_empty_component_raises(self) -> None:
        handler, *_ = _make_handler()
        handler.initialize()
        handler.start()
        with pytest.raises(InputValidationError):
            handler.handle_error(RuntimeError("x"), component="")

    def test_handle_error_not_started_raises(self) -> None:
        handler, *_ = _make_handler()
        with pytest.raises(JochenXError):
            handler.handle_error(
                RuntimeError("x"), component="comp",
            )

    def test_successful_recovery(self) -> None:
        handler, event_bus, audit_log, _ = _make_handler()
        handler.initialize()
        handler.start()
        result = handler.handle_error(
            RuntimeError("test"),
            component="comp",
            level=RecoveryLevel.COMPONENT_RETRY,
        )
        assert result is True
        initiated = [
            e for e in event_bus.published
            if isinstance(e, RecoveryInitiatedEvent)
        ]
        completed = [
            e for e in event_bus.published
            if isinstance(e, RecoveryCompletedEvent)
        ]
        assert len(initiated) == 1
        assert len(completed) == 1
        assert completed[0].success is True
        assert len(audit_log.recorded) >= 2

    def test_escalation_on_failure(self) -> None:
        retry_level = RecoveryLevel.COMPONENT_RETRY
        failing_strategies: dict[
            RecoveryLevel, IRecoveryStrategy
        ] = {retry_level: _FailingStrategy(retry_level)}
        configs = {
            retry_level: RecoveryLevelConfig(
                level=retry_level,
                max_retries=1,
                cooldown_seconds=0.0,
            ),
        }
        handler, event_bus, _, _ = _make_handler(
            strategies=failing_strategies,
            level_configs=configs,
        )
        handler.initialize()
        handler.start()
        result = handler.handle_error(
            RuntimeError("fail"),
            component="comp",
            level=retry_level,
        )
        assert result is True
        escalated = [
            e for e in event_bus.published
            if isinstance(e, RecoveryEscalatedEvent)
        ]
        assert len(escalated) >= 1

    def test_all_levels_fail(self) -> None:
        all_failing: dict[
            RecoveryLevel, IRecoveryStrategy
        ] = {
            level: _FailingStrategy(level)
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
            strategies=all_failing,
            level_configs=configs,
        )
        handler.initialize()
        handler.start()
        result = handler.handle_error(
            RuntimeError("fail"),
            component="comp",
            level=RecoveryLevel.COMPONENT_RETRY,
        )
        assert result is False

    def test_reset_clears_state(self) -> None:
        handler, *_ = _make_handler()
        handler.initialize()
        handler.start()
        handler.handle_error(
            RuntimeError("test"), component="comp",
        )
        handler.reset("comp")
        count = handler.get_attempt_count(
            "comp", RecoveryLevel.COMPONENT_RETRY,
        )
        assert count == 0

    def test_reset_empty_component_raises(self) -> None:
        handler, *_ = _make_handler()
        with pytest.raises(InputValidationError):
            handler.reset("")


class TestRecoveryHandlerEscalation:
    """Tests for the escalate method."""

    def test_escalate_retry_to_restart(self) -> None:
        handler, *_ = _make_handler()
        level = handler.escalate(
            "comp", RecoveryLevel.COMPONENT_RETRY,
        )
        assert level == RecoveryLevel.COMPONENT_RESTART

    def test_escalate_restart_to_service(self) -> None:
        handler, *_ = _make_handler()
        level = handler.escalate(
            "comp", RecoveryLevel.COMPONENT_RESTART,
        )
        assert level == RecoveryLevel.SERVICE_RESTART

    def test_escalate_service_to_runtime(self) -> None:
        handler, *_ = _make_handler()
        level = handler.escalate(
            "comp", RecoveryLevel.SERVICE_RESTART,
        )
        assert level == RecoveryLevel.RUNTIME_RESTART

    def test_escalate_beyond_runtime_raises(self) -> None:
        handler, *_ = _make_handler()
        with pytest.raises(JochenXError):
            handler.escalate(
                "comp", RecoveryLevel.RUNTIME_RESTART,
            )

    def test_escalate_empty_component_raises(self) -> None:
        handler, *_ = _make_handler()
        with pytest.raises(InputValidationError):
            handler.escalate(
                "", RecoveryLevel.COMPONENT_RETRY,
            )


class TestRecoveryHandlerCircuitBreaker:
    """Tests for circuit-breaker integration."""

    def test_circuit_breaker_triggers_escalation(self) -> None:
        retry_level = RecoveryLevel.COMPONENT_RETRY
        failing_strategies: dict[
            RecoveryLevel, IRecoveryStrategy
        ] = {retry_level: _FailingStrategy(retry_level)}
        configs = {
            retry_level: RecoveryLevelConfig(
                level=retry_level,
                max_retries=10,
                cooldown_seconds=0.0,
                circuit_breaker_threshold=2,
                circuit_breaker_window_seconds=60.0,
            ),
        }
        handler, event_bus, _, _ = _make_handler(
            strategies=failing_strategies,
            level_configs=configs,
        )
        handler.initialize()
        handler.start()

        handler.handle_error(
            RuntimeError("1"), component="comp",
        )
        handler.reset("comp")

        handler.handle_error(
            RuntimeError("2"), component="comp",
        )

        escalated = [
            e for e in event_bus.published
            if isinstance(e, RecoveryEscalatedEvent)
        ]
        assert len(escalated) >= 1


class TestRecoveryHandlerReentrancy:
    """Tests for re-entrancy protection."""

    def test_reentrant_call_returns_false(self) -> None:
        handler, *_ = _make_handler()
        handler.initialize()
        handler.start()

        with handler._lock:
            handler._recovery_in_progress["comp"] = True

        result = handler.handle_error(
            RuntimeError("x"), component="comp",
        )
        assert result is False

        with handler._lock:
            handler._recovery_in_progress["comp"] = False


class TestRecoveryHandlerThreadSafety:
    """Tests for thread safety."""

    def test_concurrent_handle_error(self) -> None:
        handler, *_ = _make_handler()
        handler.initialize()
        handler.start()
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
                target=worker, args=(f"comp-{i}",),
            )
            for i in range(8)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert len(results) == 8
        assert all(results)

    def test_concurrent_reset(self) -> None:
        handler, *_ = _make_handler()
        handler.initialize()
        handler.start()
        errors: list[Exception] = []

        def worker(comp: str) -> None:
            try:
                handler.handle_error(
                    RuntimeError("err"), component=comp,
                )
                handler.reset(comp)
            except Exception as exc:
                errors.append(exc)

        threads = [
            threading.Thread(
                target=worker, args=(f"comp-{i}",),
            )
            for i in range(8)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors


class TestRecoveryHandlerIntrospection:
    """Tests for introspection methods."""

    def test_get_attempt_count(self) -> None:
        handler, *_ = _make_handler()
        handler.initialize()
        handler.start()
        level = RecoveryLevel.COMPONENT_RETRY
        assert handler.get_attempt_count("comp", level) == 0
        handler.handle_error(
            RuntimeError("x"), component="comp",
        )
        assert handler.get_attempt_count("comp", level) == 1

    def test_is_recovery_in_progress(self) -> None:
        handler, *_ = _make_handler()
        assert handler.is_recovery_in_progress("comp") is False

    def test_get_level_config(self) -> None:
        handler, *_ = _make_handler()
        config = handler.get_level_config(
            RecoveryLevel.COMPONENT_RETRY,
        )
        assert config.level == RecoveryLevel.COMPONENT_RETRY
        assert config.max_retries >= 1
