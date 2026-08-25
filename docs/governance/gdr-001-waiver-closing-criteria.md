# GDR-001 — Governance Decision Record

## Auslegung der Closing Criteria §9 (1) und §9 (2) von WAIVER-DEV-001

| Eigenschaft | Wert |
|---|---|
| **Dokument-ID** | GDR-001 |
| **Typ** | Governance Decision Record — Entscheidungsvorlage und Entscheidung |
| **Status** | **ENTSCHIEDEN — Option B angenommen** (siehe §7) |
| **Datum der Vorlage** | 2026-08-05 |
| **Datum der Entscheidung** | 2026-08-05 |
| **Vorgelegt von** | Lead Implementation Planner |
| **Entscheidungsinstanz** | Governance Architect / Release Authority |
| **Umsetzendes Artefakt** | [WAIVER-AMENDMENT-001](waiver-amendment-001.md) (APPROVED, 2026-08-05) |
| **Auslöser** | Global Consistency Audit (W-2, R1), Finding **H-01** |
| **Betroffene Artefakte** | [WAIVER-DEV-001](waiver-dev-001.md) §3.1, §9; [Development Standard v1.1](../development-standard-v1.1.md) §6.2 #4/#5; [Implementation Plan 1.0](../milestone-1.0-implementation-plan.md) Kapitel 1.6, 4, 5, 5.5.1, 5.8, ST-10 |
| **Späteste notwendige Entscheidung** | Vor dem Independent Review (W-3) — **eingehalten** |
| **War blockierend für** | Workflow-Schritt W-6 (Approval) über AB-01 und AB-02 — **Blockade aufgehoben** |
| **War nicht blockierend für** | Workflow-Schritt W-3 (Independent Review) |

---

## 1. Zweck dieses Dokuments

Dieses Dokument legt einen **Konflikt zwischen zwei genehmigten
Governance-Artefakten** zur Entscheidung vor. Es trifft **keine Entscheidung**
und empfiehlt keine Option als bereits beschlossen.

Der Implementation Plan 1.0 darf diesen Konflikt nicht eigenständig auflösen:

- Kapitel 1.5 des Plans verpflichtet zur Unterbrechung und Eskalation, wenn ein
  Bedarf eine Governance Constraint verletzen würde.
- PP-04 (Governance First) untersagt die Auflösung erkannter
  Governance-Konflikte im Plan.
- ACN-09 untersagt die Absenkung bestehender Bedingungen zur Herstellung der
  Genehmigungsfähigkeit.

Der Plan wurde daher im Correction Cycle R1 in diesem Punkt **nicht
korrigiert**. Kapitel 5.5.1 verweist auf dieses Dokument.

---

## 2. Sachverhalt

### 2.1 Wortlaut der normativen Vorgaben

**Development Standard v1.1 §6.2 — Pflichtabschnitte der Engineering
Specification:**

| # | Abschnitt | Inhalt gemäß Wortlaut |
|---|---|---|
| 4 | Delta Analysis | „Exakte Differenz zwischen Baseline und Zielzustand **pro Datei**" |
| 5 | Module Work Breakdown | „**Pro Datei: konkrete Änderungen mit Codebeispielen**" |

**WAIVER-DEV-001 §3.1 — Verbindliche Festlegungen:**

> (4) Der Implementation Plan MUSS eine vollständige Delta Analysis **gemäß
> Development Standard v1.1 §6.2 #4** enthalten.
>
> (5) Der Implementation Plan MUSS ein vollständiges Module Work Breakdown
> **gemäß Development Standard v1.1 §6.2 #5** enthalten.

**WAIVER-DEV-001 §9 — Closing Criteria:**

> (1) Implementation Plan 1.0 enthält eine vollständige Delta Analysis gemäß
> Development Standard v1.1 §6.2 #4 — mit Dateireferenzen (**Datei, Zeile,
> Status**) für jede Änderung im Milestone-Scope.
>
> (2) Implementation Plan 1.0 enthält ein vollständiges Module Work Breakdown
> gemäß Development Standard v1.1 §6.2 #5 — mit dateibasierten
> Änderungsbeschreibungen und **Codebeispielen** für jedes Work Package.

### 2.2 Gegenläufige Vorgaben desselben Governance-Rahmens

| Quelle | Vorgabe | Wirkung |
|---|---|---|
| Milestone 1.0 Charter §8 | Zweistufiger Governance-Prozess; Implementierung erst nach genehmigtem Plan und Sprint Planning | Der Plan ist ein Planungs-, kein Umsetzungsartefakt |
| Implementation Plan 1.0, Kapitel 1.6 | Produktionscode, Sprint Implementation und Runtime Changes sind **NOT AUTHORIZED** | Der Plan darf keine Umsetzungsentscheidungen treffen |
| ES 1.0 Approval Record §11 | Autorisiert ausschließlich „Implementation Plan 1.0 (DRAFT)" | Autorisierungsgrenze |
| Implementation Plan 1.0, ST-10 / SQ-08 / VC-06 | „Keine Implementierungsdetails. Keine Klassen, Methoden, Algorithmen." | Codebeispiele sind planintern ausgeschlossen |
| Implementation Plan 1.0, Kapitel 5.8 | „Klassen, Methoden, Algorithmen, **Codebeispiele** — Nicht Gegenstand der Planungsphase" | Ausdrücklicher Ausschluss |
| Implementation Plan 1.0, Kapitel 4.1 / 4.10 | Delta Analysis „nicht auf Codeebene"; „keine Dateinamen" | Delta Analysis ist bewusst lösungsneutral |

### 2.3 Tatsächlicher Erfüllungsstand des Plans

| Kriterium | Gefordert | Im Plan enthalten | Fundstelle |
|---|---|---|---|
| Delta Analysis pro Datei | Differenz **pro Datei** | Differenz auf Anforderungsebene (15 Deltas); Dateizuordnung getrennt in Kapitel 5 | 4.5, 5.5.2 |
| Dateireferenz: **Datei** | ja | **Erfüllt** — 50 Artefakte, sämtlich gegen den Repository-Stand verifiziert | 5.5.2 |
| Dateireferenz: **Status** | ja | **Erfüllt** — vier definierte Statuswerte je Datei | 5.2, 5.5.2 |
| Dateireferenz: **Zeile** | ja | **Teilweise** — 9 verifizierte Zeilenanker; für Änderungen, deren Ort erst die Umsetzung bestimmt, bewusst keine Angabe | 5.5.3 |
| MWB pro Work Package | ja | **Erfüllt** — alle 7 Work Packages, 15 MWB-Einträge | 5.3, 5.4, 5.6 |
| MWB: dateibasierte Änderungsbeschreibungen | ja | **Teilweise** — je Datei Änderungsart, Änderungsstatus und Änderungsbeziehung (Primär / Sekundär / Nachweis); keine inhaltliche Beschreibung der Änderung | 5.4, 5.5.2 |
| MWB: **Codebeispiele** | ja | **Nicht enthalten** — ausdrücklich ausgeschlossen | 5.8, ST-10 |
| Scope Verification mit Dateireferenzen | ja | **Erfüllt** | 4.6, 5.5.2 |

### 2.4 Der eigentliche Konflikt

Zwei genehmigte Artefakte verlangen Gegenläufiges:

> **WAIVER-DEV-001 §9 (2)** verlangt Codebeispiele im Implementation Plan.
> **Charter §8 und die Autorisierungsgrenze** untersagen dem Implementation
> Plan implementierungsnahe Festlegungen vor der Sprint Planning Phase.

Der Konflikt ist **strukturell**, nicht redaktionell: Er entstand, weil §6.2
des Development Standard Pflichtabschnitte einer *Engineering Specification*
definiert, die durch den Waiver in ein Dokument mit anderer
Autorisierungsgrenze verschoben wurden. Die Anforderungen an den Detailgrad
wurden dabei unverändert mitgeführt.

### 2.5 Warum eine Entscheidung erforderlich ist

| Wirkung | Grundlage |
|---|---|
| §9 (3) verlangt die Bestätigung der Vollständigkeit durch den Independent Review | WAIVER-DEV-001 §9 (3) |
| Eine unerfüllte Closing Criterion verhindert den Übergang nach W-6 | Implementation Plan, AB-02 |
| Eine unerfüllte Closing Criterion ist Ausschlussgrund für den Beginn der Umsetzung | Implementation Plan, 10.6, Ausschluss 4 |
| Der Waiver bleibt aktiv, bis alle Closing Criteria erfüllt sind | WAIVER-DEV-001 §9, Schlusssatz |
| Ohne Entscheidung trifft der Independent Review die Auslegung implizit | Risiko einer nicht dokumentierten Governance-Entscheidung |

---

## 3. Entscheidungsoptionen

Die Optionen sind vollständig und schließen einander aus. Für jede sind
Wirkung, Aufwandsrichtung, Risiken und Folgeartefakte angegeben.

### Option A — Auslegungsentscheidung: Zweckerfüllung genügt

**Inhalt.** Der Governance Architect stellt fest, dass Kapitel 4 und 5 die
Closing Criteria §9 (1) und §9 (2) **ihrem Zweck nach** erfüllen. Der Zweck der
Kriterien — die Vorab-Bestimmung des exakten Änderungsumfangs zur
Scope-Begrenzung (Development Standard v1.1 §6.2, Begründung) — wird durch die
Kombination aus Delta-Katalog, Modul- und Dateizuordnung, Änderungsart,
Änderungsstatus und Änderungsbeziehung erreicht. Die Merkmale „Zeile" und
„Codebeispiele" werden als **nicht anwendbar** auf ein Dokument mit der
Autorisierungsgrenze des Implementation Plans festgestellt.

| Aspekt | Bewertung |
|---|---|
| Änderung am Plan | Keine inhaltliche; Kapitel 5.5.1 erhält den Verweis auf diese Entscheidung |
| Änderung am Waiver | Keine |
| Änderung am Development Standard | Keine |
| Aufwand | Gering — ein Governance-Dokument |
| Vereinbar mit Charter §8 | Ja |
| Vereinbar mit ACN-09 | Ja, **sofern** die Feststellung ausdrücklich als Auslegung dokumentiert wird und nicht als stillschweigende Absenkung erfolgt |
| Risiko | Eine dokumentierte Auslegungsentscheidung, die vom Wortlaut abweicht, kann bei späteren Milestones als Präzedenz herangezogen werden. Gegenmittel: ausdrückliche Begrenzung auf Milestone 1.0 analog WAIVER-DEV-001 §3.2 |
| Folgeartefakt | Ergänzung dieses GDR um den Entscheidungsteil; Aufnahme in den Approval Record des Plans |

### Option B — Präzisierung des Waivers (Waiver Amendment)

**Inhalt.** WAIVER-DEV-001 wird um ein Amendment ergänzt, das §9 (1) und §9 (2)
für Milestone 1.0 an die Autorisierungsgrenze des Implementation Plans
anpasst: Dateireferenz mit Datei und Status verbindlich, Zeilenanker nur wo
stabil verifizierbar, Änderungsbeschreibung auf Ebene von Änderungsart und
Änderungsbeziehung, keine Codebeispiele.

| Aspekt | Bewertung |
|---|---|
| Änderung am Plan | Keine |
| Änderung am Waiver | Ja — Amendment mit eigenem Genehmigungsverfahren |
| Änderung am Development Standard | Keine |
| Aufwand | Mittel — Amendment, Genehmigung, Fortschreibung von IN-08 |
| Vereinbar mit Charter §8 | Ja |
| Vereinbar mit ACN-09 | Ja — die Bedingung wird nicht durch den Plan abgesenkt, sondern durch die zuständige Instanz im dafür vorgesehenen Verfahren geändert |
| Risiko | Ein Amendment an einem bereits genehmigten Waiver erfordert eine erneute Genehmigungsentscheidung und verlängert den Governance-Weg vor W-3 |
| Folgeartefakt | `waiver-dev-001-amendment-1.md`; Approval Record; Fortschreibung von Kapitel 1.4 (IN-08) und 5.5.1 |

### Option C — Erfüllung des Wortlauts im Plan

**Inhalt.** Der Implementation Plan wird um dateibasierte
Änderungsbeschreibungen mit Codebeispielen je Work Package und um
Zeilenangaben für jede Änderung ergänzt.

| Aspekt | Bewertung |
|---|---|
| Änderung am Plan | Erheblich — Kapitel 5 wird um Änderungsbeschreibungen und Codebeispiele erweitert; 5.8 und ST-10 müssten geändert werden |
| Änderung am Waiver | Keine |
| Änderung am Development Standard | Keine |
| Aufwand | Hoch |
| Vereinbar mit Charter §8 | **Nein.** Codebeispiele und Zeilenfestlegungen für noch nicht bestimmte Änderungsorte sind Umsetzungsentscheidungen. Kapitel 1.6 führt Sprint Implementation und Feature Development als NOT AUTHORIZED |
| Vereinbar mit ACN-09 | Ja |
| Risiko | **Hoch.** Die Ergänzung würde die Autorisierungsgrenze überschreiten und zugleich Regel 9 aus Kapitel 5.2 („Keine Erfindung von Dateien") verletzen, da Codebeispiele für noch nicht bestimmte Artefakte erfunden werden müssten. Zusätzlich entstünde ein Widerspruch zu PP-04 und SP-01 |
| Folgeartefakt | Umfangreiche Planüberarbeitung; Rückkehr nach W-1; erneutes W-2 |

### Option D — Verschiebung der Kriterien in die Sprint Planning Phase

**Inhalt.** Die Closing Criteria §9 (1) und §9 (2) werden in ihren
implementierungsnahen Anteilen (Zeile, Codebeispiele) der Sprint Planning
Phase zugewiesen. Der Waiver bleibt über die Genehmigung des Implementation
Plans hinaus aktiv und schließt erst mit der genehmigten Sprintplanung.

| Aspekt | Bewertung |
|---|---|
| Änderung am Plan | Gering — Kapitel 5.5.1 und AP-02 kennzeichnen die Teilerfüllung; die Waiver-Schließung wird von der Plangenehmigung entkoppelt |
| Änderung am Waiver | Ja — Fortschreibung der Closing Criteria um eine Phasenzuordnung |
| Änderung am Development Standard | Keine |
| Aufwand | Mittel |
| Vereinbar mit Charter §8 | Ja — die Detailtiefe entsteht dort, wo sie autorisiert ist |
| Vereinbar mit ACN-09 | Ja, sofern die Kriterien nicht entfallen, sondern verschoben werden |
| Risiko | Der Waiver bleibt länger aktiv und ist bei jeder Governance-Prüfung des Milestones mitzuführen. WR-1 (Kapitel 11.9) bleibt entsprechend länger offen. Die Genehmigung des Plans erfolgt mit einem ausdrücklich unerfüllten Closing Criterion — AB-02 müsste dafür ausdrücklich außer Anwendung gesetzt werden |
| Folgeartefakt | Waiver-Fortschreibung; Anpassung von AB-02 oder ausdrückliche Ausnahmeentscheidung |

---

## 4. Vergleich

| Kriterium | Option A | Option B | Option C | Option D |
|---|---|---|---|---|
| Wortlauttreue zu §9 | Auslegung | Angepasst | Vollständig | Verschoben |
| Wahrt die Autorisierungsgrenze | Ja | Ja | **Nein** | Ja |
| Wahrt ACN-09 | Ja | Ja | Ja | Bedingt |
| Aufwand | Gering | Mittel | Hoch | Mittel |
| Verzögerung vor W-3 | Keine | Mittel | Hoch | Mittel |
| Präzedenzrisiko | Mittel | Gering | Gering | Mittel |
| Waiver schließbar mit Plangenehmigung | Ja | Ja | Ja | **Nein** |

---

## 5. Bewertung durch den Vorlegenden

Ohne Entscheidungswirkung, zur Information der Entscheidungsinstanz:

**Option C ist nicht empfehlbar.** Sie ist die einzige Option, die die
Autorisierungsgrenze aus Charter §8 und Kapitel 1.6 verletzt und zugleich die
Erfindung von Artefakten erzwingt, die Regel 9 aus Kapitel 5.2 ausdrücklich
untersagt.

**Option A und Option B führen zum gleichen materiellen Ergebnis** und
unterscheiden sich in der Form: A entscheidet durch Auslegung, B durch Änderung
des Wortlauts. B ist formal sauberer, A ist schneller. Für ein
Engineering-Referenzprojekt spricht die höhere Revisionssicherheit von B; für
den Projektfortschritt spricht A.

**Option D** ist sachlich vertretbar, erzeugt aber eine zusätzliche
Abhängigkeit: Die Genehmigung des Plans erfolgte dann mit einem ausdrücklich
unerfüllten Closing Criterion, was eine Ausnahmeentscheidung zu AB-02
erfordert.

Die Entscheidung selbst trifft ausschließlich die in der Kopftabelle benannte
Instanz.

---

## 6. Wirkung auf den Implementation Plan bis zur Entscheidung

| Gegenstand | Stand |
|---|---|
| Kapitel 5.5.1 | Führt alle vier Closing Criteria mit Status; verweist auf dieses Dokument; stellt ausdrücklich fest, dass es die Erfüllung **nicht** feststellt |
| Wortlaut der Kriterienzitate in 5.5.1 | **Unverändert** — im Correction Cycle R1 bewusst nicht korrigiert |
| Kapitel 5.8, ST-10 | **Unverändert** — Ausschluss von Codebeispielen bleibt bestehen |
| CC-08, AP-02, 8.9 (#5) | **Unverändert** — sämtlich mit „adressiert" beziehungsweise „berücksichtigt" formuliert, nicht mit „erfüllt" |
| W-3 | Nicht blockiert. Der Independent Review kann und soll zu dieser Vorlage Stellung nehmen |
| W-6 | Blockiert bis zur dokumentierten Entscheidung (AB-01, AB-02) |

**Stand nach der Entscheidung.** Die vorstehende Tabelle beschreibt den Zustand
vor der Entscheidung. Der Implementation Plan wurde durch das Amendment
**nicht geändert**; seine Statusaussagen zu GDR-001 sind seither überholt und
als redaktionelle Nachführung **NV-001** im Finding Closure Addendum geführt —
editorial, nicht blockierend, ohne Wirkung auf Traceability oder RL-01.

---

## 7. Entscheidungsteil

| Feld | Wert |
|---|---|
| **Gewählte Option** | **Option B — Präzisierung des Waivers (Waiver Amendment)** |
| **Begründung** | Option C scheidet aus, weil sie als einzige Option die Autorisierungsgrenze aus Charter §8 und Kapitel 1.6 verletzt und die Erfindung von Artefakten erzwingt, die Regel 9 aus Kapitel 5.2 untersagt. Option D erzeugt eine zusätzliche Abhängigkeit: Die Plangenehmigung erfolgte dann mit einem ausdrücklich unerfüllten Closing Criterion und erforderte eine Ausnahmeentscheidung zu AB-02. Zwischen A und B wurde **B** gewählt, weil ein Engineering-Referenzprojekt die höhere Revisionssicherheit einer Wortlautpräzisierung gegenüber einer reinen Auslegungsentscheidung verlangt: Ein späterer Prüfer soll die verbindliche Bedeutung des Begriffs „Dateireferenz" unmittelbar im Governance-Artefakt vorfinden und nicht aus einer Auslegungsfeststellung ableiten müssen. Der Zeitvorteil von Option A wiegt diesen Nachteil nicht auf, zumal beide Optionen materiell zum selben Ergebnis führen. |
| **Geltungsbereich** | Ausschließlich Milestone 1.0. Präzisiert werden ausschließlich WAIVER-DEV-001 §9 (1) und §9 (2) sowie deren Inkorporation über §3.1 (4) und §3.1 (5). Kein Präzedenzfall für spätere Milestones (analog WAIVER-DEV-001 §3.2). |
| **Entscheidungsdatum** | 2026-08-05 |
| **Entscheidende Instanz** | Governance Architect / Release Authority |
| **Folgeartefakte** | [WAIVER-AMENDMENT-001](waiver-amendment-001.md) (APPROVED); [Finding Closure Addendum H-01](../audits/implementation-plan-1.0-finding-closure-addendum-h-01.md); [Governance Status Summary](implementation-plan-1.0-governance-status-summary.md) |
| **Wirkung auf WR-1 (Implementation Plan 11.9)** | **Keine Neubewertung.** WR-1 bleibt RK-05, Kritikalität Erhöht, Status MITIGATED mit ausstehender Bestätigung durch den Independent Review. Das Amendment beseitigt die Auslegungsunsicherheit, nicht die Bestätigungspflicht nach §9 (3). Registerstand unverändert 16 Einträge. |
| **Wirkung auf AB-02** | AB-02 („Eine Closing Criterion von WAIVER-DEV-001 ist nicht erfüllt → kein Übergang nach W-6") bleibt **unverändert in Kraft**. Es wird nicht außer Anwendung gesetzt. §9 (1), (2) und (4) sind nach der präzisierten Auslegung erfüllt; §9 (3) bleibt ausstehend und wird durch W-3 erfüllt. AB-02 greift damit weiterhin bis zum Abschluss von W-3 — was der vorgesehenen Reihenfolge W-3 → W-4 → W-5 → W-6 entspricht und keinen zusätzlichen Vorbehalt begründet. |
| **Wirkung auf AB-01** | AB-01 („Ein Finding der Schweregrade Critical oder High ist offen → kein Übergang nach W-6") ist mit der Schließung von H-01 **nicht mehr einschlägig**. |
| **Wirkung auf Charter, ES, IP, Architecture Book, Bootstrap Baseline, ADRs** | **Keine.** Sämtlich unverändert. |
| **Wirkung auf RL-01** | RL-01 ist mit der Schließung von H-01 **erreicht** (Finding Closure Addendum §5). |

### 7.1 Was mit dieser Entscheidung ausdrücklich nicht entschieden wurde

| Gegenstand | Status |
|---|---|
| Bestätigung der Vollständigkeit nach §9 (3) | **Nicht entschieden** — obliegt ausschließlich dem Independent Review (W-3) |
| Schließung von WAIVER-DEV-001 | **Nicht erfolgt** — der Waiver bleibt aktiv bis zur Bestätigung nach §9 (3) |
| GR-001 — Paralleler Artefaktbaum | **Nicht entschieden** — unverändert PENDING DECISION mit Frist gemäß PR-001.7 |
| Genehmigung des Implementation Plans | **Nicht erteilt** — Status bleibt DRAFT |
| Implementierungs- oder Sprint-Planungsautorisierung | **Nicht erteilt** |

---

## 8. Abgrenzung

Dieses Dokument ist **kein ADR und kein RDR**. Es ändert keine Architektur,
keine Baseline, keine Requirements, keine Acceptance Criteria und keine
Quality Gates. Es legt ausschließlich die Auslegung zweier Closing Criteria
eines bereits genehmigten Waivers zur Entscheidung vor.

Sollte die gewählte Option eine Änderung an der Bootstrap Baseline oder am
Architecture Book erfordern — was nach keiner der vier Optionen der Fall ist —,
wäre zusätzlich ein ADR oder RDR erforderlich.

---

*Ende GDR-001.*
