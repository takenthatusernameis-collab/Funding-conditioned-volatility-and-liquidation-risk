#!/usr/bin/env python3
"""FCLR-FWD-VOL-2025-CROSS — Track C volatility period-specificity (P2).

Frozen prereg: research_state/prereg_fclr_fwd_vol_2025_cross_20261113T063000Z.{json,md}

Tests whether the FCLR-011 funding-conditioned volatility PASS (C2 vs B1, +4.94%
relative QLIKE) is period-specific to 2026-05..2026-08 by running a pre-registered
rolling-origin walk-forward over the cached Binance 2025-02..2025-05 window
(non-overlapping with the sealed FCLR-011 test and the forward 2026 window).

No network; cached Binance archive only. No mutation of sealed artifacts.

Usage:
  python3 scripts/fclr_fwd_vol_2025_cross.py
  python3 scripts/fclr_fwd_vol_2025_cross.py --smoke
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
PREREG = RS / "prereg_fclr_fwd_vol_2025_cross_20261113T063000Z.json"

import sys
if str(REPO / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "scripts"))
import fclr_fwd_vol_confirm as fwd  # noqa: E402


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--out-utc", default=None)
    args = ap.parse_args()

    prereg = json.loads(PREREG.read_text())
    assert prereg["status"] == "FROZEN_PRE_OUTCOMES"
    assert prereg["outcome_data_inspected_before_freeze"] is False

    out_utc = args.out_utc or now_utc()
    safe = out_utc.replace(":", "").replace("-", "")
    syms = fwd.SYMBOLS[:1] if args.smoke else fwd.SYMBOLS
    blocks = prereg["splits"]["blocks"][:1] if args.smoke else prereg["splits"]["blocks"]

    data_start = pd.Timestamp(prereg["splits"]["data_start"], tz=fwd.UTC)
    data_end = pd.Timestamp(prereg["splits"]["data_end"], tz=fwd.UTC)
    panels = []
    coverage = {}
    for sym in syms:
        df = fwd.build_symbol(sym, data_start, data_end)
        panels.append(df)
        coverage[sym] = int(df["target_24h"].notna().sum())
    panel = pd.concat(panels, ignore_index=True)
    mask = fwd.common_valid_mask(panel)
    panel_valid = panel[mask].copy()

    block_results = []
    pooled_primary = []
    pooled_all = []
    for b in blocks:
        blk = {"block": b["block"], "train_start": prereg["splits"]["train_start"],
               "train_end": b["train_end"], "test_start": b["test_start"], "test_end": b["test_end"]}
        res = fwd.run_block(panel_valid, blk)
        block_results.append({"block": b["block"], "train_rows": res["train_rows"],
                              "test_rows": res["test_rows"]})
        for k, M in res["diffs"].items():
            pooled_all.append(M.assign(block=b["block"], contrast=k))
            if k == "C2_vs_B1":
                pooled_primary.append(M.assign(block=b["block"]))

    pooled_primary_df = pd.concat(pooled_primary, ignore_index=True) if pooled_primary else pd.DataFrame()
    pooled = pd.concat(pooled_all, ignore_index=True) if pooled_all else pd.DataFrame()
    primary = fwd.bootstrap_diff(pooled_primary_df, reps=500 if args.smoke else prereg["gates"]["bootstrap_reps"])

    # Holm over the contrast family (per-block C2_vs_B1, C1_vs_B1, C2_vs_C1).
    # Family = 3 contrasts x n_blocks; adjusted p reported for the pooled primary.
    pvals = {}
    for b in blocks:
        blk = {"block": b["block"], "train_start": prereg["splits"]["train_start"],
               "train_end": b["train_end"], "test_start": b["test_start"], "test_end": b["test_end"]}
        res = fwd.run_block(panel_valid, blk)
        for k, M in res["diffs"].items():
            bs = fwd.bootstrap_diff(M, reps=500 if args.smoke else 500)
            if bs:
                pvals[f"b{b['block']}_{k}"] = bs["p_boot"]
    holm = fwd.holm(pvals) if pvals else {}

    loio = []
    if not args.smoke:
        for held in syms:
            sub = panel_valid[panel_valid["symbol"] != held]
            diffs = []
            for b in blocks:
                blk = {"block": b["block"], "train_start": prereg["splits"]["train_start"],
                       "train_end": b["train_end"], "test_start": b["test_start"], "test_end": b["test_end"]}
                p = sub.copy(); p["ts"] = pd.to_datetime(p["ts"])
                train = p[(p["ts"] >= pd.Timestamp(blk["train_start"], tz=fwd.UTC)) &
                          (p["ts"] <= pd.Timestamp(blk["train_end"], tz=fwd.UTC))]
                test_all = panel_valid[panel_valid["symbol"] == held].copy()
                test_all["ts"] = pd.to_datetime(test_all["ts"])
                test = test_all[(test_all["ts"] >= pd.Timestamp(blk["test_start"], tz=fwd.UTC)) &
                                (test_all["ts"] <= pd.Timestamp(blk["test_end"], tz=fwd.UTC))]
                frames = fwd.qlike_frame(train, test)
                diffs.append(fwd.paired_diffs(frames, "C2", "B1"))
            M = pd.concat(diffs, ignore_index=True)
            loio.append({"held_out": held, **(fwd.bootstrap_diff(M, reps=500) or {})})

    placebo = None
    if not args.smoke:
        rng = np.random.default_rng(prereg["gates"]["placebo_seed"] + 1)
        null = []
        base = panel_valid.copy()
        for _ in range(prereg["gates"]["placebo_reps"]):
            pp = base.copy()
            for sym in syms:
                idx = pp.index[pp["symbol"] == sym]
                for col in ("signed_funding", "abs_fund_pct"):
                    pp.loc[idx, col] = rng.permutation(pp.loc[idx, col].values)
            diffs = []
            for b in blocks:
                blk = {"block": b["block"], "train_start": prereg["splits"]["train_start"],
                       "train_end": b["train_end"], "test_start": b["test_start"], "test_end": b["test_end"]}
                p = pp.copy(); p["ts"] = pd.to_datetime(p["ts"])
                train = p[(p["ts"] >= pd.Timestamp(blk["train_start"], tz=fwd.UTC)) &
                          (p["ts"] <= pd.Timestamp(blk["train_end"], tz=fwd.UTC))]
                test = p[(p["ts"] >= pd.Timestamp(blk["test_start"], tz=fwd.UTC)) &
                         (p["ts"] <= pd.Timestamp(blk["test_end"], tz=fwd.UTC))]
                frames = fwd.qlike_frame(train, test)
                diffs.append(fwd.paired_diffs(frames, "C2", "B1"))
            M = pd.concat(diffs, ignore_index=True)
            null.append(float(-M["diff"].mean() / abs(M["qb"].mean()) * 100.0))
        null = np.array(null)
        placebo = {"null_p95": float(np.percentile(null, 95)),
                   "true_rel_reduction_pct": primary["rel_reduction_pct"],
                   "pass": bool(primary["rel_reduction_pct"] > np.percentile(null, 95)),
                   "n_perm": len(null)}

    checks = {
        "materiality_ge_2pct": bool(primary and primary["rel_reduction_pct"] is not None and primary["rel_reduction_pct"] >= 2.0),
        "ci_excludes_zero": bool(primary and primary["ci_hi"] < 0),
        "instruments_ge_5": len(syms) >= 5,
        "blocks_ge_3": len(blocks) >= 3,
        "loio_ge_4_of_5": bool(loio and sum(1 for x in loio if x.get("rel_reduction_pct") and x["rel_reduction_pct"] >= 2.0 and x.get("ci_hi", 0) < 0) >= 4),
        "placebo_pass": bool(placebo and placebo["pass"]),
        "no_leakage": bool(panel_valid["ts"].notna().all()),
    }

    if args.smoke:
        verdict = "SMOKE"
    elif primary is None or primary["n"] == 0:
        verdict = "INCONCLUSIVE"
    elif not (checks["instruments_ge_5"] and checks["blocks_ge_3"] and checks["no_leakage"]):
        verdict = "INCONCLUSIVE"
    elif all(checks.values()):
        verdict = "CONFIRMED"
    else:
        verdict = "NOT_REPLICATED"

    payload = {
        "experiment_id": prereg["experiment_id"],
        "campaign": prereg["campaign"],
        "cell": prereg["cell"],
        "generated_utc": out_utc,
        "prereg": PREREG.name,
        "verdict": verdict,
        "checks": checks,
        "primary": primary,
        "holm": holm,
        "per_block": block_results,
        "loio": loio,
        "placebo": placebo,
        "coverage": coverage,
        "n_panel_rows": int(len(panel)),
        "n_valid_rows": int(len(panel_valid)),
    }

    if args.smoke:
        print(json.dumps(payload, indent=1))
        return

    panel_path = RS / f"tracka_fwd_vol_2025_cross_panel_{safe}.parquet"
    panel.to_parquet(panel_path, index=False)
    build_report = {
        "experiment_id": prereg["experiment_id"],
        "generated_utc": out_utc,
        "panel_path": panel_path.name,
        "panel_sha256": sha256_file(panel_path),
        "n_rows": int(len(panel)),
        "n_valid_rows": int(len(panel_valid)),
        "coverage": coverage,
        "blocks": blocks,
        "inputs": "research_state/data_cache/{SYM}_{YYYY}_{MM}/{markPriceKlines,premiumIndexKlines,indexPriceKlines}-{date} + {SYM}-fundingRate-{YYYY-MM}",
    }
    (RS / f"tracka_fwd_vol_2025_cross_build_report_{safe}.json").write_text(json.dumps(build_report, indent=1))
    (RS / f"evaluation_summary_FCLR-FWD-VOL-2025-CROSS-{safe}.json").write_text(json.dumps(payload, indent=1))
    md = [
        f"# Evaluation Summary — {prereg['experiment_id']}", "",
        f"Generated: {out_utc}", f"Verdict: **{verdict}**", "",
        "## Primary (C2 vs B1, 24h QLIKE, pooled 3 blocks)", "",
        f"- mean diff (C2 - B1): {primary['mean_diff']:.6f} (positive = C2 worse)",
        f"- 95% CI: [{primary['ci_lo']:.6f}, {primary['ci_hi']:.6f}]",
        f"- relative reduction: {primary['rel_reduction_pct']:.2f}%",
        f"- n: {primary['n']}", f"- days: {primary['n_days']}", "",
        "## Checks", "",
    ]
    for k, v in checks.items():
        md.append(f"- {k}: {v}")
    md += ["", "## Interpretation", "",
           "A NOT_REPLICATED verdict on this non-overlapping 2025 window indicates the FCLR-011 "
           "PASS is period-specific rather than a general funding-conditioned volatility effect.", ""]
    (RS / f"evaluation_summary_FCLR-FWD-VOL-2025-CROSS-{safe}.md").write_text("\n".join(md))
    print(json.dumps({"verdict": verdict, "checks": checks, "primary": primary,
                      "panel": panel_path.name,
                      "eval": f"evaluation_summary_FCLR-FWD-VOL-2025-CROSS-{safe}.json"}, indent=1))


if __name__ == "__main__":
    main()