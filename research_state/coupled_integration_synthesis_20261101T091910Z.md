# Coupled Integration Synthesis (FCLR-COUPLED-INTEGRATE)
**TIMESTAMP (UTC):** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**HANDOFF:** FCLR-HANDOFF-030-20261101T091553Z
**STATUS:** INTEGRATION-FOCUSED (no exhausted-panel reruns)

## 1) Coupling rationale
Funding-conditioned volatility and liquidation risk are coupled via feedback: funding affects positioning cost/one-sidedness (fragility), volatility/regime sets sensitivity, and observed liquidations create flow feedback. Track A (FCLR-010) shows forecastable observed liquidations under firewall; Track C (vol-only) is exhausted/negative; Track B (modeled boundaries) is weak/negative. Optimize on observed liquidations with funding×vol conditioning, not on vol-forecast alone.

## 2) Evidence map
| Track/Exp | Status | Evidence |
|-----------|--------|----------|
| A/FCLR-010 | COMPLETE/PASSED | research_state/evaluation_summary_FCLR010.md, research_state/run_manifest.json#experiments.FCLR-010 (+2.21% rel Brier C2 vs B1) |
| C/FCLR-009 | NOT_MET/CLOSED | research_state/evaluation_summary_FCLR009.md, research_state/track_c_final_synthesis_dossier.md (-0.43% QLIKE C2 vs B1) |
| B/FCLR-H003/FCLR-002 | CLOSED_NEGATIVE/weak | research_state/evaluation_summary_h003_FCLR002.md |
| H002 | PARTIAL/EXPLORATORY | research_state/h002_replication_report.md |

## 3) Joint model spec (testable without merging panels)
- Target: observed liquidations (ironflow Hyperliquid), modeled != observed.
- Features (minimal): funding state (level/z/change), vol regime (RV/ATR), lagged observed liquidation flow (decay), mark-index premium where available, interactions funding×regime, funding×lagged flow.
- Firewall: Hyperliquid labels only; no merge with Binance price panels.
- Controls: decision-time only, frozen splits/embargo, block-aware OOS, label-history proxies only if allowed.

## 4) Pre-registered next test (H_COUPLED-001)
Hypothesis: funding×vol×observed-flow conditioning gives >= +1.0% relative Brier reduction over FCLR-010 C2 on same frozen protocol (primary). Gates: >=+1.0% rel Brier, paired OOS>=5, >=3 blocks, firewall preserved, calibration ok. Use Holm if multiplicity>1. Fixed logistic, no tuning.

## 5) Actionable plan (single highest-value step)
Create pre-registration locking features/contrasts/metrics/gates before any runs. No reruns of exhausted Track C/B.

Verify: `LATEST_PREREG=$(ls -t research_state/pre_registration_h_coupled_001_*.md 2>/dev/null | head -1); test -n "$LATEST_PREREG" && echo $LATEST_PREREG && wc -l $LATEST_PREREG`
