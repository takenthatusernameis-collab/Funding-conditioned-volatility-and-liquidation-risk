#!/usr/bin/env python3
"""FCLR-NEXT-144 / FCLR-022: deterministic read-only Gate 4 blocker-resolution
evidence preflight consuming FCLR-021 coverage matrix + missing_action_warnings.

For each coverage-gap row (missing_action_warnings entry) it performs a read-only
snapshot of the prerequisite's cited evidence_ref path: exists, read_state,
sha256, bytes. Missing stays missing — never fabricate evidence as present.
Emits resolution-readiness rows (window, prerequisite, current_state, gate_class,
evidence_ref, evidence_present, read_state, sha256, bytes, resolution_ready=false,
reason_copied_from_index, missing_action_class) plus resolution_readiness_warnings
for gaps lacking any local artifact. Planning/draft evidence only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_FCLR021 = REPO / "research_state" / "fclr021_local_audit" / "fclr021_gate4_blocker_resolution_checklist_validator_latest.json"
DEFAULT_OUT = REPO / "research_state" / "fclr022_local_audit"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO))
    except Exception:
        return str(path)


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


def evidence_snapshot(path_str):
    if not path_str or not isinstance(path_str, str):
        return {"path": path_str, "exists": False, "read_state": "no_path_cited", "sha256": None, "bytes": 0}
    p = Path(path_str)
    if not p.is_absolute():
        p = REPO / path_str
    if not p.exists():
        return {"path": path_str, "exists": False, "read_state": "missing", "sha256": None, "bytes": 0}
    try:
        raw = p.read_bytes()
    except Exception as e:
        return {"path": path_str, "exists": True, "read_state": f"read_error:{e}", "sha256": None, "bytes": 0}
    if raw.startswith(b"version https://git-lfs.github.com/spec/v1"):
        return {"path": path_str, "exists": True, "read_state": "unavailable_pointer", "sha256": None, "bytes": len(raw)}
    return {"path": path_str, "exists": True, "read_state": "ok", "sha256": sha256_bytes(raw), "bytes": len(raw)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fclr021", default=str(DEFAULT_FCLR021))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    src, state, err = read_json(Path(args.fclr021))
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    warnings = []
    if src is None:
        warnings.append({"type": "input_unavailable", "detail": err})
    else:
        gaps = src.get("missing_action_warnings") or []
        for g in gaps:
            snap = evidence_snapshot(g.get("evidence_ref"))
            present = bool(snap["exists"] and snap["read_state"] == "ok")
            row = {
                "window": g.get("window"),
                "prerequisite": g.get("prerequisite"),
                "current_state": g.get("current_state"),
                "gate_class": g.get("gate_class"),
                "evidence_ref": g.get("evidence_ref"),
                "evidence_present": present,
                "read_state": snap["read_state"],
                "sha256": snap["sha256"],
                "bytes": snap["bytes"],
                "resolution_ready": False,
                "reason_copied_from_index": g.get("reason") or g.get("blocker_or_missing_reason") or g.get("missing_action_class"),
                "missing_action_class": g.get("missing_action_class"),
            }
            rows.append(row)
            if not present:
                warnings.append({"type": "resolution_readiness_warning", "window": row["window"], "prerequisite": row["prerequisite"], "detail": snap["read_state"]})

    payload = {
        "script": "fclr022_gate4_blocker_resolution_evidence_preflight.py",
        "generated_at_utc": ts,
        "input": rel(Path(args.fclr021)),
        "input_state": state,
        "row_count": len(rows),
        "resolution_readiness_rows": rows,
        "resolution_readiness_warnings": warnings,
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
    }

    stamp = ts
    json_path = out_dir / f"fclr022_gate4_blocker_resolution_evidence_preflight_{stamp}.json"
    md_path = out_dir / f"fclr022_gate4_blocker_resolution_evidence_preflight_{stamp}.md"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(f"# FCLR-022 evidence preflight\n\nrows={len(rows)} warnings={len(warnings)}\n", encoding="utf-8")
    (out_dir / "fclr022_gate4_blocker_resolution_evidence_preflight_latest.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (out_dir / "fclr022_gate4_blocker_resolution_evidence_preflight_latest.md").write_text(md_path.read_text(), encoding="utf-8")
    print(json.dumps({"row_count": len(rows), "warnings": len(warnings), "out": rel(json_path)}, indent=2))


if __name__ == "__main__":
    main()
