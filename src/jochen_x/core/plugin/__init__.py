"""Plugin infrastructure for JOCHEN X Core Runtime.

Provides isolated plugin contexts, lifecycle management, and
sandboxed execution to ensure that plugins interact with the
runtime exclusively through defined interfaces and that errors
in one plugin never affect others.
"""

from jochen_x.core.plugin.context import PluginContext
from jochen_x.core.plugin.registry import IPlugin, PluginRegistry, PluginState
from jochen_x.core.plugin.sandbox import PluginSandbox

__all__ = [
    "IPlugin",
    "PluginContext",
    "PluginRegistry",
    "PluginSandbox",
    "PluginState",
]
