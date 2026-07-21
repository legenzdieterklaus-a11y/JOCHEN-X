"""Identity and session management for the Security Foundation.

:class:`IdentityManager` owns the lifecycle of security principals and their
sessions. The current phase runs single-user, but the API is deliberately
multi-identity and multi-session so future multi-user support can be added
without reshaping callers. All state is in-memory and thread-safe.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Iterable
from dataclasses import dataclass
from threading import RLock
from uuid import uuid4

from app.security.exceptions import SecurityError
from app.security.models import Identity

_LOGGER_NAME = "jochen_x.security.identity"


@dataclass(frozen=True, slots=True)
class Session:
    """An immutable record of an authenticated session for an identity.

    Attributes:
        session_id: Stable, unique identifier of the session.
        identity_id: Identifier of the owning identity.
        started_at: Wall-clock start timestamp in seconds since the epoch.
        active: Whether the session is currently open.
    """

    session_id: str
    identity_id: str
    started_at: float
    active: bool = True


class IdentityManager:
    """Thread-safe registry of identities and their sessions."""

    def __init__(self, *, logger: logging.Logger | None = None) -> None:
        """Create an empty identity manager.

        Args:
            logger: Optional logger for diagnostics.
        """
        self._logger = logger or logging.getLogger(_LOGGER_NAME)
        self._identities: dict[str, Identity] = {}
        self._sessions: dict[str, Session] = {}
        self._lock = RLock()

    def create_identity(self, display_name: str, *, roles: Iterable[str] = ()) -> Identity:
        """Create and register a new identity.

        Args:
            display_name: Human-readable name for the identity.
            roles: Optional initial role names for the identity.

        Returns:
            The newly created :class:`~app.security.models.Identity`.

        Raises:
            ValueError: If ``display_name`` is empty.
        """
        if not display_name:
            raise ValueError("Identity display name must be a non-empty string")
        identity = Identity(
            identifier=uuid4().hex,
            display_name=display_name,
            roles=tuple(roles),
            created_at=time.time(),
        )
        with self._lock:
            self._identities[identity.identifier] = identity
        self._logger.info("identity.created", extra={"context": {"identity": identity.identifier}})
        return identity

    def get(self, identity_id: str) -> Identity:
        """Return the identity registered under ``identity_id``.

        Raises:
            SecurityError: If the identity does not exist.
        """
        with self._lock:
            identity = self._identities.get(identity_id)
        if identity is None:
            raise SecurityError(f"Unknown identity: {identity_id}")
        return identity

    def identities(self) -> tuple[Identity, ...]:
        """Return all registered identities."""
        with self._lock:
            return tuple(self._identities.values())

    def start_session(self, identity_id: str) -> Session:
        """Open a new session for an existing identity.

        Args:
            identity_id: Identifier of the identity to open a session for.

        Returns:
            The newly created active :class:`Session`.

        Raises:
            SecurityError: If the identity does not exist.
        """
        self.get(identity_id)
        session = Session(session_id=uuid4().hex, identity_id=identity_id, started_at=time.time())
        with self._lock:
            self._sessions[session.session_id] = session
        self._logger.info("identity.session_started", extra={"context": {"session": session.session_id}})
        return session

    def end_session(self, session_id: str) -> None:
        """Close an active session.

        Args:
            session_id: Identifier of the session to close.

        Raises:
            SecurityError: If the session does not exist.
        """
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                raise SecurityError(f"Unknown session: {session_id}")
            self._sessions[session_id] = Session(
                session_id=session.session_id,
                identity_id=session.identity_id,
                started_at=session.started_at,
                active=False,
            )
        self._logger.info("identity.session_ended", extra={"context": {"session": session_id}})

    def active_sessions(self) -> tuple[Session, ...]:
        """Return all currently active sessions."""
        with self._lock:
            return tuple(session for session in self._sessions.values() if session.active)
