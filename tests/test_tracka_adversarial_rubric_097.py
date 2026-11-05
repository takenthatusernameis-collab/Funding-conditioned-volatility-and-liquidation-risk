#!/usr/bin/env python3
"""FCLR-NEXT-097: strict full-manifest defaults + minimal_fixture_compat proof.

097 measurable delta:
- strict_tracka_manifest default path fail-closes for GO-shaped observed Hyperliquid
  claims that only satisfy minimal fields (no machine-verifiable provenance/label/
  coverage/block/raw-epoch evidence).
- minimal_fixture_compat preserves 093-096 legacy minimal fixture behavior.
- deterministic, no network, no writes.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.tracka_rubric import (
    assess_candidate, assess_strict_manifest, assess_minimal_fixture,
)


def minimal_go_shaped():
    # GO-shaped by minimal fields only (093-style) — must be NO-GO in strict mode.
    return {
        "venue": "hyperliquid", "unauthenticated": True, "requires_api_key": False,
        "requires_signature": False, "requester_pays": False, "observed_liquidations": True,
        "modeled_or_proxy": False, "merges_non_hyperliquid": False, "symbol_count": 6,
        "symbols": ["BTC", "ETH", "SOL", "AVAX", "ARB", "DOGE"], "completeness_documented": True,
        "license_ok": True, "license_spdx": "CC-BY-4.0",
        "schema_fields": ["timestamp", "symbol", "liquidation_notional"],
        "timestamp_normalized_utc": True,
    }


def full_strict_manifest_go():
    c = minimal_go_shaped()
    c.update({
        "source_url": "https://example.invalid/hyperliquid/observed_liquidations",
        "dataset_id": "hl-observed-liquidations-v1",
        "access_provenance": "unauthenticated public dataset; Hyperliquid-only; observed fills",
        "label_definition": "exchange_observed_liquidation_fill_notional",
        "coverage_months": 1,
        "coverage_evidence_required": True,
        "complete_months_list": ["2026-11"],
        "claims_3x30d_blocks": True,
        "block_count": 3,
        "block_evidence": [
            {"start": "2026-11-01", "end": "2026-11-30", "days": 30},
            {"start": "2026-12-01", "end": "2026-12-30", "days": 30},
            {"start": "2027-01-01", "end": "2027-01-30", "days": 30},
        ],
        "canonical_symbol_map": {"BTC": "BTC", "ETH": "ETH", "SOL": "SOL", "AVAX": "AVAX", "ARB": "ARB", "DOGE": "DOGE"},
        "symbol_normalization_proof": {"normalized_map": {"BTC": "BTC", "ETH": "ETH", "SOL": "SOL", "AVAX": "AVAX", "ARB": "ARB", "DOGE": "DOGE"}},
        "symbol_proof_covers_claimed_required": True,
    })
    return c


class TestStrictManifestDefaults097(unittest.TestCase):
    def test_minimal_go_shaped_is_nogo_in_strict_default(self):
        r = assess_strict_manifest(minimal_go_shaped())
        self.assertFalse(r["go"])
        self.assertTrue(r["strict_tracka_manifest"])
        self.assertTrue(any(f in r["failures"] for f in (
            "observed_access_provenance_missing", "label_definition_missing")), r["failures"])

    def test_minimal_go_shaped_preserved_in_compat(self):
        r = assess_minimal_fixture(minimal_go_shaped())
        self.assertTrue(r["go"], r["failures"])
        self.assertTrue(r["minimal_fixture_compat"])

    def test_default_legacy_call_preserves_minimal_go_shaped(self):
        r = assess_candidate(minimal_go_shaped())
        self.assertTrue(r["go"], r["failures"])
        self.assertFalse(r["strict_tracka_manifest"])

    def test_full_manifest_go_in_strict(self):
        r = assess_strict_manifest(full_strict_manifest_go())
        self.assertTrue(r["go"], r["failures"])

    def test_strict_requires_label_definition(self):
        c = full_strict_manifest_go(); c["label_definition"] = ""
        r = assess_strict_manifest(c)
        self.assertFalse(r["go"]); self.assertIn("label_definition_missing", r["failures"])

    def test_strict_requires_access_provenance(self):
        c = full_strict_manifest_go()
        for k in ("source_url", "dataset_id", "access_provenance", "download_path", "repo_url"):
            c.pop(k, None)
        r = assess_strict_manifest(c)
        self.assertFalse(r["go"]); self.assertIn("observed_access_provenance_missing", r["failures"])

    def test_strict_requires_machine_month_evidence_when_months_claimed(self):
        c = full_strict_manifest_go(); c.pop("complete_months_list", None)
        r = assess_strict_manifest(c)
        self.assertFalse(r["go"]); self.assertIn("coverage_month_evidence_missing", r["failures"])

    def test_strict_requires_block_evidence_when_3x30d_claimed(self):
        c = full_strict_manifest_go(); c["block_evidence"] = []
        r = assess_strict_manifest(c)
        self.assertFalse(r["go"]); self.assertIn("block_count_evidence_insufficient", r["failures"])

    def test_strict_rejects_raw_epoch_without_normalization(self):
        c = full_strict_manifest_go(); c["raw_epoch_fields"] = ["ts_ms"]; c["timestamp_normalized_utc"] = False
        r = assess_strict_manifest(c)
        self.assertFalse(r["go"])
        self.assertTrue("timestamp_unit_ambiguous" in r["failures"] or "timestamp_not_normalized" in r["failures"])

    def test_strict_rejects_incomplete_symbol_proof_when_required(self):
        c = full_strict_manifest_go(); c["symbols"] = ["BTC", "ETH", "SOL", "AVAX", "ARB", "DOGE"]; c["symbol_count"] = 6
        c["symbol_normalization_proof"] = {"normalized_map": {"BTC": "BTC"}}
        r = assess_strict_manifest(c)
        self.assertFalse(r["go"]); self.assertTrue(any(f in r["failures"] for f in ("symbol_normalization_proof_incomplete","symbol_normalization_proof_missing")), r["failures"])

    def test_compat_explicit_flag_does_not_apply_strict_defaults(self):
        c = minimal_go_shaped(); c["access_provenance_required"] = False
        r = assess_candidate(c, minimal_fixture_compat=True)
        self.assertTrue(r["go"], r["failures"])

    def test_non_go_shaped_not_forced_into_strict_provenance_path(self):
        # non-observed candidate should not gain strict GO-shaped provenance auto-fail beyond existing rules
        c = minimal_go_shaped(); c["observed_liquidations"] = False
        r = assess_strict_manifest(c)
        self.assertFalse(r["go"])
        # should fail for not_observed_liquidations; strict auto-provenance is for GO-shaped observed HL only
        self.assertIn("not_observed_liquidations", r["failures"])


if __name__ == "__main__":
    unittest.main()
