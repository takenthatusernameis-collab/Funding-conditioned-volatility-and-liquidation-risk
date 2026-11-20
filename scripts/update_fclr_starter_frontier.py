#!/usr/bin/env python3
"""Mark FCLR-STARTER-001 Step 1 phases COMPLETE in experiment_frontier.json.

Reads the on-disk session_20261120T024217Z artifact triad and flips the
rank-0 phases from NOT_STARTED to COMPLETE where the corresponding artifacts
exist and are non-empty. Never mutates any other rank. Never writes
research_state/research_protocol.md.

Usage:
  python3 scripts/update_fclr_starter_frontier.py [--json]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
FRONTIER = RS / "experiment_frontier.json"
SESSION = "session_20261120T024217Z"

# phase -> required file stems inside the session dir
PHASE_FILES = {
    "PREREG_FREEZE": [
        "fclr_starter001_protocol_freeze_20261120T024217Z.json",
        "fclr_starter001_protocol_freeze_20261120T024217Z.md",
    ],
    "PANEL_BUILD_AND_HASH": [
        "fclr_starter001_panel_freeze_20261120T024217Z.json",
        "fclr_starter001_panel_freeze_20261120T024217Z.md",
    ],
    "BASELINE_B0_B1": [
        "fclr_starter001_baselines_20261120T024217Z.py",
        "fclr_starter001_baselines_20261120T024217Z.json",
        "fclr_starter001_baselines_20261120T024217Z.md",
    ],
}


def _nonempty(rel_paths: list[str]) -> bool:
    return all((REPO / p).is_file() and (REPO / p).stat().st_size > 0 for p in rel_paths)


def main() -> int:
    data = json.loads(FRONTIER.read_text(encoding="utf-8"))
    changed = False
    sdir = RS / SESSION
    for entry in data:
        if entry.get("rank") != 0:
            continue
        for phase in entry.get("phases", []):
            name = phase.get("phase")
            files = PHASE_FILES.get(name)
            if files is None:
                continue
            if phase.get("status") == "COMPLETE":
                continue
            if _nonempty([str(sdir / f) for f in files]):
                phase["status"] = "COMPLETE"
                changed = True
        if changed:
            entry["refreshed"] = "20261120T033205Z"
            entry["last_checked"] = "20261120T033205Z"
            entry["next_unfinished_task"] = (
                "FCLR-STARTER-001 Step 2/3 confirmatory evaluation (Track C: 24h forward "
                "realized variance forecasting). Step 1 (protocol freeze + panel freeze + "
                "B0/B1 baselines + trigger_check) COMPLETE under "
                "research_state/session_20261120T024217Z/. Next: run C1/C2 vs B1 on the "
                "sealed holdout after 7-day purge/embargo; compute paired QLIKE diff, block "
                "bootstrap >=2000 reps, Holm correction, and emit verdict "
                "(FORECAST_GATE_PASSED or NOT_SUPPORTED)."
            )
            entry["next_action_heavy"] = (
                "Step 2/3: C1 (B1 + funding + percentile) and C2 (C1 + premium + EMA24) on "
                "dev/validation/holdout; paired QLIKE diff C2 vs B1; block bootstrap CI "
                "(>=2000 reps); Holm over family; verdict. Holdout opened only after "
                "protocol freeze (already frozen). Do NOT overwrite "
                "research_state/research_protocol.md (sealed legacy)."
            )
    if "--json" in sys.argv:
        print(json.dumps({"changed": changed, "phases": [
            {"phase": p["phase"], "status": p["status"]}
            for e in data if e.get("rank") == 0 for p in e.get("phases", [])
        ]}, indent=2))
    if changed:
        FRONTIER.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())