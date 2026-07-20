# ADR 002: Explicit event delivery modes

The bus retains synchronous publishing for deterministic short notifications and provides an async
entry point for non-blocking delivery. Consumers, rather than the core, own executor or UI-loop
integration because the core cannot safely assume a running event loop.
