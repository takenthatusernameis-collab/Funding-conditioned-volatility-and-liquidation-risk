"""Tests for scripts/fclr018_gate4_prereg_readiness_matrix.py (read-only, no network)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "fclr018_gate4_prereg_readiness_matrix.py"


def _mk_zip(path: Path, inner_name: str, payload: bytes = b"ok\n"):
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(inner_name, payload)


def build_month(cache: Path, sym: str, ym: str, days, kinds=("klines", "markPriceKlines", "indexPriceKlines", "premiumIndexKlines"), funding=True):
    d = cache / f"{sym}_{ym.replace('-', '_')}"
    d.mkdir(parents=True, exist_ok=True)
    for kind in kinds:
        for day in days:
            kd = d / f"{kind}-{day}"
            kd.mkdir(parents=True, exist_ok=True)
            _mk_zip(kd / f"{sym}-1h-{day}.zip", f"{sym}-1h-{day}.csv")
    if funding:
        _mk_zip(d / f"{sym}-fundingRate-{ym}.zip", f"{sym}-fundingRate-{ym}.csv", b"ts,rate\n1,0.0001\n")
        (d / f"{sym}-fundingRate-{ym}").mkdir(parents=True, exist_ok=True)


def run_script(cache: Path, out_dir: Path, extra=()):
    cmd = [sys.executable, str(SCRIPT), "--cache-root", str(cache), "--out-dir", str(out_dir), "--json-name", "audit.json", "--md-name", "audit.md", *extra]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    doc = json.loads((out_dir / "audit.json").read_text()) if (out_dir / "audit.json").exists() else None
    return p, doc


SYMS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]


class TestFclr018PrereqReadiness(unittest.TestCase):
    def _build_evidenced(self, cache):
        month_days = {
            "2024-04": 30, "2024-05": 31, "2024-06": 30, "2024-07": 31, "2024-08": 31, "2024-09": 30,
        }
        for sym in SYMS:
            for ym, nd in month_days.items():
                build_month(cache, sym, ym, [f"{ym}-{d:02d}" for d in range(1, nd + 1)])

    def test_draft_metadata_and_no_confirmatory(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); cache = root / "cache"; out_dir = root / "out"
            self._build_evidenced(cache)
            p, doc = run_script(cache, out_dir)
            self.assertEqual(p.returncode, 0, p.stderr + p.stdout)
            self.assertEqual(doc["prereg_status"], "DRAFT_NOT_FROZEN")
            self.assertTrue(doc["no_confirmatory_outcomes"])
            self.assertTrue(doc["exploratory_only"])
            self.assertTrue(doc["no_network"])
            self.assertTrue(doc["not_go_for_confirmatory_outcomes"])
            self.assertFalse(doc["decision"]["confirmatory_ready_now"])
            self.assertFalse(doc["draft_prereg_skeleton"]["freeze_promotion_authorized"])
            self.assertTrue(doc["draft_prereg_skeleton"]["not_executable_as_confirmatory"])
            self.assertTrue((out_dir / "fclr018_gate4_prereg_readiness_latest.json").exists())

    def test_evidenced_window_classification_and_v5_blocker(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); cache = root / "cache"; out_dir = root / "out"
            self._build_evidenced(cache)
            p, doc = run_script(cache, out_dir)
            self.assertEqual(p.returncode, 0, p.stderr)
            w = next(x for x in doc["candidate_windows"] if x["window_id"] == "cand_2024_04_09_evidenced")
            self.assertEqual(w["provenance_status"], "IDENTITY_VERIFIED_BOUNDED_FCLR015")
            self.assertTrue(w["block_count_gate_ge_3"])
            self.assertTrue(w["calendar_coverage_all_symbols_complete"])
            self.assertFalse(w["confirmatory_eligible_now"])
            self.assertEqual(w["v5_terms_blocker_state"]["terms_status"], "EXPLICIT_BLOCKER_UNRESOLVED")
            self.assertIn("v5_terms_blocker_unresolved_all_go_false", w["confirmatory_ineligibility_reasons"])
            # even evidenced complete window cannot be confirmatory-now due to v5/fresh-frozen-prereg
            self.assertIn(w["confirmatory_eligibility"], ["INELIGIBLE_EXPLORATORY", "ELIGIBLE_ONLY_IF_FRESH_FROZEN_PREREG_AND_ADMISSIBILITY_GATES_GREEN"])

    def test_unprovenanced_window_is_exploratory(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); cache = root / "cache"; out_dir = root / "out"
            self._build_evidenced(cache)
            for sym in SYMS:
                for ym, nd in [("2024-10", 31), ("2024-11", 30), ("2024-12", 31)]:
                    build_month(cache, sym, ym, [f"{ym}-{d:02d}" for d in range(1, nd + 1)])
            p, doc = run_script(cache, out_dir)
            self.assertEqual(p.returncode, 0, p.stderr)
            w = next(x for x in doc["candidate_windows"] if x["window_id"] == "cand_2024_10_12_local_exploratory")
            self.assertEqual(w["provenance_status"], "UNVERIFIED")
            self.assertEqual(w["confirmatory_eligibility"], "INELIGIBLE_EXPLORATORY")
            self.assertFalse(w["confirmatory_eligible_now"])
            self.assertIn("provenance_not_identity_verified_bounded_fclr015", w["confirmatory_ineligibility_reasons"])

    def test_block_count_math_and_coverage_ineligibility(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); cache = root / "cache"; out_dir = root / "out"
            # partial coverage only: evidenced window span is fixed (183d => 5 blocks by math)
            # but incomplete calendar coverage must force confirmatory ineligibility.
            for sym in SYMS:
                build_month(cache, sym, "2024-04", [f"2024-04-{d:02d}" for d in range(1, 31)])
            p, doc = run_script(cache, out_dir)
            self.assertEqual(p.returncode, 0, p.stderr)
            w = next(x for x in doc["candidate_windows"] if x["window_id"] == "cand_2024_04_09_evidenced")
            self.assertFalse(w["calendar_coverage_all_symbols_complete"])
            self.assertEqual(w["max_non_overlapping_30d_blocks_with_7d_purge"], 5)
            self.assertTrue(w["block_count_gate_ge_3"])
            self.assertFalse(w["confirmatory_eligible_now"])
            self.assertIn("calendar_coverage_incomplete_or_unverified", w["confirmatory_ineligibility_reasons"])

    def test_module_block_math_and_provenance(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location("fclr018", SCRIPT)
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
        self.assertEqual(mod.max_non_overlapping_blocks(183, 30, 7), 5)  # 30 + (7+30)*4 = 178 <= 183
        self.assertEqual(mod.max_non_overlapping_blocks(90, 30, 7), 2)
        self.assertEqual(mod.provenance_status_for_window("2024-04-01", "2024-09-30"), "IDENTITY_VERIFIED_BOUNDED_FCLR015")
        self.assertEqual(mod.provenance_status_for_window("2024-10-01", "2024-12-31"), "UNVERIFIED")
        self.assertEqual(mod.provenance_status_for_window("2024-04-01", "2024-12-31"), "UNVERIFIED")


if __name__ == "__main__":
    unittest.main()
