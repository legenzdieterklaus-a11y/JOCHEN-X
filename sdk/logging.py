"""Structured plugin logging.

:class:`PluginLogger` is the sole logging surface exposed by the SDK. It is a
thin wrapper around a :mod:`logging` logger that:

* automatically prefixes every record with the plugin identifier,
* forwards structured context as the ``extra["context"]`` payload expected
  by the JOCHEN X foundation's :class:`core.logging.StructuredFormatter`, and
* attaches exception information for error and critical records so plugin
  faults are visible in the shared rotating log file.

The base logger the wrapper writes to is injected by the host during context
construction, keeping the SDK free of global loggers and hardcoded paths.
"""

from __future__ import annotations

import logging
from typing import Any


class PluginLogger:
    """Structured, plugin-scoped logger wrapper.

    The wrapper never creates its own handlers; it delegates every record to
    the host-provided base logger. This keeps log rotation, formatting, and
    file paths under the host's control while still giving plugin authors a
    clean, plugin-scoped API.
    """

    __slots__ = ("_logger", "_plugin_id")

    def __init__(
        self,
        plugin_id: str,
        *,
        base_logger: logging.Logger | None = None,
        namespace: str = "sdk.plugins",
    ) -> None:
        """Create a plugin logger.

        Args:
            plugin_id: The plugin's stable identifier. Must be non-empty.
            base_logger: Optional root logger to derive from. When omitted the
                shared ``jochen_x`` logger is used, which is the same
                destination the foundation writes to.
            namespace: Namespace used to build the child logger under
                ``base_logger`` (e.g. ``jochen_x.sdk.plugins.<plugin_id>``).

        Raises:
            ValueError: If ``plugin_id`` is empty.
        """
        if not plugin_id:
            raise ValueError("plugin_id must be a non-empty string")
        self._plugin_id = plugin_id
        root = base_logger if base_logger is not None else logging.getLogger("jochen_x")
        self._logger = root.getChild(f"{namespace}.{plugin_id}")

    @property
    def plugin_id(self) -> str:
        """Return the plugin identifier bound to this logger."""
        return self._plugin_id

    @property
    def underlying(self) -> logging.Logger:
        """Return the underlying :class:`logging.Logger` for diagnostics only.

        This accessor is intentionally exposed so tests and integrators can
        attach handlers or assertions, but plugin authors should always use
        the wrapper's structured methods.
        """
        return self._logger

    def debug(self, message: str, **context: Any) -> None:
        """Log a debug-severity record with structured context."""
        self._emit(logging.DEBUG, message, context, None)

    def info(self, message: str, **context: Any) -> None:
        """Log an info-severity record with structured context."""
        self._emit(logging.INFO, message, context, None)

    def warning(self, message: str, **context: Any) -> None:
        """Log a warning-severity record with structured context."""
        self._emit(logging.WARNING, message, context, None)

    def error(
        self,
        message: str,
        *,
        exc: BaseException | None = None,
        **context: Any,
    ) -> None:
        """Log an error-severity record, optionally attaching an exception.

        Args:
            message: Stable, searchable log event name.
            exc: Optional exception to record with the message.
            **context: Structured context appended to the record.
        """
        self._emit(logging.ERROR, message, context, exc)

    def critical(
        self,
        message: str,
        *,
        exc: BaseException | None = None,
        **context: Any,
    ) -> None:
        """Log a critical-severity record, optionally attaching an exception."""
        self._emit(logging.CRITICAL, message, context, exc)

    def exception(self, message: str, **context: Any) -> None:
        """Log an error record with the current exception, if any.

        Intended for use inside ``except`` blocks; behaves like
        :meth:`logging.Logger.exception`.
        """
        self._logger.exception(
            message,
            extra={"context": self._build_context(context)},
        )

    def log(self, level: int, message: str, **context: Any) -> None:
        """Log a record at the given standard :mod:`logging` level."""
        self._emit(level, message, context, None)

    def _emit(
        self,
        level: int,
        message: str,
        context: dict[str, Any],
        exc: BaseException | None,
    ) -> None:
        """Dispatch a record to the underlying logger with SDK metadata."""
        payload = self._build_context(context)
        if exc is None:
            self._logger.log(level, message, extra={"context": payload})
            return
        self._logger.log(level, message, exc_info=exc, extra={"context": payload})

    def _build_context(self, context: dict[str, Any]) -> dict[str, Any]:
        """Merge caller-provided context with the plugin identifier."""
        payload: dict[str, Any] = {"plugin": self._plugin_id}
        payload.update(context)
        return payload


__all__ = ["PluginLogger"]
