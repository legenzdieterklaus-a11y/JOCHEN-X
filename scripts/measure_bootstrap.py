#!/usr/bin/env python3
"""Technische Vorerhebung der Bootstrap-Laufzeiten (PM-01, PM-02, PM-03).

Dies ist eine VORERHEBUNG, keine Baseline-Messreihe. Der Implementation Plan
1.0 verlangt in Anhang B.2, dass eine Baseline-Messreihe nach Bestaetigung des
Baseline-Zustands erhoben wird; diese Bestaetigung gehoert zu einem Zyklus, den
es noch nicht gibt. Ob die hier erzeugten Werte spaeter als Baseline anerkannt
werden, entscheidet der neue Plan.

Uebernommene Methodik (ohne Uebernahme des Plans):

  B.3  Referenzsystem wird protokolliert; ein Wechsel entwertet Messreihen.
  B.4  Identische Konfiguration, keine Fremdlast, gleicher Datenbestand,
       deterministisch; Erst- und Folgeausfuehrung getrennt.
  B.5  Mindestens fuenf Wiederholungen; Median als Kennwert; Streuung als
       Spanne; Streuung > Median  ->  "nicht stabil messbar".
  B.6  PM-01 Gesamtdauer Bootstrap · PM-02 Dauer je Startup-Phase ·
       PM-03 Plugin-Runtime-Pipeline von Discovery bis Activation.
       Ressourcenkennzahlen sind ausdruecklich ausgeschlossen.
  B.9  Protokollpflichtfelder; ein unvollstaendiges Protokoll ist kein Nachweis.

Harte Regel fuer PM-03: Erreicht keine Plugin-Runtime den Zustand STARTED,
wird PM-03 nicht als Zahl ausgewiesen, sondern der Lauf fuer PM-03 als
NICHT VERWERTBAR markiert. "Pipeline ausgefuehrt" ist nicht "Discovery bis
Activation gemessen".

Aufruf:

    python scripts/measure_bootstrap.py --out <pfad-ohne-endung> [--repeats 5]

Das Skript veraendert keine Projektdatei. Es schreibt ausschliesslich die
beiden Protokolldateien an den mit --out angegebenen Pfad und arbeitet
waehrend der Messung in einem temporaeren Verzeichnis.
"""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

__all__ = ["main"]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REFERENCE_PLUGIN = PROJECT_ROOT / "plugins" / "reference"
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "default.toml"

# Stages der Plugin-Runtime-Pipeline (PL-01..PL-05) in Ausfuehrungsreihenfolge.
PIPELINE_STAGES = ("PluginDiscoveryStage", "PluginSecurityStage", "PluginActivationStage")


# --------------------------------------------------------------------------- #
# Instrumentierung
# --------------------------------------------------------------------------- #


@dataclass
class _TimedStage:
    """Kapselt eine Bootstrap-Stage und misst ihre Ausfuehrungsdauer.

    Der Wrapper erfuellt den von :class:`BootstrapManager` erwarteten Vertrag:
    er traegt ``phase`` und stellt ``execute`` bereit. Er veraendert das
    Verhalten der gekapselten Stage nicht.
    """

    inner: Any
    sink: dict[str, float]
    order: list[str]
    phase: Any = field(init=False)

    def __post_init__(self) -> None:
        self.phase = self.inner.phase

    @property
    def name(self) -> str:
        return type(self.inner).__name__

    def execute(self, context: Any) -> None:
        started = time.perf_counter()
        try:
            self.inner.execute(context)
        finally:
            elapsed = (time.perf_counter() - started) * 1000.0
            self.sink[self.name] = self.sink.get(self.name, 0.0) + elapsed
            self.order.append(self.name)


# --------------------------------------------------------------------------- #
# Einzelner Messlauf
# --------------------------------------------------------------------------- #


def _prepare_root(directory: Path) -> Path:
    """Legt eine isolierte Ablaufumgebung mit dem Referenzplugin an.

    ConfigurationStage (stages_init.py:62-69) laedt
    <root>/config/default.toml ueber ConfigurationService.load(); fehlt die
    Datei, bricht INITIALIZE ab. Die Datei wird deshalb aus dem Repository
    kopiert.

    config/profile.toml wird BEWUSST NICHT kopiert: die Profildatei ist
    arbeitsplatzspezifisch und wuerde die Messreihe von lokalen Einstellungen
    abhaengig machen. Die Messung laeuft ausschliesslich gegen die
    versionierte Standardkonfiguration (B.4 Bedingung 3).
    """
    config_dir = directory / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(DEFAULT_CONFIG, config_dir / "default.toml")

    plugin_dir = directory / "plugins"
    plugin_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        REFERENCE_PLUGIN,
        plugin_dir / "reference",
        ignore=shutil.ignore_patterns("__pycache__"),
    )
    (directory / "data").mkdir(exist_ok=True)
    (directory / "logs").mkdir(exist_ok=True)
    return directory


def _close_log_handlers(logger: Any) -> None:
    """Schliesst und entfernt alle Handler des Anwendungsloggers."""
    if logger is None:
        return
    for handler in list(getattr(logger, "handlers", [])):
        try:
            handler.close()
        except Exception:  # noqa: BLE001, S110 - ein defekter Handler darf nicht blockieren
            pass
        logger.removeHandler(handler)


def _install_measurement_security(context: Any) -> None:
    """Registriert die fuer PM-03 erforderliche Plugin-Freigabe.

    ZEITPUNKT IST ZWINGEND: erst NACH StartupPhase.INITIALIZE, unmittelbar VOR
    StartupPhase.LOAD_PLUGINS.

    Grund: app/bootstrap/stages_init.py RegistryStage erzeugt in Zeile 117
    bedingungslos eine neue ServiceRegistry und weist sie in Zeile 132 dem
    Context zu. Eine vor INITIALIZE registrierte PluginSecurity wird dadurch
    verworfen. PluginSecurityStage loest sie in stages_plugin.py Zeile 424 aus
    der Registry auf und faellt bei LookupError auf eine Default-Instanz
    zurueck, unter der das Referenzplugin nicht zugelassen wird — PM-03 waere
    dann nicht messbar.

    Diese Reihenfolge entspricht tests/test_golden_reference.py: PluginSecurity
    erzeugen, "reference" freigeben, registrieren, danach Discovery, Security,
    Activation.

    Die Konfiguration ist Bestandteil der Messkonfiguration und in jeder
    Messreihe identisch zu verwenden (B.4 Bedingung 1).
    """
    from app.security.plugin_security import PermissionPolicy, PluginSecurity

    policy = PermissionPolicy(
        wildcard_grants=frozenset({"events.publish", "events.subscribe"}),
    )
    security = PluginSecurity(
        context.events,
        logger=context.logger,
        permission_policy=policy,
    )
    security.approve("reference")
    context.registry.register(PluginSecurity, security)


def _single_run(root: Path) -> dict[str, Any]:
    """Fuehrt einen vollstaendigen Bootstrap aus und liefert die Rohzeiten."""
    from app.bootstrap import (
        BootstrapManager,
        PluginRuntimePool,
        StartupPhase,
        default_stages,
    )

    stage_ms: dict[str, float] = {}
    stage_order: list[str] = []
    stages = tuple(_TimedStage(stage, stage_ms, stage_order) for stage in default_stages())
    manager = BootstrapManager(stages=stages)

    # Kein vorkonfigurierter Logger, keine vorbelegte Registry, kein
    # vorbelegter EventBus: LoggingStage (stages_init.py:83) und RegistryStage
    # (stages_init.py:117/132-136) erzeugen logger, registry, events, versions
    # und metrics waehrend INITIALIZE selbst. Eine Vorbelegung waere entweder
    # wirkungslos oder wuerde den zu messenden Pfad verfaelschen.
    context = manager.begin(root)

    phase_ms: dict[str, float] = {}
    setup_ms = 0.0
    total_started = time.perf_counter()
    for phase in (
        StartupPhase.INITIALIZE,
        StartupPhase.LOAD_PLUGINS,
        StartupPhase.LOAD_RESOURCES,
        StartupPhase.FINALIZE,
    ):
        # Messkonfiguration nach INITIALIZE, vor LOAD_PLUGINS. Die Dauer wird
        # gesondert erfasst und aus PM-01 herausgerechnet, damit die
        # Vorkonfiguration die Bootstrap-Zeit nicht verfaelscht.
        if phase is StartupPhase.LOAD_PLUGINS:
            setup_started = time.perf_counter()
            _install_measurement_security(context)
            setup_ms = (time.perf_counter() - setup_started) * 1000.0

        started = time.perf_counter()
        manager.run_phase(context, phase)
        phase_ms[phase.name] = (time.perf_counter() - started) * 1000.0
    total_ms = (time.perf_counter() - total_started) * 1000.0 - setup_ms

    # --- Aktivierungsnachweis fuer PM-03
    activated = 0
    states: list[str] = []
    try:
        pool = context.registry.get(PluginRuntimePool)
        for runtime in pool.runtimes:
            state = getattr(runtime.state, "name", str(runtime.state))
            states.append(state)
            if state == "STARTED":
                activated += 1
    except Exception as error:  # noqa: BLE001 - Diagnose, kein Kontrollfluss
        states.append(f"<Runtime-Pool nicht abrufbar: {error}>")

    # --- Vom System selbst erhobene Aktivierungsdauer (Zusatzinformation,
    #     kein Ersatz fuer PM-03 und nicht Teil der B.6-Messgroessen)
    activation_metric: float | None = None
    try:
        snapshot = context.metrics.snapshot()
        for key, value in snapshot.items():
            if key.startswith("plugin.activation.duration_ms"):
                activation_metric = float(value)
                break
    except Exception:  # noqa: BLE001 - Zusatzinformation, kein Kontrollfluss
        activation_metric = None

    # --- Geordnetes Herunterfahren in der Reihenfolge aus app/shutdown.py:
    #     erst die Runtimes, dann die Disposables, zuletzt das Logging.
    #     Das Logging zuletzt, weil dispose_all() noch protokolliert.
    try:
        pool = context.registry.get(PluginRuntimePool)
        for runtime in reversed(pool.runtimes):
            runtime.shutdown()
    except Exception:  # noqa: BLE001, S110 - Aufraeumen darf die Messung nicht kippen
        pass

    try:
        if context.disposables is not None:
            context.disposables.dispose_all()
    except Exception:  # noqa: BLE001, S110
        pass

    # core/logging.py:27 haengt einen RotatingFileHandler an <root>/logs/.
    # configure_logging ruft in Zeile 21 handlers.clear() — das entfernt die
    # Handler, schliesst sie aber NICHT. Ohne explizites close() bleibt je Lauf
    # ein offenes Dateihandle zurueck: unter Windows scheitert daran das
    # Loeschen des temporaeren Verzeichnisses, und ueber die Messreihe hinweg
    # sammeln sich Handles auf bereits beendete Laeufe an.
    _close_log_handlers(context.logger)

    pipeline_sum = sum(stage_ms.get(name, 0.0) for name in PIPELINE_STAGES)
    pipeline_complete = all(name in stage_ms for name in PIPELINE_STAGES)

    return {
        "pm01_total_ms": total_ms,
        "pm02_phase_ms": phase_ms,
        "pm03_pipeline_sum_ms": pipeline_sum,
        "pm03_pipeline_stages_present": pipeline_complete,
        "stage_ms": dict(stage_ms),
        "stage_order": list(stage_order),
        "activated_runtimes": activated,
        "runtime_states": states,
        "activation_metric_ms": activation_metric,
        "measurement_setup_ms": setup_ms,
    }


def _run_isolated(_index: int) -> dict[str, Any]:
    """Fuehrt einen Messlauf in einem eigenen temporaeren Verzeichnis aus.

    Das Aufraeumen erfolgt bewusst NICHT ueber den Kontextmanager von
    TemporaryDirectory: dessen __exit__ wuerde einen Fehler beim rmtree
    weiterreichen und damit eine bereits vollstaendig erhobene Messung
    vernichten. Ein Aufraeumfehler wird stattdessen im Ergebnis gemeldet und
    im Protokoll ausgewiesen — er wird nicht unterdrueckt.
    """
    modules_before = set(sys.modules)
    directory = Path(tempfile.mkdtemp(prefix="jx-measure-"))
    try:
        result = _single_run(_prepare_root(directory))
    finally:
        for name in set(sys.modules) - modules_before:
            sys.modules.pop(name, None)

    cleanup_error: str | None = None
    try:
        shutil.rmtree(directory)
    except OSError as error:
        cleanup_error = f"{type(error).__name__}: {error}"

    result["cleanup_error"] = cleanup_error
    result["temp_dir_removed"] = cleanup_error is None
    if cleanup_error is not None:
        result["temp_dir"] = str(directory)
    return result


# --------------------------------------------------------------------------- #
# Auswertung nach B.5
# --------------------------------------------------------------------------- #


def _evaluate(values: list[float]) -> dict[str, Any]:
    """Berechnet Median und Spanne und wendet die Verwerfungsregel an."""
    if not values:
        return {"median_ms": None, "spread_ms": None, "stable": None, "values_ms": []}
    median = statistics.median(values)
    spread = max(values) - min(values)
    return {
        "median_ms": round(median, 3),
        "spread_ms": round(spread, 3),
        "min_ms": round(min(values), 3),
        "max_ms": round(max(values), 3),
        "stable": bool(spread <= median),
        "values_ms": [round(v, 3) for v in values],
    }


def _reference_system() -> dict[str, str]:
    """Erfasst die identitaetsbestimmenden Eigenschaften nach B.3."""
    return {
        "os": f"{platform.system()} {platform.release()} ({platform.version()})",
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_executable": sys.executable,
        "hostname": platform.node(),
    }


def _git(*args: str) -> str:
    try:
        result = subprocess.run(  # noqa: S603 - festes Kommando, keine Nutzereingabe
            ["git", "--no-optional-locks", *args],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip()
    except OSError:
        return "<git nicht verfuegbar>"


# --------------------------------------------------------------------------- #
# Protokoll
# --------------------------------------------------------------------------- #


def _build_report(cold: dict[str, Any], warm: list[dict[str, Any]]) -> dict[str, Any]:
    warm_pm01 = [run["pm01_total_ms"] for run in warm]
    phase_names = ("INITIALIZE", "LOAD_PLUGINS", "LOAD_RESOURCES", "FINALIZE")
    warm_pm02 = {
        name: _evaluate([run["pm02_phase_ms"].get(name, 0.0) for run in warm])
        for name in phase_names
    }

    activated_all = [run["activated_runtimes"] for run in warm] + [cold["activated_runtimes"]]
    pm03_usable = all(count >= 1 for count in activated_all) and all(
        run["pm03_pipeline_stages_present"] for run in [*warm, cold]
    )

    pm03: dict[str, Any]
    if pm03_usable:
        pm03 = _evaluate([run["pm03_pipeline_sum_ms"] for run in warm])
        pm03["status"] = "GEMESSEN"
        pm03["basis"] = "Summe der Stages PluginDiscoveryStage + PluginSecurityStage + PluginActivationStage"
    else:
        pm03 = {
            "status": "NICHT VERWERTBAR",
            "grund": (
                "Keine Plugin-Runtime hat den Zustand STARTED erreicht oder eine "
                "Pipeline-Stage wurde nicht ausgefuehrt. PM-03 wird nicht als Zahl "
                "ausgewiesen."
            ),
            "activated_runtimes_je_lauf": activated_all,
            "median_ms": None,
            "spread_ms": None,
            "stable": None,
            "values_ms": [],
        }

    return {
        "dokumenttyp": "Technische Vorerhebung — KEINE Baseline-Messreihe",
        "hinweis": (
            "Anhang B.2 verlangt die Erhebung nach Bestaetigung des "
            "Baseline-Zustands. Diese Bestaetigung liegt nicht vor. Ob diese "
            "Werte als Baseline anerkannt werden, entscheidet der neue "
            "Implementation Plan."
        ),
        "erhoben_am": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "bezugszustand": {
            "commit": _git("rev-parse", "HEAD"),
            "branch": _git("rev-parse", "--abbrev-ref", "HEAD"),
            "working_tree_abweichungen": len(
                [
                    line
                    for line in _git("status", "--porcelain").splitlines()
                    if line and not line.startswith("??")
                ]
            ),
        },
        "referenzsystem": _reference_system(),
        "messkonfiguration": {
            "plugin_freigabe": "PluginSecurity.approve('reference')",
            "permission_policy": "wildcard_grants = {events.publish, events.subscribe}",
            "begruendung": (
                "Ohne diese Vorkonfiguration wird das Referenzplugin nicht "
                "zugelassen und PM-03 waere nicht messbar. In jeder Messreihe "
                "identisch zu verwenden (B.4 Bedingung 1)."
            ),
            "ablaufumgebung": "je Lauf ein eigenes temporaeres Verzeichnis mit kopiertem Referenzplugin",
            "ausgeschlossen": "Ressourcenkennzahlen (Speicher, CPU) — B.6",
        },
        "messbedingungen_b4": {
            "1_identische_konfiguration": (
                "erfuellt — identischer Ablauf je Lauf. ABWEICHUNG VON DER "
                "PRODUKTIVKONFIGURATION: nach INITIALIZE und vor LOAD_PLUGINS "
                "wird eine PluginSecurity mit wildcard_grants "
                "{events.publish, events.subscribe} registriert und das "
                "Referenzplugin freigegeben. Ohne diese Freigabe wird das "
                "Referenzplugin nicht aktiviert und PM-03 ist nicht messbar. "
                "Die Werte gelten daher NICHT unter Default-Permission-Policy."
            ),
            "2_keine_fremdlast": "vom Ausfuehrenden zu bestaetigen",
            "3_gleicher_datenbestand": "erfuellt — frisches temporaeres Verzeichnis je Lauf",
            "4_deterministisch": "erfuellt — keine Wartezeiten, keine externen Abhaengigkeiten",
            "5_erst_und_folgeausfuehrung_getrennt": "erfuellt — Cold-Run separat ausgewiesen",
        },
        "wiederholungen_warm": len(warm),
        "messgroessen": {
            "PM-01": {
                **_evaluate(warm_pm01),
                "beschreibung": (
                    "Gesamtdauer der Bootstrap-Ausfuehrung ueber alle vier "
                    "Phasen. Die Dauer der Messkonfiguration ist "
                    "herausgerechnet (siehe zusatzinformation)."
                ),
            },
            "PM-02": {
                name: {**warm_pm02[name], "beschreibung": f"Dauer der Phase {name}"}
                for name in phase_names
            },
            "PM-03": {
                **pm03,
                "beschreibung": "Plugin-Runtime-Pipeline von Discovery bis Activation",
            },
        },
        "cold_run": {
            "pm01_total_ms": round(cold["pm01_total_ms"], 3),
            "pm02_phase_ms": {k: round(v, 3) for k, v in cold["pm02_phase_ms"].items()},
            "pm03_pipeline_sum_ms": round(cold["pm03_pipeline_sum_ms"], 3),
            "activated_runtimes": cold["activated_runtimes"],
            "hinweis": "Nicht mit den Warmlaeufen verrechnet (B.4 Bedingung 5)",
        },
        "stage_details_warm": [
            {k: round(v, 3) for k, v in run["stage_ms"].items()} for run in warm
        ],
        "zusatzinformation": {
            "hinweis": (
                "Vom System selbst erhobene Aktivierungsdauer "
                "(plugin.activation.duration_ms). KEINE B.6-Messgroesse, kein "
                "Ersatz fuer PM-03 — ausschliesslich zur Plausibilisierung."
            ),
            "activation_metric_ms_warm": [
                run.get("activation_metric_ms") for run in warm
            ],
            "activation_metric_ms_cold": cold.get("activation_metric_ms"),
            "measurement_setup_ms_warm": [
                round(run.get("measurement_setup_ms", 0.0), 3) for run in warm
            ],
        },
        "aufraeumen": {
            "alle_temp_verzeichnisse_entfernt": all(
                run.get("temp_dir_removed", False) for run in [cold, *warm]
            ),
            "fehler": [
                {"lauf": idx, "fehler": run["cleanup_error"], "pfad": run.get("temp_dir")}
                for idx, run in enumerate([cold, *warm])
                if run.get("cleanup_error")
            ],
            "hinweis": (
                "Ein Aufraeumfehler beeintraechtigt die Messwerte nicht — sie "
                "sind zu diesem Zeitpunkt bereits vollstaendig erhoben. "
                "Zurueckgebliebene Verzeichnisse sind manuell zu loeschen."
            ),
        },
        "ergebnis": (
            "Vorerhebung durchgefuehrt. Keine Regressionsbewertung — es "
            "existiert keine Vergleichsmessreihe und keine bestaetigte Baseline."
        ),
    }


def _markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    add = lines.append
    add("# JOCHEN X — Technische Vorerhebung der Bootstrap-Laufzeiten")
    add("")
    add("> **KEINE Baseline-Messreihe.** " + report["hinweis"])
    add("")
    add("| Feld | Wert |")
    add("|---|---|")
    add(f"| Erhoben am | {report['erhoben_am']} |")
    add(f"| Commit | `{report['bezugszustand']['commit']}` |")
    add(f"| Branch | {report['bezugszustand']['branch']} |")
    add(f"| Abweichungen am versionierten Bestand | {report['bezugszustand']['working_tree_abweichungen']} |")
    add(f"| Wiederholungen (warm) | {report['wiederholungen_warm']} |")
    add("")
    add("## Referenzsystem (B.3)")
    add("")
    add("| Eigenschaft | Wert |")
    add("|---|---|")
    for key, value in report["referenzsystem"].items():
        add(f"| {key} | {value} |")
    add("")
    add("## Messkonfiguration")
    add("")
    for key, value in report["messkonfiguration"].items():
        add(f"- **{key}**: {value}")
    add("")
    add("## Messbedingungen (B.4)")
    add("")
    for key, value in report["messbedingungen_b4"].items():
        add(f"- **{key}**: {value}")
    add("")
    add("## Messgroessen (B.6) — Kennwerte nach B.5")
    add("")
    pm01 = report["messgroessen"]["PM-01"]
    add("| Messgroesse | Median (ms) | Spanne (ms) | min | max | stabil |")
    add("|---|---|---|---|---|---|")
    add(
        f"| **PM-01** Gesamt | {pm01['median_ms']} | {pm01['spread_ms']} | "
        f"{pm01.get('min_ms')} | {pm01.get('max_ms')} | {pm01['stable']} |"
    )
    for name, data in report["messgroessen"]["PM-02"].items():
        add(
            f"| PM-02 {name} | {data['median_ms']} | {data['spread_ms']} | "
            f"{data.get('min_ms')} | {data.get('max_ms')} | {data['stable']} |"
        )
    pm03 = report["messgroessen"]["PM-03"]
    if pm03.get("status") == "GEMESSEN":
        add(
            f"| **PM-03** Pipeline | {pm03['median_ms']} | {pm03['spread_ms']} | "
            f"{pm03.get('min_ms')} | {pm03.get('max_ms')} | {pm03['stable']} |"
        )
    else:
        add("| **PM-03** Pipeline | — | — | — | — | **NICHT VERWERTBAR** |")
    add("")
    if pm03.get("status") != "GEMESSEN":
        add(f"> **PM-03 nicht verwertbar:** {pm03.get('grund')}")
        add("")
    add("### Einzelwerte (B.9)")
    add("")
    add(f"- PM-01: {pm01['values_ms']}")
    for name, data in report["messgroessen"]["PM-02"].items():
        add(f"- PM-02 {name}: {data['values_ms']}")
    add(f"- PM-03: {pm03.get('values_ms')}")
    add("")
    add("## Cold Run — getrennt gefuehrt (B.4 Bedingung 5)")
    add("")
    cold = report["cold_run"]
    add(f"- PM-01: {cold['pm01_total_ms']} ms")
    add(f"- PM-02: {cold['pm02_phase_ms']}")
    add(f"- PM-03: {cold['pm03_pipeline_sum_ms']} ms")
    add(f"- aktivierte Runtimes: {cold['activated_runtimes']}")
    add("")
    add("## Ergebnis")
    add("")
    add(report["ergebnis"])
    add("")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        required=True,
        metavar="PFAD",
        help="Zielpfad ohne Endung; es entstehen <PFAD>.json und <PFAD>.md",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=5,
        metavar="N",
        help="Anzahl der Warmlaeufe (B.5 verlangt mindestens 5, Vorgabe: 5)",
    )
    args = parser.parse_args(argv)

    if args.repeats < 5:
        print("B.5 verlangt mindestens fuenf Wiederholungen.", file=sys.stderr)
        return 3
    if not REFERENCE_PLUGIN.is_dir():
        print(f"Referenzplugin nicht gefunden: {REFERENCE_PLUGIN}", file=sys.stderr)
        return 3
    if not DEFAULT_CONFIG.is_file():
        print(f"Standardkonfiguration nicht gefunden: {DEFAULT_CONFIG}", file=sys.stderr)
        return 3

    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    print("Cold Run ...", flush=True)
    cold = _run_isolated(0)
    print(
        f"  PM-01 {cold['pm01_total_ms']:.1f} ms | aktivierte Runtimes: "
        f"{cold['activated_runtimes']} | Zustaende: {cold['runtime_states']}",
        flush=True,
    )

    warm: list[dict[str, Any]] = []
    for index in range(args.repeats):
        run = _run_isolated(index + 1)
        warm.append(run)
        print(
            f"Warm {index + 1}/{args.repeats}: PM-01 {run['pm01_total_ms']:.1f} ms | "
            f"Runtimes {run['activated_runtimes']}",
            flush=True,
        )

    report = _build_report(cold, warm)

    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    json_path = target.with_suffix(".json")
    md_path = target.with_suffix(".md")
    json_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    md_path.write_text(_markdown(report), encoding="utf-8")

    print("")
    print(f"Protokoll geschrieben: {json_path}")
    print(f"Protokoll geschrieben: {md_path}")
    pm03 = report["messgroessen"]["PM-03"]
    if pm03.get("status") != "GEMESSEN":
        print("")
        print("ACHTUNG: PM-03 ist NICHT VERWERTBAR - keine aktivierte Runtime.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
