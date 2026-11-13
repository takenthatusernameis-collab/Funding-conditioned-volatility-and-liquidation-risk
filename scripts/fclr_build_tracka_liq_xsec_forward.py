#!/usr/bin/env python3
"""Build + evaluate Arm B forward: TRACKA-LIQ-XSEC-FORWARD-20261113T222859Z (P2, exploratory).

Cloned from scripts/fclr_build_tracka_liq_xsec.py for the frozen forward window.
Frozen prereg: research_state/prereg_tracka_liq_xsec_forward_2026q1q2_20261113T222859Z.json
  promotable=false; never promotable; never overrides sealed verdicts.

Inputs (on-disk ironflow bulk cache, CC BY 4.0, unauthenticated):
  - liquidations: research_state/data_cache/ironflow_bulk/liquidations/2026-01..2026-04.parquet
                  (observed only; no modeled/proxy/synthetic labels)
  - candles_1h / funding: research_state/data_cache/ironflow_bulk/<dataset>/<YYYY-MM>.parquet
                  (2025-12..2026-04; 2025-12 tail for 24h rv warm-up only)

Panel: coin x 24h UTC bucket over burn-in 2026-01-18..2026-02-02 (never scored)
and test blocks 0/1/2 with 7-day embargoes (see prereg). Block end is target
horizon; builder scores start..end-1 day (last scored day 2026-04-29, target
[2026-04-30, 2026-05-01)). Never read May 2026.

Universe (coverage-only, frozen ex ante; only label EXISTENCE counts):
  native perps (market endswith -PERP, no ':') with >=20 observed liquidation-days,
  >=100 observed liquidation events (2026-01-18..2026-04-30), and complete hourly
  candle+funding coverage over 2026-02-10..2026-04-30. >=5 coins required.

Features/score/estimand/inference identical to Arm B TRACKA-LIQ-XSEC-20261112T201536Z.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
EVENTS = RS / "data_cache" / "ironflow_bulk" / "liquidations"
BULK = RS / "data_cache" / "ironflow_bulk"
PREREG_PATH = RS / "prereg_tracka_liq_xsec_forward_2026q1q2_20261113T222859Z.json"
EXPERIMENT_ID = "TRACKA-LIQ-XSEC-FORWARD-20261113T222859Z"
CAMPAIGN = "FCLR-FORWARD-LIQ-2026Q1Q2"

UTC = timezone.utc
SEED = 20261112
PERM_REPS = 1000
ALPHA = 0.05
MATERIALITY_IC = 0.05

COVERAGE_START = "2026-01-18 00:00:00"
COVERAGE_END = "2026-04-30 23:00:00"  # target horizon included; May not read
TEST_START = "2026-02-10 00:00:00"
TEST_END = "2026-04-30 23:00:00"
BLOCKS = [
    (0, "2026-02-10 00:00:00", "2026-03-11 23:00:00"),
    (1, "2026-03-19 00:00:00", "2026-04-03 23:00:00"),
    (2, "2026-04-11 00:00:00", "2026-04-30 23:00:00"),
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
    assert prereg["pre_registered_before_outcomes"] is True
    assert prereg["frozen_before_outcomes"] is True

    # ---- 1. Load observed liquidation labels from bulk cache ----
    label_months = ["2026-01", "2026-02", "2026-03", "2026-04"]
    label_frames, label_sums = [], {}
    for m in label_months:
        p = EVENTS / f"{m}.parquet"
        if not p.exists():
            fail(f"missing cached label object {p}")
        label_sums[f"ironflow_bulk/liquidations/{m}.parquet"] = sha256_file(p)
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
    # 2025-12 tail for 24h rv warm-up only; never read 2025-11 or earlier, never 2026-05+
    months = ["2025-12", "2026-01", "2026-02", "2026-03", "2026-04"]
    candles_frames, funding_frames = [], []
    candle_sums, funding_sums = {}, {}
    for m in months:
        pc = BULK / "candles_1h" / f"{m}.parquet"
        pf = BULK / "funding" / f"{m}.parquet"
        if not pc.exists() or not pf.exists():
            fail(f"missing bulk cache object for {m}")
        candle_sums[f"candles_1h/{m}.parquet"] = sha256_file(pc)
        funding_sums[f"funding/{m}.parquet"] = sha256_file(pf)
        c = pd.read_parquet(pc)
        c["market"] = c["market"].astype(str)
        f = pd.read_parquet(pf)
        f["market"] = f["market"].astype(str)
        candles_frames.append(c)
        funding_frames.append(f)
    candles = pd.concat(candles_frames, ignore_index=True)
    funding = pd.concat(funding_frames, ignore_index=True)
    funding["timestamp"] = funding["timestamp"].dt.floor("1h")

    # ---- 3. Universe selection (ex ante; only label existence counts) ----
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

    # scored buckets: day in test window, day+1 within same block (block end = target horizon)
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

    if panel.empty:
        fail("INADMISSIBLE: panel has 0 rows")

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
    if panel.empty:
        fail("INADMISSIBLE: panel empty after feature filtering")

    # ---- 7. Estimand: Spearman IC per block + pooled ----
    def spearman_ic(sub):
        if len(sub) < 3 or sub["score"].nunique() < 2 or sub["t1_liq_count"].nunique() < 2:
            return None, int(len(sub))
        ic, _ = spearmanr(sub["score"].to_numpy(), sub["t1_liq_count"].to_numpy())
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

    # ---- 9. Permutation inference (within-bucket score shuffle) ----
    rng = np.random.RandomState(SEED)
    null_mean_ics = []
    null_per_block = {f"block_{b}": [] for b in range(3)}
    score_by_bucket = {b: panel[panel["bucket"] == b]["score"].to_numpy() for b in panel["bucket"].unique()}
    labels_by_bucket = {b: panel[panel["bucket"] == b]["t1_liq_count"].to_numpy() for b in panel["bucket"].unique()}
    block_of_bucket = dict(zip(panel["bucket"], panel["block"]))
    buckets = sorted(score_by_bucket.keys())
    for _ in range(PERM_REPS):
        perb = {0: [], 1: [], 2: []}
        for b in buckets:
            s = score_by_bucket[b].copy()
            rng.shuffle(s)
            y = labels_by_bucket[b]
            if len(np.unique(s)) < 2 or len(np.unique(y)) < 2:
                continue
            ic, _ = spearmanr(s, y)
            if np.isfinite(ic):
                perb[block_of_bucket[b]].append(float(ic))
        for b in range(3):
            if perb[b]:
                v = float(np.mean(perb[b]))
                null_per_block[f"block_{b}"].append(v)
        allb = [x for b in range(3) for x in perb[b]]
        if allb:
            null_mean_ics.append(float(np.mean(allb)))
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

    blocks_with_ic = len([b for b in range(3) if per_block[f"block_{b}"]["ic"] is not None])
    materiality_met = bool(mean_ic is not None and abs(mean_ic) >= MATERIALITY_IC and sign_consistent)
    if n_coins < MIN_COINS or blocks_with_ic < 3:
        verdict = "INADMISSIBLE"
    elif materiality_met:
        verdict = "EXPLORATORY_SIGNAL"
    else:
        verdict = "EXPLORATORY_NULL"

    # ---- 10. Emit artifacts ----
    stamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    panel_path = RS / f"tracka_liq_xsec_forward_panel_{stamp}.parquet"
    report_path = RS / f"tracka_liq_xsec_forward_panel_build_report_{stamp}.json"
    eval_json_path = RS / f"evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-{stamp}.json"
    eval_md_path = RS / f"evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-{stamp}.md"

    panel.to_parquet(panel_path, index=False)
    panel_sha = sha256_file(panel_path)

    build_report = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "arm": "B",
        "prereg": str(PREREG_PATH.relative_to(REPO)),
        "generated_utc": stamp,
        "promotable": False,
        "max_status": "EXPLORATORY_ONLY",
        "universe_size": n_coins,
        "universe_min_instruments_required": MIN_COINS,
        "selection_rule": "coverage-only + label existence (>=20 liq-days, >=100 liq events, complete hourly candle+funding over test window)",
        "windows_utc": {
            "burn_in_never_scored": f"{COVERAGE_START} .. 2026-02-02 23:00:00",
            "test_blocks": [[b, s, e] for b, s, e in BLOCKS],
            "scored_decision_days_end": "2026-04-29 00:00:00",
        },
        "inputs_hashes": {"labels": label_sums, "candles": candle_sums, "funding": funding_sums},
        "panel": {"path": str(panel_path.relative_to(REPO)), "sha256": panel_sha,
                  "n_rows": int(len(panel)), "n_buckets": int(panel["bucket"].nunique())},
        "panel_sha256": panel_sha,
        "feature_rule": "score_d = z(funding_rate) + z(abs_funding), cross-sectional z within bucket",
        "k": int(k),
        "runtime_seconds": round(time.time() - t0, 2),
    }
    report_path.write_text(json.dumps(build_report, indent=2) + "\n")

    lines = [
        f"# Evaluation Summary — TRACKA-LIQ-XSEC-FORWARD-{stamp}",
        f"**Generated (UTC):** {stamp}",
        f"**Campaign:** `{CAMPAIGN}` — Arm B forward (P2, exploratory)",
        f"**Experiment:** `{EXPERIMENT_ID}`",
        f"**Prereg:** `research_state/prereg_tracka_liq_xsec_forward_2026q1q2_20261113T222859Z.json` (frozen 2026-11-13T22:28:59Z, promotable=false, max EXPLORATORY_ONLY)",
        f"**Panel:** `{panel_path.relative_to(REPO)}`",
        f"**Verdict:** `{verdict}` (EXPLORATORY_ONLY; never promotable)", "",
        "## Universe (coverage-only, label-existence only)",
        f"- eligible coins (>= {MIN_LIQ_DAYS} liq-days, >= {MIN_LIQ_EVENTS} liq events): {len(eligible)}",
        f"- complete hourly candle+funding coverage over test window: {n_coins} coins",
        f"- universe (first 12): {universe[:12]} ... ({n_coins} total)", "",
        "## Primary estimand: Spearman rank IC(score_d, next-24h liquidation event count)",
        f"- mean IC across blocks = {mean_ic if mean_ic is not None else 'NA'}",
        f"- pooled IC = {pooled_ic if pooled_ic is not None else 'NA'} (n={pooled_n})",
        "| Block | IC | n_rows | p_value (permutation) |",
    ]
    for b in range(3):
        pb = per_block[f"block_{b}"]
        lines.append(f"| {b} | {pb['ic'] if pb['ic'] is not None else 'NA'} | {pb['n']} | {per_block_p[f'block_{b}']} |")
    lines += [
        f"- permutation null (1000 reps, seed 20261112): 5th={null_lo}, 95th={null_hi}, pooled p={p_pooled}",
        "## Secondary: top-k minus bottom-k next-24h notional spread",
    ]
    for b in range(3):
        v = spread_per_block[f"block_{b}"]
        if v is None:
            lines.append(f"- block {b}: spread=NA")
        else:
            lines.append(f"- block {b}: k={v['k']}, top={v['top_k_mean_notional']:.2f}, bottom={v['bottom_k_mean_notional']:.2f}, spread={v['spread']:.2f}")
    lines += [
        f"- spread sign consistent (positive) in >= 2/3 blocks: {sign_consistent} ({sum(spread_signs)}/{len(spread_signs)})",
        "## Materiality / Decision",
        f"- |mean IC| = {abs(mean_ic) if mean_ic is not None else 'NA'} >= 0.05: {bool(mean_ic is not None and abs(mean_ic) >= MATERIALITY_IC)}",
        f"- verdict = {verdict}",
        f"- failing minima if EXPLORATORY_NULL: mean_IC={mean_ic}, floor 0.05, sign consistency {sum(spread_signs)}/3",
        "- Not promotable; not confirmatory; does not override sealed verdicts.",
    ]
    eval_md_path.write_text("\n".join(lines) + "\n")

    eval_json = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "arm": "B",
        "decision": verdict,
        "verdict": verdict,
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
        "panel_sha256": panel_sha,
        "panel_path": str(panel_path.relative_to(REPO)),
        "build_report": str(report_path.relative_to(REPO)),
        "generated_utc": stamp,
        "blocks_with_ic": blocks_with_ic,
    }
    eval_json_path.write_text(json.dumps(eval_json, indent=2) + "\n")

    print(json.dumps({
        "verdict": verdict,
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
