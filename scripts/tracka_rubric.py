#!/usr/bin/env python3
"""Pure Track A (FCLR-010) source admissibility rubric - Hyperliquid-only, observed liquidations.

This module provides deterministic GO/NO-GO assessment for candidate liquidation
data sources. It enforces the maximally strict rubric and rejects common conflation
cases (modeled-as-observed, non-Hyperliquid merge, schema mismatch, auth/requester-pays,
incomplete coverage). Used for adversarial tests and source hardening; it does not
perform network access.
"""
from __future__ import annotations

from typing import Any, Dict, List

RUBRIC: Dict[str, Any] = {
    "track": "A",
    "experiment": "FCLR-010",
    "hyperliquid_only": True,
    "observed_liquidations_only": True,
    "unauthenticated_only": True,
    "no_requester_pays": True,
    "no_api_key_or_signature": True,
    "min_symbols": 5,
    "completeness_doc_required": True,
    "license_ok_required": True,
    "schema_compatible_fclr010": True,
    "required_schema_fields_any": [
        ["timestamp", "symbol", "liquidation_notional"],
        ["timestamp", "symbol", "mark_price", "funding_rate", "liquidation_notional"],
    ],
    "forbidden_conflations": [
        "modeled_as_observed",
        "non_hyperliquid_merge",
        "proxy_without_observed_label",
        "synthetic_liquidations",
    ],
}

REQUIRED_FCLR010_SCHEMA = {"timestamp", "symbol", "liquidation_notional"}


def _has_required_schema(fields: List[str]) -> bool:
    s = set(fields or [])
    return REQUIRED_FCLR010_SCHEMA.issubset(s)


_NORMALIZED_HYPERLIQUID = {"hyperliquid", "hl", "hyperliquid_perp", "hyperliquid-perp"}


def _norm_symbols(candidate: Dict[str, Any]) -> List[str]:
    raw = candidate.get("symbols") or []
    if not isinstance(raw, list):
        return []
    out = []
    for s in raw:
        if s is None:
            continue
        n = str(s).strip().upper()
        if n:
            out.append(n)
    return out


def assess_candidate(candidate: Dict[str, Any]) -> Dict[str, Any]:
    """Assess a candidate source dict against the strict Track A rubric.

    Expected candidate keys (all explicit; missing = fail-closed):
      - venue: str
      - unauthenticated: bool
      - requires_api_key: bool
      - requires_signature: bool
      - requester_pays: bool
      - observed_liquidations: bool
      - modeled_or_proxy: bool
      - merges_non_hyperliquid: bool
      - symbol_count: int
      - symbols: list[str] (optional)
      - completeness_documented: bool
      - license_ok: bool
      - schema_fields: list[str]
      - coverage_months: int (optional, informational)
      - partial_month_coverage: bool (optional, fail if true)
      - schema_conflicts: bool/list (optional, fail if truthy)
      - row_mix_observed_modeled: bool (optional, fail if true)
      - timestamp_normalized_utc: bool (optional, fail if false when schema present)
      - coverage_complete_months: int (optional; if provided must be >=1 when months claimed)
    """
    failures: List[str] = []
    venue_raw = (candidate.get("venue") or "").strip()
    venue = venue_raw.lower()
    if venue not in _NORMALIZED_HYPERLIQUID or candidate.get("venue_alias_spoof"):
        failures.append("non_hyperliquid_venue")
    if candidate.get("merges_non_hyperliquid"):
        failures.append("non_hyperliquid_merge")
    if not candidate.get("unauthenticated", False):
        failures.append("not_unauthenticated")
    if candidate.get("requires_api_key"):
        failures.append("requires_api_key")
    if candidate.get("requires_signature"):
        failures.append("requires_signature")
    if candidate.get("requester_pays"):
        failures.append("requester_pays")
    if not candidate.get("observed_liquidations", False):
        failures.append("not_observed_liquidations")
    if candidate.get("modeled_or_proxy"):
        failures.append("modeled_or_proxy")
    if candidate.get("row_mix_observed_modeled"):
        failures.append("mixed_observed_modeled_rows")
    if candidate.get("partial_month_coverage"):
        failures.append("partial_month_coverage")
    ccm = candidate.get("coverage_complete_months")
    if ccm is not None:
        try:
            if int(ccm) < 1 and (candidate.get("coverage_months") or 0):
                failures.append("partial_month_coverage")
        except Exception:
            failures.append("partial_month_coverage")
    sc = candidate.get("schema_conflicts")
    if sc:
        failures.append("schema_conflicts")
    # timestamp normalization: fail-closed when schema claims present but not normalized
    if candidate.get("schema_fields") and candidate.get("timestamp_normalized_utc") is False:
        failures.append("timestamp_not_normalized")
    norm_syms = _norm_symbols(candidate)
    sym_n = int(candidate.get("symbol_count") or len(norm_syms) or 0)
    if norm_syms and len(set(norm_syms)) != len(norm_syms):
        failures.append("duplicate_symbols")
    unique_n = len(set(norm_syms)) if norm_syms else sym_n
    if norm_syms and candidate.get("symbol_count") is not None:
        # conflicting count claim
        try:
            claim = int(candidate.get("symbol_count"))
        except Exception:
            claim = -1
        if claim != unique_n:
            failures.append("incomplete_symbol_coverage")
    if unique_n < RUBRIC["min_symbols"]:
        failures.append("incomplete_symbol_coverage")
    if not candidate.get("completeness_documented", False):
        failures.append("completeness_not_documented")
    if not candidate.get("license_ok", False):
        failures.append("license_not_ok")
    if not _has_required_schema(candidate.get("schema_fields") or []):
        failures.append("schema_mismatch")

    failures = sorted(set(failures))
    go = len(failures) == 0
    return {
        "go": go,
        "verdict": "GO" if go else "NO-GO",
        "failures": failures,
        "rubric": {k: v for k, v in RUBRIC.items() if k != "required_schema_fields_any"},
        "venue": venue,
        "venue_raw": venue_raw,
        "symbol_count": len(set(norm_syms)) if norm_syms else sym_n,
    }


if __name__ == "__main__":
    import json, sys
    sample = json.loads(sys.stdin.read() or "{}")
    print(json.dumps(assess_candidate(sample), indent=2))
