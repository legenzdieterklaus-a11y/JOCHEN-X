"""Centralized application error handling.

All unexpected and expected-but-notable failures flow through a single
:class:`CentralErrorHandler`. It classifies each error, logs it, publishes an
:class:`app.events.ErrorRaised` event, and escalates fatal errors to an injected
handler so the host can terminate the application safely. Classification is
driven by the application error taxonomy rather than by ad-hoc string checks.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol

from core.exceptions import ConfigurationError, DatabaseError, JochenXError

from app.events import ErrorRaised, EventPublisher


class PluginError(JochenXError):
    """Raised for recoverable plugin discovery or activation failures."""


class UiError(JochenXError):
    """Raised for recoverable failures originating at the UI boundary."""


class WorkerError(JochenXError):
    """Raised for recoverable failures inside background workers."""


class ErrorSeverity(StrEnum):
    """Severity classification controlling escalation behaviour."""

    RECOVERABLE = "recoverable"
    FATAL = "fatal"


class ErrorCategory(StrEnum):
    """Semantic category used for logging, routing, and escalation."""

    RECOVERABLE = "recoverable"
    FATAL = "fatal"
    PLUGIN = "plugin"
    UI = "ui"
    WORKER = "worker"
    CONFIGURATION = "configuration"
    DATABASE = "database"
    UNEXPECTED = "unexpected"


_CATEGORY_BY_TYPE: tuple[tuple[type[BaseException], ErrorCategory], ...] = (
    (ConfigurationError, ErrorCategory.CONFIGURATION),
    (DatabaseError, ErrorCategory.DATABASE),
    (PluginError, ErrorCategory.PLUGIN),
    (UiError, ErrorCategory.UI),
    (WorkerError, ErrorCategory.WORKER),
    (JochenXError, ErrorCategory.RECOVERABLE),
)

_FATAL_CATEGORIES: frozenset[ErrorCategory] = frozenset({
    ErrorCategory.FATAL,
    ErrorCategory.CONFIGURATION,
    ErrorCategory.DATABASE,
    ErrorCategory.UNEXPECTED,
})


@dataclass(frozen=True, slots=True)
class ErrorReport:
    """Immutable outcome of handling a single error."""

    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    exception_type: str
    context: Mapping[str, Any] = field(default_factory=dict)

    @property
    def is_fatal(self) -> bool:
        """Return whether the error was classified as fatal."""
        return self.severity is ErrorSeverity.FATAL


class ErrorHandler(Protocol):
    """Port for centralized error handling."""

    def handle(
        self,
        error: BaseException,
        *,
        category: ErrorCategory | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> ErrorReport:
        """Handle an error and return a structured report."""
        ...


class CentralErrorHandler:
    """Classifies, logs, publishes, and escalates every reported error."""

    def __init__(
        self,
        *,
        logger: logging.Logger,
        publisher: EventPublisher | None = None,
        on_fatal: Callable[[ErrorReport], None] | None = None,
    ) -> None:
        """Create the handler.

        Args:
            logger: Logger that receives every handled error.
            publisher: Optional event publisher for ``ErrorRaised`` events.
            on_fatal: Optional callback invoked exactly once per fatal error so
                the host can begin a safe termination.
        """
        self._logger = logger
        self._publisher = publisher
        self._on_fatal = on_fatal

    def handle(
        self,
        error: BaseException,
        *,
        category: ErrorCategory | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> ErrorReport:
        """Classify, record, and escalate a single error.

        Args:
            error: The raised exception.
            category: Optional explicit category overriding classification.
            context: Optional structured context to attach to the report.

        Returns:
            The structured :class:`ErrorReport`.
        """
        resolved_category = category or self._classify(error)
        severity = (
            ErrorSeverity.FATAL
            if resolved_category in _FATAL_CATEGORIES
            else ErrorSeverity.RECOVERABLE
        )
        report = ErrorReport(
            category=resolved_category,
            severity=severity,
            message=str(error) or type(error).__name__,
            exception_type=type(error).__name__,
            context=dict(context or {}),
        )
        self._log(report, error)
        if self._publisher is not None:
            ErrorRaised(
                report.category.value, report.severity.value, report.message
            ).publish(self._publisher)
        if report.is_fatal and self._on_fatal is not None:
            self._on_fatal(report)
        return report

    def guard(
        self, report: Callable[[BaseException], None] | None = None
    ) -> Callable[[BaseException], None]:
        """Return a reporter callable suitable for UI-boundary error routing."""
        def reporter(error: BaseException) -> None:
            self.handle(error, category=ErrorCategory.UI)
            if report is not None:
                report(error)

        return reporter

    @staticmethod
    def _classify(error: BaseException) -> ErrorCategory:
        """Map an exception instance to its error category."""
        for error_type, category in _CATEGORY_BY_TYPE:
            if isinstance(error, error_type):
                return category
        return ErrorCategory.UNEXPECTED

    def _log(self, report: ErrorReport, error: BaseException) -> None:
        """Record the error at a severity-appropriate log level."""
        payload = {
            "category": report.category.value,
            "severity": report.severity.value,
            "type": report.exception_type,
            **report.context,
        }
        if report.is_fatal:
            self._logger.critical("error.fatal", exc_info=error, extra={"context": payload})
        else:
            self._logger.error("error.recoverable", exc_info=error, extra={"context": payload})
