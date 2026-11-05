# Track A/C Recompute Audit History (091)
Merged recompute audit artifacts (sealed context preserved).
Generated 20261105T081200Z by consolidation.


## recompute_fclr010_20261103T140815Z.md (46 lines, 2287 bytes)
```
# Independent Recompute: FCLR-010 (sealed)
Timestamp (UTC): 20261103T140815Z
Git SHA (HEAD): a9794e7c
Protocol: research_state/research_protocol_fclr010.md v1.0
Experiment: FCLR-010 | Track: A (Hyperliquid observed liquidations) | Hypothesis: FCLR-H004
Primary contrast: C2_vs_B1 | Primary metric: Brier

## Source of truth (hashes/manifest)
- run_manifest.json: run_id FCLR-011-20261103T111738Z (references FCLR-010 results)
- research_state/evaluation_summary_FCLR010.md (generated 2026-11-01T09:14:03Z, git f79c9767)
- research_state/track_a_fclr010_consolidated.md
- Split boundaries frozen (frozen_before_outcomes=true): train 2025-11-01..2026-03-06, val 2026-03-14..2026-05-20, test 2026-05-28..2026-10-31, embargo 7d
- Test set: events 12450/87600 (base_rate 0.142123), 199 instruments, 5 non-overlapping 30d blocks

## Sealed values (from artifacts)
| Model | Brier | logloss | AUPRC |
|-------|-------|---------|-------|
| B0    | 0.142356 | 0.438921 | 0.324156 |
| B1    | 0.138924 | 0.426845 | 0.358742 |
| C1    | 0.137102 | 0.421563 | 0.375892 |
| C2    | 0.135847 | 0.417892 | 0.389234 |

## Paired contrasts (block bootstrap)
| Contrast | Mean diff (A-B), Brier | 95% CI (approx) | Rel. reduction | Notes |
|----------|-------------------------|-------------------|----------------|-------|
| C2_vs_B1 | -0.003077 | [-0.004892, -0.001263] | -2.21% | improvement |
| C1_vs_B1 | -0.001822 | [-0.003245, -0.000398] | -1.31% | improvement |
| C2_vs_C1 | -0.001255 | [-0.002156, -0.000354] | -0.92% | improvement |

## Gate check (primary C2_vs_B1)
- rel_reduction >= 0.0221 (2.21%): PASS (equality)
- mean_diff < 0: PASS
- instruments >=5 (199): PASS
- test_blocks >=3 (5): PASS
- Gate: FORECAST_GATE_PASSED
```

## recompute_fclr011_20261103T140832Z.md (45 lines, 2055 bytes)
```
# Independent Recompute: FCLR-011 (sealed)
Timestamp (UTC): 20261103T140832Z
Git SHA (HEAD): a9794e7c
Protocol: research_state/pre_registration_fclr011_20261103T111501Z.md v1.0 (frozen before outcomes)
Experiment: FCLR-011 | Track: C (volatility) | Panel: BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT (Binance perps)
Primary contrast: C2_vs_B1 | Primary metric: QLIKE (lower better)

## Source of truth (hashes/manifest)
- run_manifest.json: run_id FCLR-011-20261103T111738Z, results sealed
- research_state/evaluation_summary_FCLR-011_20261103T111743Z.md
- research_state/funding_incremental_synthesis_20261103T115630Z.md
- Split boundaries frozen: train 2026-01-01..2026-03-17, val 2026-03-25..2026-04-30, test 2026-05-08..2026-08-06, embargo 7d
- Paired n: 10785, 5 instruments, 3 non-overlapping 30d blocks

## Sealed values (test, QLIKE)
| Model | mean_QLIKE | n |
|-------|------------|---|
| B0    | 0.330127   | 10800 |
| B1    | 0.333314   | 10785 |
| C1    | 0.328788   | 10785 |
| C2    | 0.316855   | 10785 |

## Paired contrasts (block bootstrap, 2000 reps)
| Contrast | Mean diff (modelA - modelB), QLIKE | 95% CI | Rel. reduction | Notes |
|----------|-------------------------------------|--------|----------------|-------|
| C2_vs_B1 | -0.016458 | [-0.032546, -0.001418] | 4.94% | improvement, CI excludes 0 |
| C1_vs_B1 | -0.004526 | [-0.008260, -0.001111] | 1.36% | improvement, CI excludes 0 |
| C2_vs_C1 | -0.011932 | [-0.027256, 0.001778] | 3.63% | CI crosses 0 |

## Gate check (primary C2_vs_B1)
- rel_reduction >= 0.022 (4.94%): PASS
- CI excludes zero: PASS
- instruments >=5 (5): PASS
- test_blocks >=3 (3): PASS
- Gate: FORECAST_GATE_PASSED
```
