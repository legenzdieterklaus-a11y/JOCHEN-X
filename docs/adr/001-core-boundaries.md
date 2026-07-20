# ADR 001: Explicit core boundaries

Core modules expose ports and value types and are assembled by the application host. This preserves
dependency inversion, avoids global state, and allows platform or feature implementations to remain
outside the low-overhead startup path.
