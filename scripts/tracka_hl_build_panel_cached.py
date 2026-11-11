#!/usr/bin/env python3
"""Build Track A aligned panel from cached admissible inputs only (no network).

Inputs (cached, provenance recorded in successor prereg):
- research_state/data_cache/ironflow_events/2026-0[5-9].parquet, 2026-10.parquet (observed labels)
- research_state/data_cache/hyperliquid_funding/{9 coins}.json (funding context, 2026-05..2026-10)

Outputs:
- research_state/tracka_hl_aligned_panel_<UTC>.parquet  (symbol x 24h bucket: label intensity + funding)
- research_state/tracka_hl_panel_build_report_<UTC>.json (row counts, coverage, missingness/gap, input hashes)

No outcome computation. No mark-price/RV (not cached). Fail-closed on schema.
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
TS = "20261111T133430Z"
UTC = timezone.utc

SYMBOLS = ["BTC","ETH","BNB","SOL","XRP","AVAX","DOGE","LINK","SUI"]
PERP = {s: f"{s}-PERP" for s in SYMBOLS}
COINS = SYMBOLS

LABEL_COLS = ["timestamp","market","issuer","wallet","position_side","size","notional_usd","avg_price","fills","block","tx_hash"]

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> None:
    out_dir = RS
    out_dir.mkdir(parents=True, exist_ok=True)

    # ---- 1. Load ironflow labels (overlap months 2026-05..2026-10) ----
    label_months = ["2026-05","2026-06","2026-07","2026-08","2026-09","2026-10"]
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
    # validate schema
    missing = [c for c in LABEL_COLS if c not in labels.columns]
    assert not missing, f"missing label cols: {missing}"
    # filter to 9 *-PERP markets
    perp_markets = set(PERP.values())
    labels = labels[labels["market"].isin(perp_markets)].copy()
    labels["coin"] = labels["market"].str.replace("-PERP","",regex=False)
    labels["ts"] = labels["timestamp"].dt.tz_convert("UTC").dt.floor("24h")
    labels = labels[labels["ts"] >= pd.Timestamp("2026-05-01", tz="UTC")]
    labels = labels[labels["ts"] <= pd.Timestamp("2026-10-31 23:59:59", tz="UTC")]

    # label intensity: notional_usd-weighted event count per symbol per 24h UTC bucket
    # "notional_usd-weighted event count" = sum of notional_usd per symbol per day (intensity proxy)
    label_daily = (
        labels.groupby(["coin","ts"])["notional_usd"]
        .agg(["sum","count"])
        .rename(columns={"sum":"liq_notional_usd","count":"liq_event_count"})
        .reset_index()
    )
    label_daily.columns = ["coin","ts","liq_notional_usd","liq_event_count"]

    # ---- 2. Load funding context (cached, 2026-05..2026-10) ----
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
    funding["ts"] = funding["ts"].dt.floor("1h")

    # ---- 3. Build full grid (symbol x 24h bucket) over overlap ----
    all_days = pd.date_range("2026-05-01", "2026-10-31", freq="24h", tz="UTC")
    grid = pd.DataFrame({
        "coin": np.repeat(COINS, len(all_days)),
        "ts": np.tile(all_days, len(COINS)),
    })
    panel = grid.merge(label_daily, on=["coin","ts"], how="left")
    # funding: map hourly funding to the 24h bucket of the forecast origin (use latest funding <= bucket start)
    panel = panel.sort_values(["coin","ts"]).reset_index(drop=True)
    funding_sorted = funding.sort_values(["coin","ts"]).reset_index(drop=True)
    # asof merge per coin (latest funding at or before each daily bucket, tolerance 24h)
    merged = []
    for coin in COINS:
        pl = panel[panel["coin"] == coin].sort_values("ts").reset_index(drop=True)
        fl = funding_sorted[funding_sorted["coin"] == coin].sort_values("ts").reset_index(drop=True)
        if fl.empty:
            pl["fundingRate"] = np.nan
            pl["premium"] = np.nan
        else:
            pl = pd.merge_asof(
                pl, fl[["ts","fundingRate","premium"]],
                on="ts", direction="backward", tolerance=pd.Timedelta("24h")
            )
        merged.append(pl)
    panel = pd.concat(merged, ignore_index=True).sort_values(["coin","ts"]).reset_index(drop=True)
    panel["liq_notional_usd"] = panel["liq_notional_usd"].fillna(0.0)
    panel["liq_event_count"] = panel["liq_event_count"].fillna(0).astype(int)
    panel["has_funding"] = panel["fundingRate"].notna()
    panel["has_label"] = panel["liq_event_count"] > 0

    panel_path = out_dir / f"tracka_hl_aligned_panel_{TS}.parquet"
    panel.to_parquet(panel_path, index=False)
    panel_hash = sha256_file(panel_path)

    # ---- 4. Build report ----
    total_buckets = len(panel)
    buckets_with_label = int(panel["has_label"].sum())
    buckets_with_funding = int(panel["has_funding"].sum())
    buckets_complete = int((panel["has_label"] & panel["has_funding"]).sum())
    label_days = panel.loc[panel["has_label"], ["coin","ts"]].drop_duplicates()
    symbols_with_label = sorted(label_days["coin"].unique().tolist())

    coverage_by_coin = (
        panel.groupby("coin").agg(
            buckets=("ts","size"),
            label_buckets=("has_label","sum"),
            funding_buckets=("has_funding","sum"),
            total_notional=("liq_notional_usd","sum"),
            total_events=("liq_event_count","sum"),
        ).reset_index()
    )

    report = {
        "track": "A",
        "experiment_id": "TRACKA-HL-S-20261111T133430Z",
        "prereg_document": "research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json",
        "generated_utc": "2026-11-11T13:34:30Z",
        "window_utc": "2026-05-01T00:00:00Z .. 2026-10-31T23:59:59Z",
        "symbols": COINS,
        "n_symbols": len(COINS),
        "admissible_overlap": "2026-05-01..2026-10-31",
        "inputs": {
            "ironflow_labels": {**label_checksums, "rows_total": label_rows_total, "months": label_months},
            "hyperliquid_funding": {**funding_checksums, "rows_per_coin": funding_coverage, "coverage_utc": "2026-05-01..2026-10-30 (hourly)"},
        },
        "panel": {
            "path": str(panel_path),
            "sha256": panel_hash,
            "total_buckets": int(total_buckets),
            "buckets_with_label": buckets_with_label,
            "buckets_with_funding": buckets_with_funding,
            "buckets_complete_label_and_funding": buckets_complete,
            "symbols_with_any_label": symbols_with_label,
            "n_symbols_with_label": len(symbols_with_label),
            "min_paired_instruments_required": 5,
            "min_paired_instruments_met": len(symbols_with_label) >= 5,
        },
        "coverage_by_coin": coverage_by_coin.to_dict(orient="records"),
        "missingness": {
            "buckets_missing_label": int(total_buckets - buckets_with_label),
            "buckets_missing_funding": int(total_buckets - buckets_with_funding),
        },
        "feasibility": {
            "rv_mark_price_cached": False,
            "rv_baseline_b1_computable": False,
            "reason": "mark-price / 1h candle / RV context NOT present in cached admissible inputs; handoff prohibits redundant network polling. Pre-registered C2 vs B1 primary contrast infeasible.",
            "min_test_blocks_temporally_feasible": True,
            "min_test_blocks": 3,
            "claim_worthy_on_cache": False,
            "determination": "Path (c) terminal closure (NOT_SUPPORTED / context insufficient) — see evaluation_summary_TRACKA-HL-terminal-20261111T133430Z.md",
        },
    }
    report_path = out_dir / f"tracka_hl_panel_build_report_{TS}.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "panel": str(panel_path),
        "report": str(report_path),
        "total_buckets": total_buckets,
        "buckets_with_label": buckets_with_label,
        "buckets_with_funding": buckets_with_funding,
        "symbols_with_label": symbols_with_label,
        "claim_worthy_on_cache": False,
    }, indent=2))

if __name__ == "__main__":
    main()
