# Pre-Registration: H_COUPLED-001 (Funding×Vol×Observed-Flow Coupling)

**TIMESTAMP (UTC):** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**EXPERIMENT ID:** FCLR-COUPLED-001
**HYPOTHESIS ID:** H_COUPLED-001
**STATUS:** PRE-REGISTERED BEFORE OUTCOMES
**TRACK:** A' (COUPLED OBSERVED-LIQUIDATION FORECAST) — HYPERLIQUID IRONFLOW ONLY
**PRIORITIZED BY:** repo name = funding-conditioned volatility ∩ liquidation risk (ONE COUPLED PROBLEM)

## 1) Hypothesis (falsifiable)
H_COUPLED-001: Funding state × realized-volatility regime × lagged observed liquidation flow conditioning improves OOS forecast of OBSERVED liquidation occurrence on Hyperliquid (ironflow) beyond FCLR-010 C2 (RV + funding).

Primary claim: relative Brier reduction >= +1.0% for H_COUPLED-001 (coupled) vs FCLR-010 C2 on the same frozen protocol/window.
Null: <= +0.5% relative reduction or difference not distinguishable from 0 under block-aware inference.

## 2) Cross-track firewall (non-negotiable)
- **ONLY** use ironflow_hyperliquid_liquidation_events (Track A).
- **NO** merge with Binance price panels (FCLR-001/002/003/006/007/008/009).
- **NO** reuse Track B (modeled boundary breaches) labels as observed.
- **NO** reuse Track C (volatility forecasting) panels for this experiment.
- Modeled != observed. Firewall must remain intact.

## 3) Data (frozen)
- Labels: ironflow_hyperliquid_liquidation_events (cached at research_state/data_cache/ironflow_events/), window 2025-11-01T00:00:00Z .. 2026-10-31T23:00:00Z (12 monthly files). Universe: native Hyperliquid perpetuals only (>=5).
- Predictors: Hyperliquid public mark prices/funding (api.hyperliquid.xyz/info) as in FCLR-010 protocol; decision-time only.
- Splits: inherit FCLR-010 frozen boundaries from run_manifest.json#split_boundaries_fclr010 (train/val/test, 7d embargo). frozen_before_outcomes=true must hold.

## 4) Frozen feature set (minimal, causal)
All features computed with information available at forecast timestamp t (no look-ahead).

Funding state:
- signed_funding_rate (latest by t)
- abs_funding_rate
- funding_z_90d (trailing 90d z-score of signed funding, >=30 obs)
- funding_change_1h / funding_change_4h (if available)

Vol regime:
- rv_24h, rv_168h (from mark log-returns)
- rv_ratio_24_168
- vol_regime_flag (pre-specified bucket from training-period quantiles only)

Observed-flow conditioning (lagged, no label leakage into features):
- liq_count_lag1h, liq_count_lag4h, liq_count_lag24h (sum over symbol from ironflow, using history up to t-ε)
- liq_notional_log1p_lag24h (decayed)
- flow_persistence (exponentially decayed lagged flow)

Interactions (pre-specified):
- funding_z_90d × vol_regime_flag
- signed_funding_rate × rv_24h
- (abs_funding_rate or funding_z_90d) × liq_notional_log1p_lag24h

Price context (where available, decision-time):
- mark_index_premium (if aligned)
- price_dev_ma24h (deviation from MA, no smoothing over future)

NO unconstrained feature search; fixed set above.

## 5) Models / contrasts (fixed form)
- B1 (reference inherited): FCLR-010 C2 configuration as frozen (RV + funding) — treat as locked baseline for comparison.
- C_coupled (candidate): logistic regression with fixed coefficients form, L2 penalty only if pre-committed (or no penalty) — MUST use same fixed logistic family as FCLR-010 or justify. Default: fixed logistic, no hyperparameter tuning.

Primary contrast: C_coupled vs B1 (FCLR-010 C2).

## 6) Evaluation protocol
- Chronological OOS on frozen FCLR-010 test set (2026-05-28T00:00:00Z .. 2026-10-31T23:00:00Z). Embargo/purge respected.
- Label: binary occurrence (>=1 liquidation in symbol-hour). Primary metric: Brier score.
- Secondary: log loss, calibration slope/intercept, AUPRC (descriptive), precision/recall at pre-specified alert budgets.
- Inference: block bootstrap by UTC time blocks (~24h blocks) jointly across instruments (>=2000 replicates), cluster-aware.
- Multiplicity: if >1 primary/secondary registered, apply Holm correction. Only 1 primary contrast registered now.
- Leakage: features computed from t- history only; lagged flow uses observed labels up to t-ε (allowed if part of decision-time information set, documented). No tuning on test.

## 7) Gates (PASS/FAIL)
| Gate | Criterion | Required |
|------|-----------|----------|
| G1 Relative improvement | (Brier_B1 - Brier_C)/Brier_B1 >= 1.0% (negative diff = improvement) | PASS |
| G2 Paired OOS coverage | >= 5 native perps in paired evaluation | PASS |
| G3 Blocks | >= 3 non-overlapping 30-day blocks in test window | PASS |
| G4 Firewall | No Binance merge; modeled!=observed preserved | PASS |
| G5 Calibration | Acceptable calibration (slope near 1, intercept near 0; no severe miscalibration) | PASS |
| G6 No leakage | Decision-time features only; splits unchanged | PASS |

All gates required for SUPPORT. Otherwise NOT_SUPPORTED/PARTIAL with evidence.

## 8) Execution plan (single highest-value next step)
1. Verify firewall and frozen splits intact.
2. Implement minimal coupled feature builder for ironflow panel (using existing cached data), reusing FCLR-010 pipeline structure.
3. Train fixed logistic on frozen train/val with locked features; evaluate on frozen test.
4. Block-bootstrap paired comparison vs B1; write evaluation summary.
5. Update AGENT_HANDOFF.md + experiment_frontier.json.

**VERIFY COMMAND (for next agent):**
```bash
LATEST_PREREG=$(ls -t research_state/pre_registration_h_coupled_001_*.md 2>/dev/null | head -1); test -n "$LATEST_PREREG" && echo "---" && echo "$LATEST_PREREG" && echo "---" && wc -l "$LATEST_PREREG" && echo "---" && grep -n "H_COUPLED-001\|FCLR-COUPLED-001\|>= +1.0%\|firewall\|ironflow" "$LATEST_PREREG" | head -15
```
