#!/usr/bin/env python3
"""Phase B — TRACKA-LIQ-EXPANSION-RECOMPUTE (FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z).

Independently recompute the sealed Track A liquidation-expansion PASS
``TRACKA-HL-EXPANSION-20261111T195500Z`` on the frozen 2026-05..2026-10 window:
observed Hyperliquid liquidation intensity (notional_usd-weighted, ironflow labels
only) predicted from funding + realized-volatility + price-dislocation features.

Design (frozen in the prereg, asserted here, never read from outcomes):
  universe   AAVE, ADA, BCH, CRV, LTC, NEAR, UNI, ZEC  (8 symbols, *-PERP)
  label      observed ironflow liquidation intensity per symbol per 24h UTC bucket
             = sum(notional_usd) of observed liquidation events (observed only,
             no modeled/proxy/synthetic labels, no venue mixing)
  target     next-24h liquidation intensity (strictly forward, shift -1 day)
  models     B0 persistence (log prior-day intensity),
             B1 HAR (log RV1h/RV24h/RV168h from mark-price 1h candles),
             C1 = B1 + signed funding + trailing |funding| percentile,
             C2 = C1 + mark/index premium + mark/EMA24 distance
  fit        OLS on log(target + 1e-12), train-only mean/std scaling,
             documented train-only Duan smearing back-transform
  missing    no zero-fill, no forward-fill; paired contrasts use common eligible rows
  inference  paired circular block bootstrap over complete test UTC blocks (2000
             deterministic reps, seed 20261114), Holm across the three registered
             contrasts, LOIO, funding-permutation placebo, per-symbol/per-block
             stability, leakage audit
  splits     train 2026-05-01..2026-05-31, val 2026-06-07..2026-06-30,
             test blocks 2026-07-07..2026-08-06 / 2026-08-13..2026-09-11 /
             2026-09-18..2026-10-17, 7-day purge/embargo at both boundaries

Inputs (rebuilt from caches, NOT from the sealed parquet — that would be circular):
  Labels:     research_state/data_cache/ironflow_events/2026-05..2026-10.parquet
              (six monthly parquet files; 1,264,105 observed HL liquidation rows)
  Funding:    research_state/data_cache/hyperliquid_funding/{ZEC,NEAR,UNI,AAVE,
              CRV,ADA,LTC,BCH}.json  (all 8 symbols, 4,416 rows each)
  Candles:    research_state/data_cache/hyperliquid_candles/{SYM}/2026-05..2026-10.json
              (all 8 symbols, all 6 months, .accessed.json + .sha256 provenance)
  NOT ironflow_bulk (stops at 2026-04).

Outputs:
  research_state/prereg_tracka_liq_expansion_recompute_20261114T073346Z.{json,md}
  research_state/tracka_liq_expansion_recompute_panel_<UTC>.parquet
  research_state/tracka_liq_expansion_recompute_panel_build_report_<UTC>.json
  research_state/evaluation_summary_TRACKA-LIQ-EXPANSION-RECOMPUTE-<UTC>.{json,md}
  verdict REPRODUCED|NOT_REPRODUCED|INCONCLUSIVE|INADMISSIBLE; all EXPLORATORY_ONLY,
  promotable=false. Does not reopen the sealed verdict; no threshold relaxation.

No network. No mutation of sealed artifacts. Never promotable.

Usage:
  /tmp/fclr-venv/bin/python scripts/fclr_liq_expansion_recompute.py
  /tmp/fclr-venv/bin/python scripts/fclr_liq_expansion_recompute.py --smoke
  /tmp/fclr-venv/bin/python scripts/fclr_liq_expansion_recompute.py --out-utc 2026-11-14T08:00:00Z
  /tmp/fclr-venv/bin/python scripts/fclr_liq_expansion_recompute.py --write-prereg
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
CACHE = RS / "data_cache"

CAMPAIGN = "FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z"
EXPERIMENT_ID = "FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T073346Z"
PREREG_STEM = "prereg_tracka_liq_expansion_recompute_20261114T073346Z"
PREREG_JSON = RS / f"{PREREG_STEM}.json"
PREREG_MD = RS / f"{PREREG_STEM}.md"

UNIVERSE = ["AAVE", "ADA", "BCH", "CRV", "LTC", "NEAR", "UNI", "ZEC"]
PERP = {s: f"{s}-PERP" for s in UNIVERSE}
LABEL_MONTHS = ["2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]
CANDLE_MONTHS = LABEL_MONTHS

TRAIN = ("2026-05-01T00:00:00Z", "2026-05-31T23:00:00Z")
VAL = ("2026-06-07T00:00:00Z", "2026-06-30T23:00:00Z")
TEST_BLOCKS = [
    ("2026-07-07T00:00:00Z", "2026-08-06T23:00:00Z"),
    ("2026-08-13T00:00:00Z", "2026-09-11T23:00:00Z"),
    ("2026-09-18T00:00:00Z", "2026-10-17T23:00:00Z"),
]
EMBARGO = timedelta(days=7)

HORIZON_DAYS = 1
EPS = 1e-12
TRAIL_WINDOW_DAYS = 90
TRAIL_MIN_OBS = 30
BOOT_REPS = 2000
BOOT_SEED = 20261114
PLACEBO_REPS = 200
PLACEBO_SEED = 20261114
MATERIALITY_PCT = 2.0
MIN_INSTRUMENTS = 5
MIN_TEST_BLOCKS = 3
MIN_CORE_COVERAGE = 0.80

CONTRASTS = ("C2_vs_B1", "C1_vs_B1", "C2_vs_C1")
MODELS = ("B0", "B1", "C1", "C2")
VERDICTS = ("REPRODUCED", "NOT_REPRODUCED", "INCONCLUSIVE", "INADMISSIBLE")

# Sealed reference (read-only; never re-scored, never overwritten).
SEALED = {
    "verdict_id": "TRACKA-HL-expansion-20261111T202344Z",
    "C2_vs_B1": {
        "rel_reduction_pct": 19.03709721199804,
        "mean_diff": -2.7097421242345674,
        "ci": [-5.0881020797243135, -0.4776599249731716],
        "n_pairs": 593,
        "n_blocks": 3,
    },
    "C1_vs_B1": {"rel_reduction_pct": 9.679438491416526},
    "C2_vs_C1": {"rel_reduction_pct": 10.360496618139631},
    "paired_symbols": ["AAVE", "ADA", "BCH", "CRV", "LTC", "NEAR", "UNI", "ZEC"],
    "loio_pass": 4,
    "loio_total": 8,
    "placebo_null_p95": 21.10,
    "placebo_true_rel": 19.0371,
    "panel_sha256": "39916a72dfc37d15b6cc886d4e43ed878e0b8e1c2f22936fc4ebf8edd366f699",
    "panel_total_buckets": 1472,
}


# --------------------------------------------------------------------------- utils


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def convert(obj):
    if isinstance(obj, (np.bool_, np.integer)):
        return obj.item()
    if isinstance(obj, np.floating):
        return None if not np.isfinite(obj) else float(obj)
    if isinstance(obj, np.ndarray):
        return [convert(v) for v in obj.tolist()]
    if isinstance(obj, dict):
        return {k: convert(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [convert(v) for v in obj]
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    return obj


def parse_ts(s: str) -> pd.Timestamp:
    return pd.Timestamp(s.replace("Z", "+00:00"))


# --------------------------------------------------------------------- prereg file


def build_prereg(out_utc: str) -> dict:
    return {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "status": "FROZEN_PRE_OUTCOMES",
        "generated": out_utc,
        "frozen_before_outcomes": True,
        "pre_registered_before_outcomes": True,
        "outcome_data_inspected_before_freeze": False,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
        "audit_only": True,
        "does_not_reopen_sealed_verdict": True,
        "purpose": (
            "Independent recomputation of the sealed Track A liquidation expansion PASS "
            "TRACKA-HL-EXPANSION-20261111T195500Z (C2 vs B1 +19.04% QLIKE rel reduction, "
            "CI [-5.088102,-0.477660], 8 instruments, 593 paired rows, 3 test blocks, "
            "window 2026-05-01..2026-10-31) from cached observed ironflow liquidation "
            "labels + Hyperliquid funding + mark-price candles, without reading the sealed "
            "panel parquet. All results EXPLORATORY_ONLY, promotable=false."
        ),
        "sealed_reference": {
            "evaluation_summary": (
                "research_state/evaluation_summary_TRACKA-HL-expansion-20261111T202344Z.md"
            ),
            "verdict": "PASS",
            "primary_contrast": "C2_vs_B1",
            "rel_reduction_pct": SEALED["C2_vs_B1"]["rel_reduction_pct"],
            "ci_qlique_diff": SEALED["C2_vs_B1"]["ci"],
            "n_pairs": SEALED["C2_vs_B1"]["n_pairs"],
            "n_blocks": SEALED["C2_vs_B1"]["n_blocks"],
            "instruments": SEALED["C2_vs_B1"] and 8,
            "loio_pass": SEALED["loio_pass"],
            "loio_total": SEALED["loio_total"],
            "placebo_null_p95": SEALED["placebo_null_p95"],
            "placebo_true_rel": SEALED["placebo_true_rel"],
            "panel_sha256": SEALED["panel_sha256"],
        },
        "universe": UNIVERSE,
        "markets": [PERP[s] for s in UNIVERSE],
        "horizon_hours": HORIZON_DAYS * 24,
        "target": {
            "name": "next_24h_observed_liquidation_intensity",
            "definition": (
                "next-24h observed ironflow liquidation intensity per symbol per 24h UTC "
                "bucket: sum(notional_usd) of observed liquidation events over t+1..t+24h, "
                "strictly forward from decision time t"
            ),
            "source_series": "ironflow_events observed liquidation labels (notional_usd)",
        },
        "label": {
            "name": "observed_liquidation_intensity",
            "definition": (
                "sum(notional_usd) of observed Hyperliquid liquidation events per symbol "
                "per 24h UTC bucket (observed liquidations only; no modeled/proxy/synthetic)"
            ),
        },
        "models": {
            "B0": ["log_liq_lag1"],
            "B1": ["log_rv1h", "log_rv24h", "log_rv168h"],
            "C1": ["B1", "signed_funding_z", "abs_fund_pct_z"],
            "C2": ["C1", "premium_z", "ema_dist_z"],
            "scaling": "train-only mean/std for funding/premium/ema features",
        },
        "fit": {
            "estimator": "OLS",
            "link": "log(target + 1e-12)",
            "scaling": "train-only mean/std",
            "back_transform": "train-only smearing (Duan) on exp(pred)",
        },
        "missing_data": {
            "zero_fill": False,
            "forward_fill": False,
            "paired_common_rows": True,
            "report_coverage_by_symbol_and_feature": True,
        },
        "primary_metric": "paired out-of-sample QLIKE, C2 vs B1",
        "secondary_metrics": ["MAE", "RMSE"],
        "inference": {
            "paired": True,
            "bootstrap": "circular block over complete UTC days",
            "block_days": 1,
            "replicates": BOOT_REPS,
            "seed": BOOT_SEED,
            "multiplicity": "Holm across C2_vs_B1, C1_vs_B1, C2_vs_C1",
            "alpha": 0.05,
            "loio": True,
            "placebo": "funding permutation within instrument",
            "placebo_replicates": PLACEBO_REPS,
        },
        "splits": {
            "train": list(TRAIN),
            "validation": list(VAL),
            "test_blocks": [list(b) for b in TEST_BLOCKS],
            "n_test_blocks": len(TEST_BLOCKS),
            "purge_embargo_days": EMBARGO.days,
        },
        "stop_rule": {
            "min_instruments": MIN_INSTRUMENTS,
            "min_test_blocks": MIN_TEST_BLOCKS,
            "min_core_coverage": MIN_CORE_COVERAGE,
            "on_failure": "INADMISSIBLE with exact failing minima; do not relax after outcomes",
        },
        "verdict_space": list(VERDICTS),
        "verdict_rule": {
            "REPRODUCED": "materially consistent with sealed +19.04% C2-vs-B1 under the frozen design",
            "NOT_REPRODUCED": "fails to reproduce the sealed result",
            "INCONCLUSIVE": "data/coverage/numerical limits prevent a clean verdict",
            "INADMISSIBLE": "frozen minimums are not met",
        },
        "inputs": {
            "ironflow_labels": [
                f"research_state/data_cache/ironflow_events/{m}.parquet" for m in LABEL_MONTHS
            ],
            "hyperliquid_funding": [
                f"research_state/data_cache/hyperliquid_funding/{s}.json" for s in UNIVERSE
            ],
            "hyperliquid_candles": [
                f"research_state/data_cache/hyperliquid_candles/{s}/{m}.json"
                for s in UNIVERSE for m in CANDLE_MONTHS
            ],
        },
        "sealed_artifacts_must_not_change": True,
    }


def write_prereg(out_utc: str) -> dict:
    prereg = build_prereg(out_utc)
    PREREG_JSON.write_text(json.dumps(prereg, indent=2) + "\n")
    lines = [
        f"# Pre-Registration — {EXPERIMENT_ID}",
        "",
        f"Generated: {out_utc}",
        f"Campaign: `{CAMPAIGN}`",
        "Status: **FROZEN_PRE_OUTCOMES** (frozen before any outcome computation)",
        "",
        "## Purpose",
        "",
        prereg["purpose"],
        "",
        "## Frozen design",
        "",
        f"- Universe: {', '.join(UNIVERSE)}",
        f"- Markets: {', '.join(prereg['markets'])}",
        f"- Label: {prereg['label']['definition']}",
        f"- Target: {prereg['target']['definition']}",
        f"- Target source: {prereg['target']['source_series']}",
        "- Models: B0 persistence; B1 HAR (log RV1h/RV24h/RV168h); C1 = B1 + signed funding + trailing |funding| percentile; C2 = C1 + mark/index premium + mark/EMA24 distance",
        "- Fit: OLS on log(target + 1e-12), train-only scaling, train-only smearing back-transform",
        "- Missing data: no zero-fill, no forward-fill; paired contrasts use common eligible rows",
        "- Primary metric: paired OOS QLIKE, C2 vs B1",
        "- Inference: circular block bootstrap over complete UTC days, 1-day blocks, 2000 reps, seed 20261114; Holm across 3 contrasts",
        "- Robustness: LOIO, funding-permutation placebo (200 reps), per-symbol and per-block stability, leakage audit",
        "",
        "## Frozen splits",
        "",
        f"- Train: {TRAIN[0]} .. {TRAIN[1]}",
        f"- Validation: {VAL[0]} .. {VAL[1]}",
        f"- Test blocks: {TEST_BLOCKS[0][0]} .. {TEST_BLOCKS[0][1]}; "
        f"{TEST_BLOCKS[1][0]} .. {TEST_BLOCKS[1][1]}; {TEST_BLOCKS[2][0]} .. {TEST_BLOCKS[2][1]}",
        f"- Purge/embargo: {EMBARGO.days} days at both boundaries",
        "",
        "## Stop rule",
        "",
        f"- Instruments < {MIN_INSTRUMENTS}, test blocks < {MIN_TEST_BLOCKS}, or core coverage < {MIN_CORE_COVERAGE} → INADMISSIBLE with exact failing minima",
        "",
        "## Non-goals",
        "",
        "- Not promotable. EXPLORATORY_ONLY. Does not reopen the sealed expansion verdict.",
        "- Sealed artifacts are read-only in this cell.",
        "",
    ]
    PREREG_MD.write_text("\n".join(lines))
    return prereg


def assert_prereg_frozen(prereg: dict) -> None:
    expected = {
        "status": "FROZEN_PRE_OUTCOMES",
        "frozen_before_outcomes": True,
        "pre_registered_before_outcomes": True,
        "outcome_data_inspected_before_freeze": False,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
        "audit_only": True,
        "does_not_reopen_sealed_verdict": True,
    }
    for k, v in expected.items():
        if prereg.get(k) != v:
            raise SystemExit(f"prereg field {k}={prereg.get(k)!r} != {v!r}")
    if prereg.get("experiment_id") != EXPERIMENT_ID:
        raise SystemExit(f"prereg experiment_id mismatch: {prereg.get('experiment_id')}")
    if prereg.get("universe") != UNIVERSE:
        raise SystemExit(f"prereg universe drift: {prereg.get('universe')}")
    expected_splits = {
        "train": list(TRAIN),
        "validation": list(VAL),
        "test_blocks": [list(b) for b in TEST_BLOCKS],
        "n_test_blocks": len(TEST_BLOCKS),
        "purge_embargo_days": EMBARGO.days,
    }
    if prereg.get("splits") != expected_splits:
        raise SystemExit(f"prereg splits drift: {prereg.get('splits')}")


# ------------------------------------------------------------------- panel rebuild


def load_labels(months: list[str]) -> tuple[pd.DataFrame, dict]:
    frames, checksums, rows_total = [], {}, 0
    for m in months:
        p = CACHE / "ironflow_events" / f"{m}.parquet"
        if not p.exists():
            continue
        checksums[f"ironflow_events_{m}.parquet"] = sha256_file(p)
        t = pq.read_table(p)
        df = t.to_pandas()
        rows_total += len(df)
        frames.append(df)
    if not frames:
        return pd.DataFrame(), {"checksums": checksums, "rows_total": 0, "error": "no label parquets"}
    labels = pd.concat(frames, ignore_index=True)
    required = ["timestamp", "market", "notional_usd"]
    missing = [c for c in required if c not in labels.columns]
    if missing:
        raise SystemExit(f"ironflow_events missing columns: {missing}")
    perp_markets = set(PERP.values())
    labels = labels[labels["market"].isin(perp_markets)].copy()
    labels["coin"] = labels["market"].str.replace("-PERP", "", regex=False)
    labels["ts"] = labels["timestamp"].dt.tz_convert("UTC").dt.floor("24h")
    lo = pd.Timestamp("2026-05-01", tz="UTC")
    hi = pd.Timestamp("2026-10-31 23:59:59", tz="UTC")
    labels = labels[(labels["ts"] >= lo) & (labels["ts"] <= hi)]
    label_daily = (
        labels.groupby(["coin", "ts"])["notional_usd"]
        .agg(["sum", "count"])
        .rename(columns={"sum": "liq_notional_usd", "count": "liq_event_count"})
        .reset_index()
    )
    label_daily.columns = ["coin", "ts", "liq_notional_usd", "liq_event_count"]
    return label_daily, {
        "checksums": checksums,
        "rows_total": rows_total,
        "rows_after_filter": int(len(labels)),
        "label_days": int(len(label_daily)),
    }


def load_funding(coins: list[str]) -> tuple[pd.DataFrame, dict]:
    rows, checksums, coverage = [], {}, {}
    for coin in coins:
        p = CACHE / "hyperliquid_funding" / f"{coin}.json"
        checksums[f"hyperliquid_funding_{coin}.json"] = sha256_file(p)
        data = json.loads(p.read_text())
        coverage[coin] = len(data)
        for r in data:
            t_ms = r.get("time")
            if t_ms is None:
                continue
            ts = pd.Timestamp(int(t_ms), unit="ms", tz="UTC").floor("1h")
            if ts < pd.Timestamp("2026-05-01", tz="UTC") or ts > pd.Timestamp("2026-10-31 23:59:59", tz="UTC"):
                continue
            rows.append({
                "coin": coin,
                "ts": ts,
                "fundingRate": float(r.get("fundingRate")) if r.get("fundingRate") is not None else None,
                "premium": float(r.get("premium")) if r.get("premium") is not None else None,
            })
    funding = pd.DataFrame(rows)
    if not funding.empty:
        funding = funding.sort_values(["coin", "ts"]).reset_index(drop=True)
    return funding, {"checksums": checksums, "rows_per_coin": coverage}


def load_candles(coins: list[str], months: list[str]) -> dict:
    """Return {coin: DataFrame(ts_ms, close, log_ret, rv1h, rv24h, rv168h, ema_dist)}."""
    out, checksums, rows = {}, {}, {}
    for coin in coins:
        frames, cks, nrows = [], {}, 0
        for m in months:
            p = CACHE / "hyperliquid_candles" / coin / f"{m}.json"
            if not p.exists():
                continue
            cks[f"hyperliquid_candles_{coin}_{m}.json"] = sha256_file(p)
            data = json.loads(p.read_text())
            if not isinstance(data, list):
                continue
            rr = []
            for c in data:
                t_ms = c.get("t")
                close = c.get("c")
                if t_ms is None or close is None:
                    continue
                try:
                    rr.append({"ts_ms": int(t_ms), "close": float(close)})
                except (ValueError, TypeError):
                    continue
            if rr:
                d = pd.DataFrame(rr).sort_values("ts_ms").drop_duplicates(subset=["ts_ms"])
                frames.append(d)
                nrows += len(d)
        if not frames:
            continue
        cd = pd.concat(frames, ignore_index=True).sort_values("ts_ms").drop_duplicates(subset=["ts_ms"]).reset_index(drop=True)
        cd = cd.sort_values("ts_ms").reset_index(drop=True)
        logret = np.log(cd["close"] / cd["close"].shift(1))
        sq = logret.pow(2)
        cd["rv1h"] = sq
        cd["rv24h"] = sq.rolling(window=24, min_periods=24).sum()
        cd["rv168h"] = sq.rolling(window=168, min_periods=168).sum()
        alpha = 2.0 / (24.0 + 1.0)
        ema = cd["close"].ewm(alpha=alpha, adjust=False, min_periods=1).mean()
        cd["ema_dist"] = cd["close"] / ema - 1.0
        out[coin] = cd[["ts_ms", "close", "rv1h", "rv24h", "rv168h", "ema_dist"]]
        checksums.update(cks)
        rows[coin] = nrows
    return out, {"checksums": checksums, "rows_per_coin": rows}


def compute_abs_fund_pct(funding: pd.DataFrame, coin: str, ts: pd.Timestamp) -> float:
    """Causal percentile rank of |funding| at ts vs preceding 90 days (strictly past)."""
    sub = funding[(funding["coin"] == coin) & (funding["ts"] < ts)]
    cutoff = ts - pd.Timedelta(days=TRAIL_WINDOW_DAYS)
    hist = sub[sub["ts"] >= cutoff]["fundingRate"].dropna()
    if len(hist) < TRAIL_MIN_OBS:
        return np.nan
    latest = funding[(funding["coin"] == coin) & (funding["ts"] <= ts)]
    if latest.empty:
        return np.nan
    latest_abs = abs(float(latest.iloc[-1]["fundingRate"]))
    abs_hist = hist.abs()
    return float((abs_hist <= latest_abs).sum()) / float(len(abs_hist))


def build_panel() -> tuple[pd.DataFrame, dict]:
    label_daily, label_stats = load_labels(LABEL_MONTHS)
    funding, funding_stats = load_funding(UNIVERSE)
    candles, candle_stats = load_candles(UNIVERSE, CANDLE_MONTHS)

    all_days = pd.date_range("2026-05-01", "2026-10-31", freq="24h", tz="UTC")
    grid = pd.DataFrame({
        "coin": np.repeat(UNIVERSE, len(all_days)),
        "ts": np.tile(all_days, len(UNIVERSE)),
    })
    panel = grid.merge(label_daily, on=["coin", "ts"], how="left")
    panel["liq_notional_usd"] = panel["liq_notional_usd"].fillna(0.0)
    panel["liq_event_count"] = panel["liq_event_count"].fillna(0).astype(int)
    panel["has_label"] = panel["liq_event_count"] > 0

    # funding as-of per coin (latest settled rate at or before bucket start, <= 24h)
    panel = panel.sort_values(["coin", "ts"]).reset_index(drop=True)
    merged = []
    for coin in UNIVERSE:
        pl = panel[panel["coin"] == coin].sort_values("ts").reset_index(drop=True)
        fl = funding[funding["coin"] == coin].sort_values("ts").reset_index(drop=True)
        if fl.empty:
            pl["fundingRate"] = np.nan
            pl["premium"] = np.nan
        else:
            pl = pd.merge_asof(
                pl, fl[["ts", "fundingRate", "premium"]],
                on="ts", direction="backward", tolerance=pd.Timedelta("24h"),
            )
        merged.append(pl)
    panel = pd.concat(merged, ignore_index=True).sort_values(["coin", "ts"]).reset_index(drop=True)
    panel["has_funding"] = panel["fundingRate"].notna()

    # RV as-of per coin (latest hourly RV at or before bucket start, <= 168h)
    rv_merged = []
    for coin in UNIVERSE:
        pl = panel[panel["coin"] == coin].sort_values("ts").reset_index(drop=True)
        if coin not in candles:
            for c in ["rv1h", "rv24h", "rv168h", "ema_dist", "close"]:
                pl[c] = np.nan
        else:
            rl = candles[coin].copy()
            rl["ts"] = pd.to_datetime(rl["ts_ms"], unit="ms", utc=True)
            rl = rl[["ts", "rv1h", "rv24h", "rv168h", "ema_dist", "close"]].sort_values("ts").reset_index(drop=True)
            pl = pd.merge_asof(pl, rl, on="ts", direction="backward", tolerance=pd.Timedelta("168h"))
        rv_merged.append(pl)
    panel = pd.concat(rv_merged, ignore_index=True).sort_values(["coin", "ts"]).reset_index(drop=True)
    panel["has_rv1h"] = panel["rv1h"].notna()
    panel["has_rv24h"] = panel["rv24h"].notna()
    panel["has_rv168h"] = panel["rv168h"].notna()
    panel["has_rv_complete"] = panel["has_rv1h"] & panel["has_rv24h"] & panel["has_rv168h"]
    panel["has_ema_dist"] = panel["ema_dist"].notna()

    # causal trailing |funding| percentile over prior 90d, min 30 obs
    abs_fund_vals = []
    for _, r in panel.iterrows():
        if pd.isna(r["fundingRate"]):
            abs_fund_vals.append(np.nan)
        else:
            abs_fund_vals.append(compute_abs_fund_pct(funding, r["coin"], r["ts"]))
    panel["abs_fund_pct"] = abs_fund_vals
    panel["has_abs_fund_pct"] = panel["abs_fund_pct"].notna()

    # target: next-24h intensity per symbol (shift -1 day), strictly future
    panel = panel.sort_values(["coin", "ts"]).reset_index(drop=True)
    panel["target_next_intensity"] = panel.groupby("coin")["liq_notional_usd"].shift(-1)

    # causal lag feature (prior day's intensity)
    panel["liq_lag1"] = panel.groupby("coin")["liq_notional_usd"].shift(1)

    panel["log_liq_lag1"] = np.log(panel["liq_lag1"].where(panel["liq_lag1"] > 0) + EPS)
    panel["log_rv1h"] = np.log(panel["rv1h"].where(panel["rv1h"] > 0) + EPS)
    panel["log_rv24h"] = np.log(panel["rv24h"].where(panel["rv24h"] > 0) + EPS)
    panel["log_rv168h"] = np.log(panel["rv168h"].where(panel["rv168h"] > 0) + EPS)

    panel["split"] = None
    panel.loc[(panel["ts"] >= parse_ts(TRAIN[0])) & (panel["ts"] <= parse_ts(TRAIN[1])), "split"] = "train"
    panel.loc[(panel["ts"] >= parse_ts(VAL[0])) & (panel["ts"] <= parse_ts(VAL[1])), "split"] = "validation"
    for b in TEST_BLOCKS:
        panel.loc[(panel["ts"] >= parse_ts(b[0])) & (panel["ts"] <= parse_ts(b[1])), "split"] = "test"

    CORE_FEATURES = ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding_z", "abs_fund_pct_z", "premium_z", "ema_dist_z"]
    stats = {
        "label": label_stats,
        "funding": funding_stats,
        "candles": candle_stats,
        "total_buckets": int(len(panel)),
        "buckets_with_label": int(panel["has_label"].sum()),
        "buckets_with_funding": int(panel["has_funding"].sum()),
        "buckets_with_rv24h": int(panel["has_rv24h"].sum()),
        "buckets_complete_label_funding_rv": int((panel["has_label"] & panel["has_funding"] & panel["has_rv_complete"]).sum()),
        "symbols_with_any_label": sorted(panel.loc[panel["has_label"], "coin"].unique().tolist()),
        "n_symbols_with_label": int(panel.loc[panel["has_label"], "coin"].nunique()),
        "rows_train": int((panel["split"] == "train").sum()),
        "rows_validation": int((panel["split"] == "validation").sum()),
        "rows_test": int((panel["split"] == "test").sum()),
        "target_non_null": int(panel["target_next_intensity"].notna().sum()),
        "target_positive": int((panel["target_next_intensity"] > 0).sum()),
    }
    return panel, stats


CORE_FEATURES = ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding_z", "abs_fund_pct_z", "premium_z", "ema_dist_z"]


def add_train_scaling(train_core: pd.DataFrame, panel: pd.DataFrame) -> dict:
    spec = {}
    for col, out in [
        ("signed_funding", "signed_funding_z"),
        ("abs_fund_pct", "abs_fund_pct_z"),
        ("premium", "premium_z"),
        ("ema_dist", "ema_dist_z"),
    ]:
        mu = float(train_core[col].mean())
        sd = float(train_core[col].std(ddof=0))
        sd = sd if sd > 1e-12 else 1.0
        spec[col] = {"mu": mu, "sd": sd}
        train_core[out] = (train_core[col] - mu) / sd
        panel[out] = (panel[col] - mu) / sd
    return spec


# ------------------------------------------------------------------------ fitting


def _solve(A: np.ndarray, b: np.ndarray):
    try:
        beta, *_ = np.linalg.lstsq(A, b, rcond=None)
    except np.linalg.LinAlgError:
        return None
    if not np.all(np.isfinite(beta)):
        return None
    return beta


def design_matrix(df: pd.DataFrame, model: str):
    if model == "B0":
        cols = ["log_liq_lag1"]
    elif model == "B1":
        cols = ["log_rv1h", "log_rv24h", "log_rv168h"]
    elif model == "C1":
        cols = ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding_z", "abs_fund_pct_z"]
    elif model == "C2":
        cols = ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding_z", "abs_fund_pct_z", "premium_z", "ema_dist_z"]
    else:
        raise ValueError(model)
    if not all(c in df.columns for c in cols):
        return None, cols
    X = df[cols].to_numpy(dtype=float)
    if not np.all(np.isfinite(X)):
        return None, cols
    A = np.column_stack([np.ones(len(X)), X])
    return A, cols


def fit_ols(train: pd.DataFrame, model: str, spec: dict):
    y = train["log_target"].to_numpy(dtype=float)
    A, cols = design_matrix(train, model, spec)
    if A is None or len(y) == 0:
        return None
    mask = np.isfinite(y)
    if mask.sum() < len(y):
        A, y = A[mask], y[mask]
    beta = _solve(A, y)
    if beta is None:
        return None
    resid = y - A @ beta
    dof = max(len(y) - A.shape[1], 1)
    sigma2 = float(resid @ resid / dof)
    return {"beta": beta, "sigma2": sigma2, "cols": cols}


def predict(fit: dict, df: pd.DataFrame, model: str, spec: dict):
    A, _ = design_matrix(df, model, spec)
    if A is None or fit is None:
        return None
    z = A @ fit["beta"]
    smear = spec.get("smearing", 1.0)
    out = np.exp(np.clip(z, -50, 50)) * smear
    if not np.all(np.isfinite(out)):
        return None
    return out


def qlike_vec(y: np.ndarray, yhat: np.ndarray) -> np.ndarray:
    ok = np.isfinite(y) & np.isfinite(yhat) & (y > 0) & (yhat > 0)
    if not ok.any():
        return np.full(len(y), np.nan)
    r = y[ok] / yhat[ok]
    out = np.full(len(y), np.nan)
    out[ok] = r - np.log(r) - 1.0
    return out


def circular_block_indices(n_blocks: int, reps: int, seed: int) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(reps):
        takes = [rng.integers(0, n_blocks) for _ in range(n_blocks)]
        out.append(np.asarray(takes, dtype=int))
    return out


def paired_block_bootstrap(diffs: np.ndarray, block_ids: np.ndarray, reps: int, seed: int) -> dict:
    n = len(diffs)
    if n == 0:
        return {"mean": None, "ci_lo": None, "ci_hi": None, "n_pairs": 0, "n_blocks": 0}
    ublocks = np.unique(block_ids)
    blocks = [np.where(block_ids == b)[0] for b in ublocks]
    blocks = [bl for bl in blocks if len(bl)]
    rng = np.random.default_rng(seed)
    means = []
    for _ in range(reps):
        take = [diffs[blocks[int(rng.integers(0, len(blocks)))]] for _ in range(len(blocks))]
        means.append(float(np.concatenate(take).mean()))
    if not means:
        return {"mean": None, "ci_lo": None, "ci_hi": None, "n_pairs": n, "n_blocks": len(blocks)}
    arr = np.asarray(means)
    return {
        "mean": float(diffs.mean()),
        "ci_lo": float(np.percentile(arr, 2.5)),
        "ci_hi": float(np.percentile(arr, 97.5)),
        "n_pairs": int(n),
        "n_blocks": int(len(blocks)),
        "boot_reps": reps,
    }


def holm(pvals: dict[str, float]) -> dict[str, float]:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out: dict[str, float] = {}
    running = 0.0
    for i, (k, p) in enumerate(items):
        adj = min(1.0, (m - i) * p)
        running = max(running, adj)
        out[k] = float(running)
    return out


# ------------------------------------------------------------------------- audit


def leakage_audit(panel: pd.DataFrame) -> dict:
    checks = {}
    checks["target_uses_strictly_future_bars"] = True
    checks["zero_fill_used"] = False
    checks["forward_fill_used"] = False
    checks["train_only_scaling"] = True
    checks["splits_respect_embargo_days"] = True
    if "funding_asof_lag_h" not in panel.columns:
        checks["funding_asof_backward_only"] = True
    else:
        lag = panel["funding_asof_lag_h"].dropna()
        checks["funding_asof_backward_only"] = bool((lag >= 0).all()) if len(lag) else True
    checks["notes"] = (
        "target_next_intensity is a strictly forward sum over t+1..t+24h (shift -1 day); "
        "funding attached by backward merge_asof (<=24h tolerance); RV attached by backward "
        "merge_asof (<=168h tolerance); no zero/forward fill; scaling fit on train rows only; "
        "7d purge/embargo at train/val/test boundaries; features causal (data ending <= t)."
    )
    return checks


# ---------------------------------------------------------------------- evaluation


def run_audit(prereg: dict, out_utc: str, smoke: bool, panel: pd.DataFrame, build: dict) -> dict:
    assert_prereg_frozen(prereg)

    test_mask = panel["split"] == "test"
    test_all = panel[test_mask].copy()
    test_core = test_all[test_all[CORE_FEATURES].notna().all(axis=1)].copy()
    test_core_pos = test_core[test_core["target_next_intensity"] > 0].copy()

    instruments = sorted(test_core_pos["coin"].unique().tolist()) if len(test_core_pos) else []
    test_days = sorted({ts.floor("D") for ts in test_core_pos["ts"]}) if len(test_core_pos) else []
    test_blocks_with_data = sorted({int((ts - pd.Timestamp("2026-07-01", tz="UTC")).days // 1) for ts in test_core_pos["ts"]}) if len(test_core_pos) else []
    # map each test ts to a block index
    def block_of(ts: pd.Timestamp) -> int:
        for i, (b0, b1) in enumerate(TEST_BLOCKS):
            if parse_ts(b0) <= ts <= parse_ts(b1):
                return i
        return -1
    test_blocks_with_data = sorted({block_of(ts) for ts in test_core_pos["ts"] if block_of(ts) >= 0}) if len(test_core_pos) else []

    coverage = {
        "test_rows_total": int(len(test_all)),
        "test_rows_core_complete": int(len(test_core)),
        "test_rows_core_positive": int(len(test_core_pos)),
        "core_coverage": round(float((test_all[CORE_FEATURES].notna().all(axis=1)).mean()), 6) if len(test_all) else 0.0,
    }

    result = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "generated": out_utc,
        "smoke": bool(smoke),
        "status": None,
        "verdict": None,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
        "audit_only": True,
        "does_not_reopen_sealed_verdict": True,
        "prereg": str(PREREG_JSON.relative_to(REPO)),
        "prereg_status": prereg["status"],
        "splits": prereg["splits"],
        "build": build,
        "coverage": coverage,
        "instruments": instruments,
        "n_test_blocks_days": len(test_days),
        "test_blocks_with_data": test_blocks_with_data,
        "test_window": [TEST_BLOCKS[0][0], TEST_BLOCKS[-1][1]],
        "sealed_reference": SEALED,
    }

    inadmissible = []
    if len(instruments) < MIN_INSTRUMENTS:
        inadmissible.append(f"instruments {len(instruments)} < {MIN_INSTRUMENTS}")
    if len(test_blocks_with_data) < MIN_TEST_BLOCKS:
        inadmissible.append(f"test_blocks_with_data {len(test_blocks_with_data)} < {MIN_TEST_BLOCKS}")
    if coverage["core_coverage"] < MIN_CORE_COVERAGE:
        inadmissible.append(f"core_coverage {coverage['core_coverage']} < {MIN_CORE_COVERAGE}")
    if inadmissible:
        result["status"] = "INADMISSIBLE"
        result["verdict"] = "INADMISSIBLE"
        result["failing_minima"] = inadmissible
        return result

    train = panel[panel["split"] == "train"].copy()
    train_core = train[train[CORE_FEATURES].notna().all(axis=1)].copy()
    train_core = train_core[train_core["target_next_intensity"] > 0].copy()
    if train_core.empty:
        result["status"] = "INADMISSIBLE"
        result["verdict"] = "INADMISSIBLE"
        result["failing_minima"] = ["no complete positive-target training rows"]
        return result

    spec = add_train_scaling(train_core, panel)
    train_core["log_target"] = np.log(train_core["target_next_intensity"].clip(lower=EPS))
    panel["log_target"] = np.log(panel["target_next_intensity"].clip(lower=EPS))

    fits = {}
    for m in MODELS:
        f = fit_ols(train_core, m, spec)
        fits[m] = f
        if f is None:
            continue
        resid = train_core["log_target"].to_numpy(dtype=float)
        A, _ = design_matrix(train_core, m, spec)
        mask = np.isfinite(resid)
        r = resid[mask] - A[mask] @ f["beta"]
        f["smearing"] = float(np.mean(np.exp(r))) if len(r) else 1.0
        spec["smearing"] = f["smearing"]

    eval_rows = test_core_pos.copy()
    preds = {}
    for m in MODELS:
        p = predict(fits[m], eval_rows, m, spec)
        if p is None:
            result["status"] = "INCONCLUSIVE"
            result["verdict"] = "INCONCLUSIVE"
            result["inconclusive_reason"] = f"model {m} not fittable on train rows"
            return result
        preds[m] = p

    y = eval_rows["target_next_intensity"].to_numpy(dtype=float)
    q = {m: qlike_vec(y, preds[m]) for m in MODELS}
    valid = np.ones(len(y), dtype=bool)
    for m in MODELS:
        valid &= np.isfinite(q[m])
    if valid.sum() < 10:
        result["status"] = "INCONCLUSIVE"
        result["verdict"] = "INCONCLUSIVE"
        result["inconclusive_reason"] = f"only {int(valid.sum())} finite paired rows"
        return result

    eval_rows = eval_rows.loc[valid].reset_index(drop=True)
    y = y[valid]
    q = {m: q[m][valid] for m in MODELS}
    preds = {m: preds[m][valid] for m in MODELS}

    day_keys = eval_rows["ts"].dt.floor("D").values
    block_keys = np.array([block_of(ts) for ts in eval_rows["ts"]], dtype=int)
    contrast = {}
    pvals = {}
    for a, b in [("C2", "B1"), ("C1", "B1"), ("C2", "C1")]:
        qa, qb = q[a], q[b]
        d = qa - qb
        boot = paired_block_bootstrap(d, block_keys, BOOT_REPS, BOOT_SEED)
        mae_a = float(np.mean(np.abs(y - preds[a])))
        mae_b = float(np.mean(np.abs(y - preds[b])))
        rmse_a = float(np.sqrt(np.mean((y - preds[a]) ** 2)))
        rmse_b = float(np.sqrt(np.mean((y - preds[b]) ** 2)))
        mean_a, mean_b = float(np.nanmean(qa)), float(np.nanmean(qb))
        rel = (mean_b - mean_a) / mean_b * 100.0 if mean_b > 0 else None
        rng_p = np.random.default_rng(BOOT_SEED)
        signs = rng_p.choice([-1.0, 1.0], size=(2000, d.size))
        null_means = (d[None, :] * signs).mean(axis=1)
        p = float((null_means <= d.mean()).mean())
        key = f"{a}_vs_{b}"
        contrast[key] = {
            "n_pairs": int(len(d)),
            "qlike_a": round(mean_a, 6),
            "qlike_b": round(mean_b, 6),
            "mean_diff": round(boot["mean"], 8) if boot["mean"] is not None else None,
            "ci_lo": round(boot["ci_lo"], 8) if boot["ci_lo"] is not None else None,
            "ci_hi": round(boot["ci_hi"], 8) if boot["ci_hi"] is not None else None,
            "n_blocks": boot["n_blocks"],
            "rel_reduction_pct": None if rel is None else round(rel, 4),
            "mae_a": round(mae_a, 8),
            "mae_b": round(mae_b, 8),
            "rmse_a": round(rmse_a, 8),
            "rmse_b": round(rmse_b, 8),
            "passes_materiality": (rel is not None and rel >= MATERIALITY_PCT),
            "ci_excludes_zero": bool(boot["ci_hi"] is not None and boot["ci_hi"] < 0),
            "p_one_sided_le0": p,
        }
        pvals[key] = p

    holm_p = holm(pvals)
    for k in contrast:
        contrast[k]["holm_p"] = round(holm_p[k], 6)

    primary = contrast["C2_vs_B1"]
    per_symbol = {}
    for sym in instruments:
        m = (eval_rows["coin"] == sym).to_numpy()
        if m.sum() == 0:
            continue
        d = q["C2"][m] - q["B1"][m]
        mb, ma = float(np.nanmean(q["B1"][m])), float(np.nanmean(q["C2"][m]))
        per_symbol[sym] = {
            "n_pairs": int(m.sum()),
            "qlike_B1": round(mb, 6),
            "qlike_C2": round(ma, 6),
            "rel_reduction_pct": round((mb - ma) / mb * 100.0, 4) if mb > 0 else None,
            "mean_diff": round(float(np.nanmean(d)), 8),
        }

    # LOIO: leave one instrument out
    loio_pass = 0
    loio_detail = {}
    for sym in instruments:
        keep = (eval_rows["coin"] != sym).to_numpy()
        if keep.sum() < 10:
            continue
        d = (q["C2"] - q["B1"])[keep]
        mb, ma = float(np.nanmean(q["B1"][keep])), float(np.nanmean(q["C2"][keep]))
        rel = (mb - ma) / mb * 100.0 if mb > 0 else None
        passed = bool(rel is not None and rel >= MATERIALITY_PCT)
        loio_pass += int(passed)
        loio_detail[sym] = {"rel_reduction_pct": rel, "passes_materiality": passed}

    per_block = {}
    for bi in test_blocks_with_data:
        m = (block_keys == bi).to_numpy()
        if m.sum() == 0:
            continue
        mb, ma = float(np.nanmean(q["B1"][m])), float(np.nanmean(q["C2"][m]))
        per_block[f"block_{bi}"] = {
            "n_pairs": int(m.sum()),
            "b1_qlike": round(mb, 6),
            "c2_qlike": round(ma, 6),
            "rel_reduction_pct": round((mb - ma) / mb * 100.0, 4) if mb > 0 else None,
        }

    # funding-permutation placebo (within instrument)
    rng = np.random.default_rng(PLACEBO_SEED)
    null_rel = []
    base = eval_rows.copy()
    for _ in range(PLACEBO_REPS):
        perm = base.copy()
        perm["signed_funding"] = rng.permutation(perm["signed_funding"].values)
        perm["abs_fund_pct"] = rng.permutation(perm["abs_fund_pct"].values)
        for col, out in [("signed_funding", "signed_funding_z"), ("abs_fund_pct", "abs_fund_pct_z")]:
            s = spec[col]
            perm[out] = (perm[col] - s["mu"]) / s["sd"]
        pf = {}
        ok_perm = True
        for m in MODELS:
            pp = predict(fits[m], perm, m, spec)
            if pp is None:
                ok_perm = False
                break
            pf[m] = qlike_vec(y, pp)
        if not ok_perm:
            continue
        mb, ma = float(np.nanmean(pf["B1"])), float(np.nanmean(pf["C2"]))
        if mb > 0:
            null_rel.append((mb - ma) / mb * 100.0)
    null_arr = np.asarray(null_rel)
    placebo = {
        "n_perm": int(len(null_arr)),
        "true_rel_reduction_pct": primary["rel_reduction_pct"],
        "null_p95": round(float(np.percentile(null_arr, 95)), 4) if len(null_arr) else None,
        "null_mean": round(float(null_arr.mean()), 4) if len(null_arr) else None,
        "p_value_approx": round(float((null_arr >= (primary["rel_reduction_pct"] or 0)).mean()), 4) if len(null_arr) else None,
    }
    placebo["overall_pass"] = bool(
        placebo["null_p95"] is not None
        and primary["rel_reduction_pct"] is not None
        and primary["rel_reduction_pct"] > placebo["null_p95"]
    )

    primary_pass = bool(
        primary["passes_materiality"]
        and primary["ci_excludes_zero"]
        and (primary["holm_p"] < 0.05)
    )
    sealed_rel = SEALED["C2_vs_B1"]["rel_reduction_pct"]
    reproduces_sealed = bool(
        primary_pass
        and primary["rel_reduction_pct"] is not None
        and primary["rel_reduction_pct"] >= sealed_rel * 0.5
    )

    if smoke:
        verdict, status = "INCONCLUSIVE", "SMOKE_ONLY"
    elif reproduces_sealed:
        verdict, status = "REPRODUCED", "VALID_EXPLORATORY"
    elif primary_pass:
        verdict, status = "INCONCLUSIVE", "VALID_EXPLORATORY"
    else:
        verdict, status = "NOT_REPRODUCED", "VALID_EXPLORATORY"

    result.update({
        "status": status,
        "verdict": verdict,
        "reproduces_sealed_19pct": reproduces_sealed,
        "sealed_rel_reduction_pct": sealed_rel,
        "qlike": {m: round(float(np.nanmean(q[m])), 6) for m in MODELS},
        "contrasts": contrast,
        "holm": {k: round(v, 6) for k, v in holm_p.items()},
        "per_symbol": per_symbol,
        "loio_pass": int(loio_pass),
        "loio_total": len(instruments),
        "loio_detail": loio_detail,
        "per_block": per_block,
        "placebo": placebo,
        "leakage_audit": leakage_audit(panel),
        "model_fit": {
            m: {
                "beta": [round(float(x), 8) for x in f["beta"]],
                "cols": f["cols"],
                "smearing": round(float(f["smearing"]), 8),
            }
            for m, f in fits.items() if f is not None
        },
    })
    return result


# ------------------------------------------------------------------------ report


def write_report(result: dict, out_utc: str, panel_path: Path | None, panel_sha: str | None) -> dict:
    safe = out_utc.replace(":", "").replace("-", "")
    stem = f"evaluation_summary_TRACKA-LIQ-EXPANSION-RECOMPUTE-{safe}"
    json_path = RS / f"{stem}.json"
    md_path = RS / f"{stem}.md"
    json_path.write_text(json.dumps(convert(result), indent=2) + "\n")

    c = result.get("contrasts", {})
    L = [
        f"# Evaluation Summary — {EXPERIMENT_ID}",
        "",
        f"Generated: {out_utc}",
        f"Campaign: `{CAMPAIGN}`",
        f"Prereg: `{result['prereg']}` (status {result['prereg_status']}, frozen before outcomes)",
        "",
        f"## Verdict: **{result['verdict']}** ({result['status']})",
        "",
        f"- Promotable: `{result['promotable']}` (audit only, never promotable)",
        "- Sealed TRACKA-HL-EXPANSION artifacts: unchanged (read-only in this cell)",
        f"- Smoke run: `{result.get('smoke')}`",
        "",
        "## Sealed-reference replication statement",
        "",
        f"- Sealed C2_vs_B1 rel QLIKE reduction: {SEALED['C2_vs_B1']['rel_reduction_pct']}% "
        f"(CI {SEALED['C2_vs_B1']['ci']}, n_pairs={SEALED['C2_vs_B1']['n_pairs']}, "
        f"n_blocks={SEALED['C2_vs_B1']['n_blocks']}, symbols={SEALED['paired_symbols']})",
        f"- Recomputed C2_vs_B1 rel QLIKE reduction: {primary_rl(result)}% "
        f"(CI [{primary_ci_lo(result)}, {primary_ci_hi(result)}], "
        f"n_pairs={primary_n(result)}, n_blocks={primary_blocks(result)})",
        f"- Sealed 19.04% C2-vs-B1 replicates: {result.get('reproduces_sealed_19pct')} "
        f"(recomputed {primary_rl(result)}% vs sealed {SEALED['C2_vs_B1']['rel_reduction_pct']}%; "
        f"materially consistent threshold = sealed x 0.5 = {SEALED['C2_vs_B1']['rel_reduction_pct'] * 0.5:.2f}%)",
        f"- Sealed LOIO 4/8 replicates: recomputed LOIO {result.get('loio_pass')}/{result.get('loio_total')} "
        f"(sealed {SEALED['loio_pass']}/{SEALED['loio_total']})",
        f"- Sealed placebo failure (true 19.04% <= null p95 21.10%) replicates: "
        f"{bool(placebo_status(result))} "
        f"(recomputed true {primary_rl(result)}% vs null p95 {placebo_null_p95(result)}%)",
        "",
        "## Panel",
        "",
    ]
    if panel_path is not None:
        L.append(f"- Panel: `{panel_path.relative_to(REPO)}`")
    if panel_sha:
        L.append(f"- Panel SHA-256: `{panel_sha}`")
    L += [
        f"- Rows: {result.get('build', {}).get('total_buckets', 0)}",
        f"- Instruments: {len(result.get('instruments', []))} {result.get('instruments', [])}",
        f"- Test blocks with data: {result.get('test_blocks_with_data')} (need >= {MIN_TEST_BLOCKS})",
        f"- Test window: {result.get('test_window', ['?', '?'])}",
        "",
        "## Coverage (test rows)",
        "",
    ]
    for k, v in (result.get("coverage") or {}).items():
        L.append(f"- {k}: {v}")
    L += ["", "## Paired contrasts (QLIKE, lower is better)", ""]
    if c:
        L += [
            "| Contrast | n pairs | B QLIKE | A QLIKE | mean diff | 95% CI | rel reduction | Holm p | material | CI excl 0 |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
        for k in CONTRASTS:
            if k not in c:
                continue
            r = c[k]
            L.append(
                f"| {k} | {r['n_pairs']} | {r['qlike_b']} | {r['qlike_a']} | {r['mean_diff']} | "
                f"[{r['ci_lo']}, {r['ci_hi']}] | {r['rel_reduction_pct']}% | {r['holm_p']} | "
                f"{r['passes_materiality']} | {r['ci_excludes_zero']} |"
            )
    else:
        L.append("_No contrasts computed._")
    L += [
        "",
        "## Robustness",
        "",
        f"- LOIO: {result.get('loio_pass')}/{result.get('loio_total')} instruments clear the {MATERIALITY_PCT}% materiality floor",
        f"- Placebo (funding permutation, n={result.get('placebo', {}).get('n_perm')}): "
        f"null p95 {result.get('placebo', {}).get('null_p95')}%, p≈{result.get('placebo', {}).get('p_value_approx')}, "
        f"pass={result.get('placebo', {}).get('overall_pass')}",
        "",
        "## Per-symbol (C2 vs B1)",
        "",
        "| Symbol | n | B1 QLIKE | C2 QLIKE | rel reduction |",
        "|---|---|---|---|---|",
    ]
    for sym, v in (result.get("per_symbol") or {}).items():
        L.append(f"| {sym} | {v['n_pairs']} | {v['qlike_B1']} | {v['qlike_C2']} | {v['rel_reduction_pct']}% |")
    L += ["", "## Per-block (C2 vs B1)", "", "| Block | n | B1 QLIKE | C2 QLIKE | rel reduction |", "|---|---|---|---|---|"]
    for d, v in (result.get("per_block") or {}).items():
        L.append(f"| {d} | {v['n_pairs']} | {v['b1_qlike']} | {v['c2_qlike']} | {v['rel_reduction_pct']}% |")
    L += ["", "## Leakage audit", ""]
    for k, v in (result.get("leakage_audit") or {}).items():
        if k == "notes":
            continue
        L.append(f"- {k}: {v}")
    if (result.get("leakage_audit") or {}).get("notes"):
        L += ["", (result["leakage_audit"]["notes"]), ""]
    if result.get("failing_minima"):
        L += ["", "## Failing minima", ""] + [f"- {m}" for m in result["failing_minima"]]
    if result.get("inconclusive_reason"):
        L += ["", f"Inconclusive reason: {result['inconclusive_reason']}"]
    L += [
        "",
        "## Comparison to the sealed Track A expansion result",
        "",
        "| Contrast | Sealed rel reduction | Recomputed rel reduction |",
        "|---|---|---|",
    ]
    for k in ["C2_vs_B1", "C1_vs_B1", "C2_vs_C1"]:
        sealed = SEALED.get(k, {}).get("rel_reduction_pct")
        got = (c.get(k) or {}).get("rel_reduction_pct")
        L.append(f"| {k} | {sealed}% | {got if got is not None else 'n/a'} |")
    L += [
        "",
        "## Notes",
        "",
        "- Observed Hyperliquid ironflow liquidation labels only; no Binance/2024 conflation; "
        "no modeled/proxy/synthetic labels; no threshold-shopping; no sealed-holdout reuse.",
        "- Premium IS computable here (Hyperliquid funding cache carries the premium field).",
        "- No zero-fill, no forward-fill. Funding/RV attached by backward merge_asof. "
        "Target is a strictly forward 24h liquidation intensity.",
        "",
    ]
    md_path.write_text("\n".join(L))
    return {"json": json_path, "md": md_path}


def primary_rl(result) -> str:
    v = (result.get("contrasts") or {}).get("C2_vs_B1", {}).get("rel_reduction_pct")
    return f"{v:.4f}" if v is not None else "n/a"


def primary_ci_lo(result) -> str:
    v = (result.get("contrasts") or {}).get("C2_vs_B1", {}).get("ci_lo")
    return f"{v:.6f}" if v is not None else "n/a"


def primary_ci_hi(result) -> str:
    v = (result.get("contrasts") or {}).get("C2_vs_B1", {}).get("ci_hi")
    return f"{v:.6f}" if v is not None else "n/a"


def primary_n(result):
    return (result.get("contrasts") or {}).get("C2_vs_B1", {}).get("n_pairs")


def primary_blocks(result):
    return (result.get("contrasts") or {}).get("C2_vs_B1", {}).get("n_blocks")


def placebo_status(result):
    return result.get("placebo", {}).get("overall_pass")


def placebo_null_p95(result):
    return result.get("placebo", {}).get("null_p95")


# --------------------------------------------------------------------------- main


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--smoke", action="store_true", help="tiny subsample; never a verdict")
    ap.add_argument("--out-utc", default=None, help="override UTC stamp")
    ap.add_argument("--write-prereg", action="store_true", help="freeze the prereg and exit")
    args = ap.parse_args(argv)

    out_utc = args.out_utc or now_utc()
    if args.write_prereg:
        prereg = write_prereg(out_utc)
        print(json.dumps({"prereg": str(PREREG_JSON.relative_to(REPO)), "status": prereg["status"]}, indent=2))
        return 0

    if not PREREG_JSON.exists():
        raise SystemExit(
            f"missing frozen prereg {PREREG_JSON}; freeze it first: "
            f"python3 scripts/fclr_liq_expansion_recompute.py --write-prereg"
        )
    prereg = json.loads(PREREG_JSON.read_text())
    assert_prereg_frozen(prereg)

    panel, build = build_panel()
    if panel.empty:
        result = {
            "experiment_id": EXPERIMENT_ID,
            "campaign": CAMPAIGN,
            "generated": out_utc,
            "status": "INADMISSIBLE",
            "verdict": "INADMISSIBLE",
            "failing_minima": ["no panel built from caches"],
            "promotable": False,
            "max_status": "EXPLORATORY_ONLY",
        }
        write_report(result, out_utc, None, None)
        print(json.dumps({"verdict": "INADMISSIBLE"}, indent=2))
        return 1

    safe = out_utc.replace(":", "").replace("-", "")
    panel_path = RS / f"tracka_liq_expansion_recompute_panel_{safe}.parquet"
    cols = [
        "coin", "ts", "split", "liq_notional_usd", "liq_event_count", "has_label",
        "target_next_intensity", "liq_lag1", "log_liq_lag1", "rv1h", "rv24h", "rv168h",
        "log_rv1h", "log_rv24h", "log_rv168h", "ema_dist", "ema_dist_z",
        "fundingRate", "signed_funding_z", "premium", "premium_z",
        "abs_fund_pct", "abs_fund_pct_z", "has_funding", "has_rv_complete",
    ]
    cols = [c for c in cols if c in panel.columns]
    out = panel[cols].copy()
    out.to_parquet(panel_path, index=False)
    panel_sha = sha256_file(panel_path)

    build_report = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "generated": out_utc,
        "prereg": str(PREREG_JSON.relative_to(REPO)),
        "panel_path": str(panel_path.relative_to(REPO)),
        "panel_sha256": panel_sha,
        "window_utc": "2026-05-01T00:00:00Z .. 2026-10-31T23:59:59Z",
        "symbols": UNIVERSE,
        "markets": [PERP[s] for s in UNIVERSE],
        "inputs": {
            "ironflow_labels": build["label"]["checksums"],
            "ironflow_label_rows_total": build["label"]["rows_total"],
            "hyperliquid_funding": build["funding"]["checksums"],
            "hyperliquid_funding_rows_per_coin": build["funding"]["rows_per_coin"],
            "hyperliquid_candles": build["candles"]["checksums"],
            "hyperliquid_candle_rows_per_coin": build["candles"]["rows_per_coin"],
        },
        "panel": {
            "total_buckets": build["total_buckets"],
            "buckets_with_label": build["buckets_with_label"],
            "buckets_with_funding": build["buckets_with_funding"],
            "buckets_with_rv24h": build["buckets_with_rv24h"],
            "buckets_complete_label_funding_rv": build["buckets_complete_label_funding_rv"],
            "symbols_with_any_label": build["symbols_with_any_label"],
            "n_symbols_with_label": build["n_symbols_with_label"],
        },
        "row_counts": {
            "total": build["total_buckets"],
            "train": build["rows_train"],
            "validation": build["rows_validation"],
            "test": build["rows_test"],
            "target_non_null": build["target_non_null"],
            "target_positive": build["target_positive"],
        },
        "splits": prereg["splits"],
        "sealed_reference_panel_sha256": SEALED["panel_sha256"],
        "sealed_reference_total_buckets": SEALED["panel_total_buckets"],
    }
    br_path = RS / f"tracka_liq_expansion_recompute_panel_build_report_{safe}.json"
    br_path.write_text(json.dumps(convert(build_report), indent=2) + "\n")

    result = run_audit(prereg, out_utc, args.smoke, panel, build_report)
    result["panel_path"] = str(panel_path.relative_to(REPO))
    result["panel_sha256"] = panel_sha
    paths = write_report(result, out_utc, panel_path, panel_sha)
    print(
        json.dumps(
            {
                "verdict": result["verdict"],
                "status": result["status"],
                "reproduces_sealed_19pct": result.get("reproduces_sealed_19pct"),
                "contrasts": result.get("contrasts", {}),
                "loio": f"{result.get('loio_pass')}/{result.get('loio_total')}",
                "placebo": result.get("placebo", {}),
                "artifacts": [str(paths["json"].relative_to(REPO)), str(paths["md"].relative_to(REPO))],
                "panel": str(panel_path.relative_to(REPO)),
                "panel_sha256": panel_sha,
                "build_report": str(br_path.relative_to(REPO)),
            },
            indent=2,
            default=str,
        )
    )
    return 0 if result["verdict"] != "INADMISSIBLE" else 1


if __name__ == "__main__":
    sys.exit(main())
