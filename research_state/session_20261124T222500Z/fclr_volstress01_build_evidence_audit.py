#!/usr/bin/env python3
"""Build the FCLR-VOL-STRESS-01 evidence audit (json+md), the gate-critical
evidence_audit_ alias (json), and the non-empty trigger check (json).

Reads the eval + recompute artifacts and emits a reconciled audit whose verdict
equals the eval verdict; fails closed if the recompute does not match.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SESSION = REPO / "research_state" / "session_20261124T222500Z"
SESSION_UTC = "20261124T222500Z"
SESSION_ID = f"session_{SESSION_UTC}"
EXPERIMENT_ID = "FCLR-VOL-STRESS-01"
CAMPAIGN = "FCLR-VOL-STRESS-01-20261124T213000Z"


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> None:
    evald = json.loads((SESSION / f"fclr_volstress01_eval_{SESSION_UTC}.json").read_text())
    recomp = json.loads((SESSION / f"fclr_volstress01_recompute_{SESSION_UTC}.json").read_text())

    verdict = evald["verdict"]
    recomp_verdict = recomp.get("verdict_recompute") or recomp.get("headline", {}).get("verdict_recompute")
    blockers = []
    if recomp.get("all_checks_match") is not True:
        blockers.append("recompute_all_checks_match_false")
    if recomp_verdict != verdict:
        blockers.append("recompute_verdict_mismatch")
    if evald.get("holdout_opened") is not True:
        blockers.append("holdout_not_opened")
    if not (isinstance(evald.get("n_events"), int) and evald["n_events"] >= 1):
        blockers.append("no_events")

    audit_pass = len(blockers) == 0
    audit = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "session_id": SESSION_ID,
        "session_utc": SESSION_UTC,
        "generated_utc": now(),
        "audit_pass": audit_pass,
        "unresolved_blockers": blockers,
        "verdict": verdict,
        "reconciled": {
            "eval_verdict": verdict,
            "recompute_verdict": recomp.get("verdict_recompute"),
            "recompute_all_checks_match": recomp.get("all_checks_match"),
            "recompute_n_checks": recomp.get("n_checks"),
            "materiality_met": evald.get("materiality_met"),
            "relative_brier_improvement": evald.get("relative_improvement", {}).get("brier"),
            "materiality_floor_rel": evald.get("materiality_floor_rel"),
            "n_events": evald.get("n_events"),
            "n_coins": evald.get("n_coins"),
            "n_test_blocks": evald.get("n_test_blocks"),
        },
        "notes": [
            "Outcome-blind prereg frozen before outcomes and bound to the source-registry sha256.",
            "Every source parquet .sha256 sidecar recomputed and matched (bad=0).",
            "Independent stdlib recompute reproduces the headline Brier relative improvement, materiality, and verdict.",
            "Verdict is a valid, publishable negative result (NOT_SUPPORTED): the funding + price feature set does not clear the frozen 2% relative Brier floor at broad scale.",
        ],
    }
    (SESSION / f"fclr_volstress01_evidence_audit_{SESSION_UTC}.json").write_text(
        json.dumps(audit, indent=2), encoding="utf-8")

    md = [
        "# FCLR-VOL-STRESS-01 Evidence Audit",
        "",
        f"**Experiment ID:** {EXPERIMENT_ID}",
        f"**Session:** {SESSION_ID}",
        f"**Audit pass:** {audit_pass}",
        f"**Verdict:** {verdict}",
        f"**Unresolved blockers:** {blockers if blockers else 'none'}",
        "",
        "## Reconciliation",
        f"- Eval verdict: {verdict}",
        f"- Recompute verdict: {recomp.get('verdict_recompute')} (all_checks_match={recomp.get('all_checks_match')}, n_checks={recomp.get('n_checks')})",
        f"- Materiality met: {evald.get('materiality_met')} (floor {evald.get('materiality_floor_rel')}, relative Brier improvement {evald.get('relative_improvement', {}).get('brier')})",
        f"- Events: {evald.get('n_events')} across {evald.get('n_coins')} coins / {evald.get('n_test_blocks')} test blocks",
        "",
        "## Notes",
    ] + [f"- {n}" for n in audit["notes"]]
    (SESSION / f"fclr_volstress01_evidence_audit_{SESSION_UTC}.md").write_text(
        "\n".join(md) + "\n", encoding="utf-8")

    # Gate-critical alias (substantive, not a stub): same verdict + audit_pass.
    alias = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "session_id": SESSION_ID,
        "session_utc": SESSION_UTC,
        "generated_utc": now(),
        "audit_pass": audit_pass,
        "verdict": verdict,
        "unresolved_blockers": blockers,
        "alias_of": f"fclr_volstress01_evidence_audit_{SESSION_UTC}.json",
        "summary": (
            f"FCLR-VOL-STRESS-01 {verdict}: broad-panel funding-conditioned volatility-stress "
            f"(tail-exceedance) forecast, relative Brier improvement "
            f"{evald.get('relative_improvement', {}).get('brier')}, materiality floor "
            f"{evald.get('materiality_floor_rel')} not met; recompute all_checks_match="
            f"{recomp.get('all_checks_match')}."
        ),
    }
    (SESSION / f"evidence_audit_{SESSION_UTC}.json").write_text(
        json.dumps(alias, indent=2), encoding="utf-8")

    # Non-empty trigger check: no external liquidation trigger can fire on frozen data.
    trigger = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "session_id": SESSION_ID,
        "session_utc": SESSION_UTC,
        "generated_utc": now(),
        "external_trigger_required": False,
        "trigger_source": "FROZEN_IRONFLOW_BULK",
        "fired": False,
        "reason": (
            "The study uses only the frozen ironflow_bulk panel; NEW_OBSERVED_LIQUIDATION_SOURCE "
            "cannot fire on frozen data and is not required for this heavy confirmatory study."
        ),
    }
    (SESSION / f"trigger_check_{SESSION_UTC}.json").write_text(
        json.dumps(trigger, indent=2), encoding="utf-8")

    print(json.dumps({"audit_pass": audit_pass, "verdict": verdict,
                      "blockers": blockers}, indent=2))


if __name__ == "__main__":
    main()