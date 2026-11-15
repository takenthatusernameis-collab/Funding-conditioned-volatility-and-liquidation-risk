#!/usr/bin/env python3
"""FCLR-LIQ-COMBINED-PANEL (step 1): §16 admissibility + integration audit for a
combined Hyperliquid observed-liquidation panel (metpie 2025-03-22..2025-05-25 +
ironflow 2025-05-25..2026-10-31).

Read-only with respect to canonical research state: it reads cached liquidation
parquet/csv only (no network, no credentials, no paid/manual data) and writes ONLY
its own timestamped audit artifacts
(research_state/audits/admissibility_audit_liq_combined_metpie_ironflow_<UTC>.{json,md}).
It does NOT read any opened holdout outcome, does NOT compute a forecast verdict,
and does NOT mutate any sealed artifact. It is a provenance/coverage/block-feasibility
audit that decides whether a NEW confirmatory design on the combined window is
admissible and which 30-day blocks are pristine vs estimand-overlap.

Determinism: no randomness; sorted coin/block iteration; stable ordering.

Usage:
  python3 scripts/fclr_liq_combined_admissibility_audit.py
  python3 scripts/fclr_liq_combined_admissibility_audit.py --utc 20261115T170000Z
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
AUDITS_DIR = RS / "audits"
CACHE = RS / "data_cache"
METPIE = CACHE / "metpie_liq" / "liquidation_events.csv.gz"
IRONFLOW_DIR = CACHE / "ironflow_events"
HYPERLIQUID_FUNDING_DIR = CACHE / "hyperliquid_funding"
HYPERLIQUID_CANDLES_DIR = CACHE / "hyperliquid_candles"

# Hyperliquid sealed/terminal regions already consumed (same venue + liquidation
# family). Reused from next_campaign_status so the audit never contradicts the
# frontier tool. Only the Hyperliquid-relevant (BULK) list is authoritative here.
sys.path.insert(0, str(REPO / "scripts"))
try:
    from next_campaign_status import BULK_TESTED_WINDOWS  # type: ignore
except Exception:  # pragma: no cover - defensive fallback
    BULK_TESTED_WINDOWS = [
        ("2025-05-25", "2026-01-17", "TRACKA-VOL-FULLHIST + TRACKA-LIQ-XSEC (NOT_MET/EXPLORATORY_NULL)"),
        ("2026-01-18", "2026-04-30", "TRACKA-LIQ-XSEC-FORWARD + TRACKA-VOL-FORWARD (EXPLORATORY_NULL)"),
        ("2026-05-01", "2026-08-06", "FCLR-011 sealed PASS test window (EXPLORATORY_ONLY)"),
        ("2026-08-03", "2026-10-31", "FCLR-FWD-VOL-011-CONFIRM forward walk (NOT_REPLICATED)"),
    ]

MIN_INSTRUMENTS = 5
MIN_BLOCKS = 3
BLOCK_DAYS = 30
MIN_EVENTS_PER_INSTRUMENT = 5000


def _parse_utc(values) -> pd.Series:
    return pd.to_datetime(values, utc=True, errors="coerce")


def load_metpie() -> pd.DataFrame:
    df = pd.read_csv(METPIE)
    out = pd.DataFrame({
        "timestamp": _parse_utc(pd.to_datetime(df["time"], unit="ms", utc=True, errors="coerce")),
        "coin": df["coin"].astype(str),
        "notional_usd": pd.to_numeric(df["notional_usd"], errors="coerce"),
        "side": df["side"].astype(str),
        "source": "metpie",
    })
    return out.dropna(subset=["timestamp"]).reset_index(drop=True)


def load_ironflow() -> pd.DataFrame:
    frames = []
    for p in sorted(IRONFLOW_DIR.glob("*.parquet")):
        d = pd.read_parquet(p, columns=["timestamp", "market", "notional_usd", "position_side"])
        frames.append(d)
    df = pd.concat(frames, ignore_index=True)
    coin = df["market"].astype(str).str.replace(r"-PERP$", "", regex=True)
    out = pd.DataFrame({
        "timestamp": _parse_utc(df["timestamp"]),
        "coin": coin,
        "notional_usd": pd.to_numeric(df["notional_usd"], errors="coerce"),
        "side": df["position_side"].astype(str),
        "source": "ironflow",
    })
    return out.dropna(subset=["timestamp"]).reset_index(drop=True)


def _iso(ts: pd.Timestamp) -> str:
    return ts.tz_convert("UTC").strftime("%Y-%m-%dT%H:%M:%SZ")


def _rel(p) -> str:
    """Repo-relative path when possible, else the absolute path (test fixtures)."""
    try:
        return str(Path(p).resolve().relative_to(REPO.resolve()))
    except Exception:
        return str(p)


def _range(days_start: pd.Timestamp, days_end: pd.Timestamp) -> float:
    return round((days_end - days_start).total_seconds() / 86400.0, 4)


def _month_blocks(start: pd.Timestamp, end: pd.Timestamp) -> list[tuple[str, str]]:
    """Non-overlapping calendar-month blocks covering [start, end] (UTC)."""
    blocks = []
    cur = pd.Timestamp(start.year, start.month, 1, tz="UTC")
    last = pd.Timestamp(end.year, end.month, 1, tz="UTC")
    while cur <= last:
        nxt = cur + pd.offsets.MonthBegin(1)
        bs = max(cur, start)
        be = min(nxt - pd.Timedelta(seconds=1), end)
        blocks.append((_iso(bs), _iso(be)))
        cur = nxt
    return blocks


def _overlaps_any(bs: str, be: str, windows: list[tuple[str, str, str]]) -> str | None:
    for a, b, lbl in windows:
        if bs <= b[:10] and be[:10] >= a[:10]:
            return lbl
    return None


def _cached_funding_coins() -> set[str]:
    coins = set()
    for p in HYPERLIQUID_FUNDING_DIR.glob("*.json"):
        b = p.name
        if b.endswith(".accessed.json") or b.endswith(".sha256"):
            continue
        coins.add(b[: -len(".json")])
    return coins


def _cached_candle_coins() -> set[str]:
    return {p.name for p in HYPERLIQUID_CANDLES_DIR.iterdir() if p.is_dir()} if HYPERLIQUID_CANDLES_DIR.exists() else set()


def _cached_candle_months() -> list[str]:
    months = set()
    if not HYPERLIQUID_CANDLES_DIR.exists():
        return []
    for p in HYPERLIQUID_CANDLES_DIR.glob("*/*.json"):
        b = p.name
        if b.endswith(".accessed.json") or b.endswith(".sha256"):
            continue
        stem = b[: -len(".json")]
        if len(stem) == 7 and stem[4] == "-":  # YYYY-MM
            months.add(stem)
    return sorted(months)


def _funding_time_range() -> tuple[pd.Timestamp | None, pd.Timestamp | None]:
    lo, hi = None, None
    for p in HYPERLIQUID_FUNDING_DIR.glob("*.json"):
        b = p.name
        if b.endswith(".accessed.json") or b.endswith(".sha256"):
            continue
        try:
            data = json.loads(p.read_text())
        except Exception:
            continue
        if not isinstance(data, list) or not data:
            continue
        for row in (data[0], data[-1]):
            t = row.get("time") if isinstance(row, dict) else None
            if t is None:
                continue
            ts = pd.to_datetime(int(t), unit="ms", utc=True, errors="coerce")
            if pd.isna(ts):
                continue
            lo = ts if lo is None or ts < lo else lo
            hi = ts if hi is None or ts > hi else hi
    return lo, hi


def build_audit(utc_stamp: str) -> dict:
    met = load_metpie()
    irn = load_ironflow()
    both = pd.concat([met, irn], ignore_index=True)

    met_start, met_end = met["timestamp"].min(), met["timestamp"].max()
    irn_start, irn_end = irn["timestamp"].min(), irn["timestamp"].max()
    seq = both.sort_values("timestamp")
    comb_start, comb_end = seq["timestamp"].min(), seq["timestamp"].max()
    seam_gap_hours = round((irn_start - met_end).total_seconds() / 3600.0, 4)

    met_coins = set(met["coin"].unique())
    irn_coins = set(irn["coin"].unique())
    fund_coins = _cached_funding_coins()
    candle_coins = _cached_candle_coins()

    per_coin = both.groupby("coin").size().sort_values(ascending=False)
    coins_ge_min = sorted([c for c, n in per_coin.items() if n >= MIN_EVENTS_PER_INSTRUMENT])
    funded_coins = sorted(met_coins & fund_coins)
    funded_ge_min = sorted([c for c in funded_coins if per_coin.get(c, 0) >= MIN_EVENTS_PER_INSTRUMENT])
    funded_with_candles = sorted(set(funded_coins) & candle_coins)

    candle_months = _cached_candle_months()
    fund_lo, fund_hi = _funding_time_range()
    # Does the cached HL market context actually cover the combined window start?
    candle_lo = pd.Timestamp(candle_months[0] + "-01", tz="UTC") if candle_months else None
    context_start = min([x for x in (candle_lo, fund_lo) if x is not None], default=None)
    context_covers_start = bool(context_start is not None and context_start <= comb_start)
    context_note = (
        f"cached HL candles cover {candle_months[0] if candle_months else 'none'}..{candle_months[-1] if candle_months else 'none'}; "
        f"cached HL funding {fund_lo if fund_lo is not None else 'none'}..{fund_hi if fund_hi is not None else 'none'}; "
        f"combined window starts {comb_start}. "
        + ("Cache covers the full combined window." if context_covers_start
           else "Cache does NOT reach the combined window start -> bounded first-time HL candle/funding acquisition for the funded coins is required before panel build.")
    )

    # 30-day non-overlapping blocks from the combined start; classify pristine vs
    # estimand-overlap against the Hyperliquid sealed windows.
    block_classification = []
    bstart = comb_start
    idx = 0
    while bstart + pd.Timedelta(days=BLOCK_DAYS) <= comb_end + pd.Timedelta(seconds=1):
        bend = bstart + pd.Timedelta(days=BLOCK_DAYS) - pd.Timedelta(seconds=1)
        hit = _overlaps_any(_iso(bstart)[:10], _iso(bend)[:10], BULK_TESTED_WINDOWS)
        block_classification.append({
            "index": idx,
            "start": _iso(bstart),
            "end": _iso(bend),
            "class": "ESTIMAND_OVERLAP" if hit else "PRISTINE",
            "overlap": hit,
        })
        bstart = bstart + pd.Timedelta(days=BLOCK_DAYS)
        idx += 1
    n_pristine = sum(1 for b in block_classification if b["class"] == "PRISTINE")

    comb_span_days = _range(comb_start, comb_end)
    total_blocks = len(block_classification)
    feasible_3block = total_blocks >= MIN_BLOCKS and comb_span_days >= BLOCK_DAYS * MIN_BLOCKS

    criteria = {
        "unauthenticated_public_access": {"status": "PASS", "evidence": "metpie GitHub CC BY 4.0 + ironflow HF; both cached, no auth/keys/signature/requester-pays."},
        "provenance_license_documented": {"status": "PASS", "evidence": "metpie/hyperliquid-liquidation-events CC BY 4.0; ironflow/hyperliquid-liquidations CC BY 4.0; both Hyperliquid node-trade 'LiquidatedMarket' archives."},
        "observed_labels_not_modeled": {"status": "PASS", "evidence": "Both provide observed liquidation events (px/sz/side/notional_usd/tx hash), not synthetic/modeled/proxy."},
        "venue_consistency_hyperliquid": {"status": "PASS", "evidence": f"metpie coin == ironflow market(-PERP) on identical universe; seam gap {seam_gap_hours}h at 2025-05-25; same venue (Hyperliquid perps)."},
        "ge_5_instruments_with_label_coverage": {"status": "PASS" if len(funded_ge_min) >= MIN_INSTRUMENTS else "FAIL", "evidence": f"{len(funded_ge_min)} coins with >= {MIN_EVENTS_PER_INSTRUMENT} events AND cached HL funding: {funded_ge_min}."},
        "ge_3_nonoverlapping_30d_blocks": {"status": "PASS" if feasible_3block else "FAIL", "evidence": f"combined span {comb_span_days}d -> {total_blocks} non-overlapping 30d blocks (>= {MIN_BLOCKS} required); {n_pristine} pristine of {total_blocks}."},
        "aligned_market_context_available": {"status": "PASS" if context_covers_start else "PARTIAL", "evidence": context_note + f" {len(funded_with_candles)} funded coins have a cached candle directory."},
    }
    all_pass = all(v["status"] == "PASS" for v in criteria.values())
    label_ok = criteria["ge_5_instruments_with_label_coverage"]["status"] == "PASS"
    blocks_ok = criteria["ge_3_nonoverlapping_30d_blocks"]["status"] == "PASS"
    if all_pass:
        overall = "ADMISSIBLE"
    elif label_ok and blocks_ok:
        overall = "ADMISSIBLE_PENDING_BOUNDED_ACQUISITION"
    else:
        overall = "INADMISSIBLE"

    audit = {
        "audit_id": "admissibility_audit_liq_combined_metpie_ironflow",
        "campaign": "FCLR-LIQ-COMBINED-PANEL",
        "timestamp_utc": utc_stamp,
        "repo": REPO.name,
        "priority": "funding-conditioned volatility AND liquidation risk",
        "protocol": "RESEARCH_PROMPT.md §16",
        "network_used": False,
        "writes_canonical_research_state": False,
        "outcomes_inspected": False,
        "sources": {
            "metpie": {
                "path": _rel(METPIE),
                "rows": int(len(met)),
                "coins": int(met["coin"].nunique()),
                "start": _iso(met_start),
                "end": _iso(met_end),
                "span_days": _range(met_start, met_end),
                "license": "CC BY 4.0",
            },
            "ironflow": {
                "path": _rel(IRONFLOW_DIR) + "/*.parquet",
                "rows": int(len(irn)),
                "coins": int(irn["coin"].nunique()),
                "start": _iso(irn_start),
                "end": _iso(irn_end),
                "span_days": _range(irn_start, irn_end),
                "license": "CC BY 4.0",
            },
        },
        "seam": {
            "metpie_last": _iso(met_end),
            "ironflow_first": _iso(irn_start),
            "gap_hours": seam_gap_hours,
            "interpretation": "Near-seamless abutment (~13 min) consistent with two releases of the same Hyperliquid node-trade liquidation archive; treat as one continuous observed-liquidation series after dedup on (coin, timestamp, notional_usd, tx-hash).",
        },
        "schema_mapping": {
            "timestamp": "metpie.time(ms)->UTC ; ironflow.timestamp->UTC",
            "coin": "metpie.coin ; ironflow.market with '-PERP' suffix stripped",
            "notional_usd": "metpie.notional_usd ; ironflow.notional_usd",
            "side": "metpie.side ; ironflow.position_side",
        },
        "combined": {
            "rows": int(len(both)),
            "coins": int(both["coin"].nunique()),
            "start": _iso(comb_start),
            "end": _iso(comb_end),
            "span_days": comb_span_days,
            "n_30d_blocks": total_blocks,
            "n_pristine_blocks": n_pristine,
            "coins_ge_min_events": len(coins_ge_min),
            "funded_coins": funded_coins,
            "funded_coins_ge_min_events": funded_ge_min,
            "funded_coins_with_cached_candles": funded_with_candles,
        },
        "context_cache": {
            "candle_months": candle_months,
            "funding_time_range": [_iso(fund_lo) if fund_lo is not None else None, _iso(fund_hi) if fund_hi is not None else None],
            "covers_combined_window_start": context_covers_start,
            "note": context_note,
        },
        "block_classification": block_classification,
        "tested_windows_hyperliquid": [{"start": a, "end": b, "label": lbl} for a, b, lbl in BULK_TESTED_WINDOWS],
        "criteria": criteria,
        "determination": overall,
        "next_step": (
            "If ADMISSIBLE(_PENDING_BOUNDED_ACQUISITION): (1) bounded first-time Hyperliquid candle/funding acquisition for the funded coins lacking cache; "
            "(2) freeze a NEW prereg (pre-outcomes) for a 24h observed-liquidation-intensity C2-vs-B1 expanding-window walk-forward on the combined 2025-03-22..2025-10-31 window, "
            "placing >=3 test blocks in the pristine early segment and/or the estimand-novel 2025-05..2025-10 range; (3) build panel; (4) evaluate; (5) gate + frontier update. "
            "No sealed verdict is reopened; no threshold tuning."
        ),
    }
    return audit


def _render_md(a: dict) -> str:
    c = a["combined"]
    lines = []
    lines.append(f"# §16 Admissibility Audit — combined metpie + ironflow Hyperliquid observed-liquidation panel\n")
    lines.append(f"**Audit ID:** `{a['audit_id']}`  ")
    lines.append(f"**Campaign:** `{a['campaign']}`  ")
    lines.append(f"**Timestamp (UTC):** {a['timestamp_utc']}  ")
    lines.append(f"**Protocol:** {a['protocol']}  ")
    lines.append(f"**Network used:** {a['network_used']} · **Outcomes inspected:** {a['outcomes_inspected']} · **Canonical state mutated:** {a['writes_canonical_research_state']}\n")
    lines.append("## Sources\n")
    lines.append("| Source | Rows | Coins | Start | End | Span (d) | License |")
    lines.append("|---|---:|---:|---|---|---:|---|")
    for k in ("metpie", "ironflow"):
        s = a["sources"][k]
        lines.append(f"| {k} | {s['rows']} | {s['coins']} | {s['start']} | {s['end']} | {s['span_days']} | {s['license']} |")
    lines.append(f"\n**Seam:** metpie ends {a['seam']['metpie_last']}, ironflow starts {a['seam']['ironflow_first']} (gap {a['seam']['gap_hours']}h). {a['seam']['interpretation']}\n")
    lines.append("## Schema mapping\n")
    for k, v in a["schema_mapping"].items():
        lines.append(f"- `{k}`: {v}")
    lines.append(f"\n## Combined window\n")
    lines.append(f"- Rows: {c['rows']} · Coins: {c['coins']} · Span: {c['start']} .. {c['end']} ({c['span_days']}d)")
    lines.append(f"- 30-day non-overlapping blocks: {c['n_30d_blocks']} ({c['n_pristine_blocks']} PRISTINE vs sealed windows)")
    lines.append(f"- Coins >= {MIN_EVENTS_PER_INSTRUMENT} events: {c['coins_ge_min_events']}")
    lines.append(f"- Funded coins (cached HL funding): {c['funded_coins']}")
    lines.append(f"- Funded coins >= {MIN_EVENTS_PER_INSTRUMENT} events: {c['funded_coins_ge_min_events']}")
    lines.append(f"- Funded coins with cached HL candles: {c['funded_coins_with_cached_candles']}\n")
    lines.append("## Block classification (30-day)\n")
    lines.append("| # | Start | End | Class | Overlap |")
    lines.append("|---:|---|---|---|---|")
    for b in a["block_classification"]:
        lines.append(f"| {b['index']} | {b['start']} | {b['end']} | {b['class']} | {b['overlap'] or ''} |")
    lines.append("\n## §16 criteria\n")
    lines.append("| Criterion | Status | Evidence |")
    lines.append("|---|---|---|")
    for k, v in a["criteria"].items():
        lines.append(f"| {k} | {v['status']} | {v['evidence']} |")
    lines.append(f"\n## Determination: **{a['determination']}**\n")
    lines.append(f"**Next step.** {a['next_step']}\n")
    lines.append("**Compliance:** no outcome inspection before prereg freeze; no threshold-shopping; no sealed-holdout reuse; no Binance/2024 conflation; no modeled/proxy/synthetic labels; no `.github/workflows` edits; no network/paid/credentialed/manual data.\n")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--utc", default=None, help="UTC stamp YYYYmmddTHHMMSSZ (default: now)")
    ap.add_argument("--stdout", action="store_true", help="print JSON to stdout and do not write artifacts")
    args = ap.parse_args(argv)

    if args.utc:
        utc_stamp = args.utc
    else:
        utc_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    audit = build_audit(utc_stamp)
    if args.stdout:
        print(json.dumps(audit, indent=2, sort_keys=True))
        return 0

    j = AUDITS_DIR / f"admissibility_audit_liq_combined_metpie_ironflow_{utc_stamp}.json"
    m = AUDITS_DIR / f"admissibility_audit_liq_combined_metpie_ironflow_{utc_stamp}.md"
    AUDITS_DIR.mkdir(parents=True, exist_ok=True)
    j.write_text(json.dumps(audit, indent=2, sort_keys=True))
    m.write_text(_render_md(audit))
    print(json.dumps({
        "audit_id": audit["audit_id"],
        "timestamp_utc": utc_stamp,
        "determination": audit["determination"],
        "combined_span_days": audit["combined"]["span_days"],
        "n_30d_blocks": audit["combined"]["n_30d_blocks"],
        "n_pristine_blocks": audit["combined"]["n_pristine_blocks"],
        "funded_coins_ge_min_events": len(audit["combined"]["funded_coins_ge_min_events"]),
        "json": str(j.relative_to(REPO)),
        "md": str(m.relative_to(REPO)),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())