# FCLR-VOL-CORR-01 Prereg (outcome-blind, frozen before outcomes)

**Experiment ID:** FCLR-VOL-CORR-01
**Campaign:** FCLR-VOL-CORR-01-20261124T180000Z
**Session:** session_20261124T204500Z
**Frozen before outcomes:** True
**Outcome data inspected before freeze:** False
**Source registry sha256:** `44993cfb700924ad01dad21b92f8830f1469fcda92cbd3d1159a9e651f2939ef`

## Question
On the full frozen ironflow_bulk panel (18 monthly parquet, 2025-05..2026-10), does the Shek (2026) funding-extreme correction pattern reconstruct: is the median/mean time for an extreme funding observation to correct back to its pre-extreme band LONGER in a high realized-volatility regime than in a low regime, and is the correction hazard LOWER when realized volatility is higher, clearing a frozen materiality floor with Holm-adjusted uncertainty?

## Design
- Kind: event_study_survival
- Event: funding extreme: |funding_rate| >= q_t where q_t is an EXPANDING, TRAIN-ONLY quantile of |funding_rate| per coin (no future information)
- Correction: first subsequent hour the funding rate returns inside the pre-extreme band (|funding_rate| < q_t) within a frozen maximum horizon; censored events recorded as censored, never as completed negatives
- Regime split: realized-volatility tercile (high vs low) from trailing 24h close-to-close log returns, train-only thresholds
- Walk-forward: train_frac=0.6, purge/embargo=48h, random_split=False
- Estimands: median correction time by regime, mean correction time by regime, correction hazard (survival) contrast high-RV vs low-RV
- Inference: cluster-robust (CR1) by coin, Driscoll-Kraay HAC, Holm step-down over the declared family; Holm over ['regime_contrast_median_correction_time', 'regime_contrast_correction_hazard']
- Materiality floor (relative): 0.1
- Verdict rule: symmetric: PROMOTED if materiality_met and direction slower; else NOT_SUPPORTED; INCONCLUSIVE if a regime median is undefined

## Paper claim (Shek 2026, SSRN 7529458)
Median correction 27h high-RV vs 3h low-RV; lower correction hazard with higher RV. Treated as a working-paper claim to reconstruct.
