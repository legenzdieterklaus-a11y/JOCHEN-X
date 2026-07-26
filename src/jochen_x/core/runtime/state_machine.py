"""Lifecycle state machine engine for the JOCHEN X Core Runtime.

The ``StateMachine`` enforces the explicit transition table from the
specification.  Only the transitions listed in the table are allowed;
any other transition raises ``IllegalStateTransitionError``.

Every state transition is atomic and thread-safe.  The machine emits
a ``RuntimeStateChangedEvent`` on each successful transition and
records it in the audit log.

All operations are thread-safe.
"""

from __future__ import annotations

from threading import RLock
from uuid import uuid4

from jochen_x.core.exceptions.lifecycle import IllegalStateTransitionError
from jochen_x.core.interfaces.audit import IAuditLog
from jochen_x.core.interfaces.event_bus import IEventBus
from jochen_x.core.interfaces.logging import ILogger
from jochen_x.core.types.events import RuntimeStateChangedEvent
from jochen_x.core.types.health_status import HealthStatus
from jochen_x.core.types.runtime_state import RuntimeState
from jochen_x.core.types.severity import LogSeverity

__all__ = ["StateMachine"]

_COMPONENT_NAME = "StateMachine"

_TRANSITION_TABLE: dict[RuntimeState, set[RuntimeState]] = {
    RuntimeState.CREATED: {RuntimeState.BOOTSTRAPPING},
    RuntimeState.BOOTSTRAPPING: {RuntimeState.INITIALIZING},
    RuntimeState.INITIALIZING: {RuntimeState.READY},
    RuntimeState.READY: {RuntimeState.STARTING},
    RuntimeState.STARTING: {RuntimeState.RUNNING},
    RuntimeState.RUNNING: {RuntimeState.PAUSED, RuntimeState.STOPPING},
    RuntimeState.PAUSED: {RuntimeState.RUNNING, RuntimeState.STOPPING},
    RuntimeState.STOPPING: {RuntimeState.STOPPED},
    RuntimeState.STOPPED: {RuntimeState.SHUTDOWN, RuntimeState.STARTING},
    RuntimeState.FAILED: {RuntimeState.BOOTSTRAPPING, RuntimeState.STARTING},
}


class StateMachine:
    """Explicit lifecycle state machine with audited transitions.

    Manages the runtime lifecycle state and enforces the transition
    table from the specification.  Every transition is atomic, logged,
    audited, and published as an event.

    The ``FAILED`` state is reachable from any other state (except
    ``SHUTDOWN``).  All other transitions must follow the explicit
    table.

    Args:
        event_bus: Event bus for publishing state-change events.
        audit_log: Audit log for recording transitions.
        logger: Structured logger for transition logging.

    """

    def __init__(
        self,
        *,
        event_bus: IEventBus,
        audit_log: IAuditLog,
        logger: ILogger,
    ) -> None:
        """Initialise the state machine in CREATED state."""
        self._event_bus: IEventBus = event_bus
        self._audit_log: IAuditLog = audit_log
        self._logger: ILogger = logger
        self._lock: RLock = RLock()
        self._state: RuntimeState = RuntimeState.CREATED
        self._correlation_id: str = str(uuid4())

    @property
    def state(self) -> RuntimeState:
        """Return the current state.

        Returns:
            The current ``RuntimeState``.

        """
        with self._lock:
            return self._state

    @property
    def correlation_id(self) -> str:
        """Return the current correlation ID.

        Returns:
            The active correlation ID string.

        """
        return self._correlation_id

    def transition(self, target: RuntimeState) -> None:
        """Transition to the given target state.

        Validates the transition against the explicit table, updates
        the state atomically, emits a ``RuntimeStateChangedEvent``,
        records the transition in the audit log, and logs the change.

        Args:
            target: The desired target state.

        Raises:
            IllegalStateTransitionError: If the transition is not
                allowed by the transition table.

        """
        with self._lock:
            old_state = self._state

            if target == RuntimeState.FAILED:
                if old_state == RuntimeState.SHUTDOWN:
                    raise IllegalStateTransitionError(
                        old_state,
                        target,
                        correlation_id=self._correlation_id,
                        component=_COMPONENT_NAME,
                    )
            else:
                allowed = _TRANSITION_TABLE.get(old_state, set())
                if target not in allowed:
                    raise IllegalStateTransitionError(
                        old_state,
                        target,
                        correlation_id=self._correlation_id,
                        component=_COMPONENT_NAME,
                    )

            self._state = target

        event = RuntimeStateChangedEvent(
            old_state=old_state,
            new_state=target,
            source=_COMPONENT_NAME,
            correlation_id=self._correlation_id,
        )

        transition_msg = "State transition: " + old_state.value + " -> " + target.value
        self._logger.log(
            LogSeverity.INFO,
            transition_msg,
            component=_COMPONENT_NAME,
            correlation_id=self._correlation_id,
        )

        self._audit_log.record(event)
        self._publish_event(event)

    def fail(self) -> None:
        """Transition to the FAILED state from any state except SHUTDOWN.

        Raises:
            IllegalStateTransitionError: If in SHUTDOWN state.

        """
        self.transition(RuntimeState.FAILED)

    def reset_correlation_id(self) -> str:
        """Generate and set a new correlation ID.

        Returns:
            The new correlation ID.

        """
        self._correlation_id = str(uuid4())
        return self._correlation_id

    def set_event_bus(self, event_bus: IEventBus) -> None:
        """Replace the event bus used for state-change events.

        Args:
            event_bus: The new event bus instance.

        """
        with self._lock:
            self._event_bus = event_bus

    def check_health(self) -> HealthStatus:
        """Return the health status of the state machine.

        Returns:
            ``HEALTHY`` if RUNNING, ``DEGRADED`` if PAUSED or READY,
            ``UNHEALTHY`` if FAILED, ``UNKNOWN`` otherwise.

        """
        with self._lock:
            if self._state == RuntimeState.RUNNING:
                return HealthStatus.HEALTHY
            if self._state in (RuntimeState.PAUSED, RuntimeState.READY):
                return HealthStatus.DEGRADED
            if self._state == RuntimeState.FAILED:
                return HealthStatus.UNHEALTHY
            return HealthStatus.UNKNOWN

    def get_component_name(self) -> str:
        """Return the component name.

        Returns:
            The string ``"StateMachine"``.

        """
        return _COMPONENT_NAME

    def _publish_event(self, event: RuntimeStateChangedEvent) -> None:
        """Publish a state-change event, suppressing bus errors."""
        try:
            self._event_bus.publish(event)
        except Exception:  # noqa: BLE001
            publish_msg = (
                "Failed to publish state change event: "
                + event.old_state.value + " -> " + event.new_state.value
            )
            self._logger.log(
                LogSeverity.WARNING,
                publish_msg,
                component=_COMPONENT_NAME,
                correlation_id=self._correlation_id,
            )
