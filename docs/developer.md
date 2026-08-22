# Developer Platform

The Developer Platform is an optional package, disabled by default and absent
from normal host composition (see [ADR-003](adr/003-optional-developer-platform.md)).
Instantiate `DeveloperPlatform(enabled=True, ...)` only from a developer-only
composition root. It starts no workers and performs file I/O only when a caller
requests logs.

## Plugin Inspection

When enabled, the Developer Platform exposes plugin diagnostics through the
`plugins()` method, which calls `PluginDiagnostics.discover()` and maps each
result to a `PluginStatus` value object. The platform never imports, loads, or
executes plugin code.

`plugin_diagnostics()` returns the consolidated runtime diagnostics supplied by
an injected `PluginRuntimeDiagnostics` port — the `PluginDiagnosticsReport`
published by the activation stage satisfies it. When that port is supplied,
`plugins()` also derives each `PluginStatus.enabled` flag from the real
activation outcome instead of assuming success.

Without the port the two surfaces behave differently: `plugin_diagnostics()`
returns nothing rather than a placeholder, while `plugins()` still lists every
discovered plugin and falls back to `enabled = True`, because the activation
outcome mapping is empty.

`ArchitectureInspector` accepts the same port and adds a warning for every
plugin that did not reach activation.

See [Plugin Framework](extensions.md) §3.7 and [Diagnostics](diagnostics.md)
for the diagnostic port contract.

**Cross-references:** [Plugin Framework](extensions.md) ·
[Diagnostics](diagnostics.md) · [Health](health.md) ·
[ADR-003](adr/003-optional-developer-platform.md)
