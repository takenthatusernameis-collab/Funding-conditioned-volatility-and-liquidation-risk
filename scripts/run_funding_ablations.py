#!/usr/bin/env python3
"""Run funding-conditioned volatility ablations (Gate 4), multi-split pilot.

Leakage-resistant, pre-registered (research_state/pre_registration_gate4_funding_multisplit_20261107.md):
- Chronological walk-forward splits, purge/embargo >= 7d
- Train-only normalization per split
- Funding last-known at/before hour (no lookahead); trailing stats past-only
- Direct-variance OLS HAR (Gate 3 form); A_rv_only regression-stable
- Block bootstrap ΔQLIKE CIs, resampling whole UTC time blocks jointly across instruments
- Honest verdict PILOT/INCONCLUSIVE when data-sufficiency criteria unmet
"""

from __future__ import annotations

import json
import hashlib
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone, timedelta
import os

import numpy as np
import pandas as pd

from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

# numpy/pandas are imported at module top (installed via requirements.txt);
# src.* ingestion helpers stay lazy inside data-loading functions so the v5
# admissibility guard/report/preflight/promotion-dryrun paths import cleanly
# under the frozen Gate 4 protocol without pulling the full src graph at module
# import time.

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
RAW = REPO / "data" / "raw"
RES = REPO / "research_state"
ZIPS_DIR = REPO
EPS = 1e-12

CACHE = RES / "data_cache"


# --- Confirmatory provenance guard (FCLR-014/FCLR-016) ---
# 2025+ cache windows lack admissible confirmatory provenance (FCLR-014 NO-GO).
# Fail-closed: confirmatory-labeled runs touching unprovenanced 2025+ data must refuse.
PROVENANCED_CONFIRMATORY_RANGES = [
    # (start_inclusive, end_inclusive) — 2024-04..09 identity-verified vs Binance Vision (FCLR-015)
    ("2024-04-01", "2024-09-30"),
]
UNPROVENANCED_CONFIRMATORY_PREFIXES = ("2025", "2026")  # 2025+ cache; 2026-01..06/10 candidates NO-GO per FCLR-014

def _range_overlaps_unprovenanced(start: str, end: str) -> bool:
    try:
        s = str(start)[:10]; e = str(end)[:10]
    except Exception:
        return True  # fail closed
    # any 2025+ year in range
    for pref in UNPROVENANCED_CONFIRMATORY_PREFIXES:
        if s[:4] <= pref <= e[:4] or s.startswith(pref) or e.startswith(pref):
            # 2024 is partially provenanced; 2025+ is not
            if pref >= "2025":
                return True
    return False

def _is_confirmatory_intent(experiment_id: str, pre_registration: str, out_suffix: str, confirmatory_flag: bool) -> bool:
    if confirmatory_flag:
        return True
    blob = f"{experiment_id} {pre_registration} {out_suffix}".lower()
    if "exploratory" in blob or "pilot" in blob:
        return False
    # v5+ confirmatory preregs / explicit confirmatory naming
    if "confirmatory" in blob or re.search(r"\bv[5-9]\b", blob):
        return True
    return False


def _confirmatory_data_path_seam_error(symbols: List[str], start: str, end: str, include_cache: bool) -> Optional[str]:
    """Fail-closed pre-load seam for confirmatory/expect-go paths.

    Returns a stable machine-readable reason string when required local data
    sources are missing/unreadable/nonexistent for the requested range, so
    confirmatory paths refuse before any kline/funding/outcome loader is called.
    Exploratory/non-confirmatory callers must not use this guard.
    """
    problems: List[str] = []
    for root in ([RAW] + ([CACHE] if include_cache else [])):
        try:
            root_p = Path(root)
        except Exception:
            problems.append(f"invalid_data_root:{root}")
            continue
        if not root_p.exists():
            problems.append(f"missing_data_root:{root_p}")
            continue
        if not root_p.is_dir():
            problems.append(f"data_root_not_directory:{root_p}")
            continue
        try:
            if not os.access(root_p, os.R_OK):
                problems.append(f"unreadable_data_root:{root_p}")
        except Exception:
            problems.append(f"unreadable_data_root:{root_p}")
    found_k = False
    found_f = False
    for sym in symbols:
        kpats = [f"{sym}-1h-*.csv", f"{sym}-1h-*.zip", f"{sym}_*/{sym}-1h-*.csv", f"{sym}_*/{sym}-1h-*.zip",
                 f"{sym}_*/klines-*/{sym}-1h-*.csv", f"{sym}_*/klines-*/{sym}-1h-*.zip"]
        fpats = [f"{sym}-fundingRate-*.csv", f"{sym}-fundingRate-*.zip",
                 f"{sym}_*/{sym}-fundingRate-*.csv", f"{sym}_*/{sym}-fundingRate-*.zip",
                 f"{sym}_*/*/{sym}-fundingRate-*.csv", f"{sym}_*/*/{sym}-fundingRate-*.zip"]
        try:
            ksrc = [p for p in _iter_readable_sources(kpats, include_cache=include_cache)
                    if p.is_file() and sym in p.name and '1h' in p.name and 'fundingRate' not in p.name
                    and not any(x in str(p) for x in ('indexPriceKlines', 'markPriceKlines', 'premiumIndexKlines'))]
        except Exception as e:
            problems.append(f"unreadable_kline_source_probe:{sym}:{type(e).__name__}")
            ksrc = []
        try:
            fsrc = [p for p in _iter_readable_sources(fpats, include_cache=include_cache)
                    if p.is_file() and sym in p.name and 'fundingRate' in p.name]
        except Exception as e:
            problems.append(f"unreadable_funding_source_probe:{sym}:{type(e).__name__}")
            fsrc = []
        if not ksrc:
            problems.append(f"missing_kline_sources:{sym}:{start}..{end}")
        else:
            found_k = True
        if not fsrc:
            problems.append(f"missing_funding_sources:{sym}:{start}..{end}")
        else:
            found_f = True
    if not found_k and not found_f and problems:
        return "confirmatory_data_path_seam_blocked:" + "|".join(sorted(set(problems)))[:2000]
    if problems and (not found_k or not found_f):
        return "confirmatory_data_path_seam_blocked:" + "|".join(sorted(set(problems)))[:2000]
    return None

def _manifest_scope_covers(manifest: dict, start: str, end: str) -> Optional[str]:
    """Return error if manifest declares frozen_scope/window that does not cover [start,end]."""
    scope = manifest.get("frozen_scope") or {}
    window = scope.get("window")
    if isinstance(window, str) and ".." in window:
        ws, we = [x.strip()[:10] for x in window.split("..", 1)]
        if str(start)[:10] < ws or str(end)[:10] > we:
            return f"manifest frozen_scope.window {window} does not cover requested {start}..{end}"
    # month-based scope
    months = scope.get("months") or []
    if months and isinstance(months, list):
        ms, me = min(months) + "-01", max(months) + "-31"
        if str(start)[:10] < ms[:10] or str(end)[:10] > me[:10]:
            # approximate; only fail on clear mismatch
            if str(end)[:7] > max(months) or str(start)[:7] < min(months):
                return f"manifest frozen_scope.months {months} does not cover requested {start}..{end}"
    return None


def check_confirmatory_provenance(start: str, end: str, experiment_id: str, pre_registration: str,
                                  out_suffix: str, confirmatory_flag: bool = False,
                                  provenance_manifest: Optional[str] = None,
                                  terms_evidence: Optional[str] = None) -> Optional[str]:
    """Return error message if confirmatory run is inadmissible; else None.

    Fail-closed. Legacy manifests require identity GO; v5+ manifests (artifact
    fclr016_v5_provenance_license_manifest / schema_version>=5 / explicit fields)
    additionally require confirmatory_provenance_go, resolved license/terms,
    admissibility_complete, no_confirmatory_outcomes, and scope coverage.

    If terms_evidence is provided (path to terms evidence artifact), it is
    cross-checked fail-closed: RESOLVED_VERIFIED requires required human fields
    (terms_url_reviewed, access_date_utc, reviewer_role, conclusion),
    fabricated=false, and non-agent-only reviewer_role. A manifest claiming GO
    cannot be accepted when cross-checked terms evidence is unresolved/missing
    required fields (no false-accept).
    """
    if not _is_confirmatory_intent(experiment_id, pre_registration, out_suffix, confirmatory_flag):
        return None
    te_obj = None
    if terms_evidence is not None:
        tep = Path(terms_evidence)
        if not tep.exists():
            return f"CONFIRMATORY PROVENANCE GUARD: --terms-evidence not found: {tep}"
        try:
            te_obj = json.loads(tep.read_text(encoding="utf-8"))
        except Exception as e:
            return f"CONFIRMATORY PROVENANCE GUARD: cannot read terms evidence: {e}"
        # Always validate required fields/markers when a RESOLVED claim is present;
        # also refuse fabricated=true regardless of status.
        te_err = _check_resolved_terms_evidence_package(te_obj)
        if te_err:
            return f"CONFIRMATORY PROVENANCE GUARD: terms evidence cross-check failed: {te_err}"
        if te_obj.get("fabricated") is True:
            return "CONFIRMATORY PROVENANCE GUARD: terms evidence fabricated marker present"
    if provenance_manifest:
        mp = Path(provenance_manifest)
        if not mp.exists():
            return f"CONFIRMATORY PROVENANCE GUARD: --provenance-manifest not found: {mp}"
        try:
            m = json.loads(mp.read_text())
        except Exception as e:
            return f"CONFIRMATORY PROVENANCE GUARD: cannot read provenance manifest: {e}"
        # If terms evidence provided and unresolved, no manifest can pass confirmatory GO.
        if te_obj is not None:
            te_resolved = te_obj.get("status") == RESOLVED_TERMS and te_obj.get("fabricated") is False
            if not te_resolved:
                return f"CONFIRMATORY PROVENANCE GUARD: terms evidence not RESOLVED_VERIFIED (status={te_obj.get('status')!r}); confirmatory GO refused"
        identity = str(m.get("cache_identity_vs_binance_vision", ""))
        identity_go = identity.startswith("GO") and "IDENTITY_ONLY" not in identity.upper()
        # detect v5/strict schema
        is_v5 = (
            str(m.get("artifact", "")).startswith("fclr016_v5_provenance_license_manifest")
            or int(m.get("schema_version", 0) or 0) >= 5
            or "license_terms" in m
            or "admissibility_complete" in m
        )
        if is_v5:
            if m.get("confirmatory_provenance_go") is not True:
                return f"CONFIRMATORY PROVENANCE GUARD: v5 manifest confirmatory_provenance_go!=true (NO_GO): {mp}"
            if m.get("admissibility_complete") is not True:
                return f"CONFIRMATORY PROVENANCE GUARD: v5 manifest admissibility_complete!=true: {mp}"
            if m.get("no_confirmatory_outcomes") is not True:
                return f"CONFIRMATORY PROVENANCE GUARD: v5 manifest must set no_confirmatory_outcomes=true (admissibility artifact): {mp}"
            lt = m.get("license_terms") or {}
            if lt.get("status") != "RESOLVED_VERIFIED" or lt.get("fabricated") is True:
                return f"CONFIRMATORY PROVENANCE GUARD: v5 license_terms unresolved/unverified or fabricated marker present: {mp}"
            scope_err = _manifest_scope_covers(m, start, end)
            if scope_err:
                return f"CONFIRMATORY PROVENANCE GUARD: {scope_err}: {mp}"
            if not identity.startswith("GO"):
                return f"CONFIRMATORY PROVENANCE GUARD: v5 identity evidence not GO: {identity!r}: {mp}"
            return None
        # legacy behavior
        if te_obj is not None and te_obj.get("status") != RESOLVED_TERMS:
            return f"CONFIRMATORY PROVENANCE GUARD: terms evidence cross-check requires RESOLVED_VERIFIED for legacy confirmatory path (status={te_obj.get('status')!r})"
        if not identity_go and not m.get("confirmatory_provenance_go"):
            return f"CONFIRMATORY PROVENANCE GUARD: manifest not GO: {mp}"
        return None
    if _range_overlaps_unprovenanced(start, end):
        return (
            "CONFIRMATORY PROVENANCE GUARD (FCLR-014 NO-GO): Refusing confirmatory-labeled run on "
            f"unprovenanced 2025+ cache window {start}..{end} (experiment={experiment_id}). "
            "2025-01..2025-12,2026-01..06,2026-10 cache months lack admissible confirmatory provenance/license evidence "
            "(research_state/fclr014_local_audit/fclr014_provenance_decision_20261107T133102Z.md). "
            "Provide --provenance-manifest with verified Binance Vision identity+licensing evidence, or run as exploratory/pilot. "
            "Do NOT run claim outcomes on unprovenanced data."
        )
    # 2024 ranges outside FCLR-015 verified slice: fail closed for confirmatory
    s, e = str(start)[:10], str(end)[:10]
    in_proven = any(s >= a and e <= b for a, b in PROVENANCED_CONFIRMATORY_RANGES)
    if not in_proven and not (s < "2025" and e < "2025"):
        pass
    elif not in_proven and s.startswith("2024"):
        # 2024 but outside verified 04-09: advisory but allow only if not overlapping consumed? fail closed
        return (
            f"CONFIRMATORY PROVENANCE GUARD: 2024 range {start}..{end} outside FCLR-015 identity-verified slice "
            f"{PROVENANCED_CONFIRMATORY_RANGES} and may overlap consumed/confounded windows; provide --provenance-manifest or use exploratory."
        )
    return None

# --- Admissibility package check (FCLR-016 v5) ---
# Library-callable, read-only: validates provenance/license manifest, completeness/leakage
# audit, terms evidence, and prereg draft as a coherent fail-closed package without loading
# any kline/funding/outcome data. Emits canonical JSON summary for guard acceptance evidence.
# Mirrors scripts/fclr016_validate_v5_admissibility.py gate logic as a callable check.

RESOLVED_TERMS = "RESOLVED_VERIFIED"
PASS_COMPLETENESS = "PASS_COMPLETENESS_LEAKAGE_DETERMINISTIC"


def admissibility_sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _admissibility_artifact_common(name: str, d: dict) -> Optional[str]:
    if d.get("no_confirmatory_outcomes") is not True:
        return f"{name}.no_confirmatory_outcomes must be true"
    if d.get("fabricated") is True:
        return f"{name}.fabricated must not be true"
    if str(d.get("confirmatory_claim_go", "")).upper() not in ("NO_GO", "GO", ""):
        return f"{name}.confirmatory_claim_go has unexpected value"
    return None


def _admissibility_scope_window(d: dict) -> Optional[str]:
    return (d.get("frozen_scope") or {}).get("window")


def _check_resolved_terms_evidence_package(te: dict) -> Optional[str]:
    """Fail-closed checks when terms evidence claims RESOLVED_VERIFIED (aligned with validator)."""
    if te.get("status") != RESOLVED_TERMS:
        return None
    if te.get("fabricated") is not False:
        return "RESOLVED_VERIFIED terms evidence must set fabricated=false"
    for k in ("terms_url_reviewed", "access_date_utc", "reviewer_role", "conclusion"):
        v = te.get(k)
        if v is None or (isinstance(v, str) and not v.strip()):
            return f"RESOLVED_VERIFIED terms evidence missing required field: {k}"
    rr = str(te.get("reviewer_role", "")).lower()
    if "agent" in rr and "human" not in rr and "legal" not in rr and "maintainer" not in rr:
        return "RESOLVED_VERIFIED terms evidence reviewer_role appears agent-only (human/legal review required)"
    return None


def check_admissibility_package(provenance_manifest_path: str, completeness_audit_path: str,
                                terms_evidence_path: str, prereg_draft_path: str,
                                expect_go: bool = False) -> dict:
    """Fail-closed Gate 4 v5 admissibility package check. No outcomes/data loaded."""
    pm_p, ca_p, te_p, pr_p = map(Path, [provenance_manifest_path, completeness_audit_path,
                                        terms_evidence_path, prereg_draft_path])
    hashes = {"provenance_manifest": None, "completeness_audit": None, "terms_evidence": None, "prereg_draft": None}
    for key, p in [("provenance_manifest", pm_p), ("completeness_audit", ca_p), ("terms_evidence", te_p), ("prereg_draft", pr_p)]:
        if not p.exists():
            return {"validator": "run_funding_ablations.admissibility_package", "ok": False, "expect_go": bool(expect_go),
                    "all_go": False, "confirmatory_outcomes_permitted": False, "expect_go_refused": bool(expect_go),
                    "gates": {}, "blockers": ["missing_artifact"], "errors": [f"missing: {p}"], "error": f"missing: {p}", "hashes": hashes}
        if not p.is_file():
            return {"validator": "run_funding_ablations.admissibility_package", "ok": False, "expect_go": bool(expect_go),
                    "all_go": False, "confirmatory_outcomes_permitted": False, "expect_go_refused": bool(expect_go),
                    "gates": {}, "blockers": ["invalid_artifact_path"], "errors": [f"not a file: {p}"], "error": f"not a file: {p}", "hashes": hashes}
        try:
            hashes[key] = admissibility_sha256(p)
        except Exception as e:
            return {"validator": "run_funding_ablations.admissibility_package", "ok": False, "expect_go": bool(expect_go),
                    "all_go": False, "confirmatory_outcomes_permitted": False, "expect_go_refused": bool(expect_go),
                    "gates": {}, "blockers": ["unreadable_artifact"], "errors": [f"cannot hash {p}: {e}"], "error": f"cannot hash {p}: {e}", "hashes": hashes}
    try:
        pm, ca, te, pr = (json.loads(p.read_text(encoding="utf-8")) for p in (pm_p, ca_p, te_p, pr_p))
    except Exception as e:
        return {"validator": "run_funding_ablations.admissibility_package", "ok": False, "expect_go": bool(expect_go),
                "all_go": False, "confirmatory_outcomes_permitted": False, "expect_go_refused": bool(expect_go),
                "gates": {}, "blockers": ["parse_error"], "errors": [f"cannot parse artifact: {e}"], "error": f"cannot parse artifact: {e}", "hashes": hashes}
    errors: List[str] = []
    for name, d in [("provenance", pm), ("completeness", ca), ("terms", te), ("prereg", pr)]:
        err = _admissibility_artifact_common(name, d)
        if err:
            errors.append(err)
    lt = pm.get("license_terms") or {}
    if lt.get("fabricated") is True:
        errors.append("provenance.license_terms.fabricated must not be true")
    if te.get("fabricated") is True:
        errors.append("terms evidence fabricated marker inconsistent")
    if te.get("status") == RESOLVED_TERMS and te.get("fabricated") is not False:
        errors.append("terms evidence fabricated marker inconsistent with resolved status")
    scope = pm.get("frozen_scope") or {}
    if not scope:
        errors.append("provenance manifest missing frozen_scope")
    scope_window = _admissibility_scope_window(pm)
    for name, d in [("completeness", ca), ("terms", te), ("prereg", pr)]:
        dw = _admissibility_scope_window(d)
        if dw and scope_window and dw != scope_window:
            errors.append(f"{name} scope window mismatch vs provenance manifest")
    if pr.get("draft") is True:
        for k in ("frozen_before_outcomes", "promotable_to_frozen", "admissibility_complete", "license_terms_resolved"):
            if pr.get(k) is True:
                errors.append(f"draft prereg cannot set {k}=true")
        if pr.get("confirmatory_claim_go") != "NO_GO":
            errors.append("draft prereg must keep confirmatory_claim_go=NO_GO")
        if (pr.get("gates") or {}).get("confirmatory_outcomes_permitted") is True:
            errors.append("draft prereg gates.confirmatory_outcomes_permitted must be false")
    terms_err = _check_resolved_terms_evidence_package(te)
    if terms_err:
        errors.append(terms_err)
    terms_resolved = te.get("status") == RESOLVED_TERMS and te.get("fabricated") is False and terms_err is None
    if te.get("status") in ("EXPLICIT_BLOCKER_UNRESOLVED", "UNRESOLVED", "BLOCKED") and (
        pm.get("confirmatory_provenance_go") is True or pm.get("admissibility_complete") is True
    ):
        errors.append("provenance manifest cannot be GO while terms evidence is unresolved")
    if pm.get("confirmatory_provenance_go") is True and not terms_resolved:
        errors.append("provenance confirmatory_provenance_go=true requires RESOLVED_VERIFIED terms evidence")
    if (pm.get("license_terms") or {}).get("status") == "RESOLVED_VERIFIED" and not terms_resolved:
        errors.append("provenance manifest claims RESOLVED_VERIFIED license_terms but terms evidence artifact is not resolved")
    if ca.get("verdict") != PASS_COMPLETENESS and (pm.get("admissibility_complete") is True or expect_go):
        errors.append(f"admissibility/expect-go requires completeness verdict {PASS_COMPLETENESS}")
    if (ca.get("completeness") or {}).get("ok") is False and ca.get("verdict") == PASS_COMPLETENESS:
        errors.append("completeness verdict PASS but completeness.ok is false")
    # non-draft prereg claiming GO/admissible without terms resolved/provenance is refused
    if pr.get("draft") is False and (pr.get("confirmatory_claim_go") == "GO" or pr.get("admissibility_complete") is True):
        if not terms_resolved:
            errors.append("non-draft GO/admissible prereg requires RESOLVED_VERIFIED terms evidence")
        if pm.get("confirmatory_provenance_go") is not True or pm.get("admissibility_complete") is not True:
            errors.append("non-draft GO/admissible prereg requires provenance manifest GO+admissibility_complete")
    refs = (pr.get("admissibility_refs_sha256") or {})
    expected = {
        "provenance_license_manifest": admissibility_sha256(pm_p),
        "completeness_leakage_audit": admissibility_sha256(ca_p),
    }
    for k, v in expected.items():
        if refs.get(k) and refs.get(k) != v:
            errors.append(f"prereg refs sha256 mismatch for {k}: {refs.get(k)} != {v}")
    if refs.get("terms_evidence") and refs.get("terms_evidence") != admissibility_sha256(te_p):
        errors.append(f"prereg refs sha256 mismatch for terms_evidence: {refs.get('terms_evidence')} != {admissibility_sha256(te_p)}")
    gates = {
        "terms_resolved_verified": bool(terms_resolved),
        "provenance_manifest_go": bool(pm.get("confirmatory_provenance_go") is True and pm.get("admissibility_complete") is True),
        "completeness_leakage_pass": bool(ca.get("verdict") == PASS_COMPLETENESS and ca.get("admissibility_complete") is True),
        "prereg_frozen_non_draft": bool(pr.get("draft") is False and pr.get("frozen_before_outcomes") is True and pr.get("admissibility_complete") is True),
        "prereg_claim_go": bool(pr.get("confirmatory_claim_go") == "GO"),
    }
    blockers = [k for k, v in gates.items() if not v]
    all_go = not blockers and not errors and all([
        pm.get("no_confirmatory_outcomes") is True,
        ca.get("no_confirmatory_outcomes") is True,
        te.get("no_confirmatory_outcomes") is True,
        pr.get("no_confirmatory_outcomes") is True,
        pm.get("fabricated") is not True,
        te.get("fabricated") is False,
    ])
    if expect_go and not all_go:
        return {
            "validator": "run_funding_ablations.admissibility_package",
            "ok": True,  # package parsed/validated; expect-go refusal is structured non-GO
            "expect_go": True,
            "expect_go_refused": True,
            "all_go": False,
            "confirmatory_outcomes_permitted": False,
            "gates": gates,
            "blockers": blockers,
            "errors": errors,
            "hashes": {
                "provenance_manifest": admissibility_sha256(pm_p),
                "completeness_audit": admissibility_sha256(ca_p),
                "terms_evidence": admissibility_sha256(te_p),
                "prereg_draft": admissibility_sha256(pr_p),
            },
        }
    return {
        "validator": "run_funding_ablations.admissibility_package",
        "ok": True,
        "expect_go": bool(expect_go),
        "all_go": bool(all_go),
        "confirmatory_outcomes_permitted": bool(all_go),
        "gates": gates,
        "blockers": blockers,
        "errors": errors,
        "hashes": {
            "provenance_manifest": admissibility_sha256(pm_p),
            "completeness_audit": admissibility_sha256(ca_p),
            "terms_evidence": admissibility_sha256(te_p),
            "prereg_draft": admissibility_sha256(pr_p),
        },
    }


PRE_REG_SPLITS_V1 = [
    {"id": 0, "train": ("2024-01-01T00:00:00+00:00", "2024-01-28T23:59:59+00:00"), "test": ("2024-02-05T00:00:00+00:00", "2024-02-18T23:59:59+00:00")},
    {"id": 1, "train": ("2024-01-15T00:00:00+00:00", "2024-02-11T23:59:59+00:00"), "test": ("2024-02-19T00:00:00+00:00", "2024-03-03T23:59:59+00:00")},
    {"id": 2, "train": ("2024-01-29T00:00:00+00:00", "2024-02-25T23:59:59+00:00"), "test": ("2024-03-04T00:00:00+00:00", "2024-03-17T23:59:59+00:00")},
]
PRE_REG_SPLITS_V3_30D = [
    {"id": 0, "train": ("2024-04-01T00:00:00+00:00", "2024-05-07T23:59:59+00:00"), "test": ("2024-05-15T00:00:00+00:00", "2024-06-13T23:59:59+00:00")},
    {"id": 1, "train": ("2024-04-01T00:00:00+00:00", "2024-06-06T23:59:59+00:00"), "test": ("2024-06-14T00:00:00+00:00", "2024-07-13T23:59:59+00:00")},
    {"id": 2, "train": ("2024-04-01T00:00:00+00:00", "2024-07-06T23:59:59+00:00"), "test": ("2024-07-14T00:00:00+00:00", "2024-08-12T23:59:59+00:00")},
    {"id": 3, "train": ("2024-04-01T00:00:00+00:00", "2024-08-05T23:59:59+00:00"), "test": ("2024-08-13T00:00:00+00:00", "2024-09-11T23:59:59+00:00")},
]
PRE_REG_SPLITS = PRE_REG_SPLITS_V1  # default/v1; tests import this name
PURGE_DAYS = 7
EMBARGO_DAYS = 7
BOOTSTRAP_SEED = 12345
BOOTSTRAP_REPS = 2000
BOOTSTRAP_BLOCK_HOURS = 24
BOOTSTRAP_ALPHA = 0.05


def git_sha() -> str:
    try:
        out = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except Exception:
        return "unknown"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_manifest_json(p: Path) -> dict:
    """LFS-tolerant manifest read: missing/pointer/unreadable/invalid -> {}."""
    if not p.exists():
        return {}
    try:
        txt = p.read_text()
        if txt.lstrip().startswith("version https://git-lfs.github.com/spec/v1"):
            return {}
        return json.loads(txt)
    except Exception:
        return {}


def ensure_extracted(symbols: List[str]) -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    from src.ingest import loader
    # 1) canonical contract-day zips at repo root (legacy layout)
    zips = loader.discover_zips(ZIPS_DIR)
    # 2) canonical contract-day zips in the local data cache under <SYM>_<YYYY_MM>/
    #    (the primary provenanced source for 2024-01..2024-03 klines). These are
    #    unauthenticated local files only; extraction is idempotent and bounded.
    if CACHE.exists():
        for sym in symbols:
            for zp in sorted(CACHE.glob(f"{sym}_*/{sym}-1h-*.zip")):
                if zp.is_file():
                    zips.append(zp)
            for zp in sorted(CACHE.glob(f"{sym}_*/{sym}-fundingRate-*.zip")):
                if zp.is_file():
                    zips.append(zp)
    for zp in zips:
        if not any(s in zp.name for s in symbols):
            continue
        try:
            # Remove any pre-existing RAW copy (e.g. zero-volume placeholder CSVs that
            # shipped at repo root for the same stem) so the provenanced canonical zip
            # overwrites them. loader.extract_zip skips existing targets by design, so
            # the placeholder would otherwise silently shadow the real data.
            with zipfile.ZipFile(zp) as zf:
                for member in zf.namelist():
                    t = RAW / member
                    if t.exists():
                        t.unlink()
            loader.extract_zip(zp, RAW)
        except Exception:
            continue


def _iter_readable_sources(patterns: List[str], prefer_csv: bool = True, include_cache: bool = False,
                           dedupe_by_stem: bool = True, canonical_sub: str = "klines-") -> List[Path]:
    """Deterministic local sources (CSV/ZIP). RAW primary; cache opt-in to preserve v1 behavior.

    When ``dedupe_by_stem`` is set, files sharing a stem (e.g. the same contract-day) are
    collapsed to one representative. Canonical contract-kline archives live under a
    ``<SYM>_<YYYY_MM>/klines-<YYYY-MM-DD>/`` directory; the same date also appears as a
    top-level placeholder zip and inside mark/index/premium directories. The canonical
    copy carries real volume; the placeholders are zero-volume stubs. Keep only the
    canonical copy to avoid duplicate (symbol, timestamp) rows and the downstream
    "cannot reindex on duplicate labels" failure in the funding merge.
    """
    seen = set()
    out: List[Path] = []
    roots = [RAW]
    if include_cache and CACHE.exists():
        roots.append(CACHE)
    for root in roots:
        for pat in patterns:
            for fp in sorted(root.glob(pat)):
                if not fp.is_file():
                    continue
                key = fp.resolve()
                if key in seen:
                    continue
                seen.add(key)
                out.append(fp)
    if prefer_csv:
        csvs = [p for p in out if p.suffix.lower() == '.csv']
        zips = [p for p in out if p.suffix.lower() == '.zip']
        stems = {p.stem for p in csvs}
        zips = [z for z in zips if z.stem not in stems]
        out = sorted(csvs) + sorted(zips)
    if dedupe_by_stem:
        by_stem: Dict[str, List[Path]] = {}
        for p in out:
            by_stem.setdefault(p.stem, []).append(p)
        out = []
        for stem, cands in by_stem.items():
            if len(cands) == 1:
                out.append(cands[0])
                continue
            # Prefer a path that lives under the canonical klines- directory.
            canon = [c for c in cands if canonical_sub in c.parent.name]
            out.append(canon[0] if canon else sorted(cands, key=lambda x: str(x))[0])
    return sorted(out, key=lambda x: (x.suffix != '.csv', str(x)))


def _load_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == '.zip':
        import zipfile
        with zipfile.ZipFile(path) as zf:
            names = [n for n in zf.namelist() if n.lower().endswith('.csv')]
            if not names:
                raise ValueError(f'no csv in {path}')
            # deterministic: first csv
            with zf.open(sorted(names)[0]) as f:
                return pd.read_csv(f)
    return pd.read_csv(path)


def load_funding_series(symbols: List[str], start: str, end: str, include_cache: bool = False) -> pd.DataFrame:
    ensure_extracted(symbols)
    from src.ingest import loader
    frames = []
    for sym in symbols:
        flist = []
        pats = [f"{sym}-fundingRate-*.csv", f"{sym}-fundingRate-*.zip",
                f"{sym}_*/{sym}-fundingRate-*.csv", f"{sym}_*/{sym}-fundingRate-*.zip",
                f"{sym}_*/*/{sym}-fundingRate-*.csv", f"{sym}_*/*/{sym}-fundingRate-*.zip"]
        for fp in _iter_readable_sources(pats, include_cache=include_cache):
            if sym not in fp.name or 'fundingRate' not in fp.name:
                continue
            try:
                df = _load_table(fp)
                df = df.rename(columns={c: c.strip() for c in df.columns})
                if 'calc_time' not in df.columns:
                    continue
                df['calc_time'] = loader._to_utc_ms(df['calc_time'])
                df = df.sort_values('calc_time').drop_duplicates('calc_time', keep='last').set_index('calc_time')
                if 'last_funding_rate' in df.columns:
                    df['last_funding_rate'] = pd.to_numeric(df['last_funding_rate'], errors='coerce')
                if 'funding_interval_hours' in df.columns:
                    df['funding_interval_hours'] = pd.to_numeric(df['funding_interval_hours'], errors='coerce').astype('Int64')
                flist.append(df)
            except Exception:
                continue
        if not flist:
            continue
        fdf = pd.concat(flist).sort_index()
        fdf = fdf.loc[(fdf.index >= pd.Timestamp(start, tz='UTC')) & (fdf.index <= pd.Timestamp(end, tz='UTC') + pd.Timedelta(days=1))]
        fdf = fdf.reset_index().rename(columns={'calc_time': 'timestamp'})
        fdf['symbol'] = sym
        frames.append(fdf)
    if not frames:
        raise RuntimeError('No funding data loaded')
    panel = pd.concat(frames, ignore_index=True)
    panel['timestamp'] = pd.to_datetime(panel['timestamp'], utc=True)
    return panel.set_index(['symbol', 'timestamp']).sort_index()


def load_kline_series(symbols: List[str], start: str, end: str, horizon: int = 24, include_cache: bool = False) -> pd.DataFrame:
    ensure_extracted(symbols)
    from src.ingest import loader
    from src.features import volatility as vf
    frames = []
    for sym in symbols:
        klist = []
        pats = [f"{sym}-1h-*.csv", f"{sym}-1h-*.zip",
                f"{sym}_*/{sym}-1h-*.csv", f"{sym}_*/{sym}-1h-*.zip",
                f"{sym}_*/klines-*/{sym}-1h-*.csv", f"{sym}_*/klines-*/{sym}-1h-*.zip"]
        for fp in _iter_readable_sources(pats, include_cache=include_cache):
            if sym not in fp.name or '1h' not in fp.name or 'fundingRate' in fp.name:
                continue
            # skip mark/index/premium kline variants
            if any(x in str(fp) for x in ('indexPriceKlines', 'markPriceKlines', 'premiumIndexKlines')):
                continue
            try:
                df = _load_table(fp)
                df = df.rename(columns={c: c.strip() for c in df.columns})
                if 'open_time' not in df.columns:
                    continue
                df['open_time'] = loader._to_utc_ms(df['open_time'])
                df = df.sort_values('open_time').drop_duplicates('open_time', keep='last').set_index('open_time')
                for col in ['open', 'high', 'low', 'close', 'volume']:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                c = pd.to_numeric(df.get('close'), errors='coerce')
                if c is None or len(c) == 0:
                    continue
                pos = c[c > 0]
                if len(pos) == 0 or (c <= 0).mean() > 0.2:
                    continue
                df.loc[c <= 0, 'close'] = np.nan
                df['_file_med_close'] = float(pos.median())
                klist.append(df)
            except Exception:
                continue
        if not klist:
            continue
        kdf = pd.concat(klist).sort_index()
        # deterministic integrity: drop file-slices whose median close is wildly inconsistent
        # with symbol's robust center (catches corrupt local cache artifacts, e.g. BTC close ~1e-3).
        # This is a data-quality guard, not outcome tuning; threshold is scale-ratio only.
        if '_file_med_close' in kdf.columns:
            ref = pd.to_numeric(kdf['_file_med_close'], errors='coerce')
            center = float(ref[ref > 0].median()) if (ref > 0).any() else None
            if center and center > 0:
                bad = (ref <= 0) | (ref < center / 500.0) | (ref > center * 500.0)
                kdf = kdf.loc[~bad].copy()
            kdf = kdf.drop(columns=['_file_med_close'], errors='ignore')
        kdf = kdf.loc[(kdf.index >= pd.Timestamp(start, tz='UTC')) & (kdf.index <= pd.Timestamp(end, tz='UTC') + timedelta(days=1))]
        kdf = vf.add_rv_features(kdf, short_windows=[6, 24], long_windows=[168])
        kdf['target_rv'] = vf.forward_rv(kdf['close'], horizon=horizon)
        kdf['rv_lag'] = kdf['rv_trail_24'].shift(1)
        kdf = kdf.reset_index().rename(columns={'open_time': 'timestamp'})
        kdf['symbol'] = sym
        frames.append(kdf)
    if not frames:
        raise RuntimeError('No kline data loaded')
    panel = pd.concat(frames, ignore_index=True)
    panel['timestamp'] = pd.to_datetime(panel['timestamp'], utc=True)
    return panel.set_index(['symbol', 'timestamp']).sort_index()


def load_funding_panel(symbols: List[str], start: str, end: str, include_cache: bool = False) -> pd.DataFrame:
    return load_funding_series(symbols, start, end, include_cache=include_cache)


def load_kline_panel(symbols: List[str], start: str, end: str, horizon: int = 24, include_cache: bool = False) -> pd.DataFrame:
    return load_kline_series(symbols, start, end, horizon=horizon, include_cache=include_cache)


def add_funding_to_panel(kpanel: pd.DataFrame, fpanel: pd.DataFrame) -> pd.DataFrame:
    from src.features import funding as ff
    """Merge funding features onto the kline panel by (symbol, timestamp).

    Funding features are aligned to each contract's kline index via last-known
    value at/before each hour (forward-fill). Missing history stays NaN; the
    merge never zero-fills. Rows without a kline timestamp are dropped.
    """
    out = kpanel.copy()
    feat_frames = []
    for sym in out.index.get_level_values("symbol").unique():
        kidx = out.xs(sym, level="symbol").index
        try:
            fdf = fpanel.xs(sym, level="symbol")
        except KeyError:
            continue
        ffeat = ff.add_funding_features(kidx, fdf)
        ffeat = ffeat.reset_index()
        ffeat["symbol"] = sym
        ffeat = ffeat.set_index(["symbol", "timestamp"]).sort_index()
        feat_frames.append(ffeat)
    if not feat_frames:
        return out
    feats = pd.concat(feat_frames, axis=0)
    feats = feats[~feats.index.duplicated(keep="last")].sort_index()
    new_cols = [c for c in feats.columns if c not in out.columns]
    return out.join(feats[new_cols], how="left")


def fit_predict_ols(train_n: pd.DataFrame, test_n: pd.DataFrame, fcols: List[str]) -> np.ndarray:
    """Direct-variance OLS (same form as the validated Gate 3 RV-only baseline).

    Degenerate inputs are handled explicitly instead of silently inflating
    coefficients: missing required columns fail closed; zero-variance /
    non-finite predictor columns are dropped before the solve (coefficient
    effectively 0); symbols with too few usable rows or no usable predictors
    produce NaN predictions (never spurious forecasts).
    """
    missing = [c for c in fcols if c not in train_n.columns or c not in test_n.columns]
    if missing:
        raise ValueError(f"fit_predict_ols: required feature column(s) missing: {missing}")
    preds = np.full(len(test_n), np.nan)
    for sym, grp in test_n.groupby(level="symbol", sort=False):
        tr = train_n.loc[train_n.index.get_level_values("symbol") == sym]
        ytr = tr["target_rv"].to_numpy(dtype=float)
        Xtr = tr[fcols].to_numpy(dtype=float)
        mask = np.isfinite(ytr) & np.all(np.isfinite(Xtr), axis=1)
        Xc, yc = Xtr[mask], ytr[mask]
        if len(yc) < 2:
            continue
        col_std = Xc.std(axis=0)
        keep = np.isfinite(col_std) & (col_std > 0.0)
        if not bool(np.any(keep)):
            continue
        kept_cols = [c for c, k in zip(fcols, keep.tolist()) if k]
        Xc = Xc[:, keep]
        k = Xc.shape[1]
        XtX = Xc.T @ Xc
        ridge = 1e-10 * np.eye(k)
        try:
            coef = np.linalg.solve(XtX + ridge, Xc.T @ yc)
        except np.linalg.LinAlgError:
            continue
        intercept = float(yc.mean() - coef @ Xc.mean(axis=0))
        Xte = grp[kept_cols].to_numpy(dtype=float)
        p = intercept + Xte @ coef
        p[~np.isfinite(p)] = np.nan
        p = np.maximum(p, 0.0)
        preds[test_n.index.get_indexer(grp.index)] = p
    return preds


def metrics(y: np.ndarray, p: np.ndarray) -> Dict[str, object]:
    from src.volatility import eval as veval
    mask = np.isfinite(y) & np.isfinite(p) & (y > 0) & (p > 0)
    ql = veval.qlike(y.tolist(), p.tolist())
    ma = veval.mae(y.tolist(), p.tolist())
    mse_v = veval.mse(y.tolist(), p.tolist())
    rmse_v = float(np.sqrt(mse_v)) if mse_v is not None and np.isfinite(mse_v) else None
    neg = int(np.sum(np.isfinite(p) & (p <= 0)))
    return {"qlike": ql, "mae": ma, "rmse": rmse_v, "valid_n": int(mask.sum()), "neg_pred": neg, "n": int(len(y))}


def paired_qlike_by_time(y: np.ndarray, p_base: np.ndarray, p_alt: np.ndarray, ts: pd.DatetimeIndex) -> pd.DataFrame:
    """Paired per-observation QLIKE contributions on jointly valid rows, by timestamp."""
    y = np.asarray(y, dtype=float)
    p_base = np.asarray(p_base, dtype=float)
    p_alt = np.asarray(p_alt, dtype=float)
    mask = np.isfinite(y) & np.isfinite(p_base) & np.isfinite(p_alt) & (y > 0) & (p_base > 0) & (p_alt > 0)
    if not mask.any():
        return pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"])
    yv, bv, av = y[mask], p_base[mask], p_alt[mask]
    tsv = pd.DatetimeIndex(ts[mask])
    rb = yv / bv
    ra = yv / av
    ql_base = rb - np.log(rb) - 1.0
    ql_alt = ra - np.log(ra) - 1.0
    return pd.DataFrame({"timestamp": tsv, "ql_base": ql_base, "ql_alt": ql_alt, "diff": ql_alt - ql_base})


def block_bootstrap_delta_ci(paired: pd.DataFrame, block_hours: int = BOOTSTRAP_BLOCK_HOURS, n_reps: int = BOOTSTRAP_REPS, seed: int = BOOTSTRAP_SEED, alpha: float = BOOTSTRAP_ALPHA) -> Dict[str, object]:
    """Block bootstrap CI for mean ΔQLIKE (alt-base), resampling whole UTC time blocks jointly across instruments.

    Delegates to hardened src.eval.inference diagnostics while preserving the
    legacy return shape for existing callers (additive diagnostic fields only).
    Non-finite diffs are excluded from inference accounting; effective block
    count and degenerate/too-few-block regimes are reported.
    """
    from src.eval.inference import block_bootstrap_delta_ci_diagnostic
    return block_bootstrap_delta_ci_diagnostic(
        paired, block_hours=block_hours, n_reps=n_reps, seed=seed, alpha=alpha,
    )

def build_prereg_splits(splits: Optional[List[Dict[str, object]]] = None) -> List[wf.SplitBounds]:
    from src.eval import walkforward as wf
    src = PRE_REG_SPLITS if splits is None else splits
    return [
        wf.SplitBounds(
            train=s["train"], validation=s["test"], test=s["test"],
            purge_days=PURGE_DAYS, embargo_days=EMBARGO_DAYS,
        )
        for s in src
    ]


def _split_design_for_range(start: str, end: str) -> Optional[str]:
    """Infer pre-registered split design from requested [start,end] (deterministic, no filename coupling).

    Returns 'v3_30d' when the range matches/encompasses the 4×30-day 2024-04..09 walk-forward
    design (frozen in PRE_REG_SPLITS_V3_30D), else None. Fail-closed to v1 for ambiguous ranges.
    """
    try:
        s = pd.Timestamp(start, tz="UTC").normalize()
        e = pd.Timestamp(end, tz="UTC").normalize()
    except Exception:
        return None
    # Exact/covering match for the pre-registered Apr–Sep 30d design.
    # v3_30d spans train anchor 2024-04-01 through final test end 2024-09-11; requested end 2024-09-30 is fine.
    if s <= pd.Timestamp("2024-04-01", tz="UTC") and e >= pd.Timestamp("2024-09-11", tz="UTC") and e <= pd.Timestamp("2024-12-31", tz="UTC") and s >= pd.Timestamp("2024-03-01", tz="UTC"):
        # Guard: don't steal the v1 Jan-Mar default pilot range.
        v1_end = pd.Timestamp(PRE_REG_SPLITS_V1[-1]["test"][1]).normalize()
        if e <= v1_end:
            return None
        # All v3 test windows must fit inside the requested range.
        fits = all(
            pd.Timestamp(sp["test"][0], tz="UTC").normalize() >= s
            and pd.Timestamp(sp["test"][1], tz="UTC").normalize() <= e
            for sp in PRE_REG_SPLITS_V3_30D
        )
        return "v3_30d" if fits else None
    return None


def select_split_defs(start: str, end: str, out_suffix: str = "", pre_reg_path: str = "",
                      split_design: str = "auto") -> tuple[List[Dict[str, object]], str, str]:
    """Select split definitions deterministically.

    Priority: explicit split_design (v1/v3_30d) > date-range inference (auto) > legacy
    out_suffix/pre_registration name coupling (backward compat). Returns (split_defs, design, source).
    """
    sd = (split_design or "auto").strip().lower()
    if sd in ("v3_30d", "v3-30d", "v3", "30d"):
        return PRE_REG_SPLITS_V3_30D, "v3_30d", "explicit_split_design"
    if sd in ("v1", "default"):
        return PRE_REG_SPLITS_V1, "v1", "explicit_split_design"
    # auto: deterministic date-range inference first (no filename coupling)
    by_range = _split_design_for_range(start, end)
    if by_range == "v3_30d":
        return PRE_REG_SPLITS_V3_30D, "v3_30d", "date_range"
    # legacy backward compat: suffix/prereg naming (preserve existing behavior)
    _low = ((out_suffix or "") + " " + (pre_reg_path or "")).lower()
    if ("v3" in _low and "30d" in _low) or ("v4" in _low):
        return PRE_REG_SPLITS_V3_30D, "v3_30d", "legacy_name_coupling"
    return PRE_REG_SPLITS_V1, "v1", "default"


def run_multisplit(panel: pd.DataFrame, ablations: Dict[str, List[str]], split_defs: Optional[List[Dict[str, object]]] = None) -> Tuple[List[Dict[str, object]], Dict[str, pd.DataFrame], Dict[str, List[pd.DataFrame]]]:
    from src.eval import walkforward as wf
    split_defs = PRE_REG_SPLITS if split_defs is None else split_defs
    splits = build_prereg_splits(split_defs)
    idx = panel.index.get_level_values("timestamp")
    all_results: List[Dict[str, object]] = []
    pooled_paired: Dict[str, List[pd.DataFrame]] = {k: [] for k in ablations.keys() if k != "A_rv_only"}
    split_paired: Dict[str, List[pd.DataFrame]] = {k: [] for k in ablations.keys() if k != "A_rv_only"}
    for i, sp in enumerate(splits):
        meta = split_defs[i]
        split_res: Dict[str, object] = {"split_id": i, "train": meta["train"], "test": meta["test"], "purge_days": PURGE_DAYS, "embargo_days": EMBARGO_DAYS, "ablations": {}}
        train = panel.loc[wf._in_window(idx, sp.train)]
        test = panel.loc[wf._in_window(idx, sp.test)]
        if train.empty or test.empty:
            split_res["status"] = "INSUFFICIENT_DATA"
            split_res["n_train"] = int(len(train)); split_res["n_test"] = int(len(test))
            all_results.append(split_res)
            for k in split_paired:
                split_paired[k].append(pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"]))
            continue
        preds_map: Dict[str, np.ndarray] = {}
        y_test: Optional[np.ndarray] = None
        ts_test: Optional[pd.DatetimeIndex] = None
        for ab_name, fcols in ablations.items():
            fcols = [c for c in fcols if c in panel.columns]
            try:
                train_n, _, test_n, _ = wf.apply_train_only_normalization(train, test, test, fcols)
                p = fit_predict_ols(train_n, test_n, fcols)
                y = test_n["target_rv"].to_numpy(dtype=float)
                m = metrics(y, p)
                m["n_features"] = len(fcols)
                split_res["ablations"][ab_name] = m
                preds_map[ab_name] = p
                y_test = y
                ts_test = test_n.index.get_level_values("timestamp")
            except Exception as e:
                split_res["ablations"][ab_name] = {"err": str(e)}
        if y_test is not None and ts_test is not None and "A_rv_only" in preds_map:
            for ab_name in pooled_paired.keys():
                dfp = paired_qlike_by_time(y_test, preds_map["A_rv_only"], preds_map[ab_name], ts_test) if ab_name in preds_map else pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"])
                pooled_paired[ab_name].append(dfp)
                split_paired[ab_name].append(dfp)
        else:
            for ab_name in split_paired:
                split_paired[ab_name].append(pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"]))
        split_res["status"] = "OK"
        split_res["n_train"] = int(len(train)); split_res["n_test"] = int(len(test))
        all_results.append(split_res)
    pooled = {}
    for k, parts in pooled_paired.items():
        pooled[k] = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame(columns=["timestamp", "ql_base", "ql_alt", "diff"])
    return all_results, pooled, split_paired


def _test_days(win) -> Optional[int]:
    try:
        a = pd.Timestamp(win[0]); b = pd.Timestamp(win[1])
        return int((b.normalize() - a.normalize()).days) + 1
    except Exception:
        return None

def data_sufficiency(symbols: List[str], all_results: List[Dict[str, object]], split_defs: Optional[List[Dict[str, object]]] = None) -> Dict[str, object]:
    split_defs = PRE_REG_SPLITS if split_defs is None else split_defs
    ok_splits = [r for r in all_results if r.get("status") == "OK"]
    test_windows = [r.get("test") for r in ok_splits]
    ok_30 = [w for w in test_windows if _test_days(w) is not None and _test_days(w) >= 30]
    shortfalls = []
    if len(symbols) < 5:
        shortfalls.append(f"instruments={len(symbols)} < 5")
    if len(ok_30) < 3:
        # honest about actual design
        td = [_test_days(s.get('test')) for s in split_defs]
        shortfalls.append(f"insufficient_30day_non_overlapping_test_blocks (ok_30d={len(ok_30)}, required>=3, split_test_days={td})")
    # local admissible cache span note (not a hard fail by itself, but material)
    span_note = 'local_admissible_cache_data_only'
    meets = len(symbols) >= 5 and len(ok_30) >= 3 and len(ok_splits) == len(split_defs)
    return {
        "instruments": len(symbols),
        "instruments_required": 5,
        "ok_splits": len(ok_splits),
        "ok_30day_splits": len(ok_30),
        "test_windows": test_windows,
        "split_test_days": [_test_days(s.get('test')) for s in split_defs],
        "span_note": span_note,
        "meets_claim_worthy_data_sufficiency": meets,
        "meets_claim_worthy": meets,
        "shortfalls": shortfalls,
    }


def replace_section(text: str, marker: str, body: str) -> str:
    if marker in text:
        text = text.split(marker)[0].rstrip()
    return text.rstrip() + "\n\n" + marker + "\n" + body.lstrip("\n") + ("\n" if not body.endswith("\n") else "")


def update_leakage_audit(path: Path, ts: str) -> None:
    txt = path.read_text() if path.exists() else "# Leakage Audit\n"
    marker = "## Funding ablations (Gate 4, multi-split pilot, direct-variance OLS)"
    # remove stale log-ridge and old pilot entries that duplicate/confuse; keep a clean current entry
    stale_markers = [
        "## Funding ablations (Gate 4, pilot log-ridge)",
        "## Funding ablations (Gate 4, pilot direct-variance OLS)",
    ]
    for sm in stale_markers:
        if sm in txt:
            # keep header text before first stale occurrence? easier: rebuild canonical sections
            pass
    body = f"- **Updated:** {ts}\n- [x] Funding ffill last-known at/before hour (no future).\n- [x] Trailing funding stats past-only on aligned series.\n- [x] Chronological multi-split walk-forward, purge/embargo={PURGE_DAYS}d.\n- [x] Train-only normalization per split.\n- [x] Direct-variance OLS fit on train only; predictions floored at zero; no log/exp transform; no test leakage.\n- [x] Block bootstrap resamples whole UTC time blocks jointly across instruments (seed={BOOTSTRAP_SEED}, reps={BOOTSTRAP_REPS}, block={BOOTSTRAP_BLOCK_HOURS}h); no leakage.\n- [x] No basis/premium features added (unavailable/misaligned locally); NaN policy preserved, never zero-filled.\n"
    # strip all Gate 4 ablation sections and append one clean section
    lines = txt.splitlines()
    keep = []
    skip = False
    for ln in lines:
        if ln.startswith("## Funding ablations (Gate 4"):
            skip = True
            continue
        if skip and ln.startswith("## "):
            skip = False
        if not skip:
            keep.append(ln)
    txt2 = "\n".join(keep).rstrip() + "\n\n" + marker + "\n" + body
    path.write_text(txt2)


def main(argv: Optional[List[str]] = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Gate 4 funding ablations (pre-registered). Defaults = v1 behavior.")
    # Default symbol set matches the admissible 5-symbol local cache panel
    # (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT). The previous 4-symbol
    # default silently excluded BNBUSDT, which is present in the cache and is
    # required to meet the >=5-instrument claim-worthy data-sufficiency gate.
    ap.add_argument("--symbols", default="BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT")
    ap.add_argument("--start", default="2024-01-01")
    ap.add_argument("--end", default="2024-03-31")
    ap.add_argument("--horizon", type=int, default=24)
    ap.add_argument("--pre-registration", default="research_state/pre_registration_gate4_funding_multisplit_20261107.md")
    ap.add_argument("--out-suffix", default="", help="Suffix for versioned outputs, e.g. _v2_5sym; empty preserves v1 paths.")
    ap.add_argument("--experiment-id", default="GATE4-FUND-VOL-ABLATIONS-MSPLIT")
    ap.add_argument("--skip-main-summary", action="store_true")
    ap.add_argument("--include-cache", action="store_true", help="Search research_state/data_cache for local admissible files (v3/extended runs).")
    ap.add_argument("--split-design", default="auto", choices=["auto", "v1", "v3_30d"], help="Split design: auto infers deterministically from --start/--end (no filename coupling); v3_30d selects the 4x30-day 2024-04..09 walk-forward design (PRE_REG_SPLITS_V3_30D, 7d purge/embargo). Legacy out_suffix/pre_registration naming remains backward-compatible.")
    ap.add_argument("--confirmatory", action="store_true", help="Assert confirmatory intent; triggers provenance guard (fail-closed on unprovenanced 2025+).")
    ap.add_argument("--provenance-manifest", default=None, help="Path to verified provenance manifest for confirmatory runs.")
    ap.add_argument("--terms-evidence", default=None, help="Path to terms evidence artifact; cross-checked fail-closed (RESOLVED requires human fields, fabricated=false).")
    ap.add_argument("--check-admissibility-package", nargs=4, metavar=("PROVENANCE", "COMPLETENESS", "TERMS", "PREREG"),
                    help="Run Gate 4 v5 admissibility package check on four artifacts; emit canonical JSON summary; no kline/funding/outcome data loaded.")
    ap.add_argument("--dry-run-admissibility", nargs=4, metavar=("PROVENANCE", "COMPLETENESS", "TERMS", "PREREG"),
                    help="Alias for --check-admissibility-package.")
    ap.add_argument("--expect-go", action="store_true", help="With --check-admissibility-package/--dry-run-admissibility, require full confirmatory GO; exit 2 otherwise.")
    args = ap.parse_args(argv)

    # --- Admissibility package check mode (read-only, no outcomes/data loaded) ---
    check_paths = getattr(args, "check_admissibility_package", None) or getattr(args, "dry_run_admissibility", None)
    if check_paths:
        result = check_admissibility_package(*check_paths, expect_go=bool(getattr(args, "expect_go", False)))
        print(json.dumps(result, indent=2, sort_keys=True))
        if not result.get("ok", False):
            return 2
        if getattr(args, "expect_go", False) and not result["all_go"]:
            return 2
        return 0

    prov_err = check_confirmatory_provenance(
        args.start, args.end, args.experiment_id, args.pre_registration, args.out_suffix,
        confirmatory_flag=bool(getattr(args, "confirmatory", False)),
        provenance_manifest=getattr(args, "provenance_manifest", None),
        terms_evidence=getattr(args, "terms_evidence", None),
    )
    if prov_err:
        print(json.dumps({"status": "REFUSED", "guard": "confirmatory_provenance_fclr014", "error": prov_err, "start": args.start, "end": args.end}, indent=2), file=sys.stderr)
        return 2

    symbols = [x.strip() for x in args.symbols.split(",") if x.strip()]
    start, end, horizon = args.start, args.end, args.horizon
    pre_reg_path = args.pre_registration
    out_suffix = args.out_suffix
    experiment_id = args.experiment_id
    RES.mkdir(parents=True, exist_ok=True)
    # select split defs deterministically: explicit flag > date-range inference (no filename coupling) > legacy naming (backward compat)
    split_defs, split_design_resolved, split_design_source = select_split_defs(
        start, end, out_suffix=out_suffix, pre_reg_path=pre_reg_path,
        split_design=getattr(args, "split_design", "auto"),
    )
    use_30d_0409 = split_design_resolved == "v3_30d"
    include_cache = bool(use_30d_0409 or getattr(args, 'include_cache', False))

    # Confirmatory/expect-go-admissible paths must refuse before any data/outcome
    # loader when local data seams are missing/unreadable/nonexistent.
    if _is_confirmatory_intent(args.experiment_id, args.pre_registration, args.out_suffix, bool(getattr(args, 'confirmatory', False))):
        seam_err = _confirmatory_data_path_seam_error(symbols, start, end, include_cache)
        if seam_err:
            print(json.dumps({
                "status": "REFUSED",
                "guard": "confirmatory_data_path_seam",
                "error": seam_err,
                "reason_codes": [p for p in seam_err.split(":", 1)[1].split("|") if p],
                "start": start, "end": end, "symbols": symbols,
                "no_data_loaded": True, "no_outcomes_computed": True,
                "confirmatory_outcomes_permitted": False,
            }, indent=2, sort_keys=True), file=sys.stderr)
            return 2

    kpanel = load_kline_panel(symbols, start, end, horizon=horizon, include_cache=include_cache)
    fpanel = load_funding_panel(symbols, start, end, include_cache=include_cache)
    panel = add_funding_to_panel(kpanel, fpanel)

    base = [c for c in ["rv_trail_24", "rv_trail_168", "rv_trail_6"] if c in panel.columns]
    trail = [c for c in panel.columns if c.startswith(("funding_pct_", "funding_z_"))]
    ablations = {
        "A_rv_only": base[:],
        "B_rv_signed": base + ["funding_signed"],
        "C_rv_abs": base + ["funding_abs"],
        "D_rv_signed_abs": base + ["funding_signed", "funding_abs"],
        "E_rv_funding_trails": base + ["funding_signed", "funding_abs"] + trail,
    }

    all_results, pooled, split_paired = run_multisplit(panel, ablations, split_defs=split_defs)

    def agg(ab_name: str, key: str = "qlike") -> Optional[float]:
        vals = [r["ablations"][ab_name][key] for r in all_results if r.get("status") == "OK" and ab_name in r.get("ablations", {}) and isinstance(r["ablations"][ab_name].get(key), (int, float)) and np.isfinite(r["ablations"][ab_name].get(key))]
        return float(np.mean(vals)) if vals else None

    ci_results = {}
    for ab_name, df in pooled.items():
        ci_results[ab_name] = block_bootstrap_delta_ci(df)
    # per-split paired deltas (primary E vs A and secondaries) — instability visibility
    per_split_deltas = {}
    for ab_name, parts in split_paired.items():
        per_split_deltas[ab_name] = []
        for i, df in enumerate(parts):
            point = float(df["diff"].mean()) if df is not None and not df.empty else None
            per_split_deltas[ab_name].append({"split_id": i, "delta_qlike_vs_A": point, "n_obs": int(len(df)) if df is not None else 0})
    # EXPLORATORY sensitivity (addendum where applicable; not confirmatory, not claim-bearing)
    exploratory_sensitivity = {"label": "EXPLORATORY — not pre-registered primary; do not promote if unstable", "block_hours": {}}
    for bh in [12, 24, 48]:
        exploratory_sensitivity["block_hours"][str(bh)] = {ab: block_bootstrap_delta_ci(df, block_hours=bh) for ab, df in pooled.items()}

    suff = data_sufficiency(symbols, all_results, split_defs=split_defs)
    primary_ci = ci_results.get("E_rv_funding_trails") or {}
    ci_spans_0 = (primary_ci.get("ci_low") is not None and primary_ci.get("ci_high") is not None and primary_ci["ci_low"] <= 0 <= primary_ci["ci_high"])
    if not suff.get("meets_claim_worthy_data_sufficiency"):
        verdict = "PILOT/INCONCLUSIVE (data-sufficiency criteria not met; no claim-worthy inference)"
    elif ci_spans_0:
        verdict = "DATA-SUFFICIENT PILOT / INCONCLUSIVE ON PRIMARY CONTRAST (pre-registered 30-day blocks met; E vs A CI spans 0; no improvement claim)"
    else:
        verdict = "DATA-SUFFICIENT (30-day blocks met) — primary E vs A CI excludes 0 in observed run; requires robustness/leakage review before confirmatory claim; no economic value/overlay claim"

    summary = {
        "generated_at": now_iso(), "git_sha": git_sha(), "symbols": symbols,
        "experiment_id": experiment_id,
        "period": {"start": start, "end": end}, "horizon": horizon,
        "model": "direct-variance OLS HAR (target = forward realized VARIANCE; train-only normalization per split; no log/exp transform)",
        "pre_registration": pre_reg_path,
        "splits": [{"id": s["id"], "train": s["train"], "test": s["test"], "purge_days": PURGE_DAYS, "embargo_days": EMBARGO_DAYS} for s in split_defs],
        "split_design": {"resolved": split_design_resolved, "source": split_design_source, "arg": getattr(args, "split_design", "auto")},
        "include_cache": bool(include_cache),
        "aggregate": {k: {"qlike": agg(k, "qlike"), "mae": agg(k, "mae"), "rmse": agg(k, "rmse")} for k in ablations.keys()},
        "contrasts_vs_A": ci_results,
        "per_split_paired_delta_vs_A": per_split_deltas,
        "exploratory_sensitivity_block_hours": exploratory_sensitivity,
        "splits_detail": all_results,
        "data_sufficiency": suff,
        "bootstrap": {"seed": BOOTSTRAP_SEED, "reps": BOOTSTRAP_REPS, "block_hours": BOOTSTRAP_BLOCK_HOURS, "alpha": BOOTSTRAP_ALPHA, "joint_across_instruments": True, "resamples_time_blocks": True},
        "verdict": verdict,
        "primary_contrast_inconclusive_ci_spans_zero": ( (ci_results.get("E_rv_funding_trails") or {}).get("ci_low") is not None and (ci_results.get("E_rv_funding_trails") or {}).get("ci_high") is not None and (ci_results.get("E_rv_funding_trails") or {})["ci_low"] <= 0 <= (ci_results.get("E_rv_funding_trails") or {})["ci_high"] ),
    }
    qA = summary["aggregate"]["A_rv_only"]["qlike"]

    out_md = RES / f"evaluation_summary_funding{out_suffix}.md"
    lines = [
        "# Evaluation Summary - Funding Ablations (Gate 4, multi-split pilot)",
        "", f"**Generated:** {summary['generated_at']}", f"**Git SHA:** {summary['git_sha']}",
        f"**Pre-registration:** `{summary['pre_registration']}` (frozen before outcomes)",
        f"**Scope:** {', '.join(symbols)}, {start} to {end}, 24h forward RV, {len(split_defs)} pre-registered walk-forward splits",
        f"**Model:** {summary['model']}",
        f"**Verdict:** **{verdict}**",
        "",
        "## Data Sufficiency (honest)",
        f"- instruments={suff['instruments']} (required >=5): {'MET' if suff['instruments']>=5 else 'NOT MET'}",
        f"- claim-worthy: {suff['meets_claim_worthy']}",
    ]
    for sh in suff["shortfalls"]:
        lines.append(f"- shortfall: {sh}")
    lines += [
        "", "## Aggregate (mean across OK splits)",
        "| Ablation | QLIKE | MAE | RMSE | ΔQLIKE vs A (pooled paired) | 95% block-bootstrap CI | n_obs/n_blocks |",
        "|---|---|---|---|---|---|---|",
    ]
    for k in ablations.keys():
        a = summary["aggregate"][k]
        ci = ci_results.get(k)
        if k == "A_rv_only" or not ci:
            dstr = "—"; cistr = "—"; nstr = "—"
        else:
            dstr = f"{ci['point']}" if ci.get('point') is not None else "NA"
            cistr = f"[{ci['ci_low']}, {ci['ci_high']}]" if ci.get('ci_low') is not None else "NA"
            nstr = f"{ci.get('n_obs',0)}/{ci.get('n_blocks',0)}"
        lines.append(f"| {k} | {a['qlike']} | {a['mae']} | {a['rmse']} | {dstr} | {cistr} | {nstr} |")
    lines += ["", "## Per-Split Paired ΔQLIKE vs A (instability visibility)"]
    nsp=len(split_defs); header = "| Contrast | " + " | ".join([f"Split {i}" for i in range(nsp)]) + f" | n_obs ({'/'.join(str(i) for i in range(nsp))}) |"; lines.append(header)
    lines.append("|---|" + "|".join(["---:"]*nsp) + "|---|")
    for ab in [k for k in ablations.keys() if k != "A_rv_only"]:
        rows = per_split_deltas.get(ab, [])
        vals = [(str(r["delta_qlike_vs_A"]) if r.get("delta_qlike_vs_A") is not None else "NA") for r in rows]
        ns = "/".join(str(r.get("n_obs",0)) for r in rows)
        while len(vals) < nsp: vals.append("NA")
        lines.append(f"| {ab} vs A | " + " | ".join(vals[:nsp]) + f" | {ns} |")
    lines += ["", "## Exploratory Sensitivity (NOT confirmatory; do not promote if unstable)", "> Block-bootstrap block size sensitivity for paired ΔQLIKE vs A. Pre-registered primary remains block=24h, seed=12345, reps=2000.", "| Contrast | block=12h CI | block=24h CI (primary) | block=48h CI |", "|---|---|---|---|"]
    for ab in [k for k in ablations.keys() if k != "A_rv_only"]:
        def _ci(bh):
            c = exploratory_sensitivity["block_hours"][str(bh)].get(ab, {})
            return f"[{c.get('ci_low')}, {c.get('ci_high')}] (pt={c.get('point')})" if c.get('ci_low') is not None else "NA"
        lines.append(f"| {ab} vs A | {_ci(12)} | {_ci(24)} | {_ci(48)} |")
    lines += ["", "## Per-Split Details"]
    for r in all_results:
        if r.get("status") != "OK":
            lines.append(f"- Split {r['split_id']} ({r.get('train')} -> {r.get('test')}): {r.get('status')} n_train={r.get('n_train')} n_test={r.get('n_test')}")
            continue
        lines.append(f"- Split {r['split_id']}: train {r['train']} | test {r['test']} | purge/embargo={PURGE_DAYS}d | n_train={r.get('n_train')} n_test={r.get('n_test')}")
        for k, v in r["ablations"].items():
            if "err" in v:
                lines.append(f"  - {k}: ERR {v['err']}")
            else:
                lines.append(f"  - {k}: qlike={v['qlike']}, mae={v['mae']}, rmse={v['rmse']}, n_feat={v['n_features']}, valid_n={v['valid_n']}")
    inst_ok = suff.get("instruments", 0) >= suff.get("instruments_required", 5)
    ds_ok = suff.get("meets_claim_worthy_data_sufficiency")
    inst_note = f"instruments={suff.get('instruments')} ({'MET' if inst_ok else f'NOT MET; required >={suff.get("instruments_required",5)}'})"
    lines += [
        "", "## Bootstrap (pre-registered)",
        f"- Paired ΔQLIKE (alt-base; negative = better for QLIKE) with circular block bootstrap on whole UTC time blocks, jointly across instruments.",
        f"- seed={BOOTSTRAP_SEED}, reps={BOOTSTRAP_REPS}, block_hours={BOOTSTRAP_BLOCK_HOURS}, alpha={BOOTSTRAP_ALPHA}, two-sided percentile CI.",
        "", "## Leakage/Alignment Notes",
        "- Funding (8h) aligned to 1h via last-known value at/before each hour (ffill). NaN if missing.",
        "- Trailing funding pct/z computed over rolling windows on aligned series (past-only).",
        "- Chronological splits, 7d purge/embargo, train-only normalization per split.",
        "- Basis/premium not included (no aligned admissible local series verified); missing treated as NaN per policy.",
        "", "## Caveats (non-negotiable)",
        f"- **Verdict:** {verdict}",
        f"- **Data sufficiency:** {inst_note}; ok_30day_splits={suff.get('ok_30day_splits')} (required>=3) => meets_claim_worthy_data_sufficiency={ds_ok}.",
        "- **No economic value claim, no overlay, no Track A linkage.** Observed metrics are out-of-sample forecast evidence under pre-registered design; instability across splits/instrument sets must be reported honestly.",
        "- If any leakage/alignment doubt exists, treat as non-confirmatory.",
    ]
    out_md.write_text("\n".join(lines) + "\n")

    if not args.skip_main_summary and not out_suffix:
        main_sum = RES / "evaluation_summary.md"
        txt = main_sum.read_text() if main_sum.exists() else ""
        addition = [
            f"**Updated:** {summary['generated_at']} (multi-split, {len(split_defs)} splits, direct-variance OLS HAR; verdict={verdict})",
            f"**Verdict:** {verdict}",
            "", "| Ablation | QLIKE (mean) | ΔQLIKE vs A (pooled) | 95% block-bootstrap CI |", "|---|---|---|---|",
        ]
        for k in ablations.keys():
            a = summary["aggregate"][k]
            ci = ci_results.get(k)
            if k == "A_rv_only" or not ci:
                addition.append(f"| {k} | {a['qlike']} | — | — |")
            else:
                addition.append(f"| {k} | {a['qlike']} | {ci.get('point')} | [{ci.get('ci_low')}, {ci.get('ci_high')}] |")
        addition.append("")
        addition.append(f"> Shortfalls: {'; '.join(suff['shortfalls'])}. No confirmatory claim; no economic value claim.")
        main_sum.write_text(replace_section(txt, "## Funding Ablations (Gate 4)", "\n".join(addition)))

    manifest_path = RES / (f"run_manifest_funding{out_suffix}.json" if out_suffix else "run_manifest.json")
    manifest = {} if out_suffix else _load_manifest_json(RES / "run_manifest.json")
    manifest["last_funding_ablations"] = summary["generated_at"]
    manifest["funding_ablations_experiment_id"] = experiment_id
    manifest["funding_ablations"] = summary["aggregate"]
    manifest["funding_ablations_contrasts_vs_A"] = ci_results
    manifest["funding_ablations_note"] = f"pilot_multisplit_direct_variance_ols_inconclusive{out_suffix}"
    manifest["funding_ablations_splits"] = summary["splits"]
    manifest["funding_ablations_split_design"] = summary.get("split_design")
    manifest["funding_ablations_include_cache"] = summary.get("include_cache")
    manifest["funding_ablations_bootstrap"] = summary["bootstrap"]
    manifest["funding_ablations_data_sufficiency"] = suff
    manifest["funding_ablations_per_split_paired_delta_vs_A"] = per_split_deltas
    manifest["funding_ablations_exploratory_sensitivity_block_hours"] = exploratory_sensitivity
    manifest["funding_ablations_verdict"] = verdict
    manifest["funding_ablations_pre_registration"] = summary["pre_registration"]
    manifest_path.write_text(json.dumps(manifest, indent=2, default=str) + "\n")

    update_leakage_audit(RES / "leakage_audit.md", summary["generated_at"])

    print(json.dumps({"verdict": verdict, "split_design": summary.get("split_design"), "include_cache": summary.get("include_cache"), "aggregate": {k: v["qlike"] for k, v in summary["aggregate"].items()}, "primary_E_vs_A": ci_results.get("E_rv_funding_trails")}, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
