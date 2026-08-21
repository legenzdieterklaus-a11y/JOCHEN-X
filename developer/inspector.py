"""Architecture analysis based solely on diagnostics ports."""

from dataclasses import dataclass

from core.observability import DiagnosticOutcome

from .contracts import PluginRuntimeDiagnostics, ServiceDiagnostics


@dataclass(frozen=True, slots=True)
class ArchitectureReport:
    services: int
    warnings: tuple[str, ...]


class ArchitectureInspector:
    def __init__(
        self,
        services: ServiceDiagnostics,
        *,
        plugins: PluginRuntimeDiagnostics | None = None,
    ) -> None:
        self._services = services
        self._plugins = plugins

    def inspect(self) -> ArchitectureReport:
        descriptors = self._services.descriptors()
        warnings = []
        for descriptor in descriptors:
            if descriptor.lifetime == "scoped" and not descriptor.dependencies:
                warnings.append(f"Scoped service without dependencies: {descriptor.key}")
        for diagnostic in self._plugins.diagnostics() if self._plugins else ():
            if diagnostic.outcome == DiagnosticOutcome.ACTIVATED:
                continue
            warnings.append(
                f"Plugin {diagnostic.outcome} at stage {diagnostic.stage}: "
                f"{diagnostic.plugin_id} ({diagnostic.reason})"
            )
        return ArchitectureReport(len(descriptors), tuple(warnings))
