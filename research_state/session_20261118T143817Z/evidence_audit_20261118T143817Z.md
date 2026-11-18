# Evidence Audit — FCLR-VOL-LIQ-ROBUST-05

**Session:** session_20261118T143817Z
**Campaign:** FCLR-VOL-LIQ-ROBUST-05-20261118T132800Z
**Timestamp (UTC):** 20261118T143817Z
**Label:** EXPLORATORY/PILOT
**Network:** none. **Parquet:** none. **numpy/pandas/scipy:** none (stdlib only).

## Artifacts (all non-empty, this session dir)
- `fclr_robust05_prereg_20261118T143817Z.{json,md}` — outcome-blind prereg (`outcome_data_inspected_before_freeze=false`) frozen before any outcome access.
- `fclr_robust05_robustness_20261118T143817Z.{py,json,md}` — source, per-origin loss arrays, report.
- `trigger_check_20261118T143817Z.json` — all four reopen triggers OPEN; none fired.
- `recompute_fclr_robust05_robustness_20261118T143817Z.{py,json}` — independent aggregate + bootstrap recompute.
- Carried forward (not recomputed): `trackc_design_a_forecast_20261118T093031Z.*`, `trackb_breach_labels_20261118T093031Z.*`, `trackbc_breach_{prereg,forecast}_20261118T114500Z.*`, `fclr_robust04_{prereg,robustness}_20261118T132800Z.*`.

## Sign convention (do not invert)
`mean_delta_qlike_vs_A = mean(QLIKE_A − QLIKE_model)`; QLIKE is a loss (lower is better).
**Positive = model beats RV-only. Negative = model is worse.** The earlier "funding-trail improves QLIKE" headline was a sign inversion and is not repeated here.

## ROBUST-05 verdict (honest negative)
Four chronological holdouts (test months 2024-06/07/08/09), expanding train, 7-day purge/embargo, 5 instruments, stdlib OLS HAR + Duan smearing, QLIKE primary.

| Holdout | mean ΔQLIKE (A − E) | bootstrap CI95 | E beats A |
|---|---|---|---|
| 2024-06 | −0.0632 | [−0.0915, −0.0344] | no |
| 2024-07 | −0.2166 | [−0.2839, −0.1491] | no |
| 2024-08 | −0.7476 | [−1.1282, −0.3058] | no |
| 2024-09 | −0.0293 | [−0.0418, −0.0161] | no |

- Pooled: best model by mean QLIKE = **A_rv_only**; ΔQLIKE vs A: B −0.0060, C −0.0144, D −0.0480, E −0.2678 (CI95 [−0.3733, −0.1501]).
- Placebo (funding permuted across timestamps, seed 12345): pooled ΔQLIKE vs A = −0.0934; real |Δ| = 0.2678 > placebo |Δ| = 0.0934.
- **Materiality floor NOT met** (E beats A in 0 of 4 holdouts). Funding-conditioned volatility models are dominated by RV-only on every cached chronological holdout tested.

## Independent recompute
`recompute_fclr_robust05_robustness_20261118T143817Z.json` re-derives every reported aggregate and the frozen UTC-day block bootstrap (seed 12345, 2000 reps) from the stored per-origin loss arrays, without model re-estimation: **0 discrepancies**, materiality verdict matches. The result is reproducible from the artifact alone.

## Trigger check
All 4 reopen triggers OPEN; none fired. No confirmatory estimand advanced or re-scored.

## Prohibitions respected
No sealed re-score, no network, no root `research_state/*.md|json` writes (root 498/500), no sealed-artifact/workflow mutation, no duplicate `AGENT_HANDOFF`, no look-ahead, no full-sample normalization, no sealed months, no observed-liquidation labeling, no zero-byte artifacts.

## Honest status
EXPLORATORY/PILOT. The pre-registered funding-conditioned hypothesis is rejected on cached 2024-06..09 data under QLIKE. Negative result reported as-is; no confirmatory promotion claimed.
