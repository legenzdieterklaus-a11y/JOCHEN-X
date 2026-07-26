"""Unit tests for the StructuredLogger."""

from __future__ import annotations

import json
import logging
import threading
import time
from pathlib import Path

import pytest

from jochen_x.core.exceptions.security import InputValidationError
from jochen_x.core.observability.logging import StructuredLogger, _JsonFormatter
from jochen_x.core.types.health_status import HealthStatus
from jochen_x.core.types.severity import LogSeverity

ASYNC_SETTLE_TIME = 0.2
SHORT_SETTLE_TIME = 0.1
LONG_SETTLE_TIME = 0.3
FILE_SETTLE_TIME = 0.3
CONCURRENT_SETTLE_TIME = 0.5
MESSAGES_PER_THREAD = 50
CONCURRENT_THREADS = 5
EXPECTED_CONCURRENT_TOTAL = 250


class _CaptureHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.records: list[logging.LogRecord] = []
        self.formatted: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)
        self.formatted.append(self.format(record))


class TestStructuredLoggerInit:
    def test_default_init(self) -> None:
        logger = StructuredLogger()
        assert logger.get_level("any") == LogSeverity.INFO

    def test_custom_default_level(self) -> None:
        logger = StructuredLogger(default_level=LogSeverity.DEBUG)
        assert logger.get_level("any") == LogSeverity.DEBUG


class TestStructuredLoggerLevels:
    def test_set_and_get_level(self) -> None:
        logger = StructuredLogger()
        logger.set_level("comp1", LogSeverity.ERROR)
        assert logger.get_level("comp1") == LogSeverity.ERROR

    def test_unset_component_uses_default(self) -> None:
        logger = StructuredLogger(default_level=LogSeverity.WARNING)
        assert logger.get_level("unknown") == LogSeverity.WARNING

    def test_set_level_empty_component_raises(self) -> None:
        logger = StructuredLogger()
        with pytest.raises(InputValidationError, match="empty"):
            logger.set_level("", LogSeverity.DEBUG)

    def test_set_level_invalid_severity_raises(self) -> None:
        logger = StructuredLogger()
        with pytest.raises(InputValidationError, match="LogSeverity"):
            logger.set_level("comp", "DEBUG")  # type: ignore[arg-type]


class TestStructuredLoggerLog:
    def test_log_entry_format(self) -> None:
        logger = StructuredLogger(default_level=LogSeverity.DEBUG)
        handler = _CaptureHandler()
        handler.setFormatter(_JsonFormatter())
        logger._handlers.append(handler)  # noqa: SLF001
        logger.start()
        try:
            logger.log(
                LogSeverity.INFO,
                "test message",
                component="TestComp",
                correlation_id="test-cid-123",
            )
            time.sleep(ASYNC_SETTLE_TIME)
        finally:
            logger.stop()

        assert len(handler.formatted) >= 1
        entry = json.loads(handler.formatted[0])
        assert entry["severity"] == "INFO"
        assert entry["message"] == "test message"
        assert entry["component"] == "TestComp"
        assert entry["correlation_id"] == "test-cid-123"
        assert "timestamp" in entry

    def test_log_below_level_is_filtered(self) -> None:
        logger = StructuredLogger(default_level=LogSeverity.WARNING)
        handler = _CaptureHandler()
        logger._handlers.append(handler)  # noqa: SLF001
        logger.start()
        try:
            logger.log(LogSeverity.DEBUG, "should not appear")
            logger.log(LogSeverity.INFO, "should not appear")
            time.sleep(SHORT_SETTLE_TIME)
        finally:
            logger.stop()

        assert len(handler.records) == 0

    def test_component_level_filtering(self) -> None:
        logger = StructuredLogger(default_level=LogSeverity.DEBUG)
        logger.set_level("quiet", LogSeverity.ERROR)
        handler = _CaptureHandler()
        logger._handlers.append(handler)  # noqa: SLF001
        logger.start()
        try:
            logger.log(
                LogSeverity.WARNING, "filtered", component="quiet",
            )
            logger.log(
                LogSeverity.ERROR, "passes", component="quiet",
            )
            time.sleep(ASYNC_SETTLE_TIME)
        finally:
            logger.stop()

        assert len(handler.records) == 1
        assert handler.records[0].getMessage() == "passes"

    def test_invalid_severity_raises(self) -> None:
        logger = StructuredLogger()
        with pytest.raises(InputValidationError, match="LogSeverity"):
            logger.log("INVALID", "msg")  # type: ignore[arg-type]

    def test_auto_correlation_id(self) -> None:
        logger = StructuredLogger(default_level=LogSeverity.DEBUG)
        handler = _CaptureHandler()
        handler.setFormatter(_JsonFormatter())
        logger._handlers.append(handler)  # noqa: SLF001
        logger.start()
        try:
            logger.log(LogSeverity.INFO, "auto cid")
            time.sleep(ASYNC_SETTLE_TIME)
        finally:
            logger.stop()

        assert len(handler.formatted) >= 1
        entry = json.loads(handler.formatted[0])
        assert entry["correlation_id"] != ""


class TestStructuredLoggerConvenienceMethods:
    def _make_logger(self) -> tuple[StructuredLogger, _CaptureHandler]:
        logger = StructuredLogger(default_level=LogSeverity.DEBUG)
        handler = _CaptureHandler()
        logger._handlers.append(handler)  # noqa: SLF001
        return logger, handler

    def test_debug(self) -> None:
        logger, handler = self._make_logger()
        logger.start()
        try:
            logger.debug("dbg msg", component="c")
            time.sleep(SHORT_SETTLE_TIME)
        finally:
            logger.stop()
        assert len(handler.records) == 1
        assert handler.records[0].levelno == logging.DEBUG

    def test_info(self) -> None:
        logger, handler = self._make_logger()
        logger.start()
        try:
            logger.info("info msg")
            time.sleep(SHORT_SETTLE_TIME)
        finally:
            logger.stop()
        assert len(handler.records) == 1

    def test_warning(self) -> None:
        logger, handler = self._make_logger()
        logger.start()
        try:
            logger.warning("warn msg")
            time.sleep(SHORT_SETTLE_TIME)
        finally:
            logger.stop()
        assert len(handler.records) == 1

    def test_error(self) -> None:
        logger, handler = self._make_logger()
        logger.start()
        try:
            logger.error("err msg")
            time.sleep(SHORT_SETTLE_TIME)
        finally:
            logger.stop()
        assert len(handler.records) == 1

    def test_critical(self) -> None:
        logger, handler = self._make_logger()
        logger.start()
        try:
            logger.critical("crit msg")
            time.sleep(SHORT_SETTLE_TIME)
        finally:
            logger.stop()
        assert len(handler.records) == 1


class TestStructuredLoggerLifecycle:
    def test_start_stop(self) -> None:
        logger = StructuredLogger()
        logger.initialize()
        logger.start()
        logger.stop()

    def test_double_start_is_idempotent(self) -> None:
        logger = StructuredLogger()
        logger.start()
        logger.start()
        logger.stop()

    def test_double_stop_is_idempotent(self) -> None:
        logger = StructuredLogger()
        logger.start()
        logger.stop()
        logger.stop()


class TestStructuredLoggerFileOutput:
    def test_configure_file_output(self, tmp_path: Path) -> None:
        log_file = tmp_path / "test.log"
        logger = StructuredLogger(default_level=LogSeverity.DEBUG)
        logger.configure_file_output(log_file)
        logger.start()
        try:
            logger.info("file test", component="FileTest")
            time.sleep(FILE_SETTLE_TIME)
        finally:
            logger.stop()

        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "file test" in content
        entry = json.loads(content.strip().split("\n")[0])
        assert entry["component"] == "FileTest"

    def test_file_output_invalid_max_bytes(
        self, tmp_path: Path,
    ) -> None:
        logger = StructuredLogger()
        with pytest.raises(InputValidationError, match="at least 1"):
            logger.configure_file_output(
                tmp_path / "x.log", max_bytes=0,
            )

    def test_file_output_invalid_backup_count(
        self, tmp_path: Path,
    ) -> None:
        logger = StructuredLogger()
        with pytest.raises(InputValidationError, match="at least 1"):
            logger.configure_file_output(
                tmp_path / "x.log", backup_count=0,
            )


class TestStructuredLoggerHealthCheck:
    def test_health_when_started(self) -> None:
        logger = StructuredLogger()
        logger.start()
        try:
            assert logger.check_health() == HealthStatus.HEALTHY
        finally:
            logger.stop()

    def test_health_when_stopped(self) -> None:
        logger = StructuredLogger()
        assert logger.check_health() == HealthStatus.DEGRADED

    def test_component_name(self) -> None:
        logger = StructuredLogger()
        assert logger.get_component_name() == "StructuredLogger"


class TestStructuredLoggerThreadSafety:
    def test_concurrent_logging(self) -> None:
        logger = StructuredLogger(default_level=LogSeverity.DEBUG)
        handler = _CaptureHandler()
        logger._handlers.append(handler)  # noqa: SLF001
        logger.start()
        errors: list[Exception] = []

        def log_many(idx: int) -> None:
            try:
                for i in range(MESSAGES_PER_THREAD):
                    msg = f"msg-{idx}-{i}"
                    logger.info(
                        msg,
                        component=f"thread-{idx}",
                    )
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=log_many, args=(i,))
            for i in range(CONCURRENT_THREADS)
        ]
        try:
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            time.sleep(CONCURRENT_SETTLE_TIME)
        finally:
            logger.stop()

        assert not errors
        assert len(handler.records) == EXPECTED_CONCURRENT_TOTAL
