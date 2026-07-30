"""Deterministic, phase-grouped bootstrap of the application foundation.

:class:`BootstrapManager` executes an ordered set of isolated
:class:`BootstrapStage` objects. Stages are grouped by :class:`StartupPhase` so
the startup sequence can advance the application state machine between phases
while every stage remains independently testable. Each stage populates a mutable
:class:`BootstrapContext`; the manager then assembles an immutable
:class:`app.context.ApplicationContext`.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol, TypeVar

if TYPE_CHECKING:
    from sdk.plugin import PluginRuntime

from config.settings import ApplicationSettings, ConfigurationService
from core.environment import Environment
from core.events import EventBus
from core.exceptions import JochenXError
from core.logging import configure_logging
from core.registry import ServiceRegistry
from core.scheduler import TaskScheduler
from core.version import Version, VersionManager
from database.sqlite import ConnectionManager, MigrationManager, SettingsRepository
from plugins.loader import PluginCatalog, PluginLoader, PluginManifest
from styles.theme import ThemeEngine

from app.context import ApplicationContext, RuntimeState
from app.di import DisposableRegistry, ServiceProvider
from app.events import PluginActivated, PluginActivating, PluginFailed, PluginLoaded, PluginLoading
from app.resources import ResourceManager
from app.state_machine import ApplicationStateMachine

__all__ = [
    "BootstrapContext",
    "BootstrapError",
    "BootstrapManager",
    "BootstrapStage",
    "ConfigurationStage",
    "DatabaseStage",
    "DependencyInjectionStage",
    "DeveloperToolsStage",
    "EnvironmentStage",
    "LoggingStage",
    "PluginActivationStage",
    "PluginDiscoveryStage",
    "PluginRuntimePool",
    "PluginSecurityStage",
    "RegistryStage",
    "ResourceStage",
    "SchedulerStage",
    "StartupPhase",
    "ThemeStage",
    "default_stages",
]

T = TypeVar("T")

_CONFIG_DIRECTORY = "config"
_DEFAULT_CONFIG_FILE = "default.toml"
_PROFILE_CONFIG_FILE = "profile.toml"
_LOGS_DIRECTORY = "logs"
_LOG_FILE_NAME = "jochen_x.log"


class BootstrapError(JochenXError):
    """Raised when a bootstrap stage cannot satisfy its contract."""


class StartupPhase(IntEnum):
    """Ordered bootstrap phases aligned with the lifecycle state machine."""

    INITIALIZE = 1
    LOAD_PLUGINS = 2
    LOAD_RESOURCES = 3
    FINALIZE = 4


@dataclass(slots=True)
class BootstrapContext:
    """Mutable accumulator populated by bootstrap stages."""

    root: Path
    environment: Environment | None = None
    configuration: ConfigurationService | None = None
    settings: ApplicationSettings | None = None
    logger: logging.Logger | None = None
    connections: ConnectionManager | None = None
    settings_repository: SettingsRepository | None = None
    registry: ServiceRegistry | None = None
    events: EventBus | None = None
    disposables: DisposableRegistry | None = None
    versions: VersionManager | None = None
    plugins: PluginLoader | None = None
    manifests: tuple[PluginManifest, ...] = ()
    admitted_manifests: tuple[PluginManifest, ...] = ()
    plugin_runtimes: tuple[PluginRuntime, ...] = ()
    theme: ThemeEngine | None = None
    resources: ResourceManager | None = None
    scheduler: TaskScheduler | None = None
    service_provider: ServiceProvider | None = None


def _require(value: T | None, name: str) -> T:
    """Return ``value`` or raise :class:`BootstrapError` if it is missing."""
    if value is None:
        raise BootstrapError(f"Bootstrap stage dependency missing: {name}")
    return value


class BootstrapStage(Protocol):
    """A single, isolated, independently-testable bootstrap step."""

    @property
    def name(self) -> str:
        """Return the stable stage name for diagnostics."""
        ...

    @property
    def phase(self) -> StartupPhase:
        """Return the phase in which this stage runs."""
        ...

    def execute(self, context: BootstrapContext) -> None:
        """Perform the stage's work against the shared bootstrap context."""
        ...


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
        context.registry = registry
        context.disposables = disposables
        context.events = events
        context.versions = versions


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


@dataclass(frozen=True, slots=True)
class PluginDiscoveryStage:
    """Discovers compatible plugin manifests without importing plugin code."""

    name: str = "plugins"
    phase: StartupPhase = StartupPhase.LOAD_PLUGINS

    def execute(self, context: BootstrapContext) -> None:
        environment = _require(context.environment, "environment")
        settings = _require(context.settings, "settings")
        versions = _require(context.versions, "versions")
        registry = _require(context.registry, "registry")
        events = _require(context.events, "events")
        logger = _require(context.logger, "logger")
        loader = PluginLoader(environment.root / settings.plugin_directory, versions)
        registry.register(PluginLoader, loader)
        context.plugins = loader
        try:
            manifests = loader.discover()
        except Exception as error:  # discovery failure is recoverable; run with no plugins
            logger.error("plugins.discovery_failed", exc_info=error)
            PluginFailed("", str(error)).publish(events)
            context.manifests = ()
            registry.register(PluginCatalog, PluginCatalog(()))
            return
        for manifest in manifests:
            PluginLoading(manifest.identifier).publish(events)
            PluginLoaded(manifest.identifier, str(manifest.version)).publish(events)
        context.manifests = manifests
        registry.register(
            PluginCatalog,
            PluginCatalog(tuple(manifest.identifier for manifest in manifests)),
        )
        logger.info("plugins.discovered", extra={"context": {"count": len(manifests)}})


@dataclass(frozen=True, slots=True)
class PluginSecurityStage:
    """Verifies discovered plugin manifests against integrity policy and trust ledger.

    Executes two validation steps per ADR-005 D5 and the Runtime Pipeline:
    Step 1 — Integrity Validation: evaluates structural evidence against
    the integrity policy and determines trust level / signature status.
    Step 2 — API Version Gate (WP-03): checks manifest-level API version
    compatibility BEFORE any plugin code is imported.
    """

    name: str = "plugin_security"
    phase: StartupPhase = StartupPhase.LOAD_PLUGINS

    def execute(self, context: BootstrapContext) -> None:
        from sdk.version import SDK_API_VERSION, ApiVersion

        from app.security.events import PluginRejected
        from app.security.plugin_security import IntegrityPolicy, PluginSecurity

        events = _require(context.events, "events")
        registry = _require(context.registry, "registry")
        logger = _require(context.logger, "logger")
        try:
            security = registry.get(PluginSecurity)
        except LookupError:
            security = PluginSecurity(events, logger=logger)
            registry.register(PluginSecurity, security)

        host_api = ApiVersion.parse(SDK_API_VERSION)
        admitted: list[PluginManifest] = []

        for manifest in context.manifests:
            identifier = manifest.identifier

            integrity = security.validate_integrity(manifest)
            if not integrity.admitted:
                logger.warning(
                    "plugins.security.integrity_rejected",
                    extra={"context": {
                        "identifier": identifier,
                        "reason": integrity.reason,
                        "trust": integrity.trust.value,
                    }},
                )
                continue

            if manifest.api_version is not None:
                plugin_api = ApiVersion.parse(str(manifest.api_version))
                if not host_api.is_compatible_with(plugin_api):
                    reason = (
                        f"API version incompatible: plugin requires "
                        f"{manifest.api_version}, host provides {SDK_API_VERSION}"
                    )
                    PluginRejected(identifier, reason).publish(events)
                    logger.warning(
                        "plugins.security.api_version_rejected",
                        extra={"context": {
                            "identifier": identifier,
                            "plugin_api": str(manifest.api_version),
                            "host_api": SDK_API_VERSION,
                        }},
                    )
                    continue

            admitted.append(manifest)

        context.admitted_manifests = tuple(admitted)
        filtered = PluginCatalog(tuple(m.identifier for m in admitted))
        with registry._lock:
            registry._registrations.pop(PluginCatalog, None)
        registry.register(PluginCatalog, filtered)
        logger.info(
            "plugins.security.completed",
            extra={"context": {"admitted": len(admitted), "total": len(context.manifests)}},
        )


@dataclass(frozen=True, slots=True)
class PluginRuntimePool:
    """Ordered collection of activated plugin runtimes for registry storage."""

    runtimes: tuple[PluginRuntime, ...] = ()


@dataclass(frozen=True, slots=True)
class PluginActivationStage:
    """Imports, instantiates, wires, and starts admitted plugins."""

    name: str = "plugin_activation"
    phase: StartupPhase = StartupPhase.FINALIZE

    def execute(self, context: BootstrapContext) -> None:
        import importlib
        import sys

        from core.events import Event
        from sdk.config import FilePluginConfigStorage
        from sdk.context import PluginContextBuilder
        from sdk.manifest import PluginMetadata
        from sdk.plugin import Plugin, PluginRuntime

        settings = _require(context.settings, "settings")
        environment = _require(context.environment, "environment")
        registry = _require(context.registry, "registry")
        events = _require(context.events, "events")
        logger = _require(context.logger, "logger")

        plugin_dir = environment.root / settings.plugin_directory
        admitted_ids = {m.identifier for m in context.admitted_manifests}
        runtimes: list[PluginRuntime] = []

        parent = str(plugin_dir)
        added_to_path = parent not in sys.path
        if added_to_path:
            sys.path.insert(0, parent)
        try:
            for manifest in context.admitted_manifests:
                identifier = manifest.identifier
                try:
                    PluginActivating(identifier).publish(events)

                    module_path = plugin_dir / identifier
                    if not module_path.is_dir():
                        raise ImportError(f"Plugin directory not found: {module_path}")

                    module = importlib.import_module(identifier)

                    plugin_class: type[Plugin] | None = None
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (
                            isinstance(attr, type)
                            and issubclass(attr, Plugin)
                            and attr is not Plugin
                            and not getattr(attr, "__abstractmethods__", None)
                        ):
                            plugin_class = attr
                            break

                    if plugin_class is None:
                        raise ImportError(f"No concrete Plugin subclass found in {identifier!r}")

                    plugin = plugin_class()
                    metadata: PluginMetadata = plugin.metadata()

                    for dep in metadata.dependencies:
                        if dep.identifier not in admitted_ids:
                            raise ValueError(
                                f"Unresolved dependency: {dep.identifier!r} "
                                f"required by {identifier!r}"
                            )

                    config_root = plugin_dir / identifier
                    resources_root = plugin_dir / identifier / "resources"
                    resources_root.mkdir(parents=True, exist_ok=True)

                    plugin_context = (
                        PluginContextBuilder(metadata)
                        .with_event_bus(events, event_type=Event)
                        .with_service(logging.Logger, logger)
                        .with_config_storage(FilePluginConfigStorage(config_root))
                        .with_resources_root(resources_root)
                        .with_logger(logger)
                        .with_application_version(settings.version)
                        .build()
                    )

                    runtime = PluginRuntime(plugin)
                    runtime.initialize(plugin_context)
                    runtime.start()

                    runtimes.append(runtime)

                    PluginActivated(identifier, metadata.version).publish(events)

                    logger.info(
                        "plugins.activation.started",
                        extra={"context": {"identifier": identifier, "version": metadata.version}},
                    )
                except Exception as error:
                    PluginFailed(identifier, str(error)).publish(events)
                    logger.error(
                        "plugins.activation.failed",
                        extra={"context": {"identifier": identifier, "error": str(error)}},
                    )
        finally:
            if added_to_path:
                try:
                    sys.path.remove(parent)
                except ValueError:
                    pass

        context.plugin_runtimes = tuple(runtimes)
        pool = PluginRuntimePool(tuple(runtimes))
        registry.register(PluginRuntimePool, pool)
        logger.info(
            "plugins.activation.completed",
            extra={"context": {"activated": len(runtimes), "total": len(context.admitted_manifests)}},
        )


@dataclass(frozen=True, slots=True)
class ResourceStage:
    """Creates and registers the resource manager."""

    name: str = "resources"
    phase: StartupPhase = StartupPhase.LOAD_RESOURCES

    def execute(self, context: BootstrapContext) -> None:
        environment = _require(context.environment, "environment")
        disposables = _require(context.disposables, "disposables")
        registry = _require(context.registry, "registry")
        logger = _require(context.logger, "logger")
        resources = ResourceManager(environment, disposables, logger=logger)
        registry.register(ResourceManager, resources)
        context.resources = resources


@dataclass(frozen=True, slots=True)
class DeveloperToolsStage:
    """Registers the developer platform when developer mode is enabled."""

    name: str = "developer_tools"
    phase: StartupPhase = StartupPhase.FINALIZE

    def execute(self, context: BootstrapContext) -> None:
        settings = _require(context.settings, "settings")
        if not settings.developer_enabled:
            return
        environment = _require(context.environment, "environment")
        registry = _require(context.registry, "registry")
        events = _require(context.events, "events")
        plugins = _require(context.plugins, "plugins")
        logger = _require(context.logger, "logger")
        try:
            from developer.platform import DeveloperPlatform
        except ImportError as error:
            logger.warning("developer.unavailable", extra={"context": {"error": str(error)}})
            return
        registry.register(
            DeveloperPlatform,
            DeveloperPlatform(
                enabled=True,
                events=events,
                services=registry,
                plugins=plugins,
                log_file=environment.root / _LOGS_DIRECTORY / _LOG_FILE_NAME,
            ),
        )


@dataclass(frozen=True, slots=True)
class DependencyInjectionStage:
    """Publishes the service-provider facade and validates the container."""

    name: str = "dependency_injection"
    phase: StartupPhase = StartupPhase.FINALIZE

    def execute(self, context: BootstrapContext) -> None:
        registry = _require(context.registry, "registry")
        provider = ServiceProvider(registry)
        registry.register(ServiceProvider, provider)
        registry.validate()
        context.service_provider = provider


def default_stages() -> tuple[BootstrapStage, ...]:
    """Return the default, deterministically-ordered bootstrap stages."""
    return (
        EnvironmentStage(),
        ConfigurationStage(),
        LoggingStage(),
        DatabaseStage(),
        RegistryStage(),
        ThemeStage(),
        SchedulerStage(),
        PluginDiscoveryStage(),
        PluginSecurityStage(),
        ResourceStage(),
        PluginActivationStage(),
        DeveloperToolsStage(),
        DependencyInjectionStage(),
    )


@dataclass(frozen=True, slots=True)
class BootstrapManager:
    """Runs bootstrap stages by phase and builds the application context."""

    stages: tuple[BootstrapStage, ...] = field(default_factory=default_stages)

    def begin(self, root: Path) -> BootstrapContext:
        """Create a fresh bootstrap context rooted at ``root``."""
        return BootstrapContext(root=root)

    def run_phase(self, context: BootstrapContext, phase: StartupPhase) -> None:
        """Execute every stage belonging to ``phase`` in registration order.

        Raises:
            BootstrapError: If a stage fails; the original error is chained.
        """
        for stage in self.stages:
            if stage.phase is not phase:
                continue
            try:
                stage.execute(context)
            except BootstrapError:
                raise
            except Exception as error:
                raise BootstrapError(f"Bootstrap stage failed: {stage.name}") from error

    def build_context(self, context: BootstrapContext, state_machine: ApplicationStateMachine) -> ApplicationContext:
        """Assemble the immutable application context from a populated bootstrap context."""
        return ApplicationContext(
            settings=_require(context.settings, "settings"),
            configuration=_require(context.configuration, "configuration"),
            environment=_require(context.environment, "environment"),
            version=_require(context.versions, "versions"),
            logger=_require(context.logger, "logger"),
            services=_require(context.service_provider, "service_provider"),
            registry=_require(context.registry, "registry"),
            events=_require(context.events, "events"),
            scheduler=_require(context.scheduler, "scheduler"),
            plugins=_require(context.plugins, "plugins"),
            theme=_require(context.theme, "theme"),
            resources=_require(context.resources, "resources"),
            runtime_state=RuntimeState(state_machine),
        )
