"""Dep-light tests for Track C gap repair manifest (stdlib, no network, no outcomes)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.trackc_gap_repair_manifest import _funding_local, build_manifest


class TestGapRepairManifest(unittest.TestCase):
    def _audit(self, **over):
        base = {
            "generated_utc": "2026-11-09T00:00:00Z",
            "window_hint": "2026_11",
            "resume_trigger_met": False,
            "confirmatory_resume_ready": False,
            "symbols": ["BTCUSDT"],
            "per_symbol": {
                "BTCUSDT": {
                    "range": ["2026-11-01", "2026-11-08"],
                    "days": 8,
                    "required_series_complete": False,
                    "resume_trigger_symbol_ok": False,
                    "confirmatory_ready_symbol": False,
                    "series_gap_manifest": {
                        "indexPriceKlines": {"complete_vs_mark_union": False, "missing_days_vs_mark_union": 1, "missing_day_ranges": [["2026-11-02", "2026-11-02"]], "missing_days_sample": ["2026-11-02"]},
                        "markPriceKlines": {"complete_vs_mark_union": True, "missing_days_vs_mark_union": 0, "missing_day_ranges": [], "missing_days_sample": []},
                        "premiumIndexKlines": {"complete_vs_mark_union": True, "missing_days_vs_mark_union": 0, "missing_day_ranges": [], "missing_days_sample": []},
                    },
                    "funding_coverage": {
                        "funding_completeness_flag": "NO_MONTH_FILES_FOR_RANGE",
                        "funding_months_expected_for_range": ["2026-11"],
                        "funding_months_overlap_expected": [],
                        "funding_note": "note",
                    },
                }
            },
        }
        base.update(over)
        return base

    def test_build_manifest_reports_gaps(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "cache"
            (cache / "BTCUSDT_2026_11" / "indexPriceKlines-1h-2026-11-02").mkdir(parents=True)
            (cache / "BTCUSDT_2026_11" / "indexPriceKlines-1h-2026-11-02" / "BTCUSDT-1h-2026-11-02.csv").write_text("x\n")
            audit = td / "audit.json"
            audit.write_text(json.dumps(self._audit()))
            m = build_manifest(audit, cache, td)
            self.assertFalse(m["summary"]["outcomes_computed"])
            self.assertFalse(m["summary"]["network_used"])
            self.assertTrue(m["summary"]["any_required_series_gaps"])
            self.assertEqual(m["summary"]["funding_months_missing_union"], ["2026-11"])
            btc = m["per_symbol"]["BTCUSDT"]
            self.assertIn("REQUIRED_SERIES_GAPS_VS_MARK_UNION", btc["blockers"])
            self.assertIn("FUNDING_MONTH_FILES_MISSING_FOR_RANGE", btc["blockers"])
            sample = btc["series_repair_plan"]["indexPriceKlines"]["range_local_presence_samples"][0]["sample_day_presence"]
            self.assertTrue(sample["local_files_present"])

    def test_funding_local_detects_existing_month_file(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "cache"
            p = cache / "BTCUSDT_2024_01" / "BTCUSDT-fundingRate-2024-01.csv"
            p.parent.mkdir(parents=True)
            p.write_text("calc_time\n")
            Path(str(p) + ".sha256").write_text("abc  x\n")
            r = _funding_local(cache, td, "BTCUSDT", ["2024-01"])
            self.assertTrue(r["2024-01"]["local_present"])
            self.assertEqual(len(r["2024-01"]["adjacent_sha256_sidecars_found"]), 1)

    def test_cli_on_existing_audits(self):
        root = Path(__file__).resolve().parents[1]
        latest = root / "research_state/trackc_panel_admissibility_latest.json"
        if not latest.exists():
            self.skipTest("latest audit not present")
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "repair.json"
            cp = subprocess.run(
                [sys.executable, str(root / "scripts/trackc_gap_repair_manifest.py"),
                 "--audit", str(latest), "--repo-root", str(root), "--out", str(out)],
                cwd=root, capture_output=True, text=True, timeout=60)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            r = json.loads(out.read_text())
            self.assertFalse(r["summary"]["network_used"])
            self.assertFalse(r["summary"]["outcomes_computed"])
            self.assertIn("2026-11", r["summary"]["funding_months_missing_union"])


if __name__ == "__main__":
    unittest.main()
