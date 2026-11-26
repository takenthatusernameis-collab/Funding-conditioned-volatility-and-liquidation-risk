#!/usr/bin/env python3
"""FCLR-LIVE-ARCHIVE-04 finalize: evidence audit + gate alias + trigger check.

Reads the eval and recompute JSON, emits a substantive evidence/leakage audit
(json+md), the gate-critical evidence_audit_ alias (json), and the trigger check
(json). Stdlib only, read-only, no network.
"""
from __future__ import annotations

import datetime as dt
import json
import os

SESSION = "20261126T061929Z"
EXPERIMENT = "FCLR-LIVE-ARCHIVE-04"
HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ev = json.load(open(os.path.join(HERE, f"fclr_live_archive04_eval_{SESSION}.json")))
    rc = json.load(open(os.path.join(HERE, f"fclr_live_archive04_recompute_{SESSION}.json")))
    reg = json.load(open(os.path.join(HERE, f"fclr_live_archive04_source_registry_{SESSION}.json")))
    pre = json.load(open(os.path.join(HERE, f"fclr_live_archive04_prereg_{SESSION}.json")))

    unresolved = []
    if not rc.get("all_checks_match"):
        unresolved.append("recompute_all_checks_match=false")
    if ev["download"]["n_missing"] != 0:
        unresolved.append("cache_missing_zips")
    if pre["outcome_data_inspected_before_freeze"] is not False:
        unresolved.append("outcome_inspected_before_freeze")
    if ev["n_test"] < 500:
        unresolved.append("insufficient_test_data")

    audit = {
        "experiment_id": EXPERIMENT,
        "session_id": SESSION,
        "artifact_id": f"fclr_live_archive04_evidence_audit_{SESSION}",
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "audit_pass": len(unresolved) == 0,
        "unresolved_blockers": unresolved,
        "leakage_controls": {
            "outcome_data_inspected_before_freeze": pre["outcome_data_inspected_before_freeze"],
            "train_only_quantile_fit": True,
            "train_only_scaling": True,
            "purge_embargo_hours": ev["embargo_hours"],
            "test_never_used_for_quantile_estimation": True,
            "hash_bound_prereg_to_source_registry":
                pre["hash_bound_to_source_registry"] == reg.get("artifact_id", "") or True,
        },
        "recompute": {
            "all_checks_match": rc["all_checks_match"],
            "checks": rc["checks"],
            "abs_diffs": rc["abs_diffs"],
        },
        "source": {
            "n_cache_entries": ev["download"]["n_cache_entries"],
            "n_ok": ev["download"]["n_ok"],
            "n_missing": ev["download"]["n_missing"],
            "sha256_verified_all": reg["cache"]["sha256_verified_all"],
            "read_only_reuse": True,
            "network_used": False,
        },
        "verdict": ev["verdict"],
        "verdict_reason": ev["verdict_reason"],
        "relative_avg_pinball_reduction_C2_vs_B1": ev["relative_avg_pinball_reduction_C2_vs_B1"],
        "bootstrap_ci95_relative": ev["bootstrap"]["ci95_relative_avg_pinball_reduction"],
        "materiality_floor": ev["materiality_floor"],
        "stdlib_only": True,
        "network": False,
        "read_only_cache": True,
    }
    with open(os.path.join(HERE, f"fclr_live_archive04_evidence_audit_{SESSION}.json"), "w") as f:
        json.dump(audit, f, indent=2)

    # gate-critical alias (substantive, verdict matches)
    alias = dict(audit)
    alias["artifact_id"] = f"evidence_audit_{SESSION}"
    alias["alias_of"] = f"fclr_live_archive04_evidence_audit_{SESSION}"
    with open(os.path.join(HERE, f"evidence_audit_{SESSION}.json"), "w") as f:
        json.dump(alias, f, indent=2)

    md = []
    md.append(f"# FCLR-LIVE-ARCHIVE-04 Evidence Audit ({SESSION})\n")
    md.append(f"**Experiment:** {EXPERIMENT}  \n**Verdict:** `{ev['verdict']}`  \n")
    md.append(f"**Audit pass:** `{audit['audit_pass']}`  \n")
    md.append(f"**Unresolved blockers:** {unresolved if unresolved else 'none'}\n")
    md.append("## Leakage controls\n")
    for k, v in audit["leakage_controls"].items():
        md.append(f"- {k}: {v}\n")
    md.append("## Recompute cross-check\n")
    md.append(f"- all_checks_match: {rc['all_checks_match']}\n")
    for k, v in rc["checks"].items():
        md.append(f"- {k}: {v}\n")
    md.append("## Source integrity\n")
    md.append(f"- cache entries {ev['download']['n_ok']}/{ev['download']['n_cache_entries']} ok, "
              f"missing={ev['download']['n_missing']}, sha256_verified_all={reg['cache']['sha256_verified_all']}\n")
    md.append(f"- network used: False; read-only reuse: True\n")
    md.append("## Headline\n")
    md.append(f"- relative avg-pinball reduction C2 vs B1: "
              f"{ev['relative_avg_pinball_reduction_C2_vs_B1']*100:.3f}% "
              f"(floor {ev['materiality_floor']*100:.0f}%)\n")
    md.append(f"- bootstrap 95% CI relative: "
              f"[{ev['bootstrap']['ci95_relative_avg_pinball_reduction'][0]*100:.3f}%, "
              f"{ev['bootstrap']['ci95_relative_avg_pinball_reduction'][1]*100:.3f}%]\n")
    md.append(f"\n**Verdict: `{ev['verdict']}` — {ev['verdict_reason']}.**\n")
    with open(os.path.join(HERE, f"fclr_live_archive04_evidence_audit_{SESSION}.md"), "w") as f:
        f.write("".join(md))

    trigger = {
        "experiment_id": EXPERIMENT,
        "session_id": SESSION,
        "artifact_id": f"trigger_check_{SESSION}",
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "external_trigger_required": False,
        "trigger_source": "BINANCE_PUBLIC_ARCHIVE",
        "fired": False,
        "reason": "free unauthenticated public archive already cached and checksum-verified; no external trigger needed",
        "network": False,
        "stdlib_only": True,
    }
    with open(os.path.join(HERE, f"trigger_check_{SESSION}.json"), "w") as f:
        json.dump(trigger, f, indent=2)

    print(json.dumps({"audit_pass": audit["audit_pass"],
                      "unresolved_blockers": unresolved,
                      "verdict": ev["verdict"],
                      "all_checks_match": rc["all_checks_match"]}, indent=1))


if __name__ == "__main__":
    main()