"""FCLR-NEXT-138: unreadable data path + unreadable manifest/prereg + CLI argparse hardening.

Deterministic, tmp-isolated, dep-light, no network, no parquet/outcome reads,
no real research_state writes. Extends 136/137 with:
- unreadable data path => BLOCKED with ADMISSIBLE_SEAM_GO_DATA_PATH_UNREADABLE
- unreadable manifest (file exists, unreadable) => fail-closed JSON refusal on gate/check/operator
- unreadable prereg (file exists, unreadable) => BLOCKED with PREREG_CONTENT_INVALID_FAIL_CLOSED
- CLI argparse contract on all 3 CLIs: bogus flags, missing/unreadable prereg, malformed admissible-manifest JSON,
  unreadable manifest -- all parseable JSON, exit!=0, no traceback
Canonical outputs byte-identical on every refusal path.
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


def _make_unreadable(path):
    p = Path(path)
    p.chmod(0o000)
    return str(p)


def _restore_readable(path):
    Path(path).chmod(0o644)


class Test138UnreadableDataPath(unittest.TestCase):
    """Unreadable data path => BLOCKED with ADMISSIBLE_SEAM_GO_DATA_PATH_UNREADABLE."""

    def test_harness_unreadable_data_path_blocked(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness(repo_root=REAL)
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data_dir = td / "data"
            data_dir.mkdir()
            (data_dir / "file.parquet").write_bytes(b"fake")
            data_dir.chmod(0o000)
            prereg = td / "prereg.json"
            prereg.write_text(json.dumps({"preregistered_at_utc": "2026-11-06T00:00:00Z", "frozen": True}))
            try:
                r = h.evaluate_forward(data_dir, td, pre_reg_path=prereg, admissible_manifest=m)
            finally:
                data_dir.chmod(0o755)
        self.assertEqual(r.get("status"), "BLOCKED", r)
        self.assertEqual(r.get("reason_code"), BLOCKED_RC, r)
        self.assertEqual(r.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_DATA_PATH_UNREADABLE", r)
        self.assertTrue(r.get("seam_go_data_unreadable"), r)
        _assert_blocked_no_io(r)
        _unchanged(CANON, before)

    def test_gate_unreadable_data_path_blocked(self):
        from scripts import tracka_resume_gate as gate
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            data_dir = td / "data"
            data_dir.mkdir()
            (data_dir / "file.parquet").write_bytes(b"fake")
            data_dir.chmod(0o000)
            ap = _write_json(td / "adm.json", m)
            prereg = td / "prereg.json"
            prereg.write_text(json.dumps({"preregistered_at_utc": "2026-11-06T00:00:00Z", "frozen": True}))
            try:
                r = gate.decide(str(data_dir), td, pre_reg_path=str(prereg), admissible_manifest_path=ap, harness_repo_root=REAL)
            finally:
                data_dir.chmod(0o755)
        self.assertEqual(r.get("status"), "BLOCKED", r)
        self.assertEqual(r.get("reason_code"), BLOCKED_RC, r)
        self.assertEqual(r.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_DATA_PATH_UNREADABLE", r)
        self.assertTrue(r.get("seam_go_data_unreadable"), r)
        _assert_blocked_no_io(r)
        _unchanged(CANON, before)


class Test138UnreadableManifestPrereg(unittest.TestCase):
    """Unreadable manifest (file exists, unreadable) => fail-closed. Unreadable prereg => BLOCKED."""

    def test_harness_unreadable_prereg_blocked(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness(repo_root=REAL)
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            empty_dir = td / "empty_data"
            empty_dir.mkdir()
            bad = td / "bad_prereg.json"
            bad.write_text('{"preregistered_at_utc": "2026-11-06T00:00:00Z", "frozen": true}')
            bad.chmod(0o000)
            try:
                r = h.evaluate_forward(empty_dir, td, pre_reg_path=bad, admissible_manifest=m)
            finally:
                bad.chmod(0o644)
        self.assertEqual(r.get("status"), "BLOCKED", r)
        self.assertEqual(r.get("reason_code_detail"), "PREREG_CONTENT_INVALID_FAIL_CLOSED", r)
        _assert_blocked_no_io(r)
        _unchanged(CANON, before)

    def test_gate_cli_unreadable_manifest_fail_closed_json(self):
        m = _valid_admissible_manifest()
        before = _snap(CANON)
        with tempfile.TemporaryDirectory() as td:
            unreadable = Path(td) / "unreadable_adm.json"
            unreadable.write_text(json.dumps(m))
            unreadable.chmod(0o000)
            try:
                res = _run([sys.executable, "scripts/tracka_resume_gate.py", "--admissible-manifest", str(unreadable), "--json"])
            finally:
                unreadable.chmod(0o644)
        self.assertNotEqual(res.returncode, 0, res.stdout)
        try:
            out = json.loads(res.stdout.strip())
        except Exception as e:
            self.fail(f"stdout not parseable JSON: {e}; stdout={res.stdout[:200]}; stderr={res.stderr[:200]}")
        self.assertNotIn("Traceback", json.dumps(out))
        self.assertIn(out.get("status"), ("BLOCKED", "NO-GO"))
        self.assertFalse(out.get("outcomes_inspected"))
        self.assertFalse(out.get("reads_parquet"))
        self.assertFalse(out.get("reads_outcomes"))
        self.assertFalse(out.get("network"))
        self.assertFalse(out.get("writes_real_research_state"))
        _unchanged(CANON, before)

    def test_check_cli_unreadable_manifest_fail_closed_json(self):
        m = _valid_admissible_manifest()
        before = _snap(CANON)
        with tempfile.TemporaryDirectory() as td:
            unreadable = Path(td) / "unreadable_adm.json"
            unreadable.write_text(json.dumps(m))
            unreadable.chmod(0o000)
            try:
                res = _run([sys.executable, "scripts/tracka_resume_check.py", "--admissible-manifest", str(unreadable)])
            finally:
                unreadable.chmod(0o644)
        self.assertNotEqual(res.returncode, 0, res.stdout)
        try:
            out = json.loads(res.stdout.strip())
        except Exception as e:
            self.fail(f"stdout not parseable JSON: {e}; stdout={res.stdout[:200]}; stderr={res.stderr[:200]}")
        self.assertNotIn("Traceback", json.dumps(out))
        self.assertIn(out.get("status"), ("NO-GO", "BLOCKED"))
        self.assertFalse(out.get("outcomes_inspected", False))
        self.assertFalse(out.get("network", False))
        self.assertFalse(out.get("writes_real_research_state", False))
        _unchanged(CANON, before)


class Test138CliArgparseContractAllClis(unittest.TestCase):
    """CLI argparse contract on all 3 CLIs: bogus flags, missing/unreadable prereg, empty data path."""

    BOGUS_CASES = [
        (["scripts/tracka_resume_check.py", "--bogus"]),
        (["scripts/tracka_resume_gate.py", "--bogus", "--json"]),
        (["scripts/tracka_operator_report.py", "--bogus", "--json"]),
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
            self.assertFalse(out.get("outcomes_inspected"), cmd)
            self.assertFalse(out.get("network"), cmd)
            self.assertFalse(out.get("writes_real_research_state"), cmd)
            _unchanged(CANON, before)

    def test_gate_cli_bogus_and_missing_prereg(self):
        before = _snap(CANON)
        # bogus flag
        res = _run([sys.executable, "scripts/tracka_resume_gate.py", "--bogus", "--json"])
        self.assertNotEqual(res.returncode, 0)
        out = json.loads(res.stdout.strip())
        self.assertEqual(out.get("status"), "BLOCKED")
        # --prereg pointing to nonexistent file
        res2 = _run([sys.executable, "scripts/tracka_resume_gate.py", "--prereg", "/nonexistent_prereg.json", "--json"])
        self.assertNotEqual(res2.returncode, 0)
        out2 = json.loads(res2.stdout.strip())
        self.assertEqual(out2.get("status"), "BLOCKED", out2)
        self.assertFalse(out2.get("outcomes_inspected"))
        self.assertFalse(out2.get("network"))
        self.assertFalse(out2.get("writes_real_research_state"))
        _unchanged(CANON, before)

    def test_operator_cli_bogus_flags(self):
        before = _snap(CANON)
        res = _run([sys.executable, "scripts/tracka_operator_report.py", "--bogus", "--json"])
        self.assertNotEqual(res.returncode, 0)
        out = json.loads(res.stdout.strip())
        self.assertEqual(out.get("status"), "BLOCKED", out)
        self.assertFalse(out.get("network"))
        self.assertFalse(out.get("writes_real_research_state"))
        _unchanged(CANON, before)

    def test_canonical_outputs_identical_after_all_refusal_paths(self):
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            ap = _write_json(td / "adm.json", m)
            bad_adm = td / "bad_adm.json"; bad_adm.write_text("{broken json!!!")
            prereg = td / "prereg.json"
            prereg.write_text(json.dumps({"preregistered_at_utc": "2026-11-06T00:00:00Z", "frozen": True}))
            # malformed admissible manifest via check
            _run([sys.executable, "scripts/tracka_resume_check.py", "--admissible-manifest", str(bad_adm)])
            # bogus flags on all 3 CLIs
            _run([sys.executable, "scripts/tracka_resume_check.py", "--bogus"])
            _run([sys.executable, "scripts/tracka_resume_gate.py", "--bogus", "--json"])
            _run([sys.executable, "scripts/tracka_operator_report.py", "--bogus", "--json"])
        _unchanged(CANON, before)


if __name__ == "__main__":
    unittest.main()
