"""Security exception taxonomy for the JOCHEN X Security Foundation.

Every security failure that is expected and user-relevant derives from
:class:`SecurityError`, which itself extends the shared
:class:`core.exceptions.JochenXError` base. This keeps the security subsystem
inside the application's single, coherent error hierarchy instead of introducing
a parallel taxonomy, so the existing centralized error handler continues to
classify and route security failures without modification.
"""

from __future__ import annotations

from core.exceptions import JochenXError


class SecurityError(JochenXError):
    """Base class for all recoverable security-subsystem failures."""


class PermissionDeniedError(SecurityError):
    """Raised when an identity lacks a permission required for an operation."""


class SecretNotFoundError(SecurityError):
    """Raised when a requested secret does not exist in the vault."""


class EncryptionError(SecurityError):
    """Raised when an encryption or decryption operation cannot complete."""


class BrokerSecurityError(SecurityError):
    """Raised when broker authentication preparation or validation fails."""


class PluginSecurityError(SecurityError):
    """Raised when a plugin fails security validation or is explicitly rejected."""
