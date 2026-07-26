"""Resource monitoring for the JOCHEN X Core Runtime.

The ``ResourceMonitor`` tracks CPU usage, RAM consumption, queue
utilisation, and thread counts.  When configured thresholds are
exceeded it emits ``ResourceThresholdEvent`` and adjusts the
component's health status.

All operations are thread-safe.
"""

from __future__ import annotations

import contextlib
import ctypes
import ctypes.wintypes
import os
import sys
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.interfaces.event_bus import IEventBus
from jochen_x.core.interfaces.metrics import IMetricsCollector
from jochen_x.core.types.events import ResourceThresholdEvent
from jochen_x.core.types.health_status import HealthStatus

__all__ = ["ResourceMonitor", "ResourceThresholds"]

_COMPONENT_NAME = "ResourceMonitor"

_FIELD_CPU = "cpu_threshold"
_FIELD_MEMORY = "memory_threshold"
_FIELD_QUEUE = "queue_threshold"
_FIELD_THREAD = "thread_threshold"
_REASON_RANGE = "must be between 0.0 and 1.0"
_REASON_POSITIVE = "must be positive"

METRIC_CPU_USAGE = "cpu_usage"
METRIC_MEMORY_USAGE = "memory_usage"
METRIC_MEMORY_BYTES = "memory_bytes"
METRIC_THREAD_COUNT = "thread_count"
METRIC_THREAD_ACTIVE = "thread_active"
METRIC_QUEUE_USAGE = "queue_usage"


@dataclass(frozen=True, kw_only=True, slots=True)
class ResourceThresholds:
    """Configurable thresholds for resource monitoring.

    All threshold values are fractions between 0.0 and 1.0
    representing the utilisation ratio at which alerts trigger.

    Args:
        cpu_warning: CPU usage fraction for DEGRADED status.
        cpu_critical: CPU usage fraction for UNHEALTHY status.
        memory_warning: Memory usage fraction for DEGRADED status.
        memory_critical: Memory usage fraction for UNHEALTHY status.
        queue_warning: Queue fill fraction for DEGRADED status.
        queue_critical: Queue fill fraction for UNHEALTHY status.
        max_threads: Maximum allowed thread count.

    """

    cpu_warning: float = 0.8
    cpu_critical: float = 0.95
    memory_warning: float = 0.8
    memory_critical: float = 0.95
    queue_warning: float = 0.7
    queue_critical: float = 0.9
    max_threads: int = 200


def _get_process_memory() -> int:
    """Return the current process RSS in bytes (platform-safe)."""
    if sys.platform == "win32":
        return _get_process_memory_win32()
    return _get_process_memory_posix()


def _get_process_memory_win32() -> int:
    """Return process memory on Windows via kernel32."""
    try:

        class _ProcessMemoryCounters(ctypes.Structure):
            _fields_ = [
                ("cb", ctypes.wintypes.DWORD),
                ("PageFaultCount", ctypes.wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
            ]

        counters = _ProcessMemoryCounters()
        counters.cb = ctypes.sizeof(_ProcessMemoryCounters)
        kernel32 = ctypes.windll.kernel32
        process = kernel32.GetCurrentProcess()
        psapi = ctypes.windll.psapi
        if psapi.GetProcessMemoryInfo(
            process,
            ctypes.byref(counters),
            ctypes.sizeof(counters),
        ):
            return int(counters.WorkingSetSize)
    except (OSError, AttributeError, ValueError):
        pass
    return 0


def _get_process_memory_posix() -> int:
    """Return process memory on POSIX via /proc/self/status."""
    try:
        with Path("/proc/self/status").open() as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    parts = line.split()
                    return int(parts[1]) * 1024
    except (OSError, ValueError, IndexError):
        pass
    return 0


def _get_cpu_percent() -> float:
    """Return a rough CPU usage estimate (platform-safe)."""
    try:
        if hasattr(os, "getloadavg"):
            load: tuple[float, float, float] = os.getloadavg()
            cpu_count = os.cpu_count() or 1
            return min(load[0] / cpu_count, 1.0)
    except OSError:
        pass
    return 0.0


def _validate_fraction(value: float, field_name: str) -> None:
    """Raise if *value* is not between 0.0 and 1.0."""
    if not (0.0 <= value <= 1.0):
        raise InputValidationError(
            field_name,
            _REASON_RANGE,
            component=_COMPONENT_NAME,
        )


@dataclass(slots=True)
class _ResourceSnapshot:
    """Point-in-time resource measurements."""

    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    memory_bytes: int = 0
    thread_count: int = 0
    active_threads: int = 0
    queue_usage: float = 0.0


class ResourceMonitor:
    """Monitors system resource utilisation and emits threshold alerts.

    Collects CPU, memory, thread, and queue metrics.  When thresholds
    are exceeded, emits ``ResourceThresholdEvent`` via the EventBus
    and adjusts the component health status.

    The monitor does not run its own timer — it exposes a
    ``collect_and_check`` method that should be called periodically
    by the ``Scheduler``.

    Args:
        metrics: Metrics collector for recording measurements.
        event_bus: Event bus for threshold alerts (optional).
        thresholds: Resource thresholds configuration.
        memory_budget_bytes: Maximum memory budget in bytes (0 = no
            limit).

    """

    def __init__(
        self,
        *,
        metrics: IMetricsCollector | None = None,
        event_bus: IEventBus | None = None,
        thresholds: ResourceThresholds | None = None,
        memory_budget_bytes: int = 0,
    ) -> None:
        """Initialise the resource monitor."""
        self._metrics: IMetricsCollector | None = metrics
        self._event_bus: IEventBus | None = event_bus
        self._thresholds: ResourceThresholds = thresholds or ResourceThresholds()
        self._memory_budget_bytes: int = memory_budget_bytes
        self._lock: threading.RLock = threading.RLock()
        self._health_status: HealthStatus = HealthStatus.HEALTHY
        self._last_snapshot: _ResourceSnapshot = _ResourceSnapshot()
        self._threshold_events: list[ResourceThresholdEvent] = []
        self._baseline_memory: int = 0
        self._leak_samples: list[int] = []

    # -- Public API -------------------------------------------------------------

    def collect_and_check(
        self,
        *,
        queue_size: int = 0,
        max_queue_size: int = 1,
        active_workers: int = 0,
    ) -> list[ResourceThresholdEvent]:
        """Collect resource metrics and check thresholds.

        This method should be called periodically by the Scheduler.
        It reads system metrics, records them via the metrics
        collector, checks against configured thresholds, and returns
        any threshold breach events.

        Args:
            queue_size: Current WorkerPool queue size.
            max_queue_size: Maximum WorkerPool queue capacity.
            active_workers: Number of currently active workers.

        Returns:
            A list of threshold breach events.

        """
        snapshot = self._collect_snapshot(
            queue_size=queue_size,
            max_queue_size=max_queue_size,
            active_workers=active_workers,
        )

        with self._lock:
            self._last_snapshot = snapshot

        self._record_metrics(snapshot)
        events = self._check_thresholds(snapshot)

        with self._lock:
            self._threshold_events = events
            self._update_health(events)

        if self._event_bus is not None:
            for event in events:
                with contextlib.suppress(Exception):
                    self._event_bus.publish(event)

        return events

    def set_baseline_memory(self) -> None:
        """Set the current memory usage as the baseline for leak detection."""
        snapshot = self._collect_snapshot()
        with self._lock:
            self._baseline_memory = snapshot.memory_bytes
            self._leak_samples.clear()

    def check_for_leaks(self, *, sample_count: int = 10) -> bool:
        """Check for memory leaks by comparing against baseline.

        A leak is detected when the current memory exceeds the
        baseline by more than 50% after enough samples.

        Args:
            sample_count: Minimum number of samples needed before
                a leak can be detected.

        Returns:
            True if a potential memory leak is detected.

        """
        snapshot = self._collect_snapshot()
        with self._lock:
            if self._baseline_memory == 0:
                return False
            self._leak_samples.append(snapshot.memory_bytes)
            if len(self._leak_samples) < sample_count:
                return False
            recent = self._leak_samples[-sample_count:]
            avg = sum(recent) / len(recent)
            return avg > self._baseline_memory * 1.5

    # -- IHealthCheck protocol --------------------------------------------------

    def check_health(self) -> HealthStatus:
        """Return the health status based on resource utilisation.

        Returns:
            The current health status.

        """
        with self._lock:
            return self._health_status

    def get_component_name(self) -> str:
        """Return the component name.

        Returns:
            The string ``"ResourceMonitor"``.

        """
        return _COMPONENT_NAME

    # -- Introspection ----------------------------------------------------------

    def get_last_snapshot(self) -> dict[str, Any]:
        """Return the most recent resource snapshot.

        Returns:
            A dictionary of resource metric names to values.

        """
        with self._lock:
            snap = self._last_snapshot
        return {
            METRIC_CPU_USAGE: snap.cpu_percent,
            METRIC_MEMORY_USAGE: snap.memory_percent,
            METRIC_MEMORY_BYTES: snap.memory_bytes,
            METRIC_THREAD_COUNT: snap.thread_count,
            METRIC_THREAD_ACTIVE: snap.active_threads,
            METRIC_QUEUE_USAGE: snap.queue_usage,
        }

    def get_thresholds(self) -> ResourceThresholds:
        """Return the current threshold configuration.

        Returns:
            The active resource thresholds.

        """
        return self._thresholds

    # -- Internal ---------------------------------------------------------------

    @staticmethod
    def _collect_snapshot(
        *,
        queue_size: int = 0,
        max_queue_size: int = 1,
        active_workers: int = 0,
    ) -> _ResourceSnapshot:
        """Collect current system resource metrics.

        Args:
            queue_size: Current queue size.
            max_queue_size: Maximum queue capacity.
            active_workers: Number of active workers.

        Returns:
            A resource snapshot.

        """
        memory_bytes = _get_process_memory()
        cpu_percent = _get_cpu_percent()
        thread_count = threading.active_count()
        queue_ratio = queue_size / max(max_queue_size, 1)

        return _ResourceSnapshot(
            cpu_percent=cpu_percent,
            memory_percent=0.0,
            memory_bytes=memory_bytes,
            thread_count=thread_count,
            active_threads=active_workers,
            queue_usage=queue_ratio,
        )

    def _record_metrics(self, snapshot: _ResourceSnapshot) -> None:
        """Record snapshot values to the metrics collector.

        Args:
            snapshot: The resource snapshot to record.

        """
        if self._metrics is None:
            return
        self._metrics.record(METRIC_CPU_USAGE, snapshot.cpu_percent)
        self._metrics.record(METRIC_MEMORY_BYTES, float(snapshot.memory_bytes))
        self._metrics.record(METRIC_THREAD_COUNT, float(snapshot.thread_count))
        self._metrics.record(METRIC_THREAD_ACTIVE, float(snapshot.active_threads))
        self._metrics.record(METRIC_QUEUE_USAGE, snapshot.queue_usage)

    def _check_thresholds(
        self,
        snapshot: _ResourceSnapshot,
    ) -> list[ResourceThresholdEvent]:
        """Check snapshot values against configured thresholds.

        Args:
            snapshot: The resource snapshot to check.

        Returns:
            A list of threshold breach events.

        """
        events: list[ResourceThresholdEvent] = []

        if snapshot.cpu_percent > self._thresholds.cpu_critical:
            events.append(self._make_event(
                "cpu_critical",
                snapshot.cpu_percent,
                self._thresholds.cpu_critical,
            ))
        elif snapshot.cpu_percent > self._thresholds.cpu_warning:
            events.append(self._make_event(
                "cpu_warning",
                snapshot.cpu_percent,
                self._thresholds.cpu_warning,
            ))

        if snapshot.queue_usage > self._thresholds.queue_critical:
            events.append(self._make_event(
                "queue_critical",
                snapshot.queue_usage,
                self._thresholds.queue_critical,
            ))
        elif snapshot.queue_usage > self._thresholds.queue_warning:
            events.append(self._make_event(
                "queue_warning",
                snapshot.queue_usage,
                self._thresholds.queue_warning,
            ))

        if snapshot.thread_count > self._thresholds.max_threads:
            events.append(self._make_event(
                "thread_count",
                float(snapshot.thread_count),
                float(self._thresholds.max_threads),
            ))

        if (
            self._memory_budget_bytes > 0
            and snapshot.memory_bytes > self._memory_budget_bytes
        ):
            events.append(self._make_event(
                "memory_budget",
                float(snapshot.memory_bytes),
                float(self._memory_budget_bytes),
            ))

        return events

    def _update_health(
        self,
        events: list[ResourceThresholdEvent],
    ) -> None:
        """Update health status based on threshold events.

        Must be called with ``self._lock`` held.

        Args:
            events: The threshold events from the current check.

        """
        if not events:
            self._health_status = HealthStatus.HEALTHY
            return

        has_critical = any(
            "critical" in e.resource_name or "budget" in e.resource_name
            for e in events
        )
        if has_critical:
            self._health_status = HealthStatus.UNHEALTHY
        else:
            self._health_status = HealthStatus.DEGRADED

    @staticmethod
    def _make_event(
        resource_name: str,
        current: float,
        threshold: float,
    ) -> ResourceThresholdEvent:
        """Create a threshold breach event.

        Args:
            resource_name: Name of the breached resource.
            current: Current measured value.
            threshold: Configured threshold value.

        Returns:
            A new ``ResourceThresholdEvent``.

        """
        return ResourceThresholdEvent(
            resource_name=resource_name,
            current_value=current,
            threshold_value=threshold,
            source=_COMPONENT_NAME,
        )
