# JOCHEN X — Milestone 1.0
# NAW-B — G-1 Precision: Observable State Values

| Feld | Wert |
|---|---|
| Dokumenttyp | Governance Assessment / G-1-Präzisierung (READ-ONLY) |
| **ID** | **NAW-B** |
| Status | **FINAL GOVERNANCE ASSESSMENT** |
| Gegenstand | Präzisierung von **G-1 = OPTION HYBRID** zur Frage **F3-U2**: Gehören von Stages erzeugte Zustandswerte zum geschützten Kontrakt von `run_phase()`? |
| Governance Input | **Projekteigner-Entscheidung** (Kap. 4) · **G-1 = OPTION HYBRID** · **NAW-A** (COMPLETED) · **F-3** · **GDR-OD05-001** (Option B) |
| Datum | 2026-08-10 |
| Branch / HEAD | `milestone-1.0-governance` / `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| Bezugs-Baseline | `MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8` |
| **Ergebnis** | **§8-4 = TRIGGERED** · **CHANGE CONTROL = REQUIRED** |
| Coding | **NOT AUTHORIZED** |

---

## 1. Executive Decision

**Der Projekteigner hat F3-U2 entschieden.** Unter **G-1 HYBRID** gehören auch
Zustandswerte, die eine Stage über den bestehenden `BootstrapContext` erzeugt oder
verändert, zum geschützten beobachtbaren Kontrakt von `run_phase()` — sofern sie
für nachfolgende Bootstrap-Stufen oder für den Aufrufer beobachtbar bzw. für das
Ergebnis der Bootstrap-Ausführung bestimmend sind.

**Damit ist die letzte offene Grundlage für die §8-4-Unbestimmtheit aufgelöst:**

| Grund aus F-3 | Status |
|---|---|
| **R-3** — neuer `BootstrapError`-Pfad in INITIALIZE | **entfallen** durch **NAW-A** (Festlegung A) |
| **F3-U2 / R-5** — Einordnung geänderter Zulassungswerte | **entschieden** durch **NAW-B** — sie sind Kontraktbestandteil |

> ## **§8-4 = TRIGGERED** · **CHANGE CONTROL = REQUIRED**

**Was das nicht bedeutet:** Option B ist **nicht** verboten und **nicht**
verändert. Sie fällt hinsichtlich des in NAW-A festgelegten Änderungsumfangs unter
die Change Control der Bootstrap Baseline §8 (Kap. 5.3, 9.3).

**Was offen bleibt:** **ADR/RDR = OPEN** (B-6), **F-4** (TD-19-Restumfang) und
**F-5** (Wiederholungsprüfung).

---

## 2. Ausgangslage F-3 / NAW-A

| # | Eingangsgröße | Fundstelle |
|---|---|---|
| A-1 | **F-3** stellte fest: `begin()` = UNCHANGED · `run_phase()` = **UNKNOWN** · `build_context()` = UNCHANGED; §8-4 = UNKNOWN aus **zwei** Gründen (R-3 und R-5/F3-U2) | [SOURCE: docs/governance/f-03-od05-change-surface-assessment.md Kap. 8–10, 18] |
| A-2 | **NAW-A** legte fest: `[security]` = **OPTIONAL** ⇒ **R-3 entfällt**; kein neues öffentliches Symbol ⇒ **§8-3 = NOT TRIGGERED** (determinat) | [SOURCE: docs/governance/naw-a-od05-change-surface-fixation.md Kap. 3, 4.2, 5, 10.3] |
| A-3 | **NAW-A** fixierte die minimale Änderungsfläche: **CS-1** (`app/bootstrap/stages_plugin.py`), **CS-2** (`config/settings.py`), **CS-3** (`config/default.toml`) | [SOURCE: docs/governance/naw-a-od05-change-surface-fixation.md Kap. 6] |
| A-4 | **NAW-A** stellte fest: nach der Fixierung ruht §8-4 = UNKNOWN **nur noch** auf **F3-U2** | [SOURCE: docs/governance/naw-a-od05-change-surface-fixation.md Kap. 1, 10.4, 13] |
| A-5 | **NAW-A** Status: **AUTHORIZED / COMPLETED** | [SOURCE: docs/governance/naw-a-od05-change-surface-fixation.md Kap. 16] |

---

## 3. F3-U2

**Die offene Frage lautete:**

> Erfasst G-1 HYBRID mit „beobachtbarem Verhaltenskontrakt" auch die von Stages
> über den `BootstrapContext` erzeugten **Zustandswerte** — oder nur
> Ausführungsordnung, Rückgabe und Fehlerverhalten?

**Warum sie offen war** [SOURCE: docs/governance/f-03-od05-change-surface-assessment.md Kap. 14.2]:
Der dokumentierte Kontrakt von `run_phase()` lautet „Execute every stage belonging
to `phase` in registration order. **Raises:** `BootstrapError` if a stage fails"
[SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py:`run_phase`]. Unter dem
fixierten Umriss bleiben Ausführungsordnung, Rückgabe und Fehlerverhalten
unverändert; **verändert würden die Werte**, die eine Stage in den mutablen
Context schreibt. Ob G-1 diese erfasst, war dem Entscheidungswortlaut nicht zu
entnehmen. F-3 durfte dies nicht selbst beantworten, weil das eine Erweiterung
von G-1 gewesen wäre.

---

## 4. Projekteigner-Entscheidung

> ### **ENTSCHEIDUNG: JA**
>
> Unter **G-1 HYBRID** gehören auch solche Zustandswerte zum geschützten
> beobachtbaren Kontrakt von `run_phase()`, die von einer Stage über den
> **bestehenden** `BootstrapContext` erzeugt oder verändert werden, sofern diese
> Werte für **nachfolgende Bootstrap-Stufen** oder für **Aufrufer** beobachtbar
> bzw. für das Ergebnis der Bootstrap-Ausführung **bestimmend** sind.
>
> Insbesondere sind **`context.admitted_manifests`** und der von der
> `PluginSecurityStage` registrierte **`PluginCatalog`** Bestandteil des
> beobachtbaren Ergebnisses von `BootstrapManager.run_phase(...)`, **wenn sich
> diese Werte aufgrund der Änderung ändern.**

| Feld | Wert |
|---|---|
| Entscheidende Instanz | **Projekteigner** |
| Charakter | **Präzisierung** von G-1, keine Neuentscheidung |
| Wirkung | Auflösung von **F3-U2** |
| Nicht entschieden | ADR ↔ RDR (B-6); TD-19-Restumfang (F-4); Umsetzungsfreigabe |

---

## 5. Definition des beobachtbaren Kontrakts

### 5.1 Die maßgebliche Governance-Regel

> **Unter G-1 HYBRID sind Zustandswerte, die durch die Ausführung einer
> `BootstrapStage` über den bestehenden `BootstrapContext` erzeugt oder verändert
> werden und für nachfolgende Bootstrap-Stufen oder den Aufrufer beobachtbar
> sind, Bestandteil des beobachtbaren Kontrakts von `run_phase()`. Eine Änderung
> solcher Werte ist daher §8-4-relevant.**
>
> **Rein interne Änderungen ohne beobachtbare Wirkung bleiben außerhalb von §8-4.**

### 5.2 Der beobachtbare Kontrakt — vier Bestandteile

| # | Bestandteil | Status |
|---|---|---|
| 1 | **Rückgabeverhalten** | bereits durch G-1 erfasst |
| 2 | **Fehlerverhalten** | bereits durch G-1 erfasst |
| 3 | **Ausführungsordnung** | bereits durch G-1 erfasst |
| 4 | **Durch die Ausführung erzeugte, über den bestehenden `BootstrapContext` beobachtbare Zustandswerte** | **durch NAW-B präzisiert** |

### 5.3 Was die Regel nicht besagt

| # | Ausdrücklich nicht |
|---|---|
| N-1 | **NICHT**, dass Option B verboten wäre |
| N-2 | **NICHT**, dass jede interne Stage-Änderung §8-4-relevant ist (Kap. 8) |
| N-3 | **NICHT**, dass ein neues Feld im `BootstrapContext` eingeführt werden dürfte oder müsste — die Regel bezieht sich auf den **bestehenden** Context |
| N-4 | **NICHT**, dass §8-1, §8-2, §8-3 oder §8-5 erweitert würden (Kap. 11) |
| N-5 | **NICHT**, dass eine Änderung der Stage-Reihenfolge vorläge oder zulässig wäre |

---

## 6. `admitted_manifests`

**Belegte Beobachtbarkeit im Baseline-Code:**

| # | Befund | Fundstelle |
|---|---|---|
| M-1 | Geschrieben von `PluginSecurityStage` (**LOAD_PLUGINS**): `context.admitted_manifests = resolved` | [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:335] |
| M-2 | **Gelesen von `PluginActivationStage` (FINALIZE)**: `admitted_ids = frozenset(m.identifier for m in context.admitted_manifests)` sowie `for manifest in context.admitted_manifests:` | [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:468, 476] |
| M-3 | Zusätzlich in der Abschlussdiagnostik der Aktivierung ausgewertet | [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:585] |
| M-4 | Das Feld existiert **bereits** im `BootstrapContext` — es wird durch Option B **nicht** neu eingeführt | [SOURCE: BASELINE 8fcf42f:app/bootstrap/types.py:`BootstrapContext`] |

> **Einordnung:** `admitted_manifests` ist **bestimmend für eine nachfolgende
> Bootstrap-Stufe** — die Aktivierung iteriert unmittelbar über diesen Wert. Damit
> erfüllt es das in Kap. 5.1 formulierte Kriterium.

---

## 7. `PluginCatalog`

**Belegte Beobachtbarkeit im Baseline-Code:**

| # | Befund | Fundstelle |
|---|---|---|
| K-1 | Initial registriert von `PluginDiscoveryStage` mit allen entdeckten Identifiern | [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:58, 65–66] |
| K-2 | Von `PluginSecurityStage` **ersetzt** durch den gefilterten Katalog: `filtered = PluginCatalog(tuple(m.identifier for m in resolved))`, anschließend `registry._registrations.pop(PluginCatalog, None)` und `registry.register(PluginCatalog, filtered)` | [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:336–339] |
| K-3 | **Vom Aufrufer gelesen**: `plugin_catalog = context.services.get(PluginCatalog)` — dabei ist `context` der aus `build_context()` hervorgegangene `ApplicationContext` | [SOURCE: BASELINE 8fcf42f:ui/navigation/main_window.py:68] |
| K-4 | Der Zugriffsweg besteht bereits: `ApplicationContext.services` wird aus `context.service_provider` gesetzt | [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py:`build_context`] |

> **Einordnung:** Der `PluginCatalog` ist **für den Aufrufer beobachtbar** —
> er wird nach Abschluss des Bootstraps über den `ApplicationContext` gelesen.
> Damit erfüllt auch er das Kriterium aus Kap. 5.1.

**Hinweis (Feststellung, keine Bewertung):** Die `pop()`-Stelle in K-2 ist der als
**TD-06** dokumentierte Kapselungsbruch. Er besteht bereits am Baseline und ist
**nicht** Gegenstand von NAW-B
[SOURCE: docs/audits/jochen-x-master-engineering-plan-r0.md §6.5 AM-04].

---

## 8. Abgrenzung zu BROAD

**Diese Präzisierung macht G-1 nicht zu OPTION BROAD.**

| Kriterium | BROAD (nicht gewählt) | **HYBRID nach NAW-B** |
|---|---|---|
| Auslösekriterium | **Ort** der Änderung — jede Stage-interne Logik als solche | **Wirkung** der Änderung auf den beobachtbaren Kontrakt |
| Interner Bugfix ohne Außenwirkung | §8-4-pflichtig | **nicht** §8-4-pflichtig |
| Umbenennung einer stage-internen Hilfsvariable | §8-4-pflichtig | **nicht** §8-4-pflichtig |
| Stage-Änderung, die beobachtbare Zustandswerte ändert | §8-4-pflichtig | **§8-4-pflichtig** |

> **Es gilt ausdrücklich NICHT:** „Jede interne Änderung einer Stage ist
> automatisch §8-4-relevant."
>
> **Es gilt:** Eine interne Änderung ist unter §8-4 nur dann relevant, wenn sie
> eine **beobachtbare Wirkung** auf den bestehenden `BootstrapManager`-Kontrakt
> erzeugt — Rückgabeverhalten, Fehlerverhalten, Ausführungsordnung oder
> beobachtbare Zustandswerte.

Die in F-2 dokumentierten Quellenstützen bleiben unberührt: **RDR-001 Invariante 5**
bindet „`BootstrapManager`-Verhalten" an `begin()`, `run_phase()` und
`build_context()` — genau diese drei Methoden sind auch nach NAW-B der
Bezugspunkt; präzisiert wurde ausschließlich, **was** zu ihrem beobachtbaren
Ergebnis zählt
[SOURCE: docs/rdr/001-bootstrap-modularization.md §3 Inv. 5; docs/governance/f-02-bootstrap-baseline-scope-assessment.md Kap. 8.1].

---

## 9. §8-4 Determination

### 9.1 Anwendung der Regel auf den fixierten Umriss

| Schritt | Befund |
|---|---|
| 1 | Der fixierte Umriss **CS-1 + CS-2 + CS-3** bewirkt, dass die Policy nicht mehr fest verdrahtet, sondern aus der Konfiguration gespeist wird [SOURCE: docs/governance/naw-a-od05-change-surface-fixation.md Kap. 6] |
| 2 | Die Policy bestimmt unmittelbar das Ergebnis der Permission-Autorisierung und damit die Menge `admitted` in `PluginSecurityStage.execute` [SOURCE: BASELINE 8fcf42f:app/bootstrap/stages_plugin.py:`PluginSecurityStage.execute`, Schritt 3] |
| 3 | Aus `admitted` entstehen `context.admitted_manifests` (M-1) und der registrierte `PluginCatalog` (K-2) |
| 4 | Beide Werte sind nach der Entscheidung aus Kap. 4 Bestandteil des beobachtbaren Kontrakts von `run_phase()` (M-2, M-3, K-3) |

> ## **§8-4 = TRIGGERED**

### 9.2 Präzisierung zur Reichweite der Auslösung

Die Entscheidung knüpft an „**wenn sich diese Werte aufgrund der Änderung
ändern**". Dazu ist festzuhalten:

| # | Feststellung |
|---|---|
| P-1 | NAW-A hat ausdrücklich untersagt, neue Grants zu erfinden oder ein Plugin produktiv freizuschalten [SOURCE: docs/governance/naw-a-od05-change-surface-fixation.md Kap. 6.3] |
| P-2 | Ein `[security]`-Abschnitt **ohne** Grants ergibt über `PermissionPolicy.from_config` `wildcard = frozenset()` und `plugin_grants = {}` — identisch zur heutigen leeren Policy [SOURCE: BASELINE 8fcf42f:app/security/plugin_security.py:`PermissionPolicy.from_config`] |
| P-3 | **Folge:** In einem Lauf mit der ausgelieferten, grantfreien Konfiguration wären `admitted_manifests` und `PluginCatalog` **wertgleich** zum Baseline-Lauf |
| P-4 | **Was sich gleichwohl ändert:** Diese Werte werden durch den Umriss **konfigurationsabhängig**. Über `config/profile.toml` — den bestehenden Profilweg [SOURCE: BASELINE 8fcf42f:config/settings.py:`ConfigurationService.load`] — sind ab dann andere Zulassungsergebnisse erreichbar, ohne dass Code geändert würde |

> **Die Determination des Projekteigners stellt auf diese Änderung der
> Wertbestimmung ab, nicht auf die Wertgleichheit eines einzelnen Laufs.**
> P-1 bis P-4 sind Feststellungen zur Auditierbarkeit und **stellen die
> Determination nicht in Frage**; sie halten fest, worauf sie beruht, damit
> **F-5** dies nachvollziehen kann.

### 9.3 Was TRIGGERED bedeutet — und was nicht

| # | Bedeutung |
|---|---|
| T-1 | **Change Control nach Bootstrap Baseline §8 ist erforderlich**, bevor der Umriss umgesetzt wird |
| T-2 | **NICHT:** Option B ist verboten |
| T-3 | **NICHT:** Option B ist verändert — der Wortlaut bleibt unverändert |
| T-4 | **NICHT:** eine Umsetzungsfreigabe ist erteilt |
| T-5 | Die konkrete Umsetzung bleibt von der danach erforderlichen Governance-/Change-Control-Kette abhängig |

Implementation Plan **GC-06** verlangt die genehmigte Governance-Entscheidung
ausdrücklich **„vor der Implementierung"**
[SOURCE: docs/milestone-1.0-implementation-plan.md GC-06]. Diese Voraussetzung ist
nach NAW-B **anwendbar und noch nicht erfüllt**.

---

## 10. Auswirkungen auf `run_phase()`

| Aspekt | Vor NAW-B (F-3/NAW-A) | Nach NAW-B |
|---|---|---|
| Signatur / Rückgabetyp | unverändert | **unverändert** |
| Ausführungsordnung der Stages | unverändert | **unverändert** |
| Fehlerverhalten (`BootstrapError`-Wrapping) | unverändert; R-3 entfallen durch NAW-A | **unverändert** |
| Beobachtbare Zustandswerte (`admitted_manifests`, `PluginCatalog`) | **UNKNOWN** | **CHANGED** — Kontraktbestandteil und durch den Umriss konfigurationsabhängig |
| **Gesamtergebnis** | **UNKNOWN** | ## **CHANGED** |

**Die beiden anderen Methoden bleiben unberührt:**

| Methode | Ergebnis | Begründung |
|---|---|---|
| `begin()` | **UNCHANGED** | Erzeugt lediglich einen frischen `BootstrapContext`; keine Berührung durch den Umriss [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py:`begin`] |
| `build_context()` | **UNCHANGED** | Die 12 über `_require` geprüften Felder sind unberührt; `admitted_manifests` fließt nicht ein; die Registry-Instanz wird unverändert übergeben [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py:`build_context`; docs/governance/f-03-od05-change-surface-assessment.md Kap. 10] |

---

## 11. Auswirkungen auf §8-1 / §8-2 / §8-3 / §8-5

> **Diese Präzisierung verändert keinen dieser vier Tatbestände. Sie bleiben
> eigenständig.**

| Tatbestand | Ergebnis | Begründung |
|---|---|---|
| **§8-1** Paketstruktur | **NOT TRIGGERED** | Kein Modul im Bootstrap-Paket hinzugefügt, entfernt oder umbenannt; CS-2 und CS-3 liegen außerhalb des Baseline-Scopes §2 [SOURCE: docs/baselines/bootstrap-baseline-1.0.md §2, §8] |
| **§8-2** Runtime-Pipeline | **NOT TRIGGERED** | Phasen- und Stage-Reihenfolge unverändert; Admission-Reihenfolge Integrity → API-Version → Permission → Dependency → Activation unangetastet [SOURCE: docs/governance/naw-a-od05-change-surface-fixation.md Kap. 6.1, 10.2] |
| **§8-3** Public Exports | **NOT TRIGGERED** | `__all__` unverändert (NAW-A Festlegung B) [SOURCE: docs/governance/naw-a-od05-change-surface-fixation.md Kap. 5] |
| **§8-5** `default_stages()` | **NOT TRIGGERED** | Zusammensetzung und Reihenfolge unverändert; `PluginSecurityStage()` bleibt an Position 9 [SOURCE: BASELINE 8fcf42f:app/bootstrap/manager.py:`default_stages`] |

> **Ausdrücklich:** Dass `admitted_manifests` als Kontraktbestandteil geschützt
> ist, darf **nicht** als Änderung der Stage-Reihenfolge interpretiert werden.
> **OD-05 Option B bleibt: „Policy-Konfiguration in die bestehende
> `PluginSecurityStage` ziehen (ohne Reihenfolgeänderung)."**

**Architecture Freeze:** Kein neuer Sachverhalt widerspricht **F-1-A**. `config/**`
ist in AB §22.1 nicht aufgeführt; der Freeze-Scope für `app/bootstrap` ist auf
**BootstrapStage-Protocol** und **StartupPhase-Enum** verengt — beide unberührt
[SOURCE: BASELINE 8fcf42f:docs/architecture-book-v2.md §22.1; docs/governance/f-01-od05-architecture-freeze-assessment.md Kap. 10].
**F-1-A bleibt unverändert.**

---

## 12. ADR/RDR Status

| Prüfung | Befund |
|---|---|
| Ist §8 Change Control ausgelöst? | **JA** — §8-4 = TRIGGERED (Kap. 9) |
| **CHANGE CONTROL** | **REQUIRED** |
| Bestimmt eine autorisierte Quelle die Wahl **ADR ↔ RDR**? | **NEIN** — Bootstrap Baseline §8 nennt beide alternativ **ohne Abgrenzungskriterium**; der Development Standard v1.1 enthält keine RDR-Regeln [SOURCE: docs/baselines/bootstrap-baseline-1.0.md §8; docs/governance/f-02-bootstrap-baseline-scope-assessment.md Kap. 9, 19] |

> ## **ADR/RDR = OPEN** · **B-6 = OPEN**
>
> **NAW-B erfindet kein Kriterium und löst B-6 nicht.**
> **Kein ADR erstellt. Kein RDR erstellt.**

---

## 13. F-4 Boundary

> **F-4 bleibt unabhängig erforderlich. NAW-B nimmt F-4 nicht vorweg.**

| Feld | Inhalt |
|---|---|
| Gegenstand von F-4 | **F3-U3** — verbleibender **TD-19**-Umfang [SOURCE: docs/governance/od-05-governance-decision.md U-3] |
| Sachverhalt | `SecurityBootstrapStage` (FINALIZE) ersetzt die registrierte `PluginSecurity`-Instanz [SOURCE: BASELINE 8fcf42f:app/security/security_manager.py:203–204] |
| Wirkung von NAW-B | **keine** — `app/security/security_manager.py` ist nicht Teil des fixierten Umrisses [SOURCE: docs/governance/naw-a-od05-change-surface-fixation.md Kap. 7, E-6] |
| Status | **TD-19 = OPEN — F-4** |

---

## 14. F-5 Dependency

| Position | Status |
|---|---|
| **NAW-A** | **COMPLETED** |
| **NAW-B** | **COMPLETED** |
| **F-4** | **OPEN** — weiterhin erforderlich |
| **F-5** | **OPEN** — anschließend erforderlich |

**Aufgabe von F-5** (Feststellung, keine Autorisierung): Wiederholung der
§8-Prüfung gegen den **final** festgelegten Änderungsumfang und anschließende
Behandlung der **ADR/RDR-Frage (B-6)**. Erst danach ist **NAW-1** von Ergebnis
**D** fortzuschreiben
[SOURCE: docs/governance/naw-01-od05-adr-rdr-assessment.md Kap. 10, 13].

> **NAW-B startet F-4 und F-5 nicht.** Beide bedürfen einer eigenen,
> ausdrücklichen Autorisierung.

---

## 15. Remaining UNKNOWNs

| ID | Frage | Status |
|---|---|---|
| ~~**F3-U1**~~ | `[security]` verpflichtend oder optional? | **GESCHLOSSEN** — NAW-A (OPTIONAL) |
| ~~**F3-U4**~~ | Neues öffentliches Bootstrap-Symbol? | **GESCHLOSSEN** — NAW-A (NEIN) |
| ~~**F3-U2**~~ | Zustandswerte Teil des Kontrakts? | **GESCHLOSSEN** — NAW-B (JA) |
| **F3-U3** | Verbleibender **TD-19**-Umfang | **OFFEN** — F-4 |
| **F3-U5 / B-6** | Abgrenzungskriterium **ADR ↔ RDR** | **OFFEN** — F-5 |
| **F3-U6** | Ob die Kontraktwirkung ohne Testlauf abschließend feststellbar ist | **gegenstandslos für die §8-4-Determination** — diese folgt aus der Governance-Regel (Kap. 5.1), nicht aus einer Messung. Für den späteren Umsetzungsnachweis bleibt die Frage offen |
| **NAW-A-U1** | Wahl zwischen den CS-2-Varianten V-1 / V-2 | **OFFEN** — autorisierte Umsetzung; V-1 als bevorzugt ausgewiesen |
| **NAW-A-U2** | Z-1 (`save_profile` schreibt `[security]` nicht zurück) und Z-2 (einstufiger `_merge`) | **OFFEN** — dokumentiert, nicht entschieden |
| **C-3** (NAW-A) | Typprüfung an der `[security]`-Zugriffsstelle als Eigenschaft des Umrisses | **OFFEN** — autorisierte Umsetzung |

> Es wurde nicht implementiert und kein Test ausgeführt, um ein UNKNOWN
> künstlich zu beseitigen.

---

## 16. Repository Integrity

| Prüfung | Vor NAW-B | Nach NAW-B |
|---|---|---|
| HEAD | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` | **unverändert** |
| Baseline-Hash | `8fcf42f1997dfcf6ff232e75fd33c37b933991c8` | **unverändert** |
| `git status` — getrackte Modifikationen | 6 | **6 — unverändert** |
| Staged changes | 0 | **0 — kein Staging** |
| Untracked (`-uall`) | 79 | 80 — **+1**: dieses Dokument |
| Bestandsdateien geändert | — | **0** |
| Tests | — | **nicht verändert, nicht ausgeführt** |
| Commit / Tag / Push / Cleanup | — | **KEINE** |

**BASELINE ≠ WORKING TREE ≠ UNTRACKED DOCS** — sämtlicher Code ausschließlich
über `git show 8fcf42f:<pfad>` gelesen; keine Working-Tree-Datei als Baseline
behandelt.

---

## 17. Final Status

| Feld | Wert |
|---|---|
| **NAW-A** | **AUTHORIZED / COMPLETED** |
| **NAW-B** | **AUTHORIZED / COMPLETED** |
| **G-1** | **OPTION HYBRID — PRECISISED** |
| **OD-05** | **OPTION B — UNCHANGED** |
| **`[security]`** | **OPTIONAL** |
| **NEW PUBLIC EXPORT** | **NO** |
| **MINIMAL CHANGE SURFACE** | **CS-1 + CS-2 + CS-3** |
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
| **TD-19** | **OPEN — F-4** |
| **TD-21** | **OPEN** |
| **ODD-17 / OD-04** | **OPEN** |
| **QG-006** | **NOT STARTED** |
| **RB-1.0** | **unverändert (258/14)** |
| **Sprint Plan** | **unverändert** |
| **F-4** | **OPEN** |
| **F-5** | **OPEN** |
| **CODING** | **NOT AUTHORIZED** |

> **NAW-B ist eine Governance-Präzisierung — keine Umsetzungsfreigabe, keine
> Coding-Autorisierung, keine Sprint-Freigabe. Kein Security Finding, keine ODD,
> kein Technical Debt und kein Quality Gate wurde geschlossen.**

---

**Ende NAW-B G-1 Precision — JOCHEN X Milestone 1.0
(FINAL GOVERNANCE ASSESSMENT, 2026-08-10) — Bezugs-Baseline
`MILESTONE-1.0-BASELINE = 8fcf42f1997dfcf6ff232e75fd33c37b933991c8`**
