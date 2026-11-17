#!/usr/bin/env python3
"""FCLR-143: deterministic handoff-freshness + mandatory-heavy-work gate.

Machine-enforced, read-only, no network, no real research_state writes, no
parquet/outcome reads. This closes the last *structural* bottleneck in the
trigger-only frontier: the mandated heavy campaign (FCLR-RCA-011 / Phase-B) was
prose-only, so a future session could "complete" by running only the trigger
check + the unittest suite and skipping the heavy artifacts entirely.

This gate binds the durable handoff to concrete evidence artifacts on disk:

  (1) The sole durable handoff ``AGENT_HANDOFF.md`` must exist, must carry the
      ``INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION`` section, and must
      record the *last completed* heavy session id and its full-suite result.
  (2) The latest session in the handoff must show new heavy work: either it
      contains the mandatory Phase-B/C evidence set (feature attribution, impl
      cross-check, sealed bridge, trigger-gated prereg skeleton, and power
      synthesis), or it carries forward a complete bundle and adds an evidence
      audit plus a fresh quantitative artifact. The gate resolves the latest
      complete bundle separately.
  (3) The ``research_state/`` root md+json count must stay <= 500 (the churn
      cap enforced by test_tracka_hardening_125) — this gate also fails if the
      cap is breached, so a session cannot flood the root to dodge the check.

Exit 0 = PASS (all conditions met). Exit 1 = FAIL (machine-readable reasons).
``--json`` prints the full payload.

Usage:
  python scripts/check_handoff_heavywork_gate.py
  python scripts/check_handoff_heavywork_gate.py --json
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
HANDOFF = REPO / "AGENT_HANDOFF.md"

# Markers the handoff must contain to be a valid durable handoff.
HANDOFF_REQUIRED_MARKERS = (
    "INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION",
    "AGENT HANDOFF",
)

# Phase-B / Phase-C mandatory artifacts. Each heavy session must have produced
# these under research_state/session_<UTC>/. Filenames are matched by prefix
# because the exact UTC suffix varies per session.
PHASE_B_PREFIXES = (
    "rca011_feature_attribution_",   # feature attribution (json+md)
    "rca011_impl_crosscheck_",       # independent OLS/QR cross-check
    "rca011_sealed_bridge_",         # sealed-vs-recompute bridge (md)
    "prereg_template_trigger_gated_",  # power remediation prereg skeleton
)
PHASE_C_PREFIXES = (
    "program_power_synthesis_",      # synthesis with honest next_action_heavy
)

# Root churn cap (mirrors test_tracka_hardening_125.test_root_md_json_bounded).
ROOT_COUNT_CAP = 500

# FCLR-FRONTIER-VERIFY-06/07 hardening: once a frontier campaign has started, a
# later session cannot satisfy the gate with an arbitrary recompute_* artifact. It
# must emit the campaign's exact exhaustive-audit triad plus a trigger check.
# Multiple campaigns may be declared; every campaign that has started binds.
FRONTIER_VERIFY_CAMPAIGN_RE = re.compile(r"FCLR-FRONTIER-VERIFY-(\d+)-(\d{8}T\d{6}Z)")
FRONTIER_VERIFY_ARTIFACT_PREFIX = "recompute_frontier_exhaustive_audit_"
FRONTIER_VERIFY_REQUIRED_SUFFIXES = (".py", ".json", ".md")

# FCLR-TRIGGER-READINESS-01 hardening: once the trigger-readiness campaign has
# started, a later session cannot satisfy the gate with an arbitrary recompute_*
# artifact or a trigger-check-only session. It must emit the outcome-blind
# trigger-activation package (executor + self-test + readiness certificate) plus
# a trigger check. Sessions predating the campaign are grandfathered so the gate
# stays green during the handoff refresh that first announces the campaign.
TRIGGER_READINESS_CAMPAIGN_RE = re.compile(
    r"FCLR-TRIGGER-READINESS-(\d+)-(\d{8}T\d{6}Z)"
)
TRIGGER_READINESS_ARTIFACT_PREFIXES = (
    "trigger_activation_executor_",
    "trigger_activation_selftest_",
    "trigger_activation_readiness_",
)
# (prefix, required_suffix) pairs that must ALL be present in the latest session.
TRIGGER_READINESS_REQUIRED = (
    ("trigger_activation_executor_", ".py"),
    ("trigger_activation_executor_", ".json"),
    ("trigger_activation_selftest_", ".py"),
    ("trigger_activation_selftest_", ".json"),
    ("trigger_activation_readiness_", ".json"),
    ("trigger_activation_readiness_", ".md"),
)

_SESSION_DIR_RE = re.compile(r"(session_\d{8}T\d{6}Z)")

# New-style heavy sessions do not copy the static Phase-B bundle into every
# session directory. They carry forward a complete bundle and add a fresh
# evidence audit plus a new quantitative artifact. This keeps the gate from
# failing merely because the handoff records the latest audit session rather
# than the older complete bundle.
NEW_QUANT_PREFIXES = (
    "independent_recompute_",
    "trigger_readiness_power_calibration_",
    "trigger_readiness_power_ledger_",
    "power_ledger_refresh_",
    "reproducibility_recompute_",
    "recompute_",
    "trigger_activation_",
)
AUDIT_PREFIX = "evidence_audit_"


def _root_count(rs: Path) -> int:
    return len(list(rs.glob("*.md"))) + len(list(rs.glob("*.json")))


def _handoff_session_ids(handoff: Path) -> list[str]:
    if not handoff.exists():
        return []
    text = handoff.read_text(encoding="utf-8", errors="ignore")
    return sorted(set(_SESSION_DIR_RE.findall(text)))


def _latest_handoff_session(handoff: Path) -> str | None:
    """Return the lexicographically latest session_<UTC> id in the handoff."""
    ids = _handoff_session_ids(handoff)
    return ids[-1] if ids else None


def _latest_disk_session(rs: Path) -> str | None:
    """Return the lexicographically latest session_<UTC> directory on disk.

    FCLR-TRIGGER-READINESS-01 non-avoidance: the gate previously trusted the
    handoff's latest session id, so a session could create a post-campaign
    directory, skip the mandatory package, and leave the handoff pointing at an
    older session. The gate would stay green forever. Comparing the newest
    on-disk session against the newest handoff-recorded session closes that
    stale-handoff bypass: a newer session must be recorded (and then checked).
    """
    ids = []
    for p in rs.iterdir() if rs.is_dir() else []:
        m = _SESSION_DIR_RE.fullmatch(p.name)
        if m and p.is_dir():
            ids.append(m.group(1))
    return max(ids) if ids else None


def _session_has_required(session_dir: Path) -> dict:
    files = [p.name for p in session_dir.glob("*") if p.is_file()]
    missing = []
    for prefix in PHASE_B_PREFIXES:
        if not any(f.startswith(prefix) for f in files):
            missing.append(prefix + "*")
    for prefix in PHASE_C_PREFIXES:
        if not any(f.startswith(prefix) for f in files):
            missing.append(prefix + "*")
    return {"files": sorted(files), "missing": missing}


def _frontier_verify_state(handoff_text: str, latest_sid: str | None,
                           latest_files: list[str]) -> dict:
    """Return FCLR-FRONTIER-VERIFY-06 non-avoidance state for the latest session.

    The campaign id carries its start UTC. Sessions lexicographically after that
    start must contain the exact exhaustive-audit triad and a trigger check; an
    arbitrary recompute_* file is not enough. Sessions from before the campaign
    existed are grandfathered so this gate remains green during the handoff
    refresh that first announces the campaign.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = FRONTIER_VERIFY_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-FRONTIER-VERIFY-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    # Session ids are session_<UTC>; compare only the UTC portion.
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True
    required = [f"{FRONTIER_VERIFY_ARTIFACT_PREFIX}<UTC>{suffix}"
                for suffix in FRONTIER_VERIFY_REQUIRED_SUFFIXES]
    out["required_artifacts"] = required
    out["missing_required_artifacts"] = [
        artifact for artifact, suffix in zip(required, FRONTIER_VERIFY_REQUIRED_SUFFIXES)
        if not any(f.startswith(FRONTIER_VERIFY_ARTIFACT_PREFIX) and f.endswith(suffix)
                   for f in latest_files)
    ]
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") for f in latest_files
    )
    out["pass"] = not out["missing_required_artifacts"] and out["has_trigger_check"]
    return out


def _trigger_readiness_state(handoff_text: str, latest_sid: str | None,
                             latest_files: list[str]) -> dict:
    """Return FCLR-TRIGGER-READINESS-01 non-avoidance state for the latest session.

    After the trigger-readiness campaign starts, a post-start session must emit
    the outcome-blind trigger-activation package (executor + self-test + readiness
    certificate) plus a trigger check; an arbitrary recompute_* artifact is not
    enough. Sessions predating the campaign are grandfathered so this gate stays
    green during the handoff refresh that first announces the campaign.
    """
    out = {
        "campaign_id": None,
        "campaign_start_utc": None,
        "required": False,
        "required_artifacts": [],
        "missing_required_artifacts": [],
        "has_trigger_check": False,
        "pass": True,
    }
    m = TRIGGER_READINESS_CAMPAIGN_RE.search(handoff_text or "")
    if not m:
        return out
    campaign_start = m.group(2)
    out["campaign_id"] = f"FCLR-TRIGGER-READINESS-{m.group(1)}-{campaign_start}"
    out["campaign_start_utc"] = campaign_start
    if not latest_sid:
        return out
    latest_utc = latest_sid.removeprefix("session_")
    if latest_utc <= campaign_start:
        return out
    out["required"] = True
    required = [f"{prefix}<UTC>{suffix}" for prefix, suffix in TRIGGER_READINESS_REQUIRED]
    out["required_artifacts"] = required
    out["missing_required_artifacts"] = [
        label
        for label, (prefix, suffix) in zip(required, TRIGGER_READINESS_REQUIRED)
        if not any(f.startswith(prefix) and f.endswith(suffix) for f in latest_files)
    ]
    out["has_trigger_check"] = any(
        f.startswith("trigger_check_") and f.endswith(".json") for f in latest_files
    )
    out["pass"] = not out["missing_required_artifacts"] and out["has_trigger_check"]
    return out


def _session_has_new_heavy(session_dir: Path) -> dict:
    """Return whether a session has the new-style evidence audit + fresh quant."""
    files = [p.name for p in session_dir.glob("*") if p.is_file()]
    audit_files = [f for f in files if f.startswith(AUDIT_PREFIX)]
    quant_files = sorted(
        f for f in files if any(f.startswith(prefix) for prefix in NEW_QUANT_PREFIXES)
    )
    return {
        "files": sorted(files),
        "has_audit": bool(audit_files),
        "audit_files": audit_files,
        "has_new_quant": bool(quant_files),
        "new_quant_files": quant_files,
    }


def check(repo: Path = REPO) -> dict:
    rs = repo / "research_state"
    handoff = repo / "AGENT_HANDOFF.md"
    payload = {
        "script": "check_handoff_heavywork_gate",
        "network": False,
        "writes_real_research_state": False,
        "read_only": True,
        "pass": False,
        "failures": [],
        "handoff_exists": False,
        "handoff_markers_ok": False,
        "handoff_session_ids": [],
        "latest_session_id": None,
        "latest_disk_session_id": None,
        "handoff_stale": False,
        "latest_session_dir": None,
        "latest_session_evidence": None,
        "heavy_session_id": None,
        "heavy_session_dir": None,
        "heavy_session_exists": False,
        "heavy_session_missing": [],
        "root_count": 0,
        "root_count_cap": ROOT_COUNT_CAP,
        "frontier_verify": None,
        "trigger_readiness": None,
    }

    # (1) Handoff exists and carries the required markers.
    if not handoff.exists():
        payload["failures"].append("HANDOFF_MISSING")
    else:
        payload["handoff_exists"] = True
        text = handoff.read_text(encoding="utf-8", errors="ignore")
        missing_markers = [m for m in HANDOFF_REQUIRED_MARKERS if m not in text]
        if missing_markers:
            payload["failures"].append(f"HANDOFF_MARKERS_MISSING:{missing_markers}")
        else:
            payload["handoff_markers_ok"] = True

    # (2) The latest session must have done new heavy work.  A complete
    # carried-forward Phase-B/C bundle still satisfies the check; a new-style
    # session may instead carry a complete bundle forward and add an evidence
    # audit plus a fresh quantitative artifact.
    ids = _handoff_session_ids(handoff)
    latest_sid = ids[-1] if ids else None
    payload["handoff_session_ids"] = ids
    payload["latest_session_id"] = latest_sid
    latest_disk_sid = _latest_disk_session(rs)
    payload["latest_disk_session_id"] = latest_disk_sid
    if latest_sid and latest_disk_sid and latest_disk_sid > latest_sid:
        payload["handoff_stale"] = True
        payload["failures"].append(
            f"HANDOFF_STALE_LATEST_SESSION:{latest_disk_sid}"
        )
    if not latest_sid:
        payload["failures"].append("HEAVY_SESSION_ID_UNRECORDED")
    else:
        latest_sdir = rs / latest_sid
        payload["latest_session_dir"] = (
            str(latest_sdir.relative_to(repo)) if latest_sdir.exists() else None
        )
        latest_info = {"files": [], "missing": []}
        if not latest_sdir.exists():
            payload["failures"].append(f"HEAVY_SESSION_DIR_MISSING:{latest_sid}")
            latest_info["missing"] = [
                prefix + "*" for prefix in PHASE_B_PREFIXES + PHASE_C_PREFIXES
            ]
        else:
            latest_info = _session_has_required(latest_sdir)
            latest_new = _session_has_new_heavy(latest_sdir)
            payload["latest_session_evidence"] = latest_new
            latest_complete = not latest_info["missing"]
            latest_new_ok = latest_new["has_audit"] and latest_new["has_new_quant"]
            if not (latest_complete or latest_new_ok):
                payload["failures"].append(
                    f"HEAVY_SESSION_ARTIFACTS_MISSING:{latest_sid}:{latest_info['missing']}"
                )

            # FCLR-FRONTIER-VERIFY-06: after the campaign starts, require the
            # exact exhaustive-audit triad plus a trigger check, not any quant.
            fv = _frontier_verify_state(text, latest_sid, latest_info["files"])
            payload["frontier_verify"] = fv
            if fv["required"]:
                if fv["missing_required_artifacts"]:
                    payload["failures"].append(
                        "FRONTIER_VERIFY_ARTIFACTS_MISSING:"
                        + ",".join(fv["missing_required_artifacts"])
                    )
                if not fv["has_trigger_check"]:
                    payload["failures"].append(
                        f"FRONTIER_VERIFY_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

            # FCLR-TRIGGER-READINESS-01: after the campaign starts, require the
            # outcome-blind trigger-activation package plus a trigger check, not
            # any quant artifact.
            tr = _trigger_readiness_state(text, latest_sid, latest_info["files"])
            payload["trigger_readiness"] = tr
            if tr["required"]:
                if tr["missing_required_artifacts"]:
                    payload["failures"].append(
                        "TRIGGER_READINESS_ARTIFACTS_MISSING:"
                        + ",".join(tr["missing_required_artifacts"])
                    )
                if not tr["has_trigger_check"]:
                    payload["failures"].append(
                        f"TRIGGER_READINESS_TRIGGER_CHECK_MISSING:{latest_sid}"
                    )

        complete_sid = None
        for cand in reversed(ids):
            cdir = rs / cand
            if cdir.exists() and not _session_has_required(cdir)["missing"]:
                complete_sid = cand
                break

        heavy_sid = complete_sid or latest_sid
        payload["heavy_session_id"] = heavy_sid
        heavy_sdir = rs / heavy_sid
        if heavy_sdir.exists():
            payload["heavy_session_exists"] = True
            payload["heavy_session_dir"] = str(heavy_sdir.relative_to(repo))
            heavy_info = _session_has_required(heavy_sdir)
            payload["heavy_session_files"] = heavy_info["files"]
            payload["heavy_session_missing"] = heavy_info["missing"]
            if complete_sid is not None and heavy_info["missing"]:
                payload["failures"].append(
                    f"HEAVY_SESSION_ARTIFACTS_MISSING:{heavy_sid}:{heavy_info['missing']}"
                )
        else:
            payload["heavy_session_missing"] = latest_info["missing"]

    # (3) Root churn cap.
    rc = _root_count(rs)
    payload["root_count"] = rc
    if rc > ROOT_COUNT_CAP:
        payload["failures"].append(f"ROOT_COUNT_EXCEEDS_CAP:{rc}>{ROOT_COUNT_CAP}")

    payload["pass"] = not payload["failures"]
    payload["reason_code"] = "OK" if payload["pass"] else "HANDOFF_HEAVYWORK_GATE_FAILED"
    return payload


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    res = check()
    if args.json:
        print(json.dumps(res, indent=2, sort_keys=True))
    else:
        status = "PASS" if res["pass"] else "FAIL"
        print(
            f"[{status}] handoff-heavywork gate: handoff={res['handoff_exists']} "
            f"markers={res['handoff_markers_ok']} "
            f"heavy_session={res['heavy_session_id']} "
            f"session_ok={res['heavy_session_exists'] and not res['heavy_session_missing']} "
            f"root={res['root_count']}/{res['root_count_cap']} "
            f"reason={res['reason_code']}"
        )
        if res["failures"]:
            for f in res["failures"]:
                print("  -", f)
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())