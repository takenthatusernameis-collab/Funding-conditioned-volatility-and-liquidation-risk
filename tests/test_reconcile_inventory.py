"""FCLR-NEXT-162/165: deterministic tests for read-only inventory reconciliation."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import reconcile_inventory


def _make_cache(cache: Path, sym_month: str, content: str = "x,y\n1,2\n"):
    cdir = cache / sym_month
    cdir.mkdir(parents=True, exist_ok=True)
    (cdir / "sample.csv").write_text(content)


class TestReconcileInventory(unittest.TestCase):
    def test_reconcile_missing_in_inventory_detected(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "data_cache"
            inv = td / "data_inventory.json"
            _make_cache(cache, "BTCUSDT_2024_04")
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

    def test_gate_input_summary_present_and_read_only_contract(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "data_cache"
            inv = td / "data_inventory.json"
            _make_cache(cache, "BTCUSDT_2024_04")
            inv.write_text(json.dumps([]))
            res = reconcile_inventory.reconcile(str(cache), str(inv))
            self.assertIn("gate_input_summary", res)
            g = res["gate_input_summary"]
            self.assertEqual(g["totals"]["missing_in_inventory_months"], 1)
            self.assertTrue(g["gaps_present"])
            self.assertIn("BTCUSDT", g["by_symbol"])
            self.assertEqual(g["by_symbol"]["BTCUSDT"]["cache_months"], 1)
            self.assertIn("read-only", g["scope_note"])
            self.assertIn("not confirmatory GO", g["scope_note"])
            self.assertFalse(res["reconciled"])

    def test_gate_input_summary_cli_flag_emits_minimal_payload(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "data_cache"
            inv = td / "data_inventory.json"
            _make_cache(cache, "ETHUSDT_2024_05")
            inv.write_text(json.dumps([]))
            out = subprocess.run(
                [sys.executable, str(REPO / "scripts" / "reconcile_inventory.py"),
                 "--cache-dir", str(cache), "--inventory", str(inv),
                 "--gate-input-summary", "--json"],
                capture_output=True, text=True, check=True,
            )
            payload = json.loads(out.stdout)
            self.assertIn("by_symbol", payload)
            self.assertIn("totals", payload)
            self.assertIn("scope_note", payload)
            self.assertEqual(payload["totals"]["missing_in_inventory_months"], 1)
            self.assertEqual(payload["by_symbol"]["ETHUSDT"]["cache_months"], 1)
            # scope_note must never claim confirmatory GO or provenance/license/terms resolution
            self.assertIn("not confirmatory GO", payload["scope_note"])

    def test_gate_input_summary_cli_is_read_only_no_inventory_write(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            cache = td / "data_cache"
            inv = td / "data_inventory.json"
            _make_cache(cache, "SOLUSDT_2024_06")
            inv.write_text(json.dumps([]))
            before = inv.read_text()
            subprocess.run(
                [sys.executable, str(REPO / "scripts" / "reconcile_inventory.py"),
                 "--cache-dir", str(cache), "--inventory", str(inv),
                 "--gate-input-summary"],
                capture_output=True, text=True, check=True,
            )
            self.assertEqual(inv.read_text(), before)


if __name__ == "__main__":
    unittest.main()