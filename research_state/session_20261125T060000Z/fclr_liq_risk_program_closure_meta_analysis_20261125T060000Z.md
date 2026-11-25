# FCLR-LIQ-RISK-PROGRAM-CLOSURE-02 — Quantitative Meta-Analysis

**experiment_id:** FCLR-LIQ-RISK-PROGRAM-CLOSURE-02
**session_id:** session_20261125T060000Z
**session_utc:** 20261125T060000Z
**generated_utc:** 2026-11-25T06:00:00Z
**campaign_id:** FCLR-LIQ-RISK-PROGRAM-CLOSURE-02-20261125T054500Z
**multiplicity_method:** Holm familywise-error across declared experiment family
**alpha:** 0.05
**family_size:** 11

## Declared experiment family (all confirmatory arms across both halves)

| # | Estimand | Track | Verdict | Rel. improvement | Floor | Floor met? | p (nominal) | p (Holm adj.) | Holm rejected? |
|---|---|---|---|---|---|---|---|---|---|
| 1 | FCLR-VOL-BROAD-01 mean log-RV QLIKE | Half 1 volatility | NOT_SUPPORTED | 1.93% | 2% | No | 1.0 | 1.0 | No |
| 2 | FCLR-VOL-CORR-01 correction-time/hazard | Half 1 volatility | NOT_SUPPORTED | n/a | 10% | No | 1.0 | 1.0 | No |
| 3 | FCLR-VOL-STRESS-01 stress/tail-exceedance | Half 1 volatility | NOT_SUPPORTED | 1.51% | 2% | No | 1.0 | 1.0 | No |
| 4 | FCLR-VOL-JUMP-01 jump magnitude | Half 1 volatility | NOT_SUPPORTED | 0.0922% | 2% | No | 1.0 | 1.0 | No |
| 5 | FCLR-VOL-JUMP-02 leakage-hardened jump magnitude | Half 1 volatility | NOT_SUPPORTED | 0.1510% | 2% | No | 1.0 | 1.0 | No |
| 6 | FCLR-VOL-JUMP-03 multi-estimator x multi-horizon jump magnitude | Half 1 volatility | NOT_SUPPORTED | 0.3025% | 2% | No | 1.0 | 1.0 | No |
| 7 | FCLR-VOL-JUMP-04 directional/sign jump | Half 1 volatility | NOT_SUPPORTED | 0.0474% | 2% | No | 1.0 | 1.0 | No |
| 8 | Track A observed liquidation-event forecasting | Half 2 liquidation risk | STRUCTURALLY_BLOCKED | n/a | n/a | n/a | 1.0 | 1.0 | No |
| 9 | Track B modeled boundary-breach forecast | Half 2 liquidation risk | NOT_SUPPORTED | n/a | n/a | n/a | 1.0 | 1.0 | No |
| 10 | Track C volatility/stress outcome | Half 2 liquidation risk | NOT_SUPPORTED | n/a | n/a | n/a | 1.0 | 1.0 | No |
| 11 | Cross-sectional funding -> liquidation-intensity | Half 2 liquidation risk | SUPPORTED_GENERALIZATION but NOT_STABLE | n/a | 2% | No | 1.0 | 1.0 | No |

## Family-wide multiplicity results

- NOT_SUPPORTED: 9
- STRUCTURALLY_BLOCKED: 1
- SUPPORTED_GENERALIZATION but NOT_STABLE: 1
- Materiality floor met: 0
- Materiality floor NOT met (where applicable): 6
- Holm-surviving claims (p < 0.05): 0

## Per-track verdict table

All Holm-adjusted p-values = 1.0; no claim survives family-wide multiplicity correction.

## Conclusion

No surviving confirmatory claim after Holm adjustment. The frontier is formally exhausted on the frozen `ironflow_bulk` panel. The honest endpoint is program closure + negative-results preservation.

`audit_pass: true` | `unresolved_blockers: []`
