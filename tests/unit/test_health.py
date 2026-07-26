"""Unit tests for the HealthMonitor."""

from __future__ import annotations

import threading
from typing import Any

import pytest

from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.observability.health import HealthMonitor
from jochen_x.core.types.events import HealthStatusChangedEvent
from jochen_x.core.types.health_status import HealthStatus

CONCURRENT_COMPONENT_COUNT = 20


class _StubHealthCheck:
    def __init__(
        self,
        name: str,
        status: HealthStatus = HealthStatus.HEALTHY,
    ) -> None:
        self._name = name
        self._status = status

    def check_health(self) -> HealthStatus:
        return self._status

    def get_component_name(self) -> str:
        return self._name

    def set_status(self, status: HealthStatus) -> None:
        self._status = status


class _FailingHealthCheck:
    def check_health(self) -> HealthStatus:
        msg = "check failed"
        raise RuntimeError(msg)

    def get_component_name(self) -> str:
        return "Failing"


class TestHealthMonitorRegistration:
    def test_register_and_get_status_returns_unknown(self) -> None:
        monitor = HealthMonitor()
        check = _StubHealthCheck("comp1")
        monitor.register_check("comp1", check)
        assert monitor.get_status("comp1") == HealthStatus.UNKNOWN

    def test_register_empty_name_raises(self) -> None:
        monitor = HealthMonitor()
        check = _StubHealthCheck("x")
        with pytest.raises(InputValidationError, match="empty"):
            monitor.register_check("", check)

    def test_register_duplicate_name_raises(self) -> None:
        monitor = HealthMonitor()
        check = _StubHealthCheck("comp1")
        monitor.register_check("comp1", check)
        with pytest.raises(
            InputValidationError, match="already registered",
        ):
            monitor.register_check("comp1", check)

    def test_unregister_removes_component(self) -> None:
        monitor = HealthMonitor()
        check = _StubHealthCheck("comp1")
        monitor.register_check("comp1", check)
        monitor.unregister_check("comp1")
        with pytest.raises(
            InputValidationError, match="not registered",
        ):
            monitor.get_status("comp1")

    def test_unregister_unknown_is_noop(self) -> None:
        monitor = HealthMonitor()
        monitor.unregister_check("nonexistent")

    def test_get_status_unregistered_raises(self) -> None:
        monitor = HealthMonitor()
        with pytest.raises(
            InputValidationError, match="not registered",
        ):
            monitor.get_status("unknown")


class TestHealthMonitorOverallStatus:
    def test_no_components_returns_healthy(self) -> None:
        monitor = HealthMonitor()
        assert monitor.get_overall_status() == HealthStatus.HEALTHY

    def test_all_healthy_returns_healthy(self) -> None:
        monitor = HealthMonitor()
        for i in range(3):
            check = _StubHealthCheck(f"c{i}")
            monitor.register_check(f"c{i}", check)
        monitor.run_checks()
        assert monitor.get_overall_status() == HealthStatus.HEALTHY

    def test_one_degraded_returns_degraded(self) -> None:
        monitor = HealthMonitor()
        c1 = _StubHealthCheck("c1", HealthStatus.HEALTHY)
        c2 = _StubHealthCheck("c2", HealthStatus.DEGRADED)
        monitor.register_check("c1", c1)
        monitor.register_check("c2", c2)
        monitor.run_checks()
        assert monitor.get_overall_status() == HealthStatus.DEGRADED

    def test_unhealthy_beats_degraded(self) -> None:
        monitor = HealthMonitor()
        c1 = _StubHealthCheck("c1", HealthStatus.DEGRADED)
        c2 = _StubHealthCheck("c2", HealthStatus.UNHEALTHY)
        monitor.register_check("c1", c1)
        monitor.register_check("c2", c2)
        monitor.run_checks()
        assert monitor.get_overall_status() == HealthStatus.UNHEALTHY

    def test_unknown_beats_healthy(self) -> None:
        monitor = HealthMonitor()
        c1 = _StubHealthCheck("c1", HealthStatus.HEALTHY)
        monitor.register_check("c1", c1)
        assert monitor.get_overall_status() == HealthStatus.UNKNOWN


class TestHealthMonitorRunChecks:
    def test_status_change_emits_event(self) -> None:
        monitor = HealthMonitor()
        check = _StubHealthCheck("comp1", HealthStatus.HEALTHY)
        monitor.register_check("comp1", check)

        events = monitor.run_checks()
        assert len(events) == 1
        assert isinstance(events[0], HealthStatusChangedEvent)
        assert events[0].component_name == "comp1"
        assert events[0].old_status == HealthStatus.UNKNOWN
        assert events[0].new_status == HealthStatus.HEALTHY

    def test_no_change_emits_nothing(self) -> None:
        monitor = HealthMonitor()
        check = _StubHealthCheck("comp1", HealthStatus.HEALTHY)
        monitor.register_check("comp1", check)
        monitor.run_checks()
        events = monitor.run_checks()
        assert events == []

    def test_transition_emits_event(self) -> None:
        monitor = HealthMonitor()
        check = _StubHealthCheck("comp1", HealthStatus.HEALTHY)
        monitor.register_check("comp1", check)
        monitor.run_checks()

        check.set_status(HealthStatus.DEGRADED)
        events = monitor.run_checks()
        assert len(events) == 1
        assert events[0].old_status == HealthStatus.HEALTHY
        assert events[0].new_status == HealthStatus.DEGRADED

    def test_failing_check_results_in_unhealthy(self) -> None:
        monitor = HealthMonitor()
        check: Any = _FailingHealthCheck()
        monitor.register_check("bad", check)

        events = monitor.run_checks()
        assert len(events) == 1
        assert events[0].new_status == HealthStatus.UNHEALTHY
        assert monitor.get_status("bad") == HealthStatus.UNHEALTHY

    def test_run_checks_after_unregister(self) -> None:
        monitor = HealthMonitor()
        check = _StubHealthCheck("comp1", HealthStatus.HEALTHY)
        monitor.register_check("comp1", check)
        monitor.run_checks()
        monitor.unregister_check("comp1")
        events = monitor.run_checks()
        assert events == []


class TestHealthMonitorIntrospection:
    def test_get_all_statuses(self) -> None:
        monitor = HealthMonitor()
        c1 = _StubHealthCheck("a", HealthStatus.HEALTHY)
        c2 = _StubHealthCheck("b", HealthStatus.DEGRADED)
        monitor.register_check("a", c1)
        monitor.register_check("b", c2)
        monitor.run_checks()
        statuses = monitor.get_all_statuses()
        assert statuses == {
            "a": HealthStatus.HEALTHY,
            "b": HealthStatus.DEGRADED,
        }

    def test_get_registered_components(self) -> None:
        monitor = HealthMonitor()
        monitor.register_check("x", _StubHealthCheck("x"))
        monitor.register_check("y", _StubHealthCheck("y"))
        names = monitor.get_registered_components()
        assert set(names) == {"x", "y"}

    def test_self_health_check(self) -> None:
        monitor = HealthMonitor()
        assert monitor.check_health() == HealthStatus.HEALTHY
        assert monitor.get_component_name() == "HealthMonitor"


class TestHealthMonitorThreadSafety:
    def test_concurrent_register_and_check(self) -> None:
        monitor = HealthMonitor()
        errors: list[Exception] = []

        def register_and_check(idx: int) -> None:
            try:
                name = f"comp_{idx}"
                check = _StubHealthCheck(name)
                monitor.register_check(name, check)
                monitor.run_checks()
                monitor.get_status(name)
                monitor.get_overall_status()
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(
                target=register_and_check, args=(i,),
            )
            for i in range(CONCURRENT_COMPONENT_COUNT)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        registered = monitor.get_registered_components()
        assert len(registered) == CONCURRENT_COMPONENT_COUNT
