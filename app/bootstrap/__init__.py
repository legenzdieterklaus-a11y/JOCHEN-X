"""Deterministic, phase-grouped bootstrap of the application foundation.

:class:`BootstrapManager` executes an ordered set of isolated
:class:`BootstrapStage` objects. Stages are grouped by :class:`StartupPhase` so
the startup sequence can advance the application state machine between phases
while every stage remains independently testable. Each stage populates a mutable
:class:`BootstrapContext`; the manager then assembles an immutable
:class:`app.context.ApplicationContext`.
"""

from __future__ import annotations

from app.bootstrap.manager import BootstrapManager, default_stages
from app.bootstrap.stages_init import (
    ConfigurationStage,
    DatabaseStage,
    EnvironmentStage,
    LoggingStage,
    RegistryStage,
    SchedulerStage,
    ThemeStage,
)
from app.bootstrap.stages_late import (
    DependencyInjectionStage,
    DeveloperToolsStage,
    ResourceStage,
)
from app.bootstrap.stages_plugin import (
    PluginActivationStage,
    PluginDiscoveryStage,
    PluginRuntimePool,
    PluginSecurityStage,
    _validate_for_activation,
)
from app.bootstrap.types import (
    BootstrapContext,
    BootstrapError,
    BootstrapStage,
    RejectionCode,
    StartupPhase,
    ValidationDiagnostic,
    _require,
)

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
