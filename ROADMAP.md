# JOCHEN X — Roadmap

Zentrale Projektübersicht aller Entwicklungspakete.

---

## Paket 1: Projektgrundlage

| | |
|---|---|
| **Status** | ✅ abgeschlossen |
| **Abhängigkeiten** | keine |

Initiale Projektstruktur, `.gitignore`, `pyproject.toml`, Verzeichnislayout.

**Fertigstellungskriterien:**
- Repository initialisiert
- Build-System konfiguriert (`setuptools`, Python ≥ 3.13)
- Verzeichnisstruktur angelegt

---

## Paket 2: Core Infrastructure und Developer Platform

| | |
|---|---|
| **Status** | ✅ abgeschlossen |
| **Abhängigkeiten** | Paket 1 |

Stabile Kernverträge: `EventBus`, `ServiceRegistry`, `Version`, `VersionManager`, `Extensions`-Protokolle, `LifecycleManager`, `Scheduler`, `Observability`, `Performance`. Optionale Developer Platform mit Inspector und Diagnostics.

**Fertigstellungskriterien:**
- Alle Core-Module implementiert und getestet
- ADR-001 (Core Boundaries), ADR-002 (Event Delivery), ADR-003 (Developer Platform opt-in) akzeptiert
- Developer Platform optional aktivierbar über `developer_enabled`

---

## Paket 3A: Application Foundation

| | |
|---|---|
| **Status** | ✅ abgeschlossen |
| **Abhängigkeiten** | Paket 2 |

`ApplicationHost`, `BootstrapManager` mit deterministischer Phasenfolge, `ApplicationContext`, `ApplicationStateMachine`, DI-Container (`ServiceProvider`), typed Application Events, Konfiguration (`TOML`), SQLite-Datenbank, Logging.

**Fertigstellungskriterien:**
- Bootstrap-Phasen INITIALIZE → LOAD_PLUGINS → LOAD_RESOURCES → FINALIZE vollständig
- `PluginLoader` entdeckt Manifeste ohne Code-Import (ADR-001)
- Alle Foundation-Tests grün

---

## Paket 3B: Security Foundation

| | |
|---|---|
| **Status** | ✅ abgeschlossen |
| **Abhängigkeiten** | Paket 3A |

`SecurityManager`, `SecretVault`, `PermissionManager`, `PluginSecurity`, `AuditLogger`, `ThreatDetector`, `EncryptionService`, `IdentityManager`. Trust-Ledger mit expliziter Zulassung.

**Fertigstellungskriterien:**
- `PluginSecurity.verify_manifest()` funktionsfähig
- Security-Events (`PluginVerified`, `PluginRejected`) implementiert
- Secret-Redaktion in Logs und Diagnostics aktiv

---

## Paket 3C: UI Foundation

| | |
|---|---|
| **Status** | ✅ abgeschlossen |
| **Abhängigkeiten** | Paket 3A |

Navigation-System (`Sidebar`, `Toolbar`, `StatusBar`, `ThemeManager`), `MainWindow`, `LayoutManager`, `ModuleHost`, Dashboard, Chat-UI-Grundgerüst (`ChatPage`, `InputBar`, `ChatBubble`).

**Fertigstellungskriterien:**
- Navigation-Controller mit Seitenregistrierung
- Theme-Umschaltung (System/Light/Dark)
- Hauptfenster mit Sidebar-Navigation startfähig

---

## Paket 4: Plugin SDK

| | |
|---|---|
| **Status** | ✅ abgeschlossen |
| **Abhängigkeiten** | Paket 3A, 3B |

Enterprise Plugin SDK (`sdk/`): Plugin-Basisklassen (`Plugin`, `BackgroundPlugin`, `UIPlugin`, `ToolPlugin`, `WorkflowPlugin`), `PluginRuntime`, `PluginContext`, `PluginContextBuilder`, Facades für Events, Services, Config, Resources, Logging. Eigene Fehler-Hierarchie, unabhängige Versionierung.

**Fertigstellungskriterien:**
- ADR-004 bis ADR-010 dokumentiert
- Alle SDK-Subsysteme unabhängig testbar ohne Foundation
- `sdk/__init__.py` exportiert die gesamte öffentliche API
- `docs/sdk.md` Spezifikation vollständig

---

## Paket 5: SDK-Host-Integration

| | |
|---|---|
| **Status** | 🚧 in Arbeit |
| **Abhängigkeiten** | Paket 4, 3B |

Verbindung des Plugin SDK mit dem Host-Bootstrap. `PluginSecurityStage` (Sicherheitsprüfung vor Code-Import), `PluginActivationStage` (Import, Instanziierung, Context-Wiring, Start), Shutdown-Integration.

**Fertigstellungskriterien:**
- ADR-011 implementiert (aktuell nur dokumentiert)
- `PluginSecurityStage` filtert Manifeste vor Aktivierung
- `PluginActivationStage` erzeugt `PluginRuntime`-Instanzen
- Reverse-Order-Shutdown über `ApplicationHost`
- Erweitertes `plugin.toml`-Schema mit Permissions und Dependencies (ADR-012, noch offen)
- Neue Events: `PLUGIN_ACTIVATING`, `PLUGIN_ACTIVATED`
- Alle bestehenden Tests bleiben grün

---

## Paket 6: Plugin-Manifest-Erweiterung

| | |
|---|---|
| **Status** | 📋 geplant |
| **Abhängigkeiten** | Paket 5 |

Erweiterung von `plugin.toml` um deklarative Felder (`permissions`, `dependencies`, `api_version`, `category`, `name`, `author`, `description`, `entry_point`). Validierung der Code-Metadaten gegen TOML-Deklaration bei Aktivierung.

**Fertigstellungskriterien:**
- ADR-012 akzeptiert
- `PluginLoader` liest erweiterte TOML-Felder
- `PluginActivationStage` validiert Code-Metadaten gegen Manifest
- Offene ADRs 005–007 adressiert (Integrity, Permissions, Dependencies)

---

## Paket 7: Chat-UI und KI-Integration

| | |
|---|---|
| **Status** | 📋 geplant |
| **Abhängigkeiten** | Paket 3C, Paket 5 |

Funktionsfähige Chat-Oberfläche mit KI-Anbindung. `AIGateway`, Konversationsverwaltung, Nachrichtenanzeige, Eingabeverarbeitung.

**Fertigstellungskriterien:**
- Chat-Nachrichtenaustausch über `AIGateway` funktionsfähig
- Konversations-Persistenz in SQLite
- UI reagiert asynchron (kein UI-Thread-Blocking)
