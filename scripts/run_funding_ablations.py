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
import re
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

CACHE = RES / "data_cache"


# --- Confirmatory provenance guard (FCLR-014/FCLR-016) ---
# 2025+ cache windows lack admissible confirmatory provenance (FCLR-014 NO-GO).
# Fail-closed: confirmatory-labeled runs touching unprovenanced 2025+ data must refuse.
PROVENANCED_CONFIRMATORY_RANGES = [
    # (start_inclusive, end_inclusive) — 2024-04..09 identity-verified vs Binance Vision (FCLR-015)
    ("2024-04-01", "2024-09-30"),
]
UNPROVENANCED_CONFIRMATORY_PREFIXES = ("2025", "2026")  # 2025+ cache; 2026-01..06/10 candidates NO-GO per FCLR-014

def _range_overlaps_unprovenanced(start: str, end: str) -> bool:
    try:
        s = str(start)[:10]; e = str(end)[:10]
    except Exception:
        return True  # fail closed
    # any 2025+ year in range
    for pref in UNPROVENANCED_CONFIRMATORY_PREFIXES:
        if s[:4] <= pref <= e[:4] or s.startswith(pref) or e.startswith(pref):
            # 2024 is partially provenanced; 2025+ is not
            if pref >= "2025":
                return True
    return False

def _is_confirmatory_intent(experiment_id: str, pre_registration: str, out_suffix: str, confirmatory_flag: bool) -> bool:
    if confirmatory_flag:
        return True
    blob = f"{experiment_id} {pre_registration} {out_suffix}".lower()
    if "exploratory" in blob or "pilot" in blob:
        return False
    # v5+ confirmatory preregs / explicit confirmatory naming
    if "confirmatory" in blob or re.search(r"\bv[5-9]\b", blob):
        return True
    return False

def check_confirmatory_provenance(start: str, end: str, experiment_id: str, pre_registration: str,
                                  out_suffix: str, confirmatory_flag: bool = False,
                                  provenance_manifest: Optional[str] = None) -> Optional[str]:
    """Return error message if confirmatory run is inadmissible; else None."""
    if not _is_confirmatory_intent(experiment_id, pre_registration, out_suffix, confirmatory_flag):
        return None
    if provenance_manifest:
        mp = Path(provenance_manifest)
        if not mp.exists():
            return f"CONFIRMATORY PROVENANCE GUARD: --provenance-manifest not found: {mp}"
        try:
            m = json.loads(mp.read_text())
        except Exception as e:
            return f"CONFIRMATORY PROVENANCE GUARD: cannot read provenance manifest: {e}"
        if not m.get("cache_identity_vs_binance_vision", "").startswith("GO") and not m.get("confirmatory_provenance_go"):
            return f"CONFIRMATORY PROVENANCE GUARD: manifest not GO: {mp}"
        # manifest accepted - caller responsible for scope match; record in run
        return None
    if _range_overlaps_unprovenanced(start, end):
        return (
            "CONFIRMATORY PROVENANCE GUARD (FCLR-014 NO-GO): Refusing confirmatory-labeled run on "
            f"unprovenanced 2025+ cache window {start}..{end} (experiment={experiment_id}). "
            "2025-01..2025-12,2026-01..06,2026-10 cache months lack admissible confirmatory provenance/license evidence "
            "(research_state/fclr014_local_audit/fclr014_provenance_decision_20261107T133102Z.md). "
            "Provide --provenance-manifest with verified Binance Vision identity+licensing evidence, or run as exploratory/pilot. "
            "Do NOT run claim outcomes on unprovenanced data."
        )
    # 2024 ranges outside FCLR-015 verified slice: fail closed for confirmatory
    s, e = str(start)[:10], str(end)[:10]
    in_proven = any(s >= a and e <= b for a, b in PROVENANCED_CONFIRMATORY_RANGES)
    if not in_proven and not (s < "2025" and e < "2025"):
        pass
    elif not in_proven and s.startswith("2024"):
        # 2024 but outside verified 04-09: advisory but allow only if not overlapping consumed? fail closed
        return (
            f"CONFIRMATORY PROVENANCE GUARD: 2024 range {start}..{end} outside FCLR-015 identity-verified slice "
            f"{PROVENANCED_CONFIRMATORY_RANGES} and may overlap consumed/confounded windows; provide --provenance-manifest or use exploratory."
        )
    return None

PRE_REG_SPLITS_V1 = [
    {"id": 0, "train": ("2024-01-01T00:00:00+00:00", "2024-01-28T23:59:59+00:00"), "test": ("2024-02-05T00:00:00+00:00", "2024-02-18T23:59:59+00:00")},
    {"id": 1, "train": ("2024-01-15T00:00:00+00:00", "2024-02-11T23:59:59+00:00"), "test": ("2024-02-19T00:00:00+00:00", "2024-03-03T23:59:59+00:00")},
    {"id": 2, "train": ("2024-01-29T00:00:00+00:00", "2024-02-25T23:59:59+00:00"), "test": ("2024-03-04T00:00:00+00:00", "2024-03-17T23:59:59+00:00")},
]
PRE_REG_SPLITS_V3_30D = [
    {"id": 0, "train": ("2024-04-01T00:00:00+00:00", "2024-05-07T23:59:59+00:00"), "test": ("2024-05-15T00:00:00+00:00", "2024-06-13T23:59:59+00:00")},
    {"id": 1, "train": ("2024-04-01T00:00:00+00:00", "2024-06-06T23:59:59+00:00"), "test": ("2024-06-14T00:00:00+00:00", "2024-07-13T23:59:59+00:00")},
    {"id": 2, "train": ("2024-04-01T00:00:00+00:00", "2024-07-06T23:59:59+00:00"), "test": ("2024-07-14T00:00:00+00:00", "2024-08-12T23:59:59+00:00")},
    {"id": 3, "train": ("2024-04-01T00:00:00+00:00", "2024-08-05T23:59:59+00:00"), "test": ("2024-08-13T00:00:00+00:00", "2024-09-11T23:59:59+00:00")},
]
PRE_REG_SPLITS = PRE_REG_SPLITS_V1  # default/v1; tests import this name
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


def _iter_readable_sources(patterns: List[str], prefer_csv: bool = True, include_cache: bool = False,
                           dedupe_by_stem: bool = True, canonical_sub: str = "klines-") -> List[Path]:
    """Deterministic local sources (CSV/ZIP). RAW primary; cache opt-in to preserve v1 behavior.

    When ``dedupe_by_stem`` is set, files sharing a stem (e.g. the same contract-day) are
    collapsed to one representative. Canonical contract-kline archives live under a
    ``<SYM>_<YYYY_MM>/klines-<YYYY-MM-DD>/`` directory; the same date also appears as a
    top-level placeholder zip and inside mark/index/premium directories. The canonical
    copy carries real volume; the placeholders are zero-volume stubs. Keep only the
    canonical copy to avoid duplicate (symbol, timestamp) rows and the downstream
    "cannot reindex on duplicate labels" failure in the funding merge.
    """
    seen = set()
    out: List[Path] = []
    roots = [RAW]
    if include_cache and CACHE.exists():
        roots.append(CACHE)
    for root in roots:
        for pat in patterns:
            for fp in sorted(root.glob(pat)):
                if not fp.is_file():
                    continue
                key = fp.resolve()
                if key in seen:
                    continue
                seen.add(key)
                out.append(fp)
    if prefer_csv:
        csvs = [p for p in out if p.suffix.lower() == '.csv']
        zips = [p for p in out if p.suffix.lower() == '.zip']
        stems = {p.stem for p in csvs}
        zips = [z for z in zips if z.stem not in stems]
        out = sorted(csvs) + sorted(zips)
    if dedupe_by_stem:
        by_stem: Dict[str, List[Path]] = {}
        for p in out:
            by_stem.setdefault(p.stem, []).append(p)
        out = []
        for stem, cands in by_stem.items():
            if len(cands) == 1:
                out.append(cands[0])
                continue
            # Prefer a path that lives under the canonical klines- directory.
            canon = [c for c in cands if canonical_sub in c.parent.name]
            out.append(canon[0] if canon else sorted(cands, key=lambda x: str(x))[0])
    return sorted(out, key=lambda x: (x.suffix != '.csv', str(x)))


def _load_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == '.zip':
        import zipfile
        with zipfile.ZipFile(path) as zf:
            names = [n for n in zf.namelist() if n.lower().endswith('.csv')]
            if not names:
                raise ValueError(f'no csv in {path}')
            # deterministic: first csv
            with zf.open(sorted(names)[0]) as f:
                return pd.read_csv(f)
    return pd.read_csv(path)


def load_funding_series(symbols: List[str], start: str, end: str, include_cache: bool = False) -> pd.DataFrame:
    ensure_extracted(symbols)
    frames = []
    for sym in symbols:
        flist = []
        pats = [f"{sym}-fundingRate-*.csv", f"{sym}-fundingRate-*.zip",
                f"{sym}_*/{sym}-fundingRate-*.csv", f"{sym}_*/{sym}-fundingRate-*.zip",
                f"{sym}_*/*/{sym}-fundingRate-*.csv", f"{sym}_*/*/{sym}-fundingRate-*.zip"]
        for fp in _iter_readable_sources(pats, include_cache=include_cache):
            if sym not in fp.name or 'fundingRate' not in fp.name:
                continue
            try:
                df = _load_table(fp)
                df = df.rename(columns={c: c.strip() for c in df.columns})
                if 'calc_time' not in df.columns:
                    continue
                df['calc_time'] = loader._to_utc_ms(df['calc_time'])
                df = df.sort_values('calc_time').drop_duplicates('calc_time', keep='last').set_index('calc_time')
                if 'last_funding_rate' in df.columns:
                    df['last_funding_rate'] = pd.to_numeric(df['last_funding_rate'], errors='coerce')
                if 'funding_interval_hours' in df.columns:
                    df['funding_interval_hours'] = pd.to_numeric(df['funding_interval_hours'], errors='coerce').astype('Int64')
                flist.append(df)
            except Exception:
                continue
        if not flist:
            continue
        fdf = pd.concat(flist).sort_index()
        fdf = fdf.loc[(fdf.index >= pd.Timestamp(start, tz='UTC')) & (fdf.index <= pd.Timestamp(end, tz='UTC') + pd.Timedelta(days=1))]
        fdf = fdf.reset_index().rename(columns={'calc_time': 'timestamp'})
        fdf['symbol'] = sym
        frames.append(fdf)
    if not frames:
        raise RuntimeError('No funding data loaded')
    panel = pd.concat(frames, ignore_index=True)
    panel['timestamp'] = pd.to_datetime(panel['timestamp'], utc=True)
    return panel.set_index(['symbol', 'timestamp']).sort_index()


def load_kline_series(symbols: List[str], start: str, end: str, horizon: int = 24, include_cache: bool = False) -> pd.DataFrame:
    ensure_extracted(symbols)
    frames = []
    for sym in symbols:
        klist = []
        pats = [f"{sym}-1h-*.csv", f"{sym}-1h-*.zip",
                f"{sym}_*/{sym}-1h-*.csv", f"{sym}_*/{sym}-1h-*.zip",
                f"{sym}_*/klines-*/{sym}-1h-*.csv", f"{sym}_*/klines-*/{sym}-1h-*.zip"]
        for fp in _iter_readable_sources(pats, include_cache=include_cache):
            if sym not in fp.name or '1h' not in fp.name or 'fundingRate' in fp.name:
                continue
            # skip mark/index/premium kline variants
            if any(x in str(fp) for x in ('indexPriceKlines', 'markPriceKlines', 'premiumIndexKlines')):
                continue
            try:
                df = _load_table(fp)
                df = df.rename(columns={c: c.strip() for c in df.columns})
                if 'open_time' not in df.columns:
                    continue
                df['open_time'] = loader._to_utc_ms(df['open_time'])
                df = df.sort_values('open_time').drop_duplicates('open_time', keep='last').set_index('open_time')
                for col in ['open', 'high', 'low', 'close', 'volume']:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                c = pd.to_numeric(df.get('close'), errors='coerce')
                if c is None or len(c) == 0:
                    continue
                pos = c[c > 0]
                if len(pos) == 0 or (c <= 0).mean() > 0.2:
                    continue
                df.loc[c <= 0, 'close'] = np.nan
                df['_file_med_close'] = float(pos.median())
                klist.append(df)
            except Exception:
                continue
        if not klist:
            continue
        kdf = pd.concat(klist).sort_index()
        # deterministic integrity: drop file-slices whose median close is wildly inconsistent
        # with symbol's robust center (catches corrupt local cache artifacts, e.g. BTC close ~1e-3).
        # This is a data-quality guard, not outcome tuning; threshold is scale-ratio only.
        if '_file_med_close' in kdf.columns:
            ref = pd.to_numeric(kdf['_file_med_close'], errors='coerce')
            center = float(ref[ref > 0].median()) if (ref > 0).any() else None
            if center and center > 0:
                bad = (ref <= 0) | (ref < center / 500.0) | (ref > center * 500.0)
                kdf = kdf.loc[~bad].copy()
            kdf = kdf.drop(columns=['_file_med_close'], errors='ignore')
        kdf = kdf.loc[(kdf.index >= pd.Timestamp(start, tz='UTC')) & (kdf.index <= pd.Timestamp(end, tz='UTC') + timedelta(days=1))]
        kdf = vf.add_rv_features(kdf, short_windows=[6, 24], long_windows=[168])
        kdf['target_rv'] = vf.forward_rv(kdf['close'], horizon=horizon)
        kdf['rv_lag'] = kdf['rv_trail_24'].shift(1)
        kdf = kdf.reset_index().rename(columns={'open_time': 'timestamp'})
        kdf['symbol'] = sym
        frames.append(kdf)
    if not frames:
        raise RuntimeError('No kline data loaded')
    panel = pd.concat(frames, ignore_index=True)
    panel['timestamp'] = pd.to_datetime(panel['timestamp'], utc=True)
    return panel.set_index(['symbol', 'timestamp']).sort_index()


def load_funding_panel(symbols: List[str], start: str, end: str, include_cache: bool = False) -> pd.DataFrame:
    return load_funding_series(symbols, start, end, include_cache=include_cache)


def load_kline_panel(symbols: List[str], start: str, end: str, horizon: int = 24, include_cache: bool = False) -> pd.DataFrame:
    return load_kline_series(symbols, start, end, horizon=horizon, include_cache=include_cache)


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


def build_prereg_splits(splits: Optional[List[Dict[str, object]]] = None) -> List[wf.SplitBounds]:
    src = PRE_REG_SPLITS if splits is None else splits
    return [
        wf.SplitBounds(
            train=s["train"], validation=s["test"], test=s["test"],
            purge_days=PURGE_DAYS, embargo_days=EMBARGO_DAYS,
        )
        for s in src
    ]


def run_multisplit(panel: pd.DataFrame, ablations: Dict[str, List[str]], split_defs: Optional[List[Dict[str, object]]] = None) -> Tuple[List[Dict[str, object]], Dict[str, pd.DataFrame], Dict[str, List[pd.DataFrame]]]:
    split_defs = PRE_REG_SPLITS if split_defs is None else split_defs
    splits = build_prereg_splits(split_defs)
    idx = panel.index.get_level_values("timestamp")
    all_results: List[Dict[str, object]] = []
    pooled_paired: Dict[str, List[pd.DataFrame]] = {k: [] for k in ablations.keys() if k != "A_rv_only"}
    split_paired: Dict[str, List[pd.DataFrame]] = {k: [] for k in ablations.keys() if k != "A_rv_only"}
    for i, sp in enumerate(splits):
        meta = split_defs[i]
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


def _test_days(win) -> Optional[int]:
    try:
        a = pd.Timestamp(win[0]); b = pd.Timestamp(win[1])
        return int((b.normalize() - a.normalize()).days) + 1
    except Exception:
        return None

def data_sufficiency(symbols: List[str], all_results: List[Dict[str, object]], split_defs: Optional[List[Dict[str, object]]] = None) -> Dict[str, object]:
    split_defs = PRE_REG_SPLITS if split_defs is None else split_defs
    ok_splits = [r for r in all_results if r.get("status") == "OK"]
    test_windows = [r.get("test") for r in ok_splits]
    ok_30 = [w for w in test_windows if _test_days(w) is not None and _test_days(w) >= 30]
    shortfalls = []
    if len(symbols) < 5:
        shortfalls.append(f"instruments={len(symbols)} < 5")
    if len(ok_30) < 3:
        # honest about actual design
        td = [_test_days(s.get('test')) for s in split_defs]
        shortfalls.append(f"insufficient_30day_non_overlapping_test_blocks (ok_30d={len(ok_30)}, required>=3, split_test_days={td})")
    # local admissible cache span note (not a hard fail by itself, but material)
    span_note = 'local_admissible_cache_data_only'
    meets = len(symbols) >= 5 and len(ok_30) >= 3 and len(ok_splits) == len(split_defs)
    return {
        "instruments": len(symbols),
        "instruments_required": 5,
        "ok_splits": len(ok_splits),
        "ok_30day_splits": len(ok_30),
        "test_windows": test_windows,
        "split_test_days": [_test_days(s.get('test')) for s in split_defs],
        "span_note": span_note,
        "meets_claim_worthy_data_sufficiency": meets,
        "meets_claim_worthy": meets,
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
    ap.add_argument("--include-cache", action="store_true", help="Search research_state/data_cache for local admissible files (v3/extended runs).")
    ap.add_argument("--confirmatory", action="store_true", help="Assert confirmatory intent; triggers provenance guard (fail-closed on unprovenanced 2025+).")
    ap.add_argument("--provenance-manifest", default=None, help="Path to verified provenance manifest for confirmatory runs.")
    args = ap.parse_args(argv)

    prov_err = check_confirmatory_provenance(
        args.start, args.end, args.experiment_id, args.pre_registration, args.out_suffix,
        confirmatory_flag=bool(getattr(args, "confirmatory", False)),
        provenance_manifest=getattr(args, "provenance_manifest", None),
    )
    if prov_err:
        print(json.dumps({"status": "REFUSED", "guard": "confirmatory_provenance_fclr014", "error": prov_err, "start": args.start, "end": args.end}, indent=2), file=sys.stderr)
        return 2

    symbols = [x.strip() for x in args.symbols.split(",") if x.strip()]
    start, end, horizon = args.start, args.end, args.horizon
    pre_reg_path = args.pre_registration
    out_suffix = args.out_suffix
    experiment_id = args.experiment_id
    RES.mkdir(parents=True, exist_ok=True)
    # select split defs: v3/v4 30-day 2024-04..09 design when indicated; v4 is exploratory on confounded slice (per prereg)
    _low = ((out_suffix or '') + ' ' + (pre_reg_path or '')).lower()
    use_30d_0409 = ('v3' in _low and '30d' in _low) or ('v4' in _low)
    split_defs = PRE_REG_SPLITS_V3_30D if use_30d_0409 else PRE_REG_SPLITS
    include_cache = bool(use_30d_0409 or getattr(args, 'include_cache', False))

    kpanel = load_kline_panel(symbols, start, end, horizon=horizon, include_cache=include_cache)
    fpanel = load_funding_panel(symbols, start, end, include_cache=include_cache)
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

    all_results, pooled, split_paired = run_multisplit(panel, ablations, split_defs=split_defs)

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

    suff = data_sufficiency(symbols, all_results, split_defs=split_defs)
    primary_ci = ci_results.get("E_rv_funding_trails") or {}
    ci_spans_0 = (primary_ci.get("ci_low") is not None and primary_ci.get("ci_high") is not None and primary_ci["ci_low"] <= 0 <= primary_ci["ci_high"])
    if not suff.get("meets_claim_worthy_data_sufficiency"):
        verdict = "PILOT/INCONCLUSIVE (data-sufficiency criteria not met; no claim-worthy inference)"
    elif ci_spans_0:
        verdict = "DATA-SUFFICIENT PILOT / INCONCLUSIVE ON PRIMARY CONTRAST (pre-registered 30-day blocks met; E vs A CI spans 0; no improvement claim)"
    else:
        verdict = "DATA-SUFFICIENT (30-day blocks met) — primary E vs A CI excludes 0 in observed run; requires robustness/leakage review before confirmatory claim; no economic value/overlay claim"

    summary = {
        "generated_at": now_iso(), "git_sha": git_sha(), "symbols": symbols,
        "experiment_id": experiment_id,
        "period": {"start": start, "end": end}, "horizon": horizon,
        "model": "direct-variance OLS HAR (target = forward realized VARIANCE; train-only normalization per split; no log/exp transform)",
        "pre_registration": pre_reg_path,
        "splits": [{"id": s["id"], "train": s["train"], "test": s["test"], "purge_days": PURGE_DAYS, "embargo_days": EMBARGO_DAYS} for s in split_defs],
        "aggregate": {k: {"qlike": agg(k, "qlike"), "mae": agg(k, "mae"), "rmse": agg(k, "rmse")} for k in ablations.keys()},
        "contrasts_vs_A": ci_results,
        "per_split_paired_delta_vs_A": per_split_deltas,
        "exploratory_sensitivity_block_hours": exploratory_sensitivity,
        "splits_detail": all_results,
        "data_sufficiency": suff,
        "bootstrap": {"seed": BOOTSTRAP_SEED, "reps": BOOTSTRAP_REPS, "block_hours": BOOTSTRAP_BLOCK_HOURS, "alpha": BOOTSTRAP_ALPHA, "joint_across_instruments": True, "resamples_time_blocks": True},
        "verdict": verdict,
        "primary_contrast_inconclusive_ci_spans_zero": ( (ci_results.get("E_rv_funding_trails") or {}).get("ci_low") is not None and (ci_results.get("E_rv_funding_trails") or {}).get("ci_high") is not None and (ci_results.get("E_rv_funding_trails") or {})["ci_low"] <= 0 <= (ci_results.get("E_rv_funding_trails") or {})["ci_high"] ),
    }
    qA = summary["aggregate"]["A_rv_only"]["qlike"]

    out_md = RES / f"evaluation_summary_funding{out_suffix}.md"
    lines = [
        "# Evaluation Summary - Funding Ablations (Gate 4, multi-split pilot)",
        "", f"**Generated:** {summary['generated_at']}", f"**Git SHA:** {summary['git_sha']}",
        f"**Pre-registration:** `{summary['pre_registration']}` (frozen before outcomes)",
        f"**Scope:** {', '.join(symbols)}, {start} to {end}, 24h forward RV, {len(split_defs)} pre-registered walk-forward splits",
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
    nsp=len(split_defs); header = "| Contrast | " + " | ".join([f"Split {i}" for i in range(nsp)]) + f" | n_obs ({'/'.join(str(i) for i in range(nsp))}) |"; lines.append(header)
    lines.append("|---|" + "|".join(["---:"]*nsp) + "|---|")
    for ab in [k for k in ablations.keys() if k != "A_rv_only"]:
        rows = per_split_deltas.get(ab, [])
        vals = [(str(r["delta_qlike_vs_A"]) if r.get("delta_qlike_vs_A") is not None else "NA") for r in rows]
        ns = "/".join(str(r.get("n_obs",0)) for r in rows)
        while len(vals) < nsp: vals.append("NA")
        lines.append(f"| {ab} vs A | " + " | ".join(vals[:nsp]) + f" | {ns} |")
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
    ds_ok = suff.get("meets_claim_worthy_data_sufficiency")
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
        f"- **Verdict:** {verdict}",
        f"- **Data sufficiency:** {inst_note}; ok_30day_splits={suff.get('ok_30day_splits')} (required>=3) => meets_claim_worthy_data_sufficiency={ds_ok}.",
        "- **No economic value claim, no overlay, no Track A linkage.** Observed metrics are out-of-sample forecast evidence under pre-registered design; instability across splits/instrument sets must be reported honestly.",
        "- If any leakage/alignment doubt exists, treat as non-confirmatory.",
    ]
    out_md.write_text("\n".join(lines) + "\n")

    if not args.skip_main_summary and not out_suffix:
        main_sum = RES / "evaluation_summary.md"
        txt = main_sum.read_text() if main_sum.exists() else ""
        addition = [
            f"**Updated:** {summary['generated_at']} (multi-split, {len(split_defs)} splits, direct-variance OLS HAR; verdict={verdict})",
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
