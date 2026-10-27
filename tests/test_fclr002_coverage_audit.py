#!/usr/bin/env python3
"""Tests for scripts/fclr002_coverage_audit.py."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_audit_runs_and_reports_5_instruments():
    p = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "fclr002_coverage_audit.py")],
        capture_output=True, text=True, timeout=300,
    )
    assert p.returncode == 0, p.stderr
    doc = json.loads((REPO / "research_state" / "fclr002_coverage_audit.json").read_text())
    assert doc["universe"] == ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
    assert len(doc["per_symbol"]) == 5
    for row in doc["per_symbol"]:
        assert row["mark_rows"] > 0, row
    assert doc["common_timestamps"] > 0
    assert doc["common_first"] is not None and doc["common_last"] is not None
    assert doc["longest_window"]["hours"] >= 30 * 24


def test_longest_window_is_contiguous_and_within_jul_sep():
    doc = json.loads((REPO / "research_state" / "fclr002_coverage_audit.json").read_text())
    lw = doc["longest_window"]
    assert lw["start"] >= "2024-07-01"
    assert lw["end"] <= "2024-09-30T23:59:59Z"
    # >=3 non-overlapping 30-day blocks must fit inside the window
    assert lw["hours"] >= 3 * 30 * 24