#!/usr/bin/env python3
"""Tests for scripts/nonfinite_serialization.py.

The workflow diagnostics ledger is written with ``json.dumps``. Python's
default ``json.dumps`` emits the bare tokens ``NaN`` / ``Infinity`` /
``-Infinity`` for non-finite floats, which are NOT valid JSON and break
downstream parsers. This module sanitizes non-finite floats to a stable
sentinel string before serialization. These tests run offline.

No network access, no credentials, no trading.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from nonfinite_serialization import (  # noqa: E402
    NONFINITE_SENTINEL,
    dumps,
    is_strict_json,
    loads,
    sanitize,
    sanitize_float,
)


def test_sanitize_float_passthrough():
    assert sanitize_float(1.5) == 1.5
    assert sanitize_float(-3.0) == -3.0


def test_sanitize_float_nonfinite_maps_to_sentinel():
    assert sanitize_float(float("nan")) == NONFINITE_SENTINEL
    assert sanitize_float(float("inf")) == NONFINITE_SENTINEL
    assert sanitize_float(float("-inf")) == NONFINITE_SENTINEL


def test_sanitize_recurses_into_containers():
    obj = {"a": float("nan"), "b": [1.0, float("inf")], "c": (float("-inf"), 2.0)}
    out = sanitize(obj)
    assert out["a"] == NONFINITE_SENTINEL
    assert out["b"][1] == NONFINITE_SENTINEL
    assert out["c"][0] == NONFINITE_SENTINEL


def test_dumps_is_strict_json_without_nan_tokens():
    rec = {"q": float("nan"), "p": float("inf"), "n": float("-inf"), "ok": 1.0}
    text = dumps(rec)
    # Non-finite floats must be serialized to the quoted sentinel string, which
    # is ordinary JSON; the bare NaN/Infinity/-Infinity float tokens must be
    # absent so the output is strict JSON.
    assert is_strict_json(text)
    parsed = loads(text)
    assert parsed["q"] == NONFINITE_SENTINEL
    assert parsed["p"] == NONFINITE_SENTINEL
    assert parsed["n"] == NONFINITE_SENTINEL
    assert parsed["ok"] == 1.0


def test_is_strict_json_rejects_nan_tokens():
    assert is_strict_json('{"a": 1}') is True
    assert is_strict_json('{"a": NaN}') is False
    assert is_strict_json('{"a": Infinity}') is False
    assert is_strict_json('not json') is False


def test_dumps_round_trip_is_strict_json():
    rec = {"x": float("nan"), "y": [float("inf"), 2]}
    text = dumps(rec)
    assert is_strict_json(text)
    assert loads(text)["y"][0] == NONFINITE_SENTINEL


def test_dumps_matches_json_dumps_shape_for_finite():
    rec = {"a": 1, "b": 2.5, "c": [1, 2]}
    assert dumps(rec) == json.dumps(rec, sort_keys=True, separators=(",", ":"), ensure_ascii=False)