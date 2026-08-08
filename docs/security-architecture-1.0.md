# JOCHEN X – Security Architecture & Trust Framework 1.0

| Feld                | Wert                                                                                      |
|---------------------|-------------------------------------------------------------------------------------------|
| Status              | **APPROVED**                                                                               |
| Version             | 1.0                                                                                        |
| Revision            | R0                                                                                         |
| Datum               | 2026-08-08                                                                                 |
| Autor               | Chief Security Architect / Zero-Trust Architect / AI Security Architect                    |
| Genehmigungsinstanz | Projekteigner JOCHEN X                                                                     |
| Genehmigt           | 2026-08-08 durch Projekteigner JOCHEN X — Approval Decision W-2 (ADW-SA-1.0-002), Approval Record W-3 (APR-SA-1.0-001) |
| Dokumenttyp         | Security Architecture / Trust Framework                                                    |
| Normative Grundlage | JOCHEN X – Core Principles 1.0 (APPROVED, R2, 2026-08-07)                                  |
| Erstellungsauftrag  | Core Principles 1.0 Governance Closing W-7 (Nächster autorisierter Dokumenttyp, „Autorisiert zur Erstellung") |
| Gültigkeit          | Wirksam ab Genehmigung als nachgeordnetes, selbstbeschränktes Architekturartefakt — siehe Geltungsvorbehalt und Kapitel 0.3 |

---

## Geltungsvorbehalt

Solange dieses Dokument den Status DRAFT trägt, entfaltet es **keine
Bindungswirkung**. Sämtliche Bestimmungen der Kapitel 0 bis 24 sind bis zu
einer Genehmigung durch die im Dokumentkopf genannte Genehmigungsinstanz als
Entwurf zu lesen. Die Kennzeichnungen `CP-derived`, `architecture-open` und
`governance-conflict` beschreiben die **Herkunft** einer Aussage, nicht ihre
Verbindlichkeit; auch eine als `CP-derived` gekennzeichnete Aussage ist im
Status DRAFT nicht verbindlich.

---

## Referenzen — geprüfter Quellenbestand

Die folgende Aufstellung führt den vor der Erstellung dieses Dokuments
tatsächlich gelesenen Repository-Bestand mit der im jeweiligen Artefakt
ausgewiesenen Statusangabe. Sie ist deklaratorisch. Statusangaben sind
unverändert übernommen; Abweichungen zwischen Artefakten sind in Kapitel 24.1
als `governance-conflict` dokumentiert und hier **nicht** korrigiert.

| Artefakt | Pfad | Ausgewiesener Status |
|---|---|---|
| JOCHEN X – Core Principles 1.0 | `docs/core-principles-1.0.md` | **APPROVED** (R2, 2026-08-07) |
| Architecture Book v2.0 | `docs/architecture-book-v2.md` | **APPROVED / FROZEN** (2026-07-26) |
| Development Standard v1.1 | `docs/development-standard-v1.1.md` | **APPROVED** (2026-07-27) |
| Bootstrap Baseline 1.0 | `docs/baselines/bootstrap-baseline-1.0.md` | **APPROVED** (2026-08-01) |
| Security (Modulspezifikation) | `docs/security.md` | *keine Statusangabe im Dokument* → GC-02 |
| ADR-001 Explicit core boundaries | `docs/adr/001-core-boundaries.md` | Accepted |
| ADR-002 Explicit event delivery modes | `docs/adr/002-event-delivery.md` | Accepted |
| ADR-003 Developer platform is opt-in | `docs/adr/003-optional-developer-platform.md` | Accepted |
| ADR-004 Plugin security integration timing | `docs/adr/004-plugin-security-integration.md` | „Resolved by ADR-011 §D3" → GC-05 |
| ADR-005 Plugin Integrity Validation | `docs/adr/005-plugin-integrity-validation.md` | **APPROVED** (2026-07-30) |
| ADR-006 Plugin Permission Model | `docs/adr/006-plugin-permission-model.md` | **APPROVED** (2026-07-29) |
| ADR-007 Plugin Dependency Resolution | `docs/adr/007-plugin-dependency-resolution.md` | **APPROVED** (2026-07-29) |
| ADR-008 Plugin context definition | `docs/adr/008-plugin-context-definition.md` | „Resolved by ADR-010 / ADR-011 §D4" → GC-05 |
| ADR-009 Plugin isolation strategy | `docs/adr/009-plugin-isolation-strategy.md` | „Resolved by ADR-011 §D2" → GC-05 |
| ADR-010 Plugin SDK architecture | `docs/adr/010-plugin-sdk-architecture.md` | Accepted (v0.7.1) |
| ADR-011 SDK-Host-Integration | `docs/adr/011-sdk-host-integration.md` | Accepted (v0.8.0) — CP-Referenzliste führt „APPROVED" → GC-06 |
| Milestone 1.0 Implementation Plan | `docs/milestone-1.0-implementation-plan.md` | **APPROVED** (Approval Record W-6) |
| Core Principles 1.0 Governance Closing W-7 | `docs/governance/core-principles-1.0-governance-closing-w7.md` | COMPLETED |
| Milestone 1.0 Governance Closing Report W-8 | `docs/governance/milestone-1.0-governance-closing-report-w8.md` | COMPLETED |
| RDR-001 Bootstrap Modularization | `docs/rdr/001-bootstrap-modularization.md` | APPROVED (laut CP-Referenzliste) |

**Nicht geprüft und daher nicht referenziert:** Implementierungsquellcode
(`app/`, `core/`, `sdk/`, `services/`), Tests, sowie Audit-Artefakte, die keine
Sicherheitsaussage tragen. Dieses Dokument trifft keine Aussage über den
Implementierungsstand.

---

## 0. Governance-Einordnung

Dieses Kapitel ordnet das Dokument in die bestehende Governance ein. Es enthält
selbst keine Sicherheitsarchitektur.

### 0.1 Verhältnis zu den Core Principles

**Core Principles 1.0 sind die normative Wahrheit. Diese Security Architecture
ist deren sicherheitsarchitektonische Konkretisierung.**

Dieses Dokument:

- konkretisiert die Core Principles im Sicherheitsbereich
- leitet Sicherheitsgrenzen aus ihnen ab
- beschreibt Vertrauensbeziehungen
- bereitet zukünftige Sicherheitsarchitektur vor
- benennt offene Architekturentscheidungen

Dieses Dokument **DARF NICHT** Core Principles neu definieren, umformulieren,
ersetzen, neue Verfassungsartikel erzeugen oder eine konkurrierende
Dokumenthierarchie erzeugen. Es **DARF NICHT** bestehende APPROVED-, FROZEN-
oder BASELINE-Artefakte rückwirkend verändern.

Bei einem Widerspruch zwischen diesem Dokument und den Core Principles gilt der
Widerspruch als Fehler dieses Dokuments (Core Principles Governance Rule 2).

### 0.2 Einordnung gegenüber bestehenden Dokumentklassen

| Bezugsdokument | Verhältnis dieses Dokuments |
|---|---|
| Core Principles 1.0 | Vollständig nachgeordnet und gebunden. Quelle jeder normativen Ableitung. |
| Architecture Book v2.0 (FROZEN) | Wird referenziert und berücksichtigt. Wird **nicht** geändert, ausgelegt oder außer Kraft gesetzt. Bestehende Aussagen bleiben in der eingefrorenen Fassung unberührt. |
| Development Standard v1.1 | Verfahren, Reviewform und Genehmigungsweg richten sich ausschließlich nach diesem Dokument. Diese Security Architecture setzt kein eigenes Verfahren. |
| Bestehende ADRs (001–011) | Werden referenziert, berücksichtigt und abgegrenzt. Werden **nicht** ersetzt, geändert oder neu geschrieben. |
| Engineering Specifications | Nicht betroffen. Dieses Dokument definiert keinen Milestone-Scope. |
| Implementation Plans | Nicht betroffen. Dieses Dokument definiert keine Arbeitspakete. |

### 0.3 Keine neue Dokumenthierarchie

Dieses Dokument **beansprucht keine Rangstufe** in der Rangordnung nach Core
Principles 1.0, Kapitel 0 („Dokumenteinordnung und Dokumenthierarchie"), und
ändert die Konfliktregel in Development Standard v1.1 §3.3 nicht.

Eine Rangfolge der Form *Core Principles → Security Architecture → ADR → ES →
IP* wird von diesem Dokument **nicht** behauptet und **nicht** eingeführt.

Die Rangeinordnung der Dokumentklasse „Security Architecture / Trust Framework"
ist aus dem bestehenden Dokumentmodell **nicht eindeutig ableitbar**. Die
Rangordnung der Core Principles führt zwölf Dokumentklassen, unter denen diese
Klasse nicht enthalten ist; Development Standard v1.1 §3.1–§3.3 führt sie
ebenfalls nicht; die Tabelle „Single Authoritative Source" (Development Standard
v1.1 §2.1) weist die Domäne „Architektur" dem eingefrorenen Architecture Book
v2.0 zu und kennt keine Domäne „Sicherheitsarchitektur". Zugleich benennt Core
Principles Governance Rule 2 die Security Architecture ausdrücklich als
gebundenes zukünftiges Dokument.

→ **`governance-conflict` GC-01.** Die Entscheidung über die Rangeinordnung
obliegt der Genehmigungsinstanz und wird hier nicht getroffen.

Bis zu dieser Entscheidung gilt für dieses Dokument nach eigener Setzung: es ist
sämtlichen in der Core-Principles-Rangordnung geführten Dokumentklassen der
Ränge 1 bis 5 gegenüber **nachgeordnet** und beansprucht gegenüber keiner
Dokumentklasse Vorrang. Diese Setzung ist eine Selbstbeschränkung dieses
Entwurfs, keine Rangbestimmung.

### 0.4 No Retroactive Effect

Die Bestandsschutzregel der Core Principles (Governance Rule 1) gilt für dieses
Dokument vollständig.

Kein Artefakt mit Status APPROVED, FROZEN, BASELINE oder Accepted, das vor dem
Genehmigungsdatum dieses Dokuments genehmigt wurde, wird durch dieses Dokument
verändert, ausgelegt, ersetzt oder ungültig. Dies gilt insbesondere für
Architecture Book v2.0, Development Standard v1.1, Bootstrap Baseline 1.0 und
sämtliche ADRs.

Wo dieses Dokument eine Spannung zwischen einer bestehenden Festlegung und einem
Core Principle feststellt, wird diese als `governance-conflict` **dokumentiert**
und der Genehmigungsinstanz zur Entscheidung überlassen. Sie wird nicht durch
dieses Dokument aufgelöst.

### 0.5 No Redefinition Rule

Sämtliche in den Core Principles bestimmten Begriffe sind normativ vorgegeben
und werden hier **ausschließlich referenziert**, niemals neu definiert.

Betroffen sind insbesondere: Human Authority (CP 5.1, Artikel 1), Local
Sovereignty (CP 5.2), Zero Trust (CP 5.3), Least Privilege (CP 5.4), Wirkung
(CP Kap. 0), bedeutsam (CP Kap. 0), erheblich (CP Kap. 0), kritisch (CP Kap. 0),
sensibel (CP Kap. 0), lokale Vertrauensdomäne (CP Kap. 0), die Vertrauensebenen
(CP 6.2), Eigentümer (CP 6.2), Kritische Freigabe (CP 6.2) sowie die
Non-Negotiable Principles (CP Kap. 12).

Dieses Dokument führt für keinen dieser Begriffe eine zweite Definition, keine
alternative Terminologie und keine abweichende Bedeutung ein. Wo eine
sicherheitsarchitektonische Präzisierung erfolgt, betrifft sie ausschließlich
die **Sicherheitsfolge** des bereits definierten Begriffs.

Diese Regel setzt Development Standard v1.1 §2.3 („No Normative Duplication")
für dieses Dokument um.

### 0.6 Normsprache

| Schlüsselwort | Bedeutung |
|---|---|
| **MUSS** / **DARF NICHT** | Zwingend aus den Core Principles abgeleitete Anforderung bzw. zwingendes Verbot. Keine Ausnahme. |
| **SOLL** | Architektonische Konkretisierung. Abweichung nur mit dokumentierter Begründung. |
| **KANN** | Zulässige zukünftige Möglichkeit. Keine Anforderung. Entspricht „DARF" nach Development Standard v1.1 §1.1 und MAY nach RFC 2119. |

Die Bezeichnung **KANN** wird auf Vorgabe des Erstellungsauftrags verwendet und
ist bedeutungsgleich mit „DARF" im Development Standard; eine neue
Verbindlichkeitsstufe entsteht dadurch nicht.

Eine als `architecture-open` oder `governance-conflict` gekennzeichnete Aussage
ist **niemals** eine Anforderung, unabhängig von ihrer sprachlichen Form.

### 0.7 Kennzeichnungssystem

Jede über eine bloße Wiedergabe hinausgehende Aussage dieses Dokuments trägt
genau eine Kennzeichnung:

| Kennzeichnung | Bedeutung |
|---|---|
| `CP-derived` | Direkt aus einer benannten Stelle der Core Principles oder aus einem zulässigen bestehenden Architekturartefakt abgeleitet. Die Fundstelle ist angegeben. |
| `architecture-open` | Sinnvolle zukünftige Architekturentscheidung, die noch **nicht** normativ festgelegt ist. Keine Anforderung. |
| `governance-conflict` | Widerspruch oder ungeklärtes Verhältnis zu bestehender Governance. Wird dokumentiert, nicht entschieden. |

**Regel.** Keine neue verbindliche Norm ohne nachvollziehbare Herkunft. Wo eine
Fundstelle fehlt, ist die Aussage `architecture-open`.

---

## 1. Purpose

Diese Security Architecture beschreibt den sicherheitsarchitektonischen Rahmen
von JOCHEN X. Sie übersetzt die Core Principles in Sicherheitsziele,
Vertrauensbeziehungen und Sicherheitsgrenzen, aus denen spätere Security
Designs, ADRs, Engineering Specifications und Implementierungen abgeleitet
werden können.

Sie soll sicherstellen, dass JOCHEN X langfristig

- die Autorität des Menschen schützt *(CP 5.1, Artikel 1)*
- die lokale Souveränität wahrt *(CP 5.2, Artikel 4, Artikel 10)*
- externe Systeme kontrolliert behandelt *(CP 7.7, Artikel 3)*
- minimale Berechtigungen verwendet *(CP 5.4)*
- kritische Aktionen absichert *(CP 5.10, CP 6.2, Artikel 8)*
- nachvollziehbar bleibt *(CP 4.8, CP 5.5, Artikel 8)*
- sicher weiterentwickelt werden kann *(CP 5.6, CP 11.1, Artikel 7)*

**Was dieses Dokument nicht leistet.** Es garantiert keine technische
Sicherheit. Ein Rahmen ist keine Schutzmaßnahme. Die Wirksamkeit jeder
Sicherheitseigenschaft entsteht erst durch spätere Entwurfsentscheidungen,
Implementierung und Verifikation — und ist erst dort nachweisbar. Aussagen
dieses Dokuments über Sicherheitseigenschaften sind **Zielaussagen**, keine
Zusicherungen. *(CP 8.3: das System stellt Vermutungen nicht als Wissen dar.)*

**Adressaten.** Autoren zukünftiger Security-ADRs, Architekturdokumente und
Engineering Specifications sowie die Genehmigungsinstanz.

---

## 2. Security Objectives

Die folgenden Sicherheitsziele werden aus den Core Principles abgeleitet. Jedes
Ziel trägt seine Herkunft. Ziele sind **Ziele**, keine Kontrollen: sie sagen,
*was erreicht werden soll*, nicht *womit*.

| ID | Ziel | Aussage | Herkunft |
|---|---|---|---|
| **SO-01** | Human Authority | Die Sicherheitsarchitektur MUSS so beschaffen sein, dass keine ihrer Komponenten, Konfigurationen oder Zustände die menschliche Letztentscheidung ersetzen, umgehen oder faktisch entwerten kann. | `CP-derived` — CP 5.1, 8.5, 8.6, Artikel 1 |
| **SO-02** | Local Sovereignty | Wesentliche Verarbeitung, Zustand und Entscheidungslogik MÜSSEN innerhalb der lokalen Vertrauensdomäne verbleiben. Ihr Verlassen MUSS bewusst, begründet, autorisiert und nachvollziehbar sein. | `CP-derived` — CP 5.2, 4.3, Artikel 4, Artikel 10 |
| **SO-03** | Zero Trust | Kein Akteur — extern, intern, Erweiterung oder das System selbst — DARF allein aufgrund seiner Herkunft, seiner Zugehörigkeit oder seiner bisherigen Nutzung als vertrauenswürdig behandelt werden. | `CP-derived` — CP 5.3, 7.4, Artikel 5 |
| **SO-04** | Least Privilege | Jeder Akteur und jeder Vorgang MUSS nur die minimal erforderlichen Rechte erhalten, und diese nur so lange wie nötig. Rechte DÜRFEN NICHT durch Gewohnheit, Dauer oder Wiederholung wachsen. | `CP-derived` — CP 5.4, 7.5 |
| **SO-05** | Explicit Authorization | Handlungen mit erheblicher oder kritischer Wirkung MÜSSEN auf einer ausdrücklichen, informierten und anlassbezogenen menschlichen Autorisierung beruhen. Eine erteilte Zustimmung gilt nicht für künftige gleichartige Vorgänge. | `CP-derived` — CP 5.10, 6.2 („Verhältnis zur menschlichen Freigabe") |
| **SO-06** | Confidentiality | Sensible Informationen MÜSSEN unter lokaler Kontrolle bleiben und DÜRFEN NICHT beiläufig offengelegt werden — auch nicht in Protokollen, Fehlermeldungen, Diagnosedaten oder Erklärungen. | `CP-derived` — CP 7.2, 4.4 |
| **SO-07** | Integrity | Das System MUSS Veränderungen an seinen Bestandteilen, seinen Regeln und seinen Aufzeichnungen erkennen können. | `CP-derived` — CP 7.3 |
| **SO-08** | Availability | Verfügbarkeit ist ein Ziel, aber niemals ein Grund zur Aufgabe von Kontrolle oder Souveränität. Der Ausfall externer Systeme DARF das System schwächen, aber nicht unbrauchbar machen. | `CP-derived` — CP 3.2, 10.4, 10.7 |
| **SO-09** | Auditability | Kritische Vorgänge MÜSSEN eine belastbare, gegen nachträgliche Veränderung geschützte und für den Eigentümer zugängliche Spur hinterlassen. | `CP-derived` — CP 4.8, Artikel 8 |
| **SO-10** | Explainability | Jede bedeutsame Entscheidung MUSS in einer für den Eigentümer verständlichen Sprache erklärbar sein. Eine nicht erklärbare Entscheidung DARF NICHT Grundlage kritischen Handelns sein. | `CP-derived` — CP 4.6, 5.5, 8.4 |
| **SO-11** | Resilience | Der Ausfall eines Teils DARF NICHT den Verlust der Grundfunktion bewirken. Das System MUSS seinen beeinträchtigten Zustand erkennen und benennen. | `CP-derived` — CP 4.12, 10.7, Artikel 11 |
| **SO-12** | Recovery | Das System MUSS aus einem beeinträchtigten oder kompromittierten Zustand geordnet in einen sicheren Zustand zurückkehren können. Schutz vor Datenverlust hat Vorrang vor Verfügbarkeit. | `CP-derived` — CP 10.7, 4.12 |
| **SO-13** | Separation of Trust | Identität, Vertrauensebene, Herkunft, Berechtigung und Autorität MÜSSEN als getrennte Konzepte geführt werden. Keines dieser Konzepte DARF ein anderes automatisch erzeugen. | `CP-derived` — CP 5.3 („Die Herkunft einer Anfrage begründet allein keine Berechtigung"), 6.2, 7.4, Artikel 5 |
| **SO-14** | Simulation Isolation | Fähigkeiten mit finanzieller Wirkung MÜSSEN in einer folgenlosen Umgebung von der Realität getrennt bleiben. Der folgenlose Zustand ist der Standardzustand. | `CP-derived` — CP 9.1, 9.2 |

**Verhältnis der Ziele untereinander.** Bei Kollision gilt die Prioritätsregel
der Core Principles: **Human First vor Security First vor allen übrigen Werten**
(CP Kap. 4). SO-01 geht damit sämtlichen übrigen Zielen vor; SO-03 bis SO-14
gehen komfort- oder leistungsbezogenen Erwägungen vor. `CP-derived` — CP Kap. 4.

**Nicht enthalten.** Eine Gewichtung, Messbarkeit oder Zielerreichungsmetrik der
Sicherheitsziele ist nicht festgelegt. `architecture-open` **AO-01**.

---

## 3. Trust Architecture

Dieses Kapitel beschreibt, **wie Vertrauen entsteht, nachgewiesen, entzogen und
begrenzt wird**. Es enthält keine Rollenmatrix und keine
Permission-Zuordnungstabelle.

### 3.1 Die Vertrauensebenen bleiben unverändert

Die Vertrauensebenen von JOCHEN X sind ausschließlich die in Core Principles 6.2
bestimmten:

**Gast · Benutzer · Verifizierter Benutzer · Eigentümer · Kritische Freigabe**

Diese Ebenen werden hier **referenziert, nicht wiedergegeben und nicht
ausgelegt**. Maßgeblich ist der Wortlaut in CP 6.2.

Dieses Dokument führt **keine** alternative Vertrauenshierarchie ein. Insbesondere
werden die Bezeichnungen *Unknown, External, Local, Trusted, Admin, Root, Low
Trust, High Trust* und vergleichbare Skalen **nicht** als Vertrauensebenen von
JOCHEN X verwendet. `CP-derived` — CP 6.2, Development Standard v1.1 §2.3.

### 3.2 Entstehung von Vertrauen

Vertrauen entsteht ausschließlich durch **Erwerb**, niemals durch Zuweisung,
Herkunft, Dauer oder technischen Zustand. `CP-derived` — CP 6.3, Artikel 5.

Sicherheitsarchitektonische Konsequenz: Eine Sicherheitsarchitektur, in der ein
Akteur eine Vertrauensebene allein dadurch erreicht, dass er lange genug
existiert, häufig genug genutzt wurde oder an einem bestimmten Ort ausgeführt
wird, ist mit CP 6.3 unvereinbar. Ein solcher Mechanismus DARF NICHT entworfen
werden. `CP-derived` — CP 6.3.

### 3.3 Nachweisbarkeit

Der erforderliche Nachweisaufwand richtet sich nach der **Wirkungsstufe** der
Handlung (bedeutsam < erheblich < kritisch), nicht nach ihrer technischen
Komplexität. `CP-derived` — CP 6.3, CP Kap. 0 („Wirkung").

Ein Nachweis MUSS auf einer überprüfbaren Grundlage beruhen; die bloße
Behauptung einer Identität begründet niemals Berechtigung. `CP-derived` — CP 7.4.

Welche Nachweisarten für welche Wirkungsstufe genügen, ist **nicht** entschieden.
`architecture-open` **AO-02**.

### 3.4 Widerrufbarkeit

Vertrauen ist jederzeit widerrufbar — durch den Eigentümer und durch das System
bei begründetem Verdacht. `CP-derived` — CP 6.3.

Sicherheitsarchitektonische Konsequenz: Jede zukünftige Vertrauensdarstellung
SOLL so entworfen werden, dass ein Widerruf vollständig, unverzüglich und ohne
Restwirkung möglich ist. Ein Vertrauenszustand, der nach seinem Widerruf noch
Wirkung entfaltet, widerspricht CP 6.3. `CP-derived` — CP 6.3.

Die technische Form des Widerrufs und seiner Ausbreitung über bereits laufende
Vorgänge ist nicht entschieden. `architecture-open` **AO-03**.

### 3.5 Verfall

Was lange nicht bestätigt wurde, gilt als ungeprüft. `CP-derived` — CP 6.3.

Sicherheitsarchitektonische Konsequenz: Vertrauen SOLL als **zeitlich begrenzter
Zustand** modelliert werden, nicht als dauerhafte Eigenschaft. Fristen,
Auslöser und Wirkung des Verfalls sind nicht entschieden. `architecture-open`
**AO-04**.

### 3.6 Kontextabhängigkeit

Eine Vertrauensebene, die für einen Bereich ausreicht, reicht für einen anderen
möglicherweise nicht. `CP-derived` — CP 6.3.

Sicherheitsarchitektonische Konsequenz: Vertrauen SOLL stets in Bezug auf einen
konkreten Vorgang, eine konkrete Sicherheitsdomäne und eine konkrete
Wirkungsstufe beurteilt werden, nicht als globaler Zustand eines Akteurs.
`CP-derived` — CP 6.3.

### 3.7 Delegation

Ein Akteur DARF NICHT durch Weitergabe, Verkettung oder Zwischenschaltung mehr
bewirken, als ihm unmittelbar erlaubt wäre. Eine Kette von Handlungen DARF in
Summe nicht mehr bewirken als jede einzelne Handlung. `CP-derived` — CP 7.5.

Menschliche Autorität ist **nicht delegierbar**. `CP-derived` — CP 5.1,
Artikel 1.

Die Ebene „Eigentümer" ist dem Menschen vorbehalten und KANN von einem
nicht-menschlichen Akteur nicht erreicht werden. `CP-derived` — CP 6.2,
Artikel 1.

Ob und in welcher Form eine begrenzte, widerrufliche Delegation zwischen
nicht-menschlichen Akteuren zulässig sein soll, ist nicht entschieden.
`architecture-open` **AO-05**.

### 3.8 Vertrauensgrenzen

Eine Vertrauensgrenze ist der Punkt, an dem ein Vorgang von einem
Vertrauensverhältnis in ein anderes übergeht. An jeder solchen Grenze MUSS eine
erneute Beurteilung stattfinden; ein Vertrauenszustand DARF NICHT ungeprüft über
eine Grenze hinweg übernommen werden. `CP-derived` — CP 5.3, 7.5.

Die konkreten Grenzen sind in Kapitel 18 benannt.

### 3.9 Im Zweifel

Im Zweifel gilt die **niedrigere** Vertrauensebene. `CP-derived` — CP 6.3.

Lässt sich eine Handlung nicht eindeutig einer Wirkungsstufe zuordnen, gilt die
**höhere** Stufe. `CP-derived` — CP Kap. 0 („Auslegungsregel").

---

## 4. Identity Architecture

Dieses Kapitel beschreibt konzeptionell, welche Akteursarten die
Sicherheitsarchitektur unterscheiden muss. Es weist keine Rechte zu und legt
kein Authentifizierungsverfahren fest.

### 4.1 Der zentrale Trennungsgrundsatz

> **Identität erzeugt nicht automatisch Vertrauen.**
> **Vertrauen erzeugt nicht automatisch Berechtigung.**
> **Berechtigung erzeugt nicht automatisch menschliche Autorität.**

Diese drei Trennungen MÜSSEN in jeder zukünftigen Sicherheitsarchitektur von
JOCHEN X erhalten bleiben. `CP-derived` — CP 5.3, 6.2 („Verhältnis zur
menschlichen Freigabe"), 7.4, Artikel 1, Artikel 5.

Ergänzend gilt: **Herkunft** ist weder Identität noch Vertrauensebene noch
Berechtigung. Die Eigenschaft „lokal" oder „extern" beschreibt, wo etwas
herkommt — nicht, was es darf. `CP-derived` — CP 5.3 („Die Herkunft einer
Anfrage begründet allein keine Berechtigung").

**Lokal ist keine Vertrauensebene.** Die lokale Vertrauensdomäne (CP Kap. 0) ist
ein Schutzbereich, kein Vertrauensrang. Ein Akteur wird nicht dadurch
vertrauenswürdig, dass er innerhalb dieser Domäne ausgeführt wird.
`CP-derived` — CP 5.3, CP Kap. 0.

### 4.2 Akteursarten

Die folgende Aufstellung ist konzeptionell und nicht abschließend. Sie ordnet
keine Vertrauensebenen zu.

| Akteursart | Sicherheitsarchitektonische Einordnung |
|---|---|
| **Eigentümer** | Der Mensch, dem das System gehört. Einziger Träger der Ebene „Eigentümer" (CP 6.2) und einzige Quelle menschlicher Autorität (Artikel 1). |
| **Benutzer** | Ein menschlicher Akteur ohne Eigentümerstellung. Sein Nachweisstand bestimmt seine Vertrauensebene nach CP 6.2. |
| **Geräte** | Sachen, an denen ein Nachweis erbracht werden kann. Ein Gerät ist niemals selbst Autorität; ein Gerätenachweis ist ein Beitrag zu einem Identitätsnachweis, nicht dessen Ersatz. `architecture-open` **AO-06** |
| **Agenten** | Nicht-menschliche, weisungsgebundene Akteure, die im Auftrag handeln. Ihre Vertrauensebene begründet keine eigenständige Handlungsbefugnis (CP 6.2). |
| **Plugins** | Erweiterungen im Sinne der bestehenden Plugin-Governance (ADR-005, ADR-006, ADR-007, ADR-011). Siehe Kapitel 11. |
| **Lokale Dienste** | Bestandteile innerhalb der lokalen Vertrauensdomäne. Ihre Lage begründet kein Vertrauen (CP 5.3). |
| **Externe Dienste** | Bestandteile außerhalb der lokalen Vertrauensdomäne. Gäste, niemals Kernbestandteil (CP 5.2). |
| **Externe KI-Systeme** | Werkzeuge. Siehe Kapitel 9. |
| **Broker** | Externe Dienste mit finanzieller Wirkung. Siehe Kapitel 14. |
| **Börsen** | Externe Dienste mit finanzieller Wirkung. Siehe Kapitel 14. |
| **Datenquellen** | Lieferanten von Informationen. Informationsquelle, niemals Autorität (CP 7.7). |

### 4.3 Was dieses Kapitel nicht festlegt

Verfahren der Identitätsfeststellung, Identitätsträger, Lebensdauer von
Identitäten, Zuordnung mehrerer Identitäten zu einer Person sowie das Verhältnis
zwischen einer Identität und einem konkreten Nachweismittel sind **nicht**
entschieden. `architecture-open` **AO-07**.

---

## 5. Human Authority & Owner Trust

Dies ist die zentrale Sicherheitsdomäne von JOCHEN X.

### 5.1 Unveränderlicher Grundsatz

**Kein technischer Nachweis DARF die menschliche Autorität ersetzen.**
`CP-derived` — CP 5.1, 8.5, 8.6, Artikel 1.

Ein Nachweis kann belegen, **wer** handelt. Er kann niemals ersetzen, **dass**
ein Mensch entscheidet. Ein System, das aufgrund eines erfolgreichen Nachweises
eine Entscheidung selbst trifft, die dem Menschen zusteht, verletzt Artikel 1 —
unabhängig von der Qualität des Nachweises. `CP-derived` — CP 5.1, 6.2, 8.5.

Handlungen mit erheblicher oder kritischer Wirkung setzen unabhängig von der
erreichten Vertrauensebene eine menschliche Bestätigung voraus. `CP-derived` —
CP 6.2 („Verhältnis zur menschlichen Freigabe"), CP 5.10.

### 5.2 Mehrfachnachweis als Zukunftsrichtung

JOCHEN X SOLL langfristig mehrere voneinander unabhängige Nachweise kombinieren
können, um die Identität des Eigentümers mit einer der Wirkungsstufe
angemessenen Sicherheit festzustellen. `CP-derived` — CP 6.3 (Nachweisaufwand
steigt mit der Tragweite), CP 7.4.

Als **mögliche** zukünftige Nachweisrichtungen kommen in Betracht:

- Stimme
- Kamera
- Gesicht
- Smartphone
- lokale Anwesenheit
- Kombinationen mehrerer der vorstehenden Nachweise

Diese Aufzählung ist **keine technische Anforderung**, keine Auswahl und keine
Zusage. Sie benennt Richtungen, über die später zu entscheiden ist.
`architecture-open` **AO-08**.

### 5.3 Grenzen des Mehrfachnachweises

Auch ein vollständig erfolgreicher Mehrfachnachweis

- begründet keine autonome Entscheidungsbefugnis des Systems `CP-derived` — CP 8.5
- ersetzt keine nach CP 5.10 erforderliche Bestätigung `CP-derived` — CP 6.2
- verschiebt die Autonomiegrenze nach CP 8.5 nicht `CP-derived` — CP 6.2
- erzeugt keine dauerhafte Vertrauensebene `CP-derived` — CP 6.3 (Verfall)

Die Ebene „Kritische Freigabe" bleibt ein bewusst herbeigeführter
Ausnahmezustand für einen einzelnen Vorgang, zeitlich begrenzt und mit dem
Anlass endend. `CP-derived` — CP 6.2.

### 5.4 Nachweisverlust und Nachweisfälschung

Das System MUSS davon ausgehen, dass Identitätsbehauptungen gefälscht sein
können. `CP-derived` — CP 7.4.

Sicherheitsarchitektonische Konsequenz: Jeder zukünftige Nachweis SOLL so
entworfen werden, dass sein Ausfall oder seine Fälschung das System in einen
**restriktiveren**, nicht in einen freizügigeren Zustand versetzt.
`CP-derived` — CP 7.1 („sicherer Zustand ist dem funktionsfähigen vorzuziehen"),
CP 6.3 („im Zweifel die niedrigere Vertrauensebene").

Das Verfahren zur Wiederherstellung der Eigentümerstellung nach Verlust
sämtlicher Nachweismittel ist nicht entschieden und berührt zugleich Kapitel 17.
`architecture-open` **AO-09**.

---

## 6. Critical Actions

### 6.1 Maßstab

Der Maßstab für die Schutzbedürftigkeit einer Handlung ist ausschließlich die in
den Core Principles bestimmte Wirkungsstufe:

**bedeutsam < erheblich < kritisch**

Dieses Dokument führt **keine** zweite Risikoskala ein. Insbesondere wird die
Skala *Low → Medium → High → Critical* **nicht** als normative Skala von
JOCHEN X verwendet. `CP-derived` — CP Kap. 0 („Tragweite … Ein zweites
Maßsystem besteht nicht"), Development Standard v1.1 §2.3.

Sollte eine spätere technische Risikoanalyse feinere Kategorien benötigen, sind
diese ausdrücklich als **nicht-normative Analysekategorien** zu kennzeichnen
oder in einem eigenständigen Security Risk Framework zu behandeln. Eine solche
Analyse DARF NICHT die Wirkungsstufen der Core Principles ersetzen, ergänzen
oder umdeuten. `architecture-open` **AO-10**.

### 6.2 Beispielhafte Sicherheitsdomänen

Die folgende Aufstellung ordnet Sicherheitsdomänen **beispielhaft** ein. Sie ist
weder abschließend noch eine normative Klassifikation; die Einordnung im
Einzelfall folgt der Wirkungsdefinition der Core Principles (Reichweite und
Umkehrbarkeit) und der Auslegungsregel „im Zweifel die höhere Stufe".

| Sicherheitsdomäne | Typische Einordnung | Tragende Merkmale nach CP Kap. 0 |
|---|---|---|
| **Informationszugriff** | bedeutsam bis kritisch | Erhöht sich mit der Sensibilität der Information (CP Kap. 0, „Sensibel") |
| **Dateiveränderung** | bedeutsam bis erheblich | Erheblich, sobald nicht mit vertretbarem Aufwand umkehrbar |
| **Externe Kommunikation** | erheblich | Verlässt die lokale Vertrauensdomäne |
| **Systemänderungen** | erheblich bis kritisch | Umkehrbarkeit und Auswirkung auf den Systembestand |
| **Sicherheitsänderungen** | kritisch | Verändert Berechtigungen, Identitäten, Vertrauensebenen oder Sicherheitsregeln; berührt Artikel 2 |
| **Wallet-Aktionen** | kritisch | Berührt den Bestand anvertrauter Mittel |
| **Kapitalbewegungen** | kritisch | Finanzielle Folgen, regelmäßig nicht umkehrbar |
| **Irreversible Aktionen** | mindestens erheblich, regelmäßig kritisch | Nicht mit vertretbarem Aufwand umkehrbar |

`CP-derived` — CP Kap. 0 („Wirkung", „Erhebliche Wirkung", „Kritisch",
„Auslegungsregel").

### 6.3 Folge der Einordnung

- **bedeutsam** — Der Eigentümer MUSS die Handlung kennen können, bevor sie
  wirksam wird; sie MUSS erklärbar sein. `CP-derived` — CP Kap. 0, CP 4.6.
- **erheblich** — Es MUSS eine ausdrückliche, informierte menschliche
  Bestätigung vorliegen. `CP-derived` — CP 5.10.
- **kritisch** — Es MUSS zusätzlich eine Kritische Freigabe im Sinne von
  CP 6.2 vorliegen; die Handlung MUSS nachvollziehbar sein. `CP-derived` —
  CP 9.6, Artikel 8.

Dieses Dokument legt **keine** Freigabemechanismen, keine Bestätigungsdialoge,
keine Fristen und keine technischen Verfahren fest. `architecture-open`
**AO-11**.

---

## 7. Local Trust Domain

### 7.1 Bestimmung

Die lokale Vertrauensdomäne ist in Core Principles Kapitel 0 bestimmt. Sie wird
hier referenziert, nicht neu bestimmt.

Sicherheitsarchitektonische Konsequenz: Die Grenze der lokalen
Vertrauensdomäne MUSS in jeder zukünftigen Architektur **bestimmbar** sein. Eine
Architektur, in der nicht feststellbar ist, ob ein Datum die Domäne verlassen
hat, ist mit CP 5.2 und Artikel 4 unvereinbar. `CP-derived` — CP 5.2,
Artikel 4.

### 7.2 Besonders schützenswerte Inhalte

Die folgenden Inhalte sind konzeptionell besonders schützenswert; ihr Verlust
oder ihre Offenlegung kann eine der in CP Kap. 0 („Kritisch") genannten
Grundlagen dauerhaft beeinträchtigen:

- private Schlüssel
- Wallet-Zugänge
- Passwörter
- API-Secrets
- Recovery-Daten
- Identitätsnachweise
- persönliche Memory-Daten
- Sicherheitsrichtlinien

`CP-derived` — CP 7.2, CP Kap. 0 („Sensibel", „Kritisch"), Artikel 4.

### 7.3 Konsequenzen

- Diese Inhalte DÜRFEN NICHT ohne Autorisierung die lokale Vertrauensdomäne
  verlassen. `CP-derived` — Artikel 4.
- Sie DÜRFEN NICHT beiläufig offengelegt werden — auch nicht in Protokollen,
  Fehlermeldungen, Diagnosedaten, Erklärungen oder Auditspuren. `CP-derived` —
  CP 7.2.
- Auch interne Komponenten erhalten nur Zugriff auf das, was sie benötigen.
  `CP-derived` — CP 4.4, CP 5.4.
- Sicherheitsrichtlinien sind selbst schützenswert: ihre Veränderung ist eine
  Sicherheitsänderung im Sinne von 6.2 und damit kritisch. `CP-derived` —
  CP Kap. 0 („Erhebliche Wirkung"), Artikel 2.

### 7.4 Nicht entschieden

Kryptografische Verfahren, Schlüsselverwaltung, Speichertechnologie,
Speicherorte, Verschlüsselung im Ruhezustand und Zugriffsprotokolle sind
**nicht** Gegenstand dieses Dokuments. `architecture-open` **AO-12**.

---

## 8. External Trust Domain

### 8.1 Grundsatz

> **Das Internet ist Informationsquelle, nicht Autorität.**

Externe Systeme können ausfallen, kompromittiert oder feindselig sein. Das
System behandelt jede externe Quelle als potenziell unzuverlässig.
`CP-derived` — CP 7.7.

Externe Systeme sind Gäste, niemals Bestandteile des Kerns. `CP-derived` —
CP 5.2.

### 8.2 Was externe Inhalte niemals bewirken

Ein externer Inhalt DARF NICHT allein dadurch, dass er empfangen, gelesen,
verarbeitet oder zitiert wird,

- Berechtigungen erzeugen oder erweitern `CP-derived` — Artikel 3, CP 7.7
- Sicherheitsregeln verändern `CP-derived` — Artikel 2, CP 7.7
- Geheimnisse erhalten `CP-derived` — Artikel 4, CP 7.2
- kritische Aktionen autorisieren `CP-derived` — Artikel 1, CP 7.6
- eine Vertrauensebene begründen oder erhöhen `CP-derived` — Artikel 5, CP 6.3

Dies gilt unabhängig davon, wie der Inhalt formuliert ist, welche Autorität er
behauptet und welche Vorautorisierung er geltend macht. `CP-derived` — CP 7.9.

### 8.3 Erfasste externe Systeme

Internet, Webseiten, APIs, Cloud-Dienste, externe LLMs, Plugins,
Nachrichtenquellen, Broker und Börsen. Die Aufzählung ist nicht abschließend;
maßgeblich ist, ob sich der Akteur außerhalb der lokalen Vertrauensdomäne
befindet. `CP-derived` — CP Kap. 0, CP 7.7.

### 8.4 Zulässige Nutzung

Externe Dienste DÜRFEN genutzt werden, wo sie einen klaren Vorteil bieten. Sie
DÜRFEN NICHT zur Voraussetzung der grundlegenden Funktionsfähigkeit werden.
`CP-derived` — CP 3.2, CP 10.3, CP 10.5.

Für jede externe Abhängigkeit MUSS ein Ausweg denkbar sein: Ersatz, Rückbau oder
Verzicht. `CP-derived` — CP 10.5, Artikel 10.

---

## 9. AI Trust Architecture

### 9.1 Grundsatz

> **KI-Modelle sind Werkzeuge, keine Autoritäten.**

`CP-derived` — CP 8.1, 8.5, 8.6, Artikel 1.

Ein externes Modell DARF NICHT JOCHEN-Berechtigungen erhöhen — weder die eigenen
noch die eines anderen Akteurs. `CP-derived` — Artikel 3, CP 7.7.

Ein Modellergebnis ist eine **Auskunft**, keine Anweisung und keine
Autorisierung. `CP-derived` — CP 7.6.

### 9.2 Orchestrierung mehrerer KI-Systeme

JOCHEN X SOLL langfristig verschiedene KI-Systeme orchestrieren können —
beispielsweise lokale Modelle, Cloud-Modelle oder spezialisierte Modelle.
Produktnamen wie *ChatGPT*, *Claude* oder *Cursor* erscheinen hier
ausschließlich als **Beispiele**; die Architektur bleibt technologieagnostisch
und legt sich auf keinen Anbieter und kein Modell fest. `CP-derived` —
CP 10.5 (Herstellerunabhängigkeit), Artikel 10.

### 9.3 Sicherheitsarchitektonische Konsequenzen

- Ein lokales Modell ist nicht deshalb vertrauenswürdiger, weil es lokal
  ausgeführt wird; Lokalität ist Herkunft, nicht Vertrauen. Ihr
  sicherheitsarchitektonischer Vorteil liegt in Souveränität und Vertraulichkeit
  (CP 4.3), nicht in einer höheren Vertrauensebene. `CP-derived` — CP 5.3,
  CP 4.3.
- Die Weitergabe von Eingaben an ein externes Modell verlässt die lokale
  Vertrauensdomäne und ist damit eine Handlung mit mindestens erheblicher
  Wirkung. `CP-derived` — CP Kap. 0 („Erhebliche Wirkung"), Artikel 4.
- Ein Modell DARF NICHT über die Zulässigkeit einer sicherheitsrelevanten
  Handlung entscheiden. Sicherheitsentscheidungen sind keine Modellaufgabe.
  `CP-derived` — CP 7.7, Artikel 2.
- Die Auswahl eines Modells für eine Aufgabe ist bei bedeutsamer Wirkung
  erklärbar zu machen. `CP-derived` — CP 4.6, CP 8.2.
- Modellergebnisse mit erkennbarer Unsicherheit MÜSSEN als unsicher
  gekennzeichnet werden. `CP-derived` — CP 4.5, CP 8.3.

### 9.4 Nicht entschieden

Auswahlkriterien, Routing zwischen Modellen, zulässige Datenkategorien je
Modellklasse, Umgang mit Modellausgaben als Eingabe weiterer Modelle sowie die
Bewertung von Modellvertrauenswürdigkeit sind nicht entschieden.
`architecture-open` **AO-13**.

---

## 10. Prompt & Instruction Security

### 10.1 Grundsatz

> **Inhalt erzeugt keine Autorität.**

Das System unterscheidet strikt zwischen Anweisungen seines Eigentümers und
Inhalten, die es lediglich verarbeitet. Verarbeitete Inhalte sind Daten, niemals
Befehle — unabhängig davon, wie sie formuliert sind. `CP-derived` — CP 7.6.

Die Grenze zwischen Anweisung und Inhalt ist eine **Sicherheitsgrenze**. Sie
DARF NICHT durch Formulierung, Formatierung, behauptete Autorität,
Verschleierung oder angebliche Vorautorisierung überschritten werden.
`CP-derived` — CP 7.9.

Wo diese Grenze berührt wird, gilt: nachfragen statt ausführen. `CP-derived` —
CP 7.9.

### 10.2 Bedrohungsklassen

Die folgenden Klassen sind für die zukünftige Sicherheitsarchitektur zu
berücksichtigen:

| Klasse | Kern der Bedrohung |
|---|---|
| Prompt Injection | Externer Inhalt versucht, unmittelbar als Anweisung zu wirken. |
| Indirekte Prompt Injection | Der Angriff erreicht das System über einen Umweg (Dokument, Webseite, Datenquelle, Werkzeugausgabe). |
| Social Engineering | Der Angriff richtet sich gegen den Menschen als Teil der Angriffsfläche. |
| Manipulierte Webseiten | Angreiferkontrollierter Inhalt an einer als harmlos wahrgenommenen Stelle. |
| Manipulierte Dokumente | Angreiferkontrollierter Inhalt in verarbeiteten Dateien. |
| Manipulierte Nachrichten | Angreiferkontrollierter Inhalt in eingehender Kommunikation. |
| Bösartige Plugins | Ein zugelassener Erweiterungsakteur handelt gegen den Eigentümer. |
| Kompromittierte Agenten | Ein zuvor legitimer nicht-menschlicher Akteur ist unter fremder Kontrolle. |

`CP-derived` — CP 7.6, 7.8, 7.9, 5.3.

### 10.3 Sicherheitsarchitektonische Konsequenzen

- Herkunft und Berechtigung einer Anweisung MÜSSEN feststehen, bevor sie als
  Anweisung behandelt wird. `CP-derived` — CP 7.6.
- Dringlichkeit ist niemals ein Grund, eine Prüfung zu überspringen.
  `CP-derived` — CP 7.8.
- Das System DARF NICHT selbst künstlichen Zeitdruck erzeugen; es stellt
  Tragweite klar dar und macht ungewöhnliche Vorgänge als ungewöhnlich
  erkennbar. `CP-derived` — CP 7.8.
- Ein Angriffsversuch bleibt ein Angriff, unabhängig von seiner Formulierung
  und unabhängig davon, ob er erfolgreich war. `CP-derived` — CP 7.9.

### 10.4 Nicht entschieden

Konkrete Gegenmaßnahmen — Erkennungsverfahren, Filterung, Kennzeichnung von
Inhaltsherkunft, Trennung von Anweisungs- und Datenkanälen, Rückfragestrategien
— werden hier **nicht** festgelegt. `architecture-open` **AO-14**.

---

## 11. Plugin & Agent Trust

### 11.1 Verhältnis zu bestehenden ADRs

Die Plugin-Sicherheit von JOCHEN X ist bereits durch genehmigte Artefakte
geregelt: **ADR-005** (Integrity Validation, APPROVED), **ADR-006**
(Permission Model, APPROVED), **ADR-007** (Dependency Resolution, APPROVED) und
**ADR-011** (SDK-Host-Integration, Accepted), eingebettet in Architecture Book
v2.0 §10 und §11.

Diese Artefakte werden hier **referenziert und abgegrenzt**. Sie werden durch
dieses Dokument nicht neu geschrieben, nicht ausgelegt, nicht ersetzt und nicht
ergänzt. `CP-derived` — CP Governance Rule 1.

### 11.2 Übereinstimmung mit den Core Principles

Die folgenden Merkmale der bestehenden Plugin-Governance sind mit den Core
Principles vereinbar und werden als Bestand bestätigt:

| Merkmal | Bestehende Quelle | Core-Principles-Bezug |
|---|---|---|
| Default Deny | ADR-006 D1 | CP 5.4, Artikel 5 |
| Explizite Berechtigung | ADR-006 D1, D2 | CP 5.4 |
| Least Privilege | ADR-006 D1, D4 | CP 5.4 |
| Prüfung vor Ausführung (Admission vor Aktivierung) | ADR-005 D1, ADR-006 D3, ADR-011 D3 | CP 5.6, Artikel 2 |
| Keine Ausnahme für hauseigene Erweiterungen | ADR-006 D1 | CP 5.3 |
| Manifest-only Discovery (kein Plugin-Code vor Prüfung) | ADR-001, ADR-011 | CP 5.6 |
| Isolation | ADR-009 / ADR-011 D2 | CP 5.8, CP 4.12 |

### 11.3 Sicherheitsarchitektonische Grundsätze für Erweiterungen und Agenten

Die folgenden Grundsätze gelten für **jeden** nicht-menschlichen Akteur, der im
System handelt — Plugin, Agent, Dienst oder Stellvertreter:

- **Keine Selbstaufwertung.** Ein Akteur DARF NICHT sich selbst eine höhere
  Vertrauensebene oder weitergehende Berechtigungen verschaffen. `CP-derived` —
  CP 7.5, CP 6.3, Artikel 5.
- **Keine transitive Autorität.** Die Berechtigung eines Akteurs DARF NICHT
  dadurch entstehen, dass ein anderer berechtigter Akteur ihn aufruft. Eine
  Kette DARF in Summe nicht mehr bewirken als jedes ihrer Glieder.
  `CP-derived` — CP 7.5.
- **Widerrufbarkeit.** Eine erteilte Berechtigung MUSS entziehbar sein.
  `CP-derived` — CP 6.3, CP 5.4.
- **Keine eigenständige Handlungsbefugnis.** Die Vertrauensebene eines
  nicht-menschlichen Akteurs begründet keine eigenständige Handlungsbefugnis;
  Handlungen mit erheblicher oder kritischer Wirkung setzen unabhängig davon
  eine menschliche Bestätigung voraus. `CP-derived` — CP 6.2.
- **Keine Erreichbarkeit der Eigentümerebene.** Kein nicht-menschlicher Akteur
  KANN die Ebene „Eigentümer" erreichen. `CP-derived` — CP 6.2, Artikel 1.

### 11.4 Festgestellte Spannungen

**Begriffskollision „Vertrauensebene".** Architecture Book v2.0 §11.3 und
`docs/security.md` führen `PluginTrustLevel` mit den Werten
UNTRUSTED → VERIFIED → TRUSTED | REJECTED und bezeichnen diese als *Trust
Levels*. Core Principles 6.2 führt die Vertrauensebenen Gast, Benutzer,
Verifizierter Benutzer, Eigentümer und Kritische Freigabe. Es handelt sich um
zwei sachlich verschiedene Konzepte unter derselben Bezeichnung: das eine ist
ein technischer Zulassungszustand einer Erweiterung, das andere ein
Vertrauensverhältnis eines Akteurs. Beide Artefakte sind geschützt
(Architecture Book v2.0 FROZEN; Core Principles APPROVED). Dieses Dokument löst
die Kollision **nicht** auf. → `governance-conflict` **GC-03**.

**Binäre Vertrauensgrenze.** Architecture Book v2.0 §11.4 bezeichnet die
Foundation als *Trusted* und den Plugin Space als *Untrusted*. Core Principles
5.3 bestimmt, dass auch interne Komponenten und das System selbst nicht per se
vertrauenswürdig sind. Architecture Book v2.0 bleibt nach Governance Rule 1 in
seiner eingefrorenen Fassung unberührt; das Verhältnis für zukünftige
Architecture-Book-Versionen ist nicht geklärt. → `governance-conflict`
**GC-04**.

**Rollenmodell.** Architecture Book v2.0 §11.1 modelliert
`Identity → Role → Permission`. Das Verhältnis zwischen dem dort geführten
Begriff *Role* und den Vertrauensebenen der Core Principles ist nicht bestimmt.
→ `governance-conflict` **GC-07**.

### 11.5 Nicht entschieden

Die Übertragung der Plugin-Sicherheitsmechanismen auf Agenten, die Frage einer
Vertrauensbewertung über die Lebensdauer eines Akteurs hinweg sowie die Behandlung
eines nachträglich kompromittierten, bereits zugelassenen Akteurs sind nicht
entschieden. `architecture-open` **AO-15**.

---

## 12. Memory Security

### 12.1 Grundsatz

> **Lernen verändert Wissen nicht automatisch in Berechtigung.**

Lernen DARF NICHT Sicherheitsgrenzen, Berechtigungen oder Grundprinzipien
verändern. `CP-derived` — CP 5.9, CP 11.2, Artikel 6.

Extern gelerntes Wissen DARF NICHT neue Autorität erzeugen. Erfahrung begründet
keine erweiterten Rechte; Gewohnheit ersetzt keine Autorisierung. `CP-derived` —
CP 11.2, Artikel 3, Artikel 6.

Gelerntes Wissen ist Eigentum des Benutzers: es MUSS einsehbar, korrigierbar,
exportierbar und löschbar sein. `CP-derived` — CP 3.3, CP 5.9, Artikel 9.

### 12.2 Konzeptionelle Unterscheidung von Wissensklassen

Die Sicherheitsarchitektur SOLL die folgenden Wissensklassen unterscheiden, weil
sie unterschiedliche Schutzbedürfnisse und unterschiedliche Herkunftsrisiken
tragen:

| Klasse | Kern | Vorherrschendes Risiko |
|---|---|---|
| **Öffentliches Wissen** | Allgemein verfügbar, nicht personenbezogen | Richtigkeit, nicht Vertraulichkeit |
| **Externes Wissen** | Aus einer Quelle außerhalb der lokalen Vertrauensdomäne übernommen | Manipulation der Quelle; indirekte Injection (Kap. 10) |
| **Projektdaten** | Arbeitskontext des Eigentümers | Vertraulichkeit und Integrität |
| **Persönliche Daten** | Person, Gewohnheiten, Beziehungen des Eigentümers | Privatsphäre (CP 4.4) |
| **Sensible Daten** | Sensibel im Sinne von CP Kap. 0 | Offenlegungsschaden |
| **Sicherheitsdaten** | Sicherheitsrichtlinien, Vertrauenszustände, Auditspuren | Manipulation; berührt Artikel 2 |
| **Geheimnisse** | Schlüssel, Zugänge, Nachweise (siehe 7.2) | Vollständiger Kontrollverlust; berührt Artikel 4 |

`CP-derived` — CP Kap. 0 („Sensibel"), CP 4.4, CP 7.2, CP 5.9.

### 12.3 Sicherheitsarchitektonische Konsequenzen

- Die **Herkunft** eines Wissensbestandteils MUSS erhalten bleiben; extern
  übernommenes Wissen MUSS als extern erkennbar bleiben. `CP-derived` —
  CP 3.3 (rückverfolgbares Lernen), CP 8.2.
- Wissen DARF NICHT als Anweisung wirken. Ein gespeicherter Inhalt bleibt Inhalt,
  auch wenn er aus dem eigenen Gedächtnis stammt. `CP-derived` — CP 7.6, 7.9.
- Der Übergang eines Wissensbestandteils in eine niedriger geschützte Klasse ist
  eine Handlung mit mindestens erheblicher Wirkung. `CP-derived` — CP Kap. 0.
- Sicherheitsdaten und Geheimnisse DÜRFEN NICHT Gegenstand desselben
  Lernmechanismus sein wie gewöhnliches Wissen. `CP-derived` — CP 11.2,
  Artikel 6.
- Das Gedächtnis ist Teil der Auditierbarkeit: Der Eigentümer MUSS erkennen
  können, was das System gelernt hat, und es verwerfen dürfen. `CP-derived` —
  CP 5.9.

### 12.4 Nicht entschieden

Speicherform, Struktur, Segmentierung, Lebensdauer, Löschsemantik,
Herkunftskennzeichnung und Zugriffsmodell des zukünftigen Memory sind nicht
entschieden. Die Memory Architecture ist ein eigenständiges zukünftiges
Dokument. `architecture-open` **AO-16**.

---

## 13. Multimodal Security

### 13.1 Rahmen

JOCHEN X SOLL langfristig multimodal arbeiten können. Betroffen sind auf
Architekturebene: Audio, Sprache, Kamera, Vision und Bildschirmverständnis.

### 13.2 Sicherheitsarchitektonische Einordnung

- **Jeder Sensoreingang ist Inhalt, nicht Anweisung.** Gesprochene, gezeigte
  oder auf dem Bildschirm dargestellte Inhalte sind Daten. Ihre Verarbeitung
  begründet keine Autorität. `CP-derived` — CP 7.6, 7.9.
- Sensordaten können **sensibel** im Sinne von CP Kap. 0 sein und unterliegen
  dann CP 7.2 und Artikel 4. `CP-derived` — CP Kap. 0, CP 7.2.
- Die Erfassung MUSS zweckgebunden und erkennbar erfolgen; es werden nur Daten
  erhoben, die für einen erkennbaren Zweck erforderlich sind. Vorratserfassung
  widerspricht CP 4.4. `CP-derived` — CP 4.4.
- Stille Hintergrunderfassung mit relevanter Wirkung widerspricht CP 4.5.
  `CP-derived` — CP 4.5.
- Eine multimodale Fähigkeit wird erst freigegeben, wenn ihr sicherer Betrieb
  gewährleistet ist. `CP-derived` — CP 5.6, Artikel 7.

### 13.3 Ausdrückliche Nicht-Festlegungen

Zukünftige Funktionen wie Sprach- oder Kameraidentifikation werden ausschließlich
als `architecture-open` **AO-17** geführt (siehe auch 5.2 / AO-08).

Dieses Dokument enthält **keine** biometrische Implementierung, **keine**
Festlegung auf Hardware und **keine** Überwachungsarchitektur. Eine dauerhafte,
anlasslose Erfassung von Personen ist von diesem Dokument nicht vorgesehen und
wäre an CP 4.1, 4.4 und 4.5 zu messen. `CP-derived` — CP 4.1, 4.4, 4.5.

---

## 14. Trading Security

### 14.1 Grundsatz

> **Simulation vor Realität.**

Jede Fähigkeit mit finanzieller Wirkung wird zuerst in einer folgenlosen
Umgebung erprobt. Der Standardzustand ist immer der folgenlose. `CP-derived` —
CP 9.1, 9.2.

### 14.2 Was JOCHEN X in diesem Bereich zukünftig darf

JOCHEN X KANN zukünftig Trading-Bots entwickeln, Strategien simulieren,
Ergebnisse analysieren, Bots vergleichen und Bots validieren. Diese Tätigkeiten
haben für sich genommen keine finanzielle Wirkung. `CP-derived` — CP 9.1
(Simulation als verbindlicher Nachweis).

### 14.3 Was daraus nicht folgt

> **Performance allein erzeugt keine Echtgeld-Autorität.**

Kein Simulationsergebnis, kein Benchmark und keine Erfolgsquote begründet die
Befugnis zu realem Handeln. Der Übergang von folgenlosem zu realem Handeln ist
eine bewusste, ausdrücklich autorisierte Entscheidung des Eigentümers — niemals
ein Konfigurationsdetail oder eine Nebenwirkung. `CP-derived` — CP 9.2,
Artikel 5.

### 14.4 Höchste Autoritätsanforderung

Wallet-Transfers und Kapitalbewegungen sind kritisch im Sinne von CP Kap. 0. Sie
erfordern eine Kritische Freigabe im Sinne von CP 6.2. `CP-derived` — CP 9.6,
CP Kap. 0.

Finanzielle Verantwortung ist nicht delegierbar. Das System handelt niemals aus
eigenem Antrieb mit fremdem Vermögen. `CP-derived` — CP 9.6.

### 14.5 Weitere abgeleitete Sicherheitsfolgen

- Ein Vorgang, dessen Risiko nicht bestimmbar ist, wird nicht ausgeführt.
  `CP-derived` — CP 9.3.
- Risikogrenzen werden nicht situativ gelockert. `CP-derived` — CP 9.3.
- Geschwindigkeit ist niemals ein Grund, Prüfung, Protokollierung oder
  Erklärbarkeit zu reduzieren. `CP-derived` — CP 9.5.
- Kein finanziell wirksamer Vorgang ohne nachvollziehbare Begründung.
  `CP-derived` — CP 9.5, Artikel 8.
- Die Trennung zwischen folgenloser und realer Umgebung ist selbst eine
  Sicherheitsgrenze; ihre Veränderung ist eine Sicherheitsänderung im Sinne von
  6.2. `CP-derived` — CP 9.2, CP Kap. 0.

### 14.6 Nicht entschieden

Dieses Dokument enthält **keine** Trading-Algorithmen, **keine**
Handelsstrategien, **keine** Börsen- oder Broker-Architektur, **keine**
Wallet-Technologie und **keine** Risikokennzahlen. `architecture-open`
**AO-18**.

---

## 15. Trading Bot Maturity

Das folgende Reifegradmodell wird als **zukünftige Architekturidee**
vorgeschlagen. Es ist **kein genehmigter Governance-Prozess**, keine
Freigabekette und keine Anforderung. `architecture-open` **AO-19**.

| Stufe | Inhalt |
|---|---|
| 1 | Entwicklung |
| 2 | Simulation |
| 3 | Historische Validierung |
| 4 | Benchmark |
| 5 | Paper Trading |
| 6 | Langzeitvalidierung |
| 7 | Menschliche Bewertung |
| 8 | Explizite Live-Autorisierung |

**Unabhängig von jeder Stufe gilt:** Das Erreichen einer Stufe erzeugt **keine**
Berechtigung. Die letzte Stufe ist keine Folge der vorherigen, sondern eine
eigenständige Entscheidung des Eigentümers. `CP-derived` — CP 9.2, CP 9.6,
Artikel 5.

Ob dieses Modell übernommen wird, wie viele Stufen es führt, welche Nachweise
eine Stufe verlangt und wer sie feststellt, ist nicht entschieden.
`architecture-open` **AO-19**.

---

## 16. Runtime & Resource Security

### 16.1 Grundsatz

> **Ressourcen können geteilt werden; Autorität wird nicht geteilt.**

Die Ausführung eines Vorgangs auf einer anderen Ressource verändert weder seine
Vertrauensebene noch seine Berechtigung noch die Zuständigkeit für die
Entscheidung. `CP-derived` — CP 5.1, 5.3, 7.5, Artikel 1, Artikel 3.

Der Ausbau auf weitere Ressourcen DARF NICHT dazu führen, dass eine Ressource
für den Systembetrieb unverzichtbar wird. `CP-derived` — CP 10.5, Artikel 10.

### 16.2 Ressourcenarten

Haupt-PC, lokaler Kleinrechner, weitere lokale Systeme, Server und VPS sind
**Beispiele**. Maßgeblich ist nicht die Bauart, sondern ob sich die Ressource
innerhalb oder außerhalb der lokalen Vertrauensdomäne befindet. `CP-derived` —
CP Kap. 0, CP 10.2, CP 10.3.

Eine Ressource außerhalb der lokalen Vertrauensdomäne unterliegt Kapitel 8.
`CP-derived` — CP 5.2, 10.3.

### 16.3 Rücksicht auf den Benutzer

JOCHEN X DARF die Benutzererfahrung nicht unangemessen beeinträchtigen. Die
Aufmerksamkeit und die Arbeitsfähigkeit des Benutzers sind zu schonende
Ressourcen. `CP-derived` — CP 4.10, CP 10.1.

Lang laufende Vorgänge wie Simulation und Überwachung SOLLEN perspektivisch
unabhängig vom interaktiven Betrieb weiterarbeiten können, ohne diesen zu
verdrängen. `CP-derived` — CP 4.10, CP 10.1.

### 16.4 Weitere abgeleitete Sicherheitsfolgen

- Ein ausgelagerter Vorgang MUSS derselben Prüfung unterliegen wie ein lokal
  ausgeführter. `CP-derived` — CP 5.3, 7.5.
- Der Ausfall einer zusätzlichen Ressource DARF NICHT die Grundfunktion des
  Systems beseitigen. `CP-derived` — CP 4.12, 10.7, Artikel 11.
- Ein lang laufender autonomer Vorgang DARF NICHT die Autonomiegrenze nach
  CP 8.5 überschreiten, nur weil er unbeaufsichtigt läuft. `CP-derived` —
  CP 8.5.

### 16.5 Nicht entschieden

Konkrete Ressourcensteuerung, Verteilung, Priorisierung, Planung, Isolation
zwischen Ressourcen und Kommunikationswege zwischen ihnen sind nicht
entschieden. Die Runtime Architecture ist ein eigenständiges zukünftiges
Dokument. `architecture-open` **AO-20**.

---

## 17. Emergency & Recovery

### 17.1 Grundsatz

> **Wenn JOCHEN X seine Sicherheitslage nicht zuverlässig beurteilen kann,
> findet keine kritische autonome Aktion statt.**

`CP-derived` — CP 7.1 („sicherer Zustand ist dem funktionsfähigen Zustand
vorzuziehen"), CP 8.5, CP 6.3 („im Zweifel die niedrigere Vertrauensebene"),
Artikel 1.

### 17.2 Konzepte

| Konzept | Sicherheitsarchitektonische Bedeutung | Herkunft |
|---|---|---|
| **Safe State** | Ein Zustand, in dem keine Handlung mit erheblicher oder kritischer Wirkung ausgeführt wird und die lokale Vertrauensdomäne geschützt bleibt. | `CP-derived` — CP 7.1, Artikel 4 |
| **Fail Secure** | Bei Ausfall einer Sicherheitsprüfung wird die Handlung nicht ausgeführt. Ein Prüfausfall DARF NICHT als Zustimmung gewertet werden. | `CP-derived` — CP 7.1, CP 5.6 |
| **Isolation** | Ein Fehler oder eine Kompromittierung bleibt örtlich begrenzt und reißt nicht das Ganze mit. | `CP-derived` — CP 4.12, CP 5.8 |
| **Recovery** | Geordnete Rückkehr in den Normalzustand. Schutz vor Datenverlust hat Vorrang vor Verfügbarkeit. | `CP-derived` — CP 10.7 |
| **Graceful Degradation** | Fällt eine Fähigkeit aus, verliert das System diese Fähigkeit — nicht seine Grundfunktion. | `CP-derived` — CP 4.12 |
| **Manual Override** | Der Eigentümer kann jede Entscheidung des Systems aufheben und jederzeit eingreifen. Diese Möglichkeit MUSS auch im beeinträchtigten Zustand bestehen. | `CP-derived` — CP 4.1, CP 6.2, Artikel 1 |
| **Auditability** | Auch Notfall- und Wiederherstellungsvorgänge hinterlassen eine Spur. | `CP-derived` — CP 4.8, Artikel 8 |

### 17.3 Weitere abgeleitete Sicherheitsfolgen

- Das System MUSS seinen eigenen beeinträchtigten Zustand erkennen und
  kommunizieren. `CP-derived` — CP 4.12, CP 10.7.
- Eine Sicherheitsregel DARF NICHT autonom aufgehoben werden, auch nicht zur
  Wiederherstellung der Funktionsfähigkeit. `CP-derived` — Artikel 2.
- Der Eigentümer KANN abweichend entscheiden; Artikel 2 untersagt allein die
  autonome, nicht die vom Eigentümer angeordnete Aufhebung. `CP-derived` —
  CP 7.1.
- Ein Wiederherstellungsvorgang, der Berechtigungen, Identitäten oder
  Vertrauenszustände verändert, ist eine Sicherheitsänderung und damit kritisch.
  `CP-derived` — CP Kap. 0.

### 17.4 Nicht entschieden

Auslösekriterien, Eskalationsstufen, Wiederherstellungsverfahren, Sicherung und
Rückspielung von Zuständen sowie das Verfahren nach vollständigem Verlust der
Nachweismittel (siehe AO-09) sind nicht entschieden. `architecture-open`
**AO-21**.

**Hinweis auf Bestand.** Architecture Book v2.0 §12 führt bereits Recovery
Levels, Recovery Handler, Strategien, Eskalation und Graceful Degradation für
die Core Runtime. Dieses Kapitel beschreibt die **sicherheitsarchitektonische**
Sicht und ändert die dortigen Festlegungen nicht. Siehe ESD-06.

---

## 18. Security Boundaries

Eine Sicherheitsgrenze ist der Punkt, an dem ein Vorgang von einem
Vertrauensverhältnis in ein anderes übergeht. An jeder Grenze MUSS eine erneute
Beurteilung stattfinden. `CP-derived` — CP 5.3, 7.5.

| ID | Grenze | Was an dieser Grenze sicherheitsarchitektonisch geschieht | Herkunft |
|---|---|---|---|
| **SB-01** | Mensch ↔ JOCHEN | Übergang von Autorität zu Ausführung. Nur hier entsteht menschliche Autorisierung. Das System DARF widersprechen, warnen und begründen — niemals übergehen. | `CP-derived` — CP 5.1, 5.10, Artikel 1 |
| **SB-02** | JOCHEN ↔ lokale Systeme | Übergang innerhalb der lokalen Vertrauensdomäne. Lage begründet kein Vertrauen; die Beurteilung entfällt nicht. | `CP-derived` — CP 5.3, 4.4 |
| **SB-03** | JOCHEN ↔ Plugins | Übergang zu einem zugelassenen, aber nicht vertrauenswürdigen Erweiterungsakteur. Prüfung vor Ausführung; keine Selbstaufwertung; keine transitive Autorität. | `CP-derived` — CP 5.4, 5.6, 7.5; Bestand: ADR-005, ADR-006, ADR-011 |
| **SB-04** | JOCHEN ↔ externe KI | Übergang zu einem Werkzeug ohne Autorität. Eingaben verlassen die lokale Vertrauensdomäne; Ausgaben sind Inhalt, nicht Anweisung. | `CP-derived` — CP 7.6, 7.7, Artikel 3 |
| **SB-05** | JOCHEN ↔ Internet | Übergang zu einer Informationsquelle ohne Autorität. Empfangener Inhalt ist niemals Befehl. | `CP-derived` — CP 7.6, 7.7, 7.9, Artikel 3 |
| **SB-06** | JOCHEN ↔ Trading | Übergang von folgenlosem zu potenziell finanziell wirksamem Handeln. Der folgenlose Zustand ist der Standard. | `CP-derived` — CP 9.1, 9.2 |
| **SB-07** | JOCHEN ↔ Wallet | Übergang zum Bestand anvertrauter Mittel. Höchste Autoritätsanforderung; Kritische Freigabe. | `CP-derived` — CP 9.6, CP 6.2, Artikel 9 |
| **SB-08** | JOCHEN ↔ Cloud | Verlassen der lokalen Vertrauensdomäne zugunsten fremder Infrastruktur. Begründet, begrenzt, sichtbar, rückführbar. | `CP-derived` — CP 10.3, 10.4, Artikel 4, Artikel 10 |
| **SB-09** | JOCHEN ↔ Sensoren | Eintritt von Umgebungsinhalt in das System. Sensordaten sind Inhalt und können sensibel sein. | `CP-derived` — CP 4.4, 4.5, 7.6, CP Kap. 0 |

Dieses Kapitel enthält **keine** Implementierungsdetails, keine Protokolle und
keine Schnittstellenfestlegungen. Die technische Ausgestaltung jeder Grenze ist
`architecture-open` **AO-22**.

---

## 19. Auditability

### 19.1 Grundsatz

Kritische Vorgänge hinterlassen eine belastbare Spur. Diese Spur ist gegen
nachträgliche Veränderung zu schützen und MUSS für den Eigentümer zugänglich
sein. `CP-derived` — CP 4.8, Artikel 8.

Auditierbarkeit dient der Kontrolle **des Systems durch den Benutzer**, nicht
der Kontrolle des Benutzers. `CP-derived` — CP 4.8.

### 19.2 Konzeptionell nachvollziehbare Informationen

Die folgenden Fragen MÜSSEN für einen kritischen Vorgang im Nachhinein
beantwortbar sein:

| Frage | Gegenstand | Herkunft |
|---|---|---|
| **Wer?** | Welcher Akteur hat gehandelt | `CP-derived` — CP 4.8 |
| **Was?** | Was geschah | `CP-derived` — CP 4.8 |
| **Wann?** | Zeitpunkt | `CP-derived` — CP 4.8 |
| **Warum?** | Auslöser und Begründung | `CP-derived` — CP 4.8, 5.5, 9.5 |
| **Welche Vertrauensebene?** | Auf welcher Ebene nach CP 6.2 gehandelt wurde | `CP-derived` — CP 6.2, 6.3 |
| **Welche Autorisierung?** | Ob und wie eine menschliche Bestätigung vorlag | `CP-derived` — CP 5.10, 9.6 |
| **Welche externe Quelle?** | Welche Inhalte von außerhalb der lokalen Vertrauensdomäne eingeflossen sind | `CP-derived` — CP 7.7, 8.2 |
| **Welche Entscheidung?** | Welche Alternativen bestanden und was gewählt wurde | `CP-derived` — CP 5.5 |
| **Welches Ergebnis?** | Wirkung des Vorgangs | `CP-derived` — CP 4.8 |

### 19.3 Grenzen

Die Auditspur DARF NICHT selbst zum Offenlegungsweg für sensible Informationen
werden. Sensible Informationen werden auch in Protokollen nicht beiläufig
offengelegt. `CP-derived` — CP 7.2.

Erklärbarkeit ist nicht dasselbe wie Protokollierung. Eine Spur, die nur
Fachleute lesen können, erfüllt CP 4.6 nur teilweise; das Ziel ist Verständnis,
nicht Beleglage. `CP-derived` — CP 4.6.

### 19.4 Nicht entschieden

Logging-Technologie, Speicherform, Aufbewahrungsdauer, Manipulationsschutz,
Zugriffsweg und Darstellung sind nicht entschieden. `architecture-open`
**AO-23**.

**Hinweis auf Bestand.** Architecture Book v2.0 §13.4 und `docs/security.md`
führen bereits Audit-Hooks und Security-Events. Siehe ESD-05.

---

## 20. Verification Objectives

Dieses Kapitel definiert ausschließlich **spätere Nachweisziele** — was zu einem
späteren Zeitpunkt nachweisbar sein soll. Es enthält keine Testfälle, keine
Prüfkriterien und keine Verifikationsverfahren.

| ID | Nachweisziel | Bezug |
|---|---|---|
| **VO-01** | Kein Akteur erlangt Berechtigungen ohne ausdrückliche Erteilung. | SO-04, SO-05, Artikel 5 |
| **VO-02** | Kein externes System erweitert Berechtigungen. | SO-03, Artikel 3 |
| **VO-03** | Kritische Geheimnisse verlassen die lokale Vertrauensdomäne nicht ohne Autorisierung. | SO-02, SO-06, Artikel 4 |
| **VO-04** | Handlungen mit erheblicher oder kritischer Wirkung sind menschlich autorisiert. | SO-01, SO-05, Artikel 1 |
| **VO-05** | Simulation und Realität sind wirksam getrennt; der folgenlose Zustand ist der Standard. | SO-14, CP 9.1, 9.2 |
| **VO-06** | Externe KI-Systeme besitzen keine Autorität und treffen keine Sicherheitsentscheidungen. | SO-03, SO-13, Artikel 3 |
| **VO-07** | Kritische Aktionen sind im Nachhinein vollständig nachvollziehbar. | SO-09, Artikel 8 |
| **VO-08** | Wiederherstellung führt in einen sicheren Zustand und hebt keine Sicherheitsregel autonom auf. | SO-11, SO-12, Artikel 2 |
| **VO-09** | Verarbeitete Inhalte wirken zu keinem Zeitpunkt als Anweisung. | SO-13, CP 7.6, 7.9 |
| **VO-10** | Lernen verändert keine Sicherheitsgrenze, keine Berechtigung und kein Grundprinzip. | SO-04, Artikel 6 |
| **VO-11** | Identität, Vertrauensebene, Herkunft, Berechtigung und Autorität bleiben getrennt. | SO-13, CP 5.3, 6.2 |
| **VO-12** | Ein Widerruf von Vertrauen wirkt vollständig und ohne Restwirkung. | SO-03, CP 6.3 |

Wann, durch wen und mit welchen Mitteln diese Ziele nachzuweisen sind, ist
**nicht** entschieden und richtet sich nach dem Development Standard sowie nach
zukünftigen Engineering Specifications. `architecture-open` **AO-24**.

Der Milestone 1.0 Implementation Plan hält in STR-03 fest, dass Security Tests
erst **nach** Definition einer Security Architecture und der zugehörigen
Security ADRs konkretisiert werden. Dieses Kapitel greift dem nicht vor: Es
benennt Ziele, keine Prüfungen. Siehe ESD-07.

---

## 21. Security Principles — Ableitungstabelle

Dieses Kapitel formuliert **keine neuen Verfassungsartikel**. Es weist
ausschließlich nach, welche sicherheitsarchitektonische Konsequenz sich aus
welchem Core Principle ergibt. Die Core Principles bleiben die normative Quelle.

| Core Principle | Sicherheitsarchitektonische Konsequenz | Status |
|---|---|---|
| **Human Authority** (CP 5.1, Art. 1) | Kein technischer Nachweis, keine Vertrauensebene und kein Automatisierungsgrad ersetzt die menschliche Letztentscheidung. Die Sicherheitsarchitektur hält den Menschen als Entscheidungspunkt strukturell offen (SB-01). | `CP-derived` |
| **Local Sovereignty** (CP 5.2, Art. 4) | Die Grenze der lokalen Vertrauensdomäne ist eine Sicherheitsgrenze und muss bestimmbar sein; ihr Überschreiten ist ein autorisierter, protokollierter Ausnahmefall (SB-05, SB-08). | `CP-derived` |
| **Zero Trust** (CP 5.3, Art. 5) | Kein Akteur ist aufgrund von Herkunft, Lage oder Nutzungsdauer vertrauenswürdig. An jeder Vertrauensgrenze wird neu beurteilt (Kap. 3.8, Kap. 18). | `CP-derived` |
| **Least Privilege** (CP 5.4) | Rechte werden minimal, befristet und widerruflich erteilt; sie wachsen nicht durch Gewohnheit (Kap. 11.3). | `CP-derived` |
| **Human Confirmation** (CP 5.10) | Erhebliche und kritische Wirkung setzt informierte, anlassbezogene Bestätigung voraus; Zustimmung überträgt sich nicht auf Folgevorgänge (Kap. 6.3). | `CP-derived` |
| **Explainable Decisions** (CP 5.5, Art. 8) | Was nicht erklärbar ist, darf nicht kritisch sein; der Erklärungsaufwand folgt der Wirkungsstufe (Kap. 19). | `CP-derived` |
| **Safety before Capability** (CP 5.6, Art. 7) | Eine Sicherheitsprüfung wird niemals übersprungen, um eine Fähigkeit früher verfügbar zu machen (Kap. 11.2, Kap. 13.2). | `CP-derived` |
| **Continuous Learning** (CP 5.9, Art. 6) | Lernen erzeugt kein Recht; Wissen ist niemals Berechtigung; Sicherheitsdaten unterliegen nicht dem gewöhnlichen Lernmechanismus (Kap. 12). | `CP-derived` |
| **Trust Model** (CP 6.2, 6.3) | Vertrauen ist erworben, kontextabhängig, befristet und widerruflich; die fünf Ebenen bleiben unverändert (Kap. 3). | `CP-derived` |
| **Schutz sensibler Informationen** (CP 7.2, Art. 4) | Geheimnisse und sensible Daten verlassen die lokale Vertrauensdomäne nicht ohne Autorisierung und erscheinen nicht in Protokollen (Kap. 7, Kap. 19.3). | `CP-derived` |
| **Schutz vor Manipulation** (CP 7.3) | Das System muss Veränderungen an Bestandteilen, Regeln und Aufzeichnungen erkennen können (SO-07). | `CP-derived` |
| **Schutz vor Identitätsmissbrauch** (CP 7.4) | Identitätsbehauptungen werden geprüft, nicht geglaubt; Nachweisausfall führt in den restriktiveren Zustand (Kap. 5.4). | `CP-derived` |
| **Schutz vor Rechteausweitung** (CP 7.5, Art. 3) | Keine Selbstaufwertung, keine transitive Autorität, keine Rechteerweiterung durch Verkettung (Kap. 11.3, Kap. 16.1). | `CP-derived` |
| **Schutz vor unautorisierten Befehlen** (CP 7.6) | Verarbeitete Inhalte sind Daten, niemals Befehle; Herkunft und Berechtigung stehen vor der Ausführung fest (Kap. 10). | `CP-derived` |
| **Schutz vor externer Einflussnahme** (CP 7.7, Art. 3) | Externe Systeme liefern Information, niemals Autorität, Regeln oder Sicherheitsentscheidungen (Kap. 8, Kap. 9). | `CP-derived` |
| **Schutz vor Social Engineering** (CP 7.8) | Dringlichkeit rechtfertigt keine Prüfungsverkürzung; das System erzeugt selbst keinen Zeitdruck (Kap. 10.3). | `CP-derived` |
| **Prompt- und Command-Manipulation** (CP 7.9) | Die Grenze zwischen Anweisung und Inhalt ist eine Sicherheitsgrenze; bei Berührung gilt: nachfragen statt ausführen (Kap. 10). | `CP-derived` |
| **Kein autonomer Entscheider** (CP 8.5) | Autonomie endet, wo Folgen schwer umkehrbar sind — auch bei unbeaufsichtigtem Dauerbetrieb (Kap. 16.4). | `CP-derived` |
| **Simulation vor Realität** (CP 9.1, 9.2) | Der folgenlose Zustand ist der Standard; der Übergang zur Realität ist eine eigenständige Autorisierung, keine Folge von Performance (Kap. 14, Kap. 15). | `CP-derived` |
| **Menschliche Verantwortung im Finanzbereich** (CP 9.6, Art. 9) | Kapitalbewegungen sind kritisch und erfordern eine Kritische Freigabe; das System handelt nie aus eigenem Antrieb mit fremdem Vermögen (Kap. 14.4). | `CP-derived` |
| **Resilienz und Ausfallsicherheit** (CP 4.12, 10.7, Art. 11) | Fehler bleiben lokal begrenzt; das System erkennt und benennt seinen beeinträchtigten Zustand; Datenverlustschutz vor Verfügbarkeit (Kap. 17). | `CP-derived` |
| **Herstellerunabhängigkeit** (CP 10.5, Art. 10) | Für jede externe Abhängigkeit muss ein Ausweg denkbar sein; keine Ressource wird unverzichtbar (Kap. 8.4, Kap. 16.1). | `CP-derived` |
| **Auditierbarkeit** (CP 4.8, Art. 8) | Kritische Vorgänge hinterlassen eine geschützte, für den Eigentümer zugängliche Spur (Kap. 19). | `CP-derived` |
| **Unantastbarkeit der Sicherheitsregeln** (Art. 2) | Keine Sicherheitsregel wird autonom aufgehoben — auch nicht im Notfall, auch nicht zur Wiederherstellung (Kap. 17.3). | `CP-derived` |
| **Stewardship** (CP 4.13, Art. 9) | Aus Verwaltung erwächst kein Anspruch; anvertraute Mittel und Zugänge bleiben fremdes Eigentum (Kap. 14.4). | `CP-derived` |

---

## 22. Architectural Boundaries

Dieses Dokument entscheidet **ausdrücklich nicht** über:

- konkrete Hardware
- konkrete Software
- konkrete Cloudanbieter
- konkrete LLMs
- konkrete Kryptografie
- konkrete Datenbanken
- konkrete APIs
- konkrete Netzwerkarchitektur
- konkrete Authentifizierungsverfahren
- konkrete biometrische Verfahren
- konkrete Trading-Algorithmen
- konkrete Security Controls

Diese Entscheidungen gehören in spätere Architektur-, ADR- und
Engineering-Dokumente.

**Weitere ausdrückliche Nicht-Entscheidungen dieses Dokuments:**

- Es erzeugt **keinen** neuen ADR und ändert **keinen** bestehenden ADR.
- Es ändert **kein** genehmigtes oder eingefrorenes Dokument.
- Es definiert **keinen** Milestone-Scope und **kein** Arbeitspaket.
- Es nimmt **keine** Governance-Entscheidung vorweg — insbesondere nicht die
  Rangeinordnung dieser Dokumentklasse (GC-01).
- Es trifft **keine** Aussage über den gegenwärtigen Implementierungsstand der
  Sicherheit von JOCHEN X.
- Es enthält **keine** Verifikationsverfahren und **keine** Testfälle.

---

## 23. Traceability

Die folgende Kette weist die Herkunft der Sicherheitsdomänen dieses Dokuments
nach. Sie erzeugt **keine** neuen normativen Anforderungen; sie macht die
Ableitung prüfbar.

**Core Principle → Security Consequence (Kap. 21) → Security Objective (Kap. 2)
→ Security Domain (Kapitel) → zukünftige Architekturentscheidung**

| Core Principle | Konsequenz | Objective | Domäne | Zukünftige Entscheidung |
|---|---|---|---|---|
| CP 5.1 / Art. 1 | Autorität nicht ersetzbar | SO-01 | Kap. 5 Human Authority & Owner Trust; SB-01 | AO-08, AO-09 |
| CP 5.2 / Art. 4 | Domänengrenze ist Sicherheitsgrenze | SO-02 | Kap. 7 Local Trust Domain; SB-08 | AO-12 |
| CP 5.3 / Art. 5 | Kein Vertrauen aus Herkunft | SO-03, SO-13 | Kap. 3 Trust Architecture; Kap. 4 Identity | AO-02, AO-06, AO-07 |
| CP 5.4 | Minimale, befristete Rechte | SO-04 | Kap. 11 Plugin & Agent Trust | AO-15 |
| CP 5.10 / CP 6.2 | Anlassbezogene Bestätigung | SO-05 | Kap. 6 Critical Actions | AO-11 |
| CP 7.2 | Keine beiläufige Offenlegung | SO-06 | Kap. 7 Local Trust Domain; Kap. 19.3 | AO-12, AO-23 |
| CP 7.3 | Erkennbarkeit von Veränderung | SO-07 | Kap. 7; Kap. 19 | AO-23 |
| CP 3.2 / CP 10.4 | Verfügbarkeit ohne Kontrollverlust | SO-08 | Kap. 8 External Trust Domain; Kap. 16 | AO-20 |
| CP 4.8 / Art. 8 | Geschützte Spur | SO-09 | Kap. 19 Auditability | AO-23 |
| CP 4.6 / CP 5.5 | Erklärbarkeit nach Tragweite | SO-10 | Kap. 6; Kap. 19 | AO-11 |
| CP 4.12 / Art. 11 | Degradation statt Zusammenbruch | SO-11 | Kap. 17 Emergency & Recovery | AO-21 |
| CP 10.7 | Geordnete Rückkehr | SO-12 | Kap. 17 | AO-21 |
| CP 5.3 / CP 6.2 / CP 7.4 | Trennung der Konzepte | SO-13 | Kap. 4 Identity Architecture | AO-07 |
| CP 9.1 / CP 9.2 | Folgenlos als Standard | SO-14 | Kap. 14 Trading Security; Kap. 15 | AO-18, AO-19 |
| CP 7.6 / CP 7.9 | Inhalt ist kein Befehl | SO-03, SO-13 | Kap. 10 Prompt & Instruction Security | AO-14 |
| CP 7.7 / Art. 3 | Extern ohne Autorität | SO-03 | Kap. 8; Kap. 9 AI Trust | AO-13 |
| CP 5.9 / CP 11.2 / Art. 6 | Lernen ohne Rechtewirkung | SO-04, SO-13 | Kap. 12 Memory Security | AO-16 |
| CP 4.4 / CP 4.5 | Zweckbindung und Sichtbarkeit | SO-06 | Kap. 13 Multimodal Security | AO-17 |
| CP 10.1 / CP 10.5 / Art. 10 | Ressourcen ohne Autoritätsübertragung | SO-02, SO-08 | Kap. 16 Runtime & Resource Security | AO-20 |
| Art. 2 | Keine autonome Aufhebung | SO-01, SO-12 | Kap. 17.3 | AO-21 |

---

## 24. Findings & Open Questions

### 24.1 Governance Conflicts

Die folgenden Konflikte werden **dokumentiert, nicht entschieden**. Die
Entscheidung obliegt der Genehmigungsinstanz.

| ID | Gegenstand | Beschreibung | Betroffene Artefakte |
|---|---|---|---|
| **GC-01** | Rangeinordnung dieser Dokumentklasse | Die Klasse „Security Architecture / Trust Framework" ist weder in der Rangordnung der Core Principles (Kap. 0, 12 Klassen) noch in Development Standard v1.1 §3.1–§3.3 geführt. Die Tabelle „Single Authoritative Source" (DevStd §2.1) weist die Domäne „Architektur" dem eingefrorenen Architecture Book zu und kennt keine Domäne „Sicherheitsarchitektur". Zugleich nennt Core Principles Governance Rule 2 die Security Architecture ausdrücklich als gebundenes zukünftiges Dokument, und Governance Closing W-7 autorisiert ihre Erstellung. Die Rangstufe ist damit nicht ableitbar. | Core Principles 1.0 Kap. 0; Development Standard v1.1 §2.1, §3.1–§3.3; Governance Closing W-7 |
| **GC-02** | Governance-Status von `docs/security.md` | Das Dokument trägt keine Statusangabe, keine Version, kein Datum und keine Genehmigungsangabe. Es ist weder in der Referenzliste der Core Principles noch in den Dokumentklassen des Development Standard geführt. Seine Verbindlichkeit und seine Zugehörigkeit zum geschützten Bestand nach Governance Rule 1 sind ungeklärt. | `docs/security.md`; Core Principles Governance Rule 1; Development Standard v1.1 §3 |
| **GC-03** | Begriffskollision „Vertrauensebene" / „Trust Level" | Architecture Book v2.0 §11.3 und `docs/security.md` führen `PluginTrustLevel` (UNTRUSTED → VERIFIED → TRUSTED \| REJECTED) als *Trust Levels*. Core Principles 6.2 führt die Vertrauensebenen Gast, Benutzer, Verifizierter Benutzer, Eigentümer, Kritische Freigabe. Zwei sachlich verschiedene Konzepte tragen dieselbe Bezeichnung. Beide Quellen sind geschützt. Eine Auflösung ist ohne Änderung eines geschützten Artefakts nicht möglich. | Architecture Book v2.0 §11.3; `docs/security.md`; Core Principles 6.2 |
| **GC-04** | Binäre Vertrauensgrenze | Architecture Book v2.0 §11.4 bezeichnet die Foundation als *Trusted* und den Plugin Space als *Untrusted*. Core Principles 5.3 bestimmt, dass auch interne Komponenten und das System selbst nicht per se vertrauenswürdig sind. Architecture Book v2.0 bleibt nach Governance Rule 1 unberührt; das Verhältnis für zukünftige Architecture-Book-Versionen ist offen. | Architecture Book v2.0 §11.4; Core Principles 5.3, Governance Rule 1 |
| **GC-05** | ADR-Status „Resolved by" | ADR-004, ADR-008 und ADR-009 tragen den Status „Resolved by ADR-0xx". Development Standard v1.1 §5 („Approved ADRs") kennt akzeptierte ADRs als Teil der Baseline und offene ADRs (Status: Open) als nicht implementierungsfähig. „Resolved by" ist keiner dieser Kategorien zugeordnet. Die Zugehörigkeit dieser ADRs zum geschützten Bestand ist ungeklärt. | ADR-004, ADR-008, ADR-009; Development Standard v1.1 §5 |
| **GC-06** | Uneinheitliche Statusbezeichnungen | ADR-001, -002, -003, -010 und -011 tragen „Accepted"; ADR-005, -006 und -007 tragen „APPROVED". Die Referenzliste der Core Principles führt ADR-011 als „APPROVED", die Datei selbst als „Accepted (v0.8.0)". Ob „Accepted" und „APPROVED" denselben Governance-Status bezeichnen, ist nicht bestimmt. | ADR-001 bis ADR-011; Core Principles 1.0 Referenzen |
| **GC-07** | Verhältnis „Role" ↔ Vertrauensebene | Architecture Book v2.0 §11.1 modelliert `Identity → Role → Permission`. Core Principles 6.2 führt Vertrauensebenen und trennt Identität, Vertrauensebene und Berechtigung. Das Verhältnis zwischen *Role* und Vertrauensebene ist in keinem Artefakt bestimmt. | Architecture Book v2.0 §11.1; Core Principles 6.2 |

**Kein Konflikt wird durch dieses Dokument geschlossen.** Kein bestehendes
Artefakt wurde zur Auflösung dieser Konflikte verändert.

### 24.2 Architecture Open Questions

| ID | Offene Frage | Kapitel |
|---|---|---|
| **AO-01** | Gewichtung, Messbarkeit und Zielerreichung der Sicherheitsziele | 2 |
| **AO-02** | Welche Nachweisarten für welche Wirkungsstufe genügen | 3.3 |
| **AO-03** | Form des Vertrauensentzugs und seine Ausbreitung über laufende Vorgänge | 3.4 |
| **AO-04** | Fristen, Auslöser und Wirkung des Vertrauensverfalls | 3.5 |
| **AO-05** | Zulässigkeit und Form begrenzter Delegation zwischen nicht-menschlichen Akteuren | 3.7 |
| **AO-06** | Rolle des Gerätenachweises innerhalb eines Identitätsnachweises | 4.2 |
| **AO-07** | Identitätsfeststellung, Identitätsträger, Lebensdauer, Mehrfachidentitäten | 4.3 |
| **AO-08** | Zukünftige Nachweisrichtungen für den Eigentümer (Stimme, Kamera, Gesicht, Smartphone, lokale Anwesenheit, Kombinationen) | 5.2 |
| **AO-09** | Wiederherstellung der Eigentümerstellung nach Verlust aller Nachweismittel | 5.4, 17.4 |
| **AO-10** | Umgang mit feineren, nicht-normativen Risikokategorien in einer späteren Risikoanalyse | 6.1 |
| **AO-11** | Freigabemechanismen, Bestätigungsform, Fristen für erhebliche und kritische Handlungen | 6.3 |
| **AO-12** | Kryptografie, Schlüsselverwaltung, Speichertechnologie und Speicherorte der lokalen Vertrauensdomäne | 7.4 |
| **AO-13** | Modellauswahl, Routing, zulässige Datenkategorien je Modellklasse, Kettung von Modellausgaben | 9.4 |
| **AO-14** | Gegenmaßnahmen gegen Prompt- und Instruction-Angriffe | 10.4 |
| **AO-15** | Übertragung der Plugin-Sicherheitsmechanismen auf Agenten; Umgang mit nachträglich kompromittierten Akteuren | 11.5 |
| **AO-16** | Speicherform, Segmentierung, Lebensdauer, Löschsemantik und Herkunftskennzeichnung des Memory | 12.4 |
| **AO-17** | Sprach- und Kameraidentifikation als zukünftige Funktion | 13.3 |
| **AO-18** | Trading-Algorithmen, Börsen-/Broker-Architektur, Wallet-Technologie, Risikokennzahlen | 14.6 |
| **AO-19** | Übernahme, Stufenzahl und Nachweise des Trading-Bot-Reifegradmodells | 15 |
| **AO-20** | Ressourcensteuerung, Verteilung, Priorisierung, Isolation zwischen Ressourcen | 16.5 |
| **AO-21** | Notfallauslöser, Eskalationsstufen, Wiederherstellungsverfahren, Zustandssicherung | 17.4 |
| **AO-22** | Technische Ausgestaltung der Sicherheitsgrenzen SB-01 bis SB-09 | 18 |
| **AO-23** | Logging-Technologie, Aufbewahrung, Manipulationsschutz, Zugriffsweg der Auditspur | 19.4 |
| **AO-24** | Zeitpunkt, Zuständigkeit und Mittel der späteren Verifikation | 20 |

### 24.3 CP-Derived Decisions

Die folgenden Aussagen sind direkt aus den Core Principles abgeleitet und
bilden den sicherheitsarchitektonischen Kern dieses Entwurfs. Sie sind keine
neuen Normen, sondern Konkretisierungen bestehender Normen.

| ID | Aussage | Fundstelle in den Core Principles | Kapitel |
|---|---|---|---|
| **CPD-01** | Kein technischer Nachweis ersetzt die menschliche Autorität. | 5.1, 8.5, 8.6, Artikel 1 | 5.1 |
| **CPD-02** | Identität, Vertrauen, Berechtigung und Autorität sind getrennte Konzepte; keines erzeugt automatisch ein anderes. | 5.3, 6.2, 7.4, Artikel 1, Artikel 5 | 4.1 |
| **CPD-03** | Herkunft — insbesondere „lokal" — ist keine Vertrauensebene. | 5.3, Kap. 0 | 4.1 |
| **CPD-04** | Die fünf Vertrauensebenen der Core Principles bleiben die einzigen Vertrauensebenen von JOCHEN X. | 6.2 | 3.1 |
| **CPD-05** | Die Wirkungsskala bedeutsam < erheblich < kritisch ist die einzige normative Skala; eine zweite wird nicht eingeführt. | Kap. 0 („Tragweite") | 6.1 |
| **CPD-06** | Externe Inhalte erzeugen weder Berechtigung noch Autorität noch Regeländerung. | 7.6, 7.7, 7.9, Artikel 3 | 8.2, 10.1 |
| **CPD-07** | KI-Modelle sind Werkzeuge, keine Autoritäten; ein externes Modell erhöht keine Berechtigung. | 8.1, 8.5, 8.6, Artikel 3 | 9.1 |
| **CPD-08** | Lernen erzeugt keine Berechtigung; extern gelerntes Wissen erzeugt keine Autorität. | 5.9, 11.2, Artikel 6 | 12.1 |
| **CPD-09** | Der folgenlose Zustand ist im Finanzbereich der Standardzustand; Performance erzeugt keine Echtgeld-Autorität. | 9.1, 9.2, 9.6 | 14.1, 14.3 |
| **CPD-10** | Ressourcen können geteilt werden; Autorität wird nicht geteilt. | 5.1, 5.3, 7.5, Artikel 1, Artikel 3 | 16.1 |
| **CPD-11** | Kann das System seine Sicherheitslage nicht zuverlässig beurteilen, findet keine kritische autonome Aktion statt. | 7.1, 8.5, 6.3, Artikel 1 | 17.1 |
| **CPD-12** | Keine Sicherheitsregel wird autonom aufgehoben — auch nicht zur Wiederherstellung der Funktionsfähigkeit. | Artikel 2, 7.1 | 17.3 |
| **CPD-13** | An jeder Vertrauensgrenze findet eine erneute Beurteilung statt; Vertrauen wird nicht ungeprüft übernommen. | 5.3, 7.5 | 3.8, 18 |
| **CPD-14** | Keine Selbstaufwertung und keine transitive Autorität für nicht-menschliche Akteure. | 7.5, 6.2, Artikel 5 | 11.3 |
| **CPD-15** | Kritische Vorgänge hinterlassen eine geschützte, dem Eigentümer zugängliche Spur; die Spur ist selbst kein Offenlegungsweg. | 4.8, 7.2, Artikel 8 | 19 |

### 24.4 Existing-System Dependencies

| ID | Bestehendes Artefakt | Abhängigkeit dieses Dokuments | Wirkung auf das Bestandsartefakt |
|---|---|---|---|
| **ESD-01** | ADR-005 Plugin Integrity Validation (APPROVED) | Kapitel 11 setzt die dort bestimmte Prüfung vor Ausführung als Bestand voraus. | Keine. Nicht geändert, nicht ausgelegt. |
| **ESD-02** | ADR-006 Plugin Permission Model (APPROVED) | Kapitel 11 setzt Default Deny, Dreizustandsauflösung und Admission-Time-Validierung als Bestand voraus. | Keine. |
| **ESD-03** | ADR-007 Plugin Dependency Resolution (APPROVED) | Kapitel 11 setzt die dort bestimmte Auflösungssemantik als Bestand voraus. | Keine. |
| **ESD-04** | ADR-011 SDK-Host-Integration (Accepted) | Kapitel 11 setzt die zweiphasige Lifecycle-Ordnung (Discovery → Security → Aktivierung) als Bestand voraus. | Keine. Statusabweichung siehe GC-06. |
| **ESD-05** | Architecture Book v2.0 §11 (Security), §13.4 (Audit) | Kapitel 11, 18 und 19 referenzieren bestehende Trust Boundaries, den Trust Ledger und die Audit-Infrastruktur. | Keine. FROZEN, unberührt. Spannungen siehe GC-03, GC-04, GC-07. |
| **ESD-06** | Architecture Book v2.0 §12 (Recovery) | Kapitel 17 beschreibt die sicherheitsarchitektonische Sicht auf bereits geführte Recovery-Konzepte. | Keine. FROZEN, unberührt. |
| **ESD-07** | Milestone 1.0 Implementation Plan, STR-01 bis STR-04 (APPROVED) | Kapitel 20 respektiert STR-03: Security Tests werden erst nach Definition dieser Security Architecture und der zugehörigen Security ADRs konkretisiert. STR-04 bestätigt die bestehenden Artefakte als alleinige Autorität bis dahin. | Keine. |
| **ESD-08** | `docs/security.md` | Kapitel 11 und 19 nehmen auf die dort beschriebenen Trust-Ledger-Zustände und Security Events Bezug. | Keine. Governance-Status ungeklärt, siehe GC-02. |
| **ESD-09** | Development Standard v1.1 | Verfahren, Reviewform und Genehmigungsweg dieses Dokuments richten sich ausschließlich nach diesem Standard. | Keine. |
| **ESD-10** | Bootstrap Baseline 1.0 (APPROVED) | Nicht inhaltlich in Anspruch genommen; als geschützter Bestand nach Governance Rule 1 erfasst. | Keine. |

---

## Schlussbestimmung

Dieses Dokument baut keine Sicherheit. Es bestimmt den Rahmen, innerhalb dessen
Sicherheit später gebaut werden darf.

Die Core Principles bleiben die Verfassung von JOCHEN X. Diese Security
Architecture ist deren sicherheitstechnische Konkretisierung. Sie darf niemals
zur zweiten Verfassung werden.

Wenn eine Aussage dieses Dokuments im Widerspruch zu den Core Principles steht,
ist dieses Dokument zu korrigieren — nicht die Core Principles.

---

## Revisionshistorie

| Revision | Datum | Auslöser | Änderungsumfang | Prüfartefakt |
|---|---|---|---|---|
| R0 | 2026-08-08 | Ersterstellung nach Autorisierung durch Core Principles 1.0 Governance Closing W-7 | Kapitel 0–24 und Schlussbestimmung erstellt | Creation Summary R0 (`docs/audits/security-architecture-1.0-creation-summary-r0.md`) |
| R0 (Status-Nachführung) | 2026-08-08 | Governance Closing W-4 nach Approval Decision W-2 (Option A) und Approval Record W-3 | Ausschließlich Governance-Metadaten: Status DRAFT → APPROVED. Kein fachlicher Inhalt geändert; Kapitel 0–24 unverändert. | Approval Record APR-SA-1.0-001 (`docs/governance/security-architecture-1.0-approval-record.md`); Governance Closing W-4 (`docs/governance/security-architecture-1.0-governance-closing-w4.md`) |

---

**Ende JOCHEN X – Security Architecture & Trust Framework 1.0 (APPROVED, R0)**
