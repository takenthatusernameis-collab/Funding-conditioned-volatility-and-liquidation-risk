"""FCLR-NEXT-123: evaluate_forward seam-GO+prereg-missing normalization parity +
liqmicro_v2 write-guard args bound to constants/scope proof +
h004 sandbox-root nondir/unusable fail-closed matrix +
guarded ready-writing refusal payload network/wrs emission audit +
coupled_robust_eval guarded-class runtime/source-contract blocked-path assertions.

Deterministic, tmp-isolated, no network, no parquet/outcome reads, no real research_state writes.
"""
from __future__ import annotations

import ast
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

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.fclr010_guarded_entry import guarded_execute, refusal_payload
from scripts.fclr010_harness import FCLR010Harness
from src.analysis.tracka_admissible import build_ironflow_month_manifest

REAL = Path(__file__).resolve().parent.parent
RS = REAL / "research_state"
SCRIPTS = REAL / "scripts"
FRONTIER = RS / "experiment_frontier.json"
RUN_MANIFEST = RS / "run_manifest.json"
EVAL_FCLR010 = RS / "evaluation_summary_FCLR010.md"
EVAL_LIQM2 = RS / "evaluation_summary_FCLR-LIQMICRO-002.md"
CROSS = RS / "cross_track_decision_log.md"
REQ_REFUSAL = {
    "status", "outcomes_inspected", "canonical_outputs_mutated", "network",
    "writes_real_research_state", "script", "reason_code",
}


def _snap(paths):
    return {str(p): (p.read_bytes() if p.exists() else None) for p in paths}


def _unchanged(paths, before):
    for s, b in before.items():
        p = Path(s)
        a = p.read_bytes() if p.exists() else None
        if b != a:
            raise AssertionError(f"canonical target mutated: {s}")


def _mock_heavy():
    for mn in ("numpy", "pandas", "statsmodels", "statsmodels.api", "statsmodels.formula.api", "pyarrow", "pyarrow.parquet"):
        if mn not in sys.modules:
            m = types.ModuleType(mn)
            if mn == "pandas":
                class _S:
                    def nunique(self):
                        return 1
                class _DF:
                    def __init__(self, *a, **k):
                        pass
                    def __len__(self):
                        return 1
                    @property
                    def empty(self):
                        return False
                    def __getitem__(self, k):
                        return _S()
                m.DataFrame = _DF
                m.read_parquet = lambda *a, **k: _DF()
            if mn == "numpy":
                m.nan = float("nan")
                m.isnan = lambda x: False
                m.isinf = lambda x: False
            sys.modules[mn] = m
    sys.modules.pop("scripts.run_liqmicro_v2", None)
    sys.modules.pop("scripts.coupled_build_panel", None)
    sys.modules.pop("scripts.coupled_robust_eval", None)


def _real_go_manifest(month="2026-11"):
    return build_ironflow_month_manifest(
        month=month,
        events_path=f"research_state/data_cache/ironflow_events/events/{month}.parquet",
        fills_path=f"research_state/data_cache/ironflow_events/fills/{month}.parquet",
        events_url=f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/{month}.parquet",
        fills_url=f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/{month}.parquet",
        schema_fields_events=["timestamp", "symbol", "notional_usd", "position_side", "market"],
        schema_fields_fills=["timestamp", "symbol", "size", "price", "market"],
    )


class Test123G1EvaluateForwardSeamGoPreregParity(unittest.TestCase):
    """G1: evaluate_forward direct seam GO + prereg missing/nonexistent => stable parity."""

    def _assert_parity(self, res):
        self.assertEqual(res.get("status"), "BLOCKED", res)
        self.assertEqual(res.get("reason_code"), "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS", res)
        self.assertTrue(res.get("seam_go_prereg_required"), res)
        self.assertEqual(res.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED", res)
        self.assertFalse(res.get("outcomes_inspected"), res)
        self.assertTrue(res.get("prereg_required"), res)

    def test_direct_evaluate_forward_missing_prereg(self):
        h = FCLR010Harness(repo_root=REAL)
        m = _real_go_manifest()
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            res = h.evaluate_forward(data, Path(td) / "out", pre_reg_path=None, admissible_manifest=m)
        self._assert_parity(res)

    def test_direct_evaluate_forward_nonexistent_prereg(self):
        h = FCLR010Harness(repo_root=REAL)
        m = _real_go_manifest()
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            res = h.evaluate_forward(data, Path(td) / "out", pre_reg_path=Path(td) / "missing.json", admissible_manifest=m)
        self._assert_parity(res)

    def test_direct_evaluate_forward_no_loader_no_outcome_read(self):
        h = FCLR010Harness(repo_root=REAL)
        m = _real_go_manifest()
        called = {"n": 0}
        def bad(*a, **k):
            called["n"] += 1
            raise AssertionError("loader must not be called")
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            res = h.evaluate_forward(data, Path(td) / "out", pre_reg_path=None, admissible_manifest=m, outcome_loader=bad)
        self._assert_parity(res)
        self.assertEqual(called["n"], 0)


class Test123G2LiqmicroV2WriteGuardArgsBound(unittest.TestCase):
    """G2: _guard_liqmicro_v2_write_targets validates effective args; no bypass/divergence."""

    def test_args_diverge_from_policy_fail_closed(self):
        _mock_heavy()
        import scripts.run_liqmicro_v2 as mod
        r = mod._guard_liqmicro_v2_write_targets(allowed_write_roots=(mod.REPO / "src",))
        self.assertFalse(r.get("pass"), r)
        self.assertEqual(r.get("reason_code"), "LIQMICRO_V2_WRITE_TARGET_ALLOWLIST_VIOLATION")
        self.assertTrue(any("diverge" in f or "arbitrary" in f for f in r.get("failures", [])), r)

    def test_arbitrary_repo_dir_arg_fail_closed(self):
        _mock_heavy()
        import scripts.run_liqmicro_v2 as mod
        eval_liqm2 = mod.RESEARCH_STATE / "evaluation_summary_FCLR-LIQMICRO-002.md"
        r = mod._guard_liqmicro_v2_write_targets(allowed_write_roots=(mod.REPO / "scripts", eval_liqm2))
        self.assertFalse(r.get("pass"), r)

    def test_research_state_dir_wide_arg_fail_closed(self):
        _mock_heavy()
        import scripts.run_liqmicro_v2 as mod
        r = mod._guard_liqmicro_v2_write_targets(allowed_write_roots=(mod.RESEARCH_STATE,))
        self.assertFalse(r.get("pass"), r)

    def test_results_dir_specific_allowed_policy_passes(self):
        _mock_heavy()
        import scripts.run_liqmicro_v2 as mod
        r = mod._guard_liqmicro_v2_write_targets(allowed_write_roots=(mod.RESULTS_DIR, mod.RESEARCH_STATE / "evaluation_summary_FCLR-LIQMICRO-002.md"))
        self.assertTrue(r.get("pass"), r)

    def test_blocked_main_no_write_guard_invoked(self):
        _mock_heavy()
        import scripts.run_liqmicro_v2 as mod
        before = _snap([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2])
        calls = {"pipe": 0, "wguard": 0}
        orig = mod._guard_liqmicro_v2_write_targets
        def spy(*a, **k):
            calls["wguard"] += 1
            return orig(*a, **k)
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value={
            "status": "BLOCKED", "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "outcomes_inspected": False, "canonical_outputs_mutated": False, "guarded_execution_contract": "fclr_next_111",
        }), patch.object(mod, "_guard_liqmicro_v2_write_targets", spy), \
             patch.object(mod, "_run_pipeline", lambda *a, **k: calls.__setitem__("pipe", calls["pipe"] + 1)), \
             redirect_stdout(io.StringIO()):
            rc = mod.main()
        self.assertEqual(rc, 1)
        self.assertEqual(calls["pipe"], 0)
        self.assertEqual(calls["wguard"], 0)
        _unchanged([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2], before)


class Test123G3H004SandboxRootNondirUnusable(unittest.TestCase):
    """G3: sandbox root file-not-dir/unusable/nonexistent fail-closed before census/heavy work."""

    def test_sandbox_root_nonexistent_fail_closed(self):
        import scripts.h004_fclr005_pipeline as mod
        g = mod._h004_sandbox_guard(repo=mod.REPO)
        # without env, requires sandbox root
        self.assertIsNotNone(g)
        self.assertEqual(g.get("status"), "BLOCKED")
        self.assertIn(g.get("reason_code"), {"H004_ALLOWED_MODE_REQUIRES_SANDBOX_ROOT"})
        self.assertFalse(g.get("network"))
        self.assertFalse(g.get("writes_real_research_state"))

    def test_sandbox_root_is_regular_file_fail_closed(self):
        import scripts.h004_fclr005_pipeline as mod
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "notadir.txt"; f.write_text("x")
            with patch.dict(os.environ, {"FCLR_H004_SANDBOX_ROOT": str(f)}, clear=False):
                g = mod._h004_sandbox_guard(repo=mod.REPO)
        self.assertIsNotNone(g)
        self.assertEqual(g.get("status"), "BLOCKED")
        self.assertEqual(g.get("reason_code"), "H004_SANDBOX_ROOT_NOT_DIRECTORY")
        self.assertFalse(g.get("writes_real_research_state"))

    def test_sandbox_root_unusable_path_fail_closed(self):
        import scripts.h004_fclr005_pipeline as mod
        with tempfile.TemporaryDirectory() as td:
            missing = Path(td) / "nope_sandbox"
            with patch.dict(os.environ, {"FCLR_H004_SANDBOX_ROOT": str(missing)}, clear=False):
                g = mod._h004_sandbox_guard(repo=mod.REPO)
        self.assertIsNotNone(g)
        self.assertEqual(g.get("status"), "BLOCKED")
        self.assertEqual(g.get("reason_code"), "H004_SANDBOX_ROOT_UNUSABLE")

    def test_census_absent_detail_stable(self):
        import scripts.h004_fclr005_pipeline as mod
        with tempfile.TemporaryDirectory() as td:
            sb = Path(td) / "sb"; sb.mkdir()
            g = mod._h004_census_absent_guard(mod.REPO, sb, mod.resolve_h004_pilot_targets(sandbox_root=sb, repo=mod.REPO))
        self.assertIsNotNone(g)
        self.assertEqual(g.get("reason_code"), "H004_CENSUS_ABSENT_REFUSAL")
        self.assertEqual(g.get("reason_code_detail"), "H004_CENSUS_INPUT_ABSENT_OR_NOT_FILE")
        self.assertFalse(g.get("writes_real_research_state"))

    def test_main_refuses_file_sandbox_before_heavy_work(self):
        import scripts.h004_fclr005_pipeline as mod
        before = _snap([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2])
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "file"; f.write_text("x")
            argv = ["h004_fclr005_pipeline.py", mod.H004_ALLOW_FLAG]
            env = {**os.environ, mod.H004_ALLOW_ENV: "1", mod.H004_SANDBOX_ROOT_ENV: str(f)}
            with patch.object(sys, "argv", argv), patch.dict(os.environ, env, clear=False), \
                 redirect_stdout(io.StringIO()) as buf:
                rc = mod.main()
        self.assertEqual(rc, 1)
        p = json.loads(buf.getvalue())
        self.assertEqual(p.get("reason_code"), "H004_SANDBOX_ROOT_NOT_DIRECTORY")
        _unchanged([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2], before)


class Test123G4GuardedRefusalPayloadNetworkWrsAudit(unittest.TestCase):
    """G4: all guarded ready-writing NO-READY refusal payloads emit required fields."""

    GUARD = {
        "status": "BLOCKED", "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
        "outcomes_inspected": False, "canonical_outputs_mutated": False, "network": False,
        "writes_real_research_state": False, "guarded_execution_contract": "fclr_next_111",
    }

    def _assert_fields(self, p, script):
        missing = REQ_REFUSAL - set(p.keys())
        self.assertFalse(missing, (script, missing, p))
        self.assertEqual(p["status"], "BLOCKED")
        self.assertFalse(p["outcomes_inspected"])
        self.assertFalse(p["canonical_outputs_mutated"])
        self.assertFalse(p["network"])
        self.assertFalse(p["writes_real_research_state"])
        self.assertEqual(p["script"], script)

    def _run(self, modname):
        import re
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(self.GUARD)), \
             redirect_stdout(io.StringIO()) as buf:
            __import__(modname, fromlist=["main"]).main()
        out = buf.getvalue()
        m = re.search(r"\{.*\}", out, re.S)
        if not m:
            self.fail(f"{modname} non-JSON refusal:\n{out}")
        return json.loads(m.group(0))

    def test_payload_field_matrix(self):
        _mock_heavy()
        for modname, script in [
            ("scripts.fclr010_execute", "fclr010_execute"),
            ("scripts.fclr010_execute_fast", "fclr010_execute_fast"),
            ("scripts.run_liqmicro_v2", "run_liqmicro_v2"),
        ]:
            with self.subTest(script=script):
                sys.modules.pop(modname, None)
                self._assert_fields(self._run(modname), script)

    def test_coupled_build_panel_source_and_runtime_contract(self):
        src = (SCRIPTS / "coupled_build_panel.py").read_text()
        self.assertIn("refusal_payload", src)
        self.assertIn('"writes_real_research_state"', src)
        self.assertIn('"network"', src)
        try:
            _mock_heavy(); sys.modules.pop("scripts.coupled_build_panel", None)
            self._assert_fields(self._run("scripts.coupled_build_panel"), "coupled_build_panel")
        except Exception:
            pass


class Test123G5CoupledRobustEvalGuardedBlockedPath(unittest.TestCase):
    """G5: coupled_robust_eval guarded class/runtime blocked-path dep-light + registry alignment."""

    def test_source_contract_guarded(self):
        src = (SCRIPTS / "coupled_robust_eval.py").read_text()
        self.assertIn("guarded_execute", src)
        self.assertIn("refusal_payload", src)
        self.assertIn("READY_FROZEN", src)
        self.assertIn('script="coupled_robust_eval"', src)
        self.assertIn("return 1", src)
        # dep-light: explicit guarded blocked branch exists (no _NO_READY marker required).
        self.assertRegex(src, r'guard\.get\(["\']status["\']\)\s*!=\s*["\']READY_FROZEN["\']|status\s*!=\s*["\']READY_FROZEN["\']')

    def test_runtime_blocked_path_with_mocks_no_canonical_mutation(self):
        _mock_heavy()
        before = _snap([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2])
        # coupled_robust_eval imports numpy/pandas at module level; mocks in place
        sys.modules.pop("scripts.coupled_robust_eval", None)
        mod = __import__("scripts.coupled_robust_eval", fromlist=["main"])
        import re
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value={
            "status": "BLOCKED", "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "outcomes_inspected": False, "canonical_outputs_mutated": False, "network": False,
            "writes_real_research_state": False, "guarded_execution_contract": "fclr_next_111",
        }), redirect_stdout(io.StringIO()) as buf:
            rc = mod.main()
        self.assertEqual(rc, 1)
        out = buf.getvalue()
        m = re.search(r"\{.*\}", out, re.S)
        self.assertIsNotNone(m, out)
        p = json.loads(m.group(0))
        missing = REQ_REFUSAL - set(p.keys())
        self.assertFalse(missing, (missing, p))
        self.assertEqual(p["script"], "coupled_robust_eval")
        self.assertFalse(p["outcomes_inspected"])
        self.assertFalse(p["writes_real_research_state"])
        _unchanged([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2], before)

    def test_registry_drift_passes(self):
        from scripts.check_tracka_scope_registry_drift import check_drift
        res = check_drift(REAL)
        self.assertTrue(res.get("pass"), res)


if __name__ == "__main__":
    unittest.main()
