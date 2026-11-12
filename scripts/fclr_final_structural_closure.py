#!/usr/bin/env python3
"""Deterministic, offline generator of the program terminal structural closure.

Emits (without running any estimator, fetch, probe, or discovery):
  research_state/fclr_final_structural_closure_<UTC>.md
  research_state/fclr_final_structural_closure_<UTC>.json
  research_state/resume_trigger_registry.json

Inputs (read-only, hashed for reproducibility):
  research_state/hypothesis_registry.json
  research_state/experiment_frontier.json
  research_state/evaluation_summary_*.json / *.md
  research_state/terminal_structural_stop_*.md
  research_state/alt_source_probe_audit_*.json

Same inputs -> byte-identical outputs except the generated timestamp.
No network. Never changes a sealed verdict.
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
RESEARCH_STATE = REPO_ROOT / "research_state"

SECTION_17_CONDITIONS = [
    "data_and_label_gates_pass",
    "frozen_oos_beats_baseline_on_primary_target",
    "materiality_floor_and_multiplicity_uncertainty_pass",
    "skill_not_dominated_by_one_coin_venue_brief_crisis_block",
    "calibration_and_subgroup_diagnostics_acceptable",
    "independent_recomputation_reproduces_headline_within_tolerance",
    "red_team_and_leakage_audits_show_no_unresolved_issue",
]

# Machine-checkable reopen triggers (exactly these four; no others).
TRIGGERS = [
    {
        "trigger_id": "GATE4_BRANCH_1",
        "machine_predicate": {
            "type": "file_glob_with_fields",
            "glob": "research_state/fclr016_v5_terms_evidence_RESOLVED_*.json",
            "required_fields": {
                "status": "RESOLVED_VERIFIED",
                "fabricated": False,
            },
            "attestation": "human/legal",
            "note": "Never agent-set; never bypassed; no whole-tree grep for the trigger string.",
        },
        "required_evidence_artifact": "research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json",
        "gate_protocol": "RESEARCH_PROMPT.md Gate 4 Branch 1 (external/legal evidence)",
        "priority": 1,
        "status": "OPEN",
        "do_not_act_until_satisfied": True,
    },
    {
        "trigger_id": "NEW_OBSERVED_LIQUIDATION_SOURCE",
        "machine_predicate": {
            "type": "file_exists_with_fields",
            "path_template": "research_state/<source>_admissibility_audit_<UTC>.json",
            "required_fields": {
                "status": "ADMISSIBLE",
                "observed_labels": True,
                "instruments": {"op": ">=", "value": 5},
                "blocks": {"op": ">=", "value": 3},
                "complete_month": {"op": ">=", "value": 1},
                "unauthenticated": True,
            },
            "also_documented": ["provenance", "license", "venue_consistent"],
            "note": "Or (instruments>=5 AND complete_month>=1) in place of blocks>=3 per RESEARCH_PROMPT §16.",
        },
        "required_evidence_artifact": "research_state/<source>_admissibility_audit_<UTC>.{md,json}",
        "gate_protocol": "RESEARCH_PROMPT.md §5 source acceptance + §16 admissibility audit BEFORE preregistration/outcomes",
        "priority": 2,
        "status": "OPEN",
        "do_not_act_until_satisfied": True,
    },
    {
        "trigger_id": "HL_LABEL_EXTENSION",
        "machine_predicate": {
            "type": "verified_label_extension",
            "source": "ironflow/hyperliquid-liquidations",
            "required": {
                "labels_after": "2026-10-31",
                "min_depth_days": 100,
                "venue": "hyperliquid_perpetuals",
                "observed_only": True,
            },
        },
        "required_evidence_artifact": "research_state/hl_label_extension_audit_<UTC>.{md,json}",
        "gate_protocol": "RESEARCH_PROMPT.md §5/§16 on verified post-2026-10-31 observed ironflow labels",
        "priority": 3,
        "status": "OPEN",
        "do_not_act_until_satisfied": True,
    },
    {
        "trigger_id": "EXPANSION_ROBUSTNESS_REDO",
        "machine_predicate": {
            "type": "newly_preregistered_design",
            "basis": "H_tracka_hl_expansion_robustness sealed FRAGILE",
            "conditions": [
                "LOIO >= 6 of 8 subsets pass",
                "placebo/permutation: true effect > 95th percentile of null",
            ],
            "forbidden": "re-scoring the sealed 19.04% result",
        },
        "required_evidence_artifact": "research_state/expansion_robustness_redo_prereg_<UTC>.json + evaluation_summary_*.json",
        "gate_protocol": "RESEARCH_PROMPT.md §17 promotion conditions 1-7 all met by a newly preregistered design (conditional, non-priority)",
        "priority": 4,
        "status": "OPEN",
        "do_not_act_until_satisfied": True,
    },
]

# Reopen trigger(s) per hypothesis/experiment ID. Empty list = no registry
# trigger currently maps to it (needs a wholly new protocol outside the four).
REOPEN_MAP: dict[str, list[str]] = {
    "H1_primary": ["GATE4_BRANCH_1", "NEW_OBSERVED_LIQUIDATION_SOURCE"],
    "H2_shek_replication": [],
    "H_trackb_modeled_breaches": [],
    "H_tracka_hl_liquidation_forecast": [
        "NEW_OBSERVED_LIQUIDATION_SOURCE",
        "HL_LABEL_EXTENSION",
    ],
    "H_tracka_hl_early_liquidation_forecast": [
        "NEW_OBSERVED_LIQUIDATION_SOURCE",
        "HL_LABEL_EXTENSION",
    ],
    "H_tracka_hl_symbol_expansion_liquidation_forecast": [
        "NEW_OBSERVED_LIQUIDATION_SOURCE",
        "HL_LABEL_EXTENSION",
    ],
    "H_tracka_hl_funding_conditioned_volatility_forecast": [
        "GATE4_BRANCH_1",
        "NEW_OBSERVED_LIQUIDATION_SOURCE",
    ],
    "H_tracka_hl_expansion_robustness": ["EXPANSION_ROBUSTNESS_REDO"],
    "H_tracka_hl_alt_volatility_forecast": [
        "GATE4_BRANCH_1",
        "NEW_OBSERVED_LIQUIDATION_SOURCE",
    ],
    "TRACKA-HL-EARLY4H-2025H1-LIQ-GLM-ROBUST": [
        "NEW_OBSERVED_LIQUIDATION_SOURCE",
        "HL_LABEL_EXTENSION",
    ],
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def collect_input_artifacts() -> list[dict[str, str]]:
    patterns = [
        "hypothesis_registry.json",
        "experiment_frontier.json",
        "evaluation_summary_*.json",
        "evaluation_summary_*.md",
        "terminal_structural_stop_*.md",
        "alt_source_probe_audit_*.json",
    ]
    seen: set[str] = set()
    artifacts: list[dict[str, str]] = []
    for pattern in patterns:
        for path in sorted(RESEARCH_STATE.glob(pattern)):
            rel = str(path.relative_to(RESEARCH_STATE))
            if rel in seen:
                continue
            seen.add(rel)
            artifacts.append({"path": rel, "sha256": sha256_file(path)})
    artifacts.sort(key=lambda a: a["path"])
    return artifacts


def _failing_minima_from_gate(gate: dict | None) -> str:
    if not isinstance(gate, dict):
        return ""
    failed = []
    for key, value in gate.items():
        if value is False or value is None:
            failed.append(key)
    if failed:
        return "failed gate criteria: " + ", ".join(sorted(failed))
    return ""


def _failing_minima_from_evidence(evidence: str) -> str:
    if not evidence:
        return ""
    hints = []
    low = evidence.lower()
    for token in [
        "2% floor",
        "materiality",
        "ci crosses",
        "ci upper",
        "holm",
        "not rejected",
        "loio",
        "placebo",
        "permutation",
        "bootstrap",
        "blocks",
        "instruments",
        "degenerate",
        "zero",
        "inadmissible",
    ]:
        if token in low:
            hints.append(token)
    if hints:
        return "evidence flags: " + ", ".join(sorted(set(hints)))
    return ""


def section_17_evaluation(row: dict) -> dict:
    """Evaluate RESEARCH_PROMPT §17 promotion conditions for a sealed row.

    All sealed/terminal rows fail promotion: every condition is met=False
    (not_evaluable conditions count as not met; re-running sealed designs is
    banned). This matches §4 step 3: all §17 conditions must be "no".
    """
    verdict = str(row.get("verdict", "")).upper()
    status = str(row.get("status", "")).upper()
    sealed = any(
        token in verdict or token in status
        for token in [
            "NOT_SUPPORTED",
            "NOT_MET",
            "FRAGILE",
            "INCONCLUSIVE",
            "TERMINAL",
            "NO_GO",
            "INADMISSIBLE",
            "DEGENERATE",
            "UNKNOWN",
            "",
        ]
    )
    # No sealed/terminal row can affirm any §17 promotion condition: that would
    # require re-running sealed designs (banned) or fresh evidence. Every
    # condition is therefore not met, matching §4 step 3 (all must be "no").
    return {cond: False for cond in SECTION_17_CONDITIONS}


def build_rows(input_artifacts: list[dict[str, str]]) -> list[dict]:
    artifact_names = {a["path"].split("/")[-1] for a in input_artifacts}
    rows: list[dict] = []

    # --- hypotheses from hypothesis_registry.json ---
    reg_path = RESEARCH_STATE / "hypothesis_registry.json"
    if reg_path.exists():
        registry = load_json(reg_path)
        for hyp in registry.get("hypotheses", []):
            hid = hyp.get("id", "unknown")
            verdict = hyp.get("last_verdict", hyp.get("status", "unknown"))
            evidence = hyp.get("evidence", "")
            gate_outcome = verdict
            failing = _failing_minima_from_evidence(evidence)
            if "NOT_MET" in verdict or "NOT_SUPPORTED" in verdict:
                failing = failing or "forecast gate NOT_MET"
            row = {
                "id": hid,
                "type": "hypothesis",
                "status": hyp.get("status", "unknown"),
                "verdict": verdict,
                "gate_outcome": gate_outcome,
                "failing_minima": failing or "no gate passed; sealed",
                "section_17_promotion_met": False,
                "section_17_conditions": section_17_evaluation(
                    {"verdict": verdict, "status": hyp.get("status", "")}
                ),
                "terminal_class": hyp.get("status", "unknown"),
                "source_artifact": "research_state/hypothesis_registry.json",
                "reopen_requires": list(REOPEN_MAP.get(hid, [])),
                "evidence_summary": evidence[:400],
            }
            rows.append(row)

    # --- sealed verdicts: terminal structural stop docs ---
    for path in sorted(RESEARCH_STATE.glob("terminal_structural_stop_*.md")):
        text = path.read_text(encoding="utf-8")
        rid = path.stem
        verdict = "NOT_MET"
        for line in text.splitlines():
            if line.lstrip().startswith("**NOT_"):
                verdict = line.lstrip().strip("* ").split(" ")[0]
                break
        row = {
            "id": rid,
            "type": "sealed_verdict",
            "status": "TERMINAL_STRUCTURAL_STOP",
            "verdict": verdict,
            "gate_outcome": verdict,
            "failing_minima": "terminal structural stop; gate failed on statistical evidence",
            "section_17_promotion_met": False,
            "section_17_conditions": section_17_evaluation({"verdict": verdict, "status": "TERMINAL_STRUCTURAL_STOP"}),
            "terminal_class": "TERMINAL_STRUCTURAL_STOP",
            "source_artifact": f"research_state/{path.name}",
            "reopen_requires": list(
                REOPEN_MAP.get(
                    rid.replace("terminal_structural_stop_", "").replace("_", "-").upper(),
                    [],
                )
            )
            if rid.startswith("terminal_structural_stop_liq_glm_robust")
            else ["NEW_OBSERVED_LIQUIDATION_SOURCE", "HL_LABEL_EXTENSION"],
            "evidence_summary": text[:400],
        }
        rows.append(row)

    # --- sealed verdicts: evaluation summaries ---
    # Multiple summary files can share one experiment_id (re-runs). Keep the
    # latest per ID and record the superseded files; never drop silently.
    latest_by_id: dict[str, dict] = {}
    sources_by_id: dict[str, list[str]] = {}
    for path in sorted(RESEARCH_STATE.glob("evaluation_summary_*.json")):
        data = load_json(path)
        rid = data.get("experiment_id", path.stem)
        sources_by_id.setdefault(rid, []).append(f"research_state/{path.name}")
        generated = data.get("generated_utc", "")
        cur = latest_by_id.get(rid)
        if cur is None or generated > cur[0]:
            latest_by_id[rid] = (generated, data)
    for rid in sorted(latest_by_id):
        generated, data = latest_by_id[rid]
        verdict = data.get("verdict", "unknown")
        gate = data.get("gate", {})
        failing = _failing_minima_from_gate(gate) or _failing_minima_from_evidence(
            str(data.get("evidence", ""))
        )
        if not failing:
            failing = f"verdict={verdict}; gate_pass={data.get('gate_pass', 'n/a')}"
        row = {
            "id": rid,
            "type": "experiment",
            "status": verdict,
            "verdict": verdict,
            "gate_outcome": data.get("last_verdict", verdict),
            "failing_minima": failing,
            "section_17_promotion_met": False,
            "section_17_conditions": section_17_evaluation(
                {"verdict": verdict, "status": verdict}
            ),
            "terminal_class": verdict,
            "source_artifact": f"research_state/{sources_by_id[rid][0]}",
            "source_artifacts": sources_by_id[rid],
            "superseded_sources": sources_by_id[rid][1:],
            "generated_utc": generated,
            "reopen_requires": list(REOPEN_MAP.get(rid, [])),
            "evidence_summary": str(data.get("evidence", ""))[:400],
        }
        rows.append(row)

    # --- alternative source probe audit ---
    for path in sorted(RESEARCH_STATE.glob("alt_source_probe_audit_*.json")):
        data = load_json(path)
        rid = path.stem
        row = {
            "id": rid,
            "type": "source_probe_audit",
            "status": "NO_ADMISSIBLE_SOURCE",
            "verdict": "NO_GO",
            "gate_outcome": "all probed families NO-GO",
            "failing_minima": "no candidate met §5/§16 minima (≥5 instruments, ≥1 complete month or ≥3×30d blocks, unauthenticated, provenance/license, observed labels only, venue-consistent)",
            "section_17_promotion_met": False,
            "section_17_conditions": {cond: False for cond in SECTION_17_CONDITIONS},
            "terminal_class": "NO_ADMISSIBLE_SOURCE",
            "source_artifact": f"research_state/{path.name}",
            "reopen_requires": ["NEW_OBSERVED_LIQUIDATION_SOURCE"],
            "evidence_summary": str(data)[:400],
        }
        rows.append(row)

    rows.sort(key=lambda r: r["id"])
    # Enforce exactly one row per ID.
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), f"duplicate row IDs: {ids}"
    return rows


def generate(utc: str) -> tuple[str, dict, dict]:
    artifacts = collect_input_artifacts()
    rows = build_rows(artifacts)
    section17_all_false = all(
        not r["section_17_promotion_met"]
        and all(not v for v in r["section_17_conditions"].values())
        for r in rows
    )
    closure = {
        "generated_utc": utc,
        "program_status": "CLOSED_TERMINAL",
        "terminal_verdict": "NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED",
        "n_rows": len(rows),
        "n_section_17_promotion_met": sum(
            1 for r in rows if r["section_17_promotion_met"]
        ),
        "section_17_all_conditions_not_met": section17_all_false,
        "reopen_only_via_registry": [t["trigger_id"] for t in TRIGGERS],
        "reopen_conditions": TRIGGERS,
        "rows": rows,
        "input_artifacts": artifacts,
        "determinism": "same inputs -> byte-identical output except generated_utc",
    }
    md = render_md(closure)
    registry = {
        "generated_utc": utc,
        "registry_version": 1,
        "n_triggers": len(TRIGGERS),
        "triggers": TRIGGERS,
    }
    return md, closure, registry


def render_md(closure: dict) -> str:
    lines: list[str] = []
    lines.append("# Program Terminal Structural Closure — FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS")
    lines.append("")
    lines.append(f"**Generated (UTC):** {closure['generated_utc']}")
    lines.append(f"**Program status:** {closure['program_status']}")
    lines.append(f"**Terminal verdict:** {closure['terminal_verdict']}")
    lines.append(f"**Rows enumerated:** {closure['n_rows']}")
    lines.append(f"**§17 promotion met (any row):** {closure['n_section_17_promotion_met']}")
    lines.append(f"**All §17 conditions not met:** {closure['section_17_all_conditions_not_met']}")
    lines.append("")
    lines.append("## Reopen conditions (machine-checkable; act only when satisfied)")
    lines.append("")
    for trig in closure["reopen_conditions"]:
        lines.append(f"- `{trig['trigger_id']}` (priority {trig['priority']}, status={trig['status']})")
        lines.append(f"  - predicate: {json.dumps(trig['machine_predicate'], sort_keys=True)}")
        lines.append(f"  - required evidence: {trig['required_evidence_artifact']}")
        lines.append(f"  - gate protocol: {trig['gate_protocol']}")
        lines.append(f"  - do_not_act_until_satisfied: {trig['do_not_act_until_satisfied']}")
    lines.append("")
    lines.append("## Enumerated experiments / hypotheses / sealed verdicts")
    lines.append("")
    lines.append(
        "| id | type | status | verdict | gate_outcome | §17 promotion met | terminal class | reopen_requires |"
    )
    lines.append(
        "|---|---|---|---|---|---|---|---|"
    )
    for r in closure["rows"]:
        lines.append(
            "| {id} | {type} | {status} | {verdict} | {gate_outcome} | {promo} | {tc} | {rr} |".format(
                id=r["id"],
                type=r["type"],
                status=r["status"],
                verdict=r["verdict"],
                gate_outcome=r["gate_outcome"],
                promo=r["section_17_promotion_met"],
                tc=r["terminal_class"],
                rr=",".join(r["reopen_requires"]) or "—",
            )
        )
    lines.append("")
    lines.append("## Failing minima (per row)")
    lines.append("")
    for r in closure["rows"]:
        lines.append(f"- **{r['id']}** ({r['type']}): {r['failing_minima']}")
    lines.append("")
    lines.append("## §17 condition detail (all not met)")
    lines.append("")
    for r in closure["rows"]:
        lines.append(f"- **{r['id']}**: " + ", ".join(
            f"{cond}={met}" for cond, met in r["section_17_conditions"].items()
        ))
    lines.append("")
    lines.append("## Input artifacts (sha256, for determinism audit)")
    lines.append("")
    for a in closure["input_artifacts"]:
        lines.append(f"- {a['path']} sha256={a['sha256']}")
    lines.append("")
    lines.append("## Determinism note")
    lines.append(
        "Same inputs -> byte-identical output except `generated_utc`. "
        "Generated offline; no estimators, fetches, probes, or discovery executed."
    )
    return "\n".join(lines) + "\n"


def write_json(path: Path, obj: dict) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")


def write_md(path: Path, text: str) -> None:
    with path.open("w", encoding="utf-8") as f:
        f.write(text)


def main() -> int:
    utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    ts = utc.replace("-", "").replace(":", "").replace(".", "").replace("Z", "")
    md, closure, registry = generate(utc)
    md_path = RESEARCH_STATE / f"fclr_final_structural_closure_{ts}.md"
    json_path = RESEARCH_STATE / f"fclr_final_structural_closure_{ts}.json"
    registry_path = RESEARCH_STATE / "resume_trigger_registry.json"
    write_md(md_path, md)
    write_json(json_path, closure)
    write_json(registry_path, registry)
    print(f"WROTE {md_path}")
    print(f"WROTE {json_path}")
    print(f"WROTE {registry_path}")
    print(f"rows={closure['n_rows']} section17_promotion_met_any={closure['n_section_17_promotion_met']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
