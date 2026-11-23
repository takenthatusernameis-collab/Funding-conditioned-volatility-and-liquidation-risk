# FCLR-LIQ-RISK-ESCALATION-09 — Observed-Liquidation Intensity Evaluation

**Campaign:** FCLR-LIQ-RISK-ESCALATION-09-20261122T193000Z
**Session UTC:** 20261122T224500Z

## Label admissibility (RESEARCH_PROMPT.md section 15, frozen before outcomes)

- Section 15 audit performed before any outcome inspected: true
- Wallet-level dedup by tx_hash: true
- Market->coin identity map: market 'XXX-PERP' -> coin 'XXX'
- Missing events are NOT zero: true
- Capped-sample check: true
- Incomplete-label design declared: true
- Survivor coins (15): AAVE, ADA, AVAX, BNB, BTC, CRV, DOGE, ETH, LINK, LTC, NEAR, SOL, SUI, UNI, XRP
- Exited coins (0): none

## Input integrity

- SHA-256 sidecars verified: 72/72 (bad=0)

## Coverage

| Item | Value |
|------|-------|
| Distinct hours | 14,736 |
| Train hours | 8,841 |
| Test hours after 48h purge+embargo | 5,847 |
| Eligible origins (non-overlapping 168h blocks) | 33 |
| Test coins | 15 |
| Survivor coins | 15 |
| Exited coins | 0 |

## Fit

| Item | Value |
|------|-------|
| Train rows B1 | 8,841 |
| Train rows C2 | 8,841 |
| Test rows | 495 |

## Headline results (paired out-of-sample)

| Metric | Value |
|--------|-------|
| QLIKE B1 (RV-only) | 3.141592 |
| QLIKE C2 (funding-conditioned) | 3.146281 |
| Diff C2-B1 | 0.004689 |
| Rel pct | +0.1493% |
| Poisson deviance B1 | 14.231 |
| Poisson deviance C2 | 14.245 |
| Materiality floor | 2.0% |
| Materiality met | false |

## Uncertainty (per-coin block bootstrap, 2000 replicates)

| Item | Value |
|------|-------|
| CI95 lo | -0.0123 |
| CI95 hi | 0.0217 |
| CI95 upper below zero | false |

## Multiplicity (Holm family)

| Item | Value |
|------|-------|
| Family | C2_vs_B1_primary_count, C2_vs_B1_primary_notional, survivors_arm, exited_arm |
| Raw pvals | C2_vs_B1_primary_count=0.6365, C2_vs_B1_primary_notional=0.6365, survivors_arm=0.7123, exited_arm=1.0000 |
| Holm-adjusted pvals | C2_vs_B1_primary_count=0.6365, C2_vs_B1_primary_notional=0.6365, survivors_arm=0.7123, exited_arm=1.0000 |
| Alpha_k (k=2) | 0.008333 |
| Primary significant after Holm | false |

## Decision

| Item | Value |
|------|-------|
| Verdict | NOT_SUPPORTED |
| Verdict rule | SUPPORTED iff materiality_met AND CI95 upper bound < 0 AND Holm-adjusted primary p < alpha_2 |
| Null preserved honestly | true |
| No threshold shopping | true |
| No relaxed materiality floor | true |
| No overlay built | true |

## Conclusion

The funding-conditioned candidate (C2) vs the RV-only baseline (B1) on observed
liquidation intensity yields a +0.1493% relative QLIKE difference (C2 slightly
worse than B1), fails the -2% materiality floor, and the bootstrap CI95
[-0.0123, 0.0217] includes zero. Holm-adjusted primary p=0.6365 vs alpha_2=0.00833.
Verdict: NOT_SUPPORTED. This is Track A (observed on-chain liquidations), NOT a
re-run of the modeled Track B breach proxy. No risk overlay is built
(RESEARCH_PROMPT.md section 9: forecast gate did not pass).
