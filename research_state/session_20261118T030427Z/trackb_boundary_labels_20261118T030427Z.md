# Track B — Modeled Liquidation-Boundary Labels (feasibility/protocol, cached data)

**Session:** `session_20261118T030427Z`
**Timestamp (UTC):** 2026-11-18T03:04:27Z
**Campaign:** `FCLR-VOL-LIQ-FORECAST-01-20261118T023259Z` (ACTIVE_CAMPAIGN)
**Network:** none. **Parquet engine:** none. **Observed liquidation labels:** NOT used/available here (Track B = modeled/synthetic boundary breach only).

## Objective
Specify and feasibility-check modeled liquidation-boundary-breach labels from public mark-price data on disk (ZIP/CSV/dir twins only), for predefined hypothetical leverage/margin scenarios. These labels are **synthetic/modeled** — they do **not** reconstruct account-specific liquidation mechanics, portfolio margin, liquidation engine execution, insurance-fund behavior, or actual forced liquidations. Never label as observed.

## Cached mark-price data available (read-only)
- `research_state/data_cache/<SYMBOL>_YYYY_MM/markPriceKlines-YYYY-MM-DD/` (zip/csv per day) present broadly for BTC/ETH/SOL/XRP/BNB across 2024-01..2026-11 (per `cache_symbol_months_20261118T030427Z.json` / coverage audit). 2024 Q1-Q4 has dense daily mark-price kline dirs for all 5 instruments.
- Also index/premium klines and 1h klines available; mark price is the appropriate public proxy for boundary checks per RESEARCH_PROMPT §5 Track B.
- **No parquet required**; readers must use zip/csv/dir.

## Modeling protocol (predefined, to freeze in outcome-blind prereg before label construction)
1. **Scenarios (hypothetical, fixed ex ante):** isolated-margin long/short at leverage levels L ∈ {5x, 10x, 20x} (example set — finalize in prereg). Entry at bar-open mark; maintenance margin rate `mmr` and initial margin assumptions must be stated from documented/public contract parameters if verifiable on disk, else use explicit simplified approximations and label as `APPROXIMATE_MODEL`.
2. **Boundary definition:** breach when mark price crosses maintenance boundary for the scenario within horizon H (e.g., 24h/4h bars). Compute path-wise using mark-price series; record first-breach time, no lookahead.
3. **Labels:** binary `breach_h` per (symbol, t, scenario, side); optionally distance-to-boundary. Store with scenario metadata, parameters, and provenance of mark source.
4. **Splits/evaluation:** chronological, 7d purge/embargo, train-only normalization; compare predictors (RV-only baseline vs funding+RV) on modeled-breach probability/forecast metrics — only after forecasting gate logic and with clear synthetic-label caveat.
5. **Leakage controls:** no future mark prices in features; features at/before t; horizon labels use t+1..t+H only; no sealed-holdout reuse.

## Feasibility assessment
- **Data:** FEASIBLE on cached mark-price ZIP/CSV for 5 instruments over 2024+ windows (subject to per-bar completeness check). No network/parquet needed.
- **Execution:** labeling/feature computation implementable in stdlib+csv/zip; statistical modeling/evaluation scripts in repo assume numpy/pandas — **blocked in this environment** without approved runtime. A minimal stdlib breach-label generator could be built, but downstream forecast evaluation pipeline would still need numerical stack.
- **Scientific caveat:** modeled breaches are a proxy stress outcome (Track B/C), not observed liquidations (Track A). Any result must be reported with that boundary and cannot claim observed-liquidation predictiveness.

## Recommended next step
- Write outcome-blind prereg in session dir fixing scenarios (L, sides, mmr assumption/source, horizon), symbol set, window, split calendar, and metrics.
- Build a zip/csv mark-price loader + breach-label generator (stdlib) producing a session-local label artifact; then run forecast comparison in numpy-capable environment. Record completeness/leakage audit.

## Status
**PROTOCOL/FEASIBILITY DOCUMENTED (heavy); label generation/evaluation NOT EXECUTED due to missing numerical runtime and absent outcome-blind prereg freeze in this session.**
