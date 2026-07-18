from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QTextEdit,
    QPushButton,
    QLineEdit,
    QHBoxLayout,
    QVBoxLayout,
)

from ui.sidebar import Sidebar
from ui.dashboard import Dashboard
from ui.status_bar import StatusBar

from core.worker import WorkerThread


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("JOCHEN X v0.2 Professional")

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

        self.chat = QTextEdit()

        self.chat.setReadOnly(True)

        self.chat.append("🤖 Willkommen bei JOCHEN X")

        self.chat.append("")

        self.chat.append("System erfolgreich gestartet.")

        self.chat.append("")

        self.right_layout.addWidget(self.chat)

        ####################################################
        # Eingabe
        ####################################################

        bottom = QHBoxLayout()

        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "Schreibe eine Nachricht..."
        )

        self.input.returnPressed.connect(
            self.send_message
        )

        self.send_button = QPushButton("Senden")

        self.send_button.clicked.connect(
            self.send_message
        )

        self.send_button.setMinimumHeight(42)

        bottom.addWidget(self.input)

        bottom.addWidget(self.send_button)

        self.right_layout.addLayout(bottom)

        ####################################################
        # Statusbar
        ####################################################

        self.status = StatusBar()

        self.setStatusBar(self.status)

        ####################################################
        # Thread

        self.worker = None

        ####################################################
    # Nachricht senden
    ####################################################

    def send_message(self):

        prompt = self.input.text().strip()

        if not prompt:
            return

        # Nachricht anzeigen
        self.chat.append(f"\n🧑 Du:\n{prompt}\n")

        # Eingabe sperren
        self.input.setEnabled(False)
        self.send_button.setEnabled(False)

        # Status
        self.status.set_status("🟡 JOCHEN denkt...")

        # Eingabefeld leeren
        self.input.clear()

        # Worker starten
        self.worker = WorkerThread(prompt)

        self.worker.finished.connect(self.receive_answer)
        self.worker.error.connect(self.show_error)

        self.worker.start()

    ####################################################
    # Antwort erhalten
    ####################################################

    def receive_answer(self, answer):

        self.chat.append(f"\n🤖 JOCHEN:\n{answer}\n")

        # Eingabe wieder freigeben
        self.input.setEnabled(True)
        self.send_button.setEnabled(True)

        self.input.setFocus()

        # Nach unten scrollen
        scrollbar = self.chat.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

        # Status zurücksetzen
        self.status.set_status("🟢 Bereit")

    ####################################################
    # Fehler anzeigen
    ####################################################

    def show_error(self, error):

        self.chat.append(f"\n❌ Fehler:\n{error}\n")

        self.input.setEnabled(True)
        self.send_button.setEnabled(True)

        self.input.setFocus()

        self.status.set_status("🔴 Fehler")    