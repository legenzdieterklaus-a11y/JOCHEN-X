"""Responsive central-layout coordinator with dock-widget preparation."""

from __future__ import annotations

from PySide6.QtCore import QByteArray, Qt
from PySide6.QtWidgets import QMainWindow, QSplitter, QWidget

from ui.navigation.module_host import ModuleHost
from ui.navigation.sidebar import Sidebar

_RESPONSIVE_COLLAPSE_WIDTH = 980
_SIDEBAR_STRETCH = 0
_CONTENT_STRETCH = 1


class LayoutManager:
    """Owns window composition and responsive sidebar behavior."""

    def __init__(
        self,
        window: QMainWindow,
        sidebar: Sidebar,
        module_host: ModuleHost,
    ) -> None:
        """Compose the main splitter and configure future docking support."""
        self._window = window
        self._sidebar = sidebar
        self._module_host = module_host
        self._splitter = QSplitter(Qt.Orientation.Horizontal, window)
        self._splitter.setObjectName("mainSplitter")
        self._splitter.setChildrenCollapsible(False)
        self._splitter.addWidget(sidebar)
        self._splitter.addWidget(module_host)
        self._splitter.setStretchFactor(0, _SIDEBAR_STRETCH)
        self._splitter.setStretchFactor(1, _CONTENT_STRETCH)
        window.setCentralWidget(self._splitter)
        window.setDockNestingEnabled(True)
        window.setDockOptions(
            QMainWindow.DockOption.AllowNestedDocks
            | QMainWindow.DockOption.AllowTabbedDocks
            | QMainWindow.DockOption.AnimatedDocks
        )
        self._narrow: bool | None = None

    @property
    def central_widget(self) -> QWidget:
        """Return the managed splitter."""
        return self._splitter

    @property
    def is_narrow(self) -> bool:
        """Return whether the most recent width is in compact range."""
        return bool(self._narrow)

    def update_for_width(self, width: int) -> None:
        """Apply responsive presentation when the breakpoint changes."""
        narrow = width < _RESPONSIVE_COLLAPSE_WIDTH
        if narrow == self._narrow:
            return
        self._narrow = narrow
        self._sidebar.set_collapsed(narrow)

    def save_state(self) -> QByteArray:
        """Return splitter state suitable for persistence."""
        return self._splitter.saveState()

    def restore_state(self, state: QByteArray) -> bool:
        """Restore a previously saved splitter state."""
        if state.isEmpty():
            return False
        return self._splitter.restoreState(state)
