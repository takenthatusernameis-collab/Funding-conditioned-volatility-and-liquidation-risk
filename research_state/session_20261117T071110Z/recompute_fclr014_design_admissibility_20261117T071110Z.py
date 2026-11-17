#!/usr/bin/env python3
"""FCLR-014 design-admissibility adjudication (session-local, stdlib only).

Purpose
-------
Resolve the conflicting FCLR-014 blocker resolutions left by earlier sessions
(``session_20261117T041333Z`` and ``session_20261117T051045Z``) against the
canonical campaign tool ``scripts/next_campaign_status.py``.

The conflict
------------
* Canonical tool (FULL C2 rule: mark+index+premium+funding) -> 0 feasible
  disjoint blocks, no contiguous untested run >= 127d -> BLOCKED-ON-DESIGN.
* 041333Z (as corrected 2026-11-17T06:08:53Z) and 051045Z -> mark+funding-only
  (B0/B1/C1) has 4 *individually* feasible test months (2024-10, 2024-11,
  2024-12, 2025-01) -> claims a new prereg CAN be frozen.

Root cause of the conflict
--------------------------
The "4 blocks" count treats each month independently and never checks that the
30-day train + 7-day embargo + 30-day test windows of the selected blocks are
*mutually non-overlapping*.  A confirmatory design requires non-overlapping
blocks precisely to avoid cross-block leakage.  When the non-overlap
constraint is enforced, the maximum number of mutually non-overlapping
mark+funding-only blocks is 2 (< 3 required) -> still BLOCKED-ON-DESIGN.

This script recomputes both quantities deterministically and emits the
adjudication.  No network, no parquet, no sealed-artifact mutation, read-only.
"""
from __future__ import annotations

import argparse
import calendar
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
SESSION = Path(__file__).resolve().parent
TS = SESSION.name[len("session_"):] if SESSION.name.startswith("session_") else SESSION.name

# 31 months with complete mark+funding for all 5 symbols (coverage audit,
# session_20261117T051045Z / fclr014_panel_coverage_audit). 2024-01..03 lack
# funding; 2026-11 is partial (8 days, no funding).
MARKFUND_MONTHS = [
    "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09",
    "2024-10", "2024-11", "2024-12",
    "2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
    "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12",
    "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06",
    "2026-07", "2026-08", "2026-09", "2026-10",
]

# Month-granularity union of TESTED_WINDOWS in scripts/next_campaign_status.py.
TESTED_MONTHS = {
    "2024-06", "2024-07", "2024-08", "2024-09",
    "2025-02", "2025-03", "2025-04", "2025-05", "2025-06", "2025-07",
    "2025-08", "2025-09", "2025-10", "2025-11", "2025-12",
    "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06",
    "2026-07", "2026-08", "2026-09", "2026-10",
}

TRAIN_DAYS = 30
EMBARGO_DAYS = 7
MIN_BLOCKS = 3
MIN_DESIGN_DAYS = TRAIN_DAYS + EMBARGO_DAYS + MIN_BLOCKS * 30  # 127

MARKFUND = set(MARKFUND_MONTHS)


def month_first_last(key: str) -> tuple[dt.date, dt.date]:
    y, m = int(key[:4]), int(key[5:7])
    first = dt.date(y, m, 1)
    last = dt.date(y, m, calendar.monthrange(y, m)[1])
    return first, last


def months_touched(start: dt.date, end: dt.date) -> list[str]:
    out = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out


def run_canonical_tool() -> dict:
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "next_campaign_status.py"), "--json"],
        cwd=str(REPO), capture_output=True, text=True, timeout=300,
    )
    if proc.returncode != 0:
        return {"error": proc.stderr[-800:], "returncode": proc.returncode}
    return json.loads(proc.stdout)


def compute_markfund_blocks() -> dict:
    candidates = []
    for key in sorted(MARKFUND):
        if key in TESTED_MONTHS:
            continue  # consumed by a sealed cell
        test_start, test_end = month_first_last(key)
        train_end = test_start - dt.timedelta(days=EMBARGO_DAYS)
        train_start = train_end - dt.timedelta(days=TRAIN_DAYS)
        train_months = months_touched(train_start, train_end)
        incomplete = [m for m in train_months if m not in MARKFUND]
        individually_feasible = not incomplete
        candidates.append({
            "test_month": key,
            "train_start": train_start.isoformat(),
            "train_end": train_end.isoformat(),
            "embargo_days": EMBARGO_DAYS,
            "test_start": test_start.isoformat(),
            "test_end": test_end.isoformat(),
            "train_months": train_months,
            "incomplete_train_months": incomplete,
            "individually_feasible": individually_feasible,
        })

    feasible = [c for c in candidates if c["individually_feasible"]]
    feasible.sort(key=lambda c: c["train_start"])

    # Greedy maximum set of mutually non-overlapping blocks (by train_start).
    selected: list[dict] = []
    last_test_end: dt.date | None = None
    for c in feasible:
        ts = dt.date.fromisoformat(c["train_start"])
        if last_test_end is None or ts > last_test_end:
            selected.append(c)
            last_test_end = dt.date.fromisoformat(c["test_end"])

    # Overlap audit: for every pair of individually-feasible blocks, do their
    # [train_start, test_end] windows intersect?
    overlaps = []
    for i in range(len(feasible)):
        for j in range(i + 1, len(feasible)):
            a, b = feasible[i], feasible[j]
            a0, a1 = dt.date.fromisoformat(a["train_start"]), dt.date.fromisoformat(a["test_end"])
            b0, b1 = dt.date.fromisoformat(b["train_start"]), dt.date.fromisoformat(b["test_end"])
            if a0 <= b1 and b0 <= a1:
                overlaps.append({
                    "block_a": a["test_month"], "block_b": b["test_month"],
                    "overlap_window": [
                        max(a0, b0).isoformat(), min(a1, b1).isoformat()
                    ],
                })

    return {
        "candidate_test_months": candidates,
        "n_individually_feasible": len(feasible),
        "individually_feasible_months": [c["test_month"] for c in feasible],
        "max_mutually_non_overlapping": len(selected),
        "non_overlapping_selection": [c["test_month"] for c in selected],
        "n_overlapping_pairs": len(overlaps),
        "overlapping_pairs": overlaps,
        "min_blocks_required": MIN_BLOCKS,
        "markfund_only_campaign_feasible": len(selected) >= MIN_BLOCKS,
        "min_design_days": MIN_DESIGN_DAYS,
    }


def load_prior_claim(path: Path) -> dict:
    if not path.exists():
        return {"present": False, "path": str(path)}
    try:
        d = json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001
        return {"present": True, "path": str(path), "parse_error": str(exc)}
    return {
        "present": True,
        "path": str(path),
        "campaign_feasible_new_prereg": d.get("campaign_feasible_new_prereg"),
        "n_available_disjoint_blocks_markfund": d.get("n_available_disjoint_blocks_markfund"),
        "corrected_blocker": d.get("corrected_blocker"),
        "overall_verdict": d.get("overall_verdict"),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    canonical = run_canonical_tool()
    markfund = compute_markfund_blocks()

    canonical_feasible = False
    canonical_detail = {}
    if "error" not in canonical:
        df = canonical.get("design_feasibility", {})
        db = canonical.get("disjoint_block_frontier", {})
        canonical_feasible = bool(df.get("any_feasible")) or bool(db.get("campaign_feasible"))
        canonical_detail = {
            "design_feasibility_any_feasible": df.get("any_feasible"),
            "design_runs": df.get("runs"),
            "disjoint_n_feasible": db.get("n_feasible"),
            "disjoint_campaign_feasible": db.get("campaign_feasible"),
            "disjoint_blocks": [
                {"month": b["month"], "feasible": b["feasible"], "reason": b["reason"]}
                for b in db.get("blocks", [])
            ],
        }
    else:
        canonical_detail = {"error": canonical.get("error")}

    prior_041333Z = load_prior_claim(
        RS / "session_20261117T041333Z" / "fclr014_panel_blocker_resolution_20261117T041333Z.json")
    prior_051045Z = load_prior_claim(
        RS / "session_20261117T051045Z" / "fclr014_panel_blocker_resolution_20261117T051045Z.json")

    blocked = (not canonical_feasible) and (not markfund["markfund_only_campaign_feasible"])
    verdict = "BLOCKED_ON_DESIGN" if blocked else "NEW_PRERG_FREEZABLE"

    result = {
        "artifact_id": f"FCLR-014-DESIGN-ADMISSIBILITY-{TS}",
        "generated_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "question": (
            "Can a >=3-block confirmatory FCLR-014 design be frozen from local "
            "cached data before outcome inspection?"
        ),
        "canonical_tool": "scripts/next_campaign_status.py --json",
        "canonical_tool_path": canonical_detail,
        "canonical_full_c2_feasible": canonical_feasible,
        "markfund_only_analysis": markfund,
        "prior_session_claims": {
            "session_20261117T041333Z": prior_041333Z,
            "session_20261117T051045Z": prior_051045Z,
        },
        "conflict_resolution": {
            "discrepancy": (
                "041333Z (corrected JSON) and 051045Z count 4 mark+funding-only "
                "blocks and claim a prereg is freezable; the canonical full-C2 "
                "tool reports 0 feasible blocks / no >=127d run."
            ),
            "root_cause": (
                "The 4-block count treats each month independently and omits the "
                "mutual non-overlap constraint across blocks.  A 30d train + 7d "
                "embargo + 30d test window spans ~2.2 months, so consecutive "
                "candidate months (2024-10/11/12, 2025-01) have train windows "
                "that overlap a neighbouring block's test month, i.e. cross-block "
                "leakage.  Enforcing non-overlap leaves at most 2 blocks."
            ),
            "retraction": (
                "RETRACTED: the claim 'campaign_feasible_new_prereg=true / freeze "
                "a NEW mark+funding-only prereg using 2024-10, 2024-11, 2024-12' "
                "(session_20261117T051045Z and the corrected 041333Z JSON) is "
                "UNSAFE for a confirmatory claim: it uses mutually overlapping "
                "blocks.  It is valid only as an EXPLORATORY / NOT-CONFIRMATORY / "
                "NOT-PROMOTABLE 2-block pilot."
            ),
        },
        "verdict": verdict,
        "verdict_detail": (
            "FCLR-014 is BLOCKED-ON-DESIGN.  Under the registered full-C2 rule "
            "(mark+index+premium+funding) the canonical tool finds 0 feasible "
            "disjoint blocks and no contiguous untested run >=127d.  Under a "
            "mark+funding-only rule (a materially different estimand requiring a "
            "new prereg) only 2 mutually non-overlapping blocks exist (<3).  "
            "Therefore no >=3-block confirmatory design can be frozen from local "
            "data without consuming a sealed window.  Do NOT freeze a prereg on "
            "the retracted 4-block claim; do NOT re-score sealed results."
        ),
        "permits_new_prereg": False,
    }

    out_json = SESSION / f"recompute_fclr014_design_admissibility_{TS}.json"
    out_md = SESSION / f"recompute_fclr014_design_admissibility_{TS}.md"
    out_json.write_text(json.dumps(result, indent=2, sort_keys=True))

    lines = []
    lines.append(f"# FCLR-014 Design-Admissibility Adjudication — {result['generated_utc']}")
    lines.append("")
    lines.append(f"**Verdict: `{verdict}`**")
    lines.append("")
    lines.append("## Question")
    lines.append(result["question"])
    lines.append("")
    lines.append("## Canonical tool (full-C2: mark+index+premium+funding)")
    lines.append(f"- `design_feasibility.any_feasible`: {canonical_detail.get('design_feasibility_any_feasible')}")
    for r in canonical_detail.get("design_runs", []) or []:
        lines.append(f"  - run {r['months']} span={r['span_days']}d feasible={r['feasible']}")
    lines.append(f"- `disjoint_block_frontier.n_feasible`: {canonical_detail.get('disjoint_n_feasible')} (need >= {MIN_BLOCKS})")
    lines.append(f"- `disjoint_block_frontier.campaign_feasible`: {canonical_detail.get('disjoint_campaign_feasible')}")
    for b in canonical_detail.get("disjoint_blocks", []) or []:
        lines.append(f"  - {b['month']}: feasible={b['feasible']} reason={b['reason']}")
    lines.append("")
    lines.append("## Mark+funding-only rule (B0/B1/C1, materially different estimand)")
    lines.append(f"- candidate untested mark+fund months: {[c['test_month'] for c in markfund['candidate_test_months']]}")
    lines.append(f"- individually feasible: {markfund['n_individually_feasible']} -> {markfund['individually_feasible_months']}")
    lines.append(f"- **mutually non-overlapping maximum: {markfund['max_mutually_non_overlapping']} -> {markfund['non_overlapping_selection']} (need >= {MIN_BLOCKS})**")
    lines.append(f"- overlapping pairs among individually-feasible blocks: {markfund['n_overlapping_pairs']}")
    for o in markfund["overlapping_pairs"]:
        lines.append(f"  - {o['block_a']} vs {o['block_b']} overlap {o['overlap_window']}")
    lines.append("")
    lines.append("## Conflict resolution")
    lines.append(f"- discrepancy: {result['conflict_resolution']['discrepancy']}")
    lines.append(f"- root cause: {result['conflict_resolution']['root_cause']}")
    lines.append(f"- retraction: {result['conflict_resolution']['retraction']}")
    lines.append("")
    lines.append("## Verdict detail")
    lines.append(result["verdict_detail"])
    lines.append("")
    lines.append("## Prior-session claims (recorded, adjudicated)")
    lines.append(f"- session_20261117T041333Z: campaign_feasible_new_prereg={prior_041333Z.get('campaign_feasible_new_prereg')} n_blocks={prior_041333Z.get('n_available_disjoint_blocks_markfund')}")
    lines.append(f"- session_20261117T051045Z: overall_verdict={prior_051045Z.get('overall_verdict')}")
    out_md.write_text("\n".join(lines) + "\n")

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"[{verdict}] canonical_full_c2_feasible={canonical_feasible} "
              f"markfund_individually={markfund['n_individually_feasible']} "
              f"markfund_non_overlapping={markfund['max_mutually_non_overlapping']} "
              f"need_blocks={MIN_BLOCKS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())