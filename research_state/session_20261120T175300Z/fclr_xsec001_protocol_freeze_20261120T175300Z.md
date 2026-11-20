# FCLR-XSEC-001 frozen protocol — within-hour cross-sectional funding-intensity contrast

**Experiment ID:** FCLR-XSEC-001-20261120T175300Z
**Session UTC:** 20261120T175300Z
**Outcome data inspected before freeze:** false

## 1. Estimand and identification strategy

Within-hour cross-sectional funding-intensity contrast. For each closed UTC hourly timestamp t, rank the eligible perpetual contracts by signed funding rate observed at or before t. Compare next-hour realized variance (rv1h at t+1) of high-funding vs low-funding coins *within the same hour*. This isolates the funding effect from common market shocks (all coins share the same hour), avoiding the serial correlation and non-stationarity that plagued the time-series 24h forward RV forecast in FCLR-STARTER-001 (verdict NOT_SUPPORTED).

This is a distinct estimand from FCLR-STARTER-001 (time-series predictability of 24h RV). Per RESEARCH_PROMPT.md §16 (adaptive feasibility policy), a distinct-mechanism exploratory campaign on the same frozen panel is the designated next step after a NOT_SUPPORTED confirmatory verdict.

## 2. Unit, timing, and universe

- **Unit:** one eligible linear perpetual contract × one fully closed UTC hourly timestamp.
- **Forecast timestamp t:** immediately after all data for closed hour t are available. Every input available by that instant. Outcome begins with the next hourly interval (rv1h at t+1).
- **Panel:** frozen FCLR-001 panel at `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` (panel_sha256: 41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4). Hash-verified before target generation.
- **Universe:** 5 coins — BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT (the eligible sample of the frozen panel). No new data acquisition; no network; no paid/credentialed sources.
- **Coverage:** 2026-01-01 through 2026-08-31 (5,785 hourly timestamps; 23,558 coin-hour rows with a next-hour target).

## 3. Predictor (causal, computed at t)

- **signed_funding:** latest funding observation whose availability timestamp is no later than t, retaining sign.
- **Cross-sectional funding rank within hour:** for each UTC hour t, rank coins by signed_funding (descending, rank 1 = highest funding). Convert to percentile: rank / n_coins_in_hour.
- **Funding group:** coins with funding percentile <= 0.5 = "high_funding"; > 0.5 = "low_funding".
- Missing funding remains missing; no zero-fill or forward-fill.

## 4. Target

- **target_rv1h_t1:** next-hour realized variance (rv1h at t+1) for the same coin, computed from the frozen panel's rv1h column shifted by -1 within each coin. Rows where t+1 is beyond the panel's last timestamp are excluded.

## 5. Baseline

- **Within-hour RV persistence:** split coins within each hour by their own rv1h at t (percentile rank within hour, <= 0.5 = high_rv, > 0.5 = low_rv). Compare next-hour RV of high-rv vs low-rv coins within the same hour. Same paired structure as the funding contrast.

## 6. Evaluation

- **Within-hour paired comparison:** for each hour t with both high- and low-group coins, compute diff = mean(next-hour RV, high group) − mean(next-hour RV, low group).
- **Funding contrast:** diff computed on funding groups. Primary estimand.
- **RV persistence baseline:** diff computed on RV groups. Secondary reference.
- **Uncertainty:** block bootstrap across hours (resample whole UTC hours jointly across coins, preserving common shocks and serial dependence), seed 20261120, 2,000 deterministic replicates. 95% CI from percentile method.
- **Multiplicity:** Holm familywise-error correction across the family of 2 tests (funding contrast, RV persistence baseline).
- **Minimum claim-worthy:** ≥5 instruments, ≥3 non-overlapping evaluation blocks, CI supports direction, Holm passes. All satisfied by design (5 coins, 5,334+ hours, CI and Holm computed).

## 7. Gate

- Forecast gate passes only if: CI excludes zero in the improvement direction AND Holm-adjusted p < 0.05 AND ≥5 instruments AND ≥3 blocks.
- Otherwise verdict = NOT_SUPPORTED. Null result preserved; no threshold shopping.

## 8. Constraints

- No holdout outcomes inspected before protocol freeze. `outcome_data_inspected_before_freeze = false`.
- No modification of sealed legacy `research_state/research_protocol.md`.
- No network, no paid/credentialed data, no live/paper trading.
- All artifacts under `research_state/session_20261120T175300Z/`; no root-level md/json additions (root churn cap 499/500).
