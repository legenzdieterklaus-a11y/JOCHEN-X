"""INITIALIZE-phase bootstrap stages."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from config.settings import ApplicationSettings, ConfigurationService
from core.environment import Environment
from core.events import EventBus
from core.logging import configure_logging
from core.observability import Metrics
from core.registry import ServiceRegistry
from core.scheduler import TaskScheduler
from core.version import Version, VersionManager
from database.sqlite import ConnectionManager, MigrationManager, SettingsRepository
from styles.theme import ThemeEngine

from app.bootstrap.constants import (
    _CONFIG_DIRECTORY,
    _DEFAULT_CONFIG_FILE,
    _LOGS_DIRECTORY,
    _PROFILE_CONFIG_FILE,
)
from app.bootstrap.types import (
    BootstrapContext,
    StartupPhase,
    _require,
)
from app.di import DisposableRegistry

__all__ = [
    "ConfigurationStage",
    "DatabaseStage",
    "EnvironmentStage",
    "LoggingStage",
    "RegistryStage",
    "SchedulerStage",
    "ThemeStage",
]


@dataclass(frozen=True, slots=True)
class EnvironmentStage:
    """Resolves the runtime environment and ensures runtime directories exist."""

    name: str = "environment"
    phase: StartupPhase = StartupPhase.INITIALIZE

    def execute(self, context: BootstrapContext) -> None:
        context.environment = Environment.from_root(context.root)


@dataclass(frozen=True, slots=True)
class ConfigurationStage:
    """Loads validated application settings from the TOML configuration."""

    name: str = "configuration"
    phase: StartupPhase = StartupPhase.INITIALIZE

    def execute(self, context: BootstrapContext) -> None:
        root = context.root
        configuration = ConfigurationService(
            root / _CONFIG_DIRECTORY / _DEFAULT_CONFIG_FILE,
            root / _CONFIG_DIRECTORY / _PROFILE_CONFIG_FILE,
        )
        context.configuration = configuration
        context.settings = configuration.load()


@dataclass(frozen=True, slots=True)
class LoggingStage:
    """Configures the isolated application logger."""

    name: str = "logging"
    phase: StartupPhase = StartupPhase.INITIALIZE

    def execute(self, context: BootstrapContext) -> None:
        environment = _require(context.environment, "environment")
        settings = _require(context.settings, "settings")
        logger = configure_logging(environment.root / _LOGS_DIRECTORY, settings.log_level)
        context.logger = logger
        logger.info("bootstrap.started", extra={"context": {"version": settings.version}})


@dataclass(frozen=True, slots=True)
class DatabaseStage:
    """Initialises the SQLite database and applies the foundation schema."""

    name: str = "database"
    phase: StartupPhase = StartupPhase.INITIALIZE

    def execute(self, context: BootstrapContext) -> None:
        environment = _require(context.environment, "environment")
        settings = _require(context.settings, "settings")
        connections = ConnectionManager(environment.root / settings.database_path)
        MigrationManager(connections).migrate()
        context.connections = connections
        context.settings_repository = SettingsRepository(connections)


@dataclass(frozen=True, slots=True)
class RegistryStage:
    """Creates the DI registry and registers the composed core services."""

    name: str = "registry"
    phase: StartupPhase = StartupPhase.INITIALIZE

    def execute(self, context: BootstrapContext) -> None:
        environment = _require(context.environment, "environment")
        configuration = _require(context.configuration, "configuration")
        settings = _require(context.settings, "settings")
        logger = _require(context.logger, "logger")
        connections = _require(context.connections, "connections")
        repository = _require(context.settings_repository, "settings_repository")
        registry = ServiceRegistry()
        disposables = context.disposables or DisposableRegistry(logger)
        events = context.events or EventBus(logger=logger)
        versions = VersionManager(Version.parse(settings.version))
        registry.register(Environment, environment)
        registry.register(ConfigurationService, configuration)
        registry.register(ApplicationSettings, settings)
        registry.register(logging.Logger, logger)
        registry.register(ConnectionManager, connections)
        registry.register(SettingsRepository, repository)
        registry.register(EventBus, events)
        registry.register(VersionManager, versions)
        registry.register(DisposableRegistry, disposables)
        metrics = Metrics()
        registry.register(Metrics, metrics)
        context.registry = registry
        context.disposables = disposables
        context.events = events
        context.versions = versions
        context.metrics = metrics


@dataclass(frozen=True, slots=True)
class ThemeStage:
    """Registers the theme engine."""

    name: str = "theme"
    phase: StartupPhase = StartupPhase.INITIALIZE

    def execute(self, context: BootstrapContext) -> None:
        registry = _require(context.registry, "registry")
        theme = ThemeEngine()
        registry.register(ThemeEngine, theme)
        context.theme = theme


@dataclass(frozen=True, slots=True)
class SchedulerStage:
    """Registers the cooperative task scheduler."""

    name: str = "scheduler"
    phase: StartupPhase = StartupPhase.INITIALIZE

    def execute(self, context: BootstrapContext) -> None:
        registry = _require(context.registry, "registry")
        scheduler = TaskScheduler()
        registry.register(TaskScheduler, scheduler)
        context.scheduler = scheduler
