# JOCHEN X — Milestone 1.0
# SPR-01 — Baseline Confirmation & RB-1.0 Formalization

## 1. Sprint Metadata

| Feld | Wert |
|---|---|
| Sprint | **SPR-01 — Baseline Confirmation** (Phase A) |
| Status dieses Dokuments | **FINAL** |
| Datum der Feststellung | 2026-08-09 |
| Rolle | Senior Software Architect / Verification Engineer / Baseline-Verantwortlicher |
| Charakter | Read-only-Feststellung — **kein Coding-Sprint**; keine Datei des Bestands verändert |
| Begleitartefakt | [`docs/audits/milestone-1.0-sprint-01-verification-summary.md`](../audits/milestone-1.0-sprint-01-verification-summary.md) |

## 2. Authorization

Sprint Plan 1.0 R0, genehmigt durch **ADW-SPR-1.0-001** (OP-1, APPROVED FOR SPRINT EXECUTION PLANNING); ausdrückliche SPR-01-Freigabe des Projekteigners. Grundlagen: GDR-002 (GR-001 DECIDED, D-1..D-4), Preflight 2026-08-09, IP 1.0 R1.2 (APPROVED).

## 3. Source Gate

Alle Pflichtquellen vorhanden, gelesen, statuskonform: Sprint Plan (DRAFT 1.0 R0, genehmigt als Planungsgrundlage) · Planning Summary R0 (**Pfadhinweis:** tatsächliche Fundstelle `docs/audits/milestone-1.0-sprint-planning-summary-r0.md`, nicht `docs/…` wie im Auftrag — eindeutig, kein STOP) · ADW-SPR-1.0-001 (FINAL) · IP 1.0 R1.2 (APPROVED; §3, §5.5, §9.6) · Charter (APPROVED) · Engineering Spec R1 (APPROVED) · Architecture Book v2.0 (APPROVED/FROZEN) · DevStd v1.1 (APPROVED) · Bootstrap Baseline 1.0 (APPROVED) · GDR-002 (FINAL) · W-8 (CLOSED). **Source Gate: BESTANDEN.**

## 4. Baseline Identity

Die produktive Milestone-Baseline ist die **baseline-geführte Struktur** gemäß Bootstrap Baseline 1.0 und Architecture Book v2.0 (GDR-002 D-1). `src/jochen_x/**` ist gemäß GDR-002 D-2 **stillgelegt, kein Milestone-Bestand, nicht Teil der produktiven Baseline**; seine physische Behandlung ist ausdrücklich nicht Bestandteil von SPR-01 und wurde nicht durchgeführt.

## 5. Productive Tree

| Element | Befund (read-only, 2026-08-09) |
|---|---|
| Einstiegspunkt | `main.py` (vorhanden; enthält **keine** Referenz auf `src/jochen_x` — verifiziert per Volltextsuche) |
| Produktive Pakete | `core/`, `app/` (inkl. `app/bootstrap/`, `app/security/`), `plugins/`, `sdk/`, `services/`, `developer/`, `ui/` |
| Unterstützend | `config/`, `database/`, `data/`, `docs/`, `tests/` |
| Nicht produktiv (Milestone) | `src/` (stillgelegter Parallelbaum `src/jochen_x/**`), Cache-/Artefaktverzeichnisse |

## 6. Baseline Inventory

Der Bestand entspricht der von Bootstrap Baseline 1.0 / Architecture Book v2.0 beschriebenen Schichtstruktur (Core → App → Plugins/SDK → Services → Developer → UI). Die vom IP §5.5 als bestehend geführten Dateien (u. a. `app/bootstrap/types.py`, `app/bootstrap/manager.py`, `core/observability.py`, `plugins/loader.py`, `sdk/version.py`) sind im Working Tree vorhanden. **Hinweis:** Teile dieses Bestands liegen als vorbestehende, uncommittete Working-Tree-Änderungen bzw. untracked Dateien vor (siehe Finding F-SPR01-01 / OPEN BASELINE IDENTIFIER). SPR-01 hat diesen Bestand ausschließlich gelesen.

## 7. Test Inventory

Teststruktur der baseline-geführten Struktur: `tests/` (Wurzelebene) und `tests/integration/` (anteilig). Zuordnungsmethode: **Import-Analyse** — eine Testdatei gehört zum stillgelegten Bestand genau dann, wenn sie aus dem Paket `jochen_x` importiert (`^(from|import)\s+(src\.)?jochen_x`); String-Vorkommen („jochen_x" als Logger-Name/Pfad) gelten ausdrücklich **nicht** als Zugehörigkeitsnachweis. Zählmethode: `pytest --collect-only -q -p no:cacheprovider` — reine Kollektion, **keine Testausführung** (§11 eingehalten; kein Testlauf war für die Feststellung erforderlich).

### RB-1.0 — dateigenaue Zählung (14 Dateien)

| Testdatei | Tests | Zuordnungsbegründung |
|---|---|---|
| `tests/test_activation_validation.py` | 42 | Kein `jochen_x`-Import; prüft Baseline-Plugin-Pipeline |
| `tests/test_application_foundation.py` | 62 | Kein `jochen_x`-Import (nur Logger-String); prüft `app/` |
| `tests/test_capability_matrix.py` | 2 | Kein `jochen_x`-Import |
| `tests/test_core.py` | 6 | Kein `jochen_x`-Import; prüft `core/` |
| `tests/test_dependency_resolution.py` | 12 | Kein `jochen_x`-Import |
| `tests/test_developer.py` | 3 | Kein `jochen_x`-Import; prüft `developer/` |
| `tests/test_foundation.py` | 7 | Kein `jochen_x`-Import |
| `tests/test_golden_reference.py` | 3 | Kein `jochen_x`-Import |
| `tests/test_manifest_v2.py` | 8 | Kein `jochen_x`-Import |
| `tests/test_navigation.py` | 22 | Kein `jochen_x`-Import; prüft `ui/navigation` |
| `tests/test_plugin_observability.py` | 4 | Kein `jochen_x`-Import |
| `tests/test_sdk.py` | 51 | Kein `jochen_x`-Import; prüft `sdk/` |
| `tests/test_security_foundation.py` | 33 | Kein `jochen_x`-Import; prüft `app/security/` |
| `tests/integration/test_plugin_integration.py` | 3 | Kein `jochen_x`-Import |
| **Summe** | **258** | |

## 8. RB-1.0 Determination

| Erwartung (Sprint Plan) | Befund SPR-01 | Ergebnis |
|---|---|---|
| 14 Testdateien | 14 | ✓ |
| 258 Tests | 258 (dateigenau nachgezählt, Kap. 7) | ✓ |

Die Erwartung wurde **nicht übernommen, sondern unabhängig reproduziert** (eigene Kollektion, eigene Import-Analyse, dateigenaue Zählung).

## 9. `src/jochen_x/**` Exclusion

| Menge | Befund | Ergebnis |
|---|---|---|
| Stillgelegter Testbestand (22 Dateien mit `jochen_x`-Imports: `tests/unit/**` [18], `tests/recovery/test_recovery_scenarios.py`, `tests/security/test_security_policies.py`, `tests/integration/test_{concurrency,event_bus,runtime}_integration.py`) | **761 Tests / 22 Dateien** | ✓ verifiziert |
| Repository-Gesamtkennzahl | **1019 Tests** | ✓ (258 + 761 = 1019, deckungsgleich IP §3.1) |
| `src/**` eigene `test_*.py` | 0 — der „eigene Testbestand" des Parallelbaums liegt vollständig in den 22 Dateien | ✓ |

**1019 ist NICHT die RB-1.0-Bezugsgröße.** Kein Test des stillgelegten Bestands fließt in RB-1.0 ein. `src/jochen_x/**` wurde nicht entfernt, verschoben, archiviert oder reaktiviert.

## 10. Regression Baseline

> **RB-1.0 (formal festgestellt): 258 Tests in den 14 in Kap. 7 gelisteten
> Testdateien der baseline-geführten Struktur.**

Grundlage: GDR-002 D-3; IP §9.6 (Regressionsregeln unverändert), §11.10 (Completion: „dokumentierte Entscheidung und anschließende Festlegung der Regressionsbezugsgröße" — hiermit erfolgt). Spätere in MWB-015 hinzukommende Tests erweitern den Nachweisumfang, nicht RB-1.0.

## 11. Reproducibility

| Element | Wert |
|---|---|
| Methode | Import-Analyse (`^(from|import)\s+(src\.)?jochen_x`) + `pytest --collect-only -q -p no:cacheprovider` (read-only; `PYTHONDONTWRITEBYTECODE=1`) |
| Ausschlussregel | 22 Dateien mit `jochen_x`-Import (Kap. 9); String-Vorkommen zählen nicht |
| Zeitpunkt | 2026-08-09 |
| Branch | `milestone-1.0-governance` |
| HEAD-Commit | `63407ad9d8538c5ea5ae5b06b2f7f461332eea14` |
| Baseline-Identifier | **OPEN BASELINE IDENTIFIER** — der bestätigte Zustand ist der Working Tree vom 2026-08-09, der über HEAD hinaus 12 vorbestehende uncommittete Änderungen und vorbestehende untracked Bestandsdateien enthält (Finding F-SPR01-01). Es existiert kein einzelner Commit, der den bestätigten Zustand vollständig abbildet; es wird keiner erfunden. |

## 12. Findings

| ID | Severity | Kategorie | Befund | Auswirkung | Status |
|---|---|---|---|---|---|
| F-SPR01-01 | MEDIUM | BASELINE FINDING | Der Baseline-Zustand liegt teilweise uncommitted vor: 12 vorbestehende getrackte Modifikationen (u. a. `app/application_host.py`, `app/bootstrap/__init__.py`, `app/events.py`, `app/security/security_manager.py`, `docs/architecture-book-v2.md`, ADR-005/006/007, sowie die RB-1.0-Dateien `tests/test_application_foundation.py`, `tests/integration/test_plugin_integration.py`) und vorbestehende untracked Dateien, die der IP als bestehend führt (`app/bootstrap/constants.py`, `manager.py`, `stages_*.py`, `types.py`, `sdk/_test_hooks.py`). RB-1.0 wurde gegen diesen Working-Tree-Stand festgestellt. | Kein eindeutiger Commit-Identifier (→ OPEN BASELINE IDENTIFIER); für spätere Nachweise (EV-D01-Nachnutzung, EV-G04/GV-03/GV-05) ist die Herstellung eines committeten, eindeutig identifizierbaren Baseline-Stands relevant. Die Änderungen sind **fremd/vorbestehend** und wurden durch SPR-01 nicht berührt, nicht bewertet und nicht bereinigt. | OPEN — Entscheidung über Commit/Identifier obliegt dem Projekteigner |
| F-SPR01-02 | EDITORIAL | Source Gate | Auftragspfad `docs/milestone-1.0-sprint-planning-summary-r0.md` weicht von der tatsächlichen Fundstelle `docs/audits/…` ab | Keine — Quelle eindeutig | NOT A BLOCKER |

Keine CRITICAL/HIGH Findings. Keine Abweichung wurde stillschweigend korrigiert.

## 13. Verification

| Prüfung | Ergebnis |
|---|---|
| Baseline-Pfade / Einstiegspunkt erneut geprüft | PASS |
| 14 Testdateien / 258 Tests dateigenau reproduziert | PASS |
| Ausschluss `src/jochen_x/**` (761/22; 258+761=1019) | PASS |
| Keine Produktions-, Test-, Security-, Governance- oder Baseline-Datei verändert | PASS |
| Fremde Working-Tree-Änderungen unberührt | PASS |
| Keine Testausführung (nur Kollektion) | PASS |
| Kein Commit / Tag / Push | PASS |

## 14. Final Decision

> **BASELINE CONFIRMED** — die baseline-geführte Struktur ist eindeutig
> identifiziert und sauber von `src/jochen_x/**` getrennt (mit Finding
> F-SPR01-01 zur Identifier-Frage, nicht identitätsblockierend).
>
> **RB-1.0 CONFIRMED** — 258 Tests / 14 Testdateien, eindeutig und
> reproduzierbar festgestellt.

**SPR-01 ist erfolgreich abgeschlossen.** Quality Gates QG-001–QG-008 bleiben NOT STARTED (dieses Dokument liefert Nachweisgrundlagen für spätere Gates, nimmt aber kein Gate vorweg). **CODING = NOT AUTHORIZED** — SPR-01 erzeugt keine RL-05-Erfüllung und keine Coding-Freigabe.

## 15. Next Authorized Action

Nächster Sprint gemäß genehmigtem Sprint Plan (Phase B: SPR-02–SPR-07, parallelisierbar) — **erst nach ausdrücklicher Freigabe des Projekteigners** und erst nach Erfüllung der Coding Conditions des Implementation Plans (10.6 Nr. 7–9, RL-05), soweit Umsetzungsarbeit betroffen ist. Empfohlen zur Behandlung von F-SPR01-01: Projekteigner-Entscheidung über die Herstellung eines committeten Baseline-Identifiers vor Umsetzungsbeginn.

---

**Ende SPR-01 Baseline Confirmation — JOCHEN X Milestone 1.0 (FINAL, 2026-08-09)**
