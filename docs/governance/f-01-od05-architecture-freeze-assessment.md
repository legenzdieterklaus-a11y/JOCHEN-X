# JOCHEN X — Milestone 1.0
# F-1 — OD-05 Option B — Architecture Freeze Assessment

## 1. Assessment Identity

| Feld | Wert |
|---|---|
| Dokumenttyp | Governance / Architecture Assessment |
| **Assessment ID** | **F-1** |
| Titel | F-1 — OD-05 Option B — Architecture Freeze Assessment |
| Status | **FINAL ASSESSMENT** |
| Reference | **NAW-1** (FINAL ASSESSMENT, Kap. 13 F-1) · **GDR-OD05-001** (FINAL, Option B) |
| Scope | Ausschließlich F-1: Berührt OD-05 Option B den Architecture Freeze des Architecture Book v2.0? |
| Datum | 2026-08-10 |
| Branch / HEAD | `milestone-1.0-governance` / `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| Bezugs-Baseline | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| **Ergebnis** | **F-1-A — ARCHITECTURE FREEZE NOT TOUCHED** (Kap. 10) |
| Charakter | Governance-/Architekturprüfung. **Keine** Implementierung, **kein** ADR, **kein** RDR, **keine** AB-Änderung |

> **OD-05 Option B wird nicht neu entschieden.** Der verbindliche Wortlaut
> — „Policy-Konfiguration in die bestehende `PluginSecurityStage` ziehen (ohne
> Reihenfolgeänderung)" — bleibt unverändert. Option A und Option C werden nicht
> bewertet.

---

## 2. Source Gate

### 2.1 Pflichtquellen

| # | Quelle | Pfad | Status | Verifikation |
|---|---|---|---|---|
| 1 | Architecture Book v2.0 | `docs/architecture-book-v2.md` | **APPROVED / FROZEN (v2.0)**, 2026-07-26 | Kopf/Änderungsregel, **§6.5**, **§9**, §11.5, §20 (ADR-011), §21.1, **§22.1–§22.4** im Wortlaut gelesen |
| 2 | OD-05 Governance Decision | `docs/governance/od-05-governance-decision.md` | **FINAL** (GDR-OD05-001) | Kap. 4, 6 (C-1/C-2), 8, 11, 12.2, 17 (U-3) gelesen |
| 3 | NAW-1 Assessment | `docs/governance/naw-01-od05-adr-rdr-assessment.md` | **FINAL ASSESSMENT** | Kap. 6, 7.1, 7.3, **7.4 (L-1/L-2)**, 12 (B-1…B-7), 13 (F-1) gelesen |
| 4 | Bootstrap Baseline 1.0 | `docs/baselines/bootstrap-baseline-1.0.md` | **APPROVED** | **§4** (7 Invarianten), **§8** (Change Control), §2, §3 gelesen |
| 5 | Development Standard v1.1 | `docs/development-standard-v1.1.md` | **APPROVED** | **§13 ADR Rules** inkl. „Architecture Freeze und ADRs" im Wortlaut gelesen |
| 6 | Decision Briefs R0 | `docs/audits/jochen-x-decision-briefs-r0.md` | R0 | Brief 4 (OD-05): A.1, A.3, A.5.4, C-1/C-2, D, K gelesen |
| 7 | Master Engineering Plan R0 | `docs/audits/jochen-x-master-engineering-plan-r0.md` | R0 | §5.2, §5.4, §8.4, §10.6, §10.9, §20 OD-05 gelesen |
| 8 | Decision Execution Matrix R0 | `docs/audits/jochen-x-decision-execution-matrix-r0.md` | R0 | §D-3 gelesen |

**Pfadabweichungen:** **keine.** Alle acht im Auftrag genannten Pfade existieren
exakt wie angegeben (verifiziert per Existenzprüfung).

### 2.2 Fassungsentscheidung Architecture Book (wesentlich)

`docs/architecture-book-v2.md` ist im Working Tree **modifiziert** (Welt B) und
gehört zu den sechs uncommitteten Dokumentänderungen, deren Disposition per
**GDR-OD01-001 (Option C)** ausdrücklich **getrennt und noch nicht** erfolgt ist.

> **Für dieses Assessment ist ausschließlich die autoritative Fassung Welt A
> maßgeblich** (`git show 8fcf42f:docs/architecture-book-v2.md`, read-only
> entnommen). Die Welt-B-Fassung wurde **nicht** als Grundlage verwendet und
> **nicht** verändert. Die Divergenz zwischen beiden Fassungen betrifft
> ausschließlich die ADR-Statuszeilen in §20; **§6.5, §9 und §22 sind davon nicht
> betroffen** — die Freeze-Prüfung ist damit fassungsunabhängig belastbar.

### 2.3 Repository-Zustand vor Beginn

| Prüfung | Ergebnis |
|---|---|
| HEAD | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` — identisch mit MILESTONE-1.0-BASELINE |
| Branch | `milestone-1.0-governance` |
| Getrackte Änderungen | genau die sechs bekannten Excludes (`CLAUDE.md`, `ROADMAP.md`, ADR-005/006/007, AB v2.0) |
| Staging | **leer** |

> **SOURCE GATE: BESTANDEN.**

---

## 3. Question / Scope

**Geprüfte Frage — ausschließlich diese:**

> Ist OD-05 Option B innerhalb des bestehenden, FROZEN Architecture Book v2.0
> zulässig, oder verändert Option B eine **eingefrorene** Architekturentscheidung
> über Lebenszyklus, Erstellung, Registrierung oder Kompositionsort von
> `PluginSecurity`?

**Nicht geprüft und nicht beantwortet:** wie Option B implementiert werden sollte;
ob Option A oder C vorzuziehen wären; TD-04; der Abschluss von TD-19; QG-006;
sowie **F-2, F-3, F-4 und F-5** — diese bleiben unberührt und separat zu
autorisieren.

**Zu unterscheidende Lesarten** (Vorgabe des Auftrags):

- **L-1** — Option B konfiguriert lediglich die bereits vorhandene
  `PluginSecurity`-Instanz innerhalb der bestehenden `PluginSecurityStage`;
  Lebenszyklus, Erstellungs- und Registrierungsort bleiben unverändert.
- **L-2** — Option B etabliert einen neuen bzw. abweichenden
  Kompositions-/Lebenszykluspunkt, indem `PluginSecurity` in LOAD_PLUGINS
  policy-konfiguriert erzeugt/komponiert wird, und weicht damit von der
  eingefrorenen Aussage des AB v2.0 ab.

---

## 4. Authoritative Architecture Book Findings

### 4.1 §6.5 — Wortlaut (Welt A)

Kapitel **§6.5** trägt den Titel **„SecurityManager"** und die Datei-Zuordnung
**`app/security/security_manager.py`**. Es beschreibt den `SecurityManager` als
Koordinator, der **10 Sicherheitskomponenten** komponiert; `PluginSecurity` ist
darin **Position 8** der Aufzählung („Trust Ledger für Plugins").

Die maßgebliche Aussage lautet wörtlich:

> „**Lebenszyklus:** Erstellt und registriert in `SecurityBootstrapStage`
> (FINALIZE). Disposed in `ShutdownSequence`."

**Beantwortung der Prüffragen A:**

| Frage | Befund aus §6.5 |
|---|---|
| Wer erstellt `PluginSecurity`? | Der **`SecurityManager`** — als eine von 10 komponierten Services |
| Wo wird erstellt? | In **`SecurityBootstrapStage`** |
| Wo wird registriert? | Ebenda — „Erstellt **und registriert**" |
| In welcher Bootstrap-Phase? | **FINALIZE** |
| Ist diese Aussage ausdrücklich FROZEN? | **NEIN** — siehe §4.3. Die Aussage steht in einem FROZEN-**Dokument**, ihr Gegenstand (`app/security/security_manager.py`) ist jedoch **nicht** im enumerierten Freeze-Scope des AB §22.1 |

### 4.2 §9 Bootstrap Flow und weitere Lifecycle-Aussagen (Welt A)

| Fundstelle | Aussage | Relevanz für F-1 |
|---|---|---|
| §9 Bootstrap-Flow, Phase 4 | `SecurityBootstrapStage → SecurityManager (10 Services)` mit Fußnote: „**SecurityBootstrapStage ist NICHT in `default_stages()` enthalten.** Sie wird separat angehängt (z. B. über `create_desktop_bootstrap_manager()`)" | Das AB stellt selbst fest, dass diese Stage **außerhalb** der Standard-Komposition liegt |
| §9 Bootstrap-Flow, Phase 2 | LOAD_PLUGINS führt dort nur `PluginDiscoveryStage` auf | Beschreibt den Stand **vor** ADR-011-Implementierung — siehe §21.1 |
| **§20 (ADR-011), D3** | „**D3: `PluginSecurityStage` in LOAD_PLUGINS**" — Sub-Entscheidung einer im AB dokumentierten ADR | Das AB **sanktioniert** eine Plugin-Security-Stage in LOAD_PLUGINS ausdrücklich als Architekturentscheidung |
| §20 (ADR-011), Problem/Lösung | „`PluginDiscoveryStage` (LOAD_PLUGINS) und `SecurityBootstrapStage` (FINALIZE) haben eine **Timing-Lücke**. … **Lösung:** ADR-011 führt `PluginSecurityStage` ein, die in LOAD_PLUGINS nach Discovery läuft." | Das AB benennt die Timing-Lücke zwischen FINALIZE-Security und LOAD_PLUGINS **selbst** und löst sie über eine Stage in LOAD_PLUGINS |
| **§21.1 Zukunftsroadmap** | SDK-Host-Integration: „**Status: In Arbeit** (ADR-011 dokumentiert, **Implementation ausstehend**)" — gelistet u. a. „`PluginSecurityStage` in LOAD_PLUGINS Phase" | Das AB führt diesen Bereich ausdrücklich als **in Arbeit**, nicht als abgeschlossen eingefroren |
| §11.5 Plugin Security | Beschreibt `PluginSecurity` funktional (Trust Ledger, `RLock`, Events) — **ohne** Aussage zu Erstellungs-/Registrierungsort | keine zusätzliche Freeze-relevante Festlegung |

### 4.3 §22 Architecture Freeze — die operative Definition

Dies ist die für F-1 **entscheidende** Fundstelle.

**§22.1 „Eingefrorene Bestandteile"**, Chapeau: „Die folgenden Komponenten sind
unter Architecture Freeze (v1.0.0):" — gefolgt von einer **abschließenden
Aufzählung von zwölf Komponenten mit jeweils eigenem Freeze-Scope**:

| # | Komponente | Freeze-Scope |
|---|---|---|
| 1 | `core/events.py` | EventBus-API, Event-Dataclass |
| 2 | `core/registry.py` | ServiceRegistry-API, Lifetime-Enum |
| 3 | `core/lifecycle.py` | LifecycleManager-API, LifecycleState-Enum |
| 4 | `core/version.py` | Version-Dataclass, VersionManager-API |
| 5 | `core/extensions.py` | 5 Extension Protocols |
| 6 | `core/observability.py` | HealthCheck-Protocol, HealthStatus |
| 7 | `app/state_machine.py` | ApplicationState-Enum, Transition Table |
| 8 | **`app/bootstrap.py`** | **BootstrapStage-Protocol, StartupPhase-Enum** |
| 9 | `app/events.py` | ApplicationEventName-Enum, Event-Dataclasses |
| 10 | `sdk/__init__.py` | Öffentliche API-Surface (48 Symbole) |
| 11 | `sdk/manifest.py` | PluginMetadata-Felder, PluginPermission-Enum |
| 12 | `sdk/plugin.py` | Plugin-Basisklassen, PluginLifecycleState |

> **Zwei Feststellungen von entscheidender Tragweite:**
>
> 1. **`app/security/**` kommt in §22.1 überhaupt nicht vor.** Weder
>    `app/security/security_manager.py` (Gegenstand von §6.5) noch
>    `app/security/plugin_security.py` sind eingefrorene Bestandteile.
> 2. Für `app/bootstrap` ist der Freeze-Scope **ausdrücklich verengt** auf
>    **BootstrapStage-Protocol** und **StartupPhase-Enum** — nicht auf
>    Stage-Zusammensetzung, nicht auf Stage-Interna, nicht auf Lebenszyklusorte.

**§22.2 „Erlaubte Änderungen":**

| Änderungstyp | Erlaubt? | Bedingung |
|---|---|---|
| Bugfix in Implementierung | **Ja** | Keine API-Änderung |
| Neue optionale Felder | Ja | Default-Werte, Minor-Version-Bump |
| Neue Event-Typen | Ja | Minor-Version-Bump |
| Neue Bootstrap Stages | Ja | Bestehende Stages unverändert |
| Performance-Optimierung | Ja | Verhalten unverändert |
| **Interne Refactorings** | **Ja** | **API-Surface unverändert** |

**§22.3 „ADR-pflichtige Änderungen"** — sieben Positionen: Entfernung eines
eingefrorenen Symbols · Änderung der Transition Table · Neues
Plugin-Lifecycle-State · **Änderung der Bootstrap-Phasenreihenfolge** · Neue
Required Fields in `PluginMetadata` · Änderung der SDK-API-Version (Major) ·
Entfernung/Umbenennung eines Protocols.

*(Diese sieben sind inhaltsgleich mit Development Standard v1.1 §13 Nr. 1–7.)*

### 4.4 Nomenklatur-Hinweis zu §22.1 Zeile 8

§22.1 nennt `app/bootstrap.py` — den **Monolith-Pfad vor RDR-001**. Nach der
durch RDR-001 genehmigten und in Bootstrap Baseline 1.0 dokumentierten
Modularisierung liegen die beiden eingefrorenen Inhalte heute in
**`app/bootstrap/types.py`** (verifiziert am Baseline: `class StartupPhase(IntEnum)`,
`class BootstrapStage(Protocol)`). Der Freeze-Scope ist damit inhaltlich
eindeutig zuordenbar; die Pfadbezeichnung ist historisch. **Diese Feststellung
verschiebt den Freeze-Scope nicht** — sie lokalisiert ihn nur.

### 4.5 Änderungsregel des Dokumentkopfes

> „**Änderungsregel:** Keine inhaltlichen Änderungen an v2.0. Anpassungen erfolgen
> ausschließlich über neue Dokumentversionen (z. B. v2.1 oder v3.0) und
> dokumentierte ADRs."

Diese Regel adressiert **Änderungen am Dokument**. Sie wird durch dieses
Assessment eingehalten: das Architecture Book wurde **nicht verändert**.

**Development Standard v1.1 §13, „Architecture Freeze und ADRs":**

> „ADRs ändern nicht das Architecture Book v2.0 · ADRs dokumentieren
> Erweiterungen oder Ausnahmen · **Wenn eine ADR den Freeze-Scope betrifft**,
> wird eine neue Architecture Book Version (v2.1+) erforderlich."

Der Auslöser für eine AB-Version v2.1+ ist damit ausdrücklich an den
**Freeze-Scope** geknüpft — und dieser ist in AB §22.1 definiert.

---

## 5. OD-05 Option B — Authoritative Scope

Ausschließlich aus **GDR-OD05-001** belastbar abgeleitet — **nicht** aus einer
vermuteten Implementierung:

| # | Entschieden | Beleg |
|---|---|---|
| 1 | Ort: die **bestehende** `PluginSecurityStage` — keine neue Stage | GDR-OD05-001 Kap. 4, 8 |
| 2 | Gegenstand: **Policy-Konfiguration** | GDR-OD05-001 Kap. 4, 8 |
| 3 | **Keine** Änderung der Phasen-/Stage-Reihenfolge — konstitutiv | GDR-OD05-001 Kap. 8; R0 §20 OD-05 |

| # | **Nicht** entschieden / ausdrücklich offen | Beleg |
|---|---|---|
| 1 | Der Weg, auf dem die Policy-Konfiguration die Stage erreicht (Ausgestaltung von C-2) | GDR-OD05-001 Kap. 6 |
| 2 | Ob ein neues öffentliches Symbol entsteht | NAW-1 B-1 |
| 3 | Der **verbleibende Umfang von TD-19** („teilweise") | GDR-OD05-001 **U-3**, Kap. 12.2 |
| 4 | **TD-04** — die Übertragung des Host-Grant-Sets in den `PluginContext` ist durch OD-05 **nicht** entschieden und hängt zusätzlich an OD-01 | GDR-OD05-001 Kap. 6 (C-3), Kap. 12.1 |

**Für F-1 wesentlich:** Option B trifft **keine** Aussage über den Lebenszyklus
des `SecurityManager` und **keine** Aussage über `SecurityBootstrapStage`. Ihr
Gegenstand ist die **Policy-Konfiguration** an einem Ort, den das AB selbst über
ADR-011 D3 als Architekturbestandteil führt.

---

## 6. Baseline-Code Verification

**Ausschließlich lesend erhoben** (`git show 8fcf42f:<pfad>`). Keine Simulation,
kein Patch, keine Ausführung.

| # | Artefakt | Verifizierter Baseline-Zustand |
|---|---|---|
| V-1 | `app/bootstrap/stages_plugin.py`, `PluginSecurityStage.execute` (Z. 262–266) | `try: security = registry.get(PluginSecurity)` / `except LookupError:` → **`security = PluginSecurity(events, logger=logger)`** und **`registry.register(PluginSecurity, security)`** |
| V-2 | `app/security/security_manager.py` (Z. 116) | `plugins = PluginSecurity(events, logger=resolved_logger)` — Komposition im `SecurityManager` |
| V-3 | `app/security/security_manager.py` (Z. 203–204) | `registry._registrations.pop(PluginSecurity, None)` gefolgt von `registry.register(PluginSecurity, self._plugins)` — die FINALIZE-Stage **ersetzt** die zuvor registrierte Instanz |
| V-4 | `app/bootstrap/types.py` | `class StartupPhase(IntEnum)` (Z. 45), `class BootstrapStage(Protocol)` (Z. 122) — die beiden eingefrorenen Inhalte aus §22.1 Zeile 8 |
| V-5 | `app/bootstrap/manager.py`, `default_stages()` | 13 Stages, `PluginSecurityStage()` an Position 9 |
| V-6 | `ui/navigation/navigation_service.py`, `create_desktop_bootstrap_manager()` | Filtert eine **Kopie** von `default_stages()`; hängt `SecurityBootstrapStage()` und `NavigationBootstrapStage()` an; `default_stages()` selbst unangetastet |

> **V-1 ist der zentrale Befund:** Ein Erstellungs- **und** Registrierungspunkt
> für `PluginSecurity` in **LOAD_PLUGINS** existiert **bereits am autoritativen
> Baseline** — unabhängig von Option B und vor jeder Umsetzung.

---

## 7. L-1 Analysis

**L-1:** Option B konfiguriert lediglich die bereits vorhandene Instanz; der im AB
beschriebene Lebenszyklus bleibt unverändert.

| Prüfpunkt | Befund |
|---|---|
| Ist eine Konfiguration ohne Neukomposition technisch abbildbar? | **Ja** — `PluginSecurity.__init__` akzeptiert bereits heute die optionalen Keyword-Argumente `integrity_policy` und `permission_policy`. Die Policy-Konfiguration setzt daher **keine** neue Kompositionsstruktur voraus. *(Feststellung zum vorhandenen Code — keine Implementierungsempfehlung.)* |
| Bleibt §6.5 unter L-1 unberührt? | **Ja** — der `SecurityManager` komponiert und registriert seine Instanz weiterhin in `SecurityBootstrapStage` (FINALIZE) |
| Wird der Freeze-Scope §22.1 berührt? | **Nein** |

**L-1 ist mit dem AB uneingeschränkt vereinbar.**

---

## 8. L-2 Analysis

**L-2:** Option B etabliert einen neuen bzw. abweichenden
Kompositions-/Lebenszykluspunkt in LOAD_PLUGINS und weicht dadurch von der
eingefrorenen AB-Aussage ab.

Diese Lesart wurde in NAW-1 Kap. 7.4 als möglicher Freeze-Auslöser benannt. Der
Auftrag verlangt ausdrücklich ihre **Verifikation, nicht ihre Übernahme**. Die
Verifikation ergibt:

| # | Prüfpunkt | Befund |
|---|---|---|
| L2-1 | Wäre ein Kompositionspunkt in LOAD_PLUGINS **neu**? | **NEIN** — V-1 belegt: `PluginSecurityStage` erzeugt und registriert bereits am Baseline eine `PluginSecurity`-Instanz. Option B könnte diesen Punkt **konfigurieren**, aber nicht **neu schaffen** |
| L2-2 | Ist der Gegenstand von §6.5 im Freeze-Scope? | **NEIN** — `app/security/security_manager.py` ist in §22.1 **nicht aufgeführt**. §6.5 ist beschreibende Architekturdarstellung, keine eingefrorene Festlegung |
| L2-3 | Ist eine Plugin-Security-Stage in LOAD_PLUGINS architektonisch sanktioniert? | **JA** — AB §20 dokumentiert **ADR-011 D3: „`PluginSecurityStage` in LOAD_PLUGINS"** als getroffene Architekturentscheidung; §20 benennt die Timing-Lücke gegenüber der FINALIZE-Security ausdrücklich als das zu lösende Problem |
| L2-4 | Führt das AB diesen Bereich als abgeschlossen? | **NEIN** — §21.1 führt die SDK-Host-Integration inkl. „`PluginSecurityStage` in LOAD_PLUGINS Phase" als **„In Arbeit … Implementation ausstehend"** |
| L2-5 | Wird ein §22.3-Tatbestand ausgelöst? | **NEIN** — keiner der sieben; insbesondere bleibt die Bootstrap-Phasenreihenfolge durch Option B konstitutiv unverändert |
| L2-6 | Wird der Freeze-Scope von §22.1 Zeile 8 berührt (BootstrapStage-Protocol, StartupPhase-Enum)? | **NEIN** — Option B ändert weder das Protocol noch das Enum (V-4) |
| L2-7 | Wird `sdk/__init__.py` (48 Symbole), `sdk/manifest.py` oder `sdk/plugin.py` berührt? | **NEIN** — diese Artefakte gehören zu **TD-04**, das durch OD-05 ausdrücklich **nicht** entschieden ist |

**Ergebnis der L-2-Verifikation:** L-2 trägt in der Fassung, in der NAW-1 sie
benannt hat, **nicht**. Der in NAW-1 Kap. 7.4 formulierte Freeze-Vorbehalt war
allein auf §6.5 gestützt; er hielt **AB §22.1 nicht entgegen**. §22.1 definiert
den Freeze-Scope enumerativ und schließt `app/security/**` vollständig aus.
**Diese Korrektur ist für den weiteren Governance-Weg erheblich** (Kap. 11.3).

---

## 9. TD-19 Relevance

TD-19 wird hier **ausschließlich** insoweit betrachtet, wie es für F-1 erforderlich
ist. **TD-19 wird nicht geschlossen und nicht bewertet.**

| Aspekt | Feststellung |
|---|---|
| Sachverhalt | `SecurityBootstrapStage` (FINALIZE) ersetzt die in LOAD_PLUGINS registrierte Instanz (V-3); der konsumierte Trust Ledger ist nicht der prüfende. Im R0 als **DEVIATION** geführt [R0 §10.6, §10.9] |
| Verbleibender Umfang nach Option B | **UNKNOWN** — R0 sagt für Option (b) nur „TD-19 **teilweise**"; was ungelöst bliebe, ist **nicht ausgeführt** [GDR-OD05-001 U-3] |
| **Ist dieser UNKNOWN für F-1 entscheidend?** | **NEIN.** Selbst wenn die spätere Ausgestaltung `SecurityBootstrapStage` berühren müsste, liegt `app/security/security_manager.py` **außerhalb** des Freeze-Scopes §22.1. Der TD-19-Restumfang kann die Freeze-Frage daher **nicht kippen** |
| Wofür bleibt U-3 entscheidend? | Für **F-4** (Bestimmung des TD-19-Restumfangs) und mittelbar für **F-2/F-3** unter dem **anderen** Governance-Instrument Bootstrap Baseline §8 — **nicht** für F-1 |
| Verhältnis §6.5 ↔ TD-19 | Die Divergenz zwischen §6.5 und dem Ist-Zustand **besteht bereits am Baseline** (V-1 gegen §6.5) und ist als TD-19 dokumentiert. Sie wird durch Option B **nicht erzeugt** |

> **TD-19 bleibt OPEN.** U-3 bleibt **UNKNOWN**, ist für F-1 jedoch **nicht
> entscheidungserheblich** — die Begründung dafür ist L2-2 (Gegenstand außerhalb
> des Freeze-Scopes).

---

## 10. Architecture Freeze Determination

> # **F-1-A — ARCHITECTURE FREEZE NOT TOUCHED**

**Begründung mit Fundstellen:**

| # | Begründungsschritt | Fundstelle |
|---|---|---|
| 1 | Der Architecture Freeze ist im AB **selbst enumerativ definiert**: „Die folgenden Komponenten sind unter Architecture Freeze (v1.0.0)" — zwölf Komponenten mit je eigenem Freeze-Scope | **AB §22.1** |
| 2 | **`app/security/security_manager.py`** — der Gegenstand von §6.5 — ist in dieser Aufzählung **nicht enthalten**. Ebenso wenig `app/security/plugin_security.py` | **AB §22.1** (Negativbefund, vollständige Liste geprüft) |
| 3 | Für `app/bootstrap` ist der Freeze-Scope ausdrücklich auf **BootstrapStage-Protocol** und **StartupPhase-Enum** verengt. Option B ändert weder das eine noch das andere | **AB §22.1 Zeile 8**; Verifikation V-4 |
| 4 | Keiner der **sieben** ADR-pflichtigen Änderungstypen wird ausgelöst; insbesondere bleibt die **Bootstrap-Phasenreihenfolge** durch den konstitutiven Wortlaut von Option B unverändert | **AB §22.3**; Development Standard **§13 Nr. 1–7**; GDR-OD05-001 Kap. 8 |
| 5 | Das AB **sanktioniert** eine Plugin-Security-Stage in LOAD_PLUGINS ausdrücklich als Architekturentscheidung (ADR-011 **D3**) und benennt die Timing-Lücke zur FINALIZE-Security als das zu lösende Problem | **AB §20 (ADR-011)** |
| 6 | Das AB führt diesen Bereich selbst als **„In Arbeit … Implementation ausstehend"**, nicht als abgeschlossen | **AB §21.1** |
| 7 | Ein Erstellungs- und Registrierungspunkt in LOAD_PLUGINS besteht **bereits am autoritativen Baseline**; Option B könnte ihn konfigurieren, aber nicht neu schaffen | Verifikation **V-1** (`8fcf42f:app/bootstrap/stages_plugin.py` Z. 262–266) |
| 8 | §22.2 erlaubt ausdrücklich „**Interne Refactorings** — API-Surface unverändert" und „**Bugfix in Implementierung** — keine API-Änderung" | **AB §22.2** |
| 9 | Die AB-Änderungsregel und Development Standard §13 knüpfen eine neue AB-Version **v2.1+** an eine ADR, die den **Freeze-Scope** betrifft. Da weder eine §22.3-ADR-Pflicht ausgelöst noch der Freeze-Scope berührt ist, entsteht **keine** v2.1-Pflicht | AB Kopf-Änderungsregel; **Development Standard §13** „Architecture Freeze und ADRs" |

**Eingeordnete Lesart:** **L-1 trifft zu** bzw. — soweit die spätere Ausgestaltung
Elemente von L-2 aufwiese — bleibt auch L-2 **außerhalb** des in §22.1 definierten
Freeze-Scopes (L2-1 bis L2-7). Die Freeze-Frage ist damit **unabhängig von der
noch offenen Ausgestaltung** determinierbar. Das ist der Grund, weshalb F-1 —
anders als NAW-1 insgesamt — **nicht** in F-1-D endet.

**Es liegt keine Mischkategorie vor.**

---

## 11. Consequences

### 11.1 Was aus F-1-A folgt

| # | Folge |
|---|---|
| 1 | Für **OD-05 Option B** ist aus dem Architecture Freeze **kein ADR** erforderlich |
| 2 | Eine **Architecture-Book-Version v2.1+** wird durch Option B **nicht** ausgelöst |
| 3 | **NAW-1 B-5** ist damit **beantwortet**; Development Standard **§13 Nr. 8** ist **nicht erfüllt**. Zusammen mit den in NAW-1 Kap. 7.3 festgestellten Nr. 1–7 sind damit **alle acht** ADR-Auslöser des Development Standard **nicht erfüllt** |
| 4 | Die eingefrorene Aussage über **BootstrapStage-Protocol** und **StartupPhase-Enum** bleibt unverändert und ist weiterhin zu wahren |

### 11.2 Fortbestehende Grenzen

F-1-A gilt für **Option B in ihrem entschiedenen Wortlaut**. Die Feststellung
würde neu zu prüfen sein, falls eine spätere Ausgestaltung entgegen dem
Entscheidungswortlaut:

- die **Bootstrap-Phasenreihenfolge** änderte (§22.3), oder
- das **BootstrapStage-Protocol** oder das **StartupPhase-Enum** änderte (§22.1), oder
- die **SDK-Freeze-Artefakte** `sdk/__init__.py` (48 Symbole), `sdk/manifest.py`
  oder `sdk/plugin.py` berührte — was **TD-04**-Gebiet wäre und durch OD-05
  **nicht** entschieden ist, oder
- ein Protocol entfernte/umbenennte oder ein eingefrorenes Symbol entfernte (§22.3).

**F-1-A ist kein Freibrief für die Umsetzung.** Es beantwortet ausschließlich die
Freeze-Frage.

### 11.3 Was F-1-A ausdrücklich NICHT beantwortet

| # | Weiterhin offen | Instrument |
|---|---|---|
| 1 | **NAW-1 B-2** — Reichweite von Bootstrap Baseline **§8-4** („BootstrapManager … Verhalten") | **Bootstrap Baseline §8** — anderes Governance-Instrument als der Architecture Freeze |
| 2 | **NAW-1 B-1 / B-3** — neues öffentliches Symbol in `app/bootstrap/__init__.py` `__all__`; `default_stages()`-Zusammensetzung | **Bootstrap Baseline §8-3 / §8-5** |
| 3 | **NAW-1 B-4** / GDR-OD05-001 **U-3** — TD-19-Restumfang | F-4 |
| 4 | **NAW-1 B-6** — Abgrenzungskriterium ADR ↔ RDR bei bejahter §8-Pflicht | F-2/F-5 |
| 5 | **NAW-1 B-7** — Inkongruenz AB §9-Flussdiagramm ↔ `default_stages()` (13 Stages) | Dokumentationsfrage; an die getrennte AB-Disposition aus **GDR-OD01-001** gebunden |

> **Wesentlich:** Bootstrap Baseline §8 schützt ausdrücklich die
> `__all__`-Einträge des Bootstrap-Pakets; AB §22.1 tut dies **nicht**. Die beiden
> Instrumente haben unterschiedliche Schutzbereiche. **F-1-A präjudiziert das
> NAW-1-Gesamtergebnis (D) daher nicht** — dieses bleibt bis zum Abschluss von
> F-2/F-3 und der Wiederholungsprüfung F-5 bestehen.

### 11.4 Beobachtung zur Dokumentgenauigkeit (keine F-1-Folge)

AB §6.5 beschreibt den Ist-Zustand bereits am Baseline unvollständig (V-1 gegen
§6.5) — dokumentiert als **TD-19 (DEVIATION)**. Ob und wann der AB-Text
nachgeführt wird, ist eine **Dokumentationsfrage**, keine Freeze-Frage, und ist an
die per **GDR-OD01-001 (Option C)** getrennt zu führende Disposition des
Architecture Book gebunden. **Nicht Gegenstand von F-1; hier weder entschieden
noch veranlasst.**

---

## 12. Remaining UNKNOWNs

| ID | Offener Punkt | Entscheidungserheblich für F-1? | Zuordnung |
|---|---|---|---|
| **U-3** (GDR-OD05-001) | Verbleibender Umfang von TD-19 nach Option B | **NEIN** — Begründung L2-2: Gegenstand außerhalb §22.1 | F-4 |
| **B-1** (NAW-1) | Neues öffentliches Symbol in `app/bootstrap/__init__.py`? | **NEIN** für den Freeze (§22.1 schützt diese Liste nicht) — **JA** für Bootstrap Baseline §8-3 | F-2/F-3 |
| **B-2** (NAW-1) | Reichweite von Baseline §8-4 | **NEIN** — anderes Instrument | **F-2** |
| **B-3** (NAW-1) | `default_stages()`-Zusammensetzung | **NEIN** für den Freeze — **JA** für §8-5 | F-3 |
| **B-4** (NAW-1) | Berührung von `SecurityBootstrapStage` / Desktop-Komposition | **NEIN** — beide außerhalb §22.1 | F-4 |
| **B-6** (NAW-1) | Kriterium ADR ↔ RDR | **NEIN** | F-2/F-5 |
| **B-7** (NAW-1) | AB §9 „11 Default-Stages" ↔ 13 Stages in `default_stages()`; `PluginSecurityStage` in §9-Phase-2 nicht aufgeführt | **NEIN** — betrifft die Darstellungsgenauigkeit des AB, nicht den Freeze-Scope (§22.1). Vermerkt, **nicht aufgelöst** | AB-Disposition (GDR-OD01-001) |

> **Keiner der verbleibenden UNKNOWNs ist für die Freeze-Determination
> entscheidungserheblich.** Genau deshalb ist F-1 determinierbar, während NAW-1
> insgesamt bei Ergebnis D bleibt.

---

## 13. Governance Recommendation

> **Keine der folgenden Positionen wird durch dieses Assessment ausgeführt oder
> ausgelöst.** Jede bedarf einer eigenen, ausdrücklichen Autorisierung.

| # | Empfehlung | Begründung | Status |
|---|---|---|---|
| **G-1** | **F-1 als abgeschlossen führen**; NAW-1 **B-5** als beantwortet vermerken | Freeze-Frage ist quellengebunden determiniert | **vorgeschlagen** |
| **G-2** | **Als Nächstes F-2** — autoritative Auslegung von Bootstrap Baseline **§8-4** („BootstrapManager … Verhalten") | F-2 ist die einzige verbliebene **Regelungslücke**, die eine ADR-/RDR-Pflicht **unabhängig von der Ausgestaltung** auslösen kann. Sie ist damit vorrangig vor F-3 | **OPEN — nicht gestartet** |
| **G-3** | **Danach F-3** — Fixierung des Änderungsumrisses (B-1, B-3) | F-3 ist nur dann noch ergebnisrelevant, wenn F-2 die Stage-Interna **nicht** bereits erfasst | **OPEN — nicht gestartet** |
| **G-4** | **F-4** — Bestimmung des TD-19-Restumfangs | unabhängig von F-1; weiterhin erforderlich | **OPEN** |
| **G-5** | **F-5** — Wiederholung der §8-Prüfung nach F-2/F-3/F-4 | erst danach ist NAW-1 von Ergebnis D auf A, B oder C fortzuschreiben | **OPEN** |

**Reihenfolgeempfehlung: F-2 vor F-3.** Begründung: F-2 klärt eine
**Regelungslücke der Baseline** und wirkt damit unabhängig von der Ausgestaltung;
F-3 klärt die **Ausgestaltung** und ist in seiner Ergebnisrelevanz von F-2
abhängig. Diese Empfehlung ist **keine Autorisierung**.

**Kein ADR und kein RDR sind aus F-1 abzuleiten.** Ob unter Bootstrap Baseline §8
eine Governance-Aktion erforderlich wird, bleibt durch NAW-1 (Ergebnis D) offen.

---

## 14. Final Assessment Statement

> **F-1 — FINAL ASSESSMENT**
>
> **Ergebnis: F-1-A — ARCHITECTURE FREEZE NOT TOUCHED.**
>
> **OD-05 Option B ist innerhalb des bestehenden, FROZEN Architecture Book v2.0
> zulässig.** Option B verändert **keine eingefrorene Architekturentscheidung**
> über Lebenszyklus, Erstellung, Registrierung oder Kompositionsort von
> `PluginSecurity`.
>
> **Tragender Grund:** Der Architecture Freeze ist in **AB §22.1** enumerativ
> definiert. `app/security/security_manager.py` — der Gegenstand der
> Lebenszyklus-Aussage in §6.5 — ist dort **nicht enthalten**; für `app/bootstrap`
> ist der Freeze-Scope ausdrücklich auf **BootstrapStage-Protocol** und
> **StartupPhase-Enum** verengt, die Option B beide nicht berührt. **Keiner** der
> sieben ADR-pflichtigen Änderungstypen aus **§22.3** wird ausgelöst. Ergänzend
> sanktioniert das AB über **ADR-011 D3** eine Plugin-Security-Stage in
> LOAD_PLUGINS ausdrücklich und führt den Bereich in **§21.1** selbst als „In
> Arbeit". Ein Erstellungs- und Registrierungspunkt in LOAD_PLUGINS besteht
> zudem **bereits am autoritativen Baseline** (V-1) und wird durch Option B nicht
> neu geschaffen.
>
> **Der in NAW-1 Kap. 7.4 gestützt auf §6.5 formulierte Freeze-Vorbehalt (L-2)
> hält AB §22.1 nicht stand.** NAW-1 **B-5** ist damit beantwortet; Development
> Standard **§13 Nr. 8** ist nicht erfüllt.
>
> **Folge:** Aus dem Architecture Freeze entsteht **kein ADR** und **keine
> Architecture-Book-Version v2.1+**.
>
> **Nicht beantwortet und ausdrücklich offen:** die Reichweite von Bootstrap
> Baseline **§8-4** (NAW-1 B-2), der Änderungsumriss (B-1, B-3), der
> TD-19-Restumfang (U-3 / B-4) und das ADR-↔-RDR-Kriterium (B-6). **Das
> NAW-1-Gesamtergebnis bleibt D** — Bootstrap Baseline §8 und Architecture Freeze
> sind **verschiedene Instrumente mit verschiedenen Schutzbereichen**.
>
> **F-1-A ist keine Umsetzungsfreigabe.** F-2, F-3, F-4 und F-5 bleiben offen und
> separat zu autorisieren.
>
> **TD-04 / TD-05 / TD-19 / TD-21 / TD-06: OPEN. ODD-17: OPEN. OD-04: OPEN.
> QG-006: NOT STARTED. RB-1.0: unverändert (258/14). Sprint Plan: unverändert.
> Architecture Book v2.0: unverändert und weiterhin FROZEN.**
>
> **CODING = NOT AUTHORIZED.**

---

## 15. Change-Control / Repository State

| Prüfung | Ergebnis |
|---|---|
| HEAD vor und nach dem Assessment | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` — **unverändert** |
| Getrackte Änderungen | genau die sechs bekannten Excludes — **unverändert** |
| Staging | **leer** — kein `git add` |
| Neue Dateien | **genau eine**: `docs/governance/f-01-od05-architecture-freeze-assessment.md` |
| Bestandsdateien verändert | **keine** |
| `src/**`, `app/**`, `sdk/**`, `tests/**`, `config/**` | **unverändert** — ausschließlich lesend über `git show 8fcf42f:<pfad>` verifiziert |
| **Architecture Book v2.0** | **nicht verändert**; weiterhin **APPROVED / FROZEN** |
| Architecture Book v2.1 | **nicht erstellt** |
| Bootstrap Baseline, Development Standard, Implementation Plan, Sprint Plan, ADRs, RDRs, `CLAUDE.md`, `ROADMAP.md` | **unverändert** |
| GDR-OD01-001, GDR-OD05-001, NAW-1 | **unverändert** |
| **OD-05 Option B** | **unverändert** — nicht neu entschieden |
| ADR erstellt | **NEIN** |
| RDR erstellt | **NEIN** |
| Implementierung | **KEINE** |
| Tests | **nicht verändert, nicht ausgeführt** |
| Quality Gates geschlossen | **KEINE** — QG-006 bleibt NOT STARTED |
| Findings / ODDs geschlossen | **KEINE** |
| Implementierungsautorisierung erteilt | **KEINE** |
| Commit / Tag / Push | **KEINE** |

---

**Ende F-1 Architecture Freeze Assessment — JOCHEN X Milestone 1.0
(FINAL ASSESSMENT, 2026-08-10, Reference NAW-1 / GDR-OD05-001) —
Bezugs-Baseline `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
