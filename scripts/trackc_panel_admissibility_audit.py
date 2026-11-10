
"""Track C resume-trigger / panel admissibility + gap/provenance audit.

Dep-light, stdlib-only, NO NETWORK, NO OUTCOMES/TARGETS/FEATURES/MODELS.

Checks cached panel fragments against FCLR-014 confirmatory resume trigger:
  - >=5 symbols
  - >=3 non-overlapping 30-day OOS blocks (calendar days, contiguous coverage heuristic)
  - required series dirs/files present (mark/index/premium)
Emits machine-checkable gap manifests (missing day ranges per series vs mark days),
funding completeness/provenance signals, and deterministic sidecar/checksum detection.
This does NOT satisfy prereg resume alone (frozen prereg-before-outcomes + verified
funding/provenance/checksums still required).

Usage:
  python scripts/trackc_panel_admissibility_audit.py \
    [--cache research_state/data_cache] \
    [--symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT] \
    [--window-hint 2026_11] \
    [--out research_state/trackc_panel_admissibility_latest.json]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

try:
    from scripts.trackc_provenance_lineage import verify_paths_with_manifests
except Exception:  # pragma: no cover
    verify_paths_with_manifests = None

SYMS_DEFAULT = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
REQUIRED_SERIES = ["markPriceKlines", "indexPriceKlines", "premiumIndexKlines"]
MAX_MISSING_DAYS_LISTED = 120
MAX_MISSING_RANGES_LISTED = 60


def _parse_day(s: str) -> datetime | None:
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except Exception:
        return None


def missing_day_ranges(days_present: list[str], ref_days: list[str]):
    ref = set(ref_days)
    pres = set(days_present)
    missing = sorted(ref - pres)
    ranges = []
    i = 0
    while i < len(missing):
        start = missing[i]
        prev = _parse_day(start)
        j = i
        while j + 1 < len(missing):
            cur = _parse_day(missing[j + 1])
            if prev and cur and (cur - prev).days == 1:
                prev = cur
                j += 1
            else:
                break
        ranges.append([missing[i], missing[j]])
        i = j + 1
    return missing, ranges


def month_keys_for_range(start_day: str | None, end_day: str | None):
    if not start_day or not end_day:
        return []
    s = _parse_day(start_day)
    e = _parse_day(end_day)
    if not s or not e or e < s:
        return []
    out = []
    y, m = s.year, s.month
    while (y, m) <= (e.year, e.month):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            m = 1
            y += 1
    return out


def find_funding_files(cache: Path, sym: str, window_hint: str | None = None):
    files = []
    roots = [cache, cache.parent.parent]  # research_state/data_cache and repo root
    seen = set()
    for root in roots:
        if not root.exists():
            continue
        pats = [f"**/{sym}-fundingRate-*.csv", f"**/{sym}*fundingRate*.csv"]
        for pat in pats:
            for p in root.glob(pat):
                rp = p.resolve()
                if rp in seen:
                    continue
                seen.add(rp)
                rel = str(p)
                if window_hint and window_hint not in rel and root == cache:
                    # include root-level historical funding even with window hint for context,
                    # but prefer window-matching cache files
                    pass
                files.append(p)
    return sorted(files)


def funding_coverage(cache: Path, sym: str, ref_days: list[str], window_hint: str | None = None):
    files = find_funding_files(cache, sym, window_hint)
    months_expected = month_keys_for_range(ref_days[0] if ref_days else None, ref_days[-1] if ref_days else None)
    month_files = {}
    rows_in_range = 0
    funding_days = set()
    ref_set = set(ref_days)
    ref_start = _parse_day(ref_days[0]) if ref_days else None
    ref_end = _parse_day(ref_days[-1]) if ref_days else None
    for p in files:
        m = re.search(r"(\d{4}-\d{2})", p.name)
        if m:
            month_files.setdefault(m.group(1), []).append(str(p))
        try:
            with p.open("r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ct = row.get("calc_time") or row.get("calcTime") or row.get("fundingTime")
                    if not ct:
                        continue
                    try:
                        ms = int(float(ct))
                    except Exception:
                        continue
                    dt = datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc)
                    day = dt.strftime("%Y-%m-%d")
                    funding_days.add(day)
                    if ref_start and ref_end and ref_start <= dt.replace(tzinfo=None) <= ref_end.replace(hour=23, minute=59, second=59):
                        if not ref_set or day in ref_set or (ref_days[0] <= day <= ref_days[-1]):
                            rows_in_range += 1
        except Exception:
            # unreadable/unexpected format: report file presence only
            pass
    months_found = sorted(month_files.keys())
    slot_cov = funding_slot_coverage(files, ref_days)
    months_overlap = [m for m in months_expected if m in month_files] if months_expected else months_found
    if not files:
        flag = "MISSING"
    elif months_expected and len(months_overlap) == len(months_expected):
        flag = "MONTH_FILES_PRESENT"
    elif months_expected and months_overlap:
        flag = "PARTIAL_MONTH_FILES"
    elif months_expected and not months_overlap:
        flag = "NO_MONTH_FILES_FOR_RANGE"
    else:
        flag = "FILES_PRESENT"
    return {
        "funding_csv_files_found": len(files),
        "funding_csv_paths_sample": [str(p) for p in files[:12]],
        "funding_months_expected_for_range": months_expected,
        "funding_months_found": months_found,
        "funding_months_overlap_expected": months_overlap,
        "funding_rows_in_day_range": rows_in_range,
        "funding_distinct_days_detected": len(funding_days),
        "funding_completeness_flag": flag,
        "funding_slot_coverage_diagnostic": slot_cov,
        "funding_note": "Monthly funding files are 8h observations; MONTH_FILES_PRESENT means month coverage files exist for the day range, not day-level parity proof. funding_slot_coverage_diagnostic is heuristic only. Verify schema/provenance/checksums before confirmatory use.",
    }


def detect_provenance(cache: Path, repo_root: Path | None = None):
    root = (repo_root or cache.parent.parent).resolve()
    roots = [cache, cache.parent, cache.parent.parent]
    sidecars = {"sha256": [], "checksum": [], "etag": [], "provenance_json": []}
    seen = set()
    for r in roots:
        if not r.exists():
            continue
        patterns = [
            ("sha256", "**/*.sha256"),
            ("checksum", "**/*.CHECKSUM"),
            ("checksum", "**/*.checksum"),
            ("etag", "**/*.etag"),
            ("provenance_json", "**/*provenance*.json"),
        ]
        for kind, pat in patterns:
            for p in r.glob(pat):
                rp = str(p.resolve())
                if rp in seen or ".git" in rp:
                    continue
                seen.add(rp)
                sidecars[kind].append(str(p))
    for k in sidecars:
        sidecars[k] = sorted(sidecars[k])[:40]
    present = any(sidecars[k] for k in sidecars)
    sample_files = []
    for pat in ["**/*.csv", "**/*.zip"]:
        for fp in cache.glob(pat):
            sample_files.append(fp)
            if len(sample_files) >= 40:
                break
        if len(sample_files) >= 40:
            break
    sha_verify = verify_sha256_sidecars(sorted(set(sample_files)), limit=25, repo_root=root)
    run_manifest = cache.parent / "run_manifest.json"
    manifest_has_hashes = False
    if run_manifest.exists():
        try:
            mtxt = run_manifest.read_text(errors="ignore")
            manifest_has_hashes = ("sha256" in mtxt.lower()) or ("checksum" in mtxt.lower()) or ("etag" in mtxt.lower())
        except Exception:
            pass
    return {
        "provenance_sidecars_present": present,
        "run_manifest_has_hash_fields": manifest_has_hashes,
        "sidecar_counts": {k: len(v) for k, v in sidecars.items()},
        "sidecar_paths_sample": {k: v[:10] for k, v in sidecars.items() if v},
        "adjacent_sha256_verification_sample": sha_verify,
        "manifest_lineage_ingest": sha_verify.get("manifest_ingest", {}),
        "provenance_verified_sample": sha_verify.get("provenance_verified", False),
        "provenance_source_counts_sample": sha_verify.get("provenance_source_counts", {}),
        "provenance_checked": sha_verify.get("checked_with_hash_source", sha_verify.get("sidecars_checked", 0)),
        "provenance_ok": sha_verify.get("verified_count", sha_verify.get("sidecars_ok", 0)),
        "provenance_mismatch": sha_verify.get("mismatch_count", sha_verify.get("sidecars_mismatch", 0)),
        "provenance_unmapped": sha_verify.get("unmapped_count", sha_verify.get("files_without_adjacent_sha256_sidecar", 0)),
        "provenance_source": sha_verify.get("provenance_source", "none"),
        "provenance_note": "Deterministic local detection: adjacent sidecars and/or unambiguous manifest path+sha256 lineage where content hash matches. No network. Presence/URLs alone do not prove provenance; absence of verifiable hash match means not machine-verified.",
    }



def funding_slot_coverage(files: list[Path], ref_days: list[str]):
    """Diagnostic only: 8h funding => up to 3 slots/day; report observed slots vs heuristic.
    Not a completeness proof; monthly files may be complete while day boundaries vary."""
    if not ref_days:
        return {"status": "NO_REF_DAYS", "slots_observed": 0, "expected_slots_heuristic": 0}
    ref_set = set(ref_days)
    slots = set()
    for p in files:
        try:
            with p.open("r", newline="") as f:
                for row in csv.DictReader(f):
                    ct = row.get("calc_time") or row.get("calcTime") or row.get("fundingTime")
                    if not ct:
                        continue
                    try:
                        ms = int(float(ct))
                    except Exception:
                        continue
                    dt = datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc)
                    day = dt.strftime("%Y-%m-%d")
                    if day in ref_set:
                        slots.add((day, dt.hour))
        except Exception:
            pass
    expected = len(ref_days) * 3
    obs = len(slots)
    ratio = (obs / expected) if expected else None
    # heuristic status only
    if expected == 0:
        status = "NO_REF_DAYS"
    elif obs == 0:
        status = "NO_SLOTS_IN_RANGE"
    elif ratio is not None and ratio >= 0.9:
        status = "HEURISTIC_DENSE"
    elif ratio is not None and ratio >= 0.5:
        status = "HEURISTIC_PARTIAL"
    else:
        status = "HEURISTIC_SPARSE"
    return {
        "status": status,
        "slots_observed": obs,
        "expected_slots_heuristic": expected,
        "coverage_ratio_heuristic": round(ratio, 6) if ratio is not None else None,
        "note": "Heuristic only (3x8h/day). Funding schedule/partial days/window edges can make this differ from true completeness. Use for gap planning, not confirmatory proof.",
    }


def verify_sha256_sidecars(paths: list[Path], limit: int = 25, repo_root: Path | None = None):
    """Deterministic local verification: adjacent *.sha256 sidecars and/or unambiguous
    local manifest path+sha256 lineage (manifest_extended/manifest_extract). No network.
    URL/manifest presence alone is not verification without content hash match."""
    root = repo_root.resolve() if repo_root else Path(".").resolve()
    if verify_paths_with_manifests is not None:
        res = verify_paths_with_manifests(paths, repo_root=root, limit=limit)
        # backward-compatible fields expected by prior consumers/tests
        res.update({
            "files_considered": res.get("files_considered", min(len(paths), limit)),
            "sidecars_checked": res.get("checked_with_hash_source", 0),
            "sidecars_ok": res.get("verified_count", 0),
            "sidecars_mismatch": res.get("mismatch_count", 0),
            "mismatch_samples": res.get("mismatch_samples", []),
            "files_without_adjacent_sha256_sidecar": res.get("unmapped_count", 0),
            "adjacent_or_manifest_verified": res.get("verified_count", 0),
            "provenance_source": "mixed" if len(res.get("provenance_source_counts", {})) > 1 else (next(iter(res.get("provenance_source_counts", {})), "none")),
        })
        return res
    # fallback: sidecar-only (legacy)
    checked = 0
    ok = 0
    mismatches = []
    missing_hash_for_file = 0
    for p in paths[:limit]:
        sc = Path(str(p) + ".sha256")
        if not sc.exists():
            alt = p.with_suffix(p.suffix + ".sha256")
            sc = alt if alt.exists() else sc
        if not sc.exists():
            missing_hash_for_file += 1
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
                mismatches.append({"file": str(p), "expected_prefix": expected[:16], "got_prefix": got[:16]})
        except Exception as e:
            mismatches.append({"file": str(p), "error": str(e)[:120]})
    return {
        "files_considered": min(len(paths), limit),
        "sidecars_checked": checked,
        "sidecars_ok": ok,
        "sidecars_mismatch": len(mismatches),
        "mismatch_samples": mismatches[:10],
        "files_without_adjacent_sha256_sidecar": missing_hash_for_file,
        "provenance_verified": ok > 0 and ok == min(len(paths), limit) and len(mismatches) == 0 and missing_hash_for_file == 0,
        "provenance_source_counts": {"adjacent_sidecar": ok} if ok else {},
        "provenance_source": "adjacent_sidecar" if ok else "none",
        "manifest_ingest": {"manifests_loaded": [], "manifests_missing": [], "records_indexed": 0},
        "verification_note": "Local deterministic check only for adjacent *.sha256 sidecars. No network. Does not prove provenance origin; only content hash match when sidecar exists.",
    }


def _hint_matches(name: str, window_hints: list[str] | str | None) -> bool:
    """OR-semantics: a dir matches if any hint is a substring of its name. None/empty => match all."""
    if not window_hints:
        return True
    if isinstance(window_hints, str):
        window_hints = [window_hints]
    return any(h and h in name for h in window_hints)


def collect_days(cache: Path, sym: str, window_hints: list[str] | str | None = None):
    days = set()
    series = {k: set() for k in REQUIRED_SERIES}
    has_funding = False
    has_klines_zip = False
    for d in sorted(cache.glob(f"{sym}_*")):
        if not d.is_dir():
            continue
        if not _hint_matches(d.name, window_hints):
            continue
        for child in d.rglob("*.csv"):
            m = re.search(r"(\d{4}-\d{2}-\d{2})", child.as_posix())
            if not m:
                continue
            day = m.group(1)
            days.add(day)
            posix = child.as_posix().lower()
            if "indexpriceklines" in posix:
                series["indexPriceKlines"].add(day)
            if "markpriceklines" in posix:
                series["markPriceKlines"].add(day)
            if "premiumindexklines" in posix:
                series["premiumIndexKlines"].add(day)
        if list(d.rglob("*funding*.csv")) or list(d.rglob("*fundingRate*")):
            has_funding = True
        if list(d.rglob(f"{sym}-1h-*.zip")):
            has_klines_zip = True
    return sorted(days), {k: sorted(v) for k, v in series.items()}, has_funding, has_klines_zip


def non_overlapping_30d_blocks(n_days: int) -> int:
    return max(0, int(n_days)) // 30


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="research_state/data_cache")
    ap.add_argument("--symbols", default=",".join(SYMS_DEFAULT))
    ap.add_argument("--window-hint", default=None, help="substring filter for sym dirs, e.g. 2026_11. May be repeated/comma-separated for OR-semantics across a candidate window.")
    ap.add_argument("--out", default="research_state/trackc_panel_admissibility_latest.json")
    args = ap.parse_args()
    cache = Path(args.cache)
    syms = [s.strip() for s in args.symbols.split(",") if s.strip()]
    hints = [h.strip() for h in args.window_hint.split(",") if h.strip()] if args.window_hint else None
    per = {}
    all_ok_syms = 0
    min_days = None
    for sym in syms:
        days, series, has_funding, has_klines = collect_days(cache, sym, hints)
        n = len(days)
        blocks = non_overlapping_30d_blocks(n)
        series_gaps = {}
        required_ok = n > 0
        for s in REQUIRED_SERIES:
            missing, ranges = missing_day_ranges(series[s], days)
            series_gaps[s] = {
                "present_days": len(series[s]),
                "missing_days_vs_mark_union": len(missing),
                "missing_day_ranges": ranges[:MAX_MISSING_RANGES_LISTED],
                "missing_days_sample": missing[:MAX_MISSING_DAYS_LISTED],
                "complete_vs_mark_union": len(missing) == 0 and n > 0,
            }
            if not series_gaps[s]["complete_vs_mark_union"]:
                required_ok = False
        funding = funding_coverage(cache, sym, days, args.window_hint)
        funding_months_ok = (not funding["funding_months_expected_for_range"]) or funding["funding_completeness_flag"] in ("MONTH_FILES_PRESENT",)
        sym_ok = required_ok  # required series only; confirmatory also needs funding/provenance/prereg
        if sym_ok:
            all_ok_syms += 1
            min_days = n if min_days is None else min(min_days, n)
        per[sym] = {
            "days": n,
            "range": [days[0], days[-1]] if days else None,
            "non_overlapping_30d_blocks": blocks,
            "required_series_complete": required_ok,
            "series_day_counts": {k: len(v) for k, v in series.items()},
            "series_gap_manifest": series_gaps,
            "has_funding_files_detected": has_funding or funding["funding_csv_files_found"] > 0,
            "has_1h_klines_zip_detected": has_klines,
            "funding_coverage": funding,
            "funding_month_files_complete_for_range": funding_months_ok,
            "resume_trigger_symbol_ok": sym_ok,
            "confirmatory_ready_symbol": False,  # always false in audit: requires verified funding/provenance/checksums + frozen prereg-before-outcomes
        }
    panel_blocks = non_overlapping_30d_blocks(min_days or 0)
    meets = all_ok_syms >= 5 and panel_blocks >= 3
    provenance = detect_provenance(cache, repo_root=cache.parent.parent)
    report = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cache": str(cache),
        "window_hint": args.window_hint,
        "window_hints_resolved": hints,
        "symbols": syms,
        "per_symbol": per,
        "symbols_with_required_series": all_ok_syms,
        "min_complete_symbol_days": min_days or 0,
        "panel_non_overlapping_30d_blocks_estimate": panel_blocks,
        "resume_trigger_met": meets,
        "resume_trigger_rule": ">=5 symbols with required series complete vs mark-union days AND >=3 non-overlapping 30d blocks (estimate). Funding completeness/provenance/checksums + frozen prereg-before-outcomes still required before confirmatory resume.",
        "confirmatory_resume_ready": False,
        "provenance_audit": provenance,
        "outcomes_computed": False,
        "network_used": False,
        "next_action_if_met": "freeze new prereg version before any outcome inspection; verify funding schema/coverage/provenance/checksums; repair/manifest any series gaps deterministically; materialize splits/manifest; run confirmatory pipeline with block-bootstrap/Holm per protocol",
        "next_action_if_not_met": "no confirmatory outcomes; use series_gap_manifest/funding_coverage for deterministic local repair planning; continue resume-trigger watch (no default probing); keep dep-light gates green",
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    summary = {"out": str(out), "resume_trigger_met": meets, "panel_blocks": panel_blocks, "symbols_ok": all_ok_syms, "outcomes_computed": False, "network_used": False}
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
