"""Unit tests for the Scheduler."""

from __future__ import annotations

import threading
import time

import pytest

from jochen_x.core.concurrency.scheduler import Scheduler
from jochen_x.core.exceptions.concurrency import SchedulerError
from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.types.health_status import HealthStatus


def _noop() -> None:
    pass


def _create_running_scheduler(
    *,
    tick_interval: float = 0.05,
) -> Scheduler:
    submitted: list[object] = []

    def fake_submit(task: object, /, *_args: object, **_kwargs: object) -> None:
        if callable(task):
            submitted.append(task)
            task()

    scheduler = Scheduler(submit_fn=fake_submit, tick_interval=tick_interval)
    scheduler.initialize()
    scheduler.start()
    return scheduler


class TestSchedulerConstruction:
    def test_default_construction(self) -> None:
        scheduler = Scheduler()
        assert not scheduler.is_running()

    def test_custom_tick_interval(self) -> None:
        scheduler = Scheduler(tick_interval=0.5)
        assert not scheduler.is_running()


class TestSchedulerLifecycle:
    def test_initialize_and_start(self) -> None:
        scheduler = _create_running_scheduler()
        assert scheduler.is_running()
        scheduler.stop()

    def test_double_start_raises(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            with pytest.raises(SchedulerError, match="state"):
                scheduler.start()
        finally:
            scheduler.stop()

    def test_stop_when_not_running_raises(self) -> None:
        scheduler = Scheduler()
        with pytest.raises(SchedulerError, match="state"):
            scheduler.stop()

    def test_restart_after_stop(self) -> None:
        scheduler = _create_running_scheduler()
        scheduler.stop()
        scheduler.initialize()
        scheduler.start()
        assert scheduler.is_running()
        scheduler.stop()

    def test_initialize_while_running_raises(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            with pytest.raises(SchedulerError, match="state"):
                scheduler.initialize()
        finally:
            scheduler.stop()


class TestSchedulerSchedule:
    def test_schedule_returns_task_id(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            task_id = scheduler.schedule("test", _noop, 1.0)
            assert task_id
            assert isinstance(task_id, str)
        finally:
            scheduler.stop()

    def test_schedule_empty_name_raises(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            with pytest.raises(InputValidationError, match="name"):
                scheduler.schedule("", _noop, 1.0)
        finally:
            scheduler.stop()

    def test_schedule_whitespace_name_raises(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            with pytest.raises(InputValidationError, match="name"):
                scheduler.schedule("   ", _noop, 1.0)
        finally:
            scheduler.stop()

    def test_schedule_not_callable_raises(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            with pytest.raises(InputValidationError, match="callable"):
                scheduler.schedule("test", 42, 1.0)  # type: ignore[arg-type]
        finally:
            scheduler.stop()

    def test_schedule_zero_interval_raises(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            with pytest.raises(InputValidationError, match="positive"):
                scheduler.schedule("test", _noop, 0.0)
        finally:
            scheduler.stop()

    def test_schedule_negative_interval_raises(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            with pytest.raises(InputValidationError, match="positive"):
                scheduler.schedule("test", _noop, -1.0)
        finally:
            scheduler.stop()

    def test_schedule_duplicate_name_raises(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            scheduler.schedule("dup", _noop, 1.0)
            with pytest.raises(InputValidationError, match="already registered"):
                scheduler.schedule("dup", _noop, 2.0)
        finally:
            scheduler.stop()

    def test_schedule_when_not_running_raises(self) -> None:
        scheduler = Scheduler()
        with pytest.raises(SchedulerError, match="not operational"):
            scheduler.schedule("test", _noop, 1.0)

    def test_scheduled_task_executes(self) -> None:
        counter: list[int] = []

        def count() -> None:
            counter.append(1)

        submitted: list[object] = []

        def fake_submit(task: object, /, *_a: object, **_k: object) -> None:
            if callable(task):
                submitted.append(task)
                task()

        scheduler = Scheduler(submit_fn=fake_submit, tick_interval=0.05)
        scheduler.initialize()
        scheduler.start()
        try:
            scheduler.schedule("counter", count, 0.1)
            time.sleep(0.5)
        finally:
            scheduler.stop()
        assert len(counter) >= 2


class TestSchedulerCron:
    def test_schedule_cron_returns_task_id(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            task_id = scheduler.schedule_cron("test", _noop, "* * * * *")
            assert task_id
        finally:
            scheduler.stop()

    def test_schedule_cron_invalid_expression_raises(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            with pytest.raises(InputValidationError, match="cron"):
                scheduler.schedule_cron("test", _noop, "invalid")
        finally:
            scheduler.stop()

    def test_schedule_cron_empty_expression_raises(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            with pytest.raises(InputValidationError, match="empty"):
                scheduler.schedule_cron("test", _noop, "")
        finally:
            scheduler.stop()

    def test_schedule_cron_too_few_fields_raises(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            with pytest.raises(InputValidationError, match="cron"):
                scheduler.schedule_cron("test", _noop, "* * *")
        finally:
            scheduler.stop()

    def test_schedule_cron_too_many_fields_raises(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            with pytest.raises(InputValidationError, match="cron"):
                scheduler.schedule_cron("test", _noop, "* * * * * *")
        finally:
            scheduler.stop()

    def test_schedule_cron_with_ranges(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            task_id = scheduler.schedule_cron("test", _noop, "0-30 9-17 * * 1-5")
            assert task_id
        finally:
            scheduler.stop()

    def test_schedule_cron_with_steps(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            task_id = scheduler.schedule_cron("test", _noop, "*/5 * * * *")
            assert task_id
        finally:
            scheduler.stop()


class TestSchedulerCancel:
    def test_cancel_existing_task(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            task_id = scheduler.schedule("test", _noop, 10.0)
            assert scheduler.cancel(task_id)
            assert scheduler.get_scheduled_task_count() == 0
        finally:
            scheduler.stop()

    def test_cancel_nonexistent_returns_false(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            assert not scheduler.cancel("nonexistent")
        finally:
            scheduler.stop()

    def test_cancel_all(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            scheduler.schedule("a", _noop, 10.0)
            scheduler.schedule("b", _noop, 10.0)
            scheduler.cancel_all()
            assert scheduler.get_scheduled_task_count() == 0
        finally:
            scheduler.stop()


class TestSchedulerHealth:
    def test_healthy_when_running(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            assert scheduler.check_health() == HealthStatus.HEALTHY
        finally:
            scheduler.stop()

    def test_unhealthy_when_not_running(self) -> None:
        scheduler = Scheduler()
        assert scheduler.check_health() == HealthStatus.UNHEALTHY

    def test_component_name(self) -> None:
        scheduler = Scheduler()
        assert scheduler.get_component_name() == "Scheduler"


class TestSchedulerIntrospection:
    def test_get_scheduled_task_count(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            scheduler.schedule("a", _noop, 10.0)
            scheduler.schedule("b", _noop, 10.0)
            assert scheduler.get_scheduled_task_count() == 2
        finally:
            scheduler.stop()

    def test_get_task_names(self) -> None:
        scheduler = _create_running_scheduler()
        try:
            scheduler.schedule("alpha", _noop, 10.0)
            scheduler.schedule("beta", _noop, 10.0)
            names = scheduler.get_task_names()
            assert set(names) == {"alpha", "beta"}
        finally:
            scheduler.stop()


class TestSchedulerThreadSafety:
    def test_concurrent_schedule_and_cancel(self) -> None:
        scheduler = _create_running_scheduler()
        errors: list[Exception] = []
        ids: list[str] = []
        lock = threading.Lock()

        def schedule_tasks(prefix: str) -> None:
            try:
                for i in range(10):
                    tid = scheduler.schedule(
                        f"{prefix}_{i}", _noop, 100.0,
                    )
                    with lock:
                        ids.append(tid)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=schedule_tasks, args=(f"t{t}",))
            for t in range(5)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        scheduler.stop()
        assert not errors
        assert len(ids) == 50
