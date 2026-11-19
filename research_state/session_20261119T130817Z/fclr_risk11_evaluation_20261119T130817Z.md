# FCLR-RISK-11 Evaluation Report
Campaign: `FCLR-LIQ-RISK-ESCALATION-11-20261119T120000Z`
Session UTC: `20261119T130817Z`

## Verdict: `NOT_MET-with-bound`
Power status: `UNDERPOWERED` | models_run: `False`
Plausible effect (Brier): `0.001` | Smallest defensible effect: `0.002817725360790807`

## Member verdicts (block_3 primary)
- funding_x_rv: NOT_MET
- funding_x_oi: NOT_MET
- rv_x_oi: NOT_MET
- three_way: NOT_MET
- funding_spline: NOT_MET
- decile_regime: NOT_MET

## Per-block per-member results
### block_2 (n_test=27443)
| member | brier | log_loss | auc | brier_improvement | p_raw | p_holm | placebo_p | placebo_p95 |
|---|---|---|---|---|---|---|---|---|
| funding_x_rv | 0.150937 | 0.479240 | 0.560308866364508 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
| funding_x_oi | 0.150937 | 0.479240 | 0.560308866364508 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
| rv_x_oi | 0.150937 | 0.479240 | 0.560308866364508 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
| three_way | 0.150937 | 0.479240 | 0.560308866364508 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
| funding_spline | 0.150937 | 0.479240 | 0.560308866364508 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
| decile_regime | 0.150937 | 0.479240 | 0.560308866364508 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
### block_3 (n_test=28379)
| member | brier | log_loss | auc | brier_improvement | p_raw | p_holm | placebo_p | placebo_p95 |
|---|---|---|---|---|---|---|---|---|
| funding_x_rv | 0.141731 | 0.457792 | 0.5731222820259988 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
| funding_x_oi | 0.141731 | 0.457792 | 0.5731222820259988 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
| rv_x_oi | 0.141731 | 0.457792 | 0.5731222820259988 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
| three_way | 0.141731 | 0.457792 | 0.5731222820259988 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
| funding_spline | 0.141731 | 0.457792 | 0.5731222820259988 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
| decile_regime | 0.141731 | 0.457792 | 0.5731222820259988 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
### pooled (n_test=55822)
| member | brier | log_loss | auc | brier_improvement | p_raw | p_holm | placebo_p | placebo_p95 |
|---|---|---|---|---|---|---|---|---|
| funding_x_rv | 0.146225 | 0.468238 | 0.5690448672828688 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
| funding_x_oi | 0.146225 | 0.468238 | 0.5690448672828688 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
| rv_x_oi | 0.146225 | 0.468238 | 0.5690448672828688 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
| three_way | 0.146225 | 0.468238 | 0.5690448672828688 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
| funding_spline | 0.146225 | 0.468238 | 0.5690448672828688 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |
| decile_regime | 0.146225 | 0.468238 | 0.5690448672828688 | 0.000000 | 1.0 | 1.0 | 1.000000 | 0.000000 |

## MDE by instrument count
Full table in `fclr_risk11_power_20261119T130817Z.json` (`mde_by_instrument_count`).
Full instrument count (13 coins): block_3 mde_brier_80pct = 0.003886; pooled = 0.002818

## Recompute integrity
n_discrepancies = 0; panel_sha256 = 0448a56a676eaadc7094d0e42a6b90a5f407a80502da0da74e5141547725e7d9

## Prohibitions honored
No RISK-09/RISK-10 replay; no sealed Binance months; no post-hoc metric addition; no ingest/alignment re-run; no zero-byte artifacts; no outcome mining; no family slimming.
