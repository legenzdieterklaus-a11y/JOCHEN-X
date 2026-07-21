"""Immutable application context and live runtime state.

:class:`ApplicationContext` is the fully-injected, read-only aggregate of every
foundation service. Nothing here is static or global: the context is constructed
once during bootstrap and passed by reference to collaborators. :class:`RuntimeState`
exposes a live, thread-safe view of the current lifecycle phase and uptime.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from time import monotonic

from config.settings import ApplicationSettings, ConfigurationService
from core.environment import Environment
from core.events import EventBus
from core.scheduler import TaskScheduler
from core.registry import ServiceRegistry
from core.version import VersionManager
from plugins.loader import PluginLoader
from styles.theme import ThemeEngine

from app.di import ServiceProvider
from app.resources import ResourceManager
from app.state_machine import ApplicationState, ApplicationStateMachine


class RuntimeState:
    """Live, thread-safe view of the application's runtime status."""

    def __init__(self, state_machine: ApplicationStateMachine, *, started_at: float | None = None) -> None:
        """Create the runtime view.

        Args:
            state_machine: The authoritative lifecycle state machine.
            started_at: Optional monotonic start timestamp; defaults to now.
        """
        self._state_machine = state_machine
        self._started_at = monotonic() if started_at is None else started_at

    @property
    def state(self) -> ApplicationState:
        """Return the current lifecycle state."""
        return self._state_machine.state

    @property
    def is_ready(self) -> bool:
        """Return whether the application has reached the ready state."""
        return self._state_machine.state is ApplicationState.READY

    @property
    def uptime_seconds(self) -> float:
        """Return seconds elapsed since the runtime state was created."""
        return monotonic() - self._started_at


@dataclass(frozen=True, slots=True)
class ApplicationContext:
    """Fully-injected, immutable aggregate of all foundation services."""

    settings: ApplicationSettings
    configuration: ConfigurationService
    environment: Environment
    version: VersionManager
    logger: logging.Logger
    services: ServiceProvider
    registry: ServiceRegistry
    events: EventBus
    scheduler: TaskScheduler
    plugins: PluginLoader
    theme: ThemeEngine
    resources: ResourceManager
    runtime_state: RuntimeState
