#!/usr/bin/env python3
"""FCLR-NEXT-103: gate reason-code/order hardening + monitor quick-evidence field proof.
Deterministic, no network, tmp-only. No real research_state mutation.
"""
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.fclr010_harness import FCLR010Harness
from scripts.tracka_resume_check import _valid_go, _valid_strict_manifest_go
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
    (rs / "ironflow_probe_digest_latest.json").write_text(json.dumps({"latest_probe": "ironflow_probe_20990101T000000Z.json"}))
    (rs / "alt_source_scan_latest.json").write_text("{}")
    (rs / "alt_source_deep_review_latest.md").write_text("# ok\n")
    (rs / "watch" / "trigger_harden_20261104T113550Z.json").write_text("{}")
    (rs / "experiment_frontier.json").write_text("{}")
    return rs


def _mk_repo(root: Path):
    root.mkdir(parents=True, exist_ok=True)
    (root / "AGENT_HANDOFF.md").write_text("# handoff\n")
    return root


class TestGateReasonCodeOrder103(unittest.TestCase):
    def setUp(self):
        self.h = FCLR010Harness()

    def test_drift_fail_has_stable_reason_and_order_before_prereg(self):
        before = _snapshot_real_rs()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td); root = _mk_repo(td / "repo"); rs = _mk_valid_rs(td / "rs")
            (rs / "ironflow_probe_20990102T000000Z.json").write_text("{}")
            res = tracka_resume_gate.decide("/nonexistent_tracka_resume", str(td), None,
                                           source_manifest=_valid_strict_manifest_go(),
                                           repo_root=root, research_state_dir=rs,
                                           harness_repo_root=Path(__file__).resolve().parent.parent)
            self.assertEqual(res["status"], "BLOCKED")
            self.assertEqual(res.get("reason_code"), "DRIFT_PREFLIGHT_FAIL_BEFORE_PREREG")
            self.assertEqual(res.get("fail_closed_order"), "drift_preflight->manifest_prereg")
            self.assertFalse(res["drift_preflight"]["pass"])
            self.assertFalse(res.get("outcomes_inspected", True))
        self.assertEqual(before, _snapshot_real_rs())

    def test_prereg_block_after_drift_pass_has_stable_reason(self):
        before = _snapshot_real_rs()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td); root = _mk_repo(td / "repo"); rs = _mk_valid_rs(td / "rs")
            res = tracka_resume_gate.decide("/nonexistent_tracka_resume", str(td), None,
                                           source_manifest=_valid_strict_manifest_go(),
                                           repo_root=root, research_state_dir=rs,
                                           harness_repo_root=Path(__file__).resolve().parent.parent)
            self.assertEqual(res["status"], "BLOCKED")
            self.assertTrue(res["drift_preflight"]["pass"])
            self.assertEqual(res.get("reason_code"), "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")
            self.assertEqual(res.get("fail_closed_order"), "drift_preflight->manifest_prereg")
            self.assertFalse(res.get("outcomes_inspected", True))
        self.assertEqual(before, _snapshot_real_rs())

    def test_ready_after_drift_pass_has_stable_reason_and_semantics_preserved(self):
        before = _snapshot_real_rs()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td); root = _mk_repo(td / "repo"); rs = _mk_valid_rs(td / "rs")
            prereg = self.h.pre_register_forward_experiment(td)
            data = td / "hl"; data.mkdir()
            res = tracka_resume_gate.decide(str(data), str(td), str(prereg),
                                           source_manifest=_valid_strict_manifest_go(),
                                           compat_fixture=False, repo_root=root, research_state_dir=rs,
                                           harness_repo_root=Path(__file__).resolve().parent.parent)
            self.assertEqual(res["status"], "READY_FROZEN")
            self.assertTrue(res["drift_preflight"]["pass"])
            self.assertEqual(res.get("reason_code"), "RESUME_READY_AFTER_DRIFT_PASS")
            self.assertEqual(res.get("fail_closed_order"), "drift_preflight->manifest_prereg")
            self.assertFalse(res.get("outcomes_inspected", True))
        self.assertEqual(before, _snapshot_real_rs())

    def test_real_repo_prereg_block_reason_code(self):
        res = tracka_resume_gate.decide("/nonexistent_tracka_resume", None, None,
                                       source_manifest=_valid_strict_manifest_go())
        self.assertTrue(res["drift_preflight"]["pass"], res["drift_preflight"])
        self.assertEqual(res["status"], "BLOCKED")
        self.assertEqual(res.get("reason_code"), "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")


class TestMonitorQuickEvidenceField103(unittest.TestCase):
    def test_assert_probe_invariant_result_shape_for_evidence(self):
        # deterministic proof of field shape used by quick path evidence (no network)
        with tempfile.TemporaryDirectory() as td:
            ev = Path(td)
            p = ev / "ironflow_probe_20990101T000001Z.json"
            p.write_text(json.dumps({"probe_id": "ironflow_probe_20990101T000001Z"}))
            os.utime(p, (time.time()+1, time.time()+1))
            (ev / "ironflow_probe_digest_latest.json").write_text("{}")
            r = mon.assert_probe_invariant(ev, raise_on_violation=True)
            self.assertTrue(r["pass"])
            self.assertEqual(r["total"], 2)
            evidence = {"probe_invariant_runtime": r}
            self.assertIn("probe_invariant_runtime", evidence)
            self.assertTrue(evidence["probe_invariant_runtime"]["pass"])

    def test_violation_evidence_field_shape(self):
        with tempfile.TemporaryDirectory() as td:
            ev = Path(td)
            p = ev / "ironflow_probe_20990101T000001Z.json"
            p.write_text("{}"); os.utime(p, (time.time()+1, time.time()+1))
            # missing digest => fail
            r = mon.assert_probe_invariant(ev, raise_on_violation=False)
            evidence = {"probe_invariant_runtime": r}
            self.assertFalse(evidence["probe_invariant_runtime"]["pass"])
            self.assertFalse(evidence["probe_invariant_runtime"]["pass"])
            self.assertIn("total", evidence["probe_invariant_runtime"])
            self.assertIn("invariant", evidence["probe_invariant_runtime"])


if __name__ == "__main__":
    unittest.main()
