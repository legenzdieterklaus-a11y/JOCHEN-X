"""Tests for the Process Watchdog plugin."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

from sdk.errors import PluginConfigurationError

_PLUGIN_DIR = Path(__file__).resolve().parent.parent / "plugins" / "com_jochen_x_watchdog"
_spec = importlib.util.spec_from_file_location(
    "watchdog_plugin", _PLUGIN_DIR / "__init__.py",
)
assert _spec is not None and _spec.loader is not None
_mod = importlib.util.module_from_spec(_spec)
sys.modules["watchdog_plugin"] = _mod
_spec.loader.exec_module(_mod)

ProcessEntry = _mod.ProcessEntry
ProcessStatus = _mod.ProcessStatus
WatchdogPlugin = _mod.WatchdogPlugin
_find_process = _mod._find_process
_validate_processes = _mod._validate_processes
_validate_interval = _mod._validate_interval
_validate_bool = _mod._validate_bool


class TestProcessEntry:
    def test_frozen(self) -> None:
        entry = ProcessEntry(name="nginx", pattern="nginx")
        with pytest.raises(AttributeError):
            entry.name = "other"  # type: ignore[misc]

    def test_fields(self) -> None:
        entry = ProcessEntry(name="nginx", pattern="nginx.exe")
        assert entry.name == "nginx"
        assert entry.pattern == "nginx.exe"


class TestProcessStatus:
    def test_frozen(self) -> None:
        entry = ProcessEntry(name="test", pattern="test")
        status = ProcessStatus(
            entry=entry, running=True, pid=123,
            last_seen="2026-01-01T00:00:00", last_checked="2026-01-01T00:00:00",
        )
        with pytest.raises(AttributeError):
            status.running = False  # type: ignore[misc]


class TestValidators:
    def test_processes_valid(self) -> None:
        _validate_processes([{"name": "nginx", "pattern": "nginx"}])

    def test_processes_empty(self) -> None:
        _validate_processes([])

    def test_processes_not_list(self) -> None:
        with pytest.raises(PluginConfigurationError):
            _validate_processes("not a list")

    def test_processes_item_not_dict(self) -> None:
        with pytest.raises(PluginConfigurationError):
            _validate_processes(["not a dict"])

    def test_processes_missing_name(self) -> None:
        with pytest.raises(PluginConfigurationError):
            _validate_processes([{"pattern": "nginx"}])

    def test_processes_empty_name(self) -> None:
        with pytest.raises(PluginConfigurationError):
            _validate_processes([{"name": "", "pattern": "nginx"}])

    def test_interval_valid(self) -> None:
        _validate_interval(30)

    def test_interval_zero(self) -> None:
        with pytest.raises(PluginConfigurationError):
            _validate_interval(0)

    def test_interval_negative(self) -> None:
        with pytest.raises(PluginConfigurationError):
            _validate_interval(-1)

    def test_interval_not_int(self) -> None:
        with pytest.raises(PluginConfigurationError):
            _validate_interval(1.5)

    def test_bool_valid(self) -> None:
        _validate_bool(True)
        _validate_bool(False)

    def test_bool_not_bool(self) -> None:
        with pytest.raises(PluginConfigurationError):
            _validate_bool("true")


class TestFindProcess:
    def test_found(self) -> None:
        processes = [(100, "nginx"), (200, "python")]
        assert _find_process(processes, "nginx") == 100

    def test_not_found(self) -> None:
        processes = [(100, "nginx")]
        assert _find_process(processes, "apache") is None

    def test_substring_match(self) -> None:
        processes = [(100, "nginx.exe")]
        assert _find_process(processes, "nginx") == 100

    def test_empty_list(self) -> None:
        assert _find_process([], "nginx") is None


class TestWatchdogMetadata:
    def test_metadata(self) -> None:
        plugin = WatchdogPlugin()
        meta = plugin.metadata()
        assert meta.identifier == "com_jochen_x_watchdog"
        assert meta.version == "1.0.0"
        assert meta.category.value == "background"
