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

See [Plugin Framework](extensions.md) §3.7 and [Diagnostics](diagnostics.md)
for the diagnostic port contract.

**Cross-references:** [Plugin Framework](extensions.md) ·
[Diagnostics](diagnostics.md) · [ADR-003](adr/003-optional-developer-platform.md)
