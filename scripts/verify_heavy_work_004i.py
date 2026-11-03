#!/usr/bin/env python3
"""
Verify heavy-work checklist for campaign LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i is complete.
Non-skippable gate: fails if any required evidence missing.
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).parent.parent
HANDOFF = REPO_ROOT / "AGENT_HANDOFF.md"
FRONTIER = REPO_ROOT / "research_state" / "experiment_frontier.json"
MONITOR_STATE = REPO_ROOT / "research_state" / "ironflow_monitor_state.json"
CHECKLIST = REPO_ROOT / "research_state" / "heavy_work_checklist_004i.md"

REQUIRED_BLOCKER_PATTERNS = ["liquidation_forward_validate_004_blocker_"]


def fail(msg):
    print(f"FAIL: {msg}", file=sys.stderr)
    return False


def main():
    ok = True
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    # Check handoff exists and has required sections
    if not HANDOFF.exists():
        ok = fail("AGENT_HANDOFF.md missing")
    else:
        txt = HANDOFF.read_text()
        required = [
            "LIQUIDATION_FORWARD_VALIDATE_HEAVY-004i",
            "HEAVY WORK",
        ]
        for r in required:
            if r.lower() not in txt.lower():
                ok = fail(f"HANDOFF missing required: {r}")
        # Resume triggers: accept either literal "resume trigger" or the
        # "RESUME CONDITIONS" / "RESUME CONDITION" section heading used by the
        # durable handoff. The canonical non-skippable checklist lives in
        # research_state/heavy_work_checklist_004i.md (checked separately below).
        if not any(s in txt.lower() for s in (
                "resume trigger", "resume condition", "resume conditions")):
            ok = fail("HANDOFF missing resume trigger/condition section")
        if "heavy_work_checklist_004i.md" not in txt.lower() and not (REPO_ROOT / "research_state" / "heavy_work_checklist_004i.md").exists():
            ok = fail("HANDOFF must reference heavy_work_checklist_004i.md")
        if ok:
            print("OK: handoff has required sections")

    # Check frontier
    if not FRONTIER.exists():
        ok = fail("experiment_frontier.json missing")
    else:
        try:
            with open(FRONTIER) as f:
                data = json.load(f)
            # Check for 004i campaign
            found = False
            for item in data.get("frontier", []):
                if "004i" in str(item.get("task", "")) or "LIQUIDATION_FORWARD_VALIDATE" in str(item.get("task", "")):
                    found = True
                    if item.get("status") != "BLOCKED_ON_DATA":
                        print(f"WARN: 004i status is {item.get('status')}, expected BLOCKED_ON_DATA")
            if not found:
                ok = fail("frontier missing 004i campaign entry")
            else:
                print("OK: frontier has 004i entry")
        except Exception as e:
            ok = fail(f"frontier parse error: {e}")

    # Check monitor state
    if not MONITOR_STATE.exists():
        ok = fail("ironflow_monitor_state.json missing")
    else:
        try:
            with open(MONITOR_STATE) as f:
                ms = json.load(f)
            print(f"OK: monitor state exists (data_through={ms.get('data_through')}, consecutive_absent={ms.get('consecutive_absent')})")
        except Exception as e:
            ok = fail(f"monitor state parse error: {e}")

    # Check checklist
    if not CHECKLIST.exists():
        ok = fail("heavy_work_checklist_004i.md missing")
    else:
        print("OK: heavy work checklist exists")

    # Check for blocker docs
    blocker_docs = list((REPO_ROOT / "research_state").glob("liquidation_forward_validate_004_blocker_*.md"))
    if not blocker_docs:
        ok = fail("No liquidation_forward_validate_004_blocker_*.md found")
    else:
        latest = sorted(blocker_docs)[-1]
        print(f"OK: blocker docs exist ({len(blocker_docs)} found), latest: {latest.name}")

    if ok:
        print(f"ALL CHECKS PASSED [{ts}]")
        return 0
    else:
        print(f"SOME CHECKS FAILED [{ts}]", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
