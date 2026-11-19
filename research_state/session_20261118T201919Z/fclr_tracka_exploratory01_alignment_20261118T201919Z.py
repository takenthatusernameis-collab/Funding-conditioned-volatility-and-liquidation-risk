#!/usr/bin/env python3
"""Track A exploratory alignment + admissibility: observed Hyperliquid liquidations.

Campaign : FCLR-LIQ-TRACKA-EXPLORATORY-01-20261118T201919Z
Session  : session_20261118T201919Z
Window   : 2025-11 .. 2026-04 (6 complete months), 13 main-dex perp coins.

Method
------
1. Build the coin-hour grid from 1h candles (main dex, market_class == "perp").
2. Floor observed liquidation event timestamps to the hour and aggregate
   liq_count / liq_notional_usd per coin-hour (observed labels only).
3. Join funding and open interest by (coin, hour).
4. Emit a stdlib-readable panel CSV (the canonical downstream twin).
5. Evaluate frozen admissibility gates; emit verdict JSON + MD.

No modeled/proxy liquidation column is read or written. No sealed Binance month
is touched. No network access.
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
UTC = timezone.utc

SESSION_ID = "session_20261118T201919Z"
CAMPAIGN = "FCLR-LIQ-TRACKA-EXPLORATORY-01-20261118T201919Z"
MONTHS = ["2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04"]
COINS = [
    "BTC", "ETH", "BNB", "SOL", "XRP", "AVAX", "DOGE", "LINK",
    "SUI", "ARB", "OP", "APT", "ADA",
]

# Frozen admissibility thresholds (prereg).
MIN_INSTRUMENTS = 5
MIN_COMPLETE_MONTHS = 3
MAX_GAP_RATE = 0.20
MIN_ALIGN_YIELD = 0.95

FORBIDDEN_LABEL_COLUMNS = {
    "modeled", "proxy", "liquidation_estimate", "estimated_liquidation",
    "synthetic_liquidation", "simulated_liquidation", "is_modeled", "is_proxy",
}


def month_start(month: str) -> pd.Timestamp:
    return pd.Timestamp(f"{month}-01T00:00:00Z")


def month_hours(month: str) -> int:
    start = month_start(month)
    end = start + pd.DateOffset(months=1)
    return int((end - start) / pd.Timedelta(hours=1))


def load(dataset: str, month: str) -> pd.DataFrame:
    return pd.read_parquet(CACHE / dataset / f"{month}.parquet")


def main() -> None:
    now = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    frames = []
    columns_seen: dict[str, list[str]] = {}
    per_coin_month = {}

    for month in MONTHS:
        ev = load("liquidations", month)
        ca = load("candles_1h", month)
        fu = load("funding", month)
        oi = load("open_interest", month)
        columns_seen[month] = list(ev.columns)

        ca = ca[(ca["dex"] == "") & (ca["market_class"] == "perp")
                & (ca["coin"].isin(COINS))].copy()
        ca["hour"] = ca["timestamp"].dt.floor("h")
        ca = ca[["coin", "hour", "close", "volume"]].drop_duplicates(["coin", "hour"])

        fu = fu[fu["coin"].isin(COINS)].copy()
        fu["hour"] = fu["timestamp"].dt.floor("h")
        fu = fu[["coin", "hour", "funding_rate", "premium"]].drop_duplicates(["coin", "hour"])

        oi = oi[oi["coin"].isin(COINS)].copy()
        oi["hour"] = oi["timestamp"].dt.floor("h")
        oi = oi[["coin", "hour", "mark_price", "open_interest_usd"]].drop_duplicates(
            ["coin", "hour"])

        ev = ev[ev["market"].isin([f"{c}-PERP" for c in COINS])].copy()
        ev["coin"] = ev["market"].str.replace("-PERP", "", regex=False)
        ev["hour"] = ev["timestamp"].dt.floor("h")
        ev["is_long"] = (ev["position_side"] == "long").astype(int)
        agg = ev.groupby(["coin", "hour"]).agg(
            liq_count=("notional_usd", "size"),
            liq_notional_usd=("notional_usd", "sum"),
            liq_long_count=("is_long", "sum"),
            liq_fills=("fills", "sum"),
        ).reset_index()
        agg["liq_short_count"] = agg["liq_count"] - agg["liq_long_count"]

        panel = ca.merge(agg, on=["coin", "hour"], how="left")
        panel = panel.merge(fu, on=["coin", "hour"], how="left")
        panel = panel.merge(oi, on=["coin", "hour"], how="left")
        for col in ("liq_count", "liq_long_count", "liq_short_count", "liq_fills",
                    "liq_notional_usd"):
            panel[col] = panel[col].fillna(0.0 if col == "liq_notional_usd" else 0).astype(
                "float64" if col == "liq_notional_usd" else "int64")
        panel["month"] = month
        frames.append(panel)

        n_expected = month_hours(month)
        for coin, g in panel.groupby("coin"):
            per_coin_month[f"{coin}|{month}"] = {
                "expected_hours": n_expected,
                "candle_hours": int(len(g)),
                "funding_hours": int(g["funding_rate"].notna().sum()),
                "oi_hours": int(g["open_interest_usd"].notna().sum()),
                "hours_with_liq": int((g["liq_count"] > 0).sum()),
                "liq_count": int(g["liq_count"].sum()),
                "liq_notional_usd": float(g["liq_notional_usd"].sum()),
                "gap_rate": round(1.0 - len(g) / n_expected, 6),
            }

    panel = pd.concat(frames, ignore_index=True)
    panel["hour_utc"] = panel["hour"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    out_cols = ["coin", "hour_utc", "month", "close", "volume", "funding_rate",
                "premium", "mark_price", "open_interest_usd", "liq_count",
                "liq_long_count", "liq_short_count", "liq_fills", "liq_notional_usd"]
    panel_out = panel[out_cols].sort_values(["coin", "hour_utc"])

    csv_path = SESSION / f"fclr_tracka_exploratory01_panel_20261118T201919Z.csv"
    panel_out.to_csv(csv_path, index=False)
    panel_sha = hashlib.sha256(csv_path.read_bytes()).hexdigest()

    # Alignment yield: observed events that land on an existing candle hour.
    candle_hours = set(zip(panel["coin"], panel["hour"]))
    dropped = 0
    joined = 0
    for month in MONTHS:
        ev = load("liquidations", month)
        ev = ev[ev["market"].isin([f"{c}-PERP" for c in COINS])].copy()
        ev["coin"] = ev["market"].str.replace("-PERP", "", regex=False)
        ev["hour"] = ev["timestamp"].dt.floor("h")
        keys = list(zip(ev["coin"], ev["hour"]))
        j = sum(1 for k in keys if k in candle_hours)
        joined += j
        dropped += len(keys) - j
    align_yield = round(joined / (joined + dropped), 6) if joined + dropped else 0.0

    coins_with_events = sorted({c for c in panel["coin"].unique()
                                if per_coin_month and any(
                                    per_coin_month[f"{c}|{m}"]["liq_count"] > 0 for m in MONTHS)})
    complete_months = []
    for m in MONTHS:
        ok = all(per_coin_month[f"{c}|{m}"]["gap_rate"] <= MAX_GAP_RATE for c in COINS)
        if ok:
            complete_months.append(m)
    max_gap = max(v["gap_rate"] for v in per_coin_month.values())

    forbidden_hits = sorted({c.lower() for cols in columns_seen.values() for c in cols}
                            & FORBIDDEN_LABEL_COLUMNS)

    gates = {
        "g1_provenance_hashed": True,
        "g2_instruments_ge_5": len(coins_with_events) >= MIN_INSTRUMENTS,
        "g3_complete_months_ge_3": len(complete_months) >= MIN_COMPLETE_MONTHS,
        "g4_gap_rate_le_20pct": max_gap <= MAX_GAP_RATE,
        "g5_observed_labels_only": not forbidden_hits,
        "g6_alignment_yield_ge_95pct": align_yield >= MIN_ALIGN_YIELD,
    }
    verdict = "ADMISSIBLE" if all(gates.values()) else "NOT_ADMISSIBLE"

    summary = {
        "generated_utc": now,
        "campaign_id": CAMPAIGN,
        "session_id": SESSION_ID,
        "window_months": MONTHS,
        "coins": COINS,
        "panel_rows": int(len(panel_out)),
        "panel_csv": str(csv_path.relative_to(REPO)),
        "panel_csv_sha256": panel_sha,
        "hours_with_liq_total": int((panel_out["liq_count"] > 0).sum()),
        "liq_count_total": int(panel_out["liq_count"].sum()),
        "liq_notional_usd_total": float(panel_out["liq_notional_usd"].sum()),
        "events_joined": joined,
        "events_unjoined": dropped,
        "alignment_yield": align_yield,
        "max_gap_rate": max_gap,
        "coins_with_events": coins_with_events,
        "complete_months": complete_months,
        "forbidden_label_columns": forbidden_hits,
        "funding_coverage_rate": round(float(panel_out["funding_rate"].notna().mean()), 6),
        "oi_coverage_rate": round(float(panel_out["open_interest_usd"].notna().mean()), 6),
        "per_coin_month": per_coin_month,
        "gates": gates,
        "verdict": verdict,
        "label_definition": "observed Hyperliquid perp forced-liquidation event rows "
                            "(one row = one liquidation), aggregated to coin-hour counts "
                            "and USD notional; absence from feed is not evidence of no liquidation",
        "scope_limits": [
            "Exploratory only: no confirmatory split, model, or claim.",
            "Window limited to cached 2025-11..2026-04; 2026-05..2026-10 requires a bulk fetch.",
            "Reporting caps and venue collector gaps are unquantified from public metadata.",
        ],
    }
    (SESSION / "fclr_tracka_exploratory01_alignment_20261118T201919Z.json").write_text(
        json.dumps(summary, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# Track A exploratory alignment (observed Hyperliquid liquidations)",
        "",
        f"- campaign: `{CAMPAIGN}`",
        f"- window: {MONTHS[0]}..{MONTHS[-1]}; coins: {len(COINS)} main-dex perps",
        f"- panel rows: {len(panel_out)} -> `{summary['panel_csv']}`",
        f"- observed liquidation events: {summary['liq_count_total']} "
        f"(USD notional {summary['liq_notional_usd_total']:.0f})",
        f"- events joined to candle hours: {joined} / {joined + dropped} "
        f"(yield {align_yield:.4f})",
        f"- hours with >=1 liquidation: {summary['hours_with_liq_total']}",
        f"- funding coverage: {summary['funding_coverage_rate']:.3f}; "
        f"OI coverage: {summary['oi_coverage_rate']:.3f}",
        f"- max coin-month candle gap rate: {max_gap:.4f}",
        "",
        "## Gates",
        "",
    ]
    for k, v in gates.items():
        lines.append(f"- `{k}`: {'PASS' if v else 'FAIL'}")
    lines += [
        "",
        f"**Verdict:** `{verdict}`",
        "",
        "Absence from the feed is not evidence of no liquidation; the panel labels "
        "observed events only. This is an admissibility assessment, not a forecast test.",
        "",
    ]
    (SESSION / "fclr_tracka_exploratory01_alignment_20261118T201919Z.md").write_text(
        "\n".join(lines), encoding="utf-8")

    admiss = {
        "generated_utc": now,
        "campaign_id": CAMPAIGN,
        "session_id": SESSION_ID,
        "source": "ironflow/hyperliquid-liquidations",
        "source_url": "https://huggingface.co/datasets/ironflow/hyperliquid-liquidations",
        "license": "cc-by-4.0",
        "unauthenticated": True,
        "venue": "hyperliquid_perpetuals",
        "observed_labels": True,
        "modeled_or_proxy": False,
        "status": verdict,
        "instruments": len(coins_with_events),
        "complete_month": len(complete_months),
        "blocks": len(complete_months),
        "window_months": MONTHS,
        "coins_with_events": coins_with_events,
        "alignment_yield": align_yield,
        "max_gap_rate": max_gap,
        "gates": gates,
        "evidence": {
            "ingest_manifest": "fclr_tracka_exploratory01_ingest_20261118T201919Z.json",
            "alignment_summary": "fclr_tracka_exploratory01_alignment_20261118T201919Z.json",
            "panel_csv_sha256": panel_sha,
        },
        "shortfalls": [k for k, v in gates.items() if not v],
        "confirmatory_design_registered": False,
        "next_action": (
            "Register FCLR-LIQ-TRACKA-CONFIRMATORY-01 only after extending the "
            "candle/funding/OI cache to 2026-05..2026-10 and re-running this audit."
            if verdict == "ADMISSIBLE" else
            "Track A remains DATA_BLOCKED; document the failing gate."
        ),
    }
    (SESSION / "fclr_tracka_exploratory01_admissibility_20261118T201919Z.json").write_text(
        json.dumps(admiss, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    md = [
        "# Track A exploratory admissibility verdict",
        "",
        f"- status: **{verdict}**",
        f"- instruments with observed liquidations: {len(coins_with_events)} "
        f"(gate >= {MIN_INSTRUMENTS})",
        f"- complete months: {len(complete_months)} (gate >= {MIN_COMPLETE_MONTHS})",
        f"- max coin-month candle gap: {max_gap:.4f} (gate <= {MAX_GAP_RATE})",
        f"- alignment yield: {align_yield:.4f} (gate >= {MIN_ALIGN_YIELD})",
        f"- observed-only labels: {not forbidden_hits}",
        "",
        "## Gate detail",
        "",
    ]
    for k, v in gates.items():
        md.append(f"- `{k}`: {'PASS' if v else 'FAIL'}")
    md += [
        "",
        "## Consequences",
        "",
        admiss["next_action"],
        "",
        "No confirmatory claim is made in this exploratory session.",
        "",
    ]
    (SESSION / "fclr_tracka_exploratory01_admissibility_20261118T201919Z.md").write_text(
        "\n".join(md), encoding="utf-8")

    print(json.dumps({"verdict": verdict, "gates": gates, "panel_rows": len(panel_out),
                      "alignment_yield": align_yield, "max_gap": max_gap}, indent=1))


if __name__ == "__main__":
    main()
