"""Unit tests for the AuditLog."""

from __future__ import annotations

import threading

import pytest

from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.observability.audit import AuditLog, _AuditEntry
from jochen_x.core.types.events import (
    RuntimeEvent,
    RuntimeStateChangedEvent,
    SecurityViolationEvent,
)
from jochen_x.core.types.health_status import HealthStatus
from jochen_x.core.types.runtime_state import RuntimeState

EXPECTED_MULTI_COUNT = 5
EXPECTED_DEFAULT_LIMIT = 100
EXPECTED_CUSTOM_LIMIT = 3
EXPECTED_OFFSET_REMAINING = 5
EXPECTED_APPEND_ONLY_COUNT = 5
EXPECTED_AFTER_RECORDS = 10
EXPECTED_CONCURRENT_TOTAL = 500
CONCURRENT_THREADS = 10
EVENTS_PER_THREAD = 50
READER_ITERATIONS = 100
WRITER_COUNT = 100


class TestAuditLogRecord:
    def test_record_single_event(self) -> None:
        audit = AuditLog()
        event = RuntimeEvent(source="test")
        audit.record(event)
        entries = audit.get_entries()
        assert len(entries) == 1
        assert entries[0] is event

    def test_record_multiple_events(self) -> None:
        audit = AuditLog()
        events = [RuntimeEvent(source=f"src_{i}") for i in range(EXPECTED_MULTI_COUNT)]
        for e in events:
            audit.record(e)
        entries = audit.get_entries(limit=10)
        assert len(entries) == EXPECTED_MULTI_COUNT
        for i, entry in enumerate(entries):
            assert entry.source == f"src_{i}"

    def test_record_non_event_raises(self) -> None:
        audit = AuditLog()
        with pytest.raises(InputValidationError, match="RuntimeEvent"):
            audit.record("not an event")  # type: ignore[arg-type]

    def test_record_preserves_event_types(self) -> None:
        audit = AuditLog()
        state_event = RuntimeStateChangedEvent(
            old_state=RuntimeState.CREATED,
            new_state=RuntimeState.BOOTSTRAPPING,
            source="runtime",
        )
        sec_event = SecurityViolationEvent(
            violation_type="unauthorized_access",
            details="test",
            component_name="test",
            source="security",
        )
        audit.record(state_event)
        audit.record(sec_event)

        entries = audit.get_entries(limit=10)
        assert isinstance(entries[0], RuntimeStateChangedEvent)
        assert isinstance(entries[1], SecurityViolationEvent)


class TestAuditLogGetEntries:
    def test_default_limit(self) -> None:
        audit = AuditLog()
        for i in range(150):
            audit.record(RuntimeEvent(source=f"s{i}"))
        entries = audit.get_entries()
        assert len(entries) == EXPECTED_DEFAULT_LIMIT

    def test_custom_limit(self) -> None:
        audit = AuditLog()
        for i in range(10):
            audit.record(RuntimeEvent(source=f"s{i}"))
        entries = audit.get_entries(limit=EXPECTED_CUSTOM_LIMIT)
        assert len(entries) == EXPECTED_CUSTOM_LIMIT

    def test_offset(self) -> None:
        audit = AuditLog()
        for i in range(10):
            audit.record(RuntimeEvent(source=f"s{i}"))
        entries = audit.get_entries(
            offset=EXPECTED_OFFSET_REMAINING, limit=100,
        )
        assert len(entries) == EXPECTED_OFFSET_REMAINING
        assert entries[0].source == "s5"

    def test_offset_beyond_entries(self) -> None:
        audit = AuditLog()
        audit.record(RuntimeEvent(source="s0"))
        entries = audit.get_entries(offset=10)
        assert entries == []

    def test_negative_limit_raises(self) -> None:
        audit = AuditLog()
        with pytest.raises(InputValidationError, match="negative"):
            audit.get_entries(limit=-1)

    def test_negative_offset_raises(self) -> None:
        audit = AuditLog()
        with pytest.raises(InputValidationError, match="negative"):
            audit.get_entries(offset=-1)

    def test_zero_limit_returns_empty(self) -> None:
        audit = AuditLog()
        audit.record(RuntimeEvent(source="s"))
        entries = audit.get_entries(limit=0)
        assert entries == []


class TestAuditLogIntegrity:
    def test_empty_log_is_valid(self) -> None:
        audit = AuditLog()
        assert audit.verify_integrity() is True

    def test_single_entry_is_valid(self) -> None:
        audit = AuditLog()
        audit.record(RuntimeEvent(source="test"))
        assert audit.verify_integrity() is True

    def test_multiple_entries_valid(self) -> None:
        audit = AuditLog()
        for i in range(EXPECTED_DEFAULT_LIMIT):
            audit.record(RuntimeEvent(source=f"s{i}"))
        assert audit.verify_integrity() is True

    def test_tampered_hash_detected(self) -> None:
        audit = AuditLog()
        audit.record(RuntimeEvent(source="a"))
        audit.record(RuntimeEvent(source="b"))
        audit.record(RuntimeEvent(source="c"))
        assert audit.verify_integrity() is True

        audit._entries[1].integrity_hash = "tampered_hash_value"  # noqa: SLF001
        assert audit.verify_integrity() is False

    def test_tampered_event_detected(self) -> None:
        audit = AuditLog()
        event = RuntimeEvent(source="original")
        audit.record(event)
        assert audit.verify_integrity() is True

        replacement = RuntimeEvent(source="replaced")
        audit._entries[0] = _AuditEntry(  # noqa: SLF001
            sequence_number=1,
            event=replacement,
            integrity_hash=audit._entries[0].integrity_hash,  # noqa: SLF001
        )
        assert audit.verify_integrity() is False

    def test_append_only_sequence(self) -> None:
        audit = AuditLog()
        for i in range(EXPECTED_APPEND_ONLY_COUNT):
            audit.record(RuntimeEvent(source=f"s{i}"))
        assert audit.get_entry_count() == EXPECTED_APPEND_ONLY_COUNT
        assert audit.verify_integrity() is True


class TestAuditLogEntryCount:
    def test_empty_count(self) -> None:
        audit = AuditLog()
        assert audit.get_entry_count() == 0

    def test_count_after_records(self) -> None:
        audit = AuditLog()
        for _ in range(EXPECTED_AFTER_RECORDS):
            audit.record(RuntimeEvent(source="s"))
        assert audit.get_entry_count() == EXPECTED_AFTER_RECORDS


class TestAuditLogHealthCheck:
    def test_healthy_when_intact(self) -> None:
        audit = AuditLog()
        audit.record(RuntimeEvent(source="test"))
        assert audit.check_health() == HealthStatus.HEALTHY

    def test_unhealthy_when_tampered(self) -> None:
        audit = AuditLog()
        audit.record(RuntimeEvent(source="test"))
        audit._entries[0].integrity_hash = "bad"  # noqa: SLF001
        assert audit.check_health() == HealthStatus.UNHEALTHY

    def test_component_name(self) -> None:
        audit = AuditLog()
        assert audit.get_component_name() == "AuditLog"


class TestAuditLogThreadSafety:
    def test_concurrent_record(self) -> None:
        audit = AuditLog()
        errors: list[Exception] = []

        def record_events(start: int) -> None:
            try:
                for i in range(EVENTS_PER_THREAD):
                    event = RuntimeEvent(
                        source=f"thread_{start}_event_{i}",
                    )
                    audit.record(event)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=record_events, args=(i,))
            for i in range(CONCURRENT_THREADS)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert audit.get_entry_count() == EXPECTED_CONCURRENT_TOTAL
        assert audit.verify_integrity() is True

    def test_concurrent_record_and_read(self) -> None:
        audit = AuditLog()
        errors: list[Exception] = []

        def writer() -> None:
            try:
                for i in range(WRITER_COUNT):
                    audit.record(RuntimeEvent(source=f"w{i}"))
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        def reader() -> None:
            try:
                for _ in range(READER_ITERATIONS):
                    audit.get_entries(limit=10)
                    audit.verify_integrity()
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=writer),
            threading.Thread(target=reader),
            threading.Thread(target=reader),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
