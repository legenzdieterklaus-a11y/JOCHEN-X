"""Tests for the Process Watchdog plugin."""

from __future__ import annotations

import importlib.util
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

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
_enumerate_windows = _mod._enumerate_windows
_enumerate_windows_cim = _mod._enumerate_windows_cim
_enumerate_windows_tasklist = _mod._enumerate_windows_tasklist
_merge_signals = _mod._merge_signals
_query_task = _mod._query_task


class TestProcessEntry:
    def test_frozen(self) -> None:
        entry = ProcessEntry(name="nginx", pattern="nginx")
        with pytest.raises(AttributeError):
            entry.name = "other"  # type: ignore[misc]

    def test_fields(self) -> None:
        entry = ProcessEntry(name="nginx", pattern="nginx.exe")
        assert entry.name == "nginx"
        assert entry.pattern == "nginx.exe"
        assert entry.task is None

    def test_task_only(self) -> None:
        entry = ProcessEntry(name="bot", task="MyBot")
        assert entry.pattern is None
        assert entry.task == "MyBot"

    def test_both_signals(self) -> None:
        entry = ProcessEntry(name="bot", pattern="bot.py", task="MyBot")
        assert entry.pattern == "bot.py"
        assert entry.task == "MyBot"


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

    def test_processes_missing_name_task_only(self) -> None:
        with pytest.raises(PluginConfigurationError):
            _validate_processes([{"task": "MyTask"}])

    def test_processes_empty_name(self) -> None:
        with pytest.raises(PluginConfigurationError):
            _validate_processes([{"name": "", "pattern": "nginx"}])

    def test_processes_task_only_valid(self) -> None:
        _validate_processes([{"name": "bot", "task": "MyTask"}])

    def test_processes_both_valid(self) -> None:
        _validate_processes([{"name": "bot", "pattern": "bot.py", "task": "MyTask"}])

    def test_processes_neither_pattern_nor_task(self) -> None:
        with pytest.raises(PluginConfigurationError, match="pattern.*task.*both"):
            _validate_processes([{"name": "bot"}])

    def test_processes_empty_task(self) -> None:
        with pytest.raises(PluginConfigurationError):
            _validate_processes([{"name": "bot", "task": ""}])

    def test_processes_task_not_string(self) -> None:
        with pytest.raises(PluginConfigurationError):
            _validate_processes([{"name": "bot", "task": 123}])

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
        processes = [(100, "nginx", ""), (200, "python", "")]
        assert _find_process(processes, "nginx") == [(100, "nginx")]

    def test_not_found(self) -> None:
        processes = [(100, "nginx", "")]
        assert _find_process(processes, "apache") == []

    def test_substring_match(self) -> None:
        processes = [(100, "nginx.exe", "")]
        assert _find_process(processes, "nginx") == [(100, "nginx.exe")]

    def test_empty_list(self) -> None:
        assert _find_process([], "nginx") == []

    # --- §8 Test 1: Treffer über den Dateinamen ---
    def test_match_by_name(self) -> None:
        processes = [
            (100, "explorer.exe", "C:\\Windows\\explorer.exe"),
            (200, "python.exe", "python.exe -m myapp"),
        ]
        result = _find_process(processes, "explorer.exe")
        assert result == [(100, "explorer.exe")]

    # --- §8 Test 2: Treffer über die Kommandozeile ---
    def test_match_by_cmdline(self) -> None:
        processes = [
            (100, "pythonw.exe", "pythonw.exe -m legenz1.collector"),
            (200, "pythonw.exe", "pythonw.exe -m legenz1.dashboard"),
        ]
        result = _find_process(processes, "legenz1.collector")
        assert result == [(100, "pythonw.exe")]

    # --- §8 Test 3: Kein Treffer → missing ---
    def test_no_match_missing(self) -> None:
        processes = [
            (100, "nginx.exe", "nginx.exe -c /etc/nginx.conf"),
            (200, "python.exe", "python.exe server.py"),
        ]
        result = _find_process(processes, "postgres")
        assert result == []

    # --- §8 Test 4: Zwei Treffer → WARNING, Status running, niedrigste PID ---
    def test_two_matches_lowest_pid(self) -> None:
        processes = [
            (8122, "Code.exe", "Code.exe --folder /project"),
            (4711, "pythonw.exe", "pythonw.exe -m legenz1.collector"),
            (9330, "explorer.exe", "explorer.exe /legenz1"),
        ]
        result = _find_process(processes, "legenz1")
        assert len(result) == 2
        pids = [pid for pid, _ in result]
        assert min(pids) == 4711

    # --- §8 Test 5: Leere Kommandozeile → nur Dateiname, kein Fehler ---
    def test_empty_cmdline_name_only(self) -> None:
        processes = [
            (100, "pythonw.exe", ""),
            (200, "nginx.exe", ""),
        ]
        result = _find_process(processes, "pythonw")
        assert result == [(100, "pythonw.exe")]
        result_no = _find_process(processes, "legenz1")
        assert result_no == []

    # --- §8 Test 7: Gemischter Mehrfachtreffer ---
    def test_mixed_match(self) -> None:
        processes = [
            (5000, "legenz1.exe", "legenz1.exe --config test"),
            (3000, "pythonw.exe", "pythonw.exe -m legenz1.dashboard"),
        ]
        result = _find_process(processes, "legenz1")
        assert len(result) == 2
        pids = sorted(pid for pid, _ in result)
        assert pids == [3000, 5000]


class _CapturingLogger:
    def __init__(self) -> None:
        self.entries: list[tuple[str, str, dict[str, object]]] = []

    def warning(self, msg: str, **kwargs: object) -> None:
        self.entries.append(("WARNING", msg, kwargs))

    def info(self, msg: str, **kwargs: object) -> None:
        self.entries.append(("INFO", msg, kwargs))

    def error(self, msg: str, **kwargs: object) -> None:
        self.entries.append(("ERROR", msg, kwargs))


def _make_plugin_with_logger() -> tuple[WatchdogPlugin, _CapturingLogger]:
    plugin = WatchdogPlugin()
    logger = _CapturingLogger()

    class _Ctx:
        pass

    ctx = _Ctx()
    ctx.logger = logger  # type: ignore[attr-defined]
    plugin._context = ctx  # type: ignore[assignment]
    return plugin, logger


class TestAmbiguityWarning:
    """§8 Tests 4, 7, 8 — Mehrdeutigkeit und Geheimnisschutz."""

    # --- §8 Test 4: WARNING bei Mehrdeutigkeit ---
    def test_ambiguity_warning_logged(self) -> None:
        plugin, logger = _make_plugin_with_logger()
        entry = ProcessEntry(name="bot", pattern="legenz1")
        processes: list[tuple[int, str, str]] = [
            (4711, "pythonw.exe", "pythonw.exe -m legenz1.collector"),
            (9330, "explorer.exe", "explorer.exe /legenz1"),
        ]
        is_up, pid = plugin._resolve_match(entry, processes)
        assert is_up is True
        assert pid == 4711
        warnings = [e for e in logger.entries if e[0] == "WARNING"]
        assert len(warnings) == 1
        assert warnings[0][1] == "watchdog.pattern_ambiguous"
        assert warnings[0][2]["pattern"] == "legenz1"
        assert warnings[0][2]["matches"] == 2

    # --- §8 Test 7: Gemischter Mehrfachtreffer — WARNING enthält beide PIDs ---
    def test_mixed_match_warning(self) -> None:
        plugin, logger = _make_plugin_with_logger()
        entry = ProcessEntry(name="bot", pattern="legenz1")
        processes: list[tuple[int, str, str]] = [
            (5000, "legenz1.exe", "legenz1.exe --config test"),
            (3000, "pythonw.exe", "pythonw.exe -m legenz1.dashboard"),
        ]
        is_up, pid = plugin._resolve_match(entry, processes)
        assert is_up is True
        assert pid == 3000
        warnings = [e for e in logger.entries if e[0] == "WARNING"]
        assert len(warnings) == 1
        details = warnings[0][2]["details"]
        assert "5000" in details
        assert "3000" in details
        assert "legenz1.exe" in details
        assert "pythonw.exe" in details

    # --- §8 Test 8: Kein Geheimnis im Protokoll ---
    def test_no_secret_in_log(self) -> None:
        plugin, logger = _make_plugin_with_logger()
        secret_token = "sk-SUPER-SECRET-TOKEN-12345"
        entry = ProcessEntry(name="bot", pattern="legenz1")
        processes: list[tuple[int, str, str]] = [
            (100, "pythonw.exe", f"pythonw.exe -m legenz1.collector --token {secret_token}"),
            (200, "pythonw.exe", f"pythonw.exe -m legenz1.dashboard --key {secret_token}"),
        ]
        plugin._resolve_match(entry, processes)
        for _, _, kwargs in logger.entries:
            for value in kwargs.values():
                assert secret_token not in str(value)

    def test_debounce_suppresses_repeat(self) -> None:
        plugin, logger = _make_plugin_with_logger()
        entry = ProcessEntry(name="bot", pattern="legenz1")
        processes: list[tuple[int, str, str]] = [
            (100, "pythonw.exe", "pythonw.exe -m legenz1.collector"),
            (200, "pythonw.exe", "pythonw.exe -m legenz1.dashboard"),
        ]
        plugin._resolve_match(entry, processes)
        plugin._resolve_match(entry, processes)
        plugin._resolve_match(entry, processes)
        warnings = [e for e in logger.entries if e[1] == "watchdog.pattern_ambiguous"]
        assert len(warnings) == 1

    def test_debounce_warns_on_count_change(self) -> None:
        plugin, logger = _make_plugin_with_logger()
        entry = ProcessEntry(name="bot", pattern="legenz1")
        two_matches: list[tuple[int, str, str]] = [
            (100, "pythonw.exe", "pythonw.exe -m legenz1.collector"),
            (200, "pythonw.exe", "pythonw.exe -m legenz1.dashboard"),
        ]
        three_matches = two_matches + [
            (300, "Code.exe", "Code.exe legenz1/config.toml"),
        ]
        plugin._resolve_match(entry, two_matches)
        plugin._resolve_match(entry, three_matches)
        warnings = [e for e in logger.entries if e[1] == "watchdog.pattern_ambiguous"]
        assert len(warnings) == 2
        assert warnings[0][2]["matches"] == 2
        assert warnings[1][2]["matches"] == 3

    def test_debounce_warns_after_one_hour(self) -> None:
        plugin, logger = _make_plugin_with_logger()
        entry = ProcessEntry(name="bot", pattern="legenz1")
        processes: list[tuple[int, str, str]] = [
            (100, "pythonw.exe", "pythonw.exe -m legenz1.collector"),
            (200, "pythonw.exe", "pythonw.exe -m legenz1.dashboard"),
        ]
        plugin._resolve_match(entry, processes)
        plugin._ambiguity_state["legenz1"] = (
            2, datetime.now(timezone.utc) - timedelta(hours=1, seconds=1),
        )
        plugin._resolve_match(entry, processes)
        warnings = [e for e in logger.entries if e[1] == "watchdog.pattern_ambiguous"]
        assert len(warnings) == 2


class TestFallback:
    """§8 Test 6 — Rückfall auf tasklist."""

    def test_fallback_on_cim_failure(self) -> None:
        with patch.object(
            _mod, "_enumerate_windows_cim",
            side_effect=FileNotFoundError("powershell not found"),
        ):
            entries, reason = _enumerate_windows()
        assert reason is not None
        assert isinstance(entries, list)

    def test_fallback_on_timeout(self) -> None:
        import subprocess as sp

        with patch.object(
            _mod, "_enumerate_windows_cim",
            side_effect=sp.TimeoutExpired(cmd="powershell", timeout=2),
        ):
            entries, reason = _enumerate_windows()
        assert reason == "TimeoutExpired"
        assert isinstance(entries, list)

    def test_fallback_on_bad_returncode(self) -> None:
        with patch.object(
            _mod, "_enumerate_windows_cim",
            side_effect=RuntimeError("bad output"),
        ):
            entries, reason = _enumerate_windows()
        assert reason == "RuntimeError"
        assert isinstance(entries, list)

    def test_fallback_entries_have_empty_cmdline(self) -> None:
        tasklist_output = '"explorer.exe","1234","Console","1","50.000 K"\r\n'
        with patch.object(
            _mod, "_enumerate_windows_cim",
            side_effect=FileNotFoundError,
        ), patch(
            "subprocess.run",
        ) as mock_run:
            mock_run.return_value.stdout = tasklist_output
            mock_run.return_value.returncode = 0
            entries, reason = _enumerate_windows()
        assert reason is not None
        for _, _, cmdline in entries:
            assert cmdline == ""


class TestWatchdogMetadata:
    def test_metadata(self) -> None:
        plugin = WatchdogPlugin()
        meta = plugin.metadata()
        assert meta.identifier == "com_jochen_x_watchdog"
        assert meta.version == "1.0.0"
        assert meta.category.value == "background"


class TestMergeSignals:
    """§5 — Zusammenführung von TASK und PROCESS."""

    def test_both_running(self) -> None:
        assert _merge_signals("running", "running") == "running"

    def test_task_running_process_unobservable(self) -> None:
        assert _merge_signals("running", "unobservable") == "running"

    def test_task_running_process_missing(self) -> None:
        assert _merge_signals("running", "missing") == "problem"

    def test_task_missing_process_running(self) -> None:
        assert _merge_signals("missing", "running") == "problem"

    def test_both_missing(self) -> None:
        assert _merge_signals("missing", "missing") == "missing"

    def test_task_missing_process_unobservable(self) -> None:
        assert _merge_signals("missing", "unobservable") == "missing"

    def test_task_unobservable_process_running(self) -> None:
        assert _merge_signals("unobservable", "running") == "running"

    def test_task_unobservable_process_missing(self) -> None:
        assert _merge_signals("unobservable", "missing") == "missing"

    def test_both_unobservable(self) -> None:
        assert _merge_signals("unobservable", "unobservable") == "unobservable"

    def test_task_only(self) -> None:
        assert _merge_signals("running", None) == "running"
        assert _merge_signals("missing", None) == "missing"

    def test_process_only(self) -> None:
        assert _merge_signals(None, "running") == "running"
        assert _merge_signals(None, "missing") == "missing"

    def test_neither(self) -> None:
        assert _merge_signals(None, None) == "unknown"


class TestQueryTask:
    """§4 — Erhebung der Aufgabe (gemockt)."""

    def test_running_state(self) -> None:
        with patch.object(_mod, "subprocess") as mock_sp:
            mock_sp.run.return_value.returncode = 0
            mock_sp.run.return_value.stdout = "Running,0\n"
            mock_sp.TimeoutExpired = TimeoutError
            signal, result = _query_task("TestTask")
        assert signal == "running"
        assert result == 0

    def test_ready_state(self) -> None:
        with patch.object(_mod, "subprocess") as mock_sp:
            mock_sp.run.return_value.returncode = 0
            mock_sp.run.return_value.stdout = "Ready,267011\n"
            mock_sp.TimeoutExpired = TimeoutError
            signal, result = _query_task("TestTask")
        assert signal == "missing"
        assert result == 267011

    def test_disabled_state(self) -> None:
        with patch.object(_mod, "subprocess") as mock_sp:
            mock_sp.run.return_value.returncode = 0
            mock_sp.run.return_value.stdout = "Disabled,0\n"
            mock_sp.TimeoutExpired = TimeoutError
            signal, result = _query_task("TestTask")
        assert signal == "missing"

    def test_queued_state(self) -> None:
        with patch.object(_mod, "subprocess") as mock_sp:
            mock_sp.run.return_value.returncode = 0
            mock_sp.run.return_value.stdout = "Queued,0\n"
            mock_sp.TimeoutExpired = TimeoutError
            signal, result = _query_task("TestTask")
        assert signal == "missing"

    def test_task_not_found(self) -> None:
        with patch.object(_mod, "subprocess") as mock_sp:
            mock_sp.run.return_value.returncode = 1
            mock_sp.run.return_value.stdout = ""
            mock_sp.TimeoutExpired = TimeoutError
            signal, result = _query_task("NoSuchTask")
        assert signal == "unobservable"
        assert result is None

    def test_query_timeout(self) -> None:
        with patch.object(_mod, "subprocess") as mock_sp:
            mock_sp.run.side_effect = TimeoutError("timeout")
            mock_sp.TimeoutExpired = TimeoutError
            signal, result = _query_task("SlowTask")
        assert signal == "unobservable"
        assert result is None

    def test_query_oserror(self) -> None:
        with patch.object(_mod, "subprocess") as mock_sp:
            mock_sp.run.side_effect = OSError("no powershell")
            mock_sp.TimeoutExpired = TimeoutError
            signal, result = _query_task("AnyTask")
        assert signal == "unobservable"
        assert result is None

    def test_non_windows(self) -> None:
        with patch.object(_mod, "sys") as mock_sys:
            mock_sys.platform = "linux"
            signal, result = _query_task("AnyTask")
        assert signal == "unobservable"
        assert result is None


class TestEvaluateEntry:
    """§8 Tests 1–9 — Auswertung beider Signale."""

    def _make_plugin(self) -> WatchdogPlugin:
        plugin = WatchdogPlugin()
        logger = _CapturingLogger()

        class _Ctx:
            pass

        ctx = _Ctx()
        ctx.logger = logger  # type: ignore[attr-defined]
        plugin._context = ctx  # type: ignore[assignment]
        return plugin

    # --- §8 Test 1: Nur pattern — Verhalten wie bisher ---
    def test_pattern_only_running(self) -> None:
        plugin = self._make_plugin()
        entry = ProcessEntry(name="bot", pattern="bot.py")
        processes: list[tuple[int, str, str]] = [(100, "python.exe", "python bot.py")]
        merged, pid, proc_sig, task_sig, task_result = plugin._evaluate_entry(
            entry, processes,
        )
        assert merged == "running"
        assert pid == 100
        assert proc_sig == "running"
        assert task_sig is None
        assert task_result is None

    def test_pattern_only_missing(self) -> None:
        plugin = self._make_plugin()
        entry = ProcessEntry(name="bot", pattern="bot.py")
        processes: list[tuple[int, str, str]] = [(100, "nginx.exe", "nginx")]
        merged, pid, proc_sig, task_sig, task_result = plugin._evaluate_entry(
            entry, processes,
        )
        assert merged == "missing"
        assert pid is None
        assert proc_sig == "missing"

    # --- §8 Test 2: Nur task, State=Running → running ---
    def test_task_only_running(self) -> None:
        plugin = self._make_plugin()
        entry = ProcessEntry(name="bot", task="MyBot")
        with patch.object(_mod, "_query_task", return_value=("running", 0)):
            merged, pid, proc_sig, task_sig, task_result = plugin._evaluate_entry(
                entry, [],
            )
        assert merged == "running"
        assert pid is None
        assert proc_sig is None
        assert task_sig == "running"
        assert task_result == 0

    # --- §8 Test 3: Nur task, State=Ready → missing ---
    def test_task_only_ready(self) -> None:
        plugin = self._make_plugin()
        entry = ProcessEntry(name="bot", task="MyBot")
        with patch.object(_mod, "_query_task", return_value=("missing", 267011)):
            merged, pid, proc_sig, task_sig, task_result = plugin._evaluate_entry(
                entry, [],
            )
        assert merged == "missing"
        assert task_sig == "missing"
        assert task_result == 267011

    # --- §8 Test 4: Nur task, Aufgabe nicht gefunden → unobservable ---
    def test_task_only_not_found(self) -> None:
        plugin = self._make_plugin()
        entry = ProcessEntry(name="bot", task="NoSuchTask")
        with patch.object(_mod, "_query_task", return_value=("unobservable", None)):
            merged, pid, proc_sig, task_sig, task_result = plugin._evaluate_entry(
                entry, [],
            )
        assert merged == "unobservable"
        assert task_sig == "unobservable"
        assert task_result is None

    # --- §8 Test 5: Nur task, Abfrage schlägt fehl → unobservable ---
    def test_task_only_query_fails(self) -> None:
        plugin = self._make_plugin()
        entry = ProcessEntry(name="bot", task="FailTask")
        with patch.object(_mod, "_query_task", return_value=("unobservable", None)):
            merged, pid, proc_sig, task_sig, task_result = plugin._evaluate_entry(
                entry, [],
            )
        assert merged == "unobservable"

    # --- §8 Test 6: Beide running → running ---
    def test_both_running(self) -> None:
        plugin = self._make_plugin()
        entry = ProcessEntry(name="bot", pattern="bot.py", task="MyBot")
        processes: list[tuple[int, str, str]] = [(100, "python.exe", "python bot.py")]
        with patch.object(_mod, "_query_task", return_value=("running", 0)):
            merged, pid, proc_sig, task_sig, task_result = plugin._evaluate_entry(
                entry, processes,
            )
        assert merged == "running"
        assert pid == 100
        assert proc_sig == "running"
        assert task_sig == "running"

    # --- §8 Test 7: TASK running, PROCESS missing → problem ---
    def test_task_running_process_missing(self) -> None:
        plugin = self._make_plugin()
        entry = ProcessEntry(name="bot", pattern="bot.py", task="MyBot")
        processes: list[tuple[int, str, str]] = [(100, "nginx.exe", "nginx")]
        with patch.object(_mod, "_query_task", return_value=("running", 0)):
            merged, pid, proc_sig, task_sig, task_result = plugin._evaluate_entry(
                entry, processes,
            )
        assert merged == "problem"
        assert proc_sig == "missing"
        assert task_sig == "running"

    # --- §8 Test 8: TASK missing, PROCESS running → problem ---
    def test_task_missing_process_running(self) -> None:
        plugin = self._make_plugin()
        entry = ProcessEntry(name="bot", pattern="bot.py", task="MyBot")
        processes: list[tuple[int, str, str]] = [(100, "python.exe", "python bot.py")]
        with patch.object(_mod, "_query_task", return_value=("missing", 0)):
            merged, pid, proc_sig, task_sig, task_result = plugin._evaluate_entry(
                entry, processes,
            )
        assert merged == "problem"
        assert proc_sig == "running"
        assert task_sig == "missing"

    # --- §8 Test 9: Beide unobservable → unobservable ---
    def test_both_unobservable(self) -> None:
        plugin = self._make_plugin()
        entry = ProcessEntry(name="bot", pattern="bot.py", task="MyBot")
        with patch.object(_mod, "_query_task", return_value=("unobservable", None)):
            merged, pid, proc_sig, task_sig, task_result = plugin._evaluate_entry(
                entry, [], process_available=False,
            )
        assert merged == "unobservable"
        assert proc_sig == "unobservable"
        assert task_sig == "unobservable"


class TestConfigValidationR1:
    """§8 Test 10 — Weder task noch pattern → Konfigurationsfehler."""

    def test_neither_pattern_nor_task_rejected(self) -> None:
        with pytest.raises(PluginConfigurationError, match="pattern.*task.*both"):
            _validate_processes([{"name": "bot"}])

    def test_pattern_only_accepted(self) -> None:
        _validate_processes([{"name": "bot", "pattern": "bot.py"}])

    def test_task_only_accepted(self) -> None:
        _validate_processes([{"name": "bot", "task": "MyBot"}])

    def test_both_accepted(self) -> None:
        _validate_processes([{"name": "bot", "pattern": "bot.py", "task": "MyBot"}])


class TestUnobservableWarning:
    """§8 Test 11 — Wechsel nach unobservable → WARNING."""

    def test_transition_to_unobservable_logs_warning(self) -> None:
        plugin, logger = _make_plugin_with_logger()
        entry = ProcessEntry(name="gustav", task="GustavBot")
        plugin._status_map["gustav"] = "running"
        plugin._statuses["gustav"] = ProcessStatus(
            entry=entry, running=True, pid=None,
            last_seen="2026-01-01T00:00:00", last_checked="2026-01-01T00:00:00",
            status="running", task_signal="running",
        )

        class _FakeEvents:
            def publish(self, name: str, payload: dict[str, object]) -> None:
                pass

        class _FakeConfig:
            def get(self, key: str) -> object:
                if key == "check_interval_seconds":
                    return 30
                if key == "processes":
                    return [{"name": "gustav", "task": "GustavBot"}]
                if key == "host_id":
                    return "test"
                return None

        plugin._context.events = _FakeEvents()  # type: ignore[attr-defined]
        plugin._context.config = _FakeConfig()  # type: ignore[attr-defined]

        with patch.object(_mod, "_query_task", return_value=("unobservable", None)), \
             patch.object(_mod, "_enumerate_processes", return_value=([], None)):
            plugin._check_cycle()

        warnings = [
            e for e in logger.entries
            if e[0] == "WARNING" and e[1] == "watchdog.unobservable"
        ]
        assert len(warnings) == 1
        assert warnings[0][2]["subject"] == "gustav"
        assert warnings[0][2]["previous"] == "running"

    def test_unobservable_to_unobservable_no_warning(self) -> None:
        plugin, logger = _make_plugin_with_logger()
        entry = ProcessEntry(name="gustav", task="GustavBot")
        plugin._status_map["gustav"] = "unobservable"
        plugin._statuses["gustav"] = ProcessStatus(
            entry=entry, running=False, pid=None,
            last_seen=None, last_checked="2026-01-01T00:00:00",
            status="unobservable", task_signal="unobservable",
        )

        class _FakeEvents:
            def publish(self, name: str, payload: dict[str, object]) -> None:
                pass

        class _FakeConfig:
            def get(self, key: str) -> object:
                if key == "processes":
                    return [{"name": "gustav", "task": "GustavBot"}]
                if key == "host_id":
                    return "test"
                return None

        plugin._context.events = _FakeEvents()  # type: ignore[attr-defined]
        plugin._context.config = _FakeConfig()  # type: ignore[attr-defined]

        with patch.object(_mod, "_query_task", return_value=("unobservable", None)), \
             patch.object(_mod, "_enumerate_processes", return_value=([], None)):
            plugin._check_cycle()

        warnings = [
            e for e in logger.entries
            if e[0] == "WARNING" and e[1] == "watchdog.unobservable"
        ]
        assert len(warnings) == 0


class TestProcessStatusR1:
    """ProcessStatus carries new fields."""

    def test_backward_compat(self) -> None:
        entry = ProcessEntry(name="test", pattern="test")
        status = ProcessStatus(
            entry=entry, running=True, pid=123,
            last_seen="2026-01-01T00:00:00", last_checked="2026-01-01T00:00:00",
        )
        assert status.status == "unknown"
        assert status.process_signal is None
        assert status.task_signal is None
        assert status.last_task_result is None

    def test_with_all_fields(self) -> None:
        entry = ProcessEntry(name="bot", pattern="bot.py", task="MyBot")
        status = ProcessStatus(
            entry=entry, running=True, pid=100,
            last_seen="2026-01-01T00:00:00", last_checked="2026-01-01T00:00:00",
            status="running", process_signal="running",
            task_signal="running", last_task_result=0,
        )
        assert status.status == "running"
        assert status.process_signal == "running"
        assert status.task_signal == "running"
        assert status.last_task_result == 0
