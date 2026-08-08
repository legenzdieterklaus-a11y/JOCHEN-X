# Core Principles 1.0 — Revision History Update R2

| Eigenschaft | Wert |
|---|---|
| **Dokumenttyp** | Revision History Update — Correction Cycle R2 |
| **Gegenstand** | [JOCHEN X – Core Principles 1.0](../core-principles-1.0.md) |
| **Datum** | 2026-08-07 |
| **Anlass** | Correction Cycle R2; Schließung von W3-E-01 und Fortschreibung nach Governance Rule 3 |
| **Grundlage** | Governance Rule 3 — Anforderungen „dokumentierter Änderungsgrund" und „Eintrag in der Revisionshistorie" |
| **Status** | **COMPLETED** |

---

## 1. Zweck

Zwei Anlässe:

1. **Schließung W3-E-01.** Der Independent Review W-3 stellte fest, dass die
   Revisionshistorie für R0 kein Prüfartefakt führte, obwohl R0 durch den
   Governance Review W-1 geprüft wurde. Die Historie erfüllte damit ihre eigene
   Vorgabe nicht.
2. **Fortschreibung.** Governance Rule 3 verlangt für jede Änderung einen
   Eintrag in der Revisionshistorie. Revision R2 ist einzutragen.

---

## 2. Revisionshistorie nach R2

| Revision | Datum | Auslöser | Änderungsumfang | Prüfartefakt |
|---|---|---|---|---|
| R0 | 2026-08-07 | Ersterstellung | Kapitel 0–12 und Schlussbestimmung erstellt | Governance Review W-1 |
| R1 | 2026-08-07 | Governance Review W-1: PASS WITH FINDINGS — REVISION REQUIRED | Schließung von 3 High-, 11 Medium-, 4 Low- und 2 Editorial-Findings; 2 Low-Findings mit dokumentiertem Waiver | Correction Report R1, Verification Summary R1, Independent Review W-3 |
| R2 | 2026-08-07 | Independent Governance Review W-3: REVISION REQUIRED | Schließung von 1 High-, 3 Medium-, 4 Low- und 1 Editorial-Finding; keine Waiver | Correction Report R2, Verification Summary R2 |

### Änderungen gegenüber dem Stand nach R1

| Zeile | Feld | Vorher | Nachher | Anlass |
|---|---|---|---|---|
| R0 | Prüfartefakt | „—" | „Governance Review W-1" | W3-E-01 |
| R1 | Prüfartefakt | „Correction Report R1, Verification Summary R1" | zusätzlich „Independent Review W-3" | W3-E-01 |
| R2 | gesamte Zeile | nicht vorhanden | neu eingetragen | Governance Rule 3 |

---

## 3. Geänderte Kopfdaten

| Feld | R1 | R2 | Anlass |
|---|---|---|---|
| Revision | R1 | **R2** | Correction Cycle |
| Vorgängerrevision | „R0 (2026-08-07), geprüft durch Governance Review W-1" | **„R1 (2026-08-07), geprüft durch Independent Governance Review W-3"** | Fortschreibung |
| Referenzen | 13 Einträge | **14 Einträge** — ergänzt um „Core Principles 1.0 Independent Review W-3 · COMPLETED" | Fortschreibung des deklaratorischen Bestands |
| Status | DRAFT | **DRAFT** (unverändert) | — |
| Version | 1.0 | **1.0** (unverändert) | — |
| Datum | 2026-08-07 | **2026-08-07** (unverändert) | — |
| Genehmigungsinstanz | Projekteigner JOCHEN X | unverändert | — |
| Genehmigt | offen | unverändert | — |
| Gültigkeit | unverändert | unverändert | — |

---

## 4. Nachweiskette der Revisionen

| Schritt | Artefakt | Ergebnis |
|---|---|---|
| Erstellung | Core Principles 1.0 R0 | DRAFT |
| W-1 | Governance Review Report W-1 | PASS WITH FINDINGS — REVISION REQUIRED (3 High, 11 Medium, 6 Low, 2 Editorial) |
| W-2 | Correction Report R1, Verification Summary R1, Revision History Update R1 | 20 CLOSED, 2 WAIVER → R1 |
| W-3 | Independent Governance Review W-3 | REVISION REQUIRED (1 High, 3 Medium, 4 Low, 1 Editorial) |
| R2 | Correction Report R2, Verification Summary R2, Revision History Update R2 | 9 CLOSED, 0 WAIVER → R2 |
| W-4 | Independent Governance Review W-4 | ausstehend |
| — | Approval Record | nicht autorisiert; erst nach W-4 |

Die Kette ist lückenlos. Jede Revision ist mit Auslöser, Umfang und
Prüfartefakt belegt. Keine Stufe wurde übersprungen, keine Genehmigung
vorweggenommen.

---

## 5. Fortschreibungsregel

Unverändert gegenüber Revision History Update R1. Ergänzend gilt nach der in R2
präzisierten Fassung von Governance Rule 3:

| Anforderung | Ablageort |
|---|---|
| Neue Version oder Revision | Kopffeld „Revision" bzw. „Version" und Revisionshistorie |
| Dokumentierter Änderungsgrund | Spalte „Auslöser" |
| Folgenabschätzung für gebundene Dokumente | Prüfartefakt |
| Governance Review vor der Entscheidung | Prüfartefakt |
| **Bei Änderungen an Kapitel 0 oder Kapitel 12: unabhängiger Review** | Prüfartefakt; Form nach Development Standard |
| Entscheidung der Genehmigungsinstanz | Approval Record; Kopffeld „Genehmigt" |
| Eintrag in der Revisionshistorie | Revisionshistorie |
| **Erstgenehmigung** | Nicht Gegenstand von Rule 3; Verfahren nach Development Standard |

Ein Eintrag wird nie überschrieben. Frühere Revisionen bleiben mit Auslöser und
Prüfartefakt dauerhaft nachvollziehbar.

**Hinweis für künftige Zyklen.** Die Revision R2 hat Kapitel 0 geändert. Nach
der in R2 präzisierten Fassung von Governance Rule 3 erfordern Änderungen an
Kapitel 0 künftig einen unabhängigen Review. Diese Anforderung gilt ab
Genehmigung des Dokuments und wirkt nicht auf R2 zurück (Geltungsvorbehalt,
Governance Rule 1).

---

## 6. Verifikation

| Prüfung | Ergebnis |
|---|---|
| W3-E-01 geschlossen | ✓ |
| R0 mit Prüfartefakt geführt | ✓ |
| R1 mit vollständigem Prüfartefakt geführt | ✓ |
| R2 eingetragen | ✓ |
| Auslöser je Revision benannt | ✓ |
| Kopfdaten fortgeschrieben | ✓ |
| Kein normativer Gehalt eingeführt | ✓ |
| Kein neues Kapitel entstanden | ✓ |
| Kein Eintrag überschrieben | ✓ |
| Status DRAFT unverändert | ✓ |

---

**Ende Revision History Update R2**
