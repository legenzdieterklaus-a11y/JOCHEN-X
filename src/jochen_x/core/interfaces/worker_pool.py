"""Worker pool protocol for managed concurrent task execution."""

from __future__ import annotations

from collections.abc import Callable
from concurrent.futures import Future
from typing import Any, Protocol, runtime_checkable

__all__ = ["IWorkerPool"]


@runtime_checkable
class IWorkerPool(Protocol):
    """Protocol for the centralised worker pool.

    All runtime tasks execute through the worker pool.  It provides
    configurable thread/task pools, task prioritisation, graceful
    shutdown, and overload protection (queue limits with backpressure).
    """

    def submit(
        self,
        task: Callable[..., Any],
        /,
        *args: Any,
        **kwargs: Any,
    ) -> Future[Any]:
        """Submit a task for execution.

        Args:
            task: Callable to execute.
            *args: Positional arguments for the callable.
            **kwargs: Keyword arguments for the callable.

        Returns:
            A ``Future`` representing the pending result.

        Raises:
            WorkerPoolOverloadError: If the queue is at capacity.
            WorkerPoolError: If the pool is not operational.

        """
        ...

    def submit_priority(
        self,
        task: Callable[..., Any],
        priority: int,
        /,
        *args: Any,
        **kwargs: Any,
    ) -> Future[Any]:
        """Submit a task with explicit priority.

        Higher priority values are executed first.

        Args:
            task: Callable to execute.
            priority: Execution priority (higher = sooner).
            *args: Positional arguments for the callable.
            **kwargs: Keyword arguments for the callable.

        Returns:
            A ``Future`` representing the pending result.

        Raises:
            WorkerPoolOverloadError: If the queue is at capacity.
            WorkerPoolError: If the pool is not operational.

        """
        ...

    def shutdown(self, *, wait: bool = True) -> None:
        """Shut down the worker pool.

        Args:
            wait: If ``True``, block until all running tasks complete
                  before returning.  Pending tasks in the queue are
                  not started.

        """
        ...

    def get_active_count(self) -> int:
        """Return the number of currently executing tasks.

        Returns:
            Count of active tasks.

        """
        ...

    def get_queue_size(self) -> int:
        """Return the number of tasks waiting in the queue.

        Returns:
            Count of queued tasks.

        """
        ...
