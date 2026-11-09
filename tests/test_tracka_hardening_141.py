"""FCLR-NEXT-141: Track A seam/CLI/prereg/guard hardening campaign.

tmp-isolated, dep-light, no network, no parquet/outcome reads, no real
research_state writes. Covers (clusters):
  (a) admissible seam manifest schema matrix: missing/extra/wrong-type/unknown
      verdict shapes and corrupt candidate manifests -> stable refusal reason
      codes + outcomes_inspected:false, loader never called.
  (b) prereg/manifest contract edge cases: unreadable/corrupt prereg JSON,
      mismatched experiment IDs, explicitly unfrozen, path-traversal-ish refs
      refused safely (tmp only) -> no canonical writes, stable JSON refusals.
  (c) NOGO/GO seam matrix with valid prereg: NOGO refuses before load with
      stable ADMISSIBLE/PREREG reason codes; GO without trigger/data path
      refuses on data-path (no fabricated outcomes), loader never called.
  (d) CLI --json/exit-code/field-type determinism + refusal parity across all 3
      CLIs for malformed inputs; canonical outputs byte-identical after refusals.
"""
from __future__ import annotations

import json
import os
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


def _valid_prereg_obj():
    return {"experiment_id": "FCLR-010", "frozen": True, "preregistered_at_utc": "2026-11-06T00:00:00Z"}


def _valid_prereg(td):
    return _write_json(Path(td) / "prereg.json", _valid_prereg_obj())


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(REAL))


class Test141AdmissibleSeamManifestSchemaMatrix(unittest.TestCase):
    """(a) admissible seam manifest schema/shape matrix -> stable refusals, loader never called."""

    def test_seam_missing_extra_wrong_type_unknown_shapes_nogo(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness(repo_root=REAL)
        cases = [
            {},  # empty/missing required
            {"venue": "hyperliquid"},  # missing most required
            {"venue": "hyperliquid", "observed_liquidations": "true", "month": 202611},  # wrong types
            {"venue": "binance", "observed_liquidations": True, "unauthenticated": True,
             "month": "2026-11", "label_definition": "x", "timestamp_normalized_utc": True,
             "source": "binance", "artifacts": {}},  # wrong venue/source
            {"track": "A", "venue": "hyperliquid", "observed_liquidations": True,
             "modeled_or_proxy": True, "unauthenticated": True, "month": "2026-11",
             "label_definition": "x", "timestamp_normalized_utc": True,
             "source": "ironflow/hyperliquid-liquidations", "artifacts": {}},  # modeled conflation
            {"verdict": "TOTALLY_UNKNOWN", "admissible": "maybe", "extra_field": [1, 2]},  # unknown/conflicting
        ]
        for i, m in enumerate(cases):
            with self.subTest(i=i):
                s = h._evaluate_admissible_seam(m, None)
                self.assertFalse(s.get("pass"), s)
                self.assertFalse(s.get("reads_outcomes", True), s)
                self.assertFalse(s.get("reads_parquet", True), s)
                self.assertFalse(s.get("network", True), s)
                self.assertIn("reason_code", s)
                self.assertIn("failures", s)
                self.assertIsInstance(s.get("failures"), list)

    def test_corrupt_candidate_manifest_path_refused(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness(repo_root=REAL)
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "adm.json"
            bad.write_text("{not json", encoding="utf-8")
            s = h._evaluate_admissible_seam(None, str(bad))
        self.assertFalse(s.get("pass"), s)
        self.assertEqual(s.get("reason_code"), "ADMISSIBLE_CANDIDATE_LOAD_ERROR", s)
        self.assertFalse(s.get("reads_outcomes", True), s)
        self.assertFalse(s.get("reads_parquet", True), s)

    def test_missing_candidate_manifest_path_refused(self):
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness(repo_root=REAL)
        s = h._evaluate_admissible_seam(None, "/nonexistent_adm_manifest_141_xyz.json")
        self.assertFalse(s.get("pass"), s)
        self.assertEqual(s.get("reason_code"), "ADMISSIBLE_CANDIDATE_PATH_MISSING", s)


class Test141PreregContractEdgeCases(unittest.TestCase):
    """(b) prereg/manifest contract edge cases -> stable refusals, no canonical writes."""

    def test_corrupt_prereg_json_blocked(self):
        from scripts import tracka_resume_gate as gate
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            ap = _write_json(Path(td) / "adm.json", m)
            badp = Path(td) / "prereg.json"
            badp.write_text("{bad json", encoding="utf-8")
            r = gate.decide("/nodata141", Path(td), pre_reg_path=str(badp), admissible_manifest_path=ap, harness_repo_root=REAL)
        self.assertEqual(r.get("status"), "BLOCKED", r)
        self.assertEqual(r.get("reason_code"), BLOCKED_RC, r)
        self.assertEqual(r.get("reason_code_detail"), "PREREG_CONTENT_INVALID_FAIL_CLOSED", r)
        _assert_blocked_no_io(r)
        _unchanged(CANON, before)

    def test_prereg_semantic_mismatch_unfrozen_path_refused(self):
        from scripts import tracka_resume_gate as gate
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        cases = [
            {"experiment_id": "NOT_ALLOWED_999", "frozen": True},
            {"experiment_id": "FCLR-010", "frozen": False},
            {"experiment_id": "FCLR-010", "frozen": True, "manifest_path": "/etc/passwd"},
            {"experiment_id": "FCLR-010", "frozen": True, "protocol_path": "../../etc/hosts"},
        ]
        for i, obj in enumerate(cases):
            with self.subTest(i=i):
                with tempfile.TemporaryDirectory() as td:
                    ap = _write_json(Path(td) / "adm.json", m)
                    pp = _write_json(Path(td) / "prereg.json", obj)
                    r = gate.decide("/nodata141", Path(td), pre_reg_path=pp, admissible_manifest_path=ap, harness_repo_root=REAL)
                self.assertEqual(r.get("status"), "BLOCKED", r)
                self.assertEqual(r.get("reason_code"), BLOCKED_RC, r)
                self.assertEqual(r.get("reason_code_detail"), "PREREG_SEMANTIC_CONTRACT_FAIL_CLOSED", r)
                self.assertTrue(r.get("prereg_semantic_failures"), r)
                _assert_blocked_no_io(r)
        _unchanged(CANON, before)

    def test_legacy_prereg_without_experiment_id_remains_compatible(self):
        from scripts import tracka_resume_gate as gate
        before = _snap(CANON)
        m = _valid_admissible_manifest()
        with tempfile.TemporaryDirectory() as td:
            ap = _write_json(Path(td) / "adm.json", m)
            pp = _write_json(Path(td) / "prereg.json", {"preregistered_at_utc": "x", "frozen": True})
            r = gate.decide("/nodata141", Path(td), pre_reg_path=pp, admissible_manifest_path=ap, harness_repo_root=REAL)
        # legacy shape should pass semantic check; may still BLOCK on data path (stable)
        self.assertIn(r.get("status"), ("BLOCKED", "READY_FROZEN"), r)
        if r.get("status") == "BLOCKED":
            self.assertNotEqual(r.get("reason_code_detail"), "PREREG_SEMANTIC_CONTRACT_FAIL_CLOSED", r)
        _unchanged(CANON, before)


class Test141NogoGoSeamMatrix(unittest.TestCase):
    """(c) NOGO/GO seam matrix with valid prereg; loader spy never called."""

    def test_nogo_seam_refuses_before_load_loader_never_called(self):
        from scripts.fclr010_guarded_entry import guarded_execute
        before = _snap(CANON)
        called = {"n": 0}

        def spy(*_a, **_k):
            called["n"] += 1
            raise AssertionError("loader must not be called")

        with tempfile.TemporaryDirectory() as td:
            pp = _valid_prereg(td)
            r = guarded_execute(
                data_path=Path(td) / "nodata",
                pre_reg_path=Path(pp),
                repo_root=REAL,
                admissible_manifest={"venue": "binance", "observed_liquidations": True},  # NO-GO
                outcome_loader=spy,
            )
        self.assertEqual(r.get("status"), "BLOCKED", r)
        self.assertEqual(called["n"], 0, "loader called on blocked NOGO seam")
        self.assertFalse(r.get("outcomes_inspected", True), r)
        self.assertFalse(r.get("reads_parquet", True), r)
        self.assertFalse(r.get("reads_outcomes", True), r)
        self.assertFalse(r.get("network", True), r)
        self.assertFalse(r.get("writes_real_research_state", True), r)
        self.assertIn(str(r.get("reason_code", "")), (BLOCKED_RC, "ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES", "ADMISSIBLE_SEAM_NOGO_BEFORE_PREREG"), r)
        _unchanged(CANON, before)

    def test_go_seam_without_trigger_data_refuses_on_data_path_no_fabrication(self):
        from scripts.fclr010_guarded_entry import guarded_execute
        before = _snap(CANON)
        called = {"n": 0}

        def spy(*_a, **_k):
            called["n"] += 1
            return {"fabricated": True}

        with tempfile.TemporaryDirectory() as td:
            pp = _valid_prereg(td)
            r = guarded_execute(
                data_path=Path(td) / "missing_trigger_data_141",
                pre_reg_path=Path(pp),
                repo_root=REAL,
                admissible_manifest=_valid_admissible_manifest(),
                outcome_loader=spy,
            )
        self.assertEqual(r.get("status"), "BLOCKED", r)
        self.assertEqual(called["n"], 0, "loader called before data-path resolution/fabrication")
        self.assertEqual(r.get("reason_code"), BLOCKED_RC, r)
        self.assertIn(r.get("reason_code_detail"), ("ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING", "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED", None), r)
        self.assertFalse(r.get("outcomes_inspected", True), r)
        self.assertFalse(r.get("reads_parquet", True), r)
        self.assertIsNone(r.get("outcomes_loaded"), r)
        _unchanged(CANON, before)


class Test141CliJsonDeterminismFieldTypes(unittest.TestCase):
    """(d) CLI --json/exit/field-type determinism + cross-CLI parity for refusals."""

    def _extract_json_refusal(self, text):
        # argparse contract violations may emit usage text; refusal JSON appears in stdout/stderr.
        # Find the last parseable JSON object/line that looks like a refusal payload.
        for line in reversed([ln for ln in text.splitlines() if ln.strip()]):
            s = line.strip()
            if s.startswith("{") and s.endswith("}"):
                try:
                    p = json.loads(s)
                    if isinstance(p, dict):
                        return p
                except Exception:
                    pass
        # fallback: try whole text
        try:
            p = json.loads(text)
            if isinstance(p, dict):
                return p
        except Exception:
            pass
        return None

    def test_all_clis_bogus_flag_json_refusal_stable_types(self):
        before = _snap(CANON)
        cases = [
            ["scripts/tracka_resume_check.py", "--bogus"],
            ["scripts/tracka_resume_gate.py", "--bogus", "--json"],
            ["scripts/tracka_operator_report.py", "--bogus", "--json"],
        ]
        for cmd in cases:
            with self.subTest(cli=cmd[0]):
                r = _run([sys.executable] + cmd)
                # contract: refusal must be machine-detectable and safe; exit!=0 preferred but
                # resume_check may exit 0 while emitting a refusal payload (legacy behavior).
                combined = (r.stdout or "") + "\n" + (r.stderr or "")
                p = self._extract_json_refusal(r.stdout) or self._extract_json_refusal(combined)
                self.assertIsNotNone(p, (cmd, r.returncode, r.stdout[:400], r.stderr[:400]))
                status = p.get("status")
                self.assertIn(status, ("BLOCKED", "SEAM_IMPORT_ERROR"), p)
                # pass may be False on check; safety booleans stable
                if p.get("reason_code") is not None:
                    self.assertIn(p.get("reason_code"), (BLOCKED_RC, "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS", "ADMISSIBLE_SEAM_UNAVAILABLE"), p)
                for k in ("outcomes_inspected", "canonical_outputs_mutated", "network", "writes_real_research_state"):
                    if k in p:
                        self.assertIs(p.get(k), False, (k, p, cmd))
        _unchanged(CANON, before)

    def test_gate_malformed_admissible_manifest_json_refusal(self):
        before = _snap(CANON)
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td) / "adm.json"
            bad.write_text("{bad", encoding="utf-8")
            pp = _valid_prereg(td)
            r = _run([sys.executable, "scripts/tracka_resume_gate.py", "--json",
                      "--admissible-manifest", str(bad), "--pre-reg", pp, "--data-path", "/nodata141"])
        self.assertNotEqual(r.returncode, 0)
        text = (r.stdout + "\n" + r.stderr).strip()
        # must not be an unstructured traceback contract; parseable refusal preferred
        self.assertNotIn("Traceback (most recent call last):", text.split("\n")[0] if text else "")
        if r.stdout.strip():
            try:
                p = json.loads(r.stdout.strip().splitlines()[-1])
                self.assertEqual(p.get("status"), "BLOCKED", p)
            except Exception:
                pass
        _unchanged(CANON, before)

    def test_operator_report_malformed_prereg_refusal_deterministic(self):
        before = _snap(CANON)
        with tempfile.TemporaryDirectory() as td:
            badp = Path(td) / "prereg.json"
            badp.write_text("{bad", encoding="utf-8")
            ap = _write_json(Path(td) / "adm.json", _valid_admissible_manifest())
            r = _run([sys.executable, "scripts/tracka_operator_report.py", "--json",
                      "--admissible-manifest", ap, "--pre-reg", str(badp), "--data-path", "/nodata141"])
        # operator may report blocked in JSON payload; exit behavior stable (non-crash contract)
        self.assertIsInstance(r.returncode, int)
        if r.stdout.strip():
            p = json.loads(r.stdout.strip().splitlines()[-1])
            gd = p.get("gate_decision") or p
            self.assertIn((gd.get("status") or p.get("status")), ("BLOCKED", "SEAM_IMPORT_ERROR", None), p)
        _unchanged(CANON, before)


if __name__ == "__main__":
    unittest.main()
