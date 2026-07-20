from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)


class InputBar(QWidget):

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Schreibe eine Nachricht...")

        self.send_button = QPushButton("Senden")
        self.send_button.setMinimumHeight(42)

        layout.addWidget(self.input)
        layout.addWidget(self.send_button)

    def text(self):
        return self.input.text()

    def clear(self):
        self.input.clear()

    def set_enabled(self, enabled: bool):
        self.input.setEnabled(enabled)
        self.send_button.setEnabled(enabled)

    def focus(self):
        self.input.setFocus()