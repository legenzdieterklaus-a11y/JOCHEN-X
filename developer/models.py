"""Immutable, secret-free data models rendered by developer views."""
from dataclasses import dataclass
from typing import Mapping
@dataclass(frozen=True, slots=True)
class DeveloperSummary:
    version: str; build: str; python: str; os_name: str; started_at: float; uptime_seconds: float
    modules: tuple[str,...]; services: int; plugins: int; database_status: str; theme: str; profile: str
@dataclass(frozen=True, slots=True)
class LogEntry:
    timestamp: str; level: str; message: str
@dataclass(frozen=True, slots=True)
class PluginStatus:
    identifier: str; version: str; api_version: str; enabled: bool; signature_status: str; permissions: tuple[str,...]; dependencies: tuple[str,...]
@dataclass(frozen=True, slots=True)
class ConfigurationView:
    values: Mapping[str, str]
