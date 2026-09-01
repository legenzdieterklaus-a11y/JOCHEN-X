"""Application service and bootstrap integration for navigation metadata."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from threading import RLock
from typing import Protocol

from app.bootstrap import (
    BootstrapContext,
    BootstrapManager,
    DependencyInjectionStage,
    StartupPhase,
    default_stages,
)
from app.security import SecurityBootstrapStage, SecurityManager
from services.monitoring import MonitoringBootstrapStage
from app.security.permission_manager import PermissionManager
from ui.navigation.navigation_models import (
    NavigationItemModel,
    NavigationRegistration,
)
from ui.navigation.navigation_registry import NavigationRegistry


class NavigationServicePort(Protocol):
    """Read-only navigation use-case boundary."""

    def destinations(self, identity_id: str | None = None) -> tuple[NavigationItemModel, ...]:
        """Return destinations visible to an optional authenticated identity."""
        ...

    def resolve(self, identifier: str, identity_id: str | None = None) -> NavigationRegistration:
        """Resolve an accessible destination."""
        ...


class NavigationService:
    """Applies availability and Security Foundation authorization to routes."""

    def __init__(
        self,
        registry: NavigationRegistry,
        permissions: PermissionManager | None = None,
    ) -> None:
        """Create the service from injected collaborators."""
        self._registry = registry
        self._permissions = permissions

    @property
    def registry(self) -> NavigationRegistry:
        """Return the extensible registry owned by this service."""
        return self._registry

    def destinations(self, identity_id: str | None = None) -> tuple[NavigationItemModel, ...]:
        """Return enabled destinations available to ``identity_id``.

        A missing identity represents the current single-user desktop mode and
        keeps prepared modules visible. Once an identity is supplied, the
        Security Foundation permission assignments are authoritative.
        """
        return tuple(
            registration.item
            for registration in self._registry.registrations()
            if registration.item.enabled and self._is_authorized(registration.item, identity_id)
        )

    def resolve(self, identifier: str, identity_id: str | None = None) -> NavigationRegistration:
        """Resolve an enabled and authorized destination.

        Raises:
            LookupError: If the destination is unknown.
            PermissionError: If it is disabled or inaccessible.
        """
        registration = self._registry.get(identifier)
        if not registration.item.enabled:
            raise PermissionError(f"Navigation destination is disabled: {identifier}")
        if not self._is_authorized(registration.item, identity_id):
            raise PermissionError(f"Navigation permission denied: {identifier}")
        return registration

    def _is_authorized(self, item: NavigationItemModel, identity_id: str | None) -> bool:
        """Evaluate access without emitting audit events during menu rendering."""
        if identity_id is None:
            return True
        if self._permissions is None:
            return False
        return item.permission in self._permissions.permissions_of(identity_id)


class NavigationComposition:
    """Per-lifecycle, idempotent composer for built-in module registrations."""

    def __init__(self, registry: NavigationRegistry) -> None:
        """Create a composer for the shared registry."""
        self._registry = registry
        self._composed = False
        self._lock = RLock()

    def compose(self, registrations: Iterable[NavigationRegistration]) -> bool:
        """Register built-ins exactly once for the current application lifecycle."""
        with self._lock:
            if self._composed:
                return False
            resolved = tuple(registrations)
            self._registry.register_many(resolved)
            self._composed = True
            return True


@dataclass(frozen=True, slots=True)
class NavigationBootstrapStage:
    """Register non-widget navigation services into the existing DI registry."""

    name: str = "navigation"
    phase: StartupPhase = StartupPhase.FINALIZE

    def execute(self, context: BootstrapContext) -> None:
        """Compose the navigation registry and service."""
        registry = context.registry
        if registry is None:
            raise RuntimeError("Navigation stage requires the service registry")
        navigation_registry = NavigationRegistry()
        try:
            security = registry.get(SecurityManager)
        except LookupError:
            permissions = None
        else:
            permissions = security.permissions
        service = NavigationService(navigation_registry, permissions)
        composition = NavigationComposition(navigation_registry)
        registry.register(NavigationRegistry, navigation_registry)
        registry.register(NavigationService, service)
        registry.register(NavigationComposition, composition)


def create_desktop_bootstrap_manager() -> BootstrapManager:
    """Compose the existing bootstrap with Security and Navigation stages.

    The original dependency-injection stage is moved to the end so its graph
    validation includes extension services. No bootstrap behavior is replaced.
    """
    stages = default_stages()
    without_di = tuple(stage for stage in stages if not isinstance(stage, DependencyInjectionStage))
    return BootstrapManager(
        stages=(
            *without_di,
            MonitoringBootstrapStage(),
            SecurityBootstrapStage(),
            NavigationBootstrapStage(),
            DependencyInjectionStage(),
        )
    )
