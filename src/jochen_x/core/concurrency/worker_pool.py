"""WorkerPool implementation for managed concurrent task execution.

The ``WorkerPool`` is the central execution facility for all runtime
tasks.  It provides configurable thread pools, priority-based task
scheduling, graceful shutdown, and overload protection via queue
limits with backpressure.

All operations are thread-safe.
"""

from __future__ import annotations

import itertools
import os
from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import UTC, datetime
from enum import Enum, unique
from queue import PriorityQueue
from threading import Condition, Event, RLock, Thread
from typing import Any

from jochen_x.core.concurrency.task import Task, TaskResult, TaskState
from jochen_x.core.exceptions.concurrency import (
    WorkerPoolError,
    WorkerPoolOverloadError,
)
from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.types.health_status import HealthStatus

__all__ = ["WorkerPool"]

DEFAULT_MAX_WORKERS = min(32, (os.cpu_count() or 4) + 4)
DEFAULT_MAX_QUEUE_SIZE = 10_000
_COMPONENT_NAME = "WorkerPool"

_FIELD_MAX_WORKERS = "max_workers"
_FIELD_MAX_QUEUE_SIZE = "max_queue_size"
_FIELD_TASK = "task"
_REASON_MIN_ONE = "must be at least 1"
_REASON_NOT_CALLABLE = "must be callable"


@unique
class _PoolState(Enum):
    """Internal lifecycle states of the WorkerPool."""

    CREATED = "CREATED"
    RUNNING = "RUNNING"
    SHUTTING_DOWN = "SHUTTING_DOWN"
    STOPPED = "STOPPED"


class _PrioritizedTask:
    """Wrapper to make tasks comparable by priority for PriorityQueue.

    Higher priority values execute first, so we negate for min-heap.
    Ties are broken by insertion order (monotonic counter).
    """

    _counter: itertools.count[int] = itertools.count(1)

    __slots__ = ("_order", "future", "task")

    def __init__(self, task: Task, future: Future[Any]) -> None:
        """Initialise with a task and its associated future."""
        self.task: Task = task
        self.future: Future[Any] = future
        self._order: int = next(_PrioritizedTask._counter)

    def __lt__(self, other: object) -> bool:
        """Compare by negated priority, then insertion order."""
        if not isinstance(other, _PrioritizedTask):
            return NotImplemented
        if self.task.priority != other.task.priority:
            return self.task.priority > other.task.priority
        return self._order < other._order


class WorkerPool:
    """Thread-safe worker pool with priority queue and overload protection.

    All runtime tasks execute through this pool.  Tasks are scheduled
    by priority (higher values first) and executed on a configurable
    ``ThreadPoolExecutor``.

    The pool supports graceful shutdown: running tasks complete before
    the pool stops, but pending tasks in the queue are not started.

    Args:
        max_workers: Maximum number of concurrent worker threads.
        max_queue_size: Maximum number of tasks in the pending queue.
            When exceeded, ``WorkerPoolOverloadError`` is raised.

    """

    def __init__(
        self,
        *,
        max_workers: int = DEFAULT_MAX_WORKERS,
        max_queue_size: int = DEFAULT_MAX_QUEUE_SIZE,
    ) -> None:
        """Initialise the worker pool in CREATED state."""
        if max_workers < 1:
            raise InputValidationError(
                _FIELD_MAX_WORKERS,
                _REASON_MIN_ONE,
                component=_COMPONENT_NAME,
            )
        if max_queue_size < 1:
            raise InputValidationError(
                _FIELD_MAX_QUEUE_SIZE,
                _REASON_MIN_ONE,
                component=_COMPONENT_NAME,
            )

        self._max_workers: int = max_workers
        self._max_queue_size: int = max_queue_size
        self._lock: RLock = RLock()
        self._state: _PoolState = _PoolState.CREATED
        self._queue: PriorityQueue[_PrioritizedTask] = PriorityQueue()
        self._queue_size: int = 0
        self._active_count: int = 0
        self._executor: ThreadPoolExecutor | None = None
        self._dispatcher_thread: Thread | None = None
        self._shutdown_event: Event = Event()
        self._queue_condition: Condition = Condition(self._lock)
        self._completed_tasks: list[TaskResult] = []

    # -- ILifecycle -------------------------------------------------------------

    def initialize(self) -> None:
        """Initialise the worker pool.

        Prepares internal structures.  Must be called before ``start``.

        Raises:
            WorkerPoolError: If the pool is not in CREATED or STOPPED
                state.

        """
        with self._lock:
            if self._state not in (_PoolState.CREATED, _PoolState.STOPPED):
                msg = f"Cannot initialise WorkerPool in state {self._state.value}"
                raise WorkerPoolError(msg, component=_COMPONENT_NAME)
            self._state = _PoolState.CREATED
            self._shutdown_event.clear()

    def start(self) -> None:
        """Start the worker pool and its dispatch thread.

        Raises:
            WorkerPoolError: If the pool is not in CREATED state.

        """
        with self._lock:
            if self._state != _PoolState.CREATED:
                msg = f"Cannot start WorkerPool in state {self._state.value}"
                raise WorkerPoolError(msg, component=_COMPONENT_NAME)

            self._executor = ThreadPoolExecutor(
                max_workers=self._max_workers,
                thread_name_prefix="WorkerPool",
            )
            self._state = _PoolState.RUNNING
            self._shutdown_event.clear()

            self._dispatcher_thread = Thread(
                target=self._dispatch_loop,
                name="WorkerPool-Dispatch",
                daemon=True,
            )
            self._dispatcher_thread.start()

    def stop(self) -> None:
        """Stop the worker pool gracefully.

        Running tasks are allowed to complete.  Pending tasks in the
        queue are cancelled.  Blocks until shutdown completes.

        Raises:
            WorkerPoolError: If the pool is not in RUNNING state.

        """
        self.shutdown(wait=True)

    # -- IWorkerPool protocol ---------------------------------------------------

    def submit(
        self,
        task: Callable[..., Any],
        /,
        *args: Any,
        **kwargs: Any,
    ) -> Future[Any]:
        """Submit a task for execution at default priority.

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
        return self.submit_priority(task, 0, *args, **kwargs)

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
        if not callable(task):
            raise InputValidationError(
                _FIELD_TASK,
                _REASON_NOT_CALLABLE,
                component=_COMPONENT_NAME,
            )

        with self._lock:
            if self._state != _PoolState.RUNNING:
                msg = f"WorkerPool is not operational (state={self._state.value})"
                raise WorkerPoolError(msg, component=_COMPONENT_NAME)

            if self._queue_size >= self._max_queue_size:
                raise WorkerPoolOverloadError(
                    queue_size=self._queue_size,
                    max_queue_size=self._max_queue_size,
                    component=_COMPONENT_NAME,
                )

            task_name = getattr(
                task, "__qualname__",
                getattr(task, "__name__", repr(task)),
            )

            wrapped = Task(
                name=task_name,
                callable_ref=task,
                args=args,
                kwargs=dict(kwargs),
                priority=priority,
            )

            future: Future[Any] = Future()
            entry = _PrioritizedTask(wrapped, future)
            self._queue.put_nowait(entry)
            self._queue_size += 1
            self._queue_condition.notify()

        return future

    def shutdown(self, *, wait: bool = True) -> None:
        """Shut down the worker pool.

        Args:
            wait: If ``True``, block until all running tasks complete
                  before returning.

        """
        dispatcher: Thread | None = None

        with self._lock:
            if self._state != _PoolState.RUNNING:
                return
            self._state = _PoolState.SHUTTING_DOWN
            self._shutdown_event.set()
            self._queue_condition.notify_all()
            dispatcher = self._dispatcher_thread

        if dispatcher is not None:
            dispatcher.join(timeout=60.0)

        with self._lock:
            self._cancel_pending_tasks()

        if self._executor is not None:
            self._executor.shutdown(wait=wait)

        with self._lock:
            self._state = _PoolState.STOPPED
            self._executor = None
            self._dispatcher_thread = None

    def get_active_count(self) -> int:
        """Return the number of currently executing tasks.

        Returns:
            Count of active tasks.

        """
        with self._lock:
            return self._active_count

    def get_queue_size(self) -> int:
        """Return the number of tasks waiting in the queue.

        Returns:
            Count of queued tasks.

        """
        with self._lock:
            return self._queue_size

    # -- IHealthCheck protocol --------------------------------------------------

    def check_health(self) -> HealthStatus:
        """Return the health status of the worker pool.

        Returns:
            ``HEALTHY`` if running, ``DEGRADED`` if queue > 80%
            capacity, ``UNHEALTHY`` if not running.

        """
        with self._lock:
            if self._state != _PoolState.RUNNING:
                return HealthStatus.UNHEALTHY
            threshold = int(self._max_queue_size * 0.8)
            if self._queue_size > threshold:
                return HealthStatus.DEGRADED
            return HealthStatus.HEALTHY

    def get_component_name(self) -> str:
        """Return the component name.

        Returns:
            The string ``"WorkerPool"``.

        """
        return _COMPONENT_NAME

    # -- Introspection ----------------------------------------------------------

    def get_max_workers(self) -> int:
        """Return the maximum number of worker threads.

        Returns:
            Maximum worker count.

        """
        return self._max_workers

    def get_max_queue_size(self) -> int:
        """Return the maximum queue capacity.

        Returns:
            Maximum queue size.

        """
        return self._max_queue_size

    def get_completed_tasks(self) -> list[TaskResult]:
        """Return a snapshot of completed task results.

        Returns:
            List of task results.

        """
        with self._lock:
            return list(self._completed_tasks)

    def is_running(self) -> bool:
        """Check whether the pool is currently operational.

        Returns:
            True if the pool is in RUNNING state.

        """
        with self._lock:
            return self._state == _PoolState.RUNNING

    # -- Internal dispatch ------------------------------------------------------

    def _dispatch_loop(self) -> None:
        """Background loop that dequeues tasks and submits them to the executor.

        Runs until shutdown is signalled and the queue is empty.
        Uses a condition variable to avoid busy-waiting.
        """
        while True:
            entry: _PrioritizedTask | None = None

            with self._lock:
                while self._queue_size == 0 and not self._shutdown_event.is_set():
                    self._queue_condition.wait()

                if self._queue_size > 0:
                    entry = self._queue.get_nowait()
                    self._queue_size -= 1
                elif self._shutdown_event.is_set():
                    return

            if entry is not None:
                self._submit_to_executor(entry)

    def _submit_to_executor(self, entry: _PrioritizedTask) -> None:
        """Submit a task to the ThreadPoolExecutor for concurrent execution.

        Args:
            entry: The prioritized task entry to execute.

        """
        if self._executor is None:
            return

        with self._lock:
            self._active_count += 1

        self._executor.submit(self._execute_task, entry)

    def _execute_task(self, entry: _PrioritizedTask) -> None:
        """Execute a single task on a worker thread.

        Args:
            entry: The prioritized task entry to execute.

        """
        started_at = datetime.now(UTC)
        task_result: TaskResult

        try:
            result = entry.task.callable_ref(
                *entry.task.args,
                **entry.task.kwargs,
            )
            completed_at = datetime.now(UTC)
            duration = (completed_at - started_at).total_seconds()

            entry.future.set_result(result)

            task_result = TaskResult(
                task_id=entry.task.task_id,
                task_name=entry.task.name,
                state=TaskState.COMPLETED,
                result=result,
                started_at=started_at,
                completed_at=completed_at,
                duration_seconds=duration,
            )

        except Exception as exc:  # noqa: BLE001
            completed_at = datetime.now(UTC)
            duration = (completed_at - started_at).total_seconds()

            entry.future.set_exception(exc)

            task_result = TaskResult(
                task_id=entry.task.task_id,
                task_name=entry.task.name,
                state=TaskState.FAILED,
                error=exc,
                started_at=started_at,
                completed_at=completed_at,
                duration_seconds=duration,
            )

        finally:
            with self._lock:
                self._active_count -= 1
                self._completed_tasks.append(task_result)

    def _cancel_pending_tasks(self) -> None:
        """Cancel all pending tasks still in the queue."""
        while self._queue_size > 0:
            try:
                entry = self._queue.get_nowait()
                self._queue_size -= 1
                entry.future.cancel()
            except Exception:  # noqa: BLE001
                break
