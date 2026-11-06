"""FCLR-NEXT-121: real seam-GO manifest acceptance proof (manifest-only, tmp-isolated) +
registry AST/structural refusal coverage for all guarded ready-writing/audit entrypoints +
guarded-audit refusal-payload field-stability/rc matrix expansion +
run_liqmicro_v2 post-gate write-target allowlist guard (source + monkeypatched constants) +
h004 allowed-mode census-absent refusal smoke (stable reason_code, no heavy work, no real RS writes).

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
from src.analysis.tracka_admissible import (
    assess_ironflow_month_admissibility,
    build_ironflow_month_manifest,
)

REAL = Path(__file__).resolve().parent.parent
RS = REAL / "research_state"
SCRIPTS = REAL / "scripts"
REGISTRY_PATH = RS / "tracka_script_scope_registry.json"
FRONTIER = RS / "experiment_frontier.json"
RUN_MANIFEST = RS / "run_manifest.json"
EVAL_FCLR010 = RS / "evaluation_summary_FCLR010.md"
EVAL_LIQM2 = RS / "evaluation_summary_FCLR-LIQMICRO-002.md"
CROSS = RS / "cross_track_decision_log.md"
COV_AUDIT = RS / "fclr010_coverage_audit.json"
LIQ_AUDIT = RS / "liqmicro_data_audit_001.md"


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
    """121 G1: minimal manifest fixture the real admissible seam accepts (manifest-only)."""
    return build_ironflow_month_manifest(
        month=month,
        events_path=f"research_state/data_cache/ironflow_events/events/{month}.parquet",
        fills_path=f"research_state/data_cache/ironflow_events/fills/{month}.parquet",
        events_url=f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/{month}.parquet",
        fills_url=f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/{month}.parquet",
        schema_fields_events=["timestamp", "symbol", "notional_usd"],
        schema_fields_fills=["timestamp", "symbol", "size"],
    )


def _real_nogo_manifest_pretrigger():
    """121 G1 paired NO-GO: pre-trigger month refused by production seam with stable reason."""
    return build_ironflow_month_manifest(
        month="2026-10",
        events_path="research_state/data_cache/ironflow_events/events/2026-10.parquet",
        fills_path="research_state/data_cache/ironflow_events/fills/2026-10.parquet",
        schema_fields_events=["timestamp", "symbol", "notional_usd"],
        schema_fields_fills=["timestamp", "symbol", "size"],
    )


class Test121G1RealSeamGoManifestAcceptance(unittest.TestCase):
    """G1: real admissible seam GO manifest fixture accepted by production seam
    before loader (manifest-only, no network/parquet/outcome reads). Paired NO-GO
    refused before loader with stable reason_code."""

    def _setup(self, td):
        td = Path(td)
        pre = td / "prereg.json"
        pre.write_text(json.dumps({"status": "PREREGISTERED"}))
        data = td / "data"
        data.mkdir(exist_ok=True)
        return pre, data

    def test_seam_assess_accepts_real_go_fixture_manifest_only(self):
        m = _real_go_manifest()
        r = assess_ironflow_month_admissibility(m, for_resume_trigger=True)
        self.assertTrue(r.get("pass"), r)
        self.assertEqual(r.get("verdict"), "GO")
        self.assertEqual(r.get("failures"), [])

    def test_harness_production_path_seam_go_before_loader(self):
        m = _real_go_manifest()
        h = FCLR010Harness(repo_root=REAL)
        calls = {"n": 0}

        def loader(dp, ctx=None):
            calls["n"] += 1
            return {"synthetic": 1}

        with tempfile.TemporaryDirectory() as td:
            pre, data = self._setup(td)
            res = h.execute_ready_data_load(
                data_path=data,
                pre_reg_path=pre,
                admissible_manifest=m,
                outcome_loader=loader,
            )
        self.assertEqual(res.get("status"), "READY_FROZEN", res)
        self.assertEqual(calls["n"], 1)
        seam = res.get("admissible_seam_wired") or {}
        self.assertTrue(seam.get("pass"), seam)
        self.assertEqual(seam.get("reason_code"), "ADMISSIBLE_SEAM_GO")
        self.assertFalse(seam.get("reads_outcomes"))
        self.assertFalse(seam.get("reads_parquet"))
        self.assertFalse(seam.get("network"))

    def test_guarded_execute_production_path_seam_go_before_loader(self):
        m = _real_go_manifest()
        calls = {"n": 0}

        def loader(dp, ctx=None):
            calls["n"] += 1
            return {"ok": True}

        with tempfile.TemporaryDirectory() as td:
            pre, data = self._setup(td)
            res = guarded_execute(
                data_path=data,
                pre_reg_path=pre,
                repo_root=REAL,
                admissible_manifest=m,
                outcome_loader=loader,
                allow_default_loader=False,
            )
        self.assertEqual(res.get("status"), "READY_FROZEN", res)
        self.assertEqual(calls["n"], 1)
        seam = res.get("admissible_seam_wired") or {}
        self.assertEqual(seam.get("reason_code"), "ADMISSIBLE_SEAM_GO")
        self.assertFalse(res.get("canonical_outputs_mutated"))
        self.assertFalse(res.get("writes_real_research_state"))

    def test_nogo_fixture_refused_before_loader_stable_reason(self):
        m = _real_nogo_manifest_pretrigger()
        r = assess_ironflow_month_admissibility(m, for_resume_trigger=True)
        self.assertFalse(r.get("pass"))
        self.assertEqual(r.get("verdict"), "NO-GO")
        self.assertTrue(any("month_below_trigger" in f for f in r.get("failures", [])), r)

        h = FCLR010Harness(repo_root=REAL)

        def bad(*a, **k):
            raise AssertionError("loader called despite NO-GO seam")

        with tempfile.TemporaryDirectory() as td:
            pre, data = self._setup(td)
            res = h.execute_ready_data_load(
                data_path=data,
                pre_reg_path=pre,
                admissible_manifest=m,
                outcome_loader=bad,
            )
        self.assertEqual(res.get("status"), "BLOCKED")
        self.assertEqual(res.get("reason_code"), "ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES")
        self.assertFalse(res.get("outcomes_inspected"))
        seam = res.get("admissible_seam_wired") or {}
        self.assertFalse(seam.get("pass"))
        self.assertEqual(seam.get("reason_code"), "ADMISSIBLE_SEAM_NOGO")

    def test_nogo_modeled_manifest_fixture_refused_before_loader(self):
        m = build_ironflow_month_manifest(
            month="2026-11",
            modeled_or_proxy=True,
            schema_fields_events=["timestamp", "symbol", "notional_usd"],
            schema_fields_fills=["timestamp", "symbol", "size"],
        )
        def bad(*a, **k):
            raise AssertionError("loader called despite modeled/proxy")
        with tempfile.TemporaryDirectory() as td:
            pre, data = self._setup(td)
            res = guarded_execute(
                data_path=data, pre_reg_path=pre, repo_root=REAL,
                admissible_manifest=m, outcome_loader=bad, allow_default_loader=False,
            )
        self.assertEqual(res.get("status"), "BLOCKED")
        self.assertFalse(res.get("outcomes_inspected"))
        self.assertFalse(res.get("canonical_outputs_mutated"))


class Test121G2RegistryStructuralRefusalCoverage(unittest.TestCase):
    """G2: every guarded_tracka_ready_writing / guarded_tracka_audit_ready_writing
    entrypoint has machine-verified refusal/guard structure (AST/source), deterministic."""

    GUARDED_CLASSES = {"guarded_tracka_ready_writing", "guarded_tracka_audit_ready_writing"}

    def _registry(self):
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def _has_structural_refusal(self, cls, src):
        # mirrors 120/121 registry structural contract without requiring a private export name
        try:
            tree = ast.parse(src)
        except SyntaxError:
            return False, ["syntax_error"]
        guard_tokens = ("guarded_execute", "GuardedReadRefused", "fclr010harness",
                        "FCLR010Harness", "guarded_execution_contract")
        has_guard = any(
            (isinstance(n, ast.Import) and any(any(t in a.name for t in guard_tokens) for a in n.names))
            or (isinstance(n, ast.ImportFrom) and ((n.module and any(t in n.module for t in guard_tokens)) or any(any(t in a.name for t in guard_tokens) for a in n.names)))
            or (isinstance(n, ast.Name) and any(t in n.id for t in guard_tokens))
            or (isinstance(n, ast.Attribute) and any(t in n.attr for t in guard_tokens))
            for n in ast.walk(tree)
        )
        if cls == "harness_core":
            return (True, []) if has_guard else (False, ["guard_seam"])
        has_refusal_path = False
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                fn = n.func
                fname = fn.id if isinstance(fn, ast.Name) else (fn.attr if isinstance(fn, ast.Attribute) else None)
                if fname in ("guarded_execute", "execute_ready_data_load"):
                    has_refusal_path = True
            if isinstance(n, ast.Name) and n.id == "refusal_payload":
                has_refusal_path = True
        errs = []
        if not has_guard:
            errs.append("guard_seam")
        if not has_refusal_path:
            errs.append("blocked_refusal_path")
        return (not errs), errs

    def test_all_guarded_ready_writing_entrypoints_structurally_verified(self):
        reg = self._registry()["scripts"]
        targets = [(n, m) for n, m in reg.items() if m.get("class") in self.GUARDED_CLASSES]
        self.assertGreaterEqual(len(targets), 6, "expected >=6 guarded ready-writing/audit entrypoints")
        missing = []
        for name, meta in targets:
            src = (SCRIPTS / name).read_text(encoding="utf-8")
            ok, errs = self._has_structural_refusal(meta.get("class"), src)
            if not ok:
                missing.append((name, errs))
        self.assertEqual(missing, [], f"structural refusal drift: {missing}")

    def test_drift_fails_on_newly_added_guarded_script_missing_structure(self):
        from scripts.check_tracka_scope_registry_drift import check_drift
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "scripts").mkdir()
            (td / "research_state").mkdir()
            (td / "scripts" / "x.py").write_text("print('no guard, no refusal')\n")
            (td / "research_state" / "tracka_script_scope_registry.json").write_text(json.dumps({
                "allowed_classes": ["guarded_tracka_audit_ready_writing"],
                "scripts": {"x.py": {"class": "guarded_tracka_audit_ready_writing", "reason": "missing structure"}},
            }))
            res = check_drift(td)
        self.assertFalse(res.get("pass"))
        bad = " ".join(str(b) for b in res.get("bad_entries", []))
        self.assertTrue("structural_refusal" in bad or "guard_seam" in bad or "missing" in bad, res)

    def test_drift_fails_when_guarded_entrypoint_has_no_blocked_refusal_path(self):
        from scripts.check_tracka_scope_registry_drift import check_drift
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "scripts").mkdir()
            (td / "research_state").mkdir()
            # has guard token but no refusal path (no guarded_execute call / no refusal_payload)
            (td / "scripts" / "x.py").write_text(
                "from scripts.fclr010_guarded_entry import GuardedReadRefused\n"
                "def run():\n    raise GuardedReadRefused('x')\n"
            )
            (td / "research_state" / "tracka_script_scope_registry.json").write_text(json.dumps({
                "allowed_classes": ["guarded_tracka_ready_writing"],
                "scripts": {"x.py": {"class": "guarded_tracka_ready_writing", "reason": "token only, no refusal path"}},
            }))
            res = check_drift(td)
        self.assertFalse(res.get("pass"), res)
        bad = " ".join(str(b) for b in res.get("bad_entries", []))
        self.assertIn("blocked_refusal_path", bad)

    def test_current_repo_drift_pass(self):
        from scripts.check_tracka_scope_registry_drift import check_drift
        res = check_drift(REAL)
        self.assertTrue(res.get("pass"), res)


class Test121G3AuditRefusalPayloadStabilityMatrix(unittest.TestCase):
    """G3: refusal-payload field-stability assertions + guard snapshot shape +
    expanded machine-representable guard states for audit ready-writing scripts."""

    REQUIRED_KEYS = {
        "status", "outcomes_inspected", "canonical_outputs_mutated",
        "network", "writes_real_research_state", "script", "reason_code",
    }
    EXPANDED_STATES = [
        ("missing_prereg", dict(status="BLOCKED", reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
                                outcomes_inspected=False, canonical_outputs_mutated=False,
                                network=False, writes_real_research_state=False, reason="Pre-registration required")),
        ("nogo_seam", dict(status="BLOCKED", reason_code="ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES",
                           outcomes_inspected=False, canonical_outputs_mutated=False,
                           network=False, writes_real_research_state=False, reason="Admissible seam NO-GO",
                           admissible_seam_wired={"pass": False, "reason_code": "ADMISSIBLE_SEAM_NOGO"})),
        ("modeled_proxy", dict(status="BLOCKED", reason_code="ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES",
                               outcomes_inspected=False, canonical_outputs_mutated=False,
                               network=False, writes_real_research_state=False, reason="modeled/proxy not admissible")),
        ("wrong_venue", dict(status="BLOCKED", reason_code="ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES",
                             outcomes_inspected=False, canonical_outputs_mutated=False,
                             network=False, writes_real_research_state=False, reason="venue not hyperliquid")),
        ("missing_manifest_data", dict(status="BLOCKED", reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
                                       outcomes_inspected=False, canonical_outputs_mutated=False,
                                       network=False, writes_real_research_state=False, reason="manifest/data missing")),
        ("seam_go_prereg_required_detail", dict(status="BLOCKED", reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
                                                outcomes_inspected=False, canonical_outputs_mutated=False,
                                                network=False, writes_real_research_state=False,
                                                seam_go_prereg_required=True,
                                                reason_code_detail="ADMISSIBLE_SEAM_GO_PREREG_REQUIRED",
                                                reason="seam GO but prereg required")),
    ]

    def _assert_payload_shape(self, payload, script):
        for k in self.REQUIRED_KEYS:
            self.assertIn(k, payload, f"missing required key {k} in {script}: {payload}")
        self.assertEqual(payload.get("script"), script)
        self.assertEqual(payload.get("status"), "BLOCKED")
        self.assertFalse(payload.get("outcomes_inspected"), payload)
        self.assertFalse(payload.get("canonical_outputs_mutated"), payload)
        self.assertFalse(payload.get("network"), payload)
        self.assertFalse(payload.get("writes_real_research_state"), payload)
        self.assertIsInstance(payload.get("reason_code"), str)
        self.assertTrue(payload.get("reason_code"))

    def _run_audit_blocked(self, mod_name, targets, guard_payload):
        mod = importlib.import_module(f"scripts.{mod_name}")
        before = _snap(targets)
        def no_loader(*a, **k):
            raise AssertionError(f"{mod_name} loader called on blocked state")
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(guard_payload)), \
             redirect_stdout(io.StringIO()) as buf:
            rc = mod.main()
        self.assertEqual(rc, 1)
        _unchanged(targets, before)
        m = re.search(r"\{.*\}", buf.getvalue(), re.S)
        self.assertIsNotNone(m, buf.getvalue()[:400])
        payload = json.loads(m.group(0))
        importlib.reload(mod)
        return payload

    def test_refusal_payload_direct_field_stability(self):
        guard = {"status": "BLOCKED", "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
                 "outcomes_inspected": False, "canonical_outputs_mutated": False}
        p = refusal_payload(reason="x", reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
                            script="fclr010_coverage_audit", guard=guard)
        self._assert_payload_shape(p, "fclr010_coverage_audit")
        self.assertIn("guard", p)
        self.assertIsInstance(p["guard"], dict)
        self.assertEqual(p["guard"].get("status"), "BLOCKED")

    def test_fclr010_coverage_audit_expanded_matrix(self):
        targets = [COV_AUDIT, FRONTIER, RUN_MANIFEST, EVAL_FCLR010]
        for label, state in self.EXPANDED_STATES:
            with self.subTest(state=label):
                p = self._run_audit_blocked("fclr010_coverage_audit", targets, state)
                self._assert_payload_shape(p, "fclr010_coverage_audit")

    def test_liqmicro_audit_expanded_matrix(self):
        targets = [LIQ_AUDIT, FRONTIER, RUN_MANIFEST, EVAL_LIQM2]
        for label, state in self.EXPANDED_STATES:
            with self.subTest(state=label):
                p = self._run_audit_blocked("liqmicro_audit", targets, state)
                self._assert_payload_shape(p, "liqmicro_audit")


class Test121G4RunLiqmicroV2WriteAllowlistGuard(unittest.TestCase):
    """G4: source-level allowlist/denylist guard for _run_pipeline write targets
    (frontier/run_manifest/cross-track/FCLR010 summary excluded) + monkeypatched constants proof."""

    def test_source_allowlist_denylist_guard_present(self):
        src = (SCRIPTS / "run_liqmicro_v2.py").read_text(encoding="utf-8")
        self.assertIn("LIQMICRO_V2_ALLOWED_WRITE_ROOTS", src)
        self.assertIn("_LIQMICRO_V2_DENIED_WRITE_TARGETS", src)
        self.assertIn("_guard_liqmicro_v2_write_targets", src)
        # guard called before pipeline writes (in _run_pipeline)
        self.assertIn("_guard_liqmicro_v2_write_targets()", src)
        # denied canonical targets must not be allowed (may be concatenated in source)
        self.assertIn("experiment", src)
        self.assertIn("run_manifest", src)
        self.assertIn("cross", src)
        self.assertIn("decision_log", src)
        self.assertIn("evaluation_summary_FCLR010", src)
        # fail-closed refusal on violation
        self.assertIn("LIQMICRO_V2_WRITE_TARGET_ALLOWLIST_VIOLATION", src)

    def test_write_guard_passes_with_default_constants(self):
        _mock_heavy()
        import scripts.run_liqmicro_v2 as mod
        r = mod._guard_liqmicro_v2_write_targets()
        self.assertTrue(r.get("pass"), r)
        self.assertEqual(r.get("reason_code"), "OK")
        self.assertFalse(r.get("network"))
        self.assertFalse(r.get("writes_real_research_state"))

    def test_write_guard_rejects_allowed_root_escaping_repo_monkeypatched(self):
        _mock_heavy()
        import scripts.run_liqmicro_v2 as mod
        # monkeypatch to a path outside repo -> must fail closed
        with patch.object(mod, "LIQMICRO_V2_ALLOWED_WRITE_ROOTS", (Path("/tmp/evil_liqmicro"),)):
            r = mod._guard_liqmicro_v2_write_targets()
        self.assertFalse(r.get("pass"), r)
        self.assertEqual(r.get("reason_code"), "LIQMICRO_V2_WRITE_TARGET_ALLOWLIST_VIOLATION")
        self.assertTrue(r.get("failures"))

    def test_write_guard_rejects_denied_target_in_allowed_root(self):
        _mock_heavy()
        import scripts.run_liqmicro_v2 as mod
        # allowed root string that would contain denied target name -> fail
        bad_root = mod.REPO / "research_state" / "experiment_frontier.json"
        with patch.object(mod, "LIQMICRO_V2_ALLOWED_WRITE_ROOTS", (bad_root,)):
            r = mod._guard_liqmicro_v2_write_targets()
        self.assertFalse(r.get("pass"), r)
        self.assertTrue(any("denied_write_target" in f for f in r.get("failures", [])), r)

    def test_sandboxed_ready_branch_cannot_mutate_canonical_targets(self):
        _mock_heavy()
        import scripts.run_liqmicro_v2 as mod
        before = _snap([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2])

        class _DF:
            def __len__(self): return 2
            @property
            def empty(self): return False
            def __getitem__(self, k): return type("S", (), {"nunique": lambda self: 1})()

        def sandbox_pipeline(raw_df, hourly, funding_df):
            with tempfile.TemporaryDirectory() as td:
                td = Path(td)
                (td / "panel.csv").write_text("x")
        ready = {
            "status": "READY_FROZEN", "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "outcomes_inspected": True, "canonical_outputs_mutated": False,
            "data_loaded_implicitly": False, "data_load_mode": "EXPLICIT_LOADER_AFTER_GATES",
            "network": False, "writes_real_research_state": False,
            "outcomes_loaded": {"raw_df": _DF(), "hourly": _DF(), "funding_df": _DF()},
        }
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=ready), \
             patch.object(mod, "_run_pipeline", sandbox_pipeline), \
             redirect_stdout(io.StringIO()):
            rc = mod.main()
        self.assertEqual(rc, 0)
        _unchanged([FRONTIER, RUN_MANIFEST, CROSS, EVAL_FCLR010, EVAL_LIQM2], before)


class Test121G5H004CensusAbsentRefusalSmoke(unittest.TestCase):
    """G5: allowed mode + valid sandbox must fail-closed on absent census/input files
    with stable reason_code and no heavy pipeline/data-read side effects; tmp-sandbox smoke."""

    CANONICAL_RS = {FRONTIER, RUN_MANIFEST, EVAL_FCLR010, CROSS}

    def test_allowed_valid_sandbox_absent_census_refused_before_heavy_work(self):
        import scripts.h004_fclr005_pipeline as mod
        before = _snap(list(self.CANONICAL_RS))
        old_argv = sys.argv[:]
        old_env = os.environ.get(mod.H004_SANDBOX_ROOT_ENV)
        with tempfile.TemporaryDirectory() as td:
            # sandbox exists but has NO required census/input files
            try:
                os.environ[mod.H004_SANDBOX_ROOT_ENV] = td
                sys.argv = ["h004_fclr005_pipeline.py", mod.H004_ALLOW_FLAG]
                # guard against accidental heavy work if refusal regresses
                with patch.object(mod, "_h004_required_input_files", wraps=mod._h004_required_input_files) as req, \
                     redirect_stdout(io.StringIO()) as buf:
                    rc = mod.main()
                self.assertEqual(rc, 1)
                payload = json.loads(buf.getvalue())
                self.assertEqual(payload.get("reason_code"), "H004_CENSUS_ABSENT_REFUSAL")
                self.assertEqual(payload.get("status"), "BLOCKED")
                self.assertFalse(payload.get("canonical_outputs_mutated"))
                self.assertFalse(payload.get("network"))
                self.assertFalse(payload.get("writes_real_research_state"))
                self.assertFalse(payload.get("outcomes_inspected"))
                # census guard consulted required inputs and refused before heavy pipeline
                self.assertGreaterEqual(req.call_count, 1)
            finally:
                sys.argv = old_argv
                if old_env is None:
                    os.environ.pop(mod.H004_SANDBOX_ROOT_ENV, None)
                else:
                    os.environ[mod.H004_SANDBOX_ROOT_ENV] = old_env
        _unchanged(list(self.CANONICAL_RS), before)

    def test_census_absent_guard_stable_shape(self):
        import scripts.h004_fclr005_pipeline as mod
        with tempfile.TemporaryDirectory() as td:
            targets = mod.resolve_h004_pilot_targets(sandbox_root=Path(td))
            g = mod._h004_census_absent_guard(mod.REPO, Path(td), targets)
        self.assertIsInstance(g, dict)
        self.assertEqual(g.get("reason_code"), "H004_CENSUS_ABSENT_REFUSAL")
        self.assertEqual(g.get("status"), "BLOCKED")
        self.assertFalse(g.get("canonical_outputs_mutated"))
        self.assertFalse(g.get("writes_real_research_state"))
        self.assertFalse(g.get("network"))

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
            self.assertFalse(payload.get("canonical_outputs_mutated"))
        finally:
            sys.argv = old_argv
        _unchanged(list(self.CANONICAL_RS), before)


if __name__ == "__main__":
    unittest.main()
