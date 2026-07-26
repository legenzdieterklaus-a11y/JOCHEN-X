"""Structured logging system with asynchronous dispatch.

The ``StructuredLogger`` emits JSON-formatted log entries through
Python's standard ``logging`` module.  Every entry carries mandatory
fields: timestamp (ISO 8601 UTC), severity, component name, and
correlation ID.

Logging is asynchronous via a ``QueueHandler`` / ``QueueListener``
pair to avoid blocking the caller (especially the UI thread).
Log levels are configurable per component.
"""

from __future__ import annotations

import json
import logging
import logging.handlers
from datetime import UTC, datetime
from pathlib import Path
from queue import SimpleQueue
from threading import RLock
from typing import ClassVar
from uuid import uuid4

from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.types.health_status import HealthStatus
from jochen_x.core.types.severity import LogSeverity

__all__ = ["StructuredLogger"]

_COMPONENT_NAME = "StructuredLogger"
_FIELD_COMPONENT = "component"
_FIELD_SEVERITY = "severity"
_FIELD_MAX_BYTES = "max_bytes"
_FIELD_BACKUP_COUNT = "backup_count"
_REASON_EMPTY = "must not be empty"
_REASON_INVALID_SEVERITY = "must be a LogSeverity enum value"
_REASON_MIN_ONE = "must be at least 1"

_SEVERITY_TO_LEVEL: dict[LogSeverity, int] = {
    LogSeverity.DEBUG: logging.DEBUG,
    LogSeverity.INFO: logging.INFO,
    LogSeverity.WARNING: logging.WARNING,
    LogSeverity.ERROR: logging.ERROR,
    LogSeverity.CRITICAL: logging.CRITICAL,
}


class _JsonFormatter(logging.Formatter):
    """Formats log records as single-line JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        """Format *record* as a JSON string.

        Args:
            record: The log record to format.

        Returns:
            A single-line JSON string.

        """
        entry: dict[str, str | int | float] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "severity": record.levelname,
            "component": getattr(record, "component", ""),
            "correlation_id": getattr(record, "correlation_id", ""),
            "message": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info and record.exc_info[1] is not None:
            entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(entry, ensure_ascii=False)


class StructuredLogger:
    """Asynchronous structured logging system.

    Uses Python's standard ``logging`` module with a
    ``QueueHandler``/``QueueListener`` pair for non-blocking
    dispatch.  Log output is formatted as JSON.

    Log levels can be configured globally or per component.
    File-based logging with rotation is supported via
    ``configure_file_output``.

    Args:
        default_level: The default minimum severity level for all
            components.

    """

    _LOGGER_NAME: ClassVar[str] = "jochen_x.runtime"

    def __init__(
        self,
        *,
        default_level: LogSeverity = LogSeverity.INFO,
    ) -> None:
        """Initialise the structured logger."""
        self._lock: RLock = RLock()
        self._default_level: LogSeverity = default_level
        self._component_levels: dict[str, LogSeverity] = {}
        self._started: bool = False

        self._log_queue: SimpleQueue[logging.LogRecord] = SimpleQueue()
        self._queue_handler: logging.handlers.QueueHandler = (
            logging.handlers.QueueHandler(self._log_queue)
        )

        self._logger: logging.Logger = logging.getLogger(self._LOGGER_NAME)
        self._logger.setLevel(logging.DEBUG)
        self._logger.propagate = False
        self._logger.addHandler(self._queue_handler)

        self._handlers: list[logging.Handler] = []
        self._listener: logging.handlers.QueueListener | None = None

    # -- Lifecycle -----------------------------------------------------------

    def initialize(self) -> None:
        """Initialise the logging system.

        Prepares internal structures.  Must be called before ``start``.
        """
        with self._lock:
            self._logger.setLevel(logging.DEBUG)

    def start(self) -> None:
        """Start the asynchronous log dispatch.

        Starts the ``QueueListener`` that processes log records on a
        background thread.
        """
        with self._lock:
            if self._started:
                return
            if not self._handlers:
                console = logging.StreamHandler()
                console.setFormatter(_JsonFormatter())
                self._handlers.append(console)

            self._listener = logging.handlers.QueueListener(
                self._log_queue,
                *self._handlers,
                respect_handler_level=True,
            )
            self._listener.start()
            self._started = True

    def stop(self) -> None:
        """Stop the asynchronous log dispatch.

        Flushes all pending log records and stops the background
        thread.
        """
        with self._lock:
            if not self._started:
                return
            if self._listener is not None:
                self._listener.stop()
                self._listener = None
            self._started = False

    # -- ILogger protocol ----------------------------------------------------

    def log(
        self,
        severity: LogSeverity,
        message: str,
        *,
        component: str = "",
        correlation_id: str = "",
    ) -> None:
        """Emit a structured log entry.

        Args:
            severity: Log severity level.
            message: Human-readable log message.
            component: Name of the originating component.
            correlation_id: Correlation ID for cross-component tracing.

        """
        if not isinstance(severity, LogSeverity):
            raise InputValidationError(
                _FIELD_SEVERITY,
                _REASON_INVALID_SEVERITY,
                component=_COMPONENT_NAME,
            )

        effective_level = self._get_effective_level(component)
        if _SEVERITY_TO_LEVEL[severity] < _SEVERITY_TO_LEVEL[effective_level]:
            return

        cid = correlation_id or str(uuid4())
        level = _SEVERITY_TO_LEVEL[severity]

        record = self._logger.makeRecord(
            name=self._LOGGER_NAME,
            level=level,
            fn="",
            lno=0,
            msg=message,
            args=(),
            exc_info=None,
        )
        record.component = component
        record.correlation_id = cid
        self._logger.handle(record)

    def debug(
        self,
        message: str,
        *,
        component: str = "",
        correlation_id: str = "",
    ) -> None:
        """Log a DEBUG-level message.

        Args:
            message: Human-readable log message.
            component: Name of the originating component.
            correlation_id: Correlation ID for cross-component tracing.

        """
        self.log(
            LogSeverity.DEBUG,
            message,
            component=component,
            correlation_id=correlation_id,
        )

    def info(
        self,
        message: str,
        *,
        component: str = "",
        correlation_id: str = "",
    ) -> None:
        """Log an INFO-level message.

        Args:
            message: Human-readable log message.
            component: Name of the originating component.
            correlation_id: Correlation ID for cross-component tracing.

        """
        self.log(
            LogSeverity.INFO,
            message,
            component=component,
            correlation_id=correlation_id,
        )

    def warning(
        self,
        message: str,
        *,
        component: str = "",
        correlation_id: str = "",
    ) -> None:
        """Log a WARNING-level message.

        Args:
            message: Human-readable log message.
            component: Name of the originating component.
            correlation_id: Correlation ID for cross-component tracing.

        """
        self.log(
            LogSeverity.WARNING,
            message,
            component=component,
            correlation_id=correlation_id,
        )

    def error(
        self,
        message: str,
        *,
        component: str = "",
        correlation_id: str = "",
    ) -> None:
        """Log an ERROR-level message.

        Args:
            message: Human-readable log message.
            component: Name of the originating component.
            correlation_id: Correlation ID for cross-component tracing.

        """
        self.log(
            LogSeverity.ERROR,
            message,
            component=component,
            correlation_id=correlation_id,
        )

    def critical(
        self,
        message: str,
        *,
        component: str = "",
        correlation_id: str = "",
    ) -> None:
        """Log a CRITICAL-level message.

        Args:
            message: Human-readable log message.
            component: Name of the originating component.
            correlation_id: Correlation ID for cross-component tracing.

        """
        self.log(
            LogSeverity.CRITICAL,
            message,
            component=component,
            correlation_id=correlation_id,
        )

    # -- Configuration -------------------------------------------------------

    def set_level(self, component: str, severity: LogSeverity) -> None:
        """Set the minimum log level for a specific component.

        Args:
            component: Component name.
            severity: Minimum severity level for this component.

        Raises:
            InputValidationError: If component is empty or severity
                is not a ``LogSeverity``.

        """
        if not component:
            raise InputValidationError(
                _FIELD_COMPONENT,
                _REASON_EMPTY,
                component=_COMPONENT_NAME,
            )
        if not isinstance(severity, LogSeverity):
            raise InputValidationError(
                _FIELD_SEVERITY,
                _REASON_INVALID_SEVERITY,
                component=_COMPONENT_NAME,
            )
        with self._lock:
            self._component_levels[component] = severity

    def get_level(self, component: str) -> LogSeverity:
        """Return the effective log level for a component.

        Args:
            component: Component name.

        Returns:
            The component-specific level, or the default level if
            none is configured.

        """
        with self._lock:
            return self._component_levels.get(component, self._default_level)

    def configure_file_output(
        self,
        path: Path,
        *,
        max_bytes: int = 10_485_760,
        backup_count: int = 5,
    ) -> None:
        """Add a rotating file handler.

        Args:
            path: Path to the log file.
            max_bytes: Maximum size of a single log file in bytes.
            backup_count: Number of backup files to keep.

        Raises:
            InputValidationError: If max_bytes or backup_count is
                less than 1.

        """
        if max_bytes < 1:
            raise InputValidationError(
                _FIELD_MAX_BYTES,
                _REASON_MIN_ONE,
                component=_COMPONENT_NAME,
            )
        if backup_count < 1:
            raise InputValidationError(
                _FIELD_BACKUP_COUNT,
                _REASON_MIN_ONE,
                component=_COMPONENT_NAME,
            )

        path.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.handlers.RotatingFileHandler(
            filename=str(path),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        handler.setFormatter(_JsonFormatter())

        with self._lock:
            self._handlers.append(handler)
            if self._started and self._listener is not None:
                self._listener.stop()
                self._listener = logging.handlers.QueueListener(
                    self._log_queue,
                    *self._handlers,
                    respect_handler_level=True,
                )
                self._listener.start()

    # -- IHealthCheck protocol -----------------------------------------------

    def check_health(self) -> HealthStatus:
        """Return the health status of the logger.

        Returns:
            ``HealthStatus.HEALTHY`` if the logger is started,
            ``HealthStatus.DEGRADED`` otherwise.

        """
        with self._lock:
            if self._started:
                return HealthStatus.HEALTHY
            return HealthStatus.DEGRADED

    def get_component_name(self) -> str:
        """Return the component name.

        Returns:
            The string ``"StructuredLogger"``.

        """
        return _COMPONENT_NAME

    # -- Internal ------------------------------------------------------------

    def _get_effective_level(self, component: str) -> LogSeverity:
        """Return the effective log level for *component*."""
        if component:
            with self._lock:
                level = self._component_levels.get(component)
                if level is not None:
                    return level
        return self._default_level
