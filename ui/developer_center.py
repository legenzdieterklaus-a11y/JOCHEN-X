"""Small optional Developer Center view; instantiate only when diagnostics are enabled."""

from PySide6.QtWidgets import QLabel, QTabWidget, QVBoxLayout, QWidget


class DeveloperCenter(QWidget):
    def __init__(self, summary: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        tabs = QTabWidget(self)
        for name in (
            "Overview",
            "Logs",
            "Events",
            "Services",
            "Performance",
            "Plugins",
            "Configuration",
            "Architecture",
            "Health",
        ):
            page = QWidget(tabs)
            page_layout = QVBoxLayout(page)
            page_layout.addWidget(QLabel("Loaded on demand", page))
            tabs.addTab(page, name)
        layout.addWidget(QLabel(summary, self))
        layout.addWidget(tabs)
