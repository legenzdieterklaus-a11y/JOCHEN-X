"""Bootstrap type definitions, protocols, and data structures."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import IntEnum, StrEnum
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, TypeVar

if TYPE_CHECKING:
    from sdk.plugin import PluginRuntime

from config.settings import ApplicationSettings, ConfigurationService
from core.environment import Environment
from core.events import EventBus
from core.exceptions import JochenXError
from core.observability import ActivationFailure, Metrics
from core.registry import ServiceRegistry
from core.scheduler import TaskScheduler
from core.version import VersionManager
from database.sqlite import ConnectionManager, SettingsRepository
from plugins.loader import PluginLoader, PluginManifest
from styles.theme import ThemeEngine

from app.di import DisposableRegistry, ServiceProvider
from app.resources import ResourceManager

__all__ = [
    "BootstrapContext",
    "BootstrapError",
    "BootstrapStage",
    "RejectionCode",
    "StartupPhase",
    "ValidationDiagnostic",
]

T = TypeVar("T")


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
    metrics: Metrics | None = None
    activation_failures: list[ActivationFailure] = field(default_factory=list)


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
