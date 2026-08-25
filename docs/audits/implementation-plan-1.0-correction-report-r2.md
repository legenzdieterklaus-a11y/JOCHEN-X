# Implementation Plan 1.0 — Correction Report R2

| Eigenschaft | Wert |
|---|---|
| **Dokumenttyp** | Correction Report — Workflow-Schritt **W-4** |
| **Korrekturzyklus** | R2 |
| **Datum** | 2026-08-05 |
| **Rolle** | Implementation Plan Governance Editor |
| **Grundlage** | [Independent Review W-3](implementation-plan-1.0-independent-review-w3.md) |
| **Korrigiertes Dokument** | [Milestone 1.0 Implementation Plan](../milestone-1.0-implementation-plan.md), Revision R1.1 → **R1.2** |
| **Umfang** | 2 Findings: 1 Medium, 1 Editorial |
| **Ergebnis** | **Beide Findings CLOSED.** Keine weitere Änderung vorgenommen. |
| **Dokumentstatus** | **DRAFT** — unverändert |

---

## 1. Autorisierter Umfang

Der Umfang ist durch den Independent Review W-3 §11 abschließend bestimmt:

| # | Zugelassen | Umgesetzt |
|---|---|---|
| 1 | W3-M-01 — Korrektur der Exportanzahl an vier Stellen | **Ja** |
| 2 | W3-E-01 — Registerregel 3 um klassenbezogene Präfixe ergänzen (optional) | **Ja** |
| 3 | Revisionshistorie — Zeile R1.2 | **Ja** |

Jede weitere Änderung war ausdrücklich nicht zugelassen und ist nicht erfolgt
(Abschnitt 4).

---

## 2. W3-M-01 — CLOSED

| Feld | Inhalt |
|---|---|
| **Finding ID** | W3-M-01 |
| **Severity** | Medium |
| **Ursprüngliches Finding** | Kapitel 3.4 führte die Baseline-Invariante API-01 unter „Öffentliche Exports (**20 Symbole**)", im Fließtext als „die folgenden **zwanzig** Symbole" und mit der Summenzeile **20**. Die Tabelle selbst zählt 6 + 2 + 7 + 4 + 3 = **22** Symbole auf; `app/bootstrap/__init__.py` deklariert in `__all__` **22** Symbole, die mit der Aufzählung des Plans exakt übereinstimmen. Die Zahl 20 war zusätzlich in die Null-Delta-Tabelle 4.7 übernommen. |
| **Wirkung des Findings** | API-01 gehört zum Bestätigungsumfang der Phase A (Kapitel 3.8, EV-D01) und ist Vergleichsbasis des API-Oberflächenvergleichs EV-I03. Eine Bestätigung gegen „20" hätte nach Kapitel 3.2 Verfahrensregel 3 als Abweichung gewertet werden und die Planung unterbrechen müssen. |
| **Status** | **CLOSED** |

### 2.1 Durchgeführte Änderungen

| # | Kapitel | Stelle | Vorher | Nachher |
|---|---|---|---|---|
| C-01 | 3.4 | Überschrift API-01 | `#### API-01 — Öffentliche Exports (20 Symbole)` | `#### API-01 — Öffentliche Exports (22 Symbole)` |
| C-02 | 3.4 | Fließtext | „exportiert die folgenden **zwanzig** Symbole" | „exportiert die folgenden **zweiundzwanzig** Symbole" |
| C-03 | 3.4 | Summenzeile der Exporttabelle | `\| **Summe** \| \| **20** \|` | `\| **Summe** \| \| **22** \|` |
| C-04 | 4.7 | Null-Delta-Tabelle, Zeile Exportmenge | „Öffentliche Exportmenge (**20** Symbole)" | „Öffentliche Exportmenge (**22** Symbole)" |

### 2.2 Ausdrücklich nicht geändert

| Gegenstand | Status |
|---|---|
| Symbolmenge in der API-01-Tabelle | **Unverändert** — 22 Symbole in fünf Gruppen, keine Ergänzung, keine Streichung, keine Umbenennung |
| Gruppierung und Gruppen-Anzahlen (6 / 2 / 7 / 4 / 3) | **Unverändert** |
| API-02 — Interne Re-Exports (2 Symbole) | **Unverändert** |
| API-03 — Consumer-Import-Kompatibilität | **Unverändert** |
| API-04 — Änderungsschutz | **Unverändert** |
| Baseline-Invarianten BI-01 bis BI-07 | **Unverändert** |
| Bestätigungsumfang in 3.8 | **Unverändert** — verweist unverändert auf API-01..API-04 |
| Übrige Zeilen der Null-Delta-Tabelle 4.7 | **Unverändert** — weiterhin 11 Erhaltungsbereiche |

### 2.3 Verifikation

| Prüfung | Ergebnis |
|---|---|
| Reststellen „20 Symbole" / „zwanzig Symbole" / Summenzeile 20 | **0** |
| Symbolmenge des Plans gegen `__all__` von `app.bootstrap` | 22 / 22, **Mengen identisch**, keine Abweichung in beiden Richtungen |
| Summenbildung 6 + 2 + 7 + 4 + 3 | 22 — stimmt mit der Summenzeile überein |
| Konsistenz 3.4 gegen 4.7 | Beide führen 22 |

---

## 3. W3-E-01 — CLOSED

| Feld | Inhalt |
|---|---|
| **Finding ID** | W3-E-01 (im Global Consistency Audit R2 als R2-E-01 geführt) |
| **Severity** | Editorial |
| **Ursprüngliches Finding** | Registerregel 3 in Kapitel 11.11 sah für neu erkannte Risiken „eine fortlaufende Kennung des Frameworks" und die Quelle „Implementation" oder „Review" vor. Die sechs im Plan entstandenen Einträge tragen die Präfixe **MGR** und **ROR** sowie die Quellenangabe „Implementation Plan Kapitel 12" beziehungsweise „Kapitel 13". |
| **Status** | **CLOSED** |

### 3.1 Durchgeführte Änderung

| # | Kapitel | Stelle | Änderung |
|---|---|---|---|
| C-05 | 11.11 | Registerregel 3 | Regel um die ausdrückliche Zulässigkeit klassenbezogener Präfixe ergänzt: **MGR** für Klasse RK-10, **ROR** für Klasse RK-11; die Quellenangabe benennt das erzeugende Kapitel. |

Die Regel beschreibt damit die bereits geführte Praxis, statt ihr zu
widersprechen. Es wird keine neue Kennungssystematik eingeführt.

### 3.2 Ausdrücklich nicht geändert

| Gegenstand | Status |
|---|---|
| Registereinträge (16) | **Unverändert** — keine Kennung, Klasse, Kritikalität, Owner, Status, Quelle oder Fundstelle geändert |
| Registerregeln 1, 2, 4, 5, 6 | **Unverändert** |
| Zusammensetzung, Verteilung, Statusübersicht | **Unverändert** — 16 / 16 / 16 |
| Prüfzeilen 11.12 und RCC-04 bis RCC-08 | **Unverändert** — 16 |
| Herleitungen in 12.9 und 13.9 | **Unverändert** |

---

## 4. Nachweis der Einhaltung der Bearbeitungsgrenzen

### 4.1 Nicht geänderte Fremddokumente

| Dokument | Letzte Änderung | Ergebnis |
|---|---|---|
| Milestone 1.0 Charter | 2026-08-02 | **Unverändert** |
| Engineering Specification 1.0 | 2026-08-03 | **Unverändert** |
| Bootstrap Baseline 1.0 | 2026-08-01 | **Unverändert** |
| Architecture Book v2.0 | 2026-07-30 | **Unverändert** |
| ADR-005, ADR-006, ADR-007, ADR-011 | 2026-07-26 bis 2026-07-30 | **Unverändert** |
| Development Standard v1.1 | 2026-07-27 | **Unverändert** |
| WAIVER-DEV-001 | 2026-08-02 | **Unverändert** |
| WAIVER-AMENDMENT-001 | 2026-08-05 | **Unverändert** |
| GDR-001 | 2026-08-05 | **Unverändert** |

### 4.2 Nicht geänderte Planinhalte

| Gegenstand | Ergebnis |
|---|---|
| Functional Requirements (14) | Unverändert |
| Non-Functional Requirements (10) | Unverändert |
| Acceptance Criteria (29) | Unverändert |
| Quality Gates (8) | Unverändert |
| Work Packages (7) | Unverändert |
| Deliverables (10) | Unverändert |
| Evidence (20) | Unverändert |
| Delta Analysis (Kapitel 4, 15 Deltas) | Unverändert — ausgenommen die Zahl in der Null-Delta-Zeile 4.7 (C-04) |
| Module Work Breakdown (Kapitel 5, 15 Einträge) | Unverändert |
| Sequencing (Kapitel 6) | Unverändert |
| Implementation Strategy (Kapitel 7) | Unverändert |
| Verification Strategy (Kapitel 8) | Unverändert |
| Test Strategy (Kapitel 9) | Unverändert |
| Risiken und Register (Kapitel 11) | Unverändert — ausgenommen Registerregel 3 (C-05) |
| Migration (Kapitel 12) | Unverändert |
| Rollout (Kapitel 13) | Unverändert |
| Anhang A, Anhang B | Unverändert |
| Governance Chain | Unverändert |
| Authorization Boundary | Unverändert |

### 4.3 Nicht erzeugt

| Gegenstand | Anzahl |
|---|---|
| Neue Kapitel | **0** — Struktur unverändert bei 13 Kapiteln und 2 Anhängen, 146 Unterabschnitten |
| Neue Tabellen | **0** |
| Neue Anforderungen, Kriterien, Gates, Work Packages | **0** |
| Neue Registereinträge | **0** |
| Neue Evidence-Artefakte | **0** |
| Architekturänderungen | **0** |
| Codebeispiele oder Implementierungsdetails | **0** |
| Neue Governance-Instanzen oder Prozessschritte | **0** |

---

## 5. Revisionshistorie

| # | Kapitel | Änderung |
|---|---|---|
| C-06 | 1.1 | Revision von „R1.1 — Editorial Synchronization" auf „**R1.2 — Correction Cycle R2**" |
| C-07 | 1.1 | Neue Historienzeile R1.2 mit Datum, Änderungsbeschreibung und Prüfartefakten |

Eintrag im Wortlaut:

> **R1.2 · 2026-08-05 · Correction Cycle R2** — Abarbeitung der Findings des
> Independent Review (W-3): W3-M-01 (Korrektur der Exportanzahl in API-01 von
> 20 auf 22 an vier Stellen; Symbolmenge unverändert) und W3-E-01
> (Registerregel 3 um klassenbezogene Präfixe ergänzt). Keine inhaltlichen
> Änderungen.

---

## 6. Ergebnis

| Finding | Severity | Status |
|---|---|---|
| W3-M-01 | Medium | **CLOSED** |
| W3-E-01 | Editorial | **CLOSED** |

Beide Findings des Independent Review W-3 sind geschlossen. Der Workflow-Schritt
**W-4 ist abgeschlossen**.

Der einzige autorisierte nächste Schritt ist **W-5 — Supplementary Independent
Review**.

---

*Ende Correction Report R2.*
