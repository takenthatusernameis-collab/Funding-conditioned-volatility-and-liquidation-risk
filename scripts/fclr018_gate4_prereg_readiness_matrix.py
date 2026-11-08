#!/usr/bin/env python3
"""FCLR-NEXT-140 / FCLR-018: deterministic read-only Gate 4 prereg-readiness matrix.

Consumes local evidence (fclr017 latest audit + sealed v3 manifest/prereg refs where
readable) and enumerates candidate Gate 4 windows with design feasibility fields.
Emits DRAFT (NOT FROZEN) prereg skeleton under research_state/fclr018_local_audit/.

Read-only, no network, no model-outcome computation, no freeze/promotion, no sealed
artifact overwrite. Planning/draft evidence only.
"""
from __future__ import annotations

import argparse
import calendar
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_FCLR017 = REPO / "research_state" / "fclr017_local_audit" / "fclr017_gate4_cache_audit_latest.json"
DEFAULT_V3_MANIFEST = REPO / "research_state" / "run_manifest_funding_v3_30d.json"
DEFAULT_V3_PREREG = REPO / "research_state" / "pre_registration_gate4_funding_multisplit_v3_30d_20261107T033500Z.md"
DEFAULT_V3_EVAL = REPO / "research_state" / "evaluation_summary_funding_v3_30d.md"
DEFAULT_OUT = REPO / "research_state" / "fclr018_local_audit"
DEFAULT_CACHE = REPO / "research_state" / "data_cache"
DEFAULT_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT"]
EVIDENCED_BOUNDED_RANGE = ("2024-04-01", "2024-09-30")  # identity-verified bounded slice per FCLR-015 context
V5_TERMS_BLOCKER = {
    "all_go": False,
    "confirmatory_outcomes_permitted": False,
    "terms_status": "EXPLICIT_BLOCKER_UNRESOLVED",
    "fabricated": False,
}
DAILY_KINDS = ["klines", "markPriceKlines", "indexPriceKlines", "premiumIndexKlines"]
FUNDING_KIND = "fundingRate"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO))
    except Exception:
        return str(path)


def read_json_optional(path: Path):
    if not path.exists():
        return None, f"missing:{rel(path)}"
    try:
        txt = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return None, f"read_error:{rel(path)}:{e}"
    # LFS pointer is not JSON evidence content
    if txt.startswith("version https://git-lfs.github.com/spec/v1"):
        return None, f"lfs_pointer_unavailable:{rel(path)}"
    try:
        return json.loads(txt), None
    except Exception as e:
        return None, f"json_parse_error:{rel(path)}:{e}"


def days_in_month(ym: str) -> int:
    y, m = map(int, ym.split("-"))
    return calendar.monthrange(y, m)[1]


def month_days(ym: str):
    return [f"{ym}-{d:02d}" for d in range(1, days_in_month(ym) + 1)]


def all_days_in_range(start_ym: str, end_ym: str):
    # inclusive month range YYYY-MM
    y1, m1 = map(int, start_ym.split("-"))
    y2, m2 = map(int, end_ym.split("-"))
    cur = (y1, m1)
    end = (y2, m2)
    out = []
    while cur <= end:
        ym = f"{cur[0]:04d}-{cur[1]:02d}"
        out.extend(month_days(ym))
        ny, nm = (cur[0] + 1, 1) if cur[1] == 12 else (cur[0], cur[1] + 1)
        cur = (ny, nm)
    return out


def cache_month_complete(cache: Path, sym: str, ym: str):
    d = cache / f"{sym}_{ym.replace('-', '_')}"
    if not d.exists() or not d.is_dir():
        return False, "missing_month_dir"
    expected = set(month_days(ym))
    for kind in DAILY_KINDS:
        present = set()
        for p in d.iterdir():
            if p.is_dir() and p.name.startswith(f"{kind}-"):
                present.add(p.name.replace(f"{kind}-", "", 1))
        missing = expected - present
        if missing:
            return False, f"missing_days:{kind}:{len(missing)}"
        for day in sorted(expected):
            kd = d / f"{kind}-{day}"
            if not any((kd / n).exists() for n in [f"{sym}-1h-{day}.zip", f"{sym}-1h-{day}.csv"]):
                return False, f"missing_canonical:{kind}:{day}"
    # funding: expected zip or csv-bearing source
    fzip = d / f"{sym}-fundingRate-{ym}.zip"
    fdir = d / f"{sym}-fundingRate-{ym}"
    has_csv = fdir.exists() and any(fdir.rglob(f"{sym}-fundingRate-{ym}.csv"))
    if not fzip.exists() and not has_csv:
        return False, "missing_funding"
    return True, "ok"


def window_months(start: str, end: str):
    # start/end YYYY-MM-DD
    y1, m1 = int(start[:4]), int(start[5:7])
    y2, m2 = int(end[:4]), int(end[5:7])
    cur = (y1, m1)
    endm = (y2, m2)
    out = []
    while cur <= endm:
        out.append(f"{cur[0]:04d}-{cur[1]:02d}")
        ny, nm = (cur[0] + 1, 1) if cur[1] == 12 else (cur[0], cur[1] + 1)
        cur = (ny, nm)
    return out


def span_days(start: str, end: str) -> int:
    from datetime import date
    a = date.fromisoformat(start)
    b = date.fromisoformat(end)
    return (b - a).days + 1


def max_non_overlapping_blocks(span: int, block_days: int = 30, purge_days: int = 7):
    # Simple feasibility: count non-overlapping 30d test blocks with >=7d purge gap
    # between consecutive test windows in an expanding-walk-forward framing requires train space;
    # deterministic upper bound given by fitting blocks+gaps in available span.
    if span < block_days:
        return 0
    n = 1
    used = block_days
    while used + purge_days + block_days <= span:
        used += purge_days + block_days
        n += 1
    return n


def provenance_status_for_window(start: str, end: str, evidenced_range=EVIDENCED_BOUNDED_RANGE):
    # Bounded identity-verified only where evidenced (FCLR-015): 2024-04..09
    if start >= evidenced_range[0] and end <= evidenced_range[1]:
        return "IDENTITY_VERIFIED_BOUNDED_FCLR015"
    return "UNVERIFIED"


def candidate_windows(cache: Path):
    # Deterministic candidate set from local cache months for default 5-symbol cohort.
    months = []
    for p in sorted(cache.iterdir()):
        if not p.is_dir():
            continue
        name = p.name
        # SYMBOL_YYYY_MM
        for sym in DEFAULT_SYMBOLS:
            pref = f"{sym}_"
            if name.startswith(pref):
                ym = name[len(pref):].replace("_", "-")
                if len(ym) == 7 and ym[4] == "-":
                    months.append(ym)
                break
    months = sorted(set(months))
    # Candidate windows: evidenced bounded first, then contiguous local ranges as exploratory.
    windows = []
    # Always include evidenced bounded window
    windows.append({"window_id": "cand_2024_04_09_evidenced", "start": "2024-04-01", "end": "2024-09-30", "basis": "fclr015_evidenced_bounded"})
    # 2024-10..12 if present
    if all(m in months for m in ["2024-10", "2024-11", "2024-12"]):
        windows.append({"window_id": "cand_2024_10_12_local_exploratory", "start": "2024-10-01", "end": "2024-12-31", "basis": "local_cache_contiguous_unprovenanced"})
    # 2024-04..12 contiguous exploratory extension (contains evidenced prefix)
    if all(m in months for m in ["2024-04","2024-05","2024-06","2024-07","2024-08","2024-09","2024-10","2024-11","2024-12"]):
        windows.append({"window_id": "cand_2024_04_12_mixed_evidenced_prefix", "start": "2024-04-01", "end": "2024-12-31", "basis": "local_cache_mixed_evidenced_prefix_unprovenanced_suffix"})
    # 2025 full-year exploratory only if all 12 months present
    y2025 = [f"2025-{m:02d}" for m in range(1, 13)]
    if all(m in months for m in y2025):
        windows.append({"window_id": "cand_2025_01_12_local_exploratory", "start": "2025-01-01", "end": "2025-12-31", "basis": "local_cache_contiguous_unprovenanced"})
    # 2024 full year exploratory if complete
    y2024 = [f"2024-{m:02d}" for m in range(1, 13)]
    if all(m in months for m in y2024):
        windows.append({"window_id": "cand_2024_01_12_local_exploratory", "start": "2024-01-01", "end": "2024-12-31", "basis": "local_cache_contains_evidenced_but_entire_window_not_verified"})
    # de-dupe by id preserving order
    seen = set(); out = []
    for w in windows:
        if w["window_id"] not in seen:
            seen.add(w["window_id"]); out.append(w)
    return out, months


def evaluate_window(w, cache: Path, symbols, fclr017, v3_manifest):
    start, end = w["start"], w["end"]
    months = window_months(start, end)
    span = span_days(start, end)
    blocks_max = max_non_overlapping_blocks(span, 30, 7)
    block_count_gate = blocks_max >= 3
    coverage = {}
    all_complete = True
    for sym in symbols:
        sym_cov = {"months": {}, "all_months_complete": True}
        for ym in months:
            ok, reason = cache_month_complete(cache, sym, ym)
            sym_cov["months"][ym] = {"complete": ok, "reason": reason}
            if not ok:
                sym_cov["all_months_complete"] = False
                all_complete = False
        coverage[sym] = sym_cov
    prov = provenance_status_for_window(start, end)
    # v5 unresolved terms forces confirmatory ineligibility always
    confirmatory_eligible = False
    confirmatory_eligibility = "INELIGIBLE_EXPLORATORY"
    eligibility_reasons = []
    if V5_TERMS_BLOCKER["terms_status"] == "EXPLICIT_BLOCKER_UNRESOLVED" or not V5_TERMS_BLOCKER["all_go"]:
        eligibility_reasons.append("v5_terms_blocker_unresolved_all_go_false")
    if prov != "IDENTITY_VERIFIED_BOUNDED_FCLR015":
        eligibility_reasons.append("provenance_not_identity_verified_bounded_fclr015")
    if not all_complete:
        eligibility_reasons.append("calendar_coverage_incomplete_or_unverified")
    if not block_count_gate:
        eligibility_reasons.append("block_count_gate_lt_3")
    # Even if technical preconditions were met, confirmatory requires fresh frozen prereg+admissibility gates green
    if not eligibility_reasons:
        confirmatory_eligibility = "ELIGIBLE_ONLY_IF_FRESH_FROZEN_PREREG_AND_ADMISSIBILITY_GATES_GREEN"
    else:
        confirmatory_eligibility = "INELIGIBLE_EXPLORATORY"
    return {
        **w,
        "symbols": list(symbols),
        "span_days": span,
        "months": months,
        "max_non_overlapping_30d_blocks_with_7d_purge": blocks_max,
        "block_count_gate_ge_3": block_count_gate,
        "purge_embargo_days": 7,
        "block_days": 30,
        "calendar_coverage_all_symbols_complete": all_complete,
        "coverage_by_symbol": coverage,
        "provenance_status": prov,
        "confirmatory_eligibility": confirmatory_eligibility,
        "confirmatory_eligible_now": confirmatory_eligible,
        "confirmatory_ineligibility_reasons": eligibility_reasons,
        "v5_terms_blocker_state": V5_TERMS_BLOCKER,
        "fclr017_reference_global_ok_for_default_scope": bool((fclr017 or {}).get("summary", {}).get("global_all_months_ok")) if fclr017 else None,
        "sealed_v3_manifest_ref": rel(DEFAULT_V3_MANIFEST),
        "sealed_v3_manifest_readable_json": bool(v3_manifest),
    }


def draft_prereg_skeleton(best_candidate, report):
    return {
        "status": "DRAFT_NOT_FROZEN",
        "not_executable_as_confirmatory": True,
        "freeze_promotion_authorized": False,
        "requires_fresh_frozen_prereg_before_outcomes": True,
        "based_on_candidate": best_candidate["window_id"] if best_candidate else None,
        "hypotheses": {
            "H1_primary": "DRAFT: RV+funding features vs RV-only baseline improve 24h forward realized-variance forecast loss (QLIKE) out-of-sample; direction/magnitude not pre-claimed.",
            "H0": "DRAFT: No incremental forecast skill beyond RV-only baseline."
        },
        "primary_contrast_candidates": ["E_rv_signed_abs_roll vs A_rv_only (candidate, subject to frozen prereg)", "D/B/C vs A secondary/reporting-only unless separately frozen"],
        "split_block_bootstrap_params_draft": {
            "chronological": True,
            "walk_forward_non_overlapping_test_blocks": True,
            "block_days": 30,
            "purge_embargo_days": 7,
            "min_non_overlapping_blocks": 3,
            "bootstrap": "block bootstrap over UTC day blocks (draft; seed/reps fixed only at freeze)",
            "leakage_controls": ["chronological splits", "train-only normalization", "funding merge last-known<=hour", "forward targets not used in train", "no random splits", "no test tuning"]
        },
        "acceptance_stop_rules_draft": [
            "Claim-worthy only if fresh frozen prereg before outcomes, admissibility gates green, provenance/terms resolved as required, >=5 instruments, >=3 non-overlapping 30d blocks, leakage audit clean, stable pre-registered uncertainty.",
            "If any sufficiency/coverage/leakage/provenance/terms criterion fails: PILOT/INCONCLUSIVE or INELIGIBLE; no confirmatory claim.",
            "No threshold shopping; no H001/economic/overlay/Track A status change without separate evidence."
        ],
        "confirmatory_gate_note": "2024-04..09 confirmatory bounded by PROVENANCED_CONFIRMATORY_RANGES + manifest/terms evidence + admissibility guards; v5 terms EXPLICIT_BLOCKER_UNRESOLVED/all_go=false blocks confirmatory outcomes."
    }


def build_report(cache: Path, fclr017_path: Path, v3_manifest_path: Path, v3_prereg_path: Path, out_dir: Path):
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fclr017, fclr017_err = read_json_optional(fclr017_path)
    v3_manifest, v3_manifest_err = read_json_optional(v3_manifest_path)
    v3_prereg_ok = v3_prereg_path.exists() and v3_prereg_path.is_file()
    windows, local_months = candidate_windows(cache)
    evaluated = [evaluate_window(w, cache, DEFAULT_SYMBOLS, fclr017, v3_manifest) for w in windows]
    # best candidate: evidenced complete first, else any complete exploratory (still ineligible if unprovenanced/v5)
    evidenced_complete = [w for w in evaluated if w["window_id"] == "cand_2024_04_09_evidenced" and w["calendar_coverage_all_symbols_complete"]]
    complete_any = [w for w in evaluated if w["calendar_coverage_all_symbols_complete"]]
    best = evidenced_complete[0] if evidenced_complete else (complete_any[0] if complete_any else (evaluated[0] if evaluated else None))
    draft = draft_prereg_skeleton(best, None)
    report = {
        "artifact": "fclr018_gate4_prereg_readiness_matrix",
        "version": 1,
        "timestamp_utc": ts,
        "no_confirmatory_outcomes": True,
        "exploratory_only": True,
        "no_network": True,
        "not_go_for_confirmatory_outcomes": True,
        "prereg_status": "DRAFT_NOT_FROZEN",
        "purpose": "deterministic read-only Gate 4 prereg-readiness/draft design matrix from local evidence; planning/draft only",
        "inputs": {
            "fclr017_latest": {"path": rel(fclr017_path), "readable": bool(fclr017), "note": fclr017_err},
            "v3_manifest": {"path": rel(v3_manifest_path), "readable": bool(v3_manifest), "note": v3_manifest_err, "sealed_ref_only": True},
            "v3_prereg": {"path": rel(v3_prereg_path), "exists": v3_prereg_ok},
            "v3_eval": {"path": rel(DEFAULT_V3_EVAL), "exists": DEFAULT_V3_EVAL.exists()},
            "cache_root": rel(cache),
            "local_cache_months_detected": local_months,
        },
        "symbols": DEFAULT_SYMBOLS,
        "v5_terms_blocker_state": V5_TERMS_BLOCKER,
        "provenanced_confirmatory_ranges_note": "2024-04-01..2024-09-30 identity-verified bounded (FCLR-015 context) only; confirmatory bounded by PROVENANCED_CONFIRMATORY_RANGES + manifest/terms evidence + admissibility guards.",
        "caveats": {
            "draft_only_not_frozen_not_promoted": True,
            "no_confirmatory_outcomes_computed": True,
            "v5_terms_explicit_blocker_unresolved": True,
            "fclr015_identity_verified_slice_only_where_evidenced": "2024-04..09",
            "unprovenanced_windows_are_exploratory": True,
            "sealed_artifacts_untouched": [rel(DEFAULT_V3_EVAL), rel(DEFAULT_V3_MANIFEST), rel(DEFAULT_V3_PREREG)],
            "confirmatory_requires_fresh_frozen_prereg_before_outcomes": True,
        },
        "candidate_windows": evaluated,
        "best_candidate_planning_reference": best["window_id"] if best else None,
        "draft_prereg_skeleton": draft,
        "decision": {
            "confirmatory_ready_now": False,
            "reason": "draft_planning_only_and_v5_terms_blocker_unresolved",
            "next_claimworthy_gate": "fresh frozen prereg before outcomes + admissibility/terms/provenance gates green + bounded confirmatory range evidence",
        },
    }
    report["report_sha256"] = sha256_bytes(json.dumps(report, sort_keys=True).encode())
    return report, ts


def write_md(report: dict, path: Path):
    lines = []
    lines.append(f"# FCLR-018 Gate 4 prereg-readiness matrix ({report['timestamp_utc']})")
    lines.append("")
    lines.append("- method: deterministic local evidence read; read-only; no network; no model-outcome computation")
    lines.append(f"- prereg_status: **{report['prereg_status']}** (NOT FROZEN / NOT PROMOTED / NOT EXECUTABLE AS CONFIRMATORY)")
    lines.append(f"- no_confirmatory_outcomes: **{report['no_confirmatory_outcomes']}**")
    lines.append(f"- exploratory_only: **{report['exploratory_outcomes'] if 'exploratory_outcomes' in report else report['exploratory_only']}**")
    lines.append(f"- no_network: **{report['no_network']}**")
    lines.append(f"- not_go_for_confirmatory_outcomes: **{report['not_go_for_confirmatory_outcomes']}**")
    lines.append(f"- confirmatory_ready_now: **{report['decision']['confirmatory_ready_now']}**")
    lines.append("")
    lines.append("## Caveats / gates")
    for k, v in report["caveats"].items():
        lines.append(f"- {k}: `{v}`")
    lines.append(f"- v5_terms_blocker_state: `{json.dumps(report['v5_terms_blocker_state'], sort_keys=True)}`")
    lines.append(f"- provenanced_confirmatory_ranges_note: {report['provenanced_confirmatory_ranges_note']}")
    lines.append("")
    lines.append("## Candidate windows")
    for w in report["candidate_windows"]:
        lines.append(f"### {w['window_id']} ({w['start']}..{w['end']})")
        lines.append(f"- basis: `{w['basis']}` | span_days={w['span_days']} | months={len(w['months'])}")
        lines.append(f"- max_non_overlapping_30d_blocks_with_7d_purge: {w['max_non_overlapping_30d_blocks_with_7d_purge']} | block_count_gate_ge_3: **{w['block_count_gate_ge_3']}**")
        lines.append(f"- calendar_coverage_all_symbols_complete: **{w['calendar_coverage_all_symbols_complete']}**")
        lines.append(f"- provenance_status: **{w['provenance_status']}**")
        lines.append(f"- confirmatory_eligibility: **{w['confirmatory_eligibility']}** | confirmatory_eligible_now: **{w['confirmatory_eligible_now']}**")
        lines.append(f"- confirmatory_ineligibility_reasons: `{w['confirmatory_ineligibility_reasons']}`")
        lines.append("")
    lines.append("## DRAFT prereg skeleton (NOT FROZEN)")
    lines.append("```json")
    lines.append(json.dumps(report["draft_prereg_skeleton"], indent=2, sort_keys=True))
    lines.append("```")
    lines.append("")
    lines.append("Planning/draft evidence only — not GO for confirmatory outcomes, not frozen/promoted, no overlay/H001/Track A status change.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cache-root", default=str(DEFAULT_CACHE))
    ap.add_argument("--fclr017-json", default=str(DEFAULT_FCLR017))
    ap.add_argument("--v3-manifest", default=str(DEFAULT_V3_MANIFEST))
    ap.add_argument("--v3-prereg", default=str(DEFAULT_V3_PREREG))
    ap.add_argument("--out-dir", default=str(DEFAULT_OUT))
    ap.add_argument("--json-name", default=None)
    ap.add_argument("--md-name", default=None)
    args = ap.parse_args(argv)
    cache = Path(args.cache_root)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report, ts = build_report(cache, Path(args.fclr017_json), Path(args.v3_manifest), Path(args.v3_prereg), out_dir)
    json_name = args.json_name or f"fclr018_gate4_prereg_readiness_{ts}.json"
    md_name = args.md_name or f"fclr018_gate4_prereg_readiness_{ts}.md"
    jpath = out_dir / json_name
    mpath = out_dir / md_name
    jpath.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_md(report, mpath)
    (out_dir / "fclr018_gate4_prereg_readiness_latest.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "fclr018_gate4_prereg_readiness_latest.md").write_text(mpath.read_text(encoding="utf-8"), encoding="utf-8")
    print(json.dumps({
        "json": rel(jpath), "md": rel(mpath),
        "latest_json": rel(out_dir / "fclr018_gate4_prereg_readiness_latest.json"),
        "latest_md": rel(out_dir / "fclr018_gate4_prereg_readiness_latest.md"),
        "prereg_status": report["prereg_status"],
        "no_confirmatory_outcomes": True, "exploratory_only": True, "no_network": True,
        "confirmatory_ready_now": False,
        "candidate_count": len(report["candidate_windows"]),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
