"""Lazy developer-center façade. It creates no thread and is disabled by default."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import time
import re
from typing import Iterable

from core.events import EventDelivery
from core.observability import DiagnosticOutcome, HealthStatus, PluginDiagnostic
from core.registry import ServiceDescriptor
from .contracts import (
    EventDiagnostics,
    PluginDiagnostics,
    PluginRuntimeDiagnostics,
    ServiceDiagnostics,
)
from .models import ConfigurationView, DeveloperSummary, LogEntry, PluginStatus

_SECRET = re.compile(r"(secret|token|password|credential|api[_-]?key)\s*[=:]\s*[^\s]+", re.I)
_SECRET_KEY = re.compile(r"secret|token|password|credential|api[_-]?key", re.I)
_LOGGER_FIELD_INDEX = 2


@dataclass(frozen=True, slots=True)
class SummaryRequest:
    """Caller-supplied inputs of a summary; the rest is platform state."""

    version: str
    build: str
    python: str
    os_name: str
    modules: Iterable[str]
    database_status: str
    theme: str
    profile: str


class DeveloperPlatform:
    """Optional diagnostics adapter. Construction and all I/O are explicit."""

    def __init__(
        self,
        *,
        enabled: bool = False,
        events: EventDiagnostics | None = None,
        services: ServiceDiagnostics | None = None,
        plugins: PluginDiagnostics | None = None,
        diagnostics: PluginRuntimeDiagnostics | None = None,
        log_file: Path | None = None,
        started_at: float | None = None,
    ) -> None:
        self.enabled = enabled
        self._events = events
        self._services = services
        self._plugins = plugins
        self._diagnostics = diagnostics
        self._log_file = log_file
        self._started_at = started_at or time()

    def summary(self, request: SummaryRequest) -> DeveloperSummary:
        """Assemble the developer-center overview of the running application.

        Args:
            request: Identity and environment values supplied by the caller;
                uptime, service count, and plugin count are derived from the
                platform's own state.

        Returns:
            The assembled :class:`DeveloperSummary`.

        Raises:
            RuntimeError: If the developer platform is disabled.
        """
        self._require()
        plugins = tuple(self._plugins.discover()) if self._plugins else ()
        return DeveloperSummary(
            request.version,
            request.build,
            request.python,
            request.os_name,
            self._started_at,
            time() - self._started_at,
            tuple(request.modules),
            len(self.services()),
            len(plugins),
            request.database_status,
            request.theme,
            request.profile,
        )

    def events(self, name_filter: str = "") -> tuple[EventDelivery, ...]:
        self._require()
        records = self._events.delivery_history() if self._events else ()
        return tuple(
            record for record in records if name_filter.lower() in record.name.lower()
        )

    def services(self) -> tuple[ServiceDescriptor, ...]:
        self._require()
        return self._services.descriptors() if self._services else ()

    def plugins(self) -> tuple[PluginStatus, ...]:
        self._require()
        activation = self._activation_outcomes()
        return tuple(
            PluginStatus(
                str(item.identifier),
                str(item.version),
                str(item.required_application_version),
                activation.get(str(item.identifier), True),
                "unverified",
                (),
                (),
            )
            for item in (self._plugins.discover() if self._plugins else ())
        )

    def plugin_diagnostics(self) -> tuple[PluginDiagnostic, ...]:
        """Return the consolidated plugin runtime diagnostics (FR-007).

        The diagnostics are read from the injected port, so they are available
        programmatically rather than only through the log (AC-007.2). Without
        a port the platform reports nothing instead of a placeholder.
        """
        self._require()
        return tuple(self._diagnostics.diagnostics()) if self._diagnostics else ()

    def _activation_outcomes(self) -> dict[str, bool]:
        """Map plugin identifier to activation success; empty without the port."""
        outcomes: dict[str, bool] = {}
        for diagnostic in self._diagnostics.diagnostics() if self._diagnostics else ():
            activated = diagnostic.outcome == DiagnosticOutcome.ACTIVATED
            outcomes[diagnostic.plugin_id] = (
                outcomes.get(diagnostic.plugin_id, True) and activated
            )
        return outcomes

    def logs(self, *, query: str = "", level: str = "") -> tuple[LogEntry, ...]:
        self._require()
        if self._log_file is None or not self._log_file.exists():
            return ()
        entries = []
        for line in self._log_file.read_text(encoding="utf-8", errors="replace").splitlines():
            scrubbed = _SECRET.sub("<redacted>", line)
            if query.lower() in scrubbed.lower() and (
                not level or f" {level.upper()} " in scrubbed
            ):
                parts = scrubbed.split(" ", 3)
                entries.append(
                    LogEntry(
                        parts[0] if parts else "",
                        parts[_LOGGER_FIELD_INDEX] if len(parts) > _LOGGER_FIELD_INDEX else "",
                        scrubbed,
                    )
                )
        return tuple(entries)

    def configuration(self, values: dict[str, object]) -> ConfigurationView:
        self._require()
        return ConfigurationView(
            {
                key: "<redacted>" if _SECRET_KEY.search(key) else str(value)
                for key, value in values.items()
            }
        )

    def health(self, checks: Iterable[HealthStatus]) -> tuple[HealthStatus, ...]:
        self._require()
        return tuple(checks)

    def _require(self) -> None:
        if not self.enabled:
            raise RuntimeError("Developer platform is disabled")
