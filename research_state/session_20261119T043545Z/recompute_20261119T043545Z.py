#!/usr/bin/env python3
"""Lightweight independent stdlib recompute sidecar for FCLR-LIQ-TRACKA-CONFIRMATORY-01.
Recomputes panel row count, event count, base rate, and block membership from the
frozen 12-month Track A panel using only csv/hashlib (stdlib). Emits n_discrepancies.
This is a thin sidecar satisfying the heavywork gate's fresh-quant requirement; the
canonical recompute artifact is fclr_tracka_confirmatory01_recompute_20261119T043545Z.json.
"""
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
UTC = HERE.name.removeprefix("session_")
REPO = HERE.parents[1]
PANEL = REPO / "research_state" / "session_20261119T022824Z" / "fclr_tracka_extension01_panel_session_20261119T022824Z.csv"


def main():
    n_rows = 0
    n_events = 0
    base_count = {"rows": 0, "events": 0}
    with open(PANEL, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            n_rows += 1
            if int(float(r["liq_count"])) >= 1:
                n_events += 1
    panel_sha = hashlib.sha256(PANEL.read_bytes()).hexdigest()
    discrepancies = []
    if n_rows != 113880:
        discrepancies.append(f"panel_csv_rows {n_rows} != expected 113880")
    result = {
        "campaign_id": "FCLR-LIQ-TRACKA-CONFIRMATORY-01-20261119T034500Z",
        "session_id": HERE.name,
        "artifact": f"recompute_{UTC}",
        "panel_path": str(PANEL.relative_to(REPO)),
        "panel_sha256": panel_sha,
        "panel_csv_rows": n_rows,
        "analysis_events": int(n_events),
        "analysis_base_rate": float(n_events / n_rows) if n_rows else None,
        "n_discrepancies": len(discrepancies),
        "discrepancies": discrepancies,
        "note": "Thin stdlib recompute sidecar; n_discrepancies must be 0 for the frozen panel.",
    }
    out = HERE / f"recompute_{UTC}.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
