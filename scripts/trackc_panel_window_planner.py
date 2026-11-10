#!/usr/bin/env python3
"""Track C deterministic local-only panel-window planner/ranker.

Dep-light, stdlib-only, NO NETWORK, NO OUTCOMES/TARGETS/FEATURES/MODELS.
Scans cached SYMBOL_YYYY_MM windows using fast local existence/count signals
(no full CSV reads) and emits a machine-checkable ranked table of candidate
contiguous multi-month panels with coverage/block estimates and explicit
blockers. Optional --deep mode uses full admissibility helpers (slower).

This does NOT download, probe, compute outcomes, or satisfy confirmatory resume.
Confirmatory resume still requires: admissible >=5-symbol/>=3-block panel with
verified funding+provenance+checksums, and a NEW frozen prereg before outcomes.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

SYMS_DEFAULT = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
WINDOW_RE = re.compile(r"^([A-Z0-9]+USDT)_(\d{4})_(\d{2})$")
REQUIRED_SERIES = ("markPriceKlines", "indexPriceKlines", "premiumIndexKlines")


def discover_windows(cache: Path, symbols: list[str]):
    by_month: dict[str, dict[str, Path]] = defaultdict(dict)
    symset = set(symbols)
    if not cache.exists():
        return by_month
    for d in cache.iterdir():
        if not d.is_dir():
            continue
        m = WINDOW_RE.match(d.name)
        if not m:
            continue
        sym, y, mo = m.group(1), m.group(2), m.group(3)
        if sym in symset:
            by_month[f"{y}-{mo}"][sym] = d
    return dict(sorted(by_month.items()))


def _count_series_day_dirs(wdir: Path, series: str):
    # fast: count dirs like series-1h-YYYY-MM-*
    pat = re.compile(rf"^{re.escape(series)}.*(\d{{4}}-\d{{2}}-\d{{2}})")
    days = set()
    if not wdir.exists():
        return 0, set()
    try:
        for child in wdir.iterdir():
            if child.is_dir():
                m = pat.match(child.name)
                if m:
                    days.add(m.group(1))
            elif child.suffix == ".csv":
                m = re.search(r"(\d{4}-\d{2}-\d{2})", child.name)
                if series.lower().replace("klines", "") in child.name.lower() and m:
                    days.add(m.group(1))
    except Exception:
        pass
    return len(days), days


def audit_window_fast(cache: Path, repo_root: Path, sym: str, month_key: str, window_hint: str):
    wdir = cache / f"{sym}_{window_hint}"
    day_counts = {}
    all_mark_days = set()
    required_ok = True
    for s in REQUIRED_SERIES:
        n, days = _count_series_day_dirs(wdir, s)
        day_counts[s] = n
        if s == "markPriceKlines":
            all_mark_days = days
        if n == 0:
            required_ok = False
    # if mark exists, check others cover mark days (fast set compare)
    series_complete = {}
    if all_mark_days:
        for s in REQUIRED_SERIES:
            _, days = _count_series_day_dirs(wdir, s)
            missing = len(all_mark_days - days)
            series_complete[s] = missing == 0
            if missing != 0:
                required_ok = False
    else:
        for s in REQUIRED_SERIES:
            series_complete[s] = day_counts[s] > 0
        required_ok = all(series_complete.values()) and sum(day_counts.values()) > 0
    # funding month file presence (local existence only)
    fname = f"{sym}-fundingRate-{month_key}.csv"
    funding_paths = []
    for root in (cache, repo_root):
        for p in root.glob(f"**/{fname}"):
            if "/.git/" not in str(p):
                funding_paths.append(str(p))
    funding_paths = sorted(set(funding_paths))
    funding_ok = bool(funding_paths)
    has_klines = any(wdir.glob(f"{sym}-1h-*.zip")) if wdir.exists() else False
    blockers = []
    if not required_ok:
        blockers.append("REQUIRED_SERIES_GAPS_OR_MISSING")
    if not funding_ok:
        blockers.append("MISSING_FUNDING_MONTH_FILE")
    blockers.append("PROVENANCE_NOT_MACHINE_VERIFIED")
    blockers.append("SCHEMA_NOT_VERIFIED_IN_FAST_MODE")
    return {
        "symbol": sym,
        "month": month_key,
        "window_hint": window_hint,
        "series_day_dir_counts": day_counts,
        "required_series_complete_fast": required_ok,
        "series_complete_vs_mark_fast": series_complete,
        "funding_month_file_present_locally": funding_ok,
        "funding_month_file_paths_sample": funding_paths[:3],
        "has_1h_klines_zip_detected": has_klines,
        "blockers": blockers,
        "confirmatory_ready_symbol_window": False,
        "mode": "fast",
    }


def contiguous_sequences(months: list[str]):
    if not months:
        return []
    out = []
    def to_idx(m):
        y, mo = m.split("-")
        return int(y) * 12 + int(mo)
    def from_idx(o):
        y = (o - 1) // 12
        mo = (o - 1) % 12 + 1
        return f"{y:04d}-{mo:02d}"
    ords = sorted(to_idx(m) for m in months)
    cur = [ords[0]]
    for o in ords[1:]:
        if o == cur[-1] + 1:
            cur.append(o)
        else:
            out.append([from_idx(x) for x in cur])
            cur = [o]
    out.append([from_idx(x) for x in cur])
    return out


def rank_candidates(by_month_audits, symbols, min_symbols, min_blocks):
    full_months = [m for m, s in sorted(by_month_audits.items()) if all(sym in s for sym in symbols)]
    seqs = contiguous_sequences(full_months)
    candidates = []
    for seq in seqs:
        total_days_min = None
        all_series_ok = True
        all_funding_ok = True
        blockers = set()
        sym_rows = {}
        n_sym_months = 0
        n_complete_sym_months = 0
        for sym in symbols:
            rows = [by_month_audits[m][sym] for m in seq]
            # fast estimate: min series day dirs across required series, summed
            day_est = sum(min((r["series_day_dir_counts"].get(s, 0) for s in REQUIRED_SERIES), default=0) for r in rows)
            series_ok = all(r["required_series_complete_fast"] for r in rows)
            funding_ok = all(r["funding_month_file_present_locally"] for r in rows)
            total_days_min = day_est if total_days_min is None else min(total_days_min, day_est)
            n_sym_months += len(rows)
            n_complete_sym_months += sum(1 for r in rows if r["required_series_complete_fast"] and r["funding_month_file_present_locally"])
            if not series_ok:
                all_series_ok = False
                blockers.add("REQUIRED_SERIES_GAPS_IN_SEQUENCE")
            if not funding_ok:
                all_funding_ok = False
                blockers.add("FUNDING_GAPS_IN_SEQUENCE")
            sym_rows[sym] = {
                "estimated_days_sum_fast": day_est,
                "all_required_series_complete_fast": series_ok,
                "all_funding_month_ok": funding_ok,
            }
        blocks_est = max(0, int(total_days_min or 0)) // 30
        blockers.update(["PROVENANCE_NOT_MACHINE_VERIFIED", "CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES", "SCHEMA_NOT_VERIFIED_IN_FAST_MODE"])
        meets_structure = len(symbols) >= min_symbols and blocks_est >= min_blocks
        meets_local_data = meets_structure and all_series_ok and all_funding_ok
        completeness_ratio = (n_complete_sym_months / n_sym_months) if n_sym_months else 0.0
        candidates.append({
            "months": seq, "month_count": len(seq), "symbols": symbols,
            "min_symbol_estimated_days_sum_fast": total_days_min or 0,
            "estimated_non_overlapping_30d_blocks_fast": blocks_est,
            "all_required_series_complete_fast": all_series_ok,
            "all_funding_month_ok": all_funding_ok,
            "symbol_months_total_fast": n_sym_months,
            "symbol_months_complete_fast": n_complete_sym_months,
            "completeness_ratio_fast": round(completeness_ratio, 6),
            "meets_structural_thresholds_estimate_fast": meets_structure,
            "meets_local_data_signals_fast": meets_local_data,
            "confirmatory_resume_ready": False,
            "blockers": sorted(blockers),
            "per_symbol_summary": sym_rows,
        })
    # Rank: completeness-first. A larger window that is incomplete must NOT outrank
    # a smaller window that is complete; previously the tiebreak on raw block count
    # promoted the biggest incomplete window to rank 1.
    candidates.sort(key=lambda c: (
        0 if c["meets_local_data_signals_fast"] else 1,
        0 if c["meets_structural_thresholds_estimate_fast"] else 1,
        -c["completeness_ratio_fast"],
        -c["estimated_non_overlapping_30d_blocks_fast"],
        -c["min_symbol_estimated_days_sum_fast"],
        -c["month_count"], c["months"][0]))
    for i, c in enumerate(candidates, 1):
        c["rank"] = i
    return candidates, full_months


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="research_state/data_cache")
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--symbols", default=",".join(SYMS_DEFAULT))
    ap.add_argument("--min-symbols", type=int, default=5)
    ap.add_argument("--min-blocks", type=int, default=3)
    ap.add_argument("--max-candidates", type=int, default=25)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    repo_root = Path(args.repo_root).resolve()
    cache = (repo_root / args.cache).resolve() if not Path(args.cache).is_absolute() else Path(args.cache)
    symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
    by_month = discover_windows(cache, symbols)
    by_month_audits = {}
    for month, sym_dirs in by_month.items():
        wh = month.replace("-", "_")
        by_month_audits[month] = {}
        for sym in symbols:
            if sym in sym_dirs:
                by_month_audits[month][sym] = audit_window_fast(cache, repo_root, sym, month, wh)
    candidates, full_months = rank_candidates(by_month_audits, symbols, args.min_symbols, args.min_blocks)
    report = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": "fast_local_existence_only_no_csv_reads",
        "cache": str(cache), "repo_root": str(repo_root), "symbols": symbols,
        "min_symbols": args.min_symbols, "min_blocks_estimate": args.min_blocks,
        "months_discovered": sorted(by_month.keys()),
        "months_with_all_symbols_present": full_months,
        "window_audits_fast": by_month_audits,
        "candidates_ranked": candidates[: args.max_candidates],
        "candidate_count_total": len(candidates),
        "summary": {
            "any_meets_local_data_signals_fast": any(c["meets_local_data_signals_fast"] for c in candidates),
            "best_candidate": candidates[0] if candidates else None,
            "best_complete_candidate": next((c for c in candidates if c["meets_local_data_signals_fast"]), None),
            "best_complete_candidate_months": (next((c for c in candidates if c["meets_local_data_signals_fast"]), None) or {}).get("months"),
            "best_complete_candidate_blocks_estimate_fast": (next((c for c in candidates if c["meets_local_data_signals_fast"]), None) or {}).get("estimated_non_overlapping_30d_blocks_fast"),
            "confirmatory_resume_ready": False, "provenance_verified": False,
            "network_used": False, "outcomes_computed": False,
        },
        "caveats": [
            "Fast mode uses directory/file existence and day-dir counts; not full CSV schema/provenance verification.",
            "meets_local_data_signals_fast is necessary-but-not-sufficient local signal only; verify with trackc_panel_admissibility_audit, trackc_gap_repair_manifest, trackc_funding_schema_audit, and checksum/provenance lineage before confirmatory resume.",
            "Freeze a NEW preregistration before any outcome inspection.",
        ],
        "next_action": "if a fast candidate looks plausible, run deep admissibility+gap+funding-schema audits on the candidate window(s) and verify provenance/checksums locally; freeze NEW prereg before outcomes; no network/no outcomes in this step",
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "out": str(out), "candidate_count": len(candidates),
        "any_meets_local_data_signals_fast": report["summary"]["any_meets_local_data_signals_fast"],
        "best_months": (candidates[0]["months"][:2] + ["..."] + candidates[0]["months"][-1:]) if candidates else None,
        "best_blocks_estimate_fast": candidates[0]["estimated_non_overlapping_30d_blocks_fast"] if candidates else None,
        "best_funding_ok": candidates[0]["all_funding_month_ok"] if candidates else None,
        "best_series_ok_fast": candidates[0]["all_required_series_complete_fast"] if candidates else None,
        "confirmatory_resume_ready": False, "network_used": False, "outcomes_computed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
