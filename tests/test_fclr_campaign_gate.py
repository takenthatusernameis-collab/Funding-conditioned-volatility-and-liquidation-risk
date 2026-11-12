#!/usr/bin/env python3
"""Fixture tests for scripts/fclr_campaign_gate.py (no network, no real cache).

The gate is the campaign's definition of done, so its failure modes must be pinned:
absent artifacts fail, a mismatched panel hash fails, a non-frozen prereg fails,
an unrecognised verdict fails, and a complete fixture passes.
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "fclr_campaign_gate.py"

_spec = importlib.util.spec_from_file_location("fclr_campaign_gate", SCRIPT)
gate = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(gate)


def _write_panel(root: Path, name: str, payload: bytes = b"panel-bytes") -> str:
    p = root / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(payload)
    return gate.sha256_file(p)


class GateTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "research_state").mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _prereg(self, stem: str, frozen: bool) -> None:
        (self.root / "research_state" / f"{stem}.json").write_text(json.dumps({
            "experiment_id": stem,
            "frozen_before_outcomes": frozen,
            "pre_registered_before_outcomes": frozen,
        }))

    def _report(self, stem: str, sha: str) -> None:
        (self.root / "research_state" / f"{stem}.json").write_text(json.dumps({
            "panel_sha256": sha,
        }))

    def _eval(self, stem: str, verdict: str, with_family: bool = True) -> None:
        payload = {"verdict": verdict, "contrasts": {"C2_vs_B1": {"rel_reduction_pct": 0.0}}}
        if with_family:
            payload["family_results"] = {
                h: {c: {"p": 1.0} for c in ("C2_vs_B1", "C1_vs_B1", "C2_vs_C1")}
                for h in ("6h", "24h", "72h", "168h")
            }
        (self.root / "research_state" / f"{stem}.json").write_text(json.dumps(payload))


class TestPreregCheck(GateTestCase):
    def test_missing_prereg_fails(self):
        self.assertFalse(gate.check_prereg_frozen(self.root, gate.ARM_A_PREREG_GLOB, "A1")["ok"])

    def test_unfrozen_prereg_fails(self):
        self._prereg("prereg_tracka_vol_fullhist_20261112T201536Z", frozen=False)
        self.assertFalse(gate.check_prereg_frozen(self.root, gate.ARM_A_PREREG_GLOB, "A1")["ok"])

    def test_frozen_prereg_passes(self):
        self._prereg("prereg_tracka_vol_fullhist_20261112T201536Z", frozen=True)
        self.assertTrue(gate.check_prereg_frozen(self.root, gate.ARM_A_PREREG_GLOB, "A1")["ok"])


class TestPanelReportCheck(GateTestCase):
    def test_missing_panel_and_report_fail(self):
        checks = gate.check_panel_and_report(
            self.root, "tracka_vol_fullhist_panel_*.parquet",
            "tracka_vol_fullhist_panel_build_report_*.json", "A3")
        self.assertFalse(any(c["ok"] for c in checks))

    def test_matching_hash_passes(self):
        sha = _write_panel(self.root, "research_state/tracka_vol_fullhist_panel_20261112T201536Z.parquet")
        self._report("tracka_vol_fullhist_panel_build_report_20261112T201536Z", sha)
        checks = gate.check_panel_and_report(
            self.root, "tracka_vol_fullhist_panel_*.parquet",
            "tracka_vol_fullhist_panel_build_report_*.json", "A3")
        self.assertTrue(all(c["ok"] for c in checks))

    def test_hash_mismatch_fails(self):
        _write_panel(self.root, "research_state/tracka_vol_fullhist_panel_20261112T201536Z.parquet")
        self._report("tracka_vol_fullhist_panel_build_report_20261112T201536Z", "0" * 64)
        checks = gate.check_panel_and_report(
            self.root, "tracka_vol_fullhist_panel_*.parquet",
            "tracka_vol_fullhist_panel_build_report_*.json", "A3")
        self.assertFalse(checks[-1]["ok"])
        self.assertIn("MISMATCH", checks[-1]["detail"])


class TestEvalCheck(GateTestCase):
    def test_unrecognised_verdict_fails(self):
        self._eval("evaluation_summary_TRACKA-VOL-FULLHIST-20261112T201536Z", "looks_great")
        checks = gate.check_eval_summary(
            self.root, gate.ARM_A_EVAL_GLOB, "A4")
        self.assertFalse(checks[0]["ok"])

    def test_missing_family_cells_flagged(self):
        self._eval("evaluation_summary_TRACKA-VOL-FULLHIST-20261112T201536Z", "NOT_MET",
                   with_family=False)
        checks = gate.check_eval_summary(self.root, gate.ARM_A_EVAL_GLOB, "A4")
        a6 = [c for c in checks if c["check"] == "A6"]
        self.assertEqual(len(a6), 1)
        self.assertFalse(a6[0]["ok"])

    def test_complete_eval_passes_all_three(self):
        self._eval("evaluation_summary_TRACKA-VOL-FULLHIST-20261112T201536Z", "NOT_MET")
        checks = gate.check_eval_summary(self.root, gate.ARM_A_EVAL_GLOB, "A4")
        self.assertTrue(all(c["ok"] for c in checks))
        self.assertEqual({c["check"] for c in checks}, {"A4", "A5", "A6"})


class TestFullGateExitCode(GateTestCase):
    def test_empty_state_is_blocked(self):
        self.assertEqual(gate.main(["--arm", "all", "--root", str(self.root)]), 1)


if __name__ == "__main__":
    unittest.main()