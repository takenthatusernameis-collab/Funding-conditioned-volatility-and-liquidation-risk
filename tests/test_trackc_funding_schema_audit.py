"""Dep-light tests for Track C funding schema/provenance checklist audit."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.trackc_funding_schema_audit import audit_file, find_funding_file


class TestFundingSchemaAudit(unittest.TestCase):
    def test_finds_and_audits_valid_file(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "research_state" / "data_cache" / "BTCUSDT_2024_01"
            cache.mkdir(parents=True)
            p = cache / "BTCUSDT-fundingRate-2024-01.csv"
            p.write_text("calc_time,funding_interval_hours,last_funding_rate\n1704067200000,8,0.0001\n1704096000000,8,0.0002\n")
            found = find_funding_file(td, td / "research_state" / "data_cache", "BTCUSDT", "2024-01")
            self.assertEqual(len(found), 1)
            a = audit_file(found[0], "2024-01")
            self.assertTrue(a["schema_ok"])
            self.assertEqual(a["row_count"], 2)
            self.assertFalse(a["provenance_verified"])
            self.assertIn("sha256", a)

    def test_missing_file_via_cli(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "funding_audit.json"
            cp = subprocess.run(
                [sys.executable, str(root / "scripts/trackc_funding_schema_audit.py"),
                 "--repo-root", str(root), "--months", "2099-01", "--symbols", "BTCUSDT", "--out", str(out)],
                cwd=root, capture_output=True, text=True, timeout=60)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            r = json.loads(out.read_text())
            self.assertFalse(r["summary"]["network_used"])
            self.assertFalse(r["summary"]["outcomes_computed"])
            self.assertFalse(r["summary"]["confirmatory_resume_ready"])
            self.assertIn("BTCUSDT:2099-01", r["summary"]["missing_symbol_months"])

    def test_cli_existing_repo_month(self):
        root = Path(__file__).resolve().parents[1]
        if not (root / "BTCUSDT-fundingRate-2024-01" / "BTCUSDT-fundingRate-2024-01.csv").exists():
            self.skipTest("local funding fixture missing")
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "funding_audit.json"
            cp = subprocess.run(
                [sys.executable, str(root / "scripts/trackc_funding_schema_audit.py"),
                 "--repo-root", str(root), "--months", "2024-01", "--symbols", "BTCUSDT,ETHUSDT", "--out", str(out)],
                cwd=root, capture_output=True, text=True, timeout=60)
            self.assertEqual(cp.returncode, 0, cp.stderr + cp.stdout)
            r = json.loads(out.read_text())
            self.assertFalse(r["summary"]["network_used"])
            self.assertTrue(r["per_symbol"]["BTCUSDT"]["months"]["2024-01"]["local_present"])
            self.assertTrue(r["per_symbol"]["BTCUSDT"]["months"]["2024-01"]["schema_ok"])


if __name__ == "__main__":
    unittest.main()
