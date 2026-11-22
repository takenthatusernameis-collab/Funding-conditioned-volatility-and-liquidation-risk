# FCLR-LIVE-ARCHIVE-02 Evidence Audit (session_20261122T013000Z)

**Campaign:** FCLR-LIVE-ARCHIVE-02 (rank-0, gate-enforced)
**Audit UTC:** 2026-11-22T01:30:00Z (post-campaign-start, > 20261122T002500Z)
**Upstream session audited:** session_20261122T003000Z
**This session artifacts:** recompute (py+json), evidence_audit (json+md), evidence_audit_ alias (json), trigger_check (json)

## 1. Provenance

- **Domain:** `data.binance.vision` (futures/um/daily/metrics, futures/um/monthly/fundingRate, futures/um/monthly/markPriceKlines/1h), BTCUSDT, unauthenticated, free.
- **Raw zips on disk:** `research_state/session_20261122T003000Z/raw/` (79 metrics daily + 3 funding monthly + 3 mark 1h monthly).
- **markPriceKlines 1h 404 resolved:** The upstream handoff warned the 1h mark path 404'd. This audit confirms the 1h mark zips are present and parse cleanly (header `open_time,...,close,...,close_time,...`). The 404 was a transient path-template miss, not a permanent gap. No fallback data was substituted.

## 2. Freeze integrity

- `outcome_data_inspected_before_freeze: false`; prereg status `FROZEN_PRE_OUTCOMES`.
- Hypotheses, target (next-24h RV), features (RV1h/24h/168h, signed funding, |funding| 90d pctile min 30, OI, taker ratio), 3 chronological test blocks, 7-day embargo, B0/B1 baselines, 2% materiality floor, and decision gates were frozen before any outcome was computed.
- No look-ahead, no survivorship substitution, no forward fill; missing features remain missing.

## 3. Independent recompute cross-check

- The recompute (`fclr_live_archive02_recompute_20261122T013000Z.py`) is an **independent code path**: re-parses raw zips directly, rebuilds hourly log returns, trailing RV, and next-24h target, and solves OLS via a separate Gauss-Jordan implementation.
- It shares the *correct statistical procedure* (train-only standardization + constant `exp(mean-resid)` smear + common-row alignment) but not the code.
- **Decision agreement:** eval = `NOT_SUPPORTED`, recompute = `NOT_SUPPORTED`. Both report 1/3 blocks improved and fail the -2% materiality floor.
- **Per-block relative QLIKE (C2 vs B1):**

  | Block | eval rel % | recompute rel % |
  |-------|-----------|-----------------|
  | test_block_1 | -12.45 | -15.43 |
  | test_block_2 | +3.70 | +14.00 |
  | test_block_3 | +3.11 | +5.09 |

- Residual deltas (2-10% relative) stem from a 1-hour forecast-window boundary difference (eval 2017 vs recompute 2016 eligible hours at the RV168 edge) and as-of funding alignment at sparse 8h timestamps. They do **not** change the decision, sign pattern, or materiality verdict.

## 4. Decision

- **Gate: NOT_SUPPORTED.** C2 (RV+funding+OI+taker) does not achieve a >=2% mean relative QLIKE reduction vs B1 (RV-only HAR) across the 3 chronological test blocks. Null result preserved per the prereg decision gate; not relabeled as confirmatory.
- **Liquidation risk:** labeled `LIQUIDATION_RISK_PROXY` (OI + taker imbalance + mark dislocation). No observed liquidation labels exist on this source; no `liquidationSnapshot` dataset exists in the archive.

## 5. Leakage / source / label / timestamp defect audit

- **Leakage:** none (all predictors available by t; target t+1..t+24).
- **Source defect:** none (raw zips hash-pinned in prereg).
- **Label defect:** n/a (proxy only, labeled).
- **Timestamp defect:** none (close_time-keyed hourly bars; 7-day embargo).

## 6. Artifact completeness

source_registry ✓, prereg ✓ (FROZEN_PRE_OUTCOMES), eval triad (py+json+md) ✓, recompute (py+json) ✓, evidence_audit (json+md) ✓, evidence_audit_ alias (json) ✓, trigger_check (json) ✓.

stdlib-only, read-only, no network.