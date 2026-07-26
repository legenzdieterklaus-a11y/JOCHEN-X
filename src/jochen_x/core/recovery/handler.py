"""Recovery handler with multi-level escalation and circuit breaker.

The ``RecoveryHandler`` is the central entry point for all error
recovery in the Core Runtime.  It coordinates recovery strategies,
tracks per-component state, enforces cooldowns and circuit-breaker
semantics, and integrates with EventBus, AuditLog, and Logging.
"""

from __future__ import annotations

import contextlib
import threading
from datetime import UTC, datetime

from jochen_x.core.exceptions.base import JochenXError
from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.interfaces.audit import IAuditLog
from jochen_x.core.interfaces.event_bus import IEventBus
from jochen_x.core.interfaces.health import IHealthCheck
from jochen_x.core.interfaces.lifecycle import ILifecycle
from jochen_x.core.interfaces.logging import ILogger
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
)
from jochen_x.core.types.health_status import HealthStatus
from jochen_x.core.types.recovery_level import RecoveryLevel
from jochen_x.core.types.severity import LogSeverity

__all__ = ["RecoveryHandler"]

_COMPONENT_NAME: str = "RecoveryHandler"

_FIELD_COMPONENT: str = "component"
_REASON_EMPTY: str = "must not be empty"

_MSG_ALREADY_INIT: str = "RecoveryHandler is already initialized"
_MSG_NOT_INIT: str = (
    "RecoveryHandler must be initialized before starting"
)
_MSG_ALREADY_STARTED: str = "RecoveryHandler is already started"
_MSG_NOT_STARTED: str = "RecoveryHandler is not started"
_MSG_CANNOT_ESCALATE: str = (
    "Cannot escalate beyond RUNTIME_RESTART for '{}'"
)


class RecoveryHandler(ILifecycle, IHealthCheck):
    """Multi-level recovery handler with circuit-breaker semantics.

    Implements ``IRecoveryHandler``, ``ILifecycle``, and
    ``IHealthCheck``.

    The handler maintains per-component recovery state and enforces:

    - Configurable max retries per level before escalation.
    - Cooldown periods between recovery attempts at the same level.
    - Circuit-breaker semantics to prevent recovery thrashing.
    - Automatic escalation from lower to higher recovery levels.
    - Full audit trail of all recovery actions.

    Args:
        event_bus: Event bus for publishing recovery events.
        audit_log: Audit log for recording recovery actions.
        logger: Structured logger for logging.
        level_configs: Optional per-level configuration overrides.
        strategies: Optional mapping of recovery levels to custom
            strategies.  Missing levels receive default strategies.

    """

    def __init__(
        self,
        *,
        event_bus: IEventBus,
        audit_log: IAuditLog,
        logger: ILogger,
        level_configs: (
            dict[RecoveryLevel, RecoveryLevelConfig] | None
        ) = None,
        strategies: (
            dict[RecoveryLevel, IRecoveryStrategy] | None
        ) = None,
    ) -> None:
        """Initialise with injected dependencies."""
        self._event_bus: IEventBus = event_bus
        self._audit_log: IAuditLog = audit_log
        self._logger: ILogger = logger
        self._registry: RecoveryLevelRegistry = RecoveryLevelRegistry(
            level_configs,
        )
        self._strategies: dict[RecoveryLevel, IRecoveryStrategy] = (
            strategies if strategies is not None else {}
        )
        self._ensure_default_strategies()
        self._lock: threading.RLock = threading.RLock()
        self._initialized: bool = False
        self._started: bool = False
        self._recovery_in_progress: dict[str, bool] = {}

    def _ensure_default_strategies(self) -> None:
        """Populate missing strategy slots with defaults."""
        defaults: list[IRecoveryStrategy] = [
            ComponentRetryStrategy(),
            ComponentRestartStrategy(),
            ServiceRestartStrategy(),
            RuntimeRestartStrategy(),
        ]
        for strategy in defaults:
            if strategy.level not in self._strategies:
                self._strategies[strategy.level] = strategy

    # -- ILifecycle ---------------------------------------------------------

    def initialize(self) -> None:
        """Initialize the recovery handler.

        Raises:
            JochenXError: If already initialized.

        """
        with self._lock:
            if self._initialized:
                raise JochenXError(
                    _MSG_ALREADY_INIT,
                    component=_COMPONENT_NAME,
                )
            self._initialized = True
            self._logger.log(
                LogSeverity.INFO,
                "RecoveryHandler initialized",
                component=_COMPONENT_NAME,
            )

    def start(self) -> None:
        """Start the recovery handler.

        Raises:
            JochenXError: If not initialized or already started.

        """
        with self._lock:
            if not self._initialized:
                raise JochenXError(
                    _MSG_NOT_INIT,
                    component=_COMPONENT_NAME,
                )
            if self._started:
                raise JochenXError(
                    _MSG_ALREADY_STARTED,
                    component=_COMPONENT_NAME,
                )
            self._started = True
            self._logger.log(
                LogSeverity.INFO,
                "RecoveryHandler started",
                component=_COMPONENT_NAME,
            )

    def stop(self) -> None:
        """Stop the recovery handler.

        Clears all recovery state.  Safe to call multiple times.
        """
        with self._lock:
            self._started = False
            self._initialized = False
            self._registry.reset_all()
            self._recovery_in_progress.clear()
            self._logger.log(
                LogSeverity.INFO,
                "RecoveryHandler stopped",
                component=_COMPONENT_NAME,
            )

    # -- IHealthCheck -------------------------------------------------------

    def check_health(self) -> HealthStatus:
        """Return the health status of the recovery handler.

        Returns:
            ``HEALTHY`` if started, ``DEGRADED`` if initialized but
            not started, ``UNHEALTHY`` otherwise.

        """
        with self._lock:
            if self._started:
                return HealthStatus.HEALTHY
            if self._initialized:
                return HealthStatus.DEGRADED
            return HealthStatus.UNHEALTHY

    def get_component_name(self) -> str:
        """Return the component name.

        Returns:
            The fixed name ``"RecoveryHandler"``.

        """
        return _COMPONENT_NAME

    # -- IRecoveryHandler ---------------------------------------------------

    def handle_error(
        self,
        error: Exception,
        *,
        component: str = "",
        level: RecoveryLevel = RecoveryLevel.COMPONENT_RETRY,
    ) -> bool:
        """Handle an error at the specified recovery level.

        This method is thread-safe and re-entrant-safe: if recovery
        is already in progress for the same component, it returns
        ``False`` immediately to prevent infinite recursion.

        Args:
            error: The exception that triggered recovery.
            component: Name of the affected component.
            level: Recovery level to attempt.

        Returns:
            ``True`` if recovery succeeded, ``False`` if escalation
            is required or recovery failed.

        Raises:
            InputValidationError: If component name is empty.
            JochenXError: If the handler is not started.

        """
        if not component:
            raise InputValidationError(
                _FIELD_COMPONENT,
                _REASON_EMPTY,
                component=_COMPONENT_NAME,
            )

        with self._lock:
            if not self._started:
                raise JochenXError(
                    _MSG_NOT_STARTED,
                    component=_COMPONENT_NAME,
                )

            if self._recovery_in_progress.get(component, False):
                msg = (
                    f"Recovery already in progress for '{component}', "
                    "skipping to prevent re-entrant loop"
                )
                self._logger.log(
                    LogSeverity.WARNING,
                    msg,
                    component=_COMPONENT_NAME,
                )
                return False

            self._recovery_in_progress[component] = True

        try:
            return self._do_handle_error(error, component, level)
        finally:
            with self._lock:
                self._recovery_in_progress[component] = False

    def _do_handle_error(
        self,
        error: Exception,
        component: str,
        level: RecoveryLevel,
    ) -> bool:
        """Execute recovery with automatic escalation.

        Args:
            error: The exception that triggered recovery.
            component: Name of the affected component.
            level: Starting recovery level.

        Returns:
            ``True`` if any level succeeded, ``False`` if all
            levels are exhausted.

        """
        current_level = level
        now = datetime.now(UTC)

        while True:
            with self._lock:
                cooldown = self._registry.is_cooldown_active(
                    component, current_level, now=now,
                )
                circuit = self._registry.is_circuit_open(
                    component, current_level, now=now,
                )
                has_retries = self._registry.has_retries_remaining(
                    component, current_level,
                )

            if cooldown:
                msg = (
                    f"Cooldown active for '{component}' at level {current_level.name}, "
                    "escalating"
                )
                self._logger.log(
                    LogSeverity.WARNING,
                    msg,
                    component=_COMPONENT_NAME,
                )
                escalated = self._try_escalate(
                    component, current_level,
                )
                if escalated is None:
                    return False
                current_level = escalated
                now = datetime.now(UTC)
                continue

            if circuit:
                msg = (
                    f"Circuit breaker open for '{component}' at level "
                    f"{current_level.name}, escalating"
                )
                self._logger.log(
                    LogSeverity.ERROR,
                    msg,
                    component=_COMPONENT_NAME,
                )
                escalated = self._try_escalate(
                    component, current_level,
                )
                if escalated is None:
                    return False
                current_level = escalated
                now = datetime.now(UTC)
                continue

            if not has_retries:
                msg = (
                    f"No retries remaining for '{component}' at level "
                    f"{current_level.name}, escalating"
                )
                self._logger.log(
                    LogSeverity.WARNING,
                    msg,
                    component=_COMPONENT_NAME,
                )
                escalated = self._try_escalate(
                    component, current_level,
                )
                if escalated is None:
                    return False
                current_level = escalated
                now = datetime.now(UTC)
                continue

            success = self._execute_recovery(
                error, component, current_level, now=now,
            )
            if success:
                return True

            escalated = self._try_escalate(
                component, current_level,
            )
            if escalated is None:
                return False
            current_level = escalated
            now = datetime.now(UTC)

    def _execute_recovery(
        self,
        error: Exception,
        component: str,
        level: RecoveryLevel,
        *,
        now: datetime,
    ) -> bool:
        """Execute a single recovery attempt and record it.

        Args:
            error: The exception that triggered recovery.
            component: Name of the affected component.
            level: Recovery level to attempt.
            now: Current timestamp.

        Returns:
            ``True`` if the strategy executed successfully.

        """
        initiated_event = RecoveryInitiatedEvent(
            component_name=component,
            level=level,
            reason=str(error),
            source=_COMPONENT_NAME,
        )
        with contextlib.suppress(Exception):
            self._event_bus.publish(initiated_event)
        with contextlib.suppress(Exception):
            self._audit_log.record(initiated_event)

        with self._lock:
            self._registry.record_attempt(
                component, level, now=now,
            )

        strategy = self._strategies[level]
        success = strategy.execute(
            error, component, logger=self._logger,
        )

        completed_event = RecoveryCompletedEvent(
            component_name=component,
            level=level,
            success=success,
            source=_COMPONENT_NAME,
        )
        with contextlib.suppress(Exception):
            self._event_bus.publish(completed_event)
        with contextlib.suppress(Exception):
            self._audit_log.record(completed_event)

        if not success:
            with self._lock:
                self._registry.record_failure(
                    component, level, now=now,
                )
            msg = f"Recovery failed for '{component}' at level {level.name}"
            self._logger.log(
                LogSeverity.ERROR,
                msg,
                component=_COMPONENT_NAME,
            )

        return success

    def _try_escalate(
        self,
        component: str,
        from_level: RecoveryLevel,
    ) -> RecoveryLevel | None:
        """Attempt to escalate to the next recovery level.

        Args:
            component: Name of the affected component.
            from_level: The current level that failed.

        Returns:
            The next recovery level, or ``None`` if at the highest.

        """
        if from_level == RecoveryLevel.RUNTIME_RESTART:
            msg = (
                "Cannot escalate beyond RUNTIME_RESTART for "
                f"'{component}'. All recovery options exhausted."
            )
            self._logger.log(
                LogSeverity.CRITICAL,
                msg,
                component=_COMPONENT_NAME,
            )
            completed_event = RecoveryCompletedEvent(
                component_name=component,
                level=from_level,
                success=False,
                source=_COMPONENT_NAME,
            )
            with contextlib.suppress(Exception):
                self._event_bus.publish(completed_event)
            with contextlib.suppress(Exception):
                self._audit_log.record(completed_event)
            return None

        to_level = self.escalate(component, from_level)

        escalated_event = RecoveryEscalatedEvent(
            component_name=component,
            from_level=from_level,
            to_level=to_level,
            source=_COMPONENT_NAME,
        )
        with contextlib.suppress(Exception):
            self._event_bus.publish(escalated_event)
        with contextlib.suppress(Exception):
            self._audit_log.record(escalated_event)

        msg = (
            f"Escalated recovery for '{component}' "
            f"from {from_level.name} to {to_level.name}"
        )
        self._logger.log(
            LogSeverity.WARNING,
            msg,
            component=_COMPONENT_NAME,
        )
        return to_level

    def escalate(
        self,
        component: str,
        from_level: RecoveryLevel,
    ) -> RecoveryLevel:
        """Escalate to the next recovery level.

        Args:
            component: Name of the affected component.
            from_level: The current recovery level that failed.

        Returns:
            The next higher recovery level.

        Raises:
            InputValidationError: If component name is empty.
            JochenXError: If already at the highest level.

        """
        if not component:
            raise InputValidationError(
                _FIELD_COMPONENT,
                _REASON_EMPTY,
                component=_COMPONENT_NAME,
            )
        if from_level == RecoveryLevel.RUNTIME_RESTART:
            raise JochenXError(
                _MSG_CANNOT_ESCALATE.format(component),
                component=_COMPONENT_NAME,
            )

        levels = list(RecoveryLevel)
        current_index = levels.index(from_level)
        return levels[current_index + 1]

    def reset(self, component: str) -> None:
        """Reset recovery state for a component.

        Args:
            component: Name of the recovered component.

        Raises:
            InputValidationError: If component name is empty.

        """
        if not component:
            raise InputValidationError(
                _FIELD_COMPONENT,
                _REASON_EMPTY,
                component=_COMPONENT_NAME,
            )
        with self._lock:
            self._registry.reset_component(component)
            self._recovery_in_progress.pop(component, None)
        msg = f"Recovery state reset for '{component}'"
        self._logger.log(
            LogSeverity.INFO,
            msg,
            component=_COMPONENT_NAME,
        )

    # -- Introspection ------------------------------------------------------

    def get_attempt_count(
        self, component: str, level: RecoveryLevel,
    ) -> int:
        """Return recovery attempts for a component at a level.

        Args:
            component: Name of the component.
            level: The recovery level.

        Returns:
            Number of recorded attempts.

        """
        with self._lock:
            return self._registry.get_attempt_count(
                component, level,
            )

    def is_recovery_in_progress(self, component: str) -> bool:
        """Check whether recovery is in progress for a component.

        Args:
            component: Name of the component.

        Returns:
            ``True`` if recovery is currently running.

        """
        with self._lock:
            return self._recovery_in_progress.get(component, False)

    def get_level_config(
        self, level: RecoveryLevel,
    ) -> RecoveryLevelConfig:
        """Return the configuration for a recovery level.

        Args:
            level: The recovery level.

        Returns:
            The configuration for the requested level.

        """
        return self._registry.get_config(level)
