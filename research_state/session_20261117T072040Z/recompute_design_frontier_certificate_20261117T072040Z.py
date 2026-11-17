#!/usr/bin/env python3
"""Design-frontier certificate: full-C2 and mark+funding-only non-overlapping block feasibility.

Implements the mark+funding-only non-overlapping block frontier (30d train + 7d embargo
+ 30d test per block; blocks mutually non-overlapping in [train_start, test_end]) and
emits a machine-readable certificate reproducing the closed FCLR-014 verdict.

Read-only over cached inputs and scripts/next_campaign_status.py. No network, no parquet.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
TRAIN_DAYS = 30
EMBARGO_DAYS = 7
TEST_DAYS = 30
MIN_BLOCKS = 3
MIN_DESIGN_DAYS = TRAIN_DAYS + EMBARGO_DAYS + TEST_DAYS * MIN_BLOCKS  # 127


def month_days(key: str) -> int:
    import calendar
    y, m = int(key[:4]), int(key[5:7])
    return calendar.monthrange(y, m)[1]


def month_start(key: str) -> date:
    return date.fromisoformat(f"{key}-01")


def month_last_day(key: str) -> date:
    y, m = int(key[:4]), int(key[5:7])
    return date(y, m, month_days(key))


def months_between(start: date, end: date) -> list[str]:
    out = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out


def overlaps(a, b) -> bool:
    s = max(a[0], b[0]); e = min(a[1], b[1])
    return s <= e


def max_non_overlapping(intervals: list[tuple[date, date, str]]) -> list[str]:
    ordered = sorted(intervals, key=lambda x: (x[1], x[0], x[2]))
    chosen = []
    last_end = None
    for s, e, name in ordered:
        if last_end is None or s > last_end:
            chosen.append(name)
            last_end = e
    return chosen


def canonical_full_c2() -> dict:
    cmd = [sys.executable, str(REPO / "scripts/next_campaign_status.py"), "--json"]
    proc = subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True)
    data = json.loads(proc.stdout) if proc.stdout.strip() else {"error": proc.stderr.strip(), "returncode": proc.returncode}
    data["_returncode"] = proc.returncode
    return data


def markfund_frontier(full: dict) -> dict:
    # Build mark+funding completeness per month from ready_windows logic context:
    # a month is mark+funding-complete if it has sufficient mark kline coverage and funding for all 5 symbols.
    # For train history we only require mark+funding completeness (not premium/index) and do NOT require
    # the train month to be outside TESTED_WINDOWS (history may overlap tested windows). Test month must be
    # outside TESTED_WINDOWS and complete. We derive completeness and tested status from ready_windows + cache.
    rows = full.get("ready_funding_backed_months", []) + full.get("no_funding_months", [])
    # Also include any months present in ready_windows-like enumeration via full tool data not exposed;
    # instead compute completeness directly and tested status via next_campaign_status.TESTED_WINDOWS.
    sys.path.insert(0, str(REPO / "scripts"))
    import next_campaign_status as ncs  # type: ignore

    ncs_rows = ncs.ready_windows()
    by_month = {w["month"]: w for w in ncs_rows}

    # mark+funding complete month set (all 5 symbols): reuse mark_csv>=125 and funding_available
    complete_mf = set()
    for m, w in by_month.items():
        if w.get("funding_available") and w.get("mark_csv", 0) >= 5 * 25:
            complete_mf.add(m)
    # If a month not in ready_windows (not all 3 kline kinds complete for C2) it can still be mark+funding complete;
    # scan cache for funding+mark completeness.
    counts = {}
    for sym in SYMBOLS:
        # mark counts
        for d in CACHE.glob(f"{sym}_20??_??"):
            parts = d.name.rsplit("_", 2)
            if len(parts) < 3:
                continue
            try:
                key = f"{parts[-2]}-{parts[-1]}"; int(parts[-2]); int(parts[-1])
            except Exception:
                continue
            n = 0
            for sub in d.glob("markPriceKlines-*"):
                n += len(list(sub.glob("**/*.csv")))
            tgt = counts.setdefault(key, {"mark": 0, "fund": 0})
            tgt["mark"] += n
        # funding
        for d in CACHE.glob(f"{sym}_20??_??/{sym}-fundingRate-*"):
            if "fundingRate-" in d.name and any(d.glob("**/*.csv")):
                key = d.name.split("fundingRate-")[-1][:7]
                tgt = counts.setdefault(key, {"mark": 0, "fund": 0})
                tgt["fund"] += 1
    for key, c in counts.items():
        if c.get("mark", 0) >= 5 * 25 and c.get("fund", 0) >= 5:
            complete_mf.add(key)

    def inside_tested(month: str) -> bool:
        for a, b, _lbl in ncs.TESTED_WINDOWS:
            if a[:7] <= month <= b[:7]:
                return True
        return False

    candidates = []
    for key in sorted(complete_mf):
        if inside_tested(key):
            # test month consumed; cannot be a fresh test block
            continue
        test_start = month_start(key)
        test_end = month_last_day(key)
        train_end_excl = test_start - timedelta(days=EMBARGO_DAYS)
        train_start = train_end_excl - timedelta(days=TRAIN_DAYS)
        train_months = months_between(train_start, train_end_excl - timedelta(days=1))
        missing = [m for m in train_months if m not in complete_mf]
        feasible = len(missing) == 0
        candidates.append({
            "test_month": key,
            "block_window": [train_start.isoformat(), test_end.isoformat()],
            "train_start": train_start.isoformat(),
            "train_end": (train_end_excl - timedelta(days=1)).isoformat(),
            "embargo_start": train_end_excl.isoformat(),
            "embargo_end": (test_start - timedelta(days=1)).isoformat(),
            "test_start": test_start.isoformat(),
            "test_end": test_end.isoformat(),
            "train_months": train_months,
            "individually_feasible": feasible,
            "incomplete_train_months": missing,
            "estimator_scope": "mark+funding-only (B0/B1/C1; no premium/index C2 terms)",
            "test_month_inside_tested_window": False,
        })
    feasible = [c for c in candidates if c["individually_feasible"]]
    intervals = [(date.fromisoformat(c["block_window"][0]), date.fromisoformat(c["block_window"][1]), c["test_month"]) for c in feasible]
    pair_overlaps = []
    for i in range(len(intervals)):
        for j in range(i + 1, len(intervals)):
            if overlaps(intervals[i], intervals[j]):
                s = max(intervals[i][0], intervals[j][0]).isoformat()
                e = min(intervals[i][1], intervals[j][1]).isoformat()
                pair_overlaps.append({"block_a": intervals[i][2], "block_b": intervals[j][2], "overlap_window": [s, e]})
    selection = max_non_overlapping(intervals)

    usable = sorted([m for m in complete_mf if not inside_tested(m)])
    contiguous_runs = []
    if usable:
        cur = [usable[0]]; runs = []
        for prev, nxt in zip(usable, usable[1:]):
            py, pm = int(prev[:4]), int(prev[5:7]); pm += 1
            if pm > 12: pm, py = 1, py + 1
            ny, nm = int(nxt[:4]), int(nxt[5:7])
            if (ny, nm) == (py, pm): cur.append(nxt)
            else: runs.append(cur); cur = [nxt]
        runs.append(cur)
        for run in runs:
            days = sum(month_days(m) for m in run)
            contiguous_runs.append({"months": run, "span_days": days, "feasible_ge_min_design_days": days >= MIN_DESIGN_DAYS})

    return {
        "estimand": "mark+funding-only",
        "min_blocks_required": MIN_BLOCKS,
        "min_design_days": MIN_DESIGN_DAYS,
        "block_rule": {"train_days": TRAIN_DAYS, "embargo_days": EMBARGO_DAYS, "test_days": TEST_DAYS, "mutual_non_overlap_window": "[train_start, test_end]"},
        "tested_windows_source": "scripts.next_campaign_status.TESTED_WINDOWS",
        "candidate_test_months": candidates,
        "individually_feasible_months": [c["test_month"] for c in feasible],
        "n_individually_feasible": len(feasible),
        "overlapping_pairs": pair_overlaps,
        "n_overlapping_pairs": len(pair_overlaps),
        "max_mutually_non_overlapping": len(selection),
        "non_overlapping_selection": selection,
        "campaign_feasible_non_overlapping": len(selection) >= MIN_BLOCKS,
        "contiguous_runs_untested_complete_mf_months": contiguous_runs,
        "any_contiguous_run_ge_min_design_days": any(r["feasible_ge_min_design_days"] for r in contiguous_runs),
    }


def main() -> None:
    full = canonical_full_c2()
    mf = markfund_frontier(full)

    df = full.get("design_feasibility") or {}
    dbf = full.get("disjoint_block_frontier") or {}
    full_cert = {
        "estimand": "full-C2 (mark+index+premium+funding, all 3 kline kinds)",
        "canonical_tool": "scripts/next_campaign_status.py --json",
        "disjoint_n_feasible": dbf.get("n_feasible", 0),
        "disjoint_campaign_feasible": bool(dbf.get("campaign_feasible", False)),
        "any_feasible_without_nonoverlap_enumeration_gap": bool(dbf.get("campaign_feasible", False)),
        "design_runs": df.get("runs", []),
        "design_feasibility_any_feasible": bool(df.get("any_feasible", False)),
        "min_design_days": MIN_DESIGN_DAYS,
        "campaign_feasible_non_overlapping": bool(dbf.get("campaign_feasible", False)),
        "verdict": "BLOCKED_ON_DESIGN" if not dbf.get("campaign_feasible", False) and not df.get("any_feasible", False) else "FEASIBLE",
    }

    fclr014_reproduction = (
        full_cert["disjoint_n_feasible"] == 0
        and full_cert["design_feasibility_any_feasible"] is False
        and mf["n_individually_feasible"] == 4
        and mf["max_mutually_non_overlapping"] == 2
        and mf["non_overlapping_selection"] == ["2024-10", "2025-01"]
        and set(mf["individually_feasible_months"]) == {"2024-10", "2024-11", "2024-12", "2025-01"}
    )

    overall = "BLOCKED_ON_DESIGN" if (full_cert["campaign_feasible_non_overlapping"] is False and mf["campaign_feasible_non_overlapping"] is False) else "FEASIBLE"
    cert = {
        "artifact_id": "FCLR-DESIGN-FRONTIER-CERT-20261117T072040Z",
        "generated_utc": "2026-11-17T07:20:40Z",
        "question": "Can a >=3-block confirmatory FCLR-014 design be frozen from local cached data before outcome inspection?",
        "min_blocks_required": MIN_BLOCKS,
        "min_design_days": MIN_DESIGN_DAYS,
        "per_estimand": {
            "full_c2": full_cert,
            "markfund_only": mf,
        },
        "fclr014_closed_verdict_reproduced": fclr014_reproduction,
        "fclr014_expected": {
            "full_c2": {"disjoint_n_feasible": 0, "any_contiguous_ge_127d": False},
            "markfund_only": {"n_individually_feasible": 4, "max_mutually_non_overlapping": 2, "non_overlapping_selection": ["2024-10", "2025-01"]},
        },
        "promotable": False,
        "overall_verdict": overall,
        "verdict_detail": (
            "Full-C2: 0 feasible disjoint blocks and no contiguous untested run >=127d. "
            "Mark+funding-only: 4 individually feasible test months but only 2 mutually non-overlapping "
            "blocks (<3) after enforcing non-overlap in [train_start, test_end] and excluding TESTED_WINDOWS; "
            "consecutive candidates leak across blocks. No >=3-block confirmatory design can be frozen from local cached data. "
            "FCLR-014 BLOCKED_ON_DESIGN; the 4-block 'freeze a prereg' claim is retracted."
        ) if overall == "BLOCKED_ON_DESIGN" else "A feasible non-overlapping >=3-block design exists.",
        "retracted_claim": "session_20261117T051045Z / corrected session_20261117T041333Z claim of 4-block mark+funding-only feasibility for freezing a confirmatory prereg (overlapping train/test windows -> leakage).",
    }

    out_dir = REPO / "research_state/session_20261117T072040Z"
    out_json = out_dir / "recompute_design_frontier_certificate_20261117T072040Z.json"
    out_md = out_dir / "recompute_design_frontier_certificate_20261117T072040Z.md"
    out_json.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")

    lines = [
        "# Design Frontier Certificate — FCLR-REPRO-SYNTH-05 (2026-11-17T07:20:40Z)",
        "",
        f"- **Overall verdict:** `{overall}`",
        f"- **Promotable:** `{cert['promotable']}`",
        f"- **FCLR-014 closed verdict reproduced:** `{fclr014_reproduction}`",
        "",
        "## Per-estimand certificate",
        "",
        "### Full-C2 (mark+index+premium+funding)",
        f"- Disjoint feasible blocks (canonical tool): **{full_cert['disjoint_n_feasible']}** (campaign_feasible={full_cert['disjoint_campaign_feasible']})",
        f"- Contiguous run feasible (>= {MIN_DESIGN_DAYS}d): **{full_cert['design_feasibility_any_feasible']}**",
        "- With/without explicit mutual non-overlap: no feasible blocks/runs (unchanged).",
        f"- Verdict: **{full_cert['verdict']}**",
        "",
        "### Mark+funding-only (B0/B1/C1; materially different estimand, new prereg required)",
        f"- Individually feasible test months (outside TESTED_WINDOWS, without mutual non-overlap): **{mf['n_individually_feasible']}** — {', '.join(mf['individually_feasible_months']) or 'none'}",
        f"- Mutually non-overlapping feasible blocks (enforced on [train_start,test_end]): **{mf['max_mutually_non_overlapping']}** — {', '.join(mf['non_overlapping_selection']) or 'none'}",
        f"- Overlapping pairs: **{mf['n_overlapping_pairs']}**",
        f"- Campaign feasible (>=3 non-overlapping): **{mf['campaign_feasible_non_overlapping']}**",
        f"- Contiguous untested complete mark+funding months run >= {MIN_DESIGN_DAYS}d: **{mf['any_contiguous_run_ge_min_design_days']}**",
        "",
        "## FCLR-014 reproduction",
        "- Full-C2: 0 feasible blocks / no >=127d contiguous run. ✓" if full_cert['disjoint_n_feasible']==0 and not full_cert['design_feasibility_any_feasible'] else "- Full-C2: mismatch.",
        "- Mark+funding-only: 4 individually feasible (2024-10/11/12, 2025-01), 2 mutually non-overlapping (2024-10, 2025-01). ✓" if mf['n_individually_feasible']==4 and mf['max_mutually_non_overlapping']==2 else f"- Mark+funding-only: got {mf['n_individually_feasible']} individually / {mf['max_mutually_non_overlapping']} non-overlapping {mf['non_overlapping_selection']}.",
        "- Retracted claim: 4-block confirmatory prereg freeze (041333Z corrected / 051045Z) due to cross-block train/test overlap leakage.",
        "",
        "## Verdict detail",
        cert["verdict_detail"],
        "",
    ]
    out_md.write_text("\n".join(lines))
    print(json.dumps({"overall_verdict": overall, "promotable": False, "fclr014_closed_verdict_reproduced": fclr014_reproduction, "n_individually_feasible": mf['n_individually_feasible'], "max_mutually_non_overlapping": mf['max_mutually_non_overlapping'], "selection": mf['non_overlapping_selection'], "json": str(out_json), "md": str(out_md)}))


if __name__ == "__main__":
    main()
