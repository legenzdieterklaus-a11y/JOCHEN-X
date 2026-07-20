from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)


class ChatBubble(QFrame):

    def __init__(self, text="", sender="assistant", timestamp=""):
        super().__init__()

        self.setMaximumWidth(700)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        bubble = QFrame()
        bubble.setMaximumWidth(600)

        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.setContentsMargins(15, 10, 15, 10)

        self.message = QLabel(text)
        self.message.setWordWrap(True)
        self.message.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        self.time = QLabel(timestamp)
        self.time.setAlignment(Qt.AlignRight)

        bubble_layout.addWidget(self.message)
        bubble_layout.addWidget(self.time)

        if sender == "user":

            layout.addStretch()
            layout.addWidget(bubble)

            bubble.setStyleSheet("""
                QFrame{
                    background:#2d7df6;
                    border-radius:16px;
                }

                QLabel{
                    color:white;
                    font-size:13px;
                }
            """)

        else:

            layout.addWidget(bubble)
            layout.addStretch()

            bubble.setStyleSheet("""
                QFrame{
                    background:#353535;
                    border-radius:16px;
                }

                QLabel{
                    color:white;
                    font-size:13px;
                }
            """)

    def set_text(self, text):
        self.message.setText(text)

    def append_text(self, text):
        self.message.setText(self.message.text() + text)

    def set_timestamp(self, timestamp):
        self.time.setText(timestamp)