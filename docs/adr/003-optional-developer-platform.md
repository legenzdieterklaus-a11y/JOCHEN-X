# ADR 003: Developer platform is opt-in

Diagnostics are packaged separately and disabled by default. This preserves startup performance,
allows removal without affecting production composition, and prevents developer tooling from
becoming an application dependency.
