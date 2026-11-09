#!/usr/bin/env python3
"""Track C local funding month-file schema/provenance checklist audit.

Dep-light, stdlib-only, NO NETWORK, NO OUTCOMES/TARGETS/FEATURES/MODELS.
Verifies schema and basic row/time sanity of locally present funding CSV files
for given symbols and expected month range. Emits a machine-checkable blocker
register. It does NOT prove upstream provenance, does NOT download, and does
NOT satisfy confirmatory resume (verified provenance/checksums + frozen
prereg-before-outcomes still required).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
REQUIRED_FIELDS = {"calc_time", "last_funding_rate"}
ACCEPTED_TIME_FIELDS = ("calc_time", "calcTime", "fundingTime")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def find_funding_file(repo_root: Path, cache: Path, sym: str, month: str):
    name = f"{sym}-fundingRate-{month}.csv"
    roots = [cache, repo_root, repo_root / "data" / "raw", repo_root / "data_cache"]
    seen = set()
    found = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.glob(f"**/{name}"):
            try:
                rp = str(p.resolve())
            except Exception:
                rp = str(p)
            if rp in seen or "/.git/" in rp:
                continue
            seen.add(rp)
            found.append(Path(rp))
    return sorted(found)


def month_start_end_ms(month: str):
    y, m = [int(x) for x in month.split("-")]
    start = datetime(y, m, 1, tzinfo=timezone.utc)
    if m == 12:
        end = datetime(y + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end = datetime(y, m + 1, 1, tzinfo=timezone.utc)
    return int(start.timestamp() * 1000), int(end.timestamp() * 1000) - 1


def audit_file(p: Path, month: str):
    start_ms, end_ms = month_start_end_ms(month)
    blockers = []
    warnings = []
    row_count = 0
    bad_time = 0
    out_of_month = 0
    bad_rate = 0
    time_field = None
    fields = None
    min_ms = None
    max_ms = None
    try:
        with p.open("r", newline="") as f:
            reader = csv.DictReader(f)
            fields = reader.fieldnames or []
            if not set(fields) & REQUIRED_FIELDS:
                blockers.append("SCHEMA_MISSING_REQUIRED_FIELDS")
            for tf in ACCEPTED_TIME_FIELDS:
                if tf in fields:
                    time_field = tf
                    break
            if not time_field:
                blockers.append("SCHEMA_MISSING_TIME_FIELD")
            for row in reader:
                row_count += 1
                ct = (row.get(time_field) if time_field else None) or row.get("calc_time") or row.get("calcTime") or row.get("fundingTime")
                try:
                    ms = int(float(ct)) if ct is not None and str(ct).strip() != "" else None
                except Exception:
                    ms = None
                if ms is None:
                    bad_time += 1
                else:
                    min_ms = ms if min_ms is None else min(min_ms, ms)
                    max_ms = ms if max_ms is None else max(max_ms, ms)
                    if ms < start_ms - 86400000 or ms > end_ms + 86400000:
                        out_of_month += 1
                lr = row.get("last_funding_rate") or row.get("fundingRate") or row.get("lastFundingRate")
                try:
                    if lr is None or str(lr).strip() == "":
                        bad_rate += 1
                    else:
                        float(lr)
                except Exception:
                    bad_rate += 1
    except Exception as e:
        blockers.append(f"READ_ERROR:{type(e).__name__}")
    if row_count == 0:
        blockers.append("NO_ROWS")
    if bad_time > 0:
        warnings.append(f"BAD_TIME_ROWS:{bad_time}")
    if out_of_month > 0:
        warnings.append(f"ROWS_OUTSIDE_MONTH_TOLERANCE:{out_of_month}")
    if bad_rate > 0:
        warnings.append(f"BAD_RATE_ROWS:{bad_rate}")
    sidecar = Path(str(p) + ".sha256")
    return {
        "path": str(p),
        "sha256": sha256_file(p),
        "adjacent_sha256_sidecar_present": sidecar.exists(),
        "adjacent_sha256_sidecar_path": str(sidecar) if sidecar.exists() else None,
        "schema_fields": fields,
        "time_field_used": time_field,
        "row_count": row_count,
        "min_calc_time_ms": min_ms,
        "max_calc_time_ms": max_ms,
        "month_expected": month,
        "schema_ok": "SCHEMA_MISSING_REQUIRED_FIELDS" not in blockers and "SCHEMA_MISSING_TIME_FIELD" not in blockers and row_count > 0,
        "blockers": blockers,
        "warnings": warnings,
        "provenance_verified": False,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--cache", default="research_state/data_cache")
    ap.add_argument("--symbols", default=",".join(DEFAULT_SYMBOLS))
    ap.add_argument("--months", required=True, help="comma-separated YYYY-MM")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    repo_root = Path(args.repo_root).resolve()
    cache = (repo_root / args.cache).resolve() if not Path(args.cache).is_absolute() else Path(args.cache)
    syms = [s.strip() for s in args.symbols.split(",") if s.strip()]
    months = [m.strip() for m in args.months.split(",") if m.strip()]
    per = {}
    missing = []
    schema_bad = []
    for sym in syms:
        per[sym] = {"months": {}}
        for month in months:
            found = find_funding_file(repo_root, cache, sym, month)
            if not found:
                per[sym]["months"][month] = {
                    "local_present": False,
                    "files": [],
                    "schema_ok": False,
                    "provenance_verified": False,
                    "blockers": ["MISSING_LOCAL_FUNDING_MONTH_FILE"],
                    "required_local_action": "obtain admissible unauthenticated source with provenance (URL/ETag/checksum) and place verified local month file; this tool does not download; do not compute outcomes",
                }
                missing.append(f"{sym}:{month}")
                continue
            audits = [audit_file(p, month) for p in found[:3]]
            ok = any(a["schema_ok"] for a in audits)
            if not ok:
                schema_bad.append(f"{sym}:{month}")
            per[sym]["months"][month] = {
                "local_present": True,
                "files": audits,
                "schema_ok": ok,
                "provenance_verified": False,
                "blockers": [] if ok else ["SCHEMA_OR_ROW_SANITY_FAILED"],
                "required_local_action": "verify upstream provenance/checksum lineage before confirmatory use; do not compute outcomes" if ok else "repair/replace file from admissible source with verified provenance; do not compute outcomes",
            }
    report = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repo_root": str(repo_root),
        "cache": str(cache),
        "symbols": syms,
        "months": months,
        "per_symbol": per,
        "summary": {
            "missing_symbol_months": missing,
            "schema_bad_symbol_months": schema_bad,
            "all_requested_present_and_schema_ok": len(missing) == 0 and len(schema_bad) == 0,
            "confirmatory_resume_ready": False,
            "provenance_verified": False,
            "network_used": False,
            "outcomes_computed": False,
        },
        "blockers_global": [
            "CONFIRMATORY_REQUIRES_VERIFIED_PROVENANCE_CHECKSUMS",
            "CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES",
        ] + (["MISSING_LOCAL_FUNDING_MONTH_FILES"] if missing else []) + (["SCHEMA_OR_ROW_SANITY_FAILED"] if schema_bad else []),
        "next_action": "resolve missing/schema issues only from admissible local sources with provenance lineage; this audit is local-only and does not authorize outcomes",
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"out": str(out), "missing": len(missing), "schema_bad": len(schema_bad), "all_ok": report["summary"]["all_requested_present_and_schema_ok"], "network_used": False, "outcomes_computed": False}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
