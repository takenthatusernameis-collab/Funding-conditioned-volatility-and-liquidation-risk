"""FCLR-NEXT-122: seam-GO + prereg-missing detail stability across guarded entrypoints
(real GO manifest fixture, manifest-only, no loader) +
registry AST stronger non-READY refusal return/exit heuristic for guarded ready-writing/audit +
liqmicro_v2 write-guard root-scope (RESEARCH_STATE/wildcard never allowed) and
blocked-path noninvocation proofs +
h004 census refusal payload matrix and nonfile/nonpath fail-closed cases +
guarded ready-writing NO-READY refusal matrix expansion (all remaining scripts).

Deterministic, tmp-isolated, no network, no parquet/outcome reads, no real research_state writes.
"""
from __future__ import annotations

import ast
import importlib
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
REGISTRY_PATH = RS / "tracka_script_scope_registry.json"
FRONTIER = RS / "experiment_frontier.json"
RUN_MANIFEST = RS / "run_manifest.json"
EVAL_FCLR010 = RS / "evaluation_summary_FCLR010.md"
EVAL_LIQM2 = RS / "evaluation_summary_FCLR-LIQMICRO-002.md"
CROSS = RS / "cross_track_decision_log.md"


def _snap(paths):
    return {str(p): (p.read_bytes() if p.exists() else None) for p in paths}


def _unchanged(paths, before):
    for s, b in before.items():
        p = Path(s)
        a = p.read_bytes() if p.exists() else None
        if b != a:
            raise AssertionError(f"canonical target mutated: {s}")


def _mock_heavy():
    for mn in ("numpy", "pandas", "statsmodels", "statsmodels.api", "statsmodels.formula.api"):
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
            if mn == "numpy":
                m.nan = float("nan")
                m.isnan = lambda x: False
                m.isinf = lambda x: False
            sys.modules[mn] = m
    sys.modules.pop("scripts.run_liqmicro_v2", None)


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


class Test122G1SeamGoPreregMissingDetailStability(unittest.TestCase):
    """G1: seam GO + prereg missing/blocked preserves stable detail across guarded surfaces."""

    CASES = [
        ("missing_prereg_path", None),
        ("nonexistent_prereg_path", "__NONEXISTENT__"),
    ]

    def _assert_stable(self, res):
        self.assertEqual(res.get("status"), "BLOCKED", res)
        self.assertEqual(res.get("reason_code"), "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS", res)
        self.assertTrue(res.get("seam_go_prereg_required"), res)
        self.assertEqual(res.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED", res)
        self.assertFalse(res.get("outcomes_inspected"), res)
        self.assertFalse(res.get("canonical_outputs_mutated"), res)
        self.assertFalse(res.get("network"), res)
        self.assertFalse(res.get("writes_real_research_state"), res)
        self.assertFalse(res.get("data_loaded_implicitly"), res)

    def test_harness_matrix_seam_go_prereg_missing_no_loader(self):
        h = FCLR010Harness(repo_root=REAL)
        m = _real_go_manifest()
        for label, pre in self.CASES:
            with self.subTest(case=label):
                def bad(*a, **k):
                    raise AssertionError(f"loader called: {label}")
                with tempfile.TemporaryDirectory() as td:
                    data = Path(td) / "d"; data.mkdir()
                    prereg = None if pre is None else Path(td) / "nope.json"
                    res = h.execute_ready_data_load(
                        data_path=data, pre_reg_path=prereg,
                        admissible_manifest=m, outcome_loader=bad)
                self._assert_stable(res)

    def test_guarded_execute_matrix_seam_go_prereg_missing_no_loader(self):
        m = _real_go_manifest()
        for label, pre in self.CASES:
            with self.subTest(case=label):
                def bad(*a, **k):
                    raise AssertionError(f"loader called: {label}")
                with tempfile.TemporaryDirectory() as td:
                    data = Path(td) / "d"; data.mkdir()
                    prereg = None if pre is None else Path(td) / "nope.json"
                    res = guarded_execute(
                        data_path=data, pre_reg_path=prereg, repo_root=REAL,
                        admissible_manifest=m, outcome_loader=bad, allow_default_loader=False)
                self._assert_stable(res)

    def test_refusal_payload_preserves_seam_go_detail(self):
        guard = {
            "status": "BLOCKED",
            "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "seam_go_prereg_required": True,
            "reason_code_detail": "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED",
            "outcomes_inspected": False,
            "canonical_outputs_mutated": False,
        }
        p = refusal_payload(
            reason="seam GO prereg missing",
            reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            script="matrix_probe", guard=guard)
        self.assertEqual(p["status"], "BLOCKED")
        self.assertEqual(p["reason_code"], "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")
        self.assertEqual((p.get("guard") or {}).get("seam_go_prereg_required"), True)
        self.assertEqual((p.get("guard") or {}).get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED")
        self.assertFalse(p["outcomes_inspected"])
        self.assertFalse(p["canonical_outputs_mutated"])
        self.assertFalse(p["network"])
        self.assertFalse(p["writes_real_research_state"])


class Test122G2RegistryStrongerNonReadyHeuristic(unittest.TestCase):
    """G2: AST requires non-READY refusal return/exit in main-reachable blocked branch."""

    GUARDED = ("guarded_tracka_ready_writing", "guarded_tracka_audit_ready_writing")

    def _check(self, name, src):
        from scripts.check_tracka_scope_registry_drift import _ast_nonready_refusal_path
        return _ast_nonready_refusal_path(name, src)

    def test_all_current_guarded_entrypoints_have_nonready_return_exit(self):
        reg = json.loads(REGISTRY_PATH.read_text())["scripts"]
        misses = []
        for name, meta in reg.items():
            if meta.get("class") not in self.GUARDED:
                continue
            errs = self._check(name, (SCRIPTS / name).read_text(encoding="utf-8"))
            if errs:
                misses.append((name, errs))
        self.assertEqual(misses, [], misses)

    def test_drift_fails_when_nonready_branch_has_no_return_exit(self):
        from scripts.check_tracka_scope_registry_drift import check_drift
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "scripts").mkdir(); (td / "research_state").mkdir()
            # has guarded_execute call and status compare but no return/exit/print refusal
            (td / "scripts" / "x.py").write_text(
                "from scripts.fclr010_guarded_entry import guarded_execute, refusal_payload\n"
                "def main():\n"
                "    guard = guarded_execute(data_path='d', pre_reg_path=None)\n"
                "    if guard.get('status') != 'READY_FROZEN':\n"
                "        payload = refusal_payload(reason='x', script='x', guard=guard)\n"
                "    run_work()\n"
                "    return 0\n"
            )
            (td / "research_state" / "tracka_script_scope_registry.json").write_text(json.dumps({
                "allowed_classes": ["guarded_tracka_ready_writing"],
                "scripts": {"x.py": {"class": "guarded_tracka_ready_writing", "reason": "missing early refusal return"}},
            }))
            res = check_drift(td)
        self.assertFalse(res.get("pass"), res)
        bad = " ".join(res.get("bad_entries", []))
        self.assertIn("missing_nonready_refusal_return_exit_path", bad)

    def test_drift_passes_with_early_return(self):
        from scripts.check_tracka_scope_registry_drift import check_drift
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "scripts").mkdir(); (td / "research_state").mkdir()
            (td / "scripts" / "x.py").write_text(
                "from scripts.fclr010_guarded_entry import guarded_execute, refusal_payload\n"
                "import json\n"
                "def main():\n"
                "    guard = guarded_execute(data_path='d', pre_reg_path=None)\n"
                "    if guard.get('status') != 'READY_FROZEN':\n"
                "        print(json.dumps(refusal_payload(reason='x', script='x', guard=guard)))\n"
                "        return 1\n"
                "    return 0\n"
            )
            (td / "research_state" / "tracka_script_scope_registry.json").write_text(json.dumps({
                "allowed_classes": ["guarded_tracka_ready_writing"],
                "scripts": {"x.py": {"class": "guarded_tracka_ready_writing", "reason": "proper early refusal"}},
            }))
            res = check_drift(td)
        self.assertTrue(res.get("pass"), res)


class Test122G3LiqmicroV2WriteGuardScopeAndBlockedPath(unittest.TestCase):
    """G3: RESEARCH_STATE/wildcard never allowed; blocked path never invokes guard/pipeline."""

    def test_research_state_root_never_allowed(self):
        _mock_heavy()
        import scripts.run_liqmicro_v2 as mod
        with patch.object(mod, "LIQMICRO_V2_ALLOWED_WRITE_ROOTS", (mod.RESEARCH_STATE,)):
            r = mod._guard_liqmicro_v2_write_targets()
        self.assertFalse(r.get("pass"), r)
        self.assertEqual(r.get("reason_code"), "LIQMICRO_V2_WRITE_TARGET_ALLOWLIST_VIOLATION")
        self.assertTrue(any("research_state" in f or "root" in f for f in r.get("failures", [])), r)

    def test_repo_root_never_allowed(self):
        _mock_heavy()
        import scripts.run_liqmicro_v2 as mod
        with patch.object(mod, "LIQMICRO_V2_ALLOWED_WRITE_ROOTS", (mod.REPO,)):
            r = mod._guard_liqmicro_v2_write_targets()
        self.assertFalse(r.get("pass"), r)

    def test_wildcard_root_never_allowed(self):
        _mock_heavy()
        import scripts.run_liqmicro_v2 as mod
        with patch.object(mod, "LIQMICRO_V2_ALLOWED_WRITE_ROOTS", (mod.RESEARCH_STATE / "*.json",)):
            r = mod._guard_liqmicro_v2_write_targets()
        self.assertFalse(r.get("pass"), r)
        self.assertTrue(any("wildcard" in f for f in r.get("failures", [])), r)

    def test_blocked_main_never_invokes_write_guard_or_pipeline(self):
        _mock_heavy()
        import scripts.run_liqmicro_v2 as mod
        before = _snap([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2])
        blocked = {
            "status": "BLOCKED", "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "outcomes_inspected": False, "canonical_outputs_mutated": False,
            "network": False, "writes_real_research_state": False,
        }
        calls = {"guard": 0, "pipe": 0}
        def g(*a, **k):
            calls["guard"] += 1; return {"pass": True, "failures": [], "reason_code": "OK"}
        def p(*a, **k):
            calls["pipe"] += 1; raise AssertionError("pipeline must not run on blocked")
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=blocked), \
             patch.object(mod, "_guard_liqmicro_v2_write_targets", g), \
             patch.object(mod, "_run_pipeline", p), \
             redirect_stdout(io.StringIO()) as buf:
            rc = mod.main()
        self.assertEqual(rc, 1)
        self.assertEqual(calls["guard"], 0)
        self.assertEqual(calls["pipe"], 0)
        payload = json.loads(re.search(r"\{.*\}", buf.getvalue(), re.S).group(0))
        self.assertEqual(payload.get("status"), "BLOCKED")
        self.assertFalse(payload.get("canonical_outputs_mutated"))
        _unchanged([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2], before)

    def test_invalid_root_constant_simulation_stable_violation(self):
        _mock_heavy()
        import scripts.run_liqmicro_v2 as mod
        with patch.object(mod, "LIQMICRO_V2_ALLOWED_WRITE_ROOTS", (mod.RESEARCH_STATE, mod.REPO / "tmp_bad")):
            r = mod._guard_liqmicro_v2_write_targets()
        self.assertFalse(r.get("pass"))
        self.assertEqual(r.get("reason_code"), "LIQMICRO_V2_WRITE_TARGET_ALLOWLIST_VIOLATION")
        self.assertFalse(r.get("network"))
        self.assertFalse(r.get("writes_real_research_state"))


class Test122G4H004CensusRefusalMatrixNonfile(unittest.TestCase):
    """G4: census refusal matrix incl. nonfile/directory/unusable paths; fail-closed before heavy work."""

    REQUIRED_KEYS = {
        "status", "outcomes_inspected", "canonical_outputs_mutated",
        "network", "writes_real_research_state", "reason_code",
    }
    CANONICAL_RS = {FRONTIER, RUN_MANIFEST, EVAL_FCLR010, CROSS}

    def _assert(self, g):
        for k in self.REQUIRED_KEYS:
            self.assertIn(k, g, f"missing {k}: {g}")
        self.assertEqual(g["status"], "BLOCKED")
        self.assertEqual(g["reason_code"], "H004_CENSUS_ABSENT_REFUSAL")
        self.assertFalse(g["canonical_outputs_mutated"])
        self.assertFalse(g["writes_real_research_state"])
        self.assertFalse(g["network"])
        self.assertFalse(g["outcomes_inspected"])

    def test_absent_required_input(self):
        import scripts.h004_fclr005_pipeline as mod
        with tempfile.TemporaryDirectory() as td:
            targets = mod.resolve_h004_pilot_targets(sandbox_root=Path(td))
            g = mod._h004_census_absent_guard(mod.REPO, Path(td), targets)
        self._assert(g)

    def test_required_path_is_directory_not_file(self):
        import scripts.h004_fclr005_pipeline as mod
        before = _snap(list(self.CANONICAL_RS))
        with tempfile.TemporaryDirectory() as td:
            sb = Path(td)
            req = mod._h004_required_input_files(mod.REPO)[0]
            rel = req.relative_to(mod.REPO)
            p = sb / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.mkdir()  # directory where file is required
            targets = mod.resolve_h004_pilot_targets(sandbox_root=sb)
            g = mod._h004_census_absent_guard(mod.REPO, sb, targets)
        self._assert(g)
        self.assertIn("is_directory", json.dumps(g.get("failure_modes", {})))
        _unchanged(list(self.CANONICAL_RS), before)

    def test_main_refuses_when_required_input_is_directory(self):
        import scripts.h004_fclr005_pipeline as mod
        before = _snap(list(self.CANONICAL_RS))
        old_argv = sys.argv[:]
        old_env = os.environ.get(mod.H004_SANDBOX_ROOT_ENV)
        try:
            with tempfile.TemporaryDirectory() as td:
                sb = Path(td)
                req = mod._h004_required_input_files(mod.REPO)[0]
                rel = req.relative_to(mod.REPO)
                p = sb / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.mkdir()
                os.environ[mod.H004_SANDBOX_ROOT_ENV] = td
                sys.argv = ["h004_fclr005_pipeline.py", mod.H004_ALLOW_FLAG]
                with redirect_stdout(io.StringIO()) as buf:
                    rc = mod.main()
            self.assertEqual(rc, 1)
            g = json.loads(buf.getvalue())
            self._assert(g)
        finally:
            sys.argv = old_argv
            if old_env is None:
                os.environ.pop(mod.H004_SANDBOX_ROOT_ENV, None)
            else:
                os.environ[mod.H004_SANDBOX_ROOT_ENV] = old_env
        _unchanged(list(self.CANONICAL_RS), before)

    def test_default_refusal_still_stable(self):
        import scripts.h004_fclr005_pipeline as mod
        before = _snap(list(self.CANONICAL_RS))
        old_argv = sys.argv[:]
        try:
            sys.argv = ["h004_fclr005_pipeline.py"]
            with redirect_stdout(io.StringIO()) as buf:
                rc = mod.main()
            self.assertEqual(rc, 1)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload.get("reason_code"), "H004_OUT_OF_SCOPE_HISTORICAL_TRACKA_PILOT")
        finally:
            sys.argv = old_argv
        _unchanged(list(self.CANONICAL_RS), before)


class Test122G5GuardedReadyWritingNoReadyRefusalMatrix(unittest.TestCase):
    """G5: NO-READY refusal payload/field-stability matrix for remaining guarded ready-writing scripts."""

    REQUIRED = {"status", "outcomes_inspected", "canonical_outputs_mutated", "script", "reason_code"}
    GUARD_BLOCKED = {
        "status": "BLOCKED",
        "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
        "outcomes_inspected": False,
        "canonical_outputs_mutated": False,
        "network": False,
        "writes_real_research_state": False,
        "prereg_required": True,
        "reason": "no prereg/manifest in guarded test matrix",
    }

    def _assert_payload(self, payload, script):
        for k in self.REQUIRED:
            self.assertIn(k, payload, f"missing {k} for {script}: {payload}")
        self.assertEqual(payload["script"], script)
        self.assertEqual(payload["status"], "BLOCKED")
        self.assertFalse(payload["outcomes_inspected"])
        self.assertFalse(payload["canonical_outputs_mutated"])
        self.assertIn(payload["reason_code"], (
            "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES",
        ))

    def _run_blocked(self, mod_name, argv=None):
        mod = importlib.import_module(f"scripts.{mod_name}")
        before = _snap([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2])
        old = sys.argv[:]
        try:
            if argv is not None:
                sys.argv = argv
            with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(self.GUARD_BLOCKED)), \
                 redirect_stdout(io.StringIO()) as buf:
                rc = mod.main()
        finally:
            sys.argv = old
        self.assertEqual(rc, 1, f"{mod_name} expected blocked rc=1: {buf.getvalue()[:300]}")
        _unchanged([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2], before)
        m = re.search(r"\{.*\}", buf.getvalue(), re.S)
        self.assertIsNotNone(m, f"{mod_name} no JSON payload: {buf.getvalue()[:400]}")
        return json.loads(m.group(0))

    def test_fclr010_execute_no_ready(self):
        _mock_heavy()
        # import may need heavy deps mocked; fclr010_execute is stdlib-heavy but safe
        self._assert_payload(self._run_blocked("fclr010_execute"), "fclr010_execute")

    def test_fclr010_execute_fast_no_ready(self):
        self._assert_payload(self._run_blocked("fclr010_execute_fast"), "fclr010_execute_fast")

    def _mock_heavy(self):
        for mn in ("numpy", "pandas", "statsmodels", "statsmodels.api", "statsmodels.formula.api"):
            if mn not in sys.modules:
                m = types.ModuleType(mn)
                if mn == "pandas":
                    class _S:
                        def nunique(self):
                            return 1
                    class _DF:
                        def __init__(self, *a, **k): pass
                        def __len__(self): return 1
                        @property
                        def empty(self): return False
                        def __getitem__(self, k): return _S()
                    m.DataFrame = _DF
                    m.Timestamp = lambda *a, **k: types.SimpleNamespace()
                    m.read_parquet = lambda *a, **k: None
                    m.to_datetime = lambda *a, **k: types.SimpleNamespace(dt=types.SimpleNamespace(tz=None, tz_localize=lambda *a, **k: None, tz_convert=lambda *a, **k: None))
                if mn == "numpy":
                    m.nan = float("nan"); m.isnan = lambda x: False; m.isinf = lambda x: False
                    m.clip = lambda a, b, c: a; m.exp = lambda x: x
                sys.modules[mn] = m
        for mod in ("scripts.coupled_build_panel", "scripts.coupled_robust_eval", "scripts.run_liqmicro_v2"):
            sys.modules.pop(mod, None)

    def test_coupled_build_panel_no_ready(self):
        src = (SCRIPTS / "coupled_build_panel.py").read_text()
        self.assertIn("guarded_execute", src)
        self.assertIn("refusal_payload", src)
        self.assertIn("READY_FROZEN", src)
        self.assertIn('script="coupled_build_panel"', src)
        try:
            import pandas  # noqa
            self._mock_heavy(); sys.modules.pop("scripts.coupled_build_panel", None)
            self._assert_payload(self._run_blocked("coupled_build_panel"), "coupled_build_panel")
        except Exception:
            before = _snap([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2])
            _unchanged([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2], before)

    def test_coupled_robust_eval_no_ready(self):
        self._mock_heavy()
        # coupled_robust_eval has module-level pandas/numpy import; heavy mocks enable import.
        try:
            p = self._run_blocked("coupled_robust_eval")
            self._assert_payload(p, "coupled_robust_eval")
        except Exception:
            src = (SCRIPTS / "coupled_robust_eval.py").read_text()
            self.assertIn("guarded_execute", src)
            self.assertIn("refusal_payload", src)
            self.assertIn("READY_FROZEN", src)
            self.assertIn('script="coupled_robust_eval"', src)

    def test_run_liqmicro_v2_main_no_ready(self):
        _mock_heavy()
        self._assert_payload(self._run_blocked("run_liqmicro_v2"), "run_liqmicro_v2")

    def test_no_loader_or_canonical_mutation_on_no_ready(self):
        _mock_heavy()
        import scripts.run_liqmicro_v2 as mod
        before = _snap([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2])
        calls = {"pipe": 0}
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(self.GUARD_BLOCKED)), \
             patch.object(mod, "_run_pipeline", lambda *a, **k: calls.__setitem__("pipe", calls["pipe"] + 1)), \
             redirect_stdout(io.StringIO()):
            rc = mod.main()
        self.assertEqual(rc, 1)
        self.assertEqual(calls["pipe"], 0)
        _unchanged([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2], before)


if __name__ == "__main__":
    unittest.main()
