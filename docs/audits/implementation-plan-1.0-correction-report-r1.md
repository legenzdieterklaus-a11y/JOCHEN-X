# Implementation Plan 1.0 — Correction Report R1

| Eigenschaft | Wert |
|---|---|
| **Dokumenttyp** | Finding Closure Report — Workflow-Schritt W-2 → Korrekturzyklus |
| **Korrekturzyklus** | R1 |
| **Datum** | 2026-08-05 |
| **Grundlage** | [Global Consistency Audit (W-2)](implementation-plan-1.0-global-consistency-audit.md) |
| **Korrigiertes Dokument** | [Milestone 1.0 Implementation Plan](../milestone-1.0-implementation-plan.md), Revision R0 → **R1** |
| **Erstellte Artefakte** | [GDR-001](../governance/gdr-001-waiver-closing-criteria.md) |
| **Umfang** | 21 Findings: 2 High, 8 Medium, 7 Low, 4 Editorial |
| **Ergebnis** | 20 Findings geschlossen, 1 Finding (H-01) auftragsgemäß ohne Textkorrektur an die Governance übergeben |

---

## 1. Bearbeitungsgrundsätze

| # | Grundsatz | Einhaltung |
|---|---|---|
| 1 | Keine neuen Functional Requirements | Eingehalten — FR-001..FR-014 unverändert |
| 2 | Keine neuen Acceptance Criteria | Eingehalten — 29 AC unverändert |
| 3 | Keine neuen Quality Gates | Eingehalten — QG-001..QG-008 unverändert |
| 4 | Keine Änderung an Charter, Engineering Specification, Architecture Book, Bootstrap Baseline | Eingehalten — kein Zugriff auf diese Dokumente |
| 5 | Keine Architekturänderungen | Eingehalten |
| 6 | Jede Korrektur exakt einem Finding zugeordnet | Eingehalten — siehe Abschnitt 3 |
| 7 | Keine Textkorrektur zu H-01 | Eingehalten — siehe Abschnitt 2 |

**Zusätzlich eingehalten, ohne ausdrückliche Vorgabe:** keine neuen
Deliverables, keine neuen Evidence-Einträge, keine neuen Work Packages, keine
neue Traceability-Ebene, keine neue Governance-Instanz, keine neuen
Registereinträge. Die Anzahl der Evidence-Einträge bleibt bei 20, die der
Registereinträge bei 16, die der Completion Conditions je Kapitel unverändert.

---

## 2. H-01 — auftragsgemäß nicht korrigiert

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | H-01 — Verengte Wiedergabe der Waiver Closing Criteria ohne deklarierte Abweichung. WAIVER-DEV-001 §9 (1) fordert Dateireferenzen „Datei, **Zeile**, Status", §9 (2) „dateibasierte Änderungsbeschreibungen und **Codebeispiele**"; über §3.1 ist zusätzlich Development Standard v1.1 §6.2 #4/#5 inkorporiert. Kapitel 5.5.1 gibt beide Kriterien verkürzt wieder; Kapitel 5.8 und ST-10 schließen Codebeispiele aus. |
| **Durchgeführte Änderung am Plan** | **Keine inhaltliche Korrektur.** Der Wortlaut der Kriterienzitate in 5.5.1, der Ausschluss in 5.8 und ST-10 sowie die Formulierungen in CC-08, AP-02 und 8.9 (#5) bleiben **unverändert**. |
| **Stattdessen erstellt** | **GDR-001 — Governance Decision Record** (`docs/governance/gdr-001-waiver-closing-criteria.md`) mit vollständigem Sachverhalt, Wortlautgegenüberstellung, tatsächlichem Erfüllungsstand je Teilkriterium und **vier** einander ausschließenden Entscheidungsoptionen (A Auslegungsentscheidung, B Waiver Amendment, C Erfüllung des Wortlauts, D Verschiebung in die Sprint Planning Phase), jeweils mit Wirkung, Aufwand, Vereinbarkeit mit Charter §8 und ACN-09, Risiko und Folgeartefakten. |
| **Begründung** | Der Sachverhalt ist ein Konflikt zwischen zwei genehmigten Governance-Artefakten. Kapitel 1.5, PP-04 und ACN-09 des Plans verlangen bei einem solchen Konflikt Eskalation, nicht Auflösung durch den Plan. Eine Textkorrektur wäre entweder eine Absenkung der Waiver-Bedingung oder eine Überschreitung der Autorisierungsgrenze aus Charter §8 und Kapitel 1.6 — beides unzulässig. |
| **Betroffene Kapitel** | Keine inhaltliche Änderung. Verweisende Ergänzungen in 5.5.1 (Absatz „Bewertungsvorbehalt"), 7.6 (Angewandtes Beispiel), 7.8 und 10.7 — sämtlich zur **Sichtbarmachung** des offenen Entscheidungsbedarfs gemäß PP-04, nicht zu seiner Auflösung. |
| **Auswirkung auf Traceability** | Keine. GDR-001 ist als externes Governance-Artefakt referenziert; es entsteht kein neuer Knoten in der Traceability-Kette. |
| **Status** | **OFFEN — der Entscheidungsinstanz vorgelegt.** Blockierend für W-6 (AB-01, AB-02), nicht blockierend für W-3. |

### Abgrenzung zur Änderung an Kapitel 5.5.1

Kapitel 5.5.1 wurde im Rahmen von **M-05** strukturell geändert (Aufnahme des
vierten Closing Criterion §9 (3), Statusspalte). Diese Änderung berührt den
Wortlaut der Zitate zu §9 (1) und §9 (2) nicht. Zur Klarstellung:

| Element in 5.5.1 | R0 | R1 | Zugeordnetes Finding |
|---|---|---|---|
| Zitat §9 (1) — „(Datei, Status)" | vorhanden | **unverändert** | H-01, nicht korrigiert |
| Zitat §9 (2) — ohne „Codebeispiele" | vorhanden | **unverändert** | H-01, nicht korrigiert |
| Zeile für §9 (3) | fehlte | ergänzt | M-05 |
| Statusspalte | fehlte | ergänzt | M-05 |
| Verweis auf GDR-001 | fehlte | ergänzt | H-01 — Sichtbarmachung, keine Auflösung |

---

## 3. Geschlossene Findings

### H-02 — QG-001 ist entgegen 7.5 und 8.7 nicht innerhalb von WP-001 abschließbar

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | 7.5 nannte als frühestmöglichen Prüfzeitpunkt von QG-001 den Abschluss WP-001 mit der Begründung „Prüft ausschließlich Acceptance Criteria aus WP-001" und führte nur QG-006/007/008 als nicht einzeln abschließbar. Der QG-Katalog der Engineering Specification weist QG-001 zusätzlich NFR-002, NFR-004 und NFR-008 zu; Anhang B.12 verortet den NFR-004-Nachweis am Ende von Phase B. 8.5 ordnete QG-001 nur EV-W01 zu. Folge: QG-001 hätte formal geschlossen werden können, bevor sein Kriterium belegt ist — entgegen der Grundregel in 8.7 und 10.10 Nr. 9. |
| **Durchgeführte Änderung** | 1. **7.4** (WP-001): Abschlusskriterium auf den AC-Anteil begrenzt; NFR-004-Anteil ausdrücklich **nicht** Abschlusskriterium des Work Package. Voraussetzung um die Baseline-Messreihe (Anhang B.2) ergänzt. 2. **7.5**: Gate-Tabelle um die Spalten „Prüft AC aus" und „Prüft NFR" erweitert; QG-001 mit geteiltem Prüfzeitpunkt („AC-Anteil: Abschluss WP-001 — abschließend: Ende Phase B"); NFR-Zuordnung für alle acht Gates aus dem ES-Katalog ergänzt. Feststellung um **QG-001** erweitert. Neuer Absatz „Klarstellung zu QG-001". 3. **8.5**: EV-W01-Abschlussbedingung um den ausdrücklichen Ausschluss des NFR-004-Anteils ergänzt; EV-I01 um den performancebezogenen Anteil erweitert; Gate-Zuordnung QG-001 → EV-W01 **+ EV-I01**. 4. **8.7**: QG-001 auf „Nicht innerhalb WP-001 abschließbar", Prüfebene VL-02 **+ VL-03**; abhängige Work Packages auf „WP-001 sowie alle Provider-Pakete", frühestmöglicher Abschluss „Ende Phase B". 5. **13.9** (ROR-002): QG-001 in Beschreibung und Gate-Zuordnung aufgenommen. 6. **13.12** (RR-04): QG-001 aufgenommen. 7. **13.11**: phasenbezogener Anteil von QG-001 als querschnittlich ausgewiesen. |
| **Begründung** | Nachführung an den bereits genehmigten Prüfumfang von QG-001. Der Quality-Gate-Katalog der Engineering Specification weist QG-001 seit jeher NFR-004 zu; Anhang B (Schließung von F9-004) machte den zugehörigen Nachweis erstmals verortbar, ohne dass 7.5 und 8.7 nachgezogen wurden. |
| **Betroffene Kapitel** | 7.4, 7.5, 8.5, 8.7, 13.9, 13.11, 13.12 |
| **Auswirkung auf Traceability** | **Additiv, ohne Änderung bestehender Zuordnungen.** Die Kante QG-001 → EV-I01 wird ergänzt; EV-I01 war bereits definiert und bereits QG-007 zugeordnet. Kein neuer Nachweis, kein neues Gate, kein neues Kriterium. Die FR-zentrierten Matrizen in 8.4, 9.5, 12.11 und 13.11 bleiben unverändert; sie wurden um Lesehinweise ergänzt, die die NFR-Anteile an 8.5 verweisen (siehe auch L-02). |
| **Status** | **CLOSED** |

---

### M-01 — Zwei einander ausschließende Definitionen des Planungsscope

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | 1.3 und 2.3 definierten den Scope beide exklusiv („ausschließlich") mit unterschiedlichem Inhalt: 1.3 mit Delta Analysis und MWB, ohne Migration und Risiken; 2.3 mit Migration und Risiken, ohne Delta Analysis und MWB. |
| **Durchgeführte Änderung** | **1.3** vollständig neu gefasst: Trennung in zwei Quellen (Planungsscope PS-01..PS-06 und Waiver-Pflichtabschnitte) mit Angabe der jeweiligen Verbindlichkeitsgrundlage; die Übersicht ist ausdrücklich als **Zusammenfassung auf Dokumentebene** gekennzeichnet und tritt nicht neben Kapitel 2.3; Vorrangregel („bei Abweichung gilt Kapitel 2.3"); ausdrückliche Zuordnung, welche Vollständigkeitsaussagen sich auf welche Quelle beziehen. **2.3** um den Vorspann ergänzt, der ihn als abschließende und normative Scope-Definition ausweist. |
| **Begründung** | Die Vereinigungsmenge ist sachlich zutreffend; unzulässig war ausschließlich die doppelte Exklusivformulierung. Die Auflösung erfolgt über eine Rangregel, nicht über Streichung von Inhalt. |
| **Betroffene Kapitel** | 1.3, 2.3 |
| **Auswirkung auf Traceability** | Keine. Es wird kein Planungsgegenstand hinzugefügt oder entfernt. AP-09, RL-00, CC-11 bis CC-13, 10.7 und AB-03 beziehen sich unverändert auf PS-01 bis PS-06. |
| **Status** | **CLOSED** |

### M-02 — GR-001 trägt zwei einander ausschließende Statuswerte

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | GR-001 wurde in Anhang A (Registertabelle, Eintrag, PR-001.6, PR-001.9), 6.5, 8.8 und 10.7 mit **OPEN**, in 11.10, 11.11, 12.10 und 13.4 mit **PENDING DECISION** geführt. 11.6 definiert beide als getrennte Zustände; 11.11 wies OPEN = 0 aus. |
| **Durchgeführte Änderung** | Einheitlich auf **PENDING DECISION** gesetzt in: Anhang A (Kopftabelle, Eintragstabelle, „Wirkung auf den Plan", PR-001.6, PR-001.9), 5.5.4 (zusätzlich Umstellung von „GB-001 offen" auf den Registerzustand von GR-001), 6.5, 7.6, 8.8 (Hinweis zu GV-08), 10.7. Neue **Registerregel 6** in 11.11: die fünf Zustandsbezeichner aus 11.6 sind ausschließlich; OPEN und PENDING DECISION sind keine Synonyme; GR-001 trägt in sämtlichen Fundstellen PENDING DECISION. 11.10 („Verortung") um die Zeile zum Wechsel des Statusbezeichners ergänzt. |
| **Begründung** | PENDING DECISION ist der zutreffende Zustand nach 11.6: Instanz und späteste notwendige Entscheidung sind benannt (PR-001.7, RCC-13). OPEN wäre der Zustand ohne zugeordnete Behandlung. |
| **Betroffene Kapitel** | 5.5.4, 6.5, 7.6, 8.8, 10.7, 11.10, 11.11, Anhang A |
| **Auswirkung auf Traceability** | Keine. Die Kette GB-001 → GR-001 → Fundstellen → QG-007/QG-008 → Evidence → PR-001 bleibt unverändert. Die blockierende Wirkung ist in beiden Lesarten identisch. |
| **Status** | **CLOSED** |

### M-03 — Das konsolidierte Register bildete seinen eigenen Gesamtstand nicht ab

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | 11.11 beanspruchte die alleinige Registerführung und den verbindlichen Gesamtstand, führte aber 10 Einträge, während Registerregel 5, 12.9, 13.9 und 13.15 den Stand mit 16 angaben. 11.12 und RCC-04..RCC-08 prüften gegen 10; 11.16 nannte 9 MITIGATED. Die sechs Einträge MGR-001..003 und ROR-001..003 fehlten im führenden Register. |
| **Durchgeführte Änderung** | 1. **11.11**: Registertabelle auf **16 Einträge** erweitert; neue Tabelle „Zusammensetzung" (5 ES + 4 Waiver + 1 Governance + 3 Migration + 3 Rollout = 16) mit Angabe der quellenseitigen Prüfbedingung je Block; Verteilung auf Kritikalität (0/6/6/4) und Status (15 MITIGATED, 1 PENDING DECISION, Summenzeile) fortgeschrieben; Registerregel 1 präzisiert („ein Eintrag, der hier nicht geführt ist, existiert für den Milestone nicht"); Registerregel 5 neu gefasst (12.9/13.9 **leiten her**, führen kein Register). 2. **11.12**: alle acht Prüfzeilen von 10 auf **16**; Vorspann zum Prüfbezug ergänzt; Abschnitt „Risiken ohne Work-Package-Bezug" um die querschnittlich geführten Einträge erweitert. 3. **11.15**: RCC-04 bis RCC-08 von 10 auf **16**; Bewertungsabsatz um die Erläuterung des Verhältnisses RCC-01..03 (quellenseitig) zu RCC-04..08 (Gesamtstand) ergänzt. 4. **11.16**: Risikolage auf „16 Einträge: 15 MITIGATED, 1 PENDING DECISION". 5. **12.9** und **13.9**: Abschnitt „Fortschreibung des konsolidierten Registers" zu „Übergabe an die Registerführung" umgestellt; eigener Registerstand entfernt, Verweis auf 11.11 als verbindlichen Gesamtstand. 6. **13.9** („Registerführung") und **13.15** entsprechend nachgeführt. 7. **MCC-14** und **ROC-14** um den ausdrücklichen Prüfbezug (10 bzw. 13 vor dem jeweiligen Kapitel bestehende Einträge) ergänzt; **ROC-08** um den Gesamtstand präzisiert. |
| **Begründung** | Registerregel 1 und die Selbstbezeichnung als verbindlicher Gesamtstand sind nur haltbar, wenn das Register vollständig ist. Die Alternative — Aufspaltung der Registerführung — wurde verworfen, weil sie RS-03 und 13.14 ohne einzelne vollständige Tabelle ließe. |
| **Betroffene Kapitel** | 11.11, 11.12, 11.15, 11.16, 12.9, 12.13, 13.9, 13.13, 13.15 |
| **Auswirkung auf Traceability** | **Keine Änderung bestehender Zuordnungen.** Sämtliche 16 Einträge behalten Kennung, Klasse, Kritikalität, Owner, Status, Quelle und Fundstelle unverändert (RC-11 eingehalten). Es wird kein Risiko hinzugefügt, entfernt oder neu bewertet; ausschließlich der Ort der Registerführung wird vereinheitlicht. |
| **Status** | **CLOSED** |

### M-04 — Widersprüchliche Risikobedingung für die Freigabereife

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | RPR-06 und RR-06 schlossen nur OPEN und PENDING DECISION aus (MITIGATED zulässig); RS-03 und 13.14 verlangten für sämtliche Einträge CLOSED oder ACCEPTED. Bei 15 von 16 Einträgen im Zustand MITIGATED ergaben beide Fassungen unterschiedliche Freigabereife. |
| **Durchgeführte Änderung** | Einheitlich auf die **strengere** Fassung: **RPR-06** neu gefasst („Ein Registereintrag, der nicht den Zustand CLOSED oder ACCEPTED trägt, schließt die Freigabe aus", mit ausdrücklicher Erstreckung auf MITIGATED unter Verweis auf RP-09). **RR-06** entsprechend. **ROO-05** von „unbehandelter Zustand" auf den Registerzustand präzisiert. **RS-03** in Gegenstand und Austrittsbedingung präzisiert (16 Einträge; kein Eintrag mehr in OPEN, MITIGATED oder PENDING DECISION). **13.8** (Anlässe) nachgeführt. |
| **Begründung** | Die strengere Fassung ist die einzige, die mit RP-09 („Keine Schließung ohne Review; das Ausbleiben des Eintritts ist kein Schließungsgrund") und mit der Lifecycle-Stufe L-6 vereinbar ist. MITIGATED bedeutet nach 11.6 ausdrücklich „Eintritt weiterhin möglich". |
| **Betroffene Kapitel** | 13.2 (ROO-05), 13.3 (RPR-06), 13.7 (RS-03), 13.8, 13.12 (RR-06) |
| **Auswirkung auf Traceability** | Keine. Die Bedingung wird verschärft, nicht verschoben; es entsteht kein neuer Knoten. |
| **Status** | **CLOSED** |

### M-05 — Closing Criterion §9 (3) fehlte in der Erfüllungstabelle

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | 5.5.1 führte drei Closing Criteria (§9 (1), (2), (4)); §9 (3) fehlte. CC-08, 8.9 (#5) und EV-D02 zählten 4 und verwiesen auf 5.5.1 als Nachweisort. |
| **Durchgeführte Änderung** | 5.5.1 um die Zeile **§9 (3)** im vollen Wortlaut ergänzt, adressiert durch W-3 / AP-07 / CC-14, Status „Ausstehend — prozessual, durch Planinhalt nicht erfüllbar". Tabelle um Nummern- und Statusspalte erweitert. |
| **Begründung** | §9 (3) ist prozessual und kann durch Planinhalt nicht erfüllt werden, ist aber Bestandteil der gezählten vier Kriterien und muss daher am Nachweisort sichtbar sein. |
| **Betroffene Kapitel** | 5.5.1 |
| **Auswirkung auf Traceability** | Keine. CC-08, 8.9 (#5), EV-D02, AP-02 und SC-09 bleiben unverändert; ihr Nachweisort trägt nun alle vier gezählten Kriterien. |
| **Status** | **CLOSED** |

### M-06 — Findings-Bilanz veraltet und unvollständig

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | AP-01, CC-10 und 10.7 stützten sich auf „Audit Kapitel 9; Anhang A" („6 geschlossen, 1 Pending Resolution") und berücksichtigten die Independent Reviews der Kapitel 10 bis 13 sowie GP-001 bis GP-005 nicht. F9-005 war einmal genannt, ohne im Dokument auflösbar zu sein. |
| **Durchgeführte Änderung** | Neuer Abschnitt **„Findings-Übersicht" in 10.7** mit einer Zeile je Prüfartefakt (Consistency Audit Kapitel 9; Independent Reviews Kapitel 10, 11, 12, 13; planweite Befunde GP-001 bis GP-005; Global Consistency Audit W-2/R1) sowie einer Bewertungstabelle (Findings ohne dokumentierten Status: 0; offener Entscheidungsbedarf: 2 — GR-001 und GDR-001; prozessbedingt offen: 1 — GP-005/CC-14). F9-005 dort ausdrücklich als Ursprungsbezeichner von GR-001 aufgelöst. **AP-01** auf die neue Übersicht als Nachweisquelle umgestellt und in der Statusaussage präzisiert. **CC-10** auf die neue Übersicht umgestellt. **10.7** (Abschnittstabelle) in den Befundspalten nachgeführt. **10.7** (Gesamtprüfung) Zeile „Findings" neu gefasst. |
| **Begründung** | RO-07 verlangt, dass die Lage zu jedem Governance-Prüfpunkt vollständig darstellbar ist. Eine auf ein einzelnes Prüfartefakt gestützte Bilanz erfüllt das nach fünf abgeschlossenen Prüfungen nicht mehr. |
| **Betroffene Kapitel** | 10.3 (AP-01), 10.7, 10.8 (CC-10) |
| **Auswirkung auf Traceability** | Keine neue Ebene. Die Übersicht aggregiert bestehende Prüfartefakte und ersetzt keines. GV-08 und EV-D05 wurden um den Verweis auf die Übersicht ergänzt. |
| **Status** | **CLOSED** |

### M-07 — Deliverable-Abdeckung behauptet, aber nicht nachgewiesen

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | 10.7 behauptete „10 Deliverables abgebildet", PO-02 „unverändert übernommen"; referenziert waren nur D-001, D-009, D-010. Es existierte keine Zuordnung und keine Abdeckungsprüfung. |
| **Durchgeführte Änderung** | Neuer Abschnitt **„Deliverable-Abdeckung" in 10.7** mit einer Zeile je Deliverable D-001 bis D-010: Typ, Zuordnung im Plan (Migrations- und Rollouteinheit, Kapitel) und Nachweis (Evidence, Quality Gate). Zeile „Vollständigkeit gegenüber der Engineering Specification" in der Gesamtprüfung um den Verweis auf die Zuordnung ergänzt und um Charter Objectives und Engineering Goals vervollständigt. |
| **Begründung** | Die Behauptung bestand bereits; sie war nur nicht belegt. Die Zuordnung führt kein neues Deliverable ein (5.6 unverändert: „Neue Deliverables 0"). |
| **Betroffene Kapitel** | 10.7 |
| **Auswirkung auf Traceability** | **Additiv und rein nachweisend.** Jedes Deliverable wird auf bereits bestehende Knoten (WP, MU, RU, Evidence, Quality Gate) abgebildet. Keine neue Ebene, keine geänderte Zuordnung. |
| **Status** | **CLOSED** |

### M-08 — Revisionshistorie nicht fortgeschrieben

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | Metadaten: Revision R0 „Initial Draft — Kapitel 1", Datum 2026-08-03, eine einzige Historienzeile — bei inzwischen 13 Kapiteln, zwei Anhängen und fünf dokumentierten Prüfzyklen. |
| **Durchgeführte Änderung** | Revisionshistorie in 1.1 neu gefasst: acht Zeilen (R0, R0.1 bis R0.6, R1) mit Datum, Änderung und **Auslöser/Prüfartefakt**. Die Zwischenstände R0.1 bis R0.6 sind ausdrücklich als **rekonstruiert** gekennzeichnet, mit Angabe des Prüfartefakts, aus dem die Rekonstruktion abgeleitet ist. Zusage der fortlaufenden Führung ab R1. Metadaten auf Revision **R1** und Datum 2026-08-05 gesetzt; Status bleibt DRAFT. |
| **Begründung** | Revisionssicherheit verlangt, dass der Entwicklungsweg aus dem Dokument selbst rekonstruierbar ist. Die Kennzeichnung als rekonstruiert ist zwingend: eine nachträgliche Historie darf nicht als zeitgleiche Aufzeichnung erscheinen. |
| **Betroffene Kapitel** | 1.1 |
| **Auswirkung auf Traceability** | Keine. |
| **Status** | **CLOSED** |

---

### L-01 — Drei Reihenfolgen der kanonischen Traceability-Kette

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | PP-01 führte „… FR → AC → QG → WP"; 8.4/9.5/10.7 „… FR → WP → AC → QG → Evidence" und bezeichneten dies als kanonische Kette. |
| **Durchgeführte Änderung** | **PP-01** auf die kanonische Reihenfolge „Charter Objective → Engineering Goal → Functional Requirement → **Work Package → Acceptance Criterion → Quality Gate**" umgestellt, mit Verweis auf Kapitel 8.4 als Ausführung und auf den dort ergänzten Nachweisknoten Evidence. |
| **Begründung** | 8.4 ist gegen die Engineering Specification geprüft und deckungsgleich; PP-01 war die abweichende Stelle. Kapitel 4.8 bleibt unverändert, da es die Delta-Ebene ausdrücklich als additiven Einschub führt. |
| **Betroffene Kapitel** | 2.2 (PP-01) |
| **Auswirkung auf Traceability** | **Keine inhaltliche.** Sämtliche Einzelzuordnungen waren bereits deckungsgleich mit der Engineering Specification; korrigiert wurde ausschließlich die Reihenfolgeangabe im Prinzipientext. |
| **Status** | **CLOSED** |

### L-02 — EV-G03 ohne beziehungsweise mit widersprüchlicher Gate-Zuordnung

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | 8.5 wies QG-008 die Nachweise EV-G01, EV-G02, EV-G04, EV-D03, EV-D05 zu; R-004 (11.8) führte „QG-008 → EV-G01, **EV-G03**". 10.7 behauptete „vollständig zugeordnet", obwohl EV-D01, EV-D02 und EV-G03 keinem Gate zugeordnet waren. |
| **Durchgeführte Änderung** | **EV-G03** in der Gate-Zuordnung zu QG-008 ergänzt, mit Anmerkungsspalte. Neuer Unterabschnitt **„Nachweise ohne Gate-Zuordnung"** in 8.5: EV-D01 und EV-D02 mit Angabe ihrer Verwendung (GV-04 / Phase A / MS-01 beziehungsweise GV-06 / AP-02) und Fundstelle; Feststellung, dass damit jeder der 20 Nachweise entweder einem Gate oder einem Governance-Bestätigungspunkt zugeordnet ist. Zeile „Evidence" in der Gesamtprüfung 10.7 auf „18 einem Quality Gate, 2 einem Governance-Bestätigungspunkt" präzisiert. |
| **Begründung** | R-004 setzte die Zuordnung bereits voraus; 8.5 war die lückenhafte Stelle. Für EV-D01 und EV-D02 ist die Nicht-Zuordnung sachlich richtig — sie wirken außerhalb der Gate-Prüfung — und wird nun ausgewiesen statt stillschweigend gelassen. |
| **Betroffene Kapitel** | 8.5, 10.7 |
| **Auswirkung auf Traceability** | **Additiv.** Die Kante QG-008 → EV-G03 wird ergänzt; sie war in R-004 bereits behauptet. Kein neuer Nachweis. |
| **Status** | **CLOSED** |

### L-03 — Zählfehler in 5.5.2

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | „51 referenzierte bestehende Artefakte" — tatsächlich 50 eindeutige Artefakte plus 2 offene Positionen. |
| **Durchgeführte Änderung** | Zahl auf **50** korrigiert; Formulierung um die Bestätigung ergänzt, dass alle 50 im Repository vorhanden sind (Regel 9). **5.6**: Prüfzeile „Als bestehend geführte Dateien gegen Repository-Stand geprüft" von „alle | alle" auf **50 | 50** präzisiert. |
| **Begründung** | Programmatisch verifiziert: 50 eindeutige Dateipfade in der Tabelle, sämtlich im Repository vorhanden. |
| **Betroffene Kapitel** | 5.5.2, 5.6 |
| **Auswirkung auf Traceability** | Keine. |
| **Status** | **CLOSED** |

### L-04 — Nicht nachgeführte generische Vorwärtsverweise

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | Acht generische Verweise („nachfolgendes Kapitel", „Verifikationskapitel", „Rolloutkapitel", „spätere Kapitel") sowie die sachlich überholte Präambel von Anhang A, die Kapitel 11 als künftig beschrieb. |
| **Durchgeführte Änderung** | Ersetzt durch konkrete Kapitelnummern in: **2** (Vorspann → Kapitel 4 und 5), **4.1** (→ Kapitel 5, 6, 7 und Sprint Planning Phase), **4.8** (→ Kapitel 6 und 6.4), **5.4** (DA-012 → Kapitel 8, EV-D04, GV-03), **5.8** (→ Kapitel 6; Kapitel 8 und 9; Kapitel 13), **6.1** (→ Kapitel 7.3, 12.7), **6.5** (Tabelle um Spalte „Kapitel" erweitert, mit Angabe der konkreten Abschnitte), **7.1** (Tabelle ebenso, mit Angabe der übernehmenden Prinzipien MP-01, MP-03, RPR-04). **Anhang A**, Präambel vollständig neu gefasst: Feststellung, dass die angekündigte Überführung mit Kapitel 11.10 vollzogen ist. |
| **Begründung** | Die Verweise waren auflösbar, aber nicht aufgelöst — Restbestand des Befundes GP-002. |
| **Betroffene Kapitel** | 2 (Vorspann), 4.1, 4.8, 5.4, 5.8, 6.1, 6.5, 7.1, Anhang A |
| **Auswirkung auf Traceability** | **Verbessert.** Sämtliche Verweise sind nun numerisch auflösbar; die programmatische Referenzprüfung meldet weiterhin 0 tote Referenzen. |
| **Status** | **CLOSED** |

### L-05 — Anhang A als zweites Register

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | Anhang A trug den Titel „Governance Risk Register" und führte eine eigene Registertabelle mit Statusspalte, während 11.11 und 13.9 die Registerführung ausschließlich für 11.11 reklamierten. |
| **Durchgeführte Änderung** | Anhang A umbenannt in **„Pending Governance Resolution GR-001"**. Ausdrückliche Feststellung „Er ist kein Register"; die Kopftabelle als **nachrichtlich** gekennzeichnet, um eine Spalte „Registerführung → Kapitel 11.11" ergänzt und auf die Klasse RK-04 umgestellt. Der GR-001-Eintrag um das Feld „Registerführung" ergänzt; „Risikokategorie" auf „Risikoklasse (Kapitel 11.4)" präzisiert. PR-001.9 entsprechend nachgeführt. Sämtliche verweisenden Stellen umgestellt: **5.5.4** (Aufnahme ins konsolidierte Register statt „Governance Risk Register (Anhang A)"), **8.5** (EV-D05 Quelle), **8.8** (GV-08 Bezug), **9.6**, **9.7** (TC-06 Quelle), **10.7** (Abschnittstabelle), **11.10** („Verortung"). |
| **Begründung** | Zwei Artefakte mit der Bezeichnung Register waren die Ursache von M-02. Die Umbenennung beseitigt sie an der Wurzel. |
| **Betroffene Kapitel** | 5.5.4, 8.5, 8.8, 9.6, 9.7, 10.7, 11.10, Anhang A |
| **Auswirkung auf Traceability** | Keine. PR-001.1 bis PR-001.9 bleiben inhaltlich unverändert; ausschließlich Bezeichnung und Registerzuordnung wurden vereinheitlicht. |
| **Status** | **CLOSED** |

### L-06 — 13.14 verwies auf eine nicht existierende Empfangsbedingung

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | 13.14 übergab die Risikolage „sämtliche Einträge CLOSED oder ACCEPTED" an „Kapitel 10.3, AP-01"; AP-01 ist eine Findings-, keine Risikostatusbedingung. |
| **Durchgeführte Änderung** | Empfangende Stelle auf **Kapitel 10.6 (Bedingung 5)** und **Kapitel 8.8 (GV-08)** korrigiert; Gegenstand um den Verweis auf Kapitel 11.11 und die Zahl 16 präzisiert. |
| **Begründung** | 10.6 Bedingung 5 („Zu GR-001 liegt eine dokumentierte Entscheidung vor") und GV-08 sind die tatsächlichen Empfangsbedingungen für die Risikolage. |
| **Betroffene Kapitel** | 13.14 |
| **Auswirkung auf Traceability** | **Repariert.** Die Schnittstelle Kapitel 13 → Kapitel 10 verweist nun auf existierende Bedingungen. |
| **Status** | **CLOSED** |

### L-07 — ADR-011-Bezeichnungsdifferenz ohne Registerführung

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | 3.7 dokumentierte die Bezeichnungsdifferenz zu ADR-011 als „Governance-Befund", ohne ID, Owner, Status, Frist oder Registereintrag. |
| **Durchgeführte Änderung** | Umgestellt auf eine ausdrückliche **Einstufung als redaktionelle Feststellung, nicht als Governance-Befund im Sinne von AP-01 und GV-08**, mit fünfzeiliger Prüftabelle: kein inhaltlicher Widerspruch, keine Wirkung auf Planungsinhalte, keine Wirkung auf GI-10 (das ADR-011 nach Nummer und Status bestätigt, nicht nach Titel), keine Wirkung auf AP-01/GV-08, keine Registeraufnahme mit Begründung (RP-03). |
| **Begründung** | Die vom Audit angebotene Alternative zur Registrierung. Eine Registeraufnahme wäre ohne Risikogehalt und würde die Registerlage verzerren; sie hätte zudem einen 17. Eintrag erzeugt und sämtliche Registerzählungen erneut verschoben. |
| **Betroffene Kapitel** | 3.7 |
| **Auswirkung auf Traceability** | Keine. Die Feststellung bleibt dokumentiert; ausschließlich ihre Einstufung wird eindeutig. |
| **Status** | **CLOSED** |

---

### E-01 — Dokumentkopf im Widerspruch zu 10.5 und 10.8

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | „DRAFT — **in Erstellung** … enthält **derzeit** die Kapitel …" widersprach 10.8 („Planungsscope vollständig abgedeckt") und 10.5 („RL-00 verlassen"). |
| **Durchgeführte Änderung** | Kopf neu gefasst: „**DRAFT — inhaltlich vollständig, nicht genehmigt**"; „enthält derzeit" → „umfasst"; Ergänzung des Verweises auf 10.8/CC-11..CC-13 und der Feststellung, dass der Status DRAFT bis zum Durchlaufen des Genehmigungsprozesses gemäß 10.4 fortbesteht. |
| **Betroffene Kapitel** | Dokumentkopf |
| **Auswirkung auf Traceability** | Keine. |
| **Status** | **CLOSED** |

### E-02 — Anhänge als Zeilen einer Kapiteltabelle

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | 10.7 führte Anhang A und B als Zeilen einer „Kapitelbezogenen Prüfung", während Anhang A feststellt, kein Kapitel zu sein. |
| **Durchgeführte Änderung** | Überschrift auf **„Abschnittsbezogene Prüfung"**, Spalte „Kapitel" auf „Abschnitt", Zeilenbezeichner auf „Kapitel 1" … „Anhang A" vereinheitlicht; Vorspann mit der ausdrücklichen Feststellung, dass die Anhänge keine Kapitel sind und ausschließlich zur Vollständigkeit der Prüfung geführt werden. |
| **Betroffene Kapitel** | 10.7 |
| **Auswirkung auf Traceability** | Keine. |
| **Status** | **CLOSED** |

### E-03 — Widerspruch bei der Anzahl kritischer Pfade

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | 6.8 prüfte „Kritischer Pfad identifiziert: 1 | 1", während 6.5 zwei Pfade darstellte. |
| **Durchgeführte Änderung** | Ergebnisspalte in 6.8 präzisiert: der Pfad besteht aus der verbindlichen Kette und der innerhalb von Phase 1 strukturell längsten Teilkette; beide sind in 6.5 als **ein** Pfad dargestellt, nicht als zwei konkurrierende. |
| **Betroffene Kapitel** | 6.8 |
| **Auswirkung auf Traceability** | Keine. |
| **Status** | **CLOSED** |

### E-04 — Kursive Selbstbegründungen gegenüber dem Auftraggeber

| Feld | Inhalt |
|---|---|
| **Ursprüngliches Finding** | Acht Abschnitte enthielten kursive Hinweise der Form „*Ergänzung gegenüber der vorgegebenen Struktur. Begründung: …*", die sich an den Auftraggeber der Kapitelerstellung richteten, nicht an den Leser des Referenzdokuments. |
| **Durchgeführte Änderung** | Sämtlich in leserorientierte Einordnungen der Form „**Einordnung.** …" überführt: **11.5**, **11.9**, **11.11**, **11.13**, **12.6**, **12.8**, **12.9**, **13.13**. Die sachliche Begründung bleibt erhalten und wurde jeweils auf die tatsächlich einschlägige Beschränkung bezogen (RC-01/RC-02, RC-11, RC-09, ACN-05, MC-10). Programmatisch verifiziert: keine Fundstelle mehr. |
| **Betroffene Kapitel** | 11.5, 11.9, 11.11, 11.13, 12.6, 12.8, 12.9, 13.13 |
| **Auswirkung auf Traceability** | Keine. |
| **Status** | **CLOSED** |

---

## 4. Zusätzlich vorgenommene Folgeanpassungen

Die folgenden Ergänzungen sind **keine eigenständigen Korrekturen**, sondern
zwingende Folgen der obigen Änderungen. Sie wurden vorgenommen, um durch die
Korrektur keine neue Inkonsistenz zu erzeugen.

| Ergänzung | Kapitel | Folge von | Zweck |
|---|---|---|---|
| Lesehinweis zur Evidence-Spalte (FR-zentrierte Matrix führt keine NFR-Nachweise) | 8.4 | H-02 | Verhindert eine scheinbare Divergenz zwischen der Matrix in 8.4 und der Gate-Zuordnung in 8.5 |
| Entsprechender Hinweis zur Test-Traceability | 9.5 | H-02 | Wie vorstehend |
| Hinweis zum einheitenbezogenen gegenüber dem phasenbezogenen Gate-Anteil | 12.11 | H-02 | Erklärt, warum „Ende MS-02" auch für QG-001 zutrifft |
| Hinweis zur Zuordnung von QG-001 zu RU-01 | 13.11 | H-02 | Wie vorstehend |
| Verweis auf GDR-001 als angewandtes Eskalationsbeispiel | 7.6, 7.8 | H-01 | PP-04 verlangt die Sichtbarkeit erkannter Governance-Konflikte |
| Statusaussagen zum Gesamtkonsistenzaudit nachgeführt (AP-09, RL-01 „Aktueller Stand", 10.8 Schlussabsatz) | 10.3, 10.5, 10.8 | Durchführung des Audits selbst | Die Formulierungen „W-2 steht aus" waren mit Abschluss des Audits stale geworden; ACN-08 verlangt Feststellungen statt Entscheidungen, und die Feststellung musste dem tatsächlichen Stand entsprechen |

---

## 5. Nachweis der Einhaltung der Bearbeitungsgrundsätze

Programmatisch und manuell verifiziert nach Abschluss der Korrekturen:

| Prüfung | Ergebnis |
|---|---|
| Tote Kapitelreferenzen | **0** |
| Anzahl Functional Requirements | 14 — unverändert |
| Anzahl Acceptance Criteria | 29 — unverändert |
| Anzahl Quality Gates | 8 — unverändert |
| Anzahl Work Packages | 7 — unverändert |
| Anzahl Evidence-Einträge | 20 — unverändert |
| Anzahl Registereinträge | 16 — unverändert; ausschließlich der Führungsort vereinheitlicht |
| Anzahl Deliverables | 10 — unverändert; erstmals zugeordnet |
| Einträge im konsolidierten Register (11.11) | 16 — programmatisch gezählt |
| Reststellen „GR-001 … OPEN" | **0** |
| Reststellen „Governance Risk Register" | **0** |
| Reststellen „Ergänzung gegenüber der vorgegebenen Struktur" | **0** |
| Reststellen „51 referenzierte" | **0** |
| Änderungen an Charter, ES, Architecture Book, Baseline, ADRs | **keine** |

---

## 6. Ergebnis

| Kategorie | Anzahl | Geschlossen | Offen |
|---|---|---|---|
| Critical | 0 | — | 0 |
| High | 2 | 1 (H-02) | **1 (H-01 — an Governance übergeben)** |
| Medium | 8 | 8 | 0 |
| Low | 7 | 7 | 0 |
| Editorial | 4 | 4 | 0 |
| **Summe** | **21** | **20** | **1** |

H-01 ist nicht „offen geblieben", sondern auftragsgemäß in das dafür
vorgesehene Verfahren überführt: Der Sachverhalt ist vollständig dokumentiert,
die Entscheidungsinstanz ist benannt, vier Optionen sind bewertet, die Frist
ist bestimmt. Der Plan löst ihn nicht auf (PP-04).

Die abschließende Bewertung, ob Readiness Level RL-01 erreicht ist, erfolgt im
**Global Consistency Audit R2**.

---

*Ende Correction Report R1.*
