"""Policy, capabilities, audit, and secret-provider security boundaries."""

from dataclasses import dataclass
from enum import StrEnum
import logging
from typing import Protocol


class Permission(StrEnum):
    CREDENTIALS = "credentials"
    PLUGIN = "plugin"
    SYSTEM_OBSERVATION = "system_observation"
    NETWORK = "network"
    FILESYSTEM = "filesystem"


class TrustLevel(StrEnum):
    UNTRUSTED = "untrusted"
    RESTRICTED = "restricted"
    TRUSTED = "trusted"


@dataclass(frozen=True, slots=True)
class SecurityContext:
    subject: str
    permissions: frozenset[Permission]
    trust: TrustLevel = TrustLevel.RESTRICTED


@dataclass(frozen=True, slots=True)
class AuditContext:
    subject: str
    action: str
    resource: str


class CapabilityModel:
    def permits(self, context: SecurityContext, permission: Permission) -> bool:
        return permission in context.permissions


class PermissionLayer:
    def __init__(self, granted: frozenset[Permission] = frozenset()) -> None:
        self._granted = granted

    def allows(self, permission: Permission) -> bool:
        return permission in self._granted


@dataclass(frozen=True, slots=True)
class SecurityPolicy:
    permissions: PermissionLayer


class SecretProvider(Protocol):
    def get(self, name: str) -> str | None: ...


class SecretManager:
    def get(self, name: str) -> str | None:
        return None


class AuditHooks:
    def __init__(self, logger: logging.Logger) -> None:
        self._logger = logger

    def record(self, action: str, **context: str) -> None:
        self._logger.info(action, extra={"context": context})
