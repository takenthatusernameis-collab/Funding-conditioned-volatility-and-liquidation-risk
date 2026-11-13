# Evaluation Summary — TRACKA-VOL-FULLHIST-2026-11-13T02:44:48Z
**Generated (UTC):** 2026-11-13T02:44:48Z
**Campaign:** `FCLR-FULLHISTORY-VOL-LIQ-20261112T201536Z` — Arm A (P1, primary)
**Prereg:** `research_state/prereg_tracka_vol_fullhist_20261112T201536Z.json` (frozen 2026-11-12T20:15:36Z, `outcome_data_inspected_before_freeze=false`)
**Panel:** `research_state/tracka_vol_fullhist_panel_2026-11-13T02:44:48Z.parquet`
**Verdict:** `NOT_MET`

## Primary contrast (T24, C2 vs B1, QLIKE, pooled test blocks 0/1/2)
- QLIKE(B1) = 5.80836949, QLIKE(C2) = 5.73929722
- diff = QLIKE(C2) - QLIKE(B1) = -0.06907227
- relative reduction = 1.1892% (floor 2.0%)
- 95% block-bootstrap CI = [-0.08084497, -0.05756497] (block 168h, 2000 reps, seed 20261112)
- p_value (bootstrap sign, two-sided) = 0.000000
- Holm (12-comparison primary family): rank 4, alpha_adj 0.005556, rejected = True
- n_pairs = 16560, instruments = 10, test blocks = 3
## Full 12-comparison primary family (Holm, alpha 0.05)
| Horizon | Contrast | QLIKE_base | QLIKE_alt | diff | rel_reduction_pct | 95% CI | p_value | Holm rejected |
| 6h | C2_vs_B1 | 7.491016 | 7.414241 | -0.076775 | 1.0249% | [-0.089461, -0.064094] | 0.000000 | True |
| 6h | C1_vs_B1 | 7.491016 | 7.441946 | -0.049069 | 0.6550% | [-0.056521, -0.041694] | 0.000000 | True |
| 6h | C2_vs_C1 | 7.441946 | 7.414241 | -0.027705 | 0.3723% | [-0.035854, -0.019200] | 0.000000 | True |
| 24h | C2_vs_B1 | 5.808369 | 5.739297 | -0.069072 | 1.1892% | [-0.080845, -0.057565] | 0.000000 | True |
| 24h | C1_vs_B1 | 5.808369 | 5.764635 | -0.043735 | 0.7530% | [-0.050614, -0.037066] | 0.000000 | True |
| 24h | C2_vs_C1 | 5.764635 | 5.739297 | -0.025338 | 0.4395% | [-0.032405, -0.017868] | 0.000000 | True |
| 72h | C2_vs_B1 | 4.549343 | 4.475421 | -0.073921 | 1.6249% | [-0.084696, -0.062915] | 0.000000 | True |
| 72h | C1_vs_B1 | 4.549343 | 4.503616 | -0.045726 | 1.0051% | [-0.052930, -0.038621] | 0.000000 | True |
| 72h | C2_vs_C1 | 4.503616 | 4.475421 | -0.028195 | 0.6261% | [-0.034218, -0.021882] | 0.000000 | True |
| 168h | C2_vs_B1 | 3.641541 | 3.575138 | -0.066403 | 1.8235% | [-0.076301, -0.056532] | 0.000000 | True |
| 168h | C1_vs_B1 | 3.641541 | 3.598147 | -0.043394 | 1.1916% | [-0.050161, -0.036686] | 0.000000 | True |
| 168h | C2_vs_C1 | 3.598147 | 3.575138 | -0.023009 | 0.6395% | [-0.028279, -0.017567] | 0.000000 | True |

## Secondary OI family (8 cells, separate Holm, NOT promotable)
| Horizon | Contrast | QLIKE_base | QLIKE_alt | diff | rel_reduction_pct | 95% CI | p_value | Holm rejected |
| 6h | B2_vs_B1 | 7.491016 | 7.542754 | 0.051739 | -0.6907% | [0.010660, 0.092710] | 0.019000 | False |
| 6h | C3_vs_B1 | 7.491016 | 7.438199 | -0.052817 | 0.7051% | [-0.101581, -0.004324] | 0.033000 | False |
| 24h | B2_vs_B1 | 5.808369 | 5.860809 | 0.052440 | -0.9028% | [0.010563, 0.094234] | 0.019000 | False |
| 24h | C3_vs_B1 | 5.808369 | 5.763702 | -0.044667 | 0.7690% | [-0.094356, 0.004345] | 0.083000 | False |
| 72h | B2_vs_B1 | 4.549343 | 4.594232 | 0.044889 | -0.9867% | [0.002143, 0.086904] | 0.041000 | False |
| 72h | C3_vs_B1 | 4.549343 | 4.503027 | -0.046315 | 1.0181% | [-0.093657, 0.000847] | 0.054000 | False |
| 168h | B2_vs_B1 | 3.641541 | 3.688798 | 0.047256 | -1.2977% | [0.002038, 0.091551] | 0.042000 | False |
| 168h | C3_vs_B1 | 3.641541 | 3.604607 | -0.036934 | 1.0142% | [-0.085847, 0.012064] | 0.157000 | False |

## Per-block primary (T24, C2 vs B1)
- block 0: QLIKE_B1=5.893864, QLIKE_C2=5.826360, rel_reduction=1.1453%, n=5520
- block 1: QLIKE_B1=5.597816, QLIKE_C2=5.519613, rel_reduction=1.3970%, n=5520
- block 2: QLIKE_B1=5.933429, QLIKE_C2=5.871919, rel_reduction=1.0367%, n=5520

## Per-coin primary (T24, C2 vs B1)
- BTC: rel_reduction=0.7682%, QLIKE_B1=6.334915, QLIKE_C2=6.286249, n=1656
- ETH: rel_reduction=1.1643%, QLIKE_B1=5.812846, QLIKE_C2=5.745169, n=1656
- SOL: rel_reduction=1.4774%, QLIKE_B1=5.587343, QLIKE_C2=5.504797, n=1656
- HYPE: rel_reduction=0.4450%, QLIKE_B1=5.304753, QLIKE_C2=5.281147, n=1656
- ENA: rel_reduction=1.4963%, QLIKE_B1=5.509831, QLIKE_C2=5.427390, n=1656
- WLD: rel_reduction=1.7429%, QLIKE_B1=5.800646, QLIKE_C2=5.699548, n=1656
- FARTCOIN: rel_reduction=1.1665%, QLIKE_B1=6.401888, QLIKE_C2=6.327213, n=1656
- TRUMP: rel_reduction=1.1627%, QLIKE_B1=6.056912, QLIKE_C2=5.986486, n=1656
- NEAR: rel_reduction=1.2609%, QLIKE_B1=5.578295, QLIKE_C2=5.507956, n=1656
- XRP: rel_reduction=1.2157%, QLIKE_B1=5.696265, QLIKE_C2=5.627017, n=1656

## LOIO primary (T24, C2 vs B1, train without left-out coin)
- without BTC: rel_reduction=0.8601%, QLIKE_B1=6.383661, QLIKE_C2=6.328758, n=1656
- without ETH: rel_reduction=1.1769%, QLIKE_B1=5.770529, QLIKE_C2=5.702617, n=1656
- without SOL: rel_reduction=1.7171%, QLIKE_B1=5.548955, QLIKE_C2=5.453672, n=1656
- without HYPE: rel_reduction=0.3954%, QLIKE_B1=5.312856, QLIKE_C2=5.291850, n=1656
- without ENA: rel_reduction=1.1944%, QLIKE_B1=5.600836, QLIKE_C2=5.533942, n=1656
- without WLD: rel_reduction=1.8773%, QLIKE_B1=5.900268, QLIKE_C2=5.789504, n=1656
- without FARTCOIN: rel_reduction=0.4093%, QLIKE_B1=6.676194, QLIKE_C2=6.648868, n=1656
- without TRUMP: rel_reduction=1.0925%, QLIKE_B1=6.017209, QLIKE_C2=5.951471, n=1656
- without NEAR: rel_reduction=1.3006%, QLIKE_B1=5.567000, QLIKE_C2=5.494595, n=1656
- without XRP: rel_reduction=1.3437%, QLIKE_B1=5.657199, QLIKE_C2=5.581185, n=1656

## Placebo/permutation (funding features shuffled within train hour, 500 reps, seed 20261112)
- observed diff T24 = -0.06907227
- null 95th percentile = -0.02932036
- p_value (two-sided) = 0.0
## Section 17 promotion criteria
- 1_data_label_gates_pass: True
- 2_frozen_oos_beats_rv_baseline: False
- 3_materiality_and_multiplicity: False
- 4_not_dominated_coin_block_crisis: True
- 5_calibration_subgroup_acceptable: True
- 6_recomputation_from_hashes: True
- 7_red_team_leakage_audit: True
- notes: {"4_per_coin_rel_reduction_pct": {"BTC": 0.7682310554466314, "ETH": 1.1642663172728462, "SOL": 1.4773798299018766, "HYPE": 0.4449922770997055, "ENA": 1.4962556273775622, "WLD": 1.7428723019762804, "FARTCOIN": 1.1664522051865396, "TRUMP": 1.1627405493590597, "NEAR": 1.2609376433441781, "XRP": 1.2156716588152423}, "4_per_block_rel_reduction_pct": {"block_0": 1.145328486810777, "block_1": 1.3970255842350996, "block_2": 1.0366650086183227}, "6_manifest_objects_verified": 42, "7_max_panel_t": "2026-01-10 23:00:00+00:00"}
## Decision rule
- primary_gate_pass = False; conditions = {"min_paired_instruments_ge_5": true, "min_test_blocks_ge_3": true, "materiality_rel_reduction_ge_2pct": false, "ci_excludes_zero_in_favor_of_C2": true, "holm_significant_t24": true}
- verdict = NOT_MET
- NOT_MET failing minima: rel_reduction=1.1892% (floor 2.0%), CI=[-0.08084497, -0.05756497], Holm rejected=False
