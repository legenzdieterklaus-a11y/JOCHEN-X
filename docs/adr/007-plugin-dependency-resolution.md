# ADR 007: Plugin dependency resolution

**Status:** Open – requires decision before implementation

## Context

The `PluginStatus` model includes a `dependencies` field (currently hardcoded
to `()`) that anticipates plugins declaring dependencies on other plugins. The
`plugin.toml` manifest schema does not yet support dependency declarations, and
no dependency resolver exists.

Plugins are currently independent: each manifest is evaluated in isolation
during discovery.

## Decision Required

How should inter-plugin dependencies be declared and resolved?

### Option A: Manifest-declared dependencies with topological sorting

Plugins declare dependencies in `plugin.toml`:

```toml
dependencies = ["com.example.base-plugin >= 1.0.0"]
```

The `PluginLoader` or a dedicated `DependencyResolver` topologically sorts
manifests and rejects plugins with unsatisfied or cyclic dependencies.

### Option B: Optional dependencies with runtime resolution

Dependencies are declared but not enforced at discovery time. Plugins check
for the presence of dependencies at activation time and degrade gracefully.

### Option C: No inter-plugin dependencies

Plugins are always independent. Shared functionality is provided by foundation
services, not by other plugins.

## Consequences

The chosen option determines:
- The `plugin.toml` schema extension.
- The `PluginStatus.dependencies` semantic.
- Whether the `PluginCatalog` ordering is significant.
- The complexity of the discovery algorithm (topological sort, cycle detection).
- The error model for unsatisfied dependencies.

**Cross-references:** [Plugin Framework](../extensions.md) §3.1, §3.3
