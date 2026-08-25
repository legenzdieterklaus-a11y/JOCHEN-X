# JOCHEN X — Development Standard v1.1

> **Status:** APPROVED  
> **Version:** 1.1  
> **Datum:** 2026-07-27  
> **Vorgänger:** Development Standard v1.0 (ARCHIVED)  
> **Geltungsbereich:** Alle Milestones ab v0.8  
> **Referenz:** [Architecture Book v2.0](architecture-book-v2.md) (FROZEN)

---

## 1. Purpose

Dieses Dokument definiert den verbindlichen Engineering-Workflow für JOCHEN X. Es formalisiert die etablierten Prozesse für Spezifikation, Review, Implementierung, Test und Release.

Was dieses Dokument **ist:**
- Der offizielle Entwicklungsprozess
- Wiederverwendbar für alle zukünftigen Milestones
- Die einzige autoritative Quelle für Prozess- und Governance-Regeln

Was dieses Dokument **nicht ist:**
- Keine Architekturdokumentation (→ Architecture Book v2.0)
- Keine Coding-Guideline (→ CLAUDE.md)
- Keine API-Referenz (→ SDK-Dokumentation)
- Keine Milestone-Spezifikation (→ Engineering Specifications)

### 1.1 Normative Terminologie

Dieses Dokument verwendet die folgenden normativen Schlüsselwörter:

| Schlüsselwort | Bedeutung | Äquivalent (RFC 2119) |
|---------------|-----------|----------------------|
| **MUSS** | Verbindliche Anforderung. Keine Ausnahmen. | SHALL / MUST |
| **DARF NICHT** | Verbindliches Verbot. Keine Ausnahmen. | SHALL NOT / MUST NOT |
| **SOLL** | Erwartete Anforderung. Abweichung nur mit dokumentierter Begründung. | SHOULD |
| **DARF** | Erlaubte, aber optionale Handlung. | MAY |

Nicht-normative Formulierungen (z.B. "wird", "enthält", "definiert") beschreiben Fakten oder bestehende Strukturen.

---

## 2. Governance Principles

### 2.1 Single Authoritative Source

Jede Kategorie normativer Information hat genau eine autoritative Quelle. Keine andere Quelle DARF diese Informationen normativ duplizieren.

| Domäne | Autoritative Quelle |
|--------|---------------------|
| **Architektur** | Architecture Book v2.0 (FROZEN) |
| **Architekturentscheidungen** | ADRs in `docs/adr/` |
| **Entwicklungsprozess** | Development Standard (dieses Dokument) |
| **Milestone-Scope** | Jeweilige Engineering Specification |
| **Coding-Standards** | CLAUDE.md |

### 2.2 Prompt Governance

Prompts sind **Orchestrierungsartefakte**. Sie steuern die Erstellung von Dokumenten, initiieren Reviews und starten Implementierungen.

**Prompts DÜRFEN:**
- Genehmigte Dokumente referenzieren
- Templates referenzieren
- Das gewünschte Artefakt definieren

**Prompts SOLLEN:**
- Self-Review-Kriterien enthalten

**Prompts DÜRFEN NICHT:**
- Architektur definieren oder ändern
- Implementierungs-Scope definieren
- Dokumentstruktur umdefinieren (→ Templates)
- Engineering-Regeln umdefinieren (→ Development Standard)
- Prozessabläufe umdefinieren (→ Development Standard)

### 2.3 No Normative Duplication

Kein Dokument DARF normativen Inhalt duplizieren, der einem anderen Dokument gehört. Verweise (z.B. "gemäß Architecture Book v2.0 §X") sind erlaubt. Paraphrasierung mit normativer Wirkung ist verboten.

**Begründung:** Während Milestone 0.8 wurde nachgewiesen, dass duplizierte Regeln in Prompts und Spezifikationen zu Inkonsistenzen und Scope-Überschreitungen führen.

---

## 3. Document Hierarchy

### 3.1 Übersicht

```
Architecture Book (FROZEN)          Architektur, Schichtmodell, Contracts, Freeze-Scope
        │
        ├── ADRs                    Architekturentscheidungen und -erweiterungen
        │
Development Standard               Prozess, Governance, Templates, Review-Workflow
        │
        ├── Templates               Dokumentstruktur (subordinat zum Development Standard)
        │
        ├── Engineering Spec        Milestone-Scope, Implementation Contract
        │
        ├── Review Reports          Independent Review, Milestone Review
        │
        ├── Correction Reports      Adressierung von Review-Findings
        │
        └── Final Verification      Bestätigung genehmigter Arbeit
```

### 3.2 Dokumentverantwortlichkeiten

| Dokument | Verantwortlichkeit | DARF NICHT |
|----------|-------------------|------------|
| **Architecture Book** | Schichtmodell, Komponenten, Contracts, Freeze-Scope | Prozesse definieren |
| **ADR** | Architekturentscheidungen mit Alternativen und Konsequenzen | Scope definieren, Prozesse ändern |
| **Development Standard** | Prozess, Governance, Templates, Review-Regeln | Architektur definieren |
| **Templates** | Dokumentstruktur für wiederkehrende Artefakte | Normativen Inhalt besitzen (subordinat) |
| **Engineering Specification** | Milestone-Scope, Gap Analysis, Implementation Contract | Architektur ändern, Prozesse umdefinieren |
| **Review Reports** | Strukturierte Befunde mit Schweregrad | Scope erweitern, Architektur ändern |
| **Correction Reports** | Dokumentation durchgeführter Korrekturen | Neue Findings einführen, Scope erweitern |
| **Final Verification Reports** | Bestätigung, dass alle Findings adressiert sind | Neue Findings einführen, Scope erweitern |
| **Prompts** | Orchestrierung: Artefakterstellung initiieren | Normativen Inhalt besitzen (→ §2.2) |

### 3.3 Konfliktregel

Bei Widersprüchen zwischen Dokumenten gilt die folgende Hierarchie (absteigend):

1. Architecture Book
2. ADR
3. Development Standard
4. Engineering Specification
5. Review Reports
6. Final Verification Reports
7. Correction Reports
8. Templates
9. Prompts

---

## 4. Engineering Principles

### Architecture Freeze

Die in Architecture Book v2.0 §22 eingefrorenen APIs und Contracts sind unveränderlich. Erlaubte Änderungen (Bugfixes, neue optionale Felder, neue Stages) erfordern keine ADR. ADR-pflichtige Änderungen (Entfernung eingefrorener Symbole, Lifecycle-Änderungen, Major-Version-Bumps) sind nur über eine neue Dokumentversion (v2.1+) zulässig.

### Evidence First

Jede Entscheidung basiert auf nachprüfbaren Fakten: vorhandener Code, existierende Tests, bestehende ADRs. Spezifikationen enthalten Gap-Analysen mit konkreten Dateireferenzen (Datei, Zeile, Status). Keine Annahmen ohne Verifikation.

**Evidence-Klassifikation:**

Jede Engineering Specification MUSS technische Aussagen klassifizieren als:

| Klassifikation | Bedeutung | Anforderung |
|---------------|-----------|-------------|
| **Verified Evidence** | Durch Code, Tests oder Dateireferenzen belegt | Referenz angeben |
| **Inference** | Aus Evidence abgeleitet, nicht direkt geprüft | Ableitung dokumentieren |
| **Open Blocker** | Nicht verifizierbar, blockiert Fortschritt | Explizit als ungelöst markieren |

Keine technische Aussage in einer Engineering Specification DARF ohne Klassifikation stehen.

**Begründung Geltungsbereich:** Review Reports und Final Verification Reports verifizieren Aussagen der Engineering Specification — sie treffen keine eigenständigen technischen Aussagen. Die Evidence Summary (§6.2, Abschnitt 15) ist die korrekte Implementierungsebene für die Klassifikation. Die Anwendung auf prüfende Dokumente wäre eine Kategorienverwechslung.

### ADR Driven

Architekturentscheidungen werden als ADR in `docs/adr/` dokumentiert, bevor sie implementiert werden. ADRs benennen das Problem, Alternativen, die gewählte Lösung und deren Konsequenzen.

### No Scope Creep

Jeder Milestone hat einen definierten Scope. Implementierungen außerhalb dieses Scopes sind verboten — auch "offensichtliche Verbesserungen". Folgearbeiten werden als Future Items dokumentiert.

### Incremental Development

Arbeit erfolgt in kleinen, verifizierbaren Schritten. Jeder Schritt hat definierte Eingaben, Ausgaben und Akzeptanzkriterien. Kein Schritt setzt unverifizierte Ergebnisse eines anderen voraus.

### Review Before Approval

Kein Artefakt gelangt ohne unabhängige Prüfung in den Baseline-Branch. Reviews sind strukturiert (Critical/Major/Minor), Korrekturen werden verifiziert.

---

## 5. Project Baseline

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

Jeder Milestone wird durch eine Engineering Specification gebunden (→ §6).

---

## 6. Engineering Specification

### 6.1 Zweck

Die Engineering Specification ist der **Implementation Contract** für einen Milestone. Sie definiert Scope, Gap Analysis, Implementierungsreihenfolge und Akzeptanzkriterien. Sie wird vor der Implementierung reviewed und freigegeben.

### 6.2 Normative Struktur

Jede Engineering Specification MUSS die folgenden Abschnitte in dieser Reihenfolge enthalten:

| # | Abschnitt | Inhalt | Pflicht |
|---|-----------|--------|---------|
| 1 | **Baseline Verification** | Commit-Hash, Tags, Versionsnummern, Verweis auf Architecture Book | Ja |
| 2 | **Scope Verification** | Completed / Partial / Missing — mit Dateireferenzen (Datei, Zeile, Status) | Ja |
| 3 | **Gap Analysis** | Was fehlt, Abhängigkeitskette, Lückenbewertung | Ja |
| 4 | **Delta Analysis** | Exakte Differenz zwischen Baseline und Zielzustand pro Datei | Ja |
| 5 | **Module Work Breakdown** | Pro Datei: konkrete Änderungen mit Codebeispielen | Ja |
| 6 | **Dependency Graph** | Abhängigkeiten zwischen Änderungen, visualisiert | Ja |
| 7 | **Implementation Sequence** | Geordnete Schritte mit Abhängigkeiten | Ja |
| 8 | **Acceptance Criteria** | Nummerierte, prüfbare Kriterien (AC-N) | Ja |
| 9 | **Test Strategy** | Unit Tests, Integration Tests, Testprinzipien | Ja |
| 10 | **Quality Gates** | Nummerierte Gates (QG-N) mit Prüfmethode | Ja |
| 11 | **Risks** | Wahrscheinlichkeit, Auswirkung, Mitigation | Ja |
| 12 | **Deliverables** | Nummerierte Liste aller Lieferobjekte | Ja |
| 13 | **Definition of Done** | Vollständige Checkliste | Ja |
| 14 | **Future Items** | Explizit ausgeschlossene Folgearbeiten | Ja |
| 15 | **Evidence Summary** | Tabellarische Übersicht: Aussage → Klassifikation (Verified/Inference/Blocker) | Ja |

**Neu gegenüber v1.0:** Die Abschnitte *Delta Analysis* (4) und *Evidence Summary* (15) sind hinzugekommen. *Baseline* wurde zu *Baseline Verification* präzisiert.

**Begründung:** Die Delta Analysis wurde während Milestone 0.8 als notwendig erkannt, um den exakten Änderungsumfang pro Datei vorab zu bestimmen. Die Evidence Summary formalisiert das Evidence-First-Prinzip (§4) auf Dokumentebene.

### 6.3 Scope-Regel

Die Specification definiert den Scope. Alles, was nicht in der Specification steht, ist nicht Teil des Milestones. Ausnahmen erfordern eine Scope-Erweiterung mit erneuter Review.

---

## 7. Development Lifecycle

```
Architecture Book (frozen)
        │
        ▼
   ADR (falls nötig)
        │
        ▼
   Engineering Specification
        │
        ▼
   Independent Review
        │
        ▼
   Corrections
        │
        ▼
   Approval
        │
        ▼
   Implementation (Sprints)
        │
        ▼
   Sprint Reviews
        │
        ▼
   Milestone Review
        │
        ▼
   Correction Sprint
        │
        ▼
   Final Verification
        │
        ▼
   Release
```

**Reihenfolge ist verbindlich.** Keine Phase DARF übersprungen werden.

**Änderungen gegenüber v1.0:**
- *Approval* als explizite Phase nach Corrections eingefügt
- *Sprint Reviews* als Phase während der Implementierung eingefügt
- *Milestone Review* und *Correction Sprint* zwischen Implementierung und Final Verification eingefügt
- *Final Verification* verschoben: findet nach der Implementierung statt (nicht vor ihr)
- *Code Review* und *Test Verification* aus v1.0 sind in *Sprint Reviews* bzw. *Milestone Review* aufgegangen

**Begründung:** Der in v1.0 definierte Lifecycle platzierte Final Verification vor der Implementierung. Dies entspricht der Specification-Freigabe. Der vollständige Workflow, wie er in Milestone 0.8 praktiziert wurde, umfasst zusätzlich Sprint Reviews während der Implementierung und eine abschließende Final Verification nach der Implementierung.

---

## 8. Sprint Rules

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

## 9. Review Rules

### 9.1 Strukturierte Reviews

Reviews klassifizieren Befunde nach Schweregrad:

| Schweregrad | Bedeutung | Aktion |
|-------------|-----------|--------|
| **Critical** | Architekturverletzung, Security-Problem, fehlende Komponente | MUSS korrigiert werden |
| **Major** | Inkonsistenz, fehlende Akzeptanzkriterien, unvollständige Spezifikation | MUSS korrigiert werden |
| **Minor** | Klarstellungen, Formulierungen, optionale Verbesserungen | DARF korrigiert werden |

### 9.2 Review-Workflow

Der vollständige Review-Workflow umfasst:

```
Engineering Specification
        │
        ▼
Independent Review              Prüfung gegen Architecture Book, ADRs, Baseline
        │
        ▼
Correction Report               Adressierung aller Critical und Major Findings
        │
        ▼
Approval                        Formale Freigabe zur Implementierung
        │
        ▼
Implementation (Sprints)        Jeder Sprint mit Sprint Review
        │
        ▼
Sprint Reviews                  Prüfung pro Sprint gegen Specification
        │
        ▼
Milestone Review                Gesamtprüfung aller Deliverables (→ §9.6)
        │
        ▼
Correction Sprint               Adressierung offener Findings aus Milestone Review
        │
        ▼
Final Verification              Bestätigung genehmigter Arbeit (→ §9.3)
        │
        ▼
Release
```

### 9.3 Final Verification

Final Verification ist ein **Bestätigungsprozess**. Sie verifiziert, dass alle genehmigten Arbeiten korrekt implementiert und alle Findings aus vorherigen Reviews adressiert wurden.

**Final Verification IST:**
- Bestätigung genehmigter Arbeit
- Prüfung, dass alle Corrections umgesetzt wurden
- Verifizierung der Definition of Done

**Final Verification ist NICHT:**
- Ein erneutes Review
- Ein Architektur-Review
- Ein Feature-Review
- Eine Gelegenheit für neue Anforderungen

**Während Final Verification ist es VERBOTEN:**
- Neue Findings einzuführen
- Neue Anforderungen einzuführen
- Scope zu erweitern
- Architektur zu redesignen
- Implementierungsentscheidungen in Frage zu stellen, die bereits genehmigt sind

Nur die Verifikation genehmigter Arbeit ist zulässig.

**Begründung:** Während Milestone 0.8 wurde nachgewiesen, dass ein nicht formalisierter Final-Verification-Prozess zu Scope-Erweiterungen und unnötigen Korrekturrunden führen kann, wenn der Prüfer neue Findings einführt statt genehmigte Arbeit zu bestätigen.

### 9.4 Review-Kriterien für Specifications

- [ ] Scope ist vollständig und abgegrenzt
- [ ] Keine Architekturverletzungen
- [ ] Acceptance Criteria sind prüfbar
- [ ] Dependency Graph ist korrekt
- [ ] Implementation Sequence respektiert Abhängigkeiten
- [ ] Test Strategy deckt alle Acceptance Criteria ab
- [ ] Quality Gates sind messbar
- [ ] Definition of Done ist vollständig
- [ ] Future Items dokumentieren bewusste Ausschlüsse
- [ ] Evidence Summary vorhanden und konsistent mit Dokumentinhalt

### 9.5 Review-Kriterien für Code

- [ ] Nur genehmigter Scope implementiert
- [ ] Schichtmodell eingehalten (Abhängigkeiten nach innen)
- [ ] Architecture Freeze respektiert
- [ ] Type Hints auf allen öffentlichen APIs
- [ ] `__all__` aktualisiert
- [ ] Keine unbegründeten TODOs
- [ ] Tests vorhanden und grün

### 9.6 Milestone Review

Der Milestone Review ist die Gesamtprüfung aller Deliverables nach Abschluss der Implementierung.

**Zweck:** Verifizieren, dass der implementierte Milestone die Engineering Specification vollständig und korrekt erfüllt.

**Eingaben:**
- Genehmigte Engineering Specification
- Alle Sprint Reports
- Aktueller Codestand (Baseline + alle Sprint-Commits)

**Prüfkriterien:** Der Milestone Review wendet die folgenden bestehenden Checklisten an:

- Review-Kriterien für Code (§9.5) — auf den gesamten Milestone-Changeset
- Acceptance Criteria (AC-N) aus der Engineering Specification — vollständig geprüft
- Quality Gates (QG-N) aus der Engineering Specification — vollständig geprüft
- Definition of Done aus der Engineering Specification — vollständig geprüft

**Output:** Der Milestone Review verwendet die Independent Review Struktur (§14.3) mit dem Gesamt-Milestone als Prüfgegenstand. Findings werden nach Schweregrad klassifiziert (§9.1).

**Entscheidung:**
- **Keine Findings:** → Final Verification
- **Nur Minor Findings:** → Final Verification (Minor optional adressieren)
- **Major oder Critical Findings:** → Correction Sprint → erneuter Milestone Review der korrigierten Findings

---

## 10. Implementation Rules

1. **Nur genehmigter Scope** — Implementiere ausschließlich, was in der Specification steht
2. **Keine Architekturänderungen** — Architecture Book v2.0 und eingefrorene APIs bleiben unverändert
3. **Kein verdecktes Refactoring** — Keine "Aufräumarbeiten" außerhalb des Scopes
4. **Keine unrelated Änderungen** — Jede Änderung MUSS zur Specification zurückverfolgbar sein
5. **Production-ready Code** — Kein Placeholder-Code, keine temporären Lösungen, keine TODOs ohne Begründung
6. **Implementation Sequence einhalten** — Schritte in der spezifizierten Reihenfolge abarbeiten
7. **Schichtmodell einhalten** — Core importiert nicht aus App/SDK/UI/Services

---

## 11. Testing Rules

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
- Bestehende Tests DÜRFEN NICHT brechen

### Testausführung

```bash
python -m pytest tests/test_core.py      # Einzelner Testfile
python -m pytest -q                      # Kompletter Lauf
```

- Nur relevante Tests während der Entwicklung
- Kompletter Lauf vor jedem Commit bei mehreren betroffenen Kernmodulen
- Alle Tests grün = Voraussetzung für Release

---

## 12. Release Rules

### Release-Ablauf

1. **Release Candidate** — Alle Deliverables implementiert, alle Tests grün
2. **Code Review** — Vollständige Review aller Änderungen (→ §9.5)
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

## 13. ADR Rules

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
- **Problem:** Was MUSS entschieden werden
- **Alternativen:** Mindestens zwei Optionen mit Vor-/Nachteilen
- **Lösung:** Gewählte Alternative mit Begründung
- **Konsequenzen:** Auswirkungen auf bestehenden Code und zukünftige Arbeit

### Architecture Freeze und ADRs

- ADRs ändern nicht das Architecture Book v2.0
- ADRs dokumentieren Erweiterungen oder Ausnahmen
- Wenn eine ADR den Freeze-Scope betrifft, wird eine neue Architecture Book Version (v2.1+) erforderlich

---

## 14. Templates

### 14.1 Zweck

Templates definieren die verbindliche Dokumentstruktur für wiederkehrende Artefakte. Sie sind **subordinat** zum Development Standard — der Standard definiert die Regeln, Templates implementieren die Struktur.

### 14.2 Normative Templates

| Template | Zweck | Strukturdefinition |
|----------|-------|--------------------|
| **Engineering Specification** | Milestone-Implementation-Contract | §6.2 dieses Dokuments |
| **Independent Review** | Strukturierte Prüfung gegen Baseline | §14.3 |
| **Correction Report** | Dokumentation durchgeführter Korrekturen | §14.5 |
| **Final Verification** | Bestätigung genehmigter Arbeit | §14.4 |

### 14.3 Independent Review Template

Ein Independent Review MUSS folgende Abschnitte enthalten:

| Abschnitt | Inhalt |
|-----------|--------|
| **Scope Reference** | Verweis auf die geprüfte Engineering Specification |
| **Baseline Reference** | Commit, Tags, Versionen zum Prüfzeitpunkt |
| **Methodology** | Prüfverfahren und -kriterien |
| **Findings** | Nummerierte Befunde mit Schweregrad (Critical/Major/Minor) |
| **Evidence** | Dateireferenzen und Begründungen für jeden Befund |
| **Summary** | Gesamtbewertung, Anzahl Befunde pro Schweregrad |
| **Recommendation** | Approve / Approve with Corrections / Reject |

### 14.4 Final Verification Template

Eine Final Verification MUSS folgende Abschnitte enthalten:

| Abschnitt | Inhalt |
|-----------|--------|
| **Scope Reference** | Verweis auf die geprüfte Engineering Specification |
| **Correction Reference** | Verweis auf den Correction Report |
| **Verification Checklist** | Pro Finding: Status (Addressed / Not Addressed) mit Evidence |
| **Definition of Done** | DoD-Checkliste mit Einzelstatus |
| **Quality Gates** | Alle QG-N mit Prüfergebnis |
| **Result** | Verified / Not Verified |

**Einschränkung:** Final Verification enthält keine neuen Findings, keine neuen Anforderungen, keine Scope-Erweiterungen (→ §9.3).

### 14.5 Correction Report Template

Ein Correction Report MUSS folgende Abschnitte enthalten:

| Abschnitt | Inhalt |
|-----------|--------|
| **Scope Reference** | Verweis auf das korrigierte Artefakt (Specification, Milestone, etc.) |
| **Findings Reference** | Verweis auf das Review, dessen Findings adressiert werden |
| **Corrections** | Pro Finding: Finding-ID, durchgeführte Modifikation, betroffene Abschnitte, Begründung |
| **Deferred Findings** | Findings, die nicht in diesem Correction Sprint adressiert werden, mit Begründung |
| **Evidence** | Nachweise für jede durchgeführte Korrektur (Dateireferenzen, Vorher/Nachher) |
| **Summary** | Gesamtstatus: Anzahl adressierter / zurückgestellter Findings |

**Zweck:** Der Correction Report dokumentiert die Adressierung aller Findings aus einem vorherigen Review. Er dient als Eingabe für die Final Verification (§14.4, Correction Reference).

---

## 15. Definition of Done

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

## 16. Engineering Checklists

### Milestone Checklist

```
□ ADR geschrieben (falls Architekturentscheidung nötig)
□ Engineering Specification erstellt (gemäß §6.2)
□ Baseline dokumentiert (Commit, Tags, Versionen)
□ Scope Verification durchgeführt
□ Gap Analysis abgeschlossen
□ Delta Analysis abgeschlossen
□ Evidence Summary erstellt
□ Independent Review durchgeführt (gemäß §14.3)
□ Correction Report erstellt (gemäß §14.5)
□ Approval erteilt
□ Implementation nach Sequence abgearbeitet
□ Sprint Reviews durchgeführt
□ Milestone Review durchgeführt (gemäß §9.6)
□ Correction Sprint abgeschlossen (falls nötig)
□ Final Verification bestanden (gemäß §14.4)
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
□ Baseline Verification vollständig (Commit, Tags, Versionen)
□ Scope Verification mit Dateireferenzen
□ Gap Analysis korrekt
□ Delta Analysis vorhanden
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
□ Evidence Summary vorhanden und konsistent
□ Keine normativen Duplikate (→ §2.3)
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
□ Final Verification bestanden (gemäß §14.4)
```

### Prompt Checklist

```
□ Referenziert genehmigte Dokumente (Architecture Book, ADRs, Development Standard)
□ Referenziert anwendbare Templates (§14)
□ Definiert das gewünschte Artefakt
□ Enthält Self-Review-Kriterien (SOLL, → §2.2)
□ Definiert KEINE Architektur
□ Definiert KEINEN Implementierungs-Scope
□ Definiert KEINE Dokumentstruktur um
□ Definiert KEINE Engineering-Regeln um
```

---

## 17. Appendix

### A. Workflow-Diagramm

```
                    ┌─────────────┐
                    │  ADR (opt.) │
                    └──────┬──────┘
                           ▼
                   ┌───────────────┐
                   │ Engineering   │
                   │ Specification │
                   └──────┬────────┘
                          ▼
              ┌───────────────────────┐
              │  Independent Review   │
              └───────────┬───────────┘
                          ▼
                 ┌─────────────────┐
                 │  Corrections    │◄──┐
                 └────────┬────────┘   │
                          ▼            │
              ┌───────────────────────┐│
              │     Approval          ├┘ (bei neuen Findings)
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │   Implementation      │
              │   (Sprint 1..N)       │
              │   + Sprint Reviews    │
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │   Milestone Review    │
              │   (→ §9.6)           │
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │   Correction Sprint   │
              │   (falls nötig)       │
              └───────────┬───────────┘
                          ▼
              ┌───────────────────────┐
              │  Final Verification   │
              │  (Bestätigung only)   │
              │   (→ §9.3)           │
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
| Development Standard | `docs/development-standard-v1.1.md` | Verbindlicher Entwicklungsprozess |
| Engineering Specifications | `docs/milestone-*.md` | Milestone-Spezifikationen |
| CLAUDE.md | `CLAUDE.md` | Coding-Standards und Arbeitsregeln |

### E. Document Hierarchy Diagram

```
┌─────────────────────────────────────────────────────────┐
│                  Architecture Book v2.0                  │
│              (Architektur — FROZEN)                       │
└─────────────────────┬───────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
┌─────────────────┐    ┌──────────────────────────────────┐
│      ADRs       │    │      Development Standard v1.1   │
│  (Entscheidung) │    │      (Prozess — dieses Dok.)     │
└─────────────────┘    └──────────┬───────────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ▼             ▼             ▼
             ┌──────────┐ ┌────────────┐ ┌──────────────┐
             │ Templates│ │ Engineering│ │   Review /   │
             │(Struktur)│ │   Specs    │ │  Correction  │
             └──────────┘ │  (Scope)   │ │   Reports    │
                          └────────────┘ └──────────────┘
```

---

## 18. Version History

### Changelog v1.0 → v1.1

| Abschnitt | Änderung | Typ | Begründung |
|-----------|----------|-----|------------|
| §1 Purpose | Klarstellung als einzige autoritative Prozessquelle | Modifiziert | Governance-Principle: Single Authoritative Source |
| §1.1 Normative Terminologie | Definition MUSS/SOLL/DARF/DARF NICHT | Neu | Correction m-2: normative Sprache war undefiniert |
| §2 Governance Principles | Neuer Abschnitt: Single Source, Prompt Governance, No Duplication | Neu | Formalisierung der während M0.8 validierten Governance-Regeln |
| §2.2 Prompt Governance | Self-Review-Kriterien: DÜRFEN → SOLLEN | Modifiziert | Correction m-4: Konsistenz mit Prompt Checklist §16 |
| §3 Document Hierarchy | Neuer Abschnitt: Hierarchie, Verantwortlichkeiten, Konfliktregel | Neu | Klärung der Dokumentbeziehungen nach M0.8-Erfahrungen |
| §3.3 Konfliktregel | Vollständige Hierarchie mit allen 9 Dokumenttypen | Modifiziert | Correction M-4: fehlende Dokumenttypen ergänzt |
| §4 Engineering Principles | Evidence-Klassifikation (Verified/Inference/Blocker) hinzugefügt | Modifiziert | M0.8: unklassifizierte Aussagen führten zu falschen Review-Findings |
| §4 Evidence First | Geltungsbereich auf Engineering Specifications eingeschränkt | Modifiziert | Correction M-3: Ambiguität "Jedes Milestone-Dokument" aufgelöst |
| §6 Engineering Specification | Delta Analysis und Evidence Summary als Pflichtabschnitte; Baseline Verification präzisiert | Modifiziert | M0.8: Delta Analysis war notwendig zur Scope-Begrenzung; Evidence Summary formalisiert Evidence First |
| §7 Development Lifecycle | Vollständiger Workflow: Approval, Sprint Reviews, Milestone Review, Correction Sprint | Modifiziert | M0.8: der praktizierte Workflow war umfangreicher als in v1.0 dokumentiert |
| §9 Review Rules | Final Verification formalisiert mit expliziten Verboten; Evidence Summary in Review-Kriterien | Modifiziert | M0.8: unklar definierte Final Verification führte zu Scope-Erweiterungen |
| §9.2 Review-Workflow | Terminologie: Change Report (v1.0) → Correction Report (v1.1) | Modifiziert | Correction m-3: Umbenennung war nicht dokumentiert |
| §9.6 Milestone Review | Definition: Zweck, Eingaben, Prüfkriterien, Output, Entscheidung | Neu | Correction M-2: Milestone Review war als Pflichtphase ohne Definition |
| §14 Templates | Neuer Abschnitt: Engineering Spec, Independent Review, Correction Report, Final Verification Templates | Neu | Formalisierung der in M0.8 benutzten Dokumentstrukturen |
| §14.5 Correction Report | Template mit Pflichtabschnitten | Neu | Correction M-1: Correction Report Template fehlte |
| §16 Checklists | Governance-Prüfpunkte in Milestone/Review/Release Checklists; neue Prompt Checklist | Modifiziert | Integration der neuen Governance-Regeln in operative Checklisten |
| §17 Appendix | Workflow-Diagramm aktualisiert; Document Hierarchy Diagram hinzugefügt | Modifiziert | Konsistenz mit neuem Lifecycle (§7) und Hierarchie (§3) |
| Nummerierung | §§ 2–3 eingefügt; nachfolgende Abschnitte um 2 verschoben (alt §2→neu §4, etc.) | Modifiziert | Platz für Governance und Hierarchy am Dokumentanfang |

### Unveränderte Abschnitte

Die folgenden Abschnitte wurden inhaltlich nicht verändert (nur umnummeriert):

| Alter § | Neuer § | Titel |
|---------|---------|-------|
| §3 | §5 | Project Baseline |
| §6 | §8 | Sprint Rules |
| §8 | §10 | Implementation Rules |
| §9 | §11 | Testing Rules |
| §10 | §12 | Release Rules |
| §11 | §13 | ADR Rules |
| §12 | §15 | Definition of Done |

---

## Self-Review

| Prüfpunkt | Ergebnis |
|-----------|----------|
| Bestehender Development Standard v1.0 inhaltlich bewahrt | ✓ Alle Abschnitte übernommen, kein normativer Inhalt entfernt |
| Keine Architekturänderungen eingeführt | ✓ Architecture Book v2.0 bleibt unverändert referenziert |
| Keine duplizierte Governance | ✓ §2.3 verbietet normative Duplikation; Verantwortlichkeiten in §3.2 klar getrennt |
| Templates subordinat zum Development Standard | ✓ §14.1 definiert explizite Subordination |
| Prompts enthalten keine normativen Projektregeln | ✓ §2.2 verbietet Architektur-/Scope-/Regel-Definition in Prompts |
| Single Process Authority | ✓ §2.1 definiert dieses Dokument als einzige Prozessquelle |
| Interne Konsistenz | ✓ Lifecycle (§7), Review (§9), Checklists (§16) und Workflow-Diagramm (§17.A) sind synchron |
| Normative Terminologie definiert | ✓ §1.1 definiert MUSS/SOLL/DARF/DARF NICHT |
