"""FCLR-NEXT-130: guarded_entry default/outcome-loader refusal contract (G1),
tracka_resume_gate CLI blocked-matrix parity (G2), and cross-entrypoint refusal
payload schema parity (G3).

Deterministic, tmp-isolated, dep-light, no network, no parquet/outcome reads,
no real research_state writes.
"""
from __future__ import annotations

import io
import json
import os
import re
import subprocess
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
COUPLED_CACHE = RS / ".cache" / "fclr_coupled_panel.parquet"
BLOCKED_RC = "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS"
REQ_REFUSAL = {
    "status", "outcomes_inspected", "canonical_outputs_mutated", "network",
    "writes_real_research_state", "script", "reason_code",
}
SAFE_FALSE = ("outcomes_inspected", "canonical_outputs_mutated", "network", "writes_real_research_state")


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
    assert m, f"no JSON in stdout: {buf.getvalue()!r}"
    return json.loads(m.group(0))


def _assert_no_outcome_read_flags(p):
    for k in SAFE_FALSE:
        assert p.get(k) is False, (k, p.get(k), p)
    assert p.get("reads_parquet") is False or p.get("reads_parquet") is None or k == "reads_parquet", None


def _assert_safe_no_io(p):
    for k in SAFE_FALSE:
        assert p.get(k) is False, (k, p.get(k), p)
    assert p.get("reads_parquet") in (False, None), p.get("reads_parquet")
    assert p.get("reads_outcomes") in (False, None), p.get("reads_outcomes")


def _mock_heavy():
    for mn in list(sys.modules):
        if mn == "numpy" or mn.startswith("numpy.") or mn == "pandas" or mn.startswith("pandas.") \
           or mn == "pyarrow" or mn.startswith("pyarrow.") or mn == "statsmodels" or mn.startswith("statsmodels.") \
           or mn == "scipy" or mn.startswith("scipy."):
            sys.modules.pop(mn, None)

    def _mod(name, **attrs):
        m = types.ModuleType(name)
        for k, v in attrs.items():
            setattr(m, k, v)
        sys.modules[name] = m
        return m

    class _DF:
        def __init__(self, *a, **k): pass
        def __len__(self): return 0
        @property
        def empty(self): return True
        def __getitem__(self, k): return _S()
        def __setitem__(self, k, v): pass
        def sort_values(self, *a, **k): return self
        def groupby(self, *a, **k): return _GB()
        def to_dict(self, *a, **k): return []
        def copy(self): return _DF()
        def dropna(self, *a, **k): return self
        def reset_index(self, *a, **k): return self
        def merge(self, *a, **k): return self
        def rename(self, *a, **k): return self
        def assign(self, *a, **k): return self
        def query(self, *a, **k): return self
        def iterrows(self): return iter([])
        @property
        def columns(self): return []
        @property
        def index(self): return []
        @property
        def shape(self): return (0, 0)
        @property
        def values(self): return []
        @property
        def iloc(self): return self
        @property
        def loc(self): return self
        def to_parquet(self, *a, **k): pass
        def to_csv(self, *a, **k): pass

    class _S:
        def nunique(self): return 0
        def sum(self): return 0
        def mean(self): return 0
        def std(self): return 0
        def min(self): return None
        def max(self): return None
        def count(self): return 0
        def __len__(self): return 0
        def __iter__(self): return iter([])
        def values(self): return []
        @property
        def empty(self): return True

    class _GB:
        def __getattr__(self, k): return self
        def __call__(self, *a, **k): return self
        def shift(self, *a, **k): return _S()
        def rolling(self, *a, **k): return _GB()
        def ewm(self, *a, **k): return _GB()
        def mean(self, *a, **k): return _S()
        def sum(self, *a, **k): return _S()
        def apply(self, *a, **k): return _S()
        def agg(self, *a, **k): return _DF()
        def transform(self, *a, **k): return _S()
        def first(self, *a, **k): return _DF()
        def last(self, *a, **k): return _DF()

    class _TS:
        def __init__(self, *a, **k): pass
        def __call__(self, *a, **k): return _TS()

    _mod("numpy", nan=float("nan"), isnan=lambda x: False, isinf=lambda x: False,
         float64=float, int64=int, ones=lambda n, *a, **k: [0.0] * int(n),
         array=lambda x, *a, **k: list(x) if hasattr(x, "__iter__") else [x],
         sign=lambda x: 0, clip=lambda x, *a, **k: x, log1p=lambda x: x,
         maximum=lambda a, b: a, minimum=lambda a, b: a, quantile=lambda x, q: 0.0,
         exp=lambda x: 1.0, column_stack=lambda cols: cols, zeros=lambda *a, **k: [0.0],
         mean=lambda x, *a, **k: 0.0, sum=lambda x, *a, **k: 0, abs=lambda x: x,
         diff=lambda x, *a, **k: [], sqrt=lambda x: 1.0, where=lambda c, a, b: a,
         unique=lambda x: [], argsort=lambda x: [], percentile=lambda x, q: 0.0,
         median=lambda x: 0.0, random=types.SimpleNamespace(seed=lambda *a: None, normal=lambda *a, **k: [0.0]),
         linalg=types.SimpleNamespace(solve=lambda A, b: [0.0] * len(b), pinv=lambda A: []),
         ndarray=list, float_=float, int_=int, bool_=bool)
    _mod("pandas", DataFrame=_DF, Series=_S, read_parquet=lambda *a, **k: _DF(),
         read_csv=lambda *a, **k: _DF(), to_datetime=lambda x, *a, **k: x,
         concat=lambda *a, **k: _DF(), merge=lambda *a, **k: _DF(),
         Timestamp=_TS, Timedelta=lambda *a, **k: None, isna=lambda x: False,
         notna=lambda x: True, NA=None, NaT=None)
    _mod("pyarrow")
    _mod("pyarrow.parquet", read_table=lambda *a, **k: (_ for _ in ()).throw(AssertionError("parquet read forbidden on blocked/contract path")),
         write_table=lambda *a, **k: (_ for _ in ()).throw(AssertionError("parquet write forbidden")))
    _mod("statsmodels"); _mod("statsmodels.api", OLS=lambda *a, **k: None, Logit=lambda *a, **k: None, add_constant=lambda x: x)
    _mod("statsmodels.formula", api=types.SimpleNamespace(ols=lambda *a, **k: None, logit=lambda *a, **k: None))
    _mod("statsmodels.formula.api", ols=lambda *a, **k: None, logit=lambda *a, **k: None)
    _mod("scipy"); _mod("scipy.stats", norm=types.SimpleNamespace(cdf=lambda x: 0.5), ttest_ind=lambda *a, **k: (0, 1))


def _fresh(name):
    _mock_heavy()
    for mn in list(sys.modules):
        if mn == name or mn.startswith("scripts."):
            sys.modules.pop(mn, None)
    return importlib.import_module(name)


import importlib  # after helpers


class Test130G1GuardedEntryLoaderContract(unittest.TestCase):
    """G1: guarded_execute/loader refusal & safe contract (no parquet/outcome reads)."""

    def _ready_no_load(self):
        # READY_FROZEN but harness reports no implicit load / explicit loader required.
        return {
            "status": "READY_FROZEN",
            "outcomes_inspected": False,
            "data_loaded_implicitly": False,
            "data_load_mode": "EXPLICIT_LOADER_REQUIRED_NO_IMPLICIT_PARQUET_READ",
            "reads_parquet": False,
            "reads_outcomes": False,
            "outcomes_loaded": None,
        }

    def test_ready_path_absent_loader_and_no_default_loader_is_safe_no_parquet_read(self):
        from scripts import fclr010_guarded_entry as ge
        with patch.object(ge, "FCLR010Harness") as H:
            H.return_value.execute_ready_data_load.return_value = self._ready_no_load()
            r = ge.guarded_execute(
                data_path=Path("/tmp/d"), pre_reg_path=Path("/tmp/p"),
                outcome_loader=None, allow_default_loader=False,
            )
        _assert_safe_no_io(r)
        assert r.get("status") in ("READY_FROZEN", "BLOCKED"), r
        # no loader invoked => no outcomes loaded
        assert r.get("outcomes_loaded") in (None, False), r
        assert r.get("canonical_outputs_mutated") is False
        assert r.get("network") is False
        assert r.get("writes_real_research_state") is False

    def test_loader_raises_fail_closed_no_parquet_outcome_reads(self):
        from scripts import fclr010_guarded_entry as ge

        def boom(*a, **k):
            raise RuntimeError("loader boom")

        # Exercise harness contract via guarded_execute: harness returns BLOCKED-on-loader-fail
        with patch.object(ge, "FCLR010Harness") as H:
            H.return_value.execute_ready_data_load.return_value = {
                "status": "BLOCKED",
                "reason": "outcome_loader failed: RuntimeError('boom')",
                "outcomes_inspected": False,
                "reads_parquet": False,
                "reads_outcomes": False,
                "outcomes_loaded": None,
            }
            r = ge.guarded_execute(
                data_path=Path("/tmp/d"), pre_reg_path=Path("/tmp/p"),
                outcome_loader=boom, allow_default_loader=False,
            )
        assert r.get("status") == "BLOCKED", r
        assert r.get("reason_code") == BLOCKED_RC, r
        _assert_safe_no_io(r)
        assert "outcome_loader" in (r.get("reason") or ""), r

    def test_loader_invalid_payload_shape_fail_closed_no_outcome_inspection_claim(self):
        from scripts import fclr010_guarded_entry as ge
        # invalid/non-dict payload surfaced as BLOCKED by guarded contract
        with patch.object(ge, "FCLR010Harness") as H:
            H.return_value.execute_ready_data_load.return_value = {
                "status": "BLOCKED",
                "reason": "outcome_loader failed: invalid payload shape",
                "outcomes_inspected": False,
                "reads_parquet": False,
                "reads_outcomes": False,
                "outcomes_loaded": None,
            }
            r = ge.guarded_execute(
                data_path=Path("/tmp/d"), pre_reg_path=Path("/tmp/p"),
                outcome_loader=lambda *a, **k: "not-a-dict",
                allow_default_loader=False,
            )
        assert r.get("status") == "BLOCKED", r
        assert r.get("reason_code") == BLOCKED_RC, r
        _assert_safe_no_io(r)

    def test_default_loader_never_used_when_not_explicitly_enabled_on_ready_path(self):
        from scripts import fclr010_guarded_entry as ge
        with patch.object(ge, "_default_outcome_loader") as dl:
            dl.side_effect = AssertionError("default loader must not run")
            with patch.object(ge, "FCLR010Harness") as H:
                H.return_value.execute_ready_data_load.return_value = self._ready_no_load()
                r = ge.guarded_execute(
                    data_path=Path("/tmp/d"), pre_reg_path=Path("/tmp/p"),
                    outcome_loader=None, allow_default_loader=False,
                )
        assert dl.call_count == 0
        _assert_safe_no_io(r)


class Test130G2ResumeGateCLIMatrix(unittest.TestCase):
    """G2: tracka_resume_gate CLI blocked-matrix parity."""

    def _run(self, args):
        return subprocess.run(
            [sys.executable, "scripts/tracka_resume_gate.py"] + args,
            capture_output=True, text=True, cwd=str(REAL),
        )

    def test_missing_prereg_fail_closed_stable(self):
        r = self._run(["--prereg", "/nonexistent_prereg_130.json"])
        self.assertNotEqual(r.returncode, 0)
        o = json.loads(r.stdout)
        self.assertEqual(o["status"], "BLOCKED")
        self.assertEqual(o["reason_code"], BLOCKED_RC)
        self.assertEqual(o["fail_closed_order"], "drift_preflight->manifest_prereg")
        self.assertFalse(o["outcomes_inspected"])
        self.assertFalse(o.get("network", False))
        self.assertFalse(o.get("writes_real_research_state", False))

    def test_malformed_prereg_fixture_fail_closed_no_outcomes(self):
        with tempfile.TemporaryDirectory() as td:
            pr = Path(td) / "bad.json"
            pr.write_text("not json {{{")
            r = self._run(["--prereg", str(pr), "--json"])
        self.assertNotEqual(r.returncode, 0)
        # existing path may treat malformed/nonexistent-shaped prereg as blocked; must be machine-readable no-outcomes refusal.
        o = json.loads(r.stdout)
        self.assertEqual(o["status"], "BLOCKED")
        self.assertFalse(o.get("outcomes_inspected", False))
        self.assertFalse(o.get("network", False))
        self.assertFalse(o.get("writes_real_research_state", False))

    def test_malformed_manifest_fixture_fail_closed_no_outcomes(self):
        with tempfile.TemporaryDirectory() as td:
            mf = Path(td) / "mf.json"
            mf.write_text("{broken")
            r = self._run(["--manifest", str(mf), "--json"])
        self.assertNotEqual(r.returncode, 0)
        o = json.loads(r.stdout)
        self.assertEqual(o["status"], "BLOCKED")
        self.assertFalse(o.get("outcomes_inspected", False))
        self.assertFalse(o.get("network", False))
        self.assertFalse(o.get("writes_real_research_state", False))
        self.assertEqual(o.get("reason_code"), BLOCKED_RC)

    def test_valid_prereg_missing_data_fail_closed_no_network_writes(self):
        with tempfile.TemporaryDirectory() as td:
            pr = Path(td) / "prereg.json"
            pr.write_text(json.dumps({"frozen": True, "config": {"experiment_id": "x"}}))
            data = Path(td) / "no_such_data"
            r = self._run(["--prereg", str(pr), "--data", str(data), "--json"])
        self.assertNotEqual(r.returncode, 0)
        o = json.loads(r.stdout)
        self.assertEqual(o["status"], "BLOCKED")
        self.assertEqual(o["reason_code"], BLOCKED_RC)
        self.assertEqual(o["fail_closed_order"], "drift_preflight->manifest_prereg")
        self.assertFalse(o["outcomes_inspected"])
        self.assertFalse(o.get("network", False))
        self.assertFalse(o.get("writes_real_research_state", False))
        self.assertFalse(o.get("reads_parquet", False))
        self.assertFalse(o.get("reads_outcomes", False))


G3_SPECS = [
    ("scripts.coupled_build_panel", "coupled_build_panel", [FRONTIER, RUN_MANIFEST, EVAL_FCLR010, COUPLED_CACHE],
     [("scripts.coupled_build_panel._load_coupled_outcomes", None)]),
    ("scripts.fclr010_execute_fast", "fclr010_execute_fast", [RUN_MANIFEST, EVAL_FCLR010], []),
    ("scripts.run_liqmicro", "run_liqmicro", [FRONTIER, RUN_MANIFEST],
     [("scripts.run_liqmicro._load_liqmicro_outcomes", None)]),
    ("scripts.run_liqmicro_v2", "run_liqmicro_v2", [FRONTIER, RUN_MANIFEST],
     [("scripts.run_liqmicro_v2._load_liqmicro_v2_outcomes", None)]),
    ("scripts.fclr010_coverage_audit", "fclr010_coverage_audit", [FRONTIER, RUN_MANIFEST, EVAL_FCLR010],
     [("scripts.fclr010_coverage_audit._load_coverage_outcomes", None)]),
    ("scripts.liqmicro_audit", "liqmicro_audit", [FRONTIER, RUN_MANIFEST],
     [("scripts.liqmicro_audit._load_liqmicro_outcomes", None)]),
    ("scripts.fclr010_execute", "fclr010_execute", [RUN_MANIFEST, EVAL_FCLR010],
     [("scripts.fclr010_execute._load_outcomes_guarded", None), ("scripts.fclr010_execute._load_outcomes", None)]),
    ("scripts.coupled_robust_eval", "coupled_robust_eval", [FRONTIER, RUN_MANIFEST, EVAL_FCLR010],
     [("scripts.coupled_build_panel._load_coupled_outcomes", None)]),
    ("scripts.overlay_quick", "overlay_quick", [FRONTIER, RUN_MANIFEST, EVAL_FCLR010],
     [("scripts.coupled_build_panel._load_coupled_outcomes", None)]),
    ("scripts.overlay_tracka_execute", "overlay_tracka_execute", [FRONTIER, RUN_MANIFEST, EVAL_FCLR010],
     [("scripts.coupled_build_panel._load_coupled_outcomes", None)]),
]


def _blocked_guard(script):
    return {
        "status": "BLOCKED", "reason_code": BLOCKED_RC,
        "reason": "blocked", "outcomes_inspected": False,
        "canonical_outputs_mutated": False, "network": False,
        "writes_real_research_state": False, "reads_parquet": False,
        "reads_outcomes": False, "guarded_execution_contract": "fclr_next_111",
        "script": script,
    }


class Test130G3RefusalPayloadSchemaParity(unittest.TestCase):
    """G3: all 10 guarded entrypoints emit stable refusal payload schema on BLOCKED."""

    def test_all_guarded_entrypoints_blocked_payload_schema_parity(self):
        self.assertEqual(len(G3_SPECS), 10)
        for modname, script, snaps, loader_patches in G3_SPECS:
            with self.subTest(script=script):
                mod = _fresh(modname)
                before = _snap(snaps)
                guard = _blocked_guard(script)

                def boom(*a, **k):
                    raise AssertionError(f"loader must not run for {script}")

                patches = [patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=guard)]
                for tgt, _ in loader_patches:
                    patches.append(patch(tgt, boom))
                try:
                    for p in patches:
                        p.start()
                    with redirect_stdout(io.StringIO()) as buf:
                        rc = mod.main()
                finally:
                    for p in reversed(patches):
                        p.stop()
                self.assertEqual(rc, 1, (script, buf.getvalue()[:300]))
                payload = _parse_json_stdout(buf)
                missing = REQ_REFUSAL - set(payload.keys())
                self.assertFalse(missing, (script, missing, payload))
                self.assertEqual(payload["status"], "BLOCKED", (script, payload))
                self.assertEqual(payload["reason_code"], BLOCKED_RC, (script, payload))
                for k in SAFE_FALSE:
                    self.assertIs(payload.get(k), False, (script, k, payload))
                self.assertIsInstance(payload["status"], str)
                self.assertIsInstance(payload["reason_code"], str)
                for k in SAFE_FALSE:
                    self.assertIsInstance(payload[k], bool, (script, k))
                _unchanged(snaps, before)


if __name__ == "__main__":
    unittest.main()
