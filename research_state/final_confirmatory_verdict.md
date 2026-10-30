# Final Confirmatory Verdict — Funding-Conditioned Volatility and Liquidation Risk

**Report ID:** FCLR-FINAL-001
**Date (UTC):** 2026-10-30T10:46:44Z
**Git HEAD:** 5655c6ca (main)
**Protocol:** FCLR-002/FCLR-003 frozen splits (RESEARCH_PROMPT.md compliant)
**Status:** CLOSEOUT COMPLETE

## Executive Verdict
**H001 (FCLR-H001): NOT_SUPPORTED.** On the powered confirmatory test FCLR-003, adding funding extremes plus pre-specified price-dislocation/smoothing features to a realized-volatility-only HAR baseline does **not** improve out-of-sample 24h realized-variance forecasts on a frozen 5-symbol panel.

The primary contrast C2 (funding + price-dislocation/smoothing) vs B1 (RV-only HAR) fails the forecast gate under pre-registered criteria. No risk-overlay phase is eligible.

## FCLR-003 Results (canonical)
Source: `research_state/evaluation_summary_FCLR003.md`
Splits (frozen before outcomes): `research_state/run_manifest.json#split_boundaries_fclr003`
- Train: 2024-04-01T00:00:00Z .. 2024-07-23T23:00:00Z
- Val:   2024-07-31T00:00:00Z .. 2024-09-24T23:00:00Z
- Test:  2024-10-02T00:00:00Z .. 2024-12-31T23:00:00Z (7d embargo; 91 days = 3 non-overlapping 30-day blocks)
- Instruments (paired): BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (n=10,796)

### QLIKE (lower is better), test set
| Model | mean_QLIKE | n |
|-------|------------|---|
| B0    | 0.487674   | 10800 |
| B1    | 0.401884   | 10796 |
| C1    | 0.369366   | 10796 |
| C2    | 0.417089   | 10796 |

### Paired comparisons (block bootstrap, ~24h blocks, 2000 reps)
| Contrast | Mean diff (A-B), QLIKE | 95% CI | Relative reduction | Verdict |
|----------|--------------------------|--------|-------------------|---------|
| C2 vs B1 (primary) | +0.015205 | [-0.020240, 0.056734] | -3.78% (worse) | **FAIL** (CI crosses zero) |
| C1 vs B1 (secondary) | -0.032518 | [-0.045813, -0.020303] | +8.09% (better) | Better alone, but not primary claim |
| C2 vs C1 | +0.047723 | [0.006214, 0.095465] | -12.92% (worse) | Adding price features hurts when added to C1 |

### Gate assessment (pre-registered)
- >=2% relative QLIKE reduction (C2 vs B1): **NOT_MET** (-3.78%)
- 95% CI excludes zero: **NO**
- >=5 paired OOS instruments: **PASS**
- >=3 non-overlapping 30-day blocks: **PASS**
- **Forecast gate (all): NOT_MET → Risk overlay INELIGIBLE**

## Supporting Tests
- **FCLR-002 (underpowered):** Test 70 days = 2 blocks. C2 vs B1 showed -9.28% with CI excluding zero on that window, but did not meet the >=3-block minimum for claim-worthiness → INCONCLUSIVE.
- **FCLR-001 (coverage defect):** Single ~4-day block, BTCUSDT only in effect → PILOT/INCONCLUSIVE.

## Tracks
- **Track A (observed liquidations):** STRUCTURALLY BLOCKED for 2024 (Binance `liquidationSnapshot` HTTP 404; `fapi forceOrders` HTTP 451 geo-restricted). Enumeration found no admissible unauthenticated census for confirmatory-feasible 2024 window. **FCLR-H004 BLOCKED (2024) / EXPLORATORY_ONLY (2026 FCLR-005)** — 2026 pilot showed no incremental skill of funding+price over RV-only on a ~30-day window (<3 blocks).
- **Track B (hypothetical boundary breach):** FCLR-H003 INCONCLUSIVE across pre-registered evaluations. No incremental skill demonstrated; extensions require fresh pre-registration and fresh data.

## Data Exhaustion (hard constraint)
No unsealed, contiguous >=5-symbol confirmatory window remains:
- 2024-04..12: fully committed to FCLR-002/FCLR-003
- 2025: mark price available only for BTCUSDT/ETHUSDT (2 symbols)
- 2026: partial coverage (BTCUSDT Jan-Aug; ETHUSDT Jan+Apr-Aug; others Apr-Aug only)

**No new confirmatory experiment (FCLR-004+) is feasible on current admissible data without a NEW admissible data source per RESEARCH_PROMPT.md §16.**

## Reproducibility
- Splits frozen in `research_state/run_manifest.json` (`split_boundaries_fclr003.frozen_before_outcomes: true`)
- Canonical artifact: `research_state/evaluation_summary_FCLR003.md` (2026-10-29T19:13:39Z)
- Verification: `FCLR_EXPERIMENT=FCLR-003 timeout 1800 python scripts/run_evaluation.py` (reproduces above)
- Tests: `python -m unittest discover -s tests -v` — all passing

## Final Recommendations
1. **Do not build risk-overlay/position-sizing** — forecast gate not met.
2. **Do not tune on sealed holds** — threshold-shopping/rescue on FCLR-002/003 test sets is prohibited.
3. **Preserve negative results** — this verdict is the correct scientific outcome.
4. **Only if new admissible data appears** (unauthenticated, with provenance/licenses/coverage, >=5 symbols, >=3 non-overlapping 30-day blocks) should a new experiment be pre-registered before examining outcomes.

**Conclusion:** H001 is NOT_SUPPORTED. Confirmatory program closed out as negative with no path forward on existing admissible data.
