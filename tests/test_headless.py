"""Tests for the headless bootstrap composition."""

from __future__ import annotations

import pytest

from app.bootstrap import (
    BootstrapManager,
    DependencyInjectionStage,
    default_stages,
)
from app.security.security_manager import SecurityBootstrapStage
from services.headless import create_headless_bootstrap_manager
from services.monitoring import MonitoringBootstrapStage


class TestCreateHeadlessBootstrapManager:

    def test_returns_bootstrap_manager(self) -> None:
        manager = create_headless_bootstrap_manager()
        assert isinstance(manager, BootstrapManager)

    def test_contains_monitoring_stage(self) -> None:
        manager = create_headless_bootstrap_manager()
        types = [type(s) for s in manager.stages]
        assert MonitoringBootstrapStage in types

    def test_contains_security_stage(self) -> None:
        manager = create_headless_bootstrap_manager()
        types = [type(s) for s in manager.stages]
        assert SecurityBootstrapStage in types

    def test_no_navigation_stage(self) -> None:
        manager = create_headless_bootstrap_manager()
        names = [s.name for s in manager.stages]
        assert "navigation" not in names

    def test_dependency_injection_is_last(self) -> None:
        manager = create_headless_bootstrap_manager()
        last = manager.stages[-1]
        assert isinstance(last, DependencyInjectionStage)

    def test_contains_all_default_stages_except_di(self) -> None:
        manager = create_headless_bootstrap_manager()
        headless_names = [s.name for s in manager.stages]
        for stage in default_stages():
            if isinstance(stage, DependencyInjectionStage):
                continue
            assert stage.name in headless_names

    def test_stage_count(self) -> None:
        manager = create_headless_bootstrap_manager()
        default_count = len(default_stages())
        assert len(manager.stages) == default_count + 2
