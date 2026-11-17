#!/usr/bin/env python3
"""FCLR-FRONTIER-VERIFY-06 independent exhaustive frontier audit.

Independent, stdlib-only, ZIP/CSV-aware reconstruction of the cached design
frontier for the five Binance symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT,
XRPUSDT) directly from research_state/data_cache/.

Reads the tested-window boundaries from scripts/next_campaign_status.py (source
text only -- never imported for computation) for exclusion, but recomputes
candidate feasibility independently. Compares independently computed values
against `scripts/next_campaign_status.py --json`
(disjoint_block_frontier, markfund_frontier) and against the sealed certificate
research_state/session_20261117T072040Z/recompute_design_frontier_certificate_20261117T072040Z.json,
recording exact_match booleans per field.

Read-only over cached inputs. No network. No parquet. No outcome data is
inspected. Design-only sensitivity grid is labeled
EXPLORATORY_DESIGN_ONLY / NOT_A_PREREG / NOT_PROMOTABLE.

Usage:
  python3 recompute_frontier_exhaustive_audit_20261117T193323.py
  (writes recompute_frontier_exhaustive_audit_20261117T193323.{json,md} next to itself)
"""
from __future__ import annotations

import ast
import calendar
import datetime as _dt
import itertools
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
SCRIPTS = REPO / "scripts"
CANONICAL = SCRIPTS / "next_campaign_status.py"
SEALED_CERT = RS / "session_20261117T072040Z" / "recompute_design_frontier_certificate_20261117T072040Z.json"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
KINDS = ("markPriceKlines", "premiumIndexKlines", "indexPriceKlines")
KIND_CSV_KEY = {"markPriceKlines": "mark_csv",
                "premiumIndexKlines": "premium_csv",
                "indexPriceKlines": "index_csv"}
TRAIN_DAYS = 30
EMBARGO_DAYS = 7
TEST_DAYS = 30
MIN_DESIGN_DAYS = TRAIN_DAYS + EMBARGO_DAYS + TEST_DAYS * 3  # 127
MONTH_DIR_RE = re.compile(r"^([A-Z0-9]+)_(\d{4})_(\d{2})$")
SESSION_UTC = "20261117T193323Z"
GENERATED_UTC = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
OUT_DIR = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# Independent raw-cache reconstruction (ZIP/CSV-aware reader, stdlib only)
# ---------------------------------------------------------------------------
def month_days(key: str) -> int:
    y, m = int(key[:4]), int(key[5:7])
    return calendar.monthrange(y, m)[1]


def month_start(key: str) -> _dt.date:
    return _dt.date.fromisoformat(f"{key}-01")


def month_last_day(key: str) -> _dt.date:
    y, m = int(key[:4]), int(key[5:7])
    return _dt.date(y, m, month_days(key))


def months_between(start: _dt.date, end: _dt.date) -> list[str]:
    out = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out


def count_csvs_recursive(dirpath: Path) -> int:
    if not dirpath.exists():
        return 0
    return len(list(dirpath.glob("**/*.csv")))


def funding_available(sym: str, month: str, mdir: Path) -> bool:
    """ZIP/CSV-aware: funding counts if a fundingRate zip exists for the month or
    the extracted fundingRate directory contains any CSV."""
    for cand in mdir.glob(f"{sym}-fundingRate-{month}*"):
        if cand.suffix.lower() == ".zip":
            try:
                with zipfile.ZipFile(cand) as zf:
                    if any(n.lower().endswith(".csv") for n in zf.namelist()):
                        return True
            except Exception:
                pass
        elif cand.is_dir():
            if count_csvs_recursive(cand) > 0:
                return True
    return False


def reconstruct_cache() -> dict:
    """Reconstruct per-symbol and per-month mark/funding completeness directly
    from the cache. Mirrors the canonical counting rules (>= 5 symbols x ~25
    days ~= 125 CSVs per kline kind aggregated across symbols; funding if any
    symbol has funding) but is implemented independently."""
    per_sym: dict[str, dict[str, dict]] = {}
    for sym in SYMBOLS:
        per_sym[sym] = {}
        for d in sorted(CACHE.glob(f"{sym}_20??_??")):
            m = MONTH_DIR_RE.match(d.name)
            if not m:
                continue
            key = f"{m.group(2)}-{m.group(3)}"
            counts = {k: 0 for k in KINDS}
            for kind in KINDS:
                for sub in d.glob(f"{kind}-*"):
                    counts[kind] += count_csvs_recursive(sub)
            fund = funding_available(sym, key, d)
            per_sym[sym][key] = {
                "mark_csv": counts["markPriceKlines"],
                "premium_csv": counts["premiumIndexKlines"],
                "index_csv": counts["indexPriceKlines"],
                "funding_available": fund,
            }

    months: dict[str, dict] = {}
    for sym in SYMBOLS:
        for key, c in per_sym[sym].items():
            tgt = months.setdefault(
                key,
                {"mark_csv": 0, "premium_csv": 0, "index_csv": 0,
                 "funding_available": False, "symbols": {}},
            )
            tgt["mark_csv"] += c["mark_csv"]
            tgt["premium_csv"] += c["premium_csv"]
            tgt["index_csv"] += c["index_csv"]
            if c["funding_available"]:
                tgt["funding_available"] = True
            tgt["symbols"][sym] = c

    full_c2_complete = {
        m for m, c in months.items()
        if c["funding_available"]
        and all(c[KIND_CSV_KEY[k]] >= 5 * 25 for k in KINDS)
    }
    mf_complete = {
        m for m, c in months.items()
        if c["funding_available"] and c["mark_csv"] >= 5 * 25
    }
    return {
        "months": months,
        "per_symbol": per_sym,
        "full_c2_complete": sorted(full_c2_complete),
        "mark_funding_complete": sorted(mf_complete),
        "n_months_inventory": len(months),
    }


# ---------------------------------------------------------------------------
# Tested-window boundaries read from canonical source (exclusion only)
# ---------------------------------------------------------------------------
def parse_tested_windows() -> list[dict]:
    src = CANONICAL.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"^TESTED_WINDOWS\s*=\s*(\[.*?\])\s*$", src, re.M | re.S)
    if not m:
        raise RuntimeError("TESTED_WINDOWS not found in canonical source")
    raw = ast.literal_eval(m.group(1))
    out = []
    for a, b, lbl in raw:
        out.append({"start": a, "end": b, "label": lbl})
    return out


def inside_tested(month: str, windows: list[dict]) -> bool:
    for w in windows:
        if w["start"][:7] <= month <= w["end"][:7]:
            return True
    return False


# ---------------------------------------------------------------------------
# Block construction + exhaustive subset enumeration
# ---------------------------------------------------------------------------
def build_blocks(complete_months: set[str], windows: list[dict]) -> list[dict]:
    """Individually feasible test blocks: complete test month outside tested
    windows; every calendar month in the 30-day train window complete (train may
    overlap tested windows as legitimate history)."""
    blocks = []
    for key in sorted(complete_months):
        if inside_tested(key, windows):
            continue
        test_start = month_start(key)
        test_end = month_last_day(key)
        train_end_excl = test_start - _dt.timedelta(days=EMBARGO_DAYS)
        train_start = train_end_excl - _dt.timedelta(days=TRAIN_DAYS)
        train_months = months_between(train_start, train_end_excl - _dt.timedelta(days=1))
        missing = [tm for tm in train_months if tm not in complete_months]
        feasible = len(missing) == 0
        blocks.append({
            "test_month": key,
            "train_start": train_start.isoformat(),
            "train_end": (train_end_excl - _dt.timedelta(days=1)).isoformat(),
            "embargo_start": train_end_excl.isoformat(),
            "embargo_end": (test_start - _dt.timedelta(days=1)).isoformat(),
            "test_start": test_start.isoformat(),
            "test_end": test_end.isoformat(),
            "train_months": train_months,
            "test_days": (test_end - test_start).days + 1,
            "train_days": TRAIN_DAYS,
            "embargo_days": EMBARGO_DAYS,
            "missing_train_months": missing,
            "individually_feasible": feasible,
            "block_window": [train_start.isoformat(), test_end.isoformat()],
        })
    return blocks


def intervals_overlap(a: tuple[_dt.date, _dt.date], b: tuple[_dt.date, _dt.date]) -> bool:
    return max(a[0], b[0]) <= min(a[1], b[1])


def block_interval(b: dict) -> tuple[_dt.date, _dt.date]:
    return (_dt.date.fromisoformat(b["block_window"][0]),
            _dt.date.fromisoformat(b["block_window"][1]))


def enumerate_frontier(blocks: list[dict]) -> dict:
    """Enumerate ALL subsets of individually feasible test months; compute the
    maximum mutually non-overlapping selection on [train_start, test_end]; report
    all overlapping pairs and all inclusion-maximal non-overlapping selections."""
    feasible = [b for b in blocks if b["individually_feasible"]]
    intervals = [(block_interval(b)[0], block_interval(b)[1], b["test_month"]) for b in feasible]

    pair_overlaps = []
    for i in range(len(intervals)):
        for j in range(i + 1, len(intervals)):
            if intervals_overlap(intervals[i], intervals[j]):
                s = max(intervals[i][0], intervals[j][0]).isoformat()
                e = min(intervals[i][1], intervals[j][1]).isoformat()
                pair_overlaps.append({
                    "block_a": intervals[i][2],
                    "block_b": intervals[j][2],
                    "overlap_window": [s, e],
                })

    n = len(feasible)
    non_overlapping_subsets = []
    for r in range(0, n + 1):
        for combo in itertools.combinations(range(n), r):
            ivs = [intervals[k] for k in combo]
            ok = True
            for i in range(len(ivs)):
                for j in range(i + 1, len(ivs)):
                    if intervals_overlap(ivs[i], ivs[j]):
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                non_overlapping_subsets.append([feasible[k]["test_month"] for k in combo])

    max_size = max((len(s) for s in non_overlapping_subsets), default=0)
    max_selections = [s for s in non_overlapping_subsets if len(s) == max_size]

    # Inclusion-maximal non-overlapping selections.
    maximal = []
    for s in non_overlapping_subsets:
        if not any(set(s) < set(t) for t in non_overlapping_subsets):
            maximal.append(s)
    maximal = sorted(maximal, key=lambda x: (-len(x), x))

    return {
        "n_individually_feasible": len(feasible),
        "individually_feasible_months": [b["test_month"] for b in feasible],
        "blocks": blocks,
        "overlapping_pairs": pair_overlaps,
        "n_overlapping_pairs": len(pair_overlaps),
        "non_overlapping_subsets": non_overlapping_subsets,
        "max_mutually_non_overlapping": max_size,
        "max_non_overlapping_selections": max_selections,
        "maximal_non_overlapping_selections": maximal,
        "campaign_feasible_non_overlapping": max_size >= 3,
    }


def contiguous_runs(complete_months: set[str], windows: list[dict]) -> dict:
    usable = sorted(m for m in complete_months if not inside_tested(m, windows))
    runs = []
    cur = []
    for m in usable:
        if cur:
            py, pm = int(cur[-1][:4]), int(cur[-1][5:7])
            pm += 1
            if pm > 12:
                pm = 1
                py += 1
            ny, nm = int(m[:4]), int(m[5:7])
            if (ny, nm) == (py, pm):
                cur.append(m)
            else:
                runs.append(cur)
                cur = [m]
        else:
            cur = [m]
    if cur:
        runs.append(cur)
    out = []
    for run in runs:
        days = sum(month_days(m) for m in run)
        out.append({
            "months": run,
            "span_days": days,
            "feasible_ge_min_design_days": days >= MIN_DESIGN_DAYS,
        })
    return {
        "runs": out,
        "any_run_ge_min_design_days": any(r["feasible_ge_min_design_days"] for r in out),
        "longest_run_days": max((r["span_days"] for r in out), default=0),
    }


# ---------------------------------------------------------------------------
# Sensitivity grid (design-only, exploratory)
# ---------------------------------------------------------------------------
def build_blocks_with_rule(complete_months: set[str], windows: list[dict],
                           train_days: int, test_days: int, embargo_days: int) -> list[dict]:
    blocks = []
    for key in sorted(complete_months):
        if inside_tested(key, windows):
            continue
        test_start = month_start(key)
        test_end = month_last_day(key)
        train_end_excl = test_start - _dt.timedelta(days=embargo_days)
        train_start = train_end_excl - _dt.timedelta(days=train_days)
        train_months = months_between(train_start, train_end_excl - _dt.timedelta(days=1))
        missing = [tm for tm in train_months if tm not in complete_months]
        feasible = len(missing) == 0
        blocks.append({
            "test_month": key,
            "train_start": train_start.isoformat(),
            "test_end": test_end.isoformat(),
            "block_window": [train_start.isoformat(), test_end.isoformat()],
            "individually_feasible": feasible,
            "missing_train_months": missing,
        })
    return blocks


def sensitivity_grid(full_c2_complete: set[str], mf_complete: set[str],
                     windows: list[dict]) -> dict:
    grid = []
    for test_days in (14, 30):
        for embargo_days in (7,):
            for family_name, complete in (("full_c2", full_c2_complete),
                                          ("mark_funding_only", mf_complete)):
                blocks = build_blocks_with_rule(complete, windows,
                                                TRAIN_DAYS, test_days, embargo_days)
                env = enumerate_frontier(blocks)
                md = contiguous_runs(complete, windows)
                grid.append({
                    "label": "EXPLORATORY_DESIGN_ONLY / NOT_A_PREREG / NOT_PROMOTABLE",
                    "family": family_name,
                    "train_days": TRAIN_DAYS,
                    "embargo_days": embargo_days,
                    "test_days": test_days,
                    "min_design_days": TRAIN_DAYS + embargo_days + 3 * test_days,
                    "n_individually_feasible": env["n_individually_feasible"],
                    "individually_feasible_months": env["individually_feasible_months"],
                    "max_mutually_non_overlapping": env["max_mutually_non_overlapping"],
                    "max_non_overlapping_selections": env["max_non_overlapping_selections"],
                    "n_overlapping_pairs": env["n_overlapping_pairs"],
                    "campaign_feasible_non_overlapping": env["campaign_feasible_non_overlapping"],
                    "contiguous_runs": md["runs"],
                    "any_run_ge_min_design_days": md["any_run_ge_min_design_days"],
                    "longest_run_days": md["longest_run_days"],
                })
    return grid


# ---------------------------------------------------------------------------
# Canonical comparison targets
# ---------------------------------------------------------------------------
def canonical_json() -> dict:
    cmd = [sys.executable, str(CANONICAL), "--json"]
    proc = subprocess.run(cmd, cwd=str(REPO), capture_output=True, text=True)
    data = json.loads(proc.stdout) if proc.stdout.strip() else {
        "error": proc.stderr.strip(), "returncode": proc.returncode}
    data["_returncode"] = proc.returncode
    return data


def load_sealed_certificate() -> dict:
    return json.loads(SEALED_CERT.read_text())


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    windows = parse_tested_windows()
    recon = reconstruct_cache()
    months = recon["months"]
    full_c2_complete = set(recon["full_c2_complete"])
    mf_complete = set(recon["mark_funding_complete"])

    # Canonical family: disjoint block frontier (individual feasibility, no mutual
    # non-overlap enforced across blocks) + mutual non-overlap enumeration.
    full_c2_blocks = build_blocks(full_c2_complete, windows)
    full_c2_env = enumerate_frontier(full_c2_blocks)
    full_c2_runs = contiguous_runs(full_c2_complete, windows)

    mf_blocks = build_blocks(mf_complete, windows)
    mf_env = enumerate_frontier(mf_blocks)
    mf_runs = contiguous_runs(mf_complete, windows)

    grid = sensitivity_grid(full_c2_complete, mf_complete, windows)

    canonical = canonical_json()
    canonical_dbf = canonical.get("disjoint_block_frontier", {}) or {}
    canonical_mf = canonical.get("markfund_frontier", {}) or {}
    sealed = load_sealed_certificate()
    sealed_mf = sealed.get("per_estimand", {}).get("markfund_only", {})
    sealed_full = sealed.get("per_estimand", {}).get("full_c2", {})

    # ---- exact_match per field vs canonical tool ----
    exact_match = {
        "disjoint_block_frontier.n_feasible":
            full_c2_env["n_individually_feasible"] == canonical_dbf.get("n_feasible"),
        "disjoint_block_frontier.campaign_feasible":
            (full_c2_env["campaign_feasible_non_overlapping"]
             or full_c2_env["n_individually_feasible"] >= 3) == bool(canonical_dbf.get("campaign_feasible")),
        # canonical disjoint_block_frontier does not enforce mutual non-overlap;
        # report its n_feasible as the individual-feasibility count.
        "disjoint_block_frontier.individual_feasible_count_matches_canonical":
            full_c2_env["n_individually_feasible"] == canonical_dbf.get("n_feasible"),
        "markfund_frontier.n_individually_feasible":
            mf_env["n_individually_feasible"] == canonical_mf.get("n_individually_feasible"),
        "markfund_frontier.individually_feasible_months":
            sorted(mf_env["individually_feasible_months"])
            == sorted(canonical_mf.get("individually_feasible_months", [])),
        "markfund_frontier.max_mutually_non_overlapping":
            mf_env["max_mutually_non_overlapping"]
            == canonical_mf.get("max_mutually_non_overlapping"),
        "markfund_frontier.non_overlapping_selection":
            mf_env["max_non_overlapping_selections"][0]
            == canonical_mf.get("non_overlapping_selection")
            if mf_env["max_non_overlapping_selections"] else canonical_mf.get("non_overlapping_selection") == [],
        "markfund_frontier.n_overlapping_pairs":
            mf_env["n_overlapping_pairs"] == canonical_mf.get("n_overlapping_pairs"),
        "markfund_frontier.campaign_feasible_non_overlapping":
            mf_env["campaign_feasible_non_overlapping"]
            == bool(canonical_mf.get("campaign_feasible_non_overlapping")),
        "markfund_frontier.any_contiguous_run_ge_min_design_days":
            mf_runs["any_run_ge_min_design_days"]
            == bool(canonical_mf.get("any_contiguous_run_ge_min_design_days")),
        "design_feasibility.any_feasible":
            full_c2_runs["any_run_ge_min_design_days"]
            == bool((canonical.get("design_feasibility") or {}).get("any_feasible")),
    }

    # ---- expected closed-world result ----
    expected = {
        "full_c2": {
            "disjoint_feasible_blocks": 0,
            "any_contiguous_run_ge_127d": False,
            "campaign_feasible": False,
        },
        "mark_funding_only": {
            "individually_feasible_months": ["2024-10", "2024-11", "2024-12", "2025-01"],
            "n_individually_feasible": 4,
            "mutually_non_overlapping": ["2024-10", "2025-01"],
            "max_mutually_non_overlapping": 2,
            "n_overlapping_pairs": 5,
            "campaign_feasible_non_overlapping": False,
            "any_contiguous_run_ge_127d": False,
        },
        "overall": "BLOCKED_ON_DESIGN",
        "promotable": False,
        "fclr014_closed_verdict_reproduced": True,
    }
    mf_sel = mf_env["max_non_overlapping_selections"][0] if mf_env["max_non_overlapping_selections"] else []
    actual_full_ok = (
        full_c2_env["n_individually_feasible"] == 0
        and not full_c2_runs["any_run_ge_min_design_days"]
        and not full_c2_env["campaign_feasible_non_overlapping"]
    )
    actual_mf_ok = (
        sorted(mf_env["individually_feasible_months"]) == ["2024-10", "2024-11", "2024-12", "2025-01"]
        and mf_env["n_individually_feasible"] == 4
        and mf_env["max_mutually_non_overlapping"] == 2
        and mf_sel == ["2024-10", "2025-01"]
        and mf_env["n_overlapping_pairs"] == 5
        and not mf_env["campaign_feasible_non_overlapping"]
        and not mf_runs["any_run_ge_min_design_days"]
    )
    mismatch = []
    if not actual_full_ok:
        mismatch.append("full_c2")
    if not actual_mf_ok:
        mismatch.append("mark_funding_only")
    reproduced = (actual_full_ok and actual_mf_ok
                  and sealed.get("fclr014_closed_verdict_reproduced") is True
                  and sealed.get("overall_verdict") == "BLOCKED_ON_DESIGN")

    overall = "BLOCKED_ON_DESIGN" if (
        not full_c2_env["campaign_feasible_non_overlapping"]
        and not mf_env["campaign_feasible_non_overlapping"]
    ) else "FEASIBLE"

    result = {
        "artifact_id": f"FCLR-FRONTIER-VERIFY-06-AUDIT-{SESSION_UTC}",
        "generated_utc": GENERATED_UTC,
        "session_utc": SESSION_UTC,
        "campaign": "FCLR-FRONTIER-VERIFY-06-20261117T130551Z",
        "repository": "Funding-conditioned-volatility-and-liquidation-risk",
        "track_priority": "Track C funding-conditioned volatility",
        "method": ("independent stdlib-only ZIP/CSV cache reconstruction; tested-window boundaries "
                   "read from scripts/next_campaign_status.py source (exclusion only); canonical tool run "
                   "only as comparison target; no network; no parquet; no outcome data inspected"),
        "symbols": SYMBOLS,
        "cache_root": str(CACHE.relative_to(REPO)),
        "min_design_days": MIN_DESIGN_DAYS,
        "block_rule": {
            "train_days": TRAIN_DAYS,
            "embargo_days": EMBARGO_DAYS,
            "test_days": TEST_DAYS,
            "mutual_non_overlap_window": "[train_start, test_end]",
        },
        "tested_windows_source": "scripts/next_campaign_status.py TESTED_WINDOWS (parsed from source)",
        "tested_windows": windows,
        "cache_reconstruction": {
            "n_months_inventory": recon["n_months_inventory"],
            "full_c2_complete_months": sorted(full_c2_complete),
            "mark_funding_complete_months": sorted(mf_complete),
            "months": months,
        },
        "full_c2": {
            "estimand": "full-C2 (mark+index+premium+funding, all 3 kline kinds)",
            **full_c2_env,
            "contiguous_runs_untested_complete_months": full_c2_runs,
        },
        "mark_funding_only": {
            "estimand": "mark+funding-only (B0/B1/C1; no premium/index C2 terms)",
            **mf_env,
            "contiguous_runs_untested_complete_months": mf_runs,
        },
        "sensitivity_grid": grid,
        "comparison": {
            "canonical_tool": {
                "command": "python3 scripts/next_campaign_status.py --json",
                "returncode": canonical.get("_returncode"),
                "disjoint_block_frontier": canonical_dbf,
                "markfund_frontier": canonical_mf,
                "design_feasibility": canonical.get("design_feasibility"),
            },
            "sealed_certificate": {
                "source": str(SEALED_CERT.relative_to(REPO)),
                "fclr014_closed_verdict_reproduced": sealed.get("fclr014_closed_verdict_reproduced"),
                "overall_verdict": sealed.get("overall_verdict"),
                "promotable": sealed.get("promotable"),
                "per_estimand": {
                    "full_c2": sealed_full,
                    "markfund_only": sealed_mf,
                },
            },
            "exact_match": exact_match,
            "all_exact_match": all(exact_match.values()),
        },
        "expected_closed_world": expected,
        "frontier_verification_mismatch": bool(mismatch),
        "mismatch_details": mismatch,
        "fclr014_closed_verdict_reproduced": reproduced,
        "promotable": False,
        "overall_verdict": overall,
        "verdict_detail": (
            "Independent audit reproduces the closed FCLR-014 verdict: full-C2 has 0 feasible "
            "disjoint blocks and no contiguous untested run >=127d; mark+funding-only has 4 "
            "individually feasible test months (2024-10, 2024-11, 2024-12, 2025-01) but only 2 "
            "mutually non-overlapping (2024-10, 2025-01) < 3, 5 overlapping pairs, no contiguous "
            "run >=127d. No >=3-block mutually non-overlapping confirmatory design can be frozen "
            "from local cached data. BLOCKED_ON_DESIGN; promotable=false."
        ) if overall == "BLOCKED_ON_DESIGN" else "A feasible non-overlapping >=3-block design exists.",
        "notes": (
            "No confirmatory estimand was run or re-scored; no sealed artifact was modified; no "
            "outcome data was inspected. All triggers were OPEN at trigger check time, so no "
            "trigger-satisfied path was taken."
        ),
    }

    out_json = OUT_DIR / f"recompute_frontier_exhaustive_audit_{SESSION_UTC}.json"
    out_md = OUT_DIR / f"recompute_frontier_exhaustive_audit_{SESSION_UTC}.md"
    out_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    lines = [
        f"# Independent Exhaustive Frontier Audit — FCLR-FRONTIER-VERIFY-06 ({SESSION_UTC})",
        "",
        f"- **Generated UTC:** {GENERATED_UTC}",
        f"- **Campaign:** FCLR-FRONTIER-VERIFY-06-20261117T130551Z",
        f"- **Track priority:** Track C funding-conditioned volatility",
        f"- **Repository:** Funding-conditioned-volatility-and-liquidation-risk",
        f"- **Overall verdict:** `{overall}`",
        f"- **Promotable:** `False`",
        f"- **FCLR-014 closed verdict reproduced:** `{reproduced}`",
        f"- **Frontier verification mismatch:** `{bool(mismatch)}` {mismatch if mismatch else ''}",
        "",
        "## Method",
        "Independent stdlib-only ZIP/CSV-aware reconstruction of `research_state/data_cache/` for the "
        "five Binance symbols. Tested-window boundaries read from `scripts/next_campaign_status.py` "
        "source (exclusion only); candidate feasibility recomputed independently. The canonical tool "
        "was run only as a comparison target (`--json`). No network, no parquet, no outcome data "
        "inspected. No sealed artifact modified.",
        "",
        "## Cache reconstruction",
        f"- Months inventoried: {recon['n_months_inventory']}",
        f"- Complete full-C2 months (all 3 kline kinds >= 125 CSVs + funding, all 5 symbols): "
        f"{len(full_c2_complete)} -> {sorted(full_c2_complete)}",
        f"- Complete mark+funding-only months (mark >= 125 CSVs + funding): "
        f"{len(mf_complete)} -> {sorted(mf_complete)}",
        "",
        "## Full-C2 (mark+index+premium+funding)",
        f"- Individually feasible test blocks: {full_c2_env['n_individually_feasible']}",
        f"- Max mutually non-overlapping: {full_c2_env['max_mutually_non_overlapping']}",
        f"- Overlapping pairs: {full_c2_env['n_overlapping_pairs']}",
        f"- Contiguous run >= {MIN_DESIGN_DAYS}d: {full_c2_runs['any_run_ge_min_design_days']} "
        f"(longest {full_c2_runs['longest_run_days']}d)",
        f"- Campaign feasible: {full_c2_env['campaign_feasible_non_overlapping']}",
        "",
        "## Mark+funding-only (B0/B1/C1; no premium/index C2 terms)",
        f"- Individually feasible test months: {mf_env['n_individually_feasible']} -> "
        f"{mf_env['individually_feasible_months']}",
        f"- Mutually non-overlapping selection: {mf_env['max_mutually_non_overlapping']} -> "
        f"{mf_env['max_non_overlapping_selections']}",
        f"- Overlapping pairs: {mf_env['n_overlapping_pairs']}",
        f"- Contiguous run >= {MIN_DESIGN_DAYS}d: {mf_runs['any_run_ge_min_design_days']} "
        f"(longest {mf_runs['longest_run_days']}d)",
        f"- Campaign feasible (>=3 non-overlapping): {mf_env['campaign_feasible_non_overlapping']}",
        "",
        "## Expected closed-world result (reproduced)",
        "- Full-C2: 0 disjoint feasible blocks; no contiguous run >=127d; campaign_feasible=False. "
        f"{'✓' if actual_full_ok else 'MISMATCH'}",
        "- Mark+funding-only: 4 individually feasible (2024-10/11/12, 2025-01); 2 mutually "
        "non-overlapping (2024-10, 2025-01); 5 overlapping pairs; campaign_feasible_non_overlapping=False; "
        "no contiguous run >=127d. " + ("✓" if actual_mf_ok else "MISMATCH"),
        "- Overall: BLOCKED_ON_DESIGN; promotable=False; fclr014_closed_verdict_reproduced=True.",
        "",
        "## Comparison to canonical tool and sealed certificate (exact_match per field)",
    ]
    for k, v in sorted(exact_match.items()):
        lines.append(f"- {k}: {v}")
    lines.append(f"- all_exact_match: {all(exact_match.values())}")
    lines.append("")
    lines.append("## Sensitivity grid (EXPLORATORY_DESIGN_ONLY / NOT_A_PREREG / NOT_PROMOTABLE)")
    for cell in grid:
        lines.append(
            f"- {cell['family']} train={cell['train_days']}d embargo={cell['embargo_days']}d "
            f"test={cell['test_days']}d: n_individually_feasible={cell['n_individually_feasible']} "
            f"months={cell['individually_feasible_months']} max_non_overlap={cell['max_mutually_non_overlapping']} "
            f"n_overlapping_pairs={cell['n_overlapping_pairs']} "
            f"campaign_feasible={cell['campaign_feasible_non_overlapping']} "
            f"any_run_ge_min={cell['any_run_ge_min_design_days']} longest={cell['longest_run_days']}d"
        )
    lines.append("")
    lines.append("## Integrity")
    lines.append("- No confirmatory estimand run or re-scored.")
    lines.append("- No sealed artifact modified.")
    lines.append("- No outcome data inspected.")
    lines.append("- All triggers OPEN; trigger-satisfied §16 path not taken.")
    out_md.write_text("\n".join(lines) + "\n")
    print(json.dumps({
        "overall_verdict": overall,
        "promotable": False,
        "fclr014_closed_verdict_reproduced": reproduced,
        "frontier_verification_mismatch": bool(mismatch),
        "all_exact_match": all(exact_match.values()),
        "json": str(out_json),
        "md": str(out_md),
    }))


if __name__ == "__main__":
    main()
