# Gate 4 v4 bootstrap diagnostic summary (20261109T100310Z)

**EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE**

Deterministic summary of saved exploratory JSON artifacts. No recomputation, no network, no confirmatory claim, no promotion.
A non-degenerate CI excluding zero is claimable **only** when `degenerate=false`, `ci_valid=true`, and `inference_ok=true`.


## Diagnostic backfill audit trace (read-only; no source mutation)

- backfill_rules_version: `1.0`
- derivable fields only: `effective_block_count` (from `n_blocks` > 0), `ci_valid` (from finite ordered CI `ci_low <= ci_high` + finite `point`/`n_obs`)
- never inferred: `degenerate`, `inference_ok` (require explicit saved diagnostic evidence); backfilled fields alone never make a row claimable
- trace entries: **180** | fields backfilled (applied): **72** | fields refused (not derivable): **108**

- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::B_rv_signed` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::B_rv_signed` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::B_rv_signed` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::B_rv_signed` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::B_rv_signed` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::C_rv_abs` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::C_rv_abs` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::C_rv_abs` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::C_rv_abs` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::C_rv_abs` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::D_rv_signed_abs` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::D_rv_signed_abs` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::D_rv_signed_abs` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::D_rv_signed_abs` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::D_rv_signed_abs` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::E_rv_funding_trails` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::E_rv_funding_trails` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::E_rv_funding_trails` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::E_rv_funding_trails` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::E_rv_funding_trails` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::B_rv_signed` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::B_rv_signed` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::B_rv_signed` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::B_rv_signed` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::B_rv_signed` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::C_rv_abs` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::C_rv_abs` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::C_rv_abs` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::C_rv_abs` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::C_rv_abs` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::D_rv_signed_abs` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::D_rv_signed_abs` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::D_rv_signed_abs` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::D_rv_signed_abs` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::D_rv_signed_abs` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::E_rv_funding_trails` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::E_rv_funding_trails` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::E_rv_funding_trails` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::E_rv_funding_trails` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::E_rv_funding_trails` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::all` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::all` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::all` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::all` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::all` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_BTCUSDT` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_BTCUSDT` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_BTCUSDT` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_BTCUSDT` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_BTCUSDT` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_ETHUSDT` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_ETHUSDT` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_ETHUSDT` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_ETHUSDT` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_ETHUSDT` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_SOLUSDT` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_SOLUSDT` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_SOLUSDT` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_SOLUSDT` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_SOLUSDT` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_XRPUSDT` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_XRPUSDT` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_XRPUSDT` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_XRPUSDT` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_XRPUSDT` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_BNBUSDT` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_BNBUSDT` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_BNBUSDT` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_BNBUSDT` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_BNBUSDT` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::B_rv_signed` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::B_rv_signed` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::B_rv_signed` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::B_rv_signed` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::B_rv_signed` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::C_rv_abs` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::C_rv_abs` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::C_rv_abs` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::C_rv_abs` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::C_rv_abs` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::D_rv_signed_abs` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::D_rv_signed_abs` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::D_rv_signed_abs` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::D_rv_signed_abs` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::D_rv_signed_abs` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::E_rv_funding_trails` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::E_rv_funding_trails` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::E_rv_funding_trails` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::E_rv_funding_trails` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::E_rv_funding_trails` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::B_rv_signed` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::B_rv_signed` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::B_rv_signed` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::B_rv_signed` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::B_rv_signed` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::C_rv_abs` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::C_rv_abs` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::C_rv_abs` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::C_rv_abs` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::C_rv_abs` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::D_rv_signed_abs` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::D_rv_signed_abs` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::D_rv_signed_abs` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::D_rv_signed_abs` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::D_rv_signed_abs` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::E_rv_funding_trails` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::E_rv_funding_trails` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::E_rv_funding_trails` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::E_rv_funding_trails` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::E_rv_funding_trails` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::B_rv_signed` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::B_rv_signed` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::B_rv_signed` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::B_rv_signed` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::B_rv_signed` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::C_rv_abs` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::C_rv_abs` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::C_rv_abs` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::C_rv_abs` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::C_rv_abs` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::D_rv_signed_abs` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::D_rv_signed_abs` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::D_rv_signed_abs` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::D_rv_signed_abs` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::D_rv_signed_abs` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::E_rv_funding_trails` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::E_rv_funding_trails` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::E_rv_funding_trails` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::E_rv_funding_trails` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::E_rv_funding_trails` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::B_rv_signed` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::B_rv_signed` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::B_rv_signed` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::B_rv_signed` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::B_rv_signed` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::C_rv_abs` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::C_rv_abs` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::C_rv_abs` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::C_rv_abs` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::C_rv_abs` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::D_rv_signed_abs` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::D_rv_signed_abs` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::D_rv_signed_abs` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::D_rv_signed_abs` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::D_rv_signed_abs` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::E_rv_funding_trails` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::E_rv_funding_trails` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::E_rv_funding_trails` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::E_rv_funding_trails` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::E_rv_funding_trails` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::all` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::all` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::all` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::all` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::all` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_BTCUSDT` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_BTCUSDT` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_BTCUSDT` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_BTCUSDT` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_BTCUSDT` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_ETHUSDT` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_ETHUSDT` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_ETHUSDT` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_ETHUSDT` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_ETHUSDT` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_SOLUSDT` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_SOLUSDT` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_SOLUSDT` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_SOLUSDT` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_SOLUSDT` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_XRPUSDT` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_XRPUSDT` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_XRPUSDT` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_XRPUSDT` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_XRPUSDT` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_BNBUSDT` | field=effective_block_count | rule=effective_block_count_from_n_blocks | applied=true | source=n_blocks | value=120 | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_BNBUSDT` | field=ci_valid | rule=ci_valid_from_finite_ordered_ci | applied=true | source=ci_low,ci_high,point,n_obs | value=true | refusal=—
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_BNBUSDT` | field=degenerate | rule=degenerate_from_ci_width | applied=false | source=— | value=— | refusal=degenerate_not_inferrable_from_ci_width_or_point
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_BNBUSDT` | field=inference_ok | rule=inference_ok_from_explicit_evidence | applied=false | source=— | value=— | refusal=inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_BNBUSDT` | field=diagnostic_gates_residual | rule=residual_missing_diagnostic_fields | applied=false | source=— | value=false | refusal=degenerate_or_inference_ok_unproven

Claimability remains governed by degenerate==false, ci_valid==true, inference_ok==true and a finite CI excluding zero. Backfilled `ci_valid`/`effective_block_count` alone never make a row claimable while `degenerate`/`inference_ok` are unproven; such rows keep MISSING_DIAGNOSTIC_FIELDS and claimable_excludes_zero=false.

## Backfill coverage summary (machine-checkable)

- backfill_coverage_rules_version: `1.0`
- rows total: **40**
- rows already complete (no missing diagnostic fields): **4**
- rows missing diagnostic fields after backfill: **36**
- rows with at least one provably backfilled field: **36**
- derivable fields: `['effective_block_count', 'ci_valid']`
- never-inferrable fields: `['degenerate', 'inference_ok']`
- refused field counts (field -> number of rows where the backfill refused to derive it):
  - `degenerate`: **36**
  - `inference_ok`: **36**
- A row is claimable only when `degenerate=false`, `ci_valid=true`, `inference_ok=true` and the CI excludes zero. Backfill coverage never changes claimability for rows with unproven `degenerate`/`inference_ok`.

## MISSING_DIAGNOSTIC_FIELDS remediation list (refusal-first; no source mutation)

- backfill_strict_rules_version: `1.0`
- remediation entries: **72**
- Each entry names the row, the still-missing field, the concrete reason the field cannot be derived from saved CI geometry, and the only admissible remedy (explicit saved diagnostic evidence in a source artifact). No field is inferred; no gate is fabricated.

- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::B_rv_signed` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::B_rv_signed` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::C_rv_abs` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::C_rv_abs` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::D_rv_signed_abs` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::D_rv_signed_abs` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::E_rv_funding_trails` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_primary_fit::E_rv_funding_trails` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::B_rv_signed` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::B_rv_signed` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::C_rv_abs` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::C_rv_abs` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::D_rv_signed_abs` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::D_rv_signed_abs` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::E_rv_funding_trails` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::pooled_contrasts_vs_A_stabilized_exploratory::E_rv_funding_trails` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::all` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::all` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_BTCUSDT` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_BTCUSDT` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_ETHUSDT` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_ETHUSDT` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_SOLUSDT` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_SOLUSDT` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_XRPUSDT` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_XRPUSDT` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_BNBUSDT` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_diag_20261109T021456Z.json::instrument_loo_E_vs_A_exploratory::drop_BNBUSDT` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::B_rv_signed` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::B_rv_signed` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::C_rv_abs` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::C_rv_abs` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::D_rv_signed_abs` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::D_rv_signed_abs` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::E_rv_funding_trails` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V1_primary.contrasts_vs_A::E_rv_funding_trails` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::B_rv_signed` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::B_rv_signed` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::C_rv_abs` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::C_rv_abs` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::D_rv_signed_abs` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::D_rv_signed_abs` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::E_rv_funding_trails` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V2_scale_ridge.contrasts_vs_A::E_rv_funding_trails` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::B_rv_signed` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::B_rv_signed` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::C_rv_abs` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::C_rv_abs` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::D_rv_signed_abs` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::D_rv_signed_abs` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::E_rv_funding_trails` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V3_scale_ridge_target_floor.contrasts_vs_A::E_rv_funding_trails` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::B_rv_signed` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::B_rv_signed` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::C_rv_abs` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::C_rv_abs` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::D_rv_signed_abs` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::D_rv_signed_abs` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::E_rv_funding_trails` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::V4_winsor_train.contrasts_vs_A::E_rv_funding_trails` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::all` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::all` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_BTCUSDT` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_BTCUSDT` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_ETHUSDT` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_ETHUSDT` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_SOLUSDT` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_SOLUSDT` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_XRPUSDT` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_XRPUSDT` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=false
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_BNBUSDT` | field=degenerate | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: degenerate is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field
- `gate4_v4_exploratory_stab_20261109T045805Z.json::loo_e_vs_a_v3::drop_BNBUSDT` | field=inference_ok | claimable_excludes_zero=false | ci_excludes_zero=true
  - reason: inference_ok is not inferrable from CI width, point estimate, or excludes-zero geometry; it requires explicit saved diagnostic evidence in a source artifact.
  - remediation: Supply explicit saved diagnostic evidence for this field in a source artifact (e.g. a block_bootstrap_reproducibility diagnostics record with exact context), or leave the row unproven and not claimable.
  - refusal_reasons: degenerate_not_inferrable_from_ci_width_or_point, degenerate_or_inference_ok_unproven, inference_ok_not_inferrable_without_explicit_diagnostic_field

## Remediation by source artifact (still-unproven degenerate/inference_ok counts)

- deduped remediation entries: **72** per (row_id, field) with stable deterministic `remediation_id`
- source artifacts with unproven gate fields: **2**
- Counts reflect still-unproven `degenerate`/`inference_ok` fields only (never inferred; refusal-first).

  - `gate4_v4_exploratory_diag_20261109T021456Z.json`: degenerate=14, inference_ok=14, total=28
  - `gate4_v4_exploratory_stab_20261109T045805Z.json`: degenerate=22, inference_ok=22, total=44

A future diagnostic-producer can target these exact source artifacts rather than scanning the flat entry list.


Machine-readable remediation list emitted as `missing_diagnostic_fields_<UTC>.json` alongside this report.

## Artifacts consumed

- `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/gate4_v4_exploratory_diag/gate4_v4_exploratory_diag_20261109T021456Z.json`
- `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/gate4_v4_exploratory_stab/gate4_v4_exploratory_stab_20261109T045805Z.json`
- `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T070000Z.json`

## Risk table

| source | section | contrast | point | ci_low | ci_high | eff_blocks | ci_valid | regime_flags | degenerate | inference_ok | excludes_zero | claimable_excludes_zero |
|---|---|---|---:|---:|---:|---:|:---:|---|:---:|:---:|:---:|:---:|
| gate4_v4_exploratory_diag_20261109T021456Z.json | pooled_contrasts_vs_A_primary_fit | B_rv_signed | 11.1105 | 0.480523 | 32.3126 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | pooled_contrasts_vs_A_primary_fit | C_rv_abs | -0.0247101 | -0.371595 | 0.270799 | 120 | true | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | pooled_contrasts_vs_A_primary_fit | D_rv_signed_abs | 2.42192 | -0.25396 | 7.5122 | 120 | true | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | pooled_contrasts_vs_A_primary_fit | E_rv_funding_trails | 0.487902 | -0.0421608 | 1.19734 | 120 | true | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | pooled_contrasts_vs_A_stabilized_exploratory | B_rv_signed | 2996.43 | 1820.39 | 4323.81 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | pooled_contrasts_vs_A_stabilized_exploratory | C_rv_abs | 16.5646 | -0.293723 | 50.3007 | 120 | true | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | pooled_contrasts_vs_A_stabilized_exploratory | D_rv_signed_abs | 5920.47 | 3877.09 | 8091.82 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | pooled_contrasts_vs_A_stabilized_exploratory | E_rv_funding_trails | 9213.35 | 5201.59 | 14629.1 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | instrument_loo_E_vs_A_exploratory | all | 0.487902 | -0.0421608 | 1.19734 | 120 | true | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | instrument_loo_E_vs_A_exploratory | drop_BTCUSDT | 0.634232 | 0.13681 | 1.43679 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | instrument_loo_E_vs_A_exploratory | drop_ETHUSDT | 0.504444 | 0.0788974 | 1.19925 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | instrument_loo_E_vs_A_exploratory | drop_SOLUSDT | 1.13649 | 0.273338 | 2.37137 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | instrument_loo_E_vs_A_exploratory | drop_XRPUSDT | 0.110879 | -0.128657 | 0.358264 | 120 | true | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_diag_20261109T021456Z.json | instrument_loo_E_vs_A_exploratory | drop_BNBUSDT | 1.93818 | 0.714012 | 3.92039 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V1_primary.contrasts_vs_A | B_rv_signed | 11.1105 | 0.480523 | 32.3126 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V1_primary.contrasts_vs_A | C_rv_abs | -0.0247101 | -0.371595 | 0.270799 | 120 | true | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V1_primary.contrasts_vs_A | D_rv_signed_abs | 2.42192 | -0.25396 | 7.5122 | 120 | true | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V1_primary.contrasts_vs_A | E_rv_funding_trails | 0.487902 | -0.0421608 | 1.19734 | 120 | true | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V2_scale_ridge.contrasts_vs_A | B_rv_signed | 11.0677 | 0.480517 | 32.1829 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V2_scale_ridge.contrasts_vs_A | C_rv_abs | -0.0247096 | -0.371591 | 0.270797 | 120 | true | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V2_scale_ridge.contrasts_vs_A | D_rv_signed_abs | 2.39307 | -0.253958 | 7.42515 | 120 | true | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V2_scale_ridge.contrasts_vs_A | E_rv_funding_trails | 0.487859 | -0.0421738 | 1.19725 | 120 | true | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V3_scale_ridge_target_floor.contrasts_vs_A | B_rv_signed | 319.543 | 157.063 | 501.879 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V3_scale_ridge_target_floor.contrasts_vs_A | C_rv_abs | -59.5957 | -147.941 | -1.61092 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V3_scale_ridge_target_floor.contrasts_vs_A | D_rv_signed_abs | 517.9 | 79.1512 | 976.403 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V3_scale_ridge_target_floor.contrasts_vs_A | E_rv_funding_trails | 1096.43 | 330.863 | 2103.87 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V4_winsor_train.contrasts_vs_A | B_rv_signed | 514.086 | 368.846 | 665.249 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V4_winsor_train.contrasts_vs_A | C_rv_abs | -61.0569 | -171.677 | 33.6637 | 120 | true | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V4_winsor_train.contrasts_vs_A | D_rv_signed_abs | 386.206 | 14.9974 | 761.26 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | V4_winsor_train.contrasts_vs_A | E_rv_funding_trails | 1421.5 | 414.222 | 2994.92 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | loo_e_vs_a_v3 | all | 1096.43 | 330.863 | 2103.87 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | loo_e_vs_a_v3 | drop_BTCUSDT | 1050.14 | 166.761 | 2255.25 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | loo_e_vs_a_v3 | drop_ETHUSDT | 1174.32 | 254.447 | 2376.07 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | loo_e_vs_a_v3 | drop_SOLUSDT | 1272.05 | 435.539 | 2476.22 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | loo_e_vs_a_v3 | drop_XRPUSDT | 343.813 | -131.785 | 813.773 | 120 | true | MISSING_DIAGNOSTIC_FIELDS | — | — | false | false |
| gate4_v4_exploratory_stab_20261109T045805Z.json | loo_e_vs_a_v3 | drop_BNBUSDT | 2024.78 | 813.658 | 3946.14 | 120 | true | EXCLUDES_ZERO_NOT_CLAIMABLE,MISSING_DIAGNOSTIC_FIELDS | — | — | true | false |
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
