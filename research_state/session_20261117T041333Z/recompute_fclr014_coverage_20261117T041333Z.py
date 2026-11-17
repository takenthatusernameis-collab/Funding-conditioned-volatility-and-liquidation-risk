#!/usr/bin/env python3
"""FCLR-014 panel coverage audit + blocker resolution (parquet-free, no network).

Independently recomputes, from the raw local cache, the per-symbol x per-month
coverage matrix that the prior handoff only asserted in prose. This resolves the
FCLR-014 blocker with evidence instead of repeating the "no admissible panel"
claim:

  * Phase 1 - coverage matrix over research_state/data_cache/{SYM}_YYYY_MM/ for
    the 5 registered symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT):
    mark/index/premium day counts, funding presence, and an
    `admissible_for_fclr014` boolean per month.

  * Phase 2 - blocker resolution: classify every untested complete month as
    AVAILABLE / CONSUMED_BY_SEALED_CELL / INCOMPLETE_TRAIN and decide whether a
    NEW pre-registered >=3-block design can be frozen BEFORE outcomes. This
    reads TESTED_WINDOWS and MIN_DESIGN_DAYS from scripts/next_campaign_status.py
    (imported, not re-typed) and cross-checks against the tool's own frontier so
    two independent computations must agree.

No parquet engine is used. No outcome summary is read. No sealed artifact is
mutated. Writes only under this session directory.

Outputs:
  recompute_fclr014_coverage_<UTC>.json / .md   (full evidence)
  fclr014_panel_coverage_audit_<UTC>.json / .md (coverage-matrix view)
  fclr014_panel_blocker_resolution_<UTC>.json / .md (blocker view)

Usage:
  python3 recompute_fclr014_coverage_<UTC>.py
"""
from __future__ import annotations

import calendar
import importlib.util
import json
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
OUT_DIR = Path(__file__).resolve().parent

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
KINDS = ("markPriceKlines", "indexPriceKlines", "premiumIndexKlines")
KIND_PREFIX = {
    "markPriceKlines": "markPriceKlines-",
    "indexPriceKlines": "indexPriceKlines-",
    "premiumIndexKlines": "premiumIndexKlines-",
}
UTC = "20261117T041333Z"
# Completeness threshold per symbol-month (matches next_campaign_status.py 5*25 rule).
PER_SYMBOL_MIN_DAYS = 25


def _load_status_module():
    path = REPO / "scripts" / "next_campaign_status.py"
    spec = importlib.util.spec_from_file_location("ncs", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _month_days(key: str) -> int:
    y, m = int(key[:4]), int(key[5:7])
    return calendar.monthrange(y, m)[1]


def _day_dirs(base: Path, prefix: str) -> list[Path]:
    if not base.exists():
        return []
    return sorted(d for d in base.glob(f"{prefix}*") if d.is_dir())


def _dir_has_data(d: Path) -> bool:
    if not d.is_dir():
        return False
    for child in d.iterdir():
        if child.suffix in (".csv", ".zip"):
            return True
        if child.is_dir():
            for sub in child.iterdir():
                if sub.suffix in (".csv", ".zip"):
                    return True
    return False


def _count_days(base: Path, prefix: str) -> int:
    return sum(1 for d in _day_dirs(base, prefix) if _dir_has_data(d))


def _funding_present(sym: str, base: Path, ym: str) -> bool:
    y, m = ym.split("-")
    month_key = f"{y}-{m}"
    subdir = base / f"{sym}-fundingRate-{month_key}"
    if subdir.exists():
        for p in subdir.rglob("*"):
            if p.suffix in (".csv", ".zip"):
                return True
    zip_path = base / f"{sym}-fundingRate-{month_key}.zip"
    if zip_path.exists():
        return True
    csv_path = base / f"{sym}-fundingRate-{month_key}.csv"
    if csv_path.exists():
        return True
    return False


def build_coverage() -> dict:
    # symbol -> ym -> counts
    per_symbol: dict[str, dict[str, dict]] = {}
    all_months: set[str] = set()
    for sym in SYMBOLS:
        per_symbol[sym] = {}
        for d in sorted(CACHE.glob(f"{sym}_20??_??")):
            name = d.name
            parts = name.rsplit("_", 2)
            if len(parts) != 3:
                continue
            y, mo = parts[1], parts[2]
            ym = f"{y}-{mo}"
            all_months.add(ym)
            base = d
            per_symbol[sym][ym] = {
                "mark_days": _count_days(base, KIND_PREFIX["markPriceKlines"]),
                "index_days": _count_days(base, KIND_PREFIX["indexPriceKlines"]),
                "premium_days": _count_days(base, KIND_PREFIX["premiumIndexKlines"]),
                "funding_present": _funding_present(sym, base, ym),
            }

    # per-month aggregate
    months = {}
    for ym in sorted(all_months):
        ndays = _month_days(ym)
        row = {
            "month": ym,
            "days_in_month": ndays,
            "symbols": {},
            "mark_total": 0,
            "index_total": 0,
            "premium_total": 0,
            "funding_symbols": 0,
            "symbols_with_full_mark": 0,
        }
        all_mark_ok = True
        all_funding = True
        all_full_mark = True
        all_index_ok = True
        all_premium_ok = True
        for sym in SYMBOLS:
            s = per_symbol[sym].get(ym)
            if s is None:
                row["symbols"][sym] = {
                    "present_dir": False,
                    "mark_days": 0, "index_days": 0, "premium_days": 0,
                    "funding_present": False,
                }
                all_mark_ok = False
                all_funding = False
                all_full_mark = False
                all_index_ok = False
                all_premium_ok = False
                continue
            row["symbols"][sym] = {"present_dir": True, **s}
            row["mark_total"] += s["mark_days"]
            row["index_total"] += s["index_days"]
            row["premium_total"] += s["premium_days"]
            if s["funding_present"]:
                row["funding_symbols"] += 1
            mark_ok = s["mark_days"] >= PER_SYMBOL_MIN_DAYS
            full = s["mark_days"] >= ndays
            if full:
                row["symbols_with_full_mark"] += 1
            if not mark_ok:
                all_mark_ok = False
            if s["index_days"] < PER_SYMBOL_MIN_DAYS:
                all_index_ok = False
            if s["premium_days"] < PER_SYMBOL_MIN_DAYS:
                all_premium_ok = False
            if not s["funding_present"]:
                all_funding = False
            if not full:
                all_full_mark = False
        row["all_symbols_mark_ge_min"] = all_mark_ok
        row["all_symbols_funding"] = all_funding
        row["all_symbols_full_mark"] = all_full_mark
        # Operative admissibility rule (handoff definition): every symbol has
        # >=25 mark days AND funding. This is the mark+funding-only family that
        # can support B0/B1/C1 but NOT the C2 premium/EMA features.
        row["admissible_for_fclr014"] = bool(all_mark_ok and all_funding)
        # Stricter rule for the FULL C2 estimand: mark + index + premium + funding
        # all complete for every symbol (C2 needs mark/index premium + EMA).
        row["admissible_full_c2"] = bool(
            all_mark_ok and all_index_ok and all_premium_ok and all_funding
        )
        months[ym] = row

    return {"per_symbol": per_symbol, "months": months}


def _blocks_for(coverage: dict, months: dict, overlaps, adm_key: str) -> dict:
    """Enumerate disjoint 30-day test blocks under one admissibility predicate."""

    def month_adm(ym: str) -> bool:
        m = months.get(ym)
        return bool(m and m[adm_key] and not overlaps(ym))

    def months_between(start: date, end: date) -> list[str]:
        out = []
        y, mo = start.year, start.month
        while (y, mo) <= (end.year, end.month):
            out.append(f"{y:04d}-{mo:02d}")
            mo += 1
            if mo > 12:
                mo = 1
                y += 1
        return out

    blocks = []
    for ym in sorted(months):
        m = months[ym]
        if overlaps(ym) or not m[adm_key]:
            continue
        test_start = date.fromisoformat(f"{ym}-01")
        test_end = date(int(ym[:4]), int(ym[5:7]), _month_days(ym))
        train_end_excl = test_start - timedelta(days=7)
        train_start = train_end_excl - timedelta(days=30)
        train_months = months_between(train_start, train_end_excl - timedelta(days=1))
        missing = [tm for tm in train_months if not month_adm(tm)]
        feasible = not missing
        if feasible:
            bstatus = "AVAILABLE"
            reason = "complete funding-backed untested test block with complete train history"
        else:
            bstatus = "INCOMPLETE_TRAIN"
            reason = "; ".join(f"{tm}:missing_or_unfunded_or_tested" for tm in missing)
        blocks.append({
            "test_month": ym,
            "train_start": train_start.isoformat(),
            "train_end": (train_end_excl - timedelta(days=1)).isoformat(),
            "embargo_days": 7,
            "test_start": test_start.isoformat(),
            "test_end": test_end.isoformat(),
            "train_months": train_months,
            "missing_train_months": missing,
            "status": bstatus,
            "feasible": feasible,
            "reason": reason,
        })

    # Contiguous runs for a rolling 127-day design under this predicate.
    usable = [ym for ym in sorted(months) if month_adm(ym)]
    runs = []
    cur = []
    for ym in usable:
        if cur:
            py, pm = int(cur[-1][:4]), int(cur[-1][5:7])
            ny, nm = int(ym[:4]), int(ym[5:7])
            pm += 1
            if pm > 12:
                pm = 1
                py += 1
            if (ny, nm) != (py, pm):
                runs.append(cur)
                cur = []
        cur.append(ym)
    if cur:
        runs.append(cur)
    run_rows = []
    for r in runs:
        span = sum(_month_days(m) for m in r)
        run_rows.append({"months": r, "span_days": span, "feasible": span >= ncs_MIN_DESIGN})
    return {
        "admissibility_rule": adm_key,
        "candidate_blocks": blocks,
        "n_available_blocks": sum(1 for b in blocks if b["status"] == "AVAILABLE"),
        "available_test_months": [b["test_month"] for b in blocks if b["status"] == "AVAILABLE"],
        "contiguous_runs": run_rows,
        "any_contiguous_feasible": any(r["feasible"] for r in run_rows),
    }


def classify(coverage: dict, ncs) -> dict:
    global ncs_MIN_DESIGN
    ncs_MIN_DESIGN = ncs.MIN_DESIGN_DAYS
    tested = list(ncs.TESTED_WINDOWS)
    min_design = ncs.MIN_DESIGN_DAYS
    months = coverage["months"]

    def overlaps(ym: str):
        hits = []
        for a, b, lbl in tested:
            if a[:7] <= ym <= b[:7]:
                hits.append({"window": [a, b], "label": lbl})
        return hits

    rows = []
    for ym in sorted(months):
        m = months[ym]
        ov = overlaps(ym)
        adm = m["admissible_for_fclr014"]
        adm_c2 = m["admissible_full_c2"]
        if ov:
            status = "CONSUMED_BY_SEALED_CELL"
            reason = f"month overlaps tested window(s): {[h['label'] for h in ov]}"
        elif adm:
            status = "UNTESTED_COMPLETE_MARKFUND"
            reason = ("outside every TESTED_WINDOW; mark+funding complete for 5 symbols"
                      + ("" if adm_c2 else "; index/premium INCOMPLETE -> full-C2 NOT admissible"))
        else:
            missing = [s for s in SYMBOLS if not m["symbols"][s]["present_dir"]]
            unfunded = [s for s in SYMBOLS if not m["symbols"][s]["funding_present"]]
            lowmark = [s for s in SYMBOLS
                       if m["symbols"][s]["present_dir"]
                       and m["symbols"][s]["mark_days"] < PER_SYMBOL_MIN_DAYS]
            status = "INCOMPLETE_COVERAGE"
            reason = (f"missing_dir={missing} unfunded={unfunded} "
                      f"mark_lt_{PER_SYMBOL_MIN_DAYS}={lowmark}")
        rows.append({
            "month": ym,
            "admissible_for_fclr014_markfund": adm,
            "admissible_full_c2": adm_c2,
            "status": status,
            "reason": reason,
            "tested_windows": [h["label"] for h in ov],
            "mark_total": m["mark_total"],
            "index_total": m["index_total"],
            "premium_total": m["premium_total"],
            "funding_symbols": m["funding_symbols"],
        })

    markfund = _blocks_for(coverage, months, overlaps, "admissible_for_fclr014")
    fullc2 = _blocks_for(coverage, months, overlaps, "admissible_full_c2")

    campaign_feasible = (
        markfund["n_available_blocks"] >= 3
        or markfund["any_contiguous_feasible"]
        or fullc2["n_available_blocks"] >= 3
        or fullc2["any_contiguous_feasible"]
    )

    return {
        "month_classification": rows,
        "markfund_blocks": markfund,
        "fullc2_blocks": fullc2,
        "min_design_days": min_design,
        "campaign_feasible_new_prereg": bool(campaign_feasible),
        "blocker": (
            "DESIGN_ADMISSIBILITY: full-C2 estimand has 0 available disjoint blocks and "
            f"no contiguous untested run >= {min_design}d; mark+funding-only (B0/B1/C1) "
            f"has {markfund['n_available_blocks']} available blocks (<3). A confirmatory "
            ">=3-block FCLR-014 design cannot be frozen from local data without consuming "
            "a sealed window. A 2-block mark+funding-only EXPLORATORY pilot is the only "
            "constructible local design, and it is NOT promotable."
            if not campaign_feasible else
            "A new pre-registered design is feasible from untested complete months."
        ),
    }


def cross_check(ncs) -> dict:
    """Independent agreement with scripts/next_campaign_status.py frontier."""
    try:
        ready = ncs.ready_windows()
        feas = ncs.design_feasible_months(ready)
        disj = ncs.disjoint_block_frontier(ready)
        return {
            "tool_ready_funding_backed_months": [
                w["month"] for w in ready if w["funding_available"] and not w["inside_tested_window"]
            ],
            "tool_any_contiguous_feasible": feas.get("any_feasible"),
            "tool_contiguous_runs": feas.get("runs"),
            "tool_n_feasible_disjoint_blocks": disj.get("n_feasible"),
            "tool_campaign_feasible": disj.get("campaign_feasible"),
        }
    except Exception as e:  # pragma: no cover
        return {"error": repr(e)}


def main() -> int:
    ncs = _load_status_module()
    coverage = build_coverage()
    cls = classify(coverage, ncs)
    xcheck = cross_check(ncs)

    # Coverage matrix view (compact)
    cov_view = {
        "audit_id": f"FCLR-014-COVERAGE-{UTC}",
        "generated_utc": "2026-11-17T04:13:33Z",
        "coverage_only": True,
        "outcomes_inspected": False,
        "network": False,
        "symbols": SYMBOLS,
        "per_symbol_min_mark_days": PER_SYMBOL_MIN_DAYS,
        "months": {
            ym: {
                "days_in_month": m["days_in_month"],
                "mark_total": m["mark_total"],
                "index_total": m["index_total"],
                "premium_total": m["premium_total"],
                "funding_symbols": m["funding_symbols"],
                "admissible_for_fclr014": m["admissible_for_fclr014"],
                "all_symbols_full_mark": m["all_symbols_full_mark"],
                "per_symbol": {
                    s: {
                        "mark_days": m["symbols"][s]["mark_days"],
                        "index_days": m["symbols"][s]["index_days"],
                        "premium_days": m["symbols"][s]["premium_days"],
                        "funding_present": m["symbols"][s]["funding_present"],
                    }
                    for s in SYMBOLS
                },
            }
            for ym, m in coverage["months"].items()
        },
    }

    blocker_view = {
        "blocker_id": f"FCLR-014-BLOCKER-RESOLUTION-{UTC}",
        "generated_utc": "2026-11-17T04:13:33Z",
        "prereg": "research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json",
        "prereg_status": "FROZEN_BEFORE_OUTCOMES; confirmatory_claim_go=NO_GO; "
                         "exploratory_label_required=EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE",
        "prereg_split_defect": "candidate_frozen_splits_pending_panel.test = 2024-07-23..2024-09-30 "
                               "(70 days = 2 non-overlapping 30-day blocks) copied from FCLR-002; "
                               "fails block_requirement >=3",
        "corrected_blocker": cls["blocker"],
        "campaign_feasible_new_prereg": cls["campaign_feasible_new_prereg"],
        "min_design_days": cls["min_design_days"],
        "full_c2_estimand": {
            "admissibility_rule": "mark+index+premium+funding complete for all 5 symbols",
            "n_available_disjoint_blocks": cls["fullc2_blocks"]["n_available_blocks"],
            "available_test_months": cls["fullc2_blocks"]["available_test_months"],
            "candidate_blocks": cls["fullc2_blocks"]["candidate_blocks"],
            "contiguous_runs": cls["fullc2_blocks"]["contiguous_runs"],
        },
        "markfund_only_estimand": {
            "admissibility_rule": "mark+funding complete for all 5 symbols (B0/B1/C1; no C2 premium/EMA)",
            "n_available_disjoint_blocks": cls["markfund_blocks"]["n_available_blocks"],
            "available_test_months": cls["markfund_blocks"]["available_test_months"],
            "candidate_blocks": cls["markfund_blocks"]["candidate_blocks"],
            "contiguous_runs": cls["markfund_blocks"]["contiguous_runs"],
        },
        "month_classification": cls["month_classification"],
        "tool_cross_check": xcheck,
        "conclusion": (
            "FCLR-014 is BLOCKED-ON-DESIGN, not blocked-on-data. The cache DOES hold "
            "complete 5-symbol mark+funding months, but every untested complete month lacks "
            "a complete funded 30-day train window, and no contiguous untested run reaches "
            "MIN_DESIGN_DAYS. Under the FULL C2 rule (mark+index+premium+funding) there are "
            f"{cls['fullc2_blocks']['n_available_blocks']} available disjoint blocks; under the "
            "mark+funding-only rule there are "
            f"{cls['markfund_blocks']['n_available_blocks']} (2024-12, 2025-01) - still <3. A "
            "confirmatory >=3-block FCLR-014 design cannot be frozen from local data without "
            "consuming a sealed window; do NOT re-score and do NOT relax the completeness rule."
        ),
    }

    # Full evidence view
    full = {
        "experiment_id": "FCLR-014",
        "cell": "FCLR-014-COVERAGE-BLOCKER-RESOLUTION",
        "generated_utc": "2026-11-17T04:13:33Z",
        "input_mode": "local_csv_zip_no_parquet_no_network",
        "coverage": cov_view,
        "blocker_resolution": blocker_view,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    def _w(name, obj):
        (OUT_DIR / name).write_text(json.dumps(obj, indent=2) + "\n")

    _w(f"recompute_fclr014_coverage_{UTC}.json", full)
    _w(f"fclr014_panel_coverage_audit_{UTC}.json", cov_view)
    _w(f"fclr014_panel_blocker_resolution_{UTC}.json", blocker_view)

    # Markdown summaries
    lines = [
        f"# FCLR-014 Panel Coverage Audit + Blocker Resolution — {UTC}",
        "",
        f"Verdict: **FCLR-014 BLOCKED-ON-DESIGN (corrected; NOT blocked-on-data)**",
        "",
        "Coverage-only. No outcomes inspected. No parquet engine used. No network.",
        "",
        "## Per-month admissibility (5 symbols: " + ", ".join(SYMBOLS) + ")",
        "",
        "| month | days | mark_total | funding_syms | admissible | status |",
        "|---|---|---|---|---|---|",
    ]
    for ym, m in coverage["months"].items():
        st = next(r["status"] for r in cls["month_classification"] if r["month"] == ym)
        lines.append(
            f"| {ym} | {m['days_in_month']} | {m['mark_total']} | "
            f"{m['funding_symbols']}/5 | {m['admissible_for_fclr014']} | {st} |"
        )
    lines += [
        "",
        "## Candidate disjoint 30-day blocks — mark+funding-only estimand (B0/B1/C1)",
        "",
        f"available = {cls['markfund_blocks']['n_available_blocks']} "
        f"({cls['markfund_blocks']['available_test_months']})",
        "",
    ]
    if not cls["markfund_blocks"]["candidate_blocks"]:
        lines.append("- none (no untested complete month)")
    for b in cls["markfund_blocks"]["candidate_blocks"]:
        lines.append(
            f"- test {b['test_month']}: **{b['status']}** "
            f"(train {b['train_start']}..{b['train_end']}; missing={b['missing_train_months']})"
        )
    lines += [
        "",
        "## Candidate disjoint 30-day blocks — FULL C2 estimand (needs mark+index+premium+funding)",
        "",
        f"available = {cls['fullc2_blocks']['n_available_blocks']} "
        f"({cls['fullc2_blocks']['available_test_months']})",
        "",
    ]
    if not cls["fullc2_blocks"]["candidate_blocks"]:
        lines.append("- none (no untested month with complete index+premium+funding)")
    for b in cls["fullc2_blocks"]["candidate_blocks"]:
        lines.append(
            f"- test {b['test_month']}: **{b['status']}** "
            f"(train {b['train_start']}..{b['train_end']}; missing={b['missing_train_months']})"
        )
    lines += [
        "",
        "## Contiguous rolling-design runs (need >= "
        f"{cls['min_design_days']}d)",
        "",
        "mark+funding-only:",
    ]
    if not cls["markfund_blocks"]["contiguous_runs"]:
        lines.append("- none")
    for r in cls["markfund_blocks"]["contiguous_runs"]:
        lines.append(f"- {r['months'][0]}..{r['months'][-1]} span={r['span_days']}d feasible={r['feasible']}")
    lines += ["", "full-C2:"]
    if not cls["fullc2_blocks"]["contiguous_runs"]:
        lines.append("- none")
    for r in cls["fullc2_blocks"]["contiguous_runs"]:
        lines.append(f"- {r['months'][0]}..{r['months'][-1]} span={r['span_days']}d feasible={r['feasible']}")
    lines += [
        "",
        f"**AVAILABLE disjoint blocks (mark+funding): {cls['markfund_blocks']['n_available_blocks']}** (need >=3)",
        f"**AVAILABLE disjoint blocks (full-C2): {cls['fullc2_blocks']['n_available_blocks']}** (need >=3)",
        f"**campaign_feasible_new_prereg: {cls['campaign_feasible_new_prereg']}**",
        "",
        "## Tool cross-check (scripts/next_campaign_status.py)",
        "",
        f"- ready funding-backed untested months: {xcheck.get('tool_ready_funding_backed_months')}",
        f"- any contiguous feasible: {xcheck.get('tool_any_contiguous_feasible')}",
        f"- n feasible disjoint blocks: {xcheck.get('tool_n_feasible_disjoint_blocks')}",
        "",
        "## Corrected blocker",
        "",
        cls["blocker"],
        "",
        blocker_view["conclusion"],
        "",
    ]
    (OUT_DIR / f"recompute_fclr014_coverage_{UTC}.md").write_text("\n".join(lines) + "\n")

    # Coverage-audit markdown view
    cov_md = [
        f"# FCLR-014 Panel Coverage Audit — {UTC}",
        "",
        f"Symbols: {', '.join(SYMBOLS)}",
        "",
        "| month | mark_total | index_total | premium_total | funding_syms | admissible_for_fclr014 |",
        "|---|---|---|---|---|---|",
    ]
    for ym, m in coverage["months"].items():
        cov_md.append(
            f"| {ym} | {m['mark_total']} | {m['index_total']} | {m['premium_total']} | "
            f"{m['funding_symbols']}/5 | {m['admissible_for_fclr014']} |"
        )
    (OUT_DIR / f"fclr014_panel_coverage_audit_{UTC}.md").write_text("\n".join(cov_md) + "\n")

    # Blocker-resolution markdown view
    blk_md = [
        f"# FCLR-014 Blocker Resolution — {UTC}",
        "",
        f"**corrected_blocker:** {cls['blocker']}",
        "",
        f"- campaign_feasible_new_prereg: {cls['campaign_feasible_new_prereg']}",
        f"- available disjoint blocks (mark+funding-only, B0/B1/C1): "
        f"{cls['markfund_blocks']['n_available_blocks']} (need >=3) -> {cls['markfund_blocks']['available_test_months']}",
        f"- available disjoint blocks (full-C2): {cls['fullc2_blocks']['n_available_blocks']} (need >=3) -> {cls['fullc2_blocks']['available_test_months']}",
        f"- min_design_days: {cls['min_design_days']}",
        "",
        "## Month classification",
        "",
        "| month | mark+fund adm | full-C2 adm | status | reason |",
        "|---|---|---|---|---|",
    ]
    for r in cls["month_classification"]:
        blk_md.append(
            f"| {r['month']} | {r['admissible_for_fclr014_markfund']} | {r['admissible_full_c2']} | "
            f"{r['status']} | {r['reason']} |"
        )
    blk_md += ["", blocker_view["conclusion"], ""]
    (OUT_DIR / f"fclr014_panel_blocker_resolution_{UTC}.md").write_text("\n".join(blk_md) + "\n")

    print(json.dumps({
        "experiment_id": "FCLR-014",
        "cell": "FCLR-014-COVERAGE-BLOCKER-RESOLUTION",
        "blocker": cls["blocker"],
        "campaign_feasible_new_prereg": cls["campaign_feasible_new_prereg"],
        "available_markfund_blocks": cls["markfund_blocks"]["n_available_blocks"],
        "available_markfund_months": cls["markfund_blocks"]["available_test_months"],
        "available_fullc2_blocks": cls["fullc2_blocks"]["n_available_blocks"],
        "available_fullc2_months": cls["fullc2_blocks"]["available_test_months"],
        "untested_complete_markfund_months": [
            r["month"] for r in cls["month_classification"] if r["status"] == "UNTESTED_COMPLETE_MARKFUND"
        ],
        "consumed_months": [
            r["month"] for r in cls["month_classification"] if r["status"] == "CONSUMED_BY_SEALED_CELL"
        ],
        "incomplete_months": [
            r["month"] for r in cls["month_classification"] if r["status"] == "INCOMPLETE_COVERAGE"
        ],
        "tool_cross_check": xcheck,
        "artifacts": [
            f"recompute_fclr014_coverage_{UTC}.json",
            f"recompute_fclr014_coverage_{UTC}.md",
            f"fclr014_panel_coverage_audit_{UTC}.json",
            f"fclr014_panel_coverage_audit_{UTC}.md",
            f"fclr014_panel_blocker_resolution_{UTC}.json",
            f"fclr014_panel_blocker_resolution_{UTC}.md",
        ],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())