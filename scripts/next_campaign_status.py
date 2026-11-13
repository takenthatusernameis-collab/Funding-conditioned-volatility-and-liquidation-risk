#!/usr/bin/env python3
"""Campaign truth: what is actually executable right now.

Two failure modes this script exists to prevent:

1. A session declares "no frozen prereg remains executable" while a valid,
   pre-outcomes prereg exists whose experiment id simply has no matching
   evaluation artifact (this happened for FCLR-FWD-VOL-2024Q4-CROSS, which sat
   frozen and unexecuted for ~1 hour across several sessions because the
   executor hardcoded a different filename stem).
2. A session declares the cached data exhausted while a complete, disjoint,
   never-tested window is still on disk.

Reads only. No network. No outcome computation.

Usage:
  python3 scripts/next_campaign_status.py
  python3 scripts/next_campaign_status.py --json
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
CACHE = RS / "data_cache"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
KINDS = ("markPriceKlines", "premiumIndexKlines", "indexPriceKlines")

# Windows already consumed by a sealed or terminal cell. Keep this list honest:
# a window listed here must not be re-proposed as "new".
TESTED_WINDOWS = [
    ("2024-07-23", "2024-09-30", "FCLR-FWD-VOL-2024Q4-CROSS (NOT_REPLICATED)"),
    ("2025-02-01", "2025-05-31", "FCLR-FWD-VOL-2025-CROSS (NOT_REPLICATED)"),
    ("2026-05-01", "2026-08-31", "FCLR-011 sealed PASS + FCLR-FWD-VOL-011-CONFIRM"),
    ("2026-08-03", "2026-10-31", "FCLR-FWD-VOL-011-CONFIRM forward walk"),
    ("2025-07-23", "2025-10-15", "FCLR-FWD-VOL-2025H2-CROSS (NOT_REPLICATED)"),
    ("2026-01-01", "2026-04-01", "FCLR-FWD-VOL-2025Q1Q2-CROSS (NOT_REPLICATED)"),
]


def read_json(p: Path):
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def _tokens(s: str) -> set[str]:
    return {t for t in re.split(r"[^A-Za-z0-9]+", s.upper()) if t}


def evaluation_index() -> list[dict]:
    """Parse each evaluation artifact into {stem, tokens, experiment_id}."""
    out = []
    for ev in RS.glob("evaluation_summary_*.json"):
        d = read_json(ev) or {}
        exp = d.get("experiment_id")
        out.append({
            "path": ev.name,
            "experiment_id": exp,
            "tokens": _tokens(exp) if exp else _tokens(ev.stem),
        })
    return out


def prereg_status() -> dict:
    """List frozen preregs and whether an evaluation artifact exists for them."""
    evals = evaluation_index()
    rows = []
    for p in sorted(RS.glob("prereg_*.json")):
        d = read_json(p)
        if not d:
            continue
        exp = d.get("experiment_id") or p.stem
        status = d.get("status")
        frozen = bool(d.get("frozen_before_outcomes") or d.get("pre_registered_before_outcomes"))
        post = d.get("outcome_data_inspected_before_freeze")
        # Executed iff some evaluation artifact names this exact experiment id, or
        # shares its distinctive cell token (e.g. 2024Q4, 2025, 011).
        want = _tokens(exp)
        executed = False
        for ev in evals:
            if ev["experiment_id"] == exp or want <= ev["tokens"]:
                executed = True
                break
        rows.append({
            "prereg": p.name,
            "experiment_id": exp,
            "status": status,
            "frozen_before_outcomes": frozen,
            "outcomes_inspected_before_freeze": post,
            "has_evaluation_artifact": executed,
            # Terminal cells legitimately keep a frozen prereg; only an unexecuted
            # frozen prereg is actionable.
            "actionable_now": bool(frozen and post is False and not executed),
        })
    return {"preregs": rows}


def funding_months(sym: str) -> set[str]:
    """Funding is cached as <SYM>_YYYY_MM/<SYM>-fundingRate-YYYY-MM/*.csv."""
    out = set()
    for d in CACHE.glob(f"{sym}_20??_??/{sym}-fundingRate-*"):
        m = re.search(r"fundingRate-(\d{4}-\d{2})", d.name)
        if m and any(d.glob("*.csv")):
            out.add(m.group(1))
    return out


def kline_months(sym: str) -> dict[str, dict[str, int]]:
    """Return {YYYY-MM: {kind: csv_count}} for one symbol."""
    out: dict[str, dict[str, int]] = {}
    for d in CACHE.glob(f"{sym}_20??_??"):
        m = re.search(r"_(\d{4})_(\d{2})$", d.name)
        if not m:
            continue
        key = f"{m.group(1)}-{m.group(2)}"
        row = out.setdefault(key, {k: 0 for k in KINDS})
        for kind in KINDS:
            for sub in d.glob(f"{kind}-*"):
                row[kind] += len(list(sub.glob("*.csv")))
    return out


def ready_windows() -> list[dict]:
    """Complete, funding-backed months that are not already inside a tested window."""
    months: dict[str, dict[str, int]] = {}
    for sym in SYMBOLS:
        for key, counts in kline_months(sym).items():
            tgt = months.setdefault(key, {k: 0 for k in KINDS})
            for k, v in counts.items():
                tgt[k] += v

    funding = set()
    for sym in SYMBOLS:
        funding |= funding_months(sym)

    rows = []
    for key, counts in sorted(months.items()):
        complete = all(counts[k] >= 5 * 25 for k in KINDS)  # ~5 symbols x ~30 days
        if not complete:
            continue
        overlaps = [lbl for (a, b, lbl) in TESTED_WINDOWS if a[:7] <= key <= b[:7]]
        rows.append({
            "month": key,
            "mark_csv": counts["markPriceKlines"],
            "premium_csv": counts["premiumIndexKlines"],
            "index_csv": counts["indexPriceKlines"],
            "funding_available": key in funding,
            "inside_tested_window": bool(overlaps),
            "tested_by": overlaps[0] if overlaps else None,
        })
    return rows


# A rolling-origin design needs, for each of 3 non-overlapping 30-day test
# blocks, >=30 days of prior train plus a 7-day embargo. The minimum span is
# therefore 30 (train) + 7 (embargo) + 3 x 30 (tests) = 127 days.
MIN_DESIGN_DAYS = 30 + 7 + 3 * 30


def _month_days(key: str) -> int:
    """Days in a YYYY-MM month key (calendar length)."""
    import calendar
    y, m = int(key[:4]), int(key[5:7])
    return calendar.monthrange(y, m)[1]


def design_feasible_months(rows: list[dict]) -> dict:
    """Contiguous runs of ready, funding-backed, untested months that can host a
    full 3-block pre-registered design under MIN_DESIGN_DAYS.

    A month is only usable if it is funding-backed and outside every tested
    window. Only *contiguous* runs matter: a rolling-origin design needs an
    unbroken history. A run shorter than MIN_DESIGN_DAYS cannot support the
    frozen design even though the individual months are 'ready'.
    """
    usable = {w["month"] for w in rows
              if w["funding_available"] and not w["inside_tested_window"]}
    if not usable:
        return {"runs": [], "any_feasible": False}

    ordered = sorted(usable)
    runs: list[list[str]] = []
    cur = [ordered[0]]
    for prev, nxt in zip(ordered, ordered[1:]):
        py, pm = int(prev[:4]), int(prev[5:7])
        ny, nm = int(nxt[:4]), int(nxt[5:7])
        pm += 1
        if pm > 12:
            pm = 1
            py += 1
        if (ny, nm) == (py, pm):
            cur.append(nxt)
        else:
            runs.append(cur)
            cur = [nxt]
    runs.append(cur)

    out = []
    for run in runs:
        days = sum(_month_days(m) for m in run)
        out.append({"months": run, "span_days": days,
                    "feasible": days >= MIN_DESIGN_DAYS})
    return {"runs": out, "any_feasible": any(r["feasible"] for r in out),
            "min_design_days": MIN_DESIGN_DAYS}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    pr = prereg_status()
    actionable = [r for r in pr["preregs"] if r["actionable_now"]]
    windows = ready_windows()
    ready = [w for w in windows if w["funding_available"] and not w["inside_tested_window"]]
    partial = [w for w in windows if not w["funding_available"] and not w["inside_tested_window"]]
    feasibility = design_feasible_months(windows)

    if args.json:
        print(json.dumps({"actionable_preregs": actionable,
                          "ready_funding_backed_months": ready,
                          "no_funding_months": partial,
                          "design_feasibility": feasibility}, indent=1))
        return

    print("== FROZEN PRE-RESULTS PREREGS WITHOUT AN EVALUATION ARTIFACT ==")
    if actionable:
        for r in actionable:
            print(f"  ACTIONABLE  {r['experiment_id']}  ({r['prereg']})")
        print("\n  -> Freeze/execute these BEFORE declaring the campaign closed.")
    else:
        print("  none (every frozen prereg has an evaluation artifact)")

    print("\n== COMPLETE CACHED MONTHS (5 symbols) ==")
    for w in windows:
        flag = "TESTED" if w["inside_tested_window"] else ("READY" if w["funding_available"] else "NO-FUNDING")
        print(f"  {w['month']}  {flag:10s} mark={w['mark_csv']:4d} prem={w['premium_csv']:4d} "
              f"idx={w['index_csv']:4d} funding={w['funding_available']}")

    print("\n== READY, DISJOINT, FUNDING-BACKED MONTHS ==")
    if ready:
        for w in ready:
            print(f"  {w['month']}")
    else:
        print("  none")

    print("\n== CONTIGUOUS RUN FEASIBILITY FOR A 3-BLOCK PRE-REGISTERED DESIGN ==")
    runs = feasibility["runs"]
    if not runs:
        print("  no ready disjoint funding-backed months -> cache frontier exhausted")
    else:
        for r in runs:
            tag = "FEASIBLE" if r["feasible"] else "TOO SHORT"
            print(f"  {r['months'][0]}..{r['months'][-1]}  span={r['span_days']}d  "
                  f"(need >= {feasibility['min_design_days']}d)  {tag}")
        if feasibility["any_feasible"]:
            print("\n  -> A full 3-block pre-registered design fits a FEASIBLE run above.")
        else:
            print("\n  -> No contiguous run spans enough days; a 3-block design would "
                  "need an empty/overlapping train. Cache frontier EXHAUSTED for a full "
                  "pre-registered funding-conditioned test.")

    print("\n== MONTHS WITH COMPLETE KLINES BUT NO FUNDING (baseline-only designs) ==")
    if partial:
        for w in partial:
            print(f"  {w['month']}  (funding starts 2024-04)")
    else:
        print("  none")


if __name__ == "__main__":
    main()