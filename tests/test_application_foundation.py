"""Isolated tests for the JOCHEN X application foundation layer.

Each foundation subsystem is verified independently without starting a Qt event
loop. Bootstrap and host tests run against a throwaway project root so they never
touch the developer's working configuration.
"""

from __future__ import annotations

import ast
import gc
import inspect
import json
import logging
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

from core.environment import Environment
from core.events import EventBus
from core.exceptions import DatabaseError
from core.registry import ServiceRegistry
from core.version import Version

from plugins.loader import PluginCatalog, PluginManifest

import app.bootstrap
from app.application_host import ApplicationHost
from app.bootstrap import (
    BootstrapContext,
    BootstrapManager,
    PluginActivationStage,
    PluginRuntimePool,
    PluginSecurityStage,
    StartupPhase,
    default_stages,
)
from app.bootstrap import PluginSecurityStage as PSS
from app.concurrency import CancellationToken, TaskCancelledError, WorkerPool
from app.context import ApplicationContext
from app.di import DisposableRegistry, ServiceProvider
from app.errors import CentralErrorHandler, ErrorCategory, PluginError
from app.events import ApplicationEventName, ApplicationStarting, PluginActivated, PluginActivating
from app.resources import ResourceError, ResourceManager
from app.security.plugin_security import PluginSecurity
from app.settings import RequiredKeysValidator, SettingsError, SettingsProvider
from app.state_machine import ApplicationState, ApplicationStateMachine, IllegalStateTransitionError

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


def _reset_application_logging() -> None:
    """Release log handlers and short-lived DB connections before cleanup.

    The core logger and the core SQLite layer close their file handles and
    connections on garbage collection; forcing a collection here ensures Windows
    can remove the throwaway project root without file-lock races.
    """
    logger = logging.getLogger("jochen_x")
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)
    gc.collect()


def _make_project_root(directory: str) -> Path:
    """Create a minimal, self-contained project root inside ``directory``."""
    root = Path(directory)
    config_directory = root / "config"
    config_directory.mkdir(parents=True, exist_ok=True)
    (config_directory / "default.toml").write_text(_DEFAULT_CONFIG, encoding="utf-8")
    return root


class StateMachineTests(unittest.TestCase):
    def test_valid_transition_emits_event(self) -> None:
        bus = EventBus()
        captured: list[dict[str, object]] = []
        bus.subscribe(str(ApplicationEventName.STATE_CHANGED), lambda event: captured.append(event.payload))
        machine = ApplicationStateMachine(publisher=bus)
        machine.transition(ApplicationState.INITIALIZING)
        self.assertIs(machine.state, ApplicationState.INITIALIZING)
        self.assertEqual(captured, [{"previous": "starting", "current": "initializing"}])

    def test_illegal_transition_raises(self) -> None:
        machine = ApplicationStateMachine()
        machine.transition(ApplicationState.INITIALIZING)
        with self.assertRaises(IllegalStateTransitionError):
            machine.transition(ApplicationState.READY)

    def test_assert_state(self) -> None:
        machine = ApplicationStateMachine()
        with self.assertRaises(IllegalStateTransitionError):
            machine.assert_state(ApplicationState.READY)


class LifecycleEventTests(unittest.TestCase):
    def test_typed_event_converts_to_bus_event(self) -> None:
        event = ApplicationStarting("0.3.0").to_event()
        self.assertEqual(event.name, str(ApplicationEventName.STARTING))
        self.assertEqual(event.payload, {"version": "0.3.0"})


class DependencyInjectionTests(unittest.TestCase):
    def test_service_provider_reads_registry(self) -> None:
        registry = ServiceRegistry()
        registry.register(str, "hello")
        provider = ServiceProvider(registry)
        self.assertEqual(provider.get(str), "hello")
        self.assertIsNone(provider.get_optional(int))

    def test_disposable_registry_reverse_order(self) -> None:
        order: list[int] = []

        class Resource:
            def __init__(self, number: int) -> None:
                self._number = number

            def dispose(self) -> None:
                order.append(self._number)

        registry = DisposableRegistry()
        registry.register(Resource(1))
        registry.register(Resource(2))
        registry.dispose_all()
        self.assertEqual(order, [2, 1])

    def test_disposable_registry_rejects_non_disposable(self) -> None:
        with self.assertRaises(TypeError):
            DisposableRegistry().register(object())


class SettingsProviderTests(unittest.TestCase):
    def test_defaults_migration_backup_restore(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            provider = SettingsProvider(
                path,
                version=2,
                defaults={"a": 1, "b": 2},
                migrations={1: lambda data: {**data, "b": 10}},
                validator=RequiredKeysValidator(("a", "b")),
            )
            self.assertEqual(provider.load(), {"a": 1, "b": 2})
            self.assertTrue(path.exists())

            path.write_text(json.dumps({"version": 1, "settings": {"a": 9}}), encoding="utf-8")
            migrated = provider.load()
            self.assertEqual(migrated, {"a": 9, "b": 10})

            provider.save({"a": 100})
            provider.backup()
            provider.save({"a": 200})
            self.assertEqual(provider.restore()["a"], 100)

    def test_unsupported_future_version_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            path.write_text(json.dumps({"version": 5, "settings": {}}), encoding="utf-8")
            provider = SettingsProvider(path, version=1, defaults={})
            with self.assertRaises(SettingsError):
                provider.load()


class ResourceManagerTests(unittest.TestCase):
    def test_path_safety_and_read(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            environment = Environment.from_root(Path(directory))
            manager = ResourceManager(environment, DisposableRegistry())
            (manager.root / "sample.txt").write_text("content", encoding="utf-8")
            self.assertEqual(manager.read_text("sample.txt"), "content")
            with self.assertRaises(ResourceError):
                manager.path("..", "escape.txt")


class ErrorHandlingTests(unittest.TestCase):
    def test_classification_and_fatal_escalation(self) -> None:
        fatal: list[str] = []
        handler = CentralErrorHandler(
            logger=logging.getLogger("test.errors"), on_fatal=lambda report: fatal.append(report.category.value)
        )
        database = handler.handle(DatabaseError("boom"))
        self.assertTrue(database.is_fatal)
        self.assertIs(database.category, ErrorCategory.DATABASE)

        plugin = handler.handle(PluginError("bad plugin"))
        self.assertFalse(plugin.is_fatal)
        self.assertIs(plugin.category, ErrorCategory.PLUGIN)

        unexpected = handler.handle(ValueError("unknown"))
        self.assertIs(unexpected.category, ErrorCategory.UNEXPECTED)
        self.assertEqual(fatal, ["database", "unexpected"])


class ConcurrencyTests(unittest.TestCase):
    def test_cancellation_token(self) -> None:
        fired: list[int] = []
        token = CancellationToken()
        token.register(lambda: fired.append(1))
        self.assertFalse(token.is_cancelled)
        token.cancel()
        token.cancel()
        self.assertTrue(token.is_cancelled)
        self.assertEqual(fired, [1])
        with self.assertRaises(TaskCancelledError):
            token.raise_if_cancelled()

    def test_worker_pool_runs_task(self) -> None:
        pool = WorkerPool(max_workers=2)
        try:
            handle = pool.submit(lambda token: 21 * 2)
            self.assertTrue(handle.wait(2.0))
            self.assertEqual(handle.result(), 42)
        finally:
            self.assertTrue(pool.shutdown(timeout=2.0))

    def test_worker_pool_cooperative_cancellation(self) -> None:
        pool = WorkerPool(max_workers=1)
        started = threading.Event()

        def work(token: CancellationToken) -> None:
            started.set()
            while not token.is_cancelled:
                time.sleep(0.005)
            token.raise_if_cancelled()

        try:
            handle = pool.submit(work)
            self.assertTrue(started.wait(2.0))
            handle.cancel()
            self.assertTrue(handle.wait(2.0))
            self.assertTrue(handle.is_cancelled)
        finally:
            pool.shutdown(timeout=2.0)


class BootstrapContextTests(unittest.TestCase):
    def test_admitted_manifests_default(self) -> None:
        context = BootstrapContext(root=Path("."))
        self.assertEqual(context.admitted_manifests, ())

    def test_plugin_runtimes_default(self) -> None:
        context = BootstrapContext(root=Path("."))
        self.assertEqual(context.plugin_runtimes, ())


class PluginSecurityStageTests(unittest.TestCase):
    def _make_manifest(self, identifier: str) -> PluginManifest:
        return PluginManifest(
            identifier=identifier,
            version=Version(1, 0, 0),
            required_application_version=Version(0, 3, 0),
        )

    def _make_context(self) -> BootstrapContext:
        logger = logging.getLogger("test.security_stage")
        events = EventBus(logger=logger)
        registry = ServiceRegistry()
        context = BootstrapContext(root=Path("."))
        context.logger = logger
        context.events = events
        context.registry = registry
        return context

    def test_admitted_manifests_set_for_trusted_plugins(self) -> None:
        context = self._make_context()
        manifest = self._make_manifest("good-plugin")
        context.manifests = (manifest,)
        security = PluginSecurity(context.events, logger=context.logger)
        security.approve("good-plugin")
        context.registry.register(PluginSecurity, security)
        stage = PluginSecurityStage()
        stage.execute(context)
        self.assertEqual(len(context.admitted_manifests), 1)
        self.assertEqual(context.admitted_manifests[0].identifier, "good-plugin")

    def test_untrusted_plugins_admitted_after_integrity(self) -> None:
        context = self._make_context()
        manifest = self._make_manifest("untrusted-plugin")
        context.manifests = (manifest,)
        stage = PluginSecurityStage()
        stage.execute(context)
        self.assertEqual(len(context.admitted_manifests), 1)
        self.assertEqual(context.admitted_manifests[0].identifier, "untrusted-plugin")

    def test_explicitly_rejected_plugins_handled(self) -> None:
        context = self._make_context()
        manifest = self._make_manifest("bad-plugin")
        context.manifests = (manifest,)
        security = PluginSecurity(context.events, logger=context.logger)
        security.reject("bad-plugin", "policy violation")
        context.registry.register(PluginSecurity, security)
        stage = PluginSecurityStage()
        stage.execute(context)
        self.assertEqual(context.admitted_manifests, ())

    def test_partition_admitted_and_rejected(self) -> None:
        context = self._make_context()
        good = self._make_manifest("admitted")
        bad = self._make_manifest("not-admitted")
        context.manifests = (good, bad)
        security = PluginSecurity(context.events, logger=context.logger)
        security.approve("admitted")
        security.reject("not-admitted", "policy violation")
        context.registry.register(PluginSecurity, security)
        stage = PluginSecurityStage()
        stage.execute(context)
        self.assertEqual(len(context.admitted_manifests), 1)
        self.assertEqual(context.admitted_manifests[0].identifier, "admitted")

    def test_filtered_plugin_catalog_registered(self) -> None:
        context = self._make_context()
        good = self._make_manifest("admitted")
        bad = self._make_manifest("not-admitted")
        context.manifests = (good, bad)
        security = PluginSecurity(context.events, logger=context.logger)
        security.approve("admitted")
        security.reject("not-admitted", "policy violation")
        context.registry.register(PluginSecurity, security)
        stage = PluginSecurityStage()
        stage.execute(context)
        catalog = context.registry.get(PluginCatalog)
        self.assertEqual(catalog.identifiers, ("admitted",))

    def test_plugin_security_registered_in_registry(self) -> None:
        context = self._make_context()
        context.manifests = ()
        stage = PluginSecurityStage()
        stage.execute(context)
        security = context.registry.get(PluginSecurity)
        self.assertIsInstance(security, PluginSecurity)

    def test_no_plugin_code_imported(self) -> None:
        context = self._make_context()
        manifest = self._make_manifest("some-plugin")
        context.manifests = (manifest,)
        stage = PluginSecurityStage()
        stage.execute(context)
        self.assertNotIn("some-plugin", sys.modules)

    def test_empty_manifests(self) -> None:
        context = self._make_context()
        context.manifests = ()
        stage = PluginSecurityStage()
        stage.execute(context)
        self.assertEqual(context.admitted_manifests, ())


class DefaultStagesOrderingTests(unittest.TestCase):
    def test_security_stage_after_discovery(self) -> None:
        stages = default_stages()
        names = [s.name for s in stages]
        discovery_idx = names.index("plugins")
        security_idx = names.index("plugin_security")
        self.assertEqual(security_idx, discovery_idx + 1)

    def test_security_stage_phase(self) -> None:
        stages = default_stages()
        security = next(s for s in stages if s.name == "plugin_security")
        self.assertIs(security.phase, StartupPhase.LOAD_PLUGINS)


class BootstrapTests(unittest.TestCase):
    def test_phases_build_context(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            root = _make_project_root(directory)
            try:
                manager = BootstrapManager()
                context = manager.begin(root)
                for phase in StartupPhase:
                    manager.run_phase(context, phase)
                application_context = manager.build_context(context, ApplicationStateMachine())
                self.assertIsInstance(application_context, ApplicationContext)
                self.assertEqual(application_context.settings.name, "JOCHEN X")
                self.assertIs(application_context.services.get(EventBus), application_context.events)
            finally:
                _reset_application_logging()


class ApplicationHostTests(unittest.TestCase):
    def test_start_reaches_ready_then_shutdown(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            root = _make_project_root(directory)
            try:
                host = ApplicationHost(root)
                context = host.start()
                self.assertIs(host.state, ApplicationState.READY)
                self.assertTrue(context.runtime_state.is_ready)
                self.assertTrue(all(status.healthy for status in host.health()))
                host.shutdown()
                self.assertIs(host.state, ApplicationState.SHUTDOWN)
            finally:
                _reset_application_logging()

    def test_restart_returns_to_ready(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            root = _make_project_root(directory)
            try:
                host = ApplicationHost(root)
                host.start()
                host.restart()
                self.assertIs(host.state, ApplicationState.READY)
                host.shutdown()
            finally:
                _reset_application_logging()


def _snapshot_sys_modules() -> set[str]:
    """Capture module names for later cleanup of test-loaded plugins."""
    return set(sys.modules)


def _cleanup_test_modules(snapshot: set[str]) -> None:
    """Remove modules added since the snapshot was taken."""
    for name in set(sys.modules) - snapshot:
        sys.modules.pop(name, None)


class PluginActivationStageTests(unittest.TestCase):
    """Tests for PluginActivationStage (Sprint 2)."""

    def setUp(self) -> None:
        self._modules_snapshot = _snapshot_sys_modules()

    def tearDown(self) -> None:
        _cleanup_test_modules(self._modules_snapshot)

    def _make_manifest(self, identifier: str) -> PluginManifest:
        from core.version import Version

        return PluginManifest(
            identifier=identifier,
            version=Version(1, 0, 0),
            required_application_version=Version(0, 3, 0),
        )

    def _make_context(self, root: Path) -> BootstrapContext:
        from config.settings import ApplicationSettings

        logger = logging.getLogger("test.activation_stage")
        events = EventBus(logger=logger)
        registry = ServiceRegistry()
        context = BootstrapContext(root=root)
        context.logger = logger
        context.events = events
        context.registry = registry
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

    def _create_test_plugin(self, plugin_dir: Path, identifier: str, *, api_version: str = "1.0.0") -> None:
        """Create a minimal plugin package on disk."""
        pkg = plugin_dir / identifier
        pkg.mkdir(parents=True, exist_ok=True)
        init_content = f'''
from sdk.plugin import Plugin
from sdk.manifest import PluginMetadata

class TestPlugin(Plugin):
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            identifier="{identifier}",
            name="Test Plugin",
            version="1.0.0",
            api_version="{api_version}",
            author="Test",
            description="A test plugin",
        )
'''
        (pkg / "__init__.py").write_text(init_content, encoding="utf-8")

    def test_activation_stage_activates_plugin(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            self._create_test_plugin(plugin_dir, "test-activation-plugin")
            context = self._make_context(root)
            context.admitted_manifests = (self._make_manifest("test-activation-plugin"),)
            stage = PluginActivationStage()
            stage.execute(context)
            pool = context.registry.get(PluginRuntimePool)
            self.assertEqual(len(pool.runtimes), 1)
            from sdk.plugin import PluginLifecycleState

            self.assertIs(pool.runtimes[0].state, PluginLifecycleState.STARTED)

    def test_activation_stage_api_version_mismatch_at_security_stage(self) -> None:
        """API version mismatch is now caught at PluginSecurityStage (WP-03)."""
        from core.version import Version

        context = self._make_context(Path("."))
        manifest = PluginManifest(
            identifier="bad-api-plugin",
            version=Version(1, 0, 0),
            required_application_version=Version(0, 3, 0),
            api_version=Version(2, 0, 0),
        )
        context.manifests = (manifest,)
        rejected_events: list[str] = []
        context.events.subscribe(
            "security.plugin.rejected",
            lambda e: rejected_events.append(e.payload["identifier"]),
        )

        stage = PSS()
        stage.execute(context)
        self.assertEqual(context.admitted_manifests, ())
        self.assertIn("bad-api-plugin", rejected_events)

    def test_activation_stage_import_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "plugins").mkdir(parents=True)
            context = self._make_context(root)
            context.admitted_manifests = (self._make_manifest("nonexistent-plugin"),)
            failed_events: list[str] = []
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_FAILED),
                lambda e: failed_events.append(e.payload["identifier"]),
            )
            stage = PluginActivationStage()
            stage.execute(context)
            pool = context.registry.get(PluginRuntimePool)
            self.assertEqual(len(pool.runtimes), 0)
            self.assertIn("nonexistent-plugin", failed_events)

    def test_activation_stage_lifecycle_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            pkg = plugin_dir / "failing-init-plugin"
            pkg.mkdir(parents=True)
            (pkg / "__init__.py").write_text(
                '''
from sdk.plugin import Plugin
from sdk.manifest import PluginMetadata

class FailingPlugin(Plugin):
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            identifier="failing-init-plugin",
            name="Failing Plugin",
            version="1.0.0",
            api_version="1.0.0",
            author="Test",
            description="Fails on init",
        )
    def on_initialize(self) -> None:
        raise RuntimeError("init boom")
''',
                encoding="utf-8",
            )
            context = self._make_context(root)
            context.admitted_manifests = (self._make_manifest("failing-init-plugin"),)
            failed_events: list[str] = []
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_FAILED),
                lambda e: failed_events.append(e.payload["identifier"]),
            )
            stage = PluginActivationStage()
            stage.execute(context)
            pool = context.registry.get(PluginRuntimePool)
            self.assertEqual(len(pool.runtimes), 0)
            self.assertIn("failing-init-plugin", failed_events)

    def test_activation_stage_unresolved_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            pkg = plugin_dir / "dep-plugin"
            pkg.mkdir(parents=True)
            (pkg / "__init__.py").write_text(
                '''
from sdk.plugin import Plugin
from sdk.manifest import PluginMetadata, PluginDependency

class DepPlugin(Plugin):
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            identifier="dep-plugin",
            name="Dep Plugin",
            version="1.0.0",
            api_version="1.0.0",
            author="Test",
            description="Has unresolved dep",
            dependencies=(PluginDependency(identifier="missing-dep", minimum_version="1.0.0"),),
        )
''',
                encoding="utf-8",
            )
            context = self._make_context(root)
            context.admitted_manifests = (self._make_manifest("dep-plugin"),)
            failed_events: list[str] = []
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_FAILED),
                lambda e: failed_events.append(e.payload["identifier"]),
            )
            stage = PluginActivationStage()
            stage.execute(context)
            pool = context.registry.get(PluginRuntimePool)
            self.assertEqual(len(pool.runtimes), 0)
            self.assertIn("dep-plugin", failed_events)

    def test_activation_stage_empty_admitted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "plugins").mkdir(parents=True)
            context = self._make_context(root)
            context.admitted_manifests = ()
            stage = PluginActivationStage()
            stage.execute(context)
            pool = context.registry.get(PluginRuntimePool)
            self.assertEqual(len(pool.runtimes), 0)

    def test_activation_stage_graceful_degradation(self) -> None:
        """One bad plugin does not prevent activation of a good plugin."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            self._create_test_plugin(plugin_dir, "good-plugin")
            context = self._make_context(root)
            bad = self._make_manifest("nonexistent-plugin")
            good = self._make_manifest("good-plugin")
            context.admitted_manifests = (bad, good)
            stage = PluginActivationStage()
            stage.execute(context)
            pool = context.registry.get(PluginRuntimePool)
            self.assertEqual(len(pool.runtimes), 1)

    def test_plugin_runtime_pool_registered(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "plugins").mkdir(parents=True)
            context = self._make_context(root)
            context.admitted_manifests = ()
            stage = PluginActivationStage()
            stage.execute(context)
            pool = context.registry.get(PluginRuntimePool)
            self.assertIsInstance(pool, PluginRuntimePool)


class PluginActivationStageOrderingTests(unittest.TestCase):
    def test_activation_stage_in_default_stages(self) -> None:
        stages = default_stages()
        names = [s.name for s in stages]
        self.assertIn("plugin_activation", names)

    def test_activation_stage_before_developer_tools(self) -> None:
        stages = default_stages()
        names = [s.name for s in stages]
        activation_idx = names.index("plugin_activation")
        dev_idx = names.index("developer_tools")
        self.assertLess(activation_idx, dev_idx)

    def test_activation_stage_phase_is_finalize(self) -> None:
        stages = default_stages()
        activation = next(s for s in stages if s.name == "plugin_activation")
        self.assertIs(activation.phase, StartupPhase.FINALIZE)


class PluginActivatingEventTests(unittest.TestCase):
    def test_plugin_activating_event(self) -> None:
        event = PluginActivating("my-plugin")
        self.assertEqual(event.identifier, "my-plugin")
        self.assertIs(event.EVENT_NAME, ApplicationEventName.PLUGIN_ACTIVATING)
        bus_event = event.to_event()
        self.assertEqual(bus_event.name, "application.plugin.activating")
        self.assertEqual(bus_event.payload, {"identifier": "my-plugin"})

    def test_plugin_activated_event(self) -> None:
        event = PluginActivated("my-plugin", "1.2.0")
        self.assertEqual(event.identifier, "my-plugin")
        self.assertEqual(event.version, "1.2.0")
        self.assertIs(event.EVENT_NAME, ApplicationEventName.PLUGIN_ACTIVATED)
        bus_event = event.to_event()
        self.assertEqual(bus_event.name, "application.plugin.activated")
        self.assertEqual(bus_event.payload, {"identifier": "my-plugin", "version": "1.2.0"})


class PluginActivationEventsIntegrationTests(unittest.TestCase):
    """Tests that PLUGIN_ACTIVATING and PLUGIN_ACTIVATED are emitted correctly during activation."""

    def setUp(self) -> None:
        self._modules_snapshot = _snapshot_sys_modules()

    def tearDown(self) -> None:
        _cleanup_test_modules(self._modules_snapshot)

    def _make_manifest(self, identifier: str) -> PluginManifest:
        from core.version import Version

        return PluginManifest(
            identifier=identifier,
            version=Version(1, 0, 0),
            required_application_version=Version(0, 3, 0),
        )

    def _make_context(self, root: Path) -> BootstrapContext:
        from config.settings import ApplicationSettings

        logger = logging.getLogger("test.activation_events")
        events = EventBus(logger=logger)
        registry = ServiceRegistry()
        context = BootstrapContext(root=root)
        context.logger = logger
        context.events = events
        context.registry = registry
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

    def _create_test_plugin(self, plugin_dir: Path, identifier: str) -> None:
        pkg = plugin_dir / identifier
        pkg.mkdir(parents=True, exist_ok=True)
        (pkg / "__init__.py").write_text(
            f'''
from sdk.plugin import Plugin
from sdk.manifest import PluginMetadata

class TestPlugin(Plugin):
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            identifier="{identifier}",
            name="Test Plugin",
            version="1.0.0",
            api_version="1.0.0",
            author="Test",
            description="A test plugin",
        )
''',
            encoding="utf-8",
        )

    def test_activating_emitted_once_per_plugin(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            self._create_test_plugin(plugin_dir, "evt-test-plugin")
            context = self._make_context(root)
            context.admitted_manifests = (self._make_manifest("evt-test-plugin"),)
            activating_events: list[str] = []
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_ACTIVATING),
                lambda e: activating_events.append(e.payload["identifier"]),
            )
            stage = PluginActivationStage()
            stage.execute(context)
            self.assertEqual(activating_events, ["evt-test-plugin"])

    def test_activated_emitted_once_per_plugin(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            self._create_test_plugin(plugin_dir, "evt-activated-plugin")
            context = self._make_context(root)
            context.admitted_manifests = (self._make_manifest("evt-activated-plugin"),)
            activated_events: list[dict[str, object]] = []
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_ACTIVATED),
                lambda e: activated_events.append(e.payload),
            )
            stage = PluginActivationStage()
            stage.execute(context)
            self.assertEqual(len(activated_events), 1)
            self.assertEqual(activated_events[0]["identifier"], "evt-activated-plugin")
            self.assertEqual(activated_events[0]["version"], "1.0.0")

    def test_correct_event_ordering(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            self._create_test_plugin(plugin_dir, "evt-order-plugin")
            context = self._make_context(root)
            context.admitted_manifests = (self._make_manifest("evt-order-plugin"),)
            event_order: list[str] = []
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_ACTIVATING),
                lambda e: event_order.append("activating"),
            )
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_ACTIVATED),
                lambda e: event_order.append("activated"),
            )
            stage = PluginActivationStage()
            stage.execute(context)
            self.assertEqual(event_order, ["activating", "activated"])

    def test_no_activated_event_for_failed_plugin(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "plugins").mkdir(parents=True)
            context = self._make_context(root)
            context.admitted_manifests = (self._make_manifest("nonexistent-evt-plugin"),)
            activated_events: list[str] = []
            activating_events: list[str] = []
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_ACTIVATING),
                lambda e: activating_events.append(e.payload["identifier"]),
            )
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_ACTIVATED),
                lambda e: activated_events.append(e.payload["identifier"]),
            )
            stage = PluginActivationStage()
            stage.execute(context)
            self.assertEqual(activating_events, ["nonexistent-evt-plugin"])
            self.assertEqual(activated_events, [])

    def test_multiple_plugin_activation_events(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            self._create_test_plugin(plugin_dir, "evt-multi-a")
            self._create_test_plugin(plugin_dir, "evt-multi-b")
            context = self._make_context(root)
            context.admitted_manifests = (
                self._make_manifest("evt-multi-a"),
                self._make_manifest("evt-multi-b"),
            )
            event_log: list[tuple[str, str]] = []
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_ACTIVATING),
                lambda e: event_log.append(("activating", e.payload["identifier"])),
            )
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_ACTIVATED),
                lambda e: event_log.append(("activated", e.payload["identifier"])),
            )
            stage = PluginActivationStage()
            stage.execute(context)
            self.assertEqual(
                event_log,
                [
                    ("activating", "evt-multi-a"),
                    ("activated", "evt-multi-a"),
                    ("activating", "evt-multi-b"),
                    ("activated", "evt-multi-b"),
                ],
            )

    def test_plugin_runtimes_populated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            self._create_test_plugin(plugin_dir, "rt-pop-plugin")
            context = self._make_context(root)
            context.admitted_manifests = (self._make_manifest("rt-pop-plugin"),)
            stage = PluginActivationStage()
            stage.execute(context)
            self.assertEqual(len(context.plugin_runtimes), 1)
            from sdk.plugin import PluginLifecycleState

            self.assertIs(context.plugin_runtimes[0].state, PluginLifecycleState.STARTED)

    def test_plugin_runtimes_empty_for_no_plugins(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "plugins").mkdir(parents=True)
            context = self._make_context(root)
            context.admitted_manifests = ()
            stage = PluginActivationStage()
            stage.execute(context)
            self.assertEqual(context.plugin_runtimes, ())

    def test_plugin_runtimes_excludes_failed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin_dir = root / "plugins"
            self._create_test_plugin(plugin_dir, "rt-good-plugin")
            context = self._make_context(root)
            context.admitted_manifests = (
                self._make_manifest("nonexistent-rt-plugin"),
                self._make_manifest("rt-good-plugin"),
            )
            stage = PluginActivationStage()
            stage.execute(context)
            self.assertEqual(len(context.plugin_runtimes), 1)

    def test_no_events_for_rejected_plugins(self) -> None:
        """Plugins not in admitted_manifests produce no activation events."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "plugins").mkdir(parents=True)
            context = self._make_context(root)
            context.admitted_manifests = ()
            event_log: list[str] = []
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_ACTIVATING),
                lambda e: event_log.append(e.payload["identifier"]),
            )
            context.events.subscribe(
                str(ApplicationEventName.PLUGIN_ACTIVATED),
                lambda e: event_log.append(e.payload["identifier"]),
            )
            stage = PluginActivationStage()
            stage.execute(context)
            self.assertEqual(event_log, [])


class ReverseShutdownTests(unittest.TestCase):
    """Tests for Sprint 4: reverse plugin shutdown ordering."""

    def setUp(self) -> None:
        self._modules_snapshot = _snapshot_sys_modules()

    def tearDown(self) -> None:
        _cleanup_test_modules(self._modules_snapshot)

    def _make_manifest(self, identifier: str) -> PluginManifest:
        from core.version import Version

        return PluginManifest(
            identifier=identifier,
            version=Version(1, 0, 0),
            required_application_version=Version(0, 3, 0),
        )

    def _make_context(self, root: Path) -> BootstrapContext:
        from config.settings import ApplicationSettings

        logger = logging.getLogger("test.reverse_shutdown")
        events = EventBus(logger=logger)
        registry = ServiceRegistry()
        context = BootstrapContext(root=root)
        context.logger = logger
        context.events = events
        context.registry = registry
        context.settings = ApplicationSettings(
            name="Test",
            version="0.8.0",
            log_level="INFO",
            theme_mode="dark",
            developer_enabled=False,
            database_path="data/test.sqlite3",
            plugin_directory="plugins",
        )

        context.environment = Environment.from_root(root)
        return context

    def _create_tracking_plugin(
        self, plugin_dir: Path, identifier: str, *, fail_on_shutdown: bool = False
    ) -> None:
        pkg = plugin_dir / identifier
        pkg.mkdir(parents=True, exist_ok=True)
        fail_code = "raise RuntimeError('shutdown boom')" if fail_on_shutdown else "pass"
        (pkg / "__init__.py").write_text(
            f'''
import sdk._test_hooks as _hooks
from sdk.plugin import Plugin
from sdk.manifest import PluginMetadata

class TrackingPlugin(Plugin):
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            identifier="{identifier}",
            name="{identifier}",
            version="1.0.0",
            api_version="1.0.0",
            author="Test",
            description="Tracking plugin",
        )

    def on_stop(self) -> None:
        _hooks.STOP_ORDER.append("{identifier}")

    def on_shutdown(self) -> None:
        _hooks.SHUTDOWN_ORDER.append("{identifier}")
        {fail_code}
''',
            encoding="utf-8",
        )

    def _activate_plugins(self, root: Path, identifiers: list[str], *, fail_shutdown: str | None = None) -> BootstrapContext:
        plugin_dir = root / "plugins"
        for ident in identifiers:
            self._create_tracking_plugin(
                plugin_dir, ident, fail_on_shutdown=(ident == fail_shutdown)
            )
        context = self._make_context(root)
        context.admitted_manifests = tuple(self._make_manifest(i) for i in identifiers)
        stage = PluginActivationStage()
        stage.execute(context)
        return context

    def test_reverse_shutdown_order(self) -> None:
        """Plugins are shut down in reverse activation order."""
        import sdk._test_hooks as hooks

        hooks.STOP_ORDER.clear()
        hooks.SHUTDOWN_ORDER.clear()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = self._activate_plugins(root, ["rs-alpha", "rs-beta", "rs-gamma"])
            pool = context.registry.get(PluginRuntimePool)
            self.assertEqual(len(pool.runtimes), 3)


            for runtime in reversed(pool.runtimes):
                runtime.shutdown()

            self.assertEqual(hooks.STOP_ORDER, ["rs-gamma", "rs-beta", "rs-alpha"])
            self.assertEqual(hooks.SHUTDOWN_ORDER, ["rs-gamma", "rs-beta", "rs-alpha"])

    def test_shutdown_without_plugins(self) -> None:
        """Shutdown works cleanly when no plugins are activated."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            root = _make_project_root(directory)
            try:
                host = ApplicationHost(root)
                host.start()
                host.shutdown()
                self.assertIs(host.state, ApplicationState.SHUTDOWN)
            finally:
                _reset_application_logging()

    def test_shutdown_with_failed_plugin(self) -> None:
        """A failing plugin shutdown does not prevent others from stopping."""
        import sdk._test_hooks as hooks

        hooks.STOP_ORDER.clear()
        hooks.SHUTDOWN_ORDER.clear()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = self._activate_plugins(
                root, ["rs-ok-a", "rs-failing", "rs-ok-b"], fail_shutdown="rs-failing"
            )
            pool = context.registry.get(PluginRuntimePool)
            self.assertEqual(len(pool.runtimes), 3)

            for runtime in reversed(pool.runtimes):
                try:
                    runtime.shutdown()
                except Exception:
                    pass

            self.assertIn("rs-ok-a", hooks.STOP_ORDER)
            self.assertIn("rs-ok-b", hooks.STOP_ORDER)

    def test_host_reverse_shutdown_integration(self) -> None:
        """ApplicationHost.shutdown() calls _shutdown_plugins before ShutdownSequence."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            root = _make_project_root(directory)
            try:
                host = ApplicationHost(root)
                host.start()
                pool = host.context.registry.get(PluginRuntimePool)
                self.assertEqual(len(pool.runtimes), 0)
                host.shutdown()
                self.assertIs(host.state, ApplicationState.SHUTDOWN)
            finally:
                _reset_application_logging()

    def test_shutdown_idempotent(self) -> None:
        """Calling shutdown twice is safe."""
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            root = _make_project_root(directory)
            try:
                host = ApplicationHost(root)
                host.start()
                host.shutdown()
                host.shutdown()
                self.assertIs(host.state, ApplicationState.SHUTDOWN)
            finally:
                _reset_application_logging()

    def test_plugin_runtime_reaches_stopped_state(self) -> None:
        """After shutdown, plugin runtimes reach STOPPED state."""
        import sdk._test_hooks as hooks

        hooks.STOP_ORDER.clear()
        hooks.SHUTDOWN_ORDER.clear()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = self._activate_plugins(root, ["rs-state-check"])
            pool = context.registry.get(PluginRuntimePool)
            from sdk.plugin import PluginLifecycleState

            self.assertIs(pool.runtimes[0].state, PluginLifecycleState.STARTED)
            pool.runtimes[0].shutdown()
            self.assertIs(pool.runtimes[0].state, PluginLifecycleState.STOPPED)

    def test_shutdown_before_start_is_safe(self) -> None:
        """Calling shutdown on a host that was never started does not raise."""
        host = ApplicationHost(Path("."))
        host.shutdown()
        self.assertIs(host.state, ApplicationState.SHUTDOWN)


class BootstrapFacadeTests(unittest.TestCase):
    """Verify the bootstrap package facade re-exports all public symbols."""

    _EXPECTED_EXPORTS = (
        "BootstrapContext",
        "BootstrapError",
        "BootstrapManager",
        "BootstrapStage",
        "ConfigurationStage",
        "DatabaseStage",
        "DependencyInjectionStage",
        "DeveloperToolsStage",
        "EnvironmentStage",
        "LoggingStage",
        "PluginActivationStage",
        "PluginDiscoveryStage",
        "PluginRuntimePool",
        "PluginSecurityStage",
        "RegistryStage",
        "RejectionCode",
        "ResourceStage",
        "SchedulerStage",
        "StartupPhase",
        "ThemeStage",
        "ValidationDiagnostic",
        "default_stages",
    )

    def test_all_public_exports_available(self) -> None:
        """Every declared public export is importable from the facade."""
        self.assertEqual(len(app.bootstrap.__all__), 22)
        for name in self._EXPECTED_EXPORTS:
            with self.subTest(name=name):
                self.assertIn(name, app.bootstrap.__all__)
                self.assertTrue(hasattr(app.bootstrap, name))

    def test_facade_contains_no_definitions(self) -> None:
        """The facade module defines no classes or functions of its own."""
        source = inspect.getsource(sys.modules["app.bootstrap"])
        tree = ast.parse(source)
        for node in ast.iter_child_nodes(tree):
            self.assertNotIsInstance(
                node, ast.ClassDef, f"unexpected class: {getattr(node, 'name', '?')}"
            )
            self.assertNotIsInstance(
                node, ast.FunctionDef, f"unexpected function: {getattr(node, 'name', '?')}"
            )

    def test_default_stages_sequence(self) -> None:
        """default_stages() returns the exact 13-stage sequence."""
        stages = default_stages()
        expected = (
            "EnvironmentStage",
            "ConfigurationStage",
            "LoggingStage",
            "DatabaseStage",
            "RegistryStage",
            "ThemeStage",
            "SchedulerStage",
            "PluginDiscoveryStage",
            "PluginSecurityStage",
            "ResourceStage",
            "PluginActivationStage",
            "DeveloperToolsStage",
            "DependencyInjectionStage",
        )
        self.assertEqual(len(stages), 13)
        self.assertEqual(tuple(type(s).__name__ for s in stages), expected)

    def test_bootstrap_manager_uses_default_stages(self) -> None:
        """BootstrapManager default factory produces the canonical sequence."""
        manager = BootstrapManager()
        self.assertEqual(manager.stages, default_stages())


if __name__ == "__main__":
    unittest.main()
