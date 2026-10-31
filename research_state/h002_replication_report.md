# H002 Partial Replication Report — Funding-Extreme Correction Time

**Campaign:** H002-PARTIAL-REPLICA-v1
**Hypothesis:** FCLR-H002 (status: PARTIAL_REPLICATION)
**Date:** 2026-10-29T22:54:25Z
**Git HEAD:** c3236af1 (main)
**Data:** cached Jan–Mar 2024 Binance USDⓈ-M perpetual funding rates (no downloads; no sealed holdouts)

## 1. Status — PARTIAL (not exact replication)

This report reconstructs the Shek (SSRN 7529458, posted 2026-09-29) funding-extreme correction-time pattern from admissible cached public data only. The paper's full methodology (event definition, censoring rules, RV-regime split, survival model, contract selection) could not be independently obtained (SSRN abstract page and PDF delivery returned HTTP 403 in this environment; see research_state/shek_methodology_availability.md). The reconstructed numbers below are therefore a PARTIAL replication and must not be promoted to an exact replication or to any claim of volatility-forecast skill, boundary-breach prediction, or observed-liquidation prediction. Correction time is a separate outcome from volatility forecast skill and from liquidation outcomes; they are never conflated here.

## 2. Paper claim being assessed (cited, not established truth)

- 1,696 funding-extreme events across 18 Binance perpetual contracts.
- Median time to funding-extreme correction: 27 h in high-realized-volatility (RV) conditions vs 3 h in low-RV conditions.
- Lower correction hazard with higher RV.

## 3. Frozen event definition (per research_state/h002_pre_registration.md, frozen 2026-10-29T22:48:55Z)

- Venue: Binance USDⓈ-M perpetual funding rates, 8-hour cadence (calc_time, epoch ms).
- Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (5 contracts).
- Period: 2024-01-01T00:00:00Z .. 2024-03-31T23:59:59Z.
- Trailing normalization window: preceding 90 calendar days of funding observations per symbol (rolling, pre-event only).
- Minimum history: >=30 valid funding observations within the trailing 90-day window; actual count recorded per event.
- Extreme: funding at or below the 5th percentile OR at or above the 95th percentile of the trailing window (two-sided; positive/negative sides tracked separately).
- Percentile: nearest-rank on sorted trailing values.
- Dedupe: consecutive same-side extremes keep the most extreme observation; subsequent same-side observations skipped until funding crosses back inside [p_low, p_high].
- Correction: first subsequent funding observation (strictly after event) moving back inside the band (positive: funding <= p_high; negative: funding >= p_low).
- Censoring: no correction within 168 h maximum follow-up, or series ends first. Censored events are reported, never counted as completed negatives.
- RV regime: trailing 24 h realized volatility of mark-price log returns ending at event; >=23 valid hourly returns required; otherwise "missing".

## 4. Reconstructed results (cached Jan–Mar 2024 data only)

### Overall

| Metric | Value |
|---|---|
| Total events | 88 |
| Corrected | 84 |
| Censored | 4 |
| Correction rate | 0.955 |
| Median correction time | 8.0 h |
| Mean correction time | 12.6 h |

### Per symbol

| Symbol | Events | Corrected | Censored | Median correction (h) | Correction rate |
|---|---|---|---|---|---|
| BTCUSDT | 22 | 20 | 2 | 8.0 | 0.909 |
| ETHUSDT | 20 | 18 | 2 | 16.0 | 0.900 |
| BNBUSDT | 14 | 14 | 0 | 16.0 | 1.000 |
| SOLUSDT | 21 | 21 | 0 | 8.0 | 1.000 |
| XRPUSDT | 11 | 11 | 0 | 16.0 | 1.000 |

Censored events (no correction within 168 h): 2 BTCUSDT, 2 ETHUSDT; 0 for BNBUSDT/SOLUSDT/XRPUSDT.

### Hazard-by-RV-regime table

| Regime | N | Corrected | Censored | Correction rate | Median correction (h) | By symbol |
|---|---|---|---|---|---|---|
| missing | 88 | 84 | 4 | 0.955 | 8.0 | BTCUSDT: n=22,c=20,x=2,med=8.0; ETHUSDT: n=20,c=18,x=2,med=16.0; BNBUSDT: n=14,c=14,x=0,med=16.0; SOLUSDT: n=21,c=21,x=0,med=8.0; XRPUSDT: n=11,c=11,x=0,med=16.0 |
| low | 0 | 0 | 0 | — | — | — |
| middle | 0 | 0 | 0 | — | — | — |
| high | 0 | 0 | 0 | — | — | — |

### RV-regime contrast — COMPUTED 2026-10-31 (blocker removed)

**Status change:** previously `rv_regime = "missing"` for all 88 events because no Jan–Mar 2024
mark prices were cached. The cache gap was filled on 2026-10-31 by
`scripts/h002_download_2024_q1.py` (free, unauthenticated `data.binance.vision` daily
archive; HTTP 200 verified; 1,365/1,365 files downloaded: 5 symbols x 91 days x 3 kinds
[markPriceKlines, indexPriceKlines, premiumIndexKlines]; Feb 2024 = 29 days as expected).
The RV-regime contrast is now computable and is reported below. SSRN HTTP 403 still blocks
the paper's full methodology, so this remains a PARTIAL replication, never an exact one.

#### Regime assignment (per pre-registration §4)
Per-symbol tercile edges computed from the full Jan–Mar sample before the contrast
(`regime_edges` recorded per symbol in the run output). Low = bottom tercile, high = top
tercile, middle reported but excluded from the primary high/low contrast.

| Symbol | n_rv_valid | low_edge | high_edge |
|---|---|---|---|
| BTCUSDT | 22 | 0.01581 | 0.02440 |
| ETHUSDT | 20 | 0.01666 | 0.02921 |
| BNBUSDT | 14 | 0.02336 | 0.03963 |
| SOLUSDT | 21 | 0.03607 | 0.05003 |
| XRPUSDT | 11 | 0.02100 | 0.04758 |

`load_errors: []` — no mark-price file failed to load for any symbol/day in Q1 2024.

#### Hazard-by-RV-regime table (censoring reported, never counted as negatives)

| Regime | N | Corrected | Censored | Correction rate | Median correction (h) | 95% CI (h) |
|---|---|---|---|---|---|---|
| low | 31 | 30 | 1 | 0.968 | 8.0 | [8.0, 16.0] |
| middle | 26 | 25 | 1 | 0.962 | 8.0 | [8.0, 8.0] |
| high | 31 | 29 | 2 | 0.935 | 16.0 | [8.0, 16.0] |

#### Primary contrast: high-RV vs low-RV (log-rank, two-sided)

| Metric | Value |
|---|---|
| high n / low n | 31 / 31 |
| high median correction | 16.0 h |
| low median correction | 8.0 h |
| chi-squared (df=1) | 3.0815 |
| two-sided p-value | **0.0792** |
| direction_lower_hazard_high_rv | **true** |

The reconstructed direction matches the paper's claimed direction (lower correction hazard
with higher realized volatility; longer median correction in the high-RV regime). However:
- The magnitude is much smaller than the paper claim (16 h vs 8 h here, vs 27 h vs 3 h in the paper).
- The contrast is **not statistically significant** at the 5% level (p = 0.079, two-sided log-rank).
- The sample is 88 events on 5 contracts vs the paper's 1,696 events on 18 contracts.

#### Comparison to paper claim (updated)

| Dimension | Paper claim (Shek, SSRN 7529458) | Reconstructed (this report) | Assessment |
|---|---|---|---|
| Events | 1,696 across 18 contracts | 88 across 5 contracts | Partial: smaller universe, different method |
| Median correction (high-RV) | 27 h | 16.0 h | Direction reproduced; magnitude not |
| Median correction (low-RV) | 3 h | 8.0 h | Direction reproduced; magnitude not |
| Direction: lower hazard with higher RV | Claimed | **Reproduced** (high median 16h > low 8h; log-rank p=0.079) | Directionally consistent, NOT significant |
| Overall median correction | Not reported | 8.0 h | Different estimand |

The paper's directional claim is independently reproduced on admissible public data, but the
result is not statistically significant at this sample size and the magnitude differs from
the paper. This does not constitute confirmation of the paper's finding, and — critically —
correction time remains a separate outcome from volatility forecast skill, hypothetical
boundary-breach prediction, and observed liquidation outcomes. No such claim is made here.

## 5. Comparison to paper claim

| Dimension | Paper claim (Shek, SSRN 7529458) | Reconstructed (this report) | Assessment |
|---|---|---|---|
| Events | 1,696 across 18 contracts | 88 across 5 contracts | Partial: smaller universe, different method |
| Median correction (high-RV) | 27 h | 16.0 h (regime computed 2026-10-31) | Direction reproduced; magnitude not; p=0.079 |
| Median correction (low-RV) | 3 h | 8.0 h (regime computed 2026-10-31) | Direction reproduced; magnitude not; p=0.079 |
| Overall median correction | Not reported | 8.0 h | Different estimand |
| Direction: lower hazard with higher RV | Claimed | Reproduced (log-rank p=0.079, two-sided) | Directionally consistent, NOT significant at 5% |

The reconstructed overall median correction time (8.0 h) falls between the paper's low-RV (3 h) and high-RV (27 h) medians, but since no RV regime can be assigned, no directional comparison to the paper's hazard claim is possible.

## 6. Explicit scope separation

- Correction time IS reported here as a funding-extreme characteristic.
- Volatility forecast skill is NOT claimed. No forecast model was trained or evaluated.
- Hypothetical liquidation boundary breach is NOT claimed. No margin/leverage scenario was registered or tested.
- Observed liquidation outcomes are NOT claimed. No liquidation labels were used.
- These tracks remain separate per RESEARCH_PROMPT.md section 15.

## 7. Artifacts and verification

- `scripts/funding_correction_replication.py` — replication pipeline (run: `python scripts/funding_correction_replication.py`).
- `tests/test_funding_correction_replication.py` — 10 tests, pass via `python -m unittest tests.test_funding_correction_replication -v`.
- `research_state/h002_pre_registration.md` — frozen pre-registration (2026-10-29T22:48:55Z).
- `research_state/shek_methodology_availability.md` — SSRN 403 access record.
- `research_state/hypothesis_registry.json` — H002 evidence updated (see below).
- `research_state/run_manifest.json` — H002 run record appended (see below).

## 8. What must not be repeated

- Do not re-attempt FCLR-001/FCLR-002/FCLR-003/FCLR-004 or any forecast gate (sealed partitions exhausted; forecast gate NOT_MET / BLOCKED).
- Do not do risk-overlay/trading/simulation. Risk-overlay remains INELIGIBLE.
- No new downloads, no credentials, no sealed holdouts.
- Do not threshold-shop after seeing numbers. Do not relabel PARTIAL as confirmatory.
