from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("🏠 Dashboard")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            margin-bottom:20px;
        """)

        info = QFrame()
        info.setStyleSheet("""
            QFrame{
                background:#252526;
                border-radius:12px;
                padding:15px;
            }
        """)

        info_layout = QVBoxLayout(info)

        self.model = QLabel("🤖 Modell: qwen3")
        self.ollama = QLabel("🟢 Ollama: Verbunden")
        self.memory = QLabel("🧠 Memory: Noch nicht aktiv")
        self.version = QLabel("🚀 Version: Genesis 0.2")

        info_layout.addWidget(self.model)
        info_layout.addWidget(self.ollama)
        info_layout.addWidget(self.memory)
        info_layout.addWidget(self.version)

        layout.addWidget(title)
        layout.addWidget(info)
        layout.addStretch()