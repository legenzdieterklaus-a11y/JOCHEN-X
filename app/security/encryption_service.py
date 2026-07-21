"""Encryption abstraction for the Security Foundation.

This module defines the :class:`EncryptionService` interface that the rest of the
subsystem depends on. Following the phase plan, no real cryptography (AES, RSA,
and similar) is implemented yet. The shipped default,
:class:`ReversibleEncryptionService`, provides a fully working, reversible
*encoding* so dependent components (vault, backups) can store and retrieve values
today and be transparently upgraded to a real cryptographic implementation later
without any API change. It is intentionally and explicitly **not** secure.
"""

from __future__ import annotations

import base64
import secrets
from abc import ABC, abstractmethod

from app.security.exceptions import EncryptionError

_DEFAULT_KEY_BYTES = 32


class EncryptionService(ABC):
    """Interface for reversible protection of byte payloads.

    Implementations must guarantee that ``decrypt(encrypt(data)) == data`` for
    any byte payload. Concrete cryptographic implementations will be introduced
    in a later phase behind this same contract.
    """

    @abstractmethod
    def generate_key(self) -> bytes:
        """Return freshly generated key material.

        Returns:
            A new, unpredictable key suitable for a future cryptographic backend.
        """

    @abstractmethod
    def encrypt(self, plaintext: bytes) -> bytes:
        """Protect ``plaintext`` and return the transformed representation.

        Args:
            plaintext: The raw bytes to protect.

        Returns:
            The protected representation of ``plaintext``.

        Raises:
            EncryptionError: If the payload cannot be transformed.
        """

    @abstractmethod
    def decrypt(self, ciphertext: bytes) -> bytes:
        """Reverse :meth:`encrypt` and return the original bytes.

        Args:
            ciphertext: A representation previously returned by :meth:`encrypt`.

        Returns:
            The original plaintext bytes.

        Raises:
            EncryptionError: If the payload cannot be reversed.
        """


class ReversibleEncryptionService(EncryptionService):
    """Reversible, non-cryptographic default encoder.

    This implementation base64-encodes payloads so the storage layer works end to
    end during the Security Foundation phase. It performs no confidentiality
    protection and must be replaced by a cryptographic backend before any real
    secret is trusted to it.
    """

    def generate_key(self) -> bytes:
        """Return a cryptographically-random 256-bit token as placeholder key material."""
        return secrets.token_bytes(_DEFAULT_KEY_BYTES)

    def encrypt(self, plaintext: bytes) -> bytes:
        """Base64-encode ``plaintext`` into a reversible representation."""
        try:
            return base64.b64encode(plaintext)
        except (TypeError, ValueError) as error:
            raise EncryptionError("Failed to encode payload") from error

    def decrypt(self, ciphertext: bytes) -> bytes:
        """Reverse :meth:`encrypt` by base64-decoding ``ciphertext``."""
        try:
            return base64.b64decode(ciphertext, validate=True)
        except (TypeError, ValueError) as error:
            raise EncryptionError("Failed to decode payload") from error
