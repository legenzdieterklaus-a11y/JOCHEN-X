"""Strongly typed application state machine with validated transitions.

The state machine is the single source of truth for the application lifecycle
phase. Every transition is validated against an explicit adjacency table, illegal
transitions raise :class:`IllegalStateTransitionError`, and each accepted
transition emits an :class:`app.events.ApplicationStateChanged` event through an
injected publisher so observers never poll for state.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Mapping
from enum import StrEnum
from threading import RLock
from types import MappingProxyType

from core.exceptions import StateTransitionError, TransitionRejection

from app.events import ApplicationStateChanged, EventPublisher


class ApplicationState(StrEnum):
    """Exhaustive set of application lifecycle states."""

    STARTING = "starting"
    INITIALIZING = "initializing"
    LOADING_PLUGINS = "loading_plugins"
    LOADING_RESOURCES = "loading_resources"
    READY = "ready"
    BUSY = "busy"
    UPDATING = "updating"
    RESTART_REQUIRED = "restart_required"
    SHUTTING_DOWN = "shutting_down"
    SHUTDOWN = "shutdown"


class IllegalStateTransitionError(StateTransitionError):
    """Raised when a state transition is not permitted by the transition table.

    The structured rejection result (source, target, reason, allowed targets)
    is available as ``rejection``.
    """


_TRANSITIONS: dict[ApplicationState, frozenset[ApplicationState]] = {
    ApplicationState.STARTING: frozenset({ApplicationState.INITIALIZING, ApplicationState.SHUTTING_DOWN}),
    ApplicationState.INITIALIZING: frozenset({ApplicationState.LOADING_PLUGINS, ApplicationState.SHUTTING_DOWN}),
    ApplicationState.LOADING_PLUGINS: frozenset({ApplicationState.LOADING_RESOURCES, ApplicationState.SHUTTING_DOWN}),
    ApplicationState.LOADING_RESOURCES: frozenset({ApplicationState.READY, ApplicationState.SHUTTING_DOWN}),
    ApplicationState.READY: frozenset({
        ApplicationState.BUSY,
        ApplicationState.UPDATING,
        ApplicationState.RESTART_REQUIRED,
        ApplicationState.SHUTTING_DOWN,
    }),
    ApplicationState.BUSY: frozenset({ApplicationState.READY, ApplicationState.SHUTTING_DOWN}),
    ApplicationState.UPDATING: frozenset({
        ApplicationState.READY,
        ApplicationState.RESTART_REQUIRED,
        ApplicationState.SHUTTING_DOWN,
    }),
    ApplicationState.RESTART_REQUIRED: frozenset({ApplicationState.SHUTTING_DOWN}),
    ApplicationState.SHUTTING_DOWN: frozenset({ApplicationState.SHUTDOWN}),
    ApplicationState.SHUTDOWN: frozenset(),
}


def transition_table() -> Mapping[ApplicationState, frozenset[ApplicationState]]:
    """Return the complete, read-only application transition table.

    Every state appears as a key; the value is the exhaustive set of permitted
    target states. Transitions outside this table are rejected.
    """
    return MappingProxyType(_TRANSITIONS)


def _reject(
    source: ApplicationState,
    target: ApplicationState | None,
    reason: str,
    allowed: frozenset[ApplicationState],
) -> IllegalStateTransitionError:
    """Build the structured rejection carried by every denied transition."""
    return IllegalStateTransitionError(
        TransitionRejection(
            source=source.value,
            target=None if target is None else target.value,
            reason=reason,
            allowed=tuple(sorted(state.value for state in allowed)),
        )
    )


TransitionListener = Callable[[ApplicationState, ApplicationState], None]


class ApplicationStateMachine:
    """Thread-safe lifecycle state machine with validated, event-emitting transitions."""

    def __init__(
        self,
        *,
        publisher: EventPublisher | None = None,
        logger: logging.Logger | None = None,
        initial_state: ApplicationState = ApplicationState.STARTING,
    ) -> None:
        """Initialise the machine in ``initial_state``.

        Args:
            publisher: Optional event publisher used to broadcast transitions.
            logger: Optional logger for transition diagnostics.
            initial_state: The starting state; defaults to ``STARTING``.
        """
        self._state = initial_state
        self._publisher = publisher
        self._logger = logger or logging.getLogger("jochen_x.state")
        self._listeners: list[TransitionListener] = []
        self._lock = RLock()

    @property
    def state(self) -> ApplicationState:
        """Return the current lifecycle state."""
        with self._lock:
            return self._state

    def add_listener(self, listener: TransitionListener) -> Callable[[], None]:
        """Register a transition listener and return an unsubscribe callback."""
        with self._lock:
            self._listeners.append(listener)

        def unsubscribe() -> None:
            with self._lock:
                if listener in self._listeners:
                    self._listeners.remove(listener)

        return unsubscribe

    def can_transition(self, target: ApplicationState) -> bool:
        """Return whether a transition to ``target`` is currently permitted."""
        with self._lock:
            return target in _TRANSITIONS[self._state]

    def allowed_transitions(self) -> frozenset[ApplicationState]:
        """Return the exhaustive set of currently permitted target states."""
        with self._lock:
            return _TRANSITIONS[self._state]

    def assert_state(self, *expected: ApplicationState) -> None:
        """Raise :class:`IllegalStateTransitionError` if not in an expected state."""
        with self._lock:
            if self._state not in expected:
                allowed = ", ".join(state.value for state in expected)
                raise _reject(
                    self._state,
                    None,
                    f"Expected one of [{allowed}] but current state is '{self._state.value}'",
                    frozenset(expected),
                )

    def transition(self, target: ApplicationState) -> ApplicationState:
        """Validate and perform a transition to ``target``.

        Args:
            target: The desired next state.

        Returns:
            The new current state.

        Raises:
            IllegalStateTransitionError: If the transition is not permitted.
        """
        with self._lock:
            previous = self._state
            if target not in _TRANSITIONS[previous]:
                raise _reject(
                    previous,
                    target,
                    f"Illegal transition: '{previous.value}' -> '{target.value}'",
                    _TRANSITIONS[previous],
                )
            self._state = target
            listeners = tuple(self._listeners)
        self._logger.info("state.transition", extra={"context": {"from": previous.value, "to": target.value}})
        if self._publisher is not None:
            ApplicationStateChanged(previous.value, target.value).publish(self._publisher)
        for listener in listeners:
            listener(previous, target)
        return target
