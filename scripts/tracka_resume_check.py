#!/usr/bin/env python3
"""Offline bounded Track A resume check (FCLR-NEXT-095).

No network. No writes to real research_state. Runs:
  1) rubric self-check (GO fixture + NO-GO fail-closed)
  2) fixture manifest load + frozen/coverage assertions
  3) harness cold init + frozen config
  4) prereg-block proof (evaluate_forward without prereg => BLOCKED)
Prints machine-readable JSON with pass/fail/timing.
"""
from __future__ import annotations
import json
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.tracka_rubric import assess_candidate, assess_strict_manifest, assess_minimal_fixture
from scripts.fclr010_harness import FCLR010Harness


def _valid_go():
    return {
        "venue": "hyperliquid",
        "unauthenticated": True,
        "requires_api_key": False,
        "requires_signature": False,
        "requester_pays": False,
        "observed_liquidations": True,
        "modeled_or_proxy": False,
        "merges_non_hyperliquid": False,
        "symbol_count": 6,
        "symbols": ["BTC", "ETH", "SOL", "AVAX", "ARB", "DOGE"],
        "completeness_documented": True,
        "license_ok": True,
        "license_spdx": "CC-BY-4.0",
        "schema_fields": ["timestamp", "symbol", "liquidation_notional"],
        "timestamp_normalized_utc": True,
    }


def _valid_strict_manifest_go():
    """097: full manifest with machine-verifiable provenance/label/coverage evidence."""
    c = _valid_go()
    c.update({
        "source_url": "https://example.invalid/hyperliquid/observed_liquidations",
        "dataset_id": "hl-observed-liquidations-v1",
        "access_provenance": "unauthenticated public dataset; Hyperliquid-only; observed fills",
        "label_definition": "exchange_observed_liquidation_fill_notional",
        "coverage_months": 1,
        "coverage_evidence_required": True,
        "complete_months_list": ["2026-11"],
        "claims_3x30d_blocks": True,
        "block_count": 3,
        "block_evidence": [
            {"start": "2026-11-01", "end": "2026-11-30", "days": 30},
            {"start": "2026-12-01", "end": "2026-12-30", "days": 30},
            {"start": "2027-01-01", "end": "2027-01-30", "days": 30},
        ],
        "canonical_symbol_map": {"BTC": "BTC", "ETH": "ETH", "SOL": "SOL", "AVAX": "AVAX", "ARB": "ARB", "DOGE": "DOGE"},
        "symbol_normalization_proof": {"normalized_map": {"BTC": "BTC", "ETH": "ETH", "SOL": "SOL", "AVAX": "AVAX", "ARB": "ARB", "DOGE": "DOGE"}},
        "symbol_proof_covers_claimed_required": True,
    })
    return c


def run() -> dict:
    t0 = time.time()
    checks = {}
    # 1) rubric (097: strict-manifest default path + compat)
    r_go = assess_candidate(_valid_go())
    checks["rubric_go"] = {"pass": r_go["go"] is True and r_go["verdict"] == "GO", "failures": r_go["failures"]}
    r_no = assess_candidate({})
    checks["rubric_fail_closed"] = {"pass": r_no["go"] is False and len(r_no["failures"]) >= 3, "n_failures": len(r_no["failures"])}
    # strict mode rejects minimal-only GO-shaped candidate lacking machine-verifiable evidence
    r_strict_min = assess_strict_manifest(_valid_go())
    checks["rubric_strict_rejects_minimal_go_shaped"] = {
        "pass": r_strict_min["go"] is False and any(f in r_strict_min["failures"] for f in
                ("observed_access_provenance_missing", "label_definition_missing")),
        "failures": r_strict_min["failures"], "mode": "strict_tracka_manifest",
    }
    # compat path preserves legacy minimal behavior
    r_compat = assess_minimal_fixture(_valid_go())
    checks["rubric_minimal_fixture_compat_preserved"] = {"pass": r_compat["go"] is True, "failures": r_compat["failures"]}
    # strict mode accepts full manifest with machine-verifiable evidence
    r_strict_full = assess_strict_manifest(_valid_strict_manifest_go())
    checks["rubric_strict_accepts_full_manifest"] = {"pass": r_strict_full["go"] is True, "failures": r_strict_full["failures"]}
    # 2) fixture manifest
    fx = ROOT / "tests" / "fixtures" / "tracka" / "manifest.json"
    if fx.exists():
        m = json.loads(fx.read_text(encoding="utf-8"))
        sp = m.get("splits") or {}
        ok = bool(sp.get("frozen_before_outcomes")) and len(m.get("symbols") or []) >= 5 and "train" in sp and "test" in sp
        checks["fixture_manifest"] = {"pass": ok, "symbols": len(m.get("symbols") or []), "frozen": bool(sp.get("frozen_before_outcomes"))}
    else:
        checks["fixture_manifest"] = {"pass": False, "error": "missing"}
    # 3) harness cold + frozen config (reads repo manifest; no writes)
    try:
        h = FCLR010Harness(repo_root=ROOT)
        cfg = h.get_frozen_config()
        ok = cfg.get("experiment_id") == "FCLR-010"
        rules = cfg.get("rules") or {}
        if isinstance(rules, dict) and rules:
            ok = ok and rules.get("no_retuning") is True
        # accept split-boundary presence/frozen flag if exposed
        sb = cfg.get("split_boundaries_fclr010") or cfg.get("splits") or {}
        if isinstance(sb, dict) and sb:
            ok = ok and (sb.get("frozen_before_outcomes") is True or "train" in sb or "test" in sb)
        checks["harness_cold"] = {"pass": ok, "experiment_id": cfg.get("experiment_id"), "has_rules": bool(rules), "has_splits": bool(sb)}
    except Exception as e:
        checks["harness_cold"] = {"pass": False, "error": repr(e)}
        h = None
    # 4) prereg-block (uses temp dir only)
    try:
        with tempfile.TemporaryDirectory() as td:
            blocked = h.evaluate_forward(Path("/nonexistent_tracka_resume"), Path(td), pre_reg_path=None)
        checks["prereg_block"] = {"pass": blocked.get("status") == "BLOCKED", "status": blocked.get("status")}
    except Exception as e:
        checks["prereg_block"] = {"pass": False, "error": repr(e)}
    dt = time.time() - t0
    all_pass = all(v.get("pass") is True for v in checks.values())
    return {
        "script": "tracka_resume_check",
        "pass": all_pass,
        "elapsed_s": round(dt, 6),
        "checks": checks,
        "network": False,
        "writes_real_research_state": False,
    }


if __name__ == "__main__":
    out = run()
    print(json.dumps(out, indent=2, sort_keys=True))
    sys.exit(0 if out["pass"] else 1)
