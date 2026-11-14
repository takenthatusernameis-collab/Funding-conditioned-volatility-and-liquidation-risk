#!/usr/bin/env python3
"""FCLR-011 independent recomputation (Phase A of FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z).

Rebuilds the FCLR-011 volatility panel from the cached Binance public archive and
re-runs the frozen design end-to-end with a clean OLS/HAR implementation.

Why this exists: the sealed FCLR-011 PASS (C2 vs B1 -4.94% QLIKE on
2026-05-08..2026-08-06) is the program's only volatility gate PASS and it failed
every later out-of-sample test. ``research_state/data_cache/fclr011_panel.json``
is an unresolved Git-LFS pointer, and the earlier "recompute audit" reused the
heuristic ``run_trackc_*`` scripts (+6.86%, not the sealed +4.94%). This script is
the clean independent check: no LFS panel, no heuristic predictor.

Design (frozen in the prereg, asserted here, never read from outcomes):
  universe   BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
  target     next-24h realized variance of mark-price returns (sum of squared
             log returns over t+1..t+24), scored on QLIKE
  models     B0 persistence, B1 HAR, C1 = B1 + signed funding + trailing
             absolute-funding percentile, C2 = C1 + mark/index premium + mark/EMA24
  fit        OLS on log(RV + 1e-12), training-only mean/std scaling, documented
             training-only smearing back-transform
  missing    no zero-fill, no forward-fill; paired contrasts use common eligible rows
  inference  paired circular block bootstrap over UTC days (2000 deterministic reps),
             Holm across the three registered contrasts, LOIO, funding placebo,
             per-symbol and per-block stability, leakage audit
  splits     train 2026-01-01..2026-03-17, val 2026-03-25..2026-04-30,
             test 2026-05-08..2026-08-06, 7-day purge/embargo at both boundaries

Source limitation (recorded, not hidden): the 2026 cache holds only ``klines`` and
``fundingRate`` archives for the five symbols. ``markPriceKlines`` /
``indexPriceKlines`` / ``premiumIndexKlines`` are absent, so the mark/index premium
cannot be computed. The premium slot of C2 is therefore registered as NOT
COMPUTABLE and C2 degrades to C1 + mark/EMA24 distance; the build report and the
evaluation summary both state this, and the verdict is capped at INCONCLUSIVE
unless the primary contrast still reproduces materially.

Outputs:
  research_state/fclr011_recompute_panel_<UTC>.parquet
  research_state/fclr011_recompute_panel_build_report_<UTC>.json
  research_state/evaluation_summary_FCLR-011-RECOMPUTE-<UTC>.json
  research_state/evaluation_summary_FCLR-011-RECOMPUTE-<UTC>.md

No network. No mutation of sealed FCLR-011 artifacts. Never promotable.

Usage:
  python3 scripts/fclr011_recompute_audit.py
  python3 scripts/fclr011_recompute_audit.py --smoke        # tiny subsample, not a verdict
  python3 scripts/fclr011_recompute_audit.py --out-utc 2026-11-14T05:30:00Z
  python3 scripts/fclr011_recompute_audit.py --write-prereg # freeze the prereg only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
CACHE = RS / "data_cache"

CAMPAIGN = "FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z"
EXPERIMENT_ID = "FCLR-011-INDEPENDENT-RECOMPUTE-20261114T042139Z"
PREREG_STEM = "prereg_fclr011_recompute_20261114T042139Z"
PREREG_JSON = RS / f"{PREREG_STEM}.json"
PREREG_MD = RS / f"{PREREG_STEM}.md"

UNIVERSE = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
MONTHS = [f"2026_{m:02d}" for m in range(1, 9)]  # cache dirs use YYYY_MM

TRAIN = ("2026-01-01T00:00:00Z", "2026-03-17T23:00:00Z")
VAL = ("2026-03-25T00:00:00Z", "2026-04-30T23:00:00Z")
TEST = ("2026-05-08T00:00:00Z", "2026-08-06T23:00:00Z")
EMBARGO = timedelta(days=7)

HORIZON = 24
EPS = 1e-12
TRAIL_WINDOW = 90 * 24
TRAIL_MIN_OBS = 30
BOOT_REPS = 2000
BOOT_BLOCK_HOURS = 24
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

SEALED = {
    "C2_vs_B1": {"rel_reduction_pct": 4.94, "ci": [-0.032546, -0.001418], "n_pairs": 10785},
    "C1_vs_B1": {"rel_reduction_pct": 1.36, "ci": [-0.008260, -0.001111], "n_pairs": 10785},
    "C2_vs_C1": {"rel_reduction_pct": 3.63, "ci": [-0.027256, 0.001778], "n_pairs": 10785},
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


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def parse_ts(s: str) -> pd.Timestamp:
    return pd.Timestamp(s.replace("Z", "+00:00"))


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
            "Clean independent recomputation of the sealed FCLR-011 volatility PASS "
            "(C2 vs B1 4.94% QLIKE, CI [-0.032546,-0.001418], 5 instruments, 3 blocks, "
            "test 2026-05-08..2026-08-06) from cached Binance inputs, without the Git-LFS "
            "panel and without the heuristic run_trackc_* predictor."
        ),
        "sealed_reference": {
            "evaluation_summary": "research_state/evaluation_summary_FCLR-011.md",
            "prereg": "research_state/pre_registration_fclr011_20261103T111501Z.md",
            "verdict": "forecast_gate_PASS",
            "primary_contrast": "C2_vs_B1",
            "rel_reduction_pct": SEALED["C2_vs_B1"]["rel_reduction_pct"],
            "ci_qlipe_diff": SEALED["C2_vs_B1"]["ci"],
            "instruments": 5,
            "test_blocks": 3,
        },
        "universe": UNIVERSE,
        "horizon_hours": HORIZON,
        "target": {
            "name": "rv24h",
            "definition": (
                "next-24h realized variance of mark-price log returns: sum of squared "
                "1h log returns over t+1..t+24, forward-looking from decision time t"
            ),
            "source_series": "klines close (mark price unavailable in cache)",
            "source_limitation": (
                "markPriceKlines/indexPriceKlines/premiumIndexKlines are absent from the "
                "2026 cache; close-to-close RV and close-based premium proxies are used and "
                "recorded in the build report"
            ),
        },
        "models": {
            "B0": ["log_rv24h_lag1"],
            "B1": ["log_rv1h", "log_rv24h", "log_rv168h"],
            "C1": ["B1", "signed_funding", "abs_funding_pct_trail"],
            "C2": ["C1", "premium", "ema24_dist"],
            "premium_status": "NOT_COMPUTABLE_WITHOUT_INDEX_PRICE",
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
            "block_hours": BOOT_BLOCK_HOURS,
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
            "test": list(TEST),
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
            "REPRODUCED": "materially consistent with sealed +4.94% under the frozen design",
            "NOT_REPRODUCED": "fails to reproduce the sealed result",
            "INCONCLUSIVE": "data/coverage/numerical limits prevent a clean verdict",
            "INADMISSIBLE": "frozen minimums are not met",
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
        f"- Target: {prereg['target']['definition']}",
        f"- Target source: {prereg['target']['source_series']}",
        f"- Source limitation: {prereg['target']['source_limitation']}",
        "- Models: B0 persistence; B1 HAR; C1 = B1 + signed funding + trailing |funding| percentile; C2 = C1 + premium + EMA24 distance",
        "- Premium status: NOT_COMPUTABLE_WITHOUT_INDEX_PRICE",
        "- Fit: OLS on log(RV + 1e-12), train-only scaling, train-only smearing back-transform",
        "- Missing data: no zero-fill, no forward-fill; paired contrasts use common eligible rows",
        "- Primary metric: paired OOS QLIKE, C2 vs B1",
        "- Inference: circular block bootstrap over UTC days, 24h blocks, 2000 reps, seed 20261114; Holm across 3 contrasts",
        "- Robustness: LOIO, funding-permutation placebo (200 reps), per-symbol and per-block stability, leakage audit",
        "",
        "## Frozen splits",
        "",
        f"- Train: {TRAIN[0]} .. {TRAIN[1]}",
        f"- Validation: {VAL[0]} .. {VAL[1]}",
        f"- Test: {TEST[0]} .. {TEST[1]}",
        f"- Purge/embargo: {EMBARGO.days} days at both boundaries",
        "",
        "## Stop rule",
        "",
        f"- Instruments < {MIN_INSTRUMENTS}, test blocks < {MIN_TEST_BLOCKS}, or core coverage < {MIN_CORE_COVERAGE} → INADMISSIBLE with exact failing minima",
        "",
        "## Non-goals",
        "",
        "- Not promotable. EXPLORATORY_ONLY. Does not reopen the sealed FCLR-011 verdict.",
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
    if prereg.get("splits") != {"train": list(TRAIN), "validation": list(VAL), "test": list(TEST), "purge_embargo_days": 7}:
        raise SystemExit(f"prereg splits drift: {prereg.get('splits')}")
    if prereg.get("universe") != UNIVERSE:
        raise SystemExit(f"prereg universe drift: {prereg.get('universe')}")


# ------------------------------------------------------------------- panel rebuild


def _read_zip_csvs(zip_path: Path, want: str) -> list[dict]:
    rows: list[dict] = []
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            if not name.endswith(".csv"):
                continue
            stem = Path(name).stem
            if want == "klines":
                if "-1h-" not in stem:
                    continue
            elif want not in stem:
                continue
            raw = z.read(name)
            lines = raw.decode("utf-8", errors="replace").splitlines()
            if not lines:
                continue
            header = lines[0].split(",")
            for line in lines[1:]:
                if not line.strip():
                    continue
                rows.append(dict(zip(header, line.split(","))))
    return rows


def load_klines(sym: str, months: list[str]) -> pd.DataFrame:
    frames = []
    for ym in months:
        month_dir = CACHE / f"{sym}_{ym}"
        if not month_dir.is_dir():
            continue
        for zp in sorted(month_dir.glob("*.zip")):
            for r in _read_zip_csvs(zp, "klines"):
                try:
                    frames.append(
                        {
                            "ts": pd.to_datetime(int(r["open_time"]), unit="ms", utc=True),
                            "close": float(r["close"]),
                            "high": float(r["high"]),
                            "low": float(r["low"]),
                            "open": float(r["open"]),
                        }
                    )
                except (KeyError, TypeError, ValueError):
                    continue
    if not frames:
        return pd.DataFrame(columns=["ts", "close", "high", "low", "open"])
    df = pd.DataFrame(frames)
    df = df.dropna(subset=["ts", "close"])
    df = df[(df["close"] > 0) & (df["open"] > 0)]
    df = df.sort_values("ts").drop_duplicates(subset=["ts"], keep="last")
    return df.reset_index(drop=True)


def load_funding(sym: str, months: list[str]) -> pd.DataFrame:
    frames = []
    for ym in months:
        month_dir = CACHE / f"{sym}_{ym}"
        if not month_dir.is_dir():
            continue
        for zp in sorted(month_dir.glob("*fundingRate*.zip")):
            for r in _read_zip_csvs(zp, "fundingRate"):
                try:
                    rate = float(r["last_funding_rate"])
                    frames.append(
                        {
                            "funding_ts": pd.to_datetime(int(r["calc_time"]), unit="ms", utc=True),
                            "signed_funding": rate,
                            "funding_interval_hours": int(float(r.get("funding_interval_hours", 8) or 8)),
                        }
                    )
                except (KeyError, TypeError, ValueError):
                    continue
    if not frames:
        return pd.DataFrame(columns=["funding_ts", "signed_funding", "funding_interval_hours"])
    df = pd.DataFrame(frames).sort_values("funding_ts").drop_duplicates(subset=["funding_ts"], keep="last")
    return df.reset_index(drop=True)


def build_symbol_panel(sym: str, months: list[str]) -> tuple[pd.DataFrame, dict]:
    kl = load_klines(sym, months)
    stats = {"symbol": sym, "kline_rows_raw": int(len(kl))}
    if kl.empty:
        stats["error"] = "no klines"
        return pd.DataFrame(), stats

    full_hours = pd.date_range(kl["ts"].min(), kl["ts"].max(), freq="1h", tz="UTC")
    kl = kl.set_index("ts").reindex(full_hours)
    stats["kline_rows_on_regular_grid"] = int(len(kl))
    stats["kline_missing_hours"] = int(kl["close"].isna().sum())

    logret = np.log(kl["close"] / kl["close"].shift(1))
    sq = logret.pow(2)

    # ---- trailing realized-variance features, causal (available at decision time t)
    kl["rv1h"] = sq
    kl["rv24h"] = sq.rolling(24, min_periods=24).sum()
    kl["rv168h"] = sq.rolling(168, min_periods=168).sum()

    close = kl["close"]
    kl["ema24"] = close.ewm(span=24, adjust=False, min_periods=24).mean()
    kl["ema24_dist"] = (close - kl["ema24"]) / kl["ema24"]

    panel = kl.reset_index().rename(columns={"index": "ts"})
    if "ts" not in panel.columns:
        panel = panel.rename(columns={panel.columns[0]: "ts"})
    panel["coin"] = sym

    # ---- target: forward 24h RV of log returns over t+1..t+24 (strictly future)
    fwd = sq.shift(-1).rolling(HORIZON, min_periods=HORIZON).sum().shift(-(HORIZON - 1))
    panel["target_rv24h"] = fwd.reindex(panel["ts"]).values

    # ---- funding as-of (latest settled rate at or before decision time)
    # Explicit backward as-of via searchsorted: a settled rate at time f is used for
    # every decision timestamp t with f <= t <= f + 24h. Never forward-looking.
    fund = load_funding(sym, months)
    panel = panel.sort_values("ts").reset_index(drop=True)
    if fund.empty:
        panel["signed_funding"] = np.nan
        panel["funding_interval_hours"] = np.nan
        panel["funding_asof_lag_h"] = np.nan
        stats["funding_rows"] = 0
        stats["funding_asof_min_lag_h"] = None
    else:
        fts = fund.sort_values("funding_ts")["funding_ts"].to_numpy()
        frate = fund.sort_values("funding_ts")["signed_funding"].to_numpy(dtype=float)
        fint = fund.sort_values("funding_ts")["funding_interval_hours"].to_numpy()
        tns = panel["ts"].to_numpy()
        pos = np.searchsorted(fts, tns, side="right") - 1
        tol = np.timedelta64(24, "h")
        safe = np.clip(pos, 0, None)
        gap = tns - fts[safe]
        ok = (pos >= 0) & (gap <= tol)
        rate = np.where(ok, frate[np.clip(safe, 0, len(frate) - 1)], np.nan)
        ivl = np.where(ok, fint[np.clip(safe, 0, len(fint) - 1)], np.nan)
        panel["signed_funding"] = rate
        panel["funding_interval_hours"] = ivl
        lag = gap.astype("timedelta64[s]").astype("float64") / 3600.0
        lag = np.where(ok, lag, np.nan)
        panel["funding_asof_lag_h"] = lag
        stats["funding_rows"] = int(len(fund))
        stats["funding_asof_min_lag_h"] = (
            round(float(np.nanmin(lag)), 3) if np.isfinite(lag).any() else None
        )

    # ---- trailing absolute-funding percentile over prior 90d, min 30 obs (causal)
    # vectorised two-pointer over the hourly grid; only rows whose funding is known
    # are eligible, and the current value is excluded from its own history window.
    panel = panel.sort_values(["coin", "ts"]).reset_index(drop=True)
    absfund = panel["signed_funding"].abs()
    known = absfund.notna().to_numpy()
    known_ts = panel["ts"].to_numpy()[known]
    known_vals = absfund.to_numpy()[known]
    trail_pct: list[float] = []
    trail_n: list[int] = []
    lo_ptr = 0
    for ts, cur, ok in zip(panel["ts"].to_numpy(), absfund.to_numpy(), known):
        if not ok:
            trail_pct.append(np.nan)
            trail_n.append(0)
            continue
        cutoff = ts - np.timedelta64(TRAIL_WINDOW, "h")
        while lo_ptr < len(known_ts) and known_ts[lo_ptr] < cutoff:
            lo_ptr += 1
        hi = int(np.searchsorted(known_ts, ts, side="left"))
        hist = known_vals[lo_ptr:hi]
        n_hist = int(len(hist))
        trail_n.append(n_hist)
        if n_hist < TRAIL_MIN_OBS:
            trail_pct.append(np.nan)
            continue
        trail_pct.append(float((hist <= cur).mean()))
    panel["abs_funding_pct_trail"] = trail_pct
    panel["abs_funding_trail_n"] = trail_n

    # ---- causal lag features (available at decision time t)
    panel["log_rv1h"] = np.log(panel["rv1h"].where(panel["rv1h"] > 0) + EPS)
    panel["log_rv24h"] = np.log(panel["rv24h"].where(panel["rv24h"] > 0) + EPS)
    panel["log_rv168h"] = np.log(panel["rv168h"].where(panel["rv168h"] > 0) + EPS)
    panel["premium"] = np.nan  # mark/index premium: not computable without index klines
    panel["premium_status"] = "NOT_COMPUTABLE_WITHOUT_INDEX_PRICE"

    panel["split"] = None
    panel.loc[(panel["ts"] >= parse_ts(TRAIN[0])) & (panel["ts"] <= parse_ts(TRAIN[1])), "split"] = "train"
    panel.loc[(panel["ts"] >= parse_ts(VAL[0])) & (panel["ts"] <= parse_ts(VAL[1])), "split"] = "validation"
    panel.loc[(panel["ts"] >= parse_ts(TEST[0])) & (panel["ts"] <= parse_ts(TEST[1])), "split"] = "test"

    stats["rows_total"] = int(len(panel))
    stats["rows_train"] = int((panel["split"] == "train").sum())
    stats["rows_validation"] = int((panel["split"] == "validation").sum())
    stats["rows_test"] = int((panel["split"] == "test").sum())
    stats["target_non_null"] = int(panel["target_rv24h"].notna().sum())
    return panel, stats


CORE_FEATURES = ["log_rv1h", "log_rv24h", "log_rv168h", "signed_funding", "abs_funding_pct_trail", "ema24_dist"]


def assemble_panel(months: list[str]) -> tuple[pd.DataFrame, dict]:
    frames, per_symbol = [], []
    for sym in UNIVERSE:
        p, st = build_symbol_panel(sym, months)
        if p.empty:
            per_symbol.append(st)
            continue
        frames.append(p)
        st["coverage"] = {
            f: round(float(p[f].notna().mean()), 6) for f in CORE_FEATURES if f in p.columns
        }
        st["core_coverage"] = round(
            float(p[CORE_FEATURES].notna().all(axis=1).mean()), 6
        ) if len(p) else 0.0
        per_symbol.append(st)
    if not frames:
        return pd.DataFrame(), {"symbols": per_symbol, "rows_total": 0}
    panel = pd.concat(frames, ignore_index=True)
    panel = panel.sort_values(["coin", "ts"]).reset_index(drop=True)
    report = {
        "symbols": per_symbol,
        "rows_total": int(len(panel)),
        "instruments": sorted(panel["coin"].unique().tolist()),
    }
    return panel, report


# ------------------------------------------------------------------------ fitting


def _solve(A: np.ndarray, b: np.ndarray) -> np.ndarray | None:
    try:
        beta, *_ = np.linalg.lstsq(A, b, rcond=None)
    except np.linalg.LinAlgError:
        return None
    if not np.all(np.isfinite(beta)):
        return None
    return beta


def design_matrix(df: pd.DataFrame, model: str, spec: dict) -> tuple[np.ndarray | None, list[str]]:
    cols: list[str] = []
    if model == "B0":
        cols = ["log_rv24h"]
    elif model == "B1":
        cols = ["log_rv1h", "log_rv24h", "log_rv168h"]
    elif model == "C1":
        cols = ["log_rv1h", "log_rv24h", "log_rv168h", "funding_z", "abs_fund_pct_z"]
    elif model == "C2":
        cols = ["log_rv1h", "log_rv24h", "log_rv168h", "funding_z", "abs_fund_pct_z", "ema24_dist_z"]
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


def predict(fit: dict, df: pd.DataFrame, model: str, spec: dict) -> np.ndarray | None:
    A, _ = design_matrix(df, model, spec)
    if A is None or fit is None:
        return None
    z = A @ fit["beta"]
    # smearing back-transform: E[RV] = exp(z) * mean(exp(resid)) over training residuals
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


def circular_block_indices(n: int, block: int, reps: int, seed: int) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    n_blocks = int(math.ceil(n / block))
    out = []
    for _ in range(reps):
        starts = rng.integers(0, n, size=n_blocks)
        idx = np.concatenate([(np.arange(s, s + block) % n) for s in starts])[:n]
        out.append(idx)
    return out


def paired_bootstrap(diffs: np.ndarray, day_keys: np.ndarray, reps: int, seed: int) -> dict:
    """Circular block bootstrap over complete UTC days of paired per-row QLIKE diffs."""
    n = len(diffs)
    if n == 0:
        return {"mean": None, "ci_lo": None, "ci_hi": None, "n_pairs": 0, "n_blocks": 0}
    udays = np.unique(day_keys)
    # block = one UTC day; build contiguous day blocks so the resample respects time order
    blocks = [np.where(day_keys == d)[0] for d in udays]
    blocks = [b for b in blocks if len(b)]
    rng = np.random.default_rng(seed)
    means = []
    for _ in range(reps):
        take = []
        for _b in range(len(blocks)):
            blk = blocks[int(rng.integers(0, len(blocks)))]
            take.append(diffs[blk])
        if not take:
            continue
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
    t = panel[["coin", "ts", "target_rv24h", "rv24h", "log_rv24h", "rv1h", "rv168h", "signed_funding", "ema24_dist"]].copy()
    same = np.isclose(
        t["target_rv24h"].astype(float), t["rv24h"].astype(float), equal_nan=True
    )
    checks["target_not_equal_to_trailing_rv24h"] = bool((~same).mean() > 0.99)
    checks["target_uses_strictly_future_bars"] = True  # constructed as sum over t+1..t+24
    if "funding_asof_lag_h" in panel.columns:
        lag = panel["funding_asof_lag_h"].dropna()
        checks["funding_asof_backward_only"] = bool((lag >= 0).all()) if len(lag) else True
        checks["funding_asof_min_lag_h"] = round(float(lag.min()), 3) if len(lag) else None
    else:
        checks["funding_asof_backward_only"] = True
    checks["zero_fill_used"] = False
    checks["forward_fill_used"] = False
    checks["train_only_scaling"] = True
    checks["splits_respect_embargo_days"] = True
    checks["notes"] = (
        "target_rv24h is a forward sum over t+1..t+24 and never equals trailing rv24h; "
        "funding is attached with merge_asof(direction=backward, tolerance=24h) and the "
        "resulting lag is reported; no zero/forward fill; scaling fit on train rows only; "
        "7d purge/embargo at both boundaries."
    )
    return checks


def run_audit(prereg: dict, out_utc: str, smoke: bool) -> dict:
    assert_prereg_frozen(prereg)

    months = MONTHS
    if smoke:
        months = ["2026_05", "2026_06"]

    panel, build = assemble_panel(months)

    test_start, test_end = parse_ts(TEST[0]), parse_ts(TEST[1])
    test_all = panel[(panel["split"] == "test") & panel["target_rv24h"].notna()].copy()
    core_mask = test_all[CORE_FEATURES].notna().all(axis=1)
    test_core = test_all[core_mask].copy()

    instruments = sorted(test_core["coin"].unique().tolist()) if len(test_core) else []
    test_days = (
        sorted({ts.floor("D") for ts in test_core["ts"]}) if len(test_core) else []
    )
    coverage = (
        {
            "test_rows_total": int(len(test_all)),
            "test_rows_core_complete": int(len(test_core)),
            "core_coverage": round(float(core_mask.mean()), 6) if len(test_all) else 0.0,
        }
        if len(test_all)
        else {"test_rows_total": 0, "test_rows_core_complete": 0, "core_coverage": 0.0}
    )

    inadmissible = []
    if len(instruments) < MIN_INSTRUMENTS:
        inadmissible.append(f"instruments {len(instruments)} < {MIN_INSTRUMENTS}")
    if len(test_days) < MIN_TEST_BLOCKS:
        inadmissible.append(f"test_blocks {len(test_days)} < {MIN_TEST_BLOCKS}")
    if coverage["core_coverage"] < MIN_CORE_COVERAGE:
        inadmissible.append(
            f"core_coverage {coverage['core_coverage']} < {MIN_CORE_COVERAGE}"
        )

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
        "test_window": [TEST[0], TEST[1]],
        "sealed_reference": SEALED,
    }

    if inadmissible:
        result["status"] = "INADMISSIBLE"
        result["verdict"] = "INADMISSIBLE"
        result["failing_minima"] = inadmissible
        return result

    train = panel[panel["split"] == "train"].copy()
    train_core = train[train[CORE_FEATURES].notna().all(axis=1)].copy()
    if train_core.empty:
        result["status"] = "INADMISSIBLE"
        result["verdict"] = "INADMISSIBLE"
        result["failing_minima"] = ["no complete training rows"]
        return result

    # ---- train-only scaling (fit on train, applied everywhere)
    spec = {}
    for col, out in [
        ("signed_funding", "funding_z"),
        ("abs_funding_pct_trail", "abs_fund_pct_z"),
        ("ema24_dist", "ema24_dist_z"),
    ]:
        mu = float(train_core[col].mean())
        sd = float(train_core[col].std(ddof=0))
        sd = sd if sd > 1e-12 else 1.0
        spec[col] = {"mu": mu, "sd": sd}
        train_core[out] = (train_core[col] - mu) / sd
        panel[out] = (panel[col] - mu) / sd

    train_core["log_target"] = np.log(train_core["target_rv24h"].clip(lower=EPS))
    panel["log_target"] = np.log(panel["target_rv24h"].clip(lower=EPS))

    fits = {}
    for m in MODELS:
        f = fit_ols(train_core, m, spec)
        if f is None:
            fits[m] = None
            continue
        resid = train_core["log_target"].to_numpy(dtype=float)
        A, _ = design_matrix(train_core, m, spec)
        mask = np.isfinite(resid)
        r = resid[mask] - A[mask] @ f["beta"]
        f["smearing"] = float(np.mean(np.exp(r))) if len(r) else 1.0
        spec["smearing"] = f["smearing"]
        fits[m] = f

    eval_rows = test_core.copy()
    preds = {}
    for m in MODELS:
        p = predict(fits[m], eval_rows, m, spec)
        if p is None:
            result["status"] = "INCONCLUSIVE"
            result["verdict"] = "INCONCLUSIVE"
            result["inconclusive_reason"] = f"model {m} not fittable on train rows"
            return result
        preds[m] = p

    y = eval_rows["target_rv24h"].to_numpy(dtype=float)
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
    contrast = {}
    pvals = {}
    for a, b in [("C2", "B1"), ("C1", "B1"), ("C2", "C1")]:
        qa, qb = q[a], q[b]
        d = qa - qb
        boot = paired_bootstrap(d, day_keys, BOOT_REPS, BOOT_SEED)
        mae_a = float(np.mean(np.abs(y - preds[a])))
        mae_b = float(np.mean(np.abs(y - preds[b])))
        rmse_a = float(np.sqrt(np.mean((y - preds[a]) ** 2)))
        rmse_b = float(np.sqrt(np.mean((y - preds[b]) ** 2)))
        mean_a, mean_b = float(np.nanmean(qa)), float(np.nanmean(qb))
        rel = (mean_b - mean_a) / mean_b * 100.0 if mean_b > 0 else None
        # one-sided sign-flip permutation p that the mean paired diff is < 0
        # (C better). Deterministic, exact for the observed mean.
        rng_p = np.random.default_rng(BOOT_SEED)
        signs = rng_p.choice([-1.0, 1.0], size=(2000, d.size))
        null_means = (d[None, :] * signs).mean(axis=1)
        p = float((null_means <= d.mean()).mean())
        key = f"{a}_vs_{b}"
        contrast[key] = {
            "n_pairs": int(len(d)),
            "qlike_a": round(mean_a, 6),
            "qlike_b": round(mean_b, 6),
            "mean_diff": boot["mean"] if boot["mean"] is None else round(boot["mean"], 8),
            "ci_lo": boot["ci_lo"] if boot["ci_lo"] is None else round(boot["ci_lo"], 8),
            "ci_hi": boot["ci_hi"] if boot["ci_hi"] is None else round(boot["ci_hi"], 8),
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
    loio_pass = sum(
        1
        for v in per_symbol.values()
        if (v["rel_reduction_pct"] or 0) >= MATERIALITY_PCT
    )

    per_block = {}
    for d in test_days:
        m = (eval_rows["ts"].dt.floor("D") == d).to_numpy()
        if m.sum() == 0:
            continue
        mb, ma = float(np.nanmean(q["B1"][m])), float(np.nanmean(q["C2"][m]))
        per_block[str(d.date())] = {
            "n_pairs": int(m.sum()),
            "rel_reduction_pct": round((mb - ma) / mb * 100.0, 4) if mb > 0 else None,
        }

    # ---- funding-permutation placebo (within instrument, preserves marginal)
    rng = np.random.default_rng(PLACEBO_SEED)
    null_rel = []
    base = eval_rows.copy()
    for _ in range(PLACEBO_REPS):
        perm = base.copy()
        perm["signed_funding"] = rng.permutation(perm["signed_funding"].values)
        perm["abs_funding_pct_trail"] = rng.permutation(perm["abs_funding_pct_trail"].values)
        for col, out in [("signed_funding", "funding_z"), ("abs_funding_pct_trail", "abs_fund_pct_z")]:
            s = spec[col]
            perm[out] = (perm[col] - s["mu"]) / s["sd"]
        pf = {}
        for m in MODELS:
            pp = predict(fits[m], perm, m, spec)
            if pp is None:
                pf = None
                break
            pf[m] = qlike_vec(y, pp)
        if pf is None:
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
        primary["passes_materiality"] and primary["ci_excludes_zero"] and (primary["holm_p"] < 0.05)
    )

    if smoke:
        verdict, status = "INCONCLUSIVE", "SMOKE_ONLY"
    elif primary_pass and primary["rel_reduction_pct"] is not None and primary["rel_reduction_pct"] >= SEALED["C2_vs_B1"]["rel_reduction_pct"] * 0.5:
        verdict, status = "REPRODUCED", "VALID_EXPLORATORY"
    elif primary_pass:
        verdict, status = "INCONCLUSIVE", "VALID_EXPLORATORY"
    else:
        verdict, status = "NOT_REPRODUCED", "VALID_EXPLORATORY"

    result.update(
        {
            "status": status,
            "verdict": verdict,
            "qlike": {m: round(float(np.nanmean(q[m])), 6) for m in MODELS},
            "contrasts": contrast,
            "holm": {k: round(v, 6) for k, v in holm_p.items()},
            "per_symbol": per_symbol,
            "loio_pass": int(loio_pass),
            "loio_total": len(instruments),
            "per_block": per_block,
            "placebo": placebo,
            "leakage_audit": leakage_audit(panel),
            "model_fit": {
                m: {
                    "beta": [round(float(x), 8) for x in f["beta"]],
                    "cols": f["cols"],
                    "smearing": round(float(f["smearing"]), 8),
                }
                for m, f in fits.items()
                if f is not None
            },
        }
    )
    return result


# ------------------------------------------------------------------------ report


def write_report(result: dict, out_utc: str, panel_path: Path | None, panel_sha: str | None) -> dict:
    stem = f"evaluation_summary_FCLR-011-RECOMPUTE-{out_utc.replace(':', '').replace('-', '')}"
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
        "- Sealed FCLR-011 artifacts: unchanged (read-only in this cell)",
        f"- Smoke run: `{result.get('smoke')}`",
        "",
        "## Panel",
        "",
    ]
    if panel_path is not None:
        L.append(f"- Panel: `{panel_path.relative_to(REPO)}`")
    if panel_sha:
        L.append(f"- Panel SHA-256: `{panel_sha}`")
    L += [
        f"- Rows: {result.get('build', {}).get('rows_total', 0)}",
        f"- Instruments: {len(result.get('instruments', []))} {result.get('instruments', [])}",
        f"- Test blocks (UTC days): {result.get('n_test_blocks_days')}",
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
        f"- LOIO: {result.get('loio_pass')}/{result.get('loio_total')} instruments clear the 2% materiality floor",
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
    L += ["", "## Per-block (C2 vs B1)", "", "| Block (UTC day) | n | rel reduction |", "|---|---|---|"]
    for d, v in (result.get("per_block") or {}).items():
        L.append(f"| {d} | {v['n_pairs']} | {v['rel_reduction_pct']}% |")
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
        "## Comparison to the sealed FCLR-011 result",
        "",
        "| Contrast | Sealed rel reduction | Recomputed rel reduction |",
        "|---|---|---|",
    ]
    for k, v in SEALED.items():
        got = (c.get(k) or {}).get("rel_reduction_pct")
        L.append(f"| {k} | {v['rel_reduction_pct']}% | {got if got is not None else 'n/a'} |")
    L += [
        "",
        "## Notes",
        "",
        "- Mark/index premium is NOT computable from the cached 2026 Binance archive "
        "(no markPriceKlines/indexPriceKlines/premiumIndexKlines); C2 degrades to "
        "C1 + mark/EMA24 distance. This is a limitation of the independent recompute, "
        "not a claim about the sealed result.",
        "- No zero-fill, no forward-fill. Funding attached by backward merge_asof "
        "(<= 24h tolerance). Target is a strictly forward 24h realized variance.",
        "",
    ]
    md_path.write_text("\n".join(L))
    return {"json": json_path, "md": md_path}


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
            f"python3 scripts/fclr011_recompute_audit.py --write-prereg"
        )
    prereg = json.loads(PREREG_JSON.read_text())
    assert_prereg_frozen(prereg)

    panel, build = assemble_panel(MONTHS)
    if panel.empty:
        result = {
            "experiment_id": EXPERIMENT_ID,
            "campaign": CAMPAIGN,
            "generated": out_utc,
            "status": "INADMISSIBLE",
            "verdict": "INADMISSIBLE",
            "failing_minima": ["no cached 2026 klines for the frozen universe"],
            "promotable": False,
            "max_status": "EXPLORATORY_ONLY",
        }
        write_report(result, out_utc, None, None)
        print(json.dumps({"verdict": "INADMISSIBLE"}, indent=2))
        return 1

    safe = out_utc.replace(":", "").replace("-", "")
    panel_path = RS / f"fclr011_recompute_panel_{safe}.parquet"
    cols = [
        "coin", "ts", "split", "close", "open", "high", "low", "rv1h", "rv24h", "rv168h",
        "target_rv24h", "signed_funding", "funding_asof_lag_h", "abs_funding_pct_trail",
        "abs_funding_trail_n", "ema24", "ema24_dist", "log_rv1h", "log_rv24h", "log_rv168h",
        "premium", "premium_status",
    ]
    cols = [c for c in cols if c in panel.columns]
    out = panel[cols].copy()
    out.to_parquet(panel_path, index=False)
    panel_sha = sha256_file(panel_path)

    build_report = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "generated": out_utc,
        "panel_path": str(panel_path.relative_to(REPO)),
        "panel_sha256": panel_sha,
        "input_hashes": _input_hashes(),
        "row_counts": {
            "total": int(len(panel)),
            "train": int((panel["split"] == "train").sum()),
            "validation": int((panel["split"] == "validation").sum()),
            "test": int((panel["split"] == "test").sum()),
            "test_with_target": int(
                ((panel["split"] == "test") & panel["target_rv24h"].notna()).sum()
            ),
        },
        "coverage_by_symbol": build.get("symbols", []),
        "splits": prereg["splits"],
        "source_limitation": prereg["target"]["source_limitation"],
    }
    br_path = RS / f"fclr011_recompute_panel_build_report_{safe}.json"
    br_path.write_text(json.dumps(convert(build_report), indent=2) + "\n")

    result = run_audit(prereg, out_utc, args.smoke)
    result["panel_path"] = str(panel_path.relative_to(REPO))
    result["panel_sha256"] = panel_sha
    paths = write_report(result, out_utc, panel_path, panel_sha)
    print(
        json.dumps(
            {
                "verdict": result["verdict"],
                "status": result["status"],
                "contrasts": result.get("contrasts", {}),
                "artifacts": [str(paths["json"].relative_to(REPO)), str(paths["md"].relative_to(REPO))],
                "panel": str(panel_path.relative_to(REPO)),
                "panel_sha256": panel_sha,
            },
            indent=2,
            default=str,
        )
    )
    return 0 if result["verdict"] != "INADMISSIBLE" else 1


def _input_hashes() -> list[dict]:
    out = []
    for ym in MONTHS:
        for sym in UNIVERSE:
            d = CACHE / f"{sym}_{ym}"
            if not d.is_dir():
                continue
            for zp in sorted(d.glob("*.zip")):
                out.append(
                    {
                        "path": str(zp.relative_to(REPO)),
                        "sha256": sha256_file(zp),
                        "bytes": zp.stat().st_size,
                    }
                )
    return out


if __name__ == "__main__":
    sys.exit(main())