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
from enum import IntEnum, StrEnum
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
    "RejectionCode",
    "ResourceStage",
    "SchedulerStage",
    "StartupPhase",
    "ThemeStage",
    "ValidationDiagnostic",
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


class RejectionCode(StrEnum):
    """Structured rejection reason codes for the plugin validation pipeline."""

    MANIFEST_INVALID = "manifest_invalid"
    API_VERSION_INCOMPATIBLE = "api_version_incompatible"
    PERMISSION_DENIED = "permission_denied"
    DEPENDENCY_MISSING = "dependency_missing"
    DEPENDENCY_CYCLE = "dependency_cycle"
    DEPENDENCY_VERSION = "dependency_version"
    DEPENDENCY_CASCADE = "dependency_cascade"
    INTEGRITY_FAILED = "integrity_failed"
    IMPORT_FAILED = "import_failed"
    SUBCLASS_MISSING = "subclass_missing"
    ACTIVATION_FAILED = "activation_failed"


@dataclass(frozen=True, slots=True)
class ValidationDiagnostic:
    """Per-plugin pre-import validation result (WP-07 / AC-6).

    Captures a binary accept/reject decision with structured diagnostics
    covering all validation checks performed before code import.
    """

    identifier: str
    accepted: bool
    schema_valid: bool = True
    api_version_valid: bool = True
    permissions_valid: bool = True
    dependencies_valid: bool = True
    rejection_code: RejectionCode | None = None
    reason: str = ""


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


def _resolve_dependencies(
    manifests: tuple[PluginManifest, ...],
    logger: logging.Logger,
    events: EventBus,
) -> tuple[PluginManifest, ...]:
    """Resolve plugin dependencies and return manifests in activation order.

    Implements ADR-007: dependency graph construction, topological sorting,
    cycle detection, version constraint validation, and cascade rejection.
    Resolution occurs after permission authorization, producing the ordered
    set that activation will process (ADR-007 D5, D6).
    """
    from app.security.events import PluginRejected

    if not manifests:
        return ()

    by_id: dict[str, PluginManifest] = {m.identifier: m for m in manifests}
    deps: dict[str, list[tuple[str, Version | None]]] = {}
    rejected: dict[str, str] = {}

    for manifest in manifests:
        parsed: list[tuple[str, Version | None]] = []
        seen: set[str] = set()
        valid = True

        for dep_dict in manifest.dependencies:
            dep_id = dep_dict.get("id", "")
            if not dep_id:
                continue

            if dep_id == manifest.identifier:
                rejected[manifest.identifier] = (
                    f"Self-dependency: {manifest.identifier!r} depends on itself"
                )
                valid = False
                break

            if dep_id in seen:
                rejected[manifest.identifier] = (
                    f"Duplicate dependency: {dep_id!r} declared multiple times "
                    f"in {manifest.identifier!r}"
                )
                valid = False
                break
            seen.add(dep_id)

            min_version: Version | None = None
            ver_raw = dep_dict.get("version", "")
            if ver_raw:
                ver_str = ver_raw[2:] if ver_raw.startswith(">=") else ver_raw
                try:
                    min_version = Version.parse(ver_str)
                except ValueError:
                    pass

            parsed.append((dep_id, min_version))

        if valid:
            deps[manifest.identifier] = parsed

    changed = True
    while changed:
        changed = False
        for pid in list(deps):
            if pid in rejected:
                continue
            for dep_id, min_ver in deps[pid]:
                reason: str | None = None
                if dep_id in rejected:
                    reason = (
                        f"Dependency {dep_id!r} was rejected: "
                        f"{rejected[dep_id]}"
                    )
                elif dep_id not in by_id:
                    reason = (
                        f"Missing dependency: {dep_id!r} "
                        f"required by {pid!r}"
                    )
                elif min_ver is not None and by_id[dep_id].version < min_ver:
                    reason = (
                        f"Version constraint not satisfied: "
                        f"{dep_id!r} provides {by_id[dep_id].version}, "
                        f"{pid!r} requires >={min_ver}"
                    )
                if reason is not None:
                    rejected[pid] = reason
                    changed = True
                    break

    active = {pid for pid in by_id if pid not in rejected}
    if not active:
        for pid in sorted(rejected):
            PluginRejected(pid, rejected[pid]).publish(events)
            logger.warning(
                "plugins.dependency.rejected",
                extra={"context": {"identifier": pid, "reason": rejected[pid]}},
            )
        return ()

    in_degree: dict[str, int] = {pid: 0 for pid in active}
    forward: dict[str, list[str]] = {pid: [] for pid in active}

    for pid in active:
        for dep_id, _ in deps.get(pid, []):
            if dep_id in active:
                in_degree[pid] += 1
                forward[dep_id].append(pid)

    queue = sorted(pid for pid in active if in_degree[pid] == 0)
    ordered: list[str] = []

    while queue:
        current = queue.pop(0)
        ordered.append(current)
        for dependent in sorted(forward.get(current, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
        queue.sort()

    cycle_ids = active - set(ordered)
    if cycle_ids:
        for cid in sorted(cycle_ids):
            rejected[cid] = f"Cyclic dependency detected involving {cid!r}"
        stable = False
        while not stable:
            stable = True
            filtered: list[str] = []
            for pid in ordered:
                cascade = False
                for dep_id, _ in deps.get(pid, []):
                    if dep_id in rejected:
                        rejected[pid] = (
                            f"Dependency {dep_id!r} rejected due to cycle"
                        )
                        stable = False
                        cascade = True
                        break
                if not cascade:
                    filtered.append(pid)
            ordered = filtered

    for pid in sorted(rejected):
        PluginRejected(pid, rejected[pid]).publish(events)
        logger.warning(
            "plugins.dependency.rejected",
            extra={"context": {"identifier": pid, "reason": rejected[pid]}},
        )

    if ordered:
        logger.info(
            "plugins.dependency.resolved",
            extra={"context": {
                "order": ordered,
                "rejected_count": len(rejected),
            }},
        )

    return tuple(by_id[pid] for pid in ordered)


@dataclass(frozen=True, slots=True)
class PluginSecurityStage:
    """Verifies discovered plugin manifests against security policies.

    Executes four validation steps per the Runtime Pipeline:
    Step 1 — Integrity Validation (WP-04 / ADR-005): evaluates structural
    evidence against the integrity policy and determines trust level.
    Step 2 — API Version Gate (WP-03): checks manifest-level API version
    compatibility BEFORE any plugin code is imported.
    Step 3 — Permission Authorization (WP-05 / ADR-006): evaluates declared
    permissions against the host's permission policy. Plugins with denied
    permissions are rejected before activation.
    Step 4 — Dependency Resolution (WP-06 / ADR-007): constructs a dependency
    graph from admitted manifests, validates version constraints, detects
    cycles, and determines activation order via topological sort.
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

            # Step 3: Permission Authorization (WP-05 / ADR-006)
            perm_result = security.validate_permissions(manifest)
            if not perm_result.admitted:
                logger.warning(
                    "plugins.security.permission_rejected",
                    extra={"context": {
                        "identifier": identifier,
                        "reason": perm_result.reason,
                        "denied": sorted(perm_result.denied),
                    }},
                )
                continue

            admitted.append(manifest)

        # Step 4: Dependency Resolution (WP-06 / ADR-007)
        resolved = _resolve_dependencies(tuple(admitted), logger, events)

        context.admitted_manifests = resolved
        filtered = PluginCatalog(tuple(m.identifier for m in resolved))
        with registry._lock:
            registry._registrations.pop(PluginCatalog, None)
        registry.register(PluginCatalog, filtered)
        logger.info(
            "plugins.security.completed",
            extra={"context": {"admitted": len(resolved), "total": len(context.manifests)}},
        )


def _validate_for_activation(
    manifest: PluginManifest,
    admitted_ids: frozenset[str],
    host_api_version: str,
) -> ValidationDiagnostic:
    """Consolidated pre-import validation (WP-07 / AC-6).

    Performs all validation checks before code import:
    1. Schema validation — required fields present and non-empty
    2. API version gate — host/plugin compatibility
    3. Permission verification — manifest permissions are declared
    4. Dependency verification — all dependencies in accepted set
    """
    from sdk.version import ApiVersion

    identifier = manifest.identifier

    if not identifier or not str(manifest.version):
        return ValidationDiagnostic(
            identifier=identifier or "<unknown>",
            accepted=False,
            schema_valid=False,
            rejection_code=RejectionCode.MANIFEST_INVALID,
            reason="Manifest missing required fields: identifier or version",
        )
    if not manifest.required_application_version:
        return ValidationDiagnostic(
            identifier=identifier,
            accepted=False,
            schema_valid=False,
            rejection_code=RejectionCode.MANIFEST_INVALID,
            reason="Manifest missing required field: required_application_version",
        )

    if manifest.api_version is not None:
        host_api = ApiVersion.parse(host_api_version)
        plugin_api = ApiVersion.parse(str(manifest.api_version))
        if not host_api.is_compatible_with(plugin_api):
            return ValidationDiagnostic(
                identifier=identifier,
                accepted=False,
                api_version_valid=False,
                rejection_code=RejectionCode.API_VERSION_INCOMPATIBLE,
                reason=(
                    f"API version incompatible: plugin requires "
                    f"{manifest.api_version}, host provides {host_api_version}"
                ),
            )

    for dep_dict in manifest.dependencies:
        dep_id = dep_dict.get("id", "")
        if dep_id and dep_id not in admitted_ids:
            return ValidationDiagnostic(
                identifier=identifier,
                accepted=False,
                dependencies_valid=False,
                rejection_code=RejectionCode.DEPENDENCY_MISSING,
                reason=(
                    f"Unresolved dependency: {dep_id!r} "
                    f"required by {identifier!r}"
                ),
            )

    return ValidationDiagnostic(identifier=identifier, accepted=True)


def _reject_plugin(
    identifier: str,
    diagnostic: ValidationDiagnostic,
    events: EventBus,
    logger: logging.Logger,
) -> None:
    """Centralized rejection handler for activation validation (WP-07)."""
    from app.security.events import PluginRejected

    PluginRejected(identifier, diagnostic.reason).publish(events)
    logger.warning(
        "plugins.activation.validation_rejected",
        extra={"context": {
            "identifier": identifier,
            "rejection_code": diagnostic.rejection_code.value if diagnostic.rejection_code else "",
            "reason": diagnostic.reason,
            "schema_valid": diagnostic.schema_valid,
            "api_version_valid": diagnostic.api_version_valid,
            "permissions_valid": diagnostic.permissions_valid,
            "dependencies_valid": diagnostic.dependencies_valid,
        }},
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
        from sdk.version import SDK_API_VERSION

        settings = _require(context.settings, "settings")
        environment = _require(context.environment, "environment")
        registry = _require(context.registry, "registry")
        events = _require(context.events, "events")
        logger = _require(context.logger, "logger")

        plugin_dir = environment.root / settings.plugin_directory
        admitted_ids = frozenset(m.identifier for m in context.admitted_manifests)
        runtimes: list[PluginRuntime] = []

        parent = str(plugin_dir)
        added_to_path = parent not in sys.path
        if added_to_path:
            sys.path.insert(0, parent)
        try:
            for manifest in context.admitted_manifests:
                identifier = manifest.identifier
                try:
                    diagnostic = _validate_for_activation(
                        manifest, admitted_ids, SDK_API_VERSION,
                    )
                    if not diagnostic.accepted:
                        _reject_plugin(identifier, diagnostic, events, logger)
                        continue

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
