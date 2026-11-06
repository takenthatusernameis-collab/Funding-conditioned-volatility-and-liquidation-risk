"""FCLR-NEXT-119: READY_FROZEN end-to-end testability (no real outcomes) +
h004 allowed-path pilot artifact boundary + repo-local scope-registry drift
enforcement + run_liqmicro_v2 no-frontier-mutation surface + experiment_frontier
mutation audit.

Deterministic, tmp-isolated, no network, no real parquet/outcome reads,
no real research_state writes. Closes exact uncovered gaps left by FCLR-NEXT-118.
"""
from __future__ import annotations

import importlib
import io
import json
import os
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.fclr010_guarded_entry import guarded_execute, refusal_payload
from scripts.fclr010_harness import FCLR010Harness

REAL = Path(__file__).resolve().parent.parent
SCRIPTS = REAL / "scripts"
RS = REAL / "research_state"
REGISTRY_PATH = RS / "tracka_script_scope_registry.json"
FRONTIER = RS / "experiment_frontier.json"
RUN_MANIFEST = RS / "run_manifest.json"
CROSS_TRACK = RS / "cross_track_decision_log.md"

CANONICAL_TARGETS = [
    FRONTIER,
    RUN_MANIFEST,
    RS / "evaluation_summary_FCLR010.md",
    RS / "evaluation_summary_FCLR-LIQMICRO-002.md",
    CROSS_TRACK,
]


def _snap(paths):
    return {str(p): (p.read_bytes() if p.exists() else None) for p in paths}


def _assert_unchanged(paths, before):
    for s, b in before.items():
        p = Path(s)
        a = p.read_bytes() if p.exists() else None
        assert b == a, f"canonical target mutated: {s}"


def _strict_go_manifest():
    # Machine-verifiable manifest shape accepted by strict rubric (observed Hyperliquid GO).
    return {
        "venue": "hyperliquid",
        "label_type": "observed",
        "observed_vs_modeled": "observed",
        "source_family": "hyperliquid_ironflow",
        "coverage": {"symbols_n": 5, "days": 120, "blocks_30d": 4},
        "provenance": {"source": "ironflow", "auth": "unauthenticated", "verified": True},
        "machine_verifiable": True,
    }


class Test119G1ReadyFrozenEndToEnd(unittest.TestCase):
    """G1: READY_FROZEN reached only via guarded_execute/harness READY_FROZEN
    (source order + branch-order asserted), and no canonical summary/manifest/
    frontier mutation occurs when trigger absent (no real outcome data/network)."""

    def test_ready_frozen_via_guarded_execute_explicit_loader_only(self):
        # Preconditions: prereg exists + strict GO manifest + admissible seam GO + data path exists.
        calls = {"n": 0, "args": None}

        def loader(dp, ctx=None):
            calls["n"] += 1
            calls["args"] = (str(dp), ctx)
            return {"synthetic_outcome_rows": 3}

        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            pre = td / "prereg.json"
            pre.write_text(json.dumps({"status": "PREREGISTERED"}))
            data = td / "data"
            data.mkdir()
            # Minimal seam manifest: seam check is manifest-only; we supply a manifest
            # that the seam may accept or refuse — but to exercise READY_FROZEN end-to-end
            # we need all gates to pass. Use harness directly with a permissive path:
            # evaluate_forward requires (1) prereg exists (done), (2) if source_manifest
            # strict GO, (3) admissible seam if provided not NO-GO, (4) data exists.
            # A missing seam manifest means seam=None (legacy behavior preserved) => OK.
            res = guarded_execute(
                data_path=data,
                pre_reg_path=pre,
                repo_root=REAL,
                source_manifest=None,
                admissible_manifest=None,
                outcome_loader=loader,
                loader_context={"split": "frozen"},
                allow_default_loader=False,
            )
        self.assertEqual(res.get("status"), "READY_FROZEN", res)
        self.assertEqual(calls["n"], 1, "explicit loader must be invoked exactly once on READY_FROZEN")
        self.assertEqual(res.get("data_loaded_implicitly"), False)
        self.assertEqual(res.get("data_load_mode"), "EXPLICIT_LOADER_AFTER_GATES")
        self.assertFalse(res.get("canonical_outputs_mutated"))
        self.assertFalse(res.get("network"))
        self.assertFalse(res.get("writes_real_research_state"))
        self.assertIn("guarded_execution_contract", res)

    def test_blocked_branch_never_calls_loader_and_no_canonical_mutation(self):
        before = _snap(CANONICAL_TARGETS)

        def must_not_call(*a, **k):
            raise AssertionError("loader must not be called on blocked branch")

        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            res = guarded_execute(
                data_path=td / "missing_data",
                pre_reg_path=None,  # blocked: prereg required
                repo_root=REAL,
                outcome_loader=must_not_call,
                allow_default_loader=False,
            )
        self.assertEqual(res.get("status"), "BLOCKED")
        self.assertFalse(res.get("outcomes_inspected"))
        self.assertFalse(res.get("canonical_outputs_mutated"))
        self.assertIn(res.get("reason_code"), ("PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS", "PREREG_REQUIRED_BEFORE_DATA_LOAD"))
        _assert_unchanged(CANONICAL_TARGETS, before)

    def test_ready_frozen_branch_order_source_invariant(self):
        src = (REAL / "scripts" / "fclr010_harness.py").read_text()
        ge = (REAL / "scripts" / "fclr010_guarded_entry.py").read_text()
        # evaluate_forward does pre-check with outcome_loader=None then only READY_FROZEN proceeds.
        self.assertRegex(src, r"res\s*=\s*self\.evaluate_forward\([\s\S]*?outcome_loader\s*=\s*None")
        self.assertRegex(src, r'if\s+res\.get\("status"\)\s*!=\s*"READY_FROZEN"')
        self.assertIn("data_loaded_implicitly", src)
        self.assertIn("EXPLICIT_LOADER_AFTER_GATES", src)
        self.assertIn("guarded_execution_contract", ge)
        # execute_ready_data_load explicit loader only after gates.
        idx_gate = src.index('if res.get("status") != "READY_FROZEN"')
        idx_load = src.index("res[\"outcomes_loaded\"] = outcome_loader(Path(data_path))")
        self.assertLess(idx_gate, idx_load)


class Test119G2H004AllowedPathBoundary(unittest.TestCase):
    """G2: h004 allowed path writes target only non-canonical pilot artifacts and
    cannot touch Hyperliquid Track A canonical targets/frontier/run_manifest/
    cross-track liquidation gate fields; no FCLR010Harness/fclr010_guarded_entry
    invocation from allowed path."""

    def test_default_refused_no_canonical_mutation(self):
        import scripts.h004_fclr005_pipeline as mod
        before = _snap([FRONTIER, RUN_MANIFEST, RS / "evaluation_summary_FCLR010.md", CROSS_TRACK])
        old = sys.argv[:]
        try:
            sys.argv = ["h004_fclr005_pipeline.py"]
            with redirect_stdout(io.StringIO()) as buf:
                rc = mod.main()
            self.assertEqual(rc, 1)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload.get("reason_code"), "H004_OUT_OF_SCOPE_HISTORICAL_TRACKA_PILOT")
            self.assertFalse(payload.get("hyperliquid_fclr010_guarded_seam"))
            self.assertFalse(payload.get("canonical_outputs_mutated"))
        finally:
            sys.argv = old
        _assert_unchanged([FRONTIER, RUN_MANIFEST, RS / "evaluation_summary_FCLR010.md", CROSS_TRACK], before)

    def test_allowed_path_guard_refuses_if_seam_flag_flipped(self):
        import scripts.h004_fclr005_pipeline as mod
        before = _snap([FRONTIER, RUN_MANIFEST, RS / "evaluation_summary_FCLR010.md", CROSS_TRACK])
        old = sys.argv[:]
        old_flag = mod.H004_HYPERLIQUID_FCLR010_GUARDED_SEAM
        try:
            mod.H004_HYPERLIQUID_FCLR010_GUARDED_SEAM = True
            sys.argv = ["h004_fclr005_pipeline.py", mod.H004_ALLOW_FLAG]
            with redirect_stdout(io.StringIO()) as buf:
                rc = mod.main()
            self.assertEqual(rc, 1)
            payload = json.loads(buf.getvalue())
            self.assertIn("H004", payload.get("reason_code", "") + payload.get("reason", ""))
        finally:
            mod.H004_HYPERLIQUID_FCLR010_GUARDED_SEAM = old_flag
            sys.argv = old
        _assert_unchanged([FRONTIER, RUN_MANIFEST, RS / "evaluation_summary_FCLR010.md", CROSS_TRACK], before)

    def test_no_fclr010_guarded_invocation_tokens_in_h004(self):
        src = (SCRIPTS / "h004_fclr005_pipeline.py").read_text()
        self.assertNotIn("FCLR010Harness", src)
        self.assertNotIn("fclr010_guarded_entry", src)
        self.assertNotIn("from scripts.fclr010_harness", src)
        self.assertNotIn("guarded_execute(", src)
        # Allowed pilot artifacts are its own, not Hyperliquid Track A canonical targets.
        self.assertIn("evaluation_summary_FCLR005.md", src)
        self.assertIn("H004_HYPERLIQUID_FCLR010_GUARDED_SEAM", src)

    def test_canonical_target_quarantine_declaration(self):
        import scripts.h004_fclr005_pipeline as mod
        targets = getattr(mod, "H004_HYPERLIQUID_CANONICAL_TARGETS", ())
        self.assertIn("experiment_frontier.json", targets)
        self.assertIn("run_manifest.json", targets)
        self.assertIn("evaluation_summary_FCLR010.md", targets)
        self.assertIn("cross_track_decision_log.md", targets)


class Test119G3ScopeRegistryDriftEnforcement(unittest.TestCase):
    """G3: repo-local drift check fails on scripts/*.py additions/removals not
    reflected in tracka_script_scope_registry.json (and reconciled with 117)."""

    def test_drift_check_passes_current_repo(self):
        from scripts.check_tracka_scope_registry_drift import check_drift
        res = check_drift(REAL)
        self.assertTrue(res.get("pass"), res)
        self.assertEqual(res.get("reason_code"), "OK")
        self.assertEqual(res.get("missing_in_registry"), [])
        self.assertEqual(res.get("extra_in_registry"), [])

    def test_drift_check_detects_missing_script(self):
        from scripts.check_tracka_scope_registry_drift import check_drift
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "scripts").mkdir()
            (td / "research_state").mkdir()
            (td / "scripts" / "real.py").write_text("# x\n")
            (td / "scripts" / "extra.py").write_text("# y\n")
            (td / "research_state" / "tracka_script_scope_registry.json").write_text(json.dumps({
                "allowed_classes": ["repo_maintenance_utility"],
                "scripts": {"real.py": {"class": "repo_maintenance_utility", "reason": "ok reason long enough"}},
            }))
            res = check_drift(td)
        self.assertFalse(res.get("pass"))
        self.assertEqual(res.get("reason_code"), "SCOPE_REGISTRY_DRIFT")
        self.assertIn("extra.py", res.get("missing_in_registry", []))

    def test_drift_check_detects_extra_registry_entry(self):
        from scripts.check_tracka_scope_registry_drift import check_drift
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "scripts").mkdir()
            (td / "research_state").mkdir()
            (td / "scripts" / "real.py").write_text("# x\n")
            (td / "research_state" / "tracka_script_scope_registry.json").write_text(json.dumps({
                "allowed_classes": ["repo_maintenance_utility"],
                "scripts": {
                    "real.py": {"class": "repo_maintenance_utility", "reason": "ok reason long enough"},
                    "gone.py": {"class": "repo_maintenance_utility", "reason": "ok reason long enough"},
                },
            }))
            res = check_drift(td)
        self.assertFalse(res.get("pass"))
        self.assertIn("gone.py", res.get("extra_in_registry", []))

    def test_registry_reconciled_with_117(self):
        from tests.test_tracka_hardening_117 import SCRIPT_REGISTRY
        reg = json.loads(REGISTRY_PATH.read_text())["scripts"]
        self.assertEqual(set(reg.keys()), set(SCRIPT_REGISTRY.keys()))
        self.assertEqual(len(reg), len(SCRIPT_REGISTRY))


class Test119G4RunLiqmicroV2NoFrontierMutation(unittest.TestCase):
    """G4: run_liqmicro_v2 never mutates experiment_frontier.json under any state;
    blocked path performs no canonical mutation and no loader call."""

    def test_blocked_no_frontier_or_canonical_mutation(self):
        import scripts.run_liqmicro_v2 as mod
        targets = [FRONTIER, RS / "evaluation_summary_FCLR-LIQMICRO-002.md", RUN_MANIFEST, CROSS_TRACK]
        before = _snap(targets)
        pipeline_called = {"n": 0}

        def fake_pipeline(*a, **k):
            pipeline_called["n"] += 1

        with patch.object(mod, "_run_pipeline", fake_pipeline), \
             patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(
                 status="BLOCKED", reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
                 outcomes_inspected=False, canonical_outputs_mutated=False)), \
             redirect_stdout(io.StringIO()):
            rc = mod.main()
        self.assertEqual(rc, 1)
        self.assertEqual(pipeline_called["n"], 0)
        _assert_unchanged(targets, before)

    def test_source_has_no_experiment_frontier_write(self):
        src = (SCRIPTS / "run_liqmicro_v2.py").read_text()
        self.assertNotIn("experiment_frontier.json", src)
        self.assertNotIn("_write_experiment_frontier", src)
        # Uses guarded_execute
        self.assertIn("guarded_execute", src)
        self.assertIn("_run_pipeline", src)
        # Pipeline only called after READY_FROZEN guard in main source order.
        self.assertRegex(src, r'if\s+guard\.get\("status"\)\s*!=\s*"READY_FROZEN"[\s\S]*?return\s+1[\s\S]*?_run_pipeline')


class Test119G5ExperimentFrontierMutationAudit(unittest.TestCase):
    """G5: blocked main() of run_liqmicro_v2 + all guarded_tracka_ready_writing
    scripts never mutate experiment_frontier.json (snapshot before/after)."""

    BLOCKED = {
        "status": "BLOCKED",
        "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
        "outcomes_inspected": False,
        "canonical_outputs_mutated": False,
        "network": False,
        "writes_real_research_state": False,
        "guarded_execution_contract": "fclr_next_111",
    }

    def test_run_liqmicro_v2_frontier_unchanged(self):
        import scripts.run_liqmicro_v2 as mod
        before = _snap([FRONTIER])
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(self.BLOCKED)), \
             redirect_stdout(io.StringIO()):
            mod.main()
        _assert_unchanged([FRONTIER], before)

    def test_all_guarded_ready_writing_frontier_unchanged_on_block(self):
        reg = json.loads(REGISTRY_PATH.read_text())["scripts"]
        writers = sorted(k for k, v in reg.items() if v["class"] == "guarded_tracka_ready_writing")
        # coupled/overlay scripts mutate frontier on READY by design; blocked must not.
        for name in writers:
            mod = importlib.import_module(f"scripts.{name[:-3]}")
            before = _snap([FRONTIER])
            with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=dict(self.BLOCKED)), \
                 redirect_stdout(io.StringIO()):
                rc = mod.main()
            self.assertEqual(rc, 1, f"{name} must refuse blocked")
            _assert_unchanged([FRONTIER], before)
            importlib.reload(mod)


if __name__ == "__main__":
    unittest.main()
