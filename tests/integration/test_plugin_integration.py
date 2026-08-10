"""Bootstrap pipeline integration tests (Engineering Specification §9).

Tests exercise the full plugin pipeline at bootstrap level:
Discovery → Security → Activation → Shutdown.
No Qt event loop required.
"""

from __future__ import annotations

import gc
import logging
import sys
import tempfile
import unittest
from pathlib import Path

from core.events import EventBus
from core.registry import ServiceRegistry
from core.version import Version, VersionManager
from config.settings import ApplicationSettings
from core.environment import Environment
from plugins.loader import PluginCatalog, PluginLoader, PluginManifest

from app.bootstrap import (
    BootstrapContext,
    PluginActivationStage,
    PluginDiscoveryStage,
    PluginRuntimePool,
    PluginSecurityStage,
    StartupPhase,
    default_stages,
)
from app.events import ApplicationEventName
from app.security.plugin_security import PluginSecurity


_PLUGIN_TOML_TEMPLATE = """\
id = "{identifier}"
version = "1.0.0"
requires_application = "0.3.0"
"""

_PLUGIN_CODE_TEMPLATE = '''\
from sdk.plugin import Plugin
from sdk.manifest import PluginMetadata

class TestPlugin(Plugin):
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            identifier="{identifier}",
            name="{identifier}",
            version="1.0.0",
            api_version="1.0.0",
            author="Test",
            description="Integration test plugin",
        )
'''

_BROKEN_PLUGIN_CODE = '''\
raise ImportError("deliberate import failure for testing")
'''


def _snapshot_sys_modules() -> set[str]:
    return set(sys.modules)


def _cleanup_test_modules(snapshot: set[str]) -> None:
    for name in set(sys.modules) - snapshot:
        sys.modules.pop(name, None)


def _create_plugin_package(
    plugin_dir: Path,
    identifier: str,
    *,
    broken: bool = False,
) -> None:
    pkg = plugin_dir / identifier
    pkg.mkdir(parents=True, exist_ok=True)
    (pkg / "plugin.toml").write_text(
        _PLUGIN_TOML_TEMPLATE.format(identifier=identifier),
        encoding="utf-8",
    )
    code = _BROKEN_PLUGIN_CODE if broken else _PLUGIN_CODE_TEMPLATE.format(identifier=identifier)
    (pkg / "__init__.py").write_text(code, encoding="utf-8")


def _make_context(root: Path) -> BootstrapContext:
    logger = logging.getLogger("test.integration.pipeline")
    events = EventBus(logger=logger)
    registry = ServiceRegistry()
    versions = VersionManager(Version.parse("0.8.0"))
    context = BootstrapContext(root=root)
    context.logger = logger
    context.events = events
    context.registry = registry
    context.versions = versions
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


class TestFullPluginPipeline(unittest.TestCase):
    """Discovery → Security → Activation → Shutdown end-to-end."""

    def setUp(self) -> None:
        self._modules_snapshot = _snapshot_sys_modules()

    def tearDown(self) -> None:
        _cleanup_test_modules(self._modules_snapshot)

    def test_full_plugin_pipeline(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            _create_plugin_package(plugin_dir, "integ-pipeline-plugin")
            context = _make_context(root)

            event_log: list[str] = []
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_LOADING),
                lambda e: event_log.append(f"loading:{e.payload['identifier']}"),
            )
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_LOADED),
                lambda e: event_log.append(f"loaded:{e.payload['identifier']}"),
            )
            context.events.subscribe(
                "security.plugin.verified",
                lambda e: event_log.append(f"verified:{e.payload['identifier']}"),
            )
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_ACTIVATING),
                lambda e: event_log.append(f"activating:{e.payload['identifier']}"),
            )
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_ACTIVATED),
                lambda e: event_log.append(f"activated:{e.payload['identifier']}"),
            )

            # Phase 1: Discovery
            discovery = PluginDiscoveryStage()
            discovery.execute(context)
            self.assertEqual(len(context.manifests), 1)
            self.assertEqual(context.manifests[0].identifier, "integ-pipeline-plugin")

            # Phase 2: Security
            security = PluginSecurity(context.events, logger=context.logger)
            security.approve("integ-pipeline-plugin")
            context.registry.register(PluginSecurity, security)
            security_stage = PluginSecurityStage()
            security_stage.execute(context)
            self.assertEqual(len(context.admitted_manifests), 1)

            # Phase 3: Activation
            activation = PluginActivationStage()
            activation.execute(context)
            pool = context.registry.get(PluginRuntimePool)
            self.assertEqual(len(pool.runtimes), 1)

            from sdk.plugin import PluginLifecycleState

            self.assertIs(pool.runtimes[0].state, PluginLifecycleState.STARTED)

            # Phase 4: Shutdown (reverse order)
            for runtime in reversed(pool.runtimes):
                runtime.shutdown()
            self.assertIs(pool.runtimes[0].state, PluginLifecycleState.STOPPED)

            # Verify event sequence
            self.assertEqual(event_log, [
                "loading:integ-pipeline-plugin",
                "loaded:integ-pipeline-plugin",
                "verified:integ-pipeline-plugin",
                "activating:integ-pipeline-plugin",
                "activated:integ-pipeline-plugin",
            ])


class TestDefaultStagesOrdering(unittest.TestCase):
    """Verifies correct stage ordering in default_stages()."""

    def test_default_stages_ordering(self) -> None:
        stages = default_stages()
        names = [s.name for s in stages]
        phases = [s.phase for s in stages]

        # Phases must be monotonically non-decreasing
        for i in range(len(phases) - 1):
            self.assertLessEqual(
                phases[i],
                phases[i + 1],
                f"Stage {names[i + 1]} (phase {phases[i + 1].name}) "
                f"appears after {names[i]} (phase {phases[i].name})",
            )

        # All four phases must be represented
        phase_set = set(phases)
        for phase in StartupPhase:
            self.assertIn(phase, phase_set, f"Phase {phase.name} missing from default stages")

        # Critical ordering constraints within phases
        self.assertLess(names.index("plugins"), names.index("plugin_security"))
        self.assertLess(names.index("plugin_security"), names.index("plugin_activation"))
        self.assertLess(names.index("plugin_activation"), names.index("dependency_injection"))


class TestGracefulDegradation(unittest.TestCase):
    """One faulty plugin must not prevent activation of a good plugin."""

    def setUp(self) -> None:
        self._modules_snapshot = _snapshot_sys_modules()

    def tearDown(self) -> None:
        _cleanup_test_modules(self._modules_snapshot)

    def test_graceful_degradation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            _create_plugin_package(plugin_dir, "integ-good-plugin")
            _create_plugin_package(plugin_dir, "integ-broken-plugin", broken=True)
            context = _make_context(root)

            failed_ids: list[str] = []
            activated_ids: list[str] = []
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_FAILED),
                lambda e: failed_ids.append(e.payload["identifier"]),
            )
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_ACTIVATED),
                lambda e: activated_ids.append(e.payload["identifier"]),
            )

            # Discovery
            discovery = PluginDiscoveryStage()
            discovery.execute(context)
            self.assertEqual(len(context.manifests), 2)

            # Security — approve both
            security = PluginSecurity(context.events, logger=context.logger)
            security.approve("integ-good-plugin")
            security.approve("integ-broken-plugin")
            context.registry.register(PluginSecurity, security)
            security_stage = PluginSecurityStage()
            security_stage.execute(context)
            self.assertEqual(len(context.admitted_manifests), 2)

            # Activation — broken plugin fails, good plugin succeeds
            activation = PluginActivationStage()
            activation.execute(context)
            pool = context.registry.get(PluginRuntimePool)

            self.assertEqual(len(pool.runtimes), 1)
            self.assertIn("integ-broken-plugin", failed_ids)
            self.assertIn("integ-good-plugin", activated_ids)


if __name__ == "__main__":
    unittest.main()
