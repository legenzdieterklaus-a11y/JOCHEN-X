from PySide6.QtWidgets import QLabel, QStatusBar


class StatusBar(QStatusBar):

    def __init__(self):
        super().__init__()

        self.status = QLabel("🟢 Bereit")
        self.model = QLabel(" | Modell: qwen3")
        self.connection = QLabel(" | Ollama: Verbunden")

        self.addWidget(self.status)
        self.addPermanentWidget(self.model)
        self.addPermanentWidget(self.connection)

    def set_status(self, text):
        self.status.setText(text)