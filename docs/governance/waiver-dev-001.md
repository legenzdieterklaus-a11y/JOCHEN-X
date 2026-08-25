# Governance Waiver DEV-001

| Feld              | Wert                                                             |
|-------------------|------------------------------------------------------------------|
| Waiver-ID         | WAIVER-DEV-001                                                   |
| Titel             | Zuweisung von Delta Analysis und Module Work Breakdown an den Implementation Plan 1.0 |
| Status            | **APPROVED**                                                     |
| Datum             | 2026-08-02                                                       |
| Auslöser          | Independent Governance Review — Finding F-001 (Critical)         |
| Autorität         | Governance Architect, Independent Review                         |

---

## 1. Referenzen

| Dokument                                        | Status      | Relevanz                                      |
|-------------------------------------------------|-------------|-----------------------------------------------|
| Development Standard v1.1                       | APPROVED    | §6.2 Normative Struktur — 15 Pflichtabschnitte |
| Milestone 1.0 Charter                           | APPROVED    | §8 Zweistufiger Governance-Prozess             |
| Milestone 1.0 Charter Approval Record           | APPROVED    | Implementation Authorization nur für ES-Phase  |
| Engineering Specification 1.0, Revision R1      | IN REVIEW   | Prüfgegenstand, §16.11 Option A               |
| Independent Governance Review ES-1.0 R1         | COMPLETED   | Finding F-001 (Critical), F-002 (Medium)       |
| Architecture Book v2.0                          | FROZEN      | Nicht betroffen                                |
| Bootstrap Baseline 1.0                          | APPROVED    | Nicht betroffen                                |

---

## 2. Problem Statement

Der Development Standard v1.1 §6.2 definiert 15 Pflichtabschnitte für eine Engineering
Specification. Darunter:

- **§6.2 #4 — Delta Analysis**: Exakte Differenz zwischen Baseline und Zielzustand pro Datei
- **§6.2 #5 — Module Work Breakdown**: Pro Datei konkrete Änderungen mit Codebeispielen

Der Milestone 1.0 Charter §8 etabliert einen zweistufigen Governance-Prozess:

1. **Engineering Specification** — Vertraglicher Rahmen (Scope, Requirements, Acceptance Criteria)
2. **Implementation Plan** — Strukturierter Umsetzungsplan mit Abhängigkeiten und Reihenfolge

Diese zwei Vorgaben stehen in einem Zielkonflikt:

- Der Development Standard setzt einen einstufigen Prozess voraus, in dem alle 15 Abschnitte
  in der Engineering Specification stehen.
- Der Charter separiert den vertraglichen Rahmen (ES) von der Umsetzungsplanung
  (Implementation Plan) in zwei unabhängige Governance-Artefakte.

Die Engineering Specification 1.0 R1 dokumentiert diesen Konflikt als DEV-001 (Critical) in
ihrem Deviation Register (§16.12). Das Independent Review bestätigt den Befund als F-001
und empfiehlt Option A — die Genehmigung der Abweichung.

Die Engineering Specification kann diesen Governance-Konflikt nicht eigenständig auflösen, da
er zwischen zwei höherrangigen Dokumenten besteht.

---

## 3. Decision

**Die Abweichung wird genehmigt (Option A gemäß ES §16.11).**

Die Pflichtabschnitte Delta Analysis (§6.2 #4) und Module Work Breakdown (§6.2 #5) werden
für Milestone 1.0 dem Implementation Plan 1.0 zugewiesen.

### 3.1 Verbindliche Festlegungen

1. **Die Engineering Specification 1.0 bleibt unverändert.**
   Keine inhaltlichen Änderungen am Dokument als Folge dieses Waivers.

2. **Der Milestone 1.0 Charter bleibt unverändert.**
   Keine Modifikation des genehmigten Charter-Textes.

3. **Der Development Standard v1.1 bleibt unverändert.**
   Keine Versionsänderung des Development Standard als Folge dieses Waivers.

4. **Delta Analysis wird verpflichtender Bestandteil des Implementation Plans 1.0.**
   Der Implementation Plan MUSS eine vollständige Delta Analysis gemäß Development
   Standard v1.1 §6.2 #4 enthalten.

5. **Module Work Breakdown wird verpflichtender Bestandteil des Implementation Plans 1.0.**
   Der Implementation Plan MUSS ein vollständiges Module Work Breakdown gemäß Development
   Standard v1.1 §6.2 #5 enthalten.

### 3.2 Geltungsbereich

Dieser Waiver gilt ausschließlich für Milestone 1.0. Er begründet keinen Präzedenzfall für
zukünftige Milestones. Jeder weitere Milestone mit zweistufigem Governance-Prozess erfordert
eine eigene Governance-Entscheidung zur Verteilung der Pflichtabschnitte.

---

## 4. Rationale

### 4.1 Charter-Autorität

Der Milestone 1.0 Charter ist das höchstrangige milestone-spezifische Governance-Dokument.
Er wurde am 2026-08-02 nach zwei Review-Runden genehmigt (Charter Approval Record). Der
Charter §8 etabliert den zweistufigen Prozess als bewusste Governance-Entscheidung — nicht
als Auslassung.

### 4.2 Inhaltliche Zugehörigkeit

Die betroffenen Abschnitte sind implementierungsnah:

- **Delta Analysis** erfordert Dateireferenzen (Datei, Zeile, Status) und beschreibt den
  exakten Änderungsumfang pro Datei. Dies setzt die Kenntnis konkreter Implementierungs-
  entscheidungen voraus.
- **Module Work Breakdown** erfordert Codebeispiele und dateibasierte Änderungsbeschreibungen.
  Dies ist Umsetzungsplanung, nicht vertragliche Spezifikation.

Beide Abschnitte gehören sachlich in den Implementation Plan, nicht in den vertraglichen
Rahmen der Engineering Specification.

### 4.3 ES-Selbstbeschränkung

Die Engineering Specification definiert sich in §1.5 als Implementation Contract, der Scope,
Requirements und Acceptance Criteria festlegt — nicht die Umsetzungsdetails. Diese
Selbstbeschränkung ist konsistent mit dem Charter Approval Record, der die Implementation
Authorization ausschließlich für die Engineering Specification Phase erteilt.

### 4.4 Konfliktregel

Gemäß Development Standard v1.1 §3.3 hat der Development Standard Vorrang vor der
Engineering Specification. Allerdings fügt die ES §2.2 den Charter als milestone-bindendes
Artefakt zwischen Development Standard und Engineering Specification ein — eine Erweiterung,
die der Independent Review als F-003 (Low) dokumentiert. Der vorliegende Waiver löst den
Rangkonflikt formal auf, ohne die bestehende Hierarchie zu ändern.

---

## 5. Scope

### 5.1 Betroffen

| Element                              | Auswirkung                                           |
|--------------------------------------|------------------------------------------------------|
| Delta Analysis (Dev Standard §6.2 #4) | Verpflichtend im Implementation Plan statt in der ES |
| Module Work Breakdown (Dev Standard §6.2 #5) | Verpflichtend im Implementation Plan statt in der ES |
| DEV-001 (ES §16.12)                 | Status: Geschlossen (Waiver genehmigt)               |
| DEV-002 (ES §16.12)                 | Status: Geschlossen (Dateireferenzen im IP)          |
| E-21, E-22 (ES §20.4)              | Open Blocker aufgelöst                               |

### 5.2 Nicht betroffen

| Element                              | Begründung                                           |
|--------------------------------------|------------------------------------------------------|
| Engineering Specification 1.0 R1     | Keine inhaltliche Änderung                           |
| Milestone 1.0 Charter                | Keine Änderung                                       |
| Development Standard v1.1            | Keine Versionsänderung                               |
| Architecture Book v2.0               | Nicht betroffen (Architektur-Freeze)                 |
| Bootstrap Baseline 1.0               | Nicht betroffen                                      |
| Functional Requirements FR-001..014  | Unverändert                                          |
| Non-Functional Requirements NFR-001..010 | Unverändert                                       |
| Acceptance Criteria AC-001..014      | Unverändert                                          |
| Work Packages WP-001..007            | Unverändert                                          |
| Quality Gates QG-001..008            | Unverändert                                          |
| Engineering Goals EG-001..007        | Unverändert                                          |
| Deliverables D-001..010              | Unverändert                                          |

---

## 6. Impact Assessment

### 6.1 Auswirkungen auf die Governance-Kette

| Phase                          | Auswirkung                                               |
|--------------------------------|----------------------------------------------------------|
| Engineering Specification      | Keine. Genehmigungsfähig nach diesem Waiver.             |
| Implementation Plan 1.0       | Erweitert: MUSS Delta Analysis und Module Work Breakdown enthalten. |
| Independent Review (IP)        | Review des Implementation Plans MUSS die Vollständigkeit der zugewiesenen Abschnitte prüfen. |
| Sprint Implementation          | Keine. Arbeitet auf Basis des Implementation Plans.      |
| Milestone Review               | Keine. Prüft gegen Acceptance Criteria und Quality Gates. |

### 6.2 Auswirkungen auf den Development Standard

Der Development Standard v1.1 bleibt formal unverändert. Dieser Waiver dokumentiert eine
milestone-spezifische Abweichung, keine generelle Änderung der Normativstruktur.

Empfehlung für zukünftige Revisionen: Eine Version v1.2 des Development Standard sollte den
zweistufigen Governance-Prozess als explizite Option in §6.2 aufnehmen und die Verteilung
der 15 Pflichtabschnitte auf Engineering Specification und Implementation Plan regeln.
Dies beseitigt die Ursache des Governance-Konflikts dauerhaft (Option B aus ES §16.11).

### 6.3 Auswirkungen auf den Independent Review

Der Independent Governance Review ES-1.0 R1 identifizierte fünf Findings:

| Finding | Schweregrad | Auswirkung dieses Waivers                                |
|---------|-------------|-----------------------------------------------------------|
| F-001   | Critical    | **Adressiert.** DEV-001 durch Waiver aufgelöst.           |
| F-002   | Medium      | **Adressiert.** DEV-002 aufgelöst (Dateireferenzen im IP). |
| F-003   | Low         | Unverändert. Empfehlung für Dev Standard v1.2.            |
| F-004   | Low         | Unverändert. Performance-Messmethodik im IP definieren.   |
| F-005   | Editorial   | Unverändert. Keine Korrektur erforderlich.                |

---

## 7. Risk Assessment

### 7.1 Risiken des Waivers

| ID   | Risiko                                    | Wahrscheinlichkeit | Auswirkung | Mitigation                      |
|------|-------------------------------------------|---------------------|------------|----------------------------------|
| WR-1 | Implementation Plan vergisst zugewiesene Abschnitte | Niedrig | Hoch | Closing Criteria (§9) erzwingen Vollständigkeitsprüfung |
| WR-2 | Waiver wird als Präzedenzfall missbraucht | Niedrig | Mittel | §3.2 begrenzt Geltung auf Milestone 1.0 |
| WR-3 | Governance-Lücke zwischen ES und IP       | Niedrig | Mittel | ES Deliverable D-008 definiert IP als Pflicht-Lieferobjekt |
| WR-4 | Dev Standard §6.2 Konformitätsprüfung schlägt fehl | Niedrig | Niedrig | Waiver dokumentiert die genehmigte Abweichung |

### 7.2 Risiken ohne Waiver

| ID   | Risiko                                    | Wahrscheinlichkeit | Auswirkung |
|------|-------------------------------------------|---------------------|------------|
| NR-1 | ES bleibt in Status IN REVIEW blockiert   | Hoch                | Hoch       |
| NR-2 | Governance-Kette verzögert (kein IP möglich) | Hoch             | Hoch       |
| NR-3 | Implementierungsnahe Inhalte in vertraglichem Dokument | — | Widerspricht ES §1.5 und Charter Approval Record |

---

## 8. Mitigation

| Risiko | Maßnahme                                                     | Verantwortlich        |
|--------|---------------------------------------------------------------|-----------------------|
| WR-1   | Closing Criteria (§9) als Pflichtprüfung vor IP-Genehmigung  | Independent Review    |
| WR-2   | Explizite Begrenzung auf Milestone 1.0 (§3.2)                | Governance Architect  |
| WR-3   | ES Deliverable D-008 referenziert IP als Governance-Artefakt  | Projektleitung        |
| WR-4   | Waiver als Governance-Artefakt im Approval Record referenziert | Independent Review   |

---

## 9. Closing Criteria

Dieser Waiver gilt als geschlossen, wenn **alle** folgenden Bedingungen erfüllt sind:

1. **Implementation Plan 1.0 enthält eine vollständige Delta Analysis**
   gemäß Development Standard v1.1 §6.2 #4 — mit Dateireferenzen (Datei, Zeile, Status)
   für jede Änderung im Milestone-Scope.

2. **Implementation Plan 1.0 enthält ein vollständiges Module Work Breakdown**
   gemäß Development Standard v1.1 §6.2 #5 — mit dateibasierten Änderungsbeschreibungen
   und Codebeispielen für jedes Work Package.

3. **Der Independent Review des Implementation Plans bestätigt die Vollständigkeit**
   der zugewiesenen Abschnitte als Bestandteil der IP-Genehmigung.

4. **Scope Verification mit Dateireferenzen** ist im Implementation Plan enthalten
   (Auflösung von DEV-002 / Finding F-002).

Solange die Closing Criteria nicht erfüllt sind, bleibt der Waiver aktiv und ist
bei jeder Governance-Prüfung des Milestone 1.0 zu berücksichtigen.

---

## 10. Approval Recommendation

### 10.1 Empfehlung

**APPROVED.**

Der Waiver wird zur Genehmigung empfohlen. Die Begründung stützt sich auf:

1. Der Milestone 1.0 Charter (APPROVED) als höchstrangiges milestone-spezifisches
   Governance-Dokument etabliert den zweistufigen Prozess in §8.

2. Die betroffenen Abschnitte (Delta Analysis, Module Work Breakdown) sind inhaltlich
   implementierungsnah und gehören sachlich in den Implementation Plan.

3. Die Engineering Specification 1.0 R1 behandelt den Governance-Konflikt transparent,
   mit vollständigem Deviation Register und drei bewerteten Lösungsoptionen.

4. Der Independent Governance Review bestätigt den Befund und empfiehlt Option A.

5. Alle verbindlichen ES-Inhalte (Scope, Requirements, Acceptance Criteria, Quality Gates,
   Test Strategy, Definition of Done, Risks, Deliverables) sind vollständig und
   intern konsistent.

### 10.2 Konsequenz der Genehmigung

Nach Genehmigung dieses Waivers:

- DEV-001 → **Geschlossen** (Waiver genehmigt)
- DEV-002 → **Geschlossen** (Dateireferenzen dem Implementation Plan zugewiesen)
- ES-1.0 R1 → **Genehmigungsfähig** (keine offenen Critical/High Findings)
- F-001 → **Adressiert**
- F-002 → **Adressiert**
- E-21, E-22 → **Open Blocker aufgelöst**

### 10.3 Nächste Schritte

1. Waiver genehmigen
2. Engineering Specification 1.0 R1 genehmigen
3. Implementation Plan 1.0 erstellen (MUSS Delta Analysis und Module Work Breakdown enthalten)
4. Independent Review des Implementation Plans (MUSS Closing Criteria dieses Waivers prüfen)

---

## 11. Decision Record

| Feld                  | Wert                                                              |
|-----------------------|-------------------------------------------------------------------|
| Entscheidung          | Option A — Abweichung genehmigen                                 |
| Alternativen bewertet | Option B (Dev Standard v1.2), Option C (ES erweitern)             |
| Begründung            | Charter-Autorität, inhaltliche Zugehörigkeit, ES-Selbstbeschränkung |
| Geltungsbereich       | Milestone 1.0                                                    |
| Reversibilität        | Vollständig reversibel durch Rücknahme des Waivers                |
| Betroffene Dokumente  | Keine Änderungen an bestehenden Dokumenten                        |
| Neue Verpflichtungen  | Implementation Plan MUSS §6.2 #4 und #5 enthalten                |
| Closing Criteria      | Ja — vier Kriterien definiert (§9)                                |
