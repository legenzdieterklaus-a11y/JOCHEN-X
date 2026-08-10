"""Test-only hooks for tracking plugin lifecycle calls in tests."""

from __future__ import annotations

STOP_ORDER: list[str] = []
SHUTDOWN_ORDER: list[str] = []
