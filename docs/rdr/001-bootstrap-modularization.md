# RDR-001: Bootstrap Modularization

| Feld                         | Wert                                        |
|------------------------------|---------------------------------------------|
| Status                       | **APPROVED**                                |
| Typ                          | Refactoring Decision Record                 |
| Erstellt                     | 2026-08-01                                  |
| Genehmigt                    | 2026-08-01                                  |
| Betrifft                     | `app/bootstrap.py`                          |
| Governance                   | Draft → Independent Review → Correction → Approval → **Implementation Authorized** |
| Implementation Authorization | Sprint R-01 authorized                      |

---

## 1. Context

### 1.1 Aktuelle Struktur

`app/bootstrap.py` ist ein monolithisches Modul mit **979 Zeilen**, das den
gesamten Bootstrap-Lebenszyklus der Anwendung implementiert:

- **Typdefinitionen** — `BootstrapError`, `StartupPhase`, `RejectionCode`,
  `ValidationDiagnostic`, `BootstrapContext`, `BootstrapStage` (Protocol),
  `PluginRuntimePool`
- **Initialisierungs-Stages** — `EnvironmentStage`, `ConfigurationStage`,
  `LoggingStage`, `DatabaseStage`, `RegistryStage`, `ThemeStage`,
  `SchedulerStage`
- **Plugin-Stages** — `PluginDiscoveryStage`, `PluginSecurityStage`
  (inkl. `_resolve_dependencies`)
- **Späte Stages** — `ResourceStage` (`LOAD_RESOURCES`),
  `PluginActivationStage` (`FINALIZE`, inkl. `_validate_for_activation`,
  `_reject_plugin`), `DeveloperToolsStage` (`FINALIZE`),
  `DependencyInjectionStage` (`FINALIZE`)
- **Orchestrierung** — `default_stages()`, `BootstrapManager`

Das Modul exportiert **22 öffentliche Symbole** über `__all__`.

### 1.2 Motivation

Das Modul ist historisch gewachsen. Die Stages der vier Bootstrap-Phasen
(`INITIALIZE`, `LOAD_PLUGINS`, `LOAD_RESOURCES`, `FINALIZE`), die
Typdefinitionen und der Manager befinden sich in einer einzigen Datei. Dies
erschwert:

- **Auffindbarkeit** — Stages sind nicht nach Phase physisch getrennt, was
  die Navigation in der Datei bei fast 1000 Zeilen aufwendig macht.
- **Review-Effizienz** — Änderungen an einer einzelnen Stage produzieren
  Diffs auf dem gesamten Modul und können Git-Merge-Konflikte verursachen.
- **Selektives Testen** — Alle Stages teilen denselben Modulscope, was
  isolierte Import-basierte Tests verkompliziert.
- **Wartbarkeit** — Das Modul hat eine hohe Dichte an Verantwortlichkeiten
  (Typen, 13 Stages, Orchestrierung), die gegen das Single-Responsibility-
  Prinzip auf Modulebene steht.

### 1.3 Review-Befund (Observation B1)

Die interne Code-Review hat `app/bootstrap.py` als monolithisches Modul
identifiziert, das von einer physischen Aufteilung nach Verantwortlichkeit
profitieren würde — ohne dabei die bestehende Laufzeitpipeline, API oder
Architektur zu verändern.

### 1.4 Wartungsrisiken des aktuellen Zustands

- **Merge-Konflikte**: Parallele Arbeiten an unterschiedlichen Stages
  erzeugen Konflikte in derselben Datei.
- **Kognitive Last**: Entwickler müssen ~1000 Zeilen navigieren, um eine
  spezifische Stage zu finden.
- **Import-Kopplung**: Alle internen Symbole (Hilfsfunktionen,
  Typ-Definitionen, Stage-Klassen) teilen denselben Namespace.

---

## 2. Decision

### 2.1 Entscheidung

`app/bootstrap.py` wird in ein Package `app/bootstrap/` physisch
modularisiert. Die Aufteilung erfolgt nach funktionaler Verantwortlichkeit
und Phase-Zugehörigkeit.

### 2.2 Einschränkungen

- **Keine Architekturänderungen.** Die Schichtarchitektur
  (Core → App → Plugins/SDK → Services → Developer → UI) bleibt unverändert.
- **Keine Verhaltensänderungen.** Die Laufzeitpipeline, Phase-Reihenfolge
  und Stage-Ausführungslogik bleiben identisch.
- **Keine öffentlichen API-Änderungen.** Alle 22 exportierten Symbole
  bleiben über `app.bootstrap` importierbar.

---

## 3. Invariants

Die folgenden Invarianten sind **verbindlich** und gelten für jeden
Refactoring-Sprint:

1. **Runtime-Pipeline bleibt identisch.** Die Ausführungsreihenfolge der
   Stages ändert sich nicht.
2. **Bootstrap-Phase-Reihenfolge bleibt identisch.** `INITIALIZE` →
   `LOAD_PLUGINS` → `LOAD_RESOURCES` → `FINALIZE`.
3. **Öffentliche Imports bleiben identisch.** `from app.bootstrap import X`
   funktioniert für alle 22 Symbole.
4. **`__all__`-Exporte bleiben identisch.** Die 22 Symbole in `__init__.py`:
   - `BootstrapContext`
   - `BootstrapError`
   - `BootstrapManager`
   - `BootstrapStage`
   - `ConfigurationStage`
   - `DatabaseStage`
   - `DependencyInjectionStage`
   - `DeveloperToolsStage`
   - `EnvironmentStage`
   - `LoggingStage`
   - `PluginActivationStage`
   - `PluginDiscoveryStage`
   - `PluginRuntimePool`
   - `PluginSecurityStage`
   - `RegistryStage`
   - `RejectionCode`
   - `ResourceStage`
   - `SchedulerStage`
   - `StartupPhase`
   - `ThemeStage`
   - `ValidationDiagnostic`
   - `default_stages`
5. **`BootstrapManager`-Verhalten bleibt identisch.** `begin()`,
   `run_phase()` und `build_context()` verhalten sich exakt wie vorher.
6. **Plugin-Lebenszyklus bleibt identisch.** Discovery → Security →
   Activation Pipeline ist unverändert.
7. **Sicherheitsvalidierungs-Reihenfolge bleibt identisch.** Integrity →
   API Version Gate → Permission Authorization → Dependency Resolution.
8. **Keine neuen Abhängigkeiten zwischen Schichten.** Es werden keine
   Imports aus äußeren Schichten in innere Schichten eingeführt.
9. **Interne Module importieren nie durch die Package-Fassade.**
   Submodule wie `app.bootstrap.types` oder `app.bootstrap.manager`
   importieren nie über `app.bootstrap` (das `__init__.py`).
10. **Interne Imports referenzieren konkrete Submodule.** Zum Beispiel
    `from app.bootstrap.types import BootstrapContext` oder
    `from app.bootstrap.constants import _LOGS_DIRECTORY`, nicht
    `from app.bootstrap import BootstrapContext` innerhalb des Packages.

---

## 4. Target Structure

Genehmigte Zielstruktur nach Abschluss der Modularisierung:

```
app/bootstrap/
├── __init__.py           Package-Fassade: Re-Export aller 22 Symbole,
│                         identisches __all__, bewahrt Import-Kompatibilität
├── types.py              BootstrapError, StartupPhase, RejectionCode,
│                         ValidationDiagnostic, BootstrapContext,
│                         BootstrapStage (Protocol), PluginRuntimePool
├── constants.py          Gemeinsame interne Konstanten (_CONFIG_DIRECTORY,
│                         _DEFAULT_CONFIG_FILE, _PROFILE_CONFIG_FILE,
│                         _LOGS_DIRECTORY, _LOG_FILE_NAME)
├── stages_init.py        EnvironmentStage, ConfigurationStage, LoggingStage,
│                         DatabaseStage, RegistryStage, ThemeStage,
│                         SchedulerStage
├── stages_plugin.py      PluginDiscoveryStage, PluginSecurityStage,
│                         _resolve_dependencies
├── stages_late.py        ResourceStage (LOAD_RESOURCES),
│                         PluginActivationStage (FINALIZE),
│                         _validate_for_activation, _reject_plugin,
│                         DeveloperToolsStage (FINALIZE),
│                         DependencyInjectionStage (FINALIZE)
└── manager.py            default_stages(), BootstrapManager
```

**Hinweis zu `stages_late.py`:** Dieses Modul fasst die späten Bootstrap-
Stages physisch zusammen: `ResourceStage` (`StartupPhase.LOAD_RESOURCES`)
und die drei `FINALIZE`-Stages. Die Gruppierung ist rein physischer Natur
und vermeidet ein Ein-Klassen-Modul für `ResourceStage`. Die Runtime-Phase-
Zuordnung jeder Stage bleibt unverändert — `ResourceStage.phase` ist und
bleibt `StartupPhase.LOAD_RESOURCES`. Der `BootstrapManager` steuert die
Ausführung weiterhin ausschließlich über das `phase`-Attribut jeder Stage.

### Modulverantwortlichkeiten

| Modul                | Inhalt                                                      | Zeilen (ca.) |
|----------------------|-------------------------------------------------------------|:------------:|
| `__init__.py`        | Re-Exports, `__all__`                                       | ~40          |
| `types.py`           | Typen, Protokolle, Datenklassen, Helpers                    | ~120         |
| `constants.py`       | Gemeinsame interne Konstanten                               | ~15          |
| `stages_init.py`     | 7 Initialisierungs-Stages (`INITIALIZE`)                    | ~190         |
| `stages_plugin.py`   | 2 Plugin-Stages (`LOAD_PLUGINS`) + Dependency Resolution    | ~280         |
| `stages_late.py`     | 1 `LOAD_RESOURCES`-Stage + 3 `FINALIZE`-Stages + Validation | ~250         |
| `manager.py`         | `default_stages()`, `BootstrapManager`                      | ~90          |

---

## 5. Migration Strategy

Die Migration erfolgt in **sechs Refactoring-Sprints**. Jeder Sprint ist
**verhaltensbewahrend** und hinterlässt das Repository in einem
**release-fähigen Zustand**.

### Sprint 1 — Package-Skelett

`app/bootstrap.py` wird zu `app/bootstrap/__init__.py` umbenannt. Die Datei
bleibt zunächst monolithisch. Alle externen Imports funktionieren weiterhin.

### Sprint 2 — Types und Constants extrahieren

`BootstrapError`, `StartupPhase`, `RejectionCode`, `ValidationDiagnostic`,
`BootstrapContext`, `BootstrapStage` (Protocol), `PluginRuntimePool` und
Hilfsfunktionen (`_require`) werden nach `types.py` verschoben.
Gemeinsame Konstanten (`_CONFIG_DIRECTORY`, `_DEFAULT_CONFIG_FILE`,
`_PROFILE_CONFIG_FILE`, `_LOGS_DIRECTORY`, `_LOG_FILE_NAME`) werden nach
`constants.py` verschoben. `__init__.py` re-exportiert die öffentlichen
Symbole.

### Sprint 3 — Initialisierungs-Stages extrahieren

`EnvironmentStage`, `ConfigurationStage`, `LoggingStage`, `DatabaseStage`,
`RegistryStage`, `ThemeStage`, `SchedulerStage` werden nach
`stages_init.py` verschoben. `__init__.py` re-exportiert.

### Sprint 4 — Plugin-Stages extrahieren

`PluginDiscoveryStage`, `PluginSecurityStage` und `_resolve_dependencies`
werden nach `stages_plugin.py` verschoben. `__init__.py` re-exportiert.

### Sprint 5 — Späte Stages extrahieren

`ResourceStage` (`LOAD_RESOURCES`), `PluginActivationStage` (`FINALIZE`),
`_validate_for_activation`, `_reject_plugin`, `DeveloperToolsStage`
(`FINALIZE`), `DependencyInjectionStage` (`FINALIZE`) werden nach
`stages_late.py` verschoben. Die Runtime-Phase-Zuordnung jeder Stage
bleibt unverändert. `__init__.py` re-exportiert.

### Sprint 6 — Manager extrahieren

`default_stages()` und `BootstrapManager` werden nach `manager.py`
verschoben. `__init__.py` wird auf die reine Re-Export-Fassade reduziert.

### Sprint-Invariante

Jeder Sprint endet mit:
- Alle 22 Exporte über `app.bootstrap` verfügbar
- `python -m pytest` erfolgreich
- Keine Verhaltensänderung gegenüber dem vorherigen Sprint

---

## 6. Risks

### 6.1 Zirkuläre Imports

**Risiko:** Submodule importieren gegenseitig und erzeugen
`ImportError` zur Laufzeit.

**Mitigation:** Strenge, azyklische Import-Hierarchie:

```
types.py          ← keine Package-internen Imports
constants.py      ← keine Package-internen Imports
      ↓
stages_*.py       ← importieren nur aus types.py und constants.py
      ↓
manager.py        ← importiert aus types.py und stages_*.py
      ↓
__init__.py       ← importiert aus allen Submodulen (reine Re-Exports)
```

`types.py` und `constants.py` bilden die Basis ohne gegenseitige
Abhängigkeit. `stages_*.py` importieren ausschließlich aus `types.py`
und `constants.py`. Kein Submodul importiert über `__init__.py`. Diese
Hierarchie wird per Code-Review verifiziert.

### 6.2 Git-History-Kontinuität

**Risiko:** Die Umbenennung von `bootstrap.py` zu `bootstrap/__init__.py`
und die Extraktion in Submodule können die `git log --follow`-Nachverfolgung
brechen.

**Mitigation:** Sprint 1 führt ausschließlich die Umbenennung durch
(kein inhaltlicher Edit). Nachfolgende Sprints verwenden `git mv`-äquivalente
Operationen wo möglich. Die logische Historie bleibt über die Commit-Messages
und dieses RDR nachvollziehbar.

### 6.3 Import-Kompatibilität

**Risiko:** Bestehende `from app.bootstrap import X`-Statements in
konsumierenden Modulen brechen nach der Modularisierung.

**Mitigation:** `__init__.py` re-exportiert alle 22 Symbole und bewahrt
`__all__` identisch. Betroffene konsumierende Module (Stand 2026-08-01):

| Datei                                         | Importierte Symbole                        |
|-----------------------------------------------|--------------------------------------------|
| `app/application_host.py`                     | `BootstrapManager`, `PluginRuntimePool`    |
| `app/startup.py`                              | `BootstrapManager`, `StartupPhase`         |
| `app/security/security_manager.py`            | `BootstrapContext`, `StartupPhase`         |
| `ui/navigation/navigation_service.py`         | (diverse Stage-/Typ-Imports)               |
| `tests/test_application_foundation.py`        | (breiter Import aller Typen und Stages)    |
| `tests/test_golden_reference.py`              | (diverse Stage-/Typ-Imports)               |
| `tests/test_activation_validation.py`         | (diverse Stage-/Typ-Imports)               |
| `tests/test_dependency_resolution.py`         | (diverse Stage-/Typ-Imports)               |
| `tests/test_security_foundation.py`           | `BootstrapManager`, `StartupPhase`, `default_stages` |
| `tests/integration/test_plugin_integration.py`| (diverse Stage-/Typ-Imports)               |

Alle diese Imports bleiben nach der Modularisierung funktionsfähig, da
sie über die Package-Fassade (`app.bootstrap`) importieren.

### 6.4 Test-Kompatibilität

**Risiko:** Tests, die Interna von `app.bootstrap` patchen (z.B.
`@patch("app.bootstrap.PluginSecurityStage")`), brechen wenn das Symbol
nun in einem Submodul lebt.

**Mitigation:** Patch-Targets in Tests werden nach jedem Sprint überprüft.
Da die Symbole via `__init__.py` re-exportiert werden, bleiben
`app.bootstrap.X`-Patches funktionsfähig. Tests, die den internen
Modulpfad referenzieren (z.B. `app.bootstrap.stages_plugin.X`), werden
bei Bedarf angepasst — dies ist ebenfalls ein verhaltensbewahrende Änderung.

---

## 7. Success Criteria

Die Modularisierung gilt als abgeschlossen, wenn **alle** der folgenden
Kriterien erfüllt sind:

1. **Alle 22 Exporte bleiben verfügbar.** `from app.bootstrap import X`
   funktioniert für jedes Symbol in `__all__`.
2. **Alle bestehenden Import-Statements funktionieren.** Kein konsumierendes
   Modul muss angepasst werden.
3. **`default_stages()` produziert die identische Stage-Sequenz.** Gleiche
   Stages in gleicher Reihenfolge wie vor der Modularisierung.
4. **Vollständiger Testlauf erfolgreich.** `python -m pytest` besteht
   ohne Fehler.
5. **Golden Reference Plugin besteht.** Das Golden Reference Plugin
   wird erfolgreich entdeckt, validiert und aktiviert.
6. **Keine Laufzeit-Verhaltensänderungen.** Die Anwendung startet und
   verhält sich identisch.
7. **Keine ADR-Änderungen erforderlich.** Kein ADR muss aufgrund dieses
   Refactorings aktualisiert werden.

---

## 8. Out of Scope

Die folgenden Themen sind **explizit ausgeschlossen** und dürfen nicht
im Rahmen dieses RDR bearbeitet werden:

- **Validator-Redesign** — Keine Änderung an der Validierungslogik
  (`_validate_for_activation`, `_resolve_dependencies`).
- **Security-Redesign** — Keine Änderung an der Sicherheitspipeline
  (Integrity → API Version → Permission → Dependency).
- **Pipeline-Redesign** — Keine Änderung an der Bootstrap-Pipeline-
  Architektur (`BootstrapManager`, Phase-Modell).
- **SDK-Redesign** — Keine Änderung am Plugin SDK.
- **Performance-Optimierung** — Kein Profiling, keine Optimierungen.
- **Neue Features** — Keine neuen Stages, keine neuen Typen, keine
  neuen Exporte.
- **Architekturänderungen** — Keine Änderungen an der Schichtarchitektur,
  dem Kompositionsmodell oder der Event-Infrastruktur.

---

## Referenzen

- Architecture Book v2.0: `docs/architecture-book-v2.md`
- Engineering Specification v0.9.1: `docs/milestone-0.9-engineering-spec.md`
- Milestone 0.9 Implementation Plan: `docs/milestone-0.9-implementation-plan.md`
- ADR-005: Plugin Integrity Validation — `docs/adr/005-plugin-integrity-validation.md`
- ADR-006: Plugin Permission Model — `docs/adr/006-plugin-permission-model.md`
- ADR-007: Plugin Dependency Resolution — `docs/adr/007-plugin-dependency-resolution.md`
- ADR-011: SDK Host Integration — `docs/adr/011-sdk-host-integration.md`

---

## Approval Record

| Phase                | Datum      | Ergebnis |
|----------------------|------------|----------|
| Draft                | 2026-08-01 | Erstellt |
| Independent Review   | 2026-08-01 | Abgeschlossen — Befunde dokumentiert |
| Correction Phase     | 2026-08-01 | Alle Review-Befunde adressiert |
| Approval Review      | 2026-08-01 | **PASS** |
| Implementation Auth. | 2026-08-01 | Sprint R-01 autorisiert |

Dieses Dokument ist die verbindliche Governance-Baseline für die
Bootstrap-Modularisierung. Inhaltliche Änderungen an Architektur,
Implementierung, Migration oder Anforderungen sind ab diesem Status
ausschließlich über eine neue Dokumentversion oder einen ADR zulässig.

Detaillierter Approval Record: [`001-bootstrap-modularization-approval-record.md`](001-bootstrap-modularization-approval-record.md)
