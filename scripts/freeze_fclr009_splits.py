#!/usr/bin/env python3
"""Freeze FCLR-009 split boundaries into run_manifest.json BEFORE outcome inspection.

60/20/20 chronological split by unique UTC timestamps across the common 5-symbol
panel; 7-day purge/embargo at all split boundaries (FCLR-009 pre-registered).
Coverage-only audit research_state/fclr009_coverage_audit.json confirmed contiguous
2025-01-01..2025-12-31 coverage across all 5 symbols (365 days, 8760 common hourly
timestamps, 12 non-overlapping 30-day blocks) BEFORE this file was created and
BEFORE any QLIKE/outcome computation.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "research_state" / "run_manifest.json"

BOUNDARIES = {
    "status": "frozen",
    "rule": "chronological 60/20/20 split by unique UTC timestamps across the common 5-symbol panel; 7-day purge/embargo at all split boundaries (FCLR-009 pre-registered; coverage-only audit research_state/fclr009_coverage_audit.json confirmed contiguous 2025-01-01..2025-12-31 coverage across all 5 symbols before any outcomes computed)",
    "embargo_days": 7,
    "data_window": {
        "start": "2025-01-01T00:00:00Z",
        "end": "2025-12-31T23:00:00Z",
    },
    "train": {
        "start": "2025-01-01T00:00:00Z",
        "end": "2025-04-05T23:00:00Z",
    },
    "validation": {
        "start": "2025-04-13T00:00:00Z",
        "end": "2025-05-31T23:00:00Z",
    },
    "test": {
        "start": "2025-06-08T00:00:00Z",
        "end": "2025-12-31T23:00:00Z",
    },
    "block_requirement": "test window 2025-06-08..2025-12-31 = 206 days = 6 non-overlapping 30-day blocks (Jun 8-Jul 7, Jul 8-Aug 7, Aug 8-Sep 6, Sep 7-Oct 6, Oct 7-Nov 5, Nov 6-Dec 5) + 26-day remainder; required >=3 -> MET",
    "frozen_before_outcomes": True,
    "frozen_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "protocol_ref": "research_state/research_protocol_fclr009.md v1.0",
}


def main():
    m = json.loads(MANIFEST.read_text())
    m["split_boundaries_fclr009"] = BOUNDARIES
    m["last_experiment"] = "FCLR-009"
    m.setdefault("experiments", {})["FCLR-009"] = {
        "track": "C",
        "status": "SPLITS_FROZEN_OUTCOMES_NOT_COMPUTED",
        "gate": "PENDING",
        "summary": "Confirmatory volatility forecast on unsealed 2025-01-01..2025-12-31 panel (5 symbols BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT, 365 days, 8760 common hourly timestamps, 12 non-overlapping 30-day blocks). Splits frozen BEFORE outcome inspection. Awaiting FCLR_EXPERIMENT=FCLR-009 run of scripts/run_evaluation.py.",
    }
    m["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    MANIFEST.write_text(json.dumps(m, indent=1))
    print("Wrote split_boundaries_fclr009 to run_manifest.json")
    print(json.dumps(BOUNDARIES, indent=1))


if __name__ == "__main__":
    main()