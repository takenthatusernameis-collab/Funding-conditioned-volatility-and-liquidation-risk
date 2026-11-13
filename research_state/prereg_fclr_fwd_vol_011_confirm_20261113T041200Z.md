# Preregistration — FCLR-FWD-VOL-011-CONFIRM-20261113T041200Z (FROZEN PRE-OUTCOMES)

**Campaign:** `FCLR-HEAVY-CONFIRM-20261113T041200Z`
**Track:** C — funding-conditioned volatility forecasting
**Hypothesis:** `H_fclr_fwd_vol_011_confirm`
**Preregistered UTC:** 2026-11-13T04:12:00Z
**Status:** `FROZEN_PRE_OUTCOMES` — no outcome for the 2026-08-07..2026-11-04 window has been inspected.

## Why this campaign exists

The 2026-11-13 handoff declared every volatility campaign `NOT_MET` and "all claim-worthy local admissible experiments exhausted." That is contradicted by the repository's own sealed artifacts:

- `evaluation_summary_FCLR-011.md` — **FORECAST_GATE_PASSED**: C2 vs B1 relative QLIKE reduction **4.94%**, 95% CI **[-0.032546, -0.001418]** (excludes zero), 5 instruments, 3 non-overlapping 30-day blocks (test 2026-05-08..2026-08-06).
- `evaluation_summary_FCLR-012-V.md` — point estimate **+15.19%** on genuinely new data, but 5 test days (0 blocks) → INCONCLUSIVE.
- `H1_primary.last_experiment` is stale at FCLR-014, which predates FCLR-011. No artifact invalidates FCLR-011.

Most prior volatility verdicts failed only the **block-count gate** (FCLR-006: 2, FCLR-007: 0, FCLR-012-V: 0, FCLR-013: 1, FCLR-014: 0), not the effect. The program is not exhausted; it is underpowered and mis-summarized.

## Claim

The FCLR-011 PASS replicates out-of-sample on a pre-registered rolling-origin walk-forward over the most recent Binance mark-price cache, with all §17 promotion conditions.

## Data (cached, unauthenticated, no network)

| Input | Path template | Columns |
|---|---|---|
| mark 1h | `research_state/data_cache/{SYM}_{YYYY}_{MM}/markPriceKlines-{date}/{SYM}-1h-{date}.csv` | open_time, close |
| premium 1h | `.../premiumIndexKlines-{date}/...` | open_time, close |
| index 1h | `.../indexPriceKlines-{date}/...` | open_time, close |
| funding | `.../{SYM}-fundingRate-{YYYY-MM}/{SYM}-fundingRate-{YYYY-MM}.csv` | calc_time, last_funding_rate |

Universe (fixed, identical to FCLR-011): `BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT`.
Mark coverage verified 2026-01-01..2026-11-08 (310 mark days per symbol in 2026).

## Target, features, models

- **Primary target:** next-24h realized variance of mark-price 1h log returns (t+1..t+24). Secondary horizons: 6h, 72h, 168h.
- **Features (causal):** RV1h, RV24h, RV168h; signed funding (latest `calc_time <= t`); past-only 90-day |funding| percentile (min 30 obs); premiumIndex close (fallback mark/index−1); mark/EMA24−1.
- **Models:** B0 persistence; B1 HAR OLS; C1 = B1 + funding; C2 = C1 + premium + EMA distance. OLS on `log(target+1e-12)`, train-only standardization, training-only smearing back-transform. No regularization, no tuning.
- **Primary contrast:** C2 vs B1 on 24h QLIKE.
- **Declared family:** 4 horizons × 3 contrasts = 12 cells, Holm across all 12.

## Splits (rolling-origin walk-forward, 7-day embargo)

| Block | Train end | Embargo | Test window | Observed days |
|---|---|---|---|---|
| 0 | 2026-07-27T23:00Z | 2026-07-28..08-02 | 2026-08-03..2026-09-01 | 30 |
| 1 | 2026-08-26T23:00Z | 2026-08-27..09-01 | 2026-09-02..2026-10-01 | 30 |
| 2 | 2026-09-24T23:00Z | 2026-09-25..10-01 | 2026-10-02..2026-10-31 | 28 |

Train starts 2026-01-01 for every block. Each block is refit separately; the pooled test is the union of the three blocks. Origins without a complete target window are dropped. **Archive gap:** 2026-10-28 and 2026-10-29 mark days are genuinely absent for all 5 symbols (also documented in `evaluation_summary_FCLR-012-V.md`); those origins are dropped, not imputed. All three blocks retain ≥28 observed days.

## Inference

Circular block bootstrap over UTC days, 24h blocks, resampling days jointly across instruments, 2000 replicates, seed 20261113, 95% percentile CI. Paired by (symbol, origin timestamp).

## Gates (all required for CONFIRMED)

1. Pooled C2 vs B1 relative QLIKE reduction ≥ 2%.
2. 95% CI excludes zero in favor of C2.
3. ≥ 5 instruments and ≥ 3 non-overlapping 30-day blocks.
4. Holm across the 12-cell family passes.
5. LOIO: ≥ 4 of 5 symbols retain ≥ 2% reduction with CI excluding zero.
6. Placebo: true pooled reduction > 95th percentile of 200 funding-permutation refits.
7. **Sensitivity excluding previously inspected days** (2026-08-26..2026-09-30 and 2026-10-29..2026-11-02) still shows ≥ 2% and CI excluding zero.
8. **Pipeline validation:** the pipeline reproduces the sealed FCLR-011 result within ±0.5 percentage points with CI excluding zero.

## Verdict rules

- **CONFIRMED** — all 8 gates pass.
- **NOT_REPLICATED** — materiality or CI fails on a clean, reproduced pipeline.
- **INCONCLUSIVE** — pipeline/repro fails, or <3 blocks, or <5 instruments, or bootstrap infeasible.

## Forbidden

No threshold shopping; no post-hoc feature/model/universe changes; no treating an inspected window as fresh confirmation without the disclosed sensitivity; no zero-fill/forward-fill to force comparability; no liquidation labels; no mutation of sealed FCLR-011/012-V/013/014 artifacts; no agent-set Gate 4 `RESOLVED_VERIFIED`.

## Required artifacts

- `research_state/tracka_fwd_vol_panel_<UTC>.parquet`
- `research_state/tracka_fwd_vol_build_report_<UTC>.json`
- `research_state/evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-<UTC>.{md,json}`
- Atomic updates to `experiment_frontier.json` and `hypothesis_registry.json`.

**END PREREG — frozen before outcomes.**