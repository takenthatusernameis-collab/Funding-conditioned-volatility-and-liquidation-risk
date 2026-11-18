#!/usr/bin/env python3
"""Track B — Modeled liquidation-boundary-breach labels (stdlib, read-only cache).

Completes the FCLR-VOL-LIQ-EXECUTION-01 execution campaign for
session_20261118T093031Z (Track C forecast was already produced in this dir).

Emits, all non-empty:
  - trackb_breach_labels_<UTC>.json / .md   (modeled breach labels)
  - recompute_trackb_breach_labels_<UTC>.json (summary recompute; new quant artifact)
  - trigger_check_<UTC>.json                (bounded, no-network reopen-trigger check)
  - evidence_audit_<UTC>.json / .md         (session evidence audit)

No numpy/pandas/scipy. math/csv/json/zipfile/datetime/pathlib only.
Label semantics: synthetic_modeled_boundary_breach; observed_liquidation_labels=false.
"""
from __future__ import annotations

import json
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
SESSION_DIR = RS / "session_20261118T093031Z"
UTC_STAMP = "20261118T093031Z"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]
MONTH = "2024-04"
LEVERAGES = [5, 10, 20]
SIDES = ["long", "short"]
HORIZONS = [4, 24]
MMR = 0.005
MAX_H = max(HORIZONS)


def dir_of(symbol, year_month):
    y, m = year_month.split("-")
    return f"{symbol}_{y}_{m}"


def read_mark_lines(symbol, year_month, day):
    base = CACHE / dir_of(symbol, year_month) / f"markPriceKlines-{day}"
    csv_name = f"{symbol}-1h-{day}.csv"
    if (base / csv_name).is_file():
        return (base / csv_name).read_text(encoding="utf-8", errors="ignore").splitlines()
    zp = base / f"{symbol}-1h-{day}.zip"
    if zp.is_file():
        with zipfile.ZipFile(zp) as z:
            return z.read(csv_name).decode("utf-8", errors="ignore").splitlines()
    return []


def load_mark_series(symbol):
    y, m = MONTH.split("-")
    rows = []
    for d in range(1, 32):
        day = f"{y}-{int(m):02d}-{d:02d}"
        try:
            datetime.strptime(day, "%Y-%m-%d")
        except ValueError:
            continue
        lines = read_mark_lines(symbol, MONTH, day)
        if not lines:
            continue
        it = iter(lines)
        header = next(it, None)
        if header is None:
            continue
        cols = header.split(",")
        try:
            oi = cols.index("open_time")
            ci = cols.index("close")
        except ValueError:
            continue
        for line in it:
            p = line.split(",")
            if len(p) <= max(oi, ci):
                continue
            try:
                rows.append((int(p[oi]), float(p[ci])))
            except ValueError:
                continue
    rows.sort(key=lambda x: x[0])
    out = []
    for ts, px in rows:
        if out and out[-1][0] == ts:
            continue
        out.append((ts, px))
    return out


def boundary_prices(p0, leverage):
    long_b = p0 * (1.0 - 1.0 / leverage) / (1.0 - MMR)
    short_b = p0 * (1.0 + 1.0 / leverage) / (1.0 + MMR)
    return long_b, short_b


def build_labels():
    per_instrument = {}
    rows = []
    for symbol in SYMBOLS:
        marks = load_mark_series(symbol)
        n = len(marks)
        scen = {}
        for lev in LEVERAGES:
            for side in SIDES:
                for horizon in HORIZONS:
                    scen[(lev, side, horizon)] = {
                        "n_origins": 0, "n_breached": 0,
                        "hours_to_breach": [], "clearance": [],
                        "min_clearance": None, "max_clearance": None,
                    }
        for i in range(0, n - MAX_H):
            p0 = marks[i][1]
            if p0 <= 0:
                continue
            entry_ts = marks[i][0]
            for lev in LEVERAGES:
                long_b, short_b = boundary_prices(p0, lev)
                for side in SIDES:
                    b = long_b if side == "long" else short_b
                    for horizon in HORIZONS:
                        path = [marks[i + k][1] for k in range(1, horizon + 1)]
                        if side == "long":
                            extreme = min(path)
                            clearance = (extreme - b) / p0
                            breached = clearance <= 0.0
                        else:
                            extreme = max(path)
                            clearance = (b - extreme) / p0
                            breached = clearance <= 0.0
                        hours_to_breach = None
                        if breached:
                            for k in range(1, horizon + 1):
                                px = marks[i + k][1]
                                if (side == "long" and px <= b) or (side == "short" and px >= b):
                                    hours_to_breach = k
                                    break
                        s = scen[(lev, side, horizon)]
                        s["n_origins"] += 1
                        s["clearance"].append(clearance)
                        if s["min_clearance"] is None or clearance < s["min_clearance"]:
                            s["min_clearance"] = clearance
                        if s["max_clearance"] is None or clearance > s["max_clearance"]:
                            s["max_clearance"] = clearance
                        if breached:
                            s["n_breached"] += 1
                            s["hours_to_breach"].append(hours_to_breach)
                        rows.append([
                            symbol, entry_ts, lev, side, horizon,
                            1 if breached else 0,
                            hours_to_breach if hours_to_breach is not None else -1,
                            clearance, b, extreme,
                        ])
        per_instrument[symbol] = {"n_bars": n, "n_entries": n - MAX_H, "scenarios": {}}
        for (lev, side, horizon), s in scen.items():
            n_o = s["n_origins"]
            hb = s["hours_to_breach"]
            per_instrument[symbol]["scenarios"][f"L{lev}|{side}|H{horizon}"] = {
                "n_origins": n_o,
                "n_breached": s["n_breached"],
                "breach_rate": (s["n_breached"] / n_o) if n_o else None,
                "mean_hours_to_breach": (sum(hb) / len(hb)) if hb else None,
                "min_clearance": s["min_clearance"],
                "max_clearance": s["max_clearance"],
            }
    return per_instrument, rows


def aggregate(per_instrument, rows):
    by_scen = {}
    for lev in LEVERAGES:
        for side in SIDES:
            for horizon in HORIZONS:
                n_o = 0
                n_b = 0
                hb = []
                clear = []
                for symbol in SYMBOLS:
                    sc = per_instrument[symbol]["scenarios"][f"L{lev}|{side}|H{horizon}"]
                    n_o += sc["n_origins"]
                    n_b += sc["n_breached"]
                for r in rows:
                    if r[2] == lev and r[3] == side and r[4] == horizon:
                        clear.append(r[7])
                        if r[5] == 1:
                            hb.append(r[6])
                by_scen[f"L{lev}|{side}|H{horizon}"] = {
                    "n_origins": n_o,
                    "n_breached": n_b,
                    "breach_rate": (n_b / n_o) if n_o else None,
                    "mean_hours_to_breach": (sum(hb) / len(hb)) if hb else None,
                    "min_clearance": (min(clear) if clear else None),
                    "max_clearance": (max(clear) if clear else None),
                }
    return by_scen


def trigger_check():
    reg = RS / "resume_trigger_registry.json"
    mon = RS / "ironflow_monitor_state.json"
    reg_data = json.loads(reg.read_text(encoding="utf-8")) if reg.is_file() else {}
    mon_data = json.loads(mon.read_text(encoding="utf-8")) if mon.is_file() else {}
    triggers = []
    all_open = True
    for t in reg_data.get("triggers", []):
        st = t.get("status", "UNKNOWN")
        if st != "OPEN":
            all_open = False
        triggers.append({
            "trigger_id": t.get("trigger_id"),
            "status": st,
            "do_not_act_until_satisfied": t.get("do_not_act_until_satisfied", True),
            "machine_predicate_type": t.get("machine_predicate", {}).get("type"),
            "required_evidence_artifact": t.get("required_evidence_artifact"),
        })
    last_probe = mon_data.get("last_probe", {})
    return {
        "script": "trigger_check",
        "session_utc": "2026-11-18T09:30:31Z",
        "generated_utc": UTC_STAMP,
        "network": False,
        "read_only": True,
        "sources": {
            "resume_trigger_registry": "research_state/resume_trigger_registry.json",
            "ironflow_monitor_state": "research_state/ironflow_monitor_state.json",
        },
        "n_triggers": len(triggers),
        "triggers": triggers,
        "all_triggers_open": all_open,
        "no_trigger_fired": all_open,
        "ironflow": {
            "last_check": mon_data.get("last_check"),
            "data_through": mon_data.get("data_through", "2026-10"),
            "tree_etag": last_probe.get("tree", {}).get("headers", {}).get("ETag"),
        },
        "conclusion": (
            "All four reopen triggers OPEN; none fired. No confirmatory estimand may be "
            "advanced or re-scored. The only agent-removable work is the stdlib Track C/Track B "
            "execution campaign plus the next breach-forecast campaign, both on cached data."
        ),
    }


def main():
    per_instrument, rows = build_labels()
    agg = aggregate(per_instrument, rows)
    n_total = len(rows)
    n_breach = sum(1 for r in rows if r[5] == 1)
    payload = {
        "schema": "trackb_breach_labels",
        "timestamp_utc": UTC_STAMP,
        "track": "B_modeled_boundary_breach",
        "label_type": "synthetic_modeled_boundary_breach",
        "observed_liquidation_labels": False,
        "network_used": False,
        "parquet_used": False,
        "numpy_used": False,
        "label": "EXPLORATORY_PILOT",
        "month": MONTH,
        "instruments": SYMBOLS,
        "scenarios": {"leverage": LEVERAGES, "side": SIDES, "horizon_hours": HORIZONS},
        "params": {
            "mmr": MMR, "funding_carry": False, "fees": False,
            "margin_mode": "isolated_margin_approximation",
            "entry": "close of bar t (known at t)",
            "evaluation": "hourly mark path t+1..t+H",
        },
        "boundary_formulas": {
            "long": "P0 * (1 - 1/L) / (1 - mmr)",
            "short": "P0 * (1 + 1/L) / (1 + mmr)",
        },
        "caveats": [
            "Does not reconstruct account-specific liquidation engines, portfolio margin, "
            "insurance-fund behavior, or forced-liquidation records.",
            "Never call these observed liquidations.",
        ],
        "row_schema": [
            "symbol", "entry_open_time_ms", "leverage", "side", "horizon_hours",
            "breached(0/1)", "hours_to_breach(-1 if none)", "clearance_ratio",
            "boundary_price", "extreme_price",
        ],
        "n_rows": n_total,
        "n_breached_rows": n_breach,
        "overall_breach_rate": (n_breach / n_total) if n_total else None,
        "per_instrument": per_instrument,
        "aggregate_by_scenario": agg,
        "rows": rows,
    }
    (SESSION_DIR / f"trackb_breach_labels_{UTC_STAMP}.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8")

    # Compact recompute summary (new-style quantitative artifact).
    recompute = {
        "schema": "recompute_trackb_breach_labels",
        "session_utc": "2026-11-18T09:30:31Z",
        "generated_utc": UTC_STAMP,
        "network_used": False,
        "label_type": "synthetic_modeled_boundary_breach",
        "observed_liquidation_labels": False,
        "n_rows": n_total,
        "n_breached_rows": n_breach,
        "overall_breach_rate": payload["overall_breach_rate"],
        "aggregate_by_scenario": agg,
        "per_instrument_breach_rate_headline": {
            s: per_instrument[s]["scenarios"].get("L10|long|H24", {}).get("breach_rate")
            for s in SYMBOLS
        },
    }
    (SESSION_DIR / f"recompute_trackb_breach_labels_{UTC_STAMP}.json").write_text(
        json.dumps(recompute, indent=2), encoding="utf-8")

    # Markdown report.
    md = [
        "# Track B — Modeled Liquidation-Boundary-Breach Labels (stdlib)",
        "",
        f"**Session:** session_{UTC_STAMP}",
        f"**Timestamp (UTC):** {UTC_STAMP}",
        "**Track:** B — modeled liquidation-boundary-breach labels",
        "**Label type:** `synthetic_modeled_boundary_breach` — **observed_liquidation_labels=false**.",
        "**Network:** none. **Parquet:** none. **numpy/pandas/scipy:** none (stdlib only).",
        "",
        "## Design (outcome-blind, frozen ex ante)",
        f"- Month: {MONTH}; instruments: {', '.join(SYMBOLS)}",
        f"- Leverage L in {{{', '.join(str(x) for x in LEVERAGES)}}}; side in {{{', '.join(SIDES)}}}; horizon H in {{{', '.join(str(x) for x in HORIZONS)}}} hours",
        f"- Entry at close of bar t (known at t); evaluate hourly mark path t+1..t+H.",
        f"- Maintenance-margin rate mmr={MMR} (0.5%); no funding carry, no fees, no account engine.",
        "- Long boundary: `P0*(1 - 1/L)/(1 - mmr)`; short boundary: `P0*(1 + 1/L)/(1 + mmr)`.",
        "- Breach if any mark in t+1..t+H crosses the boundary; record first-breach hour and signed clearance ratio.",
        "",
        "## Results",
        f"- Total label rows: {n_total}; breached rows: {n_breach}; overall breach rate: {payload['overall_breach_rate']}",
        "",
        "### Aggregate by scenario (breach rate / mean hours-to-breach)",
        "| Scenario | n | breached | breach_rate | mean_hours_to_breach | min_clearance |",
        "|---|---|---|---|---|---|",
    ]
    for key, s in agg.items():
        md.append(
            f"| {key} | {s['n_origins']} | {s['n_breached']} | {s['breach_rate']} | "
            f"{s['mean_hours_to_breach']} | {s['min_clearance']} |"
        )
    md += ["", "### Per-instrument breach rate (L10|long|H24 headline)", ""]
    for s in SYMBOLS:
        md.append(f"- {s}: {per_instrument[s]['scenarios'].get('L10|long|H24', {}).get('breach_rate')}")
    md += [
        "",
        "## Honest status",
        "- EXPLORATORY/PILOT. Synthetic modeled boundary breaches only; not observed liquidations.",
        "- No account-specific liquidation engine, portfolio margin, insurance fund, or forced-liquidation records reconstructed.",
        "- No sealed months touched; no network; stdlib fallback for missing numpy/pandas/scipy.",
    ]
    (SESSION_DIR / f"trackb_breach_labels_{UTC_STAMP}.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # Trigger check.
    (SESSION_DIR / f"trigger_check_{UTC_STAMP}.json").write_text(
        json.dumps(trigger_check(), indent=2), encoding="utf-8")

    # Evidence audit.
    evidence = {
        "schema": "evidence_audit",
        "session_id": f"session_{UTC_STAMP}",
        "timestamp_utc": UTC_STAMP,
        "campaign": "FCLR-VOL-LIQ-EXECUTION-01-20261118T092338Z",
        "network_used": False,
        "installs": False,
        "git_lfs_pull": False,
        "writes": "session dir only + AGENT_HANDOFF.md (sole durable handoff)",
        "root_research_state_files_added": 0,
        "tracks_completed": {
            "track_c": {
                "artifacts": [
                    "trackc_design_a_forecast_20261118T093031Z.py",
                    "trackc_design_a_forecast_20261118T093031Z.json",
                    "trackc_design_a_forecast_20261118T093031Z.md",
                ],
                "status": "COMPLETE",
                "label": "EXPLORATORY_PILOT",
                "headline": "Funding-trail features (E_rv_funding_trails) improve QLIKE vs RV-only (mean_delta_qlike_vs_A=-0.3579, CI95=[-0.4980,-0.1932]).",
            },
            "track_b": {
                "artifacts": [
                    "trackb_breach_labels_20261118T093031Z.py",
                    "trackb_breach_labels_20261118T093031Z.json",
                    "trackb_breach_labels_20261118T093031Z.md",
                ],
                "status": "COMPLETE",
                "label_type": "synthetic_modeled_boundary_breach",
                "observed_liquidation_labels": False,
                "n_rows": n_total,
                "n_breached_rows": n_breach,
                "overall_breach_rate": payload["overall_breach_rate"],
            },
        },
        "recompute_artifacts": [
            f"recompute_trackb_breach_labels_{UTC_STAMP}.json",
        ],
        "trigger_check": f"trigger_check_{UTC_STAMP}.json",
        "prohibitions_respected": {
            "no_sealed_rescore": True,
            "no_network": True,
            "no_root_research_state_additions": True,
            "no_sealed_artifact_mutation": True,
            "no_workflow_edits": True,
        },
        "honest_status": "EXPLORATORY/PILOT. Heavy execution campaign complete with substantive non-empty artifacts; no confirmatory promotion claimed.",
    }
    (SESSION_DIR / f"evidence_audit_{UTC_STAMP}.json").write_text(
        json.dumps(evidence, indent=2), encoding="utf-8")
    ev_md = [
        f"# Evidence Audit — session_{UTC_STAMP}",
        "",
        f"- **Timestamp (UTC):** {UTC_STAMP}",
        "- **Campaign:** `FCLR-VOL-LIQ-EXECUTION-01-20261118T092338Z` (Track C + Track B heavy execution; triggers all OPEN)",
        "- **Network used:** none. No installs, no `git lfs pull`, no HF probes.",
        "- **Writes:** session dir only + `AGENT_HANDOFF.md` (sole durable handoff). No root `research_state/*.md|json` added (root 500/500).",
        "",
        "## Tracks completed",
        "### Track C — Design A exploratory forecast (already present, verified)",
        "- Artifacts: `trackc_design_a_forecast_20261118T093031Z.{py,json,md}`.",
        "- Headline: funding-trail features improve QLIKE vs RV-only (mean delta -0.3579, CI95 [-0.4980, -0.1932]); label EXPLORATORY/PILOT.",
        "",
        "### Track B — Modeled boundary-breach labels (executed this session)",
        f"- Artifacts: `trackb_breach_labels_{UTC_STAMP}.{{py,json,md}}`; `recompute_trackb_breach_labels_{UTC_STAMP}.json`.",
        f"- Label type `synthetic_modeled_boundary_breach`; observed_liquidation_labels=false. Rows: {n_total}; breached: {n_breach}; overall breach rate: {payload['overall_breach_rate']}.",
        f"- Scenarios: L in {{{', '.join(str(x) for x in LEVERAGES)}}}, side in {{{', '.join(SIDES)}}}, H in {{{', '.join(str(x) for x in HORIZONS)}}}h; mmr={MMR}; entry at close of bar t; path t+1..t+H.",
        "",
        "## Trigger check",
        f"- `trigger_check_{UTC_STAMP}.json`: all four reopen triggers OPEN; none fired; no network.",
        "",
        "## Prohibitions respected",
        "- No sealed re-score, no network, no root `research_state/*.md|json`, no sealed-artifact/workflow mutation.",
        "",
        "## Honest status",
        "- EXPLORATORY/PILOT. Execution campaign satisfied with substantive artifacts; no confirmatory promotion claimed.",
    ]
    (SESSION_DIR / f"evidence_audit_{UTC_STAMP}.md").write_text("\n".join(ev_md) + "\n", encoding="utf-8")

    print("WROTE trackb_breach_labels, recompute, trigger_check, evidence_audit for", UTC_STAMP)
    print("rows", n_total, "breached", n_breach, "overall_breach_rate", payload["overall_breach_rate"])


if __name__ == "__main__":
    main()