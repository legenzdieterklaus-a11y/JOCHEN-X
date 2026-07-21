"""Tests for the JOCHEN X v0.6 desktop navigation framework."""

from __future__ import annotations

import gc
import logging
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

from config.settings import ApplicationSettings, ConfigurationService, ThemeMode
from core.events import EventBus
from plugins.loader import PluginCatalog
from styles.theme import ThemeEngine

from app.application_host import ApplicationHost
from app.concurrency import WorkerPool
from app.security import Permission, SecurityManager
from app.state_machine import ApplicationState
from ui.navigation.layout_manager import LayoutManager
from ui.navigation.main_window import MainWindow
from ui.navigation.module_host import ModuleHost
from ui.navigation.navigation_controller import NavigationController
from ui.navigation.navigation_events import (
    NavigationChanged,
    NavigationEventName,
    WindowStateChanged,
)
from ui.navigation.navigation_item import NavigationItem
from ui.navigation.navigation_models import (
    NavigationGroup,
    NavigationIcon,
    NavigationItemModel,
    NavigationRegistration,
)
from ui.navigation.navigation_registry import NavigationRegistry
from ui.navigation.navigation_service import (
    NavigationService,
    create_desktop_bootstrap_manager,
)
from ui.navigation.sidebar import Sidebar
from ui.navigation.status_bar import StatusBar
from ui.navigation.theme_manager import ThemeManager
from ui.navigation.window_state import WindowState

_DEFAULT_CONFIG = """[application]
name = "JOCHEN X"
version = "0.6.0"
log_level = "INFO"
theme_mode = "dark"
developer_enabled = false

[database]
path = "data/test.sqlite3"

[plugins]
directory = "plugins"
"""


def _make_project_root(directory: str) -> Path:
    """Create a self-contained application root."""
    root = Path(directory)
    config_directory = root / "config"
    config_directory.mkdir(parents=True, exist_ok=True)
    (config_directory / "default.toml").write_text(_DEFAULT_CONFIG, encoding="utf-8")
    return root


def _reset_application_logging() -> None:
    """Release Windows file handles held by test loggers."""
    logger = logging.getLogger("jochen_x")
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)
    gc.collect()


def _item(identifier: str, order: int = 10) -> NavigationItemModel:
    """Build deterministic test metadata."""
    return NavigationItemModel(
        identifier=identifier,
        name=identifier.title(),
        description=f"{identifier} description",
        icon=NavigationIcon.DASHBOARD,
        order=order,
        permission=Permission(f"navigation.{identifier}"),
        group=NavigationGroup.GENERAL,
    )


def _registration(identifier: str, order: int = 10) -> NavigationRegistration:
    """Build a lazy QLabel test module registration."""
    return NavigationRegistration(_item(identifier, order), lambda: QLabel(identifier))


class QtTestCase(unittest.TestCase):
    """Provide one QApplication for widget tests."""

    application: QApplication

    @classmethod
    def setUpClass(cls) -> None:
        cls.application = QApplication.instance() or QApplication([])

    @classmethod
    def tearDownClass(cls) -> None:
        cls.application.processEvents()


class NavigationEventTests(unittest.TestCase):
    """Verify typed event conversion."""

    def test_navigation_changed_payload(self) -> None:
        event = NavigationChanged("dashboard", "chat").to_event()
        self.assertEqual(event.name, str(NavigationEventName.NAVIGATION_CHANGED))
        self.assertEqual(
            event.payload,
            {"previous": "dashboard", "current": "chat"},
        )

    def test_window_state_changed_payload(self) -> None:
        event = WindowStateChanged(False, 1200, 800).to_event()
        self.assertEqual(event.payload["width"], 1200)
        self.assertFalse(event.payload["maximized"])


class NavigationRegistryTests(unittest.TestCase):
    """Verify dynamic registration behavior."""

    def test_register_resolve_order_and_unregister(self) -> None:
        registry = NavigationRegistry()
        registry.register(_registration("later", 20))
        registry.register(_registration("first", 10))
        self.assertEqual(
            tuple(item.item.identifier for item in registry.registrations()),
            ("first", "later"),
        )
        self.assertEqual(registry.get("first").item.name, "First")
        self.assertEqual(registry.unregister("later").item.identifier, "later")

    def test_duplicate_and_unknown_registration_fail(self) -> None:
        registry = NavigationRegistry()
        registry.register(_registration("dashboard"))
        with self.assertRaises(ValueError):
            registry.register(_registration("dashboard"))
        with self.assertRaises(LookupError):
            registry.get("missing")

    def test_parent_must_exist_and_cannot_be_removed_with_child(self) -> None:
        registry = NavigationRegistry()
        child = NavigationItemModel(
            identifier="child",
            name="Child",
            description="Child destination",
            icon=NavigationIcon.SETTINGS,
            order=20,
            permission=Permission("navigation.child"),
            group=NavigationGroup.GENERAL,
            parent_identifier="parent",
        )
        with self.assertRaises(ValueError):
            registry.register(NavigationRegistration(child, lambda: QLabel("child")))
        registry.register(_registration("parent"))
        registry.register(NavigationRegistration(child, lambda: QLabel("child")))
        with self.assertRaises(ValueError):
            registry.unregister("parent")

    def test_batch_registration_is_atomic(self) -> None:
        registry = NavigationRegistry()
        orphan = NavigationItemModel(
            identifier="orphan",
            name="Orphan",
            description="Invalid child",
            icon=NavigationIcon.SETTINGS,
            order=20,
            permission=Permission("navigation.orphan"),
            group=NavigationGroup.GENERAL,
            parent_identifier="missing",
        )
        with self.assertRaises(ValueError):
            registry.register_many(
                (
                    _registration("valid"),
                    NavigationRegistration(orphan, lambda: QLabel("orphan")),
                )
            )
        self.assertEqual(len(registry), 0)

    def test_batch_registration_rejects_parent_cycle(self) -> None:
        registry = NavigationRegistry()
        first = NavigationItemModel(
            identifier="first",
            name="First",
            description="First child",
            icon=NavigationIcon.SETTINGS,
            order=10,
            permission=Permission("navigation.first"),
            group=NavigationGroup.GENERAL,
            parent_identifier="second",
        )
        second = NavigationItemModel(
            identifier="second",
            name="Second",
            description="Second child",
            icon=NavigationIcon.SETTINGS,
            order=20,
            permission=Permission("navigation.second"),
            group=NavigationGroup.GENERAL,
            parent_identifier="first",
        )
        with self.assertRaises(ValueError):
            registry.register_many(
                (
                    NavigationRegistration(first, lambda: QLabel("first")),
                    NavigationRegistration(second, lambda: QLabel("second")),
                )
            )
        self.assertEqual(len(registry), 0)

    def test_listener_failure_does_not_invalidate_mutation(self) -> None:
        registry = NavigationRegistry()
        captured: list[str] = []

        def fail_listener(change: object) -> None:
            raise RuntimeError("observer failed")

        registry.subscribe(fail_listener)
        registry.subscribe(lambda change: captured.append(change.identifier))
        registry.register(_registration("dashboard"))
        self.assertTrue(registry.contains("dashboard"))
        self.assertEqual(captured, ["dashboard"])


class NavigationServiceTests(unittest.TestCase):
    """Verify Security Foundation authorization integration."""

    def test_authenticated_identity_requires_navigation_permission(self) -> None:
        events = EventBus()
        security = SecurityManager.create(events)
        registry = NavigationRegistry()
        registry.register(_registration("dashboard"))
        service = NavigationService(registry, security.permissions)
        self.assertEqual(service.destinations("operator"), ())
        permission = registry.get("dashboard").item.permission
        security.permissions.define_role("desktop-user", (permission,))
        security.permissions.assign_role("operator", "desktop-user")
        self.assertEqual(
            tuple(item.identifier for item in service.destinations("operator")),
            ("dashboard",),
        )


class NavigationControllerTests(QtTestCase):
    """Verify routing, module retention, and history."""

    def setUp(self) -> None:
        self.events = EventBus()
        registry = NavigationRegistry()
        registry.register(_registration("dashboard", 10))
        registry.register(_registration("chat", 20))
        self.navigation = NavigationService(registry)
        self.host = ModuleHost(self.navigation, self.events)
        self.controller = NavigationController(
            self.navigation,
            self.host,
            self.events,
            default_identifier="dashboard",
        )

    def test_default_navigation_and_module_memory(self) -> None:
        self.controller.start()
        first_dashboard = self.host.module("dashboard")
        self.controller.navigate("chat")
        self.controller.back()
        self.assertIs(self.host.module("dashboard"), first_dashboard)
        self.assertEqual(self.host.loaded_identifiers(), ("dashboard", "chat"))
        self.assertEqual(self.controller.current_identifier, "dashboard")

    def test_back_forward_and_branching_history(self) -> None:
        self.controller.start()
        self.controller.navigate("chat")
        self.assertTrue(self.controller.back())
        self.assertTrue(self.controller.forward())
        self.assertEqual(self.controller.history, ("dashboard", "chat"))
        self.assertFalse(self.controller.forward())

    def test_unknown_route_does_not_corrupt_history(self) -> None:
        self.controller.start()
        with self.assertRaises(LookupError):
            self.controller.navigate("missing")
        self.assertEqual(self.controller.history, ("dashboard",))

    def test_factory_failure_does_not_corrupt_history(self) -> None:
        def fail() -> QLabel:
            raise RuntimeError("factory failed")

        self.navigation.registry.register(
            NavigationRegistration(_item("broken", 30), fail)
        )
        self.controller.start()
        with self.assertRaises(RuntimeError):
            self.controller.navigate("broken")
        self.assertEqual(self.controller.history, ("dashboard",))
        self.assertEqual(self.controller.current_identifier, "dashboard")

    def test_deactivate_hides_active_module(self) -> None:
        self.controller.start()
        active = self.host.currentWidget()
        self.host.deactivate()
        self.assertIsNone(self.host.active_identifier)
        self.assertIsNot(self.host.currentWidget(), active)

    def test_event_subscriber_failure_does_not_corrupt_navigation(self) -> None:
        def fail_on_event(event: object) -> None:
            raise RuntimeError("subscriber failed")

        self.events.subscribe("navigation.module.activated", fail_on_event)
        self.controller.start()
        self.controller.navigate("chat")
        self.assertEqual(self.controller.current_identifier, "chat")
        self.assertEqual(self.controller.history, ("dashboard", "chat"))

    def test_unregister_active_route_returns_to_default_and_releases_module(self) -> None:
        changed: list[dict[str, object]] = []
        self.events.subscribe(
            str(NavigationEventName.NAVIGATION_CHANGED),
            lambda event: changed.append(event.payload),
        )
        self.controller.start()
        self.controller.navigate("chat")
        previous_chat = self.host.module("chat")
        self.navigation.registry.unregister("chat")
        self.assertEqual(self.controller.current_identifier, "dashboard")
        self.assertEqual(self.controller.history, ("dashboard",))
        self.assertIsNone(self.host.module("chat"))
        self.assertEqual(
            changed[-1],
            {"previous": "chat", "current": "dashboard"},
        )
        self.navigation.registry.register(_registration("chat", 20))
        self.controller.navigate("chat")
        self.assertIsNot(self.host.module("chat"), previous_chat)


class SidebarTests(QtTestCase):
    """Verify route rendering, active state, and collapse events."""

    def test_sidebar_renders_and_collapses(self) -> None:
        events = EventBus()
        captured: list[str] = []
        events.subscribe("navigation.sidebar.*", lambda event: captured.append(event.name))
        registry = NavigationRegistry()
        registry.register(_registration("dashboard"))
        sidebar = Sidebar(NavigationService(registry), events)
        self.assertEqual(len(sidebar.findChildren(NavigationItem)), 1)
        sidebar.set_active("dashboard")
        self.assertTrue(sidebar.findChildren(NavigationItem)[0].isChecked())
        sidebar.set_collapsed(True)
        sidebar.set_collapsed(False)
        self.assertEqual(
            captured,
            [
                str(NavigationEventName.SIDEBAR_COLLAPSED),
                str(NavigationEventName.SIDEBAR_EXPANDED),
            ],
        )

    def test_sidebar_updates_after_dynamic_registration(self) -> None:
        events = EventBus()
        registry = NavigationRegistry()
        registry.register(_registration("dashboard"))
        sidebar = Sidebar(NavigationService(registry), events)
        registry.register(_registration("chat", 20))
        self.assertEqual(
            tuple(
                item.identifier
                for item in sidebar.findChildren(NavigationItem)
            ),
            ("dashboard", "chat"),
        )
        registry.unregister("chat")
        self.assertEqual(
            tuple(
                item.identifier
                for item in sidebar.findChildren(NavigationItem)
            ),
            ("dashboard",),
        )


class ThemeManagerTests(QtTestCase):
    """Verify existing configuration and ThemeEngine integration."""

    def test_theme_change_persists_applies_and_emits(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            default_path = root / "default.toml"
            profile_path = root / "profile.toml"
            default_path.write_text(_DEFAULT_CONFIG, encoding="utf-8")
            configuration = ConfigurationService(default_path, profile_path)
            settings = ApplicationSettings(
                name="JOCHEN X",
                version="0.6.0",
                log_level="INFO",
                theme_mode=ThemeMode.DARK,
                database_path="data/test.sqlite3",
                plugin_directory="plugins",
            )
            events = EventBus()
            modes: list[str] = []
            events.subscribe(
                "application.theme.changed",
                lambda event: modes.append(str(event.payload["mode"])),
            )
            manager = ThemeManager(
                self.application,
                ThemeEngine(),
                configuration,
                settings,
                events,
            )
            manager.set_mode(ThemeMode.LIGHT)
            self.assertIs(manager.current_mode, ThemeMode.LIGHT)
            self.assertTrue(profile_path.exists())
            self.assertIn("QFrame#navigationSidebar", self.application.styleSheet())
            self.assertEqual(modes, ["light"])


class LayoutAndWindowStateTests(QtTestCase):
    """Verify responsive layout and window persistence."""

    def test_layout_collapses_and_window_state_round_trips(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            events = EventBus()
            registry = NavigationRegistry()
            registry.register(_registration("dashboard"))
            navigation = NavigationService(registry)
            window = QMainWindow()
            sidebar = Sidebar(navigation, events)
            module_host = ModuleHost(navigation, events)
            layout = LayoutManager(window, sidebar, module_host)
            layout.update_for_width(800)
            self.assertTrue(sidebar.is_collapsed)
            layout.update_for_width(1200)
            self.assertFalse(sidebar.is_collapsed)
            settings = QSettings(
                str(Path(directory) / "window.ini"),
                QSettings.Format.IniFormat,
            )
            state = WindowState(settings, events, layout)
            window.resize(1100, 700)
            state.save(window)
            self.assertTrue(state.restore(window))


class StatusBarTests(QtTestCase):
    """Verify all required subsystem indicators."""

    def test_status_bar_displays_foundation_health(self) -> None:
        events = EventBus()
        security = SecurityManager.create(events)
        security.initialize()
        try:
            status = StatusBar(
                events,
                application_status="ready",
                security=security,
                worker_count=lambda: 2,
                plugin_count=3,
            )
            self.assertEqual(status.subsystem_status("application"), "Application: ready")
            self.assertEqual(status.subsystem_status("security"), "Security: Ready")
            self.assertEqual(status.subsystem_status("workers"), "Workers: 2 active")
            self.assertEqual(status.subsystem_status("plugins"), "Plugins: 3 discovered")
            status.dispose()
        finally:
            security.dispose()


class MainWindowIntegrationTests(QtTestCase):
    """Verify desktop composition against the real host and Security Foundation."""

    def test_host_exposes_navigation_security_and_main_window(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            root = _make_project_root(directory)
            host = ApplicationHost(
                root,
                bootstrap_manager=create_desktop_bootstrap_manager(),
                worker_pool=WorkerPool(max_workers=1),
            )
            try:
                context = host.start()
                security = context.services.get(SecurityManager)
                self.assertTrue(security.is_initialized)
                self.assertIsInstance(
                    context.services.get(NavigationService),
                    NavigationService,
                )
                self.assertEqual(context.services.get(PluginCatalog).count, 0)
                settings = QSettings(
                    str(root / "window.ini"),
                    QSettings.Format.IniFormat,
                )
                window = MainWindow(context, host.workers, settings=settings)
                self.assertEqual(
                    window.navigation_controller.current_identifier,
                    "dashboard",
                )
                self.assertTrue(
                    any(
                        event.name == str(NavigationEventName.DASHBOARD_LOADED)
                        for event in context.events.history()
                    )
                )
                self.assertEqual(len(window.sidebar.findChildren(NavigationItem)), 9)
                window.navigation_controller.navigate("plugins")
                self.assertEqual(window.module_host.active_identifier, "plugins")
                self.assertEqual(host.state, ApplicationState.READY)
                window.close()
                second_window = MainWindow(context, host.workers, settings=settings)
                self.assertEqual(
                    second_window.navigation_controller.current_identifier,
                    "dashboard",
                )
                second_window.close()
                host.shutdown()
                self.assertFalse(security.is_initialized)
            finally:
                if host.state is not ApplicationState.SHUTDOWN:
                    host.shutdown()
                _reset_application_logging()


if __name__ == "__main__":
    unittest.main()
