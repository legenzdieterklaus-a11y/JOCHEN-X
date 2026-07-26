"""Lifecycle manager coordinating state transitions for the Core Runtime.

The ``LifecycleManager`` provides high-level lifecycle operations
(start, stop, restart, pause, resume) that map to sequences of
state machine transitions.  It delegates the actual state tracking
to the ``StateMachine`` and coordinates observability integration.

All operations are thread-safe.
"""

from __future__ import annotations

from threading import RLock

from jochen_x.core.interfaces.audit import IAuditLog
from jochen_x.core.interfaces.event_bus import IEventBus
from jochen_x.core.interfaces.logging import ILogger
from jochen_x.core.runtime.state_machine import StateMachine
from jochen_x.core.types.health_status import HealthStatus
from jochen_x.core.types.runtime_state import RuntimeState
from jochen_x.core.types.severity import LogSeverity

__all__ = ["LifecycleManager"]

_COMPONENT_NAME = "LifecycleManager"


class LifecycleManager:
    """High-level lifecycle coordinator for the runtime.

    Wraps a ``StateMachine`` and provides semantic operations that
    correspond to the runtime's lifecycle phases.  Each operation
    validates the current state, executes the transition sequence,
    and integrates with logging and auditing.

    Args:
        event_bus: Event bus for state-change events.
        audit_log: Audit log for recording lifecycle transitions.
        logger: Structured logger for lifecycle logging.

    """

    def __init__(
        self,
        *,
        event_bus: IEventBus,
        audit_log: IAuditLog,
        logger: ILogger,
    ) -> None:
        """Initialise the lifecycle manager in CREATED state."""
        self._lock: RLock = RLock()
        self._logger: ILogger = logger
        self._state_machine: StateMachine = StateMachine(
            event_bus=event_bus,
            audit_log=audit_log,
            logger=logger,
        )

    @property
    def state(self) -> RuntimeState:
        """Return the current lifecycle state.

        Returns:
            The current ``RuntimeState``.

        """
        return self._state_machine.state

    @property
    def correlation_id(self) -> str:
        """Return the current correlation ID.

        Returns:
            The active correlation ID string.

        """
        return self._state_machine.correlation_id

    @property
    def state_machine(self) -> StateMachine:
        """Return the underlying state machine.

        Returns:
            The ``StateMachine`` instance.

        """
        return self._state_machine

    def begin_bootstrap(self) -> None:
        """Transition from CREATED to BOOTSTRAPPING.

        Raises:
            IllegalStateTransitionError: If not in CREATED state.

        """
        with self._lock:
            self._state_machine.transition(RuntimeState.BOOTSTRAPPING)
            self._logger.log(
                LogSeverity.INFO,
                "Bootstrap sequence started",
                component=_COMPONENT_NAME,
                correlation_id=self.correlation_id,
            )

    def complete_bootstrap(self) -> None:
        """Transition from BOOTSTRAPPING to INITIALIZING.

        Raises:
            IllegalStateTransitionError: If not in BOOTSTRAPPING state.

        """
        with self._lock:
            self._state_machine.transition(RuntimeState.INITIALIZING)

    def complete_initialization(self) -> None:
        """Transition from INITIALIZING to READY.

        Raises:
            IllegalStateTransitionError: If not in INITIALIZING state.

        """
        with self._lock:
            self._state_machine.transition(RuntimeState.READY)

    def begin_start(self) -> None:
        """Transition from READY or STOPPED to STARTING.

        Raises:
            IllegalStateTransitionError: If not in READY or STOPPED state.

        """
        with self._lock:
            self._state_machine.transition(RuntimeState.STARTING)

    def complete_start(self) -> None:
        """Transition from STARTING to RUNNING.

        Raises:
            IllegalStateTransitionError: If not in STARTING state.

        """
        with self._lock:
            self._state_machine.transition(RuntimeState.RUNNING)
            self._logger.log(
                LogSeverity.INFO,
                "Runtime is now RUNNING",
                component=_COMPONENT_NAME,
                correlation_id=self.correlation_id,
            )

    def pause(self) -> None:
        """Transition from RUNNING to PAUSED.

        Raises:
            IllegalStateTransitionError: If not in RUNNING state.

        """
        with self._lock:
            self._state_machine.transition(RuntimeState.PAUSED)
            self._logger.log(
                LogSeverity.INFO,
                "Runtime paused",
                component=_COMPONENT_NAME,
                correlation_id=self.correlation_id,
            )

    def resume(self) -> None:
        """Transition from PAUSED to RUNNING.

        Raises:
            IllegalStateTransitionError: If not in PAUSED state.

        """
        with self._lock:
            self._state_machine.transition(RuntimeState.RUNNING)
            self._logger.log(
                LogSeverity.INFO,
                "Runtime resumed",
                component=_COMPONENT_NAME,
                correlation_id=self.correlation_id,
            )

    def begin_stop(self) -> None:
        """Transition from RUNNING or PAUSED to STOPPING.

        Raises:
            IllegalStateTransitionError: If not in RUNNING or PAUSED state.

        """
        with self._lock:
            self._state_machine.transition(RuntimeState.STOPPING)
            self._logger.log(
                LogSeverity.INFO,
                "Shutdown sequence started",
                component=_COMPONENT_NAME,
                correlation_id=self.correlation_id,
            )

    def complete_stop(self) -> None:
        """Transition from STOPPING to STOPPED.

        Raises:
            IllegalStateTransitionError: If not in STOPPING state.

        """
        with self._lock:
            self._state_machine.transition(RuntimeState.STOPPED)

    def shutdown(self) -> None:
        """Transition from STOPPED to SHUTDOWN.

        Raises:
            IllegalStateTransitionError: If not in STOPPED state.

        """
        with self._lock:
            self._state_machine.transition(RuntimeState.SHUTDOWN)
            self._logger.log(
                LogSeverity.INFO,
                "Runtime shut down",
                component=_COMPONENT_NAME,
                correlation_id=self.correlation_id,
            )

    def fail(self) -> None:
        """Transition to FAILED from any state except SHUTDOWN.

        Raises:
            IllegalStateTransitionError: If in SHUTDOWN state.

        """
        with self._lock:
            self._state_machine.fail()
            self._logger.log(
                LogSeverity.CRITICAL,
                "Runtime entered FAILED state",
                component=_COMPONENT_NAME,
                correlation_id=self.correlation_id,
            )

    def recover_bootstrap(self) -> None:
        """Transition from FAILED to BOOTSTRAPPING for runtime restart.

        Raises:
            IllegalStateTransitionError: If not in FAILED state.

        """
        with self._lock:
            self._state_machine.reset_correlation_id()
            self._state_machine.transition(RuntimeState.BOOTSTRAPPING)
            self._logger.log(
                LogSeverity.INFO,
                "Recovery: transitioning to BOOTSTRAPPING",
                component=_COMPONENT_NAME,
                correlation_id=self.correlation_id,
            )

    def recover_start(self) -> None:
        """Transition from FAILED to STARTING for service restart.

        Raises:
            IllegalStateTransitionError: If not in FAILED state.

        """
        with self._lock:
            self._state_machine.reset_correlation_id()
            self._state_machine.transition(RuntimeState.STARTING)
            self._logger.log(
                LogSeverity.INFO,
                "Recovery: transitioning to STARTING",
                component=_COMPONENT_NAME,
                correlation_id=self.correlation_id,
            )

    def set_event_bus(self, event_bus: IEventBus) -> None:
        """Replace the event bus used for state-change events.

        Called by the RuntimeHost after the real EventBus is
        bootstrapped to replace the initial null implementation.

        Args:
            event_bus: The new event bus instance.

        """
        with self._lock:
            self._state_machine.set_event_bus(event_bus)

    def check_health(self) -> HealthStatus:
        """Return the health status of the lifecycle manager.

        Returns:
            The health status based on the current state.

        """
        return self._state_machine.check_health()

    def get_component_name(self) -> str:
        """Return the component name.

        Returns:
            The string ``"LifecycleManager"``.

        """
        return _COMPONENT_NAME
