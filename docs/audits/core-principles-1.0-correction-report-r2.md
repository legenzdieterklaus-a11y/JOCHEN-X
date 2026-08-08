# Core Principles 1.0 — Correction Report R2 (W-4)

| Eigenschaft | Wert |
|---|---|
| **Dokumenttyp** | Correction Report — Correction Cycle R2 |
| **Gegenstand** | [JOCHEN X – Core Principles 1.0](../core-principles-1.0.md), Revision R1 → **R2** |
| **Datum** | 2026-08-07 |
| **Rolle** | Chief Governance Architect / Principal Governance Engineer |
| **Änderungsgrundlage** | [Independent Governance Review W-3](core-principles-1.0-independent-review-w3.md) — allein verbindlich |
| **Status** | **COMPLETED** |
| **Ergebnis** | 1 High CLOSED · 3 Medium CLOSED · 4 Low CLOSED · 1 Editorial CLOSED · 0 Waiver · 0 offen |
| **Dokumentstatus nach R2** | DRAFT (unverändert) |

---

## 1. Grundlage und Abgrenzung

Einzige Änderungsgrundlage sind die neun Findings des Independent Governance
Review W-3. Jede Änderung ist in Abschnitt 3 genau einem Finding zugeordnet.

**Autorisierte Eingaben, die zur Prüfung herangezogen wurden:**

| Quelle | Verwendung |
|---|---|
| Core Principles 1.0 R1 | Ausgangsfassung |
| Independent Review W-3 | Findinggrundlage |
| Correction Report R1, Verification Summary R1, Revision History Update R1 | Nachvollzug des Vorzyklus |
| **Development Standard v1.1 §3.2, §3.3, Anhang E** | Auflösung von W3-H-01 und W3-M-03 |
| **Architecture Book v2.0** | Prüfung auf konkurrierende Hierarchieregel — **Ergebnis: keine vorhanden** |
| Milestone 1.0 Charter, Engineering Specification 1.0, Implementation Plan 1.0, Bootstrap Baseline 1.0, ADR-005/006/007/011, RDR-001, Waiver, GDR-001 | Prüfung auf konkurrierende Hierarchieregel — **Ergebnis: keine vorhanden** |

**Ausdrücklich nicht vorgenommen:**

| Ausschluss | Einhaltung |
|---|---|
| Neufassung | Nein — punktuelle Präzisierungen |
| Neue Prinzipien | Keine |
| Neue Kapitel | Keine — Kapitelfolge 0–12 unverändert |
| Neue Philosophie | Keine |
| Scope-Erweiterung | Keine |
| Designentscheidungen | Keine |
| Implementierungsdetails | Keine |
| Änderung an Kapitel 1–12 (inhaltlich) | Keine — siehe Abschnitt 4 |
| Änderung an einem genehmigten Fremddokument | Keine — Development Standard v1.1 wurde nicht angefasst |

---

## 2. Änderungsübersicht

| Finding | Kritikalität | Ergebnis | Fundstelle in R2 |
|---|---|---|---|
| W3-H-01 | High | **CLOSED** | Kapitel 0 — Rangordnung (12 Ränge), Absatz „Verhältnis zum Development Standard", Absatz „Verhältnis zu Governance Rule 1" |
| W3-M-01 | Medium | **CLOSED** | Kapitel 0 — Begriffsbestimmungen, Eintrag „Tragweite" |
| W3-M-02 | Medium | **CLOSED** | 6.2 — Absatz „Verhältnis zur menschlichen Freigabe"; Präzisierung der Ebenen „Benutzer" und „Verifizierter Benutzer" |
| W3-M-03 | Medium | **CLOSED** | Governance Rule 2 — Absatz „Konformitätsnachweis" |
| W3-L-01 | Low | **CLOSED** | Kapitel 6, Vorspann |
| W3-L-02 | Low | **CLOSED** | Dokumentcharakter — Geltungsvorbehalt; Governance Rule 3 — Absatz „Anwendungsbereich" |
| W3-L-03 | Low | **CLOSED** | Governance Rule 3 — Absatz „Erhöhte Anforderung" |
| W3-L-04 | Low | **CLOSED** | Kapitel 0 — Normsprache |
| W3-E-01 | Editorial | **CLOSED** | Revisionshistorie, Zeilen R0 und R1 |

---

## 3. Korrekturen im Einzelnen

### 3.1 W3-H-01 — Dokumenthierarchie vollständig gegen Development Standard v1.1 aufgelöst

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | Development Standard v1.1 §3.3 (APPROVED) enthält eine Konfliktregel über neun Dokumenttypen und stellt das Architecture Book an die Spitze. Core Principles R1 führte eine zweite Rangordnung mit abweichender Spitze und verortete den Development Standard nicht. Beide Regeln standen nach Governance Rule 1 gleichzeitig in Kraft. |

**Analyse vor der Korrektur.**

Der Abgleich der beiden Ordnungen ergab, dass die relative Reihenfolge der
gemeinsam geführten Klassen identisch ist. Der Widerspruch bestand nicht in der
Reihenfolge, sondern in drei Punkten: fehlende Verortung des Development
Standard, fehlende Aufnahme von fünf weiteren §3.3-Klassen und die ungeklärte
Frage, ob §3.3 oder die Rangordnung der Core Principles maßgeblich ist.

Geprüfte Auflösungsmöglichkeiten:

| Option | Bewertung |
|---|---|
| Änderung des Development Standard v1.1 | **Verworfen.** Verstoß gegen Governance Rule 1 und gegen den Auftrag; ein APPROVED-Artefakt darf in diesem Zyklus nicht geändert werden. |
| Streichung der Rangordnung aus den Core Principles | **Verworfen.** Governance-Regression; W1-H-01 würde wieder offen. |
| Verweis auf §3.3 ohne eigene Ordnung | **Verworfen.** §3.3 führt Core Principles, Implementation Plans und Implementation nicht; die vom W-1 Review geforderte Kette wäre unvollständig. |
| **Vollständige Übernahme der §3.3-Reihenfolge, ergänzt um die dort nicht geführten Klassen** | **Gewählt.** Erzeugt eine einzige Ordnung, ohne eine Reihenfolge des Development Standard zu verändern. |

**Änderung 1 — Rangordnung.** Die Tabelle wurde von sechs auf zwölf Ränge
erweitert und um eine Spalte „Quelle" ergänzt, die für jeden Rang ausweist, ob
er aus Development Standard v1.1 §3.3 stammt oder von diesem Dokument ergänzt
wird.

| Rang | Klasse | Herkunft | Rang in DS §3.3 |
|---|---|---|---|
| 1 | Core Principles | ergänzt | — |
| 2 | Architecture Book | DS §3.3 | 1 |
| 3 | ADRs | DS §3.3 | 2 |
| 4 | Development Standard | DS §3.3 | 3 |
| 5 | Engineering Specification | DS §3.3 | 4 |
| 6 | Implementation Plans | ergänzt | — |
| 7 | Review Reports | DS §3.3 | 5 |
| 8 | Final Verification Reports | DS §3.3 | 6 |
| 9 | Correction Reports | DS §3.3 | 7 |
| 10 | Templates | DS §3.3 | 8 |
| 11 | Prompts | DS §3.3 | 9 |
| 12 | Implementation | ergänzt | — |

**Nachweis der Ordnungstreue.** Die Ränge der aus §3.3 übernommenen Klassen
sind streng monoton: 2 < 3 < 4 < 5 < 7 < 8 < 9 < 10 < 11 entspricht
1 < 2 < 3 < 4 < 5 < 6 < 7 < 8 < 9. **Keine Klasse des Development Standard hat
ihre relative Stellung zu einer anderen Klasse des Development Standard
verändert.** Die drei ergänzten Klassen sind ausschließlich eingefügt, nicht
umgestellt.

**Änderung 2 — Absatz „Verhältnis zum Development Standard".** Neu eingefügt.
Er bestimmt: §3.3 bleibt unverändert gültig; die Rangordnung übernimmt deren
relative Reihenfolge vollständig und ergänzt ausschließlich die dort nicht
geführten Klassen; §3.3 trifft keine Aussage über die Core Principles, deren
Einordnung über dem Architecture Book die Konfliktregel ergänzt und ihr nicht
widerspricht; es besteht eine einzige Rangordnung; für die in §3.3 geführten
Dokumenttypen gilt §3.3 unverändert fort.

**Änderung 3 — Absatz „Verhältnis zu Governance Rule 1".** Um den Halbsatz
„Development Standard v1.1 bleibt in seiner genehmigten Fassung unberührt"
ergänzt, parallel zur bereits vorhandenen Aussage zum Architecture Book v2.0.

| Prüfung | Ergebnis |
|---|---|
| Nur noch eine eindeutig interpretierbare Hierarchie | Erfüllt — eine Tabelle, eine Konfliktregel, ausdrückliche Vereinbarkeitserklärung |
| Keine Regelkonkurrenz | Erfüllt — §3.3 ist echte Teilfolge der Rangordnung; keine Aussage steht gegen eine andere |
| Development Standard eindeutig eingeordnet | Erfüllt — Rang 4, identisch mit seiner Stellung in §3.3 |
| Architecture Book, ADRs, Engineering Specification, Implementation Plans widerspruchsfrei eingebunden | Erfüllt — Ränge 2, 3, 5, 6 |
| Governance Rule 1 gewahrt | Erfüllt — kein genehmigtes Artefakt geändert, keine Rückwirkung |
| **Status** | **CLOSED** |

**Ergänzende Feststellung ohne Änderungsfolge.** Development Standard v1.1
Anhang E enthält ein *Document Hierarchy Diagram*, das Templates als
Geschwister der Engineering Specification darstellt, während §3.3 sie auf Rang 8
führt. Dies ist eine dokumentinterne Frage des Development Standard.
Normativ ist §3.3 („Bei Widersprüchen zwischen Dokumenten gilt die folgende
Hierarchie"); die Rangordnung in R2 knüpft ausdrücklich an §3.3 an. Der
Sachverhalt wird hier festgehalten, aber weder aufgelöst noch bewertet — er
liegt außerhalb des Prüfgegenstands.

---

### 3.2 W3-M-01 — Begriff „Tragweite" auf die Wirkungsskala zurückgeführt

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | „Tragweite" skalierte an vier Stellen (5.5, 6.3, 7.8, 8.4) Pflichten, ohne bestimmt zu sein und ohne ausgewiesenes Verhältnis zur Wirkungsskala. |
| **Gewählte Auflösung** | Rückführung statt Ersetzung. Eine Ersetzung des Wortes in 5.5, 6.3, 7.8 und 8.4 hätte in vier unveränderliche Kapitel eingegriffen; der Auftrag lässt nur die zur Schließung notwendigen Präzisierungen zu. |
| **Änderung** | In den Begriffsbestimmungen ergänzt: „**Tragweite** — Gleichbedeutend mit der Wirkungsstufe einer Handlung oder Entscheidung. Der Begriff bezeichnet keinen eigenständigen Maßstab. Wo dieses Dokument eine Pflicht nach der Tragweite bemisst, bemisst es sie nach der Wirkungsstufe. Ein zweites Maßsystem besteht nicht." |
| **Wirkung auf die vier Fundstellen** | 5.5 (Erklärungsaufwand), 6.3 (Nachweisaufwand), 7.8 (Darstellung gegenüber dem Benutzer) und 8.4 (Grenze zulässiger Undurchsichtigkeit) skalieren nun nachweislich über die dreistufige Wirkungsskala. Kein Kapiteltext wurde geändert. |
| **Prüfung „keine parallelen Begriffssysteme"** | Erfüllt — die Gleichsetzung ist ausdrücklich, das Bestehen eines zweiten Maßsystems ausdrücklich verneint. |
| **Status** | **CLOSED** |

---

### 3.3 W3-M-02 — Verhältnis von Vertrauensstufe, Bestätigung und Autonomie eindeutig

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | 6.1 erstreckt das Modell auf nicht-menschliche Akteure; 6.2 bestimmte, der Vertrauensnachweis „trägt" Handlungen mit erheblicher Wirkung. Gegenüber 5.10 (menschliche Bestätigung) und 8.5 (Autonomiegrenze) waren zwei Lesarten begründbar. |
| **Änderung 1** | Ebene „Benutzer": „Sein Vertrauensnachweis trägt Handlungen bis zur Stufe ‚bedeutsam'" → „Sein **Nachweis genügt für** Handlungen bis zur Stufe ‚bedeutsam'". |
| **Änderung 2** | Ebene „Verifizierter Benutzer": „Sein Vertrauensnachweis trägt Handlungen mit erheblicher Wirkung" → „Sein **Nachweis genügt als Identitätsgrundlage für** Handlungen mit erheblicher Wirkung". Damit ist der Aussagegehalt eindeutig auf die Identitätsfrage begrenzt. |
| **Änderung 3** | Neuer Absatz am Ende von 6.2, „**Verhältnis zur menschlichen Freigabe**": Eine Vertrauensebene bestimmt allein den erbrachten Nachweisgrad. Sie ersetzt niemals eine nach 5.10 erforderliche menschliche Bestätigung und verschiebt niemals die Autonomiegrenze nach 8.5. Für nicht-menschliche Akteure gilt zusätzlich: Ihre Vertrauensebene begründet keine eigenständige Handlungsbefugnis; Handlungen mit erheblicher oder kritischer Wirkung setzen unabhängig von der erreichten Ebene eine menschliche Bestätigung voraus. Menschliche Autorität ist durch keine Vertrauensebene ersetzbar (Artikel 1). |
| **Prüfung gegen die Vorgabe** | „Es darf niemals der Eindruck entstehen, dass eine Vertrauensstufe die menschliche Freigabe ersetzt" — ausdrücklich und wörtlich ausgeschlossen. „Human Authority bleibt absolut" — durch den Schlusssatz mit Verweis auf Artikel 1 gesichert. |
| **Kein neues Prinzip** | Der Absatz stellt ausschließlich das Verhältnis bereits bestehender Bestimmungen (5.10, 8.5, Artikel 1) klar. 5.10, 8.5 und Artikel 1 sind im Wortlaut unverändert. |
| **Status** | **CLOSED** |

---

### 3.4 W3-M-03 — Zuständigkeit für den Konformitätsnachweis geklärt

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | Rule 2 verpflichtete jedes gebundene Dokument, seine Vereinbarkeit „ausdrücklich" auszuweisen. Das ist eine Anforderung an Struktur und Pflichtinhalt anderer Dokumente. Development Standard v1.1 §3.2 weist die Zuständigkeit für Prozess, Governance, Templates und Review-Regeln dem Development Standard zu und untersagt anderen Dokumentklassen, Prozesse zu definieren. |
| **Änderung** | Der Absatz „Konformitätsnachweis" wurde um die Zuständigkeitsabgrenzung ergänzt: Die Bestimmung begründet allein die **inhaltliche Pflicht zur Vereinbarkeit**; **Form, Ort und Verfahren** des Nachweises richten sich ausschließlich nach dem Development Standard; die Core Principles treffen dazu keine Regelung und setzen kein Verfahren; eine doppelte Zuständigkeit besteht nicht. Das Wort „ausdrücklich" wurde gestrichen, da es eine Formvorgabe enthielt. |
| **Begründung** | Die Trennung folgt der in DS §3.2 angelegten Aufteilung: materielle Norm bei der ranghöheren Dokumentklasse, Verfahren und Form beim Development Standard. W1-M-11 bleibt geschlossen, da die Nachweispflicht dem Grunde nach erhalten bleibt. |
| **Prüfung „keine Prozessüberschneidung"** | Erfüllt — die Core Principles setzen kein Verfahren mehr. |
| **Prüfung „keine doppelte Zuständigkeit"** | Erfüllt — ausdrücklich verneint. |
| **Status** | **CLOSED** |

---

### 3.5 Low Findings

#### W3-L-01 — Selbstbeschreibung Kapitel 6 präzisiert

Der Vorspann lautete „keine Rollenmatrix, keine Rechtezuordnung, keine
Umsetzung". Er lautet nun „keine Rollenmatrix, keine Zuordnung konkreter
Rechte, Daten oder Ressourcen, keine Umsetzung". Damit deckt sich die
Selbstbeschreibung mit dem Kapitelinhalt: Kapitel 6 ordnet keine konkreten
Rechte zu, wohl aber Nachweisgrade. Keine strukturelle Änderung.
**CLOSED**

#### W3-L-02 — Erstgenehmigung geregelt

Zwei Präzisierungen. Erstens im Geltungsvorbehalt: „Die Bindungswirkung tritt
mit der **Erstgenehmigung durch die Genehmigungsinstanz** ein; Governance Rule 3
regelt ausschließlich spätere Änderungen." Zweitens in Rule 3 der neue Absatz
„**Anwendungsbereich**": Die Regel gilt für Änderungen eines bereits genehmigten
Dokuments; die Erstgenehmigung richtet sich nach dem im Development Standard
geregelten Genehmigungsverfahren und wird von der Genehmigungsinstanz
ausgesprochen. Der Zirkelbezug ist damit aufgelöst; zugleich bleibt die
Verfahrenszuständigkeit beim Development Standard (konsistent mit W3-M-03).
**CLOSED**

#### W3-L-03 — Erhöhte Anforderung wirkt nun als Genehmigungshürde

Der Absatz „Erhöhte Anforderung" wurde um den Satz ergänzt, dass der ohnehin
erforderliche Governance Review bei Änderungen an Kapitel 0 und Kapitel 12 ein
**unabhängiger** Review sein muss, durchgeführt von einer an der Änderung
unbeteiligten Instanz; Form und Durchführung richten sich nach dem Development
Standard. Damit wirkt die erhöhte Anforderung nicht mehr nur dokumentarisch.
Es wird kein neuer Mechanismus geschaffen: Die Präzisierung qualifiziert eine
bereits bestehende Anforderung und verweist für die Durchführung auf den
Development Standard. **CLOSED**

#### W3-L-04 — Normsprache um indikativische Bestimmungen ergänzt

Ergänzt: „Bestimmungen, die ohne Modalverb im Indikativ formuliert sind, sind
unbedingt verbindlich; die indikativische Form beschreibt den geforderten
Zustand und schwächt die Verbindlichkeit nicht ab." Damit ist für den gesamten
Dokumenttext ein Verbindlichkeitsgrad bestimmt. Kein Kapiteltext wurde
umformuliert. **CLOSED**

---

### 3.6 Editorial Finding

#### W3-E-01 — Revisionshistorie vervollständigt

Zeile R0, Spalte „Prüfartefakt": „—" → „Governance Review W-1". Zeile R1,
Spalte „Prüfartefakt" um „Independent Review W-3" ergänzt. Zeile R2
hinzugefügt. Die Historie erfüllt damit ihre eigene Vorgabe, jede Revision mit
Auslöser, Umfang und Prüfartefakt zu führen. **CLOSED**

---

## 4. Änderungen ohne Finding-Bezug

**Keine.**

| Bereich | Zustand nach R2 |
|---|---|
| Kapitel 1 Purpose | Unverändert seit R0 |
| Kapitel 2 Mission | Unverändert seit R0 |
| Kapitel 3 Vision | Unverändert seit R1 |
| Kapitel 4 Core Values (13 Werte) | Unverändert seit R1; Wertetexte unverändert seit R0 |
| Kapitel 5 Fundamental Principles (10 Prinzipien) | **Unverändert seit R0** |
| Kapitel 6 Trust Model | Vorspann (W3-L-01), 6.2 (W3-M-02); 6.1 und 6.3 unverändert |
| Kapitel 7 Security Philosophy | **Unverändert seit R1** |
| Kapitel 8 AI Philosophy | **Unverändert seit R0** |
| Kapitel 9 Trading Philosophy | **Unverändert seit R1** |
| Kapitel 10 Infrastructure Philosophy | **Unverändert seit R0** |
| Kapitel 11 Evolution Principles | **Unverändert seit R1** |
| Kapitel 12 Non-Negotiable Principles | **Unverändert seit R0 — alle 11 Artikel wortgleich** |
| Schlussbestimmung | **Unverändert seit R0** |
| Anhang A | Unverändert seit R1 |

Sämtliche Änderungen in R2 betreffen ausschließlich Kapitel 0, den
Dokumentkopf, den Vorspann von Kapitel 6, Abschnitt 6.2 und die
Revisionshistorie.

---

## 5. Ergebnis

| Kritikalität | Anzahl | CLOSED | WAIVER | OFFEN |
|---|---|---|---|---|
| Critical | 0 | 0 | 0 | 0 |
| High | 1 | 1 | 0 | **0** |
| Medium | 3 | 3 | 0 | **0** |
| Low | 4 | 4 | 0 | **0** |
| Editorial | 1 | 1 | 0 | **0** |
| **Summe** | **9** | **9** | **0** | **0** |

Sämtliche Findings des Independent Governance Review W-3 sind geschlossen.
Es wurde kein Waiver in Anspruch genommen. Der Dokumentstatus bleibt **DRAFT**.

---

**Ende Correction Report R2**
