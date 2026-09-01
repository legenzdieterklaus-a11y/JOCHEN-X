"""Process Watchdog plugin — monitors local processes and reports missing ones."""

from __future__ import annotations

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
        result = _enumerate_processes()
        with self._lock:
            for entry in entries:
                pid = _find_process(result, entry.pattern)
                running = pid is not None
                self._statuses[entry.name] = ProcessStatus(
                    entry=entry,
                    running=running,
                    pid=pid,
                    last_seen=now if running else None,
                    last_checked=now,
                )
                status = "running" if running else "missing"
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
            result = _enumerate_processes()
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

        entries = self._read_entries()

        with self._lock:
            for entry in entries:
                pid = _find_process(result, entry.pattern)
                was_running = self._statuses.get(entry.name)
                is_up = pid is not None
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


def _enumerate_processes() -> list[tuple[int, str]]:
    if sys.platform == "win32":
        return _enumerate_windows()
    return _enumerate_posix()


def _enumerate_windows() -> list[tuple[int, str]]:
    proc = subprocess.run(
        ["tasklist", "/FO", "CSV", "/NH"],
        capture_output=True,
        text=True,
    )
    entries: list[tuple[int, str]] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split('","')
        if len(parts) >= 2:
            name = parts[0].strip('"')
            try:
                pid = int(parts[1].strip('"'))
            except ValueError:
                continue
            entries.append((pid, name))
    return entries


def _enumerate_posix() -> list[tuple[int, str]]:
    proc = subprocess.run(
        ["ps", "-eo", "pid,comm"],
        capture_output=True,
        text=True,
    )
    entries: list[tuple[int, str]] = []
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
            entries.append((pid, parts[1]))
    return entries


def _find_process(processes: list[tuple[int, str]], pattern: str) -> int | None:
    for pid, name in processes:
        if pattern in name:
            return pid
    return None
