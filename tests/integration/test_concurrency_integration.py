"""Integration tests for the concurrency subsystem.

Tests the interaction between WorkerPool, Scheduler, and
ResourceMonitor.
"""

from __future__ import annotations

import threading
import time

import pytest

from jochen_x.core.concurrency.resource_monitor import ResourceMonitor
from jochen_x.core.concurrency.scheduler import Scheduler
from jochen_x.core.concurrency.worker_pool import WorkerPool
from jochen_x.core.observability.metrics import MetricsCollector
from jochen_x.core.types.health_status import HealthStatus


class TestWorkerPoolSchedulerIntegration:
    def test_scheduler_dispatches_through_worker_pool(self) -> None:
        counter: list[int] = []
        lock = threading.Lock()

        def count() -> None:
            with lock:
                counter.append(1)

        pool = WorkerPool(max_workers=4)
        pool.initialize()
        pool.start()

        scheduler = Scheduler(submit_fn=pool.submit, tick_interval=0.05)
        scheduler.initialize()
        scheduler.start()

        try:
            scheduler.schedule("counter", count, 0.1)
            time.sleep(0.6)
        finally:
            scheduler.stop()
            pool.shutdown(wait=True)

        assert len(counter) >= 3

    def test_scheduler_stops_before_pool(self) -> None:
        pool = WorkerPool(max_workers=2)
        pool.initialize()
        pool.start()

        scheduler = Scheduler(submit_fn=pool.submit, tick_interval=0.1)
        scheduler.initialize()
        scheduler.start()

        scheduler.stop()
        pool.shutdown(wait=True)

        assert not scheduler.is_running()
        assert not pool.is_running()

    def test_multiple_scheduled_tasks_execute(self) -> None:
        results_a: list[int] = []
        results_b: list[int] = []
        lock = threading.Lock()

        def task_a() -> None:
            with lock:
                results_a.append(1)

        def task_b() -> None:
            with lock:
                results_b.append(1)

        pool = WorkerPool(max_workers=4)
        pool.initialize()
        pool.start()

        scheduler = Scheduler(submit_fn=pool.submit, tick_interval=0.05)
        scheduler.initialize()
        scheduler.start()

        try:
            scheduler.schedule("task_a", task_a, 0.1)
            scheduler.schedule("task_b", task_b, 0.1)
            time.sleep(0.6)
        finally:
            scheduler.stop()
            pool.shutdown(wait=True)

        assert len(results_a) >= 2
        assert len(results_b) >= 2


class TestResourceMonitorIntegration:
    def test_resource_monitor_with_metrics_collector(self) -> None:
        metrics = MetricsCollector()
        pool = WorkerPool(max_workers=2, max_queue_size=100)
        pool.initialize()
        pool.start()

        monitor = ResourceMonitor(metrics=metrics)

        try:
            events = monitor.collect_and_check(
                queue_size=pool.get_queue_size(),
                max_queue_size=pool.get_max_queue_size(),
                active_workers=pool.get_active_count(),
            )
            assert isinstance(events, list)
            assert metrics.get_metric("cpu_usage") is not None
        finally:
            pool.shutdown(wait=True)

    def test_resource_monitor_scheduled_collection(self) -> None:
        metrics = MetricsCollector()
        pool = WorkerPool(max_workers=2, max_queue_size=100)
        pool.initialize()
        pool.start()

        monitor = ResourceMonitor(metrics=metrics)
        collection_count: list[int] = []
        lock = threading.Lock()

        def collect() -> None:
            monitor.collect_and_check(
                queue_size=pool.get_queue_size(),
                max_queue_size=pool.get_max_queue_size(),
                active_workers=pool.get_active_count(),
            )
            with lock:
                collection_count.append(1)

        scheduler = Scheduler(submit_fn=pool.submit, tick_interval=0.05)
        scheduler.initialize()
        scheduler.start()

        try:
            scheduler.schedule("resource_check", collect, 0.1)
            time.sleep(0.5)
        finally:
            scheduler.stop()
            pool.shutdown(wait=True)

        assert len(collection_count) >= 2


class TestConcurrencyHealthIntegration:
    def test_all_components_report_health(self) -> None:
        pool = WorkerPool(max_workers=2)
        pool.initialize()
        pool.start()

        scheduler = Scheduler(submit_fn=pool.submit, tick_interval=0.1)
        scheduler.initialize()
        scheduler.start()

        monitor = ResourceMonitor()

        try:
            assert pool.check_health() == HealthStatus.HEALTHY
            assert scheduler.check_health() == HealthStatus.HEALTHY
            monitor.collect_and_check()
            assert monitor.check_health() == HealthStatus.HEALTHY
        finally:
            scheduler.stop()
            pool.shutdown(wait=True)

    def test_pool_health_after_shutdown(self) -> None:
        pool = WorkerPool(max_workers=2)
        pool.initialize()
        pool.start()
        pool.shutdown(wait=True)
        assert pool.check_health() == HealthStatus.UNHEALTHY


class TestConcurrencyUnderLoad:
    def test_high_throughput_execution(self) -> None:
        results: list[int] = []
        lock = threading.Lock()

        def work(n: int) -> int:
            with lock:
                results.append(n)
            return n

        pool = WorkerPool(max_workers=8, max_queue_size=1000)
        pool.initialize()
        pool.start()

        try:
            futures = [pool.submit(work, i) for i in range(100)]
            for f in futures:
                f.result(timeout=10.0)
        finally:
            pool.shutdown(wait=True)

        assert len(results) == 100
        assert set(results) == set(range(100))

    def test_graceful_shutdown_under_load(self) -> None:
        barrier = threading.Event()
        completed: list[str] = []
        lock = threading.Lock()

        def slow_task(name: str) -> None:
            barrier.wait(timeout=5.0)
            with lock:
                completed.append(name)

        pool = WorkerPool(max_workers=4, max_queue_size=100)
        pool.initialize()
        pool.start()

        for i in range(4):
            pool.submit(slow_task, f"task_{i}")
        time.sleep(0.05)

        barrier.set()
        pool.shutdown(wait=True)

        assert len(completed) == 4
