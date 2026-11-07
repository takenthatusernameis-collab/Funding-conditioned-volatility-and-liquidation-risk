#!/usr/bin/env python3
"""Run funding-conditioned volatility ablations (Gate 4), multi-split pilot.

Leakage-resistant, pre-registered (research_state/pre_registration_gate4_funding_multisplit_20261107.md):
- Chronological walk-forward splits, purge/embargo >= 7d
- Train-only normalization per split
- Funding last-known at/before hour (no lookahead); trailing stats past-only
- Direct-variance OLS HAR (Gate 3 form); A_rv_only regression-stable
- Block bootstrap ΔQLIKE CIs, resampling whole UTC time blocks jointly across instruments
- Honest verdict PILOT/INCONCLUSIVE when data-sufficiency criteria unmet
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ingest import loader
from src.features import volatility as vf
from src.features import funding as ff
from src.eval import walkforward as wf
from src.volatility import block_bootstrap as bb
from src.volatility import eval as veval

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "data" / "raw"
RES = REPO / "research_state"
ZIPS_DIR = REPO
EPS = 1e-12

PRE_REG_SPLITS = [
    {"id": 0, "train": ("2024-01-01T00:00:00+00:00", "2024-01-28T23:59:59+00:00"), "test": ("2024-02-05T00:00:00+00:00", "2024-02-18T23:59:59+00:00")},
    {"id": 1, "train": ("2024-01-15T00:00:00+00:00", "2024-02-11T23:59:59+00:00"), "test": ("2024-02-19T00:00:00+00:00", "2024-03-03T23:59:59+00:00")},
    {"id": 2, "train": ("2024-01-29T00:00:00+00:00", "2024-02-25T23:59:59+00:00"), "test": ("2024-03-04T00:00:00+00:00", "2024-03-17T23:59:59+00:00")},
]
PURGE_DAYS = 7
EMBARGO_DAYS = 7
BOOTSTRAP_SEED = 12345
BOOTSTRAP_REPS = 2000
BOOTSTRAP_BLOCK_HOURS = 24
BOOTSTRAP_ALPHA = 0.05


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
    feats = pd.concat(feat_frames, axis=0)
    feats = feats[~feats.index.duplicated(keep="last")].sort_index()
    new_cols = [c for c in feats.columns if c not in out.columns]
    return out.join(feats[new_cols], how="left")


def fit_predict_ols(train_n: pd.DataFrame, test_n: pd.DataFrame, fcols: List[str]) -> np.ndarray:
    """Direct-variance OLS (same form as the validated Gate 3 RV-only baseline)."""
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
        p = np.maximum(p, 0.0)
        preds[test_n.index.get_indexer(grp.index)] = p
    return preds


def metrics(y: np.ndarray, p: np.ndarray) -> Dict[str, object]:
    mask = np.isfinite(y) & np.isfinite(p) & (y > 0) & (p > 0)
    ql = veval.qlike(y.tolist(), p.tolist())
    ma = veval.mae(y.tolist(), p.tolist())
    mse_v = veval.mse(y.tolist(), p.tolist())
    rmse_v = float(np.sqrt(mse_v)) if mse_v is not None and np.isfinite(mse_v) else None
    neg = int(np.sum(np.isfinite(p) & (p <= 0)))
    return {"qlike": ql, "mae": ma, "rmse": rmse_v, "valid_n": int(mask.sum()), "neg_pred": neg, "n": int(len(y))}


def paired_qlike_by_time(y: np.ndarray, p_base: np.ndarray, p_alt: np.ndarray, ts: pd.DatetimeIndex) -> pd.DataFrame:
    """Paired per-observation QLIKE contributions on jointly valid rows, by timestamp."""
    y = np.asarray(y, dtype=float)
    p_base = np.asarray(p_base, dtype=float)
    p_alt = np.asarray(p_alt, dtype=float)
    mask = np.isfinite(y) & np.isfinite(p_base) & np.isfinite(p_alt) & (y > 0) & (p_base > 0) & (p_alt > 0)
    if not mask.any():
        return pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"])
    yv, bv, av = y[mask], p_base[mask], p_alt[mask]
    tsv = pd.DatetimeIndex(ts[mask])
    rb = yv / bv
    ra = yv / av
    ql_base = rb - np.log(rb) - 1.0
    ql_alt = ra - np.log(ra) - 1.0
    return pd.DataFrame({"timestamp": tsv, "ql_base": ql_base, "ql_alt": ql_alt, "diff": ql_alt - ql_base})


def block_bootstrap_delta_ci(paired: pd.DataFrame, block_hours: int = BOOTSTRAP_BLOCK_HOURS, n_reps: int = BOOTSTRAP_REPS, seed: int = BOOTSTRAP_SEED, alpha: float = BOOTSTRAP_ALPHA) -> Dict[str, object]:
    """Block bootstrap CI for mean ΔQLIKE (alt-base), resampling whole UTC time blocks jointly across instruments."""
    if paired.empty:
        return {"point": None, "ci_low": None, "ci_high": None, "n_obs": 0, "n_blocks": 0, "n_reps": 0, "seed": seed, "block_hours": block_hours}
    paired = paired.copy()
    paired["_block"] = paired["timestamp"].dt.floor(f"{int(block_hours)}h")
    blocks = paired.groupby("_block", sort=True)["diff"].apply(lambda s: s.to_numpy(dtype=float)).to_dict()
    keys = list(blocks.keys())
    if not keys:
        return {"point": None, "ci_low": None, "ci_high": None, "n_obs": int(len(paired)), "n_blocks": 0, "n_reps": 0, "seed": seed, "block_hours": block_hours}
    point = float(paired["diff"].mean())
    n_blocks = len(keys)
    reps_idx = bb.circular_block_bootstrap_indices(n_blocks, 1, n_reps, seed=seed)
    diffs = []
    for ridx in reps_idx:
        vals = []
        for bi in ridx:
            vals.append(blocks[keys[bi]])
        arr = np.concatenate(vals)
        if arr.size:
            diffs.append(float(np.mean(arr)))
    if not diffs:
        return {"point": point, "ci_low": point, "ci_high": point, "n_obs": int(len(paired)), "n_blocks": n_blocks, "n_reps": 0, "seed": seed, "block_hours": block_hours}
    diffs_sorted = sorted(diffs)
    lo_i = max(0, min(len(diffs_sorted) - 1, int(np.floor((alpha / 2.0) * len(diffs_sorted)))))
    hi_i = max(0, min(len(diffs_sorted) - 1, int(np.ceil((1.0 - alpha / 2.0) * len(diffs_sorted))) - 1))
    return {"point": point, "ci_low": float(diffs_sorted[lo_i]), "ci_high": float(diffs_sorted[hi_i]), "n_obs": int(len(paired)), "n_blocks": n_blocks, "n_reps": int(len(diffs)), "seed": seed, "block_hours": block_hours, "alpha": alpha}


def build_prereg_splits() -> List[SplitBounds]:
    return [
        wf.SplitBounds(
            train=s["train"], validation=s["test"], test=s["test"],
            purge_days=PURGE_DAYS, embargo_days=EMBARGO_DAYS,
        )
        for s in PRE_REG_SPLITS
    ]


def run_multisplit(panel: pd.DataFrame, ablations: Dict[str, List[str]]) -> Tuple[List[Dict[str, object]], Dict[str, pd.DataFrame], Dict[str, List[pd.DataFrame]]]:
    splits = build_prereg_splits()
    idx = panel.index.get_level_values("timestamp")
    all_results: List[Dict[str, object]] = []
    pooled_paired: Dict[str, List[pd.DataFrame]] = {k: [] for k in ablations.keys() if k != "A_rv_only"}
    split_paired: Dict[str, List[pd.DataFrame]] = {k: [] for k in ablations.keys() if k != "A_rv_only"}
    for i, sp in enumerate(splits):
        meta = PRE_REG_SPLITS[i]
        split_res: Dict[str, object] = {"split_id": i, "train": meta["train"], "test": meta["test"], "purge_days": PURGE_DAYS, "embargo_days": EMBARGO_DAYS, "ablations": {}}
        train = panel.loc[wf._in_window(idx, sp.train)]
        test = panel.loc[wf._in_window(idx, sp.test)]
        if train.empty or test.empty:
            split_res["status"] = "INSUFFICIENT_DATA"
            split_res["n_train"] = int(len(train)); split_res["n_test"] = int(len(test))
            all_results.append(split_res)
            for k in split_paired:
                split_paired[k].append(pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"]))
            continue
        preds_map: Dict[str, np.ndarray] = {}
        y_test: Optional[np.ndarray] = None
        ts_test: Optional[pd.DatetimeIndex] = None
        for ab_name, fcols in ablations.items():
            fcols = [c for c in fcols if c in panel.columns]
            try:
                train_n, _, test_n, _ = wf.apply_train_only_normalization(train, test, test, fcols)
                p = fit_predict_ols(train_n, test_n, fcols)
                y = test_n["target_rv"].to_numpy(dtype=float)
                m = metrics(y, p)
                m["n_features"] = len(fcols)
                split_res["ablations"][ab_name] = m
                preds_map[ab_name] = p
                y_test = y
                ts_test = test_n.index.get_level_values("timestamp")
            except Exception as e:
                split_res["ablations"][ab_name] = {"err": str(e)}
        if y_test is not None and ts_test is not None and "A_rv_only" in preds_map:
            for ab_name in pooled_paired.keys():
                dfp = paired_qlike_by_time(y_test, preds_map["A_rv_only"], preds_map[ab_name], ts_test) if ab_name in preds_map else pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"])
                pooled_paired[ab_name].append(dfp)
                split_paired[ab_name].append(dfp)
        else:
            for ab_name in split_paired:
                split_paired[ab_name].append(pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"]))
        split_res["status"] = "OK"
        split_res["n_train"] = int(len(train)); split_res["n_test"] = int(len(test))
        all_results.append(split_res)
    pooled = {}
    for k, parts in pooled_paired.items():
        pooled[k] = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"])
    return all_results, pooled, split_paired


def data_sufficiency(symbols: List[str], all_results: List[Dict[str, object]]) -> Dict[str, object]:
    ok_splits = [r for r in all_results if r.get("status") == "OK"]
    test_windows = [r.get("test") for r in ok_splits]
    # 30-day non-overlapping blocks (FCLR-001 claim-worthy) not met by 14-day pre-reg design
    shortfalls = []
    if len(symbols) < 5:
        shortfalls.append(f"instruments={len(symbols)} < 5")
    shortfalls.append("no_30day_non_overlapping_test_blocks (pre-reg uses 14-day windows; Q1 2024 local data insufficient for >=3 x 30-day)")
    shortfalls.append("q1_2024_only_local_data")
    return {
        "instruments": len(symbols),
        "instruments_required": 5,
        "ok_splits": len(ok_splits),
        "test_windows": test_windows,
        "meets_claim_worthy": False,
        "shortfalls": shortfalls,
    }


def replace_section(text: str, marker: str, body: str) -> str:
    if marker in text:
        text = text.split(marker)[0].rstrip()
    return text.rstrip() + "\n\n" + marker + "\n" + body.lstrip("\n") + ("\n" if not body.endswith("\n") else "")


def update_leakage_audit(path: Path, ts: str) -> None:
    txt = path.read_text() if path.exists() else "# Leakage Audit\n"
    marker = "## Funding ablations (Gate 4, multi-split pilot, direct-variance OLS)"
    # remove stale log-ridge and old pilot entries that duplicate/confuse; keep a clean current entry
    stale_markers = [
        "## Funding ablations (Gate 4, pilot log-ridge)",
        "## Funding ablations (Gate 4, pilot direct-variance OLS)",
    ]
    for sm in stale_markers:
        if sm in txt:
            # keep header text before first stale occurrence? easier: rebuild canonical sections
            pass
    body = f"- **Updated:** {ts}\n- [x] Funding ffill last-known at/before hour (no future).\n- [x] Trailing funding stats past-only on aligned series.\n- [x] Chronological multi-split walk-forward, purge/embargo={PURGE_DAYS}d.\n- [x] Train-only normalization per split.\n- [x] Direct-variance OLS fit on train only; predictions floored at zero; no log/exp transform; no test leakage.\n- [x] Block bootstrap resamples whole UTC time blocks jointly across instruments (seed={BOOTSTRAP_SEED}, reps={BOOTSTRAP_REPS}, block={BOOTSTRAP_BLOCK_HOURS}h); no leakage.\n- [x] No basis/premium features added (unavailable/misaligned locally); NaN policy preserved, never zero-filled.\n"
    # strip all Gate 4 ablation sections and append one clean section
    lines = txt.splitlines()
    keep = []
    skip = False
    for ln in lines:
        if ln.startswith("## Funding ablations (Gate 4"):
            skip = True
            continue
        if skip and ln.startswith("## "):
            skip = False
        if not skip:
            keep.append(ln)
    txt2 = "\n".join(keep).rstrip() + "\n\n" + marker + "\n" + body
    path.write_text(txt2)


def main(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Gate 4 funding ablations (pre-registered). Defaults = v1 behavior.")
    ap.add_argument("--symbols", default="BTCUSDT,ETHUSDT,SOLUSDT,XRPUSDT")
    ap.add_argument("--start", default="2024-01-01")
    ap.add_argument("--end", default="2024-03-31")
    ap.add_argument("--horizon", type=int, default=24)
    ap.add_argument("--pre-registration", default="research_state/pre_registration_gate4_funding_multisplit_20261107.md")
    ap.add_argument("--out-suffix", default="", help="Suffix for versioned outputs, e.g. _v2_5sym; empty preserves v1 paths.")
    ap.add_argument("--experiment-id", default="GATE4-FUND-VOL-ABLATIONS-MSPLIT")
    ap.add_argument("--skip-main-summary", action="store_true")
    args = ap.parse_args(argv)

    symbols = [x.strip() for x in args.symbols.split(",") if x.strip()]
    start, end, horizon = args.start, args.end, args.horizon
    pre_reg_path = args.pre_registration
    out_suffix = args.out_suffix
    experiment_id = args.experiment_id
    RES.mkdir(parents=True, exist_ok=True)

    kpanel = load_kline_panel(symbols, start, end, horizon=horizon)
    fpanel = load_funding_panel(symbols, start, end)
    panel = add_funding_to_panel(kpanel, fpanel)

    base = [c for c in ["rv_trail_24", "rv_trail_168", "rv_trail_6"] if c in panel.columns]
    trail = [c for c in panel.columns if c.startswith(("funding_pct_", "funding_z_"))]
    ablations = {
        "A_rv_only": base[:],
        "B_rv_signed": base + ["funding_signed"],
        "C_rv_abs": base + ["funding_abs"],
        "D_rv_signed_abs": base + ["funding_signed", "funding_abs"],
        "E_rv_funding_trails": base + ["funding_signed", "funding_abs"] + trail,
    }

    all_results, pooled, split_paired = run_multisplit(panel, ablations)

    def agg(ab_name: str, key: str = "qlike") -> Optional[float]:
        vals = [r["ablations"][ab_name][key] for r in all_results if r.get("status") == "OK" and ab_name in r.get("ablations", {}) and isinstance(r["ablations"][ab_name].get(key), (int, float)) and np.isfinite(r["ablations"][ab_name].get(key))]
        return float(np.mean(vals)) if vals else None

    ci_results = {}
    for ab_name, df in pooled.items():
        ci_results[ab_name] = block_bootstrap_delta_ci(df)
    # per-split paired deltas (primary E vs A and secondaries) — instability visibility
    per_split_deltas = {}
    for ab_name, parts in split_paired.items():
        per_split_deltas[ab_name] = []
        for i, df in enumerate(parts):
            point = float(df["diff"].mean()) if df is not None and not df.empty else None
            per_split_deltas[ab_name].append({"split_id": i, "delta_qlike_vs_A": point, "n_obs": int(len(df)) if df is not None else 0})
    # EXPLORATORY sensitivity (addendum where applicable; not confirmatory, not claim-bearing)
    exploratory_sensitivity = {"label": "EXPLORATORY — not pre-registered primary; do not promote if unstable", "block_hours": {}}
    for bh in [12, 24, 48]:
        exploratory_sensitivity["block_hours"][str(bh)] = {ab: block_bootstrap_delta_ci(df, block_hours=bh) for ab, df in pooled.items()}

    suff = data_sufficiency(symbols, all_results)
    verdict = "PILOT/INCONCLUSIVE (data-sufficiency criteria not met; no claim-worthy inference)"

    summary = {
        "generated_at": now_iso(), "git_sha": git_sha(), "symbols": symbols,
        "experiment_id": experiment_id,
        "period": {"start": start, "end": end}, "horizon": horizon,
        "model": "direct-variance OLS HAR (target = forward realized VARIANCE; train-only normalization per split; no log/exp transform)",
        "pre_registration": pre_reg_path,
        "splits": [{"id": s["id"], "train": s["train"], "test": s["test"], "purge_days": PURGE_DAYS, "embargo_days": EMBARGO_DAYS} for s in PRE_REG_SPLITS],
        "aggregate": {k: {"qlike": agg(k, "qlike"), "mae": agg(k, "mae"), "rmse": agg(k, "rmse")} for k in ablations.keys()},
        "contrasts_vs_A": ci_results,
        "per_split_paired_delta_vs_A": per_split_deltas,
        "exploratory_sensitivity_block_hours": exploratory_sensitivity,
        "splits_detail": all_results,
        "data_sufficiency": suff,
        "bootstrap": {"seed": BOOTSTRAP_SEED, "reps": BOOTSTRAP_REPS, "block_hours": BOOTSTRAP_BLOCK_HOURS, "alpha": BOOTSTRAP_ALPHA, "joint_across_instruments": True, "resamples_time_blocks": True},
        "verdict": verdict,
    }
    qA = summary["aggregate"]["A_rv_only"]["qlike"]

    out_md = RES / f"evaluation_summary_funding{out_suffix}.md"
    lines = [
        "# Evaluation Summary - Funding Ablations (Gate 4, multi-split pilot)",
        "", f"**Generated:** {summary['generated_at']}", f"**Git SHA:** {summary['git_sha']}",
        f"**Pre-registration:** `{summary['pre_registration']}` (frozen before outcomes)",
        f"**Scope:** {', '.join(symbols)}, {start} to {end}, 24h forward RV, {len(PRE_REG_SPLITS)} pre-registered walk-forward splits",
        f"**Model:** {summary['model']}",
        f"**Verdict:** **{verdict}**",
        "",
        "## Data Sufficiency (honest)",
        f"- instruments={suff['instruments']} (required >=5): {'MET' if suff['instruments']>=5 else 'NOT MET'}",
        f"- claim-worthy: {suff['meets_claim_worthy']}",
    ]
    for sh in suff["shortfalls"]:
        lines.append(f"- shortfall: {sh}")
    lines += [
        "", "## Aggregate (mean across OK splits)",
        "| Ablation | QLIKE | MAE | RMSE | ΔQLIKE vs A (pooled paired) | 95% block-bootstrap CI | n_obs/n_blocks |",
        "|---|---|---|---|---|---|---|",
    ]
    for k in ablations.keys():
        a = summary["aggregate"][k]
        ci = ci_results.get(k)
        if k == "A_rv_only" or not ci:
            dstr = "—"; cistr = "—"; nstr = "—"
        else:
            dstr = f"{ci['point']}" if ci.get('point') is not None else "NA"
            cistr = f"[{ci['ci_low']}, {ci['ci_high']}]" if ci.get('ci_low') is not None else "NA"
            nstr = f"{ci.get('n_obs',0)}/{ci.get('n_blocks',0)}"
        lines.append(f"| {k} | {a['qlike']} | {a['mae']} | {a['rmse']} | {dstr} | {cistr} | {nstr} |")
    lines += ["", "## Per-Split Paired ΔQLIKE vs A (instability visibility)"]
    lines.append("| Contrast | Split 0 | Split 1 | Split 2 | n_obs (0/1/2) |")
    lines.append("|---|---:|---:|---:|---|")
    for ab in [k for k in ablations.keys() if k != "A_rv_only"]:
        rows = per_split_deltas.get(ab, [])
        vals = [(str(r["delta_qlike_vs_A"]) if r.get("delta_qlike_vs_A") is not None else "NA") for r in rows]
        ns = "/".join(str(r.get("n_obs",0)) for r in rows)
        while len(vals) < 3: vals.append("NA")
        lines.append(f"| {ab} vs A | {vals[0]} | {vals[1]} | {vals[2]} | {ns} |")
    lines += ["", "## Exploratory Sensitivity (NOT confirmatory; do not promote if unstable)", "> Block-bootstrap block size sensitivity for paired ΔQLIKE vs A. Pre-registered primary remains block=24h, seed=12345, reps=2000.", "| Contrast | block=12h CI | block=24h CI (primary) | block=48h CI |", "|---|---|---|---|"]
    for ab in [k for k in ablations.keys() if k != "A_rv_only"]:
        def _ci(bh):
            c = exploratory_sensitivity["block_hours"][str(bh)].get(ab, {})
            return f"[{c.get('ci_low')}, {c.get('ci_high')}] (pt={c.get('point')})" if c.get('ci_low') is not None else "NA"
        lines.append(f"| {ab} vs A | {_ci(12)} | {_ci(24)} | {_ci(48)} |")
    lines += ["", "## Per-Split Details"]
    for r in all_results:
        if r.get("status") != "OK":
            lines.append(f"- Split {r['split_id']} ({r.get('train')} -> {r.get('test')}): {r.get('status')} n_train={r.get('n_train')} n_test={r.get('n_test')}")
            continue
        lines.append(f"- Split {r['split_id']}: train {r['train']} | test {r['test']} | purge/embargo={PURGE_DAYS}d | n_train={r.get('n_train')} n_test={r.get('n_test')}")
        for k, v in r["ablations"].items():
            if "err" in v:
                lines.append(f"  - {k}: ERR {v['err']}")
            else:
                lines.append(f"  - {k}: qlike={v['qlike']}, mae={v['mae']}, rmse={v['rmse']}, n_feat={v['n_features']}, valid_n={v['valid_n']}")
    inst_ok = suff.get("instruments", 0) >= suff.get("instruments_required", 5)
    inst_note = f"instruments={suff.get('instruments')} ({'MET' if inst_ok else f'NOT MET; required >={suff.get("instruments_required",5)}'})"
    lines += [
        "", "## Bootstrap (pre-registered)",
        f"- Paired ΔQLIKE (alt-base; negative = better for QLIKE) with circular block bootstrap on whole UTC time blocks, jointly across instruments.",
        f"- seed={BOOTSTRAP_SEED}, reps={BOOTSTRAP_REPS}, block_hours={BOOTSTRAP_BLOCK_HOURS}, alpha={BOOTSTRAP_ALPHA}, two-sided percentile CI.",
        "", "## Leakage/Alignment Notes",
        "- Funding (8h) aligned to 1h via last-known value at/before each hour (ffill). NaN if missing.",
        "- Trailing funding pct/z computed over rolling windows on aligned series (past-only).",
        "- Chronological splits, 7d purge/embargo, train-only normalization per split.",
        "- Basis/premium not included (no aligned admissible local series verified); missing treated as NaN per policy.",
        "", "## Caveats (non-negotiable)",
        f"- **Pilot/inconclusive:** {inst_note}; Q1-2024-only local data and 14-day test windows do not satisfy FCLR-001 claim-worthy criteria (>=3 non-overlapping 30-day blocks, robust uncertainty under sufficient data coverage).",
        "- **Do NOT promote to confirmatory, do NOT claim economic value, do NOT build any overlay.** Point estimates/CIs are pilot evidence only.",
        "- Direction/magnitude can change with more data, more splits, and claim-worthy instrument/block coverage.",
    ]
    out_md.write_text("\n".join(lines) + "\n")

    if not args.skip_main_summary and not out_suffix:
        main_sum = RES / "evaluation_summary.md"
        txt = main_sum.read_text() if main_sum.exists() else ""
        addition = [
            f"**Updated:** {summary['generated_at']} (multi-split pilot, {len(PRE_REG_SPLITS)} splits, direct-variance OLS HAR; NOT claim-worthy)",
            f"**Verdict:** {verdict}",
            "", "| Ablation | QLIKE (mean) | ΔQLIKE vs A (pooled) | 95% block-bootstrap CI |", "|---|---|---|---|",
        ]
        for k in ablations.keys():
            a = summary["aggregate"][k]
            ci = ci_results.get(k)
            if k == "A_rv_only" or not ci:
                addition.append(f"| {k} | {a['qlike']} | — | — |")
            else:
                addition.append(f"| {k} | {a['qlike']} | {ci.get('point')} | [{ci.get('ci_low')}, {ci.get('ci_high')}] |")
        addition.append("")
        addition.append(f"> Shortfalls: {'; '.join(suff['shortfalls'])}. No confirmatory claim; no economic value claim.")
        main_sum.write_text(replace_section(txt, "## Funding Ablations (Gate 4)", "\n".join(addition)))

    manifest_path = RES / (f"run_manifest_funding{out_suffix}.json" if out_suffix else "run_manifest.json")
    manifest = {} if out_suffix else (json.loads((RES / "run_manifest.json").read_text()) if (RES / "run_manifest.json").exists() else {})
    manifest["last_funding_ablations"] = summary["generated_at"]
    manifest["funding_ablations_experiment_id"] = experiment_id
    manifest["funding_ablations"] = summary["aggregate"]
    manifest["funding_ablations_contrasts_vs_A"] = ci_results
    manifest["funding_ablations_note"] = f"pilot_multisplit_direct_variance_ols_inconclusive{out_suffix}"
    manifest["funding_ablations_splits"] = summary["splits"]
    manifest["funding_ablations_bootstrap"] = summary["bootstrap"]
    manifest["funding_ablations_data_sufficiency"] = suff
    manifest["funding_ablations_per_split_paired_delta_vs_A"] = per_split_deltas
    manifest["funding_ablations_exploratory_sensitivity_block_hours"] = exploratory_sensitivity
    manifest["funding_ablations_verdict"] = verdict
    manifest["funding_ablations_pre_registration"] = summary["pre_registration"]
    manifest_path.write_text(json.dumps(manifest, indent=2, default=str) + "\n")

    update_leakage_audit(RES / "leakage_audit.md", summary["generated_at"])

    print(json.dumps({"verdict": verdict, "aggregate": {k: v["qlike"] for k, v in summary["aggregate"].items()}, "primary_E_vs_A": ci_results.get("E_rv_funding_trails")}, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
