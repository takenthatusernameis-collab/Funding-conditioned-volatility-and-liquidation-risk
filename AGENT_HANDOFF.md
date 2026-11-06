# AGENT_HANDOFF.md

**TIMESTAMP (UTC):** 2026-11-06T23:10:18Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY:** FUNDING-CONDITIONED VOLATILITY & LIQUIDATION RISK
**STATUS:** Gate 3 (RV-only OOS baseline) SATISFIED. Funding ablations UNBLOCKED.

---

## WHAT WAS COMPLETED (2026-11-06)
- **RV-only baseline pipeline built and executed** (`scripts/run_rv_baseline.py`).
- Extracted/loaded BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT 1h klines (Jan–Mar 2024) from local zips via `src.ingest.loader`.
- Built panel with trailing RV features (`rv_trail_6/24/168`), `rv_lag`, and 24h forward RV target (`target_rv`).
- Chronological walk-forward split with purge/embargo (7d) and train-only normalization.
- **Results (aggregate, split 0 OOS test 2024-02-22→2024-03-31, n_train=2980, n_test=3600):**
  - Persistence (B1): QLIKE=40.4201, MAE=0.03123, RMSE=0.04310
  - RV-HAR (B2, RV-only): QLIKE=35.2103, MAE=0.03303, RMSE=0.04517
- Artifacts updated: `research_state/evaluation_summary.md`, `research_state/run_manifest.json`, `research_state/leakage_audit.md`.
- Bug fix: `src/volatility/eval.py` now treats NaN/inf correctly (QLIKE/MAE/MSE no longer return NaN when valid pairs exist).

## NEXT HEAVY WORK (DO IN ORDER)

### PHASE 3: FUNDING-CONDITIONED VOLATILITY ABLATIONS (GATE 4)
1. **Load funding data** for same symbols/period (fundingRate zips present). Align to 1h grid (forward-fill 8h funding where appropriate, document). Preserve signed funding and |funding|.
2. **Add funding features** (train-only stats): signed, absolute, trailing percentile/zscore (use `src/features/funding.py`/`src/volatility/feature_engineering.py`). Include basis/premium if available; **missing basis/spot = NaN, never zero**.
3. **Run ablations vs B2 (RV-only HAR)** on same walk-forward splits:
   - A: RV-only (done, baseline)
   - B: RV + signed funding
   - C: RV + |funding|
   - D: RV + funding + basis/premium (if coverage)
4. **Compute metrics** (QLIKE primary, MAE/RMSE), deltas vs B2, coverage by asset/period, block-aware CIs where feasible. Record in `research_state/evaluation_summary.md` (append or new section) and update manifest.
5. **Leakage check**: verify funding features computed with only past info; no lookahead in alignment.

### PHASE 4 (AFTER 3): LIQUIDATION RISK TRACKS
- Track A: observed liquidations (only if data available; check registry).
- Track B: modeled breaches (distance-to-liquidation proxies) — requires clear assumptions.
- Track C: volatility (done baseline + funding ablations).

## BOTTLENECKS REMOVED
- `scripts/run_rv_baseline.py` now exists and runs (Gate 3).
- NaN handling in metrics fixed for valid evaluation.

## CONSTRAINTS (NON-NEGOTIABLE)
- **NO TRADING/CREDS/PAID DATA** - local files only
- **NO WORKFLOW CHANGES** - do not touch `.github/workflows/`
- **LEAKAGE-RESISTANT** - chronological only, purge/embargo, train-only normalization
- **MISSING != ZERO** - treat missing basis/spot as NaN
- **TRACK SEPARATION** - do not conflate A/B/C
- **HEAVY WORK REQUIRED** - produce code/artifacts, not just status

**START WITH PHASE 3 STEP 1: load and align funding data.**
