# FCLR-XSEC-004 Protocol Freeze — Regime-Conditioned Cross-Sectional Funding Effect on Next-Hour Observed Liquidation Intensity

**Experiment ID:** FCLR-XSEC-004-20261120T230000Z
**Session UTC:** 20261120T230000Z
**Frozen at:** 2026-11-20T23:06:00Z (BEFORE any liquidation outcome was inspected)
**outcome_data_inspected_before_freeze:** `false`

---

## 1. Why this campaign (repository-name priority)

The repository is `Funding-conditioned-volatility-and-liquidation-risk`. Every prior SUPPORTED finding is **volatility-only** (FCLR-XSEC-002: regime-conditioned next-hour RV). The **liquidation-risk** half of the mandate has only been tested time-series-wise (FCLR-010/TBRACKA expansion panels, all NOT_MET/FRAGILE) and has **never** been tested as a regime-conditioned cross-sectional contrast on the combined metpie+ironflow observed-liquidation panel. That is the single heaviest, highest-value, still-open question matching the repo's dual mandate. It is a *distinct estimand* (liquidation intensity, not RV), uses a *materially different panel* (1.74M observed-liquidation events, 15 coins, 2025-03-22..2026-10-31), and is feasible with zero new data / no network / no credentials.

FCLR-XSEC-003 (thin RV-only holdout) is superseded: enqueuing it would leave the liquidation-risk half permanently avoided.

## 2. Frozen panel (hash-verified, do not re-derive)

- Path: `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet`
- sha256: `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`
- 1,740,415 rows x 13 cols; 15 coins (AAVE/ADA/AVAX/BNB/BTC/CRV/DOGE/ETH/LINK/LTC/NEAR/SOL/SUI/UNI/XRP); 10,052 hourly buckets; 2025-03-22 19:00 -> 2026-10-31 22:00 UTC; zero nulls in all features.
- Columns: `timestamp, coin, notional_usd, side, source, tx_hash, fundingRate, premium, abs_fund_pct, mark, ema_dist, rv24h, rv168h`.

The sha256 is asserted at the top of every script (`assert actual_sha == PANEL_SHA256`).

## 3. Estimand (defined ex ante)

- **Unit:** one eligible coin x one fully closed UTC hour.
- **Outcome (primary):** next-hour observed liquidation intensity per coin = sum of `notional_usd` over all observed liquidation events of that coin in the closed UTC hour t+1 (shift -1 within coin).
- **Outcome (secondary, robustness):** next-hour observed liquidation event count per coin.
- **Regime:** market-wide RV at hour t = cross-sectional mean of coin `rv24h` at t across coins present in hour t; split into high vs low tercile (middle tercile excluded); hours with fewer than 3 coins present excluded from regime eligibility.
- **Predictor:** within-(hour, regime) cross-sectional rank of `abs_fund_pct`; high_funding = top half of coins by rank, low_funding = bottom half within the same (hour, regime).
- **Baseline (specificity control):** within-regime RV persistence = coin's own `rv24h` at t split high/low within (hour, regime), predicting next-hour liquidation intensity.

Track separation is explicit: this is **observed liquidations (Track A)**, never conflated with modeled boundary breaches (Track B) or RV forecasts.

## 4. Inference (frozen pre-outcomes)

- Block bootstrap across whole UTC hours within each regime; seed `20261120`; >= 2000 deterministic replicates.
- Holm correction over the 4-test family (2 regimes x {funding contrast, RV persistence baseline}).
- 95% CIs; 2% materiality floor: `|mean_diff_high_minus_low| / mean_abs_outcome >= 0.02`, where `mean_abs_outcome` is the mean absolute next-hour liquidation intensity across the regime's coin-hours.
- Verdict = SUPPORTED only if a funding-contrast CI excludes zero AND Holm passes AND materiality clears; otherwise the honest null is preserved as NOT_SUPPORTED. No threshold-shopping; the floor is not relaxed after seeing outcomes.

## 5. Constraints honored

- No holdout outcomes inspected before this freeze (`outcome_data_inspected_before_freeze=false`).
- No re-run of FCLR-STARTER-001 / FCLR-XSEC-001 / FCLR-XSEC-002 / FCLR-XSEC-003.
- No overwrite of sealed `research_state/research_protocol.md`.
- No root-level `research_state/*.md` or `*.json` (root churn cap 499/500; all new artifacts go under `research_state/session_<UTC>/`).
- No network, no paid or credentialed data.
- No empty/placeholder files.

## 6. Acceptance (the gate)

`python3 scripts/check_handoff_heavywork_gate.py` exits 0 AND `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_125` -> 0 failures; no liquidation outcomes inspected before freeze; zero-byte placeholders do NOT count.