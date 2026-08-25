# Implementation Plan 1.0 — Independent Chapter Review Kapitel 11 (Risk Management)

| Feld | Wert |
|---|---|
| Auditgegenstand | Milestone 1.0 Implementation Plan, Kapitel 11 — Risk Management (PS-06) |
| Pfad | `docs/milestone-1.0-implementation-plan.md` |
| Dokumentstatus | DRAFT |
| Auditart | Independent Chapter Review |
| Auditumfang | Ausschließlich Kapitel 11. Kapitel 1–10 und Anhänge nur als Referenz. |
| Datum | 2026-08-03 |
| Autorität | Governance Architect |
| Vorgängerprüfungen | Consistency Audit Kapitel 9; Independent Chapter Review Kapitel 10 und Gesamtbewertung |

---

## 1. Prüfumfang

### 1.1 Scope-Prüfung

| Prüfpunkt | Ergebnis |
|---|---|
| Kapitel behandelt ausschließlich Engineering Risk Management | Bestätigt |
| Kein Incident Management | Bestätigt |
| Kein Betrieb, kein Monitoring | Bestätigt |
| Keine Security Operations | Bestätigt |
| Kein Runtime-Verhalten | Bestätigt — RC-09 schließt Runtime-, Betriebs- und Incidentrisiken ausdrücklich aus; 11.4 führt keine entsprechende Klasse |
| Kein Produktionssupport | Bestätigt |
| Geltungsbereich Planung, Implementierung, Verifikation | Bestätigt |
| Charakter als Framework, nicht als Register | Bestätigt — 11.3 bis 11.7 und 11.12 bis 11.14 sind normativ; das Register in 11.11 ist Aggregation, nicht Kapitelzweck |

### 1.2 Strukturprüfung

| Abschnitt | Vorhanden | Bewertung |
|---|---|---|
| 11.1 Purpose | Ja | Zweck, Abgrenzung und acht Bezugsverhältnisse vollständig |
| 11.2 Risk Objectives | Ja | RO-01..RO-08 mit Ableitung aus Engineering Goals, Non-Functional Requirements, Quality Gates und Governance-Prinzipien |
| 11.3 Risk Principles | Ja | RP-01..RP-09 mit Konfliktregel |
| 11.4 Risk Classification | Ja | RK-01..RK-16; alle sechzehn geforderten Klassen; Ausschlussregel für Runtime |
| 11.5 Risk Ownership & Decision Authority | Ja | **Ergänzung** — begründet |
| 11.6 Risk Lifecycle | Ja | L-1..L-7, fünf Zustände, fünf Zustandsregeln |
| 11.7 Risk Assessment | Ja | Ordinale Skalen, Kritikalitätsmatrix, Priorisierung, Restrisiko, Reassessment |
| 11.8 Engineering Specification Risk Mapping | Ja | R-001..R-005 mit allen elf geforderten Feldern |
| 11.9 Waiver Risk Mapping | Ja | **Ergänzung** — begründet |
| 11.10 Governance Risk Transfer GR-001 | Ja | Überführung ohne neue Entscheidung |
| 11.11 Consolidated Risk Register | Ja | **Ergänzung** — begründet |
| 11.12 Risk Traceability | Ja | Kette, Lückenlosigkeitsnachweis, Behandlung work-package-freier Risiken |
| 11.13 Interfaces to Migration and Rollout | Ja | **Ergänzung** — begründet |
| 11.14 Risk Constraints | Ja | RC-01..RC-12 |
| 11.15 Completion Conditions | Ja | RCC-01..RCC-14 mit Soll, Ist, Nachweis, Review, Evidence, Owner |
| 11.16 Final Risk Statement | Ja | Acht Bedingungen, Abgrenzung zur Risikofreiheit, Feststellung zum Stichtag |

#### Bewertung der vier Strukturergänzungen

| Ergänzung | Normativ erforderlich | Neue Anforderung | Neue Governance-Ebene | Bewertung |
|---|---|---|---|---|
| 11.5 Ownership & Decision Authority | Ja — RC-01, RC-02 und die Owner-Spalten sind ohne definierte Funktionen nicht prüfbar | Nein | Nein — Funktionen unverändert aus Kapitel 7.6 und 8.5 | Zulässig |
| 11.9 Waiver Risk Mapping | Ja — WAIVER-DEV-001 §7 weist Mitigationen ausdrücklich dem Implementation Plan zu | Nein — reine Überführung ohne Neubewertung | Nein | Zulässig |
| 11.11 Consolidated Risk Register | Ja — ohne Aggregation ist RCC-04 bis RCC-08 nicht führbar | Nein — Aggregation ohne eigenen Inhalt | Nein | Zulässig |
| 11.13 Interfaces to Migration and Rollout | Ja — verhindert, dass Kapitel 12 und 13 eigene Klassifikations- und Bewertungsmodelle bilden | Nein | Nein | Zulässig |

### 1.3 Formale Prüfung

| Prüfpunkt | Ergebnis |
|---|---|
| Nummerierung 11.1 bis 11.16 | Lückenlos, keine Dubletten |
| ID-Räume RO, RP, RK, L, RC, RCC | Eindeutig; keine Kollision mit den ID-Räumen der Kapitel 1–10 und der Anhänge |
| Beibehaltung der Ursprungskennungen R-, WR-, GR- | Bestätigt; keine Neunummerierung bei Überführung |
| Referenzen auf Kapitel 2, 4 bis 10 | Aufgelöst |
| Referenzen auf Anhang A und Anhang B | Aufgelöst |
| Referenzen auf Kapitel 12 und 13 | Als Schnittstellenzusage geführt; Auflösung mit Erstellung der Kapitel |
| Circular References | Keine. Kapitel 11 referenziert vorangehende Kapitel und kündigt Anschlussstellen an; kein vorangehendes Kapitel referenziert Kapitel 11 inhaltlich. |

### 1.4 Prüfung des Risk Mappings

#### Vollständigkeit der Überführung

| Quelle | Soll | Überführt | Ergebnis |
|---|---|---|---|
| Engineering Specification — Risikoregister | 5 | 5 | Vollständig |
| WAIVER-DEV-001 §7.1 — Risiken des Waivers | 4 | 4 | Vollständig |
| WAIVER-DEV-001 §7.2 — Risiken ohne Waiver | 3 | 0 | Zutreffend nicht überführt; der Waiver ist genehmigt, die Risiken können nicht mehr eintreten. Die Feststellung ist im Kapitel dokumentiert. |
| Anhang A — Governance Risk Register | 1 | 1 | Vollständig |
| **Summe** | **10** | **10** | **Vollständig** |

#### Prüfung der Bewertungstreue

Die aus den Quelldokumenten übernommenen Bewertungen wurden gegen die
Quellwerte geprüft.

| ID | Quellwert Wahrscheinlichkeit / Auswirkung | Im Kapitel | Kritikalität laut Matrix | Im Kapitel | Ergebnis |
|---|---|---|---|---|---|
| R-001 | Mittel / Hoch | Mittel / Hoch | Hoch | Hoch | Übereinstimmend |
| R-002 | Niedrig / Kritisch | Niedrig / Kritisch | Hoch | Hoch | Übereinstimmend |
| R-003 | Niedrig / Hoch | Niedrig / Hoch | Erhöht | Erhöht | Übereinstimmend |
| R-004 | Mittel / Mittel | Mittel / Mittel | Erhöht | Erhöht | Übereinstimmend |
| R-005 | Niedrig / Mittel | Niedrig / Mittel | Beobachtung | Beobachtung | Übereinstimmend |
| WR-1 | Niedrig / Hoch | Niedrig / Hoch | Erhöht | Erhöht | Übereinstimmend |
| WR-2 | Niedrig / Mittel | Niedrig / Mittel | Beobachtung | Beobachtung | Übereinstimmend |
| WR-3 | Niedrig / Mittel | Niedrig / Mittel | Beobachtung | Beobachtung | Übereinstimmend |
| WR-4 | Niedrig / Niedrig | Niedrig / Niedrig | Beobachtung | Beobachtung | Übereinstimmend |
| GR-001 | — (Befund, ohne Quellbewertung) | Eingetreten / Hoch | Kritikalität aus Auswirkung | Hoch | Übereinstimmend — siehe F11-002 |

Keine Neubewertung, keine Abweichung von den Quellwerten. RC-11 eingehalten.

#### Prüfung der Registerverteilung

| Kritikalität | Auszählung aus 11.11 | Angabe im Kapitel | Ergebnis |
|---|---|---|---|
| Kritisch | 0 | 0 | Übereinstimmend |
| Hoch | R-001, R-002, GR-001 = 3 | 3 | Übereinstimmend |
| Erhöht | R-003, R-004, WR-1 = 3 | 3 | Übereinstimmend |
| Beobachtung | R-005, WR-2, WR-3, WR-4 = 4 | 4 | Übereinstimmend |

### 1.5 Prüfung auf unzulässige Einführungen

| Verbotene Einführung | Ergebnis |
|---|---|
| Neue Functional oder Non-Functional Requirements | Keine |
| Neue Acceptance Criteria | Keine |
| Neue Quality Gates | Keine — 11.8 bis 11.10 verweisen ausschließlich auf QG-001 bis QG-008 |
| Neue Governance-Ebenen | Keine — die Entscheidungsinstanzen in 11.5 sind unverändert aus Kapitel 7.6 übernommen |
| Neue Evidence-Artefakte | Keine — sämtliche Nachweisverweise zeigen auf Kapitel 8.5; RC-08 untersagt risikospezifische Evidence ausdrücklich |
| Neue Architektur, neue ADRs | Keine — RC-05, RC-06 |
| Neue Traceability-Ebene | Keine — 11.12 weist den Risikoknoten als Einstiegsknoten aus; alle Folgeknoten bestehen |

### 1.6 Konformitätsprüfung

| Bezugsrahmen | Ergebnis |
|---|---|
| Engineering Specification 1.0 | Konform — Risiken und Mitigationen unverändert übernommen |
| Development Standard v1.1 | Konform — keine abweichenden Prüf- oder Schließungszeitpunkte |
| WAIVER-DEV-001 | Konform — Risiken überführt, Geltungsbegrenzung als WR-2 geführt |
| Milestone 1.0 Charter | Konform |
| Bootstrap Baseline 1.0 | Konform — RC-06 schützt die Change Control |
| Architecture Book v2.0 | Konform — RC-05 |
| Kapitel 6 (Work Packages) | Konform — Zuordnungen entsprechen WP-001 bis WP-007; Priorisierung erzeugt keine abweichende Reihenfolge |
| Kapitel 8 (Evidence) | Konform — sämtliche Evidence-IDs existieren |
| Kapitel 9 (Quality Gates) | Konform — Gate-Zuordnungen entsprechen 8.7 und 9.4 |
| Kapitel 10 (Constraints) | Konform — RC-10 entspricht ST-09; keine Terminaussage |

### 1.7 Prüfung der Schnittstellen zu Migration und Rollout

| Prüfpunkt | Ergebnis |
|---|---|
| Klasse RK-10 für Migration definiert | Ja |
| Klasse RK-11 für Rollout definiert | Ja |
| Übernahmepflicht für Bewertungs-, Lifecycle- und Ownership-Regeln festgelegt | Ja |
| Verbot eigener Klassifikations- und Bewertungsmodelle in Kapitel 12 und 13 | Ja |
| Eskalationsregel für baselineberührende Migrations- oder Rolloutrisiken | Ja |
| Klassen RK-10 und RK-11 derzeit ohne Eintrag | Ja — als Folge der ausstehenden Kapitel ausdrücklich ausgewiesen, siehe F11-004 |
| Inhaltliche Vorwegnahme der Kapitel 12 oder 13 | Keine |

---

## 2. Befunde

### F11-001

| Feld | Inhalt |
|---|---|
| **ID** | F11-001 |
| **Severity** | Medium |
| **Kapitel** | 11.10; Anhang A |
| **Beschreibung** | GR-001 ist nach der Überführung an zwei Stellen geführt: als Pending Resolution in Anhang A und als Registereintrag in Kapitel 11.10 und 11.11. Ohne eindeutige Zuständigkeitsteilung besteht die Gefahr divergierender Stände. |
| **Empfehlung** | Zuständigkeitsteilung in beiden Fundstellen ausdrücklich festhalten. |
| **Status** | **CLOSED** — Kapitel 11.10 weist die Verortung aus: Anhang A bleibt Fundstelle der Pending Resolution, die laufende Registerführung liegt in Kapitel 11. Anhang A wurde um eine entsprechende Zeile ergänzt, die auf 11.10 und 11.11 verweist. Beide Fundstellen sind damit wechselseitig verbunden. |

### F11-002

| Feld | Inhalt |
|---|---|
| **ID** | F11-002 |
| **Severity** | Low |
| **Kapitel** | 11.7; 11.10 |
| **Beschreibung** | GR-001 wird mit der Wahrscheinlichkeitsangabe „Eingetreten" geführt. Diese Stufe war in der ursprünglichen Skala nicht definiert; die Kritikalitätsmatrix war auf sie nicht anwendbar. |
| **Empfehlung** | Skala um die Behandlung bereits eingetretener Sachverhalte ergänzen, ohne ein neues Bewertungsmodell einzuführen. |
| **Status** | **CLOSED** — 11.7 wurde um die Stufe „Eingetreten" ergänzt: die Wahrscheinlichkeitsstufe entfällt, die Kritikalität ergibt sich allein aus der Auswirkung und entspricht der Spalte Hoch. Für GR-001 (Auswirkung Hoch) ergibt sich Kritikalität Hoch — übereinstimmend mit der Angabe im Kapitel. Keine neue Anforderung, keine neue Governance-Ebene. |

### F11-003

| Feld | Inhalt |
|---|---|
| **ID** | F11-003 |
| **Severity** | Editorial |
| **Kapitel** | 11.4, RK-08 |
| **Beschreibung** | Die Risikoklasse Schedule könnte als Einstieg in Terminplanung gelesen werden, die durch ST-09 und RC-10 untersagt ist. |
| **Empfehlung** | Abgrenzung in der Klassendefinition halten. |
| **Status** | **CLOSED** — Die Klassendefinition beschränkt RK-08 ausdrücklich auf Reihenfolge- und Abhängigkeitswirkungen und schließt Termine aus. RC-10 bestätigt dies für das gesamte Kapitel. Keine Korrektur erforderlich. |

### F11-004

| Feld | Inhalt |
|---|---|
| **ID** | F11-004 |
| **Severity** | Medium |
| **Kapitel** | 11.13; 11.11 |
| **Beschreibung** | Die Risikoklassen RK-10 (Migration) und RK-11 (Rollout) sind ohne Eintrag. Das konsolidierte Register ist damit für den Milestone noch nicht vollständig. |
| **Empfehlung** | Mit Erstellung der Kapitel 12 und 13 befüllen; Registerstand anschließend fortschreiben. |
| **Status** | **OPEN** — Für Kapitel 11 **nicht blockierend**: die Leere ist Folge der noch ausstehenden Kapitel und im Kapitel ausdrücklich als solche ausgewiesen. Der Befund gehört zum planweiten Befund GP-001 und entfällt mit dessen Schließung. |

### F11-005

| Feld | Inhalt |
|---|---|
| **ID** | F11-005 |
| **Severity** | Low |
| **Kapitel** | 11.16 |
| **Beschreibung** | Die Abschlussfeststellung erklärt die Engineering Risks als kontrolliert, obwohl ein Risiko im Zustand PENDING DECISION geführt wird. |
| **Empfehlung** | Vorbehalt ausdrücklich benennen. |
| **Status** | **CLOSED** — Die Feststellung führt den Vorbehalt ausdrücklich: „vorbehaltlich der ausstehenden Entscheidung zu GR-001 und der Bestätigung durch den Independent Review". Bedingung 6 des Final Risk Statement verlangt für PENDING DECISION ausdrücklich Instanz und Frist; beide liegen vor. Die Feststellung ist damit tragfähig. |

### F11-006

| Feld | Inhalt |
|---|---|
| **ID** | F11-006 |
| **Severity** | Low |
| **Kapitel** | 11.15, RCC-14 |
| **Beschreibung** | Die Completion Condition „keine neuen Requirements, Kriterien, Gates, Evidence oder Governance-Ebenen" ist eine Selbstauskunft des Kapitels. |
| **Empfehlung** | Extern prüfen. |
| **Status** | **CLOSED** — Extern geprüft in Abschnitt 1.5 dieses Berichts. Sämtliche sieben Prüfpunkte ohne Befund. Die Selbstauskunft ist bestätigt. |

---

## 3. Befundübersicht

| ID | Severity | Abschnitt | Status | Blockierend für Kapitel 11 |
|---|---|---|---|---|
| F11-001 | Medium | 11.10, Anhang A | CLOSED | Nein |
| F11-002 | Low | 11.7, 11.10 | CLOSED | Nein |
| F11-003 | Editorial | 11.4 | CLOSED | Nein |
| F11-004 | Medium | 11.11, 11.13 | **OPEN** | Nein |
| F11-005 | Low | 11.16 | CLOSED | Nein |
| F11-006 | Low | 11.15 | CLOSED | Nein |

| Severity | Gesamt | Offen | Geschlossen |
|---|---|---|---|
| Critical | 0 | 0 | 0 |
| High | 0 | 0 | 0 |
| Medium | 2 | 1 | 1 |
| Low | 3 | 0 | 3 |
| Editorial | 1 | 0 | 1 |
| **Summe** | **6** | **1** | **5** |

---

## 4. Wirkung auf planweite Befunde

| Planweiter Befund | Wirkung von Kapitel 11 |
|---|---|
| GP-001 — Planungsscope unvollständig | **Teilweise geschlossen.** PS-06 ist behandelt. PS-04 und PS-05 bleiben offen. |
| GP-002 — Nicht auflösbare Vorwärtsverweise | Teilweise reduziert. Der Verweis aus Kapitel 6.5 auf ein Risikokapitel ist aufgelöst. Die Verweise auf Migrations- und Rolloutkapitel bleiben offen. |
| GP-003 — Risiken der Engineering Specification nicht überführt | **CLOSED.** R-001 bis R-005 sind vollständig überführt und mit Mitigation, Nachweis, Owner, Review und Completion versehen. |
| GP-004 — GR-001 offen | Unverändert. Kapitel 11.10 verortet, entscheidet nicht. |
| GP-005 — Selbsterklärte Schließungen nicht extern bestätigt | Unverändert; zusätzlich betrifft dies nunmehr RCC-01 bis RCC-14. |

---

## 5. Chapter 11 Governance Status

```
Chapter 11 Governance Status

OPEN:
1 Finding
  F11-004 (Medium) — Risikoklassen RK-10 und RK-11 ohne Eintrag;
                     Folge der ausstehenden Kapitel 12 und 13

CLOSED:
5 Findings
  F11-001 (Medium), F11-002 (Low), F11-003 (Editorial),
  F11-005 (Low), F11-006 (Low)

BLOCKING:
  Für Kapitel 11: keine.

NON BLOCKING:
  F11-001, F11-002, F11-003, F11-005, F11-006 — geschlossen.
  F11-004 ist für Kapitel 11 nicht blockierend, da die Leere der Klassen
  RK-10 und RK-11 im Kapitel ausdrücklich als Folge der ausstehenden
  Kapitel ausgewiesen ist. Der Befund gehört zu GP-001 und entfaellt mit
  dessen Schliessung.

Recommendation:

APPROVED WITH FINDINGS
```

---

## 6. Auflagen

| # | Auflage | Adressat | Frist |
|---|---|---|---|
| 1 | Befüllung der Risikoklassen RK-10 und RK-11 mit Erstellung der Kapitel 12 und 13 | Lead Implementation Planner | Mit Kapitel 12 und 13 |
| 2 | Fortschreibung des konsolidierten Registers nach Aufnahme von Migrations- und Rolloutrisiken | Governance Architect | Vor W-2 |
| 3 | Übernahme der Bewertungs-, Lifecycle- und Ownership-Regeln in Kapitel 12 und 13 ohne Bildung eigener Modelle | Lead Implementation Planner | Mit Kapitel 12 und 13 |
| 4 | Bestätigung von RCC-01 bis RCC-14 durch den Independent Review des Gesamtplans | Independent Review | Mit W-3 |

---

## 7. Vorgenommene Korrekturen

| Korrektur | Ort | Art |
|---|---|---|
| Ergänzung der Wahrscheinlichkeitsstufe „Eingetreten" mit Kritikalitätsregel | 11.7 | Schließung von F11-002 |
| Ergänzung der Zeile Registerführung mit Verweis auf 11.10 und 11.11 | Anhang A, PR-001.9 | Schließung von F11-001 |

Keine Umstrukturierung der Kapitel 1 bis 11. Beide Korrekturen sind
Ergänzungen innerhalb bestehender Tabellen.

---

## 8. Referenzen

- Implementation Plan 1.0: `docs/milestone-1.0-implementation-plan.md`
- Independent Chapter Review Kapitel 10 und Gesamtbewertung: `docs/audits/implementation-plan-1.0-chapter-10-independent-review.md`
- Consistency Audit Kapitel 9: `docs/audits/implementation-plan-1.0-chapter-9-consistency-audit.md`
- Engineering Specification 1.0: `docs/milestone-1.0-engineering-spec.md`
- WAIVER-DEV-001: `docs/governance/waiver-dev-001.md`
- Milestone 1.0 Charter: `docs/milestone-1.0-charter.md`
- Bootstrap Baseline 1.0: `docs/baselines/bootstrap-baseline-1.0.md`
- Development Standard v1.1: `docs/development-standard-v1.1.md`
- Architecture Book v2.0: `docs/architecture-book-v2.md`
