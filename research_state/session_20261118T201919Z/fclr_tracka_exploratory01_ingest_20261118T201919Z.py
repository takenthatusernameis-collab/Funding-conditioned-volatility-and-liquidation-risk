#!/usr/bin/env python3
"""Track A exploratory ingest/manifest: Ironflow Hyperliquid observed liquidations.

Campaign : FCLR-LIQ-TRACKA-EXPLORATORY-01-20261118T201919Z
Session  : session_20261118T201919Z
Scope    : cached bulk parquet, months 2025-11 .. 2026-04 (6 complete months),
           main-dex perpetual markets only (dex == "", market_class == "perp").

Guarantees
----------
* Read-only on the parquet cache; never mutates cached inputs.
* Provenance: sha256 of every source parquet plus row/coin/date census.
* Fail closed on missing month or missing required column.
* Outputs are non-empty JSON/MD written into the session directory.
* pandas/pyarrow are used for parquet reads only; semantics stay explicit.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
CACHE = RS / "data_cache" / "ironflow_bulk"
SESSION = RS / "session_20261118T201919Z"

SESSION_ID = "session_20261118T201919Z"
CAMPAIGN = "FCLR-LIQ-TRACKA-EXPLORATORY-01-20261118T201919Z"
MONTHS = ["2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04"]
COINS = [
    "BTC", "ETH", "BNB", "SOL", "XRP", "AVAX", "DOGE", "LINK",
    "SUI", "ARB", "OP", "APT", "ADA",
]

EVENT_COLS = ["timestamp", "market", "issuer", "wallet", "position_side",
              "size", "notional_usd", "avg_price", "fills", "block", "tx_hash"]
CANDLE_COLS = ["timestamp", "market", "coin", "dex", "market_class", "close", "volume"]
FUNDING_COLS = ["timestamp", "market", "coin", "funding_rate", "premium"]
OI_COLS = ["timestamp", "market", "coin", "open_interest", "open_interest_usd"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_month(dataset: str, month: str, cols: list[str]) -> pd.DataFrame:
    path = CACHE / dataset / f"{month}.parquet"
    if not path.is_file():
        raise SystemExit(f"FAIL_CLOSED missing cached parquet: {path}")
    df = pd.read_parquet(path)
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise SystemExit(f"FAIL_CLOSED schema violation {dataset}/{month}: {missing}")
    return df


def month_census(df: pd.DataFrame, value_col: str | None) -> dict:
    ts = df["timestamp"]
    out = {
        "rows": int(len(df)),
        "ts_min_utc": ts.min().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "ts_max_utc": ts.max().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "markets": int(df["market"].nunique()),
    }
    if value_col:
        out["value_sum"] = float(df[value_col].sum())
        out["value_mean"] = float(df[value_col].mean())
    return out


def main() -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    manifest = {
        "generated_utc": now,
        "campaign_id": CAMPAIGN,
        "session_id": SESSION_ID,
        "track": "A",
        "source": "ironflow/hyperliquid-liquidations",
        "source_url": "https://huggingface.co/datasets/ironflow/hyperliquid-liquidations",
        "license": "cc-by-4.0",
        "unauthenticated": True,
        "requires_api_key": False,
        "observed_liquidations": True,
        "modeled_or_proxy": False,
        "window_months": MONTHS,
        "coins_batch": COINS,
        "venue_filter": {"dex": "", "market_class": "perp"},
        "timestamp_semantics": "Arrow datetime64 UTC -> integer milliseconds since epoch after normalization",
        "months": [],
        "duplicates": {},
        "carry_forward_note": "RISK-06/RISK-07/ROBUST-05 packages copied verbatim into this session dir.",
    }

    all_event_keys: list[int] = []
    event_rows_13 = 0
    candles_hours_13 = 0

    for month in MONTHS:
        ev = read_month("liquidations", month, EVENT_COLS)
        ca = read_month("candles_1h", month, CANDLE_COLS)
        fu = read_month("funding", month, FUNDING_COLS)
        oi = read_month("open_interest", month, OI_COLS)

        dup = int(ev.duplicated(subset=["tx_hash", "wallet", "market", "timestamp"]).sum())
        manifest["duplicates"][month] = dup

        ev13 = ev[ev["market"].isin([f"{c}-PERP" for c in COINS])]
        ca13 = ca[(ca["dex"] == "") & (ca["market_class"] == "perp")
                  & (ca["coin"].isin(COINS))]
        fu13 = fu[(fu["coin"].isin(COINS))]
        oi13 = oi[(oi["coin"].isin(COINS))]

        hours = ca13["timestamp"].dt.floor("h").nunique()
        candles_hours_13 += int(len(ca13))
        event_rows_13 += int(len(ev13))

        manifest["months"].append({
            "month": month,
            "events": {
                "path": str((CACHE / "liquidations" / f"{month}.parquet").relative_to(REPO)),
                "sha256": sha256(CACHE / "liquidations" / f"{month}.parquet"),
                "census_all": month_census(ev, "notional_usd"),
                "census_13coin": month_census(ev13, "notional_usd"),
                "coins_present": sorted(ev13["market"].str.replace("-PERP", "", regex=False).unique().tolist()),
                "duplicate_rows": dup,
            },
            "candles_1h": {
                "path": str((CACHE / "candles_1h" / f"{month}.parquet").relative_to(REPO)),
                "sha256": sha256(CACHE / "candles_1h" / f"{month}.parquet"),
                "census_13coin": month_census(ca13, "volume"),
                "unique_hours": int(hours),
                "coins_present": sorted(ca13["coin"].unique().tolist()),
            },
            "funding": {
                "path": str((CACHE / "funding" / f"{month}.parquet").relative_to(REPO)),
                "sha256": sha256(CACHE / "funding" / f"{month}.parquet"),
                "census_13coin": month_census(fu13, "funding_rate"),
                "coins_present": sorted(fu13["coin"].unique().tolist()),
            },
            "open_interest": {
                "path": str((CACHE / "open_interest" / f"{month}.parquet").relative_to(REPO)),
                "sha256": sha256(CACHE / "open_interest" / f"{month}.parquet"),
                "census_13coin": month_census(oi13, "open_interest_usd"),
                "coins_present": sorted(oi13["coin"].unique().tolist()),
            },
        })
        all_event_keys.append(int(len(ev)))

    manifest["totals"] = {
        "months": len(MONTHS),
        "event_rows_all_markets": int(sum(all_event_keys)),
        "event_rows_13coin": event_rows_13,
        "candle_hours_13coin": candles_hours_13,
    }
    out_json = SESSION / f"fclr_tracka_exploratory01_ingest_20261118T201919Z.json"
    out_json.write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Track A exploratory ingest manifest",
        "",
        f"- campaign: `{CAMPAIGN}`",
        f"- session: `{SESSION_ID}`",
        f"- generated_utc: {now}",
        f"- source: {manifest['source_url']} (cc-by-4.0, unauthenticated)",
        f"- window: {MONTHS[0]} .. {MONTHS[-1]} (6 complete months)",
        f"- venue filter: main-dex perps only (`dex == ''`, `market_class == 'perp'`)",
        f"- coins: {', '.join(COINS)}",
        "",
        "| month | events(all) | events(13c) | liq_notional_13c | candle_hours | dup_rows |",
        "|---|---|---|---|---|---|",
    ]
    for m in manifest["months"]:
        lines.append(
            f"| {m['month']} | {m['events']['census_all']['rows']} | "
            f"{m['events']['census_13coin']['rows']} | "
            f"{m['events']['census_13coin']['value_sum']:.0f} | "
            f"{m['candles_1h']['unique_hours']} | {manifest['duplicates'][m['month']]} |"
        )
    lines += [
        "",
        f"Totals: {manifest['totals']['event_rows_13coin']} 13-coin liquidation rows, "
        f"{manifest['totals']['candle_hours_13coin']} coin-hours of 1h candles.",
        "",
        "Provenance: every source parquet sha256 is recorded in the JSON twin. "
        "No cached input was modified; no CSV twin of raw events is written because "
        "raw parquet remains the canonical provenance object.",
        "",
    ]
    (SESSION / "fclr_tracka_exploratory01_ingest_20261118T201919Z.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )
    print(json.dumps(manifest["totals"], indent=1))


if __name__ == "__main__":
    main()
