# Health

Health checks are supplied as `HealthStatus` values from the core observability
module. The Developer Platform only displays supplied results, so it cannot alter
lifecycle, scheduler, or application state.

## Health Subsystems

`ApplicationHost.health()` reports on these subsystems:

| Subsystem | Healthy Condition | Detail |
|---|---|---|
| `lifecycle` | State is `READY`, `BUSY`, or `UPDATING` | Current state value |
| `workers` | Always `True` | Active worker count |
| `errors` | No fatal error recorded | `"ok"` or error category |

## Plugin Health

Plugin health is represented by the `PluginCatalog.count` property, which is
displayed in the UI status bar (`"Plugins: N discovered"`). Individual plugin
health checks are not implemented in v0.7.0; plugins are treated as inert
metadata and have no runtime health state.

**Cross-references:** [Plugin Framework](extensions.md) ·
[Diagnostics](diagnostics.md) · [Performance](performance.md)
