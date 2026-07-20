from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
)

from ui.message_widget import MessageWidget


class ChatPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.messages = MessageWidget()

        self.scroll.setWidget(self.messages)

        layout.addWidget(self.scroll)

    def add_user_message(self, text, timestamp=""):

        bubble = self.messages.add_message(
            text=text,
            sender="user",
            timestamp=timestamp,
        )

        self.scroll_to_bottom()

        return bubble

    def add_ai_message(self, text, timestamp=""):

        bubble = self.messages.add_message(
            text=text,
            sender="assistant",
            timestamp=timestamp,
        )

        self.scroll_to_bottom()

        return bubble

    def scroll_to_bottom(self):

        scrollbar = self.scroll.verticalScrollBar()

        scrollbar.setValue(
            scrollbar.maximum()
        )

    def clear(self):

        self.messages.clear_messages()