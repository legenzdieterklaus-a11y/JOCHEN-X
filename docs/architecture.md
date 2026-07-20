# Foundation architecture

`ApplicationHost` owns the lifecycle. During bootstrap it constructs infrastructure in this
order: environment, logging, configuration, database migration, theme, security,
observability, AI gateway, and plugin loader. The `ServiceRegistry` is the only composition
mechanism and is passed explicitly to consumers.

The SQLite database contains only `schema_version` and `settings`. Configuration is validated
before it reaches runtime services. Provider and plugin code is discovered as metadata; neither
is executed by the foundation.

## Proposed ADRs

The referenced Master Specification 1.0 was not supplied with this implementation request, so
no undocumented architectural change has been made. If it requires a different composition
root or package direction, record that as an ADR before modifying these boundaries.
