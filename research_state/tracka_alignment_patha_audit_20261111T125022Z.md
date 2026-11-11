# Track A Alignment Path (a) Audit — Admissible Hyperliquid Context Coverage
**Timestamp (UTC):** 2026-11-11T12:50:22Z
**Experiment:** `TRACKA-HL-20261111T073000Z` (frozen prereg: `research_state/tracka_prereg_hyperliquid_2026.json`)
**Path:** (a) extend coverage with admissible unauthenticated Hyperliquid-native evidence (no new network fetches; local cached provenance only)

## Scope / admissibility constraints (unchanged)
- Hyperliquid-only, 2025-06..2026-10 target; observed ironflow labels only (no modeled/proxy/synthetic); no Binance/2024 conflation.
- Context required by prereg: Hyperliquid mark price, index price, premium index, OHLCV klines, funding context, same window/symbols, provenance documented.
- No outcome inspection before (successor) prereg freeze.

## Evidence reviewed (local, cached)
| Artifact | Coverage / content | Provenance notes |
|---|---|---|
| `research_state/data_cache/ironflow_events/*.parquet` (2025-05..2026-10) | 18 months labels; complete months 2025-06..2026-10; 2.85M rows / 468 markets (`research_state/tracka_hl_alignment_blocker.md`) | ironflow/hyperliquid-liquidations, CC BY 4.0, unauth HF bulk; see `research_state/ironflow_probe_digest_latest.json` |
| `research_state/data_cache/hyperliquid_funding/{BTC,ETH,BNB,SOL,XRP,AVAX,DOGE,LINK,SUI}.json` | 8,668 rows each; **2025-11-01T00:00:00.078Z .. 2026-10-30T23:00:00.078Z** (hourly; fields incl. `coin,fundingRate,premium,time`) | Hyperliquid `info` `fundingHistory`, unauthenticated; fetched/cached per `scripts/hyperliquid_funding_fetch.py` workflow |
| `research_state/hl_pathb_probe_20261111T122801Z.json` | `candleSnapshot` 1h monthly probe, 9 coins: **n=0 for 2025-06..2026-03; partial 2026-04 (331-335); full 2026-05..2026-10 (mostly 720-744, minor HTTP 429 on AVAX 2026-09, BNB 2026-06 in probe)** | Hyperliquid `info` `candleSnapshot` (`req` payload), unauthenticated, ~6-7mo lookback; probe ran 182.9s, no outcomes inspected |
| `research_state/hl_coverage_probe.json`, `research_state/tracka_hl_alignment_blocker.md` | Prior depth probes consistent (mark-price candles ~2026-05..2026-10; no separate historical index/premium endpoint identified) | Same admissible API family |

Local cache search (`research_state/data_cache/`, repo root zips/dirs) shows no additional admissible Hyperliquid-native historical mark/index/premium/klines or funding extending back to 2025-06.

## Findings (path a)
1. **Labels:** sufficient for full prereg window 2025-06..2026-10 (9 funded symbols present as `*-PERP`).
2. **Funding:** admissible coverage only **2025-11-01..2026-10-30** → missing 2025-06..2025-10 (5 months) required by frozen splits (train starts 2025-06-01).
3. **Mark/OHLCV candles:** admissible `candleSnapshot` coverage only **~2026-05..2026-10** (2026-04 partial) → missing 2025-06..2026-04.
4. **Index price / premium index historical series:** no separate admissible unauthenticated historical endpoint identified/cached; funding rows include `premium` but not a complete aligned mark/index/klines context back to 2025-06.
5. **Maximal intersection (labels + funding + usable candles):** **2026-05-01..2026-10-31** (6 months). This deviates materially from frozen prereg window/splits (`2025-06-01..2026-10-31`, train through 2025-11-30, ≥3 30d test blocks from 2026-02 onward as specified).

## Conclusion
**Path (a) exhausted on available admissible local evidence: full prereg panel `2025-06..2026-10` is NOT buildable.** Track A cannot execute the frozen prereg `TRACKA-HL-20261111T073000Z` as specified.

## Required next action (terminalize Track A)
- **Do not** compute outcomes under the frozen prereg.
- Proceed to **path (b)**: freeze a NEW successor prereg (pre-outcomes) scoped to `2026-05-01..2026-10-31` (or tighter if required for completeness), with explicit symbols, 7d embargo, splits, and feasibility of ≥3 non-overlapping test blocks / min paired instruments documented; record input hashes/checksums; only then build aligned panel and run evaluation → emit `evaluation_summary_TRACKA-HL-<successor>.md` and update `run_manifest`/`experiment_frontier`/`hypothesis_registry`/final verdict atomically.
- If successor prereg cannot meet minimum claim-worthy/test requirements on admissible overlap, take **path (c)**: emit terminal verdict artifact closing Track A panel as `NOT_SUPPORTED`/`BLOCKED` (alignment/context insufficient) with evidence, and update state atomically.
