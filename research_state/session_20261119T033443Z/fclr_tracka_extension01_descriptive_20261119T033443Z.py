#!/usr/bin/env python3
"""FCLR-LIQ-TRACKA-EXTENSION-01 descriptive layer (stdlib only).

Reads the frozen 12-month Track A panel (13 main-dex Hyperliquid perps,
2025-11..2026-10) and emits descriptive associations only:

  * per-coin event totals / notional / share of hours with >=1 event
  * per-coin top-10 liquidation hours
  * per-coin weekday and hour-of-day profiles
  * event incidence by within-coin funding-rate decile and within-coin
    trailing-24h realized-volatility decile, with counts and Wilson 95% CIs

This is NOT a forecast test and must never be reported as predictive evidence.
Absence from the liquidation feed is not treated as evidence of no liquidation.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path

CAMPAIGN_ID = "FCLR-LIQ-TRACKA-EXTENSION-01-20261119T015256Z"
SESSION_ID = "session_20261119T033443Z"
UTC = "20261119T033443Z"
PANEL = Path(
    "research_state/session_20261119T022824Z/"
    "fclr_tracka_extension01_panel_session_20261119T022824Z.csv"
)
GEN_UTC = "2026-11-19T03:37:00Z"
RV_WINDOW_HOURS = 24
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def wilson(k: int, n: int, z: float = 1.96) -> list[float]:
    if n <= 0:
        return [0.0, 0.0]
    p = k / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2.0 * n)) / denom
    half = z * math.sqrt((p * (1.0 - p) + z * z / (4.0 * n)) / n) / denom
    return [max(0.0, centre - half), min(1.0, centre + half)]


def parse_hour(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def decile_assign(values: list[float]) -> list[int]:
    """Rank-based within-group deciles (ties broken by stable order)."""
    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    out = [0] * n
    for rank, idx in enumerate(order):
        out[idx] = min(9, (10 * rank) // n)
    return out


def aggregate_bins(rows: list[dict], key: str, label: str) -> list[dict]:
    bins = []
    for d in range(10):
        sub = [r for r in rows if r["decile"] == d]
        n = len(sub)
        k = sum(1 for r in sub if r["event"])
        lo, hi = wilson(k, n)
        vals = sorted(r[key] for r in sub)
        bins.append(
            {
                "decile": d + 1,
                "n_coin_hours": n,
                "n_hours_with_event": k,
                "incidence": (k / n) if n else 0.0,
                "incidence_ci95_low": lo,
                "incidence_ci95_high": hi,
                f"{label}_min": vals[0] if vals else None,
                f"{label}_max": vals[-1] if vals else None,
            }
        )
    return bins


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", type=Path, default=PANEL)
    ap.add_argument("--out-json", type=Path, required=True)
    ap.add_argument("--out-md", type=Path, required=True)
    args = ap.parse_args()

    by_coin: dict[str, list[dict]] = defaultdict(list)
    with args.panel.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            row["_hour"] = parse_hour(row["hour_utc"])
            row["_close"] = float(row["close"])
            row["_funding"] = float(row["funding_rate"])
            row["_liq_count"] = int(float(row["liq_count"]))
            row["_liq_notional"] = float(row["liq_notional_usd"])
            row["_event"] = row["_liq_count"] > 0
            by_coin[row["coin"]].append(row)

    coins = sorted(by_coin)
    n_coin_hours = 0
    total_events = 0.0
    total_notional = 0.0
    hours_with_event = 0
    per_coin = []
    funding_rows: list[dict] = []
    rv_rows: list[dict] = []
    weekday_agg: dict[str, dict] = {
        w: {"hours": 0, "hours_with_event": 0, "events": 0.0} for w in WEEKDAYS
    }
    hod_agg: dict[str, dict] = {
        f"{h:02d}": {"hours": 0, "hours_with_event": 0, "events": 0.0}
        for h in range(24)
    }

    for coin in coins:
        rows = sorted(by_coin[coin], key=lambda r: r["_hour"])
        closes = [r["_close"] for r in rows]
        logret = [None]
        for i in range(1, len(closes)):
            if closes[i - 1] > 0 and closes[i] > 0:
                logret.append(math.log(closes[i] / closes[i - 1]))
            else:
                logret.append(None)
        rv = [None] * len(rows)
        for i in range(len(rows)):
            if i < RV_WINDOW_HOURS:
                continue
            window = logret[i - RV_WINDOW_HOURS + 1:i + 1]
            if any(x is None for x in window):
                continue
            rv[i] = math.sqrt(sum(x * x for x in window))

        funding_vals = [r["_funding"] for r in rows]
        funding_dec = decile_assign(funding_vals)
        rv_pairs = [(i, rv[i]) for i in range(len(rows)) if rv[i] is not None]
        rv_dec = {i: d for (i, _), d in zip(rv_pairs, decile_assign([v for _, v in rv_pairs]))}

        for i, r in enumerate(rows):
            funding_rows.append(
                {"coin": coin, "decile": funding_dec[i], "funding_rate": r["_funding"],
                 "event": r["_event"]}
            )
            if i in rv_dec:
                rv_rows.append(
                    {"coin": coin, "decile": rv_dec[i], "rv": rv[i], "event": r["_event"]}
                )

        n = len(rows)
        ev = sum(1 for r in rows if r["_event"])
        events = sum(r["_liq_count"] for r in rows)
        notional = sum(r["_liq_notional"] for r in rows)
        n_coin_hours += n
        total_events += events
        total_notional += notional
        hours_with_event += ev

        top = sorted(
            rows,
            key=lambda r: (r["_liq_count"], r["_liq_notional"], r["hour_utc"]),
            reverse=True,
        )[:10]
        weekday_profile = {w: {"hours": 0, "hours_with_event": 0, "events": 0.0} for w in WEEKDAYS}
        hod_profile = {f"{h:02d}": {"hours": 0, "hours_with_event": 0, "events": 0.0}
                       for h in range(24)}
        for r in rows:
            w = WEEKDAYS[r["_hour"].weekday()]
            hh = f"{r['_hour'].hour:02d}"
            for prof, key in ((weekday_profile, w), (hod_profile, hh)):
                prof[key]["hours"] += 1
                prof[key]["hours_with_event"] += 1 if r["_event"] else 0
                prof[key]["events"] += r["_liq_count"]
            weekday_agg[w]["hours"] += 1
            weekday_agg[w]["hours_with_event"] += 1 if r["_event"] else 0
            weekday_agg[w]["events"] += r["_liq_count"]
            hod_agg[hh]["hours"] += 1
            hod_agg[hh]["hours_with_event"] += 1 if r["_event"] else 0
            hod_agg[hh]["events"] += r["_liq_count"]

        lo, hi = wilson(ev, n)
        per_coin.append(
            {
                "coin": coin,
                "n_coin_hours": n,
                "total_liq_events": events,
                "total_liq_notional_usd": notional,
                "hours_with_ge1_event": ev,
                "share_hours_with_ge1_event": ev / n if n else 0.0,
                "share_hours_with_ge1_event_ci95_low": lo,
                "share_hours_with_ge1_event_ci95_high": hi,
                "total_liq_long_count": sum(int(float(r["liq_long_count"])) for r in rows),
                "total_liq_short_count": sum(int(float(r["liq_short_count"])) for r in rows),
                "top10_liquidation_hours": [
                    {
                        "hour_utc": r["hour_utc"],
                        "liq_count": r["_liq_count"],
                        "liq_notional_usd": r["_liq_notional"],
                        "liq_long_count": int(float(r["liq_long_count"])),
                        "liq_short_count": int(float(r["liq_short_count"])),
                        "close": r["_close"],
                        "funding_rate": r["_funding"],
                    }
                    for r in top
                    if r["_liq_count"] > 0
                ],
                "weekday_profile": weekday_profile,
                "hour_of_day_profile": hod_profile,
                "rv_window_hours": RV_WINDOW_HOURS,
                "rv_nonmissing_hours": len(rv_pairs),
            }
        )

    funding_bins = aggregate_bins(funding_rows, "funding_rate", "funding_rate")
    rv_bins = aggregate_bins(rv_rows, "rv", "rv_24h")
    overall_lo, overall_hi = wilson(hours_with_event, n_coin_hours)

    out = {
        "generated_utc": GEN_UTC,
        "campaign_id": CAMPAIGN_ID,
        "session_id": SESSION_ID,
        "artifact": f"fclr_tracka_extension01_descriptive_{UTC}",
        "artifact_kind": "descriptive_layer",
        "predictive_claim": False,
        "confirmatory_evaluation_run": False,
        "panel_source": str(PANEL),
        "panel_rows": n_coin_hours,
        "coins": coins,
        "n_coins": len(coins),
        "window_months": sorted({r["month"] for rows in by_coin.values() for r in rows}),
        "label_contract": {
            "event": "liq_count >= 1 in the closed hour",
            "absence_is_zero": False,
            "absence_contract": "an hour with liq_count == 0 is an hour with no observed event in the feed; it is not proof that no liquidation occurred",
            "observed_labels": True,
            "modeled_or_proxy": False,
        },
        "rv_definition": (
            f"sqrt(sum of squared hourly log close-to-close returns over the trailing "
            f"{RV_WINDOW_HOURS} closed hours, ending at the prior hour; missing for the "
            f"first {RV_WINDOW_HOURS} rows of each coin"
        ),
        "summary": {
            "n_coin_hours": n_coin_hours,
            "total_liq_events": total_events,
            "total_liq_notional_usd": total_notional,
            "hours_with_ge1_event": hours_with_event,
            "share_hours_with_ge1_event": hours_with_event / n_coin_hours if n_coin_hours else 0.0,
            "share_hours_with_ge1_event_ci95_low": overall_lo,
            "share_hours_with_ge1_event_ci95_high": overall_hi,
        },
        "per_coin": per_coin,
        "aggregate_weekday_profile": {
            w: {
                **weekday_agg[w],
                "incidence": (weekday_agg[w]["hours_with_event"] / weekday_agg[w]["hours"])
                if weekday_agg[w]["hours"] else 0.0,
            }
            for w in WEEKDAYS
        },
        "aggregate_hour_of_day_profile": {
            h: {
                **hod_agg[h],
                "incidence": (hod_agg[h]["hours_with_event"] / hod_agg[h]["hours"])
                if hod_agg[h]["hours"] else 0.0,
            }
            for h in (f"{x:02d}" for x in range(24))
        },
        "incidence_by_funding_decile": {
            "definition": "deciles assigned within each coin on the same-hour funding_rate; pooled across coins",
            "bins": funding_bins,
        },
        "incidence_by_rv_decile": {
            "definition": (
                f"deciles assigned within each coin on trailing-{RV_WINDOW_HOURS}h realized volatility; "
                f"hours without a full trailing window are excluded"
            ),
            "n_coin_hours_with_rv": len(rv_rows),
            "bins": rv_bins,
        },
        "interpretation": (
            "Descriptive associations on observed liquidation labels. No model was fit, no "
            "out-of-sample forecast was evaluated, and no causal or predictive claim is made. "
            "The decile tables describe co-incidence in the same panel and must not be read as "
            "lead-lag evidence."
        ),
        "prohibitions_respected": {
            "no_confirmatory_evaluation": True,
            "no_sealed_binance_outcomes": True,
            "no_risk_05_06_07_rerun": True,
            "no_robust_05_rerun": True,
            "no_track_c_qlike_rerun": True,
            "stdlib_only": True,
            "no_zero_byte_artifacts": True,
        },
    }
    args.out_json.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def fmt_pct(x: float) -> str:
        return f"{100.0 * x:.3f}%"

    lines = [
        f"# Track A extension descriptive layer — {GEN_UTC}",
        "",
        f"Campaign: `{CAMPAIGN_ID}`  ",
        f"Session: `{SESSION_ID}`  ",
        "**Descriptive only. Not a forecast test. No predictive or causal claim.**",
        "",
        "## Scope",
        f"- Panel rows: {n_coin_hours:,} coin-hours",
        f"- Coins: {len(coins)} ({', '.join(coins)})",
        f"- Window: {out['window_months'][0]} .. {out['window_months'][-1]}",
        f"- Observed liquidation events: {int(total_events):,}",
        f"- Observed liquidation notional: ${total_notional:,.2f}",
        f"- Hours with >=1 observed event: {hours_with_event:,} "
        f"({fmt_pct(out['summary']['share_hours_with_ge1_event'])}, "
        f"Wilson 95% CI {fmt_pct(overall_lo)}..{fmt_pct(overall_hi)})",
        "",
        "Absence from the feed is not treated as evidence of no liquidation. "
        "A zero `liq_count` hour means no observed event in the feed, not a confirmed calm hour.",
        "",
        "## Per-coin summary",
        "",
        "| Coin | Events | Notional USD | Hours | Hours >=1 event | Share (95% CI) | RV hours |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for c in per_coin:
        lines.append(
            f"| {c['coin']} | {int(c['total_liq_events']):,} | ${c['total_liq_notional_usd']:,.0f} | "
            f"{c['n_coin_hours']:,} | {c['hours_with_ge1_event']:,} | "
            f"{fmt_pct(c['share_hours_with_ge1_event'])} "
            f"({fmt_pct(c['share_hours_with_ge1_event_ci95_low'])}.."
            f"{fmt_pct(c['share_hours_with_ge1_event_ci95_high'])}) | "
            f"{c['rv_nonmissing_hours']:,} |"
        )
    lines += ["", "## Incidence by within-coin funding-rate decile (pooled)", "",
              "| Decile | Coin-hours | Hours >=1 event | Incidence | Wilson 95% CI | Funding min | Funding max |",
              "|---:|---:|---:|---:|---|---:|---:|"]
    for b in funding_bins:
        lines.append(
            f"| {b['decile']} | {b['n_coin_hours']:,} | {b['n_hours_with_event']:,} | "
            f"{fmt_pct(b['incidence'])} | {fmt_pct(b['incidence_ci95_low'])}.."
            f"{fmt_pct(b['incidence_ci95_high'])} | {b['funding_rate_min']:.3e} | "
            f"{b['funding_rate_max']:.3e} |"
        )
    lines += ["", f"## Incidence by within-coin trailing-{RV_WINDOW_HOURS}h RV decile (pooled)", "",
              "| Decile | Coin-hours | Hours >=1 event | Incidence | Wilson 95% CI | RV min | RV max |",
              "|---:|---:|---:|---:|---|---:|---:|"]
    for b in rv_bins:
        lines.append(
            f"| {b['decile']} | {b['n_coin_hours']:,} | {b['n_hours_with_event']:,} | "
            f"{fmt_pct(b['incidence'])} | {fmt_pct(b['incidence_ci95_low'])}.."
            f"{fmt_pct(b['incidence_ci95_high'])} | {b['rv_24h_min']:.6f} | "
            f"{b['rv_24h_max']:.6f} |"
        )
    lines += [
        "",
        "## Top observed liquidation hours per coin",
        "",
    ]
    for c in per_coin:
        lines.append(f"### {c['coin']}")
        lines.append("")
        lines.append("| Hour (UTC) | liq_count | Notional USD | Long | Short | Close | Funding |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for r in c["top10_liquidation_hours"]:
            lines.append(
                f"| {r['hour_utc']} | {r['liq_count']:,} | ${r['liq_notional_usd']:,.0f} | "
                f"{r['liq_long_count']:,} | {r['liq_short_count']:,} | {r['close']:.6g} | "
                f"{r['funding_rate']:.3e} |"
            )
        lines.append("")
    lines += [
        "## Interpretation",
        "",
        out["interpretation"],
        "",
        "## Contract",
        "",
        "- Observed labels only; no modeled or proxy liquidation column was used.",
        "- No confirmatory evaluation was run in this campaign.",
        "- No sealed Binance month was read for outcomes.",
        "- Core statistics are stdlib only.",
        "",
    ]
    args.out_md.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "panel_rows": n_coin_hours,
        "coins": len(coins),
        "total_liq_events": total_events,
        "total_liq_notional_usd": total_notional,
        "hours_with_ge1_event": hours_with_event,
        "rv_coin_hours": len(rv_rows),
        "out_json": str(args.out_json),
        "out_md": str(args.out_md),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
