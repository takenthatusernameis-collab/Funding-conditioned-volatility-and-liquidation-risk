"""FCLR-NEXT-124: dep-light deterministic Track A hardening (NO TRIGGER).

G1: coupled_build_panel READY-path/cache write-scope allowlist; blocked NO-READY path
    must not invoke cache writes; tmp-sandboxed (no real research_state writes).
G2: evaluate_forward seam-GO + prereg present + data_path missing stable BLOCKED
    payload parity across direct/execute_ready_data_load/guarded_execute; no loader.
G3: h004 allowed-sandbox census/input path traversal (..) and symlink-escape
    fail-closed matrix before heavy work; stable reason_code/payload.
G4: coupled_build_panel runtime blocked NO-READY refusal emits full required fields
    (dep-light, no parquet/loader/canonical mutation).
G5: liqmicro_v2 write-guard divergence regression matrix preserved/extended
    (constant+arg+results_dir/research_state arg bypass attempts, denied targets).

No network, no parquet/outcome reads, no real research_state writes. Mock heavy deps.
"""
from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

REAL = Path(__file__).resolve().parents[1]
SCRIPTS = REAL / "scripts"

FRONTIER = REAL / "research_state" / "experiment_frontier.json"
RUN_MANIFEST = REAL / "research_state" / "run_manifest.json"
CROSS = REAL / "research_state" / "cross_track_decision_log.md"
EVAL_FCLR010 = REAL / "research_state" / "evaluation_summary_FCLR010.md"
EVAL_LIQM2 = REAL / "research_state" / "evaluation_summary_FCLR-LIQMICRO-002.md"
REQ_REFUSAL = {
    "status", "outcomes_inspected", "canonical_outputs_mutated", "network",
    "writes_real_research_state", "script", "reason_code",
}


def _snap(paths):
    return {str(p): (p.exists(), p.read_bytes() if p.exists() else b"") for p in paths}


def _unchanged(paths, before):
    for p in paths:
        k = str(p)
        ex = p.exists()
        b = p.read_bytes() if ex else b""
        assert (before[k][0], before[k][1]) == (ex, b), f"canonical output mutated: {p}"


def _loader_must_not_run(*a, **k):
    raise AssertionError("outcome/parquet loader invoked (forbidden on blocked/124 parity paths)")


def _mock_heavy():
    def _mk(name, attrs=None):
        m = types.ModuleType(name)
        for k, v in (attrs or {}).items():
            setattr(m, k, v)
        sys.modules[name] = m
        return m

    np = _mk("numpy", {"nan": float("nan"), "isnan": lambda x: False, "log1p": lambda x: x, "int64": int, "float64": float})
    np.ndarray = object
    pd = _mk("pandas")
    pd.DataFrame = object
    pd.Series = object
    pd.Timestamp = lambda *a, **k: None
    pd.to_datetime = lambda *a, **k: None
    pd.date_range = lambda *a, **k: []
    pd.MultiIndex = types.SimpleNamespace(from_product=lambda *a, **k: None)
    _mk("pyarrow")
    _mk("pyarrow.parquet", {"read_table": lambda *a, **k: (_ for _ in ()).throw(AssertionError("pyarrow read forbidden"))})
    # liqmicro chain (not exercised by 124 directly but keeps imports safe)
    for n in ["analysis", "analysis.liqmicro", "analysis.liqmicro.ingest", "analysis.liqmicro.features"]:
        _mk(n)
    sys.modules["analysis.liqmicro.ingest"].GuardedReadRefused = RuntimeError
    sys.modules["analysis.liqmicro.ingest"].IronflowIngestor = object
    sys.modules["analysis.liqmicro.ingest"].HyperliquidFundingIngestor = object
    sys.modules["analysis.liqmicro.features"].LiqMicroFeatures = object


class Test124G1CoupledBuildPanelCacheWriteScope(unittest.TestCase):
    """G1: coupled_build_panel cache write-scope allowlist + blocked-path nonwrite."""

    def setUp(self):
        _mock_heavy()
        sys.modules.pop("scripts.coupled_build_panel", None)
        self.mod = __import__("scripts.coupled_build_panel", fromlist=["_guard_coupled_cache_write_target"])

    def test_allowed_cache_artifact_passes(self):
        r = self.mod._guard_coupled_cache_write_target(self.mod.CACHE)
        self.assertTrue(r["pass"], r)
        self.assertEqual(r["reason_code"], "OK")
        self.assertFalse(r["network"])
        self.assertFalse(r["writes_real_research_state"])

    def test_rejects_repo_root_research_state_dir_wildcard_canonical(self):
        cases = [
            REAL,
            REAL / "research_state",
            REAL / "research_state" / "*.parquet",
            REAL / "research_state" / "run_manifest.json",
            REAL / "research_state" / "experiment_frontier.json",
            Path("/tmp/outside.parquet"),
        ]
        for c in cases:
            r = self.mod._guard_coupled_cache_write_target(c)
            self.assertFalse(r["pass"], (c, r))
            self.assertEqual(r["reason_code"], "COUPLED_CACHE_WRITE_SCOPE_VIOLATION", (c, r))

    def test_load_outcomes_refuses_before_write_on_scope_violation(self):
        # force write path by making CACHE "not exist" check irrelevant? easier: patch CACHE to bad target
        bad = REAL / "research_state" / "experiment_frontier.json"
        before = _snap([FRONTIER, RUN_MANIFEST, CROSS])
        with patch.object(self.mod, "CACHE", bad):
            # _load_coupled_outcomes reads parquet (mocked to raise AssertionError on read_table)
            # but scope guard runs before mkdir/to_parquet; if it somehow reached parquet read,
            # mock forbids. Guard must fail-closed on target scope.
            with self.assertRaises(self.mod.GuardedReadRefused) as ctx:
                # force=True bypasses cached-exists early return
                self.mod._load_coupled_outcomes(Path("/nonexistent_data"), {"force": True})
        self.assertIn("COUPLED_CACHE_WRITE_SCOPE_VIOLATION", str(ctx.exception))
        _unchanged([FRONTIER, RUN_MANIFEST, CROSS], before)

    def test_blocked_main_never_invokes_loader_or_writes(self):
        before = _snap([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010])
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value={
            "status": "BLOCKED", "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "outcomes_inspected": False, "canonical_outputs_mutated": False, "network": False,
            "writes_real_research_state": False,
        }), patch.object(self.mod, "_load_coupled_outcomes", _loader_must_not_run):
            with redirect_stdout(io.StringIO()):
                rc = self.mod.main()
        self.assertEqual(rc, 1)
        _unchanged([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010], before)

    def test_build_requires_explicit_loader(self):
        with self.assertRaises(self.mod.GuardedReadRefused):
            self.mod.build(force=False, outcome_loader=None)


class Test124G2EvaluateForwardSeamGoDataMissingParity(unittest.TestCase):
    """G2: seam-GO + prereg present + data_path missing => stable BLOCKED parity, no loader."""

    def test_direct_harness_parity(self):
        sys.modules.pop("scripts.fclr010_harness", None)
        sys.modules.pop("scripts.fclr010_guarded_entry", None)
        seam_ok = {"status": "GO", "pass": True, "reason_code": "ADMISSIBLE_SEAM_GO",
                   "failures": [], "network": False, "reads_outcomes": False, "reads_parquet": False}
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            tf.write(b"{}")
            prereg = Path(tf.name)
        try:
            with patch("scripts.tracka_resume_check.admissible_seam_check", return_value=seam_ok):
                from scripts.fclr010_harness import FCLR010Harness
                h = FCLR010Harness(repo_root=REAL)
                r = h.evaluate_forward(Path("/nonexistent_data_124"), REAL / "research_state",
                                       pre_reg_path=prereg, admissible_manifest={"dummy": True})
        finally:
            prereg.unlink(missing_ok=True)
        self.assertEqual(r["status"], "BLOCKED")
        self.assertEqual(r["reason_code"], "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")
        self.assertEqual(r.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING")
        self.assertTrue(r.get("seam_go_data_missing"))
        self.assertFalse(r["outcomes_inspected"])
        self.assertFalse(r.get("reads_parquet", False))
        self.assertIsNone(r.get("outcomes_loaded"))
        self.assertFalse(r["network"])

    def test_guarded_execute_and_ready_loader_no_loader_invoked(self):
        sys.modules.pop("scripts.fclr010_guarded_entry", None)
        from scripts.fclr010_guarded_entry import guarded_execute
        seam_ok = {"status": "GO", "pass": True, "reason_code": "ADMISSIBLE_SEAM_GO",
                   "failures": [], "network": False, "reads_outcomes": False, "reads_parquet": False}
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
            tf.write(b"{}")
            prereg = Path(tf.name)
        try:
            with patch("scripts.tracka_resume_check.admissible_seam_check", return_value=seam_ok):
                r = guarded_execute(data_path=Path("/nonexistent_data_124"), pre_reg_path=prereg,
                                    repo_root=REAL, admissible_manifest={"x": 1},
                                    outcome_loader=_loader_must_not_run, allow_default_loader=False)
        finally:
            prereg.unlink(missing_ok=True)
        self.assertEqual(r["status"], "BLOCKED")
        self.assertEqual(r["reason_code"], "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")
        self.assertEqual(r.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING")
        self.assertFalse(r["outcomes_inspected"])
        self.assertFalse(r["data_loaded_implicitly"])
        self.assertFalse(r["writes_real_research_state"])


class Test124G3H004TraversalSymlinkEscape(unittest.TestCase):
    """G3: h004 census/input traversal (..) and symlink-escape fail-closed."""

    def setUp(self):
        sys.modules.pop("scripts.h004_fclr005_pipeline", None)
        self.mod = __import__("scripts.h004_fclr005_pipeline", fromlist=["_h004_path_traversal_or_symlink_escape_guard"])

    def test_traversal_dotdot_refused(self):
        with tempfile.TemporaryDirectory() as td:
            sb = Path(td)
            bad = sb / "research_state" / "data_cache" / ".." / ".." / "etc" / "passwd.csv"
            r = self.mod._h004_path_traversal_or_symlink_escape_guard([bad], sandbox_root=sb)
            self.assertIsNotNone(r)
            self.assertEqual(r["reason_code"], "H004_CENSUS_INPUT_PATH_TRAVERSAL_OR_SYMLINK_ESCAPE")
            self.assertFalse(r["writes_real_research_state"])
            self.assertFalse(r["network"])

    def test_symlink_escape_refused(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as outside:
            sb = Path(td)
            (sb / "research_state" / "data_cache").mkdir(parents=True)
            tgt = Path(outside) / "secret.csv"
            tgt.write_text("x")
            link = sb / "research_state" / "data_cache" / "liquidations_full_20260807.csv"
            try:
                link.symlink_to(tgt)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            r = self.mod._h004_path_traversal_or_symlink_escape_guard([link], sandbox_root=sb)
            self.assertIsNotNone(r)
            self.assertEqual(r["reason_code"], "H004_CENSUS_INPUT_PATH_TRAVERSAL_OR_SYMLINK_ESCAPE")

    def test_main_refuses_traversal_before_heavy(self):
        with tempfile.TemporaryDirectory() as td:
            sb = Path(td)
            # path with traversal component under repo shape so relative_to preserves ..
            def _bad_inputs(repo=REAL):
                return [Path(repo) / "research_state" / "data_cache" / ".." / "escape.csv"]
            with patch.dict(os.environ, {"FCLR_ALLOW_H004_HISTORICAL_PILOT": "1", "FCLR_H004_SANDBOX_ROOT": str(sb)}, clear=False), \
                 patch.object(self.mod, "_h004_required_input_files", side_effect=_bad_inputs):
                with redirect_stdout(io.StringIO()) as buf:
                    rc = self.mod.main()
            self.assertEqual(rc, 1)
            p = json.loads(buf.getvalue())
            self.assertEqual(p["reason_code"], "H004_CENSUS_INPUT_PATH_TRAVERSAL_OR_SYMLINK_ESCAPE")
            self.assertFalse(p["writes_real_research_state"])


class Test124G4CoupledBuildPanelRuntimeRefusalFields(unittest.TestCase):
    """G4: coupled_build_panel runtime blocked NO-READY emits full required fields (dep-light)."""

    def test_runtime_blocked_payload_full_fields(self):
        _mock_heavy()
        sys.modules.pop("scripts.coupled_build_panel", None)
        mod = __import__("scripts.coupled_build_panel", fromlist=["main"])
        before = _snap([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010])
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value={
            "status": "BLOCKED", "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "outcomes_inspected": False, "canonical_outputs_mutated": False, "network": False,
            "writes_real_research_state": False,
        }), patch.object(mod, "_load_coupled_outcomes", _loader_must_not_run):
            with redirect_stdout(io.StringIO()) as buf:
                rc = mod.main()
        self.assertEqual(rc, 1)
        out = buf.getvalue()
        m = json.loads(out[out.index("{"):out.rindex("}") + 1])
        missing = REQ_REFUSAL - set(m.keys())
        self.assertFalse(missing, (missing, m))
        self.assertEqual(m["script"], "coupled_build_panel")
        self.assertFalse(m["outcomes_inspected"])
        self.assertFalse(m["writes_real_research_state"])
        self.assertFalse(m["network"])
        self.assertFalse(m["canonical_outputs_mutated"])
        _unchanged([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010], before)

    def test_source_emits_required_fields(self):
        src = (SCRIPTS / "coupled_build_panel.py").read_text()
        self.assertIn("refusal_payload", src)
        self.assertIn('"writes_real_research_state"', src)
        self.assertIn('"network"', src)
        self.assertIn('"canonical_outputs_mutated"', src)
        self.assertIn("_guard_coupled_cache_write_target", src)
        self.assertIn("COUPLED_CACHE_WRITE_SCOPE_VIOLATION", src)


class Test124G5LiqmicroV2WriteGuardMatrix(unittest.TestCase):
    """G5: liqmicro_v2 write-guard divergence regression matrix preserved/extended."""

    def setUp(self):
        # import with heavy deps mocked
        _mock_heavy()
        for n in list(sys.modules):
            if n.startswith("scripts.run_liqmicro_v2") or n.startswith("analysis"):
                sys.modules.pop(n, None)
        _mock_heavy()
        self.mod = __import__("scripts.run_liqmicro_v2", fromlist=["_guard_liqmicro_v2_write_targets", "RESULTS_DIR", "RESEARCH_STATE"])

    def test_policy_roots_pass(self):
        r = self.mod._guard_liqmicro_v2_write_targets()
        self.assertTrue(r["pass"], r)
        self.assertEqual(r["reason_code"], "OK")
        self.assertFalse(r["network"])

    def test_rejects_divergence_repo_root_rs_dir_wildcard_arbitrary(self):
        bad = [
            (REAL, self.mod.RESEARCH_STATE),  # repo root
            (self.mod.RESEARCH_STATE, self.mod.RESEARCH_STATE / "evaluation_summary_FCLR-LIQMICRO-002.md"),
            (self.mod.RESULTS_DIR, self.mod.RESEARCH_STATE / "*.md"),
            (REAL / "arbitrary_dir", self.mod.RESEARCH_STATE / "evaluation_summary_FCLR-LIQMICRO-002.md"),
        ]
        for roots in bad:
            r = self.mod._guard_liqmicro_v2_write_targets(
                results_dir=roots[0], research_state=self.mod.RESEARCH_STATE,
                allowed_write_roots=roots)
            self.assertFalse(r["pass"], (roots, r))

    def test_rejects_denied_targets_and_arg_bypass_attempts(self):
        # denied canonical in allowed roots
        r = self.mod._guard_liqmicro_v2_write_targets(
            allowed_write_roots=(REAL / "research_state" / "run_manifest.json",))
        self.assertFalse(r["pass"], r)
        # monkeypatch-constant divergence path is validated (effective roots checked)
        with patch.object(self.mod, "LIQMICRO_V2_ALLOWED_WRITE_ROOTS", (REAL, self.mod.RESEARCH_STATE)):
            r2 = self.mod._guard_liqmicro_v2_write_targets()
        self.assertFalse(r2["pass"], r2)

    def test_results_dir_specific_allowed_only(self):
        # exact results dir root remains policy-compatible as results root component
        r = self.mod._guard_liqmicro_v2_write_targets(
            results_dir=self.mod.RESULTS_DIR, research_state=self.mod.RESEARCH_STATE,
            allowed_write_roots=(self.mod.RESULTS_DIR, self.mod.RESEARCH_STATE / "evaluation_summary_FCLR-LIQMICRO-002.md"))
        self.assertTrue(r["pass"], r)


if __name__ == "__main__":
    unittest.main()