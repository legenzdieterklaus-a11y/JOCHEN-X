# JOCHEN X — Milestone 1.0
# HD4-A1-R0 — ADR-ID Assignment & Registration
## Administrative Follow-up nach HD-4-Approval

> **COMPLETED — ADR-ID ASSIGNED & REGISTERED**
>
> Dieses Dokument protokolliert den rein administrativen Vollzug **A-1**:
> Vergabe der ADR-ID **ADR-012** und Registrierung des bereits genehmigten
> HD-4-ADR unter `docs/adr/`. **Die Genehmigung wurde nicht durch diesen
> Schritt erzeugt** — sie wurde bereits durch die Human-Entscheidung des
> Projekteigners erteilt (HD4-APP-01-R0). A-1 ist deren Registrierung.

---

## 1. Document Identity

| Feld | Wert |
|---|---|
| **Document ID** | **HD4-A1-R0** |
| Subject | **A-1 — ADR-ID Assignment & Registration (HD-4)** |
| Date | 2026-08-11 |
| Pfad | `docs/audits/hd-4-a1-registration-r0.md` |
| **Bezugs-Baseline** | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| HEAD bei Beginn | `14354b850e9b8e45d5ca0a5f277587b2544e65d0` |
| Branch | `milestone-1.0-governance` |
| **Status** | **COMPLETED — ADR-ID ASSIGNED & REGISTERED** |
| **Vergebene ADR-ID** | **ADR-012** |
| **Registrierter Pfad** | `docs/adr/012-plugin-security-policy-configuration.md` |
| ADR-Status | **Accepted** (Dev-Standard §13) |
| Coding | **NOT AUTHORIZED** · RL-05 **NOT REACHED** · QG-006 **NOT STARTED** |

---

## 2. Baseline

| Prüfung | Ergebnis | Klasse |
|---|---|---|
| `git rev-parse HEAD` | `14354b850e9b8e45d5ca0a5f277587b2544e65d0` | SOURCE FACT |
| Governance-Kette | `14354b8` (HD4-APP-01-R0) → `8414384` (HD4-HDR-01-R0) → `b20858e` (HD4-GOV-DECISION-R0) → `641947c` (HD4-AP-01-R0) → `1efb61b` (HD4-FU-R0) → `8fcf42f` (MILESTONE-1.0-BASELINE) — **exakt wie erwartet** | SOURCE FACT |
| Staging vor Beginn | leer | SOURCE FACT |

**Status: PASS** — keine neue Baseline definiert.

---

## 3. Source Gate

| # | Source | Verwendung |
|---|---|---|
| 1 | `docs/audits/hd-4-od05-adr-draft-r0.md` (vor Überführung) | Registrierungsgegenstand — vollständig bekannt, R0, unverändert |
| 2 | `docs/audits/hd-4-approval-decision-r0.md` (HD4-APP-01-R0) | Approval-Nachweis: HD-4 = APPROVED (Projekteigner, 2026-08-11); ADR-ID ausdrücklich als separate Folgearbeit ausgewiesen |
| 3 | `docs/audits/hd-4-approval-readiness-r0.md` (HD4-AP-01-R0) | A-1 = ADMINISTRATIVE FOLLOW-UP |
| 4 | `docs/audits/hd-4-human-decision-record-r0.md` (HD4-HDR-01-R0) | Chronologie |
| 5 | `docs/governance/hd-1-adr-rdr-decision.md` | SF-14: Bestand ADR-001 … ADR-011 + RDR-001; „Identifikatorvergabe gehört zu HD-4" |
| 6 | `docs/governance/f-05-…` / `f-04-…` / `od-05-…` | Kontext, unverändert |
| 7 | `docs/development-standard-v1.1.md` | §13 Dateimuster `docs/adr/{NNN}-{kebab-case-title}.md`; §13/§17 Anh. B Status `Open → Accepted`; §5 „Alle akzeptierten ADRs in `docs/adr/` sind Teil der Baseline" |
| 8 | Repository-Struktur `docs/adr/`, `docs/rdr/` | tatsächliche ID-/Namenskonvention (Kap. 4) |

Keine externe Quelle. **Status: PASS**

---

## 4. Vorhandene ADR-ID-Struktur (Repository-Befund)

| Befund | Ergebnis | Klasse |
|---|---|---|
| Bestand `docs/adr/` | `001-core-boundaries.md` · `002-event-delivery.md` · `003-optional-developer-platform.md` · `004-plugin-security-integration.md` · `005-plugin-integrity-validation.md` · `006-plugin-permission-model.md` · `007-plugin-dependency-resolution.md` · `008-plugin-context-definition.md` · `009-plugin-isolation-strategy.md` · `010-plugin-sdk-architecture.md` · `011-sdk-host-integration.md` | SOURCE FACT |
| Nummernraum | **001 … 011, lückenlos**, keine Reservierungen, kein `012` vorhanden | SOURCE FACT |
| RDR-Namensraum | `docs/rdr/` (RDR-001) — **separater** Namensraum, beeinflusst die ADR-Nummerierung nicht (deckungsgleich mit HD-1 SF-14) | SOURCE FACT |
| ADR-Index/Register | **nicht vorhanden** (kein README/Index in `docs/adr/`) — daher keine Registerdatei nachzuführen | SOURCE FACT |
| Etablierte Dateikonvention | `{NNN}-{kebab-case-title}.md`, dreistellig, englischsprachige beschreibende Kebab-Titel, kein „ADR-"-Präfix im Dateinamen | SOURCE FACT |
| Etablierte Dokumentkonvention | H1 `# ADR NNN: <Titel>`; danach `**Status:** Accepted \| Resolved by …` (verifiziert an ADR-001, ADR-004) | SOURCE FACT |
| Working-Tree-Hinweis | ADR-005/006/007 sind im Working Tree modifiziert (fremder Bestand, GDR-OD01-001-Kontext) — **nicht berührt** | SOURCE FACT |

## 5. ID-Vergaberegel und Eindeutigkeit

| Frage | Ergebnis |
|---|---|
| ID-Format | dreistellig `{NNN}`, fortlaufend (Dev-Standard §13 + Repository-Bestand) |
| Vergebene IDs | 001 … 011 |
| Lücken/Reservierungen | keine |
| **Nächste zulässige ID** | **012** — deterministisch (einzige regelkonforme Fortschreibung des lückenlosen Bestands) |
| Kollision | keine — `012` war nicht vergeben |
| Deterministisch? | **JA** — kein STOP-Tatbestand „ADR-ID NOT DETERMINABLE" |

**Vergebene ID: ADR-012.**

**Titel-/Dateinamensableitung:** Gegenstand des ADR ist die Policy-Konfiguration
der bestehenden `PluginSecurityStage` (OD-05 Option B). Gemäß etablierter
Konvention (englische beschreibende Kebab-Titel; vgl. `004-plugin-security-integration.md`,
`005-plugin-integrity-validation.md`): **`012-plugin-security-policy-configuration.md`**.

---

## 6. Gegenstandsverifikation (Pre-Registration Check)

| Prüfung | Ergebnis |
|---|---|
| Dokument | HD-4 ADR-Entwurf **R0** — identisch mit dem in HD4-APP-01-R0 genehmigten Gegenstand |
| Status vor Registrierung | `DRAFT / NON-NORMATIVE / PENDING APPROVAL`, ADR-Feld `Open`, unverändert seit Erstellung (Pre-Approval Source Check in HD4-APP-01-R0 Kap. 8) |
| Nachträgliche inhaltliche Änderung | **keine** |
| Human Decision | APPROVED — Projekteigner, 2026-08-11 (HD4-APP-01-R0 Kap. 5) |

**Kein ADR SCOPE MISMATCH.**

---

## 7. Autorisierungsgrundlage der Registrierung

| # | Grundlage | Wirkung |
|---|---|---|
| 1 | **Dev-Standard §13**: ADR-Datei = `docs/adr/{NNN}-{kebab-case-title}.md` | bestimmt Zielpfad und Namensschema |
| 2 | **Dev-Standard §5**: „Alle akzeptierten ADRs in `docs/adr/` sind Teil der Baseline" | ein akzeptierter ADR gehört nach `docs/adr/` |
| 3 | **Dev-Standard §13/§17 Anh. B**: Statusübergang `Open → Accepted` | bestimmt den Post-Approval-Status **`Accepted`** — quellenbelegt, kein STOP „POST-APPROVAL STATUS NOT DETERMINABLE" |
| 4 | **HD-4 Kap. 1.1/21**: „endgültige ADR-ID und Registrierung unter `docs/adr/` sind Gegenstand der … Genehmigung"; Rolle „Zuweisung `{NNN}` und Überführung nach `docs/adr/`" | definiert die Überführung als Vollzug nach Genehmigung |
| 5 | **HD-1 SF-14**: „Identifikatorvergabe gehört zu HD-4" | verortet die ID-Vergabe im HD-4-Prozess |
| 6 | **HD4-APP-01-R0**: HD-4 = APPROVED; „ADR-ID ASSIGNMENT = SEPARATE FOLLOW-UP" | dieses Follow-up ist der vorliegende Auftrag |

**Die Registrierung ist damit eindeutig autorisiert** — kein STOP-Tatbestand
„REGISTRATION ACTION NOT AUTHORIZED".

---

## 8. Tatsächlich vorgenommene Änderungen (vollständig)

| # | Änderung | Art |
|---|---|---|
| 1 | **Überführung**: `docs/audits/hd-4-od05-adr-draft-r0.md` → `docs/adr/012-plugin-security-policy-configuration.md` (Move; der Draft-Pfad existiert nicht mehr — historische Referenzen auf den alten Pfad bleiben als Zeitpunktdokumentation gültig) | mechanisch (Registrierung) |
| 2 | **Titel/H1**: „# HD-4 — ADR-ENTWURF (R0): …" → „# ADR 012: Policy-Konfiguration in der bestehenden PluginSecurityStage (OD-05 Option B)" + Statuszeile `**Status:** Accepted` gemäß Hauskonvention | mechanisch (ID/Status) |
| 3 | **Banner**: DRAFT-Banner ersetzt durch ACCEPTED/REGISTERED-Banner mit Approval-/Registrierungsreferenz, Registrierungsvermerk (historische R0-Statusmarker in Kap. 1.1/19/20/21 bleiben unverändert und sind durch Banner + Records überholt) und unveränderter Zeile `CODING = NOT AUTHORIZED · RL-05 = NOT REACHED · QG-006 = NOT STARTED` | mechanisch (Status) |
| 4 | **Kap. 1 (Document Identity)**: Pfad, ADR-ID (**ADR-012**), Dokumentstatus (**ACCEPTED / REGISTERED**), ADR-Status-Feld (**Accepted**), Dokumenttyp/Auftrag um Registrierungsverweis ergänzt | mechanisch (ID/Status) |
| 5 | **Kap. 2 (Status)**: Status **Accepted**; Dokumentstatus **ACCEPTED / REGISTERED**; „Genehmigt? **JA**" mit Quellenverweis HD4-APP-01-R0; „Implementierung autorisiert? **NEIN**" unverändert | mechanisch (Status) |
| 6 | **Kap. 22 (Revision History)**: Zusatzzeile „R0 (Registrierung)" mit Genehmigungs- und Registrierungsvermerk | mechanisch (Registervermerk) |
| 7 | **Neues Audit-Artefakt**: dieses Dokument | Archiv |

**Nicht verändert:** sämtlicher Architektur- und Entscheidungstext (Kap. 3–18),
das OI-Register (Kap. 19), der historische Governance-Status (Kap. 20), die
Approval Section (Kap. 21, historischer R0-Stand), die Schlusszeile sowie alle
anderen Repository-Dateien. Insbesondere: keine Änderung an ADR-001 … ADR-011,
keine Änderung an den im Working Tree modifizierten ADR-005/006/007, keine
Änderung an historischen HD-4-Audit-Artefakten.

---

## 9. Trennung Approval ↔ Registrierung

```text
HD-4 Approval → bereits durch Human Decision erteilt (HD4-APP-01-R0, 2026-08-11).
A-1          → administrative Registrierung dieser bereits genehmigten ADR.
```

Die ADR-ID erzeugt die Genehmigung **nicht** — sie vollzieht sie administrativ.
`ADR-ID Assignment ≠ Approval Decision`.

---

## 10. Unveränderte Downstream-Governance

| Position | Status | Wirkung von A-1 |
|---|---|---|
| **HD-2** | **OPEN / NOT DECIDED** | keine |
| **HD-3** | **OPEN / NOT DECIDED** | keine |
| **Coding** | **NOT AUTHORIZED** | keine — A-1 autorisiert kein Coding |
| **RL-05** | **NOT REACHED** | keine |
| **QG-006** | **NOT STARTED** | keine |
| **Tests** | **NOT EXECUTED** | keine |
| **OI-1 … OI-6** | unverändert offen | keine |
| **OI-7** (ADR-ID/Registrierung) | **FULFILLED BY HD4-A1-R0** — OI-7 bildet exakt diese administrative Vergabe/Registrierung ab; der historische Registereintrag im ADR-Dokument (Kap. 19) bleibt unverändert | Vollzug dokumentiert |
| **OI-8** (ADR-Genehmigung) | FULFILLED BY HUMAN DECISION (HD4-APP-01-R0) — unverändert | keine |
| **UNKNOWNs** | sämtlich unverändert — keine Position durch die ID-Vergabe geschlossen | keine |
| **Change Surface** | CS-1 + CS-2 + CS-3 — unverändert | keine |

**Beobachtung HD4-A1-B-01** (OBSERVATION): Der in HD-4 Kap. 1.1 dokumentierte
Zusatzbefund zur Register-Lage (ADR-005/006/007: Welt A `Open` vs. Welt B
`APPROVED`, Disposition per GDR-OD01-001 getrennt) bleibt unverändert bestehen
und wird durch die Vergabe von ADR-012 nicht berührt.

---

## 11. Preflight (Ergebnis)

Alle 23 Checks **PASS** — u. a.: Baseline korrekt; Human Approval verifiziert;
ADR eindeutig identifiziert; ID-Schema quellenverifiziert; alle bestehenden IDs
geprüft; ID **012** eindeutig, kollisionsfrei; Zielpfad eindeutig; Status
`Accepted` quellenbelegt (§13/§17 Anh. B); Inhalt nicht inhaltlich verändert
(nur die in Kap. 8 gelisteten mechanischen Nachführungen); HD-2/HD-3/Coding/
RL-05/QG-006/UNKNOWNs unverändert; historische Audit-Artefakte unverändert;
fremde Working-Tree-Änderungen unverändert; keine generischen `B-<n>`-IDs;
nur A-1-relevante Dateien staged.

## 12. Commit / Push

| Feld | Wert |
|---|---|
| Staged | `docs/adr/012-plugin-security-policy-configuration.md` + `docs/audits/hd-4-a1-registration-r0.md` — beide zwingend A-1-zugehörig |
| Commit | `docs: register approved HD-4 ADR` |
| Push / PR / Merge | **NOT PERFORMED** |

---

## 13. Final Governance Gate

> ## **HD4-A1-R0 = COMPLETED — ADR-ID ASSIGNED & REGISTERED**
>
> **ADR-012** = `docs/adr/012-plugin-security-policy-configuration.md` · **Status: Accepted**
>
> **HD-4 = APPROVED** (unverändert) · **HD-2/HD-3 = OPEN** · **CODING = NOT
> AUTHORIZED** · **RL-05 = NOT REACHED** · **QG-006 = NOT STARTED**

---

**Ende HD4-A1-R0 — ADR-ID Assignment & Registration — JOCHEN X Milestone 1.0
(2026-08-11) — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
