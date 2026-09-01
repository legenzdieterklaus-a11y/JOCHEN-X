"""Production desktop main window composed from foundation services."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QSettings
from PySide6.QtGui import QCloseEvent, QResizeEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from app.concurrency import WorkerPool
from app.context import ApplicationContext
from app.security import Permission, SecurityManager
from plugins.loader import PluginCatalog
from services.monitoring import MonitoringStateCollector
from ui.chat_page import ChatPage
from ui.monitoring_page import MonitoringPage
from ui.navigation.dashboard_page import DashboardPage
from ui.navigation.layout_manager import LayoutManager
from ui.navigation.module_host import ModuleHost, ModulePlaceholder
from ui.navigation.navigation_controller import NavigationController
from ui.navigation.navigation_models import (
    NavigationGroup,
    NavigationIcon,
    NavigationId,
    NavigationItemModel,
    NavigationRegistration,
)
from ui.navigation.navigation_service import (
    NavigationComposition,
    NavigationService,
)
from ui.navigation.sidebar import Sidebar
from ui.navigation.status_bar import StatusBar
from ui.navigation.theme_manager import ThemeManager
from ui.navigation.toolbar import Toolbar
from ui.navigation.window_state import WindowState

_DEFAULT_WIDTH = 1440
_DEFAULT_HEIGHT = 900


class MainWindow(QMainWindow):
    """Scalable desktop shell for all current and future JOCHEN X modules."""

    def __init__(
        self,
        context: ApplicationContext,
        worker_pool: WorkerPool,
        *,
        settings: QSettings | None = None,
        parent: QWidget | None = None,
    ) -> None:
        """Compose the desktop shell from the initialized application context."""
        super().__init__(parent)
        self.setObjectName("mainWindow")
        self.setWindowTitle(f"{context.settings.name} {context.settings.version}")
        self.resize(_DEFAULT_WIDTH, _DEFAULT_HEIGHT)
        security = context.services.get_optional(SecurityManager)
        self.theme_manager = ThemeManager(
            self._application(),
            context.theme,
            context.configuration,
            context.settings,
            context.events,
            context.logger,
        )
        self.theme_manager.apply_current()
        self.navigation_service = context.services.get(NavigationService)
        plugin_catalog = context.services.get(PluginCatalog)
        context.services.get(NavigationComposition).compose(
            _builtin_registrations(
                context,
                security,
                plugin_catalog.count,
            )
        )
        self.module_host = ModuleHost(
            self.navigation_service,
            context.events,
            self,
            logger=context.logger,
        )
        self.sidebar = Sidebar(
            self.navigation_service,
            context.events,
            self,
            logger=context.logger,
        )
        self.layout_manager = LayoutManager(self, self.sidebar, self.module_host)
        self.navigation_controller = NavigationController(
            self.navigation_service,
            self.module_host,
            context.events,
            default_identifier=NavigationId.DASHBOARD.value,
            parent=self,
            logger=context.logger,
        )
        self.toolbar = Toolbar(self)
        self.addToolBar(self.toolbar)
        self.status_bar = StatusBar(
            context.events,
            application_status=context.runtime_state.state.value,
            security=security,
            worker_count=worker_pool.active_count,
            plugin_count=plugin_catalog.count,
            parent=self,
        )
        self.setStatusBar(self.status_bar)
        state_settings = settings or QSettings(
            context.settings.name,
            context.settings.name,
        )
        self.window_state = WindowState(
            state_settings,
            context.events,
            self.layout_manager,
            context.logger,
        )
        self._connect_navigation()
        self.window_state.restore(self)
        self.layout_manager.update_for_width(self.width())
        self.navigation_controller.start()

    def _connect_navigation(self) -> None:
        """Wire presentation signals to the navigation controller."""
        self.sidebar.navigation_requested.connect(self.navigation_controller.navigate)
        self.navigation_controller.navigation_changed.connect(self.sidebar.set_active)
        self.navigation_controller.history_changed.connect(self.toolbar.set_history_state)
        self.toolbar.back_action.triggered.connect(self.navigation_controller.back)
        self.toolbar.forward_action.triggered.connect(self.navigation_controller.forward)

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Update responsive layout after the window size changes."""
        super().resizeEvent(event)
        self.layout_manager.update_for_width(event.size().width())

    def closeEvent(self, event: QCloseEvent) -> None:
        """Persist window state and release event subscriptions."""
        self.window_state.save(self)
        self.status_bar.dispose()
        super().closeEvent(event)

    @staticmethod
    def _application() -> QApplication:
        """Return the existing Qt application required by the desktop shell."""
        application = QApplication.instance()
        if not isinstance(application, QApplication):
            raise RuntimeError("MainWindow requires an active QApplication")
        return application


def _builtin_registrations(
    context: ApplicationContext,
    security: SecurityManager | None,
    plugin_count: int,
) -> tuple[NavigationRegistration, ...]:
    """Build lazy registrations for dashboard, chat, and prepared modules."""
    dashboard_item = _item(
        NavigationId.DASHBOARD,
        "Dashboard",
        "Application overview and subsystem status.",
        NavigationIcon.DASHBOARD,
        10,
        NavigationGroup.GENERAL,
    )
    chat_item = _item(
        NavigationId.CHAT,
        "Chat",
        "JOCHEN X conversation workspace.",
        NavigationIcon.CHAT,
        20,
        NavigationGroup.GENERAL,
    )
    prepared = (
        _item(
            NavigationId.TRADING,
            "Trading Center",
            "Prepared workspace for future trading capabilities.",
            NavigationIcon.TRADING,
            10,
            NavigationGroup.WORKSPACE,
        ),
        _item(
            NavigationId.AI_STUDIO,
            "AI Studio",
            "Prepared workspace for future AI capabilities.",
            NavigationIcon.AI,
            20,
            NavigationGroup.WORKSPACE,
        ),
        _item(
            NavigationId.MARKETPLACE,
            "Marketplace",
            "Prepared workspace for the future marketplace.",
            NavigationIcon.MARKETPLACE,
            30,
            NavigationGroup.WORKSPACE,
        ),
        _item(
            NavigationId.PLUGINS,
            "Plugins",
            "Prepared workspace for plugin administration.",
            NavigationIcon.PLUGIN,
            10,
            NavigationGroup.PLATFORM,
        ),
        _item(
            NavigationId.DEVELOPER,
            "Developer Center",
            "Prepared workspace for developer tooling.",
            NavigationIcon.DEVELOPER,
            20,
            NavigationGroup.PLATFORM,
        ),
        _item(
            NavigationId.ANALYTICS,
            "Analytics",
            "Prepared workspace for future analytics.",
            NavigationIcon.ANALYTICS,
            30,
            NavigationGroup.PLATFORM,
        ),
        _item(
            NavigationId.SETTINGS,
            "Settings",
            "Prepared workspace for application settings.",
            NavigationIcon.SETTINGS,
            10,
            NavigationGroup.SYSTEM,
        ),
    )
    monitoring_item = _item(
        NavigationId.MONITORING,
        "Monitoring",
        "Live view of monitored subjects and their status.",
        NavigationIcon.MONITORING,
        5,
        NavigationGroup.PLATFORM,
    )
    collector = context.services.get(MonitoringStateCollector)
    registrations = [
        NavigationRegistration(
            dashboard_item,
            lambda: DashboardPage(
                context,
                security,
                plugin_count,
                context.events,
            ),
        ),
        NavigationRegistration(chat_item, ChatPage),
        NavigationRegistration(
            monitoring_item,
            lambda: MonitoringPage(collector, context.events),
        ),
    ]
    registrations.extend(
        NavigationRegistration(item, _placeholder_factory(item))
        for item in prepared
    )
    return tuple(registrations)


def _item(
    identifier: NavigationId,
    name: str,
    description: str,
    icon: NavigationIcon,
    order: int,
    group: NavigationGroup,
) -> NavigationItemModel:
    """Create built-in metadata with a stable security permission."""
    return NavigationItemModel(
        identifier=identifier.value,
        name=name,
        description=description,
        icon=icon,
        order=order,
        permission=Permission(
            f"navigation.{identifier.value}",
            f"Open the {name} module",
        ),
        group=group,
    )


def _placeholder_factory(item: NavigationItemModel) -> Callable[[], QWidget]:
    """Return a lazy factory bound to immutable item metadata."""
    return lambda: ModulePlaceholder(item.name, item.description)
