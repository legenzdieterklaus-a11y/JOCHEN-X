"""Plugin trust validation for the Security Foundation.

:class:`PluginSecurity` decides whether a plugin may be admitted. It maintains a
trust ledger keyed by plugin identifier and enforces an explicit-approval policy:
a plugin is only allowed once it has been verified or trusted, and a rejected
plugin can never be silently admitted. It integrates directly with the existing
:class:`plugins.loader.PluginManifest` so discovery output can be validated
without re-parsing manifests.

:class:`IntegrityPolicy` defines the configuration-driven integrity validation
model (ADR-005). The policy determines what evidence is required to establish
integrity and what minimum trust threshold a plugin must achieve.

:class:`IntegrityResult` records the outcome of integrity validation for a single
plugin: the trust level assigned, the signature status determined, and the
admission decision.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import StrEnum
from threading import RLock

from plugins.loader import PluginManifest
from sdk.manifest import SignatureStatus

from app.events import EventPublisher
from app.security.events import PluginRejected, PluginVerified
from app.security.exceptions import PluginSecurityError
from app.security.models import PluginTrustLevel

_LOGGER_NAME = "jochen_x.security.plugins"
_ALLOWED_TRUST = frozenset({PluginTrustLevel.VERIFIED, PluginTrustLevel.TRUSTED})


class IntegrityEvidenceLevel(StrEnum):
    """Required evidence level for integrity validation (ADR-005 D2)."""

    STRUCTURAL = "structural"
    CONTENT = "content"
    SIGNATURE = "signature"


@dataclass(frozen=True, slots=True)
class IntegrityPolicy:
    """Configuration-driven integrity policy (ADR-005 D2).

    Attributes:
        evidence_level: The category of evidence required for admission.
        scope: What aspects of a plugin are validated ("manifest", "content", "both").
        minimum_trust: The minimum trust level required for admission.
    """

    evidence_level: IntegrityEvidenceLevel = IntegrityEvidenceLevel.STRUCTURAL
    scope: str = "manifest"
    minimum_trust: PluginTrustLevel = PluginTrustLevel.VERIFIED

    @classmethod
    def from_config(cls, config: dict[str, object]) -> IntegrityPolicy:
        """Construct a policy from a configuration mapping.

        Unknown keys are ignored. Missing keys use safe defaults.
        """
        evidence_raw = config.get("evidence_level", IntegrityEvidenceLevel.STRUCTURAL.value)
        try:
            evidence = IntegrityEvidenceLevel(str(evidence_raw))
        except ValueError:
            evidence = IntegrityEvidenceLevel.STRUCTURAL

        scope = str(config.get("scope", "manifest"))
        if scope not in ("manifest", "content", "both"):
            scope = "manifest"

        trust_raw = config.get("minimum_trust", PluginTrustLevel.VERIFIED.value)
        try:
            minimum_trust = PluginTrustLevel(str(trust_raw))
        except ValueError:
            minimum_trust = PluginTrustLevel.VERIFIED

        return cls(evidence_level=evidence, scope=scope, minimum_trust=minimum_trust)


@dataclass(frozen=True, slots=True)
class IntegrityResult:
    """Immutable outcome of integrity validation for a single plugin (ADR-005 D3/D4).

    Attributes:
        identifier: Identifier of the evaluated plugin.
        version: Version string of the evaluated plugin.
        trust: The trust level determined by integrity validation.
        signature_status: The integrity classification assigned.
        admitted: Whether the plugin passed integrity validation.
        reason: Human-readable reason when rejected; empty when admitted.
    """

    identifier: str
    version: str
    trust: PluginTrustLevel
    signature_status: SignatureStatus
    admitted: bool
    reason: str = ""


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


@dataclass(frozen=True, slots=True)
class PermissionPolicy:
    """Configuration-driven permission policy (ADR-006 D5).

    Determines which capabilities the host grants to each plugin.
    Default-deny: an empty policy grants nothing (ADR-006 D1).

    Attributes:
        wildcard_grants: Baseline capability set granted to all plugins.
        plugin_grants: Per-plugin grants mapping identifiers to capability sets.
    """

    wildcard_grants: frozenset[str] = field(default_factory=frozenset)
    plugin_grants: dict[str, frozenset[str]] = field(default_factory=dict)

    @classmethod
    def from_config(cls, config: dict[str, object]) -> PermissionPolicy:
        """Construct a policy from a configuration mapping.

        Unknown keys are ignored. Missing keys produce a default-deny policy.
        """
        wildcard_raw = config.get("wildcard", ())
        wildcard: frozenset[str]
        if isinstance(wildcard_raw, (list, tuple)):
            wildcard = frozenset(str(c) for c in wildcard_raw)
        else:
            wildcard = frozenset()

        grants_raw = config.get("grants", {})
        plugin_grants: dict[str, frozenset[str]] = {}
        if isinstance(grants_raw, dict):
            for pid, perms in grants_raw.items():
                if isinstance(perms, (list, tuple)):
                    plugin_grants[str(pid)] = frozenset(str(p) for p in perms)

        return cls(wildcard_grants=wildcard, plugin_grants=plugin_grants)

    def granted_for(self, plugin_id: str) -> frozenset[str]:
        """Return the set of capabilities granted to a specific plugin."""
        specific = self.plugin_grants.get(plugin_id, frozenset())
        return specific | self.wildcard_grants


@dataclass(frozen=True, slots=True)
class PermissionResult:
    """Immutable outcome of permission validation for a single plugin (ADR-006 D3).

    Attributes:
        identifier: Identifier of the evaluated plugin.
        granted: Capabilities granted by the host policy.
        denied: Capabilities declared but denied by the host policy.
        admitted: Whether the plugin passed permission validation.
        reason: Human-readable reason when rejected; empty when admitted.
    """

    identifier: str
    granted: frozenset[str]
    denied: frozenset[str]
    admitted: bool
    reason: str = ""


class PluginSecurity:
    """Thread-safe plugin trust ledger and validator."""

    def __init__(
        self,
        events: EventPublisher,
        *,
        logger: logging.Logger | None = None,
        integrity_policy: IntegrityPolicy | None = None,
        permission_policy: PermissionPolicy | None = None,
    ) -> None:
        """Create an empty plugin trust ledger.

        Args:
            events: Publisher port used to broadcast plugin verdicts.
            logger: Optional logger for diagnostics.
            integrity_policy: Integrity policy for validation. Defaults to
                structural validation when not provided.
            permission_policy: Permission policy for validation. Defaults to
                default-deny when not provided (ADR-006 D1).
        """
        self._events = events
        self._logger = logger or logging.getLogger(_LOGGER_NAME)
        self._trust: dict[str, PluginTrustLevel] = {}
        self._integrity_results: dict[str, IntegrityResult] = {}
        self._permission_results: dict[str, PermissionResult] = {}
        self._integrity_policy = integrity_policy or IntegrityPolicy()
        self._permission_policy = permission_policy or PermissionPolicy()
        self._lock = RLock()

    @property
    def integrity_policy(self) -> IntegrityPolicy:
        """Return the active integrity policy."""
        return self._integrity_policy

    @property
    def permission_policy(self) -> PermissionPolicy:
        """Return the active permission policy."""
        return self._permission_policy

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

    def integrity_result(self, identifier: str) -> IntegrityResult | None:
        """Return the integrity validation result for ``identifier``, if any."""
        with self._lock:
            return self._integrity_results.get(identifier)

    def validate_integrity(self, manifest: PluginManifest) -> IntegrityResult:
        """Evaluate integrity evidence for a manifest against the active policy.

        Integrity validation occurs at the security verification boundary —
        after discovery, before permission authorization (ADR-005 D5). Each
        plugin is evaluated exactly once per application run (Invariant 6).

        The structural evidence level validates manifest well-formedness:
        required fields present and non-empty. Stronger evidence levels
        (content, signature) are deferred — the architecture supports them
        but the current implementation evaluates structural evidence only.

        Args:
            manifest: A manifest produced by :class:`plugins.loader.PluginLoader`.

        Returns:
            The :class:`IntegrityResult` for the manifest's plugin.
        """
        identifier = manifest.identifier
        version = str(manifest.version)
        policy = self._integrity_policy

        existing = self.trust_level(identifier)
        if existing is PluginTrustLevel.REJECTED:
            result = IntegrityResult(
                identifier=identifier,
                version=version,
                trust=PluginTrustLevel.REJECTED,
                signature_status=SignatureStatus.REJECTED,
                admitted=False,
                reason="explicitly rejected",
            )
            self._record_integrity(result)
            self._logger.info(
                "security.integrity.rejected",
                extra={"context": {
                    "identifier": identifier,
                    "reason": "explicitly rejected",
                    "policy": policy.evidence_level.value,
                }},
            )
            return result

        if existing is PluginTrustLevel.TRUSTED:
            result = IntegrityResult(
                identifier=identifier,
                version=version,
                trust=PluginTrustLevel.TRUSTED,
                signature_status=SignatureStatus.TRUSTED,
                admitted=True,
            )
            self._record_integrity(result)
            PluginVerified(
                identifier, version, PluginTrustLevel.TRUSTED.value
            ).publish(self._events)
            self._logger.info(
                "security.integrity.verified",
                extra={"context": {
                    "identifier": identifier,
                    "trust": PluginTrustLevel.TRUSTED.value,
                    "policy": policy.evidence_level.value,
                }},
            )
            return result

        structural_ok = self._evaluate_structural_evidence(manifest)

        if not structural_ok:
            self._set_trust(identifier, PluginTrustLevel.REJECTED)
            result = IntegrityResult(
                identifier=identifier,
                version=version,
                trust=PluginTrustLevel.REJECTED,
                signature_status=SignatureStatus.REJECTED,
                admitted=False,
                reason="structural validation failed: manifest incomplete",
            )
            self._record_integrity(result)
            PluginRejected(identifier, result.reason).publish(self._events)
            self._logger.info(
                "security.integrity.rejected",
                extra={"context": {
                    "identifier": identifier,
                    "reason": result.reason,
                    "policy": policy.evidence_level.value,
                }},
            )
            return result

        determined_trust = (
            PluginTrustLevel.VERIFIED
            if existing is PluginTrustLevel.UNTRUSTED
            else existing
        )
        self._set_trust(identifier, determined_trust)

        admitted = determined_trust in _ALLOWED_TRUST
        sig_status = (
            SignatureStatus.VERIFIED
            if determined_trust is PluginTrustLevel.VERIFIED
            else SignatureStatus.TRUSTED
            if determined_trust is PluginTrustLevel.TRUSTED
            else SignatureStatus.UNVERIFIED
        )

        result = IntegrityResult(
            identifier=identifier,
            version=version,
            trust=determined_trust,
            signature_status=sig_status,
            admitted=admitted,
        )
        self._record_integrity(result)

        if admitted:
            PluginVerified(identifier, version, determined_trust.value).publish(self._events)
            self._logger.info(
                "security.integrity.verified",
                extra={"context": {
                    "identifier": identifier,
                    "trust": determined_trust.value,
                    "policy": policy.evidence_level.value,
                }},
            )
        else:
            self._logger.info(
                "security.integrity.evidence_missing",
                extra={"context": {
                    "identifier": identifier,
                    "trust": determined_trust.value,
                    "policy": policy.evidence_level.value,
                }},
            )

        return result

    def validate_permissions(
        self,
        manifest: PluginManifest,
        policy: PermissionPolicy | None = None,
    ) -> PermissionResult:
        """Evaluate declared permissions against the host's permission policy.

        Permission validation occurs at the admission boundary — after integrity
        validation, before activation (ADR-006 D3). Each declared permission is
        evaluated against the policy. If any declared permission is denied, the
        plugin is rejected entirely (ADR-006 D1).

        Args:
            manifest: A manifest produced by :class:`plugins.loader.PluginLoader`.
            policy: Override policy; defaults to the instance's stored policy.

        Returns:
            The :class:`PermissionResult` for the manifest's plugin.
        """
        identifier = manifest.identifier
        declared = frozenset(manifest.permissions)
        effective_policy = policy or self._permission_policy

        if not declared:
            result = PermissionResult(
                identifier=identifier,
                granted=frozenset(),
                denied=frozenset(),
                admitted=True,
            )
            with self._lock:
                self._permission_results[identifier] = result
            return result

        policy_grants = effective_policy.granted_for(identifier)
        granted = declared & policy_grants
        denied = declared - policy_grants

        if denied:
            reason = (
                f"Permission denied: {', '.join(sorted(denied))} "
                f"not granted by host policy"
            )
            self._logger.warning(
                "security.permission.denied",
                extra={"context": {
                    "identifier": identifier,
                    "denied": sorted(denied),
                    "granted": sorted(granted),
                }},
            )
            PluginRejected(identifier, reason).publish(self._events)
            result = PermissionResult(
                identifier=identifier,
                granted=granted,
                denied=denied,
                admitted=False,
                reason=reason,
            )
            with self._lock:
                self._permission_results[identifier] = result
            return result

        for perm in sorted(granted):
            self._logger.info(
                "security.permission.granted",
                extra={"context": {
                    "identifier": identifier,
                    "permission": perm,
                }},
            )

        result = PermissionResult(
            identifier=identifier,
            granted=granted,
            denied=frozenset(),
            admitted=True,
        )
        with self._lock:
            self._permission_results[identifier] = result
        return result

    def permission_result(self, identifier: str) -> PermissionResult | None:
        """Return the permission validation result for ``identifier``, if any."""
        with self._lock:
            return self._permission_results.get(identifier)

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
        verdict = PluginVerdict(
            identifier=identifier, version=version, trust=trust, allowed=allowed
        )
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

    def _evaluate_structural_evidence(self, manifest: PluginManifest) -> bool:
        """Check manifest well-formedness: required fields present and valid."""
        if not manifest.identifier or not str(manifest.version):
            return False
        if not manifest.required_application_version:
            return False
        return True

    def _record_integrity(self, result: IntegrityResult) -> None:
        """Store an integrity result (immutable for this application run)."""
        with self._lock:
            self._integrity_results[result.identifier] = result

    def _set_trust(self, identifier: str, level: PluginTrustLevel) -> None:
        """Store the trust ``level`` for ``identifier``.

        Raises:
            ValueError: If ``identifier`` is empty.
        """
        if not identifier:
            raise ValueError("Plugin identifier must be a non-empty string")
        with self._lock:
            self._trust[identifier] = level
