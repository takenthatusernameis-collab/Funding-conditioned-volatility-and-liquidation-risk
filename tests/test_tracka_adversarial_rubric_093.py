#!/usr/bin/env python3
"""FCLR-NEXT-093 Step 4: adversarial Track A rubric edge fixtures.

Explicit fail fixtures for: auth/key/signature/requester-pays, incomplete
coverage/<5 symbols, non-Hyperliquid merge/venue, modeled-as-observed/proxy,
schema mismatch. Hyperliquid-only. These tests are deterministic and must stay
green while blocked.
"""
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.tracka_rubric import assess_candidate, RUBRIC


def valid_hyperliquid():
    return {
        "venue": "hyperliquid",
        "unauthenticated": True,
        "requires_api_key": False,
        "requires_signature": False,
        "requester_pays": False,
        "observed_liquidations": True,
        "modeled_or_proxy": False,
        "merges_non_hyperliquid": False,
        "symbol_count": 6,
        "completeness_documented": True,
        "license_ok": True,
        "license_spdx": "CC-BY-4.0",
        "schema_fields": ["timestamp", "symbol", "liquidation_notional", "mark_price"],
    }


class TestAdversarialRubric093(unittest.TestCase):
    def test_valid_hyperliquid_observed_is_go(self):
        r = assess_candidate(valid_hyperliquid())
        self.assertTrue(r["go"])
        self.assertEqual(r["verdict"], "GO")
        self.assertEqual(r["failures"], [])

    def test_reject_auth_required(self):
        c = valid_hyperliquid(); c["unauthenticated"] = False
        r = assess_candidate(c)
        self.assertFalse(r["go"]); self.assertIn("not_unauthenticated", r["failures"])

    def test_reject_api_key(self):
        c = valid_hyperliquid(); c["requires_api_key"] = True
        r = assess_candidate(c)
        self.assertFalse(r["go"]); self.assertIn("requires_api_key", r["failures"])

    def test_reject_signature(self):
        c = valid_hyperliquid(); c["requires_signature"] = True
        r = assess_candidate(c)
        self.assertFalse(r["go"]); self.assertIn("requires_signature", r["failures"])

    def test_reject_requester_pays(self):
        c = valid_hyperliquid(); c["requester_pays"] = True
        r = assess_candidate(c)
        self.assertFalse(r["go"]); self.assertIn("requester_pays", r["failures"])

    def test_reject_incomplete_symbol_coverage(self):
        c = valid_hyperliquid(); c["symbol_count"] = 4
        r = assess_candidate(c)
        self.assertFalse(r["go"]); self.assertIn("incomplete_symbol_coverage", r["failures"])

    def test_reject_zero_symbols(self):
        c = valid_hyperliquid(); c["symbol_count"] = 0; c["symbols"] = []
        r = assess_candidate(c)
        self.assertFalse(r["go"]); self.assertIn("incomplete_symbol_coverage", r["failures"])

    def test_reject_non_hyperliquid_venue(self):
        c = valid_hyperliquid(); c["venue"] = "binance"
        r = assess_candidate(c)
        self.assertFalse(r["go"]); self.assertIn("non_hyperliquid_venue", r["failures"])

    def test_reject_non_hyperliquid_merge(self):
        c = valid_hyperliquid(); c["merges_non_hyperliquid"] = True
        r = assess_candidate(c)
        self.assertFalse(r["go"]); self.assertIn("non_hyperliquid_merge", r["failures"])

    def test_reject_modeled_as_observed(self):
        c = valid_hyperliquid(); c["observed_liquidations"] = False
        r = assess_candidate(c)
        self.assertFalse(r["go"]); self.assertIn("not_observed_liquidations", r["failures"])

    def test_reject_proxy_or_modeled_flag(self):
        c = valid_hyperliquid(); c["modeled_or_proxy"] = True
        r = assess_candidate(c)
        self.assertFalse(r["go"]); self.assertIn("modeled_or_proxy", r["failures"])

    def test_reject_schema_mismatch_missing_liquidation_notional(self):
        c = valid_hyperliquid(); c["schema_fields"] = ["timestamp", "symbol", "mark_price"]
        r = assess_candidate(c)
        self.assertFalse(r["go"]); self.assertIn("schema_mismatch", r["failures"])

    def test_reject_schema_mismatch_missing_symbol(self):
        c = valid_hyperliquid(); c["schema_fields"] = ["timestamp", "liquidation_notional"]
        r = assess_candidate(c)
        self.assertFalse(r["go"]); self.assertIn("schema_mismatch", r["failures"])

    def test_reject_missing_completeness_doc(self):
        c = valid_hyperliquid(); c["completeness_documented"] = False
        r = assess_candidate(c)
        self.assertFalse(r["go"]); self.assertIn("completeness_not_documented", r["failures"])

    def test_reject_license_not_ok(self):
        c = valid_hyperliquid(); c["license_ok"] = False
        r = assess_candidate(c)
        self.assertFalse(r["go"]); self.assertIn("license_not_ok", r["failures"])

    def test_multi_failure_case(self):
        c = {"venue": "okx", "unauthenticated": False, "requires_api_key": True,
             "requester_pays": True, "observed_liquidations": False, "modeled_or_proxy": True,
             "merges_non_hyperliquid": True, "symbol_count": 2, "completeness_documented": False,
             "license_ok": False, "schema_fields": ["foo"]}
        r = assess_candidate(c)
        self.assertFalse(r["go"])
        for f in ["non_hyperliquid_venue","not_unauthenticated","requires_api_key","requester_pays",
                  "not_observed_liquidations","modeled_or_proxy","non_hyperliquid_merge",
                  "incomplete_symbol_coverage","completeness_not_documented","license_not_ok","schema_mismatch"]:
            self.assertIn(f, r["failures"])

    def test_rubric_is_hyperliquid_only(self):
        self.assertTrue(RUBRIC["hyperliquid_only"])
        self.assertTrue(RUBRIC["observed_liquidations_only"])
        self.assertTrue(RUBRIC["unauthenticated_only"])
        self.assertFalse(RUBRIC.get("allow_modeled", False))


if __name__ == "__main__":
    unittest.main()
