# Program Terminal Structural Closure — FCLR_FINAL_STRUCTURAL_CLOSURE_AND_REOPEN_CONDITIONS

**Generated (UTC):** 2026-11-12T21:20:43Z
**Program status:** CLOSED_TERMINAL
**Terminal verdict:** NO_CLAIM_WORTHY_RESULT_PROMOTABLE; ALL_P1_P2_P3_SEALED
**Rows enumerated:** 18
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
| H1_primary | hypothesis | NOT_SUPPORTED | forecast_gate_NOT_MET | forecast_gate_NOT_MET | False | NOT_SUPPORTED | GATE4_BRANCH_1,NEW_OBSERVED_LIQUIDATION_SOURCE |
| H2_shek_replication | hypothesis | EXPLORATORY_ONLY | PARTIAL (direction reproduced, not statistically significant) | PARTIAL (direction reproduced, not statistically significant) | False | EXPLORATORY_ONLY | — |
| H_tracka_hl_alt_volatility_forecast | hypothesis | NOT_MET | forecast_gate_NOT_MET | forecast_gate_NOT_MET | False | NOT_MET | GATE4_BRANCH_1,NEW_OBSERVED_LIQUIDATION_SOURCE |
| H_tracka_hl_early_liquidation_forecast | hypothesis | INCONCLUSIVE_PILOT_SHORTFALL | inconclusive_pilot_shortfall | inconclusive_pilot_shortfall | False | INCONCLUSIVE_PILOT_SHORTFALL | NEW_OBSERVED_LIQUIDATION_SOURCE,HL_LABEL_EXTENSION |
| H_tracka_hl_expansion_robustness | hypothesis | FRAGILE | robustness_gate_FRAGILE | robustness_gate_FRAGILE | False | FRAGILE | EXPANSION_ROBUSTNESS_REDO |
| H_tracka_hl_funding_conditioned_volatility_forecast | hypothesis | NOT_MET | forecast_gate_NOT_MET | forecast_gate_NOT_MET | False | NOT_MET | GATE4_BRANCH_1,NEW_OBSERVED_LIQUIDATION_SOURCE |
| H_tracka_hl_liquidation_forecast | hypothesis | NOT_MET | forecast_gate_NOT_MET | forecast_gate_NOT_MET | False | NOT_MET | NEW_OBSERVED_LIQUIDATION_SOURCE,HL_LABEL_EXTENSION |
| H_tracka_hl_symbol_expansion_liquidation_forecast | hypothesis | SUPPORTED_PASS_PRIMARY_GATE | forecast_gate_PASS | forecast_gate_PASS | False | SUPPORTED_PASS_PRIMARY_GATE | NEW_OBSERVED_LIQUIDATION_SOURCE,HL_LABEL_EXTENSION |
| H_trackb_modeled_breaches | hypothesis | NOT_SUPPORTED | forecast_gate_NOT_MET | forecast_gate_NOT_MET | False | NOT_SUPPORTED | — |
| TRACKA-HL-EARLY-4H-20261112T054737Z | experiment | INCONCLUSIVE_PILOT_SHORTFALL | INCONCLUSIVE_PILOT_SHORTFALL | INCONCLUSIVE_PILOT_SHORTFALL | False | INCONCLUSIVE_PILOT_SHORTFALL | — |
| TRACKA-HL-EARLY4H-2025H1 | experiment | unknown | unknown | unknown | False | unknown | — |
| TRACKA-HL-EARLY4H-2025H1-LIQ-GLM | experiment | INCONCLUSIVE_NUMERICAL_INSTABILITY | INCONCLUSIVE_NUMERICAL_INSTABILITY | INCONCLUSIVE_NUMERICAL_INSTABILITY | False | INCONCLUSIVE_NUMERICAL_INSTABILITY | — |
| TRACKA-HL-EARLY4H-2025H1-LIQ-GLM-ROBUST | experiment | NOT_MET | NOT_MET | NOT_MET | False | NOT_MET | NEW_OBSERVED_LIQUIDATION_SOURCE,HL_LABEL_EXTENSION |
| TRACKA-VOL-20261111T234918Z | experiment | NOT_MET | NOT_MET | NOT_MET | False | NOT_MET | — |
| alt_source_probe_audit_20261112T191400Z | source_probe_audit | NO_ADMISSIBLE_SOURCE | NO_GO | all probed families NO-GO | False | NO_ADMISSIBLE_SOURCE | NEW_OBSERVED_LIQUIDATION_SOURCE |
| evaluation_summary_TRACKA-ALT-VOL-20261112T020322Z | experiment | NOT_MET | NOT_MET | NOT_MET | False | NOT_MET | — |
| evaluation_summary_TRACKA-EXP-ROBUST-20261112T015119Z | experiment | FRAGILE | FRAGILE | FRAGILE | False | FRAGILE | — |
| terminal_structural_stop_liq_glm_robust_20261112T170457Z | sealed_verdict | TERMINAL_STRUCTURAL_STOP | NOT_MET** | NOT_MET** | False | TERMINAL_STRUCTURAL_STOP | — |

## Failing minima (per row)

- **H1_primary** (hypothesis): evidence flags: 2% floor, blocks, zero
- **H2_shek_replication** (hypothesis): no gate passed; sealed
- **H_tracka_hl_alt_volatility_forecast** (hypothesis): evidence flags: blocks, zero
- **H_tracka_hl_early_liquidation_forecast** (hypothesis): evidence flags: blocks, instruments, materiality, zero
- **H_tracka_hl_expansion_robustness** (hypothesis): evidence flags: bootstrap, loio, permutation, placebo
- **H_tracka_hl_funding_conditioned_volatility_forecast** (hypothesis): evidence flags: holm
- **H_tracka_hl_liquidation_forecast** (hypothesis): evidence flags: blocks, instruments
- **H_tracka_hl_symbol_expansion_liquidation_forecast** (hypothesis): evidence flags: blocks, instruments
- **H_trackb_modeled_breaches** (hypothesis): evidence flags: blocks, bootstrap, degenerate, holm, inadmissible, materiality, zero
- **TRACKA-HL-EARLY-4H-20261112T054737Z** (experiment): failed gate criteria: ci_excludes_zero_better, materiality_ge_2pct, min_test_blocks_ge_3
- **TRACKA-HL-EARLY4H-2025H1** (experiment): verdict=unknown; gate_pass=n/a
- **TRACKA-HL-EARLY4H-2025H1-LIQ-GLM** (experiment): failed gate criteria: ci_upper_below_zero, holm_pass, materiality_ge_2pct, single_coin_only
- **TRACKA-HL-EARLY4H-2025H1-LIQ-GLM-ROBUST** (experiment): failed gate criteria: ci_upper_below_zero, holm_pass, single_coin_only
- **TRACKA-VOL-20261111T234918Z** (experiment): verdict=NOT_MET; gate_pass=n/a
- **alt_source_probe_audit_20261112T191400Z** (source_probe_audit): no candidate met §5/§16 minima (≥5 instruments, ≥1 complete month or ≥3×30d blocks, unauthenticated, provenance/license, observed labels only, venue-consistent)
- **evaluation_summary_TRACKA-ALT-VOL-20261112T020322Z** (experiment): failed gate criteria: ci_excludes_zero, overall
- **evaluation_summary_TRACKA-EXP-ROBUST-20261112T015119Z** (experiment): verdict=FRAGILE; gate_pass=n/a
- **terminal_structural_stop_liq_glm_robust_20261112T170457Z** (sealed_verdict): terminal structural stop; gate failed on statistical evidence

## §17 condition detail (all not met)

- **H1_primary**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H2_shek_replication**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_tracka_hl_alt_volatility_forecast**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_tracka_hl_early_liquidation_forecast**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_tracka_hl_expansion_robustness**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_tracka_hl_funding_conditioned_volatility_forecast**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_tracka_hl_liquidation_forecast**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_tracka_hl_symbol_expansion_liquidation_forecast**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **H_trackb_modeled_breaches**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **TRACKA-HL-EARLY-4H-20261112T054737Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **TRACKA-HL-EARLY4H-2025H1**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **TRACKA-HL-EARLY4H-2025H1-LIQ-GLM**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **TRACKA-HL-EARLY4H-2025H1-LIQ-GLM-ROBUST**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **TRACKA-VOL-20261111T234918Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
- **alt_source_probe_audit_20261112T191400Z**: data_and_label_gates_pass=False, frozen_oos_beats_baseline_on_primary_target=False, materiality_floor_and_multiplicity_uncertainty_pass=False, skill_not_dominated_by_one_coin_venue_brief_crisis_block=False, calibration_and_subgroup_diagnostics_acceptable=False, independent_recomputation_reproduces_headline_within_tolerance=False, red_team_and_leakage_audits_show_no_unresolved_issue=False
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
- evaluation_summary_FCLR-011.md sha256=a83977e5518871ab03c141fce2bce42c287bb522ed7d49638c005559b1ef58cc
- evaluation_summary_FCLR-011_20261103T111743Z.md sha256=b8e38a2c2b2061e1dd5182022c7999ee2d5d5671bc4df635c8dcce5adb9c0105
- evaluation_summary_FCLR-012-V.md sha256=cadb163e9db6f4b72a02cd0b513947546c5e13ba92b5ee7df3ae9b407efc4933
- evaluation_summary_FCLR-013.md sha256=107bc981ebb6f519205b42f94ce778e14b445036f4758995914dabb0ef6bd08a
- evaluation_summary_FCLR-014.md sha256=e308cd622c88981be134bcb1ad576b3d25f0b4df251c3c9fb3768b630ffa53ff
- evaluation_summary_FCLR-COUPLED-001-ROBUST.md sha256=b6d6e91c3d2d2fbb981e3d5c981afa426d9123ac5892fb25d8745d187f9e6c20
- evaluation_summary_FCLR-COUPLED-001.md sha256=e3b50793c576bb14221ad31c68ef871247082972e889763b3e8c12aa6e2643a4
- evaluation_summary_FCLR-H003-EXT-001.md sha256=6aa6f68f1baf2ca7c0e99716513c777c6ac9e6999ef47c1c7b18fbd15531b9cc
- evaluation_summary_FCLR-LIQMICRO-001.md sha256=17a01e325b25368af4235c4d6184bcabeea166b06c13a11a1590515602e3d90d
- evaluation_summary_FCLR-LIQMICRO-002.md sha256=a09df21d6145a80df16850f1625858f71c93226d3bc1a77afd6314c6cd29fd01
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
- evaluation_summary_TRACKA-VOL-20261111T234918Z.json sha256=8943044c08e315c01df425160a946ca2b824ef7566db4354b9542e76bde79362
- evaluation_summary_TRACKA-VOL-20261111T234918Z.md sha256=1f76257f809b4c44225a97740c1a5e0de878e57939f6700c18ee862320ca1ff6
- evaluation_summary_TRACKA-VOL-FAMILY-20261112T005111Z.md sha256=92cbc6adc6dc5b749d955763e9be232a1831dd9d828c11ad0229aff9f9e3247b
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
- experiment_frontier.json sha256=f359b20630cbb8791398c16e43fe0a02add336eada181666149a3b7c28f816b8
- hypothesis_registry.json sha256=ddb0bc84d2fcdb3b79589125b277c99c90ed4445741d4a8123906de321709288
- terminal_structural_stop_liq_glm_robust_20261112T170457Z.md sha256=f5105524def72a0063670bed7430b335d38e3204692edf60740fc202aa203ae2

## Determinism note
Same inputs -> byte-identical output except `generated_utc`. Generated offline; no estimators, fetches, probes, or discovery executed.
