#!/usr/bin/env python3
"""Tests for scripts/diagnostics_scanner.py (workflow diagnostics scanner invariants).

The GitHub Actions workflow (`.github/workflows/main.yml`) embeds the full
diagnostics collector inline. This module extracts the pure, deterministic
invariants that must hold of the persisted ledger
(``research_state/workflow_run_diagnostics.jsonl``) so they can be unit-tested
outside the workflow. These tests run offline and touch no network.

No network access, no credentials, no trading.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from diagnostics_scanner import (  # noqa: E402
    MAX_ERROR_LINES_PER_RUN,
    REQUIRED_FIELDS,
    SCHEMA_VERSION,
    ledger_has_no_secrets,
    normalize_records,
    redact,
    run_key,
    serialize_records,
    validate_record,
)
from nonfinite_serialization import is_strict_json  # noqa: E402


def _base_record(**overrides):
    rec = {
        "schema_version": SCHEMA_VERSION,
        "run_id": 1,
        "run_attempt": 1,
        "status": "completed",
        "conclusion": "success",
        "capture_status": "complete",
        "potential_errors": [],
    }
    rec.update(overrides)
    return rec


def test_schema_constants_match_ledger():
    tracked = Path(__file__).resolve().parents[1] / "research_state" / "workflow_run_diagnostics.jsonl"
    for line in tracked.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        assert rec["schema_version"] == SCHEMA_VERSION
        for field in REQUIRED_FIELDS:
            assert field in rec, field


def test_validate_record_accepts_well_formed():
    validate_record(_base_record())  # must not raise


def test_validate_record_rejects_wrong_schema():
    bad = _base_record(schema_version=SCHEMA_VERSION + 1)
    try:
        validate_record(bad)
    except ValueError:
        return
    raise AssertionError("expected ValueError for wrong schema_version")


def test_validate_record_rejects_missing_field():
    bad = _base_record()
    del bad["run_id"]
    try:
        validate_record(bad)
    except ValueError:
        return
    raise AssertionError("expected ValueError for missing run_id")


def test_validate_record_rejects_too_many_errors():
    bad = _base_record(
        potential_errors=[{"type": f"t{i}"} for i in range(MAX_ERROR_LINES_PER_RUN + 1)]
    )
    try:
        validate_record(bad)
    except ValueError:
        return
    raise AssertionError("expected ValueError for oversized potential_errors")


def test_run_key_is_none_without_run_id():
    assert run_key({"run_attempt": 1}) is None


def test_run_key_deduplicates_by_run_and_attempt():
    a = _base_record(run_id=10, run_attempt=2)
    b = _base_record(run_id=10, run_attempt=2, conclusion="failure")
    assert run_key(a) == run_key(b) == (10, 2)


def test_normalize_records_dedup_and_order():
    a = _base_record(run_id=1, run_attempt=1, run_completed_at="2026-01-01T00:00:00Z")
    b = _base_record(run_id=1, run_attempt=1, run_completed_at="2026-01-01T00:00:00Z", conclusion="success")
    c = _base_record(run_id=2, run_attempt=1, run_completed_at="2026-01-02T00:00:00Z")
    out = normalize_records([a, b, c])
    assert len(out) == 2
    assert out[0]["run_id"] == 1
    assert out[1]["run_id"] == 2


def test_serialize_records_is_strict_json():
    a = _base_record(run_id=1, run_attempt=1, run_completed_at="2026-01-01T00:00:00Z")
    text = serialize_records([a])
    # serialize_records renders newline-delimited JSON (JSONL), one record per line.
    lines = [ln for ln in text.splitlines() if ln.strip()]
    assert len(lines) == 1
    parsed = json.loads(lines[0])
    assert parsed["run_id"] == 1
    assert is_strict_json(lines[0])


def test_redact_strips_bearer_and_tokens():
    sample = "auth Bearer abc.def.ghi failed; token=secret123; api_key=hunter2"
    out = redact(sample)
    assert "Bearer" not in out or "REDACTED" in out
    assert "secret123" not in out
    assert "hunter2" not in out


def test_ledger_has_no_secrets_on_tracked_file():
    tracked = Path(__file__).resolve().parents[1] / "research_state" / "workflow_run_diagnostics.jsonl"
    text = tracked.read_text(encoding="utf-8")
    assert ledger_has_no_secrets(text)


def test_tracked_ledger_is_not_modified_by_tests():
    """The tracked ledger must be byte-identical before and after the test suite."""
    tracked = Path(__file__).resolve().parents[1] / "research_state" / "workflow_run_diagnostics.jsonl"
    before = tracked.read_bytes()
    normalize_records([json.loads(line) for line in before.decode("utf-8").splitlines() if line.strip()])
    after = tracked.read_bytes()
    assert before == after