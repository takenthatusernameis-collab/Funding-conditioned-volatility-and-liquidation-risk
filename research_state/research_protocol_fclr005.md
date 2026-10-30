# FCLR-005 Research Protocol — Track A Observed Liquidation Outcomes (2026 expansion)

Protocol version: FCLR-005 v1.0
Status: PROTOCOL_FROZEN (pre-registered before any outcome inspection)
Date frozen: 2026-10-30T04:30:00Z
Experiment ID: FCLR-005
Primary hypothesis: FCLR-H004 (observed liquidation outcomes)
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk

## Rationale (evidence-based adaptive scope expansion, RESEARCH_PROMPT §16)

FCLR-H004 Track A is BLOCKED for the frozen 2024 test windows (FCLR-001/002/003/004): no admissible unauthenticated public observed-liquidation census exists for 2024 (research_state/liquidation_sources_enumeration.md §1-4, §84-92; research_state/binance_source_probe.md). Three materially distinct routes spanning two source families were exhausted: (1) Binance data.binance.vision archives + fapi forceOrders (HTTP 404 / 451), (2) Bybit/OKX/Deribit venue-native archives (no unauthenticated liquidation census), (3) HF/Zenodo/GitHub dataset repos (HF crypto-liquidation-ticks admissible but covers only 2026).

Per §16, after exhaustive routes, create the smallest useful alternative experiment with a new ID. Smallest admissible scope expansion: evaluate Track A on the 2026 window where an admissible, unauthenticated, CC-BY-4.0 observed-liquidation census exists (HF ochinimus/crypto-liquidation-ticks, Bybit complete allLiquidation stream). Decision recorded at research_state/fclr_h004_tracka_viable.json (2026-10-30T02:15:00Z).

This experiment is PILOT/EXPLORATORY on the 2026 window. It does NOT clear any sealed FCLR-001-004 forecast gate, does NOT change FCLR-H004's frozen-2024 BLOCKED status, and does NOT justify a risk overlay. Absence of events in any sub-interval is never labeled "no liquidation."

## 1. Unit, timing, universe

- Unit: one eligible linear perpetual contract × one fully closed UTC hourly timestamp.
- Forecast timestamp t immediately after all data for closed hour t available; no same-bar / future leakage.
- Universe (frozen): 5 symbols BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT on Binance USDⓈ-M perpetuals (feature side) cross-referenced to Bybit liquidation labels (label side).
- Feature history: 2026-04-01 .. 2026-08-06 (complete unauthenticated cache in research_state/data_cache/<SYM>_2026_*/; mark/index/premium klines 1h + monthly fundingRate).
- Label window: 2026-07-08 16:42:32 .. 2026-08-06 23:59:42 UTC (HF crypto-liquidation-ticks coverage). First forecast origin requires >=90d funding history and >=168h RV history → earliest origin 2026-07-08.
- Label source: research_state/data_cache/liquidations_full_20260807.csv (sha256 to be recorded in run manifest), schema [ts_ms, utc_time, symbol, exchange, event, size, price, usd], events {short_liquidated, long_liquidated}.
- Bybit rows are the complete-census arm (allLiquidation stream, every liquidation at 500ms). Binance/OKX rows are undercounted (snapshot cap 1 order/symbol/1000ms; 1 update/sec) → lower-bound partial evidence only, never a census.
- Universe change artifact 2026-07-12 16:23 UTC (5 -> 800 symbols): filter to 5-symbol universe for continuity, or start after 2026-07-12 16:23 UTC. Protocol starts labels at 2026-07-08; pre-2026-07-12 Bybit rows kept but flagged.

## 2. Target (observed liquidation, Track A only)

- Target: hourly liquidation-event count and USD notional intensity per symbol, long and short separate.
- long_liquidated → short-side liquidation event count/intensity; short_liquidated → long-side. Sign convention documented; never merge venues/tracks.
- Target constructed from observed Bybit rows only (census arm). Binance/OKX rows never used for the binary presence/absence target.
- Missing event coverage must NOT be interpreted as zero liquidations. Hours with zero Bybit rows = observed-zero in the census arm only; not an absolute zero claim.
- No modeled boundary-breach labels mixed in (Track B/C strictly separate; scripts/synthetic_boundary_labels.py not used here).

## 3. Predictors (frozen, causal, computed at/before t from Binance mark data)

- RV1h, RV24h, RV168h: trailing realized variances from hourly mark-price log returns.
- Signed funding: latest funding observation availability <= t, sign retained.
- Funding extremeness: percentile rank of |funding| vs preceding 90 calendar days only; >=30 valid obs required else missing (no zero-fill).
- Premium feature: mark/index - 1 when contemporaneously aligned within frozen tolerance.
- Smoothing/dislocation: mark / EMA24(mark) - 1, EMA from fully closed prior bars only.
- Missing features: row dropped for that model comparison; no forward-fill / zero-fill across splits.

## 4. Models and primary contrast

- B0: persistence → forecast next-hour liquidation intensity by trailing intensity.
- B1: volatility-only → logistic regression on log RV features.
- C1: B1 + signed funding + abs-funding percentile.
- C2: C1 + mark/index premium + mark/EMA24 distance.
- OLS/logistic as fixed form; no regularization, no hyperparameter search, no threshold tuning on outcomes.
- Primary contrast: C2 vs B1 on out-of-sample Brier / log-loss for hourly liquidation presence (binary) and count intensity, long and short separate.

## 5. Splits, embargo, inference

- Chronological train / validation / test within the 2026-07-08 .. 2026-08-06 label window (~30 days).
- LIMITATION: window is ~30 days → cannot satisfy the >=3 non-overlapping 30-day blocks confirmatory requirement. FCLR-005 is therefore PILOT/exploratory; report block counts explicitly; no confirmatory claim.
- 7-day purge/embargo between partitions where feasible given window length; no target interval overlaps train/val/test.
- Metrics: Brier score, log-loss, calibration slope/intercept, precision-recall, AUPRC (secondary descriptive). Pre-specified alert budget NOT available (pilot) → report precision at observed base rate only, no threshold shopping.
- Uncertainty: block bootstrap over complete UTC hours, deterministic seed; report leave-one-symbol-out stability.

## 6. Acceptance criteria (recorded, not outcome-dependent)

- Pre-registered before evaluation; appended to hypothesis_registry.json; run manifest with data hashes, git SHA, timestamps, source vintages, sample counts.
- Provenance recorded: HF dataset URL, license CC BY 4.0, access date, row counts per venue/symbol, completeness diagnosis (Bybit census vs Binance/OKX undercount).
- Results reported honestly with base rate, event prevalence, coverage gaps; no event-free inference from missing data.
- If gate-equivalent conditions not met (expected given ~30-day window): status PILOT_ONLY / EXPLORATORY_ONLY, FCLR-H004 remains BLOCKED for frozen 2024; document exact shortfall; no threshold relaxation after seeing outcomes.

## 7. What must NOT be done

- Do not re-run sealed FCLR-001-004 forecast gates. Do not modify .github/workflows. Do not build risk overlay / simulation / merge tracks.
- Do not label modeled boundary breaches as observed liquidations. Do not use Binance/OKX undercounted rows as census. Do not infer event-free intervals from missing data. Do not claim this clears any frozen gate.

## Links

- research_state/fclr_h004_tracka_viable.json
- research_state/liquidation_sources_enumeration.md
- research_state/binance_source_probe.md
- scripts/h004_audit.py
- RESEARCH_PROMPT.md §7.2, §15, §16
