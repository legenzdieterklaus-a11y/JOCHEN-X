from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
)

from ui.sidebar import Sidebar
from ui.dashboard import Dashboard
from ui.status_bar import StatusBar
from ui.chat_page import ChatPage
from ui.input_bar import InputBar

from core.worker import WorkerThread


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("JOCHEN X v0.3")

        self.resize(1600, 900)

        ####################################################
        # Zentrales Widget
        ####################################################

        central = QWidget()

        self.setCentralWidget(central)

        self.main_layout = QHBoxLayout()

        central.setLayout(self.main_layout)

        ####################################################
        # Sidebar
        ####################################################

        self.sidebar = Sidebar()

        self.main_layout.addWidget(self.sidebar)

        ####################################################
        # Rechte Seite
        ####################################################

        self.right_layout = QVBoxLayout()

        self.main_layout.addLayout(self.right_layout)

        ####################################################
        # Dashboard
        ####################################################

        self.dashboard = Dashboard()

        self.right_layout.addWidget(self.dashboard)

        ####################################################
        # Chat
        ####################################################

        self.chat = ChatPage()

        self.right_layout.addWidget(self.chat)

        self.chat.add_ai_message(
            "👋 Willkommen bei JOCHEN X",
            "System"
        )

        self.chat.add_ai_message(
            "System erfolgreich gestartet.",
            ""
        )

        ####################################################
        # Eingabe
        ####################################################

        self.input_bar = InputBar()

        self.right_layout.addWidget(self.input_bar)

        self.input_bar.send_button.clicked.connect(
            self.send_message
        )

        self.input_bar.input.returnPressed.connect(
            self.send_message
        )

        ####################################################
        # StatusBar
        ####################################################

        self.status = StatusBar()

        self.setStatusBar(self.status)

        ####################################################
        # Worker
        ####################################################

        self.worker = None
          ####################################################
    # Nachricht senden
    ####################################################

    def send_message(self):

        prompt = self.input_bar.text().strip()

        if not prompt:
            return

        self.chat.add_user_message(prompt)

        self.input_bar.set_enabled(False)

        self.status.set_status("🟡 JOCHEN denkt...")

        self.input_bar.clear()

        self.worker = WorkerThread(prompt)

        self.worker.finished.connect(
            self.receive_answer
        )

        self.worker.error.connect(
            self.show_error
        )

        self.worker.start()

    ####################################################
    # Antwort erhalten
    ####################################################

    def receive_answer(self, answer):

        self.chat.add_ai_message(answer)

        self.input_bar.set_enabled(True)

        self.input_bar.focus()

        self.status.set_status("🟢 Bereit")

    ####################################################
    # Fehler anzeigen
    ####################################################

    def show_error(self, error):

        self.chat.add_ai_message(
            f"❌ Fehler:\n{error}"
        )

        self.input_bar.set_enabled(True)

        self.input_bar.focus()

        self.status.set_status("🔴 Fehler")  