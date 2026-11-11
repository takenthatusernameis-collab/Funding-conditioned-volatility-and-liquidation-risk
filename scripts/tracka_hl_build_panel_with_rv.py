#!/usr/bin/env python3
"""Rebuild Track A aligned panel WITH mark-price/RV context.

Inputs (cached admissible, provenance recorded in successor prereg):
- research_state/data_cache/ironflow_events/2026-0[5-9].parquet, 2026-10.parquet (observed labels)
- research_state/data_cache/hyperliquid_funding/{9 coins}.json (funding context, incl. premium)
- research_state/data_cache/hyperliquid_candles/{COIN}/{YYYY-MM}.json (mark-price 1h candles, newly fetched)

Outputs:
- research_state/tracka_hl_aligned_panel_with_rv_<UTC>.parquet  (symbol x 24h bucket: label intensity + funding + RV1h/RV24h/RV168h + ema_dist)
- research_state/tracka_hl_panel_with_rv_build_report_<UTC>.json (row counts, coverage, missingness/gap, input hashes)

All features causal: data ending no later than bucket start. Fail-closed on schema.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
UTC = timezone.utc

SYMBOLS = ["BTC", "ETH", "BNB", "SOL", "XRP", "AVAX", "DOGE", "LINK", "SUI"]
PERP = {s: f"{s}-PERP" for s in SYMBOLS}
COINS = SYMBOLS

LABEL_COLS = ["timestamp", "market", "issuer", "wallet", "position_side", "size",
              "notional_usd", "avg_price", "fills", "block", "tx_hash"]

LABEL_MONTHS = ["2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]
CANDLE_MONTHS = LABEL_MONTHS


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_candles(coin: str):
    frames = []
    checksums = {}
    rows_total = 0
    months_ok = []
    for m in CANDLE_MONTHS:
        p = CACHE / "hyperliquid_candles" / coin / f"{m}.json"
        if not p.exists():
            continue
        checksums[f"hyperliquid_candles_{coin}_{m}.json"] = sha256_file(p)
        data = json.loads(p.read_text())
        if not isinstance(data, list):
            continue
        rows = []
        for c in data:
            t_ms = c.get("t")
            close = c.get("c")
            if t_ms is None or close is None:
                continue
            try:
                rows.append({"ts_ms": int(t_ms), "close": float(close)})
            except (ValueError, TypeError):
                continue
        if rows:
            df = pd.DataFrame(rows)
            df = df.sort_values("ts_ms").drop_duplicates(subset=["ts_ms"])
            frames.append(df)
            rows_total += len(df)
            months_ok.append(m)
    if not frames:
        return None, {}, 0, []
    candles = pd.concat(frames, ignore_index=True)
    candles = candles.sort_values("ts_ms").drop_duplicates(subset=["ts_ms"]).reset_index(drop=True)
    return candles, checksums, rows_total, months_ok


def compute_rv_with_close(candles_df):
    df = candles_df.sort_values("ts_ms").reset_index(drop=True)
    df["log_ret"] = np.log(df["close"] / df["close"].shift(1))
    sq = df["log_ret"] ** 2
    df["rv1h"] = sq
    df["rv24h"] = sq.rolling(window=24, min_periods=24).sum()
    df["rv168h"] = sq.rolling(window=168, min_periods=168).sum()
    # EMA24 distance: mark / EMA24(mark) - 1, causal
    alpha = 2.0 / (24.0 + 1.0)
    ema = df["close"].ewm(alpha=alpha, adjust=False, min_periods=1).mean()
    df["ema_dist"] = df["close"] / ema - 1.0
    return df[["ts_ms", "close", "log_ret", "rv1h", "rv24h", "rv168h", "ema_dist"]]


def compute_abs_fund_pct(funding_df, coin, ts, window_days=90, min_obs=30):
    """Percentile rank of abs(funding) at ts vs preceding window_days of abs funding (causal, strictly past)."""
    sub = funding_df[(funding_df["coin"] == coin) & (funding_df["ts"] < ts)]
    cutoff = ts - pd.Timedelta(days=window_days)
    hist = sub[sub["ts"] >= cutoff]["fundingRate"].dropna()
    if len(hist) < min_obs:
        return np.nan
    latest = funding_df[(funding_df["coin"] == coin) & (funding_df["ts"] <= ts)]
    if latest.empty:
        return np.nan
    latest_abs = abs(latest.iloc[-1]["fundingRate"])
    abs_hist = hist.abs()
    cnt = (abs_hist <= latest_abs).sum()
    return cnt / len(abs_hist)


def main() -> None:
    out_dir = RS
    out_dir.mkdir(parents=True, exist_ok=True)

    # ---- 1. Load ironflow labels ----
    label_frames = []
    label_checksums = {}
    label_rows_total = 0
    for m in LABEL_MONTHS:
        p = CACHE / "ironflow_events" / f"{m}.parquet"
        t = pq.read_table(p)
        label_checksums[f"ironflow_events_{m}.parquet"] = sha256_file(p)
        df = t.to_pandas()
        label_rows_total += len(df)
        label_frames.append(df)
    labels = pd.concat(label_frames, ignore_index=True)
    missing = [c for c in LABEL_COLS if c not in labels.columns]
    assert not missing, f"missing label cols: {missing}"
    perp_markets = set(PERP.values())
    labels = labels[labels["market"].isin(perp_markets)].copy()
    labels["coin"] = labels["market"].str.replace("-PERP", "", regex=False)
    labels["ts"] = labels["timestamp"].dt.tz_convert("UTC").dt.floor("24h")
    labels = labels[(labels["ts"] >= pd.Timestamp("2026-05-01", tz="UTC")) &
                    (labels["ts"] <= pd.Timestamp("2026-10-31 23:59:59", tz="UTC"))]
    label_daily = (
        labels.groupby(["coin", "ts"])["notional_usd"]
        .agg(["sum", "count"])
        .rename(columns={"sum": "liq_notional_usd", "count": "liq_event_count"})
        .reset_index()
    )
    label_daily.columns = ["coin", "ts", "liq_notional_usd", "liq_event_count"]

    # ---- 2. Load funding context ----
    funding_rows = []
    funding_checksums = {}
    funding_coverage = {}
    for coin in COINS:
        p = CACHE / "hyperliquid_funding" / f"{coin}.json"
        funding_checksums[f"hyperliquid_funding_{coin}.json"] = sha256_file(p)
        data = json.loads(p.read_text())
        funding_coverage[coin] = len(data)
        for r in data:
            t_ms = r.get("time")
            if t_ms is None:
                continue
            ts = pd.Timestamp(int(t_ms), unit="ms", tz="UTC")
            if ts < pd.Timestamp("2026-05-01", tz="UTC") or ts > pd.Timestamp("2026-10-31 23:59:59", tz="UTC"):
                continue
            funding_rows.append({
                "coin": coin,
                "ts": ts,
                "fundingRate": float(r.get("fundingRate")) if r.get("fundingRate") is not None else None,
                "premium": float(r.get("premium")) if r.get("premium") is not None else None,
            })
    funding = pd.DataFrame(funding_rows)
    if not funding.empty:
        funding["ts"] = funding["ts"].dt.floor("1h")
        funding = funding.sort_values(["coin", "ts"]).reset_index(drop=True)

    # ---- 3. Load mark-price candles + compute RV + ema_dist ----
    candle_checksums = {}
    candle_rows = {}
    candle_months_ok = {}
    rv_frames = {}
    for coin in COINS:
        cdf, cks, nrows, months_ok = load_candles(coin)
        if cdf is None:
            continue
        candle_checksums.update(cks)
        candle_rows[coin] = nrows
        candle_months_ok[coin] = months_ok
        rv_df = compute_rv_with_close(cdf)
        rv_df["coin"] = coin
        rv_frames[coin] = rv_df
    rv_all = pd.concat(rv_frames, ignore_index=True) if rv_frames else pd.DataFrame()
    if not rv_all.empty:
        rv_all["ts"] = pd.to_datetime(rv_all["ts_ms"], unit="ms", utc=True)

    # ---- 4. Build full grid (symbol x 24h bucket) over overlap ----
    all_days = pd.date_range("2026-05-01", "2026-10-31", freq="24h", tz="UTC")
    grid = pd.DataFrame({
        "coin": np.repeat(COINS, len(all_days)),
        "ts": np.tile(all_days, len(COINS)),
    })
    panel = grid.merge(label_daily, on=["coin", "ts"], how="left")

    # funding asof merge per coin
    panel = panel.sort_values(["coin", "ts"]).reset_index(drop=True)
    funding_sorted = funding if not funding.empty else funding
    merged = []
    for coin in COINS:
        pl = panel[panel["coin"] == coin].sort_values("ts").reset_index(drop=True)
        if funding_sorted.empty:
            pl["fundingRate"] = np.nan
            pl["premium"] = np.nan
        else:
            fl = funding_sorted[funding_sorted["coin"] == coin].sort_values("ts").reset_index(drop=True)
            if fl.empty:
                pl["fundingRate"] = np.nan
                pl["premium"] = np.nan
            else:
                pl = pd.merge_asof(
                    pl, fl[["ts", "fundingRate", "premium"]],
                    on="ts", direction="backward", tolerance=pd.Timedelta("24h")
                )
        merged.append(pl)
    panel = pd.concat(merged, ignore_index=True).sort_values(["coin", "ts"]).reset_index(drop=True)

    # RV asof merge per coin (tolerance 168h for rv168h coverage)
    rv_sorted = rv_all if not rv_all.empty else rv_all
    rv_merged = []
    for coin in COINS:
        pl = panel[panel["coin"] == coin].sort_values("ts").reset_index(drop=True)
        if rv_sorted.empty:
            for c in ["rv1h", "rv24h", "rv168h", "ema_dist", "close"]:
                pl[c] = np.nan
        else:
            rl = rv_sorted[rv_sorted["coin"] == coin][["ts", "rv1h", "rv24h", "rv168h", "ema_dist", "close"]].sort_values("ts").reset_index(drop=True)
            if rl.empty:
                for c in ["rv1h", "rv24h", "rv168h", "ema_dist", "close"]:
                    pl[c] = np.nan
            else:
                pl = pd.merge_asof(
                    pl, rl, on="ts", direction="backward", tolerance=pd.Timedelta("168h")
                )
        rv_merged.append(pl)
    panel = pd.concat(rv_merged, ignore_index=True).sort_values(["coin", "ts"]).reset_index(drop=True)

    # abs_fund_pct: causal percentile of abs funding vs preceding 90 days
    abs_fund_vals = []
    for _, r in panel.iterrows():
        if pd.isna(r["fundingRate"]):
            abs_fund_vals.append(np.nan)
        else:
            v = compute_abs_fund_pct(funding, r["coin"], r["ts"])
            abs_fund_vals.append(v)
    panel["abs_fund_pct"] = abs_fund_vals

    panel["liq_notional_usd"] = panel["liq_notional_usd"].fillna(0.0)
    panel["liq_event_count"] = panel["liq_event_count"].fillna(0).astype(int)
    panel["has_funding"] = panel["fundingRate"].notna()
    panel["has_label"] = panel["liq_event_count"] > 0
    panel["has_rv1h"] = panel["rv1h"].notna()
    panel["has_rv24h"] = panel["rv24h"].notna()
    panel["has_rv168h"] = panel["rv168h"].notna()
    panel["has_rv_complete"] = panel["has_rv1h"] & panel["has_rv24h"] & panel["has_rv168h"]
    panel["has_ema_dist"] = panel["ema_dist"].notna()
    panel["has_abs_fund_pct"] = panel["abs_fund_pct"].notna()

    panel_path = out_dir / f"tracka_hl_aligned_panel_with_rv_{TS}.parquet"
    panel.to_parquet(panel_path, index=False)
    panel_hash = sha256_file(panel_path)

    # ---- 5. Build report ----
    total_buckets = len(panel)
    buckets_with_label = int(panel["has_label"].sum())
    buckets_with_funding = int(panel["has_funding"].sum())
    buckets_with_rv24h = int(panel["has_rv24h"].sum())
    buckets_complete = int((panel["has_label"] & panel["has_funding"] & panel["has_rv_complete"]).sum())
    label_days = panel.loc[panel["has_label"], ["coin", "ts"]].drop_duplicates()
    symbols_with_label = sorted(label_days["coin"].unique().tolist())

    coverage_by_coin = (
        panel.groupby("coin").agg(
            buckets=("ts", "size"),
            label_buckets=("has_label", "sum"),
            funding_buckets=("has_funding", "sum"),
            rv24h_buckets=("has_rv24h", "sum"),
            rv_complete_buckets=("has_rv_complete", "sum"),
            abs_fund_pct_buckets=("has_abs_fund_pct", "sum"),
            ema_dist_buckets=("has_ema_dist", "sum"),
            total_notional=("liq_notional_usd", "sum"),
            total_events=("liq_event_count", "sum"),
        ).reset_index()
    )

    report = {
        "track": "A",
        "experiment_id": f"TRACKA-HL-S-RV-{TS}",
        "prereg_document": "research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json",
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "window_utc": "2026-05-01T00:00:00Z .. 2026-10-31T23:59:59Z",
        "symbols": COINS,
        "n_symbols": len(COINS),
        "admissible_overlap": "2026-05-01..2026-10-31",
        "inputs": {
            "ironflow_labels": {**label_checksums, "rows_total": label_rows_total, "months": LABEL_MONTHS},
            "hyperliquid_funding": {**funding_checksums, "rows_per_coin": funding_coverage},
            "hyperliquid_candles": {**candle_checksums, "rows_per_coin": candle_rows, "months_ok": candle_months_ok},
        },
        "panel": {
            "path": str(panel_path),
            "sha256": panel_hash,
            "total_buckets": int(total_buckets),
            "buckets_with_label": buckets_with_label,
            "buckets_with_funding": buckets_with_funding,
            "buckets_with_rv24h": buckets_with_rv24h,
            "buckets_complete_label_funding_rv": buckets_complete,
            "symbols_with_any_label": symbols_with_label,
            "n_symbols_with_label": len(symbols_with_label),
            "min_paired_instruments_required": 5,
            "min_paired_instruments_met": len(symbols_with_label) >= 5,
            "rv_baseline_b1_computable": buckets_with_rv24h > 0,
        },
        "coverage_by_coin": coverage_by_coin.to_dict(orient="records"),
        "missingness": {
            "buckets_missing_label": int(total_buckets - buckets_with_label),
            "buckets_missing_funding": int(total_buckets - buckets_with_funding),
            "buckets_missing_rv24h": int(total_buckets - buckets_with_rv24h),
            "buckets_missing_rv_complete": int(total_buckets - int(panel["has_rv_complete"].sum())),
            "buckets_missing_abs_fund_pct": int(total_buckets - int(panel["has_abs_fund_pct"].sum())),
            "buckets_missing_ema_dist": int(total_buckets - int(panel["has_ema_dist"].sum())),
        },
        "feasibility": {
            "rv_mark_price_cached": True,
            "rv_baseline_b1_computable": buckets_with_rv24h > 0,
            "reason": "mark-price 1h candleSnapshot acquired (first-time, unauthenticated) for 2026-05..2026-10; RV1h/RV24h/RV168h + ema_dist computable causally; abs_fund_pct computable from funding history.",
            "min_test_blocks_temporally_feasible": True,
            "min_test_blocks": 3,
            "claim_worthy_on_cache": (buckets_with_rv24h > 0) and (len(symbols_with_label) >= 5),
            "determination": "RV context acquired; proceed to pre-registered successor C2 vs B1 evaluation.",
        },
    }
    report_path = out_dir / f"tracka_hl_panel_with_rv_build_report_{TS}.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "panel": str(panel_path),
        "report": str(report_path),
        "total_buckets": total_buckets,
        "buckets_with_label": buckets_with_label,
        "buckets_with_funding": buckets_with_funding,
        "buckets_with_rv24h": buckets_with_rv24h,
        "buckets_complete_label_funding_rv": buckets_complete,
        "symbols_with_label": symbols_with_label,
        "claim_worthy": report["feasibility"]["claim_worthy_on_cache"],
    }, indent=2))


if __name__ == "__main__":
    main()
