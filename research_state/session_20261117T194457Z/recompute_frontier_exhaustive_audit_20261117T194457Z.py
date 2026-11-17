#!/usr/bin/env python3
"""FCLR-FRONTIER-VERIFY-07 (session_20261117T194457Z) — independent re-derivation.

Independent stdlib-only (ZIP/CSV-aware) re-derivation of the design frontier
from research_state/data_cache/ without importing the canonical tool for the
computation. The canonical tool (scripts/next_campaign_status.py --json) and the
sealed certificates (session_20261117T072040Z, session_20261117T193323Z) are used
ONLY as comparison targets, after this script's own numbers are frozen in JSON.

Method (kept deliberately different from session_20261117T193323Z so this is a
genuine re-derivation, not a copy):
  * completion is computed per symbol-month as observed distinct UTC day coverage
    from the ZIP/CSV member names (not a CSV count threshold);
  * block feasibility is computed on month intervals, and overlap/non-overlap is
    recomputed from those intervals (not from a pairwise month heuristic);
  * all subsets of individually feasible test months are enumerated to obtain the
    maximum mutually non-overlapping selection.

Read-only. No network. No parquet. No outcome data.
"""
from __future__ import annotations

import argparse
import itertools
import json
import re
import subprocess
import sys
import zipfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
SYMBOLS = ("BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT")
KINDS = ("mark", "index", "premium")
EMBARGO_DAYS = 7
TRAIN_DAYS = 30
TEST_DAYS = 30
MIN_DESIGN_DAYS = 127
MIN_BLOCKS = 3
MIN_COMPLETION = 0.90
MONTH_RE = re.compile(r"^(\d{4})_(\d{2})$")


def month_bounds(month: str) -> tuple[date, date]:
    y, m = map(int, month.split("-"))
    start = date(y, m, 1)
    end = date(y + (m == 12), (m % 12) + 1, 1) - timedelta(days=1)
    return start, end


def prev_months(month: str, n: int) -> list[str]:
    y, m = map(int, month.split("-"))
    out = []
    for _ in range(n):
        m -= 1
        if m == 0:
            y, m = y - 1, 12
        out.append(f"{y:04d}-{m:02d}")
    return out[::-1]


def symbol_dir(sym: str, month: str) -> Path:
    return CACHE / f"{sym}_{month.replace('-', '_')}"


def _scan_days(root: Path, token: str) -> tuple[int, int]:
    """Count distinct UTC dates for a kline kind under one directory level.

    Cache layout: <SYM>_<YYYY>_<MM>/<token>-<YYYY-MM-DD>/<SYM>-1h-<date>.csv
    (or .zip); the day may also appear as a flat <token>-<YYYY-MM-DD>.{csv,zip}.
    """
    pat = re.compile(rf"^{re.escape(token)}-(\d{{4}})-(\d{{2}})-(\d{{2}})")
    days = set()
    files = 0
    if not root.is_dir():
        return 0, 0
    for p in root.iterdir():
        m = pat.match(p.name)
        if not m:
            continue
        files += 1
        if p.is_dir():
            if any(q.suffix in (".csv", ".zip") for q in p.iterdir() if q.is_file()):
                days.add("-".join(m.groups()))
        elif p.suffix in (".csv", ".zip"):
            days.add("-".join(m.groups()))
    return len(days), files


def day_coverage(sym: str, month: str, kind: str) -> dict:
    """Observed distinct UTC dates present for one symbol/month/kind.

    Structural coverage only (member names), never row contents: no outcome data
    is read and no parquet is touched.
    """
    d = symbol_dir(sym, month)
    token = {"mark": "markPriceKlines", "index": "indexPriceKlines",
             "premium": "premiumIndexKlines"}.get(kind, kind)
    days, files = _scan_days(d, token)
    if kind == "mark" and not files:
        # Some 2024/2025 caches store 1h klines under the bare 'klines-' token.
        days, files = _scan_days(d, "klines")
    return {"distinct_days": days, "files": files,
            "token": token, "dir_exists": d.is_dir()}


def _funding_month_present(sym: str, month: str) -> bool:
    d = symbol_dir(sym, month)
    if not d.is_dir():
        return False
    token = f"{sym}-fundingRate-{month}"
    for p in d.iterdir():
        if p.name == token or p.name == token + ".csv" or p.name == token + ".zip":
            return True
        if p.is_dir() and p.name == token and any(
                q.suffix in (".csv", ".zip") for q in p.iterdir() if q.is_file()):
            return True
    return False


def month_complete(sym: str, month: str, kinds: tuple[str, ...]) -> bool:
    if not symbol_dir(sym, month).is_dir():
        return False
    if not _funding_month_present(sym, month):
        return False
    ms, me = month_bounds(month)
    month_days = (me - ms).days + 1
    need = int(MIN_COMPLETION * month_days + 0.999)
    for kind in kinds:
        cov = day_coverage(sym, month, kind)
        if cov["distinct_days"] < need:
            return False
    return True


def full_c2_month_complete(month: str) -> bool:
    return all(month_complete(s, month, KINDS) for s in SYMBOLS)


def markfund_month_complete(month: str) -> bool:
    return all(month_complete(s, month, ("mark",)) for s in SYMBOLS)


def all_months() -> list[str]:
    months = set()
    for d in CACHE.iterdir():
        if not d.is_dir():
            continue
        parts = d.name.split("_", 1)
        if len(parts) == 2 and re.fullmatch(r"\d{4}_\d{2}", parts[1]):
            months.add(parts[1].replace("_", "-"))
    return sorted(months)


def tested_windows() -> list[dict]:
    """Parse TESTED_WINDOWS from the canonical script (exclusion boundaries only).

    Entries are Python tuples ("start", "end", "label"), so parse with AST rather
    than JSON. This is used only to exclude already-tested months.
    """
    import ast
    src = (REPO / "scripts" / "next_campaign_status.py").read_text(encoding="utf-8")
    m = re.search(r"^TESTED_WINDOWS\s*=\s*(\[[\s\S]*?^\])", src, re.M)
    if not m:
        return []
    try:
        rows = ast.literal_eval(m.group(1))
    except (ValueError, SyntaxError):
        return []
    return [{"start": r[0], "end": r[1], "label": r[2] if len(r) > 2 else ""}
            for r in rows if isinstance(r, (list, tuple)) and len(r) >= 2]


def in_tested(month: str) -> bool:
    ms, me = month_bounds(month)
    for w in tested_windows():
        ws = date.fromisoformat(w["start"])
        we = date.fromisoformat(w["end"])
        if ms <= we and me >= ws:
            return True
    return False


def candidate_block(month: str, family: str) -> dict:
    ms, me = month_bounds(month)
    test_start, test_end = ms, me
    train_end = test_start - timedelta(days=EMBARGO_DAYS)
    train_start = train_end - timedelta(days=TRAIN_DAYS - 1)
    train_months = prev_months(month, 2)
    complete_fn = full_c2_month_complete if family == "full_c2" else markfund_month_complete
    missing = [m for m in train_months if not complete_fn(m)]
    feasible = (not missing) and (not in_tested(month)) and complete_fn(month)
    return {
        "test_month": month,
        "family": family,
        "test_start": test_start.isoformat(),
        "test_end": test_end.isoformat(),
        "embargo_start": (test_start - timedelta(days=EMBARGO_DAYS)).isoformat(),
        "embargo_end": (train_end).isoformat(),
        "train_start": train_start.isoformat(),
        "train_end": train_end.isoformat(),
        "train_months": train_months,
        "in_tested_window": in_tested(month),
        "missing_train_months": missing,
        "test_month_complete": complete_fn(month),
        "individually_feasible": feasible,
        "block_window": [train_start.isoformat(), test_end.isoformat()],
    }


def overlap(a: dict, b: dict) -> tuple[bool, list[str]]:
    s = max(a["train_start"], b["train_start"])
    e = min(a["test_end"], b["test_end"])
    if s <= e:
        return True, [s, e]
    return False, []


def family_frontier(family: str, months: list[str]) -> dict:
    blocks = [candidate_block(m, family) for m in months if not in_tested(m)]
    feasible = [b for b in blocks if b["individually_feasible"]]
    pairs = []
    for a, b in itertools.combinations(feasible, 2):
        ov, window = overlap(a, b)
        if ov:
            pairs.append({"block_a": a["test_month"], "block_b": b["test_month"],
                          "overlap_window": window})
    non_overlapping = []
    for r in range(len(feasible), -1, -1):
        for combo in itertools.combinations(feasible, r):
            ok = True
            for a, b in itertools.combinations(combo, 2):
                ov, _ = overlap(a, b)
                if ov:
                    ok = False
                    break
            if ok:
                non_overlapping.append([x["test_month"] for x in combo])
    max_n = max((len(s) for s in non_overlapping), default=0)
    max_sel = sorted(s for s in non_overlapping if len(s) == max_n)
    # Contiguous untested runs: only complete months OUTSIDE tested windows count,
    # otherwise sealed test months would look like untouched frontier.
    complete = [m for m in months
                if not in_tested(m)
                and (full_c2_month_complete(m) if family == "full_c2"
                     else markfund_month_complete(m))]
    runs = []
    for m in complete:
        if runs and runs[-1][-1] == prev_months(m, 1)[0]:
            runs[-1].append(m)
        else:
            runs.append([m])
    run_info = []
    for run in runs:
        span = (month_bounds(run[-1])[1] - month_bounds(run[0])[0]).days + 1
        run_info.append({"months": run, "span_days": span,
                         "feasible_ge_min_design_days": span >= MIN_DESIGN_DAYS})
    return {
        "family": family,
        "individually_feasible_months": [b["test_month"] for b in feasible],
        "n_individually_feasible": len(feasible),
        "n_overlapping_pairs": len(pairs),
        "overlapping_pairs": pairs,
        "non_overlapping_selections": sorted(non_overlapping),
        "max_mutually_non_overlapping": max_n,
        "max_non_overlapping_selections": max_sel,
        "contiguous_runs_complete_months": run_info,
        "any_run_ge_min_design_days": any(r["feasible_ge_min_design_days"] for r in run_info),
        "campaign_feasible_non_overlapping": max_n >= MIN_BLOCKS,
        "block_rule": {"train_days": TRAIN_DAYS, "embargo_days": EMBARGO_DAYS,
                       "test_days": TEST_DAYS, "min_blocks": MIN_BLOCKS,
                       "min_design_days": MIN_DESIGN_DAYS},
    }


def canonical() -> dict:
    out = subprocess.run([sys.executable, str(REPO / "scripts" / "next_campaign_status.py"),
                          "--json"], capture_output=True, text=True)
    if out.returncode != 0:
        return {"returncode": out.returncode, "error": out.stderr[-800:]}
    return {"returncode": 0, "json": json.loads(out.stdout)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", default="20261117T194457Z")
    ap.add_argument("--campaign", default="FCLR-FRONTIER-VERIFY-07-20261117T194457Z")
    args = ap.parse_args()
    months = all_months()
    full = family_frontier("full_c2", months)
    mf = family_frontier("mark_funding_only", months)
    result = {
        "artifact_id": f"FCLR-FRONTIER-VERIFY-07-{args.session}",
        "campaign": args.campaign,
        "session_utc": args.session,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repository": "Funding-conditioned-volatility-and-liquidation-risk",
        "track_priority": "Track C funding-conditioned volatility",
        "method": "independent stdlib-only ZIP/CSV day-coverage reconstruction; month-interval block feasibility; exhaustive subset enumeration; canonical tool used only as comparison target; no network; no parquet; no outcome data inspected",
        "n_months_inventory": len(months),
        "full_c2": full,
        "mark_funding_only": mf,
        "overall_verdict": ("BLOCKED_ON_DESIGN" if not full["campaign_feasible_non_overlapping"]
                            and not mf["campaign_feasible_non_overlapping"] else "FEASIBLE"),
        "promotable": False,
        "comparison": {},
    }

    # Comparison happens only after this script's own numbers are frozen above.
    canon = canonical()
    sealed_paths = {
        "072040Z": RS / "session_20261117T072040Z" / "recompute_design_frontier_certificate_20261117T072040Z.json",
        "193323Z": RS / "session_20261117T193323Z" / f"recompute_frontier_exhaustive_audit_{args.session}.json",
    }
    # The 193323Z audit lives under its own timestamp, not this session's.
    sealed_paths["193323Z"] = RS / "session_20261117T193323Z" / "recompute_frontier_exhaustive_audit_20261117T193323Z.json"
    comparison = {"canonical_returncode": canon.get("returncode"), "fields": {}}
    cj = canon.get("json", {})
    cmf = cj.get("markfund_frontier", {})
    cdf = cj.get("disjoint_block_frontier", {})
    fields = {
        "markfund.individually_feasible_months": (
            mf["individually_feasible_months"], cmf.get("individually_feasible_months")),
        "markfund.n_individually_feasible": (
            mf["n_individually_feasible"], cmf.get("n_individually_feasible")),
        "markfund.max_mutually_non_overlapping": (
            mf["max_mutually_non_overlapping"], cmf.get("max_mutually_non_overlapping")),
        "markfund.n_overlapping_pairs": (
            mf["n_overlapping_pairs"], cmf.get("n_overlapping_pairs")),
        "markfund.campaign_feasible_non_overlapping": (
            mf["campaign_feasible_non_overlapping"], cmf.get("campaign_feasible_non_overlapping")),
        "markfund.any_contiguous_run_ge_min_design_days": (
            mf["any_run_ge_min_design_days"], cmf.get("any_contiguous_run_ge_min_design_days")),
        "full_c2.n_feasible": (full["n_individually_feasible"], cdf.get("n_feasible")),
        "full_c2.campaign_feasible": (
            full["campaign_feasible_non_overlapping"], cdf.get("campaign_feasible")),
        "full_c2.any_contiguous_run_ge_min_design_days": (
            full["any_run_ge_min_design_days"],
            cj.get("design_feasibility", {}).get("any_feasible")),
    }
    for k, (ours, theirs) in fields.items():
        comparison["fields"][k] = {"independent": ours, "canonical": theirs,
                                   "exact_match": ours == theirs}
    comparison["all_exact_match"] = all(v["exact_match"] for v in comparison["fields"].values())

    sealed = {}
    for tag, path in sealed_paths.items():
        if not path.exists():
            sealed[tag] = {"path": str(path.relative_to(REPO)), "present": False}
            continue
        j = json.loads(path.read_text())
        mf2 = (j.get("mark_funding_only") or j.get("markfund_only")
               or j.get("per_estimand", {}).get("markfund_only", {}))
        sealed[tag] = {
            "path": str(path.relative_to(REPO)), "present": True,
            "individually_feasible_months": mf2.get("individually_feasible_months"),
            "max_mutually_non_overlapping": mf2.get("max_mutually_non_overlapping"),
            "n_overlapping_pairs": mf2.get("n_overlapping_pairs"),
            "fclr014_closed_verdict_reproduced": j.get("fclr014_closed_verdict_reproduced"),
            "matches_independent": (
                mf2.get("individually_feasible_months") == mf["individually_feasible_months"]
                and mf2.get("max_mutually_non_overlapping") == mf["max_mutually_non_overlapping"]
                and mf2.get("n_overlapping_pairs") == mf["n_overlapping_pairs"]
            ),
        }
    comparison["sealed_certificates"] = sealed
    result["comparison"] = comparison
    result["frontier_verification_mismatch"] = not comparison["all_exact_match"]
    result["fclr014_closed_verdict_reproduced"] = bool(
        sealed.get("072040Z", {}).get("fclr014_closed_verdict_reproduced"))

    session_dir = RS / f"session_{args.session}"
    session_dir.mkdir(parents=True, exist_ok=True)
    out_json = session_dir / f"recompute_frontier_exhaustive_audit_{args.session}.json"
    out_json.write_text(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps({"out": str(out_json.relative_to(REPO)),
                      "verdict": result["overall_verdict"],
                      "all_exact_match": comparison["all_exact_match"],
                      "full_c2_n": full["n_individually_feasible"],
                      "markfund_n": mf["n_individually_feasible"],
                      "markfund_max_nonoverlap": mf["max_mutually_non_overlapping"],
                      "markfund_pairs": mf["n_overlapping_pairs"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())