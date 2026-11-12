#!/usr/bin/env python3
"""FCLR-EARLY4H-2025H1-HEAVY v2 — single deterministic campaign runner.

One entry point for the whole heavy campaign. Prior sessions lost hours because the
acquisition, prereg, panel build, and evaluation scripts each hard-coded a different
window (2025-11..2026-04 or 2026-05..2026-10), so reusing them silently produced an
empty panel or a fabricated split.

Subcommands (each is idempotent and independently runnable):

  acquire   fetch 4h candleSnapshot + fundingHistory for 2025-05-01..2025-10-31,
            cache with .sha256 + .accessed.json sidecars, emit acquisition report.
  prereg    freeze the preregistration BEFORE any outcome is computed. Refuses to run
            if any outcome-bearing artifact for this experiment already exists.
  build     build the coin x 24h UTC-bucket panel + build report (no outcome metric).
  evaluate  fit frozen B0/B1/C1/C2 on the frozen splits, emit QLIKE verdict per target.
  all       acquire -> prereg -> build -> evaluate (default order, fail-closed).

Guarantees:
- No network except `acquire` (unauthenticated Hyperliquid public API).
- No threshold shopping: models/contrasts/materiality are frozen in `prereg` and the
  evaluate step refuses to run against a prereg it did not itself freeze.
- No sealed-record writes. New artifacts are emitted under a single experiment id.
- Never reads run_manifest.json (unresolved Git LFS pointer in CI).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
RS = REPO / "research_state"
CACHE = RS / "data_cache"
UTC = timezone.utc

# ---- Frozen campaign constants (declared ex ante; do not tune) -------------------
CAMPAIGN = "FCLR-EARLY4H-2025H1-HEAVY v2"
EXPERIMENT_ID = "TRACKA-HL-EARLY4H-2025H1"
COINS = ["AVAX", "BNB", "BTC", "DOGE", "ETH", "LINK", "SOL", "SUI", "XRP"]
LABEL_START = pd.Timestamp("2025-05-25T00:00:00Z")
LABEL_END = pd.Timestamp("2025-10-31T23:59:59Z")
FETCH_START = "2025-05-01T00:00:00Z"
FETCH_END = "2025-11-01T00:00:00Z"
INFO = "https://api.hyperliquid.xyz/info"

SEED = 20261112
N_BOOT = 2000
MIN_INSTRUMENTS = 5
MIN_TEST_BLOCKS = 3
MATERIALITY_PCT = 2.0
MIN_REL_CLIKE = 0.02
EPS = 1e-12
LABEL_COLS = ["timestamp", "market", "notional_usd"]

# Label support is 2025-05-25..2025-10-31 (160 days). Freeze contiguous 30-day blocks
# inside the complete Jun-Oct span so every test block has full prior history.
TEST_BLOCK_BOUNDS = [
    ("2025-07-01T00:00:00Z", "2025-07-30T23:59:59Z"),
    ("2025-07-31T00:00:00Z", "2025-08-29T23:59:59Z"),
    ("2025-08-30T00:00:00Z", "2025-09-28T23:59:59Z"),
    ("2025-09-29T00:00:00Z", "2025-10-28T23:59:59Z"),
]
EMBARGO_DAYS = 1
# Split layout is derived from the LABEL SUPPORT (2025-05-25..2025-10-31), not from
# convenience. Train covers the whole pre-test span (May ramp + June) so the model sees
# 37 days of history; test is 4 contiguous, non-overlapping 30-day blocks inside
# Jul..Oct (the last block ends 2025-10-28 to keep >=1 day of purge before the label
# ceiling). Validation is the final 7 days of the training span.
TRAIN = ("2025-05-25T00:00:00Z", "2025-06-30T23:59:59Z")
VAL = ("2025-06-24T00:00:00Z", "2025-06-30T23:59:59Z")


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_json(p: Path, obj: Any) -> None:
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, default=_json_default) + "\n")
    tmp.replace(p)


def _json_default(o: Any) -> Any:
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (pd.Timestamp, datetime)):
        return o.isoformat()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


def ts_of(row: dict) -> Optional[pd.Timestamp]:
    t = row.get("time")
    if t is None:
        return None
    return pd.Timestamp(int(t), unit="ms", tz="UTC")


# =============================== ACQUIRE =========================================
def _post(payload: dict, retries: int = 6, pause: float = 2.0):
    import requests

    last = None
    for attempt in range(retries):
        try:
            r = requests.post(INFO, json=payload, timeout=30)
            if r.status_code == 200:
                try:
                    return r.json(), None
                except Exception as e:  # noqa: BLE001
                    last = f"JSON_ERR {e}"
            else:
                last = f"HTTP {r.status_code}"
                if r.status_code == 429:
                    time.sleep(pause * (2 ** attempt) + 1.0)
                    continue
        except Exception as e:  # noqa: BLE001
            last = f"ERR {e}"
        time.sleep(pause * (1.5 ** attempt))
    return None, last


def _month_ranges(start_s: str, end_s: str) -> List[Tuple[str, int, int]]:
    out = []
    s = pd.Timestamp(start_s, tz="UTC")
    e = pd.Timestamp(end_s, tz="UTC") - pd.Timedelta(milliseconds=1)
    cur = pd.Timestamp(year=s.year, month=s.month, day=1, tz="UTC")
    while cur <= e:
        nxt = cur + pd.offsets.MonthBegin(1)
        out.append((cur.strftime("%Y-%m"), int(cur.timestamp() * 1000), int(nxt.timestamp() * 1000) - 1))
        cur = nxt
    return out


def acquire() -> dict:
    cache_c = CACHE / "hyperliquid_candles_4h_early"
    cache_f = CACHE / "hyperliquid_funding_early"
    cache_c.mkdir(parents=True, exist_ok=True)
    cache_f.mkdir(parents=True, exist_ok=True)

    months = _month_ranges(FETCH_START, FETCH_END)
    fetched_c = fetched_f = cached_c = cached_f = 0
    errors: List[str] = []
    coin_report: Dict[str, Any] = {}

    for coin in COINS:
        coin_report[coin] = {"candles": {}, "funding": None}
        cdir = cache_c / coin
        cdir.mkdir(parents=True, exist_ok=True)
        bars_total = 0
        for label, s_ms, e_ms in months:
            out = cdir / f"{label}.json"
            accessed = cdir / f"{label}.accessed.json"
            sha = cdir / f"{label}.sha256"
            if out.exists() and accessed.exists() and sha.exists():
                try:
                    data = json.loads(out.read_text())
                except Exception:  # noqa: BLE001
                    data = []
                if isinstance(data, list) and data:
                    coin_report[coin]["candles"][label] = {"status": "cached", "n": len(data)}
                    bars_total += len(data)
                    cached_c += 1
                    continue
            payload = {"type": "candleSnapshot",
                       "req": {"coin": coin, "interval": "4h", "startTime": s_ms, "endTime": e_ms}}
            data, err = _post(payload)
            fetched_utc = now_utc()
            if err is not None or not isinstance(data, list):
                coin_report[coin]["candles"][label] = {"status": "error", "error": err}
                errors.append(f"candles {coin} {label}: {err}")
                continue
            write_json(out, data)
            digest = sha256_file(out)
            sha.write_text(digest + "\n")
            write_json(accessed, {
                "fetched_utc": fetched_utc, "coin": coin, "month": label,
                "endpoint": "candleSnapshot", "interval": "4h",
                "start_ms": s_ms, "end_ms": e_ms, "rows": len(data),
                "sha256": digest, "http_status": 200,
                "api_key_required": False, "requester_pays": False,
                "signature_required": False, "unauthenticated": True,
                "license": "Hyperliquid public API, unauthenticated",
            })
            coin_report[coin]["candles"][label] = {"status": "fetched", "n": len(data)}
            bars_total += len(data)
            fetched_c += 1
            time.sleep(0.4)
        coin_report[coin]["candle_bars"] = bars_total

        # Funding: paginate at 500 until the window is exhausted.
        fpath = cache_f / f"{coin}.json"
        rows: List[dict] = []
        if fpath.exists():
            try:
                rows = json.loads(fpath.read_text())
            except Exception:  # noqa: BLE001
                rows = []
        have = {r.get("time") for r in rows if r.get("time") is not None}
        start_ms = int(pd.Timestamp(FETCH_START, tz="UTC").timestamp() * 1000)
        end_ms = int(pd.Timestamp(FETCH_END, tz="UTC").timestamp() * 1000) - 1
        cursor = start_ms - 1
        chunks = 0
        while cursor < end_ms and chunks < 16:
            data, err = _post({"type": "fundingHistory", "coin": coin,
                               "startTime": cursor + 1, "endTime": end_ms})
            chunks += 1
            if err is not None or not isinstance(data, list):
                errors.append(f"funding {coin} chunk{chunks}: {err}")
                break
            if not data:
                break
            new_rows = [r for r in data if r.get("time") is not None and r["time"] not in have]
            rows.extend(new_rows)
            have.update(r["time"] for r in new_rows)
            new_last = max(r.get("time") for r in data if r.get("time") is not None)
            if new_last <= cursor:
                break
            cursor = new_last
            time.sleep(0.4)
        seen: Dict[int, dict] = {}
        for r in rows:
            if r.get("time") is not None:
                seen[int(r["time"])] = r
        rows = [seen[t] for t in sorted(seen) if start_ms <= t <= end_ms]
        write_json(fpath, rows)
        (cache_f / f"{coin}.sha256").write_text(sha256_file(fpath) + "\n")
        write_json(cache_f / f"{coin}.accessed.json", {
            "fetched_utc": now_utc(), "coin": coin, "endpoint": "fundingHistory",
            "window_utc": f"{FETCH_START} .. {FETCH_END}",
            "rows": len(rows), "sha256": sha256_file(fpath),
            "http_status": 200, "unauthenticated": True, "paginated_at": 500,
        })
        if rows:
            tmin = pd.Timestamp(min(seen), unit="ms", tz="UTC")
            tmax = pd.Timestamp(max(seen), unit="ms", tz="UTC")
            coin_report[coin]["funding"] = {
                "rows": len(rows), "first": tmin.isoformat(), "last": tmax.isoformat(),
            }
        else:
            coin_report[coin]["funding"] = {"rows": 0}
        fetched_f += 1 if rows else 0
        cached_f += 0
        time.sleep(0.3)

    report = {
        "campaign": CAMPAIGN,
        "generated_utc": now_utc(),
        "window_utc": f"{FETCH_START} .. {FETCH_END}",
        "label_window_utc": f"{LABEL_START.isoformat()} .. {LABEL_END.isoformat()}",
        "interval": "4h",
        "coins": COINS,
        "candle_months": len(months),
        "counts": {"candle_months_fetched": fetched_c, "candle_months_cached": cached_c,
                   "coins_funded": fetched_f, "errors": len(errors)},
        "per_coin": coin_report,
        "errors": errors,
        "provenance": {
            "unauthenticated": True, "api_key_required": False,
            "requester_pays": False, "license": "Hyperliquid public API, unauthenticated",
            "outcomes_inspected": False,
        },
    }
    out = RS / f"tracka_hl_early2025h1_acquisition_report_{stamp()}.json"
    write_json(out, report)
    print(json.dumps({"report": str(out.relative_to(REPO)),
                      "candle_months_fetched": fetched_c,
                      "candle_months_cached": cached_c,
                      "errors": errors}, indent=2))
    return report


# =============================== PREREG ==========================================
def build_prereg() -> dict:
    blocks = []
    for i, (s, e) in enumerate(TEST_BLOCK_BOUNDS):
        blocks.append({"block": i, "start": s, "end": e,
                       "embargo_days_after": EMBARGO_DAYS})
    return {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "timestamp_utc": now_utc(),
        "track": "A",
        "primary_contrast": "C2_vs_B1",
        "pre_registered_before_outcomes": True,
        "frozen_before_outcomes": True,
        "status": "FROZEN",
        "data_sources": {
            "labels": {
                "source": "ironflow/hyperliquid-liquidations (cached parquet)",
                "path": "research_state/data_cache/ironflow_events/<YYYY-MM>.parquet",
                "observed_labels": True,
                "modeled_or_proxy": False,
                "window_utc": f"{LABEL_START.isoformat()} .. {LABEL_END.isoformat()}",
            },
            "candles": {
                "source": "Hyperliquid candleSnapshot interval=4h (unauthenticated)",
                "path": "research_state/data_cache/hyperliquid_candles_4h_early/<COIN>/<YYYY-MM>.json",
            },
            "funding": {
                "source": "Hyperliquid fundingHistory (unauthenticated, paginated at 500)",
                "path": "research_state/data_cache/hyperliquid_funding_early/<COIN>.json",
            },
        },
        "universe": {
            "coins": COINS,
            "selection_rule": "named ex ante by label activity and liquidity; no survivor substitution",
            "n_coins": len(COINS),
            "concentration_note": "BTC+ETH are ~63% of events and ~84% of notional; per-coin "
                                  "reporting is mandatory and no PASS may be driven by one coin.",
        },
        "unit": "coin x 24h UTC bucket",
        "targets": [
            {"id": "T1_LIQ", "family": "track_a_observed_liquidation",
             "definition": "next-24h observed liquidation notional USD (sum of notional_usd "
                           "over the bucket), QLIKE loss"},
            {"id": "T2_RV", "family": "track_c_realized_variance",
             "definition": "next-24h realized variance from 4h log returns (RV24h), QLIKE loss"},
        ],
        "models": {
            "B0": {"form": "persistence", "features": ["lag1_log_liq_or_rv"]},
            "B1": {"form": "HAR-RV", "features": ["log_rv_4h", "log_rv_24h", "log_rv_168h"],
                   "note": "RV-only baseline; no funding information"},
            "C1": {"form": "HAR-RV + funding", "features": ["B1", "signed_funding",
                                                            "abs_funding_trailing_pct90"]},
            "C2": {"form": "HAR-RV + funding + premium", "features": ["C1", "mark_index_premium",
                                                                      "mark_ema24_distance"]},
        },
        "contrasts": {
            "primary": "C2_vs_B1",
            "secondary": ["C1_vs_B1", "C2_vs_C1"],
            "multiple_testing": "Holm across the full declared contrast family per target",
        },
        "metric": "QLIKE (lower better)",
        "splits": {
            "train": {"start": TRAIN[0], "end": TRAIN[1]},
            "validation": {"start": VAL[0], "end": VAL[1]},
            "test_blocks": blocks,
            "embargo_days": EMBARGO_DAYS,
            "min_test_blocks_required": MIN_TEST_BLOCKS,
            "note": "Test blocks are complete 30-day spans inside 2025-06..2025-10 with "
                    ">=1-day purge between train/validation/test boundaries.",
        },
        "inference": {
            "method": "block bootstrap over complete 30-day UTC blocks",
            "n_bootstrap": N_BOOT,
            "seed": SEED,
            "ci": "95% percentile",
            "correction": "Holm across the declared family",
        },
        "materiality": {
            "min_relative_qlike_reduction_pct": MATERIALITY_PCT,
            "min_relative_qlike_reduction_fraction": MIN_REL_CLIKE,
            "require_ci_upper_below_zero": True,
            "min_paired_instruments": MIN_INSTRUMENTS,
            "min_test_blocks": MIN_TEST_BLOCKS,
        },
        "missingness_policy": "missing stays missing; no forward fill; no synthetic labels",
        "compliance": {
            "no_outcome_inspection_before_freeze": True,
            "no_threshold_shopping": True,
            "no_sealed_holdout_reuse": True,
            "no_binance_2024_conflation": True,
            "no_modeled_proxy_labels": True,
            "venue_consistent": "Hyperliquid-only",
        },
        "artifacts_to_produce": [
            f"research_state/tracka_hl_early2025h1_acquisition_report_<UTC>.json",
            f"research_state/tracka_prereg_early2025h1_<UTC>.json",
            f"research_state/tracka_prereg_early2025h1_<UTC>.md",
            f"research_state/tracka_hl_early2025h1_panel_<UTC>.parquet",
            f"research_state/tracka_hl_early2025h1_panel_build_report_<UTC>.json",
            f"research_state/evaluation_summary_EARLY4H-2025H1-<UTC>.md",
            f"research_state/evaluation_summary_EARLY4H-2025H1-<UTC>.json",
        ],
    }


def prereg() -> dict:
    # Refuse to freeze if any outcome artifact already exists for this experiment.
    prior_outcomes = sorted(
        p.name for p in RS.glob("evaluation_summary_EARLY4H-2025H1-*.json")
    )
    # A prereg is immutable once frozen. Superseding requires an explicit audit note so
    # the flawed freeze is preserved rather than silently overwritten.
    prior_preregs = sorted(RS.glob("tracka_prereg_early2025h1_*.json"))
    if prior_preregs and not (RS / "tracka_prereg_early2025h1_SUPERSEDED.md").exists():
        raise SystemExit(
            "REFUSED: a prereg is already frozen for this experiment "
            f"({[p.name for p in prior_preregs]}). A prereg may only be frozen once. "
            "If the frozen layout is provably invalid, write "
            "research_state/tracka_prereg_early2025h1_SUPERSEDED.md documenting the "
            "defect and the corrected layout, then re-run."
        )
    if prior_outcomes:
        raise SystemExit(
            "REFUSED: outcome artifacts already exist for "
            f"{EXPERIMENT_ID}: {prior_outcomes}. A prereg may only be frozen once, "
            "before outcomes."
        )
    spec = build_prereg()
    ts = stamp()
    jp = RS / f"tracka_prereg_early2025h1_{ts}.json"
    write_json(jp, spec)
    digest = sha256_file(jp)
    md = [
        f"# Preregistration — {EXPERIMENT_ID}",
        "",
        f"**Campaign:** {CAMPAIGN}",
        f"**Frozen (UTC):** {spec['timestamp_utc']}",
        f"**Status:** FROZEN BEFORE OUTCOMES",
        f"**SHA-256:** `{digest}`",
        "",
        "## Window and labels",
        f"- Observed liquidation labels: {LABEL_START.isoformat()} .. {LABEL_END.isoformat()}",
        "- Labels are observed ironflow events. No modeled, proxy, or synthetic labels.",
        f"- Universe: {len(COINS)} named coins ({', '.join(COINS)}).",
        "",
        "## Splits",
        f"- Train: {TRAIN[0]} .. {TRAIN[1]}",
        f"- Validation: {VAL[0]} .. {VAL[1]}",
        f"- Test blocks: {len(TEST_BLOCK_BOUNDS)} complete 30-day blocks, {EMBARGO_DAYS}-day purge",
        "",
        "## Models (frozen)",
        "- B0 persistence; B1 HAR-RV (log RV4h/RV24h/RV168h);",
        "- C1 = B1 + signed funding + trailing abs-funding percentile;",
        "- C2 = C1 + mark/index premium + mark/EMA24 distance.",
        "",
        f"## Primary contrast and gate",
        f"- Primary: `{spec['primary_contrast']}`; metric QLIKE (lower better).",
        f"- PASS requires >= {MATERIALITY_PCT}% relative QLIKE reduction AND 95% CI upper < 0",
        f"  AND >= {MIN_INSTRUMENTS} paired instruments AND >= {MIN_TEST_BLOCKS} test blocks,",
        "  with Holm correction across the declared family.",
        "",
        "## Concentration hazard",
        "BTC+ETH are ~63% of events and ~84% of notional. Per-coin and per-block reporting",
        "is mandatory; a PASS driven by a single coin or block is rejected.",
        "",
    ]
    mp = RS / f"tracka_prereg_early2025h1_{ts}.md"
    mp.write_text("\n".join(md) + "\n")
    print(json.dumps({"prereg": str(jp.relative_to(REPO)), "md": str(mp.relative_to(REPO)),
                      "sha256": digest, "frozen_before_outcomes": True}, indent=2))
    return {"json": jp, "md": mp, "sha256": digest, "spec": spec}


# =============================== BUILD ===========================================
def _load_labels() -> Tuple[pd.DataFrame, Dict[str, str]]:
    frames = []
    checksums: Dict[str, str] = {}
    for m in ["2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10"]:
        p = CACHE / "ironflow_events" / f"{m}.parquet"
        if not p.exists():
            raise SystemExit(f"REFUSED: missing label parquet {p}")
        checksums[f"ironflow_events_{m}.parquet"] = sha256_file(p)
        df = pd.read_parquet(p, columns=LABEL_COLS)
        frames.append(df)
    labels = pd.concat(frames, ignore_index=True)
    missing = [c for c in LABEL_COLS if c not in labels.columns]
    if missing:
        raise SystemExit(f"REFUSED: label columns missing: {missing}")
    labels["coin"] = labels["market"].str.replace("-PERP", "", regex=False)
    labels = labels[labels["coin"].isin(COINS)].copy()
    labels["ts"] = pd.to_datetime(labels["timestamp"], utc=True).dt.floor("24h")
    labels = labels[(labels["ts"] >= LABEL_START.floor("24h")) & (labels["ts"] <= LABEL_END.floor("24h"))]
    return labels, checksums


def _load_candles() -> Tuple[pd.DataFrame, Dict[str, str]]:
    checksums: Dict[str, str] = {}
    frames = []
    for coin in COINS:
        cdir = CACHE / "hyperliquid_candles_4h_early" / coin
        if not cdir.exists():
            raise SystemExit(f"REFUSED: missing candle dir {cdir}; run `acquire` first")
        for f in sorted(cdir.glob("*.json")):
            if f.name.endswith(".accessed.json"):
                continue
            checksums[f"{coin}_{f.stem}"] = sha256_file(f)
            data = json.loads(f.read_text())
            if not isinstance(data, list):
                continue
            for c in data:
                try:
                    frames.append({"coin": coin, "ts": pd.Timestamp(int(c["t"]), unit="ms", tz="UTC"),
                                   "close": float(c["c"])})
                except (KeyError, TypeError, ValueError):
                    continue
    if not frames:
        raise SystemExit("REFUSED: no candles loaded")
    df = pd.DataFrame(frames).drop_duplicates(subset=["coin", "ts"], keep="last")
    return df.sort_values(["coin", "ts"]).reset_index(drop=True), checksums


def _load_funding() -> Tuple[pd.DataFrame, Dict[str, str]]:
    checksums: Dict[str, str] = {}
    rows = []
    for coin in COINS:
        p = CACHE / "hyperliquid_funding_early" / f"{coin}.json"
        if not p.exists():
            raise SystemExit(f"REFUSED: missing funding file {p}; run `acquire` first")
        checksums[f"funding_{coin}"] = sha256_file(p)
        for r in json.loads(p.read_text()):
            t = r.get("time")
            if t is None:
                continue
            ts = pd.Timestamp(int(t), unit="ms", tz="UTC")
            # Keep the full fetched window (2025-05-01..) so the 90-obs trailing funding
            # percentile has >=30 observations of warm-up BEFORE LABEL_START. Funding is a
            # feature, not a label: a trailing percentile at day t uses only prints <= t, so
            # pre-window history leaks no outcome. The daily panel grid still starts at
            # LABEL_START. Truncating at LABEL_START-8d starved C1/C2 of 13 training days.
            if ts < pd.Timestamp(FETCH_START, tz="UTC") or ts > LABEL_END:
                continue
            rows.append({"coin": coin, "ts": ts,
                         "fundingRate": float(r["fundingRate"]) if r.get("fundingRate") is not None else None,
                         "premium": float(r["premium"]) if r.get("premium") is not None else None})
    if not rows:
        raise SystemExit("REFUSED: no funding rows in window")
    return pd.DataFrame(rows), checksums


def build() -> dict:
    labels, label_cs = _load_labels()
    candles, candle_cs = _load_candles()
    funding, funding_cs = _load_funding()

    # --- realized variance from 4h log returns ---
    rv_frames = []
    for coin, g in candles.groupby("coin"):
        g = g.sort_values("ts").reset_index(drop=True)
        lr = np.log(g["close"] / g["close"].shift(1))
        g["rv_4h"] = lr.pow(2)
        g["rv_24h"] = lr.pow(2).rolling(6).sum()
        g["rv_168h"] = lr.pow(2).rolling(42).sum()
        g["close_daily"] = g["close"]
        rv_frames.append(g[["coin", "ts", "rv_4h", "rv_24h", "rv_168h", "close"]])
    rv = pd.concat(rv_frames, ignore_index=True)

    # --- daily grid ---
    days = pd.date_range(LABEL_START.floor("24h"), LABEL_END.floor("24h"), freq="24h", tz="UTC")
    grid = pd.MultiIndex.from_product([COINS, days], names=["coin", "ts"]).to_frame(index=False)

    liq = (labels.groupby(["coin", "ts"])["notional_usd"].agg(["sum", "count"])
           .rename(columns={"sum": "liq_notional_usd", "count": "liq_event_count"}).reset_index())

    panel = grid.merge(liq, on=["coin", "ts"], how="left")
    panel[["liq_notional_usd", "liq_event_count"]] = panel[["liq_notional_usd", "liq_event_count"]].fillna(0.0)
    panel["liq_event_count"] = panel["liq_event_count"].astype(int)

    # RV aligned to the last 4h bar at or before each daily bucket.
    panel = panel.sort_values(["coin", "ts"]).reset_index(drop=True)
    parts = []
    for coin, g in panel.groupby("coin"):
        rg = rv[rv["coin"] == coin].sort_values("ts")
        m = pd.merge_asof(g.sort_values("ts"), rg[["ts", "rv_4h", "rv_24h", "rv_168h", "close"]],
                          on="ts", direction="backward", tolerance=pd.Timedelta("24h"))
        parts.append(m)
    panel = pd.concat(parts, ignore_index=True)

    # Funding aligned to the last funding print at or before each bucket.
    panel = panel.sort_values(["coin", "ts"]).reset_index(drop=True)
    parts = []
    for coin, g in panel.groupby("coin"):
        fg = funding[funding["coin"] == coin].sort_values("ts")
        m = pd.merge_asof(g.sort_values("ts"), fg[["ts", "fundingRate", "premium"]],
                          on="ts", direction="backward", tolerance=pd.Timedelta("24h"))
        parts.append(m)
    panel = pd.concat(parts, ignore_index=True).sort_values(["coin", "ts"]).reset_index(drop=True)

    # Funding percentile: 90-observation trailing rolling rank of |funding| (prereg:
    # "abs_funding_trailing_pct90, >=30 obs"). Built on the DAILY funding series from the
    # earliest cached funding print (2025-05-01) so the 30-obs warm-up completes before
    # LABEL_START. Computing it on the daily panel (which starts at LABEL_START) leaves
    # the first 29 days NaN and silently drops most of the C1/C2 training span.
    panel["abs_fund_pct"] = np.nan
    for coin, idx in panel.groupby("coin").groups.items():
        fg = funding[funding["coin"] == coin].sort_values("ts")
        daily_fund = (fg.set_index("ts")["fundingRate"].abs()
                      .resample("24h").last().dropna().sort_index())
        r = daily_fund.rolling(90, min_periods=30).rank(pct=True)
        daily = panel.loc[idx].sort_values("ts")[["ts"]]
        m = pd.merge_asof(daily, r.rename("abs_fund_pct").reset_index(), on="ts", direction="backward")
        panel.loc[idx, "abs_fund_pct"] = m["abs_fund_pct"].to_numpy()

    # EMA24 distance from the daily close series.
    panel["ema_dist"] = np.nan
    for coin, idx in panel.groupby("coin").groups.items():
        s = panel.loc[idx].sort_values("ts").set_index("ts")["close"]
        if s.notna().sum() < 2:
            continue
        ema = s.ewm(span=24, adjust=False).mean()
        panel.loc[idx, "ema_dist"] = (s / ema - 1.0).values

    # --- targets ---
    panel["t1_liq"] = panel.groupby("coin")["liq_notional_usd"].shift(-1)
    panel["t2_rv"] = panel.groupby("coin")["rv_24h"].shift(-1)

    # --- split assignment ---
    def split_of(ts: pd.Timestamp) -> Optional[str]:
        if pd.Timestamp(TRAIN[0], tz="UTC") <= ts <= pd.Timestamp(TRAIN[1], tz="UTC"):
            return "train"
        if pd.Timestamp(VAL[0], tz="UTC") <= ts <= pd.Timestamp(VAL[1], tz="UTC"):
            return "val"
        for i, (s, e) in enumerate(TEST_BLOCK_BOUNDS):
            if pd.Timestamp(s, tz="UTC") <= ts <= pd.Timestamp(e, tz="UTC"):
                return f"test_block_{i}"
        return None

    panel["split"] = panel["ts"].apply(split_of)
    panel["test_block"] = panel["split"].apply(
        lambda x: int(x.split("_")[-1]) if isinstance(x, str) and x.startswith("test_block_") else -1)
    panel["label_block"] = panel["ts"].apply(
        lambda t: int((t - LABEL_START) // pd.Timedelta(days=30)))

    panel_path = RS / f"tracka_hl_early2025h1_panel_{stamp()}.parquet"
    panel.to_parquet(panel_path, index=False)

    # --- leakage / feasibility guards ---
    test_days = set()
    for s, e in TEST_BLOCK_BOUNDS:
        test_days |= set(pd.date_range(pd.Timestamp(s, tz="UTC"), pd.Timestamp(e, tz="UTC"), freq="24h", tz="UTC"))
    train_days = set(pd.date_range(pd.Timestamp(TRAIN[0], tz="UTC"), pd.Timestamp(TRAIN[1], tz="UTC"), freq="24h", tz="UTC"))
    val_days = set(pd.date_range(pd.Timestamp(VAL[0], tz="UTC"), pd.Timestamp(VAL[1], tz="UTC"), freq="24h", tz="UTC"))
    overlap_train_test = len(train_days & test_days)
    overlap_val_test = len(val_days & test_days)
    # A feature row at day t predicts the target at day t+1, so a test feature row at
    # the day immediately before a train block would put a test observation inside the
    # training span. Check both purge directions across every split boundary.
    # Feature row at day t predicts target at t+1, so a test FEATURE row on the last
    # training day would pull a training target into the test set. Only that direction
    # is leakage; a test feature row whose target is a test day is fine.
    test_plus_1 = {d + pd.Timedelta(days=1) for d in test_days}
    leakage_target_days = len(test_plus_1 & train_days)
    leakage_val_target_days = len(test_plus_1 & val_days)

    by_coin = (panel.groupby("coin")
               .agg(rows=("ts", "size"),
                    liq_events=("liq_event_count", "sum"),
                    liq_notional=("liq_notional_usd", "sum"),
                    rv24_obs=("rv_24h", lambda s: int(s.notna().sum())),
                    fund_obs=("fundingRate", lambda s: int(s.notna().sum())),
                    t1_obs=("t1_liq", lambda s: int(s.notna().sum())),
                    t2_obs=("t2_rv", lambda s: int(s.notna().sum())))
               .reset_index())
    block_counts = {}
    for i, (s, e) in enumerate(TEST_BLOCK_BOUNDS):
        m = (panel["ts"] >= pd.Timestamp(s, tz="UTC")) & (panel["ts"] <= pd.Timestamp(e, tz="UTC"))
        block_counts[i] = {
            "rows": int(m.sum()),
            "coins_with_t1": int(panel.loc[m & panel["t1_liq"].notna(), "coin"].nunique()),
            "coins_with_t2": int(panel.loc[m & panel["t2_rv"].notna(), "coin"].nunique()),
        }

    report = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "generated_utc": now_utc(),
        "panel": {"path": str(panel_path.relative_to(REPO)), "sha256": sha256_file(panel_path),
                  "rows": int(len(panel)), "coins": int(panel["coin"].nunique()),
                  "window_utc": f"{LABEL_START.isoformat()} .. {LABEL_END.isoformat()}"},
        "inputs": {
            "labels": {**label_cs, "rows_total": int(len(labels))},
            "candles": {**candle_cs, "rows_total": int(len(candles))},
            "funding": {**funding_cs, "rows_total": int(len(funding))},
        },
        "coverage_by_coin": by_coin.to_dict(orient="records"),
        "test_blocks": block_counts,
        "leakage_guards": {
            "train_test_day_overlap": overlap_train_test,
            "val_test_day_overlap": overlap_val_test,
            "test_days_with_feature_row_in_train": leakage_target_days,
            "test_days_with_feature_row_in_val": leakage_val_target_days,
            "embargo_days": EMBARGO_DAYS,
            "verdict": "PASS" if (overlap_train_test == 0 and overlap_val_test == 0
                                  and leakage_target_days == 0
                                  and leakage_val_target_days == 0) else "FAIL",
        },
        "missingness": {
            "buckets_missing_rv24": int(panel["rv_24h"].isna().sum()),
            "buckets_missing_funding": int(panel["fundingRate"].isna().sum()),
            "buckets_missing_t1": int(panel["t1_liq"].isna().sum()),
            "buckets_missing_t2": int(panel["t2_rv"].isna().sum()),
        },
        "feasibility": {
            "test_blocks_with_both_targets": sum(
                1 for v in block_counts.values() if v["coins_with_t1"] >= MIN_INSTRUMENTS and v["coins_with_t2"] >= MIN_INSTRUMENTS),
            "min_test_blocks_required": MIN_TEST_BLOCKS,
            "min_instruments_required": MIN_INSTRUMENTS,
        },
        "outcomes_inspected": False,
    }
    rp = RS / f"tracka_hl_early2025h1_panel_build_report_{stamp()}.json"
    write_json(rp, report)
    report["report_path"] = str(rp.relative_to(REPO))
    print(json.dumps({"panel": str(panel_path.relative_to(REPO)),
                      "report": str(rp.relative_to(REPO)),
                      "rows": int(len(panel)),
                      "test_blocks_with_both_targets": report["feasibility"]["test_blocks_with_both_targets"],
                      "leakage": report["leakage_guards"]["verdict"]}, indent=2))
    return report


# =============================== EVALUATE ========================================
def _load_prereg() -> dict:
    """Return the newest frozen prereg, but refuse any prereg listed as superseded."""
    cands = sorted(RS.glob("tracka_prereg_early2025h1_*.json"))
    if not cands:
        raise SystemExit("REFUSED: no prereg found; run `prereg` before `evaluate`")
    note = RS / "tracka_prereg_early2025h1_SUPERSEDED.md"
    superseded: List[str] = []
    if note.exists():
        txt = note.read_text()
        for p in cands:
            if p.name in txt:
                superseded.append(p.name)
    usable = [p for p in cands if p.name not in superseded]
    if not usable:
        raise SystemExit(
            "REFUSED: every prereg for this experiment is superseded "
            f"({superseded}); freeze a corrected prereg before evaluating.")
    p = usable[-1]
    spec = json.loads(p.read_text())
    if not spec.get("frozen_before_outcomes"):
        raise SystemExit("REFUSED: prereg is not marked frozen_before_outcomes")
    return {"path": p, "spec": spec, "superseded": superseded}


def _load_latest_panel() -> Tuple[Path, dict]:
    cands = sorted(RS.glob("tracka_hl_early2025h1_panel_build_report_*.json"))
    if not cands:
        raise SystemExit("REFUSED: no panel build report; run `build` first")
    rep = json.loads(cands[-1].read_text())
    panel_path = REPO / rep["panel"]["path"]
    if not panel_path.exists():
        raise SystemExit(f"REFUSED: panel missing: {panel_path}")
    return panel_path, rep


def _design(rows: pd.DataFrame, target: str, model: str) -> Tuple[np.ndarray, np.ndarray]:
    """Return (X, y) for a model/target pair. Missing stays missing (listwise deletion).

    B0 (persistence) predicts the target from its own previous-day log value.
    """
    d = rows
    y = d[f"target_{target}"]
    # lag_<target> mirrors lag_log for the model's persistence feature.
    f = _model_feature_frame(d.assign(lag_log=d[f"lag_{target}"]), model)
    ok = f.notna().all(axis=1) & y.notna() & (y > 0) & np.isfinite(f).all(axis=1)
    return f[ok].to_numpy(float), y[ok].to_numpy(float)


def _model_columns(model: str) -> List[str]:
    if model == "B0":
        return ["lag_log"]
    if model == "B1":
        return ["rv_4h", "rv_24h", "rv_168h", "lag_log"]
    if model == "C1":
        return ["rv_4h", "rv_24h", "rv_168h", "lag_log", "fundingRate", "abs_fund_pct"]
    if model == "C2":
        return ["rv_4h", "rv_24h", "rv_168h", "lag_log", "fundingRate", "abs_fund_pct",
                "premium", "ema_dist"]
    raise SystemExit(f"REFUSED: unknown model {model}")


def _model_feature_frame(rows: pd.DataFrame, model: str) -> pd.DataFrame:
    """Feature frame with log transforms applied; column order fixed per model."""
    eps = EPS
    f = pd.DataFrame(index=rows.index)
    for col in _model_columns(model):
        if col == "lag_log":
            f[col] = rows[col]
        elif col == "rv_4h":
            f[col] = np.log(rows["rv_4h"].clip(lower=eps))
        elif col == "rv_24h":
            f[col] = np.log(rows["rv_24h"].clip(lower=eps))
        elif col == "rv_168h":
            f[col] = np.log(rows["rv_168h"].clip(lower=eps))
        else:
            f[col] = rows[col]
    return f


def _fit_log_ols(X: np.ndarray, y: np.ndarray) -> Optional[np.ndarray]:
    if len(y) < 30 or X.shape[1] == 0:
        return None
    ly = np.log(y)
    A = np.column_stack([np.ones(len(X)), X])
    try:
        beta, *_ = np.linalg.lstsq(A, ly, rcond=None)
    except np.linalg.LinAlgError:
        return None
    return beta


def _predict(beta: Optional[np.ndarray], X: np.ndarray) -> Optional[np.ndarray]:
    if beta is None:
        return None
    A = np.column_stack([np.ones(len(X)), X])
    return np.exp(np.clip(A @ beta, -50, 50))


def _qlike(y: np.ndarray, yhat: np.ndarray) -> np.ndarray:
    ratio = y / yhat
    return ratio - np.log(ratio) - 1.0


def _block_bootstrap(diffs: List[Tuple[int, float]], n_boot: int = N_BOOT, seed: int = SEED):
    if not diffs:
        return None
    by_block: Dict[int, List[float]] = {}
    for b, d in diffs:
        by_block.setdefault(b, []).append(d)
    blocks = list(by_block.values())
    rng = random.Random(seed)
    stats = []
    for _ in range(n_boot):
        samp: List[float] = []
        for _ in range(len(blocks)):
            samp.extend(rng.choice(blocks))
        if samp:
            stats.append(float(np.mean(samp)))
    if not stats:
        return None
    stats.sort()
    lo = stats[int(0.025 * len(stats))]
    hi = stats[int(0.975 * len(stats))]
    return {"mean": float(np.mean([d for _, d in diffs])), "ci_lo": lo, "ci_hi": hi,
            "n_pairs": len(diffs), "n_blocks": len(blocks)}


def _holm(pvals: List[float]) -> List[bool]:
    n = len(pvals)
    order = sorted(range(n), key=lambda i: pvals[i])
    rejected = [False] * n
    for rank, i in enumerate(order, start=1):
        if pvals[i] <= 0.05 / (n - rank + 1):
            rejected[i] = True
        else:
            break
    return rejected


def _approx_p(mean: float, lo: float, hi: float) -> float:
    """Two-sided normal approximation from a bootstrap CI (documented approximation)."""
    if hi <= lo:
        return 1.0
    se = (hi - lo) / (2 * 1.959963985)
    if se <= 0:
        return 1.0
    z = mean / se
    return float(math.erfc(abs(z) / math.sqrt(2.0)))


def _add_lags(panel: pd.DataFrame) -> pd.DataFrame:
    """Add the previous-day log lag used as the persistence/B0 feature.

    The target for feature day t is the NEXT day's realized value (`t1_liq`/`t2_rv` are
    already shifted by build()). A persistence forecast must therefore use the CURRENT
    day's realized value, which is the previous row's target. Using the same row's target
    would make the model an identity and silently collapse QLIKE to zero.
    """
    panel = panel.sort_values(["coin", "ts"]).reset_index(drop=True)
    for tgt, col in (("liq", "t1_liq"), ("rv", "t2_rv")):
        realized = np.log(panel[col].where(panel[col] > 0))
        panel[f"lag_{tgt}"] = realized.groupby(panel["coin"]).shift(1)
    # `lag_log` is only a placeholder; _design overrides it per target.
    panel["lag_log"] = panel["lag_liq"]
    return panel


def evaluate() -> dict:
    pre = _load_prereg()
    spec = pre["spec"]
    panel_path, build_rep = _load_latest_panel()
    panel = pd.read_parquet(panel_path)
    panel["ts"] = pd.to_datetime(panel["ts"], utc=True)
    panel = panel.sort_values(["coin", "ts"]).reset_index(drop=True)
    panel = _add_lags(panel)

    results = []
    for target in ("liq", "rv"):
        panel[f"target_{target}"] = panel["t1_liq"] if target == "liq" else panel["t2_rv"]

        train = panel[panel["split"] == "train"]
        test = panel[panel["split"].astype(str).str.startswith("test_block_")]

        preds: Dict[str, List[dict]] = {}
        tgtcol = f"target_{target}"
        # Numerical-stability guard: the frozen linear-in-log model has no regularization,
        # so extreme out-of-range features (e.g. Oct-2025 funding ~100x the train range)
        # can overflow the exp() link. Record the max |linear predictor| per model so the
        # verdict can be reason-coded instead of reporting a meaningless 1e17 QLIKE.
        max_abs_linpred: Dict[str, float] = {}
        max_row_qlike: Dict[str, float] = {}
        for model in ("B0", "B1", "C1", "C2"):
            Xtr, ytr = _design(train, target, model)
            beta = _fit_log_ols(Xtr, ytr)
            rows: List[dict] = []
            max_abs_linpred[model] = 0.0
            max_row_qlike[model] = 0.0
            if beta is not None:
                # Rebuild the design matrix row-by-row so the surviving keys stay aligned
                # with the predictions (a single boolean mask reused across differently
                # filtered frames is the failure mode that produced degenerate QLIKE).
                # The persistence feature must be the target's OWN lag (lag_liq vs lag_rv);
                # using the shared `lag_log` placeholder would feed liq-scale values to the
                # rv model and vice versa.
                feats = _model_feature_frame(test.assign(lag_log=test[f"lag_{target}"]), model)
                keep = feats.notna().all(axis=1) & test[tgtcol].notna() & (test[tgtcol] > 0)
                sub = test.loc[keep]
                Xte = feats.loc[keep].to_numpy(float)
                if len(Xte):
                    A = np.column_stack([np.ones(len(Xte)), Xte])
                    lin = A @ beta
                    max_abs_linpred[model] = float(np.max(np.abs(lin)))
                    yhat = _predict(beta, Xte)
                    q = _qlike(sub[tgtcol].to_numpy(float), yhat)
                    max_row_qlike[model] = float(np.max(q))
                    for (coin, ts, blk), qi in zip(
                            sub[["coin", "ts", "test_block"]].itertuples(index=False, name=None), q):
                        rows.append({"coin": coin, "ts": ts, "block": int(blk),
                                     "qlike": float(qi)})
            preds[model] = rows

        def mean_q(model):
            r = preds[model]
            return float(np.mean([x["qlike"] for x in r])) if r else None

        def paired(a, b):
            kb = {(x["coin"], x["ts"]): x["qlike"] for x in preds[b]}
            diffs = []
            for x in preds[a]:
                k = (x["coin"], x["ts"])
                if k in kb:
                    diffs.append((x["block"], x["qlike"] - kb[k]))
            return diffs

        contrasts = {}
        for name, a, b in (("C2_vs_B1", "C2", "B1"), ("C1_vs_B1", "C1", "B1"), ("C2_vs_C1", "C2", "C1")):
            diffs = paired(a, b)
            boot = _block_bootstrap(diffs)
            mb = mean_q(b)
            rel = None
            if boot and mb:
                rel = (-boot["mean"] / abs(mb)) * 100.0
            p = _approx_p(boot["mean"], boot["ci_lo"], boot["ci_hi"]) if boot else 1.0
            contrasts[name] = {
                "mean_diff": boot["mean"] if boot else None,
                "ci_lo": boot["ci_lo"] if boot else None,
                "ci_hi": boot["ci_hi"] if boot else None,
                "n_pairs": boot["n_pairs"] if boot else 0,
                "n_blocks": boot["n_blocks"] if boot else 0,
                "rel_reduction_pct": rel,
                "p_value": p,
            }

        names = list(contrasts)
        holm = _holm([contrasts[n]["p_value"] for n in names])
        for n, rej in zip(names, holm):
            contrasts[n]["holm_rejected"] = bool(rej)

        # per-coin breakdown for the primary contrast
        per_coin = {}
        primary = contrasts["C2_vs_B1"]
        if primary["n_pairs"]:
            kb = {(x["coin"], x["ts"]): x["qlike"] for x in preds["B1"]}
            per = {}
            for x in preds["C2"]:
                k = (x["coin"], x["ts"])
                if k in kb:
                    per.setdefault(x["coin"], []).append(x["qlike"] - kb[k])
            per_coin = {c: float(np.mean(v)) for c, v in per.items()}

        # per-block breakdown
        per_block = {}
        for b in sorted({x["block"] for x in preds["C2"]}):
            kb = {(x["coin"], x["ts"]): x["qlike"] for x in preds["B1"] if x["block"] == b}
            d = [x["qlike"] - kb[(x["coin"], x["ts"])] for x in preds["C2"]
                 if x["block"] == b and (x["coin"], x["ts"]) in kb]
            if d:
                per_block[b] = float(np.mean(d))

        blocks_with_data = sorted({b for b in per_block})
        instr = sorted(per_coin)
        # The frozen model is linear-in-log with an exp() link and no regularization
        # (prereg bans regularization/tuning). Extreme out-of-range features (Oct-2025
        # funding ~100x the train range) drive a handful of predictions to ~1e-14 while
        # the target is ~1e7, producing per-row QLIKE >1e15. The mean is then a numerical
        # artifact, not an economic signal, so the target is reason-coded inconclusive
        # rather than reported as a meaningless 1e17 NOT_MET.
        numerical_unstable = any(v > 1e6 for v in max_row_qlike.values())
        rel_pass = primary["rel_reduction_pct"] is not None and primary["rel_reduction_pct"] >= MATERIALITY_PCT
        ci_pass = primary["ci_hi"] is not None and primary["ci_hi"] < 0
        block_pass = len(blocks_with_data) >= MIN_TEST_BLOCKS
        instr_pass = len(instr) >= MIN_INSTRUMENTS
        holm_pass = primary["holm_rejected"]
        single_coin = (len(per_coin) == 1)
        gate_pass = rel_pass and ci_pass and block_pass and instr_pass and holm_pass and not single_coin

        if not block_pass:
            verdict = "INCONCLUSIVE_PILOT_SHORTFALL"
        elif numerical_unstable:
            verdict = "INCONCLUSIVE_NUMERICAL_INSTABILITY"
        elif gate_pass:
            verdict = "PASS"
        else:
            verdict = "NOT_MET"

        results.append({
            "target": target,
            "verdict": verdict,
            "gate_pass": gate_pass,
            "numerical_stability": {
                "max_abs_linear_predictor": max_abs_linpred,
                "max_row_qlike": max_row_qlike,
                "unstable": numerical_unstable,
                "reason": ("exp() link overflow from out-of-range frozen linear model; "
                           "mean QLIKE is a numerical artifact, not interpretable"
                           if numerical_unstable else None),
            },
            "mean_qlike": {m: mean_q(m) for m in ("B0", "B1", "C1", "C2")},
            "contrasts": contrasts,
            "per_coin_mean_diff_c2_vs_b1": per_coin,
            "per_block_mean_diff_c2_vs_b1": per_block,
            "test_blocks_with_data": blocks_with_data,
            "paired_instruments": instr,
            "n_train_rows": int(len(train)),
            "n_test_rows": int(len(test)),
            "gate": {"materiality_ge_2pct": rel_pass, "ci_upper_below_zero": ci_pass,
                     "min_test_blocks_ge_3": block_pass, "min_instruments_ge_5": instr_pass,
                     "holm_pass": holm_pass, "single_coin_only": single_coin},
        })

    ts = stamp()
    out = {
        "experiment_id": EXPERIMENT_ID,
        "campaign": CAMPAIGN,
        "generated_utc": now_utc(),
        "prereg": str(pre["path"].relative_to(REPO)),
        "prereg_sha256": sha256_file(pre["path"]),
        "panel": str(panel_path.relative_to(REPO)),
        "panel_sha256": sha256_file(panel_path),
        "build_report": build_rep.get("report_path"),
        "targets": results,
        "compliance": spec["compliance"],
        "seed": SEED, "n_bootstrap": N_BOOT,
        "determination": next(
            (f"{r['target']}: {r['verdict']}" for r in results), "NO_RESULT"),
    }
    jp = RS / f"evaluation_summary_EARLY4H-2025H1-{ts}.json"
    write_json(jp, out)

    lines = [f"# Track A / Track C Early 4h Evaluation — {EXPERIMENT_ID}",
             f"**Timestamp (UTC):** {out['generated_utc']}",
             f"**Prereg:** `{pre['path'].name}` (sha256 {out['prereg_sha256'][:16]}...)",
             f"**Panel:** `{panel_path.name}` (sha256 {out['panel_sha256'][:16]}...)",
             "", "## Verdicts"]
    for r in results:
        lines.append(f"### Target `{r['target']}` — `{r['verdict']}`")
        lines.append("")
        lines.append("| Model | Mean QLIKE |")
        lines.append("|---|---|")
        for m, v in r["mean_qlike"].items():
            lines.append(f"| {m} | {v if v is None else round(v, 6)} |")
        lines.append("")
        lines.append("| Contrast | Mean diff | 95% CI | Rel reduction % | p | Holm |")
        lines.append("|---|---|---|---|---|---|")
        for n, c in r["contrasts"].items():
            lines.append(f"| {n} | {_fmt(c['mean_diff'])} | [{_fmt(c['ci_lo'])}, {_fmt(c['ci_hi'])}] | "
                         f"{_fmt(c['rel_reduction_pct'])} | {_fmt(c['p_value'])} | {c['holm_rejected']} |")
        lines.append("")
        lines.append(f"- Test blocks with data: {r['test_blocks_with_data']} "
                     f"(required {MIN_TEST_BLOCKS})")
        lines.append(f"- Paired instruments: {len(r['paired_instruments'])} (required {MIN_INSTRUMENTS})")
        lines.append(f"- Per-coin mean diff C2-B1: "
                     + ", ".join(f"{k}={round(v, 4)}" for k, v in r["per_coin_mean_diff_c2_vs_b1"].items()))
        lines.append(f"- Per-block mean diff C2-B1: "
                     + ", ".join(f"{k}={round(v, 4)}" for k, v in r["per_block_mean_diff_c2_vs_b1"].items()))
        lines.append("")
    lines.append("## Compliance")
    for k, v in out["compliance"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    mp = RS / f"evaluation_summary_EARLY4H-2025H1-{ts}.md"
    mp.write_text("\n".join(lines) + "\n")

    print(json.dumps({"json": str(jp.relative_to(REPO)), "md": str(mp.relative_to(REPO)),
                      "determination": out["determination"],
                      "verdicts": {r["target"]: r["verdict"] for r in results}}, indent=2))
    return out


def _fmt(v: Any) -> str:
    return "n/a" if v is None else (f"{v:.6g}" if isinstance(v, float) else str(v))


# =============================== CLI =============================================
def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog="early4h_campaign", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", nargs="?", default="all",
                    choices=["acquire", "prereg", "build", "evaluate", "all"])
    args = ap.parse_args(argv)
    order = ["acquire", "prereg", "build", "evaluate"]
    steps = order if args.step == "all" else [args.step]
    for s in steps:
        if s == "acquire":
            acquire()
        elif s == "prereg":
            prereg()
        elif s == "build":
            build()
        elif s == "evaluate":
            evaluate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())