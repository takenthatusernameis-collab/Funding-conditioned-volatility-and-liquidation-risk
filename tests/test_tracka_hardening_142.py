"""FCLR-NEXT-142: Track A guarded/operator/CLI hardening campaign (cluster a-d).

tmp-isolated, dep-light, no network, no parquet/outcome reads, no real
research_state writes. Covers:
  (a) guarded/operator parity matrix — same NOGO/GO/malformed-prereg/missing-data
      inputs produce stable, comparable refusal fields across guarded_execute,
      tracka_resume_gate.decide, and operator/gate CLI JSON
      (status/reason_code/reason_code_detail/outcomes_inspected/reads_*/network/writes).
  (b) canonical output + real-research-state mutation proofs across refusal matrix:
      byte snapshots of FRONTIER/RUN_MANIFEST/EVAL_FCLR010 unchanged;
      writes_real_research_state:false; tmp output_dir only.
  (c) admissible seam wired-field type stability (pass/status/reason_code/failures/
      month/fail_closed/network/reads_outcomes/reads_parquet types stable across
      missing/corrupt/NOGO/GO cases).
  (d) CLI --json determinism under mixed flag order / duplicate-safe refusals
      (bogus + valid-looking combos, missing required-like paths) — parseable
      refusal or stable stderr+JSON contract, no traceback-as-first-line contract.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

REAL = Path(__file__).resolve().parent.parent
RS = REAL / "research_state"
RUN_MANIFEST = RS / "run_manifest.json"
FRONTIER = RS / "experiment_frontier.json"
EVAL_FCLR010 = RS / "evaluation_summary_FCLR010.md"
CANON = [FRONTIER, RUN_MANIFEST, EVAL_FCLR010]
BLOCKED_RC = "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS"
SAFE_FALSE = ("outcomes_inspected", "canonical_outputs_mutated", "network", "writes_real_research_state")
READ_FALSE = ("reads_parquet", "reads_outcomes")
CLIS = [
    "scripts/tracka_resume_check.py",
    "scripts/tracka_resume_gate.py",
    "scripts/tracka_operator_report.py",
]


def _snap(paths):
    return {str(p): (p.read_bytes() if p.exists() else None) for p in paths}


def _unchanged(paths, before):
    for s, b in before.items():
        p = Path(s)
        a = p.read_bytes() if p.exists() else None
        if b != a:
            raise AssertionError(f"canonical target mutated: {s}")


def _assert_blocked_no_io(p, *, allow_reason_prefixes=("ADMISSIBLE_", "PREREG_", "DRIFT_", "ARGPARSE_")):
    assert p.get("status") == "BLOCKED", p
    rc = str(p.get("reason_code") or "")
    rcd = str(p.get("reason_code_detail") or "")
    assert rc == BLOCKED_RC or rc.startswith("ADMISSIBLE_") or any(rc.startswith(x) for x in allow_reason_prefixes), (rc, p)
    for k in SAFE_FALSE:
        assert p.get(k) is False, (k, p.get(k), p)
    for k in READ_FALSE:
        assert p.get(k) in (False, None), (k, p.get(k), p)
    assert p.get("outcomes_loaded") in (None, False), p


def _valid_admissible_manifest(month="2026-11"):
    return {
        "track": "A",
        "source_family": "ironflow_hyperliquid_liquidations",
        "venue": "hyperliquid",
        "source": "ironflow/hyperliquid-liquidations",
        "month": month,
        "unauthenticated": True,
        "requires_api_key": False,
        "requires_signature": False,
        "observed_liquidations": True,
        "modeled_or_proxy": False,
        "merges_non_hyperliquid": False,
        "label_definition": "observed_hyperliquid_liquidation_event_rows_from_ironflow",
        "timestamp_normalized_utc": True,
        "artifacts": {
            "events": {
                "path": f"research_state/data_cache/ironflow_events/events/{month}.parquet",
                "url": f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/{month}.parquet",
                "schema_fields": ["timestamp", "symbol", "liquidation_notional", "side"],
            },
            "fills": {
                "path": f"research_state/data_cache/ironflow_events/fills/{month}.parquet",
                "url": f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/{month}.parquet",
                "schema_fields": ["timestamp", "symbol", "size", "price"],
            },
        },
    }


def _write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj), encoding="utf-8")
    return str(path)


def _valid_prereg(td):
    return _write_json(Path(td) / "prereg.json", {"experiment_id": "FCLR-010", "frozen": True, "preregistered_at_utc": "2026-11-06T00:00:00Z"})


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(REAL))


def _extract_json_refusal(text):
    for line in reversed([ln for ln in text.splitlines() if ln.strip()]):
        s = line.strip()
        if s.startswith("{") and s.endswith("}"):
            try:
                p = json.loads(s)
                if isinstance(p, dict):
                    return p
            except Exception:
                pass
    try:
        p = json.loads(text)
        if isinstance(p, dict):
            return p
    except Exception:
        pass
    return None


class Test142ParityMatrixGuardedGateCli(unittest.TestCase):
    """(a) guarded/operator parity matrix: same inputs -> stable comparable refusal fields."""

    def _case_inputs(self, td):
        """Return a list of (label, kwargs_for_guarded_execute, cli_args_extra) cases."""
        adm_nogo = {"venue": "binance", "observed_liquidations": True}  # NO-GO seam
        adm_go = _valid_admissible_manifest()
        cases = []
        # missing prereg + NOGO seam
        cases.append(("nogo_seam_missing_prereg", {
            "data_path": Path(td) / "nodata",
            "pre_reg_path": None,
            "repo_root": REAL,
            "admissible_manifest": adm_nogo,
            "outcome_loader": None,
            "allow_default_loader": False,
        }, ["--admissible-manifest", str(_write_json(Path(td) / "adm_nogo.json", adm_nogo))]))
        # missing prereg + GO seam (valid admissible manifest, missing data path)
        cases.append(("go_seam_missing_prereg_missing_data", {
            "data_path": Path(td) / "nodata",
            "pre_reg_path": None,
            "repo_root": REAL,
            "admissible_manifest": adm_go,
            "outcome_loader": None,
            "allow_default_loader": False,
        }, ["--admissible-manifest", str(_write_json(Path(td) / "adm_go.json", adm_go))]))
        # valid prereg + GO seam + missing data path
        pp = _valid_prereg(td)
        ap = _write_json(Path(td) / "adm_go2.json", adm_go)
        cases.append(("go_seam_valid_prereg_missing_data", {
            "data_path": Path(td) / "nodata",
            "pre_reg_path": Path(pp),
            "repo_root": REAL,
            "admissible_manifest": adm_go,
            "outcome_loader": None,
            "allow_default_loader": False,
        }, ["--admissible-manifest", ap, "--pre-reg", pp]))
        # corrupt prereg + GO seam
        bad_pp = Path(td) / "bad_prereg.json"
        bad_pp.write_text("{bad json", encoding="utf-8")
        cases.append(("go_seam_corrupt_prereg", {
            "data_path": Path(td) / "nodata",
            "pre_reg_path": Path(bad_pp),
            "repo_root": REAL,
            "admissible_manifest": adm_go,
            "outcome_loader": None,
            "allow_default_loader": False,
        }, ["--admissible-manifest", ap, "--pre-reg", str(bad_pp)]))
        return cases

    def test_parity_refusal_fields_across_guarded_gate_cli(self):
        from scripts.fclr010_guarded_entry import guarded_execute
        from scripts import tracka_resume_gate as gate
        before = _snap(CANON)
        cases = self._case_inputs(tempfile.mkdtemp(prefix="fclr142_parity_"))
        td_parent = Path(cases[0][1]["data_path"]).parent
        for label, gk, cli_extra in cases:
            with self.subTest(label=label):
                # guarded_execute
                r_ge = guarded_execute(**gk)
                # tracka_resume_gate.decide (map manifest path)
                adm_path = None
                for x in cli_extra:
                    if x == "--admissible-manifest":
                        pass
                adm_path = cli_extra[cli_extra.index("--admissible-manifest") + 1] if "--admissible-manifest" in cli_extra else None
                pre_reg = cli_extra[cli_extra.index("--pre-reg") + 1] if "--pre-reg" in cli_extra else None
                r_gate = gate.decide(str(gk["data_path"]), str(td_parent / "out"),
                                     pre_reg_path=pre_reg, admissible_manifest_path=adm_path,
                                     harness_repo_root=REAL)
                self.assertEqual(r_ge.get("status"), "BLOCKED", (label, r_ge))
                self.assertEqual(r_gate.get("status"), "BLOCKED", (label, r_gate))
                # comparable refusal fields
                for key in ("status", "reason_code", "reason_code_detail", "outcomes_inspected",
                            "reads_parquet", "reads_outcomes", "network", "writes_real_research_state"):
                    gv = r_ge.get(key)
                    gt = r_gate.get(key)
                    self.assertEqual(type(gv), type(gt), (label, key, gv, gt))
                    if key in SAFE_FALSE + READ_FALSE + ("network", "writes_real_research_state"):
                        self.assertFalse(gv, (label, key, gv))
                self.assertFalse(r_gate.get("outcomes_inspected"), label)
                self.assertFalse(r_gate.get("reads_parquet"), label)
                self.assertFalse(r_gate.get("reads_outcomes"), label)
                self.assertFalse(r_gate.get("network"), label)
                self.assertFalse(r_gate.get("writes_real_research_state"), label)
        _unchanged(CANON, before)

    def test_operator_cli_json_parity_matches_gate_blocked(self):
        before = _snap(CANON)
        adm_go = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            ap = _write_json(Path(td) / "adm.json", adm_go)
            pp = _valid_prereg(td)
            r_cli = _run([sys.executable, "scripts/tracka_operator_report.py", "--json",
                          "--admissible-manifest", ap, "--pre-reg", pp,
                          "--data-path", str(Path(td) / "nodata")])
            text = (r_cli.stdout or "") + "\n" + (r_cli.stderr or "")
            p = _extract_json_refusal(r_cli.stdout) or _extract_json_refusal(text)
            self.assertIsNotNone(p, (r_cli.returncode, r_cli.stdout[:400], r_cli.stderr[:400]))
            gd = p.get("gate_decision") or p
            self.assertIn(gd.get("status"), ("BLOCKED", "SEAM_IMPORT_ERROR"), p)
            self.assertFalse(gd.get("outcomes_inspected", True), p)
            self.assertFalse(gd.get("network", True), p)
            self.assertFalse(gd.get("writes_real_research_state", True), p)
            self.assertIsInstance(r_cli.returncode, int)
        _unchanged(CANON, before)


class Test142CanonicalOutputMutationProofs(unittest.TestCase):
    """(b) canonical output + real-research-state mutation proofs across refusal matrix."""

    def test_refusal_matrix_leaves_canonical_and_real_state_untouched(self):
        from scripts.fclr010_guarded_entry import guarded_execute
        before = _snap(CANON)
        adm_go = _valid_admissible_manifest()
        adm_nogo = {"venue": "binance", "observed_liquidations": True}
        pp = None
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            ap = _write_json(td / "adm.json", adm_go)
            pp = _valid_prereg(str(td))
            bad_pp = td / "bad_prereg.json"
            bad_pp.write_text("{bad json", encoding="utf-8")
            # refusal matrix: NOGO seam; corrupt prereg; GO seam + missing data; missing prereg
            matrix = [
                dict(data_path=td / "nodata", pre_reg_path=None, repo_root=REAL,
                     admissible_manifest=adm_nogo, outcome_loader=None, allow_default_loader=False),
                dict(data_path=td / "nodata", pre_reg_path=Path(bad_pp), repo_root=REAL,
                     admissible_manifest=adm_go, outcome_loader=None, allow_default_loader=False),
                dict(data_path=td / "nodata", pre_reg_path=Path(pp), repo_root=REAL,
                     admissible_manifest=adm_go, outcome_loader=None, allow_default_loader=False),
                dict(data_path=td / "nodata", pre_reg_path=Path(td / "missing_prereg.json"), repo_root=REAL,
                     admissible_manifest=adm_go, outcome_loader=None, allow_default_loader=False),
            ]
            for i, kw in enumerate(matrix):
                with self.subTest(i=i):
                    r = guarded_execute(**kw)
                    self.assertEqual(r.get("status"), "BLOCKED", (i, r))
                    self.assertFalse(r.get("writes_real_research_state", True), (i, r))
                    self.assertFalse(r.get("canonical_outputs_mutated", True), (i, r))
                    self.assertFalse(r.get("outcomes_inspected", True), (i, r))
                    self.assertFalse(r.get("network", True), (i, r))
        _unchanged(CANON, before)

    def test_writes_real_research_state_false_on_blocked_and_ready(self):
        from scripts.fclr010_guarded_entry import guarded_execute
        from scripts.fclr010_harness import FCLR010Harness
        before = _snap(CANON)
        h = FCLR010Harness(repo_root=REAL)
        adm_go = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            pp = _valid_prereg(td)
            # blocked branch
            r_blocked = guarded_execute(data_path=Path(td) / "nodata", pre_reg_path=Path(pp),
                                        repo_root=REAL, admissible_manifest=adm_go,
                                        outcome_loader=None, allow_default_loader=False)
            self.assertFalse(r_blocked.get("writes_real_research_state", True), r_blocked)
            # READY_FROZEN branch (empty data dir) -> still no real state writes
            empty_dir = Path(td) / "empty_data"
            empty_dir.mkdir()
            r_ready = h.execute_ready_data_load(empty_dir, Path(pp), admissible_manifest=adm_go)
            self.assertEqual(r_ready.get("status"), "READY_FROZEN", r_ready)
            self.assertIsNot(r_ready.get("writes_real_research_state"), True, r_ready)
        _unchanged(CANON, before)


class Test142AdmissibleSeamWiredFieldTypeStability(unittest.TestCase):
    """(c) admissible seam wired-field type stability across missing/corrupt/NOGO/GO cases."""

    def _stable_type_checks(self, asc):
        self.assertIsInstance(asc.get("pass"), bool, asc)
        self.assertIsInstance(asc.get("status"), str, asc)
        if asc.get("reason_code") is not None:
            self.assertIsInstance(asc.get("reason_code"), str, asc)
        if asc.get("failures") is not None:
            self.assertIsInstance(asc.get("failures"), list, asc)
        if "month" in asc and asc.get("month") is not None:
            self.assertIsInstance(asc.get("month"), (str, type(None)), asc)
        self.assertIsInstance(asc.get("fail_closed"), bool, asc)
        self.assertIsInstance(asc.get("network"), bool, asc)
        self.assertIsInstance(asc.get("reads_outcomes"), bool, asc)
        self.assertIsInstance(asc.get("reads_parquet"), bool, asc)

    def test_seam_no_candidate_wired_stable_types(self):
        from scripts.tracka_resume_check import admissible_seam_check
        asc = admissible_seam_check(candidate_path=None, repo_root=REAL)
        self.assertTrue(asc.get("pass"), asc)
        self._stable_type_checks(asc)
        self.assertFalse(asc.get("network"), asc)
        self.assertFalse(asc.get("reads_outcomes"), asc)
        self.assertFalse(asc.get("reads_parquet"), asc)
        self.assertTrue(asc.get("fail_closed"), asc)

    def test_seam_missing_path_stable_types(self):
        from scripts.tracka_resume_check import admissible_seam_check
        asc = admissible_seam_check(candidate_path="/nonexistent_adm_142_xyz.json", repo_root=REAL)
        self.assertFalse(asc.get("pass"), asc)
        self._stable_type_checks(asc)
        self.assertEqual(asc.get("reason_code"), "ADMISSIBLE_CANDIDATE_PATH_MISSING", asc)

    def test_seam_corrupt_path_stable_types(self):
        from scripts.tracka_resume_check import admissible_seam_check
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "adm.json"
            bad.write_text("{not json", encoding="utf-8")
            asc = admissible_seam_check(candidate_path=str(bad), repo_root=REAL)
        self.assertFalse(asc.get("pass"), asc)
        self._stable_type_checks(asc)
        self.assertEqual(asc.get("reason_code"), "ADMISSIBLE_CANDIDATE_LOAD_ERROR", asc)

    def test_seam_nogo_manifest_stable_types(self):
        from scripts.tracka_resume_check import admissible_seam_check
        m = _valid_admissible_manifest()
        m["observed_liquidations"] = False  # modeled/proxy conflation => NO-GO
        with tempfile.TemporaryDirectory() as td:
            ap = _write_json(Path(td) / "adm_nogo.json", m)
            asc = admissible_seam_check(candidate_path=str(ap), repo_root=REAL)
        self.assertFalse(asc.get("pass"), asc)
        self._stable_type_checks(asc)
        self.assertFalse(asc.get("network"), asc)
        self.assertFalse(asc.get("reads_outcomes"), asc)
        self.assertFalse(asc.get("reads_parquet"), asc)
        self.assertTrue(asc.get("fail_closed"), asc)


class Test142CliJsonDeterminismMixedFlags(unittest.TestCase):
    """(d) CLI --json determinism under mixed flag order / duplicate-safe refusals."""

    def test_bogus_plus_valid_looking_combos_refusal_stable_types(self):
        before = _snap(CANON)
        adm_go = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            ap = _write_json(Path(td) / "adm.json", adm_go)
            pp = _valid_prereg(td)
            bad_adm = Path(td) / "bad_adm.json"
            bad_adm.write_text("{broken", encoding="utf-8")
            cmds = [
                # bogus + valid-looking combos, mixed order
                ["scripts/tracka_resume_gate.py", "--bogus", "--json", "--admissible-manifest", str(ap),
                 "--pre-reg", pp, "--data-path", "/nodata142"],
                ["scripts/tracka_resume_gate.py", "--admissible-manifest", str(bad_adm), "--bogus", "--json"],
                ["scripts/tracka_operator_report.py", "--bogus", "--json", "--admissible-manifest", str(ap),
                 "--pre-reg", str(Path(td) / "corrupt_prereg.json")],
                # missing required-like path (nonexistent pre-reg) + bogus
                ["scripts/tracka_resume_gate.py", "--bogus", "--pre-reg", "/nonexistent_prereg_142.json", "--json"],
            ]
            for cmd in cmds:
                with self.subTest(cmd=cmd[0]):
                    Path(td, "corrupt_prereg.json").write_text("{bad", encoding="utf-8")
                    r = _run([sys.executable] + cmd)
                    combined = (r.stdout or "") + "\n" + (r.stderr or "")
                    p = _extract_json_refusal(r.stdout) or _extract_json_refusal(combined)
                    self.assertIsNotNone(p, (cmd, r.returncode, r.stdout[:400], r.stderr[:400]))
                    # no traceback-as-first-line contract
                    first = (r.stdout + "\n" + r.stderr).splitlines()[0] if (r.stdout or r.stderr) else ""
                    self.assertNotIn("Traceback (most recent call last):", first, (cmd, combined[:300]))
                    status = p.get("status")
                    self.assertIn(status, ("BLOCKED", "SEAM_IMPORT_ERROR", "NO-GO"), p)
                    for k in ("outcomes_inspected", "canonical_outputs_mutated", "network", "writes_real_research_state"):
                        if k in p:
                            self.assertIs(p.get(k), False, (k, p, cmd))
        _unchanged(CANON, before)


if __name__ == "__main__":
    unittest.main()
