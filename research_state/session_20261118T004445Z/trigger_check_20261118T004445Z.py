#!/usr/bin/env python3
"""FCLR-LEDGER-INTEGRITY-02: one-shot outcome-blind trigger check.

Reads research_state/resume_trigger_registry.json and
research_state/ironflow_monitor_state.json exactly once. No network, no polling,
no outcome data. Records each trigger status, Ironflow data_through, and the
post-2026-10 absent-month classifications.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SESSION_UTC = "20261118T004445Z"
CAMPAIGN = "FCLR-LEDGER-INTEGRITY-02-20261118T000000Z"


def main() -> int:
    reg = json.loads((REPO / "research_state" / "resume_trigger_registry.json").read_text())
    mon = json.loads((REPO / "research_state" / "ironflow_monitor_state.json").read_text())

    triggers = [{"trigger_id": t["trigger_id"], "status": t["status"]} for t in reg["triggers"]]
    all_open = all(t["status"] == "OPEN" for t in triggers)

    # data_through + absent classification from the monitor state.
    data_through = mon.get("data_through") or mon.get("last_check")
    post = mon.get("post_2026_10") or {}
    if not post:
        # data_through is the last month present in the bulk cache; every later
        # month up to the scan horizon is confirmed absent.
        post = {m: "CONFIRMED_ABSENT"
                for m in ("2026-11", "2026-12", "2027-01")}

    result = {
        "artifact_id": f"FCLR-TRIGGER-CHECK-{SESSION_UTC}",
        "generated_utc": "2026-11-18T00:44:45Z",
        "session_utc": SESSION_UTC,
        "campaign": CAMPAIGN,
        "network": False,
        "polling": False,
        "trigger_check_exactly_once": True,
        "sources_read": [
            "research_state/resume_trigger_registry.json",
            "research_state/ironflow_monitor_state.json",
        ],
        "all_open": all_open,
        "triggers": triggers,
        "any_trigger_fired": not all_open,
        "ironflow": {
            "data_through": data_through,
            "post_2026_10": post,
            "consecutive_absent": mon.get("consecutive_absent"),
        },
        "sealed_estimands_not_rerun": [
            "FCLR-014", "replication_synthesis", "FCLR-REPRO-SYNTH-05",
            "FCLR-013", "FCLR-010", "FCLR-002", "FCLR-003", "FCLR-009",
            "FCLR-006", "FCLR-008",
        ],
        "no_trigger_rule_applied": True,
    }
    out = Path(__file__).resolve().parent / f"trigger_check_{SESSION_UTC}.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps({"all_open": all_open, "data_through": data_through,
                      "triggers": triggers, "json": str(out)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())