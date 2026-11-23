# FCLR-POOLED-ROBUST-002 Evidence Audit (20261122T190000Z)

## Inputs verified
- Prereg present and frozen before outcomes (`outcome_data_inspected_before_freeze: false`)
- Robustness result present (`fclr_pooled_robust002_robustness_20261122T190000Z.json`)
- Independent recompute present (`fclr_pooled_robust002_recompute_20261122T190000Z.json`)

## Provenance
- Data: ironflow bulk {candles_1h, funding, open_interest}, 18 months 2025-05..2026-10
- sha256 asserted before every read; 54/54 files matched, 0 mismatched
- Caches never mutated; no network; no new source
- Software: stdlib + pyarrow only (numpy/pandas/scipy not used)

## Design fidelity
| Remediation | Applied | Matches prereg |
|-------------|---------|----------------|
| d2 48h purge+embargo | 48h | yes |
| d10 non-overlapping 168h blocks | 168h | yes |
| d4 1% mark-oracle tolerance | 0.01 | yes |
| d6 delisting-aware identity | yes | yes |
| d7 survivors-vs-exited arm | yes | yes |
| d9 per-month threshold drift | yes | yes |

## Recompute agreement
- Independent recompute PASS
- QLIKE B1 agree within 1e-6: robust 4033.4168819088313 vs recompute 4033.4168819088322
- QLIKE C2 agree within 1e-6: robust 4074.201549089205 vs recompute 4074.201549089229
- n_test_rows agree: yes

## Decision integrity
- Materiality floor 2.0%: NOT MET (rel_pct = +1.011%, i.e. C2 is worse than B1)
- Bootstrap CI95 rel%: [-0.110, +1.025] (includes zero)
- Holm-adjusted primary p = 0.6365 vs alpha_2 = 0.00833: NOT significant
- Decision: NOT_SUPPORTED_LEAKAGE_ROBUST_NULL
- Null preserved honestly; no threshold shopping; no relaxed materiality floor; no overlay built

## Verdict

The FCLR-POOLED-001 NOT_SUPPORTED null is confirmed leakage-robust. After applying all FCLR-POOLED-AUDIT-001 remediations simultaneously, funding-conditioned features (C2) add +1.01% QLIKE vs the HAR-RV baseline (B1), which is WORSE than the baseline (positive diff = higher QLIKE = worse), fails the -2% materiality floor, and the bootstrap CI95 includes zero. The earlier null was NOT a leakage artifact.