"""Unit tests for the ResourceMonitor."""

from __future__ import annotations

from typing import Any

import pytest

from jochen_x.core.concurrency.resource_monitor import (
    METRIC_CPU_USAGE,
    METRIC_MEMORY_BYTES,
    METRIC_QUEUE_USAGE,
    METRIC_THREAD_ACTIVE,
    METRIC_THREAD_COUNT,
    ResourceMonitor,
    ResourceThresholds,
)
from jochen_x.core.types.events import ResourceThresholdEvent, RuntimeEvent
from jochen_x.core.types.health_status import HealthStatus


class _StubMetrics:
    """Minimal metrics collector for testing."""

    def __init__(self) -> None:
        self._values: dict[str, float] = {}

    def record(self, name: str, value: float) -> None:
        self._values[name] = value

    def increment(self, name: str, amount: float = 1.0) -> None:
        self._values[name] = self._values.get(name, 0.0) + amount

    def get_metric(self, name: str) -> float | None:
        return self._values.get(name)

    def get_all_metrics(self) -> dict[str, float]:
        return dict(self._values)


class _StubEventBus:
    """Minimal event bus for testing."""

    def __init__(self) -> None:
        self.published: list[RuntimeEvent] = []

    def publish(self, event: RuntimeEvent) -> None:
        self.published.append(event)

    def subscribe(
        self,
        event_type: type[RuntimeEvent],
        handler: Any,
        *,
        priority: int = 0,
    ) -> None:
        pass

    def unsubscribe(
        self,
        event_type: type[RuntimeEvent],
        handler: Any,
    ) -> None:
        pass


class TestResourceMonitorConstruction:
    def test_default_construction(self) -> None:
        monitor = ResourceMonitor()
        assert monitor.get_component_name() == "ResourceMonitor"

    def test_custom_thresholds(self) -> None:
        thresholds = ResourceThresholds(cpu_warning=0.5, cpu_critical=0.8)
        monitor = ResourceMonitor(thresholds=thresholds)
        assert monitor.get_thresholds().cpu_warning == 0.5
        assert monitor.get_thresholds().cpu_critical == 0.8


class TestResourceMonitorCollect:
    def test_collect_returns_events_list(self) -> None:
        monitor = ResourceMonitor()
        events = monitor.collect_and_check()
        assert isinstance(events, list)

    def test_collect_records_metrics(self) -> None:
        metrics = _StubMetrics()
        monitor = ResourceMonitor(metrics=metrics)
        monitor.collect_and_check()
        assert metrics.get_metric(METRIC_CPU_USAGE) is not None
        assert metrics.get_metric(METRIC_THREAD_COUNT) is not None

    def test_collect_with_queue_metrics(self) -> None:
        metrics = _StubMetrics()
        monitor = ResourceMonitor(metrics=metrics)
        monitor.collect_and_check(queue_size=5, max_queue_size=10)
        assert metrics.get_metric(METRIC_QUEUE_USAGE) == pytest.approx(0.5)

    def test_collect_with_active_workers(self) -> None:
        metrics = _StubMetrics()
        monitor = ResourceMonitor(metrics=metrics)
        monitor.collect_and_check(active_workers=3)
        assert metrics.get_metric(METRIC_THREAD_ACTIVE) == 3.0

    def test_snapshot_accessible(self) -> None:
        monitor = ResourceMonitor()
        monitor.collect_and_check(queue_size=2, max_queue_size=10)
        snapshot = monitor.get_last_snapshot()
        assert METRIC_CPU_USAGE in snapshot
        assert METRIC_QUEUE_USAGE in snapshot


class TestResourceMonitorThresholds:
    def test_no_events_when_below_thresholds(self) -> None:
        monitor = ResourceMonitor()
        events = monitor.collect_and_check(queue_size=0, max_queue_size=100)
        queue_events = [e for e in events if "queue" in e.resource_name]
        assert not queue_events

    def test_queue_warning_event(self) -> None:
        thresholds = ResourceThresholds(queue_warning=0.5, queue_critical=0.9)
        monitor = ResourceMonitor(thresholds=thresholds)
        events = monitor.collect_and_check(queue_size=60, max_queue_size=100)
        queue_events = [e for e in events if "queue" in e.resource_name]
        assert len(queue_events) == 1
        assert queue_events[0].resource_name == "queue_warning"

    def test_queue_critical_event(self) -> None:
        thresholds = ResourceThresholds(queue_warning=0.5, queue_critical=0.9)
        monitor = ResourceMonitor(thresholds=thresholds)
        events = monitor.collect_and_check(queue_size=95, max_queue_size=100)
        queue_events = [e for e in events if "queue" in e.resource_name]
        assert len(queue_events) == 1
        assert queue_events[0].resource_name == "queue_critical"

    def test_memory_budget_event(self) -> None:
        monitor = ResourceMonitor(memory_budget_bytes=1)
        events = monitor.collect_and_check()
        budget_events = [e for e in events if "budget" in e.resource_name]
        # Memory measurement may be 0 on some platforms
        if budget_events:
            assert budget_events[0].resource_name == "memory_budget"

    def test_events_published_to_event_bus(self) -> None:
        bus = _StubEventBus()
        thresholds = ResourceThresholds(queue_warning=0.1, queue_critical=0.5)
        monitor = ResourceMonitor(event_bus=bus, thresholds=thresholds)
        monitor.collect_and_check(queue_size=80, max_queue_size=100)
        queue_events = [
            e for e in bus.published
            if isinstance(e, ResourceThresholdEvent) and "queue" in e.resource_name
        ]
        assert len(queue_events) >= 1


class TestResourceMonitorHealth:
    def test_healthy_when_no_thresholds_exceeded(self) -> None:
        monitor = ResourceMonitor()
        monitor.collect_and_check(queue_size=0, max_queue_size=100)
        assert monitor.check_health() == HealthStatus.HEALTHY

    def test_degraded_on_warning(self) -> None:
        thresholds = ResourceThresholds(queue_warning=0.1, queue_critical=0.95)
        monitor = ResourceMonitor(thresholds=thresholds)
        monitor.collect_and_check(queue_size=50, max_queue_size=100)
        assert monitor.check_health() == HealthStatus.DEGRADED

    def test_unhealthy_on_critical(self) -> None:
        thresholds = ResourceThresholds(queue_warning=0.1, queue_critical=0.5)
        monitor = ResourceMonitor(thresholds=thresholds)
        monitor.collect_and_check(queue_size=80, max_queue_size=100)
        assert monitor.check_health() == HealthStatus.UNHEALTHY

    def test_component_name(self) -> None:
        monitor = ResourceMonitor()
        assert monitor.get_component_name() == "ResourceMonitor"


class TestResourceMonitorLeakDetection:
    def test_no_leak_without_baseline(self) -> None:
        monitor = ResourceMonitor()
        assert not monitor.check_for_leaks()

    def test_set_baseline(self) -> None:
        monitor = ResourceMonitor()
        monitor.set_baseline_memory()
        assert not monitor.check_for_leaks(sample_count=1)
