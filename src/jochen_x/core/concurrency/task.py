"""Task abstraction for the WorkerPool.

Wraps a callable with priority, name, and metadata so the WorkerPool
can schedule and observe it.  All tasks are immutable value objects
once created.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, unique
from typing import Any
from uuid import uuid4

__all__ = [
    "Task",
    "TaskResult",
    "TaskState",
]


@unique
class TaskState(Enum):
    """Lifecycle state of a task.

    Attributes:
        PENDING: Task is queued and waiting for execution.
        RUNNING: Task is currently being executed.
        COMPLETED: Task finished successfully.
        FAILED: Task raised an exception.
        CANCELLED: Task was cancelled before execution.

    """

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True, kw_only=True, slots=True)
class Task:
    """Represents a unit of work submitted to the WorkerPool.

    Args:
        task_id: Unique identifier (auto-generated UUID).
        name: Human-readable task name.
        callable_ref: The callable to execute.
        args: Positional arguments for the callable.
        kwargs: Keyword arguments for the callable.
        priority: Execution priority (higher = sooner).
        created_at: UTC timestamp of creation.

    """

    task_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    callable_ref: Callable[..., Any] = field(repr=False)
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, kw_only=True, slots=True)
class TaskResult:
    """Result of a completed or failed task.

    Args:
        task_id: Identifier of the task.
        task_name: Human-readable name of the task.
        state: Final state of the task.
        result: Return value on success, ``None`` on failure.
        error: Exception on failure, ``None`` on success.
        started_at: UTC timestamp when execution began.
        completed_at: UTC timestamp when execution ended.
        duration_seconds: Wall-clock execution time in seconds.

    """

    task_id: str
    task_name: str
    state: TaskState
    result: Any = None
    error: Exception | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_seconds: float = 0.0
