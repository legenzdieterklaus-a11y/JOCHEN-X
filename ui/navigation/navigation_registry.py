"""Thread-safe registry for built-in and future plugin navigation modules."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
import logging
from threading import RLock

from ui.navigation.navigation_models import NavigationRegistration


class RegistryChangeAction(StrEnum):
    """Kinds of navigation registry mutation."""

    REGISTERED = "registered"
    UNREGISTERED = "unregistered"


@dataclass(frozen=True, slots=True)
class RegistryChange:
    """Immutable notification describing one registry mutation."""

    action: RegistryChangeAction
    identifier: str


RegistryListener = Callable[[RegistryChange], None]


class NavigationRegistry:
    """Owns navigation registrations without constructing their modules."""

    def __init__(self, logger: logging.Logger | None = None) -> None:
        """Create an empty registry."""
        self._registrations: dict[str, NavigationRegistration] = {}
        self._listeners: list[RegistryListener] = []
        self._logger = logger or logging.getLogger("jochen_x.navigation.registry")
        self._lock = RLock()

    def register(self, registration: NavigationRegistration) -> None:
        """Register a destination.

        Raises:
            ValueError: If the identifier already exists or its parent is unknown.
        """
        self.register_many((registration,))

    def register_many(self, registrations: tuple[NavigationRegistration, ...]) -> None:
        """Atomically register destinations and notify after commit."""
        if not registrations:
            return
        identifiers = tuple(registration.item.identifier for registration in registrations)
        with self._lock:
            if len(set(identifiers)) != len(identifiers):
                raise ValueError("Navigation registration batch contains duplicate identifiers")
            conflicts = tuple(
                identifier for identifier in identifiers if identifier in self._registrations
            )
            if conflicts:
                raise ValueError(
                    f"Navigation items already registered: {', '.join(conflicts)}"
                )
            available = set(self._registrations).union(identifiers)
            missing_parents = tuple(
                registration.item.parent_identifier
                for registration in registrations
                if registration.item.parent_identifier is not None
                and registration.item.parent_identifier not in available
            )
            if missing_parents:
                raise ValueError(
                    f"Navigation parents are not registered: {', '.join(missing_parents)}"
                )
            parent_by_identifier = {
                identifier: registration.item.parent_identifier
                for identifier, registration in self._registrations.items()
            }
            parent_by_identifier.update(
                {
                    registration.item.identifier: registration.item.parent_identifier
                    for registration in registrations
                }
            )
            for identifier in identifiers:
                visited: set[str] = set()
                current: str | None = identifier
                while current is not None:
                    if current in visited:
                        raise ValueError(
                            f"Navigation parent cycle detected at: {current}"
                        )
                    visited.add(current)
                    current = parent_by_identifier.get(current)
            for registration in registrations:
                self._registrations[registration.item.identifier] = registration
            listeners = tuple(self._listeners)
        for identifier in identifiers:
            self._notify(
                RegistryChange(RegistryChangeAction.REGISTERED, identifier),
                listeners,
            )

    def unregister(self, identifier: str) -> NavigationRegistration:
        """Remove and return a destination when no child depends on it."""
        with self._lock:
            if any(
                registration.item.parent_identifier == identifier
                for registration in self._registrations.values()
            ):
                raise ValueError(f"Navigation item still has children: {identifier}")
            try:
                registration = self._registrations.pop(identifier)
            except KeyError as error:
                raise LookupError(f"Navigation item is not registered: {identifier}") from error
            listeners = tuple(self._listeners)
        self._notify(
            RegistryChange(RegistryChangeAction.UNREGISTERED, identifier),
            listeners,
        )
        return registration

    def subscribe(self, listener: RegistryListener) -> Callable[[], None]:
        """Observe registration changes and return an unsubscribe callback."""
        with self._lock:
            self._listeners.append(listener)

        def unsubscribe() -> None:
            with self._lock:
                if listener in self._listeners:
                    self._listeners.remove(listener)

        return unsubscribe

    def _notify(
        self,
        change: RegistryChange,
        listeners: tuple[RegistryListener, ...],
    ) -> None:
        """Notify every observer without invalidating a committed mutation."""
        for listener in listeners:
            try:
                listener(change)
            except Exception as error:
                self._logger.error(
                    "navigation.registry_listener_failed",
                    exc_info=error,
                    extra={
                        "context": {
                            "action": change.action.value,
                            "identifier": change.identifier,
                        }
                    },
                )

    def get(self, identifier: str) -> NavigationRegistration:
        """Return a required registration."""
        with self._lock:
            try:
                return self._registrations[identifier]
            except KeyError as error:
                raise LookupError(f"Navigation item is not registered: {identifier}") from error

    def contains(self, identifier: str) -> bool:
        """Return whether an identifier is registered."""
        with self._lock:
            return identifier in self._registrations

    def registrations(self) -> tuple[NavigationRegistration, ...]:
        """Return all registrations in deterministic presentation order."""
        with self._lock:
            values = tuple(self._registrations.values())
        return tuple(
            sorted(
                values,
                key=lambda registration: (
                    registration.item.group.value,
                    registration.item.order,
                    registration.item.name.casefold(),
                ),
            )
        )

    def children_of(self, identifier: str) -> tuple[NavigationRegistration, ...]:
        """Return the direct children of a destination."""
        return tuple(
            registration
            for registration in self.registrations()
            if registration.item.parent_identifier == identifier
        )

    def __len__(self) -> int:
        """Return the number of registered destinations."""
        with self._lock:
            return len(self._registrations)
