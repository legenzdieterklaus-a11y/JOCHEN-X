# JOCHEN X — Development Standard v1.0

> **Status:** APPROVED  
> **Version:** 1.0  
> **Datum:** 2026-07-27  
> **Geltungsbereich:** Alle Milestones ab v0.8  
> **Referenz:** [Architecture Book v2.0](architecture-book-v2.md) (FROZEN)

---

## 1. Purpose

Dieses Dokument definiert den verbindlichen Engineering-Workflow für JOCHEN X. Es formalisiert die etablierten Prozesse für Spezifikation, Review, Implementierung, Test und Release.

Was dieses Dokument **ist:**
- Der offizielle Entwicklungsprozess
- Wiederverwendbar für alle zukünftigen Milestones

Was dieses Dokument **nicht ist:**
- Keine Architekturdokumentation (→ Architecture Book v2.0)
- Keine Coding-Guideline (→ CLAUDE.md)
- Keine API-Referenz (→ SDK-Dokumentation)

---

## 2. Engineering Principles

### Architecture Freeze

Die in Architecture Book v2.0 §22 eingefrorenen APIs und Contracts sind unveränderlich. Erlaubte Änderungen (Bugfixes, neue optionale Felder, neue Stages) erfordern keine ADR. ADR-pflichtige Änderungen (Entfernung eingefrorener Symbole, Lifecycle-Änderungen, Major-Version-Bumps) sind nur über eine neue Dokumentversion (v2.1+) zulässig.

### Evidence First

Jede Entscheidung basiert auf nachprüfbaren Fakten: vorhandener Code, existierende Tests, bestehende ADRs. Spezifikationen enthalten Gap-Analysen mit konkreten Dateireferenzen (Datei, Zeile, Status). Keine Annahmen ohne Verifikation.

### ADR Driven

Architekturentscheidungen werden als ADR in `docs/adr/` dokumentiert, bevor sie implementiert werden. ADRs benennen das Problem, Alternativen, die gewählte Lösung und deren Konsequenzen.

### No Scope Creep

Jeder Milestone hat einen definierten Scope. Implementierungen außerhalb dieses Scopes sind verboten — auch "offensichtliche Verbesserungen". Folgearbeiten werden als Future Items dokumentiert.

### Incremental Development

Arbeit erfolgt in kleinen, verifizierbaren Schritten. Jeder Schritt hat definierte Eingaben, Ausgaben und Akzeptanzkriterien. Kein Schritt setzt unverifizierte Ergebnisse eines anderen voraus.

### Review Before Approval

Kein Artefakt gelangt ohne unabhängige Prüfung in den Baseline-Branch. Reviews sind strukturiert (Critical/Major/Minor), Korrekturen werden verifiziert.

---

## 3. Project Baseline

### Architecture Book

[Architecture Book v2.0](architecture-book-v2.md) ist die verbindliche Architekturreferenz. Es definiert Schichtmodell, Komponenten, Contracts und Freeze-Scope.

### Baseline Commit

Jeder Milestone dokumentiert seinen Ausgangs-Commit und die zugehörigen Versionsnummern (Application, SDK, SDK-API).

### Git Tags

| Tag-Typ | Format | Beispiel |
|---------|--------|----------|
| Architecture Freeze | `core-runtime-v{major}.{minor}.{patch}` | `core-runtime-v1.0.0` |
| Architecture Book | `architecture-book-v{version}` | `architecture-book-v2.0` |
| Release | `v{major}.{minor}.{patch}` | `v0.8.0` |

### Approved ADRs

Alle akzeptierten ADRs in `docs/adr/` sind Teil der Baseline. Offene ADRs (Status: Open) dokumentieren bekannte Entscheidungslücken und sind nicht implementierungsfähig.

### Milestone Contract

Jeder Milestone wird durch eine Engineering Specification gebunden (→ §4).

---

## 4. Development Lifecycle

```
Architecture Book (frozen)
        │
        ▼
   ADR (falls nötig)
        │
        ▼
   Specification
        │
        ▼
   Independent Review
        │
        ▼
   Corrections
        │
        ▼
   Final Verification
        │
        ▼
   Implementation
        │
        ▼
   Code Review
        │
        ▼
   Test Verification
        │
        ▼
   Release Candidate
        │
        ▼
   Release
```

**Reihenfolge ist verbindlich.** Keine Phase darf übersprungen werden. Die Implementierung beginnt erst nach Final Verification der Specification.

---

## 5. Milestone Rules

Jeder Milestone erfordert eine **Engineering Specification** mit folgenden Abschnitten:

### Pflichtinhalte

| Abschnitt | Inhalt |
|-----------|--------|
| **Baseline** | Commit-Hash, Tags, Versionsnummern |
| **Scope Verification** | Completed / Partial / Missing — mit Dateireferenzen |
| **Gap Analysis** | Was fehlt, Abhängigkeitskette |
| **Module Work Breakdown** | Pro Datei: konkrete Änderungen mit Codebeispielen |
| **Dependency Graph** | Abhängigkeiten zwischen den Änderungen |
| **Implementation Sequence** | Geordnete Schritte mit Abhängigkeiten |
| **Acceptance Criteria** | Nummerierte, prüfbare Kriterien (AC-N) |
| **Test Strategy** | Unit Tests, Integration Tests, Testprinzipien |
| **Quality Gates** | Nummerierte Gates (QG-N) mit Prüfmethode |
| **Risks** | Wahrscheinlichkeit, Auswirkung, Mitigation |
| **Deliverables** | Nummerierte Liste aller Lieferobjekte |
| **Definition of Done** | Vollständige Checkliste |
| **Future Items** | Explizit ausgeschlossene Folgearbeiten |

### Scope-Regel

Die Specification definiert den Scope. Alles, was nicht in der Specification steht, ist nicht Teil des Milestones. Ausnahmen erfordern eine Scope-Erweiterung mit erneuter Review.

---

## 6. Sprint Rules

Jeder Sprint innerhalb eines Milestones definiert:

| Element | Beschreibung |
|---------|-------------|
| **Sprint Goal** | Ein Satz: was dieser Sprint liefert |
| **Affected Files** | Vollständige Liste aller zu ändernden Dateien |
| **Acceptance Criteria** | Verweis auf die relevanten AC-N aus der Specification |
| **Tests** | Welche Tests geschrieben/ausgeführt werden |
| **Deliverables** | Welche Deliverables aus der Specification abgedeckt werden |
| **Sprint Report** | Nach Abschluss: was wurde geliefert, was weicht ab |
| **Approval Gate** | Tests grün, Code Review bestanden, keine Scope-Verletzung |

### Sprint-Größe

- Maximal 5 betroffene Dateien pro Sprint
- Bei > 5 Dateien: Freigabe einholen oder Sprint aufteilen
- Ein Sprint = ein thematisch sauberer Commit

---

## 7. Review Rules

### Strukturierte Reviews

Reviews klassifizieren Befunde nach Schweregrad:

| Schweregrad | Bedeutung | Aktion |
|-------------|-----------|--------|
| **Critical** | Architekturverletzung, Security-Problem, fehlende Komponente | Muss korrigiert werden |
| **Major** | Inkonsistenz, fehlende Akzeptanzkriterien, unvollständige Spezifikation | Muss korrigiert werden |
| **Minor** | Klarstellungen, Formulierungen, optionale Verbesserungen | Kann korrigiert werden |

### Review-Ablauf

1. **Independent Review** — Prüfung gegen Architecture Book, ADRs und Baseline
2. **Corrections** — Adressierung aller Critical und Major Findings
3. **Change Report** — Dokumentation aller durchgeführten Korrekturen
4. **Final Verification** — Bestätigung, dass alle Findings adressiert sind

### Review-Kriterien für Specifications

- [ ] Scope ist vollständig und abgegrenzt
- [ ] Keine Architekturverletzungen
- [ ] Acceptance Criteria sind prüfbar
- [ ] Dependency Graph ist korrekt
- [ ] Implementation Sequence respektiert Abhängigkeiten
- [ ] Test Strategy deckt alle Acceptance Criteria ab
- [ ] Quality Gates sind messbar
- [ ] Definition of Done ist vollständig
- [ ] Future Items dokumentieren bewusste Ausschlüsse

### Review-Kriterien für Code

- [ ] Nur genehmigter Scope implementiert
- [ ] Schichtmodell eingehalten (Abhängigkeiten nach innen)
- [ ] Architecture Freeze respektiert
- [ ] Type Hints auf allen öffentlichen APIs
- [ ] `__all__` aktualisiert
- [ ] Keine unbegründeten TODOs
- [ ] Tests vorhanden und grün

---

## 8. Implementation Rules

1. **Nur genehmigter Scope** — Implementiere ausschließlich, was in der Specification steht
2. **Keine Architekturänderungen** — Architecture Book v2.0 und eingefrorene APIs bleiben unverändert
3. **Kein verdecktes Refactoring** — Keine "Aufräumarbeiten" außerhalb des Scopes
4. **Keine unrelated Änderungen** — Jede Änderung muss zur Specification zurückverfolgbar sein
5. **Production-ready Code** — Kein Placeholder-Code, keine temporären Lösungen, keine TODOs ohne Begründung
6. **Implementation Sequence einhalten** — Schritte in der spezifizierten Reihenfolge abarbeiten
7. **Schichtmodell einhalten** — Core importiert nicht aus App/SDK/UI/Services

---

## 9. Testing Rules

### Teststufen

| Stufe | Verzeichnis | Zweck |
|-------|------------|-------|
| **Unit Tests** | `tests/`, `tests/unit/` | Einzelne Komponenten isoliert prüfen |
| **Integration Tests** | `tests/integration/` | Zusammenspiel mehrerer Komponenten |
| **Security Tests** | `tests/security/` | Default Deny, Adversarial Input, Permission Bypass |
| **Recovery Tests** | `tests/recovery/` | Escalation, Retry, Determinismus |

### Testprinzipien

- Kein Qt-Event-Loop erforderlich (außer UI-Tests)
- Deterministisch: kein `time.sleep()`, keine externen Abhängigkeiten
- Isolation: jeder Test erstellt eigene Instanzen
- Thread Safety wird explizit getestet
- `QT_QPA_PLATFORM=offscreen` für UI-Tests

### Test-Anforderungen pro Milestone

- Jedes Acceptance Criterion (AC-N) hat mindestens einen Test
- Fehlerszenarien explizit testen (Import-Fehler, Timeout, inkompatible Version)
- Bestehende Tests dürfen nicht brechen

### Testausführung

```bash
python -m pytest tests/test_core.py      # Einzelner Testfile
python -m pytest -q                      # Kompletter Lauf
```

- Nur relevante Tests während der Entwicklung
- Kompletter Lauf vor jedem Commit bei mehreren betroffenen Kernmodulen
- Alle Tests grün = Voraussetzung für Release

---

## 10. Release Rules

### Release-Ablauf

1. **Release Candidate** — Alle Deliverables implementiert, alle Tests grün
2. **Code Review** — Vollständige Review aller Änderungen (→ §7)
3. **Final Test Run** — `python -m pytest -q` — kompletter Lauf, keine Fehler
4. **Quality Gate Verification** — Alle QG-N aus der Specification bestanden
5. **Definition of Done** — Alle Punkte der DoD-Checkliste erfüllt
6. **Release Commit** — Ein sauberer Commit mit Prefix `feat(<scope>):` oder `fix(<scope>):`
7. **Git Tag** — `v{major}.{minor}.{patch}` auf den Release-Commit
8. **Documentation Update** — Architecture Book nur bei neuer Version, sonst ADRs und Specs aktualisieren

### Versionierung

| Artefakt | Ort | Regel |
|----------|-----|-------|
| Applikation | `pyproject.toml` → `project.version` | Semantic Versioning |
| SDK | `sdk/version.py` → `SDK_VERSION` | Semantic Versioning |
| SDK API | `sdk/version.py` → `SDK_API_VERSION` | Unabhängig, nur bei API-Surface-Änderung |

- **Major** = Breaking Changes an öffentlichen APIs
- **Minor** = Additive Erweiterungen
- **Patch** = Bugfixes ohne API-Änderung

---

## 11. ADR Rules

### Wann eine ADR erforderlich ist

- Entfernung eines eingefrorenen Symbols
- Änderung der State Machine Transition Table
- Neues Plugin-Lifecycle-State
- Änderung der Bootstrap-Phasenreihenfolge
- Neue Required Fields in PluginMetadata
- Major-Version-Bump der SDK-API
- Entfernung oder Umbenennung eines Protocols
- Jede Entscheidung, die den Architecture Freeze betrifft

### ADR-Format

Datei: `docs/adr/{NNN}-{kebab-case-title}.md`

Pflichtinhalte:
- **Status:** Open | Accepted | Resolved by ADR-XXX
- **Problem:** Was muss entschieden werden
- **Alternativen:** Mindestens zwei Optionen mit Vor-/Nachteilen
- **Lösung:** Gewählte Alternative mit Begründung
- **Konsequenzen:** Auswirkungen auf bestehenden Code und zukünftige Arbeit

### Architecture Freeze und ADRs

- ADRs ändern nicht das Architecture Book v2.0
- ADRs dokumentieren Erweiterungen oder Ausnahmen
- Wenn eine ADR den Freeze-Scope betrifft, wird eine neue Architecture Book Version (v2.1+) erforderlich

---

## 12. Definition of Done

Eine Aufgabe gilt als abgeschlossen, wenn:

- [ ] Specification wurde reviewed und freigegeben
- [ ] Nur genehmigter Scope implementiert
- [ ] Architecture Book v2.0 unverändert (oder neue Version erstellt)
- [ ] Schichtmodell eingehalten
- [ ] Alle Acceptance Criteria erfüllt
- [ ] Alle Quality Gates bestanden
- [ ] Alle bestehenden Tests weiterhin grün
- [ ] Alle neuen Tests grün
- [ ] Type Hints auf allen öffentlichen APIs
- [ ] `__all__` in jedem betroffenen Modul aktualisiert
- [ ] Keine unbegründeten TODOs
- [ ] Commit thematisch sauber (ein Thema pro Commit)
- [ ] Keine Secrets oder unnötigen Dateien im Commit
- [ ] Dokumentation aktualisiert (ADRs, Specs)
- [ ] Git Tag gesetzt (bei Release)

---

## 13. Engineering Checklists

### Milestone Checklist

```
□ ADR geschrieben (falls Architekturentscheidung nötig)
□ Engineering Specification erstellt
□ Baseline dokumentiert (Commit, Tags, Versionen)
□ Scope Verification durchgeführt
□ Gap Analysis abgeschlossen
□ Independent Review durchgeführt
□ Corrections umgesetzt
□ Final Verification bestanden
□ Implementation nach Sequence abgearbeitet
□ Code Review bestanden
□ Alle Tests grün
□ Quality Gates bestanden
□ Definition of Done erfüllt
□ Release Tag gesetzt
□ Future Items dokumentiert
```

### Sprint Checklist

```
□ Sprint Goal definiert
□ Betroffene Dateien aufgelistet (max. 5)
□ Acceptance Criteria zugewiesen
□ Implementation Sequence eingehalten
□ Tests geschrieben und grün
□ Code Review bestanden
□ Sprint Report erstellt
□ Commit thematisch sauber
```

### Review Checklist — Specification

```
□ Baseline vollständig (Commit, Tags, Versionen)
□ Scope Verification mit Dateireferenzen
□ Gap Analysis korrekt
□ Module Work Breakdown mit konkreten Änderungen
□ Dependency Graph konsistent
□ Implementation Sequence respektiert Abhängigkeiten
□ Acceptance Criteria nummeriert und prüfbar
□ Test Strategy deckt alle AC ab
□ Quality Gates messbar
□ Risks mit Mitigations
□ Definition of Done vollständig
□ Keine Architekturverletzungen
□ Architecture Freeze respektiert
□ Future Items explizit ausgeschlossen
```

### Review Checklist — Code

```
□ Nur genehmigter Scope
□ Schichtmodell eingehalten
□ Architecture Freeze respektiert
□ Type Hints vollständig
□ __all__ aktualisiert
□ Keine unbegründeten TODOs
□ Keine Secrets im Code
□ Tests vorhanden und grün
□ Bestehende Tests nicht gebrochen
□ Commit-Message folgt Konvention
```

### Release Checklist

```
□ Alle Deliverables implementiert
□ Alle Acceptance Criteria erfüllt
□ Alle Quality Gates bestanden
□ python -m pytest -q — alle Tests grün
□ Code Review bestanden
□ Definition of Done erfüllt
□ Versionen korrekt (pyproject.toml, sdk/version.py)
□ Git Tag gesetzt
□ Specification als abgeschlossen markiert
□ Future Items dokumentiert
```

---

## 14. Appendix

### A. Workflow-Diagramm

```
                    ┌─────────────┐
                    │  ADR (opt.) │
                    └──────┬──────┘
                           ▼
                   ┌───────────────┐
                   │ Specification │
                   └──────┬────────┘
                          ▼
              ┌───────────────────────┐
              │  Independent Review   │
              └───────────┬───────────┘
                          ▼
                 ┌─────────────────┐
                 │   Corrections   │◄──┐
                 └────────┬────────┘   │
                          ▼            │
              ┌───────────────────────┐│
              │  Final Verification   ├┘ (bei neuen Findings)
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │   Implementation      │
              │   (Sprint 1..N)       │
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │     Code Review       │
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │   Test Verification   │
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │  Release Candidate    │
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │       Release         │
              │   (Tag + Version)     │
              └───────────────────────┘
```

### B. Approval States

| Artefakt | States |
|----------|--------|
| ADR | Open → Accepted \| Resolved by ADR-XXX |
| Specification | Draft → In Review → Corrections → Approved |
| Sprint | Planned → In Progress → Review → Done |
| Release | Candidate → Verified → Released |

### C. Git Conventions

**Commit-Präfixe:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

**Format:** `<prefix>(<scope>): <kurze Beschreibung>`

**Prüfung vor jedem Commit:**
- Gehört alles zum gleichen Thema?
- Kann der Commit einzeln verstanden werden?
- Sind keine Secrets oder unnötigen Dateien enthalten?

### D. Referenzdokumente

| Dokument | Pfad | Zweck |
|----------|------|-------|
| Architecture Book v2.0 | `docs/architecture-book-v2.md` | Verbindliche Architekturreferenz |
| ADRs | `docs/adr/*.md` | Architekturentscheidungen |
| Engineering Specifications | `docs/milestone-*.md` | Milestone-Spezifikationen |
| CLAUDE.md | `CLAUDE.md` | Coding-Standards und Arbeitsregeln |
