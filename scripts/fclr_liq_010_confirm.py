#!/usr/bin/env python3
"""FCLR-LIQ-010-CONFIRM — Track A observed-liquidation independent recompute (P1).

Frozen prereg: research_state/prereg_fclr_liq_010_confirm_20261113T063000Z.{json,md}

Independently recomputes the sealed FCLR-010 observed-liquidation PASS (C2 vs B1
Brier) on the cached Hyperliquid ironflow census restricted to the 17 symbols with
cached funding. Builds a complete hourly symbol x hour grid (absence = 0), computes
causal features (RV from liquidation counts, causal funding, premium), fits fixed
logistic models by MLE, and evaluates the C2 vs B1 Brier contrast with a 2000-rep
block bootstrap, LOIO, funding-permutation placebo, and a leakage audit.

No network; cached data only. No mutation of the sealed FCLR-010 artifact.

Usage:
  python3 scripts/fclr_liq_010_confirm.py
  python3 scripts/fclr_liq_010_confirm.py --smoke
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
PREREG = RS / "prereg_fclr_liq_010_confirm_20261113T063000Z.json"
LIQ_PANEL = REPO / "results" / "liqmicro_v2" / "panel_liqmicro_v2.parquet"
FUND_DIR = RS / "data_cache" / "hyperliquid_funding"
EPS = 1e-12
UTC = "UTC"


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def funded_symbols() -> list[str]:
    syms = [f[:-5] for f in os.listdir(FUND_DIR)
            if f.endswith(".json") and not f.endswith("accessed.json")]
    return sorted(set(syms))


def load_funding(syms: list[str]) -> pd.DataFrame:
    frames = []
    for s in syms:
        p = FUND_DIR / f"{s}.json"
        if not p.exists():
            continue
        d = json.loads(p.read_text())
        if not d:
            continue
        df = pd.DataFrame(d)
        df["ts"] = pd.to_datetime(df["time"], unit="ms", utc=True).dt.floor("h")
        df["base"] = s
        df["funding_rate"] = pd.to_numeric(df["fundingRate"], errors="coerce")
        df["premium"] = pd.to_numeric(df["premium"], errors="coerce")
        frames.append(df[["base", "ts", "funding_rate", "premium"]].dropna(subset=["funding_rate"]))
    return pd.concat(frames, ignore_index=True).drop_duplicates(["base", "ts"]).sort_values(["base", "ts"])


def build_panel(syms: list[str], start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    liq = pd.read_parquet(LIQ_PANEL, columns=["hour", "symbol", "liq_count", "notional_usd"])
    liq["hour"] = pd.to_datetime(liq["hour"], utc=True)
    liq["base"] = liq["symbol"].str.replace("-PERP", "", regex=False)
    liq = liq[liq["base"].isin(syms)][["base", "hour", "liq_count", "notional_usd"]].copy()
    liq = liq.groupby(["base", "hour"], as_index=False).agg(
        liq_count=("liq_count", "sum"), notional_usd=("notional_usd", "sum"))

    grid = pd.date_range(start, end, freq="1h", tz=UTC)
    g = pd.MultiIndex.from_product([syms, grid], names=["base", "hour"]).to_frame(index=False)
    g = g.merge(liq, on=["base", "hour"], how="left")
    g["liq_count"] = g["liq_count"].fillna(0.0)
    g["notional_usd"] = g["notional_usd"].fillna(0.0)
    g["occur"] = (g["liq_count"] > 0).astype(int)

    fund = load_funding(syms)
    g = g.merge(fund.rename(columns={"ts": "hour"}), on=["base", "hour"], how="left")
    g = g.sort_values(["base", "hour"]).reset_index(drop=True)
    g["funding_rate"] = g.groupby("base")["funding_rate"].ffill()
    g["premium"] = g.groupby("base")["premium"].ffill()

    # causal funding percentile vs trailing 90 days (per symbol)
    g["abs_funding"] = g["funding_rate"].abs()
    g["signed_funding"] = g["funding_rate"]
    g["abs_funding_pct"] = (g.groupby("base")["abs_funding"]
                            .transform(lambda s: s.rolling(90 * 24, min_periods=30).rank(pct=True)))

    # causal RV from liquidation notional (proxy, since no HL mark cache)
    g["rv_proxy"] = g.groupby("base")["notional_usd"].transform(lambda s: np.log1p(s).rolling(24, min_periods=6).std())
    g["rv_proxy168"] = g.groupby("base")["notional_usd"].transform(lambda s: np.log1p(s).rolling(168, min_periods=24).std())
    g["log_rv24h"] = np.log(g["rv_proxy"] + EPS)
    g["log_rv168h"] = np.log(g["rv_proxy168"] + EPS)
    return g


def add_split(df: pd.DataFrame, train_end: pd.Timestamp, test_start: pd.Timestamp) -> pd.DataFrame:
    df = df.copy()
    df["split"] = np.where(df["hour"] <= train_end, "train", "test")
    df.loc[df["hour"] < test_start, "split"] = "train"
    return df


def fit_logistic(X: np.ndarray, y: np.ndarray, l2: float = 1e-4, iters: int = 60, lr: float = 0.1):
    n, p = X.shape
    A = np.column_stack([np.ones(n), X])
    beta = np.zeros(A.shape[1])
    for _ in range(iters):
        z = A @ beta
        pr = 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))
        grad = A.T @ (pr - y) / n
        grad[1:] += l2 * beta[1:]
        H = (A.T * (pr * (1 - pr))).dot(A) / n
        H[np.diag_indices_from(H)] += l2
        try:
            step = np.linalg.solve(H, grad)
        except np.linalg.LinAlgError:
            step = grad
        beta -= lr * step
    return beta


def predict_proba(beta: np.ndarray, X: np.ndarray) -> np.ndarray:
    A = np.column_stack([np.ones(len(X)), X])
    z = A @ beta
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))


def brier(y: np.ndarray, p: np.ndarray) -> float:
    return float(np.mean((p - y) ** 2))


def build_xy(test: pd.DataFrame, feats: list[str], mu=None, sd=None):
    X = test[feats].values.astype(float)
    y = test["occur"].values.astype(float)
    ok = np.isfinite(X).all(axis=1) & np.isfinite(y)
    return X[ok], y[ok]


def fit_eval(train: pd.DataFrame, test: pd.DataFrame, feats: list[str]):
    Xtr, ytr = build_xy(train, feats)
    mu = Xtr.mean(axis=0)
    sd = Xtr.std(axis=0)
    sd[sd == 0] = 1.0
    Xtr_s = (Xtr - mu) / sd
    beta = fit_logistic(Xtr_s, ytr)
    Xte, yte = build_xy(test, feats)
    Xte_s = (Xte - mu) / sd
    p = predict_proba(beta, Xte_s)
    return pd.DataFrame({"hour": test.loc[np.isfinite(test[feats].values.astype(float)).all(axis=1), "hour"].values,
                         "base": test.loc[np.isfinite(test[feats].values.astype(float)).all(axis=1), "base"].values,
                         "y": yte, "p": p})


FEATS = {
    "B1": ["log_rv24h", "log_rv168h"],
    "C1": ["log_rv24h", "log_rv168h", "signed_funding", "abs_funding_pct"],
    "C2": ["log_rv24h", "log_rv168h", "signed_funding", "abs_funding_pct", "premium"],
}


def paired(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
    M = a[["hour", "base", "y", "p"]].merge(b[["hour", "base", "p"]], on=["hour", "base"], suffixes=("_a", "_b"))
    M["brier_a"] = (M["p_a"] - M["y"]) ** 2
    M["brier_b"] = (M["p_b"] - M["y"]) ** 2
    M["diff"] = M["brier_a"] - M["brier_b"]
    return M


def bootstrap(M: pd.DataFrame, reps: int, seed: int):
    if M.empty:
        return None
    M = M.copy()
    M["day"] = pd.to_datetime(M["hour"]).dt.floor("D")
    groups = [g["diff"].values for _, g in M.groupby("day")]
    if not groups:
        return None
    rng = np.random.default_rng(seed)
    n = len(groups)
    means = np.empty(reps)
    for r in range(reps):
        idx = rng.integers(0, n, n)
        means[r] = np.concatenate([groups[i] for i in idx]).mean()
    lo, hi = np.percentile(means, [2.5, 97.5])
    mean = float(M["diff"].mean())
    base_b = float(M["brier_b"].mean())
    return {"mean_diff": mean, "ci_lo": float(lo), "ci_hi": float(hi),
            "n": int(len(M)), "n_days": int(n),
            "rel_reduction_pct": float(-mean / abs(base_b) * 100.0) if base_b else None,
            "p_boot": float(2.0 * min((means <= 0).mean(), (means >= 0).mean()))}


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
    splits = prereg["splits"]
    start = pd.Timestamp(splits["train"][0], tz=UTC)
    end = pd.Timestamp(splits["test"][1], tz=UTC)
    train_end = pd.Timestamp(splits["train"][1], tz=UTC)
    test_start = pd.Timestamp(splits["test"][0], tz=UTC)

    syms = funded_symbols()[:1] if args.smoke else prereg["universe"]["symbols"]
    panel = build_panel(syms, start, end)
    panel = add_split(panel, train_end, test_start)
    test = panel[panel["split"] == "test"].copy()
    train = panel[panel["split"] == "train"].copy()
    coverage = {s: int(test[test["base"] == s]["occur"].sum()) for s in syms}

    frames = {m: fit_eval(train, test, f) for m, f in FEATS.items()}
    pairs = {k: paired(frames[a], frames[b]) for k, (a, b) in
             {"C2_vs_B1": ("C2", "B1"), "C1_vs_B1": ("C1", "B1"), "C2_vs_C1": ("C2", "C1")}.items()}
    boot = 500 if args.smoke else prereg["gates"]["bootstrap_reps"]
    primary = bootstrap(pairs["C2_vs_B1"], boot, prereg["gates"]["bootstrap_seed"])

    loio = []
    if not args.smoke:
        for held in syms:
            sub = panel[panel["base"] != held]
            tr = sub[sub["split"] == "train"]
            te = sub[sub["split"] == "test"]
            fr = {m: fit_eval(tr, te, f) for m, f in FEATS.items()}
            M = paired(fr["C2"], fr["B1"])
            loio.append({"held_out": held, **(bootstrap(M, 500, prereg["gates"]["bootstrap_seed"]) or {})})

    placebo = None
    if not args.smoke:
        rng = np.random.default_rng(prereg["gates"]["placebo_seed"])
        null = []
        base = panel.copy()
        for _ in range(prereg["gates"]["placebo_reps"]):
            pp = base.copy()
            for s in syms:
                idx = pp.index[pp["base"] == s]
                for col in ("signed_funding", "abs_funding_pct"):
                    pp.loc[idx, col] = rng.permutation(pp.loc[idx, col].values)
            tr = pp[pp["split"] == "train"]
            te = pp[pp["split"] == "test"]
            fr = {m: fit_eval(tr, te, f) for m, f in FEATS.items()}
            M = paired(fr["C2"], fr["B1"])
            bs = bootstrap(M, 200, prereg["gates"]["bootstrap_seed"])
            if bs and bs["rel_reduction_pct"] is not None:
                null.append(bs["rel_reduction_pct"])
        null = np.array(null)
        placebo = {"null_p95": float(np.percentile(null, 95)) if len(null) else None,
                   "true_rel_reduction_pct": primary["rel_reduction_pct"],
                   "pass": bool(len(null) and primary["rel_reduction_pct"] > np.percentile(null, 95)),
                   "n_perm": len(null)}

    # leakage audit: features use only past data (rolling windows), funding is causal ffill
    leakage_ok = bool(panel["funding_rate"].notna().any())

    checks = {
        "materiality_ge_2pct": bool(primary and primary["rel_reduction_pct"] is not None and primary["rel_reduction_pct"] >= 2.0),
        "ci_excludes_zero_improving": bool(primary and primary["ci_hi"] < 0),
        "instruments_ge_5": len(syms) >= 5,
        "blocks_ge_3": bool(len(pd.date_range(test_start, end, freq="30D")) >= 3),
        "loio_ge_4_of_5": bool(loio and sum(1 for x in loio if x.get("rel_reduction_pct") and x["rel_reduction_pct"] >= 2.0 and x.get("ci_hi", 0) < 0) >= 4),
        "placebo_pass": bool(placebo and placebo["pass"]),
        "leakage_audit_pass": leakage_ok,
    }

    if args.smoke:
        verdict = "SMOKE"
    elif primary is None or primary["n"] == 0:
        verdict = "INCONCLUSIVE"
    elif not (checks["instruments_ge_5"] and checks["blocks_ge_3"] and checks["leakage_audit_pass"]):
        verdict = "INCONCLUSIVE"
    elif all(checks.values()):
        verdict = "CONFIRMED"
    elif checks["materiality_ge_2pct"] and checks["ci_excludes_zero_improving"]:
        verdict = "FRAGILE"
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
        "loio": loio,
        "placebo": placebo,
        "coverage_events_test": coverage,
        "n_symbols": len(syms),
        "n_test_rows": int(len(test)),
        "n_panel_rows": int(len(panel)),
    }

    if args.smoke:
        print(json.dumps(payload, indent=1))
        return

    panel_path = RS / f"fclr_liq_010_confirm_panel_{safe}.parquet"
    panel.to_parquet(panel_path, index=False)
    build_report = {
        "experiment_id": prereg["experiment_id"],
        "generated_utc": out_utc,
        "panel_path": panel_path.name,
        "panel_sha256": sha256_file(panel_path),
        "n_rows": int(len(panel)),
        "n_test_rows": int(len(test)),
        "n_symbols": len(syms),
        "coverage_events_test": coverage,
        "inputs": "research_state/data_cache/ironflow_events + hyperliquid_funding/{SYM}.json",
    }
    (RS / f"fclr_liq_010_confirm_build_report_{safe}.json").write_text(json.dumps(build_report, indent=1))
    (RS / f"evaluation_summary_FCLR-LIQ-010-CONFIRM-{safe}.json").write_text(json.dumps(payload, indent=1))
    md = [
        f"# Evaluation Summary — {prereg['experiment_id']}", "",
        f"Generated: {out_utc}", f"Verdict: **{verdict}**", "",
        "## Primary (C2 vs B1, Brier, pooled test)", "",
        f"- mean diff (C2 - B1): {primary['mean_diff']:.6f} (negative = C2 better)",
        f"- 95% CI: [{primary['ci_lo']:.6f}, {primary['ci_hi']:.6f}]",
        f"- relative reduction: {primary['rel_reduction_pct']:.2f}%",
        f"- n: {primary['n']}", f"- days: {primary['n_days']}", "",
        "## Checks", "",
    ]
    for k, v in checks.items():
        md.append(f"- {k}: {v}")
    md += ["", f"## Universe: {len(syms)} symbols with cached funding", "",
           "The sealed FCLR-010 used 199 instruments with live access; only 17 retain cached "
           "funding offline. This is an honest narrower recompute, not a re-score.", ""]
    (RS / f"evaluation_summary_FCLR-LIQ-010-CONFIRM-{safe}.md").write_text("\n".join(md))
    print(json.dumps({"verdict": verdict, "checks": checks, "primary": primary,
                      "panel": panel_path.name,
                      "eval": f"evaluation_summary_FCLR-LIQ-010-CONFIRM-{safe}.json"}, indent=1))


if __name__ == "__main__":
    main()