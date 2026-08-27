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

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)

        self.messages = MessageWidget()

        self._scroll_area.setWidget(self.messages)

        layout.addWidget(self._scroll_area)

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

        scrollbar = self._scroll_area.verticalScrollBar()

        scrollbar.setValue(
            scrollbar.maximum()
        )

    def clear(self):

        self.messages.clear_messages()