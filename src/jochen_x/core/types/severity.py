"""Log severity definitions for structured logging."""

from __future__ import annotations

from enum import Enum, unique

__all__ = ["LogSeverity"]


@unique
class LogSeverity(Enum):
    """Severity levels for the structured logging system.

    Every log entry carries exactly one severity level.  Log levels
    are configurable per component.

    Attributes:
        DEBUG: Detailed diagnostic information.
        INFO: General operational information.
        WARNING: Indication of a potential problem.
        ERROR: An error that does not prevent continued operation.
        CRITICAL: A severe error requiring immediate attention.

    """

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
