#!/usr/bin/env python3
"""Build Track A early 4h panel from cached admissible inputs only (no network).

Inputs (cached, provenance recorded in prereg):
- research_state/data_cache/hyperliquid_candles_4h/<COIN>/<YYYY-MM>.json (4h candles, 2025-11..2026-04)
- research_state/data_cache/hyperliquid_funding/<COIN>.json (funding context, ~2025-11..2026-10)
- research_state/data_cache/ironflow_events/<YYYY-MM>.parquet (observed labels, 2025-11..2026-04)

Outputs:
- research_state/tracka_hl_early_4h_panel_<UTC>.parquet (symbol x 24h bucket: label intensity + RV + funding)
- research_state/tracka_hl_early_4h_panel_build_report_<UTC>.json (row counts, coverage, missingness/gap, input hashes)

No outcome computation. Fail-closed on schema.
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
TS = "20261112T054737Z"
UTC = timezone.utc

SYMBOLS = ["BTC", "ETH", "BNB", "SOL", "XRP", "AVAX", "DOGE", "LINK", "SUI"]
PERP = {s: f"{s}-PERP" for s in SYMBOLS}
COINS = SYMBOLS

LABEL_COLS = ["timestamp", "market", "issuer", "wallet", "position_side", "size", "notional_usd", "avg_price", "fills", "block", "tx_hash"]

PREREG_PATH = RS / "tracka_prereg_hyperliquid_early_4h_20261112T054737Z.json"
PREG = json.loads(PREREG_PATH.read_text())
SPLITS = PREG["splits"]
TRAIN = (pd.Timestamp(SPLITS["train"]["start"], tz="UTC"), pd.Timestamp(SPLITS["train"]["end"], tz="UTC"))
VAL = (pd.Timestamp(SPLITS["validation"]["start"], tz="UTC"), pd.Timestamp(SPLITS["validation"]["end"], tz="UTC"))
TEST_BLOCKS = [(pd.Timestamp(b["start"], tz="UTC"), pd.Timestamp(b["end"], tz="UTC")) for b in SPLITS["test_blocks"]]

EPS = 1e-12


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_rv_from_4h_closes(closes: pd.Series, periods: int) -> pd.Series:
    """Compute realized volatility from 4h log returns over given periods."""
    if len(closes) < periods + 1:
        return pd.Series([np.nan] * len(closes), index=closes.index)
    log_returns = np.log(closes / closes.shift(1))
    rv = log_returns.rolling(periods).apply(lambda x: np.sum(x**2) if len(x) == periods else np.nan, raw=True)
    return rv


def main() -> None:
    out_dir = RS
    out_dir.mkdir(parents=True, exist_ok=True)

    # ---- 1. Load ironflow labels (2025-11..2026-04) ----
    label_months = ["2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04"]
    frames = []
    label_checksums = {}
    label_rows_total = 0
    for m in label_months:
        p = CACHE / "ironflow_events" / f"{m}.parquet"
        t = pq.read_table(p)
        label_checksums[f"ironflow_events_{m}.parquet"] = sha256_file(p)
        df = t.to_pandas()
        label_rows_total += len(df)
        frames.append(df)
    labels = pd.concat(frames, ignore_index=True)
    missing = [c for c in LABEL_COLS if c not in labels.columns]
    assert not missing, f"missing label cols: {missing}"
    perp_markets = set(PERP.values())
    labels = labels[labels["market"].isin(perp_markets)].copy()
    labels["coin"] = labels["market"].str.replace("-PERP", "", regex=False)
    labels["ts"] = labels["timestamp"].dt.tz_convert("UTC").dt.floor("24h")
    labels = labels[labels["ts"] >= pd.Timestamp("2025-11-01", tz="UTC")]
    labels = labels[labels["ts"] <= pd.Timestamp("2026-04-30 23:59:59", tz="UTC")]

    # label intensity: notional_usd-weighted event count per symbol per 24h UTC bucket
    label_daily = (
        labels.groupby(["coin", "ts"])["notional_usd"]
        .agg(["sum", "count"])
        .rename(columns={"sum": "liq_notional_usd", "count": "liq_event_count"})
        .reset_index()
    )
    label_daily.columns = ["coin", "ts", "liq_notional_usd", "liq_event_count"]

    # ---- 2. Load 4h candles and compute RV features ----
    candle_checksums = {}
    rv_frames = []
    for coin in COINS:
        coin_dir = CACHE / "hyperliquid_candles_4h" / coin
        if not coin_dir.exists():
            print(f"WARNING: No candle dir for {coin}")
            continue
        month_files = sorted(coin_dir.glob("2025-11.json"), key=lambda x: x.name) + \
                      sorted(coin_dir.glob("2025-12.json"), key=lambda x: x.name) + \
                      sorted(coin_dir.glob("2026-01.json"), key=lambda x: x.name) + \
                      sorted(coin_dir.glob("2026-02.json"), key=lambda x: x.name) + \
                      sorted(coin_dir.glob("2026-03.json"), key=lambda x: x.name) + \
                      sorted(coin_dir.glob("2026-04.json"), key=lambda x: x.name)

        all_candles = []
        for f in month_files:
            if not f.exists():
                continue
            candle_checksums[f"hyperliquid_candles_4h_{coin}_{f.stem}.json"] = sha256_file(f)
            data = json.loads(f.read_text())
            for c in data:
                all_candles.append({
                    "coin": coin,
                    "ts": pd.Timestamp(int(c["t"]), unit="ms", tz="UTC"),
                    "close": float(c["c"]),
                })
        if not all_candles:
            print(f"WARNING: No candles for {coin}")
            continue
        candles_df = pd.DataFrame(all_candles).sort_values("ts").reset_index(drop=True)
        candles_df = candles_df.drop_duplicates(subset=["coin", "ts"], keep="last")

        # Compute RV features from 4h closes
        closes = candles_df.set_index("ts")["close"]
        rv_4h = compute_rv_from_4h_closes(closes, 1).rename("rv_4h")
        rv_24h = compute_rv_from_4h_closes(closes, 6).rename("rv_24h")
        rv_168h = compute_rv_from_4h_closes(closes, 42).rename("rv_168h")

        rv_df = pd.concat([rv_4h, rv_24h, rv_168h], axis=1).reset_index()
        rv_df["coin"] = coin
        rv_frames.append(rv_df)

    rv_all = pd.concat(rv_frames, ignore_index=True) if rv_frames else pd.DataFrame(columns=["ts", "rv_4h", "rv_24h", "rv_168h", "coin"])

    # ---- 3. Load funding context ----
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
            if ts < pd.Timestamp("2025-11-01", tz="UTC") or ts > pd.Timestamp("2026-04-30 23:59:59", tz="UTC"):
                continue
            funding_rows.append({
                "coin": coin,
                "ts": ts,
                "fundingRate": float(r.get("fundingRate")) if r.get("fundingRate") is not None else None,
                "premium": float(r.get("premium")) if r.get("premium") is not None else None,
            })
    funding = pd.DataFrame(funding_rows)
    funding["ts"] = funding["ts"].dt.floor("1h")

    # ---- 4. Build full grid (symbol x 24h bucket) over window ----
    all_days = pd.date_range("2025-11-01", "2026-04-30", freq="24h", tz="UTC")
    grid = pd.DataFrame({
        "coin": np.repeat(COINS, len(all_days)),
        "ts": np.tile(all_days, len(COINS)),
    })

    # Merge labels
    panel = grid.merge(label_daily, on=["coin", "ts"], how="left")

    # Merge RV features (need to align 4h RV to 24h bucket - use latest 4h RV at or before bucket start)
    rv_all = rv_all.sort_values(["coin", "ts"]).reset_index(drop=True)
    merged = []
    for coin in COINS:
        pl = panel[panel["coin"] == coin].sort_values("ts").reset_index(drop=True)
        rl = rv_all[rv_all["coin"] == coin].sort_values("ts").reset_index(drop=True)
        if rl.empty:
            pl["rv_4h"] = np.nan
            pl["rv_24h"] = np.nan
            pl["rv_168h"] = np.nan
        else:
            pl = pd.merge_asof(
                pl, rl[["ts", "rv_4h", "rv_24h", "rv_168h"]],
                on="ts", direction="backward", tolerance=pd.Timedelta("24h")
            )
        merged.append(pl)
    panel = pd.concat(merged, ignore_index=True).sort_values(["coin", "ts"]).reset_index(drop=True)

    # Merge funding (asof merge per coin, latest funding at or before each daily bucket, tolerance 24h)
    funding_sorted = funding.sort_values(["coin", "ts"]).reset_index(drop=True)
    merged = []
    for coin in COINS:
        pl = panel[panel["coin"] == coin].sort_values("ts").reset_index(drop=True)
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

    # Fill missing labels with 0
    panel["liq_notional_usd"] = panel["liq_notional_usd"].fillna(0.0)
    panel["liq_event_count"] = panel["liq_event_count"].fillna(0).astype(int)
    panel["has_funding"] = panel["fundingRate"].notna()
    panel["has_label"] = panel["liq_event_count"] > 0
    panel["has_rv_24h"] = panel["rv_24h"].notna() & (panel["rv_24h"] > 0)
    panel["has_rv_168h"] = panel["rv_168h"].notna() & (panel["rv_168h"] > 0)
    panel["has_rv_complete"] = panel["has_rv_24h"] & panel["has_rv_168h"]

    # Compute funding percentile (90-day trailing, min 30 obs)
    panel = panel.sort_values(["coin", "ts"]).reset_index(drop=True)
    abs_fund_pct = []
    for coin in COINS:
        coin_mask = panel["coin"] == coin
        coin_data = panel.loc[coin_mask, "fundingRate"].abs()
        # Rolling 90-day window (90 * 24 = 2160 hours, but funding is hourly)
        # Use 90 calendar days = 90*24 = 2160 periods at hourly, but our grid is daily
        # Approximate: 90 days of daily buckets
        rolling = coin_data.rolling(window=90, min_periods=30)
        pct = rolling.rank(pct=True)
        abs_fund_pct.extend(pct.values)
    panel["abs_fund_pct"] = abs_fund_pct

    # Compute EMA24 distance (mark/EMA24 - 1) - use close as proxy for mark
    # Since we don't have mark price, use close from candles
    # Re-load closes for EMA
    ema_dist = []
    for coin in COINS:
        coin_dir = CACHE / "hyperliquid_candles_4h" / coin
        all_candles = []
        for m in ["2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04"]:
            f = coin_dir / f"{m}.json"
            if f.exists():
                data = json.loads(f.read_text())
                for c in data:
                    all_candles.append({
                        "ts": pd.Timestamp(int(c["t"]), unit="ms", tz="UTC"),
                        "close": float(c["c"]),
                    })
        if all_candles:
            candles_df = pd.DataFrame(all_candles).sort_values("ts").reset_index(drop=True)
            candles_df = candles_df.drop_duplicates(subset=["ts"], keep="last")
            # Resample to daily frequency (take last 4h close of each day)
            daily_closes = candles_df.set_index("ts")["close"].resample("24h").last()
            ema24 = daily_closes.ewm(span=24, adjust=False).mean()  # 24 periods = ~96h at 4h, but we use daily
            # Align to panel daily grid
            coin_panel = panel[panel["coin"] == coin].set_index("ts")["rv_24h"]  # dummy to get index
            aligned_ema = ema24.reindex(coin_panel.index, method="ffill")
            ema_dist.extend((daily_closes.reindex(coin_panel.index, method="ffill") / aligned_ema - 1).values)
        else:
            ema_dist.extend([np.nan] * len(panel[panel["coin"] == coin]))
    panel["ema_dist"] = ema_dist

    # ---- 5. Assign splits ----
    def split_of(ts: pd.Timestamp):
        if TRAIN[0] <= ts <= TRAIN[1]:
            return "train"
        if VAL[0] <= ts <= VAL[1]:
            return "val"
        for i, tb in enumerate(TEST_BLOCKS):
            if tb[0] <= ts <= tb[1]:
                return f"test_block_{i}"
        return None

    panel["split"] = panel["ts"].apply(split_of)
    panel["test_block"] = panel["split"].apply(lambda x: int(x.split("_")[-1]) if isinstance(x, str) and x.startswith("test_block") else -1)

    # ---- 6. Save panel ----
    panel_path = out_dir / f"tracka_hl_early_4h_panel_{TS}.parquet"
    panel.to_parquet(panel_path, index=False)
    panel_hash = sha256_file(panel_path)

    # ---- 7. Build report ----
    total_buckets = len(panel)
    buckets_with_label = int(panel["has_label"].sum())
    buckets_with_funding = int(panel["has_funding"].sum())
    buckets_with_rv24h = int(panel["has_rv_24h"].sum())
    buckets_with_rv168h = int(panel["has_rv_168h"].sum())
    buckets_complete = int((panel["has_label"] & panel["has_funding"] & panel["has_rv_complete"]).sum())
    label_days = panel.loc[panel["has_label"], ["coin", "ts"]].drop_duplicates()
    symbols_with_label = sorted(label_days["coin"].unique().tolist())

    coverage_by_coin = (
        panel.groupby("coin").agg(
            buckets=("ts", "size"),
            label_buckets=("has_label", "sum"),
            funding_buckets=("has_funding", "sum"),
            rv24h_buckets=("has_rv_24h", "sum"),
            rv168h_buckets=("has_rv_168h", "sum"),
            total_notional=("liq_notional_usd", "sum"),
            total_events=("liq_event_count", "sum"),
        ).reset_index()
    )

    # Count test blocks with data
    test_blocks_with_data = []
    for i, tb in enumerate(TEST_BLOCKS):
        tb_data = panel[(panel["test_block"] == i) & panel["has_label"] & panel["has_funding"] & panel["has_rv_complete"]]
        if len(tb_data) > 0:
            test_blocks_with_data.append(i)

    paired_syms_test = sorted(panel[(panel["split"].str.startswith("test", na=False)) & panel["has_label"] & panel["has_funding"] & panel["has_rv_complete"]]["coin"].unique().tolist())

    report = {
        "track": "A",
        "experiment_id": "TRACKA-HL-EARLY-4H-20261112T054737Z",
        "prereg_document": "research_state/tracka_prereg_hyperliquid_early_4h_20261112T054737Z.json",
        "generated_utc": "2026-11-12T05:47:37Z",
        "window_utc": "2025-11-01T00:00:00Z .. 2026-04-30T23:59:59Z",
        "symbols": COINS,
        "n_symbols": len(COINS),
        "inputs": {
            "ironflow_labels": {**label_checksums, "rows_total": label_rows_total, "months": label_months},
            "hyperliquid_candles_4h": {**candle_checksums, "coverage_utc": "2025-11-01..2026-04-30 (4h)"},
            "hyperliquid_funding": {**funding_checksums, "rows_per_coin": funding_coverage, "coverage_utc": "2025-11-01..2026-10-30 (hourly)"},
        },
        "panel": {
            "path": str(panel_path),
            "sha256": panel_hash,
            "total_buckets": int(total_buckets),
            "buckets_with_label": buckets_with_label,
            "buckets_with_funding": buckets_with_funding,
            "buckets_with_rv24h": buckets_with_rv24h,
            "buckets_with_rv168h": buckets_with_rv168h,
            "buckets_complete_label_funding_rv": buckets_complete,
            "symbols_with_any_label": symbols_with_label,
            "n_symbols_with_label": len(symbols_with_label),
            "min_paired_instruments_required": 5,
            "min_paired_instruments_met": len(paired_syms_test) >= 5,
            "paired_instruments_in_test": paired_syms_test,
            "min_test_blocks_required": 3,
            "test_blocks_with_data": test_blocks_with_data,
            "n_test_blocks_with_data": len(test_blocks_with_data),
        },
        "coverage_by_coin": coverage_by_coin.to_dict(orient="records"),
        "missingness": {
            "buckets_missing_label": int(total_buckets - buckets_with_label),
            "buckets_missing_funding": int(total_buckets - buckets_with_funding),
            "buckets_missing_rv24h": int(total_buckets - buckets_with_rv24h),
            "buckets_missing_rv168h": int(total_buckets - buckets_with_rv168h),
        },
        "feasibility": {
            "rv_baseline_b1_computable": buckets_with_rv24h > 100 and buckets_with_rv168h > 100,
            "funding_percentile_computable": panel["abs_fund_pct"].notna().sum() > 100,
            "min_test_blocks_temporally_feasible": len(test_blocks_with_data) >= 3,
            "min_paired_instruments_feasible": len(paired_syms_test) >= 5,
            "determination": "Proceed to evaluation" if (len(paired_syms_test) >= 5 and len(test_blocks_with_data) >= 2) else "PILOT/INCONCLUSIVE - insufficient test blocks",
        },
    }
    report_path = out_dir / f"tracka_hl_early_4h_panel_build_report_{TS}.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "panel": str(panel_path),
        "report": str(report_path),
        "total_buckets": total_buckets,
        "buckets_with_label": buckets_with_label,
        "buckets_with_funding": buckets_with_funding,
        "buckets_with_rv24h": buckets_with_rv24h,
        "buckets_with_rv168h": buckets_with_rv168h,
        "buckets_complete": buckets_complete,
        "symbols_with_label": symbols_with_label,
        "paired_instruments_in_test": paired_syms_test,
        "test_blocks_with_data": test_blocks_with_data,
        "feasible": report["feasibility"]["determination"],
    }, indent=2))


if __name__ == "__main__":
    main()