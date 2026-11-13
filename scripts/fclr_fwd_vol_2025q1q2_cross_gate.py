#!/usr/bin/env python3
"""Completion gate for FCLR-FWD-VOL-2025Q1Q2-CROSS (Track C volatility period-specificity, P1).

Fail-closed completion contract for the 2026 Q1-Q2 period cell. Performs no network
access and no outcome computation: it only inspects persisted artifacts. The gate
FAILS until a terminal verdict is recorded with the complete pre-registered check
set, the panel and its build report exist and agree on sha256, the prereg is frozen
pre-outcomes, and the prereg artifact hash matches the one recorded in the
evaluation payload.

Usage:
  python3 scripts/fclr_fwd_vol_2025q1q2_cross_gate.py
  python3 scripts/fclr_fwd_vol_2025q1q2_cross_gate.py --json
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
PREREG_GLOB = "prereg_fclr_fwd_vol_2025q1q2_cross_*.json"
EVAL_GLOB = "evaluation_summary_FCLR-FWD-VOL-2025Q1Q2-CROSS-*.json"
PANEL_GLOB = "tracka_fwd_vol_2025q1q2_cross_panel_*.parquet"
BUILD_REPORT_GLOB = "tracka_fwd_vol_2025q1q2_cross_build_report_*.json"
REQUIRED_CHECKS = [
    "materiality_ge_2pct",
    "ci_excludes_zero_improving",
    "instruments_ge_5",
    "blocks_ge_3",
    "loio_ge_4_of_5",
    "placebo_pass",
    "holm_pass",
    "leakage_audit_pass",
]
FINAL_VERDICTS = {"CONFIRMED", "FRAGILE", "NOT_REPLICATED", "INCONCLUSIVE"}


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
    pre_ok = bool(pre and pre.get("status") == "FROZEN_PRE_OUTCOMES"
                  and pre.get("outcome_data_inspected_before_freeze") is False)
    checks.append(check("prereg_frozen_pre_outcomes", pre_ok,
                        "frozen prereg present" if pre else "missing prereg"))

    panel = _latest(PANEL_GLOB)
    checks.append(check("panel_exists", panel is not None and panel.exists()
                        and panel.stat().st_size > 0, panel.name if panel else "missing panel"))

    build_report = _read_json(_latest(BUILD_REPORT_GLOB))
    checks.append(check("build_report_exists", build_report is not None,
                        "build report present" if build_report else "missing build report"))

    if panel is not None and build_report:
        actual = sha256_file(panel)
        checks.append(check("panel_hash_matches_build_report",
                            actual == build_report.get("panel_sha256"),
                            f"panel sha256 {actual[:16]} vs report {str(build_report.get('panel_sha256'))[:16]}"))
    else:
        checks.append(check("panel_hash_matches_build_report", False, "panel or report missing"))

    ev = _read_json(_latest(EVAL_GLOB))
    checks.append(check("evaluation_exists", ev is not None,
                        "evaluation artifact present" if ev else "missing evaluation"))

    if ev:
        checks.append(check("verdict_is_final", ev.get("verdict") in FINAL_VERDICTS,
                            f"verdict={ev.get('verdict')}"))
        checks.append(check("verdict_not_smoke", ev.get("verdict") != "SMOKE",
                            f"verdict={ev.get('verdict')}"))
        got = set((ev.get("checks") or {}).keys())
        missing = sorted(set(REQUIRED_CHECKS) - got)
        checks.append(check("all_checks_present", not missing,
                            "all present" if not missing else f"missing {missing}"))
        if pre is not None:
            same = ev.get("prereg_sha256") == sha256_file(_latest(PREREG_GLOB))
            checks.append(check("eval_prereg_hash_matches", bool(same),
                                "evaluation records the frozen prereg hash"))
        per_block = ev.get("per_block") or []
        checks.append(check("three_blocks_executed", len(per_block) >= 3,
                            f"{len(per_block)} block(s) recorded"))
        prim = ev.get("primary") or {}
        checks.append(check("primary_contrast_reported",
                            bool(prim) and all(k in prim for k in
                                               ("mean_diff", "ci_lo", "ci_hi", "rel_reduction_pct")),
                            "primary C2_vs_B1 stats present"))
        checks.append(check("loio_complete", len(ev.get("loio") or []) >= 5,
                            f"{len(ev.get('loio') or [])} LOIO rows"))
        checks.append(check("placebo_reported", bool(ev.get("placebo")),
                            "funding-permutation placebo present"))
    else:
        checks.append(check("verdict_is_final", False, "no evaluation artifact"))
        checks.append(check("verdict_not_smoke", False, "no evaluation artifact"))
        checks.append(check("all_checks_present", False, "no evaluation artifact"))
        checks.append(check("eval_prereg_hash_matches", False, "no evaluation artifact"))
        checks.append(check("three_blocks_executed", False, "no evaluation artifact"))
        checks.append(check("primary_contrast_reported", False, "no evaluation artifact"))
        checks.append(check("loio_complete", False, "no evaluation artifact"))
        checks.append(check("placebo_reported", False, "no evaluation artifact"))

    return checks


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    checks = run_gate()
    ok = all(c["ok"] for c in checks)
    if args.json:
        print(json.dumps({"gate": "PASS" if ok else "FAIL", "checks": checks}, indent=1))
        return
    for c in checks:
        print(f"[{'PASS' if c['ok'] else 'FAIL'}] {c['check']}: {c['detail']}")
    print(f"\nGATE: {'PASS' if ok else 'FAIL'}")


if __name__ == "__main__":
    main()
