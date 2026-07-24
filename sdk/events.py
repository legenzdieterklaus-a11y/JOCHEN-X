"""SDK event API.

Plugins interact with the shared JOCHEN X event bus only through this
module. The SDK exposes:

* :class:`PluginEvent` – a plain, plugin-facing event value type;
* :class:`PluginEventBus` – a scoped helper offering ``subscribe``,
  ``unsubscribe`` and ``publish`` without exposing the underlying
  :class:`core.events.EventBus` type; and
* :class:`Subscription` – an opaque handle returned by ``subscribe`` that
  the plugin can pass to :meth:`PluginEventBus.unsubscribe` (or dispose of
  directly).

The wrapper adapts between the plugin-facing :class:`PluginEvent` value
type and the transport-neutral event contract accepted by the foundation
bus, so plugin authors never import framework-internal event types.
Publishing and subscription can also be gated on declared permissions.
"""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from threading import RLock
from typing import Any, Protocol, runtime_checkable

from sdk.errors import PluginEventError, PluginPermissionError
from sdk.manifest import PluginPermission


@dataclass(frozen=True, slots=True)
class PluginEvent:
    """Immutable, plugin-facing event value type.

    Attributes:
        name: Stable, dotted event name (glob patterns are allowed on the
            subscription side, not on published events).
        payload: JSON-friendly, immutable-in-intent payload dictionary.
    """

    name: str
    payload: dict[str, Any]


PluginEventHandler = Callable[[PluginEvent], None | Awaitable[None]]
"""Callable invoked by :class:`PluginEventBus` when an event matches."""


@runtime_checkable
class EventBusPort(Protocol):
    """Narrow port satisfied structurally by :class:`core.events.EventBus`.

    The port only lists the methods the SDK actually calls; hosts can pass
    the foundation :class:`core.events.EventBus` directly because its public
    surface matches this protocol.
    """

    def subscribe(
        self,
        event_name: str,
        handler: Callable[[Any], Any],
        *,
        priority: int = 0,
        receive_sticky: bool = True,
    ) -> Callable[[], None]:
        """Register ``handler`` for events matching ``event_name``."""
        ...

    def publish(self, event: Any, *, sticky: bool = False) -> None:
        """Publish an event to synchronous subscribers."""
        ...


@runtime_checkable
class _BusEventProtocol(Protocol):
    """Structural view of the transport-neutral ``Event`` value type."""

    name: str
    payload: dict[str, Any]


PermissionCheck = Callable[[PluginPermission], None]
"""Callable that raises :class:`PluginPermissionError` when denied."""


class Subscription:
    """Opaque handle representing a live plugin event subscription.

    The handle owns the raw unsubscribe callable returned by the underlying
    bus. Disposal is idempotent.
    """

    __slots__ = ("_dispose", "_disposed", "_event_name", "_lock")

    def __init__(self, event_name: str, dispose: Callable[[], None]) -> None:
        self._event_name = event_name
        self._dispose = dispose
        self._disposed = False
        self._lock = RLock()

    @property
    def event_name(self) -> str:
        """Return the subscribed event name or glob pattern."""
        return self._event_name

    @property
    def is_active(self) -> bool:
        """Return whether the subscription is still live."""
        with self._lock:
            return not self._disposed

    def unsubscribe(self) -> None:
        """Dispose of the subscription; safe to call multiple times."""
        with self._lock:
            if self._disposed:
                return
            self._disposed = True
        try:
            self._dispose()
        except Exception as error:  # translate any bus error to SDK error
            raise PluginEventError(
                f"Failed to unsubscribe from {self._event_name!r}: {error}"
            ) from error


class PluginEventBus:
    """Plugin-scoped event bus wrapper.

    All events are converted to and from the transport-neutral event value
    type used by the underlying bus. Permission enforcement is delegated to
    the injected :class:`PermissionCheck` callable so this module contains
    no policy of its own.
    """

    __slots__ = ("_bus", "_event_type", "_permission_check", "_plugin_id", "_subscriptions", "_lock")

    def __init__(
        self,
        plugin_id: str,
        bus: EventBusPort,
        *,
        event_type: type,
        permission_check: PermissionCheck | None = None,
    ) -> None:
        """Create the plugin event bus.

        Args:
            plugin_id: The owning plugin identifier.
            bus: The underlying event bus, satisfying :class:`EventBusPort`.
            event_type: The transport-neutral event class used by ``bus``
                (typically ``core.events.Event``). It is injected at
                construction time so this SDK module has no import-time
                dependency on the foundation event type.
            permission_check: Optional callable invoked before publishing or
                subscribing. Raises :class:`PluginPermissionError` on denial.
        """
        if not plugin_id:
            raise ValueError("plugin_id must be a non-empty string")
        if bus is None:
            raise ValueError("bus is required")
        if event_type is None:
            raise ValueError("event_type is required")
        self._plugin_id = plugin_id
        self._bus = bus
        self._event_type = event_type
        self._permission_check = permission_check
        self._subscriptions: list[Subscription] = []
        self._lock = RLock()

    @property
    def plugin_id(self) -> str:
        """Return the owning plugin identifier."""
        return self._plugin_id

    def subscribe(
        self,
        event_name: str,
        handler: PluginEventHandler,
        *,
        priority: int = 0,
        receive_sticky: bool = True,
    ) -> Subscription:
        """Register ``handler`` for events matching ``event_name``.

        Args:
            event_name: Exact event name or ``fnmatch`` glob pattern.
            handler: Callable receiving a :class:`PluginEvent`. Async
                handlers are supported for use with async publishing.
            priority: Delivery priority; higher priorities run first.
            receive_sticky: Whether to receive currently sticky events.

        Returns:
            An opaque :class:`Subscription` handle.

        Raises:
            PluginEventError: If ``event_name`` is empty or ``handler`` is
                not callable.
            PluginPermissionError: If a permission check is configured and
                the plugin lacks ``events.subscribe``.
        """
        self._ensure_permission(PluginPermission.EVENTS_SUBSCRIBE)
        self._validate_event_name(event_name)
        if not callable(handler):
            raise PluginEventError("handler must be callable")

        async_handler = inspect.iscoroutinefunction(handler)

        def adapter(event: Any) -> Any:
            plugin_event = self._to_plugin_event(event)
            result = handler(plugin_event)
            return result

        try:
            dispose = self._bus.subscribe(
                event_name,
                adapter,
                priority=priority,
                receive_sticky=receive_sticky and not async_handler,
            )
        except Exception as error:
            raise PluginEventError(
                f"Failed to subscribe to {event_name!r}: {error}"
            ) from error
        subscription = Subscription(event_name, dispose)
        with self._lock:
            self._subscriptions.append(subscription)
        return subscription

    def unsubscribe(self, subscription: Subscription) -> None:
        """Dispose of ``subscription`` and forget its bookkeeping."""
        if not isinstance(subscription, Subscription):
            raise PluginEventError("subscription must be a Subscription instance")
        subscription.unsubscribe()
        with self._lock:
            try:
                self._subscriptions.remove(subscription)
            except ValueError:
                pass

    def publish(
        self,
        event_name: str,
        payload: dict[str, Any] | None = None,
        *,
        sticky: bool = False,
    ) -> None:
        """Publish an event to the shared bus.

        Args:
            event_name: Stable, dotted event name (glob patterns rejected).
            payload: JSON-friendly payload; ``None`` publishes an empty
                payload.
            sticky: When ``True``, the event is retained for late
                subscribers.

        Raises:
            PluginEventError: If the event name is invalid or the bus
                rejects the publish.
            PluginPermissionError: If a permission check is configured and
                the plugin lacks ``events.publish``.
        """
        self._ensure_permission(PluginPermission.EVENTS_PUBLISH)
        self._validate_event_name(event_name)
        if any(character in event_name for character in "*?["):
            raise PluginEventError(
                f"Event name must not contain glob wildcards: {event_name!r}"
            )
        resolved_payload: dict[str, Any] = dict(payload or {})
        resolved_payload.setdefault("plugin", self._plugin_id)
        try:
            self._bus.publish(
                self._event_type(event_name, resolved_payload), sticky=sticky
            )
        except Exception as error:
            raise PluginEventError(
                f"Failed to publish {event_name!r}: {error}"
            ) from error

    def dispose(self) -> None:
        """Dispose every live subscription owned by this wrapper."""
        with self._lock:
            subscriptions = tuple(self._subscriptions)
            self._subscriptions.clear()
        for subscription in subscriptions:
            try:
                subscription.unsubscribe()
            except PluginEventError:
                # Best-effort disposal; a broken unsubscribe must not stop
                # cleanup of the remaining handles.
                continue

    def active_subscriptions(self) -> tuple[Subscription, ...]:
        """Return a snapshot of currently active subscriptions."""
        with self._lock:
            return tuple(item for item in self._subscriptions if item.is_active)

    def _ensure_permission(self, permission: PluginPermission) -> None:
        """Delegate to the injected permission check when configured."""
        if self._permission_check is None:
            return
        try:
            self._permission_check(permission)
        except PluginPermissionError:
            raise
        except Exception as error:  # normalise unexpected errors
            raise PluginPermissionError(
                f"Permission check failed for {permission.value!r}: {error}"
            ) from error

    def _validate_event_name(self, event_name: str) -> None:
        """Reject empty or non-string event names."""
        if not isinstance(event_name, str) or not event_name:
            raise PluginEventError("event_name must be a non-empty string")

    def _to_plugin_event(self, event: Any) -> PluginEvent:
        """Adapt a transport-neutral event to :class:`PluginEvent`."""
        name = getattr(event, "name", None)
        payload = getattr(event, "payload", None)
        if not isinstance(name, str) or not isinstance(payload, dict):
            raise PluginEventError(
                "Underlying event does not expose the expected name/payload shape"
            )
        return PluginEvent(name=name, payload=dict(payload))


__all__ = [
    "EventBusPort",
    "PermissionCheck",
    "PluginEvent",
    "PluginEventBus",
    "PluginEventHandler",
    "Subscription",
]
