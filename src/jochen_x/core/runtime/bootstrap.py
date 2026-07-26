"""Bootstrap and shutdown sequences for the Core Runtime.

The ``BootstrapSequence`` orchestrates the ordered startup and
shutdown of all runtime components.  The bootstrap follows the
exact 9-step sequence from the specification.  The shutdown follows
the exact reverse order.

Bootstrap is fail-fast: any step failure triggers a transition
to FAILED and initiates recovery.  Shutdown is best-effort: errors
during individual steps are logged but do not prevent subsequent
steps from executing.

All operations are thread-safe.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable
from dataclasses import dataclass
from threading import RLock

from jochen_x.core.exceptions.bootstrap import BootstrapStepError
from jochen_x.core.interfaces.audit import IAuditLog
from jochen_x.core.interfaces.event_bus import IEventBus
from jochen_x.core.interfaces.logging import ILogger
from jochen_x.core.types.events import (
    BootstrapStepCompletedEvent,
    ShutdownStepCompletedEvent,
)
from jochen_x.core.types.health_status import HealthStatus
from jochen_x.core.types.severity import LogSeverity

__all__ = ["BootstrapSequence"]

_COMPONENT_NAME = "BootstrapSequence"

BOOTSTRAP_STEP_NAMES: list[str] = [
    "Environment",
    "Configuration",
    "Logging",
    "DependencyInjection",
    "ServiceRegistry",
    "EventBus",
    "RuntimeServices",
    "PluginFramework",
    "HealthCheck",
]

SHUTDOWN_STEP_NAMES: list[str] = list(reversed(BOOTSTRAP_STEP_NAMES))


@dataclass(frozen=True, kw_only=True, slots=True)
class BootstrapStep:
    """A single step in the bootstrap or shutdown sequence.

    Args:
        name: Human-readable name of the step.
        execute: Callable that performs the step.

    """

    name: str
    execute: Callable[[], None]


class BootstrapSequence:
    """Orchestrates the bootstrap and shutdown sequences.

    Maintains an ordered list of bootstrap steps and executes them
    sequentially.  Each completed step emits a
    ``BootstrapStepCompletedEvent`` or ``ShutdownStepCompletedEvent``.

    The bootstrap is fail-fast: if any step fails, a
    ``BootstrapStepError`` is raised immediately.

    The shutdown is best-effort: all steps are attempted regardless
    of individual failures, and errors are logged.

    Args:
        event_bus: Event bus for step-completion events.
        audit_log: Audit log for recording step completions.
        logger: Structured logger for step logging.
        correlation_id: Correlation ID for cross-component tracing.

    """

    def __init__(
        self,
        *,
        event_bus: IEventBus,
        audit_log: IAuditLog,
        logger: ILogger,
        correlation_id: str = "",
    ) -> None:
        """Initialise the bootstrap sequence."""
        self._event_bus: IEventBus = event_bus
        self._audit_log: IAuditLog = audit_log
        self._logger: ILogger = logger
        self._correlation_id: str = correlation_id
        self._lock: RLock = RLock()
        self._bootstrap_steps: list[BootstrapStep] = []
        self._shutdown_steps: list[BootstrapStep] = []
        self._completed_bootstrap_steps: list[str] = []
        self._completed_shutdown_steps: list[str] = []

    @property
    def completed_bootstrap_steps(self) -> list[str]:
        """Return the names of completed bootstrap steps.

        Returns:
            A list of step names in completion order.

        """
        with self._lock:
            return list(self._completed_bootstrap_steps)

    @property
    def completed_shutdown_steps(self) -> list[str]:
        """Return the names of completed shutdown steps.

        Returns:
            A list of step names in completion order.

        """
        with self._lock:
            return list(self._completed_shutdown_steps)

    def register_bootstrap_step(
        self,
        name: str,
        execute: Callable[[], None],
    ) -> None:
        """Register a bootstrap step.

        Steps are executed in registration order during bootstrap.

        Args:
            name: Unique name for the step.
            execute: Callable that performs the step.

        """
        with self._lock:
            self._bootstrap_steps.append(
                BootstrapStep(name=name, execute=execute),
            )

    def register_shutdown_step(
        self,
        name: str,
        execute: Callable[[], None],
    ) -> None:
        """Register a shutdown step.

        Steps are executed in registration order during shutdown.

        Args:
            name: Unique name for the step.
            execute: Callable that performs the step.

        """
        with self._lock:
            self._shutdown_steps.append(
                BootstrapStep(name=name, execute=execute),
            )

    def execute_bootstrap(self) -> None:
        """Execute all registered bootstrap steps in order.

        Each step is executed sequentially.  On success, a
        ``BootstrapStepCompletedEvent`` is emitted and recorded in
        the audit log.  On failure, a ``BootstrapStepError`` is
        raised immediately (fail-fast).

        Raises:
            BootstrapStepError: If any bootstrap step fails.

        """
        with self._lock:
            steps = list(self._bootstrap_steps)
            self._completed_bootstrap_steps.clear()

        for index, step in enumerate(steps):
            step_msg = "Bootstrap step " + str(index) + ": " + step.name
            self._logger.log(
                LogSeverity.INFO,
                step_msg,
                component=_COMPONENT_NAME,
                correlation_id=self._correlation_id,
            )

            try:
                step.execute()
            except Exception as exc:
                fail_msg = (
                    "Bootstrap step '" + step.name
                    + "' (index " + str(index)
                    + ") failed: " + str(exc)
                )
                self._logger.log(
                    LogSeverity.CRITICAL,
                    fail_msg,
                    component=_COMPONENT_NAME,
                    correlation_id=self._correlation_id,
                )
                raise BootstrapStepError(
                    step.name,
                    index,
                    str(exc),
                    correlation_id=self._correlation_id,
                    component=_COMPONENT_NAME,
                ) from exc

            event = BootstrapStepCompletedEvent(
                step_name=step.name,
                step_index=index,
                source=_COMPONENT_NAME,
                correlation_id=self._correlation_id,
            )

            self._audit_log.record(event)
            self._publish_event(event)

            with self._lock:
                self._completed_bootstrap_steps.append(step.name)

            done_msg = "Bootstrap step " + str(index) + " completed: " + step.name
            self._logger.log(
                LogSeverity.INFO,
                done_msg,
                component=_COMPONENT_NAME,
                correlation_id=self._correlation_id,
            )

    def execute_shutdown(self) -> list[Exception]:
        """Execute all registered shutdown steps in order.

        Shutdown is best-effort: all steps are attempted regardless
        of individual failures.  On success, a
        ``ShutdownStepCompletedEvent`` is emitted and recorded.

        Returns:
            A list of exceptions from failed steps (empty on success).

        """
        with self._lock:
            steps = list(self._shutdown_steps)
            self._completed_shutdown_steps.clear()

        errors: list[Exception] = []

        for index, step in enumerate(steps):
            step_msg = "Shutdown step " + str(index) + ": " + step.name
            self._logger.log(
                LogSeverity.INFO,
                step_msg,
                component=_COMPONENT_NAME,
                correlation_id=self._correlation_id,
            )

            try:
                step.execute()
            except Exception as exc:  # noqa: BLE001
                fail_msg = (
                    "Shutdown step '" + step.name
                    + "' (index " + str(index)
                    + ") failed: " + str(exc)
                )
                self._logger.log(
                    LogSeverity.ERROR,
                    fail_msg,
                    component=_COMPONENT_NAME,
                    correlation_id=self._correlation_id,
                )
                errors.append(exc)
                continue

            event = ShutdownStepCompletedEvent(
                step_name=step.name,
                step_index=index,
                source=_COMPONENT_NAME,
                correlation_id=self._correlation_id,
            )

            with contextlib.suppress(Exception):
                self._audit_log.record(event)
            self._publish_event(event)

            with self._lock:
                self._completed_shutdown_steps.append(step.name)

            done_msg = "Shutdown step " + str(index) + " completed: " + step.name
            self._logger.log(
                LogSeverity.INFO,
                done_msg,
                component=_COMPONENT_NAME,
                correlation_id=self._correlation_id,
            )

        return errors

    def reset(self) -> None:
        """Reset all registered steps and completion tracking."""
        with self._lock:
            self._bootstrap_steps.clear()
            self._shutdown_steps.clear()
            self._completed_bootstrap_steps.clear()
            self._completed_shutdown_steps.clear()

    def set_correlation_id(self, correlation_id: str) -> None:
        """Update the correlation ID for subsequent steps.

        Args:
            correlation_id: The new correlation ID.

        """
        self._correlation_id = correlation_id

    def set_event_bus(self, event_bus: IEventBus) -> None:
        """Replace the event bus used for step-completion events.

        Called by the RuntimeHost after the real EventBus is
        bootstrapped to replace the initial null implementation.

        Args:
            event_bus: The new event bus instance.

        """
        self._event_bus = event_bus

    def check_health(self) -> HealthStatus:
        """Return the health status of the bootstrap sequence.

        Returns:
            ``HEALTHY`` if all bootstrap steps completed,
            ``UNKNOWN`` otherwise.

        """
        with self._lock:
            expected = len(self._bootstrap_steps)
            completed = len(self._completed_bootstrap_steps)
        if expected > 0 and completed == expected:
            return HealthStatus.HEALTHY
        return HealthStatus.UNKNOWN

    def get_component_name(self) -> str:
        """Return the component name.

        Returns:
            The string ``"BootstrapSequence"``.

        """
        return _COMPONENT_NAME

    def _publish_event(
        self,
        event: BootstrapStepCompletedEvent | ShutdownStepCompletedEvent,
    ) -> None:
        """Publish an event, suppressing bus errors during shutdown."""
        with contextlib.suppress(Exception):
            self._event_bus.publish(event)
