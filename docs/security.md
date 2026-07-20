# Security

Security is capability-based. A `SecurityContext` holds a subject, permissions, and trust level;
`CapabilityModel` evaluates requests. Secrets are accessed through the `SecretProvider` port and
audit data through `AuditHooks`; the core stores no credentials.
