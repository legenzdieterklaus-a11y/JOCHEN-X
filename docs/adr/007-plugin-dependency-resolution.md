# ADR 007: Plugin Dependency Resolution

**Status:** APPROVED
**Approval Date:** 2026-07-29
**Supersedes:** —

---

## Context

The JOCHEN X plugin system enforces a two-phase lifecycle
([ADR-011](011-sdk-host-integration.md)): manifest-only discovery followed by
SDK-driven activation. Plugins are currently independent — each manifest is
evaluated in isolation during discovery, and the activation phase processes
plugins without considering inter-plugin relationships.

**The gap:** No architectural decision defines

1. how a plugin declares that it depends on another plugin,
2. what it means for a dependency to be satisfied or unsatisfied,
3. how dependency relationships constrain activation order,
4. what guarantees the system provides about dependency availability.

Without this decision, activation order is arbitrary, version compatibility
between plugins is unchecked, and dependency-related failures occur at
unpredictable points during plugin execution rather than at admission time.

### Existing Architectural Capabilities

The following capabilities are established by prior ADRs and authoritative
documents:

- The SDK defines a dependency value type carrying an identifier and a
  minimum version constraint (Architecture Book v2.0 §10)
- The SDK error hierarchy includes a dedicated dependency error type
  (Architecture Book v2.0 §10)
- Manifest-only discovery produces an immutable catalog of compatible plugins
  ([ADR-001](001-core-boundaries.md))
- Two-phase admission and activation are established as the plugin lifecycle
  model ([ADR-011](011-sdk-host-integration.md))
- Permission validation at the admission boundary is defined by
  [ADR-006](006-plugin-permission-model.md)
- The service registry provides trail-based cycle detection as an existing
  architectural pattern (Architecture Book v2.0 §8)

### Terminology

- **Dependency Declaration** — A plugin listing another plugin's identifier
  (and optionally a minimum version) in its manifest. A declaration expresses
  *structural intent*: "this plugin requires the presence and prior activation
  of plugin X."
- **Required Dependency** — A dependency whose absence prevents the declaring
  plugin from functioning. The declaring plugin cannot activate without it.
- **Optional Dependency** — A dependency whose absence does not prevent the
  declaring plugin from functioning. The declaring plugin activates regardless,
  but may offer reduced functionality.
- **Dependency Graph** — The directed acyclic graph formed by all dependency
  declarations across all admitted plugins. Vertices are plugins; edges point
  from a declaring plugin to its dependency.
- **Resolution** — The process of evaluating whether each declared dependency
  can be satisfied by an admitted, compatible plugin.

**Key distinction: Declaration = Structural Intent ≠ Activation.** A plugin
declaring a dependency on plugin X does not cause X to be loaded or admitted.
X must independently pass discovery, security verification
([ADR-004](004-plugin-security-integration.md)), and permission authorization
([ADR-006](006-plugin-permission-model.md)) before it can satisfy any
dependency.

---

## Decision

### D1: Dependency Declaration

A plugin declares dependencies on other plugins through its manifest metadata.
Two categories of dependency exist:

**Required Dependency.** The declaring plugin cannot function without the
dependency. If the dependency is absent, incompatible, or itself failed,
the declaring plugin is rejected at the resolution boundary.

**Optional Dependency.** The declaring plugin can function without the
dependency, potentially with reduced capability. If the dependency is
absent or incompatible, the declaring plugin proceeds to activation.
The plugin is informed of which optional dependencies were resolved
and which were not.

Each dependency declaration carries:
- The dependency's plugin identifier (mandatory)
- A minimum version constraint (optional; absence means any version)
- The dependency category: required or optional (mandatory)

**Rationale:** The distinction between required and optional reflects a
fundamental difference in architectural intent. A required dependency
expresses a structural prerequisite — the plugin's core contract cannot
be fulfilled without it. An optional dependency expresses an enhancement
opportunity — the plugin's core contract is complete without it, but
additional integration is possible when the dependency is present. Treating
all dependencies as required would unnecessarily couple plugin availability
to non-essential relationships.

**Milestone 0.9 scope:** The architectural semantics of both required and
optional dependencies are defined by this ADR. Implementation of optional
dependency behavior (graceful degradation, conditional feature registration)
may be deferred. An implementation that treats all dependencies as required
in Milestone 0.9 satisfies this ADR, provided the declaration schema
distinguishes the two categories so that future implementations can honor
the distinction without manifest changes.

### D2: Dependency Resolution Semantics

Each declared dependency resolves to exactly one of four states at the
resolution boundary:

| State | Meaning |
|---|---|
| **Resolved** | A plugin matching the declared identifier exists in the admitted set, and its version satisfies the declared constraint (if any). The dependency is satisfied. |
| **Unresolved** | A plugin matching the declared identifier exists in the admitted set, but its version does not satisfy the declared constraint. The dependency is present but incompatible. |
| **Missing** | No plugin matching the declared identifier exists in the admitted set. The dependency is absent. |
| **Failed** | A plugin matching the declared identifier was admitted but was itself rejected during resolution (e.g., due to its own unsatisfied dependencies or a cycle). The dependency cannot be relied upon. |

**State interpretation for required dependencies:**
Only the Resolved state permits the declaring plugin to proceed to activation.
Unresolved, Missing, and Failed each cause the declaring plugin to be rejected.

**State interpretation for optional dependencies:**
All four states permit the declaring plugin to proceed to activation. The
resolution result is propagated to the plugin at activation time so it can
adapt its behavior.

**Immutability:** Once a dependency's resolution state is determined, it does
not change for the lifetime of that activation cycle. Re-resolution requires
a full application restart.

### D3: Version Compatibility

Version compatibility is evaluated when a dependency declaration includes a
minimum version constraint.

**Compatible.** The dependency plugin's declared version is equal to or
greater than the minimum version specified in the declaration. The dependency
satisfies the version constraint.

**Incompatible.** The dependency plugin's declared version is less than the
minimum version specified in the declaration. The dependency does not satisfy
the version constraint, and the resolution state is Unresolved.

**No constraint.** When a dependency declaration omits the minimum version,
any version of the dependency plugin satisfies the constraint. Version
compatibility is trivially satisfied.

**Architectural semantics only.** This ADR defines what compatibility *means*
— whether a version relationship satisfies a constraint. It does not define
version string parsing, comparison algorithms, or the version numbering
scheme. The version scheme used by plugins follows the project's versioning
conventions as established in the Architecture Book v2.0.

### D4: Dependency Graph Semantics

The set of all dependency declarations across all admitted plugins forms a
dependency graph. This graph has the following architectural properties:

**Cycles.** A cycle exists when plugin A depends on plugin B, and plugin B
(directly or transitively) depends on plugin A. Cycles are architecturally
prohibited. A cycle means no valid activation order exists — each plugin in
the cycle requires another to be activated first, creating a deadlock in the
activation sequence. All plugins participating in a cycle are rejected.

**Self-dependencies.** A plugin declaring a dependency on itself is a
degenerate cycle of length one. Self-dependencies are rejected.

**Duplicate dependencies.** A plugin declaring the same dependency identifier
more than once (whether with the same or different version constraints) is a
manifest error. The dependency graph contains at most one edge from any
plugin to any other plugin.

**Transitive dependencies.** If plugin A depends on plugin B, and plugin B
depends on plugin C, then A has a transitive dependency on C. Transitive
dependencies are not declared — they are a consequence of the graph structure.
The activation guarantee (D6) ensures that all transitive dependencies are
activated before the declaring plugin, without requiring explicit transitive
declarations.

**Cascade failures.** When a plugin is rejected (due to a cycle, missing
dependency, version incompatibility, or any other resolution failure), all
plugins that depend on it — directly or transitively — must also be rejected
if the dependency is required. This propagation is deterministic: the same
graph with the same failure always produces the same set of rejections. For
optional dependencies, a cascade does not propagate — the depending plugin
proceeds with the dependency marked as Failed.

### D5: Resolution Boundary

Dependency resolution occupies a distinct position within the plugin lifecycle.
It occurs after permission authorization and before activation:

```
Discovery → Security Verification → Permission Authorization → Dependency Resolution → Activation
```

**Discovery** (LOAD_PLUGINS phase) answers: *which compatible plugins exist?*
Discovery reads manifests, checks application version compatibility, and
produces a catalog of compatible manifests. It does not evaluate dependencies.

**Security Verification** ([ADR-004](004-plugin-security-integration.md),
[ADR-005](005-plugin-integrity-validation.md)) answers: *is this plugin
trusted?* Security verification validates plugin integrity. It does not
evaluate dependencies.

**Permission Authorization** ([ADR-006](006-plugin-permission-model.md))
answers: *what is this plugin authorized to do?* Permission authorization
evaluates declared capabilities against the host's policy. It does not
evaluate dependencies. Only plugins that pass permission authorization enter
the admitted set available for dependency resolution.

**Dependency Resolution** (this ADR) answers: *are this plugin's structural
prerequisites satisfied?* Resolution evaluates the dependency graph formed by
admitted plugins, determines the resolution state of each declared dependency,
and rejects plugins whose required dependencies are not resolved.

**Activation** (FINALIZE phase) answers: *is this plugin operational?*
Activation imports plugin code, constructs the plugin context, and invokes
lifecycle hooks. Activation receives the dependency-ordered sequence from
resolution and activates plugins in that order.

**Separation principle:** Each phase owns exactly one responsibility and
produces exactly one output. No phase assumes or replicates the
responsibility of another. Dependency resolution consumes the output of
permission authorization (the admitted set) and produces input for activation
(the resolved, ordered set).

### D6: Activation Guarantees

The following conditions must hold before a plugin enters the Active state:

1. **All required dependencies resolved.** Every required dependency declared
   by the plugin has resolution state Resolved.
2. **All required dependencies activated.** Every required dependency has
   completed its own activation (including its lifecycle hooks) before the
   declaring plugin's activation begins.
3. **Transitive closure satisfied.** The activation guarantee applies
   recursively: if plugin A requires B, and B requires C, then C is activated
   before B, and B is activated before A.
4. **Optional dependency resolution known.** The resolution state of every
   optional dependency is determined and available to the plugin at activation
   time. Optional dependencies that are Resolved are activated before the
   declaring plugin. Optional dependencies that are Missing, Unresolved, or
   Failed do not block activation.

**Activation order respects all required dependency relationships.** If
plugin A requires plugin B, then B is activated before A in every execution.
This ordering is deterministic: the same dependency graph always produces the
same activation sequence.

This ADR does not prescribe any particular ordering algorithm. Any algorithm
that satisfies the guarantees above is a valid implementation.

### D7: Architectural Invariants

These properties hold for any implementation of this ADR:

1. **Deterministic resolution.** The resolution state of every dependency is
   a pure function of the admitted plugin set, the declared dependencies, and
   the declared versions. It does not depend on filesystem ordering, runtime
   state, activation timing, or external input.

2. **Graph consistency.** The dependency graph is validated as a whole before
   any activation begins. There is no state where part of the graph is
   resolved and part is not.

3. **Reproducible startup.** Given the same set of plugin manifests and the
   same host configuration, the system produces the same resolution states,
   the same rejections, and the same activation order on every startup.

4. **No partial activation.** A plugin is either fully resolved (all required
   dependencies satisfied) and eligible for activation, or it is rejected.
   There is no intermediate state where a plugin is activated with some
   required dependencies satisfied and others pending.

5. **Immutable resolution result.** Once dependency resolution completes, the
   resolution state of every dependency and the activation order are fixed for
   the lifetime of that application run. No runtime event changes the
   resolution result.

6. **Fail-fast on graph violations.** Cycles, self-dependencies, and
   duplicate dependencies are detected and rejected at the resolution
   boundary, before any plugin in the graph is activated.

7. **Isolation of rejection.** A plugin's rejection due to dependency failure
   affects only those plugins that (directly or transitively) require it. All
   other plugins proceed to activation normally. The rejection of a plugin
   that is only an optional dependency of others does not prevent those others
   from activating.

### D8: Separation of Responsibilities

| Phase | Responsibility | Input | Output |
|---|---|---|---|
| **Discovery** | Identify compatible plugins from manifests | Plugin directory, application version | `PluginCatalog` — set of compatible manifests |
| **Security Verification** | Validate plugin integrity and trust | Compatible manifests, security policy | Verified manifest set |
| **Permission Authorization** | Evaluate declared capabilities against host policy | Verified manifests, permission policy | Admitted set with granted permissions |
| **Dependency Resolution** | Evaluate structural prerequisites and determine activation order | Admitted set with dependency declarations | Resolved set with activation order; rejected set with rejection reasons |
| **Activation** | Import code, construct context, invoke lifecycle hooks | Resolved set in dependency order | Running plugin instances |

Each phase:
- Owns exactly one concern
- Consumes the output of the preceding phase
- Does not replicate or bypass the checks of any other phase
- Produces an output that is consumed by the next phase

No phase has visibility into the internal decisions of another. Dependency
resolution does not re-evaluate permissions; permission authorization does
not evaluate dependencies; activation does not re-resolve the dependency
graph.

---

## Consequences

### Resolution Boundary

The plugin lifecycle gains a new phase: dependency resolution, positioned
between permission authorization and activation. This extends the existing
admission contract ([ADR-011](011-sdk-host-integration.md)) without replacing
it — security verification, permission authorization, and dependency
resolution are complementary admission checks, each with a distinct
responsibility.

### Activation Order

Activation order becomes architecturally significant. Without this ADR, the
activation phase processes plugins without regard to inter-plugin
relationships. With this ADR, activation order is constrained by the
dependency graph: dependencies are activated before the plugins that require
them. The activation phase assumes a new architectural responsibility —
honoring the dependency-determined order.

### Rejection Propagation

A plugin's rejection can cascade to other plugins. If plugin A is rejected
(for any reason — security, permissions, or dependency failure), any plugin
that declares a required dependency on A is also rejected. This cascade is
deterministic and bounded by the dependency graph.

### Manifest Responsibility

The plugin manifest assumes a new architectural responsibility: carrying
dependency declarations that distinguish required from optional dependencies
and optionally specify version constraints. This extends the manifest's role
as the single source of plugin metadata.

### Diagnostic Responsibility

Dependency-related rejections must produce diagnostics that convey the
specific resolution state (Missing, Unresolved, Failed) and the identity
of the unsatisfied dependency. The SDK's existing dependency error type
carries this responsibility.

### What Remains Unchanged

The manifest discovery contract ([ADR-001](001-core-boundaries.md)) is
unchanged — dependency declarations extend the manifest metadata, they do
not alter the discovery mechanism. The permission model
([ADR-006](006-plugin-permission-model.md)) is unchanged — dependency
resolution is a separate phase that does not modify or reinterpret permission
decisions. Plugin lifecycle states (Architecture Book v2.0 §10.6) are
unchanged. The SDK's existing dependency and error type definitions are
unchanged in structure.

### Architectural Invariants

These properties hold for any implementation of this ADR:

1. **Deterministic resolution.** The same set of manifests and configuration
   always produces the same resolution states and activation order (D7.1).
2. **Immutable resolution result.** Resolution states are fixed for the
   lifetime of an application run (D7.5).
3. **No partial activation.** A plugin with any unsatisfied required
   dependency is never activated (D7.4).
4. **Mandatory graph validation.** The dependency graph is validated as a
   whole before any activation begins (D7.2, D7.6).

---

## Out of Scope

| Topic | Rationale |
|---|---|
| **Graph traversal algorithms** | This ADR defines what the graph means, not how to traverse it. Topological sort, DFS, or any other algorithm that satisfies D6 and D7 is valid. |
| **Cycle detection algorithms** | This ADR defines that cycles are prohibited (D4). Detection mechanism is an implementation choice. |
| **Scheduling and threading** | This ADR defines activation guarantees (D6), not execution strategy. Implementations may choose any execution strategy — including parallel activation — provided the guarantees in D6 remain satisfied. |
| **Caching and performance** | Resolution runs once per startup. Optimization is an implementation concern. |
| **SDK resolver implementation** | The SDK provides value types. Resolution logic belongs to the host. |
| **Dynamic dependency registration** | Dependencies are declared in the manifest, not at runtime. Runtime service discovery uses `ServiceRegistry`, which is a separate mechanism. |
| **Inter-plugin permission delegation** | Noted as future work in [ADR-006](006-plugin-permission-model.md). Requires dependency model (this ADR) as prerequisite; delegation semantics are a separate architectural decision. |
| **Plugin hot-reload** | Resolution result is immutable per application run (D7.5). Hot-reload would require re-resolution, which is a separate architectural decision. |

---

## Alternatives Considered

### A: No Dependency Model

Plugins remain permanently independent. Shared functionality is provided
exclusively through foundation services registered in the `ServiceRegistry`.
Inter-plugin communication occurs only through the `EventBus`.

**Rejected** because it forces all shared functionality into foundation
services, even when the functionality is plugin-specific. It prevents the
plugin ecosystem from growing organically — every reusable capability must
be anticipated and provided by the host. The `PluginDependency` value type
and `PluginDependencyError` already exist in the SDK, indicating that the
platform anticipates inter-plugin relationships. Ignoring this leaves
activation order undefined and version compatibility unchecked.

### B: Runtime-only Resolution

Dependencies are declared in the manifest but not evaluated at the resolution
boundary. Plugins discover their dependencies at activation time by querying
the `ServiceRegistry` or `EventBus` for expected providers. Missing
dependencies cause runtime failures.

**Rejected** because it violates deterministic behavior (Invariant D7.1) and
fail-fast principles (Invariant D7.6). A plugin with a missing dependency
would be activated, begin execution, and fail at an unpredictable point.
Cycle detection is impossible at runtime because the activation sequence has
already committed. The same reasoning that led ADR-006 to reject runtime-only
enforcement (Alternative B) applies here: early, predictable failure at a
well-defined boundary is architecturally superior to late, unpredictable
failure during operation.

### C: Dependency Resolution before Admission

Evaluate dependencies at the discovery boundary, before security verification
and permission authorization. Dependency resolution is the first check after
manifest parsing.

**Rejected** because it violates the separation of responsibilities
established by [ADR-011](011-sdk-host-integration.md) and extended by
[ADR-006](006-plugin-permission-model.md). Discovery answers "which compatible
plugins exist?" — a question about identity and compatibility, not about
structural relationships. Evaluating dependencies before security verification
would allow untrusted plugins to influence the admission of other plugins
(a rejected dependency could cascade-reject a trusted plugin before security
is even checked). Evaluating dependencies before permission authorization
would resolve dependencies against plugins that may subsequently be denied
their required capabilities, producing a dependency graph that does not
reflect the actual set of operational plugins.

### D: Approved Resolution Boundary (Selected)

Dependency resolution occurs after permission authorization and before
activation, as defined in D5. This is the selected approach.

**Rationale:** The resolution boundary is positioned at the point where all
prerequisite information is available. Discovery has identified compatible
plugins. Security verification has established trust. Permission
authorization has determined capability grants. Only now can dependency
resolution meaningfully evaluate whether a plugin's structural prerequisites
are met — because only now is the set of admitted, authorized plugins known.
This placement follows the same architectural reasoning as ADR-006 D3
(admission-time validation): resolve early, resolve completely, resolve
before any plugin code executes.

---

## Traceability

| This ADR | Specification Reference |
|---|---|
| D1 (Dependency Declaration) | Spec §5.5 bullet 1 (graph from `dependencies.requires`) |
| D2 (Resolution Semantics) | Spec §5.5 bullet 5 (missing required → rejection) |
| D3 (Version Compatibility) | Spec §5.5 bullet 4 (`minimum_version` constraints) |
| D4 (Dependency Graph) | Spec §5.5 bullet 3 (cycle detection and rejection) |
| D5 (Resolution Boundary) | Spec §5.5 Constraint (architectural semantics from accepted ADR-007) |
| D6 (Activation Guarantees) | Spec §5.5 bullet 2 (topological sort determines activation order) |
| D7 (Invariants) | AC-5 bullet 7 (dependency semantics per accepted ADR-007) |
| D8 (Separation) | Architecture Book v2.0 §7.2 (Bootstrap phase separation) |

**Acceptance Criteria Coverage:** AC-5 requires (1) ADR-007 accepted before
implementation, (2) dependency graph constructed from manifest, (3)
topological sort determines activation order, (4) cycles detected and
rejected, (5) version constraints checked, (6) missing required dependencies
cause rejection, (7) semantics per accepted ADR-007. Decisions D1–D6 define
the architectural semantics these criteria reference. D7–D8 provide the
invariants and separation guarantees that ensure deterministic, reproducible
behavior.

---

## Cross-References

- [ADR-001](001-core-boundaries.md) — Core boundaries (manifest-only discovery)
- [ADR-004](004-plugin-security-integration.md) — Security integration point
- [ADR-005](005-plugin-integrity-validation.md) — Plugin integrity validation
- [ADR-006](006-plugin-permission-model.md) — Plugin permission model
- [ADR-008](008-plugin-context-definition.md) — PluginContext definition
- [ADR-010](010-plugin-sdk-architecture.md) — SDK architecture
- [ADR-011](011-sdk-host-integration.md) — SDK-Host integration (two-phase lifecycle)
- Milestone 0.9 Engineering Spec §5.5 — Dependency Resolution Integration
- Milestone 0.9 Engineering Spec AC-5 — Dependency Resolution Acceptance Criteria
- Architecture Book v2.0 §7.2 — Bootstrap phase separation
- Architecture Book v2.0 §10 — Plugin-System
