import asyncio
import unittest

from core.ai_contracts import AICapability
from core.extensions import (
    CommandExtension,
    PluginExtension,
    ToolExtension,
    UIExtension,
    WorkflowExtension,
)
from core.observability import Metrics, Tracer
from core.resources import ResourceSnapshot
from core.events import Event, EventBus
from core.lifecycle import LifecycleManager, LifecycleState
from core.performance import PerformanceController, PerformanceMode
from core.registry import CircularDependencyError, Lifetime, ServiceRegistry
from core.scheduler import Schedule, TaskScheduler
from services.security import CapabilityModel, Permission, SecurityContext


class CycleA:
    def __init__(self, dependency: "CycleB") -> None:
        pass


class CycleB:
    def __init__(self, dependency: CycleA) -> None:
        pass


class CoreTests(unittest.TestCase):
    def test_event_priority_filter_wildcard_history_and_sticky(self) -> None:
        bus = EventBus(history_size=2)
        received: list[str] = []
        bus.subscribe("system.*", lambda e: received.append("low"))
        bus.subscribe("system.ready", lambda e: received.append("high"), priority=1)
        bus.publish(Event("system.ready", {}), sticky=True)
        self.assertEqual(received, ["high", "low"])
        sticky: list[str] = []
        bus.subscribe("system.*", lambda e: sticky.append(e.name))
        self.assertEqual(sticky, ["system.ready"])
        self.assertEqual(bus.history()[0].name, "system.ready")

    def test_event_async(self) -> None:
        async def run() -> list[str]:
            bus = EventBus()
            results: list[str] = []

            async def handler(event: Event) -> None:
                results.append(event.name)

            bus.subscribe("x", handler)
            await bus.publish_async(Event("x", {}))
            return results

        self.assertEqual(asyncio.run(run()), ["x"])

    def test_container_lifetimes_and_cycle(self) -> None:
        class Value:
            pass

        registry = ServiceRegistry()
        registry.register_type(Value, Value, lifetime=Lifetime.TRANSIENT)
        self.assertIsNot(registry.get(Value), registry.get(Value))
        cyclic = ServiceRegistry()
        cyclic.register_type(CycleA, CycleA)
        cyclic.register_type(CycleB, CycleB)
        with self.assertRaises(CircularDependencyError):
            cyclic.get(CycleA)

    def test_lifecycle_and_performance(self) -> None:
        events: list[str] = []
        lifecycle = LifecycleManager()
        lifecycle.register_module(
            "a", lambda: events.append("start"), lambda: events.append("stop")
        )
        lifecycle.start()
        lifecycle.shutdown()
        self.assertEqual(events, ["start", "stop"])
        self.assertIs(lifecycle.state, LifecycleState.STOPPED)
        controller = PerformanceController()
        controller.set_mode(PerformanceMode.GAMING)
        self.assertFalse(controller.permits("indexer"))

    def test_scheduler_and_security(self) -> None:
        async def run() -> list[str]:
            scheduler = TaskScheduler()
            completed: list[str] = []
            scheduler.schedule(lambda: _append(completed), Schedule())
            await asyncio.sleep(0.01)
            await scheduler.shutdown()
            return completed

        self.assertEqual(asyncio.run(run()), ["done"])
        context = SecurityContext("test", frozenset({Permission.NETWORK}))
        self.assertTrue(CapabilityModel().permits(context, Permission.NETWORK))

    def test_observability_resource_and_contract_shapes(self) -> None:
        metrics = Metrics()
        metrics.increment("jobs")
        self.assertEqual(metrics.snapshot(), {"jobs": 1})
        self.assertGreaterEqual(Tracer().start("test").started, 0)
        self.assertIsNone(ResourceSnapshot().gpu_percent)
        self.assertEqual(AICapability.STREAMING, "streaming")
        self.assertTrue(
            all(
                getattr(contract, "_is_protocol", False)
                for contract in (
                    PluginExtension,
                    ToolExtension,
                    UIExtension,
                    CommandExtension,
                    WorkflowExtension,
                )
            )
        )


def _append(items: list[str]) -> asyncio.coroutines:
    async def callback() -> None:
        items.append("done")

    return callback()
