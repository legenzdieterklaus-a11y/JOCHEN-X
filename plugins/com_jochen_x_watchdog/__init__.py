"""Process Watchdog plugin — monitors local processes and scheduled tasks."""

from __future__ import annotations

import csv
import platform
import subprocess
import sys
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from sdk.errors import PluginConfigurationError, PluginLifecycleError, PluginPermissionError
from sdk.manifest import PluginCategory, PluginMetadata, PluginPermission
from sdk.plugin import BackgroundPlugin, PluginLifecycleState

__all__ = ["ProcessEntry", "ProcessStatus", "WatchdogPlugin"]


@dataclass(frozen=True, slots=True)
class ProcessEntry:
    name: str
    pattern: str | None = None
    task: str | None = None


@dataclass(frozen=True, slots=True)
class ProcessStatus:
    entry: ProcessEntry
    running: bool
    pid: int | None
    last_seen: str | None
    last_checked: str
    status: str = "unknown"
    process_signal: str | None = None
    task_signal: str | None = None
    last_task_result: int | None = None


class WatchdogPlugin(BackgroundPlugin):

    def __init__(self) -> None:
        super().__init__()
        self._statuses: dict[str, ProcessStatus] = {}
        self._status_map: dict[str, str] = {}
        self._lock = threading.Lock()
        self._ambiguity_state: dict[str, tuple[int, datetime]] = {}

    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            identifier="com_jochen_x_watchdog",
            name="Process Watchdog",
            version="1.0.0",
            api_version="1.0.0",
            author="JOCHEN X",
            description="Monitors local processes and reports when expected processes are not running.",
            category=PluginCategory.BACKGROUND,
            permissions=frozenset({
                PluginPermission.EVENTS_PUBLISH,
                PluginPermission.CONFIGURATION,
                PluginPermission.SYSTEM_OBSERVATION,
            }),
            minimum_application_version="0.9.0",
            entry_point="watchdog",
        )

    def on_initialize(self) -> None:
        cfg = self.context.config
        cfg.register_default("processes", [])
        cfg.register_default("check_interval_seconds", 30)
        cfg.register_default("report_recovery", True)
        cfg.register_validator("processes", _validate_processes)
        cfg.register_validator("check_interval_seconds", _validate_interval)
        cfg.register_default("host_id", platform.node())
        cfg.register_validator("report_recovery", _validate_bool)
        cfg.load()
        self.context.logger.info("watchdog.initialized")

    def on_start(self) -> None:
        entries = self._read_entries()
        if not entries:
            self.context.logger.warning("watchdog.empty_process_list")
        now = _now_iso()
        result, fallback_reason = _enumerate_processes()
        if fallback_reason is not None:
            self.context.logger.warning(
                "watchdog.enumeration_fallback", reason=fallback_reason,
            )
        with self._lock:
            for entry in entries:
                merged, pid, proc_sig, task_sig, task_result = self._evaluate_entry(
                    entry, result,
                )
                is_up = merged == "running"
                self._statuses[entry.name] = ProcessStatus(
                    entry=entry,
                    running=is_up,
                    pid=pid,
                    last_seen=now if is_up else None,
                    last_checked=now,
                    status=merged,
                    process_signal=proc_sig,
                    task_signal=task_sig,
                    last_task_result=task_result,
                )
                self._status_map[entry.name] = merged
                if merged == "unobservable":
                    self.context.logger.warning(
                        "watchdog.unobservable",
                        subject=entry.name,
                        previous="unknown",
                    )
                self._publish_state_changed(entry.name, merged, "unknown", now)
        self.context.logger.info("watchdog.started")
        super().on_start()

    def run_background(self, stop_event: threading.Event) -> None:
        interval = self.context.config.get("check_interval_seconds")
        while not stop_event.is_set():
            stop_event.wait(interval)
            if stop_event.is_set():
                break
            self._check_cycle()

    def on_stop(self) -> None:
        super().on_stop()
        with self._lock:
            self._statuses.clear()
            self._status_map.clear()
            self._ambiguity_state.clear()
        self.context.logger.info("watchdog.stopped")

    def on_shutdown(self) -> None:
        pass

    def current_status(self) -> tuple[ProcessStatus, ...]:
        if self.state != PluginLifecycleState.STARTED:
            raise PluginLifecycleError("current_status() requires STARTED state")
        with self._lock:
            return tuple(self._statuses.values())

    def _read_entries(self) -> list[ProcessEntry]:
        raw = self.context.config.get("processes")
        return [
            ProcessEntry(
                name=item["name"],
                pattern=item.get("pattern"),
                task=item.get("task"),
            )
            for item in raw
        ]

    def _evaluate_entry(
        self,
        entry: ProcessEntry,
        processes: list[tuple[int, str, str]],
        process_available: bool = True,
    ) -> tuple[str, int | None, str | None, str | None, int | None]:
        proc_signal: str | None = None
        task_signal: str | None = None
        pid: int | None = None
        task_result: int | None = None

        if entry.pattern is not None:
            if process_available:
                is_up, pid = self._resolve_match(entry, processes)
                proc_signal = "running" if is_up else "missing"
            elif entry.task is None:
                return "unknown", None, None, None, None
            else:
                proc_signal = "unobservable"

        if entry.task is not None:
            task_signal, task_result = _query_task(entry.task)

        merged = _merge_signals(task_signal, proc_signal)
        return merged, pid, proc_signal, task_signal, task_result

    def _check_cycle(self) -> None:
        now = _now_iso()
        processes: list[tuple[int, str, str]] = []
        process_available = True

        try:
            result, fallback_reason = _enumerate_processes()
            processes = result
        except Exception:
            self.context.logger.error("watchdog.enumeration_failed")
            process_available = False
            fallback_reason = None

        if fallback_reason is not None:
            self.context.logger.warning(
                "watchdog.enumeration_fallback", reason=fallback_reason,
            )

        entries = self._read_entries()

        with self._lock:
            for entry in entries:
                merged, pid, proc_sig, task_sig, task_result = self._evaluate_entry(
                    entry, processes, process_available,
                )
                was = self._statuses.get(entry.name)
                is_up = merged == "running"
                last_seen = now if is_up else (was.last_seen if was else None)

                self._statuses[entry.name] = ProcessStatus(
                    entry=entry,
                    running=is_up,
                    pid=pid,
                    last_seen=last_seen,
                    last_checked=now,
                    status=merged,
                    process_signal=proc_sig,
                    task_signal=task_sig,
                    last_task_result=task_result,
                )

                previous = self._status_map.get(entry.name, "unknown")
                if merged != previous:
                    self._status_map[entry.name] = merged
                    if merged == "unobservable":
                        self.context.logger.warning(
                            "watchdog.unobservable",
                            subject=entry.name,
                            previous=previous,
                        )
                    self._publish_state_changed(entry.name, merged, previous, now)

    def _resolve_match(
        self, entry: ProcessEntry, processes: list[tuple[int, str, str]],
    ) -> tuple[bool, int | None]:
        matches = _find_process(processes, entry.pattern)
        if len(matches) > 1:
            if self._should_warn_ambiguity(entry.pattern, len(matches)):
                pid_list = ", ".join(f"{p} {n}" for p, n in matches)
                self.context.logger.warning(
                    "watchdog.pattern_ambiguous",
                    pattern=entry.pattern,
                    matches=len(matches),
                    details=f"[{pid_list}]",
                )
                self._ambiguity_state[entry.pattern] = (
                    len(matches), datetime.now(timezone.utc),
                )
            return True, min(m[0] for m in matches)
        if matches:
            self._ambiguity_state.pop(entry.pattern, None)
            return True, matches[0][0]
        self._ambiguity_state.pop(entry.pattern, None)
        return False, None

    def _should_warn_ambiguity(self, pattern: str, match_count: int) -> bool:
        state = self._ambiguity_state.get(pattern)
        if state is None:
            return True
        last_count, last_time = state
        if match_count != last_count:
            return True
        elapsed = datetime.now(timezone.utc) - last_time
        return elapsed.total_seconds() >= 3600

    def _publish_state_changed(
        self, subject: str, status: str, previous: str, timestamp: str,
    ) -> None:
        host_id = self.context.config.get("host_id")
        self._try_publish("monitoring.state_changed", {
            "host_id": host_id,
            "subject": subject,
            "status": status,
            "previous": previous,
            "timestamp": timestamp,
        })

    def _try_publish(self, name: str, payload: dict[str, Any]) -> None:
        try:
            self.context.events.publish(name, payload)
        except PluginPermissionError:
            self.context.logger.error("watchdog.publish_denied", event=name)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _validate_processes(value: Any) -> None:
    if not isinstance(value, list):
        raise PluginConfigurationError("processes must be a list")
    for item in value:
        if not isinstance(item, dict):
            raise PluginConfigurationError("each process entry must be a dict")
        if "name" not in item:
            raise PluginConfigurationError("each process entry must have 'name'")
        if not isinstance(item["name"], str) or not item["name"]:
            raise PluginConfigurationError("process 'name' must be a non-empty string")
        has_pattern = "pattern" in item
        has_task = "task" in item
        if not has_pattern and not has_task:
            raise PluginConfigurationError(
                "each process entry must have 'pattern', 'task', or both",
            )
        if has_pattern:
            if not isinstance(item["pattern"], str) or not item["pattern"]:
                raise PluginConfigurationError("process 'pattern' must be a non-empty string")
        if has_task:
            if not isinstance(item["task"], str) or not item["task"]:
                raise PluginConfigurationError("process 'task' must be a non-empty string")


def _validate_interval(value: Any) -> None:
    if not isinstance(value, int) or value <= 0:
        raise PluginConfigurationError("check_interval_seconds must be a positive integer")


def _validate_bool(value: Any) -> None:
    if not isinstance(value, bool):
        raise PluginConfigurationError("report_recovery must be a bool")


_MERGE_TABLE: dict[tuple[str, str], str] = {
    ("running", "running"): "running",
    ("running", "unobservable"): "running",
    ("running", "missing"): "problem",
    ("missing", "running"): "problem",
    ("missing", "missing"): "missing",
    ("missing", "unobservable"): "missing",
    ("unobservable", "running"): "running",
    ("unobservable", "missing"): "missing",
    ("unobservable", "unobservable"): "unobservable",
}


def _merge_signals(task: str | None, process: str | None) -> str:
    if task is None and process is None:
        return "unknown"
    if task is None:
        return process  # type: ignore[return-value]
    if process is None:
        return task
    return _MERGE_TABLE.get((task, process), "unknown")


def _query_task(task_name: str) -> tuple[str, int | None]:
    if sys.platform != "win32":
        return "unobservable", None
    safe_name = task_name.replace("'", "''")
    try:
        proc = subprocess.run(
            [
                "powershell", "-NoProfile", "-Command",
                "$ErrorActionPreference='Stop';"
                f"$t=Get-ScheduledTask -TaskName '{safe_name}';"
                "$i=Get-ScheduledTaskInfo -InputObject $t;"
                'Write-Output "$($t.State),$($i.LastTaskResult)"',
            ],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=2,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return "unobservable", None
    if proc.returncode != 0:
        return "unobservable", None
    line = proc.stdout.strip()
    if not line:
        return "unobservable", None
    parts = line.split(",", 1)
    state = parts[0].strip()
    last_result: int | None = None
    if len(parts) > 1:
        try:
            last_result = int(parts[1].strip())
        except ValueError:
            pass
    if state == "Running":
        return "running", last_result
    if state in ("Ready", "Queued", "Disabled"):
        return "missing", last_result
    return "unobservable", last_result


def _enumerate_processes() -> tuple[list[tuple[int, str, str]], str | None]:
    if sys.platform == "win32":
        return _enumerate_windows()
    return _enumerate_posix(), None


def _enumerate_windows() -> tuple[list[tuple[int, str, str]], str | None]:
    try:
        return _enumerate_windows_cim(), None
    except Exception as exc:
        return _enumerate_windows_tasklist(), type(exc).__name__


def _enumerate_windows_cim() -> list[tuple[int, str, str]]:
    proc = subprocess.run(
        [
            "powershell", "-NoProfile", "-Command",
            "Get-CimInstance Win32_Process"
            " | Select-Object ProcessId,Name,CommandLine"
            " | ConvertTo-Csv -NoTypeInformation",
        ],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=2,
    )
    if proc.returncode != 0:
        raise subprocess.SubprocessError(
            f"powershell exited with code {proc.returncode}",
        )
    entries: list[tuple[int, str, str]] = []
    lines = proc.stdout.splitlines()
    for row in csv.reader(lines[1:]):
        if len(row) < 2:
            continue
        try:
            pid = int(row[0])
        except ValueError:
            continue
        name = row[1]
        cmdline = row[2] if len(row) >= 3 else ""
        entries.append((pid, name, cmdline or ""))
    return entries


def _enumerate_windows_tasklist() -> list[tuple[int, str, str]]:
    proc = subprocess.run(
        ["tasklist", "/FO", "CSV", "/NH"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    entries: list[tuple[int, str, str]] = []
    for row in csv.reader(proc.stdout.splitlines()):
        if len(row) < 2:
            continue
        name = row[0]
        try:
            pid = int(row[1])
        except ValueError:
            continue
        entries.append((pid, name, ""))
    return entries


def _enumerate_posix() -> list[tuple[int, str, str]]:
    proc = subprocess.run(
        ["ps", "-eo", "pid,args"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    entries: list[tuple[int, str, str]] = []
    for line in proc.stdout.splitlines()[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) == 2:
            try:
                pid = int(parts[0])
            except ValueError:
                continue
            args = parts[1]
            first_word = args.split()[0] if args.strip() else ""
            if first_word.startswith("["):
                name = first_word
            else:
                name = first_word.rsplit("/", 1)[-1]
            entries.append((pid, name, args))
    return entries


def _find_process(
    processes: list[tuple[int, str, str]], pattern: str,
) -> list[tuple[int, str]]:
    matches: list[tuple[int, str]] = []
    for pid, name, cmdline in processes:
        if pattern in name or (cmdline and pattern in cmdline):
            matches.append((pid, name))
    return matches
