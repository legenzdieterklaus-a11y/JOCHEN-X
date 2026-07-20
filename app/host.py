"""Application host: the sole composition root and lifecycle owner."""

import logging
from pathlib import Path
import sys
from PySide6.QtWidgets import QApplication

from ai.gateway import ProviderRegistry, RoutingEngine
from config.settings import ConfigurationService
from core.environment import Environment
from core.events import EventBus
from core.lifecycle import LifecycleManager
from core.logging import configure_logging
from core.observability import Metrics, Tracer
from core.performance import PerformanceController
from core.registry import ServiceRegistry
from core.scheduler import TaskScheduler
from core.version import Version, VersionManager
from database.sqlite import ConnectionManager, MigrationManager, SettingsRepository
from plugins.loader import PluginLoader
from services.observability import PerformanceMonitor
from services.security import AuditHooks, PermissionLayer, SecretManager, SecurityPolicy
from styles.theme import ThemeEngine
from ui.foundation_window import FoundationWindow


class ApplicationHost:
    """Composes all foundation services and owns startup/shutdown ordering."""
    def __init__(self, root: Path) -> None:
        self._root = root
        self.services = ServiceRegistry()
        self._app: QApplication | None = None
        self._window: FoundationWindow | None = None

    @classmethod
    def create_default(cls) -> "ApplicationHost":
        """Create a host rooted at the project directory."""
        return cls(Path(__file__).resolve().parents[1])

    def bootstrap(self) -> None:
        """Initialize the foundation in dependency order, exactly once."""
        environment = Environment.from_root(self._root)
        config = ConfigurationService(self._root / "config" / "default.toml", self._root / "config" / "profile.toml")
        settings = config.load()
        logger = configure_logging(environment.root / "logs", settings.log_level)
        logger.info("bootstrap.started")
        connections = ConnectionManager(environment.root / settings.database_path)
        MigrationManager(connections).migrate()
        versions = VersionManager(Version.parse(settings.version))
        providers = ProviderRegistry()
        self.services.register(Environment, environment)
        self.services.register(ConfigurationService, config)
        self.services.register(logging.Logger, logger)
        self.services.register(ConnectionManager, connections)
        self.services.register(SettingsRepository, SettingsRepository(connections))
        self.services.register(ThemeEngine, ThemeEngine())
        self.services.register(VersionManager, versions)
        self.services.register(ProviderRegistry, providers)
        self.services.register(RoutingEngine, RoutingEngine(providers))
        self.services.register(PluginLoader, PluginLoader(environment.root / settings.plugin_directory, versions))
        self.services.register(PerformanceMonitor, PerformanceMonitor())
        policy = SecurityPolicy(PermissionLayer())
        self.services.register(SecurityPolicy, policy)
        self.services.register(SecretManager, SecretManager())
        self.services.register(AuditHooks, AuditHooks(logger))
        self.services.register(EventBus, EventBus(logger=logger))
        self.services.register(LifecycleManager, LifecycleManager())
        self.services.register(PerformanceController, PerformanceController())
        self.services.register(Metrics, Metrics())
        self.services.register(Tracer, Tracer())
        self.services.register(TaskScheduler, TaskScheduler())
        if settings.developer_enabled:
            from developer.platform import DeveloperPlatform
            self.services.register(DeveloperPlatform, DeveloperPlatform(
                enabled=True, events=self.services.get(EventBus), services=self.services,
                plugins=self.services.get(PluginLoader), log_file=environment.root / "logs" / "jochen_x.log"))
        logger.info("bootstrap.completed")

    def run(self) -> int:
        """Bootstrap, show the shell, and run the Qt event loop."""
        self.bootstrap()
        settings = self.services.get(ConfigurationService).load()
        self._app = QApplication.instance() or QApplication(sys.argv)
        engine = self.services.get(ThemeEngine)
        self._app.setStyleSheet(engine.stylesheet(engine.select(settings.theme_mode)))
        developer_center = None
        try:
            from developer.platform import DeveloperPlatform
            platform = self.services.get(DeveloperPlatform)
            from ui.developer_center import DeveloperCenter
            environment = self.services.get(Environment)
            summary = platform.summary(version=settings.version, build="local", python=environment.python_version,
                                       os_name=environment.os_name, modules=("core", "services"),
                                       database_status="ready", theme=str(settings.theme_mode), profile="default")
            developer_center = DeveloperCenter(f"{summary.version} · {summary.os_name}")
        except LookupError:
            pass
        self._window = FoundationWindow(settings.name, settings.version, developer_center)
        self._window.show()
        exit_code = self._app.exec()
        self.shutdown()
        return exit_code

    def shutdown(self) -> None:
        """Record orderly shutdown; services own no autonomous worker threads."""
        try:
            self.services.get(logging.Logger).info("shutdown.completed")
        except LookupError:
            return
