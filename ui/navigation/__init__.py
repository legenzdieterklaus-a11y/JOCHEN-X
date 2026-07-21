"""Public surface for the JOCHEN X desktop navigation framework."""

from ui.navigation.dashboard_page import DashboardPage
from ui.navigation.layout_manager import LayoutManager
from ui.navigation.main_window import MainWindow
from ui.navigation.module_host import ModuleHost, ModulePlaceholder
from ui.navigation.navigation_controller import NavigationController
from ui.navigation.navigation_events import (
    DashboardLoaded,
    ModuleActivated,
    ModuleDeactivated,
    NavigationChanged,
    NavigationEventName,
    SidebarCollapsed,
    SidebarExpanded,
    ThemeChanged,
    WindowStateChanged,
)
from ui.navigation.navigation_item import NavigationItem
from ui.navigation.navigation_models import (
    NavigationGroup,
    NavigationIcon,
    NavigationId,
    NavigationItemModel,
    NavigationRegistration,
)
from ui.navigation.navigation_registry import NavigationRegistry
from ui.navigation.navigation_service import (
    NavigationBootstrapStage,
    NavigationComposition,
    NavigationService,
    NavigationServicePort,
    create_desktop_bootstrap_manager,
)
from ui.navigation.sidebar import Sidebar
from ui.navigation.sidebar_section import SidebarSection
from ui.navigation.status_bar import StatusBar
from ui.navigation.theme_manager import ThemeManager
from ui.navigation.toolbar import Toolbar
from ui.navigation.window_state import WindowState

__all__ = [
    "DashboardLoaded",
    "DashboardPage",
    "LayoutManager",
    "MainWindow",
    "ModuleActivated",
    "ModuleDeactivated",
    "ModuleHost",
    "ModulePlaceholder",
    "NavigationBootstrapStage",
    "NavigationChanged",
    "NavigationComposition",
    "NavigationController",
    "NavigationEventName",
    "NavigationGroup",
    "NavigationIcon",
    "NavigationId",
    "NavigationItem",
    "NavigationItemModel",
    "NavigationRegistration",
    "NavigationRegistry",
    "NavigationService",
    "NavigationServicePort",
    "Sidebar",
    "SidebarCollapsed",
    "SidebarExpanded",
    "SidebarSection",
    "StatusBar",
    "ThemeChanged",
    "ThemeManager",
    "Toolbar",
    "WindowState",
    "WindowStateChanged",
    "create_desktop_bootstrap_manager",
]
