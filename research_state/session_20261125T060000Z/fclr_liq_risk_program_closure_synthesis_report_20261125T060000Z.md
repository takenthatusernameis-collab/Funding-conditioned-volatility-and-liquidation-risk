# FCLR-LIQ-RISK-PROGRAM-CLOSURE-02 — Negative-Results Synthesis Report

**experiment_id:** FCLR-LIQ-RISK-PROGRAM-CLOSURE-02
**session_id:** session_20261125T060000Z
**session_utc:** 20261125T060000Z
**generated_utc:** 2026-11-25T06:00:00Z
**campaign_id:** FCLR-LIQ-RISK-PROGRAM-CLOSURE-02-20261125T054500Z

## Basis

Synthesized exclusively from frozen on-disk experiment artifacts (source registries, preregs, evals, recomputes, evidence audits) under `research_state/session_*/`. No heavy evaluations re-run.

## Verdict table — Half 1: Funding-conditioned volatility (all closed NOT_SUPPORTED)

| Estimand | Verdict | Materiality vs 2% floor | Session | Forecasts/Events |
|---|---|---|---|---|
| FCLR-VOL-BROAD-01 mean log-RV QLIKE | NOT_SUPPORTED | 1.93% < 2% | session_20261124T120000Z | 684,301 / 23 blocks |
| FCLR-VOL-CORR-01 correction-time/hazard | NOT_SUPPORTED | >=10% slower-correction floor NOT met | session_20261124T204500Z | 227,023 events |
| FCLR-VOL-STRESS-01 stress/tail-exceedance | NOT_SUPPORTED | 1.51% < 2% | session_20261124T222500Z | 1,393,204 / 63,059 stress |
| FCLR-VOL-JUMP-01 jump magnitude | NOT_SUPPORTED | 0.0922% < 2% | session_20261125T030000Z | 1,136,222 / 39,116 jump |
| FCLR-VOL-JUMP-02 leakage-hardened jump magnitude | NOT_SUPPORTED | 0.1510% < 2%; null survives full leakage remediation | session_20261125T034400Z | 30,284 / 1,388 jump |
| FCLR-VOL-JUMP-03 multi-estimator x multi-horizon jump magnitude | NOT_SUPPORTED | aggregate 0.3025% < 2%; null survives bipower vs threshold-bipower AND {24h,48h} | session_20261125T045000Z | 87,162 / 4,235 jump |
| FCLR-VOL-JUMP-04 directional/sign jump | NOT_SUPPORTED | aggregate 0.0474% / <=0.1020% best-config < 2%; null survives full leakage remediation + estimator/horizon variation | session_20261125T054500Z | 110,914 / 57,354 downside-dominance |

## Verdict table — Half 2: Liquidation risk (confirmatory-exhausted)

| Track / estimand | Verdict | Basis |
|---|---|---|
| Track A observed liquidation-event forecasting | STRUCTURALLY_BLOCKED | capped-sample feed; no complete observed-liquidation source; NEW_OBSERVED_LIQUIDATION_SOURCE cannot fire on frozen data |
| Track B modeled hypothetical boundary-breach forecast | NOT_SUPPORTED | modeled proxy does not reconstruct account-specific liquidation mechanics |
| Track C volatility/stress outcome from mark-price history | NOT_SUPPORTED | no arm cleared frozen materiality floor |
| Cross-sectional regime-conditioned funding -> liquidation-intensity | SUPPORTED_GENERALIZATION but NOT_STABLE | 2% Poisson-deviance floor NOT MET; section 17 condition #4 fails |

## Overall verdict

Program closure. All confirmatory paths exhausted on the frozen `ironflow_bulk` panel. The honest endpoint is closure + negative-results preservation.

`negative_results_preserved: true` | `all_nulls_honest: true` | `no_threshold_shop: true` | `no_overlay: true` | `audit_pass: true` | `unresolved_blockers: []`
