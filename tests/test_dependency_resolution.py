"""Tests for Dependency Resolution Integration (WP-06 / ADR-007).

SP-05 test suite covering AC-5:
- Dependency graph constructed from manifest dependencies
- Topological sort determines activation order
- Cyclic dependencies detected and rejected
- Version constraints checked
- Missing required dependencies cause rejection
"""

from __future__ import annotations

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
from plugins.loader import PluginManifest

from app.bootstrap import (
    BootstrapContext,
    PluginActivationStage,
    PluginDiscoveryStage,
    PluginRuntimePool,
    PluginSecurityStage,
)
from app.security.plugin_security import PluginSecurity


class _TestBase(unittest.TestCase):
    """Shared helpers for dependency resolution tests."""

    def _make_manifest(
        self,
        identifier: str,
        *,
        version: Version = Version(1, 0, 0),
        dependencies: tuple[dict[str, str], ...] = (),
    ) -> PluginManifest:
        return PluginManifest(
            identifier=identifier,
            version=version,
            required_application_version=Version(0, 3, 0),
            dependencies=dependencies,
        )

    def _make_context(
        self,
        manifests: tuple[PluginManifest, ...] = (),
    ) -> BootstrapContext:
        logger = logging.getLogger("test.dependency_resolution")
        events = EventBus(logger=logger)
        registry = ServiceRegistry()
        context = BootstrapContext(root=Path("."))
        context.logger = logger
        context.events = events
        context.registry = registry
        context.manifests = manifests
        return context

    def _run_security_stage(
        self,
        context: BootstrapContext,
    ) -> tuple[PluginManifest, ...]:
        stage = PluginSecurityStage()
        stage.execute(context)
        return context.admitted_manifests


class TestDependencyGraphOrdering(_TestBase):
    """AC-5: Topological sort determines activation order."""

    def test_dependency_graph_ordering(self) -> None:
        """A depends on B, B depends on C → activation order C, B, A."""
        manifest_c = self._make_manifest("dep_c")
        manifest_b = self._make_manifest(
            "dep_b",
            dependencies=({"id": "dep_c", "version": ">=1.0.0"},),
        )
        manifest_a = self._make_manifest(
            "dep_a",
            dependencies=({"id": "dep_b", "version": ">=1.0.0"},),
        )
        context = self._make_context((manifest_a, manifest_b, manifest_c))

        admitted = self._run_security_stage(context)

        self.assertEqual(len(admitted), 3)
        ids = [m.identifier for m in admitted]
        self.assertLess(ids.index("dep_c"), ids.index("dep_b"))
        self.assertLess(ids.index("dep_b"), ids.index("dep_a"))

    def test_dependency_ordering_no_deps(self) -> None:
        """Plugins without dependencies are all admitted in deterministic order."""
        manifest_b = self._make_manifest("beta")
        manifest_a = self._make_manifest("alpha")
        context = self._make_context((manifest_b, manifest_a))

        admitted = self._run_security_stage(context)

        self.assertEqual(len(admitted), 2)
        ids = [m.identifier for m in admitted]
        self.assertEqual(ids, sorted(ids))

    def test_dependency_ordering_diamond(self) -> None:
        """Diamond: D depends on B and C, both depend on A → A first, D last."""
        manifest_a = self._make_manifest("dep_a")
        manifest_b = self._make_manifest(
            "dep_b",
            dependencies=({"id": "dep_a", "version": ">=1.0.0"},),
        )
        manifest_c = self._make_manifest(
            "dep_c",
            dependencies=({"id": "dep_a", "version": ">=1.0.0"},),
        )
        manifest_d = self._make_manifest(
            "dep_d",
            dependencies=(
                {"id": "dep_b", "version": ">=1.0.0"},
                {"id": "dep_c", "version": ">=1.0.0"},
            ),
        )
        context = self._make_context(
            (manifest_d, manifest_c, manifest_b, manifest_a),
        )

        admitted = self._run_security_stage(context)

        self.assertEqual(len(admitted), 4)
        ids = [m.identifier for m in admitted]
        self.assertLess(ids.index("dep_a"), ids.index("dep_b"))
        self.assertLess(ids.index("dep_a"), ids.index("dep_c"))
        self.assertLess(ids.index("dep_b"), ids.index("dep_d"))
        self.assertLess(ids.index("dep_c"), ids.index("dep_d"))


class TestDependencyCycleDetection(_TestBase):
    """AC-5: Cyclic dependencies detected and rejected."""

    def test_dependency_cycle_detection(self) -> None:
        """A depends on B, B depends on A → both rejected."""
        manifest_a = self._make_manifest(
            "cycle_a",
            dependencies=({"id": "cycle_b", "version": ">=1.0.0"},),
        )
        manifest_b = self._make_manifest(
            "cycle_b",
            dependencies=({"id": "cycle_a", "version": ">=1.0.0"},),
        )
        context = self._make_context((manifest_a, manifest_b))

        rejected: list[str] = []
        context.events.subscribe(
            "security.plugin.rejected",
            lambda e: rejected.append(e.payload["identifier"]),
        )

        admitted = self._run_security_stage(context)

        self.assertEqual(len(admitted), 0)
        self.assertIn("cycle_a", rejected)
        self.assertIn("cycle_b", rejected)

    def test_dependency_self_dependency(self) -> None:
        """Plugin depending on itself is rejected (degenerate cycle)."""
        manifest = self._make_manifest(
            "self_dep",
            dependencies=({"id": "self_dep", "version": ">=1.0.0"},),
        )
        context = self._make_context((manifest,))

        rejected: list[str] = []
        context.events.subscribe(
            "security.plugin.rejected",
            lambda e: rejected.append(e.payload["identifier"]),
        )

        admitted = self._run_security_stage(context)

        self.assertEqual(len(admitted), 0)
        self.assertIn("self_dep", rejected)

    def test_cycle_does_not_affect_independent_plugins(self) -> None:
        """D7.7: Cycle rejection does not affect independent plugins."""
        manifest_a = self._make_manifest(
            "cycle_x",
            dependencies=({"id": "cycle_y", "version": ">=1.0.0"},),
        )
        manifest_b = self._make_manifest(
            "cycle_y",
            dependencies=({"id": "cycle_x", "version": ">=1.0.0"},),
        )
        manifest_ok = self._make_manifest("independent")
        context = self._make_context((manifest_a, manifest_b, manifest_ok))

        admitted = self._run_security_stage(context)

        self.assertEqual(len(admitted), 1)
        self.assertEqual(admitted[0].identifier, "independent")


class TestDependencyVersionConstraint(_TestBase):
    """AC-5: Version constraints checked; unsatisfied → rejection."""

    def test_dependency_version_constraint(self) -> None:
        """Provider is 1.0.0 but consumer requires >=2.0.0 → consumer rejected."""
        manifest_dep = self._make_manifest("provider", version=Version(1, 0, 0))
        manifest_req = self._make_manifest(
            "consumer",
            dependencies=({"id": "provider", "version": ">=2.0.0"},),
        )
        context = self._make_context((manifest_req, manifest_dep))

        rejected: list[str] = []
        context.events.subscribe(
            "security.plugin.rejected",
            lambda e: rejected.append(e.payload["identifier"]),
        )

        admitted = self._run_security_stage(context)

        admitted_ids = [m.identifier for m in admitted]
        self.assertNotIn("consumer", admitted_ids)
        self.assertIn("provider", admitted_ids)
        self.assertIn("consumer", rejected)

    def test_dependency_version_satisfied(self) -> None:
        """Provider is 2.0.0, consumer requires >=1.0.0 → both admitted."""
        manifest_dep = self._make_manifest("provider", version=Version(2, 0, 0))
        manifest_req = self._make_manifest(
            "consumer",
            dependencies=({"id": "provider", "version": ">=1.0.0"},),
        )
        context = self._make_context((manifest_req, manifest_dep))

        admitted = self._run_security_stage(context)

        self.assertEqual(len(admitted), 2)

    def test_dependency_no_version_constraint(self) -> None:
        """No version constraint → any version satisfies (D3)."""
        manifest_dep = self._make_manifest("provider", version=Version(0, 1, 0))
        manifest_req = self._make_manifest(
            "consumer",
            dependencies=({"id": "provider", "version": ""},),
        )
        context = self._make_context((manifest_req, manifest_dep))

        admitted = self._run_security_stage(context)

        self.assertEqual(len(admitted), 2)


class TestDependencyMissingRequired(_TestBase):
    """AC-5: Missing required dependency → rejection."""

    def test_dependency_missing_required(self) -> None:
        """Dependency on non-existent plugin → plugin rejected."""
        manifest = self._make_manifest(
            "needy",
            dependencies=({"id": "nonexistent", "version": ">=1.0.0"},),
        )
        context = self._make_context((manifest,))

        rejected: list[str] = []
        context.events.subscribe(
            "security.plugin.rejected",
            lambda e: rejected.append(e.payload["identifier"]),
        )

        admitted = self._run_security_stage(context)

        self.assertEqual(len(admitted), 0)
        self.assertIn("needy", rejected)

    def test_dependency_cascade_rejection(self) -> None:
        """D4: A depends on B, B depends on missing C → both A and B rejected."""
        manifest_a = self._make_manifest(
            "chain_a",
            dependencies=({"id": "chain_b", "version": ">=1.0.0"},),
        )
        manifest_b = self._make_manifest(
            "chain_b",
            dependencies=({"id": "missing", "version": ">=1.0.0"},),
        )
        context = self._make_context((manifest_a, manifest_b))

        rejected: list[str] = []
        context.events.subscribe(
            "security.plugin.rejected",
            lambda e: rejected.append(e.payload["identifier"]),
        )

        admitted = self._run_security_stage(context)

        self.assertEqual(len(admitted), 0)
        self.assertIn("chain_b", rejected)
        self.assertIn("chain_a", rejected)


def _snapshot_sys_modules() -> set[str]:
    return set(sys.modules)


def _cleanup_test_modules(snapshot: set[str]) -> None:
    for name in set(sys.modules) - snapshot:
        sys.modules.pop(name, None)


def _create_dep_plugin(
    plugin_dir: Path,
    identifier: str,
    *,
    deps: list[dict[str, str]],
) -> None:
    """Create a plugin package with optional dependencies for testing."""
    pkg = plugin_dir / identifier
    pkg.mkdir(parents=True, exist_ok=True)

    lines = [
        f'id = "{identifier}"',
        'version = "1.0.0"',
        'requires_application = "0.3.0"',
    ]
    if deps:
        lines.append("")
        lines.append("[dependencies]")
        dep_entries = []
        for d in deps:
            dep_entries.append(
                f'{{ id = "{d["id"]}", version = "{d["version"]}" }}'
            )
        lines.append(f"requires = [{', '.join(dep_entries)}]")

    (pkg / "plugin.toml").write_text("\n".join(lines), encoding="utf-8")

    code = f'''\
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
            description="Dependency test plugin",
        )
'''
    (pkg / "__init__.py").write_text(code, encoding="utf-8")


class TestMultiplePluginsDependencyOrder(unittest.TestCase):
    """AC-5 Integration: Multiple plugins activated in dependency order."""

    def setUp(self) -> None:
        self._modules_snapshot = _snapshot_sys_modules()

    def tearDown(self) -> None:
        _cleanup_test_modules(self._modules_snapshot)

    def test_multiple_plugins_dependency_order(self) -> None:
        """Integration: Discovery → Security → Activation respects dependency order."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"

            _create_dep_plugin(plugin_dir, "dep_c", deps=[])
            _create_dep_plugin(
                plugin_dir, "dep_b",
                deps=[{"id": "dep_c", "version": ">=1.0.0"}],
            )
            _create_dep_plugin(
                plugin_dir, "dep_a",
                deps=[{"id": "dep_b", "version": ">=1.0.0"}],
            )

            logger = logging.getLogger("test.dep.integration")
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

            activated_order: list[str] = []
            events.subscribe(
                "application.plugin.activated",
                lambda e: activated_order.append(e.payload["identifier"]),
            )

            PluginDiscoveryStage().execute(context)
            self.assertEqual(len(context.manifests), 3)

            security = PluginSecurity(events, logger=logger)
            security.approve("dep_a")
            security.approve("dep_b")
            security.approve("dep_c")
            registry.register(PluginSecurity, security)
            PluginSecurityStage().execute(context)
            self.assertEqual(len(context.admitted_manifests), 3)

            ids = [m.identifier for m in context.admitted_manifests]
            self.assertLess(ids.index("dep_c"), ids.index("dep_b"))
            self.assertLess(ids.index("dep_b"), ids.index("dep_a"))

            PluginActivationStage().execute(context)
            pool = registry.get(PluginRuntimePool)
            self.assertEqual(len(pool.runtimes), 3)

            self.assertEqual(activated_order, ["dep_c", "dep_b", "dep_a"])


if __name__ == "__main__":
    unittest.main()
