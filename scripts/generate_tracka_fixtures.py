#!/usr/bin/env python3
"""Generate deterministic, leakage-safe Track A (FCLR-010) dry-run fixtures.

Pure Python (no pandas/pyarrow). Produces train/val/test JSONL panels matching
the frozen FCLR-010 schema contract in tests/fixtures/tracka/README.md, plus a
manifest.json recording the frozen split boundaries.

Deterministic seed => identical fixtures on every clone, so the dry-run is
reproducible without the ironflow census or any network access.

Leakage safety: every feature is computed from rows strictly prior to the
forecast timestamp (rolling windows look backward only). The generator is
deliberately simple so the dry-run's leakage assertion is about the FEATURE
COMPUTATION PATH, not about the synthetic generator's honesty.
"""
import json
import math
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "tracka"
SEED = 20261105
RNG = random.Random(SEED)

SYMBOLS = ["BTC-PERP", "ETH-PERP", "SOL-PERP", "AVAX-PERP", "ARB-PERP", "DOGE-PERP"]

# Frozen split boundaries from run_manifest.json#split_boundaries_fclr010
SPLITS = {
    "train": {"start": "2025-11-01T00:00:00Z", "end": "2026-03-06T23:00:00Z"},
    "validation": {"start": "2026-03-14T00:00:00Z", "end": "2026-05-20T23:00:00Z"},
    "test": {"start": "2026-05-28T00:00:00Z", "end": "2026-10-31T23:00:00Z"},
    "embargo_days": 7,
    "frozen_before_outcomes": True,
}


def parse_z(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def hour_range(start, end):
    """Yield every whole-hour UTC timestamp in [start, end]."""
    t = start.replace(minute=0, second=0, microsecond=0)
    end = end.replace(minute=0, second=0, microsecond=0)
    while t <= end:
        yield t
        t += timedelta(hours=1)


def synth_row(sym, ts, prev_by_sym):
    """One symbol-hour row. Funding/mark are causal by construction (drawn from
    a process indexed on ts); liquidation labels are drawn from a process that
    depends on the PRIOR hour's funding only, so the label can never leak the
    current-hour funding."""
    # Base price process (random walk in log space)
    last = prev_by_sym.get(sym, {}).get("mark_price", 30000.0 if "BTC" in sym else 2000.0)
    ret = RNG.gauss(0.0, 0.002)
    price = max(1.0, last * math.exp(ret))

    # Funding: mean-reverting with occasional extremes (the signal under test)
    fund = RNG.gauss(0.0, 0.0002)
    if RNG.random() < 0.05:
        fund += RNG.choice([-1, 1]) * 0.002

    # Liquidation occurrence depends on PRIOR-hour funding only (causal)
    prev_fund = prev_by_sym.get(sym, {}).get("funding_rate", 0.0)
    p_occ = 0.02 + 0.6 * abs(prev_fund) * 100
    p_occ = min(0.9, max(0.001, p_occ))
    occ = 1 if RNG.random() < p_occ else 0
    notional = 0.0
    if occ:
        notional = 1000.0 * (1.0 + abs(fund) * 500) * RNG.uniform(0.2, 5.0)

    return {
        "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "symbol": sym,
        "mark_price": round(price, 4),
        "funding_rate": round(fund, 8),
        "liquidation_count": occ,
        "notional_usd": round(notional, 2),
        "side": "long",
    }


def build_split(name, start_s, end_s):
    start, end = parse_z(start_s), parse_z(end_s)
    rows = []
    prev_by_sym = {}
    for ts in hour_range(start, end):
        for sym in SYMBOLS:
            r = synth_row(sym, ts, prev_by_sym)
            rows.append(r)
            prev_by_sym[sym] = r
    return rows


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "seed": SEED,
        "schema_contract": "tests/fixtures/tracka/README.md",
        "splits": SPLITS,
        "symbols": SYMBOLS,
        "files": {},
    }
    for name, (s, e) in SPLITS.items():
        if name in ("embargo_days", "frozen_before_outcomes"):
            continue
        rows = build_split(name, s, e)
        path = OUT / f"panel_{name}.jsonl"
        with open(path, "w") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        manifest["files"][name] = {
            "path": str(path.relative_to(path.parents[3])),
            "rows": len(rows),
            "hours": len(set(r["timestamp"] for r in rows)),
            "symbols": len(set(r["symbol"] for r in rows)),
        }
    with open(OUT / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote fixtures to {OUT}")
    for k, v in manifest["files"].items():
        print(f"  {k}: {v['rows']} rows, {v['hours']} hours, {v['symbols']} symbols")


if __name__ == "__main__":
    main()