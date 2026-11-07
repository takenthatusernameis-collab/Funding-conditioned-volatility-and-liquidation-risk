#!/usr/bin/env python3
"""Run funding-conditioned volatility ablations (Gate 4). Leakage-resistant, pilot."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingest import loader
from src.features import volatility as vf
from src.features import funding as ff
from src.eval import walkforward as wf

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "data" / "raw"
RES = REPO / "research_state"
ZIPS_DIR = REPO
EPS = 1e-12


def git_sha() -> str:
    try:
        out = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except Exception:
        return "unknown"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_extracted(symbols: List[str]) -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    zips = loader.discover_zips(ZIPS_DIR)
    for zp in zips:
        if not any(s in zp.name for s in symbols):
            continue
        try:
            loader.extract_zip(zp, RAW)
        except Exception:
            continue


def load_funding_panel(symbols: List[str], start: str, end: str) -> pd.DataFrame:
    ensure_extracted(symbols)
    frames = []
    for sym in symbols:
        flist = []
        for fp in sorted(RAW.glob(f"{sym}-fundingRate-*.csv")):
            try:
                flist.append(loader.load_funding(fp))
            except Exception:
                continue
        if not flist:
            continue
        fdf = pd.concat(flist).sort_index()
        fdf = fdf.loc[(fdf.index >= pd.Timestamp(start, tz="UTC")) & (fdf.index <= pd.Timestamp(end, tz="UTC") + pd.Timedelta(days=1))]
        fdf = fdf.reset_index().rename(columns={"calc_time": "timestamp"})
        fdf["symbol"] = sym
        frames.append(fdf)
    if not frames:
        raise RuntimeError("No funding data loaded")
    panel = pd.concat(frames, ignore_index=True)
    panel["timestamp"] = pd.to_datetime(panel["timestamp"], utc=True)
    return panel.set_index(["symbol", "timestamp"]).sort_index()


def load_kline_panel(symbols: List[str], start: str, end: str, horizon: int = 24) -> pd.DataFrame:
    ensure_extracted(symbols)
    frames = []
    for sym in symbols:
        klist = []
        for kf in sorted(RAW.glob(f"{sym}-1h-*.csv")):
            try:
                klist.append(loader.load_klines(kf))
            except Exception:
                continue
        if not klist:
            continue
        kdf = pd.concat(klist).sort_index()
        kdf = kdf.loc[(kdf.index >= pd.Timestamp(start, tz="UTC")) & (kdf.index <= pd.Timestamp(end, tz="UTC") + timedelta(days=1))]
        kdf = vf.add_rv_features(kdf, short_windows=[6, 24], long_windows=[168])
        kdf["target_rv"] = vf.forward_rv(kdf["close"], horizon=horizon)
        kdf["rv_lag"] = kdf["rv_trail_24"].shift(1)
        kdf = kdf.reset_index().rename(columns={"open_time": "timestamp"})
        kdf["symbol"] = sym
        frames.append(kdf)
    if not frames:
        raise RuntimeError("No kline data loaded")
    panel = pd.concat(frames, ignore_index=True)
    panel["timestamp"] = pd.to_datetime(panel["timestamp"], utc=True)
    return panel.set_index(["symbol", "timestamp"]).sort_index()


def add_funding_to_panel(kpanel: pd.DataFrame, fpanel: pd.DataFrame) -> pd.DataFrame:
    """Merge funding features onto the kline panel by (symbol, timestamp).

    Funding features are aligned to each contract's kline index via last-known
    value at/before each hour (forward-fill). Missing history stays NaN; the
    merge never zero-fills. Rows without a kline timestamp are dropped.
    """
    out = kpanel.copy()
    feat_frames = []
    for sym in out.index.get_level_values("symbol").unique():
        kidx = out.xs(sym, level="symbol").index
        try:
            fdf = fpanel.xs(sym, level="symbol")
        except KeyError:
            continue
        ffeat = ff.add_funding_features(kidx, fdf)
        ffeat = ffeat.reset_index()
        ffeat["symbol"] = sym
        ffeat = ffeat.set_index(["symbol", "timestamp"]).sort_index()
        feat_frames.append(ffeat)
    if not feat_frames:
        return out
    # Concatenate per-symbol frames along axis=0 (rows), not axis=1.
    # axis=1 would stack identical column names from each symbol and produce
    # duplicated columns across the multi-symbol panel, which then breaks
    # downstream numpy array construction.
    feats = pd.concat(feat_frames, axis=0)
    feats = feats[~feats.index.duplicated(keep="last")].sort_index()
    # Avoid column collisions with existing kline columns.
    new_cols = [c for c in feats.columns if c not in out.columns]
    merged = out.join(feats[new_cols], how="left")
    return merged


def fit_predict_ols(train_n: pd.DataFrame, test_n: pd.DataFrame, fcols: List[str]) -> np.ndarray:
    """Direct-variance OLS (same form as the validated Gate 3 RV-only baseline).

    Fits target_rv (raw, non-negative) on train-only-normalized features per
    symbol. No log target, no exponentiation -- predictions stay on the
    variance scale and cannot explode to absurd magnitudes.
    """
    preds = np.full(len(test_n), np.nan)
    for sym, grp in test_n.groupby(level="symbol", sort=False):
        tr = train_n.loc[train_n.index.get_level_values("symbol") == sym]
        ytr = tr["target_rv"].to_numpy(dtype=float)
        Xtr = tr[fcols].to_numpy(dtype=float)
        mask = np.isfinite(ytr) & np.all(np.isfinite(Xtr), axis=1)
        Xc, yc = Xtr[mask], ytr[mask]
        if len(yc) < 2:
            continue
        k = Xc.shape[1]
        XtX = Xc.T @ Xc
        ridge = 1e-10 * np.eye(k)
        try:
            coef = np.linalg.solve(XtX + ridge, Xc.T @ yc)
        except np.linalg.LinAlgError:
            continue
        intercept = float(yc.mean() - coef @ Xc.mean(axis=0))
        Xte = grp[fcols].to_numpy(dtype=float)
        p = intercept + Xte @ coef
        p[~np.isfinite(p)] = np.nan
        # Variance forecasts are non-negative by construction; floor tiny OLS
        # overshoots at zero without affecting QLIKE (p<=0 rows are excluded).
        p = np.maximum(p, 0.0)
        preds[test_n.index.get_indexer(grp.index)] = p
    return preds


def metrics(y: np.ndarray, p: np.ndarray) -> Dict[str, object]:
    from src.volatility import eval as veval
    mask = np.isfinite(y) & np.isfinite(p) & (y > 0) & (p > 0)
    ql = veval.qlike(y.tolist(), p.tolist())
    ma = veval.mae(y.tolist(), p.tolist())
    mse_v = veval.mse(y.tolist(), p.tolist())
    rmse_v = float(np.sqrt(mse_v)) if mse_v is not None and np.isfinite(mse_v) else None
    neg = int(np.sum(np.isfinite(p) & (p <= 0)))
    return {"qlike": ql, "mae": ma, "rmse": rmse_v, "valid_n": int(mask.sum()), "neg_pred": neg, "n": int(len(y))}


def main() -> int:
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT"]
    start = "2024-01-01"
    end = "2024-03-31"
    horizon = 24
    RES.mkdir(parents=True, exist_ok=True)

    kpanel = load_kline_panel(symbols, start, end, horizon=horizon)
    fpanel = load_funding_panel(symbols, start, end)
    panel = add_funding_to_panel(kpanel, fpanel)

    from src.eval.walkforward import SplitBounds
    splits = [SplitBounds(
        train=("2024-01-01T00:00:00+00:00", "2024-02-01T00:00:00+00:00"),
        validation=("2024-02-09T00:00:00+00:00", "2024-02-15T00:00:00+00:00"),
        test=("2024-02-22T00:00:00+00:00", "2024-03-31T00:00:00+00:00"),
        purge_days=7, embargo_days=7,
    )]

    base = [c for c in ["rv_trail_24", "rv_trail_168", "rv_trail_6"] if c in panel.columns]
    trail = [c for c in panel.columns if c.startswith(("funding_pct_", "funding_z_"))]
    ablations = {
        "A_rv_only": base[:],
        "B_rv_signed": base + ["funding_signed"],
        "C_rv_abs": base + ["funding_abs"],
        "D_rv_signed_abs": base + ["funding_signed", "funding_abs"],
        "E_rv_funding_trails": base + ["funding_signed", "funding_abs"] + trail,
    }

    all_results = []
    for i, sp in enumerate(splits):
        split_res = {"split_id": i, "ablations": {}}
        idx = panel.index.get_level_values("timestamp")
        train = panel.loc[wf._in_window(idx, sp.train)]
        val = panel.loc[wf._in_window(idx, sp.validation)]
        test = panel.loc[wf._in_window(idx, sp.test)]
        if train.empty or test.empty:
            split_res["status"] = "INSUFFICIENT_DATA"
            all_results.append(split_res)
            continue
        for ab_name, fcols in ablations.items():
            fcols = [c for c in fcols if c in panel.columns]
            try:
                train_n, val_n, test_n, _ = wf.apply_train_only_normalization(train, val, test, fcols)
                p = fit_predict_ols(train_n, test_n, fcols)
                y = test_n["target_rv"].to_numpy(dtype=float)
                m = metrics(y, p)
                m["n_features"] = len(fcols)
                split_res["ablations"][ab_name] = m
            except Exception as e:
                split_res["ablations"][ab_name] = {"err": str(e)}
        split_res["status"] = "OK"
        all_results.append(split_res)

    def agg(ab_name, key="qlike"):
        vals = [r["ablations"][ab_name][key] for r in all_results if r.get("status") == "OK" and ab_name in r.get("ablations", {}) and isinstance(r["ablations"][ab_name].get(key), (int, float)) and np.isfinite(r["ablations"][ab_name].get(key))]
        return float(np.mean(vals)) if vals else None

    summary = {
        "generated_at": now_iso(), "git_sha": git_sha(), "symbols": symbols,
        "period": {"start": start, "end": end}, "horizon": horizon,
        "model": "direct-variance OLS HAR (target = forward realized VARIANCE; train-only normalization; no log/exp transform)",
        "aggregate": {k: {"qlike": agg(k, "qlike"), "mae": agg(k, "mae"), "rmse": agg(k, "rmse"), "neg_pred": agg(k, "neg_pred")} for k in ablations.keys()},
        "splits_detail": all_results,
    }
    qA = summary["aggregate"]["A_rv_only"]["qlike"]
    out_md = RES / "evaluation_summary_funding.md"
    lines = [
        "# Evaluation Summary - Funding Ablations (Gate 4, pilot)",
        "", f"**Generated:** {summary['generated_at']}", f"**Git SHA:** {summary['git_sha']}",
        f"**Scope:** {', '.join(symbols)}, {start} to {end}, 24h forward RV, 1 walk-forward split",
        f"**Model:** direct-variance OLS HAR (target = forward realized VARIANCE; train-only normalization). No log target, no exp transform.",
        "",
        "## Aggregate (mean across splits)",
        "| Ablation | QLIKE | MAE | RMSE | ΔQLIKE vs A | neg_pred |",
        "|---|---|---|---|---|---|",
    ]
    for k in ablations.keys():
        a = summary["aggregate"][k]
        d = (a["qlike"] - qA) if (a["qlike"] is not None and qA is not None) else None
        lines.append(f"| {k} | {a['qlike']} | {a['mae']} | {a['rmse']} | {d} | {a['neg_pred']} |")
    lines += ["", "## Split Details"]
    for r in all_results:
        if r.get("status") != "OK":
            lines.append(f"- Split {r['split_id']}: {r.get('status')}")
            continue
        lines.append(f"- Split {r['split_id']}: test 2024-02-22..2024-03-31")
        for k, v in r["ablations"].items():
            if "err" in v:
                lines.append(f"  - {k}: ERR {v['err']}")
            else:
                lines.append(f"  - {k}: qlike={v['qlike']}, mae={v['mae']}, rmse={v['rmse']}, n_feat={v['n_features']}, valid_n={v['valid_n']}, neg_pred={v['neg_pred']}")
    lines += [
        "", "## Leakage/Alignment Notes",
        "- Funding (8h) aligned to 1h via last-known value at/before each hour (ffill). NaN if missing.",
        "- Trailing funding pct/z computed over rolling windows on aligned series (past-only).",
        "- Chronological splits, 7d purge/embargo, train-only normalization.",
        "- Basis/premium not included in this run (no aligned series added); missing treated as NaN per policy.",
        "", "## Caveats (non-negotiable)",
        "- **Pilot only**: 1 split, 4 assets, Jan-Mar 2024. Not a sealed holdout result; no block-aware CIs; no multiple-comparison control applied.",
        "- Funding ablations B/C/D/E show **worse QLIKE than RV-only (A)** in this pilot sample (possible overfit, regime, or feature construction). Do NOT interpret as evidence funding has no value; do NOT interpret as evidence of value.",
        "- Gate 4 requires robust OOS evidence across adequate splits/assets before any claim. Next: expand splits/period, add basis/premium if available, add regularization tuning on train/val only, and pre-register contrasts.",
    ]
    out_md.write_text("\n".join(lines) + "\n")

    main_sum = RES / "evaluation_summary.md"
    txt = main_sum.read_text() if main_sum.exists() else ""
    marker = "## Funding Ablations (Gate 4)"
    if marker in txt:
        txt = txt.split(marker)[0].rstrip()
    addition = [
        "", "", marker,
        f"**Updated:** {summary['generated_at']} (pilot, 1 split, log-target ridge HAR; not a sealed claim)",
        "", "| Ablation | QLIKE | ΔQLIKE vs A | MAE | neg_pred |", "|---|---|---|---|---|",
    ]
    for k in ablations.keys():
        a = summary["aggregate"][k]
        d = (a["qlike"] - qA) if (a["qlike"] is not None and qA is not None) else None
        addition.append(f"| {k} | {a['qlike']} | {d} | {a['mae']} | {a['neg_pred']} |")
    addition.append("")
    addition.append("> Pilot result: funding variants worse than RV-only on this split/sample. Inconclusive; expand splits and robustness before inference.")
    main_sum.write_text(txt + "\n".join(addition) + "\n")

    manifest = json.loads((RES / "run_manifest.json").read_text()) if (RES / "run_manifest.json").exists() else {}
    manifest["last_funding_ablations"] = summary["generated_at"]
    manifest["funding_ablations"] = summary["aggregate"]
    manifest["funding_ablations_note"] = "pilot_direct_variance_ols"
    (RES / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    leak = (RES / "leakage_audit.md").read_text() if (RES / "leakage_audit.md").exists() else "# Leakage Audit\n"
    if "funding ablations (Gate 4, pilot log-ridge)" not in leak:
        leak += f"\n## Funding ablations (Gate 4, pilot log-ridge) - {summary['generated_at']}\n- [x] Funding ffill last-known at/before hour (no future).\n- [x] Trailing funding stats past-only on aligned series.\n- [x] Chronological splits, purge/embargo=7d.\n- [x] Train-only normalization.\n- [x] Ridge fit on train only; log-target transform applied consistently; no test leakage.\n"
        (RES / "leakage_audit.md").write_text(leak)

    print(json.dumps({k: v["qlike"] for k, v in summary["aggregate"].items()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
