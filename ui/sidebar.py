from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget


class Sidebar(QListWidget):

    def __init__(self):
        super().__init__()

        self.setFixedWidth(230)

        self.setSpacing(5)

        self.setFocusPolicy(Qt.NoFocus)

        self.addItem("🏠 Dashboard")
        self.addItem("💬 Chat")
        self.addItem("🧠 Memory")
        self.addItem("🤖 Agenten")
        self.addItem("📁 Dateien")
        self.addItem("🔌 Plugins")
        self.addItem("⚙ Einstellungen")
        self.addItem("📋 Logs")