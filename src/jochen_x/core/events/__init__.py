"""EventBus subsystem for typed, asynchronous event distribution.

Re-exports the public API of the events package.
"""

from __future__ import annotations

from jochen_x.core.events.bus import EventBus
from jochen_x.core.events.handler import HandlerEntry, HandlerRegistry
from jochen_x.core.events.types import EventBusError, EventPublishError

__all__ = [
    "EventBus",
    "EventBusError",
    "EventPublishError",
    "HandlerEntry",
    "HandlerRegistry",
]
