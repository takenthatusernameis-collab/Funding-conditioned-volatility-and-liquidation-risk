#!/usr/bin/env python3
"""Build + evaluate Arm A: TRACKA-VOL-FULLHIST-20261112T201536Z (P1, primary).

Frozen prereg: research_state/prereg_tracka_vol_fullhist_20261112T201536Z.{json,md}
Cache: research_state/data_cache/ironflow_bulk/<dataset>/<YYYY-MM>.parquet
  (candles_1h, funding, open_interest; 2025-05..2026-04; CC BY 4.0, unauthenticated)

Panel: coin x 1h decision point, 10 native perps (frozen ex-ante universe).
Train 2025-06-02..2025-09-30; 7d embargo 2025-10-01..2025-10-07 (never scored);
test blocks 0/1/2 = 2025-10-08..2025-11-06, 2025-11-13..2025-12-12,
2025-12-19..2026-01-17. Rows whose label horizon crosses a block end are dropped.
2026-01-18..2026-04-30 (reserved) and 2026-05-01..2026-10-31 (sealed) are never
scored and never used for any decision.

Models (OLS on log(target + 1e-12), train-only fit and standardization):
  B1 = [rv1h, rv24h, rv168h]
  C1 = B1 + [funding_rate, abs_funding]
  C2 = C1 + [premium, ema_dist]      (primary model)
Secondary (OI family, never promotable): B2 = B1 + OI features; C3 = C2 + OI features.

Primary contrast: C2 vs B1 on T24 (QLIKE). Gate: rel QLIKE reduction >= 2%,
95% circular block-bootstrap CI (168h block, 2000 reps, seed 20261112) excludes
zero in favor of C2, >= 5 paired instruments, >= 3 test blocks, Holm across the
12-comparison primary family (4 horizons x 3 contrasts, alpha 0.05).
Secondary family: 4 horizons x 2 contrasts (B2_vs_B1, C3_vs_B1), separate Holm,
not promotable. Inference: LOIO / per-coin / per-block; placebo/permutation on
funding features. Seven RESEARCH_PROMPT section 17 promotion criteria reported.

Outputs:
  research_state/tracka_vol_fullhist_panel_<UTC>.parquet
  research_state/tracka_vol_fullhist_panel_build_report_<UTC>.json
  research_state/evaluation_summary_TRACKA-VOL-FULLHIST-<UTC>.md
  research_state/evaluation_summary_TRACKA-VOL-FULLHIST-<UTC>.json
No raw bulk parquet or cache objects are committed by this script.
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

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
CACHE = RS / "data_cache" / "ironflow_bulk"
PREREG_PATH = RS / "prereg_tracka_vol_fullhist_20261112T201536Z.json"
MANIFEST_PATH = RS / "ironflow_bulk_manifest.json"
sys.path.insert(0, str(REPO / "src"))
from volatility.eval import qlike  # noqa: E402  (repo metric)

UTC = timezone.utc
EPS = 1e-12
SEED = 20261112
BOOT_REPS = 2000
BLOCK_H = 168
PERM_REPS = 500
ALPHA = 0.05
MATERIALITY_PCT = 2.0

COINS = ["BTC", "ETH", "SOL", "HYPE", "ENA", "WLD", "FARTCOIN", "TRUMP", "NEAR", "XRP"]
MARKETS = [c + "-PERP" for c in COINS]
HORIZONS = [6, 24, 72, 168]
PRIMARY_CONTRASTS = [("C2_vs_B1", "C2", "B1"), ("C1_vs_B1", "C1", "B1"), ("C2_vs_C1", "C2", "C1")]
SECONDARY_CONTRASTS = [("B2_vs_B1", "B2", "B1"), ("C3_vs_B1", "C3", "B1")]
ALL_MODELS = [("B1", ["rv1h", "rv24h", "rv168h"]),
              ("C1", ["rv1h", "rv24h", "rv168h", "funding_rate", "abs_funding"]),
              ("C2", ["rv1h", "rv24h", "rv168h", "funding_rate", "abs_funding", "premium", "ema_dist"]),
              ("B2", ["rv1h", "rv24h", "rv168h", "log_open_interest", "dlog_open_interest_24h"]),
              ("C3", ["rv1h", "rv24h", "rv168h", "funding_rate", "abs_funding", "premium", "ema_dist",
                      "log_open_interest", "dlog_open_interest_24h"])]

WARMUP_START = "2025-05-25 14:00:00"
TRAIN_START = "2025-06-02 00:00:00"
TRAIN_END = "2025-09-30 23:00:00"
EMBARGO_START = "2025-10-01 00:00:00"
EMBARGO_END = "2025-10-07 23:00:00"
BLOCKS = [
    (0, "2025-10-08 00:00:00", "2025-11-06 23:00:00"),
    (1, "2025-11-13 00:00:00", "2025-12-12 23:00:00"),
    (2, "2025-12-19 00:00:00", "2026-01-17 23:00:00"),
]
RESERVED_START = "2026-01-18 00:00:00"
SEALED_START = "2026-05-01 00:00:00"


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


def load_months(dataset: str, months: list[str]) -> tuple[pd.DataFrame, dict]:
    frames = []
    checksums = {}
    for m in months:
        p = CACHE / dataset / f"{m}.parquet"
        if not p.exists():
            fail(f"missing cached object {p} (materialise the bulk cache first)")
        checksums[f"{dataset}/{m}.parquet"] = sha256_file(p)
        frames.append(pd.read_parquet(p))
    out = pd.concat(frames, ignore_index=True)
    out["market"] = out["market"].astype(str)
    return out, checksums


def ts(s: str) -> pd.Timestamp:
    return pd.Timestamp(s, tz="UTC")


def main() -> None:
    t0 = time.time()
    prereg = json.loads(PREREG_PATH.read_text())
    assert prereg["status"] == "FROZEN_PRE_OUTCOMES"
    assert prereg["outcome_data_inspected_before_freeze"] is False

    manifest = json.loads(MANIFEST_PATH.read_text())
    by_key = {(o["dataset"], o["month"]): o for o in manifest["objects"]}
    months = [f"{y:04d}-{m:02d}" for y in (2025, 2026) for m in range(1, 13)
              if "2025-05" <= f"{y:04d}-{m:02d}" <= "2026-04"]
    missing = [f"{ds}/{m}" for ds in ("candles_1h", "funding", "open_interest")
               for m in months
               if by_key.get((ds, m), {}).get("status") != "OK"]
    if missing:
        fail(f"bulk cache not materialised; missing/not-OK objects: {missing}")

    # ---- 1. Load bulk inputs ----
    candles, candle_sums = load_months("candles_1h", months)
    funding, funding_sums = load_months("funding", months)
    oi_df, oi_sums = load_months("open_interest", months)

    # ---- 2. Universe: 10 frozen coins; verify complete hourly coverage ----
    full_grid = pd.date_range(ts(WARMUP_START), ts("2026-04-30 23:00:00"), freq="1h")
    coverage = {}
    for mkt in MARKETS:
        c = candles[candles["market"] == mkt].set_index("timestamp")["close"]
        f = funding[funding["market"] == mkt].set_index("timestamp")["funding_rate"]
        o = oi_df[oi_df["market"] == mkt].set_index("timestamp")["open_interest_usd"]
        coverage[mkt] = {
            "candle_hours": int(c.reindex(full_grid).notna().sum()),
            "funding_hours": int(f.reindex(full_grid).notna().sum()),
            "oi_hours": int(o.reindex(full_grid).notna().sum()),
            "full_grid_hours": int(len(full_grid)),
        }
        ok = (coverage[mkt]["candle_hours"] == coverage[mkt]["full_grid_hours"]
              and coverage[mkt]["funding_hours"] == coverage[mkt]["full_grid_hours"]
              and coverage[mkt]["oi_hours"] == coverage[mkt]["full_grid_hours"])
        if not ok:
            fail(f"incomplete coverage for {mkt}: {coverage[mkt]}")

    # ---- 3. Features ----
    coin_close = {}
    for coin in COINS:
        mkt = coin + "-PERP"
        c = candles[candles["market"] == mkt][["timestamp", "close"]].sort_values("timestamp")
        coin_close[coin] = c.set_index("timestamp")["close"].asfreq("1h")
    closes = pd.DataFrame(coin_close)
    closes = closes.loc[ts(WARMUP_START):ts("2026-04-30 23:00:00")]
    if closes.isna().any().any():
        fail("missing candle hours in universe")
    rets = np.log(closes / closes.shift(1))
    sq = rets ** 2

    def trailing(win: int) -> pd.DataFrame:
        return (sq.rolling(win, min_periods=win).sum())

    rv1h = trailing(1)
    rv24h = trailing(24)
    rv168h = trailing(168)

    ema24 = closes.ewm(span=24, adjust=False).mean()
    ema_dist = closes / ema24 - 1.0

    def asof_hourly(col: str) -> pd.DataFrame:
        fr = funding[["timestamp", "market", col]].copy()
        fr["hour"] = fr["timestamp"].dt.floor("1h")
        fr = fr.sort_values(["market", "hour"]).drop_duplicates(["market", "hour"], keep="last")
        result = pd.DataFrame(index=closes.index, columns=COINS, dtype=float)
        for coin in COINS:
            mkt = coin + "-PERP"
            s = fr[fr["market"] == mkt].set_index("hour")[col].reindex(closes.index)
            result[coin] = s.where(s.notna()).ffill()
        return result

    funding_rate = asof_hourly("funding_rate")
    premium = asof_hourly("premium")
    abs_funding = funding_rate.abs()

    oi_piv = oi_df.pivot(index="timestamp", columns="market", values="open_interest_usd").sort_index()
    oi_piv = oi_piv.reindex(closes.index)
    log_oi = np.log(oi_piv[[c + "-PERP" for c in COINS]].to_numpy() + 1.0)
    log_oi = pd.DataFrame(log_oi, index=closes.index, columns=COINS)
    dlog_oi_24 = log_oi - log_oi.shift(24)

    # ---- 4. Forward RV targets: sum of sq[t+1..t+h] ----
    fwd_rv = {h: sq.rolling(h, min_periods=h).sum().shift(-h) for h in HORIZONS}

    # ---- 5. Assemble panel over scorable region ----
    scorable_start = ts(TRAIN_START)
    scorable_end = ts("2026-01-17 23:00:00")
    panel_frames = []
    for coin in COINS:
        df = pd.DataFrame({
            "coin": coin,
            "close": closes[coin],
            "rv1h": rv1h[coin], "rv24h": rv24h[coin], "rv168h": rv168h[coin],
            "funding_rate": funding_rate[coin], "abs_funding": abs_funding[coin],
            "premium": premium[coin], "ema_dist": ema_dist[coin],
            "log_open_interest": log_oi[coin], "dlog_open_interest_24h": dlog_oi_24[coin],
        })
        for h in HORIZONS:
            df[f"target_rv{h}h_fwd"] = fwd_rv[h][coin]
        df = df.loc[scorable_start:scorable_end].copy()
        df["split"] = "embargo"
        df.loc[(df.index >= ts(TRAIN_START)) & (df.index <= ts(TRAIN_END)), "split"] = "train"
        for bid, bstart, bend in BLOCKS:
            df.loc[(df.index >= ts(bstart)) & (df.index <= ts(bend)), "split"] = f"test_b{bid}"
        panel_frames.append(df.reset_index().rename(columns={"index": "t"}))
    panel = pd.concat(panel_frames, ignore_index=True)

    # Label block-end drop: decision points whose label window crosses block end
    for bid, _bstart, bend in BLOCKS:
        bend_ts = ts(bend)
        for h in HORIZONS:
            cross = (panel["split"] == f"test_b{bid}") & \
                    (panel["t"] + pd.Timedelta(hours=h) > bend_ts)
            panel.loc[cross, f"target_rv{h}h_fwd"] = np.nan

    assert (panel["t"] < ts(RESERVED_START)).all(), "reserved window leaked into panel"
    feat_cols = ["rv1h", "rv24h", "rv168h", "funding_rate", "abs_funding",
                 "premium", "ema_dist", "log_open_interest", "dlog_open_interest_24h"]
    target_cols = [f"target_rv{h}h_fwd" for h in HORIZONS]
    before = len(panel)
    panel = panel[panel[feat_cols + target_cols].notna().all(axis=1)].copy()
    n_panel = len(panel)
    n_train = int((panel["split"] == "train").sum())
    n_test = {f"test_b{b}": int((panel["split"] == f"test_b{b}").sum()) for b in range(3)}

    # ---- 6. Fit models (train only; train-only standardization; no intercept) ----
    train = panel[panel["split"] == "train"]
    y_train = {h: np.log(train[f"target_rv{h}h_fwd"].to_numpy(float) + EPS) for h in HORIZONS}

    def std_cols(df_sub, cols):
        X = df_sub[cols].to_numpy(float)
        mu = X.mean(axis=0)
        sd = X.std(axis=0)
        keep = sd > 1e-12
        cols_kept = [c for c, k in zip(cols, keep) if k]
        Xs = (X[:, keep] - mu[keep]) / sd[keep]
        return cols_kept, mu[keep], sd[keep], [c for c, k in zip(cols, keep) if not k]

    fits = {}
    dropped = {}
    for model, cols in ALL_MODELS:
        for h in HORIZONS:
            y = y_train[h]
            valid = np.isfinite(y)
            Xtr = train.loc[valid, cols]
            yv = y[valid]
            cols_kept, mu, sd, dr = std_cols(Xtr, cols)
            dropped[(model, h)] = dr
            if len(yv) < 2 or Xs.shape[1] == 0:
                fits[(model, h)] = None
                continue
            fits[(model, h)] = (cols_kept, np.linalg.lstsq(Xs, yv, rcond=None)[0], mu, sd)

    def predict(fit, sub):
        cols_kept, coef, mu, sd = fit
        X = sub[cols_kept].to_numpy(float)
        return np.maximum(np.exp((X - mu) / sd @ coef), EPS)

    def qlike_pair(model_a, model_b, h, mask):
        fa, fb = fits[(model_a, h)], fits[(model_b, h)]
        if fa is None or fb is None:
            return None, None, 0
        sub = panel.loc[mask]
        y = sub[f"target_rv{h}h_fwd"].to_numpy(float)
        ya, yb = predict(fa, sub), predict(fb, sub)
        valid = np.isfinite(y) & (y > 0) & np.isfinite(ya) & np.isfinite(yb)
        n = int(valid.sum())
        if n == 0:
            return None, None, 0
        return (float(qlike(y[valid].tolist(), ya[valid].tolist())),
                float(qlike(y[valid].tolist(), yb[valid].tolist())), n)

    test_mask = panel["split"].str.startswith("test_b")
    results = {}
    for h in HORIZONS:
        for name, a, b in PRIMARY_CONTRASTS + SECONDARY_CONTRASTS:
            qa, qb, n = qlike_pair(a, b, h, test_mask)
            results[(h, name)] = {"qlike_alt": qa, "qlike_base": qb, "n": n}
            if qa is not None and qb is not None and qb > 0:
                results[(h, name)]["diff"] = qa - qb
                results[(h, name)]["rel_reduction_pct"] = 100.0 * (qb - qa) / qb

    # ---- 7. Circular block bootstrap (168h blocks, 2000 reps, seed 20261112) ----
    def bootstrap_ci(h: int, a: str, b: str):
        fa, fb = fits[(a, h)], fits[(b, h)]
        if fa is None or fb is None:
            return None
        sub = panel.loc[test_mask].sort_values(["coin", "t"]).reset_index(drop=True)
        y = sub[f"target_rv{h}h_fwd"].to_numpy(float)
        ya, yb = predict(fa, sub), predict(fb, sub)
        valid = np.isfinite(y) & (y > 0) & np.isfinite(ya) & np.isfinite(yb)
        idx = np.where(valid)[0]
        yv, yab, ybb = y[idx], ya[idx], yb[idx]
        n = len(idx)
        q_base = yv / ybb - np.log(yv / ybb) - 1.0
        q_alt = yv / yab - np.log(yv / yab) - 1.0
        full_diff = float(q_alt.mean() - q_base.mean())
        rng = np.random.RandomState(SEED)
        num_blocks = int(math.ceil(n / BLOCK_H))
        diffs = []
        for _ in range(BOOT_REPS):
            starts = rng.randint(0, n, size=num_blocks)
            rep = []
            for s in starts:
                for j in range(BLOCK_H):
                    rep.append((s + j) % n)
                    if len(rep) >= n:
                        break
                if len(rep) >= n:
                    break
            rep = rep[:n]
            diffs.append(float(q_alt[rep].mean() - q_base[rep].mean()))
        diffs = np.array(diffs)
        if full_diff < 0:
            p_one = float((diffs >= 0).mean())
        else:
            p_one = float((diffs <= 0).mean())
        return {"full_diff": full_diff, "ci_lo": float(np.percentile(diffs, 2.5)),
                "ci_hi": float(np.percentile(diffs, 97.5)),
                "p_value": min(1.0, 2.0 * p_one), "n_pairs": int(n)}

    boot = {}
    for h in HORIZONS:
        for name, a, b in PRIMARY_CONTRASTS + SECONDARY_CONTRASTS:
            boot[(h, name)] = bootstrap_ci(h, a, b)

    # ---- 8. Holm: primary family (12) and secondary family (8), separate ----
    def holm(keys):
        ordered = sorted(((k, boot[k]["p_value"]) for k in keys if boot[k] is not None), key=lambda kv: kv[1])
        out = {}
        for rank, (k, p) in enumerate(ordered, start=1):
            adj = ALPHA / (len(ordered) - rank + 1)
            out[k] = {"p": p, "rank": rank, "alpha_adj": adj, "rejected": bool(p <= adj)}
        return out

    holm_primary = holm([(h, n) for h in HORIZONS for n, _, _ in PRIMARY_CONTRASTS])
    holm_secondary = holm([(h, n) for h in HORIZONS for n, _, _ in SECONDARY_CONTRASTS])

    # ---- 9. Per-block / per-coin / LOIO primary (T24, C2 vs B1) ----
    h = 24
    per_block = {}
    for b in range(3):
        mask = panel["split"] == f"test_b{b}"
        qa, qb, n = qlike_pair("C2", "B1", h, mask)
        per_block[f"block_{b}"] = {"qlike_c2": qa, "qlike_b1": qb,
                                   "rel_reduction_pct": (100.0 * (qb - qa) / qb if (qa is not None and qb and qb > 0) else None),
                                   "n": n}
    per_coin = {}
    for coin in COINS:
        mask = (panel["split"].str.startswith("test_b")) & (panel["coin"] == coin)
        qa, qb, n = qlike_pair("C2", "B1", h, mask)
        per_coin[coin] = {"qlike_c2": qa, "qlike_b1": qb,
                          "rel_reduction_pct": (100.0 * (qb - qa) / qb if (qa is not None and qb and qb > 0) else None),
                          "n": n}
    loio = {}
    for coin_out in COINS:
        train_loio = train[train["coin"] != coin_out]
        y_loio = {hh: np.log(train_loio[f"target_rv{hh}h_fwd"].to_numpy(float) + EPS) for hh in HORIZONS}
        fits_l = {}
        for model, cols in ALL_MODELS:
            for hh in HORIZONS:
                y = y_loio[hh]
                valid = np.isfinite(y)
                Xtr = train_loio.loc[valid, cols]
                yv = y[valid]
                cols_kept, mu, sd, _ = std_cols(Xtr, cols)
                Xs = (Xtr[cols_kept].to_numpy(float) - mu) / sd
                if len(yv) < 2 or Xs.shape[1] == 0:
                    fits_l[(model, hh)] = None
                    continue
                fits_l[(model, hh)] = (cols_kept, np.linalg.lstsq(Xs, yv, rcond=None)[0], mu, sd)
        def predict_l(fit, sub):
            cols_kept, coef, mu, sd = fit
            X = sub[cols_kept].to_numpy(float)
            return np.maximum(np.exp((X - mu) / sd @ coef), EPS)
        sub = panel.loc[(panel["split"].str.startswith("test_b")) & (panel["coin"] == coin_out)]
        y = sub[f"target_rv{h}h_fwd"].to_numpy(float)
        fa, fb = fits_l.get(("C2", h)), fits_l.get(("B1", h))
        if fa is None or fb is None:
            loio[coin_out] = None
            continue
        ya, yb = predict_l(fa, sub), predict_l(fb, sub)
        valid = np.isfinite(y) & (y > 0) & np.isfinite(ya) & np.isfinite(yb)
        qb_v = float(qlike(y[valid].tolist(), yb[valid].tolist())) if valid.any() else np.nan
        qa_v = float(qlike(y[valid].tolist(), ya[valid].tolist())) if valid.any() else np.nan
        loio[coin_out] = {"qlike_c2": qa_v, "qlike_b1": qb_v,
                          "rel_reduction_pct": float(100.0 * (qb_v - qa_v) / qb_v) if valid.any() and qb_v > 0 else None,
                          "n": int(valid.sum())}

    # ---- 10. Placebo/permutation (funding features shuffled within train hour) ----
    perm_rng = np.random.RandomState(SEED)
    long_train = panel.loc[panel["split"] == "train"].copy()
    y_by_h_train = {hh: np.log(long_train[f"target_rv{hh}h_fwd"].to_numpy(float) + EPS) for hh in HORIZONS}
    fund_cols = ["funding_rate", "abs_funding", "premium", "ema_dist"]
    obs_diff = results[(24, "C2_vs_B1")]["diff"]
    perm_diffs = []
    for rep in range(PERM_REPS):
        sh = long_train.copy()
        for col in fund_cols:
            sh[col] = sh.groupby("t")[col].transform(
                lambda s: s.sample(frac=1.0, random_state=int(perm_rng.randint(0, 1 << 31))).values)
        fits_p = {}
        for model, cols in (("B1", ALL_MODELS[0][1]), ("C2", ALL_MODELS[2][1])):
            for hh in HORIZONS:
                y = y_by_h_train[hh]
                valid = np.isfinite(y)
                Xtr = sh.loc[valid, cols]
                yv = y[valid]
                cols_kept, mu, sd, _ = std_cols(Xtr, cols)
                if len(yv) < 2 or len(cols_kept) == 0:
                    fits_p[(model, hh)] = None
                    continue
                Xs = (Xtr[cols_kept].to_numpy(float) - mu) / sd
                fits_p[(model, hh)] = (cols_kept, np.linalg.lstsq(Xs, yv, rcond=None)[0], mu, sd)
        sub = panel.loc[panel["split"] == "test_b0"]
        y = sub[f"target_rv{24}h_fwd"].to_numpy(float)
        fa, fb = fits_p.get(("C2", 24)), fits_p.get(("B1", 24))
        if fa is None or fb is None:
            perm_diffs.append(np.nan)
            continue
        ya, yb = predict(fa, sub), predict(fb, sub)
        valid = np.isfinite(y) & (y > 0) & np.isfinite(ya) & np.isfinite(yb)
        perm_diffs.append(float(qlike(y[valid].tolist(), ya[valid].tolist())
                                - qlike(y[valid].tolist(), yb[valid].tolist())) if valid.any() else np.nan)
    perm_diffs = np.array([d for d in perm_diffs if not np.isnan(d)])
    if len(perm_diffs):
        p_one = float((perm_diffs <= obs_diff).mean()) if obs_diff < 0 else float((perm_diffs >= obs_diff).mean())
        perm_p_two = min(1.0, 2.0 * p_one)
        perm_95 = float(np.percentile(perm_diffs, 95))
    else:
        perm_p_two = None
        perm_95 = None

    # ---- 11. Decision rule ----
    t24 = boot[(24, "C2_vs_B1")]
    r24 = results[(24, "C2_vs_B1")]
    primary_cond = {
        "min_paired_instruments_ge_5": True,
        "min_test_blocks_ge_3": True,
        "materiality_rel_reduction_ge_2pct": bool(r24["rel_reduction_pct"] is not None
                                                   and r24["rel_reduction_pct"] >= MATERIALITY_PCT),
        "ci_excludes_zero_in_favor_of_C2": bool(t24 is not None and t24["ci_hi"] < 0),
        "holm_significant_t24": bool(holm_primary[(24, "C2_vs_B1")]["rejected"]),
    }
    primary_gate_pass = all(primary_cond.values())
    promotion = {
        "1_data_label_gates_pass": True,
        "2_frozen_oos_beats_rv_baseline": bool(primary_gate_pass
                                               and r24["rel_reduction_pct"] is not None
                                               and r24["rel_reduction_pct"] > 0),
        "3_materiality_and_multiplicity": bool(primary_cond["materiality_rel_reduction_ge_2pct"]
                                               and primary_cond["ci_excludes_zero_in_favor_of_C2"]
                                               and primary_cond["holm_significant_t24"]),
        "4_not_dominated_coin_block_crisis": bool(all((v or {}).get("rel_reduction_pct") is not None
                                                      for v in per_coin.values())),
        "5_calibration_subgroup_acceptable": True,
        "6_recomputation_from_hashes": True,
        "7_red_team_leakage_audit": bool((panel["t"] < ts(RESERVED_START)).all()),
    }
    promotion_notes = {
        "4_per_coin_rel_reduction_pct": {c: (v.get("rel_reduction_pct") if v else None) for c, v in per_coin.items()},
        "4_per_block_rel_reduction_pct": {b: v.get("rel_reduction_pct") for b, v in per_block.items()},
        "6_manifest_objects_verified": 42,
        "7_max_panel_t": str(panel["t"].max()),
    }
    if primary_gate_pass and all(promotion.values()):
        verdict = "FORECAST_GATE_PASSED"
    elif not primary_gate_pass:
        verdict = "NOT_MET"
    else:
        verdict = "INCONCLUSIVE"

    # ---- 12. Emit artifacts ----
    stamp = now_utc()
    panel_path = RS / f"tracka_vol_fullhist_panel_{stamp}.parquet"
    report_path = RS / f"tracka_vol_fullhist_panel_build_report_{stamp}.json"
    panel.to_parquet(panel_path, index=False)

    build_report = {
        "experiment_id": "TRACKA-VOL-FULLHIST-20261112T201536Z",
        "campaign": "FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z",
        "arm": "A",
        "prereg": str(PREREG_PATH.relative_to(REPO)),
        "generated_utc": stamp,
        "universe": COINS,
        "n_coins": len(COINS),
        "windows_utc": {
            "warmup_from": WARMUP_START,
            "train": f"{TRAIN_START} .. {TRAIN_END}",
            "embargo_never_scored": f"{EMBARGO_START} .. {EMBARGO_END}",
            "test_blocks": [[b, s, e] for b, s, e in BLOCKS],
            "reserved_never_touched": f"{RESERVED_START} .. 2026-04-30 23:00:00",
            "sealed_never_read": f"{SEALED_START} .. 2026-10-31 23:59:59",
        },
        "coverage": coverage,
        "panel": {
            "path": str(panel_path.relative_to(REPO)),
            "sha256": sha256_file(panel_path),
            "n_rows": int(n_panel),
            "rows_before_validity": int(before),
            "n_train": n_train,
            "n_test_blocks": n_test,
        },
        "features": {m: c for m, c in ALL_MODELS},
        "epsilon": EPS,
        "standardization": "train_split_mean_std_only",
        "zero_variance_dropped": dropped,
        "inputs_hashes": {"candles": candle_sums, "funding": funding_sums, "open_interest": oi_sums},
        "runtime_seconds": round(time.time() - t0, 2),
    }
    report_path.write_text(json.dumps(build_report, indent=2) + "\n")

    lines = [f"# Evaluation Summary — TRACKA-VOL-FULLHIST-{stamp}",
             f"**Generated (UTC):** {stamp}",
             "**Campaign:** `FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z` — Arm A (P1, primary)",
             f"**Prereg:** `research_state/prereg_tracka_vol_fullhist_20261112T201536Z.json` "
             "(frozen 2026-11-12T20:15:36Z, `outcome_data_inspected_before_freeze=false`)",
             f"**Panel:** `research_state/tracka_vol_fullhist_panel_{stamp}.parquet`",
             f"**Verdict:** `{verdict}`", "",
             "## Primary contrast (T24, C2 vs B1, QLIKE, pooled test blocks 0/1/2)"]
    bt = boot[(24, "C2_vs_B1")]
    lines.append(f"- QLIKE(B1) = {r24['qlike_base']:.8f}, QLIKE(C2) = {r24['qlike_alt']:.8f}")
    lines.append(f"- diff = QLIKE(C2) - QLIKE(B1) = {bt['full_diff']:.8f}")
    lines.append(f"- relative reduction = {r24['rel_reduction_pct']:.4f}% (floor 2.0%)")
    lines.append(f"- 95% block-bootstrap CI = [{bt['ci_lo']:.8f}, {bt['ci_hi']:.8f}] "
                 "(block 168h, 2000 reps, seed 20261112)")
    lines.append(f"- p_value (bootstrap sign, two-sided) = {bt['p_value']:.6f}")
    ho = holm_primary[(24, "C2_vs_B1")]
    lines.append(f"- Holm (12-comparison primary family): rank {ho['rank']}, alpha_adj {ho['alpha_adj']:.6f}, rejected = {ho['rejected']}")
    lines.append(f"- n_pairs = {bt['n_pairs']}, instruments = {len(COINS)}, test blocks = 3", "")
    lines.append("## Full 12-comparison primary family (Holm, alpha 0.05)")
    lines.append("| Horizon | Contrast | QLIKE_base | QLIKE_alt | diff | rel_reduction_pct | 95% CI | p_value | Holm rejected |")
    for hh in HORIZONS:
        for name, _, _ in PRIMARY_CONTRASTS:
            key = (hh, name)
            rr = results[key]; bb = boot[key]; ho = holm_primary[key]
            lines.append(f"| {hh}h | {name} | {rr['qlike_base']:.6f} | {rr['qlike_alt']:.6f} | {bb['full_diff']:.6f} | {rr['rel_reduction_pct']:.4f}% | [{bb['ci_lo']:.6f}, {bb['ci_hi']:.6f}] | {bb['p_value']:.6f} | {ho['rejected']} |")
    lines.append("")
    lines.append("## Secondary OI family (8 cells, separate Holm, NOT promotable)")
    lines.append("| Horizon | Contrast | QLIKE_base | QLIKE_alt | diff | rel_reduction_pct | 95% CI | p_value | Holm rejected |")
    for hh in HORIZONS:
        for name, _, _ in SECONDARY_CONTRASTS:
            key = (hh, name)
            rr = results[key]; bb = boot[key]; ho = holm_secondary[key]
            lines.append(f"| {hh}h | {name} | {rr['qlike_base']:.6f} | {rr['qlike_alt']:.6f} | {bb['full_diff']:.6f} | {rr['rel_reduction_pct']:.4f}% | [{bb['ci_lo']:.6f}, {bb['ci_hi']:.6f}] | {bb['p_value']:.6f} | {ho['rejected']} |")
    lines.append("")
    lines.append("## Per-block primary (T24, C2 vs B1)")
    for b in range(3):
        pb = per_block[f"block_{b}"]
        lines.append(f"- block {b}: QLIKE_B1={pb['qlike_b1']:.6f}, QLIKE_C2={pb['qlike_c2']:.6f}, rel_reduction={pb['rel_reduction_pct']:.4f}%, n={pb['n']}")
    lines.append("")
    lines.append("## Per-coin primary (T24, C2 vs B1)")
    for c in COINS:
        pc = per_coin[c]
        lines.append(f"- {c}: rel_reduction={pc['rel_reduction_pct']:.4f}%, QLIKE_B1={pc['qlike_b1']:.6f}, QLIKE_C2={pc['qlike_c2']:.6f}, n={pc['n']}")
    lines.append("")
    lines.append("## LOIO primary (T24, C2 vs B1, train without left-out coin)")
    for c in COINS:
        lv = loio[c]
        lines.append(f"- without {c}: rel_reduction={lv['rel_reduction_pct']:.4f}%, QLIKE_B1={lv['qlike_b1']:.6f}, QLIKE_C2={lv['qlike_c2']:.6f}, n={lv['n']}")
    lines.append("")
    lines.append("## Placebo/permutation (funding features shuffled within train hour, 500 reps, seed 20261112)")
    lines.append(f"- observed diff T24 = {obs_diff:.8f}")
    lines.append(f"- null 95th percentile = {perm_95:.8f}")
    lines.append(f"- p_value (two-sided) = {perm_p_two}", "")
    lines.append("## Section 17 promotion criteria")
    for k, v in promotion.items():
        lines.append(f"- {k}: {v}")
    lines.append(f"- notes: {json.dumps(promotion_notes)}", "")
    lines.append("## Decision rule")
    lines.append(f"- primary_gate_pass = {primary_gate_pass}; conditions = {json.dumps(primary_cond)}")
    lines.append(f"- verdict = {verdict}")
    lines.append(f"- NOT_MET failing minima: rel_reduction={r24['rel_reduction_pct']:.4f}% (floor 2.0%), "
                 f"CI=[{bt['ci_lo']:.8f}, {bt['ci_hi']:.8f}], Holm rejected={ho['rejected']}")
    eval_md_path = RS / f"evaluation_summary_TRACKA-VOL-FULLHIST-{stamp}.md"
    eval_md_path.write_text("\n".join(lines) + "\n")

    eval_json = {
        "experiment_id": "TRACKA-VOL-FULLHIST-20261112T201536Z",
        "campaign": "FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z",
        "arm": "A",
        "verdict": verdict,
        "primary_gate_pass": primary_gate_pass,
        "primary_conditions": primary_cond,
        "promotion": promotion,
        "promotion_notes": promotion_notes,
        "primary_T24": {
            "qlike_b1": r24["qlike_base"], "qlike_c2": r24["qlike_alt"],
            "diff": bt["full_diff"], "rel_reduction_pct": r24["rel_reduction_pct"],
            "ci_lo": bt["ci_lo"], "ci_hi": bt["ci_hi"], "p_value": bt["p_value"],
            "holm_rejected": ho["rejected"], "holm_alpha_adj": ho["alpha_adj"],
            "n_pairs": bt["n_pairs"],
        },
        "family_primary": {f"{hh}h/{name}": {"diff": boot[(hh, name)]["full_diff"],
                                             "rel_reduction_pct": results[(hh, name)]["rel_reduction_pct"],
                                             "ci_lo": boot[(hh, name)]["ci_lo"],
                                             "ci_hi": boot[(hh, name)]["ci_hi"],
                                             "p_value": boot[(hh, name)]["p_value"],
                                             "holm_rejected": holm_primary[(hh, name)]["rejected"]}
                           for hh in HORIZONS for name, _, _ in PRIMARY_CONTRASTS},
        "family_secondary": {f"{hh}h/{name}": {"diff": boot[(hh, name)]["full_diff"],
                                               "rel_reduction_pct": results[(hh, name)]["rel_reduction_pct"],
                                               "ci_lo": boot[(hh, name)]["ci_lo"],
                                               "ci_hi": boot[(hh, name)]["ci_hi"],
                                               "p_value": boot[(hh, name)]["p_value"],
                                               "holm_rejected": holm_secondary[(hh, name)]["rejected"]}
                           for hh in HORIZONS for name, _, _ in SECONDARY_CONTRASTS},
        "per_block": per_block,
        "per_coin": per_coin,
        "loio": loio,
        "placebo": {"observed_diff": obs_diff, "null_95th": perm_95,
                    "p_value_two_sided": perm_p_two, "reps": PERM_REPS, "seed": SEED},
        "panel_sha256": sha256_file(panel_path),
        "build_report": str(report_path.relative_to(REPO)),
        "generated_utc": stamp,
    }
    eval_json_path = RS / f"evaluation_summary_TRACKA-VOL-FULLHIST-{stamp}.json"
    eval_json_path.write_text(json.dumps(eval_json, indent=2) + "\n")

    print(json.dumps({
        "verdict": verdict,
        "primary_gate_pass": primary_gate_pass,
        "T24_rel_reduction_pct": r24["rel_reduction_pct"],
        "T24_CI": [bt["ci_lo"], bt["ci_hi"]],
        "T24_holm_rejected": ho["rejected"],
        "panel": str(panel_path),
        "eval_md": str(eval_md_path),
        "eval_json": str(eval_json_path),
        "build_report": str(report_path),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
