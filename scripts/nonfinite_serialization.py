#!/usr/bin/env python3
"""JSON-safe serialization of result records that may contain non-finite floats.

The workflow's diagnostics ledger is written with
``json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)``.
Python's default ``json.dumps`` emits the bare tokens ``NaN`` / ``Infinity`` /
``-Infinity`` for non-finite floats, which are NOT valid JSON and break
downstream parsers (and any future strict JSON loader). This module sanitizes
non-finite floats to a stable sentinel string before serialization so ledger
records remain strictly JSON-loadable while preserving the distinction between
a genuine missing value and a computed non-finite result.

No network access, no credentials, no trading.
"""
from __future__ import annotations

import json
import math
from typing import Any

NONFINITE_SENTINEL = "NaN"


def sanitize_float(value: float) -> str | float:
    """Map a float to itself, or to the NONFINITE_SENTINEL when not finite."""
    if isinstance(value, float) and not math.isfinite(value):
        return NONFINITE_SENTINEL
    return value


def sanitize(obj: Any) -> Any:
    """Recursively sanitize non-finite floats inside nested containers."""
    if isinstance(obj, float):
        return sanitize_float(obj)
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize(v) for v in obj]
    if isinstance(obj, tuple):
        return [sanitize(v) for v in obj]
    return obj


def dumps(record: dict, *, sort_keys: bool = True, separators: tuple[str, str] = (",", ":")) -> str:
    """Serialize a record to strict JSON, sanitizing non-finite floats first."""
    cleaned = sanitize(record)
    return json.dumps(cleaned, sort_keys=sort_keys, separators=separators, ensure_ascii=False)


def loads(text: str) -> dict:
    """Load a sanitized ledger line back into a dict."""
    return json.loads(text)


def is_strict_json(text: str) -> bool:
    """Return True iff text parses as strict JSON with no NaN/Infinity tokens.

    ``json.loads`` accepts the bare tokens ``NaN`` / ``Infinity`` /
    ``-Infinity`` by default, so we install a ``parse_constant`` hook that
    rejects them. Quoted string values such as the NONFINITE_SENTINEL
    ``"NaN"`` are ordinary JSON strings and remain valid.
    """
    try:
        json.loads(text, parse_constant=_reject_nonfinite)
    except (ValueError, TypeError):
        return False
    return True


def _reject_nonfinite(token: str):
    raise ValueError(f"non-finite JSON constant not allowed: {token!r}")