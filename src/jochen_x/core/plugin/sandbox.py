"""Plugin sandbox for isolated, safe execution of plugin code.

The ``PluginSandbox`` wraps plugin lifecycle callbacks in a
protective execution boundary.  All exceptions from plugin code
are caught, logged, and tracked — never propagated.  A failing
plugin cannot crash the runtime or affect other plugins.

Health status degrades with consecutive failures and recovers
on the next successful execution.

All operations are thread-safe.
"""

from __future__ import annotations

from collections.abc import Callable
from threading import RLock
from typing import TYPE_CHECKING

from jochen_x.core.types.events import PluginAction
from jochen_x.core.types.health_status import HealthStatus

if TYPE_CHECKING:
    from jochen_x.core.interfaces.logging import ILogger

__all__ = ["PluginSandbox"]

_CONSECUTIVE_FAILURE_UNHEALTHY_THRESHOLD = 5


class PluginSandbox:
    """Isolated execution environment for a single plugin.

    Wraps plugin lifecycle callbacks so that exceptions are caught
    and recorded, never propagated.  Tracks consecutive and total
    failure counts for health monitoring.

    Args:
        plugin_id: Unique identifier of the plugin.
        logger: Logger for recording execution outcomes.

    """

    __slots__ = (
        "_consecutive_failures",
        "_lock",
        "_logger",
        "_plugin_id",
        "_total_executions",
        "_total_failures",
    )

    def __init__(
        self,
        *,
        plugin_id: str,
        logger: ILogger,
    ) -> None:
        """Initialise the sandbox for a specific plugin."""
        self._plugin_id: str = plugin_id
        self._logger: ILogger = logger
        self._lock: RLock = RLock()
        self._consecutive_failures: int = 0
        self._total_failures: int = 0
        self._total_executions: int = 0

    def execute(
        self,
        action: PluginAction,
        callback: Callable[[], None],
    ) -> bool:
        """Execute a plugin callback within the sandbox.

        The callback is invoked in a protected context.  Any
        exception is caught, logged, and tracked — never propagated
        to the caller.

        Args:
            action: The lifecycle action being performed.
            callback: The plugin callback to execute.

        Returns:
            ``True`` if the callback completed without error,
            ``False`` otherwise.

        """
        component = self.get_component_name()

        msg = f"Executing plugin action {action.value}"
        self._logger.debug(msg, component=component)

        with self._lock:
            self._total_executions += 1

        try:
            callback()
        except Exception as exc:  # noqa: BLE001
            with self._lock:
                self._consecutive_failures += 1
                self._total_failures += 1

            detail = (
                f"Plugin '{self._plugin_id}' failed during "
                f"{action.value}: {exc}"
            )
            self._logger.error(detail, component=component)  # noqa: TRY400
            return False

        with self._lock:
            self._consecutive_failures = 0

        done = f"Plugin action {action.value} completed"
        self._logger.debug(done, component=component)
        return True

    # -- IHealthCheck protocol -------------------------------------------------

    def check_health(self) -> HealthStatus:
        """Return the health status based on recent failure history.

        Returns:
            ``HEALTHY`` with no consecutive failures,
            ``DEGRADED`` below the unhealthy threshold,
            ``UNHEALTHY`` at or above the threshold.

        """
        with self._lock:
            if self._consecutive_failures == 0:
                return HealthStatus.HEALTHY
            if self._consecutive_failures < _CONSECUTIVE_FAILURE_UNHEALTHY_THRESHOLD:
                return HealthStatus.DEGRADED
            return HealthStatus.UNHEALTHY

    def get_component_name(self) -> str:
        """Return the component name.

        Returns:
            A string of the form ``"PluginSandbox[<plugin_id>]"``.

        """
        return f"PluginSandbox[{self._plugin_id}]"

    # -- Introspection ---------------------------------------------------------

    def get_consecutive_failures(self) -> int:
        """Return the number of consecutive execution failures.

        Returns:
            The consecutive failure count.

        """
        with self._lock:
            return self._consecutive_failures

    def get_total_failures(self) -> int:
        """Return the total number of execution failures.

        Returns:
            The total failure count across all executions.

        """
        with self._lock:
            return self._total_failures

    def get_total_executions(self) -> int:
        """Return the total number of executions attempted.

        Returns:
            The total execution count.

        """
        with self._lock:
            return self._total_executions

    def reset_failure_counts(self) -> None:
        """Reset all failure counters to zero."""
        with self._lock:
            self._consecutive_failures = 0
            self._total_failures = 0
