#!/usr/bin/env python3
"""Tests for scripts/fclr002_coverage_audit.py."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _run_audit() -> dict:
    """Run the audit into a throwaway temp file so the tracked artifact is never rewritten."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "audit.json"
        p = subprocess.run(
            [
                sys.executable,
                str(REPO / "scripts" / "fclr002_coverage_audit.py"),
                "--out",
                str(out),
            ],
            capture_output=True, text=True, timeout=300,
        )
        assert p.returncode == 0, p.stderr
        return json.loads(out.read_text())


def test_audit_runs_and_reports_5_instruments():
    doc = _run_audit()
    assert doc["universe"] == ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
    assert len(doc["per_symbol"]) == 5
    for row in doc["per_symbol"]:
        assert row["mark_rows"] > 0, row
    assert doc["common_timestamps"] > 0
    assert doc["common_first"] is not None and doc["common_last"] is not None
    assert doc["longest_window"]["hours"] >= 30 * 24


def test_longest_window_is_contiguous_and_meets_minimum_blocks():
    doc = _run_audit()
    lw = doc["longest_window"]
    # The audited 5-instrument common window is 2024-04-01..2024-09-30
    # (mark-price coverage for the other four symbols begins 2024-04-01).
    assert lw["start"] == doc["common_first"]
    assert lw["end"] == doc["common_last"]
    assert lw["start"] >= "2024-04-01"
    assert lw["end"] <= "2024-09-30T23:59:59Z"
    # >=3 non-overlapping 30-day blocks must fit inside the window
    assert lw["hours"] >= 3 * 30 * 24


def test_tracked_artifact_is_not_modified_by_test_runs():
    """The tracked audit JSON must be byte-identical before and after the test suite."""
    tracked = REPO / "research_state" / "fclr002_coverage_audit.json"
    before = tracked.read_bytes()
    _run_audit()
    after = tracked.read_bytes()
    assert before == after, "test suite rewrote the tracked coverage audit artifact"