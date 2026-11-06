#!/usr/bin/env python3
"""FCLR-NEXT-119 (G3): repo-local drift check for Track A script-scope registry.

Machine-enforced, deterministic, no network, no real research_state writes.
Fails when scripts/*.py additions/removals are not reflected in
research_state/tracka_script_scope_registry.json, or when entries are malformed.

Usage:
  python scripts/check_tracka_scope_registry_drift.py
  python scripts/check_tracka_scope_registry_drift.py --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "scripts"
REGISTRY_PATH = REPO / "research_state" / "tracka_script_scope_registry.json"

ALLOWED_CLASSES = {
    "guarded_tracka",
    "guarded_tracka_ready_writing",
    "guarded_tracka_audit_ready_writing",
    "harness_core",
    "resume_gate_infra",
    "prereg_utility",
    "raw_fetch_monitor_provenance",
    "track_b_modeled_boundary",
    "track_c_sealed_volatility",
    "track_c_or_aux_audit_utility",
    "track_c_or_aux_utility",
    "test_fixture_utility",
    "repo_maintenance_utility",
    "out_of_scope_historical_tracka_pilot",
    "unclassified_auxiliary",
}


def check_drift(repo: Path = REPO) -> dict:
    scripts_dir = repo / "scripts"
    reg_path = repo / "research_state" / "tracka_script_scope_registry.json"
    actual = sorted(p.name for p in scripts_dir.glob("*.py"))
    payload = {
        "script": "check_tracka_scope_registry_drift",
        "network": False,
        "writes_real_research_state": False,
        "read_only": True,
        "registry_path": str(reg_path.relative_to(repo)),
        "actual_script_count": len(actual),
        "pass": False,
        "failures": [],
        "missing_in_registry": [],
        "extra_in_registry": [],
        "bad_entries": [],
    }
    if not reg_path.exists():
        payload["failures"].append("REGISTRY_MISSING")
        payload["reason_code"] = "SCOPE_REGISTRY_DRIFT"
        return payload
    reg = json.loads(reg_path.read_text())
    scripts = reg.get("scripts") or {}
    reg_keys = sorted(scripts.keys())
    payload["registry_script_count"] = len(reg_keys)
    missing = [n for n in actual if n not in scripts]
    extra = [n for n in reg_keys if n not in actual]
    payload["missing_in_registry"] = missing
    payload["extra_in_registry"] = extra
    if missing:
        payload["failures"].append(f"MISSING_IN_REGISTRY:{missing}")
    if extra:
        payload["failures"].append(f"EXTRA_IN_REGISTRY:{extra}")
    allowed = set(reg.get("allowed_classes") or ALLOWED_CLASSES)
    for name, meta in scripts.items():
        if not isinstance(meta, dict):
            payload["bad_entries"].append(f"{name}:not_dict")
            continue
        cls = meta.get("class")
        reason = meta.get("reason")
        if cls not in allowed:
            payload["bad_entries"].append(f"{name}:bad_class:{cls}")
        if not isinstance(reason, str) or len(reason.strip()) < 10:
            payload["bad_entries"].append(f"{name}:bad_reason")
    if payload["bad_entries"]:
        payload["failures"].append(f"BAD_ENTRIES:{payload['bad_entries'][:12]}")
    payload["pass"] = not payload["failures"]
    payload["reason_code"] = "OK" if payload["pass"] else "SCOPE_REGISTRY_DRIFT"
    return payload


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    res = check_drift()
    if args.json:
        print(json.dumps(res, indent=2, sort_keys=True))
    else:
        status = "PASS" if res["pass"] else "FAIL"
        print(f"[{status}] scope-registry drift: scripts={res['actual_script_count']} registry={res.get('registry_script_count')} reason={res['reason_code']}")
        if res["missing_in_registry"]:
            print(" missing_in_registry:", res["missing_in_registry"])
        if res["extra_in_registry"]:
            print(" extra_in_registry:", res["extra_in_registry"])
        if res["bad_entries"]:
            print(" bad_entries:", res["bad_entries"][:12])
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
