#!/usr/bin/env python3
"""Definition-of-done gate for FCLR-NEXT-CAMPAIGN-20261113T063000Z.

This gate is fail-closed: it FAILS until EVERY one of the three campaign cells has
a frozen prereg AND a timestamped evaluation artifact carrying a terminal verdict.
It performs no network access and no outcome computation; it only inspects
persisted artifacts. A cell is complete only when its verdict is one of the
terminal classes for that cell.

Cells:
  LIQ-010-CONFIRM     -> CONFIRMED / FRAGILE / NOT_REPLICATED / INCONCLUSIVE
  EXP-ROBUST-REDO     -> ROBUST / FRAGILE / INCONCLUSIVE
  FWD-VOL-2025-CROSS  -> CONFIRMED / NOT_REPLICATED / INCONCLUSIVE

Usage:
  python3 scripts/fclr_next_campaign_gate.py
  python3 scripts/fclr_next_campaign_gate.py --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

CELLS = [
    {
        "cell": "LIQ-010-CONFIRM",
        "prereg_glob": "prereg_fclr_liq_010_confirm_*.json",
        "eval_glob": "evaluation_summary_FCLR-LIQ-010-CONFIRM-*.json",
        "verdicts": {"CONFIRMED", "FRAGILE", "NOT_REPLICATED", "INCONCLUSIVE"},
        "script": "scripts/fclr_liq_010_confirm.py",
    },
    {
        "cell": "EXP-ROBUST-REDO",
        "prereg_glob": "prereg_fclr_exp_robust_redo_*.json",
        "eval_glob": "evaluation_summary_FCLR-EXP-ROBUST-REDO-*.json",
        "verdicts": {"ROBUST", "FRAGILE", "INCONCLUSIVE"},
        "script": "scripts/fclr_exp_robust_redo.py",
    },
    {
        "cell": "FWD-VOL-2025-CROSS",
        "prereg_glob": "prereg_fclr_fwd_vol_2025_cross_*.json",
        "eval_glob": "evaluation_summary_FCLR-FWD-VOL-2025-CROSS-*.json",
        "verdicts": {"CONFIRMED", "NOT_REPLICATED", "INCONCLUSIVE"},
        "script": "scripts/fclr_fwd_vol_2025_cross.py",
    },
]


def _rs() -> Path:
    """Resolve research_state at call time (tests monkeypatch module globals)."""
    return globals().get("RS") or (Path(__file__).resolve().parents[1] / "research_state")


def _latest(glob: str) -> Path | None:
    hits = sorted(_rs().glob(glob))
    return hits[-1] if hits else None


def _read_json(p: Path | None) -> dict | None:
    if p is None or not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def _check(name: str, ok: bool, detail: str) -> dict:
    return {"check": name, "ok": bool(ok), "detail": detail}


def run_gate() -> list[dict]:
    checks: list[dict] = []
    repo = globals().get("REPO") or (Path(__file__).resolve().parents[1])
    for spec in CELLS:
        cell = spec["cell"]
        prereg = _read_json(_latest(spec["prereg_glob"]))
        prereg_ok = bool(prereg and prereg.get("status") == "FROZEN_PRE_OUTCOMES"
                         and prereg.get("outcome_data_inspected_before_freeze") is False)
        checks.append(_check(f"{cell}:prereg_frozen", prereg_ok,
                             "frozen prereg present" if prereg_ok else "missing/invalid prereg"))

        ev = _read_json(_latest(spec["eval_glob"]))
        verdict = ev.get("verdict") if ev else None
        terminal = verdict in spec["verdicts"]
        checks.append(_check(f"{cell}:terminal_verdict", terminal,
                             f"verdict={verdict}" if ev else "missing evaluation json"))

        has_checks = bool(ev and isinstance(ev.get("checks"), dict) and ev["checks"])
        checks.append(_check(f"{cell}:checks_present", has_checks,
                             f"{len(ev['checks'])} checks" if has_checks else "no checks block"))

        script_ok = (repo / spec["script"]).exists()
        checks.append(_check(f"{cell}:script_exists", script_ok,
                             spec["script"] if script_ok else f"missing {spec['script']}"))
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