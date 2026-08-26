#!/usr/bin/env bash
#
# JOCHEN X — Technisches Verifikationsskript (Milestone 1.0)
#
# Zweck: ausschliesslich reproduzierbare Fakten erheben. Das Skript trifft
# keine Governance-Entscheidung, schliesst kein Quality Gate und setzt keinen
# Acceptance-Criterion-Status.
#
# Ergebniswerte je Pruefung:
#   PASS     Pruefung ausgefuehrt und erfuellt
#   FAIL     Pruefung ausgefuehrt und nicht erfuellt
#   UNKNOWN  Pruefung nicht ausfuehrbar (fehlendes Werkzeug, fehlende Eingabe)
#   INFO     Bestandsaufnahme ohne Bewertung — auch fuer diagnostische
#            Pruefungen, die kein genehmigter Maszstab fordert
#
# PASS/FAIL setzt einen genehmigten Maszstab voraus. Fehlt er, ist das
# Ergebnis INFO; ist die Pruefung gar nicht durchfuehrbar, UNKNOWN.
#
# UNKNOWN ist ausdruecklich NICHT "bestanden".
#
# Exit-Codes: 0 = kein FAIL und kein UNKNOWN | 1 = mindestens ein FAIL
#             2 = kein FAIL, aber mindestens ein UNKNOWN | 3 = Aufruffehler
#
# Aufruf:
#   scripts/verify_gate.sh [--baseline <sha>] [--quick]
#
#   --baseline <sha>  Vergleichsbasis fuer Diff- und Scope-Pruefungen
#   --quick           Testlaeufe ueberspringen (Ergebnis dann UNKNOWN)

set -u

REQUIRED_PYTHON_MAJOR=3
REQUIRED_PYTHON_MINOR=13

# --------------------------------------------------------------- Test-Scope
#
# Der Gate-Scope ist explizit und reproduzierbar: er besteht aus genau zwei
# Bloecken. Es findet KEINE dynamische Sammlung ueber tests/ statt, damit der
# stillgelegte Bestand (src/jochen_x, GDR-002 D-2) nicht einfliesst.
#
# Quelle: docs/milestone-1.0-sprint-plan.md Kapitel 2 — Ziel ist
# „keine Regressionen gegen RB-1.0 zuzueglich der in MWB-015 hinzukommenden
# Tests".

# Block 1 — Regressionsbasis RB-1.0 (14 Dateien, Soll 258 Tests)
RB10_FILES="
tests/test_activation_validation.py
tests/test_application_foundation.py
tests/test_capability_matrix.py
tests/test_core.py
tests/test_dependency_resolution.py
tests/test_developer.py
tests/test_foundation.py
tests/test_golden_reference.py
tests/test_manifest_v2.py
tests/test_navigation.py
tests/test_plugin_observability.py
tests/test_sdk.py
tests/test_security_foundation.py
tests/integration/test_plugin_integration.py
"
RB10_EXPECTED_TESTS=258

# Block 2 — MWB-015-Zugaenge aus WP-001..WP-007 (6 Dateien, Soll 128 Tests)
MWB015_FILES="
tests/test_platform_hardening.py
tests/test_host_services_extensions.py
tests/test_developer_experience.py
tests/test_observability_extension.py
tests/test_reliability.py
tests/test_documentation_currency.py
"
MWB015_EXPECTED_TESTS=128

# Gesamter Gate-Scope: 20 Dateien, Soll 386 Tests
GATE_SCOPE_FILES="$RB10_FILES $MWB015_FILES"
GATE_EXPECTED_TESTS=386

# Pfade, die ohne ausdrueckliche Human Decision unveraendert bleiben muessen
FORBIDDEN_PATHS="docs/architecture-book-v2.md"

API_SNAPSHOT_SDK="scripts/baselines/sdk_api_surface_1.0.0.json"
API_SNAPSHOT_BOOTSTRAP="scripts/baselines/app_bootstrap_api_surface_1.0.0.json"
DOC_CURRENCY_TEST="tests/test_documentation_currency.py"

BASELINE=""
QUICK=0

while [ $# -gt 0 ]; do
    case "$1" in
        --baseline)
            [ $# -ge 2 ] || { echo "fehlendes Argument fuer --baseline" >&2; exit 3; }
            BASELINE="$2"; shift 2 ;;
        --quick) QUICK=1; shift ;;
        -h|--help) sed -n '2,26p' "$0" | sed 's/^#\{1,\} \{0,1\}//'; exit 0 ;;
        *) echo "unbekanntes Argument: $1" >&2; exit 3 ;;
    esac
done

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
cd "$REPO_ROOT" || exit 3

PASS_COUNT=0
FAIL_COUNT=0
UNKNOWN_COUNT=0

report() {
    # report <STATUS> <ID> <Text>
    status="$1"; id="$2"; shift 2
    printf '%-8s %-10s %s\n' "$status" "$id" "$*"
    case "$status" in
        PASS) PASS_COUNT=$((PASS_COUNT + 1)) ;;
        FAIL) FAIL_COUNT=$((FAIL_COUNT + 1)) ;;
        UNKNOWN) UNKNOWN_COUNT=$((UNKNOWN_COUNT + 1)) ;;
    esac
}

have() { command -v "$1" >/dev/null 2>&1; }

# core.safecrlf=false unterdrueckt reine Normalisierungshinweise; es aendert
# weder Dateien noch Vergleichsergebnisse.
git() { command git -c core.safecrlf=false "$@"; }

echo "JOCHEN X — verify_gate  ($(date -u '+%Y-%m-%dT%H:%M:%SZ'))"
echo "Repository: $REPO_ROOT"
echo "--------------------------------------------------------------------"

# ---------------------------------------------------------------- Werkzeuge
#
# Interpreter-Auswahl: Ein Kandidat gilt nur dann als Interpreter, wenn er
# tatsaechlich eine Versionsnummer zurueckliefert. Blosse Existenz im PATH
# genuegt nicht — unter Windows liegt in Git Bash ein Microsoft-Store-
# Platzhalter namens `python3` im PATH, der keinen Interpreter startet,
# sondern einen Hinweistext ausgibt. Wird er akzeptiert, faellt die gesamte
# nachgelagerte Pruefkette aus (Befund D-A).
#
# Gewaehlt wird der erste Kandidat, der die Projektvorgabe erfuellt; erfuellt
# keiner sie, wird der erste funktionsfaehige Interpreter fuer die Meldung
# herangezogen, damit die tatsaechlich vorgefundene Version sichtbar wird.

PYTHON=""
PY_VERSION=""
PY_FALLBACK=""
PY_FALLBACK_VERSION=""
PY_CANDIDATES="python3 python py"

for candidate in $PY_CANDIDATES; do
    have "$candidate" || continue
    version=$("$candidate" -c 'import sys; print("%d.%d.%d" % sys.version_info[:3])' 2>/dev/null)
    case "$version" in
        [0-9]*.[0-9]*.[0-9]*) ;;
        *) continue ;;   # kein funktionsfaehiger Interpreter (z. B. Store-Platzhalter)
    esac
    cand_major=${version%%.*}
    cand_rest=${version#*.}
    cand_minor=${cand_rest%%.*}
    if [ "$cand_major" -gt "$REQUIRED_PYTHON_MAJOR" ] || \
       { [ "$cand_major" -eq "$REQUIRED_PYTHON_MAJOR" ] && [ "$cand_minor" -ge "$REQUIRED_PYTHON_MINOR" ]; }; then
        PYTHON="$candidate"
        PY_VERSION="$version"
        break
    fi
    if [ -z "$PY_FALLBACK" ]; then
        PY_FALLBACK="$candidate"
        PY_FALLBACK_VERSION="$version"
    fi
done

if [ -n "$PYTHON" ]; then
    report PASS ENV-01 "$PYTHON $PY_VERSION erfuellt >= $REQUIRED_PYTHON_MAJOR.$REQUIRED_PYTHON_MINOR"
    PY_OK=1
elif [ -n "$PY_FALLBACK" ]; then
    PYTHON="$PY_FALLBACK"
    PY_VERSION="$PY_FALLBACK_VERSION"
    report FAIL ENV-01 "$PYTHON $PY_VERSION unterschreitet die Projektvorgabe >= $REQUIRED_PYTHON_MAJOR.$REQUIRED_PYTHON_MINOR — Testergebnisse waeren nicht massgeblich"
    PY_OK=0
else
    report UNKNOWN ENV-01 "kein funktionsfaehiger Python-Interpreter gefunden (geprueft: $PY_CANDIDATES)"
    PY_OK=0
fi

if [ -n "$PYTHON" ] && "$PYTHON" -m pytest --version >/dev/null 2>&1; then
    PYTEST_OK=1
    report INFO ENV-02 "pytest verfuegbar: $("$PYTHON" -m pytest --version 2>&1 | head -1)"
else
    PYTEST_OK=0
    report INFO ENV-02 "pytest nicht verfuegbar"
fi

# ------------------------------------------------------------------- Git
if ! have git; then
    report UNKNOWN GIT-01 "git nicht verfuegbar — alle Git-Pruefungen entfallen"
    GIT_OK=0
else
    GIT_OK=1
    report INFO GIT-01 "Branch $(git rev-parse --abbrev-ref HEAD) @ $(git rev-parse --short HEAD)"

    # GIT-02 bewertet ausschliesslich den VERSIONIERTEN Bestand: geaenderte,
    # geloeschte oder umbenannte Dateien, die Git bereits verfolgt. Ein
    # unversionierter Eintrag ist kein Defekt des versionierten Standes und
    # wird getrennt in GIT-05 gefuehrt.
    TRACKED_DIRTY=$(git status --porcelain | grep -v '^??' | wc -l | tr -d ' ')
    if [ "$TRACKED_DIRTY" -eq 0 ]; then
        report PASS GIT-02 "versionierter Bestand unveraendert: 0 Abweichungen"
    else
        report FAIL GIT-02 "$TRACKED_DIRTY Abweichung(en) am versionierten Bestand"
        git status --porcelain | grep -v '^??' | sed 's/^/         /'
    fi

    STAGED=$(git diff --cached --name-only | wc -l | tr -d ' ')
    if [ "$STAGED" -eq 0 ]; then
        report PASS GIT-03 "Staging leer"
    else
        report FAIL GIT-03 "$STAGED Datei(en) im Staging"
    fi

    if [ -z "$BASELINE" ]; then
        report UNKNOWN GIT-04 "keine Baseline-SHA uebergeben (--baseline) — Change Surface nicht bestimmbar"
        report UNKNOWN SCOPE-01 "ohne Baseline keine Pruefung der geschuetzten Pfade"
    elif ! git cat-file -e "${BASELINE}^{commit}" 2>/dev/null; then
        report FAIL GIT-04 "Baseline-SHA nicht im Repository: $BASELINE"
        report UNKNOWN SCOPE-01 "Baseline ungueltig — geschuetzte Pfade nicht pruefbar"
    else
        CHANGED=$(git diff --name-only "$BASELINE" -- | wc -l | tr -d ' ')
        report INFO GIT-04 "Change Surface gegen $BASELINE: $CHANGED Datei(en)"
        git diff --stat "$BASELINE" -- | tail -1 | sed 's/^/         /'
        HITS=""
        for path in $FORBIDDEN_PATHS; do
            if git diff --name-only "$BASELINE" -- "$path" | grep -q .; then
                HITS="$HITS $path"
            fi
        done
        if [ -z "$HITS" ]; then
            report PASS SCOPE-01 "keine Aenderung an geschuetzten Pfaden ($FORBIDDEN_PATHS)"
        else
            report FAIL SCOPE-01 "geschuetzte Pfade veraendert:$HITS — Human Decision erforderlich"
        fi
    fi

    # ------------------------------------------------- GIT-05 Ablagekontrolle
    #
    # Grundlage ist eine ausdrueckliche Human Decision, nicht der jeweils
    # vorgefundene Zustand:
    #
    #   JX-DEV-SPR07-D3-VERSIONING-SCOPE-HUMAN-DECISION-R0 (2026-08-24),
    #   Option A: Es werden ausschliesslich die von versionierten Dokumenten
    #   referenzierten Artefakte und die Werkzeuge unter scripts/** versioniert.
    #   Nicht referenzierte Arbeits-, Audit- und Zwischenstaende bleiben
    #   bewusst unversioniert. `.claude/settings.local.json` ist ausdruecklich
    #   als lokale, umgebungsspezifische Werkzeugkonfiguration ausgeschlossen.
    #
    # Daraus folgt die Allowlist unten. Sie ist die technische Umsetzung dieser
    # Entscheidung — nicht ihre nachtraegliche Rechtfertigung. Ein unversionierter
    # Eintrag ausserhalb dieser Bereiche ist unerwartet und ergibt FAIL, damit
    # versehentlich abgelegte Dateien in Code-, Test- oder Skriptpfaden nicht
    # unbemerkt bleiben.

    is_allowed_untracked() {
        case "$1" in
            docs/audits/*|docs/governance/*|docs/rdr/*) return 0 ;;
            .claude/settings.local.json)                return 0 ;;
            docs/*/*)                                   return 1 ;;  # tiefere docs-Ebenen: nicht erfasst
            docs/*.md)                                  return 0 ;;  # nur Dokumente direkt in docs/
            *)                                          return 1 ;;
        esac
    }

    allowed=0
    unexpected=""
    for path in $(git status --porcelain --untracked-files=all | grep '^??' | cut -c4-); do
        if is_allowed_untracked "$path"; then
            allowed=$((allowed + 1))
        else
            unexpected="$unexpected $path"
        fi
    done
    unexpected_count=$(printf '%s\n' $unexpected | grep -c . || true)

    if [ -z "$unexpected" ]; then
        report INFO GIT-05 "$allowed unversionierte Eintraege, alle in den durch D-3 entschiedenen Ablagebereichen; 0 ausserhalb"
    else
        report FAIL GIT-05 "$unexpected_count unversionierte Datei(en) ausserhalb der entschiedenen Ablagebereiche ($allowed innerhalb)"
        for path in $unexpected; do printf '         %s\n' "$path"; done
    fi

    # ------------------------------------------------------------ Zeilenenden
    if [ -f .gitattributes ]; then
        report PASS EOL-01 ".gitattributes vorhanden"
    else
        report FAIL EOL-01 ".gitattributes fehlt — EOL-Rauschen in Diffs moeglich (F-1)"
    fi

    CRLF_INDEX=$(git ls-files --eol | grep -c 'i/crlf' || true)
    if [ "$CRLF_INDEX" -eq 0 ]; then
        report PASS EOL-02 "keine Textdatei mit CRLF im Index"
    else
        report FAIL EOL-02 "$CRLF_INDEX Datei(en) mit CRLF im Index gespeichert"
    fi
fi

# ------------------------------------------------------------------ Tests
run_pytest() {
    # run_pytest <ID> <Beschreibung> <Sollzahl oder 0> <Dateien...>
    id="$1"; label="$2"; expected="$3"; shift 3
    if [ "$QUICK" -eq 1 ]; then
        report UNKNOWN "$id" "$label — uebersprungen (--quick)"
        return
    fi
    if [ "$PYTEST_OK" -eq 0 ]; then
        report UNKNOWN "$id" "$label — pytest nicht verfuegbar"
        return
    fi
    if [ "$PY_OK" -eq 0 ]; then
        report UNKNOWN "$id" "$label — Interpreterversion unterschreitet Projektvorgabe, Ergebnis waere nicht massgeblich"
        return
    fi
    missing=""
    for file in "$@"; do
        [ -f "$file" ] || missing="$missing $file"
    done
    if [ -n "$missing" ]; then
        report FAIL "$id" "$label — fehlende Testdatei(en):$missing"
        return
    fi
    output=$("$PYTHON" -m pytest -q "$@" 2>&1)
    code=$?
    summary=$(printf '%s\n' "$output" | tail -3 | tr '\n' ' ')
    if [ $code -ne 0 ]; then
        report FAIL "$id" "$label — pytest exit $code | $summary"
        return
    fi
    if [ "$expected" -gt 0 ]; then
        passed=$(printf '%s\n' "$output" | grep -oE '[0-9]+ passed' | head -1 | grep -oE '[0-9]+')
        passed=${passed:-0}
        if [ "$passed" -lt "$expected" ]; then
            report FAIL "$id" "$label — $passed Tests, Soll >= $expected (Regressionsbasis unterschritten)"
            return
        fi
        report PASS "$id" "$label — $passed Tests bestanden (Soll >= $expected)"
        return
    fi
    report PASS "$id" "$label — $summary"
}

count_test_functions() {
    # count_test_functions <Dateien...> — statische AST-Zaehlung.
    # Eine Zaehlung ist KEIN Testlauf und ergibt niemals ein Testergebnis.
    "$PYTHON" -B - "$@" <<'PY' 2>/dev/null
import ast, sys
total = 0
for path in sys.argv[1:]:
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except (OSError, SyntaxError):
        continue
    total += sum(
        1
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.startswith("test")
    )
print(total)
PY
}

# SCOPE-02 prueft die Vollstaendigkeit des Gate-Scope, nicht das Testergebnis.
if [ -n "$PYTHON" ]; then
    # shellcheck disable=SC2086
    rb_count=$(count_test_functions $RB10_FILES)
    # shellcheck disable=SC2086
    mwb_count=$(count_test_functions $MWB015_FILES)
    scope_files=$(printf '%s\n' $GATE_SCOPE_FILES | grep -c .)
    total_count=$(( ${rb_count:-0} + ${mwb_count:-0} ))
    report INFO TEST-00 "Statische Zaehlung: RB-1.0 ${rb_count:-?}/$RB10_EXPECTED_TESTS + MWB-015 ${mwb_count:-?}/$MWB015_EXPECTED_TESTS = ${total_count}/$GATE_EXPECTED_TESTS in $scope_files Dateien — Zaehlung, kein Testlauf"
    if [ "$total_count" -eq "$GATE_EXPECTED_TESTS" ] && [ "$scope_files" -eq 20 ]; then
        report PASS SCOPE-02 "Gate-Scope vollstaendig: 20 Dateien, $GATE_EXPECTED_TESTS Testfunktionen (Scope-Pruefung, kein Testergebnis)"
    else
        report FAIL SCOPE-02 "Gate-Scope weicht ab: $scope_files Dateien / $total_count Testfunktionen statt 20 / $GATE_EXPECTED_TESTS"
    fi
else
    report UNKNOWN SCOPE-02 "kein Python-Interpreter — Gate-Scope nicht zaehlbar"
fi

# shellcheck disable=SC2086
run_pytest TEST-01 "Gate-Scope RB-1.0 + MWB-015" "$GATE_EXPECTED_TESTS" $GATE_SCOPE_FILES

# TEST-02 ist eine Teilmenge von TEST-01 (kein zusaetzlicher Scope) und liefert
# ein eigenes Signal fuer den Dokumentationsstand (AC-011/AC-012, EV-D04).
if [ -f "$DOC_CURRENCY_TEST" ]; then
    run_pytest TEST-02 "Dokumentationsaktualitaet (Teilmenge von TEST-01)" 0 "$DOC_CURRENCY_TEST"
else
    report FAIL TEST-02 "Dokumentationstest fehlt, ist aber Teil des Gate-Scope: $DOC_CURRENCY_TEST"
fi

# ------------------------------------------------------------- API-Surface
check_api_surface() {
    # check_api_surface <ID> <package> <snapshot>
    id="$1"; package="$2"; snapshot="$3"
    if [ -z "$PYTHON" ]; then
        report UNKNOWN "$id" "kein Python-Interpreter — API-Surface $package nicht pruefbar"
        return
    fi
    if [ ! -f "$snapshot" ]; then
        report UNKNOWN "$id" "Snapshot fehlt: $snapshot (erzeugen mit: $PYTHON scripts/api_surface.py --package $package --write $snapshot)"
        return
    fi
    output=$("$PYTHON" scripts/api_surface.py --package "$package" --check "$snapshot" 2>&1)
    code=$?
    case $code in
        0) report PASS "$id" "API-Surface $package identisch zum Snapshot" ;;
        1) report FAIL "$id" "API-Surface $package weicht ab — Bewertung (additiv/brechend) ist Human Decision"
           printf '%s\n' "$output" | sed 's/^/         /' ;;
        *) report UNKNOWN "$id" "API-Surface-Pruefung $package nicht ausfuehrbar"
           printf '%s\n' "$output" | sed 's/^/         /' ;;
    esac
}

check_api_surface API-SDK sdk "$API_SNAPSHOT_SDK"
check_api_surface API-BOOT app.bootstrap "$API_SNAPSHOT_BOOTSTRAP"

# ------------------------------------------------------------ Lint / Typen
# Normative Einordnung (Quellenlage, Stand dieses Skripts):
# Weder der NFR-Katalog (NFR-001..NFR-010) noch eines der Quality Gates
# QG-001..QG-008 fordert eine Lint- oder statische Typpruefung. `ruff` und
# `mypy` kommen in Charter, Engineering Specification, Implementation Plan,
# Sprint Plan und Development Standard nicht vor.
#
# Beide Pruefungen sind daher DIAGNOSTISCH und werden als INFO gefuehrt: ihre
# Befunde bleiben sichtbar, erzeugen aber kein FAIL, weil kein genehmigter
# Maszstab existiert, gegen den sie fehlschlagen koennten. Die Tool- und
# Packaging-Konfiguration ist Gegenstand der offenen Entscheidung OD-03.
#
# Ausnahme: Kann `mypy` wegen Modul-/Package-Aufloesung ueberhaupt keine
# Typpruefung durchfuehren, ist das Ergebnis UNKNOWN — nicht INFO und nicht
# FAIL. Ein Abbruch vor der Pruefung ist kein Befund.

if have ruff; then
    lint_output=$(ruff check . --statistics 2>&1)
    if [ $? -eq 0 ]; then
        report INFO LINT-01 "ruff ohne Befund (diagnostisch, nicht normativ gefordert)"
    else
        lint_count=$(printf '%s\n' "$lint_output" | grep -oE 'Found [0-9]+ error' | grep -oE '[0-9]+' | head -1)
        report INFO LINT-01 "ruff meldet ${lint_count:-unbestimmt} Befunde — DIAGNOSTISCH, kein genehmigter Maszstab (OD-03)"
    fi
else
    report INFO LINT-01 "ruff nicht verfuegbar — diagnostische Pruefung entfaellt"
fi

if have mypy; then
    type_output=$(mypy . 2>&1)
    type_code=$?
    case "$type_output" in
        *"Duplicate module named"*|*"Source file found twice"*|*"errors prevented further checking"*)
            type_reason=$(printf '%s\n' "$type_output" | grep -m1 'error:' | sed 's/^[[:space:]]*//')
            report UNKNOWN TYPE-01 "mypy konnte keine Typpruefung durchfuehren — Abbruch bei der Modulaufloesung, kein Typbefund nachgewiesen"
            printf '         %s\n' "${type_reason:-kein Fehlertext}"
            ;;
        *)
            if [ $type_code -eq 0 ]; then
                report INFO TYPE-01 "mypy ohne Befund (diagnostisch, nicht normativ gefordert)"
            else
                report INFO TYPE-01 "mypy meldet Befunde — DIAGNOSTISCH, kein genehmigter Maszstab (OD-03): $(printf '%s\n' "$type_output" | tail -1)"
            fi
            ;;
    esac
else
    report INFO TYPE-01 "mypy nicht verfuegbar — diagnostische Pruefung entfaellt"
fi

# ---------------------------------------------------------------- Ergebnis
echo "--------------------------------------------------------------------"
echo "PASS=$PASS_COUNT  FAIL=$FAIL_COUNT  UNKNOWN=$UNKNOWN_COUNT"
echo
echo "Dieses Skript bewertet keine Acceptance Criteria und schliesst kein"
echo "Quality Gate. UNKNOWN bedeutet: nicht geprueft, nicht bestanden."

if [ "$FAIL_COUNT" -gt 0 ]; then exit 1; fi
if [ "$UNKNOWN_COUNT" -gt 0 ]; then exit 2; fi
exit 0
