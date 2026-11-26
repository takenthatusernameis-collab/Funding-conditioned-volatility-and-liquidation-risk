# AGENT HANDOFF

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION

# AGENT_HANDOFF.md — FCLR-009 Confirmatory Volatility Evaluation

**Timestamp:** 2026-11-26T01:53:15Z
**Session:** NEXT (to execute)
**Campaign:** FCLR-009 (CONFIRMATORY VOLATILITY — 2025 full-year panel)
**Hypothesis:** FCLR-H001 (incremental 24-hour volatility forecasting)
**Status:** PROTOCOL_FROZEN | COVERAGE_AUDIT_PASSED | EVALUATION_NOT_STARTED

---

## 1. What Changed & Why

The repository contains a **pre-registered, frozen confirmatory protocol** (FCLR-009) for the 2025 calendar-year panel (5 symbols × 365 days × 8760 hourly timestamps). The coverage audit passed (fclr009_coverage_audit.json: 5 symbols, 0 missing days, 12 non-overlapping 30-day blocks). Data is fully cached in `research_state/data_cache/` (markPriceKlines + fundingRate for BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT).

**The confirmatory evaluation has NOT been run.** The last session (2026-11-21) completed a separate Track A liquidation-contagion experiment (FCLR-LIQ-CONTAGION-001). The primary Track C volatility forecasting gate (FCLR-009) remains the highest-priority unfinished confirmatory task.

---

## 2. What Was Actually Tested — Exact Outcomes

| Artifact | Status | Evidence |
|----------|--------|----------|
| `research_protocol_fclr009.md` | FROZEN pre-outcomes | Version 1.0, 2026-11-01T03:00:00Z, splits frozen |
| `fclr009_coverage_audit.json` | PASSED | 5 symbols, 365 days, 8760 common timestamps, 12 non-overlapping 30-day blocks, all file hashes recorded |
| Data cache | VERIFIED | markPriceKlines + fundingRate CSVs with SHA256 for all 5 symbols × 12 months |
| FCLR-009 evaluation | NOT_STARTED | No evaluation_summary_FCLR-009* artifact exists |

---

## 3. Evidence Added & Where

- `research_state/research_protocol_fclr009.md` — frozen protocol (primary outcome: next-24h realized variance of mark-price returns; models B0/B1/C1/C2; splits train/val/test with 7-day purge/embargo; block bootstrap 2000 reps; Holm correction; ≥2% relative QLIKE floor; ≥5 instruments & ≥3 blocks minimum)
- `research_state/fclr009_coverage_audit.json` — coverage-only audit with per-day file hashes
- `research_state/data_cache/{SYMBOL}_2025_*/` — raw CSVs + SHA256 for all required series

---

## 4. Current State of Each Research Gate

| Gate | Status | Evidence |
|------|--------|----------|
| Source feasibility (Track C) | DATA_READY | Binance public archive markPriceKlines + fundingRate cached, hash-verified |
| Label decision | TRACK_C_ACTIVE | Track A (observed liquidations) BLOCKED structurally; Track C (volatility) proceeds independently per protocol |
| Protocol freeze (FCLR-009) | PROTOCOL_FROZEN | research_protocol_fclr009.md frozen 2026-11-01 pre-outcomes |
| Baseline evaluation | NOT_STARTED | No B0/B1/C1/C2 results on 2025 panel |
| Confirmatory evaluation | NOT_STARTED | Primary contrast C2 vs B1 on 24h OOS QLIKE not computed |
| Forecast gate | PENDING | Requires ≥2% relative QLIKE reduction, 95% CI excluding zero on improving side, ≥5 instruments, ≥3 non-overlapping 30-day blocks |

---

## 5. Single Highest-Value Next Task

**Execute FCLR-009 confirmatory evaluation on the frozen 2025 panel and emit the evaluation summary with gate verdict.**

This means:
1. Build the unified 2025 panel from cached CSVs (markPriceKlines → close; fundingRate → last_funding_rate)
2. Compute frozen features per protocol: RV1h/RV24h/RV168h, signed funding, 90-day abs-funding percentile, mark/index premium (if index cached), mark/EMA24 distance
3. Construct target: forward 24h realized variance (sum of squared log returns over t+1..t+24)
4. Apply frozen chronological splits (train: 2025-01-01..2025-04-05, val: 2025-04-13..2025-05-31, test: 2025-06-08..2025-12-31 with 7-day purge/embargo)
5. Fit models B0 (persistence), B1 (RV-HAR log-linear), C1 (B1 + signed funding + funding_pct_90d), C2 (C1 + premium + EMA24 distance) using train-only OLS with train-only standardization
6. Evaluate on test panel: paired QLIKE, MAE, RMSE for each model; C2 vs B1 primary contrast
7. Block bootstrap (24h blocks, 2000 reps, seed=12345) for ΔQLIKE CI; Holm correction across registered family
8. Check gate: ≥2% relative QLIKE reduction? 95% CI excludes zero on improving side? ≥5 instruments? ≥3 non-overlapping 30-day blocks in test?
9. Write `research_state/evaluation_summary_FCLR-009-<TIMESTAMP>.json` + `.md` with full metrics, CI, gate verdict (MET / NOT_MET), and artifact hashes

---

## 6. Precise Command/Check to Verify Progress

```bash
# After the evaluation script completes, verify the gate artifact exists and is non-empty:
ls -la research_state/evaluation_summary_FCLR-009-*.json
cat research_state/evaluation_summary_FCLR-009-*.json | jq '.gate_verdict, .primary_contrast.relative_qlike_reduction_pct, .primary_contrast.ci_low, .primary_contrast.ci_high, .n_instruments_test, .n_30day_blocks_test'
```

Expected gate fields in output:
- `gate_verdict`: "MET" or "NOT_MET"
- `primary_contrast.relative_qlike_reduction_pct`: numeric (e.g., 3.2)
- `primary_contrast.ci_low`, `ci_high`: numeric (must have ci_high < 0 for improvement)
- `n_instruments_test`: integer (≥5 required)
- `n_30day_blocks_test`: integer (≥3 required)

---

## 7. Blockers & Next Materially Different Free Route

**No blockers.** All data is cached, protocol is frozen, splits are fixed, code primitives exist (src/volatility/*, src/features/*, src/models/*, src/eval/walkforward.py, src/eval/inference.py). The only gap is the orchestration script that assembles these pieces for the FCLR-009 panel specifically.

**If any step fails** (e.g., index-price data missing for premium feature), the protocol requires registering a separate price-source version — do NOT silently substitute. Record the exact shortfall and emit evaluation with the available feature set, noting the deviation in the summary.

**Do not** re-run FCLR-008, re-open sealed holdouts, or modify the frozen protocol. FCLR-009 is a distinct estimand window; its result stands independently.

---

## 8. Minimal Implementation Sketch (for the next agent)

Create a single script `scripts/run_fclr009_eval.py` that:
- Loads cached CSVs from `research_state/data_cache/*/markPriceKlines-*/*.csv` and `*fundingRate*/*.csv`
- Builds hourly panel indexed by (symbol, timestamp) with columns: close, funding_signed, (index_close if available)
- Computes features per `src/features/volatility.py` + `src/features/funding.py` + `src/volatility/feature_engineering.py`
- Constructs target via `forward_rv(close, horizon=24)` → log(target + 1e-12)
- Applies frozen splits from protocol (hardcode the ISO boundaries)
- Fits B0/B1/C1/C2 per `src/models/baselines.py` + extended C1/C2 with funding/premium/EMA features
- Uses `src/eval/inference.py:block_bootstrap_delta_ci_diagnostic` for C2-B1 ΔQLIKE CI
- Applies Holm correction across the 3 registered contrasts (C2vsB1, C1vsB1, C2vsC1)
- Emits JSON + MD summary with all required gate fields

**Verification test:** Run the script; confirm it produces the evaluation summary artifact with all gate fields populated and `gate_verdict` ∈ {MET, NOT_MET}.

**Latest session:** session_20261125T060000Z
