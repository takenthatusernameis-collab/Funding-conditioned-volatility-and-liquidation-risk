"""FCLR-NEXT-110: actual harness data-load refusal + explicit seam-GO/prereg reason surface.

Deterministic, tmp-isolated, no network, no parquet/outcome reads, no real
research_state writes. Preserves 108 stable semantics.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts import tracka_resume_check as rc
from scripts import tracka_resume_gate as gate
from scripts import tracka_operator_report as op
from scripts.fclr010_harness import FCLR010Harness
from src.analysis.tracka_admissible import build_ironflow_month_manifest

REAL = Path(__file__).resolve().parent.parent


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


def _loader_must_not_run(*_a, **_k):
    raise AssertionError("outcome/parquet loader must not run")


class TestExplicitSeamGoPreregSurface110(unittest.TestCase):
    def test_gate_go_seam_missing_prereg_exposes_explicit_surface_preserves_108(self):
        with tempfile.TemporaryDirectory() as td:
            ap = _write(Path(td) / "adm.json", _valid_admissible())
            r = gate.decide("/nonexistent", td, pre_reg_path=None,
                            admissible_manifest_path=ap, harness_repo_root=REAL)
            # 108-preserved stable semantics
            self.assertEqual(r["status"], "BLOCKED")
            self.assertEqual(r["reason_code"], "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")
            self.assertEqual(r["fail_closed_order"], "drift_preflight->admissible_seam->manifest_prereg")
            self.assertFalse(r["outcomes_inspected"])
            self.assertTrue(r["admissible_seam_wired"]["pass"])
            # 110 explicit surface
            self.assertEqual(r.get("seam_go_prereg_required"), True)
            self.assertEqual(r.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED")

    def test_gate_nogo_seam_no_prereg_not_go_prereg_surface(self):
        with tempfile.TemporaryDirectory() as td:
            ap = _write(Path(td) / "adm.json", _valid_admissible(month="2026-10"))
            r = gate.decide("/nonexistent", td, pre_reg_path=None,
                            admissible_manifest_path=ap, harness_repo_root=REAL)
            self.assertEqual(r["reason_code"], "ADMISSIBLE_SEAM_NOGO_BEFORE_PREREG")
            self.assertNotEqual(r.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED")
            self.assertFalse(r.get("seam_go_prereg_required") is True)

    def test_operator_exposes_explicit_go_prereg_surface(self):
        with tempfile.TemporaryDirectory() as td:
            ap = _write(Path(td) / "go.json", _valid_admissible())
            r = rc.compose_operator_report(repo_root=REAL, research_state_dir=REAL / "research_state",
                                           harness_repo_root=REAL, admissible_candidate_path=ap)
            self.assertEqual(r["gate_decision"]["status"], "BLOCKED")
            self.assertFalse(r["gate_decision"]["outcomes_inspected"])
            self.assertEqual(r["gate_decision"]["reason_code"], "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")
            self.assertEqual(r["gate_decision"].get("seam_go_prereg_required"), True)
            self.assertEqual(r["gate_decision"].get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED")
            self.assertEqual(r["admissible_seam_wired"]["reason_code"], "ADMISSIBLE_SEAM_GO")

    def test_operator_cli_exposes_surface(self):
        with tempfile.TemporaryDirectory() as td:
            ap = _write(Path(td) / "go.json", _valid_admissible())
            # compose path used by CLI
            r = rc.compose_operator_report(repo_root=REAL, research_state_dir=REAL / "research_state",
                                           harness_repo_root=REAL, admissible_candidate_path=ap)
            payload = json.dumps(r, sort_keys=True)
            self.assertIn("ADMISSIBLE_SEAM_GO_PREREG_REQUIRED", payload)
            self.assertIn('"seam_go_prereg_required": true', payload)


class TestHarnessActualDataLoadRefusal110(unittest.TestCase):
    def _h(self):
        return FCLR010Harness(repo_root=REAL)

    def test_guarded_data_load_refuses_missing_prereg(self):
        h = self._h()
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            r = h.execute_ready_data_load(
                data_path=data, pre_reg_path=None,
                admissible_manifest=_valid_admissible(),
                outcome_loader=_loader_must_not_run,
            )
            self.assertEqual(r["status"], "BLOCKED")
            self.assertFalse(r["outcomes_inspected"])
            self.assertFalse(r.get("data_loaded") is True)
            # 132 G2 schema parity with gate/operator: seam GO + missing prereg =>
            # PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS with ADMISSIBLE_SEAM_GO_PREREG_REQUIRED detail.
            self.assertEqual(r.get("reason_code"), "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")
            self.assertEqual(r.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED")
            self.assertTrue(r.get("seam_go_prereg_required") is True)

    def test_guarded_data_load_refuses_nogo_seam_with_prereg(self):
        h = self._h()
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            prereg = Path(td) / "p.json"; prereg.write_text("{}")
            r = h.execute_ready_data_load(
                data_path=data, pre_reg_path=prereg,
                admissible_manifest=_valid_admissible(venue="binance"),
                outcome_loader=_loader_must_not_run,
            )
            self.assertEqual(r["status"], "BLOCKED")
            self.assertEqual(r.get("reason_code"), "ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES")
            self.assertFalse(r["outcomes_inspected"])

    def test_guarded_data_load_refuses_missing_data_after_gates(self):
        h = self._h()
        with tempfile.TemporaryDirectory() as td:
            prereg = Path(td) / "p.json"; prereg.write_text("{}")
            r = h.execute_ready_data_load(
                data_path=Path(td) / "nope", pre_reg_path=prereg,
                admissible_manifest=_valid_admissible(),
                outcome_loader=_loader_must_not_run,
            )
            self.assertEqual(r["status"], "BLOCKED")
            self.assertFalse(r["outcomes_inspected"])
            self.assertIn("data", r.get("reason", "").lower())

    def test_guarded_data_load_allows_only_after_ready_gates(self):
        h = self._h()
        seen = {"ran": 0}
        def loader(p):
            seen["ran"] += 1
            return {"loaded": str(p)}
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            prereg = Path(td) / "p.json"; prereg.write_text("{}")
            r = h.execute_ready_data_load(
                data_path=data, pre_reg_path=prereg,
                admissible_manifest=_valid_admissible(),
                outcome_loader=loader,
            )
            self.assertEqual(r["status"], "READY_FROZEN", r)
            self.assertEqual(seen["ran"], 1)
            self.assertEqual(r.get("outcomes_loaded"), {"loaded": str(data)})
            self.assertFalse(r.get("outcomes_inspected") is True)

    def test_guarded_data_load_no_loader_refuses_parquet_read_path(self):
        # actual harness must not silently read parquet; without approved loader it refuses/fails closed
        h = self._h()
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            (data / "x.parquet").write_bytes(b"PAR1fake")
            prereg = Path(td) / "p.json"; prereg.write_text("{}")
            r = h.execute_ready_data_load(
                data_path=data, pre_reg_path=prereg,
                admissible_manifest=_valid_admissible(),
                outcome_loader=None,
            )
            # must be fail-closed: either READY_FROZEN with no implicit parquet load, or explicit refusal
            self.assertIn(r["status"], ("READY_FROZEN", "BLOCKED"))
            self.assertFalse(r.get("data_loaded_implicitly") is True)
            self.assertFalse(r.get("outcomes_inspected") is True)


class TestMatrixGuards110(unittest.TestCase):
    CASES = [
        ("go", _valid_admissible(), True),
        ("nogo_month", _valid_admissible(month="2026-10"), False),
        ("nogo_missing_field", {k: v for k, v in _valid_admissible().items() if k != "venue"}, False),
        ("nogo_leakage", _valid_admissible(label_definition="proxy liquidation estimate"), False),
        ("nogo_auth", _valid_admissible(requires_signature=True), False),
        ("nogo_conflation", _valid_admissible(modeled_or_proxy=True), False),
    ]

    def test_matrix_gate_harness_operator_no_outcome_reads(self):
        h = FCLR010Harness(repo_root=REAL)
        for name, manifest, expect_go in self.CASES:
            with tempfile.TemporaryDirectory() as td:
                ap = _write(Path(td) / f"{name}.json", manifest)
                prereg = Path(td) / "p.json"; prereg.write_text("{}")
                data = Path(td) / "d"; data.mkdir()
                gr = gate.decide(str(data), td, pre_reg_path=prereg,
                                 admissible_manifest_path=ap, harness_repo_root=REAL)
                hr = h.evaluate_forward(data, td, pre_reg_path=prereg,
                                        admissible_manifest=manifest,
                                        outcome_loader=_loader_must_not_run if not expect_go else (lambda _: {"ok": 1}))
                opr = rc.compose_operator_report(repo_root=REAL, research_state_dir=REAL / "research_state",
                                                 harness_repo_root=REAL, admissible_candidate_path=ap)
                self.assertFalse(gr.get("outcomes_inspected"), name)
                self.assertFalse(hr.get("outcomes_inspected"), name)
                self.assertFalse(opr.get("network"), name)
                if expect_go:
                    self.assertEqual(gr["admissible_seam_wired"]["status"], "GO", name)
                    self.assertEqual(hr["status"], "READY_FROZEN", (name, hr))
                    self.assertEqual(opr["admissible_seam_wired"]["status"], "GO", name)
                else:
                    self.assertEqual(hr["status"], "BLOCKED", (name, hr))
                    self.assertFalse(opr["admissible_seam_wired"]["pass"], name)


class TestNoRealResearchStateWrites110(unittest.TestCase):
    def test_no_real_research_state_writes(self):
        real = REAL / "research_state"
        before = {p.name for p in real.iterdir()} if real.exists() else set()
        with tempfile.TemporaryDirectory() as td:
            ap = _write(Path(td) / "adm.json", _valid_admissible())
            gate.decide("/nonexistent", td, pre_reg_path=None, admissible_manifest_path=ap, harness_repo_root=REAL)
            rc.compose_operator_report(repo_root=REAL, research_state_dir=REAL / "research_state",
                                       harness_repo_root=REAL, admissible_candidate_path=ap)
            FCLR010Harness(repo_root=REAL).execute_ready_data_load(
                data_path=Path(td) / "d", pre_reg_path=None,
                admissible_manifest=_valid_admissible(), outcome_loader=_loader_must_not_run)
        after = {p.name for p in real.iterdir()} if real.exists() else set()
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
