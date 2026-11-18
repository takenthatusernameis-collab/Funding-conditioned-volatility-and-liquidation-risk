#!/usr/bin/env python3
"""FCLR-LIQ-RISK-CALIBRATION-06 — multi-month modeled breach labels (stdlib, read-only cache).

Campaign: FCLR-LIQ-RISK-CALIBRATION-06-20261118T182600Z
Session:  session_20261118T182813Z

Emits, all non-empty, in the session dir:
  - fclr_risk06_labels_<UTC>.json  (multi-month modeled breach labels + per-scenario counts)
  - fclr_risk06_labels_<UTC>.md

Label semantics: synthetic_modeled_boundary_breach; observed_liquidation_labels=false.
Stdlib only: math/json/zipfile/datetime/pathlib. No network, no parquet, no sealed months.
"""
from __future__ import annotations

import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
SESSION_DIR = RS / "session_20261118T182813Z"
UTC_STAMP = "20261118T182813Z"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]
LABEL_MONTHS = ["2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09"]
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
    rows = []
    for ym in LABEL_MONTHS:
        y, m = ym.split("-")
        for d in range(1, 32):
            day = f"{y}-{int(m):02d}-{d:02d}"
            try:
                datetime.strptime(day, "%Y-%m-%d")
            except ValueError:
                continue
            lines = read_mark_lines(symbol, ym, day)
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
    rows = []          # compact: [sym_idx, entry_ts, lev, side_idx, horizon, breached, hours(-1), clearance]
    for sym_idx, symbol in enumerate(SYMBOLS):
        marks = load_mark_series(symbol)
        n = len(marks)
        scen = {}
        for lev in LEVERAGES:
            for side in SIDES:
                for horizon in HORIZONS:
                    scen[(lev, side, horizon)] = {
                        "n_origins": 0, "n_breached": 0,
                        "hours_to_breach": [], "min_clearance": None,
                    }
        for i in range(0, n - MAX_H):
            p0 = marks[i][1]
            if p0 <= 0:
                continue
            entry_ts = marks[i][0]
            for lev in LEVERAGES:
                long_b, short_b = boundary_prices(p0, lev)
                for side_idx, side in enumerate(SIDES):
                    b = long_b if side == "long" else short_b
                    for horizon in HORIZONS:
                        path = [marks[i + k][1] for k in range(1, horizon + 1)]
                        if side == "long":
                            extreme = min(path)
                            clearance = (extreme - b) / p0
                        else:
                            extreme = max(path)
                            clearance = (b - extreme) / p0
                        breached = clearance <= 0.0
                        hours_to_breach = -1
                        if breached:
                            for k in range(1, horizon + 1):
                                px = marks[i + k][1]
                                if (side == "long" and px <= b) or (side == "short" and px >= b):
                                    hours_to_breach = k
                                    break
                        s = scen[(lev, side, horizon)]
                        s["n_origins"] += 1
                        if s["min_clearance"] is None or clearance < s["min_clearance"]:
                            s["min_clearance"] = clearance
                        if breached:
                            s["n_breached"] += 1
                            s["hours_to_breach"].append(hours_to_breach)
                        rows.append([sym_idx, entry_ts, lev, side_idx, horizon,
                                     1 if breached else 0, hours_to_breach, clearance])
        stat = {"n_bars": n, "n_entries": max(0, n - MAX_H), "scenarios": {}}
        for (lev, side, horizon), s in scen.items():
            n_o = s["n_origins"]
            hb = s["hours_to_breach"]
            stat["scenarios"][f"L{lev}|{side}|H{horizon}"] = {
                "n_origins": n_o,
                "n_breached": s["n_breached"],
                "breach_rate": (s["n_breached"] / n_o) if n_o else None,
                "mean_hours_to_breach": (sum(hb) / len(hb)) if hb else None,
                "min_clearance": s["min_clearance"],
            }
        per_instrument[symbol] = stat
    return per_instrument, rows


def aggregate(per_instrument):
    by_scen = {}
    for lev in LEVERAGES:
        for side in SIDES:
            for horizon in HORIZONS:
                n_o = 0
                n_b = 0
                for symbol in SYMBOLS:
                    sc = per_instrument[symbol]["scenarios"][f"L{lev}|{side}|H{horizon}"]
                    n_o += sc["n_origins"]
                    n_b += sc["n_breached"]
                by_scen[f"L{lev}|{side}|H{horizon}"] = {
                    "n_origins": n_o,
                    "n_breached": n_b,
                    "breach_rate": (n_b / n_o) if n_o else None,
                }
    return by_scen


def aggregate_by_month(rows):
    out = {}
    for r in rows:
        sym_idx, entry_ts, lev, side_idx, horizon, breached = r[0], r[1], r[2], r[3], r[4], r[5]
        month = datetime.fromtimestamp(entry_ts / 1000, tz=timezone.utc).strftime("%Y-%m")
        key = f"{month}|L{lev}|{SIDES[side_idx]}|H{horizon}"
        s = out.setdefault(key, {"n": 0, "breached": 0})
        s["n"] += 1
        s["breached"] += breached
    for k, s in out.items():
        s["breach_rate"] = (s["breached"] / s["n"]) if s["n"] else None
    return dict(sorted(out.items()))


def main():
    per_instrument, rows = build_labels()
    agg = aggregate(per_instrument)
    n_total = len(rows)
    n_breach = sum(r[5] for r in rows)
    payload = {
        "schema": "fclr_risk06_labels",
        "campaign": "FCLR-LIQ-RISK-CALIBRATION-06-20261118T182600Z",
        "session": f"session_{UTC_STAMP}",
        "timestamp_utc": UTC_STAMP,
        "track": "B_modeled_boundary_breach",
        "label_type": "synthetic_modeled_boundary_breach",
        "observed_liquidation_labels": False,
        "network_used": False,
        "parquet_used": False,
        "numpy_used": False,
        "label": "EXPLORATORY_PILOT",
        "label_months": LABEL_MONTHS,
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
            "Does not reconstruct account-specific liquidation engines, portfolio margin, insurance-fund behavior, or forced-liquidation records.",
            "Never call these observed liquidations.",
        ],
        "row_schema": ["symbol_idx", "entry_open_time_ms", "leverage", "side_idx(0=long,1=short)",
                       "horizon_hours", "breached(0/1)", "hours_to_breach(-1 if none)", "clearance_ratio"],
        "n_rows": n_total,
        "n_breached_rows": n_breach,
        "overall_breach_rate": (n_breach / n_total) if n_total else None,
        "per_instrument": per_instrument,
        "aggregate_by_scenario": agg,
        "aggregate_by_month_scenario": aggregate_by_month(rows),
        "rows": rows,
    }
    (SESSION_DIR / f"fclr_risk06_labels_{UTC_STAMP}.json").write_text(
        json.dumps(payload, separators=(",", ":"), default=None), encoding="utf-8")

    md = [
        "# FCLR-LIQ-RISK-CALIBRATION-06 — Multi-Month Modeled Breach Labels",
        "",
        f"**Session:** `session_{UTC_STAMP}`",
        f"**Campaign:** `FCLR-LIQ-RISK-CALIBRATION-06-20261118T182600Z`",
        "**Label type:** `synthetic_modeled_boundary_breach` — **observed_liquidation_labels=false**.",
        "**Stdlib only** (no numpy/pandas/scipy); no network; no parquet; no sealed months.",
        "",
        "## Design",
        f"- Label months: {', '.join(LABEL_MONTHS)}; instruments: {', '.join(SYMBOLS)}",
        f"- L ∈ {{{', '.join(str(x) for x in LEVERAGES)}}}, side ∈ {{{', '.join(SIDES)}}}, H ∈ {{{', '.join(str(x) for x in HORIZONS)}}}h, mmr={MMR}",
        "- Entry at close of bar t; hourly mark path t+1..t+H.",
        "",
        "## Per-scenario breach counts (all instruments x all months)",
        "",
        "| Scenario | n_origins | n_breached | breach_rate |",
        "|---|---|---|---|",
    ]
    for key, s in agg.items():
        md.append(f"| {key} | {s['n_origins']} | {s['n_breached']} | {s['breach_rate']} |")
    md += [
        "",
        f"**Total rows:** {n_total}; **breached rows:** {n_breach}; **overall breach rate:** {payload['overall_breach_rate']}",
        "",
        "## Honest status",
        "- EXPLORATORY/PILOT. Synthetic modeled boundary breaches only; not observed liquidations.",
        "- No account-specific liquidation engine, portfolio margin, insurance fund, or forced-liquidation records reconstructed.",
    ]
    (SESSION_DIR / f"fclr_risk06_labels_{UTC_STAMP}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({"n_rows": n_total, "n_breached": n_breach,
                      "overall_breach_rate": payload["overall_breach_rate"],
                      "primary_scenario": agg["L10|long|H24"]}, indent=2))


if __name__ == "__main__":
    main()
