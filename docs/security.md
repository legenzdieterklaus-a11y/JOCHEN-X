# Security

Security is capability-based. A `SecurityContext` holds a subject, permissions, and trust level;
`CapabilityModel` evaluates requests. Secrets are accessed through the `SecretProvider` port and
audit data through `AuditHooks`; the core stores no credentials.

## Plugin Security

`PluginSecurity` implements the Zero Trust principle for plugins. It maintains a
thread-safe trust ledger keyed by plugin identifier and enforces an
explicit-approval policy: a plugin is only admitted once it has been verified or
trusted, and a rejected plugin raises `PluginSecurityError` on any subsequent
verification attempt.

Trust levels: `UNTRUSTED` (default) → `VERIFIED` → `TRUSTED` | `REJECTED`.

See [Plugin Framework](extensions.md) §3.6 for the complete trust model, API
surface, and event integration.

## Security Events

All security events are defined in `app.security.events` with stable
`SecurityEventName` identifiers. Plugin-related security events:

| Event | Bus Name | Emitted When |
|---|---|---|
| `PluginVerified` | `security.plugin.verified` | A plugin passes security validation. |
| `PluginRejected` | `security.plugin.rejected` | A plugin is explicitly rejected. |

**Cross-references:** [Plugin Framework](extensions.md) · [Events](events.md) ·
[ADR-001](adr/001-core-boundaries.md)
