"""JOCHEN X executable entry point."""

from pathlib import Path

from app.application import Application
from app.application_host import ApplicationHost
from app.context import ApplicationContext
from ui.navigation.main_window import MainWindow
from ui.navigation.navigation_service import create_desktop_bootstrap_manager


def main() -> int:
    """Start the desktop application and return its exit code."""
    host = ApplicationHost(
        Path(__file__).resolve().parent,
        bootstrap_manager=create_desktop_bootstrap_manager(),
    )

    def create_window(context: ApplicationContext) -> MainWindow:
        """Create the injected desktop shell for the ready application."""
        return MainWindow(context, host.workers)

    return Application(host, window_factory=create_window).run()


if __name__ == "__main__":
    raise SystemExit(main())
