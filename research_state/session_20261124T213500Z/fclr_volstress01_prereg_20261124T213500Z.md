# FCLR-VOL-STRESS-01 Preregistration (outcome-blind, frozen before outcomes)

**Experiment:** FCLR-VOL-STRESS-01
**Campaign:** FCLR-VOL-STRESS-01-20261124T213000Z
**Session:** session_20261124T213500Z (UTC 2026-11-24T21:35:00Z)
**Source registry sha256:** 01ea3208fca6e3aeaea91dfd8be4fc534db172acb552878817ebf71bf13df191

## Primary question

On the full frozen ironflow_bulk panel (18 monthly parquet, 2025-05..2026-10; 466 coins with candles_1h + funding + open_interest), does the funding + price-dislocation feature set improve out-of-sample forecasts of a realized-volatility STRESS event - next-24h realized variance exceeding an expanding, train-only high quantile per coin - beyond a realized-volatility-only baseline, judged on Brier / log-loss / calibration with a frozen materiality floor and Holm-adjusted uncertainty?

This addresses RESEARCH_PROMPT.md section 3.1 ("future realized volatility or volatility stress"), target 1: the volatility-stress sub-target. It is a DISTINCT outcome family (tail-exceedance classification) from the closed mean-QLIKE arm (FCLR-VOL-BROAD-01) and the closed correction-time arm (FCLR-VOL-CORR-01); it is not a re-run of a terminal endpoint.

## Design (frozen before any outcome was inspected)

- **Kind:** walk_forward_classification_stress (forecast / classification / stress / tail / exceedance / walk_forward).
- **Universe:** all coins present in candles_1h, funding, and open_interest (466 coins) on the frozen ironflow_bulk panel.
- **Forecast origin t:** immediately after all data for closed hour t are available; every input available by t; outcomes begin at t+1.
- **Trailing 24h realized variance (RV24h):** sum of squared hourly mark-price log returns over the trailing 24 complete hourly intervals ending at t, per coin.
- **Forward 24h realized variance:** sum of squared hourly mark-price log returns over the next 24 complete hourly intervals (t+1..t+24), per coin.
- **Stress event label at t:** forward_24h_RV > q_{c,t}, where q_{c,t} is an expanding, TRAIN-ONLY 0.90 quantile of the coin's own trailing-24h-RV observed strictly before t (no future information; thresholds computed only from prior observations).
- **Baseline (RV-only):** logistic regression of the stress label on trailing realized-variance features (RV24h, RV168h, lagged RV), persistence/HAR-style.
- **Candidate:** same logistic form and fitting procedure as baseline, plus signed funding rate, absolute funding rate, mark/index premium, and mark/EMA24 distance.
- **Feature standardization:** train-only means/stds; zero-variance columns dropped; missing features remain missing (no zero-fill / forward-fill).
- **Walk-forward:** chronological expanding train-only thresholds; train_frac=0.6; PURGE_EMBARGO_H=48 (>= max 24h forward horizon); no random split; no overlapping forward targets across the purge boundary.
- **Holdout:** chronological final holdout opened once, after the prereg is frozen; never re-tuned.

## Inference and multiplicity

- Cluster-robust (CR1) by coin; Driscoll-Kraay HAC; Holm step-down over the declared family {baseline_vs_candidate_brier, baseline_vs_candidate_log_loss}.
- Report raw and adjusted results and the whole tested family.

## Materiality floor (frozen, NOT relaxed)

- materiality_floor_rel = 0.02 (2% relative).
- The candidate's relative Brier (or log-loss) improvement over the RV-only baseline must exceed 2% relative.
- Verdict rule: symmetric - PROMOTED if materiality_met and direction improves; else NOT_SUPPORTED; INCONCLUSIVE if a holdout cannot be formed. A null (NOT_SUPPORTED) is a valid, publishable negative result that closes the volatility-stress arm.

## Do NOT

- Re-run FCLR-VOL-BROAD-01 (closed NOT_SUPPORTED) or FCLR-VOL-CORR-01 (closed NOT_SUPPORTED).
- Build a risk overlay (section 9 forecast gate not passed).
- Threshold-shop or relax the frozen floor after outcomes.
- Relabel exploratory as confirmatory.
- Wait for NEW_OBSERVED_LIQUIDATION_SOURCE (cannot fire on frozen data).

## Frozen inputs (read-only, sha256-asserted)

- candles_1h: research_state/data_cache/ironflow_bulk/candles_1h/
- funding: research_state/data_cache/ironflow_bulk/funding/
- open_interest: research_state/data_cache/ironflow_bulk/open_interest/

All artifacts for this campaign live under research_state/session_20261124T213500Z/; none are written at research_state root (root md+json cap 500/500).
