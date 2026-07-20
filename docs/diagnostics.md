# Diagnostics API

Developer modules depend on `EventDiagnostics`, `ServiceDiagnostics`, and `PluginDiagnostics`
ports. Core components expose safe diagnostic snapshots (`EventDelivery` and `ServiceDescriptor`)
rather than registrations, handlers, or event payloads.
