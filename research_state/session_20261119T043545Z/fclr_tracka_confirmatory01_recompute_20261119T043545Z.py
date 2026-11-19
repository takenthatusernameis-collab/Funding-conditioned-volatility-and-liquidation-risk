#!/usr/bin/env python3
"""FCLR-LIQ-TRACKA-CONFIRMATORY-01 independent stdlib recompute wrapper.
Delegates to fclr_tracka_confirmatory01_evaluation_20261119T043545Z.py and writes
the recompute artifact pair for this session.
"""
import importlib.util
import json
from pathlib import Path

here = Path(__file__).resolve().parent
core_path = here / "fclr_tracka_confirmatory01_evaluation_20261119T043545Z.py"
spec = importlib.util.spec_from_file_location("fclr_confirm_core", core_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

rows = mod.load_panel(mod.PANEL)
analysis = mod.build_features(rows)
recompute = mod.run_recompute(analysis)
mod._dump_json(f"fclr_tracka_confirmatory01_recompute_{mod.UTC}.json", recompute)

lines = [
    "# Track A confirmatory independent stdlib recompute",
    f"Campaign: `{mod.CAMPAIGN_ID}`",
    f"Session: `{mod.SESSION}`",
    f"Panel: {recompute['panel_path']}",
    f"Panel SHA-256: {recompute['panel_sha256']}",
    f"Panel CSV rows: {recompute['panel_csv_rows']}",
    f"Analysis rows: {recompute['analysis_rows']}",
    f"Analysis events: {recompute['analysis_events']}",
    f"Analysis base rate: {recompute['analysis_base_rate']:.6f}",
    f"n_discrepancies: {recompute['n_discrepancies']}",
    f"Discrepancies: {recompute['discrepancies']}",
    "",
    "## Block membership",
] + [f"- {b['name']}: n_test={recompute['block_membership'][b['name']]}, n_events={recompute['block_events'][b['name']]}"
     for b in mod.BLOCKS] + [
    "",
    "n_discrepancies must be 0 for the frozen panel.",
]
mod._write_text(f"fclr_tracka_confirmatory01_recompute_{mod.UTC}.md", "\n".join(lines) + "\n")
print(json.dumps({"n_discrepancies": recompute["n_discrepancies"]}, indent=2))
