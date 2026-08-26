"""Golden Reference Plugin integration tests (WP-08 / AC-7).

Validates the reference plugin through the full bootstrap pipeline:
Discovery -> Security -> Activation -> Runtime -> Shutdown.
"""

from __future__ import annotations

import logging
import shutil
import tomllib
import sys
import tempfile
import unittest
from pathlib import Path

from core.events import EventBus
from core.observability import Metrics
from core.registry import ServiceRegistry
from core.version import Version, VersionManager
from config.settings import ApplicationSettings
from core.environment import Environment
from plugins.loader import _parse_manifest
from sdk.plugin import PluginLifecycleState

from app.bootstrap import (
    BootstrapContext,
    PluginActivationStage,
    PluginDiscoveryStage,
    PluginRuntimePool,
    PluginSecurityStage,
)
from app.events import ApplicationEventName
from app.security.plugin_security import PermissionPolicy, PluginSecurity

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_REFERENCE_DIR = _PROJECT_ROOT / "plugins" / "reference"


def _snapshot_sys_modules() -> set[str]:
    return set(sys.modules)


def _cleanup_test_modules(snapshot: set[str]) -> None:
    for name in set(sys.modules) - snapshot:
        sys.modules.pop(name, None)


def _make_context(root: Path) -> BootstrapContext:
    logger = logging.getLogger("test.golden_reference")
    events = EventBus(logger=logger)
    registry = ServiceRegistry()
    versions = VersionManager(Version.parse("0.8.0"))
    metrics = Metrics()
    context = BootstrapContext(root=root)
    context.logger = logger
    context.events = events
    context.registry = registry
    context.versions = versions
    context.metrics = metrics
    context.environment = Environment.from_root(root)
    context.settings = ApplicationSettings(
        name="Test",
        version="0.8.0",
        log_level="INFO",
        theme_mode="dark",
        developer_enabled=False,
        database_path="data/test.sqlite3",
        plugin_directory="plugins",
    )
    return context


class TestGoldenReferencePlugin(unittest.TestCase):
    """Full lifecycle validation of the Golden Reference Plugin (AC-7)."""

    def setUp(self) -> None:
        self._modules_snapshot = _snapshot_sys_modules()

    def tearDown(self) -> None:
        _cleanup_test_modules(self._modules_snapshot)

    def test_golden_reference_full_lifecycle(self) -> None:
        """Discovery -> Security -> Activation -> Runtime -> Shutdown."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            shutil.copytree(
                _REFERENCE_DIR, plugin_dir / "reference",
                ignore=shutil.ignore_patterns("__pycache__"),
            )
            context = _make_context(root)

            policy = PermissionPolicy(
                wildcard_grants=frozenset({"events.publish", "events.subscribe"}),
            )
            security = PluginSecurity(
                context.events, logger=context.logger, permission_policy=policy,
            )
            security.approve("reference")
            context.registry.register(PluginSecurity, security)

            event_log: list[str] = []
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_ACTIVATING),
                lambda e: event_log.append(f"activating:{e.payload['identifier']}"),
            )
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_ACTIVATED),
                lambda e: event_log.append(f"activated:{e.payload['identifier']}"),
            )

            # Discovery
            PluginDiscoveryStage().execute(context)
            self.assertEqual(len(context.manifests), 1)
            self.assertEqual(context.manifests[0].identifier, "reference")

            # Security
            PluginSecurityStage().execute(context)
            self.assertEqual(len(context.admitted_manifests), 1)

            # Activation
            PluginActivationStage().execute(context)
            pool = context.registry.get(PluginRuntimePool)
            self.assertEqual(len(pool.runtimes), 1)

            self.assertIs(pool.runtimes[0].state, PluginLifecycleState.STARTED)

            # Shutdown
            for runtime in reversed(pool.runtimes):
                runtime.shutdown()
            self.assertIs(pool.runtimes[0].state, PluginLifecycleState.STOPPED)

            # Event sequence
            self.assertIn("activating:reference", event_log)
            self.assertIn("activated:reference", event_log)

            # Activation duration metric captured
            snapshot = context.metrics.snapshot()
            self.assertIn("plugin.activation.duration_ms.reference", snapshot)
            self.assertGreater(snapshot["plugin.activation.duration_ms.reference"], 0)

    def test_golden_reference_manifest_v2(self) -> None:
        """Manifest v2 is fully parsed with all fields present."""
        manifest_path = _REFERENCE_DIR / "plugin.toml"
        with manifest_path.open("rb") as f:
            data = tomllib.load(f)

        plugin = data["plugin"]
        for field_name in ("id", "version", "requires_application", "api_version",
                           "category", "entry_point"):
            self.assertIn(field_name, plugin, f"Missing v2 field: {field_name}")

        self.assertIn("metadata", plugin)
        self.assertIn("permissions", plugin)
        self.assertIn("dependencies", plugin)

        metadata = plugin["metadata"]
        self.assertIn("display_name", metadata)
        self.assertIn("author", metadata)
        self.assertIn("description", metadata)

        manifest = _parse_manifest(data)
        self.assertEqual(manifest.identifier, "reference")
        self.assertIsNotNone(manifest.api_version)
        self.assertEqual(manifest.category, "developer")
        self.assertEqual(manifest.entry_point, "reference")
        self.assertTrue(len(manifest.permissions) > 0)

    def test_golden_reference_permissions(self) -> None:
        """Permission declarations are correctly validated by the security pipeline."""
        manifest_path = _REFERENCE_DIR / "plugin.toml"
        with manifest_path.open("rb") as f:
            data = tomllib.load(f)

        manifest = _parse_manifest(data)
        self.assertIn("events.publish", manifest.permissions)
        self.assertIn("events.subscribe", manifest.permissions)

        events = EventBus(logger=logging.getLogger("test"))

        policy = PermissionPolicy(
            wildcard_grants=frozenset({"events.publish", "events.subscribe"}),
        )
        security = PluginSecurity(events, permission_policy=policy)
        result = security.validate_permissions(manifest)
        self.assertTrue(result.admitted)
        self.assertEqual(result.denied, frozenset())

        deny_security = PluginSecurity(events, permission_policy=PermissionPolicy())
        deny_result = deny_security.validate_permissions(manifest)
        self.assertFalse(deny_result.admitted)
        self.assertTrue(len(deny_result.denied) > 0)


if __name__ == "__main__":
    unittest.main()
