# ADR 004: Plugin security integration timing

**Status:** Resolved by [ADR-011](011-sdk-host-integration.md) §D3 — `PluginSecurityStage` runs in `LOAD_PLUGINS` after discovery

## Context

The `PluginDiscoveryStage` runs during `StartupPhase.LOAD_PLUGINS` (phase 2).
The `SecurityBootstrapStage` runs during `StartupPhase.FINALIZE` (phase 4).
This means `PluginSecurity` is not available when plugins are discovered.

Currently, discovered plugins are registered in the `PluginCatalog` without
security validation. The `PluginSecurity.verify_manifest()` method exists but
is not called during bootstrap.

## Decision Required

When and how should `PluginSecurity` validate discovered plugin manifests?

### Option A: Move security validation into the LOAD_PLUGINS phase

Create the `PluginSecurity` service early (before or during `LOAD_PLUGINS`) so
that `PluginDiscoveryStage` can call `verify_manifest()` for each discovered
manifest. Only admitted plugins would be included in the `PluginCatalog`.

### Option B: Add a separate security validation stage after FINALIZE

Add a `PluginSecurityValidationStage` after the `SecurityBootstrapStage` that
iterates over the already-registered `PluginCatalog` and validates each entry
against `PluginSecurity`. Non-admitted plugins would be removed from the catalog.

### Option C: Defer security validation to runtime

Keep the current behavior. Security validation occurs only when a consumer
explicitly calls `PluginSecurity.verify()` or `verify_manifest()` at the point
of plugin activation, not during bootstrap.

## Consequences

The chosen option determines:
- Whether the `PluginCatalog` contains only security-approved plugins.
- Whether `PluginLoaded` events represent security-validated or only
  compatibility-validated manifests.
- The ordering dependency between `PluginDiscoveryStage` and
  `SecurityBootstrapStage`.

**Cross-references:** [Plugin Framework](../extensions.md) §3.4, §3.6 ·
[Foundation Architecture](../architecture.md)
