"""Track C resume-trigger / panel admissibility audit (dep-light, no network, no outcomes).

Checks cached panel fragments against FCLR-014 confirmatory resume trigger:
  - >=5 symbols
  - >=3 non-overlapping 30-day OOS blocks (calendar days, contiguous coverage heuristic)
  - required series dirs/files present (mark/index/premium/funding/klines as available)
Reports coverage; does NOT compute targets, features, or model outcomes.

Usage: python scripts/trackc_panel_admissibility_audit.py [--cache research_state/data_cache] [--out research_state/trackc_panel_admissibility_latest.json]
"""
from __future__ import annotations
import argparse, json, os, re
from datetime import datetime, timezone
from pathlib import Path

SYMS_DEFAULT = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT"]
REQUIRED_SERIES = ["markPriceKlines","indexPriceKlines","premiumIndexKlines"]  # funding/klines noted separately


def collect_days(cache: Path, sym: str, window_hint: str | None = None):
    # scan sym dirs matching hint or all sym_* dirs
    days = set()
    series = {k: set() for k in REQUIRED_SERIES}
    has_funding = False
    has_klines_zip = False
    for d in sorted(cache.glob(f"{sym}_*")):
        if not d.is_dir():
            continue
        if window_hint and window_hint not in d.name:
            continue
        for child in d.rglob("*.csv"):
            m = re.search(r"(\d{4}-\d{2}-\d{2})", child.as_posix())
            if m:
                day = m.group(1)
                days.add(day)
                for s in REQUIRED_SERIES:
                    if s.lower().replace("klines","") in child.as_posix().lower() or s in child.as_posix():
                        series[s].add(day)
        for child in d.rglob("*funding*.csv"):
            m = re.search(r"(\d{4}-\d{2})", child.as_posix())
            if m:
                has_funding = True
        for child in d.rglob(f"{sym}-1h-*.zip"):
            has_klines_zip = True
    return sorted(days), {k: sorted(v) for k,v in series.items()}, has_funding, has_klines_zip


def non_overlapping_30d_blocks(n_days: int) -> int:
    return n_days // 30


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="research_state/data_cache")
    ap.add_argument("--symbols", default=",".join(SYMS_DEFAULT))
    ap.add_argument("--window-hint", default=None, help="substring filter for sym dirs, e.g. 2026_11")
    ap.add_argument("--out", default="research_state/trackc_panel_admissibility_latest.json")
    args = ap.parse_args()
    cache = Path(args.cache)
    syms = [s.strip() for s in args.symbols.split(",") if s.strip()]
    per = {}
    all_ok_syms = 0
    min_days = None
    for sym in syms:
        days, series, has_funding, has_klines = collect_days(cache, sym, args.window_hint)
        n = len(days)
        blocks = non_overlapping_30d_blocks(n)
        required_ok = all(len(series[s]) == n and n > 0 for s in REQUIRED_SERIES)
        sym_ok = n > 0 and required_ok
        if sym_ok:
            all_ok_syms += 1
            min_days = n if min_days is None else min(min_days, n)
        per[sym] = {
            "days": n, "range": [days[0], days[-1]] if days else None,
            "non_overlapping_30d_blocks": blocks,
            "required_series_complete": required_ok,
            "series_day_counts": {k: len(v) for k,v in series.items()},
            "has_funding_files_detected": has_funding,
            "has_1h_klines_zip_detected": has_klines,
            "resume_trigger_symbol_ok": sym_ok,
        }
    panel_blocks = non_overlapping_30d_blocks(min_days or 0)
    meets = all_ok_syms >= 5 and panel_blocks >= 3
    report = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cache": str(cache), "window_hint": args.window_hint, "symbols": syms,
        "per_symbol": per,
        "symbols_with_required_series": all_ok_syms,
        "min_complete_symbol_days": min_days or 0,
        "panel_non_overlapping_30d_blocks_estimate": panel_blocks,
        "resume_trigger_met": meets,
        "resume_trigger_rule": ">=5 symbols with required series AND >=3 non-overlapping 30d blocks (estimate; funding/provenance/prereg still required before outcomes)",
        "outcomes_computed": False, "network_used": False,
        "next_action_if_met": "freeze new prereg version before any outcome inspection; verify funding/provenance/checksums; materialize splits/manifest; run confirmatory pipeline with block-bootstrap/Holm per protocol",
        "next_action_if_not_met": "no confirmatory outcomes; continue resume-trigger watch (no default probing); keep dep-light gates green",
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"out": str(out), "resume_trigger_met": meets, "panel_blocks": panel_blocks, "symbols_ok": all_ok_syms}, indent=2))

if __name__ == "__main__":
    main()
