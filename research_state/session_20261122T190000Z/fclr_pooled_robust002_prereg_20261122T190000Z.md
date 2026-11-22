# FCLR-POOLED-ROBUST-002 Preregistration (frozen before outcomes)

**Experiment:** FCLR-POOLED-ROBUST-002
**Campaign:** FCLR-POOLED-ROBUST-002-20261122T180000Z
**Session UTC:** 20261122T190000Z
**Outcome data inspected before freeze:** false
**Frozen before outcomes:** true

## Context

FCLR-POOLED-001 (session_20261122T092003Z) returned NOT_SUPPORTED: funding-conditioned features add ~0.0% QLIKE vs RV-only baseline, below the -2.0% materiality floor, bootstrap CI95 includes zero. FCLR-POOLED-AUDIT-001 (session_20261122T165200Z) found concrete quality gaps that could have manufactured OR masked that null:

- d2: only a 1-hour train/test gap (48h purge+embargo NOT applied)
- d10: overlapping forward outcomes (pairwise Jaccard 0.52..0.92 dependence)
- d4: 6.8% of rows above the 1% mark/index tolerance
- d6/d7: delisting/survivorship (344 coins new, 44 exited, survivor share 38%)
- d9: monthly threshold drift

This is a heavy, outcome-blind, leakage-hardened RE-CONFIRMATION applying all remediations simultaneously. It is NOT a re-run of FCLR-POOLED-001 and NOT a re-run of the FCLR-POOLED-AUDIT-001 audit.

## Remediations applied

| Audit gap | Remediation |
|-----------|-------------|
| d2 split embargo | 48h purge+embargo on the chronological train/test boundary (cut + 48h dropped before test) |
| d10 overlapping outcomes | non-overlapping 168h forward blocks; only origins whose 24h forward window fits inside one block are eligible |
| d4 mark/index tolerance | exclude rows where |mark-oracle|/oracle > 1% |
| d6 delisting identity | delisting-aware per-coin identity from candles; survivors = present in final 5% of hours |
| d7 survivorship | survivors-vs-exited sensitivity arm reported separately |
| d9 threshold drift | per-month funding-tercile thresholds on train only; drift (max/mean abs t2 change) reported |

## Design

- **Data:** ironflow bulk {candles_1h, funding, open_interest}, 18 months 2025-05..2026-10, sha256 asserted before every read, read-only.
- **Splits:** train = first 70% of distinct hourly timestamps; test = remaining after 48h purge+embargo, restricted to non-overlapping 168h-block origins with mark-oracle tolerance pass.
- **Primary target:** forward 24h realized variance (sum of squared 1h log returns over t+1..t+24h).
- **Primary metric:** QLIKE(C2) - QLIKE(B1), absolute difference and relative % reduction.
- **Models:** B1 = HAR-style OLS on log RV1h, log RV24h, log RV168h (train-only standardized, smearing correction). C2 = B1 + signed funding + premium index + open interest.
- **Secondary target:** Track B modeled boundary-breach proxy (breach if sqrt(forward 24h RV) > 2.5% band = 20x lev, 50% maint). **LABELED MODELED, NEVER OBSERVED LIQUIDATION.**
- **Secondary metrics:** Brier, log loss, Brier skill vs climatology.

## Decision rule (symmetric)

- **Materiality floor:** 2.0% relative QLIKE reduction.
- **Uncertainty:** per-coin block bootstrap, 2000 replicates, seed 20261122; CI95 of rel_pct.
- **Multiplicity:** Holm across declared family {C2_vs_B1_primary, survivors_arm, exited_arm}; raw and Holm-adjusted p reported.
- **Alpha-spending:** sequential confirmatory look k=2; alpha_2 = 0.05/(2*3) = 0.008333.
- **Decision:** SUPPORTED_LEAKAGE_ROBUST_EDGE iff materiality_met AND bootstrap CI95 upper bound < 0 AND Holm-adjusted primary p < alpha_2; otherwise NOT_SUPPORTED_LEAKAGE_ROBUST_NULL (null confirmed leakage-robust). Either outcome is valid and publishable.

## Software

Stdlib + pyarrow only. numpy/pandas/scipy NOT used. No network. No new source.

## Independent recompute

`fclr_pooled_robust002_recompute_20261122T190000Z.py` (independent stdlib recompute from stored input hashes, no pyarrow, reproduces headline QLIKE within declared tolerance).