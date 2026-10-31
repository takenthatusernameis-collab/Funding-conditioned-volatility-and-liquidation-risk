#!/usr/bin/env python3
"""Tests for scripts/fclr006_block_audit.py (rigorous block counting)."""
import datetime as dt
import json
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import fclr006_block_audit as audit  # noqa: E402


class TestBlockCounting(unittest.TestCase):
    def setUp(self):
        self.parse = audit.parse

    def test_parse(self):
        d = self.parse("2026-05-23T00:00:00Z")
        self.assertEqual(d.year, 2026)
        self.assertEqual(d.month, 5)
        self.assertEqual(d.tzinfo, dt.timezone.utc)

    def test_full_30_day_blocks_strict(self):
        # Exactly 60 days -> 2 strict blocks, 2 loose
        s = self.parse("2026-01-01T00:00:00Z")
        e = self.parse("2026-03-02T00:00:00Z")
        strict_total, strict_full, _ = audit.count_blocks(s, e, require_full=True)
        loose_total, loose_full, _ = audit.count_blocks(s, e, require_full=False)
        self.assertEqual(strict_total, 2)
        self.assertEqual(loose_total, 2)

    def test_partial_trailing_block_strict_drops(self):
        # 75 days -> 2 full + 15-day remainder; strict drops remainder
        s = self.parse("2026-05-23T00:00:00Z")
        e = self.parse("2026-08-06T23:00:00Z")
        strict_total, strict_full, _ = audit.count_blocks(s, e, require_full=True)
        loose_total, loose_full, _ = audit.count_blocks(s, e, require_full=False)
        self.assertEqual(strict_total, 2)
        self.assertEqual(loose_total, 3)
        self.assertLess(strict_total, loose_total)

    def test_fclr003_gate_passes_both_definitions(self):
        s = self.parse("2024-10-02T00:00:00Z")
        e = self.parse("2024-12-31T23:00:00Z")
        strict_total, _, _ = audit.count_blocks(s, e, require_full=True)
        loose_total, _, _ = audit.count_blocks(s, e, require_full=False)
        self.assertGreaterEqual(strict_total, 3)
        self.assertGreaterEqual(loose_total, 3)

    def test_fclr007_underpowered_both_definitions(self):
        s = self.parse("2026-07-21T00:00:00Z")
        e = self.parse("2026-07-31T23:00:00Z")
        strict_total, _, _ = audit.count_blocks(s, e, require_full=True)
        loose_total, _, _ = audit.count_blocks(s, e, require_full=False)
        self.assertLess(strict_total, 3)
        self.assertLess(loose_total, 3)

    def test_report_written(self):
        p = Path(__file__).resolve().parent.parent / "research_state" / "fclr006_block_audit.json"
        self.assertTrue(p.exists())
        data = json.loads(p.read_text())
        self.assertIn("windows", data)
        self.assertEqual(set(data["windows"]), {"FCLR-003", "FCLR-006", "FCLR-007"})
        self.assertIn("definitions", data)


if __name__ == "__main__":
    unittest.main()