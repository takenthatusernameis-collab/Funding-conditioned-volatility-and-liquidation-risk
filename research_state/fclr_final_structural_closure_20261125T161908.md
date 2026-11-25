# Program Terminal Structural Closure — FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS

**Generated (UTC):** 2026-11-25T16:19:08Z
**Program status:** CLOSED_TERMINAL
**Terminal verdict:** NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED
**Rows enumerated:** 71
**§17 promotion met (any row):** 0
**All §17 conditions not met:** True

## Reopen conditions (machine-checkable; act only when satisfied)

- `GATE4_BRANCH_1` (priority 1, status=OPEN)
  - predicate: {"attestation": "human/legal", "glob": "research_state/fclr016_v5_terms_evidence_RESOLVED_*.json", "note": "Never agent-set; never bypassed; no whole-tree grep for the trigger string.", "required_fields": {"fabricated": false, "status": "RESOLVED_VERIFIED"}, "type": "file_glob_with_fields"}
  - required evidence: research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json
  - gate protocol: RESEARCH_PROMPT.md Gate 4 Branch 1 (external/legal evidence)
  - do_not_act_until_satisfied: True
- `NEW_OBSERVED_LIQUIDATION_SOURCE` (priority 2, status=OPEN)
  - predicate: {"also_documented": ["provenance", "license", "venue_consistent"], "note": "Or (instruments>=5 AND complete_month>=1) in place of blocks>=3 per RESEARCH_PROMPT \u00a716.", "path_template": "research_state/<source>_admissibility_audit_<UTC>.json", "required_fields": {"blocks": {"op": ">=", "value": 3}, "complete_month": {"op": ">=", "value": 1}, "instruments": {"op": ">=", "value": 5}, "observed_labels": true, "status": "ADMISSIBLE", "unauthenticated": true}, "type": "file_exists_with_fields"}
  - required evidence: research_state/<source>_admissibility_audit_<UTC>.{md,json}
  - gate protocol: RESEARCH_PROMPT.md §5 source acceptance + §16 admissibility audit BEFORE preregistration/outcomes
  - do_not_act_until_satisfied: True
- `HL_LABEL_EXTENSION` (priority 3, status=OPEN)
  - predicate: {"required": {"labels_after": "2026-10-31", "min_depth_days": 100, "observed_only": true, "venue": "hyperliquid_perpetuals"}, "source": "ironflow/hyperliquid-liquidations", "type": "verified_label_extension"}
  - required evidence: research_state/hl_label_extension_audit_<UTC>.{md,json}
  - gate protocol: RESEARCH_PROMPT.md §5/§16 on verified post-2026-10-31 observed ironflow labels
  - do_not_act_until_satisfied: True
- `EXPANSION_ROBUSTNESS_REDO` (priority 4, status=OPEN)
  - predicate: {"basis": "H_tracka_hl_expansion_robustness sealed FRAGILE", "conditions": ["LOIO >= 6 of 8 subsets pass", "placebo/permutation: true effect > 95th percentile of null"], "forbidden": "re-scoring the sealed 19.04% result", "type": "newly_preregistered_design"}
  - required evidence: research_state/expansion_robustness_redo_prereg_<UTC>.json + evaluation_summary_*.json
  - gate protocol: RESEARCH_PROMPT.md §17 promotion conditions 1-7 all met by a newly preregistered design (conditional, non-priority)
  - do_not_act_until_satisfied: True

## Enumerated experiments / hypotheses / sealed verdicts

| id | type | status | verdict | gate_outcome | §17 promotion met | terminal class | reopen_requires |
|---|---|---|---|---|---|---|---|
| FCLR-011-INDEPENDENT-RECOMPUTE-20261114T042139Z | experiment | INADMISSIBLE | INADMISSIBLE | INADMISSIBLE | False | INADMISSIBLE | — |
| FCLR-DESIGN-FEASIBILITY-20261115T021249Z | experiment | UNDECIDABLE_ON_CACHE | UNDECIDABLE_ON_CACHE | UNDECIDABLE_ON_CACHE | False | UNDECIDABLE_ON_CACHE | — |
| FCLR-EXP-ROBUST-REDO-20261113T063000Z | experiment | FRAGILE | FRAGILE | FRAGILE | False | FRAGILE | — |
| FCLR-FWD-VOL-011-CONFIRM-20261113T041200Z | experiment | NOT_REPLICATED | NOT_REPLICATED | NOT_REPLICATED | False | NOT_REPLICATED | — |
| FCLR-FWD-VOL-2024-DISJOINT-2024-06-20261114T231100Z | experiment | EXPLAINED_BY_ESTIMATOR | EXPLAINED_BY_ESTIMATOR | EXPLAINED_BY_ESTIMATOR | False | EXPLAINED_BY_ESTIMATOR | — |
| FCLR-FWD-VOL-2024Q4-CROSS-20261113T091500Z | experiment | NOT_REPLICATED | NOT_REPLICATED | NOT_REPLICATED | False | NOT_REPLICATED | — |
| FCLR-FWD-VOL-2025-CROSS-20261113T063000Z | experiment | NOT_REPLICATED | NOT_REPLICATED | NOT_REPLICATED | False | NOT_REPLICATED | — |
| FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z | experiment | NOT_EXPLAINED_BY_ESTIMATOR | NOT_EXPLAINED_BY_ESTIMATOR | NOT_EXPLAINED_BY_ESTIMATOR | False | NOT_EXPLAINED_BY_ESTIMATOR | — |
| FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z | experiment | EXPLORATORY_NULL | EXPLORATORY_NULL | EXPLORATORY_NULL | False | EXPLORATORY_NULL | — |
| FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z | experiment | UNEXPLAINED | UNEXPLAINED | UNEXPLAINED | False | UNEXPLAINED | — |
| FCLR-FWD-VOL-2025H2-CROSS-20261113T102139Z | experiment | NOT_REPLICATED | NOT_REPLICATED | NOT_REPLICATED | False | NOT_REPLICATED | — |
| FCLR-FWD-VOL-2025Q1Q2-CROSS-20261113T111601Z | experiment | NOT_REPLICATED | NOT_REPLICATED | NOT_REPLICATED | False | NOT_REPLICATED | — |
| FCLR-LIQ-010-CONFIRM-20261113T063000Z | experiment | NOT_REPLICATED | NOT_REPLICATED | NOT_REPLICATED | False | NOT_REPLICATED | — |
| FCLR-LIQ-COMBINED-20261115T181449Z | experiment | unknown | unknown | unknown | False | unknown | — |
| FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T073346Z | experiment | INCONCLUSIVE | INCONCLUSIVE | INCONCLUSIVE | False | INCONCLUSIVE | — |
| FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z | experiment | INCONCLUSIVE | INCONCLUSIVE | INCONCLUSIVE | False | INCONCLUSIVE | — |
| FCLR-LIQ-XSEC-ORDERING-20261115T200813Z | experiment | unknown | unknown | unknown | False | unknown | — |
| FCLR-LIQ-XSEC-ORDERING-20261115T203501Z | experiment | unknown | unknown | unknown | False | unknown | — |
| FCLR-LIQ-XSEC-QLIKE-20261115T214903Z | experiment | unknown | unknown | unknown | False | unknown | — |
| FCLR-POWER-CALIBRATION-2026-11-15T01:34:12Z | experiment | INCONCLUSIVE | INCONCLUSIVE | INCONCLUSIVE | False | INCONCLUSIVE | — |
| H1_primary | hypothesis | NOT_SUPPORTED | FCLR-011 forecast_gate_PASS (4.94%, CI excludes zero) on 2026-05..2026-08 window; forward confirmation FCLR-FWD-VOL-011-CONFIRM NOT_REPLICATED on 2026-08..2026-10 (C2 worse by 5.55%, CI [0.000343,0.064822] favouring B1, rel -5.55%, reproduction delta 0.044pp within tolerance). FCLR-011 PASS does not generalize forward. | FCLR-011 forecast_gate_PASS (4.94%, CI excludes zero) on 2026-05..2026-08 window; forward confirmation FCLR-FWD-VOL-011-CONFIRM NOT_REPLICATED on 2026-08..2026-10 (C2 worse by 5.55%, CI [0.000343,0.064822] favouring B1, rel -5.55%, reproduction delta 0.044pp within tolerance). FCLR-011 PASS does not generalize forward. | False | NOT_SUPPORTED | GATE4_BRANCH_1,NEW_OBSERVED_LIQUIDATION_SOURCE |
| H2_shek_replication | hypothesis | EXPLORATORY_ONLY | SCALED_EXPLORATORY (Arm A TAIL_SHAPE_EFFECT, Arm B REPLICATES_DIRECTION; EXPLORATORY_ONLY, not promotable) | SCALED_EXPLORATORY (Arm A TAIL_SHAPE_EFFECT, Arm B REPLICATES_DIRECTION; EXPLORATORY_ONLY, not promotable) | False | EXPLORATORY_ONLY | — |
| H_contagion_funding | hypothesis | NOT_STARTED | NOT_STARTED | NOT_STARTED | False | NOT_STARTED | — |
| H_contagion_liq | hypothesis | NOT_STARTED | NOT_STARTED | NOT_STARTED | False | NOT_STARTED | — |
| H_fclr_exp_robust_redo | hypothesis | FRAGILE | FRAGILE | FRAGILE | False | FRAGILE | — |
| H_fclr_fwd_vol_011_confirm | hypothesis | NOT_REPLICATED | NOT_REPLICATED | NOT_REPLICATED | False | NOT_REPLICATED | — |
| H_fclr_fwd_vol_2024q4_cross | hypothesis | NOT_REPLICATED | NOT_REPLICATED | NOT_REPLICATED | False | NOT_REPLICATED | — |
| H_fclr_fwd_vol_2025_cross | hypothesis | NOT_REPLICATED | NOT_REPLICATED | NOT_REPLICATED | False | NOT_REPLICATED | — |
| H_fclr_fwd_vol_2025h2_cross | hypothesis | NOT_REPLICATED | NOT_REPLICATED | NOT_REPLICATED | False | NOT_REPLICATED | — |
| H_fclr_fwd_vol_2025q1q2_cross | hypothesis | NOT_REPLICATED | NOT_REPLICATED | NOT_REPLICATED | False | NOT_REPLICATED | — |
| H_fclr_liq_010_confirm | hypothesis | NOT_REPLICATED | NOT_REPLICATED | NOT_REPLICATED | False | NOT_REPLICATED | — |
| H_fclr_liq_combined_panel_forecast | hypothesis | NOT_MET | forecast_gate_NOT_MET | forecast_gate_NOT_MET | False | NOT_MET | — |
| H_fclr_liq_xsec_ordering_forecast | hypothesis | NOT_MET | NOT_MET | NOT_MET | False | NOT_MET | — |
| H_fclr_liq_xsec_qlike_forecast | hypothesis | NOT_MET | NOT_MET | NOT_MET | False | NOT_MET | — |
| H_fclr_panelfe_001 | hypothesis | NOT_SUPPORTED | NOT_SUPPORTED | NOT_SUPPORTED | False | NOT_SUPPORTED | — |
| H_fclr_session_synthesis_01 | hypothesis | CONSOLIDATORY_ONLY | CONSOLIDATORY_ONLY: RV fixed-effect pooled d=1.237 (CI incl. zero); liquidation fixed-effect pooled d=0.379 (CI excl. zero) but random-effects DL pooled d=0.228 (CI incl. zero) under I^2=97.5% heterogeneity; joint random-effects CI incl. zero. Cross-sectional associations detectable in specific regimes but not homogeneous and not robust under random effects; combined with failed OOS forecast/forward gates, no promotable funding-conditioned forecast skill. Does not promote any terminal hypothesis; all terminal verdicts carried forward unchanged. | CONSOLIDATORY_ONLY: RV fixed-effect pooled d=1.237 (CI incl. zero); liquidation fixed-effect pooled d=0.379 (CI excl. zero) but random-effects DL pooled d=0.228 (CI incl. zero) under I^2=97.5% heterogeneity; joint random-effects CI incl. zero. Cross-sectional associations detectable in specific regimes but not homogeneous and not robust under random effects; combined with failed OOS forecast/forward gates, no promotable funding-conditioned forecast skill. Does not promote any terminal hypothesis; all terminal verdicts carried forward unchanged. | False | CONSOLIDATORY_ONLY | — |
| H_fclr_xsec_001 | hypothesis | NOT_SUPPORTED | NOT_SUPPORTED | NOT_SUPPORTED | False | NOT_SUPPORTED | — |
| H_fclr_xsec_002 | hypothesis | SUPPORTED | SUPPORTED | SUPPORTED | False | SUPPORTED | — |
| H_fclr_xsec_003 | hypothesis | SUPERSEDED | SUPERSEDED | SUPERSEDED | False | SUPERSEDED | — |
| H_fclr_xsec_004 | hypothesis | SUPPORTED | SUPPORTED | SUPPORTED | False | SUPPORTED | — |
| H_fclr_xsec_005 | hypothesis | SUPPORTED | SUPPORTED | SUPPORTED | False | SUPPORTED | — |
| H_fclr_xsec_006 | hypothesis | SUPPORTED | SUPPORTED | SUPPORTED | False | SUPPORTED | — |
| H_fclr_xsec_007 | hypothesis | NOT_SUPPORTED | NOT_SUPPORTED | NOT_SUPPORTED | False | NOT_SUPPORTED | — |
| H_fclr_xsec_008 | hypothesis | NOT_SUPPORTED | NOT_SUPPORTED | NOT_SUPPORTED | False | NOT_SUPPORTED | — |
| H_liq_oos_funding_conditioned_forecast | hypothesis | NOT_SUPPORTED | OOS forecast gate NOT_SUPPORTED (QLIKE fail; Brier +11.48% PASS; LogLoss +8.63% PASS; joint requires ALL three metrics; independent recompute concurs NOT_SUPPORTED) | OOS forecast gate NOT_SUPPORTED (QLIKE fail; Brier +11.48% PASS; LogLoss +8.63% PASS; joint requires ALL three metrics; independent recompute concurs NOT_SUPPORTED) | False | NOT_SUPPORTED | — |
| H_tracka_hl_alt_volatility_forecast | hypothesis | NOT_MET | forecast_gate_NOT_MET | forecast_gate_NOT_MET | False | NOT_MET | GATE4_BRANCH_1,NEW_OBSERVED_LIQUIDATION_SOURCE |
| H_tracka_hl_early_liquidation_forecast | hypothesis | INCONCLUSIVE_PILOT_SHORTFALL | inconclusive_pilot_shortfall | inconclusive_pilot_shortfall | False | INCONCLUSIVE_PILOT_SHORTFALL | NEW_OBSERVED_LIQUIDATION_SOURCE,HL_LABEL_EXTENSION |
| H_tracka_hl_expansion_recompute | hypothesis | INCONCLUSIVE | INCONCLUSIVE (VALID_EXPLORATORY) | INCONCLUSIVE (VALID_EXPLORATORY) | False | INCONCLUSIVE | — |
| H_tracka_hl_expansion_robustness | hypothesis | FRAGILE | robustness_gate_FRAGILE | robustness_gate_FRAGILE | False | FRAGILE | EXPANSION_ROBUSTNESS_REDO |
| H_tracka_hl_funding_conditioned_volatility_forecast | hypothesis | NOT_MET | forecast_gate_NOT_MET | forecast_gate_NOT_MET | False | NOT_MET | GATE4_BRANCH_1,NEW_OBSERVED_LIQUIDATION_SOURCE |
| H_tracka_hl_funding_conditioned_volatility_fullhistory | hypothesis | NOT_MET | forecast_gate_NOT_MET | forecast_gate_NOT_MET | False | NOT_MET | — |
| H_tracka_hl_liquidation_cross_sectional_funding | hypothesis | EXPLORATORY_NULL | exploratory_null | exploratory_null | False | EXPLORATORY_NULL | — |
| H_tracka_hl_liquidation_forecast | hypothesis | NOT_MET | forecast_gate_NOT_MET | forecast_gate_NOT_MET | False | NOT_MET | NEW_OBSERVED_LIQUIDATION_SOURCE,HL_LABEL_EXTENSION |
| H_tracka_hl_symbol_expansion_liquidation_forecast | hypothesis | SUPPORTED_PASS_PRIMARY_GATE | forecast_gate_PASS | forecast_gate_PASS | False | SUPPORTED_PASS_PRIMARY_GATE | NEW_OBSERVED_LIQUIDATION_SOURCE,HL_LABEL_EXTENSION |
| H_trackb_modeled_breaches | hypothesis | NOT_SUPPORTED | forecast_gate_NOT_MET | forecast_gate_NOT_MET | False | NOT_SUPPORTED | — |
| TRACKA-HL-EARLY-4H-20261112T054737Z | experiment | INCONCLUSIVE_PILOT_SHORTFALL | INCONCLUSIVE_PILOT_SHORTFALL | INCONCLUSIVE_PILOT_SHORTFALL | False | INCONCLUSIVE_PILOT_SHORTFALL | — |
| TRACKA-HL-EARLY4H-2025H1 | experiment | unknown | unknown | unknown | False | unknown | — |
| TRACKA-HL-EARLY4H-2025H1-LIQ-GLM | experiment | INCONCLUSIVE_NUMERICAL_INSTABILITY | INCONCLUSIVE_NUMERICAL_INSTABILITY | INCONCLUSIVE_NUMERICAL_INSTABILITY | False | INCONCLUSIVE_NUMERICAL_INSTABILITY | — |
| TRACKA-HL-EARLY4H-2025H1-LIQ-GLM-ROBUST | experiment | NOT_MET | NOT_MET | NOT_MET | False | NOT_MET | NEW_OBSERVED_LIQUIDATION_SOURCE,HL_LABEL_EXTENSION |
| TRACKA-LIQ-XSEC-20261112T201536Z | experiment | EXPLORATORY_NULL | EXPLORATORY_NULL | EXPLORATORY_NULL | False | EXPLORATORY_NULL | — |
| TRACKA-LIQ-XSEC-FORWARD-20261113T222859Z | experiment | EXPLORATORY_NULL | EXPLORATORY_NULL | EXPLORATORY_NULL | False | EXPLORATORY_NULL | — |
| TRACKA-VOL-20261111T234918Z | experiment | NOT_MET | NOT_MET | NOT_MET | False | NOT_MET | — |
| TRACKA-VOL-FORWARD-2026Q1Q2-20261114T015222Z | experiment | EXPLORATORY_NULL | EXPLORATORY_NULL | EXPLORATORY_NULL | False | EXPLORATORY_NULL | — |
| TRACKA-VOL-FULLHIST-20261112T201536Z | experiment | NOT_MET | NOT_MET | NOT_MET | False | NOT_MET | — |
| alt_source_probe_audit_20261112T191400Z | source_probe_audit | NO_ADMISSIBLE_SOURCE | NO_GO | all probed families NO-GO | False | NO_ADMISSIBLE_SOURCE | NEW_OBSERVED_LIQUIDATION_SOURCE |
| evaluation_summary_FCLR-SHEK-SCALE-20261115T071135Z | experiment | unknown | unknown | unknown | False | unknown | — |
| evaluation_summary_FCLR-SHEK-SCALE-20261115T144938Z | experiment | unknown | unknown | unknown | False | unknown | — |
| evaluation_summary_FCLR-SHEK-SCALE-SENS-20261115T144938Z | experiment | unknown | unknown | unknown | False | unknown | — |
| evaluation_summary_TRACKA-ALT-VOL-20261112T020322Z | experiment | NOT_MET | NOT_MET | NOT_MET | False | NOT_MET | — |
| evaluation_summary_TRACKA-EXP-ROBUST-20261112T015119Z | experiment | FRAGILE | FRAGILE | FRAGILE | False | FRAGILE | — |
| terminal_structural_stop_liq_glm_robust_20261112T170457Z | sealed_verdict | TERMINAL_STRUCTURAL_STOP | NOT_MET** | NOT_MET** | False | TERMINAL_STRUCTURAL_STOP | — |

## Failing minima (per row)

- **FCLR-011-INDEPENDENT-RECOMPUTE-20261114T042139Z** (experiment): verdict=INADMISSIBLE; gate_pass=n/a
- **FCLR-DESIGN-FEASIBILITY-20261115T021249Z** (experiment): verdict=UNDECIDABLE_ON_CACHE; gate_pass=n/a
- **FCLR-EXP-ROBUST-REDO-20261113T063000Z** (experiment): verdict=FRAGILE; gate_pass=n/a
- **FCLR-FWD-VOL-011-CONFIRM-20261113T041200Z** (experiment): verdict=NOT_REPLICATED; gate_pass=n/a
- **FCLR-FWD-VOL-2024-DISJOINT-2024-06-20261114T231100Z** (experiment): verdict=EXPLAINED_BY_ESTIMATOR; gate_pass=n/a
- **FCLR-FWD-VOL-2024Q4-CROSS-20261113T091500Z** (experiment): verdict=NOT_REPLICATED; gate_pass=n/a
- **FCLR-FWD-VOL-2025-CROSS-20261113T063000Z** (experiment): verdict=NOT_REPLICATED; gate_pass=n/a
- **FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z** (experiment): verdict=NOT_EXPLAINED_BY_ESTIMATOR; gate_pass=n/a
- **FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z** (experiment): verdict=EXPLORATORY_NULL; gate_pass=n/a
- **FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z** (experiment): verdict=UNEXPLAINED; gate_pass=n/a
- **FCLR-FWD-VOL-2025H2-CROSS-20261113T102139Z** (experiment): verdict=NOT_REPLICATED; gate_pass=n/a
- **FCLR-FWD-VOL-2025Q1Q2-CROSS-20261113T111601Z** (experiment): verdict=NOT_REPLICATED; gate_pass=n/a
- **FCLR-LIQ-010-CONFIRM-20261113T063000Z** (experiment): verdict=NOT_REPLICATED; gate_pass=n/a
- **FCLR-LIQ-COMBINED-20261115T181449Z** (experiment): failed gate criteria: ci_pass, rel_pass
- **FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T073346Z** (experiment): verdict=INCONCLUSIVE; gate_pass=n/a
- **FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z** (experiment): verdict=INCONCLUSIVE; gate_pass=n/a
- **FCLR-LIQ-XSEC-ORDERING-20261115T200813Z** (experiment): failed gate criteria: rel_pass
- **FCLR-LIQ-XSEC-ORDERING-20261115T203501Z** (experiment): failed gate criteria: rel_pass
- **FCLR-LIQ-XSEC-QLIKE-20261115T214903Z** (experiment): failed gate criteria: block_pass, ci_pass, rel_pass
- **FCLR-POWER-CALIBRATION-2026-11-15T01:34:12Z** (experiment): verdict=INCONCLUSIVE; gate_pass=n/a
- **H1_primary** (hypothesis): evidence flags: 2% floor, blocks, ci crosses, instruments, zero
- **H2_shek_replication** (hypothesis): evidence flags: holm, materiality
- **H_contagion_funding** (hypothesis): no gate passed; sealed
- **H_contagion_liq** (hypothesis): no gate passed; sealed
- **H_fclr_exp_robust_redo** (hypothesis): evidence flags: bootstrap, loio, materiality, permutation, placebo, zero
- **H_fclr_fwd_vol_011_confirm** (hypothesis): evidence flags: loio, placebo, zero
- **H_fclr_fwd_vol_2024q4_cross** (hypothesis): evidence flags: blocks, holm, instruments, loio, materiality, placebo, zero
- **H_fclr_fwd_vol_2025_cross** (hypothesis): evidence flags: blocks, instruments, loio, materiality, placebo, zero
- **H_fclr_fwd_vol_2025h2_cross** (hypothesis): evidence flags: blocks, holm, instruments, loio, materiality, placebo, zero
- **H_fclr_fwd_vol_2025q1q2_cross** (hypothesis): evidence flags: 2% floor, blocks, holm, instruments, loio, materiality, placebo, zero
- **H_fclr_liq_010_confirm** (hypothesis): evidence flags: instruments, loio, materiality, permutation, placebo, zero
- **H_fclr_liq_combined_panel_forecast** (hypothesis): evidence flags: blocks
- **H_fclr_liq_xsec_ordering_forecast** (hypothesis): forecast gate NOT_MET
- **H_fclr_liq_xsec_qlike_forecast** (hypothesis): forecast gate NOT_MET
- **H_fclr_panelfe_001** (hypothesis): forecast gate NOT_MET
- **H_fclr_session_synthesis_01** (hypothesis): no gate passed; sealed
- **H_fclr_xsec_001** (hypothesis): forecast gate NOT_MET
- **H_fclr_xsec_002** (hypothesis): no gate passed; sealed
- **H_fclr_xsec_003** (hypothesis): no gate passed; sealed
- **H_fclr_xsec_004** (hypothesis): no gate passed; sealed
- **H_fclr_xsec_005** (hypothesis): no gate passed; sealed
- **H_fclr_xsec_006** (hypothesis): no gate passed; sealed
- **H_fclr_xsec_007** (hypothesis): forecast gate NOT_MET
- **H_fclr_xsec_008** (hypothesis): forecast gate NOT_MET
- **H_liq_oos_funding_conditioned_forecast** (hypothesis): evidence flags: blocks, bootstrap, holm, materiality, zero
- **H_tracka_hl_alt_volatility_forecast** (hypothesis): evidence flags: blocks, zero
- **H_tracka_hl_early_liquidation_forecast** (hypothesis): evidence flags: blocks, instruments, materiality, zero
- **H_tracka_hl_expansion_recompute** (hypothesis): evidence flags: blocks, holm, instruments, loio, placebo
- **H_tracka_hl_expansion_robustness** (hypothesis): evidence flags: bootstrap, loio, permutation, placebo
- **H_tracka_hl_funding_conditioned_volatility_forecast** (hypothesis): evidence flags: holm
- **H_tracka_hl_funding_conditioned_volatility_fullhistory** (hypothesis): forecast gate NOT_MET
- **H_tracka_hl_liquidation_cross_sectional_funding** (hypothesis): evidence flags: permutation
- **H_tracka_hl_liquidation_forecast** (hypothesis): evidence flags: blocks, instruments
- **H_tracka_hl_symbol_expansion_liquidation_forecast** (hypothesis): evidence flags: blocks, instruments
- **H_trackb_modeled_breaches** (hypothesis): evidence flags: blocks, bootstrap, degenerate, holm, inadmissible, materiality, zero
- **TRACKA-HL-EARLY-4H-20261112T054737Z** (experiment): failed gate criteria: ci_excludes_zero_better, materiality_ge_2pct, min_test_blocks_ge_3
- **TRACKA-HL-EARLY4H-2025H1** (experiment): verdict=unknown; gate_pass=n/a
- **TRACKA-HL-EARLY4H-2025H1-LIQ-GLM** (experiment): failed gate criteria: ci_upper_below_zero, holm_pass, materiality_ge_2pct, single_coin_only
- **TRACKA-HL-EARLY4H-2025H1-LIQ-GLM-ROBUST** (experiment): failed gate criteria: ci_upper_below_zero, holm_pass, single_coin_only
- **TRACKA-LIQ-XSEC-20261112T201536Z** (experiment): verdict=EXPLORATORY_NULL; gate_pass=n/a
- **TRACKA-LIQ-XSEC-FORWARD-20261113T222859Z** (experiment): verdict=EXPLORATORY_NULL; gate_pass=n/a
- **TRACKA-VOL-20261111T234918Z** (experiment): verdict=NOT_MET; gate_pass=n/a
- **TRACKA-VOL-FORWARD-2026Q1Q2-20261114T015222Z** (experiment): verdict=EXPLORATORY_NULL; gate_pass=n/a
- **TRACKA-VOL-FULLHIST-20261112T201536Z** (experiment): verdict=NOT_MET; gate_pass=n/a
- **alt_source_probe_audit_20261112T191400Z** (source_probe_audit): no candidate met §5/§16 minima (≥5 instruments, ≥1 complete month or ≥3×30d blocks, unauthenticated, provenance/license, observed labels only, venue-consistent)
- **evaluation_summary_FCLR-SHEK-SCALE-20261115T071135Z** (experiment): verdict=unknown; gate_pass=n/a
- **evaluation_summary_FCLR-SHEK-SCALE-20261115T144938Z** (experiment): verdict=unknown; gate_pass=n/a
- **evaluation_summary_FCLR-SHEK-SCALE-SENS-20261115T144938Z** (experiment): verdict=unknown; gate_pass=n/a
- **evaluation_summary_TRACKA-ALT-VOL-20261112T020322Z** (experiment): failed gate criteria: ci_excludes_zero, overall
- **evaluation_summary_TRACKA-EXP-ROBUST-20261112T015119Z** (experiment): verdict=FRAGILE; gate_pass=n/a
- **terminal_structural_stop_liq_glm_robust_20261112T170457Z** (sealed_verdict): terminal structural stop; gate failed on statistical evidence

## §17 condition detail (all not met)

- **FCLR-011-INDEPENDENT-RECOMPUTE-20261114T042139Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-DESIGN-FEASIBILITY-20261115T021249Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-EXP-ROBUST-REDO-20261113T063000Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-FWD-VOL-011-CONFIRM-20261113T041200Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-FWD-VOL-2024-DISJOINT-2024-06-20261114T231100Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-FWD-VOL-2024Q4-CROSS-20261113T091500Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-FWD-VOL-2025-CROSS-20261113T063000Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T183000Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-FWD-VOL-2025H2-CROSS-20261113T102139Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-FWD-VOL-2025Q1Q2-CROSS-20261113T111601Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-LIQ-010-CONFIRM-20261113T063000Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-LIQ-COMBINED-20261115T181449Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T073346Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-LIQ-EXPANSION-RECONCILIATION-20261114T083642Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-LIQ-XSEC-ORDERING-20261115T200813Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-LIQ-XSEC-ORDERING-20261115T203501Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-LIQ-XSEC-QLIKE-20261115T214903Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **FCLR-POWER-CALIBRATION-2026-11-15T01:34:12Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H1_primary**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H2_shek_replication**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_contagion_funding**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_contagion_liq**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_exp_robust_redo**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_fwd_vol_011_confirm**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_fwd_vol_2024q4_cross**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_fwd_vol_2025_cross**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_fwd_vol_2025h2_cross**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_fwd_vol_2025q1q2_cross**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_liq_010_confirm**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_liq_combined_panel_forecast**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_liq_xsec_ordering_forecast**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_liq_xsec_qlike_forecast**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_panelfe_001**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_session_synthesis_01**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_xsec_001**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_xsec_002**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_xsec_003**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_xsec_004**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_xsec_005**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_xsec_006**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_xsec_007**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_fclr_xsec_008**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_liq_oos_funding_conditioned_forecast**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_tracka_hl_alt_volatility_forecast**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_tracka_hl_early_liquidation_forecast**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_tracka_hl_expansion_recompute**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_tracka_hl_expansion_robustness**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_tracka_hl_funding_conditioned_volatility_forecast**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_tracka_hl_funding_conditioned_volatility_fullhistory**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_tracka_hl_liquidation_cross_sectional_funding**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_tracka_hl_liquidation_forecast**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_tracka_hl_symbol_expansion_liquidation_forecast**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_trackb_modeled_breaches**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **TRACKA-HL-EARLY-4H-20261112T054737Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **TRACKA-HL-EARLY4H-2025H1**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **TRACKA-HL-EARLY4H-2025H1-LIQ-GLM**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **TRACKA-HL-EARLY4H-2025H1-LIQ-GLM-ROBUST**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **TRACKA-LIQ-XSEC-20261112T201536Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **TRACKA-LIQ-XSEC-FORWARD-20261113T222859Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **TRACKA-VOL-20261111T234918Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **TRACKA-VOL-FORWARD-2026Q1Q2-20261114T015222Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **TRACKA-VOL-FULLHIST-20261112T201536Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **alt_source_probe_audit_20261112T191400Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **evaluation_summary_FCLR-SHEK-SCALE-20261115T071135Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **evaluation_summary_FCLR-SHEK-SCALE-20261115T144938Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **evaluation_summary_FCLR-SHEK-SCALE-SENS-20261115T144938Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **evaluation_summary_TRACKA-ALT-VOL-20261112T020322Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **evaluation_summary_TRACKA-EXP-ROBUST-20261112T015119Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **terminal_structural_stop_liq_glm_robust_20261112T170457Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False

## Input artifacts (sha256, for determinism audit)

- alt_source_probe_audit_20261112T191400Z.json sha256=7cf6ce072323a9dd1badf910bb311d44baf268f6ae1aed3e5686fdae6c862df6
- evaluation_summary_EARLY4H-2025H1-20261112T134536Z.json sha256=fdc0910657b5fa09f6f2fe1b867a49f3dc79166693c31ddee1c4b16c104db57e
- evaluation_summary_EARLY4H-2025H1-20261112T134536Z.md sha256=70ebce28e60f24bac19bc969c24cca2932d9d0d1f24049c54770397e2efee535
- evaluation_summary_EARLY4H-2025H1-20261112T134634Z.json sha256=351867b9f9ba29f026961e9ce178c07caede54e96b9f4c1cc36af0d5a81731fe
- evaluation_summary_EARLY4H-2025H1-20261112T134634Z.md sha256=be0bfe9fb541d357ddde7c02ad948b22620cc89cc8d0ec44e4333f44c31aa18d
- evaluation_summary_EARLY4H-2025H1-20261112T145537Z.json sha256=01aed1f0bc7e510a82865383fa640f46619b87c7a8d405befefb8ae912a49c3a
- evaluation_summary_EARLY4H-2025H1-20261112T145537Z.md sha256=35c3d6a8c8c7f24d12a26f7f18c49c38bd847320fa160de85b573414ac0d8c2b
- evaluation_summary_EARLY4H-2025H1-LIQ-GLM-20261112T164926Z.json sha256=49c8ddd3ccb34814f737cdc555d77166ec19fd8bb3b6758f0ca5c6920aa34ce6
- evaluation_summary_EARLY4H-2025H1-LIQ-GLM-20261112T164926Z.md sha256=4f8fc1cf359940b117751bf3291e5ca4e7a58953cf3a42a31abbf8da323927dd
- evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-20261112T170457Z.json sha256=7f1f7edb5c2e1b1857645957876f4fdca72d2204b2728ff8df6dd6a413e2c04a
- evaluation_summary_EARLY4H-2025H1-LIQ-GLM-ROBUST-20261112T170457Z.md sha256=daaca437ab369ffc010cd7455abfa25155020ee3546417bec9be92b1c26c8939
- evaluation_summary_FCLR-008.md sha256=9d31db9dea8a68ae4e8fc5324ffe1c3a248db4adc260396e89439d710bf3b6a2
- evaluation_summary_FCLR-009.md sha256=1b7e1113ce4815473217b9baefac3a3d96ccbf82fbdae83f0f8a0905321c0a0f
- evaluation_summary_FCLR-011-RECOMPUTE-20261115T234700Z.json sha256=25b1f324f05dfc53586525d5137551575e1a770b33349fe7c44da885d4aea8ca
- evaluation_summary_FCLR-011-RECOMPUTE-20261115T234700Z.md sha256=0f66359b56e814d6b5805eb1b9824ebadf0dde2276a38b122b77abe6e79a3c6e
- evaluation_summary_FCLR-011-RECOMPUTE-20261115T235000Z.json sha256=0f2a23ca0a7cb8f2111471c60e91221a7fbfd198ad89df148878376c73bc34e3
- evaluation_summary_FCLR-011-RECOMPUTE-20261115T235000Z.md sha256=d0c537f7de55ff002cb1e95e74450fcef87c688ec3d8746b52f99ef3f16540c9
- evaluation_summary_FCLR-011.md sha256=a83977e5518871ab03c141fce2bce42c287bb522ed7d49638c005559b1ef58cc
- evaluation_summary_FCLR-011_20261103T111743Z.md sha256=b8e38a2c2b2061e1dd5182022c7999ee2d5d5671bc4df635c8dcce5adb9c0105
- evaluation_summary_FCLR-012-V.md sha256=cadb163e9db6f4b72a02cd0b513947546c5e13ba92b5ee7df3ae9b407efc4933
- evaluation_summary_FCLR-013.md sha256=107bc981ebb6f519205b42f94ce778e14b445036f4758995914dabb0ef6bd08a
- evaluation_summary_FCLR-014.md sha256=e308cd622c88981be134bcb1ad576b3d25f0b4df251c3c9fb3768b630ffa53ff
- evaluation_summary_FCLR-COUPLED-001-ROBUST.md sha256=b6d6e91c3d2d2fbb981e3d5c981afa426d9123ac5892fb25d8745d187f9e6c20
- evaluation_summary_FCLR-COUPLED-001.md sha256=e3b50793c576bb14221ad31c68ef871247082972e889763b3e8c12aa6e2643a4
- evaluation_summary_FCLR-DESIGN-FEASIBILITY-2026-11-15T02:35:00Z.json sha256=e1a6620c7072fa495c5d23b14e9e8c0d3ad8fff7763bfbd624ffcf18ba035c1b
- evaluation_summary_FCLR-DESIGN-FEASIBILITY-2026-11-15T02:35:00Z.md sha256=384d4125cfdddcf72b72468ae12ed5fda99182cb1e7f294b2b1ecb5f0ba2a56c
- evaluation_summary_FCLR-EXP-ROBUST-REDO-20261113T071229Z.json sha256=0fdd08b4e66b1feb9f40fbc40e4ebcfc705aef648a61bab431f3252f033cde65
- evaluation_summary_FCLR-EXP-ROBUST-REDO-20261113T071229Z.md sha256=82fcb9e637037474f8113e3a23de9db4343689a6f93219ffd561e397b6eaf46a
- evaluation_summary_FCLR-EXP-ROBUST-REDO-20261113T080456Z.json sha256=508c93d28b70e3cf0c1aa077ba3c227f9e7b8996a83e5dbbf29320f50e7e9cbc
- evaluation_summary_FCLR-EXP-ROBUST-REDO-20261113T080456Z.md sha256=c871b3530ba7493c92584a9d6642c2733ad6d43e4105928890aea33dbac3db67
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041259Z.json sha256=e0f646f778e51109ae4aa06eea0e34d92fb55e7525b26a20975ed9995ad36eac
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041259Z.md sha256=3fc2b5bdca2116353662eef72b56e97b9f394a11522ed4fdfd5fac780505ce8d
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041401Z.json sha256=47bdd0beb99dcf287ab9aac3258fc01084399103d7cd145926ccb8bdef7fe4c6
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041401Z.md sha256=febb3b28842f00479bc7543f2ecadba50e9cf126e7412dde00c9d00e96bc1c9c
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041459Z.json sha256=1f25e7469429132c4efe275aadaaaf2e33510ec33abc063e9f12fdac8d71fa86
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041459Z.md sha256=1c515f3c1d3ee99272c63eff4eafa995b7099aa97885cb30bea2ad18d3a88ef0
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041543Z.json sha256=273c87d829e2c5d406435497406bbef377e9937a318a3cf065b84b93b3cb014b
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041543Z.md sha256=a221fc165265b54b948a307d091e8d8c601616c178c2a9ba4db486e038cc05b2
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041630Z.json sha256=f853686271204ce52588c662761d49c4e3c06ad447fc551640f2dd36998aa522
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041630Z.md sha256=3ee24eac32374d0073de9f5fd7db666380bbb33a5162d5c0f02acd35d34071d8
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041731Z.json sha256=3603ffe8e79c1c79b8fca8542a7859de5e67d4ee09d1b37b57efe3613a6154c5
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041731Z.md sha256=aeae2807be04d22af62f8e747ded9b1d5a132dc16bbd1f7d9fd27489a6f7a3f1
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041934Z.json sha256=49d843183724c00c8f896c2842fce06edfc647e5eaa8ed85c6e5fc1925783c0f
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T041934Z.md sha256=c8badb4587ca2932792ee39bb1350597fb51b4fab971e1ed1630ddaf9400c0f0
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T050407Z.json sha256=587b1961861edc846ca012ad4c3fe282915332fc79946e44b11179f1f5f2b0f7
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T050407Z.md sha256=1580f6a037ac980905a23ba00ce34d441303b433004c77f69d33ba232989be81
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T061005Z.json sha256=f5900d681b238c41860c593952bd88cea01f5c8977bc609bb9073920ea85b6ec
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T061005Z.md sha256=616bbb9ad0a2d1e10ed96aa8aa7e6ba7555ccd37fea7f4bd1fb1c186429e2d2d
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T061555Z.json sha256=1a06abd7099714028674b246919cf2488048f09625eb0fc63920395e17e786b0
- evaluation_summary_FCLR-FWD-VOL-011-CONFIRM-20261113T061555Z.md sha256=a422847c97c417b76263b12ba5717ba791b5515efe6bd5df631ceeaa36a93e95
- evaluation_summary_FCLR-FWD-VOL-2024-DISJOINT-2024-06-20261114T231100Z_20261114T231545Z.json sha256=7fee65a723b4242b02fdb8a5c6e290af4bc2a6cee9ad216a2577125789cef8c1
- evaluation_summary_FCLR-FWD-VOL-2024-DISJOINT-2024-06-20261114T231100Z_20261114T231545Z.md sha256=d68e7c1b03933c5a942deba75704358255bf7a2fdd46b3633d54c225fe80016e
- evaluation_summary_FCLR-FWD-VOL-2024Q4-CROSS-20261113T100451Z.json sha256=7122075ecf8d4af2e38d65b8bdbc0ce35c8955112eb8bb0e4f8f986aacfe8746
- evaluation_summary_FCLR-FWD-VOL-2024Q4-CROSS-20261113T100451Z.md sha256=cb907e13d20d591362c8b5e8b66be620d7b8029de223b8400daaab72c9513fee
- evaluation_summary_FCLR-FWD-VOL-2025-CROSS-20261113T081147Z.json sha256=59eb18b427ff77e9a56a745baded5c3ca5700f086fed445ab2602a2c442defbd
- evaluation_summary_FCLR-FWD-VOL-2025-CROSS-20261113T081147Z.md sha256=8abe3eb84c93fdb943be8a51944e3b2b51ef3763d78c5577745ab6d21de67378
- evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z.json sha256=b829fbe90a6da05f55f4be0821716ab802494452390eb867d29ee281a64d569b
- evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CORRECTED-AUDIT-2026-11-15T00:12:56Z.md sha256=10c673687d3869c04a6bf862d07578e31e37d3eb7c1f575df1afab5baf26a038
- evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T191615Z.json sha256=78537585fe59ed4a75d7861a80bf3964e35c97a6a53c48a39c6d012354e69215
- evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-CROSS-20261114T191615Z.md sha256=139ab2faa9b24a93b0d958e7cbd0619c76bb46990e6b6f0816d25887e78245e4
- evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z.json sha256=a4d9410f0d44359c01dec9434afcea808c9cc172395f58019ecbcbfa6098f3e6
- evaluation_summary_FCLR-FWD-VOL-2025-DISJOINT-RECONCILE-20261114T193000Z.md sha256=f8c6d5718ed1ab54fd5f6f7eb40bc597201d624ce0130349a0d77a926ed01f2c
- evaluation_summary_FCLR-FWD-VOL-2025H2-CROSS-20261113T102240Z.json sha256=cc230583703a40bb53042fc3e3b8f0db65d0109094550c95fa6c992275d995f8
- evaluation_summary_FCLR-FWD-VOL-2025H2-CROSS-20261113T102240Z.md sha256=0838f216844e8582a4bcd64c48716f953222a0df47db735ae1a204dd18ef22a7
- evaluation_summary_FCLR-FWD-VOL-2025Q1Q2-CROSS-20261113T111712Z.json sha256=f081641df36c5c31f85f436d042e0d1bc641662e6bdabf20bb51979486932cf8
- evaluation_summary_FCLR-FWD-VOL-2025Q1Q2-CROSS-20261113T111712Z.md sha256=04f177d1504a2914022f87d1ed566f81d326756e1727ea0eb2317e082d658f65
- evaluation_summary_FCLR-H003-EXT-001.md sha256=6aa6f68f1baf2ca7c0e99716513c777c6ac9e6999ef47c1c7b18fbd15531b9cc
- evaluation_summary_FCLR-LIQ-010-CONFIRM-20261113T065953Z.json sha256=183edb1633de50555d0833e072920574b9e4877026ce6555998bb546dcd23d78
- evaluation_summary_FCLR-LIQ-010-CONFIRM-20261113T065953Z.md sha256=11d30c3a33ca4ecffe9933bbdf40d7a14db471ac47ed71ce2be57b305de9642a
- evaluation_summary_FCLR-LIQ-COMBINED-20261115T185844Z.json sha256=a613574dde3846948ff85870dcb5655b27ecafb739947315720daef7d9da264f
- evaluation_summary_FCLR-LIQ-COMBINED-20261115T185844Z.md sha256=c7ecb98b24d2f5b03e0cdd10cddcb2605a7a638de4e37c31dcd81825efa29ec6
- evaluation_summary_FCLR-LIQ-XSEC-ORDERING-20261115T201101Z.json sha256=f91c1b2cb5d2e7e5d3e52384ee56fe36d56f829497b873591c97f774dbc06597
- evaluation_summary_FCLR-LIQ-XSEC-ORDERING-20261115T201101Z.md sha256=8bd27d2d7ffb163a69f611986c019101b2f7fbf9274cd59720e5d433fa039506
- evaluation_summary_FCLR-LIQ-XSEC-ORDERING-20261115T203507Z.json sha256=1c1144e0d1224ba760c02e3ddc24b0230aff82287a88674404c421437df5aa40
- evaluation_summary_FCLR-LIQ-XSEC-ORDERING-20261115T203507Z.md sha256=22a113dc4b42f8b60077745dd7898cd28d1c0cd9973ee2ea09691a0d93c77613
- evaluation_summary_FCLR-LIQ-XSEC-QLIKE-20261115T214949Z.json sha256=37c7e5485d99a00cd2cc10d482c9c13cef219a735dceaeb14d93fc15240cd5a0
- evaluation_summary_FCLR-LIQ-XSEC-QLIKE-20261115T214949Z.md sha256=b11a5a94145eb74e48ade61f4e39af56850aa9e75e725dc5ce0413dc5c763d4a
- evaluation_summary_FCLR-LIQMICRO-001.md sha256=17a01e325b25368af4235c4d6184bcabeea166b06c13a11a1590515602e3d90d
- evaluation_summary_FCLR-LIQMICRO-002.md sha256=a09df21d6145a80df16850f1625858f71c93226d3bc1a77afd6314c6cd29fd01
- evaluation_summary_FCLR-POWER-CALIBRATION-2026-11-15T01:34:12Z.json sha256=90a9cb219e9c2c7d348e53f60c79e265ddaa746a5755aeb74111a11ac4594d4d
- evaluation_summary_FCLR-POWER-CALIBRATION-2026-11-15T01:34:12Z.md sha256=1b66057e6db7f0ad1e250d78361e22b94d1941fc97eeb0ff1e96c00f4b5fe98f
- evaluation_summary_FCLR-SHEK-SCALE-20261115T071135Z.json sha256=cabdb1e06c0fc34b9873afc072d28cbb713370d97fd88280d73d86e5687fcfa0
- evaluation_summary_FCLR-SHEK-SCALE-20261115T071135Z.md sha256=3c04080d127863daea20bcf4394980e9bb7b9d8e766e53249b49d86da3c7dafd
- evaluation_summary_FCLR-SHEK-SCALE-20261115T144938Z.json sha256=1f43d37d053b64fd39182acec3a606bdd6831c9171baaa8065703057f85c4bef
- evaluation_summary_FCLR-SHEK-SCALE-20261115T144938Z.md sha256=f7287c8740fb099395975d25f29936d0f81510c4b076f290204955e7b96612de
- evaluation_summary_FCLR-SHEK-SCALE-SENS-20261115T144938Z.json sha256=3cb9ee471d99018cda354f9bdb2a8fb09350eb0117cc71e3f575f8bc2c6afd8c
- evaluation_summary_FCLR-SHEK-SCALE-SENS-20261115T144938Z.md sha256=ded04ab9af71a2a7466b339a72e1f5b9c81615b90552d0166c09b048d733e977
- evaluation_summary_FCLR002.md sha256=cbf5c42205c7177de4eb52be3d5296e0f02ca994007c653ff6469b920cacb46b
- evaluation_summary_FCLR002_REPRO.md sha256=344dd24dc699e866331d8f19733719aafc51af0f7e07bea60abccdcd9e14307c
- evaluation_summary_FCLR003.md sha256=a623d098caaa01404dcef22bd703eb2476a63f4602b789c81c4d56fa688f9ec2
- evaluation_summary_FCLR005.md sha256=881fb1d7adae29e3943d0feeec939595de82eaabe8405b732c7b43de1e8219fc
- evaluation_summary_FCLR006.md sha256=be6f749786628e455909e29891dc7535bf7f6ca55344b4cfcac18b55999f545b
- evaluation_summary_FCLR007.md sha256=ed34935e512247034ef4192af007bcd8c6cb4672e0fcfc9cd4b6a833be32ef40
- evaluation_summary_FCLR010.md sha256=8b7773b2d7eff3663be4fa975e75095c5406f27c5bcf096988935fad0871a334
- evaluation_summary_STREAM_B_DEEP_ANALYSIS-001_20261109T162703Z.md sha256=9d1c7660fda4286267b0242ea6ce1acc6867b1b7984c5f3021a1ff26c43e81ca
- evaluation_summary_STREAM_B_DEEP_ANALYSIS-002_20261109T163517Z.md sha256=42df57ac371c5c46084943f0fde200fa5b5bd5bfddea466a7ea86a9f4b155a31
- evaluation_summary_TRACKA-ALT-VOL-20261112T020322Z.json sha256=1c141a4798b7ad7941db9e8360708d8bb553caf64974e4c703cfae13b9b6287a
- evaluation_summary_TRACKA-ALT-VOL-20261112T020322Z.md sha256=844261592c227fd2a6e832e5be078dc2c74baaf257e9ad5db7027e21c4fd1bc2
- evaluation_summary_TRACKA-EXP-ROBUST-20261112T014744Z.md sha256=76de26de15905e88bec41b60a38946cc171559bdd4b86aa15e550c661bbcbde9
- evaluation_summary_TRACKA-EXP-ROBUST-20261112T015119Z.json sha256=12ed11af799f9047696f8d02397dd08883d135cc930c14086472014578692769
- evaluation_summary_TRACKA-EXP-ROBUST-20261112T015119Z.md sha256=e0d1cff1362f7e85f634fb17ef39c7f2dc0ed28279f436f62a65200da64121bc
- evaluation_summary_TRACKA-HL-20261111T145835Z.md sha256=89678d80e2bffcf5449d3b85300a49e7941ac90e7db009f5fe417344c10015a7
- evaluation_summary_TRACKA-HL-20261111T160124Z.md sha256=856f6b5379dba8da79114da96f67b755600e871cc07df43d883a37c645a8f5a9
- evaluation_summary_TRACKA-HL-20261111T201852Z.md sha256=b41c02dfe8e0f819d9ddc0a337236bdc6eab28f8da5a55bd4bfcdff1ed70283b
- evaluation_summary_TRACKA-HL-EARLY-4H-20261112T054737Z.json sha256=114641edda020bcfb54c50ee8ffd4b7e7d388f72733ea8e95447d9e42153b5cf
- evaluation_summary_TRACKA-HL-EARLY-4H-20261112T054737Z.md sha256=377a8d24a3f516b42b04f652cec99f3e64bfe392042c5b5f71c753416321eeaf
- evaluation_summary_TRACKA-HL-early-infeasible-20261111T193500Z.md sha256=c9715c2ef11a246098ee44f66db00cace674fec196a806c36896c30508c2c920
- evaluation_summary_TRACKA-HL-expansion-20261111T202344Z.md sha256=73dbe8b54b08c71144ac009cfd080d272e3c1e81f2895faea034f73c15813f43
- evaluation_summary_TRACKA-HL-terminal-20261111T133430Z.md sha256=2ab8f5a441b0112c2630589b15250c30e1f6b5182d5d09de5553dc8d7fd5b33a
- evaluation_summary_TRACKA-LIQ-EXPANSION-RECOMPUTE-20261114T083000Z.json sha256=58b2ae2326e7358080cc073f7f98eb74b8f6e02c36a0329e06f1b5bf92fe2272
- evaluation_summary_TRACKA-LIQ-EXPANSION-RECOMPUTE-20261114T083000Z.md sha256=31f210b7dad7d51b7c6431cc4774d99b49f0a84c07523affeafee22c1a7523fd
- evaluation_summary_TRACKA-LIQ-EXPANSION-RECONCILIATION-20261114T112451Z.json sha256=c5362baa4fc88669c31a75b4a04a45f840e236103927bbbc74e9d596ff1d06af
- evaluation_summary_TRACKA-LIQ-EXPANSION-RECONCILIATION-20261114T112451Z.md sha256=c8db0b1c7d51b11df65510d8ae35be71ee3a78924941a96563c907d7bfed292a
- evaluation_summary_TRACKA-LIQ-EXPANSION-RECONCILIATION-20261114T112620Z.json sha256=c2facbeb1ce1d28e20dd523451ac029bfa3dddf09637b42cf4ebbf89d24bb61f
- evaluation_summary_TRACKA-LIQ-EXPANSION-RECONCILIATION-20261114T112620Z.md sha256=7a0c8e18d9be80f57ff5da4e0ab4abf4c6e54860c6fd6625d293747bb2b0c83b
- evaluation_summary_TRACKA-LIQ-EXPANSION-RECONCILIATION-20261114T113226Z.json sha256=f9b476dd483c0de39ca32ca110c1197c660cc6f3355076ae9db1dea0c9686eba
- evaluation_summary_TRACKA-LIQ-EXPANSION-RECONCILIATION-20261114T113226Z.md sha256=917c7de36ca2e70b9c3cf123b87dea78b779d80be3679c338dc3b173315b0676
- evaluation_summary_TRACKA-LIQ-XSEC-2026-11-13T00:33:08Z.json sha256=35d7c3614e565bb8b94047fdd851b4661356c00834bee633293d788eeeb90267
- evaluation_summary_TRACKA-LIQ-XSEC-2026-11-13T00:33:08Z.md sha256=fd9c039a850cf7db59e9930dcd17c5d74382bb25d2f6e24c1216e76bc0b8d0e9
- evaluation_summary_TRACKA-LIQ-XSEC-2026-11-13T20:24:18Z.json sha256=82578f44e9c485b8d85a21014743cce2384e0c63db3176939ba9709373d412ff
- evaluation_summary_TRACKA-LIQ-XSEC-2026-11-13T20:24:18Z.md sha256=f77dd5c561d8355ba442f47b88bc505743795318475f2a0f3962cf75a293d4b1
- evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-2026-11-13T22:31:55Z.json sha256=3b94f07361ef2fc59de6bdf4534d587ddb5d0752a905d1d8591a134d451ac5f1
- evaluation_summary_TRACKA-LIQ-XSEC-FORWARD-2026-11-13T22:31:55Z.md sha256=3ca6a481277e08826338eaa3e2b4869a10a4835d0abebf51ee68ee4fc9222041
- evaluation_summary_TRACKA-VOL-20261111T234918Z.json sha256=8943044c08e315c01df425160a946ca2b824ef7566db4354b9542e76bde79362
- evaluation_summary_TRACKA-VOL-20261111T234918Z.md sha256=1f76257f809b4c44225a97740c1a5e0de878e57939f6700c18ee862320ca1ff6
- evaluation_summary_TRACKA-VOL-FAMILY-20261112T005111Z.md sha256=92cbc6adc6dc5b749d955763e9be232a1831dd9d828c11ad0229aff9f9e3247b
- evaluation_summary_TRACKA-VOL-FORWARD-2026-11-14T02:33:29Z.json sha256=746f3adddade3e2626dd5837ca49889d15a554fdb7ab60aa5316a4e6b2af9d32
- evaluation_summary_TRACKA-VOL-FORWARD-2026-11-14T02:33:29Z.md sha256=aa1d011d255101a59d36281958938ef8af1430fafc8a5a0c07550a2c32d969d0
- evaluation_summary_TRACKA-VOL-FORWARD-2026-11-14T02:43:53Z.json sha256=63b5a5656a3a119c90e1e8f277635b9be22eeaab948e93cbc124aa46ebabcf43
- evaluation_summary_TRACKA-VOL-FORWARD-2026-11-14T02:43:53Z.md sha256=f0a7abd483bfcc19e597d6c60171a8d96f76b41d98304cc8e3740e0f7c36e379
- evaluation_summary_TRACKA-VOL-FORWARD-2026-11-14T02:45:26Z.json sha256=ec2b6f956859b0fb02c6e39f005b1525b4c93289f8f596415641dbc4f6425ddb
- evaluation_summary_TRACKA-VOL-FORWARD-2026-11-14T02:45:26Z.md sha256=dae41dd0300fbdd331a2a7bb5c5d29fcd4d4d3d71ae7a27fe3052c5e1fcd4e00
- evaluation_summary_TRACKA-VOL-FORWARD-2026-11-14T03:30:40Z.json sha256=24636d80b460233ce10cafd6109d78d6e2a6c55a2491215b97162a0415338712
- evaluation_summary_TRACKA-VOL-FORWARD-2026-11-14T03:30:40Z.md sha256=15183e2026689eb97445d76a84c0125707b446718dcf206e359d64a437ea03c4
- evaluation_summary_TRACKA-VOL-FULLHIST-2026-11-13T02:44:48Z.json sha256=a38c61d1d8ec5599a0bb31ba6dbf19ed61a1ce31d12c6371f4a140655d15ba37
- evaluation_summary_TRACKA-VOL-FULLHIST-2026-11-13T02:44:48Z.md sha256=e9d487cf2a286e2a80de1584947f9996e03246879ec8d29422ce5662da07dcdd
- evaluation_summary_funding.md sha256=d20128b3658cd8fa6d2814a0fa0e53ec3608698a432191fb8ce0b0d0403c147d
- evaluation_summary_funding_explor_5sym.md sha256=b94d885dbd74fcb9d6453fbcf227dc7bac3e2b0208f5ce27c9808c439b7d41b4
- evaluation_summary_funding_repro.md sha256=5d46600d1a02d2c1aa8f29376ceb2f94d0b0190fd179c4ac60c132409a84ef99
- evaluation_summary_funding_v2_5sym.md sha256=7d4a0bb630e571544888d79c9eda1b539f1fc8a5021ed508c11f092513a05e88
- evaluation_summary_funding_v3_30d.md sha256=774e4a9f85205116cbdab4e3bfa71d57e84f07e8d2bd21fc31056c4e080573f5
- evaluation_summary_funding_v3_30d_exploratory_v4.md sha256=704017ac4b5e36c0a2802d3bfc4eda6a3e28c9b99ed5a9eeca53764841dee3c9
- evaluation_summary_funding_v4_exploratory_30d.md sha256=cec0a4ad28d2016cff5f747be51a08ce9a83f37adabb8a0630c4aee0e4ac87f4
- evaluation_summary_h003.md sha256=851b26135894b459c6de36e96d52ad731ee45dd15164e93e85133c6abf9cf3b7
- evaluation_summary_h003_FCLR002.md sha256=4da5b3b07b4d9783e52f606da7458d9f7fffd23b7404d172c1ee63f1911cbb37
- evaluation_summary_tracka_overlay_001.md sha256=f2143a09ab5e1271b6afdccf895c21f3ed92422072a262654fdbbfcf3f49513f
- evaluation_summary_trackb_20251110T154307Z.md sha256=f8a01e2c9977a185b59680029906e85ddbd42737df219c3f77ed7931af3659b2
- evaluation_summary_trackb_TB1_20261110T173838Z.md sha256=d65a8a305332ee8cb0a60284758ca7fdb823b2a69631bff542aad75150ca2ae2
- evaluation_summary_trackb_TB2_20261110T190405Z.md sha256=9f0b0c45d2952f60cfb90eb8fe9b601b806c091518d3f61c4b3c2e09359e38eb
- experiment_frontier.json sha256=e57fd7447db108515c36630de1e9af303cdcbade651a74aca83d4155d422b14e
- hypothesis_registry.json sha256=5df67f842554daa8dc52ed0e4671138a49a4fb841614f6664fc22d58cc2c9df1
- terminal_structural_stop_liq_glm_robust_20261112T170457Z.md sha256=f5105524def72a0063670bed7430b335d38e3204692edf60740fc202aa203ae2

## Determinism note
Same inputs -> byte-identical output except `generated_utc`. Generated offline; no estimators, fetches, probes, or discovery executed.
