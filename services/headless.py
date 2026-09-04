"""Headless bootstrap composition — core without a window.

Composes the same foundation as :func:`ui.navigation.navigation_service.
create_desktop_bootstrap_manager` minus the navigation stage, producing a
bootstrap manager suitable for unattended operation in session 0.
"""

from __future__ import annotations

from app.bootstrap import BootstrapManager, DependencyInjectionStage, default_stages
from app.security.security_manager import SecurityBootstrapStage
from services.monitoring import MonitoringBootstrapStage

__all__ = ["create_headless_bootstrap_manager"]


def create_headless_bootstrap_manager() -> BootstrapManager:
    """Return a bootstrap manager for headless (no-window) operation.

    The composition mirrors :func:`create_desktop_bootstrap_manager` with one
    difference: :class:`NavigationBootstrapStage` is omitted because no display
    is available.  Monitoring and Security stages are included so that
    persistence and the plugin pipeline function identically to the desktop
    path.
    """
    stages = default_stages()
    without_di = tuple(
        stage for stage in stages
        if not isinstance(stage, DependencyInjectionStage)
    )
    return BootstrapManager(
        stages=(
            *without_di,
            MonitoringBootstrapStage(),
            SecurityBootstrapStage(),
            DependencyInjectionStage(),
        )
    )
