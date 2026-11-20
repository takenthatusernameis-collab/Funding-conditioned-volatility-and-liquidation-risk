# FCLR-XSEC-002 frozen protocol — UTC-hour / market-wide-RV conditioning of the funding effect

**Experiment ID:** FCLR-XSEC-002-20261120T210000Z
**Session UTC:** 20261120T210000Z
**Outcome data inspected before freeze:** false

## 1. Estimand and identification strategy

UTC-hour / market-wide-RV conditioning of the within-hour cross-sectional funding effect. For each closed UTC hourly timestamp t, compute the market-wide realized variance at t as the cross-sectional mean of coin rv1h at t across the 5 eligible coins. Split hours into high vs low market-wide-RV tercile (primary). Within each regime, within each hour, rank coins by within-hour cross-sectional funding abs_funding_pct_trail and split into high- vs low-funding. Compare next-hour realized variance (rv1h at t+1) of high-funding vs low-funding coins *within the same hour and regime*. This is a regime-masked identification: a funding effect present only in high-RV hours would surface here even though the pooled time-series (FCLR-STARTER-001, NOT_SUPPORTED) and pooled cross-sectional (FCLR-XSEC-001, NOT_SUPPORTED) tests were null.

This is a distinct estimand from FCLR-STARTER-001 (time-series 24h forward RV forecast) and FCLR-XSEC-001 (pooled within-hour cross-sectional funding contrast). Per RESEARCH_PROMPT.md §16 contingency ladder mechanism 1, this distinct-regime exploratory campaign on the same frozen panel is the designated next step after NOT_SUPPORTED verdicts on both prior campaigns.

## 2. Unit, timing, and universe

- **Unit:** one eligible linear perpetual contract × one fully closed UTC hourly timestamp.
- **Forecast timestamp t:** immediately after all data for closed hour t are available. Every input available by that instant. Outcome begins with the next hourly interval (rv1h at t+1).
- **Panel:** frozen FCLR-001 panel at `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` (panel_sha256: 41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4). Hash-verified before target generation.
- **Universe:** 5 coins — BNBUSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT (the eligible sample of the frozen panel). No new data acquisition; no network; no paid/credentialed sources.
- **Coverage:** 2026-01-01 through 2026-08-31 (5,832 distinct hourly timestamps; 29,136 coin-hour rows).

## 3. Regime variable (computed at t, causal)

- **Market-wide RV at hour t:** cross-sectional mean of coin rv1h at t across the 5 coins (only coins with non-null rv1h at t contribute; require >= 3 coins with valid rv1h for the hour to be regime-eligible).
- **Primary regime split:** hours split into high vs low tercile by market-wide RV at t (top tercile = high-RV regime, bottom tercile = low-RV regime; middle tercile excluded from primary contrast).
- **Registered robustness cuts:** (a) high/low median split of market-wide RV; (b) Asian/European/US UTC-session buckets (UTC hours 0–7 / 8–15 / 16–23).

## 4. Predictor (causal, computed at t)

- **abs_funding_pct_trail:** past-only trailing absolute-funding percentile. Require abs_funding_trail_n >= 30 valid historical funding observations to emit (per FCLR-001 §14). Missing funding remains missing; no zero-fill or forward-fill.
- **Cross-sectional funding rank within (hour, regime):** for each UTC hour t within a regime, rank coins by abs_funding_pct_trail (descending, rank 1 = highest trailing abs funding). Convert to percentile: rank / n_coins_in_hour_regime.
- **Funding group:** coins with funding percentile <= 0.5 = "high_funding"; > 0.5 = "low_funding".
- **Signed secondary:** signed_funding used as a secondary signed contrast (high vs low signed funding within (hour, regime)).
- A (hour, regime) cell contributes to a contrast only if it contains >= 1 coin in each funding group with a non-null next-hour target.

## 5. Target

- **target_rv1h_t1:** next-hour realized variance (rv1h at t+1) for the same coin, computed from the frozen panel's rv1h column shifted by -1 within each coin. Rows where t+1 is beyond the panel's last timestamp have a null target and are excluded from that hour's contrast.

## 6. Baseline (within-regime RV persistence)

- **Within-regime RV persistence:** within each market-wide-RV regime, split coins within each hour by their own rv1h at t (percentile rank within hour within regime, <= 0.5 = high_rv, > 0.5 = low_rv). Compare next-hour RV of high-rv vs low-rv coins within the same hour and regime. Same paired structure as the funding contrast, computed per regime.
- A (hour, regime) cell contributes to the baseline contrast only if it contains >= 1 coin in each RV group with a non-null next-hour target.

## 7. Evaluation

- **Within-regime paired comparison:** for each hour t in a regime with both groups present, compute diff = mean(next-hour RV, high group) − mean(next-hour RV, low group). Collect hourly diffs per regime per contrast.
- **Primary family:** regimes × {funding contrast, RV persistence baseline} = 2 regimes × 2 contrasts = 4 tests (high-RV funding, high-RV persistence, low-RV funding, low-RV persistence).
- **Uncertainty:** block bootstrap across whole UTC hours within each regime (resample whole hours jointly across coins, preserving common shocks and serial dependence), seed 20261120, >= 2,000 deterministic replicates. 95% CI from percentile method.
- **Multiplicity:** Holm familywise-error correction across the full family of 4 tests.
- **Materiality floor:** pre-registered 2% practical materiality floor on relative effect; not relaxed after seeing outcomes.
- **Minimum claim-worthy:** CI excludes zero in the improvement direction AND Holm-adjusted p < 0.05 AND effect clears materiality floor AND >= 5 instruments represented AND adequate hours per regime.
- Otherwise verdict = NOT_SUPPORTED. Null result preserved; no threshold shopping.

## 8. Gate

- Forecast gate passes only if: for at least one test in the family, CI excludes zero AND Holm-adjusted p < 0.05 AND the effect clears the 2% materiality floor.
- Otherwise verdict = NOT_SUPPORTED. Null result preserved; no threshold shopping.

## 9. Constraints

- No holdout outcomes inspected before protocol freeze. `outcome_data_inspected_before_freeze = false`.
- No modification of sealed legacy `research_state/research_protocol.md`.
- No network, no paid/credentialed data, no live/paper trading.
- All artifacts under `research_state/session_20261120T210000Z/`; no root-level md/json additions (root churn cap 499/500).
- Do NOT re-run FCLR-STARTER-001 or FCLR-XSEC-001 (both terminal NOT_SUPPORTED).
