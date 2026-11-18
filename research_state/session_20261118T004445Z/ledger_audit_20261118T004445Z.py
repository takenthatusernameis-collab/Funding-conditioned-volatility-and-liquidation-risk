#!/usr/bin/env python3
"""FCLR-LEDGER-INTEGRITY-02: outcome-blind per-month consumed-window ledger audit.

Read-only. No network. No outcome metrics are opened. The only evaluation
artifacts read are the FCLR-002 / FCLR-003 ``## Splits (frozen)`` header lines
(train/val/test window *metadata*), never their QLIKE tables or any holdout.

For every month 2024-01..2026-10 it computes the union of train/val/test months
consumed by the frozen experiments, from:
  * scripts/next_campaign_status.py  TESTED_WINDOWS / BULK_TESTED_WINDOWS
  * research_state/evaluation_summary_FCLR002.md  frozen Splits header
  * research_state/evaluation_summary_FCLR003.md  frozen Splits header

Headline assertion: every month in the FCLR-002/003 train/val/test union
(2024-04..2024-12) is marked consumed by at least one experiment.

Usage:
  python3 research_state/<sid>/ledger_audit_<UTC>.py [--out-dir DIR]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import next_campaign_status as ncs  # noqa: E402

SESSION_UTC = "20261118T004445Z"
CAMPAIGN = "FCLR-LEDGER-INTEGRITY-02-20261118T000000Z"

SPLIT_FILES = {
    "FCLR-002": REPO / "research_state" / "evaluation_summary_FCLR002.md",
    "FCLR-003": REPO / "research_state" / "evaluation_summary_FCLR003.md",
}

MONTH_START = "2024-01"
MONTH_END = "2026-10"


def _months(a: str, b: str) -> list[str]:
    out = []
    y, m = int(a[:4]), int(a[5:7])
    ey, em = int(b[:4]), int(b[5:7])
    while (y, m) <= (ey, em):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out


def parse_frozen_splits(path: Path) -> dict:
    """Parse only the ``## Splits (frozen)`` window lines. Outcome-free."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    out = {"path": str(path.relative_to(REPO)), "lines": {}, "raw": {}}
    cur = None
    for i, ln in enumerate(lines, 1):
        if ln.startswith("## "):
            cur = ln.strip("# ").strip()
            continue
        if cur and cur.lower().startswith("splits"):
            m = re.match(r"\s*-\s*(Train|Val|Test)\s*:\s*(.+?)\s*\.\.\s*(.+?)\s*(?:\(.*\))?\s*$", ln)
            if m:
                phase = m.group(1).lower()
                start = m.group(2).strip()[:10]
                end = m.group(3).strip()[:10]
                out["lines"][phase] = i
                out["raw"][phase] = {"start": start, "end": end}
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=str(Path(__file__).resolve().parent))
    args = ap.parse_args(argv)
    out_dir = Path(args.out_dir)

    # 1) Registry windows (authoritative, code-truth).
    registry_windows = []
    for a, b, label in ncs.TESTED_WINDOWS:
        registry_windows.append({"start": a, "end": b, "label": label, "source": "TESTED_WINDOWS"})
    for a, b, label in ncs.BULK_TESTED_WINDOWS:
        registry_windows.append({"start": a, "end": b, "label": label, "source": "BULK_TESTED_WINDOWS"})

    # 2) Explicit frozen splits (metadata only).
    splits = {}
    split_windows = []
    for exp, path in SPLIT_FILES.items():
        p = parse_frozen_splits(path)
        splits[exp] = p
        for phase, w in p["raw"].items():
            split_windows.append({
                "experiment": exp,
                "phase": phase,
                "start": w["start"],
                "end": w["end"],
                "source_line": p["lines"][phase],
                "source_file": p["path"],
            })

    # 3) Per-month union.
    consumed: dict[str, dict] = {}

    def touch(month: str, exp: str, phase: str, src: str):
        rec = consumed.setdefault(month, {"consumed_by": [], "phases": []})
        tag = f"{exp}:{phase}"
        if tag not in rec["consumed_by"]:
            rec["consumed_by"].append(tag)
        if phase not in rec["phases"]:
            rec["phases"].append(phase)
        if src not in rec.setdefault("sources", []):
            rec["sources"].append(src)

    for w in registry_windows:
        for mo in _months(w["start"][:7], w["end"][:7]):
            if not (MONTH_START <= mo <= MONTH_END):
                continue
            # Registry labels look like "FCLR-... (STATUS)"; take the leading id token.
            exp = w["label"].split("(")[0].strip()
            touch(mo, exp, "test", w["source"])

    for w in split_windows:
        for mo in _months(w["start"][:7], w["end"][:7]):
            if not (MONTH_START <= mo <= MONTH_END):
                continue
            touch(mo, w["experiment"], w["phase"], "frozen_splits")

    # 4) Frontier cross-check per month (test-window truth only).
    months = []
    for mo in _months(MONTH_START, MONTH_END):
        rec = consumed.get(mo, {"consumed_by": [], "phases": []})
        months.append({
            "month": mo,
            "consumed": bool(rec["consumed_by"]),
            "consumed_by": rec["consumed_by"],
            "phase": rec["phases"],
            "frontier_says_tested": bool(ncs._inside_tested(mo)),
        })

    # 5) Headline assertions.
    union_002_003 = []
    for exp in ("FCLR-002", "FCLR-003"):
        for w in split_windows:
            if w["experiment"] == exp:
                for mo in _months(w["start"][:7], w["end"][:7]):
                    if mo not in union_002_003:
                        union_002_003.append(mo)
    union_002_003.sort()
    not_consumed = [mo for mo in union_002_003
                    if not consumed.get(mo, {}).get("consumed_by")]

    # The specific regression this campaign closes: 2024-10/11/12 must be consumed
    # (FCLR-003 test) and must NOT be reported as an untested fresh test month.
    regression_months = ["2024-10", "2024-11", "2024-12"]
    regression_ok = all(
        consumed.get(mo, {}).get("consumed_by") and ncs._inside_tested(mo)
        for mo in regression_months
    )

    result = {
        "artifact_id": f"FCLR-LEDGER-AUDIT-{SESSION_UTC}",
        "generated_utc": date.today().isoformat(),
        "session_utc": SESSION_UTC,
        "campaign": CAMPAIGN,
        "read_only": True,
        "network": False,
        "outcome_blind": True,
        "outcome_metrics_inspected": False,
        "note": (
            "Only the FCLR-002/003 '## Splits (frozen)' window lines (train/val/test "
            "metadata) are read; no QLIKE table, holdout, or results/* is opened. "
            "Consumed = any train/val/test window that used the month. "
            "frontier_says_tested = the mark+funding frontier's TEST-window ledger "
            "(scripts/next_campaign_status.py TESTED_WINDOWS); train/val months are "
            "legitimately NOT frontier-tested and may serve as pre-test history."
        ),
        "sources": {
            "tested_windows": "scripts/next_campaign_status.py:TESTED_WINDOWS",
            "bulk_tested_windows": "scripts/next_campaign_status.py:BULK_TESTED_WINDOWS",
            "fclr002_frozen_splits": splits["FCLR-002"]["path"],
            "fclr003_frozen_splits": splits["FCLR-003"]["path"],
        },
        "frozen_split_windows": split_windows,
        "registry_window_count": len(registry_windows),
        "months": months,
        "headline": {
            "fclr002_003_union_months": union_002_003,
            "n_union_months": len(union_002_003),
            "months_not_consumed": not_consumed,
            "all_union_months_consumed": len(not_consumed) == 0,
            "regression_months_2024_10_11_12_consumed_and_tested": regression_ok,
            "pass": len(not_consumed) == 0 and regression_ok,
        },
    }

    out_json = out_dir / f"ledger_audit_{SESSION_UTC}.json"
    out_json.write_text(json.dumps(result, indent=2, sort_keys=True))

    # Markdown rendering.
    md = []
    md.append(f"# Ledger Audit — {SESSION_UTC} (outcome-blind, read-only)\n")
    md.append(f"Campaign: `{CAMPAIGN}`\n")
    md.append("Reads only: `TESTED_WINDOWS` / `BULK_TESTED_WINDOWS` "
              "(scripts/next_campaign_status.py) and the FCLR-002/003 "
              "`## Splits (frozen)` header lines. No outcome metric, holdout, or "
              "`results/*` is opened.\n")
    md.append("## Headline assertion\n")
    h = result["headline"]
    md.append(f"- FCLR-002/003 consumed-union months: {h['n_union_months']} "
              f"({', '.join(h['fclr002_003_union_months'])})")
    md.append(f"- Months NOT consumed: {h['months_not_consumed'] or 'NONE'}")
    md.append(f"- 2024-10/11/12 consumed AND frontier-tested: "
              f"{h['regression_months_2024_10_11_12_consumed_and_tested']}")
    md.append(f"- **PASS: {h['pass']}**\n")
    md.append("## Frozen split windows (metadata only)\n")
    md.append("| experiment | phase | start | end | source |\n|---|---|---|---|---|")
    for w in split_windows:
        md.append(f"| {w['experiment']} | {w['phase']} | {w['start']} | {w['end']} "
                  f"| {w['source_file']}:{w['source_line']} |")
    md.append("\n## Per-month consumed ledger (2024-01..2026-10)\n")
    md.append("| month | consumed | consumed_by | phase | frontier_says_tested |\n"
              "|---|---|---|---|---|")
    for r in months:
        md.append(f"| {r['month']} | {r['consumed']} | "
                  f"{', '.join(r['consumed_by']) or '—'} | "
                  f"{', '.join(r['phase']) or '—'} | {r['frontier_says_tested']} |")
    md.append("")
    out_md = out_dir / f"ledger_audit_{SESSION_UTC}.md"
    out_md.write_text("\n".join(md))

    print(json.dumps({"json": str(out_json), "md": str(out_md),
                      "pass": h["pass"],
                      "union_months": len(union_002_003),
                      "months_not_consumed": not_consumed}, indent=2))
    return 0 if h["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())