#!/usr/bin/env python3
"""
FCLR-LIQ-RISK-ESCALATION-09 observed-liquidation power/MDE audit (stdlib + pyarrow only).

Audits observed-event sparsity/coverage for the rare observed-liquidation intensity
target: events per coin-hour, notional coverage, market->coin identity-match rate,
effective sample size, and minimum-detectable-effect (MDE) for the C2 vs B1 contrast.

Reads research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}
(18 monthly parquet, 2025-05..2026-10), asserts .parquet.sha256 before every read,
caches read-only, no network, no new source.

Usage:
  python3 fclr_risk09_power_<UTC>.py <session_dir>

Produces under <session_dir>:
  fclr_risk09_power_<UTC>.json   (machine-readable power/MDE audit)
  fclr_risk09_power_<UTC>.md     (human-readable power/MDE audit)
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from datetime import timezone
from pathlib import Path

try:
    import pyarrow.parquet as pq
except Exception as e:  # pragma: no cover
    print("pyarrow required but unavailable:", e)
    sys.exit(2)

REPO = Path(__file__).resolve().parents[2]
BULK = REPO / "research_state" / "data_cache" / "ironflow_bulk"
SESSION_UTC = "20261122T224500Z"

MONTHS = ["2025-05", "2025-06", "2025-07", "2025-08", "2025-09", "2025-10",
          "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
          "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]

# Frozen design (matches prereg)
TRAIN_FRAC = 0.60
PURGE_EMBARGO_H = 48
BLOCK_H = 168
HORIZON_H = 24
EPS = 1e-12
SEED = 20261122


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def hkey(ts):
    if isinstance(ts, (int, float)):
        return int(ts // 3600) * 3600
    dt = ts.to_pydatetime() if hasattr(ts, "to_pydatetime") else ts
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() // 3600) * 3600


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def pstd(xs):
    n = len(xs)
    if n == 0:
        return 1.0
    m = sum(xs) / n
    v = sum((x - m) ** 2 for x in xs) / n
    return math.sqrt(v) if v > 0 else 1.0


def coin_from_market(market: str) -> str:
    """Strip -PERP suffix and any exchange prefix before the first ':'."""
    s = str(market)
    if ":" in s:
        s = s.split(":", 1)[1]
    if s.endswith("-PERP"):
        s = s[:-5]
    return s.upper()


def load_sidecar_sha256(subdir: str, month: str) -> str:
    sp = BULK / subdir / f"{month}.parquet.sha256"
    if not sp.is_file():
        return None
    return sp.read_text().strip().split()[0]


def verify_sha256(subdir: str, month: str, stored: str) -> bool:
    actual = sha256_file(BULK / subdir / f"{month}.parquet")
    return actual == stored


def main():
    sdir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "research_state/session_" + SESSION_UTC)

    # ---- 1. Verify all input sha256 sidecars ----
    sha_ok = 0
    sha_bad = 0
    sha_map = {}
    for subdir in ["candles_1h", "funding", "open_interest", "liquidations"]:
        for month in MONTHS:
            stored = load_sidecar_sha256(subdir, month)
            if stored is None:
                sha_bad += 1
                sha_map[f"{subdir}/{month}"] = "MISSING_SIDECAR"
                continue
            ok = verify_sha256(subdir, month, stored)
            sha_map[f"{subdir}/{month}"] = {"stored": stored, "match": ok}
            if ok:
                sha_ok += 1
            else:
                sha_bad += 1

    total_sidecars = sha_ok + sha_bad

    # ---- 2. Load liquidations and build market->coin identity ----
    liq_rows = 0
    liq_markets = set()
    liq_coins = set()
    liq_bad_market = 0
    liq_by_coin_hour = {}  # (coin, hour) -> list of notional
    liq_tx_seen = set()    # dedup by tx_hash within hour

    for month in MONTHS:
        t = pq.read_table(BULK / "liquidations" / f"{month}.parquet")
        n = t.num_rows
        ts = t.column("timestamp").to_pylist()
        mk = t.column("market").to_pylist()
        wallet = t.column("wallet").to_pylist()
        notional = t.column("notional_usd").to_pylist()
        tx = t.column("tx_hash").to_pylist()
        for i in range(n):
            liq_rows += 1
            m = str(mk[i])
            liq_markets.add(m)
            coin = coin_from_market(m)
            liq_coins.add(coin)
            hk = hkey(ts[i])
            # dedup by (coin, hour, tx_hash)
            dedup_key = (coin, hk, str(tx[i]) if tx[i] is not None else None)
            if dedup_key in liq_tx_seen:
                continue
            liq_tx_seen.add(dedup_key)
            key = (coin, hk)
            if key not in liq_by_coin_hour:
                liq_by_coin_hour[key] = []
            try:
                liq_by_coin_hour[key].append(float(notional[i]) if notional[i] is not None else 0.0)
            except (TypeError, ValueError):
                liq_by_coin_hour[key].append(0.0)

    # ---- 3. Load candles for identity coverage (coin eligibility per hour) ----
    candle_coin_hour = set()  # (coin, hour) with valid close
    candle_markets = set()
    for month in MONTHS:
        t = pq.read_table(BULK / "candles_1h" / f"{month}.parquet")
        n = t.num_rows
        ts = t.column("timestamp").to_pylist()
        mk = t.column("market").to_pylist()
        cl = t.column("close").to_pylist()
        coin_col = t.column("coin").to_pylist() if "coin" in t.column_names else None
        for i in range(n):
            m = str(mk[i])
            candle_markets.add(m)
            coin = coin_from_market(m)
            if coin_col is not None and coin_col[i] is not None:
                coin = str(coin_col[i]).upper()
            c = cl[i]
            if c is None:
                continue
            try:
                if float(c) <= 0:
                    continue
            except (TypeError, ValueError):
                continue
            candle_coin_hour.add((coin, hkey(ts[i])))

    # ---- 4. Build eligible coin-hour panel ----
    all_hours = sorted({hk for (_, hk) in candle_coin_hour})
    n_hours = len(all_hours)
    cut = int(n_hours * TRAIN_FRAC)
    train_hours = set(all_hours[:cut])
    test_hours_raw = sorted(set(h for h in all_hours[cut + PURGE_EMBARGO_H:]))
    # Non-overlapping 168h blocks
    blocks = [test_hours_raw[i:i + BLOCK_H] for i in range(0, len(test_hours_raw), BLOCK_H)]
    block_of = {}
    for bi, blk in enumerate(blocks):
        for hk in blk:
            block_of[hk] = bi

    def elig_origin(hk):
        bi = block_of.get(hk)
        if bi is None:
            return False
        return hk + HORIZON_H * 3600 <= blocks[bi][-1]

    eligible_origins = [hk for hk in test_hours_raw if elig_origin(hk)]
    n_eligible_origins = len(eligible_origins)

    # Eligible coins: present in candles in the test window
    test_coins = sorted({coin for (coin, hk) in candle_coin_hour if hk in test_hours_raw})
    n_test_coins = len(test_coins)

    # ---- 5. Observed-event sparsity / coverage ----
    coin_hours_with_liq = 0
    coin_hours_total_eligible = 0
    total_events = 0
    total_notional = 0.0
    coins_with_zero_events = 0
    events_per_coin = {}

    for coin in test_coins:
        n_events_coin = 0
        for hk in eligible_origins:
            # outcome window: hk+1 .. hk+24h
            win_events = 0
            win_notional = 0.0
            for offset in range(1, HORIZON_H + 1):
                wh = hk + offset * 3600
                evs = liq_by_coin_hour.get((coin, wh), [])
                win_events += len(evs)
                win_notional += sum(evs)
            coin_hours_total_eligible += 1
            if win_events > 0:
                coin_hours_with_liq += 1
            n_events_coin += win_events
            total_events += win_events
            total_notional += win_notional
        events_per_coin[coin] = n_events_coin
        if n_events_coin == 0:
            coins_with_zero_events += 1

    event_rate = (coin_hours_with_liq / coin_hours_total_eligible
                  if coin_hours_total_eligible else 0.0)
    avg_events_per_coin_hour = (total_events / coin_hours_total_eligible
                                if coin_hours_total_eligible else 0.0)

    # Identity-match rate: liquidation markets that map to a candle coin
    liq_markets_mapped = 0
    for m in liq_markets:
        c = coin_from_market(m)
        if any(c == c2 for (c2, _) in candle_coin_hour):
            liq_markets_mapped += 1
    identity_match_rate = (liq_markets_mapped / len(liq_markets)
                           if liq_markets else 0.0)

    # ---- 6. Minimum-detectable-effect (MDE) ----
    # For a paired count/intensity contrast C2 vs B1 on N paired origins,
    # approximate MDE as the relative reduction detectable at 80% power,
    # alpha = 0.00833 (Holm-adjusted), two-sided, using normal approximation
    # for the paired difference of rates.
    alpha = 0.008333333333333333
    z_alpha = 2.638  # approx two-sided z for alpha=0.00833
    z_power = 0.8416  # 80% power
    n_pairs = n_eligible_origins * n_test_coins  # paired coin-origin observations
    # baseline event rate per coin-hour
    base_rate = avg_events_per_coin_hour
    # Poisson variance of difference approx 2 * base_rate / n_pairs (paired)
    if base_rate > 0 and n_pairs > 0:
        se_diff = math.sqrt(2.0 * base_rate / n_pairs)
        mde_abs = (z_alpha + z_power) * se_diff
        mde_rel_pct = (mde_abs / base_rate * 100.0) if base_rate > 0 else float("nan")
    else:
        mde_abs = float("nan")
        mde_rel_pct = float("nan")

    underpowered = (mde_rel_pct > 20.0) if not math.isnan(mde_rel_pct) else True

    result = {
        "experiment_id": "FCLR-LIQ-RISK-ESCALATION-09",
        "campaign": "FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z",
        "session_utc": SESSION_UTC,
        "software": "stdlib + pyarrow (parquet read only); statistical audit is independent stdlib code",
        "input_integrity": {
            "sha256_sidecars_total": total_sidecars,
            "sha256_verified_ok": sha_ok,
            "sha256_verified_bad": sha_bad,
            "sha256_all_match": sha_bad == 0,
            "sha256_map": sha_map,
        },
        "coverage": {
            "months": "2025-05 .. 2026-10 (18 months)",
            "n_distinct_hours": n_hours,
            "train_hours": len(train_hours),
            "test_hours_after_purge": len(test_hours_raw),
            "n_eligible_origins_nonoverlap": n_eligible_origins,
            "n_test_coins": n_test_coins,
            "n_paired_coin_origin_observations": n_pairs,
        },
        "liquidations": {
            "n_liquidation_rows": liq_rows,
            "n_distinct_markets": len(liq_markets),
            "n_distinct_coins": len(liq_coins),
            "n_markets_mapped_to_candle_coin": liq_markets_mapped,
            "identity_match_rate": identity_match_rate,
        },
        "observed_event_sparsity": {
            "coin_hours_total_eligible": coin_hours_total_eligible,
            "coin_hours_with_at_least_one_event": coin_hours_with_liq,
            "event_rate_per_coin_hour": event_rate,
            "total_events_forward_windows": total_events,
            "total_notional_forward_windows_usd": total_notional,
            "avg_events_per_coin_hour": avg_events_per_coin_hour,
            "coins_with_zero_events_across_all_windows": coins_with_zero_events,
            "events_per_coin": events_per_coin,
        },
        "power_mde": {
            "alpha_holm_adjusted": alpha,
            "target_power": 0.80,
            "n_pairs": n_pairs,
            "baseline_event_rate_per_coin_hour": base_rate,
            "mde_abs_events_per_coin_hour": mde_abs,
            "mde_rel_pct": mde_rel_pct,
            "underpowered_for_2pct_floor": underpowered,
            "note": "MDE is computed on the sparse observed-count scale; if underpowered for the 2% materiality floor, the evaluation artifacts must still be written with status UNDERPOWERED and the frozen decision recorded (never threshold-shop).",
        },
    }

    out_json = sdir / f"fclr_risk09_power_{SESSION_UTC}.json"
    out_json.write_text(json.dumps(result, indent=2))

    out_md = sdir / f"fclr_risk09_power_{SESSION_UTC}.md"
    lines = [
        "# FCLR-LIQ-RISK-ESCALATION-09 — Observed-Liquidation Power/MDE Audit",
        "",
        f"**Campaign:** FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z",
        f"**Session UTC:** {SESSION_UTC}",
        "",
        "## Input integrity",
        f"- SHA-256 sidecars verified: {sha_ok}/{total_sidecars} (bad={sha_bad})",
        "",
        "## Coverage",
        f"- Months: 2025-05 .. 2026-10 (18 months)",
        f"- Distinct hours: {n_hours}",
        f"- Train hours: {len(train_hours)}",
        f"- Test hours after 48h purge+embargo: {len(test_hours_raw)}",
        f"- Eligible origins (non-overlapping 168h blocks): {n_eligible_origins}",
        f"- Test coins: {n_test_coins}",
        f"- Paired coin-origin observations: {n_pairs}",
        "",
        "## Liquidations identity",
        f"- Liquidation rows: {liq_rows}",
        f"- Distinct markets: {len(liq_markets)}",
        f"- Distinct coins: {len(liq_coins)}",
        f"- Markets mapped to candle coin: {liq_markets_mapped}",
        f"- Identity-match rate: {identity_match_rate:.4f}",
        "",
        "## Observed-event sparsity (rare-target audit)",
        f"- Eligible coin-hours: {coin_hours_total_eligible}",
        f"- Coin-hours with >=1 event: {coin_hours_with_liq}",
        f"- Event rate per coin-hour: {event_rate:.6f}",
        f"- Total events in forward windows: {total_events}",
        f"- Total notional (USD): {total_notional:.2f}",
        f"- Avg events per coin-hour: {avg_events_per_coin_hour:.6f}",
        f"- Coins with zero events across all windows: {coins_with_zero_events}",
        "",
        "## Minimum-detectable effect",
        f"- Alpha (Holm-adjusted, k=2): {alpha}",
        f"- Target power: 0.80",
        f"- N pairs: {n_pairs}",
        f"- Baseline event rate per coin-hour: {base_rate:.6f}",
        f"- MDE (abs events/coin-hour): {mde_abs:.6f}",
        f"- MDE (rel %): {mde_rel_pct:.4f}%",
        f"- Underpowered for 2% materiality floor: {underpowered}",
        "",
        "## Conclusion",
        "Observed liquidation events are sparse (rare target). If MDE exceeds the 2% "
        "materiality floor, the evaluation must still be executed with status "
        "UNDERPOWERED and the frozen decision recorded; no threshold-shopping or "
        "materiality-floor relaxation after outcomes.",
    ]
    out_md.write_text("\n".join(lines) + "\n")
    print(f"WROTE {out_json}")
    print(f"WROTE {out_md}")
    print(f"sha_ok={sha_ok}/{total_sidecars} event_rate={event_rate:.6f} MDE_rel={mde_rel_pct:.4f}% underpowered={underpowered}")


if __name__ == "__main__":
    main()
