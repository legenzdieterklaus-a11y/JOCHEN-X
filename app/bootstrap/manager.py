"""Bootstrap orchestration: manager and default stage sequence."""

from __future__ import annotations

import logging
import sys
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
    # Single-element holder for the context begun but not yet completed, so a
    # failed startup has a defined cleanup target (FR-009 / AC-009.2). The
    # list is mutated, never reassigned, keeping the dataclass frozen.
    _pending: list[BootstrapContext] = field(
        default_factory=list, init=False, repr=False, compare=False
    )

    def begin(self, root: Path) -> BootstrapContext:
        """Create a fresh bootstrap context rooted at ``root``."""
        context = BootstrapContext(root=root)
        self._pending.clear()
        self._pending.append(context)
        return context

    def pending_context(self) -> BootstrapContext | None:
        """Return the context begun but not yet completed, if any."""
        return self._pending[-1] if self._pending else None

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

    def abort(self, context: BootstrapContext) -> None:
        """Release every partially initialised component of a failed bootstrap.

        Defined cleanup path for AC-009.2: after a failed stage run all
        already-initialised components are returned to a consistent state.
        Teardown mirrors the regular shutdown order — plugin runtimes in
        reverse activation order first, then imported plugin modules, then
        owned resources in reverse registration order. Every step is guarded;
        aborting must never raise so the original stage error stays visible.
        """
        logger = context.logger or logging.getLogger("jochen_x.bootstrap")
        for runtime in reversed(context.plugin_runtimes):
            try:
                runtime.shutdown()
            except Exception as error:
                logger.error(
                    "bootstrap.abort.plugin_shutdown_failed",
                    extra={"context": {"error": str(error)}},
                )
        context.plugin_runtimes = ()
        identifiers = {manifest.identifier for manifest in context.manifests}
        identifiers.update(manifest.identifier for manifest in context.admitted_manifests)
        if identifiers:
            for name in list(sys.modules):
                if name.partition(".")[0] in identifiers:
                    sys.modules.pop(name, None)
        if context.disposables is not None:
            context.disposables.dispose_all()
        self._pending.clear()
        logger.info("bootstrap.aborted", extra={"context": {"root": str(context.root)}})

    def build_context(
        self, context: BootstrapContext, state_machine: ApplicationStateMachine
    ) -> ApplicationContext:
        """Assemble the immutable application context from a populated bootstrap context."""
        application_context = ApplicationContext(
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
        self._pending.clear()
        return application_context
