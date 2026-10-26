#!/usr/bin/env python3
"""Testable core invariants of the workflow diagnostics scanner/ledger writer.

The GitHub Actions workflow (`.github/workflows/main.yml`) embeds the full
diagnostics collector inline. This module extracts the pure, deterministic
invariants that must hold of the persisted ledger
(`research_state/workflow_run_diagnostics.jsonl`) so they can be unit-tested
outside the workflow:

  * redaction of authorization material and long opaque values;
  * ANSI escape stripping;
  * stable per-run deduplication on (run_id, run_attempt);
  * schema version and required-field stability;
  * deterministic ordering and compact JSON serialization;
  * bounded per-run error excerpts.

No network access, no credentials, no trading.
"""
from __future__ import annotations

import json
import re
from typing import Any, Iterable

SCHEMA_VERSION = 1
REQUIRED_FIELDS = (
    "schema_version",
    "run_id",
    "run_attempt",
    "status",
    "conclusion",
    "capture_status",
    "potential_errors",
)
MAX_ERROR_LINES_PER_RUN = 20

_BEARER_RE = re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+")
_GH_TOKEN_RE = re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})")
_JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{8,}\b")
_SECRET_ASSIGN_RE = re.compile(
    r"""(?i)\b(token|password|secret|api[_-]?key|client[_-]?secret|"""
    r"""authorization)\b(\s*[:=]\s*)(["']?)[^\s,"';]+"""
)
_URL_SECRET_RE = re.compile(r"(?i)([?&](?:token|sig|signature|x-amz-credential|x-amz-signature)=)[^&\s]+")
_LONG_VALUE_RE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z0-9_+/=-]{100,}(?![A-Za-z0-9])")
_ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences."""
    return _ANSI_RE.sub("", str(text))


def redact(text: str) -> str:
    """Redact authorization material and long opaque values from a string."""
    text = strip_ansi(text)
    text = _BEARER_RE.sub("Bearer [REDACTED]", text)
    text = _GH_TOKEN_RE.sub("[REDACTED_GITHUB_TOKEN]", text)
    text = _JWT_RE.sub("[REDACTED_JWT]", text)
    text = _SECRET_ASSIGN_RE.sub(r"\1\2[REDACTED]", text)
    text = _URL_SECRET_RE.sub(r"\1[REDACTED]", text)
    text = _LONG_VALUE_RE.sub("[REDACTED_LONG_VALUE]", text)
    return text


def run_key(record: dict) -> tuple[Any, int] | None:
    """Stable deduplication key for a diagnostic record."""
    run_id = record.get("run_id")
    if run_id is None:
        return None
    attempt = record.get("run_attempt") or 1
    return (run_id, attempt)


def validate_record(record: dict) -> None:
    """Raise ValueError if a record violates the frozen ledger schema."""
    if not isinstance(record, dict):
        raise ValueError("record must be a dict")
    if record.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(
            f"schema_version must be {SCHEMA_VERSION}, got {record.get('schema_version')!r}"
        )
    for field in REQUIRED_FIELDS:
        if field not in record:
            raise ValueError(f"record missing required field {field!r}")
    if record.get("potential_errors") is None:
        raise ValueError("potential_errors must be present")
    excerpts = record.get("potential_errors") or []
    if len(excerpts) > MAX_ERROR_LINES_PER_RUN:
        raise ValueError(
            f"potential_errors exceeds bound of {MAX_ERROR_LINES_PER_RUN} entries"
        )
    for entry in excerpts:
        if not isinstance(entry, dict):
            raise ValueError("each potential_error entry must be a dict")
        if "type" not in entry:
            raise ValueError("each potential_error entry must have a 'type'")


def normalize_records(records: Iterable[dict]) -> list[dict]:
    """Deduplicate, validate, and deterministically order ledger records."""
    by_key: dict[tuple[Any, int], dict] = {}
    for record in records:
        validate_record(record)
        key = run_key(record)
        if key is None:
            # Non-run diagnostic events are kept distinct and never merged.
            continue
        by_key[key] = record
    ordered = sorted(
        by_key.values(),
        key=lambda r: (
            r.get("run_completed_at") or r.get("created_at") or "",
            int(r.get("run_id") or 0),
            int(r.get("run_attempt") or 1),
        ),
    )
    return ordered


def serialize_records(records: Iterable[dict]) -> str:
    """Render records as deterministic, compact, JSON-safe JSONL text."""
    lines = []
    for record in normalize_records(records):
        lines.append(json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    return "\n".join(lines) + ("\n" if lines else "")


def ledger_has_no_secrets(text: str) -> bool:
    """Return True if the ledger text contains no unredacted secrets."""
    for pattern in (_BEARER_RE, _GH_TOKEN_RE, _JWT_RE, _SECRET_ASSIGN_RE, _URL_SECRET_RE, _LONG_VALUE_RE):
        if pattern.search(text):
            return False
    return True