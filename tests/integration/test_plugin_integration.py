"""Integration tests for plugin lifecycle, isolation, and observability.

Tests verify the plugin infrastructure against real runtime
components (EventBus, AuditLog, HealthMonitor, StructuredLogger)
instead of mocks.
"""

from __future__ import annotations

import time

import pytest

from jochen_x.core.events.bus import EventBus
from jochen_x.core.exceptions.plugin import (
    PluginError,
    PluginIsolationError,
    PluginLifecycleError,
    PluginLoadError,
)
from jochen_x.core.interfaces.plugin_context import IPluginContext
from jochen_x.core.observability.audit import AuditLog
from jochen_x.core.observability.health import HealthMonitor
from jochen_x.core.observability.logging import StructuredLogger
from jochen_x.core.plugin.registry import PluginRegistry, PluginState
from jochen_x.core.registry.service_registry import ServiceRegistry
from jochen_x.core.types.events import (
    PluginAction,
    PluginLifecycleEvent,
    RuntimeEvent,
)
from jochen_x.core.types.health_status import HealthStatus
from jochen_x.core.types.severity import LogSeverity


# ---------------------------------------------------------------------------
# Test plugins
# ---------------------------------------------------------------------------


class GoodPlugin:
    """Plugin that completes all lifecycle callbacks successfully."""

    def __init__(self) -> None:
        self.lifecycle: list[PluginAction] = []
        self.context: IPluginContext | None = None

    def on_load(self, context: IPluginContext) -> None:
        self.context = context
        self.lifecycle.append(PluginAction.LOAD)

    def on_initialize(self) -> None:
        self.lifecycle.append(PluginAction.INITIALIZE)

    def on_enable(self) -> None:
        self.lifecycle.append(PluginAction.ENABLE)

    def on_disable(self) -> None:
        self.lifecycle.append(PluginAction.DISABLE)

    def on_unload(self) -> None:
        self.lifecycle.append(PluginAction.UNLOAD)


class CrashingPlugin:
    """Plugin that crashes on a specified action."""

    def __init__(self, crash_on: PluginAction) -> None:
        self._crash_on: PluginAction = crash_on

    def on_load(self, context: IPluginContext) -> None:
        if self._crash_on == PluginAction.LOAD:
            msg = "Crash during LOAD"
            raise RuntimeError(msg)

    def on_initialize(self) -> None:
        if self._crash_on == PluginAction.INITIALIZE:
            msg = "Crash during INITIALIZE"
            raise RuntimeError(msg)

    def on_enable(self) -> None:
        if self._crash_on == PluginAction.ENABLE:
            msg = "Crash during ENABLE"
            raise RuntimeError(msg)

    def on_disable(self) -> None:
        if self._crash_on == PluginAction.DISABLE:
            msg = "Crash during DISABLE"
            raise RuntimeError(msg)

    def on_unload(self) -> None:
        if self._crash_on == PluginAction.UNLOAD:
            msg = "Crash during UNLOAD"
            raise RuntimeError(msg)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def event_bus() -> EventBus:
    bus = EventBus()
    bus.initialize()
    bus.start()
    yield bus
    if bus.is_running():
        bus.stop()


@pytest.fixture()
def audit_log() -> AuditLog:
    return AuditLog()


@pytest.fixture()
def logger() -> StructuredLogger:
    lg = StructuredLogger(default_level=LogSeverity.DEBUG)
    lg.initialize()
    lg.start()
    yield lg
    lg.stop()


@pytest.fixture()
def service_registry() -> ServiceRegistry:
    return ServiceRegistry()


@pytest.fixture()
def health_monitor() -> HealthMonitor:
    return HealthMonitor()


@pytest.fixture()
def plugin_registry(
    event_bus: EventBus,
    audit_log: AuditLog,
    logger: StructuredLogger,
    service_registry: ServiceRegistry,
    health_monitor: HealthMonitor,
) -> PluginRegistry:
    return PluginRegistry(
        event_bus=event_bus,
        audit_log=audit_log,
        logger=logger,
        service_registry=service_registry,
        health_monitor=health_monitor,
    )


# ===================================================================
# Integration Tests
# ===================================================================


class TestFullLifecycleIntegration:
    """End-to-end lifecycle with real runtime components."""

    def test_complete_lifecycle(
        self, plugin_registry: PluginRegistry
    ) -> None:
        plugin = GoodPlugin()

        plugin_registry.load_plugin("alpha", plugin)
        assert plugin_registry.get_plugin_state("alpha") == PluginState.LOADED

        plugin_registry.initialize_plugin("alpha")
        assert (
            plugin_registry.get_plugin_state("alpha")
            == PluginState.INITIALIZED
        )

        plugin_registry.enable_plugin("alpha")
        assert (
            plugin_registry.get_plugin_state("alpha") == PluginState.ENABLED
        )

        plugin_registry.disable_plugin("alpha")
        assert (
            plugin_registry.get_plugin_state("alpha") == PluginState.DISABLED
        )

        plugin_registry.unload_plugin("alpha")
        assert plugin_registry.has_plugin("alpha") is False

        assert plugin.lifecycle == [
            PluginAction.LOAD,
            PluginAction.INITIALIZE,
            PluginAction.ENABLE,
            PluginAction.DISABLE,
            PluginAction.UNLOAD,
        ]

    def test_context_provides_event_bus(
        self, plugin_registry: PluginRegistry, event_bus: EventBus
    ) -> None:
        plugin = GoodPlugin()
        plugin_registry.load_plugin("alpha", plugin)

        assert plugin.context is not None
        bus = plugin.context.get_event_bus()
        assert bus is event_bus


class TestAuditIntegration:
    """Verify audit log records all lifecycle transitions."""

    def test_all_transitions_audited(
        self,
        plugin_registry: PluginRegistry,
        audit_log: AuditLog,
    ) -> None:
        plugin = GoodPlugin()

        plugin_registry.load_plugin("alpha", plugin)
        plugin_registry.initialize_plugin("alpha")
        plugin_registry.enable_plugin("alpha")
        plugin_registry.disable_plugin("alpha")
        plugin_registry.unload_plugin("alpha")

        entries = audit_log.get_entries(limit=100)
        lifecycle_entries = [
            e for e in entries if isinstance(e, PluginLifecycleEvent)
        ]

        actions = [e.action for e in lifecycle_entries]
        assert PluginAction.LOAD in actions
        assert PluginAction.INITIALIZE in actions
        assert PluginAction.ENABLE in actions
        assert PluginAction.DISABLE in actions
        assert PluginAction.UNLOAD in actions

    def test_audit_integrity_after_lifecycle(
        self,
        plugin_registry: PluginRegistry,
        audit_log: AuditLog,
    ) -> None:
        plugin = GoodPlugin()
        plugin_registry.load_plugin("alpha", plugin)
        plugin_registry.initialize_plugin("alpha")

        assert audit_log.verify_integrity() is True

    def test_failed_action_audited(
        self,
        plugin_registry: PluginRegistry,
        audit_log: AuditLog,
    ) -> None:
        plugin = CrashingPlugin(crash_on=PluginAction.LOAD)

        with pytest.raises(PluginLoadError):
            plugin_registry.load_plugin("broken", plugin)

        entries = audit_log.get_entries(limit=100)
        lifecycle_entries = [
            e for e in entries if isinstance(e, PluginLifecycleEvent)
        ]

        failures = [e for e in lifecycle_entries if not e.success]
        assert len(failures) >= 1


class TestEventBusIntegration:
    """Verify lifecycle events arrive on the real EventBus."""

    def test_lifecycle_events_published(
        self,
        plugin_registry: PluginRegistry,
        event_bus: EventBus,
    ) -> None:
        received: list[PluginLifecycleEvent] = []

        def handler(event: RuntimeEvent) -> None:
            if isinstance(event, PluginLifecycleEvent):
                received.append(event)

        event_bus.subscribe(PluginLifecycleEvent, handler)

        plugin = GoodPlugin()
        plugin_registry.load_plugin("alpha", plugin)
        plugin_registry.initialize_plugin("alpha")

        time.sleep(0.1)

        actions = [e.action for e in received]
        assert PluginAction.LOAD in actions
        assert PluginAction.INITIALIZE in actions


class TestHealthMonitorIntegration:
    """Verify health monitoring with real HealthMonitor."""

    def test_plugin_registered_with_health_monitor(
        self,
        plugin_registry: PluginRegistry,
        health_monitor: HealthMonitor,
    ) -> None:
        plugin_registry.load_plugin("alpha", GoodPlugin())

        assert "Plugin[alpha]" in health_monitor.get_registered_components()

    def test_plugin_unregistered_from_health_monitor(
        self,
        plugin_registry: PluginRegistry,
        health_monitor: HealthMonitor,
    ) -> None:
        plugin_registry.load_plugin("alpha", GoodPlugin())
        plugin_registry.unload_plugin("alpha")

        assert (
            "Plugin[alpha]" not in health_monitor.get_registered_components()
        )

    def test_health_status_tracks_plugin_sandbox(
        self,
        plugin_registry: PluginRegistry,
        health_monitor: HealthMonitor,
    ) -> None:
        plugin_registry.load_plugin("alpha", GoodPlugin())
        health_monitor.run_checks()

        status = health_monitor.get_status("Plugin[alpha]")
        assert status == HealthStatus.HEALTHY


class TestPluginIsolationIntegration:
    """Verify isolation with real runtime components."""

    def test_crashing_plugin_does_not_affect_good_plugin(
        self, plugin_registry: PluginRegistry
    ) -> None:
        crashing = CrashingPlugin(crash_on=PluginAction.INITIALIZE)
        good = GoodPlugin()

        plugin_registry.load_plugin("crash", crashing)
        plugin_registry.load_plugin("good", good)

        with pytest.raises(PluginError):
            plugin_registry.initialize_plugin("crash")

        plugin_registry.initialize_plugin("good")
        plugin_registry.enable_plugin("good")

        assert (
            plugin_registry.get_plugin_state("good") == PluginState.ENABLED
        )

    def test_context_disposed_after_unload(
        self, plugin_registry: PluginRegistry
    ) -> None:
        plugin = GoodPlugin()
        plugin_registry.load_plugin("alpha", plugin)

        ctx = plugin_registry.get_plugin_context("alpha")
        plugin_registry.unload_plugin("alpha")

        with pytest.raises(PluginIsolationError):
            ctx.get_event_bus()

    def test_multiple_plugins_independent_lifecycle(
        self, plugin_registry: PluginRegistry
    ) -> None:
        plugins = {f"p{i}": GoodPlugin() for i in range(5)}

        for pid, p in plugins.items():
            plugin_registry.load_plugin(pid, p)
            plugin_registry.initialize_plugin(pid)
            plugin_registry.enable_plugin(pid)

        plugin_registry.disable_plugin("p2")
        plugin_registry.unload_plugin("p2")

        for pid in ["p0", "p1", "p3", "p4"]:
            assert (
                plugin_registry.get_plugin_state(pid) == PluginState.ENABLED
            )

        assert plugin_registry.has_plugin("p2") is False

    def test_unload_with_callback_failure_still_completes(
        self, plugin_registry: PluginRegistry
    ) -> None:
        crashing = CrashingPlugin(crash_on=PluginAction.UNLOAD)
        plugin_registry.load_plugin("crash", crashing)

        plugin_registry.unload_plugin("crash")

        assert plugin_registry.has_plugin("crash") is False

    def test_illegal_transitions_rejected(
        self, plugin_registry: PluginRegistry
    ) -> None:
        plugin_registry.load_plugin("alpha", GoodPlugin())

        with pytest.raises(PluginLifecycleError):
            plugin_registry.enable_plugin("alpha")

        assert (
            plugin_registry.get_plugin_state("alpha") == PluginState.LOADED
        )
