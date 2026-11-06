# AGENT_HANDOFF.md

**TIMESTAMP (UTC):** 2026-11-06T20:36:32Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**SESSION GOAL:** Unblock ingestion → freeze protocol → establish RV-only OOS baseline before adding funding features

---

## IMMEDIATE MANDATE (DO NOT DEVIATE)
Based on the repo name and the research prompt, this project is about funding-conditioned volatility and liquidation risk. The correct order is: get data loadable, freeze the protocol, prove RV-only baseline out-of-sample, then test incremental funding value. Do the heavy engineering work first.

---

## CURRENT GROUND TRUTH TO ESTABLISH
Before doing any modeling, you MUST inventory the working tree:

- [ ] Read `RESEARCH_PROMPT.md`, `AGENT_HANDOFF.md` (this file), `requirements.txt`, and any `README*` files.
- [ ] Inspect `src/`, `scripts/`, `tests/`, and `research_state/` to see what actually exists (do not assume emptiness).
- [ ] Inventory all zip files at repo root (count by symbol/type/date). Write a machine-readable inventory to `research_state/data_inventory.json` with paths, sizes, and mtimes.
- [ ] Identify which archives are klines/index/mark/premium/funding for BTC/ETH/SOL/XRP (Jan-Mar 2024) and note gaps.

---

## PRIORITIZED EXECUTION PLAN (HEAVY WORK)

### PHASE 0: DATA DISCOVERY & EXTRACTION (BLOCKING - DO FIRST)
**Goal:** Make data readable without internet/auth.

- [ ] Create `data/raw/` (gitignored) and extract a small representative sample (1-2 days per symbol and per data type: klines, funding, index/mark/premium). Do not extract everything blindly.
- [ ] Infer schemas: column names, dtypes, timestamp units (ms/s), timezone assumptions, symbol naming, and units.
- [ ] Build `research_state/data_source_registry.json` with Binance public archive entries (paths used, unauthenticated access, tested extraction, coverage, known gaps, license/terms). Mark acceptance status per source.
- [ ] Write fixtures under `tests/fixtures/` from the extracted samples for deterministic tests.

### PHASE 1: PROTOCOL FREEZE (BLOCKING - BEFORE HOLDOUT)
**Goal:** Lock the evaluation before touching holdout.

- [ ] Create/freeze `research_state/research_protocol.md` with: universe, features (signed/abs funding, RV 6h/24h/168h, RV ratios, price dislocation/basis), targets (forward RV 6h/24h/72h/7d), baselines (persistence + RV-only/HAR), walk-forward CV, purge/embargo, sealed holdout boundaries (set from coverage, not arbitrary), metrics (QLIKE/MAE/RMSE/Brier where applicable), and decision gates.
- [ ] Create `research_state/hypothesis_registry.json` with primary (funding+RV -> future RV/stress) and secondary (Shek replication) hypotheses and states.
- [ ] Create `research_state/leakage_audit.md` with explicit checks (timestamp alignment, normalization using train-only params, no future leakage).

### PHASE 2: MINIMAL PIPELINE (HEAVY ENGINEERING)
**Goal:** Deterministic, restartable ingestion/features/eval.

- [ ] Implement `src/ingest/` to read zips/CSV/JSON, normalize to UTC, deduplicate, checkpoint, and log hashes.
- [ ] Implement `src/features/` for funding (signed, abs, trailing percentile/standardized using rolling history only), RV, and price dislocation/mark-index basis. Treat missing basis as missing (never zero).
- [ ] Implement `src/eval/walkforward.py` (or equivalent) with purge/embargo and train-only normalization.
- [ ] Implement `src/models/baselines.py` for persistence and RV-only/HAR baseline.

### PHASE 3: MANDATORY BASELINE GATE (PROVE IT)
**Goal:** No funding features until this passes.

- [ ] Run RV-only baseline out-of-sample via walk-forward on the constructed universe. Compute QLIKE, MAE/RMSE on log/level RV as appropriate with block-aware uncertainty.
- [ ] Write `research_state/evaluation_summary.md` with sample sizes, coverage, metrics, CIs, and exclusions.
- [ ] Write `research_state/run_manifest.json` with git SHA, timestamps, config, data hashes, counts, versions, and status.
- [ ] Only after this gate is satisfied, implement funding ablations (RV+funding, RV+funding+price) and compare incrementally.

---

## BOTTLENECKS TO REMOVE NOW
1. **Data unreadable** - zips not extracted/parsed. Fix in Phase 0.
2. **No frozen protocol** - prevents leakage-resistant evaluation. Fix in Phase 1 (blocks holdout).
3. **No baseline** - cannot measure incremental value of funding. Fix in Phase 3 (hard gate).
4. **Unclear existing code** - may duplicate or conflict. Read `src/`, `scripts/`, `tests/` first and extend minimally; do not add redundant controllers/schedulers/agents.

---

## NEXT SINGLE TASK (START HERE)
**TASK:** `PHASE 0.1 - Inventory and sample extraction`
**ACTIONS:**
1. Run a quick inventory of all `*.zip` files (count by prefix/symbol/date).
2. Extract 1 day of klines + funding for BTCUSDT and ETHUSDT into `data/raw/` to infer schema.
3. Create `research_state/data_inventory.json` and initial `research_state/data_source_registry.json` entries.
4. Add a tiny fixture-based test to validate timestamp parsing for the sample.

**SUCCESS CRITERIA:** You can load the sample into a dataframe with normalized UTC timestamps and know column semantics. No modeling yet.

---

## CONSTRAINTS (NON-NEGOTIABLE)
- No trading, paper trading, live orders, credentials, API keys, paid data, or workflow changes under `.github/workflows`.
- Chronological OOS only. No random splits. Freeze protocol before holdout.
- Separate observed liquidations (Track A) from modeled boundary breaches (Track B). Never conflate them.
- Treat missing basis/spot as missing, not zero.
- Preserve negative/inconclusive results.
- Keep raw data out of git; commit code, manifests, provenance, and reports.

**THIS HANDOFF IS DURABLE. DO THE HEAVY WORK IN THIS ORDER.**
**NEXT AGENT: START AT PHASE 0.1. DO NOT SKIP TO ANALYSIS.**