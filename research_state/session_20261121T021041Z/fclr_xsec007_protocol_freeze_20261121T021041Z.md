# FCLR-XSEC-007 Protocol Freeze — Cross-Panel Mechanism Reconciliation

**Experiment ID:** FCLR-XSEC-007-20261121T021041Z
**Session UTC:** 20261121T021041Z
**Repository:** Funding-conditioned-volatility-and-liquidation-risk
**Status:** PREREG_FREEZE (frozen before any outcome inspection)
**outcome_data_inspected_before_freeze:** false

## 1. Purpose

Cross-panel mechanism reconciliation on overlapping 5-coin FCLR-001 hours. Test whether the regime-conditioned funding effect that is SUPPORTED for RV (FCLR-XSEC-002, HIGH-RV regime, next-hour RV) and for liquidation intensity (FCLR-XSEC-004/005, LOW-RV regime; FCLR-XSEC-006, ALL THREE UTC session buckets, next-hour notional-weighted liquidation intensity) can be reconciled on the **same coin×hour panel** by joining the two frozen panels on coin×hour.

This is a distinct, non-duplicative estimand from all terminal campaigns (FCLR-XSEC-001 through XSEC-006). No panel is rebuilt; both panels are hash-frozen and read-only. No network, no paid data, no credentials.

## 2. Frozen Panels (hash-verified, do not re-derive)

| Panel | Path | SHA-256 | Rows | Coins | Span |
|-------|------|---------|------|-------|------|
| FCLR-001 (RV + funding) | `research_state/fclr011_recompute_panel_20261115T234700Z.parquet` | `41962f823e59de5989c7d854cb3180cad61a4cbc2f5f230133c41b321342c1f4` | 29,136 | 5 (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT) | 2026-01-01..2026-08-31 |
| Combined liquidation (observed liq. intensity + funding) | `research_state/fclr_liq_combined_panel_20261115T181405Z.parquet` | `81a100d5d0625832bebabaabea13b786e15319577721cfe8507da5b779ec7f14` | 1,740,415 | 15 | 2025-03-22..2026-10-31 |

**Coin name mapping (FCLR-001 → liquidation panel):** BTCUSDT→BTC, ETHUSDT→ETH, BNBUSDT→BNB, SOLUSDT→SOL, XRPUSDT→XRP.

**Overlap:** 5 coins × hours 2026-01-01T00:00Z..2026-08-31T23:00Z (FCLR-001 span is the binding constraint).

## 3. Join Design

Aggregate the combined liquidation panel to one (coin, hour) row:
- next-hour NOTIONAL-WEIGHTED liquidation intensity = sum(notional_usd) per coin in hour t+1 (shift -1 within coin) — dollar severity, not event count
- abs_fund_pct mean per (coin, hour)
- rv24h mean per (coin, hour)

Join with FCLR-001 on (coin, hour) for the 5 overlapping coins and overlapping hours. FCLR-001 provides: rv24h, abs_funding_pct_trail, target_rv24h (next-hour RV), signed_funding.

## 4. Regime Variables (assigned ex-ante, before outcome inspection)

**Regime A (Primary A):** Market-wide RV tercile at hour t, computed from FCLR-001 rv24h across the 5 coins. High / mid / low tercile per hour.

**Regime B (Primary B):** UTC trading-session bucket at hour t:
- Asian [00:00, 08:00)
- European [08:00, 16:00)
- US [16:00, 24:00)

Bucket assigned by clock hour, independent of RV. Hour eligible if >= 3 coins present.

## 5. Predictor

Within each (hour, regime), rank coins by abs_fund_pct cross-sectionally. high_funding = top half by rank, low_funding = bottom half. Paired high-minus-low contrast within each hour.

## 6. Primary Estimands

**Primary A** (FCLR-XSEC-002 style, restricted to overlapping hours): within-(hour, RV-tercile) funding rank → next-hour RV (target_rv24h from FCLR-001).

**Primary B** (FCLR-XSEC-006 style, restricted to overlapping hours): within-(hour, UTC-session-bucket) funding rank → next-hour notional-weighted liquidation intensity.

## 7. Baselines (specificity controls)

- Baseline A: within-RV-tercile RV persistence (coin's own rv24h at t, high vs low within (hour, tercile)) → next-hour RV.
- Baseline B: within-session-bucket RV persistence (coin's own rv24h at t, high vs low within (hour, bucket)) → next-hour notional-weighted liquidation intensity.

## 8. Inference

Block bootstrap across whole UTC hours within each regime family (seed 20261121, >=2000 deterministic replicates). Holm correction over the joint test family of 4 tests (2 regimes × {funding contrast, RV persistence baseline}). 95% CIs. 2% materiality floor: |mean_diff_high_minus_low| / mean_abs_outcome >= 0.02.

## 9. Cross-Panel Reconciliation (on shared overlapping hours)

- Coefficient sign agreement: sign(funding-rank coefficient for RV) == sign(funding-rank coefficient for notional-weighted liq intensity)
- Magnitude correlation: correlation of per-hour funding-contrast effect sizes between the two outcomes on shared hours
- Joint significance: both primary contrasts individually clear the gate on shared hours

## 10. Verdict Rule

SUPPORTED only if BOTH primary funding contrasts (Primary A and Primary B) clear all three gates (CI excludes zero, Holm adj_p < 0.05, materiality >= 0.02) on the overlapping hours. Otherwise preserve the honest null as NOT_SUPPORTED. Do not threshold-shop; do not relax the 2% floor after seeing outcomes.

## 11. Cross-References

- FCLR-XSEC-002: high-RV regime funding CI [0.0046, 0.2348], p=0.019, materiality 1.09 → SUPPORTED
- FCLR-XSEC-004: low-RV count-based funding CI [448605.26, 841155.73], p=0.0, materiality 0.80 → SUPPORTED
- FCLR-XSEC-005: low-RV notional-weighted funding CI [452972.90, 850198.89], p=0.0, materiality 0.80 → SUPPORTED
- FCLR-XSEC-006: all three UTC buckets SUPPORTED (Asian CI [162051, 521424], European CI [334550, 782272], US CI [94750, 698082])

## 12. Constraints

- No holdout outcomes inspected before protocol freeze (outcome_data_inspected_before_freeze = false)
- No sealed protocol overwrite (`research_state/research_protocol.md` untouched)
- No network, no paid data, no credentials
- No root-level research_state/*.md or *.json added (root churn cap 499/500 holds)
- No re-run of FCLR-STARTER-001 / FCLR-XSEC-001 / FCLR-XSEC-002 / FCLR-XSEC-003 / FCLR-XSEC-004 / FCLR-XSEC-005 / FCLR-XSEC-006
- Track separation: observed liquidations (Track A) never conflated with modeled boundary breaches (Track B) or RV forecasts

## 13. Required Artifacts (under `research_state/session_20261121T021041Z/`)

1. `fclr_xsec007_protocol_freeze_20261121T021041Z.json` + `.md` (this document)
2. `fclr_xsec007_evaluation_20261121T021041Z.py` + `.json` + `.md` — joint evaluation on overlapping hours
3. `fclr_xsec007_recompute_20261121T021041Z.py` + `.json` — independent recompute
4. `evidence_audit_20261121T021041Z.json` + `.md`
5. `trigger_check_20261121T021041Z.json` — non-empty, all checks PASS/FAIL
