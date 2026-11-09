"""Dep-light tests for Track C panel admissibility audit (stdlib, no network, no outcomes)."""
import json, os, subprocess, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.trackc_panel_admissibility_audit import non_overlapping_30d_blocks


class TestPanelAdmissibility(unittest.TestCase):
    def test_blocks(self):
        self.assertEqual(non_overlapping_30d_blocks(0), 0)
        self.assertEqual(non_overlapping_30d_blocks(29), 0)
        self.assertEqual(non_overlapping_30d_blocks(30), 1)
        self.assertEqual(non_overlapping_30d_blocks(89), 2)
        self.assertEqual(non_overlapping_30d_blocks(90), 3)

    def test_cli_no_outcomes_no_network(self):
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
