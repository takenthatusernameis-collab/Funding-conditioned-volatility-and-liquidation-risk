#!/usr/bin/env python3
"""Fixture tests for scripts/fclr_ironflow_bulk.py (no network, no data-cache reads).

Covers the fail-closed contracts the next campaign depends on:
  * month/range expansion is strict and total;
  * schema validation rejects drift;
  * verify detects hash mismatch, missing sidecar, and absent objects;
  * fetch is a cache hit when a verified object already exists;
  * the manifest is deterministic and sorted.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "fclr_ironflow_bulk.py"

_spec = importlib.util.spec_from_file_location("fclr_ironflow_bulk", SCRIPT)
bulk = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(bulk)

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
except Exception:  # pragma: no cover
    pa = None
    pq = None


def _write_parquet(path: Path, columns: dict) -> None:
    table = pa.table({k: v for k, v in columns.items()})
    pq.write_table(table, path)


class TempCacheMixin(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self._orig_cache = bulk.CACHE
        bulk.CACHE = self.root / "data_cache" / "ironflow_bulk"

    def tearDown(self) -> None:
        bulk.CACHE = self._orig_cache
        self._tmp.cleanup()


class TestMonthExpansion(unittest.TestCase):
    def test_single_month(self):
        self.assertEqual(bulk.expand_months("2025-06"), ["2025-06"])

    def test_range_is_inclusive_and_ordered(self):
        self.assertEqual(
            bulk.expand_months("2025-11..2026-02"),
            ["2025-11", "2025-12", "2026-01", "2026-02"],
        )

    def test_reversed_range_refused(self):
        with self.assertRaises(bulk.BulkError):
            bulk.expand_months("2026-02..2025-11")

    def test_malformed_months_refused(self):
        for bad in ("2025-6", "2025-13", "202506", "2025/06", ""):
            with self.assertRaises(bulk.BulkError):
                bulk.expand_months(bad)

    def test_unknown_dataset_refused(self):
        with self.assertRaises(bulk.BulkError):
            bulk.expand_datasets("candles_1h,nope")


class TestSchemaValidation(TempCacheMixin):
    @unittest.skipIf(pa is None, "pyarrow unavailable")
    def test_valid_schema_accepted(self):
        p = bulk.local_path("candles_1h", "2025-06")
        p.parent.mkdir(parents=True, exist_ok=True)
        _write_parquet(p, {"timestamp": [1, 2], "market": ["BTC-PERP"] * 2, "close": [1.0, 2.0]})
        info = bulk.validate_schema("candles_1h", p)
        self.assertEqual(info["rows"], 2)
        self.assertIn("close", info["columns"])

    @unittest.skipIf(pa is None, "pyarrow unavailable")
    def test_missing_column_fails_closed(self):
        p = bulk.local_path("funding", "2025-06")
        p.parent.mkdir(parents=True, exist_ok=True)
        _write_parquet(p, {"timestamp": [1], "market": ["BTC-PERP"]})  # no funding_rate
        with self.assertRaises(bulk.BulkError) as ctx:
            bulk.validate_schema("funding", p)
        self.assertIn("funding_rate", str(ctx.exception))

    @unittest.skipIf(pa is None, "pyarrow unavailable")
    def test_unreadable_file_fails_closed(self):
        p = bulk.local_path("candles_1h", "2025-06")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"not a parquet")
        with self.assertRaises(bulk.BulkError):
            bulk.validate_schema("candles_1h", p)


class TestVerifyObject(TempCacheMixin):
    @unittest.skipIf(pa is None, "pyarrow unavailable")
    def test_ok_when_sidecar_matches(self):
        p = bulk.local_path("candles_1h", "2025-06")
        p.parent.mkdir(parents=True, exist_ok=True)
        _write_parquet(p, {"timestamp": [1], "market": ["BTC-PERP"], "close": [1.0]})
        digest = bulk.sha256_file(p)
        p.with_suffix(".parquet.sha256").write_text(digest + "\n")
        info = bulk.verify_object("candles_1h", "2025-06")
        self.assertEqual(info["status"], "OK")
        self.assertEqual(info["sha256"], digest)

    @unittest.skipIf(pa is None, "pyarrow unavailable")
    def test_hash_mismatch_detected(self):
        p = bulk.local_path("candles_1h", "2025-06")
        p.parent.mkdir(parents=True, exist_ok=True)
        _write_parquet(p, {"timestamp": [1], "market": ["BTC-PERP"], "close": [1.0]})
        p.with_suffix(".parquet.sha256").write_text("0" * 64 + "\n")
        info = bulk.verify_object("candles_1h", "2025-06")
        self.assertEqual(info["status"], "HASH_MISMATCH")
        self.assertTrue(info["problems"])

    @unittest.skipIf(pa is None, "pyarrow unavailable")
    def test_missing_sidecar_flagged(self):
        p = bulk.local_path("candles_1h", "2025-06")
        p.parent.mkdir(parents=True, exist_ok=True)
        _write_parquet(p, {"timestamp": [1], "market": ["BTC-PERP"], "close": [1.0]})
        info = bulk.verify_object("candles_1h", "2025-06")
        self.assertEqual(info["status"], "NO_SIDECAR")

    def test_absent_object(self):
        self.assertEqual(bulk.verify_object("candles_1h", "2025-06", require_exists=False)["status"], "ABSENT")
        with self.assertRaises(bulk.BulkError):
            bulk.verify_object("candles_1h", "2025-06")


class TestFetchIsCacheFirst(TempCacheMixin):
    @unittest.skipIf(pa is None, "pyarrow unavailable")
    def test_fetch_hits_verified_cache_without_network(self):
        p = bulk.local_path("candles_1h", "2025-06")
        p.parent.mkdir(parents=True, exist_ok=True)
        _write_parquet(p, {"timestamp": [1], "market": ["BTC-PERP"], "close": [1.0]})
        p.with_suffix(".parquet.sha256").write_text(bulk.sha256_file(p) + "\n")

        def _boom(_url: str, **_kw):
            raise AssertionError("network used despite verified cache")

        orig = bulk._download
        bulk._download = _boom
        try:
            info = bulk.fetch_object("candles_1h", "2025-06")
        finally:
            bulk._download = orig
        self.assertEqual(info["action"], "cache_hit")
        self.assertEqual(info["status"], "OK")


class TestManifestDeterminism(TempCacheMixin):
    @unittest.skipIf(pa is None, "pyarrow unavailable")
    def test_manifest_sorted_and_totals_consistent(self):
        p = bulk.local_path("candles_1h", "2025-06")
        p.parent.mkdir(parents=True, exist_ok=True)
        _write_parquet(p, {"timestamp": [1], "market": ["BTC-PERP"], "close": [1.0]})
        p.with_suffix(".parquet.sha256").write_text(bulk.sha256_file(p) + "\n")

        a = bulk.build_manifest(["2025-06"])
        b = bulk.build_manifest(["2025-06"])
        a.pop("generated_utc")
        b.pop("generated_utc")
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))
        self.assertEqual(a["totals"]["objects"], len(bulk.DATASETS))
        self.assertEqual(a["totals"]["ok"], 1)
        self.assertEqual(a["totals"]["absent"], len(bulk.DATASETS) - 1)
        self.assertEqual(a["months"], ["2025-06"])
        datasets = [o["dataset"] for o in a["objects"]]
        self.assertEqual(datasets, sorted(datasets))


if __name__ == "__main__":
    unittest.main()