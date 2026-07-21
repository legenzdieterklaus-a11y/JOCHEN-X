"""Grouped section used by the application sidebar."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.navigation.navigation_item import NavigationItem
from ui.navigation.navigation_models import NavigationItemModel


class SidebarSection(QWidget):
    """Displays a named group of navigation item widgets."""

    def __init__(
        self,
        title: str,
        items: tuple[NavigationItemModel, ...],
        on_requested: Callable[[str], None],
        parent: QWidget | None = None,
    ) -> None:
        """Create a section and connect item activation."""
        super().__init__(parent)
        self.setObjectName("sidebarSection")
        self._heading = QLabel(title, self)
        self._heading.setObjectName("sidebarSectionTitle")
        self._items: dict[str, NavigationItem] = {}
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(3)
        layout.addWidget(self._heading)
        for model in items:
            item = NavigationItem(model, self)
            item.clicked.connect(
                lambda checked=False, identifier=model.identifier: on_requested(identifier)
            )
            layout.addWidget(item)
            self._items[model.identifier] = item

    def set_active(self, identifier: str) -> None:
        """Set the active item when it belongs to this section."""
        for item_identifier, item in self._items.items():
            item.set_active(item_identifier == identifier)

    def set_collapsed(self, collapsed: bool) -> None:
        """Apply compact presentation to the section."""
        self._heading.setVisible(not collapsed)
        for item in self._items.values():
            item.set_collapsed(collapsed)

    def item(self, identifier: str) -> NavigationItem | None:
        """Return an item widget by identifier."""
        return self._items.get(identifier)
