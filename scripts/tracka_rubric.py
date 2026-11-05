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
    """
    failures: List[str] = []
    venue = (candidate.get("venue") or "").strip().lower()
    if venue != "hyperliquid":
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
    sym_n = int(candidate.get("symbol_count") or len(candidate.get("symbols") or []) or 0)
    if sym_n < RUBRIC["min_symbols"]:
        failures.append("incomplete_symbol_coverage")
    if not candidate.get("completeness_documented", False):
        failures.append("completeness_not_documented")
    if not candidate.get("license_ok", False):
        failures.append("license_not_ok")
    if not _has_required_schema(candidate.get("schema_fields") or []):
        failures.append("schema_mismatch")

    go = len(failures) == 0
    return {
        "go": go,
        "verdict": "GO" if go else "NO-GO",
        "failures": failures,
        "rubric": {k: v for k, v in RUBRIC.items() if k != "required_schema_fields_any"},
        "venue": venue,
        "symbol_count": sym_n,
    }


if __name__ == "__main__":
    import json, sys
    sample = json.loads(sys.stdin.read() or "{}")
    print(json.dumps(assess_candidate(sample), indent=2))
