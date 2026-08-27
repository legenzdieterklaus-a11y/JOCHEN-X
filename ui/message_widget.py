from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from ui.chat_bubble import ChatBubble


class MessageWidget(QWidget):

    def __init__(self):
        super().__init__()

        self._box = QVBoxLayout(self)
        self._box.setSpacing(8)
        self._box.addStretch()

    def add_message(self, text, sender="assistant", timestamp=""):

        bubble = ChatBubble(
            text=text,
            sender=sender,
            timestamp=timestamp,
        )

        self._box.insertWidget(
            self._box.count() - 1,
            bubble,
        )

        return bubble

    def clear_messages(self):

        while self._box.count() > 1:

            item = self._box.takeAt(0)

            if item is None:
                break

            widget = item.widget()

            if widget:
                widget.deleteLater()