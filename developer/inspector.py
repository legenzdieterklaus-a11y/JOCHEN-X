"""Architecture analysis based solely on diagnostics ports."""

from dataclasses import dataclass

from .contracts import ServiceDiagnostics


@dataclass(frozen=True, slots=True)
class ArchitectureReport:
    services: int
    warnings: tuple[str, ...]


class ArchitectureInspector:
    def __init__(self, services: ServiceDiagnostics) -> None:
        self._services = services

    def inspect(self) -> ArchitectureReport:
        descriptors = self._services.descriptors()
        warnings = []
        for descriptor in descriptors:
            if descriptor.lifetime == "scoped" and not descriptor.dependencies:
                warnings.append(f"Scoped service without dependencies: {descriptor.key}")
        return ArchitectureReport(len(descriptors), tuple(warnings))
