#!/usr/bin/env python3
"""Machine-checkable completion gate for FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z.

Purpose
-------
The campaign is heavy by design. This gate is the *definition of done*: it turns "I did some
analysis" into a small set of objective, file-level checks so a future session cannot declare
progress without producing the required evidence, and cannot quietly skip a phase.

It performs no network access and no outcome computation. It only inspects files.

Checks (Arm A, P1 primary)
--------------------------
  A0  bulk cache objects for 2025-05..2026-04 verify (sha256 sidecar + schema) for
      candles_1h, funding, open_interest
  A1  frozen prereg exists and is marked frozen-before-outcomes
  A2  panel parquet exists
  A3  build report exists and its recorded panel sha256 matches the panel on disk
  A4  evaluation summary JSON exists with a recognised verdict
  A5  the primary contrast C2_vs_B1 is present
  A6  all 12 declared primary-family cells are present (4 horizons x 3 contrasts)

Checks (Arm B, P2 exploratory)
-----------------------------
  B1  frozen prereg exists and is marked frozen-before-outcomes
  B2  panel parquet exists
  B3  build report exists and its recorded panel sha256 matches the panel on disk
  B4  evaluation summary JSON exists with a recognised verdict

Checks (Arm F, forward — the "heavy work cannot be avoided" arm)
---------------------------------------------------------------
  F0  the four forward bulk months (2026-01..2026-04) are present on disk
  F1  a frozen forward prereg exists (prereg_tracka_liq_xsec_forward_*.json)
  F3  forward panel parquet + build report exist and the recorded sha256 matches
  F4  forward evaluation summary JSON exists with a recognised verdict

Arm F is the point of `--arm all`. Without it, `--arm all` is green on the two
already-consumed cells alone, so a session can report "gate passed" while the only
remaining unopened window (2026-01-18..2026-04-30) is still unread. Arm F fails
closed until that window has actually been built and evaluated. It reads metadata
only (filename stems + prereg/report/eval JSON); it never opens the reserved
parquet bodies and never computes an outcome, so it cannot leak the forward window.

Usage
-----
  python3 scripts/fclr_campaign_gate.py --arm a      # Arm A only
  python3 scripts/fclr_campaign_gate.py --arm f      # forward readiness only
  python3 scripts/fclr_campaign_gate.py --arm all    # A + B + F (definition of done)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"

ARM_A_PREREG_GLOB = "prereg_tracka_vol_fullhist_*.json"
ARM_B_PREREG_GLOB = "prereg_tracka_liq_xsec_*.json"
ARM_A_EVAL_GLOB = "evaluation_summary_TRACKA-VOL-FULLHIST-*.json"
ARM_B_EVAL_GLOB = "evaluation_summary_TRACKA-LIQ-XSEC-*.json"

# Arm F: the untouched, on-disk ironflow Hyperliquid forward region. This arm is the
# "heavy work cannot be avoided" check. Without it, `--arm all` is green on the two
# already-consumed cells alone and a session can report done while the only remaining
# unopened window is still unread. Arm F therefore fails closed until Phase 1-4 of the
# forward campaign have produced a frozen prereg, a hash-matched panel, a build report,
# and a recognised verdict for 2026-01-18..2026-04-30. It reads metadata only: it never
# opens the reserved parquet files and never computes an outcome, so it cannot leak.
ARM_F_PREREG_GLOB = "prereg_tracka_liq_xsec_forward_*.json"
ARM_F_PANEL_GLOB = "tracka_liq_xsec_forward_panel_*.parquet"
ARM_F_REPORT_GLOB = "tracka_liq_xsec_forward_panel_build_report_*.json"
ARM_F_EVAL_GLOB = "evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-*.json"
# Vol-forward cell on the same reserved forward window (P1). Additive to F0-F4;
# never weakens them. Requires the frozen vol-forward prereg and a recognised
# eval verdict (INADMISSIBLE is a recognised bounded NO_GO verdict).
ARM_F_VOL_PREREG_GLOB = "prereg_tracka_vol_forward_*.json"
ARM_F_VOL_EVAL_GLOB = "evaluation_summary_TRACKA-VOL-FORWARD-*.json"

BULK_DATASETS = ("candles_1h", "funding", "open_interest")

# Must stay in lockstep with DATASETS in scripts/fclr_ironflow_bulk.py; used by the
# fixture writer so tests build schema-valid objects without importing pyarrow here.
BULK_REQUIRED_COLUMNS = {
    "candles_1h": ("timestamp", "market", "close"),
    "funding": ("timestamp", "market", "funding_rate"),
    "open_interest": ("timestamp", "market", "open_interest_usd"),
}
BULK_MONTHS = (
    "2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10",
    "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
)

HORIZONS = ("6h", "24h", "72h", "168h")
CONTRASTS = ("C2_vs_B1", "C1_vs_B1", "C2_vs_C1")

VALID_VERDICTS = {
    "NOT_MET", "INCONCLUSIVE", "FORECAST_GATE_PASSED", "PROMOTE_CANDIDATE",
    "EXPLORATORY_SIGNAL", "EXPLORATORY_NULL", "INADMISSIBLE",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _rs(root: Path) -> Path:
    """Research-state directory: <root>/research_state when it exists, else <root>."""
    candidate = root / "research_state"
    return candidate if candidate.is_dir() else root


def _latest(stem_glob: str, root: Path) -> Optional[Path]:
    cands = sorted(_rs(root).glob(stem_glob))
    return cands[-1] if cands else None


def _read_json(path: Path) -> Optional[dict]:
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def _check(name: str, ok: bool, detail: str) -> Dict[str, object]:
    return {"check": name, "ok": bool(ok), "detail": detail}


# ------------------------------- Arm A ------------------------------------------
def check_bulk_cache(root: Path = REPO) -> List[Dict[str, object]]:
    import importlib.util

    script = root / "scripts" / "fclr_ironflow_bulk.py"
    if not script.exists():
        return [_check("A0", False, f"missing {script.name}")]
    spec = importlib.util.spec_from_file_location("fclr_ironflow_bulk", script)
    if not spec or not spec.loader:
        return [_check("A0", False, f"cannot load {script}")]
    bulk = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bulk)

    # A0 must be evaluated against `root`, not the real repo cache: otherwise the
    # definition-of-done gate cannot be validated hermetically and every fixture
    # run reports the live cache state instead of the candidate root.
    cache_root = _rs(root) / "data_cache" / "ironflow_bulk"

    out: List[Dict[str, object]] = []
    bad: List[str] = []
    for dataset in BULK_DATASETS:
        for month in BULK_MONTHS:
            try:
                info = bulk.verify_object(
                    dataset, month, require_exists=False, cache_root=cache_root)
            except Exception as exc:  # schema/disk failure
                bad.append(f"{dataset}/{month}: {exc}")
                continue
            if info["status"] != "OK":
                bad.append(f"{dataset}/{month}: {info['status']}")
    out.append(_check("A0", not bad, "all bulk objects verify" if not bad else "; ".join(bad[:8])))
    return out


def check_prereg_frozen(root: Path, pattern: str, label: str) -> Dict[str, object]:
    p = _latest(pattern, root)
    if p is None:
        return _check(label, False, f"no prereg matching {pattern}")
    spec = _read_json(p)
    if spec is None:
        return _check(label, False, f"{p.name} is not valid JSON")
    ok = bool(spec.get("frozen_before_outcomes")) and bool(spec.get("pre_registered_before_outcomes"))
    return _check(label, ok, f"{p.name} frozen={spec.get('frozen_before_outcomes')}")


def check_panel_and_report(root: Path, panel_glob: str, report_glob: str, label: str) -> List[Dict[str, object]]:
    panel = _latest(panel_glob, root)
    report = _latest(report_glob, root)
    out: List[Dict[str, object]] = []
    if panel is None:
        out.append(_check(label + "_panel", False, f"no panel matching {panel_glob}"))
    else:
        out.append(_check(label + "_panel", True, f"{panel.name} ({panel.stat().st_size} bytes)"))
    if report is None:
        out.append(_check(label + "_report", False, f"no build report matching {report_glob}"))
        return out
    spec = _read_json(report)
    if spec is None:
        out.append(_check(label + "_report", False, f"{report.name} is not valid JSON"))
        return out
    recorded = spec.get("panel_sha256") or spec.get("panel", {}).get("panel_sha256")
    if panel is None or not recorded:
        out.append(_check(label + "_report", False, f"{report.name} lacks panel_sha256"))
        return out
    actual = sha256_file(panel)
    out.append(_check(
        label + "_report",
        actual == recorded,
        f"{report.name}: panel sha256 {'matches' if actual == recorded else 'MISMATCH'}",
    ))
    return out


def check_eval_summary(root: Path, pattern: str, label: str) -> List[Dict[str, object]]:
    p = _latest(pattern, root)
    if p is None:
        return [_check(label, False, f"no evaluation summary matching {pattern}")]
    spec = _read_json(p)
    if spec is None:
        return [_check(label, False, f"{p.name} is not valid JSON")]
    verdict = spec.get("verdict")
    checks = [_check(label, verdict in VALID_VERDICTS, f"{p.name}: verdict={verdict}")]
    if label == "A4":
        primary = spec.get("contrasts", {}).get("C2_vs_B1") or spec.get("primary_contrast_result")
        checks.append(_check("A5", isinstance(primary, dict), "primary contrast C2_vs_B1 present"
                             if isinstance(primary, dict) else "primary contrast C2_vs_B1 MISSING"))
        results = spec.get("family_results") or spec.get("per_horizon") or {}
        cells = spec.get("primary_family_cells")
        if isinstance(cells, dict):
            missing = [f"{h}/{c}" for h in HORIZONS for c in CONTRASTS if f"{h}/{c}" not in cells]
        else:
            missing = [f"{h}/{c}" for h in HORIZONS for c in CONTRASTS
                       if not isinstance(results.get(h), dict) or c not in results[h]]
        checks.append(_check("A6", not missing,
                             "all 12 primary-family cells present" if not missing
                             else f"missing {len(missing)}: {missing[:6]}"))
    return checks


def run_arm_a(root: Path = REPO) -> List[Dict[str, object]]:
    checks: List[Dict[str, object]] = []
    checks += check_bulk_cache(root)
    checks.append(check_prereg_frozen(root, ARM_A_PREREG_GLOB, "A1"))
    checks += check_panel_and_report(
        root, "tracka_vol_fullhist_panel_*.parquet",
        "tracka_vol_fullhist_panel_build_report_*.json", "A3",
    )
    checks += check_eval_summary(root, ARM_A_EVAL_GLOB, "A4")
    return checks


# ------------------------------- Arm B ------------------------------------------
def run_arm_b(root: Path = REPO) -> List[Dict[str, object]]:
    checks: List[Dict[str, object]] = []
    checks.append(check_prereg_frozen(root, ARM_B_PREREG_GLOB, "B1"))
    checks += check_panel_and_report(
        root, "tracka_liq_xsec_panel_*.parquet",
        "tracka_liq_xsec_panel_build_report_*.json", "B3",
    )
    checks += check_eval_summary(root, ARM_B_EVAL_GLOB, "B4")
    return checks


# ------------------------------- Arm F (forward) --------------------------------
def _forward_days_present(root: Path) -> List[str]:
    """Months of the on-disk forward region, without opening any parquet body.

    Presence is judged from the parquet filename stem only; no file content is read,
    so this check cannot touch or leak the reserved window's outcomes. The labels
    may live in either the bulk liquidations cache or the legacy events cache; the
    forward campaign reads the former, so that directory is the primary source.
    """
    candidates = [
        _rs(root) / "data_cache" / "ironflow_bulk" / "liquidations",
        _rs(root) / "data_cache" / "ironflow_events",
    ]
    for base in candidates:
        if base.is_dir() and any(base.glob("*.parquet")):
            return sorted({p.stem for p in base.glob("*.parquet")
                           if p.stem in ("2026-01", "2026-02", "2026-03", "2026-04")})
    return []


def run_arm_f(root: Path = REPO) -> List[Dict[str, object]]:
    """Forward-cell readiness: the unopened 2026-01-18..2026-04-30 window.

    Fail-closed until the forward campaign has produced a frozen prereg, a panel with
    a matching build report, and a recognised verdict. Metadata-only; never reads
    parquet bodies.
    """
    checks: List[Dict[str, object]] = []
    months = _forward_days_present(root)
    have = [m for m in ("2026-01", "2026-02", "2026-03", "2026-04") if m in months]
    checks.append(_check(
        "F0", len(have) == 4,
        "forward bulk months present: " + ", ".join(have) if have
        else "no forward bulk months on disk",
    ))
    checks.append(check_prereg_frozen(root, ARM_F_PREREG_GLOB, "F1"))
    checks += check_panel_and_report(root, ARM_F_PANEL_GLOB, ARM_F_REPORT_GLOB, "F3")
    checks += check_eval_summary(root, ARM_F_EVAL_GLOB, "F4")
    # Vol-forward cell (P1) on the same reserved window — additive, fail-closed.
    checks.append(check_prereg_frozen(root, ARM_F_VOL_PREREG_GLOB, "F5"))
    checks += check_eval_summary(root, ARM_F_VOL_EVAL_GLOB, "F6")
    return checks


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arm", choices=("a", "b", "f", "all"), default="all")
    ap.add_argument("--root", default=str(REPO))
    args = ap.parse_args(list(argv) if argv is not None else None)

    root = Path(args.root).resolve()
    checks: List[Dict[str, object]] = []
    if args.arm in ("a", "all"):
        checks += run_arm_a(root)
    if args.arm in ("b", "all"):
        checks += run_arm_b(root)
    if args.arm in ("f", "all"):
        checks += run_arm_f(root)

    width = max((len(str(c["check"])) for c in checks), default=4)
    for c in checks:
        print(f"{str(c['check']):<{width}}  {'PASS' if c['ok'] else 'FAIL'}  {c['detail']}")
    failed = [c["check"] for c in checks if not c["ok"]]
    print(f"\ncampaign gate: {len(checks) - len(failed)}/{len(checks)} checks passed")
    if failed:
        print("blocking: " + ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())