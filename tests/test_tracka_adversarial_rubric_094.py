#!/usr/bin/env python3
"""FCLR-NEXT-094: stricter adversarial Track A rubric + offline resume proof.

Extends 093 coverage with explicit fail fixtures for: partial month coverage claims,
conflicting schema fields, symbol aliases/duplicates, mixed observed+modeled rows,
missing timestamp normalization, venue casing/alias spoofing. All deterministic.
Also enforces offline resume-path timing (<10s).
"""
import unittest
import json
import time
import subprocess
import sys
import tempfile
from pathlib import Path

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
        "symbols": ["BTC", "ETH", "SOL", "AVAX", "ARB", "DOGE"],
        "completeness_documented": True,
        "license_ok": True,
        "license_spdx": "CC-BY-4.0",
        "schema_fields": ["timestamp", "symbol", "liquidation_notional", "mark_price"],
        "timestamp_normalized_utc": True,
    }


class TestAdversarialRubric094(unittest.TestCase):
    def test_partial_month_coverage_flag_rejected(self):
        c = valid_hyperliquid(); c["partial_month_coverage"] = True
        r = assess_candidate(c)
        self.assertFalse(r["go"])
        self.assertIn("partial_month_coverage", r["failures"])

    def test_partial_month_via_zero_complete_months_rejected(self):
        c = valid_hyperliquid(); c["coverage_months"] = 1; c["coverage_complete_months"] = 0
        r = assess_candidate(c)
        self.assertFalse(r["go"])
        self.assertIn("partial_month_coverage", r["failures"])

    def test_conflicting_schema_fields_rejected(self):
        c = valid_hyperliquid(); c["schema_conflicts"] = ["timestamp type differs", "symbol encoding"]
        r = assess_candidate(c)
        self.assertFalse(r["go"])
        self.assertIn("schema_conflicts", r["failures"])

    def test_schema_conflicts_bool_rejected(self):
        c = valid_hyperliquid(); c["schema_conflicts"] = True
        r = assess_candidate(c)
        self.assertFalse(r["go"])
        self.assertIn("schema_conflicts", r["failures"])

    def test_duplicate_symbols_rejected(self):
        c = valid_hyperliquid(); c["symbols"] = ["BTC", "ETH", "SOL", "AVAX", "ARB", "BTC"]
        r = assess_candidate(c)
        self.assertFalse(r["go"])
        self.assertIn("duplicate_symbols", r["failures"])
        self.assertIn("incomplete_symbol_coverage", r["failures"])

    def test_symbol_alias_casing_normalized_to_go(self):
        c = valid_hyperliquid(); c["symbols"] = ["btc", "eth", "sol", "avax", "arb", "doge"]
        r = assess_candidate(c)
        self.assertTrue(r["go"], r["failures"])
        self.assertEqual(r["symbol_count"], 6)

    def test_symbol_count_claim_conflict_rejected(self):
        c = valid_hyperliquid(); c["symbol_count"] = 4  # conflicts with 6 unique symbols
        r = assess_candidate(c)
        self.assertFalse(r["go"])
        self.assertIn("incomplete_symbol_coverage", r["failures"])

    def test_mixed_observed_modeled_rows_rejected(self):
        c = valid_hyperliquid(); c["row_mix_observed_modeled"] = True
        r = assess_candidate(c)
        self.assertFalse(r["go"])
        self.assertIn("mixed_observed_modeled_rows", r["failures"])

    def test_missing_timestamp_normalization_rejected(self):
        c = valid_hyperliquid(); c["timestamp_normalized_utc"] = False
        r = assess_candidate(c)
        self.assertFalse(r["go"])
        self.assertIn("timestamp_not_normalized", r["failures"])

    def test_venue_casing_accepted_when_canonical(self):
        c = valid_hyperliquid(); c["venue"] = "HyperLiquid"
        r = assess_candidate(c)
        self.assertTrue(r["go"], r["failures"])

    def test_venue_alias_hl_accepted(self):
        c = valid_hyperliquid(); c["venue"] = "HL"
        r = assess_candidate(c)
        self.assertTrue(r["go"], r["failures"])

    def test_venue_alias_spoof_rejected(self):
        c = valid_hyperliquid(); c["venue"] = "hyperliquid"; c["venue_alias_spoof"] = True
        r = assess_candidate(c)
        self.assertFalse(r["go"])
        self.assertIn("non_hyperliquid_venue", r["failures"])

    def test_unknown_venue_alias_rejected(self):
        c = valid_hyperliquid(); c["venue"] = "hyperliquid_v2"
        r = assess_candidate(c)
        self.assertFalse(r["go"])
        self.assertIn("non_hyperliquid_venue", r["failures"])

    def test_fail_closed_missing_fields(self):
        r = assess_candidate({})
        self.assertFalse(r["go"])
        self.assertGreater(len(r["failures"]), 3)

    def test_failures_deterministic_sorted(self):
        c = valid_hyperliquid(); c["partial_month_coverage"] = True; c["row_mix_observed_modeled"] = True
        r1 = assess_candidate(c); r2 = assess_candidate(c)
        self.assertEqual(r1["failures"], r2["failures"])
        self.assertEqual(r1["failures"], sorted(r1["failures"]))


class TestOfflineResumeProof094(unittest.TestCase):
    """Single-command-block equivalent offline resume path, enforced <10s."""

    def test_rubric_harness_prereg_offline_under_10s(self):
        t = time.time()
        # rubric import/assess
        verdict = assess_candidate(valid_hyperliquid())["verdict"]
        self.assertEqual(verdict, "GO")
        # fixture manifest load
        root = Path(__file__).parent.parent
        fx = root / "tests" / "fixtures" / "tracka" / "manifest.json"
        self.assertTrue(fx.exists(), "Track A fixtures missing; run generate_tracka_fixtures.py")
        m = json.loads(fx.read_text())
        self.assertTrue(m["splits"]["frozen_before_outcomes"])
        self.assertGreaterEqual(len(m["symbols"]), 5)
        # harness cold + prereg block
        from scripts.fclr010_harness import FCLR010Harness
        h = FCLR010Harness()
        cfg = h.get_frozen_config()
        self.assertEqual(cfg["experiment_id"], "FCLR-010")
        blocked = h.evaluate_forward(Path("/nonexistent"), Path(tempfile.mkdtemp()), pre_reg_path=None)
        self.assertEqual(blocked["status"], "BLOCKED")
        dt = time.time() - t
        self.assertLess(dt, 10.0, f"offline resume proof took {dt:.3f}s")

    def test_harness_cli_offline_under_10s(self):
        t = time.time()
        r = subprocess.run([sys.executable, "scripts/fclr010_harness.py"], capture_output=True, text=True, timeout=15)
        dt = time.time() - t
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertLess(dt, 10.0, f"harness CLI took {dt:.3f}s")


if __name__ == "__main__":
    unittest.main()
