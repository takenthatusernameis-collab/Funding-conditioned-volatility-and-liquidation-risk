#!/usr/bin/env python3
"""FCLR-NEXT-096: uncovered adversarial Track A rubric gaps (additive, fail-closed).

Covers 096 requirements: observed Hyperliquid access/dataset provenance required in
strict manifest mode (fail-closed when missing), label-definition/observed semantics
required in strict mode, machine-verifiable block/month evidence for >=1 complete month
and >=3x30d block claims, symbol-map proof completeness vs claimed symbols (opt-in),
and raw-epoch timestamp normalization/unit evidence. Deterministic, no network.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.tracka_rubric import assess_candidate


def base():
    return {
        "venue": "hyperliquid", "unauthenticated": True, "requires_api_key": False,
        "requires_signature": False, "requester_pays": False, "observed_liquidations": True,
        "modeled_or_proxy": False, "merges_non_hyperliquid": False, "symbol_count": 6,
        "symbols": ["BTC", "ETH", "SOL", "AVAX", "ARB", "DOGE"], "completeness_documented": True,
        "license_ok": True, "license_spdx": "CC-BY-4.0",
        "schema_fields": ["timestamp", "symbol", "liquidation_notional"],
        "timestamp_normalized_utc": True,
        "source_url": "https://example.invalid/hl", "dataset_id": "hl-obs", "label_definition": "exchange_observed_liquidation_fill",
    }


class TestAdversarialRubric096(unittest.TestCase):
    def test_strict_access_provenance_missing_rejected(self):
        c = base(); c["access_provenance_required"] = True; c["source_url"] = ""; c["dataset_id"] = ""
        c.pop("access_provenance", None); c.pop("download_path", None); c.pop("repo_url", None)
        r = assess_candidate(c); self.assertFalse(r["go"]); self.assertIn("observed_access_provenance_missing", r["failures"])

    def test_strict_access_provenance_present_ok(self):
        c = base(); c["access_provenance_required"] = True
        r = assess_candidate(c); self.assertNotIn("observed_access_provenance_missing", r["failures"])

    def test_strict_label_definition_missing_rejected(self):
        c = base(); c["access_provenance_required"] = True; c["label_definition"] = ""
        r = assess_candidate(c); self.assertFalse(r["go"]); self.assertIn("label_definition_missing", r["failures"])

    def test_label_definition_required_flag_rejected(self):
        c = base(); c["label_definition_required"] = True; c["label_definition"] = "   "
        r = assess_candidate(c); self.assertFalse(r["go"]); self.assertIn("label_definition_missing", r["failures"])

    def test_coverage_claim_without_machine_month_evidence_rejected(self):
        c = base(); c["coverage_months"] = 3; c["coverage_evidence_required"] = True
        r = assess_candidate(c); self.assertFalse(r["go"]); self.assertIn("coverage_month_evidence_missing", r["failures"])

    def test_coverage_claim_with_complete_months_list_ok(self):
        c = base(); c["coverage_months"] = 3; c["coverage_evidence_required"] = True
        c["complete_months_list"] = ["2026-11", "2026-12", "2027-01"]
        r = assess_candidate(c); self.assertNotIn("coverage_month_evidence_missing", r["failures"])

    def test_claims_3x30d_blocks_without_evidence_rejected(self):
        c = base(); c["claims_3x30d_blocks"] = True; c["block_count"] = 2
        r = assess_candidate(c); self.assertFalse(r["go"]); self.assertIn("block_count_evidence_insufficient", r["failures"])

    def test_claims_3x30d_blocks_without_block_evidence_list_rejected(self):
        c = base(); c["claims_3x30d_blocks"] = True; c["block_count"] = 3
        r = assess_candidate(c); self.assertFalse(r["go"]); self.assertIn("block_count_evidence_insufficient", r["failures"])

    def test_claims_3x30d_blocks_with_evidence_ok(self):
        c = base(); c["claims_3x30d_blocks"] = True; c["block_count"] = 3
        c["block_evidence"] = [{"start": "2026-11-01", "end": "2026-11-30"}, {"start": "2026-12-01", "end": "2026-12-30"}, {"start": "2027-01-01", "end": "2027-01-30"}]
        r = assess_candidate(c); self.assertNotIn("block_count_evidence_insufficient", r["failures"])

    def test_symbol_proof_incomplete_vs_claimed_symbols_rejected(self):
        c = base(); c["canonical_symbol_map"] = {"btc": "BTC"}; c["symbol_normalization_proof"] = {"normalized_map": {"BTC": "BTC"}}
        c["symbol_proof_covers_claimed_required"] = True
        r = assess_candidate(c); self.assertFalse(r["go"]); self.assertIn("symbol_normalization_proof_incomplete", r["failures"])

    def test_symbol_proof_covers_all_claimed_ok(self):
        c = base(); c["symbols"] = ["BTC", "ETH"]; c["symbol_count"] = 2
        c["canonical_symbol_map"] = {"btc": "BTC", "eth": "ETH"}; c["symbol_normalization_proof"] = {"normalized_map": {"BTC": "BTC", "ETH": "ETH"}}
        c["symbol_proof_covers_claimed_required"] = True
        r = assess_candidate(c); self.assertNotIn("symbol_normalization_proof_incomplete", r["failures"])

    def test_raw_epoch_fields_without_normalization_rejected(self):
        c = base(); c["timestamp_normalized_utc"] = False; c["raw_epoch_fields"] = ["ts_ms"]
        r = assess_candidate(c); self.assertFalse(r["go"]); self.assertIn("timestamp_unit_ambiguous", r["failures"])

    def test_raw_epoch_fields_with_normalization_ok(self):
        c = base(); c["raw_epoch_fields"] = ["ts_ms"]; c["timestamp_normalized_utc"] = True
        r = assess_candidate(c); self.assertNotIn("timestamp_unit_ambiguous", r["failures"])

    def test_strict_observed_semantics_requires_label(self):
        c = base(); c["strict_observed_semantics"] = True; c["label_definition"] = ""
        r = assess_candidate(c); self.assertFalse(r["go"]); self.assertIn("label_definition_missing", r["failures"])

    def test_base_candidate_still_go(self):
        r = assess_candidate(base()); self.assertTrue(r["go"], r["failures"])


if __name__ == "__main__":
    unittest.main()
