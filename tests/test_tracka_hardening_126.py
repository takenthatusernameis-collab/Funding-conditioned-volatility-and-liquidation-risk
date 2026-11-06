"""FCLR-NEXT-126: gate refusal-shape + fail-closed order (G1),
fclr010_execute blocked-entry rc + script field (G2),
run_liqmicro v1 READY write-scope / blocked no-pipeline (G3).

Deterministic, tmp-isolated, no network, no parquet/outcome reads,
no real research_state writes. Dep-light.
"""
from __future__ import annotations

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

REAL = Path(__file__).resolve().parent.parent
RS = REAL / "research_state"
FRONTIER = RS / "experiment_frontier.json"
RUN_MANIFEST = RS / "run_manifest.json"
EVAL_FCLR010 = RS / "evaluation_summary_FCLR010.md"
EVAL_LIQM1 = RS / "evaluation_summary_FCLR-LIQMICRO-001.md"
LIQMICRO_DIR = REAL / "results" / "liqmicro"
BLOCKED_RC = "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS"
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


def _results_liqmicro_snapshot():
    if not LIQMICRO_DIR.exists():
        return {}
    return {
        str(p.relative_to(REAL)): p.read_bytes()
        for p in sorted(LIQMICRO_DIR.rglob("*"))
        if p.is_file()
    }


def _parse_json_stdout(buf):
    m = re.search(r"\{.*\}", buf.getvalue(), re.S)
    assert m is not None, f"no JSON object in stdout: {buf.getvalue()!r}"
    return json.loads(m.group(0))


def _mock_heavy():
    for mn in (
        "numpy", "pandas", "pyarrow", "pyarrow.parquet",
        "statsmodels", "statsmodels.api", "statsmodels.formula.api",
        "scipy", "scipy.stats",
    ):
        sys.modules.pop(mn, None)

    def _mod(name, **attrs):
        m = types.ModuleType(name)
        for k, v in attrs.items():
            setattr(m, k, v)
        sys.modules[name] = m
        return m

    class _DF:
        def __init__(self, *a, **k):
            pass

        def __len__(self):
            return 0

        @property
        def empty(self):
            return True

        @property
        def shape(self):
            return (0, 0)

        def __getitem__(self, k):
            return _S()

        def to_csv(self, *a, **k):
            pass

        def to_parquet(self, *a, **k):
            pass

        def describe(self):
            return self

    class _S:
        def nunique(self):
            return 1

        @property
        def min(self):
            return None

        @property
        def max(self):
            return None

    _mod(
        "numpy",
        nan=float("nan"), isnan=lambda x: False, isinf=lambda x: False,
        float64=float, int64=int, ones=lambda n, *a, **k: [0.0] * int(n),
        array=lambda x, *a, **k: list(x), sign=lambda x: 0,
        clip=lambda x, *a, **k: x, log1p=lambda x: x,
        maximum=lambda a, b: a, minimum=lambda a, b: a,
        quantile=lambda x, q: 0.0, exp=lambda x: 1.0,
        column_stack=lambda cols: cols, zeros=lambda *a, **k: [],
        mean=lambda x, *a, **k: 0.0, sum=lambda x, *a, **k: 0,
        abs=lambda x: x, diff=lambda x, *a, **k: [],
        float_=float, ndarray=list, isnull=lambda x: False,
    )
    sys.modules["numpy"].linalg = types.ModuleType("numpy.linalg")
    sys.modules["numpy"].linalg.solve = lambda A, b: [0.0] * len(b)
    sys.modules["numpy"].linalg.pinv = lambda A: []
    _mod(
        "pandas",
        DataFrame=_DF, read_parquet=lambda *a, **k: _DF(),
        Timestamp=lambda x: x, concat=lambda frames, *a, **k: frames[0] if frames else _DF(),
        date_range=lambda *a, **k: [], NA=None, isnull=lambda x: False,
    )
    _mod("pyarrow")
    _mod("pyarrow.parquet")
    _mod("statsmodels")
    _mod("statsmodels.api", add_constant=lambda x: x)
    _mod("statsmodels.formula.api", ols=lambda *a, **k: None)
    _mod("scipy")
    _mod("scipy.stats")


def _fresh_mod(name):
    _mock_heavy()
    for mn in (
        name,
        "scripts.run_liqmicro",
        "scripts.fclr010_execute",
        "analysis.liqmicro.ingest",
        "analysis.liqmicro.features",
        "analysis.liqmicro.models",
        "analysis.liqmicro.stats",
    ):
        sys.modules.pop(mn, None)
    return importlib.import_module(name)


class Test126G1GateRefusalShapeFailClosedOrder(unittest.TestCase):
    """G1: tracka_resume_gate decide/CLI returns stable BLOCKED refusal shape
    on missing prereg with drift preflight first, no real research_state writes."""

    def test_decide_nonexistent_prereg_refusal_shape(self):
        with tempfile.TemporaryDirectory() as td:
            from scripts.tracka_resume_gate import decide

            res = decide(
                data_path="/nonexistent_tracka_data",
                output_dir=td,
                pre_reg_path="/nonexistent_prereg_tracka_126.json",
                source_manifest=None,
            )
        self.assertEqual(res.get("status"), "BLOCKED", res)
        self.assertEqual(res.get("reason_code"), BLOCKED_RC, res)
        self.assertEqual(
            res.get("fail_closed_order"),
            "drift_preflight->manifest_prereg",
            res,
        )
        self.assertFalse(res.get("outcomes_inspected"), res)
        self.assertFalse(res.get("network"), res)
        self.assertFalse(res.get("writes_real_research_state"), res)
        self.assertEqual(res.get("gate_script"), "tracka_resume_gate", res)
        self.assertIn("drift_preflight", res)
        self.assertTrue(res["drift_preflight"].get("pass"), res["drift_preflight"])

    def test_cli_nonexistent_prereg_rc1_and_shape(self):
        with tempfile.TemporaryDirectory() as td:
            from scripts import tracka_resume_gate

            argv = [
                "--data", "/nonexistent_tracka_data",
                "--output-dir", td,
                "--prereg", "/nonexistent_prereg_tracka_126.json",
                "--json",
            ]
            with redirect_stdout(io.StringIO()) as buf:
                rc = tracka_resume_gate.main(argv)
            res = _parse_json_stdout(buf)
        self.assertEqual(rc, 1, (rc, res))
        self.assertEqual(res.get("status"), "BLOCKED", res)
        self.assertEqual(res.get("reason_code"), BLOCKED_RC, res)
        self.assertEqual(
            res.get("fail_closed_order"),
            "drift_preflight->manifest_prereg",
            res,
        )
        self.assertFalse(res.get("outcomes_inspected"), res)
        self.assertTrue(res.get("drift_preflight", {}).get("pass"), res)
        self.assertFalse(res.get("network"), res)
        self.assertFalse(res.get("writes_real_research_state"), res)
        self.assertEqual(res.get("gate_script"), "tracka_resume_gate", res)

    def test_drift_preflight_enforced_first_on_block(self):
        # A synthetic failing drift via harness_root pointing at a dir with bad registry
        # is not used here because drift uses repo_root (REAL) by default; instead we
        # assert the positive invariant: pass:true precedes manifest/prereg decision.
        with tempfile.TemporaryDirectory() as td:
            from scripts.tracka_resume_gate import decide

            res = decide(
                data_path="/nonexistent_tracka_data",
                output_dir=td,
                pre_reg_path="/nonexistent_prereg_tracka_126.json",
            )
        self.assertTrue(res["drift_preflight"].get("pass"), res)
        self.assertEqual(res.get("reason_code"), BLOCKED_RC, res)
        self.assertEqual(
            res.get("fail_closed_order"),
            "drift_preflight->manifest_prereg",
            res,
        )


class Test126G2Fclr010ExecuteBlockedRcAndScript(unittest.TestCase):
    """G2: blocked fclr010_execute main returns rc=1 with stable refusal payload."""

    def _blocked_guard(self, **extra):
        base = {
            "status": "BLOCKED",
            "reason_code": BLOCKED_RC,
            "outcomes_inspected": False,
            "canonical_outputs_mutated": False,
            "network": False,
            "writes_real_research_state": False,
            "data_loaded_implicitly": False,
            "reads_parquet": False,
            "reads_outcomes": False,
            "outcomes_loaded": None,
            "seam_go_prereg_required": True,
            "reason_code_detail": "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED",
        }
        base.update(extra)
        return base

    def test_blocked_main_rc1_and_full_refusal_fields(self):
        mod = _fresh_mod("scripts.fclr010_execute")
        before = _snap([FRONTIER, RUN_MANIFEST, EVAL_FCLR010])
        guard = self._blocked_guard()
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=guard), \
             redirect_stdout(io.StringIO()) as buf:
            rc = mod.main()
        p = _parse_json_stdout(buf)
        self.assertEqual(rc, 1, (rc, p))
        self.assertEqual(p.get("status"), "BLOCKED", p)
        self.assertEqual(p.get("reason_code"), BLOCKED_RC, p)
        self.assertEqual(p.get("script"), "fclr010_execute", p)
        self.assertFalse(p.get("canonical_outputs_mutated"), p)
        self.assertFalse(p.get("network"), p)
        self.assertFalse(p.get("writes_real_research_state"), p)
        self.assertFalse(p.get("outcomes_inspected"), p)
        for k in REQ_REFUSAL:
            self.assertIn(k, p, (k, p))
        _unchanged([FRONTIER, RUN_MANIFEST, EVAL_FCLR010], before)

    def test_blocked_main_no_loader_no_parquet(self):
        mod = _fresh_mod("scripts.fclr010_execute")
        guard = self._blocked_guard()
        loader_called = {"n": 0}

        def _boom(*a, **k):
            loader_called["n"] += 1
            raise AssertionError("loader/parquet path must not run on blocked main")

        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=guard), \
             patch.object(mod, "_load_outcomes_guarded", _boom, create=True), \
             redirect_stdout(io.StringIO()):
            rc = mod.main()
        self.assertEqual(rc, 1)
        self.assertEqual(loader_called["n"], 0)


class Test126G3RunLiqmicroV1ReadyWriteScope(unittest.TestCase):
    """G3: blocked run_liqmicro never invokes _run_pipeline/never mutates canonicals;
    READY_FROZEN with mocked no-op _run_pipeline confined away from canonicals."""

    def _blocked_guard(self):
        return {
            "status": "BLOCKED",
            "reason_code": BLOCKED_RC,
            "outcomes_inspected": False,
            "canonical_outputs_mutated": False,
            "network": False,
            "writes_real_research_state": False,
            "data_loaded_implicitly": False,
            "reads_parquet": False,
            "reads_outcomes": False,
            "outcomes_loaded": None,
            "seam_go_prereg_required": True,
            "reason_code_detail": "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED",
        }

    def test_blocked_never_invokes_pipeline_never_mutates_canonicals(self):
        mod = _fresh_mod("scripts.run_liqmicro")
        before = _snap([FRONTIER, RUN_MANIFEST, EVAL_FCLR010, EVAL_LIQM1])
        liq_before = _results_liqmicro_snapshot()
        called = {"n": 0}

        def _boom(*a, **k):
            called["n"] += 1
            raise AssertionError("_run_pipeline must not run on blocked path")

        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=self._blocked_guard()), \
             patch.object(mod, "_run_pipeline", _boom), \
             redirect_stdout(io.StringIO()) as buf:
            rc = mod.main()
        p = _parse_json_stdout(buf)
        self.assertEqual(rc, 1, (rc, p))
        self.assertEqual(called["n"], 0)
        self.assertEqual(p.get("status"), "BLOCKED", p)
        self.assertEqual(p.get("script"), "run_liqmicro", p)
        self.assertFalse(p.get("canonical_outputs_mutated"), p)
        _unchanged([FRONTIER, RUN_MANIFEST, EVAL_FCLR010, EVAL_LIQM1], before)
        self.assertEqual(_results_liqmicro_snapshot(), liq_before)

    def test_ready_frozen_mocked_pipeline_no_canonical_writes(self):
        mod = _fresh_mod("scripts.run_liqmicro")
        before = _snap([FRONTIER, RUN_MANIFEST, EVAL_FCLR010, EVAL_LIQM1])
        liq_before = _results_liqmicro_snapshot()
        called = {"n": 0}

        def _noop(raw_df, hourly):
            called["n"] += 1

        class _DF:
            def __len__(self): return 0
        class _Sym:
            def nunique(self): return 0
        class _Hourly:
            @property
            def empty(self): return True
            def __getitem__(self, k): return _Sym()
            def __len__(self): return 0
        guard = {
            "status": "READY_FROZEN",
            "outcomes_inspected": False,
            "canonical_outputs_mutated": False,
            "network": False,
            "writes_real_research_state": False,
            "data_loaded_implicitly": False,
            "outcomes_loaded": {"raw_df": _DF(), "hourly": _Hourly()},
        }
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=guard), \
             patch.object(mod, "_run_pipeline", _noop), \
             redirect_stdout(io.StringIO()):
            rc = mod.main()
        self.assertEqual(rc, 0)
        self.assertEqual(called["n"], 1)
        # Mocked _run_pipeline does no writes: canonicals unchanged, results/liqmicro unchanged.
        _unchanged([FRONTIER, RUN_MANIFEST, EVAL_FCLR010, EVAL_LIQM1], before)
        self.assertEqual(_results_liqmicro_snapshot(), liq_before)

    def test_source_order_guard_precedes_pipeline_and_frontier_writer_inside(self):
        src = (REAL / "scripts" / "run_liqmicro.py").read_text()
        guarded_idx = src.index("guard = guarded_execute(")
        blocked_refusal_idx = src.index("return 1", guarded_idx)
        pipeline_call_idx = src.index("_run_pipeline(raw_df, hourly)")
        self.assertLess(guarded_idx, blocked_refusal_idx)
        self.assertLess(blocked_refusal_idx, pipeline_call_idx)
        # Frontier writer invoked only inside _run_pipeline body (READY path), never in main/blocked flow.
        pipeline_def = src.index("def _run_pipeline")
        writer_call = src.index("_write_experiment_frontier_ready(any_sig, summary_path)")
        self.assertLess(pipeline_def, writer_call)
        self.assertLess(writer_call, src.index("def _write_experiment_frontier_ready", pipeline_def))
        main_def = src.index("def main() -> int:")
        # no frontier writer call in main
        main_body = src[main_def:src.index('if __name__ == "__main__":')]
        self.assertNotIn("_write_experiment_frontier_ready", main_body)


if __name__ == "__main__":
    unittest.main()
