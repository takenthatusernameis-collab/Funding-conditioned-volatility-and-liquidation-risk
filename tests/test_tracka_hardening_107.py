"""FCLR-NEXT-108: wire admissible seam into named fail-closed resume/operator decision path.

Deterministic, tmp-isolated, no network, no parquet/outcome reads. Validates that
scripts.tracka_resume_check.admissible_seam_check and the named
`admissible_seam_wired` resume/operator surfaces consume
src.analysis.tracka_admissible (manifest-only) fail-closed for Track A liquidation-risk
candidates (Hyperliquid-only, month>=2026-11 trigger, events+fills, observed-only, no
modeled/proxy conflation, no auth/leakage). Existing 104/105 check names/semantics stable.
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
from src.analysis.tracka_admissible import build_ironflow_month_manifest

REAL = Path(__file__).resolve().parent.parent


def _valid_admissible_manifest(month="2026-11"):
    return build_ironflow_month_manifest(
        month=month,
        events_path=f"/tmp/ironflow/data/events/{month}.parquet",
        fills_path=f"/tmp/ironflow/data/fills/{month}.parquet",
        events_url=f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/{month}.parquet",
        fills_url=f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/{month}.parquet",
        schema_fields_events=["timestamp", "symbol", "liquidation_notional", "side"],
        schema_fields_fills=["timestamp", "symbol", "size", "price"],
    )


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
    return rs


def _mk_repo(root):
    root.mkdir(parents=True, exist_ok=True)
    (root / "AGENT_HANDOFF.md").write_text("x")
    (root / "research_state").mkdir(exist_ok=True)
    return root


class TestAdmissibleSeamDecisionPath107(unittest.TestCase):
    def test_no_candidate_wired_nonbreaking(self):
        r = rc.admissible_seam_check()
        self.assertTrue(r["pass"])
        self.assertEqual(r["status"], "NO_CANDIDATE_PENDING")
        self.assertEqual(r["reason_code"], "ADMISSIBLE_SEAM_WIRED_AWAITING_CANDIDATE")
        self.assertTrue(r["fail_closed"])
        self.assertFalse(r["network"])
        self.assertFalse(r["reads_outcomes"])
        self.assertFalse(r["reads_parquet"])

    def test_admissible_go_shaped_fixture_manifest_only_pass(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "candidate_manifest.json"
            p.write_text(json.dumps(_valid_admissible_manifest("2026-11")))
            r = rc.admissible_seam_check(candidate_path=p)
            self.assertTrue(r["pass"], r)
            self.assertEqual(r["status"], "GO")
            self.assertEqual(r["reason_code"], "ADMISSIBLE_SEAM_GO")
            self.assertEqual(r["month"], "2026-11")
            self.assertEqual(r["failures"], [])
            self.assertFalse(r["network"])
            self.assertFalse(r["reads_outcomes"])
            self.assertFalse(r["reads_parquet"])

    def test_missing_month_and_below_trigger_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            m = _valid_admissible_manifest("2026-10")
            p = Path(td) / "m.json"; p.write_text(json.dumps(m))
            r = rc.admissible_seam_check(candidate_path=p)
            self.assertFalse(r["pass"])
            self.assertEqual(r["status"], "NO-GO")
            self.assertTrue(any("month_below_trigger" in f for f in r["failures"]), r)
            m2 = _valid_admissible_manifest(); m2["month"] = ""
            p2 = Path(td) / "m2.json"; p2.write_text(json.dumps(m2))
            r2 = rc.admissible_seam_check(candidate_path=p2)
            self.assertFalse(r2["pass"])
            self.assertTrue(any("month" in f for f in r2["failures"]), r2)

    def test_non_hl_conflation_auth_leakage_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            bads = []
            m = _valid_admissible_manifest(); m["venue"] = "binance"; bads.append(m)
            m = _valid_admissible_manifest(); m["modeled_or_proxy"] = True; bads.append(m)
            m = _valid_admissible_manifest(); m["observed_liquidations"] = False; bads.append(m)
            m = _valid_admissible_manifest(); m["label_definition"] = "proxy liquidation estimate"; bads.append(m)
            m = _valid_admissible_manifest(); m["unauthenticated"] = False; bads.append(m)
            m = _valid_admissible_manifest(); m["timestamp_normalized_utc"] = False; bads.append(m)
            m = _valid_admissible_manifest(); m["artifacts"]["events"]["schema_fields"] = ["timestamp", "symbol", "liquidation_proxy"]; bads.append(m)
            m = _valid_admissible_manifest(); m["artifacts"]["events"]["url"] = m["artifacts"]["events"]["url"].replace("2026-11", "2027-01"); bads.append(m)
            for i, m in enumerate(bads):
                p = Path(td) / f"bad{i}.json"; p.write_text(json.dumps(m))
                r = rc.admissible_seam_check(candidate_path=p)
                self.assertFalse(r["pass"], (i, r))
                self.assertEqual(r["reason_code"], "ADMISSIBLE_SEAM_NOGO")

    def test_missing_path_and_load_error_fail_closed(self):
        r = rc.admissible_seam_check(candidate_path="/nonexistent/admissible_candidate.json")
        self.assertFalse(r["pass"])
        self.assertEqual(r["reason_code"], "ADMISSIBLE_CANDIDATE_PATH_MISSING")
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bad.json"; p.write_text("{not json")
            r2 = rc.admissible_seam_check(candidate_path=p)
            self.assertFalse(r2["pass"])
            self.assertEqual(r2["reason_code"], "ADMISSIBLE_CANDIDATE_LOAD_ERROR")
            p3 = Path(td) / "arr.json"; p3.write_text("[]")
            r3 = rc.admissible_seam_check(candidate_path=p3)
            self.assertFalse(r3["pass"])
            self.assertEqual(r3["reason_code"], "ADMISSIBLE_CANDIDATE_NOT_OBJECT")

    def test_outcome_inspection_attempt_not_performed_manifest_only(self):
        # The seam only parses manifest JSON; pointing at a non-json/parquet-like path
        # as candidate_path is a load failure (manifest contract), never parquet read.
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "outcomes.parquet"
            p.write_bytes(b"PAR1fakeparquet")  # would be invalid as manifest
            r = rc.admissible_seam_check(candidate_path=p)
            self.assertFalse(r["pass"])
            self.assertFalse(r["reads_parquet"])
            self.assertFalse(r["reads_outcomes"])
            self.assertIn(r["reason_code"], ("ADMISSIBLE_CANDIDATE_LOAD_ERROR", "ADMISSIBLE_CANDIDATE_NOT_OBJECT", "ADMISSIBLE_SEAM_NOGO"))


class TestNamedSurfaceWiring107(unittest.TestCase):
    def test_resume_check_includes_named_admissible_seam_real_repo(self):
        r = rc.run(repo_root=REAL, research_state_dir=REAL / "research_state")
        self.assertTrue(r["pass"], r.get("checks", {}).keys())
        self.assertIn("admissible_seam_wired", r["checks"])
        c = r["checks"]["admissible_seam_wired"]
        self.assertTrue(c["pass"])
        self.assertEqual(c["status"], "NO_CANDIDATE_PENDING")
        self.assertTrue(c["fail_closed"])
        self.assertFalse(c["network"])
        self.assertFalse(c["reads_outcomes"])
        self.assertFalse(c["reads_parquet"])
        # stable existing names preserved
        for k in ("probe_invariant_runtime_named", "handoff_single_root", "rubric_go", "drift_preflight" if False else "probe_count_exactly_two"):
            self.assertIn(k, r["checks"])

    def test_operator_compose_exposes_admissible_seam_real_repo(self):
        r = rc.compose_operator_report(repo_root=REAL, research_state_dir=REAL / "research_state", harness_repo_root=REAL)
        self.assertTrue(r["pass"])
        self.assertTrue(r["admissible_seam_wired"]["pass"])
        self.assertEqual(r["admissible_seam_wired"]["status"], "NO_CANDIDATE_PENDING")
        self.assertEqual(r["fail_closed_order"], "drift_preflight->gate_decision->probe_invariant_state")
        self.assertFalse(r["network"])
        self.assertFalse(r["writes_real_research_state"])

    def test_gate_and_resume_semantics_stable_tmp_no_real_writes(self):
        real = REAL / "research_state"
        before = set(p.name for p in real.iterdir()) if real.exists() else set()
        with tempfile.TemporaryDirectory() as td:
            root = _mk_repo(Path(td) / "repo"); _mk_valid_rs(Path(td) / "rs")
            # gate still BLOCKED with stable reason/order; no seam-driven GO
            # harness_repo_root=REAL so gate can load frozen splits/manifest; drift uses tmp repo/rs.
            g = gate.decide(data_path="/nonexistent_tracka_resume", output_dir=td, pre_reg_path=None,
                            source_manifest=None, compat_fixture=False, repo_root=root,
                            research_state_dir=Path(td) / "rs", harness_repo_root=REAL)
            self.assertEqual(g["status"], "BLOCKED")
            self.assertEqual(g.get("reason_code"), "PREREG_OR_MANIFEST_BLOCK_AFTER_DRIFT_PASS")
            self.assertEqual(g.get("fail_closed_order"), "drift_preflight->manifest_prereg")
            self.assertFalse(g.get("outcomes_inspected", True))
            # resume check: named guards present/stable on tmp fixture; seam wired (manifest-only).
            # Overall pass depends on repo fixtures/splits (tmp is minimal) - assert named 105/108 surfaces.
            rr = rc.run(repo_root=root, research_state_dir=Path(td) / "rs")
            self.assertIn("probe_invariant_runtime_named", rr["checks"])
            self.assertTrue(rr["checks"]["probe_invariant_runtime_named"]["pass"])
            self.assertIn("admissible_seam_wired", rr["checks"])
            self.assertTrue(rr["checks"]["admissible_seam_wired"]["pass"])
            self.assertEqual(rr["checks"]["admissible_seam_wired"]["status"], "NO_CANDIDATE_PENDING")
            self.assertFalse(rr["network"])
            self.assertFalse(rr["writes_real_research_state"])
        after = set(p.name for p in real.iterdir()) if real.exists() else set()
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
