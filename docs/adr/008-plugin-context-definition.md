# ADR 008: Plugin context definition

**Status:** Open – requires decision before implementation

## Context

The `ApplicationContext` is the fully-injected, immutable aggregate of all
foundation services. When plugins are activated in a future version, they will
need access to a subset of these services (e.g., `EventBus`, `ServiceRegistry`,
logging, configuration).

Currently, no `PluginContext` exists. Plugins are inert metadata and never
receive any foundation services.

## Decision Required

What services and APIs should be exposed to loaded plugin code, and through
what interface?

### Option A: Restricted PluginContext with explicit ports

Each plugin receives a `PluginContext` that exposes only the services
permitted by its declared capabilities:

- Event publishing (filtered by namespace)
- Service resolution (restricted by permission)
- Logging (namespaced to the plugin)
- Configuration (plugin-scoped section)

The `PluginContext` is a purpose-built facade, not the full
`ApplicationContext`.

### Option B: Full ApplicationContext access

Plugins receive the same `ApplicationContext` as foundation code. Security
is enforced at the API boundary by capability checks.

### Option C: SDK-mediated access

Plugins interact with the foundation exclusively through a Plugin SDK that
abstracts the internal service topology and provides versioned, stable APIs.

## Consequences

The chosen option determines:
- The plugin activation surface.
- The security boundary enforcement strategy.
- The coupling between plugins and foundation internals.
- The API stability guarantees for plugin developers.
- The testing strategy for plugins (mock context vs. real foundation).

**Cross-references:** [Plugin Framework](../extensions.md) §3.5 ·
[Core](../core.md) · [Security](../security.md) ·
[ADR-006](006-plugin-permission-model.md)
