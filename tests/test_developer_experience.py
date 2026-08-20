"""WP-003 Developer Experience tests (FR-005, FR-006).

Covers AC-005.1 (all author guidelines consolidated at a single place),
AC-005.2 (documentation consistent with the implemented ``sdk/`` contracts),
AC-006.1 (rejection results carry the triggering pipeline stage) and
AC-006.2 (rejection results carry the violated criterion with its reference
to the invariant pipeline order PL-01..PL-05 per Bootstrap Baseline 1.0
§5.2).
"""

from __future__ import annotations

import logging
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from core.events import EventBus
from core.registry import ServiceRegistry
from core.version import Version, VersionManager
from plugins.loader import PluginLoader, PluginManifest

from app.bootstrap.stages_plugin import (
    PluginDiscoveryStage,
    PluginSecurityStage,
    _reject_plugin,
    _validate_for_activation,
)
from app.bootstrap.types import (
    PIPELINE_ORDER,
    PIPELINE_STAGE_REFERENCES,
    BootstrapContext,
    PipelineStage,
    RejectionCode,
)
from app.security.plugin_security import PluginSecurity

from sdk.manifest import PluginPermission
from sdk.plugin import PluginLifecycleState

_DOCS_ROOT = Path(__file__).resolve().parents[1]
_SDK_DOC = _DOCS_ROOT / "docs" / "sdk.md"
_EXTENSIONS_DOC = _DOCS_ROOT / "docs" / "extensions.md"
_CONTRIBUTING_DOC = _DOCS_ROOT / "CONTRIBUTING.md"

_GUIDELINES_HEADING = "## 15. Plugin Author Guidelines"


def _guidelines_chapter() -> str:
    text = _SDK_DOC.read_text(encoding="utf-8")
    start = text.index(_GUIDELINES_HEADING)
    return text[start:]


def _manifest(
    identifier: str = "com.example.plugin",
    *,
    api_version: str | None = None,
    permissions: tuple[str, ...] = (),
    dependencies: tuple[dict[str, str], ...] = (),
) -> PluginManifest:
    return PluginManifest(
        identifier=identifier,
        version=Version.parse("1.0.0"),
        required_application_version=Version.parse("0.8.0"),
        api_version=Version.parse(api_version) if api_version else None,
        permissions=permissions,
        dependencies=dependencies,
    )


def _context(root: Path | None = None) -> BootstrapContext:
    root = root or Path(tempfile.mkdtemp(prefix="wp003-test-"))
    context = BootstrapContext(root=root)
    context.environment = SimpleNamespace(root=root)
    context.settings = SimpleNamespace(plugin_directory="plugins")
    context.versions = VersionManager(Version.parse("0.9.0"))
    context.registry = ServiceRegistry()
    context.events = EventBus()
    context.logger = logging.getLogger("test.wp003")
    return context


class AuthorGuidelinesSinglePlaceTests(unittest.TestCase):
    def test_guidelines_chapter_exists_as_single_place(self) -> None:
        chapter = _guidelines_chapter()
        self.assertIn("single authoritative place", chapter)
        self.assertIn("### 15.1 Manifest Schema", chapter)
        self.assertIn("### 15.2 Lifecycle Contract", chapter)
        self.assertIn("### 15.3 Permission Model", chapter)

    def test_other_documents_reference_instead_of_redefining(self) -> None:
        self.assertIn(
            "sdk.md#15-plugin-author-guidelines",
            _EXTENSIONS_DOC.read_text(encoding="utf-8"),
        )
        self.assertIn(
            "sdk.md#15-plugin-author-guidelines",
            _CONTRIBUTING_DOC.read_text(encoding="utf-8"),
        )


class AuthorGuidelinesConsistencyTests(unittest.TestCase):
    def test_every_permission_value_is_documented(self) -> None:
        chapter = _guidelines_chapter()
        for permission in PluginPermission:
            with self.subTest(permission=permission.name):
                self.assertIn(f"`{permission.value}`", chapter)
                self.assertIn(f"`{permission.name}`", chapter)

    def test_every_lifecycle_state_is_documented(self) -> None:
        chapter = _guidelines_chapter()
        for state in PluginLifecycleState:
            with self.subTest(state=state.name):
                self.assertIn(state.value, chapter)

    def test_manifest_schema_keys_match_loader_contract(self) -> None:
        chapter = _guidelines_chapter()
        for key in (
            "id",
            "version",
            "requires_application",
            "api_version",
            "category",
            "entry_point",
        ):
            with self.subTest(key=key):
                self.assertIn(f"`[plugin] {key}`", chapter)
        self.assertIn("`[plugin.metadata]`", chapter)
        self.assertIn("`[plugin.permissions] capabilities`", chapter)
        self.assertIn("`[plugin.dependencies] requires`", chapter)


class PipelineOrderContractTests(unittest.TestCase):
    def test_every_stage_has_a_pipeline_reference(self) -> None:
        self.assertEqual(set(PIPELINE_STAGE_REFERENCES), set(PipelineStage))
        self.assertEqual(set(PIPELINE_ORDER), set(PipelineStage))

    def test_baseline_stages_reference_pl_01_to_pl_05_in_order(self) -> None:
        self.assertEqual(PIPELINE_STAGE_REFERENCES[PipelineStage.DISCOVERY], "PL-01")
        self.assertEqual(PIPELINE_STAGE_REFERENCES[PipelineStage.INTEGRITY], "PL-02")
        self.assertEqual(
            PIPELINE_STAGE_REFERENCES[PipelineStage.API_VERSION_GATE], "PL-02..PL-03"
        )
        self.assertEqual(PIPELINE_STAGE_REFERENCES[PipelineStage.PERMISSION], "PL-03")
        self.assertEqual(
            PIPELINE_STAGE_REFERENCES[PipelineStage.DEPENDENCY_RESOLUTION], "PL-04"
        )
        self.assertEqual(PIPELINE_STAGE_REFERENCES[PipelineStage.ACTIVATION], "PL-05")
        self.assertEqual(
            PIPELINE_ORDER,
            (
                PipelineStage.DISCOVERY,
                PipelineStage.INTEGRITY,
                PipelineStage.API_VERSION_GATE,
                PipelineStage.PERMISSION,
                PipelineStage.DEPENDENCY_RESOLUTION,
                PipelineStage.ACTIVATION,
            ),
        )


class PipelineRejectionFeedbackTests(unittest.TestCase):
    def _assert_structured(self, rejection, stage: PipelineStage) -> None:
        self.assertIs(rejection.stage, stage)
        self.assertEqual(
            rejection.pipeline_reference, PIPELINE_STAGE_REFERENCES[stage]
        )
        self.assertTrue(rejection.criterion)
        self.assertTrue(rejection.reason)

    def test_discovery_rejection_carries_stage_and_criterion(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="wp003-disc-"))
        plugin_dir = root / "plugins"
        (plugin_dir / "compatible").mkdir(parents=True)
        (plugin_dir / "compatible" / "plugin.toml").write_text(
            'id = "compatible"\nversion = "1.0.0"\nrequires_application = "0.8.0"\n',
            encoding="utf-8",
        )
        (plugin_dir / "incompatible").mkdir(parents=True)
        (plugin_dir / "incompatible" / "plugin.toml").write_text(
            'id = "incompatible"\nversion = "1.0.0"\nrequires_application = "99.0.0"\n',
            encoding="utf-8",
        )
        context = _context(root)
        PluginDiscoveryStage().execute(context)
        self.assertEqual(
            tuple(m.identifier for m in context.manifests), ("compatible",)
        )
        self.assertEqual(len(context.pipeline_rejections), 1)
        rejection = context.pipeline_rejections[0]
        self.assertEqual(rejection.identifier, "incompatible")
        self._assert_structured(rejection, PipelineStage.DISCOVERY)
        self.assertIs(
            rejection.rejection_code, RejectionCode.APPLICATION_VERSION_INCOMPATIBLE
        )

    def test_loader_discover_contract_is_preserved(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="wp003-loader-"))
        loader = PluginLoader(root / "plugins", VersionManager(Version.parse("0.9.0")))
        self.assertEqual(loader.discover(), ())
        self.assertEqual(loader.discover_report(), ((), ()))

    def test_integrity_rejection_carries_stage_and_criterion(self) -> None:
        context = _context()
        security = PluginSecurity(context.events, logger=context.logger)
        security.reject("com.bad", "explicitly rejected for test")
        context.registry.register(PluginSecurity, security)
        context.manifests = (_manifest("com.bad"),)
        PluginSecurityStage().execute(context)
        rejections = [
            r for r in context.pipeline_rejections
            if r.stage is PipelineStage.INTEGRITY
        ]
        self.assertEqual(len(rejections), 1)
        self._assert_structured(rejections[0], PipelineStage.INTEGRITY)
        self.assertIs(rejections[0].rejection_code, RejectionCode.INTEGRITY_FAILED)

    def test_api_version_rejection_carries_stage_and_criterion(self) -> None:
        context = _context()
        context.manifests = (_manifest("com.future", api_version="99.0.0"),)
        PluginSecurityStage().execute(context)
        rejections = [
            r for r in context.pipeline_rejections
            if r.stage is PipelineStage.API_VERSION_GATE
        ]
        self.assertEqual(len(rejections), 1)
        self._assert_structured(rejections[0], PipelineStage.API_VERSION_GATE)
        self.assertIs(
            rejections[0].rejection_code, RejectionCode.API_VERSION_INCOMPATIBLE
        )

    def test_permission_rejection_carries_stage_and_criterion(self) -> None:
        context = _context()
        context.manifests = (_manifest("com.greedy", permissions=("credentials",)),)
        PluginSecurityStage().execute(context)
        rejections = [
            r for r in context.pipeline_rejections
            if r.stage is PipelineStage.PERMISSION
        ]
        self.assertEqual(len(rejections), 1)
        self._assert_structured(rejections[0], PipelineStage.PERMISSION)
        self.assertIs(rejections[0].rejection_code, RejectionCode.PERMISSION_DENIED)

    def test_dependency_rejection_carries_stage_and_criterion(self) -> None:
        context = _context()
        context.manifests = (
            _manifest(
                "com.dependent",
                dependencies=({"id": "com.missing", "version": ""},),
            ),
        )
        PluginSecurityStage().execute(context)
        rejections = [
            r for r in context.pipeline_rejections
            if r.stage is PipelineStage.DEPENDENCY_RESOLUTION
        ]
        self.assertEqual(len(rejections), 1)
        self.assertEqual(rejections[0].identifier, "com.dependent")
        self._assert_structured(rejections[0], PipelineStage.DEPENDENCY_RESOLUTION)

    def test_activation_validation_rejection_carries_stage_and_code(self) -> None:
        context = _context()
        diagnostic = _validate_for_activation(
            _manifest(""), frozenset(), "1.0.0"
        )
        self.assertFalse(diagnostic.accepted)
        _reject_plugin(
            diagnostic.identifier, diagnostic, context.events, context.logger, context
        )
        self.assertEqual(len(context.pipeline_rejections), 1)
        rejection = context.pipeline_rejections[0]
        self._assert_structured(rejection, PipelineStage.ACTIVATION)
        self.assertIs(rejection.rejection_code, RejectionCode.MANIFEST_INVALID)

    def test_admitted_plugins_produce_no_rejection(self) -> None:
        context = _context()
        context.manifests = (_manifest("com.clean"),)
        PluginSecurityStage().execute(context)
        self.assertEqual(context.pipeline_rejections, [])
        self.assertEqual(
            tuple(m.identifier for m in context.admitted_manifests), ("com.clean",)
        )


if __name__ == "__main__":
    unittest.main()
