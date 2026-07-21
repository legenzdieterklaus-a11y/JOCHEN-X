"""Startup sequence that drives the application from Starting to Ready.

:class:`StartupSequence` advances the lifecycle state machine through its
initialisation phases, invoking the matching bootstrap phase at each step and
emitting the corresponding lifecycle events. It is the single place that ties the
state machine, the bootstrap manager, and the event bus together.
"""

from __future__ import annotations

import logging
from pathlib import Path
from time import perf_counter

from core.events import EventBus

from app.bootstrap import BootstrapManager, StartupPhase
from app.context import ApplicationContext
from app.events import ApplicationReady, ApplicationStarted, ApplicationStarting
from app.state_machine import ApplicationState, ApplicationStateMachine


class StartupSequence:
    """Orchestrates the ordered transition to the ready state."""

    def __init__(
        self,
        *,
        state_machine: ApplicationStateMachine,
        bootstrap_manager: BootstrapManager,
        events: EventBus,
        logger: logging.Logger | None = None,
    ) -> None:
        """Create the startup sequence.

        Args:
            state_machine: The lifecycle state machine to advance.
            bootstrap_manager: Manager providing the ordered bootstrap phases.
            events: The shared event bus for lifecycle events.
            logger: Optional logger for diagnostics.
        """
        self._state = state_machine
        self._bootstrap = bootstrap_manager
        self._events = events
        self._logger = logger or logging.getLogger("jochen_x.startup")

    def execute(self, root: Path) -> ApplicationContext:
        """Bootstrap the foundation and drive the state machine to ``READY``.

        Args:
            root: The application root directory.

        Returns:
            The fully-initialised, immutable application context.
        """
        started = perf_counter()
        context = self._bootstrap.begin(root)
        context.events = self._events

        self._state.transition(ApplicationState.INITIALIZING)
        self._bootstrap.run_phase(context, StartupPhase.INITIALIZE)
        settings = context.settings
        version = settings.version if settings is not None else "0.0.0"
        ApplicationStarting(version).publish(self._events)
        registry = context.registry
        service_count = len(registry.descriptors()) if registry is not None else 0
        ApplicationStarted(service_count).publish(self._events)

        self._state.transition(ApplicationState.LOADING_PLUGINS)
        self._bootstrap.run_phase(context, StartupPhase.LOAD_PLUGINS)

        self._state.transition(ApplicationState.LOADING_RESOURCES)
        self._bootstrap.run_phase(context, StartupPhase.LOAD_RESOURCES)

        self._bootstrap.run_phase(context, StartupPhase.FINALIZE)
        application_context = self._bootstrap.build_context(context, self._state)

        self._state.transition(ApplicationState.READY)
        startup_ms = (perf_counter() - started) * 1_000
        ApplicationReady(startup_ms).publish(self._events)
        self._logger.info("startup.ready", extra={"context": {"startup_ms": round(startup_ms, 3)}})
        return application_context
