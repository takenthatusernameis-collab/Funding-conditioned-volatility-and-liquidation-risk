# FCLR-LIQ-OOS-FORECAST-001 — Protocol Freeze (pre-outcomes)

**Campaign:** FCLR-LIQ-OOS-FORECAST-001-20261121T055825Z (rank-0, READY_EXECUTE/ACTIVE)
**Session UTC:** 20261121T055825Z
**Frozen:** 2026-11-21T05:58:25Z — BEFORE any outcome data is inspected.
**outcome_data_inspected_before_freeze:** false

## Repository-name priority
The repository is named *Funding-conditioned-volatility-and-liquidation-risk*. The cross-sectional (XSEC) program is terminal (FCLR-XSEC-001..008; XSEC-009 not triggered). The liquidation-risk half of the mandate has a supported cross-sectional association (FCLR-XSEC-004/005/006) but NO passing out-of-sample forecast gate. This campaign executes the heavy, leakage-resistant OOS forecast validation of funding-conditioned features for **observed** liquidation risk on the verified frozen combined liquidation panel.

## Estimand
Out-of-sample forecast of next-24h **observed** notional-weighted liquidation intensity (sum of notional_usd per coin per 24h bucket) on the combined liquidation panel (sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`, 15 coins, 2025-03-22 19:00 -> 2026-10-31 22:00 UTC, zero-null features). Contrast C2 (funding-conditioned) vs B1 (RV-only). Track separation: observed liquidations only — never Track B modeled boundary breaches, never RV forecasts.

## Models (causal features at day t, target = next-24h intensity at day t+1)
- **B1 (RV-only):** [log(rv24h)]
- **C2 (funding-conditioned):** [log(rv24h), fundingRate, abs_fund_pct, premium, ema_dist]

## Splits (chronological expanding walk-forward; no random split; no threshold-shopping; no holdout tuning)
- Train: 2025-03-22 -> 2025-12-31
- Validation: 2026-01-01 -> 2026-03-31 (diagnostic only; no tuning on validation)
- Test blocks: 2026-04-01..2026-05-31 ; 2026-06-01..2026-08-31 ; 2026-09-01..2026-10-31
- Purge: 1 day

## Binary event (for Brier / LogLoss)
event = 1 if next-24h observed intensity > train-period median intensity; median computed on train only, applied ex-ante to test; never tuned on test outcomes.

## Metric family (joint, lower is better)
- QLIKE: OLS of log(y) on features, yhat = exp(pred); qlike = y/yhat - log(y/yhat) - 1 (y>0, yhat>0)
- Brier: mean((p - e)^2), p = logistic-regression probability of the binary event
- LogLoss: -mean(e*log(p) + (1-e)*log(1-p))
Contrast: paired C2 - B1 per test observation; improvement if diff < 0.

## Inference
- Block bootstrap across the 3 chronological test blocks (resample blocks with replacement), 2000 reps, seed 20261121, 95% CI.
- Holm step-down correction over the joint 3-metric family (QLIKE, Brier, LogLoss), alpha 0.05.
- Materiality floor: relative reduction (mean_B1 - mean_C2)/mean_B1 >= 2.0% per metric.
- Per-metric gates: (1) CI entirely below zero (C2 strictly better), (2) Holm adj_p < 0.05, (3) materiality >= 2%.

## Verdict rule
SUPPORTED only if ALL three metrics clear every gate. Otherwise honest NOT_SUPPORTED. No threshold-shopping or floor relaxation after seeing outcomes.

## Independent recompute
Separate numpy/stdlib-only code path (`fclr_liq_oos001_recompute_20261121T055825Z.py`) reproducing the OOS evaluation; verdict is not a single-implementation artifact.

## Cross-references
FCLR-XSEC-002 (funding->RV HIGH-RV SUPPORTED; OOS forward confirmations all failed), FCLR-XSEC-004/005/006 (funding->liq intensity SUPPORTED cross-sectionally), FCLR-XSEC-007/008 (NOT_SUPPORTED; XSEC terminal), FCLR-LIQ-COMBINED-PANEL (NOT_MET), Track B modeled breaches (NOT_MET), Track A combined panel (NOT_MET).

## Constraints
All artifacts under `research_state/session_20261121T055825Z/`; no root-level md/json (root at 499/500 cap); no `.github/workflows` edits; no sealed mutation; no `research_state/research_protocol.md` overwrite; no empty/placeholder or zero-byte artifacts; both frozen panel sha256 asserted in script headers before computation; no network/paid data/credentials.
