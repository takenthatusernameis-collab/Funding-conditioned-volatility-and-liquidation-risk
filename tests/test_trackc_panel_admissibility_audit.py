
"""Dep-light tests for Track C panel admissibility audit (stdlib, no network, no outcomes)."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.trackc_panel_admissibility_audit import (
    funding_coverage,
    missing_day_ranges,
    month_keys_for_range,
    non_overlapping_30d_blocks,
)


def _mk_series(cache: Path, sym: str, window: str, day: str, series=("markPriceKlines", "indexPriceKlines", "premiumIndexKlines")):
    root = cache / f"{sym}_{window}"
    for s in series:
        d = root / f"{s}-{day}"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{sym}-1h-{day}.csv").write_text("open_time,open\n0,1\n")
    (root / f"{sym}-1h-{day}.zip").write_bytes(b"PK")


class TestPanelAdmissibility(unittest.TestCase):
    def test_blocks(self):
        self.assertEqual(non_overlapping_30d_blocks(0), 0)
        self.assertEqual(non_overlapping_30d_blocks(29), 0)
        self.assertEqual(non_overlapping_30d_blocks(30), 1)
        self.assertEqual(non_overlapping_30d_blocks(89), 2)
        self.assertEqual(non_overlapping_30d_blocks(90), 3)

    def test_missing_day_ranges(self):
        missing, ranges = missing_day_ranges(["2024-01-01", "2024-01-03"], ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"])
        self.assertEqual(missing, ["2024-01-02", "2024-01-04"])
        self.assertEqual(ranges, [["2024-01-02", "2024-01-02"], ["2024-01-04", "2024-01-04"]])

    def test_month_keys_for_range(self):
        self.assertEqual(month_keys_for_range("2024-11-30", "2025-01-02"), ["2024-11", "2024-12", "2025-01"])

    def test_funding_coverage_month_files_present(self):
        with tempfile.TemporaryDirectory() as td:
            cache = Path(td) / "research_state" / "data_cache"
            cache.mkdir(parents=True)
            p = cache / "BTCUSDT_2024_01" / "BTCUSDT-fundingRate-2024-01.csv"
            p.parent.mkdir(parents=True)
            p.write_text("calc_time,funding_interval_hours,last_funding_rate\n1704067200000,8,0.0001\n1704096000000,8,0.0002\n")
            cov = funding_coverage(cache, "BTCUSDT", ["2024-01-01", "2024-01-02", "2024-01-31"])
            self.assertEqual(cov["funding_completeness_flag"], "MONTH_FILES_PRESENT")
            self.assertEqual(cov["funding_csv_files_found"], 1)

    def test_cli_gap_manifest_and_provenance_fields(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as td:
            cache = Path(td) / "cache"
            cache.mkdir()
            _mk_series(cache, "BTCUSDT", "2026_11", "2026-11-01")
            _mk_series(cache, "BTCUSDT", "2026_11", "2026-11-02", series=("markPriceKlines", "premiumIndexKlines"))  # index missing
            out = Path(td) / "r.json"
            cp = subprocess.run(
                [sys.executable, str(root / "scripts/trackc_panel_admissibility_audit.py"),
                 "--cache", str(cache), "--symbols", "BTCUSDT", "--window-hint", "2026_11", "--out", str(out)],
                cwd=root, capture_output=True, text=True, timeout=30)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            r = json.loads(out.read_text())
            self.assertFalse(r["outcomes_computed"])
            self.assertFalse(r["network_used"])
            self.assertFalse(r["resume_trigger_met"])
            gap = r["per_symbol"]["BTCUSDT"]["series_gap_manifest"]["indexPriceKlines"]
            self.assertEqual(gap["missing_days_vs_mark_union"], 1)
            self.assertEqual(gap["missing_day_ranges"], [["2026-11-02", "2026-11-02"]])
            self.assertIn("funding_coverage", r["per_symbol"]["BTCUSDT"])
            self.assertFalse(r["confirmatory_resume_ready"])
            self.assertFalse(r["per_symbol"]["BTCUSDT"]["confirmatory_ready_symbol"])
            self.assertIn("funding_month_files_complete_for_range", r["per_symbol"]["BTCUSDT"])
            self.assertIn("funding_slot_coverage_diagnostic", r["per_symbol"]["BTCUSDT"]["funding_coverage"])
            self.assertIn("provenance_audit", r)
            self.assertIn("sidecar_counts", r["provenance_audit"])
            self.assertIn("adjacent_sha256_verification_sample", r["provenance_audit"])

    def test_cli_multi_hint_or_semantics(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as td:
            cache = Path(td) / "cache"
            cache.mkdir()
            _mk_series(cache, "BTCUSDT", "2024_01", "2024-01-01")
            _mk_series(cache, "BTCUSDT", "2025_06", "2025-06-01")
            out = Path(td) / "r.json"
            cp = subprocess.run(
                [sys.executable, str(root / "scripts/trackc_panel_admissibility_audit.py"),
                 "--cache", str(cache), "--symbols", "BTCUSDT",
                 "--window-hint", "2024_01,2025_06", "--out", str(out)],
                cwd=root, capture_output=True, text=True, timeout=30)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            r = json.loads(out.read_text())
            self.assertEqual(r["per_symbol"]["BTCUSDT"]["days"], 2)
            self.assertEqual(r["per_symbol"]["BTCUSDT"]["range"], ["2024-01-01", "2025-06-01"])
            self.assertEqual(r["window_hints_resolved"], ["2024_01", "2025_06"])

    def test_cli_no_outcomes_no_network_existing_cache(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "r.json"
            cp = subprocess.run(
                [sys.executable, str(root / "scripts/trackc_panel_admissibility_audit.py"),
                 "--cache", str(root / "research_state" / "data_cache"),
                 "--window-hint", "2026_11_nonexistent_window",
                 "--out", str(out)],
                cwd=root, capture_output=True, text=True, timeout=30)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            r = json.loads(out.read_text())
            self.assertFalse(r["outcomes_computed"])
            self.assertFalse(r["network_used"])
            self.assertFalse(r["resume_trigger_met"])
            self.assertIn("resume_trigger_rule", r)


if __name__ == "__main__":
    unittest.main()
