"""Unit tests for the ServiceRegistry implementation.

Tests cover:
- Registration and resolution
- Input validation
- Duplicate registration prevention
- Thread-safe access
- Lifecycle management (start/stop)
- Unregistration
- Reset
- Exception attributes
"""

from __future__ import annotations

import threading
from typing import Any, Protocol, runtime_checkable

import pytest

from jochen_x.core.exceptions.base import JochenXError
from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.interfaces.service_registry import IServiceRegistry
from jochen_x.core.registry.service_registry import (
    ServiceNotFoundError,
    ServiceRegistry,
)

_THREAD_COUNT = 8


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------


@runtime_checkable
class IDummyService(Protocol):
    """A dummy protocol for testing."""

    def do_work(self) -> str: ...


@runtime_checkable
class IAnotherService(Protocol):
    """Another dummy protocol for testing."""

    def compute(self) -> int: ...


class DummyService:
    """A simple service implementation."""

    def do_work(self) -> str:
        return "done"


class AnotherService:
    """Another service implementation."""

    def compute(self) -> int:
        return 42


class LifecycleService:
    """A service that tracks lifecycle calls."""

    def __init__(self) -> None:
        self.initialized: bool = False
        self.started: bool = False
        self.stopped: bool = False

    def initialize(self) -> None:
        self.initialized = True

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True

    def do_work(self) -> str:
        return "lifecycle"


class FailingStartService:
    """A service that fails on start."""

    def initialize(self) -> None:
        pass

    def start(self) -> None:
        msg = "Start failed"
        raise JochenXError(msg, component="FailingStartService")

    def stop(self) -> None:
        pass


class FailingStopService:
    """A service that fails on stop."""

    def initialize(self) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        msg = "Stop failed"
        raise JochenXError(msg, component="FailingStopService")


# ---------------------------------------------------------------------------
# TestServiceNotFoundError
# ---------------------------------------------------------------------------


class TestServiceNotFoundError:
    """Tests for the ServiceNotFoundError exception."""

    def test_inherits_from_jochen_x_error(self) -> None:
        error = ServiceNotFoundError(IDummyService)
        assert isinstance(error, JochenXError)

    def test_message_contains_interface_name(self) -> None:
        error = ServiceNotFoundError(IDummyService)
        assert "IDummyService" in str(error)

    def test_requested_interface_attribute(self) -> None:
        error = ServiceNotFoundError(IDummyService)
        assert error.requested_interface is IDummyService

    def test_component_is_service_registry(self) -> None:
        error = ServiceNotFoundError(IDummyService)
        assert error.component == "ServiceRegistry"

    def test_correlation_id_auto_generated(self) -> None:
        error = ServiceNotFoundError(IDummyService)
        assert error.correlation_id != ""

    def test_correlation_id_custom(self) -> None:
        error = ServiceNotFoundError(IDummyService, correlation_id="test-123")
        assert error.correlation_id == "test-123"


# ---------------------------------------------------------------------------
# TestServiceRegistryRegistration
# ---------------------------------------------------------------------------


class TestServiceRegistryRegistration:
    """Tests for service registration."""

    def test_register_and_resolve(self) -> None:
        registry = ServiceRegistry()
        service = DummyService()
        registry.register(IDummyService, service)
        assert registry.resolve(IDummyService) is service

    def test_register_multiple_services(self) -> None:
        registry = ServiceRegistry()
        svc1 = DummyService()
        svc2 = AnotherService()
        registry.register(IDummyService, svc1)
        registry.register(IAnotherService, svc2)
        assert registry.resolve(IDummyService) is svc1
        assert registry.resolve(IAnotherService) is svc2

    def test_duplicate_registration_raises(self) -> None:
        registry = ServiceRegistry()
        registry.register(IDummyService, DummyService())
        with pytest.raises(InputValidationError, match="already registered"):
            registry.register(IDummyService, DummyService())

    def test_duplicate_registration_error_field_name(self) -> None:
        registry = ServiceRegistry()
        registry.register(IDummyService, DummyService())
        with pytest.raises(InputValidationError) as exc_info:
            registry.register(IDummyService, DummyService())
        assert exc_info.value.field_name == "interface"

    def test_register_non_type_interface_raises(self) -> None:
        registry = ServiceRegistry()
        with pytest.raises(InputValidationError, match="Expected a type"):
            registry.register("not_a_type", DummyService())  # type: ignore[arg-type]

    def test_register_none_implementation_raises(self) -> None:
        registry = ServiceRegistry()
        with pytest.raises(InputValidationError, match="must not be None"):
            registry.register(IDummyService, None)  # type: ignore[arg-type]

    def test_register_integer_interface_raises(self) -> None:
        registry = ServiceRegistry()
        with pytest.raises(InputValidationError):
            registry.register(42, DummyService())  # type: ignore[arg-type]

    def test_registration_preserves_order(self) -> None:
        registry = ServiceRegistry()
        registry.register(IDummyService, DummyService())
        registry.register(IAnotherService, AnotherService())
        interfaces = registry.get_registered_interfaces()
        assert list(interfaces) == [IDummyService, IAnotherService]


# ---------------------------------------------------------------------------
# TestServiceRegistryResolution
# ---------------------------------------------------------------------------


class TestServiceRegistryResolution:
    """Tests for service resolution."""

    def test_resolve_returns_same_instance(self) -> None:
        registry = ServiceRegistry()
        service = DummyService()
        registry.register(IDummyService, service)
        assert registry.resolve(IDummyService) is service
        assert registry.resolve(IDummyService) is service

    def test_resolve_unregistered_raises(self) -> None:
        registry = ServiceRegistry()
        with pytest.raises(ServiceNotFoundError):
            registry.resolve(IDummyService)

    def test_resolve_unregistered_error_has_interface(self) -> None:
        registry = ServiceRegistry()
        with pytest.raises(ServiceNotFoundError) as exc_info:
            registry.resolve(IDummyService)
        assert exc_info.value.requested_interface is IDummyService

    def test_resolve_non_type_raises(self) -> None:
        registry = ServiceRegistry()
        with pytest.raises(InputValidationError, match="Expected a type"):
            registry.resolve("not_a_type")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# TestServiceRegistryQuery
# ---------------------------------------------------------------------------


class TestServiceRegistryQuery:
    """Tests for query methods (has, get_registered_interfaces)."""

    def test_has_registered_service(self) -> None:
        registry = ServiceRegistry()
        registry.register(IDummyService, DummyService())
        assert registry.has(IDummyService) is True

    def test_has_unregistered_service(self) -> None:
        registry = ServiceRegistry()
        assert registry.has(IDummyService) is False

    def test_get_registered_interfaces_empty(self) -> None:
        registry = ServiceRegistry()
        assert list(registry.get_registered_interfaces()) == []

    def test_get_registered_interfaces_returns_copy(self) -> None:
        registry = ServiceRegistry()
        registry.register(IDummyService, DummyService())
        interfaces1 = registry.get_registered_interfaces()
        interfaces2 = registry.get_registered_interfaces()
        assert interfaces1 is not interfaces2
        assert list(interfaces1) == list(interfaces2)

    def test_has_after_unregister(self) -> None:
        registry = ServiceRegistry()
        registry.register(IDummyService, DummyService())
        registry.unregister(IDummyService)
        assert registry.has(IDummyService) is False


# ---------------------------------------------------------------------------
# TestServiceRegistryProtocolCompliance
# ---------------------------------------------------------------------------


class TestServiceRegistryProtocolCompliance:
    """Verify that ServiceRegistry implements IServiceRegistry."""

    def test_is_instance_of_protocol(self) -> None:
        registry = ServiceRegistry()
        assert isinstance(registry, IServiceRegistry)

    def test_protocol_register(self) -> None:
        registry: IServiceRegistry = ServiceRegistry()
        registry.register(IDummyService, DummyService())
        assert registry.has(IDummyService)

    def test_protocol_resolve(self) -> None:
        registry: IServiceRegistry = ServiceRegistry()
        service = DummyService()
        registry.register(IDummyService, service)
        assert registry.resolve(IDummyService) is service

    def test_protocol_has(self) -> None:
        registry: IServiceRegistry = ServiceRegistry()
        assert registry.has(IDummyService) is False
        registry.register(IDummyService, DummyService())
        assert registry.has(IDummyService) is True

    def test_protocol_get_registered_interfaces(self) -> None:
        registry: IServiceRegistry = ServiceRegistry()
        registry.register(IDummyService, DummyService())
        assert IDummyService in registry.get_registered_interfaces()


# ---------------------------------------------------------------------------
# TestServiceRegistryLifecycle
# ---------------------------------------------------------------------------


class TestServiceRegistryLifecycle:
    """Tests for lifecycle management (start/stop)."""

    def test_start_calls_start_on_lifecycle_services(self) -> None:
        registry = ServiceRegistry()
        svc = LifecycleService()
        registry.register(IDummyService, svc)
        registry.start()
        assert svc.started is True

    def test_start_does_not_affect_non_lifecycle_services(self) -> None:
        registry = ServiceRegistry()
        svc = DummyService()
        registry.register(IDummyService, svc)
        registry.start()
        assert not hasattr(svc, "started")

    def test_stop_calls_stop_on_lifecycle_services(self) -> None:
        registry = ServiceRegistry()
        svc = LifecycleService()
        registry.register(IDummyService, svc)
        registry.start()
        registry.stop()
        assert svc.stopped is True

    def test_stop_in_reverse_registration_order(self) -> None:
        registry = ServiceRegistry()
        call_order: list[str] = []

        class SvcA:
            def initialize(self) -> None:
                pass

            def start(self) -> None:
                pass

            def stop(self) -> None:
                call_order.append("A")

        class SvcB:
            def initialize(self) -> None:
                pass

            def start(self) -> None:
                pass

            def stop(self) -> None:
                call_order.append("B")

        class SvcC:
            def initialize(self) -> None:
                pass

            def start(self) -> None:
                pass

            def stop(self) -> None:
                call_order.append("C")

        class IfaceA(Protocol):
            ...

        class IfaceB(Protocol):
            ...

        class IfaceC(Protocol):
            ...

        registry.register(IfaceA, SvcA())
        registry.register(IfaceB, SvcB())
        registry.register(IfaceC, SvcC())
        registry.start()
        registry.stop()
        assert call_order == ["C", "B", "A"]

    def test_start_in_registration_order(self) -> None:
        registry = ServiceRegistry()
        call_order: list[str] = []

        class SvcA:
            def initialize(self) -> None:
                pass

            def start(self) -> None:
                call_order.append("A")

            def stop(self) -> None:
                pass

        class SvcB:
            def initialize(self) -> None:
                pass

            def start(self) -> None:
                call_order.append("B")

            def stop(self) -> None:
                pass

        class IfaceA(Protocol):
            ...

        class IfaceB(Protocol):
            ...

        registry.register(IfaceA, SvcA())
        registry.register(IfaceB, SvcB())
        registry.start()
        assert call_order == ["A", "B"]

    def test_start_failure_stops_previously_started(self) -> None:
        registry = ServiceRegistry()
        svc1 = LifecycleService()
        failing = FailingStartService()

        class IfaceA(Protocol):
            ...

        class IfaceB(Protocol):
            ...

        registry.register(IfaceA, svc1)
        registry.register(IfaceB, failing)

        with pytest.raises(JochenXError, match="Start failed"):
            registry.start()

        assert svc1.started is True
        assert svc1.stopped is True

    def test_stop_continues_on_individual_failure(self) -> None:
        registry = ServiceRegistry()
        svc1 = LifecycleService()
        failing = FailingStopService()

        class IfaceA(Protocol):
            ...

        class IfaceB(Protocol):
            ...

        registry.register(IfaceA, svc1)
        registry.register(IfaceB, failing)
        registry.start()

        with pytest.raises(JochenXError, match="Stop failed"):
            registry.stop()

        assert svc1.stopped is True

    def test_stop_raises_first_error(self) -> None:
        registry = ServiceRegistry()

        class FailA:
            def initialize(self) -> None:
                pass

            def start(self) -> None:
                pass

            def stop(self) -> None:
                msg = "Error A"
                raise JochenXError(msg)

        class FailB:
            def initialize(self) -> None:
                pass

            def start(self) -> None:
                pass

            def stop(self) -> None:
                msg = "Error B"
                raise JochenXError(msg)

        class IfaceA(Protocol):
            ...

        class IfaceB(Protocol):
            ...

        registry.register(IfaceA, FailA())
        registry.register(IfaceB, FailB())
        registry.start()

        with pytest.raises(JochenXError, match="Error B"):
            registry.stop()

    def test_initialize_is_callable(self) -> None:
        registry = ServiceRegistry()
        registry.initialize()

    def test_mixed_lifecycle_and_non_lifecycle(self) -> None:
        registry = ServiceRegistry()
        lifecycle_svc = LifecycleService()
        plain_svc = DummyService()

        registry.register(IDummyService, plain_svc)
        registry.register(IAnotherService, lifecycle_svc)  # type: ignore[arg-type]

        registry.start()
        assert lifecycle_svc.started is True

        registry.stop()
        assert lifecycle_svc.stopped is True


# ---------------------------------------------------------------------------
# TestServiceRegistryUnregister
# ---------------------------------------------------------------------------


class TestServiceRegistryUnregister:
    """Tests for service unregistration."""

    def test_unregister_removes_service(self) -> None:
        registry = ServiceRegistry()
        registry.register(IDummyService, DummyService())
        registry.unregister(IDummyService)
        assert registry.has(IDummyService) is False

    def test_unregister_nonexistent_raises(self) -> None:
        registry = ServiceRegistry()
        with pytest.raises(ServiceNotFoundError):
            registry.unregister(IDummyService)

    def test_unregister_non_type_raises(self) -> None:
        registry = ServiceRegistry()
        with pytest.raises(InputValidationError, match="Expected a type"):
            registry.unregister("not_a_type")  # type: ignore[arg-type]

    def test_unregister_stops_lifecycle_service_when_started(self) -> None:
        registry = ServiceRegistry()
        svc = LifecycleService()
        registry.register(IDummyService, svc)
        registry.start()
        registry.unregister(IDummyService)
        assert svc.stopped is True

    def test_unregister_does_not_stop_when_not_started(self) -> None:
        registry = ServiceRegistry()
        svc = LifecycleService()
        registry.register(IDummyService, svc)
        registry.unregister(IDummyService)
        assert svc.stopped is False

    def test_unregister_allows_re_registration(self) -> None:
        registry = ServiceRegistry()
        svc1 = DummyService()
        svc2 = DummyService()
        registry.register(IDummyService, svc1)
        registry.unregister(IDummyService)
        registry.register(IDummyService, svc2)
        assert registry.resolve(IDummyService) is svc2


# ---------------------------------------------------------------------------
# TestServiceRegistryReset
# ---------------------------------------------------------------------------


class TestServiceRegistryReset:
    """Tests for registry reset."""

    def test_reset_clears_all_services(self) -> None:
        registry = ServiceRegistry()
        registry.register(IDummyService, DummyService())
        registry.register(IAnotherService, AnotherService())
        registry.reset()
        assert list(registry.get_registered_interfaces()) == []

    def test_reset_stops_lifecycle_services_when_started(self) -> None:
        registry = ServiceRegistry()
        svc = LifecycleService()
        registry.register(IDummyService, svc)
        registry.start()
        registry.reset()
        assert svc.stopped is True

    def test_reset_without_start_does_not_stop(self) -> None:
        registry = ServiceRegistry()
        svc = LifecycleService()
        registry.register(IDummyService, svc)
        registry.reset()
        assert svc.stopped is False

    def test_reset_allows_fresh_registration(self) -> None:
        registry = ServiceRegistry()
        registry.register(IDummyService, DummyService())
        registry.reset()
        new_svc = DummyService()
        registry.register(IDummyService, new_svc)
        assert registry.resolve(IDummyService) is new_svc


# ---------------------------------------------------------------------------
# TestServiceRegistryThreadSafety
# ---------------------------------------------------------------------------


class TestServiceRegistryThreadSafety:
    """Tests for thread-safe access."""

    def test_concurrent_registration(self) -> None:
        registry = ServiceRegistry()
        errors: list[Exception] = []
        barrier = threading.Barrier(_THREAD_COUNT)

        protocols: list[type[Any]] = []
        for i in range(_THREAD_COUNT):
            ns: dict[str, Any] = {}
            exec(  # noqa: S102
                f"class Proto{i}:\n    pass",
                ns,
            )
            protocols.append(ns[f"Proto{i}"])

        def register_one(idx: int) -> None:
            try:
                barrier.wait()
                registry.register(protocols[idx], DummyService())
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=register_one, args=(i,))
            for i in range(_THREAD_COUNT)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert len(registry.get_registered_interfaces()) == _THREAD_COUNT

    def test_concurrent_resolve(self) -> None:
        registry = ServiceRegistry()
        service = DummyService()
        registry.register(IDummyService, service)

        results: list[Any] = []
        barrier = threading.Barrier(_THREAD_COUNT)

        def resolve_one() -> None:
            barrier.wait()
            results.append(registry.resolve(IDummyService))

        threads = [
            threading.Thread(target=resolve_one) for _ in range(_THREAD_COUNT)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == _THREAD_COUNT
        assert all(r is service for r in results)

    def test_concurrent_has(self) -> None:
        registry = ServiceRegistry()
        registry.register(IDummyService, DummyService())

        results: list[bool] = []
        barrier = threading.Barrier(_THREAD_COUNT)

        def check_one() -> None:
            barrier.wait()
            results.append(registry.has(IDummyService))

        threads = [
            threading.Thread(target=check_one) for _ in range(_THREAD_COUNT)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert all(results)

    def test_concurrent_register_and_resolve(self) -> None:
        registry = ServiceRegistry()
        registry.register(IDummyService, DummyService())

        errors: list[Exception] = []
        thread_count = 4
        barrier = threading.Barrier(thread_count)

        protocols: list[type[Any]] = []
        for i in range(2):
            ns: dict[str, Any] = {}
            exec(  # noqa: S102
                f"class ConcProto{i}:\n    pass",
                ns,
            )
            protocols.append(ns[f"ConcProto{i}"])

        def register_one(idx: int) -> None:
            try:
                barrier.wait()
                registry.register(protocols[idx], AnotherService())
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        def resolve_one() -> None:
            try:
                barrier.wait()
                registry.resolve(IDummyService)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=register_one, args=(0,)),
            threading.Thread(target=register_one, args=(1,)),
            threading.Thread(target=resolve_one),
            threading.Thread(target=resolve_one),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []


# ---------------------------------------------------------------------------
# TestServiceRegistryEdgeCases
# ---------------------------------------------------------------------------


class TestServiceRegistryEdgeCases:
    """Edge-case and boundary tests."""

    def test_register_with_concrete_class_as_interface(self) -> None:
        registry = ServiceRegistry()
        svc = DummyService()
        registry.register(DummyService, svc)
        assert registry.resolve(DummyService) is svc

    def test_resolve_after_reset_raises(self) -> None:
        registry = ServiceRegistry()
        registry.register(IDummyService, DummyService())
        registry.reset()
        with pytest.raises(ServiceNotFoundError):
            registry.resolve(IDummyService)

    def test_start_with_no_services(self) -> None:
        registry = ServiceRegistry()
        registry.start()

    def test_stop_with_no_services(self) -> None:
        registry = ServiceRegistry()
        registry.stop()

    def test_start_stop_start_cycle(self) -> None:
        registry = ServiceRegistry()
        svc = LifecycleService()
        registry.register(IDummyService, svc)
        registry.start()
        assert svc.started is True
        registry.stop()
        assert svc.stopped is True

    def test_multiple_lifecycle_services(self) -> None:
        registry = ServiceRegistry()

        class IfaceA(Protocol):
            ...

        class IfaceB(Protocol):
            ...

        svc_a = LifecycleService()
        svc_b = LifecycleService()
        registry.register(IfaceA, svc_a)
        registry.register(IfaceB, svc_b)
        registry.start()
        assert svc_a.started is True
        assert svc_b.started is True
        registry.stop()
        assert svc_a.stopped is True
        assert svc_b.stopped is True

    def test_get_registered_interfaces_after_unregister(self) -> None:
        registry = ServiceRegistry()
        registry.register(IDummyService, DummyService())
        registry.register(IAnotherService, AnotherService())
        registry.unregister(IDummyService)
        interfaces = registry.get_registered_interfaces()
        assert list(interfaces) == [IAnotherService]

    def test_error_component_is_service_registry(self) -> None:
        registry = ServiceRegistry()
        with pytest.raises(InputValidationError) as exc_info:
            registry.register("bad", DummyService())  # type: ignore[arg-type]
        assert exc_info.value.component == "ServiceRegistry"
