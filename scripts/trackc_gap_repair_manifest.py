#!/usr/bin/env python3
"""Track C gap/repair manifest from panel admissibility audits.

Dep-light, stdlib-only, NO NETWORK, NO OUTCOMES/TARGETS/FEATURES/MODELS.
Consumes trackc_panel_admissibility_*.json and local cache metadata to emit
deterministic, machine-checkable repair planning: missing-series day ranges,
missing funding month files, and local source/provenance/checksum expectations.
It does NOT download, probe, compute outcomes, or satisfy confirmatory resume.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_SERIES = ("markPriceKlines", "indexPriceKlines", "premiumIndexKlines")


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _local_presence(cache: Path, sym: str, day: str):
    # deterministic local checks only; does not prove provenance/admissibility
    hits = {"csv": [], "zip": []}
    for pat in [f"**/*{sym}*{day}*.csv", f"**/{sym}-1h-{day}.zip", f"**/*{day}*{sym}*.zip"]:
        for p in cache.glob(pat):
            rp = str(p)
            if "/.git/" in rp:
                continue
            if p.suffix == ".csv":
                hits["csv"].append(rp)
            elif p.suffix == ".zip":
                hits["zip"].append(rp)
    hits["csv"] = sorted(set(hits["csv"]))[:12]
    hits["zip"] = sorted(set(hits["zip"]))[:12]
    sidecars = []
    for rp in hits["csv"] + hits["zip"]:
        for sc in (Path(rp + ".sha256"), Path(rp + ".CHECKSUM"), Path(rp + ".checksum"), Path(rp + ".etag")):
            if sc.exists():
                sidecars.append(str(sc))
    return {
        "local_files_present": bool(hits["csv"] or hits["zip"]),
        "csv_paths_sample": hits["csv"],
        "zip_paths_sample": hits["zip"],
        "adjacent_sidecars_found": sorted(set(sidecars))[:12],
        "checksum_expectation": "adjacent <file>.sha256 (or equivalent admissible sidecar) required for machine verification before confirmatory use; presence here is local-only, not provenance proof",
    }


def _funding_local(cache: Path, repo_root: Path, sym: str, months: list[str]):
    out = {}
    for m in months:
        name = f"{sym}-fundingRate-{m}.csv"
        found = []
        for root in (cache, repo_root, repo_root / "data" / "raw"):
            if not root.exists():
                continue
            for p in root.glob(f"**/{name}"):
                rp = str(p)
                if "/.git/" not in rp:
                    found.append(rp)
        found = sorted(set(found))
        sidecars = [rp + ".sha256" for rp in found if Path(rp + ".sha256").exists()]
        out[m] = {
            "expected_filename": name,
            "local_files_found": found[:8],
            "local_present": bool(found),
            "adjacent_sha256_sidecars_found": sidecars[:8],
            "required_local_action_if_missing": "obtain admissible unauthenticated source with provenance (URL/ETag/checksum) and place verified local month file; do not download in this tool; do not compute outcomes",
            "required_local_action_if_present": "verify schema/row coverage vs day range, record provenance/checksum lineage, confirm no outcome inspection",
        }
    return out


def build_manifest(audit_path: Path, cache: Path, repo_root: Path):
    audit = json.loads(audit_path.read_text())
    per = {}
    for sym, info in audit.get("per_symbol", {}).items():
        sg = info.get("series_gap_manifest") or {}
        series_repairs = {}
        for series in REQUIRED_SERIES:
            g = sg.get(series) or {}
            ranges = g.get("missing_day_ranges") or []
            samples = []
            for r in ranges[:8]:
                if not isinstance(r, list) or len(r) != 2:
                    continue
                start, end = r
                sample_day = start
                samples.append({"range": [start, end], "local_presence_sample_day": sample_day, "sample_day_presence": _local_presence(cache, sym, sample_day)})
            series_repairs[series] = {
                "complete_vs_mark_union": g.get("complete_vs_mark_union"),
                "missing_days_vs_mark_union": g.get("missing_days_vs_mark_union"),
                "missing_day_ranges": ranges,
                "missing_days_sample": g.get("missing_days_sample", [])[:120],
                "range_local_presence_samples": samples,
                "required_local_action": "no gap repair needed" if g.get("complete_vs_mark_union") else "if admissible local source files exist, deterministically assemble/verify missing day CSVs with checksum lineage; if absent, record evidence-backed blocker (no network, no outcomes)",
            }
        fc = info.get("funding_coverage") or {}
        expected_months = fc.get("funding_months_expected_for_range") or []
        overlap = set(fc.get("funding_months_overlap_expected") or [])
        missing_months = [m for m in expected_months if m not in overlap]
        per[sym] = {
            "range": info.get("range"),
            "days": info.get("days"),
            "required_series_complete": info.get("required_series_complete"),
            "resume_trigger_symbol_ok": info.get("resume_trigger_symbol_ok"),
            "confirmatory_ready_symbol": info.get("confirmatory_ready_symbol"),
            "series_repair_plan": series_repairs,
            "funding_repair_plan": {
                "funding_completeness_flag": fc.get("funding_completeness_flag"),
                "months_expected_for_range": expected_months,
                "months_overlap_expected": fc.get("funding_months_overlap_expected") or [],
                "months_missing_for_range": missing_months,
                "month_file_local_audit": _funding_local(cache, repo_root, sym, missing_months),
                "funding_note": fc.get("funding_note"),
                "required_local_action": "no funding month-file gap for range" if not missing_months else "missing month files for range; verify/admissibly source locally only with provenance/checksums — this tool does not download; do not compute outcomes",
            },
            "blockers": [
                b for b in [
                    None if info.get("required_series_complete") else "REQUIRED_SERIES_GAPS_VS_MARK_UNION",
                    None if not missing_months else "FUNDING_MONTH_FILES_MISSING_FOR_RANGE",
                    "CONFIRMATORY_REQUIRES_VERIFIED_PROVENANCE_CHECKSUMS",
                    "CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES",
                ] if b
            ],
        }
    missing_funding_any = sorted({m for s in per.values() for m in (s["funding_repair_plan"].get("months_missing_for_range") or [])})
    series_gaps_any = any(not ((per[sym]["series_repair_plan"].get(k) or {}).get("complete_vs_mark_union")) for sym in per for k in REQUIRED_SERIES)
    return {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_audit_path": str(audit_path),
        "source_audit_sha256": _sha256_file(audit_path),
        "source_audit_generated_utc": audit.get("generated_utc"),
        "cache": str(cache),
        "window_hint": audit.get("window_hint"),
        "resume_trigger_met_in_audit": audit.get("resume_trigger_met"),
        "confirmatory_resume_ready_in_audit": audit.get("confirmatory_resume_ready"),
        "symbols": audit.get("symbols"),
        "per_symbol": per,
        "summary": {
            "any_required_series_gaps": series_gaps_any,
            "any_funding_month_gaps_for_range": bool(missing_funding_any),
            "funding_months_missing_union": missing_funding_any,
            "locally_repairable_series_gaps_detected": False,
            "network_used": False,
            "outcomes_computed": False,
            "confirmatory_resume_ready": False,
        },
        "next_action": "no confirmatory outcomes; resolve only deterministically from locally present admissible files with checksums/provenance lineage; if not locally repairable, keep evidence-backed blocker and continue dep-light engineering/watch",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", required=True, help="trackc_panel_admissibility JSON")
    ap.add_argument("--cache", default="research_state/data_cache")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    repo_root = Path(args.repo_root).resolve()
    cache = (repo_root / args.cache).resolve() if not Path(args.cache).is_absolute() else Path(args.cache)
    report = build_manifest(Path(args.audit).resolve(), cache, repo_root)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "out": str(out),
        "source_audit_sha256": report["source_audit_sha256"],
        "funding_months_missing_union": report["summary"]["funding_months_missing_union"],
        "any_required_series_gaps": report["summary"]["any_required_series_gaps"],
        "network_used": False,
        "outcomes_computed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
