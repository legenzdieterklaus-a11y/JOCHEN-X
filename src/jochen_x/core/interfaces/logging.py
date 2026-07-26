"""Structured logging protocol."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from jochen_x.core.types.severity import LogSeverity

__all__ = ["ILogger"]


@runtime_checkable
class ILogger(Protocol):
    """Protocol for the structured logging system.

    Every log entry carries mandatory fields: timestamp (ISO 8601 UTC),
    severity, component name, and correlation ID.

    Logging is asynchronous and must never block the UI thread.  Log
    levels are configurable per component.
    """

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
        ...

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
        ...

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
        ...

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
        ...

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
        ...

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
        ...
