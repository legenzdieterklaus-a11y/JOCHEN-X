# Events

`EventBus` supports synchronous and asynchronous publishing, priority-ordered subscriptions,
filters, glob-style event names, bounded history, and sticky events. It is thread safe. UI callers
must use `publish_async` for any handler that can block; synchronous publication is intentionally
reserved for brief in-process notifications.

## Event Vocabulary

### Application Lifecycle Events (`app.events`)

| Event Class | Bus Name | Payload |
|---|---|---|
| `ApplicationStarting` | `application.starting` | `{"version": str}` |
| `ApplicationStarted` | `application.started` | `{"service_count": int}` |
| `ApplicationReady` | `application.ready` | `{"startup_ms": float}` |
| `ApplicationStateChanged` | `application.state.changed` | `{"previous": str, "current": str}` |
| `PluginLoading` | `application.plugin.loading` | `{"identifier": str}` |
| `PluginLoaded` | `application.plugin.loaded` | `{"identifier": str, "version": str}` |
| `PluginActivating` | `application.plugin.activating` | `{"identifier": str}` |
| `PluginActivated` | `application.plugin.activated` | `{"identifier": str, "version": str}` |
| `PluginFailed` | `application.plugin.failed` | `{"identifier": str, "reason": str}` |
| `ConfigurationChanged` | `application.configuration.changed` | `{"keys": list[str]}` |
| `ThemeChanged` | `application.theme.changed` | `{"mode": str}` |
| `BusyStarted` | `application.busy.started` | `{"reason": str}` |
| `BusyFinished` | `application.busy.finished` | `{"reason": str}` |
| `ShutdownRequested` | `application.shutdown.requested` | `{"reason": str}` |
| `ShutdownCompleted` | `application.shutdown.completed` | `{"exit_code": int}` |
| `ErrorRaised` | `application.error.raised` | `{"category": str, "severity": str, "message": str}` |

### Security Events (`app.security.events`)

| Event Class | Bus Name | Payload |
|---|---|---|
| `SecurityInitialized` | `security.initialized` | `{"service_count": int}` |
| `PluginVerified` | `security.plugin.verified` | `{"identifier": str, "version": str, "trust": str}` |
| `PluginRejected` | `security.plugin.rejected` | `{"identifier": str, "reason": str}` |

See [Plugin Framework](extensions.md) §5 for the complete plugin event reference.

## Delivery Semantics

See [ADR-002](adr/002-event-delivery.md) for the rationale behind synchronous
and asynchronous delivery modes.

**Cross-references:** [Plugin Framework](extensions.md) ·
[Security](security.md) · [ADR-002](adr/002-event-delivery.md)
