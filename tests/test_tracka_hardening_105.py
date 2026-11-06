import json, os, sys, tempfile, time, unittest, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts import tracka_resume_check as rc
from scripts import tracka_operator_report as opr

REAL = Path(__file__).resolve().parent.parent

def _mk_valid_rs(rs):
    rs.mkdir(parents=True, exist_ok=True)
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

class TestOperatorCLIEntrypoint105(unittest.TestCase):
    def test_cli_exit_zero_on_pass_real_repo(self):
        # End-to-end on the real, complete repository: no admissible Track A trigger => gate BLOCKED fail-closed,
        # exit != 0, stable JSON, fail-closed order; drift preflight still passes.
        r = subprocess.run([sys.executable, "scripts/tracka_operator_report.py"],
                           capture_output=True, text=True, cwd=str(REAL))
        self.assertNotEqual(r.returncode, 0, r.stdout)
        data = json.loads(r.stdout)
        self.assertTrue(data["pass"])
        self.assertEqual(data["gate_decision"]["status"], "BLOCKED")
        self.assertEqual(data["gate_decision"]["reason_code"], "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")
        self.assertEqual(data["fail_closed_order"], "drift_preflight->gate_decision->probe_invariant_state")
        self.assertTrue(data["probe_invariant_runtime_named"]["pass"])
        self.assertLess(data["elapsed_s"], 30)
        self.assertFalse(data["network"])
        self.assertFalse(data["writes_real_research_state"])

    def test_cli_exit_nonzero_on_drift_violation(self):
        # Fail-closed: a tmp repo violating the probe invariant (2 live probes) must exit != 0.
        td = tempfile.mkdtemp()
        root = _mk_repo(Path(td)/"repo")
        _mk_valid_rs(root/"research_state")
        (root/"research_state"/"ironflow_probe_20990102T000000Z.json").write_text("{}")
        os.utime(root/"research_state"/"ironflow_probe_20990102T000000Z.json",(time.time()+1,time.time()+1))
        r = subprocess.run([sys.executable, "scripts/tracka_operator_report.py", "--repo-root", str(root),
                            "--research-state-dir", str(root/"research_state"), "--harness-repo-root", str(root)],
                           capture_output=True, text=True, cwd=str(REAL))
        self.assertNotEqual(r.returncode, 0)
        data = json.loads(r.stdout)
        self.assertFalse(data["pass"])

    def test_cli_no_real_research_state_writes(self):
        real = REAL/'research_state'
        before = set(p.name for p in real.iterdir()) if real.exists() else set()
        r = subprocess.run([sys.executable, "scripts/tracka_operator_report.py", "--json"],
                           capture_output=True, text=True, cwd=str(REAL))
        # No trigger on real repo => fail-closed BLOCKED => exit != 0; no research_state writes either way.
        self.assertNotEqual(r.returncode, 0)
        after = set(p.name for p in real.iterdir()) if real.exists() else set()
        self.assertEqual(before, after)
        data = json.loads(r.stdout)
        self.assertFalse(data["network"])
        self.assertFalse(data["writes_real_research_state"])

    def test_cli_argparse_contract_violation_refuses_as_json(self):
        # G3/134: malformed --output-dir / unknown flags must NOT traceback; must emit
        # parseable JSON refusal, fail-closed, exit != 0, no outcomes/parquet inspection.
        for argv in (["--output-dir", "/nonexistent/zzz", "--json"],
                     ["--bogus-flag", "--json"],
                     ["--json", "--no-such-opt"]):
            r = subprocess.run([sys.executable, "scripts/tracka_operator_report.py"] + argv,
                               capture_output=True, text=True, cwd=str(REAL))
            self.assertNotEqual(r.returncode, 0, f"argv={argv}: {r.stdout}")
            self.assertNotIn("Traceback", r.stderr, f"argv={argv}: {r.stderr}")
            data = json.loads(r.stdout)
            self.assertEqual(data["status"], "BLOCKED", f"argv={argv}: {data}")
            self.assertEqual(data["reason_code"], "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS", f"argv={argv}: {data}")
            self.assertEqual(data["reason_code_detail"], "ARGPARSE_CONTRACT_VIOLATION_FAIL_CLOSED", f"argv={argv}: {data}")
            self.assertEqual(data["fail_closed_order"], "drift_preflight->gate_decision->probe_invariant_state", f"argv={argv}: {data}")
            self.assertFalse(data["reads_parquet"], f"argv={argv}: {data}")
            self.assertFalse(data["reads_outcomes"], f"argv={argv}: {data}")
            self.assertFalse(data["outcomes_inspected"], f"argv={argv}: {data}")
            self.assertFalse(data["canonical_outputs_mutated"], f"argv={argv}: {data}")
            self.assertFalse(data["network"], f"argv={argv}: {data}")
            self.assertFalse(data["writes_real_research_state"], f"argv={argv}: {data}")

    def test_cli_malformed_admissible_manifest_refuses_as_json(self):
        # G3/134: malformed admissible manifest must refuse as parseable JSON at the
        # operator level (nested gate_decision carries the seam reason code), never traceback.
        bad = json.dumps({"wrong": "shape", "missing": "required_fields"})
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write(bad); path = f.name
        try:
            r = subprocess.run([sys.executable, "scripts/tracka_operator_report.py",
                                "--admissible-manifest", path, "--json"],
                               capture_output=True, text=True, cwd=str(REAL))
            self.assertNotEqual(r.returncode, 0)
            self.assertNotIn("Traceback", r.stderr)
            data = json.loads(r.stdout)
            gd = data.get("gate_decision") or {}
            self.assertEqual(gd.get("status"), "BLOCKED")
            self.assertEqual(gd.get("reason_code"), "ADMISSIBLE_SEAM_NOGO_BEFORE_PREREG")
            self.assertFalse(gd.get("reads_parquet", True))
            self.assertFalse(gd.get("reads_outcomes", True))
            self.assertFalse(gd.get("outcomes_inspected", True))
        finally:
            os.unlink(path)

    def test_named_probe_runtime_guard_in_resume_check_real_repo(self):
        # Named probe_invariant_runtime guard wired into run() on the real repo (fail-closed).
        r = rc.run(repo_root=REAL, research_state_dir=REAL/'research_state')
        self.assertTrue(r["pass"])
        self.assertIn("probe_invariant_runtime_named", r["checks"])
        self.assertTrue(r["checks"]["probe_invariant_runtime_named"]["pass"])

    def test_named_probe_runtime_guard_fails_closed_on_missing_runtime(self):
        td = tempfile.mkdtemp()
        root = _mk_repo(Path(td)/"repo")
        _mk_valid_rs(root/"research_state")
        p = root/"research_state"/"ironflow_probe_20990101T000001Z.json"
        d = json.loads(p.read_text())
        d.pop("probe_invariant_runtime", None)
        p.write_text(json.dumps(d))
        r = rc.run(repo_root=root, research_state_dir=root/"research_state")
        self.assertFalse(r["checks"]["probe_invariant_runtime_named"]["pass"])
        self.assertFalse(r["pass"])

if __name__=='__main__':
    unittest.main()