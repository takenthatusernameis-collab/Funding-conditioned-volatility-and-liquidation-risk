# FCLR-XSEC-002 Preregistered Protocol Freeze

**Experiment:** FCLR-XSEC-002-20261120T205500Z
**Session:** session_20261120T205500Z
**Source:** RESEARCH_PROMPT.md section 16 contingency ladder, mechanism 1 (UTC-hour / market-wide-RV conditioning of the funding effect)
**Frozen at:** 2026-11-20T20:55:00Z
**outcome_data_inspected_before_freeze:** false

## 1. Estimand (distinct from FCLR-001 and FCLR-XSEC-001)

FCLR-XSEC-002 conditions the within-hour cross-sectional funding contrast on the
**market-wide realized-variance regime** at hour `t`. It asks: does within-hour
funding-intensity rank predict next-hour realized variance *within each market-wide
RV regime*, after controlling for within-regime RV persistence?

This is a distinct estimand from:
- FCLR-STARTER-001 (time-series 24h forward-RV forecast; verdict NOT_SUPPORTED).
- FCLR-XSEC-001 (pooled within-hour cross-sectional funding contrast, no regime
  conditioning; verdict NOT_SUPPORTED).

A regime-masked effect (funding mattering only in high-RV hours/sessions) would surface
here even though the pooled time-series and pooled cross-sectional tests were null.

## 2. Unit, Timing, Universe

- **Unit:** one eligible linear perpetual contract × one fully closed UTC hour `t`.
- **Timing:** every input available at `t`; outcomes begin at `t+1`.
- **Universe:** the frozen FCLR-001 panel
  `research_state/fclr011_recompute_panel_20261115T234700Z.parquet`, sha256
  `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`.
  5 coins: BNBUSSDT, BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT. No new data, no network,
  no credentials.

## 3. Target

Next-hour realized variance = `rv1h.shift(-1)` within each coin
(`target_rv1h_t1`). Rows with a null target are excluded from that hour's contrast
(the baseline uses only non-null targets).

## 4. Regime Variable

Market-wide RV at hour `t` = cross-sectional mean of `rv1h` across the 5 coins at `t`.

**Primary split:** high vs low tercile of the market-wide RV distribution.
**Registered robustness cuts:**
- Secondary: Asian / European / US UTC-session bucketing (UTC hours 0–7 / 8–15 /
  16–23).
- Secondary: high / low median split of market-wide RV.

## 5. Predictor

Within-hour cross-sectional funding rank. Primary: `abs_funding_pct_trail`
(past-only trailing absolute-funding percentile; `abs_funding_trail_n` gives the
observation count — require `abs_funding_trail_n >= 30` as in FCLR-001 §14).
Secondary signed contrast: `signed_funding`.

Within each hour **and within each regime**, split coins into high- vs low-funding by
within-(hour, regime) rank and form the paired next-hour RV contrast
(high minus low), exactly mirroring the FCLR-XSEC-001 paired-hourly-difference
structure.

## 6. Baseline

Within-regime RV persistence: within each regime, split coins by their own `rv1h` at
`t` (high vs low) and form the paired next-hour RV contrast. This is the same
persistence baseline FCLR-XSEC-001 implements, now computed per regime.

## 7. Evaluation

- Within each regime: paired comparison, block bootstrap across whole UTC hours
  within that regime (≥ 2,000 deterministic-seed reps, seed 20261120), 95% CIs.
- Holm correction over the full family (regimes × {funding contrast, persistence
  baseline}).
- Materiality floor: 2% relative improvement in mean absolute deviation of the
  contrast (mirrors the FCLR-001 materiality convention; a null is preserved as
  NOT_SUPPORTED).
- Verdict = NOT_SUPPORTED unless a funding-contrast CI excludes zero AND Holm passes
  AND the effect clears the practical floor; otherwise report the honest null.

## 8. Constraints

- No holdout outcomes inspected before this freeze.
- No sealed legacy `research_state/research_protocol.md` modified.
- No `.github/workflows` modified.
- No root-level `research_state/*.md` or `research_state/*.json` files added
  (root churn cap 500; all artifacts go under `research_state/session_<UTC>/`).
- No network, no paid/credentialed data.
- No threshold-shopping or relaxation of the 2% materiality floor after seeing
  outcomes.