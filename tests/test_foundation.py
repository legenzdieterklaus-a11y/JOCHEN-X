"""Integration-oriented tests for the implemented foundation boundaries."""

from pathlib import Path
import tempfile
import unittest

from ai.gateway import Capability, ModelDescriptor, ProviderDescriptor, ProviderRegistry, RoutingEngine
from app.host import ApplicationHost
from config.settings import ConfigurationService, ThemeMode
from core.logging import configure_logging
from core.version import Version, VersionManager
from database.sqlite import ConnectionManager, MigrationManager, SettingsRepository
from plugins.loader import PluginLoader
from styles.theme import DARK, ThemeEngine


class FoundationTests(unittest.TestCase):
    """Verify each foundation subsystem without starting a GUI event loop."""
    def test_bootstrap_composes_services(self) -> None:
        host = ApplicationHost.create_default()
        host.bootstrap()
        self.assertGreaterEqual(sum(1 for _ in host.services), 12)
        host.shutdown()

    def test_config_load_and_profile_round_trip(self) -> None:
        root = Path(__file__).parents[1]
        with tempfile.TemporaryDirectory() as directory:
            profile = Path(directory) / "profile.toml"
            service = ConfigurationService(root / "config" / "default.toml", profile)
            settings = service.load()
            self.assertIs(settings.theme_mode, ThemeMode.SYSTEM)
            service.save_profile(settings)
            self.assertEqual(service.load(), settings)

    def test_logger_writes_rotating_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            logger = configure_logging(Path(directory), "INFO")
            logger.info("test.event", extra={"context": {"key": "value"}})
            self.assertIn("test.event", (Path(directory) / "jochen_x.log").read_text(encoding="utf-8"))
            logger.handlers.clear()

    def test_database_migration_and_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manager = ConnectionManager(Path(directory) / "foundation.sqlite3")
            MigrationManager(manager).migrate()
            repository = SettingsRepository(manager)
            repository.set("theme", "dark")
            self.assertEqual(repository.get("theme"), "dark")

    def test_theme_engine(self) -> None:
        engine = ThemeEngine()
        self.assertEqual(engine.select(ThemeMode.DARK), DARK)
        self.assertIn(DARK.background, engine.stylesheet(DARK))

    def test_ai_registry_routes_capability(self) -> None:
        registry = ProviderRegistry()
        model = ModelDescriptor("local", "model", frozenset({Capability.TEXT}))
        registry.register(ProviderDescriptor("local", "Local", (model,)))
        self.assertEqual(RoutingEngine(registry).candidates(Capability.TEXT), (model,))

    def test_plugin_loader_discovers_compatible_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            plugin = Path(directory) / "sample"
            plugin.mkdir()
            (plugin / "plugin.toml").write_text('id = "sample"\nversion = "0.1.0"\nrequires_application = "0.1.0"\n', encoding="utf-8")
            loader = PluginLoader(Path(directory), VersionManager(Version.parse("0.1.0")))
            self.assertEqual(loader.discover()[0].identifier, "sample")


if __name__ == "__main__":
    unittest.main()
