# Bootstrap Baseline 1.0

| Feld               | Wert                                                        |
|--------------------|-------------------------------------------------------------|
| Status             | **APPROVED**                                                |
| Baseline ID        | BOOTSTRAP-BASELINE-1.0                                      |
| Genehmigungsdatum  | 2026-08-01                                                  |
| Ersetzt            | Bootstrap-Implementierung vor RDR-001 (`app/bootstrap.py`)  |
| Autorität          | Bootstrap Modularization Final Audit                        |

---

## 1. Purpose

Bootstrap Baseline 1.0 ist die verbindliche Referenzimplementierung des
`app/bootstrap/`-Pakets. Sie dokumentiert den technischen Ist-Zustand nach
vollständiger Umsetzung von RDR-001 (Bootstrap Modularization).

Alle zukünftigen Bootstrap-Arbeiten müssen diese Baseline bewahren, sofern
keine genehmigte Governance-Änderung (ADR oder RDR) eine Abweichung autorisiert.

---

## 2. Baseline Scope

Das Bootstrap-Paket besteht aus den folgenden Modulen:

| Modul                          | Verantwortung                                      |
|--------------------------------|----------------------------------------------------|
| `app/bootstrap/__init__.py`    | Paket-Fassade, Public API, Re-Exports              |
| `app/bootstrap/types.py`       | Typdefinitionen, Protocols, Datenstrukturen         |
| `app/bootstrap/constants.py`   | Interne Konfigurationskonstanten                   |
| `app/bootstrap/stages_init.py` | INITIALIZE-Phase Stages                            |
| `app/bootstrap/stages_plugin.py` | Plugin-Pipeline Stages und Hilfsfunktionen       |
| `app/bootstrap/stages_late.py` | LOAD_RESOURCES- und FINALIZE-Phase Stages          |
| `app/bootstrap/manager.py`     | BootstrapManager und default_stages()              |

---

## 3. Public API Baseline

### 3.1 Öffentliche Exports (20 Symbole)

Die stabile Paket-Fassade `app/bootstrap/__init__.py` exportiert über `__all__`:

**Types & Protocols:**
- `BootstrapContext` — Mutabler Akkumulator für Bootstrap-Stages
- `BootstrapError` — Fehlertyp für fehlgeschlagene Stages
- `BootstrapStage` — Protocol für isolierte, testbare Bootstrap-Schritte
- `StartupPhase` — Geordnete Bootstrap-Phasen (IntEnum)
- `RejectionCode` — Strukturierte Ablehnungsgründe für Plugin-Validation
- `ValidationDiagnostic` — Per-Plugin Pre-Import Validierungsergebnis

**Manager & Konfiguration:**
- `BootstrapManager` — Orchestrator für phasenbasiertes Bootstrap
- `default_stages()` — Deterministische Standard-Stage-Reihenfolge

**INITIALIZE-Phase Stages:**
- `EnvironmentStage`
- `ConfigurationStage`
- `LoggingStage`
- `DatabaseStage`
- `RegistryStage`
- `ThemeStage`
- `SchedulerStage`

**Plugin-Pipeline Stages:**
- `PluginDiscoveryStage`
- `PluginSecurityStage`
- `PluginActivationStage`
- `PluginRuntimePool`

**Late-Phase Stages:**
- `ResourceStage`
- `DeveloperToolsStage`
- `DependencyInjectionStage`

### 3.2 Interne Re-Exports (2 Symbole)

Zusätzlich re-exportiert `__init__.py` zwei interne Hilfsfunktionen, die
**nicht** Teil von `__all__` sind und nicht als stabile API gelten:

- `_require` — Interne Guard-Funktion für Stage-Dependencies
- `_validate_for_activation` — Konsolidierte Pre-Import Validation

### 3.3 Consumer-Import-Kompatibilität

Alle Consumer importieren über die Paket-Fassade:

```python
from app.bootstrap import BootstrapManager, default_stages
```

Direkte Imports aus internen Modulen (z. B. `from app.bootstrap.manager import ...`)
sind nicht Teil der stabilen API.

---

## 4. Architectural Invariants

Die folgenden Invarianten sind Baseline-Bestandteil und dürfen nur durch
genehmigte Governance geändert werden:

1. **Deklarative Paket-Fassade** — `__init__.py` enthält ausschließlich
   Imports und `__all__`, keine Logik.

2. **Azyklischer Import-Graph** — Die internen Module bilden einen
   gerichteten azyklischen Graphen: `types.py` ← `constants.py` ←
   `stages_init.py` / `stages_plugin.py` / `stages_late.py` ← `manager.py`
   ← `__init__.py`.

3. **BootstrapManager als Orchestrator** — Der `BootstrapManager` ist der
   einzige Einstiegspunkt für die Bootstrap-Ausführung. Stages werden nicht
   direkt aufgerufen.

4. **default_stages() bewahrt Stage-Reihenfolge** — Die Funktion gibt eine
   deterministische, geordnete Sequenz aller Stages zurück.

5. **StartupPhase-Reihenfolge bewahrt** — Die Enum-Werte
   INITIALIZE (1) → LOAD_PLUGINS (2) → LOAD_RESOURCES (3) → FINALIZE (4)
   definieren die unveränderliche Phasenreihenfolge.

6. **Plugin-Runtime-Pipeline bewahrt** — Die Pipeline-Reihenfolge
   Discovery → Integrity → Permission → Dependency → Activation ist
   sicherheitskritisch und darf nicht umgestellt werden.

7. **Keine internen Imports durch `app.bootstrap`** — Consumer dürfen nur
   über die Paket-Fassade importieren, nicht aus internen Modulen.

---

## 5. Runtime Baseline

### 5.1 Bootstrap-Phasensequenz

```
INITIALIZE
    EnvironmentStage
    ConfigurationStage
    LoggingStage
    DatabaseStage
    RegistryStage
    ThemeStage
    SchedulerStage
         ↓
LOAD_PLUGINS
    PluginDiscoveryStage
    PluginSecurityStage
         ↓
LOAD_RESOURCES
    ResourceStage
         ↓
FINALIZE
    PluginActivationStage
    DeveloperToolsStage
    DependencyInjectionStage
```

### 5.2 Plugin-Runtime-Pipeline

```
Discovery (Manifest-Erkennung)
         ↓
Integrity Validation (ADR-005)
         ↓
Permission Authorization (ADR-006)
         ↓
Dependency Resolution (ADR-007)
         ↓
Activation (Import, Instantiation, Wiring, Start)
```

---

## 6. Governance References

| Dokument                             | Relevanz                                    |
|--------------------------------------|---------------------------------------------|
| Architecture Book v2.0               | Verbindliche Architekturreferenz             |
| Development Standard v1.1            | Entwicklungsstandards                       |
| Engineering Specification v0.9.1     | Milestone 0.9 Spezifikation                |
| ADR-005                              | Plugin Integrity Validation                 |
| ADR-006                              | Plugin Permission Model                     |
| ADR-007                              | Plugin Dependency Resolution                |
| ADR-011                              | Plugin Lifecycle Stages                     |
| RDR-001                              | Bootstrap Modularization                    |
| Bootstrap Modularization Final Audit | Abschließende Qualitätsprüfung              |

---

## 7. Regression Baseline

| Metrik                          | Wert                |
|---------------------------------|---------------------|
| Tests bestanden                 | 1019                |
| Regressionen                    | 0                   |
| Import-Kompatibilität           | Verifiziert         |
| Consumer-Kompatibilität         | Verifiziert         |

---

## 8. Change Control

Jede zukünftige Änderung am Bootstrap-Paket, die eines der folgenden betrifft:

- **Paketstruktur** (Module hinzufügen, entfernen, umbenennen)
- **Runtime-Pipeline** (Phasenreihenfolge, Stage-Reihenfolge)
- **Public Exports** (`__all__`-Einträge ändern)
- **BootstrapManager** (API-Signatur, Verhalten)
- **default_stages()** (Stage-Zusammensetzung, Reihenfolge)

erfordert eine genehmigte Governance-Entscheidung in Form von:

- einem neuen **ADR** (Architecture Decision Record), oder
- einem neuen **RDR** (Refactoring Decision Record)

---

## 9. Baseline Declaration

**Bootstrap Baseline 1.0** ist die offizielle technische Baseline für alle
zukünftigen Bootstrap-Entwicklungen ab Milestone 1.0.

Diese Baseline wurde auf Grundlage der vollständig implementierten und
auditierten RDR-001 Bootstrap Modularization etabliert. Sie dokumentiert den
genehmigten und verifizierten Zustand des Bootstrap-Pakets zum
Genehmigungsdatum.
