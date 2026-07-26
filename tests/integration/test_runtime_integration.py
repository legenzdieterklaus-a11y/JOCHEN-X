"""Integration tests for the RuntimeHost full lifecycle."""

from __future__ import annotations

import threading
import time

import pytest

from jochen_x.core.runtime.host import RuntimeHost
from jochen_x.core.types.runtime_state import RuntimeState

THREAD_COUNT = 10


@pytest.fixture
def host() -> RuntimeHost:
    return RuntimeHost()


class TestFullBootstrapSequence:
    def test_start_executes_all_nine_steps(self, host: RuntimeHost) -> None:
        host.start()
        assert host.get_state() == RuntimeState.RUNNING
        assert host.event_bus is not None
        assert host.service_registry is not None
        assert host.health_monitor is not None
        assert host.metrics is not None
        assert host.recovery_handler is not None
        assert host.plugin_registry is not None
        assert host.worker_pool is not None
        assert host.scheduler is not None
        host.stop()


class TestShutdownSequence:
    def test_stop_cleans_up_all_services(self, host: RuntimeHost) -> None:
        host.start()
        host.stop()
        assert host.get_state() == RuntimeState.STOPPED
        assert host.event_bus is None
        assert host.worker_pool is None
        assert host.scheduler is None
        assert host.recovery_handler is None


class TestLifecycleTransitions:
    def test_full_lifecycle(self, host: RuntimeHost) -> None:
        assert host.get_state() == RuntimeState.CREATED
        host.start()
        assert host.get_state() == RuntimeState.RUNNING
        host.pause()
        assert host.get_state() == RuntimeState.PAUSED
        host.resume()
        assert host.get_state() == RuntimeState.RUNNING
        host.stop()
        assert host.get_state() == RuntimeState.STOPPED

    def test_restart_cycle(self, host: RuntimeHost) -> None:
        host.start()
        host.restart()
        assert host.get_state() == RuntimeState.RUNNING
        host.stop()


class TestRecoveryFlow:
    def test_stop_from_failed_state(self, host: RuntimeHost) -> None:
        host.start()
        assert host.lifecycle is not None
        host.lifecycle.fail()
        assert host.get_state() == RuntimeState.FAILED
        host.stop()


class TestFullRuntimeConcurrency:
    def test_concurrent_start_stop(self) -> None:
        errors: list[Exception] = []

        def run() -> None:
            try:
                h = RuntimeHost()
                h.start()
                time.sleep(0.01)
                h.stop()
            except Exception as exc:
                errors.append(exc)

        threads = [
            threading.Thread(target=run) for _ in range(THREAD_COUNT)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=30)

        assert not errors
