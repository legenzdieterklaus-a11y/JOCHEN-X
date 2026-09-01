"""Immutable models shared by the navigation framework."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum

from PySide6.QtWidgets import QWidget

from app.security.models import Permission


class NavigationId(StrEnum):
    """Stable identifiers for built-in navigation destinations."""

    DASHBOARD = "dashboard"
    CHAT = "chat"
    TRADING = "trading"
    AI_STUDIO = "ai_studio"
    MARKETPLACE = "marketplace"
    PLUGINS = "plugins"
    DEVELOPER = "developer"
    ANALYTICS = "analytics"
    SETTINGS = "settings"
    MONITORING = "monitoring"


class NavigationGroup(StrEnum):
    """Stable sidebar groups for built-in destinations."""

    GENERAL = "general"
    WORKSPACE = "workspace"
    PLATFORM = "platform"
    SYSTEM = "system"


class NavigationIcon(StrEnum):
    """Semantic icon names resolved by the presentation layer."""

    DASHBOARD = "dashboard"
    CHAT = "chat"
    TRADING = "trading"
    AI = "ai"
    MARKETPLACE = "marketplace"
    PLUGIN = "plugin"
    DEVELOPER = "developer"
    ANALYTICS = "analytics"
    SETTINGS = "settings"
    MONITORING = "monitoring"


@dataclass(frozen=True, slots=True)
class NavigationItemModel:
    """Describes one navigation destination independently of Qt widgets."""

    identifier: str
    name: str
    description: str
    icon: NavigationIcon
    order: int
    permission: Permission
    group: NavigationGroup
    parent_identifier: str | None = None
    enabled: bool = True

    def __post_init__(self) -> None:
        """Validate stable fields at the registration boundary."""
        if not self.identifier.strip():
            raise ValueError("Navigation identifier must not be empty")
        if not self.name.strip():
            raise ValueError("Navigation name must not be empty")
        if self.order < 0:
            raise ValueError("Navigation order must not be negative")
        if self.parent_identifier == self.identifier:
            raise ValueError("A navigation item cannot be its own parent")


ModuleFactory = Callable[[], QWidget]


@dataclass(frozen=True, slots=True)
class NavigationRegistration:
    """Couples destination metadata to a lazy module factory."""

    item: NavigationItemModel
    factory: ModuleFactory
