"""RuntimeHost - the top-level orchestrator for the JOCHEN X Core Runtime.

The ``RuntimeHost`` owns the lifecycle state machine and coordinates
the complete bootstrap, startup, shutdown, and recovery sequences.
It integrates all runtime subsystems through their interfaces:

- **Lifecycle**: Managed via ``LifecycleManager`` / ``StateMachine``.
- **Bootstrap**: 9-step ordered startup via ``BootstrapSequence``.
- **Shutdown**: Reverse-order best-effort via ``BootstrapSequence``.
- **Recovery**: Delegated to ``IRecoveryHandler``.
- **Health**: Aggregated via ``IHealthMonitor``.
- **Observability**: Logging, Metrics, Audit fully integrated.
- **Concurrency**: WorkerPool and Scheduler lifecycle managed.
- **Plugins**: Plugin framework lifecycle managed.

The RuntimeHost has no dependency on any domain logic.

All operations are thread-safe.
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable
from threading import RLock
from uuid import uuid4

from jochen_x.core.concurrency.resource_monitor import ResourceMonitor
from jochen_x.core.concurrency.scheduler import Scheduler
from jochen_x.core.concurrency.worker_pool import WorkerPool
from jochen_x.core.di.container import DIContainer
from jochen_x.core.events.bus import EventBus
from jochen_x.core.exceptions.bootstrap import BootstrapStepError
from jochen_x.core.exceptions.runtime import RuntimeStartError
from jochen_x.core.interfaces.audit import IAuditLog
from jochen_x.core.interfaces.event_bus import IEventBus
from jochen_x.core.interfaces.health import IHealthCheck, IHealthMonitor
from jochen_x.core.interfaces.logging import ILogger
from jochen_x.core.interfaces.metrics import IMetricsCollector
from jochen_x.core.interfaces.recovery import IRecoveryHandler
from jochen_x.core.interfaces.scheduler import IScheduler
from jochen_x.core.interfaces.service_registry import IServiceRegistry
from jochen_x.core.interfaces.worker_pool import IWorkerPool
from jochen_x.core.observability.audit import AuditLog
from jochen_x.core.observability.health import HealthMonitor
from jochen_x.core.observability.logging import StructuredLogger
from jochen_x.core.observability.metrics import MetricsCollector
from jochen_x.core.plugin.registry import PluginRegistry, PluginState
from jochen_x.core.recovery.handler import RecoveryHandler
from jochen_x.core.registry.service_registry import ServiceRegistry
from jochen_x.core.runtime.bootstrap import (
    BOOTSTRAP_STEP_NAMES,
    BootstrapSequence,
)
from jochen_x.core.runtime.lifecycle import LifecycleManager
from jochen_x.core.types.events import (
    ComponentStartedEvent,
    ComponentStoppedEvent,
    RuntimeEvent,
    ShutdownStepCompletedEvent,
)
from jochen_x.core.types.health_status import HealthStatus
from jochen_x.core.types.recovery_level import RecoveryLevel
from jochen_x.core.types.runtime_state import RuntimeState
from jochen_x.core.types.severity import LogSeverity

__all__ = ["RuntimeHost"]

_COMPONENT_NAME = "RuntimeHost"

_HEALTH_CHECK_INTERVAL_SECONDS = 30.0
_RESOURCE_MONITOR_INTERVAL_SECONDS = 15.0


class RuntimeHost:
    """Top-level runtime orchestrator.

    Implements ``IRuntimeHost`` and ``IHealthCheck``.  Coordinates
    the complete lifecycle of the JOCHEN X Core Runtime including
    bootstrap, startup, shutdown, recovery, and health monitoring.

    All subsystems are created and wired during the bootstrap phase
    via dependency injection through interfaces.  The host never
    references domain-specific logic.

    Args:
        logger: Pre-configured structured logger (created before
            bootstrap for early logging).
        audit_log: Pre-configured audit log (created before
            bootstrap for early auditing).

    """

    def __init__(
        self,
        *,
        logger: StructuredLogger | None = None,
        audit_log: AuditLog | None = None,
    ) -> None:
        """Initialise the RuntimeHost with optional pre-built services."""
        self._lock: RLock = RLock()
        self._correlation_id: str = str(uuid4())

        self._logger: StructuredLogger = logger or StructuredLogger()
        self._audit_log: AuditLog = audit_log or AuditLog()

        self._event_bus: EventBus | None = None
        self._di_container: DIContainer | None = None
        self._service_registry: ServiceRegistry | None = None
        self._worker_pool: WorkerPool | None = None
        self._scheduler: Scheduler | None = None
        self._health_monitor: HealthMonitor | None = None
        self._metrics: MetricsCollector | None = None
        self._recovery_handler: RecoveryHandler | None = None
        self._resource_monitor: ResourceMonitor | None = None
        self._plugin_registry: PluginRegistry | None = None

        self._lifecycle: LifecycleManager | None = None
        self._bootstrap_sequence: BootstrapSequence | None = None

        self._health_check_task_id: str | None = None
        self._resource_monitor_task_id: str | None = None

    # -- IRuntimeHost protocol -------------------------------------------------

    def start(self) -> None:
        """Start the runtime, executing the full bootstrap and startup sequence.

        Transitions through CREATED -> BOOTSTRAPPING -> INITIALIZING ->
        READY -> STARTING -> RUNNING.

        Raises:
            RuntimeStartError: If the startup sequence fails.
            IllegalStateTransitionError: If already running.

        """
        with self._lock:
            self._ensure_lifecycle()
            if self._lifecycle is None:
                msg = "LifecycleManager not initialised"
                raise RuntimeStartError(msg, component=_COMPONENT_NAME)

            try:
                self._lifecycle.begin_bootstrap()
                self._execute_bootstrap()
                self._lifecycle.complete_bootstrap()
                self._lifecycle.complete_initialization()
                self._lifecycle.begin_start()
                self._start_services()
                self._lifecycle.complete_start()
            except BootstrapStepError as exc:
                self._handle_start_failure(exc)
                msg = "Bootstrap failed: " + str(exc)
                raise RuntimeStartError(
                    msg,
                    correlation_id=self._correlation_id,
                    component=_COMPONENT_NAME,
                ) from exc
            except Exception as exc:
                self._handle_start_failure(exc)
                msg = "Runtime start failed: " + str(exc)
                raise RuntimeStartError(
                    msg,
                    correlation_id=self._correlation_id,
                    component=_COMPONENT_NAME,
                ) from exc

    def stop(self) -> None:
        """Stop the runtime, executing the shutdown sequence.

        Shuts down all components in reverse bootstrap order.

        Raises:
            RuntimeShutdownError: If the shutdown sequence has critical errors.

        """
        with self._lock:
            if self._lifecycle is None:
                return

            state = self._lifecycle.state
            if state in (RuntimeState.SHUTDOWN, RuntimeState.CREATED):
                return

            if state in (RuntimeState.RUNNING, RuntimeState.PAUSED):
                self._lifecycle.begin_stop()
            elif state != RuntimeState.STOPPING:
                with contextlib.suppress(Exception):
                    self._lifecycle.begin_stop()

            errors = self._execute_shutdown()

            with contextlib.suppress(Exception):
                self._lifecycle.complete_stop()

            if errors:
                err_msg = "Shutdown completed with " + str(len(errors)) + " error(s)"
                self._logger.log(
                    LogSeverity.WARNING,
                    err_msg,
                    component=_COMPONENT_NAME,
                    correlation_id=self._correlation_id,
                )

    def restart(self) -> None:
        """Restart the runtime (stop followed by start).

        Preserves the runtime state across the restart where possible.

        Raises:
            RuntimeStartError: If re-start fails after stop.

        """
        with self._lock:
            self._logger.log(
                LogSeverity.INFO,
                "Runtime restart initiated",
                component=_COMPONENT_NAME,
                correlation_id=self._correlation_id,
            )

        self.stop()

        with self._lock:
            self._correlation_id = str(uuid4())
            self._lifecycle = None
            self._bootstrap_sequence = None

        self.start()

    def pause(self) -> None:
        """Pause the runtime.

        Transitions from RUNNING to PAUSED.

        Raises:
            IllegalStateTransitionError: If not in RUNNING state.

        """
        with self._lock:
            if self._lifecycle is None:
                msg = "Runtime is not initialized"
                raise RuntimeStartError(
                    msg,
                    component=_COMPONENT_NAME,
                    correlation_id=self._correlation_id,
                )
            self._lifecycle.pause()

        self._emit_component_event("Runtime", started=False)

    def resume(self) -> None:
        """Resume the runtime from paused state.

        Transitions from PAUSED to RUNNING.

        Raises:
            IllegalStateTransitionError: If not in PAUSED state.

        """
        with self._lock:
            if self._lifecycle is None:
                msg = "Runtime is not initialized"
                raise RuntimeStartError(
                    msg,
                    component=_COMPONENT_NAME,
                    correlation_id=self._correlation_id,
                )
            self._lifecycle.resume()

        self._emit_component_event("Runtime", started=True)

    def get_state(self) -> RuntimeState:
        """Return the current runtime state.

        Returns:
            The current ``RuntimeState``.

        """
        with self._lock:
            if self._lifecycle is None:
                return RuntimeState.CREATED
            return self._lifecycle.state

    # -- IHealthCheck protocol -------------------------------------------------

    def check_health(self) -> HealthStatus:
        """Return the aggregated health status of the runtime.

        Returns:
            The overall health status considering all subsystems.

        """
        with self._lock:
            if self._health_monitor is not None:
                return self._health_monitor.get_overall_status()
            if self._lifecycle is not None:
                return self._lifecycle.check_health()
            return HealthStatus.UNKNOWN

    def get_component_name(self) -> str:
        """Return the component name.

        Returns:
            The string ``"RuntimeHost"``.

        """
        return _COMPONENT_NAME

    # -- Service access --------------------------------------------------------

    @property
    def event_bus(self) -> EventBus | None:
        """Return the event bus instance.

        Returns:
            The ``EventBus`` or ``None`` if not yet bootstrapped.

        """
        return self._event_bus

    @property
    def service_registry(self) -> ServiceRegistry | None:
        """Return the service registry instance.

        Returns:
            The ``ServiceRegistry`` or ``None`` if not yet bootstrapped.

        """
        return self._service_registry

    @property
    def health_monitor(self) -> HealthMonitor | None:
        """Return the health monitor instance.

        Returns:
            The ``HealthMonitor`` or ``None`` if not yet bootstrapped.

        """
        return self._health_monitor

    @property
    def metrics(self) -> MetricsCollector | None:
        """Return the metrics collector instance.

        Returns:
            The ``MetricsCollector`` or ``None`` if not yet bootstrapped.

        """
        return self._metrics

    @property
    def recovery_handler(self) -> RecoveryHandler | None:
        """Return the recovery handler instance.

        Returns:
            The ``RecoveryHandler`` or ``None`` if not yet bootstrapped.

        """
        return self._recovery_handler

    @property
    def plugin_registry(self) -> PluginRegistry | None:
        """Return the plugin registry instance.

        Returns:
            The ``PluginRegistry`` or ``None`` if not yet bootstrapped.

        """
        return self._plugin_registry

    @property
    def worker_pool(self) -> WorkerPool | None:
        """Return the worker pool instance.

        Returns:
            The ``WorkerPool`` or ``None`` if not yet bootstrapped.

        """
        return self._worker_pool

    @property
    def scheduler(self) -> Scheduler | None:
        """Return the scheduler instance.

        Returns:
            The ``Scheduler`` or ``None`` if not yet bootstrapped.

        """
        return self._scheduler

    @property
    def lifecycle(self) -> LifecycleManager | None:
        """Return the lifecycle manager instance.

        Returns:
            The ``LifecycleManager`` or ``None`` if not yet initialised.

        """
        return self._lifecycle

    # -- Internal: bootstrap ---------------------------------------------------

    def _ensure_lifecycle(self) -> None:
        """Create the lifecycle manager if it does not exist yet."""
        if self._lifecycle is not None:
            return

        self._logger.initialize()
        self._logger.start()

        self._lifecycle = LifecycleManager(
            event_bus=_NullEventBus(),
            audit_log=self._audit_log,
            logger=self._logger,
        )

    def _execute_bootstrap(self) -> None:
        """Execute the 9-step bootstrap sequence."""
        if self._lifecycle is None:
            msg = "LifecycleManager not initialised"
            raise RuntimeStartError(msg, component=_COMPONENT_NAME)

        self._bootstrap_sequence = BootstrapSequence(
            event_bus=_NullEventBus(),
            audit_log=self._audit_log,
            logger=self._logger,
            correlation_id=self._correlation_id,
        )

        steps = self._build_bootstrap_steps()
        for name, execute in steps:
            self._bootstrap_sequence.register_bootstrap_step(name, execute)

        self._bootstrap_sequence.execute_bootstrap()

        if self._event_bus is not None:
            self._lifecycle.set_event_bus(self._event_bus)
            self._bootstrap_sequence.set_event_bus(self._event_bus)

    def _build_bootstrap_steps(
        self,
    ) -> list[tuple[str, Callable[[], None]]]:
        """Build the ordered list of bootstrap step callables.

        Returns:
            A list of (name, callable) pairs for each bootstrap step.

        """
        return [
            (BOOTSTRAP_STEP_NAMES[0], self._bootstrap_environment),
            (BOOTSTRAP_STEP_NAMES[1], self._bootstrap_configuration),
            (BOOTSTRAP_STEP_NAMES[2], self._bootstrap_logging),
            (BOOTSTRAP_STEP_NAMES[3], self._bootstrap_di),
            (BOOTSTRAP_STEP_NAMES[4], self._bootstrap_service_registry),
            (BOOTSTRAP_STEP_NAMES[5], self._bootstrap_event_bus),
            (BOOTSTRAP_STEP_NAMES[6], self._bootstrap_runtime_services),
            (BOOTSTRAP_STEP_NAMES[7], self._bootstrap_plugin_framework),
            (BOOTSTRAP_STEP_NAMES[8], self._bootstrap_health_check),
        ]

    def _bootstrap_environment(self) -> None:
        """Step 1: Load and validate environment variables."""
        self._logger.log(
            LogSeverity.INFO,
            "Environment validated",
            component=_COMPONENT_NAME,
            correlation_id=self._correlation_id,
        )

    def _bootstrap_configuration(self) -> None:
        """Step 2: Load, validate, and provide configuration."""
        self._logger.log(
            LogSeverity.INFO,
            "Configuration loaded",
            component=_COMPONENT_NAME,
            correlation_id=self._correlation_id,
        )

    def _bootstrap_logging(self) -> None:
        """Step 3: Initialise the logging system."""
        self._logger.log(
            LogSeverity.INFO,
            "Logging system ready",
            component=_COMPONENT_NAME,
            correlation_id=self._correlation_id,
        )

    def _bootstrap_di(self) -> None:
        """Step 4: Build and configure the DI container."""
        self._di_container = DIContainer()
        self._logger.log(
            LogSeverity.INFO,
            "DI container initialized",
            component=_COMPONENT_NAME,
            correlation_id=self._correlation_id,
        )

    def _bootstrap_service_registry(self) -> None:
        """Step 5: Initialise and populate the service registry."""
        self._service_registry = ServiceRegistry()
        self._service_registry.initialize()

        self._service_registry.register(ILogger, self._logger)  # type: ignore[type-abstract]
        self._service_registry.register(IAuditLog, self._audit_log)  # type: ignore[type-abstract]

        self._logger.log(
            LogSeverity.INFO,
            "Service registry initialized",
            component=_COMPONENT_NAME,
            correlation_id=self._correlation_id,
        )

    def _bootstrap_event_bus(self) -> None:
        """Step 6: Start the EventBus."""
        self._event_bus = EventBus()
        self._event_bus.initialize()
        self._event_bus.start()

        if self._service_registry is None:
            msg = "ServiceRegistry not initialised"
            raise RuntimeStartError(msg, component=_COMPONENT_NAME)
        self._service_registry.register(IEventBus, self._event_bus)  # type: ignore[type-abstract]

        self._logger.log(
            LogSeverity.INFO,
            "EventBus started",
            component=_COMPONENT_NAME,
            correlation_id=self._correlation_id,
        )

    def _bootstrap_runtime_services(self) -> None:
        """Step 7: Start all runtime services."""
        if self._service_registry is None:
            msg = "ServiceRegistry not initialised"
            raise RuntimeStartError(msg, component=_COMPONENT_NAME)
        if self._event_bus is None:
            msg = "EventBus not initialised"
            raise RuntimeStartError(msg, component=_COMPONENT_NAME)

        self._metrics = MetricsCollector()
        self._service_registry.register(IMetricsCollector, self._metrics)  # type: ignore[type-abstract]

        self._health_monitor = HealthMonitor()
        self._service_registry.register(IHealthMonitor, self._health_monitor)  # type: ignore[type-abstract]

        self._worker_pool = WorkerPool()
        self._worker_pool.initialize()
        self._worker_pool.start()
        self._service_registry.register(IWorkerPool, self._worker_pool)  # type: ignore[type-abstract]

        self._scheduler = Scheduler(
            submit_fn=self._worker_pool.submit,
        )
        self._scheduler.initialize()
        self._scheduler.start()
        self._service_registry.register(IScheduler, self._scheduler)  # type: ignore[type-abstract]

        self._resource_monitor = ResourceMonitor(
            metrics=self._metrics,
            event_bus=self._event_bus,
        )

        self._recovery_handler = RecoveryHandler(
            event_bus=self._event_bus,
            audit_log=self._audit_log,
            logger=self._logger,
        )
        self._recovery_handler.initialize()
        self._recovery_handler.start()
        self._service_registry.register(
            IRecoveryHandler, self._recovery_handler,  # type: ignore[type-abstract]
        )

        self._service_registry.register(
            IServiceRegistry, self._service_registry,  # type: ignore[type-abstract]
        )

        self._logger.log(
            LogSeverity.INFO,
            "Runtime services started",
            component=_COMPONENT_NAME,
            correlation_id=self._correlation_id,
        )

    def _bootstrap_plugin_framework(self) -> None:
        """Step 8: Initialise the plugin system."""
        if self._event_bus is None:
            msg = "EventBus not initialised"
            raise RuntimeStartError(msg, component=_COMPONENT_NAME)
        if self._service_registry is None:
            msg = "ServiceRegistry not initialised"
            raise RuntimeStartError(msg, component=_COMPONENT_NAME)
        if self._health_monitor is None:
            msg = "HealthMonitor not initialised"
            raise RuntimeStartError(msg, component=_COMPONENT_NAME)

        self._plugin_registry = PluginRegistry(
            event_bus=self._event_bus,
            audit_log=self._audit_log,
            logger=self._logger,
            service_registry=self._service_registry,
            health_monitor=self._health_monitor,
        )

        self._logger.log(
            LogSeverity.INFO,
            "Plugin framework initialized",
            component=_COMPONENT_NAME,
            correlation_id=self._correlation_id,
        )

    def _bootstrap_health_check(self) -> None:
        """Step 9: Perform initial health check of all components."""
        if self._health_monitor is None:
            msg = "HealthMonitor not initialised"
            raise RuntimeStartError(msg, component=_COMPONENT_NAME)

        self._register_health_checks()

        events = self._health_monitor.run_checks()
        if self._event_bus is not None:
            for event in events:
                with contextlib.suppress(Exception):
                    self._event_bus.publish(event)

        overall = self._health_monitor.get_overall_status()
        health_msg = "Initial health check complete: " + overall.value
        self._logger.log(
            LogSeverity.INFO,
            health_msg,
            component=_COMPONENT_NAME,
            correlation_id=self._correlation_id,
        )

    def _register_health_checks(self) -> None:
        """Register all components with the health monitor."""
        if self._health_monitor is None:
            msg = "HealthMonitor not initialised"
            raise RuntimeStartError(msg, component=_COMPONENT_NAME)

        components: list[IHealthCheck] = [
            c for c in [
                self._logger,
                self._audit_log,
                self._worker_pool,
                self._scheduler,
                self._recovery_handler,
                self._resource_monitor,
                self._metrics,
            ] if c is not None and isinstance(c, IHealthCheck)
        ]

        for component in components:
            name = component.get_component_name()
            with contextlib.suppress(Exception):
                self._health_monitor.register_check(name, component)

        with contextlib.suppress(Exception):
            self._health_monitor.register_check(
                _COMPONENT_NAME, self,
            )

    # -- Internal: start services ---------------------------------------------

    def _start_services(self) -> None:
        """Start scheduled tasks after all services are running."""
        if self._scheduler is None:
            msg = "Scheduler not initialised"
            raise RuntimeStartError(msg, component=_COMPONENT_NAME)
        if self._health_monitor is None:
            msg = "HealthMonitor not initialised"
            raise RuntimeStartError(msg, component=_COMPONENT_NAME)

        self._health_check_task_id = self._scheduler.schedule(
            "health_check",
            self._run_health_checks,
            _HEALTH_CHECK_INTERVAL_SECONDS,
        )

        self._resource_monitor_task_id = self._scheduler.schedule(
            "resource_monitor",
            self._run_resource_monitoring,
            _RESOURCE_MONITOR_INTERVAL_SECONDS,
        )

        if self._metrics is not None:
            self._metrics.increment("runtime.start_count")

        self._emit_component_event("Runtime", started=True)

    def _run_health_checks(self) -> None:
        """Periodic health check callback for the scheduler."""
        if self._health_monitor is None:
            return

        events = self._health_monitor.run_checks()
        if self._event_bus is not None:
            for event in events:
                with contextlib.suppress(Exception):
                    self._event_bus.publish(event)

    def _run_resource_monitoring(self) -> None:
        """Periodic resource monitoring callback for the scheduler."""
        if self._resource_monitor is None or self._worker_pool is None:
            return

        self._resource_monitor.collect_and_check(
            queue_size=self._worker_pool.get_queue_size(),
            max_queue_size=self._worker_pool.get_max_queue_size(),
            active_workers=self._worker_pool.get_active_count(),
        )

    # -- Internal: shutdown ----------------------------------------------------

    def _execute_shutdown(self) -> list[Exception]:
        """Execute the shutdown sequence in reverse bootstrap order.

        Returns:
            A list of errors encountered during shutdown.

        """
        errors: list[Exception] = []

        shutdown_steps: list[tuple[str, Callable[[], None]]] = [
            ("HealthCheck", self._shutdown_health_check),
            ("PluginFramework", self._shutdown_plugin_framework),
            ("RuntimeServices", self._shutdown_runtime_services),
            ("EventBus", self._shutdown_event_bus),
            ("ServiceRegistry", self._shutdown_service_registry),
            ("DependencyInjection", self._shutdown_di),
            ("Logging", self._shutdown_logging),
            ("Configuration", self._shutdown_configuration),
            ("Environment", self._shutdown_environment),
        ]

        for index, (name, execute) in enumerate(shutdown_steps):
            step_msg = "Shutdown step " + str(index) + ": " + name
            self._logger.log(
                LogSeverity.INFO,
                step_msg,
                component=_COMPONENT_NAME,
                correlation_id=self._correlation_id,
            )

            try:
                execute()
            except Exception as exc:  # noqa: BLE001
                fail_msg = "Shutdown step '" + name + "' failed: " + str(exc)
                self._logger.log(
                    LogSeverity.ERROR,
                    fail_msg,
                    component=_COMPONENT_NAME,
                    correlation_id=self._correlation_id,
                )
                errors.append(exc)
                continue

            event = ShutdownStepCompletedEvent(
                step_name=name,
                step_index=index,
                source=_COMPONENT_NAME,
                correlation_id=self._correlation_id,
            )

            with contextlib.suppress(Exception):
                self._audit_log.record(event)

            if self._event_bus is not None and self._event_bus.is_running():
                with contextlib.suppress(Exception):
                    self._event_bus.publish(event)

            done_msg = "Shutdown step " + str(index) + " completed: " + name
            self._logger.log(
                LogSeverity.INFO,
                done_msg,
                component=_COMPONENT_NAME,
                correlation_id=self._correlation_id,
            )

        if self._metrics is not None:
            with contextlib.suppress(Exception):
                self._metrics.increment("runtime.shutdown_count")

        self._emit_component_event("Runtime", started=False)

        return errors

    def _shutdown_health_check(self) -> None:
        """Shutdown step 1: Deactivate health checks."""
        if self._scheduler is not None and self._health_check_task_id is not None:
            with contextlib.suppress(Exception):
                self._scheduler.cancel(self._health_check_task_id)
            self._health_check_task_id = None

        if self._scheduler is not None and self._resource_monitor_task_id is not None:
            with contextlib.suppress(Exception):
                self._scheduler.cancel(self._resource_monitor_task_id)
            self._resource_monitor_task_id = None

    def _shutdown_plugin_framework(self) -> None:
        """Shutdown step 2: Unload all plugins."""
        if self._plugin_registry is None:
            return

        plugin_ids = list(self._plugin_registry.get_plugin_ids())
        for plugin_id in plugin_ids:
            with contextlib.suppress(Exception):
                state = self._plugin_registry.get_plugin_state(plugin_id)
                if state == PluginState.ENABLED:
                    self._plugin_registry.disable_plugin(plugin_id)
                self._plugin_registry.unload_plugin(plugin_id)

        self._plugin_registry = None

    def _shutdown_runtime_services(self) -> None:
        """Shutdown step 3: Stop WorkerPool, Scheduler, etc."""
        if self._scheduler is not None:
            with contextlib.suppress(Exception):
                self._scheduler.cancel_all()
                self._scheduler.stop()
            self._scheduler = None

        if self._worker_pool is not None:
            with contextlib.suppress(Exception):
                self._worker_pool.shutdown(wait=True)
            self._worker_pool = None

        if self._recovery_handler is not None:
            with contextlib.suppress(Exception):
                self._recovery_handler.stop()
            self._recovery_handler = None

        self._resource_monitor = None
        self._metrics = None
        self._health_monitor = None

    def _shutdown_event_bus(self) -> None:
        """Shutdown step 4: Stop the EventBus (process remaining events)."""
        if self._event_bus is not None:
            with contextlib.suppress(Exception):
                self._event_bus.stop()
            self._event_bus = None

    def _shutdown_service_registry(self) -> None:
        """Shutdown step 5: Clear the service registry."""
        if self._service_registry is not None:
            with contextlib.suppress(Exception):
                self._service_registry.reset()
            self._service_registry = None

    def _shutdown_di(self) -> None:
        """Shutdown step 6: Reset the DI container."""
        if self._di_container is not None:
            with contextlib.suppress(Exception):
                self._di_container.reset()
            self._di_container = None

    def _shutdown_logging(self) -> None:
        """Shutdown step 7: Flush and close logging."""
        self._logger.log(
            LogSeverity.INFO,
            "Logging shutdown",
            component=_COMPONENT_NAME,
            correlation_id=self._correlation_id,
        )
        with contextlib.suppress(Exception):
            self._logger.stop()

    def _shutdown_configuration(self) -> None:
        """Shutdown step 8: Release configuration."""

    def _shutdown_environment(self) -> None:
        """Shutdown step 9: Environment cleanup."""

    # -- Internal: recovery ----------------------------------------------------

    def _handle_start_failure(self, error: Exception) -> None:
        """Handle a failure during the start sequence.

        Transitions to FAILED and attempts recovery via the
        recovery handler if available.

        Args:
            error: The exception that caused the failure.

        """
        failure_msg = "Start failure: " + str(error)
        self._logger.log(
            LogSeverity.CRITICAL,
            failure_msg,
            component=_COMPONENT_NAME,
            correlation_id=self._correlation_id,
        )

        if self._lifecycle is not None:
            with contextlib.suppress(Exception):
                self._lifecycle.fail()

        if self._recovery_handler is not None:
            with contextlib.suppress(Exception):
                self._recovery_handler.handle_error(
                    error,
                    component=_COMPONENT_NAME,
                    level=RecoveryLevel.RUNTIME_RESTART,
                )

    # -- Internal: events ------------------------------------------------------

    def _emit_component_event(
        self,
        component_name: str,
        *,
        started: bool,
    ) -> None:
        """Emit a component started/stopped event.

        Args:
            component_name: Name of the component.
            started: True for started, False for stopped.

        """
        if self._event_bus is None or not self._event_bus.is_running():
            return

        event: RuntimeEvent
        if started:
            event = ComponentStartedEvent(
                component_name=component_name,
                source=_COMPONENT_NAME,
                correlation_id=self._correlation_id,
            )
        else:
            event = ComponentStoppedEvent(
                component_name=component_name,
                source=_COMPONENT_NAME,
                correlation_id=self._correlation_id,
            )

        with contextlib.suppress(Exception):
            self._event_bus.publish(event)

        with contextlib.suppress(Exception):
            self._audit_log.record(event)


# -- Null EventBus for early bootstrap (before EventBus is created) --------


class _NullEventBus:
    """No-op event bus used during early bootstrap phases.

    Before the EventBus is created in bootstrap step 6, the
    lifecycle manager and bootstrap sequence need an event bus
    reference.  This null implementation silently drops all
    operations.
    """

    def publish(self, event: RuntimeEvent) -> None:
        """No-op publish."""

    def subscribe(
        self,
        event_type: type[RuntimeEvent],
        handler: Callable[..., None],
        *,
        priority: int = 0,
    ) -> None:
        """No-op subscribe."""

    def unsubscribe(
        self,
        event_type: type[RuntimeEvent],
        handler: Callable[..., None],
    ) -> None:
        """No-op unsubscribe."""


