#!/usr/bin/env python3
"""FCLR-EARLY4H-2025H1-LIQ-GLM v1 — QLIKE-consistent estimator for `liq`.

The sealed EARLY4H-2025H1 campaign (prereg 134503Z) answered `rv` (NOT_MET) and left
`liq` INCONCLUSIVE_NUMERICAL_INSTABILITY: its frozen unregularized linear-in-log model
with an exp() link extrapolated on the Oct-2025 funding spike (max per-row QLIKE ~1.6e27).

This campaign re-answers ONLY `liq` with a Poisson / quasi-Poisson GLM (log link, IRLS),
reusing the SAME frozen panel, universe, and splits as the sealed campaign. The estimator
models the conditional mean directly, so it does not exponentiate an unbounded linear
predictor. `rv` is not re-tested. No sealed artifact is modified.

Run:  python3 scripts/early4h_liq_glm.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"

UTC = timezone.utc

CAMPAIGN = "FCLR-EARLY4H-2025H1-LIQ-GLM v1"
EXPERIMENT_ID = "TRACKA-HL-EARLY4H-2025H1-LIQ-GLM"
PREREG_GLOB = "tracka_prereg_early2025h1_liq_glm_*.json"
PANEL = RS / "tracka_hl_early2025h1_panel_20261112T145529Z.parquet"
PANEL_SHA256 = "08c608035d179be8c274dd0b14386c5330893176c1b963048d09f82d98e3f958"

MIN_INSTRUMENTS = 5
MIN_TEST_BLOCKS = 3
MATERIALITY_PCT = 2.0
SEED = 20261112
N_BOOT = 2000
MAX_ROW_QLIKE = 1e6


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(p: Path, obj: Any) -> None:
    p.write_text(json.dumps(obj, indent=2, default=_json_default) + "\n")


def _json_default(o: Any) -> Any:
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (pd.Timestamp, datetime)):
        return o.isoformat()
    raise TypeError(f"not serializable: {type(o)}")


# ============================ prereg / panel =====================================
def load_prereg() -> Tuple[Path, dict]:
    cands = sorted(RS.glob(PREREG_GLOB))
    if not cands:
        raise SystemExit("REFUSED: no frozen liq-glm prereg; freeze one before evaluating")
    p = cands[-1]
    spec = json.loads(p.read_text())
    if not spec.get("frozen_before_outcomes") or not spec.get("pre_registered_before_outcomes"):
        raise SystemExit(f"REFUSED: prereg {p.name} is not marked frozen before outcomes")
    return p, spec


def load_panel() -> pd.DataFrame:
    if not PANEL.exists():
        raise SystemExit(f"REFUSED: panel missing: {PANEL}")
    digest = sha256_file(PANEL)
    if digest != PANEL_SHA256:
        raise SystemExit(
            f"REFUSED: panel sha256 {digest} != expected {PANEL_SHA256}; "
            "rebuild via `python3 scripts/early4h_campaign.py build` and update this script.")
    df = pd.read_parquet(PANEL)
    df["ts"] = pd.to_datetime(df["ts"], utc=True)
    return df.sort_values(["coin", "ts"]).reset_index(drop=True)


# ================================ design =========================================
def model_columns(model: str) -> List[str]:
    if model == "B1":
        return ["rv_4h", "rv_24h", "rv_168h"]
    if model == "C1":
        return ["rv_4h", "rv_24h", "rv_168h", "fundingRate", "abs_fund_pct"]
    if model == "C2":
        return ["rv_4h", "rv_24h", "rv_168h", "fundingRate", "abs_fund_pct",
                "premium", "ema_dist"]
    raise SystemExit(f"REFUSED: unknown model {model}")


def feature_frame(rows: pd.DataFrame, model: str) -> pd.DataFrame:
    eps = 1e-12
    f = pd.DataFrame(index=rows.index)
    for col in model_columns(model):
        if col in ("rv_4h", "rv_24h", "rv_168h"):
            f[col] = np.log(rows[col].clip(lower=eps))
        else:
            f[col] = rows[col]
    return f


def design(rows: pd.DataFrame, model: str, target: pd.Series) -> Tuple[np.ndarray, np.ndarray, pd.DataFrame]:
    """Return (X, y, kept_rows) for a model. y must be > 0 (QLIKE is undefined at 0)."""
    f = feature_frame(rows, model)
    ok = f.notna().all(axis=1) & target.notna() & (target > 0) & np.isfinite(f).all(axis=1)
    return f[ok].to_numpy(float), target[ok].to_numpy(float), rows.loc[ok]


# ============================== Poisson IRLS =====================================
def fit_poisson_loglink(X: np.ndarray, y: np.ndarray,
                        max_iter: int = 100, tol: float = 1e-8) -> Optional[dict]:
    n, p = X.shape
    A = np.column_stack([np.ones(n), X])
    beta = np.linalg.lstsq(A, np.log(y), rcond=None)[0]
    if not np.all(np.isfinite(beta)):
        beta = np.zeros(p + 1)

    def deviance(mu: np.ndarray) -> float:
        return float(2.0 * np.sum(y * np.log(y / mu) - (y - mu)))

    eta = np.clip(A @ beta, -30.0, 30.0)
    mu = np.maximum(np.exp(eta), 1e-12)
    dev = deviance(mu)

    converged = False
    it = 0
    for it in range(1, max_iter + 1):
        eta = np.clip(A @ beta, -30.0, 30.0)
        mu = np.maximum(np.exp(eta), 1e-12)
        z = eta + (y - mu) / mu
        sw = np.sqrt(mu)
        Aw = A * sw[:, None]
        zw = z * sw
        try:
            step = np.linalg.lstsq(Aw, zw, rcond=None)[0]
        except np.linalg.LinAlgError:
            return None
        if not np.all(np.isfinite(step)):
            return None
        # step-halving on the Poisson deviance (numerical safeguard only)
        accepted = False
        shrink = 1.0
        cand = beta
        dev_c = dev
        for _ in range(30):
            trial = beta + shrink * (step - beta)
            mu_t = np.maximum(np.exp(np.clip(A @ trial, -30.0, 30.0)), 1e-12)
            dev_t = deviance(mu_t)
            if np.isfinite(dev_t) and dev_t <= dev + 1e-9:
                cand, dev_c, accepted = trial, dev_t, True
                break
            shrink *= 0.5
        if not accepted:
            break
        delta = float(np.max(np.abs(cand - beta)))
        beta, dev = cand, dev_c
        if delta < tol:
            converged = True
            break

    return {"beta": beta, "converged": converged, "iters": it, "deviance": dev}


def predict(fit: Optional[dict], X: np.ndarray) -> Optional[np.ndarray]:
    if fit is None:
        return None
    A = np.column_stack([np.ones(len(X)), X])
    return np.exp(np.clip(A @ fit["beta"], -30.0, 30.0))


def qlike(y: np.ndarray, yhat: np.ndarray) -> np.ndarray:
    ratio = y / yhat
    return ratio - np.log(ratio) - 1.0


# ================================ inference ======================================
def block_bootstrap(diffs: List[Tuple[int, float]], n_boot: int = N_BOOT, seed: int = SEED):
    if not diffs:
        return None
    by_block: Dict[int, List[float]] = {}
    for b, d in diffs:
        by_block.setdefault(b, []).append(d)
    blocks = list(by_block.values())
    rng = random.Random(seed)
    stats = []
    for _ in range(n_boot):
        samp: List[float] = []
        for _ in range(len(blocks)):
            samp.extend(rng.choice(blocks))
        if samp:
            stats.append(float(np.mean(samp)))
    if not stats:
        return None
    stats.sort()
    lo = stats[int(0.025 * len(stats))]
    hi = stats[int(0.975 * len(stats))]
    return {"mean": float(np.mean([d for _, d in diffs])), "ci_lo": lo, "ci_hi": hi,
            "n_pairs": len(diffs), "n_blocks": len(blocks)}


def holm(pvals: List[float]) -> List[bool]:
    n = len(pvals)
    order = sorted(range(n), key=lambda i: pvals[i])
    rejected = [False] * n
    for rank, i in enumerate(order, start=1):
        if pvals[i] <= 0.05 / (n - rank + 1):
            rejected[i] = True
        else:
            break
    return rejected


def approx_p(mean: float, lo: float, hi: float) -> float:
    if hi <= lo:
        return 1.0
    se = (hi - lo) / (2 * 1.959963985)
    if se <= 0:
        return 1.0
    z = mean / se
    return float(math.erfc(abs(z) / math.sqrt(2.0)))


# ================================ evaluate =======================================
def evaluate() -> dict:
    prereg_path, spec = load_prereg()
    panel = load_panel()
    target = panel["t1_liq"]
    train = panel[panel["split"] == "train"]
    test = panel[panel["split"].astype(str).str.startswith("test_block_")]

    preds: Dict[str, List[dict]] = {}
    fits: Dict[str, Any] = {}
    max_abs_linpred: Dict[str, float] = {}
    max_row_qlike: Dict[str, float] = {}

    for model in ("B1", "C1", "C2"):
        Xtr, ytr, _ = design(train, model, train["t1_liq"])
        fit = fit_poisson_loglink(Xtr, ytr)
        fits[model] = {
            "converged": bool(fit["converged"]) if fit else False,
            "iters": int(fit["iters"]) if fit else 0,
            "deviance": float(fit["deviance"]) if fit else None,
        }
        rows: List[dict] = []
        max_abs_linpred[model] = 0.0
        max_row_qlike[model] = 0.0
        if fit is not None:
            feats = feature_frame(test, model)
            keep = feats.notna().all(axis=1) & target.loc[test.index].notna() \
                & (target.loc[test.index] > 0) & np.isfinite(feats).all(axis=1)
            sub = test.loc[keep]
            Xte = feats.loc[keep].to_numpy(float)
            if len(Xte):
                A = np.column_stack([np.ones(len(Xte)), Xte])
                lin = A @ fit["beta"]
                max_abs_linpred[model] = float(np.max(np.abs(lin)))
                yhat = predict(fit, Xte)
                q = qlike(sub["t1_liq"].to_numpy(float), yhat)
                max_row_qlike[model] = float(np.max(q)) if len(q) else 0.0
                for (coin, ts, blk), qi in zip(
                        sub[["coin", "ts", "test_block"]].itertuples(index=False, name=None), q):
                    rows.append({"coin": coin, "ts": ts, "block": int(blk),
                                 "qlike": float(qi)})
        preds[model] = rows

    def mean_q(model: str) -> Optional[float]:
        r = preds[model]
        return float(np.mean([x["qlike"] for x in r])) if r else None

    def paired(a: str, b: str) -> List[Tuple[int, float]]:
        kb = {(x["coin"], x["ts"]): x["qlike"] for x in preds[b]}
        return [(x["block"], x["qlike"] - kb[(x["coin"], x["ts"])])
                for x in preds[a] if (x["coin"], x["ts"]) in kb]

    contrasts = {}
    for name, a, b in (("C2_vs_B1", "C2", "B1"), ("C1_vs_B1", "C1", "B1"), ("C2_vs_C1", "C2", "C1")):
        boot = block_bootstrap(paired(a, b))
        mb = mean_q(b)
        rel = None
        if boot and mb:
            rel = (-boot["mean"] / abs(mb)) * 100.0
        p = approx_p(boot["mean"], boot["ci_lo"], boot["ci_hi"]) if boot else 1.0
        contrasts[name] = {
            "mean_diff": boot["mean"] if boot else None,
            "ci_lo": boot["ci_lo"] if boot else None,
            "ci_hi": boot["ci_hi"] if boot else None,
            "n_pairs": boot["n_pairs"] if boot else 0,
            "n_blocks": boot["n_blocks"] if boot else 0,
            "rel_reduction_pct": rel,
            "p_value": p,
        }

    names = list(contrasts)
    for n, rej in zip(names, holm([contrasts[n]["p_value"] for n in names])):
        contrasts[n]["holm_rejected"] = bool(rej)

    primary = contrasts["C2_vs_B1"]
    kb = {(x["coin"], x["ts"]): x["qlike"] for x in preds["B1"]}
    per_coin = {}
    per = {}
    for x in preds["C2"]:
        k = (x["coin"], x["ts"])
        if k in kb:
            per.setdefault(x["coin"], []).append(x["qlike"] - kb[k])
    per_coin = {c: float(np.mean(v)) for c, v in per.items()}

    per_block = {}
    for b in sorted({x["block"] for x in preds["C2"]}):
        kb_b = {(x["coin"], x["ts"]): x["qlike"] for x in preds["B1"] if x["block"] == b}
        d = [x["qlike"] - kb_b[(x["coin"], x["ts"])] for x in preds["C2"]
             if x["block"] == b and (x["coin"], x["ts"]) in kb_b]
        if d:
            per_block[b] = float(np.mean(d))

    blocks_with_data = sorted(per_block)
    instr = sorted(per_coin)
    numerical_unstable = any(v > MAX_ROW_QLIKE for v in max_row_qlike.values())

    rel_pass = primary["rel_reduction_pct"] is not None and primary["rel_reduction_pct"] >= MATERIALITY_PCT
    ci_pass = primary["ci_hi"] is not None and primary["ci_hi"] < 0
    block_pass = len(blocks_with_data) >= MIN_TEST_BLOCKS
    instr_pass = len(instr) >= MIN_INSTRUMENTS
    holm_pass = primary["holm_rejected"]
    single_coin = (len(per_coin) == 1)
    gate_pass = rel_pass and ci_pass and block_pass and instr_pass and holm_pass and not single_coin

    if not block_pass:
        verdict = "INCONCLUSIVE_PILOT_SHORTFALL"
    elif numerical_unstable:
        verdict = "INCONCLUSIVE_NUMERICAL_INSTABILITY"
    elif gate_pass:
        verdict = "PASS"
    else:
        verdict = "NOT_MET"

    out = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "generated_utc": now_utc(),
        "prereg": str(prereg_path.relative_to(REPO)),
        "prereg_sha256": sha256_file(prereg_path),
        "panel": str(PANEL.relative_to(REPO)),
        "panel_sha256": sha256_file(PANEL),
        "estimator": "Poisson/quasi-Poisson GLM, log link, IRLS, no regularization",
        "target": "t1_liq (next-24h observed liquidation notional USD), positive rows only",
        "verdict": verdict,
        "gate_pass": gate_pass,
        "numerical_stability": {
            "max_abs_linear_predictor": max_abs_linpred,
            "max_row_qlike": max_row_qlike,
            "threshold": MAX_ROW_QLIKE,
            "unstable": numerical_unstable,
            "reason": ("per-row QLIKE > 1e6; mean QLIKE is a numerical artifact, not interpretable"
                       if numerical_unstable else None),
        },
        "fit": fits,
        "mean_qlike": {m: mean_q(m) for m in ("B1", "C1", "C2")},
        "contrasts": contrasts,
        "per_coin_mean_diff_c2_vs_b1": per_coin,
        "per_block_mean_diff_c2_vs_b1": per_block,
        "test_blocks_with_data": blocks_with_data,
        "paired_instruments": instr,
        "n_train_rows": int(len(train)),
        "n_test_rows": int(len(test)),
        "gate": {"materiality_ge_2pct": rel_pass, "ci_upper_below_zero": ci_pass,
                 "min_test_blocks_ge_3": block_pass, "min_instruments_ge_5": instr_pass,
                 "holm_pass": holm_pass, "single_coin_only": single_coin},
        "compliance": spec.get("compliance", {}),
        "seed": SEED,
        "n_bootstrap": N_BOOT,
    }

    ts = stamp()
    jp = RS / f"evaluation_summary_EARLY4H-2025H1-LIQ-GLM-{ts}.json"
    write_json(jp, out)

    lines = [f"# Track A — Early 4h Liquidation GLM Evaluation — {EXPERIMENT_ID}",
             f"**Timestamp (UTC):** {out['generated_utc']}",
             f"**Prereg:** `{prereg_path.name}` (sha256 {out['prereg_sha256'][:16]}...)",
             f"**Panel:** `{PANEL.name}` (sha256 {out['panel_sha256'][:16]}...)",
             f"**Estimator:** Poisson/quasi-Poisson GLM, log link, IRLS, no regularization",
             f"**Target:** `t1_liq` (positive rows only)", "",
             f"## Verdict — `liq`: `{verdict}`", "",
             "| Model | Mean QLIKE | Converged | Iters | Max row QLIKE |",
             "|---|---|---|---|---|"]
    for m in ("B1", "C1", "C2"):
        lines.append(f"| {m} | {_fmt(out['mean_qlike'][m])} | {out['fit'][m]['converged']} | "
                     f"{out['fit'][m]['iters']} | {_fmt(out['numerical_stability']['max_row_qlike'][m])} |")
    lines += ["", "| Contrast | Mean diff | 95% CI | Rel reduction % | p | Holm |",
              "|---|---|---|---|---|---|"]
    for n, c in out["contrasts"].items():
        lines.append(f"| {n} | {_fmt(c['mean_diff'])} | [{_fmt(c['ci_lo'])}, {_fmt(c['ci_hi'])}] | "
                     f"{_fmt(c['rel_reduction_pct'])} | {_fmt(c['p_value'])} | {c['holm_rejected']} |")
    lines += ["",
              f"- Test blocks with data: {out['test_blocks_with_data']} (required {MIN_TEST_BLOCKS})",
              f"- Paired instruments: {len(out['paired_instruments'])} (required {MIN_INSTRUMENTS})",
              "- Per-coin mean diff C2-B1: "
              + ", ".join(f"{k}={round(v, 4)}" for k, v in out["per_coin_mean_diff_c2_vs_b1"].items()),
              "- Per-block mean diff C2-B1: "
              + ", ".join(f"{k}={round(v, 4)}" for k, v in out["per_block_mean_diff_c2_vs_b1"].items()),
              "", "## Gate"]
    for k, v in out["gate"].items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## Compliance"]
    for k, v in out["compliance"].items():
        lines.append(f"- {k}: {v}")
    mp = RS / f"evaluation_summary_EARLY4H-2025H1-LIQ-GLM-{ts}.md"
    mp.write_text("\n".join(lines) + "\n")

    print(json.dumps({"json": str(jp.relative_to(REPO)), "md": str(mp.relative_to(REPO)),
                      "verdict": verdict, "gate_pass": gate_pass,
                      "mean_qlike": out["mean_qlike"],
                      "C2_vs_B1": out["contrasts"]["C2_vs_B1"]}, indent=2))
    return out


def _fmt(v: Any) -> str:
    return "n/a" if v is None else (f"{v:.6g}" if isinstance(v, float) else str(v))


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog="early4h_liq_glm", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", nargs="?", default="evaluate", choices=["evaluate"])
    ap.parse_args(argv)
    evaluate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())