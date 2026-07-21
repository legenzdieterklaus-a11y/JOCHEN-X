"""Isolated tests for the JOCHEN X application foundation layer.

Each foundation subsystem is verified independently without starting a Qt event
loop. Bootstrap and host tests run against a throwaway project root so they never
touch the developer's working configuration.
"""

from __future__ import annotations

import gc
import json
import logging
import tempfile
import threading
import time
import unittest
from pathlib import Path

from core.environment import Environment
from core.events import EventBus
from core.exceptions import DatabaseError
from core.registry import ServiceRegistry

from app.application_host import ApplicationHost
from app.bootstrap import BootstrapManager, StartupPhase
from app.concurrency import CancellationToken, TaskCancelledError, WorkerPool
from app.context import ApplicationContext
from app.di import DisposableRegistry, ServiceProvider
from app.errors import CentralErrorHandler, ErrorCategory, PluginError
from app.events import ApplicationEventName, ApplicationStarting
from app.resources import ResourceError, ResourceManager
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


if __name__ == "__main__":
    unittest.main()
