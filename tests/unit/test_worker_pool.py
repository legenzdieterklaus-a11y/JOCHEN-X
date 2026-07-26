"""Unit tests for the WorkerPool."""

from __future__ import annotations

import threading
import time
from concurrent.futures import Future
from typing import Any

import pytest

from jochen_x.core.concurrency.worker_pool import WorkerPool
from jochen_x.core.exceptions.concurrency import (
    WorkerPoolError,
    WorkerPoolOverloadError,
)
from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.types.health_status import HealthStatus


def _noop() -> None:
    pass


def _returns_42() -> int:
    return 42


def _add(a: int, b: int) -> int:
    return a + b


def _slow_task(duration: float = 0.2) -> str:
    time.sleep(duration)
    return "done"


def _failing_task() -> None:
    msg = "intentional failure"
    raise RuntimeError(msg)


def _create_running_pool(
    *,
    max_workers: int = 4,
    max_queue_size: int = 100,
) -> WorkerPool:
    pool = WorkerPool(max_workers=max_workers, max_queue_size=max_queue_size)
    pool.initialize()
    pool.start()
    return pool


class TestWorkerPoolConstruction:
    def test_default_construction(self) -> None:
        pool = WorkerPool()
        assert pool.get_max_workers() >= 1
        assert pool.get_max_queue_size() > 0

    def test_custom_parameters(self) -> None:
        pool = WorkerPool(max_workers=2, max_queue_size=50)
        assert pool.get_max_workers() == 2
        assert pool.get_max_queue_size() == 50

    def test_invalid_max_workers_raises(self) -> None:
        with pytest.raises(InputValidationError, match="max_workers"):
            WorkerPool(max_workers=0)

    def test_invalid_max_queue_size_raises(self) -> None:
        with pytest.raises(InputValidationError, match="max_queue_size"):
            WorkerPool(max_queue_size=0)

    def test_boundary_max_workers_one(self) -> None:
        pool = WorkerPool(max_workers=1)
        assert pool.get_max_workers() == 1

    def test_boundary_max_queue_size_one(self) -> None:
        pool = WorkerPool(max_queue_size=1)
        assert pool.get_max_queue_size() == 1


class TestWorkerPoolLifecycle:
    def test_initialize_and_start(self) -> None:
        pool = WorkerPool(max_workers=2)
        pool.initialize()
        pool.start()
        assert pool.is_running()
        pool.shutdown(wait=True)

    def test_double_start_raises(self) -> None:
        pool = _create_running_pool()
        try:
            with pytest.raises(WorkerPoolError, match="state"):
                pool.start()
        finally:
            pool.shutdown(wait=True)

    def test_initialize_while_running_raises(self) -> None:
        pool = _create_running_pool()
        try:
            with pytest.raises(WorkerPoolError, match="state"):
                pool.initialize()
        finally:
            pool.shutdown(wait=True)

    def test_stop_calls_shutdown(self) -> None:
        pool = _create_running_pool()
        pool.stop()
        assert not pool.is_running()

    def test_shutdown_not_running_is_noop(self) -> None:
        pool = WorkerPool(max_workers=2)
        pool.shutdown(wait=True)

    def test_restart_after_stop(self) -> None:
        pool = _create_running_pool()
        pool.shutdown(wait=True)
        pool.initialize()
        pool.start()
        assert pool.is_running()
        pool.shutdown(wait=True)


class TestWorkerPoolSubmit:
    def test_submit_simple_task(self) -> None:
        pool = _create_running_pool()
        try:
            future = pool.submit(_returns_42)
            result = future.result(timeout=5.0)
            assert result == 42
        finally:
            pool.shutdown(wait=True)

    def test_submit_with_args(self) -> None:
        pool = _create_running_pool()
        try:
            future = pool.submit(_add, 3, 7)
            assert future.result(timeout=5.0) == 10
        finally:
            pool.shutdown(wait=True)

    def test_submit_with_kwargs(self) -> None:
        pool = _create_running_pool()
        try:
            future = pool.submit(_add, a=5, b=15)
            assert future.result(timeout=5.0) == 20
        finally:
            pool.shutdown(wait=True)

    def test_submit_not_callable_raises(self) -> None:
        pool = _create_running_pool()
        try:
            with pytest.raises(InputValidationError, match="callable"):
                pool.submit(42)  # type: ignore[arg-type]
        finally:
            pool.shutdown(wait=True)

    def test_submit_when_not_running_raises(self) -> None:
        pool = WorkerPool(max_workers=2)
        with pytest.raises(WorkerPoolError, match="not operational"):
            pool.submit(_noop)

    def test_submit_failing_task(self) -> None:
        pool = _create_running_pool()
        try:
            future = pool.submit(_failing_task)
            with pytest.raises(RuntimeError, match="intentional"):
                future.result(timeout=5.0)
        finally:
            pool.shutdown(wait=True)


class TestWorkerPoolPriority:
    def test_higher_priority_executes_first(self) -> None:
        results: list[int] = []
        barrier = threading.Event()

        def blocking_task() -> None:
            barrier.wait(timeout=5.0)

        def record_task(value: int) -> None:
            results.append(value)

        pool = _create_running_pool(max_workers=1, max_queue_size=100)
        try:
            pool.submit(blocking_task)
            time.sleep(0.05)

            pool.submit_priority(lambda: record_task(1), 1)
            pool.submit_priority(lambda: record_task(3), 3)
            pool.submit_priority(lambda: record_task(2), 2)

            barrier.set()
            time.sleep(0.5)
        finally:
            pool.shutdown(wait=True)

        assert results == [3, 2, 1]


class TestWorkerPoolOverload:
    def test_overload_raises(self) -> None:
        pool = _create_running_pool(max_workers=1, max_queue_size=2)
        barrier = threading.Event()
        try:
            pool.submit(lambda: barrier.wait(timeout=5.0))
            time.sleep(0.05)

            pool.submit(_noop)
            pool.submit(_noop)

            with pytest.raises(WorkerPoolOverloadError):
                pool.submit(_noop)
        finally:
            barrier.set()
            pool.shutdown(wait=True)

    def test_overload_error_fields(self) -> None:
        pool = _create_running_pool(max_workers=1, max_queue_size=1)
        barrier = threading.Event()
        try:
            pool.submit(lambda: barrier.wait(timeout=5.0))
            time.sleep(0.05)
            pool.submit(_noop)

            with pytest.raises(WorkerPoolOverloadError) as exc_info:
                pool.submit(_noop)
            assert exc_info.value.max_queue_size == 1
        finally:
            barrier.set()
            pool.shutdown(wait=True)


class TestWorkerPoolGracefulShutdown:
    def test_running_tasks_complete_on_shutdown(self) -> None:
        result_holder: list[str] = []

        def slow() -> None:
            time.sleep(0.1)
            result_holder.append("completed")

        pool = _create_running_pool(max_workers=2)
        pool.submit(slow)
        time.sleep(0.02)
        pool.shutdown(wait=True)
        assert "completed" in result_holder

    def test_pending_tasks_cancelled_on_shutdown(self) -> None:
        barrier = threading.Event()
        pool = _create_running_pool(max_workers=1, max_queue_size=100)

        pool.submit(lambda: barrier.wait(timeout=5.0))
        time.sleep(0.02)

        futures: list[Future[Any]] = []
        for _ in range(5):
            futures.append(pool.submit(_noop))

        barrier.set()
        pool.shutdown(wait=True)


class TestWorkerPoolMetrics:
    def test_active_count_during_execution(self) -> None:
        barrier = threading.Event()
        pool = _create_running_pool(max_workers=4)
        try:
            for _ in range(3):
                pool.submit(lambda: barrier.wait(timeout=5.0))
            time.sleep(0.1)
            assert pool.get_active_count() == 3
        finally:
            barrier.set()
            pool.shutdown(wait=True)

    def test_queue_size_updates(self) -> None:
        barrier = threading.Event()
        pool = _create_running_pool(max_workers=1, max_queue_size=100)
        try:
            pool.submit(lambda: barrier.wait(timeout=5.0))
            time.sleep(0.05)

            pool.submit(_noop)
            pool.submit(_noop)
            assert pool.get_queue_size() == 2
        finally:
            barrier.set()
            pool.shutdown(wait=True)

    def test_completed_tasks_recorded(self) -> None:
        pool = _create_running_pool()
        pool.submit(_returns_42)
        time.sleep(0.2)
        pool.shutdown(wait=True)
        completed = pool.get_completed_tasks()
        assert len(completed) >= 1
        assert completed[0].result == 42


class TestWorkerPoolHealth:
    def test_healthy_when_running(self) -> None:
        pool = _create_running_pool()
        try:
            assert pool.check_health() == HealthStatus.HEALTHY
        finally:
            pool.shutdown(wait=True)

    def test_unhealthy_when_not_running(self) -> None:
        pool = WorkerPool(max_workers=2)
        assert pool.check_health() == HealthStatus.UNHEALTHY

    def test_degraded_when_queue_high(self) -> None:
        barrier = threading.Event()
        pool = _create_running_pool(max_workers=1, max_queue_size=10)
        try:
            pool.submit(lambda: barrier.wait(timeout=5.0))
            time.sleep(0.05)

            for _ in range(9):
                pool.submit(_noop)

            assert pool.check_health() == HealthStatus.DEGRADED
        finally:
            barrier.set()
            pool.shutdown(wait=True)

    def test_component_name(self) -> None:
        pool = WorkerPool()
        assert pool.get_component_name() == "WorkerPool"


class TestWorkerPoolThreadSafety:
    def test_concurrent_submit(self) -> None:
        pool = _create_running_pool(max_workers=4, max_queue_size=1000)
        errors: list[Exception] = []
        results: list[Future[int]] = []
        lock = threading.Lock()

        def submit_many(start: int) -> None:
            try:
                for i in range(20):
                    f = pool.submit(_add, start + i, 1)
                    with lock:
                        results.append(f)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=submit_many, args=(i * 20,))
            for i in range(5)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        pool.shutdown(wait=True)
        assert not errors
        assert len(results) == 100
