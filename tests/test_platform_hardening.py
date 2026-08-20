"""WP-001 Platform Hardening tests (FR-001, FR-002).

Covers AC-001.1 (complete transition table), AC-001.2 (no transition outside
the table), AC-001.3 (at least one test per transition), AC-002.1 (allowed set
explicitly defined and exported) and AC-002.2 (structured rejection result
carrying the reason) for both the application state machine and the core
lifecycle manager.
"""

from __future__ import annotations

import unittest

from core.exceptions import StateTransitionError, TransitionRejection
from core.lifecycle import LifecycleManager, LifecycleState
from core.lifecycle import transition_table as lifecycle_transition_table

from app.state_machine import (
    ApplicationState,
    ApplicationStateMachine,
    IllegalStateTransitionError,
    transition_table,
)


class ApplicationTransitionTableTests(unittest.TestCase):
    def test_table_is_complete_and_readonly(self) -> None:
        table = transition_table()
        self.assertEqual(set(table), set(ApplicationState))
        with self.assertRaises(TypeError):
            table[ApplicationState.READY] = frozenset()  # type: ignore[index]

    def test_shutdown_is_terminal(self) -> None:
        self.assertEqual(transition_table()[ApplicationState.SHUTDOWN], frozenset())

    def test_every_permitted_transition_executes(self) -> None:
        for source, targets in transition_table().items():
            for target in targets:
                with self.subTest(source=source, target=target):
                    machine = ApplicationStateMachine(initial_state=source)
                    self.assertTrue(machine.can_transition(target))
                    self.assertIs(machine.transition(target), target)
                    self.assertIs(machine.state, target)

    def test_every_non_permitted_transition_is_rejected(self) -> None:
        for source, targets in transition_table().items():
            for target in set(ApplicationState) - set(targets):
                with self.subTest(source=source, target=target):
                    machine = ApplicationStateMachine(initial_state=source)
                    self.assertFalse(machine.can_transition(target))
                    with self.assertRaises(IllegalStateTransitionError):
                        machine.transition(target)
                    self.assertIs(machine.state, source)

    def test_allowed_transitions_matches_table(self) -> None:
        for source, targets in transition_table().items():
            with self.subTest(source=source):
                machine = ApplicationStateMachine(initial_state=source)
                self.assertEqual(machine.allowed_transitions(), targets)


class ApplicationRejectionResultTests(unittest.TestCase):
    def test_rejected_transition_carries_structured_result(self) -> None:
        machine = ApplicationStateMachine(initial_state=ApplicationState.SHUTDOWN)
        with self.assertRaises(IllegalStateTransitionError) as caught:
            machine.transition(ApplicationState.READY)
        rejection = caught.exception.rejection
        self.assertIsInstance(rejection, TransitionRejection)
        self.assertEqual(rejection.source, "shutdown")
        self.assertEqual(rejection.target, "ready")
        self.assertIn("shutdown", rejection.reason)
        self.assertIn("ready", rejection.reason)
        self.assertEqual(rejection.allowed, ())

    def test_rejection_lists_allowed_targets(self) -> None:
        machine = ApplicationStateMachine(initial_state=ApplicationState.BUSY)
        with self.assertRaises(IllegalStateTransitionError) as caught:
            machine.transition(ApplicationState.UPDATING)
        self.assertEqual(caught.exception.rejection.allowed, ("ready", "shutting_down"))

    def test_assert_state_rejection_has_no_target(self) -> None:
        machine = ApplicationStateMachine()
        with self.assertRaises(IllegalStateTransitionError) as caught:
            machine.assert_state(ApplicationState.READY)
        rejection = caught.exception.rejection
        self.assertEqual(rejection.source, "starting")
        self.assertIsNone(rejection.target)
        self.assertEqual(rejection.allowed, ("ready",))

    def test_rejection_error_is_state_transition_error(self) -> None:
        machine = ApplicationStateMachine(initial_state=ApplicationState.SHUTDOWN)
        with self.assertRaises(StateTransitionError):
            machine.transition(ApplicationState.READY)


class LifecycleTransitionTableTests(unittest.TestCase):
    def test_table_is_complete_and_readonly(self) -> None:
        table = lifecycle_transition_table()
        self.assertEqual(set(table), set(LifecycleState))
        with self.assertRaises(TypeError):
            table[LifecycleState.NEW] = frozenset()  # type: ignore[index]

    def test_new_to_running(self) -> None:
        manager = LifecycleManager()
        manager.start()
        self.assertIs(manager.state, LifecycleState.RUNNING)

    def test_running_to_stopped(self) -> None:
        manager = LifecycleManager()
        manager.start()
        manager.shutdown()
        self.assertIs(manager.state, LifecycleState.STOPPED)

    def test_stopped_to_running(self) -> None:
        manager = LifecycleManager()
        manager.start()
        manager.shutdown()
        manager.start()
        self.assertIs(manager.state, LifecycleState.RUNNING)

    def test_new_to_failed(self) -> None:
        manager = LifecycleManager()
        manager.register_module("boom", self._raise, lambda: None)
        with self.assertRaises(RuntimeError):
            manager.start()
        self.assertIs(manager.state, LifecycleState.FAILED)

    def test_failed_to_running_via_recover(self) -> None:
        manager = LifecycleManager()
        calls = {"count": 0}

        def flaky() -> None:
            calls["count"] += 1
            if calls["count"] == 1:
                raise RuntimeError("first start fails")

        manager.register_module("flaky", flaky, lambda: None)
        with self.assertRaises(RuntimeError):
            manager.start()
        manager.recover()
        self.assertIs(manager.state, LifecycleState.RUNNING)

    def test_failed_to_failed_on_repeated_failure(self) -> None:
        manager = LifecycleManager()
        manager.register_module("boom", self._raise, lambda: None)
        with self.assertRaises(RuntimeError):
            manager.start()
        with self.assertRaises(RuntimeError):
            manager.recover()
        self.assertIs(manager.state, LifecycleState.FAILED)

    def test_stopped_to_failed(self) -> None:
        manager = LifecycleManager()
        manager.start()
        manager.shutdown()
        manager.register_module("boom", self._raise, lambda: None)
        with self.assertRaises(RuntimeError):
            manager.start()
        self.assertIs(manager.state, LifecycleState.FAILED)

    def test_idempotent_start_and_shutdown_are_not_transitions(self) -> None:
        manager = LifecycleManager()
        manager.start()
        manager.start()
        self.assertIs(manager.state, LifecycleState.RUNNING)
        manager.shutdown()
        manager.shutdown()
        self.assertIs(manager.state, LifecycleState.STOPPED)

    @staticmethod
    def _raise() -> None:
        raise RuntimeError("boom")


if __name__ == "__main__":
    unittest.main()
