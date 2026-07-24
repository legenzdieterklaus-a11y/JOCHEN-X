# ADR 006: Plugin permission model

**Status:** Open – requires decision before implementation

## Context

The existing security model uses `Permission` objects with dotted capability
identifiers (e.g., `"secret.read"`, `"broker.trade"`). The `PluginStatus` model
includes a `permissions` field (currently hardcoded to `()`) that anticipates
plugins declaring required capabilities in their manifests.

The `plugin.toml` manifest schema does not yet support permission declarations.

## Decision Required

How should plugins declare required capabilities, and how should the foundation
enforce them?

### Option A: Manifest-declared permissions with static validation

Plugins list required permissions in `plugin.toml`:

```toml
permissions = ["event.publish", "service.resolve", "ui.register"]
```

The foundation validates at discovery time that all requested permissions are
known and permitted by the operator's trust policy.

### Option B: Capability-based sandboxing

Plugins receive a restricted `PluginContext` that only exposes APIs matching
their declared permissions. The foundation constructs a capability-limited view
at activation time.

### Option C: Defer permissions to the plugin activation layer

Permission validation is not performed at discovery time. Permissions are
enforced at the API boundary when plugins attempt to use foundation services.

## Consequences

The chosen option determines:
- The `plugin.toml` schema extension.
- The `PluginStatus.permissions` semantic.
- The `PluginContext` surface area (see [ADR-008](008-plugin-context-definition.md)).
- Whether permission violations are caught early (discovery) or late (runtime).

**Cross-references:** [Plugin Framework](../extensions.md) §3.1 ·
[Security](../security.md)
