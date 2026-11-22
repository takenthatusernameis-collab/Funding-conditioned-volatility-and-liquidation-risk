#!/usr/bin/env python3
"""FCLR-POOLED-AUDIT-001 adversarial leakage/quality audit implementation.

Stdlib + pyarrow only (numpy/pandas/scipy NOT used). Reads on-disk
ironflow bulk parquet under research_state/data_cache/ironflow_bulk/,
asserts the .parquet.sha256 sidecar before every read, never mutates the
caches, uses no network and no new source. Ten adversarial audit domains
plus Track B modeled boundary-breach labels (clearly a modeled proxy, never
an observed liquidation).

Run:
  python3 research_state/session_20261122T165200Z/fclr_pooled_audit001_audit_20261122T165200Z.py
"""
from __future__ import annotations

import array
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
PURGE_HOURS = 24
EMBARGO_HOURS = 24
STRESS_Q = 0.99
BREACH_BAND = 0.025  # modeled 20x leverage, 50% maintenance: (1 - 0.5) / 20 = 2.5%
HORIZONS_H = (6, 24, 72, 168)
TOLERANCE = 0.01


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_month(dataset: str, month: str):
    parquet = BASE / dataset / f"{month}.parquet"
    sidecar = BASE / dataset / f"{month}.parquet.sha256"
    if not parquet.is_file():
        raise FileNotFoundError(parquet)
    if not sidecar.is_file():
        raise FileNotFoundError(sidecar)
    expected = sidecar.read_text(encoding="utf-8").strip().split()[0]
    actual = sha256_file(parquet)
    if actual != expected:
        raise ValueError(f"sha256 mismatch {dataset}/{month}: expected {expected} got {actual}")
    return pq.read_table(parquet)


def hour_of(ts: dt.datetime) -> dt.datetime:
    return ts.replace(minute=0, second=0, microsecond=0)


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")


def pctile(vals: list[float], q: float) -> float:
    vals = sorted(vals)
    k = len(vals)
    if k == 0:
        return float("nan")
    return vals[max(0, min(k - 1, int(math.floor(q * (k - 1)))))]


def main() -> int:
    results: dict = {
        "experiment_id": "FCLR-POOLED-AUDIT-001",
        "campaign": "FCLR-POOLED-AUDIT-001-20261122T120000Z",
        "session_utc": SESSION_UTC,
        "audit_type": "adversarial_leakage_quality_audit",
        "software": "stdlib + pyarrow only; numpy/pandas/scipy not used",
        "data": "ironflow_bulk {candles_1h,funding,open_interest,liquidations} 18 months 2025-05..2026-10",
        "domains": {},
    }

    # ===== Pass 1: candles only (clock, D1, D8 samples, D6/D7 coin sets, D5 nulls) =====
    all_hours: set[dt.datetime] = set()
    coin_months: list[set[str]] = []
    d1_within_vios = 0
    d1_overlap_markets: set[str] = set()
    prev_ts_by_market: dict[str, dt.datetime] = {}
    prev_month_last_by_market: dict[str, dt.datetime] = {}
    rv_values: array.array = array.array("d")
    rv_market_idx: array.array = array.array("I")
    market_index: dict[str, int] = {}
    per_month_rows: dict[str, dict[str, int]] = {}
    per_month_nulls: dict[str, dict[str, dict[str, int]]] = {}

    for month in MONTHS:
        ct = read_month("candles_1h", month)
        c_ts = ct.column("timestamp").to_pylist()
        c_market = ct.column("market").to_pylist()
        c_coin = ct.column("coin").to_pylist()
        c_open = ct.column("open").to_pylist()
        c_high = ct.column("high").to_pylist()
        c_low = ct.column("low").to_pylist()
        c_close = ct.column("close").to_pylist()
        n_c = len(c_ts)
        per_month_rows.setdefault("candles_1h", {})[month] = n_c
        per_month_nulls.setdefault("candles_1h", {})[month] = {
            col: int(ct.column(col).null_count) for col in ct.schema.names
        }
        all_hours.update(hour_of(ts) for ts in c_ts)
        coin_months.append(set(c_coin))
        for i in range(n_c):
            ts = c_ts[i]
            m = c_market[i]
            o = c_open[i]
            h = c_high[i]
            l = c_low[i]
            c = c_close[i]
            pts = prev_ts_by_market.get(m)
            if pts is not None and ts < pts:
                d1_within_vios += 1
            prev_ts_by_market[m] = ts
            if o and o > 0:
                rv = (h - l) / o
                if rv == rv:
                    mi = market_index.setdefault(m, len(market_index))
                    rv_values.append(rv)
                    rv_market_idx.append(mi)
        pfl: dict[str, tuple[dt.datetime, dt.datetime]] = {}
        for m in set(c_market):
            pfl[m] = (c_ts[0], c_ts[-1]) if n_c else (None, None)
        for m, (f, _) in pfl.items():
            plast = prev_month_last_by_market.get(m)
            if plast is not None and f is not None and f < plast:
                d1_overlap_markets.add(m)
        prev_month_last_by_market = {m: v[1] for m, v in pfl.items() if v[1] is not None}
        del ct

    sorted_hours = sorted(all_hours)
    n_h = len(sorted_hours)
    cutoff_idx = max(1, int(math.floor(TRAIN_FRAC * n_h)))
    train_end = sorted_hours[cutoff_idx - 1]
    test_start = sorted_hours[cutoff_idx]
    train_hours = set(sorted_hours[:cutoff_idx])
    test_hours = set(sorted_hours[cutoff_idx:])
    gap_hours = (test_start - train_end).total_seconds() / 3600.0
    purge_ok = gap_hours >= (PURGE_HOURS + EMBARGO_HOURS) and test_start > train_end

    results["domains"]["d2_split_embargo"] = {
        "distinct_hours": n_h,
        "train_frac": TRAIN_FRAC,
        "train_hours": len(train_hours),
        "test_hours": len(test_hours),
        "train_end_utc": train_end.isoformat(),
        "test_start_utc": test_start.isoformat(),
        "gap_hours": gap_hours,
        "purge_plus_embargo_hours": PURGE_HOURS + EMBARGO_HOURS,
        "embargo_integrity": bool(purge_ok),
        "no_train_test_overlap": bool(min(test_hours) > max(train_hours)),
    }

    # ===== Pass 2: all four datasets (D3, D4, D5, D7, D9, D10) =====
    d3: dict[str, dict] = {}
    last_close: dict[str, float] = {}
    last_funding: dict[str, float] = {}
    prev_interval: dict[str, tuple[float, float | None]] = {}
    trackb_train_funding: dict[str, list[float]] = {}
    fund_surv: list[float] = []
    fund_non: list[float] = []
    funding_sign_pos = funding_sign_neg = funding_sign_zero = funding_n = 0
    d9: dict[str, list[tuple[str, float, float]]] = {}
    d4_rows = 0
    d4_max_premium = 0.0
    d4_over_tol = 0
    d4_market_max: dict[str, float] = {}
    d10_notional: dict[tuple[str, dt.datetime], float] = {}
    d10_events = 0

    universe_by_month = coin_months
    first_coins = universe_by_month[0]
    last_coins = universe_by_month[-1]
    all_coins = set().union(*universe_by_month)
    survivors = set(all_coins)
    for s in universe_by_month:
        survivors &= s
    market_coin_sets: dict[str, set[str]] = {}

    for month in MONTHS:
        # candles: D3 funding-timing pairs + Track B inputs + market-coin identity
        ct = read_month("candles_1h", month)
        c_ts = ct.column("timestamp").to_pylist()
        c_market = ct.column("market").to_pylist()
        c_coin = ct.column("coin").to_pylist()
        c_close = ct.column("close").to_pylist()
        for i in range(len(c_ts)):
            m = c_market[i]
            ts = c_ts[i]
            c = c_close[i]
            market_coin_sets.setdefault(m, set()).add(c_coin[i])
            pc = last_close.get(m)
            if pc is not None and c and c > 0 and pc > 0:
                ret = math.log(c / pc)
                pf = prev_interval.get(m)
                if pf is not None and pf[0] is not None and pf[1] is not None:
                    st = d3.setdefault(m, {"n_lag": 0, "n_fwd": 0, "sum_f": 0.0, "sum_f2": 0.0,
                                           "sum_rl": 0.0, "sum_rl2": 0.0, "sum_rf": 0.0,
                                           "sum_rf2": 0.0, "sum_frl": 0.0, "sum_frf": 0.0})
                    st["n_fwd"] += 1
                    st["sum_f"] += pf[1]
                    st["sum_f2"] += pf[1] * pf[1]
                    st["sum_rf"] += ret
                    st["sum_rf2"] += ret * ret
                    st["sum_frf"] += pf[1] * ret
                lf = last_funding.get(m)
                if lf is not None:
                    st = d3.setdefault(m, {"n_lag": 0, "n_fwd": 0, "sum_f": 0.0, "sum_f2": 0.0,
                                           "sum_rl": 0.0, "sum_rl2": 0.0, "sum_rf": 0.0,
                                           "sum_rf2": 0.0, "sum_frl": 0.0, "sum_frf": 0.0})
                    st["n_lag"] += 1
                    st["sum_f"] += lf
                    st["sum_f2"] += lf * lf
                    st["sum_rl"] += ret
                    st["sum_rl2"] += ret * ret
                    st["sum_frl"] += lf * ret
                prev_interval[m] = (c, last_funding.get(m))
            last_close[m] = c if (c and c > 0) else last_close.get(m)
            if m not in prev_interval:
                prev_interval[m] = (last_close.get(m), last_funding.get(m))
        del ct

        # funding: D5 nulls, D7 survivorship means, D9 monthly terciles, Track B train funding
        ft = read_month("funding", month)
        f_ts = ft.column("timestamp").to_pylist()
        f_market = ft.column("market").to_pylist()
        f_coin = ft.column("coin").to_pylist()
        f_rate = ft.column("funding_rate").to_pylist()
        per_month_rows.setdefault("funding", {})[month] = len(f_ts)
        per_month_nulls.setdefault("funding", {})[month] = {
            col: int(ft.column(col).null_count) for col in ft.schema.names
        }
        monthly_abs: dict[str, list[float]] = {}
        for i in range(len(f_ts)):
            ts = f_ts[i]
            m = f_market[i]
            r = f_rate[i]
            coin = f_coin[i]
            if r is None or r != r:
                continue
            funding_n += 1
            if r > 0:
                funding_sign_pos += 1
            elif r < 0:
                funding_sign_neg += 1
            else:
                funding_sign_zero += 1
            last_funding[m] = r
            av = abs(r)
            if hour_of(ts) in train_hours:
                trackb_train_funding.setdefault(m, []).append(av)
            monthly_abs.setdefault(m, []).append(av)
            if coin in survivors:
                fund_surv.append(av)
            else:
                fund_non.append(av)
        for m, vals in monthly_abs.items():
            d9.setdefault(m, []).append((month, pctile(vals, 0.33), pctile(vals, 0.66)))
        del ft

        # open_interest: D4 mark vs oracle(index) alignment
        ot = read_month("open_interest", month)
        o_market = ot.column("market").to_pylist()
        o_mark = ot.column("mark_price").to_pylist()
        o_oracle = ot.column("oracle_price").to_pylist()
        per_month_rows.setdefault("open_interest", {})[month] = len(o_market)
        per_month_nulls.setdefault("open_interest", {})[month] = {
            col: int(ot.column(col).null_count) for col in ot.schema.names
        }
        for i in range(len(o_market)):
            mark = o_mark[i]
            oracle = o_oracle[i]
            if mark is None or mark != mark or oracle is None or oracle != oracle or oracle <= 0:
                continue
            d4_rows += 1
            prem = abs(mark - oracle) / oracle
            if prem > d4_max_premium:
                d4_max_premium = prem
            if prem > TOLERANCE:
                d4_over_tol += 1
            cur = d4_market_max.get(o_market[i], 0.0)
            if prem > cur:
                d4_market_max[o_market[i]] = prem
        del ot

        # liquidations: D10 notional per market-hour
        lt = read_month("liquidations", month)
        l_ts = lt.column("timestamp").to_pylist()
        l_market = lt.column("market").to_pylist()
        l_notional = lt.column("notional_usd").to_pylist()
        per_month_rows.setdefault("liquidations", {})[month] = len(l_ts)
        per_month_nulls.setdefault("liquidations", {})[month] = {
            col: int(lt.column(col).null_count) for col in lt.schema.names
        }
        for i in range(len(l_ts)):
            notional = l_notional[i]
            if notional is None or notional != notional:
                continue
            d10_events += 1
            key = (l_market[i], hour_of(l_ts[i]))
            d10_notional[key] = d10_notional.get(key, 0.0) + notional
        del lt

    # ---- D1 ---------------------------------------------------------------
    results["domains"]["d1_future_row_perturbation"] = {
        "within_file_monotonicity_violations": d1_within_vios,
        "markets_with_cross_file_overlap": len(d1_overlap_markets),
        "overlap_markets_sample": sorted(d1_overlap_markets)[:10],
        "no_look_ahead_from_row_order": bool(d1_within_vios == 0),
    }

    # ---- D3 ---------------------------------------------------------------
    corr_lags: list[float] = []
    corr_fwds: list[float] = []
    n_lag_pairs = n_fwd_pairs = 0
    markets_lag = markets_fwd = 0
    for m, st in d3.items():
        n = st["n_lag"]
        n_lag_pairs += n
        if n >= 10:
            markets_lag += 1
            mean_f = st["sum_f"] / n
            mean_rl = st["sum_rl"] / n
            vf = st["sum_f2"] / n - mean_f * mean_f
            vl = st["sum_rl2"] / n - mean_rl * mean_rl
            cov = st["sum_frl"] / n - mean_f * mean_rl
            if vf > 0 and vl > 0:
                corr_lags.append(cov / math.sqrt(vf * vl))
        n = st["n_fwd"]
        n_fwd_pairs += n
        if n >= 10:
            markets_fwd += 1
            mean_f = st["sum_f"] / n
            mean_rf = st["sum_rf"] / n
            vf = st["sum_f2"] / n - mean_f * mean_f
            vr = st["sum_rf2"] / n - mean_rf * mean_rf
            cov = st["sum_frf"] / n - mean_f * mean_rf
            if vf > 0 and vr > 0:
                corr_fwds.append(cov / math.sqrt(vf * vr))
    ml = mean(corr_lags)
    mf = mean(corr_fwds)
    results["domains"]["d3_funding_sign_timing"] = {
        "markets_lag_pairs": markets_lag,
        "markets_fwd_pairs": markets_fwd,
        "n_lag_pairs": n_lag_pairs,
        "n_fwd_pairs": n_fwd_pairs,
        "mean_corr_funding_vs_lag_return": ml,
        "mean_corr_funding_vs_fwd_return": mf,
        "timing_reading": ("settlement-timing (funding_t tracks lagged move)"
                           if ml > mf else
                           ("publication-timing (funding_t leads fwd move)" if mf > ml else "unresolved")),
        "funding_sign_balance": {"n": funding_n, "positive": funding_sign_pos,
                                 "negative": funding_sign_neg, "zero": funding_sign_zero},
        "method": "last-known funding at/before candle ts; lag = return into candle ts, fwd = return out of candle ts",
    }

    # ---- D4 ---------------------------------------------------------------
    top_markets = sorted(d4_market_max.items(), key=lambda kv: kv[1], reverse=True)[:5]
    results["domains"]["d4_mark_index_alignment"] = {
        "aligned_rows": d4_rows,
        "max_mark_oracle_premium": d4_max_premium,
        "fraction_above_1pct_tolerance": (d4_over_tol / d4_rows) if d4_rows else float("nan"),
        "top5_markets_by_max_premium": [(m, round(v, 6)) for m, v in top_markets],
        "tolerance": TOLERANCE,
    }

    # ---- D5 ---------------------------------------------------------------
    results["domains"]["d5_missingness_preservation"] = {
        "per_dataset_per_month": per_month_nulls,
        "rows_per_dataset_per_month": per_month_rows,
        "policy": "no zero-fill / forward-fill anywhere; nulls preserved as-is; caches read-only",
    }

    # ---- D6 ---------------------------------------------------------------
    results["domains"]["d6_delisting_symbol_migration"] = {
        "coins_first_month": len(first_coins),
        "coins_last_month": len(last_coins),
        "distinct_coins_all_months": len(all_coins),
        "coins_absent_from_last_month": len(first_coins - last_coins),
        "coins_new_in_last_month": len(last_coins - first_coins),
        "coins_present_every_month": len(survivors),
        "survivor_share_of_last_month": (len(survivors & last_coins) / len(last_coins)) if last_coins else float("nan"),
        "markets_checked_for_coin_stability": len(market_coin_sets),
        "markets_with_multiple_coins_observed": sum(1 for coins in market_coin_sets.values() if len(coins) > 1),
    }

    # ---- D7 ---------------------------------------------------------------
    results["domains"]["d7_survivorship"] = {
        "survivor_coins": len(survivors),
        "survivor_share_of_universe": len(survivors) / len(all_coins) if all_coins else float("nan"),
        "mean_abs_funding_survivors": mean(fund_surv),
        "mean_abs_funding_non_survivors": mean(fund_non),
        "n_survivor_funding_obs": len(fund_surv),
        "n_non_survivor_funding_obs": len(fund_non),
    }

    # ---- D8 ---------------------------------------------------------------
    rv_sorted = sorted(rv_values.tolist())
    n_rv = len(rv_sorted)
    stress_thr = rv_sorted[max(0, min(n_rv - 1, int(math.floor(STRESS_Q * (n_rv - 1)))))]
    stress_counts: dict[int, int] = {}
    n_stress = 0
    for i in range(n_rv):
        if rv_values[i] >= stress_thr:
            n_stress += 1
            stress_counts[rv_market_idx[i]] = stress_counts.get(rv_market_idx[i], 0) + 1
    counts = sorted(stress_counts.values(), reverse=True)
    total_counts = sum(counts) if counts else 0
    top_share = (counts[0] / total_counts) if total_counts else float("nan")
    top3_share = (sum(counts[:3]) / total_counts) if total_counts else float("nan")
    hh = sum((c / total_counts) ** 2 for c in counts) if total_counts else float("nan")
    results["domains"]["d8_stress_concentration"] = {
        "n_hourly_rv_obs": n_rv,
        "stress_threshold_rv_p99": stress_thr,
        "n_stress_hours": n_stress,
        "markets_with_stress_hours": len(stress_counts),
        "top_market_share_of_stress": top_share,
        "top3_market_share_of_stress": top3_share,
        "herfindahl_over_markets": hh,
        "stress_dominated_by_single_coin_gt_25pct": bool(top_share > 0.25),
    }

    # ---- D9 ---------------------------------------------------------------
    d9_drift: list[float] = []
    for m, series in d9.items():
        series.sort(key=lambda t: t[0])
        prev_p66 = None
        for _, _, p66 in series:
            if p66 != p66:
                continue
            if prev_p66 is not None:
                d9_drift.append(abs(p66 - prev_p66))
            prev_p66 = p66
    results["domains"]["d9_threshold_drift"] = {
        "markets_with_monthly_thresholds": len(d9),
        "market_months": sum(len(s) for s in d9.values()),
        "mean_monthly_p66_drift": mean(d9_drift),
        "max_monthly_p66_drift": max(d9_drift) if d9_drift else float("nan"),
        "note": "funding tercile thresholds computed per market-month from |funding_rate|; "
                "train-only thresholds (pooled design) vs full-sample thresholds differ by construction",
    }

    # ---- D10 --------------------------------------------------------------
    train_notional_vals = sorted(v for (m, h), v in d10_notional.items() if h in train_hours)
    med_idx = max(0, min(len(train_notional_vals) - 1, len(train_notional_vals) // 2))
    train_median = train_notional_vals[med_idx] if train_notional_vals else 0.0

    def forward_notional(market: str, hour: dt.datetime, h: int) -> float:
        total = 0.0
        for k in range(1, h + 1):
            total += d10_notional.get((market, hour + dt.timedelta(hours=k)), 0.0)
        return total

    label_sets: dict[int, set[tuple[str, dt.datetime]]] = {h: set() for h in HORIZONS_H}
    for (market, hour) in d10_notional:
        if hour not in test_hours:
            continue
        for h in HORIZONS_H:
            if forward_notional(market, hour, h) > train_median:
                label_sets[h].add((market, hour))

    def jaccard(a: set, b: set) -> float:
        if not a and not b:
            return float("nan")
        return len(a & b) / len(a | b)

    overlap = {}
    hs = list(HORIZONS_H)
    for i, ha in enumerate(hs):
        for hb in hs[i + 1:]:
            overlap[f"{ha}h_vs_{hb}h"] = jaccard(label_sets[ha], label_sets[hb])
    results["domains"]["d10_overlapping_outcomes"] = {
        "train_median_notional": train_median,
        "liquidation_events": d10_events,
        "distinct_market_hours_with_events": len(d10_notional),
        "label_counts": {f"{h}h": len(label_sets[h]) for h in HORIZONS_H},
        "pairwise_jaccard": overlap,
        "note": "high pairwise Jaccard => forward liquidation-intensity outcomes across horizons are not independent",
    }

    # ---- Track B: modeled boundary-breach labels --------------------------
    tb_thresholds: dict[str, tuple[float, float]] = {}
    for m, vals in trackb_train_funding.items():
        if len(vals) < 10:
            continue
        tb_thresholds[m] = (pctile(vals, 0.33), pctile(vals, 0.66))

    def tercile(m: str, fv: float) -> str:
        th = tb_thresholds.get(m)
        if th is None or fv != fv:
            return "unlabeled"
        if fv <= th[0]:
            return "low"
        if fv <= th[1]:
            return "mid"
        return "high"

    tb_counts: dict[str, dict] = {"low": {"n": 0, "b": 0}, "mid": {"n": 0, "b": 0},
                                  "high": {"n": 0, "b": 0}, "unlabeled": {"n": 0, "b": 0}}
    tb_total_n = 0
    tb_total_b = 0
    last_close2: dict[str, float] = {}
    last_funding2: dict[str, float] = {}
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
        f_n = len(f_ts)
        for i in range(len(c_ts)):
            m = c_market[i]
            ts = c_ts[i]
            c = c_close[i]
            while fi < f_n and f_ts[fi] <= ts:
                r = f_rate[fi]
                if r is not None and r == r:
                    last_funding2[f_market[fi]] = r
                fi += 1
            pc = last_close2.get(m)
            if pc is not None and c and c > 0 and pc > 0 and hour_of(ts) in test_hours:
                ret_abs = abs(math.log(c / pc))
                terc = tercile(m, last_funding2.get(m))
                tb_counts[terc]["n"] += 1
                tb_total_n += 1
                if ret_abs >= BREACH_BAND:
                    tb_counts[terc]["b"] += 1
                    tb_total_b += 1
            if c and c > 0:
                last_close2[m] = c
        del ct
        del ft

    results["domains"]["trackb_modeled_boundary_breach"] = {
        "leverage_assumed": 20,
        "maintenance_fraction_of_initial": 0.5,
        "breach_band_abs_return": BREACH_BAND,
        "label_kind": "modeled boundary-breach proxy (NOT observed liquidation)",
        "test_market_hours_evaluated": tb_total_n,
        "modeled_breach_count": tb_total_b,
        "modeled_breach_rate": (tb_total_b / tb_total_n) if tb_total_n else float("nan"),
        "by_tercile": {k: dict(v) for k, v in tb_counts.items()},
        "markets_with_train_thresholds": len(tb_thresholds),
        "data_limit": "Track B is a hypothetical scenario on public mark history + publicly documented margin params; "
                      "it does not reconstruct account-level liquidation mechanics or actual forced liquidations.",
    }

    out_json = REPO / "research_state" / f"session_{SESSION_UTC}" / f"fclr_pooled_audit001_audit_{SESSION_UTC}.json"
    out_md = REPO / "research_state" / f"session_{SESSION_UTC}" / f"fclr_pooled_audit001_audit_{SESSION_UTC}.md"
    out_json.write_text(json.dumps(results, indent=2, default=str) + "\n", encoding="utf-8")
    md_lines = [
        f"# FCLR-POOLED-AUDIT-001 Adversarial Audit Results",
        f"Session UTC: {SESSION_UTC}",
        f"Campaign: FCLR-POOLED-AUDIT-001-20261122T120000Z",
        f"Software: stdlib + pyarrow only; numpy/pandas/scipy not used",
        f"Data: ironflow bulk, 18 months 2025-05..2026-10, .parquet.sha256 asserted before every read, caches read-only",
        "",
        "## Domains",
    ]
    for name, dom in results["domains"].items():
        md_lines.append(f"### {name}")
        md_lines.append(json.dumps(dom, indent=2, default=str))
        md_lines.append("")
    out_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"[FCLR-POOLED-AUDIT-001] audit complete: {SESSION_UTC}")
    print(f"  json: {out_json}")
    print(f"  md:   {out_md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
