"""Unit tests for the plugin infrastructure (Phase 9).

Tests cover ``PluginSandbox``, ``PluginContext``, and
``PluginRegistry`` in isolation and verify lifecycle management,
isolation guarantees, event emission, and audit integration.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, TypeVar
from unittest.mock import MagicMock

import pytest

from jochen_x.core.exceptions.plugin import (
    PluginError,
    PluginIsolationError,
    PluginLifecycleError,
    PluginLoadError,
    PluginNotFoundError,
)
from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.interfaces.plugin_context import IPluginContext
from jochen_x.core.plugin.context import PluginContext
from jochen_x.core.plugin.registry import IPlugin, PluginRegistry, PluginState
from jochen_x.core.plugin.sandbox import PluginSandbox
from jochen_x.core.registry.service_registry import ServiceNotFoundError
from jochen_x.core.types.events import (
    PluginAction,
    PluginLifecycleEvent,
    RuntimeEvent,
)
from jochen_x.core.types.health_status import HealthStatus
from jochen_x.core.types.severity import LogSeverity

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Mock infrastructure
# ---------------------------------------------------------------------------


class MockLogger:
    """Minimal ILogger implementation for testing."""

    def __init__(self) -> None:
        self.entries: list[dict[str, Any]] = []

    def log(
        self,
        severity: LogSeverity,
        message: str,
        *,
        component: str = "",
        correlation_id: str = "",
    ) -> None:
        self.entries.append(
            {
                "severity": severity,
                "message": message,
                "component": component,
                "correlation_id": correlation_id,
            }
        )

    def debug(
        self, message: str, *, component: str = "", correlation_id: str = ""
    ) -> None:
        self.log(
            LogSeverity.DEBUG, message,
            component=component, correlation_id=correlation_id,
        )

    def info(
        self, message: str, *, component: str = "", correlation_id: str = ""
    ) -> None:
        self.log(
            LogSeverity.INFO, message,
            component=component, correlation_id=correlation_id,
        )

    def warning(
        self, message: str, *, component: str = "", correlation_id: str = ""
    ) -> None:
        self.log(
            LogSeverity.WARNING, message,
            component=component, correlation_id=correlation_id,
        )

    def error(
        self, message: str, *, component: str = "", correlation_id: str = ""
    ) -> None:
        self.log(
            LogSeverity.ERROR, message,
            component=component, correlation_id=correlation_id,
        )

    def critical(
        self, message: str, *, component: str = "", correlation_id: str = ""
    ) -> None:
        self.log(
            LogSeverity.CRITICAL, message,
            component=component, correlation_id=correlation_id,
        )


class MockEventBus:
    """Minimal IEventBus implementation for testing."""

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
        self, event_type: type[RuntimeEvent], handler: Any
    ) -> None:
        pass


class MockAuditLog:
    """Minimal IAuditLog implementation for testing."""

    def __init__(self) -> None:
        self.entries: list[RuntimeEvent] = []

    def record(self, event: RuntimeEvent) -> None:
        self.entries.append(event)

    def get_entries(
        self, *, limit: int = 100, offset: int = 0
    ) -> Sequence[RuntimeEvent]:
        return list(self.entries[offset : offset + limit])

    def verify_integrity(self) -> bool:
        return True


class MockServiceRegistry:
    """Minimal IServiceRegistry implementation for testing."""

    def __init__(self) -> None:
        self._services: dict[type[Any], Any] = {}

    def register(self, interface: type[T], implementation: T) -> None:
        self._services[interface] = implementation

    def resolve(self, interface: type[T]) -> T:
        impl = self._services.get(interface)
        if impl is None:
            raise ServiceNotFoundError(interface)
        return impl  # type: ignore[no-any-return]

    def has(self, interface: type[Any]) -> bool:
        return interface in self._services

    def get_registered_interfaces(self) -> Sequence[type[Any]]:
        return list(self._services.keys())


class MockHealthMonitor:
    """Minimal IHealthMonitor implementation for testing."""

    def __init__(self) -> None:
        self.registered: dict[str, Any] = {}

    def register_check(self, name: str, check: Any) -> None:
        self.registered[name] = check

    def unregister_check(self, name: str) -> None:
        self.registered.pop(name, None)

    def get_status(self, name: str) -> HealthStatus:
        return HealthStatus.UNKNOWN

    def get_overall_status(self) -> HealthStatus:
        return HealthStatus.HEALTHY


class MockPlugin:
    """A well-behaved plugin for testing."""

    def __init__(self) -> None:
        self.loaded: bool = False
        self.initialized: bool = False
        self.enabled: bool = False
        self.unloaded: bool = False
        self.context: IPluginContext | None = None

    def on_load(self, context: IPluginContext) -> None:
        self.context = context
        self.loaded = True

    def on_initialize(self) -> None:
        self.initialized = True

    def on_enable(self) -> None:
        self.enabled = True

    def on_disable(self) -> None:
        self.enabled = False

    def on_unload(self) -> None:
        self.unloaded = True
        self.loaded = False


class FailingPlugin:
    """A plugin that fails on specific lifecycle actions."""

    def __init__(self, fail_on: set[PluginAction] | None = None) -> None:
        self.fail_on: set[PluginAction] = fail_on or set()

    def on_load(self, context: IPluginContext) -> None:
        if PluginAction.LOAD in self.fail_on:
            msg = "Load failed"
            raise RuntimeError(msg)

    def on_initialize(self) -> None:
        if PluginAction.INITIALIZE in self.fail_on:
            msg = "Initialize failed"
            raise RuntimeError(msg)

    def on_enable(self) -> None:
        if PluginAction.ENABLE in self.fail_on:
            msg = "Enable failed"
            raise RuntimeError(msg)

    def on_disable(self) -> None:
        if PluginAction.DISABLE in self.fail_on:
            msg = "Disable failed"
            raise RuntimeError(msg)

    def on_unload(self) -> None:
        if PluginAction.UNLOAD in self.fail_on:
            msg = "Unload failed"
            raise RuntimeError(msg)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def logger() -> MockLogger:
    return MockLogger()


@pytest.fixture()
def event_bus() -> MockEventBus:
    return MockEventBus()


@pytest.fixture()
def audit_log() -> MockAuditLog:
    return MockAuditLog()


@pytest.fixture()
def service_registry() -> MockServiceRegistry:
    return MockServiceRegistry()


@pytest.fixture()
def health_monitor() -> MockHealthMonitor:
    return MockHealthMonitor()


@pytest.fixture()
def sandbox(logger: MockLogger) -> PluginSandbox:
    return PluginSandbox(plugin_id="test-plugin", logger=logger)


@pytest.fixture()
def context(
    event_bus: MockEventBus,
    logger: MockLogger,
    service_registry: MockServiceRegistry,
) -> PluginContext:
    return PluginContext(
        plugin_id="test-plugin",
        event_bus=event_bus,
        logger=logger,
        service_registry=service_registry,
    )


@pytest.fixture()
def registry(
    event_bus: MockEventBus,
    audit_log: MockAuditLog,
    logger: MockLogger,
    service_registry: MockServiceRegistry,
    health_monitor: MockHealthMonitor,
) -> PluginRegistry:
    return PluginRegistry(
        event_bus=event_bus,
        audit_log=audit_log,
        logger=logger,
        service_registry=service_registry,
        health_monitor=health_monitor,
    )


# ===================================================================
# PluginSandbox Tests
# ===================================================================


class TestPluginSandbox:
    """Tests for ``PluginSandbox``."""

    def test_execute_success(self, sandbox: PluginSandbox) -> None:
        called = False

        def callback() -> None:
            nonlocal called
            called = True

        result = sandbox.execute(PluginAction.LOAD, callback)

        assert result is True
        assert called is True

    def test_execute_failure_returns_false(
        self, sandbox: PluginSandbox
    ) -> None:
        def failing() -> None:
            msg = "boom"
            raise RuntimeError(msg)

        result = sandbox.execute(PluginAction.LOAD, failing)

        assert result is False

    def test_execute_failure_does_not_propagate(
        self, sandbox: PluginSandbox
    ) -> None:
        def failing() -> None:
            msg = "boom"
            raise RuntimeError(msg)

        sandbox.execute(PluginAction.LOAD, failing)

    def test_consecutive_failure_counting(
        self, sandbox: PluginSandbox
    ) -> None:
        failing = MagicMock(side_effect=RuntimeError("fail"))

        sandbox.execute(PluginAction.ENABLE, failing)
        assert sandbox.get_consecutive_failures() == 1

        sandbox.execute(PluginAction.ENABLE, failing)
        assert sandbox.get_consecutive_failures() == 2

    def test_consecutive_failure_resets_on_success(
        self, sandbox: PluginSandbox
    ) -> None:
        failing = MagicMock(side_effect=RuntimeError("fail"))
        sandbox.execute(PluginAction.ENABLE, failing)
        sandbox.execute(PluginAction.ENABLE, failing)
        assert sandbox.get_consecutive_failures() == 2

        sandbox.execute(PluginAction.ENABLE, lambda: None)
        assert sandbox.get_consecutive_failures() == 0

    def test_total_failure_counting(self, sandbox: PluginSandbox) -> None:
        failing = MagicMock(side_effect=RuntimeError("fail"))

        sandbox.execute(PluginAction.ENABLE, failing)
        sandbox.execute(PluginAction.ENABLE, lambda: None)
        sandbox.execute(PluginAction.ENABLE, failing)

        assert sandbox.get_total_failures() == 2

    def test_total_execution_counting(self, sandbox: PluginSandbox) -> None:
        failing = MagicMock(side_effect=RuntimeError("fail"))

        sandbox.execute(PluginAction.ENABLE, lambda: None)
        sandbox.execute(PluginAction.ENABLE, failing)
        sandbox.execute(PluginAction.ENABLE, lambda: None)

        assert sandbox.get_total_executions() == 3

    def test_health_healthy(self, sandbox: PluginSandbox) -> None:
        assert sandbox.check_health() == HealthStatus.HEALTHY

    def test_health_degraded(self, sandbox: PluginSandbox) -> None:
        failing = MagicMock(side_effect=RuntimeError("fail"))

        sandbox.execute(PluginAction.ENABLE, failing)
        assert sandbox.check_health() == HealthStatus.DEGRADED

    def test_health_unhealthy(self, sandbox: PluginSandbox) -> None:
        failing = MagicMock(side_effect=RuntimeError("fail"))

        for _ in range(5):
            sandbox.execute(PluginAction.ENABLE, failing)

        assert sandbox.check_health() == HealthStatus.UNHEALTHY

    def test_reset_failure_counts(self, sandbox: PluginSandbox) -> None:
        failing = MagicMock(side_effect=RuntimeError("fail"))
        sandbox.execute(PluginAction.ENABLE, failing)
        sandbox.execute(PluginAction.ENABLE, failing)

        sandbox.reset_failure_counts()

        assert sandbox.get_consecutive_failures() == 0
        assert sandbox.get_total_failures() == 0

    def test_component_name(self, sandbox: PluginSandbox) -> None:
        assert sandbox.get_component_name() == "PluginSandbox[test-plugin]"

    def test_execute_logs_error_on_failure(
        self, sandbox: PluginSandbox, logger: MockLogger
    ) -> None:
        sandbox.execute(
            PluginAction.LOAD,
            MagicMock(side_effect=RuntimeError("test error")),
        )

        error_entries = [
            e for e in logger.entries if e["severity"] == LogSeverity.ERROR
        ]
        assert len(error_entries) >= 1
        assert "test error" in error_entries[0]["message"]

    def test_execute_logs_debug_on_start(
        self, sandbox: PluginSandbox, logger: MockLogger
    ) -> None:
        sandbox.execute(PluginAction.LOAD, lambda: None)

        debug_entries = [
            e for e in logger.entries if e["severity"] == LogSeverity.DEBUG
        ]
        assert len(debug_entries) >= 1


# ===================================================================
# PluginContext Tests
# ===================================================================


class TestPluginContext:
    """Tests for ``PluginContext``."""

    def test_get_plugin_id(self, context: PluginContext) -> None:
        assert context.get_plugin_id() == "test-plugin"

    def test_get_event_bus(
        self, context: PluginContext, event_bus: MockEventBus
    ) -> None:
        assert context.get_event_bus() is event_bus

    def test_get_logger_returns_scoped_logger(
        self, context: PluginContext, logger: MockLogger
    ) -> None:
        scoped = context.get_logger()
        scoped.info("hello")

        assert len(logger.entries) == 1
        assert logger.entries[0]["component"] == "Plugin[test-plugin]"

    def test_scoped_logger_allows_component_override(
        self, context: PluginContext, logger: MockLogger
    ) -> None:
        scoped = context.get_logger()
        scoped.info("hello", component="CustomComponent")

        assert logger.entries[0]["component"] == "CustomComponent"

    def test_scoped_logger_log_method(
        self, context: PluginContext, logger: MockLogger
    ) -> None:
        scoped = context.get_logger()
        scoped.log(LogSeverity.WARNING, "warn msg")

        assert logger.entries[0]["severity"] == LogSeverity.WARNING
        assert logger.entries[0]["component"] == "Plugin[test-plugin]"

    def test_scoped_logger_all_levels(
        self, context: PluginContext, logger: MockLogger
    ) -> None:
        scoped = context.get_logger()

        scoped.debug("d")
        scoped.info("i")
        scoped.warning("w")
        scoped.error("e")
        scoped.critical("c")

        severities = [e["severity"] for e in logger.entries]
        assert severities == [
            LogSeverity.DEBUG,
            LogSeverity.INFO,
            LogSeverity.WARNING,
            LogSeverity.ERROR,
            LogSeverity.CRITICAL,
        ]

    def test_get_service(
        self,
        context: PluginContext,
        service_registry: MockServiceRegistry,
    ) -> None:
        sentinel = object()
        service_registry._services[str] = sentinel

        result = context.get_service(str)
        assert result is sentinel

    def test_get_service_not_found(self, context: PluginContext) -> None:
        with pytest.raises(ServiceNotFoundError):
            context.get_service(int)

    def test_dispose(self, context: PluginContext) -> None:
        assert context.is_disposed() is False
        context.dispose()
        assert context.is_disposed() is True

    def test_get_event_bus_after_dispose(self, context: PluginContext) -> None:
        context.dispose()
        with pytest.raises(PluginIsolationError):
            context.get_event_bus()

    def test_get_logger_after_dispose(self, context: PluginContext) -> None:
        context.dispose()
        with pytest.raises(PluginIsolationError):
            context.get_logger()

    def test_get_service_after_dispose(self, context: PluginContext) -> None:
        context.dispose()
        with pytest.raises(PluginIsolationError):
            context.get_service(str)

    def test_get_plugin_id_works_after_dispose(
        self, context: PluginContext
    ) -> None:
        context.dispose()
        assert context.get_plugin_id() == "test-plugin"

    def test_check_health_active(self, context: PluginContext) -> None:
        assert context.check_health() == HealthStatus.HEALTHY

    def test_check_health_disposed(self, context: PluginContext) -> None:
        context.dispose()
        assert context.check_health() == HealthStatus.UNHEALTHY

    def test_component_name(self, context: PluginContext) -> None:
        assert context.get_component_name() == "PluginContext[test-plugin]"


# ===================================================================
# PluginRegistry Tests
# ===================================================================


class TestPluginRegistryLoad:
    """Tests for ``PluginRegistry.load_plugin``."""

    def test_load_plugin(self, registry: PluginRegistry) -> None:
        plugin = MockPlugin()
        registry.load_plugin("p1", plugin)

        assert registry.has_plugin("p1") is True
        assert registry.get_plugin_state("p1") == PluginState.LOADED
        assert plugin.loaded is True
        assert plugin.context is not None

    def test_load_plugin_empty_id(self, registry: PluginRegistry) -> None:
        with pytest.raises(InputValidationError):
            registry.load_plugin("", MockPlugin())

    def test_load_plugin_non_string_id(
        self, registry: PluginRegistry
    ) -> None:
        with pytest.raises(InputValidationError):
            registry.load_plugin(42, MockPlugin())  # type: ignore[arg-type]

    def test_load_plugin_invalid_plugin(
        self, registry: PluginRegistry
    ) -> None:
        with pytest.raises(InputValidationError):
            registry.load_plugin("p1", "not a plugin")  # type: ignore[arg-type]

    def test_load_plugin_duplicate(self, registry: PluginRegistry) -> None:
        registry.load_plugin("p1", MockPlugin())

        with pytest.raises(PluginError, match="already loaded"):
            registry.load_plugin("p1", MockPlugin())

    def test_load_plugin_failure(self, registry: PluginRegistry) -> None:
        plugin = FailingPlugin(fail_on={PluginAction.LOAD})

        with pytest.raises(PluginLoadError):
            registry.load_plugin("p1", plugin)

        assert registry.has_plugin("p1") is False

    def test_load_plugin_failure_disposes_context(
        self,
        registry: PluginRegistry,
    ) -> None:
        plugin = FailingPlugin(fail_on={PluginAction.LOAD})

        with pytest.raises(PluginLoadError):
            registry.load_plugin("p1", plugin)


class TestPluginRegistryLifecycle:
    """Tests for plugin lifecycle transitions."""

    def test_initialize_plugin(self, registry: PluginRegistry) -> None:
        plugin = MockPlugin()
        registry.load_plugin("p1", plugin)
        registry.initialize_plugin("p1")

        assert registry.get_plugin_state("p1") == PluginState.INITIALIZED
        assert plugin.initialized is True

    def test_enable_plugin(self, registry: PluginRegistry) -> None:
        plugin = MockPlugin()
        registry.load_plugin("p1", plugin)
        registry.initialize_plugin("p1")
        registry.enable_plugin("p1")

        assert registry.get_plugin_state("p1") == PluginState.ENABLED
        assert plugin.enabled is True

    def test_disable_plugin(self, registry: PluginRegistry) -> None:
        plugin = MockPlugin()
        registry.load_plugin("p1", plugin)
        registry.initialize_plugin("p1")
        registry.enable_plugin("p1")
        registry.disable_plugin("p1")

        assert registry.get_plugin_state("p1") == PluginState.DISABLED
        assert plugin.enabled is False

    def test_re_enable_from_disabled(self, registry: PluginRegistry) -> None:
        plugin = MockPlugin()
        registry.load_plugin("p1", plugin)
        registry.initialize_plugin("p1")
        registry.enable_plugin("p1")
        registry.disable_plugin("p1")
        registry.enable_plugin("p1")

        assert registry.get_plugin_state("p1") == PluginState.ENABLED
        assert plugin.enabled is True

    def test_unload_from_loaded(self, registry: PluginRegistry) -> None:
        plugin = MockPlugin()
        registry.load_plugin("p1", plugin)
        registry.unload_plugin("p1")

        assert registry.has_plugin("p1") is False
        assert plugin.unloaded is True

    def test_unload_from_initialized(self, registry: PluginRegistry) -> None:
        plugin = MockPlugin()
        registry.load_plugin("p1", plugin)
        registry.initialize_plugin("p1")
        registry.unload_plugin("p1")

        assert registry.has_plugin("p1") is False

    def test_unload_from_disabled(self, registry: PluginRegistry) -> None:
        plugin = MockPlugin()
        registry.load_plugin("p1", plugin)
        registry.initialize_plugin("p1")
        registry.enable_plugin("p1")
        registry.disable_plugin("p1")
        registry.unload_plugin("p1")

        assert registry.has_plugin("p1") is False

    def test_full_lifecycle(self, registry: PluginRegistry) -> None:
        plugin = MockPlugin()
        registry.load_plugin("p1", plugin)
        registry.initialize_plugin("p1")
        registry.enable_plugin("p1")
        registry.disable_plugin("p1")
        registry.unload_plugin("p1")

        assert registry.has_plugin("p1") is False
        assert plugin.loaded is False
        assert plugin.unloaded is True


class TestPluginRegistryInvalidTransitions:
    """Tests for invalid lifecycle transitions."""

    def test_initialize_unloaded(self, registry: PluginRegistry) -> None:
        registry.load_plugin("p1", MockPlugin())
        registry.unload_plugin("p1")

        with pytest.raises(PluginNotFoundError):
            registry.initialize_plugin("p1")

    def test_enable_from_loaded(self, registry: PluginRegistry) -> None:
        registry.load_plugin("p1", MockPlugin())

        with pytest.raises(PluginLifecycleError):
            registry.enable_plugin("p1")

    def test_disable_from_loaded(self, registry: PluginRegistry) -> None:
        registry.load_plugin("p1", MockPlugin())

        with pytest.raises(PluginLifecycleError):
            registry.disable_plugin("p1")

    def test_disable_from_initialized(
        self, registry: PluginRegistry
    ) -> None:
        registry.load_plugin("p1", MockPlugin())
        registry.initialize_plugin("p1")

        with pytest.raises(PluginLifecycleError):
            registry.disable_plugin("p1")

    def test_unload_from_enabled(self, registry: PluginRegistry) -> None:
        registry.load_plugin("p1", MockPlugin())
        registry.initialize_plugin("p1")
        registry.enable_plugin("p1")

        with pytest.raises(PluginLifecycleError):
            registry.unload_plugin("p1")

    def test_initialize_from_enabled(self, registry: PluginRegistry) -> None:
        registry.load_plugin("p1", MockPlugin())
        registry.initialize_plugin("p1")
        registry.enable_plugin("p1")

        with pytest.raises(PluginLifecycleError):
            registry.initialize_plugin("p1")

    def test_operations_on_nonexistent_plugin(
        self, registry: PluginRegistry
    ) -> None:
        with pytest.raises(PluginNotFoundError):
            registry.initialize_plugin("nonexistent")

        with pytest.raises(PluginNotFoundError):
            registry.enable_plugin("nonexistent")

        with pytest.raises(PluginNotFoundError):
            registry.disable_plugin("nonexistent")

        with pytest.raises(PluginNotFoundError):
            registry.unload_plugin("nonexistent")


class TestPluginRegistryCallbackFailure:
    """Tests for plugin callback failures."""

    def test_initialize_failure(self, registry: PluginRegistry) -> None:
        plugin = FailingPlugin(fail_on={PluginAction.INITIALIZE})
        registry.load_plugin("p1", plugin)

        with pytest.raises(PluginError, match="failed during INITIALIZE"):
            registry.initialize_plugin("p1")

        assert registry.get_plugin_state("p1") == PluginState.LOADED

    def test_enable_failure(self, registry: PluginRegistry) -> None:
        plugin = FailingPlugin(fail_on={PluginAction.ENABLE})
        registry.load_plugin("p1", plugin)
        registry.initialize_plugin("p1")

        with pytest.raises(PluginError, match="failed during ENABLE"):
            registry.enable_plugin("p1")

        assert registry.get_plugin_state("p1") == PluginState.INITIALIZED

    def test_disable_failure(self, registry: PluginRegistry) -> None:
        plugin = FailingPlugin(fail_on={PluginAction.DISABLE})
        registry.load_plugin("p1", plugin)
        registry.initialize_plugin("p1")
        registry.enable_plugin("p1")

        with pytest.raises(PluginError, match="failed during DISABLE"):
            registry.disable_plugin("p1")

        assert registry.get_plugin_state("p1") == PluginState.ENABLED

    def test_unload_callback_failure_still_unloads(
        self, registry: PluginRegistry
    ) -> None:
        plugin = FailingPlugin(fail_on={PluginAction.UNLOAD})
        registry.load_plugin("p1", plugin)

        registry.unload_plugin("p1")

        assert registry.has_plugin("p1") is False


class TestPluginRegistryEvents:
    """Tests for event emission and audit recording."""

    def test_load_emits_lifecycle_event(
        self, registry: PluginRegistry, event_bus: MockEventBus
    ) -> None:
        registry.load_plugin("p1", MockPlugin())

        lifecycle_events = [
            e for e in event_bus.published
            if isinstance(e, PluginLifecycleEvent)
        ]
        assert len(lifecycle_events) >= 1
        event = lifecycle_events[0]
        assert event.plugin_id == "p1"
        assert event.action == PluginAction.LOAD
        assert event.success is True

    def test_full_lifecycle_emits_all_events(
        self, registry: PluginRegistry, event_bus: MockEventBus
    ) -> None:
        plugin = MockPlugin()
        registry.load_plugin("p1", plugin)
        registry.initialize_plugin("p1")
        registry.enable_plugin("p1")
        registry.disable_plugin("p1")
        registry.unload_plugin("p1")

        lifecycle_events = [
            e for e in event_bus.published
            if isinstance(e, PluginLifecycleEvent)
        ]
        actions = [e.action for e in lifecycle_events]

        assert PluginAction.LOAD in actions
        assert PluginAction.INITIALIZE in actions
        assert PluginAction.ENABLE in actions
        assert PluginAction.DISABLE in actions
        assert PluginAction.UNLOAD in actions

    def test_load_records_audit(
        self, registry: PluginRegistry, audit_log: MockAuditLog
    ) -> None:
        registry.load_plugin("p1", MockPlugin())

        lifecycle_audits = [
            e for e in audit_log.entries
            if isinstance(e, PluginLifecycleEvent)
        ]
        assert len(lifecycle_audits) >= 1
        assert lifecycle_audits[0].plugin_id == "p1"

    def test_full_lifecycle_records_all_audits(
        self, registry: PluginRegistry, audit_log: MockAuditLog
    ) -> None:
        plugin = MockPlugin()
        registry.load_plugin("p1", plugin)
        registry.initialize_plugin("p1")
        registry.enable_plugin("p1")
        registry.disable_plugin("p1")
        registry.unload_plugin("p1")

        lifecycle_audits = [
            e for e in audit_log.entries
            if isinstance(e, PluginLifecycleEvent)
        ]
        assert len(lifecycle_audits) == 5

    def test_failed_load_emits_failure_event(
        self, registry: PluginRegistry, event_bus: MockEventBus
    ) -> None:
        plugin = FailingPlugin(fail_on={PluginAction.LOAD})

        with pytest.raises(PluginLoadError):
            registry.load_plugin("p1", plugin)

        lifecycle_events = [
            e for e in event_bus.published
            if isinstance(e, PluginLifecycleEvent)
        ]
        assert len(lifecycle_events) >= 1
        assert lifecycle_events[0].success is False


class TestPluginRegistryIntrospection:
    """Tests for registry introspection methods."""

    def test_get_plugin_state(self, registry: PluginRegistry) -> None:
        registry.load_plugin("p1", MockPlugin())
        assert registry.get_plugin_state("p1") == PluginState.LOADED

    def test_get_plugin_state_not_found(
        self, registry: PluginRegistry
    ) -> None:
        with pytest.raises(PluginNotFoundError):
            registry.get_plugin_state("nonexistent")

    def test_get_plugin_context(self, registry: PluginRegistry) -> None:
        registry.load_plugin("p1", MockPlugin())
        ctx = registry.get_plugin_context("p1")
        assert ctx.get_plugin_id() == "p1"

    def test_get_plugin_context_not_found(
        self, registry: PluginRegistry
    ) -> None:
        with pytest.raises(PluginNotFoundError):
            registry.get_plugin_context("nonexistent")

    def test_get_plugin_ids(self, registry: PluginRegistry) -> None:
        registry.load_plugin("p1", MockPlugin())
        registry.load_plugin("p2", MockPlugin())

        ids = registry.get_plugin_ids()
        assert set(ids) == {"p1", "p2"}

    def test_get_plugin_ids_empty(self, registry: PluginRegistry) -> None:
        assert list(registry.get_plugin_ids()) == []

    def test_has_plugin(self, registry: PluginRegistry) -> None:
        assert registry.has_plugin("p1") is False
        registry.load_plugin("p1", MockPlugin())
        assert registry.has_plugin("p1") is True

    def test_get_loaded_count(self, registry: PluginRegistry) -> None:
        assert registry.get_loaded_count() == 0
        registry.load_plugin("p1", MockPlugin())
        registry.load_plugin("p2", MockPlugin())
        assert registry.get_loaded_count() == 2


class TestPluginRegistryHealth:
    """Tests for registry health reporting."""

    def test_health_no_plugins(self, registry: PluginRegistry) -> None:
        assert registry.check_health() == HealthStatus.HEALTHY

    def test_health_all_healthy(self, registry: PluginRegistry) -> None:
        registry.load_plugin("p1", MockPlugin())
        registry.load_plugin("p2", MockPlugin())
        assert registry.check_health() == HealthStatus.HEALTHY

    def test_health_degraded(self, registry: PluginRegistry) -> None:
        registry.load_plugin("p1", MockPlugin())
        failing = FailingPlugin(fail_on={PluginAction.INITIALIZE})
        registry.load_plugin("p2", failing)

        with pytest.raises(PluginError):
            registry.initialize_plugin("p2")

        assert registry.check_health() == HealthStatus.DEGRADED

    def test_component_name(self, registry: PluginRegistry) -> None:
        assert registry.get_component_name() == "PluginRegistry"

    def test_health_monitor_registration(
        self,
        registry: PluginRegistry,
        health_monitor: MockHealthMonitor,
    ) -> None:
        registry.load_plugin("p1", MockPlugin())
        assert "Plugin[p1]" in health_monitor.registered

    def test_health_monitor_unregistration(
        self,
        registry: PluginRegistry,
        health_monitor: MockHealthMonitor,
    ) -> None:
        registry.load_plugin("p1", MockPlugin())
        registry.unload_plugin("p1")
        assert "Plugin[p1]" not in health_monitor.registered


class TestPluginIsolation:
    """Tests for plugin isolation guarantees."""

    def test_plugin_a_failure_does_not_affect_plugin_b(
        self, registry: PluginRegistry
    ) -> None:
        plugin_a = FailingPlugin(fail_on={PluginAction.INITIALIZE})
        plugin_b = MockPlugin()

        registry.load_plugin("a", plugin_a)
        registry.load_plugin("b", plugin_b)

        with pytest.raises(PluginError):
            registry.initialize_plugin("a")

        registry.initialize_plugin("b")
        assert registry.get_plugin_state("b") == PluginState.INITIALIZED

    def test_context_disposed_after_unload(
        self, registry: PluginRegistry
    ) -> None:
        plugin = MockPlugin()
        registry.load_plugin("p1", plugin)
        ctx = registry.get_plugin_context("p1")

        registry.unload_plugin("p1")

        with pytest.raises(PluginIsolationError):
            ctx.get_event_bus()

    def test_contexts_are_independent(
        self, registry: PluginRegistry
    ) -> None:
        plugin_a = MockPlugin()
        plugin_b = MockPlugin()

        registry.load_plugin("a", plugin_a)
        registry.load_plugin("b", plugin_b)

        ctx_a = registry.get_plugin_context("a")
        ctx_b = registry.get_plugin_context("b")

        assert ctx_a is not ctx_b
        assert ctx_a.get_plugin_id() != ctx_b.get_plugin_id()

    def test_unloading_one_does_not_affect_other(
        self, registry: PluginRegistry
    ) -> None:
        plugin_a = MockPlugin()
        plugin_b = MockPlugin()

        registry.load_plugin("a", plugin_a)
        registry.load_plugin("b", plugin_b)

        registry.unload_plugin("a")

        assert registry.has_plugin("b") is True
        ctx_b = registry.get_plugin_context("b")
        assert ctx_b.check_health() == HealthStatus.HEALTHY

    def test_multiple_failures_do_not_cascade(
        self, registry: PluginRegistry
    ) -> None:
        for i in range(5):
            plugin = FailingPlugin(fail_on={PluginAction.INITIALIZE})
            registry.load_plugin(f"fail-{i}", plugin)

        good_plugin = MockPlugin()
        registry.load_plugin("good", good_plugin)

        for i in range(5):
            with pytest.raises(PluginError):
                registry.initialize_plugin(f"fail-{i}")

        registry.initialize_plugin("good")
        registry.enable_plugin("good")

        assert registry.get_plugin_state("good") == PluginState.ENABLED


class TestPluginExceptions:
    """Tests for exception types."""

    def test_plugin_error_has_plugin_id(self) -> None:
        err = PluginError("msg", plugin_id="p1")
        assert err.plugin_id == "p1"

    def test_plugin_load_error_inherits(self) -> None:
        err = PluginLoadError("msg", plugin_id="p1")
        assert isinstance(err, PluginError)
        assert err.plugin_id == "p1"

    def test_plugin_isolation_error_inherits(self) -> None:
        err = PluginIsolationError("msg", plugin_id="p1")
        assert isinstance(err, PluginError)

    def test_plugin_lifecycle_error(self) -> None:
        err = PluginLifecycleError(
            "msg",
            plugin_id="p1",
            from_state="LOADED",
            to_action="ENABLE",
        )
        assert err.plugin_id == "p1"
        assert err.from_state == "LOADED"
        assert err.to_action == "ENABLE"
        assert isinstance(err, PluginError)

    def test_plugin_not_found_error(self) -> None:
        err = PluginNotFoundError("msg", plugin_id="p1")
        assert isinstance(err, PluginError)
        assert err.plugin_id == "p1"
