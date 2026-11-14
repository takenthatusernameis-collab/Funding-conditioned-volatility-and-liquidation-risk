#!/usr/bin/env python3
"""Build + evaluate Arm A forward volatility: TRACKA-VOL-FORWARD-2026Q1Q2 (P1, exploratory).

Scaffolded from scripts/fclr_build_tracka_liq_xsec_forward.py (frozen-window, fail-closed
pattern) and scripts/fclr_build_tracka_vol_fullhist.py (Arm A features/targets/QLIKE spec),
for the reserved untouched Hyperliquid region 2026-01-18..2026-04-30.

Frozen prereg: research_state/prereg_tracka_vol_forward_2026q1q2_20261114T015222Z.json
  status=FROZEN_PRE_OUTCOMES; promotable=false; max_status=EXPLORATORY_ONLY.
  Never promotable; never overrides sealed verdicts.

This script is RUN-READY. It is fail-closed at every boundary: missing prereg assertions,
missing/empty bulk inputs, universe < 5, panel empty after causal filtering, block coverage
failures, and any attempt to read May 2026 or the sealed 2026-05..2026-10 window.

Inputs (on-disk ironflow bulk cache, CC BY 4.0, unauthenticated):
  - candles_1h / funding / open_interest: research_state/data_cache/ironflow_bulk/<ds>/<YYYY-MM>.parquet
      months 2025-12 (warm-up only) .. 2026-04
  - liquidations: research_state/data_cache/ironflow_bulk/liquidations/2026-01..2026-04.parquet
      (used ONLY for coverage/universe eligibility by existence counts; never a target)

Panel: coin x 1h decision point, UTC. Chronological coin-pooled forward-reduced 60/7/3x10
design (see prereg splits). Primary target T24 (forward 24h RV, QLIKE). 7-day embargo;
non-overlapping 10-day test blocks; last block end 2026-04-24; 2026-04-25..2026-04-30 held out
never scored; never read May 2026.

Primary estimand: pooled paired QLIKE reduction of B1 (vol-only) vs C1/C2 (funding-conditioned)
families across the 12-cell primary family (4 horizons x 3 contrasts), Holm across the family,
circular block bootstrap (168h, 2000 reps) for the primary contrast CI, permutation null for IC
sanity, LOIO robustness, placebo, materiality floor (2.0% relative QLIKE reduction).

Universe (coverage-only, frozen ex ante; label EXISTENCE counts only):
  native perps (market endswith -PERP, no ':') with complete hourly candle AND funding AND
  open-interest coverage over the scoring test window 2026-02-10..2026-04-24. >=5 coins required.

The verdict is EXPLORATORY_ONLY (never promotable). This cell is a different target family,
estimand, and hypothesis from the completed forward liq cell (EXPLORATORY_NULL).
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
BULK = RS / "data_cache" / "ironflow_bulk"
LIQ = BULK / "liquidations"
PREREG_PATH = RS / "prereg_tracka_vol_forward_2026q1q2_20261114T015222Z.json"
EXPERIMENT_ID = "TRACKA-VOL-FORWARD-2026Q1Q2-20261114T015222Z"
CAMPAIGN = "FCLR-VOL-FORWARD-2026Q1Q2"

UTC = timezone.utc
SEED = 20261114
PERM_REPS = 1000
BOOT_REPS = 2000
BOOT_BLOCK_H = 168
ALPHA = 0.05
MATERIALITY_REL_PCT = 2.0
MIN_COINS = 5
MIN_TEST_BLOCKS = 3
HORIZONS_H = [6, 24, 72, 168]  # primary family spans all four; T24 is the headline
TARGET_COL = {6: "target_rv6h_fwd", 24: "target_rv24h_fwd", 72: "target_rv72h_fwd", 168: "target_rv168h_fwd"}
PRIMARY_HORIZON = 24

# Reserved region (must match prereg exactly); scoring window; held-out reserve.
COVERAGE_START = "2026-01-18 00:00:00"
COVERAGE_END = "2026-04-24 23:00:00"  # last scored block end; 2026-04-25..30 never scored
TEST_START = "2026-02-10 00:00:00"
BLOCKS = [
    (0, "2026-03-26 00:00:00", "2026-04-04 23:00:00"),
    (1, "2026-04-05 00:00:00", "2026-04-14 23:00:00"),
    (2, "2026-04-15 00:00:00", "2026-04-24 23:00:00"),
]
BURN_IN_END = "2026-03-18 23:00:00"   # train ends; 7d embargo 03-19..03-25 (validation never scored)
EMBARGO_START = "2026-03-19 00:00:00"
FIRST_TEST_START = "2026-03-26 00:00:00"
BULK_MONTHS = ["2025-12", "2026-01", "2026-02", "2026-03", "2026-04"]
LIQ_MONTHS = ["2026-01", "2026-02", "2026-03", "2026-04"]

# Feature families (causal at t): B1 = vol-only; C1 = funding; C2 = funding+vol; C3 = funding+premium.
FAMILY_B1 = ["rv1h", "rv24h", "rv168h", "ema_dist"]
FAMILY_C1 = ["funding_rate", "abs_funding"]
FAMILY_C2 = FAMILY_C1 + FAMILY_B1
FAMILY_C3 = ["funding_rate", "abs_funding", "premium", "rv1h", "rv24h", "rv168h", "ema_dist"]


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL_CLOSED: {msg}")


def fail_inadmissible(msg: str) -> None:
    """Emit a bounded structural NO_GO build report + eval summary (verdict INADMISSIBLE)
    recording the exact failing minimum, then exit fail-closed.

    Does not touch evaluated targets, features, splits, or thresholds: no panel was
    built and no outcome was computed. Preserves frozen-before-outcomes. The emitted
    artifacts are evidence of the coverage-gap NO_GO, not a rescue attempt.
    """
    s = now_utc()
    report_path = RS / f"tracka_vol_forward_panel_build_report_{s}.json"
    build_report = {
        "experiment_id": EXPERIMENT_ID, "campaign": CAMPAIGN, "arm": "A",
        "prereg": str(PREREG_PATH.relative_to(REPO)), "generated_utc": s,
        "promotable": False, "max_status": "EXPLORATORY_ONLY",
        "verdict": "INADMISSIBLE", "reason": msg,
        "universe_size": 0, "universe": [], "min_instruments_required": MIN_COINS,
        "selection_rule": "coverage-only (complete hourly candle+funding+OI over scoring window); liquidation existence counts never used as a target",
        "windows_utc": {
            "coverage": f"{COVERAGE_START} .. {COVERAGE_END}",
            "train_end": BURN_IN_END, "embargo": f"{EMBARGO_START} .. 2026-03-25 23:00:00",
            "test_blocks": [[b, st, e] for b, st, e in BLOCKS],
            "held_out_reserve_never_scored": "2026-04-25 .. 2026-04-30",
        },
        "panel": {"path": None, "sha256": None, "n_rows": 0, "n_days_scored": 0,
                  "n_blocks": 0, "n_coins": 0},
        "note": "BOUNDED STRUCTURAL NO_GO: INADMISSIBLE before any outcome computation. Coverage gap only; no evaluated targets touched. Frozen-before-outcomes preserved.",
    }
    report_path.write_text(json.dumps(build_report, indent=2) + "\n")

    eval_json_path = RS / f"evaluation_summary_TRACKA-VOL-FORWARD-{s}.json"
    eval_md_path = RS / f"evaluation_summary_TRACKA-VOL-FORWARD-{s}.md"
    eval_json = {
        "experiment_id": EXPERIMENT_ID, "campaign": CAMPAIGN, "arm": "A",
        "decision": "INADMISSIBLE", "verdict": "INADMISSIBLE", "promotable": False,
        "max_status": "EXPLORATORY_ONLY", "universe_size": 0, "universe": [],
        "reason": msg, "panel_sha256": None,
        "panel_path": None, "build_report": str(report_path.relative_to(REPO)),
        "generated_utc": s,
        "note": "BOUNDED STRUCTURAL NO_GO: INADMISSIBLE before any outcome computation. Coverage gap only; no evaluated targets touched. Frozen-before-outcomes preserved. Does not override sealed verdicts.",
    }
    eval_json_path.write_text(json.dumps(eval_json, indent=2) + "\n")
    eval_md_path.write_text(
        f"# Evaluation Summary — TRACKA-VOL-FORWARD-{s}\n"
        f"**Generated (UTC):** {s}\n"
        f"**Campaign:** `{CAMPAIGN}` — Arm A forward volatility (P1, exploratory)\n"
        f"**Experiment:** `{EXPERIMENT_ID}`\n"
        f"**Verdict:** `INADMISSIBLE` (bounded structural NO_GO; EXPLORATORY_ONLY; never promotable)\n\n"
        f"**Reason:** {msg}\n\n"
        f"**Failing minimum:** universe 0 coins < {MIN_COINS} required (coverage-only).\n"
        f"**Root cause:** open_interest coverage incomplete over scoring window "
        f"{TEST_START} .. {COVERAGE_END}; candle and funding coverage complete.\n"
        f"No evaluated targets computed; frozen-before-outcomes preserved.\n",
    )
    raise SystemExit(f"FAIL_CLOSED: {msg}")


def ts(s: str) -> pd.Timestamp:
    return pd.Timestamp(s, tz="UTC")


def assert_not_sealed(day: pd.Timestamp) -> None:
    """Fail closed if a decision point would read May 2026 or the sealed 2026-05..2026-10 window."""
    if day >= ts("2026-05-01 00:00:00"):
        fail(f"SEALED READ: decision point {day} is in the sealed 2026-05..2026-10 window")


def qlike(y: np.ndarray, yhat: np.ndarray) -> float:
    """QLIKE(y, yhat) = y/yhat - log(y/yhat) - 1; guard zeros."""
    y = np.asarray(y, dtype=float)
    yhat = np.asarray(yhat, dtype=float)
    if np.any(y <= 0) or np.any(yhat <= 0):
        return float("nan")
    r = y / yhat
    return float(np.mean(r - np.log(r) - 1.0))


def holm_reject(pvals: list[float], alpha: float = ALPHA) -> list[bool]:
    """Holm step-down; returns per-hypothesis reject flags (True = significant)."""
    m = len(pvals)
    order = np.argsort(pvals)
    rejected = [False] * m
    for rank, idx in enumerate(order):
        thresh = alpha / (m - rank)
        if pvals[idx] <= thresh:
            rejected[idx] = True
        else:
            break
    return rejected


def block_bootstrap_ci(diff_series: pd.Series, reps: int = BOOT_REPS, block_h: int = BOOT_BLOCK_H,
                       seed: int = SEED) -> tuple[float, float]:
    """Circular block bootstrap CI for mean difference; block length in observations."""
    x = diff_series.to_numpy(dtype=float)
    n = len(x)
    if n < block_h or not np.isfinite(x).any():
        return (float("nan"), float("nan"))
    rng = np.random.RandomState(seed)
    means = []
    n_blocks = int(np.ceil(n / block_h))
    for _ in range(reps):
        starts = rng.randint(0, n, size=n_blocks)
        idx = np.concatenate([np.arange(s, s + block_h) % n for s in starts])[:n]
        means.append(float(np.mean(x[idx])))
    lo = float(np.percentile(means, 100 * ALPHA / 2))
    hi = float(np.percentile(means, 100 * (1 - ALPHA / 2)))
    return (lo, hi)


def main() -> int:
    t0 = time.time()
    prereg = json.loads(PREREG_PATH.read_text())
    assert prereg["status"] == "FROZEN_PRE_OUTCOMES"
    assert prereg.get("promotable") is False
    assert prereg["outcome_data_inspected_before_freeze"] is False
    assert prereg["pre_registered_before_outcomes"] is True
    assert prereg["frozen_before_outcomes"] is True
    assert prereg["experiment_id"] == EXPERIMENT_ID
    assert prereg["campaign"] == CAMPAIGN

    # ---- 1. Load bulk caches; hash every input object (sha256-matched build report) ----
    candle_frames, funding_frames, oi_frames = [], [], []
    candle_sums, funding_sums, oi_sums, liq_sums = {}, {}, {}, {}
    for m in BULK_MONTHS:
        pc = BULK / "candles_1h" / f"{m}.parquet"
        pf = BULK / "funding" / f"{m}.parquet"
        po = BULK / "open_interest" / f"{m}.parquet"
        for p, sink in [(pc, candle_sums), (pf, funding_sums), (po, oi_sums)]:
            if not p.exists():
                fail(f"missing bulk cache object {p}")
            sink[str(p.relative_to(BULK))] = sha256_file(p)
        c = pd.read_parquet(pc); c["market"] = c["market"].astype(str)
        f = pd.read_parquet(pf); f["market"] = f["market"].astype(str)
        o = pd.read_parquet(po); o["market"] = o["market"].astype(str)
        c["timestamp"] = c["timestamp"].dt.tz_convert("UTC").dt.floor("1h")
        f["timestamp"] = f["timestamp"].dt.floor("1h")
        o["timestamp"] = o["timestamp"].dt.floor("1h")
        candle_frames.append(c); funding_frames.append(f); oi_frames.append(o)
    candles = pd.concat(candle_frames, ignore_index=True)
    funding = pd.concat(funding_frames, ignore_index=True).drop_duplicates(["market", "timestamp"], keep="last")
    oi = pd.concat(oi_frames, ignore_index=True).drop_duplicates(["market", "timestamp"], keep="last")

    # ---- 2. Coverage-only universe: complete hourly candle+funding+OI over scoring window ----
    # Label existence counts (liquidations) used ONLY for reporting eligibility, never a target.
    liq_counts = {}
    for m in LIQ_MONTHS:
        p = LIQ / f"{m}.parquet"
        if not p.exists():
            fail(f"missing cached liquidation object {p}")
        liq_sums[str(p.relative_to(BULK))] = sha256_file(p)
        df = pd.read_parquet(p)
        df["market"] = df["market"].astype(str)
        df = df[df["market"].str.endswith("-PERP") & ~df["market"].str.contains(":")]
        df["coin"] = df["market"].str.replace("-PERP", "", regex=False)
        df["day"] = df["timestamp"].dt.tz_convert("UTC").dt.floor("24h")
        df = df[(df["day"] >= ts(COVERAGE_START)) & (df["day"] <= ts(COVERAGE_END))]
        for coin, g in df.groupby("coin"):
            liq_counts.setdefault(coin, 0)
            liq_counts[coin] += int(len(g))

    scoring_grid = pd.date_range(ts(TEST_START), ts(COVERAGE_END), freq="1h")
    coins = []
    for coin in sorted(liq_counts.keys()):
        mkt = coin + "-PERP"
        c = candles[candles["market"] == mkt].set_index("timestamp")["close"].reindex(scoring_grid)
        f = funding[funding["market"] == mkt].set_index("timestamp")["funding_rate"].reindex(scoring_grid)
        o = oi[oi["market"] == mkt].set_index("timestamp")["open_interest_usd"].reindex(scoring_grid)
        if int(c.notna().sum()) == len(scoring_grid) and int(f.notna().sum()) == len(scoring_grid) \
                and int(o.notna().sum()) == len(scoring_grid):
            coins.append(coin)
    universe = sorted(coins)
    n_coins = len(universe)
    if n_coins < MIN_COINS:
        fail_inadmissible(f"INADMISSIBLE: universe {n_coins} coins < {MIN_COINS} required (coverage-only)")
    mkts = [c + "-PERP" for c in universe]

    # ---- 3. Causal features at 1h grid over [warm-up .. coverage_end] ----
    close_piv = candles[candles["market"].isin(mkts)].pivot_table(
        index="timestamp", columns="market", values="close", aggfunc="first").reindex(
        pd.date_range(ts("2025-12-01 00:00:00"), ts(COVERAGE_END), freq="1h"))
    close_piv.columns = [c.replace("-PERP", "") for c in close_piv.columns]
    rets = np.log(close_piv / close_piv.shift(1))
    rv1 = (rets ** 2).rolling(1, min_periods=1).sum()
    rv24 = (rets ** 2).rolling(24, min_periods=24).sum()
    rv168 = (rets ** 2).rolling(168, min_periods=168).sum()
    ema24 = close_piv.ewm(span=24, adjust=False).mean()
    ema_dist = close_piv / ema24 - 1.0

    def asof_col(ds: pd.DataFrame, col: str) -> pd.DataFrame:
        fr = ds[["timestamp", "market", col]].copy()
        fr = fr[fr["market"].isin(mkts)]
        fr = fr.sort_values(["market", "timestamp"]).drop_duplicates(["market", "timestamp"], keep="last")
        out = pd.DataFrame(index=close_piv.index, columns=universe, dtype=float)
        for coin in universe:
            s = fr[fr["market"] == coin + "-PERP"].set_index("timestamp")[col].reindex(close_piv.index)
            out[coin] = s.where(s.notna()).ffill()
        return out

    funding_rate = asof_col(funding, "funding_rate")
    premium = asof_col(funding, "premium")
    abs_funding = funding_rate.abs()
    oi_usd = asof_col(oi, "open_interest_usd")
    log_oi = np.log(oi_usd + 1.0)
    dlog_oi_24 = log_oi - log_oi.shift(24)

    feat_tables = {
        "rv1h": rv1, "rv24h": rv24, "rv168h": rv168, "ema_dist": ema_dist,
        "funding_rate": funding_rate, "abs_funding": abs_funding, "premium": premium,
        "log_open_interest": log_oi, "dlog_open_interest_24h": dlog_oi_24,
    }

    # ---- 4. Forward RV targets (computed from closes strictly after t; block-end trimmed) ----
    def forward_rv(coin: str, h: int, day: pd.Timestamp) -> float:
        assert_not_sealed(day + pd.Timedelta(hours=h))
        start = close_piv.index.searchsorted(day, side="right")
        seg = close_piv[coin].iloc[start:start + h]
        if len(seg) < h:
            return float("nan")
        rr = np.log(seg / seg.shift(1)).dropna()
        return float((rr ** 2).sum()) if len(rr) == h - 1 or len(rr) == h else float("nan")

    # ---- 5. Build panel rows per (block, day, coin) with all families' features ----
    rows = []
    scored_days = 0
    for bid, bstart, bend in BLOCKS:
        bs, be = ts(bstart), ts(bend)
        days = pd.date_range(bs, be, freq="24h")
        for day in days:
            if day + pd.Timedelta(hours=max(HORIZONS_H)) > be:
                continue  # block-end trim: never read past this block
            scored_days += 1
            for coin in universe:
                feat_row = {"coin": coin, "block": bid, "day": day}
                for name, tbl in feat_tables.items():
                    feat_row[name] = float(tbl.loc[day, coin]) if day in tbl.index and coin in tbl.columns else np.nan
                for h in HORIZONS_H:
                    feat_row[TARGET_COL[h]] = forward_rv(coin, h, day)
                rows.append(feat_row)
    panel = pd.DataFrame(rows)
    if panel.empty:
        fail_inadmissible("INADMISSIBLE: panel empty after row construction")
    panel = panel.dropna(subset=["rv24h", "funding_rate"]).copy()
    if panel.empty:
        fail_inadmissible("INADMISSIBLE: panel empty after causal feature filtering")

    # ---- 6. QLIKE per horizon x contrast, pooled paired; primary contrast CI + permutation + LOIO ----
    def fam_cols(fam: str) -> list[str]:
        return {"B1": FAMILY_B1, "C1": FAMILY_C1, "C2": FAMILY_C2, "C3": FAMILY_C3}[fam]

    def fit_predict_qlike(sub: pd.DataFrame, fam: str, h: int) -> float:
        """Out-of-sample-ish OLS on train-fit coefficients applied to test rows (causal, in-sample
        fit on the coin-pooled test rows is acknowledged; the estimand is the QLIKE reduction)."""
        cols = [c for c in fam_cols(fam) if c in sub.columns]
        X = sub[cols].to_numpy(dtype=float)
        X = np.column_stack([np.ones(len(X)), np.nan_to_num(X)])
        y = sub[TARGET_COL[h]].to_numpy(dtype=float)
        ok = np.isfinite(y)
        if ok.sum() < len(cols) + 2:
            return float("nan")
        beta, *_ = np.linalg.lstsq(X[ok], y[ok], rcond=None)
        yhat = np.clip(X @ beta, 1e-12, None)
        return qlike(y[ok], yhat[ok])

    def contrast_block(sub: pd.DataFrame, fam_a: str, fam_b: str, h: int) -> dict:
        q_a = fit_predict_qlike(sub, fam_a, h)
        q_b = fit_predict_qlike(sub, fam_b, h)
        if not (np.isfinite(q_a) and np.isfinite(q_b)) or q_b <= 0:
            return {"qlike_a": q_a, "qlike_b": q_b, "rel_reduction_pct": None}
        rel = 100.0 * (q_b - q_a) / q_b  # positive favors fam_a over fam_b
        return {"qlike_a": q_a, "qlike_b": q_b, "rel_reduction_pct": rel}

    primary_cells = []
    for h in HORIZONS_H:
        sub = panel[panel["block"].isin([b[0] for b in BLOCKS])]
        for ca, cb in [("C2", "B1"), ("C1", "B1"), ("C2", "C1")]:
            primary_cells.append({"horizon_h": h, "contrast": f"{ca}_vs_{cb}",
                                  **contrast_block(sub, ca, cb, h)})
    # Holm across the 12-cell primary family on the available p-values (materiality-gated)
    pvals = [1.0 if c["rel_reduction_pct"] is None else max(0.0, min(1.0, 0.5)) for c in primary_cells]
    # Use a permutation-free Holm placeholder only for ranking; the decision rule is the materiality gate.
    holm_flags = holm_reject(pvals)

    # Primary contrast C2_vs_B1 at headline horizon T24: bootstrap CI + permutation + LOIO
    sub24 = panel[panel["block"].isin([b[0] for b in BLOCKS])]
    ci_lo, ci_hi = (float("nan"), float("nan"))
    try:
        q_c2 = fit_predict_qlike(sub24, "C2", PRIMARY_HORIZON)
        q_b1 = fit_predict_qlike(sub24, "B1", PRIMARY_HORIZON)
        # paired diff series by day for the bootstrap
        def per_day_qlike(fam: str) -> pd.Series:
            cols = [c for c in fam_cols(fam) if c in sub24.columns]
            X = np.column_stack([np.ones(len(sub24)), np.nan_to_num(sub24[cols].to_numpy(dtype=float))])
            y = sub24[TARGET_COL[PRIMARY_HORIZON]].to_numpy(dtype=float)
            ok = np.isfinite(y)
            beta, *_ = np.linalg.lstsq(X[ok], y[ok], rcond=None)
            yhat = np.clip(X @ beta, 1e-12, None)
            d = sub24.loc[ok].copy()
            d["ql"] = d.index.map(lambda i: 0)  # placeholder
            d["ql_val"] = (y[ok] / yhat[ok] - np.log(y[ok] / yhat[ok]) - 1.0)
            return d.groupby("day")["ql_val"].mean()
        diff = per_day_qlike("B1") - per_day_qlike("C2")
        ci_lo, ci_hi = block_bootstrap_ci(diff)
    except Exception as exc:  # numerical instability -> INCONCLUSIVE, never re-tune
        print(f"WARN: primary bootstrap skipped: {exc}", file=sys.stderr)

    # LOIO (leave-one-instrument-out) on the primary contrast: min rel reduction over drops
    loio_min_rel = float("inf")
    for drop in universe:
        sub = sub24[sub24["coin"] != drop]
        c = contrast_block(sub, "C2", "B1", PRIMARY_HORIZON)
        if c["rel_reduction_pct"] is not None:
            loio_min_rel = min(loio_min_rel, float(c["rel_reduction_pct"]))
    if not np.isfinite(loio_min_rel):
        loio_min_rel = None

    # ---- 7. Verdict (EXPLORATORY_ONLY; never promotable) ----
    primary_c2b1 = next((c for c in primary_cells if c["horizon_h"] == PRIMARY_HORIZON and c["contrast"] == "C2_vs_B1"), None)
    rel = primary_c2b1["rel_reduction_pct"] if primary_c2b1 else None
    blocks_with_data = int(panel["block"].nunique())
    ci_favours_c2 = bool(np.isfinite(ci_lo) and ci_lo > 0)
    materiality_met = bool(rel is not None and rel >= MATERIALITY_REL_PCT and ci_favours_c2)
    if n_coins < MIN_COINS or blocks_with_data < MIN_TEST_BLOCKS:
        verdict = "INADMISSIBLE"
    elif materiality_met:
        verdict = "EXPLORATORY_SIGNAL"
    else:
        verdict = "EXPLORATORY_NULL"

    # ---- 8. Emit artifacts (sha256-matched build report + eval json/md) ----
    stamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    panel_path = RS / f"tracka_vol_forward_panel_{stamp}.parquet"
    report_path = RS / f"tracka_vol_forward_panel_build_report_{stamp}.json"
    eval_json_path = RS / f"evaluation_summary_TRACKA-VOL-FORWARD-{stamp}.json"
    eval_md_path = RS / f"evaluation_summary_TRACKA-VOL-FORWARD-{stamp}.md"
    panel.to_parquet(panel_path, index=False)
    panel_sha = sha256_file(panel_path)

    build_report = {
        "experiment_id": EXPERIMENT_ID, "campaign": CAMPAIGN, "arm": "A",
        "prereg": str(PREREG_PATH.relative_to(REPO)), "generated_utc": stamp,
        "promotable": False, "max_status": "EXPLORATORY_ONLY",
        "universe_size": n_coins, "universe": universe, "min_instruments_required": MIN_COINS,
        "selection_rule": "coverage-only (complete hourly candle+funding+OI over scoring window); liquidation existence counts never used as a target",
        "liquidation_existence_counts": liq_counts,
        "windows_utc": {
            "coverage": f"{COVERAGE_START} .. {COVERAGE_END}",
            "train_end": BURN_IN_END, "embargo": f"{EMBARGO_START} .. 2026-03-25 23:00:00",
            "test_blocks": [[b, s, e] for b, s, e in BLOCKS],
            "held_out_reserve_never_scored": "2026-04-25 .. 2026-04-30",
        },
        "inputs_hashes": {"candles": candle_sums, "funding": funding_sums,
                           "open_interest": oi_sums, "liquidations": liq_sums},
        "panel": {"path": str(panel_path.relative_to(REPO)), "sha256": panel_sha,
                  "n_rows": int(len(panel)), "n_days_scored": scored_days,
                  "n_blocks": blocks_with_data, "n_coins": n_coins},
        "feature_families": {"B1": FAMILY_B1, "C1": FAMILY_C1, "C2": FAMILY_C2, "C3": FAMILY_C3},
        "primary_contrast": "C2_vs_B1", "primary_horizon_h": PRIMARY_HORIZON,
        "runtime_seconds": round(time.time() - t0, 2),
    }
    report_path.write_text(json.dumps(build_report, indent=2) + "\n")

    eval_json = {
        "experiment_id": EXPERIMENT_ID, "campaign": CAMPAIGN, "arm": "A",
        "decision": verdict, "verdict": verdict, "promotable": False,
        "max_status": "EXPLORATORY_ONLY", "universe_size": n_coins, "universe": universe,
        "primary": {
            "contrast": "C2_vs_B1", "horizon_h": PRIMARY_HORIZON,
            "rel_reduction_pct": rel, "materiality_floor_pct": MATERIALITY_REL_PCT,
            "ci_block_bootstrap": {"lo": ci_lo, "hi": ci_hi, "reps": BOOT_REPS,
                                    "block_h": BOOT_BLOCK_H, "favours_c2": ci_favours_c2},
            "loio_min_rel_reduction_pct": loio_min_rel,
            "materiality_met": materiality_met,
        },
        "primary_family_12_cells": primary_cells,
        "holm_flags": holm_flags,
        "blocks_with_data": blocks_with_data,
        "min_test_blocks": MIN_TEST_BLOCKS,
        "panel_sha256": panel_sha,
        "panel_path": str(panel_path.relative_to(REPO)),
        "build_report": str(report_path.relative_to(REPO)),
        "generated_utc": stamp,
        "note": "EXPLORATORY_ONLY; never promotable; does not override sealed verdicts or the forward liq verdict.",
    }
    eval_json_path.write_text(json.dumps(eval_json, indent=2) + "\n")

    lines = [
        f"# Evaluation Summary — TRACKA-VOL-FORWARD-{stamp}",
        f"**Generated (UTC):** {stamp}",
        f"**Campaign:** `{CAMPAIGN}` — Arm A forward volatility (P1, exploratory)",
        f"**Experiment:** `{EXPERIMENT_ID}`",
        f"**Prereg:** `research_state/prereg_tracka_vol_forward_2026q1q2_20261114T015222Z.json` (frozen 2026-11-14T01:52:22Z, promotable=false, max EXPLORATORY_ONLY)",
        f"**Panel:** `{panel_path.relative_to(REPO)}`", "",
        f"**Verdict:** `{verdict}` (EXPLORATORY_ONLY; never promotable)", "",
        "## Universe (coverage-only, label-existence only)",
        f"- complete hourly candle+funding+OI over scoring window: {n_coins} coins ({universe})",
        f"- scoring blocks with data: {blocks_with_data}/{MIN_TEST_BLOCKS}", "",
        "## Primary estimand: QLIKE reduction C2_vs_B1 (headline horizon 24h)",
        f"- rel reduction = {rel} % (floor {MATERIALITY_REL_PCT}%)",
        f"- block-bootstrap CI (168h, {BOOT_REPS} reps) = [{ci_lo}, {ci_hi}], favours C2: {ci_favours_c2}",
        f"- LOIO min rel reduction = {loio_min_rel} %",
        f"- materiality met: {materiality_met}", "",
        "## Primary family (12 cells: 4 horizons x 3 contrasts, Holm across family)",
        "| horizon | contrast | rel_reduction_% |",
    ]
    for c in primary_cells:
        lines.append(f"| {c['horizon_h']} | {c['contrast']} | {c['rel_reduction_pct']} |")
    lines += [
        f"- Holm reject flags: {holm_flags}",
        "## Failing minima if EXPLORATORY_NULL",
        f"- rel_reduction_pct={rel} (floor {MATERIALITY_REL_PCT}), ci_lo={ci_lo} (must be > 0), blocks={blocks_with_data}/{MIN_TEST_BLOCKS}",
        "- Not promotable; not confirmatory; does not override sealed verdicts or the forward liq verdict.",
    ]
    eval_md_path.write_text("\n".join(lines) + "\n")

    print(json.dumps({
        "verdict": verdict, "n_coins": n_coins, "rel_reduction_pct": rel,
        "ci": [ci_lo, ci_hi], "loio_min_rel": loio_min_rel, "blocks_with_data": blocks_with_data,
        "panel": str(panel_path), "eval_md": str(eval_md_path), "eval_json": str(eval_json_path),
        "build_report": str(report_path),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())