"""FCLR-NEXT-124: coupled_build_panel READY-path/cache write-scope guard +
evaluate_forward manifest-only seam-GO data-missing stable parity +
h004 census/input path traversal/symlink-escape fail-closed matrix +
coupled_build_panel runtime blocked NO-READY refusal full-field emission +
liqmicro_v2 write-guard divergence regression matrix (constant+arg+bypass).

Deterministic, tmp-isolated, no network, no parquet/outcome reads, no real research_state writes.
"""
from __future__ import annotations

import io
import json
import os
import re
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
    # Force-refresh the heavy modules so a prior real import (e.g. from an
    # earlier test file in the same process) cannot leak a pandas without
    # Timestamp into coupled_build_panel's module-level import.
    for mn in ("numpy", "pandas", "pyarrow", "pyarrow.parquet"):
        sys.modules.pop(mn, None)
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
            if mn == "pandas":
                m.Timestamp = lambda x: x
                m.concat = lambda frames, *a, **k: frames[0] if frames else _DF()
                m.date_range = lambda *a, **k: []
                class _MI:
                    @staticmethod
                    def from_product(*a, **k):
                        return []
                m.MultiIndex = _MI
            sys.modules[mn] = m
    for mn in ("scripts.run_liqmicro_v2", "scripts.coupled_build_panel", "scripts.coupled_robust_eval",
               "analysis.liqmicro.ingest", "analysis.liqmicro.features"):
        sys.modules.pop(mn, None)


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


class Test124G1CoupledBuildPanelCacheWriteScope(unittest.TestCase):
    """G1: cache write-scope allowlist (exact CACHE artifact only) + blocked-path nonwrite proof."""

    def setUp(self):
        self.cbp = None
        _mock_heavy()
        sys.modules.pop("scripts.coupled_build_panel", None)
        import scripts.coupled_build_panel as mod
        self.cbp = mod
        self.CACHE = mod.CACHE

    def _assert_refusal_fields(self, p, script):
        missing = REQ_REFUSAL - set(p.keys())
        self.assertFalse(missing, (script, missing, p))
        self.assertEqual(p["status"], "BLOCKED")
        self.assertFalse(p["outcomes_inspected"])
        self.assertFalse(p["canonical_outputs_mutated"])
        self.assertFalse(p["network"])
        self.assertFalse(p["writes_real_research_state"])
        self.assertEqual(p["script"], script)

    def test_guard_allows_exact_cache_artifact_only(self):
        mod = self.cbp
        ok = mod._guard_coupled_cache_write_target(mod.CACHE)
        self.assertTrue(ok.get("pass"), ok)
        self.assertEqual(ok.get("reason_code"), "OK")
        self.assertEqual(ok.get("target"), str(mod.CACHE.resolve()))

    def test_guard_denies_research_state_non_cache_artifact(self):
        mod = self.cbp
        bad = RS / "evaluation_summary_FCLR010.md"
        r = mod._guard_coupled_cache_write_target(bad)
        self.assertFalse(r.get("pass"), r)
        self.assertEqual(r.get("reason_code"), "COUPLED_CACHE_WRITE_SCOPE_VIOLATION")
        self.assertTrue(any("non_cache" in f or "not_allowed_cache_artifact" in f for f in r.get("failures", [])), r)

    def test_guard_denies_repo_root_and_research_state_dir(self):
        mod = self.cbp
        for bad in (REAL, RS):
            r = mod._guard_coupled_cache_write_target(bad)
            self.assertFalse(r.get("pass"), (bad, r))
            self.assertTrue(any("dir_wide_or_repo_root" in f for f in r.get("failures", [])), (bad, r))

    def test_guard_denies_wildcard_and_denied_canonical_markers(self):
        mod = self.cbp
        r1 = mod._guard_coupled_cache_write_target(mod.REPO / "research_state" / ".cache" / "*.parquet")
        self.assertFalse(r1.get("pass"), r1)
        self.assertTrue(any("wildcard" in f for f in r1.get("failures", [])), r1)
        for marker in mod._COUPLED_DENIED_CANONICAL_MARKERS:
            r2 = mod._guard_coupled_cache_write_target(RS / marker)
            self.assertFalse(r2.get("pass"), (marker, r2))
            self.assertTrue(any(f"denied_canonical_target:{marker}" in f for f in r2.get("failures", [])), (marker, r2))

    def test_guard_denies_target_escaping_repo(self):
        mod = self.cbp
        r = mod._guard_coupled_cache_write_target(Path("/tmp/escape/fclr_coupled_panel.parquet"))
        self.assertFalse(r.get("pass"), r)
        self.assertTrue(any("escapes_repo" in f for f in r.get("failures", [])), r)

    def test_build_refuses_without_outcome_loader(self):
        mod = self.cbp
        with self.assertRaises(mod.GuardedReadRefused):
            mod.build(force=False, outcome_loader=None)

    def test_blocked_main_no_cache_write_loader_not_called(self):
        mod = self.cbp
        before = _snap([self.CACHE])
        calls = {"loader": 0}
        def fake_loader(*a, **k):
            calls["loader"] += 1
            return {"panel_cached": True, "cache": str(mod.CACHE)}
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value={
            "status": "BLOCKED", "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "outcomes_inspected": False, "canonical_outputs_mutated": False,
        }), redirect_stdout(io.StringIO()):
            rc = mod.main()
        self.assertEqual(rc, 1)
        self.assertEqual(calls["loader"], 0)
        _unchanged([self.CACHE], before)

    def test_guard_invoked_before_cache_write_on_load_path(self):
        mod = self.cbp
        src = (SCRIPTS / "coupled_build_panel.py").read_text()
        # the write-scope guard is invoked on CACHE before any READY-path parquet write
        guard_call = '_guard_coupled_cache_write_target(CACHE)'
        write = "panel.to_parquet(CACHE, index=False)"
        mkdir = "CACHE.parent.mkdir(parents=True, exist_ok=True)"
        self.assertIn(guard_call, src)
        self.assertIn(write, src)
        self.assertIn(mkdir, src)
        src_idx_guard = src.index(guard_call)
        src_idx_mkdir = src.index(mkdir)
        src_idx_write = src.index(write)
        self.assertLess(src_idx_guard, src_idx_mkdir, "guard must run before cache dir write")
        self.assertLess(src_idx_mkdir, src_idx_write, "mkdir must run before to_parquet")
        # build() still refuses without an explicit outcome_loader (guarded contract)
        with self.assertRaises(mod.GuardedReadRefused):
            mod.build(force=False, outcome_loader=None)


class Test124G2EvaluateForwardDataMissingParity(unittest.TestCase):
    """G2: seam GO + prereg present + data_path missing => stable BLOCKED parity, no loader/outcome read."""

    def _assert_blocked_parity(self, res):
        self.assertEqual(res.get("status"), "BLOCKED", res)
        self.assertEqual(res.get("reason_code"), "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS", res)
        self.assertTrue(res.get("seam_go_data_missing"), res)
        self.assertEqual(res.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING", res)
        self.assertFalse(res.get("outcomes_inspected"), res)
        self.assertFalse(res.get("data_loaded_implicitly"), res)
        self.assertFalse(res.get("reads_parquet"), res)
        self.assertFalse(res.get("reads_outcomes"), res)
        self.assertFalse(res.get("network"), res)
        self.assertFalse(res.get("prereg_required"), res)
        self.assertIsNone(res.get("outcomes_loaded"), res)

    def test_direct_evaluate_forward_data_missing_blocked(self):
        h = FCLR010Harness(repo_root=REAL)
        m = _real_go_manifest()
        with tempfile.TemporaryDirectory() as td:
            pre_reg = Path(td) / "prereg.json"; pre_reg.write_text("{}")
            missing = Path(td) / "does_not_exist"
            called = {"n": 0}
            def bad(*a, **k):
                called["n"] += 1
                raise AssertionError("loader must not be called when data missing")
            res = h.evaluate_forward(missing, Path(td) / "out", pre_reg_path=pre_reg,
                                     admissible_manifest=m, outcome_loader=bad)
        self._assert_blocked_parity(res)
        self.assertEqual(called["n"], 0)

    def test_execute_ready_data_load_data_missing_parity(self):
        h = FCLR010Harness(repo_root=REAL)
        m = _real_go_manifest()
        with tempfile.TemporaryDirectory() as td:
            pre_reg = Path(td) / "prereg.json"; pre_reg.write_text("{}")
            missing = Path(td) / "does_not_exist"
            res = h.execute_ready_data_load(missing, pre_reg_path=pre_reg, admissible_manifest=m)
        self._assert_blocked_parity(res)
        self.assertIsNone(res.get("outcomes_loaded"), res)

    def test_data_present_reads_frozen_then_loader_called_once(self):
        h = FCLR010Harness(repo_root=REAL)
        m = _real_go_manifest()
        with tempfile.TemporaryDirectory() as td:
            pre_reg = Path(td) / "prereg.json"; pre_reg.write_text("{}")
            data = Path(td) / "d"; data.mkdir()
            calls = {"n": 0}
            def loader(dp):
                calls["n"] += 1
                return {"rows": 3}
            res = h.execute_ready_data_load(data, pre_reg_path=pre_reg, admissible_manifest=m,
                                            outcome_loader=loader)
        self.assertEqual(res.get("status"), "READY_FROZEN", res)
        self.assertEqual(calls["n"], 1)
        self.assertEqual(res.get("outcomes_loaded"), {"rows": 3})
        self.assertFalse(res.get("outcomes_inspected"))


class Test124G3H004PathTraversalSymlinkEscape(unittest.TestCase):
    """G3: allowed-sandbox census/input path traversal (..) and symlink-escape fail-closed before heavy work."""

    def test_traversal_dotdot_fail_closed(self):
        import scripts.h004_fclr005_pipeline as mod
        with tempfile.TemporaryDirectory() as td:
            sb = Path(td) / "sb"; sb.mkdir()
            bad = sb / "research_state" / ".." / "escape.csv"
            g = mod._h004_path_traversal_or_symlink_escape_guard([bad], sandbox_root=sb)
        self.assertIsNotNone(g)
        self.assertEqual(g.get("status"), "BLOCKED", g)
        self.assertEqual(g.get("reason_code"), "H004_CENSUS_INPUT_PATH_TRAVERSAL_OR_SYMLINK_ESCAPE", g)
        self.assertIn("Path traversal", g.get("reason", ""), g)
        self.assertFalse(g.get("writes_real_research_state"))
        self.assertFalse(g.get("network"))

    def test_symlink_escape_fail_closed(self):
        import scripts.h004_fclr005_pipeline as mod
        with tempfile.TemporaryDirectory() as td:
            sb = sb2 = Path(td) / "sb"; sb.mkdir()
            (sb / "research_state" / "data_cache").mkdir(parents=True)
            outside = Path(td) / "outside_escape.csv"; outside.write_text("x")
            link = sb / "research_state" / "data_cache" / "liquidations_full_20260807.csv"
            os.symlink(outside, link)
            g = mod._h004_path_traversal_or_symlink_escape_guard([link], sandbox_root=sb)
        self.assertIsNotNone(g)
        self.assertEqual(g.get("status"), "BLOCKED", g)
        self.assertEqual(g.get("reason_code"), "H004_CENSUS_INPUT_PATH_TRAVERSAL_OR_SYMLINK_ESCAPE", g)
        self.assertIn("outside sandbox", g.get("reason", ""), g)

    def test_valid_sandbox_input_passes_traversal_guard(self):
        import scripts.h004_fclr005_pipeline as mod
        with tempfile.TemporaryDirectory() as td:
            sb = Path(td) / "sb"; sb.mkdir()
            (sb / "research_state" / "data_cache").mkdir(parents=True)
            (sb / "research_state" / "data_cache" / "liquidations_full_20260807.csv").write_text("x")
            link = sb / "research_state" / "data_cache" / "liquidations_full_20260807.csv"
            g = mod._h004_path_traversal_or_symlink_escape_guard([link], sandbox_root=sb)
        self.assertIsNone(g)

    def test_main_symlink_escape_blocked_before_heavy_work_no_rs_writes(self):
        import scripts.h004_fclr005_pipeline as mod
        before = _snap([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2])
        with tempfile.TemporaryDirectory() as td:
            sb = Path(td) / "sb"; sb.mkdir()
            (sb / "research_state" / "data_cache").mkdir(parents=True)
            outside = Path(td) / "outside_escape.csv"; outside.write_text("x")
            link = sb / "research_state" / "data_cache" / "liquidations_full_20260807.csv"
            os.symlink(outside, link)
            argv = ["h004_fclr005_pipeline.py", mod.H004_ALLOW_FLAG]
            env = {**os.environ, mod.H004_ALLOW_ENV: "1", mod.H004_SANDBOX_ROOT_ENV: str(sb)}
            with patch.object(sys, "argv", argv), patch.dict(os.environ, env, clear=False), \
                 redirect_stdout(io.StringIO()) as buf:
                rc = mod.main()
        self.assertEqual(rc, 1)
        p = json.loads(buf.getvalue())
        self.assertEqual(p.get("reason_code"), "H004_CENSUS_INPUT_PATH_TRAVERSAL_OR_SYMLINK_ESCAPE", p)
        _unchanged([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2], before)


class Test124G4CoupledBuildPanelRefusalPayloadEmission(unittest.TestCase):
    """G4: runtime blocked NO-READY refusal emits full required fields, no parquet/loader/canonical mutation."""

    def test_runtime_blocked_payload_full_fields_no_cache_write(self):
        _mock_heavy()
        sys.modules.pop("scripts.coupled_build_panel", None)
        import scripts.coupled_build_panel as mod
        before = _snap([mod.CACHE, FRONTIER, RUN_MANIFEST, EVAL_FCLR010])
        guard = {
            "status": "BLOCKED", "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "outcomes_inspected": False, "canonical_outputs_mutated": False, "network": False,
            "writes_real_research_state": False, "guarded_execution_contract": "fclr_next_111",
        }
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=guard), \
             redirect_stdout(io.StringIO()) as buf:
            rc = mod.main()
        self.assertEqual(rc, 1)
        out = buf.getvalue()
        m = re.search(r"\{.*\}", out, re.S)
        self.assertIsNotNone(m, out)
        p = json.loads(m.group(0))
        missing = REQ_REFUSAL - set(p.keys())
        self.assertFalse(missing, (missing, p))
        self.assertEqual(p["script"], "coupled_build_panel")
        self.assertEqual(p["status"], "BLOCKED")
        self.assertFalse(p["outcomes_inspected"])
        self.assertFalse(p["canonical_outputs_mutated"])
        self.assertFalse(p["network"])
        self.assertFalse(p["writes_real_research_state"])
        _unchanged([mod.CACHE, FRONTIER, RUN_MANIFEST, EVAL_FCLR010], before)

    def test_guard_payload_returns_full_fields(self):
        _mock_heavy()
        sys.modules.pop("scripts.coupled_build_panel", None)
        import scripts.coupled_build_panel as mod
        r = mod._guard_coupled_cache_write_target(Path("/tmp/notallowed.parquet"))
        guard_fields = {"pass", "failures", "reason_code", "allowed_artifact", "target", "script",
                        "network", "writes_real_research_state"}
        missing = guard_fields - set(r.keys())
        self.assertFalse(missing, (missing, r))
        self.assertEqual(r["script"], "coupled_build_panel")
        self.assertEqual(r["network"], False)
        self.assertEqual(r["writes_real_research_state"], False)
        self.assertFalse(r["pass"])
        self.assertEqual(r["reason_code"], "COUPLED_CACHE_WRITE_SCOPE_VIOLATION")
        self.assertEqual(r["allowed_artifact"], str(mod.CACHE.resolve()))
        # exact allowed artifact passes
        r_ok = mod._guard_coupled_cache_write_target(mod.CACHE)
        self.assertTrue(r_ok.get("pass"), r_ok)
        self.assertEqual(r_ok.get("reason_code"), "OK")


class Test124G5LiqmicroV2WriteGuardDivergenceRegression(unittest.TestCase):
    """G5: write-guard divergence regression matrix (constant+arg+bypass attempts)."""

    def _fresh_mod(self):
        _mock_heavy()
        sys.modules.pop("scripts.run_liqmicro_v2", None)
        import scripts.run_liqmicro_v2 as mod
        return mod

    def test_policy_roots_pass_ok(self):
        mod = self._fresh_mod()
        r = mod._guard_liqmicro_v2_write_targets()
        self.assertTrue(r.get("pass"), r)
        self.assertEqual(r.get("reason_code"), "OK")

    def test_arg_divergence_fail_closed(self):
        mod = self._fresh_mod()
        r = mod._guard_liqmicro_v2_write_targets(allowed_write_roots=(mod.REPO / "src",))
        self.assertFalse(r.get("pass"), r)
        self.assertEqual(r.get("reason_code"), "LIQMICRO_V2_WRITE_TARGET_ALLOWLIST_VIOLATION")
        self.assertTrue(any("diverge" in f for f in r.get("failures", [])), r)

    def test_monkeypatched_constant_divergence_fail_closed(self):
        mod = self._fresh_mod()
        mod.LIQMICRO_V2_ALLOWED_WRITE_ROOTS = (mod.REPO / "scripts",)
        r = mod._guard_liqmicro_v2_write_targets()
        self.assertFalse(r.get("pass"), r)
        self.assertEqual(r.get("reason_code"), "LIQMICRO_V2_WRITE_TARGET_ALLOWLIST_VIOLATION")

    def test_research_state_dir_wide_arg_fail_closed(self):
        mod = self._fresh_mod()
        r = mod._guard_liqmicro_v2_write_targets(allowed_write_roots=(mod.RESEARCH_STATE,))
        self.assertFalse(r.get("pass"), r)

    def test_repo_root_arg_fail_closed(self):
        mod = self._fresh_mod()
        r = mod._guard_liqmicro_v2_write_targets(allowed_write_roots=(mod.REPO,))
        self.assertFalse(r.get("pass"), r)

    def test_wildcard_arg_fail_closed(self):
        mod = self._fresh_mod()
        r = mod._guard_liqmicro_v2_write_targets(allowed_write_roots=(str(mod.RESULTS_DIR) + "/*",))
        self.assertFalse(r.get("pass"), r)

    def test_arbitrary_repo_dir_arg_fail_closed(self):
        mod = self._fresh_mod()
        r = mod._guard_liqmicro_v2_write_targets(allowed_write_roots=(mod.REPO / "results" / "liqmicro",))
        self.assertFalse(r.get("pass"), r)

    def test_denied_target_in_allowed_root_fail_closed(self):
        mod = self._fresh_mod()
        root = mod.RESULTS_DIR / "experiment_frontier.json"
        r = mod._guard_liqmicro_v2_write_targets(allowed_write_roots=(root,))
        self.assertFalse(r.get("pass"), r)
        self.assertTrue(any("denied_write_target" in f for f in r.get("failures", [])), r)

    def test_results_dir_and_specific_summary_pass(self):
        mod = self._fresh_mod()
        r = mod._guard_liqmicro_v2_write_targets(allowed_write_roots=(mod.RESULTS_DIR, mod.RESEARCH_STATE / "evaluation_summary_FCLR-LIQMICRO-002.md"))
        self.assertTrue(r.get("pass"), r)

    def test_blocked_main_never_invokes_guard_or_pipeline_no_canonical_mutation(self):
        mod = self._fresh_mod()
        before = _snap([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2])
        calls = {"guard": 0, "pipe": 0}
        orig_guard = mod._guard_liqmicro_v2_write_targets
        def spy_guard(*a, **k):
            calls["guard"] += 1
            return orig_guard(*a, **k)
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value={
            "status": "BLOCKED", "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "outcomes_inspected": False, "canonical_outputs_mutated": False,
        }), patch.object(mod, "_guard_liqmicro_v2_write_targets", spy_guard), \
             patch.object(mod, "_run_pipeline", lambda *a, **k: calls.__setitem__("pipe", calls["pipe"] + 1)), \
             redirect_stdout(io.StringIO()):
            rc = mod.main()
        self.assertEqual(rc, 1)
        self.assertEqual(calls["guard"], 0)
        self.assertEqual(calls["pipe"], 0)
        _unchanged([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2], before)


if __name__ == "__main__":
    unittest.main()
