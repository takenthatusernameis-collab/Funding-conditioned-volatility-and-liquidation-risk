# Pipeline correction — TRACKA-HL-EARLY4H-2025H1

**UTC:** 2026-11-12T14:56:44Z
**Frozen prereg (unchanged):** `research_state/tracka_prereg_early2025h1_20261112T134503Z.json`
**Prereg SHA-256 (unchanged):** `fdd96bd116460ffd5698995dc6245f8937d58b2e078430640c2be7baef878e7b`
**Supersedes eval:** `research_state/evaluation_summary_EARLY4H-2025H1-20261112T134634Z.{md,json}` (degenerate/invalid)
**Corrected eval:** `research_state/evaluation_summary_EARLY4H-2025H1-20261112T145537Z.{md,json}`
**Corrected panel:** `research_state/tracka_hl_early2025h1_panel_20261112T145529Z.parquet`
**Corrected build report:** `research_state/tracka_hl_early2025h1_panel_build_report_20261112T145529Z.json`

This note documents a **code/pipeline defect repair only**. No frozen hypothesis,
contrast, split, minimum, materiality threshold, or model feature was altered. The
prereg was already frozen before outcomes (`pre_registered_before_outcomes: true`) and
its SHA-256 is unchanged.

## Why the 134634Z evaluation was invalid

The 134634Z eval reported `liq` mean QLIKE `0.0` for every model (rel `n/a`, CI `[0,0]`,
p=1) and `rv` contrasts at ~1e-15 with identical per-coin/per-block diffs. Root cause was
three coupled defects in `scripts/early4h_campaign.py`, reproduced and confirmed live:

1. **Identity leak in the persistence lag (`_add_lags`).** The lag was built with
   `groupby(coin).shift(0)` — a no-op. Because the target is `t1_liq = liq_notional.shift(-1)`
   (next day), `shift(0)` made the "lag" equal to the current row's *target*:
   `lag_liq[t] = log(t1_liq[t])`. The persistence model therefore predicted the target
   from itself, so `yhat == y`, `ratio == 1`, and `QLIKE == 0` exactly. This is the
   `liq` all-zero result. The code comment already warned about this exact failure mode;
   `shift(0)` silently reintroduced it.

2. **Wrong lag column on the test side (`evaluate`).** The test design matrix used the
   shared placeholder `test["lag_log"]`, which `_add_lags` sets to `lag_liq`. The `rv`
   model was therefore fed liquidation-scale log values (~1e7) instead of log-RV (~-7).
   Predictions saturated at ~1.97e7, QLIKE ~19.27, and every model produced numerically
   identical outputs (~1e-15 diffs) — the `rv` "no signal" artifact. The train side was
   already per-target (`_design` overrides `lag_log` with `lag_<target>`); only the test
   side was wrong.

3. **Truncated funding warm-up (starved C1/C2).** `abs_fund_pct` was computed on the daily
   panel, which starts at `LABEL_START` (2025-05-25), so its 30-observation warm-up pushed
   the first valid value to 2025-06-15 and left 189/1440 rows missing. `_load_funding` also
   discarded all prints before `LABEL_START - 8d` (2025-05-17), even though the cache holds
   funding from 2025-05-01. Combined, C1/C2 trained on ~57-72 rows instead of ~258-324.

## Fixes applied (code only)

- `_add_lags`: `shift(0)` → `shift(1)`, so the lag is the previous day's realized value
  (the current day's realized value for a next-day target). No leakage: the lag at day `t`
  uses only data through day `t`.
- `evaluate`: test design matrix now uses `test[f"lag_{target}"]` (per-target lag), matching
  the train side.
- `abs_fund_pct`: computed on the daily funding series from the earliest cached print
  (2025-05-01), so the 30-obs warm-up completes by 2025-05-30 (only 5 warm-up days remain
  missing, all before/at `LABEL_START`). `_load_funding` now keeps the full fetched window
  (`FETCH_START`..`LABEL_END`). Funding is a feature, not a label: a trailing percentile at
  day `t` uses only prints `<= t`, so pre-window history leaks no outcome.
- `evaluate`: added an explicit numerical-stability validity guard
  (`numerical_stability` block). The frozen model is linear-in-log with an exp() link and
  **no regularization** (prereg bans regularization/tuning). When a handful of test rows
  extrapolate to `yhat ~1e-14` against a target `~1e7`, per-row QLIKE reaches `>1e15` and
  the mean is a numerical artifact. The guard reports `INCONCLUSIVE_NUMERICAL_INSTABILITY`
  instead of a meaningless `1e17` verdict.

## Corrected outcome (valid, claim-advancing)

| Target | Verdict | Basis |
|---|---|---|
| `rv` (next-24h realized variance) | **NOT_MET** | C2_vs_B1 mean diff `+0.243` (C2 worse), 95% CI `[-0.097, 0.583]` includes 0, rel `-29.3%`, p=0.161, Holm not rejected. Stable (max per-row QLIKE 73). |
| `liq` (next-24h observed liquidation notional) | **INCONCLUSIVE_NUMERICAL_INSTABILITY** | Frozen unregularized linear model extrapolates on the Oct-2025 funding spike (funding reaches `-0.002`, ~100x the train range `±0.00025`); max per-row QLIKE `1.6e27`. QLIKE not interpretable under the frozen estimator. |

The `rv` result is the decision-relevant one: **funding-conditioned features (C1/C2) do
not improve next-24h realized-variance forecasting over an RV-only HAR baseline on the
powered 2025-05-25..2025-10-31 Hyperliquid panel.** The `liq` result is not a substantive
null — it is an estimator-validity limitation of the frozen linear-in-log model.

## What this does NOT change

- No frozen hypothesis, contrast, split, minimum, materiality threshold, or feature was
  altered. The prereg SHA-256 is unchanged.
- No sealed verdict was reopened. No raw data was committed. No workflow file was edited.
- `liq` remains open: a QLIKE-consistent (Poisson/quasi-Poisson log-link) estimator is the
  natural next test, but it is a **new model form** and therefore requires a **new frozen
  prereg** before any outcome is inspected. Do not re-interpret the frozen linear model's
  `liq` result as a null.