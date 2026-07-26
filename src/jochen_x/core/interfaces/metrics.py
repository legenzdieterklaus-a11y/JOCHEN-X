"""Metrics collector protocol for runtime observability."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

__all__ = ["IMetricsCollector"]


@runtime_checkable
class IMetricsCollector(Protocol):
    """Protocol for the metrics collection system.

    The metrics collector captures time-series data for runtime
    observability: CPU usage, RAM consumption, thread counts, queue
    fill levels, restart/shutdown counters, and event throughput.

    All operations are thread-safe.  Capture intervals are
    configurable.
    """

    def record(self, name: str, value: float) -> None:
        """Record a metric value at the current timestamp.

        Args:
            name: Metric name (e.g. ``"cpu_usage"``, ``"thread_count"``).
            value: Numeric value to record.

        Raises:
            InputValidationError: If name is empty.

        """
        ...

    def increment(self, name: str, amount: float = 1.0) -> None:
        """Increment a counter metric.

        Args:
            name: Metric name.
            amount: Value to add to the current counter.

        Raises:
            InputValidationError: If name is empty.

        """
        ...

    def get_metric(self, name: str) -> float | None:
        """Return the most recent value for a metric.

        Args:
            name: Metric name.

        Returns:
            The latest value, or ``None`` if the metric has never been
            recorded.

        """
        ...

    def get_all_metrics(self) -> dict[str, float]:
        """Return the most recent value for every recorded metric.

        Returns:
            A mapping of metric names to their latest values.

        """
        ...
