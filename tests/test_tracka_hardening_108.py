"""FCLR-NEXT-109: end-to-end trigger/resume-consumer admissible-seam contract.

Deterministic, tmp-isolated, no network, no parquet/outcome reads, no real
research_state writes. Verifies stable fail-closed reason codes/order and that
outcome inspection is refused across gate/harness/resume_check/operator paths.
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


def _mk_valid_rs(rs):
    rs.mkdir(parents=True, exist_ok=True)
    p = rs / "ironflow_probe_20990101T000001Z.json"
    p.write_text(json.dumps({"probe_id": "ironflow_probe_20990101T000001Z",
                             "probe_invariant_runtime": {"pass": True, "total": 2, "invariant": "x",
                                                         "live_probes": ["ironflow_probe_20990101T000001Z.json"],
                                                         "digests": ["ironflow_probe_digest_latest.json"]}}))
    os.utime(p, (time.time() + 1, time.time() + 1))
    (rs / "ironflow_probe_digest_latest.json").write_text("{}")
    (rs / "alt_source_scan_latest.json").write_text("{}")
    (rs / "alt_source_deep_review_latest.md").write_text("x")


def _mk_repo(root):
    root.mkdir(parents=True, exist_ok=True)
    (root / "AGENT_HANDOFF.md").write_text("x")
    (root / "research_state").mkdir(exist_ok=True)


def _write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj))
    return str(path)


def _outcome_loader_must_not_run(*_a, **_k):
    raise AssertionError("outcome loader must not run")


class TestGateSeamContract108(unittest.TestCase):
    def test_gate_go_seam_missing_prereg_blocks_stable_codes(self):
        with tempfile.TemporaryDirectory() as td:
            ap = _write(Path(td) / "adm.json", _valid_admissible())
            r = gate.decide("/nonexistent", td, pre_reg_path=None,
                            admissible_manifest_path=ap, harness_repo_root=REAL)
            self.assertEqual(r["status"], "BLOCKED")
            self.assertEqual(r["reason_code"], "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")
            self.assertEqual(r["fail_closed_order"], "drift_preflight->admissible_seam->manifest_prereg")
            self.assertFalse(r["outcomes_inspected"])
            self.assertTrue(r["admissible_seam_wired"]["pass"])
            self.assertEqual(r["admissible_seam_wired"]["status"], "GO")
            self.assertEqual(r["admissible_seam_wired"]["month"], "2026-11")
            self.assertFalse(r["network"])

    def test_gate_go_seam_prereg_present_data_missing_still_blocks_no_outcomes(self):
        with tempfile.TemporaryDirectory() as td:
            ap = _write(Path(td) / "adm.json", _valid_admissible())
            pp = _write(Path(td) / "prereg.json", {"ok": 1})
            r = gate.decide("/nonexistent", td, pre_reg_path=pp,
                            admissible_manifest_path=ap, harness_repo_root=REAL)
            self.assertEqual(r["status"], "BLOCKED")
            self.assertEqual(r["reason_code"], "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")
            self.assertEqual(r["fail_closed_order"], "drift_preflight->admissible_seam->manifest_prereg")
            self.assertFalse(r["outcomes_inspected"])
            self.assertTrue(r["admissible_seam_wired"]["pass"])
            self.assertIn("data", r.get("reason", "").lower())

    def test_gate_nogo_seam_blocks_before_prereg_and_outcomes(self):
        with tempfile.TemporaryDirectory() as td:
            ap = _write(Path(td) / "adm.json", _valid_admissible(month="2026-10"))
            r = gate.decide("/nonexistent", td, pre_reg_path=None,
                            admissible_manifest_path=ap, harness_repo_root=REAL)
            self.assertEqual(r["status"], "BLOCKED")
            self.assertEqual(r["reason_code"], "ADMISSIBLE_SEAM_NOGO_BEFORE_PREREG")
            self.assertEqual(r["fail_closed_order"], "drift_preflight->admissible_seam->manifest_prereg")
            self.assertFalse(r["outcomes_inspected"])
            self.assertFalse(r["admissible_seam_wired"]["pass"])
            self.assertEqual(r["admissible_seam_wired"]["status"], "NO-GO")
            self.assertTrue(r["admissible_seam_wired"]["failures"])


class TestHarnessTriggerConsumer108(unittest.TestCase):
    def _harness(self):
        return FCLR010Harness(repo_root=REAL)

    def test_harness_nogo_seam_no_prereg_refuses_outcome_loader(self):
        h = self._harness()
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            r = h.evaluate_forward(data, td, pre_reg_path=None,
                                   admissible_manifest=_valid_admissible(venue="binance"),
                                   outcome_loader=_outcome_loader_must_not_run)
            self.assertEqual(r["status"], "BLOCKED")
            self.assertEqual(r["reason_code"], "ADMISSIBLE_SEAM_NOGO_BEFORE_PREREG")
            self.assertFalse(r["outcomes_inspected"])
            self.assertFalse(r["admissible_seam_wired"]["pass"])

    def test_harness_go_seam_no_prereg_refuses_outcome_loader(self):
        h = self._harness()
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            r = h.evaluate_forward(data, td, pre_reg_path=None,
                                   admissible_manifest=_valid_admissible(),
                                   outcome_loader=_outcome_loader_must_not_run)
            self.assertEqual(r["status"], "BLOCKED")
            self.assertTrue(r["prereg_required"])
            self.assertFalse(r["outcomes_inspected"])
            self.assertTrue(r["admissible_seam_wired"]["pass"])

    def test_harness_nogo_seam_with_prereg_refuses_outcomes_before_data_success(self):
        h = self._harness()
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            prereg = Path(td) / "prereg.json"; prereg.write_text("{}")
            r = h.evaluate_forward(data, td, pre_reg_path=prereg,
                                   admissible_manifest=_valid_admissible(modeled_or_proxy=True),
                                   outcome_loader=_outcome_loader_must_not_run)
            self.assertEqual(r["status"], "BLOCKED")
            self.assertEqual(r["reason_code"], "ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES")
            self.assertFalse(r["outcomes_inspected"])
            self.assertFalse(r["admissible_seam_wired"]["pass"])

    def test_harness_go_seam_with_prereg_and_data_allows_loader_only_after_gates(self):
        h = self._harness()
        seen = {"ran": False}

        def loader(_):
            seen["ran"] = True
            return {"ok": True}

        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d"; data.mkdir()
            prereg = Path(td) / "prereg.json"; prereg.write_text("{}")
            r = h.evaluate_forward(data, td, pre_reg_path=prereg,
                                   admissible_manifest=_valid_admissible(),
                                   outcome_loader=loader)
            self.assertEqual(r["status"], "READY_FROZEN", r)
            self.assertFalse(r["outcomes_inspected"])
            self.assertTrue(seen["ran"])
            self.assertEqual(r["outcomes_loaded"], {"ok": True})
            self.assertTrue(r["admissible_seam_wired"]["pass"])


class TestResumeCheckOperatorSeamSurfaces108(unittest.TestCase):
    def test_resume_check_pending_go_nogo_expose_stable_fields(self):
        pending = rc.run(repo_root=REAL, research_state_dir=REAL / "research_state")
        self.assertTrue(pending["pass"], pending["checks"]["admissible_seam_wired"])
        w = pending["checks"]["admissible_seam_wired"]
        self.assertEqual(w["status"], "NO_CANDIDATE_PENDING")
        self.assertEqual(w["reason_code"], "ADMISSIBLE_SEAM_WIRED_AWAITING_CANDIDATE")
        self.assertFalse(w["network"]); self.assertFalse(w["reads_outcomes"]); self.assertFalse(w["reads_parquet"])

        with tempfile.TemporaryDirectory() as td:
            ap = _write(Path(td) / "go.json", _valid_admissible())
            go = rc.run(repo_root=REAL, research_state_dir=REAL / "research_state", admissible_candidate_path=ap)
            self.assertTrue(go["checks"]["admissible_seam_wired"]["pass"])
            self.assertEqual(go["checks"]["admissible_seam_wired"]["status"], "GO")
            self.assertEqual(go["checks"]["admissible_seam_wired"]["reason_code"], "ADMISSIBLE_SEAM_GO")
            self.assertEqual(go["checks"]["admissible_seam_wired"]["month"], "2026-11")
            an = _write(Path(td) / "no.json", _valid_admissible(month="2026-10"))
            nogo = rc.run(repo_root=REAL, research_state_dir=REAL / "research_state", admissible_candidate_path=an)
            self.assertFalse(nogo["checks"]["admissible_seam_wired"]["pass"])
            self.assertEqual(nogo["checks"]["admissible_seam_wired"]["status"], "NO-GO")
            self.assertEqual(nogo["checks"]["admissible_seam_wired"]["reason_code"], "ADMISSIBLE_SEAM_NOGO")
            self.assertTrue(nogo["checks"]["admissible_seam_wired"]["failures"])

    def test_operator_exposes_stable_seam_fields_for_fixtures(self):
        with tempfile.TemporaryDirectory() as td:
            ap = _write(Path(td) / "go.json", _valid_admissible())
            r = rc.compose_operator_report(repo_root=REAL, research_state_dir=REAL / "research_state",
                                           harness_repo_root=REAL, admissible_candidate_path=ap)
            self.assertEqual(r["fail_closed_order"], "drift_preflight->gate_decision->probe_invariant_state")
            self.assertFalse(r["network"]); self.assertFalse(r["writes_real_research_state"])
            self.assertEqual(r["admissible_seam_wired"]["status"], "GO")
            self.assertEqual(r["admissible_seam_wired"]["reason_code"], "ADMISSIBLE_SEAM_GO")
            self.assertEqual(r["gate_decision"]["status"], "BLOCKED")
            self.assertEqual(r["gate_decision"]["reason_code"], "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")
            self.assertFalse(r["gate_decision"]["outcomes_inspected"])
            an = _write(Path(td) / "no.json", _valid_admissible(venue="binance"))
            rn = rc.compose_operator_report(repo_root=REAL, research_state_dir=REAL / "research_state",
                                            harness_repo_root=REAL, admissible_candidate_path=an)
            self.assertEqual(rn["admissible_seam_wired"]["status"], "NO-GO")
            self.assertEqual(rn["gate_decision"]["reason_code"], "ADMISSIBLE_SEAM_NOGO_BEFORE_PREREG")


class TestRemainingGuardsFailClosed108(unittest.TestCase):
    def test_unwired_manifest_fields_leakage_auth_month_guards_fail_closed(self):
        cases = [
            ("month", _valid_admissible(month="2026-10"), "month_below_trigger"),
            ("auth", _valid_admissible(requires_signature=True), "requires_signature"),
            ("leakage_label", _valid_admissible(label_definition="proxy liquidation estimate"), "label_definition_conflates_modeled"),
            ("conflation", _valid_admissible(modeled_or_proxy=True), "modeled_or_proxy"),
            ("venue", _valid_admissible(venue="binance"), "venue_not_hyperliquid_only"),
            ("timestamp", _valid_admissible(timestamp_normalized_utc=False), "timestamp_not_normalized_utc"),
        ]
        for name, manifest, needle in cases:
            r = rc.admissible_seam_check(candidate_manifest=manifest)
            self.assertFalse(r["pass"], name)
            self.assertEqual(r["status"], "NO-GO", name)
            self.assertFalse(r["reads_outcomes"], name)
            self.assertFalse(r["reads_parquet"], name)
            self.assertTrue(any(needle in f for f in r["failures"]), (name, r["failures"]))

    def test_harness_manifest_path_nogo_refuses_outcomes(self):
        h = FCLR010Harness(repo_root=REAL)
        with tempfile.TemporaryDirectory() as td:
            ap = _write(Path(td) / "adm.json", _valid_admissible(unauthenticated=False))
            data = Path(td) / "d"; data.mkdir()
            prereg = Path(td) / "p.json"; prereg.write_text("{}")
            r = h.evaluate_forward(data, td, pre_reg_path=prereg,
                                   admissible_manifest_path=ap,
                                   outcome_loader=_outcome_loader_must_not_run)
            self.assertEqual(r["status"], "BLOCKED")
            self.assertEqual(r["reason_code"], "ADMISSIBLE_SEAM_NOGO_BEFORE_OUTCOMES")
            self.assertFalse(r["outcomes_inspected"])


class TestNoRealResearchStateWrites108(unittest.TestCase):
    def test_no_real_research_state_writes(self):
        real = REAL / "research_state"
        before = set(p.name for p in real.iterdir()) if real.exists() else set()
        with tempfile.TemporaryDirectory() as td:
            ap = _write(Path(td) / "adm.json", _valid_admissible())
            gate.decide("/nonexistent", td, pre_reg_path=None, admissible_manifest_path=ap, harness_repo_root=REAL)
            rc.compose_operator_report(repo_root=REAL, research_state_dir=REAL / "research_state",
                                       harness_repo_root=REAL, admissible_candidate_path=ap)
        after = set(p.name for p in real.iterdir()) if real.exists() else set()
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
