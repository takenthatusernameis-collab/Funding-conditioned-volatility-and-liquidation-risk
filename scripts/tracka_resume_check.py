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

from scripts.tracka_rubric import assess_candidate
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


def run() -> dict:
    t0 = time.time()
    checks = {}
    # 1) rubric
    r_go = assess_candidate(_valid_go())
    checks["rubric_go"] = {"pass": r_go["go"] is True and r_go["verdict"] == "GO", "failures": r_go["failures"]}
    r_no = assess_candidate({})
    checks["rubric_fail_closed"] = {"pass": r_no["go"] is False and len(r_no["failures"]) >= 3, "n_failures": len(r_no["failures"])}
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
