"""FCLR-NEXT-129: fused Track A blocked-branch refusal matrix (G1) +
operator CLI parity (G2) + registry drift fails closed (G3).

Deterministic, tmp-isolated, no network, no parquet/outcome reads,
no real research_state writes. Dep-light: heavy deps stubbed.
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
COUPLED_CACHE = RS / ".cache" / "fclr_coupled_panel.parquet"
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
    # purge heavy modules so our stubs take effect
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

    np = _mod(
        "numpy",
        nan=float("nan"), isnan=lambda x: False, isinf=lambda x: False,
        float64=float, int64=int, ones=lambda n, *a, **k: [0.0] * int(n),
        array=lambda x, *a, **k: list(x) if hasattr(x, "__iter__") else [x],
        sign=lambda x: 0, clip=lambda x, *a, **k: x, log1p=lambda x: x,
        maximum=lambda a, b: a, minimum=lambda a, b: a,
        quantile=lambda x, q: 0.0, exp=lambda x: 1.0,
        column_stack=lambda cols: cols, zeros=lambda *a, **k: [0.0] * (a[0] if a else 0),
        mean=lambda x, *a, **k: 0.0, sum=lambda x, *a, **k: 0,
        abs=lambda x: x, diff=lambda x, *a, **k: [], sqrt=lambda x: 1.0,
        where=lambda c, a, b: a, unique=lambda x: [], argsort=lambda x: [],
        percentile=lambda x, q: 0.0, median=lambda x: 0.0,
        random=types.SimpleNamespace(seed=lambda *a: None, normal=lambda *a, **k: [0.0]),
        linalg=types.SimpleNamespace(solve=lambda A, b: [0.0] * len(b), pinv=lambda A: []),
        ndarray=list, float_=float, int_=int, bool_=bool,
    )
    _mod("pandas", DataFrame=_DF, Series=_S, read_parquet=lambda *a, **k: _DF(),
         read_csv=lambda *a, **k: _DF(), to_datetime=lambda x, *a, **k: x,
         concat=lambda *a, **k: _DF(), merge=lambda *a, **k: _DF(),
         Timestamp=lambda *a, **k: None, Timedelta=lambda *a, **k: None,
         isna=lambda x: False, notna=lambda x: True, NA=None, NaT=None)
    _mod("pyarrow")
    _mod("pyarrow.parquet", read_table=lambda *a, **k: None, write_table=lambda *a, **k: None)
    _mod("statsmodels")
    _mod("statsmodels.api", OLS=lambda *a, **k: None, Logit=lambda *a, **k: None, add_constant=lambda x: x)
    _mod("statsmodels.formula", api=types.SimpleNamespace(ols=lambda *a, **k: None, logit=lambda *a, **k: None))
    _mod("statsmodels.formula.api", ols=lambda *a, **k: None, logit=lambda *a, **k: None)
    _mod("scipy")
    _mod("scipy.stats", norm=types.SimpleNamespace(cdf=lambda x: 0.5), ttest_ind=lambda *a, **k: (0, 1))


def _fresh(name):
    _mock_heavy()
    for mn in list(sys.modules):
        if mn == name or mn.startswith("scripts."):
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
        "reads_outcomes": False,
        "reads_parquet": False,
    }
    if extra:
        base.update(extra)
    return base


def _assert_refusal(p, script):
    assert p.get("status") == "BLOCKED", p
    assert p.get("reason_code") == BLOCKED_RC, p
    assert p.get("canonical_outputs_mutated") is False, p
    assert p.get("outcomes_inspected") is False, p
    assert p.get("network") is False, p
    assert p.get("writes_real_research_state") is False, p
    missing = REQ_REFUSAL - set(p.keys())
    assert not missing, (missing, p)


G1_SPECS = [
    # (module, script_name, snapshot_paths, loader_patch_targets)
    ("scripts.coupled_build_panel", "coupled_build_panel",
     [FRONTIER, RUN_MANIFEST, EVAL_FCLR010, COUPLED_CACHE],
     [("scripts.coupled_build_panel._load_coupled_outcomes", None)]),
    ("scripts.fclr010_execute_fast", "fclr010_execute_fast",
     [RUN_MANIFEST, EVAL_FCLR010],
     []),
    ("scripts.run_liqmicro", "run_liqmicro",
     [FRONTIER, RUN_MANIFEST],
     [("scripts.run_liqmicro._load_liqmicro_outcomes", None)]),
    ("scripts.run_liqmicro_v2", "run_liqmicro_v2",
     [FRONTIER, RUN_MANIFEST],
     [("scripts.run_liqmicro_v2._load_liqmicro_v2_outcomes", None)]),
    ("scripts.fclr010_coverage_audit", "fclr010_coverage_audit",
     [FRONTIER, RUN_MANIFEST, EVAL_FCLR010],
     [("scripts.fclr010_coverage_audit._load_coverage_outcomes", None)]),
    ("scripts.liqmicro_audit", "liqmicro_audit",
     [FRONTIER, RUN_MANIFEST],
     [("scripts.liqmicro_audit._load_liqmicro_outcomes", None)]),
    # regression anchors
    ("scripts.fclr010_execute", "fclr010_execute",
     [RUN_MANIFEST, EVAL_FCLR010],
     [("scripts.fclr010_execute._load_outcomes_guarded", None),
      ("scripts.fclr010_execute._load_outcomes", None)]),
    ("scripts.coupled_robust_eval", "coupled_robust_eval",
     [FRONTIER, RUN_MANIFEST, EVAL_FCLR010],
     [("scripts.coupled_build_panel._load_coupled_outcomes", None)]),
    ("scripts.overlay_quick", "overlay_quick",
     [FRONTIER, RUN_MANIFEST, EVAL_FCLR010],
     [("scripts.coupled_build_panel._load_coupled_outcomes", None)]),
    ("scripts.overlay_tracka_execute", "overlay_tracka_execute",
     [FRONTIER, RUN_MANIFEST, EVAL_FCLR010],
     [("scripts.coupled_build_panel._load_coupled_outcomes", None)]),
]


class Test129G1FusedRefusalMatrix(unittest.TestCase):
    """G1: every guarded Track A entrypoint refuses fail-closed on BLOCKED guard."""

    def test_all_guarded_entrypoints_blocked_matrix(self):
        self.assertEqual(len(G1_SPECS), 10, "matrix must include all 10 named entrypoints")
        for modname, script, snaps, loader_patches in G1_SPECS:
            with self.subTest(script=script):
                mod = _fresh(modname)
                before = _snap(snaps)
                guard = _blocked_payload(script)
                loader_called = {"n": 0}

                def _boom(*a, _lc=loader_called, **k):
                    _lc["n"] += 1
                    raise AssertionError(f"outcome loader must not run on {script} BLOCKED")

                patches = [patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=guard)]
                for tgt, _ in loader_patches:
                    patches.append(patch(tgt, _boom))
                ctxs = [p.__enter__() for p in patches]
                try:
                    with redirect_stdout(io.StringIO()) as buf:
                        rc = mod.main()
                finally:
                    for p in reversed(patches):
                        p.__exit__(None, None, None)
                self.assertEqual(rc, 1, (script, rc, buf.getvalue()[:400]))
                payload = _parse_json_stdout(buf)
                _assert_refusal(payload, script)
                self.assertEqual(loader_called["n"], 0, (script, loader_called))
                _unchanged(snaps, before)


def _real_go_manifest(month="2026-11"):
    return {
        "track": "A", "source_family": "ironflow_hyperliquid_liquidations",
        "venue": "hyperliquid", "source": "ironflow/hyperliquid-liquidations",
        "month": month, "unauthenticated": True, "requires_api_key": False,
        "requires_signature": False, "observed_liquidations": True,
        "modeled_or_proxy": False, "merges_non_hyperliquid": False,
        "label_definition": "observed_hyperliquid_liquidation_event_rows_from_ironflow",
        "timestamp_normalized_utc": True,
        "artifacts": {
            "events": {"path": f"research_state/data_cache/ironflow_events/events/{month}.parquet",
                       "url": f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/{month}.parquet",
                       "schema_fields": ["timestamp", "symbol", "notional_usd"]},
            "fills": {"path": f"research_state/data_cache/ironflow_events/fills/{month}.parquet",
                      "url": f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/{month}.parquet",
                      "schema_fields": ["timestamp", "symbol", "side", "notional_usd"]},
        },
    }


class Test129G2OperatorCLIParity(unittest.TestCase):
    """G2: tracka_operator_report CLI exit-code + JSON + drift-first + admissible passthrough."""

    def test_cli_blocked_exit1_stable_json_drift_first(self):
        from scripts.tracka_operator_report import main
        with redirect_stdout(io.StringIO()) as buf:
            rc = main(["--json"])
        self.assertEqual(rc, 1)
        r = json.loads(buf.getvalue())
        self.assertTrue(r.get("drift_preflight", {}).get("pass") is True, r)
        self.assertEqual(r.get("fail_closed_order"),
                         "drift_preflight->gate_decision->probe_invariant_state", r)
        self.assertEqual(r.get("gate_decision", {}).get("reason_code"), BLOCKED_RC, r)
        seam = r.get("admissible_seam_wired", {})
        for k in ("pass", "status", "reason_code", "failures", "month", "fail_closed",
                  "network", "reads_outcomes", "reads_parquet"):
            self.assertIn(k, seam, (k, seam))
        self.assertFalse(r.get("network"))
        self.assertFalse(r.get("writes_real_research_state"))
        self.assertTrue(r.get("read_only"))

    def test_cli_missing_admissible_manifest_fail_closed_nogo(self):
        from scripts.tracka_operator_report import main
        with redirect_stdout(io.StringIO()) as buf:
            rc = main(["--json", "--admissible-manifest", "/nonexistent_tracka_candidate.json"])
        self.assertEqual(rc, 1)
        r = json.loads(buf.getvalue())
        self.assertTrue(r.get("drift_preflight", {}).get("pass") is True, r)
        seam = r.get("admissible_seam_wired", {})
        self.assertEqual(seam.get("status"), "NO-GO", seam)
        self.assertEqual(seam.get("reason_code"), "ADMISSIBLE_CANDIDATE_PATH_MISSING", seam)
        self.assertTrue(seam.get("fail_closed"), seam)

    def test_cli_go_manifest_seam_passthrough(self):
        from scripts.tracka_operator_report import main
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(_real_go_manifest("2026-11"), f)
            p = f.name
        try:
            with redirect_stdout(io.StringIO()) as buf:
                rc = main(["--json", "--admissible-manifest", p])
        finally:
            os.unlink(p)
        self.assertEqual(rc, 1)  # prereg/data absent => still blocked
        r = json.loads(buf.getvalue())
        seam = r.get("admissible_seam_wired", {})
        self.assertEqual(seam.get("status"), "GO", seam)
        self.assertEqual(seam.get("reason_code"), "ADMISSIBLE_SEAM_GO", seam)
        self.assertEqual(seam.get("month"), "2026-11", seam)
        self.assertFalse(seam.get("network"))
        self.assertFalse(seam.get("reads_outcomes"))
        self.assertFalse(seam.get("reads_parquet"))


class Test129G3RegistryDriftFailsClosed(unittest.TestCase):
    """G3: check_tracka_scope_registry_drift fails closed on script/registry drift."""

    def _base_repo(self):
        tmp = Path(tempfile.mkdtemp())
        (tmp / "scripts").mkdir()
        (tmp / "research_state").mkdir()
        # minimal passing script
        (tmp / "scripts" / "ok.py").write_text("def main():\n    return 0\n")
        reg = {
            "schema_version": "1", "allowed_classes": [
                "repo_maintenance_utility", "unclassified_auxiliary",
                "guarded_tracka_ready_writing", "track_c_sealed_volatility",
            ],
            "scripts": {"ok.py": {"class": "repo_maintenance_utility", "reason": "0123456789abcdefghi"}},
        }
        (tmp / "research_state" / "tracka_script_scope_registry.json").write_text(json.dumps(reg))
        return tmp, reg

    def test_fails_on_unregistered_added_script(self):
        from scripts.check_tracka_scope_registry_drift import check_drift
        tmp, _ = self._base_repo()
        try:
            (tmp / "scripts" / "new_unregistered.py").write_text("x=1\n")
            r = check_drift(repo=tmp)
            self.assertFalse(r["pass"], r)
            self.assertEqual(r["reason_code"], "SCOPE_REGISTRY_DRIFT", r)
            self.assertTrue(any("MISSING_IN_REGISTRY" in f for f in r["failures"]), r)
            self.assertFalse(r["network"])
            self.assertFalse(r["writes_real_research_state"])
        finally:
            import shutil; shutil.rmtree(tmp)

    def test_fails_on_malformed_entry(self):
        from scripts.check_tracka_scope_registry_drift import check_drift
        tmp, reg = self._base_repo()
        try:
            reg["scripts"]["ok.py"] = {"class": "NOT_A_REAL_CLASS", "reason": "0123456789abcdefghi"}
            (tmp / "research_state" / "tracka_script_scope_registry.json").write_text(json.dumps(reg))
            r = check_drift(repo=tmp)
            self.assertFalse(r["pass"], r)
            self.assertTrue(any("BAD_ENTRIES" in f or "bad" in str(f).lower() for f in r["failures"] + r["bad_entries"]), r)
        finally:
            import shutil; shutil.rmtree(tmp)

    def test_fails_on_eval_summary_writer_left_unclassified_auxiliary(self):
        from scripts.check_tracka_scope_registry_drift import check_drift
        tmp, reg = self._base_repo()
        try:
            # script that writes an evaluation_summary file but is unclassified_auxiliary
            (tmp / "scripts" / "writer.py").write_text(
                'from pathlib import Path\n'
                'def main():\n'
                '    Path("research_state/evaluation_summary_test.md").write_text("x")\n'
            )
            reg["scripts"]["writer.py"] = {"class": "unclassified_auxiliary", "reason": "0123456789abcdefghi"}
            (tmp / "research_state" / "tracka_script_scope_registry.json").write_text(json.dumps(reg))
            r = check_drift(repo=tmp)
            self.assertFalse(r["pass"], r)
            self.assertTrue(r["bad_entries"] or r["failures"], r)
        finally:
            import shutil; shutil.rmtree(tmp)

    def test_real_repo_passes(self):
        from scripts.check_tracka_scope_registry_drift import check_drift
        r = check_drift(repo=REAL)
        self.assertTrue(r["pass"], (r["failures"], r["bad_entries"][:5]))


if __name__ == "__main__":
    unittest.main()
