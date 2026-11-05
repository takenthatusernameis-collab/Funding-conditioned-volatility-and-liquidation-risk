#!/usr/bin/env python3
"""FCLR-NEXT-097: monitor network-isolation proofs for state-only/cached verify paths.

Deterministic (tmp dirs, mocks/patches): prove state-only/cached verify/decision
paths do not perform network calls and do not mutate real research_state.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))
import scripts.monitor_ironflow_liquidations as mon

REPO_RS = Path(mon.__file__).resolve().parent.parent / "research_state"


def _snapshot_real_rs():
    return {
        "probe_files": sorted(p.name for p in REPO_RS.glob("ironflow_probe_*.json")),
        "probe_mtimes": {p.name: p.stat().st_mtime_ns for p in REPO_RS.glob("ironflow_probe_*.json")},
        "root_count": len(list(REPO_RS.glob("*.md"))) + len(list(REPO_RS.glob("*.json"))),
    }


class TestMonitorNetworkIsolation097(unittest.TestCase):
    def _minimal_state(self):
        return {
            "data_through": "2026-10",
            "known_available_months": {"events": ["2026-10"], "fills": ["2026-10"]},
            "tree_parquet_items": [{"kind": "events", "path": "data/events/2026-10.parquet", "oid": "abc", "size": 1}],
            "baseline_tree_oid": "treeoid",
            "last_quick_check": {"triggered": False, "months_probed": ["2026-11"], "head_probes": 0, "get_requests": 0},
            "last_quick_probe": {"probes": [{"month": "2026-11", "kind": "events", "status": 404}]},
            "last_tree_change": {"changed": False, "added": []},
            "last_probe": {"new_files_found": []},
        }

    def test_verify_state_pure_no_network(self):
        with patch.object(mon, "http_get", side_effect=AssertionError("network")) as g, \
             patch.object(mon, "head_probe", side_effect=AssertionError("network")) as h, \
             patch.object(mon, "resolve_get", side_effect=AssertionError("network")) as rg, \
             patch.object(mon, "check_resume_condition", side_effect=AssertionError("network")) as crc:
            r = mon.verify_state(self._minimal_state())
        self.assertIsInstance(r, dict)
        g.assert_not_called(); h.assert_not_called(); rg.assert_not_called(); crc.assert_not_called()

    def test_check_baseline_drift_state_only_no_network(self):
        with patch.object(mon, "http_get", side_effect=AssertionError("network")) as g, \
             patch.object(mon, "head_probe", side_effect=AssertionError("network")) as h, \
             patch.object(mon, "resolve_get", side_effect=AssertionError("network")) as rg:
            r = mon.check_baseline_drift(self._minimal_state())
        self.assertIn("drifted", r)
        g.assert_not_called(); h.assert_not_called(); rg.assert_not_called()

    def test_evaluate_resume_decision_state_only_no_network(self):
        with patch.object(mon, "http_get", side_effect=AssertionError("network")) as g, \
             patch.object(mon, "head_probe", side_effect=AssertionError("network")) as h, \
             patch.object(mon, "check_resume_condition", side_effect=AssertionError("network")) as crc:
            r = mon.evaluate_resume_decision(self._minimal_state(), rc={"triggered": False, "probe_diff": {"summary": {"changed_count": 0}}}, tree_change={"changed": False, "added": []}, new_files=[])
        self.assertIn("new_data_path", r)
        g.assert_not_called(); h.assert_not_called(); crc.assert_not_called()

    def test_simulate_resume_no_network(self):
        with patch.object(mon, "http_get", side_effect=AssertionError("network")) as g, \
             patch.object(mon, "head_probe", side_effect=AssertionError("network")) as h, \
             patch.object(mon, "check_resume_condition", side_effect=AssertionError("network")) as crc:
            r = mon.simulate_resume(self._minimal_state())
        self.assertIn("triggered", r)
        g.assert_not_called(); h.assert_not_called(); crc.assert_not_called()

    def test_main_verify_cli_isolated_no_network_no_real_rs_mutation(self):
        before = _snapshot_real_rs()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            state = self._minimal_state()
            (td / "state.json").write_text(json.dumps(state))
            orig_e, orig_s = mon.EVIDENCE_DIR, mon.STATE_PATH
            orig_argv = sys.argv
            try:
                mon.EVIDENCE_DIR = td
                mon.STATE_PATH = td / "state.json"
                sys.argv = ["monitor_ironflow_liquidations.py", "--verify"]
                with patch.object(mon, "http_get", side_effect=AssertionError("network")), \
                     patch.object(mon, "head_probe", side_effect=AssertionError("network")), \
                     patch.object(mon, "resolve_get", side_effect=AssertionError("network")), \
                     patch.object(mon, "check_resume_condition", side_effect=AssertionError("network")), \
                     patch.object(mon, "check_baseline_drift_probe", side_effect=AssertionError("network")):
                    try:
                        mon.main()
                    except SystemExit:
                        pass
            finally:
                mon.EVIDENCE_DIR, mon.STATE_PATH = orig_e, orig_s
                sys.argv = orig_argv
            self.assertEqual(list(td.glob("ironflow_probe_*.json")), [], "verify wrote probe artifacts to tmp evidence dir")
        after = _snapshot_real_rs()
        self.assertEqual(before, after)

    def test_main_decision_cli_isolated_no_network_no_real_rs_mutation(self):
        before = _snapshot_real_rs()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "state.json").write_text(json.dumps(self._minimal_state()))
            orig_e, orig_s = mon.EVIDENCE_DIR, mon.STATE_PATH
            orig_argv = sys.argv
            try:
                mon.EVIDENCE_DIR = td
                mon.STATE_PATH = td / "state.json"
                sys.argv = ["monitor_ironflow_liquidations.py", "--decision"]
                with patch.object(mon, "http_get", side_effect=AssertionError("network")), \
                     patch.object(mon, "head_probe", side_effect=AssertionError("network")), \
                     patch.object(mon, "check_resume_condition", side_effect=AssertionError("network")):
                    try:
                        mon.main()
                    except SystemExit:
                        pass
            finally:
                mon.EVIDENCE_DIR, mon.STATE_PATH = orig_e, orig_s
                sys.argv = orig_argv
            self.assertEqual(list(td.glob("ironflow_probe_*.json")), [])
        after = _snapshot_real_rs()
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
