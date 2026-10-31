# Track C Consolidated Evidence Dossier (H001: Funding-Conditioned Volatility Forecasting)

**Generated:** 2026-10-31T02:18:31Z
**Status:** NOT_SUPPORTED — SEALED_NEGATIVE
**Tracks:** C (volatility forecasting) | Priority: P0 (by repo name)

## Executive Summary

Across all three confirmatory/unsealed runs on Binance USDⓈ-M perpetuals (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), adding funding-conditioned features (C1/C2) does **not** improve out-of-sample 24h realized volatility forecasts over a realized-volatility HAR baseline (B1). In all cases the gate fails; in two cases (FCLR-006, FCLR-007) the funding-conditioned model is significantly worse. Risk overlay is **ineligible**.

## Run-by-Run Evidence

### FCLR-003 (Powered confirmatory, 2024-10-02..2024-12-31)
- **Source:** `research_state/evaluation_summary_FCLR003.md`
- **Test window:** 2024-10-02T00:00:00Z .. 2024-12-31T23:00:00Z (91 days = 3 non-overlapping 30-day blocks)
- **Instruments:** 5 (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT) — PASS (>=5)
- **Paired n (C2 vs B1):** 10796
- **QLIKE (test):** B1=0.193940, C2=0.202835
- **C2 vs B1:** mean diff = +0.015205, 95% CI [-0.020240, 0.056734] (crosses zero)
- **Relative reduction:** -3.78% (negative = worse)
- **Gate:** NOT_MET (CI crosses zero; relative < 2%)
- **Repro:** Byte-identical reproduction verified

### FCLR-006 (Unsealed 2026, underpowered blocks, 2026-05-23..2026-08-06)
- **Source:** `research_state/evaluation_summary_FCLR006.md`, `research_state/fclr006_coverage_audit.md`
- **Test window:** 2026-05-23T00:00:00Z .. 2026-08-06T23:00:00Z (76 days = 2 non-overlapping 30-day blocks)
- **Instruments:** 5 — PASS
- **Paired n (C2 vs B1):** 8987
- **QLIKE (test):** B1=0.527053, C2=0.895641
- **C2 vs B1:** mean diff = +0.368588, 95% CI [0.173749, 0.615614] (entirely positive)
- **Relative reduction:** -69.90% (significantly worse)
- **Gate:** NOT_MET (CI excludes zero on worse side; blocks < 3)
- **Repro:** Byte-identical reproduction verified

### FCLR-007 (Unsealed 2026, pre-registered before outcomes, 2026-04-01..2026-07-31)
- **Source:** `research_state/evaluation_summary_FCLR007.md`, `research_state/fclr007_coverage_audit.md`
- **Test window:** 2026-07-21T00:00:00Z .. 2026-07-31T23:00:00Z (11 days = 0 non-overlapping 30-day blocks)
- **Instruments:** 5 — PASS
- **Paired n (C2 vs B1):** 1114 (from summary)
- **QLIKE (test):** B1=0.300332, C2=0.310590
- **C2 vs B1:** mean diff = +0.010258, 95% CI [0.001308, 0.019737] (entirely positive)
- **Relative reduction:** -3.42% (worse)
- **Gate:** NOT_MET (CI excludes zero on worse side; blocks < 3, test window too short)
- **Pre-registration:** Frozen before outcome inspection per protocol; splits in run_manifest under `split_boundaries_fclr007`
- **Repro:** Byte-identical repro verified

## Cross-Run Synthesis
- **Consistency:** All three runs fail the forecast gate. Two show statistically significant degradation.
- **Block/bootstrap:** All use paired comparisons with block bootstrap (~24h blocks) as specified.
- **Track separation:** Strictly Track C (volatility). No conflation with liquidation labels.
- **Conclusion:** H001 (funding-conditioned volatility forecasting) is **NOT_SUPPORTED**. Risk overlay is **ineligible**.

## Traceability
- `scripts/run_evaluation.py` (FCLR-003/006/007 modes)
- `research_state/run_manifest.json` (split boundaries, hashes)
- `research_state/evaluation_summary_FCLR003.md`, `evaluation_summary_FCLR006.md`, `evaluation_summary_FCLR007.md`
- `research_state/fclr007_coverage_audit.md`, `fclr006_coverage_audit.md`
- Tests: `tests/test_funding_correction_*.py` all pass (14/14)
