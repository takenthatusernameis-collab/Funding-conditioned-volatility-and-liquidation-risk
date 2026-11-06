"""FCLR-NEXT-111: E2E trigger-artifact fixture matrix for guarded real execution entrypoints.

Deterministic, tmp-isolated, no network, no parquet/outcome reads, no real research_state writes.
Covers READY_FROZEN -> explicit-loader-called-once and every blocked branch
(NO-GO seam, missing prereg, GO+missing prereg detail, missing data, leakage/auth/month/missing-field/conflation)
against the guarded_execute entrypoint contract surface used by fclr010_execute.py:main and
fclr010_execute_fast.py:main. Asserts loader/parquet reader never called on blocked paths.
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
from scripts.fclr010_guarded_entry import guarded_execute, refusal_payload
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
    raise AssertionError("outcome/parquet loader must not run on blocked branch")


def _loader_called_once(data_path, context=None):
    return {"loaded": str(data_path), "context": context, "rows": 0}


class TestGuardedEntryReadOnlyFrozen111(unittest.TestCase):
    """Entrypoint contract: blocked branches refuse before any parquet/outcome read."""

    def test_guarded_execute_missing_prereg_exposes_110_detail(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            adm = _write(Path(td) / "adm.json", _valid_admissible())
            res = guarded_execute(
                data_path=data, pre_reg_path=None, repo_root=REAL,
                source_manifest=None, admissible_manifest_path=adm,
                outcome_loader=_loader_must_not_run, allow_default_loader=False,
            )
            self.assertEqual(res["status"], "BLOCKED")
            self.assertFalse(res["outcomes_inspected"])
            # 110 normalization: seam GO but prereg missing => PREREG_REQUIRED_BEFORE_DATA_LOAD
            # with explicit seam_go_prereg_required + ADMISSIBLE_SEAM_GO_PREREG_REQUIRED detail
            self.assertIn(res.get("reason_code"), ("PREREG_REQUIRED_BEFORE_DATA_LOAD", "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS"))
            self.assertTrue(res.get("seam_go_prereg_required"))
            self.assertEqual(res.get("reason_code_detail"), "ADMISSIBLE_SEAM_GO_PREREG_REQUIRED")
            self.assertNotEqual(res.get("data_loaded_implicitly"), True)
            self.assertFalse(res["canonical_outputs_mutated"])
            self.assertFalse(res["network"])
            self.assertFalse(res["writes_real_research_state"])

    def test_guarded_execute_nogo_seam_refuses_before_outcomes(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            prereg = Path(td) / "p.json"; prereg.write_text("{}")
            adm = _write(Path(td) / "adm.json", _valid_admissible(venue="binance"))
            res = guarded_execute(
                data_path=data, pre_reg_path=prereg, repo_root=REAL,
                admissible_manifest_path=adm,
                outcome_loader=_loader_must_not_run, allow_default_loader=False,
            )
            self.assertEqual(res["status"], "BLOCKED")
            self.assertEqual(res.get("reason_code"), "ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES")
            self.assertFalse(res["outcomes_inspected"])
            self.assertNotEqual(res.get("data_loaded_implicitly"), True)

    def test_guarded_execute_missing_data_after_gates_is_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            prereg = Path(td) / "p.json"; prereg.write_text("{}")
            adm = _write(Path(td) / "adm.json", _valid_admissible())
            res = guarded_execute(
                data_path=Path(td) / "nope", pre_reg_path=prereg, repo_root=REAL,
                admissible_manifest_path=adm,
                outcome_loader=_loader_must_not_run, allow_default_loader=False,
            )
            self.assertEqual(res["status"], "BLOCKED")
            self.assertFalse(res["outcomes_inspected"])
            self.assertIn("data", res.get("reason", "").lower())
            self.assertNotEqual(res.get("data_loaded_implicitly"), True)

    def test_guarded_execute_no_candidate_seam_pending_still_blocked_no_prereg(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            res = guarded_execute(
                data_path=data, pre_reg_path=None, repo_root=REAL,
                admissible_manifest_path=None,
                outcome_loader=_loader_must_not_run, allow_default_loader=False,
            )
            self.assertEqual(res["status"], "BLOCKED")
            self.assertFalse(res["outcomes_inspected"])
            # No candidate => seam not GO; reason_code is None (prereg block, no seam surface)
            rc = res.get("reason_code")
            self.assertTrue(rc is None or rc == "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")
            self.assertNotEqual(res.get("data_loaded_implicitly"), True)

    def test_guarded_execute_ready_frozen_calls_loader_once(self):
        seen = {"ran": 0}
        def loader(dp, ctx=None):
            seen["ran"] += 1
            return {"loaded": str(dp), "ctx": ctx}
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            prereg = Path(td) / "p.json"; prereg.write_text("{}")
            adm = _write(Path(td) / "adm.json", _valid_admissible())
            res = guarded_execute(
                data_path=data, pre_reg_path=prereg, repo_root=REAL,
                admissible_manifest_path=adm,
                outcome_loader=loader, loader_context={"train": ["2025-11-01"], "test": ["2026-10-31"]},
                allow_default_loader=False,
            )
            self.assertEqual(res["status"], "READY_FROZEN", res)
            self.assertEqual(seen["ran"], 1)
            self.assertFalse(res.get("outcomes_inspected") is True)
            self.assertFalse(res.get("data_loaded_implicitly") is True)
            self.assertEqual(res["data_load_mode"], "EXPLICIT_LOADER_AFTER_GATES")

    def test_guarded_execute_refusal_payload_stable_shape(self):
        payload = refusal_payload(
            reason="test refusal", reason_code="TEST_BLOCKED", fast_path=True,
            guard={"status": "BLOCKED", "outcomes_inspected": False},
        )
        self.assertEqual(payload["status"], "BLOCKED")
        self.assertFalse(payload["outcomes_inspected"])
        self.assertFalse(payload["data_loaded_implicitly"])
        self.assertFalse(payload["canonical_outputs_mutated"])
        self.assertFalse(payload["network"])
        self.assertFalse(payload["writes_real_research_state"])
        self.assertEqual(payload["reason"], "test refusal")
        self.assertEqual(payload["reason_code"], "TEST_BLOCKED")
        self.assertTrue(payload["fast_path"])
        self.assertEqual(payload["guarded_execution_contract"], "fclr_next_111")


class TestEntryPointWiringMatrix111(unittest.TestCase):
    """E2E matrix across gate + harness + guarded entrypoint surfaces."""

    CASES = [
        ("go_2026-11", _valid_admissible("2026-11"), True),
        ("nogo_month_2026-10", _valid_admissible("2026-10"), False),
        ("nogo_venue_binance", _valid_admissible(venue="binance"), False),
        ("nogo_missing_field", {k: v for k, v in _valid_admissible().items() if k != "venue"}, False),
        ("nogo_leakage_label", _valid_admissible(label_definition="proxy liquidation estimate"), False),
        ("nogo_auth_signature", _valid_admissible(requires_signature=True), False),
        ("nogo_conflation_modeled", _valid_admissible(modeled_or_proxy=True), False),
        ("nogo_merges_non_hl", _valid_admissible(merges_non_hyperliquid=True), False),
    ]

    def test_matrix_gate_harness_entrypoint_no_outcome_reads(self):
        h = FCLR010Harness(repo_root=REAL)
        for name, manifest, expect_go in self.CASES:
            with tempfile.TemporaryDirectory() as td:
                ap = _write(Path(td) / f"{name}.json", manifest)
                prereg = Path(td) / "p.json"; prereg.write_text("{}")
                data = Path(td) / "d"; data.mkdir()

                gr = guarded_execute(
                    data_path=data, pre_reg_path=prereg, repo_root=REAL,
                    admissible_manifest_path=ap,
                    outcome_loader=(_loader_called_once if expect_go else _loader_must_not_run),
                    allow_default_loader=False,
                )
                hr = h.execute_ready_data_load(
                    data_path=data, pre_reg_path=prereg,
                    admissible_manifest=manifest,
                    outcome_loader=(_loader_called_once if expect_go else _loader_must_not_run),
                )

                self.assertFalse(gr.get("outcomes_inspected"), name)
                self.assertFalse(hr.get("outcomes_inspected"), name)
                self.assertFalse(gr["network"], name)
                self.assertFalse(gr["writes_real_research_state"], name)
                self.assertNotEqual(gr.get("data_loaded_implicitly"), True, name)
                self.assertFalse(gr["canonical_outputs_mutated"], name)

                if expect_go:
                    self.assertEqual(gr["status"], "READY_FROZEN", (name, gr))
                    self.assertEqual(hr["status"], "READY_FROZEN", (name, hr))
                else:
                    self.assertEqual(gr["status"], "BLOCKED", (name, gr))
                    self.assertEqual(hr["status"], "BLOCKED", (name, hr))


class TestNoRealResearchStateWrites111(unittest.TestCase):
    def test_no_real_research_state_writes_across_entrypoint(self):
        real = REAL / "research_state"
        before = {p.name for p in real.iterdir()} if real.exists() else set()
        with tempfile.TemporaryDirectory() as td:
            ap = _write(Path(td) / "adm.json", _valid_admissible())
            prereg = Path(td) / "p.json"; prereg.write_text("{}")
            data = Path(td) / "d"; data.mkdir()
            guarded_execute(
                data_path=data, pre_reg_path=prereg, repo_root=REAL,
                admissible_manifest_path=ap,
                outcome_loader=_loader_must_not_run, allow_default_loader=False,
            )
            FCLR010Harness(repo_root=REAL).execute_ready_data_load(
                data_path=data, pre_reg_path=prereg,
                admissible_manifest=_valid_admissible(), outcome_loader=_loader_must_not_run,
            )
        after = {p.name for p in real.iterdir()} if real.exists() else set()
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
