import tempfile
import unittest
from pathlib import Path
from core.events import Event, EventBus
from core.registry import ServiceRegistry
from developer.inspector import ArchitectureInspector
from developer.platform import DeveloperPlatform

class DeveloperPlatformTests(unittest.TestCase):
    def test_disabled_platform_rejects_access(self):
        with self.assertRaises(RuntimeError): DeveloperPlatform().services()
    def test_event_service_log_and_configuration_diagnostics(self):
        events=EventBus(); events.publish(Event("system.started",{}))
        services=ServiceRegistry(); services.register(str,"value")
        with tempfile.TemporaryDirectory() as directory:
            log=Path(directory)/"app.log"; log.write_text("2026-01-01 INFO token=private started",encoding="utf-8")
            platform=DeveloperPlatform(enabled=True,events=events,services=services,log_file=log)
            self.assertEqual(platform.events()[0].name,"system.started")
            self.assertEqual(platform.services()[0].key,"str")
            self.assertIn("<redacted>",platform.logs()[0].message)
            self.assertEqual(platform.configuration({"api_key":"unsafe"}).values["api_key"],"<redacted>")
    def test_architecture_inspector_uses_service_port(self):
        services=ServiceRegistry(); services.register(str,"value")
        self.assertEqual(ArchitectureInspector(services).inspect().services,1)
