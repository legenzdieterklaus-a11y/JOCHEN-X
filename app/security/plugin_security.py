"""Plugin trust validation for the Security Foundation.

:class:`PluginSecurity` decides whether a plugin may be admitted. It maintains a
trust ledger keyed by plugin identifier and enforces an explicit-approval policy:
a plugin is only allowed once it has been verified or trusted, and a rejected
plugin can never be silently admitted. It integrates directly with the existing
:class:`plugins.loader.PluginManifest` so discovery output can be validated
without re-parsing manifests.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from threading import RLock

from plugins.loader import PluginManifest

from app.events import EventPublisher
from app.security.events import PluginRejected, PluginVerified
from app.security.exceptions import PluginSecurityError
from app.security.models import PluginTrustLevel

_LOGGER_NAME = "jochen_x.security.plugins"
_ALLOWED_TRUST = frozenset({PluginTrustLevel.VERIFIED, PluginTrustLevel.TRUSTED})


@dataclass(frozen=True, slots=True)
class PluginVerdict:
    """Immutable result of validating a plugin.

    Attributes:
        identifier: Identifier of the evaluated plugin.
        version: Version string of the evaluated plugin.
        trust: The trust level assigned to the plugin.
        allowed: Whether the plugin may be admitted.
    """

    identifier: str
    version: str
    trust: PluginTrustLevel
    allowed: bool


class PluginSecurity:
    """Thread-safe plugin trust ledger and validator."""

    def __init__(self, events: EventPublisher, *, logger: logging.Logger | None = None) -> None:
        """Create an empty plugin trust ledger.

        Args:
            events: Publisher port used to broadcast plugin verdicts.
            logger: Optional logger for diagnostics.
        """
        self._events = events
        self._logger = logger or logging.getLogger(_LOGGER_NAME)
        self._trust: dict[str, PluginTrustLevel] = {}
        self._lock = RLock()

    def approve(self, identifier: str) -> None:
        """Mark ``identifier`` as fully trusted."""
        self._set_trust(identifier, PluginTrustLevel.TRUSTED)
        self._logger.info("plugin.approved", extra={"context": {"identifier": identifier}})

    def mark_verified(self, identifier: str) -> None:
        """Mark ``identifier`` as verified (allowed, pending full trust)."""
        self._set_trust(identifier, PluginTrustLevel.VERIFIED)
        self._logger.info("plugin.marked_verified", extra={"context": {"identifier": identifier}})

    def reject(self, identifier: str, reason: str) -> None:
        """Mark ``identifier`` as rejected and emit a rejection event.

        Args:
            identifier: Identifier of the plugin to reject.
            reason: Human-readable rejection reason.
        """
        self._set_trust(identifier, PluginTrustLevel.REJECTED)
        self._logger.warning(
            "plugin.rejected", extra={"context": {"identifier": identifier, "reason": reason}}
        )
        PluginRejected(identifier, reason).publish(self._events)

    def trust_level(self, identifier: str) -> PluginTrustLevel:
        """Return the current trust level for ``identifier``."""
        with self._lock:
            return self._trust.get(identifier, PluginTrustLevel.UNTRUSTED)

    def verify(self, identifier: str, version: str) -> PluginVerdict:
        """Evaluate whether a plugin may be admitted and emit the verdict.

        Args:
            identifier: Identifier of the plugin being validated.
            version: Version string of the plugin being validated.

        Returns:
            The :class:`PluginVerdict` describing the decision.

        Raises:
            PluginSecurityError: If the plugin has been explicitly rejected.
        """
        trust = self.trust_level(identifier)
        if trust is PluginTrustLevel.REJECTED:
            raise PluginSecurityError(f"Plugin is rejected: {identifier}")
        allowed = trust in _ALLOWED_TRUST
        verdict = PluginVerdict(identifier=identifier, version=version, trust=trust, allowed=allowed)
        if allowed:
            PluginVerified(identifier, version, trust.value).publish(self._events)
        return verdict

    def verify_manifest(self, manifest: PluginManifest) -> PluginVerdict:
        """Validate a discovered plugin manifest.

        Args:
            manifest: A manifest produced by :class:`plugins.loader.PluginLoader`.

        Returns:
            The :class:`PluginVerdict` for the manifest's plugin.
        """
        return self.verify(manifest.identifier, str(manifest.version))

    def _set_trust(self, identifier: str, level: PluginTrustLevel) -> None:
        """Store the trust ``level`` for ``identifier``.

        Raises:
            ValueError: If ``identifier`` is empty.
        """
        if not identifier:
            raise ValueError("Plugin identifier must be a non-empty string")
        with self._lock:
            self._trust[identifier] = level
