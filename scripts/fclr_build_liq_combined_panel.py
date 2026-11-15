#!/usr/bin/env python3
"""FCLR-LIQ-COMBINED-PANEL step 3: COMBINED_PANEL_BUILD.

Loads the combined metpie (2025-03-22..2025-05-25) + ironflow (2025-05-25..2026-10-31)
Hyperliquid observed-liquidation event families, normalizes to one schema, dedups on
(coin, timestamp, notional_usd, tx-hash), and joins CAUSAL market-context features per
coin (all computed strictly past-only relative to each event):

  - funding_rate: signed 1h funding rate at the last funding timestamp <= event time
  - premium: funding premium at the last funding timestamp <= event time
  - abs_fund_pct: 90d past-only abs-funding percentile of the event-time funding rate
  - mark: 4h candle close at the last 4h bar end <= event time
  - ema_dist: (mark - EMA24(mark)) / EMA24(mark) using 4h closes <= event time
  - rv24h: realized vol of 4h log returns over the past 24h (6 bars) <= event time
  - rv168h: realized vol of 4h log returns over the past 168h (42 bars) <= event time

No look-ahead, no zero-fill of missing, no fabricated values. Emits:
  research_state/fclr_liq_combined_panel_<UTC>.parquet
  research_state/fclr_liq_combined_panel_build_report_<UTC>.json

Determinism: sorted iteration, fixed float math; no randomness.
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
METPIE = CACHE / "metpie_liq" / "liquidation_events.csv.gz"
IRONFLOW_DIR = CACHE / "ironflow_events"
FUNDING_DIR = CACHE / "hyperliquid_funding_early"
CANDLES_4H_EARLY = CACHE / "hyperliquid_candles_4h_early"
CANDLES_4H_MAIN = CACHE / "hyperliquid_candles_4h"

FUNDED = ["AAVE", "ADA", "AVAX", "BNB", "BTC", "CRV", "DOGE", "ETH",
          "LINK", "LTC", "NEAR", "SOL", "SUI", "UNI", "XRP"]

EMA_SPAN = 24
RV24_BARS = 6     # 6 x 4h = 24h
RV168_BARS = 42   # 42 x 4h = 168h
ABS_FUND_LOOKBACK_DAYS = 90


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_metpie() -> pd.DataFrame:
    df = pd.read_csv(METPIE)
    return pd.DataFrame({
        "timestamp": pd.to_datetime(df["time"], unit="ms", utc=True, errors="coerce"),
        "coin": df["coin"].astype(str),
        "notional_usd": pd.to_numeric(df["notional_usd"], errors="coerce"),
        "side": df["side"].astype(str),
        "source": "metpie",
        "tx_hash": df["hash"].astype(str),
    })


def load_ironflow() -> pd.DataFrame:
    frames = []
    for p in sorted(IRONFLOW_DIR.glob("*.parquet")):
        d = pd.read_parquet(p, columns=["timestamp", "market", "notional_usd",
                                        "position_side", "tx_hash"])
        frames.append(d)
    df = pd.concat(frames, ignore_index=True)
    coin = df["market"].astype(str).str.replace(r"-PERP$", "", regex=True)
    return pd.DataFrame({
        "timestamp": pd.to_datetime(df["timestamp"], utc=True, errors="coerce"),
        "coin": coin,
        "notional_usd": pd.to_numeric(df["notional_usd"], errors="coerce"),
        "side": df["position_side"].astype(str),
        "source": "ironflow",
        "tx_hash": df["tx_hash"].astype(str),
    })


def load_funding(coin: str) -> pd.DataFrame | None:
    """Funding history for one coin from the early store (2025-03..2025-10)."""
    p = FUNDING_DIR / f"{coin}.json"
    if not p.exists():
        return None
    d = json.loads(p.read_text())
    if not isinstance(d, list) or not d:
        return None
    df = pd.DataFrame(d)
    df["time"] = pd.to_datetime(df["time"], unit="ms", utc=True, errors="coerce")
    for c in ("fundingRate", "premium"):
        df[c] = pd.to_numeric(df.get(c), errors="coerce")
    return df.dropna(subset=["time"]).sort_values("time").reset_index(drop=True)


def load_candles_4h(coin: str) -> pd.DataFrame | None:
    """4h candles for one coin, early (2025-03..10) + main (2025-11..2026-10)."""
    frames = []
    for store in (CANDLES_4H_EARLY, CANDLES_4H_MAIN):
        cdir = store / coin
        if not cdir.exists():
            continue
        for p in sorted(cdir.glob("2025-*.json")) + sorted(cdir.glob("2026-*.json")):
            if "accessed" in p.name or "sha256" in p.name:
                continue
            try:
                d = json.loads(p.read_text())
            except Exception:
                continue
            if isinstance(d, list) and d:
                frames.append(pd.DataFrame(d))
    if not frames:
        return None
    df = pd.concat(frames, ignore_index=True)
    df["t"] = pd.to_datetime(df["t"], unit="ms", utc=True, errors="coerce")
    df["T"] = pd.to_datetime(df["T"], unit="ms", utc=True, errors="coerce")
    for c in ("o", "h", "l", "c"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["t", "c"]).drop_duplicates(subset=["t"]).sort_values("t")
    return df.reset_index(drop=True)


def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()


def build_coin_features(coin: str, events: pd.DataFrame) -> pd.DataFrame:
    """Join causal features to a coin's events (past-only, no look-ahead)."""
    ev = events.sort_values("timestamp").reset_index(drop=True)
    out = ev.copy()

    # --- funding features (as-of merge on event time <= funding time) ---
    fund = load_funding(coin)
    if fund is not None and not fund.empty:
        m = pd.merge_asof(
            out[["timestamp"]].sort_values("timestamp"),
            fund[["time", "fundingRate", "premium"]].sort_values("time"),
            left_on="timestamp", right_on="time", direction="backward",
        )
        out = out.merge(m[["time", "fundingRate", "premium"]], left_index=True,
                        right_index=True, how="left")
        out = out.drop(columns=["time"], errors="ignore")
    # 90d past-only abs-funding percentile (vectorized as-of)
    if fund is not None and not fund.empty:
        f_sorted = fund.sort_values("time").reset_index(drop=True)
        abs_rate = f_sorted["fundingRate"].abs()
        f_times = f_sorted["time"].values.astype("datetime64[ns]")
        abs_vals = abs_rate.values.astype("float64")
        win = np.timedelta64(ABS_FUND_LOOKBACK_DAYS, "D")
        ev_ns = out["timestamp"].values.astype("datetime64[ns]")
        # as-of index: last funding time <= event time
        pos = np.searchsorted(f_times, ev_ns, side="right") - 1
        pct = np.full(len(out), np.nan)
        for i, p in enumerate(pos):
            if p < 0:
                continue
            lo = np.searchsorted(f_times, f_times[p] - win, side="left")
            hist = abs_vals[lo:p + 1]
            if len(hist) == 0:
                continue
            pct[i] = float((hist <= abs_vals[p]).mean())
        out["abs_fund_pct"] = pct
    else:
        out["fundingRate"] = np.nan
        out["premium"] = np.nan
        out["abs_fund_pct"] = np.nan

    # --- candle features (as-of merge on event time <= 4h bar end T) ---
    candles = load_candles_4h(coin)
    if candles is not None and not candles.empty:
        candles = candles.copy()
        candles["ema24"] = ema(candles["c"], EMA_SPAN)
        ret = np.log(candles["c"]).diff()
        candles["ret"] = ret
        candles["rv24"] = candles["ret"].rolling(RV24_BARS).std() * math.sqrt(RV24_BARS)
        candles["rv168"] = candles["ret"].rolling(RV168_BARS).std() * math.sqrt(RV168_BARS)
        candles["ema_dist"] = (candles["c"] - candles["ema24"]) / candles["ema24"]
        m = pd.merge_asof(
            out[["timestamp"]].sort_values("timestamp"),
            candles[["T", "c", "ema_dist", "rv24", "rv168"]].rename(
                columns={"T": "bar_T", "c": "mark", "ema_dist": "ema_dist",
                         "rv24": "rv24h", "rv168": "rv168h"}).sort_values("bar_T"),
            left_on="timestamp", right_on="bar_T", direction="backward",
        )
        out = out.merge(m[["bar_T", "mark", "ema_dist", "rv24h", "rv168h"]],
                        left_index=True, right_index=True, how="left")
        out = out.drop(columns=["bar_T"], errors="ignore")
    else:
        out["mark"] = np.nan
        out["ema_dist"] = np.nan
        out["rv24h"] = np.nan
        out["rv168h"] = np.nan

    return out


def main() -> int:
    ts_utc = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    print("Loading metpie...", flush=True)
    met = load_metpie()
    print(f"  metpie rows: {len(met)}", flush=True)
    print("Loading ironflow...", flush=True)
    irn = load_ironflow()
    print(f"  ironflow rows: {len(irn)}", flush=True)

    combined = pd.concat([met, irn], ignore_index=True)
    combined = combined.dropna(subset=["timestamp"]).reset_index(drop=True)

    # restrict to the 15 funded coins (the estimand universe)
    combined = combined[combined["coin"].isin(FUNDED)].reset_index(drop=True)
    n_before = len(combined)

    # dedup on (coin, timestamp, notional_usd, tx_hash)
    combined = combined.drop_duplicates(subset=["coin", "timestamp", "notional_usd", "tx_hash"])
    n_after_dedup = len(combined)

    # build features per coin
    frames = []
    for coin in FUNDED:
        sub = combined[combined["coin"] == coin].reset_index(drop=True)
        if sub.empty:
            continue
        feats = build_coin_features(coin, sub)
        frames.append(feats)
        print(f"  {coin}: {len(sub)} events -> features built", flush=True)

    panel = pd.concat(frames, ignore_index=True).sort_values(["coin", "timestamp"]).reset_index(drop=True)

    # coverage diagnostics
    per_coin = {}
    for coin in FUNDED:
        sub = panel[panel["coin"] == coin]
        per_coin[coin] = {
            "n_events": int(len(sub)),
            "n_with_funding": int(sub["fundingRate"].notna().sum()),
            "n_with_mark": int(sub["mark"].notna().sum()),
            "n_with_rv24h": int(sub["rv24h"].notna().sum()),
            "n_with_rv168h": int(sub["rv168h"].notna().sum()),
            "first_ts": sub["timestamp"].min().isoformat() if len(sub) else None,
            "last_ts": sub["timestamp"].max().isoformat() if len(sub) else None,
        }

    panel_path = RS / f"fclr_liq_combined_panel_{ts_utc}.parquet"
    panel.to_parquet(panel_path, index=False)
    panel_hash = sha256_file(panel_path)

    report = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "experiment_id": "FCLR-LIQ-COMBINED-PANEL-20261115T170000Z",
        "phase": "COMBINED_PANEL_BUILD",
        "panel_path": str(panel_path.relative_to(REPO)),
        "panel_sha256": panel_hash,
        "funded_coins": FUNDED,
        "n_events_before_filters": int(n_before),
        "n_events_after_dedup": int(n_after_dedup),
        "n_rows_panel": int(len(panel)),
        "dedup_keys": ["coin", "timestamp", "notional_usd", "tx_hash"],
        "causal_features": ["fundingRate", "premium", "abs_fund_pct",
                            "mark", "ema_dist", "rv24h", "rv168h"],
        "per_coin": per_coin,
        "notes": "Past-only as-of joins (direction=backward); no zero-fill; no look-ahead. 4h candleSnapshot is the RV source (1h is live-only for old ranges).",
    }
    report_path = RS / f"fclr_liq_combined_panel_build_report_{ts_utc}.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"panel": str(panel_path.relative_to(REPO)),
                      "rows": len(panel), "sha256": panel_hash[:16],
                      "report": str(report_path.relative_to(REPO))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())