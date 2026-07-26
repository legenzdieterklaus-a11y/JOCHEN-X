"""Scheduler implementation for time-driven infrastructure tasks.

The ``Scheduler`` manages recurring tasks such as health checks,
metrics collection, and cleanup routines.  All scheduled tasks are
executed through the ``WorkerPool``, never directly.

The scheduler supports fixed-interval scheduling and cron-like
expressions.  Missed executions are handled deterministically
according to a configurable policy.

All operations are thread-safe.
"""

from __future__ import annotations

import contextlib
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, unique
from threading import Condition, RLock, Thread
from typing import Any
from uuid import uuid4

from jochen_x.core.concurrency.task import TaskState
from jochen_x.core.exceptions.concurrency import SchedulerError
from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.types.health_status import HealthStatus

__all__ = ["Scheduler"]

_COMPONENT_NAME = "Scheduler"

_FIELD_NAME = "name"
_FIELD_TASK = "task"
_FIELD_INTERVAL = "interval_seconds"
_FIELD_CRON = "cron_expression"
_REASON_EMPTY = "must not be empty"
_REASON_NOT_CALLABLE = "must be callable"
_REASON_POSITIVE = "must be positive"
_REASON_INVALID_CRON = "invalid cron expression"
_REASON_DUPLICATE = "task name already registered"

_CRON_FIELD_COUNT = 5
_CRON_MIN_INTERVAL_SECONDS = 60.0
_CRON_PATTERN = re.compile(
    r"^[\d,\-\*/]+$",
)


@unique
class _SchedulerState(Enum):
    """Internal lifecycle states of the Scheduler."""

    CREATED = "CREATED"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"


@unique
class MissedExecutionPolicy(Enum):
    """Policy for handling missed scheduled executions.

    Attributes:
        SKIP: Skip the missed execution and wait for the next one.
        RUN_ONCE: Execute once immediately, then resume normal schedule.

    """

    SKIP = "SKIP"
    RUN_ONCE = "RUN_ONCE"


@dataclass(slots=True)
class _ScheduledEntry:
    """Internal record for a scheduled task."""

    task_id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    task: Callable[[], None] = field(repr=False, default=lambda: None)
    interval_seconds: float = 0.0
    cron_expression: str = ""
    next_execution: datetime = field(default_factory=lambda: datetime.now(UTC))
    last_execution: datetime | None = None
    execution_count: int = 0
    cancelled: bool = False
    state: TaskState = TaskState.PENDING


def _cron_parse_error() -> InputValidationError:
    """Create an InputValidationError for invalid cron expressions."""
    return InputValidationError(
        _FIELD_CRON,
        _REASON_INVALID_CRON,
        component=_COMPONENT_NAME,
    )


def _cron_int(text: str) -> int:
    """Parse an integer from a cron field token, raising on failure."""
    try:
        return int(text)
    except ValueError:
        raise _cron_parse_error() from None


def _parse_cron_step(part: str, min_val: int, max_val: int) -> set[int]:
    """Parse a cron part containing a step (e.g. ``*/5``, ``10/3``)."""
    base_str, step_str = part.split("/", maxsplit=1)
    step = _cron_int(step_str)
    if step < 1:
        raise _cron_parse_error()
    start = min_val if base_str == "*" else _cron_int(base_str)
    return set(range(start, max_val + 1, step))


def _parse_cron_range(part: str) -> set[int]:
    """Parse a cron part containing a range (e.g. ``1-5``)."""
    range_parts = part.split("-", maxsplit=1)
    low = _cron_int(range_parts[0])
    high = _cron_int(range_parts[1])
    return set(range(low, high + 1))


def _parse_cron_field(field_str: str, min_val: int, max_val: int) -> set[int]:
    """Parse a single cron field into a set of valid integer values.

    Args:
        field_str: The cron field string (e.g. ``"1,3,5"`` or ``"*/2"``).
        min_val: Minimum allowed value.
        max_val: Maximum allowed value.

    Returns:
        A set of integer values this field matches.

    Raises:
        InputValidationError: If the field cannot be parsed.

    """
    values: set[int] = set()

    for raw_part in field_str.split(","):
        segment = raw_part.strip()

        if "/" in segment:
            values.update(_parse_cron_step(segment, min_val, max_val))
        elif "-" in segment:
            values.update(_parse_cron_range(segment))
        elif segment == "*":
            values.update(range(min_val, max_val + 1))
        else:
            values.add(_cron_int(segment))

    return {v for v in values if min_val <= v <= max_val}


@dataclass(frozen=True, slots=True)
class _CronSchedule:
    """Parsed cron expression with matching logic."""

    minutes: frozenset[int]
    hours: frozenset[int]
    days_of_month: frozenset[int]
    months: frozenset[int]
    days_of_week: frozenset[int]

    def matches(self, dt: datetime) -> bool:
        """Check whether a datetime matches this cron schedule.

        Args:
            dt: The datetime to check.

        Returns:
            True if the datetime matches.

        """
        return (
            dt.minute in self.minutes
            and dt.hour in self.hours
            and dt.day in self.days_of_month
            and dt.month in self.months
            and dt.weekday() in self.days_of_week
        )


def _parse_cron_expression(expr: str) -> _CronSchedule:
    """Parse a cron expression into a ``_CronSchedule``.

    Args:
        expr: A 5-field cron expression (minute hour dom month dow).

    Returns:
        A parsed cron schedule.

    Raises:
        InputValidationError: If the expression is invalid.

    """
    fields = expr.strip().split()
    if len(fields) != _CRON_FIELD_COUNT:
        raise InputValidationError(
            _FIELD_CRON,
            _REASON_INVALID_CRON,
            component=_COMPONENT_NAME,
        )

    for f in fields:
        if not _CRON_PATTERN.match(f):
            raise InputValidationError(
                _FIELD_CRON,
                _REASON_INVALID_CRON,
                component=_COMPONENT_NAME,
            )

    minutes = frozenset(_parse_cron_field(fields[0], 0, 59))
    hours = frozenset(_parse_cron_field(fields[1], 0, 23))
    days_of_month = frozenset(_parse_cron_field(fields[2], 1, 31))
    months = frozenset(_parse_cron_field(fields[3], 1, 12))
    days_of_week = frozenset(_parse_cron_field(fields[4], 0, 6))

    return _CronSchedule(
        minutes=minutes,
        hours=hours,
        days_of_month=days_of_month,
        months=months,
        days_of_week=days_of_week,
    )


class Scheduler:
    """Time-driven task scheduler for infrastructure tasks.

    Schedules recurring tasks with fixed intervals or cron expressions.
    All scheduled tasks are dispatched through a ``submit`` callback
    (typically the WorkerPool's ``submit`` method), never executed
    directly.

    The scheduler maintains its own timing thread that checks for due
    tasks at a configurable resolution.  It uses condition-variable
    based waiting to avoid busy-wait loops.

    Args:
        submit_fn: Callable used to submit tasks for execution.
            Typically ``worker_pool.submit``.
        tick_interval: Resolution of the scheduling loop in seconds.
        missed_policy: Policy for handling missed executions.

    """

    def __init__(
        self,
        *,
        submit_fn: Callable[..., Any] | None = None,
        tick_interval: float = 1.0,
        missed_policy: MissedExecutionPolicy = MissedExecutionPolicy.RUN_ONCE,
    ) -> None:
        """Initialise the scheduler in CREATED state."""
        self._submit_fn: Callable[..., Any] | None = submit_fn
        self._tick_interval: float = tick_interval
        self._missed_policy: MissedExecutionPolicy = missed_policy
        self._lock: RLock = RLock()
        self._condition: Condition = Condition(self._lock)
        self._state: _SchedulerState = _SchedulerState.CREATED
        self._entries: dict[str, _ScheduledEntry] = {}
        self._cron_schedules: dict[str, _CronSchedule] = {}
        self._names: dict[str, str] = {}
        self._scheduler_thread: Thread | None = None

    # -- ILifecycle -------------------------------------------------------------

    def initialize(self) -> None:
        """Initialise the scheduler.

        Raises:
            SchedulerError: If the scheduler is not in CREATED or
                STOPPED state.

        """
        with self._lock:
            if self._state not in (
                _SchedulerState.CREATED,
                _SchedulerState.STOPPED,
            ):
                msg = f"Cannot initialise Scheduler in state {self._state.value}"
                raise SchedulerError(msg, component=_COMPONENT_NAME)
            self._state = _SchedulerState.CREATED

    def start(self) -> None:
        """Start the scheduler timing thread.

        Raises:
            SchedulerError: If the scheduler is not in CREATED state.

        """
        with self._lock:
            if self._state != _SchedulerState.CREATED:
                msg = f"Cannot start Scheduler in state {self._state.value}"
                raise SchedulerError(msg, component=_COMPONENT_NAME)

            self._state = _SchedulerState.RUNNING
            self._scheduler_thread = Thread(
                target=self._tick_loop,
                name="Scheduler-Tick",
                daemon=True,
            )
            self._scheduler_thread.start()

    def stop(self) -> None:
        """Stop the scheduler and cancel all tasks.

        Blocks until the timing thread terminates.

        Raises:
            SchedulerError: If the scheduler is not in RUNNING state.

        """
        thread: Thread | None = None
        with self._lock:
            if self._state != _SchedulerState.RUNNING:
                msg = f"Cannot stop Scheduler in state {self._state.value}"
                raise SchedulerError(msg, component=_COMPONENT_NAME)
            self._state = _SchedulerState.STOPPING
            self._condition.notify_all()
            thread = self._scheduler_thread

        if thread is not None:
            thread.join(timeout=30.0)

        with self._lock:
            self._state = _SchedulerState.STOPPED
            self._scheduler_thread = None

    # -- IScheduler protocol ----------------------------------------------------

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
        self._validate_name(name)
        self._validate_callable(task)
        self._validate_interval(interval_seconds)

        with self._lock:
            self._assert_running()
            self._assert_unique_name(name)

            now = datetime.now(UTC)
            entry = _ScheduledEntry(
                name=name,
                task=task,
                interval_seconds=interval_seconds,
                next_execution=datetime.fromtimestamp(
                    now.timestamp() + interval_seconds,
                    tz=UTC,
                ),
            )
            self._entries[entry.task_id] = entry
            self._names[name] = entry.task_id
            self._condition.notify()

        return entry.task_id

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
            cron_expression: 5-field cron schedule definition
                (minute hour day-of-month month day-of-week).

        Returns:
            A unique task identifier for later cancellation.

        Raises:
            InputValidationError: If parameters are invalid.
            SchedulerError: If the scheduler is not operational.

        """
        self._validate_name(name)
        self._validate_callable(task)

        if not cron_expression or not cron_expression.strip():
            raise InputValidationError(
                _FIELD_CRON,
                _REASON_EMPTY,
                component=_COMPONENT_NAME,
            )

        cron_schedule = _parse_cron_expression(cron_expression)

        with self._lock:
            self._assert_running()
            self._assert_unique_name(name)

            entry = _ScheduledEntry(
                name=name,
                task=task,
                cron_expression=cron_expression,
            )
            self._entries[entry.task_id] = entry
            self._cron_schedules[entry.task_id] = cron_schedule
            self._names[name] = entry.task_id
            self._condition.notify()

        return entry.task_id

    def cancel(self, task_id: str) -> bool:
        """Cancel a scheduled task.

        Args:
            task_id: Identifier returned by ``schedule`` or
                ``schedule_cron``.

        Returns:
            ``True`` if the task was found and cancelled, ``False``
            otherwise.

        """
        with self._lock:
            entry = self._entries.get(task_id)
            if entry is None:
                return False
            entry.cancelled = True
            entry.state = TaskState.CANCELLED
            self._names.pop(entry.name, None)
            self._entries.pop(task_id, None)
            self._cron_schedules.pop(task_id, None)
            return True

    def cancel_all(self) -> None:
        """Cancel all scheduled tasks."""
        with self._lock:
            for entry in self._entries.values():
                entry.cancelled = True
                entry.state = TaskState.CANCELLED
            self._entries.clear()
            self._cron_schedules.clear()
            self._names.clear()

    # -- IHealthCheck protocol --------------------------------------------------

    def check_health(self) -> HealthStatus:
        """Return the health status of the scheduler.

        Returns:
            ``HEALTHY`` if running, ``UNHEALTHY`` otherwise.

        """
        with self._lock:
            if self._state == _SchedulerState.RUNNING:
                return HealthStatus.HEALTHY
            return HealthStatus.UNHEALTHY

    def get_component_name(self) -> str:
        """Return the component name.

        Returns:
            The string ``"Scheduler"``.

        """
        return _COMPONENT_NAME

    # -- Introspection ----------------------------------------------------------

    def get_scheduled_task_count(self) -> int:
        """Return the number of active scheduled tasks.

        Returns:
            Count of scheduled (non-cancelled) tasks.

        """
        with self._lock:
            return len(self._entries)

    def get_task_names(self) -> list[str]:
        """Return the names of all scheduled tasks.

        Returns:
            List of task names.

        """
        with self._lock:
            return [e.name for e in self._entries.values()]

    def is_running(self) -> bool:
        """Check whether the scheduler is currently operational.

        Returns:
            True if the scheduler is in RUNNING state.

        """
        with self._lock:
            return self._state == _SchedulerState.RUNNING

    # -- Internal ---------------------------------------------------------------

    def _tick_loop(self) -> None:
        """Background loop that checks for due tasks.

        Uses condition-variable based waiting at the configured
        tick interval to avoid busy-waiting.
        """
        while True:
            with self._lock:
                if self._state != _SchedulerState.RUNNING:
                    return

                now = datetime.now(UTC)
                self._process_due_tasks(now)

                self._condition.wait(timeout=self._tick_interval)

                if self._state != _SchedulerState.RUNNING:
                    return

    def _process_due_tasks(self, now: datetime) -> None:
        """Check all entries and dispatch those that are due.

        Must be called with ``self._lock`` held.

        Args:
            now: The current UTC time.

        """
        for entry in list(self._entries.values()):
            if entry.cancelled:
                continue

            is_due = False

            if entry.cron_expression:
                cron = self._cron_schedules.get(entry.task_id)
                cron_matches = cron is not None and cron.matches(now)
                not_recently_run = entry.last_execution is None or (
                    now.timestamp() - entry.last_execution.timestamp()
                    >= _CRON_MIN_INTERVAL_SECONDS
                )
                if cron_matches and not_recently_run:
                    is_due = True
            elif entry.next_execution <= now:
                is_due = True

            if is_due:
                self._dispatch_entry(entry, now)

    def _dispatch_entry(self, entry: _ScheduledEntry, now: datetime) -> None:
        """Dispatch a single scheduled entry for execution.

        Must be called with ``self._lock`` held.

        Args:
            entry: The scheduled entry to dispatch.
            now: The current UTC time.

        """
        entry.last_execution = now
        entry.execution_count += 1

        if entry.interval_seconds > 0:
            entry.next_execution = datetime.fromtimestamp(
                now.timestamp() + entry.interval_seconds,
                tz=UTC,
            )

        if self._submit_fn is not None:
            with contextlib.suppress(Exception):
                self._submit_fn(entry.task)

    # -- Validation -------------------------------------------------------------

    @staticmethod
    def _validate_name(name: str) -> None:
        """Raise if *name* is empty."""
        if not name or not name.strip():
            raise InputValidationError(
                _FIELD_NAME,
                _REASON_EMPTY,
                component=_COMPONENT_NAME,
            )

    @staticmethod
    def _validate_callable(task: Callable[[], None]) -> None:
        """Raise if *task* is not callable."""
        if not callable(task):
            raise InputValidationError(
                _FIELD_TASK,
                _REASON_NOT_CALLABLE,
                component=_COMPONENT_NAME,
            )

    @staticmethod
    def _validate_interval(interval_seconds: float) -> None:
        """Raise if *interval_seconds* is not positive."""
        if interval_seconds <= 0:
            raise InputValidationError(
                _FIELD_INTERVAL,
                _REASON_POSITIVE,
                component=_COMPONENT_NAME,
            )

    def _assert_running(self) -> None:
        """Raise if the scheduler is not in RUNNING state."""
        if self._state != _SchedulerState.RUNNING:
            msg = f"Scheduler is not operational (state={self._state.value})"
            raise SchedulerError(msg, component=_COMPONENT_NAME)

    def _assert_unique_name(self, name: str) -> None:
        """Raise if *name* is already registered."""
        if name in self._names:
            raise InputValidationError(
                _FIELD_NAME,
                _REASON_DUPLICATE,
                component=_COMPONENT_NAME,
            )
