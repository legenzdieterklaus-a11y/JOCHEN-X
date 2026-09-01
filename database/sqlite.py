"""SQLite connection, migration, and settings repository."""

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from core.exceptions import DatabaseError


@dataclass(frozen=True, slots=True)
class MonitoringState:
    """Immutable snapshot of one monitored subject's state."""

    host_id: str
    subject: str
    status: str
    first_seen: str
    last_seen: str | None
    since: str
    transitions: int


class ConnectionManager:
    """Creates short-lived SQLite connections with foreign-key enforcement."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def connect(self) -> sqlite3.Connection:
        """Open a configured connection."""
        connection: sqlite3.Connection | None = None
        try:
            connection = sqlite3.connect(self.path)
            connection.execute("PRAGMA foreign_keys = ON")
            return connection
        except sqlite3.Error as error:
            if connection is not None:
                connection.close()
            raise DatabaseError(str(error)) from error


class MigrationManager:
    """Applies the fixed foundation schema exactly once."""

    CURRENT_VERSION = 1

    def __init__(self, connections: ConnectionManager) -> None:
        self._connections = connections

    def migrate(self) -> None:
        """Create the allowed schema-version and settings tables."""
        connection = self._connections.connect()
        try:
            with connection:
                connection.execute(
                    "CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL)"
                )
                row = connection.execute("SELECT version FROM schema_version LIMIT 1").fetchone()
                if row is None:
                    connection.execute(
                        "INSERT INTO schema_version(version) VALUES (?)", (self.CURRENT_VERSION,)
                    )
                elif row[0] != self.CURRENT_VERSION:
                    raise DatabaseError(f"Unsupported schema version: {row[0]}")
                connection.execute(
                    "CREATE TABLE IF NOT EXISTS settings "
                    "(key TEXT PRIMARY KEY, value TEXT NOT NULL)"
                )
                connection.execute(
                    "CREATE TABLE IF NOT EXISTS monitoring_state "
                    "(host_id TEXT NOT NULL, subject TEXT NOT NULL, "
                    "status TEXT NOT NULL, first_seen TEXT NOT NULL, "
                    "last_seen TEXT, since TEXT NOT NULL, "
                    "transitions INTEGER NOT NULL DEFAULT 0, "
                    "PRIMARY KEY (host_id, subject))"
                )
        finally:
            connection.close()


class SettingsRepository:
    """Persists application settings in the sole business-data table."""

    def __init__(self, connections: ConnectionManager) -> None:
        self._connections = connections

    def get(self, key: str) -> str | None:
        """Return a value or `None` when it has not been saved."""
        connection = self._connections.connect()
        try:
            row = connection.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        finally:
            connection.close()
        return None if row is None else str(row[0])

    def set(self, key: str, value: str) -> None:
        """Atomically insert or update a setting."""
        connection = self._connections.connect()
        try:
            with connection:
                connection.execute(
                    "INSERT INTO settings(key, value) VALUES (?, ?) "
                    "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                    (key, value),
                )
        finally:
            connection.close()


class MonitoringStateRepository:
    """Persists monitoring state snapshots keyed by host and subject."""

    def __init__(self, connections: ConnectionManager) -> None:
        self._connections = connections

    def upsert(self, state: MonitoringState) -> None:
        """Insert or update a monitoring state record."""
        connection = self._connections.connect()
        try:
            with connection:
                connection.execute(
                    "INSERT INTO monitoring_state"
                    "(host_id, subject, status, first_seen, last_seen, since, transitions) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?) "
                    "ON CONFLICT(host_id, subject) DO UPDATE SET "
                    "status=excluded.status, last_seen=excluded.last_seen, "
                    "since=excluded.since, transitions=excluded.transitions",
                    (state.host_id, state.subject, state.status,
                     state.first_seen, state.last_seen, state.since,
                     state.transitions),
                )
        finally:
            connection.close()

    def all(self) -> tuple[MonitoringState, ...]:
        """Return every persisted monitoring state."""
        connection = self._connections.connect()
        try:
            rows = connection.execute(
                "SELECT host_id, subject, status, first_seen, last_seen, "
                "since, transitions FROM monitoring_state "
                "ORDER BY host_id, subject"
            ).fetchall()
        finally:
            connection.close()
        return tuple(MonitoringState(*row) for row in rows)

    def for_host(self, host_id: str) -> tuple[MonitoringState, ...]:
        """Return monitoring states for a single host."""
        connection = self._connections.connect()
        try:
            rows = connection.execute(
                "SELECT host_id, subject, status, first_seen, last_seen, "
                "since, transitions FROM monitoring_state "
                "WHERE host_id = ? ORDER BY subject",
                (host_id,),
            ).fetchall()
        finally:
            connection.close()
        return tuple(MonitoringState(*row) for row in rows)
