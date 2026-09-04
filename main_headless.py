"""JOCHEN X headless entry point — no window, no display required.

Starts the application core with monitoring, persistence, and the plugin
pipeline but without any UI.  Designed for unattended operation as a Windows
scheduled task running in session 0 (no user logged in).

Requires PySide6 (for QCoreApplication and QThreadPool) but never creates a
window or imports QtWidgets.
"""

from __future__ import annotations

import logging
import signal
import sys
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QTimer

from app.application_host import ApplicationHost
from services.headless import create_headless_bootstrap_manager

__all__: list[str] = []

_log = logging.getLogger("jochen_x")


def main() -> int:
    """Start the headless application and block until terminated."""
    app = QCoreApplication(sys.argv)

    host = ApplicationHost(
        Path(__file__).resolve().parent,
        bootstrap_manager=create_headless_bootstrap_manager(),
    )

    def request_quit(_signum: int = 0, _frame: object = None) -> None:
        app.quit()

    signal.signal(signal.SIGINT, request_quit)
    signal.signal(signal.SIGTERM, request_quit)
    if hasattr(signal, "SIGBREAK"):
        signal.signal(signal.SIGBREAK, request_quit)

    host.start()
    _log.info("headless.running")

    # Periodischer Leerlauf-Timer: gibt der Qt-Ereignisschleife regelmäßig die
    # Kontrolle zurück, damit Python-Signalbehandler laufen — ohne ihn wird
    # SIGTERM nie verarbeitet.
    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(1000)

    exit_code = app.exec()
    host.shutdown(exit_code=exit_code)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
