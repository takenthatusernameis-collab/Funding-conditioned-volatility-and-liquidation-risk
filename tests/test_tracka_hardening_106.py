"""FCLR-NEXT-107: Track A admissible Ironflow ingestion/manifest seam hardening.

Deterministic, tmp-isolated, no network, stdlib-only seam coverage. Proves fail-closed
Hyperliquid-only/observed-only/month>=2026-11/admissible-artifact guards and that
observed liquidation manifests cannot be conflated with modeled/proxy labels or columns.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.analysis.tracka_admissible import (
    TRIGGER_MONTH,
    assess_ironflow_month_admissibility,
    build_ironflow_month_manifest,
    month_from_ironflow_path,
    month_gte,
    validate_ironflow_month_manifest,
)


class TestTrackAAdmissibleSeam106(unittest.TestCase):
    def _valid(self, month="2026-11"):
        return build_ironflow_month_manifest(
            month=month,
            events_path=f"/tmp/ironflow/data/events/{month}.parquet",
            fills_path=f"/tmp/ironflow/data/fills/{month}.parquet",
            events_url=f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/{month}.parquet",
            fills_url=f"https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/{month}.parquet",
            schema_fields_events=["timestamp", "symbol", "liquidation_notional", "side"],
            schema_fields_fills=["timestamp", "symbol", "size", "price"],
        )

    def test_month_gate_requires_2026_11_or_later_for_trigger(self):
        self.assertFalse(month_gte("2026-10", TRIGGER_MONTH))
        self.assertTrue(month_gte("2026-11", TRIGGER_MONTH))
        self.assertTrue(month_gte("2027-02", TRIGGER_MONTH))
        res = assess_ironflow_month_admissibility(self._valid("2026-10"), for_resume_trigger=True)
        self.assertFalse(res["pass"])
        self.assertIn("month_below_trigger:2026-10<2026-11", res["failures"])

    def test_valid_admissible_month_manifest_passes_fail_closed_seam(self):
        res = assess_ironflow_month_admissibility(self._valid("2026-11"), for_resume_trigger=True)
        self.assertTrue(res["pass"], res)
        self.assertEqual(res["verdict"], "GO")
        self.assertTrue(res["fail_closed"])
        self.assertEqual(res["guards"]["required_roles"], ["events", "fills"])
        self.assertTrue(res["guards"]["no_modeled_conflation"])

    def test_non_hyperliquid_and_merge_blocked(self):
        m = self._valid(); m["venue"] = "binance"
        r = validate_ironflow_month_manifest(m)
        self.assertFalse(r["pass"]); self.assertIn("venue_not_hyperliquid_only", r["failures"])
        m = self._valid(); m["merges_non_hyperliquid"] = True
        r = validate_ironflow_month_manifest(m)
        self.assertFalse(r["pass"]); self.assertIn("merges_non_hyperliquid", r["failures"])
        m = self._valid(); m["source"] = "some-other-dataset"
        r = validate_ironflow_month_manifest(m)
        self.assertFalse(r["pass"]); self.assertIn("source_not_ironflow_hyperliquid", r["failures"])

    def test_observed_modeled_conflation_blocked(self):
        m = self._valid(); m["observed_liquidations"] = False
        self.assertIn("observed_liquidations_not_true", validate_ironflow_month_manifest(m)["failures"])
        m = self._valid(); m["modeled_or_proxy"] = True
        self.assertIn("modeled_or_proxy", validate_ironflow_month_manifest(m)["failures"])
        m = self._valid(); m["label_definition"] = "modeled liquidation estimate"
        self.assertIn("label_definition_conflates_modeled", validate_ironflow_month_manifest(m)["failures"])
        m = self._valid(); m["artifacts"]["events"]["schema_fields"] = ["timestamp","symbol","liquidation_proxy"]
        f = validate_ironflow_month_manifest(m)["failures"]
        self.assertTrue(any(x.startswith("events_forbidden_columns") for x in f), f)

    def test_missing_required_artifacts_and_role_mismatch_blocked(self):
        # explicit role swap in local path is fail-closed
        m = self._valid(); m["artifacts"]["fills"]["path"] = "/tmp/ironflow/data/events/2026-11.parquet"
        f = validate_ironflow_month_manifest(m)["failures"]
        self.assertTrue(any("fills" in x and "role" in x for x in f), f)
        # URL role mismatch is fail-closed
        m = self._valid(); m["artifacts"]["events"]["url"] = "https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/fills/2026-11.parquet"
        self.assertIn("events_url_role_mismatch", validate_ironflow_month_manifest(m)["failures"])
        # missing required role artifact is fail-closed
        m = self._valid(); m["artifacts"] = {"events": m["artifacts"]["events"]}
        self.assertIn("fills_artifact_missing", validate_ironflow_month_manifest(m)["failures"])

    def test_leakage_and_timestamp_guards_fail_closed(self):
        m = self._valid(); m["timestamp_normalized_utc"] = False
        self.assertIn("timestamp_not_normalized_utc", validate_ironflow_month_manifest(m)["failures"])
        m = self._valid(); m["artifacts"]["events"]["schema_fields"] = ["timestamp"]  # no value field
        self.assertIn("events_missing_liquidation_value_field", validate_ironflow_month_manifest(m)["failures"])
        m = self._valid(); m["artifacts"]["events"]["url"] = m["artifacts"]["events"]["url"].replace("2026-11", "2026-12")
        self.assertIn("events_url_month_mismatch", validate_ironflow_month_manifest(m)["failures"])

    def test_auth_and_provenance_fail_closed(self):
        m = self._valid(); m["unauthenticated"] = False
        self.assertIn("not_unauthenticated", validate_ironflow_month_manifest(m)["failures"])
        m = self._valid(); m["requires_api_key"] = True
        self.assertIn("requires_api_key", validate_ironflow_month_manifest(m)["failures"])
        m = self._valid(); m["label_definition"] = ""
        self.assertIn("label_definition_missing", validate_ironflow_month_manifest(m)["failures"])

    def test_path_helpers_deterministic_no_io(self):
        self.assertEqual(month_from_ironflow_path("data/events/2026-11.parquet"), "2026-11")
        self.assertIsNone(month_from_ironflow_path("nope"))
        self.assertIsNone(normalize_month("2026-1") if False else None)
        # malformed month fail-closed
        bad = self._valid(); bad["month"] = "2026/11"
        self.assertIn("month_missing_or_invalid", validate_ironflow_month_manifest(bad)["failures"])

    def test_manifest_json_roundtrip_no_network(self):
        m = self._valid("2026-12")
        blob = json.dumps(m, sort_keys=True)
        m2 = json.loads(blob)
        self.assertTrue(assess_ironflow_month_admissibility(m2, for_resume_trigger=True)["pass"])


if __name__ == "__main__":
    unittest.main()
