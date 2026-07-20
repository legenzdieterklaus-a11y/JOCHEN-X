from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from ui.chat_bubble import ChatBubble


class MessageWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(8)
        self.layout.addStretch()

    def add_message(self, text, sender="assistant", timestamp=""):

        bubble = ChatBubble(
            text=text,
            sender=sender,
            timestamp=timestamp,
        )

        self.layout.insertWidget(
            self.layout.count() - 1,
            bubble,
        )

        return bubble

    def clear_messages(self):

        while self.layout.count() > 1:

            item = self.layout.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()