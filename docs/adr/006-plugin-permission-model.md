# ADR 006: Plugin Permission Model

**Status:** APPROVED  
**Approval Date:** 2026-07-29

**Supersedes:** Draft v1 (Open), Draft v2 (Review Completed)

---

## Context

The JOCHEN X plugin system enforces a two-phase lifecycle
([ADR-011](011-sdk-host-integration.md)): manifest-only discovery followed by
SDK-driven activation. The SDK defines a permission model with typed
capability identifiers and permission-gated API facades. The host-side
security infrastructure (permission management, audit logging) exists but
is not connected to the plugin admission or runtime enforcement boundary.

**The gap:** No architectural decision defines

1. what a permission declaration in the manifest *means*,
2. how the host decides which declarations to grant or deny,
3. what happens at runtime when a plugin uses an undeclared capability.

Without this decision, plugin permissions remain inert, the manifest cannot
carry meaningful permission declarations, and the permission model integration
(Spec §5.4, AC-4) cannot proceed.

### Existing Infrastructure

The following capabilities are established by prior ADRs and the SDK:

- A typed permission enum with 10 capability identifiers (SDK)
- Plugin metadata carrying a declared permission set (SDK)
- Permission-gated API facades for events and services (SDK, [ADR-010](010-plugin-sdk-architecture.md))
- A permission check injection point in the plugin context ([ADR-008](008-plugin-context-definition.md))
- Host-side permission management and audit logging (Security layer)
- Two-phase admission and activation stages ([ADR-011](011-sdk-host-integration.md))

### Terminology

- **Declaration** — A plugin listing a `PluginPermission` in its manifest.
  A declaration expresses *intent*: "this plugin needs capability X."
- **Authorization** — The host granting or denying a declared permission
  based on policy. A declaration is necessary but not sufficient for access.
- **Enforcement** — The runtime check that verifies a granted permission
  before allowing an API call.

**Key distinction: Manifest = Intent ≠ Authorization.** A plugin declaring
`events.publish` does not mean the host must grant it. The host evaluates
each declaration against its policy and produces an explicit grant or denial.

---

## Decision

### D1: Default-Deny Policy

**All plugin capabilities are denied unless explicitly granted by the host.**

A plugin with no permission declarations receives no capabilities. A plugin
with declarations receives only those capabilities the host's policy
explicitly grants. There is no implicit grant, no "allow-by-default" mode,
and no bypass for built-in or first-party plugins.

**Rationale:** Default-deny is the only policy compatible with the zero-trust
principle established in the Architecture Book v2.0 §11.1. The alternative —
default-allow with explicit denials — inverts the security model and makes
every new capability automatically available to every plugin.

### D2: Three-State Permission Resolution

Each `PluginPermission` declared by a plugin resolves to exactly one of three
states at admission time:

| State | Meaning | Runtime Effect |
|---|---|---|
| **Granted** | Host policy allows this capability | API calls gated by this permission succeed |
| **Denied** | Host policy rejects this capability | API calls gated by this permission raise `PluginPermissionError` |
| **Undeclared** | Plugin did not declare the capability | API calls gated by this permission raise `PluginPermissionError` |

**Denied and Undeclared produce the same runtime behavior** (access refused),
but they are semantically distinct:

- **Denied** means the plugin asked and the host said no. This is a policy
  decision, logged as `security.permission.denied`.
- **Undeclared** means the plugin never asked. This is a programming error
  in the plugin, logged as `plugin.permission.undeclared`.

The distinction enables precise diagnostics: an operator seeing "denied" knows
their policy blocked a legitimate request; a developer seeing "undeclared"
knows their manifest is incomplete.

### D3: Admission-Time Validation

The host validates permissions at the admission boundary — after manifest
discovery and before plugin activation:

1. Read the plugin's declared permissions from its metadata.
2. Evaluate each declaration against the host's permission policy.
3. Partition into a granted set and a denied set.
4. If any declared permission is denied, reject the plugin entirely.
5. Propagate the granted set to the activation boundary.

A rejected plugin is never activated. One plugin's rejection does not affect
the admission of other plugins.

**Milestone 0.9 assumption: all declared permissions are required.** This ADR
treats every declared permission as essential to the plugin's function. A
plugin is either admitted with its full declared set or rejected entirely.
This assumption keeps the initial model simple and deterministic. It is not
a permanent platform restriction — a future ADR may introduce an optional
permission concept (e.g., graceful degradation for non-critical capabilities)
without changing the core authorization semantics defined here.

### D4: Runtime Enforcement

At activation, the host binds each plugin's granted permission set to its
API boundary. Every permission-gated API call is checked against the
granted set at invocation time:

- A call requiring a granted permission succeeds.
- A call requiring a non-granted permission is refused with a diagnostic
  that distinguishes "denied by policy" from "not declared in manifest."

The enforcement mechanism is the existing permission check injection point
defined by the SDK ([ADR-010](010-plugin-sdk-architecture.md)). This ADR
does not introduce a new enforcement mechanism — it connects the existing
one to the host's admission decision.

### D5: Permission Policy Source

The host's permission policy is configuration-driven: a mapping from plugin
identifiers to sets of granted permissions, read from the application
configuration (TOML profile hierarchy).

A plugin not listed in the policy receives no grants (default-deny).
A wildcard entry may grant a baseline set to all plugins.

The policy source is deliberately simple. This ADR does not define:
- Interactive prompting ("Plugin X requests network access — allow?")
- Per-invocation consent
- Permission escalation or revocation at runtime

These may be introduced in future ADRs without changing the core model.

### D6: Audit Integration

All permission decisions are recorded through the host's audit infrastructure:

| Event | When |
|---|---|
| `security.permission.granted` | Admission grants a declared permission |
| `security.permission.denied` | Admission denies a declared permission |
| `plugin.permission.undeclared` | Runtime enforcement blocks an undeclared access |

Each audit entry includes: plugin identifier, permission identifier,
decision timestamp, and policy source.

---

## Consequences

### Admission Boundary

The admission boundary gains a new responsibility: permission validation.
A plugin's declared permissions are evaluated against the host's policy
before activation. This extends the existing admission contract
([ADR-011](011-sdk-host-integration.md) D3) without replacing it — security
verification and permission validation are complementary admission checks.

### Authorization State

Each admitted plugin carries an immutable granted permission set from
admission through its entire activation lifetime. This set is the single
source of truth for what the plugin is authorized to do. The authorization
state is deterministic: the same declaration and policy always produce the
same granted set.

### Runtime Semantics

Every permission-gated API call is subject to enforcement. The runtime
distinguishes three cases (Granted, Denied, Undeclared) as defined in D2.
No API facade may bypass enforcement. The enforcement contract and injection
point are unchanged from the SDK's existing design ([ADR-010](010-plugin-sdk-architecture.md)).

### Host Responsibilities

The host assumes three new responsibilities:

1. **Policy ownership** — The host provides and evaluates the permission
   policy (D5). The policy source is configuration-driven and evolvable.
2. **Grant computation** — The host computes the granted set at admission
   and propagates it to the activation boundary (D3).
3. **Audit emission** — The host records all permission decisions through
   the audit infrastructure (D6).

### What Remains Unchanged

The SDK's permission model (capability identifiers, metadata schema,
permission check contract, API facades) is unchanged. The manifest discovery
contract ([ADR-001](001-core-boundaries.md)) is unchanged — permissions are
declared through plugin metadata, not through the TOML manifest.

### Architectural Invariants

These properties hold for any implementation of this ADR:

1. **Deterministic authorization.** The grant/deny decision for a given
   declaration depends only on the declared permission and the host's policy.
   It does not depend on plugin runtime behavior, activation order, or the
   state of other plugins.
2. **Immutable granted set.** Once computed at admission, a plugin's granted
   permissions do not change for the lifetime of that activation.
3. **Mandatory enforcement.** There is no configuration or operational mode
   that disables permission enforcement for any plugin.
4. **Declaration is necessary but not sufficient.** No undeclared capability
   can ever be granted, regardless of policy.

---

## Out of Scope

| Topic | Rationale |
|---|---|
| **Interactive permission prompting (Prompt)** | Deferred to a future ADR. This ADR defines Granted/Denied as the complete resolution space. Prompt semantics (user consent at install or first use) add UI-layer complexity that is not required for Milestone 0.9 |
| **Fine-grained RBAC** | M0.9 implements capability-grant; RBAC is future work (Spec §15) |
| **Permission revocation at runtime** | Granted set is immutable per activation (Invariant 2) |
| **Inter-plugin permission delegation** | Requires ADR-007 dependency model first |
| **New PluginPermission values** | Capability Matrix (Spec §5.1) defines the identifier set independently |
| **Manifest TOML permission syntax** | Permissions are declared via `Plugin.metadata()`, not `plugin.toml`. If Manifest v2 (Spec §5.2) adds TOML-level declarations, that is a schema decision, not a permission-model decision |

---

## Alternatives Considered

### A: Discovery-time validation (from Draft v1 Option A)

Validate permissions at the discovery boundary rather than the admission
boundary. Rejected because it violates the separation of responsibilities
established by [ADR-011](011-sdk-host-integration.md): discovery answers
"which compatible plugins exist?" (identity and compatibility), while
admission answers "what is the plugin authorized to do?" (security and
permissions). Merging these concerns would require the discovery layer to
carry authorization semantics it is not responsible for.

### B: Runtime-only enforcement (from Draft v1 Option C)

No admission-time validation; enforce only when plugins call APIs. Rejected
because it violates deterministic behavior: a plugin missing a critical
permission would be admitted, activated, and fail at an unpredictable point
during execution. Admission-time validation ensures that authorization
state is fully resolved before the plugin begins operation — the system
fails early, predictably, and with clear diagnostics.

### C: Default-Allow with Deny-List

Grant all declared permissions by default; operators deny specific ones.
Rejected because it contradicts the zero-trust principle (Architecture Book
v2.0 §11.1) and least privilege: every new capability identifier would be
automatically available to every plugin until explicitly denied, shifting
the security burden from plugin authors (who must justify their needs) to
operators (who must anticipate every risk). Default-deny preserves
evolvability — new capabilities can be added without affecting the
authorization state of existing plugins.

---

## Traceability

| This ADR | Specification Reference |
|---|---|
| D1 (Default-Deny) | Spec §5.4 Constraint, AC-4 bullet 4 |
| D2 (Three-State Resolution) | Spec §5.4 bullet 3 (undeclared → denied) |
| D3 (Admission-Time Validation) | Spec §5.4 bullet 2, AC-4 bullet 3 |
| D4 (Runtime Enforcement) | Spec §5.4 bullets 4–5, AC-4 bullets 3–4 |
| D5 (Policy Source) | Spec §5.4 Constraint (Default-Policy aus ADR-006) |
| D6 (Audit Integration) | Architecture Book v2.0 §11.1 (Audit) |

**Acceptance Criteria Coverage:** AC-4 requires (1) ADR-006 accepted before
implementation, (2) plugins declare capabilities, (3) host validates at
admission, (4) undeclared capabilities denied at runtime per default-policy.
Decisions D1–D4 satisfy these criteria. D5–D6 provide the supporting
infrastructure AC-4 implicitly requires.

---

## Cross-References

- [ADR-001](001-core-boundaries.md) — Core boundaries (manifest-only discovery)
- [ADR-004](004-plugin-security-integration.md) — Security integration point
- [ADR-008](008-plugin-context-definition.md) — PluginContext definition
- [ADR-010](010-plugin-sdk-architecture.md) — SDK architecture
- [ADR-011](011-sdk-host-integration.md) — SDK-Host integration (two-phase lifecycle)
- Milestone 0.9 Engineering Spec §5.4 — Permission Model Integration
- Architecture Book v2.0 §11.1 — Permission Model / Zero Trust
