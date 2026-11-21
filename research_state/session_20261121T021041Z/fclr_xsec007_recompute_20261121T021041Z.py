#!/usr/bin/env python3
"""
FCLR-XSEC-007 independent reproducibility recompute.

Independently recomputes the cross-panel mechanism reconciliation from the two
frozen panels under a SEPARATE code path to confirm the verdict is not an
artifact of a single implementation. Different variable naming, different
groupby/aggregation mechanics, different bootstrap draw loop, but same
pre-registered estimand and inference rules.

Design:
  - Unit: eligible coin x closed UTC hour t on overlapping hours (2026-01-01..2026-08-31).
  - Join FCLR-001 (rv24h, abs_funding_pct_trail, target_rv24h) with liquidation
    panel hourly notional-weighted intensity (sum notional_usd per coin-hour).
  - Primary A: within-(hour, RV-tercile) abs_fund_pct rank -> next-hour RV.
  - Primary B: within-(hour, UTC-session-bucket) abs_fund_pct rank ->
    next-hour notional-weighted liquidation intensity.
  - Baselines: within-regime RV persistence.
  - Inference: block bootstrap across whole UTC hours (seed 20261121, 2000 reps),
    Holm over 4-test joint family, 2% materiality floor.
No network, no paid/credentialed data, no holdout inspected before freeze.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
PANEL_A = REPO / "research_state" / "fclr011_recompute_panel_20261115T234700Z.parquet"
SHA_A = "41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4"
PANEL_B = REPO / "research_state" / "fclr_liq_combined_panel_20261115T181405Z.parquet"
SHA_B = "81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14"
SESSION = "20261121T021041Z"
OUT_DIR = REPO / "research_state" / f"session_{SESSION}"
SEED = 20261121
N_REP = 2000
ALPHA = 0.05
FLOOR = 0.02
MIN_COINS = 3

SYMBOL_MAP = {"BTCUSDT": "BTC", "ETHUSDT": "ETH", "BNBUSDT": "BNB", "SOLUSDT": "SOL", "XRPUSDT": "XRP"}
SYMBOLS = ["BTC", "ETH", "BNB", "SOL", "XRP"]

BUCKETS = {"asian": (0, 8), "european": (8, 16), "us": (16, 24)}
BUCKET_LIST = ["asian", "european", "us"]


def load_panel_a() -> pd.DataFrame:
    d = pd.read_parquet(PANEL_A)
    d = d.sort_values(["coin", "ts"]).reset_index(drop=True)
    d["h"] = d["ts"].dt.floor("h")
    d["sym"] = d["coin"].map(SYMBOL_MAP)
    d = d[d["sym"].isin(SYMBOLS)].copy()
    d = d.rename(columns={"abs_funding_pct_trail": "afp", "target_rv24h": "nrv"})
    return d


def load_panel_b_hourly() -> pd.DataFrame:
    d = pd.read_parquet(PANEL_B)
    d = d.sort_values(["coin", "timestamp"]).reset_index(drop=True)
    d["h"] = d["timestamp"].dt.floor("h")
    agg = (
        d.groupby(["coin", "h"])
        .agg(nwi=("notional_usd", "sum"), ec=("notional_usd", "size"), afp=("abs_fund_pct", "mean"), rv=("rv24h", "mean"))
        .reset_index()
    )
    agg = agg[agg["coin"].isin(SYMBOLS)].copy()
    return agg


def shift_next(d: pd.DataFrame, key: str, val: str) -> pd.DataFrame:
    d = d.sort_values([key, "h"]).reset_index(drop=True)
    d["nxt_" + val] = d.groupby(key)[val].shift(-1)
    return d


def market_rv_per_hour(d: pd.DataFrame) -> pd.DataFrame:
    mw = d.groupby("h")["rv"].agg(mw="mean", n="count").reset_index()
    d = d.merge(mw, on="h", how="left")
    d["ok"] = d["n"] >= MIN_COINS
    return d


def tercile_by_hour(d: pd.DataFrame) -> pd.DataFrame:
    d = d.copy()
    elig = d[d["ok"]].copy()
    per_hour = elig.groupby("h")["mw"].first()
    labels = pd.qcut(per_hour, q=3, labels=["lo", "md", "hi"])
    lut = labels.to_dict()
    d["terc"] = d["h"].map(lut)
    return d


def bucket_by_hour(d: pd.DataFrame) -> pd.DataFrame:
    d = d.copy()
    d["uh"] = d["h"].dt.hour

    def b(uh):
        for nm, (lo, hi) in BUCKETS.items():
            if lo <= uh < hi:
                return nm
        return None

    d["bkt"] = d["uh"].map(b)
    return d


def rank_split(d: pd.DataFrame, rank_col: str) -> pd.DataFrame:
    d = d.copy()
    d["rk"] = d.groupby("h")[rank_col].rank(method="average", ascending=False)
    nn = d.groupby("h")["sym"].transform("nunique")
    d["rkp"] = d["rk"] / nn
    d["grp"] = np.where(d["rkp"] <= 0.5, "hi", "lo")
    return d


def paired_diff(d: pd.DataFrame, gc: str, oc: str) -> np.ndarray:
    st = d.groupby(["h", gc])[oc].agg(m="mean", c="count").reset_index()
    if st.empty:
        return np.array([], dtype=float)
    mv = st.pivot_table(index="h", columns=gc, values="m", aggfunc="first")
    cv = st.pivot_table(index="h", columns=gc, values="c", aggfunc="first")
    mv.columns.name = None
    cv.columns.name = None
    mv = mv.join(cv.add_suffix("_c"))
    mcs = [c for c in mv.columns if not str(c).endswith("_c")]
    if len(mcs) < 2:
        return np.array([], dtype=float)
    a, b = sorted(mcs)[0], sorted(mcs)[1]
    both = mv[mv[a].notna() & mv[b].notna()].copy()
    return (both[a] - both[b]).to_numpy(dtype=float)


def boot_ci(vals: np.ndarray, seed: int, n_rep: int = N_REP):
    rng = np.random.RandomState(seed)
    boot = np.empty(n_rep, dtype=float)
    for i in range(n_rep):
        boot[i] = rng.choice(vals, size=len(vals), replace=True).mean()
    lo = float(np.percentile(boot, 2.5))
    hi = float(np.percentile(boot, 97.5))
    p = float(2 * min((boot >= 0).mean(), (boot <= 0).mean()))
    return lo, hi, p


def holm(pv: list[float]) -> list[float]:
    order = sorted(range(len(pv)), key=lambda i: pv[i])
    adj = [0.0] * len(pv)
    m = len(pv)
    for rank, i in enumerate(order):
        adj[i] = min(1.0, pv[i] * (m - rank))
    return adj


def contrast(diff: np.ndarray, seed: int, denom: float) -> dict:
    n = int(len(diff))
    md = float(diff.mean()) if n > 0 else None
    lo, hi, p = boot_ci(diff, seed)
    excl = bool(lo > 0 or hi < 0)
    me = float(abs(md) / denom) if md is not None and denom > 0 else None
    return {
        "n": n,
        "mean_diff": md,
        "ci_lo": lo,
        "ci_hi": hi,
        "p": p,
        "excludes_zero": excl,
        "pos": int((diff > 0).sum()) if n > 0 else 0,
        "materiality": me,
        "floor_met": bool(me is not None and me >= FLOOR),
    }


def main() -> None:
    ah = hashlib.sha256(PANEL_A.read_bytes()).hexdigest()
    assert ah == SHA_A, f"panel A hash mismatch: {ah}"
    bh = hashlib.sha256(PANEL_B.read_bytes()).hexdigest()
    assert bh == SHA_B, f"panel B hash mismatch: {bh}"

    da = load_panel_a()
    db = load_panel_b_hourly()
    print(f"Panel A rows: {len(da)}, hours: {da['h'].nunique()}")
    print(f"Panel B hourly rows: {len(db)}, hours: {db['h'].nunique()}")

    da = shift_next(da, "sym", "nrv")
    db = shift_next(db, "coin", "nwi")
    db = shift_next(db, "coin", "ec")

    j = da.merge(
        db,
        left_on=["sym", "h"],
        right_on=["coin", "h"],
        how="inner",
    )
    j = j[["sym", "h", "rv", "afp_x", "afp_y", "nrv", "nxt_nrv", "nwi", "nxt_nwi", "nxt_ec"]].copy()
    j = j.rename(columns={"afp_x": "afp", "afp_y": "afp_liq"})
    print(f"Joined rows: {len(j)}, unique hours: {j['h'].nunique()}")

    j = market_rv_per_hour(j)
    je = j[j["ok"] & j["nxt_nrv"].notna() & j["nxt_nwi"].notna()].copy()
    je = tercile_by_hour(je)
    je = je[je["terc"].notna()].copy()
    je = bucket_by_hour(je)
    je = je[je["bkt"].notna()].copy()
    print(f"Eval-eligible coin-hours: {len(je)}, unique hours: {je['h'].nunique()}")

    denom_rv = {t: float(je[je["terc"] == t]["nxt_nrv"].abs().mean()) for t in ["lo", "md", "hi"]}
    denom_liq = {b: float(je[je["bkt"] == b]["nxt_nwi"].abs().mean()) for b in BUCKET_LIST}
    hours_t = {t: int(je[je["terc"] == t]["h"].nunique()) for t in ["lo", "md", "hi"]}
    hours_b = {b: int(je[je["bkt"] == b]["h"].nunique()) for b in BUCKET_LIST}

    res = {}

    # Primary A: tercile funding -> next-hour RV
    for t in ["lo", "md", "hi"]:
        sub = rank_split(je[je["terc"] == t].copy(), "afp")
        diff = paired_diff(sub, "grp", "nxt_nrv")
        res[f"terc_{t}_fund_to_rv"] = contrast(diff, SEED, denom_rv[t])

    # Baseline A: tercile RV persistence -> next-hour RV
    for t in ["lo", "md", "hi"]:
        sub = rank_split(je[je["terc"] == t].copy(), "rv")
        diff = paired_diff(sub, "grp", "nxt_nrv")
        res[f"terc_{t}_rv_persist_to_rv"] = contrast(diff, SEED, denom_rv[t])

    # Primary B: bucket funding -> next-hour notional-weighted liq intensity
    for b in BUCKET_LIST:
        sub = rank_split(je[je["bkt"] == b].copy(), "afp")
        diff = paired_diff(sub, "grp", "nxt_nwi")
        res[f"bkt_{b}_fund_to_liq"] = contrast(diff, SEED, denom_liq[b])

    # Baseline B: bucket RV persistence -> next-hour notional-weighted liq intensity
    for b in BUCKET_LIST:
        sub = rank_split(je[je["bkt"] == b].copy(), "rv")
        diff = paired_diff(sub, "grp", "nxt_nwi")
        res[f"bkt_{b}_rv_persist_to_liq"] = contrast(diff, SEED, denom_liq[b])

    # Holm over joint family (all 12 tests)
    fam = list(res.keys())
    pv = [res[k]["p"] for k in fam]
    adj = holm(pv)
    for k, a in zip(fam, adj):
        res[k]["holm_adj_p"] = float(a)
        res[k]["holm_ok"] = bool(a < ALPHA)

    # Verdicts
    a_tests = [k for k in fam if k.startswith("terc_") and k.endswith("_fund_to_rv") and "hi" in k]
    b_tests = [k for k in fam if k.startswith("bkt_") and k.endswith("_fund_to_liq")]
    a_ok = all(res[k]["excludes_zero"] and res[k]["holm_ok"] and res[k]["floor_met"] for k in a_tests)
    b_ok = all(res[k]["excludes_zero"] and res[k]["holm_ok"] and res[k]["floor_met"] for k in b_tests)
    gate = bool(a_ok and b_ok)
    verdict = "SUPPORTED" if gate else "NOT_SUPPORTED"

    # Cross-panel reconciliation
    hi_sign = np.sign(res[a_tests[0]]["mean_diff"]) if a_tests else 0.0
    agree = []
    for bt in b_tests:
        bs = np.sign(res[bt]["mean_diff"])
        agree.append({"bucket_test": bt, "sign_agreement": bool(hi_sign == bs)})

    def hr_effect(sub, gc, oc):
        both = paired_diff(sub, gc, oc)
        return pd.DataFrame({"eff": both}, index=both.index if hasattr(both, "index") else range(len(both)))

    sub_a = rank_split(je[je["terc"] == "hi"].copy(), "afp")
    eff_rv = pd.DataFrame({"eff_rv": paired_diff(sub_a, "grp", "nxt_nrv")})
    mc = []
    for b in BUCKET_LIST:
        sub_b = rank_split(je[je["bkt"] == b].copy(), "afp")
        eff_liq = pd.DataFrame({"eff_liq": paired_diff(sub_b, "grp", "nxt_nwi")})
        mrg = eff_rv.join(eff_liq, how="inner")
        if len(mrg) > 3:
            c = float(np.corrcoef(mrg["eff_rv"], mrg["eff_liq"])[0, 1])
        else:
            c = None
        mc.append({"bucket": b, "n": int(len(mrg)), "corr": c})

    print("\n=== FCLR-XSEC-007 Recompute (Independent Code Path) ===")
    print(f"Panel A sha256: {SHA_A}, Panel B sha256: {SHA_B}")
    print(f"Joined rows: {len(j)}, eval coin-hours: {len(je)}, shared hours: {je['h'].nunique()}")
    print(f"Hours per tercile: {hours_t}, Hours per bucket: {hours_b}")
    for k in sorted(res.keys()):
        r = res[k]
        print(f"\n{k.replace('_', ' ').title()}:")
        print(f"  n={r['n']}, mean_diff={r['mean_diff']:.6f}, CI=[{r['ci_lo']:.6f},{r['ci_hi']:.6f}], p={r['p']:.6f}")
        print(f"  Holm adj_p={r['holm_adj_p']:.6f}, holm_ok={r['holm_ok']}, excludes_zero={r['excludes_zero']}")
        print(f"  materiality={r['materiality']}, floor_met={r['floor_met']}")
    print(f"\nPrimary A (hi tercile fund->RV) all pass: {a_ok}")
    print(f"Primary B (all buckets fund->liq) all pass: {b_ok}")
    print(f"\nCross-panel reconciliation:")
    print(f"  Sign agreement: {agree}")
    print(f"  Magnitude correlation: {mc}")
    print(f"\nVerdict: {verdict} (gate_passed={gate})")

    print("\n--- Cross-Reference ---")
    print("FCLR-XSEC-002 high-RV: CI [0.0046, 0.2348], SUPPORTED")
    print("FCLR-XSEC-004 low-RV count: CI [448605.26, 841155.73], SUPPORTED")
    print("FCLR-XSEC-005 low-RV notional: CI [452972.90, 850198.89], SUPPORTED")
    print("FCLR-XSEC-006 all UTC buckets: Asian [162051, 521424], European [334550, 782272], US [94750, 698082], SUPPORTED")

    out = {
        "experiment_id": f"FCLR-XSEC-007-RECOMPUTE-{SESSION}",
        "session_utc": SESSION,
        "panel_path_a": str(PANEL_A),
        "panel_sha256_a": SHA_A,
        "panel_path_b": str(PANEL_B),
        "panel_sha256_b": SHA_B,
        "panel_hash_verified_a": ah == SHA_A,
        "panel_hash_verified_b": bh == SHA_B,
        "estimand": "cross_panel_mechanism_reconciliation_rv_tercile_vs_utc_session_bucket",
        "outcome_data_inspected_before_freeze": False,
        "overlapping_coins": SYMBOLS,
        "n_joined_rows": int(len(j)),
        "n_eval_coin_hours": int(len(je)),
        "n_shared_hours": int(je["h"].nunique()),
        "hours_per_tercile": hours_t,
        "hours_per_bucket": hours_b,
        "seed": SEED,
        "n_bootstrap_reps": N_REP,
        "alpha": ALPHA,
        "materiality_floor": FLOOR,
        "joint_family_size": len(fam),
        "holm_correction": "holm",
        "tests": res,
        "primary_a_tests": a_tests,
        "primary_b_tests": b_tests,
        "primary_a_all_pass": bool(a_ok),
        "primary_b_all_pass": bool(b_ok),
        "gate_passed": bool(gate),
        "verdict": verdict,
        "reproduces_fclr_xsec007_evaluation": None,
        "cross_panel_reconciliation": {
            "shared_hours": int(je["h"].nunique()),
            "sign_agreements": agree,
            "magnitude_correlations": mc,
        },
        "cross_reference": {
            "fclr_xsec_002_high_rv_funding_ci": [0.0046, 0.2348],
            "fclr_xsec_004_low_rv_funding_ci": [448605.26, 841155.73],
            "fclr_xsec_005_low_rv_funding_ci": [452972.90, 850198.89],
            "fclr_xsec_006_all_buckets_funding_ci": {"asian": [162051, 521424], "european": [334550, 782272], "us": [94750, 698082]},
        },
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"fclr_xsec007_recompute_{SESSION}.json"
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nSaved recompute to {out_path}")


if __name__ == "__main__":
    main()
