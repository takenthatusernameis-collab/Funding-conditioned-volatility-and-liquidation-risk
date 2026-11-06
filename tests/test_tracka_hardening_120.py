"""FCLR-NEXT-120: explicit seam-GO manifest-only READY_FROZEN matrix +
Track A registry semantic consistency drift + guarded audit-ready-writing
NO-READY refusal matrix + run_liqmicro_v2 sandboxed READY-pipeline contract +
h004 allowed-pilot sandbox-root enforcement.

Deterministic, tmp-isolated, no network, no parquet/outcome reads,
no real research_state writes.
"""
from __future__ import annotations

import importlib
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.analysis.tracka_admissible import build_ironflow_month_manifest
from scripts.fclr010_guarded_entry import guarded_execute
from scripts.fclr010_harness import FCLR010Harness

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

CANONICAL = [FRONTIER, RUN_MANIFEST, EVAL_FCLR010, EVAL_LIQM2, CROSS, COV_AUDIT, LIQ_AUDIT]


def _snap(paths):
    return {str(p): (p.read_bytes() if p.exists() else None) for p in paths}


def _unchanged(paths, before):
    for s, b in before.items():
        p = Path(s)
        a = p.read_bytes() if p.exists() else None
        if b != a:
            raise AssertionError(f"canonical target mutated: {s}")


def _go_manifest(month="2026-11"):
    return build_ironflow_month_manifest(month=month)


def _nogo_modeled(month="2026-11"):
    return build_ironflow_month_manifest(month=month, modeled_or_proxy=True)


def _nogo_wrong_venue(month="2026-11"):
    return build_ironflow_month_manifest(month=month, venue="binance")


def _nogo_proxy_label(month="2026-11"):
    m = build_ironflow_month_manifest(month=month)
    m["label_definition"] = "estimated_proxy_liquidation"
    return m


class Test120G1HarnessExplicitSeamGoManifestOnly(unittest.TestCase):
    """G1: explicit admissible seam GO minimal manifest -> READY_FROZEN +
    explicit loader once; NO-GO seam refuses before loader. No real trigger,
    no network/parquet/outcome reads, no real research_state writes."""

    def _setup(self, td):
        td = Path(td)
        pre = td / "prereg.json"
        pre.write_text(json.dumps({"status": "PREREGISTERED"}))
        data = td / "data"
        data.mkdir(exist_ok=True)
        return pre, data

    def test_harness_execute_ready_data_load_seam_go_manifest_only(self):
        m = _go_manifest()
        h = FCLR010Harness(repo_root=REAL)
        calls = {"n": 0}

        def loader(dp, ctx=None):
            calls["n"] += 1
            self.assertIsInstance(dp, Path)
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
        self.assertEqual(res.get("data_loaded_implicitly"), False)
        self.assertEqual(res.get("data_load_mode"), "EXPLICIT_LOADER_AFTER_GATES")
        seam = res.get("admissible_seam_wired") or {}
        self.assertTrue(seam.get("pass"))
        self.assertEqual(seam.get("reason_code"), "ADMISSIBLE_SEAM_GO")
        self.assertFalse(seam.get("reads_outcomes"))
        self.assertFalse(seam.get("reads_parquet"))
        self.assertFalse(seam.get("network"))

    def test_guarded_execute_seam_go_manifest_only(self):
        m = _go_manifest()
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
        self.assertEqual(res.get("data_loaded_implicitly"), False)
        self.assertEqual(res.get("data_load_mode"), "EXPLICIT_LOADER_AFTER_GATES")
        self.assertFalse(res.get("canonical_outputs_mutated"))
        self.assertFalse(res.get("network"))
        self.assertFalse(res.get("writes_real_research_state"))

    def test_harness_seam_nogo_modeled_refuses_before_loader(self):
        h = FCLR010Harness(repo_root=REAL)

        def bad(*a, **k):
            raise AssertionError("loader called despite NO-GO seam")

        with tempfile.TemporaryDirectory() as td:
            pre, data = self._setup(td)
            res = h.execute_ready_data_load(
                data_path=data,
                pre_reg_path=pre,
                admissible_manifest=_nogo_modeled(),
                outcome_loader=bad,
            )
        self.assertEqual(res.get("status"), "BLOCKED")
        self.assertEqual(res.get("reason_code"), "ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES")
        self.assertFalse(res.get("outcomes_inspected"))
        seam = res.get("admissible_seam_wired") or {}
        self.assertFalse(seam.get("pass"))

    def test_guarded_seam_nogo_wrong_venue_refuses_before_loader(self):
        def bad(*a, **k):
            raise AssertionError("loader called despite wrong venue")

        with tempfile.TemporaryDirectory() as td:
            pre, data = self._setup(td)
            res = guarded_execute(
                data_path=data,
                pre_reg_path=pre,
                repo_root=REAL,
                admissible_manifest=_nogo_wrong_venue(),
                outcome_loader=bad,
                allow_default_loader=False,
            )
        self.assertEqual(res.get("status"), "BLOCKED")
        self.assertFalse(res.get("outcomes_inspected"))
        self.assertFalse(res.get("canonical_outputs_mutated"))

    def test_seam_go_but_missing_prereg_still_refuses_before_loader(self):
        def bad(*a, **k):
            raise AssertionError("loader called without prereg")

        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"
            data.mkdir()
            res = guarded_execute(
                data_path=data,
                pre_reg_path=None,
                repo_root=REAL,
                admissible_manifest=_go_manifest(),
                outcome_loader=bad,
                allow_default_loader=False,
            )
        self.assertEqual(res.get("status"), "BLOCKED")
        self.assertFalse(res.get("outcomes_inspected"))
        # stable 108/110 surface preserved
        self.assertIn(res.get("reason_code"), ("PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS", "PREREG_REQUIRED_BEFORE_DATA_LOAD"))

    def test_seam_go_manifest_only_build_passes_admissibility(self):
        from src.analysis.tracka_admissible import assess_ironflow_month_admissibility

        r = assess_ironflow_month_admissibility(_go_manifest())
        self.assertTrue(r.get("pass"))
        self.assertEqual(r.get("verdict"), "GO")


class Test120G2ScopeRegistrySemanticConsistency(unittest.TestCase):
    """G2: drift fails on class/source semantic inconsistency for guarded/liquidation."""

    def test_current_repo_passes(self):
        from scripts.check_tracka_scope_registry_drift import check_drift

        res = check_drift(REAL)
        self.assertTrue(res.get("pass"), res)

    def test_detects_guarded_ready_writing_missing_guard_tokens(self):
        from scripts.check_tracka_scope_registry_drift import check_drift

        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "scripts").mkdir()
            (td / "research_state").mkdir()
            (td / "scripts" / "x.py").write_text("print('no guard here')\n")
            (td / "research_state" / "tracka_script_scope_registry.json").write_text(json.dumps({
                "allowed_classes": ["guarded_tracka_ready_writing"],
                "scripts": {"x.py": {"class": "guarded_tracka_ready_writing", "reason": "says guarded but source lacks tokens"}},
            }))
            res = check_drift(td)
        self.assertFalse(res.get("pass"))
        self.assertTrue(any("guard_tokens" in str(b) or "ready_writing" in str(b) for b in res.get("bad_entries", [])), res)

    def test_detects_track_c_labeled_guarded(self):
        from scripts.check_tracka_scope_registry_drift import check_drift

        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "scripts").mkdir()
            (td / "research_state").mkdir()
            (td / "scripts" / "track_c_foo.py").write_text("from scripts.fclr010_guarded_entry import guarded_execute\n")
            (td / "research_state" / "tracka_script_scope_registry.json").write_text(json.dumps({
                "allowed_classes": ["guarded_tracka"],
                "scripts": {"track_c_foo.py": {"class": "guarded_tracka", "reason": "wrongly labeled track c as guarded"}},
            }))
            res = check_drift(td)
        self.assertFalse(res.get("pass"))

    def test_detects_raw_fetch_claiming_hyperliquid_guarded_seam(self):
        from scripts.check_tracka_scope_registry_drift import check_drift

        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "scripts").mkdir()
            (td / "research_state").mkdir()
            (td / "scripts" / "probe.py").write_text("HYPERLIQUID_FCLR010_GUARDED_SEAM = True\n")
            (td / "research_state" / "tracka_script_scope_registry.json").write_text(json.dumps({
                "allowed_classes": ["raw_fetch_monitor_provenance"],
                "scripts": {"probe.py": {"class": "raw_fetch_monitor_provenance", "reason": "provenance probe but claims seam"}},
            }))
            res = check_drift(td)
        self.assertFalse(res.get("pass"))


class Test120G3GuardedAuditReadyWritingNoReadyMatrix(unittest.TestCase):
    """G3: fclr010_coverage_audit + liqmicro_audit NO-READY refusal matrix."""

    STATES = [
        ("missing_prereg", dict(status="BLOCKED", reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
                                outcomes_inspected=False, canonical_outputs_mutated=False,
                                reason="Pre-registration required")),
        ("nogo_seam", dict(status="BLOCKED", reason_code="ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES",
                           outcomes_inspected=False, canonical_outputs_mutated=False,
                           reason="Admissible seam NO-GO", admissible_seam_wired={"pass": False})),
        ("modeled_proxy", dict(status="BLOCKED", reason_code="ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES",
                               outcomes_inspected=False, canonical_outputs_mutated=False,
                               reason="modeled/proxy not admissible")),
        ("wrong_venue", dict(status="BLOCKED", reason_code="ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES",
                             outcomes_inspected=False, canonical_outputs_mutated=False,
                             reason="venue not hyperliquid")),
    ]

    def _run_audit(self, mod_name, targets, guard_payload):
        mod = importlib.import_module(f"scripts.{mod_name}")
        before = _snap(targets)
        loader_called = {"n": 0}

        def no_loader(*a, **k):
            loader_called["n"] += 1
            raise AssertionError(f"{mod_name} loader called on blocked state")

        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(guard_payload)), \
             redirect_stdout(io.StringIO()) as buf:
            rc = mod.main()
        self.assertEqual(rc, 1, f"{mod_name} must refuse")
        self.assertEqual(loader_called["n"], 0)
        _unchanged(targets, before)
        out = buf.getvalue()
        self.assertIn("BLOCKED", out)
        import re
        m = re.search(r"\{.*\}", out, re.S)
        self.assertIsNotNone(m)
        payload = json.loads(m.group(0))
        self.assertEqual(payload.get("status"), "BLOCKED")
        self.assertFalse(payload.get("canonical_outputs_mutated", True))
        self.assertIn("reason_code", payload)
        importlib.reload(mod)
        return payload

    def test_fclr010_coverage_audit_no_ready_matrix(self):
        targets = [COV_AUDIT, FRONTIER, RUN_MANIFEST, EVAL_FCLR010]
        for label, state in self.STATES:
            with self.subTest(state=label):
                payload = self._run_audit("fclr010_coverage_audit", targets, state)
                self.assertEqual(payload.get("script"), "fclr010_coverage_audit")

    def test_liqmicro_audit_no_ready_matrix(self):
        targets = [LIQ_AUDIT, FRONTIER, RUN_MANIFEST, EVAL_LIQM2]
        for label, state in self.STATES:
            with self.subTest(state=label):
                payload = self._run_audit("liqmicro_audit", targets, state)
                self.assertEqual(payload.get("script"), "liqmicro_audit")


class Test120G4RunLiqmicroV2ReadyPipelineCanonicalSurface(unittest.TestCase):
    """G4: run_liqmicro_v2 _run_pipeline write inventory + blocked isolation +
    sandboxed READY-branch contract (mocked heavy deps, temp dirs)."""

    def test_source_write_inventory_and_no_frontier(self):
        src = (SCRIPTS / "run_liqmicro_v2.py").read_text()
        # inventory every known canonical/research write surface
        self.assertIn("evaluation_summary_FCLR-LIQMICRO-002.md", src)
        self.assertIn('panel_liqmicro_v2.csv', src)
        self.assertIn('panel_liqmicro_v2.parquet', src)
        self.assertIn('descriptive_stats_v2.csv', src)
        self.assertNotIn("experiment_frontier.json", src)
        self.assertNotIn("_write_experiment_frontier", src)
        # pipeline only reachable after READY_FROZEN guard
        self.assertRegex(src, r'if\s+guard\.get\("status"\)\s*!=\s*"READY_FROZEN"[\s\S]*?return\s+1[\s\S]*?_run_pipeline')

    def test_blocked_never_reaches_pipeline(self):
        import scripts.run_liqmicro_v2 as mod

        calls = {"n": 0}

        def fake_pipeline(*a, **k):
            calls["n"] += 1

        before = _snap([FRONTIER, EVAL_LIQM2, RUN_MANIFEST, CROSS])
        with patch.object(mod, "_run_pipeline", fake_pipeline), \
             patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(
                 status="BLOCKED", reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
                 outcomes_inspected=False, canonical_outputs_mutated=False,
                 network=False, writes_real_research_state=False)), \
             redirect_stdout(io.StringIO()):
            rc = mod.main()
        self.assertEqual(rc, 1)
        self.assertEqual(calls["n"], 0)
        _unchanged([FRONTIER, EVAL_LIQM2, RUN_MANIFEST, CROSS], before)

    def test_ready_branch_reaches_pipeline_sandboxed(self):
        import scripts.run_liqmicro_v2 as mod
        import pandas as pd

        before = _snap([FRONTIER, RUN_MANIFEST, CROSS, EVAL_LIQM2])
        reached = {"n": 0, "args": None}

        def sandbox_pipeline(raw_df, hourly, funding_df):
            reached["n"] += 1
            reached["args"] = (raw_df is not None, hourly is not None, funding_df is not None)
            # simulate writes only to a temp dir, never real research_state
            with tempfile.TemporaryDirectory() as td:
                td = Path(td)
                (td / "summary.md").write_text("sandbox")
                (td / "panel.csv").write_text("a,b\n1,2\n")

        ready = {
            "status": "READY_FROZEN",
            "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "outcomes_inspected": True,
            "canonical_outputs_mutated": False,
            "data_loaded_implicitly": False,
            "data_load_mode": "EXPLICIT_LOADER_AFTER_GATES",
            "network": False,
            "writes_real_research_state": False,
            "outcomes_loaded": {
                "raw_df": pd.DataFrame({"x": [1]}),
                "hourly": pd.DataFrame({"symbol": ["BTC"], "hour": ["h"]}),
                "funding_df": pd.DataFrame({"symbol_hl": ["BTC"], "funding_rate": [0.01]}),
            },
        }
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=ready), \
             patch.object(mod, "_run_pipeline", sandbox_pipeline), \
             redirect_stdout(io.StringIO()):
            rc = mod.main()
        self.assertEqual(rc, 0)
        self.assertEqual(reached["n"], 1)
        self.assertEqual(reached["args"], (True, True, True))
        # real frontier/run_manifest/cross-track/eval must remain unchanged
        _unchanged([FRONTIER, RUN_MANIFEST, CROSS, EVAL_LIQM2], before)


class Test120G5H004AllowedPilotSandboxPathEnforcement(unittest.TestCase):
    """G5: if allow flag/env set, pilot write targets must resolve under explicit
    sandbox root or be refused — without running the pilot against real census data."""

    CANONICAL_RS = {FRONTIER, RUN_MANIFEST, EVAL_FCLR010, CROSS}

    def test_allowed_without_sandbox_refused(self):
        import scripts.h004_fclr005_pipeline as mod

        before = _snap(list(self.CANONICAL_RS))
        old_argv = sys.argv[:]
        old_env = os.environ.get(mod.H004_SANDBOX_ROOT_ENV)
        try:
            os.environ.pop(mod.H004_SANDBOX_ROOT_ENV, None)
            sys.argv = ["h004_fclr005_pipeline.py", mod.H004_ALLOW_FLAG]
            with redirect_stdout(io.StringIO()) as buf:
                rc = mod.main()
            self.assertEqual(rc, 1)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload.get("reason_code"), "H004_ALLOWED_MODE_REQUIRES_SANDBOX_ROOT")
            self.assertFalse(payload.get("canonical_outputs_mutated"))
        finally:
            sys.argv = old_argv
            if old_env is None:
                os.environ.pop(mod.H004_SANDBOX_ROOT_ENV, None)
            else:
                os.environ[mod.H004_SANDBOX_ROOT_ENV] = old_env
        _unchanged(list(self.CANONICAL_RS), before)

    def test_allowed_with_non_sandbox_real_rs_refused(self):
        import scripts.h004_fclr005_pipeline as mod

        before = _snap(list(self.CANONICAL_RS))
        old_argv = sys.argv[:]
        old_env = os.environ.get(mod.H004_SANDBOX_ROOT_ENV)
        try:
            # point sandbox at real research_state-like path => must refuse
            os.environ[mod.H004_SANDBOX_ROOT_ENV] = str(RS)
            sys.argv = ["h004_fclr005_pipeline.py", mod.H004_ALLOW_FLAG]
            with redirect_stdout(io.StringIO()) as buf:
                rc = mod.main()
            self.assertEqual(rc, 1)
            payload = json.loads(buf.getvalue())
            self.assertIn(payload.get("reason_code"), ("H004_ALLOWED_MODE_REQUIRES_SANDBOX_ROOT", "H004_ALLOWED_SANDBOX_TARGETS_REAL_RS"))
            self.assertFalse(payload.get("canonical_outputs_mutated"))
        finally:
            sys.argv = old_argv
            if old_env is None:
                os.environ.pop(mod.H004_SANDBOX_ROOT_ENV, None)
            else:
                os.environ[mod.H004_SANDBOX_ROOT_ENV] = old_env
        _unchanged(list(self.CANONICAL_RS), before)

    def test_resolve_pilot_targets_sandboxed(self):
        import scripts.h004_fclr005_pipeline as mod

        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            targets = mod.resolve_h004_pilot_targets(sandbox_root=td)
            for name, p in targets.items():
                self.assertTrue(str(p).startswith(str(td.resolve())), f"{name} not in sandbox: {p}")
            self.assertNotIn(str(RS.resolve()), str(targets["out_sum"]))
            self.assertNotIn(str(RS.resolve()), str(targets["liq_enum"]))

    def test_default_refused_still_stable(self):
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
