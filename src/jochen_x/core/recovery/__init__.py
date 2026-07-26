"""Recovery subsystem for the JOCHEN X Core Runtime.

Provides multi-level error recovery with automatic escalation,
circuit-breaker semantics, and full audit integration.
"""

from jochen_x.core.recovery.handler import RecoveryHandler
from jochen_x.core.recovery.levels import (
    RecoveryLevelConfig,
    RecoveryLevelRegistry,
)
from jochen_x.core.recovery.strategy import (
    ComponentRestartStrategy,
    ComponentRetryStrategy,
    IRecoveryStrategy,
    RuntimeRestartStrategy,
    ServiceRestartStrategy,
)

__all__ = [
    "ComponentRestartStrategy",
    "ComponentRetryStrategy",
    "IRecoveryStrategy",
    "RecoveryHandler",
    "RecoveryLevelConfig",
    "RecoveryLevelRegistry",
    "RuntimeRestartStrategy",
    "ServiceRestartStrategy",
]
