# ADR 010: Plugin SDK architecture

**Status:** Accepted (v0.7.1)

## Context

The Plugin Framework (v0.7.0) discovers manifests inertly and never imports
or executes plugin code. To activate plugins in a future release without
coupling plugin authors to foundation internals, an intermediate
programming interface is required.

[ADR-008](008-plugin-context-definition.md) enumerated three options for
this interface:

* **Option A** – Restricted `PluginContext` with explicit ports.
* **Option B** – Full `ApplicationContext` access with capability checks.
* **Option C** – SDK-mediated access.

## Decision

We adopt **Option C**: a dedicated SDK package (`sdk/`) is the sole public
programming interface for JOCHEN X plugins.

Concretely:

1. Plugin authors depend only on `sdk`. Imports from `core`, `app`,
   `plugins`, `services`, `developer`, or `ui` are considered a defect.
2. The SDK provides plugin-scoped façades over the foundation's public
   contracts:
   - `PluginLogger` over the foundation's structured logger.
   - `PluginEventBus` over `core.events.EventBus` (via a narrow port).
   - `PluginServices` over a whitelisted service map (never the raw
     `ServiceRegistry`).
   - `PluginConfig` over an injected storage protocol.
   - `PluginResources` over a plugin-private directory.
3. The SDK owns the plugin lifecycle contract (`Plugin`,
   `BackgroundPlugin`, `UIPlugin`, `ToolPlugin`, `WorkflowPlugin`,
   `PluginRuntime`, `PluginLifecycleState`).
4. The SDK owns its own exception hierarchy (`PluginSDKError`), decoupled
   from `core.exceptions.JochenXError`.
5. The SDK ships with two independent semver tracks – `SDK_VERSION` and
   `SDK_API_VERSION` – so plugins can declare compatibility explicitly.

## Consequences

### Positive

* **Stable plugin surface.** The SDK contract can evolve independently of
  foundation internals as long as its public API stays backwards
  compatible.
* **Explicit capability model.** Plugins declare permissions in metadata;
  the SDK context wires enforcement automatically.
* **Independent testability.** Every SDK subsystem is unit-testable
  without spinning up the foundation.
* **Composition over inheritance.** `PluginRuntime` drives plugins without
  intruding into their class hierarchy.
* **No global state.** No SDK module holds process-wide singletons; every
  dependency is passed explicitly through the builder.

### Negative / Trade-offs

* Some duplication exists between SDK-facing value types (e.g. `PluginEvent`,
  `ApiVersion`) and their foundation-internal counterparts (`Event`,
  `Version`). This duplication is intentional: it isolates plugin code
  from foundation type changes.
* A future foundation change that adds new *required* fields to the plugin
  activation contract will require a corresponding minor SDK release. This
  is by design: adding fields is additive and safe.

## Non-goals

The SDK does not:

* Load, run, or supervise plugin *code* (that responsibility remains with
  a future host-side plugin activation stage – see
  [ADR-009](009-plugin-isolation-strategy.md)).
* Modify the existing Plugin Framework, event system, security foundation,
  or bootstrap composition.
* Introduce parallel infrastructure (loggers, buses, registries) alongside
  the foundation's.

## Cross-references

* [Plugin SDK](../sdk.md) – Specification for the shipped SDK.
* [Plugin Framework](../extensions.md) – Foundation manifest-only contract.
* [ADR-001](001-core-boundaries.md) – Core boundary rule.
* [ADR-008](008-plugin-context-definition.md) – Prior open decision resolved.
* [ADR-009](009-plugin-isolation-strategy.md) – Runtime isolation (still open).
