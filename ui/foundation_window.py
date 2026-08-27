"""Minimal desktop shell for the foundation lifecycle."""

from PySide6.QtWidgets import QLabel, QMainWindow, QStatusBar, QTabWidget, QVBoxLayout, QWidget


class FoundationWindow(QMainWindow):
    """Displays initialized foundation status without exposing product features."""
    def __init__(
        self, application_name: str, version: str, developer_center: QWidget | None = None
    ) -> None:
        super().__init__()
        self.setWindowTitle(f"{application_name} {version}")
        self.resize(960, 640)
        content = QWidget(self)
        layout = QVBoxLayout(content)
        title = QLabel(application_name, content)
        title.setObjectName("title")
        subtitle = QLabel("Foundation initialized", content)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        if developer_center is None:
            self.setCentralWidget(content)
        else:
            tabs = QTabWidget(self)
            tabs.addTab(content, "Application")
            tabs.addTab(developer_center, "Developer Center")
            self.setCentralWidget(tabs)
        status = QStatusBar(self)
        status.showMessage("Ready")
        self.setStatusBar(status)
