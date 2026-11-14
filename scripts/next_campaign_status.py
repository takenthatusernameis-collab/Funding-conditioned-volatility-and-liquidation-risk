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
3. A session declares the whole campaign exhausted because the *Binance 5-symbol*
   design has no feasible run left, while a completely separate cached dataset
   (the ironflow Hyperliquid bulk parquet: 1h candles + funding + OI + observed
   liquidation events) still has an untouched region. This actually happened: the
   tool reported "cache frontier EXHAUSTED" while 2025-11..2026-04 (181 days,
   ~180 native-perp coins with observed liquidation labels) had never been scored.

Reads only. No network. No outcome computation.

Usage:
  python3 scripts/next_campaign_status.py
  python3 scripts/next_campaign_status.py --json
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
CACHE = RS / "data_cache"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
KINDS = ("markPriceKlines", "premiumIndexKlines", "indexPriceKlines")

# Ironflow Hyperliquid bulk cache. This is a DIFFERENT data domain from the
# Binance 5-symbol cache above: many native perps, hourly candles + funding + OI
# + observed liquidation events, CC BY 4.0, unauthenticated, already on disk.
BULK = RS / "data_cache" / "ironflow_bulk"
BULK_DATASETS = ("candles_1h", "funding", "open_interest", "liquidations")
# Regions already consumed by a sealed/terminal cell in the Hyperliquid domain.
# 2026-01-18..2026-04-30 was the FullHist forward reserve; it is now tested and
# exhausted by TRACKA-LIQ-XSEC-FORWARD (EXPLORATORY_NULL) and TRACKA-VOL-FORWARD
# (EXPLORATORY_NULL/VALID_EXPLORATORY) per AGENT_HANDOFF 2026-11-14T13:15:35Z.
# Do NOT re-list it as an executable frontier.
BULK_TESTED_WINDOWS = [
    # Arm A train/embargo + Arm B burn-in/scored region of the FullHist campaign.
    ("2025-05-25", "2026-01-17", "TRACKA-VOL-FULLHIST + TRACKA-LIQ-XSEC (NOT_MET/EXPLORATORY_NULL)"),
    # Forward reserve consumed by the 2026Q1Q2 forward cells.
    ("2026-01-18", "2026-04-30", "TRACKA-LIQ-XSEC-FORWARD + TRACKA-VOL-FORWARD (EXPLORATORY_NULL; region exhausted)"),
]
# A forward cell is allowed to use a shorter, pre-registered window when the
# untouched region cannot fit the 30/30/30 rolling-origin skeleton. Minimum for
# that reduced design: 60 train + 7 embargo + 3 x 10 test = 97 days.
MIN_FORWARD_DESIGN_DAYS = 60 + 7 + 3 * 10

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
        if m and any(d.glob("**/*.csv")):
            out.add(m.group(1))
    return out


def kline_months(sym: str) -> dict[str, dict[str, int]]:
    """Return {YYYY-MM: {kind: csv_count}} for one symbol.

    Count recursively: some cache months nest per-day CSVs more deeply than the
    original one-level layout. A shallow glob undercounts those months and used
    to make a complete, executable block look absent.
    """
    out: dict[str, dict[str, int]] = {}
    for d in CACHE.glob(f"{sym}_20??_??"):
        m = re.search(r"_(\d{4})_(\d{2})$", d.name)
        if not m:
            continue
        key = f"{m.group(1)}-{m.group(2)}"
        row = out.setdefault(key, {k: 0 for k in KINDS})
        for kind in KINDS:
            for sub in d.glob(f"{kind}-*"):
                row[kind] += len(list(sub.glob("**/*.csv")))
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


# A disjoint 30-day block needs 30 days of train + a 7-day embargo + 30 test
# days. Unlike the rolling-origin design above, the three blocks do not need to
# be contiguous: each is an independent, never-tested month with its own train
# history. This is the design used by the current FCLR forward-volatility cells.
MIN_DISJOINT_BLOCKS = 3
DISJOINT_TRAIN_DAYS = 30
DISJOINT_EMBARGO_DAYS = 7
DISJOINT_TEST_DAYS = 30


def _month_start(key: str) -> date:
    return date.fromisoformat(f"{key}-01")


def _month_last_day(key: str) -> date:
    y, m = int(key[:4]), int(key[5:7])
    return date(y, m, _month_days(key))


def _months_between(start: date, end: date) -> list[str]:
    out = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out


def disjoint_block_frontier(rows: list[dict]) -> dict:
    """Find executable, independent 30-day test blocks.

    A block is usable when its test month is complete, funding-backed and not
    inside any tested window, and every calendar month in its 30-day train
    window is complete and funding-backed. Test months must be disjoint from
    prior tested windows; train months may overlap prior windows as legitimate
    pre-test history.

    Returns every ready month as a candidate plus the subset that is feasible.
    The campaign is executable when at least MIN_DISJOINT_BLOCKS blocks are
    feasible.
    """
    month_counts = {w["month"]: w for w in rows}
    blocks = []
    for w in rows:
        if not w.get("funding_available") or w.get("inside_tested_window"):
            continue
        key = w["month"]
        test_start_d = _month_start(key)
        test_end_d = _month_last_day(key)
        train_end_exclusive = test_start_d - timedelta(days=DISJOINT_EMBARGO_DAYS)
        train_start_d = train_end_exclusive - timedelta(days=DISJOINT_TRAIN_DAYS)
        train_months = _months_between(train_start_d, train_end_exclusive - timedelta(days=1))
        missing = []
        for m in train_months:
            c = month_counts.get(m)
            if not c or not c.get("funding_available"):
                missing.append(f"{m}:missing_or_unfunded")
                continue
            counts = {"markPriceKlines": c.get("mark_csv", 0),
                      "premiumIndexKlines": c.get("premium_csv", 0),
                      "indexPriceKlines": c.get("index_csv", 0)}
            if any(counts[k] < 5 * 25 for k in KINDS):
                missing.append(f"{m}:incomplete_kline_coverage")
        feasible = (w.get("funding_available")
                    and not w.get("inside_tested_window")
                    and not missing)
        blocks.append({
            "month": key,
            "train_start": f"{train_start_d.isoformat()}T00:00:00Z",
            "train_end": f"{(train_end_exclusive - timedelta(days=1)).isoformat()}T23:00:00Z",
            "embargo_start": f"{train_end_exclusive.isoformat()}T00:00:00Z",
            "embargo_end": f"{(test_start_d - timedelta(days=1)).isoformat()}T23:00:00Z",
            "test_start": f"{test_start_d.isoformat()}T00:00:00Z",
            "test_end": f"{test_end_d.isoformat()}T23:00:00Z",
            "train_months": train_months,
            "test_days": (test_end_d - test_start_d).days + 1,
            "train_days": DISJOINT_TRAIN_DAYS,
            "embargo_days": DISJOINT_EMBARGO_DAYS,
            "missing_train_months": missing,
            "feasible": bool(feasible),
            "reason": "complete funding-backed untested test block with complete train history"
                      if feasible else "; ".join(missing) or "unfunded or inside tested window",
        })
    feasible_blocks = [b for b in blocks if b["feasible"]]
    return {
        "blocks": blocks,
        "feasible_blocks": feasible_blocks,
        "n_feasible": len(feasible_blocks),
        "any_feasible": bool(feasible_blocks),
        "campaign_feasible": len(feasible_blocks) >= MIN_DISJOINT_BLOCKS,
        "min_blocks": MIN_DISJOINT_BLOCKS,
        "min_train_days": DISJOINT_TRAIN_DAYS,
        "min_embargo_days": DISJOINT_EMBARGO_DAYS,
        "min_test_days": DISJOINT_TEST_DAYS,
    }


def bulk_months(dataset: str) -> list[str]:
    """Months present in the ironflow bulk cache for one dataset."""
    d = BULK / dataset
    if not d.exists():
        return []
    return sorted(p.stem for p in d.glob("*.parquet"))


def bulk_frontier() -> dict:
    """Untouched, feasible regions in the ironflow Hyperliquid bulk cache.

    This is the second data domain the old tool was blind to. A region is
    usable when it is outside every tested Hyperliquid window and long enough to
    host a 3-block pre-registered design. Coverage of the datasets is read from
    the parquet month files already on disk; no file-content reads, no network.

    Month granularity is too coarse to be honest here: the Arm B burn-in starts
    mid-month (2025-05-25) and the scored region ends 2026-01-17, so a whole
    month such as 2026-01 is partly tested. This function therefore works in
    *days*: each dataset's month files give a covered month set, and each month
    is clipped to the untested day range before measuring contiguous runs.

    Returns per-dataset month counts and contiguous untouched runs with both the
    full 30/30/30 and the forward-reduced 60/7/3x10 feasibility flags.
    """
    present = {ds: bulk_months(ds) for ds in BULK_DATASETS}
    if not any(present.values()):
        return {"present": present, "runs": [], "any_feasible": False,
                "any_forward_feasible": False,
                "min_design_days": MIN_DESIGN_DAYS,
                "min_forward_design_days": MIN_FORWARD_DESIGN_DAYS}

    common = set(present.get("candles_1h", []))
    for ds in BULK_DATASETS:
        common &= set(present.get(ds, []))
    if not common:
        return {"present": present, "runs": [], "any_feasible": False,
                "any_forward_feasible": False,
                "min_design_days": MIN_DESIGN_DAYS,
                "min_forward_design_days": MIN_FORWARD_DESIGN_DAYS}

    # Expand covered months to a sorted set of UTC dates, then drop tested days.
    import datetime as _dt

    covered: set[_dt.date] = set()
    for m in common:
        y, mo = int(m[:4]), int(m[5:7])
        _, ndays = _month_days(m), None
        for d in range(1, _month_days(m) + 1):
            covered.add(_dt.date(y, mo, d))

    def _tested(day: _dt.date) -> bool:
        for a, b, _lbl in BULK_TESTED_WINDOWS:
            da = _dt.date.fromisoformat(a)
            db = _dt.date.fromisoformat(b)
            if da <= day <= db:
                return True
        return False

    usable = sorted(d for d in covered if not _tested(d))

    runs: list[dict] = []
    cur: list[_dt.date] = []
    for d in usable:
        if cur and (d - cur[-1]).days != 1:
            runs.append(cur)
            cur = []
        cur.append(d)
    if cur:
        runs.append(cur)

    out = []
    for run in runs:
        days = len(run)
        out.append({"start": run[0].isoformat(),
                    "end": run[-1].isoformat(),
                    "span_days": days,
                    "feasible": days >= MIN_DESIGN_DAYS,
                    "feasible_forward": days >= MIN_FORWARD_DESIGN_DAYS})
    return {"present": present, "runs": out,
            "any_feasible": any(r["feasible"] for r in out),
            "any_forward_feasible": any(r["feasible_forward"] for r in out),
            "min_design_days": MIN_DESIGN_DAYS,
            "min_forward_design_days": MIN_FORWARD_DESIGN_DAYS}


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
    disjoint = disjoint_block_frontier(windows)
    bulk = bulk_frontier()

    if args.json:
        print(json.dumps({"actionable_preregs": actionable,
                          "ready_funding_backed_months": ready,
                          "no_funding_months": partial,
                          "design_feasibility": feasibility,
                          "disjoint_block_frontier": disjoint,
                          "hyperliquid_bulk_frontier": bulk}, indent=1))
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
                  "need an empty/overlapping train. The Binance 5-symbol contiguous "
                  "design is exhausted; see the disjoint-block frontier below.")

    print("\n== DISJOINT 30-DAY BLOCK FRONTIER (independent, never-tested test months) ==")
    if not disjoint["blocks"]:
        print("  no ready disjoint funding-backed months -> no block candidates")
    else:
        for b in disjoint["blocks"]:
            tag = "FEASIBLE" if b["feasible"] else "INFEASIBLE"
            print(f"  {b['month']}  {tag:10s} train={b['train_start'][:10]}.."
                  f"{b['train_end'][:10]} test={b['test_start'][:10]}..{b['test_end'][:10]} "
                  f"test_days={b['test_days']}  {b['reason']}")
        if disjoint["campaign_feasible"]:
            print(f"\n  -> {disjoint['n_feasible']} disjoint 30-day test blocks fit "
                  f"(need >= {disjoint['min_blocks']}); executable heavy work REMAINS.")
        elif disjoint["any_feasible"]:
            print(f"\n  -> Only {disjoint['n_feasible']} feasible disjoint block(s); "
                  f"the campaign needs >= {disjoint['min_blocks']}.")
        else:
            print("\n  -> No disjoint 30-day block is feasible.")

    print("\n== HYPERLIQUID BULK FRONTIER (ironflow: candles + funding + OI + observed liq) ==")
    if not any(bulk["present"].values()):
        print("  bulk cache absent -> this domain contributes no frontier")
    else:
        for ds in BULK_DATASETS:
            print(f"  {ds:14s} months={len(bulk['present'].get(ds, []))}")
        runs = bulk["runs"]
        if not runs:
            print("  no untouched contiguous region -> Hyperliquid bulk frontier exhausted")
        else:
            for r in runs:
                if r["feasible"]:
                    tag = "FEASIBLE"
                elif r["feasible_forward"]:
                    tag = "FEASIBLE (forward-reduced: 60/7/3x10)"
                else:
                    tag = "TOO SHORT"
                print(f"  {r['start']}..{r['end']}  span={r['span_days']}d  "
                      f"(need >= {bulk['min_design_days']}d)  {tag}")
            if bulk["any_feasible"]:
                print("\n  -> An untouched Hyperliquid region fits a FEASIBLE 3-block design. "
                      "This is executable heavy work; do NOT close the campaign on the "
                      "Binance-only exhaustion.")
            elif bulk["any_forward_feasible"]:
                print("\n  -> An untouched Hyperliquid region fits a FEASIBLE forward-reduced "
                      "(60/7/3x10) design. Freeze that prereg and execute; do NOT close the "
                      "campaign on the Binance-only exhaustion.")
            else:
                print("\n  -> No untouched Hyperliquid region is long enough for a 3-block design.")

    if (not feasibility["any_feasible"] and not bulk["any_feasible"]
            and not bulk["any_forward_feasible"] and not disjoint["campaign_feasible"]):
        print("\n  == CAMPAIGN STATUS: no feasible 3-block design in ANY domain ==")
    else:
        print("\n  == CAMPAIGN STATUS: executable heavy work REMAINS (see FEASIBLE above) ==")

    print("\n== MONTHS WITH COMPLETE KLINES BUT NO FUNDING (baseline-only designs) ==")
    if partial:
        for w in partial:
            print(f"  {w['month']}  (funding starts 2024-04)")
    else:
        print("  none")


if __name__ == "__main__":
    main()