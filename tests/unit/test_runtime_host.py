"""Unit tests for the RuntimeHost."""

from __future__ import annotations

import pytest

from jochen_x.core.exceptions.lifecycle import IllegalStateTransitionError
from jochen_x.core.exceptions.runtime import RuntimeStartError
from jochen_x.core.interfaces.event_bus import IEventBus
from jochen_x.core.interfaces.health import IHealthMonitor
from jochen_x.core.interfaces.metrics import IMetricsCollector
from jochen_x.core.interfaces.recovery import IRecoveryHandler
from jochen_x.core.interfaces.scheduler import IScheduler
from jochen_x.core.interfaces.service_registry import IServiceRegistry
from jochen_x.core.interfaces.worker_pool import IWorkerPool
from jochen_x.core.runtime.host import RuntimeHost
from jochen_x.core.types.health_status import HealthStatus
from jochen_x.core.types.runtime_state import RuntimeState


@pytest.fixture
def host() -> RuntimeHost:
    return RuntimeHost()


class TestRuntimeHostInit:
    def test_initial_state_is_created(self, host: RuntimeHost) -> None:
        assert host.get_state() == RuntimeState.CREATED

    def test_component_name(self, host: RuntimeHost) -> None:
        assert host.get_component_name() == "RuntimeHost"

    def test_health_unknown_before_start(self, host: RuntimeHost) -> None:
        assert host.check_health() == HealthStatus.UNKNOWN

    def test_services_none_before_start(self, host: RuntimeHost) -> None:
        assert host.event_bus is None
        assert host.service_registry is None
        assert host.health_monitor is None
        assert host.metrics is None
        assert host.recovery_handler is None
        assert host.plugin_registry is None
        assert host.worker_pool is None
        assert host.scheduler is None
        assert host.lifecycle is None


class TestRuntimeHostStart:
    def test_start_reaches_running(self, host: RuntimeHost) -> None:
        host.start()
        assert host.get_state() == RuntimeState.RUNNING
        host.stop()

    def test_start_creates_all_services(self, host: RuntimeHost) -> None:
        host.start()
        assert host.event_bus is not None
        assert host.service_registry is not None
        assert host.health_monitor is not None
        assert host.metrics is not None
        assert host.recovery_handler is not None
        assert host.plugin_registry is not None
        assert host.worker_pool is not None
        assert host.scheduler is not None
        assert host.lifecycle is not None
        host.stop()

    def test_service_registry_has_interfaces(
        self, host: RuntimeHost,
    ) -> None:
        host.start()
        reg = host.service_registry
        assert reg is not None
        assert reg.has(IEventBus)
        assert reg.has(IMetricsCollector)
        assert reg.has(IHealthMonitor)
        assert reg.has(IWorkerPool)
        assert reg.has(IScheduler)
        assert reg.has(IRecoveryHandler)
        assert reg.has(IServiceRegistry)
        host.stop()

    def test_double_start_raises(self, host: RuntimeHost) -> None:
        host.start()
        with pytest.raises(
            (RuntimeStartError, IllegalStateTransitionError),
        ):
            host.start()
        host.stop()


class TestRuntimeHostStop:
    def test_stop_reaches_stopped(self, host: RuntimeHost) -> None:
        host.start()
        host.stop()
        assert host.get_state() == RuntimeState.STOPPED

    def test_stop_without_start_is_noop(self, host: RuntimeHost) -> None:
        host.stop()
        assert host.get_state() == RuntimeState.CREATED

    def test_double_stop_is_safe(self, host: RuntimeHost) -> None:
        host.start()
        host.stop()
        host.stop()

    def test_services_cleaned_after_stop(self, host: RuntimeHost) -> None:
        host.start()
        host.stop()
        assert host.event_bus is None
        assert host.worker_pool is None
        assert host.scheduler is None
        assert host.recovery_handler is None
        assert host.plugin_registry is None


class TestRuntimeHostPauseResume:
    def test_pause_and_resume(self, host: RuntimeHost) -> None:
        host.start()
        host.pause()
        assert host.get_state() == RuntimeState.PAUSED
        host.resume()
        assert host.get_state() == RuntimeState.RUNNING
        host.stop()

    def test_pause_without_start_raises(self, host: RuntimeHost) -> None:
        with pytest.raises(RuntimeStartError):
            host.pause()

    def test_resume_without_start_raises(self, host: RuntimeHost) -> None:
        with pytest.raises(RuntimeStartError):
            host.resume()


class TestRuntimeHostRestart:
    def test_restart_reaches_running(self, host: RuntimeHost) -> None:
        host.start()
        host.restart()
        assert host.get_state() == RuntimeState.RUNNING
        host.stop()


class TestRuntimeHostHealth:
    def test_health_not_unhealthy_when_running(
        self, host: RuntimeHost,
    ) -> None:
        host.start()
        status = host.check_health()
        assert status != HealthStatus.UNHEALTHY
        host.stop()
