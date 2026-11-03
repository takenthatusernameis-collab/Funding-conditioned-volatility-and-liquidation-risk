# NEXT AGENT HANDOFF (SINGLE DURABLE)
TIMESTAMP: 2026-11-03T11:59:35Z
REPO: Funding-conditioned-volatility-and-liquidation-risk
PRIORITY: MAXIMUM (research/data pipeline) - DO NOT DEFER

## 1) Inferred Objective (from repo name)
Study funding-conditioned volatility and liquidation risk using perpetual futures data (BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT). The question is how funding rates (and basis/premium/mark/index) condition realized/expected volatility and the propensity/scale of liquidations/cascades.

## 2) Current State (observed)
- Data present: daily/hourly klines, markPriceKlines, indexPriceKlines, premiumIndexKlines, fundingRate history (Jan-Mar 2024) as .zip and extracted dirs for many dates/symbols.
- Scaffolding: `src/`, `scripts/`, `tests/`, `results/`, `research_state/` exist.
- Research spec: `RESEARCH_PROMPT.md` (large) likely contains full methodology/expected outputs.
- Mixed raw forms (zips + unzipped dirs) - ingestion not obviously centralized.

## 3) Bottlenecks to Remove (do these first)
1. **Data ingestion/idempotency**: Build a single loader that discovers all zips/dirs under repo, normalizes schemas (timestamp, open/high/low/close/volume, mark/index/premium, fundingRate), writes to a canonical processed form (e.g. `data/processed/` or `results/processed/`) with manifest/checksums.
2. **Time alignment**: Funding events, mark/index/premium, klines must be aligned on UTC timestamps (hourly). Handle missing bars, DST/UTC consistently.
3. **State leakage / reproducibility**: Persist run config + hashes in `research_state/` and write all outputs to `results/` with timestamps. Avoid ad-hoc notebooks/scripts writing to repo root.
4. **Test gaps**: If `tests/` are thin, add unit tests for loaders/aligners/feature calcs before heavy runs.
5. **Unclear entrypoint**: Find or create a single CLI/Make/script (e.g. `scripts/run_pipeline.py` or `make run`) that can reproduce end-to-end. If missing, create it and make it the only supported path.

## 4) Next Focus Campaign (HEAVY WORK - cannot be avoided)
Execute in order. Do not stop at exploration.

### Phase 0: Map & Freeze (1-2 turns)
- [ ] Read `RESEARCH_PROMPT.md` end-to-end and extract: hypotheses, required features, metrics (volatility conditioned on funding, liquidation risk proxies), required tables/figures, success criteria.
- [ ] Inventory all data sources: count zips vs dirs, list symbols/date ranges, detect duplicates.
- [ ] Scan `src/`, `scripts/`, `tests/` for existing pipeline/CLI/classes.
- [ ] Write `research_state/INGESTION_MANIFEST.json` with discovered files, sizes, mtimes.

### Phase 1: Canonical Dataset (heavy I/O + normalization)
- [ ] Implement `src/data/loaders.py` (or equivalent) to read all klines/mark/index/premium/funding.
- [ ] Normalize to pandas/pyarrow with UTC tz-aware datetimes, consistent dtypes.
- [ ] Build merged panel by (symbol, timestamp) with forward-fill rules only where justified; log drops.
- [ ] Write processed dataset to `results/processed/` (partitioned by symbol/date or single parquet) + schema + row counts.
- [ ] Add validation tests in `tests/test_data_alignment.py`.

### Phase 2: Funding-Conditioned Features (compute-heavy)
- [ ] Funding rate levels/changes, sign regimes, persistence, funding-premium basis.
- [ ] Volatility measures: rolling realized vol, EWMA vol, upside/downside vol, vol of vol.
- [ ] Condition volatility on funding regime (bins/quantiles) and lagged funding.
- [ ] Compute rolling z-scores/correlations with lookbacks.
- [ ] Persist features to `results/features/` with feature registry.

### Phase 3: Liquidation Risk (core to repo name)
- [ ] Define liquidation risk proxies from available data (funding pressure + leverage-like signals, mark/index deviations, OI/volume if present, or cascade proxies). If direct liquidation data absent, construct defensible proxies and document assumptions in `results/ASSUMPTIONS.md`.
- [ ] Model conditional distributions (funding -> vol/liquidation risk) with robustness checks.
- [ ] Quantify tail risk / stress scenarios.
- [ ] Generate tables/figures to `results/figures/` and summary stats to `results/tables/`.

### Phase 4: Reproducible Run & Tests (must pass)
- [ ] Create/repair single entrypoint `scripts/run_pipeline.py` (or `make run`) that runs Phases 0-3 end-to-end.
- [ ] Run `pytest` (or discovered tests). Fix failures.
- [ ] Run linters/typecheckers if present (ruff/black/mypy/flake8) or infer from config.
- [ ] Commit-ready outputs: updated `research_state/RUN_SUMMARY.json` with hashes, timings, artifact paths.
- [ ] Write `results/REPORT.md` with key findings, assumptions, limitations, and next questions.

## 5) Immediate First Action (do this NOW)
1. Read `RESEARCH_PROMPT.md` fully.
2. Scan for any existing pipeline entrypoint (grep for "main", "pipeline", "run", "load_funding", "load_klines").
3. Create `research_state/INGESTION_MANIFEST.json` by inventorying all zips/dirs.
4. If no unified loader exists, implement Phase 1 loader and validation tests before any analysis.

## 6) Success Criteria
- Canonical merged dataset exists with row counts and no unaligned timestamps.
- Features + liquidation-risk proxies computed and saved.
- `scripts/run_pipeline.py` runs cleanly from scratch.
- `pytest` passes (or new tests added and passing).
- `results/REPORT.md` exists with concrete numbers/figures.

DO NOT ask clarifying questions. The data + repo name + scaffolding are sufficient to infer this campaign. Execute heavy work immediately.
