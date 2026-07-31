"""Plugin observability unit tests (WP-09 / AC-8).

Tests verify duration metrics capture and plugin health check reporting.
"""

from __future__ import annotations

import unittest

from core.observability import (
    ActivationFailure,
    Metrics,
    PluginHealthCheck,
    run_health_checks,
)


class TestPluginHealthCheck(unittest.TestCase):
    """Plugin Health Check reports correct status based on lifecycle state (AC-8)."""

    def test_plugin_health_check(self) -> None:
        """STARTED -> Healthy, FAILED -> Unhealthy, STOPPED -> Degraded."""
        check = PluginHealthCheck("test-plugin", lambda: "started")
        status = check.check()
        self.assertTrue(status.healthy)
        self.assertEqual(status.name, "plugin.test-plugin")

        check_failed = PluginHealthCheck("test-plugin", lambda: "failed")
        status_failed = check_failed.check()
        self.assertFalse(status_failed.healthy)

        check_stopped = PluginHealthCheck("test-plugin", lambda: "stopped")
        status_stopped = check_stopped.check()
        self.assertFalse(status_stopped.healthy)
        self.assertIn("degraded", status_stopped.detail)

    def test_health_check_integrates_with_run_health_checks(self) -> None:
        """PluginHealthCheck satisfies the HealthCheck protocol."""
        check = PluginHealthCheck("proto-plugin", lambda: "started")
        results = run_health_checks(check)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].healthy)


class TestActivationDurationMetric(unittest.TestCase):
    """Duration metrics are captured for plugin lifecycle steps (AC-8)."""

    def test_activation_duration_metric(self) -> None:
        """Duration metric is recorded and retrievable via snapshot."""
        metrics = Metrics()

        metrics.record_duration("plugin.activation.duration_ms.test-plugin", 42.5)
        snapshot = metrics.snapshot()
        self.assertIn("plugin.activation.duration_ms.test-plugin", snapshot)
        self.assertAlmostEqual(
            snapshot["plugin.activation.duration_ms.test-plugin"], 42.5,
        )

        metrics.record_duration("plugin.dependency.resolution_ms", 10.0)
        metrics.record_duration("plugin.security.validation_ms.test-plugin", 5.0)
        snapshot = metrics.snapshot()
        self.assertIn("plugin.dependency.resolution_ms", snapshot)
        self.assertIn("plugin.security.validation_ms.test-plugin", snapshot)


class TestActivationFailure(unittest.TestCase):
    """ActivationFailure provides structured failure diagnostics (AC-8)."""

    def test_activation_failure_structure(self) -> None:
        """Failure diagnostic carries plugin_id, phase, reason, context."""
        failure = ActivationFailure(
            plugin_id="broken-plugin",
            phase="activation",
            reason="ImportError: module not found",
            context={"error_type": "ImportError"},
        )
        self.assertEqual(failure.plugin_id, "broken-plugin")
        self.assertEqual(failure.phase, "activation")
        self.assertEqual(failure.reason, "ImportError: module not found")
        self.assertEqual(failure.context["error_type"], "ImportError")


if __name__ == "__main__":
    unittest.main()
