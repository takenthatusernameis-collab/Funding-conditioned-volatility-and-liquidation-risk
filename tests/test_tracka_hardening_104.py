import json, os, sys, tempfile, time, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts import tracka_resume_check as rc
from scripts import tracka_resume_gate as gate
import scripts.monitor_ironflow_liquidations as mon

def _mk_valid_rs(rs):
    rs.mkdir(parents=True, exist_ok=True)
    (rs/'AGENT_HANDOFF.md').write_text('x') # ignored by drift (drift checks repo root)
    p = rs/"ironflow_probe_20990101T000001Z.json"
    p.write_text(json.dumps({"probe_id":"ironflow_probe_20990101T000001Z","probe_invariant_runtime":{"pass":True,"total":2,"invariant":"live==1 and canonical_digest_latest==1 and total==2","live_probes":["ironflow_probe_20990101T000001Z.json"],"digests":["ironflow_probe_digest_latest.json"]}}))
    os.utime(p,(time.time()+1,time.time()+1))
    (rs/"ironflow_probe_digest_latest.json").write_text("{}")
    (rs/"alt_source_scan_latest.json").write_text("{}")
    (rs/"alt_source_deep_review_latest.md").write_text("x")
    return rs

def _mk_repo(root):
    root.mkdir(parents=True, exist_ok=True)
    (root/"AGENT_HANDOFF.md").write_text("x")
    (root/"research_state").mkdir(exist_ok=True)
    return root

class TestProbeInvariantRuntimeValidation104(unittest.TestCase):
    def test_valid_shape(self):
        v=rc._validate_probe_invariant_runtime_shape({"pass":True,"total":2,"invariant":"x","live_probes":["a"],"digests":["b"]})
        self.assertTrue(v["pass"]); self.assertTrue(v["shape_valid"])
    def test_missing_required(self):
        v=rc._validate_probe_invariant_runtime_shape({"pass":True})
        self.assertFalse(v["pass"]); self.assertIn("total", v["missing"])
    def test_bad_types(self):
        v=rc._validate_probe_invariant_runtime_shape({"pass":"yes","total":"2","invariant":1})
        self.assertFalse(v["pass"])
    def test_none(self):
        v=rc._validate_probe_invariant_runtime_shape(None)
        self.assertFalse(v["pass"])
    def test_probe_invariant_state_reads_runtime(self):
        with tempfile.TemporaryDirectory() as td:
            root=_mk_repo(Path(td)/"repo"); rs=_mk_valid_rs(Path(td)/"rs")
            st=rc.probe_invariant_state(root, rs)
            self.assertTrue(st["assert_probe_invariant"]["pass"])
            self.assertTrue(st["probe_invariant_runtime_present"])
            self.assertTrue(st["probe_invariant_runtime_validation"]["pass"])
            self.assertTrue(st["pass"])

class TestComposeOperatorReport104(unittest.TestCase):
    def test_compose_fail_closed_prereg_block_no_real_writes(self):
        real=Path(__file__).resolve().parent.parent/'research_state'
        before=set(p.name for p in real.iterdir()) if real.exists() else set()
        with tempfile.TemporaryDirectory() as td:
            root=_mk_repo(Path(td)/"repo"); rs=_mk_valid_rs(Path(td)/"rs")
            r=rc.compose_operator_report(repo_root=root, research_state_dir=rs, harness_repo_root=root)
            self.assertTrue(r["drift_preflight"]["pass"], r["drift_preflight"])
            self.assertEqual(r["gate_decision"]["status"], "BLOCKED")
            self.assertFalse(r["gate_decision"].get("outcomes_inspected", True))
            self.assertTrue(r["probe_invariant_state"]["pass"])
            self.assertTrue(r["probe_invariant_runtime_valid"])
            self.assertTrue(r["pass"])
            self.assertEqual(r["fail_closed_order"], "drift_preflight->gate_decision->probe_invariant_state")
            self.assertFalse(r["network"]); self.assertFalse(r["writes_real_research_state"])
            self.assertLess(r["elapsed_s"], 30)
        after=set(p.name for p in real.iterdir()) if real.exists() else set()
        self.assertEqual(before, after)

    def test_compose_fails_closed_on_drift_violation(self):
        with tempfile.TemporaryDirectory() as td:
            root=_mk_repo(Path(td)/"repo"); rs=_mk_valid_rs(Path(td)/"rs")
            # add extra live probe to violate invariant
            (rs/"ironflow_probe_20990102T000000Z.json").write_text("{}")
            r=rc.compose_operator_report(repo_root=root, research_state_dir=rs, harness_repo_root=root)
            self.assertFalse(r["pass"])
            self.assertFalse(r["probe_invariant_state"]["pass"])

    def test_compose_on_real_repo_drift_pass(self):
        root=Path(__file__).resolve().parent.parent
        r=rc.compose_operator_report(repo_root=root, research_state_dir=root/'research_state', harness_repo_root=root)
        self.assertTrue(r["drift_preflight"]["pass"], r["drift_preflight"])
        self.assertEqual(r["gate_decision"]["status"], "BLOCKED")
        self.assertTrue(r["probe_invariant_state"]["assert_probe_invariant"]["pass"])
        self.assertTrue(r["probe_invariant_runtime_valid"])

if __name__=='__main__': unittest.main()
