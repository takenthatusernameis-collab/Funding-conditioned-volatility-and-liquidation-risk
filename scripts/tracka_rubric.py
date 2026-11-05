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
    "license_provenance_required_when_claimed": True,
    "timestamp_unit_explicit_required": True,
    "observed_access_provenance_required": True,
    "label_definition_required_when_observed": True,
    "coverage_evidence_required_for_block_claims": True,
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
        "modeled_proxy_estimate_columns",
    ],
    "forbidden_schema_columns": [
        "modeled", "proxy", "liquidation_estimate", "estimated_liquidation",
        "synthetic_liquidation", "simulated_liquidation", "model_liquidation",
        "is_modeled", "is_proxy", "is_estimate",
    ],
}

REQUIRED_FCLR010_SCHEMA = {"timestamp", "symbol", "liquidation_notional"}
FORBIDDEN_SCHEMA_COLUMNS = {
    "modeled", "proxy", "liquidation_estimate", "estimated_liquidation",
    "synthetic_liquidation", "simulated_liquidation", "model_liquidation",
    "is_modeled", "is_proxy", "is_estimate", "liquidation_proxy", "breach_proxy",
}


def _has_required_schema(fields: List[str]) -> bool:
    s = set(fields or [])
    return REQUIRED_FCLR010_SCHEMA.issubset(s)


def _forbidden_schema_hits(fields: List[str]) -> List[str]:
    s = {str(f).strip().lower() for f in (fields or []) if f is not None}
    return sorted([c for c in FORBIDDEN_SCHEMA_COLUMNS if c in s])


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


def _is_go_shaped_observed_hl(candidate: Dict[str, Any], norm_syms: List[str]) -> bool:
    """Heuristic: candidate claims/looks like an observed Hyperliquid GO attempt.
    Used to apply strict full-manifest defaults only where meaningful (097)."""
    venue = str(candidate.get("venue") or "").strip().lower()
    unique_n = len(set(norm_syms)) if norm_syms else int(candidate.get("symbol_count") or 0)
    return (
        venue in _NORMALIZED_HYPERLIQUID
        and bool(candidate.get("unauthenticated", False))
        and not candidate.get("requires_api_key")
        and not candidate.get("requires_signature")
        and not candidate.get("requester_pays")
        and bool(candidate.get("observed_liquidations", False))
        and not candidate.get("modeled_or_proxy")
        and not candidate.get("merges_non_hyperliquid")
        and unique_n >= RUBRIC["min_symbols"]
        and _has_required_schema(candidate.get("schema_fields") or [])
    )


def assess_candidate(candidate: Dict[str, Any], *, strict_tracka_manifest: bool = False,
                     minimal_fixture_compat: bool = False) -> Dict[str, Any]:
    """Assess a candidate source dict against the Track A rubric.

    Modes (097):
      - strict_tracka_manifest=True: strict full-manifest default path. For GO-shaped
        observed Hyperliquid claims, fail-closes on missing machine-verifiable
        provenance/label/coverage/block/raw-epoch evidence by default (converts 096
        opt-in flags to defaults for that path).
      - minimal_fixture_compat=True: preserves legacy 093-096 minimal fixture behavior;
        strict defaults are not auto-applied.
      - default (both False): backward-compatible legacy behavior preserved exactly.

    Expected candidate keys (all explicit; missing = fail-closed):
      - venue, unauthenticated, requires_api_key, requires_signature, requester_pays,
        observed_liquidations, modeled_or_proxy, merges_non_hyperliquid, symbol_count,
        symbols (optional), completeness_documented, license_ok, schema_fields,
        coverage_months/coverage_complete_months/partial_month_coverage (optional),
        schema_conflicts/row_mix_observed_modeled/timestamp_normalized_utc (optional).
    Strict-manifest evidence keys (097): source_url/dataset_id/access_provenance/download_path/repo_url,
      label_definition, complete_months_list, block_count+block_evidence (when claiming blocks),
      timestamp_unit+timestamp_normalized_utc for raw epochs.
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
    # timestamp unit ambiguity: epoch ms vs s is fail-closed unless explicitly normalized+declared
    if candidate.get("schema_fields") and not candidate.get("timestamp_normalized_utc"):
        tu = candidate.get("timestamp_unit")
        if tu in ("epoch_ms", "epoch_s", "milliseconds", "seconds", "ms", "s"):
            failures.append("timestamp_unit_ambiguous")
        elif candidate.get("timestamp_unit_ambiguous"):
            failures.append("timestamp_unit_ambiguous")
    # forbidden modeled/proxy/estimate schema columns
    hits = _forbidden_schema_hits(candidate.get("schema_fields") or [])
    if hits:
        failures.append("modeled_proxy_estimate_columns")
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
    # row_count_claim conflicts / partial-row coverage claims
    rc = candidate.get("row_count_claim")
    ar = candidate.get("actual_row_count")
    if rc is not None and ar is not None:
        try:
            if int(rc) != int(ar):
                failures.append("row_count_claim_conflict")
        except Exception:
            failures.append("row_count_claim_conflict")
    if candidate.get("partial_row_coverage"):
        failures.append("row_count_claim_conflict")
    # canonical symbol map normalization proof when supplied
    sym_map = candidate.get("canonical_symbol_map")
    if isinstance(sym_map, dict) and sym_map:
        try:
            norm_map = {str(k).strip().upper(): str(v).strip().upper() for k, v in sym_map.items()}
            if not candidate.get("symbol_normalization_proof"):
                failures.append("symbol_normalization_proof_missing")
            else:
                # deterministic proof: normalized keys/values match supplied map normalization
                proof = candidate.get("symbol_normalization_proof")
                if isinstance(proof, dict) and proof.get("normalized_map") != norm_map:
                    failures.append("symbol_normalization_proof_missing")
        except Exception:
            failures.append("symbol_normalization_proof_missing")
    if unique_n < RUBRIC["min_symbols"]:
        failures.append("incomplete_symbol_coverage")
    if not candidate.get("completeness_documented", False):
        failures.append("completeness_not_documented")
    if not candidate.get("license_ok", False):
        failures.append("license_not_ok")
    else:
        # license provenance/URL or SPDX-style evidence required when license_ok claimed
        lic = candidate.get("license")
        prov = candidate.get("license_provenance") or candidate.get("license_url") or candidate.get("license_spdx")
        has_prov = False
        if isinstance(prov, str) and prov.strip():
            has_prov = True
        elif isinstance(lic, dict) and any(str(lic.get(k) or "").strip() for k in ("url", "spdx", "id", "provenance", "name")):
            has_prov = True
        elif isinstance(lic, str) and lic.strip() and ("http" in lic or lic.upper() in ("MIT", "APACHE-2.0", "CC-BY-4.0", "CC0-1.0", "BSD-3-CLAUSE", "ODC-BY-1.0")):
            has_prov = True
        if not has_prov:
            failures.append("license_provenance_missing")
    if not _has_required_schema(candidate.get("schema_fields") or []):
        failures.append("schema_mismatch")
    # 097: strict full-manifest default path for GO-shaped observed Hyperliquid claims.
    # Converts 096 opt-in flags to defaults on this path; minimal_fixture_compat preserves legacy.
    go_shaped_strict = (strict_tracka_manifest and not minimal_fixture_compat and
                        _is_go_shaped_observed_hl(candidate, _norm_symbols(candidate)))
    strict_mode = strict_tracka_manifest and not minimal_fixture_compat
    if go_shaped_strict:
        candidate = dict(candidate)
        candidate.setdefault("access_provenance_required", True)
        candidate.setdefault("label_definition_required", True)
        candidate.setdefault("strict_observed_semantics", True)
        # coverage/block evidence required when months/blocks are claimed
        if candidate.get("coverage_months") is not None:
            try:
                if int(candidate.get("coverage_months") or 0) >= 1:
                    candidate.setdefault("coverage_evidence_required", True)
            except Exception:
                candidate.setdefault("coverage_evidence_required", True)
        if candidate.get("claims_3x30d_blocks") or candidate.get("block_count") is not None:
            candidate.setdefault("claims_3x30d_blocks", True)
        if candidate.get("canonical_symbol_map") and candidate.get("symbol_proof_covers_claimed_required") is None:
            candidate.setdefault("symbol_proof_covers_claimed_required", True)

    # 096: access/provenance required for any candidate claiming observed Hyperliquid data
    # Fail-closed when source/dataset/access provenance fields are present-in-manifest but empty,
    # or when access_provenance_required=true (full admissibility manifest mode / 097 strict path).
    if candidate.get("access_provenance_required"):
        has_access = any(str(candidate.get(k) or "").strip() for k in ("source_url", "dataset_id", "access_provenance", "download_path", "repo_url"))
        if not has_access:
            failures.append("observed_access_provenance_missing")
        if not str(candidate.get("label_definition") or "").strip():
            failures.append("label_definition_missing")
    if candidate.get("label_definition_required") and not str(candidate.get("label_definition") or "").strip():
        failures.append("label_definition_missing")
    # if candidate supplies observed label claim but leaves definition ambiguous in strict mode
    if candidate.get("observed_liquidations", False) and candidate.get("strict_observed_semantics") and not str(candidate.get("label_definition") or "").strip():
        failures.append("label_definition_missing")

    # 096: coverage claims require machine-verifiable block/month evidence when explicitly asserted
    cm = candidate.get("coverage_months")
    if candidate.get("coverage_evidence_required") and cm is not None:
        try:
            if int(cm) >= 1 and not (isinstance(candidate.get("complete_months_list"), list) and len(candidate.get("complete_months_list")) >= 1):
                failures.append("coverage_month_evidence_missing")
        except Exception:
            failures.append("coverage_month_evidence_missing")
    if candidate.get("claims_3x30d_blocks"):
        try:
            bc = int(candidate.get("block_count") or 0)
            if bc < 3:
                failures.append("block_count_evidence_insufficient")
            if not isinstance(candidate.get("block_evidence"), list) or len(candidate.get("block_evidence")) < 3:
                failures.append("block_count_evidence_insufficient")
        except Exception:
            failures.append("block_count_evidence_insufficient")

    # 096: symbol-map proof must cover every claimed symbol (opt-in strict manifest mode)
    if candidate.get("symbol_proof_covers_claimed_required") and isinstance(sym_map, dict) and sym_map:
        try:
            norm_map = {str(k).strip().upper(): str(v).strip().upper() for k, v in sym_map.items()}
            proof = candidate.get("symbol_normalization_proof")
            proof_map = (proof.get("normalized_map") if isinstance(proof, dict) else {}) or {}
            if norm_syms:
                missing = [s for s in set(norm_syms) if s not in set(norm_map.values()) and s not in set(proof_map.keys()) and s not in set(proof_map.values())]
                if missing:
                    failures.append("symbol_normalization_proof_incomplete")
        except Exception:
            failures.append("symbol_normalization_proof_incomplete")

    # 096/097: raw epoch fields claimed require explicit timestamp unit/normalization evidence
    raw_epoch = candidate.get("raw_epoch_fields") or candidate.get("epoch_timestamp_fields")
    if raw_epoch and candidate.get("schema_fields") and not candidate.get("timestamp_normalized_utc"):
        failures.append("timestamp_unit_ambiguous")
    # 097 strict: if schema has timestamp but normalization is not explicitly true for GO-shaped observed HL, fail-closed
    if strict_mode and _is_go_shaped_observed_hl(candidate, _norm_symbols(candidate)) and candidate.get("schema_fields"):
        if candidate.get("timestamp_normalized_utc") is not True:
            if "timestamp_not_normalized" not in failures and "timestamp_unit_ambiguous" not in failures:
                failures.append("timestamp_not_normalized")


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
        "strict_tracka_manifest": bool(strict_tracka_manifest and not minimal_fixture_compat),
        "minimal_fixture_compat": bool(minimal_fixture_compat),
    }


if __name__ == "__main__":
    import json, sys
    sample = json.loads(sys.stdin.read() or "{}")
    print(json.dumps(assess_candidate(sample), indent=2))


def assess_strict_manifest(candidate: Dict[str, Any]) -> Dict[str, Any]:
    """097: strict full-manifest default path (no compat)."""
    return assess_candidate(candidate, strict_tracka_manifest=True, minimal_fixture_compat=False)


def assess_minimal_fixture(candidate: Dict[str, Any]) -> Dict[str, Any]:
    """097: explicit legacy/minimal fixture compat path (preserves 093-096 behavior)."""
    return assess_candidate(candidate, strict_tracka_manifest=False, minimal_fixture_compat=True)
