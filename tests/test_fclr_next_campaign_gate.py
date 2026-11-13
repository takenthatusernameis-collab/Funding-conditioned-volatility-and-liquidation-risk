#!/usr/bin/env python3
"""Definition-of-done gate tests for FCLR-NEXT-CAMPAIGN-20261113T063000Z.

Fixtures are written to a temp research_state; the gate must fail closed until ALL
THREE cells have a frozen prereg and a terminal verdict, and must refuse to accept
a non-terminal verdict or a missing checks block.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import scripts.fclr_next_campaign_gate as gate

TERMINAL = {
    "LIQ-010-CONFIRM": "CONFIRMED",
    "EXP-ROBUST-REDO": "ROBUST",
    "FWD-VOL-2025-CROSS": "NOT_REPLICATED",
}
PREREGS = {
    "LIQ-010-CONFIRM": "prereg_fclr_liq_010_confirm_20261113T063000Z.json",
    "EXP-ROBUST-REDO": "prereg_fclr_exp_robust_redo_20261113T063000Z.json",
    "FWD-VOL-2025-CROSS": "prereg_fclr_fwd_vol_2025_cross_20261113T063000Z.json",
}
EVALS = {
    "LIQ-010-CONFIRM": "evaluation_summary_FCLR-LIQ-010-CONFIRM-20261113T063000Z.json",
    "EXP-ROBUST-REDO": "evaluation_summary_FCLR-EXP-ROBUST-REDO-20261113T063000Z.json",
    "FWD-VOL-2025-CROSS": "evaluation_summary_FCLR-FWD-VOL-2025-CROSS-20261113T063000Z.json",
}

# The gate matches on glob prefixes; fixtures must share the real filename prefix.
PREREG_PREFIX = {
    "LIQ-010-CONFIRM": "prereg_fclr_liq_010_confirm_",
    "EXP-ROBUST-REDO": "prereg_fclr_exp_robust_redo_",
    "FWD-VOL-2025-CROSS": "prereg_fclr_fwd_vol_2025_cross_",
}
EVAL_PREFIX = {
    "LIQ-010-CONFIRM": "evaluation_summary_FCLR-LIQ-010-CONFIRM-",
    "EXP-ROBUST-REDO": "evaluation_summary_FCLR-EXP-ROBUST-REDO-",
    "FWD-VOL-2025-CROSS": "evaluation_summary_FCLR-FWD-VOL-2025-CROSS-",
}


def _write_fixture(root: Path, *, cells=None, verdict_override=None, drop_checks=False,
                   prereg_status="FROZEN_PRE_OUTCOMES"):
    rs = root / "research_state"
    rs.mkdir(parents=True, exist_ok=True)
    cells = cells if cells is not None else list(TERMINAL)
    for cell in cells:
        (rs / PREREGS[cell]).write_text(json.dumps({
            "status": prereg_status,
            "outcome_data_inspected_before_freeze": prereg_status == "FROZEN_PRE_OUTCOMES",
        }))
        verdict = (verdict_override or {}).get(cell, TERMINAL[cell])
        payload = {"verdict": verdict}
        if not drop_checks:
            payload["checks"] = {"materiality_ge_2pct": True, "ci_excludes_zero": True}
        (rs / EVALS[cell]).write_text(json.dumps(payload))
    return rs


class NextCampaignGateTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self._orig_rs = getattr(gate, "RS", None)
        gate.RS = self.root / "research_state"
        self._orig_repo = gate.REPO
        # scripts live in the real repo; keep REPO pointing at it
        gate.REPO = Path(gate.__file__).resolve().parents[1]

    def tearDown(self) -> None:
        if self._orig_rs is None:
            if hasattr(gate, "RS"):
                delattr(gate, "RS")
        else:
            gate.RS = self._orig_rs
        gate.REPO = self._orig_repo
        self._tmp.cleanup()

    def test_empty_fails_closed(self) -> None:
        self.assertFalse(gate.run_gate() and all(c["ok"] for c in gate.run_gate()))

    def test_partial_fails_closed(self) -> None:
        _write_fixture(self.root, cells=["LIQ-010-CONFIRM"])
        checks = gate.run_gate()
        ok = all(c["ok"] for c in checks)
        self.assertFalse(ok)
        # the other two cells must be failing
        failed_cells = {c["check"].split(":")[0] for c in checks if not c["ok"]}
        self.assertIn("EXP-ROBUST-REDO", failed_cells)
        self.assertIn("FWD-VOL-2025-CROSS", failed_cells)

    def test_all_cells_complete_passes(self) -> None:
        _write_fixture(self.root)
        checks = gate.run_gate()
        self.assertTrue(all(c["ok"] for c in checks), [c for c in checks if not c["ok"]])

    def test_nonterminal_verdict_fails(self) -> None:
        _write_fixture(self.root, verdict_override={"EXP-ROBUST-REDO": "INCONCLUSIVE"})
        checks = gate.run_gate()
        ok = all(c["ok"] for c in checks)
        self.assertFalse(ok)
        failed = [c["check"] for c in checks if not c["ok"]]
        self.assertIn("EXP-ROBUST-REDO:terminal_verdict", failed)

    def test_missing_checks_block_fails(self) -> None:
        _write_fixture(self.root, drop_checks=True)
        checks = gate.run_gate()
        ok = all(c["ok"] for c in checks)
        self.assertFalse(ok)
        failed = [c["check"] for c in checks if not c["ok"]]
        self.assertTrue(any(c.endswith(":checks_present") for c in failed))

    def test_unfrozen_prereg_fails(self) -> None:
        _write_fixture(self.root, prereg_status="DRAFT")
        checks = gate.run_gate()
        ok = all(c["ok"] for c in checks)
        self.assertFalse(ok)
        failed = [c["check"] for c in checks if not c["ok"]]
        self.assertTrue(any(c.endswith(":prereg_frozen") for c in failed))

    def test_cell_verdict_sets_are_correct(self) -> None:
        # INCONCLUSIVE must be accepted for all three cells
        _write_fixture(self.root, verdict_override={
            "LIQ-010-CONFIRM": "INCONCLUSIVE",
            "EXP-ROBUST-REDO": "INCONCLUSIVE",
            "FWD-VOL-2025-CROSS": "INCONCLUSIVE",
        })
        checks = gate.run_gate()
        # INCONCLUSIVE is terminal for every cell, but it must still not be "complete"
        # for the campaign; the gate accepts it as a recorded terminal verdict.
        terminal_ok = all(c["ok"] for c in checks if c["check"].endswith(":terminal_verdict"))
        self.assertTrue(terminal_ok)


if __name__ == "__main__":
    unittest.main()