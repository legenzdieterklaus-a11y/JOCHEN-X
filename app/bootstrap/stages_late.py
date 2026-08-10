"""Late-phase bootstrap stages (LOAD_RESOURCES, FINALIZE)."""

from __future__ import annotations

from dataclasses import dataclass

from app.bootstrap.constants import _LOGS_DIRECTORY, _LOG_FILE_NAME
from app.bootstrap.types import (
    BootstrapContext,
    StartupPhase,
    _require,
)
from app.di import ServiceProvider
from app.resources import ResourceManager

__all__ = [
    "DependencyInjectionStage",
    "DeveloperToolsStage",
    "ResourceStage",
]


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
