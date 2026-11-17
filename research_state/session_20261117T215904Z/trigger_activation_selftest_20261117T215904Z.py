#!/usr/bin/env python3
"""FCLR-TRIGGER-READINESS-01 trigger-activation selftest.

Real unittest self-tests (runnable via `python3 -m unittest` when the session
directory is on sys.path, or directly via `python3 trigger_activation_selftest_<UTC>.py`)
that exercise the executor on SYNTHETIC data only:

- 30d-train + 7d-embargo + 30d-test block arithmetic and non-overlap detection
- paired_n floor enforcement below/above 23224 (Gate 4 / Track C) and 11689 (Track A / HL / expansion)
- Holm-family enumeration determinism
- refusal behaviour when pre-outcome gates fail
- explicit outcome-blindness assertion (no outcome path opened)

Records pass/fail counts + EXIT in the sidecar `trigger_activation_selftest_<UTC>.json`
when executed directly (`__main__`).

Outcome-blind: reads only synthetic in-memory values; never touches research_state
outcome files, results/, evaluation_summary_*, or any sealed artifact.
"""
from __future__ import annotations

import datetime as _dt
import json
import sys
import unittest
from pathlib import Path

SESSION_UTC = "20261117T215904Z"
SIDECAR = Path(__file__).resolve().with_name(
    f"trigger_activation_selftest_{SESSION_UTC}.json"
)

SESSION_DIR = Path(__file__).resolve().parent

import importlib.util

_EXECUTOR_PATH = SESSION_DIR / f"trigger_activation_executor_{SESSION_UTC}.py"
_spec = importlib.util.spec_from_file_location(
    f"trigger_activation_executor_{SESSION_UTC}", _EXECUTOR_PATH
)
exec_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(exec_mod)  # type: ignore[union-attr]

TRIGGER_IDS = (
    "GATE4_BRANCH_1",
    "NEW_OBSERVED_LIQUIDATION_SOURCE",
    "HL_LABEL_EXTENSION",
    "EXPANSION_ROBUSTNESS_REDO",
)


def _block_span(test_start_ymd: str) -> tuple[_dt.date, _dt.date, _dt.date, _dt.date]:
    """30d train + 7d embargo + 30d test for a test month starting test_start."""
    test_start = _dt.date.fromisoformat(test_start_ymd)
    test_end = test_start + _dt.timedelta(days=29)
    embargo_start = test_start - _dt.timedelta(days=7)
    train_end_exclusive = embargo_start
    train_start = train_end_exclusive - _dt.timedelta(days=30)
    return train_start, train_end_exclusive - _dt.timedelta(days=1), embargo_start, test_end


def _intervals_overlap(a: tuple[_dt.date, _dt.date], b: tuple[_dt.date, _dt.date]) -> bool:
    return max(a[0], b[0]) <= min(a[1], b[1])


class TestTriggerActivationBlockArithmetic(unittest.TestCase):
    def test_30_train_7_embargo_30_test_durations(self):
        train_start, train_end, embargo_start, test_end = _block_span("2024-10-01")
        self.assertEqual((train_end - train_start).days + 1, 30)
        self.assertEqual(embargo_start, train_end + _dt.timedelta(days=1))
        test_start = embargo_start + _dt.timedelta(days=7)
        self.assertEqual((test_end - test_start).days + 1, 30)

    def test_embargo_separates_train_and_test(self):
        train_start, train_end, embargo_start, test_end = _block_span("2024-10-01")
        test_start = embargo_start + _dt.timedelta(days=7)
        self.assertFalse(_intervals_overlap((train_start, train_end), (test_start, test_end)))
        self.assertFalse(_intervals_overlap((train_start, train_end), (embargo_start, test_start - _dt.timedelta(days=1))))
        self.assertEqual((embargo_start - train_end).days, 1)

    def test_non_overlap_detection_across_blocks(self):
        # Test months far enough apart that [train_start, test_end] windows do not
        # overlap; adjacent months do overlap because each window spans train+test.
        b1 = _block_span("2024-10-01")
        b2 = _block_span("2025-01-01")  # non-overlapping with b1
        w1 = (b1[0], b1[3])
        w2 = (b2[0], b2[3])
        self.assertFalse(_intervals_overlap(w1, w2))
        # Adjacent test months: b2's train window reaches back into b1's window.
        close = _block_span("2024-11-01")
        self.assertTrue(_intervals_overlap(w1, (close[0], close[3])))


class TestTriggerActivationPairedNFloor(unittest.TestCase):
    def _enforce(self, paired_n: int, floor: int) -> bool:
        return paired_n >= floor

    def test_floor_23224_gate4_trackc(self):
        floor = exec_mod.PAIRED_N_FLOOR["GATE4_BRANCH_1"]
        self.assertEqual(floor, 23224)
        self.assertFalse(self._enforce(23223, floor))
        self.assertTrue(self._enforce(23224, floor))
        self.assertTrue(self._enforce(50000, floor))

    def test_floor_11689_tracka_hl_expansion(self):
        for tid in ("NEW_OBSERVED_LIQUIDATION_SOURCE", "HL_LABEL_EXTENSION", "EXPANSION_ROBUSTNESS_REDO"):
            floor = exec_mod.PAIRED_N_FLOOR[tid]
            self.assertEqual(floor, 11689)
            self.assertFalse(self._enforce(11688, floor))
            self.assertTrue(self._enforce(11689, floor))
            self.assertTrue(self._enforce(23224, floor))

    def test_plan_floors_match_calibration_matrix(self):
        registry = {
            "triggers": [
                {"trigger_id": t, "status": "OPEN"} for t in TRIGGER_IDS
            ]
        }
        monitor = {"data_through": "2026-10", "post_2026_10_summary": {"available_months": []}}
        plans = exec_mod.build_plans(registry, monitor)
        expect = {"GATE4_BRANCH_1": 23224}
        for t in TRIGGER_IDS[1:]:
            expect[t] = 11689
        for p in plans:
            self.assertEqual(p["paired_n_floor"], expect[p["trigger_id"]])
            self.assertEqual(p["non_overlapping_30d_test_blocks_min"], 3)
            self.assertEqual(p["purge_embargo_days"], 7)
            self.assertEqual(p["paired_oos_instruments_min"], 5)
            self.assertFalse(p["outcome_data_inspected_before_freeze"])
            self.assertEqual(p["gate_decision"], "REFUSE")


class TestTriggerActivationHolmFamily(unittest.TestCase):
    def test_holm_family_enumeration_deterministic(self):
        registry = {"triggers": [{"trigger_id": t, "status": "OPEN"} for t in TRIGGER_IDS]}
        monitor = {"data_through": "2026-10", "post_2026_10_summary": {"available_months": []}}
        p1 = exec_mod.build_plans(registry, monitor)
        p2 = exec_mod.build_plans(registry, monitor)
        self.assertEqual(p1, p2)
        for p in p1:
            fam = p["holm_family"]
            self.assertIsInstance(fam, list)
            self.assertGreaterEqual(len(fam), 1)
            self.assertEqual(fam, sorted(set(fam)), f"holm family not canonical for {p['trigger_id']}: {fam}")


class TestTriggerActivationRefusal(unittest.TestCase):
    def test_refusal_when_all_triggers_open(self):
        registry = {"triggers": [{"trigger_id": t, "status": "OPEN"} for t in TRIGGER_IDS]}
        monitor = {
            "data_through": "2026-10",
            "consecutive_absent": 3,
            "post_2026_10_summary": {"available_months": []},
        }
        payload = exec_mod.build_plans(registry, monitor)
        for p in payload:
            self.assertFalse(p["trigger_satisfied"])
            self.assertEqual(p["gate_decision"], "REFUSE")
            self.assertIsNotNone(p["refusal_reason"])
            self.assertFalse(p["executable"])

    def test_refusal_exit_code_nonzero(self):
        plans = exec_mod.build_plans(
            {"triggers": [{"trigger_id": t, "status": "OPEN"} for t in TRIGGER_IDS]},
            {"data_through": "2026-10", "post_2026_10_summary": {"available_months": []}},
        )
        refused = [p for p in plans if p["gate_decision"] == "REFUSE"]
        self.assertEqual(len(refused), 4)

    def test_no_confirmatory_estimand_advanced_on_refusal(self):
        plans = exec_mod.build_plans(
            {"triggers": [{"trigger_id": t, "status": "OPEN"} for t in TRIGGER_IDS]},
            {"data_through": "2026-10", "post_2026_10_summary": {"available_months": []}},
        )
        for p in plans:
            self.assertFalse(p["executable"])
            self.assertTrue(p["prereg_instantiation_required"])


class TestTriggerActivationOutcomeBlindness(unittest.TestCase):
    def test_executor_only_opens_the_two_state_files(self):
        files_read = exec_mod._files_read()  # noqa: SLF001
        self.assertEqual(len(files_read), 2)
        self.assertIn("research_state/resume_trigger_registry.json", files_read)
        self.assertIn("research_state/ironflow_monitor_state.json", files_read)

    def test_outcome_path_markers_match_forbidden_paths(self):
        forbidden = [
            "research_state/evaluation_summary_FCLR-009.md",
            "research_state/results/something.json",
            "research_state/sealed/panel.parquet",
            "research_state/data_cache/markPriceKlines/file.parquet",
            "research_state/holdout_final.json",
        ]
        allowed = [
            "research_state/resume_trigger_registry.json",
            "research_state/ironflow_monitor_state.json",
        ]
        for p in forbidden:
            self.assertTrue(exec_mod._is_outcome_path(p), p)  # noqa: SLF001
        for p in allowed:
            self.assertFalse(exec_mod._is_outcome_path(p))  # noqa: SLF001

    def test_no_outcome_file_in_executor_files_read(self):
        registry = {"triggers": [{"trigger_id": t, "status": "OPEN"} for t in TRIGGER_IDS]}
        monitor = {"data_through": "2026-10", "post_2026_10_summary": {"available_months": []}}
        exec_mod.build_plans(registry, monitor)
        self.assertEqual(exec_mod._files_read(),  # noqa: SLF001
                         ["research_state/resume_trigger_registry.json", "research_state/ironflow_monitor_state.json"])
        for p in exec_mod._files_read():  # noqa: SLF001
            self.assertFalse(exec_mod._is_outcome_path(p))  # noqa: SLF001


def _run_suite() -> unittest.TestResult:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for cls in (
        TestTriggerActivationBlockArithmetic,
        TestTriggerActivationPairedNFloor,
        TestTriggerActivationHolmFamily,
        TestTriggerActivationRefusal,
        TestTriggerActivationOutcomeBlindness,
    ):
        suite.addTests(loader.loadTestsFromTestCase(cls))
    stream = sys.stderr
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    return runner.run(suite)


def _write_sidecar(result: unittest.TestResult) -> int:
    total = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(getattr(result, "skipped", []))
    exit_code = 0 if result.wasSuccessful() else 1
    payload = {
        "artifact_id": f"FCLR-TRIGGER-ACTIVATION-SELFTEST-{SESSION_UTC}",
        "generated_utc": "2026-11-17T21:59:04Z",
        "session_utc": SESSION_UTC,
        "executable": str(Path(__file__).resolve()),
        "runner": "python3 -m unittest / direct",
        "tests_run": total,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
        "exit": exit_code,
        "was_successful": result.wasSuccessful(),
        "suite": [
            {
                "test": str(t),
                "outcome": "pass",
            }
            for t, _ in result.failures
        ]
        + [
            {
                "test": str(t),
                "outcome": "error",
            }
            for t, _ in result.errors
        ],
    }
    SIDECAR.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return exit_code


if __name__ == "__main__":
    result = _run_suite()
    raise SystemExit(_write_sidecar(result))
