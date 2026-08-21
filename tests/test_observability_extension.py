"""WP-004 Observability tests (FR-007, FR-008).

Covers AC-007.1 (diagnostics carry the plugin identifier and the affected
pipeline stage), AC-007.2 (diagnostics are programmatically retrievable and
not only available as log output), AC-008.1 (new metrics can be registered
without changing existing metrics) and AC-008.2 (plugin-specific health checks
are registered through the existing ``HealthCheck`` protocol).

The tests also pin the invariants the work package had to preserve: the
pipeline order PL-01..PL-05 (BI-06), the WP-003 ``PipelineRejection``
structure, the WP-005 ``ActivationFailurePool`` contract, the additive
character of the public export sets (API-04) and the unchanged
``PluginServices`` whitelist.
"""

from __future__ import annotations

import logging
import sys
import tempfile
import unittest
from pathlib import Path

import core.observability as observability
import sdk.services as sdk_services
from core.events import EventBus
from core.observability import (
    ActivationFailure,
    DiagnosticOutcome,
    HealthStatus,
    Metrics,
    PluginDiagnostic,
    PluginDiagnosticsReport,
    PluginHealthCheck,
    run_health_checks,
)
from core.observability_registry import (
    CallableMetricSource,
    HealthCheckRegistry,
    MetricsRegistry,
)
from core.registry import ServiceRegistry
from core.version import Version, VersionManager
from developer.inspector import ArchitectureInspector
from developer.platform import DeveloperPlatform
from plugins.loader import PluginManifest
from services.observability import MetricsSnapshot, PerformanceMonitor, ProcessMetricSource

from app.bootstrap.stages_plugin import (
    ActivationFailurePool,
    PluginActivationStage,
    PluginDiscoveryStage,
    PluginRuntimePool,
    PluginSecurityStage,
)
from app.bootstrap.types import (
    PIPELINE_ORDER,
    PIPELINE_STAGE_REFERENCES,
    BootstrapContext,
    PipelineStage,
    RejectionCode,
)

_GOOD_PLUGIN = """
from sdk.plugin import Plugin
from sdk.manifest import PluginMetadata

class GoodPlugin(Plugin):
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            identifier="{identifier}",
            name="Good Plugin",
            version="1.0.0",
            api_version="1.0.0",
            author="Test",
            description="A working plugin",
        )
"""

_BROKEN_IMPORT_PLUGIN = 'raise RuntimeError("broken at import")\n'


def _manifest(
    identifier: str,
    *,
    api_version: str | None = None,
    permissions: tuple[str, ...] = (),
    dependencies: tuple[dict[str, str], ...] = (),
) -> PluginManifest:
    return PluginManifest(
        identifier=identifier,
        version=Version.parse("1.0.0"),
        required_application_version=Version.parse("0.3.0"),
        api_version=Version.parse(api_version) if api_version else None,
        permissions=permissions,
        dependencies=dependencies,
    )


def _context(root: Path) -> BootstrapContext:
    from config.settings import ApplicationSettings
    from core.environment import Environment

    context = BootstrapContext(root=root)
    context.logger = logging.getLogger("test.wp004")
    context.events = EventBus(logger=context.logger)
    context.registry = ServiceRegistry()
    context.versions = VersionManager(Version.parse("0.9.0"))
    context.metrics = Metrics()
    context.settings = ApplicationSettings(
        name="Test",
        version="0.7.0",
        log_level="INFO",
        theme_mode="dark",
        developer_enabled=False,
        database_path="data/test.sqlite3",
        plugin_directory="plugins",
    )
    context.environment = Environment.from_root(root)
    return context


def _write_plugin(plugin_dir: Path, identifier: str, source: str) -> None:
    package = plugin_dir / identifier
    package.mkdir(parents=True, exist_ok=True)
    (package / "__init__.py").write_text(source.format(identifier=identifier), encoding="utf-8")


def _write_manifest(plugin_dir: Path, identifier: str, requires_application: str) -> None:
    package = plugin_dir / identifier
    package.mkdir(parents=True, exist_ok=True)
    (package / "plugin.toml").write_text(
        f'id = "{identifier}"\nversion = "1.0.0"\n'
        f'requires_application = "{requires_application}"\n',
        encoding="utf-8",
    )


def _snapshot_sys_modules() -> set[str]:
    return set(sys.modules)


def _cleanup_test_modules(snapshot: set[str]) -> None:
    for name in set(sys.modules) - snapshot:
        sys.modules.pop(name, None)


class _StageScenario:
    """Runs discovery, security and activation once over a prepared plugin tree."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.plugin_dir = root / "plugins"
        _write_manifest(self.plugin_dir, "wp004-old", "99.0.0")
        _write_manifest(self.plugin_dir, "wp004-good", "0.3.0")
        _write_manifest(self.plugin_dir, "wp004-broken", "0.3.0")
        _write_plugin(self.plugin_dir, "wp004-good", _GOOD_PLUGIN)
        _write_plugin(self.plugin_dir, "wp004-broken", _BROKEN_IMPORT_PLUGIN)
        self.context = _context(root)
        PluginDiscoveryStage().execute(self.context)
        self.context.manifests = (
            _manifest("wp004-good"),
            _manifest("wp004-broken"),
            _manifest("wp004-future", api_version="99.0.0"),
            _manifest("wp004-greedy", permissions=("credentials",)),
            _manifest("wp004-dependent", dependencies=({"id": "wp004-missing", "version": ""},)),
        )
        PluginSecurityStage().execute(self.context)
        PluginActivationStage().execute(self.context)

    @property
    def report(self) -> PluginDiagnosticsReport:
        return self.context.registry.get(PluginDiagnosticsReport)


class _ScenarioTestCase(unittest.TestCase):
    """Shared fixture that runs the pipeline once per test."""

    def setUp(self) -> None:
        self._modules_snapshot = _snapshot_sys_modules()
        self._directory = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.scenario = _StageScenario(Path(self._directory.name))

    def tearDown(self) -> None:
        _cleanup_test_modules(self._modules_snapshot)
        self._directory.cleanup()


class PluginDiagnosticContractTests(unittest.TestCase):
    """AC-007.1 — a diagnostic names the plugin and the affected stage."""

    def test_diagnostic_carries_plugin_id_and_stage(self) -> None:
        diagnostic = PluginDiagnostic(
            plugin_id="com.example.plugin",
            stage=PipelineStage.PERMISSION.value,
            outcome=DiagnosticOutcome.REJECTED,
            reason="permission denied",
            pipeline_reference="PL-03",
            code=RejectionCode.PERMISSION_DENIED.value,
            context={"criterion": "permission authorization"},
        )
        self.assertEqual(diagnostic.plugin_id, "com.example.plugin")
        self.assertEqual(diagnostic.stage, "permission")
        self.assertEqual(diagnostic.pipeline_reference, "PL-03")
        self.assertFalse(diagnostic.succeeded)

    def test_diagnostic_context_defaults_to_empty_mapping(self) -> None:
        diagnostic = PluginDiagnostic("id", "discovery", DiagnosticOutcome.REJECTED)
        self.assertEqual(dict(diagnostic.context), {})

    def test_activated_diagnostic_reports_success(self) -> None:
        diagnostic = PluginDiagnostic("id", "activation", DiagnosticOutcome.ACTIVATED)
        self.assertTrue(diagnostic.succeeded)


class PipelineDiagnosticsTests(_ScenarioTestCase):
    """AC-007.1 — every rejecting stage is represented in the report."""

    def test_every_rejecting_stage_is_covered(self) -> None:
        stages = {diagnostic.stage for diagnostic in self.scenario.report}
        self.assertEqual(
            stages,
            {
                PipelineStage.DISCOVERY.value,
                PipelineStage.API_VERSION_GATE.value,
                PipelineStage.PERMISSION.value,
                PipelineStage.DEPENDENCY_RESOLUTION.value,
                PipelineStage.ACTIVATION.value,
            },
        )

    def test_every_diagnostic_carries_identifier_and_pipeline_reference(self) -> None:
        for diagnostic in self.scenario.report:
            with self.subTest(plugin=diagnostic.plugin_id, stage=diagnostic.stage):
                self.assertTrue(diagnostic.plugin_id)
                self.assertEqual(
                    diagnostic.pipeline_reference,
                    PIPELINE_STAGE_REFERENCES[PipelineStage(diagnostic.stage)],
                )

    def test_activated_plugin_is_reported_at_the_activation_stage(self) -> None:
        activated = self.scenario.report.with_outcome(DiagnosticOutcome.ACTIVATED)
        self.assertEqual([item.plugin_id for item in activated], ["wp004-good"])
        self.assertEqual(activated[0].stage, PipelineStage.ACTIVATION.value)
        self.assertEqual(activated[0].pipeline_reference, "PL-05")

    def test_failed_activation_is_distinguished_from_admission_rejections(self) -> None:
        failed = self.scenario.report.with_outcome(DiagnosticOutcome.FAILED)
        self.assertEqual([item.plugin_id for item in failed], ["wp004-broken"])
        self.assertEqual(failed[0].code, RejectionCode.ACTIVATION_FAILED.value)
        self.assertEqual(failed[0].context["phase"], "activation")
        self.assertEqual(failed[0].context["error_type"], "RuntimeError")

    def test_discovery_rejection_survives_in_the_report(self) -> None:
        discovered = self.scenario.report.for_stage(PipelineStage.DISCOVERY.value)
        self.assertEqual([item.plugin_id for item in discovered], ["wp004-old"])
        self.assertEqual(
            discovered[0].code, RejectionCode.APPLICATION_VERSION_INCOMPATIBLE.value
        )
        self.assertTrue(discovered[0].context["criterion"])


class DiagnosticsRetrievalTests(_ScenarioTestCase):
    """AC-007.2 — diagnostics are retrievable programmatically after bootstrap."""

    def test_report_is_registered_and_outlives_the_bootstrap_context(self) -> None:
        registry = self.scenario.context.registry
        report = registry.get(PluginDiagnosticsReport)
        self.scenario.context.pipeline_rejections.clear()
        self.scenario.context.activation_failures.clear()
        self.assertGreater(len(report), 0)
        self.assertIs(registry.get(PluginDiagnosticsReport), report)

    def test_report_is_queryable_by_plugin_and_stage(self) -> None:
        report = self.scenario.report
        self.assertIn("wp004-greedy", report.plugin_ids())
        greedy = report.for_plugin("wp004-greedy")
        self.assertEqual(len(greedy), 1)
        self.assertEqual(greedy[0].stage, PipelineStage.PERMISSION.value)
        self.assertEqual(report.for_plugin("wp004-unknown"), ())
        self.assertEqual(report.for_stage(PipelineStage.INTEGRITY.value), ())

    def test_report_counts_outcomes_for_every_outcome_value(self) -> None:
        counts = self.scenario.report.counts()
        self.assertEqual(set(counts), {outcome.value for outcome in DiagnosticOutcome})
        self.assertEqual(counts["activated"], 1.0)
        self.assertEqual(counts["failed"], 1.0)
        self.assertEqual(sum(counts.values()), float(len(self.scenario.report)))

    def test_developer_platform_exposes_the_diagnostics_port(self) -> None:
        platform = DeveloperPlatform(enabled=True, diagnostics=self.scenario.report)
        self.assertEqual(platform.plugin_diagnostics(), self.scenario.report.diagnostics())

    def test_developer_platform_without_port_reports_nothing(self) -> None:
        self.assertEqual(DeveloperPlatform(enabled=True).plugin_diagnostics(), ())

    def test_developer_platform_plugin_status_reflects_the_real_outcome(self) -> None:
        platform = DeveloperPlatform(
            enabled=True,
            plugins=self.scenario.context.plugins,
            diagnostics=self.scenario.report,
        )
        states = {status.identifier: status.enabled for status in platform.plugins()}
        self.assertTrue(states["wp004-good"])
        self.assertFalse(states["wp004-broken"])

    def test_inspector_warns_about_plugins_that_did_not_activate(self) -> None:
        warnings = (
            ArchitectureInspector(
                self.scenario.context.registry, plugins=self.scenario.report
            )
            .inspect()
            .warnings
        )
        self.assertTrue(any("wp004-broken" in warning for warning in warnings))
        self.assertFalse(any("wp004-good" in warning for warning in warnings))

    def test_inspector_without_the_port_is_unchanged(self) -> None:
        registry = ServiceRegistry()
        registry.register(str, "value")
        report = ArchitectureInspector(registry).inspect()
        self.assertEqual(report.services, 1)
        self.assertEqual(report.warnings, ())


class MetricsExtensionTests(unittest.TestCase):
    """AC-008.1 — registering a source never changes an existing metric."""

    def test_existing_metrics_are_untouched_by_a_registration(self) -> None:
        metrics = Metrics()
        metrics.increment("jobs")
        metrics.record_duration("plugin.activation.duration_ms.demo", 42.5)
        before = metrics.snapshot()

        registry = MetricsRegistry()
        registry.register("demo", CallableMetricSource(lambda: {"queue": 3.0}))
        merged = registry.merge(metrics)

        self.assertEqual(metrics.snapshot(), before)
        self.assertEqual(merged["jobs"], 1)
        self.assertEqual(merged["plugin.activation.duration_ms.demo"], 42.5)
        self.assertEqual(merged["demo.queue"], 3.0)

    def test_existing_metric_wins_on_a_name_collision(self) -> None:
        metrics = Metrics()
        metrics.increment("demo.queue", 7)
        registry = MetricsRegistry()
        registry.register("demo", CallableMetricSource(lambda: {"queue": 3.0}))
        self.assertEqual(registry.merge(metrics)["demo.queue"], 7)

    def test_sources_are_namespaced_and_collected_together(self) -> None:
        registry = MetricsRegistry()
        registry.register("a", CallableMetricSource(lambda: {"value": 1.0}))
        registry.register("b", CallableMetricSource(lambda: {"value": 2.0}))
        self.assertEqual(registry.names(), ("a", "b"))
        self.assertEqual(registry.collect(), {"a.value": 1.0, "b.value": 2.0})

    def test_duplicate_and_empty_source_names_are_rejected(self) -> None:
        registry = MetricsRegistry()
        source = CallableMetricSource(dict)
        registry.register("a", source)
        with self.assertRaises(ValueError):
            registry.register("a", source)
        with self.assertRaises(ValueError):
            registry.register("", source)

    def test_unregister_reports_whether_the_source_existed(self) -> None:
        registry = MetricsRegistry()
        registry.register("a", CallableMetricSource(lambda: {"value": 1.0}))
        self.assertTrue(registry.unregister("a"))
        self.assertFalse(registry.unregister("a"))
        self.assertEqual(registry.collect(), {})

    def test_metrics_contract_is_preserved(self) -> None:
        metrics = Metrics()
        metrics.increment("jobs")
        metrics.increment("jobs")
        metrics.record_duration("step_ms", 1.5)
        self.assertEqual(metrics.snapshot(), {"jobs": 2, "step_ms": 1.5})

    def test_process_metric_source_publishes_measured_snapshot_values(self) -> None:
        class _FixedMonitor(PerformanceMonitor):
            def snapshot(self) -> MetricsSnapshot:
                return MetricsSnapshot(1.5, 2048, fps=60.0)

        collected = ProcessMetricSource(_FixedMonitor()).collect()
        self.assertEqual(collected["process_cpu_seconds"], 1.5)
        self.assertEqual(collected["process_ram_bytes"], 2048.0)
        self.assertEqual(collected["fps"], 60.0)
        self.assertNotIn("gpu_percent", collected)

    def test_process_metric_source_is_registrable(self) -> None:
        registry = MetricsRegistry()
        registry.register("process", ProcessMetricSource())
        self.assertIn("process.process_cpu_seconds", registry.collect())


class HealthCheckRegistrationTests(unittest.TestCase):
    """AC-008.2 — health checks register through the existing protocol."""

    def test_plugin_health_check_registers_and_runs_through_the_protocol(self) -> None:
        registry = HealthCheckRegistry()
        check = PluginHealthCheck("demo", lambda: "started")
        registry.register("demo", check)
        self.assertEqual(registry.names(), ("demo",))
        self.assertEqual(registry.checks(), (check,))
        self.assertEqual(registry.run(), run_health_checks(check))
        self.assertEqual(registry.run()[0], HealthStatus("plugin.demo", True, ""))

    def test_duplicate_and_empty_check_names_are_rejected(self) -> None:
        registry = HealthCheckRegistry()
        check = PluginHealthCheck("demo", lambda: "started")
        registry.register("demo", check)
        with self.assertRaises(ValueError):
            registry.register("demo", check)
        with self.assertRaises(ValueError):
            registry.register("", check)

    def test_unregister_reports_whether_the_check_existed(self) -> None:
        registry = HealthCheckRegistry()
        registry.register("demo", PluginHealthCheck("demo", lambda: "started"))
        self.assertTrue(registry.unregister("demo"))
        self.assertFalse(registry.unregister("demo"))
        self.assertEqual(registry.run(), ())


class ProductiveHealthRegistrationTests(_ScenarioTestCase):
    """AC-008.2 — the activation stage registers real, live health checks."""

    def test_activation_registers_a_health_check_per_plugin(self) -> None:
        checks = self.scenario.context.registry.get(HealthCheckRegistry)
        self.assertEqual(sorted(checks.names()), ["wp004-broken", "wp004-good"])

    def test_registered_checks_report_the_live_runtime_state(self) -> None:
        registry = self.scenario.context.registry
        checks = registry.get(HealthCheckRegistry)
        statuses = {status.name: status for status in checks.run()}
        self.assertTrue(statuses["plugin.wp004-good"].healthy)
        self.assertFalse(statuses["plugin.wp004-broken"].healthy)

        registry.get(PluginRuntimePool).runtimes[0].shutdown()
        statuses = {status.name: status for status in checks.run()}
        self.assertFalse(statuses["plugin.wp004-good"].healthy)
        self.assertEqual(statuses["plugin.wp004-good"].detail, "degraded")

    def test_activation_registers_a_metrics_source_for_the_plugin_runtime(self) -> None:
        metrics_registry = self.scenario.context.registry.get(MetricsRegistry)
        self.assertEqual(metrics_registry.names(), ("plugin.runtime",))
        collected = metrics_registry.collect()
        self.assertEqual(collected["plugin.runtime.activated"], 1.0)
        self.assertEqual(collected["plugin.runtime.failed"], 1.0)

    def test_registered_source_does_not_alter_the_pipeline_metrics(self) -> None:
        metrics = self.scenario.context.metrics
        assert metrics is not None
        recorded = metrics.snapshot()
        self.assertIn("plugin.activation.duration_ms.wp004-good", recorded)
        merged = self.scenario.context.registry.get(MetricsRegistry).merge(metrics)
        self.assertEqual(metrics.snapshot(), recorded)
        for name, value in recorded.items():
            with self.subTest(metric=name):
                self.assertEqual(merged[name], value)


class InvariantPreservationTests(_ScenarioTestCase):
    """BI-06, API-04 and the WP-003 / WP-005 contracts stay as they are."""

    def test_pipeline_order_is_unchanged(self) -> None:
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
        self.assertEqual(set(PIPELINE_STAGE_REFERENCES), set(PipelineStage))

    def test_wp003_rejection_structure_is_preserved(self) -> None:
        rejections = self.scenario.context.pipeline_rejections
        self.assertTrue(rejections)
        for rejection in rejections:
            with self.subTest(identifier=rejection.identifier):
                self.assertIsInstance(rejection.stage, PipelineStage)
                self.assertEqual(
                    rejection.pipeline_reference,
                    PIPELINE_STAGE_REFERENCES[rejection.stage],
                )
                self.assertTrue(rejection.criterion)
                self.assertTrue(rejection.reason)

    def test_wp005_activation_failure_pool_is_preserved(self) -> None:
        pool = self.scenario.context.registry.get(ActivationFailurePool)
        self.assertEqual([failure.plugin_id for failure in pool.failures], ["wp004-broken"])
        failure = pool.failures[0]
        self.assertIsInstance(failure, ActivationFailure)
        self.assertEqual(failure.phase, "activation")
        self.assertEqual(failure.context["error_type"], "RuntimeError")

    def test_activation_isolation_is_preserved(self) -> None:
        pool = self.scenario.context.registry.get(PluginRuntimePool)
        self.assertEqual(len(pool.runtimes), 1)

    def test_public_exports_are_additive(self) -> None:
        baseline = {
            "ActivationFailure",
            "HealthCheck",
            "HealthStatus",
            "Metrics",
            "PluginHealthCheck",
            "Span",
            "Tracer",
            "run_health_checks",
        }
        self.assertTrue(baseline.issubset(set(observability.__all__)))
        for name in observability.__all__:
            with self.subTest(name=name):
                self.assertTrue(hasattr(observability, name))

    def test_plugin_services_whitelist_is_unchanged(self) -> None:
        self.assertEqual(sdk_services.__all__, ["PluginServices", "ServicePermissionCheck"])
        runtime = self.scenario.context.registry.get(PluginRuntimePool).runtimes[0]
        self.assertEqual(set(runtime.plugin.context.services.keys()), {logging.Logger})


if __name__ == "__main__":
    unittest.main()
