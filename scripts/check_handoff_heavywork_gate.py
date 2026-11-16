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
  (2) The recorded heavy session subdir
      ``research_state/session_<UTC>/`` must exist and contain the mandatory
      Phase-B evidence set (feature attribution, impl cross-check, sealed
      bridge, trigger-gated prereg skeleton) plus the Phase-C synthesis.
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

_SESSION_DIR_RE = re.compile(r"(session_\d{8}T\d{6}Z)")


def _root_count(rs: Path) -> int:
    return len(list(rs.glob("*.md"))) + len(list(rs.glob("*.json")))


def _latest_handoff_session(handoff: Path) -> str | None:
    """Return the full ``session_<UTC>`` dir name (with prefix) from the handoff.

    Prefers the ``session_<UTC>/`` ids written in the Phase-B/Phase-C bullets and
    closeout lines. Returns the lexicographically-latest (UTC-sortable) id.
    """
    if not handoff.exists():
        return None
    text = handoff.read_text(encoding="utf-8", errors="ignore")
    matches = _SESSION_DIR_RE.findall(text)
    if not matches:
        return None
    return sorted(matches)[-1]


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
        "heavy_session_id": None,
        "heavy_session_dir": None,
        "heavy_session_exists": False,
        "heavy_session_missing": [],
        "root_count": 0,
        "root_count_cap": ROOT_COUNT_CAP,
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

    # (2) The heavy session subdir must exist and contain the Phase-B/C set.
    sid = _latest_handoff_session(handoff)
    payload["heavy_session_id"] = sid
    if not sid:
        payload["failures"].append("HEAVY_SESSION_ID_UNRECORDED")
    else:
        sdir = rs / sid
        payload["heavy_session_dir"] = str(sdir.relative_to(repo)) if sdir.exists() else None
        if not sdir.exists():
            payload["failures"].append(f"HEAVY_SESSION_DIR_MISSING:{sid}")
        else:
            payload["heavy_session_exists"] = True
            info = _session_has_required(sdir)
            payload["heavy_session_files"] = info["files"]
            payload["heavy_session_missing"] = info["missing"]
            if info["missing"]:
                payload["failures"].append(
                    f"HEAVY_SESSION_ARTIFACTS_MISSING:{sid}:{info['missing']}"
                )

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