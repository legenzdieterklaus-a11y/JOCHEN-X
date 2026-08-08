# Core Principles 1.0 — Correction Report R1 (W-2)

| Eigenschaft | Wert |
|---|---|
| **Dokumenttyp** | Correction Report — Workflow-Schritt W-2 (Correction Cycle R1) |
| **Gegenstand** | [JOCHEN X – Core Principles 1.0](../core-principles-1.0.md), Revision R0 → **R1** |
| **Datum** | 2026-08-07 |
| **Rolle** | Principal Governance Architect |
| **Änderungsgrundlage** | [Governance Review Report W-1](core-principles-1.0-governance-review-w1.md) — allein verbindlich |
| **Status** | **COMPLETED** |
| **Ergebnis** | 3 High CLOSED · 11 Medium CLOSED · 4 Low CLOSED, 2 Low WAIVER · 2 Editorial CLOSED |
| **Dokumentstatus nach R1** | DRAFT (unverändert) |

---

## 1. Grundlage und Abgrenzung

Einzige Änderungsgrundlage dieses Zyklus ist der Governance Review Report W-1.
Jede in R1 vorgenommene Änderung ist in Abschnitt 3 genau einem Finding
zugeordnet. Änderungen ohne Finding-Bezug wurden nicht vorgenommen.

**Ausdrücklich nicht vorgenommen:**

| Ausschluss | Einhaltung |
|---|---|
| Neue Prinzipien | Keine. Kapitel 4, 5 und 12 wurden inhaltlich nicht erweitert. |
| Neue Kapitel | Keine. Die Kapitelfolge 0–12 ist unverändert. Ergänzt wurden Unterabschnitte innerhalb von Kapitel 0 sowie zwei deklaratorische Abschnitte nach der Schlussbestimmung (Revisionshistorie, Anhang A). |
| Neue Visionen | Keine. Kapitel 1–3 wurden ausschließlich um eine Dopplungsstreichung berührt (W1-L-02). |
| Scope-Erweiterung | Keine. Keine neue Domäne, kein neuer Geltungsbereich, keine neue Pflicht außerhalb der Findings. |
| Umstrukturierung | Keine. Keine Verschiebung, keine Umbenennung, keine Neuordnung von Kapiteln 1–12. |
| Stilistische Änderungen ohne Finding-Bezug | Keine. |
| Technische Aussagen | Keine. Prüfung siehe Verification Summary R1, Abschnitt 4. |

---

## 2. Änderungsübersicht

| Finding | Kritikalität | Ergebnis | Fundstelle in R1 |
|---|---|---|---|
| W1-H-01 | High | **CLOSED** | Kapitel 0 — „Dokumenteinordnung und Dokumenthierarchie"; Rule 2 Abs. 3 |
| W1-H-02 | High | **CLOSED** | Kapitel 0 — „Begriffsbestimmungen" |
| W1-H-03 | High | **CLOSED** | Rule 1 — „Stichtag", „Bestimmung des geschützten Bestands"; Dokumentkopf — „Referenzen" |
| W1-M-01 | Medium | **CLOSED** | Kapitel 4, Vorspann |
| W1-M-02 | Medium | **CLOSED** | 7.1 |
| W1-M-03 | Medium | **CLOSED** | 6.2 |
| W1-M-04 | Medium | **CLOSED** | 6.1 |
| W1-M-05 | Medium | **CLOSED** | Dokumentkopf, Feld „Gültigkeit" |
| W1-M-06 | Medium | **CLOSED** | Dokumentcharakter — „Geltungsvorbehalt" |
| W1-M-07 | Medium | **CLOSED** | Rule 3 — „Genehmigungsinstanz", Anforderungsliste, „Selbstbindung", „Erhöhte Anforderung"; Dokumentkopf |
| W1-M-08 | Medium | **CLOSED** | Abschnitt „Revisionshistorie" |
| W1-M-09 | Medium | **CLOSED** | Anhang A |
| W1-M-10 | Medium | **CLOSED** | Rule 2 — „Geltungsbereich ohne eigenes Prinzipienkapitel" |
| W1-M-11 | Medium | **CLOSED** | Rule 2 — „Konformitätsnachweis", „Auslegung" |
| W1-L-01 | Low | **CLOSED** | 11.6 |
| W1-L-02 | Low | **CLOSED** | 3.1 |
| W1-L-03 | Low | **WAIVER** | 4.8, 5.4, 6.2 — unverändert |
| W1-L-04 | Low | **CLOSED** | 9.6 |
| W1-L-05 | Low | **WAIVER** | 10.3 — unverändert |
| W1-L-06 | Low | **CLOSED** | Kapitel 0 — „Normsprache" |
| W1-E-01 | Editorial | **CLOSED** | Dokumentkopf — „Referenzen" |
| W1-E-02 | Editorial | **CLOSED** | Dokumentkopf — Felder „Genehmigungsinstanz", „Genehmigt" |

---

## 3. Korrekturen im Einzelnen

### 3.1 High Findings

#### W1-H-01 — Dokumenthierarchie normativ festgelegt

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | Die Rangordnung Core Principles → Architecture Book → ADRs → Engineering Specification → Implementation Plans → Implementation war nicht geregelt. Kapitel 0 traf mit „ergänzt die bestehende Governance-Hierarchie" eine deskriptive, keine normative Aussage. Rule 2 erfasste Architecture Book, ADRs und Engineering Specification nicht. |
| **Änderung 1** | Abschnitt „Dokumenteinordnung" umbenannt in „Dokumenteinordnung und Dokumenthierarchie" und um drei normative Bestimmungen ergänzt: **Rangordnung** (Tabelle mit den sechs geforderten Rangstufen), **Wirkung der Rangordnung** (Vereinbarkeitspflicht nach oben; Widerspruch = Fehler des rangniedrigeren Dokuments; kein Änderungs-, Auslegungs- oder Aufhebungsrecht nach oben), **Verhältnis zu Governance Rule 1**. |
| **Änderung 2** | Rule 2 um einen Absatz ergänzt: zukünftige Versionen bestehender Dokumentklassen — insbesondere zukünftige Fassungen des Architecture Book, zukünftige ADRs, zukünftige Fassungen der Engineering Specification — sind erfasst. |
| **Erhalt von Rule 1** | Der Abschnitt „Verhältnis zu Governance Rule 1" bestimmt ausdrücklich: Die Rangordnung begründet keine Rückwirkung; genehmigte und eingefrorene Artefakte behalten ihre Gültigkeit in der genehmigten Fassung unabhängig von ihrer Rangstufe; die Rangordnung wirkt nur auf Dokumente, die nach Genehmigung entstehen, sowie auf zukünftige Versionen. Architecture Book v2.0 ist namentlich als unberührt ausgewiesen. |
| **Begründung** | Der vom Review beanstandete Konfliktfall — künftige Version eines bestehenden ranghöheren Dokuments — ist damit geregelt, ohne dass eine bestehende Genehmigung berührt wird. |
| **Verifikation** | Rangordnung vollständig (6/6 Stufen, Reihenfolge wie gefordert) ✓ · Rule 1 unverändert in Wirkung, ausdrücklich vorbehalten ✓ · Kein APPROVED/FROZEN-Artefakt geändert ✓ · Keine technische Aussage ✓ |
| **Status** | **CLOSED** |

#### W1-H-02 — Tragende normative Begriffe bestimmt

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | „kritisch", „erhebliche Wirkung", „bedeutsam", „sensibel" und „lokale Vertrauensdomäne" trugen die Artikel 4 und 8 sowie 5.5, 5.10, 6.2, 7.2, 8.4 und 8.5, ohne bestimmt zu sein. Artikel 4 und 8 waren dadurch nicht prüfbar. |
| **Änderung** | Abschnitt „Begriffsbestimmungen" in Kapitel 0 ergänzt. Bestimmt werden alle fünf vom Review benannten Begriffe sowie der sie verbindende Oberbegriff „Wirkung". Eingeführt wird eine dreistufige Wirkungsskala **bedeutsam < erheblich < kritisch**, gestützt auf zwei Größen: Reichweite (Verbleib in der lokalen Vertrauensdomäne) und Umkehrbarkeit. Abschließend die **Auslegungsregel**: Bei Zuordnungszweifel gilt die höhere Stufe. |
| **Abgrenzung** | Die Bestimmungen sind ausdrücklich als Auslegungshilfe gekennzeichnet („Ihre Bestimmung dient ausschließlich der Auslegung. Sie enthält keine technische Festlegung und keine Vorgabe für die Umsetzung."). Sie nennen kein Verfahren, keinen Mechanismus, keinen Schwellwert und keine Metrik. |
| **Kein neues Prinzip** | Die Begriffsbestimmungen begründen keine neue Pflicht. Sie bestimmen ausschließlich die Reichweite bereits bestehender Bestimmungen. Kapitel 4, 5 und 12 sind inhaltlich unverändert. |
| **Verifikation** | Alle fünf geforderten Begriffe bestimmt ✓ · Zweifelsregel vorhanden ✓ · Artikel 4 und 8 dadurch in ihrer Reichweite bestimmbar ✓ · 8.5 („Autonomie zulässig für Vorgänge ohne erhebliche Wirkung") dadurch begrenzt ✓ · Technikfrei ✓ |
| **Status** | **CLOSED** |

#### W1-H-03 — Schutzbereich von Governance Rule 1 bestimmt

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | Rule 1 schützte „bereits genehmigte" Artefakte ohne Stichtag und ohne Referenzliste. Der Bezugszeitpunkt war bei DRAFT-Status offen; Artefakte zwischen Erstellung und Genehmigung fielen in eine ungeregelte Zone. |
| **Änderung 1** | Rule 1 um den Absatz **Stichtag** ergänzt: Geschützt sind sämtliche Artefakte, deren Genehmigung vor dem Genehmigungsdatum dieses Dokuments dokumentiert wurde. Maßgeblich allein das im Approval Record ausgewiesene Genehmigungsdatum. Artefakte zwischen Erstellung und Genehmigung sind ausdrücklich ebenfalls geschützt. Abschließender Satz: „Ein anderer Bezugszeitpunkt kommt nicht in Betracht." |
| **Änderung 2** | Rule 1 um den Absatz **Bestimmung des geschützten Bestands** ergänzt: Verweis auf die neue Referenzen-Tabelle im Dokumentkopf; die Aufführung ist deklaratorisch; fehlende Nennung führt nicht zum Schutzverlust. |
| **Änderung 3** | Referenzen-Tabelle im Dokumentkopf ergänzt (zugleich W1-E-01) mit 13 Einträgen des bekannten Governance-Bestands. |
| **Begründung** | Die gewählte Konstruktion — bestimmter Stichtag plus deklaratorische Liste — schließt Interpretationsspielraum aus und vermeidet zugleich, dass ein versehentlich nicht aufgeführtes Artefakt seinen Bestandsschutz verliert. Die vom Review beschriebene Lücke, die mit der Dauer des DRAFT-Zustands wächst, ist geschlossen. |
| **Verifikation** | Stichtag eindeutig ✓ · Zwischenzeitraum geregelt ✓ · Kein Interpretationsspielraum verbleibend ✓ · Kein Schutzverlust durch Auslassung ✓ |
| **Status** | **CLOSED** |

---

### 3.2 Medium Findings

#### W1-M-01 — Wertehierarchie

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | Kapitel 4 erklärte die Werte für gleichrangig; die Kapitel 9, 10 und 12 setzten sechs weitere Vorrangregeln. Zwei gegenläufige Kollisionsregeln. |
| **Änderung** | Kapitel 4, Vorspann, um einen Absatz ergänzt: Die Vorrangregeln der Kapitel 9, 10 und 12 sind **Konkretisierungen** der Prioritätsregel für ihren jeweiligen Bereich, keine Ausnahmen; innerhalb ihres Bereichs gehen sie der Gleichrangigkeit vor, außerhalb bleibt es bei der Gleichrangigkeit; die Verfassungsartikel gehen sämtlichen übrigen Bestimmungen vor. |
| **Begründung** | Die bestehenden Vorrangregeln bleiben wortgleich erhalten. Ergänzt wird ausschließlich ihre Einordnung. Damit ist die Kollisionsauflösung eindeutig, ohne dass ein Wert seine Stellung ändert. |
| **Verifikation** | Kein Wert hinzugefügt, entfernt oder umgewichtet ✓ · 9.3, 9.4, 9.5, 10.7, Artikel 10 und 11 unverändert ✓ · Auflösung eindeutig ✓ |
| **Status** | **CLOSED** |

#### W1-M-02 — Sicherheitsvorrang in 7.1

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | 7.1 formulierte Sicherheit absolut („immer"), ohne den Vorrang von Human First und Artikel 1 aufzunehmen. Der Konfliktfall war offen. |
| **Änderung** | 7.1, Absatz 3, präzisiert: Das Wort „immer" entfernt; ergänzt, dass der Vorrang **das System** bindet und für jede Entscheidung gilt, die das System selbst trifft; Prioritätsregel in Kapitel 4 und Artikel 1 ausdrücklich vorbehalten; klargestellt, dass Artikel 2 allein die autonome Aufhebung untersagt. |
| **Begründung** | Die vom Review als „konstruierbar, aber nicht ausgesprochen" bezeichnete Auflösung ist nun ausgesprochen. Der Sicherheitsgrundsatz selbst bleibt unverändert streng — er verliert nur seine Wirkung gegenüber dem Eigentümer, die ihm nach Kapitel 4 und Artikel 1 ohnehin nicht zukam. |
| **Verifikation** | Kein Absenken des Sicherheitsniveaus für Systementscheidungen ✓ · Artikel 1 und 2 unverändert ✓ · Kapitel 4 Prioritätsregel unverändert ✓ |
| **Status** | **CLOSED** |

#### W1-M-03 — Rollenmatrix in 6.2

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | 6.2 ordnete jeder Vertrauensebene einen Zugriffsumfang zu („kein Zugriff auf persönliche Informationen", „Sensible Bereiche bleiben verschlossen", „Zugang zu persönlichen Informationen"). Das ist eine Rechtezuordnung und damit eine für Kapitel 6 untersagte Rollenmatrix sowie eine Vorwegnahme des Trust Frameworks. |
| **Änderung** | Sämtliche Zugriffs- und Ressourcenzuordnungen in 6.2 entfernt. Die Ebenen werden stattdessen ausschließlich über die in Kapitel 0 bestimmte Wirkungsstufe charakterisiert, die der jeweilige Vertrauensnachweis trägt (Gast: ohne bedeutsame Wirkung; Benutzer: bis „bedeutsam"; Verifizierter Benutzer: erhebliche Wirkung; Kritische Freigabe: kritische Wirkung). Die Beschreibung des Eigentümers blieb unverändert, da sie keine Rechtezuordnung enthielt. |
| **Begründung** | Eine Vertrauensebene ohne jede Aussage über ihre Bedeutung wäre inhaltsleer und würde das vom Erstellungsauftrag geforderte abgestufte Vertrauensmodell aufheben. Die Bindung an Wirkungsstufen statt an Ressourcen ist die kleinstmögliche Formulierung, die den Modellcharakter erhält und keine Rechte zuweist. Welche konkreten Rechte einer Ebene zukommen, bleibt vollständig dem Trust Framework überlassen. |
| **Verifikation** | Keine Ressourcen-, Daten- oder Funktionszuordnung mehr in Kapitel 6 ✓ · Fünf Ebenen unverändert erhalten ✓ · Kein Recht, kein Verfahren, kein Mechanismus benannt ✓ · Gestaltungsraum des Trust Frameworks wiederhergestellt ✓ |
| **Status** | **CLOSED** |

#### W1-M-04 — Nicht-menschliche Entitäten im Trust Model

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | Kapitel 6 verortete Erweiterungen, Dienste und Agenten nicht, obwohl 5.3, 5.4 und 7.7 Vertrauensfragen auf sie erstrecken und Rule 2 die künftige Agent Architecture bindet. |
| **Änderung** | 6.1 um einen Absatz ergänzt: Die Ebenen beschreiben Vertrauensverhältnisse, nicht Personen, und gelten für jeden Akteur — Mensch, Erweiterung, Dienst oder Stellvertreter. Die Ebene des Eigentümers ist dem Menschen vorbehalten und für nicht-menschliche Akteure nicht erreichbar; mit ausdrücklichem Verweis auf Artikel 1. |
| **Begründung** | Es wird keine neue Ebene und kein neues Prinzip eingeführt. Der Absatz bestimmt allein die Reichweite des bereits vorhandenen Begriffs „Akteur" und leitet die Beschränkung aus Artikel 1 ab. Der Prinzipienanker für Trust Framework und Agent Architecture ist damit vorhanden. |
| **Verifikation** | Keine sechste Ebene ✓ · Kein neues Prinzip ✓ · Ableitung aus Artikel 1 ausgewiesen ✓ · Konsistent mit 5.3, 5.4, 7.7 ✓ |
| **Status** | **CLOSED** |

#### W1-M-05 — Kopffeld „Gültigkeit"

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | Der Kopf band die Ablösung an Version 2.0, Rule 3 ließ jede neue Version zu. |
| **Änderung** | Feld „Gültigkeit" lautet nun: „Unbefristet bis zur Ablösung durch eine nach Governance Rule 3 genehmigte Folgeversion". Zusätzlich wurde die Anforderungsliste in Rule 3 auf „eine neue Version oder Revision nach der in der Revisionshistorie geführten Zählung" präzisiert. |
| **Verifikation** | Kopf und Rule 3 verwenden dieselbe Versionslogik ✓ · Kein Bezug mehr auf eine bestimmte Versionsnummer ✓ |
| **Status** | **CLOSED** |

#### W1-M-06 — Statusvorwegnahme

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | Der Genehmigungsvorbehalt stand nur im Vorspann von Kapitel 0; Rule 2, Kapitel 12 und die Schlussbestimmung sprachen im bindenden Präsens. |
| **Änderung** | Abschnitt „Dokumentcharakter" um den Absatz **Geltungsvorbehalt** ergänzt: Solange der Status DRAFT lautet, entfaltet das Dokument keine Bindungswirkung; sämtliche Bestimmungen der Kapitel 0 bis 12 und der Schlussbestimmung sind bis zur Genehmigung als Entwurf zu lesen; die Bindungswirkung tritt mit der Genehmigung nach Rule 3 ein. |
| **Begründung** | Der Vorbehalt steht vor dem gesamten normativen Inhalt und erfasst ihn ausdrücklich vollständig. Ein Umschreiben der Kapitel 1–12 in den Konjunktiv wäre eine unzulässige stilistische Änderung ohne Findingbezug und hätte die Lesbarkeit der späteren genehmigten Fassung beschädigt. |
| **Verifikation** | Vorbehalt erfasst alle Kapitel und die Schlussbestimmung ✓ · Kein Kapiteltext umformuliert ✓ · Status DRAFT unverändert ✓ |
| **Status** | **CLOSED** |

#### W1-M-07 — Amendment-Prozess und Selbstbindung

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | Rule 3 benannte keine Genehmigungsinstanz, keine Verfahrensschritte, keine Prüfpflicht und keine Folgenabschätzung; sie war nicht gegen ihre eigene Änderung geschützt; Kapitel 12 hatte keine erhöhte Änderungshürde. |
| **Änderung 1** | Rule 3 um **Genehmigungsinstanz** ergänzt: Entscheidung durch die im Dokumentkopf genannte Instanz; keine andere Stelle kann eine Änderung beschließen oder in Kraft setzen. |
| **Änderung 2** | Anforderungsliste von drei auf sechs Punkte erweitert: neue Version/Revision, dokumentierter Änderungsgrund, dokumentierte Folgenabschätzung für die nach Rule 2 gebundenen Dokumente, Governance Review vor der Entscheidung, Entscheidung der Genehmigungsinstanz mit Approval Record, Eintrag in der Revisionshistorie. |
| **Änderung 3** | Absatz **Selbstbindung** ergänzt: Rule 3 gilt für sich selbst. |
| **Änderung 4** | Absatz **Erhöhte Anforderung** ergänzt: Änderungen an Kapitel 0 und Kapitel 12 benennen zusätzlich die betroffene Regel oder den betroffenen Artikel und die Folgen für die übrigen Bestimmungen. |
| **Änderung 5** | Dokumentkopf um die Felder „Genehmigungsinstanz" und „Genehmigt" ergänzt (zugleich W1-E-02). |
| **Abgrenzung** | Die Ergänzung bleibt auf Governance-Regelebene. Sie definiert keinen Prozess mit Rollen, Fristen, Gremien oder Eskalationswegen — das wäre eine Scope-Erweiterung. Sie benennt ausschließlich Instanz, Mindestbestandteile und Selbstbindung. |
| **Verifikation** | Instanz benannt ✓ · Mindestbestandteile vollständig ✓ · Selbstbindung ausgesprochen ✓ · Erhöhte Anforderung für Kapitel 0 und 12 ✓ · Kein Prozessdesign ✓ |
| **Status** | **CLOSED** |

#### W1-M-08 — Revisionshistorie

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | Rule 3 verlangte einen dokumentierten Änderungsgrund, das Dokument bot keinen Ablageort. |
| **Änderung** | Abschnitt „Revisionshistorie" nach der Schlussbestimmung ergänzt, mit einleitendem Verweis auf die Dokumentationspflicht aus Rule 3 und Spalten Revision, Datum, Auslöser, Änderungsumfang, Prüfartefakt. Einträge für R0 und R1 gesetzt. |
| **Begründung** | Kein neues Kapitel: Der Abschnitt enthält ausschließlich Metadaten, keine Prinzipien. Format analog Implementation Plan 1.0 und Engineering Specification. |
| **Verifikation** | Ablageort vorhanden ✓ · R0 und R1 dokumentiert ✓ · Kein normativer Gehalt ✓ |
| **Status** | **CLOSED** |

#### W1-M-09 — Interne Traceability

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | Es fehlte eine Abbildung Kernwert → Grundprinzip → Verfassungsartikel; Vollständigkeit und Redundanz waren nicht formal prüfbar. |
| **Änderung** | „Anhang A — Interne Zuordnung" ergänzt, ausdrücklich als deklaratorisch gekennzeichnet, mit zwei Tabellen: A.1 Kernwert → Grundprinzip → Verfassungsartikel (13 Kernwerte) und A.2 Verfassungsartikel → Grundlage (11 Artikel). Ergänzender Hinweis, dass Grundprinzip 5.9 in Vision 3.3 verankert ist und über Artikel 6 wirkt. |
| **Ergebnis der Zuordnung** | Alle 13 Kernwerte sind einem Grundprinzip und mindestens einem Verfassungsartikel zugeordnet. Alle 10 Grundprinzipien sind erfasst. Alle 11 Verfassungsartikel führen auf eine Grundlage im Dokument zurück. **Keine Lücke, kein unverankertes Element.** |
| **Begründung** | Der Anhang enthält keine Prinzipien und begründet keine Pflichten; er weist ausschließlich vorhandene Beziehungen aus. Damit ist die vom Review beanstandete Nichtprüfbarkeit behoben, ohne Inhalt hinzuzufügen. |
| **Verifikation** | 13/13 Kernwerte ✓ · 10/10 Grundprinzipien ✓ · 11/11 Artikel ✓ · Deklaratorisch gekennzeichnet ✓ · Kein neuer Inhalt ✓ |
| **Status** | **CLOSED** |

#### W1-M-10 — Gebundene Domänen ohne Prinzipienanker

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | Rule 2 band Memory Architecture und Runtime Architecture, ohne dass das Dokument dafür einen Bezugspunkt auswies; die Asymmetrie zu Trust, Security, Trading und Infrastructure war unbegründet. |
| **Änderung** | Rule 2 um den Absatz **Geltungsbereich ohne eigenes Prinzipienkapitel** ergänzt: Die Aufzählung ist nicht abschließend; für gebundene Domänen ohne eigenes Kapitel gelten die allgemeinen Kernwerte und Grundprinzipien; einschlägig sind für Memory Architecture 3.3, 4.4, 4.13, 5.9 und 11.2, für Runtime Architecture 4.7, 4.12, 5.8 und 10.7; das Fehlen eines eigenen Kapitels bewirkt keine geringere Bindung. |
| **Gewählte Auflösung** | Von den drei im Review benannten Optionen — Ergänzung eines Kapitels, Streichung aus Rule 2, ausdrückliche Begründung der Asymmetrie — wurde die dritte gewählt. Die erste hätte neue Kapitel und neue Prinzipien erfordert (unzulässig), die zweite hätte den Geltungsbereich von Rule 2 verengt (Governance-Regression). |
| **Verifikation** | Bezugspunkt für beide Domänen ausgewiesen ✓ · Sämtliche genannten Fundstellen bestehen unverändert ✓ · Keine Bindung entfernt ✓ · Kein neues Kapitel ✓ |
| **Status** | **CLOSED** |

#### W1-M-11 — Konformitätsnachweis und Auslegungsinstanz

| Aspekt | Detail |
|---|---|
| **Review-Feststellung** | Rule 2 verlangte Vereinbarkeit ohne Nachweisverfahren; die Schlussbestimmung ordnete die Auflösung von Widersprüchen an, ohne eine zuständige Stelle zu benennen. |
| **Änderung** | Rule 2 um zwei Absätze ergänzt: **Konformitätsnachweis** — jedes gebundene Dokument weist seine Vereinbarkeit ausdrücklich aus; **Auslegung** — über die Auslegung dieses Dokuments und über die Auflösung von Widersprüchen entscheidet die im Dokumentkopf genannte Genehmigungsinstanz. |
| **Begründung** | Beide Ergänzungen bleiben auf Regelebene und benennen kein Verfahren. Die Auslegungszuständigkeit ist identisch mit der Genehmigungszuständigkeit nach Rule 3; damit entsteht keine neue Instanz. |
| **Verifikation** | Nachweispflicht vorhanden ✓ · Auslegungsinstanz benannt ✓ · Keine neue Instanz geschaffen ✓ · Schlussbestimmung unverändert ✓ |
| **Status** | **CLOSED** |

---

### 3.3 Low Findings

#### W1-L-01 — Dopplung 4.10 / 11.6 — CLOSED

Der wiederholende Halbsatz in 11.6 wurde durch einen Verweis ersetzt:
„Komplexität, die den Überblick zerstört, ist kein Fortschritt (siehe 4.10)."
4.10 blieb unverändert, da dort die Erstnennung steht. Kein Gedanke ging
verloren.

#### W1-L-02 — Dopplung 3.1 / 5.8 — CLOSED

Der Satz „Der Kern bleibt klein, stabil und verständlich; Vielfalt entsteht an
den Rändern." wurde in 3.1 gestrichen. 5.8 blieb unverändert, da das Bild dort
normativ verankert ist und 3.1 eine Vision beschreibt. Der verbleibende
Absatz in 3.1 trägt die Aussage zur Erweiterbarkeit unverändert.

#### W1-L-03 — Grenzfälle Lösungsvorwegnahme (4.8, 5.4, 6.2) — **WAIVER**

| Aspekt | Detail |
|---|---|
| **Gegenstand** | 4.8 „Spur … gegen nachträgliche Veränderung zu schützen"; 5.4 „nur so lange wie nötig"; 6.2 „zeitlich begrenzt" |
| **Begründung des Waivers** | Der Review stuft diese Stellen ausdrücklich als Low ein, weil sie als Eigenschaftsanforderung und nicht als Mechanismus formuliert sind. Eine Streichung würde die betroffenen Grundsätze inhaltlich schwächen: 4.8 verlöre die Aussage, dass eine Aufzeichnung nur dann Beweiswert hat, wenn sie nicht nachträglich veränderbar ist; 5.4 verlöre die zeitliche Begrenzung, die den Kern von Least Privilege ausmacht; 6.2 verlöre die Nichtdauerhaftigkeit der kritischen Freigabe. Damit wäre die Grenze zur unzulässigen Änderung der Grundphilosophie überschritten. |
| **Restrisiko** | Gering. Keine der Stellen benennt ein Verfahren, ein Mittel oder eine Umsetzung. Der Gestaltungsraum von Security Architecture und Trust Framework bleibt unberührt. |
| **Entscheidung** | **WAIVER** — Fundstellen bleiben unverändert. Erneute Bewertung nur, falls ein späterer Review sie höher einstuft. |

#### W1-L-04 — Querverbindung 9.6 → 6.2 — CLOSED

9.6 wurde um den Satz ergänzt: „Handlungen mit kritischer Wirkung erfordern
eine kritische Freigabe im Sinne von 6.2." Die Ergänzung stellt eine
Verbindung zwischen bestehenden Bestimmungen her und begründet keine neue
Pflicht; die kritische Freigabe war bereits in 6.2 für Vorgänge dieser Art
vorgesehen.

#### W1-L-05 — Begriff „Cloud" (10.3) — **WAIVER**

| Aspekt | Detail |
|---|---|
| **Gegenstand** | Abschnittsüberschrift 10.3 „Cloud nur wenn notwendig" |
| **Begründung des Waivers** | Der Wortlaut entstammt unverändert dem Erstellungsauftrag für Kapitel 10. Eine Ersetzung wäre eine stilistische Änderung an einer vorgegebenen Prinzipienbezeichnung und damit eine Änderung außerhalb der Findinggrundlage. Der Fließtext des Abschnitts ist bereits technologieneutral formuliert („Externe Infrastruktur wird genutzt, wenn sie einen klaren, sonst nicht erreichbaren Vorteil bietet") und trägt den Grundsatz unabhängig vom Begriff. |
| **Restrisiko** | Gering. „Cloud" bezeichnet ein Betriebsmodell, kein Produkt. Bei einer künftigen Bedeutungsverschiebung bleibt der Grundsatz über den Fließtext anwendbar. |
| **Entscheidung** | **WAIVER** — Fundstelle bleibt unverändert. |

#### W1-L-06 — Normsprache — CLOSED

Abschnitt „Normsprache" in Kapitel 0 ergänzt, mit drei Verbindlichkeitsgraden
(„muss"/„darf niemals"/„ist zu" — unbedingt; „soll" — verbindlich mit
begründeter Abweichung; „sollte" — Zielvorgabe) und der Feststellung, dass die
Verfassungsartikel ausnahmslos unbedingt verbindlich sind. Die vom Review
benannte Stelle 11.5 („sollte … soweit möglich") wurde **nicht** umformuliert:
Sie ist unter der nun definierten Konvention korrekt eingeordnet, und eine
Umformulierung wäre eine Änderung ohne Findingbezug.

---

### 3.4 Editorial Findings

#### W1-E-01 — Referenzen-Tabelle — CLOSED

Referenzen-Abschnitt im Dokumentkopf ergänzt, Format analog Milestone 1.0
Charter. Enthält 13 Einträge mit Status. Ausdrücklich als deklaratorisch
gekennzeichnet, mit Verweis auf Governance Rule 1 (Zusammenhang mit W1-H-03).

#### W1-E-02 — Metadatenfelder — CLOSED

Dokumentkopf um die Felder „Genehmigungsinstanz" (Projekteigner JOCHEN X),
„Genehmigt" (offen, Status DRAFT) und „Vorgängerrevision" ergänzt. Das Feld
„Revision" wurde von R0 auf R1 geführt.

---

## 4. Änderungen ohne Finding-Bezug

**Keine.**

Sämtliche Textstellen des Dokuments, die keinem Finding des W-1 Reviews
zugeordnet sind, wurden nicht berührt. Dies betrifft insbesondere:

| Bereich | Zustand |
|---|---|
| Kapitel 1 Purpose | Unverändert |
| Kapitel 2 Mission | Unverändert |
| Kapitel 3 Vision | Nur 3.1, Dopplungsstreichung (W1-L-02) |
| Kapitel 4 Core Values, 4.1–4.13 | Wertetexte unverändert; nur Vorspann ergänzt (W1-M-01) |
| Kapitel 5 Fundamental Principles | Unverändert |
| Kapitel 6 Trust Model | Nur 6.1 (W1-M-04) und 6.2 (W1-M-03); 6.3 unverändert |
| Kapitel 7 Security Philosophy | Nur 7.1 Absatz 3 (W1-M-02); 7.2–7.9 unverändert |
| Kapitel 8 AI Philosophy | Unverändert |
| Kapitel 9 Trading Philosophy | Nur 9.6, ein ergänzter Satz (W1-L-04); 9.1–9.5 unverändert |
| Kapitel 10 Infrastructure Philosophy | Unverändert |
| Kapitel 11 Evolution Principles | Nur 11.6, Dopplungsstreichung (W1-L-01) |
| Kapitel 12 Non-Negotiable Principles | **Vollständig unverändert** — alle 11 Artikel wortgleich |
| Schlussbestimmung | Unverändert |

---

## 5. Ergebnis

| Kritikalität | Anzahl | CLOSED | WAIVER | OFFEN |
|---|---|---|---|---|
| Critical | 0 | 0 | 0 | 0 |
| High | 3 | 3 | 0 | **0** |
| Medium | 11 | 11 | 0 | **0** |
| Low | 6 | 4 | 2 | **0** |
| Editorial | 2 | 2 | 0 | **0** |
| **Summe** | **22** | **20** | **2** | **0** |

**Sämtliche High Findings sind geschlossen. Es verbleibt kein offenes
Finding.** Die beiden Waiver sind in 3.3 begründet und betreffen ausschließlich
Low-Findings, für die der W-1 Review die Schließung als optional ausweist.

Der Dokumentstatus bleibt **DRAFT**. Die Revision R1 ist für den W-2
Independent Review bereit.

---

**Ende Correction Report R1 (W-2)**
