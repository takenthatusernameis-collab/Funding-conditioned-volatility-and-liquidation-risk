"""FCLR-NEXT-140: Track A seam/CLI/parity hardening campaign.

tmp-isolated, dep-light, no network, no parquet/outcome reads, no real
research_state writes. Covers:
  (a) empty/unreadable data path under valid prereg -> BLOCKED stable reason codes
  (b) CLI argparse contract on all 3 CLIs: bogus flags, missing/unreadable prereg,
      conflicting --output-dir, invalid JSON (admissible manifest / prereg),
      stdout stress (repeated invocations always emit parseable JSON refusals)
  (c) cross-CLI parity + canonical output integrity: identical refusal structure,
      exit codes, and field types across tracka_resume_check / tracka_resume_gate /
      tracka_operator_report; canonical outputs byte-identical after every refusal
  (d) guarded_execute refuse-before-load on malformed admissible manifests:
      outcome-loader spy never called on a blocked branch
"""
from __future__ import annotations

import json
import os
import stat
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


def _assert_blocked_no_io(p, *, allow_reason_codes=(BLOCKED_RC,)):
    assert p.get("status") == "BLOCKED", p
    if p.get("reason_code") is not None:
        assert p.get("reason_code") in allow_reason_codes or str(p.get("reason_code", "")).startswith("ADMISSIBLE_SEAM_"), p
    for k in SAFE_FALSE:
        assert p.get(k) is False, (k, p.get(k), p)
    for k in READ_FALSE:
        assert p.get(k) in (False, None), (k, p.get(k), p)


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


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(REAL))


def _valid_prereg(td):
    prereg = Path(td) / "prereg.json"
    prereg.write_text(json.dumps({"preregistered_at_utc": "2026-11-06T00:00:00Z", "frozen": True}))
    return str(prereg)


class Test140DataPathEmptyUnreadable(unittest.TestCase):
    """(a) empty/unreadable data path under valid prereg -> blocked stable reason codes."""

    def test_harness_nonexistent_data_path_blocked_missing(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness(repo_root=REAL)
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            prereg = _valid_prereg(td)
            r = h.evaluate_forward(Path(td) / "nodata", Path(td), pre_reg_path=prereg, admissible_manifest=m)
        self.assertEqual(r.get("status"), "BLOCKED", r)
        self.assertEqual(r.get("reason_code"), BLOCKED_RC, r)
        self.assertEqual(r.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING", r)
        self.assertTrue(r.get("seam_go_data_missing"), r)
        self.assertTrue((r.get("admissible_seam_wired") or {}).get("pass"), r)
        _assert_blocked_no_io(r)
        _unchanged(CANON, before)

    def test_harness_unreadable_data_path_blocked_unreadable(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness(repo_root=REAL)
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            data_dir = Path(td) / "data"
            data_dir.mkdir()
            (data_dir / "file.parquet").write_bytes(b"fake")
            data_dir.chmod(0o000)
            prereg = _valid_prereg(td)
            try:
                r = h.evaluate_forward(data_dir, Path(td), pre_reg_path=prereg, admissible_manifest=m)
            finally:
                data_dir.chmod(0o755)
        self.assertEqual(r.get("status"), "BLOCKED", r)
        self.assertEqual(r.get("reason_code"), BLOCKED_RC, r)
        self.assertEqual(r.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_DATA_PATH_UNREADABLE", r)
        self.assertTrue(r.get("seam_go_data_unreadable"), r)
        _assert_blocked_no_io(r)
        _unchanged(CANON, before)

    def test_gate_nonexistent_data_path_blocked_stable(self):
        from scripts import tracka_resume_gate as gate
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            ap = _write_json(Path(td) / "adm.json", m)
            prereg = _valid_prereg(td)
            r = gate.decide("/nonexistent_data_path_xyz_140", Path(td), pre_reg_path=prereg, admissible_manifest_path=ap, harness_repo_root=REAL)
        self.assertEqual(r.get("status"), "BLOCKED", r)
        self.assertEqual(r.get("reason_code"), BLOCKED_RC, r)
        self.assertEqual(r.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING", r)
        self.assertTrue(r.get("seam_go_data_missing"), r)
        self.assertEqual(r.get("fail_closed_order"), "drift_preflight->admissible_seam->manifest_prereg", r)
        _assert_blocked_no_io(r)
        _unchanged(CANON, before)

    def test_gate_unreadable_data_path_blocked_stable(self):
        from scripts import tracka_resume_gate as gate
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            data_dir = Path(td) / "data"
            data_dir.mkdir()
            (data_dir / "file.parquet").write_bytes(b"fake")
            data_dir.chmod(0o000)
            ap = _write_json(Path(td) / "adm.json", m)
            prereg = _valid_prereg(td)
            try:
                r = gate.decide(str(data_dir), Path(td), pre_reg_path=prereg, admissible_manifest_path=ap, harness_repo_root=REAL)
            finally:
                data_dir.chmod(0o755)
        self.assertEqual(r.get("status"), "BLOCKED", r)
        self.assertEqual(r.get("reason_code"), BLOCKED_RC, r)
        self.assertEqual(r.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_DATA_PATH_UNREADABLE", r)
        self.assertTrue(r.get("seam_go_data_unreadable"), r)
        _assert_blocked_no_io(r)
        _unchanged(CANON, before)

    def test_empty_dir_data_path_ready_frozen_no_implicit_load(self):
        """Existing but empty data dir => READY_FROZEN with no implicit parquet/outcome load."""
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness(repo_root=REAL)
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            empty_dir = Path(td) / "empty_data"
            empty_dir.mkdir()
            prereg = _valid_prereg(td)
            r = h.execute_ready_data_load(empty_dir, Path(prereg), admissible_manifest=m)
        self.assertEqual(r.get("status"), "READY_FROZEN", r)
        self.assertFalse(r.get("data_loaded_implicitly"), r)
        self.assertIsNone(r.get("outcomes_loaded"), r)
        self.assertFalse(r.get("reads_parquet"), r)
        self.assertFalse(r.get("reads_outcomes"), r)
        self.assertFalse(r.get("network"), r)
        self.assertFalse(r.get("writes_real_research_state"), r)
        _unchanged(CANON, before)


class Test140CliArgparseContractAllClis(unittest.TestCase):
    """(b) bulletproof CLI argparse contract on all 3 CLIs."""

    BOGUS_CASES = [
        (["scripts/tracka_resume_check.py", "--bogus"]),
        (["scripts/tracka_resume_gate.py", "--bogus", "--json"]),
        (["scripts/tracka_operator_report.py", "--bogus", "--json"]),
        (["scripts/tracka_resume_check.py", "--bogus=value"]),
        (["scripts/tracka_resume_gate.py", "--bogus=value", "--json"]),
        (["scripts/tracka_operator_report.py", "--bogus=value", "--json"]),
    ]

    def test_all_clis_bogus_flags_fail_closed_json(self):
        before = _snap(CANON)
        for cmd in self.BOGUS_CASES:
            res = _run([sys.executable] + cmd)
            self.assertNotEqual(res.returncode, 0, (cmd, res.stdout, res.stderr))
            try:
                out = json.loads(res.stdout.strip())
            except Exception as e:
                self.fail(f"stdout not parseable JSON for {cmd}: {e}; stdout={res.stdout[:200]}; stderr={res.stderr[:200]}")
            self.assertNotIn("Traceback", json.dumps(out), cmd)
            self.assertEqual(out.get("status"), "BLOCKED", (cmd, out))
            for k in SAFE_FALSE:
                self.assertFalse(out.get(k), (cmd, k, out))
            for k in READ_FALSE:
                self.assertIn(out.get(k), (False, None), (cmd, k, out))
        _unchanged(CANON, before)

    def test_gate_cli_nonexistent_manifest_file_fail_closed_json(self):
        before = _snap(CANON)
        res = _run([sys.executable, "scripts/tracka_resume_gate.py", "--manifest", "/nonexistent_manifest_140.json", "--json"])
        self.assertNotEqual(res.returncode, 0, (res.stdout, res.stderr))
        out = json.loads(res.stdout.strip())
        self.assertNotIn("Traceback", json.dumps(out))
        self.assertEqual(out.get("status"), "BLOCKED", out)
        self.assertFalse(out.get("outcomes_inspected"))
        self.assertFalse(out.get("network"))
        self.assertFalse(out.get("writes_real_research_state"))
        _unchanged(CANON, before)

    def test_gate_cli_malformed_prereg_json_fail_closed_json(self):
        before = _snap(CANON)
        with tempfile.TemporaryDirectory() as td:
            bad_prereg = Path(td) / "bad_prereg.json"
            bad_prereg.write_text('{"preregistered_at_utc": "2026-11-06T00:00:00Z", broken', encoding="utf-8")
            res = _run([sys.executable, "scripts/tracka_resume_gate.py", "--prereg", str(bad_prereg), "--json"])
        self.assertNotEqual(res.returncode, 0, (res.stdout, res.stderr))
        out = json.loads(res.stdout.strip())
        self.assertNotIn("Traceback", json.dumps(out))
        self.assertEqual(out.get("status"), "BLOCKED", out)
        self.assertFalse(out.get("outcomes_inspected"))
        self.assertFalse(out.get("network"))
        self.assertFalse(out.get("writes_real_research_state"))
        _unchanged(CANON, before)

    def test_gate_cli_output_dir_conflicts_with_existing_file_fail_closed_json(self):
        before = _snap(CANON)
        with tempfile.TemporaryDirectory() as td:
            existing_file = Path(td) / "not_a_dir"
            existing_file.write_text("i am a regular file", encoding="utf-8")
            res = _run([sys.executable, "scripts/tracka_resume_gate.py", "--output-dir", str(existing_file), "--json"])
        self.assertNotEqual(res.returncode, 0, (res.stdout, res.stderr))
        out = json.loads(res.stdout.strip())
        self.assertNotIn("Traceback", json.dumps(out))
        self.assertEqual(out.get("status"), "BLOCKED", out)
        self.assertFalse(out.get("outcomes_inspected"))
        self.assertFalse(out.get("network"))
        self.assertFalse(out.get("writes_real_research_state"))
        _unchanged(CANON, before)

    def test_all_clis_malformed_admissible_manifest_json_fail_closed_json(self):
        before = _snap(CANON)
        base_cmds = [
            ["scripts/tracka_resume_check.py", "--admissible-manifest"],
            ["scripts/tracka_resume_gate.py", "--admissible-manifest", "--json"],
            ["scripts/tracka_operator_report.py", "--admissible-manifest", "--json"],
        ]
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "bad_adm.json"
            bad.write_text("{broken json!!! 140", encoding="utf-8")
            for base in base_cmds:
                cmd = base + [str(bad)]
                res = _run([sys.executable] + cmd)
                self.assertNotEqual(res.returncode, 0, (cmd, res.stdout, res.stderr))
                try:
                    out = json.loads(res.stdout.strip())
                except Exception as e:
                    self.fail(f"stdout not parseable JSON for {cmd}: {e}; stdout={res.stdout[:200]}; stderr={res.stderr[:200]}")
                self.assertNotIn("Traceback", json.dumps(out), cmd)
                self.assertIn(out.get("status"), ("BLOCKED", "NO-GO"), (cmd, out))
                self.assertFalse(out.get("outcomes_inspected", False), cmd)
                self.assertFalse(out.get("reads_parquet", False), cmd)
                self.assertFalse(out.get("reads_outcomes", False), cmd)
                self.assertFalse(out.get("network", False), cmd)
                self.assertFalse(out.get("writes_real_research_state", False), cmd)
        _unchanged(CANON, before)

    def test_stdout_stress_repeated_bogus_invocations_always_parseable_json(self):
        before = _snap(CANON)
        n = 20
        for _ in range(n):
            for cmd in (["scripts/tracka_resume_gate.py", "--bogus", "--json"],
                        ["scripts/tracka_resume_check.py", "--bogus"],
                        ["scripts/tracka_operator_report.py", "--bogus", "--json"]):
                res = _run([sys.executable] + cmd)
                self.assertNotEqual(res.returncode, 0, (cmd, res.stdout, res.stderr))
                out = json.loads(res.stdout.strip())
                self.assertEqual(out.get("status"), "BLOCKED", (cmd, out))
                self.assertNotIn("Traceback", json.dumps(out), cmd)
                for k in SAFE_FALSE:
                    self.assertFalse(out.get(k), (cmd, k, out))
        _unchanged(CANON, before)


class Test140CrossCliParityCanonicalIntegrity(unittest.TestCase):
    """(c) cross-CLI parity + canonical output integrity."""

    def _refusal_payload(self, cmd):
        res = _run([sys.executable] + cmd)
        self.assertNotEqual(res.returncode, 0, (cmd, res.stdout, res.stderr))
        out = json.loads(res.stdout.strip())
        self.assertIn(out.get("status"), ("BLOCKED", "NO-GO"), (cmd, out))
        return out, res.returncode

    def test_parity_bogus_flags_across_all_clis(self):
        before = _snap(CANON)
        payloads = []
        codes = []
        for cmd in (["scripts/tracka_resume_check.py", "--bogus"],
                    ["scripts/tracka_resume_gate.py", "--bogus", "--json"],
                    ["scripts/tracka_operator_report.py", "--bogus", "--json"]):
            out, code = self._refusal_payload(cmd)
            payloads.append(out)
            codes.append(code)
        # identical refusal structure / field types across CLIs
        for out in payloads:
            self.assertIsInstance(out.get("outcomes_inspected"), bool)
            self.assertIs(out.get("outcomes_inspected"), False)
            self.assertIsInstance(out.get("network"), bool)
            self.assertIs(out.get("network"), False)
            self.assertIsInstance(out.get("writes_real_research_state"), bool)
            self.assertIs(out.get("writes_real_research_state"), False)
            self.assertIn(out.get("reads_parquet"), (False, None))
            self.assertIn(out.get("reads_outcomes"), (False, None))
            self.assertIsInstance(out.get("reason_code"), str)
        self.assertTrue(all(c != 0 for c in codes), codes)
        _unchanged(CANON, before)

    def test_parity_malformed_admissible_manifest_across_all_clis(self):
        before = _snap(CANON)
        payloads = []
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "bad_adm.json"
            bad.write_text("{broken json!!! 140", encoding="utf-8")
            cmds = [
                ["scripts/tracka_resume_check.py", "--admissible-manifest", str(bad)],
                ["scripts/tracka_resume_gate.py", "--admissible-manifest", str(bad), "--json"],
                ["scripts/tracka_operator_report.py", "--admissible-manifest", str(bad), "--json"],
            ]
            for cmd in cmds:
                res = _run([sys.executable] + cmd)
                self.assertNotEqual(res.returncode, 0, (cmd, res.stdout, res.stderr))
                out = json.loads(res.stdout.strip())
                self.assertNotIn("Traceback", json.dumps(out), cmd)
                top_status = out.get("status")
                gate_status = (out.get("gate_decision") or {}).get("status")
                effective = top_status if top_status is not None else gate_status
                self.assertIn(effective, ("BLOCKED", "NO-GO"), (cmd, out))
                self.assertFalse(out.get("outcomes_inspected", False), cmd)
                self.assertFalse(out.get("reads_parquet", False), cmd)
                self.assertFalse(out.get("reads_outcomes", False), cmd)
                self.assertFalse(out.get("network", False), cmd)
                self.assertFalse(out.get("writes_real_research_state", False), cmd)
                payloads.append((out, res.returncode))
        for out, code in payloads:
            gate = out.get("gate_decision") or {}
            status = out.get("status") or gate.get("status")
            self.assertIn(status, ("BLOCKED", "NO-GO"), out)
            self.assertFalse(out.get("outcomes_inspected", False) or gate.get("outcomes_inspected") is True)
            self.assertFalse(out.get("network", False))
            self.assertFalse(out.get("writes_real_research_state", False))
            self.assertFalse(out.get("reads_parquet", False))
            self.assertFalse(out.get("reads_outcomes", False))
        self.assertTrue(all(code != 0 for _, code in payloads))
        _unchanged(CANON, before)

    def test_canonical_outputs_byte_identical_after_all_refusal_paths(self):
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            ap = _write_json(td / "adm.json", m)
            bad_adm = td / "bad_adm.json"; bad_adm.write_text("{broken json!!! 140")
            prereg = _valid_prereg(str(td))
            # malformed admissible manifest via check
            _run([sys.executable, "scripts/tracka_resume_check.py", "--admissible-manifest", str(bad_adm)])
            # bogus flags on all 3 CLIs
            _run([sys.executable, "scripts/tracka_resume_check.py", "--bogus"])
            _run([sys.executable, "scripts/tracka_resume_gate.py", "--bogus", "--json"])
            _run([sys.executable, "scripts/tracka_operator_report.py", "--bogus", "--json"])
            # nonexistent manifest file via gate
            _run([sys.executable, "scripts/tracka_resume_gate.py", "--manifest", "/nonexistent_140.json", "--json"])
        _unchanged(CANON, before)


class Test140GuardRefuseBeforeLoadMalformedAdmissible(unittest.TestCase):
    """(d) guarded_execute refuse-before-load on malformed admissible manifests."""

    def test_guarded_execute_malformed_admissible_manifest_loader_never_called(self):
        from scripts.fclr010_guarded_entry import guarded_execute
        loader_called = {"n": 0}

        def spy_loader(dp, ctx=None):
            loader_called["n"] += 1
            raise AssertionError("outcome loader must never be called on a blocked branch")

        before = _snap(CANON)
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "bad_adm.json"
            bad.write_text("{broken json!!! 140", encoding="utf-8")
            r = guarded_execute(
                data_path=Path(td) / "data",
                pre_reg_path=None,
                repo_root=REAL,
                admissible_manifest_path=str(bad),
                outcome_loader=spy_loader,
                loader_context=None,
                allow_default_loader=False,
            )
        self.assertEqual(r.get("status"), "BLOCKED", r)
        self.assertEqual(loader_called["n"], 0, "spy loader invoked on blocked branch")
        self.assertFalse(r.get("outcomes_inspected"), r)
        self.assertFalse(r.get("reads_parquet"), r)
        self.assertFalse(r.get("reads_outcomes"), r)
        self.assertFalse(r.get("network"), r)
        self.assertFalse(r.get("writes_real_research_state"), r)
        self.assertFalse(r.get("canonical_outputs_mutated"), r)
        self.assertIsNone(r.get("outcomes_loaded"), r)
        _unchanged(CANON, before)

    def test_guarded_execute_missing_prereg_valid_admissible_manifest_loader_never_called(self):
        from scripts.fclr010_guarded_entry import guarded_execute
        loader_called = {"n": 0}

        def spy_loader(dp, ctx=None):
            loader_called["n"] += 1
            raise AssertionError("outcome loader must never be called on a blocked branch")

        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            ap = _write_json(Path(td) / "adm.json", m)
            r = guarded_execute(
                data_path=Path(td) / "data",
                pre_reg_path=Path(td) / "nonexistent_prereg.json",
                repo_root=REAL,
                admissible_manifest=m,
                outcome_loader=spy_loader,
                allow_default_loader=False,
            )
        self.assertEqual(r.get("status"), "BLOCKED", r)
        self.assertEqual(r.get("reason_code"), BLOCKED_RC, r)
        self.assertEqual(loader_called["n"], 0, "spy loader invoked on blocked branch")
        self.assertFalse(r.get("outcomes_inspected"), r)
        self.assertFalse(r.get("reads_parquet"), r)
        self.assertFalse(r.get("reads_outcomes"), r)
        self.assertFalse(r.get("network"), r)
        self.assertFalse(r.get("writes_real_research_state"), r)
        self.assertFalse(r.get("canonical_outputs_mutated"), r)
        _unchanged(CANON, before)

    def test_admissible_manifest_missing_required_fields_seam_nogo_blocked(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness(repo_root=REAL)
        before = _snap(CANON)
        bad_m = dict(_valid_admissible_manifest())
        bad_m["observed_liquidations"] = False  # modeled/proxy conflation => seam NO-GO
        with tempfile.TemporaryDirectory() as td:
            prereg = _valid_prereg(td)
            r = h.evaluate_forward(Path(td) / "nodata", Path(td), pre_reg_path=prereg, admissible_manifest=bad_m)
        self.assertEqual(r.get("status"), "BLOCKED", r)
        self.assertIn(r.get("reason_code"), ("ADMISSIBLE_SEAM_NOGO_BEFORE_PREREG", "ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES", BLOCKED_RC), r)
        self.assertFalse(r.get("outcomes_inspected"), r)
        self.assertFalse(r.get("reads_parquet"), r)
        self.assertFalse(r.get("reads_outcomes"), r)
        self.assertFalse(r.get("network"), r)
        self.assertFalse(r.get("writes_real_research_state"), r)
        _unchanged(CANON, before)


if __name__ == "__main__":
    unittest.main()
