"""Golden Reference Plugin -- governance artifact for plugin contract validation.

Official governance artifact (Milestone 0.9) that validates the fully finalized
plugin contract end-to-end. Serves as SDK Compatibility Verification, Regression
Verification, Bootstrap Pipeline Validation, and Developer Reference.

NOT a sample plugin. Lifecycle validation occurs through
``test_golden_reference_full_lifecycle`` in the test suite and as a release gate.
"""

from __future__ import annotations

from sdk.manifest import PluginCategory, PluginMetadata, PluginPermission
from sdk.plugin import Plugin

__all__ = ["ReferencePlugin"]


class ReferencePlugin(Plugin):
    """Concrete plugin exercising all SDK features and manifest v2 fields."""

    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            identifier="reference",
            name="Golden Reference Plugin",
            version="1.0.0",
            api_version="1.0.0",
            author="JOCHEN X Team",
            description="Governance artifact for end-to-end plugin contract validation",
            category=PluginCategory.DEVELOPER,
            permissions=frozenset({
                PluginPermission.EVENTS_PUBLISH,
                PluginPermission.EVENTS_SUBSCRIBE,
            }),
            minimum_application_version="0.8.0",
            entry_point="reference",
        )

    def on_initialize(self) -> None:
        self.context.logger.info("reference.initialized")

    def on_start(self) -> None:
        self.context.logger.info("reference.started")

    def on_stop(self) -> None:
        self.context.logger.info("reference.stopped")

    def on_shutdown(self) -> None:
        self.context.logger.info("reference.shutdown")
