"""FCLR-NEXT-125: guarded seam-GO READY acceptance (G1) +
audit refusal-payload shape stability (G2) +
run_liqmicro v1 frontier-write parity (G3) +
canonical alt-outputs + root bound regression (G4) +
refusal fail-closed matrix 6x4 (G5).

Deterministic, tmp-isolated, no network, no parquet/outcome reads, no real research_state writes.
Dep-light: heavy deps (numpy/pandas/pyarrow/statsmodels/scipy) are stubbed so the suite runs
in minimal environments.
"""
from __future__ import annotations

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

from scripts.fclr010_guarded_entry import refusal_payload
from scripts.fclr010_harness import FCLR010Harness
from src.analysis.tracka_admissible import build_ironflow_month_manifest

REAL = Path(__file__).resolve().parent.parent
RS = REAL / "research_state"
SCRIPTS = REAL / "scripts"
FRONTIER = RS / "experiment_frontier.json"
RUN_MANIFEST = RS / "run_manifest.json"
EVAL_FCLR010 = RS / "evaluation_summary_FCLR010.md"
EVAL_LIQM1 = RS / "evaluation_summary_FCLR-LIQMICRO-001.md"
REQ_REFUSAL = {
    "status", "outcomes_inspected", "canonical_outputs_mutated", "network",
    "writes_real_research_state", "script", "reason_code",
}
BLOCKED_RC = "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS"


def _snap(paths):
    return {str(p): (p.read_bytes() if p.exists() else None) for p in paths}


def _unchanged(paths, before):
    for s, b in before.items():
        p = Path(s)
        a = p.read_bytes() if p.exists() else None
        if b != a:
            raise AssertionError(f"canonical target mutated: {s}")


def _mock_heavy():
    """Stub heavy deps so guarded scripts import in a minimal environment."""
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

    class _S:
        def nunique(self):
            return 1

    _mod("numpy",
         nan=float("nan"), isnan=lambda x: False, isinf=lambda x: False,
         float64=float, int64=int, ones=lambda n, *a, **k: [0.0] * int(n),
         array=lambda x, *a, **k: list(x), sign=lambda x: 0,
         clip=lambda x, *a, **k: x, log1p=lambda x: x,
         maximum=lambda a, b: a, minimum=lambda a, b: a,
         quantile=lambda x, q: 0.0, exp=lambda x: 1.0,
         column_stack=lambda cols: cols, zeros=lambda *a, **k: [],
         mean=lambda x, *a, **k: 0.0, sum=lambda x, *a, **k: 0,
         abs=lambda x: x, diff=lambda x, *a, **k: [],
         float_=float, ndarray=list, isnull=lambda x: False)
    sys.modules["numpy"].linalg = types.ModuleType("numpy.linalg")
    sys.modules["numpy"].linalg.solve = lambda A, b: [0.0] * len(b)
    sys.modules["numpy"].linalg.pinv = lambda A: []
    _mod("pandas",
         DataFrame=_DF, read_parquet=lambda *a, **k: _DF(),
         Timestamp=lambda x: x, concat=lambda frames, *a, **k: frames[0] if frames else _DF(),
         date_range=lambda *a, **k: [], NA=None, isnull=lambda x: False,
         MultiIndex=types.ModuleType("pandas.MultiIndex"))
    _mod("pyarrow")
    _mod("pyarrow.parquet")
    _mod("statsmodels")
    sm = _mod("statsmodels.api", add_constant=lambda x: x)
    _mod("statsmodels.formula.api", ols=lambda *a, **k: None)
    _mod("scipy")
    _mod("scipy.stats")


def _fresh_mod(name):
    _mock_heavy()
    for mn in (name, "scripts.run_liqmicro", "scripts.run_liqmicro_v2",
               "scripts.coupled_build_panel", "scripts.coupled_robust_eval",
               "analysis.liqmicro.ingest", "analysis.liqmicro.features",
               "analysis.liqmicro.models", "analysis.liqmicro.stats"):
        sys.modules.pop(mn, None)
    return __import__(name, fromlist=["x"])


def _real_go_admissible_manifest(month="2026-11"):
    return build_ironflow_month_manifest(
        month=month,
        events_path=f"research_state/data_cache/ironflow_events/events/{month}.parquet",
        fills_path=f"research_state/data_cache/ironflow_events/fills/{month}.parquet",
        events_url=f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/{month}.parquet",
        fills_url=f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/{month}.parquet",
        schema_fields_events=["timestamp", "symbol", "notional_usd"],
        schema_fields_fills=["timestamp", "symbol", "side", "notional_usd"],
    )


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


def _parse_json_stdout(buf):
    m = re.search(r"\{.*\}", buf.getvalue(), re.S)
    assert m is not None, f"no JSON object in stdout: {buf.getvalue()!r}"
    return json.loads(m.group(0))


class Test125G1GuardedSeamGoReadyAcceptance(unittest.TestCase):
    """G1: evaluate_forward / execute_ready_data_load READY_FROZEN acceptance on
    admissible GO manifest + present prereg + present data_path; no implicit parquet
    read; explicit loader invoked exactly once; direct+execute parity."""

    def setUp(self):
        self.h = FCLR010Harness(repo_root=REAL)
        self.admissible = _real_go_admissible_manifest("2026-11")

    def test_evaluate_forward_ready_frozen_admissible_go(self):
        with tempfile.TemporaryDirectory() as td:
            pre_reg = Path(td) / "prereg.json"; pre_reg.write_text("{}")
            data = Path(td) / "data"; data.mkdir()
            res = self.h.evaluate_forward(
                data, Path(td) / "out", pre_reg_path=pre_reg,
                admissible_manifest=self.admissible, source_manifest=None,
            )
        self.assertEqual(res.get("status"), "READY_FROZEN", res)
        self.assertFalse(res.get("outcomes_inspected"))
        self.assertIsNone(res.get("outcomes_loaded"))
        self.assertFalse(res.get("reads_parquet"))
        self.assertFalse(res.get("reads_outcomes"))
        self.assertFalse(res.get("network"))
        self.assertTrue(res.get("prereg_required") is False or res.get("prereg_required") is None)

    def test_execute_ready_data_load_no_implicit_parquet_read(self):
        with tempfile.TemporaryDirectory() as td:
            pre_reg = Path(td) / "prereg.json"; pre_reg.write_text("{}")
            data = Path(td) / "data"; data.mkdir()
            res = self.h.execute_ready_data_load(
                data, pre_reg_path=pre_reg, admissible_manifest=self.admissible,
            )
        self.assertEqual(res.get("status"), "READY_FROZEN", res)
        self.assertEqual(res.get("data_load_mode"), "EXPLICIT_LOADER_REQUIRED_NO_IMPLICIT_PARQUET_READ", res)
        self.assertFalse(res.get("data_loaded_implicitly"))
        self.assertFalse(res.get("outcomes_inspected"))
        self.assertIsNone(res.get("outcomes_loaded"))

    def test_execute_ready_data_load_explicit_loader_invoked_once(self):
        calls = {"n": 0}

        def loader(dp):
            calls["n"] += 1
            return {"rows": 7}

        with tempfile.TemporaryDirectory() as td:
            pre_reg = Path(td) / "prereg.json"; pre_reg.write_text("{}")
            data = Path(td) / "data"; data.mkdir()
            res = self.h.execute_ready_data_load(
                data, pre_reg_path=pre_reg, admissible_manifest=self.admissible,
                outcome_loader=loader,
            )
        self.assertEqual(res.get("status"), "READY_FROZEN", res)
        self.assertEqual(calls["n"], 1, f"loader invoked {calls['n']} times, expected 1")
        self.assertEqual(res.get("outcomes_loaded"), {"rows": 7})
        self.assertEqual(res.get("data_load_mode"), "EXPLICIT_LOADER_AFTER_GATES", res)
        self.assertFalse(res.get("data_loaded_implicitly"))

    def test_direct_execute_parity_ready_frozen(self):
        with tempfile.TemporaryDirectory() as td:
            pre_reg = Path(td) / "prereg.json"; pre_reg.write_text("{}")
            data = Path(td) / "data"; data.mkdir()
            direct = self.h.evaluate_forward(
                data, Path(td) / "out_direct", pre_reg_path=pre_reg,
                admissible_manifest=self.admissible, source_manifest=None,
            )
            executed = self.h.execute_ready_data_load(
                data, pre_reg_path=pre_reg, admissible_manifest=self.admissible,
            )
        self.assertEqual(direct.get("status"), "READY_FROZEN", direct)
        self.assertEqual(executed.get("status"), "READY_FROZEN", executed)
        self.assertEqual(direct.get("data_path"), str(data))
        self.assertEqual(executed.get("data_path"), str(data))
        self.assertEqual(direct.get("outcomes_inspected"), executed.get("outcomes_inspected"))

    def test_blocked_when_prereg_missing(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "data"; data.mkdir()
            res = self.h.evaluate_forward(
                data, Path(td) / "out", pre_reg_path=None,
                admissible_manifest=self.admissible, source_manifest=None,
            )
        self.assertEqual(res.get("status"), "BLOCKED", res)
        self.assertTrue(res.get("prereg_required"))

    def test_blocked_when_data_path_missing(self):
        with tempfile.TemporaryDirectory() as td:
            pre_reg = Path(td) / "prereg.json"; pre_reg.write_text("{}")
            missing = Path(td) / "does_not_exist"
            res = self.h.evaluate_forward(
                missing, Path(td) / "out", pre_reg_path=pre_reg,
                admissible_manifest=self.admissible, source_manifest=None,
            )
        self.assertEqual(res.get("status"), "BLOCKED", res)
        self.assertEqual(res.get("reason_code"), BLOCKED_RC, res)
        self.assertTrue(res.get("seam_go_data_missing"))
        self.assertFalse(res.get("outcomes_inspected"))

    def test_blocked_when_admissible_manifest_nogo_modeled_proxy(self):
        nogo = build_ironflow_month_manifest(
            month="2026-11", modeled_or_proxy=True,
            label_definition="modeled_liquidation_proxy_estimate",
        )
        with tempfile.TemporaryDirectory() as td:
            pre_reg = Path(td) / "prereg.json"; pre_reg.write_text("{}")
            data = Path(td) / "data"; data.mkdir()
            res = self.h.execute_ready_data_load(
                data, pre_reg_path=pre_reg, admissible_manifest=nogo,
            )
        self.assertEqual(res.get("status"), "BLOCKED", res)
        self.assertFalse(res.get("outcomes_inspected"))
        self.assertFalse(res.get("data_loaded_implicitly"))
        self.assertIsNone(res.get("outcomes_loaded"))


class Test125G2AuditRefusalPayloadShapeStability(unittest.TestCase):
    """G2: blocked-main refusal payloads for all guarded ready-writing/audit scripts
    contain the required refusal fields with stable reason_code, correct script name,
    canonical_outputs_mutated=false, network=false, writes_real_research_state=false."""

    SCRIPTS = [
        ("scripts.coupled_build_panel", "coupled_build_panel"),
        ("scripts.fclr010_execute", "fclr010_execute"),
        ("scripts.fclr010_execute_fast", "fclr010_execute_fast"),
        ("scripts.run_liqmicro_v2", "run_liqmicro_v2"),
        ("scripts.coupled_robust_eval", "coupled_robust_eval"),
        ("scripts.liqmicro_audit", "liqmicro_audit"),
        ("scripts.fclr010_coverage_audit", "fclr010_coverage_audit"),
        ("scripts.overlay_quick", "overlay_quick"),
        ("scripts.overlay_tracka_execute", "overlay_tracka_execute"),
    ]

    def _run_blocked_main(self, mod_name, script_name, state_payload):
        mod = _fresh_mod(mod_name)
        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=state_payload), \
             redirect_stdout(io.StringIO()) as buf:
            rc = mod.main()
        p = _parse_json_stdout(buf)
        missing = REQ_REFUSAL - set(p.keys())
        self.assertFalse(missing, (mod_name, missing, p))
        self.assertEqual(rc, 1, (mod_name, rc, p))
        self.assertEqual(p.get("status"), "BLOCKED", (mod_name, p))
        self.assertEqual(p.get("reason_code"), BLOCKED_RC, (mod_name, p))
        self.assertEqual(p.get("script"), script_name, (mod_name, p))
        self.assertFalse(p.get("outcomes_inspected"), (mod_name, p))
        self.assertFalse(p.get("canonical_outputs_mutated"), (mod_name, p))
        self.assertFalse(p.get("network"), (mod_name, p))
        self.assertFalse(p.get("writes_real_research_state"), (mod_name, p))
        return p

    def test_all_scripts_refuse_stable_payload_missing_prereg(self):
        state = _blocked_payload("X", reason_code=BLOCKED_RC,
                                 extra={"seam_go_prereg_required": True,
                                        "reason_code_detail": "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED"})
        for mod_name, script_name in self.SCRIPTS:
            state["script"] = script_name
            self._run_blocked_main(mod_name, script_name, dict(state))

    def test_all_scripts_refuse_stable_payload_nogo_seam(self):
        state = _blocked_payload("X", reason_code=BLOCKED_RC,
                                 extra={"seam_pass": False, "fail_closed": True,
                                        "failures": ["admissible_seam_nogo"]})
        for mod_name, script_name in self.SCRIPTS:
            state["script"] = script_name
            self._run_blocked_main(mod_name, script_name, dict(state))

    def test_all_scripts_refuse_stable_payload_modeled_proxy(self):
        state = _blocked_payload("X", reason_code=BLOCKED_RC,
                                 extra={"seam_pass": False, "fail_closed": True,
                                        "failures": ["modeled_or_proxy_conflation"]})
        for mod_name, script_name in self.SCRIPTS:
            state["script"] = script_name
            self._run_blocked_main(mod_name, script_name, dict(state))

    def test_all_scripts_refuse_stable_payload_wrong_venue(self):
        state = _blocked_payload("X", reason_code=BLOCKED_RC,
                                 extra={"seam_pass": False, "fail_closed": True,
                                        "failures": ["venue_not_hyperliquid_only"]})
        for mod_name, script_name in self.SCRIPTS:
            state["script"] = script_name
            self._run_blocked_main(mod_name, script_name, dict(state))

    def test_refusal_payload_helper_shape(self):
        p = refusal_payload(script="coupled_build_panel",
                            reason_code=BLOCKED_RC,
                            reason="blocked by guarded execution contract")
        missing = REQ_REFUSAL - set(p.keys())
        self.assertFalse(missing, (missing, p))
        self.assertEqual(p["script"], "coupled_build_panel")
        self.assertEqual(p["reason_code"], BLOCKED_RC)
        self.assertFalse(p["canonical_outputs_mutated"])
        self.assertFalse(p["network"])
        self.assertFalse(p["writes_real_research_state"])
        self.assertFalse(p["outcomes_inspected"])


class Test125G3RunLiqmicroV1FrontierWriteParity(unittest.TestCase):
    """G3: blocked main of scripts/run_liqmicro.py never invokes _run_pipeline and
    never mutates experiment_frontier.json / run_manifest.json / canonical outputs;
    the READY_FROZEN _run_pipeline path is the sole writer (source-order/guard)."""

    def test_blocked_main_never_invokes_run_pipeline_no_canonical_mutation(self):
        mod = _fresh_mod("scripts.run_liqmicro")
        before = _snap([FRONTIER, RUN_MANIFEST, EVAL_FCLR010, EVAL_LIQM1])
        calls = {"pipe": 0}
        orig_pipe = mod._run_pipeline

        def spy_pipe(*a, **k):
            calls["pipe"] += 1
            return orig_pipe(*a, **k)

        with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value={
            "status": "BLOCKED", "reason_code": BLOCKED_RC,
            "outcomes_inspected": False, "canonical_outputs_mutated": False,
        }), patch.object(mod, "_run_pipeline", spy_pipe), \
             redirect_stdout(io.StringIO()):
            rc = mod.main()
        self.assertEqual(rc, 1)
        self.assertEqual(calls["pipe"], 0, "_run_pipeline must not run on blocked branch")
        _unchanged([FRONTIER, RUN_MANIFEST, EVAL_FCLR010, EVAL_LIQM1], before)

    def test_ready_frozen_run_pipeline_is_sole_writer_source_order(self):
        src = (SCRIPTS / "run_liqmicro.py").read_text()
        guarded_call = "guard = guarded_execute("
        status_check = 'if guard.get("status") != "READY_FROZEN":'
        pipe_call = "_run_pipeline(raw_df, hourly)"
        frontier_path = "RESEARCH_STATE / \"experiment_frontier.json\""
        frontier_write_inside_pipe = "_write_experiment_frontier_ready(any_sig, summary_path)"
        self.assertIn(guarded_call, src, "guarded_execute call missing")
        self.assertIn(status_check, src, "READY_FROZEN refusal gate missing")
        self.assertIn(pipe_call, src, "_run_pipeline call missing")
        self.assertIn(frontier_path, src, "experiment_frontier.json path reference missing")
        self.assertIn(frontier_write_inside_pipe, src,
                      "_run_pipeline must invoke the sole frontier writer")
        i_guard = src.index(guarded_call)
        i_status = src.index(status_check)
        i_pipe = src.index(pipe_call)
        # guarded call and refusal gate must precede the sole _run_pipeline write path
        self.assertLess(i_guard, i_pipe, "guarded_execute must precede _run_pipeline")
        self.assertLess(i_status, i_pipe, "READY_FROZEN gate must precede _run_pipeline")
        # the frontier writer is only invoked from within _run_pipeline's body
        i_pipe_def = src.index("def _run_pipeline(raw_df: pd.DataFrame, hourly: pd.DataFrame) -> None:")
        i_frontier_writer = src.index(frontier_write_inside_pipe)
        self.assertLess(i_pipe_def, i_frontier_writer,
                        "frontier writer must be defined inside the _run_pipeline body scope")


class Test125G4CanonicalAltOutputsRootBoundRegression(unittest.TestCase):
    """G4: deterministic read-only regression: research_state root md+json <=165,
    ironflow_probe* == 2 (1 live + 1 digest), no new recurring timestamped
    campaign_sweep_tracka_*/liquidation_forward_validate_* families beyond archived
    20261105 policy, canonical alt outputs (latest pointers) present. No writes."""

    def test_root_md_json_bounded(self):
        md_json = [p for p in RS.glob("*.md")] + [p for p in RS.glob("*.json")]
        count = len(md_json)
        # 2026-11-07T18:55Z: bound 163->165 to admit the durable Gate 4 v4 preregistration
        # freeze pair (pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.md|json).
        self.assertLessEqual(count, 165, f"root md+json count {count} exceeds bound 165")

    def test_probe_count_exactly_two(self):
        live = [p for p in RS.glob("ironflow_probe_*.json")
                if not p.name.startswith("ironflow_probe_digest_")]
        digests = [p for p in RS.glob("ironflow_probe_digest_*.json")]
        digest_latest = RS / "ironflow_probe_digest_latest.json"
        self.assertEqual(len(live), 1, f"expected exactly 1 live probe, got {live}")
        self.assertEqual(len(digests), 1, f"expected exactly 1 digest, got {digests}")
        self.assertTrue(digest_latest.exists() and digest_latest in digests)
        self.assertEqual(len(live) + len(digests), 2)

    def test_canonical_alt_outputs_latest_pointers_present(self):
        self.assertTrue((RS / "alt_source_scan_latest.json").exists(), "alt_source_scan_latest.json missing")
        self.assertTrue((RS / "alt_source_deep_review_latest.md").exists(), "alt_source_deep_review_latest.md missing")

    def test_no_new_recurring_sweep_validate_families(self):
        # Archival policy: the recurring sweep/validate families are pinned to the
        # 20261105 sweep day; any timestamped member must belong to that archived set.
        sweep = list(RS.glob("campaign_sweep_tracka_*T*.md"))
        validate = list(RS.glob("liquidation_forward_validate_*T*.md"))
        for p in sweep + validate:
            self.assertIn("20261105T", p.name, f"non-archived recurring family member: {p.name}")
        # drift_invariants canonical-alt + no-recurring-family checks must pass
        from scripts.tracka_resume_check import drift_invariants
        checks = drift_invariants(REAL, research_state_dir=RS)
        self.assertTrue(checks["canonical_alt_outputs_only"]["pass"], checks["canonical_alt_outputs_only"])
        self.assertTrue(checks["no_recurring_timestamped_probe_scan_families"]["pass"],
                        checks["no_recurring_timestamped_probe_scan_families"])


_STATE_SCRIPTS = [
    ("scripts.coupled_robust_eval", "coupled_robust_eval"),
    ("scripts.fclr010_execute", "fclr010_execute"),
    ("scripts.fclr010_coverage_audit", "fclr010_coverage_audit"),
    ("scripts.liqmicro_audit", "liqmicro_audit"),
    ("scripts.overlay_quick", "overlay_quick"),
    ("scripts.overlay_tracka_execute", "overlay_tracka_execute"),
]

_STATES = [
    ("missing_prereg", BLOCKED_RC, {"seam_go_prereg_required": True,
                                    "reason_code_detail": "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED"}),
    ("nogo_seam", "ADMISSIBLE_SEAM_NOGO_BEFORE_PREREG", {"seam_pass": False, "fail_closed": True}),
    ("modeled_proxy", "ADMISSIBLE_SEAM_NOGO_MODELED_OR_PROXY",
     {"seam_pass": False, "fail_closed": True, "failures": ["modeled_or_proxy_conflation"]}),
    ("wrong_venue", "ADMISSIBLE_SEAM_NOGO_WRONG_VENUE",
     {"seam_pass": False, "fail_closed": True, "failures": ["venue_not_hyperliquid_only"]}),
]


class Test125G5RefusalFailClosedMatrix6x4(unittest.TestCase):
    """G5: 6 scripts x 4 non-READY states; each refuses rc=1 with
    canonical_outputs_mutated=false via guarded_execute mocks."""

    def test_six_by_four_fail_closed_matrix(self):
        for mod_name, script_name in _STATE_SCRIPTS:
            mod = _fresh_mod(mod_name)
            for state_name, reason_code, extra in _STATES:
                payload = _blocked_payload(script_name, reason_code=reason_code, extra=extra)
                before = _snap([FRONTIER, RUN_MANIFEST, EVAL_FCLR010])
                with patch("scripts.fclr010_guarded_entry.guarded_execute", return_value=payload), \
                     redirect_stdout(io.StringIO()) as buf:
                    rc = mod.main()
                p = _parse_json_stdout(buf)
                self.assertEqual(rc, 1, (mod_name, state_name, rc, p))
                self.assertEqual(p.get("status"), "BLOCKED", (mod_name, state_name, p))
                self.assertFalse(p.get("canonical_outputs_mutated"),
                                 (mod_name, state_name, p))
                self.assertFalse(p.get("outcomes_inspected"), (mod_name, state_name, p))
                _unchanged([FRONTIER, RUN_MANIFEST, EVAL_FCLR010], before)


if __name__ == "__main__":
    unittest.main()
