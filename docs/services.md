# Services

Registrations belong only in the composition root. Singleton instances are constructed on first
use, transient registrations construct per resolution, and scoped registrations require an explicit
`ServiceScope`. `validate()` resolves the graph during bootstrap when eager verification is wanted.
