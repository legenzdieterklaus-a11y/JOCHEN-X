# Core Principles 1.0 — Independent Governance Review (W-4)

| Eigenschaft | Wert |
|---|---|
| **Dokumenttyp** | Independent Governance Review — Workflow-Schritt W-4 |
| **Prüfgegenstand** | [JOCHEN X – Core Principles 1.0](../core-principles-1.0.md), **Revision R2**, Status DRAFT, Kapitel 0–12, Schlussbestimmung, Revisionshistorie, Anhang A |
| **Mitgeprüfte Artefakte** | [Correction Report R2](core-principles-1.0-correction-report-r2.md), [Verification Summary R2](core-principles-1.0-verification-summary-r2.md), [Revision History Update R2](core-principles-1.0-revision-history-update-r2.md) |
| **Datum** | 2026-08-07 |
| **Rolle** | Independent Governance Review Board |
| **Prüfmaßstab** | Prüfschwerpunkte 1–11 gemäß W-4-Auftrag |
| **Ergebnis** | **APPROVED** · 0 Critical, 0 High, 0 Medium, 0 Low, 0 Editorial |
| **Am Prüfgegenstand geändert** | Nichts |

---

# TEIL 1 — Independent Governance Review W-4

## 0. Independence Statement

Dieser Review wurde in einer von R0, W-1, R1 (W-2), W-3 und R2 getrennten
Sitzung durchgeführt. An der Erstellung des Prüfgegenstands und an den
Correction Cycles war diese Prüfung nicht beteiligt.

**Methodische Absicherung.** Kein Nachweis der R2-Artefakte wurde ungeprüft
übernommen. Sämtliche tragenden Behauptungen wurden gegen die Primärquellen
nachvollzogen:

| Behauptung der R2-Artefakte | Eigenständig nachgeprüft gegen |
|---|---|
| §3.3 enthält neun Dokumenttypen mit Architecture Book an der Spitze | Development Standard v1.1, §3.1–§3.3 (Original) |
| Strenge Monotonie der Übernahme in die Rangordnung | Eigener Abgleich beider Tabellen |
| §3.2 weist Prozess/Form-Zuständigkeit dem Development Standard zu | Development Standard v1.1, §3.2 (Original) |
| Kein weiteres Bestandsartefakt enthält eine konkurrierende Hierarchieregel | Eigene Volltextsuche über Charter, Engineering Specification, Implementation Plan, ADRs, Baselines, Waiver, GDR |
| Schließung aller neun W-3-Findings | W-3-Bericht (Original) gegen Wortlaut R2, Fundstelle für Fundstelle |
| W-1-Findings bleiben geschlossen | W-1-Bericht (Original), Abgleich der Findingliste |

Die formale Bewertung der Unabhängigkeit obliegt gemäß W-3-Bedingung B-7 der
Genehmigungsinstanz und ist im Approval Record zu dokumentieren.

**Am Prüfgegenstand wurde nichts geändert.** Es wurden keine Formulierungen
verbessert, keine Prinzipien vorgeschlagen und keine Kapitel ergänzt.

---

## 1. Prüfschwerpunkt 1 — Vollständigkeit aller W-1- und W-3-Findings

### 1.1 W-3-Findings (Änderungsgrundlage R2)

Jedes der neun Findings wurde gegen den Wortlaut von R2 verifiziert:

| Finding | Kritikalität | Geforderte Schließung (W-3, B-1 bis B-5) | Befund in R2 | Status |
|---|---|---|---|---|
| W3-H-01 | High | Verhältnis zu DS §3.3 geklärt, Development Standard verortet | Rangordnung mit 12 Rängen und Quellenspalte; Development Standard auf Rang 4; Absatz „Verhältnis zum Development Standard"; Rule-1-Absatz um Development Standard ergänzt | **CLOSED — bestätigt** |
| W3-M-01 | Medium | „Tragweite" bestimmt oder auf Wirkungsskala zurückgeführt | Begriffsbestimmung: gleichbedeutend mit Wirkungsstufe, „Ein zweites Maßsystem besteht nicht"; alle vier Fundstellen (5.5, 6.3, 7.8, 8.4) unverändert und nun bestimmt | **CLOSED — bestätigt** |
| W3-M-02 | Medium | Verhältnis 6.2 ↔ 5.10 / 8.5 für nicht-menschliche Akteure eindeutig | „Nachweis genügt für" / „genügt als Identitätsgrundlage für"; neuer Absatz „Verhältnis zur menschlichen Freigabe" mit wörtlichem Ausschluss beider Fehllesarten und Verweis auf Artikel 1 | **CLOSED — bestätigt** |
| W3-M-03 | Medium | Zuständigkeit Konformitätsnachweis geklärt | Materielle Pflicht bei den Core Principles; Form, Ort, Verfahren ausdrücklich beim Development Standard; „ausdrücklich" gestrichen; doppelte Zuständigkeit verneint | **CLOSED — bestätigt** |
| W3-L-01 | Low | Vorspann Kapitel 6 deckungsgleich mit Inhalt | „keine Zuordnung konkreter Rechte, Daten oder Ressourcen" | **CLOSED — bestätigt** |
| W3-L-02 | Low | Erstgenehmigung geregelt | Geltungsvorbehalt („Erstgenehmigung durch die Genehmigungsinstanz") plus Rule 3 „Anwendungsbereich"; Zirkelbezug aufgelöst | **CLOSED — bestätigt** |
| W3-L-03 | Low | Erhöhte Anforderung als Hürde wirksam | Unabhängiger Review durch unbeteiligte Instanz bei Änderungen an Kapitel 0 und 12; Durchführung nach Development Standard | **CLOSED — bestätigt** |
| W3-L-04 | Low | Verbindlichkeitsgrad indikativischer Bestimmungen | Normsprache ergänzt: indikativische Bestimmungen unbedingt verbindlich | **CLOSED — bestätigt** |
| W3-E-01 | Editorial | Revisionshistorie vollständig | R0 mit „Governance Review W-1", R1 um „Independent Review W-3" ergänzt, R2 eingetragen | **CLOSED — bestätigt** |

**Verifikation der W3-H-01-Schließung im Detail.** Der Abgleich der
Rangordnung gegen Development Standard v1.1 §3.3 (Original) bestätigt:

- §3.3 führt exakt die neun Typen Architecture Book, ADR, Development
  Standard, Engineering Specification, Review Reports, Final Verification
  Reports, Correction Reports, Templates, Prompts — in dieser Reihenfolge.
- Die Abbildung auf die Ränge 2, 3, 4, 5, 7, 8, 9, 10, 11 ist streng monoton.
  Keine §3.3-Klasse hat ihre relative Stellung verändert; §3.3 ist echte
  Teilfolge der Rangordnung.
- §3.3 trifft keine Aussage über Core Principles, Implementation Plans oder
  Implementation. Die Einordnung der Core Principles über dem Architecture
  Book ergänzt die Konfliktregel und widerspricht ihr nicht — §3.3 ordnet
  ausschließlich seine eigenen neun Typen.
- Die Maßgeblichkeitsfrage ist geregelt: „Für die in §3.3 geführten
  Dokumenttypen gilt §3.3 unverändert fort."
- Development Standard v1.1 wurde nicht geändert; Rule 1 nimmt ihn nunmehr
  namentlich vom Rückwirkungsausschluss aus.

### 1.2 W-1-Findings

Alle 22 W-1-Findings bleiben geschlossen. Die vier von W-3 als Rest- oder
Folgebefunde geführten Sachverhalte (W1-H-01 → W3-H-01, W1-H-02 → W3-M-01,
W1-M-07 → W3-L-02/L-03, W1-L-06 → W3-L-04) sind mit R2 vollständig erledigt.
Die zwei Waiver (W1-L-03, W1-L-05) wurden von W-3 geprüft und akzeptiert; die
betroffenen Fundstellen (4.8, 5.4, 7.2, 10.3) sind in R2 unverändert — die
Waiver gelten fort und stehen einer Genehmigung nicht entgegen.

**Prüfschwerpunkt 1: bestanden.**

---

## 2. Prüfschwerpunkt 2 — Keine neuen Findings durch R2

Sämtliche R2-Änderungen wurden auf Wechselwirkungen geprüft:

| Änderung | Geprüft gegen | Ergebnis |
|---|---|---|
| Rangordnung (12 Ränge) | Rule 1, Rule 2, Rule 3, Schlussbestimmung, Kapitel 12 | Widerspruchsfrei |
| Begriffsbestimmung „Tragweite" | 5.5, 6.3, 7.8, 8.4; übrige Begriffsbestimmungen; Auslegungsregel | Widerspruchsfrei; keine Fundstelle erhält eine andere Reichweite |
| 6.2 „Verhältnis zur menschlichen Freigabe" | 5.10, 8.5, Artikel 1, 6.3, 9.6, Kritische Freigabe | Widerspruchsfrei; 5.10, 8.5 und Artikel 1 im Wortlaut unverändert; 9.6 („kritische Freigabe im Sinne von 6.2") bleibt tragfähig |
| Konformitätsnachweis / Anwendungsbereich / Erhöhte Anforderung | DS v1.1 §3.2 (Original) | Zuständigkeitstrennung sauber: materielle Norm hier, Verfahren dort; kein Übergriff |
| Normsprache-Ergänzung | Kapitel 1–12, insbesondere 11.5 („sollte") | Widerspruchsfrei; die Ergänzung betrifft nur modalverblose Bestimmungen und entspricht der bisherigen Lesart |
| Geltungsvorbehalt (Erstgenehmigung) | Rule 3, Kopffeld „Gültigkeit" | Widerspruchsfrei; Erstgenehmigung und Amendment sauber getrennt |
| Kapitel-6-Vorspann | 6.1–6.3 | Selbstbeschreibung deckt den Kapitelinhalt |
| Revisionshistorie / Kopfdaten | Zählung W-1 (22 Findings: 3H/11M/6L/2E) und W-3 (9 Findings: 1H/3M/4L/1E) | Rechnerisch und inhaltlich korrekt |
| Referenzenliste (14 Einträge) | Genehmigter Bestand | Zutreffend und deklaratorisch |
| Anhang A | R2-Änderungen | Unberührt und weiterhin zutreffend — keine Änderung betrifft Kernwerte, Grundprinzipien oder Artikel |

**Keine neuen Findings.** Insbesondere wiederholt sich das Muster aus R1 —
Entstehung neuer Findings durch das Zusammenwirken von Korrekturen — nicht:
Die R2-Änderungen sind untereinander konsistent und greifen ausschließlich
klarstellend in Kapitel 0, den Kapitel-6-Vorspann und 6.2 ein.

**Prüfschwerpunkt 2: bestanden.**

---

## 3. Prüfschwerpunkt 3 — Keine Governance-Regression

| Prüfung | Ergebnis |
|---|---|
| Schutzwirkung Rule 1 | Unverändert bzw. gestärkt (Development Standard namentlich ausgenommen) |
| Bindungswirkung Rule 2 | Erhalten; entfallen ist allein die außerhalb der Zuständigkeit liegende Formvorgabe |
| Änderungsschutz Rule 3 | **Verschärft** — unabhängiger Review für Kapitel 0 und 12 |
| Genehmigtes Artefakt geändert | Nein — durch Volltextabgleich bestätigt: Development Standard v1.1 und Architecture Book v2.0 unberührt |
| Rückwirkung erzeugt | Nein |
| Genehmigung vorweggenommen | Nein — Status DRAFT, Feld „Genehmigt" offen, Geltungsvorbehalt präzisiert |
| Neue Instanz geschaffen oder Zuständigkeit an sich gezogen | Nein — Verfahrenszuständigkeit durchgehend beim Development Standard |

**Prüfschwerpunkt 3: bestanden.**

---

## 4. Prüfschwerpunkt 4 — Dokumenthierarchie konsistent mit dem Development Standard

Siehe 1.1 (Verifikation W3-H-01). Ergänzend wurde die dokumentinterne
Konsistenz geprüft: Rangordnung ↔ „Wirkung der Rangordnung" ↔ „Verhältnis zu
Governance Rule 1" bilden eine geschlossene, eindeutig anwendbare Regelung.
Es existiert eine einzige Rangordnung; die Konfliktregel des Development
Standard gilt für ihre neun Typen unverändert fort.

**Prüfschwerpunkt 4: bestanden.**

---

## 5. Prüfschwerpunkt 5 — Keine Konflikte mit dem genehmigten Bestand

Eigenständige Volltextsuche über den gesamten Bestand nach Hierarchie-,
Rang- und Konfliktregeln:

| Artefakt | Befund dieses Reviews |
|---|---|
| Architecture Book v2.0 (FROZEN) | Keine Hierarchie- oder Konfliktregel |
| Milestone 1.0 Charter | Keine |
| Engineering Specification 1.0 | §2.2 „Referenzhierarchie" — **vorhanden, aber nicht konkurrierend**, siehe Feststellung unten |
| Implementation Plan 1.0 | Konfliktregel ausschließlich über die Planungsprinzipien PP-01 bis PP-07; keine Dokumenthierarchie — bestätigt |
| Bootstrap Baseline 1.0 | Keine |
| ADR-005, ADR-006, ADR-007, ADR-011 | Keine |
| RDR-001 | Keine |
| WAIVER-DEV-001 | §4.4 referenziert DS §3.3 und den ES-Rangkonflikt (F-003) — derivativ, keine eigene Ordnung |
| WAIVER-AMENDMENT-001, GDR-001 | Keine |
| Development Standard v1.1 | §3.3 — aufgelöst, siehe 1.1 |

**Feststellung ohne Findingcharakter — ES §2.2.** Die Engineering
Specification 1.0 führt in §2.2 eine Referenzhierarchie. Diese ist (a)
ausdrücklich „gemäß Development Standard v1.1 §3.3" gebildet, also derivativ,
(b) in ihrer relativen Ordnung deckungsgleich mit §3.3 und damit mit der
Rangordnung in R2, (c) um die milestone-bindenden Artefakte Bootstrap
Baseline und Charter ergänzt, deren Einordnung durch WAIVER-DEV-001 (F-003)
gedeckt ist, und (d) als APPROVED-Artefakt durch Governance Rule 1 geschützt.
Sie trifft keine Aussage über die Core Principles. **Eine Regelkonkurrenz
besteht nicht.** Verification Summary R2 §2.3 führt die ES mit „Keine
[konkurrierende Regel]" — das ist im Ergebnis zutreffend; die Existenz der
derivativen Referenzhierarchie wäre der Vollständigkeit halber offenzulegen
gewesen, wie es für die Konfliktregel des Implementation Plan geschehen ist.
Da dieser Review den Sachverhalt eigenständig geprüft und als konkurrenzfrei
festgestellt hat, ändert dies kein Ergebnis und begründet kein Finding.

Ferner bestätigt: Kein Konflikt der R2-Änderungen mit Charter-Scope,
ES-Vertragsinhalt, Implementation Plan, genehmigten ADRs oder aktiven
Waivern. Die Waiver-Fundstellen sind unberührt.

**Prüfschwerpunkt 5: bestanden.**

---

## 6. Prüfschwerpunkt 6 — Technikfreiheit

Gezielte Prüfung aller in R2 geänderten oder ergänzten Textstellen
(Rangordnung, drei neue Absätze in Kapitel 0, Begriffsbestimmung,
Normsprache, Kapitel-6-Vorspann, 6.2-Absatz, Revisionshistorie): keine APIs,
keine Module, keine Verfahren, keine Mechanismen, keine Schwellwerte, keine
Metriken. Die Rangordnung ordnet Dokumentklassen, keine Systembestandteile.
Der 6.2-Absatz benennt kein Bestätigungsverfahren und kein Mittel. Die
Grenzfälle 4.8, 5.4, 7.2 sind unverändert und durch den akzeptierten Waiver
W1-L-03 gedeckt.

**Prüfschwerpunkt 6: bestanden.**

---

## 7. Prüfschwerpunkt 7 — Philosophische Konsistenz

Durch Abgleich bestätigt:

| Bestand | Zustand in R2 |
|---|---|
| Kapitel 12, Artikel 1–11 | Wortgleich seit R0 |
| Kapitel 4, Wertetexte 4.1–4.13 | Wortgleich seit R0 |
| Kapitel 5, Prinzipientexte 5.1–5.10 | Wortgleich seit R0 |
| Prioritätsregel (Human First → Security First) | Unverändert |
| Trust Model, fünf Ebenen | Unverändert in Anzahl und Bezeichnung |
| Human Authority | Unverändert; durch den 6.2-Absatz zusätzlich abgesichert, nicht verschoben |
| Schlussbestimmung | Wortgleich seit R0 |

Keine R2-Änderung verschiebt eine Wertung, ein Schutzniveau oder eine
Zuständigkeit zulasten der in R0 festgelegten Grundhaltung.

**Prüfschwerpunkt 7: bestanden.**

---

## 8. Prüfschwerpunkte 8–10 — Scope, Implementierungsfreiheit, Dokumentklasse

| Prüfung | Ergebnis |
|---|---|
| Neue Domäne, neues Prinzip, neue Pflicht ohne Findingbezug | Keine — Kapitel 4, 5, 12 in Anzahl und Wortlaut unverändert; die einzige Drittpflicht (Konformitätsnachweis) wurde eingeschränkt, nicht erweitert |
| Neues Verfahren | Keines — durchgehend an den Development Standard verwiesen |
| Implementierungsinhalte | Keine |
| Dokumentklasse | Unverändert: „Grundsatzdokumentation (Verfassung)"; negative Klassenbestimmung (7 Ausschlüsse) unverändert; Kapitelfolge 0–12 unverändert; Anhang A deklaratorisch |
| Änderungen ohne Finding-Bezug | Keine — jede R2-Änderung ist genau einem W-3-Finding zugeordnet (Correction Report R2 §2, gegen den Wortlaut verifiziert) |

**Prüfschwerpunkte 8–10: bestanden.**

---

## 9. Prüfschwerpunkt 11 — Genehmigungsreife

| Kriterium | Ergebnis |
|---|---|
| Alle W-1- und W-3-Findings geschlossen oder mit akzeptiertem Waiver | Ja |
| Keine offenen Findings | Ja — 0 offen |
| Keine neuen Findings | Ja |
| Regelkonkurrenz zum Bestand | Keine — eigenständig verifiziert |
| Dokumentintern widerspruchsfrei und begrifflich bestimmt | Ja |
| Status DRAFT, keine Statusvorwegnahme | Ja |
| Revisions- und Nachweiskette lückenlos | Ja — R0 → W-1 → R1 → W-3 → R2 → W-4, jede Stufe belegt |

---

# TEIL 2 — Findings Summary

| Kritikalität | Anzahl |
|---|---|
| Critical | **0** |
| High | **0** |
| Medium | **0** |
| Low | **0** |
| Editorial | **0** |

**Es bestehen keine Findings.**

Zwei Feststellungen ohne Findingcharakter, festgehalten für künftige Zyklen:

1. **ES §2.2 Referenzhierarchie** (siehe Abschnitt 5): derivativ,
   konkurrenzfrei, durch Rule 1 geschützt; bei künftigen
   Bestandsprüfungen ausdrücklich mitzuführen.
2. **Taxonomiebindung der Rangordnung** (bereits in W-3, Prüfziel 13, und
   Verification Summary R2 §2.4 offengelegt): Die Rangordnung bindet das
   Dokument an die gegenwärtige Dokumenttaxonomie. Bei einer künftigen
   Änderung der Taxonomie ist ein Amendment nach Governance Rule 3
   erforderlich. Unvermeidbare Folge der W-1/W-3-Auflagen; kein Finding.

Die aktiven Waiver W1-L-03 und W1-L-05 (durch W-3 akzeptiert) gelten fort
und stehen der Genehmigung nicht entgegen.

---

# TEIL 3 — Review Decision

> ## APPROVED

**Begründung.** Alle neun Findings des Independent Governance Review W-3 sind
nachweislich und fundstellengenau geschlossen; alle 22 Findings des
Governance Review W-1 bleiben geschlossen. Die zentrale Auflage — Auflösung
der Regelkonkurrenz zu Development Standard v1.1 §3.3 — ist erfüllt: Die
Rangordnung übernimmt §3.3 als echte Teilfolge, verortet den Development
Standard, regelt die Maßgeblichkeit und lässt den genehmigten Bestand
unberührt. Dieser Review hat den Abgleich gegen den vollständigen genehmigten
Bestand eigenständig wiederholt und keine verbleibende oder neue
Regelkonkurrenz gefunden. Die R2-Änderungen erzeugen keine neuen Findings,
keine Governance-Regression, keine Scope-Erweiterung und keine
Klassenverletzung. Die Grundphilosophie — Kapitel 4, 5 und 12 — ist seit R0
wortgleich erhalten.

**Die Entscheidung bedeutet nicht**, dass das Dokument in Kraft ist: Es
bleibt DRAFT ohne Bindungswirkung (Geltungsvorbehalt), bis die
Genehmigungsinstanz die Erstgenehmigung ausspricht.

---

# TEIL 4 — Approval Readiness Assessment

## 4.1 Readiness Level

| Stufe | Kriterium | Erreicht |
|---|---|---|
| RL-0 | Entwurf vorhanden | Ja (R0) |
| RL-1 | Vollständig gegenüber Erstellungsauftrag | Ja (R0) |
| RL-2 | Dokumentintern widerspruchsfrei und begrifflich bestimmt | **Ja** (R2) |
| RL-3 | Widerspruchsfrei gegen den genehmigten Bestand | **Ja** (R2, durch diesen Review verifiziert) |
| RL-4 | Unabhängig geprüft | **Ja** (dieser Review; formale Würdigung durch die Genehmigungsinstanz im Approval Record, W-3 B-7) |
| RL-5 | Genehmigt | Nein — nächster Schritt |

**Erreichter Reifegrad: RL-4. Das Dokument ist genehmigungsreif.**

## 4.2 Reifegradbewertung

| Dimension | Bewertung |
|---|---|
| Dokumentklasse | Reif |
| Grundphilosophie | Reif |
| Begriffliche Bestimmtheit | Reif — alle sechs tragenden Begriffe bestimmt, „Tragweite" zurückgeführt |
| Innere Widerspruchsfreiheit | Reif — W3-M-02 aufgelöst |
| Hierarchische Verortung | Reif — W3-H-01 aufgelöst und verifiziert |
| Externe Konsistenz | Reif — vollständiger Bestandsabgleich in R2 und erneut in W-4 |
| Änderungsschutz | Reif — Erstgenehmigung geregelt, erhöhte Hürde für Kapitel 0 und 12 wirksam |
| Auditierbarkeit, Bestandsschutz, Technikfreiheit | Reif |
| Zukunftssicherheit | Reif mit dokumentierter Taxonomiebindung (Feststellung 2) |

## 4.3 Nächster autorisierter Schritt

| Schritt | Gegenstand |
|---|---|
| **W-5** | **Approval Decision** durch die Genehmigungsinstanz (Projekteigner JOCHEN X) |
| W-6 | Approval Record; darin zu dokumentieren: Unabhängigkeitswürdigung nach W-3 B-7, Fortgeltung der Waiver W1-L-03 und W1-L-05, Statusübergang DRAFT → APPROVED |
| W-7 | Governance Closing |

**Hinweis zum normativen Vakuum** (fortgeschrieben aus W-1 und W-3): Solange
das Dokument DRAFT ist, existiert für neu beginnende Architekturarbeit kein
normativer Rahmen. Mit der Genehmigungsreife entfällt der Grund, die
DRAFT-Phase zu verlängern.

---

**Ende Core Principles 1.0 — Independent Governance Review (W-4)**
