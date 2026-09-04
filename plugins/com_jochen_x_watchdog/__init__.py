"""Process Watchdog plugin — monitors local processes and reports missing ones."""

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
    pattern: str


@dataclass(frozen=True, slots=True)
class ProcessStatus:
    entry: ProcessEntry
    running: bool
    pid: int | None
    last_seen: str | None
    last_checked: str


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
                is_up, pid = self._resolve_match(entry, result)
                self._statuses[entry.name] = ProcessStatus(
                    entry=entry,
                    running=is_up,
                    pid=pid,
                    last_seen=now if is_up else None,
                    last_checked=now,
                )
                status = "running" if is_up else "missing"
                self._status_map[entry.name] = status
                self._publish_state_changed(entry.name, status, "unknown", now)
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
        return [ProcessEntry(name=item["name"], pattern=item["pattern"]) for item in raw]

    def _check_cycle(self) -> None:
        now = _now_iso()
        try:
            result, fallback_reason = _enumerate_processes()
        except Exception:
            self.context.logger.error("watchdog.enumeration_failed")
            with self._lock:
                for name, status in self._statuses.items():
                    self._statuses[name] = ProcessStatus(
                        entry=status.entry,
                        running=False,
                        pid=None,
                        last_seen=status.last_seen,
                        last_checked=now,
                    )
                    previous = self._status_map.get(name, "unknown")
                    if previous != "unknown":
                        self._status_map[name] = "unknown"
                        self._publish_state_changed(name, "unknown", previous, now)
            return

        if fallback_reason is not None:
            self.context.logger.warning(
                "watchdog.enumeration_fallback", reason=fallback_reason,
            )

        entries = self._read_entries()

        with self._lock:
            for entry in entries:
                is_up, pid = self._resolve_match(entry, result)
                was_running = self._statuses.get(entry.name)
                last_seen = now if is_up else (was_running.last_seen if was_running else None)

                self._statuses[entry.name] = ProcessStatus(
                    entry=entry,
                    running=is_up,
                    pid=pid,
                    last_seen=last_seen,
                    last_checked=now,
                )

                new_status = "running" if is_up else "missing"
                previous = self._status_map.get(entry.name, "unknown")
                if new_status != previous:
                    self._status_map[entry.name] = new_status
                    self._publish_state_changed(entry.name, new_status, previous, now)

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
        if "name" not in item or "pattern" not in item:
            raise PluginConfigurationError("each process entry must have 'name' and 'pattern'")
        if not isinstance(item["name"], str) or not item["name"]:
            raise PluginConfigurationError("process 'name' must be a non-empty string")
        if not isinstance(item["pattern"], str) or not item["pattern"]:
            raise PluginConfigurationError("process 'pattern' must be a non-empty string")


def _validate_interval(value: Any) -> None:
    if not isinstance(value, int) or value <= 0:
        raise PluginConfigurationError("check_interval_seconds must be a positive integer")


def _validate_bool(value: Any) -> None:
    if not isinstance(value, bool):
        raise PluginConfigurationError("report_recovery must be a bool")


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
