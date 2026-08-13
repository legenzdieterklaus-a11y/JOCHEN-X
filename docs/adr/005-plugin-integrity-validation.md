# ADR 005: Plugin Integrity Validation

**Status:** APPROVED
**Approval Date:** 2026-07-30
**Governance Status:** Approved Architectural Decision
**Supersedes:** Draft v3

---

## Context

The JOCHEN X plugin system enforces a two-phase lifecycle
([ADR-011](011-sdk-host-integration.md)): manifest-only discovery followed by
SDK-driven activation. Between these phases, `PluginSecurityStage` evaluates
trust for each discovered manifest ([ADR-011](011-sdk-host-integration.md) D3).
The security infrastructure provides a trust ledger (`PluginSecurity`), trust
levels, and a verification entry point — but no architectural decision defines
what *integrity validation* means, what evidence it requires, or what
guarantees it provides.

**The gap:** No architectural decision defines

1. what integrity validation establishes about a plugin,
2. what evidence integrity validation evaluates,
3. what trust states integrity validation produces,
4. how the validation result relates to subsequent lifecycle phases.

Without this decision, `PluginSecurity.verify_manifest()` operates without
defined integrity semantics, `SignatureStatus` remains inert, and the trust
boundary between Foundation and Plugin Space (Architecture Book v2.0 §11.4)
has no formal basis for trust determination.

### Existing Architectural Capabilities

The following capabilities are established by prior ADRs and authoritative
documents:

- The **Trust Ledger** provides thread-safe trust state management and
  security event emission for all discovered plugins
  (Architecture Book v2.0 §11.3, §11.5)
- Four **Trust States** — UNTRUSTED, VERIFIED, TRUSTED, REJECTED — define
  the trust lifecycle of every plugin (`PluginTrustLevel`,
  Architecture Book v2.0 §11.3)
- Four **Signature Status** values — UNVERIFIED, VERIFIED, TRUSTED,
  REJECTED — exist as a data structure in the SDK manifest model for
  recording the integrity validation classification (`SignatureStatus`,
  Spec §5.9 bullet 4)
- The **Security Verification Boundary** runs in `LOAD_PLUGINS` after
  discovery, partitions manifests into admitted and rejected sets, and
  never imports plugin code ([ADR-011](011-sdk-host-integration.md) D3)
- **Verification Results** are returned from the trust ledger; corresponding
  **Security Events** are emitted for each admission or rejection decision
  (Architecture Book v2.0 §11.5)
- **Manifest Discovery** produces an immutable catalog of compatible plugins
  ([ADR-001](001-core-boundaries.md))
- **Permission Authorization** evaluates declared capabilities against host
  policy at the admission boundary
  ([ADR-006](006-plugin-permission-model.md))
- **Dependency Resolution** evaluates structural prerequisites against the
  admitted plugin set ([ADR-007](007-plugin-dependency-resolution.md))
- The Engineering Specification explicitly defers cryptographic enforcement;
  the integrity model must be definable without cryptographic implementation
  (Spec §5.9 Explicit Deferral)

### Terminology

- **Integrity** — The property that a plugin's content has not been altered,
  corrupted, or substituted since it was authored. Integrity validation
  establishes whether the content presented at discovery matches the content
  the author intended.
- **Integrity Policy** — The host-defined specification of what evidence is
  required to establish integrity. The policy determines which aspects of a
  plugin are subject to validation and what evidence level is sufficient
  for admission.
- **Integrity Evidence** — Observable properties of a plugin that the host
  evaluates to determine integrity. Evidence may range from structural
  completeness (manifest well-formedness) to content verification (hash
  match) to provenance attestation (cryptographic signature). Evidence
  categories are properties of the Integrity Policy — they describe *how*
  integrity is established, not the result of that establishment.
- **Trust State** — The architectural trust result assigned to a plugin,
  recorded in the trust ledger via `PluginTrustLevel` (Architecture Book
  v2.0 §11.3). Trust state describes the admission decision.
- **Validation Result** — The outcome of integrity validation for a single
  plugin: the trust level assigned, the signature status determined, and the
  admission decision derived from these. Once produced, the result is
  immutable for the lifetime of that application run.
- **Trust Determination** — The process of mapping integrity evidence to a
  trust level. Trust determination is the core responsibility of integrity
  validation.

**Key distinction: Trust State ≠ Integrity Evidence.** Trust state describes
the architectural trust result — whether a plugin is admitted or rejected.
Integrity evidence describes how that result was obtained — what observable
properties were evaluated and what evidence categories the policy required.
`PluginTrustLevel` records the trust state. `SignatureStatus` records the
integrity validation classification. Evidence categories (structural, hash,
signature) belong to the Integrity Policy.

**Key distinction: Integrity ≠ Authorization.** Integrity validation
establishes whether a plugin is *what it claims to be*. Permission
authorization ([ADR-006](006-plugin-permission-model.md)) establishes what
a plugin is *allowed to do*. These are independent concerns evaluated at
separate boundaries. A plugin with perfect integrity may still be denied
capabilities. A plugin granted all requested capabilities must still have
established integrity first.

---

## Decision

### D1: Purpose of Integrity Validation

**Integrity validation determines whether a plugin is trusted for admission
into the system.**

It answers a single architectural question: *is this plugin what it claims
to be?* This question is evaluated at the security verification boundary
and must be answered before any subsequent lifecycle phase — permission
authorization, dependency resolution, or activation — proceeds.

Integrity validation does not evaluate what a plugin *does* (that is the
responsibility of permission authorization), does not evaluate what a plugin
*needs* (that is the responsibility of dependency resolution), and does not
execute plugin code (that is the responsibility of activation). Integrity
validation evaluates exclusively what a plugin *is*.

**Rationale:** The trust boundary between Foundation and Plugin Space
(Architecture Book v2.0 §11.4) requires a formal gate. Without integrity
validation, the system admits plugins based solely on compatibility (version
match), leaving the trust determination undefined. Every subsequent phase —
permission authorization, dependency resolution, activation — assumes that
the plugin presenting itself is authentic. Integrity validation provides the
basis for that assumption.

### D2: Integrity Policy

**The host defines an integrity policy that specifies what evidence is
required to establish integrity.**

The integrity policy determines:

1. **Scope of validation** — which aspects of a plugin are subject to
   integrity evaluation: manifest content, plugin content, or both.
2. **Required evidence level** — what category of evidence the policy
   requires for integrity admission. The weakest admissible policy requires
   structural validation (manifest well-formedness and required field
   presence), which confirms that the manifest is syntactically and
   semantically complete but does not by itself establish that plugin content
   has not been altered. Stronger policies may require content verification
   (hash-based tamper detection) or provenance attestation (cryptographic
   signature verification). Each stronger evidence category subsumes the
   structural validation guarantee.
3. **Minimum trust threshold** — which trust level a plugin must achieve
   to be admitted.

The integrity policy is configuration-driven: it is read from the
application configuration (TOML profile hierarchy), consistent with the
permission policy source defined in [ADR-006](006-plugin-permission-model.md)
D5.

**Policy evolution:** The integrity policy is designed to be tightened over
time without changing the architectural model. A deployment may begin with
structural validation only — the minimum admissible evidence level,
confirming manifest completeness without cryptographic dependencies — and
later require content verification or provenance attestation as the platform
matures. Future evidence levels are policy evolution: the architectural
model, lifecycle phases, and trust semantics remain unchanged regardless of
the configured evidence level. This satisfies the Engineering Specification's
requirement (§5.9 Explicit Deferral) that the model be definable without
cryptographic enforcement.

**Rationale:** The Engineering Specification (§5.9) requires that the
integrity model be definable without cryptographic enforcement. A
policy-driven approach satisfies this requirement: the architecture defines
the validation framework and trust semantics; the policy determines the
required evidence level for a specific deployment. This separation ensures
that the architectural model does not prescribe a specific validation
technology while still providing formal integrity guarantees proportional
to the configured evidence level.

### D3: Trust Determination

**Integrity validation maps integrity evidence to a trust level using the
existing `PluginTrustLevel` enumeration.**

The trust determination process produces a single, unambiguous trust level
for each discovered plugin:

| Trust Level | Integrity Meaning |
|---|---|
| **UNTRUSTED** | Initial state. The plugin has been discovered but integrity validation has not yet evaluated it. No trust assertion exists. |
| **VERIFIED** | Integrity evidence has been evaluated and satisfies the integrity policy. The plugin's content is consistent with the evidence presented. The plugin is eligible for admission. |
| **TRUSTED** | The plugin has been explicitly approved by the host beyond automated verification. This level represents an administrative trust decision that supplements integrity evidence. |
| **REJECTED** | Integrity evidence has been evaluated and does not satisfy the integrity policy, or the plugin has been explicitly rejected by the host. The plugin is not eligible for admission. |

**Admission threshold:** A plugin must achieve at least the VERIFIED trust
level to be admitted. Plugins at UNTRUSTED or REJECTED are never admitted.
The host may additionally require TRUSTED for specific plugins or
operational contexts, as defined by the integrity policy.

**Trust level transitions during validation:**

Every discovered plugin enters integrity validation at UNTRUSTED. Validation
evaluates the available integrity evidence against the integrity policy and
transitions the plugin to exactly one of: VERIFIED (evidence sufficient),
TRUSTED (administratively approved), or REJECTED (evidence insufficient or
explicit rejection). This transition occurs exactly once per plugin per
application run.

**Clarification:** ADR-005 does not change the existing `PluginTrustLevel`
semantics defined in Architecture Book v2.0 §11.3. The table above describes
how integrity validation interprets these existing trust states — it does not
introduce new semantics or redefine the enumeration. Integrity validation
determines integrity evidence and maps it to a trust level using the existing
trust assignment mechanisms (`PluginSecurity.verify()`, `.approve()`,
`.reject()` — Architecture Book v2.0 §11.5). The trust level assignment
follows the existing architecture; this ADR defines what evidence that
assignment is based on.

**Rationale:** Reusing `PluginTrustLevel` (Architecture Book v2.0 §11.3)
avoids introducing a parallel trust taxonomy. The four existing states map
naturally to integrity semantics: UNTRUSTED is the initial state before
validation, VERIFIED is the outcome of successful automated validation,
TRUSTED accommodates administrative override, and REJECTED is the outcome
of failed validation. The Engineering Specification (§5.9 bullet 2) requires
that trust semantics use this existing enumeration.

### D4: Signature Status

**Integrity validation determines the signature status of each plugin using
the existing `SignatureStatus` enumeration.**

The signature status records the integrity validation classification
assigned to each plugin by the host at the security verification boundary:

| Signature Status | Architectural Meaning |
|---|---|
| **UNVERIFIED** | Integrity validation has not yet evaluated this plugin. This is the initial state assigned by the SDK at manifest creation. No integrity assertion exists. |
| **VERIFIED** | Integrity evidence has been evaluated and satisfies the requirements of the active integrity policy. The plugin's integrity is confirmed to the extent established by the evaluated evidence. |
| **TRUSTED** | The plugin's integrity is asserted by an administrative trust decision, independent of or supplementing automated evidence evaluation. |
| **REJECTED** | Integrity evidence has been evaluated and does not satisfy the requirements of the active integrity policy, or the plugin has been explicitly rejected by the host. The plugin's integrity could not be confirmed. |

**Distinction: SignatureStatus ≠ Integrity Evidence.** SignatureStatus
records the *outcome* of integrity validation — the classification the host
assigns to a plugin. It does not describe the category or strength of
evidence that was evaluated (structural, hash-based, cryptographic). Evidence
categories are properties of the Integrity Policy (D2): the policy determines
what evidence is required; the validation process evaluates available evidence
against the policy; SignatureStatus records the resulting classification. A
VERIFIED status under a policy requiring only structural validation and a
VERIFIED status under a policy requiring cryptographic signatures represent
different evidence strengths but carry the same SignatureStatus classification.
Evidence strength is determined by the Integrity Policy, not encoded in
SignatureStatus.

**Relationship to PluginTrustLevel:** SignatureStatus and PluginTrustLevel
are related but architecturally distinct. PluginTrustLevel (D3) records the
trust state in the trust ledger — the admission decision. SignatureStatus
records the integrity validation classification on the plugin manifest.
Integrity validation determines the SignatureStatus and, together with the
integrity policy, informs the trust level assignment through the existing
trust assignment architecture (Architecture Book v2.0 §11.3, §11.5).

**Rationale:** The Engineering Specification (§5.9 bullet 4) requires that
`SignatureStatus` be used as a data structure for integrity validation. The
existing enumeration (`sdk/manifest.py:67–78`) defines four values:
UNVERIFIED, VERIFIED, TRUSTED, REJECTED. This decision gives each existing
status value a defined architectural meaning within the integrity validation
model, without introducing new values or replacing the existing enumeration.

### D5: Validation Boundary

**Integrity validation occurs at the security verification boundary —
after manifest discovery and before permission authorization.**

```
Discovery → Integrity Validation → Permission Authorization → Dependency Resolution → Activation
```

**Discovery** ([ADR-001](001-core-boundaries.md), ADR-011 D2) answers:
*which compatible plugins exist?* Discovery reads manifests, checks
application version compatibility, and produces a catalog of compatible
manifests. Discovery does not evaluate integrity.

**Integrity Validation** (this ADR) answers: *is this plugin what it
claims to be?* Integrity validation evaluates the available evidence for
each discovered manifest against the integrity policy and produces a trust
determination. Only plugins that achieve sufficient trust are admitted.
Integrity validation does not evaluate permissions or dependencies.

**Permission Authorization** ([ADR-006](006-plugin-permission-model.md))
answers: *what is this plugin authorized to do?* Permission authorization
evaluates declared capabilities against the host's policy. It operates
exclusively on the admitted set — plugins that have already passed integrity
validation. Permission authorization does not re-evaluate integrity.

**Dependency Resolution** ([ADR-007](007-plugin-dependency-resolution.md))
answers: *are this plugin's structural prerequisites satisfied?* Dependency
resolution evaluates the dependency graph formed by admitted, authorized
plugins. It does not re-evaluate integrity or permissions.

**Activation** (ADR-011 D4) answers: *is this plugin operational?*
Activation imports plugin code, constructs the plugin context, and invokes
lifecycle hooks. Activation assumes that integrity, permissions, and
dependencies have already been established.

**Placement within `PluginSecurityStage`:** Integrity validation is the
responsibility of `PluginSecurityStage` ([ADR-011](011-sdk-host-integration.md)
D3), which runs in `LOAD_PLUGINS` after `PluginDiscoveryStage`. This is
consistent with the stage's existing contract: iterate over discovered
manifests, evaluate trust, partition into admitted and rejected sets.
Integrity validation defines *what trust evaluation means* — it gives
architectural semantics to the verification that `PluginSecurityStage`
performs.

**Rationale:** Integrity must be the first trust-relevant evaluation after
discovery. Evaluating permissions before integrity would authorize plugins
whose authenticity has not been established. Evaluating dependencies before
integrity would resolve structural relationships against potentially
tampered plugins. The Architecture Book v2.0 §11.4 establishes a trust
boundary between Foundation and Plugin Space — integrity validation is the
gate at that boundary. No plugin crosses from Plugin Space into the
admitted set without passing through this gate.

### D6: Failure Semantics

**A plugin that fails integrity validation is rejected and never enters the
admitted plugin set.**

Failure semantics:

1. **Rejection is immediate.** A plugin whose integrity evidence does not
   satisfy the integrity policy is rejected at the validation boundary. It
   is not deferred, conditionally admitted, or admitted with restrictions.

2. **Rejection is per-plugin.** One plugin's rejection does not affect the
   integrity validation of other plugins. Each plugin is evaluated
   independently against the integrity policy.

3. **Rejection is recorded.** Every rejection produces a `PluginRejected`
   event (Architecture Book v2.0 §11.5) that includes the plugin identifier,
   the determined signature status, the reason for rejection, and the
   integrity policy that was applied.

4. **Rejected plugins are invisible to subsequent phases.** A rejected
   plugin does not appear in the admitted set consumed by permission
   authorization. It does not appear in the plugin set available for
   dependency resolution. It cannot be activated. From the perspective of
   all phases after integrity validation, a rejected plugin does not exist.

5. **No recovery without restart.** A rejected plugin cannot be re-evaluated
   or re-admitted during the same application run. Recovery requires
   correcting the integrity evidence (e.g., updating a hash, re-signing)
   and restarting the application.

**Rationale:** Integrity validation is a binary gate: a plugin either
establishes sufficient trust or it does not. There is no meaningful
intermediate state. Allowing conditional admission (e.g., "admit with
reduced trust") would propagate ambiguity into permission authorization
and dependency resolution, which both assume that every plugin in their
input set has established integrity. The fail-fast principle — resolve
early, resolve completely, resolve before plugin code executes —
applies here with the same force as in ADR-006 D3 and ADR-007 D5.

### D7: Audit Integration

**All integrity validation decisions are recorded through the host's audit
infrastructure.**

| Event | When |
|---|---|
| `security.integrity.verified` | Integrity validation succeeds; plugin achieves VERIFIED or TRUSTED |
| `security.integrity.rejected` | Integrity validation fails; plugin is REJECTED |
| `security.integrity.evidence_missing` | Plugin carries no integrity evidence; outcome depends on policy |

Each audit entry includes: plugin identifier, plugin version, determined
signature status, determined trust level, integrity policy applied, and
decision timestamp.

**Rationale:** Integrity decisions are security-relevant and must be
auditable. The audit integration follows the same pattern established by
ADR-006 D6 for permission decisions. An operator must be able to determine,
after the fact, why a specific plugin was admitted or rejected, what evidence
was evaluated, and what policy was in effect.

### D8: Separation of Responsibilities

| Phase | Responsibility | Question | Integrity Role |
|---|---|---|---|
| **Discovery** | Identify compatible plugins from manifests | *Which compatible plugins exist?* | None — discovery does not evaluate trust |
| **Integrity Validation** | Determine whether a plugin is what it claims to be | *Is this plugin authentic?* | **Primary** — evaluates evidence, determines trust level |
| **Permission Authorization** | Evaluate declared capabilities against host policy | *What is this plugin authorized to do?* | Consumer — operates only on integrity-admitted plugins |
| **Dependency Resolution** | Evaluate structural prerequisites and determine activation order | *Are this plugin's structural prerequisites satisfied?* | Consumer — operates only on integrity-admitted, authorized plugins |
| **Activation** | Import code, construct context, invoke lifecycle hooks | *Is this plugin operational?* | Beneficiary — assumes integrity has been established; never re-validates |

Each phase:
- Owns exactly one concern
- Consumes the output of the preceding phase
- Does not replicate or bypass the checks of any other phase
- Produces an output that is consumed by the next phase

No phase has visibility into the internal decisions of another. Integrity
validation does not evaluate permissions; permission authorization does
not re-evaluate integrity; dependency resolution does not re-evaluate
integrity or permissions; activation does not re-validate any prior phase.

---

## Architectural Invariants

These properties hold for any implementation of this ADR:

1. **Integrity before authorization.** No plugin undergoes permission
   authorization ([ADR-006](006-plugin-permission-model.md)) without first
   passing integrity validation. The integrity-admitted set is the input
   to permission authorization, never the reverse.

2. **Integrity before resolution.** No plugin participates in dependency
   resolution ([ADR-007](007-plugin-dependency-resolution.md)) without
   first passing integrity validation and permission authorization.
   The admitted set available for dependency resolution contains only
   integrity-validated, permission-authorized plugins.

3. **Integrity before code execution.** No plugin code is imported or
   executed without the plugin having first passed integrity validation.
   The activation phase ([ADR-011](011-sdk-host-integration.md) D4)
   operates exclusively on the set of plugins that have passed integrity
   validation, permission authorization, and dependency resolution.

4. **Immutable validation result.** Once integrity validation determines
   a plugin's trust level and signature status, these values do not change
   for the lifetime of that application run. No runtime event, configuration
   change, or external signal alters a completed validation result.

5. **Deterministic validation.** The validation result for a given plugin
   depends only on the plugin's integrity evidence and the host's integrity
   policy. It does not depend on the validation outcome of other plugins,
   activation order, or runtime state.

6. **Single evaluation.** Integrity validation evaluates each plugin exactly
   once per application run. No subsequent lifecycle phase re-evaluates
   integrity. The validation result is computed at the security verification
   boundary and consumed — without re-derivation — by all subsequent phases.

7. **Complete coverage.** Every plugin that passes discovery is evaluated
   under the active integrity policy. No plugin is exempt from integrity
   evaluation — including first-party and built-in plugins. Even the weakest
   default policy evaluates every discovered plugin; the policy determines
   what evidence is required, not which plugins are subject to evaluation.

---

## Consequences

### Security Verification Boundary

The security verification boundary ([ADR-011](011-sdk-host-integration.md)
D3) gains defined integrity semantics. Its existing contract — iterate over
discovered manifests, evaluate trust, partition into admitted and rejected
sets — is unchanged in structure. This ADR defines *what trust evaluation
means*: evaluating integrity evidence against the integrity policy and
determining a trust level. The verification boundary becomes the
architectural location where integrity validation occurs — the gate at the
trust boundary between Foundation and Plugin Space (Architecture Book v2.0
§11.4).

### Trust State

Each admitted plugin carries a determined trust level and signature status
from integrity validation through its entire lifecycle. These values are the
formal record of the plugin's integrity determination. They are available to
all subsequent phases as read-only context but are never re-evaluated or
modified.

### Integrity Policy as Evolvable Contract

The integrity policy is the single configuration point that determines the
rigor of integrity validation. The architecture supports policy evolution
from structural validation (no external dependencies) through content
verification (hash-based) to provenance attestation (signature-based)
without changing the architectural model, the lifecycle phases, or the
trust semantics. This satisfies the Engineering Specification's requirement
(§5.9 Explicit Deferral) that the model be definable without cryptographic
enforcement.

### What Remains Unchanged

The manifest discovery contract ([ADR-001](001-core-boundaries.md)) is
unchanged — integrity evidence extends plugin content, it does not alter
the discovery mechanism. The permission model
([ADR-006](006-plugin-permission-model.md)) is unchanged — integrity
validation is a separate phase that does not modify or reinterpret
permission decisions. The dependency resolution model
([ADR-007](007-plugin-dependency-resolution.md)) is unchanged — dependency
resolution is a separate phase that consumes the integrity-admitted,
permission-authorized plugin set. Plugin lifecycle states (Architecture
Book v2.0 §10.6) are unchanged.

---

## Out of Scope

| Topic | Rationale |
|---|---|
| **Cryptographic mechanisms** | This ADR defines integrity semantics, not cryptographic implementation. The choice of specific cryptographic mechanisms and key infrastructure is an implementation decision constrained by the integrity policy, not an architectural decision. Cryptographic enforcement is explicitly deferred (Spec §5.9 Explicit Deferral). |
| **Evidence formats** | The storage and transmission format of integrity evidence is an implementation detail. This ADR defines what evidence *means* architecturally, not how it is represented or exchanged. |
| **Key infrastructure** | The infrastructure for key management and trust anchors is a prerequisite for provenance attestation. It is deferred to a future ADR when the integrity policy evolves to require cryptographic evidence (Spec §15, Low Priority). |
| **Plugin Store integration** | A plugin store or marketplace that distributes signed plugins is a product feature that depends on integrity validation but is not defined by it (Spec §15, Low Priority). |
| **Runtime re-validation** | Integrity validation occurs once per application run (Invariant 6). Re-validating integrity at runtime (e.g., detecting tampered plugin files during execution) is a separate architectural concern that would require filesystem monitoring and hot-reload semantics, neither of which is in scope. |
| **Integrity of transitive content** | This ADR defines integrity validation for plugin manifests and plugin content as a unit. Integrity of individual files within a plugin package, or of resources loaded at runtime, is an implementation concern addressed by the resource sandbox (Architecture Book v2.0 §10.4). |

---

## Alternatives Considered

### A: Discovery-Time Integrity Validation

Evaluate integrity during `PluginDiscoveryStage`, combining compatibility
checking and integrity validation into a single phase. Plugins failing
integrity would not appear in the `PluginCatalog`.

**Rejected** because it violates the separation of responsibilities
established by [ADR-011](011-sdk-host-integration.md) D2 and extended by
this ADR. Discovery answers "which compatible plugins exist?" — a question
about identity and compatibility, not about trust. Merging integrity
validation into discovery would require the discovery layer to carry trust
semantics and integrity policy evaluation, responsibilities that belong to
the security verification boundary. The same reasoning that led ADR-006 to
reject discovery-time permission validation (Alternative A) applies here:
each phase owns exactly one concern.

### B: Activation-Time Integrity Validation

Defer integrity validation to `PluginActivationStage`. Evaluate integrity
evidence immediately before importing plugin code.

**Rejected** because it allows untrusted plugins to influence the admission
pipeline. A plugin that has not been integrity-validated would undergo
permission authorization ([ADR-006](006-plugin-permission-model.md)) and
participate in dependency resolution ([ADR-007](007-plugin-dependency-resolution.md))
before its authenticity is established. This inverts the trust model: the
system would compute authorization state and resolve dependency relationships
for plugins whose identity is unverified. Additionally, late validation
violates the fail-fast principle — a tampered plugin would consume
authorization and resolution resources before being detected.

### C: No Formal Integrity Model (Trust the Filesystem)

Rely on the filesystem boundary as the trust anchor. Plugins placed in the
plugin directory are considered trusted by convention. No integrity evidence
is required or evaluated.

**Rejected** because it provides no formal trust determination and no
auditability. The system cannot distinguish between a plugin that was
intentionally installed and one that was accidentally or maliciously placed
in the plugin directory. The trust boundary (Architecture Book v2.0 §11.4)
would have no gate — every discovered plugin would cross from Plugin Space
into the admitted set without any trust evaluation. This eliminates the
architectural basis for the security verification phase and makes the
`PluginTrustLevel` and `SignatureStatus` data structures permanently inert.

### D: Mandatory Cryptographic Validation

Require cryptographic signature verification for all plugins. No plugin
is admitted without a valid, unexpired signature from a recognized authority.

**Rejected** because it contradicts the Engineering Specification's explicit
deferral of cryptographic enforcement (§5.9 Explicit Deferral) and imposes
an external dependency that is not justified at the current platform
maturity. A local desktop assistant with a single-digit plugin count does
not require PKI infrastructure. The policy-driven approach (D2) achieves
the same architectural rigor while allowing the evidence requirements to
evolve with the platform: structural validation today, content verification
when needed, provenance attestation when the ecosystem demands it.

---

## Traceability

| This ADR | Specification Reference |
|---|---|
| D1 (Purpose) | Spec §5.9 bullet 3 (plugins failing integrity rejected before activation) |
| D2 (Integrity Policy) | Spec §5.9 bullet 1 (policy defines what is validated), AC-9 bullet 2 |
| D3 (Trust Determination) | Spec §5.9 bullet 2 (trust semantics use PluginTrustLevel), AC-9 bullet 3 |
| D4 (Signature Status) | Spec §5.9 bullet 4 (SignatureStatus as data structure), AC-9 bullet 5 |
| D5 (Validation Boundary) | Spec §5.9 bullet 3 (rejected before activation), Architecture Book v2.0 §11.4 (trust boundary) |
| D6 (Failure Semantics) | Spec §5.9 bullet 3, AC-9 bullet 4 (plugins failing integrity rejected before activation) |
| D7 (Audit Integration) | Architecture Book v2.0 §11.1 (audit), consistent with ADR-006 D6 |
| D8 (Separation) | Architecture Book v2.0 §7.2 (bootstrap phase separation), ADR-011 D2 |
| Invariants 1–7 | AC-9 bullet 6 (model definable and testable without crypto), AC-9 bullet 7 (semantics match accepted ADR-005) |

**Acceptance Criteria Coverage:** AC-9 requires (1) ADR-005 accepted before
implementation, (2) integrity policy defined, (3) trust semantics use
existing `PluginTrustLevel`, (4) plugins failing integrity rejected before
activation, (5) `SignatureStatus` used as data structure, (6) model definable
and testable without cryptographic enforcement, (7) integrity semantics per
accepted ADR-005. Decisions D1–D4 define the integrity model these criteria
reference. D5–D6 establish the lifecycle position and failure behavior. D7–D8
provide the audit and separation guarantees. The integrity policy (D2)
explicitly supports non-cryptographic evidence levels, satisfying criterion 6.

---

## Cross-References

- [ADR-001](001-core-boundaries.md) — Core boundaries (manifest-only discovery)
- [ADR-004](004-plugin-security-integration.md) — Security integration timing (resolved by ADR-011 D3)
- [ADR-006](006-plugin-permission-model.md) — Plugin permission model (subsequent phase)
- [ADR-007](007-plugin-dependency-resolution.md) — Plugin dependency resolution (subsequent phase)
- [ADR-010](010-plugin-sdk-architecture.md) — SDK architecture
- [ADR-011](011-sdk-host-integration.md) — SDK-Host integration (two-phase lifecycle, PluginSecurityStage)
- Milestone 0.9 Engineering Spec §5.9 — Integrity Validation Integration
- Milestone 0.9 Engineering Spec AC-9 — Integrity Validation Acceptance Criteria
- Architecture Book v2.0 §7.2 — Bootstrap phase separation
- Architecture Book v2.0 §10 — Plugin-System
- Architecture Book v2.0 §11.1 — Permission Model / Zero Trust
- Architecture Book v2.0 §11.3 — PluginSecurity / Trust Ledger
- Architecture Book v2.0 §11.4 — Trust Boundaries
- Architecture Book v2.0 §11.5 — Plugin Security (verification entry point)

---

## Approval Record

**Approval Decision:** APPROVED

**Governance Workflow:**

- ✓ Draft
- ✓ Independent Review
- ✓ Correction Phase
- ✓ Final Verification (PASS)
- ✓ Approval

**Approval Date:** 2026-07-30

**Governance Status:** Approved Architectural Decision

This ADR is part of the permanent JOCHEN X governance baseline.

It is authoritative for all future implementation and architectural decisions concerning Plugin Integrity Validation.
