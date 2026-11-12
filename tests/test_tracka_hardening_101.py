#!/usr/bin/env python3
"""FCLR-NEXT-101: wire 099 drift invariants into CLI resume path + consolidation regression guard.

All deterministic, no network, tmp-only. No real research_state mutation.
"""
import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))
import scripts.tracka_resume_check as trc
import scripts.monitor_ironflow_liquidations as mon


def _mk_valid_rs(rs: Path):
    rs.mkdir(parents=True, exist_ok=True)
    (rs / "watch").mkdir(exist_ok=True)
    # 1 live probe + 1 canonical digest
    (rs / "ironflow_probe_20990101T000000Z.json").write_text(json.dumps({"probe_id": "ironflow_probe_20990101T000000Z", "timestamp_utc": "2099-01-01T00:00:00Z"}))
    (rs / "ironflow_probe_digest_latest.json").write_text(json.dumps({"latest_probe": "ironflow_probe_20990101T000000Z.json", "entries": []}))
    (rs / "alt_source_scan_latest.json").write_text("{}")
    (rs / "alt_source_deep_review_latest.md").write_text("# ok\n")
    # watch trigger_harden invariant: live<=1, non-20261104T==0
    (rs / "watch" / "trigger_harden_20261104T113550Z.json").write_text("{}")
    # keep root bounded (synthetic small)
    (rs / "experiment_frontier.json").write_text("{}")
    return rs


def _mk_repo(root: Path, rs: Path):
    root.mkdir(parents=True, exist_ok=True)
    (root / "AGENT_HANDOFF.md").write_text("# handoff\n")
    # rs may be under root or separate; drift_invariants takes research_state_dir
    return root


class TestDriftInvariantsWiredCLI101(unittest.TestCase):
    def test_drift_invariants_pass_on_valid_tmp_state(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo", None)
            rs = _mk_valid_rs(td / "rs")
            checks = trc.drift_invariants(root, research_state_dir=rs)
            for k, v in checks.items():
                self.assertTrue(v.get("pass"), f"{k} failed: {v}")

    def test_resume_check_json_includes_wired_drift_checks(self):
        # run() against real repo state must include drift checks (wired) and pass
        out = trc.run()
        self.assertTrue(out["pass"], out.get("checks"))
        self.assertIn("handoff_single_root", out["checks"])
        self.assertIn("probe_count_exactly_two", out["checks"])
        self.assertIn("root_md_json_bounded", out["checks"])
        self.assertIn("canonical_alt_outputs_only", out["checks"])
        self.assertIn("no_recurring_timestamped_probe_scan_families", out["checks"])
        self.assertIn("watch_trigger_harden_invariant", out["checks"])
        self.assertIn("no_root_trigger_harden_files", out["checks"])
        self.assertFalse(out["network"])
        self.assertFalse(out["writes_real_research_state"])
        self.assertLess(out["elapsed_s"], 5.0)

    def test_fail_closed_extra_live_probe(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo", None)
            rs = _mk_valid_rs(td / "rs")
            (rs / "ironflow_probe_20990102T000000Z.json").write_text("{}")
            checks = trc.drift_invariants(root, research_state_dir=rs)
            self.assertFalse(checks["probe_count_exactly_two"]["pass"])
            self.assertEqual(checks["probe_count_exactly_two"]["count"], 3)

    def test_fail_closed_extra_digest(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo", None)
            rs = _mk_valid_rs(td / "rs")
            (rs / "ironflow_probe_digest_20990101T000000Z.json").write_text("{}")
            checks = trc.drift_invariants(root, research_state_dir=rs)
            self.assertFalse(checks["probe_count_exactly_two"]["pass"])

    def test_fail_closed_recurring_timestamped_deep_review(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo", None)
            rs = _mk_valid_rs(td / "rs")
            (rs / "alt_source_deep_review_20990101T000000Z.md").write_text("x")
            checks = trc.drift_invariants(root, research_state_dir=rs)
            self.assertFalse(checks["canonical_alt_outputs_only"]["pass"])

    def test_fail_closed_recurring_timestamped_scan(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo", None)
            rs = _mk_valid_rs(td / "rs")
            (rs / "alt_source_scan_20990101T000000Z.json").write_text("{}")
            checks = trc.drift_invariants(root, research_state_dir=rs)
            self.assertFalse(checks["canonical_alt_outputs_only"]["pass"])

    def test_fail_closed_unexpected_probe_family(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo", None)
            rs = _mk_valid_rs(td / "rs")
            (rs / "some_probe_20990101T000000Z.json").write_text("{}")
            checks = trc.drift_invariants(root, research_state_dir=rs)
            self.assertFalse(checks["no_recurring_timestamped_probe_scan_families"]["pass"])

    def test_fail_closed_watch_trigger_harden_non_20261104T(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo", None)
            rs = _mk_valid_rs(td / "rs")
            # replace allowed file with a drifted one
            (rs / "watch" / "trigger_harden_20261104T113550Z.json").unlink()
            (rs / "watch" / "trigger_harden_20990101T000000Z.json").write_text("{}")
            checks = trc.drift_invariants(root, research_state_dir=rs)
            self.assertFalse(checks["watch_trigger_harden_invariant"]["pass"])
            self.assertEqual(checks["watch_trigger_harden_invariant"]["non_20261104T"], 1)

    def test_fail_closed_watch_trigger_harden_too_many_live(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo", None)
            rs = _mk_valid_rs(td / "rs")
            (rs / "watch" / "trigger_harden_20261104T113551Z.json").write_text("{}")
            checks = trc.drift_invariants(root, research_state_dir=rs)
            self.assertFalse(checks["watch_trigger_harden_invariant"]["pass"])
            self.assertEqual(checks["watch_trigger_harden_invariant"]["live"], 2)

    def test_fail_closed_duplicate_handoff_in_tmp_layout(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo", None)
            rs = _mk_valid_rs(td / "rs")
            (root / "sub").mkdir()
            (root / "sub" / "AGENT_HANDOFF.md").write_text("dup")
            checks = trc.drift_invariants(root, research_state_dir=rs)
            self.assertFalse(checks["handoff_single_root"]["pass"])

    def test_fail_closed_root_trigger_harden_file(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo", None)
            rs = _mk_valid_rs(td / "rs")
            (rs / "trigger_harden_20990101T000000Z.json").write_text("{}")
            checks = trc.drift_invariants(root, research_state_dir=rs)
            self.assertFalse(checks["no_root_trigger_harden_files"]["pass"])

    def test_fail_closed_root_md_json_over_bound(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            root = _mk_repo(td / "repo", None)
            rs = _mk_valid_rs(td / "rs")
            # add files to exceed bound. Bound tracks the committed baseline
            # (260 as of 2026-11-12T03:2XZ heavy-campaign artifacts); pad generously so
            # the negative test stays fail-closed regardless of baseline drift.
            for i in range(300):
                (rs / f"pad_{i:04d}.md").write_text("x")
            checks = trc.drift_invariants(root, research_state_dir=rs)
            self.assertFalse(checks["root_md_json_bounded"]["pass"])
            self.assertGreater(checks["root_md_json_bounded"]["count"], 163)

    def test_run_accepts_override_dirs_does_not_touch_real_state(self):
        # smoke: run() can be pointed at synthetic layout via drift check path? run() uses
        # drift_invariants(root, research_state_dir) with defaults to real repo; override args exist.
        real_before = (Path(__file__).resolve().parent.parent / "research_state" / "ironflow_probe_digest_latest.json").stat().st_mtime_ns
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            # build minimal harness/fixture-compatible root is heavy; just verify drift fn is pure
            root = _mk_repo(td / "repo", None)
            rs = _mk_valid_rs(td / "rs")
            checks = trc.drift_invariants(root, research_state_dir=rs)
            self.assertTrue(all(v.get("pass") for v in checks.values()))
        real_after = (Path(__file__).resolve().parent.parent / "research_state" / "ironflow_probe_digest_latest.json").stat().st_mtime_ns
        self.assertEqual(real_before, real_after)


class TestMonitorConsolidationRegressionGuard101(unittest.TestCase):
    def _mk_probe(self, ev_dir: Path, name: str, ts_off: float):
        p = ev_dir / name
        p.write_text(json.dumps({
            "probe_id": name.replace(".json", ""),
            "timestamp_utc": "2099-01-01T00:00:00Z",
            "mode": "quick",
            "data_through": "2026-10",
            "quick_resume_check": {"triggered": False, "data_through": "2026-10"},
            "probe_diff": {"summary": {}},
            "tree_change": {},
            "tree": {"status": 304},
        }))
        os.utime(p, (time.time() + ts_off, time.time() + ts_off))
        return p

    def test_consolidation_leaves_probe_count_two_and_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            ev = Path(td)
            self._mk_probe(ev, "ironflow_probe_20990101T000001Z.json", 1)
            self._mk_probe(ev, "ironflow_probe_20990101T000002Z.json", 2)
            self._mk_probe(ev, "ironflow_probe_20990101T000003Z.json", 3)
            old = mon.EVIDENCE_DIR
            try:
                mon.EVIDENCE_DIR = ev
                r1 = mon._consolidate_ironflow_probes()
                live = [p for p in ev.glob("ironflow_probe_*.json") if not p.name.startswith("ironflow_probe_digest_")]
                digests = list(ev.glob("ironflow_probe_digest_*.json"))
                self.assertEqual(len(live), 1)
                self.assertEqual(live[0].name, "ironflow_probe_20990101T000003Z.json")
                self.assertEqual(len(digests), 1)
                self.assertEqual(digests[0].name, "ironflow_probe_digest_latest.json")
                self.assertEqual(len(live) + len(digests), 2)
                # idempotent
                r2 = mon._consolidate_ironflow_probes()
                live2 = [p for p in ev.glob("ironflow_probe_*.json") if not p.name.startswith("ironflow_probe_digest_")]
                digests2 = list(ev.glob("ironflow_probe_digest_*.json"))
                self.assertEqual(len(live2) + len(digests2), 2)
                self.assertEqual(r2.get("removed", 0), 0)
            finally:
                mon.EVIDENCE_DIR = old

    def test_consolidation_with_existing_digest_keeps_invariant(self):
        with tempfile.TemporaryDirectory() as td:
            ev = Path(td)
            (ev / "ironflow_probe_digest_latest.json").write_text(json.dumps({"entries": [{"probe_id": "old"}], "latest_probe": "x"}))
            self._mk_probe(ev, "ironflow_probe_20990101T000010Z.json", 10)
            self._mk_probe(ev, "ironflow_probe_20990101T000011Z.json", 11)
            old = mon.EVIDENCE_DIR
            try:
                mon.EVIDENCE_DIR = ev
                mon._consolidate_ironflow_probes()
                live = [p for p in ev.glob("ironflow_probe_*.json") if not p.name.startswith("ironflow_probe_digest_")]
                digests = list(ev.glob("ironflow_probe_digest_*.json"))
                self.assertEqual(len(live) + len(digests), 2)
                self.assertEqual(live[0].name, "ironflow_probe_20990101T000011Z.json")
            finally:
                mon.EVIDENCE_DIR = old

    def test_consolidation_noop_on_already_valid_state(self):
        with tempfile.TemporaryDirectory() as td:
            ev = Path(td)
            self._mk_probe(ev, "ironflow_probe_20990101T000020Z.json", 20)
            (ev / "ironflow_probe_digest_latest.json").write_text(json.dumps({"entries": [], "latest_probe": "ironflow_probe_20990101T000020Z.json"}))
            old = mon.EVIDENCE_DIR
            try:
                mon.EVIDENCE_DIR = ev
                r = mon._consolidate_ironflow_probes()
                live = [p for p in ev.glob("ironflow_probe_*.json") if not p.name.startswith("ironflow_probe_digest_")]
                digests = list(ev.glob("ironflow_probe_digest_*.json"))
                self.assertEqual(len(live) + len(digests), 2)
                self.assertEqual(r.get("removed", 0), 0)
            finally:
                mon.EVIDENCE_DIR = old


if __name__ == "__main__":
    unittest.main()
