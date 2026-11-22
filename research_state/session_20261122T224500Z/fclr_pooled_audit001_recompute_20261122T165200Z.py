#!/usr/bin/env python3
"""FCLR-POOLED-AUDIT-001 independent stdlib recompute.

Independent recompute of the adversarial audit with a materially different
methodology (strict exact-timestamp alignment, daily RV stress, positive-only
liquidation median, 5% breach band). Stdlib + pyarrow only; asserts
.parquet.sha256 sidecars before every read; read-only caches; no network.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
import sys
from pathlib import Path

import pyarrow.parquet as pq

REPO = Path(__file__).resolve().parents[2]
BASE = REPO / "research_state" / "data_cache" / "ironflow_bulk"
SESSION_UTC = "20261122T165200Z"
MONTHS = [f"2025-{m:02d}" for m in range(5, 13)] + [f"2026-{m:02d}" for m in range(1, 11)]
TRAIN_FRAC = 0.70
BREACH_BAND = 0.05  # 40x leverage-style band, robustness variant of the 2.5% audit band
HORIZONS_H = (6, 24, 72, 168)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_month(dataset: str, month: str):
    parquet = BASE / dataset / f"{month}.parquet"
    sidecar = BASE / dataset / f"{month}.parquet.sha256"
    expected = sidecar.read_text(encoding="utf-8").strip().split()[0]
    actual = sha256_file(parquet)
    if actual != expected:
        raise ValueError(f"sha256 mismatch {dataset}/{month}")
    return pq.read_table(parquet)


def hour_of(ts: dt.datetime) -> dt.datetime:
    return ts.replace(minute=0, second=0, microsecond=0)


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def main() -> int:
    out = {
        "experiment_id": "FCLR-POOLED-AUDIT-001",
        "campaign": "FCLR-POOLED-AUDIT-001-20261122T120000Z",
        "session_utc": SESSION_UTC,
        "recompute_type": "independent_stdlib_recompute",
        "software": "stdlib + pyarrow only; numpy/pandas/scipy not used",
        "findings": {},
    }

    # Panel clock + train/test boundary (independent: strict hour floor)
    hours = set()
    for month in MONTHS:
        ct = read_month("candles_1h", month)
        for ts in ct.column("timestamp").to_pylist():
            hours.add(hour_of(ts))
        del ct
    sorted_hours = sorted(hours)
    cut = sorted_hours[max(1, int(math.floor(TRAIN_FRAC * len(sorted_hours)))) - 1]
    train_h = set(sorted_hours[: sorted_hours.index(cut) + 1])
    test_h = set(sorted_hours[sorted_hours.index(cut) + 1:])

    # ---- D3': strict exact-timestamp funding-return correlation ------------
    lag_corrs = []
    fwd_corrs = []
    exact_pairs_total = 0
    markets_with_strict_pairs = 0
    for month in MONTHS:
        ct = read_month("candles_1h", month)
        c_ts = ct.column("timestamp").to_pylist()
        c_market = ct.column("market").to_pylist()
        c_close = ct.column("close").to_pylist()
        close_by_key = {(c_market[i], c_ts[i]): c_close[i] for i in range(len(c_ts))}
        per_market_ts: dict[str, list[dt.datetime]] = {}
        per_market_close: dict[str, list[float]] = {}
        for i in range(len(c_ts)):
            per_market_ts.setdefault(c_market[i], []).append(c_ts[i])
            per_market_close.setdefault(c_market[i], []).append(c_close[i])
        ft = read_month("funding", month)
        f_ts = ft.column("timestamp").to_pylist()
        f_market = ft.column("market").to_pylist()
        f_rate = ft.column("funding_rate").to_pylist()
        per_market: dict[str, dict] = {}
        for i in range(len(f_ts)):
            r = f_rate[i]
            if r is None or r != r:
                continue
            key = (f_market[i], f_ts[i])
            cnow = close_by_key.get(key)
            if cnow is None or cnow <= 0:
                continue
            m = f_market[i]
            ts = f_ts[i]
            ts_list = per_market_ts[m]
            close_list = per_market_close[m]
            lo, hi = 0, len(ts_list)
            while lo < hi:
                mid = (lo + hi) // 2
                if ts_list[mid] <= ts:
                    lo = mid + 1
                else:
                    hi = mid
            pos = lo
            if pos == 0:
                continue
            cprev = close_list[pos - 1]
            if cprev <= 0:
                continue
            ret_lag = math.log(cnow / cprev)
            st = per_market.setdefault(m, {"nr": 0, "sr": 0.0, "sr2": 0.0,
                                           "nl": 0, "sl": 0.0, "sl2": 0.0,
                                           "srl": 0.0, "nf": 0, "sf": 0.0,
                                           "sf2": 0.0, "sfwd": 0.0, "sfwd2": 0.0,
                                           "sfr": 0.0})
            # lag: funding_t vs return into t
            st["nl"] += 1
            st["sl"] += r
            st["sl2"] += r * r
            st["srl"] += ret_lag
            st["srl2"] = st.get("srl2", 0.0) + ret_lag * ret_lag
            st["sfr"] += r * ret_lag
            # fwd: funding_t vs return out of t (next candle of same market)
            if pos < len(ts_list):
                cnext = close_list[pos]
                if cnext > 0:
                    ret_fwd = math.log(cnext / cnow)
                    st["nf"] += 1
                    st["sf"] += r
                    st["sf2"] += r * r
                    st["sfwd"] += ret_fwd
                    st["sfwd2"] += ret_fwd * ret_fwd
                    st["sfr"] = st.get("sfr", 0.0)  # keep lag cov separate below
                    st["sfrwd"] = st.get("sfrwd", 0.0) + r * ret_fwd
        del ct
        del ft
        for m, st in per_market.items():
            n = st["nl"]
            exact_pairs_total += n
            if n >= 20:
                markets_with_strict_pairs += 1
                mf = st["sr"] / n
                ml_ = st["sl"] / n
                vf = st["sr2"] / n - mf * mf
                vl = st.get("srl2", 0.0) / n - ml_ * ml_
                cov = st.get("sfr", 0.0) / n - mf * ml_
                if vf > 0 and vl > 0:
                    lag_corrs.append(cov / math.sqrt(vf * vl))
            nf = st.get("nf", 0)
            if nf >= 20:
                mf = st["sf"] / nf
                mfr = st["sfwd"] / nf
                vf = st["sf2"] / nf - mf * mf
                vr = st["sfwd2"] / nf - mfr * mfr
                cov = st.get("sfrwd", 0.0) / nf - mf * mfr
                if vf > 0 and vr > 0:
                    fwd_corrs.append(cov / math.sqrt(vf * vr))

    out["findings"]["d3_recompute"] = {
        "mean_corr_lag_strict": mean(lag_corrs),
        "mean_corr_fwd_strict": mean(fwd_corrs),
        "n_markets_lag": len(lag_corrs),
        "n_markets_fwd": len(fwd_corrs),
        "strict_exact_pairs_total": exact_pairs_total,
        "markets_with_ge20_strict_pairs": markets_with_strict_pairs,
        "strict_alignment_estimable": bool(markets_with_strict_pairs > 0),
        "agrees_with_audit_publication_lead": bool(markets_with_strict_pairs > 0
                                                   and mean(fwd_corrs) > mean(lag_corrs)),
    }

    # ---- D8': daily RV stress concentration -------------------------------
    daily_rv: dict[str, list[float]] = {}
    for month in MONTHS:
        ct = read_month("candles_1h", month)
        c_market = ct.column("market").to_pylist()
        c_high = ct.column("high").to_pylist()
        c_low = ct.column("low").to_pylist()
        c_close = ct.column("close").to_pylist()
        c_ts = ct.column("timestamp").to_pylist()
        for i in range(len(c_ts)):
            d = c_ts[i].date()
            m = c_market[i]
            h = c_high[i]
            l = c_low[i]
            c = c_close[i]
            if h and l and c and h > 0 and l > 0 and c > 0:
                daily_rv.setdefault((m, d), []).append((h - l) / c)
        del ct
    all_daily = [rv for vlist in daily_rv.values() for rv in vlist]
    all_daily.sort()
    n_d = len(all_daily)
    thr = all_daily[max(0, min(n_d - 1, int(math.floor(0.99 * (n_d - 1)))))]
    per_market_stress: dict[str, int] = {}
    n_stress = 0
    for (m, _), vlist in daily_rv.items():
        for rv in vlist:
            if rv >= thr:
                n_stress += 1
                per_market_stress[m] = per_market_stress.get(m, 0) + 1
    counts = sorted(per_market_stress.values(), reverse=True)
    tot = sum(counts)
    out["findings"]["d8_recompute"] = {
        "n_daily_rv_obs": n_d,
        "daily_stress_threshold_p99": thr,
        "n_stress_days": n_stress,
        "top_market_share_of_stress": (counts[0] / tot) if tot else float("nan"),
        "top3_share": (sum(counts[:3]) / tot) if tot else float("nan"),
        "stress_not_single_coin_dominated": bool((counts[0] / tot) <= 0.25) if tot else None,
        "agrees_with_audit": bool((counts[0] / tot) <= 0.25) if tot else None,
    }

    # ---- D6'/D7': coin identity and survivorship from funding table -------
    coins_by_month: list[set[str]] = []
    for month in MONTHS:
        ft = read_month("funding", month)
        coins_by_month.append(set(ft.column("coin").to_pylist()))
        del ft
    first_c = coins_by_month[0]
    last_c = coins_by_month[-1]
    all_c = set().union(*coins_by_month)
    surv = set(all_c)
    for s in coins_by_month:
        surv &= s
    out["findings"]["d67_recompute"] = {
        "distinct_coins_all_months": len(all_c),
        "coins_first_month": len(first_c),
        "coins_last_month": len(last_c),
        "coins_absent_last_month": len(first_c - last_c),
        "coins_new_last_month": len(last_c - first_c),
        "survivor_coins": len(surv),
        "survivor_share_last_month": (len(surv & last_c) / len(last_c)) if last_c else float("nan"),
        "agrees_with_audit_survivorship_bias_present": bool(len(last_c - first_c) > 0),
    }

    # ---- D10': label overlap with positive-only train median --------------
    notional: dict[tuple[str, dt.datetime], float] = {}
    for month in MONTHS:
        lt = read_month("liquidations", month)
        l_ts = lt.column("timestamp").to_pylist()
        l_market = lt.column("market").to_pylist()
        l_not = lt.column("notional_usd").to_pylist()
        for i in range(len(l_ts)):
            v = l_not[i]
            if v is None or v != v:
                continue
            key = (l_market[i], hour_of(l_ts[i]))
            notional[key] = notional.get(key, 0.0) + v
        del lt
    train_vals = sorted(v for (m, h), v in notional.items() if h in train_h and v > 0)
    med = train_vals[len(train_vals) // 2] if train_vals else 0.0

    def fwd(market, hour, h):
        total = 0.0
        for k in range(1, h + 1):
            total += notional.get((market, hour + dt.timedelta(hours=k)), 0.0)
        return total

    labels: dict[int, set] = {h: set() for h in HORIZONS_H}
    for (market, hour) in notional:
        if hour not in test_h:
            continue
        for h in HORIZONS_H:
            if fwd(market, hour, h) > med:
                labels[h].add((market, hour))

    def jac(a, b):
        if not a and not b:
            return float("nan")
        return len(a & b) / len(a | b)

    overlap = {}
    hs = list(HORIZONS_H)
    for i in range(len(hs)):
        for hb in hs[i + 1:]:
            overlap[f"{hs[i]}h_vs_{hb}h"] = jac(labels[hs[i]], labels[hb])
    out["findings"]["d10_recompute"] = {
        "train_median_positive_notional": med,
        "label_counts": {f"{h}h": len(labels[h]) for h in HORIZONS_H},
        "pairwise_jaccard": overlap,
        "non_independent_outcomes": bool(any(v > 0.5 for v in overlap.values() if v == v)),
    }

    # ---- Track B': 5% band robustness -------------------------------------
    # funding tercile thresholds from train hours (market level)
    train_fund: dict[str, list[float]] = {}
    last_fund: dict[str, float] = {}
    for month in MONTHS:
        ft = read_month("funding", month)
        f_ts = ft.column("timestamp").to_pylist()
        f_market = ft.column("market").to_pylist()
        f_rate = ft.column("funding_rate").to_pylist()
        for i in range(len(f_ts)):
            r = f_rate[i]
            if r is None or r != r:
                continue
            last_fund[f_market[i]] = abs(r)
            if hour_of(f_ts[i]) in train_h:
                train_fund.setdefault(f_market[i], []).append(abs(r))
        del ft
    thr_by_m: dict[str, tuple[float, float]] = {}
    for m, vals in train_fund.items():
        if len(vals) < 10:
            continue
        vals.sort()
        k = len(vals)
        thr_by_m[m] = (vals[max(0, min(k - 1, int(math.floor(0.33 * (k - 1)))))],
                       vals[max(0, min(k - 1, int(math.floor(0.66 * (k - 1)))))])
    tb = {"low": [0, 0], "mid": [0, 0], "high": [0, 0], "unlabeled": [0, 0]}
    tot_n = tot_b = 0
    last_close: dict[str, float] = {}
    last_fund2: dict[str, float] = {}
    for month in MONTHS:
        ct = read_month("candles_1h", month)
        c_ts = ct.column("timestamp").to_pylist()
        c_market = ct.column("market").to_pylist()
        c_close = ct.column("close").to_pylist()
        ft = read_month("funding", month)
        f_ts = ft.column("timestamp").to_pylist()
        f_market = ft.column("market").to_pylist()
        f_rate = ft.column("funding_rate").to_pylist()
        fi = 0
        for i in range(len(c_ts)):
            m = c_market[i]
            ts = c_ts[i]
            c = c_close[i]
            while fi < len(f_ts) and f_ts[fi] <= ts:
                r = f_rate[fi]
                if r is not None and r == r:
                    last_fund2[f_market[fi]] = r
                fi += 1
            pc = last_close.get(m)
            if pc and c and c > 0 and pc > 0 and hour_of(ts) in test_h:
                ret_abs = abs(math.log(c / pc))
                th = thr_by_m.get(m)
                if th is None:
                    terc = "unlabeled"
                elif ret_abs != ret_abs:
                    terc = "unlabeled"
                else:
                    fv = last_fund2.get(m)
                    terc = "unlabeled" if fv is None or fv != fv else (
                        "low" if fv <= th[0] else ("mid" if fv <= th[1] else "high"))
                tb[terc][0] += 1
                tot_n += 1
                if ret_abs >= BREACH_BAND:
                    tb[terc][1] += 1
                    tot_b += 1
            last_close[m] = c if c and c > 0 else last_close.get(m)
        del ct
        del ft
    rates = {k: (v[1] / v[0] if v[0] else float("nan")) for k, v in tb.items()}
    out["findings"]["trackb_recompute"] = {
        "breach_band": BREACH_BAND,
        "test_market_hours_evaluated": tot_n,
        "modeled_breach_count": tot_b,
        "modeled_breach_rate": (tot_b / tot_n) if tot_n else float("nan"),
        "by_tercile_rate": rates,
        "high_tercile_above_low": bool(rates["high"] == rates["high"] and rates["low"] == rates["low"]
                                      and rates["high"] > rates["low"]),
        "label_kind": "modeled boundary-breach proxy (NOT observed liquidation)",
    }

    verdicts = {
        "d3_strict_exact_alignment": "not_estimable"
        if markets_with_strict_pairs == 0
        else ("publication_lead_reproduced"
              if mean(fwd_corrs) > mean(lag_corrs) else "direction_disagrees"),
        "d3_strict_exact_pairs_total": exact_pairs_total,
        "d3_markets_with_ge20_strict_pairs": markets_with_strict_pairs,
        "d8_no_single_coin_stress_dominance_reproduced": out["findings"]["d8_recompute"]["agrees_with_audit"],
        "d67_survivorship_bias_reproduced": out["findings"]["d67_recompute"]["agrees_with_audit_survivorship_bias_present"],
        "d10_non_independent_outcomes_reproduced": out["findings"]["d10_recompute"]["non_independent_outcomes"],
        "trackb_tercile_ordering_robust": out["findings"]["trackb_recompute"]["high_tercile_above_low"],
    }
    out["verdicts"] = verdicts
    out["all_verified"] = bool(
        verdicts["d8_no_single_coin_stress_dominance_reproduced"]
        and verdicts["d67_survivorship_bias_reproduced"]
        and verdicts["d10_non_independent_outcomes_reproduced"]
        and verdicts["trackb_tercile_ordering_robust"]
    )

    out_json = REPO / "research_state" / f"session_{SESSION_UTC}" / f"fclr_pooled_audit001_recompute_{SESSION_UTC}.json"
    out_py = REPO / "research_state" / f"session_{SESSION_UTC}" / f"fclr_pooled_audit001_recompute_{SESSION_UTC}.py"
    # The .py is this script itself (already written); record its hash
    out["source_script"] = f"fclr_pooled_audit001_recompute_{SESSION_UTC}.py"
    out["source_script_sha256"] = sha256_file(out_py)
    out_json.write_text(json.dumps(out, indent=2, default=str) + "\n", encoding="utf-8")
    print(f"[FCLR-POOLED-AUDIT-001] recompute complete: {SESSION_UTC}")
    print(f"  json: {out_json}")
    print(f"  all_verified: {out['all_verified']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
