# JOCHEN X — Architekturübersicht

Diese Datei gibt einen visuellen Überblick über die Gesamtarchitektur.

**Verbindliche Architekturreferenz:** [Architecture Book v2.0](docs/architecture-book-v2.md) (APPROVED / FROZEN).  
Inhaltliche Abweichungen erfordern eine neue Book-Version und dokumentierte ADRs.  
Für Einzelentscheidungen siehe zusätzlich die [ADRs](docs/adr/).

---

## Schichtenarchitektur

Abhängigkeiten zeigen ausschließlich nach innen. Keine äußere Schicht wird von einer inneren importiert.

```mermaid
graph TB
    subgraph "Core (stabil, keine externen Abhängigkeiten)"
        Events["EventBus"]
        Registry["ServiceRegistry"]
        Version["Version / VersionManager"]
        Extensions["Extension Protocols"]
        Lifecycle["LifecycleManager"]
    end

    subgraph "Application (Bootstrap, DI, Security)"
        Host["ApplicationHost"]
        Bootstrap["BootstrapManager"]
        Context["ApplicationContext"]
        Security["SecurityManager\nPluginSecurity\nSecretVault"]
        DI["ServiceProvider"]
    end

    subgraph "Plugins / SDK"
        Loader["PluginLoader\n(manifest-only)"]
        SDK["Plugin SDK\n(einzige Plugin-API)"]
        PluginRuntime["PluginRuntime"]
    end

    subgraph "Services"
        Observability["services/observability.py\nPerformanceMonitor\nProcessMetricSource"]
        SecuritySvc["services/security.py\nSecurityPolicy / CapabilityModel\nSecretManager / AuditHooks"]
    end

    subgraph "Developer (optional)"
        Platform["DeveloperPlatform"]
        Inspector["Inspector"]
    end

    subgraph "UI (PySide6)"
        MainWindow["MainWindow"]
        Navigation["Navigation"]
        Chat["Chat-UI"]
    end

    UI --> Developer --> Services --> Plugins/SDK --> Application --> Core
```

**Referenz:** [ADR-001](docs/adr/001-core-boundaries.md) (Core-Grenzen), [ADR-003](docs/adr/003-optional-developer-platform.md) (Developer opt-in)

---

## Bootstrap-Lifecycle

`ApplicationHost` startet die Anwendung über `BootstrapManager` in vier deterministischen Phasen.

```mermaid
flowchart LR
    subgraph "INITIALIZE"
        E[Environment] --> C[Config] --> L[Logging] --> DB[Database] --> R[Registry] --> T[Theme] --> S[Scheduler]
    end

    subgraph "LOAD_PLUGINS"
        PD[PluginDiscovery] --> PS[PluginSecurity]
    end

    subgraph "LOAD_RESOURCES"
        RS[ResourceManager]
    end

    subgraph "FINALIZE"
        PA[PluginActivation] --> DT[DeveloperTools] --> DI[DI-Validation]
    end

    INITIALIZE --> LOAD_PLUGINS --> LOAD_RESOURCES --> FINALIZE
```

Jede Stage ist ein isoliertes `BootstrapStage`-Objekt, das den gemeinsamen `BootstrapContext` populiert. Nach Abschluss wird der immutable `ApplicationContext` assembliert.

**Referenz:** [docs/architecture.md](docs/architecture.md) (Stage-Tabelle), [ADR-011](docs/adr/011-sdk-host-integration.md) (PluginSecurity/ActivationStage)

---

## Plugin-Lifecycle

Vom Dateisystem bis zum laufenden Plugin durchläuft ein Plugin fünf Phasen. Die Code-Ausführungsgrenze liegt zwischen Security und Activation.

```mermaid
flowchart TD
    TOML["plugin.toml\n(statische Deklaration)"]
    Discovery["PluginDiscoveryStage\nPluginManifest (9 Felder, 3 Pflicht)"]
    Security["PluginSecurityStage\nverify_manifest() → Verdict"]
    Boundary["── Code-Ausführungsgrenze ──"]
    Activation["PluginActivationStage\nimport → Plugin.metadata()\nContextBuilder → Runtime"]
    Running["STARTED\nFacades aktiv: Events, Services,\nConfig, Resources, Logger"]
    Shutdown["Shutdown\nruntime.shutdown()\n(reverse Reihenfolge)"]

    TOML --> Discovery --> Security --> Boundary --> Activation --> Running --> Shutdown

    style Boundary fill:none,stroke:#e74c3c,stroke-width:2,stroke-dasharray:5
```

**Kein Plugin-Code vor der Sicherheitsprüfung.** Discovery liest nur TOML. Security prüft Integrität, API-Version, Berechtigungen und Abhängigkeiten. Erst nach Zulassung wird Python-Code importiert.

**Referenz:** [ADR-001](docs/adr/001-core-boundaries.md) (kein Code-Import), [ADR-010](docs/adr/010-plugin-sdk-architecture.md) (SDK), [ADR-011](docs/adr/011-sdk-host-integration.md) (Integration)

---

## Runtime-Pipeline und Ablehnungsdiagnostik

Die Zulassung eines Plugins durchläuft eine invariante Stufenfolge. `PipelineStage` benennt die Stufen, `PIPELINE_STAGE_REFERENCES` ordnet jeder Stufe ihre Referenz `PL-01`..`PL-05` zu; `PIPELINE_ORDER` fixiert die Reihenfolge.

| Stufe (`PipelineStage`) | Referenz | Prüfgegenstand | Ausführende Stage |
|---|---|---|---|
| `DISCOVERY` | `PL-01` | Anwendungsversions-Kompatibilität (manifest-only) | `PluginDiscoveryStage` |
| `INTEGRITY` | `PL-02` | Integritätsprüfung ([ADR-005](docs/adr/005-plugin-integrity-validation.md)) | `PluginSecurityStage` |
| `API_VERSION_GATE` | `PL-02..PL-03` | SDK-API-Kompatibilität **vor** jedem Code-Import | `PluginSecurityStage` |
| `PERMISSION` | `PL-03` | Berechtigungsautorisierung, default-deny ([ADR-006](docs/adr/006-plugin-permission-model.md)) | `PluginSecurityStage` |
| `DEPENDENCY_RESOLUTION` | `PL-04` | Graph, Versionen, Zyklen ([ADR-007](docs/adr/007-plugin-dependency-resolution.md)) | `PluginSecurityStage` |
| `ACTIVATION` | `PL-05` | Import, Verdrahtung, Start | `PluginActivationStage` |

Jede Ablehnung wird als strukturierte `PipelineRejection` aufgezeichnet — mit Identifikator, Stufe, verletztem Kriterium, Pipeline-Referenz, `RejectionCode` und Begründung. `ValidationDiagnostic` trägt zusätzlich das Ergebnis der konsolidierten Vor-Import-Prüfung.

Am Ende der Aktivierung veröffentlicht die Foundation drei registry-persistente Aggregate, die den `BootstrapContext` überdauern:

| Registry-Eintrag | Inhalt |
|---|---|
| `PluginDiagnosticsReport` | Konsolidierte `PluginDiagnostic`-Einträge aller Stufen (`activated` / `rejected` / `failed`), abfragbar über `for_plugin()`, `for_stage()`, `with_outcome()`, `counts()` |
| `ActivationFailurePool` | `ActivationFailure`-Datensätze fehlgeschlagener Aktivierungen |
| `PluginRuntimePool` | Die aktivierten `PluginRuntime`-Instanzen in Aktivierungsreihenfolge |

Ein Ausfall bei der Aktivierung ist isoliert: die übrigen Plugins werden weiter aktiviert, der Fehlschlag bleibt dokumentiert.

**Referenz:** [docs/architecture.md](docs/architecture.md), [docs/extensions.md](docs/extensions.md) §10, [docs/diagnostics.md](docs/diagnostics.md)

---

## Observability

Metriken, Tracing und Health sind In-Memory-Verträge ohne eigenständiges Sampling; keine Komponente startet einen Thread.

```mermaid
flowchart LR
    subgraph "core/observability.py"
        M["Metrics"]
        HS["HealthStatus / HealthCheck"]
        PHC["PluginHealthCheck"]
        PD["PluginDiagnostic
PluginDiagnosticsReport"]
    end
    subgraph "core/observability_registry.py"
        MR["MetricsRegistry
MetricSource"]
        HR["HealthCheckRegistry"]
    end
    Pipeline["PluginActivationStage"] -->|"registriert"| HR
    Pipeline -->|"registriert"| MR
    Pipeline -->|"registriert"| PD
    HR -->|"run() → run_health_checks()"| HS
    PHC --> HS
    MR -->|"merge(metrics)"| M
    PM["services/observability.py
PerformanceMonitor
ProcessMetricSource"] -->|"MetricSource"| MR
```

| Baustein | Modul | Verantwortung |
|---|---|---|
| `Metrics` | `core/observability.py` | Benannter In-Memory-Recorder (`increment`, `record_duration`, `snapshot`) |
| `HealthCheck` / `HealthStatus` | `core/observability.py` | Health-Protokoll und Ergebniswert |
| `PluginHealthCheck` | `core/observability.py` | Health-Check über den **Live**-Lebenszyklus eines Plugins |
| `PluginDiagnostic(sReport)` | `core/observability.py` | Strukturierte, abfragbare Plugin-Diagnostik |
| `MetricsRegistry` / `MetricSource` | `core/observability_registry.py` | Additiver Registrierungspunkt für zusätzliche Metrikquellen; Namensraum `"<Quelle>.<Metrik>"`, bestehende Werte gewinnen bei Kollision |
| `HealthCheckRegistry` | `core/observability_registry.py` | Registrierungspunkt für `HealthCheck`-Implementierungen; `run()` wertet über `run_health_checks()` aus |
| `ProcessMetricSource` | `services/observability.py` | `MetricSource`-Adapter über `PerformanceMonitor` |

Beide Registrierungspunkte sind **rein additiv**: sie verändern keinen bestehenden Metrik- oder Health-Vertrag.

**Referenz:** [docs/health.md](docs/health.md), [docs/performance.md](docs/performance.md), [docs/diagnostics.md](docs/diagnostics.md)

---

## ServiceRegistry

Einziger Kompositionsmechanismus. Alle Services werden während Bootstrap registriert und über typisierte Schlüssel aufgelöst.

```mermaid
flowchart LR
    Bootstrap -->|"register(Type, instance)"| SR["ServiceRegistry"]
    SR -->|"resolve(Type)"| Consumer
    SR -->|"validate()"| DI["ServiceProvider\n(Facade)"]
    DI -->|"typed access"| App["ApplicationContext"]
```

Plugins erhalten keinen direkten Zugriff auf die `ServiceRegistry`. Stattdessen nutzen sie `PluginServices` — eine eingeschränkte Facade, die nur freigegebene Service-Typen exponiert.

---

## Event-System

Thread-safe, typed, synchron und asynchron. Alle Kommunikation zwischen Schichten läuft über Events.

```mermaid
flowchart LR
    Publisher -->|"Event(name, payload)"| EB["EventBus"]
    EB -->|"pattern matching\npriority ordering"| Sub1["Subscriber 1"]
    EB --> Sub2["Subscriber 2"]
    EB -->|"sticky events"| Late["Late Subscriber"]

    subgraph "Plugin-Zugriff"
        PE["PluginEventBus\n(Facade)"] -->|"permission-gated"| EB
    end
```

| Feature | Beschreibung |
|---|---|
| Typed Events | `ApplicationEvent`-Subklassen mit `EVENT_NAME` und `_payload()` |
| Glob-Patterns | Subscriber können Wildcards verwenden (`application.*`) |
| Sticky Events | Werden an späte Subscriber nachgeliefert |
| Prioritäten | Höhere Priorität wird zuerst bedient |
| Async | `publish_async()` für nicht-blockierende Delivery |

**Referenz:** [ADR-002](docs/adr/002-event-delivery.md) (Delivery-Semantik), [docs/events.md](docs/events.md)

---

## SDK

Das Plugin SDK (`sdk/`) ist die einzige öffentliche API für Plugin-Autoren. Plugins importieren nie aus `core`, `app`, `plugins`, `services` oder `ui`.

```mermaid
flowchart TB
    subgraph "SDK (sdk/)"
        Plugin["Plugin\nBackgroundPlugin\nUIPlugin\nToolPlugin\nWorkflowPlugin"]
        Context["PluginContext"]
        Facades["PluginLogger\nPluginEventBus\nPluginServices\nPluginConfig\nPluginResources\nPluginExtensions"]
        Manifest["PluginMetadata"]
        Runtime["PluginRuntime"]
    end

    subgraph "Foundation (host-side)"
        Builder["PluginContextBuilder"] -->|"build()"| Context
        Context --> Facades
        Runtime -->|"drives lifecycle"| Plugin
    end

    Plugin -->|"metadata()"| Manifest
    Plugin -->|"context.*"| Facades
```

Plugins tragen Funktionalität über `PluginExtensions` an host-definierten Erweiterungspunkten bei; der Host injiziert dazu einen `ExtensionRegistrar`. Registrierung ist strikt additiv und ändert nie eine bestehende Signatur.

**Versionsstand:** `SDK_VERSION` = `0.9.0`, `SDK_API_VERSION` = `1.0.0` (`sdk/version.py`).

**Referenz:** [ADR-010](docs/adr/010-plugin-sdk-architecture.md) (SDK-Architektur), [docs/sdk.md](docs/sdk.md) (Spezifikation)

---

## Sicherheitsmodell

Zero-Trust-Prinzip: kein Plugin wird ohne explizite Zulassung aktiviert.

```mermaid
flowchart LR
    Manifest -->|"verify_manifest()"| PS["PluginSecurity"]
    PS -->|"trust_level()"| TL["Trust-Ledger"]
    TL -->|"TRUSTED/VERIFIED"| Allow["✓ Zulassung"]
    TL -->|"UNTRUSTED"| Deny["✗ Abweisung"]
    TL -->|"REJECTED"| Block["✗ Blockiert"]

    Allow --> Activation
    Deny -->|"PluginRejected event"| Log["Audit-Log"]
    Block -->|"PluginSecurityError"| Log
```

| Komponente | Verantwortung |
|---|---|
| `PluginSecurity` | Trust-Ledger, Manifest-Verifizierung |
| `SecretVault` | Sichere Speicherung sensibler Werte |
| `PermissionManager` | Capability-basierte Zugriffssteuerung |
| `AuditLogger` | Sicherheitsrelevante Ereignisse protokollieren |
| `ThreatDetector` | Erkennung verdächtiger Muster |

**Referenz:** [docs/security.md](docs/security.md), [ADR-004](docs/adr/004-plugin-security-integration.md) (Security-Timing), [ADR-011](docs/adr/011-sdk-host-integration.md) §D3

---

## Datenfluss

Vom Start bis zur laufenden Anwendung:

```mermaid
flowchart TD
    TOML["config/default.toml"] -->|"ConfigurationService"| Settings["ApplicationSettings"]
    Settings --> Bootstrap
    Bootstrap -->|"populiert"| BC["BootstrapContext\n(mutable)"]
    BC -->|"assembliert"| AC["ApplicationContext\n(immutable)"]
    AC --> Host["ApplicationHost"]
    Host -->|"Events"| EB["EventBus"]
    Host -->|"Services"| SR["ServiceRegistry"]
    Host -->|"Plugins"| PR["PluginRuntime[]"]

    SQLite["data/jochen_x.sqlite3"] -->|"ConnectionManager"| BC
    PluginTOML["plugins/*/plugin.toml"] -->|"PluginLoader"| BC
```

---

## Komponentenübersicht

| Komponente | Modul | Verantwortung |
|---|---|---|
| `ApplicationHost` | `app/application_host.py` | Lifecycle-Eigentümer, Start/Shutdown |
| `BootstrapManager` | `app/bootstrap/manager.py` | Deterministische Stage-Ausführung |
| `BootstrapContext` · `PipelineStage` · `PipelineRejection` · `RejectionCode` · `ValidationDiagnostic` | `app/bootstrap/types.py` | Bootstrap-Akkumulator und Pipeline-Typen |
| `PluginDiscoveryStage` · `PluginSecurityStage` · `PluginActivationStage` · `PluginRuntimePool` · `ActivationFailurePool` | `app/bootstrap/stages_plugin.py` | Plugin-Pipeline und ihre registry-persistenten Aggregate |
| `ApplicationContext` | `app/context.py` | Immutables Aggregat aller Services |
| `ServiceRegistry` | `core/registry.py` | Typisierte Service-Registrierung |
| `EventBus` | `core/events.py` | Thread-safe Event-Distribution |
| `VersionManager` | `core/version.py` | Semver-Kompatibilitätsprüfung |
| `Metrics` · `HealthCheck` · `PluginHealthCheck` · `PluginDiagnosticsReport` | `core/observability.py` | Metrik-, Health- und Diagnoseverträge |
| `MetricsRegistry` · `HealthCheckRegistry` · `MetricSource` | `core/observability_registry.py` | Additive Registrierungspunkte der Observability |
| `PerformanceMonitor` · `ProcessMetricSource` | `services/observability.py` | Prozess-Sampling ohne Hintergrund-Thread |
| `PluginLoader` | `plugins/loader.py` | TOML-only Manifest-Discovery |
| `PluginSecurity` | `app/security/plugin_security.py` | Integritäts-, Berechtigungs- und Trust-Validierung |
| `PluginRuntime` | `sdk/plugin.py` | Plugin-Lifecycle-Steuerung |
| `PluginContext` · `PluginExtensions` | `sdk/context.py` | Plugin-scoped Runtime-Aggregat und Erweiterungspunkte |
| `EventDiagnostics` · `ServiceDiagnostics` · `PluginDiagnostics` · `HealthDiagnostics` · `PluginRuntimeDiagnostics` | `developer/contracts.py` | Diagnostik-Ports der Developer Platform |
| `DeveloperPlatform` | `developer/platform.py` | Opt-in Diagnostics und Inspection |
| `MainWindow` | `ui/navigation/main_window.py` | PySide6-Hauptfenster |

---

## ADR-Verzeichnis

| ADR | Thema | Status |
|---|---|---|
| [001](docs/adr/001-core-boundaries.md) | Core-Grenzen | Akzeptiert |
| [002](docs/adr/002-event-delivery.md) | Event-Delivery | Akzeptiert |
| [003](docs/adr/003-optional-developer-platform.md) | Developer Platform opt-in | Akzeptiert |
| [004](docs/adr/004-plugin-security-integration.md) | Security-Timing | Resolved (ADR-011) |
| [005](docs/adr/005-plugin-integrity-validation.md) | Integrity-Validation | APPROVED |
| [006](docs/adr/006-plugin-permission-model.md) | Permission-Model | APPROVED |
| [007](docs/adr/007-plugin-dependency-resolution.md) | Dependency-Resolution | APPROVED |
| [008](docs/adr/008-plugin-context-definition.md) | Plugin-Context | Resolved (ADR-010/011) |
| [009](docs/adr/009-plugin-isolation-strategy.md) | Isolation-Strategy | Resolved (ADR-011) |
| [010](docs/adr/010-plugin-sdk-architecture.md) | SDK-Architektur | Akzeptiert |
| [011](docs/adr/011-sdk-host-integration.md) | SDK-Host-Integration | Akzeptiert |
| [012](docs/adr/012-plugin-security-policy-configuration.md) | Plugin-Security-Policy-Konfiguration | Akzeptiert |
