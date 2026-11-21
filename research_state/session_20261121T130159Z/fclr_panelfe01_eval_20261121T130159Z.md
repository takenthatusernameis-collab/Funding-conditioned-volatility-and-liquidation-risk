# FCLR-PANEL-FE-001 — Panel Fixed-Effects Evaluation (Walk-Forward OOS)

**Experiment ID:** FCLR-PANEL-FE-001-20261121T130159Z
**Session:** session_20261121T130159Z
**Generated (UTC):** 2026-11-21T13:01:59Z
**Prereg freeze:** session_20261121T130159Z (outcome-blind, `outcome_data_inspected_before_freeze=false`)
**Overall verdict:** NOT_SUPPORTED (a null on either half is recorded as NOT_SUPPORTED; the 2% materiality floor is frozen and was not relaxed after outcomes).

## Repository-name priority

The repository is named *Funding-conditioned-volatility-and-liquidation-risk* — two scientific halves reconciled by funding conditioning:

- **Half (a):** does the funding rate **condition realized volatility (RV)**?
- **Half (b):** does it **condition liquidation risk/intensity**?

Prior campaigns answered these with pooled cross-sectional regime contrasts (FCLR-XSEC-001..008, terminal) or a 3-block time-series confirmation (exhausted: `next_campaign_status.py` → NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN). This campaign uses a **materially different, feasible design**: two-way (coin + hour) fixed-effects panel regression on the full frozen panels, exploiting within-coin, within-hour variation. It does **not** require the 3 mutually non-overlapping ≥127-day contiguous blocks.

## Frozen inputs (sha256 asserted in script header before any read)

| Panel | Path | sha256 | Rows | Coins | Span |
|---|---|---|---|---|---|
| FCLR-001 (primary) | `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` | `41962f82…c1f4` | 29,136 | 5 | 2026-01-01 → 2026-08-31 |
| Combined liquidation (Track A observed) | `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` | `81a100d5…7f14` | 1,740,415 | 15 | 2025-03-22 → 2026-10-31 |

Critical data notes:
- `premium` is **100% null** (`NOT_COMPUTABLE_WITHOUT_INDEX_PRICE`) — never used.
- `funding_asof_lag_h` is **hours-since-last-funding**, NOT a funding rate. The signed funding rate is `signed_funding`.
- Frozen split boundaries with 7-day embargo: train `01-01→03-17`, validation `03-25→04-30`, test `05-08→08-06` (Half A).
- Half B hourly grid: zero-event hours are explicit zeros (`has_event=False`); funding ffill only, never outcome ffill, flagged `funding_is_ffill=True`.

## Models estimated (two-way FE: coin FE + hour-of-day FE, within transform)

**Half A — volatility (FCLR-001):**
- A1 (PRIMARY): `next_log_rv1h ~ signed_funding`
- A2 (robustness): `log_target_rv24h ~ signed_funding`
- A3 (robustness): `next_log_rv1h ~ abs_funding_pct_trail`

**Half B — liquidation intensity (combined panel):**
- B1 (PRIMARY): `log1p(liq_count) ~ funding_rate_mean`
- B2 (PRIMARY): `log1p(liq_notional) ~ funding_rate_mean`
- B3 (robustness): `log1p(liq_count) ~ abs_fund_pct_mean`

## Inference (all three SE reported per coefficient)

1. Cluster-robust (CR1) by coin — reported; G=5 caveat noted (small number of clusters).
2. Driscoll-Kraay HAC (Bartlett kernel) on `h_t = Σ_i x_it e_it`, lag `L = floor(4*(T/100)^(2/9))`.
3. Newey-West HAC on the stacked within-transformed series (same lag rule).

Holm familywise correction across primary contrasts within each half; raw and Holm-adjusted p-values both reported.

## Walk-forward out-of-sample evaluation

Strictly chronological expanding-window one-step-ahead; re-fit at each daily 00:00 UTC origin using only data ≤ origin; forecast the following 24 hours. No random train/test split; frozen split boundaries respected as minimum; 7-day embargo.

- **Half A:** funding-conditioned FE vs no-funding FE baseline on `rv1h` level; QLIKE; Diebold-Mariano (HAC) on daily-mean QLIKE loss differential.
- **Half B:** funding-conditioned FE vs no-funding FE baseline on hourly notional intensity; QLIKE (+ Poisson deviance robustness); Diebold-Mariano.

## Materiality floor (frozen, NOT relaxed)

Implied change from a +1 sample-SD funding shock must be ≥ 2% relative (|β × SD(x)| ≥ 0.02). A null is recorded as NOT_SUPPORTED. No threshold shopping.

## Key results (see `fclr_panelfe01_eval_20261121T130159Z.json` for full statistics)

**Half A (volatility):** coefficient estimates on `signed_funding` not statistically distinguishable from zero under HAC SE; implied 1-SD effect below the 2% materiality floor; walk-forward QLIKE relative reduction not positive; DM test does not reject equal accuracy. Verdict: **NOT_SUPPORTED** for H_panelfe_vol.

**Half B (liquidation):** coefficient on `funding_rate_mean` statistically non-zero under HAC SE but implied 1-SD effect below the 2% materiality floor; Holm-adjusted p does not pass; walk-forward QLIKE relative reduction negative (-2.96%); DM p = 0.71 (equal accuracy not rejected). Verdict: **NOT_SUPPORTED** for H_panelfe_liq.

**Overall:** NOT_SUPPORTED. The funding rate does not condition RV or liquidation intensity with ≥2% materiality on the frozen panels under this two-way FE + walk-forward design.

## Hard constraints honored

- `outcome_data_inspected_before_freeze=false` (prereg frozen before any outcome statistic).
- Both frozen panel sha256 asserted in the eval script header before any read.
- `premium` never used (all-null).
- `funding_asof_lag_h` never used as a rate.
- No random train/test split; strictly chronological walk-forward.
- Materiality floor 0.02 frozen and not relaxed after outcomes.
- Observed liquidations (Track A) kept distinct from modeled boundary breaches (Track B).
- No sealed protocol overwritten; no root-level md/json added; no `.github/workflows` modified; no network or paid data used.

## Artifacts

- `fclr_panelfe01_eval_20261121T130159Z.py` — panel-FE estimation + walk-forward evaluation source
- `fclr_panelfe01_eval_20261121T130159Z.json` — evaluation results (machine-readable)
- `fclr_panelfe01_eval_20261121T130159Z.md` — this document
- `fclr_panelfe01_recompute_20261121T130159Z.py` — independent stdlib/numpy recompute
- `fclr_panelfe01_recompute_20261121T130159Z.json` — recompute results
- `fclr_panelfe01_evidence_audit_20261121T130159Z.json` — evidence audit
- `fclr_panelfe01_evidence_audit_20261121T130159Z.md` — evidence audit (markdown)
- `evidence_audit_20261121T130159Z.json` — gate-required evidence audit (literal `evidence_audit_` prefix)
- `trigger_check_20261121T130159Z.json` — non-empty trigger check (no external trigger required)
