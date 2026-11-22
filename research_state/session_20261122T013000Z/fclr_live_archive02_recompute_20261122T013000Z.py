#!/usr/bin/env python3
"""FCLR-LIVE-ARCHIVE-02 INDEPENDENT stdlib recompute (cross-check of eval).

This is NOT a copy of fclr_live_archive02_eval_*.py. It re-derives the
next-24h realized-variance target, the HAR + funding/OI/taker features, and the
paired out-of-sample QLIKE for B0/B1/C2 from the RAW archive zips on disk using
an independent code path, then cross-checks the resulting decision against the
frozen eval JSON. stdlib only (numpy/pandas/scipy are NOT installed).

Independence notes:
- Re-parses every raw CSV from the zip members directly (no shared module).
- Rebuilds the hourly mark-price close series and 1h log returns independently.
- Recomputes RV1h/RV24h/RV168h and the next-24h target with a separate loop.
- Uses a different linear-solver entry point (normal equations assembled in a
  dict-of-dicts and solved by Gauss-Jordan) than the eval script's
  augmented-matrix back-substitution.
- Recomputes funding sign, |funding| 90d percentile (min 30 obs), latest
  sum_open_interest and sum_taker_long_short_vol_ratio as-of t.

Writes: fclr_live_archive02_recompute_<UTC>.json + .py (this file).
Reads: raw/ zips, and the frozen eval JSON only to CROSS-CHECK (not to source
any number it reports). Reports agreement/disagreement per block.
"""
import csv
import io
import json
import math
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path

SESSION = Path(__file__).resolve().parent
# Raw archive zips live under the upstream session dir (post-campaign-start).
RAW = SESSION.parent / "session_20261122T003000Z" / "raw"
UTC = "20261122T013000Z"
OUT_JSON = SESSION / f"fclr_live_archive02_recompute_{UTC}.json"
EVAL_JSON = SESSION.parent / "session_20261122T003000Z" / "fclr_live_archive02_eval_20261122T003000Z.json"
EPS = 1e-12


def parse_utc(s):
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1]
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    raise ValueError(f"unparseable timestamp: {s!r}")


def _dictrows(zp):
    """Yield dict rows from the first CSV member of a zip (header-aware)."""
    with zipfile.ZipFile(zp) as z:
        csvnames = [n for n in z.namelist() if n.endswith(".csv")]
        for name in csvnames:
            text = z.read(name).decode("utf-8", "ignore")
            rdr = csv.DictReader(io.StringIO(text))
            for rec in rdr:
                yield rec


def load_mark_closes():
    """Independent parse of markPriceKlines 1h zips -> {hour_dt: close}.

    Uses close_time (ms) as the hour key, matching the archive schema.
    """
    closes = {}
    for zp in sorted(RAW.glob("BTCUSDT-markPriceKlines-1h-*.zip")):
        for rec in _dictrows(zp):
            try:
                ct = int(rec["close_time"])
                close = float(rec["close"])
            except (ValueError, KeyError, TypeError):
                continue
            hr = datetime.fromtimestamp(ct / 1000.0, tz=timezone.utc).replace(
                minute=0, second=0, microsecond=0
            )
            closes[hr] = close
    return closes


def load_funding():
    """Independent parse of monthly fundingRate zips -> {dt: funding}."""
    out = {}
    for zp in sorted(RAW.glob("BTCUSDT-fundingRate-*.zip")):
        for rec in _dictrows(zp):
            try:
                ct = int(rec["calc_time"])
                fr = float(rec["last_funding_rate"])
            except (ValueError, KeyError, TypeError):
                continue
            dt = datetime.fromtimestamp(ct / 1000.0, tz=timezone.utc)
            out[dt] = fr
    return out


def load_metrics():
    """Independent parse of daily metrics zips -> sorted list of (dt, oi, taker)."""
    rows = []
    for zp in sorted(RAW.glob("BTCUSDT-metrics-*.zip")):
        for rec in _dictrows(zp):
            try:
                ct = parse_utc(rec["create_time"])
                oi = float(rec["sum_open_interest"])
                taker = float(rec["sum_taker_long_short_vol_ratio"])
            except (ValueError, KeyError, TypeError):
                continue
            rows.append((ct, oi, taker))
    rows.sort(key=lambda r: r[0])
    return rows


def build_hourly(closes):
    """1h log returns keyed by the hour of the close."""
    hrs = sorted(closes)
    rets = {}
    for i in range(1, len(hrs)):
        if (hrs[i] - hrs[i - 1]) == timedelta(hours=1):
            c0, c1 = closes[hrs[i - 1]], closes[hrs[i]]
            if c0 > 0 and c1 > 0:
                rets[hrs[i]] = math.log(c1 / c0)
    return rets


def trailing_rv(rets, hour, window):
    """Sum of squared 1h log returns over the `window` hours ending at `hour`."""
    s = 0.0
    n = 0
    cur = hour
    for _ in range(window):
        if cur in rets:
            s += rets[cur] * rets[cur]
            n += 1
        cur -= timedelta(hours=1)
    return s if n == window else None


def next_rv(rets, hour, horizon=24):
    """Sum of squared 1h log returns over t+1..t+horizon."""
    s = 0.0
    n = 0
    for k in range(1, horizon + 1):
        h = hour + timedelta(hours=k)
        if h in rets:
            s += rets[h] * rets[h]
            n += 1
    return s if n == horizon else None


def asof(rows, t, idx):
    """Latest value at or before t from sorted rows; None if none."""
    best = None
    for r in rows:
        if r[0] <= t:
            best = r[idx]
        else:
            break
    return best


def funding_pctile_percent(funding_series, t, lookback_days=90, min_obs=30):
    """Percentile rank of |funding(t)| vs preceding `lookback_days` only.

    Uses funding observations in [t-lookback, t] inclusive. Requires >= min_obs
    observations; else returns None (missing, never zero-filled).
    """
    lo = t - timedelta(days=lookback_days)
    hist = [abs(v) for (dt, v) in funding_series if lo <= dt <= t]
    if len(hist) < min_obs:
        return None
    cur = None
    for (dt, v) in funding_series:
        if dt <= t:
            cur = abs(v)
        else:
            break
    if cur is None:
        return None
    below = sum(1 for h in hist if h <= cur)
    return below / len(hist)


def gj_solve(X, y):
    """Gauss-Jordan solver (independent of eval's augmented back-substitution)."""
    p = len(X[0]) + 1
    # build normal equations
    A = [[0.0] * (p + 1) for _ in range(p)]
    for xi, yi in zip(X, y):
        row = [1.0] + list(xi)
        for a in range(p):
            for b in range(p):
                A[a][b] += row[a] * row[b]
            A[a][p] += row[a] * yi
    # Gauss-Jordan with partial pivot
    for col in range(p):
        piv = max(range(col, p), key=lambda r: abs(A[r][col]))
        if abs(A[piv][col]) < 1e-14:
            A[col][col] = 1e-9
        else:
            A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        A[col] = [v / pv for v in A[col]]
        for r in range(p):
            if r == col:
                continue
            f = A[r][col]
            if f != 0.0:
                A[r] = [A[r][c] - f * A[col][c] for c in range(p + 1)]
    return [A[r][p] for r in range(p)]


def predict(X, b):
    return [b[0] + sum(b[i + 1] * x[i] for i in range(len(x))) for x in X]


def qlike(y, pred):
    pairs = [(yy, pp) for yy, pp in zip(y, pred) if yy > 0 and pp > 0]
    if not pairs:
        return float("nan")
    return sum(yy / pp - 1.0 - math.log(yy / pp) for yy, pp in pairs) / len(pairs)


def mae(y, pred):
    return sum(abs(a - b) for a, b in zip(y, pred)) / len(y)


def rmse(y, pred):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(y, pred)) / len(y))


BLOCKS = {
    "train": ("2025-06-01T00:00:00Z", "2025-06-30T23:00:00Z"),
    "test_block_1": ("2025-07-08T00:00:00Z", "2025-07-21T23:00:00Z"),
    "test_block_2": ("2025-07-22T00:00:00Z", "2025-08-04T23:00:00Z"),
    "test_block_3": ("2025-08-05T00:00:00Z", "2025-08-18T23:00:00Z"),
}


def in_block(dt, span):
    a = parse_utc(span[0])
    b = parse_utc(span[1]) + timedelta(hours=1)
    return a <= dt < b


def main():
    closes = load_mark_closes()
    rets = build_hourly(closes)
    funding = load_funding()
    funding_series = sorted(funding.items(), key=lambda kv: kv[0])
    metrics = load_metrics()

    # Build the eligible forecast-hour table (features as-of t, target t+1..t+24).
    rows = []
    for t in sorted(rets):
        rv1 = trailing_rv(rets, t, 1)
        rv24 = trailing_rv(rets, t, 24)
        rv168 = trailing_rv(rets, t, 168)
        y = next_rv(rets, t, 24)
        if None in (rv1, rv24, rv168, y):
            continue
        # causal funding as-of t
        fr = None
        for (dt, v) in funding_series:
            if dt <= t:
                fr = v
            else:
                break
        pct = funding_pctile_percent(funding_series, t)
        oi = asof(metrics, t, 1)
        taker = asof(metrics, t, 2)
        rows.append((t, rv1, rv24, rv168, y, fr, pct, oi, taker))

    def feats_B1(r):
        # log(RV+eps) for the three trailing realized variances
        return [math.log(r[1] + EPS), math.log(r[2] + EPS), math.log(r[3] + EPS)]

    def feats_C2(r):
        # B1 + raw signed funding + abs-funding pct + raw OI + raw taker ratio
        # (standardized later on train only; matches the frozen prereg feature set)
        fr = r[5] if r[5] is not None else 0.0
        pct = r[6] if r[6] is not None else 0.0
        oi = r[7] if r[7] is not None else 0.0
        taker = r[8] if r[8] is not None else 0.0
        return feats_B1(r) + [fr, pct, oi, taker]

    def train_stats(X):
        stats = []
        for j in range(len(X[0])):
            col = [row[j] for row in X]
            mean = sum(col) / len(col)
            var = sum((v - mean) ** 2 for v in col) / len(col)
            std = math.sqrt(var) or 1.0
            stats.append((mean, std))
        return stats

    def apply_std(X, stats):
        return [[(row[j] - stats[j][0]) / stats[j][1] for j in range(len(row))]
                for row in X]

    def fit_smear(X, y):
        """Fit OLS on standardized X; return (beta, constant smear)."""
        stats = train_stats(X)
        Xs = apply_std(X, stats)
        beta = gj_solve(Xs, y)
        pred = predict(Xs, beta)
        resid = [yy - pp for yy, pp in zip(y, pred)]
        smear = math.exp(sum(resid) / len(resid))
        return beta, smear, stats

    # Fit on train only (outcome-blind to test blocks). C2 uses common rows
    # (all C2 features present) for a fair paired contrast.
    train_all = [r for r in rows if in_block(r[0], BLOCKS["train"])]
    train_b1 = [r for r in train_all]
    train_c2 = [r for r in train_all
                if r[5] is not None and r[6] is not None
                and r[7] is not None and r[8] is not None]
    logy_b1 = [math.log(r[4] + EPS) for r in train_b1]
    logy_c2 = [math.log(r[4] + EPS) for r in train_c2]
    b1, smear_b1, stats_b1 = fit_smear([feats_B1(r) for r in train_b1], logy_b1)
    c2, smear_c2, stats_c2 = fit_smear([feats_C2(r) for r in train_c2], logy_c2)

    def eval_block(span_name):
        # Common rows across B1/C2 within the block (C2 feature superset).
        test = [r for r in rows if in_block(r[0], BLOCKS[span_name])
                and r[5] is not None and r[6] is not None
                and r[7] is not None and r[8] is not None]
        y = [r[4] for r in test]
        pred_B0 = [r[2] for r in test]  # persistence = preceding RV24h
        lp_b1 = predict(apply_std([feats_B1(r) for r in test], stats_b1), b1)
        lp_c2 = predict(apply_std([feats_C2(r) for r in test], stats_c2), c2)
        pred_B1 = [math.exp(pl) * smear_b1 for pl in lp_b1]
        pred_C2 = [math.exp(pl) * smear_c2 for pl in lp_c2]
        qB0, qB1, qC2 = qlike(y, pred_B0), qlike(y, pred_B1), qlike(y, pred_C2)
        diff = qC2 - qB1
        rel = (diff / qB1 * 100.0) if qB1 else float("nan")
        return {
            "n": len(y),
            "qlike_B0": qB0, "qlike_B1": qB1, "qlike_C2": qC2,
            "diff_C2_B1": diff, "rel_C2_B1_pct": rel,
            "mae_B0": mae(y, pred_B0), "mae_B1": mae(y, pred_B1), "mae_C2": mae(y, pred_C2),
            "rmse_B0": rmse(y, pred_B0), "rmse_B1": rmse(y, pred_B1), "rmse_C2": rmse(y, pred_C2),
        }

    blocks = {b: eval_block(b) for b in ("test_block_1", "test_block_2", "test_block_3")}
    rels = [blocks[b]["rel_C2_B1_pct"] for b in blocks]
    n_improved = sum(1 for r in rels if r < 0)
    mean_rel = sum(rels) / len(rels)
    materiality = mean_rel <= -2.0
    gate = "CONFIRMED" if (materiality and n_improved == 3) else "NOT_SUPPORTED"

    # Cross-check against frozen eval JSON (report agreement, do not source from it).
    cross = {"eval_present": EVAL_JSON.exists(), "blocks": {}}
    if EVAL_JSON.exists():
        ev = json.loads(EVAL_JSON.read_text())
        for b in blocks:
            eb = ev.get("block_results", {}).get(b, {})
            cross["blocks"][b] = {
                "recompute_rel_pct": blocks[b]["rel_C2_B1_pct"],
                "eval_rel_pct": eb.get("rel_C2_B1_pct"),
                "abs_delta_rel_pct": abs(blocks[b]["rel_C2_B1_pct"] - eb.get("rel_C2_B1_pct", float("nan")))
                if eb.get("rel_C2_B1_pct") is not None else None,
                "recompute_qlike_C2": blocks[b]["qlike_C2"],
                "eval_qlike_C2": eb.get("qlike_C2"),
            }
        cross["eval_decision"] = ev.get("decision")
        cross["recompute_decision"] = gate
        cross["decisions_agree"] = (ev.get("decision") == gate)

    out = {
        "campaign": "FCLR-LIVE-ARCHIVE-02",
        "artifact_id": f"fclr_live_archive02_recompute_{UTC}",
        "session_utc": UTC,
        "role": "INDEPENDENT stdlib recompute / cross-check of eval",
        "data_source": "raw archive zips under session_20261122T003000Z/raw (re-parsed directly)",
        "method": "independent hourly-close/log-return rebuild; trailing RV; next-24h RV target; Gauss-Jordan OLS with train-only standardization + constant exp(mean-resid) smear",
        "n_forecast_hours_total": len(rows),
        "n_train_rows_B1": len(train_b1),
        "n_train_rows_C2": len(train_c2),
        "blocks": blocks,
        "aggregate": {
            "mean_rel_C2_B1_pct": mean_rel,
            "n_blocks": len(blocks),
            "n_improved": n_improved,
            "materiality_pass": materiality,
            "gate": gate,
        },
        "cross_check_vs_eval": cross,
        "outcome_data_inspected_before_freeze": False,
        "liquidation_label_rule": "LIQUIDATION_RISK_PROXY; no observed liquidations on this source",
        "stdlib_only": True,
    }
    OUT_JSON.write_text(json.dumps(out, indent=2, sort_keys=True))
    print(json.dumps({
        "wrote": str(OUT_JSON.relative_to(SESSION.parent.parent)),
        "n_hours": len(rows),
        "mean_rel_C2_B1_pct": mean_rel,
        "n_improved": n_improved,
        "gate": gate,
        "decisions_agree": cross.get("decisions_agree"),
    }, indent=2))


if __name__ == "__main__":
    main()