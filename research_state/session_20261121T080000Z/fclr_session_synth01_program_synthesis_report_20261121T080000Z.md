# FCLR-SESSION-SYNTHESIS-01 — Program Synthesis Report

- **Experiment ID:** FCLR-SESSION-SYNTHESIS-01-20261121T080000Z
- **Generated (UTC):** 2026-11-21T08:00:00Z
- **Outcome data inspected before freeze:** `false` · **Generates no new outcomes:** `true`

## 1. Mandate

Repository: **Funding-conditioned-volatility-and-liquidation-risk**. Two scientific halves reconciled
by funding conditioning:

- **(a) Funding → volatility (RV).**
- **(b) Funding → liquidation risk.**

Both are terminal on the verified frozen panels.

## 2. Terminal campaign ledger (exact statistics)

| Campaign | Pillar | Verdict | Key evidence |
|----------|--------|---------|--------------|
| FCLR-STARTER-001 | volatility | NOT_SUPPORTED | C2 vs B1 rel QLIKE +2.62% (worse), Holm adj_p 0.075 |
| FCLR-XSEC-001 | volatility | NOT_SUPPORTED | funding contrast CI [−0.390, +0.158] incl. 0 |
| FCLR-XSEC-002 | volatility | **SUPPORTED** | high-RV funding CI [0.0046, 0.2348], p=0.019, materiality 1.09; OOS forwards all NOT_REPLICATED |
| FCLR-XSEC-003 | volatility | SUPERSEDED | folded into XSEC-004 |
| FCLR-XSEC-004 | liquidation_risk | **SUPPORTED** | low-RV funding CI [448605.26, 841155.73], p=0.0, Holm 0.0, materiality 0.80 |
| FCLR-XSEC-005 | liquidation_risk | **SUPPORTED** | low-RV notional funding CI [452972.90, 850198.89], p=0.0, Holm 0.0, materiality 0.80 |
| FCLR-XSEC-006 | liquidation_risk | **SUPPORTED** | significant across all 3 UTC session buckets |
| FCLR-XSEC-007 | cross_panel | NOT_SUPPORTED | Primary A CI [−0.0004, 2.005] incl. 0 (p=0.272, Holm 0.816); joint needs both |
| FCLR-XSEC-008 | cross_panel | NOT_SUPPORTED | Primary A passes with sign reversal, Primary B fails; XSEC terminal |
| FCLR-LIQ-OOS-FORECAST-001 | liquidation_risk | NOT_SUPPORTED | QLIKE FAIL rel −5.88% CI incl. zero; Brier +11.48% PASS; LogLoss +8.63% PASS; joint needs ALL |
| FCLR-LIQ-COMBINED-PANEL | liquidation_risk | NOT_MET | time-series QLIKE gate NOT_MET |
| FCLR-LIQ-XSEC-ORDERING/QLIKE | liquidation_risk | NOT_MET | daily ordering/QLIKE, not hourly paired contrast |
| Track A (combined panel) | liquidation_risk | NOT_MET / blocked | observed-liq forecast blocked/null |
| Track B (modeled breaches) | liq_modeled_proxy | NOT_MET | LogLoss +1.68% (<2% floor), CI crosses zero, 2 blocks (<3) |

## 3. Frozen panel audit (verified this session)

- FCLR-001: `research_state/fclr011_recompute_panel_20261115T234700Z.parquet`
  sha256 `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4`
- Combined liquidation: `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet`
  sha256 `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14`

## 4. Pillar summary

### (a) Volatility half
- **Cross-sectional:** SUPPORTED only in the HIGH-RV regime (FCLR-XSEC-002, CI [0.0046, 0.2348],
  p=0.019, materiality 1.09).
- **Out-of-sample forward:** ALL FAILED to replicate (FCLR-FWD-VOL-011-CONFIRM family
  2024Q4/2025H2/2025Q1Q2, all NOT_REPLICATED/NOT_MET).
- **Terminal hypothesis:** H1_primary NOT_SUPPORTED (FCLR-011 PASS sealed but does not generalize
  forward).

### (b) Liquidation-risk half
- **Cross-sectional:** SUPPORTED in the LOW-RV regime (FCLR-XSEC-004 count-based, FCLR-XSEC-005
  notional-weighted) and across all three UTC session buckets (FCLR-XSEC-006).
- **Out-of-sample forecast:** FAILED (FCLR-LIQ-OOS-FORECAST-001 NOT_SUPPORTED: QLIKE FAIL rel −5.88%
  CI incl. zero; Brier/LogLoss PASS but joint gate requires ALL).
- **Modeled breach (Track B):** NOT_MET (synthetic proxy only, never observed liquidations).

### Cross-panel reconciliation
- NOT_SUPPORTED (FCLR-XSEC-007: Primary A CI incl. 0; joint gate needs both. FCLR-XSEC-008
  alternative-regime conditioning NOT_SUPPORTED with sign reversal vs XSEC-002).

## 5. Synthesis conclusion

Both halves of the *Funding-conditioned-volatility-and-liquidation-risk* mandate are **terminal** on
the verified frozen panels. The cross-sectional funding-conditioning associations are statistically
detectable in specific regimes (RV high-RV; liquidation low-RV + UTC buckets) but **NO out-of-sample
forecast gate passed**, and the cross-panel reconciliation is NOT_SUPPORTED. The consolidated
evidence does not support a promotable funding-conditioned forecast skill.

**Reopening requires `NEW_OBSERVED_LIQUIDATION_SOURCE`** — a new observed-liquidation data source
beyond the frozen panels. See `frontier_exhaustion_audit_20261121T080000Z.{json,md}` for the
per-domain blockage audit and `fclr_session_synth01_meta_analysis_20261121T080000Z.{py,json,md}`
for the quantitative effect-size synthesis.