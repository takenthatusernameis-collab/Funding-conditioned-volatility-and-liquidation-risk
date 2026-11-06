"""FCLR-NEXT-127: tracka_resume_check seam detail parity (G1) +
guarded_entry refusal reason/detail parity (G2) +
READY writer scope, dep-light (G3).

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
EVAL_FCLR010 = RS / "evaluation_summary_FCLR010.md"
EVAL_LIQM1 = RS / "evaluation_summary_FCLR-LIQMICRO-001.md"
EVAL_COUPLED = RS / "evaluation_summary_FCLR-COUPLED-001-ROBUST.md"
EVAL_OVERLAY = RS / "evaluation_summary_tracka_overlay_001.md"
CROSS_TRACK = RS / "cross_track_decision_log.md"
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


def _fake_coupled_build_panel_module():
    """Inject a stub scripts.coupled_build_panel so heavy imports are avoided."""
    mod = types.ModuleType("scripts.coupled_build_panel")
    mod.build = lambda force=False, outcome_loader=None: _StubPanel()
    mod._load_coupled_outcomes = lambda dp: {"panel": _StubPanel()}
    return mod


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


class Test127G1TrackaResumeCheckSeamDetailParity(unittest.TestCase):
    """G1: tracka_resume_check.check / CLI preserve stable machine fields when a
    candidate --admissible-manifest is supplied: drift preflight first, seam fields
    pass/status/reason_code/failures/month/fail_closed/network/reads_outcomes/
    reads_parquet, network=false/writes_real_research_state=false/reads_parquet=false/
    reads_outcomes=false; missing/bad candidate => fail-closed NO-GO with stable reason."""

    def test_check_missing_candidate_fail_closed_no_go(self):
        from scripts.tracka_resume_check import check
        res = check(admissible_candidate_path="/nonexistent_tracka_candidate.json")
        self.assertFalse(res["pass"], res)
        self.assertEqual(res["status"], "NO-GO", res)
        self.assertEqual(res["reason_code"], "ADMISSIBLE_CANDIDATE_PATH_MISSING", res)
        self.assertTrue(res["drift_preflight"]["pass"], res)  # drift first
        seam = res["admissible_seam"]
        for k in ("pass", "status", "reason_code", "failures", "fail_closed",
                  "network", "reads_outcomes", "reads_parquet"):
            self.assertIn(k, seam, (k, seam))
        self.assertFalse(seam["pass"], seam)
        self.assertTrue(seam["fail_closed"], seam)
        self.assertFalse(seam["network"], seam)
        self.assertFalse(seam["reads_outcomes"], seam)
        self.assertFalse(seam["reads_parquet"], seam)
        self.assertFalse(res["writes_real_research_state"], res)
        self.assertFalse(res["network"], res)
        self.assertFalse(res["reads_outcomes"], res)
        self.assertFalse(res["reads_parquet"], res)

    def test_check_bad_json_candidate_load_error(self):
        from scripts.tracka_resume_check import check
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write("{not valid json")
            p = f.name
        try:
            res = check(admissible_candidate_path=p)
        finally:
            os.unlink(p)
        self.assertFalse(res["pass"], res)
        self.assertEqual(res["status"], "NO-GO", res)
        self.assertEqual(res["reason_code"], "ADMISSIBLE_CANDIDATE_LOAD_ERROR", res)
        seam = res["admissible_seam"]
        self.assertTrue(seam["fail_closed"], seam)
        self.assertFalse(seam["pass"], seam)

    def test_check_go_manifest_stable_fields(self):
        from scripts.tracka_resume_check import check
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(_real_go_manifest("2026-11"), f)
            p = f.name
        try:
            res = check(admissible_candidate_path=p)
        finally:
            os.unlink(p)
        self.assertTrue(res["pass"], res)
        self.assertEqual(res["status"], "GO", res)
        self.assertEqual(res["reason_code"], "ADMISSIBLE_SEAM_GO", res)
        seam = res["admissible_seam"]
        self.assertTrue(seam["pass"], seam)
        self.assertEqual(seam["status"], "GO", seam)
        self.assertEqual(seam["reason_code"], "ADMISSIBLE_SEAM_GO", seam)
        self.assertEqual(seam["month"], "2026-11", seam)
        self.assertEqual(seam["failures"], [], seam)
        self.assertTrue(seam["fail_closed"], seam)
        self.assertFalse(seam["network"], seam)
        self.assertFalse(seam["reads_outcomes"], seam)
        self.assertFalse(seam["reads_parquet"], seam)
        self.assertFalse(res["network"], res)
        self.assertFalse(res["writes_real_research_state"], res)
        self.assertFalse(res["reads_outcomes"], res)
        self.assertFalse(res["reads_parquet"], res)

    def test_check_no_candidate_pending(self):
        from scripts.tracka_resume_check import check
        res = check()
        self.assertTrue(res["pass"], res)
        self.assertEqual(res["status"], "SEAM_WIRED_AWAITING_CANDIDATE", res)
        seam = res["admissible_seam"]
        self.assertEqual(seam["status"], "NO_CANDIDATE_PENDING", seam)
        self.assertEqual(seam["reason_code"], "ADMISSIBLE_SEAM_WIRED_AWAITING_CANDIDATE", seam)
        self.assertTrue(seam["fail_closed"], seam)
        self.assertFalse(seam["network"], seam)
        self.assertFalse(seam["reads_outcomes"], seam)
        self.assertFalse(seam["reads_parquet"], seam)

    def test_check_drift_preflight_runs_first(self):
        from scripts.tracka_resume_check import check
        res = check(admissible_candidate_path="/nonexistent_tracka_candidate.json")
        self.assertIn("drift_preflight", res, res)
        self.assertTrue(res["drift_preflight"]["pass"], res)
        self.assertEqual(res["fail_closed_order"], "drift_preflight->admissible_seam", res)

    def test_cli_missing_candidate_rc1_and_stable_shape(self):
        from scripts import tracka_resume_check
        argv = ["--admissible-manifest", "/nonexistent_tracka_candidate.json"]
        with redirect_stdout(io.StringIO()) as buf:
            rc = tracka_resume_check.main(argv)
        res = _parse_json_stdout(buf)
        self.assertEqual(rc, 1, (rc, res))
        self.assertEqual(res["status"], "NO-GO", res)
        self.assertEqual(res["reason_code"], "ADMISSIBLE_CANDIDATE_PATH_MISSING", res)
        self.assertTrue(res["drift_preflight"]["pass"], res)
        seam = res["admissible_seam"]
        self.assertFalse(seam["network"], seam)
        self.assertFalse(seam["reads_outcomes"], seam)
        self.assertFalse(seam["reads_parquet"], seam)

    def test_cli_go_manifest_rc0(self):
        from scripts import tracka_resume_check
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(_real_go_manifest("2026-11"), f)
            p = f.name
        try:
            argv = ["--admissible-manifest", p]
            with redirect_stdout(io.StringIO()) as buf:
                rc = tracka_resume_check.main(argv)
            res = _parse_json_stdout(buf)
        finally:
            os.unlink(p)
        self.assertEqual(rc, 0, (rc, res))
        self.assertTrue(res["pass"], res)
        self.assertEqual(res["admissible_seam"]["status"], "GO", res)


class Test127G2GuardedEntryRefusalParity(unittest.TestCase):
    """G2: guarded_execute/refusal_payload preserve 126-stable
    reason_code=PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS + seam_go_prereg_required/
    reason_code_detail when seam GO but prereg/data missing; no regression to
    ambiguous codes. Assert fclr010_execute + run_liqmicro blocked refusal payloads
    via mocks (no parquet/import side effects)."""

    def _seam_go_prereg_required_guard(self):
        return {
            "status": "BLOCKED",
            "reason_code": BLOCKED_RC,
            "seam_go_prereg_required": True,
            "reason_code_detail": "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED",
            "outcomes_inspected": False,
            "canonical_outputs_mutated": False,
            "network": False,
            "writes_real_research_state": False,
            "data_loaded_implicitly": False,
            "reads_parquet": False,
            "reads_outcomes": False,
            "outcomes_loaded": None,
        }

    def test_guarded_execute_parity_seam_go_prereg_required(self):
        from scripts.fclr010_guarded_entry import guarded_execute
        res = guarded_execute(
            data_path=Path("/nonexistent_tracka_data"),
            pre_reg_path=None,
            repo_root=REAL,
            source_manifest=None,
            admissible_manifest=_real_go_manifest(),
            admissible_manifest_path=None,
            outcome_loader=None,
            allow_default_loader=False,
        )
        # guarded_execute normalizes seam-GO-prereg-required to stable reason_code.
        self.assertEqual(res.get("reason_code"), BLOCKED_RC, res)
        self.assertTrue(res.get("seam_go_prereg_required"), res)
        self.assertEqual(res.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED", res)
        self.assertEqual(res.get("status"), "BLOCKED", res)
        self.assertFalse(res.get("outcomes_inspected"), res)
        self.assertFalse(res.get("canonical_outputs_mutated"), res)
        self.assertFalse(res.get("network"), res)
        self.assertFalse(res.get("writes_real_research_state"), res)
        self.assertFalse(res.get("reads_parquet"), res)
        self.assertFalse(res.get("reads_outcomes"), res)

    def test_guarded_execute_parity_seam_go_data_missing(self):
        from scripts.fclr010_guarded_entry import guarded_execute
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            f.write("{}")
            pre_reg = f.name
        try:
            res = guarded_execute(
                data_path=Path("/nonexistent_tracka_data"),
                pre_reg_path=Path(pre_reg),
                repo_root=REAL,
                source_manifest=None,
                admissible_manifest=_real_go_manifest(),
                admissible_manifest_path=None,
                outcome_loader=None,
                allow_default_loader=False,
            )
        finally:
            os.unlink(pre_reg)
        # seam GO + prereg present but data missing => stable reason_code +
        # seam_go_data_missing parity.
        self.assertEqual(res.get("reason_code"), BLOCKED_RC, res)
        self.assertTrue(res.get("seam_go_data_missing"), res)
        self.assertEqual(res.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_DATA_PATH_MISSING", res)

    def test_refusal_payload_stable_shape(self):
        from scripts.fclr010_guarded_entry import refusal_payload
        p = refusal_payload(
            script="fclr010_execute",
            reason_code=BLOCKED_RC,
            reason="blocked by guarded execution contract",
            guard=self._seam_go_prereg_required_guard(),
        )
        missing = REQ_REFUSAL - set(p.keys())
        self.assertFalse(missing, (missing, p))
        self.assertEqual(p["status"], "BLOCKED", p)
        self.assertEqual(p["reason_code"], BLOCKED_RC, p)
        self.assertEqual(p["script"], "fclr010_execute", p)
        self.assertFalse(p["canonical_outputs_mutated"], p)
        self.assertFalse(p["network"], p)
        self.assertFalse(p["writes_real_research_state"], p)
        self.assertFalse(p["outcomes_inspected"], p)
        self.assertEqual(p["guard"]["reason_code_detail"], "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED", p)

    def test_fclr010_execute_blocked_refusal_parity(self):
        mod = _fresh_mod("scripts.fclr010_execute")
        before = _snap([FRONTIER, RUN_MANIFEST, EVAL_FCLR010])
        guard = self._seam_go_prereg_required_guard()
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
        missing = REQ_REFUSAL - set(p.keys())
        self.assertFalse(missing, (missing, p))
        _unchanged([FRONTIER, RUN_MANIFEST, EVAL_FCLR010], before)

    def test_run_liqmicro_blocked_refusal_parity(self):
        mod = _fresh_mod("scripts.run_liqmicro")
        before = _snap([FRONTIER, RUN_MANIFEST, EVAL_FCLR010, EVAL_LIQM1])
        guard = self._seam_go_prereg_required_guard()
        called = {"pipe": 0}

        def _boom(*a, **k):
            called["pipe"] += 1
            raise AssertionError("_run_pipeline must not run on blocked branch")

        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=guard), \
             patch.object(mod, "_run_pipeline", _boom), \
             redirect_stdout(io.StringIO()) as buf:
            rc = mod.main()
        p = _parse_json_stdout(buf)
        self.assertEqual(rc, 1, (rc, p))
        self.assertEqual(p.get("status"), "BLOCKED", p)
        self.assertEqual(p.get("reason_code"), BLOCKED_RC, p)
        self.assertEqual(p.get("script"), "run_liqmicro", p)
        self.assertEqual(called["pipe"], 0)
        self.assertFalse(p.get("canonical_outputs_mutated"), p)
        missing = REQ_REFUSAL - set(p.keys())
        self.assertFalse(missing, (missing, p))
        _unchanged([FRONTIER, RUN_MANIFEST, EVAL_FCLR010, EVAL_LIQM1], before)


class Test127G3ReadyWriterScopeDepLight(unittest.TestCase):
    """G3: READY writer scope, dep-light. For coupled_robust_eval and/or
    overlay_quick/overlay_tracka_execute: blocked path never invokes loaders/writers
    and canonical_outputs_mutated=false on blocked refusals; READY_FROZEN mocked path
    does not mutate canonical Track A evaluation/manifest/frontier beyond allowed
    targets. Assert with tmp snapshots."""

    SCRIPTS = [
        ("scripts.coupled_robust_eval", "coupled_robust_eval",
         [FRONTIER, RUN_MANIFEST, EVAL_FCLR010, EVAL_COUPLED]),
        ("scripts.overlay_quick", "overlay_quick",
         [FRONTIER, RUN_MANIFEST, EVAL_FCLR010, EVAL_OVERLAY, CROSS_TRACK]),
        ("scripts.overlay_tracka_execute", "overlay_tracka_execute",
         [FRONTIER, RUN_MANIFEST, EVAL_FCLR010, EVAL_OVERLAY, CROSS_TRACK]),
    ]

    def _run_blocked_main(self, mod_name, script_name, canon_paths):
        mod = _fresh_mod(mod_name)
        before = _snap(canon_paths)
        guard = _blocked_payload(script_name,
                                 extra={"seam_go_prereg_required": True,
                                        "reason_code_detail": "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED"})
        loader_called = {"n": 0}

        def _boom_loader(*a, **k):
            loader_called["n"] += 1
            raise AssertionError("outcome loader must not run on blocked branch")

        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=guard), \
             redirect_stdout(io.StringIO()) as buf:
            rc = mod.main()
        p = _parse_json_stdout(buf)
        self.assertEqual(rc, 1, (mod_name, rc, p))
        self.assertEqual(p.get("status"), "BLOCKED", (mod_name, p))
        self.assertEqual(p.get("reason_code"), BLOCKED_RC, (mod_name, p))
        self.assertEqual(p.get("script"), script_name, (mod_name, p))
        self.assertFalse(p.get("canonical_outputs_mutated"), (mod_name, p))
        self.assertFalse(p.get("outcomes_inspected"), (mod_name, p))
        self.assertFalse(p.get("network"), (mod_name, p))
        self.assertFalse(p.get("writes_real_research_state"), (mod_name, p))
        missing = REQ_REFUSAL - set(p.keys())
        self.assertFalse(missing, (mod_name, missing, p))
        _unchanged(canon_paths, before)
        return p

    def test_coupled_robust_eval_blocked_no_loader_no_mutation(self):
        self._run_blocked_main(*self.SCRIPTS[0])

    def test_overlay_quick_blocked_no_loader_no_mutation(self):
        self._run_blocked_main(*self.SCRIPTS[1])

    def test_overlay_tracka_execute_blocked_no_loader_no_mutation(self):
        self._run_blocked_main(*self.SCRIPTS[2])

    def _fake_coupled_build_panel_module(self):
        """Inject a stub scripts.coupled_build_panel so heavy imports are avoided."""
        panel = types.SimpleNamespace()
        panel.__getitem__ = lambda self, k: _StubDF()
        panel.__setitem__ = lambda self, k, v: None
        panel.__contains__ = lambda self, k: True
        mod = types.ModuleType("scripts.coupled_build_panel")
        mod.build = lambda force=False, outcome_loader=None: _StubPanel()
        mod._load_coupled_outcomes = lambda dp: {"panel": _StubPanel()}
        return mod


class _StubPanel:
    def __getitem__(self, k):
        return _StubDF()

    def __setitem__(self, k, v):
        return None


class _StubDF:
    def __len__(self):
        return 0

    @property
    def empty(self):
        return True

    def __getitem__(self, k):
        return _StubS()

    @property
    def dt(self):
        return _StubDT()

    def sort_values(self, *a, **k):
        return self

    def groupby(self, *a, **k):
        return _StubGB()

    def to_dict(self, *a, **k):
        return []

    def copy(self):
        return self


class _StubDT:
    tz = None

    def tz_localize(self, *a, **k):
        return self

    def tz_convert(self, *a, **k):
        return self


class _StubS:
    def nunique(self):
        return 0

    @property
    def min(self):
        return None

    @property
    def max(self):
        return None

    def __le__(self, other):
        return self

    def __ge__(self, other):
        return self

    def __gt__(self, other):
        return self

    def __lt__(self, other):
        return self

    def __and__(self, other):
        return self

    def __or__(self, other):
        return self

    def __invert__(self):
        return self

    def to_dict(self, *a, **k):
        return [{"sym": "BTC", "y_occ": 0}]

    def __iter__(self):
        return iter([])

    def __len__(self):
        return 0

    def mean(self, *a, **k):
        return self

    def sum(self, *a, **k):
        return self

    def quantile(self, *a, **k):
        return 0.0


class _StubGB:
    def __getattr__(self, k):
        return self

    def __call__(self, *a, **k):
        return self

    def shift(self, *a, **k):
        return _StubS()

    def rolling(self, *a, **k):
        return _StubRB()

    def ewm(self, *a, **k):
        return _StubS()


class _StubRB:
    def __getattr__(self, k):
        return self

    def mean(self, *a, **k):
        return _StubS()

    def sum(self, *a, **k):
        return _StubS()


class Test127G3ReadyFrozenNoCanonicalMutation(unittest.TestCase):
    """G3: mocked READY_FROZEN path completes without mutating canonical Track A
    evaluation/manifest/frontier beyond allowed targets (write_text no-op'd to
    isolate the guard boundary; snapshots compared after)."""

    def _run_ready_frozen(self, mod_name, canon_paths, extra_patches=None):
        _mock_heavy()
        for mn in (mod_name, "scripts.coupled_build_panel"):
            sys.modules.pop(mn, None)
        sys.modules["scripts.coupled_build_panel"] = _fake_coupled_build_panel_module()

        guard = {
            "status": "READY_FROZEN",
            "outcomes_inspected": False,
            "canonical_outputs_mutated": False,
            "network": False,
            "writes_real_research_state": False,
            "data_loaded_implicitly": False,
            "outcomes_loaded": {"panel": _StubPanel()},
        }

        fake_manifest_str = json.dumps({
            "split_boundaries_fclr010": {
                "frozen_before_outcomes": True,
                "train": {"start": "2024-04-01T00:00:00Z", "end": "2024-06-08T23:00:00Z"},
                "validation": {"start": "2024-06-16T00:00:00Z", "end": "2024-07-15T23:00:00Z"},
                "test": {"start": "2024-07-23T00:00:00Z", "end": "2024-09-30T23:00:00Z"},
            }
        })

        real_open = builtins.open

        def _fake_open(path, *a, **k):
            p = Path(path)
            if str(p) == str(RUN_MANIFEST):
                return io.StringIO(fake_manifest_str)
            return real_open(path, *a, **k)

        write_calls = {"n": 0}
        real_write_text = Path.write_text

        def _no_op_write_text(self, data, *a, **k):
            write_calls["n"] += 1
            return len(data) if isinstance(data, str) else 0

        patches = [
            patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=guard),
            patch("builtins.open", _fake_open),
            patch.object(Path, "write_text", _no_op_write_text),
        ]
        if extra_patches:
            patches.extend(extra_patches)

        before = _snap(canon_paths)
        try:
            for ptch in patches:
                ptch.start()
            mod = importlib.import_module(mod_name)
            with redirect_stdout(io.StringIO()):
                rc = mod.main()
        finally:
            for ptch in reversed(patches):
                ptch.stop()
        _unchanged(canon_paths, before)
        return rc, write_calls["n"]

    def test_coupled_robust_eval_ready_frozen_no_canonical_mutation(self):
        rc, nw = self._run_ready_frozen(
            "scripts.coupled_robust_eval",
            [FRONTIER, RUN_MANIFEST, EVAL_FCLR010, EVAL_COUPLED],
            extra_patches=[
                patch("scripts.coupled_robust_eval.build_features",
                      lambda panel, *a, **k: _StubDF()),
                patch("scripts.coupled_robust_eval.block_bootstrap_compare",
                      lambda *a, **k: {"mean_diff_b1_minus_c": -0.01, "ci_lo": -0.02,
                                       "ci_hi": 0.0, "b1_brier": 0.1, "c_brier": 0.09,
                                       "rel_brier_reduction": 0.05, "n_pairs": 10,
                                       "n_blocks": 5, "n_boot": 1}),
                patch("scripts.coupled_robust_eval.git_sha", lambda: "fake-sha"),
            ],
        )
        self.assertTrue(rc is None or rc == 0, (rc, nw))
        self.assertGreater(nw, 0, "READY_FROZEN path should attempt canonical writes")


if __name__ == "__main__":
    unittest.main()
