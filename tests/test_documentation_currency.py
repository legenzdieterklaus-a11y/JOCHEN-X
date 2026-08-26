"""WP-007 documentation currency tests (FR-011, FR-012).

Covers AC-011.1 (every public symbol in ``sdk.__all__`` is described in the SDK
documentation), AC-011.2 (the SDK documentation references the correct SDK API
version), AC-012.1 (the architecture documentation names the modules, public
APIs and contracts of the implemented state) and AC-012.2 (no statement of the
architecture documentation contradicts the implemented code).

The checks are mechanical on purpose: they compare the documents against the
live code rather than against a copy of it, so the documentation cannot drift
without a test failure.
"""

from __future__ import annotations

import importlib
import re
import unittest
from pathlib import Path

from app.bootstrap.stages_plugin import ActivationFailurePool, PluginRuntimePool
from app.bootstrap.types import PIPELINE_STAGE_REFERENCES, PipelineStage
from core.observability import PluginDiagnosticsReport
from core.observability_registry import HealthCheckRegistry, MetricsRegistry

import sdk
from sdk.version import SDK_API_VERSION, SDK_VERSION

_ROOT = Path(__file__).resolve().parents[1]
_SDK_DOC = _ROOT / "docs" / "sdk.md"
_EXTENSIONS_DOC = _ROOT / "docs" / "extensions.md"
_ARCHITECTURE_ROOT_DOC = _ROOT / "ARCHITECTURE.md"
_ARCHITECTURE_DOC = _ROOT / "docs" / "architecture.md"

_MWB012_DOCS = (
    _ARCHITECTURE_ROOT_DOC,
    _ARCHITECTURE_DOC,
    _ROOT / "docs" / "core.md",
    _ROOT / "docs" / "events.md",
    _ROOT / "docs" / "security.md",
    _ROOT / "docs" / "services.md",
    _ROOT / "docs" / "developer.md",
    _ROOT / "docs" / "diagnostics.md",
    _ROOT / "docs" / "health.md",
    _ROOT / "docs" / "performance.md",
)

_MODULE_PATH = re.compile(r"`([a-z_][a-z0-9_]*(?:/[a-z0-9_]+)*\.py)`")
_ADR_LINK = re.compile(r"\((?:docs/)?(adr/\d{3}-[a-z0-9-]+\.md)\)")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class SdkSymbolCoverageTests(unittest.TestCase):
    """AC-011.1 — every exported SDK symbol is described in the SDK docs."""

    def test_every_public_symbol_is_documented(self) -> None:
        document = _read(_SDK_DOC)
        for symbol in sdk.__all__:
            with self.subTest(symbol=symbol):
                self.assertRegex(document, rf"\b{re.escape(symbol)}\b")

    def test_documented_symbols_are_importable_from_sdk(self) -> None:
        for symbol in sdk.__all__:
            with self.subTest(symbol=symbol):
                self.assertTrue(hasattr(sdk, symbol))

    def test_extension_points_are_documented(self) -> None:
        """The WP-002 extension point is part of the public surface (FR-011)."""
        document = _read(_SDK_DOC)
        self.assertIn("PluginExtensions", document)
        self.assertIn("ExtensionRegistrar", document)
        self.assertIn("with_extensions", document)

    def test_package_layout_lists_only_existing_modules(self) -> None:
        for module in ("version", "errors", "manifest", "logging", "config",
                       "resources", "events", "services", "context", "plugin"):
            with self.subTest(module=module):
                self.assertTrue((_ROOT / "sdk" / f"{module}.py").is_file())
                self.assertIn(f"{module}.py", _read(_SDK_DOC))


class SdkVersionCurrencyTests(unittest.TestCase):
    """AC-011.2 — the documented version constants match the shipped SDK."""

    def test_api_version_is_referenced_correctly(self) -> None:
        self.assertEqual(SDK_API_VERSION, "1.0.0")
        self.assertIn(SDK_API_VERSION, _read(_SDK_DOC))

    def test_sdk_version_is_referenced_correctly(self) -> None:
        self.assertIn(SDK_VERSION, _read(_SDK_DOC))

    def test_specification_title_tracks_the_sdk_version(self) -> None:
        first_line = _read(_SDK_DOC).splitlines()[0]
        self.assertIn(SDK_VERSION, first_line)

    def test_no_superseded_version_claim_remains(self) -> None:
        """Superseded release numbers must not survive as version claims."""
        for document in (_SDK_DOC, _EXTENSIONS_DOC):
            with self.subTest(document=document.name):
                text = _read(document)
                self.assertNotIn("Specification v0.7", text)
                self.assertNotIn("Definition of Done – v0.7", text)

    def test_version_table_matches_the_constants(self) -> None:
        text = _read(_SDK_DOC)
        self.assertIn(f'Released SDK package semver (`"{SDK_VERSION}"`)', text)
        self.assertIn(f'Public plugin API contract semver (`"{SDK_API_VERSION}"`)', text)


class ArchitectureCoverageTests(unittest.TestCase):
    """AC-012.1 — the architecture documentation names the implemented state."""

    def test_pipeline_stages_are_named(self) -> None:
        text = _read(_ARCHITECTURE_ROOT_DOC) + _read(_ARCHITECTURE_DOC)
        for stage in PipelineStage:
            with self.subTest(stage=stage.name):
                self.assertIn(stage.name, text)
                self.assertIn(PIPELINE_STAGE_REFERENCES[stage], text)

    def test_registry_published_aggregates_are_named(self) -> None:
        text = _read(_ARCHITECTURE_ROOT_DOC) + _read(_ARCHITECTURE_DOC)
        for name in (
            "PluginRuntimePool",
            "ActivationFailurePool",
            "PluginDiagnosticsReport",
            "HealthCheckRegistry",
            "MetricsRegistry",
        ):
            with self.subTest(name=name):
                self.assertIn(name, text)

    def test_observability_contracts_are_documented(self) -> None:
        text = "\n".join(_read(doc) for doc in _MWB012_DOCS)
        for name in (
            "Metrics",
            "MetricSource",
            "CallableMetricSource",
            "PluginHealthCheck",
            "run_health_checks",
            "ProcessMetricSource",
            "PluginDiagnostic",
            "DiagnosticOutcome",
            "PluginRuntimeDiagnostics",
        ):
            with self.subTest(name=name):
                self.assertIn(name, text)

    def test_rejection_contracts_are_documented(self) -> None:
        text = "\n".join(_read(doc) for doc in (*_MWB012_DOCS, _EXTENSIONS_DOC))
        for name in ("PipelineRejection", "PipelineStage", "RejectionCode",
                     "ValidationDiagnostic", "ActivationFailure"):
            with self.subTest(name=name):
                self.assertIn(name, text)

    def test_frozen_architecture_reference_is_declared(self) -> None:
        """PP-03: the frozen reference is named and separated from this doc set."""
        for document in (_ARCHITECTURE_ROOT_DOC, _ARCHITECTURE_DOC):
            with self.subTest(document=document.name):
                text = _read(document)
                self.assertIn("architecture-book-v2.md", text)
                self.assertIn("FROZEN", text)


class ArchitectureConsistencyTests(unittest.TestCase):
    """AC-012.2 — no statement contradicts the implemented code."""

    def test_every_referenced_module_path_exists(self) -> None:
        for document in (*_MWB012_DOCS, _SDK_DOC, _EXTENSIONS_DOC):
            for path in sorted(set(_MODULE_PATH.findall(_read(document)))):
                with self.subTest(document=document.name, path=path):
                    self.assertTrue(
                        (_ROOT / path).is_file(),
                        f"{document.name} references a non-existent module: {path}",
                    )

    def test_every_referenced_adr_exists(self) -> None:
        for document in (*_MWB012_DOCS, _SDK_DOC, _EXTENSIONS_DOC):
            for adr in sorted(set(_ADR_LINK.findall(_read(document)))):
                with self.subTest(document=document.name, adr=adr):
                    self.assertTrue((_ROOT / "docs" / adr).is_file())

    def test_adr_index_matches_the_adr_files(self) -> None:
        text = _read(_ARCHITECTURE_ROOT_DOC)
        for adr_file in sorted((_ROOT / "docs" / "adr").glob("*.md")):
            with self.subTest(adr=adr_file.name):
                self.assertIn(adr_file.name, text)

    def test_approved_adrs_are_not_listed_as_open(self) -> None:
        text = _read(_ARCHITECTURE_ROOT_DOC)
        for number in ("005", "006", "007"):
            with self.subTest(adr=number):
                row = next(
                    line for line in text.splitlines()
                    if line.startswith(f"| [{number}](")
                )
                self.assertNotIn("Offen", row)
                self.assertIn("APPROVED", row)

    def test_documented_registry_keys_are_actually_registered(self) -> None:
        """Every aggregate the docs claim is published must be a real type."""
        for cls in (PluginRuntimePool, ActivationFailurePool, PluginDiagnosticsReport,
                    HealthCheckRegistry, MetricsRegistry):
            with self.subTest(cls=cls.__name__):
                self.assertTrue(isinstance(cls, type))

    def test_documented_component_modules_are_importable(self) -> None:
        for module in ("core.observability", "core.observability_registry",
                       "app.bootstrap.manager", "app.bootstrap.types",
                       "app.bootstrap.stages_plugin", "developer.contracts",
                       "services.observability", "sdk.context"):
            with self.subTest(module=module):
                self.assertIsNotNone(importlib.import_module(module))


if __name__ == "__main__":
    unittest.main()
