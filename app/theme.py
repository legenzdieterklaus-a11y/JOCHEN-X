from PySide6.QtWidgets import QApplication


DARK_THEME = """
QMainWindow {
    background-color: #1E1E1E;
}

QWidget {
    background-color: #1E1E1E;
    color: #EAEAEA;
    font-family: Segoe UI;
    font-size: 10pt;
}

QLabel {
    color: #FFFFFF;
}

QLineEdit {
    background-color: #2B2B2B;
    border: 1px solid #3A3A3A;
    border-radius: 8px;
    padding: 8px;
    color: white;
}

QTextEdit {
    background-color: #252526;
    border: 1px solid #3A3A3A;
    border-radius: 8px;
    padding: 8px;
    color: white;
}

QPushButton {
    background-color: #007ACC;
    border: none;
    border-radius: 8px;
    color: white;
    padding: 10px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1894E8;
}

QPushButton:pressed {
    background-color: #005A9E;
}

QListWidget {
    background-color: #252526;
    border: none;
    outline: none;
}

QListWidget::item {
    padding: 12px;
    border-radius: 8px;
    margin: 4px;
}

QListWidget::item:selected {
    background-color: #007ACC;
    color: white;
}

QListWidget::item:hover {
    background-color: #323233;
}

QStatusBar {
    background-color: #252526;
    color: white;
}
"""


def apply_theme(app: QApplication):
    app.setStyleSheet(DARK_THEME)