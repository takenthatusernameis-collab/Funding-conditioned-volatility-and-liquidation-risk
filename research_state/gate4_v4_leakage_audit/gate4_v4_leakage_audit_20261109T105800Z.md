# Gate 4 v4 EXPLORATORY leakage audit — 20261109T105800Z

**EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE**
- Git SHA: `8f5a3827b0d1f6a04d2eb56eb5d16d96b929f4de`
- Prereg: `research_state/pre_registration_gate4_funding_multisplit_v4_20261107T1845Z.json` — `FROZEN_BEFORE_OUTCOMES`, `confirmatory_claim_go=NO_GO`
- No confirmatory claim, no economic value, no promotion. Audit of leakage controls only.
- Verifies train-only provenance of ridge scale, winsor bounds, target floor, normalization stats; and block-bootstrap CI reproducibility with fixed seed.

## Train-only parameter provenance (test-fold perturbation invariance)
| Variant | Split | Symbol | n_train | test_perturbation_unchanged | changed_keys |
|---|---:|---|---:|---:|---|
| V1_primary | 0 | BTCUSDT | 888 | True | - |
| V1_primary | 0 | ETHUSDT | 888 | True | - |
| V1_primary | 0 | SOLUSDT | 888 | True | - |
| V1_primary | 0 | XRPUSDT | 888 | True | - |
| V1_primary | 0 | BNBUSDT | 888 | True | - |
| V1_primary | 1 | BTCUSDT | 1608 | True | - |
| V1_primary | 1 | ETHUSDT | 1608 | True | - |
| V1_primary | 1 | SOLUSDT | 1608 | True | - |
| V1_primary | 1 | XRPUSDT | 1608 | True | - |
| V1_primary | 1 | BNBUSDT | 1608 | True | - |
| V1_primary | 2 | BTCUSDT | 2328 | True | - |
| V1_primary | 2 | ETHUSDT | 2328 | True | - |
| V1_primary | 2 | SOLUSDT | 2328 | True | - |
| V1_primary | 2 | XRPUSDT | 2328 | True | - |
| V1_primary | 2 | BNBUSDT | 2328 | True | - |
| V1_primary | 3 | BTCUSDT | 3048 | True | - |
| V1_primary | 3 | ETHUSDT | 3048 | True | - |
| V1_primary | 3 | SOLUSDT | 3048 | True | - |
| V1_primary | 3 | XRPUSDT | 3048 | True | - |
| V1_primary | 3 | BNBUSDT | 3048 | True | - |
| V2_scale_ridge | 0 | BTCUSDT | 888 | True | - |
| V2_scale_ridge | 0 | ETHUSDT | 888 | True | - |
| V2_scale_ridge | 0 | SOLUSDT | 888 | True | - |
| V2_scale_ridge | 0 | XRPUSDT | 888 | True | - |
| V2_scale_ridge | 0 | BNBUSDT | 888 | True | - |
| V2_scale_ridge | 1 | BTCUSDT | 1608 | True | - |
| V2_scale_ridge | 1 | ETHUSDT | 1608 | True | - |
| V2_scale_ridge | 1 | SOLUSDT | 1608 | True | - |
| V2_scale_ridge | 1 | XRPUSDT | 1608 | True | - |
| V2_scale_ridge | 1 | BNBUSDT | 1608 | True | - |
| V2_scale_ridge | 2 | BTCUSDT | 2328 | True | - |
| V2_scale_ridge | 2 | ETHUSDT | 2328 | True | - |
| V2_scale_ridge | 2 | SOLUSDT | 2328 | True | - |
| V2_scale_ridge | 2 | XRPUSDT | 2328 | True | - |
| V2_scale_ridge | 2 | BNBUSDT | 2328 | True | - |
| V2_scale_ridge | 3 | BTCUSDT | 3048 | True | - |
| V2_scale_ridge | 3 | ETHUSDT | 3048 | True | - |
| V2_scale_ridge | 3 | SOLUSDT | 3048 | True | - |
| V2_scale_ridge | 3 | XRPUSDT | 3048 | True | - |
| V2_scale_ridge | 3 | BNBUSDT | 3048 | True | - |
| V3_scale_ridge_target_floor | 0 | BTCUSDT | 888 | True | - |
| V3_scale_ridge_target_floor | 0 | ETHUSDT | 888 | True | - |
| V3_scale_ridge_target_floor | 0 | SOLUSDT | 888 | True | - |
| V3_scale_ridge_target_floor | 0 | XRPUSDT | 888 | True | - |
| V3_scale_ridge_target_floor | 0 | BNBUSDT | 888 | True | - |
| V3_scale_ridge_target_floor | 1 | BTCUSDT | 1608 | True | - |
| V3_scale_ridge_target_floor | 1 | ETHUSDT | 1608 | True | - |
| V3_scale_ridge_target_floor | 1 | SOLUSDT | 1608 | True | - |
| V3_scale_ridge_target_floor | 1 | XRPUSDT | 1608 | True | - |
| V3_scale_ridge_target_floor | 1 | BNBUSDT | 1608 | True | - |
| V3_scale_ridge_target_floor | 2 | BTCUSDT | 2328 | True | - |
| V3_scale_ridge_target_floor | 2 | ETHUSDT | 2328 | True | - |
| V3_scale_ridge_target_floor | 2 | SOLUSDT | 2328 | True | - |
| V3_scale_ridge_target_floor | 2 | XRPUSDT | 2328 | True | - |
| V3_scale_ridge_target_floor | 2 | BNBUSDT | 2328 | True | - |
| V3_scale_ridge_target_floor | 3 | BTCUSDT | 3048 | True | - |
| V3_scale_ridge_target_floor | 3 | ETHUSDT | 3048 | True | - |
| V3_scale_ridge_target_floor | 3 | SOLUSDT | 3048 | True | - |
| V3_scale_ridge_target_floor | 3 | XRPUSDT | 3048 | True | - |
| V3_scale_ridge_target_floor | 3 | BNBUSDT | 3048 | True | - |
| V4_winsor_train | 0 | BTCUSDT | 888 | True | - |
| V4_winsor_train | 0 | ETHUSDT | 888 | True | - |
| V4_winsor_train | 0 | SOLUSDT | 888 | True | - |
| V4_winsor_train | 0 | XRPUSDT | 888 | True | - |
| V4_winsor_train | 0 | BNBUSDT | 888 | True | - |
| V4_winsor_train | 1 | BTCUSDT | 1608 | True | - |
| V4_winsor_train | 1 | ETHUSDT | 1608 | True | - |
| V4_winsor_train | 1 | SOLUSDT | 1608 | True | - |
| V4_winsor_train | 1 | XRPUSDT | 1608 | True | - |
| V4_winsor_train | 1 | BNBUSDT | 1608 | True | - |
| V4_winsor_train | 2 | BTCUSDT | 2328 | True | - |
| V4_winsor_train | 2 | ETHUSDT | 2328 | True | - |
| V4_winsor_train | 2 | SOLUSDT | 2328 | True | - |
| V4_winsor_train | 2 | XRPUSDT | 2328 | True | - |
| V4_winsor_train | 2 | BNBUSDT | 2328 | True | - |
| V4_winsor_train | 3 | BTCUSDT | 3048 | True | - |
| V4_winsor_train | 3 | ETHUSDT | 3048 | True | - |
| V4_winsor_train | 3 | SOLUSDT | 3048 | True | - |
| V4_winsor_train | 3 | XRPUSDT | 3048 | True | - |
| V4_winsor_train | 3 | BNBUSDT | 3048 | True | - |

**All train-derived parameters invariant to test perturbation: True**

## Per-row leakage diagnosis rollup by source artifact (refusal-first)

- leakage_rollup_rules_version: `1.0`
- Per-row diagnosis derived only from explicit saved/computed audit fields (test_perturbation_unchanged, changed_keys, status). Never infers degenerate/inference_ok; never fabricates claimability.
| source_artifact | total_rows | train_params_invariant | leakage_signal | insufficient_data | indeterminate | leakage_detected | detection_refused |
|---|---:|---:|---:|---:|---:|---:|---:|
| gate4_v4_leakage_audit_20261109T105800Z.json | 80 | 80 | 0 | 0 | 0 | 0 | 0 |

## Block-bootstrap reproducibility (fixed seed 20261109, two independent runs)
| Metric | Run 1 | Run 2 | Identical | eff_blocks | ci_valid | regime_flags |
|---|---:|---:|---:|---:|---:|---|
| point | 0.4879023125557301 | 0.4879023125557301 | True | 120 | True | ok |
| ci_low | -0.05470664399824281 | -0.05470664399824281 | True | 120 | True | ok |
| ci_high | 1.1856151857495267 | 1.1856151857495267 | True | 120 | True | ok |
| n_obs | 12969 | 12969 | True | 120 | True | ok |
| n_blocks | 120 | 120 | True | 120 | True | ok |
| effective_block_count | 120 | 120 | True | - | - | - |
| ci_accounting_valid | True | True | True | - | - | - |
| regime_flags | ok | ok | True | - | - | - |

**Block-bootstrap CI identical on rerun: True**
**Additive diagnostics identical on rerun: True**
**CI accounting valid: True**
**Effective blocks: 120**
**Regime flags: ok**

## Additive bootstrap diagnostics (serialized for leakage audit)
| Diagnostic | Run 1 | Run 2 | Identical |
|---|---:|---:|---:|
| effective_block_count | 120 | 120 | True |
| ci_accounting_valid | True | True | True |
| degenerate | False | False | True |
| inference_ok | True | True | True |
| n_reps_effective | 2000 | 2000 | True |
| n_obs_finite | 12969 | 12969 | True |
| regime_flags | ok | ok | True |

## Interpretation (EXPLORATORY ONLY — NOT CONFIRMATORY)
Train-only provenance: True — every train-derived parameter (ridge scale, winsor bounds, target floor, normalization mean/std) is unchanged when the test fold is perturbed; no test-derived statistic enters training parameters. Block-bootstrap reproducibility: True — fixed seed yields identical CIs across independent runs (deterministic inference). Additive diagnostics reproducible: True — effective_block_count/regime_flags/ci_accounting_valid are serialized in JSON+MD and identical on rerun. **Leakage audit PASS (EXPLORATORY diagnostic, not confirmatory):** Gate 4 v4 leakage controls hold on the local 2024-04..09 slice; block-bootstrap inference is deterministic and reproducible.

Artifacts: `research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T105800Z.json`, `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/gate4_v4_leakage_audit/gate4_v4_leakage_audit_20261109T105800Z.md`
