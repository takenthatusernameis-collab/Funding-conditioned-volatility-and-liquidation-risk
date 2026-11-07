# Pre-Registration: Gate 4 Funding-Conditioned Volatility Multi-Split Pilot

**experiment_id:** GATE4-FUNDING-MULTISPLIT-PILOT-20261107
**frozen_before_outcomes:** true
**frozen_at_utc:** 2026-11-07T01:36:11Z (pre-outcome; this file written before computing multi-split/CI results)
**git_sha_at_freeze:** recorded in run_manifest at execution time
**track:** C (volatility outcomes) — Binance-only local files; no Hyperliquid merge; Track A firewall unchanged.
**status_target:** PILOT/INCONCLUSIVE (claim-worthy criteria cannot be met with available data; see Data Sufficiency)

## Objective
Expand Gate 4 from a single split to a leakage-resistant multi-split evaluation of funding-conditioned volatility ablations (A..E) vs RV-only baseline (A), with block-aware uncertainty and pre-registered contrasts. Outcomes are pilot evidence only.

## Data (local, fixed)
- Symbols: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT (5 instruments criterion met by count? 4 instruments — **claim-worthy instrument count ≥5 NOT met**; honest shortfall recorded).
- Period: 2024-01-01 to 2024-03-31 (local extracted CSV/ZIP only). No re-probe, no paid/auth data.
- Frequency/alignment: 1h klines; funding 8h aligned via last-known value at/before each hour (ffill). Missing = NaN, never zero. No basis/premium added (no aligned series in this run).
- Horizon: 24h forward realized variance target.

## Splits (chronological, pre-registered)
Rolling walk-forward, train-only normalization, purge/embargo = 7 days (gap between train end and test start = 7 days). No random splits.

| Split | Train | Test |
|---|---|---|
| 0 | 2024-01-01T00:00:00Z .. 2024-01-28T23:59:59Z | 2024-02-05T00:00:00Z .. 2024-02-18T23:59:59Z |
| 1 | 2024-01-15T00:00:00Z .. 2024-02-11T23:59:59Z | 2024-02-19T00:00:00Z .. 2024-03-03T23:59:59Z |
| 2 | 2024-01-29T00:00:00Z .. 2024-02-25T23:59:59Z | 2024-03-04T00:00:00Z .. 2024-03-17T23:59:59Z |

Step = 14 days. Each test window = 14 days. Implementation computes masks via `src.eval.walkforward._in_window` and applies train-only normalization per split.

## Ablations (fixed)
- A_rv_only: rv_trail_24, rv_trail_168, rv_trail_6
- B_rv_signed: A + funding_signed
- C_rv_abs: A + funding_abs
- D_rv_signed_abs: A + funding_signed, funding_abs
- E_rv_funding_trails: D + funding_pct_{24,72,168}, funding_z_{24,72,168} (past-only rolling on aligned series)

Model: direct-variance OLS HAR per symbol (target = forward realized variance; train-only normalization; no log/exp transform; predictions floored at 0). Same form as validated Gate 3 baseline.

## Pre-registered Contrasts
Primary: **E vs A** (ΔQLIKE = QLIKE_E − QLIKE_A; negative = E better for QLIKE).
Secondary (descriptive, not claim-bearing alone): B vs A, C vs A, D vs A.

## Metrics
Primary: QLIKE (lower better). Secondary: MAE, RMSE. Report per-split and aggregate (mean across splits). Also report valid_n, neg_pred.

## Uncertainty (block-aware)
Paired QLIKE difference CI for primary contrast (E vs A) via **circular block bootstrap** resampling whole UTC time blocks **jointly across instruments** (all symbols for each sampled timestamp block retained), deterministic seed=12345, B=2000 replicates (or max feasible if sample smaller), block_size=24 hours, alpha=0.05, two-sided percentile CI. Applied to pooled test observations across the pre-registered splits' test windows (chronological, no leakage). If CI spans 0 or sample is insufficient, result remains PILOT/INCONCLUSIVE.

## Multiplicity
Primary family = 1 contrast (E vs A). Secondary contrasts (B/C/D vs A) reported descriptively with unadjusted point estimates; no confirmatory claim from secondaries. No Holm/Bonferroni adjustment required for a single primary contrast; if interpreted jointly, treat as exploratory.

## Data Sufficiency / Honest Verdict Rules
FCLR-001 claim-worthy requires ≥5 instruments, ≥3 non-overlapping 30-day blocks, valid uncertainty. **This pilot has 4 instruments and 14-day test windows (not 30-day blocks) within Q1 2024 only.** Therefore:
- Verdict is **PILOT/INCONCLUSIVE** regardless of point estimate direction.
- Do NOT promote to confirmatory; do NOT relax thresholds.
- Record exact shortfall: instruments=4 (<5), no 30-day non-overlapping test blocks met by design, Q1-2024-only local data.

## Leakage Controls
- Chronological splits only; purge/embargo 7d gap.
- Train-only normalization/statistics.
- Funding alignment last-known at/before hour; trailing funding past-only.
- Forward RV target uses future bars only for evaluation targets (not fit).
- No test leakage.
