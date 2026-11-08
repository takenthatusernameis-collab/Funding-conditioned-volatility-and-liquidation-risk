"""FCLR-NEXT-162: deterministic tests for read-only inventory reconciliation."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import reconcile_inventory


class TestReconcileInventory(unittest.TestCase):
    def test_reconcile_missing_in_inventory_detected(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "data_cache"
            inv = td / "data_inventory.json"
            cdir = cache / "BTCUSDT_2024_04"
            cdir.mkdir(parents=True)
            (cdir / "sample.csv").write_text("x,y\n1,2\n")
            inv.write_text(json.dumps([]))
            res = reconcile_inventory.reconcile(str(cache), str(inv))
            self.assertFalse(res["reconciled"])
            self.assertEqual(len(res["missing_in_inventory"]), 1)
            self.assertEqual(res["missing_in_inventory"][0]["symbol"], "BTCUSDT")
            self.assertEqual(res["missing_in_inventory"][0]["month_label"], "BTCUSDT_2024_04")
            self.assertTrue(res["missing_in_inventory"][0]["cache_sha256_sample"][0])

    def test_reconcile_read_only_no_inventory_write(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "data_cache"
            inv = td / "data_inventory.json"
            cdir = cache / "BNBUSDT_2024_06"
            cdir.mkdir(parents=True)
            (cdir / "f.bin").write_bytes(b"abc")
            inv.write_text(json.dumps([]))
            before = inv.read_text()
            res = reconcile_inventory.reconcile(str(cache), str(inv))
            self.assertEqual(inv.read_text(), before)
            self.assertFalse(res["reconciled"])

    def test_reconcile_reports_counts_deterministic(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "data_cache"
            inv = td / "data_inventory.json"
            inv.write_text(json.dumps([]))
            res = reconcile_inventory.reconcile(str(cache), str(inv))
            self.assertTrue(res["reconciled"])
            self.assertIn("cache_month_dirs", res)
            self.assertIn("missing_in_inventory", res)
            self.assertIn("stale_in_inventory", res)


if __name__ == "__main__":
    unittest.main()
