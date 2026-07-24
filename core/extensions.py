"""Stable contracts for inert extensions; implementations are host supplied."""

from typing import Protocol


class PluginExtension(Protocol):
    identifier: str


class ToolExtension(Protocol):
    identifier: str


class UIExtension(Protocol):
    identifier: str


class CommandExtension(Protocol):
    identifier: str


class WorkflowExtension(Protocol):
    identifier: str
