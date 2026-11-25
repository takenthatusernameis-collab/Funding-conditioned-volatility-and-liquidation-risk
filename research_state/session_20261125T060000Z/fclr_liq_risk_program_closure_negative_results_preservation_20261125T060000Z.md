# FCLR-LIQ-RISK-PROGRAM-CLOSURE-02 — Negative-Results Preservation

**experiment_id:** FCLR-LIQ-RISK-PROGRAM-CLOSURE-02
**session_id:** session_20261125T060000Z
**session_utc:** 20261125T060000Z
**generated_utc:** 2026-11-25T06:00:00Z
**campaign_id:** FCLR-LIQ-RISK-PROGRAM-CLOSURE-02-20261125T054500Z
**section_19_compliant:** true

## Preserved null / failed / inconclusive outcomes

1. **FCLR-VOL-BROAD-01 mean log-RV QLIKE** — NOT_SUPPORTED. 1.93% relative QLIKE improvement below frozen 2% materiality floor; statistically nonzero but economically immaterial at broad scale. Artifact: `research_state/session_20261124T120000Z/fclr_volbroad01_eval_*.json`.

2. **FCLR-VOL-CORR-01 funding-extreme correction-time/hazard** — NOT_SUPPORTED. High-RV median correction 9.00h vs low-RV 10.00h (high-RV not slower); >=10% relative slower-correction floor NOT met; Shek (2026) pattern not reconstructed at broad scale. Artifact: `research_state/session_20261124T204500Z/fclr_volcorr01_eval_*.json`.

3. **FCLR-VOL-STRESS-01 volatility-stress/tail-exceedance** — NOT_SUPPORTED. 1.51% relative Brier improvement below frozen 2% floor; 1,393,204 forecasts, 63,059 stress events, 314 coins. Artifact: `research_state/session_20261124T222500Z/fclr_volstress01_eval_*.json`.

4. **FCLR-VOL-JUMP-01 signed-jump magnitude exceedance** — NOT_SUPPORTED. 0.0922% relative Brier improvement, far below 2% floor; 1,136,222 forecasts, 39,116 jump events, 454 coins. Artifact: `research_state/session_20261125T030000Z/fclr_voljump01_eval_*.json`.

5. **FCLR-VOL-JUMP-02 leakage-hardened jump magnitude** — NOT_SUPPORTED. 0.1510% relative Brier improvement; null survives 48h purge+embargo, non-overlapping forward windows, mark/index tolerance filter, delisting-aware identity, per-coin cluster bootstrap, Holm. Artifact: `research_state/session_20261125T034400Z/fclr_voljump02_eval_*.json`.

6. **FCLR-VOL-JUMP-03 multi-estimator x multi-horizon jump magnitude** — NOT_SUPPORTED. Aggregate 0.3025% relative Brier improvement below 2% floor; null survives bipower vs threshold-bipower AND {24h,48h}. Artifact: `research_state/session_20261125T045000Z/fclr_voljump03_eval_*.json`.

7. **FCLR-VOL-JUMP-04 directional/sign jump** — NOT_SUPPORTED. Aggregate 0.0474% / <=0.1020% best-config relative Brier improvement below 2% floor; 110,914 non-overlapping forecasts, 57,354 downside-dominance events, 367 coins; null survives full leakage remediation. Artifact: `research_state/session_20261125T054500Z/fclr_voljump04_eval_*.json`.

8. **Track A observed liquidation-event forecasting** — STRUCTURALLY_BLOCKED. Capped-sample liquidation feed; no complete observed-liquidation source; cannot fire on frozen data.

9. **Track B modeled hypothetical boundary-breach forecast** — NOT_SUPPORTED. Modeled proxy does not reconstruct account-specific liquidation mechanics.

10. **Track C volatility/stress outcome from mark-price history** — NOT_SUPPORTED. No arm cleared frozen materiality floor.

11. **Cross-sectional regime-conditioned funding -> liquidation-intensity rank ordering** — SUPPORTED_GENERALIZATION but NOT_STABLE. 2% Poisson-deviance materiality floor NOT MET; section 17 condition #4 fails; not stable across time blocks.

## Integrity

`preserved_honestly: true` | `no_fabricated_pass: true` | `all_verdicts_evidence_backed: true` | `audit_pass: true` | `unresolved_blockers: []`
