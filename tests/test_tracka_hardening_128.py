"""FCLR-NEXT-128: coupled_build_panel blocked-refusal parity (G1) +
tracka_operator_report seam-wired fields (G2) +
refusal-payload fail-closed matrix extension to coupled_build_panel +
fclr010_execute_fast (G3).

Deterministic, tmp-isolated, no network, no parquet/outcome reads,
no real research_state writes. Dep-light: heavy deps (numpy/pandas/pyarrow)
are stubbed so the suite runs in minimal environments.
"""
from __future__ import annotations

import builtins
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
CACHE = RS / ".cache" / "fclr_coupled_panel.parquet"
EVAL_FCLR010 = RS / "evaluation_summary_FCLR010.md"
OUT_SUM = RS / "evaluation_summary_FCLR010.md"
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


def _parse_json_stdout(buf):
    m = re.search(r"\{.*\}", buf.getvalue(), re.S)
    assert m is not None, f"no JSON object in stdout: {buf.getvalue()!r}"
    return json.loads(m.group(0))


def _mock_heavy():
    for mn in ("numpy", "pandas", "pyarrow", "pyarrow.parquet",
               "statsmodels", "statsmodels.api", "statsmodels.formula.api",
               "scipy", "scipy.stats"):
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

        def __getitem__(self, k):
            return _S()

        def sort_values(self, *a, **k):
            return self

        def groupby(self, *a, **k):
            return _GB()

        def to_dict(self, *a, **k):
            return []

        def copy(self):
            return _DF()

    class _S:
        def nunique(self):
            return 0

        @property
        def min(self):
            return None

        @property
        def max(self):
            return None

    class _GB:
        def __getattr__(self, k):
            return self

        def __call__(self, *a, **k):
            return self

        def shift(self, *a, **k):
            return _S()

        def rolling(self, *a, **k):
            return _RB()

        def ewm(self, *a, **k):
            return _S()

    class _RB:
        def __getattr__(self, k):
            return self

        def mean(self, *a, **k):
            return _S()

        def sum(self, *a, **k):
            return _S()

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
        linalg=types.ModuleType("numpy.linalg"),
    )
    sys.modules["numpy"].linalg.solve = lambda A, b: [0.0] * len(b)
    sys.modules["numpy"].linalg.pinv = lambda A: []
    _mod(
        "pandas",
        DataFrame=_DF, read_parquet=lambda *a, **k: _DF(),
        Timestamp=lambda x: x, concat=lambda frames, *a, **k: frames[0] if frames else _DF(),
        date_range=lambda *a, **k: [], NA=None, isnull=lambda x: False,
        to_datetime=lambda x, *a, **k: x,
    )
    _mod("statsmodels")
    _mod("statsmodels.api", add_constant=lambda x: x)
    _mod("statsmodels.formula.api", ols=lambda *a, **k: None)
    _mod("scipy")
    _mod("scipy.stats")


def _fresh_mod(name):
    _mock_heavy()
    for mn in (name, "scripts.coupled_build_panel"):
        sys.modules.pop(mn, None)
    return importlib.import_module(name)


def _blocked_payload(script, reason_code=BLOCKED_RC, extra=None):
    base = {
        "status": "BLOCKED",
        "reason_code": reason_code,
        "outcomes_inspected": False,
        "canonical_outputs_mutated": False,
        "network": False,
        "writes_real_research_state": False,
        "script": script,
        "data_loaded_implicitly": False,
        "reads_parquet": False,
        "reads_outcomes": False,
        "outcomes_loaded": None,
    }
    if extra:
        base.update(extra)
    return base


def _real_go_manifest(month="2026-11"):
    return {
        "track": "A",
        "source_family": "ironflow_hyperliquid_liquidations",
        "venue": "hyperliquid",
        "source": "ironflow/hyperliquid-liquidations",
        "month": month,
        "unauthenticated": True,
        "requires_api_key": False,
        "requires_signature": False,
        "observed_liquidations": True,
        "modeled_or_proxy": False,
        "merges_non_hyperliquid": False,
        "label_definition": "observed_hyperliquid_liquidation_event_rows_from_ironflow",
        "timestamp_normalized_utc": True,
        "artifacts": {
            "events": {
                "path": f"research_state/data_cache/ironflow_events/events/{month}.parquet",
                "url": f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/{month}.parquet",
                "schema_fields": ["timestamp", "symbol", "notional_usd"],
            },
            "fills": {
                "path": f"research_state/data_cache/ironflow_events/fills/{month}.parquet",
                "url": f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/{month}.parquet",
                "schema_fields": ["timestamp", "symbol", "side", "notional_usd"],
            },
        },
    }


class Test128G1CoupledBuildPanelBlockedParity(unittest.TestCase):
    """G1: scripts/coupled_build_panel.py main() blocked-refusal parity:
    mock guarded_execute returns BLOCKED => rc=1, reason_code
    PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS, canonical_outputs_mutated=false,
    outcome loader never invoked, canonical snapshots unchanged."""

    def test_coupled_build_panel_blocked_loader_never_called(self):
        mod = _fresh_mod("scripts.coupled_build_panel")
        before = _snap([FRONTIER, RUN_MANIFEST, EVAL_FCLR010, CACHE])
        guard = _blocked_payload("coupled_build_panel",
                                 extra={"seam_go_prereg_required": True,
                                        "reason_code_detail": "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED"})
        loader_called = {"n": 0}

        def _boom_loader(*a, **k):
            loader_called["n"] += 1
            raise AssertionError("outcome loader must not run on coupled_build_panel BLOCKED branch")

        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=guard), \
             patch("scripts.coupled_build_panel._load_coupled_outcomes", _boom_loader), \
             redirect_stdout(io.StringIO()) as buf:
            rc = mod.main()
        p = _parse_json_stdout(buf)
        self.assertEqual(rc, 1, (rc, p))
        self.assertEqual(p.get("status"), "BLOCKED", p)
        self.assertEqual(p.get("reason_code"), BLOCKED_RC, p)
        self.assertEqual(p.get("script"), "coupled_build_panel", p)
        self.assertEqual(loader_called["n"], 0, loader_called)
        self.assertFalse(p.get("canonical_outputs_mutated"), p)
        self.assertFalse(p.get("outcomes_inspected"), p)
        self.assertFalse(p.get("network"), p)
        self.assertFalse(p.get("writes_real_research_state"), p)
        missing = REQ_REFUSAL - set(p.keys())
        self.assertFalse(missing, (missing, p))
        _unchanged([FRONTIER, RUN_MANIFEST, EVAL_FCLR010, CACHE], before)

    def test_coupled_build_panel_blocked_stable_refusal_shape(self):
        mod = _fresh_mod("scripts.coupled_build_panel")
        guard = _blocked_payload("coupled_build_panel")
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=guard), \
             redirect_stdout(io.StringIO()) as buf:
            rc = mod.main()
        p = _parse_json_stdout(buf)
        self.assertEqual(rc, 1)
        missing = REQ_REFUSAL - set(p.keys())
        self.assertFalse(missing, (missing, p))
        self.assertEqual(p["reason_code"], BLOCKED_RC)
        self.assertFalse(p["canonical_outputs_mutated"])


class Test128G2OperatorReportSeamWired(unittest.TestCase):
    """G2: scripts/tracka_operator_report.py compose_operator_report preserves
    stable seam-wired fields (admissible_seam_wired pass/status/reason_code/
    failures/month/fail_closed/network/reads_outcomes/reads_parquet) and
    drift-preflight-first fail-closed order; missing candidate => fail-closed
    NO-GO ADMISSIBLE_CANDIDATE_PATH_MISSING; dep-light, no real writes."""

    def test_compose_operator_report_no_candidate_seam_wired(self):
        from scripts.tracka_operator_report import compose_operator_report
        report = compose_operator_report(repo_root=REAL, admissible_candidate_path=None)
        self.assertTrue(report.get("pass"), report)
        self.assertTrue(report.get("drift_preflight", {}).get("pass") is True, report)
        gate = report.get("gate_decision", {})
        self.assertEqual(gate.get("status"), "BLOCKED", gate)
        self.assertEqual(gate.get("reason_code"), BLOCKED_RC, gate)
        self.assertEqual(gate.get("outcomes_inspected"), False, gate)
        self.assertEqual(report.get("fail_closed_order"), "drift_preflight->gate_decision->probe_invariant_state", report)
        seam = report.get("admissible_seam_wired", {})
        for k in ("pass", "status", "reason_code", "fail_closed",
                  "network", "reads_outcomes", "reads_parquet"):
            self.assertIn(k, seam, (k, seam))
        self.assertEqual(seam.get("status"), "NO_CANDIDATE_PENDING", seam)
        self.assertEqual(seam.get("reason_code"), "ADMISSIBLE_SEAM_WIRED_AWAITING_CANDIDATE", seam)
        self.assertTrue(seam.get("fail_closed"), seam)
        self.assertFalse(seam.get("network"), seam)
        self.assertFalse(seam.get("reads_outcomes"), seam)
        self.assertFalse(seam.get("reads_parquet"), seam)
        self.assertFalse(report.get("network"), report)
        self.assertFalse(report.get("writes_real_research_state"), report)
        self.assertTrue(report.get("read_only"), report)

    def test_compose_operator_report_missing_candidate_fail_closed(self):
        from scripts.tracka_operator_report import compose_operator_report
        report = compose_operator_report(repo_root=REAL, admissible_candidate_path="/nonexistent_tracka_candidate.json")
        self.assertTrue(report.get("drift_preflight", {}).get("pass") is True, report)  # drift first
        seam = report.get("admissible_seam_wired", {})
        self.assertEqual(seam.get("status"), "NO-GO", seam)
        self.assertEqual(seam.get("reason_code"), "ADMISSIBLE_CANDIDATE_PATH_MISSING", seam)
        self.assertTrue(seam.get("fail_closed"), seam)
        self.assertEqual(seam.get("failures"), ["candidate_path_missing_or_not_file"], seam)
        gate = report.get("gate_decision", {})
        self.assertEqual(gate.get("status"), "BLOCKED", gate)
        self.assertEqual(gate.get("reason_code"), "ADMISSIBLE_SEAM_NOGO_BEFORE_PREREG", gate)

    def test_compose_operator_report_go_manifest_seam(self):
        from scripts.tracka_operator_report import compose_operator_report
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(_real_go_manifest("2026-11"), f)
            p = f.name
        try:
            report = compose_operator_report(repo_root=REAL, admissible_candidate_path=p)
        finally:
            os.unlink(p)
        seam = report.get("admissible_seam_wired", {})
        self.assertEqual(seam.get("status"), "GO", seam)
        self.assertEqual(seam.get("reason_code"), "ADMISSIBLE_SEAM_GO", seam)
        self.assertEqual(seam.get("month"), "2026-11", seam)
        self.assertTrue(seam.get("fail_closed"), seam)
        self.assertFalse(seam.get("network"), seam)
        self.assertFalse(seam.get("reads_outcomes"), seam)
        self.assertFalse(seam.get("reads_parquet"), seam)
        gate = report.get("gate_decision", {})
        self.assertEqual(gate.get("status"), "BLOCKED", gate)  # prereg/data still absent -> blocked
        self.assertEqual(gate.get("reason_code"), BLOCKED_RC, gate)


class Test128G3RefusalMatrixExtension(unittest.TestCase):
    """G3: refusal-payload fail-closed matrix extended to coupled_build_panel
    and fclr010_execute_fast via guarded_execute mocks; assert
    canonical_outputs_mutated=false and canonical snapshots unchanged."""

    def test_coupled_build_panel_matrix_snapshots_unchanged(self):
        mod = _fresh_mod("scripts.coupled_build_panel")
        before = _snap([FRONTIER, RUN_MANIFEST, EVAL_FCLR010])
        guard = _blocked_payload("coupled_build_panel")
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=guard), \
             redirect_stdout(io.StringIO()) as buf:
            rc = mod.main()
        p = _parse_json_stdout(buf)
        self.assertEqual(rc, 1, (rc, p))
        self.assertEqual(p.get("script"), "coupled_build_panel", p)
        self.assertEqual(p.get("reason_code"), BLOCKED_RC, p)
        self.assertFalse(p.get("canonical_outputs_mutated"), p)
        self.assertFalse(p.get("outcomes_inspected"), p)
        _unchanged([FRONTIER, RUN_MANIFEST, EVAL_FCLR010], before)

    def test_fclr010_execute_fast_blocked_refusal_snapshots_unchanged(self):
        mod = _fresh_mod("scripts.fclr010_execute_fast")
        before = _snap([RUN_MANIFEST, OUT_SUM])
        guard = _blocked_payload("fclr010_execute_fast",
                                 extra={"seam_go_prereg_required": True,
                                        "reason_code_detail": "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED",
                                        "fast_path": True})
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=guard), \
             redirect_stdout(io.StringIO()) as buf:
            rc = mod.main()
        p = _parse_json_stdout(buf)
        self.assertEqual(rc, 1, (rc, p))
        self.assertEqual(p.get("status"), "BLOCKED", p)
        self.assertEqual(p.get("reason_code"), BLOCKED_RC, p)
        self.assertEqual(p.get("script"), "fclr010_execute_fast", p)
        self.assertFalse(p.get("canonical_outputs_mutated"), p)
        self.assertFalse(p.get("outcomes_inspected"), p)
        self.assertFalse(p.get("network"), p)
        self.assertFalse(p.get("writes_real_research_state"), p)
        missing = REQ_REFUSAL - set(p.keys())
        self.assertFalse(missing, (missing, p))
        _unchanged([RUN_MANIFEST, OUT_SUM], before)


if __name__ == "__main__":
    unittest.main()
