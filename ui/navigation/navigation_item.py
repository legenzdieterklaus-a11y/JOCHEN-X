"""Presentation widget for one navigation destination."""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QPushButton, QStyle, QWidget

from ui.navigation.navigation_models import NavigationIcon, NavigationItemModel


_STANDARD_ICONS: dict[NavigationIcon, QStyle.StandardPixmap] = {
    NavigationIcon.DASHBOARD: QStyle.StandardPixmap.SP_ComputerIcon,
    NavigationIcon.CHAT: QStyle.StandardPixmap.SP_MessageBoxInformation,
    NavigationIcon.TRADING: QStyle.StandardPixmap.SP_ArrowUp,
    NavigationIcon.AI: QStyle.StandardPixmap.SP_DriveNetIcon,
    NavigationIcon.MARKETPLACE: QStyle.StandardPixmap.SP_DirHomeIcon,
    NavigationIcon.PLUGIN: QStyle.StandardPixmap.SP_FileDialogDetailedView,
    NavigationIcon.DEVELOPER: QStyle.StandardPixmap.SP_DesktopIcon,
    NavigationIcon.ANALYTICS: QStyle.StandardPixmap.SP_FileDialogListView,
    NavigationIcon.SETTINGS: QStyle.StandardPixmap.SP_FileDialogContentsView,
}


class NavigationItem(QPushButton):
    """Checkable, collapsible button bound to immutable route metadata."""

    def __init__(self, model: NavigationItemModel, parent: QWidget | None = None) -> None:
        """Create a navigation button for ``model``."""
        super().__init__(model.name, parent)
        self._model = model
        self.setObjectName("navigationItem")
        self.setProperty("navigationId", model.identifier)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(f"{model.name}\n{model.description}")
        self.setAccessibleName(model.name)
        self.setEnabled(model.enabled)
        self.setIcon(self.style().standardIcon(_STANDARD_ICONS[model.icon]))
        self.setIconSize(QSize(20, 20))
        if model.parent_identifier is not None:
            self.setProperty("childItem", True)

    @property
    def identifier(self) -> str:
        """Return the destination identifier."""
        return self._model.identifier

    def set_active(self, active: bool) -> None:
        """Update active visual state."""
        self.setChecked(active)

    def set_collapsed(self, collapsed: bool) -> None:
        """Show only the icon in compact sidebar mode."""
        self.setText("" if collapsed else self._model.name)
        self.setProperty("collapsed", collapsed)
