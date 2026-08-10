"""Bootstrap orchestration: manager and default stage sequence."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

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
    PluginSecurityStage,
)
from app.bootstrap.types import (
    BootstrapContext,
    BootstrapError,
    BootstrapStage,
    StartupPhase,
    _require,
)
from app.context import ApplicationContext, RuntimeState
from app.state_machine import ApplicationStateMachine

__all__ = [
    "BootstrapManager",
    "default_stages",
]


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
