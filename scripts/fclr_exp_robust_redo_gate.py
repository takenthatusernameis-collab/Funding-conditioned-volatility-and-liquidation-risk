#!/usr/bin/env python3
"""Completion gate for FCLR-EXP-ROBUST-REDO (Track A expansion robustness, P2).

This is the cell's completion contract. It performs no network access and no
outcome computation; it only inspects the persisted artifacts. The gate FAILS
until a final terminal verdict (ROBUST / FRAGILE / INCONCLUSIVE) is recorded
together with the complete pre-registered check set, a panel whose hash matches
the frozen prereg, and a frozen prereg. SMOKE is not final.

Usage:
  python3 scripts/fclr_exp_robust_redo_gate.py
  python3 scripts/fclr_exp_robust_redo_gate.py --json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
PREREG_GLOB = "prereg_fclr_exp_robust_redo_*.json"
EVAL_GLOB = "evaluation_summary_FCLR-EXP-ROBUST-REDO-*.json"
EXPECTED_PANEL_SHA = "39916a72dfc37d15b6cc886d4e43ed878e0b8e1c2f22936fc4ebf8edd366f699"
REQUIRED_CHECKS = [
    "loio_ge_6_of_8",
    "placebo_pass",
    "materiality_ge_2pct",
    "ci_excludes_zero",
    "bootstrap_settings_pass",
]
FINAL_VERDICTS = {"ROBUST", "FRAGILE", "INCONCLUSIVE"}


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _latest(glob: str) -> Path | None:
    hits = sorted(RS.glob(glob))
    return hits[-1] if hits else None


def _read_json(p: Path | None) -> dict | None:
    if p is None or not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def check(name: str, ok: bool, detail: str) -> dict:
    return {"check": name, "ok": bool(ok), "detail": detail}


def run_gate() -> list[dict]:
    checks = []

    pre = _read_json(_latest(PREREG_GLOB))
    checks.append(check(
        "prereg_frozen", bool(pre and pre.get("status") == "FROZEN_PRE_OUTCOMES"
                              and pre.get("outcome_data_inspected_before_freeze") is False),
        "frozen pre-outcomes prereg present" if pre else "missing prereg"))

    panel = RS / "tracka_hl_expansion_panel_20261111T202344Z.parquet"
    checks.append(check("panel_exists", panel.exists() and panel.stat().st_size > 0,
                        panel.name if panel.exists() else "missing panel parquet"))

    actual_sha = sha256_file(panel) if panel.exists() else None
    checks.append(check("panel_hash_matches_prereg",
                        actual_sha == EXPECTED_PANEL_SHA,
                        f"sha256 {actual_sha[:16] if actual_sha else None}... matches prereg"
                        if actual_sha == EXPECTED_PANEL_SHA else f"mismatch: {actual_sha}"))

    ev = _read_json(_latest(EVAL_GLOB))
    verdict = ev.get("verdict") if ev else None
    checks.append(check("eval_exists", bool(ev and verdict),
                        f"verdict={verdict}" if ev else "missing evaluation json"))

    missing = [c for c in REQUIRED_CHECKS if not (ev and c in ev.get("checks", {}))]
    checks.append(check("eval_checks_complete", not missing,
                        "all 5 pre-registered checks present" if not missing else f"missing {missing}"))

    checks.append(check("final_verdict_recorded", verdict in FINAL_VERDICTS,
                        f"verdict={verdict} (SMOKE not final)" if verdict else "no verdict"))

    return checks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    checks = run_gate()
    ok = all(c["ok"] for c in checks)
    if args.json:
        print(json.dumps({"ok": ok, "checks": checks}, indent=1))
    else:
        for c in checks:
            print(f"[{'PASS' if c['ok'] else 'FAIL'}] {c['check']}: {c['detail']}")
        print("GATE:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())