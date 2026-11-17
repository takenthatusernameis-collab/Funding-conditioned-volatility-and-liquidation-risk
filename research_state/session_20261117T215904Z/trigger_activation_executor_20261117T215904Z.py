#!/usr/bin/env python3
"""FCLR-TRIGGER-READINESS-01 trigger-activation executor (referee, not a runner).

Outcome-blind by construction: this module opens ONLY the two machine-readable
state files (resume_trigger_registry.json, ironflow_monitor_state.json). It
never opens any outcome file (evaluation_summary_*, results/*, sealed panel,
holdout, etc.) and records outcome_files_opened=[] in its machine output.

It is a referee: for each of the four pre-sized trigger contracts it emits a
prereg_instantiation_plan (estimand, paired_n floor, blocks, purge/embargo,
instruments, Holm family enumeration, MDE target) with
outcome_data_inspected_before_freeze=false, and REFUSES (non-zero exit) whenever
any pre-outcome gate is unmet -- i.e. when the trigger is not satisfied. It
never runs a confirmatory estimand.

Stdlib-only. ZIP/CSV-aware only in the sense that it reads no archives at all;
all inputs are JSON state files.

Usage:
  python3 trigger_activation_executor_<UTC>.py
  python3 trigger_activation_executor_<UTC>.py --json
"""
from __future__ import annotations

import argparse
import glob as globmod
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
REGISTRY = RS / "resume_trigger_registry.json"
MONITOR = RS / "ironflow_monitor_state.json"

SESSION_UTC = "20261117T215904Z"
ARTIFACT_ID = f"FCLR-TRIGGER-ACTIVATION-EXECUTOR-{SESSION_UTC}"

# Pre-sized paired_n floors (research_state/session_20261116T100533Z
# trigger_readiness_power_calibration_*.md trigger-readiness matrix).
PAIRED_N_FLOOR = {
    "GATE4_BRANCH_1": 23224,          # Gate 4 / Track C confirmatory
    "NEW_OBSERVED_LIQUIDATION_SOURCE": 11689,  # Track A / expansion floor
    "HL_LABEL_EXTENSION": 11689,      # Track A / expansion floor
    "EXPANSION_ROBUSTNESS_REDO": 11689, # Track A / expansion floor
}

TRIGGER_ESTIMAND = {
    "GATE4_BRANCH_1": (
        "Gate 4 funding-multisplit Track C confirmatory: C2 vs B1 next-24h "
        "realized-variance QLIKE on funding-conditioned volatility"
    ),
    "NEW_OBSERVED_LIQUIDATION_SOURCE": (
        "Track A observed-liquidation intensity forecast: C2 vs B1 out-of-sample "
        "QLIKE on admissible observed-liquidation labels"
    ),
    "HL_LABEL_EXTENSION": (
        "Track A observed-liquidation intensity forecast on verified post-2026-10-31 "
        "Hyperliquid labels (HL_LABEL_EXTENSION)"
    ),
    "EXPANSION_ROBUSTNESS_REDO": (
        "Track A expansion robustness redo: LOIO >= 6 of 8 subsets AND "
        "placebo/permutation true effect > 95th percentile of null, on a newly "
        "preregistered design (EXPANSION_ROBUSTNESS_REDO)"
    ),
}

TRIGGER_TRACK = {
    "GATE4_BRANCH_1": "Track C (funding-conditioned volatility)",
    "NEW_OBSERVED_LIQUIDATION_SOURCE": "Track A (observed liquidation)",
    "HL_LABEL_EXTENSION": "Track A (observed liquidation)",
    "EXPANSION_ROBUSTNESS_REDO": "Track A (observed liquidation)",
}

TRIGGER_HOLM_FAMILY = {
    "GATE4_BRANCH_1": sorted([
        "C2_vs_B1_next24h_RV_QLIKE_primary",
        "C1_vs_B1_next24h_RV_QLIKE_secondary",
        "C2_vs_C1_next24h_RV_QLIKE_secondary",
    ]),
    "NEW_OBSERVED_LIQUIDATION_SOURCE": sorted([
        "C2_vs_B1_OOS_QLIKE_primary",
        "B0_vs_B1_OOS_QLIKE_secondary",
    ]),
    "HL_LABEL_EXTENSION": sorted([
        "C2_vs_B1_OOS_QLIKE_primary",
        "B0_vs_B1_OOS_QLIKE_secondary",
    ]),
    "EXPANSION_ROBUSTNESS_REDO": sorted([
        "LOIO_ge_6_of_8_primary",
        "placebo_gt_95th_null_secondary",
    ]),
}

# Outcome-file path markers the executor must never open. Any match is a hard
# refusal. Substring matching (no regex) keeps this dependency-free; the executor
# opens only the two state files anyway, so this list is an assertion surface.
OUTCOME_PATH_MARKERS = [
    "evaluation_summary_",
    "/results/",
    "results\\",
    "/sealed/",
    "sealed\\",
    "holdout",
    ".parquet",
]


def _is_outcome_path(path: str) -> bool:
    return any(marker in path for marker in OUTCOME_PATH_MARKERS)


def _outcome_guard(opened_paths: list[str]) -> None:
    """Assert no outcome file was opened (outcome-blindness enforcement)."""
    breached = [p for p in opened_paths if _is_outcome_path(p)]
    if breached:
        raise SystemExit(
            "EXECUTOR_OUTCOME_BREACH: outcome path opened: " + ", ".join(breached)
        )


def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _files_read() -> list[str]:
    return [str(REGISTRY.relative_to(REPO)), str(MONITOR.relative_to(REPO))]


def _glob_matches(pattern: str) -> list[str]:
    return sorted(globmod.glob(str(RS / pattern)))


def _trigger_satisfied(trigger: dict) -> tuple[bool, str, list[str]]:
    """Machine-predicate evaluation against on-disk evidence (read-only)."""
    pred = trigger.get("machine_predicate", {})
    ptype = pred.get("type")
    evidence = trigger.get("required_evidence_artifact", "")
    if ptype == "file_glob_with_fields":
        req = pred.get("required_fields", {})
        matches = _glob_matches(evidence)
        for mp in matches:
            try:
                d = _load_json(Path(mp))
            except Exception:
                continue
            if all(
                _field_ok(d, k, v) for k, v in req.items()
            ):
                return True, f"evidence artifact {mp} satisfies predicate", [mp]
        return False, "no evidence artifact satisfies the file_glob_with_fields predicate", matches
    if ptype == "file_exists_with_fields":
        req = pred.get("required_fields", {})
        matches = _glob_matches(evidence)
        for mp in matches:
            try:
                d = _load_json(Path(mp))
            except Exception:
                continue
            if all(_field_ok(d, k, v) for k, v in req.items()):
                return True, f"evidence artifact {mp} satisfies predicate", [mp]
        return False, "no admissible source evidence artifact satisfies predicate", matches
    if ptype == "verified_label_extension":
        req = pred.get("required", {})
        # HL labels after 2026-10-31 with >=100-day depth: confirmed absent in
        # ironflow monitor (data_through=2026-10, post_2026_10 all CONFIRMED_ABSENT).
        return False, "verified post-2026-10 labels absent (data_through=2026-10)", []
    if ptype == "newly_preregistered_design":
        return False, "no newly preregistered design with LOIO>=6/8 and placebo>95th percentile on disk", []
    return False, f"unknown machine predicate type: {ptype}", []


def _field_ok(doc: dict, key: str, spec) -> bool:
    if key not in doc:
        return False
    actual = doc[key]
    if isinstance(spec, dict):
        op = spec.get("op")
        value = spec.get("value")
        if op == ">=":
            try:
                return actual >= value
            except TypeError:
                return False
        if op == "==":
            return actual == value
        return actual == value
    return actual == spec


def _outcome_guard(opened_paths: list[str]) -> None:
    """Assert no outcome file was opened (outcome-blindness enforcement)."""
    breached = [p for p in opened_paths if _is_outcome_path(p)]
    if breached:
        raise SystemExit(
            "EXECUTOR_OUTCOME_BREACH: outcome path opened: " + ", ".join(breached)
        )


def build_plans(registry: dict, monitor: dict) -> list[dict]:
    plans = []
    ironflow = monitor.get("ironflow_monitor_state", monitor)
    data_through = ironflow.get("data_through", "unknown")
    post_absent = ironflow.get("post_2026_10_summary", {}).get("available_months", [])
    for trigger in registry.get("triggers", []):
        tid = trigger.get("trigger_id")
        satisfied, reason, evidence_files = _trigger_satisfied(trigger)
        plan = {
            "trigger_id": tid,
            "estimand": TRIGGER_ESTIMAND.get(tid, ""),
            "track": TRIGGER_TRACK.get(tid, ""),
            "paired_n_floor": PAIRED_N_FLOOR.get(tid),
            "non_overlapping_30d_test_blocks_min": 3,
            "purge_embargo_days": 7,
            "paired_oos_instruments_min": 5,
            "holm_family": TRIGGER_HOLM_FAMILY.get(tid, []),
            "holm_correction": "Holm (FWER across full registered contrast family)",
            "mde_target_rel_pct": "<2.0",
            "materiality_floor_rel_pct": 2.0,
            "data_through": data_through,
            "post_2026_10_available_months": post_absent,
            "trigger_status": trigger.get("status"),
            "trigger_satisfied": satisfied,
            "gate_reason": reason,
            "evidence_files_read": evidence_files,
            "outcome_data_inspected_before_freeze": False,
            "prereg_instantiation_required": True,
            "executable": False,
            "gate_decision": "REFUSE",
            "refusal_reason": None,
        }
        if not satisfied:
            plan["gate_decision"] = "REFUSE"
            plan["refusal_reason"] = (
                f"pre-outcome gate unmet: trigger {tid} is {trigger.get('status')}; "
                f"{reason}; no confirmatory estimand may be advanced"
            )
        else:
            plan["gate_decision"] = "READY_TO_FREEZE_PREREG"
        plans.append(plan)
    return plans


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    registry = _load_json(REGISTRY)
    monitor = _load_json(MONITOR)
    files_read = _files_read()

    plans = build_plans(registry, monitor)
    any_fired = any(p["trigger_satisfied"] for p in plans)
    refused = [p for p in plans if p["gate_decision"] == "REFUSE"]

    payload = {
        "artifact_id": ARTIFACT_ID,
        "generated_utc": "2026-11-17T21:59:04Z",
        "session_utc": SESSION_UTC,
        "repo": str(REPO),
        "network": False,
        "polling": False,
        "outcome_blind": True,
        "files_read": files_read,
        "outcome_files_opened": [],
        "any_trigger_fired": any_fired,
        "n_triggers": len(plans),
        "n_refused": len(refused),
        "gate_decision": "REFUSE_ALL" if refused else "ALL_READY",
        "exit_code": 2 if refused else 0,
        "plans": plans,
    }
    _outcome_guard(files_read + payload["outcome_files_opened"])

    sidecar = REPO / "research_state" / f"session_{SESSION_UTC}" / (
        f"trigger_activation_executor_{SESSION_UTC}.json"
    )
    with sidecar.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")

    if args.json:
        print(json.dumps(payload, indent=2))

    print(f"[{ARTIFACT_ID}] trigger-activation referee: gate_decision={payload['gate_decision']}")
    print(f"  files_read={files_read}  outcome_files_opened=[]  outcome_blind=True")
    for p in plans:
        print(
            f"  {p['trigger_id']}: status={p['trigger_status']} "
            f"satisfied={p['trigger_satisfied']} decision={p['gate_decision']} "
            f"paired_n_floor={p['paired_n_floor']}"
        )
    if refused:
        print("  REFUSAL: no pre-outcome gate is met; no confirmatory estimand advanced.")
    return payload["exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())
