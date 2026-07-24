# Services

Registrations belong only in the composition root. Singleton instances are
constructed on first use, transient registrations construct per resolution, and
scoped registrations require an explicit `ServiceScope`. `validate()` resolves
the graph during bootstrap when eager verification is wanted.

## Service Lifetimes

| Lifetime | Construction | Scope Requirement | Use Case |
|---|---|---|---|
| `SINGLETON` | Once (on first resolution) | None | Shared infrastructure (e.g., `EventBus`, `PluginLoader`) |
| `TRANSIENT` | Every resolution | None | Stateless or short-lived instances |
| `SCOPED` | Once per `ServiceScope` | Requires explicit scope | Request-scoped or session-scoped services |

## Plugin Framework Services

The Plugin Framework registers two singletons during bootstrap:

- `PluginLoader` — manifest discovery service.
- `PluginCatalog` — immutable snapshot of discovered plugin identifiers.

See [Plugin Framework](extensions.md) §7 for the complete registration table.

**Cross-references:** [Core](core.md) · [Plugin Framework](extensions.md) ·
[Foundation Architecture](architecture.md)
