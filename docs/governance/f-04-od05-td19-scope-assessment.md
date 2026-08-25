# JOCHEN X — Milestone 1.0
# F-4 — TD-19 Remaining-Scope Assessment (OD-05 Option B)

| Feld | Wert |
|---|---|
| Dokumenttyp | Governance / Technical-Debt Scope Assessment (READ-ONLY) |
| **ID** | **F-4** |
| Status | **FINAL ASSESSMENT** |
| Gegenstand | Verbleibender **TD-19**-Umfang nach der in **NAW-A** fixierten Change-Surface für **OD-05 Option B** |
| Governance Input | **NAW-A** (COMPLETED) · **NAW-B** (COMPLETED) · **G-1 = OPTION HYBRID — PRECISISED** · **GDR-OD05-001** (Option B) · **F-3** · **F-2-B** · **F-1-A** |
| Datum | 2026-08-10 |
| Branch / HEAD | `milestone-1.0-governance` / `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| **Ergebnis** | **TD-19 = PARTIALLY IMPACTED** (Kap. 12.5) · **Change Surface: CS-1 + CS-2 + CS-3 — keine Erweiterung erforderlich** |
| Coding | **NOT AUTHORIZED** |

---

## 1. Executive Summary

**Frage A ist mit JA zu beantworten.** OD-05 Option B kann hinsichtlich seines
entschiedenen Gegenstands — der Policy-Konfiguration der Admission — **vollständig
umgesetzt werden, ohne `app/security/security_manager.py` zu verändern.**

**Der tragende technische Befund:** Am Baseline registriert **niemand** eine
`PluginSecurity`-Instanz vor der LOAD_PLUGINS-Phase. Die beiden einzigen
Registrierungsstellen sind `stages_plugin.py:266` (LOAD_PLUGINS,
`except LookupError`) und `security_manager.py:204` (FINALIZE)
[SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:266; BASELINE 8fcf42f:app/security/security_manager.py:204].
Der `LookupError`-Zweig **greift daher stets** — die über **CS-1** konfigurierte
Instanz ist genau diejenige, gegen die die Admission geprüft wird.

**TD-19 bleibt davon unberührt und OPEN.** Weder die Ersetzung der Instanz in
FINALIZE noch die Trust-Ledger-Diskontinuität werden durch den fixierten Umriss
adressiert.

**Ein Befund, der über die bisherige Dokumentation hinausgeht.** Am Baseline sind
**beide** `PluginSecurity`-Instanzen mit **identischen Default-Policies**
konstruiert — `PluginSecurity(events, logger=…)` an beiden Stellen. Die
TD-19-Divergenz betrifft daher heute nur **Instanzidentität und Ledger-Inhalt**,
nicht die Policy. Nach Umsetzung von Option B über CS-1 trüge die
LOAD_PLUGINS-Instanz **konfigurierte** Policies, die FINALIZE-Instanz weiterhin
**fest verdrahtete Defaults**. Die bestehende Divergenz gewänne damit eine
**zusätzliche Dimension: Policy-Diskontinuität**.

**Diese Dimension ist nicht umsetzungsblockierend:** Es existiert **kein
produktiver Konsument**, der die in FINALIZE registrierte `PluginSecurity`-Instanz
liest (Kap. 9.4, 10.3). Sie ist jedoch für **F-5** und für die spätere Behandlung
von TD-19 festzuhalten.

> **Ergebnis: FALL B — TD-19 = PARTIALLY IMPACTED.**
> **CHANGE-SURFACE EXPANSION: NICHT ERFORDERLICH.**

---

## 2. Source Gate

| # | Pflichtquelle | Pfad | Status | Verifikation |
|---|---|---|---|---|
| 1 | F-3 | `docs/governance/f-03-od05-change-surface-assessment.md` | FINAL ASSESSMENT | Kap. 6, 11, 12, 21 |
| 2 | NAW-A | `docs/governance/naw-a-od05-change-surface-fixation.md` | FINAL / COMPLETED | Kap. 3, 6, 7, 8, 16 |
| 3 | NAW-B | `docs/governance/naw-b-g1-observable-state-contract-fixation.md` | FINAL / COMPLETED | Kap. 4, 9, 13, 17 |
| 4 | OD-05 Decision | `docs/governance/od-05-governance-decision.md` | FINAL (GDR-OD05-001) | Kap. 8, 12.2, 17 (U-3) |
| 5 | G-1 Decision Brief | `docs/audits/g-01-bootstrap-behavior-interpretation-decision-brief-r0.md` | DRAFT · NON-NORMATIVE | Kap. 8, 20 |
| 6 | Master Engineering Plan | `docs/audits/jochen-x-master-engineering-plan-r0.md` | R0 | **§10.6 (SEC-07)**, §10.9, §18.4 Cluster 2, §19.5, §24.2, §24.3, §26, §28 |
| 7 | Decision & Execution Matrix | `docs/audits/jochen-x-decision-execution-matrix-r0.md` | R0 | §D-3, TD-19-Zeile |
| 8 | Bootstrap Baseline 1.0 | `docs/baselines/bootstrap-baseline-1.0.md` | APPROVED | §2, §4, §5.1, §8 |
| 9 | RDR-001 | `docs/rdr/001-bootstrap-modularization.md` | APPROVED | §3 Inv. 5 |
| 10 | Architecture Book v2.0 | `docs/architecture-book-v2.md` | APPROVED / FROZEN | **Welt A** (Kap. 3.2); §6.5, §9, §22.1 |
| 11 | Development Standard v1.1 | `docs/development-standard-v1.1.md` | APPROVED | §13 |
| 12 | Implementation Plan 1.0 | `docs/milestone-1.0-implementation-plan.md` | APPROVED R1.2 | GC-06, BI-03 |
| 13 | Security Design 1.0 | `docs/security-design-1.0.md` | APPROVED | geprüft — keine Aussage zur Stage-Komposition |
| 14 | Security Architecture 1.0 | `docs/security-architecture-1.0.md` | APPROVED | dito |

**Pfadabweichungen:** keine.

**Read-only untersuchter Baseline-Code:** `app/security/security_manager.py`,
`app/security/plugin_security.py`, `app/security/__init__.py`,
`app/bootstrap/stages_plugin.py`, `app/bootstrap/manager.py`,
`app/bootstrap/types.py`, `app/bootstrap/stages_init.py`,
`app/bootstrap/stages_late.py`, `ui/navigation/navigation_service.py`,
`ui/navigation/main_window.py`, `config/settings.py`, `config/default.toml`.

> **SOURCE GATE: BESTANDEN.**

---

## 3. Baseline Reference

| Prüfung | Ergebnis |
|---|---|
| Baseline-Identifier | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` [SOURCE: docs/governance/milestone-1.0-baseline-commit-record.md §6] |
| HEAD zu Beginn | identisch mit der Baseline |
| Reproduzierbarkeit | **PASS** — sämtlicher Code über `git show 8fcf42f:<pfad>` |

### 3.1 Ebenentrennung

| Ebene | Verwendung |
|---|---|
| **BASELINE** (`8fcf42f`) | **Alleinige Grundlage** aller Code-Aussagen |
| **WORKING TREE** | Nur Divergenzfeststellung: die sechs getrackten Modifikationen betreffen `CLAUDE.md`, `ROADMAP.md`, ADR-005/006/007, Architecture Book — **kein** Security-, Bootstrap- oder Config-Artefakt |
| **UNTRACKED DOCS** | Governance-/Audit-Dokumente; **keine Baseline** |

### 3.2 Fassungsregel Architecture Book

Maßgeblich ist **Welt A**; die Working-Tree-Fassung ist per GDR-OD01-001 (Option C)
getrennt und nicht disponiert
[SOURCE: docs/governance/f-01-od05-architecture-freeze-assessment.md Kap. 2.2].

---

## 4. TD-19 Source Definition

**TD-19 wird aus den Quellen rekonstruiert, nicht neu definiert.**

| Quelle | Formulierung |
|---|---|
| **R0 §10.6 / §19-Tabelle** | „`SecurityBootstrapStage` (FINALIZE) ersetzt die `PluginSecurity`-Instanz **nach** Admission und Aktivierung … Der aus der Registry bezogene Trust Ledger ist **nicht derjenige, gegen den geprüft wurde**; `IntegrityResult`/`PermissionResult` fehlen dort" [SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §10.6, TD-19-Zeile] |
| **R0 — Klassifikation** | **SEC-07 INFERENCE:** „Die vom `SecurityManager` komponierte Instanz kann die **Admission nie beeinflussen**." Priorität **HIGH (technisch)**; in §10.9 als **DEVIATION** geführt [SOURCE: ebd. §10.6, §10.9] |
| **R0 §18.4 Cluster 2** | Gemeinsame Ursache des C2-Clusters: „Der `SecurityManager` wurde als *additive* FINALIZE-Stage **nachgerüstet**, während die Plugin-Pipeline in LOAD_PLUGINS bereits eigene Defaults erzeugt" [SOURCE: ebd. §18.4] |
| **DEM §D-3** | „(i) `SecurityBootstrapStage` läuft in FINALIZE und ersetzt die `PluginSecurity`-Instanz **nach** Admission und Aktivierung (TD-19)"; Behebungsrichtung: „Reihenfolge/Komposition klären — **Bootstrap-Baseline-Change-Control**" [SOURCE: docs/audits/jochen-x-decision-execution-matrix-r0.md §D-3, TD-19-Zeile] |
| **Security Gate** | **SG-E** — „Trust-Ledger-Identität über die Phasen": **nicht gegeben**; erforderlicher Nachweis **TG-3** existiert nicht; **BLOCKING für QG-006** [SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §26, §15.4] |
| **OD-05-Wirkung** | Option (b) löst „**TD-05 vollständig und TD-19 teilweise**"; der verbleibende Umfang ist im R0 **nicht ausgeführt** → **U-3 UNKNOWN** [SOURCE: docs/governance/od-05-governance-decision.md Kap. 12.2, U-3] |

### 4.1 Bestandteile von TD-19 nach den Quellen

| # | Bestandteil | Beleg |
|---|---|---|
| **T-a** | **Instanz-Ersetzung**: Die in LOAD_PLUGINS registrierte `PluginSecurity` wird in FINALIZE durch eine andere ersetzt | R0 §10.6 |
| **T-b** | **Trust-Ledger-Diskontinuität**: Die konsumierte Instanz enthält die `IntegrityResult`-/`PermissionResult`-Einträge der Prüfung **nicht** | R0 §10.6 |
| **T-c** | **Wirkungslosigkeit der SecurityManager-Instanz für die Admission**: Sie kann die Admission „nie beeinflussen" | R0 §10.6 SEC-07 |

### 4.2 Divergenzprüfung zwischen den Quellen

| Prüfung | Ergebnis |
|---|---|
| Formulierungsunterschiede R0 ↔ DEM | **keine inhaltliche Divergenz** — DEM übernimmt die R0-Formulierung und ergänzt den Change-Control-Bezug |
| Klassifikationsunterschiede | R0 führt TD-19 in §10.9 als **DEVIATION**, die Herleitung SEC-07 als **INFERENCE** (nicht SOURCE FACT). Dies ist eine **Abstufung innerhalb derselben Quelle**, keine Divergenz zwischen Quellen |
| Umfangsangabe „teilweise" | In **keiner** Quelle ausgeführt → **U-3 bleibt UNKNOWN** |

> **TD-19 wird nicht umbenannt, nicht neu formuliert, nicht mit anderen
> TD-Positionen verschmolzen und nicht geschlossen.**

---

## 5. Baseline Security Lifecycle

**Ablauf am Baseline, mit Klassifikation je Element:**

```
INITIALIZE
  ConfigurationStage        → context.configuration, context.settings      [EXISTING]
  RegistryStage             → ServiceRegistry, EventBus                    [EXISTING]
  … (Environment, Logging, Database, Theme, Scheduler)
        ↓
LOAD_PLUGINS                                                    [BASELINE-PROTECTED §8-2]
  PluginDiscoveryStage      → context.plugins (PluginLoader)               [EXISTING]
                            → registry.register(PluginCatalog, <alle IDs>) [EXISTING]
  PluginSecurityStage       → registry.get(PluginSecurity)                 [EXISTING]
                              └─ LookupError ⇒ PluginSecurity(events,
                                 logger=logger)  ← OHNE Policy-Argumente   [OD-05 / CS-1]
                                 registry.register(PluginSecurity, …)
                            → Schritt 1 Integrity                          [BASELINE-PROTECTED §4 Inv. 6]
                            → Schritt 2 API-Version-Gate
                            → Schritt 3 Permission (PermissionPolicy)      [OD-05]
                            → Schritt 4 Dependency Resolution
                            → context.admitted_manifests = resolved        [NAW-B: Kontraktbestandteil]
                            → registry.register(PluginCatalog, <gefiltert>)[NAW-B: Kontraktbestandteil]
        ↓
LOAD_RESOURCES
  ResourceStage                                                            [NOT RELATED]
        ↓
FINALIZE
  PluginActivationStage     → liest context.admitted_manifests             [EXISTING]
                            → Import/Instantiierung/Start                  [EXISTING]
  DeveloperToolsStage                                                      [NOT RELATED]
  SecurityBootstrapStage    → SecurityManager.create(events, logger=…)     [TD-19]
                              └─ plugins = PluginSecurity(events,
                                 logger=…)   ← OHNE Policy-Argumente       [TD-19]
                            → manager.register(registry):
                                 registry._registrations.pop(PluginSecurity)  [TD-19 / TD-06]
                                 registry.register(PluginSecurity, self._plugins)  [TD-19]
                            → manager.initialize()                         [EXISTING]
  NavigationBootstrapStage                                                 [NOT RELATED]
  DependencyInjectionStage                                                 [NOT RELATED]
        ↓
READY
```

[SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py:`default_stages`;
BASELINE 8fcf42f:ui/navigation/navigation_service.py:`create_desktop_bootstrap_manager`;
BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:`PluginSecurityStage.execute`;
BASELINE 8fcf42f:app/security/security_manager.py:`SecurityBootstrapStage.execute`, `SecurityManager.create`, `SecurityManager.register`]

**Hinweis zur Komposition:** `SecurityBootstrapStage` ist **nicht** Teil von
`default_stages()`; sie wird über `create_desktop_bootstrap_manager()` angehängt
[SOURCE: BASELINE 8fcf42f:ui/navigation/navigation_service.py:137–152; BASELINE 8fcf42f:docs/architecture-book-v2.md §9 Fußnote].

---

## 6. `PluginSecurityStage`

| Aspekt | Befund | Klasse |
|---|---|---|
| Verantwortlichkeit | Vier Admission-Schritte: Integrity → API-Version-Gate → Permission → Dependency Resolution | **EXISTING** |
| Phase | `StartupPhase.LOAD_PLUGINS`; Position 9 in `default_stages()` | **BASELINE-PROTECTED** (§8-2, §8-5) |
| Erzeugung von `PluginSecurity` | Nur im Zweig `except LookupError`: `PluginSecurity(events, logger=logger)` — **ohne Policy-Argumente** | **OD-05 / CS-1** |
| Registrierung | `registry.register(PluginSecurity, security)` | **EXISTING** |
| Beobachtbare Wirkung | Setzt `context.admitted_manifests`; ersetzt den registrierten `PluginCatalog` | **NAW-B: Kontraktbestandteil** |
| Konsum durch spätere Stufen | `PluginActivationStage` liest `context.admitted_manifests` | **EXISTING** |

[SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:234–345, insb. 262–266, 335–339]

---

## 7. `PluginSecurity`

| Aspekt | Befund | Klasse |
|---|---|---|
| Verantwortlichkeit | „Thread-safe plugin trust ledger and validator" | **EXISTING** |
| Konstruktor | `__init__(events, *, logger=None, integrity_policy=None, permission_policy=None)` — **beide Policy-Argumente existieren bereits** | **EXISTING** |
| Defaults | `integrity_policy or IntegrityPolicy()`; `permission_policy or PermissionPolicy()` (default-deny) | **EXISTING** |
| Interner Zustand | `_trust`, `_integrity_results`, `_permission_results`, `_lock` (`RLock`) | **EXISTING** |
| Lebenszyklus | Wird zweimal unabhängig instanziiert (Kap. 5) | **TD-19** |

[SOURCE: BASELINE 8fcf42f:app/security/plugin_security.py:`PluginSecurity.__init__`]

> **Wesentlich für F-4:** Die Policy-Aufnahmefähigkeit besteht **bereits**; sie ist
> weder Teil von TD-19 noch erfordert sie eine Änderung an
> `app/security/plugin_security.py` [SOURCE: docs/governance/naw-a-od05-change-surface-fixation.md Kap. 7, E-1].

---

## 8. `SecurityBootstrapStage`

**Antworten auf die zwölf Fragen des Auftrags (Kap. 9):**

| # | Frage | Befund | Klasse |
|---|---|---|---|
| 1 | Wo wird sie erzeugt? | In `create_desktop_bootstrap_manager()`, angehängt an eine Kopie von `default_stages()` [SOURCE: BASELINE 8fcf42f:ui/navigation/navigation_service.py:148] | **EXISTING** |
| 2 | In welcher Phase läuft sie? | `phase: StartupPhase = StartupPhase.FINALIZE` [SOURCE: BASELINE 8fcf42f:app/security/security_manager.py:`SecurityBootstrapStage`] | **EXISTING** |
| 3 | Was erzeugt/registriert sie? | `SecurityManager.create(events, logger=context.logger)`, dann `manager.register(registry)` und `manager.initialize()` | **EXISTING** |
| 4 | Was ersetzt sie? | In `SecurityManager.register`: `registry._registrations.pop(PluginSecurity, None)` gefolgt von `registry.register(PluginSecurity, self._plugins)` [SOURCE: BASELINE 8fcf42f:app/security/security_manager.py:203–204] | **TD-19** |
| 5 | Welche Security-Instanz existiert davor? | Die von `PluginSecurityStage` in LOAD_PLUGINS erzeugte und registrierte Instanz — mit den Ergebnissen der Admission im Ledger | **TD-19** |
| 6 | Welche danach? | Die von `SecurityManager.create` erzeugte Instanz — mit **leerem** Ledger | **TD-19** |
| 7 | Welche Policy verwendet sie? | `plugins = PluginSecurity(events, logger=resolved_logger)` — **ohne Policy-Argumente** ⇒ `IntegrityPolicy()` und `PermissionPolicy()` (default-deny) [SOURCE: BASELINE 8fcf42f:app/security/security_manager.py:116] | **TD-19** |
| 8 | Welche Konfiguration verwendet sie? | **Keine.** `SecurityManager.create(cls, events, *, encryption=None, logger=None)` besitzt **keinen** Policy- oder Konfigurationsparameter [SOURCE: BASELINE 8fcf42f:app/security/security_manager.py:`SecurityManager.create`] | **TD-19** |
| 9 | Gibt es eine Diskontinuität? | **JA** — Instanz, Ledger-Inhalt und (nach Option B) Policy | **TD-19** |
| 10 | Ist diese Diskontinuität TD-19? | **JA**, hinsichtlich T-a, T-b, T-c (Kap. 4.1) | **TD-19** |
| 11 | Wird sie durch OD-05 verändert? | **NEIN** — `app/security/security_manager.py` ist nicht Teil der fixierten Change-Surface [SOURCE: docs/governance/naw-a-od05-change-surface-fixation.md Kap. 7, E-6] | **NOT REQUIRED** |
| 12 | Muss sie für OD-05 verändert werden? | **NEIN** — Begründung in Kap. 12.2 | **NOT REQUIRED** |

> **F-4 behebt nichts. Es stellt fest.**

---

## 9. `SecurityManager`

| Aspekt | Befund | Klasse |
|---|---|---|
| Verantwortlichkeit | Koordinator; komponiert und registriert die Security-Services | **EXISTING** |
| Erzeugung von `PluginSecurity` | Zeile 116, ohne Policy-Argumente | **TD-19** |
| Registrierung | `register(registry)` — inklusive `pop()` für `PluginSecurity` | **TD-19 / TD-06** |
| Zugriffspunkt | Property `plugins` (Zeile 175) | **EXISTING** |
| Konfigurationsparameter | **keine** in `create()` | **TD-19** |

### 9.1 Registrierungsstellen von `PluginSecurity` — vollständige Erhebung

| # | Ort | Phase |
|---|---|---|
| 1 | `app/bootstrap/stages_plugin.py:266` | **LOAD_PLUGINS** |
| 2 | `app/security/security_manager.py:204` | **FINALIZE** |

> **Es existiert keine dritte Registrierungsstelle und keine Registrierung vor
> LOAD_PLUGINS.**
> [SOURCE: `git grep "register(PluginSecurity" 8fcf42f -- '*.py'`, Nicht-Test-Treffer]

### 9.2 Konsequenz für den `LookupError`-Zweig

Da vor LOAD_PLUGINS niemand registriert, schlägt `registry.get(PluginSecurity)` in
`PluginSecurityStage.execute` **stets** fehl, und der `except LookupError`-Zweig
greift. **Die dort konstruierte Instanz ist stets diejenige, gegen die die
Admission geprüft wird.**

**Klassifikation: EXISTING (Baseline-Eigenschaft), belegt.**

### 9.3 Zusatzbefund

Die Reihenfolge in `SecurityManager.register` ist `pop()` **vor** `register()`
[SOURCE: BASELINE 8fcf42f:app/security/security_manager.py:203–204]. Der `pop()`
ist der als **TD-06** dokumentierte Kapselungsbruch
[SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §6.5 AM-04]. **TD-06
bleibt eine eigene Position und wird hier nicht behandelt** (Kap. 13.2).

### 9.4 Konsumenten der FINALIZE-Instanz

| Prüfung | Ergebnis |
|---|---|
| `registry.get(PluginSecurity)` außerhalb von `stages_plugin.py:263`? | **KEIN Treffer** in produktivem Code |
| Zugriffe auf `SecurityManager.plugins`? | **KEIN Treffer** in produktivem Code — die `.plugins`-Treffer betreffen `context.plugins` (den `PluginLoader`) und Logger-Namensräume |
| `SecurityManager`-Konsumenten | `ui/navigation/main_window.py:57`, `dashboard_page.py`, `status_bar.py`, `navigation_service.py:125` — **keiner** greift auf `plugins` zu |

[SOURCE: `git grep "PluginSecurity" 8fcf42f -- '*.py'` und `git grep "\.plugins\b" 8fcf42f -- '*.py'`, jeweils ohne `tests/`]

> **Feststellung:** Die in FINALIZE registrierte `PluginSecurity`-Instanz hat am
> Baseline **keinen produktiven Konsumenten**. **Dies ist eine Feststellung zur
> gegenwärtigen Wirkung, keine Bewertung von TD-19 und keine Entwarnung** —
> SEC-07 bleibt als INFERENCE und DEVIATION bestehen.

---

## 10. Policy Continuity

**Prüffrage:** Bleibt die in LOAD_PLUGINS verwendete Policy dieselbe
Security-Autorität, die später in FINALIZE registriert ist?

### 10.1 Am Baseline

| Instanz | Konstruktion | Policies |
|---|---|---|
| LOAD_PLUGINS | `PluginSecurity(events, logger=logger)` [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:265] | `IntegrityPolicy()` / `PermissionPolicy()` (Defaults) |
| FINALIZE | `PluginSecurity(events, logger=resolved_logger)` [SOURCE: BASELINE 8fcf42f:app/security/security_manager.py:116] | `IntegrityPolicy()` / `PermissionPolicy()` (Defaults) |

> **Befund:** Die beiden Instanzen sind **funktional nicht identisch** — es sind
> zwei getrennte Objekte mit getrennten Ledgern —, tragen am Baseline aber
> **wertgleiche Policies**. Die TD-19-Diskontinuität betrifft heute **Identität und
> Ledger-Inhalt (T-a, T-b)**, **nicht** die Policy.
>
> **Ausdrücklich nicht aus dem Klassennamen geschlossen:** Die Wertgleichheit ist
> aus den beiden Konstruktoraufrufen belegt, nicht aus der Typgleichheit.

### 10.2 Nach Umsetzung von Option B über CS-1

| Instanz | Policies |
|---|---|
| LOAD_PLUGINS | **konfiguriert** (aus `[security]` über `from_config`) |
| FINALIZE | weiterhin **fest verdrahtete Defaults** — `SecurityManager.create` besitzt keinen Policy-Parameter (Kap. 8, Frage 8) |

> **Befund F-4-N:** Option B fügt der bestehenden TD-19-Divergenz eine **dritte
> Dimension** hinzu: **Policy-Diskontinuität**. Diese Dimension existiert am
> Baseline **nicht**.
>
> **Klassifikation:** Folge derselben Ursache (Kap. 11); **kein neuer Technical
> Debt**. Ob sie vom dokumentierten TD-19-Wortlaut (T-a…T-c) bereits erfasst ist
> oder als Präzisierung des „teilweise"-Restumfangs zu führen wäre, ist den
> Quellen **nicht** zu entnehmen → **UNKNOWN / OPEN DECISION** (Kap. 18, F4-U2).

### 10.3 Praktische Wirkung der Policy-Diskontinuität

| Prüfung | Befund |
|---|---|
| Wird die FINALIZE-Policy von produktivem Code ausgewertet? | **NEIN** — kein Konsument (Kap. 9.4) |
| Beeinflusst sie die Admission? | **NEIN** — die Admission ist zum Zeitpunkt der Ersetzung abgeschlossen (SEC-07) |
| Beeinflusst sie `context.admitted_manifests` oder den `PluginCatalog`? | **NEIN** — beide werden in LOAD_PLUGINS gesetzt |
| Ist sie damit umsetzungsblockierend für Option B? | **NEIN** (Kap. 12.3) |

---

## 11. TD-19 Root Cause

**Aus den Quellen übernommen, ohne neue Taxonomie:**

> **R0 §18.4 Cluster 2:** „Der `SecurityManager` wurde als *additive* FINALIZE-Stage
> **nachgerüstet**, während die Plugin-Pipeline in LOAD_PLUGINS bereits eigene
> Defaults erzeugt."

**Zuordnung zu den im Auftrag genannten Kandidaten (Kap. 7 des Auftrags):**

| Kandidat | Zutreffend? | Einordnung |
|---|---|---|
| **A — doppelte Security-Instanz** | **JA** | **Erscheinungsform** — zwei unabhängige Instanzen (Kap. 9.1) |
| **B — falscher Lebenszyklus** | **teilweise** | Die FINALIZE-Komposition ist gegenüber der LOAD_PLUGINS-Nutzung **zeitlich nachgelagert**. R0 bezeichnet die additive Nachrüstung als Ursache, **nicht** die Phasenzuordnung als „falsch" → wertende Einstufung **nicht** übernommen |
| **C — spätere Ersetzung** | **JA** | **Mechanismus** — `pop()` + `register()` in FINALIZE (Kap. 8, Frage 4) |
| **D — fehlende Autoritäts-/Policy-Kontinuität** | **JA** | **Wirkung** — T-b, T-c; nach Option B zusätzlich Policy (Kap. 10.2) |
| **E — fehlende Konfigurationsweitergabe** | **teilweise** | `SecurityManager.create` besitzt keinen Policy-Parameter. Dies ist am Baseline **folgenlos**, weil beide Instanzen Defaults tragen; es wird erst **durch Option B** wirksam. Abzugrenzen von **TD-05** (fehlender Konfigurationsweg überhaupt) |
| **F — anderes** | — | keine weitere Ursache aus den Quellen belegbar |

> **Zusammenfassung ohne neue Begriffsbildung:** Ursache ist die **additive
> Nachrüstung** (R0 §18.4); Mechanismus ist die **Ersetzung in FINALIZE**;
> Erscheinungsform ist die **doppelte Instanz**; Wirkung ist die **fehlende
> Kontinuität** von Ledger und — nach Option B — Policy.

---

## 12. OD-05 Interaction

### 12.1 Ausgangslage

**OD-05 Option B:** „Policy-Konfiguration in die bestehende `PluginSecurityStage`
ziehen (ohne Reihenfolgeänderung)"
[SOURCE: docs/governance/od-05-governance-decision.md Kap. 8].
**Fixierte Change-Surface:** CS-1 + CS-2 + CS-3
[SOURCE: docs/governance/naw-a-od05-change-surface-fixation.md Kap. 6].

### 12.2 Frage A — Kann Option B ohne `app/security/security_manager.py` umgesetzt werden?

> ## **JA.**

**Frage B — Begründung:**

| # | Begründungsschritt | Beleg |
|---|---|---|
| B-1 | Der entschiedene Gegenstand von Option B ist die **Policy-Konfiguration der Admission**. Die Admission vollzieht sich vollständig in **LOAD_PLUGINS**, in den Schritten 1–4 von `PluginSecurityStage.execute` | [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:271–333] |
| B-2 | Die dafür maßgebliche Instanz wird **in derselben Stage** erzeugt — im `except LookupError`-Zweig | [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:262–266] |
| B-3 | Dieser Zweig greift **stets**, weil vor LOAD_PLUGINS **keine** Registrierung existiert (Kap. 9.1, 9.2) | [SOURCE: vollständige Erhebung der Registrierungsstellen] |
| B-4 | `PluginSecurity.__init__` nimmt beide Policy-Objekte **bereits** entgegen; eine Änderung an `plugin_security.py` ist nicht erforderlich | [SOURCE: BASELINE 8fcf42f:app/security/plugin_security.py:`PluginSecurity.__init__`] |
| B-5 | Die Konfigurationszuführung erfolgt über **CS-2** und **CS-3**, beide außerhalb von `app/security/**` | [SOURCE: docs/governance/naw-a-od05-change-surface-fixation.md Kap. 6.2, 6.3] |
| B-6 | Die FINALIZE-Instanz hat **keinen produktiven Konsumenten** (Kap. 9.4) und beeinflusst die Admission nicht (SEC-07) | [SOURCE: Kap. 9.4; docs/audits/jochen-x-master-engineering-plan-r0.md §10.6 SEC-07] |

**Frage C — entfällt**, da Frage A mit JA beantwortet ist. **Es besteht keine
zwingende technische Abhängigkeit von `app/security/security_manager.py`.**

### 12.3 Ist ein TD-19-Anteil umsetzungsblockierend?

| Prüfung | Befund |
|---|---|
| Verhindert T-a (Instanz-Ersetzung) die Wirksamkeit der konfigurierten Admission? | **NEIN** — die Ersetzung erfolgt **nach** Abschluss der Admission |
| Verhindert T-b (Ledger-Diskontinuität) sie? | **NEIN** — der Ledger wird für die Admission innerhalb derselben Stage geführt |
| Verhindert die neue Policy-Diskontinuität (Kap. 10.2) sie? | **NEIN** — kein produktiver Konsument der FINALIZE-Policy |
| **Ergebnis** | **TD-19 ist nicht IMPLEMENTATION-BLOCKING für OD-05 Option B** |

### 12.4 Was durch OD-05 **nicht** berührt wird

| # | TD-19-Bestandteil | Status nach Option B |
|---|---|---|
| T-a | Instanz-Ersetzung in FINALIZE | **unverändert — OPEN** |
| T-b | Trust-Ledger-Diskontinuität (`IntegrityResult`/`PermissionResult` fehlen) | **unverändert — OPEN** |
| T-c | Wirkungslosigkeit der SecurityManager-Instanz für die Admission | **unverändert — OPEN** |
| SG-E / TG-3 | Nachweis der Trust-Ledger-Identität | **unverändert nicht erfüllt / nicht erbracht** |

### 12.5 Ergebnis der Fallzuordnung

| Fall | Zutreffend? |
|---|---|
| **FALL A** — TD-19 wird durch OD-05 **nicht** berührt | **nein** — Kap. 10.2 belegt eine Wechselwirkung |
| **FALL B** — TD-19 wird **teilweise** berührt | **JA** |
| **FALL C** — TD-19 ist umsetzungsblockierend | **nein** — Kap. 12.3 |

> ## **TD-19 = PARTIALLY IMPACTED**
>
> **Genau betroffener Teil:** die **Policy-Kontinuität** zwischen der in
> LOAD_PLUGINS verwendeten und der in FINALIZE registrierten
> `PluginSecurity`-Instanz. Am Baseline sind beide policy-wertgleich; nach
> Umsetzung von Option B über CS-1 wären sie es **nicht mehr** (Kap. 10.1, 10.2).
>
> **Nicht betroffen:** T-a, T-b, T-c bleiben **unverändert OPEN** (Kap. 12.4).

---

## 13. Required vs Not Required

### 13.1 Zuordnung

| Artefakt | Für OD-05 Option B | Für TD-19 | Klasse |
|---|---|---|---|
| `app/bootstrap/stages_plugin.py` (CS-1) | **REQUIRED** | nicht ausreichend | **REQUIRED** |
| `config/settings.py` (CS-2) | **REQUIRED** | nicht betroffen | **REQUIRED** |
| `config/default.toml` (CS-3) | **REQUIRED** | nicht betroffen | **REQUIRED** |
| `app/security/security_manager.py` | **NOT REQUIRED** (Kap. 12.2) | **einschlägig** — Ort von T-a/T-c | **NOT REQUIRED für OD-05; separat für TD-19** |
| `app/security/plugin_security.py` | **NOT REQUIRED** | nicht ursächlich | **NOT REQUIRED** |
| `ui/navigation/navigation_service.py` | **NOT REQUIRED** | Ort der Stage-Anhängung | **NOT REQUIRED** |
| `core/registry.py` | **NOT REQUIRED** | Symptomort **TD-06** | **NOT REQUIRED** |
| `sdk/context.py` | — | — | **NOT AUTHORIZED** (TD-04) |

### 13.2 Abgrenzung zu anderen Technical-Debt-Positionen

| Position | Beziehung zu TD-19 | Behandlung in F-4 |
|---|---|---|
| **TD-04** | Eigenständige MISSING-Position (Host-Grants im `PluginContext`); hängt an **OD-01 + OD-05** | **nicht behandelt; OPEN / NOT AUTHORIZED** |
| **TD-05** | Fehlender Konfigurationsweg; wird durch Option B adressiert. **Nicht identisch** mit dem in Kap. 11 E genannten Aspekt, der die Weitergabe an die FINALIZE-Instanz betrifft | **nicht geschlossen; OPEN** |
| **TD-06** | Im R0 als **Symptom** von TD-19 eingeordnet (die `pop()`-Stellen) | **nicht behandelt; OPEN** |
| **TD-21** | Audit-Trail; Substanz an **ODD-17** gebunden | **nicht behandelt; OPEN** |

> **TD-19 bleibt TD-19.** Keine Position wird verschmolzen, umbenannt oder
> geschlossen.

---

## 14. Change-Surface Assessment

| Prüfung | Ergebnis |
|---|---|
| Erfordert die korrekte Umsetzung von OD-05 Option B eine zusätzliche Datei? | **NEIN** (Kap. 12.2) |
| **CHANGE-SURFACE EXPANSION REQUIRED?** | **NEIN** |
| Change Surface | **CS-1 + CS-2 + CS-3 — unverändert** |

> **F-4 erweitert die NAW-A-Change-Surface nicht und autorisiert keine
> Erweiterung.**

**Feststellung für eine spätere, gesondert zu autorisierende TD-19-Behandlung
(keine Empfehlung, keine Autorisierung):** Eine Behandlung von T-a/T-c läge in
`app/security/security_manager.py` und ggf. in der Stage-Komposition. Beides ist
**nicht** Gegenstand von OD-05 und bedürfte einer eigenen Governance-Entscheidung;
für eine Änderung der Stage-Zusammensetzung wäre zudem **§8-5** einschlägig
[SOURCE: docs/baselines/bootstrap-baseline-1.0.md §8].

---

## 15. Security Impact

| # | Feststellung | Status |
|---|---|---|
| S-1 | **TD-19 bleibt OPEN** — T-a, T-b, T-c unverändert | **OPEN** |
| S-2 | **SG-E** („Trust-Ledger-Identität über die Phasen") bleibt **nicht erfüllt**; **TG-3** bleibt erforderlich und nicht erbracht | **OPEN** |
| S-3 | **SG-C** und **SG-D** unverändert; **TG-2** und **TG-4** erforderlich und nicht erbracht | **OPEN** |
| S-4 | **QG-006** bleibt **NOT STARTED** | **NOT STARTED** |
| S-5 | **Default-Deny** bleibt erhalten; NAW-A untersagt neue Grants und die produktive Freischaltung eines Plugins | **EXISTING** |
| S-6 | **TD-04 / TD-05 / TD-06 / TD-21** unverändert **OPEN**; TD-04 zusätzlich **NOT AUTHORIZED** | **OPEN** |
| S-7 | **ODD-17** und **OD-04** unverändert **OPEN**; jedes Permission-Modell bleibt bis zur Klärung von OD-04 **beratend, nicht erzwingend** [SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §10.4 SEC-04] | **OPEN** |
| S-8 | **RB-1.0 (258/14)** unverändert | **EXISTING** |
| S-9 | Die in Kap. 10.2 festgestellte Policy-Diskontinuität ist **derzeit ohne produktiven Konsumenten**; sie ist für die spätere TD-19-Behandlung festzuhalten | **UNKNOWN / OPEN DECISION** (F4-U2) |

> **F-4 schließt kein Security Finding, keine ODD, kein Quality Gate und keinen
> Technical Debt. F-4 ändert weder Security Design noch Security Architecture und
> definiert weder Policy, Trust Boundary noch Authority.**

---

## 16. Architecture Freeze

| Prüfung | Ergebnis |
|---|---|
| Erzeugt F-4 einen Befund, der **F-1-A** widerspricht? | **NEIN** |
| `app/security/security_manager.py` in AB §22.1? | **NEIN** — `app/security/**` ist im enumerierten Freeze-Scope nicht enthalten [SOURCE: BASELINE 8fcf42f:docs/architecture-book-v2.md §22.1] |
| Wird ein §22.3-Tatbestand berührt? | **NEIN** — insbesondere keine Änderung der Bootstrap-Phasenreihenfolge |
| Berührt der Befund aus Kap. 10.2 den Freeze? | **NEIN** — er betrifft `app/security/**` und `app/bootstrap/stages_plugin.py`, beide außerhalb des Freeze-Scopes bzw. außerhalb der auf Protocol und Enum verengten Bootstrap-Position |

> ## **ARCHITECTURE FREEZE: F-1-A UNCHANGED**
>
> Kein Architecture Book geändert, keine AB-Version erzeugt.

---

## 17. ADR/RDR Boundary

| Feld | Wert |
|---|---|
| Change Control | **REQUIRED** — durch **NAW-B** (§8-4 = TRIGGERED) festgestellt; F-4 ändert daran nichts |
| ADR ↔ RDR | **OPEN** — kein Abgrenzungskriterium in einer autorisierten Quelle [SOURCE: docs/baselines/bootstrap-baseline-1.0.md §8; docs/governance/f-02-bootstrap-baseline-scope-assessment.md Kap. 9] |
| **B-6** | **OPEN** |
| Rolle von F-4 | **F-4 liefert Input für F-5.** F-4 entscheidet weder ADR noch RDR und erstellt keines von beidem |

---

## 18. Remaining UNKNOWNs

| ID | Frage | Status | Zuständig |
|---|---|---|---|
| **F4-U1** | Der im R0 nicht ausgeführte „teilweise"-Restumfang von TD-19 (**U-3**) | **präzisiert, nicht aufgelöst**: F-4 stellt fest, dass T-a, T-b und T-c **vollständig** ungelöst bleiben und Option B keinen dieser Bestandteile adressiert. Ob R0 mit „teilweise" ausschließlich die TD-05-Wirkung meinte, ist den Quellen **nicht** zu entnehmen | **UNKNOWN** |
| **F4-U2** | Ist die in Kap. 10.2 festgestellte **Policy-Diskontinuität** vom dokumentierten TD-19-Wortlaut erfasst, oder wäre sie als eigener Bestandteil zu führen? | **UNKNOWN / OPEN DECISION** — F-4 erfindet keine neue Position und verschmilzt keine bestehende | Security-/Architektur-Governance |
| **F4-U3** | Ob ein künftiger Konsument der FINALIZE-Instanz entstünde und die Policy-Diskontinuität dann wirksam würde | **UNKNOWN** — nicht ohne Laufzeit-/Zukunftsannahme feststellbar; **kein Test ausgeführt** | — |
| **F4-U4** | Abgrenzungskriterium **ADR ↔ RDR** (**B-6**) | **OPEN** | **F-5** |
| **NAW-A-U1** | Wahl zwischen den CS-2-Varianten V-1 / V-2 | **OFFEN** | autorisierte Umsetzung |
| **NAW-A-U2 / C-3** | Z-1, Z-2 und die Typprüfung an der `[security]`-Zugriffsstelle | **OFFEN** | autorisierte Umsetzung |

> Es wurde kein Test ausgeführt, um ein UNKNOWN künstlich zu beseitigen.

---

## 19. Findings

| # | Finding | Klasse |
|---|---|---|
| **F-4-01** | Es existieren genau **zwei** Registrierungsstellen für `PluginSecurity`; **keine** vor LOAD_PLUGINS. Der `except LookupError`-Zweig greift daher stets | **EXISTING** |
| **F-4-02** | Option B ist hinsichtlich der Admission **ohne** Änderung an `app/security/security_manager.py` umsetzbar | **NOT REQUIRED** |
| **F-4-03** | `SecurityManager.create` besitzt **keinen** Policy- oder Konfigurationsparameter | **TD-19** |
| **F-4-04** | Am Baseline tragen **beide** `PluginSecurity`-Instanzen **wertgleiche** Default-Policies; die TD-19-Divergenz betrifft heute Identität und Ledger, **nicht** Policy | **EXISTING — neuer Befund** |
| **F-4-05** | Nach Option B entstünde zusätzlich eine **Policy-Diskontinuität** zwischen beiden Instanzen | **TD-19 / PARTIALLY IMPACTED** |
| **F-4-06** | Die FINALIZE-registrierte Instanz hat am Baseline **keinen produktiven Konsumenten** | **EXISTING** |
| **F-4-07** | TD-19 ist **nicht** umsetzungsblockierend für OD-05 Option B | **Ergebnis** |
| **F-4-08** | T-a, T-b und T-c bleiben **vollständig OPEN**; SG-E und TG-3 unverändert | **OPEN** |
| **F-4-09** | **Keine Change-Surface-Erweiterung erforderlich** | **Ergebnis** |
| **F-4-10** | **F-1-A** wird durch keinen Befund widerlegt | **bestätigt** |

---

## 20. F-5 Input

**F-4 liefert F-5 folgende Eingangsgrößen — ohne F-5 vorwegzunehmen:**

| # | Input für F-5 |
|---|---|
| I-1 | Die Change-Surface bleibt **CS-1 + CS-2 + CS-3**; keine Erweiterung |
| I-2 | **TD-19 = PARTIALLY IMPACTED**, nicht blockierend; die betroffene Dimension ist die **Policy-Kontinuität** |
| I-3 | **§8-4 = TRIGGERED** (durch NAW-B); **CHANGE CONTROL = REQUIRED** |
| I-4 | **§8-1, §8-2, §8-3, §8-5 = NOT TRIGGERED** — durch F-4 nicht verändert |
| I-5 | **ADR ↔ RDR (B-6)** bleibt offen und ist von F-5 zu behandeln |
| I-6 | **F4-U2** (Einordnung der Policy-Diskontinuität) ist bei der TD-19-Fortschreibung zu berücksichtigen |
| I-7 | **NAW-1** ist von Ergebnis **D** fortzuschreiben — erst durch F-5 |

**F-5 hat anschließend:** (1) den finalen Change-Surface-Stand zu prüfen, (2) §8-1
bis §8-5 erneut gegen den finalen Umriss zu prüfen, (3) die ADR-/RDR-Frage **B-6**
zu behandeln, (4) das **NAW-1**-Ergebnis zu aktualisieren.

> **F-4 nimmt F-5 nicht vorweg und startet F-5 nicht.**

---

## 21. Repository Integrity

| Prüfung | Vor F-4 | Nach F-4 |
|---|---|---|
| HEAD | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` | **unverändert** |
| Baseline-Hash | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` | **unverändert** |
| `git status` — getrackte Modifikationen | 6 | **6 — unverändert** |
| Staged changes | 0 | **0 — kein Staging** |
| Untracked (`-uall`) | 80 | 81 — **+1**: dieses Dokument |
| Bestandsdateien geändert | — | **0** |
| Tests | — | **nicht verändert, NICHT AUSGEFÜHRT** |
| Commit / Tag / Push / Cleanup | — | **KEINE** |

**BASELINE ≠ WORKING TREE ≠ UNTRACKED DOCS** — sämtlicher Code ausschließlich
über `git show 8fcf42f:<pfad>`.

---

## 22. Final Status

| Feld | Wert |
|---|---|
| **F-4** | **COMPLETED** |
| **TD-19** | **PARTIALLY IMPACTED** |
| **Betroffener Teil** | **Policy-Kontinuität** zwischen LOAD_PLUGINS- und FINALIZE-Instanz |
| **Nicht betroffen** | T-a (Instanz-Ersetzung), T-b (Ledger-Diskontinuität), T-c (Wirkungslosigkeit) — **unverändert OPEN** |
| **Umsetzungsblockierend** | **NEIN** |
| **OD-05** | **OPTION B — UNCHANGED** |
| **CHANGE SURFACE** | **CS-1 + CS-2 + CS-3** — keine Erweiterung erforderlich |
| **§8-1** | **NOT TRIGGERED** |
| **§8-2** | **NOT TRIGGERED** |
| **§8-3** | **NOT TRIGGERED** |
| **§8-4** | **TRIGGERED** |
| **§8-5** | **NOT TRIGGERED** |
| **ARCHITECTURE FREEZE** | **F-1-A UNCHANGED** |
| **CHANGE CONTROL** | **REQUIRED** |
| **ADR/RDR** | **OPEN** |
| **B-6** | **OPEN** |
| **TD-04** | **OPEN / NOT AUTHORIZED** |
| **TD-05** | **OPEN** |
| **TD-06** | **OPEN** |
| **TD-19** | **OPEN** |
| **TD-21** | **OPEN** |
| **ODD-17 / OD-04** | **OPEN** |
| **QG-006** | **NOT STARTED** |
| **RB-1.0** | **unverändert (258/14)** |
| **Sprint Plan** | **unverändert** |
| **F-5** | **NEXT GOVERNANCE STEP** |
| **CODING** | **NOT AUTHORIZED** |
| **TESTS** | **NOT EXECUTED** |

---

**Ende F-4 TD-19 Remaining-Scope Assessment — JOCHEN X Milestone 1.0
(FINAL ASSESSMENT, 2026-08-10) — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
