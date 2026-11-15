#!/usr/bin/env python3
"""Deterministic tests for the FCLR-LIQ-COMBINED-PANEL §16 admissibility audit.

Uses tiny synthetic fixtures (no real 3M-row cache, no network) to exercise
schema mapping, seam abutment, block classification and the admissibility
determination logic.
"""
from __future__ import annotations

import importlib
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _mod():
    return importlib.import_module("scripts.fclr_liq_combined_admissibility_audit")


def _write_fixtures(cache: Path) -> None:
    (cache / "metpie_liq").mkdir(parents=True, exist_ok=True)
    (cache / "ironflow_events").mkdir(parents=True, exist_ok=True)
    (cache / "hyperliquid_funding").mkdir(parents=True, exist_ok=True)
    (cache / "hyperliquid_candles").mkdir(parents=True, exist_ok=True)

    start = datetime(2025, 3, 22, tzinfo=timezone.utc)
    # 65 days of metpie: 2 pristine 30-day blocks + a few days
    rows = []
    t = start
    coins = ["BTC", "ETH", "SOL", "XRP", "DOGE", "ADA"]
    i = 0
    while t < start + timedelta(days=65):
        for c in coins:
            rows.append({
                "time": int(t.timestamp() * 1000),
                "coin": c,
                "px": 1.0,
                "sz": 1.0,
                "side": "B",
                "liquidated_start_pos": -1.0,
                "hash": f"0x{i}",
                "notional_usd": 100.0 + i,
            })
            i += 1
        t += timedelta(hours=6)
    pd.DataFrame(rows).to_csv(cache / "metpie_liq" / "liquidation_events.csv.gz")

    # ironflow: 2025-05-25 .. 2025-10-31 (abuts metpie), 6 coins
    irows = []
    it = datetime(2025, 5, 25, 14, 36, tzinfo=timezone.utc)
    end = datetime(2025, 10, 31, tzinfo=timezone.utc)
    j = 0
    while it < end:
        for c in coins:
            irows.append({
                "timestamp": it,
                "market": f"{c}-PERP",
                "issuer": "0x0",
                "wallet": "0x0",
                "position_side": "long",
                "size": 1.0,
                "notional_usd": 50.0 + j,
                "avg_price": 1.0,
                "fills": 1,
                "block": None,
                "tx_hash": f"0x{j}",
            })
            j += 1
        it += timedelta(hours=6)
    # split into two parquet files like the real layout
    half = len(irows) // 2
    pd.DataFrame(irows[:half]).to_parquet(cache / "ironflow_events" / "2025-05.parquet")
    pd.DataFrame(irows[half:]).to_parquet(cache / "ironflow_events" / "2025-10.parquet")

    # funding cache covering only 2025-11+ (does NOT reach the combined start)
    for c in coins:
        pd.DataFrame([{"coin": c, "fundingRate": "0.0001", "premium": "0.0", "time": 1793401200078}]).to_json(
            cache / "hyperliquid_funding" / f"{c}.json", orient="records"
        )
        (cache / "hyperliquid_candles" / c).mkdir(parents=True, exist_ok=True)
        (cache / "hyperliquid_candles" / c / "2025-11.json").write_text("[]")


class TestLiqCombinedAudit(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cache = Path(self.tmp.name)
        _write_fixtures(self.cache)
        self.mod = _mod()
        self._saved = (
            self.mod.METPIE,
            self.mod.IRONFLOW_DIR,
            self.mod.HYPERLIQUID_FUNDING_DIR,
            self.mod.HYPERLIQUID_CANDLES_DIR,
        )
        self.mod.METPIE = self.cache / "metpie_liq" / "liquidation_events.csv.gz"
        self.mod.IRONFLOW_DIR = self.cache / "ironflow_events"
        self.mod.HYPERLIQUID_FUNDING_DIR = self.cache / "hyperliquid_funding"
        self.mod.HYPERLIQUID_CANDLES_DIR = self.cache / "hyperliquid_candles"
        self._saved_min = self.mod.MIN_EVENTS_PER_INSTRUMENT
        self.mod.MIN_EVENTS_PER_INSTRUMENT = 10

    def tearDown(self):
        (
            self.mod.METPIE,
            self.mod.IRONFLOW_DIR,
            self.mod.HYPERLIQUID_FUNDING_DIR,
            self.mod.HYPERLIQUID_CANDLES_DIR,
        ) = self._saved
        self.mod.MIN_EVENTS_PER_INSTRUMENT = self._saved_min
        self.tmp.cleanup()

    def test_schema_mapping_and_seam(self):
        a = self.mod.build_audit("20260101T000000Z")
        self.assertEqual(a["schema_mapping"]["coin"], "metpie.coin ; ironflow.market with '-PERP' suffix stripped")
        # ironflow markets had -PERP stripped -> coins present
        self.assertIn("BTC", a["combined"]["funded_coins"])
        # seam: metpie ends 2025-05-25 ~ before ironflow starts same day
        self.assertLess(abs(a["seam"]["gap_hours"]), 24.0)
        self.assertGreater(a["combined"]["span_days"], 150.0)

    def test_block_classification_nonoverlap_and_deterministic(self):
        a = self.mod.build_audit("20260101T000000Z")
        blocks = a["block_classification"]
        self.assertGreaterEqual(len(blocks), self.mod.MIN_BLOCKS)
        for prev, nxt in zip(blocks, blocks[1:]):
            # each block is 30 days
            s = pd.Timestamp(prev["start"])
            e = pd.Timestamp(prev["end"])
            self.assertAlmostEqual((e - s).total_seconds() / 86400.0, 30.0, places=2)
            # non-overlapping and ordered
            self.assertLess(pd.Timestamp(prev["end"]), pd.Timestamp(nxt["start"]))
        # determinism
        b = self.mod.build_audit("20260101T000000Z")
        self.assertEqual(blocks, b["block_classification"])

    def test_criteria_and_determination_pending_acquisition(self):
        a = self.mod.build_audit("20260101T000000Z")
        self.assertEqual(a["criteria"]["ge_5_instruments_with_label_coverage"]["status"], "PASS")
        self.assertEqual(a["criteria"]["ge_3_nonoverlapping_30d_blocks"]["status"], "PASS")
        # funding cache starts 2025-11 -> does not reach 2025-03-22 start
        self.assertEqual(a["criteria"]["aligned_market_context_available"]["status"], "PARTIAL")
        self.assertEqual(a["determination"], "ADMISSIBLE_PENDING_BOUNDED_ACQUISITION")

    def test_render_md_contains_determination(self):
        a = self.mod.build_audit("20260101T000000Z")
        md = self.mod._render_md(a)
        self.assertIn(a["determination"], md)
        self.assertIn("## §16 criteria", md)


if __name__ == "__main__":
    unittest.main()