"""Tests for MonitoringStateCollector — state transition logic."""

import logging
import unittest

from core.events import Event, EventBus
from database.sqlite import MonitoringState, MonitoringStateRepository
from services.monitoring import MonitoringStateCollector


class _InMemoryRepository:
    """Minimal stand-in for MonitoringStateRepository."""

    def __init__(self) -> None:
        self._store: dict[tuple[str, str], MonitoringState] = {}

    def all(self) -> tuple[MonitoringState, ...]:
        return tuple(self._store.values())

    def upsert(self, state: MonitoringState) -> None:
        self._store[(state.host_id, state.subject)] = state


class MonitoringStateCollectorTests(unittest.TestCase):

    def setUp(self) -> None:
        self.events = EventBus()
        self.repo = _InMemoryRepository()
        self.logger = logging.getLogger("test.monitoring")
        self.collector = MonitoringStateCollector(
            self.events, self.repo, self.logger,
        )
        self.collector.start()

    def tearDown(self) -> None:
        self.collector.stop()

    def _publish(self, subject: str, status: str, previous: str, ts: str) -> None:
        self.events.publish(Event("monitoring.state_changed", {
            "host_id": "testhost",
            "subject": subject,
            "status": status,
            "previous": previous,
            "timestamp": ts,
        }))

    def test_first_event_creates_state_with_zero_transitions(self) -> None:
        self._publish("proc_a", "running", "unknown", "T1")
        states = self.collector.states()
        self.assertEqual(len(states), 1)
        self.assertEqual(states[0].status, "running")
        self.assertEqual(states[0].transitions, 0)
        self.assertEqual(states[0].since, "T1")
        self.assertEqual(states[0].first_seen, "T1")

    def test_same_status_does_not_change_since_or_transitions(self) -> None:
        self._publish("proc_a", "running", "unknown", "T1")
        self._publish("proc_a", "running", "running", "T2")
        states = self.collector.states()
        self.assertEqual(len(states), 1)
        self.assertEqual(states[0].transitions, 0)
        self.assertEqual(states[0].since, "T1")

    def test_changed_status_increments_transitions_and_updates_since(self) -> None:
        self._publish("proc_a", "running", "unknown", "T1")
        self._publish("proc_a", "missing", "running", "T2")
        states = self.collector.states()
        self.assertEqual(len(states), 1)
        self.assertEqual(states[0].status, "missing")
        self.assertEqual(states[0].transitions, 1)
        self.assertEqual(states[0].since, "T2")
        self.assertEqual(states[0].first_seen, "T1")

    def test_multiple_transitions_accumulate(self) -> None:
        self._publish("proc_a", "running", "unknown", "T1")
        self._publish("proc_a", "missing", "running", "T2")
        self._publish("proc_a", "running", "missing", "T3")
        states = self.collector.states()
        self.assertEqual(states[0].transitions, 2)
        self.assertEqual(states[0].since, "T3")
        self.assertEqual(states[0].status, "running")

    def test_restart_with_persisted_state_same_status_no_increment(self) -> None:
        self.repo.upsert(MonitoringState(
            host_id="testhost", subject="proc_a", status="running",
            first_seen="T0", last_seen="T0", since="T0", transitions=0,
        ))
        collector2 = MonitoringStateCollector(
            self.events, self.repo, self.logger,
        )
        collector2.start()
        self.events.publish(Event("monitoring.state_changed", {
            "host_id": "testhost",
            "subject": "proc_a",
            "status": "running",
            "previous": "unknown",
            "timestamp": "T5",
        }))
        states = collector2.states()
        self.assertEqual(len(states), 1)
        self.assertEqual(states[0].transitions, 0)
        self.assertEqual(states[0].since, "T0")
        self.assertEqual(states[0].first_seen, "T0")
        collector2.stop()

    def test_restart_with_persisted_state_changed_status_increments(self) -> None:
        self.repo.upsert(MonitoringState(
            host_id="testhost", subject="proc_a", status="running",
            first_seen="T0", last_seen="T0", since="T0", transitions=0,
        ))
        collector2 = MonitoringStateCollector(
            self.events, self.repo, self.logger,
        )
        collector2.start()
        self.events.publish(Event("monitoring.state_changed", {
            "host_id": "testhost",
            "subject": "proc_a",
            "status": "missing",
            "previous": "unknown",
            "timestamp": "T5",
        }))
        states = collector2.states()
        self.assertEqual(len(states), 1)
        self.assertEqual(states[0].status, "missing")
        self.assertEqual(states[0].transitions, 1)
        self.assertEqual(states[0].since, "T5")
        self.assertEqual(states[0].first_seen, "T0")
        collector2.stop()

    def test_first_event_running_is_logged(self) -> None:
        with self.assertLogs(self.logger, level="INFO") as cm:
            self._publish("proc_a", "running", "unknown", "T1")
        self.assertTrue(any("monitoring.state_changed" in m for m in cm.output))

    def test_first_event_missing_is_logged(self) -> None:
        with self.assertLogs(self.logger, level="INFO") as cm:
            self._publish("proc_a", "missing", "unknown", "T1")
        self.assertTrue(any("monitoring.state_changed" in m for m in cm.output))

    def test_same_status_not_persisted_to_repository(self) -> None:
        self._publish("proc_a", "running", "unknown", "T1")
        self.assertEqual(len(self.repo.all()), 1)
        self._publish("proc_a", "running", "running", "T2")
        state = self.repo.all()[0]
        self.assertEqual(state.since, "T1")
        self.assertEqual(state.transitions, 0)


if __name__ == "__main__":
    unittest.main()
