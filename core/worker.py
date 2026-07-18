from PySide6.QtCore import QObject, QThread, Signal

from core.ai_manager import AIManager


class AIWorker(QObject):
    """
    Führt KI-Anfragen in einem separaten Thread aus,
    damit die Oberfläche nicht einfriert.
    """

    finished = Signal(str)
    error = Signal(str)

    def __init__(self, prompt: str):
        super().__init__()

        self.prompt = prompt
        self.ai = AIManager()

    def run(self):

        try:

            answer = self.ai.ask(self.prompt)

            self.finished.emit(answer)

        except Exception as e:

            self.error.emit(str(e))


class WorkerThread(QThread):

    finished = Signal(str)
    error = Signal(str)

    def __init__(self, prompt: str):
        super().__init__()

        self.worker = AIWorker(prompt)

        self.worker.moveToThread(self)

        self.started.connect(self.worker.run)

        self.worker.finished.connect(self.finished)

        self.worker.error.connect(self.error)

        self.worker.finished.connect(self.quit)
        self.worker.error.connect(self.quit)