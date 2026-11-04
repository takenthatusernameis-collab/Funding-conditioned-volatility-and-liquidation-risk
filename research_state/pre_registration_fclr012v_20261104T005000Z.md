# Pre-Registration: FCLR-012-V (FORWARD VOLATILITY — UNSEALED 2026 PANEL)

Version: 1.0
Timestamp: 2026-11-04T00:50:00Z
Status: PRE-REGISTERED BEFORE OUTCOMES
Experiment ID: FCLR-012-V
Hypothesis: FCLR-H001 (incremental 24-hour volatility forecasting)
Track: C (funding-conditioned volatility — repo-name priority)

## 1) Why this experiment (blocker removal)
FCLR-012-V data was downloaded (scripts/fclr012_download.py) and coverage-audited
(research_state/fclr012v_coverage_audit.json, 2026-11-03T20:30Z) but the forward
validation was NEVER executed: run_evaluation.py had no experiment branch for it and
no pre-registration existed, so the campaign stalled on an engineering gap rather than
a data gap. This prereg closes that gap. Data is already on disk; no new download,
no outcome inspection has occurred.

## 2) Data (already cached, audited, unsealed)
- Window: 2026-08-07T00:00:00Z .. 2026-11-02T23:00:00Z (88 common days)
- Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (5)
- Sources: Binance UM perp markPriceKlines / indexPriceKlines / premiumIndexKlines /
  monthly fundingRate (data.binance.vision, unauthenticated)
- Coverage audit: research_state/fclr012v_coverage_audit.json
- Verified gaps (NOT repaired): 2026-10-28 and 2026-10-29 missing for all 5 symbols
  (probed live 2026-11-04T00:45Z -> HTTP 404; archive genuinely ends 2026-11-02).
  Missing days stay missing; no imputation.

## 3) Design (frozen BEFORE any outcome computation)
- Models: B0 persistence, B1 RV-HAR, C1 funding-augmented, C2 combined (fixed OLS
  log-linear, NO regularization, NO hyperparameter search — identical form to FCLR-001)
- Target: log(RV + 1e-12) of next-24h realized variance of mark-price returns (HORIZON=24)
- Features (causal, available by forecast timestamp t): RV1h/RV24h/RV168h trailing
  realized variances; signed funding (latest <= t); abs funding percentile (trailing
  90-calendar-day, >=30 prior obs required); mark/index premium (frozen alignment
  tolerance); mark/EMA24 distance (EMA from fully closed prior bars only).
- Primary contrast: C2 vs B1 on 24h out-of-sample QLIKE
- Minimum relative improvement floor: >=2% relative QLIKE reduction (frozen)
- Multiplicity: Holm correction across registered family (C2_vs_B1, C1_vs_B1, C2_vs_C1)
- Inference: block bootstrap, ~24h blocks, 2000 deterministic-seed replicates
- Minimums: >=5 instruments, >=3 non-overlapping 30-day blocks

## 4) Splits (frozen BEFORE outcomes — chosen from coverage only)
- Train: 2026-08-07T00:00:00Z .. 2026-09-16T23:00:00Z (41 days)
- Validation: 2026-09-24T00:00:00Z .. 2026-10-21T23:00:00Z (28 days)
- Test: 2026-10-29T00:00:00Z .. 2026-11-02T23:00:00Z (5 days)
- 7-day purge/embargo at all boundaries (>= max secondary horizon 168h)
- Boundary basis: unique UTC timestamps; chronological; no random split.
- NOTE: test window is 5 days = 0 non-overlapping 30-day blocks. The >=3 block
  criterion is NOT MET by construction. This is recorded BEFORE outcome inspection
  so it cannot be relaxed afterwards. Result: if executed, the honest verdict is
  PILOT / INCONCLUSIVE on the block-count criterion regardless of QLIKE point estimate.

## 5) Gates
- Gate MET only if: C2 vs B1 >=2% relative QLIKE reduction AND 95% CI excludes zero
  on improving side AND >=5 instruments AND >=3 non-overlapping 30-day blocks.
- Given §4, the block criterion fails a priori -> gate CANNOT pass. Expected verdict:
  INCONCLUSIVE / PILOT. Preserve the null; do NOT promote.

## 6) Constraints
- Pre-register BEFORE any outcome inspection (this file IS the pre-registration)
- Leakage-resistant: forecast timestamp t uses only data available <= t; trailing-only
  features; training-only standardization; no same-bar/future data in predictors
- Purge/embargo >=7 days at all split boundaries
- No re-tuning on test; no threshold shopping; no reuse of sealed holdouts
  (FCLR-001/002/003/006/007/008/011 remain sealed and untouched)
- Cross-track firewall: Binance Track C never merged with Hyperliquid Track A
- No risk overlay; hypothetical only; no live/paper trading