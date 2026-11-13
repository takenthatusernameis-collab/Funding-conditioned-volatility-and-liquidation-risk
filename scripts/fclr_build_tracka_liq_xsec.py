#!/usr/bin/env python3
"""Build + evaluate Arm B: TRACKA-LIQ-XSEC-20261112T201536Z (P2, exploratory, max EXPLORATORY_ONLY).

Frozen prereg: research_state/prereg_tracka_liq_xsec_20261112T201536Z.{json,md}
  promotable=false; never promotable; never overrides sealed verdicts.

Inputs:
  - liquidations: research_state/data_cache/ironflow_events/2025-05..2025-10.parquet
                  (observed ironflow labels, CC BY 4.0; verified cache)
  - candles_1h / funding: research_state/data_cache/ironflow_bulk/<dataset>/<YYYY-MM>.parquet
                  (2025-05..2025-10; fetched bulk cache, CC BY 4.0, unauthenticated)

Panel: coin x 24h UTC bucket over burn-in 2025-05-25..2025-10-07 (never scored)
and test blocks 0/1/2 = 2025-10-08..2025-11-06, 2025-11-13..2025-12-12,
2025-12-19..2026-01-17.

Universe (coverage-only, frozen ex ante; only label EXISTENCE counts):
  native perps (market endswith -PERP, no ':') with >=20 observed liquidation-days,
  >=100 observed liquidation events (2025-05-25..2026-01-17), and complete hourly
  candle+funding coverage over 2025-10-08..2026-01-17. >=5 coins required.

Features at bucket start d (data at or before d only):
  rv24h: trailing 24h realized variance from hourly closes ending at d
  funding_rate / abs_funding / premium: latest settled at or before d (as-of)
  score_d = z(funding_rate) + z(abs_funding), cross-sectional z within bucket d

Targets: next-24h bucket (d, d+1day]: t1_liq_count (observed event count),
t1_liq_notional (observed notional USD).

Estimand: Spearman rank IC(score_d, t1_liq_count at d+1), per 30-day block on the
pooled cross-section, mean IC across blocks + pooled IC. Secondary: top-k minus
bottom-k mean next-24h notional spread (k = 10% of universe, floor 5) per block.

Inference: within-bucket permutation of the score across coins (1000 reps,
seed 20261112); null 5th/95th percentiles; empirical p per block and pooled.
Materiality: |mean IC| >= 0.05 AND spread sign consistent in >=2/3 blocks.

Decision: EXPLORATORY_SIGNAL -> reported EXPLORATORY_ONLY, never promoted;
EXPLORATORY_NULL -> null preserved with exact failing minima;
INADMISSIBLE -> <5 coins or <3 blocks, emit infeasibility with exact minima.

Outputs:
  research_state/tracka_liq_xsec_panel_<UTC>.parquet
  research_state/tracka_liq_xsec_panel_build_report_<UTC>.json
  research_state/evaluation_summary_TRACKA-LIQ-XSEC-<UTC>.md
  research_state/evaluation_summary_TRACKA-LIQ-XSEC-<UTC>.json
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
from scipy.stats import spearmanr

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
EVENTS = RS / "data_cache" / "ironflow_events"
BULK = RS / "data_cache" / "ironflow_bulk"
PREREG_PATH = RS / "prereg_tracka_liq_xsec_20261112T201536Z.json"
UTC = timezone.utc
SEED = 20261112
PERM_REPS = 1000
ALPHA = 0.05
MATERIALITY_IC = 0.05

COVERAGE_START = "2025-05-25 00:00:00"
COVERAGE_END = "2026-01-17 23:00:00"
TEST_START = "2025-10-08 00:00:00"
TEST_END = "2026-01-17 23:00:00"
BLOCKS = [
    (0, "2025-10-08 00:00:00", "2025-11-06 23:00:00"),
    (1, "2025-11-13 00:00:00", "2025-12-12 23:00:00"),
    (2, "2025-12-19 00:00:00", "2026-01-17 23:00:00"),
]
MIN_LIQ_DAYS = 20
MIN_LIQ_EVENTS = 100
MIN_COINS = 5


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


def ts(s: str) -> pd.Timestamp:
    return pd.Timestamp(s, tz="UTC")


def main() -> None:
    t0 = time.time()
    prereg = json.loads(PREREG_PATH.read_text())
    assert prereg["status"] == "FROZEN_PRE_OUTCOMES"
    assert prereg.get("promotable") is False
    assert prereg["outcome_data_inspected_before_freeze"] is False

    # ---- 1. Load observed liquidation labels (existing verified cache) ----
    # The frozen prereg's "Data" table lists labels 2025-05..2025-10, but its Splits
    # table scores test blocks 0/1/2 through 2026-01-17, whose next-24h targets need
    # labels through 2026-01-17. Those months are cached in ironflow_events/ and are
    # inside the admissible label ceiling (2025-05-25..2026-10-31) -- NOT in the
    # reserved (2026-01-18..2026-04-30) or sealed (2026-05-01..2026-10-31) windows.
    # The day filter below (<= 2026-01-17) guarantees no reserved-window timestamp is
    # ever used. Design (universe rule, splits, score, inference) is unchanged.
    label_months = [f"{y:04d}-{m:02d}" for y in (2025, 2026) for m in range(1, 13)
                    if "2025-05" <= f"{y:04d}-{m:02d}" <= "2026-01"]
    label_frames, label_sums = [], {}
    for m in label_months:
        p = EVENTS / f"{m}.parquet"
        if not p.exists():
            fail(f"missing cached label object {p}")
        label_sums[f"ironflow_events_{m}.parquet"] = sha256_file(p)
        df = pd.read_parquet(p)
        df["market"] = df["market"].astype(str)
        label_frames.append(df)
    labels = pd.concat(label_frames, ignore_index=True)
    labels = labels[labels["market"].str.endswith("-PERP")]
    labels = labels[~labels["market"].str.contains(":")]
    labels["coin"] = labels["market"].str.replace("-PERP", "", regex=False)
    labels["day"] = labels["timestamp"].dt.tz_convert("UTC").dt.floor("24h")
    labels = labels[(labels["day"] >= ts(COVERAGE_START)) & (labels["day"] <= ts(COVERAGE_END))]

    # ---- 2. Load candles + funding for universe/eligibility and features ----
    # The frozen prereg's "Data" table lists 2025-05..2025-10 (the originally planned
    # fetch range), but its Splits table and coverage-only universe rule require
    # complete hourly candle+funding coverage over the full test window
    # 2025-10-08..2026-01-17. The bulk manifest fetched 2025-05..2026-04, so load every
    # month that intersects the test window. Design (universe rule, splits, score,
    # inference) is unchanged; only the input load range is extended to satisfy the
    # frozen coverage predicate.
    months = [f"{y:04d}-{m:02d}" for y in (2025, 2026) for m in range(1, 13)
              if "2025-10" <= f"{y:04d}-{m:02d}" <= "2026-01"]
    candles_frames, funding_frames = [], []
    candle_sums, funding_sums = {}, {}
    for m in months:
        pc = BULK / "candles_1h" / f"{m}.parquet"
        pf = BULK / "funding" / f"{m}.parquet"
        if not pc.exists() or not pf.exists():
            fail(f"missing bulk cache object for {m}")
        candle_sums[f"candles_1h/{m}.parquet"] = sha256_file(pc)
        funding_sums[f"funding/{m}.parquet"] = sha256_file(pf)
        c = pd.read_parquet(pc); c["market"] = c["market"].astype(str)
        f = pd.read_parquet(pf); f["market"] = f["market"].astype(str)
        candles_frames.append(c)
        funding_frames.append(f)
    candles = pd.concat(candles_frames, ignore_index=True)
    funding = pd.concat(funding_frames, ignore_index=True)
    # ironflow/hyperliquid-funding settlement timestamps carry sub-second jitter
    # (observed ~98.6% of rows at e.g. 00:00:00.104Z). Floor to the hourly grid so
    # funding aligns with the candle grid; the sealed panel builders do the same.
    funding["timestamp"] = funding["timestamp"].dt.floor("1h")

    # ---- 3. Universe selection (ex ante; only label existence counts) ----
    # tz-aware grid: cached timestamps are tz-aware UTC (e.g. 2025-05-25 14:00:00+00:00);
    # a naive grid would silently reindex to all-NaN and pass zero coverage.
    test_grid = pd.date_range(ts(TEST_START), ts(TEST_END), freq="1h")
    coin_stats = {}
    for coin, g in labels.groupby("coin"):
        coin_stats[coin] = {
            "liq_days": int(g["day"].nunique()),
            "liq_events": int(len(g)),
        }
    eligible = [c for c, s in coin_stats.items()
                if s["liq_days"] >= MIN_LIQ_DAYS and s["liq_events"] >= MIN_LIQ_EVENTS]

    # complete hourly candle+funding coverage over the test window
    coverage_ok = []
    for coin in eligible:
        c = candles[candles["market"] == coin + "-PERP"].set_index("timestamp")["close"]
        f = funding[funding["market"] == coin + "-PERP"].set_index("timestamp")["funding_rate"]
        ch = int(c.reindex(test_grid).notna().sum())
        fh = int(f.reindex(test_grid).notna().sum())
        if ch == len(test_grid) and fh == len(test_grid):
            coverage_ok.append(coin)
    universe = sorted(coverage_ok)
    n_coins = len(universe)
    if n_coins < MIN_COINS:
        fail(f"INADMISSIBLE: universe {n_coins} coins < {MIN_COINS} required")

    # ---- 4. Features per bucket ----
    closes = candles[candles["market"].isin([c + "-PERP" for c in universe])][
        ["timestamp", "market", "close"]].copy()
    closes["coin"] = closes["market"].str.replace("-PERP", "", regex=False)
    close_piv = closes.pivot_table(index="timestamp", columns="coin", values="close", aggfunc="first")
    close_piv = close_piv.reindex(test_grid)
    rets = np.log(close_piv / close_piv.shift(1))
    # trailing 24h RV: 24 returns over closes[d-24..d]
    rv24 = (rets ** 2).rolling(24, min_periods=24).sum()

    def asof_hourly(col: str) -> pd.DataFrame:
        fr = funding[["timestamp", "market", col]].copy()
        fr["hour"] = fr["timestamp"].dt.floor("1h")
        fr = fr[fr["market"].isin([c + "-PERP" for c in universe])]
        fr = fr.sort_values(["market", "hour"]).drop_duplicates(["market", "hour"], keep="last")
        result = pd.DataFrame(index=test_grid, columns=universe, dtype=float)
        for coin in universe:
            s = fr[fr["market"] == coin + "-PERP"].set_index("hour")[col].reindex(test_grid)
            result[coin] = s.where(s.notna()).ffill()
        return result

    funding_rate = asof_hourly("funding_rate")
    premium = asof_hourly("premium")
    abs_funding = funding_rate.abs()

    # ---- 5. Labels per coin x bucket: next-24h observed events / notional ----
    label_by_coin = {}
    for coin in universe:
        g = labels[labels["coin"] == coin].sort_values("timestamp")
        label_by_coin[coin] = g

    def bucket_label(coin: str, day: pd.Timestamp):
        g = label_by_coin[coin]
        lo = day + pd.Timedelta(days=1)
        hi = lo + pd.Timedelta(days=1)
        m = (g["timestamp"] >= lo) & (g["timestamp"] < hi)
        sub = g.loc[m]
        return int(len(sub)), float(sub["notional_usd"].sum())

    # scored buckets: day in test window, day+1 within same block
    rows = []
    for bid, bstart, bend in BLOCKS:
        bs, be = ts(bstart), ts(bend)
        days = pd.date_range(bs, be - pd.Timedelta(days=1), freq="24h")
        for day in days:
            if day + pd.Timedelta(days=1) > be:
                continue
            for coin in universe:
                cnt, notl = bucket_label(coin, day)
                rows.append({"coin": coin, "bucket": day, "block": bid,
                             "t1_liq_count": cnt, "t1_liq_notional": notl})
    panel = pd.DataFrame(rows)
    panel["day"] = panel["bucket"]

    # features aligned at bucket start
    feat = panel[["coin", "bucket"]].copy()
    feat["rv24h"] = [rv24.loc[b, c] if b in rv24.index and c in rv24.columns else np.nan
                     for b, c in zip(feat["bucket"], feat["coin"])]
    feat["funding_rate"] = [funding_rate.loc[b, c] if b in funding_rate.index else np.nan
                            for b, c in zip(feat["bucket"], feat["coin"])]
    feat["premium"] = [premium.loc[b, c] if b in premium.index else np.nan
                       for b, c in zip(feat["bucket"], feat["coin"])]
    feat["abs_funding"] = feat["funding_rate"].abs()
    panel = panel.merge(feat, on=["coin", "bucket"], how="left")
    panel["t1_liq_notional"] = panel["t1_liq_notional"].fillna(0.0)
    panel["t1_liq_count"] = panel["t1_liq_count"].fillna(0).astype(int)

    # ---- 6. Cross-sectional funding score within bucket ----
    def zcol(s: pd.Series) -> pd.Series:
        if s.std() <= 0:
            return pd.Series(0.0, index=s.index)
        return (s - s.mean()) / s.std()

    panel["score"] = panel.groupby("bucket")[["funding_rate", "abs_funding"]].transform(zcol).sum(axis=1)
    panel = panel[panel["score"].notna() & panel["rv24h"].notna() & panel["funding_rate"].notna()].copy()

    # ---- 7. Estimand: Spearman IC per block + pooled ----
    def spearman_ic(sub):
        if len(sub) < 3 or sub["score"].nunique() < 2 or sub["t1_liq_count"].nunique() < 2:
            return None, len(sub)
        ic, p = spearmanr(sub["score"].to_numpy(), sub["t1_liq_count"].to_numpy())
        return (float(ic) if np.isfinite(ic) else None), int(len(sub))

    per_block = {}
    all_ics = []
    for b in range(3):
        sub = panel[panel["block"] == b]
        ic, n = spearman_ic(sub)
        per_block[f"block_{b}"] = {"ic": ic, "n": int(len(sub)), "n_pairs": n}
        if ic is not None:
            all_ics.append(ic)
    pooled_ic, pooled_n = spearman_ic(panel)
    mean_ic = float(np.mean(all_ics)) if all_ics else None

    # ---- 8. Secondary: top-k minus bottom-k notional spread per block ----
    k = max(MIN_COINS, int(math.ceil(0.10 * n_coins))) if False else max(MIN_COINS, int(round(0.10 * n_coins)))
    import math
    k = max(MIN_COINS, int(math.ceil(0.10 * n_coins)))
    spread_per_block = {}
    for b in range(3):
        sub = panel[panel["block"] == b]
        if len(sub) < 2 * k:
            spread_per_block[f"block_{b}"] = None
            continue
        top = sub.nlargest(k, "score")["t1_liq_notional"].mean()
        bot = sub.nsmallest(k, "score")["t1_liq_notional"].mean()
        spread_per_block[f"block_{b}"] = {"top_k_mean_notional": float(top),
                                          "bottom_k_mean_notional": float(bot),
                                          "spread": float(top - bot),
                                          "k": int(k)}
    spread_signs = [v["spread"] > 0 for v in spread_per_block.values() if v is not None]
    sign_consistent = len(spread_signs) >= 2 and sum(spread_signs) >= 2

    # ---- 9. Permutation inference (within-bucket score shuffle, 1000 reps, seed 20261112) ----
    rng = np.random.RandomState(SEED)
    null_mean_ics = []
    null_per_block = {f"block_{b}": [] for b in range(3)}
    score_by_bucket = {b: panel[panel["bucket"] == b]["score"].to_numpy() for b in panel["bucket"].unique()}
    labels_by_bucket = {b: panel[panel["bucket"] == b]["t1_liq_count"].to_numpy() for b in panel["bucket"].unique()}
    block_of_bucket = dict(zip(panel["bucket"], panel["block"]))
    buckets = sorted(score_by_bucket.keys())
    for _ in range(PERM_REPS):
        block_ics = []
        for b in buckets:
            s = score_by_bucket[b].copy()
            rng.shuffle(s)
            y = labels_by_bucket[b]
            if s.nunique() if hasattr(s, "nunique") else len(np.unique(s)) < 2 or len(np.unique(y)) < 2:
                continue
            ic, _ = spearmanr(s, y)
            if np.isfinite(ic):
                block_ics.append(ic)
                null_per_block[f"block_{block_of_bucket[b]}"].append(ic)
        if block_ics:
            null_mean_ics.append(float(np.mean(block_ics)))
    null_mean_ics = np.array(null_mean_ics)
    obs_mean = mean_ic if mean_ic is not None else 0.0
    if len(null_mean_ics):
        p_pooled = float((np.abs(null_mean_ics) >= np.abs(obs_mean)).mean())
        null_lo = float(np.percentile(null_mean_ics, 5))
        null_hi = float(np.percentile(null_mean_ics, 95))
    else:
        p_pooled = None
        null_lo = None
        null_hi = None
    per_block_p = {}
    for b in range(3):
        arr = np.array(null_per_block[f"block_{b}"])
        obs = per_block[f"block_{b}"]["ic"]
        if len(arr) and obs is not None:
            per_block_p[f"block_{b}"] = float((np.abs(arr) >= np.abs(obs)).mean())
        else:
            per_block_p[f"block_{b}"] = None

    materiality_met = bool(mean_ic is not None and abs(mean_ic) >= MATERIALITY_IC and sign_consistent)
    if materiality_met:
        decision = "EXPLORATORY_SIGNAL"
    elif n_coins < MIN_COINS or len([b for b in range(3) if per_block[f"block_{b}"]["ic"] is not None]) < 3:
        decision = "INADMISSIBLE"
    else:
        decision = "EXPLORATORY_NULL"

    # ---- 10. Emit artifacts ----
    stamp = now_utc()
    panel_path = RS / f"tracka_liq_xsec_panel_{stamp}.parquet"
    report_path = RS / f"tracka_liq_xsec_panel_build_report_{stamp}.json"
    panel.to_parquet(panel_path, index=False)

    build_report = {
        "experiment_id": "TRACKA-LIQ-XSEC-20261112T201536Z",
        "campaign": "FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z",
        "arm": "B",
        "prereg": str(PREREG_PATH.relative_to(REPO)),
        "generated_utc": stamp,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
        "universe_size": n_coins,
        "universe_min_instruments_required": MIN_COINS,
        "selection_rule": "coverage-only + label existence (>=20 liq-days, >=100 liq events, complete hourly candle+funding over test window)",
        "windows_utc": {
            "burn_in_never_scored": f"{COVERAGE_START} .. 2025-10-07 23:00:00",
            "test_blocks": [[b, s, e] for b, s, e in BLOCKS],
            "reserved_never_touched": "2026-01-18 00:00:00 .. 2026-04-30 23:00:00",
            "sealed_never_read": "2026-05-01 00:00:00 .. 2026-10-31 23:59:59",
        },
        "inputs_hashes": {"labels": label_sums, "candles": candle_sums, "funding": funding_sums},
        "panel": {"path": str(panel_path.relative_to(REPO)), "sha256": sha256_file(panel_path),
                  "n_rows": int(len(panel)), "n_buckets": int(panel["bucket"].nunique())},
        "panel_sha256": sha256_file(panel_path),
        "feature_rule": "score_d = z(funding_rate) + z(abs_funding), cross-sectional z within bucket",
        "k": int(k),
        "runtime_seconds": round(time.time() - t0, 2),
    }
    report_path.write_text(json.dumps(build_report, indent=2) + "\n")

    lines = [f"# Evaluation Summary — TRACKA-LIQ-XSEC-{stamp}",
             f"**Generated (UTC):** {stamp}",
             "**Campaign:** `FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z` — Arm B (P2, exploratory)",
             f"**Prereg:** `research_state/prereg_tracka_liq_xsec_20261112T201536Z.json` (frozen 2026-11-12T20:15:36Z, `promotable=false`, max `EXPLORATORY_ONLY`)",
             f"**Panel:** `research_state/tracka_liq_xsec_panel_{stamp}.parquet`",
             f"**Decision:** `{decision}` (reported as EXPLORATORY_ONLY; never promotable)", "",
             "## Universe (coverage-only, label-existence only)"]
    lines.append(f"- eligible coins (>= {MIN_LIQ_DAYS} liq-days, >= {MIN_LIQ_EVENTS} liq events): {len(eligible)}")
    lines.append(f"- complete hourly candle+funding coverage over test window: {n_coins} coins")
    lines.append(f"- universe = {universe[:12]} ... ({n_coins} total)")
    lines.append("## Primary estimand: Spearman rank IC(score_d, next-24h liquidation event count)")
    lines.append(f"- mean IC across blocks = {mean_ic if mean_ic is not None else 'NA'}")
    lines.append(f"- pooled IC = {pooled_ic if pooled_ic is not None else 'NA'} (n={pooled_n})")
    lines.append("| Block | IC | n_rows | p_value (permutation) |")
    for b in range(3):
        pb = per_block[f"block_{b}"]
        lines.append(f"| {b} | {pb['ic'] if pb['ic'] is not None else 'NA'} | {pb['n']} | {per_block_p[f'block_{b}']} |")
    lines.append(f"- permutation null (1000 reps, seed 20261112): 5th={null_lo}, 95th={null_hi}, pooled p={p_pooled}")
    lines.append("## Secondary: top-k minus bottom-k next-24h notional spread (k = 10% universe, floor 5)")
    for b in range(3):
        v = spread_per_block[f"block_{b}"]
        if v is None:
            lines.append(f"- block {b}: k=NA, top=NA, bottom=NA, spread=NA")
        else:
            lines.append(f"- block {b}: k={v['k']}, top={v['top_k_mean_notional']:.2f}, "
                         f"bottom={v['bottom_k_mean_notional']:.2f}, spread={v['spread']:.2f}")
    lines.append(f"- spread sign consistent (positive) in >= 2/3 blocks: {sign_consistent} ({sum(spread_signs)}/{len(spread_signs)})")
    lines.append("## Materiality: |mean IC| >= 0.05 AND spread sign consistent >= 2/3 blocks")
    lines.append(f"- |mean IC| = {abs(mean_ic) if mean_ic is not None else 'NA'} >= 0.05: {bool(mean_ic is not None and abs(mean_ic) >= MATERIALITY_IC)}")
    lines.append(f"- decision = {decision}")
    lines.append(f"- If EXPLORATORY_NULL: null preserved; exact failing minima: mean_IC={mean_ic}, materiality floor 0.05, sign consistency {sum(spread_signs)}/3")
    eval_md_path = RS / f"evaluation_summary_TRACKA-LIQ-XSEC-{stamp}.md"
    eval_md_path.write_text("\n".join(lines) + "\n")

    eval_json = {
        "experiment_id": "TRACKA-LIQ-XSEC-20261112T201536Z",
        "campaign": "FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z",
        "arm": "B",
        "decision": decision,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
        "universe_size": n_coins,
        "universe": universe,
        "selection": {"eligible_by_counts": len(eligible), "coverage_ok": n_coins,
                      "min_liq_days": MIN_LIQ_DAYS, "min_liq_events": MIN_LIQ_EVENTS},
        "primary": {"mean_ic": mean_ic, "pooled_ic": pooled_ic, "pooled_n": pooled_n,
                    "p_value_pooled_permutation": p_pooled,
                    "null_5th": null_lo, "null_95th": null_hi,
                    "per_block": per_block, "per_block_p": per_block_p,
                    "permutation_reps": PERM_REPS, "seed": SEED},
        "secondary": {"k": int(k), "spread_per_block": spread_per_block,
                      "sign_consistent": sign_consistent},
        "materiality": {"floor_ic": MATERIALITY_IC, "abs_mean_ic": abs(mean_ic) if mean_ic is not None else None,
                        "met": materiality_met},
        "verdict": decision,
        "panel_sha256": sha256_file(panel_path),
        "build_report": str(report_path.relative_to(REPO)),
        "generated_utc": stamp,
    }
    eval_json_path = RS / f"evaluation_summary_TRACKA-LIQ-XSEC-{stamp}.json"
    eval_json_path.write_text(json.dumps(eval_json, indent=2) + "\n")

    print(json.dumps({
        "decision": decision,
        "n_coins": n_coins,
        "mean_ic": mean_ic,
        "pooled_ic": pooled_ic,
        "p_value_pooled": p_pooled,
        "sign_consistent": sign_consistent,
        "panel": str(panel_path),
        "eval_md": str(eval_md_path),
        "eval_json": str(eval_json_path),
        "build_report": str(report_path),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
