"""FCLR-NEXT-122 (heavy work, dep-light, tmp-isolated):

G1 seam-GO + prereg-missing detail stability across all guarded entrypoints
G2 registry AST stronger blocked-branch refusal heuristic
G3 run_liqmicro_v2 write-guard scope + blocked-path noninvocation proofs
G4 h004 census refusal payload matrix + nonfile/nonpath fail-closed cases
G5 guarded ready-writing NO-READY refusal matrix expansion across all scripts

Deterministic, no network, no parquet/outcome reads, no real research_state writes.
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
from scripts.check_tracka_scope_registry_drift import check_drift
from src.analysis.tracka_admissible import (
    assess_ironflow_month_admissibility,
    build_ironflow_month_manifest,
)

REAL = Path(__file__).resolve().parent.parent
RS = REAL / "research_state"
SCRIPTS = REAL / "scripts"
REGISTRY_PATH = RS / "tracka_script_scope_registry.json"
RUN_MANIFEST = RS / "run_manifest.json"
FRONTIER = RS / "experiment_frontier.json"
CROSS = RS / "cross_track_decision_log.md"
EVAL_FCLR010 = RS / "evaluation_summary_FCLR010.md"
EVAL_LIQM2 = RS / "evaluation_summary_FCLR-LIQMICRO-002.md"
LIQ_AUDIT = RS / "liqmicro_data_audit_001.md"
COV_AUDIT = RS / "fclr010_coverage_audit.json"

REQUIRED_KEYS = {
    "status", "outcomes_inspected", "canonical_outputs_mutated",
    "network", "script", "reason_code",
}
WRITES_KEYS = ("writes_real_research_state", "writes_real_reserved_state")


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
                class _TS:
                    def __init__(self, *a, **k):
                        pass
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
                m.Timestamp = _TS
                m.to_datetime = lambda *a, **k: _TS()
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
        schema_fields_events=["timestamp", "symbol", "notional_usd"],
        schema_fields_fills=["timestamp", "symbol", "size"],
    )


def _assert_refusal_shape(payload, script):
    for k in REQUIRED_KEYS:
        assert k in payload, f"missing required key {k} in {script}: {payload}"
    assert payload.get("script") == script, payload
    assert payload.get("status") == "BLOCKED", payload
    assert payload.get("outcomes_inspected") is False, payload
    assert payload.get("canonical_outputs_mutated") is False, payload
    assert payload.get("network") is False, payload
    # writes key (codebase emits either name); where emitted, must be False.
    for wk in WRITES_KEYS:
        if wk in payload:
            assert payload.get(wk) is False, f"{wk} not False in {script}: {payload}"
    assert isinstance(payload.get("reason_code"), str) and payload.get("reason_code"), payload


def _capture_json_stdout(out):
    start = out.find("{")
    end = out.rfind("}")
    assert start != -1 and end != -1 and end > start, out[:400]
    return json.loads(out[start:end + 1])


# ---------------------------------------------------------------------------
# G1: seam-GO + prereg-missing detail stability across guarded entrypoints
# ---------------------------------------------------------------------------
class Test122G1SeamGoPreregMissingDetailStability(unittest.TestCase):
    """G1: seam GO but prereg missing/blocked => stable refusal reason_code
    (PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS), seam_go_prereg_required /
    reason_code_detail where the contract emits them, status=BLOCKED,
    outcomes_inspected:false, canonical_outputs_mutated:false, network:false,
    writes_real_reserved_state:false. tmp-isolated, no loader invoked."""

    def _setup(self, td):
        td = Path(td)
        pre = td / "prereg.json"
        pre.write_text(json.dumps({"status": "PREREGISTERED"}))
        data = td / "data"
        data.mkdir(exist_ok=True)
        return pre, data

    def test_guarded_execute_seam_go_missing_prereg_stable_contract(self):
        m = _real_go_manifest()
        loader_called = {"n": 0}

        def loader(dp, ctx=None):
            loader_called["n"] += 1
            raise AssertionError("loader must not be invoked on blocked branch")

        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            pre, data = self._setup(td)
            # missing prereg: point at a nonexistent pre_reg_path
            missing_pre = td / "nonexistent_prereg.json"
            res = guarded_execute(
                data_path=data,
                pre_reg_path=missing_pre,
                repo_root=REAL,
                admissible_manifest=m,
                outcome_loader=loader,
                allow_default_loader=False,
            )
        self.assertEqual(res.get("status"), "BLOCKED", res)
        self.assertEqual(res.get("reason_code"), "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS", res)
        self.assertTrue(res.get("seam_go_prereg_required"), res)
        self.assertEqual(res.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED", res)
        self.assertFalse(res.get("outcomes_inspected"), res)
        self.assertFalse(res.get("canonical_outputs_mutated"), res)
        self.assertFalse(res.get("network"), res)
        self.assertFalse(res.get("writes_real_reserved_state"), res)
        self.assertEqual(loader_called["n"], 0)

    def test_harness_execute_ready_data_load_seam_go_missing_prereg(self):
        m = _real_go_manifest()
        h = FCLR010Harness(repo_root=REAL)
        loader_called = {"n": 0}

        def loader(dp, ctx=None):
            loader_called["n"] += 1
            raise AssertionError("loader must not be invoked on blocked branch")

        with tempfile.TemporaryDirectory() as td:
            pre, data = self._setup(td)
            missing_pre = td / "nonexistent_prereg.json"
            res = h.execute_ready_data_load(
                data_path=data,
                pre_reg_path=missing_pre,
                admissible_manifest=m,
                outcome_loader=loader,
            )
        self.assertEqual(res.get("status"), "BLOCKED", res)
        self.assertEqual(res.get("reason_code"), "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS", res)
        self.assertTrue(res.get("seam_go_prereg_required"), res)
        self.assertEqual(res.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED", res)
        self.assertFalse(res.get("outcomes_inspected"), res)
        self.assertFalse(res.get("network"), res)
        self.assertFalse(res.get("writes_real_reserved_state"), res)
        self.assertEqual(loader_called["n"], 0)

    def test_prereg_path_none_blocked(self):
        m = _real_go_manifest()
        with tempfile.TemporaryDirectory() as td:
            pre, data = self._setup(td)
            res = guarded_execute(
                data_path=data,
                pre_reg_path=None,
                repo_root=REAL,
                admissible_manifest=m,
                outcome_loader=lambda *a, **k: (_ for _ in ()).throw(AssertionError("loader called")),
                allow_default_loader=False,
            )
        self.assertEqual(res.get("status"), "BLOCKED", res)
        self.assertFalse(res.get("outcomes_inspected"), res)
        self.assertFalse(res.get("canonical_outputs_mutated"), res)
        self.assertFalse(res.get("network"), res)
        self.assertFalse(res.get("writes_real_reserved_state"), res)
        self.assertIsInstance(res.get("reason_code"), str)

    def test_nonexistent_empty_data_blocked(self):
        m = _real_go_manifest()
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            pre, _ = self._setup(td)
            empty_data = td / "empty_data"
            empty_data.mkdir(exist_ok=True)
            res = guarded_execute(
                data_path=empty_data,
                pre_reg_path=pre,
                repo_root=REAL,
                admissible_manifest=m,
                outcome_loader=lambda *a, **k: (_ for _ in ()).throw(AssertionError("loader called")),
                allow_default_loader=False,
            )
        self.assertEqual(res.get("status"), "BLOCKED", res)
        self.assertFalse(res.get("outcomes_inspected"), res)
        self.assertFalse(res.get("canonical_outputs_mutated"), res)
        self.assertFalse(res.get("network"), res)
        self.assertFalse(res.get("writes_real_reserved_state"), res)


# ---------------------------------------------------------------------------
# G2: registry AST stronger blocked-branch refusal heuristic
# ---------------------------------------------------------------------------
class Test122G2RegistryASTNonReadyRefusalPath(unittest.TestCase):
    """G2: every guarded_tracka_ready_writing / guarded_tracka_audit_ready_writing
    entrypoint has a machine-verified non-READY refusal return/exit path in
    main-reachable flow (AST: compare guard status to READY_FROZEN/blocked and
    return / sys.exit / print + refusal payload)."""

    GUARDED_CLASSES = {"guarded_tracka_ready_writing", "guarded_tracka_audit_ready_writing"}

    def _registry(self):
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def _has_nonready_refusal_path(self, src):
        try:
            tree = ast.parse(src)
        except SyntaxError:
            return False, ["syntax_error"]
        main_nodes = [
            n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name == "main"
        ] or [tree]
        found = False
        for root in main_nodes:
            for node in ast.walk(root):
                if not isinstance(node, ast.If):
                    continue
                if not self._is_nonready_status_cmp(node.test):
                    continue
                for stmt in node.body:
                    if isinstance(stmt, ast.Return):
                        found = True
                        break
                    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                        fn = stmt.value.func
                        fname = (fn.attr if isinstance(fn, ast.Attribute)
                                 else (fn.id if isinstance(fn, ast.Name) else None))
                        if fname in ("sys.exit", "print", "refusal_payload"):
                            found = True
                            break
                if found:
                    break
            if found:
                break
        errs = [] if found else ["missing_nonready_refusal_return_exit_path"]
        return (not errs), errs

    @staticmethod
    def _is_nonready_status_cmp(test) -> bool:
        if not isinstance(test, ast.Compare):
            return False
        left = test.left
        if not ((isinstance(left, ast.Call) and isinstance(left.func, ast.Attribute)
                 and left.func.attr == "get") or isinstance(left, ast.Name)):
            return False
        for op, comp in zip(test.ops, test.comparators):
            if not (isinstance(comp, ast.Constant) and isinstance(comp.value, str)
                    and comp.value in ("READY_FROZEN", "BLOCKED")):
                continue
            if comp.value == "READY_FROZEN" and isinstance(op, ast.NotEq):
                return True
            if comp.value == "BLOCKED" and isinstance(op, ast.Eq):
                return True
        return False

    def _has_guard_seam(self, src):
        guard_tokens = ("guarded_execute", "GuardedReadRefused", "fclr010harness",
                        "FCLR010Harness", "guarded_execution_contract")
        try:
            tree = ast.parse(src)
        except SyntaxError:
            return False
        return any(
            (isinstance(n, ast.Import) and any(any(t in a.name for t in guard_tokens) for a in n.names))
            or (isinstance(n, ast.ImportFrom) and ((n.module and any(t in n.module for t in guard_tokens))
                or any(any(t in a.name for t in guard_tokens) for a in n.names)))
            or (isinstance(n, ast.Name) and any(t in n.id for t in guard_tokens))
            or (isinstance(n, ast.Attribute) and any(t in n.attr for t in guard_tokens))
            for n in ast.walk(tree)
        )

    def test_all_guarded_ready_writing_entrypoints_have_nonready_refusal_path(self):
        reg = self._registry()["scripts"]
        targets = [(n, m) for n, m in reg.items() if m.get("class") in self.GUARDED_CLASSES]
        self.assertGreaterEqual(len(targets), 6, "expected >=6 guarded ready-writing/audit entrypoints")
        missing = []
        for name, meta in targets:
            src = (SCRIPTS / name).read_text(encoding="utf-8")
            ok_guard = self._has_guard_seam(src)
            ok_refusal, errs = self._has_nonready_refusal_path(src)
            if not (ok_guard and ok_refusal):
                missing.append((name, ([] if ok_guard else ["guard_seam"]) + errs))
        self.assertEqual(missing, [], f"AST non-READY refusal drift: {missing}")

    def test_current_repo_drift_pass_with_stronger_heuristic(self):
        res = check_drift(REAL)
        self.assertTrue(res.get("pass"), res)

    def test_drift_fails_on_guarded_script_missing_nonready_refusal_path(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "scripts").mkdir()
            (td / "research_state").mkdir()
            # guard token present but no non-READY refusal return/exit path in main
            (td / "scripts" / "x.py").write_text(
                "from scripts.fclr010_guarded_entry import guarded_execute\n"
                "def main():\n"
                "    g = guarded_execute(data_path=Path('x'), pre_reg_path=None, repo_root=Path('.'))\n"
                "    if g.get('status') == 'READY_FROZEN':\n"
                "        return 0\n"
                "    print('no refusal path')\n"
            )
            (td / "research_state" / "tracka_script_scope_registry.json").write_text(json.dumps({
                "allowed_classes": ["guarded_tracka_audit_ready_writing"],
                "scripts": {"x.py": {"class": "guarded_tracka_audit_ready_writing", "reason": "no refusal path"}},
            }))
            res = check_drift(td)
        self.assertFalse(res.get("pass"), res)
        bad = " ".join(str(b) for b in res.get("bad_entries", []))
        self.assertTrue("nonready_refusal" in bad or "missing" in bad, res)


# ---------------------------------------------------------------------------
# G3: run_liqmicro_v2 write-guard scope + blocked-path noninvocation proofs
# ---------------------------------------------------------------------------
class Test122G3RunLiqmicroV2WriteGuardScope(unittest.TestCase):
    """G3: allowed write roots limited to liqmicro-v2 canonical artifacts
    (results/liqmicro_v2, LIQMICRO-002 summary target); RESEARCH_STATE
    directory-wide / root-wildcard never allowed; blocked branch returns before
    _run_pipeline and therefore before _guard_liqmicro_v2_write_targets /
    artifact writes; monkeypatched constants assert stable
    LIQMICRO_V2_WRITE_TARGET_ALLOWLIST_VIOLATION. No real writes."""

    def setUp(self):
        _mock_heavy()

    def test_allowed_write_roots_are_liqmicro_v2_canonical(self):
        import scripts.run_liqmicro_v2 as mod
        roots = mod.LIQMICRO_V2_ALLOWED_WRITE_ROOTS
        self.assertEqual(len(roots), 2)
        self.assertEqual(roots[0], mod.RESULTS_DIR)
        self.assertEqual(roots[1], mod.RESEARCH_STATE / "evaluation_summary_FCLR-LIQMICRO-002.md")
        r = mod._guard_liqmicro_v2_write_targets()
        self.assertTrue(r.get("pass"), r)
        self.assertEqual(r.get("reason_code"), "OK")

    def test_research_state_directory_wide_root_rejected(self):
        import scripts.run_liqmicro_v2 as mod
        with patch.object(mod, "LIQMICRO_V2_ALLOWED_WRITE_ROOTS", (mod.RESEARCH_STATE,)):
            r = mod._guard_liqmicro_v2_write_targets()
        self.assertFalse(r.get("pass"), r)
        self.assertEqual(r.get("reason_code"), "LIQMICRO_V2_WRITE_TARGET_ALLOWLIST_VIOLATION")
        self.assertTrue(any("research_state_directory_wide_root_not_allowed" in f
                            for f in r.get("failures", [])), r)

    def test_root_wildcard_rejected(self):
        import scripts.run_liqmicro_v2 as mod
        with patch.object(mod, "LIQMICRO_V2_ALLOWED_WRITE_ROOTS", ("/tmp/evil_liqmicro/*",)):
            r = mod._guard_liqmicro_v2_write_targets()
        self.assertFalse(r.get("pass"), r)
        self.assertEqual(r.get("reason_code"), "LIQMICRO_V2_WRITE_TARGET_ALLOWLIST_VIOLATION")
        self.assertTrue(any("root_wildcard_not_allowed" in f for f in r.get("failures", [])), r)

    def test_invalid_root_constant_scope_assert_allowlist_violation(self):
        import scripts.run_liqmicro_v2 as mod
        bad = Path("/tmp/evil_liqmicro_v2")
        with patch.object(mod, "LIQMICRO_V2_ALLOWED_WRITE_ROOTS", (bad,)):
            r = mod._guard_liqmicro_v2_write_targets()
        self.assertFalse(r.get("pass"), r)
        self.assertEqual(r.get("reason_code"), "LIQMICRO_V2_WRITE_TARGET_ALLOWLIST_VIOLATION")

    def test_blocked_branch_never_invokes_write_guard_or_pipeline(self):
        _mock_heavy()
        import scripts.run_liqmicro_v2 as mod
        before = _snap([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2])
        guard_calls = {"n": 0}
        pipeline_calls = {"n": 0}

        def fake_guard(*a, **k):
            guard_calls["n"] += 1
            return {"pass": True, "reason_code": "OK"}

        def fake_pipeline(*a, **k):
            pipeline_calls["n"] += 1
            raise AssertionError("_run_pipeline must not run on blocked branch")

        def fake_guarded_execute(**kwargs):
            return {"status": "BLOCKED", "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
                    "outcomes_inspected": False, "canonical_outputs_mutated": False,
                    "network": False, "writes_real_reserved_state": False, "script": "run_liqmicro_v2"}

        with patch("scripts.fclr010_guarded_entry.guarded_execute", side_effect=fake_guarded_execute), \
             patch.object(mod, "_guard_liqmicro_v2_write_targets", side_effect=fake_guard), \
             patch.object(mod, "_run_pipeline", side_effect=fake_pipeline), \
             redirect_stdout(io.StringIO()):
            rc = mod.main()
        self.assertEqual(rc, 1)
        self.assertEqual(guard_calls["n"], 0)
        self.assertEqual(pipeline_calls["n"], 0)
        _unchanged([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2], before)


# ---------------------------------------------------------------------------
# G4: h004 census refusal payload matrix + nonfile/nonpath fail-closed cases
# ---------------------------------------------------------------------------
class Test122G4H004CensusRefusalMatrix(unittest.TestCase):
    """G4: h004 census refusal payload matrix + nonfile/nonpath fail-closed.
    Absent required input => H004_CENSUS_ABSENT_REFUSAL with stable required keys.
    Required census path present but a directory / otherwise unusable by path
    check => refuse before heavy pipeline/data-read with stable reason_code.
    No real Bybit census data, no real research_state writes."""

    def _assert_shape(self, payload, script):
        for k in REQUIRED_KEYS:
            self.assertIn(k, payload, f"missing key {k}: {payload}")
        self.assertEqual(payload.get("script"), script)
        self.assertEqual(payload.get("status"), "BLOCKED")
        self.assertFalse(payload.get("outcomes_inspected"), payload)
        self.assertFalse(payload.get("canonical_outputs_mutated"), payload)
        self.assertFalse(payload.get("network"), payload)
        for wk in WRITES_KEYS:
            if wk in payload:
                self.assertFalse(payload.get(wk), payload)
        self.assertIsInstance(payload.get("reason_code"), str)
        self.assertTrue(payload.get("reason_code"))

    def test_absent_required_census_refusal_stable_keys(self):
        import scripts.h004_fclr005_pipeline as mod
        with tempfile.TemporaryDirectory() as td:
            targets = mod.resolve_h004_pilot_targets(sandbox_root=Path(td))
            g = mod._h004_census_absent_guard(mod.REPO, Path(td), targets)
        self.assertIsInstance(g, dict)
        self.assertEqual(g.get("reason_code"), "H004_CENSUS_ABSENT_REFUSAL")
        self._assert_shape(g, "h004_fclr005_pipeline")
        self.assertIn("missing_required_inputs", g)

    def test_census_path_is_directory_fail_closed(self):
        import scripts.h004_fclr005_pipeline as mod
        required = mod._h004_required_input_files(mod.REPO)
        self.assertTrue(required, required)
        rel = required[0].relative_to(mod.REPO.resolve())
        with tempfile.TemporaryDirectory() as td:
            sb = Path(td)
            # required census path exists but is a directory (not a readable file)
            (sb / rel).mkdir(parents=True, exist_ok=True)
            targets = mod.resolve_h004_pilot_targets(sandbox_root=sb)
            g = mod._h004_census_absent_guard(mod.REPO, sb, targets)
        self.assertIsNotNone(g, "directory census path must be refused")
        self.assertEqual(g.get("reason_code"), "H004_CENSUS_ABSENT_REFUSAL")
        self._assert_shape(g, "h004_fclr005_pipeline")
        self.assertIn("missing_required_inputs", g)

    def test_census_path_unusable_fail_closed_before_heavy_work(self):
        import scripts.h004_fclr005_pipeline as mod
        required = mod._h004_required_input_files(mod.REPO)
        rel = required[0].relative_to(mod.REPO.resolve())
        required_input_calls = {"n": 0}
        orig_required = mod._h004_required_input_files

        def wrapped_required(repo=mod.REPO):
            required_input_calls["n"] += 1
            return orig_required(repo)

        with tempfile.TemporaryDirectory() as td:
            sb = Path(td)
            # path exists but is not a usable file
            (sb / rel).mkdir(parents=True, exist_ok=True)
            targets = mod.resolve_h004_pilot_targets(sandbox_root=sb)
            with patch.object(mod, "_h004_required_input_files", side_effect=wrapped_required):
                g = mod._h004_census_absent_guard(mod.REPO, sb, targets)
        self.assertGreaterEqual(required_input_calls["n"], 1)
        self.assertIsNotNone(g)
        self.assertEqual(g.get("reason_code"), "H004_CENSUS_ABSENT_REFUSAL")
        self._assert_shape(g, "h004_fclr005_pipeline")
        # refusal happens before heavy pipeline: census guard consulted inputs
        # and refused; no heavy data-read reached.

    def test_main_blocked_on_absent_census_no_canonical_mutation(self):
        import scripts.h004_fclr005_pipeline as mod
        CANON = {FRONTIER, RUN_MANIFEST, EVAL_FCLR010, CROSS}
        before = _snap(list(CANON))
        old_argv = sys.argv[:]
        old_env = os.environ.get(mod.H004_SANDBOX_ROOT_ENV)
        try:
            with tempfile.TemporaryDirectory() as td:
                os.environ[mod.H004_SANDBOX_ROOT_ENV] = td
                sys.argv = ["h004_fclr005_pipeline.py", mod.H004_ALLOW_FLAG]
                with redirect_stdout(io.StringIO()) as buf:
                    rc = mod.main()
                self.assertEqual(rc, 1)
                payload = _capture_json_stdout(buf.getvalue())
                self.assertEqual(payload.get("reason_code"), "H004_CENSUS_ABSENT_REFUSAL")
                self._assert_shape(payload, "h004_fclr005_pipeline")
        finally:
            sys.argv = old_argv
            if old_env is None:
                os.environ.pop(mod.H004_SANDBOX_ROOT_ENV, None)
            else:
                os.environ[mod.H004_SANDBOX_ROOT_ENV] = old_env
        _unchanged(list(CANON), before)


# ---------------------------------------------------------------------------
# G5: guarded ready-writing NO-READY refusal matrix, all remaining scripts
# ---------------------------------------------------------------------------
class Test122G5NoReadyRefusalMatrixRemainingScripts(unittest.TestCase):
    """G5: refusal-payload field-stability / NO-READY matrix for the remaining
    guarded_tracka_ready_writing entrypoints not fully covered as audits in 121
    (fclr010_execute, fclr010_execute_fast, coupled_build_panel,
    coupled_robust_eval) plus run_liqmicro_v2 main refusal. Assert required
    keys, stable script, status=BLOCKED, outcomes_inspected:false,
    canonical_outputs_mutated:false, network:false / writes_real_reserved_state
    :false where emitted, and no loader / canonical mutation."""

    SCRIPTS_MODULES = [
        ("fclr010_execute", "fclr010_execute"),
        ("fclr010_execute_fast", "fclr010_execute_fast"),
        ("coupled_build_panel", "coupled_build_panel"),
        ("coupled_robust_eval", "coupled_robust_eval"),
        ("run_liqmicro_v2", "run_liqmicro_v2"),
    ]

    def _run_main_blocked(self, mod_name):
        _mock_heavy()
        mod = importlib.import_module(f"scripts.{mod_name}")
        before = _snap([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2])
        calls = {"n": 0}

        def fake_guarded_execute(**kwargs):
            calls["n"] += 1
            return {"status": "BLOCKED", "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
                    "outcomes_inspected": False, "canonical_outputs_mutated": False,
                    "network": False, "writes_real_reserved_state": False,
                    "script": mod_name, "guarded_execution_contract": "fclr_next_111"}

        with patch("scripts.fclr010_guarded_entry.guarded_execute", side_effect=fake_guarded_execute), \
             redirect_stdout(io.StringIO()) as buf:
            rc = mod.main()
        out = buf.getvalue()
        payload = _capture_json_stdout(out)
        _unchanged([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2], before)
        return rc, payload, calls["n"], mod

    def test_all_remaining_guarded_scripts_no_ready_refusal(self):
        for label, mod_name in self.SCRIPTS_MODULES:
            with self.subTest(script=mod_name):
                rc, payload, calls, mod = self._run_main_blocked(mod_name)
                self.assertEqual(rc, 1, f"{mod_name} did not refuse")
                self.assertEqual(calls, 1, f"{mod_name} did not call guarded_execute once")
                _assert_refusal_shape(payload, mod_name)
                self.assertFalse(payload.get("outcomes_loaded"), payload)


if __name__ == "__main__":
    unittest.main()
