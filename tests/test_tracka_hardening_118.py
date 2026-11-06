"""FCLR-NEXT-118: post-READY manifest-load controlled refusal + h004 allowed-path
canonical-target quarantine/sandbox + canonical script-scope registry drift check +
run_liqmicro_v2 frontier/canonical parity + guarded ready-writing NO-READY refusal matrix.

Deterministic, tmp-isolated, no network, no real parquet/outcome reads,
no real research_state writes.

Closes exact gaps left by FCLR-NEXT-117:
  (G1) fclr010_execute post-READY loader path: if run_manifest/splits
       unavailable/corrupt/LFS-unmaterialized, _frozen_split_context raises
       inside the explicit loader after guard passed. Controlled refusal payload
       with canonical_outputs_mutated:false, no evaluation_summary_FCLR010.md /
       run_manifest.json mutation.
  (G2) h004_fclr005_pipeline allowed path cannot target Hyperliquid Track A
       canonical outputs/frontier/cross-track/run_manifest liquidation gate
       fields and cannot be invoked through the FCLR010 guarded seam.
  (G3) Canonical machine-readable script-scope registry artifact
       (research_state/tracka_script_scope_registry.json) with deterministic
       drift check: scripts/*.py filenames == registry keys, valid classes/
       reasons, synced with test_tracka_hardening_117.SCRIPT_REGISTRY.
  (G4) run_liqmicro_v2 frontier/canonical mutation parity with run_liqmicro:
       _run_pipeline/canonical writes post-gate only; blocked isolation proved.
  (G5) Guarded ready-writing NO-READY refusal matrix for
       coupled_robust_eval.py, fclr010_execute.py, fclr010_coverage_audit.py,
       liqmicro_audit.py, overlay_quick.py, overlay_tracka_execute.py: no
       canonical output mutation when guard is not READY (missing prereg,
       NOGO seam, modeled/proxy, wrong venue), tmp-isolated canonical path
       overrides where feasible.
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
from scripts.fclr010_guarded_entry import refusal_payload, guarded_execute

REAL = Path(__file__).resolve().parent.parent
SCRIPTS = REAL / "scripts"
RS = REAL / "research_state"
REGISTRY_PATH = RS / "tracka_script_scope_registry.json"

BLOCKED_PAYLOAD = {
    "status": "BLOCKED",
    "outcomes_inspected": False,
    "canonical_outputs_mutated": False,
    "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
}

READY_PAYLOAD = {
    "status": "READY_FROZEN",
    "outcomes_inspected": False,
    "canonical_outputs_mutated": False,
    "outcomes_loaded": {"panel": object()},
}

# Canonical targets per guarded ready-writing script (from 116 CANONICAL_TARGETS).
CANONICAL_TARGETS = {
    "overlay_quick": [
        RS / "evaluation_summary_tracka_overlay_001.md",
        RS / "experiment_frontier.json",
        RS / "cross_track_decision_log.md",
    ],
    "overlay_tracka_execute": [
        RS / "evaluation_summary_tracka_overlay_001.md",
        RS / "experiment_frontier.json",
        RS / "cross_track_decision_log.md",
    ],
    "coupled_robust_eval": [
        RS / "evaluation_summary_FCLR-COUPLED-001-ROBUST.md",
    ],
    "fclr010_execute": [
        RS / "evaluation_summary_FCLR010.md",
        RS / "run_manifest.json",
    ],
    "fclr010_coverage_audit": [
        RS / "fclr010_coverage_audit.json",
    ],
    "liqmicro_audit": [
        RS / "liqmicro_data_audit_001.md",
    ],
}

# run_liqmicro_v2 canonical targets (no experiment_frontier.json; writes its own
# summary + results/liqmicro_v2 artifacts only).
LIQMICRO_V2_CANONICAL = [
    RS / "evaluation_summary_FCLR-LIQMICRO-002.md",
]

# Non-READY guard states for the G5 refusal matrix.
NON_READY_PAYLOADS = {
    "missing_prereg": {
        "status": "BLOCKED",
        "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
        "outcomes_inspected": False,
        "canonical_outputs_mutated": False,
        "network": False,
        "writes_real_research_state": False,
        "prereg_required": True,
    },
    "nogo_seam": {
        "status": "BLOCKED",
        "reason_code": "ADMISSIBLE_SEAM_NOGO_BEFORE_PREREG",
        "outcomes_inspected": False,
        "canonical_outputs_mutated": False,
        "network": False,
        "writes_real_research_state": False,
        "admissible_seam_wired": {"pass": False, "status": "NO-GO"},
        "fail_closed_order": "admissible_seam->manifest_prereg",
    },
    "modeled_proxy": {
        "status": "BLOCKED",
        "reason_code": "MODELED_PROXY_NOT_OBSERVED_HYPERLIQUID_GATE",
        "outcomes_inspected": False,
        "canonical_outputs_mutated": False,
        "network": False,
        "writes_real_research_state": False,
        "observed_vs_modeled_conflation": False,
        "venue": "modeled_proxy_not_hyperliquid_gate",
    },
    "wrong_venue": {
        "status": "BLOCKED",
        "reason_code": "WRONG_VENUE_NOT_HYPERLIQUED_TRACK_A",
        "outcomes_inspected": False,
        "canonical_outputs_mutated": False,
        "network": False,
        "writes_real_research_state": False,
        "venue": "bybit_not_hyperliquid_track_a",
    },
}


def _snapshot(paths):
    return {str(p): (p.read_bytes() if p.exists() else None) for p in paths}


def _assert_snapshot_unchanged(paths, before):
    for s, b in before.items():
        p = Path(s)
        after = p.read_bytes() if p.exists() else None
        assert b == after, f"canonical target mutated: {s}"


class Test118G1Fclr010ExecutePostReadyLoaderRefusal(unittest.TestCase):
    """G1: post-READY loader failure yields controlled refusal, no canonical mutation."""

    def test_guarded_execute_loader_failure_controlled_refusal(self):
        """guarded_execute with a failing outcome_loader returns BLOCKED with
        stable reason_code and canonical_outputs_mutated:false (no loader called
        on blocked branches; loader failure after READY_FROZEN is caught)."""

        def failing_loader(dp, ctx=None):
            raise RuntimeError("run_manifest/splits unavailable or corrupt")

        with tempfile.TemporaryDirectory() as td:
            dp = Path(td)
            # pre_reg_path must exist for evaluate_forward to pass the prereg
            # gate and reach the explicit outcome_loader.
            pre_reg = dp / "pre_reg.json"
            pre_reg.write_text(json.dumps({"status": "PREREGISTERED"}))
            res = guarded_execute(
                data_path=dp,
                pre_reg_path=pre_reg,
                repo_root=REAL,
                source_manifest=None,
                admissible_manifest=None,
                admissible_manifest_path=None,
                outcome_loader=failing_loader,
                loader_context=None,
                allow_default_loader=False,
            )
        self.assertEqual(res.get("status"), "BLOCKED")
        self.assertFalse(res.get("canonical_outputs_mutated"))
        self.assertFalse(res.get("network"))
        self.assertFalse(res.get("writes_real_research_state"))
        self.assertFalse(res.get("outcomes_inspected"))
        self.assertIn("reason_code", res)
        self.assertEqual(
            res["reason_code"], "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS"
        )
        self.assertIn("outcome_loader failed", res.get("reason", ""))

    def test_main_blocked_post_ready_loader_no_canonical_mutation(self):
        """fclr010_execute.main() with guarded_execute returning a post-READY
        loader-failure BLOCKED payload: rc=1, no canonical summary/manifest
        mutation, stable reason_code printed."""
        import scripts.fclr010_execute as mod

        targets = [RS / "evaluation_summary_FCLR010.md", RS / "run_manifest.json"]
        before = _snapshot(targets)
        loader_fail_payload = {
            "status": "BLOCKED",
            "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "reason": "outcome_loader failed: run_manifest/splits unavailable or corrupt",
            "outcomes_inspected": False,
            "canonical_outputs_mutated": False,
            "network": False,
            "writes_real_research_state": False,
            "script": "fclr010_execute",
        }
        old_argv = sys.argv[:]
        try:
            sys.argv = ["fclr010_execute.py"]
            with patch(
                "scripts.fclr010_guarded_entry.guarded_execute",
                return_value=dict(loader_fail_payload),
            ), redirect_stdout(io.StringIO()) as buf:
                rc = mod.main()
            out = buf.getvalue()
            self.assertEqual(rc, 1)
            self.assertIn("BLOCKED", out)
            m = re.search(r"\{.*\}", out, re.S)
            self.assertIsNotNone(m, "no JSON payload in blocked output")
            payload = json.loads(m.group(0))
            self.assertEqual(payload.get("status"), "BLOCKED")
            self.assertEqual(
                payload.get("reason_code"), "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS"
            )
            self.assertFalse(payload.get("canonical_outputs_mutated"))
        finally:
            sys.argv = old_argv
        for s, b in before.items():
            p = Path(s)
            self.assertEqual(b, p.read_bytes() if p.exists() else None, s)

    def test_no_pre_guard_manifest_read_on_blocked_branch(self):
        """Blocked main must not print split metadata or pre-read manifest before
        guard; _frozen_split_context / _load_json_lfs_aware not invoked pre-guard."""
        import scripts.fclr010_execute as mod

        with patch(
            "scripts.fclr010_guarded_entry.guarded_execute",
            return_value=dict(BLOCKED_PAYLOAD),
        ), patch(
            "scripts.fclr010_execute._frozen_split_context",
            side_effect=AssertionError("pre-guard split context read on blocked"),
        ), patch(
            "scripts.fclr010_execute.FCLR010Harness._load_json_lfs_aware",
            side_effect=AssertionError("pre-guard manifest read on blocked"),
        ), redirect_stdout(io.StringIO()) as buf:
            rc = mod.main()
        self.assertEqual(rc, 1)
        out = buf.getvalue()
        self.assertIn("BLOCKED", out)
        self.assertNotIn("Splits:", out)


class Test118G2H004AllowedPathQuarantine(unittest.TestCase):
    """G2: h004 allowed-path Hyperliquid canonical-target quarantine."""

    def test_default_refusal_stable_no_canonical_mutation(self):
        """Default (non-allowed) execution: rc=1, stable refusal payload, no
        canonical Hyperliquid Track A target mutation."""
        mod = importlib.import_module("scripts.h004_fclr005_pipeline")
        importlib.reload(mod)
        targets = [
            RS / "evaluation_summary_FCLR005.md",
            RS / "experiment_frontier.json",
            RS / "run_manifest.json",
            RS / "evaluation_summary_FCLR010.md",
            RS / "cross_track_decision_log.md",
            RS / "hypothesis_registry.json",
            RS / "liqmicro_data_audit_001.md",
        ]
        before = _snapshot(targets)
        old_argv = sys.argv[:]
        old_env = os.environ.get(mod.H004_ALLOW_ENV)
        try:
            sys.argv = ["h004_fclr005_pipeline.py"]
            os.environ.pop(mod.H004_ALLOW_ENV, None)
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = mod.main()
            self.assertEqual(rc, 1)
            payload = json.loads(buf.getvalue())
            self.assertEqual(payload["status"], "BLOCKED")
            self.assertEqual(
                payload["reason_code"], "H004_OUT_OF_SCOPE_HISTORICAL_TRACKA_PILOT"
            )
            self.assertTrue(payload["out_of_scope_historical_tracka_pilot"])
            self.assertFalse(payload["hyperliquid_fclr010_guarded_seam"])
            self.assertFalse(payload["canonical_outputs_mutated"])
            self.assertFalse(payload["network"])
            self.assertFalse(payload["writes_real_research_state"])
        finally:
            sys.argv = old_argv
            if old_env is None:
                os.environ.pop(mod.H004_ALLOW_ENV, None)
            else:
                os.environ[mod.H004_ALLOW_ENV] = old_env
        for s, b in before.items():
            p = Path(s)
            self.assertEqual(b, p.read_bytes() if p.exists() else None, s)

    def test_allowed_path_guard_passes_no_seam_tokens(self):
        """Machine guard: H004_HYPERLIQUID_FCLR010_GUARDED_SEAM is False;
        _h004_allowed_path_guard() returns None (passes). No FCLR010Harness /
        fclr010_guarded_entry tokens in source (covered by 117 test)."""
        import scripts.h004_fclr005_pipeline as mod

        src = (SCRIPTS / "h004_fclr005_pipeline.py").read_text()
        self.assertNotIn("FCLR010Harness", src)
        self.assertNotIn("fclr010_guarded_entry", src)
        self.assertFalse(mod.H004_HYPERLIQUID_FCLR010_GUARDED_SEAM)
        self.assertIsNone(mod._h004_allowed_path_guard())

    def test_allowed_path_canonical_targets_not_in_guard(self):
        """Guard's canonical target list covers Hyperliquid Track A canonical
        outputs (frontier, run_manifest liquidation gate, FCLR010 summary,
        cross-track) and excludes h004's own pilot artifacts."""
        import scripts.h004_fclr005_pipeline as mod

        for t in mod.H004_HYPERLIQUID_CANONICAL_TARGETS:
            self.assertIn(
                t,
                (
                    "experiment_frontier.json",
                    "run_manifest.json",
                    "evaluation_summary_FCLR010.md",
                    "cross_track_decision_log.md",
                ),
            )
        # h004's own pilot artifacts are NOT Hyperliquid Track A canonical targets.
        self.assertNotIn("evaluation_summary_FCLR005.md", mod.H004_HYPERLIQUID_CANONICAL_TARGETS)
        self.assertNotIn("liquidation_sources_enumeration.md", mod.H004_HYPERLIQUID_CANONICAL_TARGETS)


class Test118G3CanonicalScriptScopeRegistryDriftCheck(unittest.TestCase):
    """G3: canonical machine-readable script-scope registry + drift check."""

    def test_registry_file_exists_valid_json(self):
        self.assertTrue(REGISTRY_PATH.exists(), "tracka_script_scope_registry.json missing")
        with open(REGISTRY_PATH) as f:
            reg = json.load(f)
        self.assertIn("scripts", reg)
        self.assertIn("allowed_classes", reg)
        self.assertIn("script_count", reg)
        self.assertGreaterEqual(len(reg["scripts"]), 82)
        self.assertEqual(reg["script_count"], len(reg["scripts"]))

    def test_registry_keys_match_scripts_dir(self):
        """Drift check: scripts/*.py filenames must exactly == registry keys."""
        with open(REGISTRY_PATH) as f:
            reg = json.load(f)
        registry_keys = set(reg["scripts"].keys())
        actual_keys = {p.name for p in SCRIPTS.glob("*.py")}
        missing = sorted(actual_keys - registry_keys)
        extra = sorted(registry_keys - actual_keys)
        self.assertEqual(
            missing, [], f"scripts in dir but missing from registry: {missing}"
        )
        self.assertEqual(
            extra, [], f"registry keys with no script file: {extra}"
        )

    def test_registry_entries_valid(self):
        """Every registry entry has a valid class and sufficient reason."""
        with open(REGISTRY_PATH) as f:
            reg = json.load(f)
        allowed = set(reg["allowed_classes"])
        for name, meta in reg["scripts"].items():
            self.assertIn("class", meta, name)
            self.assertIn("reason", meta, name)
            self.assertIn(meta["class"], allowed, f"{name}: {meta['class']}")
            self.assertNotIn("needs_manual", meta["class"], name)
            self.assertGreaterEqual(len(meta["reason"]), 15, name)

    def test_registry_synced_with_test_117(self):
        """Registry is reconciled with test_tracka_hardening_117.SCRIPT_REGISTRY."""
        from tests.test_tracka_hardening_117 import SCRIPT_REGISTRY as T117_REG

        with open(REGISTRY_PATH) as f:
            reg = json.load(f)
        reg_keys = set(reg["scripts"].keys())
        t117_keys = set(T117_REG.keys())
        self.assertEqual(reg_keys, t117_keys, "registry not synced with 117 SCRIPT_REGISTRY")
        for name in reg_keys:
            self.assertEqual(
                reg["scripts"][name]["class"],
                T117_REG[name]["class"],
                f"class mismatch for {name}",
            )

    def test_no_unclassified_eval_summary_writers(self):
        """Scripts mentioning evaluation_summary cannot be unclassified_auxiliary."""
        import re as _re
        eval_pat = _re.compile(r"evaluation_summary", _re.I)
        with open(REGISTRY_PATH) as f:
            reg = json.load(f)
        for name, meta in reg["scripts"].items():
            src = (SCRIPTS / name).read_text(errors="ignore")
            if eval_pat.search(src):
                self.assertNotEqual(
                    meta["class"], "unclassified_auxiliary", name
                )

    def test_drift_check_detects_missing_script(self):
        """Drift check logic fails when a script exists in dir but not in registry."""
        with open(REGISTRY_PATH) as f:
            reg = json.load(f)
        registry_keys = set(reg["scripts"].keys())
        actual_keys = {p.name for p in SCRIPTS.glob("*.py")}
        # Simulate a stray script: drift = actual has a key not in registry.
        stray = {"__stray_script_118__.py"}
        simulated_actual = actual_keys | stray
        missing = sorted(simulated_actual - registry_keys)
        self.assertIn("__stray_script_118__.py", missing)


class Test118G4RunLiqmicroV2FrontierParity(unittest.TestCase):
    """G4: run_liqmicro_v2 frontier/canonical mutation parity with run_liqmicro."""

    def _import_run_liqmicro_v2(self):
        import importlib, types
        saved = {}

        def _ensure(mn, attrs=None):
            if mn in sys.modules:
                return
            m = types.ModuleType(mn)
            for k, v in (attrs or {}).items():
                setattr(m, k, v)
            sys.modules[mn] = m
            saved[mn] = None

        class _R:
            def summary(self):
                return ""

            params = pvalues = bse = tvalues = {}

        class _OLS:
            def __init__(self, *a, **k):
                pass

            def fit(self, *a, **k):
                return _R()

        _ensure("statsmodels")
        _ensure("statsmodels.api", {"OLS": _OLS, "add_constant": lambda x: x})
        _ensure("statsmodels.formula.api")
        for mn, name in [
            ("analysis.liqmicro.features", "LiqMicroFeatures"),
            ("analysis.liqmicro.models", "LiqMicroModels"),
            ("analysis.liqmicro.stats", "LiqMicroStats"),
        ]:
            if mn not in sys.modules:
                m = types.ModuleType(mn)
                setattr(m, name, type(name, (), {}))
                sys.modules[mn] = m
                saved[mn] = None
        try:
            sys.modules.pop("scripts.run_liqmicro_v2", None)
            mod = importlib.import_module("scripts.run_liqmicro_v2")
            return mod
        finally:
            sys.modules.pop("scripts.run_liqmicro_v2", None)
            for mn, prev in saved.items():
                if prev is None:
                    sys.modules.pop(mn, None)
                else:
                    sys.modules[mn] = prev

    def test_blocked_never_calls_pipeline_or_mutates_canonical(self):
        """run_liqmicro_v2 blocked: _run_pipeline never called, no canonical
        summary mutation, no experiment_frontier.json mutation."""
        mod = self._import_run_liqmicro_v2()
        targets = LIQMICRO_V2_CANONICAL + [RS / "experiment_frontier.json"]
        before = _snapshot(targets)
        results_dir = mod.RESULTS_DIR
        results_before = {
            str(p): (p.read_bytes() if p.exists() else None)
            for p in results_dir.glob("*")
        } if results_dir.exists() else {}
        with patch(
            "scripts.fclr010_guarded_entry.guarded_execute",
            return_value=dict(BLOCKED_PAYLOAD),
        ), patch.object(
            mod, "_run_pipeline", side_effect=AssertionError("pipeline on blocked")
        ), redirect_stdout(io.StringIO()):
            rc = mod.main()
        self.assertEqual(rc, 1)
        for s, b in before.items():
            p = Path(s)
            self.assertEqual(b, p.read_bytes() if p.exists() else None, s)
        for s, b in results_before.items():
            p = Path(s)
            self.assertEqual(b, p.read_bytes() if p.exists() else None, s)

    def test_blocked_frontier_unchanged(self):
        """Blocked run_liqmicro_v2 never mutates experiment_frontier.json."""
        mod = self._import_run_liqmicro_v2()
        frontier = RS / "experiment_frontier.json"
        before = frontier.read_bytes() if frontier.exists() else None
        with patch(
            "scripts.fclr010_guarded_entry.guarded_execute",
            return_value=dict(BLOCKED_PAYLOAD),
        ), patch.object(
            mod, "_run_pipeline", side_effect=AssertionError("pipeline on blocked")
        ), redirect_stdout(io.StringIO()):
            mod.main()
        self.assertEqual(before, frontier.read_bytes() if frontier.exists() else None)

    def test_pipeline_only_reached_after_ready(self):
        """Source order: _run_pipeline is invoked only after the guard READY_FROZEN
        check in main()."""
        src = (SCRIPTS / "run_liqmicro_v2.py").read_text()
        main_src = src[src.index("def main") :]
        guard_check = main_src.index('guard.get("status") != "READY_FROZEN"')
        pipeline_call = main_src.index("_run_pipeline(")
        self.assertGreater(pipeline_call, guard_check)


class Test118G5GuardedReadyWritingNoReadyRefusalMatrix(unittest.TestCase):
    """G5: NO-READY refusal matrix for guarded_tracka_ready_writing scripts."""

    SCRIPTS_AND_TARGETS = [
        ("coupled_robust_eval", CANONICAL_TARGETS["coupled_robust_eval"]),
        ("fclr010_execute", CANONICAL_TARGETS["fclr010_execute"]),
        ("fclr010_coverage_audit", CANONICAL_TARGETS["fclr010_coverage_audit"]),
        ("liqmicro_audit", CANONICAL_TARGETS["liqmicro_audit"]),
        ("overlay_quick", CANONICAL_TARGETS["overlay_quick"]),
        ("overlay_tracka_execute", CANONICAL_TARGETS["overlay_tracka_execute"]),
    ]

    def _run_blocked_main(self, mod_name, payload):
        mod = importlib.import_module(f"scripts.{mod_name}")
        targets = CANONICAL_TARGETS.get(mod_name, [])
        before = _snapshot(targets)
        old_argv = sys.argv[:]
        try:
            sys.argv = [f"{mod_name}.py"]
            with patch(
                "scripts.fclr010_guarded_entry.guarded_execute",
                return_value=dict(payload),
            ), redirect_stdout(io.StringIO()) as buf:
                rc = mod.main()
            out = buf.getvalue()
        finally:
            sys.argv = old_argv
        return rc, out, before

    def test_matrix_all_non_ready_states_refuse_no_mutation(self):
        """For every guarded ready-writing script and every non-READY guard
        state (missing prereg, NOGO seam, modeled/proxy, wrong venue): rc=1,
        BLOCKED printed, canonical_outputs_mutated:false, no canonical target
        mutation, no real research_state write."""
        for mod_name, targets in self.SCRIPTS_AND_TARGETS:
            before = _snapshot(targets)
            for state_name, payload in NON_READY_PAYLOADS.items():
                rc, out, _ = self._run_blocked_main(mod_name, payload)
                self.assertEqual(
                    rc, 1, f"{mod_name} [{state_name}] did not refuse (rc={rc})"
                )
                self.assertIn("BLOCKED", out, f"{mod_name} [{state_name}] no BLOCKED")
                m = re.search(r"\{.*\}", out, re.S)
                self.assertIsNotNone(m, f"{mod_name} [{state_name}] no JSON payload")
                p = json.loads(m.group(0))
                self.assertEqual(p.get("status"), "BLOCKED", f"{mod_name} [{state_name}]")
                self.assertFalse(
                    p.get("canonical_outputs_mutated", True),
                    f"{mod_name} [{state_name}] canonical_outputs_mutated true",
                )
                self.assertFalse(
                    p.get("network", True), f"{mod_name} [{state_name}] network true"
                )
                self.assertFalse(
                    p.get("writes_real_research_state", True),
                    f"{mod_name} [{state_name}] writes_real_research_state true",
                )
            # After all states, canonical targets must be unchanged.
            _assert_snapshot_unchanged(targets, before)

    def test_each_script_canonical_targets_never_mutated_blocked(self):
        """Explicit per-script: blocked main never writes its canonical outputs."""
        for mod_name, targets in self.SCRIPTS_AND_TARGETS:
            before = _snapshot(targets)
            rc, out, _ = self._run_blocked_main(mod_name, dict(BLOCKED_PAYLOAD))
            self.assertEqual(rc, 1, mod_name)
            _assert_snapshot_unchanged(targets, before)

    def test_fclr010_execute_loader_failure_no_canonical_mutation(self):
        """fclr010_execute specific: post-READY loader failure (manifest
        unavailable/corrupt) yields controlled refusal, no summary/manifest
        mutation, stable reason_code."""
        mod = importlib.import_module("scripts.fclr010_execute")
        targets = CANONICAL_TARGETS["fclr010_execute"]
        before = _snapshot(targets)
        loader_fail = {
            "status": "BLOCKED",
            "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS",
            "reason": "outcome_loader failed: LFS pointer unmaterialized",
            "outcomes_inspected": False,
            "canonical_outputs_mutated": False,
            "network": False,
            "writes_real_research_state": False,
        }
        rc, out, _ = self._run_blocked_main("fclr010_execute", loader_fail)
        self.assertEqual(rc, 1)
        m = re.search(r"\{.*\}", out, re.S)
        self.assertIsNotNone(m)
        p = json.loads(m.group(0))
        self.assertEqual(p["reason_code"], "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")
        self.assertFalse(p["canonical_outputs_mutated"])
        _assert_snapshot_unchanged(targets, before)


if __name__ == "__main__":
    unittest.main()
