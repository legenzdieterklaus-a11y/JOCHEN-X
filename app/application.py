"""Top-level application object and Qt entry point.

:class:`Application` is the outermost object in the startup diagram. It owns the
Qt :class:`~PySide6.QtWidgets.QApplication`, delegates the entire lifecycle to an
:class:`app.application_host.ApplicationHost`, applies the resolved theme, and
runs the event loop. Product UI (main window, dashboard, navigation) is provided
by future layers through an injected ``window_factory`` so this foundation adds no
product surface itself.
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Sequence

from PySide6.QtWidgets import QApplication, QWidget

from app.application_host import ApplicationHost
from app.concurrency import UiDispatcher
from app.context import ApplicationContext
from app.errors import ErrorReport

WindowFactory = Callable[[ApplicationContext], QWidget]


class Application:
    """The composition entry point that runs the Qt event loop."""

    def __init__(
        self,
        host: ApplicationHost,
        *,
        window_factory: WindowFactory | None = None,
        argv: Sequence[str] | None = None,
    ) -> None:
        """Create the application.

        Args:
            host: The lifecycle orchestrator to run.
            window_factory: Optional factory building the top-level widget from the
                ready application context. When omitted, no product UI is created.
            argv: Optional argument vector for the Qt application.
        """
        self._host = host
        self._window_factory = window_factory
        self._argv = list(argv) if argv is not None else None
        self._app: QApplication | None = None
        self._window: QWidget | None = None
        self._dispatcher: UiDispatcher | None = None

    @classmethod
    def create_default(cls, *, window_factory: WindowFactory | None = None) -> Application:
        """Create an application with a host rooted at the repository directory."""
        return cls(ApplicationHost.create_default(), window_factory=window_factory)

    @property
    def host(self) -> ApplicationHost:
        """Return the underlying lifecycle host."""
        return self._host

    def run(self) -> int:
        """Start the foundation, show any UI, run the event loop, and shut down.

        Returns:
            The process exit code from the Qt event loop.
        """
        self._app = QApplication.instance() or QApplication(self._argv if self._argv is not None else sys.argv)
        self._host.set_fatal_callback(self._handle_fatal)
        context = self._host.start()
        self._apply_theme(context)
        self._dispatcher = UiDispatcher(logger=context.logger)
        if self._window_factory is not None:
            self._window = self._window_factory(context)
            self._window.show()
        else:
            context.logger.info("application.headless", extra={"context": {"reason": "no window factory"}})
        exit_code = self._app.exec()
        self._host.shutdown(exit_code=exit_code)
        return exit_code

    def _apply_theme(self, context: ApplicationContext) -> None:
        """Apply the resolved theme stylesheet to the Qt application."""
        if self._app is None:
            return
        engine = context.theme
        self._app.setStyleSheet(engine.stylesheet(engine.select(context.settings.theme_mode)))

    def _handle_fatal(self, report: ErrorReport) -> None:
        """Quit the event loop safely on the UI thread after a fatal error."""
        if self._dispatcher is not None:
            self._dispatcher.post(self._quit)
        else:
            self._quit()

    def _quit(self) -> None:
        """Request the Qt event loop to terminate."""
        if self._app is not None:
            self._app.quit()
