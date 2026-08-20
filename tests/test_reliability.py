"""WP-005 Reliability tests: error recovery (FR-009) and failure isolation (FR-010).

Covers AC-009.1/AC-009.2 (defined error state and consistent cleanup after a
failed stage run) and AC-010.1/AC-010.2 (plugin failure isolation during
activation and documented failed activations with continued operation).
Evidence carrier for EV-W05; contributes to EV-I01.
"""

from __future__ import annotations

import gc
import logging
import sys
import tempfile
import types
import unittest
from dataclasses import dataclass, field
from pathlib import Path

from core.events import EventBus
from core.registry import ServiceRegistry
from core.version import Version
from plugins.loader import PluginManifest

from app.application_host import ApplicationHost
from app.bootstrap import BootstrapManager, default_stages
from app.bootstrap.stages_plugin import (
    ActivationFailurePool,
    PluginActivationStage,
    PluginRuntimePool,
)
from app.bootstrap.types import (
    PIPELINE_ORDER,
    BootstrapContext,
    BootstrapError,
    PipelineStage,
    StartupPhase,
)
from app.di import DisposableRegistry
from app.errors import ErrorCategory
from app.events import ApplicationEventName
from app.state_machine import ApplicationState

_DEFAULT_CONFIG = """[application]
name = "JOCHEN X"
version = "0.3.0"
log_level = "INFO"
theme_mode = "dark"
developer_enabled = false

[database]
path = "data/test.sqlite3"

[plugins]
directory = "plugins"
"""


def _make_project_root(directory: str) -> Path:
    """Create a minimal, self-contained project root inside ``directory``."""
    root = Path(directory)
    config_directory = root / "config"
    config_directory.mkdir(parents=True, exist_ok=True)
    (config_directory / "default.toml").write_text(_DEFAULT_CONFIG, encoding="utf-8")
    return root


def _reset_application_logging() -> None:
    """Release log handlers and DB connections so Windows can delete tmp roots."""
    logger = logging.getLogger("jochen_x")
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)
    gc.collect()


@dataclass(frozen=True, slots=True)
class _FailingStage:
    """Stage that always fails with a plain exception."""

    name: str = "wp005_failing"
    phase: StartupPhase = StartupPhase.INITIALIZE
    error: Exception = field(default_factory=lambda: ValueError("boom"))

    def execute(self, context: BootstrapContext) -> None:
        raise self.error


@dataclass(frozen=True, slots=True)
class _BootstrapErrorStage:
    """Stage that fails with an already-defined BootstrapError."""

    name: str = "wp005_bootstrap_error"
    phase: StartupPhase = StartupPhase.INITIALIZE

    def execute(self, context: BootstrapContext) -> None:
        raise BootstrapError("already defined")


class _RecordingDisposable:
    """Disposable that records whether it was released."""

    def __init__(self) -> None:
        self.disposed = False

    def dispose(self) -> None:
        self.disposed = True


class _RaisingDisposable:
    """Disposable whose release fails; cleanup must swallow it."""

    def dispose(self) -> None:
        raise RuntimeError("dispose failed")


@dataclass(frozen=True, slots=True)
class _ProvisioningStage:
    """Stage that registers a disposable on the context, like RegistryStage does."""

    disposable: _RecordingDisposable
    name: str = "wp005_provisioning"
    phase: StartupPhase = StartupPhase.INITIALIZE

    def execute(self, context: BootstrapContext) -> None:
        registry = DisposableRegistry(logging.getLogger("test.wp005"))
        registry.register(self.disposable)
        context.disposables = registry


class _RecordingRuntime:
    """Stand-in plugin runtime recording shutdown calls (duck-typed like PluginRuntime)."""

    def __init__(self, *, raise_on_shutdown: bool = False) -> None:
        self.shutdown_calls = 0
        self._raise = raise_on_shutdown

    def shutdown(self) -> None:
        self.shutdown_calls += 1
        if self._raise:
            raise RuntimeError("runtime shutdown failed")


@dataclass(frozen=True, slots=True)
class _RuntimeInjectingStage:
    """Stage that leaves an activated runtime behind before a later stage fails."""

    runtime: _RecordingRuntime
    name: str = "wp005_runtime_injecting"
    phase: StartupPhase = StartupPhase.INITIALIZE

    def execute(self, context: BootstrapContext) -> None:
        context.plugin_runtimes = (self.runtime,)  # type: ignore[assignment]


class StageFailureContractTests(unittest.TestCase):
    """AC-009.1 — a failing stage yields a defined error, not an unhandled abort."""

    def test_stage_failure_raises_bootstrap_error_with_cause(self) -> None:
        original = ValueError("boom")
        manager = BootstrapManager(stages=(_FailingStage(error=original),))
        context = manager.begin(Path("."))
        with self.assertRaises(BootstrapError) as caught:
            manager.run_phase(context, StartupPhase.INITIALIZE)
        self.assertIs(caught.exception.__cause__, original)
        self.assertIn("wp005_failing", str(caught.exception))

    def test_bootstrap_error_passes_through_unwrapped(self) -> None:
        manager = BootstrapManager(stages=(_BootstrapErrorStage(),))
        context = manager.begin(Path("."))
        with self.assertRaises(BootstrapError) as caught:
            manager.run_phase(context, StartupPhase.INITIALIZE)
        self.assertIsNone(caught.exception.__cause__)
        self.assertEqual(str(caught.exception), "already defined")


class HostStartupFailureTests(unittest.TestCase):
    """AC-009.1 — the host settles in a defined error state on startup failure."""

    def _failing_host(self) -> ApplicationHost:
        manager = BootstrapManager(stages=(_FailingStage(),))
        return ApplicationHost(Path("."), bootstrap_manager=manager)

    def test_failed_startup_raises_defined_error_and_records_fatal(self) -> None:
        host = self._failing_host()
        with self.assertRaises(BootstrapError):
            host.start()
        report = host.fatal_report
        self.assertIsNotNone(report)
        assert report is not None
        self.assertIs(report.category, ErrorCategory.FATAL)
        self.assertTrue(report.is_fatal)
        self.assertEqual(report.context.get("phase"), "startup")

    def test_failed_startup_settles_in_shutdown_state(self) -> None:
        host = self._failing_host()
        with self.assertRaises(BootstrapError):
            host.start()
        self.assertIs(host.state, ApplicationState.SHUTDOWN)

    def test_failed_startup_emits_shutdown_completed_event(self) -> None:
        host = self._failing_host()
        completed: list[dict[str, object]] = []
        host.events.subscribe(
            str(ApplicationEventName.SHUTDOWN_COMPLETED),
            lambda event: completed.append(dict(event.payload)),
        )
        with self.assertRaises(BootstrapError):
            host.start()
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0].get("exit_code"), 1)

    def test_failed_startup_reports_unhealthy_errors_component(self) -> None:
        host = self._failing_host()
        with self.assertRaises(BootstrapError):
            host.start()
        errors_status = next(status for status in host.health() if status.name == "errors")
        self.assertFalse(errors_status.healthy)

    def test_failure_in_plugin_phase_follows_same_defined_path(self) -> None:
        manager = BootstrapManager(
            stages=(_FailingStage(name="wp005_plugin_phase", phase=StartupPhase.LOAD_PLUGINS),)
        )
        host = ApplicationHost(Path("."), bootstrap_manager=manager)
        with self.assertRaises(BootstrapError):
            host.start()
        self.assertIs(host.state, ApplicationState.SHUTDOWN)
        self.assertIsNotNone(host.fatal_report)


class StartupCleanupTests(unittest.TestCase):
    """AC-009.2 — initialised components are consistently released after a failure."""

    def test_disposables_released_after_failed_stage(self) -> None:
        disposable = _RecordingDisposable()
        manager = BootstrapManager(
            stages=(_ProvisioningStage(disposable), _FailingStage())
        )
        host = ApplicationHost(Path("."), bootstrap_manager=manager)
        with self.assertRaises(BootstrapError):
            host.start()
        self.assertTrue(disposable.disposed)

    def test_runtimes_shut_down_after_failed_later_stage(self) -> None:
        runtime = _RecordingRuntime()
        manager = BootstrapManager(
            stages=(
                _RuntimeInjectingStage(runtime),
                _FailingStage(name="wp005_late", phase=StartupPhase.FINALIZE),
            )
        )
        host = ApplicationHost(Path("."), bootstrap_manager=manager)
        with self.assertRaises(BootstrapError):
            host.start()
        self.assertEqual(runtime.shutdown_calls, 1)

    def test_abort_removes_imported_plugin_modules(self) -> None:
        identifier = "wp005_abort_module_probe"
        sys.modules[identifier] = types.ModuleType(identifier)
        sys.modules[f"{identifier}.sub"] = types.ModuleType(f"{identifier}.sub")
        try:
            manager = BootstrapManager(stages=())
            context = manager.begin(Path("."))
            context.manifests = (
                PluginManifest(
                    identifier=identifier,
                    version=Version(1, 0, 0),
                    required_application_version=Version(0, 3, 0),
                ),
            )
            manager.abort(context)
            self.assertNotIn(identifier, sys.modules)
            self.assertNotIn(f"{identifier}.sub", sys.modules)
        finally:
            sys.modules.pop(identifier, None)
            sys.modules.pop(f"{identifier}.sub", None)

    def test_abort_is_guarded_and_never_raises(self) -> None:
        manager = BootstrapManager(stages=())
        context = manager.begin(Path("."))
        context.plugin_runtimes = (_RecordingRuntime(raise_on_shutdown=True),)  # type: ignore[assignment]
        registry = DisposableRegistry(logging.getLogger("test.wp005"))
        registry.register(_RaisingDisposable())
        context.disposables = registry
        manager.abort(context)  # must not raise
        self.assertIsNone(manager.pending_context())

    def test_pending_context_cleared_after_successful_build(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            root = _make_project_root(directory)
            try:
                from app.state_machine import ApplicationStateMachine

                manager = BootstrapManager()
                context = manager.begin(root)
                self.assertIs(manager.pending_context(), context)
                for phase in StartupPhase:
                    manager.run_phase(context, phase)
                manager.build_context(context, ApplicationStateMachine())
                self.assertIsNone(manager.pending_context())
            finally:
                _reset_application_logging()

    def test_recover_after_failed_startup_reaches_ready(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            root = _make_project_root(directory)
            try:
                attempts: list[int] = []

                @dataclass(frozen=True, slots=True)
                class _FlakyStage:
                    name: str = "wp005_flaky"
                    phase: StartupPhase = StartupPhase.INITIALIZE

                    def execute(self, context: BootstrapContext) -> None:
                        attempts.append(1)
                        if len(attempts) == 1:
                            raise RuntimeError("transient failure")

                manager = BootstrapManager(stages=(_FlakyStage(), *default_stages()))
                host = ApplicationHost(root, bootstrap_manager=manager)
                with self.assertRaises(BootstrapError):
                    host.start()
                self.assertIs(host.state, ApplicationState.SHUTDOWN)
                context = host.recover()
                self.assertIs(host.state, ApplicationState.READY)
                self.assertTrue(context.runtime_state.is_ready)
                self.assertIsNone(host.fatal_report)
                host.shutdown()
            finally:
                _reset_application_logging()


def _snapshot_sys_modules() -> set[str]:
    return set(sys.modules)


def _cleanup_test_modules(snapshot: set[str]) -> None:
    for name in set(sys.modules) - snapshot:
        sys.modules.pop(name, None)


_GOOD_PLUGIN = '''
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
'''

_BROKEN_IMPORT_PLUGIN = 'raise RuntimeError("broken at import")\n'


class ActivationIsolationTests(unittest.TestCase):
    """AC-010.1 / AC-010.2 — activation failures stay isolated and documented."""

    def setUp(self) -> None:
        self._modules_snapshot = _snapshot_sys_modules()

    def tearDown(self) -> None:
        _cleanup_test_modules(self._modules_snapshot)

    def _make_manifest(self, identifier: str) -> PluginManifest:
        return PluginManifest(
            identifier=identifier,
            version=Version(1, 0, 0),
            required_application_version=Version(0, 3, 0),
        )

    def _make_context(self, root: Path) -> BootstrapContext:
        from config.settings import ApplicationSettings
        from core.environment import Environment

        context = BootstrapContext(root=root)
        context.logger = logging.getLogger("test.wp005.activation")
        context.events = EventBus(logger=context.logger)
        context.registry = ServiceRegistry()
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

    def _write_plugin(self, plugin_dir: Path, identifier: str, source: str) -> None:
        pkg = plugin_dir / identifier
        pkg.mkdir(parents=True, exist_ok=True)
        (pkg / "__init__.py").write_text(source.format(identifier=identifier), encoding="utf-8")

    def test_failing_plugin_does_not_prevent_other_activations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            self._write_plugin(plugin_dir, "wp005-broken", _BROKEN_IMPORT_PLUGIN)
            self._write_plugin(plugin_dir, "wp005-good", _GOOD_PLUGIN)
            context = self._make_context(root)
            context.admitted_manifests = (
                self._make_manifest("wp005-broken"),
                self._make_manifest("wp005-good"),
            )
            activated: list[str] = []
            failed: list[str] = []
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_ACTIVATED),
                lambda event: activated.append(event.payload["identifier"]),
            )
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_FAILED),
                lambda event: failed.append(event.payload["identifier"]),
            )
            PluginActivationStage().execute(context)
            pool = context.registry.get(PluginRuntimePool)
            self.assertEqual(len(pool.runtimes), 1)
            self.assertEqual(activated, ["wp005-good"])
            self.assertEqual(failed, ["wp005-broken"])

    def test_good_plugin_between_two_failing_plugins_activates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            self._write_plugin(plugin_dir, "wp005-broken-a", _BROKEN_IMPORT_PLUGIN)
            self._write_plugin(plugin_dir, "wp005-good", _GOOD_PLUGIN)
            self._write_plugin(plugin_dir, "wp005-broken-b", _BROKEN_IMPORT_PLUGIN)
            context = self._make_context(root)
            context.admitted_manifests = (
                self._make_manifest("wp005-broken-a"),
                self._make_manifest("wp005-good"),
                self._make_manifest("wp005-broken-b"),
            )
            PluginActivationStage().execute(context)
            pool = context.registry.get(PluginRuntimePool)
            self.assertEqual(len(pool.runtimes), 1)
            failures = context.registry.get(ActivationFailurePool)
            self.assertEqual(
                sorted(failure.plugin_id for failure in failures.failures),
                ["wp005-broken-a", "wp005-broken-b"],
            )

    def test_failed_activation_is_documented_in_failure_pool(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            self._write_plugin(plugin_dir, "wp005-broken", _BROKEN_IMPORT_PLUGIN)
            context = self._make_context(root)
            context.admitted_manifests = (self._make_manifest("wp005-broken"),)
            PluginActivationStage().execute(context)
            failures = context.registry.get(ActivationFailurePool)
            self.assertEqual(len(failures.failures), 1)
            failure = failures.failures[0]
            self.assertEqual(failure.plugin_id, "wp005-broken")
            self.assertEqual(failure.phase, "activation")
            self.assertTrue(failure.reason)
            activation_rejections = [
                rejection
                for rejection in context.pipeline_rejections
                if rejection.stage is PipelineStage.ACTIVATION
            ]
            self.assertEqual(len(activation_rejections), 1)
            self.assertEqual(activation_rejections[0].identifier, "wp005-broken")

    def test_failure_pool_registered_and_empty_when_all_succeed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            self._write_plugin(plugin_dir, "wp005-good", _GOOD_PLUGIN)
            context = self._make_context(root)
            context.admitted_manifests = (self._make_manifest("wp005-good"),)
            PluginActivationStage().execute(context)
            failures = context.registry.get(ActivationFailurePool)
            self.assertEqual(failures.failures, ())

    def test_operation_continues_with_successfully_activated_plugins(self) -> None:
        from sdk.plugin import PluginLifecycleState

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            self._write_plugin(plugin_dir, "wp005-broken", _BROKEN_IMPORT_PLUGIN)
            self._write_plugin(plugin_dir, "wp005-good", _GOOD_PLUGIN)
            context = self._make_context(root)
            context.admitted_manifests = (
                self._make_manifest("wp005-broken"),
                self._make_manifest("wp005-good"),
            )
            PluginActivationStage().execute(context)
            pool = context.registry.get(PluginRuntimePool)
            self.assertEqual(len(pool.runtimes), 1)
            self.assertIs(pool.runtimes[0].state, PluginLifecycleState.STARTED)
            self.assertEqual(context.plugin_runtimes, pool.runtimes)


class InvariantPreservationTests(unittest.TestCase):
    """BI-04 / BI-06 / PL-01..PL-05 remain untouched by WP-005."""

    def test_pipeline_order_unchanged(self) -> None:
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

    def test_default_stage_sequence_is_deterministic(self) -> None:
        first = [stage.name for stage in default_stages()]
        second = [stage.name for stage in default_stages()]
        self.assertEqual(first, second)
        self.assertLess(first.index("plugin_security"), first.index("plugin_activation"))


if __name__ == "__main__":
    unittest.main()
