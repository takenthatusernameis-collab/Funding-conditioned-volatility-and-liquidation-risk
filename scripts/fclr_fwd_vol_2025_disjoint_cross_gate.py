#!/usr/bin/env python3
"""Definition-of-done gate for FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z.

This gate is fail-closed. It passes only when the frozen exploratory prereg,
coverage audit, executor, hash-matched panel, build report, and a full evaluation
summary all exist and agree that the campaign is exploratory-only. It performs
no network access and no outcome computation; it only inspects files.

Usage:
  python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py
  python3 scripts/fclr_fwd_vol_2025_disjoint_cross_gate.py --json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"

PREREG_GLOB = "prereg_fclr_fwd_vol_2025_disjoint_cross_*.json"
COVERAGE_GLOB = "coverage_audit_fwd_vol_2025_disjoint_cross_*.json"
PANEL_GLOB = "tracka_fwd_vol_2025_disjoint_cross_panel_*.parquet"
REPORT_GLOB = "tracka_fwd_vol_2025_disjoint_cross_build_report_*.json"
EVAL_GLOB = "evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-*.json"
EXECUTOR = REPO / "scripts" / "fclr_fwd_vol_2025_disjoint_cross.py"

ALLOWED_VERDICTS = {"EXPLORATORY_SIGNAL", "EXPLORATORY_NULL", "INCONCLUSIVE"}
EXPECTED_PREREG_ID = "FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z"


def _latest(pattern: str) -> Path | None:
    hits = sorted(RS.glob(pattern))
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


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run_gate() -> list[dict]:
    checks: list[dict] = []

    prereg_path = _latest(PREREG_GLOB)
    prereg = _read_json(prereg_path)
    checks.append(_check("prereg_exists", prereg is not None,
                         prereg_path.name if prereg_path else "no prereg"))
    if prereg:
        checks.append(_check("prereg_frozen",
                             prereg.get("status") == "FROZEN_PRE_OUTCOMES"
                             and prereg.get("frozen_before_outcomes") is True
                             and prereg.get("outcome_data_inspected_before_freeze") is False,
                             f"status={prereg.get('status')}, frozen={prereg.get('frozen_before_outcomes')}"))
        checks.append(_check("prereg_exploratory_only",
                             prereg.get("status_rule", {}).get("promotable") is False
                             and prereg.get("status_rule", {}).get("max_status") == "EXPLORATORY_ONLY"
                             and prereg.get("gate4_status", {}).get("promotable") is False,
                             f"promotable={prereg.get('status_rule', {}).get('promotable')}, "
                             f"max_status={prereg.get('status_rule', {}).get('max_status')}"))
        checks.append(_check("prereg_id_matches", prereg.get("experiment_id") == EXPECTED_PREREG_ID,
                             f"experiment_id={prereg.get('experiment_id')}"))

    cov_path = _latest(COVERAGE_GLOB)
    cov = _read_json(cov_path)
    checks.append(_check("coverage_exists", cov is not None,
                         cov_path.name if cov_path else "no coverage audit"))
    if cov:
        checks.append(_check("coverage_feasible",
                             cov.get("feasible") is True and cov.get("no_outcomes_computed") is True
                             and all((cov.get("checks") or {}).values()),
                             f"feasible={cov.get('feasible')}, checks={cov.get('checks')}"))
        checks.append(_check("coverage_shape",
                             cov.get("n_symbols") == 5
                             and len(cov.get("blocks") or []) >= 3
                             and all(b.get("rows", 0) >= 100 for b in (cov.get("per_block") or [])),
                             f"n_symbols={cov.get('n_symbols')}, blocks={len(cov.get('blocks') or [])}"))

    checks.append(_check("executor_exists", EXECUTOR.exists(), str(EXECUTOR)))

    panel = _latest(PANEL_GLOB)
    checks.append(_check("panel_exists", panel is not None and panel.stat().st_size > 0,
                         panel.name if panel else "no panel"))

    report_path = _latest(REPORT_GLOB)
    report = _read_json(report_path)
    checks.append(_check("build_report_exists", report is not None,
                         report_path.name if report_path else "no build report"))
    if report and panel:
        recorded = report.get("panel_sha256") or (report.get("panel") or {}).get("panel_sha256")
        actual = _sha256(panel)
        checks.append(_check("panel_hash_matches", recorded == actual,
                             f"recorded={str(recorded)[:16]} actual={actual[:16]}"))
    elif report:
        checks.append(_check("panel_hash_matches", False, "panel missing"))

    ev_path = _latest(EVAL_GLOB)
    ev = _read_json(ev_path)
    checks.append(_check("evaluation_exists", ev is not None,
                         ev_path.name if ev_path else "no evaluation summary"))
    if ev:
        verdict = ev.get("verdict")
        checks.append(_check("verdict_exploratory", verdict in ALLOWED_VERDICTS,
                             f"verdict={verdict}"))
        checks.append(_check("evaluation_exploratory_only",
                             ev.get("promotable") is False
                             and (ev.get("max_status") == "EXPLORATORY_ONLY"
                                  or ev.get("status_rule", {}).get("max_status") == "EXPLORATORY_ONLY")
                             and verdict != "CONFIRMED",
                             f"promotable={ev.get('promotable')}, max_status={ev.get('max_status')}"))
        checks.append(_check("evaluation_checks_present",
                             isinstance(ev.get("checks"), dict) and bool(ev.get("checks")),
                             f"{len(ev.get('checks') or {})} checks"))
        checks.append(_check("evaluation_shape",
                             ev.get("n_symbols", 0) >= 5
                             and ev.get("n_blocks", 0) >= 3,
                             f"n_symbols={ev.get('n_symbols')}, n_blocks={ev.get('n_blocks')}"))
        if prereg:
            checks.append(_check("evaluation_experiment_id",
                                 ev.get("experiment_id") == prereg.get("experiment_id"),
                                 f"eval={ev.get('experiment_id')}"))
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