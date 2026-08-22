# Health

Health checks are supplied as `HealthStatus` values from the core observability
module. The Developer Platform only displays supplied results, so it cannot alter
lifecycle, scheduler, or application state.

## Contracts

| Symbol | Module | Role |
|---|---|---|
| `HealthStatus` | `core/observability.py` | Immutable result (`name`, `healthy`, `detail`). |
| `HealthCheck` | `core/observability.py` | Protocol: `check() -> HealthStatus`. |
| `PluginHealthCheck` | `core/observability.py` | `HealthCheck` implementation that maps a plugin's **live** lifecycle state (`started`, `initialized`, `failed`, `stopped`, `unloaded`) to a status named `plugin.<identifier>`. |
| `run_health_checks` | `core/observability.py` | Evaluates any number of `HealthCheck` implementations and returns their statuses. |
| `HealthCheckRegistry` | `core/observability_registry.py` | Registration point for `HealthCheck` implementations (`register`, `unregister`, `names`, `checks`, `run`). `run()` delegates to `run_health_checks()`. |

## Registration path

`PluginActivationStage` creates one `PluginHealthCheck` per plugin — reading the
live runtime state for activated plugins and the failed state for plugins whose
activation failed — registers them on a `HealthCheckRegistry`, and publishes the
registry in the `ServiceRegistry`. Because the checks read state on demand, a
later `runtime.shutdown()` is reflected immediately in the next `run()`.

`ApplicationHost.health()` remains a separate surface: it reports the host's own
subsystems (lifecycle, workers, errors), not plugin state.

## Health Subsystems

`ApplicationHost.health()` reports on these subsystems:

| Subsystem | Healthy Condition | Detail |
|---|---|---|
| `lifecycle` | State is `READY`, `BUSY`, or `UPDATING` | Current state value |
| `workers` | Always `True` | Active worker count |
| `errors` | No fatal error recorded | `"ok"` or error category |

## Plugin Health

Plugin health has two separate surfaces:

- **Runtime health** — `PluginActivationStage` registers one `PluginHealthCheck`
  per plugin on the `HealthCheckRegistry` (see [Registration path](#registration-path)).
  `HealthCheckRegistry.run()` therefore yields one `plugin.<identifier>` status
  per plugin, derived from the lifecycle state read at call time.
- **Discovery count** — `PluginCatalog.count` is displayed in the UI status bar
  and on the dashboard (`"N discovered"`). It counts catalog entries and carries
  no health semantics.

`PluginHealthCheck` maps the live lifecycle state as follows:

| Lifecycle state | `healthy` | `detail` |
|---|---|---|
| `started` | `True` | `""` |
| `initialized` | `True` | `"not yet started"` |
| `failed` | `False` | `"activation failed"` |
| `stopped` | `False` | `"degraded"` |
| `unloaded` | `False` | `"not loaded"` |
| unmapped value | `False` | `"unknown state: <state>"` |

**Cross-references:** [Plugin Framework](extensions.md) ·
[Diagnostics](diagnostics.md) · [Performance](performance.md)
