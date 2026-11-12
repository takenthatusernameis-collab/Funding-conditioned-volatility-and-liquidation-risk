# Track A Volatility Preregistration — TRACKA-VOL-20261111T234918Z

**Preregistered (UTC):** 2026-11-11T23:56:27Z (frozen before any outcome computation)
**Campaign:** `GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS` (repo-priority funding-conditioned volatility)
**Venue:** Hyperliquid perpetuals only (no Binance/2024 conflation). Cached admissible data only.

## Claim / Hypothesis
Funding-conditioned features (C2) improve out-of-sample forecasting of **next-24h realized variance** vs RV-only baseline (B1), measured by QLIKE (lower better), on an untested admissible cached Hyperliquid panel.

## Data (cached, ex-ante audited)
- 1h candles: `research_state/data_cache/hyperliquid_candles/{COIN}/{YYYY-MM}.json` (+ `.accessed.json/.sha256`). Ex-ante: 2025-11..2026-04 files empty for candidate coins; **2026-05..2026-10** populated for core coins. Months used: 2026-05..2026-10.
- Funding: `research_state/data_cache/hyperliquid_funding/{COIN}.json` (hourly fundingRate, premium).

## Universe (frozen ex ante)
Coins: `AVAX, BNB, BTC, DOGE, ETH, LINK, SOL, SUI, XRP` (9). Selected as cached-admissible coins with complete 2026-05..2026-10 candle+funding coverage. ADA excluded (lacks 2025-11..2026-04 and not in fixed 12-month core). No outcome-based selection. Min paired instruments: **>=5**.

## Target
`RV_{t,t+24h} = sum_{i=1}^{24} (log(close_{t+i}/close_{t+i-1}))^2` (forward 24h, 1h bars), causal label construction requiring complete future horizon.

## Features (all causal/trailing/as-of)
- B1: `rv1h`, `rv24h`, `rv168h` (trailing sums of squared 1h log returns)
- C2: B1 + `funding_rate` (as-of <=t), `abs_funding`, `premium` (as-of <=t), `ema_dist = close_t/EMA24(close)_t - 1`

## Models & Contrast
- **B1:** linear model on log(target+eps) using B1 features, train-only fit.
- **C2:** linear model on log(target+eps) using B1+C2 features, train-only fit.
- **Primary contrast:** C2 vs B1.

## Splits / Evaluation Design
- Chronological, **>=3 non-overlapping 30-day test blocks** with **>=7-day embargo** between train/test-block boundaries as applicable.
- Last contiguous eligible period partitioned into 3 test blocks; earlier data = train. Exact boundaries recorded from available timestamps before scoring.
- Seed: `20261111`.

## Metric & Materiality (all required)
- Metric: **QLIKE** = mean(y/yhat - log(y/yhat) - 1), y>0,yhat>0, lower better.
- **>=2% relative reduction** `100*(QLIKE_B1-QLIKE_C2)/QLIKE_B1 > 2%` in favor of C2.
- **95% block-bootstrap CI excludes zero** in favor of C2 (circular block bootstrap, block=24h, 2000 reps, seed 20261111).
- **>=5 paired instruments**, **>=3 non-overlapping 30-day test blocks**, **>=7-day embargo**.

## Hard INADMISSIBLE / Bans
- No outcome peeking before freeze; no threshold-shopping; no post-outcome prereg edits; no sealed-holdout reuse.
- No Binance/2024 conflation; Hyperliquid-only; observed/cached inputs only (no modeled/proxy liquidation labels).
- No `.github/workflows` edits; no redundant network polling. Gate 4 Branch 1 only on valid `fclr016_v5_terms_evidence_RESOLVED_*` with `status=RESOLVED_VERIFIED`, required fields, human/legal attestation, `fabricated=false` (absent now).

## Planned Artifacts
- `research_state/tracka_prereg_volatility_20261111T234918Z.{json,md}`
- `research_state/tracka_vol_panel_20261111T234918Z.parquet`
- `research_state/tracka_vol_panel_build_report_20261111T234918Z.json`
- `research_state/evaluation_summary_TRACKA-VOL-20261111T234918Z.md`
- State updates: `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`, `final_confirmatory_verdict.md` (append-only addendum)

**Verdict outcomes:** MET / NOT_MET / INADMISSIBLE per pre-registered criteria with full evidence.
