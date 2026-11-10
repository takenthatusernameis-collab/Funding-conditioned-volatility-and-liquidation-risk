#!/usr/bin/env python3
"""Track C per-candidate deep-audit orchestrator (local-only, no outcomes, no network).

Deterministic scoped deep-audit driver for Track C confirmatory-resume readiness.
Consumes panel admissibility + gap/repair + funding-schema audit signals for
candidate windows only (--window-hint, comma-separated month hints such as
2024_10,2024_11,2024_12; NO full-cache scan unless explicitly justified).

Emits a consolidated machine-checkable blocker JSON:
  candidate window -> per symbol -> blockers, missing month/series ranges,
  funding schema status, provenance/checksum sidecar signals,
  confirmatory_resume_ready.

confirmatory_resume_ready is true ONLY when every verified prerequisite holds:
  >=5 symbols with required series complete vs mark-union days, >=3 non-overlapping
  30-day blocks, funding month files present + schema OK, adjacent sha256 provenance
  checksums verified, and a --prereg-hash pre-declared (prereg must be frozen before
  any outcome inspection). Otherwise false.

NO NETWORK. NO DOWNLOADS. NO OUTCOMES/TARGETS/FEATURES/MODELS. Does not satisfy
confirmatory resume by itself; it is the engineering watchdog that makes blockers
machine-checkable so the next session can either resume confirmatory work or stop
cleanly with evidence.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.trackc_panel_admissibility_audit import (  # noqa: E402
    collect_days,
    detect_provenance,
    funding_coverage,
    missing_day_ranges,
    non_overlapping_30d_blocks,
)
from scripts.trackc_funding_schema_audit import (  # noqa: E402
    audit_file,
    find_funding_file,
)

SYMS_DEFAULT = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
REQUIRED_SERIES = ("markPriceKlines", "indexPriceKlines", "premiumIndexKlines")
MONTH_RE = re.compile(r"^(\d{4})[-_](\d{2})$")


def _utc_now():
    env = os.environ.get("TRACKC_ORCHESTRATOR_UTC")
    if env:
        return env
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_month_hint(h):
    h = h.strip()
    m = MONTH_RE.match(h)
    if not m:
        raise ValueError(f"invalid month hint: {h!r} (expected YYYY-MM or YYYY_MM)")
    return f"{m.group(1)}-{m.group(2)}"


def _expand_hints(hints):
    return sorted({_parse_month_hint(h) for h in hints if h.strip()})


def _is_contiguous(months):
    if not months:
        return True

    def to_idx(m):
        y, mo = m.split("-")
        return int(y) * 12 + int(mo)

    idxs = sorted(to_idx(m) for m in months)
    return all(idxs[i] == idxs[i - 1] + 1 for i in range(1, len(idxs)))


def _verify_adjacent_sha256(paths):
    checked = 0
    ok = 0
    mismatches = []
    missing = 0
    for p in paths:
        sc = Path(str(p) + ".sha256")
        if not sc.exists():
            missing += 1
            continue
        checked += 1
        try:
            expected = sc.read_text(errors="ignore").strip().split()[0].lower()
            h = hashlib.sha256()
            with p.open("rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""):
                    h.update(chunk)
            got = h.hexdigest()
            if expected and got == expected:
                ok += 1
            else:
                mismatches.append(
                    {"file": str(p), "expected_prefix": expected[:16], "got_prefix": got[:16]}
                )
        except Exception as e:
            mismatches.append({"file": str(p), "error": str(e)[:120]})
    return {
        "checked": checked,
        "ok": ok,
        "mismatch": len(mismatches),
        "mismatch_samples": mismatches[:10],
        "files_without_adjacent_sha256_sidecar": missing,
    }


def _audit_symbol_window(cache, repo_root, sym, months):
    hints = [m.replace("-", "_") for m in months]
    days, series, has_funding_dir, has_klines_zip = collect_days(cache, sym, hints)
    n = len(days)
    blocks = non_overlapping_30d_blocks(n)

    series_gaps = {}
    required_ok = n > 0
    for s in REQUIRED_SERIES:
        missing, ranges = missing_day_ranges(series[s], days)
        complete = len(missing) == 0 and n > 0
        if not complete:
            required_ok = False
        series_gaps[s] = {
            "present_days": len(series[s]),
            "missing_days_vs_mark_union": len(missing),
            "missing_day_ranges": ranges,
            "missing_days_sample": missing[:120],
            "complete_vs_mark_union": complete,
        }

    funding = funding_coverage(cache, sym, days, None)
    expected_months = funding.get("funding_months_expected_for_range") or []
    overlap = set(funding.get("funding_months_overlap_expected") or [])
    missing_months = [m for m in expected_months if m not in overlap]

    funding_month_audits = {}
    funding_schema_ok = True
    funding_blockers = []
    if not expected_months:
        funding_flag = "NO_EXPECTED_MONTHS_FOR_RANGE"
    elif not missing_months:
        funding_flag = "MONTH_FILES_PRESENT"
    elif overlap:
        funding_flag = "PARTIAL_MONTH_FILES"
    else:
        funding_flag = "NO_MONTH_FILES_FOR_RANGE"
    if missing_months:
        funding_blockers.append("FUNDING_MONTH_FILES_MISSING_FOR_RANGE")

    for m in missing_months:
        funding_blockers.append("MISSING_FUNDING_MONTH_FILE")
        funding_month_audits[m] = {
            "local_present": False,
            "schema_ok": False,
            "files": [],
            "blockers": ["MISSING_LOCAL_FUNDING_MONTH_FILE"],
        }

    for m in sorted(set(expected_months) & overlap):
        found = find_funding_file(repo_root, cache, sym, m)
        audits = [audit_file(p, m) for p in found[:3]]
        ok = any(a["schema_ok"] for a in audits)
        if not ok:
            funding_schema_ok = False
            funding_blockers.append("SCHEMA_OR_ROW_SANITY_FAILED")
        funding_month_audits[m] = {
            "local_present": bool(found),
            "schema_ok": ok,
            "files": [a["path"] for a in audits],
            "sha256": [a["sha256"] for a in audits],
            "adjacent_sha256_sidecar_present": [
                a["adjacent_sha256_sidecar_present"] for a in audits
            ],
            "blockers": [] if ok else ["SCHEMA_OR_ROW_SANITY_FAILED"],
        }

    # Provenance: adjacent sha256 sidecars for cache-resident candidate files
    # (series csvs + funding files under the local cache window). repo_root-located
    # files are context for schema audit only and must not pollute provenance.
    csv_paths = []
    for m in months:
        d = cache / f"{sym}_{m.replace('-', '_')}"
        if d.exists():
            csv_paths.extend(sorted(d.rglob("*.csv")))
    found_funding = []
    for m in months:
        found_funding.extend(find_funding_file(repo_root, cache, sym, m))
    provenance_paths = [p for p in (csv_paths + found_funding) if cache in p.parents]
    provenance = _verify_adjacent_sha256(provenance_paths)
    provenance_verified = (
        provenance["mismatch"] == 0
        and provenance["files_without_adjacent_sha256_sidecar"] == 0
        and provenance["checked"] >= 1
    )

    blockers = []
    if not required_ok:
        blockers.append("REQUIRED_SERIES_GAPS_OR_MISSING")
    if missing_months:
        blockers.append("MISSING_FUNDING_MONTH_FILE")
    funding_blockers_set = set(funding_blockers)
    if funding_blockers_set:
        blockers.extend(sorted(funding_blockers_set))
    if not funding_schema_ok:
        blockers.append("SCHEMA_OR_ROW_SANITY_FAILED")
    if not provenance_verified:
        blockers.append("PROVENANCE_NOT_MACHINE_VERIFIED")

    return {
        "symbol": sym,
        "months": months,
        "days": n,
        "range": [days[0], days[-1]] if days else None,
        "non_overlapping_30d_blocks": blocks,
        "required_series_complete": required_ok,
        "series_day_counts": {k: len(v) for k, v in series.items()},
        "series_gaps": series_gaps,
        "has_funding_files_detected": has_funding_dir,
        "has_1h_klines_zip_detected": has_klines_zip,
        "funding": {
            "flag": funding_flag,
            "months_expected_for_range": expected_months,
            "months_overlap_expected": sorted(overlap),
            "months_missing_for_range": missing_months,
            "funding_rows_in_day_range": funding.get("funding_rows_in_day_range"),
            "funding_distinct_days_detected": funding.get("funding_distinct_days_detected"),
            "funding_slot_coverage_diagnostic": funding.get("funding_slot_coverage_diagnostic"),
        },
        "funding_month_audits": funding_month_audits,
        "funding_schema_ok": funding_schema_ok,
        "provenance": provenance,
        "provenance_verified": provenance_verified,
        "blockers": sorted(set(blockers)),
        "confirmatory_ready_symbol": False,
    }


def _assemble_candidate(cache, repo_root, symbols, months, min_symbols, min_blocks, prereg_hash):
    per_symbol = {}
    symbols_ok = 0
    min_days = None
    all_required_complete = True
    any_funding_missing = False
    all_funding_schema_ok = True
    provenance_verified_all = True
    provenance_any_checked = False

    for sym in symbols:
        rep = _audit_symbol_window(cache, repo_root, sym, months)
        per_symbol[sym] = rep
        if rep["required_series_complete"]:
            symbols_ok += 1
            min_days = rep["days"] if min_days is None else min(min_days, rep["days"])
        else:
            all_required_complete = False
        if rep["funding"]["months_missing_for_range"]:
            any_funding_missing = True
        if not rep["funding_schema_ok"]:
            all_funding_schema_ok = False
        if not rep["provenance_verified"]:
            provenance_verified_all = False
        if rep["provenance"]["checked"] >= 1:
            provenance_any_checked = True

    panel_blocks = non_overlapping_30d_blocks(min_days or 0)
    provenance_verified = provenance_verified_all and provenance_any_checked

    tech_ok = (
        symbols_ok >= min_symbols
        and panel_blocks >= min_blocks
        and all_required_complete
        and not any_funding_missing
        and all_funding_schema_ok
        and provenance_verified
    )
    confirmatory_resume_ready = tech_ok and prereg_hash is not None

    blockers = []
    if symbols_ok < min_symbols:
        blockers.append("INSUFFICIENT_SYMBOLS_FOR_CONFIRMATORY")
    if panel_blocks < min_blocks:
        blockers.append("INSUFFICIENT_30D_BLOCKS_FOR_CONFIRMATORY")
    if not all_required_complete:
        blockers.append("REQUIRED_SERIES_GAPS_OR_MISSING")
    if any_funding_missing:
        blockers.append("MISSING_FUNDING_MONTH_FILE")
    if not all_funding_schema_ok:
        blockers.append("SCHEMA_OR_ROW_SANITY_FAILED")
    if not provenance_verified:
        blockers.append("PROVENANCE_NOT_MACHINE_VERIFIED")
    if prereg_hash is None:
        blockers.append("CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES")
    blockers.append("CONFIRMATORY_REQUIRES_VERIFIED_PROVENANCE_CHECKSUMS")

    return {
        "months": months,
        "month_count": len(months),
        "contiguous": _is_contiguous(months),
        "symbols": symbols,
        "symbols_ok": symbols_ok,
        "min_complete_symbol_days": min_days or 0,
        "panel_non_overlapping_30d_blocks_estimate": panel_blocks,
        "all_required_series_complete": all_required_complete,
        "any_funding_month_missing": any_funding_missing,
        "all_funding_schema_ok": all_funding_schema_ok,
        "provenance_verified": provenance_verified,
        "prereg_hash": prereg_hash,
        "confirmatory_resume_ready": confirmatory_resume_ready,
        "blockers": sorted(set(blockers)),
        "per_symbol": per_symbol,
    }


def main():
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--cache", default="research_state/data_cache")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--symbols", default=",".join(SYMS_DEFAULT))
    ap.add_argument("--window-hint", required=True, help="comma-separated month hints (YYYY-MM or YYYY_MM) defining ONE candidate window, e.g. 2024_10,2024_11,2024_12")
    ap.add_argument("--min-symbols", type=int, default=5)
    ap.add_argument("--min-blocks", type=int, default=3)
    ap.add_argument("--prereg-hash", default=None, help="SHA256 of frozen preregistration (required for confirmatory_resume_ready=true)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    cache = (repo_root / args.cache).resolve() if not Path(args.cache).is_absolute() else Path(args.cache)
    symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
    months = _expand_hints(args.window_hint.split(","))
    prereg_hash = args.prereg_hash.strip() if args.prereg_hash else None

    candidate = _assemble_candidate(cache, repo_root, symbols, months, args.min_symbols, args.min_blocks, prereg_hash)

    report = {
        "generated_utc": _utc_now(),
        "mode": "local_only_scoped_deep_audit_no_outcomes_no_network",
        "cache": str(cache),
        "repo_root": str(repo_root),
        "symbols": symbols,
        "window_hints": args.window_hint,
        "candidate_months": months,
        "min_symbols": args.min_symbols,
        "min_blocks": args.min_blocks,
        "prereg_hash": prereg_hash,
        "candidate": candidate,
        "summary": {
            "candidates_evaluated": 1,
            "confirmatory_resume_ready": candidate["confirmatory_resume_ready"],
            "provenance_verified": candidate["provenance_verified"],
            "any_funding_month_missing": candidate["any_funding_month_missing"],
            "all_required_series_complete": candidate["all_required_series_complete"],
            "panel_blocks_estimate": candidate["panel_non_overlapping_30d_blocks_estimate"],
            "symbols_ok": candidate["symbols_ok"],
            "locally_repairable_series_gaps_detected": False,
            "network_used": False,
            "outcomes_computed": False,
        },
        "blockers_global": sorted(set(candidate["blockers"])),
        "next_action": (
            "freeze new prereg before outcomes; verify funding schema/coverage/provenance/checksums; "
            "repair/manifest series gaps deterministically from locally present admissible files; "
            "no confirmatory outcomes until confirmatory_resume_ready=true"
            if not candidate["confirmatory_resume_ready"]
            else "confirmatory prerequisites met: freeze/record prereg hash, materialize panel + chronological splits (7-day purge/embargo), run confirmatory pipeline"
        ),
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "out": str(out),
                "confirmatory_resume_ready": report["summary"]["confirmatory_resume_ready"],
                "provenance_verified": report["summary"]["provenance_verified"],
                "symbols_ok": report["summary"]["symbols_ok"],
                "panel_blocks_estimate": report["summary"]["panel_blocks_estimate"],
                "blockers_global": report["blockers_global"],
                "network_used": False,
                "outcomes_computed": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
