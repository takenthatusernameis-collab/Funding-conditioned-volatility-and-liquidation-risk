#!/usr/bin/env python3
"""FCLR-NEXT-102: wire drift preflight into tracka_resume_gate + runtime consolidation assert.

All deterministic, no network, tmp-only. No real research_state mutation.
"""
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.fclr010_harness import FCLR010Harness
from scripts.tracka_resume_check import _valid_go, _valid_strict_manifest_go, drift_preflight
import scripts.tracka_resume_gate as tracka_resume_gate
import scripts.monitor_ironflow_liquidations as mon

REPO_RS = Path(__file__).resolve().parent.parent / "research_state"


def _snapshot_real_rs():
    return {
        "probe_files": sorted(p.name for p in REPO_RS.glob("ironflow_probe_*.json")),
        "root_count": len(list(REPO_RS.glob("*.md"))) + len(list(REPO_RS.glob("*.json"))),
    }


def _mk_valid_rs(rs: Path):
    rs.mkdir(parents=True, exist_ok=True)
    (rs / "watch").mkdir(exist_ok=True)
    (rs / "ironflow_probe_20990101T000000Z.json").write_text(json.dumps({"probe_id": "ironflow_probe_20990101T000000Z"}))
    (rs / "ironflow_probe_digest_latest.json").write_text(json.dumps({"latest_probe": "ironflow_probe_20990101T000000Z.json", "entries": []}))
    (rs / "alt_source_scan_latest.json").write_text("{}")
    (rs / "alt_source_deep_review_latest.md").write_text("# ok\n")
    (rs / "watch" / "trigger_harden_20261104T113550Z.json").write_text("{}")
    (rs / "experiment_frontier.json").write_text("{}")
    return rs


def _mk_repo(root: Path):
    root.mkdir(parents=True, exist_ok=True)
    (root / "AGENT_HANDOFF.md").write_text("# handoff\n")
    return root


class TestGateDriftPreflightBundled102(unittest.TestCase):
    def setUp(self):
        self.h = FCLR010Harness()

    def test_gate_blocks_on_drift_before_prereg_manifest_decision(self):
        before = _snapshot_real_rs()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo")
            rs = _mk_valid_rs(td / "rs")
            (rs / "ironflow_probe_20990102T000000Z.json").write_text("{}")  # drift: extra probe
            res = tracka_resume_gate.decide("/nonexistent_tracka_resume", str(td), None,
                                           source_manifest=_valid_strict_manifest_go(),
                                           repo_root=root, research_state_dir=rs, harness_repo_root=Path(__file__).resolve().parent.parent)
            self.assertEqual(res["status"], "BLOCKED")
            self.assertFalse(res.get("outcomes_inspected", True))
            self.assertIn("drift preflight", res.get("reason", "").lower())
            self.assertIn("drift_preflight", res)
            self.assertFalse(res["drift_preflight"]["pass"])
            self.assertFalse(res["network"])
            self.assertFalse(res["writes_real_research_state"])
        self.assertEqual(before, _snapshot_real_rs())

    def test_gate_exposes_drift_preflight_pass_on_valid_state(self):
        before = _snapshot_real_rs()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo")
            rs = _mk_valid_rs(td / "rs")
            res = tracka_resume_gate.decide("/nonexistent_tracka_resume", str(td), None,
                                           source_manifest=_valid_strict_manifest_go(),
                                           repo_root=root, research_state_dir=rs, harness_repo_root=Path(__file__).resolve().parent.parent)
            self.assertEqual(res["status"], "BLOCKED")  # prereg missing (after drift passes)
            self.assertTrue(res["drift_preflight"]["pass"])
            self.assertIn("probe_count_exactly_two", res["drift_preflight"]["checks"])
            self.assertFalse(res.get("outcomes_inspected", True))
            self.assertTrue(res.get("prereg_required") or "prereg" in str(res.get("reason", "")).lower())
        self.assertEqual(before, _snapshot_real_rs())

    def test_gate_drift_preflight_under_5s_and_no_network(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo")
            rs = _mk_valid_rs(td / "rs")
            res = tracka_resume_gate.decide("/nonexistent_tracka_resume", str(td), None,
                                           source_manifest=_valid_strict_manifest_go(),
                                           repo_root=root, research_state_dir=rs, harness_repo_root=Path(__file__).resolve().parent.parent)
            self.assertLess(res.get("elapsed_s", 999), 5.0)
            self.assertFalse(res["network"])
            self.assertFalse(res["drift_preflight"].get("network", True) is not False and res["drift_preflight"].get("pass") is True)

    def test_gate_preserves_strict_prereg_and_compat_semantics(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo")
            rs = _mk_valid_rs(td / "rs")
            prereg = self.h.pre_register_forward_experiment(td)
            data = td / "hl_2026_11"; data.mkdir()
            # strict + full manifest => READY
            res = tracka_resume_gate.decide(str(data), str(td), str(prereg),
                                           source_manifest=_valid_strict_manifest_go(),
                                           compat_fixture=False, repo_root=root, research_state_dir=rs, harness_repo_root=Path(__file__).resolve().parent.parent)
            self.assertEqual(res["status"], "READY_FROZEN")
            self.assertTrue(res["drift_preflight"]["pass"])
            self.assertFalse(res.get("outcomes_inspected", True))
            # compat + minimal manifest still accepted as before
            res2 = tracka_resume_gate.decide(str(data), str(td), str(prereg),
                                            source_manifest=_valid_go(),
                                            compat_fixture=True, repo_root=root, research_state_dir=rs, harness_repo_root=Path(__file__).resolve().parent.parent)
            self.assertEqual(res2["status"], "READY_FROZEN")
            self.assertTrue(res2["compat_fixture"])

    def test_gate_default_real_repo_drift_preflight_passes(self):
        # real repo must be clean per invariants (entry verified)
        res = tracka_resume_gate.decide("/nonexistent_tracka_resume", None, None,
                                       source_manifest=_valid_strict_manifest_go())
        self.assertIn("drift_preflight", res)
        self.assertTrue(res["drift_preflight"]["pass"], res["drift_preflight"])
        self.assertEqual(res["status"], "BLOCKED")  # prereg/path checks follow

    def test_skip_drift_preflight_flag_only_for_controlled_tests(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo")
            rs = _mk_valid_rs(td / "rs")
            (rs / "ironflow_probe_20990102T000000Z.json").write_text("{}")  # drift exists
            res = tracka_resume_gate.decide("/nonexistent_tracka_resume", str(td), None,
                                           source_manifest=_valid_strict_manifest_go(),
                                           repo_root=root, research_state_dir=rs,
                                           skip_drift_preflight=True)
            self.assertTrue(res["drift_preflight"].get("skipped"))
            # blocked later (prereg) not by drift
            self.assertNotIn("drift preflight", res.get("reason", "").lower())


class TestMonitorRuntimeInvariantAssert102(unittest.TestCase):
    def _mk_probe(self, ev_dir: Path, name: str, ts_off: float):
        p = ev_dir / name
        p.write_text(json.dumps({"probe_id": name.replace(".json", ""), "data_through": "2026-10"}))
        os.utime(p, (time.time() + ts_off, time.time() + ts_off))
        return p

    def test_assert_probe_invariant_passes_on_valid_state(self):
        with tempfile.TemporaryDirectory() as td:
            ev = Path(td)
            self._mk_probe(ev, "ironflow_probe_20990101T000001Z.json", 1)
            (ev / "ironflow_probe_digest_latest.json").write_text("{}")
            r = mon.assert_probe_invariant(ev, raise_on_violation=True)
            self.assertTrue(r["pass"])
            self.assertEqual(r["total"], 2)

    def test_assert_probe_invariant_fails_closed_on_drift(self):
        with tempfile.TemporaryDirectory() as td:
            ev = Path(td)
            self._mk_probe(ev, "ironflow_probe_20990101T000001Z.json", 1)
            self._mk_probe(ev, "ironflow_probe_20990101T000002Z.json", 2)
            (ev / "ironflow_probe_digest_latest.json").write_text("{}")
            with self.assertRaises(ValueError):
                mon.assert_probe_invariant(ev, raise_on_violation=True)
            r = mon.assert_probe_invariant(ev, raise_on_violation=False)
            self.assertFalse(r["pass"])

    def test_assert_probe_invariant_fails_closed_missing_digest(self):
        with tempfile.TemporaryDirectory() as td:
            ev = Path(td)
            self._mk_probe(ev, "ironflow_probe_20990101T000001Z.json", 1)
            r = mon.assert_probe_invariant(ev, raise_on_violation=False)
            self.assertFalse(r["pass"])

    def test_consolidation_then_assert_runtime_invariant(self):
        with tempfile.TemporaryDirectory() as td:
            ev = Path(td)
            self._mk_probe(ev, "ironflow_probe_20990101T000001Z.json", 1)
            self._mk_probe(ev, "ironflow_probe_20990101T000002Z.json", 2)
            self._mk_probe(ev, "ironflow_probe_20990101T000003Z.json", 3)
            old = mon.EVIDENCE_DIR
            try:
                mon.EVIDENCE_DIR = ev
                mon._consolidate_ironflow_probes()
                r = mon.assert_probe_invariant(ev, raise_on_violation=True)
                self.assertTrue(r["pass"])
                self.assertEqual(r["live_probes"], ["ironflow_probe_20990101T000003Z.json"])
                # idempotent + invariant holds
                mon._consolidate_ironflow_probes()
                self.assertTrue(mon.assert_probe_invariant(ev, raise_on_violation=True)["pass"])
            finally:
                mon.EVIDENCE_DIR = old

    def test_drift_preflight_helper_read_only(self):
        before = _snapshot_real_rs()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo")
            rs = _mk_valid_rs(td / "rs")
            p = drift_preflight(root, rs)
            self.assertTrue(p["pass"])
            self.assertFalse(p["network"])
            self.assertTrue(p["read_only"])
        self.assertEqual(before, _snapshot_real_rs())


if __name__ == "__main__":
    unittest.main()
