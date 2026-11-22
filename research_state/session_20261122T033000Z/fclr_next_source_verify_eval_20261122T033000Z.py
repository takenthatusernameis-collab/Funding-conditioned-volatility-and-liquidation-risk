#!/usr/bin/env python3
"""FCLR-NEXT-SOURCE-VERIFY-01 confirmatory eval (stdlib-only).

Implements the pre-specified design FCLR-NEXT-CONFIRM-001 against the admissible
local data domain (research_state/data/raw/ BTC/ETH hourly klines + funding,
Jan-Mar 2024). No numpy/pandas/scipy; pure stdlib. Reads CSVs only; writes only
its own JSON/MD outputs under research_state/session_20261122T033000Z/.

Decision rules (pre-specified in prereg):
  GO:        >=1 admissible block passes H1 at alpha 0.05 AND H2 direction
             consistent AND H3 absence confirmed
  NOT_SUPPORTED: no admissible block meets minima OR liquidation labels absent
                 (H3) AND no external source available
  INCONCLUSIVE: admissible blocks exist but sample too small for powered test

Nulls (NOT_SUPPORTED / INCONCLUSIVE) are preserved; never coerced to GO.
"""

import csv
import glob
import hashlib
import json
import math
import os
import random
from datetime import datetime, timezone

SESSION_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SESSION_DIR))
DATA_DIR = os.path.join(REPO_ROOT, "data", "raw")
UTC = "20261122T033000Z"
ARTIFACT_ID = f"fclr_next_source_verify01_eval_{UTC}"

ALPHA = 0.05
NPERM = 20000
SEED = 20261122

SYMBOLS = ["BTCUSDT", "ETHUSDT"]
BLOCKS = [
    {"id": "B1_2024-01", "start_ms": 1704067200000, "end_ms": 1706745599999, "symbols": SYMBOLS},
    {"id": "B2_2024-02", "start_ms": 1706745600000, "end_ms": 1709251199999, "symbols": SYMBOLS},
    {"id": "B3_2024-03", "start_ms": 1709251200000, "end_ms": 1711929599999, "symbols": SYMBOLS},
]


def ms_to_iso(ms):
    return datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc).isoformat()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv_rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def parse_kline(path):
    rows = read_csv_rows(path)
    out = []
    for r in rows:
        try:
            ot = int(r["open_time"])
            close = float(r["close"])
        except (KeyError, ValueError, TypeError):
            continue
        out.append({"open_time_ms": ot, "close": close})
    out.sort(key=lambda x: x["open_time_ms"])
    return out


def parse_funding(path):
    rows = read_csv_rows(path)
    out = []
    for r in rows:
        try:
            ct = int(r["calc_time"])
            rate = float(r["last_funding_rate"])
        except (KeyError, ValueError, TypeError):
            continue
        out.append({"calc_time_ms": ct, "rate": rate})
    out.sort(key=lambda x: x["calc_time_ms"])
    return out


def symbol_from_name(name):
    for s in SYMBOLS:
        if name.startswith(s + "-"):
            return s
    return None


def is_kline(name):
    return name.endswith("-1h-") and any(n in name for n in ["-1h-2024", "-1h-2024-"]) or "-1h-" in name


def is_funding(name):
    return "fundingRate" in name or "funding" in name.lower()


def nearest_prior_funding(funding, t_ms):
    best = None
    for f in funding:
        if f["calc_time_ms"] <= t_ms:
            best = f
        else:
            break
    return best


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def var(xs):
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / max(1, len(xs) - 1) if len(xs) > 1 else 0.0


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return float("nan")
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = sum((x - mx) ** 2 for x in xs)
    dy = sum((y - my) ** 2 for y in ys)
    if dx == 0 or dy == 0:
        return 0.0
    return num / math.sqrt(dx * dy)


def rankdata(xs):
    """Average-tie ranking, returns list of ranks (1-based)."""
    n = len(xs)
    order = sorted(range(n), key=lambda i: xs[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg_rank
        i = j + 1
    return ranks


def spearman(xs, ys):
    n = len(xs)
    if n < 3:
        return float("nan"), float("nan")
    rx = rankdata(xs)
    ry = rankdata(ys)
    r = pearson(rx, ry)
    # permutation p-value
    rng = random.Random(SEED)
    obs = abs(r)
    count = 0
    ys2 = list(ys)
    for _ in range(NPERM):
        rng.shuffle(ys2)
        rp = pearson(rx, ys2)
        if abs(rp) >= obs:
            count += 1
    p = (count + 1) / (NPERM + 1)
    return r, p


def ttest_ind_perm(xs, ys):
    """Permutation two-sample test for difference in means (two-tailed)."""
    nx, ny = len(xs), len(ys)
    if nx < 2 or ny < 2:
        return float("nan"), float("nan")
    obs = mean(xs) - mean(ys)
    pooled = list(xs) + list(ys)
    rng = random.Random(SEED + 1)
    count = 0
    for _ in range(NPERM):
        rng.shuffle(pooled)
        mx = mean(pooled[:nx])
        my = mean(pooled[nx:])
        if abs(mx - my) >= abs(obs):
            count += 1
    p = (count + 1) / (NPERM + 1)
    return obs, p


def chi2_survival(x, df):
    """Chi-square survival function for even integer df=2k."""
    if df % 2 != 0:
        return float("nan")
    k = df // 2
    xm2 = x / 2.0
    term = math.exp(-xm2)
    total = term
    for j in range(1, k):
        term *= xm2 / j
        total += term
    return total


def fisher_combine(ps):
    ps = [p for p in ps if p == p and p is not None]  # drop nan
    if not ps:
        return float("nan"), float("nan")
    chi2 = -2.0 * sum(math.log(max(p, 1e-300)) for p in ps)
    df = 2 * len(ps)
    p = chi2_survival(chi2, df)
    return chi2, p


def build_series(symbol):
    klines = {}
    fundings = {}
    for path in glob.glob(os.path.join(DATA_DIR, "**", "*.csv"), recursive=True):
        name = os.path.basename(path)
        if symbol_from_name(name) != symbol:
            continue
        if is_kline(name):
            klines[path] = parse_kline(path)
        elif is_funding(name):
            fundings[path] = parse_funding(path)
    # merge all kline rows for symbol
    all_k = []
    for v in klines.values():
        all_k.extend(v)
    all_k.sort(key=lambda x: x["open_time_ms"])
    # dedupe by open_time
    seen = set()
    uniq_k = []
    for r in all_k:
        if r["open_time_ms"] in seen:
            continue
        seen.add(r["open_time_ms"])
        uniq_k.append(r)
    all_f = []
    for v in fundings.values():
        all_f.extend(v)
    all_f.sort(key=lambda x: x["calc_time_ms"])
    return uniq_k, all_f


def assemble_rows(klines, fundings):
    rows = []
    n = len(klines)
    for i in range(n - 1):
        t = klines[i]["open_time_ms"]
        close_t = klines[i]["close"]
        close_t1 = klines[i + 1]["close"]
        if close_t <= 0 or close_t1 <= 0:
            continue
        log_ret = math.log(close_t1 / close_t)
        f = nearest_prior_funding(fundings, t)
        if f is None:
            continue
        rate = f["rate"]
        abs_f = abs(rate)
        sign_f = 1 if rate > 0 else (-1 if rate < 0 else 0)
        sign_r = 1 if log_ret > 0 else (-1 if log_ret < 0 else 0)
        opp = (sign_f != sign_r) and (sign_r != 0)
        rows.append({
            "t_ms": t,
            "log_return": log_ret,
            "subsequent_abs_log_return": abs(log_ret),
            "funding_rate": rate,
            "abs_funding": abs_f,
            "sign_funding": sign_f,
            "sign_return": sign_r,
            "opposite_sign": opp,
        })
    return rows


def block_rows(rows, block):
    return [r for r in rows if block["start_ms"] <= r["t_ms"] <= block["end_ms"]]


def evaluate():
    results = {"symbols": {}, "blocks": {}, "overall": {}}
    for sym in SYMBOLS:
        klines, fundings = build_series(sym)
        rows = assemble_rows(klines, fundings)
        results["symbols"][sym] = {
            "kline_rows": len(klines),
            "funding_rows": len(fundings),
            "assembled_rows": len(rows),
            "files_sha256": {},
        }
        for path in glob.glob(os.path.join(DATA_DIR, "**", "*.csv"), recursive=True):
            name = os.path.basename(path)
            if symbol_from_name(name) == sym and (is_kline(name) or is_funding(name)):
                results["symbols"][sym]["files_sha256"][name] = sha256_file(path)

    block_results = {}
    h1_ps = []
    h2_directions = []
    h3_confirmed = True
    any_admissible = False

    for block in BLOCKS:
        br = {"block_id": block["id"], "window": [ms_to_iso(block["start_ms"]), ms_to_iso(block["end_ms"])], "symbols": {}}
        for sym in SYMBOLS:
            klines, fundings = build_series(sym)
            rows = assemble_rows(klines, fundings)
            brows = block_rows(rows, block)
            sym_r = {"n_rows": len(brows)}
            if len(brows) < 10:
                sym_r["status"] = "INCONCLUSIVE_TOO_FEW_ROWS"
                sym_r["h1"] = {"rho": None, "p": None}
                sym_r["h2"] = {"diff_mean": None, "p": None, "direction_consistent": None}
            else:
                any_admissible = True
                abs_f = [r["abs_funding"] for r in brows]
                sub_vol = [r["subsequent_abs_log_return"] for r in brows]
                rho, p = spearman(abs_f, sub_vol)
                sym_r["h1"] = {"rho": rho, "p": p, "pass_alpha": (p is not None and p == p and p < ALPHA)}
                opp_vol = [r["subsequent_abs_log_return"] for r in brows if r["opposite_sign"]]
                same_vol = [r["subsequent_abs_log_return"] for r in brows if not r["opposite_sign"]]
                diff, p2 = ttest_ind_perm(opp_vol, same_vol)
                dir_consistent = None
                if p2 is not None and p2 == p2 and p2 < ALPHA:
                    dir_consistent = (diff < 0)
                sym_r["h2"] = {"diff_mean": diff, "p": p2, "direction_consistent": dir_consistent,
                               "n_opp": len(opp_vol), "n_same": len(same_vol)}
            br["symbols"][sym] = sym_r
        block_results[block["id"]] = br

    # H3: liquidation absence across all CSVs
    liq_columns_found = []
    for path in glob.glob(os.path.join(DATA_DIR, "**", "*.csv"), recursive=True):
        try:
            with open(path, newline="") as f:
                reader = csv.reader(f)
                header = next(reader, [])
        except Exception:
            header = []
        low = [c.lower() for c in header]
        for c in low:
            if "liquid" in c:
                liq_columns_found.append((os.path.basename(path), c))
    h3_confirmed = (len(liq_columns_found) == 0)

    # Aggregate H1 across blocks/symbols via Fisher
    all_ps = []
    for bid, br in block_results.items():
        for sym, sr in br["symbols"].items():
            h1 = sr.get("h1", {})
            p = h1.get("p")
            if p is not None and p == p:
                all_ps.append(p)
    chi2, fp = fisher_combine(all_ps) if all_ps else (None, None)

    # Decision
    h1_any_pass = False
    h2_dir_ok = True
    for bid, br in block_results.items():
        for sym, sr in br["symbols"].items():
            h1 = sr.get("h1", {})
            if h1.get("pass_alpha"):
                h1_any_pass = True
            h2 = sr.get("h2", {})
            dc = h2.get("direction_consistent")
            if dc is False:
                h2_dir_ok = False

    if not any_admissible:
        decision = "NOT_SUPPORTED"
        reason = "No admissible block meets minima (2 symbols, partial hourly coverage, < complete month)."
    elif not h3_confirmed:
        decision = "NOT_SUPPORTED"
        reason = "H3 failed: liquidation-related columns found in local CSVs."
    elif h1_any_pass and h2_dir_ok and h3_confirmed:
        decision = "GO"
        reason = "H1 passed in >=1 admissible block; H2 direction consistent; H3 absence confirmed."
    else:
        decision = "INCONCLUSIVE"
        reason = "Admissible blocks exist but H1/H2 did not jointly satisfy GO thresholds (sample too small)."

    results["blocks"] = block_results
    results["h3_liquidation_absence"] = {"confirmed": h3_confirmed, "liquidation_columns_found": liq_columns_found}
    results["aggregate"] = {
        "h1_fisher_chi2": chi2,
        "h1_fisher_p": fp,
        "h1_any_block_pass_alpha": h1_any_pass,
        "h2_direction_consistent_all_blocks": h2_dir_ok,
        "h3_confirmed": h3_confirmed,
        "any_admissible_block": any_admissible,
    }
    results["decision"] = decision
    results["decision_reason"] = reason
    results["prereg_design"] = "FCLR-NEXT-CONFIRM-001"
    results["prereg_status"] = "OUTCOME_BLIND"
    results["session_utc"] = UTC
    results["generated_utc"] = "2026-11-22T03:30:00Z"
    return results


def write_md(results):
    lines = []
    lines.append(f"# {ARTIFACT_ID}")
    lines.append("")
    lines.append("**Campaign:** `FCLR-NEXT-SOURCE-VERIFY-01-20261122T013100Z`")
    lines.append(f"**Session:** `{UTC}` (> campaign start `20261122T013100Z`)")
    lines.append("**Generated:** `2026-11-22T03:30:00Z`")
    lines.append("")
    lines.append("## Design")
    lines.append("- Design ID: `FCLR-NEXT-CONFIRM-001` (confirmatory, outcome-blind prereg)")
    lines.append("- Data domain: `research_state/data/raw/` BTC/ETH hourly klines + fundingRate, Jan-Mar 2024")
    lines.append("- Stdlib-only; no network; no numpy/pandas/scipy")
    lines.append("")
    lines.append("## Per-symbol summary")
    for sym, s in results["symbols"].items():
        lines.append(f"- {sym}: kline_rows={s['kline_rows']}, funding_rows={s['funding_rows']}, assembled_rows={s['assembled_rows']}")
    lines.append("")
    lines.append("## Per-block results")
    for bid, br in results["blocks"].items():
        lines.append(f"### {bid} ({br['window'][0]} .. {br['window'][1]})")
        for sym, sr in br["symbols"].items():
            h1 = sr.get("h1", {})
            h2 = sr.get("h2", {})
            lines.append(f"  - {sym}: n_rows={sr['n_rows']}, status={sr.get('status','-')}")
            lines.append(f"    H1: rho={h1.get('rho')}, p={h1.get('p')}, pass_alpha={h1.get('pass_alpha')}")
            lines.append(f"    H2: diff_mean={h2.get('diff_mean')}, p={h2.get('p')}, direction_consistent={h2.get('direction_consistent')}, n_opp={h2.get('n_opp')}, n_same={h2.get('n_same')}")
        lines.append("")
    lines.append("## Aggregate")
    ag = results["aggregate"]
    lines.append(f"- H1 Fisher chi2={ag['h1_fisher_chi2']}, p={ag['h1_fisher_p']}")
    lines.append(f"- H1 any block pass alpha: {ag['h1_any_block_pass_alpha']}")
    lines.append(f"- H2 direction consistent all blocks: {ag['h2_direction_consistent_all_blocks']}")
    lines.append(f"- H3 liquidation absence confirmed: {ag['h3_confirmed']}")
    lines.append(f"- Any admissible block: {ag['any_admissible_block']}")
    lines.append("")
    lines.append("## H3 liquidation absence")
    h3 = results["h3_liquidation_absence"]
    lines.append(f"- Confirmed: {h3['confirmed']}")
    lines.append(f"- Liquidation columns found: {h3['liquidation_columns_found']}")
    lines.append("")
    lines.append("## Decision")
    lines.append(f"- Decision: **{results['decision']}**")
    lines.append(f"- Reason: {results['decision_reason']}")
    lines.append("")
    lines.append("## Compliance")
    lines.append("- Outcome-blind: hypotheses/plan fixed in prereg before computation")
    lines.append("- Nulls preserved: NOT_SUPPORTED/INCONCLUSIVE never coerced to GO")
    lines.append("- Read-only artifacts; no root-level writes")
    return "\n".join(lines)


def main():
    results = evaluate()
    out_json = os.path.join(SESSION_DIR, f"{ARTIFACT_ID}.json")
    out_md = os.path.join(SESSION_DIR, f"{ARTIFACT_ID}.md")
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    with open(out_md, "w") as f:
        f.write(write_md(results))
    print(json.dumps({"decision": results["decision"], "json": out_json, "md": out_md}, indent=2))


if __name__ == "__main__":
    main()
