"""Unit tests for the dependency injection container (Phase 2)."""

from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Protocol, runtime_checkable

import pytest

from jochen_x.core.di.container import (
    CircularDependencyError,
    DIContainer,
    DuplicateRegistrationError,
    ScopeError,
    ServiceNotRegisteredError,
)
from jochen_x.core.di.provider import ServiceProvider
from jochen_x.core.di.scope import ServiceScope
from jochen_x.core.exceptions.base import JochenXError
from jochen_x.core.exceptions.security import InputValidationError

EXPECTED_SCOPE_COUNT = 3
THREAD_COUNT = 8


# ---------------------------------------------------------------------------
# Test helpers — protocols and dummy implementations
# ---------------------------------------------------------------------------


@runtime_checkable
class IGreeter(Protocol):
    def greet(self) -> str: ...


@runtime_checkable
class ICounter(Protocol):
    def count(self) -> int: ...


@runtime_checkable
class ILogger(Protocol):
    def log(self, message: str) -> None: ...


class HelloGreeter:
    def greet(self) -> str:
        return "hello"


class SimpleCounter:
    _next = 0

    def __init__(self) -> None:
        SimpleCounter._next += 1
        self._value = SimpleCounter._next

    def count(self) -> int:
        return self._value


class SimpleLogger:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def log(self, message: str) -> None:
        self.messages.append(message)


# ---------------------------------------------------------------------------
# ServiceScope
# ---------------------------------------------------------------------------


class TestServiceScope:
    def test_enum_values(self) -> None:
        assert ServiceScope.SINGLETON.value == "SINGLETON"
        assert ServiceScope.TRANSIENT.value == "TRANSIENT"
        assert ServiceScope.SCOPED.value == "SCOPED"

    def test_all_members(self) -> None:
        assert len(ServiceScope) == EXPECTED_SCOPE_COUNT

    def test_unique(self) -> None:
        values = [s.value for s in ServiceScope]
        assert len(values) == len(set(values))


# ---------------------------------------------------------------------------
# ServiceProvider
# ---------------------------------------------------------------------------


class TestServiceProvider:
    def test_properties(self) -> None:
        provider = ServiceProvider(IGreeter, HelloGreeter, ServiceScope.SINGLETON)
        assert provider.interface is IGreeter
        assert provider.scope == ServiceScope.SINGLETON

    def test_transient_creates_new_instances(self) -> None:
        provider = ServiceProvider(IGreeter, HelloGreeter, ServiceScope.TRANSIENT)
        a = provider.create_instance()
        b = provider.create_instance()
        assert a is not b

    def test_singleton_returns_same_instance(self) -> None:
        provider = ServiceProvider(IGreeter, HelloGreeter, ServiceScope.SINGLETON)
        a = provider.create_instance()
        b = provider.create_instance()
        assert a is b

    def test_singleton_lazy_creation(self) -> None:
        call_count = 0

        def factory() -> HelloGreeter:
            nonlocal call_count
            call_count += 1
            return HelloGreeter()

        provider = ServiceProvider(IGreeter, factory, ServiceScope.SINGLETON)
        assert call_count == 0
        provider.create_instance()
        assert call_count == 1
        provider.create_instance()
        assert call_count == 1

    def test_reset_singleton(self) -> None:
        provider = ServiceProvider(IGreeter, HelloGreeter, ServiceScope.SINGLETON)
        first = provider.create_instance()
        provider.reset_singleton()
        second = provider.create_instance()
        assert first is not second

    def test_reset_singleton_no_effect_on_transient(self) -> None:
        provider = ServiceProvider(IGreeter, HelloGreeter, ServiceScope.TRANSIENT)
        provider.reset_singleton()
        a = provider.create_instance()
        b = provider.create_instance()
        assert a is not b

    def test_singleton_thread_safety(self) -> None:
        call_count = 0
        lock = threading.Lock()

        def counted_factory() -> HelloGreeter:
            nonlocal call_count
            with lock:
                call_count += 1
            return HelloGreeter()

        provider = ServiceProvider(IGreeter, counted_factory, ServiceScope.SINGLETON)

        with ThreadPoolExecutor(max_workers=THREAD_COUNT) as pool:
            futures = [
                pool.submit(provider.create_instance)
                for _ in range(THREAD_COUNT)
            ]
            results = [f.result() for f in as_completed(futures)]

        assert all(r is results[0] for r in results)
        assert call_count == 1

    def test_factory_exception_does_not_cache(self) -> None:
        attempts = 0
        expected_retries = 2

        def failing_then_ok() -> HelloGreeter:
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                msg = "first call fails"
                raise RuntimeError(msg)
            return HelloGreeter()

        provider = ServiceProvider(IGreeter, failing_then_ok, ServiceScope.SINGLETON)

        with pytest.raises(RuntimeError, match="first call fails"):
            provider.create_instance()

        result = provider.create_instance()
        assert isinstance(result, HelloGreeter)
        assert attempts == expected_retries


# ---------------------------------------------------------------------------
# DIContainer — Registration
# ---------------------------------------------------------------------------


class TestDIContainerRegistration:
    def test_register_and_resolve(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter, ServiceScope.SINGLETON)
        result = container.resolve(IGreeter)
        assert isinstance(result, HelloGreeter)

    def test_register_default_scope_is_singleton(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter)
        a = container.resolve(IGreeter)
        b = container.resolve(IGreeter)
        assert a is b

    def test_register_duplicate_raises(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter)
        with pytest.raises(DuplicateRegistrationError, match="IGreeter"):
            container.register(IGreeter, HelloGreeter)

    def test_register_duplicate_preserves_interface(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter)
        with pytest.raises(DuplicateRegistrationError) as exc_info:
            container.register(IGreeter, HelloGreeter)
        assert exc_info.value.duplicate_interface is IGreeter

    def test_register_invalid_interface_raises(self) -> None:
        container = DIContainer()
        with pytest.raises(InputValidationError, match="interface"):
            container.register("not_a_type", HelloGreeter)  # type: ignore[arg-type]

    def test_register_non_callable_factory_raises(self) -> None:
        container = DIContainer()
        with pytest.raises(InputValidationError, match="factory"):
            container.register(IGreeter, 42)  # type: ignore[arg-type]

    def test_register_invalid_scope_raises(self) -> None:
        container = DIContainer()
        with pytest.raises(InputValidationError, match="scope"):
            container.register(IGreeter, HelloGreeter, "SINGLETON")  # type: ignore[arg-type]

    def test_register_thread_safety(self) -> None:
        container = DIContainer()
        errors: list[Exception] = []
        expected_count = 4

        @runtime_checkable
        class IA(Protocol):
            pass

        @runtime_checkable
        class IB(Protocol):
            pass

        @runtime_checkable
        class IC(Protocol):
            pass

        @runtime_checkable
        class ID(Protocol):
            pass

        interfaces: list[type[Any]] = [IA, IB, IC, ID]

        def register_one(iface: type[Any]) -> None:
            try:
                container.register(iface, object, ServiceScope.TRANSIENT)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        with ThreadPoolExecutor(max_workers=expected_count) as pool:
            list(pool.map(register_one, interfaces))

        assert not errors
        assert len(container.get_registered_interfaces()) == expected_count


# ---------------------------------------------------------------------------
# DIContainer — Resolution
# ---------------------------------------------------------------------------


class TestDIContainerResolution:
    def test_resolve_singleton_same_instance(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter, ServiceScope.SINGLETON)
        a = container.resolve(IGreeter)
        b = container.resolve(IGreeter)
        assert a is b

    def test_resolve_transient_different_instances(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter, ServiceScope.TRANSIENT)
        a = container.resolve(IGreeter)
        b = container.resolve(IGreeter)
        assert a is not b

    def test_resolve_unregistered_raises(self) -> None:
        container = DIContainer()
        with pytest.raises(ServiceNotRegisteredError, match="IGreeter"):
            container.resolve(IGreeter)

    def test_resolve_unregistered_preserves_interface(self) -> None:
        container = DIContainer()
        with pytest.raises(ServiceNotRegisteredError) as exc_info:
            container.resolve(IGreeter)
        assert exc_info.value.requested_interface is IGreeter

    def test_resolve_scoped_outside_scope_raises(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter, ServiceScope.SCOPED)
        with pytest.raises(ScopeError, match="create_scope"):
            container.resolve(IGreeter)

    def test_resolve_lazy_initialization(self) -> None:
        call_count = 0

        def factory() -> HelloGreeter:
            nonlocal call_count
            call_count += 1
            return HelloGreeter()

        container = DIContainer()
        container.register(IGreeter, factory, ServiceScope.SINGLETON)
        assert call_count == 0
        container.resolve(IGreeter)
        assert call_count == 1
        container.resolve(IGreeter)
        assert call_count == 1

    def test_resolve_with_dependencies(self) -> None:
        container = DIContainer()

        container.register(ILogger, SimpleLogger, ServiceScope.SINGLETON)

        def greeter_factory() -> HelloGreeter:
            container.resolve(ILogger)
            return HelloGreeter()

        container.register(IGreeter, greeter_factory, ServiceScope.SINGLETON)
        result = container.resolve(IGreeter)
        assert isinstance(result, HelloGreeter)

    def test_resolve_concurrent_singleton(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter, ServiceScope.SINGLETON)

        with ThreadPoolExecutor(max_workers=THREAD_COUNT) as pool:
            futures = [
                pool.submit(container.resolve, IGreeter)
                for _ in range(THREAD_COUNT)
            ]
            results = [f.result() for f in as_completed(futures)]

        assert all(r is results[0] for r in results)


# ---------------------------------------------------------------------------
# DIContainer — Circular Dependency Detection
# ---------------------------------------------------------------------------


class TestCircularDependency:
    def test_self_referencing(self) -> None:
        container = DIContainer()
        container.register(
            IGreeter,
            lambda: container.resolve(IGreeter),
            ServiceScope.TRANSIENT,
        )
        with pytest.raises(CircularDependencyError, match=r"IGreeter.*IGreeter"):
            container.resolve(IGreeter)

    def test_two_way_cycle(self) -> None:
        container = DIContainer()
        container.register(
            IGreeter,
            lambda: container.resolve(ICounter),
            ServiceScope.TRANSIENT,
        )
        container.register(
            ICounter,
            lambda: container.resolve(IGreeter),
            ServiceScope.TRANSIENT,
        )
        with pytest.raises(CircularDependencyError):
            container.resolve(IGreeter)

    def test_three_way_chain_cycle(self) -> None:
        container = DIContainer()
        container.register(
            IGreeter,
            lambda: container.resolve(ICounter),
            ServiceScope.TRANSIENT,
        )
        container.register(
            ICounter,
            lambda: container.resolve(ILogger),
            ServiceScope.TRANSIENT,
        )
        container.register(
            ILogger,
            lambda: container.resolve(IGreeter),
            ServiceScope.TRANSIENT,
        )
        with pytest.raises(CircularDependencyError) as exc_info:
            container.resolve(IGreeter)

        assert "IGreeter" in exc_info.value.chain
        assert "ICounter" in exc_info.value.chain
        assert "ILogger" in exc_info.value.chain

    def test_error_message_shows_chain(self) -> None:
        container = DIContainer()
        container.register(
            IGreeter,
            lambda: container.resolve(ICounter),
            ServiceScope.TRANSIENT,
        )
        container.register(
            ICounter,
            lambda: container.resolve(IGreeter),
            ServiceScope.TRANSIENT,
        )
        with pytest.raises(CircularDependencyError) as exc_info:
            container.resolve(IGreeter)

        msg = str(exc_info.value)
        assert "Circular dependency detected" in msg
        assert "->" in msg

    def test_no_false_positive_after_successful_resolution(self) -> None:
        container = DIContainer()
        container.register(ILogger, SimpleLogger, ServiceScope.TRANSIENT)
        container.register(
            IGreeter,
            lambda: (container.resolve(ILogger), HelloGreeter())[1],
            ServiceScope.TRANSIENT,
        )
        result = container.resolve(IGreeter)
        assert isinstance(result, HelloGreeter)
        result2 = container.resolve(IGreeter)
        assert isinstance(result2, HelloGreeter)

    def test_stack_cleaned_after_exception(self) -> None:
        container = DIContainer()

        def failing_factory() -> HelloGreeter:
            msg = "factory error"
            raise RuntimeError(msg)

        container.register(IGreeter, failing_factory, ServiceScope.TRANSIENT)

        with pytest.raises(RuntimeError, match="factory error"):
            container.resolve(IGreeter)

        container.register(ICounter, SimpleCounter, ServiceScope.TRANSIENT)
        result = container.resolve(ICounter)
        assert isinstance(result, SimpleCounter)

    def test_thread_isolated_cycle_detection(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter, ServiceScope.TRANSIENT)
        container.register(ICounter, SimpleCounter, ServiceScope.TRANSIENT)

        barrier = threading.Barrier(2)
        results: list[Any] = [None, None]

        def resolve_in_thread(idx: int, iface: type[Any]) -> None:
            barrier.wait(timeout=5)
            results[idx] = container.resolve(iface)

        t1 = threading.Thread(target=resolve_in_thread, args=(0, IGreeter))
        t2 = threading.Thread(target=resolve_in_thread, args=(1, ICounter))
        t1.start()
        t2.start()
        t1.join(timeout=5)
        t2.join(timeout=5)

        assert isinstance(results[0], HelloGreeter)
        assert isinstance(results[1], SimpleCounter)


# ---------------------------------------------------------------------------
# DIContainer — Query & Lifecycle
# ---------------------------------------------------------------------------


class TestDIContainerQuery:
    def test_has_registered(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter)
        assert container.has(IGreeter)

    def test_has_not_registered(self) -> None:
        container = DIContainer()
        assert not container.has(IGreeter)

    def test_get_registered_interfaces_empty(self) -> None:
        container = DIContainer()
        assert len(container.get_registered_interfaces()) == 0

    def test_get_registered_interfaces(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter)
        container.register(ICounter, SimpleCounter)
        interfaces = container.get_registered_interfaces()
        expected_count = 2
        assert IGreeter in interfaces
        assert ICounter in interfaces
        assert len(interfaces) == expected_count

    def test_reset_clears_all(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter, ServiceScope.SINGLETON)
        first = container.resolve(IGreeter)
        container.reset()
        assert not container.has(IGreeter)
        assert len(container.get_registered_interfaces()) == 0

        container.register(IGreeter, HelloGreeter, ServiceScope.SINGLETON)
        second = container.resolve(IGreeter)
        assert first is not second


# ---------------------------------------------------------------------------
# ScopedContainer
# ---------------------------------------------------------------------------


class TestScopedContainer:
    def test_scoped_returns_same_within_scope(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter, ServiceScope.SCOPED)
        with container.create_scope() as scope:
            a = scope.resolve(IGreeter)
            b = scope.resolve(IGreeter)
            assert a is b

    def test_different_scopes_return_different(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter, ServiceScope.SCOPED)
        with container.create_scope() as scope1:
            a = scope1.resolve(IGreeter)
        with container.create_scope() as scope2:
            b = scope2.resolve(IGreeter)
        assert a is not b

    def test_singleton_shared_across_scopes(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter, ServiceScope.SINGLETON)
        with container.create_scope() as scope1:
            a = scope1.resolve(IGreeter)
        with container.create_scope() as scope2:
            b = scope2.resolve(IGreeter)
        parent_instance = container.resolve(IGreeter)
        assert a is b is parent_instance

    def test_transient_always_new_in_scope(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter, ServiceScope.TRANSIENT)
        with container.create_scope() as scope:
            a = scope.resolve(IGreeter)
            b = scope.resolve(IGreeter)
            assert a is not b

    def test_disposed_scope_raises(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter, ServiceScope.SCOPED)
        scope = container.create_scope()
        scope.dispose()
        with pytest.raises(ScopeError, match="disposed"):
            scope.resolve(IGreeter)

    def test_context_manager_disposes(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter, ServiceScope.SCOPED)
        with container.create_scope() as scope:
            scope.resolve(IGreeter)
        with pytest.raises(ScopeError, match="disposed"):
            scope.resolve(IGreeter)

    def test_has_delegates_to_parent(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter)
        with container.create_scope() as scope:
            assert scope.has(IGreeter)
            assert not scope.has(ICounter)

    def test_unregistered_in_scope_raises(self) -> None:
        container = DIContainer()
        with (
            container.create_scope() as scope,
            pytest.raises(ServiceNotRegisteredError),
        ):
            scope.resolve(IGreeter)

    def test_scoped_thread_safety(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter, ServiceScope.SCOPED)

        with container.create_scope() as scope:
            barrier = threading.Barrier(THREAD_COUNT)
            results: list[Any] = []
            lock = threading.Lock()

            def resolve_in_thread() -> None:
                barrier.wait(timeout=5)
                result = scope.resolve(IGreeter)
                with lock:
                    results.append(result)

            threads = [
                threading.Thread(target=resolve_in_thread)
                for _ in range(THREAD_COUNT)
            ]
            for t in threads:
                t.start()
            for t in threads:
                t.join(timeout=5)

            assert len(results) == THREAD_COUNT
            assert all(r is results[0] for r in results)

    def test_circular_dependency_in_scope(self) -> None:
        container = DIContainer()

        def greeter_factory() -> HelloGreeter:
            container.create_scope().resolve(ICounter)
            return HelloGreeter()

        container.register(IGreeter, greeter_factory, ServiceScope.SCOPED)
        container.register(
            ICounter,
            lambda: container.create_scope().resolve(IGreeter),
            ServiceScope.SCOPED,
        )

        with container.create_scope() as scope, pytest.raises(CircularDependencyError):
            scope.resolve(IGreeter)


# ---------------------------------------------------------------------------
# Exception attributes
# ---------------------------------------------------------------------------


class TestDIExceptions:
    def test_circular_dependency_has_correlation_id(self) -> None:
        err = CircularDependencyError("A -> B -> A")
        assert err.correlation_id
        assert err.component == "DIContainer"

    def test_service_not_registered_has_correlation_id(self) -> None:
        err = ServiceNotRegisteredError(IGreeter)
        assert err.correlation_id
        assert err.component == "DIContainer"

    def test_duplicate_registration_has_correlation_id(self) -> None:
        err = DuplicateRegistrationError(IGreeter)
        assert err.correlation_id
        assert err.component == "DIContainer"

    def test_scope_error_has_correlation_id(self) -> None:
        err = ScopeError("test error")
        assert err.correlation_id
        assert err.component == "DIContainer"

    def test_all_inherit_from_jochen_x_error(self) -> None:
        assert issubclass(CircularDependencyError, JochenXError)
        assert issubclass(ServiceNotRegisteredError, JochenXError)
        assert issubclass(DuplicateRegistrationError, JochenXError)
        assert issubclass(ScopeError, JochenXError)


# ---------------------------------------------------------------------------
# Integration: mixed scopes
# ---------------------------------------------------------------------------


class TestMixedScopes:
    def test_singleton_transient_scoped_together(self) -> None:
        container = DIContainer()
        container.register(IGreeter, HelloGreeter, ServiceScope.SINGLETON)
        container.register(ICounter, SimpleCounter, ServiceScope.TRANSIENT)
        container.register(ILogger, SimpleLogger, ServiceScope.SCOPED)

        singleton = container.resolve(IGreeter)
        transient1 = container.resolve(ICounter)
        transient2 = container.resolve(ICounter)
        assert singleton is container.resolve(IGreeter)
        assert transient1 is not transient2

        with container.create_scope() as scope:
            scoped1 = scope.resolve(ILogger)
            scoped2 = scope.resolve(ILogger)
            assert scoped1 is scoped2

            scope_singleton = scope.resolve(IGreeter)
            assert scope_singleton is singleton

            scope_transient = scope.resolve(ICounter)
            assert scope_transient is not transient1

    def test_factory_resolves_from_container(self) -> None:
        container = DIContainer()
        container.register(ILogger, SimpleLogger, ServiceScope.SINGLETON)

        def greeter_with_logger() -> HelloGreeter:
            logger = container.resolve(ILogger)
            assert isinstance(logger, SimpleLogger)
            return HelloGreeter()

        container.register(IGreeter, greeter_with_logger, ServiceScope.SINGLETON)
        result = container.resolve(IGreeter)
        assert isinstance(result, HelloGreeter)
