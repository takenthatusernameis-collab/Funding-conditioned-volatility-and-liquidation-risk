#!/usr/bin/env python3
"""FCLR-LEDGER-INTEGRITY-02: refresh the outcome-blind trigger-activation readiness.

Carries forward the four pre-sized trigger contracts from
session_20261117T215904Z/trigger_activation_readiness_*.json (referee executor +
REFUSE_ALL + selftest already built there) and adds the corrected-frontier
reference from this session's frontier_recompute. No network, no outcome reads.

promotable=false, program_status=CLOSED_TERMINAL are preserved.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SESSION_UTC = "20261118T004445Z"
CAMPAIGN = "FCLR-LEDGER-INTEGRITY-02-20261118T000000Z"
PRIOR = REPO / "research_state" / "session_20261117T215904Z" / "trigger_activation_readiness_20261117T215904Z.json"


def main() -> int:
    prior = json.loads(PRIOR.read_text())
    contracts = prior["trigger_contracts"]
    assert len(contracts) == 4, "expected exactly four trigger contracts"

    frontier = json.loads(
        (Path(__file__).resolve().parent / f"frontier_recompute_{SESSION_UTC}.json").read_text()
    )
    ledger = json.loads(
        (Path(__file__).resolve().parent / f"ledger_audit_{SESSION_UTC}.json").read_text()
    )

    result = {
        "artifact_id": f"FCLR-TRIGGER-ACTIVATION-READINESS-{SESSION_UTC}",
        "generated_utc": "2026-11-18T00:44:45Z",
        "session_utc": SESSION_UTC,
        "campaign": CAMPAIGN,
        "network": False,
        "polling": False,
        "outcome_blind": True,
        "programme_verdict": {
            "promotable": False,
            "program_status": "CLOSED_TERMINAL",
            "new_scientific_claim": False,
            "campaign_status": "COMPLETE",
            "successor_state": "AWAITING_TRIGGER",
        },
        "sources_read": prior["sources_read"] + [
            f"research_state/{SESSION_UTC}/frontier_recompute_{SESSION_UTC}.json",
            f"research_state/{SESSION_UTC}/ledger_audit_{SESSION_UTC}.json",
        ],
        "trigger_contracts": contracts,
        "corrected_frontier_reference": {
            "artifact": f"frontier_recompute_{SESSION_UTC}.json",
            "n_individually_feasible": frontier["verdict"]["n_individually_feasible"],
            "individually_feasible_months": frontier["verdict"]["individually_feasible_months"],
            "max_mutually_non_overlapping": frontier["verdict"]["max_mutually_non_overlapping"],
            "campaign_feasible_non_overlapping":
                frontier["verdict"]["campaign_feasible_non_overlapping"],
            "frontier_closed": True,
        },
        "ledger_integrity_reference": {
            "artifact": f"ledger_audit_{SESSION_UTC}.json",
            "fclr002_003_union_months": ledger["headline"]["fclr002_003_union_months"],
            "all_union_months_consumed": ledger["headline"]["all_union_months_consumed"],
            "regression_2024_10_11_12_ok":
                ledger["headline"]["regression_months_2024_10_11_12_consumed_and_tested"],
        },
        "executable_artifacts": {
            "executor": prior["executable_artifacts"]["executor"],
            "selftest": prior["executable_artifacts"]["selftest"],
            "note": "Carried forward unchanged from session_20261117T215904Z; "
                    "referee executor is REFUSE_ALL, stdlib-only, exit 2 on all-open.",
        },
        "do_not_run_list": prior["do_not_run_list"],
        "reopen_trigger_path": prior["reopen_trigger_path"],
        "completeness_statement": (
            "Trigger-activation readiness refreshed outcome-blind. Four pre-sized "
            "contracts carried forward (Gate4/TrackC paired_n>=23224; "
            "TrackA/expansion paired_n>=11689; >=3 blocks; 7d purge/embargo; "
            "outcome_data_inspected_before_freeze=false). Corrected frontier and "
            "ledger integrity referenced. No scientific claim is promotable; "
            "advance is trigger-gated only."
        ),
    }
    out_dir = Path(__file__).resolve().parent
    (out_dir / f"trigger_activation_readiness_{SESSION_UTC}.json").write_text(
        json.dumps(result, indent=2, sort_keys=True))

    md = []
    md.append(f"# Trigger-Activation Readiness (refresh) — {SESSION_UTC}\n")
    md.append(f"Campaign: `{CAMPAIGN}`\n")
    md.append("Outcome-blind refresh of the trigger-activation package built in "
              "`session_20261117T215904Z`. Four pre-sized contracts carried "
              "forward; corrected frontier and ledger integrity referenced.\n")
    md.append("## Programme verdict\n")
    md.append(f"- promotable: **false**")
    md.append(f"- program_status: **{result['programme_verdict']['program_status']}**")
    md.append(f"- successor_state: {result['programme_verdict']['successor_state']}\n")
    md.append("## Trigger contracts (pre-sized, outcome-blind)\n")
    md.append("| trigger_id | track | paired_n_floor | 30d blocks | purge/embargo (d) | instruments | status |\n"
              "|---|---|---|---|---|---|---|")
    for c in contracts:
        md.append(f"| {c['trigger_id']} | {c.get('track','')} | {c.get('paired_n_floor')} | "
                  f"{c.get('non_overlapping_30d_test_blocks_min')} | "
                  f"{c.get('purge_embargo_days')} | {c.get('paired_oos_instruments_min')} | "
                  f"{c.get('trigger_status')} |")
    md.append("\n## Corrected frontier reference\n")
    cf = result["corrected_frontier_reference"]
    md.append(f"- artifact: `{cf['artifact']}`")
    md.append(f"- n_individually_feasible={cf['n_individually_feasible']} "
              f"({cf['individually_feasible_months']}); "
              f"max_mutually_non_overlapping={cf['max_mutually_non_overlapping']}; "
              f"campaign_feasible_non_overlapping={cf['campaign_feasible_non_overlapping']}")
    md.append(f"- frontier closed: **{cf['frontier_closed']}**\n")
    md.append("## Ledger integrity reference\n")
    li = result["ledger_integrity_reference"]
    md.append(f"- artifact: `{li['artifact']}`; "
              f"2024-04..2024-12 all consumed: **{li['all_union_months_consumed']}**; "
              f"2024-10/11/12 ok: **{li['regression_2024_10_11_12_ok']}**")
    md.append("")
    (out_dir / f"trigger_activation_readiness_{SESSION_UTC}.md").write_text("\n".join(md))

    print(json.dumps({"artifact": result["artifact_id"],
                      "contracts": [c["trigger_id"] for c in contracts],
                      "frontier_closed": cf["frontier_closed"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())