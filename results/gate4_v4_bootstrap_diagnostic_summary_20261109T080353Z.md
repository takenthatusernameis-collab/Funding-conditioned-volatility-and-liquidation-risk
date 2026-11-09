# Gate 4 v4 bootstrap diagnostic summary (20261109T080828Z)

**EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE**

Deterministic summary of saved exploratory JSON artifacts. No recomputation, no network, no confirmatory claim, no promotion.
A non-degenerate CI excluding zero is claimable **only** when `degenerate=false`, `ci_valid=true`, and `inference_ok=true`.

## Artifacts consumed

- `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/gate4_v4_exploratory_diag/gate4_v4_exploratory_diag_20261109T021456Z.json`
- `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/gate4_v4_exploratory_stab/gate4_v4_exploratory_stab_20261109T045805Z.json`
- `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T070000Z.json`

## Risk table

| source | section | contrast | point | ci_low | ci_high | eff_blocks | ci_valid | regime_flags | degenerate | inference_ok | excludes_zero | claimable_excludes_zero |
|---|---|---|---:|---:|---:|---:|:---:|---|:---:|:---:|:---:|:---:|
| gate4_v4_exploratory_diag_20261109T021456Z.json | pooled_contrasts_vs_A_primary_fit | B_rv_signed | 11.1105 | 0.480523 | 32.3126 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | pooled_contrasts_vs_A_primary_fit | C_rv_abs | -0.0247101 | -0.371595 | 0.270799 | 120 | — | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | pooled_contrasts_vs_A_primary_fit | D_rv_signed_abs | 2.42192 | -0.25396 | 7.5122 | 120 | — | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | pooled_contrasts_vs_A_primary_fit | E_rv_funding_trails | 0.487902 | -0.0421608 | 1.19734 | 120 | — | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | pooled_contrasts_vs_A_stabilized_exploratory | B_rv_signed | 2996.43 | 1820.39 | 4323.81 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | pooled_contrasts_vs_A_stabilized_exploratory | C_rv_abs | 16.5646 | -0.293723 | 50.3007 | 120 | — | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | pooled_contrasts_vs_A_stabilized_exploratory | D_rv_signed_abs | 5920.47 | 3877.09 | 8091.82 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | pooled_contrasts_vs_A_stabilized_exploratory | E_rv_funding_trails | 9213.35 | 5201.59 | 14629.1 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | instrument_loo_E_vs_A_exploratory | all | 0.487902 | -0.0421608 | 1.19734 | 120 | — | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | instrument_loo_E_vs_A_exploratory | drop_BTCUSDT | 0.634232 | 0.13681 | 1.43679 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | instrument_loo_E_vs_A_exploratory | drop_ETHUSDT | 0.504444 | 0.0788974 | 1.19925 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | instrument_loo_E_vs_A_exploratory | drop_SOLUSDT | 1.13649 | 0.273338 | 2.37137 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | instrument_loo_E_vs_A_exploratory | drop_XRPUSDT | 0.110879 | -0.128657 | 0.358264 | 120 | — | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | instrument_loo_E_vs_A_exploratory | drop_BNBUSDT | 1.93818 | 0.714012 | 3.92039 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V1_primary.contrasts_vs_A | B_rv_signed | 11.1105 | 0.480523 | 32.3126 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V1_primary.contrasts_vs_A | C_rv_abs | -0.0247101 | -0.371595 | 0.270799 | 120 | — | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V1_primary.contrasts_vs_A | D_rv_signed_abs | 2.42192 | -0.25396 | 7.5122 | 120 | — | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V1_primary.contrasts_vs_A | E_rv_funding_trails | 0.487902 | -0.0421608 | 1.19734 | 120 | — | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V2_scale_ridge.contrasts_vs_A | B_rv_signed | 11.0677 | 0.480517 | 32.1829 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V2_scale_ridge.contrasts_vs_A | C_rv_abs | -0.0247096 | -0.371591 | 0.270797 | 120 | — | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V2_scale_ridge.contrasts_vs_A | D_rv_signed_abs | 2.39307 | -0.253958 | 7.42515 | 120 | — | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V2_scale_ridge.contrasts_vs_A | E_rv_funding_trails | 0.487859 | -0.0421738 | 1.19725 | 120 | — | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V3_scale_ridge_target_floor.contrasts_vs_A | B_rv_signed | 319.543 | 157.063 | 501.879 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V3_scale_ridge_target_floor.contrasts_vs_A | C_rv_abs | -59.5957 | -147.941 | -1.61092 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V3_scale_ridge_target_floor.contrasts_vs_A | D_rv_signed_abs | 517.9 | 79.1512 | 976.403 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V3_scale_ridge_target_floor.contrasts_vs_A | E_rv_funding_trails | 1096.43 | 330.863 | 2103.87 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V4_winsor_train.contrasts_vs_A | B_rv_signed | 514.086 | 368.846 | 665.249 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V4_winsor_train.contrasts_vs_A | C_rv_abs | -61.0569 | -171.677 | 33.6637 | 120 | — | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V4_winsor_train.contrasts_vs_A | D_rv_signed_abs | 386.206 | 14.9974 | 761.26 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V4_winsor_train.contrasts_vs_A | E_rv_funding_trails | 1421.5 | 414.222 | 2994.92 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | loo_e_vs_a_v3 | all | 1096.43 | 330.863 | 2103.87 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | loo_e_vs_a_v3 | drop_BTCUSDT | 1050.14 | 166.761 | 2255.25 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | loo_e_vs_a_v3 | drop_ETHUSDT | 1174.32 | 254.447 | 2376.07 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | loo_e_vs_a_v3 | drop_SOLUSDT | 1272.05 | 435.539 | 2476.22 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | loo_e_vs_a_v3 | drop_XRPUSDT | 343.813 | -131.785 | 813.773 | 120 | — | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | loo_e_vs_a_v3 | drop_BNBUSDT | 2024.78 | 813.658 | 3946.14 | 120 | — | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_leakage_audit_20261109T070000Z.json | block_bootstrap_reproducibility.run1 | E_vs_A_probe | 0.487902 | -0.0547066 | 1.18562 | 120 | true | ok | false | true | false | false |
| gate4_v4_leakage_audit_20261109T070000Z.json | block_bootstrap_reproducibility.run2 | E_vs_A_probe | 0.487902 | -0.0547066 | 1.18562 | 120 | true | ok | false | true | false | false |
| gate4_v4_leakage_audit_20261109T070000Z.json | block_bootstrap_reproducibility.run1_diagnostics | diagnostics | — | — | — | 120 | true | ok | false | true | — | false |
| gate4_v4_leakage_audit_20261109T070000Z.json | block_bootstrap_reproducibility.run2_diagnostics | diagnostics | — | — | — | 120 | true | ok | false | true | — | false |

## Decision guardrails (EXPLORATORY)

- contrasts with non-degenerate CI excluding zero (claimable): **0**
- contrasts with degenerate/invalid/inference-not-ok risk: **0**
- contrasts missing diagnostic fields (treated as not claimable): **36**
- If claimable count is 0, **no spurious improvement is claimable** from these artifacts.
- These artifacts remain **EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE**; they do not change prereg A–E contrasts, estimands, or confirmatory status.
