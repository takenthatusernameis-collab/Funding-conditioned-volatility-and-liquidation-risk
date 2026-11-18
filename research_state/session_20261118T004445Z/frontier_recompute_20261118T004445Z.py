#!/usr/bin/env python3
"""FCLR-LEDGER-INTEGRITY-02: independent frontier recompute (verify, do not re-fix).

Re-runs the corrected `scripts/next_campaign_status.py` logic and confirms the
closed mark+funding frontier verdict. Read-only, no network, no outcome reads.

Expected (post FCLR-LEDGER-INTEGRITY-01 fix):
  n_individually_feasible = 1  (2025-01 only)
  max_mutually_non_overlapping = 1
  campaign_feasible_non_overlapping = False
  n_overlapping_pairs = 0
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import next_campaign_status as ncs  # noqa: E402

SESSION_UTC = "20261118T004445Z"
CAMPAIGN = "FCLR-LEDGER-INTEGRITY-02-20261118T000000Z"


def main() -> int:
    mf = ncs.markfund_frontier()
    df = ncs.disjoint_block_frontier(ncs.ready_windows())

    verdict = {
        "n_individually_feasible": mf["n_individually_feasible"],
        "individually_feasible_months": mf["individually_feasible_months"],
        "n_overlapping_pairs": mf["n_overlapping_pairs"],
        "max_mutually_non_overlapping": mf["max_mutually_non_overlapping"],
        "non_overlapping_selection": mf["non_overlapping_selection"],
        "campaign_feasible_non_overlapping": mf["campaign_feasible_non_overlapping"],
        "any_individually_feasible": mf["any_individually_feasible"],
        "disjoint_n_feasible": df["n_feasible"],
        "disjoint_campaign_feasible": df["campaign_feasible"],
    }

    expected = {
        "n_individually_feasible": 1,
        "individually_feasible_months": ["2025-01"],
        "n_overlapping_pairs": 0,
        "max_mutually_non_overlapping": 1,
        "campaign_feasible_non_overlapping": False,
    }
    mismatches = {k: {"expected": v, "observed": verdict[k]}
                  for k, v in expected.items() if verdict[k] != v}

    # Arithmetic that closes the frontier.
    feasible_month = mf["individually_feasible_months"]
    block = None
    for c in mf["candidate_test_months"]:
        if c["test_month"] in feasible_month:
            block = c
            break
    arithmetic = {
        "only_individually_feasible_month": feasible_month,
        "block_train_window": [block["train_start"], block["train_end"]] if block else None,
        "block_test_month": block["test_month"] if block else None,
        "block_train_months": block["train_months"] if block else None,
        "reason_single_block_insufficient": (
            "1 feasible block < MIN_MF_BLOCKS=3; train history may overlap prior "
            "tested windows, but the test month itself is untested, so a single "
            "block cannot form a 3-block campaign."
        ),
        "contiguous_untested_complete_mf_runs":
            mf["contiguous_runs_untested_complete_mf_months"],
        "min_design_days": mf["min_design_days"],
        "any_contiguous_run_ge_min_design_days":
            mf["any_contiguous_run_ge_min_design_days"],
    }

    result = {
        "artifact_id": f"FCLR-FRONTIER-RECOMPUTE-{SESSION_UTC}",
        "session_utc": SESSION_UTC,
        "campaign": CAMPAIGN,
        "read_only": True,
        "network": False,
        "outcome_blind": True,
        "note": (
            "Verification only. The FCLR-LEDGER-INTEGRITY-01 TESTED_WINDOWS fix is "
            "applied; this re-derives the closed verdict and must NOT re-fix code."
        ),
        "verdict": verdict,
        "expected_closed_verdict": expected,
        "mismatches": mismatches,
        "arithmetic_that_closes_frontier": arithmetic,
        "pass": len(mismatches) == 0,
    }

    out_dir = Path(__file__).resolve().parent
    (out_dir / f"frontier_recompute_{SESSION_UTC}.json").write_text(
        json.dumps(result, indent=2, sort_keys=True))

    md = []
    md.append(f"# Frontier Recompute — {SESSION_UTC} (verify, do not re-fix)\n")
    md.append(f"Campaign: `{CAMPAIGN}`\n")
    md.append("Independently re-runs `scripts/next_campaign_status.py` "
              "`markfund_frontier()` + `disjoint_block_frontier()`. Read-only, "
              "outcome-blind.\n")
    md.append("## Observed vs expected closed verdict\n")
    md.append("| field | expected | observed | match |\n|---|---|---|---|")
    for k, v in expected.items():
        md.append(f"| {k} | `{v}` | `{verdict[k]}` | {verdict[k] == v} |")
    md.append(f"\n**PASS: {result['pass']}** (mismatches: {mismatches or 'none'})\n")
    md.append("## Arithmetic that closes the frontier\n")
    md.append(f"- Only individually-feasible test month(s): "
              f"{feasible_month} (< MIN_MF_BLOCKS={mf['min_blocks_required']})")
    if block:
        md.append(f"- Its 30-day train window {block['train_start']}..{block['train_end']} "
                  f"over {block['train_months']} is FCLR-003 test, allowed as "
                  f"pre-test history; the test month itself is untested.")
    md.append(f"- Contiguous untested complete mark+funding runs: "
              f"{[ (r['months'], r['span_days']) for r in mf['contiguous_runs_untested_complete_mf_months'] ]}; "
              f"max span vs MIN_DESIGN_DAYS={mf['min_design_days']} -> "
              f"feasible={mf['any_contiguous_run_ge_min_design_days']}.")
    md.append(f"- Therefore `max_mutually_non_overlapping="
              f"{mf['max_mutually_non_overlapping']}` "
              f"`campaign_feasible_non_overlapping="
              f"{mf['campaign_feasible_non_overlapping']}`. **Frontier closed.**")
    md.append("")
    (out_dir / f"frontier_recompute_{SESSION_UTC}.md").write_text("\n".join(md))

    print(json.dumps({"pass": result["pass"], "verdict": verdict,
                      "mismatches": mismatches}, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())