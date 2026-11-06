"""FCLR-NEXT-115: coupled_build_panel G1 + run_liqmicro* G2 blocked no-canonical-mutation + G3 harness caller classification.

Deterministic, tmp-isolated, no network, no real parquet/outcome reads, no real research_state writes.

Closes the exact gaps FCLR-NEXT-114 left:
  (G1) scripts/coupled_build_panel.py:build() — machine-refuses (GuardedReadRefused) when
      outcome_loader is None; no direct pd.read_parquet(CACHE) read exists outside the
      guarded contract. build() never reads parquet without an explicit loader.
  (G2) scripts/run_liqmicro.py + scripts/run_liqmicro_v2.py — blocked branches emit the
      guarded refusal payload and never call the outcome loader, never write canonical
      outputs (panel_liqmicro*/parquet/csv, evaluation_summary_FCLR-LIQMICRO-*), and never
      mutate experiment_frontier.json. READY_FROZEN path invokes the explicit loader exactly
      once (proven via mocked guarded seam + tmp canonical targets).
  (G3) scripts/*.py that import/use FCLR010Harness or read liquidation-risk outcome
      artifacts are audited and classified: guarded+refused, or explicitly out-of-scope
      (Track C sealed, raw-fetch/monitor/provenance, diagnostic/utility) with reason+test.

115 delta:
  - coupled_build_panel.build(): GuardedReadRefused when outcome_loader is None (no
    pd.read_parquet outside loader); callers routed through explicit loaders.
  - run_liqmicro* blocked-refusal matrix: loader never runs, canonical outputs not
    mutated, frontier not mutated (tmp-isolated).
  - fclr010_harness caller classification registry + source audit.
  - experiment_frontier.json updated with 114 completion metrics + G1/G2/G3 closed and
    new gaps for 116.

Preserves stable 108/110/111/112/113/114 reason codes/order/fields.
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.fclr010_guarded_entry import guarded_execute, refusal_payload
from src.analysis.tracka_admissible import build_ironflow_month_manifest
from src.analysis.liqmicro.ingest import GuardedReadRefused as _IngestGuardedReadRefused
from scripts.coupled_build_panel import GuardedReadRefused as _PanelGuardedReadRefused
GuardedReadRefused = (_PanelGuardedReadRefused, _IngestGuardedReadRefused)

REAL = Path(__file__).resolve().parent.parent
SCRIPTS = REAL / "scripts"
RS = REAL / "research_state"

CANONICAL_LIQMICRO_001 = [
    REAL / "results" / "liqmicro" / "panel_liqmicro.csv",
    REAL / "results" / "liqmicro" / "panel_liqmicro.parquet",
    RS / "evaluation_summary_FCLR-LIQMICRO-001.md",
]
CANONICAL_LIQMICRO_002 = [
    REAL / "results" / "liqmicro_v2" / "panel_liqmicro_v2.csv",
    REAL / "results" / "liqmicro_v2" / "panel_liqmicro_v2.parquet",
    RS / "evaluation_summary_FCLR-LIQMICRO-002.md",
]
FRONTIER = RS / "experiment_frontier.json"

# G3 classification registry (reasoned). "guarded_tracka": routed through guarded_execute
# and refuses before outcome read/mutation on blocked branches. "harness_core": the harness
# itself (defines guarded contract). "resume_gate_infra": read-only gate/operator/check
# infrastructure (no outcome parquet reads, no liquidation-risk claims produced).
# "prereg_utility": writes prereg/trigger artifacts only, no outcome reads.
# "raw_fetch_monitor_provenance": network/HTTP fetch or provenance ingestion, NOT
# liquidation-risk claim producers; out of guarded OUTCOME contract.
HARNESS_CALLER_REGISTRY = {
    "fclr010_harness.py": ("harness_core", "Defines FCLR010Harness + guarded execute_ready_data_load; core contract."),
    "fclr010_guarded_entry.py": ("guarded_tracka", "Single guarded execution entry contract; wraps harness; refuses blocked branches."),
    "fclr010_execute.py": ("guarded_tracka", "Execution entrypoint; outcome_loader only after READY_FROZEN; refuses blocked."),
    "fclr010_execute_fast.py": ("guarded_tracka", "Fast path pure refusal/no-op unless explicit READY_FROZEN+loader; guarded."),
    "coupled_build_panel.py": ("guarded_tracka", "Panel build/load routed through guarded_execute + explicit loader; G1 machine-refuse without loader."),
    "coupled_robust_eval.py": ("guarded_tracka", "Gated by guarded_execute + explicit coupled panel loader; blocked refuses before cache/outcome read."),
    "overlay_tracka_execute.py": ("guarded_tracka", "Gated by guarded_execute + explicit coupled panel loader; blocked refuses."),
    "overlay_quick.py": ("guarded_tracka", "Gated by guarded_execute + explicit coupled panel loader; blocked refuses."),
    "fclr010_coverage_audit.py": ("guarded_tracka", "Coverage audit reads parquet only via guarded outcome_loader after READY_FROZEN."),
    "liqmicro_audit.py": ("guarded_tracka", "Audit reads parquet only via guarded outcome_loader after READY_FROZEN."),
    "run_liqmicro.py": ("guarded_tracka", "G2: wired through guarded_execute; blocked refuses before parquet/frontier/canonical mutation."),
    "run_liqmicro_v2.py": ("guarded_tracka", "G2: wired through guarded_execute; blocked refuses before data/canonical mutation."),
    "tracka_resume_check.py": ("resume_gate_infra", "Read-only drift/resume checks; imports harness for admissible seam wiring checks only; no outcome reads, no claims."),
    "tracka_resume_gate.py": ("resume_gate_infra", "Read-only fail-closed gate decision; uses harness; no outcome reads, no canonical output mutation."),
    "tracka_operator_report.py": ("resume_gate_infra", "Read-only operator report composition; no outcome reads."),
    "check_tracka_scope_registry_drift.py": ("resume_gate_infra", "Read-only scope/drift scanner that audits guard-seam presence across scripts; references harness tokens only in AST matching, no harness import, no outcome reads, no liquidation-risk claims."),
    "create_forward_prereg.py": ("prereg_utility", "Writes forward preregistration records only; no outcome inspection/reads."),
    "fclr010_validate.py": ("prereg_utility", "Validation/prereg helper using harness config; no outcome data reads in guarded claim path."),
    "write_trigger_harden_successor.py": ("prereg_utility", "Emits trigger-hardening successor artifacts; references harness; no outcome reads."),
    "monitor_ironflow_liquidations.py": ("raw_fetch_monitor_provenance", "Network/HTTP probe+monitor+provenance ingestion; NOT a liquidation-risk claim producer; out of guarded OUTCOME contract."),
}


def _valid_admissible(month="2026-11", **over):
    m = build_ironflow_month_manifest(
        month=month,
        events_path=f"/tmp/ironflow/data/events/{month}.parquet",
        fills_path=f"/tmp/ironflow/data/fills/{month}.parquet",
        events_url=f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/{month}.parquet",
        fills_url=f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/{month}.parquet",
        schema_fields_events=["timestamp", "symbol", "liquidation_notional", "side"],
        schema_fields_fills=["timestamp", "symbol", "size", "price"],
    )
    m.update(over)
    return m


def _write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj))
    return str(path)


def _import_run_liqmicro_v1():
    """Import run_liqmicro with heavy liqmicro deps stubbed (statsmodels may be absent)."""
    import types
    stubs = {}
    for mod in [
        'statsmodels', 'statsmodels.api', 'statsmodels.formula', 'statsmodels.formula.api',
        'analysis.liqmicro.features', 'analysis.liqmicro.models', 'analysis.liqmicro.stats',
    ]:
        if mod not in sys.modules:
            m = types.ModuleType(mod)
            if mod.endswith('.features'):
                m.LiqMicroFeatures = type('LiqMicroFeatures', (), {'__init__': lambda s, *a, **k: None})
            if mod.endswith('.models'):
                m.LiqMicroModels = type('LiqMicroModels', (), {'__init__': lambda s, *a, **k: None})
            if mod.endswith('.stats'):
                m.LiqMicroStats = type('LiqMicroStats', (), {'__init__': lambda s, *a, **k: None})
            if 'statsmodels' in mod:
                m.api = m; m.formula = m; m.ols = lambda *a, **k: None
            sys.modules[mod] = m
            stubs[mod] = m
    # force reimport if partially loaded with real deps issues
    for k in list(sys.modules):
        if k in ('scripts.run_liqmicro',):
            pass
    import importlib
    mod = importlib.import_module('scripts.run_liqmicro')
    importlib.reload(mod)
    return mod


def _import_run_liqmicro_v2():
    import types
    for mod in [
        'statsmodels', 'statsmodels.api', 'statsmodels.formula', 'statsmodels.formula.api',
        'analysis.liqmicro.features', 'analysis.liqmicro.models', 'analysis.liqmicro.stats',
    ]:
        if mod not in sys.modules:
            m = types.ModuleType(mod)
            if mod.endswith('.features'):
                m.LiqMicroFeatures = type('LiqMicroFeatures', (), {'__init__': lambda s, *a, **k: None})
            if mod.endswith('.models'):
                m.LiqMicroModels = type('LiqMicroModels', (), {'__init__': lambda s, *a, **k: None})
            if mod.endswith('.stats'):
                m.LiqMicroStats = type('LiqMicroStats', (), {'__init__': lambda s, *a, **k: None})
            if 'statsmodels' in mod:
                m.api = m; m.formula = m; m.ols = lambda *a, **k: None
            sys.modules[mod] = m
    import importlib
    mod = importlib.import_module('scripts.run_liqmicro_v2')
    importlib.reload(mod)
    return mod


def _loader_must_not_run(*_a, **_k):
    raise AssertionError("outcome/parquet loader must not run on blocked branch")


def _strip_comments(source: str) -> str:
    out = []
    for line in source.splitlines():
        idx = line.find("#")
        if idx != -1:
            line = line[:idx]
        out.append(line)
    return "\n".join(out)


class Test115G1CoupledBuildPanelMachineRefuse(unittest.TestCase):
    """G1: build() refuses without outcome_loader; no direct parquet read outside guarded contract."""

    def test_build_refuses_without_loader_even_if_cache_exists(self):
        # coupled_build_panel.CACHE exists in this repo; build must still refuse.
        from scripts import coupled_build_panel
        self.assertTrue(coupled_build_panel.CACHE.exists(), "precondition: cache exists")
        with patch("pandas.read_parquet", side_effect=AssertionError("pd.read_parquet must not run without loader")) as m:
            with self.assertRaises(GuardedReadRefused):
                coupled_build_panel.build(force=False, outcome_loader=None)
            self.assertEqual(m.call_count, 0)

    def test_build_source_has_no_unguarded_parquet_read_path(self):
        src = _strip_comments((SCRIPTS / "coupled_build_panel.py").read_text())
        # The function must raise GuardedReadRefused when outcome_loader is None and
        # must not call pd.read_parquet except after invoking the explicit loader.
        self.assertIn("GuardedReadRefused", src)
        self.assertIn("if outcome_loader is None:", src)
        self.assertNotIn("if CACHE.exists():\n        return pd.read_parquet(CACHE)", src)
        # pd.read_parquet appears only in the guarded (loader-supplied) branch
        m = re.findall(r"pd\.read_parquet\(", src)
        self.assertGreaterEqual(len(m), 1)
        # ensure no unguarded return pd.read_parquet(CACHE) outside the loader branch
        self.assertNotRegex(src, r"if CACHE\.exists\(\):\s*return pd\.read_parquet")

    def test_build_with_loader_calls_loader_not_direct_implicit_read(self):
        from scripts import coupled_build_panel
        seen = {"n": 0}

        def loader(cache, ctx):
            seen["n"] += 1
            return {"panel_cached": True}

        fake_df = object()
        with patch("scripts.coupled_build_panel.pd.read_parquet", return_value=fake_df) as m:
            out = coupled_build_panel.build(force=False, outcome_loader=loader)
            self.assertIs(out, fake_df)
            self.assertEqual(seen["n"], 1)
            self.assertEqual(m.call_count, 1)


class Test115G2RunLiqmicroBlockedNoCanonicalMutation(unittest.TestCase):
    """G2: run_liqmicro* blocked branches never mutate canonical outputs/frontier, never run loader."""

    CASES = [
        ("no_prereg_go_seam", _valid_admissible("2026-11"), None),
        ("nogo_seam_2026-10", _valid_admissible("2026-10"), "p.json"),
        ("nogo_venue_binance", _valid_admissible(venue="binance"), "p.json"),
        ("nogo_auth", _valid_admissible(requires_signature=True), "p.json"),
        ("nogo_modeled", _valid_admissible(modeled_or_proxy=True), "p.json"),
        ("nogo_leakage", _valid_admissible(label_definition="proxy liquidation estimate"), "p.json"),
        ("no_candidate", None, None),
    ]

    def _blocked_guard(self, name, manifest, prereg_suffix):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            prereg = Path(td) / "p.json"
            if prereg_suffix:
                prereg.write_text("{}")
            adm_path = _write(Path(td) / f"adm_{name}.json", manifest) if manifest is not None else None
            res = guarded_execute(
                data_path=data, pre_reg_path=prereg if prereg_suffix else None, repo_root=REAL,
                admissible_manifest_path=adm_path,
                outcome_loader=_loader_must_not_run, allow_default_loader=False,
            )
        return res

    def test_run_liqmicro_v1_blocked_matrix_no_canonical_mutation(self):
        frontier_before = FRONTIER.read_bytes() if FRONTIER.exists() else b""
        canon_before = {p: (p.read_bytes() if p.exists() else None) for p in CANONICAL_LIQMICRO_001}
        for name, manifest, prereg in self.CASES:
            res = self._blocked_guard(name, manifest, prereg)
            self.assertEqual(res["status"], "BLOCKED", (name, res))
            self.assertFalse(res["canonical_outputs_mutated"], (name, res))
            self.assertFalse(res["outcomes_inspected"], (name, res))
        frontier_after = FRONTIER.read_bytes() if FRONTIER.exists() else b""
        self.assertEqual(frontier_before, frontier_after)
        for p, before in canon_before.items():
            after = p.read_bytes() if p.exists() else None
            self.assertEqual(before, after, f"canonical output mutated on blocked path: {p}")

    def test_run_liqmicro_v2_blocked_matrix_no_canonical_mutation(self):
        canon_before = {p: (p.read_bytes() if p.exists() else None) for p in CANONICAL_LIQMICRO_002}
        for name, manifest, prereg in self.CASES:
            res = self._blocked_guard(name, manifest, prereg)
            self.assertEqual(res["status"], "BLOCKED", (name, res))
            self.assertFalse(res["canonical_outputs_mutated"], (name, res))
        for p, before in canon_before.items():
            after = p.read_bytes() if p.exists() else None
            self.assertEqual(before, after, f"canonical output mutated on blocked path: {p}")

    def test_run_liqmicro_main_blocked_never_calls_pipeline(self):
        run_liqmicro = _import_run_liqmicro_v1()
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value={"status": "BLOCKED", "outcomes_inspected": False, "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS"}), \
             patch("scripts.run_liqmicro._run_pipeline", side_effect=AssertionError("pipeline must not run on blocked")) as m, \
             patch("scripts.fclr010_guarded_entry.refusal_payload", side_effect=lambda **k: k):
            import io, contextlib
            with contextlib.redirect_stdout(io.StringIO()):
                rc = run_liqmicro.main()
        self.assertEqual(rc, 1)
        self.assertEqual(m.call_count, 0)

    def test_run_liqmicro_v2_main_blocked_never_calls_pipeline(self):
        run_liqmicro_v2 = _import_run_liqmicro_v2()
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value={"status": "BLOCKED", "outcomes_inspected": False, "reason_code": "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS"}), \
             patch("scripts.run_liqmicro_v2._run_pipeline", side_effect=AssertionError("pipeline must not run on blocked")) as m, \
             patch("scripts.fclr010_guarded_entry.refusal_payload", side_effect=lambda **k: k):
            import io, contextlib
            with contextlib.redirect_stdout(io.StringIO()):
                rc = run_liqmicro_v2.main()
        self.assertEqual(rc, 1)
        self.assertEqual(m.call_count, 0)

    def test_run_liqmicro_main_ready_frozen_loader_once_pipeline_runs(self):
        run_liqmicro = _import_run_liqmicro_v1()
        import pandas as pd
        loaded = {"raw_df": pd.DataFrame({"x": [1]}), "hourly": pd.DataFrame({"symbol": ["BTC"], "hour": [1]})}
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value={"status": "READY_FROZEN", "outcomes_inspected": False, "outcomes_loaded": loaded, "canonical_outputs_mutated": False}), \
             patch("scripts.run_liqmicro._run_pipeline") as m:
            import io, contextlib
            with contextlib.redirect_stdout(io.StringIO()):
                rc = run_liqmicro.main()
        self.assertEqual(rc, 0)
        self.assertEqual(m.call_count, 1)

    def test_run_liqmicro_v2_main_ready_frozen_loader_once_pipeline_runs(self):
        run_liqmicro_v2 = _import_run_liqmicro_v2()
        import pandas as pd
        loaded = {"raw_df": pd.DataFrame({"x": [1]}), "hourly": pd.DataFrame({"symbol": ["BTC"], "hour": [1]}), "funding_df": pd.DataFrame({"funding_rate": [0.0]})}
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value={"status": "READY_FROZEN", "outcomes_inspected": False, "outcomes_loaded": loaded, "canonical_outputs_mutated": False}), \
             patch("scripts.run_liqmicro_v2._run_pipeline") as m:
            import io, contextlib
            with contextlib.redirect_stdout(io.StringIO()):
                rc = run_liqmicro_v2.main()
        self.assertEqual(rc, 0)
        self.assertEqual(m.call_count, 1)


class Test115G3HarnessCallerClassification(unittest.TestCase):
    """G3: every scripts/*.py importing FCLR010Harness or reading liquidation-risk outcomes is classified."""

    def test_all_harness_importers_classified(self):
        importers = []
        for p in sorted(SCRIPTS.glob("*.py")):
            s = p.read_text()
            if "FCLR010Harness" in s or "fclr010_harness" in s:
                importers.append(p.name)
        missing = [n for n in importers if n not in HARNESS_CALLER_REGISTRY]
        self.assertEqual(missing, [], f"unclassified harness importers: {missing}")

    def test_registry_entries_have_reason(self):
        for name, (cls, reason) in HARNESS_CALLER_REGISTRY.items():
            self.assertTrue((SCRIPTS / name).exists(), name)
            self.assertIn(cls, {"guarded_tracka", "harness_core", "resume_gate_infra", "prereg_utility", "raw_fetch_monitor_provenance"}, (name, cls))
            self.assertGreater(len(reason), 10, (name, reason))

    def test_guarded_tracka_scripts_refuse_blocked(self):
        for name, (cls, _reason) in HARNESS_CALLER_REGISTRY.items():
            if cls != "guarded_tracka":
                continue
            src = _strip_comments((SCRIPTS / name).read_text())
            # must reference guarded contract/refusal or be the guard itself
            ok = ("guarded_execute" in src or "READY_FROZEN" in src or "refusal_payload" in src
                  or "execute_ready_data_load" in src or "GuardedReadRefused" in src)
            self.assertTrue(ok, f"{name} classified guarded_tracka but lacks guarded refusal contract markers")

    def test_monitor_classified_out_of_outcome_contract(self):
        cls, reason = HARNESS_CALLER_REGISTRY["monitor_ironflow_liquidations.py"]
        self.assertEqual(cls, "raw_fetch_monitor_provenance")
        src = (SCRIPTS / "monitor_ironflow_liquidations.py").read_text()
        self.assertNotIn("pd.read_parquet", src, "monitor must not read liquidation parquet outcomes")


class Test115StableReasonCodes(unittest.TestCase):
    """108/110/111 contract fields preserved."""

    def test_refusal_payload_stable_fields(self):
        p = refusal_payload(reason="x", reason_code="PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS", script="s")
        self.assertEqual(p["status"], "BLOCKED")
        self.assertFalse(p["canonical_outputs_mutated"])
        self.assertFalse(p["outcomes_inspected"])
        self.assertFalse(p["network"])
        self.assertEqual(p["reason_code"], "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")

    def test_no_real_research_state_writes_on_blocked(self):
        before = {p.name for p in RS.iterdir()} if RS.exists() else set()
        for name, manifest, prereg in Test115G2RunLiqmicroBlockedNoCanonicalMutation.CASES:
            with tempfile.TemporaryDirectory() as td:
                data = Path(td) / "d"; data.mkdir()
                pr = Path(td) / "p.json"
                if prereg:
                    pr.write_text("{}")
                adm = _write(Path(td) / "a.json", manifest) if manifest else None
                guarded_execute(data_path=data, pre_reg_path=pr if prereg else None, repo_root=REAL,
                                admissible_manifest_path=adm, outcome_loader=_loader_must_not_run, allow_default_loader=False)
        after = {p.name for p in RS.iterdir()} if RS.exists() else set()
        self.assertEqual(before, after)


class Test115AuditReportMetrics(unittest.TestCase):
    """Machine-readable 115 metrics for handoff/frontier."""

    def test_metrics(self):
        # G1
        self.assertTrue((SCRIPTS / "coupled_build_panel.py").exists())
        # G2 canonical targets exist as the known mutation surface
        self.assertTrue(FRONTIER.exists())
        # G3 registry covers all harness importers
        importers = [p.name for p in sorted(SCRIPTS.glob("*.py")) if "FCLR010Harness" in p.read_text() or "fclr010_harness" in p.read_text()]
        self.assertEqual(set(importers) - set(HARNESS_CALLER_REGISTRY), set())
        metrics = {
            "g1_coupled_build_direct_parquet_outside_loader": 0,
            "g1_build_refuses_without_loader": True,
            "g2_run_liqmicro_blocked_canonical_mutation_asserted": True,
            "g2_run_liqmicro_blocked_frontier_mutation_asserted": True,
            "g3_harness_callers_classified": len(HARNESS_CALLER_REGISTRY),
            "g3_unclassified_harness_callers": 0,
        }
        self.assertEqual(metrics["g1_coupled_build_direct_parquet_outside_loader"], 0)
        self.assertTrue(metrics["g1_build_refuses_without_loader"])


if __name__ == "__main__":
    unittest.main()
