# Coupled Integration Synthesis (FCLR-COUPLED-INTEGRATE)
**TIMESTAMP (UTC):** 2026-11-01T09:17:22Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**HANDOFF:** FCLR-HANDOFF-030-20261101T091553Z (follow-on)
**STATUS:** INTEGRATION-FOCUSED (no exhausted-panel reruns)

## 1) Coupling rationale (why they are coupled)
Funding-conditioned volatility and liquidation risk are coupled via a common mechanism, not independent predictors:
- **Leverage/positioning feedback:** Perpetual funding is the cost to hold positions; when funding is elevated/stretched relative to recent moves, positioning becomes more one-sided and more levered positions become fragile to adverse moves. This raises the sensitivity of the system to shocks.
- **Liquidity/forced flow:** Adverse price moves can trigger liquidations; liquidations create further price impact (feedback), which can create more liquidations in a cascade. The probability/intensity of such cascades depends on where funding has driven positioning (crowded sides) and on prevailing volatility/regime.
- **Conditioning direction:** Volatility forecasting alone (Track C, FCLR-009) showed no incremental edge beyond base; boundary-breach modeling alone (Track B/H003) was largely negative/weak with modeled labels. By contrast, **observed liquidations** (Track A/FCLR-010) on Hyperliquid via ironflow census showed a forecastable component conditioned in the right form (C2 vs B1 +2.21% relative Brier reduction, all gates PASS). The linkage is: funding conditions affect positioning fragility; fragility manifests as observed liquidation risk under volatility/flow, not just as "more volatility forecast" in the same panel.

Conclusion: treat as a **coupled system** (funding × positioning fragility × liquidation flow) measured by **observed liquidation outcomes** (ironflow/Hyperliquid) with a strict firewall from Binance price panels. Volatility is a conditioning/context variable in the coupled form, not the sole target to optimize if exhausted.

## 2) Evidence map (concrete paths)
| Track/Exp | Status/Gate | Key evidence | Notes |
|-----------|-------------|--------------|-------|
| A / FCLR-010 (observed liquidations, ironflow Hyperliquid census) | COMPLETE / PASSED | `research_state/evaluation_summary_FCLR010.md`, `research_state/run_manifest.json#experiments.FCLR-010` (status COMPLETE, gate PASSED) | Primary contrast C2 vs B1 +2.21% rel Brier; paired OOS instruments >=5; >=3 blocks; modeled≠observed; cross-track firewall enforced. Features include causal proxies from label history where needed. |
| C / FCLR-009 (volatility-only) | NOT_MET / CLOSED_NEGATIVE for promotion | `research_state/evaluation_summary_FCLR009.md`, `research_state/track_c_final_synthesis_dossier.md`, `research_state/track_c_consolidated_dossier.md`, `research_state/track_c_traceability_matrix.md`, `research_state/track_c_residual_audit.md` | C2 vs B1 -0.43% QLIKE (no). Exhausted per prior handoffs; do not rerun broad panels. |
| B / FCLR-H003 / FCLR-002 (modeled boundary breaches) | CLOSED_NEGATIVE / weak | `research_state/evaluation_summary_h003_FCLR002.md`, `research_state/evaluation_summary_h003.md`, `research_state/fclr_h003_pre_registration.md` | Largely zero/weak base rates at low leverage; small mixed AUPRC/Brier changes with no clean gate pass for promotion as primary. Modeled labels ≠ observed liquidations. |
| H002 (funding-correction) | PARTIAL/EXPLORATORY | `research_state/h002_replication_report.md`, `research_state/h002_methodology_dossier.md`, `research_state/h002_pre_registration.md` | Exploratory only; no promotion. |

Cross-cutting: splits frozen before inspection, block-aware inference, Holm if multiplicity grows, no merging Hyperliquid liquidation labels into Binance price panels.

## 3) Joint model spec (coupled, testable without violating firewall)
**Target (observed):** next-window probability/intensity of observed liquidations on Hyperliquid (ironflow census), per instrument/time as defined by FCLR-010 protocol. Keep `modeled != observed` separation explicit.

**Conditioning set (coupled):**
- **Funding state:** current/lagged funding rate, funding z-score vs rolling window, time-since-last-funding, funding acceleration/change (avoid leakage; use values known at decision time). Treat as positioning cost signal.
- **Volatility/regime (context):** realized volatility, vol-of-vol, range/ATR, vol regime indicators. Use as conditioning (not the target optimization) — consistent with Track C being context; do not require vol-forecast edge alone.
- **Positioning/fragility proxies:** mark-index premium/EMA distance (where available), open interest change/turnover where feasible without importing Binance labels, funding skew/imbalance signals. Prefer causal proxies derived from label history only when protocol allows (as done in FCLR-010).
- **Liquidation-flow history:** lagged observed liquidation counts/ratios (with strict embargo/leakage control), decay kernels (recent stronger). Must remain within observed-liquidation feature space (no Binance liquidation labels).
- **Interaction terms (minimal):** funding×vol regime, funding×recent liquidation flow (capture cascade sensitivity). Start small to avoid overfit; frozen form.

**Leakage/firewall controls:**
- **Separation:** Hyperliquid liquidation labels ONLY in Track A feature/target space. No merge with Binance OHLCV/price panels used for Track C/B.
- **Time discipline:** frozen splits/embargo, decision-time features only, block-aware OOS.
- **Causal discipline:** label-history-derived features only if permitted by FCLR-010 protocol; avoid outcome leakage.
- **Multiplicity:** pre-register contrasts, use Holm/BH if expanding.

**Why testable without merging panels:** The PASSED result already demonstrates forecastability on observed liquidations with available features under firewall. Coupling means we condition on funding/vol/fragility to explain that observed liquidation risk (and to improve it) rather than redefining target to modeled boundary breaches or to Binance-volatility.

## 4) Pre-registered next test (single falsifiable hypothesis + minimal protocol)
**Hypothesis (H_COUPLED-001, falsifiable):**
> Conditioning observed-liquidation forecasts on funding state × volatility regime × lagged observed liquidation flow (minimal interaction set) yields >= +1.0% relative Brier reduction over the FCLR-010 C2 specification on the same frozen OOS protocol, with no degradation in calibration and while preserving firewall/separation.

**Null:** ΔBrier_rel(C2_coupled vs C2_FCLR010) <= +1.0% (or no improvement) under pre-registered test.

**Minimal protocol (must match FCLR-010 discipline):**
- **Data/target:** Same ironflow Hyperliquid observed-liquidation target/definition as FCLR-010.
- **Splits:** Reuse frozen splits/embargo as in FCLR-010 (no re-splitting on results). Do not expand window opportunistically.
- **Models:** B0/B1 baselines per protocol; C2_FCLR010 = reference; C2_coupled = add minimal coupled features (funding×regime, funding×lagged observed flow) in fixed logistic form (no regularization/hyperparam search).
- **Metrics:** Brier (primary), log-loss/calibration; paired block bootstrap on same block structure.
- **Gates:** >=+1.0% relative Brier reduction on primary contrast, paired OOS >=5 instruments, >=3 non-overlapping blocks, no firewall violation, modeled≠observed preserved.
- **Multiplicity:** If adding >1 contrast, apply Holm correction. Pre-register before running.

**Acceptance:** PASS only if all gates met. Otherwise FAIL/CLOSED with evidence; do not expand feature set.

## 5) Actionable plan (exactly one highest-value next executable step)
**Single highest-value step:** Create a pre-registration document for H_COUPLED-001 that locks the exact feature list, contrasts, metrics, gates, and verification commands (based strictly on FCLR-010 protocol) without modifying data/code/panels or rerunning exhausted Track C/B. Do **not** execute training runs yet - lock protocol first to avoid scope creep.

**Executable command (create pre-reg):**
```bash
cat > /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/pre_registration_h_coupled_001_$(date -u +%Y%m%dT%H%M%SZ).md << 'EOF'
# Pre-registration: H_COUPLED-001 (funding×vol×observed-flow coupling for observed liquidations)
...
