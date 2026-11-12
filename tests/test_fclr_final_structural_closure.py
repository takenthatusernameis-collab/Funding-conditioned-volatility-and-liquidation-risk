#!/usr/bin/env python3
"""Tests for scripts/fclr_final_structural_closure.py.

Uses minimal in-tmpdir fixtures (a fixture registry + fixture verdict file)
so the generator is exercised offline without touching sealed artifacts.
Asserts: every input ID present exactly once; every §17 condition evaluated
(and not met); resume_trigger_registry.json predicates well-formed;
unknown/missing verdicts flagged, not silently dropped; deterministic output.
"""
from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

import scripts.fclr_final_structural_closure as gen


def _write_fixture_state(tmp: Path) -> None:
    state = tmp / "research_state"
    state.mkdir(parents=True, exist_ok=True)
    (state / "hypothesis_registry.json").write_text(
        json.dumps(
            {
                "hypotheses": [
                    {
                        "id": "FIX_H_ALPHA",
                        "type": "primary",
                        "status": "NOT_SUPPORTED",
                        "last_verdict": "forecast_gate_NOT_MET",
                        "evidence": "rel QLIKE 1.14% < 2% floor; CI crosses zero",
                    },
                    {
                        "id": "FIX_H_BETA",
                        "type": "secondary",
                        "status": "FRAGILE",
                        "last_verdict": "robustness_gate_FRAGILE",
                        "evidence": "LOIO 4/8 < 6; placebo null",
                    },
                    {
                        "id": "FIX_H_GAMMA",
                        "type": "primary",
                        "evidence": "no status or last_verdict fields",
                    },
                ]
            },
            indent=2,
        )
    )
    (state / "experiment_frontier.json").write_text("[]")
    (state / "evaluation_summary_FIX_EXP_001.json").write_text(
        json.dumps(
            {
                "experiment_id": "FIX_EXP_001",
                "verdict": "NOT_MET",
                "gate_pass": False,
                "gate": {
                    "materiality_ge_2pct": False,
                    "ci_upper_below_zero": False,
                    "holm_pass": False,
                },
            }
        )
    )
    (state / "terminal_structural_stop_liq_stop.md").write_text(
        "# stop\n**NOT_MET**\n"
    )
    (state / "alt_source_probe_audit_20260101T000000Z.json").write_text(
        json.dumps({"families_probed": 2, "all_no_go": True})
    )


class TestFixtureIdsExactlyOnce(unittest.TestCase):
    def test_all_fixture_ids_present_exactly_once(self):
        with TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            _write_fixture_state(tmp)
            gen.RESEARCH_STATE = tmp / "research_state"
            utc = "2026-11-12T21:15:00Z"
            md, closure, registry = gen.generate(utc)
            ids = [r["id"] for r in closure["rows"]]
            expected = [
                "FIX_H_ALPHA",
                "FIX_H_BETA",
                "FIX_H_GAMMA",
                "FIX_EXP_001",
                "alt_source_probe_audit_20260101T000000Z",
                "terminal_structural_stop_liq_stop",
            ]
            self.assertEqual(sorted(ids), sorted(expected))
            self.assertEqual(len(ids), len(set(ids)), "duplicate row IDs present")
            self.assertEqual(closure["n_rows"], len(ids))


class TestSection17ConditionsEvaluated(unittest.TestCase):
    def test_every_section_17_condition_present_and_not_met(self):
        with TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            _write_fixture_state(tmp)
            gen.RESEARCH_STATE = tmp / "research_state"
            _, closure, _ = gen.generate("2026-11-12T21:15:00Z")
            for row in closure["rows"]:
                self.assertFalse(row["section_17_promotion_met"])
                conds = row["section_17_conditions"]
                for cond in gen.SECTION_17_CONDITIONS:
                    self.assertIn(cond, conds, f"{row['id']} missing {cond}")
                    self.assertFalse(
                        conds[cond],
                        f"{row['id']} condition {cond} unexpectedly met",
                    )
            self.assertTrue(closure["section_17_all_conditions_not_met"])
            self.assertEqual(closure["n_section_17_promotion_met"], 0)


class TestResumeTriggerRegistryWellFormed(unittest.TestCase):
    def test_exactly_four_triggers_with_well_formed_predicates(self):
        with TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            _write_fixture_state(tmp)
            gen.RESEARCH_STATE = tmp / "research_state"
            _, _, registry = gen.generate("2026-11-12T21:15:00Z")
            trigger_ids = [t["trigger_id"] for t in registry["triggers"]]
            self.assertEqual(
                trigger_ids,
                [
                    "GATE4_BRANCH_1",
                    "NEW_OBSERVED_LIQUIDATION_SOURCE",
                    "HL_LABEL_EXTENSION",
                    "EXPANSION_ROBUSTNESS_REDO",
                ],
            )
            for trig in registry["triggers"]:
                for key in [
                    "trigger_id",
                    "machine_predicate",
                    "required_evidence_artifact",
                    "gate_protocol",
                    "priority",
                    "status",
                    "do_not_act_until_satisfied",
                ]:
                    self.assertIn(key, trig)
                self.assertEqual(trig["status"], "OPEN")
                self.assertTrue(trig["do_not_act_until_satisfied"])
                self.assertIsInstance(trig["machine_predicate"], dict)
                self.assertIsInstance(trig["priority"], int)


class TestUnknownVerdictsFlaggedNotDropped(unittest.TestCase):
    def test_missing_verdict_still_emits_row(self):
        with TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            _write_fixture_state(tmp)
            gen.RESEARCH_STATE = tmp / "research_state"
            _, closure, _ = gen.generate("2026-11-12T21:15:00Z")
            ids = {r["id"] for r in closure["rows"]}
            self.assertIn("FIX_H_GAMMA", ids)
            row = next(r for r in closure["rows"] if r["id"] == "FIX_H_GAMMA")
            self.assertEqual(row["verdict"], "unknown")
            self.assertFalse(row["section_17_promotion_met"])


class TestDeterminism(unittest.TestCase):
    def test_same_inputs_byte_identical_except_timestamp(self):
        with TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            _write_fixture_state(tmp)
            gen.RESEARCH_STATE = tmp / "research_state"
            utc = "2026-11-12T21:15:00Z"
            md1, c1, r1 = gen.generate(utc)
            md2, c2, r2 = gen.generate(utc)
            self.assertEqual(md1, md2)
            self.assertEqual(json.dumps(c1, sort_keys=True), json.dumps(c2, sort_keys=True))
            self.assertEqual(json.dumps(r1, sort_keys=True), json.dumps(r2, sort_keys=True))
            # Sanity: generated timestamp reflects the input.
            self.assertEqual(c1["generated_utc"], utc)
            self.assertEqual(r1["generated_utc"], utc)


if __name__ == "__main__":
    unittest.main()
