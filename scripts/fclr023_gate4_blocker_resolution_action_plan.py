#!/usr/bin/env python3
"""FCLR-NEXT-145 / FCLR-023: deterministic read-only Gate 4 blocker-resolution
action plan consuming FCLR-022 evidence preflight output.

For each FCLR-022 resolution_readiness_row (grouped by (window, gate_class,
prerequisite)) it emits a machine-checkable action-plan packet copying the
evidence snapshot fields plus human/prereg requirements and read-only local
verification commands. Missing stays missing — never fabricates resolution,
never marks an artifact present, never creates the hinted artifact, never
computes outcomes, never touches the network, never freezes/promotes/seals.
Planning/draft evidence only.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_FCLR022 = (
    REPO
    / "research_state"
    / "fclr022_local_audit"
    / "fclr022_gate4_blocker_resolution_evidence_preflight_latest.json"
)
DEFAULT_OUT = REPO / "research_state" / "fclr023_local_audit"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO))
    except Exception:
        return str(path)

TERMS_LEGAL_GATE_CLASSES = {"terms_legal_evidence_resolution"}
PREREG_GATE_CLASSES = {"fresh_frozen_prereg_before_outcomes"}

READ_ONLY_COMMAND_SKELETONS = [
    "python scripts/check_tracka_scope_registry_drift.py",
    "python scripts/tracka_resume_check.py",
    "python -m unittest discover tests -q",
    "git status --short",
    "git diff -- research_state/fclr023_local_audit scripts/fclr023_gate4_blocker_resolution_action_plan.py tests/test_fclr023_gate4_blocker_resolution_action_plan.py",
]


def read_json(path: Path):
    if not path.exists():
        return None, "missing", f"missing:{rel(path)}"
    try:
        txt = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return None, "read_error", f"read_error:{rel(path)}:{e}"
    if txt.startswith("version https://git-lfs.github.com/spec/v1"):
        return None, "unavailable_pointer", f"lfs_pointer_unavailable:{rel(path)}"
    try:
        return json.loads(txt), "ok", None
    except Exception as e:
        return None, "parse_error", f"parse_error:{rel(path)}:{e}"


def snapshot_row(row: dict) -> dict:
    return {
        "window": row.get("window"),
        "prerequisite": row.get("prerequisite"),
        "current_state": row.get("current_state"),
        "gate_class": row.get("gate_class"),
        "evidence_ref": row.get("evidence_ref"),
        "evidence_present": bool(row.get("evidence_present")),
        "read_state": row.get("read_state"),
        "sha256": row.get("sha256"),
        "bytes": row.get("bytes"),
        "reason_copied_from_index": row.get("reason_copied_from_index"),
        "missing_action_class": row.get("missing_action_class"),
        "resolution_ready": bool(row.get("resolution_ready")),
    }


def action_packet(window, gate_class, prerequisite, row) -> dict:
    snap = snapshot_row(row)
    human_legal_required = gate_class in TERMS_LEGAL_GATE_CLASSES
    fresh_frozen_prereg_required = gate_class in PREREG_GATE_CLASSES
    commands = list(READ_ONLY_COMMAND_SKELETONS)
    return {
        "window": window,
        "gate_class": gate_class,
        "prerequisite": prerequisite,
        "evidence_snapshot": snap,
        "current_state": row.get("current_state"),
        "missing_action_class": row.get("missing_action_class"),
        "reason_copied_from_index": row.get("reason_copied_from_index"),
        "human_legal_required": bool(human_legal_required),
        "fresh_frozen_prereg_required": bool(fresh_frozen_prereg_required),
        "local_verification_commands": commands,
        "artifact_target_hint": (
            "research_state/fclr023_local_audit/fclr023_gate4_blocker_resolution_action_plan_<UTC>.json "
            "(planning packet only; the hinted artifact is not created or marked present by this script)"
        ),
        "packet_ready_for_human_or_prereg_action": False,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fclr022", default=str(DEFAULT_FCLR022))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    src, state, err = read_json(Path(args.fclr022))
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    packets = []
    warnings = []
    if src is None:
        warnings.append({"type": "input_unavailable", "detail": err})
    else:
        rows = src.get("resolution_readiness_rows") or []
        groups = {}
        order = []
        for r in rows:
            key = (r.get("window"), r.get("gate_class"), r.get("prerequisite"))
            if key not in groups:
                groups[key] = []
                order.append(key)
            groups[key].append(r)
        for key in order:
            window, gate_class, prerequisite = key
            group_rows = groups[key]
            group_packets = [
                action_packet(window, gate_class, prerequisite, r) for r in group_rows
            ]
            packets.append(
                {
                    "window": window,
                    "gate_class": gate_class,
                    "prerequisite": prerequisite,
                    "group_packet_count": len(group_packets),
                    "packets": group_packets,
                    "group_all_packet_ready_false": all(
                        not p["packet_ready_for_human_or_prereg_action"] for p in group_packets
                    ),
                    "group_ready_for_action": False,
                }
            )
            for r in group_rows:
                if not bool(r.get("evidence_present")):
                    warnings.append(
                        {
                            "type": "action_plan_warning",
                            "window": window,
                            "prerequisite": prerequisite,
                            "gate_class": gate_class,
                            "detail": f"no local resolution evidence (read_state={r.get('read_state')}); human/prereg action required per packet",
                        }
                    )

    payload = {
        "script": "fclr023_gate4_blocker_resolution_action_plan.py",
        "generated_at_utc": ts,
        "input": rel(Path(args.fclr022)),
        "input_state": state,
        "row_count": len(packets) and sum(p["group_packet_count"] for p in packets) or 0,
        "group_count": len(packets),
        "action_plan_packets": packets,
        "action_plan_warnings": warnings,
        "draft_only": True,
        "no_confirmatory_outcomes": True,
        "exploratory_only": True,
        "no_network": True,
        "not_go_for_confirmatory_outcomes": True,
        "confirmatory_ready_now": False,
        "confirmatory_outcomes_go": False,
        "authorizes_confirmatory_outcomes": False,
        "satisfied": False,
        "satisfaction_inferred": False,
        "packet_ready_for_human_or_prereg_action": False,
    }

    stamp = ts
    json_path = out_dir / f"fclr023_gate4_blocker_resolution_action_plan_{stamp}.json"
    md_path = out_dir / f"fclr023_gate4_blocker_resolution_action_plan_{stamp}.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = [
        "# FCLR-023 Gate 4 blocker-resolution action plan",
        f"generated_at_utc: {ts}",
        f"input: {payload['input']} (state={state})",
        f"groups={len(packets)} packets={payload['row_count']} warnings={len(warnings)}",
        "",
        "All packets: packet_ready_for_human_or_prereg_action=false; draft_only; no confirmatory outcomes; no network.",
        "",
    ]
    for g in packets:
        lines.append(
            f"## group window={g['window']} gate_class={g['gate_class']} prerequisite={g['prerequisite']}"
        )
        for p in g["packets"]:
            lines.append(
                f"- prerequisite={p['prerequisite']} missing_action_class={p['missing_action_class']} "
                f"evidence_present={p['evidence_snapshot']['evidence_present']} "
                f"read_state={p['evidence_snapshot']['read_state']} "
                f"human_legal_required={p['human_legal_required']} "
                f"fresh_frozen_prereg_required={p['fresh_frozen_prereg_required']} "
                f"packet_ready={p['packet_ready_for_human_or_prereg_action']}"
            )
        lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    (out_dir / "fclr023_gate4_blocker_resolution_action_plan_latest.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    (out_dir / "fclr023_gate4_blocker_resolution_action_plan_latest.md").write_text(
        md_path.read_text(), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "group_count": len(packets),
                "packet_count": payload["row_count"],
                "warnings": len(warnings),
                "out": rel(json_path),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
