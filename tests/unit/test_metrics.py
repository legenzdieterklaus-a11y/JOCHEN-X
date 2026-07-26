"""Unit tests for the MetricsCollector."""

from __future__ import annotations

import threading

import pytest

from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.observability.metrics import MetricsCollector
from jochen_x.core.types.health_status import HealthStatus

HISTORY_LIMIT = 5
HISTORY_FIRST_VALUE = 5.0
HISTORY_LAST_VALUE = 9.0
CPU_VALUE = 45.5
FIRST_RECORD = 10.0
SECOND_RECORD = 20.0
EXPECTED_TWO = 2
NEGATIVE_RECORD = -42.5
INCREMENT_BASE = 10.0
INCREMENT_AMOUNT = 5.0
INCREMENT_RESULT = 15.0
CUSTOM_INCREMENT = 3.5
DECREMENT_AMOUNT = -3.0
DECREMENT_RESULT = 7.0
CONCURRENT_METRIC_COUNT = 10
RECORDS_PER_THREAD = 100
CONCURRENT_THREADS = 10
INCREMENTS_PER_THREAD = 100
EXPECTED_LOG_COUNT = 250


class TestMetricsCollectorInit:
    def test_default_init(self) -> None:
        collector = MetricsCollector()
        assert collector.get_all_metrics() == {}

    def test_custom_max_history(self) -> None:
        collector = MetricsCollector(max_history_per_metric=HISTORY_LIMIT)
        for i in range(10):
            collector.record("m", float(i))
        history = collector.get_history("m")
        assert len(history) == HISTORY_LIMIT
        assert history[0].value == HISTORY_FIRST_VALUE
        assert history[-1].value == HISTORY_LAST_VALUE

    def test_zero_max_history_raises(self) -> None:
        with pytest.raises(InputValidationError, match="at least 1"):
            MetricsCollector(max_history_per_metric=0)

    def test_negative_max_history_raises(self) -> None:
        with pytest.raises(InputValidationError, match="at least 1"):
            MetricsCollector(max_history_per_metric=-1)


class TestMetricsCollectorRecord:
    def test_record_and_get(self) -> None:
        collector = MetricsCollector()
        collector.record("cpu", CPU_VALUE)
        assert collector.get_metric("cpu") == CPU_VALUE

    def test_record_multiple_values(self) -> None:
        collector = MetricsCollector()
        collector.record("cpu", FIRST_RECORD)
        collector.record("cpu", SECOND_RECORD)
        assert collector.get_metric("cpu") == SECOND_RECORD
        assert len(collector.get_history("cpu")) == EXPECTED_TWO

    def test_record_empty_name_raises(self) -> None:
        collector = MetricsCollector()
        with pytest.raises(InputValidationError, match="empty"):
            collector.record("", 1.0)

    def test_record_nan_raises(self) -> None:
        collector = MetricsCollector()
        with pytest.raises(InputValidationError, match="finite"):
            collector.record("m", float("nan"))

    def test_record_inf_raises(self) -> None:
        collector = MetricsCollector()
        with pytest.raises(InputValidationError, match="finite"):
            collector.record("m", float("inf"))

    def test_record_neg_inf_raises(self) -> None:
        collector = MetricsCollector()
        with pytest.raises(InputValidationError, match="finite"):
            collector.record("m", float("-inf"))

    def test_record_zero(self) -> None:
        collector = MetricsCollector()
        collector.record("m", 0.0)
        assert collector.get_metric("m") == 0.0

    def test_record_negative_value(self) -> None:
        collector = MetricsCollector()
        collector.record("m", NEGATIVE_RECORD)
        assert collector.get_metric("m") == NEGATIVE_RECORD


class TestMetricsCollectorIncrement:
    def test_increment_new_counter(self) -> None:
        collector = MetricsCollector()
        collector.increment("count")
        assert collector.get_metric("count") == 1.0

    def test_increment_existing_counter(self) -> None:
        collector = MetricsCollector()
        collector.record("count", INCREMENT_BASE)
        collector.increment("count", INCREMENT_AMOUNT)
        assert collector.get_metric("count") == INCREMENT_RESULT

    def test_increment_custom_amount(self) -> None:
        collector = MetricsCollector()
        collector.increment("count", CUSTOM_INCREMENT)
        assert collector.get_metric("count") == CUSTOM_INCREMENT

    def test_increment_empty_name_raises(self) -> None:
        collector = MetricsCollector()
        with pytest.raises(InputValidationError, match="empty"):
            collector.increment("")

    def test_increment_nan_amount_raises(self) -> None:
        collector = MetricsCollector()
        with pytest.raises(InputValidationError, match="finite"):
            collector.increment("m", float("nan"))

    def test_increment_negative_amount(self) -> None:
        collector = MetricsCollector()
        collector.record("m", INCREMENT_BASE)
        collector.increment("m", DECREMENT_AMOUNT)
        assert collector.get_metric("m") == DECREMENT_RESULT


class TestMetricsCollectorGet:
    def test_get_nonexistent_returns_none(self) -> None:
        collector = MetricsCollector()
        assert collector.get_metric("unknown") is None

    def test_get_all_metrics(self) -> None:
        collector = MetricsCollector()
        collector.record("a", 1.0)
        collector.record("b", 2.0)
        result = collector.get_all_metrics()
        assert result == {"a": 1.0, "b": 2.0}

    def test_get_all_metrics_empty(self) -> None:
        collector = MetricsCollector()
        assert collector.get_all_metrics() == {}

    def test_get_history_nonexistent(self) -> None:
        collector = MetricsCollector()
        assert collector.get_history("unknown") == []

    def test_get_history_ordered(self) -> None:
        collector = MetricsCollector()
        collector.record("m", 1.0)
        collector.record("m", 2.0)
        collector.record("m", 3.0)
        history = collector.get_history("m")
        assert [p.value for p in history] == [1.0, 2.0, 3.0]
        ts = [p.timestamp for p in history]
        assert ts[0] <= ts[1] <= ts[EXPECTED_TWO]

    def test_get_metric_names(self) -> None:
        collector = MetricsCollector()
        collector.record("alpha", 1.0)
        collector.record("beta", 2.0)
        names = collector.get_metric_names()
        assert set(names) == {"alpha", "beta"}


class TestMetricsCollectorClear:
    def test_clear_removes_all(self) -> None:
        collector = MetricsCollector()
        collector.record("a", 1.0)
        collector.record("b", 2.0)
        collector.clear()
        assert collector.get_all_metrics() == {}
        assert collector.get_metric_names() == []


class TestMetricsCollectorHealthCheck:
    def test_health_check(self) -> None:
        collector = MetricsCollector()
        assert collector.check_health() == HealthStatus.HEALTHY
        assert collector.get_component_name() == "MetricsCollector"


class TestMetricsCollectorThreadSafety:
    def test_concurrent_record_and_read(self) -> None:
        collector = MetricsCollector()
        errors: list[Exception] = []

        def record_values(start: int) -> None:
            try:
                for i in range(RECORDS_PER_THREAD):
                    collector.record(
                        f"metric_{start}", float(i),
                    )
                    collector.get_metric(f"metric_{start}")
                    collector.get_all_metrics()
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=record_values, args=(i,))
            for i in range(CONCURRENT_THREADS)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        names = collector.get_metric_names()
        assert len(names) == CONCURRENT_METRIC_COUNT

    def test_concurrent_increment(self) -> None:
        collector = MetricsCollector()
        errors: list[Exception] = []

        def increment_counter() -> None:
            try:
                for _ in range(INCREMENTS_PER_THREAD):
                    collector.increment("shared_counter", 1.0)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=increment_counter)
            for _ in range(CONCURRENT_THREADS)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        value = collector.get_metric("shared_counter")
        assert value is not None
        assert value > 0


class TestMetricsDataPointTimestamp:
    def test_data_point_has_timestamp(self) -> None:
        collector = MetricsCollector()
        collector.record("m", 1.0)
        history = collector.get_history("m")
        assert len(history) == 1
        assert history[0].timestamp is not None
        assert history[0].value == 1.0
