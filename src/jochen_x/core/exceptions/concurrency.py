"""Concurrency exceptions for WorkerPool and Scheduler."""

from __future__ import annotations

from jochen_x.core.exceptions.base import JochenXError

__all__ = [
    "SchedulerError",
    "TaskExecutionError",
    "WorkerPoolError",
    "WorkerPoolOverloadError",
]


class WorkerPoolError(JochenXError):
    """General worker pool error.

    Args:
        message: Human-readable error description.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """


class WorkerPoolOverloadError(WorkerPoolError):
    """The worker pool rejected a task due to overload.

    Args:
        queue_size: Current queue size at the time of rejection.
        max_queue_size: Maximum configured queue size.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """

    def __init__(
        self,
        queue_size: int,
        max_queue_size: int,
        *,
        correlation_id: str = "",
        component: str = "",
    ) -> None:
        """Initialise with queue capacity details."""
        self.queue_size: int = queue_size
        self.max_queue_size: int = max_queue_size
        super().__init__(
            f"Worker pool overloaded: queue {queue_size}/{max_queue_size}",
            correlation_id=correlation_id,
            component=component,
        )


class SchedulerError(JochenXError):
    """General scheduler error.

    Args:
        message: Human-readable error description.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """


class TaskExecutionError(JochenXError):
    """A submitted task failed during execution.

    Args:
        task_name: Name or identifier of the failed task.
        message: Human-readable error description.
        correlation_id: Correlation ID for cross-component tracing.
        component: Name of the component that raised the error.

    """

    def __init__(
        self,
        task_name: str,
        message: str,
        *,
        correlation_id: str = "",
        component: str = "",
    ) -> None:
        """Initialise with the failed task details."""
        self.task_name: str = task_name
        super().__init__(
            f"Task '{task_name}' failed: {message}",
            correlation_id=correlation_id,
            component=component,
        )
