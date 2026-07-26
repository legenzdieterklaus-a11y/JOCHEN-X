# JOCHEN X — Architecture Book v2.0

> **Status:** APPROVED / FROZEN (v2.0) — 2026-07-26  
> **Verbindliche Architekturreferenz:** Dieses Dokument ist die maßgebliche Architekturreferenz für JOCHEN X.  
> **Änderungsregel:** Keine inhaltlichen Änderungen an v2.0. Anpassungen erfolgen ausschließlich über neue Dokumentversionen (z. B. v2.1 oder v3.0) und dokumentierte ADRs.  
> **Git-Tags:** `architecture-book-v2.0`, `core-runtime-v1.0.0`

---

## Deckblatt

| Feld | Wert |
|------|------|
| **Projekt** | JOCHEN X |
| **Dokumentversion** | 2.0 |
| **Architecture Freeze Version** | Core Runtime v1.0.0 |
| **Erstellungsdatum** | 2026-07-26 |
| **Autor** | Principal Software Architect |
| **Applikationsversion** | 0.7.0 |
| **SDK-Version** | 0.7.1 |
| **SDK-API-Version** | 1.0.0 |
| **Python-Version** | >= 3.13 |
| **Externe Abhängigkeit** | PySide6 >= 6.8 |

### Änderungshistorie

| Version | Datum | Beschreibung |
|---------|-------|--------------|
| 1.0 | — | Initiales Architecture Book (nicht formalisiert) |
| 2.0 | 2026-07-26 | Vollständige Neufassung auf Basis Architecture Freeze v1.0.0 |

---

## Inhaltsverzeichnis

1. Executive Summary
2. Projektübersicht
3. Architekturprinzipien
4. Gesamtarchitektur
5. Schichtenmodell
6. Komponentenbeschreibung
7. Runtime Host
8. Dependency Injection
9. Event Bus
10. Plugin-System
11. Security
12. Recovery
13. Observability
14. Concurrency
15. Interfaces
16. Exception-Modell
17. Konfigurationsmodell
18. Testarchitektur
19. Erweiterungsleitfaden
20. Architecture Decision Records
21. Zukunftsroadmap
22. Architecture Freeze
23. Glossar
24. Anhang

---

## 1. Executive Summary

### 1.1 Projektziel

JOCHEN X ist ein modularer, lokaler KI-Assistent nach dem JARVIS-Prinzip. Das Projekt implementiert ein PySide6-basiertes Desktop-Framework, das als erweiterbare Plattform für KI-gestützte Produktivitätswerkzeuge dient.

### 1.2 Vision

Eine vollständig lokale, datenschutzfreundliche Assistenz-Plattform, die durch ein Plugin-System beliebig erweiterbar ist — von Trading-Analyse über KI-gestützte Texterstellung bis hin zu Multi-Agent-Systemen — ohne Abhängigkeit von Cloud-Diensten für den Kernbetrieb.

### 1.3 Anwendungsgebiet

- Lokaler Desktop-Assistent mit KI-Integration
- Erweiterbare Plattform über ein typsicheres Plugin-System
- Modular aufgebaute Runtime mit determinischem Bootstrap
- Sicherheitsgehärtete Architektur mit Zero-Trust-Prinzip für Plugins

### 1.4 Designphilosophie

Das System folgt dem Prinzip der **kontrollierten Komplexität**: Jede Schicht hat eine klar definierte Verantwortung, kommuniziert ausschließlich über definierte Verträge (Protocols) und wird durch Dependency Injection komponiert. Die Architektur bevorzugt explizite Konstruktion vor implizitem Verhalten, Immutabilität vor Veränderlichkeit und Ports vor konkreten Implementierungen.

### 1.5 Architekturprinzipien (Kurzfassung)

1. **Clean Architecture** — Abhängigkeiten zeigen nach innen
2. **Composition Root** — Ein einziger Kompositionspunkt (`ApplicationHost`)
3. **Plugin First** — Plugins sind Bürger erster Klasse
4. **Security First** — Zero Trust für alle externen Eingaben
5. **Recovery First** — Jede Komponente muss Fehler überstehen
6. **Event Driven** — Lose Kopplung durch typisierte Events
7. **Thread Safety** — Jeder mutable State unter `RLock`

---

## 2. Projektübersicht

### 2.1 Was ist JOCHEN X?

JOCHEN X ist ein Desktop-Framework, das eine deterministische, phasenbasierte Runtime bereitstellt. Die Core Runtime startet Services in einer definierten Reihenfolge, verwaltet deren Lebenszyklus und stellt eine Plugin-Infrastruktur bereit, über die Drittanbieter-Code sicher integriert werden kann.

### 2.2 Welches Problem löst das Projekt?

Bestehende Desktop-Assistenten sind entweder:
- Monolithisch und nicht erweiterbar
- Cloud-abhängig und datenschutzproblematisch
- Ohne formale Sicherheitsgrenze für Erweiterungen

JOCHEN X löst diese Probleme durch eine geschichtete Architektur mit expliziten Trust Boundaries, einem manifest-only Plugin-Discovery-Mechanismus und einer lokalen AI-Gateway-Abstraktion.

### 2.3 Welche Ziele verfolgt es?

- Deterministische, reproduzierbare Bootstrap-Sequenz
- Sichere Plugin-Isolation ohne Prozess-Overhead
- Provider-unabhängige KI-Integration
- Lokaler Betrieb ohne Cloud-Pflicht
- Langfristige Wartbarkeit durch strikte Schichtentrennung

### 2.4 Funktionen der Core Runtime

| Funktion | Implementierung |
|----------|----------------|
| Phasenbasierter Bootstrap | `BootstrapManager` mit 4 Phasen, 11 Default-Stages + optionale Stages |
| State Machine | 10-State `ApplicationStateMachine` mit expliziter Übergangstabelle |
| Dependency Injection | `ServiceRegistry` mit Singleton/Transient/Scoped Lifetimes |
| Event-System | `EventBus` mit Glob-Patterns, Prioritäten, Sticky Events |
| Plugin-Discovery | Manifest-only über `PluginLoader` (kein Code-Import) |
| Security | Capability-basiert mit Trust Ledger und Audit |
| Concurrency | `WorkerPool` mit Cooperative Cancellation |
| Observability | Health Checks, Metrics, Structured Logging |
| Recovery | Graceful Degradation über `ShutdownSequence` |
| Theme-System | Token-basiertes Theming mit Light/Dark-Unterstützung |

### 2.5 Zukünftige Ausbaustufen

| Paket | Status | Inhalt |
|-------|--------|--------|
| SDK-Host-Integration (v0.8.0) | In Arbeit | `PluginSecurityStage`, `PluginActivationStage` |
| Plugin-Manifest-Erweiterung | Geplant | Erweiterte `plugin.toml`-Schema |
| Chat-UI und KI-Integration | Geplant | AI Gateway, Conversation Management |
| Trading Foundation | Zukunft | Broker-Anbindung, Marktdaten |
| AI Foundation | Zukunft | Multi-Provider, Streaming, Tool Calling |

---

## 3. Architekturprinzipien

### 3.1 Clean Architecture

Abhängigkeiten zeigen ausschließlich nach innen. Die äußeren Schichten (UI, Services) dürfen innere Schichten (Core, App) importieren, aber niemals umgekehrt. Core hat keine Abhängigkeit auf App, SDK, UI oder Services.

```
Datei: core/ (keine Imports aus app/, sdk/, ui/, services/, developer/)
Datei: app/ (importiert aus core/, config/, database/, styles/, plugins/)
Datei: sdk/ (importiert ausschließlich innerhalb sdk/)
Datei: ui/ (importiert aus core/, app/, config/, styles/, plugins/)
```

### 3.2 SOLID

- **Single Responsibility**: Jede Klasse hat genau eine Verantwortung (z.B. `EventBus` = Event-Verteilung, `ServiceRegistry` = Service-Auflösung)
- **Open/Closed**: Erweiterung über Protocols und Events statt Modifikation bestehender Klassen
- **Liskov Substitution**: Alle Plugin-Basisklassen (`Plugin`, `BackgroundPlugin`, `UIPlugin`, `ToolPlugin`, `WorkflowPlugin`) sind korrekt substituierbar
- **Interface Segregation**: Minimale Protocols (z.B. `HealthCheck` hat nur `check() -> HealthStatus`)
- **Dependency Inversion**: Hoch-Level-Module hängen von Abstraktionen ab (`EventPublisher` Protocol, `SecretProvider` Protocol)

### 3.3 Dependency Inversion

Konkrete Implementierungen werden niemals direkt referenziert. Alle Abhängigkeiten laufen über:
- `typing.Protocol` für strukturelle Subtypisierung
- `ServiceRegistry` für Laufzeitauflösung
- `EventBus` für lose gekoppelte Kommunikation

### 3.4 Composition Root

Der `ApplicationHost` ist der einzige Ort, an dem alle Abhängigkeiten zusammengeführt werden. Keine Klasse konstruiert ihre eigenen Abhängigkeiten — alle werden über den Bootstrap injiziert.

```
Datei: app/application_host.py
Klasse: ApplicationHost
Methode: start() -> delegiert an StartupSequence -> delegiert an BootstrapManager
```

### 3.5 Ports & Adapters

Das System definiert Ports (Protocols) in den inneren Schichten und Adapter (Implementierungen) in den äußeren:

| Port (Protocol) | Schicht | Adapter | Schicht |
|-----------------|---------|---------|---------|
| `HealthCheck` | Core | Diverse Komponenten | App, Services |
| `SecretProvider` | Services | `SecretManager` | Services |
| `GameModeDetector` | Services | — (zukünftig) | — |
| `EventPublisher` | App | `EventBus` | Core |
| `ResourceMonitor` | Core | `PerformanceMonitor` | Services |
| `BootstrapStage` | App | 11 Default-Stages + optionale Stages | App |
| `EventBusPort` | SDK | `EventBus`-Adapter | SDK/App |
| `PluginConfigStorage` | SDK | `FilePluginConfigStorage` | SDK |

### 3.6 Dependency Injection

Die DI-Implementierung besteht aus:
- `ServiceRegistry` (Core): Container mit Lifetime-Management
- `ServiceProvider` (App): Read-only Facade für Konsumenten
- `DisposableRegistry` (App): LIFO-Cleanup für Ressourcen
- `ServiceScope` (Core): Scoped Lifetime Boundary

### 3.7 Event Driven Architecture

Lose Kopplung wird durch den `EventBus` erreicht:
- Publisher kennen ihre Subscriber nicht
- Events sind frozen Dataclasses (immutabel)
- Delivery erfolgt synchron für deterministische Reihenfolge
- Glob-Patterns ermöglichen flexible Subscription (`"app.*"`)
- Sticky Events bewahren den letzten Zustand für späte Subscriber

### 3.8 Thread Safety

Jede mutable Datenstruktur ist durch `threading.RLock` geschützt. Alle Domänenmodelle sind frozen Dataclasses (inherent thread-safe). Qt-Thread-Marshalling erfolgt über `UiDispatcher` mit Queued Connections.

Betroffene Komponenten (vollständige Liste):
- `EventBus`, `ServiceRegistry`, `LifecycleManager`, `ApplicationStateMachine`
- `WorkerPool`, `CancellationToken`, `TaskHandle`
- `SecretVault`, `PermissionManager`, `IdentityManager`, `AuditLogger`
- `ApiKeyManager`, `BrokerSecurity`, `PluginSecurity`, `BackupManager`
- `ThreatDetector`, `NavigationRegistry`

### 3.9 Security First

- Zero Trust für Plugin-Code: Kein Plugin wird ohne Sicherheitsprüfung aktiviert
- Default Deny: Ohne explizite Permission kein Zugriff
- Capability-basiert: Plugins deklarieren benötigte Permissions im Manifest
- Audit: Jede sicherheitsrelevante Aktion wird protokolliert
- Encryption-at-Rest: Secrets werden verschlüsselt gespeichert
- Threat Detection: Automatische Erkennung von Brute-Force-Mustern

### 3.10 Recovery First

- Graceful Shutdown: Deterministische Reverse-Order-Deallokation
- Worker Timeout: Cooperative Cancellation mit konfigurierbarem Timeout
- Error Classification: `CentralErrorHandler` klassifiziert nach Severity
- Fatal Escalation: Nicht-behandelbare Fehler führen zu kontrolliertem Shutdown
- Bootstrap Rollback: Bei Fehler in einer Stage werden bereits gestartete Module zurückgerollt

### 3.11 Plugin First

- Plugins sind architektonisch als Erweiterungspunkt vorgesehen
- Die Core Runtime existiert, um Plugins zu hosten
- Das SDK ist die einzige öffentliche API für Plugin-Autoren
- Plugin-Discovery erfolgt manifest-only (kein Code-Import durch die Foundation)
- Jeder Plugin erhält einen isolierten `PluginContext`

### 3.12 Testbarkeit

- Keine Singletons, kein globaler State
- Alle Abhängigkeiten über Constructor Injection
- Protocols ermöglichen Mocking ohne Monkey-Patching
- Tests benötigen keinen Qt Event Loop (außer UI-Tests)
- Frozen Dataclasses sind deterministisch vergleichbar

### 3.13 Erweiterbarkeit

- Neue Services: Via `ServiceRegistry.register_factory()`
- Neue Events: Neues frozen Dataclass + `EventBus.publish()`
- Neue Plugins: Implementierung einer SDK-Basisklasse
- Neue Bootstrap Stages: Implementierung des `BootstrapStage` Protocol
- Neue UI-Module: Registrierung in `NavigationRegistry`

---

## 4. Gesamtarchitektur

### 4.1 Architekturdiagramm

```
┌─────────────────────────────────────────────────────────────────────┐
│                              UI Layer                                │
│  ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌─────────┐ ┌───────────┐  │
│  │MainWindow│ │ Sidebar │ │ Toolbar  │ │ChatPage │ │ Dashboard │  │
│  └────┬─────┘ └────┬────┘ └────┬─────┘ └────┬────┘ └─────┬─────┘  │
│       │             │           │             │             │        │
│  ┌────┴─────────────┴───────────┴─────────────┴─────────────┴────┐  │
│  │              Navigation Framework                              │  │
│  │  NavigationRegistry · NavigationService · NavigationController │  │
│  │  ModuleHost · LayoutManager · ThemeManager · WindowState       │  │
│  └────────────────────────────────┬──────────────────────────────┘  │
└───────────────────────────────────┼─────────────────────────────────┘
                                    │
┌───────────────────────────────────┼─────────────────────────────────┐
│                          Developer Layer                             │
│  ┌──────────────────┐  ┌─────────────────────┐  ┌───────────────┐  │
│  │DeveloperPlatform │  │ArchitectureInspector│  │  Diagnostics  │  │
│  └────────┬─────────┘  └──────────┬──────────┘  └───────┬───────┘  │
└───────────┼────────────────────────┼─────────────────────┼──────────┘
            │                        │                     │
┌───────────┼────────────────────────┼─────────────────────┼──────────┐
│           │              Services Layer                   │          │
│  ┌────────┴────────┐  ┌───────────┴──────────┐  ┌───────┴───────┐  │
│  │PerformanceMonitor│  │   Security Services  │  │  AI Gateway   │  │
│  │  MetricsSnapshot │  │ CapabilityModel      │  │ProviderRegistry│ │
│  └─────────────────┘  │ PermissionLayer      │  │ RoutingEngine │  │
│                        │ AuditHooks           │  └───────────────┘  │
│                        └─────────────────────┘                      │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
┌─────────────────────────────────┼───────────────────────────────────┐
│                         SDK Layer                                    │
│  ┌──────────┐ ┌──────────────┐ ┌─────────────┐ ┌───────────────┐   │
│  │  Plugin  │ │PluginContext │ │PluginRuntime│ │PluginEventBus │   │
│  │  UIPlugin│ │PluginConfig  │ │PluginLogger │ │PluginServices │   │
│  │  ToolPlug│ │PluginResources│└─────────────┘ └───────────────┘   │
│  └──────────┘ └──────────────┘                                      │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
┌─────────────────────────────────┼───────────────────────────────────┐
│                       Plugins Layer                                  │
│  ┌──────────────┐  ┌──────────────────┐  ┌─────────────────────┐   │
│  │ PluginLoader │  │  PluginCatalog   │  │ PluginDiscoveryStage│   │
│  └──────────────┘  └──────────────────┘  └─────────────────────┘   │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
┌─────────────────────────────────┼───────────────────────────────────┐
│                          App Layer                                   │
│  ┌───────────────┐  ┌────────────────┐  ┌─────────────────────────┐│
│  │ApplicationHost│  │BootstrapManager│  │   ApplicationContext    ││
│  │StartupSequence│  │ 11+opt Stages  │  │   RuntimeState          ││
│  │ShutdownSequence│ │BootstrapContext│  │   ServiceProvider       ││
│  └───────┬───────┘  └───────┬────────┘  └────────────┬────────────┘│
│          │                   │                        │             │
│  ┌───────┴───────┐  ┌───────┴────────┐  ┌────────────┴──────────┐ │
│  │  StateMachine │  │  Concurrency   │  │      Security         │ │
│  │  10 States    │  │  WorkerPool    │  │  SecurityManager      │ │
│  │  Transitions  │  │  Cancellation  │  │  SecretVault          │ │
│  └───────────────┘  │  UiDispatcher  │  │  PermissionManager    │ │
│                      └────────────────┘  │  PluginSecurity       │ │
│                                          │  ThreatDetector       │ │
│                                          └───────────────────────┘ │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
┌─────────────────────────────────┼───────────────────────────────────┐
│                          Core Layer                                  │
│  ┌──────────┐ ┌─────────────────┐ ┌──────────┐ ┌────────────────┐  │
│  │ EventBus │ │ ServiceRegistry │ │ Version  │ │  Lifecycle     │  │
│  │ Event    │ │ ServiceScope    │ │ Manager  │ │  Manager       │  │
│  │ Delivery │ │ Descriptor      │ │          │ │  States        │  │
│  └──────────┘ └─────────────────┘ └──────────┘ └────────────────┘  │
│  ┌──────────┐ ┌─────────────────┐ ┌──────────┐ ┌────────────────┐  │
│  │Extensions│ │  Observability  │ │Scheduler │ │  Environment   │  │
│  │ 5 Protos │ │  HealthCheck    │ │  Async   │ │  Exceptions    │  │
│  │          │ │  Metrics/Tracer │ │  Retry   │ │  Resources     │  │
│  └──────────┘ └─────────────────┘ └──────────┘ └────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Komponentenbeziehungen

```
ApplicationHost ─────owns────→ EventBus
       │                           ↑
       ├─────owns────→ BootstrapManager ──creates──→ BootstrapContext
       │                                                    │
       ├─────owns────→ WorkerPool                          │
       │                                                    ↓
       ├─────owns────→ ApplicationStateMachine    ServiceRegistry
       │                                                    │
       ├─────owns────→ CentralErrorHandler                 │
       │                                                    ↓
       └─────produces─→ ApplicationContext ←───── ServiceProvider
                              │
                              ├── settings: ApplicationSettings
                              ├── configuration: ConfigurationService
                              ├── environment: Environment
                              ├── version: VersionManager
                              ├── logger: Logger
                              ├── services: ServiceProvider
                              ├── registry: ServiceRegistry
                              ├── events: EventBus
                              ├── scheduler: TaskScheduler
                              ├── plugins: PluginLoader
                              ├── theme: ThemeEngine
                              ├── resources: ResourceManager
                              └── runtime_state: RuntimeState
```

### 4.3 Datenfluss

```
config/default.toml ──→ ConfigurationStage ──→ ApplicationSettings
                                                       │
config/profile.toml ──→ ConfigurationService ──────────┘
                                                       │
                                                       ↓
data/jochen_x.sqlite3 ←── DatabaseStage ←── ConnectionManager
                                                       │
                                                       ↓
plugins/*/plugin.toml ──→ PluginLoader ──→ PluginCatalog
                                                       │
                                                       ↓
                              ApplicationContext (immutable aggregate)
                                                       │
                                                       ↓
                              MainWindow (UI) ←── ThemeEngine
```

---

## 5. Schichtenmodell

### 5.1 Schichtübersicht

```
┌────────────────────────────────────────────────────────────┐
│  UI          │ PySide6 Widgets, Navigation, Chat, Dashboard │
├──────────────┼─────────────────────────────────────────────┤
│  Developer   │ Optionale Diagnostik-Plattform              │
├──────────────┼─────────────────────────────────────────────┤
│  Services    │ Observability, Security-Services, AI Gateway │
├──────────────┼─────────────────────────────────────────────┤
│  SDK         │ Einzige öffentliche API für Plugin-Autoren  │
├──────────────┼─────────────────────────────────────────────┤
│  Plugins     │ Manifest-only Discovery, PluginCatalog      │
├──────────────┼─────────────────────────────────────────────┤
│  App         │ Host, Bootstrap, DI, Security, Concurrency  │
├──────────────┼─────────────────────────────────────────────┤
│  Core        │ Events, Registry, Version, Lifecycle, Sched.│
└──────────────┴─────────────────────────────────────────────┘
```

### 5.2 Schicht: Core

**Verzeichnis:** `core/`

**Verantwortung:** Stabile Verträge und fundamentale Infrastruktur. Definiert die Grundbausteine, von denen alle anderen Schichten abhängen.

**Module:**

| Modul | Datei | Verantwortung |
|-------|-------|---------------|
| EventBus | `core/events.py` | In-Process Event Distribution |
| ServiceRegistry | `core/registry.py` | DI Container mit Lifetime-Management |
| LifecycleManager | `core/lifecycle.py` | Geordnetes Startup/Shutdown |
| Version | `core/version.py` | Semantic Versioning und Kompatibilität |
| Extensions | `core/extensions.py` | 5 Extension-Point Protocols |
| Scheduler | `core/scheduler.py` | Async Task Scheduling |
| Observability | `core/observability.py` | Health, Metrics, Tracing |
| Environment | `core/environment.py` | Laufzeitumgebung (Pfade, OS) |
| Exceptions | `core/exceptions.py` | Basis-Exception-Hierarchie |
| Resources | `core/resources.py` | System-Resource-Snapshot |
| Performance | `core/performance.py` | Performance-Modus-Controller |
| AI Contracts | `core/ai_contracts.py` | Provider-Protocols für KI |
| Logging | `core/logging.py` | Structured Logging Configuration |

**Abhängigkeiten:** Ausschließlich Python-Stdlib. Einzige Ausnahme: `worker.py` (PySide6) und `ai_manager.py` (ollama) — beides Legacy-Module, die das Clean-Core-Prinzip verletzen und zur Entfernung vorgesehen sind.

**Begründung:** Core darf keine externen Abhängigkeiten haben, damit es in jedem Kontext (Tests, CLI, Server) ohne GUI-Framework lauffähig bleibt.

### 5.3 Schicht: App

**Verzeichnis:** `app/`

**Verantwortung:** Orchestrierung des Applikationslebenszyklus. Baut auf Core auf und fügt Bootstrap, State Machine, Concurrency, Security und Error Handling hinzu.

**Module:**

| Modul | Datei | Verantwortung |
|-------|-------|---------------|
| ApplicationHost | `app/application_host.py` | Root-Orchestrator |
| Application | `app/application.py` | Qt Event Loop Runner |
| Bootstrap | `app/bootstrap.py` | Phasenbasierter Bootstrap |
| Startup | `app/startup.py` | Startup-Sequenz-Koordination |
| Shutdown | `app/shutdown.py` | Graceful Shutdown |
| StateMachine | `app/state_machine.py` | 10-State Lifecycle |
| Context | `app/context.py` | Immutable Application Context |
| DI | `app/di.py` | ServiceProvider, DisposableRegistry |
| Concurrency | `app/concurrency.py` | WorkerPool, CancellationToken |
| Events | `app/events.py` | Typisierte Application Events |
| Errors | `app/errors.py` | Error Classification + Handling, `ErrorHandler` Protocol |
| Settings | `app/settings.py` | Runtime Settings (JSON) |
| Resources | `app/resources.py` | Resource-Pfad-Verwaltung |
| Security | `app/security/` | 13 Security-Komponenten (inkl. Models) |

**Abhängigkeiten:** Core, Config, Database, Styles, Plugins. Importiert PySide6 für Qt-Integration.

**Begründung:** Die App-Schicht ist der Integrationsort. Sie verdrahtet Core-Verträge mit konkreten Implementierungen und stellt den vollständigen Applikationskontext bereit.

### 5.4 Schicht: Plugins

**Verzeichnis:** `plugins/`

**Verantwortung:** Manifest-only Plugin-Discovery. Liest `plugin.toml`-Dateien und erstellt einen immutable Katalog kompatibler Plugins. Importiert und führt niemals Plugin-Code aus.

**Module:**

| Modul | Datei | Verantwortung |
|-------|-------|---------------|
| PluginLoader | `plugins/loader.py` | TOML-Discovery + Versionsfilter |
| PluginCatalog | `plugins/loader.py` | Immutable Plugin-ID-Snapshot |
| PluginManifest | `plugins/loader.py` | 3-Feld Manifest-Werttyp (`identifier`, `version`, `required_application_version`) |

**Abhängigkeiten:** Core (`Version`, `VersionManager`), Stdlib (`tomllib`, `pathlib`).

**Begründung:** Die strikte Trennung von Discovery und Execution ermöglicht es, Plugins zu katalogisieren, ohne ihre Code-Qualität oder Sicherheit zu riskieren (ADR-001).

### 5.5 Schicht: SDK

**Verzeichnis:** `sdk/`

**Verantwortung:** Einzige öffentliche Programmierschnittstelle für Plugin-Autoren. Kapselt alle Foundation-Interna hinter stabilen, versionierten Facades.

**Module:**

| Modul | Datei | Verantwortung |
|-------|-------|---------------|
| Version | `sdk/version.py` | SDK- und API-Versionskonstanten |
| Manifest | `sdk/manifest.py` | Enterprise `PluginMetadata` (11 Felder) |
| Plugin | `sdk/plugin.py` | 5 Basisklassen + `PluginRuntime` |
| Context | `sdk/context.py` | `PluginContext` + Builder |
| Config | `sdk/config.py` | Plugin-Konfigurationsstore (`FilePluginConfigStorage`, `InMemoryPluginConfigStorage`) |
| Events | `sdk/events.py` | Permission-gated Event-Facade |
| Services | `sdk/services.py` | Permission-gated Service-Resolution |
| Resources | `sdk/resources.py` | Sandboxed Resource-Zugriff |
| Logging | `sdk/logging.py` | Plugin-scoped Structured Logging |
| Errors | `sdk/errors.py` | SDK Exception-Hierarchie |

**Abhängigkeiten:** Keine Foundation-Imports (`core/`, `app/`, `plugins/`). Ausschließlich Stdlib + intra-SDK.

**Begründung:** Plugin-Autoren dürfen niemals Foundation-Interna importieren. Dadurch kann die Foundation refaktoriert werden, ohne Plugins zu brechen (ADR-010).

### 5.6 Schicht: Services

**Verzeichnis:** `services/`

**Verantwortung:** Querschnittliche Services für Observability und Security.

**Module:**

| Modul | Datei | Verantwortung |
|-------|-------|---------------|
| PerformanceMonitor | `services/observability.py` | CPU/RAM-Sampling |
| MetricsSnapshot | `services/observability.py` | Gaming/GPU-Metriken |
| GameModeDetector | `services/observability.py` | Plattform-Port (Protocol) |
| Security Services | `services/security.py` | CapabilityModel, PermissionLayer, AuditHooks |

**Abhängigkeiten:** Ausschließlich Stdlib. Kein Import aus Core oder App.

### 5.7 Schicht: Developer

**Verzeichnis:** `developer/`

**Verantwortung:** Optionale Diagnostik-Plattform (standardmäßig deaktiviert). Bietet Introspection in Events, Services, Plugins und Health.

**Module:**

| Modul | Datei | Verantwortung |
|-------|-------|---------------|
| Contracts | `developer/contracts.py` | 4 Diagnostik-Protocols |
| Models | `developer/models.py` | View Models (secret-frei) |
| DeveloperPlatform | `developer/platform.py` | Diagnostik-Facade |
| ArchitectureInspector | `developer/inspector.py` | Service-Analyse |

**Abhängigkeiten:** Core (`EventDelivery`, `ServiceDescriptor`, `HealthStatus`).

**Begründung:** Diagnostics sind optional (ADR-003). Kein Einfluss auf Production-Performance.

### 5.8 Schicht: UI

**Verzeichnis:** `ui/`

**Verantwortung:** PySide6-basierte Desktop-Oberfläche. Navigation, Chat, Dashboard, Developer Center.

**Module (Navigation Framework):**

| Modul | Datei | Verantwortung |
|-------|-------|---------------|
| MainWindow | `ui/navigation/main_window.py` | Production Desktop Shell |
| Sidebar | `ui/navigation/sidebar.py` | Collapsible Navigation |
| Toolbar | `ui/navigation/toolbar.py` | Back/Forward, Search |
| StatusBar | `ui/navigation/status_bar.py` | Live Subsystem Health |
| ModuleHost | `ui/navigation/module_host.py` | Lazy Module Activation |
| NavigationRegistry | `ui/navigation/navigation_registry.py` | Dynamic Module Registration |
| NavigationService | `ui/navigation/navigation_service.py` | Security-gated Navigation |
| NavigationController | `ui/navigation/navigation_controller.py` | Browser-like History |
| ThemeManager | `ui/navigation/theme_manager.py` | Desktop Theme Application |
| LayoutManager | `ui/navigation/layout_manager.py` | Responsive Layout |
| WindowState | `ui/navigation/window_state.py` | Persistent Window Geometry |

**Abhängigkeiten:** Core, App, Config, Styles, Plugins, PySide6.

### 5.9 Weitere Verzeichnisse

| Verzeichnis | Inhalt | Status |
|-------------|--------|--------|
| `ai/` | AI Gateway (`gateway.py`): `ProviderRegistry`, `RoutingEngine`, `ModelDescriptor`, `Capability`-Enum. Provider-unabhängige Routing-Infrastruktur ohne API-Aufrufe. | Aktiv |
| `styles/` | Theme Engine (`theme.py`): `ThemeTokens`, `ThemeEngine`, `LIGHT`/`DARK`-Presets. Token-basierte QSS-Generierung. | Aktiv |
| `config/` | TOML-Konfiguration: `ApplicationSettings`, `ConfigurationService`, `ThemeMode`. | Aktiv |
| `database/` | SQLite-Schicht (`database/sqlite.py`): `ConnectionManager`, `MigrationManager`, `SettingsRepository`. | Aktiv |
| `agents/` | Reserviert für zukünftige Agent-Infrastruktur. Derzeit leer. | Geplant |
| `scripts/` | Reserviert für Utility-Skripte. Derzeit leer. | Geplant |
| `resources/` | Anwendungsressourcen (Icons, Assets). Derzeit leer. | Geplant |
| `logs/` | Ausgabeverzeichnis für Rotating File Handler. | Runtime |
| `data/` | SQLite-Datenbank (`jochen_x.sqlite3`). | Runtime |
| `assets/` | Projekt-Assets. | Reserviert |

### 5.10 Parallele Codebasis: `src/jochen_x/`

Das Verzeichnis `src/jochen_x/` enthält eine vollständige, eigenständige Runtime-Plattform unter einem `src/`-Layout (pip-installierbar). Diese Codebasis ist architektonisch separat von den Top-Level-Modulen und enthält:

| Paket | Inhalt |
|-------|--------|
| `core/types/` | 11-State `RuntimeState`, `HealthStatus`, `RecoveryLevel`, `LogSeverity`, 13 typisierte Event-Dataclasses |
| `core/interfaces/` | 13 `@runtime_checkable` Protocols (ILifecycle, IEventBus, ILogger, IHealthCheck, etc.) |
| `core/exceptions/` | Erweiterte Exception-Hierarchie mit Correlation-IDs (20+ Exceptions) |
| `core/di/` | DI Container mit Thread-Local Circular-Detection und Scoped Container |
| `core/registry/` | Service Registry mit Lifecycle-Management (Start/Stop-Ordering, Rollback) |
| `core/events/` | Async EventBus mit Background-Dispatch-Thread, Queue (10.000), Dead-Letter-Queue |
| `core/observability/` | HMAC-SHA256 Audit Trail, Time-Series Metrics, Async Structured Logger |
| `core/concurrency/` | ThreadPoolExecutor-basierter WorkerPool, Cron-Scheduler, Resource Monitor |
| `core/recovery/` | 4-Level Recovery (Component Retry → Runtime Restart), Circuit Breaker, Cooldown |
| `core/security/` | Default-Deny PermissionManager, PolicyEngine, InputValidator |
| `core/plugin/` | PluginRegistry mit State Machine, PluginSandbox, PluginContext (disposable) |
| `core/runtime/` | 11-State StateMachine, LifecycleManager, 9-Step BootstrapSequence, RuntimeHost |

**Beziehung zur aktiven Codebasis:** Es existieren keine direkten Imports zwischen den beiden Codebasen. `src/jochen_x/` verwendet ausschließlich `jochen_x.core.*`-Importpfade. Die parallele Codebasis stellt eine Referenzimplementierung und potenzielle Nachfolge-Infrastruktur dar, auf die die Anwendungsschicht zukünftig portiert werden kann.

**Architektonische Schlussfolgerung:** Die `src/jochen_x/`-Codebasis implementiert deutlich fortgeschrittenere Patterns (HMAC-Audit, Circuit Breaker, Dead-Letter Queue, Cron-Scheduling, Resource-Leak-Detection), die in der aktiven Codebasis noch nicht vorhanden sind.

### 5.11 Abhängigkeitsrichtung und Begründung

```
UI ──→ App ──→ Core      (äußere Schichten importieren innere)
 ↓       ↓       ↑
Developer Services ──→ Core   (Services sind peers zu App)
         ↑
SDK (isoliert, keine Foundation-Imports)
```

Die Richtung stellt sicher, dass:
1. Core ohne GUI testbar ist
2. SDK ohne Foundation-Wissen kompiliert
3. UI ausgetauscht werden kann (z.B. CLI statt PySide6)
4. Developer-Tools entfernt werden können ohne Produktions-Einfluss

---

## 6. Komponentenbeschreibung

### 6.1 EventBus

**Datei:** `core/events.py`

**Zweck:** Thread-sichere, In-Process Event-Verteilung mit Glob-Pattern-Subscriptions.

**Verantwortung:**
- Synchrone und asynchrone Event-Delivery
- Prioritätsbasierte Handler-Sortierung
- Glob-Pattern-Matching für Subscriptions (`"app.*"`, `"security.threat.*"`)
- Sticky Events (letzter Event wird für späte Subscriber bewahrt)
- Bounded Event-History und Delivery-History für Diagnostik

**Abhängigkeiten:** `asyncio`, `collections.deque`, `fnmatch`, `threading.RLock`, `time`

**Schnittstellen:**
```python
subscribe(event_name: str, handler: EventHandler, *, priority: int = 0,
          event_filter: EventFilter | None = None, receive_sticky: bool = True) -> Callable[[], None]
publish(event: Event, *, sticky: bool = False) -> None
publish_async(event: Event, *, sticky: bool = False) -> None
history() -> tuple[Event, ...]
delivery_history() -> tuple[EventDelivery, ...]
```

**Lebenszyklus:** Wird in `RegistryStage` (INITIALIZE) erstellt. Lebt für die gesamte Applikationsdauer. Kein explizites Shutdown erforderlich.

**Thread-Sicherheit:** `RLock` schützt `_subscriptions`, `_history`, `_delivery_history` und `_sticky_events`. Handler werden unter Lock selektiert, aber außerhalb des Locks aufgerufen (Deadlock-Vermeidung).

**Fehlerverhalten:** Handler-Exceptions werden gefangen, im `EventDelivery`-Record als `error` protokolliert und an den Logger weitergeleitet. Die Delivery an andere Handler wird fortgesetzt.

**Logging:** Debug-Level für Publish/Subscribe-Operationen. Warning-Level für Handler-Fehler.

**Metriken:** `EventDelivery`-Records enthalten `duration_ms` und `subscriber_count`.

**Erweiterungsmöglichkeiten:** Neue Event-Typen erfordern lediglich ein neues frozen Dataclass mit `name` und `payload`.

### 6.2 ServiceRegistry

**Datei:** `core/registry.py`

**Zweck:** Dependency-Injection-Container mit drei Lifetime-Strategien und Auto-Wiring.

**Verantwortung:**
- Registrierung von Services über Typ-Key
- Auflösung mit automatischer Parameter-Injektion via Type Hints
- Circular-Dependency-Erkennung
- Scoped Lifetime Management

**Abhängigkeiten:** `inspect`, `threading.RLock`, `typing`

**Schnittstellen:**
```python
register(key: type[T], service: T) -> None
register_factory(key: type[T], factory: Callable[..., T], *, lifetime: Lifetime) -> None
register_type(key: type[T], implementation: type[T], *, lifetime: Lifetime) -> None
get(key: type[T]) -> T
create_scope() -> ServiceScope
validate() -> None
descriptors() -> tuple[ServiceDescriptor, ...]
```

**Lebenszyklus:** Erstellt in `RegistryStage`. Populiert durch alle nachfolgenden Stages. Validiert in `DependencyInjectionStage`.

**Thread-Sicherheit:** `RLock` schützt alle Mutationsoperationen. Singleton-Instanzen werden unter Lock erstellt (Double-Check-Locking-Semantik).

**Fehlerverhalten:**
- `LookupError` bei unregistriertem Key
- `CircularDependencyError(RuntimeError)` bei zirkulären Abhängigkeiten
- `ValueError` bei doppelter Registrierung

**Auto-Wiring:** `_construct()` introspiziert die Factory-Signatur via `inspect.signature()` und `get_type_hints()`. Jeder typisierte Parameter wird rekursiv aus dem Container aufgelöst.

### 6.3 ApplicationStateMachine

**Datei:** `app/state_machine.py`

**Zweck:** Explizite, thread-sichere Zustandsmaschine für den Applikationslebenszyklus.

**Verantwortung:**
- Verwaltung des aktuellen Applikationszustands
- Validierung von Zustandsübergängen gegen eine explizite Übergangstabelle
- Benachrichtigung von Listenern bei Übergängen
- Publishing von `ApplicationStateChanged`-Events

**Zustände:**
```
STARTING → INITIALIZING → LOADING_PLUGINS → LOADING_RESOURCES → READY
                                                                   │
READY → BUSY → READY                                               │
READY → UPDATING → READY | RESTART_REQUIRED                       │
READY → SHUTTING_DOWN → SHUTDOWN                                   │
RESTART_REQUIRED → SHUTTING_DOWN → SHUTDOWN                        │
```

**Thread-Sicherheit:** `RLock` schützt `_state` und `_listeners`. Transitions sind atomar.

**Fehlerverhalten:** `IllegalStateTransitionError` bei unerlaubtem Übergang.

### 6.4 WorkerPool

**Datei:** `app/concurrency.py`

**Zweck:** Bounded Background-Worker-Pool mit kooperativer Cancellation.

**Verantwortung:**
- Hintergrund-Taskausführung über `QThreadPool`
- Kooperative Cancellation über `CancellationToken`
- Timeout-Überwachung via `threading.Timer`
- UI-Thread-Marshalling über `UiDispatcher`

**Schnittstellen:**
```python
submit(function: TaskCallable, *, token: CancellationToken | None, timeout: float | None) -> TaskHandle
shutdown(*, timeout: float | None = 5.0) -> bool
active_count() -> int
```

**Thread-Sicherheit:** `RLock` schützt `_handles` und `_timers`. `CancellationToken` verwendet `threading.Event` für Wait-Semantik.

**Fehlerverhalten:** Exceptions in Tasks werden über `WorkerSignals.error` propagiert. Timeouts führen zu automatischer Cancellation.

### 6.5 SecurityManager

**Datei:** `app/security/security_manager.py`

**Zweck:** Koordinator für alle Security-Services. Komponiert und verwaltet 10 Sicherheitskomponenten.

**Verantwortung:**
- Factory-basierte Konstruktion aller Security-Services
- Registrierung aller Services in der `ServiceRegistry`
- Lifecycle-Management (Initialize/Dispose)

**Komponierte Services:**
1. `EncryptionService` — Base64-Placeholder (non-cryptographic)
2. `SecretVault` — In-Memory Secret Storage mit Encryption
3. `PermissionManager` — Role-Based Access Control
4. `IdentityManager` — Identity und Session Management
5. `AuditLogger` — Append-Only Audit Trail
6. `ApiKeyManager` — API-Key Lifecycle
7. `BrokerSecurity` — Broker-Zugangsrichtlinien
8. `PluginSecurity` — Trust Ledger für Plugins
9. `BackupManager` — Encrypted Backup/Restore
10. `ThreatDetector` — Brute-Force-Erkennung
11. `Models` (`app/security/models.py`) — Security-Datenmodelle

**Lebenszyklus:** Erstellt und registriert in `SecurityBootstrapStage` (FINALIZE). Disposed in `ShutdownSequence`.

### 6.6 PluginLoader

**Datei:** `plugins/loader.py`

**Zweck:** Manifest-only Plugin-Discovery mit Versionskompatiblitätsprüfung.

**Verantwortung:**
- Scanning von `plugins/*/plugin.toml`
- TOML-Parsing der Manifest-Felder
- Filterung nach Applikationsversionskompatibilität
- Erstellung eines immutable `PluginCatalog`

**Schnittstellen:**
```python
discover() -> tuple[PluginManifest, ...]
```

**Fehlerverhalten:** Fehlerhafte oder inkompatible Manifeste werden stillschweigend gefiltert (nicht in den Katalog aufgenommen).

**Sicherheit:** Liest ausschließlich TOML-Dateien. Importiert und führt keinen Plugin-Code aus.

### 6.7 PluginRuntime (SDK)

**Datei:** `sdk/plugin.py`

**Zweck:** Lifecycle-Driver für Plugin-Instanzen.

**Verantwortung:**
- Steuerung des Plugin-Lifecycle (UNLOADED → INITIALIZED → STARTED → STOPPED)
- Guarding aller Übergänge durch `RLock`
- Fehlerbehandlung mit Übergang zu FAILED
- Optionaler State-Change-Callback

**Schnittstellen:**
```python
initialize(context: PluginContext) -> None
start() -> None
stop() -> None
shutdown() -> None
```

**Thread-Sicherheit:** `RLock` schützt alle Zustandsübergänge.

### 6.8 ThemeEngine

**Datei:** `styles/theme.py`

**Zweck:** Token-basierte Theme-Generierung für Qt-Stylesheets.

**Verantwortung:**
- Auflösung des System-Themes (Light/Dark)
- Generierung vollständiger QSS-Stylesheets aus `ThemeTokens`

**Tokens:**
```python
ThemeTokens(background, foreground, surface, accent, font_family, spacing, icon_size, animation_ms)
LIGHT = ThemeTokens("#f7f8fa", "#17202a", "#ffffff", "#0067c0")
DARK  = ThemeTokens("#1e1e1e", "#f1f1f1", "#292929", "#4da3ff")
```

### 6.9 NavigationRegistry

**Datei:** `ui/navigation/navigation_registry.py`

**Zweck:** Thread-sichere, dynamische Registrierung von UI-Modulen mit Observer-Pattern.

**Verantwortung:**
- Registrierung/Deregistrierung von NavigationDestinations
- Cycle-Detection bei Batch-Registrations
- Benachrichtigung von Observers bei Änderungen
- Auflösung nach Identifier

**Thread-Sicherheit:** `RLock` schützt `_registrations` und `_listeners`.

### 6.10 AI Gateway

**Datei:** `ai/gateway.py`

**Zweck:** Provider-unabhängige Routing-Infrastruktur für KI-Modelle. Enthält keine API-Aufrufe oder Credentials — reine Metadaten- und Routing-Schicht.

**Verantwortung:**
- Registrierung von Provider-Metadaten (`ProviderDescriptor`)
- Routing nach Capability (`Capability.TEXT`, `VISION`, `EMBEDDING`)
- Selektion passender Modelle für eine gegebene Capability

**Schnittstellen:**
```python
# ProviderRegistry
register(provider: ProviderDescriptor) -> None
all() -> tuple[ProviderDescriptor, ...]

# RoutingEngine
candidates(capability: Capability) -> tuple[ModelDescriptor, ...]
```

**Datenmodelle:**
- `Capability(StrEnum)` — `TEXT`, `VISION`, `EMBEDDING`
- `ModelDescriptor` (frozen) — `provider_id`, `model_id`, `capabilities`
- `ProviderDescriptor` (frozen) — `identifier`, `display_name`, `models`

**Abhängigkeiten:** Ausschließlich Stdlib (`dataclasses`, `enum`).

**Beziehung zu `core/ai_contracts.py`:** `ai/gateway.py` ist die konkrete Routing-Implementierung. `core/ai_contracts.py` definiert die abstrakten Provider-Protocols (Embedding, Vision, Streaming, etc.). Beide referenzieren einander nicht direkt — die Integration erfolgt auf Anwendungsebene.

### 6.11 ConfigurationService

**Datei:** `config/settings.py`

**Zweck:** TOML-basierte, schichtbare Konfiguration.

**Verantwortung:**
- Laden der Default-Konfiguration (`config/default.toml`)
- Optionales Merging mit Profil-Konfiguration (`config/profile.toml`)
- Persistierung von Profil-Änderungen
- Validierung von Pflichtfeldern und Wertebereichen

**Schnittstellen:**
```python
load() -> ApplicationSettings
save_profile(settings: ApplicationSettings) -> None
```

---

## 7. Runtime Host

### 7.1 Vollständige Beschreibung

Der `ApplicationHost` ist der Top-Level-Orchestrator des JOCHEN X Systems. Er besitzt alle langlebigen Infrastruktur-Objekte (EventBus, WorkerPool, StateMachine) und koordiniert Bootstrap, Betrieb und Shutdown.

**Datei:** `app/application_host.py`

**Besitzt:**
- `EventBus` (Core Event-System)
- `BootstrapManager` (Phasenbasierter Bootstrap)
- `WorkerPool` (Background-Task-Execution)
- `ApplicationStateMachine` (Lifecycle State)
- `CentralErrorHandler` (Error Classification)

### 7.2 Bootstrap

Der Bootstrap wird durch `StartupSequence.execute(root)` orchestriert:

```
Phase 1: INITIALIZE
  ├── EnvironmentStage      → Environment (root, OS, Python)
  ├── ConfigurationStage    → ApplicationSettings (TOML)
  ├── LoggingStage          → Logger (Rotating File + Console)
  ├── DatabaseStage         → ConnectionManager + Migrations
  ├── RegistryStage         → ServiceRegistry + EventBus + VersionManager
  ├── ThemeStage            → ThemeEngine
  └── SchedulerStage        → TaskScheduler

Phase 2: LOAD_PLUGINS
  └── PluginDiscoveryStage  → PluginLoader + PluginCatalog

Phase 3: LOAD_RESOURCES
  └── ResourceStage         → ResourceManager

Phase 4: FINALIZE
  ├── SecurityBootstrapStage → SecurityManager (10 Services) [*]
  ├── DeveloperToolsStage   → DeveloperPlatform (optional)
  └── DependencyInjectionStage → ServiceProvider + Validation

[*] SecurityBootstrapStage ist NICHT in default_stages() enthalten.
    Sie wird separat angehängt (z.B. über create_desktop_bootstrap_manager()).
```

**Sequenz:**
1. `begin(root)` erstellt einen mutable `BootstrapContext`
2. Transition zu `INITIALIZING`, Run INITIALIZE Phase
3. Emit `ApplicationStarting` + `ApplicationStarted`
4. Transition zu `LOADING_PLUGINS`, Run LOAD_PLUGINS Phase
5. Transition zu `LOADING_RESOURCES`, Run LOAD_RESOURCES Phase
6. Run FINALIZE Phase
7. `build_context()` erstellt den immutable `ApplicationContext`
8. Transition zu `READY`, Emit `ApplicationReady`

### 7.3 Shutdown

`ShutdownSequence.execute()` orchestriert den geordneten Shutdown:

1. Idempotenz-Prüfung (bei `SHUTDOWN` → No-Op)
2. Emit `ShutdownRequested`
3. Transition zu `SHUTTING_DOWN`
4. `WorkerPool.shutdown(timeout=5.0)` — Worker-Drain
5. `DisposableRegistry.dispose_all()` — Reverse-Order Cleanup
6. Transition zu `SHUTDOWN`
7. Emit `ShutdownCompleted`

### 7.4 Restart

```python
def restart(self) -> ApplicationContext:
    self.shutdown(reason="restart")
    self._reset()
    return self.start()
```

Reset setzt die StateMachine, den ErrorHandler und den WorkerPool zurück.

### 7.5 State Machine

Siehe Abschnitt 6.3 für die vollständige Zustandstabelle. Die State Machine ist der Single Source of Truth für den Applikationszustand.

### 7.6 Recovery

Bei einem fatalen Fehler:
1. `CentralErrorHandler` klassifiziert den Fehler
2. Bei `FATAL` Severity: `_on_fatal()` Callback
3. `Application._handle_fatal()` postet `QApplication.quit()`
4. Bei `recover()`: Reset + Neustart

### 7.7 Fehlerfälle

| Fehler | Verhalten |
|--------|-----------|
| Stage-Exception während Bootstrap | Bootstrap-Abbruch, State → FAILED |
| Worker-Exception | ErrorReport, keine State-Änderung |
| Fatal Error | Callback → Application Quit |
| Shutdown-Timeout | Best-Effort, verbleibende Disposables werden trotzdem aufgeräumt |

---

## 8. Dependency Injection

### 8.1 Container

Der DI-Container besteht aus zwei Komponenten:

1. **`ServiceRegistry`** (Core) — Vollständiger Container mit Registrierung, Resolution und Auto-Wiring
2. **`ServiceProvider`** (App) — Read-Only Facade für Konsumenten

### 8.2 Provider

Registrierung erfolgt über drei Methoden:

```python
# Direkte Instanz (Singleton)
registry.register(EventBus, event_bus_instance)

# Factory mit Lifetime
registry.register_factory(ResourceManager, create_resource_manager, lifetime=Lifetime.TRANSIENT)

# Typ-Registrierung (Auto-Wiring via Constructor)
registry.register_type(ThemeEngine, ThemeEngine, lifetime=Lifetime.SINGLETON)
```

### 8.3 Scopes

| Lifetime | Verhalten | Verwendung |
|----------|-----------|------------|
| `SINGLETON` | Einmalige Erstellung, globale Wiederverwendung | EventBus, SecurityManager |
| `TRANSIENT` | Neue Instanz bei jedem `get()` | Request-Handler, temporäre Services |
| `SCOPED` | Eine Instanz pro `ServiceScope` | Plugin-Contexts, Request-Scopes |

### 8.4 Composition Root

Die `RegistryStage` ist der primäre Composition Root:

```python
# Registrierungen in RegistryStage.execute():
registry.register(ServiceRegistry, registry)
registry.register(EventBus, event_bus)
registry.register(VersionManager, versions)
registry.register(DisposableRegistry, disposables)
# ... weitere Services in nachfolgenden Stages
```

### 8.5 Registrierung

Die Registrierung erfolgt ausschließlich während des Bootstrap (Stages). Nach `DependencyInjectionStage.validate()` ist der Container sealed — keine weiteren Registrierungen.

### 8.6 Auflösung

Auto-Wiring-Algorithmus in `_construct()`:
1. Signatur der Factory via `inspect.signature()` lesen
2. Type Hints via `typing.get_type_hints()` extrahieren
3. Jeden typisierten Parameter rekursiv aus dem Container auflösen
4. Factory mit aufgelösten Parametern aufrufen

Circular-Dependency-Detection: Ein `trail`-Set trackt die aktuell aufgelöste Kette. Bei erneutem Auftreten eines Keys → `CircularDependencyError`.

### 8.7 Lebenszyklus

```
RegistryStage.execute()     → Container erstellt, Core-Services registriert
ThemeStage.execute()        → ThemeEngine registriert
SchedulerStage.execute()    → TaskScheduler registriert
PluginDiscoveryStage        → PluginLoader + PluginCatalog registriert
ResourceStage               → ResourceManager registriert
SecurityBootstrapStage      → 10 Security-Services registriert
DeveloperToolsStage         → DeveloperPlatform registriert (optional)
DependencyInjectionStage    → ServiceProvider erstellt, validate() aufgerufen
```

---

## 9. Event Bus

### 9.1 Architektur

Der EventBus ist ein synchroner, In-Process-Event-Distributor mit folgenden Eigenschaften:

- **Pattern-basiert:** Subscriptions nutzen `fnmatch`-Glob-Patterns
- **Prioritätsgesteuert:** Handler werden in absteigender Priorität aufgerufen
- **Thread-sicher:** Alle Mutationen unter `RLock`
- **History-bounded:** Konfigurierbare maximale History-Größe (Default: 256)
- **Sticky:** Letzte Events können für späte Subscriber bewahrt werden

### 9.2 Publish

```python
def publish(self, event: Event, *, sticky: bool = False) -> None:
    # 1. Event in History aufnehmen
    # 2. Bei sticky=True: in _sticky_events speichern
    # 3. Passende Subscriptions per fnmatch filtern
    # 4. Nach Priorität sortieren (absteigend)
    # 5. Event-Filter anwenden (falls vorhanden)
    # 6. Handler sequentiell aufrufen
    # 7. EventDelivery-Record erstellen
```

### 9.3 Subscribe

```python
unsubscribe = event_bus.subscribe(
    "app.plugin.*",           # Glob-Pattern
    handler_function,          # EventHandler
    priority=10,               # Höher = früher
    event_filter=my_filter,    # Optional: zusätzliche Filterung
    receive_sticky=True        # Letzte sticky Events sofort erhalten
)
# unsubscribe() entfernt die Subscription
```

### 9.4 Reihenfolge

1. Subscriptions werden per `fnmatch` gegen `event.name` geprüft
2. Passende Subscriptions werden nach `priority` absteigend sortiert
3. Bei gleicher Priorität: Insertion-Order (First-Registered-First-Called)
4. Jeder Handler wird sequentiell aufgerufen (kein Parallelismus)

### 9.5 Fehlerbehandlung

- Handler-Exceptions werden gefangen (kein Abbruch der Delivery-Chain)
- Exception wird im `EventDelivery.error`-Feld protokolliert
- Logger erhält die Exception als Warning
- Alle weiteren Handler werden trotzdem aufgerufen

### 9.6 Synchronisation

- Publish ist synchron: Der Aufrufer blockiert bis alle Handler abgearbeitet sind
- `publish_async()` nutzt `asyncio.gather()` für async Handler
- Subscribe/Unsubscribe sind unter `RLock` atomar
- Handler-Aufruf erfolgt außerhalb des Locks (keine Deadlocks bei re-entry)

---

## 10. Plugin-System

### 10.1 Registry (Discovery)

```
plugins/
  ├── my-plugin/
  │   └── plugin.toml      ← wird von PluginLoader gescannt
  └── another-plugin/
      └── plugin.toml
```

`PluginLoader.discover()`:
1. Scannt `plugins/*/plugin.toml`
2. Parst TOML: `id`, `version`, `required_application_version`
3. Prüft Kompatibilität via `VersionManager.is_compatible()`
4. Erstellt `PluginManifest`-Werttyp
5. Gibt nur kompatible Manifeste zurück

`PluginCatalog`:
- Frozen Dataclass mit `identifiers: tuple[str, ...]`
- Property `count` für schnelle Abfrage
- Immutable Snapshot der Discovery-Ergebnisse

### 10.2 Sandbox (SDK)

Jeder Plugin erhält einen isolierten `PluginContext` mit:
- `PluginEventBus` — Permission-gated Event-Zugriff
- `PluginServices` — Permission-gated Service-Resolution
- `PluginConfig` — Private Konfiguration (thread-safe)
- `PluginResources` — Sandboxed Dateizugriff (Path-Traversal-Protection)
- `PluginLogger` — Scoped Structured Logging

**Sandbox-Enforcement:**
```python
# Im PluginContextBuilder.build():
def permission_check(permission: PluginPermission) -> None:
    if permission not in permitted:
        raise PluginPermissionError(...)

# Injiziert in PluginEventBus und PluginServices
```

### 10.3 Plugin Context

Der `PluginContext` ist ein frozen Dataclass — nach Konstruktion immutable:

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| `metadata` | `PluginMetadata` | Validiertes Manifest |
| `logger` | `PluginLogger` | Scoped Logger |
| `events` | `PluginEventBus` | Permission-gated Events |
| `services` | `PluginServices` | Permission-gated Services |
| `config` | `PluginConfig` | Private Config |
| `resources` | `PluginResources` | Sandboxed Resources |
| `application_version` | `str` | Host-Version |
| `api_version` | `str` | SDK API Version |
| `metadata_view` | `Mapping[str, Any]` | Read-only Informationsmapping (App-/SDK-Version + Plugin-ID) |

### 10.4 Isolation

- **Code-Isolation:** Plugin-Code wird erst in `PluginActivationStage` (FINALIZE) importiert
- **State-Isolation:** Jeder Plugin hat eigenen `PluginContext` (keine Shared State)
- **Permission-Isolation:** Jeder API-Zugriff wird gegen deklarierte Permissions geprüft
- **Resource-Isolation:** Dateizugriff ist auf das Plugin-Verzeichnis beschränkt
- **Thread-Isolation (geplant, ADR-009):** Dedicated Thread pro Plugin

### 10.5 Berechtigungen

10 definierte Permissions:

| Permission | Zweck |
|------------|-------|
| `network` | Netzwerkzugriff |
| `filesystem` | Dateisystemzugriff |
| `credentials` | Credential-Zugriff |
| `system_observation` | System-Beobachtung |
| `ui` | UI-Beitrag |
| `events.publish` | Event-Publishing |
| `events.subscribe` | Event-Subscription |
| `configuration` | Konfigurationszugriff |
| `resources` | Ressourcenzugriff |
| `services` | Service-Resolution |

### 10.6 Lifecycle

```
UNLOADED ──→ INITIALIZED ──→ STARTED ──→ STOPPED (terminal)
                                 │
                            (Fehler) ──→ FAILED (terminal)
```

Hooks (überschreibbar durch Plugins):
- `on_initialize()` — Nach Context-Attachment
- `on_start()` — Aktivierung
- `on_stop()` — Deaktivierung
- `on_shutdown()` — Finale Aufräumarbeiten

### 10.7 Recovery

- Bei Exception in `on_initialize()` → State: `FAILED`
- Bei Exception in `on_start()` → State: `FAILED`
- `stop()` ist safe-to-call aus jedem Zustand
- `shutdown()` ist idempotent und sicher bei Mehrfachaufruf

---

## 11. Security

### 11.1 Permission Model

Das Security-System basiert auf einem **Capability-basierten Modell** mit Default Deny:

```
Identity ──has──→ Role ──grants──→ Permission
Plugin ──declares──→ PluginPermission (im Manifest)
```

**Architektonische Schlussfolgerung:** Das aktuelle System implementiert die Permission-Infrastruktur vollständig, die tatsächliche Enforcement für Plugins ist jedoch noch nicht über den Bootstrap verdrahtet (ADR-011, in Arbeit).

### 11.2 Policies

```python
# BrokerAccessPolicy: Verbindung Broker → benötigte Permission
policy = BrokerAccessPolicy(broker="interactive_brokers", required_permission=Permission(...))

# Authentifizierung prüft PermissionManager
broker_security.authenticate("interactive_brokers", identity_id)
```

### 11.3 Validator

`PluginSecurity` fungiert als Trust-Ledger:

```python
# Trust Levels
class PluginTrustLevel(StrEnum):
    UNTRUSTED = "untrusted"
    VERIFIED = "verified"
    TRUSTED = "trusted"
    REJECTED = "rejected"

# Workflow
plugin_security.verify(identifier, version) -> PluginVerdict
plugin_security.approve(identifier)          # → TRUSTED
plugin_security.reject(identifier, reason)   # → REJECTED
```

### 11.4 Trust Boundaries

```
┌─────────────────────────────────────────────────────┐
│                Foundation (Trusted)                  │
│  ┌──────────────────────────────────────────────┐   │
│  │              Core Runtime                    │   │
│  │  EventBus · ServiceRegistry · Lifecycle      │   │
│  └──────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────┐   │
│  │        Security Boundary (PluginSecurity)    │   │
│  │  Trust Ledger · Manifest Validation          │   │
│  └──────────────────┬───────────────────────────┘   │
└─────────────────────┼───────────────────────────────┘
                      │ (gated access via PluginContext)
┌─────────────────────┼───────────────────────────────┐
│                Plugin Space (Untrusted)              │
│  ┌──────────────────┴───────────────────────────┐   │
│  │  Plugin A    Plugin B    Plugin C            │   │
│  │  (sandboxed) (sandboxed) (sandboxed)         │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### 11.5 Plugin Security

`PluginSecurity` (`app/security/plugin_security.py`):
- In-Memory Trust Ledger (Dictionary: identifier → TrustLevel)
- `verify_manifest(manifest)` prüft Manifest-Integrität
- `verify(identifier, version)` gibt `PluginVerdict` zurück
- Emittiert `PluginVerified` und `PluginRejected` Events
- Thread-sicher via `RLock`

### 11.6 Zukünftige Authentifizierung

**Architektonische Schlussfolgerung:** Das `IdentityManager`-Modul (`app/security/identity_manager.py`) implementiert bereits:
- Identity-Erstellung mit Display-Name und Rollen
- Session-Management (Start/End)
- Grundlage für Multi-User-Szenarien

Noch nicht implementiert:
- Externe Authentifizierung (OAuth, LDAP)
- Passwort-basierte Anmeldung
- Token-basierte Session-Validierung

---

## 12. Recovery

### 12.1 Recovery Levels

Das System definiert Recovery auf zwei Ebenen:

**Applikationsebene** (implementiert):
- `CentralErrorHandler` klassifiziert Fehler nach `ErrorCategory` und `ErrorSeverity`
- `RECOVERABLE` Fehler werden geloggt und per Event publiziert
- `FATAL` Fehler führen zu kontrolliertem Application-Quit
- `ApplicationHost.recover()` ermöglicht Reset + Restart

**Komponentenebene** (`src/jochen_x/` — parallele Codebasis, Referenzimplementierung):
- 4 Eskalationsstufen: Component Retry → Component Restart → Service Restart → Runtime Restart
- Cooldown-Perioden und Circuit Breaker pro Level
- Max-Retries pro Level

### 12.2 Recovery Handler

**Datei:** `app/errors.py`

```python
class CentralErrorHandler:
    def handle(self, error, *, category=None, context=None) -> ErrorReport:
        report = self._classify_and_build_report(error)
        self._log(report, error)
        self._publish_event(report)
        if report.is_fatal:
            self._on_fatal(report)
        return report
```

### 12.3 Recovery Strategien

| Strategie | Auslöser | Aktion |
|-----------|----------|--------|
| Log + Continue | `RECOVERABLE` Fehler | Log Warning, Event publizieren |
| Worker Retry | Task-Failure | Neuer Versuch (abhängig von Task-Design) |
| Application Quit | `FATAL` Fehler | Graceful Shutdown via Qt |
| Full Restart | `recover()` Aufruf | Reset + kompletter Bootstrap |

### 12.4 Escalation

```
Error Raised
    │
    ▼
CentralErrorHandler._classify()
    │
    ├── RECOVERABLE → Log + Event + Continue
    │
    └── FATAL → _on_fatal()
                    │
                    ▼
              Application._handle_fatal()
                    │
                    ▼
              QApplication.quit()
```

### 12.5 Graceful Degradation

- **WorkerPool:** Bei Überlast werden neue Tasks abgelehnt (bounded queue)
- **PluginSecurity:** Abgelehnte Plugins werden aus dem Katalog entfernt, System läuft weiter
- **Bootstrap-Fehler:** Bereits gestartete Module werden bei Stage-Fehler zurückgerollt
- **Theme-Fehler:** Fallback auf Dark-Theme
- **Developer-Tools:** Bei Deaktivierung keine Diagnostik, aber keine Beeinträchtigung

---

## 13. Observability

### 13.1 Logging

**Datei:** `core/logging.py`

- Structured Logging via `StructuredFormatter`
- Rotating File Handler (2 MB, 5 Backups)
- Console Handler + File Handler parallel
- Logger-Name: `"jochen_x"`
- Context-Attribute werden als Key-Value-Paare angehängt

**Konfiguration:**
```toml
[application]
log_level = "INFO"
```

**Secret-Redaktion** (Developer Platform):
- Regex-basierte Erkennung von `secret|token|password|credential|api_key`
- Automatische Maskierung in Log-Viewer und Configuration-View

### 13.2 Health

**Datei:** `core/observability.py`

```python
@dataclass(frozen=True, slots=True)
class HealthStatus:
    name: str
    healthy: bool
    detail: str = ""

class HealthCheck(Protocol):
    def check(self) -> HealthStatus: ...

def run_health_checks(*checks: HealthCheck) -> tuple[HealthStatus, ...]: ...
```

**ApplicationHost.health()** gibt drei Status zurück:
1. Lifecycle-Health (basierend auf StateMachine-State)
2. Worker-Health (basierend auf Active Count)
3. Error-Health (basierend auf Fatal-Error-Zustand)

### 13.3 Metrics

**Datei:** `core/observability.py`

```python
class Metrics:
    def increment(self, name: str, value: float = 1) -> None
    def snapshot(self) -> dict[str, float]
```

Simple In-Memory Counter-Store. Keine externe Metrics-Infrastruktur.

### 13.4 Audit

**Datei:** `app/security/audit_logger.py`

- Append-only, immutable Audit-Trail
- `AuditEntry` mit: category, action, actor, outcome, detail, sequence, timestamp
- Thread-sicher via `RLock`
- Monoton steigende Sequence-Nummer

### 13.5 Monitoring (UI)

**Datei:** `ui/navigation/status_bar.py`

Die StatusBar zeigt vier Live-Indikatoren:
1. **Application** — State-Änderungen via `STATE_CHANGED` Event
2. **Security** — Initialization und Threat Detection
3. **Workers** — Polling via QTimer (1s Intervall)
4. **Plugins** — Load/Fail Events

---

## 14. Concurrency

### 14.1 Worker Pool

**Datei:** `app/concurrency.py`

- Basiert auf `QThreadPool` (Qt-native Thread-Verwaltung)
- Bounded: `max_workers` konfigurierbar (Default: OS-spezifisch)
- Jeder Task erhält ein `CancellationToken`
- Optionaler Timeout via `threading.Timer`

### 14.2 Scheduler

**Datei:** `core/scheduler.py`

- Async-basiert (`asyncio`)
- Unterstützt: Delay, Interval, Retries, Timeout
- Cooperative Cancellation via Return-Callable
- `shutdown()` cancelled alle laufenden Tasks

### 14.3 Tasks

```python
# Task-Submission
handle = worker_pool.submit(
    my_task_function,
    token=CancellationToken(),
    timeout=30.0
)

# Ergebnis abfragen
handle.wait(timeout=5.0)
result = handle.result()
```

### 14.4 Locks

Alle mutable State wird durch `threading.RLock` geschützt. Die Wahl von `RLock` (reentrant) statt `Lock` ist bewusst: Callback-Chains können den gleichen Thread re-entrant erreichen.

### 14.5 Race Conditions

Vermeidungsstrategien:
- Frozen Dataclasses für alle Domänenobjekte (keine Race auf shared state)
- Lock-Akquisition vor jedem Zustandschange
- Handler-Aufruf außerhalb von Locks (Deadlock-Vermeidung)
- Copy-on-Read für Collections (z.B. `tuple(self._items)` unter Lock)

### 14.6 Deadlock-Vermeidung

- EventBus: Subscriptions unter Lock selektieren, Handler außerhalb aufrufen
- ServiceRegistry: Resolution unter Lock, Factory-Aufruf kann rekursiv resolven (daher RLock)
- StateMachine: Listener-Benachrichtigung unter Lock (kurze, nicht-blockierende Callbacks erwartet)

### 14.7 Thread Ownership

| Thread | Verantwortung |
|--------|---------------|
| Main (UI) Thread | Qt Event Loop, Widget-Updates, Signal/Slot |
| Worker Threads | `QRunnable` Tasks aus `WorkerPool` |
| Timer Threads | Timeout-Überwachung (Daemon) |
| Scheduler Thread | `asyncio` Event Loop für geplante Tasks |

**UI-Thread-Marshalling:**
```python
class UiDispatcher(QObject):
    _dispatch = Signal(object)  # Queued Connection

    def post(self, callback: Callable[[], None]) -> None:
        self._dispatch.emit(callback)
```

---

## 15. Interfaces

### 15.1 Core Protocols

| Protocol | Datei | Methoden | Thread-Sicherheit |
|----------|-------|----------|-------------------|
| `HealthCheck` | `core/observability.py` | `check() -> HealthStatus` | Implementierung verantwortlich |
| `ResourceMonitor` | `core/resources.py` | `snapshot() -> ResourceSnapshot` | Implementierung verantwortlich |

### 15.1a Services Protocols

| Protocol | Datei | Methoden | Thread-Sicherheit |
|----------|-------|----------|-------------------|
| `GameModeDetector` | `services/observability.py` | `snapshot() -> MetricsSnapshot` | Implementierung verantwortlich |
| `SecretProvider` | `services/security.py` | `get(name) -> str \| None` | Implementierung verantwortlich |

### 15.2 App Protocols

| Protocol | Datei | Methoden | Thread-Sicherheit |
|----------|-------|----------|-------------------|
| `EventPublisher` | `app/events.py` | `publish(event, *, sticky) -> None` | EventBus ist thread-safe |
| `BootstrapStage` | `app/bootstrap.py` | `name`, `phase`, `execute(context)` | Sequentiell aufgerufen |
| `Disposable` | `app/di.py` | `dispose() -> None` | Muss idempotent sein |
| `SupportsShutdown` | `app/shutdown.py` | `shutdown(*, timeout) -> bool` | Implementierung verantwortlich |
| `ErrorHandler` | `app/errors.py` | `handle(error, *, category, context) -> ErrorReport` | Thread-safe |
| `SettingsValidator` | `app/settings.py` | `validate(data) -> None` | Stateless |

### 15.3 SDK Protocols

| Protocol | Datei | Methoden | Thread-Sicherheit |
|----------|-------|----------|-------------------|
| `PluginConfigStorage` | `sdk/config.py` | `read(plugin_id)`, `write(plugin_id, data)` | Implementierung verantwortlich |
| `EventBusPort` | `sdk/events.py` | `subscribe(...)`, `publish(...)` | Host garantiert |

### 15.4 Developer Protocols

| Protocol | Datei | Methoden | Thread-Sicherheit |
|----------|-------|----------|-------------------|
| `EventDiagnostics` | `developer/contracts.py` | `delivery_history() -> tuple[EventDelivery, ...]` | Read-only |
| `ServiceDiagnostics` | `developer/contracts.py` | `descriptors() -> tuple[ServiceDescriptor, ...]` | Read-only |
| `PluginDiagnostics` | `developer/contracts.py` | `discover() -> Iterable[object]` | Read-only |
| `HealthDiagnostics` | `developer/contracts.py` | `health() -> Iterable[HealthStatus]` | Read-only |

### 15.5 Extension Protocols

| Protocol | Datei | Attribut |
|----------|-------|----------|
| `PluginExtension` | `core/extensions.py` | `identifier: str` |
| `ToolExtension` | `core/extensions.py` | `identifier: str` |
| `UIExtension` | `core/extensions.py` | `identifier: str` |
| `CommandExtension` | `core/extensions.py` | `identifier: str` |
| `WorkflowExtension` | `core/extensions.py` | `identifier: str` |

### 15.6 AI Protocols

| Protocol | Datei | Methoden |
|----------|-------|----------|
| `Model` | `core/ai_contracts.py` | `identifier: str`, `capabilities: frozenset[AICapability]` |
| `Provider` | `core/ai_contracts.py` | `identifier: str`, `models: tuple[Model, ...]` |
| `EmbeddingProvider` | `core/ai_contracts.py` | `async embed(text) -> tuple[float, ...]` |
| `VisionProvider` | `core/ai_contracts.py` | (leer, Marker-Protocol) |
| `ToolCallingProvider` | `core/ai_contracts.py` | (leer, Marker-Protocol) |
| `StreamingProvider` | `core/ai_contracts.py` | `stream(prompt) -> AsyncIterator[str]` |
| `SpeechProvider` | `core/ai_contracts.py` | (leer, Marker-Protocol) |
| `TranscriptionProvider` | `core/ai_contracts.py` | (leer, Marker-Protocol) |
| `ProviderRouter` | `core/ai_contracts.py` | `select(capability) -> Provider` |

### 15.7 UI Protocols

| Protocol | Datei | Methoden |
|----------|-------|----------|
| `NavigationServicePort` | `ui/navigation/navigation_service.py` | `destinations(identity_id)`, `resolve(identifier, identity_id)` |

---

## 16. Exception-Modell

### 16.1 Hierarchie

```
Exception
├── JochenXError (core/exceptions.py) — Basis für alle erwarteten Fehler
│   ├── ConfigurationError — Ungültige Konfiguration
│   ├── DatabaseError — Datenbank-Init oder Repository-Fehler
│   ├── PluginError (app/errors.py) — Plugin-Fehler
│   ├── UiError (app/errors.py) — UI-Fehler
│   ├── WorkerError (app/errors.py) — Worker-Fehler
│   ├── ResourceError (app/resources.py) — Resource-Pfad-Fehler
│   ├── SettingsError (app/settings.py) — Settings-Fehler
│   ├── BootstrapError (app/bootstrap.py) — Bootstrap-Fehler
│   ├── IllegalStateTransitionError (app/state_machine.py) — Ungültiger Übergang
│   └── SecurityError (app/security/exceptions.py)
│       ├── PermissionDeniedError
│       ├── PluginSecurityError
│       ├── SecretNotFoundError
│       ├── EncryptionError
│       └── BrokerSecurityError
│
├── RuntimeError
│   └── CircularDependencyError (core/registry.py) — Zirkuläre DI
│
└── PluginSDKError (sdk/errors.py) — SDK-spezifische Fehler
    ├── PluginManifestError — Ungültiges Manifest
    ├── PluginConfigurationError — Config-Fehler
    ├── PluginPermissionError — Unerlaubter Zugriff
    ├── PluginLifecycleError — Ungültiger Lifecycle-Übergang
    ├── PluginDependencyError — Abhängigkeitsfehler
    ├── PluginResourceError — Resource-Zugriffsfehler
    ├── PluginServiceNotAvailableError — Service nicht verfügbar
    └── PluginEventError — Event-Fehler
```

### 16.2 Verwendungsregeln

| Exception | Wann |
|-----------|------|
| `ConfigurationError` | TOML-Parsing-Fehler, fehlende Pflichtfelder |
| `DatabaseError` | SQLite-Connection-Fehler, Migration-Fehler |
| `CircularDependencyError` | Auto-Wiring erkennt Zyklus |
| `IllegalStateTransitionError` | State Machine Violation |
| `BootstrapError` | Stage schlägt fehl |
| `PermissionDeniedError` | RBAC-Verletzung |
| `PluginSecurityError` | Plugin im REJECTED-Status |
| `PluginPermissionError` (SDK) | Plugin versucht ungated API |
| `PluginLifecycleError` (SDK) | Ungültiger Plugin-Zustandsübergang |
| `ResourceError` | Path-Traversal-Versuch |

---

## 17. Konfigurationsmodell

### 17.1 Aktuelle Konfiguration

**Statische Konfiguration** (TOML, immutabel nach Laden):

```toml
# config/default.toml
[application]
name = "JOCHEN X"
version = "0.6.0"        # Konfigurationsversion (kann von pyproject.toml abweichen)
log_level = "INFO"
theme_mode = "system"
developer_enabled = false

[database]
path = "data/jochen_x.sqlite3"

[plugins]
directory = "plugins"
```

**Hinweis:** Die kanonische Applikationsversion ist `pyproject.toml` → `project.version` (derzeit `0.7.0`). Die Version in `config/default.toml` (`0.6.0`) ist eine Konfigurationsversion und wird unabhängig gepflegt.

**`ApplicationSettings`** (frozen Dataclass):
- `name: str`
- `version: str`
- `log_level: str`
- `theme_mode: ThemeMode`
- `database_path: str`
- `plugin_directory: str`
- `developer_enabled: bool`

### 17.2 Zukünftige Konfiguration

**Runtime Settings** (`app/settings.py`, `SettingsProvider`):
- JSON-basiert, versioniert, atomisch persistiert
- Schema-Migrationen (geordnet, single-step)
- Pluggable Validation via `SettingsValidator` Protocol
- Backup/Restore-Mechanismus
- Atomic Writes via `tempfile` + `os.replace()`

### 17.3 Profile

Profile werden über `config/profile.toml` gesteuert:
- Überschreibt selektiv Werte aus `default.toml`
- Wird von `ConfigurationService.load()` automatisch gemergt
- Persistierung via `ConfigurationService.save_profile()`
- Ermöglicht verschiedene Konfigurationen (Development, Production)

### 17.4 Secrets

- `SecretVault` (`app/security/secret_vault.py`) speichert Secrets in-memory
- Encryption via `ReversibleEncryptionService` (aktuell: Base64, nicht kryptographisch)
- Access-Events: `SecretStored`, `SecretRead`, `SecretDeleted`
- Keine Secrets in Konfigurationsdateien

**Architektonische Schlussfolgerung:** Die aktuelle Encryption-Implementierung (`ReversibleEncryptionService`) ist ein Placeholder. Für den Produktionsbetrieb wird eine echte kryptographische Implementierung benötigt (z.B. AES-256-GCM via `cryptography`-Bibliothek).

---

## 18. Testarchitektur

### 18.1 Unit Tests

**Verzeichnis:** `tests/unit/` (17 Testdateien)

**Hinweis:** Diese Tests prüfen die parallele Codebasis `src/jochen_x/`, nicht die aktiven Top-Level-Module.

Getestete Aspekte:
- DI Container — Scopes, Circular Detection, Thread Safety (`test_di_container.py`)
- Service Registry — Lifecycle, Registration, Resolution (`test_service_registry.py`)
- Event Bus — Subscription, Publish, Priority, Dead-Letter, Thread Safety (`test_event_bus.py`)
- Audit Log — Integrity Hash Chain, Tamper Detection (`test_audit.py`)
- Health Monitor — Status Aggregation, Events (`test_health.py`)
- Metrics Collector — Recording, History, Thread Safety (`test_metrics.py`)
- Structured Logger — JSON Format, Component Filtering (`test_logging.py`)
- Worker Pool — Submit, Priority, Graceful Shutdown (`test_worker_pool.py`)
- Scheduler — Cron Parsing, Cancel, Thread Safety (`test_scheduler.py`)
- Resource Monitor — Thresholds, Leak Detection (`test_resource_monitor.py`)
- Recovery — Escalation L1-L4, Circuit Breaker (`test_recovery.py`)
- Security — Permissions, Policies, Input Validation (`test_security.py`)
- Plugin Context — Sandbox, Lifecycle, Isolation (`test_plugin_context.py`)
- Lifecycle Manager — Bootstrap, Start, Pause, Resume, Recovery (`test_lifecycle.py`)
- State Machine — Transitions, Concurrency (50 Threads) (`test_state_machine.py`)
- Bootstrap — Steps, Fail-Fast, Shutdown (`test_bootstrap.py`)
- Runtime Host — Full Lifecycle (`test_runtime_host.py`)

### 18.2 Integration Tests

**Verzeichnis:** `tests/integration/` (4 Testdateien)

- Event Bus Integration: Cross-Component Communication, 400 Events under Load
- Concurrency Integration: WorkerPool + Scheduler, 100 Concurrent Tasks
- Plugin Integration: Full Lifecycle mit Real Components
- Runtime Integration: Full Bootstrap, Shutdown, Recovery, 10 Concurrent Start/Stop

### 18.3 Recovery Tests

**Verzeichnis:** `tests/recovery/` (1 Testdatei)

- Vollständige Escalation L1 durch L4
- Retry-Exhaustion
- Determinism-Garantie
- Multi-Component-Isolation
- 16 Concurrent Recovery Threads

### 18.4 Security Tests

**Verzeichnis:** `tests/security/` (1 Testdatei)

- Default Deny
- Least Privilege
- Adversarial Input Validation (Empty, None, NaN, Inf, Bool-as-Int)
- Permission Bypass Attempts (Case Sensitivity, Similar Names)
- Thread Safety

### 18.5 Foundation-Tests

**Verzeichnis:** `tests/` (Root-Level, 7 Testdateien)

- `test_core.py` — Core-Modul-Tests
- `test_sdk.py` — SDK-Modul-Tests
- `test_developer.py` — Developer-Platform-Tests
- `test_foundation.py` — Foundation-Integrationstests
- `test_application_foundation.py` — Application-Foundation-Tests
- `test_security_foundation.py` — Security-Foundation-Tests
- `test_navigation.py` — Navigation-UI-Tests (benötigt Qt)

### 18.6 Teststrategie

- **Keine Qt-Abhängigkeit** für Unit/Integration Tests (außer `test_navigation.py`)
- **Thread Safety** wird in fast allen Testdateien explizit geprüft
- **Deterministisch:** Kein `time.sleep()` in Tests, keine externen Abhängigkeiten
- **Isolation:** Jeder Test erstellt seine eigene Instanz
- **Fixtures:** Wiederverwendbare Factories und Fakes
- **Qt-Tests:** `QT_QPA_PLATFORM=offscreen` für Headless-Betrieb

---

## 19. Erweiterungsleitfaden

### 19.1 Neue Runtime-Komponente erstellen

1. **Protocol definieren** in `core/` (falls interface-würdig):
```python
class MyProtocol(Protocol):
    def operation(self) -> Result: ...
```

2. **Implementierung** in `app/` oder `services/`:
```python
class MyService:
    def __init__(self, dependency: OtherService) -> None: ...
    def operation(self) -> Result: ...
```

3. **Bootstrap Stage** erstellen oder existierende erweitern:
```python
@dataclass(frozen=True, slots=True)
class MyStage:
    name: str = "MyStage"
    phase: StartupPhase = StartupPhase.FINALIZE

    def execute(self, context: BootstrapContext) -> None:
        service = MyService(context.registry.get(OtherService))
        context.registry.register(MyProtocol, service)
```

4. **Stage in `default_stages()` registrieren**

5. **Tests schreiben** in `tests/`

### 19.2 Plugin erstellen (SDK)

```python
from sdk import Plugin, PluginMetadata, PluginCategory, PluginPermission

class MyPlugin(Plugin):
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            identifier="com.example.my-plugin",
            name="My Plugin",
            version="1.0.0",
            api_version="1.0.0",
            author="Author",
            description="Description",
            category=PluginCategory.GENERAL,
            permissions=frozenset({PluginPermission.EVENTS_SUBSCRIBE}),
        )

    def on_initialize(self) -> None:
        self.context.logger.info("Initialized")

    def on_start(self) -> None:
        self.context.events.subscribe("app.ready", self._on_ready)

    def on_stop(self) -> None:
        pass

    def _on_ready(self, event) -> None:
        self.context.logger.info("Application ready")
```

Manifest (`plugin.toml`):
```toml
id = "com.example.my-plugin"
version = "1.0.0"
required_application_version = "0.7.0"
```

### 19.3 Recovery Strategy erweitern

**Architektonische Schlussfolgerung:** In der aktuellen aktiven Codebasis existiert kein dediziertes Recovery-Strategy-Pattern. Der `CentralErrorHandler` in `app/errors.py` übernimmt die Fehlerklassifikation. Eine Erweiterung würde folgen:

1. Neue `ErrorCategory` hinzufügen (falls benötigt)
2. Mapping in `_CATEGORY_BY_TYPE` erweitern
3. Optional: Custom Handler-Logik in `CentralErrorHandler.handle()`

### 19.4 Neuen Service registrieren

```python
# In einer Bootstrap Stage:
def execute(self, context: BootstrapContext) -> None:
    # Abhängigkeiten auflösen
    events = context.events
    logger = context.logger

    # Service erstellen
    service = MyService(events=events, logger=logger)

    # Registrieren
    context.registry.register(MyService, service)

    # Optional: Als Disposable tracken
    context.disposables.register(service)
```

---

## 20. Architecture Decision Records

### ADR-001: Explicit Core Boundaries

**Status:** Accepted

**Problem:** Wie hält man Core-Module sauber, vermeidet globalen State und bewahrt Dependency Inversion?

**Lösung:** Core-Module exponieren Ports und Value Types. Assembly erfolgt im ApplicationHost. Plugin-Code wird niemals durch die Foundation importiert. `PluginLoader` liest ausschließlich TOML-Manifeste.

**Begründung:** Bewahrt Dependency Inversion, vermeidet globalen State, hält Platform-Implementierungen außerhalb des Startup-Pfades.

**Konsequenzen:** Strikte Trennung von Discovery und Execution. Plugin-Code-Import erst in `PluginActivationStage` (ADR-011).

---

### ADR-002: Explicit Event Delivery Modes

**Status:** Accepted

**Problem:** Wie soll der EventBus synchrone vs. asynchrone Delivery handhaben?

**Lösung:** Synchrones Publishing für deterministische Kurznotifikationen. Asynchroner Entry Point für non-blocking Delivery. Consumers ownen die Executor-Integration.

**Begründung:** Core kann keinen laufenden Event Loop voraussetzen. Bootstrap-Events müssen synchron abgeschlossen sein.

**Konsequenzen:** Plugin-Lifecycle-Events und Security-Events werden synchron publiziert.

---

### ADR-003: Developer Platform is Opt-In

**Status:** Accepted

**Problem:** Sollen Diagnostics immer aktiv oder optional sein?

**Lösung:** Diagnostics sind ein separates Package (`developer/`), standardmäßig deaktiviert (`developer_enabled = false`).

**Begründung:** Startup-Performance bewahren. Diagnostics sind kein Production-Dependency.

**Konsequenzen:** `DeveloperToolsStage` prüft `developer_enabled` und überspringt bei `false`.

---

### ADR-004: Plugin Security Integration Timing

**Status:** Resolved by ADR-011

**Problem:** `PluginDiscoveryStage` (LOAD_PLUGINS) und `SecurityBootstrapStage` (FINALIZE) haben eine Timing-Lücke. Plugins werden ohne Sicherheitsvalidierung katalogisiert.

**Lösung:** ADR-011 führt `PluginSecurityStage` ein, die in LOAD_PLUGINS nach Discovery läuft.

**Konsequenzen:** PluginCatalog enthält nur security-geprüfte Plugins.

---

### ADR-005: Plugin Integrity Validation

**Status:** Open

**Problem:** `signature_status` ist hardcoded auf `"unverified"`. Keine Signatur- oder Hash-Validierung vorhanden.

**Alternativen:**
- A: Kryptographische Signatur (detached `.sig`)
- B: Content-Hash (SHA-256)
- C: Externe Tooling-Validierung

**Konsequenzen bei Entscheidung:** Manifest-Schema-Erweiterung, Performance-Impact bei Discovery, eventuell neue Dependency (`cryptography`).

---

### ADR-006: Plugin Permission Model

**Status:** Open

**Problem:** `PluginStatus.permissions` ist hardcoded auf `()`. `plugin.toml` unterstützt keine Permission-Deklaration.

**Alternativen:**
- A: Manifest-deklariert mit statischer Validierung
- B: Capability-based Sandboxing via `PluginContext`
- C: Runtime-Enforcement an API-Boundary

**Hinweis:** Das SDK implementiert bereits 10 Permissions und Enforcement im `PluginContext`. Die Integration mit dem Host steht aus.

---

### ADR-007: Plugin Dependency Resolution

**Status:** Open

**Problem:** Keine Inter-Plugin-Abhängigkeiten. Plugins sind unabhängig.

**Alternativen:**
- A: Manifest-deklariert mit topologischer Sortierung
- B: Optional Dependencies mit Runtime-Resolution
- C: Keine Inter-Plugin-Dependencies (shared Services only)

---

### ADR-008: Plugin Context Definition

**Status:** Resolved by ADR-010 and ADR-011

**Problem:** Plugins benötigen Zugriff auf Foundation-Services, aber `ApplicationContext` exponiert alles.

**Lösung:** SDK-mediated Access (Option C). Plugins interagieren ausschließlich über die SDK-Facades.

---

### ADR-009: Plugin Isolation Strategy

**Status:** Resolved by ADR-011

**Problem:** Wie werden Plugins zur Laufzeit isoliert?

**Lösung:** Thread-basierte Isolation (Option C). Plugins laufen in dedizierten Threads. `PluginContext` beschränkt die API-Oberfläche.

**Zukünftig:** Subprocess-Isolation (Option B) als Opt-in für untrusted Plugins.

---

### ADR-010: Plugin SDK Architecture

**Status:** Accepted (v0.7.1)

**Problem:** Plugins benötigen eine stabile, versionierte API ohne Kopplung an Foundation-Interna.

**Lösung:** Dediziertes `sdk/`-Package als einzige öffentliche Schnittstelle. Unabhängige Versionierung (`SDK_VERSION` und `SDK_API_VERSION`).

**Begründung:** Foundation-Refactoring bricht keine Plugins. SDK-Surface ist explizit und testbar.

**Konsequenzen:** Intentionale Typ-Duplikation zwischen SDK und Foundation. Minor-Release bei neuen Required Fields.

---

### ADR-011: SDK-Host-Integration

**Status:** Accepted (v0.8.0)

**Problem:** Kein Host-Code referenziert das SDK. Lücke zwischen SDK-Surface und Bootstrap-Pipeline.

**Lösung:** 9 Sub-Entscheidungen (D1-D9):
- D1: Adapter Pattern für Manifest-Typen
- D2: Zwei-Phasen Plugin-Lifecycle (Security + Activation)
- D3: `PluginSecurityStage` in LOAD_PLUGINS
- D4: `PluginActivationStage` in FINALIZE
- D5: Reverse-Order Shutdown
- D6: Core Extensions bleiben inert
- D7: Neue BootstrapContext-Felder
- D8: Neue Events (`PLUGIN_ACTIVATING`, `PLUGIN_ACTIVATED`)
- D9: Version 0.8.0

**Konsequenzen:** SDK wird operational. ADR-004 und ADR-009 gelöst. Erste Plugin-Import-Stelle entsteht in FINALIZE.

---

## 21. Zukunftsroadmap

### 21.1 SDK-Host-Integration (Paket 5, v0.8.0)

**Status:** In Arbeit (ADR-011 dokumentiert, Implementation ausstehend)

- `PluginSecurityStage` in LOAD_PLUGINS Phase
- `PluginActivationStage` in FINALIZE Phase
- Shutdown-Integration (Reverse-Order `runtime.shutdown()`)
- Neue BootstrapContext-Felder: `admitted_manifests`, `plugin_runtimes`
- Neue Events: `PLUGIN_ACTIVATING`, `PLUGIN_ACTIVATED`

### 21.2 Plugin-Manifest-Erweiterung (Paket 6)

**Status:** Geplant

- Erweitertes `plugin.toml`-Schema mit Permissions, Dependencies, API-Version, Category
- Lösung von ADR-005, ADR-006, ADR-007
- Signaturprüfung oder Hash-Validierung
- Dependency-Resolution mit topologischer Sortierung

### 21.3 Chat-UI und KI-Integration (Paket 7)

**Status:** Geplant

- AI Gateway mit Multi-Provider-Support
- Conversation Management (SQLite-backed)
- Streaming-Response-Rendering
- Tool-Calling-Integration

### 21.4 Trading Foundation

**Architektonische Schlussfolgerung:** Basierend auf `BrokerSecurity` und `BrokerAccessPolicy` in `app/security/` ist eine Trading-Integration architektonisch vorbereitet. Benötigt:
- Broker-Adapter (Interactive Brokers, etc.)
- Marktdaten-Streaming
- Order-Management
- Portfolio-Tracking

### 21.5 AI Foundation

- Multi-Provider-Routing (bereits vorbereitet: `ai/gateway.py` + `core/ai_contracts.py`)
- Streaming-Provider-Integration
- Embedding-Provider für RAG
- Tool-Calling für Agenten-Workflows

### 21.6 Weitere Zukunftsperspektiven

| Bereich | Beschreibung |
|---------|-------------|
| Alpha-Release | Feature-complete Core Runtime + erste Plugins |
| Produktionsbetrieb | Echte Kryptographie, Performance-Optimierung |
| Cloud-Integration | Optionale Cloud-Sync für Settings/Plugins |
| GPU-Unterstützung | Lokale LLM-Inference via GPU |
| Multi-Agent-System | Koordination mehrerer KI-Agenten |

---

## 22. Architecture Freeze

### 22.1 Eingefrorene Bestandteile

Die folgenden Komponenten sind unter Architecture Freeze (v1.0.0):

| Komponente | Freeze-Scope |
|------------|-------------|
| `core/events.py` | EventBus-API, Event-Dataclass |
| `core/registry.py` | ServiceRegistry-API, Lifetime-Enum |
| `core/lifecycle.py` | LifecycleManager-API, LifecycleState-Enum |
| `core/version.py` | Version-Dataclass, VersionManager-API |
| `core/extensions.py` | 5 Extension Protocols |
| `core/observability.py` | HealthCheck-Protocol, HealthStatus |
| `app/state_machine.py` | ApplicationState-Enum, Transition Table |
| `app/bootstrap.py` | BootstrapStage-Protocol, StartupPhase-Enum |
| `app/events.py` | ApplicationEventName-Enum, Event-Dataclasses |
| `sdk/__init__.py` | Öffentliche API-Surface (48 Symbole) |
| `sdk/manifest.py` | PluginMetadata-Felder, PluginPermission-Enum |
| `sdk/plugin.py` | Plugin-Basisklassen, PluginLifecycleState |

### 22.2 Erlaubte Änderungen

| Änderungstyp | Erlaubt? | Bedingung |
|--------------|----------|-----------|
| Bugfix in Implementierung | Ja | Keine API-Änderung |
| Neue optionale Felder | Ja | Default-Werte, Minor-Version-Bump |
| Neue Event-Typen | Ja | Minor-Version-Bump |
| Neue Bootstrap Stages | Ja | Bestehende Stages unverändert |
| Performance-Optimierung | Ja | Verhalten unverändert |
| Interne Refactorings | Ja | API-Surface unverändert |

### 22.3 ADR-pflichtige Änderungen

| Änderungstyp | Begründung |
|--------------|------------|
| Entfernung eines eingefrorenen Symbols | Breaking Change |
| Änderung der Transition Table | Lifecycle-Semantik |
| Neues Plugin-Lifecycle-State | Plugin-API-Contract |
| Änderung der Bootstrap-Phasenreihenfolge | Determinismus-Garantie |
| Neue Required Fields in PluginMetadata | Plugin-Kompatibilität |
| Änderung der SDK-API-Version (Major) | SDK-Contract |
| Entfernung/Umbenennung eines Protocols | Adapter-Kompatibilität |

### 22.4 Versionierungsstrategie

| Artefakt | Ort | Track |
|----------|-----|-------|
| Applikation | `pyproject.toml` → `project.version` | `0.7.0` |
| SDK Package | `sdk/version.py` → `SDK_VERSION` | `0.7.1` |
| SDK API | `sdk/version.py` → `SDK_API_VERSION` | `1.0.0` |

Regeln:
- **Major:** Breaking Changes an öffentlichen APIs
- **Minor:** Additive Erweiterungen (neue Events, neue optionale Felder)
- **Patch:** Bugfixes ohne API-Änderung
- SDK-Version und API-Version sind unabhängig voneinander
- API-Version ändert sich nur bei Plugin-API-Surface-Änderungen

---

## 23. Glossar

| Begriff | Definition |
|---------|-----------|
| **ApplicationContext** | Frozen Dataclass mit allen aufgelösten Services. Immutable nach Bootstrap. |
| **ApplicationHost** | Top-Level-Orchestrator. Besitzt EventBus, WorkerPool, StateMachine. |
| **Architecture Freeze** | Zustand, in dem öffentliche APIs nicht mehr geändert werden dürfen. |
| **Auto-Wiring** | Automatische Parameter-Auflösung über Type Hints bei DI. |
| **Bootstrap** | Deterministische Startup-Sequenz in 4 Phasen mit 11 Default-Stages (+ optionale wie SecurityBootstrapStage). |
| **BootstrapContext** | Mutable Accumulator während des Bootstrap. |
| **BootstrapStage** | Protocol für eine Initialisierungseinheit innerhalb einer Phase. |
| **Capability Model** | Security-Modell: Zugriff nur mit explizit deklarierter Capability. |
| **Circular Dependency** | Zyklus in der DI-Auflösungskette. Wird zur Laufzeit erkannt. |
| **Composition Root** | Einziger Ort der Abhängigkeitsverdrahtung (ApplicationHost). |
| **CancellationToken** | Kooperatives Abbruch-Signal für Background-Tasks. |
| **Default Deny** | Security-Prinzip: Ohne explizite Erlaubnis ist alles verboten. |
| **Disposable** | Protocol für deterministische Ressourcenfreigabe. |
| **EventBus** | In-Process Pub/Sub mit Glob-Patterns und Prioritäten. |
| **EventDelivery** | Diagnostik-Record über eine Event-Auslieferung. |
| **Extension Protocol** | Minimaler Vertrag (`identifier: str`) für Erweiterungspunkte. |
| **Frozen Dataclass** | Immutable Datentyp. Thread-safe by design. |
| **Glob Pattern** | `fnmatch`-kompatibler Pattern für Event-Subscriptions. |
| **Lifetime** | DI-Strategie: SINGLETON, TRANSIENT oder SCOPED. |
| **Manifest-Only Discovery** | Plugin-Erkennung ohne Code-Import. |
| **Performance Mode** | Betriebsmodus (NORMAL, GAMING, IDLE, etc.) der Resource-Steuerung. |
| **PluginCatalog** | Immutable Snapshot der entdeckten Plugin-Identifier. |
| **PluginContext** | Isolierter, permission-gated Zugriff für einen Plugin. |
| **PluginManifest** | 3-Feld Value Type aus `plugin.toml` (`identifier`, `version`, `required_application_version`). Foundation-intern. |
| **PluginMetadata** | 11-Feld Enterprise Manifest (SDK, validiert). |
| **PluginRuntime** | Lifecycle-Driver für Plugin-Instanzen. |
| **Port** | Protocol-Definition in einer inneren Schicht. |
| **Adapter** | Konkrete Implementierung eines Ports in einer äußeren Schicht. |
| **RLock** | Reentrant Lock. Erlaubt verschachtelte Akquisition im gleichen Thread. |
| **SDK** | Plugin Software Development Kit. Einzige öffentliche Plugin-API. |
| **ServiceDescriptor** | Diagnostik-Metadaten über eine Service-Registrierung. |
| **ServiceProvider** | Read-only DI Facade für Konsumenten. |
| **ServiceRegistry** | DI Container mit Auto-Wiring und Lifetime-Management. |
| **ServiceScope** | Scoped Lifetime Container. Context Manager. |
| **Sticky Event** | Event, das für späte Subscriber bewahrt wird. |
| **ThemeTokens** | Design-Token-Set für Theme-Generierung. |
| **Trust Ledger** | In-Memory Dictionary: Plugin-Identifier → TrustLevel. |
| **Zero Trust** | Security-Architektur: Kein Plugin wird ohne Prüfung vertraut. |

---

## 24. Anhang

### A.1 Bootstrap-Ablauf (Sequenzdiagramm)

```
ApplicationHost          StartupSequence       BootstrapManager        Stages
     │                        │                       │                  │
     │──start()──────────────→│                       │                  │
     │                        │──begin(root)─────────→│                  │
     │                        │                       │──creates──→BootstrapContext
     │                        │←─────────────────────│                  │
     │                        │                       │                  │
     │                        │──transition(INITIALIZING)                │
     │                        │──run_phase(INITIALIZE)→│                  │
     │                        │                       │──execute()──────→│ Environment
     │                        │                       │──execute()──────→│ Configuration
     │                        │                       │──execute()──────→│ Logging
     │                        │                       │──execute()──────→│ Database
     │                        │                       │──execute()──────→│ Registry
     │                        │                       │──execute()──────→│ Theme
     │                        │                       │──execute()──────→│ Scheduler
     │                        │←─────────────────────│                  │
     │                        │                       │                  │
     │                        │──emit(ApplicationStarting)              │
     │                        │──emit(ApplicationStarted)               │
     │                        │──transition(LOADING_PLUGINS)            │
     │                        │──run_phase(LOAD_PLUGINS)→│              │
     │                        │                       │──execute()──────→│ PluginDiscovery
     │                        │←─────────────────────│                  │
     │                        │                       │                  │
     │                        │──transition(LOADING_RESOURCES)          │
     │                        │──run_phase(LOAD_RESOURCES)→│            │
     │                        │                       │──execute()──────→│ Resource
     │                        │←─────────────────────│                  │
     │                        │                       │                  │
     │                        │──run_phase(FINALIZE)──→│                  │
     │                        │                       │──execute()──────→│ Security
     │                        │                       │──execute()──────→│ Developer
     │                        │                       │──execute()──────→│ DI Validation
     │                        │←─────────────────────│                  │
     │                        │                       │                  │
     │                        │──build_context()─────→│                  │
     │                        │←─ApplicationContext───│                  │
     │                        │──transition(READY)                       │
     │                        │──emit(ApplicationReady)                  │
     │←─ApplicationContext────│                       │                  │
```

### A.2 State Machine (Zustandsdiagramm)

```
                    ┌──────────────────────────────────────────────┐
                    │                                              │
    ┌───────────┐   │   ┌──────────────┐   ┌──────────────────┐   │
    │  STARTING ├───┼──→│ INITIALIZING ├──→│ LOADING_PLUGINS  │   │
    └─────┬─────┘   │   └──────┬───────┘   └────────┬─────────┘   │
          │         │          │                     │             │
          │         │          │ (Fehler möglich)    │             │
          │         │          ↓                     ↓             │
          │         │   ┌──────────────────────────────────────┐   │
          │         │   │          LOADING_RESOURCES           │   │
          │         │   └─────────────────┬────────────────────┘   │
          │         │                     │                        │
          │         │                     ↓                        │
          │         │            ┌────────────────┐                │
          │         │            │     READY      │←───────────┐   │
          │         │            └───┬────┬────┬──┘            │   │
          │         │                │    │    │               │   │
          │         │                ↓    │    ↓               │   │
          │         │         ┌──────┐    │  ┌────────┐        │   │
          │         │         │ BUSY ├────┘  │UPDATING├────────┘   │
          │         │         └──────┘       └───┬────┘            │
          │         │                            │                 │
          │         │                            ↓                 │
          │         │                 ┌──────────────────┐         │
          │         │                 │RESTART_REQUIRED  │         │
          │         │                 └────────┬─────────┘         │
          │         │                          │                   │
          │         └──────────────────────────┼───────────────────┘
          │                                    │
          │      Alle Zustände können zu SHUTTING_DOWN:
          │                                    │
          │                                    ↓
          │                         ┌──────────────────┐
          └────────────────────────→│  SHUTTING_DOWN   │
                                    └────────┬─────────┘
                                             │
                                             ↓
                                    ┌──────────────────┐
                                    │    SHUTDOWN      │ (terminal)
                                    └──────────────────┘
```

### A.3 Plugin Lifecycle

```
    ┌──────────┐      initialize()     ┌─────────────┐
    │ UNLOADED ├──────────────────────→│ INITIALIZED │
    └──────────┘                       └──────┬──────┘
                                              │
                                        start()│
                                              ↓
                                       ┌───────────┐
                                       │  STARTED  │
                                       └─────┬─────┘
                                             │
                                       stop()│
                                             ↓
                                       ┌───────────┐
                                       │  STOPPED  │ (terminal)
                                       └───────────┘

    Fehler in initialize() oder start():
                                       ┌───────────┐
                                       │  FAILED   │ (terminal)
                                       └───────────┘
```

### A.4 Abhängigkeitsdiagramm (Schichten)

```
┌─────┐
│ UI  │──→ App, Core, Config, Styles, Plugins
└──┬──┘
   │
┌──┴───────┐
│Developer │──→ Core
└──────────┘
   │
┌──┴──────┐
│Services │──→ (nur Stdlib)
└─────────┘
   │
┌──┴──┐
│ SDK │──→ (nur Stdlib, intra-SDK)
└─────┘
   │
┌──┴─────┐
│Plugins │──→ Core (Version, VersionManager)
└────────┘
   │
┌──┴──┐
│ App │──→ Core, Config, Database, Styles, Plugins
└─────┘
   │
┌──┴───┐
│ Core │──→ (nur Stdlib)
└──────┘
```

### A.5 Thread-Modell

```
┌─────────────────────────────────────────────────────────┐
│                    Main (UI) Thread                      │
│                                                         │
│  Qt Event Loop ←──── UiDispatcher.post(callback)        │
│       │                                                 │
│  Signal/Slot ←──── Navigation, Theme, StatusBar         │
│       │                                                 │
│  Widget Updates ←── ChatPage, Dashboard, Sidebar        │
└─────────────────────────────────────────────────────────┘
         ↕ (QueuedConnection)
┌─────────────────────────────────────────────────────────┐
│                   QThreadPool Workers                    │
│                                                         │
│  QRunnable Tasks ←── WorkerPool.submit()                │
│       │                                                 │
│  CancellationToken ←── Cooperative Cancellation         │
│       │                                                 │
│  TaskHandle ←── Result/Error/Cancelled Signals          │
└─────────────────────────────────────────────────────────┘
         ↕ (threading.Timer, daemon)
┌─────────────────────────────────────────────────────────┐
│                    Timer Threads                         │
│                                                         │
│  Timeout-Überwachung für WorkerPool Tasks               │
│  StatusBar QTimer (1s) für Worker-Count-Polling         │
└─────────────────────────────────────────────────────────┘
         ↕ (asyncio)
┌─────────────────────────────────────────────────────────┐
│                   Scheduler Thread                       │
│                                                         │
│  asyncio Event Loop ←── TaskScheduler                   │
│       │                                                 │
│  Scheduled Tasks ←── delay, interval, retry, timeout    │
└─────────────────────────────────────────────────────────┘
```

### A.6 Komponentendiagramm (Registrierte Services)

Die folgende Tabelle zeigt alle im `ServiceRegistry` registrierten Services nach Bootstrap:

| Service Key | Lifetime | Registriert in |
|-------------|----------|----------------|
| `ServiceRegistry` | SINGLETON | RegistryStage |
| `EventBus` | SINGLETON | RegistryStage |
| `VersionManager` | SINGLETON | RegistryStage |
| `DisposableRegistry` | SINGLETON | RegistryStage |
| `ThemeEngine` | SINGLETON | ThemeStage |
| `TaskScheduler` | SINGLETON | SchedulerStage |
| `PluginLoader` | SINGLETON | PluginDiscoveryStage |
| `PluginCatalog` | SINGLETON | PluginDiscoveryStage |
| `ResourceManager` | SINGLETON | ResourceStage |
| `SecurityManager` | SINGLETON | SecurityBootstrapStage |
| `EncryptionService` (impl: `ReversibleEncryptionService`) | SINGLETON | SecurityBootstrapStage |
| `SecretVault` | SINGLETON | SecurityBootstrapStage |
| `PermissionManager` | SINGLETON | SecurityBootstrapStage |
| `IdentityManager` | SINGLETON | SecurityBootstrapStage |
| `AuditLogger` | SINGLETON | SecurityBootstrapStage |
| `ApiKeyManager` | SINGLETON | SecurityBootstrapStage |
| `BrokerSecurity` | SINGLETON | SecurityBootstrapStage |
| `PluginSecurity` | SINGLETON | SecurityBootstrapStage |
| `BackupManager` | SINGLETON | SecurityBootstrapStage |
| `ThreatDetector` | SINGLETON | SecurityBootstrapStage |
| `DeveloperPlatform` | SINGLETON | DeveloperToolsStage (optional) |
| `ServiceProvider` | SINGLETON | DependencyInjectionStage |

### A.7 Event-Katalog

#### Application Events (`app/events.py`, `ApplicationEventName`)

| Event Name | Sticky | Beschreibung |
|------------|--------|-------------|
| `application.starting` | Nein | Bootstrap beginnt |
| `application.started` | Nein | Bootstrap abgeschlossen |
| `application.ready` | Ja | Application bereit |
| `application.state.changed` | Nein | State-Transition |
| `application.plugin.loading` | Nein | Plugin-Discovery |
| `application.plugin.loaded` | Nein | Plugin entdeckt |
| `application.plugin.failed` | Nein | Plugin-Discovery-Fehler |
| `application.configuration.changed` | Nein | Config-Änderung |
| `application.theme.changed` | Ja | Theme gewechselt |
| `application.busy.started` | Nein | Langwierige Operation gestartet |
| `application.busy.finished` | Nein | Langwierige Operation beendet |
| `application.shutdown.requested` | Nein | Shutdown angefordert |
| `application.shutdown.completed` | Nein | Shutdown abgeschlossen |
| `application.error.raised` | Nein | Fehler klassifiziert |

#### Security Events (`app/security/events.py`, `SecurityEventName`)

| Event Name | Beschreibung |
|------------|-------------|
| `security.initialized` | Security-Subsystem bereit |
| `security.secret.stored` | Secret gespeichert |
| `security.secret.read` | Secret gelesen |
| `security.secret.deleted` | Secret gelöscht |
| `security.permission.granted` | Permission gewährt |
| `security.permission.denied` | Permission verweigert |
| `security.apikey.created` | API-Key erstellt |
| `security.apikey.revoked` | API-Key widerrufen |
| `security.plugin.verified` | Plugin verifiziert |
| `security.plugin.rejected` | Plugin abgelehnt |
| `security.threat.detected` | Bedrohung erkannt |
| `security.backup.created` | Backup erstellt |
| `security.backup.restored` | Backup wiederhergestellt |
| `security.broker.authenticated` | Broker authentifiziert |

---

*Ende des Architecture Book v2.0*

*Dieses Dokument basiert ausschließlich auf dem Quellcode-Stand zum Zeitpunkt des Architecture Freeze (Core Runtime v1.0.0, Commit b0c2243). Alle technischen Aussagen sind aus dem Quellcode ableitbar. Wo architektonische Schlussfolgerungen gezogen wurden, ist dies explizit gekennzeichnet.*
