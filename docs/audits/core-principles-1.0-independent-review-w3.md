# Core Principles 1.0 — Independent Governance Review (W-3)

| Eigenschaft | Wert |
|---|---|
| **Dokumenttyp** | Independent Governance Review — Workflow-Schritt W-3 |
| **Prüfgegenstand** | [JOCHEN X – Core Principles 1.0](../core-principles-1.0.md), **Revision R1**, Status DRAFT, Kapitel 0–12, Schlussbestimmung, Revisionshistorie, Anhang A (1134 Zeilen) |
| **Datum** | 2026-08-07 |
| **Rolle** | Unabhängiger Principal Governance Auditor |
| **Prüfmaßstab** | Prüfziele 1–13 gemäß W-3-Auftrag |
| **Ergebnis** | **REVISION REQUIRED** · 0 Critical, 1 High, 3 Medium, 4 Low, 1 Editorial |
| **Am Prüfgegenstand geändert** | Nichts |

---

# TEIL 1 — Independent Governance Review W-3

## 0. Independence Statement

Die Rolle des unabhängigen Auditors ist durch den W-3-Auftrag zugewiesen. Der
tatsächliche Sachverhalt weicht davon ab und ist offenzulegen:

| Gegenstand | Sachverhalt |
|---|---|
| Erstellung R0 | Dieselbe ausführende Instanz |
| Governance Review W-1 | Dieselbe ausführende Instanz |
| Correction Cycle R1 (W-2) | Dieselbe ausführende Instanz |
| Independent Review W-3 | Dieselbe ausführende Instanz |

**Es liegt keine personelle Unabhängigkeit vor.** Der Bericht ist fachlich
vollwertig, formal eingeschränkt. Er kann die Prüfung durch eine an R0, W-1 und
R1 unbeteiligte Instanz nicht ersetzen.

**Sachliche Absicherung.** Dieser Review wurde ausdrücklich gegen Quellen
außerhalb der vier Prüfdokumente gegengeprüft, soweit dies zur Feststellung von
Widersprüchen zum genehmigten Bestand erforderlich war. Der wesentliche Befund
(W3-H-01) beruht auf einem Abgleich mit **Development Standard v1.1 §3**, den
weder der W-1 Review noch der Correction Cycle R1 vorgenommen haben. Der Befund
widerlegt die Selbstverifikation in Verification Summary R1, Abschnitt 6.

**Am Prüfgegenstand wurde nichts geändert.** Es wurden keine Formulierungen
verbessert, keine Prinzipien vorgeschlagen und keine Kapitel ergänzt.

---

## 1. Prüfgrundlage

| Dokument | Fassung | Verwendung |
|---|---|---|
| [Core Principles 1.0](../core-principles-1.0.md) | R1, DRAFT | Prüfgegenstand |
| [Correction Report R1](core-principles-1.0-correction-report-r1.md) | COMPLETED | Nachweis der Findingzuordnung |
| [Verification Summary R1](core-principles-1.0-verification-summary-r1.md) | VERIFIED | Gegenstand der Nachprüfung |
| [Revision History Update R1](core-principles-1.0-revision-history-update-r1.md) | COMPLETED | Nachweis der Historienführung |

Ergänzend herangezogen zur Konfliktprüfung gegen den genehmigten Bestand:
Development Standard v1.1 §3 (APPROVED), Milestone 1.0 Charter (APPROVED),
Implementation Plan 1.0 (APPROVED, 2026-08-06).

---

## 2. Prüfziel 1 — Dokumentklasse

| Prüfung | Ergebnis | Fundstelle |
|---|---|---|
| Ausschließlich Verfassung | Erfüllt | Kopf „Dokumenttyp"; Dokumentcharakter |
| Keine Architektur | Erfüllt | Prüfziel 12 |
| Keine Engineering Specification | Erfüllt | Dokumentcharakter, negative Klassenbestimmung |
| Keine Implementation | Erfüllt | Prüfziel 12 |
| Keine Technik | Erfüllt | Prüfziel 12 |
| Neu ergänzte Abschnitte klassenkonform | Erfüllt | Kapitel 0 („enthält selbst keine Prinzipien"), Anhang A („deklaratorisch"), Revisionshistorie (Metadaten) |

**Feststellung.** Die Dokumentklasse ist gegenüber R0 unverändert. Die in R1
ergänzten Abschnitte sind sämtlich als nicht-prinzipiell gekennzeichnet. Die
Erweiterung von Kapitel 0 um Auslegungs- und Sprachregeln verändert den
Charakter des Dokuments nicht: Auslegungsregeln bestimmen die Reichweite
vorhandener Bestimmungen, sie begründen keine neuen.

**Prüfziel 1: bestanden.**

---

## 3. Prüfziel 2 — Governance Rules 1–3

### 3.1 Governance Rule 1 — No Retroactive Effect

| Prüfung | Ergebnis |
|---|---|
| Kernaussage erhalten | Erfüllt — Absätze 1–3 wortgleich zu R0 |
| Stichtag bestimmt | Erfüllt — Genehmigungsdatum dieses Dokuments; maßgeblich der Approval Record; Zwischenzeitraum eingeschlossen; Ausschlusssatz vorhanden |
| Geschützter Bestand bestimmbar | Erfüllt — deklaratorische Referenzliste, kein Schutzverlust bei Auslassung |
| Referenzliste sachlich richtig | Erfüllt — 13 Einträge stichprobenartig gegen den Bestand geprüft; Implementation Plan 1.0 (APPROVED 2026-08-06) und Architecture Book v2.0 (FROZEN) korrekt ausgewiesen |
| Schutzwirkung durch R1 verringert | Nein |

**Feststellung:** Rule 1 ist vollständig, in sich schlüssig und ohne
Interpretationsspielraum beim zeitlichen Bezug. Die Konstruktion aus bestimmtem
Stichtag und deklaratorischer Liste ist governance-methodisch korrekt.

### 3.2 Governance Rule 2 — Normative Reference

| Prüfung | Ergebnis |
|---|---|
| Bindungsumfang | Erweitert: zukünftige Versionen bestehender Dokumentklassen ausdrücklich erfasst |
| Domänen ohne eigenes Kapitel | Geregelt — Fundstellen für Memory und Runtime Architecture benannt; Bindung ausdrücklich nicht verringert |
| Konfliktregel | Vorhanden und unverändert |
| Konformitätsnachweis | Vorhanden — **Kompetenzfrage offen, siehe W3-M-03** |
| Auslegungsinstanz | Benannt — identisch mit der Genehmigungsinstanz |

### 3.3 Governance Rule 3 — Controlled Amendment Process

| Prüfung | Ergebnis |
|---|---|
| Genehmigungsinstanz benannt | Erfüllt |
| Verfahrensbestandteile | Sechs Anforderungen, vollständig und prüfbar |
| Selbstbindung | Ausdrücklich geregelt |
| Erhöhte Anforderung Kapitel 0 / 12 | Vorhanden — **wirkt nur dokumentarisch, siehe W3-L-03** |
| Ausschluss stillschweigender Änderung | Unverändert vollständig |
| Regelung der **Erstgenehmigung** | **Nicht geregelt — siehe W3-L-02** |

**Feststellung zu Prüfziel 2:** Die drei Regeln sind untereinander
widerspruchsfrei. Rule 1 (zeitliche Grenze) und Rule 2 (Bindung ab Genehmigung)
greifen lückenlos und überschneidungsfrei ineinander. Rule 3 bindet sich selbst.
Zwei Randfragen bleiben offen (W3-L-02, W3-L-03), eine Kompetenzfrage ist
festzustellen (W3-M-03).

**Prüfziel 2: bestanden mit Findings.**

---

## 4. Prüfziel 3 — Dokumenthierarchie

### 4.1 Formale Prüfung der geforderten Rangfolge

| Rang | Gefordert | In R1 | Abgleich |
|---|---|---|---|
| 1 | Core Principles | Core Principles | ✓ |
| 2 | Architecture Book | Architecture Book | ✓ |
| 3 | ADR | ADRs | ✓ |
| 4 | Engineering Specification | Engineering Specification | ✓ |
| 5 | Implementation Plans | Implementation Plans | ✓ |
| 6 | Implementation | Implementation | ✓ |

Die geforderte Rangfolge ist wortgetreu und vollständig umgesetzt. Wirkung der
Rangordnung, Konfliktregel und Rückwirkungsausschluss sind geregelt.

### 4.2 Widerspruchsfreiheit — dokumentintern

| Prüfpaar | Ergebnis |
|---|---|
| Rangordnung ↔ Rule 1 | Widerspruchsfrei; eigener Absatz, Architecture Book v2.0 namentlich ausgenommen |
| Rangordnung ↔ Rule 2 | Widerspruchsfrei; gleiche Konfliktlogik, unterschiedliche Blickrichtung |
| Rangordnung ↔ Schlussbestimmung | Widerspruchsfrei |
| Rangordnung ↔ Kapitel 12 | Widerspruchsfrei |

### 4.3 Widerspruchsfreiheit — gegen den genehmigten Bestand

**Hier liegt der wesentliche Befund dieses Reviews.**

Development Standard v1.1 (APPROVED) enthält in **§3 Document Hierarchy** eine
eigene Dokumenthierarchie und in **§3.3 Konfliktregel** eine eigene, absteigend
geordnete Rangfolge über neun Dokumenttypen:

| Rang nach DS v1.1 §3.3 | Dokumenttyp | Rang nach Core Principles R1 |
|---|---|---|
| — | Core Principles | 1 |
| 1 | Architecture Book | 2 |
| 2 | ADR | 3 |
| **3** | **Development Standard** | **nicht enthalten** |
| 4 | Engineering Specification | 4 |
| 5 | Review Reports | nicht enthalten |
| 6 | Final Verification Reports | nicht enthalten |
| 7 | Correction Reports | nicht enthalten |
| 8 | Templates | nicht enthalten |
| 9 | Prompts | nicht enthalten |
| — | Implementation Plans | 5 |
| — | Implementation | 6 |

Die relative Ordnung der drei gemeinsam geführten Klassen (Architecture Book →
ADR → Engineering Specification) stimmt überein. Drei Sachverhalte bleiben
jedoch ungeregelt oder gegenläufig:

1. **DS v1.1 §3.3 stellt das Architecture Book an die Spitze.** Core
   Principles R1 stellt sich selbst darüber. Beide Regeln sind nach Rule 1
   gleichzeitig in Kraft — DS v1.1 bleibt unberührt gültig. Ein Anwender, der
   §3.3 folgt, gelangt zu einem anderen Ergebnis als ein Anwender, der der
   Rangordnung in Kapitel 0 folgt.
2. **Der Development Standard ist in der Rangordnung nicht verortet.** Damit
   ist das Verhältnis zwischen Core Principles und demjenigen Dokument
   ungeregelt, das den Review- und Genehmigungsprozess definiert, auf den sich
   Rule 3 stützt.
3. **Fünf weitere in DS §3.3 geführte Dokumenttypen** (Review Reports, Final
   Verification Reports, Correction Reports, Templates, Prompts) fehlen in der
   Rangordnung; umgekehrt fehlen Implementation Plans und Implementation in
   §3.3.

→ **W3-H-01**

**Prüfziel 3: nicht bestanden.**

---

## 5. Prüfziel 4 — Fundamental Principles (Konsistenz)

| Grundprinzip | Wortlaut in R1 | Konsistenzbefund |
|---|---|---|
| Human Authority (5.1) | Unverändert | Konsistent; durch 7.1 und 6.1 zusätzlich abgesichert |
| Security (4.2 / 5.6) | Unverändert | Konsistent; 7.1 auf Systementscheidungen begrenzt |
| Local Sovereignty (5.2) | Unverändert | Konsistent; Reichweite durch die Bestimmung „lokale Vertrauensdomäne" nun bestimmbar |
| Zero Trust (5.3) | Unverändert | Konsistent; 6.1 erstreckt das Vertrauensmodell folgerichtig auf nicht-menschliche Akteure |
| Least Privilege (5.4) | Unverändert | Konsistent |
| Explainability (5.5) | Unverändert | Konsistent; Skalierung erfolgt über den **undefinierten** Begriff „Tragweite" → W3-M-01 |
| Human Confirmation (5.10) | Unverändert | **Spannung zu 6.2 in Verbindung mit 6.1** → W3-M-02 |
| Evolution (5.7) | Unverändert | Konsistent |
| Modularity (5.8) | Unverändert | Konsistent; Streichung der Dopplung in 3.1 ohne Substanzverlust |
| Continuous Learning (5.9) | Unverändert | Konsistent; einziges Grundprinzip ohne Kernwertanker, in Anhang A offengelegt und über Vision 3.3 und Artikel 6 verankert — **kein Finding**, da ausgewiesen |

**Feststellung:** Kein Grundprinzip wurde in R1 im Wortlaut verändert. Zwei
Konsistenzbefunde (W3-M-01, W3-M-02) betreffen das Zusammenwirken mit den in R1
ergänzten Abschnitten, nicht die Prinzipien selbst.

**Prüfziel 4: bestanden mit Findings.**

---

## 6. Prüfziel 5 — Core Values

| Prüfung | Ergebnis |
|---|---|
| Vollständigkeit | 13 von 13 Kernwerten, Reihenfolge und Wortlaut unverändert |
| Konsistenz | Gegeben; kein Wert wurde umgewichtet |
| Prioritätsregeln | Zweistufige Grundregel (Human First → Security First → übrige) plus ausdrückliche Einordnung der bereichsbezogenen Vorrangregeln aus Kapitel 9, 10 und 12 als Konkretisierungen |
| Kollisionsfreiheit | Hergestellt. Die im W-1 Review festgestellte Doppelregelung (W1-M-01) ist aufgelöst: bereichsintern gehen die Konkretisierungen vor, außerhalb gilt Gleichrangigkeit, Kapitel 12 geht allem vor |
| Verankerung | Anhang A weist für alle 13 Kernwerte Grundprinzip und Verfassungsartikel aus; stichprobenartig nachgeprüft, sämtliche Zuordnungen belegbar. Die Zuordnung 4.7 → 5.7 ist die schwächste, bleibt aber vertretbar (Kontinuität als Grundlage von Verlässlichkeit) |

**Prüfziel 5: bestanden.**

---

## 7. Prüfziel 6 — Trust Model

| Prüfung | Ergebnis |
|---|---|
| Keine Rollenmatrix | **Weitgehend erfüllt.** Sämtliche Ressourcen- und Zugriffszuordnungen aus R0 sind entfernt. Die Ebenen sind nun an Wirkungsstufen gebunden. |
| Keine Implementierung | Erfüllt — kein Verfahren, kein Mittel, kein Mechanismus |
| Nur Philosophie | Erfüllt für 6.1 und 6.3; für 6.2 mit Einschränkung |
| Fünf Ebenen erhalten | Erfüllt, unverändert in Anzahl und Bezeichnung |
| Nicht-menschliche Akteure verortet | Erfüllt in 6.1 |

**Zwei Feststellungen.**

1. Der Vorspann von Kapitel 6 erklärt ausdrücklich „keine Rollenmatrix, keine
   **Rechtezuordnung**, keine Umsetzung". 6.2 ordnet jeder Ebene zu, welche
   Wirkungsstufe ihr Vertrauensnachweis trägt. Das ist der Sache nach eine
   abgeschwächte Zuordnung. Die Aussage des Vorspanns ist damit weiter gefasst
   als der Kapitelinhalt sie trägt. → **W3-L-01**

2. Die Erstreckung des Modells auf nicht-menschliche Akteure (6.1) trifft auf
   die Wirkungsstufenzuordnung (6.2) und erzeugt eine Auslegungsfrage gegenüber
   5.10 und 8.5. → **W3-M-02**

**Prüfziel 6: bestanden mit Findings.**

---

## 8. Prüfziel 7 — Security Philosophy

| Prüfung | Ergebnis |
|---|---|
| Keine technischen Lösungen | Erfüllt — kein Verschlüsselungs-, Signatur-, Isolations- oder Prüfkonzept |
| Keine Architektur | Erfüllt |
| Keine Implementierungsdetails | Erfüllt |
| Nur Prinzipien | Erfüllt für 7.1–7.9 |
| Acht Schutzgüter erhalten | Erfüllt, unverändert |
| Änderung in 7.1 | Präzisierung des Adressaten; kein Absenken des Schutzniveaus für Systementscheidungen |

**Zu den bei W-1 festgestellten Grenzfällen (W1-L-03).** Die Fundstellen 4.8,
5.4 und 7.2 („protokollierter Ausnahmefall") sind unverändert. Der im
Correction Report R1 §3.3 dokumentierte Waiver ist nachvollziehbar begründet:
Eine Streichung hätte die betroffenen Grundsätze inhaltlich geschwächt. Der
Waiver wird **akzeptiert**; kein neues Finding.

**Prüfziel 7: bestanden.**

---

## 9. Prüfziel 8 — AI Philosophy

| Prüfung | Ergebnis |
|---|---|
| Keine autonome KI | Erfüllt — 8.5 unverändert; die Autonomiegrenze ist durch die Bestimmung „erhebliche Wirkung" nun bestimmbar und damit nicht mehr durch Auslegung verschiebbar |
| Mensch bleibt oberste Autorität | Erfüllt — 8.6, 5.1, Artikel 1; zusätzlich in 7.1 und 6.1 abgesichert |
| Keine Black Box | Erfüllt — 8.4 unverändert |
| Transparenz und Erklärbarkeit | Erfüllt — 4.5, 4.6, 8.2, 8.4, Artikel 8 |

**Feststellung:** Prüfziel 8 hat sich gegenüber R0 substanziell verbessert. Die
im W-1 Review festgestellte Schwäche — die Autonomiegrenze war an einen
undefinierten Begriff gebunden — ist behoben.

**Prüfziel 8: bestanden.**

---

## 10. Prüfziel 9 — Trading Philosophy

| Prüfung | Fundstelle | Ergebnis |
|---|---|---|
| Simulation vor Realität | 9.1 | Erfüllt, unverändert |
| Paper Trading vor Echtgeld | 9.2 | Erfüllt, unverändert |
| Kapitalerhalt | 9.4 | Erfüllt, unverändert |
| Risikokontrolle vor Gewinn | 9.3 | Erfüllt, unverändert |
| Nachvollziehbarkeit | 9.5 | Erfüllt, unverändert |
| Menschliche Autorisierung | 9.6 | Erfüllt; um den Verweis auf die kritische Freigabe nach 6.2 ergänzt |
| Keine Trading-Algorithmen | Kapitel 9 gesamt | Erfüllt — keine Strategie, kein Verfahren, kein Instrument, keine Kennzahl, keine Börse |

**Feststellung:** Die Ergänzung in 9.6 stellt eine Verbindung zwischen
bestehenden Bestimmungen her und begründet keine neue Pflicht. Sie ist
sachlich zutreffend; ihre Wirkung hängt allerdings von der Auslegung der
Ebenen in 6.2 ab (W3-M-02).

**Prüfziel 9: bestanden.**

---

## 11. Prüfziel 10 — Infrastructure Philosophy

| Prüfung | Ergebnis |
|---|---|
| Keine Hardware | Erfüllt |
| Keine Technologien | Erfüllt |
| Keine Cloud-Architektur | Erfüllt — 10.3 beschreibt eine Nutzungsentscheidung, kein Betriebsmodell und keine Struktur |
| Nur Grundprinzipien | Erfüllt — 10.1 bis 10.7 unverändert |

**Zum Waiver W1-L-05 („Cloud").** Der im Correction Report R1 §3.3 dokumentierte
Waiver ist nachvollziehbar: Der Wortlaut der Abschnittsüberschrift entstammt dem
Erstellungsauftrag, der Fließtext ist technologieneutral formuliert und trägt den
Grundsatz unabhängig vom Begriff. Der Waiver wird **akzeptiert**.

**Prüfziel 10: bestanden.**

---

## 12. Prüfziel 11 — Non-Negotiable Principles

| Prüfung | Ergebnis |
|---|---|
| Wortlaut unverändert | Erfüllt — alle 11 Artikel wortgleich zu R0; durch Zeilenvergleich bestätigt |
| Widerspruchsfreiheit untereinander | Erfüllt — paarweise geprüft, kein Konflikt |
| Widerspruchsfreiheit zu den Kapiteln 1–11 | Erfüllt; die bei W-1 festgestellten Spannungen (Artikel 1 ↔ 7.1; Artikel 10/11 ↔ Kapitel 4) sind aufgelöst |
| Auditierbarkeit | **Hergestellt.** Artikel 4 („kritische Daten", „lokale Vertrauensdomäne") und Artikel 8 („kritische Entscheidung") sind durch die Begriffsbestimmungen erstmals prüfbar. Dies ist die substanziellste Verbesserung der Revision R1. |
| Dauerhafte Gültigkeit | Erfüllt — kein Artikel enthält einen Technologie-, Produkt-, Markt- oder Zeitbezug |
| Änderungsschutz | Vorhanden über Rule 3 einschließlich erhöhter Dokumentationsanforderung; zur Wirkungstiefe siehe W3-L-03 |
| Artikel 3 ↔ 6.1 (nicht-menschliche Akteure) | Widerspruchsfrei — das Innehaben einer Vertrauensebene ist keine Rechteerweiterung |

**Prüfziel 11: bestanden.**

---

## 13. Prüfziel 12 — Technikfreiheit

Vollständige erneute Prüfung des Dokuments in der Fassung R1:

| Kategorie | Befund |
|---|---|
| APIs | Nicht enthalten |
| Klassen | Nicht enthalten |
| Module | Nicht enthalten |
| Datenbanken | Nicht enthalten |
| Programmiersprachen | Nicht enthalten |
| Frameworks | Nicht enthalten |
| Architekturdiagramme | Nicht enthalten |
| Coding | Nicht enthalten |
| Security-Implementierungen | Nicht enthalten; Grenzfälle 4.8, 5.4, 7.2 mit akzeptiertem Waiver |
| Sprintplanung | Nicht enthalten |

**Gezielte Prüfung der in R1 ergänzten Abschnitte:** Referenzen, Stichtag,
Geltungsbereich, Konformitätsnachweis, Auslegung, Rangordnung,
Begriffsbestimmungen, Normsprache, Revisionshistorie und Anhang A enthalten
ausschließlich Governance- und Auslegungsaussagen. Die Begriffsbestimmungen
nennen kein Verfahren, kein Mittel, keinen Schwellwert und keine Metrik; sie
arbeiten mit den Kriterien Reichweite und Umkehrbarkeit, die beide
technologieunabhängig sind.

**Feststellung:** Die Technikfreiheit ist vollständig erhalten. Durch die
Neufassung von 6.2 hat sie sich gegenüber R0 messbar erhöht: Die einzige
Fundstelle mit Ressourcenbezug ist entfallen.

**Prüfziel 12: bestanden.**

---

## 14. Prüfziel 13 — Zukunftssicherheit

| Prüfung | Ergebnis |
|---|---|
| Technologiebezeichnungen | Keine |
| Produkt- oder Herstellernennungen | Keine |
| Bindung an aktuelle Marktverhältnisse oder Rechtslage | Keine |
| Epochengebundene Begriffe | Ein Fall: „Cloud" (10.3), Waiver akzeptiert |
| Auslegungsfestigkeit der Schlüsselbegriffe | **Deutlich verbessert.** Die im W-1 Review benannte Hauptgefahr — schleichender Bedeutungsverlust undefinierter Begriffe über Jahrzehnte — ist für fünf von sechs tragenden Begriffen behoben; für „Tragweite" besteht sie fort (W3-M-01) |
| Fortschreibbarkeit | Hergestellt durch Revisionshistorie und Rule 3 |

**Beobachtung ohne Findingcharakter.** Die Rangordnung in Kapitel 0 bindet das
Dokument an die gegenwärtige Dokumenttaxonomie des Projekts (Architecture Book,
ADR, Engineering Specification, Implementation Plans). Diese Klassenbezeichnungen
sind projekt- und epochengebunden; eine Verfassung ist es nicht. Das ist die
hinzunehmende Folge der von W-1 geforderten Schließung von W1-H-01 und wird
nicht als Finding geführt. Es ist bei einer künftigen Änderung der
Dokumenttaxonomie zu beachten.

**Bewertung:** Das Dokument kann in zehn Jahren als oberste Norm dienen —
**vorbehaltlich der Auflösung von W3-H-01**, da eine Verfassung mit
ungeklärtem Rangverhältnis zum bestehenden Prozessstandard ihre Funktion als
oberste Norm nicht sicher erfüllen kann.

**Prüfziel 13: bestanden mit Vorbehalt.**

---

## 15. Nachprüfung der Verification Summary R1

| Kriterium | Selbstbewertung R1 | Befund W-3 |
|---|---|---|
| V-1 Alle High Findings geschlossen | Erfüllt | **Bestätigt** für W1-H-02 und W1-H-03. Für W1-H-01: die geforderte Rangordnung ist umgesetzt, die Widerspruchsfreiheit gegen den genehmigten Bestand wurde jedoch nicht geprüft → W3-H-01 |
| V-2 Keine neuen Findings | Erfüllt | **Nicht bestätigt.** W3-M-02 ist durch das Zusammenwirken der Korrekturen zu W1-M-03 und W1-M-04 neu entstanden. W3-M-03 ist durch die Korrektur zu W1-M-11 neu entstanden. |
| V-3 Keine Scope-Erweiterung | Erfüllt | Bestätigt |
| V-4 Keine Änderung der Grundphilosophie | Erfüllt | Bestätigt — Kapitel 12 und sämtliche Werte- und Prinzipientexte wortgleich |
| V-5 Keine Governance-Regression | Erfüllt | Bestätigt hinsichtlich Rule 1–3; die Rangordnung erzeugt jedoch eine Regelkonkurrenz zu DS v1.1 §3.3 → W3-H-01 |
| V-6 Dokumentklasse unverändert | Erfüllt | Bestätigt |
| V-7 Technikfreiheit erhalten | Erfüllt | Bestätigt |
| V-8 Hierarchie konsistent | Erfüllt | **Nur dokumentintern bestätigt.** Gegen den genehmigten Bestand nicht erfüllt → W3-H-01 |
| V-9 Rule 1–3 konsistent | Erfüllt | Bestätigt |
| V-10 Dokument bleibt DRAFT | Erfüllt | Bestätigt |

**Feststellung:** Acht von zehn Verifikationskriterien werden bestätigt. V-2 und
V-8 halten der unabhängigen Nachprüfung nicht stand. Die Ursache ist in beiden
Fällen dieselbe: Die Selbstverifikation prüfte gegen den W-1 Review und gegen
das Dokument selbst, nicht gegen den vollständigen genehmigten Bestand.

**Correction Report R1** und **Revision History Update R1** wurden gegen den
Prüfgegenstand abgeglichen. Sämtliche dort behaupteten Änderungen und
Nichtänderungen sind zutreffend; insbesondere die Aussagen „Kapitel 12
vollständig unverändert" und „Kapitel 5 unverändert" wurden bestätigt. Ein
Editorial-Befund betrifft die Revisionshistorie (W3-E-01).

---

# TEIL 2 — Findings Summary

## 2.1 Übersicht

| ID | Kritikalität | Kurzbezeichnung | Prüfziel | Ursprung |
|---|---|---|---|---|
| W3-H-01 | High | Rangordnung steht in Regelkonkurrenz zu Development Standard v1.1 §3.3; Development Standard nicht verortet | 3 | Durch R1 entstanden |
| W3-M-01 | Medium | Begriff „Tragweite" neben der definierten Wirkungsskala unbestimmt | 4, 13 | Rest aus W1-H-02 |
| W3-M-02 | Medium | 6.2 in Verbindung mit 6.1 gegen 5.10 und 8.5 auslegungsoffen | 4, 6 | Durch R1 entstanden |
| W3-M-03 | Medium | Konformitätsnachweis greift in die Zuständigkeit des Development Standard | 2 | Durch R1 entstanden |
| W3-L-01 | Low | Vorspann Kapitel 6 („keine Rechtezuordnung") weiter gefasst als 6.2 trägt | 6 | Durch R1 entstanden |
| W3-L-02 | Low | Erstgenehmigung nicht geregelt; Verweis auf Rule 3 (Amendment) | 2 | Rest aus W1-M-07 |
| W3-L-03 | Low | „Erhöhte Anforderung" wirkt dokumentarisch, nicht als Genehmigungshürde | 2, 11 | Rest aus W1-M-07 |
| W3-L-04 | Low | Normsprache erfasst indikativisch formulierte Bestimmungen nicht | 2 | Rest aus W1-L-06 |
| W3-E-01 | Editorial | Revisionshistorie führt für R0 kein Prüfartefakt, obwohl R0 durch W-1 geprüft wurde | 2 | Durch R1 entstanden |

**Verteilung:** 0 Critical · 1 High · 3 Medium · 4 Low · 1 Editorial

## 2.2 High Finding

### W3-H-01 — Regelkonkurrenz der Dokumenthierarchie

| Aspekt | Detail |
|---|---|
| **Fundstelle** | Kapitel 0, „Dokumenteinordnung und Dokumenthierarchie", Abschnitte „Rangordnung" und „Wirkung der Rangordnung" |
| **Gegenstück** | Development Standard v1.1 (APPROVED), §3 Document Hierarchy, §3.3 Konfliktregel |
| **Sachverhalt** | Der Development Standard v1.1 enthält bereits eine Konfliktregel über neun Dokumenttypen und stellt das Architecture Book an die Spitze. Core Principles R1 führt eine zweite Rangordnung ein, stellt sich selbst an die Spitze und verortet den Development Standard überhaupt nicht. Beide Regeln stehen nach Governance Rule 1 gleichzeitig in Kraft, da Rule 1 die Gültigkeit des Development Standard ausdrücklich unberührt lässt. |
| **Widerspruch** | Für die Frage „welches Dokument ist die oberste Norm" liefern die beiden Regeln unterschiedliche Antworten. Ein Anwender, der DS §3.3 folgt, gelangt zum Architecture Book; ein Anwender, der Kapitel 0 folgt, gelangt zu den Core Principles. Das Dokument regelt nicht, welche Regel vorgeht. |
| **Zusätzliche Lücke** | Das Verhältnis der Core Principles zum Development Standard ist ungeregelt. Das betrifft gerade dasjenige Dokument, das den Review- und Genehmigungsprozess definiert, auf den sich Governance Rule 3 stützt. Fünf in DS §3.3 geführte Dokumenttypen fehlen in der Rangordnung; zwei in der Rangordnung geführte Typen fehlen in §3.3. |
| **Begründung der Kritikalität** | Der Zweck des Dokuments ist, oberste Norm zu sein. Eine zweite, gleichzeitig gültige Rangordnung mit abweichender Spitze hebt diesen Zweck in der praktischen Anwendung auf. Die Korrektur zu W1-H-01 hat den dokumentinternen Mangel behoben und dabei einen dokumentübergreifenden erzeugt. Betroffen ist ein APPROVED-Artefakt. |
| **Governance-Auswirkung** | Kein bestehendes Artefakt wird ungültig — Rule 1 wirkt. Es entsteht jedoch eine Regelkonkurrenz, die bei jeder künftigen Konfliktentscheidung zwei begründbare Ergebnisse zulässt. Solange sie besteht, ist die Rangordnung nicht durchsetzbar. |
| **Ausdrücklich nicht Gegenstand dieses Reviews** | Die Auflösung. Ob sie durch Verortung des Development Standard, durch Verweis auf DS §3.3, durch eine Vorrangklausel oder durch eine Änderung des Development Standard erfolgt, ist eine Entscheidung der Genehmigungsinstanz und Gegenstand eines Correction Cycle. Dieser Review schlägt keine Formulierung vor. |
| **Status** | OPEN |

## 2.3 Medium Findings

### W3-M-01 — Begriff „Tragweite" unbestimmt

| Aspekt | Detail |
|---|---|
| **Fundstelle** | 5.5, 6.3, 7.8, 8.4 |
| **Sachverhalt** | R1 führt in Kapitel 0 eine dreistufige Wirkungsskala ein (bedeutsam, erheblich, kritisch) und bestimmt fünf tragende Begriffe. An vier Stellen skaliert das Dokument Pflichten jedoch weiterhin über den Begriff „Tragweite", der nicht bestimmt ist und in keinem ausgewiesenen Verhältnis zur Wirkungsskala steht. Betroffen sind der Erklärungsaufwand (5.5), der Nachweisaufwand im Vertrauensmodell (6.3) und die Grenze zulässiger Undurchsichtigkeit (8.4). |
| **Begründung** | Der W-1 Review verlangte die Bestimmung **aller** tragenden normativen Begriffe. Für die fünf namentlich benannten ist die Anforderung erfüllt. Ein synonym verwendeter, ebenso tragender Begriff bleibt unbestimmt; damit besteht der Auslegungsspielraum, den W1-H-02 schließen sollte, an vier Stellen fort. |
| **Abgrenzung** | Kein Widerspruch, sondern eine Bestimmtheitslücke. W1-H-02 gilt für seinen benannten Umfang als geschlossen. |
| **Status** | OPEN |

### W3-M-02 — Vertrauensebenen und Bestätigungsvorbehalt auslegungsoffen

| Aspekt | Detail |
|---|---|
| **Fundstelle** | 6.1 Absatz 3, 6.2 („Benutzer", „Verifizierter Benutzer"), 5.10, 8.5 |
| **Sachverhalt** | 6.1 erstreckt das Vertrauensmodell auf nicht-menschliche Akteure (Erweiterung, Dienst, Stellvertreter). 6.2 bestimmt für den Verifizierten Benutzer: „Sein Vertrauensnachweis trägt Handlungen mit erheblicher Wirkung." 5.10 bestimmt: Handlungen mit erheblicher Wirkung „erfordern eine ausdrückliche menschliche Bestätigung". 8.5 lässt Autonomie nur für Vorgänge ohne erhebliche Wirkung zu. Für einen nicht-menschlichen Akteur auf der Ebene „Verifizierter Benutzer" lassen sich beide Lesarten begründen: Der Vertrauensnachweis genügt für solche Handlungen — oder er genügt nur als Identitätsnachweis, während die Bestätigungspflicht nach 5.10 unberührt bleibt. |
| **Begründung** | Beide Fundstellen sind Ergebnis der Korrekturen zu W1-M-03 (Neufassung 6.2) und W1-M-04 (Erstreckung 6.1). Einzeln sind beide unbedenklich; ihr Zusammenwirken erzeugt eine Auslegungsfrage, die es in R0 nicht gab. Die Auslegungsregel in Kapitel 0 hilft nicht, da sie die Wirkungsstufe bestimmt, nicht die Berechtigungsfolge. |
| **Tragweite** | Betrifft die Reichweite von Human Confirmation (5.10) und die Autonomiegrenze (8.5) — beides Kernbestandteile der AI Philosophy. Artikel 1 bleibt unberührt, da er auf die letzte Entscheidung des Menschen abstellt. |
| **Einordnung** | **Neu durch R1 entstanden.** Die Aussage „Keine neuen Findings" in Verification Summary R1 (V-2) ist insoweit unzutreffend. |
| **Status** | OPEN |

### W3-M-03 — Konformitätsnachweis greift in fremde Zuständigkeit

| Aspekt | Detail |
|---|---|
| **Fundstelle** | Governance Rule 2, Absatz „Konformitätsnachweis" |
| **Gegenstück** | Development Standard v1.1 §3.2 (APPROVED) |
| **Sachverhalt** | Rule 2 verpflichtet jedes gebundene Dokument, seine Vereinbarkeit ausdrücklich auszuweisen. Das ist eine Anforderung an die Struktur und den Pflichtinhalt anderer Dokumente. DS v1.1 §3.2 weist die Zuständigkeit für „Prozess, Governance, Templates, Review-Regeln" dem Development Standard zu und untersagt anderen Dokumentklassen ausdrücklich, Prozesse zu definieren. |
| **Begründung** | Die Anforderung ist inhaltlich sachgerecht und schließt W1-M-11 wirksam. Sie ist jedoch eine Prozessvorgabe und damit ihrer Art nach dem Development Standard zugeordnet. Ohne Klärung des Rangverhältnisses (W3-H-01) ist offen, ob die Core Principles eine solche Vorgabe setzen dürfen. |
| **Abhängigkeit** | Fällt mit der Auflösung von W3-H-01 möglicherweise weg. Getrennt geführt, weil es eine eigenständige Zuständigkeitsfrage betrifft. |
| **Status** | OPEN |

## 2.4 Low Findings

| ID | Fundstelle | Sachverhalt | Begründung |
|---|---|---|---|
| W3-L-01 | Kapitel 6, Vorspann gegen 6.2 | Der Vorspann erklärt „keine Rollenmatrix, keine Rechtezuordnung, keine Umsetzung". 6.2 ordnet jeder Ebene die von ihrem Vertrauensnachweis getragene Wirkungsstufe zu. | Die Selbstbeschreibung ist absoluter formuliert, als der Kapitelinhalt sie trägt. Keine normative Wirkung; die Zuordnung selbst ist philosophieebene und gegenüber R0 deutlich zurückgenommen. |
| W3-L-02 | Dokumentcharakter „Geltungsvorbehalt"; Kopffeld „Gültigkeit"; Kapitel 0 Vorspann | Alle drei Stellen knüpfen die Bindungswirkung an eine „Genehmigung nach Governance Rule 3". Rule 3 ist ausweislich ihrer Überschrift und ihres Inhalts ein **Amendment**-Verfahren; die Erstgenehmigung dieses Dokuments regelt sie nicht. | Zirkelbezug ohne praktische Folge, da die Genehmigungsinstanz benannt ist und das Projekt einen etablierten Genehmigungsweg (Approval Record) führt. |
| W3-L-03 | Rule 3, Absatz „Erhöhte Anforderung" | Für Kapitel 0 und Kapitel 12 verlangt die Regel zusätzliche **Angaben** (betroffene Regel oder Artikel, Folgen). Eine erhöhte **Genehmigungshürde** — etwa unabhängige Prüfung oder gesonderte Entscheidung — besteht nicht. | W1-M-07 ist formal geschlossen. In der Sache bleiben die Verfassungsartikel mit demselben Verfahren änderbar wie jede andere Bestimmung; die Erhöhung wirkt allein dokumentarisch. |
| W3-L-04 | Kapitel 0, „Normsprache"; Kapitel 1–11 | Die Konvention bestimmt drei modale Verbindlichkeitsgrade. Der überwiegende Teil der Kapitel 1–11 ist indikativisch formuliert („Das System schützt seine eigene Integrität", „Externe Systeme sind Gäste"). Für diese Aussagen bestimmt die Konvention keinen Verbindlichkeitsgrad. | W1-L-06 ist für die modalen Formen geschlossen. Für den größeren, indikativisch formulierten Teil des Dokuments bleibt der Verbindlichkeitsgrad unbestimmt. |

## 2.5 Editorial Finding

| ID | Fundstelle | Sachverhalt |
|---|---|---|
| W3-E-01 | Revisionshistorie, Zeile R0, Spalte „Prüfartefakt" | Der Eintrag lautet „—". Tatsächlich ist der Governance Review W-1 das Prüfartefakt zu R0; er ist im Kopffeld „Vorgängerrevision" auch als solcher benannt. Die Historie ist insoweit unvollständig gegenüber ihrer eigenen Vorgabe („Jede Änderung … mit Auslöser, Umfang und Prüfartefakt zu führen"). |

## 2.6 Bestätigte Schließungen aus W-1

| W-1 Finding | Befund W-3 |
|---|---|
| W1-H-01 | Rangordnung umgesetzt; **dokumentübergreifend nicht abgeschlossen** → W3-H-01 |
| W1-H-02 | **Geschlossen** für die fünf benannten Begriffe; Rest → W3-M-01 |
| W1-H-03 | **Geschlossen** — ohne Einschränkung |
| W1-M-01 | **Geschlossen** |
| W1-M-02 | **Geschlossen** |
| W1-M-03 | **Geschlossen**; Restbefund → W3-L-01, Wechselwirkung → W3-M-02 |
| W1-M-04 | **Geschlossen**; Wechselwirkung → W3-M-02 |
| W1-M-05 | **Geschlossen** |
| W1-M-06 | **Geschlossen** |
| W1-M-07 | **Geschlossen**; Restbefunde → W3-L-02, W3-L-03 |
| W1-M-08 | **Geschlossen**; Editorial → W3-E-01 |
| W1-M-09 | **Geschlossen** — Anhang A vollständig und belegbar |
| W1-M-10 | **Geschlossen** |
| W1-M-11 | **Geschlossen**; Zuständigkeitsfrage → W3-M-03 |
| W1-L-01, W1-L-02, W1-L-04, W1-L-06 | **Geschlossen**; Rest zu L-06 → W3-L-04 |
| W1-L-03, W1-L-05 | **Waiver akzeptiert** |
| W1-E-01, W1-E-02 | **Geschlossen** |

**Bilanz:** 20 von 22 W-1-Findings sind geschlossen, 2 mit akzeptiertem Waiver.
Ein High Finding ist nur dokumentintern geschlossen. Aus den Korrekturen sind
vier neue Findings entstanden (W3-H-01, W3-M-02, W3-M-03, W3-E-01).

---

# TEIL 3 — Review Decision

## 3.1 Entscheidung

> ## REVISION REQUIRED

## 3.2 Begründung

Die Entscheidung stützt sich auf zwei Sachverhalte, die einzeln jeweils
genügen würden.

**Erstens — W3-H-01.** Die Revision R1 wurde ausgelöst durch drei High
Findings, von denen W1-H-01 (Dokumenthierarchie) das zentrale war. Die
Korrektur setzt die geforderte Rangordnung wortgetreu um und ist dokumentintern
widerspruchsfrei. Sie wurde jedoch nicht gegen den genehmigten Bestand geprüft.
Development Standard v1.1 §3.3 — APPROVED, durch Governance Rule 1 ausdrücklich
in Kraft belassen — enthält eine eigene Konfliktregel, die das Architecture Book
an die Spitze stellt und den Development Standard über die Engineering
Specification. Die Core Principles verorten sich über allem und den Development
Standard gar nicht. Damit existieren zwei gleichzeitig gültige Rangordnungen mit
unterschiedlicher Spitze. Ein Dokument, dessen erklärter Zweck es ist, oberste
Norm zu sein, kann diesen Zweck mit einer ungeklärten Regelkonkurrenz nicht
erfüllen. Der Mangel betrifft genau die Korrektur, deretwegen die Revision
durchgeführt wurde.

**Zweitens — die Selbstverifikation trägt nicht.** Verification Summary R1
bewertet V-2 („Keine neuen Findings") und V-8 („Hierarchie konsistent") als
erfüllt. Beide Bewertungen halten der unabhängigen Nachprüfung nicht stand:
Aus dem Zusammenwirken der Korrekturen zu W1-M-03 und W1-M-04 ist W3-M-02
entstanden, aus der Korrektur zu W1-M-11 ist W3-M-03 entstanden, und die
Hierarchiekonsistenz wurde ausschließlich dokumentintern geprüft. Der
Correction Cycle stand unter der ausdrücklichen Auflage, dass keine neuen
Medium Findings entstehen dürfen. Diese Auflage ist nicht eingehalten.

## 3.3 Was die Entscheidung ausdrücklich nicht bedeutet

| Aussage | Klarstellung |
|---|---|
| Die Revision R1 sei gescheitert | Nein. 20 von 22 Findings sind belastbar geschlossen. Die Verbesserung gegenüber R0 ist erheblich, insbesondere bei Auditierbarkeit (Artikel 4, 8), Bestandsschutz (Rule 1) und Technikfreiheit (6.2). |
| Das Dokument stehe im Widerspruch zu seiner Grundphilosophie | Nein. Kapitel 12 und sämtliche Werte- und Prinzipientexte sind wortgleich erhalten. |
| Eine Neufassung sei erforderlich | Nein. Alle Findings sind durch punktuelle Präzisierung schließbar. |
| Ein genehmigtes Artefakt sei durch R1 ungültig geworden | Nein. Governance Rule 1 wirkt; kein APPROVED- oder FROZEN-Artefakt ist berührt. |
| Kapitel müssten ergänzt oder umstrukturiert werden | Nein. Dieser Review schlägt weder Formulierungen noch Strukturänderungen vor. |

## 3.4 Bedingungen für eine Freigabe in R2

| Nr. | Bedingung |
|---|---|
| B-1 | W3-H-01 geschlossen: Verhältnis der Rangordnung zu Development Standard v1.1 §3.3 geklärt und der Development Standard verortet |
| B-2 | W3-M-01 geschlossen: „Tragweite" bestimmt oder auf die Wirkungsskala zurückgeführt |
| B-3 | W3-M-02 geschlossen: Verhältnis von 6.2 zu 5.10 und 8.5 für nicht-menschliche Akteure eindeutig |
| B-4 | W3-M-03 entschieden: Zuständigkeit für den Konformitätsnachweis geklärt oder als Folge von B-1 erledigt |
| B-5 | Low- und Editorial-Findings geschlossen oder mit dokumentiertem Waiver versehen |
| B-6 | Correction Report R2 mit Finding-für-Finding-Nachweis; erneuter Independent Review (W-4) |
| B-7 | Der Independent Review W-4 sollte durch eine an R0, W-1, R1 und W-3 unbeteiligte Instanz erfolgen. Die Entscheidung hierüber liegt bei der Genehmigungsinstanz und ist im Approval Record zu dokumentieren. |

---

# TEIL 4 — Review Readiness Assessment

## 4.1 Reifegradbewertung

| Dimension | Bewertung | Begründung |
|---|---|---|
| Dokumentklasse | **Reif** | Eindeutig, doppelt bestimmt, in R1 zusätzlich abgesichert |
| Grundphilosophie | **Reif** | Vollständig, kollisionsfrei, unverändert |
| Begriffliche Bestimmtheit | **Weitgehend reif** | Fünf von sechs tragenden Begriffen bestimmt; „Tragweite" offen |
| Innere Widerspruchsfreiheit | **Weitgehend reif** | Eine Auslegungsfrage offen (W3-M-02) |
| Auditierbarkeit | **Reif** | Artikel 4 und 8 erstmals prüfbar; Anhang A vollständig |
| Bestandsschutz | **Reif** | Rule 1 ohne Interpretationsspielraum |
| Änderungsschutz | **Weitgehend reif** | Instanz, Verfahren und Selbstbindung vorhanden; Erstgenehmigung und Hürdentiefe offen |
| Technikfreiheit | **Reif** | Vollständig; gegenüber R0 verbessert |
| Zukunftssicherheit | **Weitgehend reif** | Deutlich verbessert; Taxonomiebindung zu beachten |
| **Hierarchische Verortung** | **Nicht reif** | W3-H-01 |
| Externe Konsistenz | **Nicht geprüft in R1** | Erstmals in W-3 geprüft; Ergebnis W3-H-01 |

## 4.2 Readiness Level

| Stufe | Kriterium | Erreicht |
|---|---|---|
| RL-0 | Entwurf vorhanden | Ja (R0) |
| RL-1 | Vollständig gegenüber Erstellungsauftrag | Ja (R0) |
| RL-2 | Dokumentintern widerspruchsfrei und begrifflich bestimmt | **Weitgehend** (R1) |
| RL-3 | Widerspruchsfrei gegen den genehmigten Bestand | **Nein** |
| RL-4 | Unabhängig geprüft | Formal nein (siehe Abschnitt 0) |
| RL-5 | Genehmigt | Nein |

**Erreichter Reifegrad: RL-2 (weitgehend). RL-3 nicht erreicht.**

## 4.3 Aufwandseinschätzung für R2

| Finding | Erwarteter Umfang |
|---|---|
| W3-H-01 | Eine Bestimmung in Kapitel 0; ggf. Abstimmung mit Development Standard v1.1 durch die Genehmigungsinstanz |
| W3-M-01 | Ein Eintrag in den Begriffsbestimmungen oder Rückführung der vier Fundstellen |
| W3-M-02 | Eine klarstellende Bestimmung in Kapitel 6 |
| W3-M-03 | Entscheidung der Genehmigungsinstanz; ggf. keine Textänderung |
| W3-L-01 bis W3-L-04, W3-E-01 | Punktuell |

Keine Änderung erfordert eine Strukturänderung der Kapitel 1–12 oder eine
Änderung der Grundphilosophie. Ein Correction Cycle R2 vergleichbaren Umfangs
wie R1 ist nicht erforderlich.

## 4.4 Empfohlene Folgeschritte

| Schritt | Gegenstand |
|---|---|
| 1 | Entscheidung der Genehmigungsinstanz über W3-H-01 und W3-M-03 |
| 2 | Correction Cycle R2 (W-4) — ausschließlich Schließung der W-3-Findings |
| 3 | Correction Report R2, Verification Summary R2, Revision History Update R2 |
| 4 | Independent Review W-5, vorzugsweise durch eine unbeteiligte Instanz |
| 5 | Approval Record — erst nach W-5 |

## 4.5 Governance-Auswirkungen bis zur Freigabe

| Sachverhalt | Bewertung |
|---|---|
| Wirkung auf genehmigte Artefakte | Keine. Rule 1 wirkt; Status DRAFT; Geltungsvorbehalt vorhanden. |
| Wirkung auf laufende Arbeiten | Keine. |
| Normatives Vakuum | Besteht fort. Solange das Dokument DRAFT ist, existiert für neu beginnende Architekturarbeit kein normativer Rahmen. Der bereits im W-1 Review erhobene Hinweis, die DRAFT-Phase kurz zu halten oder nachgelagerte Architekturdokumente zurückzustellen, bleibt aufrecht. |
| Risiko durch W3-H-01 vor Genehmigung | Kein akutes. Die Regelkonkurrenz entsteht erst mit der Genehmigung. |

---

**Ende Core Principles 1.0 — Independent Governance Review (W-3)**
