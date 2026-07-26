"""Thread-safe metrics collection with time-series support.

The ``MetricsCollector`` captures numeric metrics with timestamps
for runtime observability.  It supports both gauge-style recording
(``record``) and counter-style incrementing (``increment``).

All operations are thread-safe.  Capture intervals are configurable
through the ``max_history_per_metric`` parameter.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import UTC, datetime
from threading import RLock

from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.types.health_status import HealthStatus

__all__ = ["MetricDataPoint", "MetricsCollector"]

_COMPONENT_NAME = "MetricsCollector"
_FIELD_NAME = "name"
_FIELD_VALUE = "value"
_FIELD_AMOUNT = "amount"
_FIELD_MAX_HISTORY = "max_history_per_metric"
_REASON_EMPTY_NAME = "Metric name must not be empty"
_REASON_NOT_FINITE = "Value must be finite"
_REASON_MIN_ONE = "must be at least 1"

DEFAULT_MAX_HISTORY = 1_000


@dataclass(frozen=True, slots=True)
class MetricDataPoint:
    """A single metric observation with its timestamp.

    Args:
        timestamp: UTC timestamp of the observation.
        value: Numeric value recorded.

    """

    timestamp: datetime
    value: float


def _is_finite(v: float) -> bool:
    """Return True if *v* is a finite number."""
    try:
        return v == v and v != float("inf") and v != float("-inf")  # noqa: PLR0124
    except (TypeError, ValueError):
        return False


class MetricsCollector:
    """Thread-safe metrics collector with time-series history.

    Records numeric metric values with UTC timestamps.  Each metric
    retains up to ``max_history_per_metric`` data points in a FIFO
    buffer.

    Counters are stored as cumulative gauge values — ``increment``
    adds to the latest value (defaulting to 0.0 if the counter has
    not been initialised).

    Args:
        max_history_per_metric: Maximum number of data points to
            retain per metric name.

    """

    def __init__(
        self,
        *,
        max_history_per_metric: int = DEFAULT_MAX_HISTORY,
    ) -> None:
        """Initialise an empty metrics collector."""
        if max_history_per_metric < 1:
            raise InputValidationError(
                _FIELD_MAX_HISTORY,
                _REASON_MIN_ONE,
                component=_COMPONENT_NAME,
            )
        self._max_history: int = max_history_per_metric
        self._lock: RLock = RLock()
        self._series: dict[str, deque[MetricDataPoint]] = {}

    # -- IMetricsCollector protocol ------------------------------------------

    def record(self, name: str, value: float) -> None:
        """Record a metric value at the current timestamp.

        Args:
            name: Metric name (e.g. ``"cpu_usage"``).
            value: Numeric value to record.

        Raises:
            InputValidationError: If name is empty or value is not
                finite.

        """
        self._validate_name(name)
        self._validate_finite(value, _FIELD_VALUE)

        point = MetricDataPoint(
            timestamp=datetime.now(UTC),
            value=value,
        )

        with self._lock:
            series = self._series.get(name)
            if series is None:
                series = deque(maxlen=self._max_history)
                self._series[name] = series
            series.append(point)

    def increment(self, name: str, amount: float = 1.0) -> None:
        """Increment a counter metric.

        Adds *amount* to the current counter value.  If the counter
        has never been recorded, it starts at 0.0 before the
        increment.

        Args:
            name: Metric name.
            amount: Value to add to the current counter.

        Raises:
            InputValidationError: If name is empty or amount is not
                finite.

        """
        self._validate_name(name)
        self._validate_finite(amount, _FIELD_AMOUNT)

        with self._lock:
            series = self._series.get(name)
            current: float = 0.0
            if series and len(series) > 0:
                current = series[-1].value

            new_value = current + amount

        self.record(name, new_value)

    def get_metric(self, name: str) -> float | None:
        """Return the most recent value for a metric.

        Args:
            name: Metric name.

        Returns:
            The latest value, or ``None`` if the metric has never
            been recorded.

        """
        with self._lock:
            series = self._series.get(name)
            if series is None or len(series) == 0:
                return None
            return series[-1].value

    def get_all_metrics(self) -> dict[str, float]:
        """Return the most recent value for every recorded metric.

        Returns:
            A mapping of metric names to their latest values.

        """
        with self._lock:
            result: dict[str, float] = {}
            for name, series in self._series.items():
                if len(series) > 0:
                    result[name] = series[-1].value
            return result

    # -- Time-series access --------------------------------------------------

    def get_history(self, name: str) -> list[MetricDataPoint]:
        """Return the full history for a metric.

        Args:
            name: Metric name.

        Returns:
            A list of data points ordered by timestamp, oldest first.
            Empty list if the metric has never been recorded.

        """
        with self._lock:
            series = self._series.get(name)
            if series is None:
                return []
            return list(series)

    def get_metric_names(self) -> list[str]:
        """Return all metric names that have been recorded.

        Returns:
            A list of metric names.

        """
        with self._lock:
            return list(self._series.keys())

    def clear(self) -> None:
        """Clear all recorded metrics."""
        with self._lock:
            self._series.clear()

    # -- IHealthCheck protocol -----------------------------------------------

    def check_health(self) -> HealthStatus:
        """Return the health status of the metrics collector.

        The collector is always healthy as long as it exists.

        Returns:
            ``HealthStatus.HEALTHY``.

        """
        return HealthStatus.HEALTHY

    def get_component_name(self) -> str:
        """Return the component name.

        Returns:
            The string ``"MetricsCollector"``.

        """
        return _COMPONENT_NAME

    # -- Validation ----------------------------------------------------------

    @staticmethod
    def _validate_name(name: str) -> None:
        """Raise if *name* is empty."""
        if not name:
            raise InputValidationError(
                _FIELD_NAME,
                _REASON_EMPTY_NAME,
                component=_COMPONENT_NAME,
            )

    @staticmethod
    def _validate_finite(value: float, field_name: str) -> None:
        """Raise if *value* is not finite."""
        if not _is_finite(value):
            raise InputValidationError(
                field_name,
                _REASON_NOT_FINITE,
                component=_COMPONENT_NAME,
            )
