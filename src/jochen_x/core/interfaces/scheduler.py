"""Scheduler protocol for time-driven infrastructure tasks."""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol, runtime_checkable

__all__ = ["IScheduler"]


@runtime_checkable
class IScheduler(Protocol):
    """Protocol for the task scheduler.

    The scheduler manages time-driven infrastructure tasks such as
    health checks, metrics collection, and cleanup routines.  All
    scheduled tasks are executed through the worker pool, never
    directly.

    The scheduler supports both fixed-interval and cron-like
    scheduling definitions.
    """

    def schedule(
        self,
        name: str,
        task: Callable[[], None],
        interval_seconds: float,
    ) -> str:
        """Schedule a recurring task with a fixed interval.

        Args:
            name: Unique human-readable name for the task.
            task: Callable to execute on each interval.
            interval_seconds: Time between executions in seconds.

        Returns:
            A unique task identifier for later cancellation.

        Raises:
            InputValidationError: If parameters are invalid.
            SchedulerError: If the scheduler is not operational.

        """
        ...

    def schedule_cron(
        self,
        name: str,
        task: Callable[[], None],
        cron_expression: str,
    ) -> str:
        """Schedule a recurring task using a cron expression.

        Args:
            name: Unique human-readable name for the task.
            task: Callable to execute on each trigger.
            cron_expression: Cron-like schedule definition.

        Returns:
            A unique task identifier for later cancellation.

        Raises:
            InputValidationError: If parameters are invalid.
            SchedulerError: If the scheduler is not operational.

        """
        ...

    def cancel(self, task_id: str) -> bool:
        """Cancel a scheduled task.

        Args:
            task_id: Identifier returned by ``schedule`` or ``schedule_cron``.

        Returns:
            ``True`` if the task was found and cancelled, ``False`` otherwise.

        """
        ...

    def cancel_all(self) -> None:
        """Cancel all scheduled tasks."""
        ...
