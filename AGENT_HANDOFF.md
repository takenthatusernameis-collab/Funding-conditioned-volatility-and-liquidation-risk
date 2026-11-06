# AGENT_HANDOFF.md

**TIMESTAMP (UTC):** 2026-11-06T21:40:32Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**SESSION GOAL:** UNBLOCK DATA → BUILD MINIMAL PIPELINE → RUN RV-ONLY OOS BASELINE (GATE 3)

---

## REPO PRIORITY (DERIVED)
This repo is **funding-conditioned volatility and liquidation risk**. The correct order is non-negotiable:
1. **Make data loadable** (extract/parse zips into normalized UTC frames)
2. **Freeze protocol** (already frozen, do not re-freeze)
3. **Prove RV-only baseline OOS** (Gate 3) - without this you cannot measure incremental value of funding
4. **Only then** test funding+price ablations vs RV-only

Everything else is noise until Gate 3 is satisfied.

---

## CURRENT BOTTLENECKS (REMOVE NOW)
| Bottleneck | Status | Action |
|---|---|---|
| **Data unreadable** | CRITICAL | Zips at root not extracted. Build extraction + normalization. |
| **No usable ingestion/features pipeline** | CRITICAL | `src/` may exist but likely incomplete. Build minimal `src/ingest/`, `src/features/`, `src/models/baselines.py`, `src/eval/walkforward.py`. |
| **RV-only baseline not run** | CRITICAL | `research_state/evaluation_summary.md` says "Not yet computed". This blocks all funding tests. |
| **Data inventory missing machine-readable** | HIGH | Need `research_state/data_inventory.json` with all zips, sizes, mtimes. |
| **Source registry incomplete** | HIGH | Need concrete entries for Binance public archive zips actually present. |

---

## HEAVY WORK PLAN (DO IN ORDER)

### PHASE 0: DATA DISCOVERY & EXTRACTION (BLOCKING - DO FIRST)
- [ ] **Inventory**: Walk repo root and all `*.zip` files. Write `research_state/data_inventory.json` (path, symbol, type, date, size_bytes, mtime).
- [ ] **Extract sample**: Extract 1-2 days for BTCUSDT and ETHUSDT across klines, funding, index/mark/premium into `data/raw/` (gitignored). Do NOT extract everything.
- [ ] **Infer schema**: Inspect CSVs - column names, dtypes, timestamp units (ms/s), timezone, symbol naming. Document in notes.
- [ ] **Build registry**: Update `research_state/data_source_registry.json` with tested extraction, coverage, gaps, unauthenticated access, acceptance status.
- [ ] **Fixtures**: Add tiny fixtures under `tests/fixtures/` from samples for deterministic tests.

### PHASE 1: MINIMAL PIPELINE (HEAVY ENGINEERING)
- [ ] **Ingest**: Implement `src/ingest/loader.py` to read zips/CSV, normalize to UTC, deduplicate, hash, checkpoint.
- [ ] **Features**: Implement `src/features/funding.py` (signed, |f|, trailing pct/standardized with rolling history), `src/features/volatility.py` (RV 6h/24h/168h), `src/features/price.py` (premium/mark-index/MA dev). Treat missing basis as NaN (NEVER zero).
- [ ] **Baselines**: Implement `src/models/baselines.py` with persistence (lagged RV) and RV-only/HAR.
- [ ] **Walk-forward**: Implement `src/eval/walkforward.py` with chronological splits, purge/embargo >= max horizon, train-only normalization.
- [ ] **CLI/script**: Add `scripts/run_rv_baseline.py` to run end-to-end on extracted universe.

### PHASE 2: MANDATORY BASELINE GATE (PROVE IT)
- [ ] **Run RV-only baseline**: Execute walk-forward on BTC/ETH/SOL/XRP using available data (Jan-Mar 2024). Compute QLIKE (primary), MAE/RMSE on log/level RV, block-aware CIs where feasible.
- [ ] **Record results**: Write full `research_state/evaluation_summary.md` with sample sizes, coverage by asset/period, exclusions, metrics, CIs, sanity checks.
- [ ] **Manifest**: Update `research_state/run_manifest.json` with git SHA, timestamps, config, data hashes, counts, versions, status=rv_baseline_complete.
- [ ] **Leakage audit**: Verify no future leakage (normalization train-only, purge/embargo applied). Update `research_state/leakage_audit.md` if needed.

**DO NOT proceed to funding ablations until Phase 2 is complete and committed to artifacts.**

---

## NEXT SINGLE TASK (START HERE - DO NOT DEVIATE)
**TASK:** `PHASE 0.1 - Inventory + Sample Extraction + Fixture Test`

**IMMEDIATE ACTIONS:**
1. Run inventory of all `*.zip` at repo root → write `research_state/data_inventory.json`
2. Extract 1 day of klines + funding for BTCUSDT and ETHUSDT into `data/raw/`
3. Create `data/raw/` if missing (add to `.gitignore` if not present)
4. Write `research_state/data_source_registry.json` entries for those extractions (tested, unauthenticated, coverage)
5. Add `tests/test_timestamp_parsing.py` that loads fixtures and asserts normalized UTC timestamps
6. Run the test - if it passes, you've unblocked data loading

**SUCCESS CRITERIA:** Can load extracted samples into DataFrames with normalized UTC timestamps, column semantics known, fixtures exist, inventory written. No modeling yet.

---

## CONSTRAINTS (NON-NEGOTIABLE)
- **NO TRADING**: No live/paper trading, orders, API keys, credentials, paid data
- **NO WORKFLOW CHANGES**: Do not modify `.github/workflows/`
- **LEAKAGE-RESISTANT**: Chronological OOS only, no random splits, purge/embargo, train-only normalization
- **TRACK SEPARATION**: Track A (observed liquidations) vs Track B (modeled breaches) vs Track C (volatility). Never conflate
- **MISSING != ZERO**: Treat missing basis/spot as missing
- **PRESERVE NEGATIVES**: Document failures/inconclusives
- **HEAVY WORK REQUIRED**: Every session must create measurable engineering/data/research progress. No status-only files.

**THIS IS THE SINGLE DURABLE HANDOFF. START AT PHASE 0.1. DO THE HEAVY WORK.**
