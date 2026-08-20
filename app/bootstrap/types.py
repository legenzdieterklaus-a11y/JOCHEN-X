"""Bootstrap type definitions, protocols, and data structures."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import IntEnum, StrEnum
from pathlib import Path
from types import MappingProxyType
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
    "PIPELINE_ORDER",
    "PIPELINE_STAGE_REFERENCES",
    "PipelineRejection",
    "PipelineStage",
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
    APPLICATION_VERSION_INCOMPATIBLE = "application_version_incompatible"
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


class PipelineStage(StrEnum):
    """Stages of the plugin runtime pipeline, in execution order.

    The five baseline stages carry the invariant pipeline order PL-01..PL-05
    (Bootstrap Baseline 1.0 §5.2, BI-06); the API version gate is the
    additional runtime check executed within the security validation after
    integrity (PL-02) and before permission authorization (PL-03). The order
    itself is never altered by this typing — it only names the stages.
    """

    DISCOVERY = "discovery"
    INTEGRITY = "integrity"
    API_VERSION_GATE = "api_version_gate"
    PERMISSION = "permission"
    DEPENDENCY_RESOLUTION = "dependency_resolution"
    ACTIVATION = "activation"


PIPELINE_ORDER: tuple[PipelineStage, ...] = (
    PipelineStage.DISCOVERY,
    PipelineStage.INTEGRITY,
    PipelineStage.API_VERSION_GATE,
    PipelineStage.PERMISSION,
    PipelineStage.DEPENDENCY_RESOLUTION,
    PipelineStage.ACTIVATION,
)
"""Execution order of the runtime pipeline; PL-01..PL-05 remain invariant."""


PIPELINE_STAGE_REFERENCES: Mapping[PipelineStage, str] = MappingProxyType({
    PipelineStage.DISCOVERY: "PL-01",
    PipelineStage.INTEGRITY: "PL-02",
    PipelineStage.API_VERSION_GATE: "PL-02..PL-03",
    PipelineStage.PERMISSION: "PL-03",
    PipelineStage.DEPENDENCY_RESOLUTION: "PL-04",
    PipelineStage.ACTIVATION: "PL-05",
})
"""Read-only reference of each stage to the pipeline order per Baseline §5.2."""


@dataclass(frozen=True, slots=True)
class PipelineRejection:
    """Structured plugin rejection result of the runtime pipeline (FR-006).

    Carries the triggering pipeline stage (AC-006.1) and the violated
    criterion together with its reference to the invariant pipeline order
    PL-01..PL-05 per Bootstrap Baseline 1.0 §5.2 (AC-006.2).
    """

    identifier: str
    stage: PipelineStage
    criterion: str
    pipeline_reference: str
    rejection_code: RejectionCode | None = None
    reason: str = ""


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
    pipeline_rejections: list[PipelineRejection] = field(default_factory=list)


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
