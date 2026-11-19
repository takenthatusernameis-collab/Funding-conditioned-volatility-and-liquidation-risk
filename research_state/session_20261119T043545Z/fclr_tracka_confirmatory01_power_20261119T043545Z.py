#!/usr/bin/env python3
"""FCLR-LIQ-TRACKA-CONFIRMATORY-01 power / MDE audit wrapper.
Delegates the stdlib computation to fclr_tracka_confirmatory01_evaluation_20261119T043545Z.py
and writes the power artifact pair for this session.
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
power = mod.run_power(analysis)
mod._dump_json(f"fclr_tracka_confirmatory01_power_{mod.UTC}.json", power)

lines = [
    "# Track A confirmatory power / MDE audit",
    f"Campaign: `{mod.CAMPAIGN_ID}`",
    f"Session: `{mod.SESSION}`",
    f"Status: **{power['status']}**",
    f"Panel base rate: {power['panel_base_rate']:.6f}",
    f"Plausible effect (absolute Brier): {power['plausible_effect_brier']}",
    "",
    "## Block MDE (80% power, two-sided alpha=0.05)",
]
for blk in mod.BLOCKS:
    v = power["blocks"][blk["name"]]
    lines.append(
        f"- {blk['name']}: n_test={v['n_test']}, n_events={v['n_events']}, "
        f"observed_base_rate={v.get('observed_base_rate', float('nan')):.6f}, "
        f"mde_brier={v.get('mde_brier')}, powered={v.get('powered')}"
    )
lines += ["", f"Overall: {power['status']}",
          "If UNDERPOWERED, the confirmatory evaluation must not be run and the campaign verdict is UNDERPOWERED."]
mod._write_text(f"fclr_tracka_confirmatory01_power_{mod.UTC}.md", "\n".join(lines) + "\n")
print(json.dumps({"status": power["status"]}, indent=2))
