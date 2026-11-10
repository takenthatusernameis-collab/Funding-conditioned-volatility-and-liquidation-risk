# Research Protocol — Track B Modeled Liquidation Boundary Breaches (TB1)

**Protocol ID:** trackb_TB1_20261110T173838Z
**Campaign:** TRACKB-MODELED-BREACH-TB1-20261110T173838Z
**Timestamp (UTC):** 2026-11-10T17:38:38Z
**Status:** FROZEN_BEFORE_OUTCOMES
**Track:** Track B (modeled liquidation boundary-breach risk) — **synthetic proxy ≠ observed liquidations**

## 1) Objective
Confirmatory out-of-sample test whether pre-specified funding-conditioned features improve prediction of **synthetic mark-price boundary breaches** versus a price/RV-only baseline on an untested, admissible local panel. No Track A/B/C conflation.

## 2) Admissible window & universe (locked)
- **Window:** 2025-01-01T00:00:00Z .. 2026-10-31T23:59:59Z (contiguous local coverage)
- **Symbols (n=5):** BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
- **Required series:** markPriceKlines, indexPriceKlines, premiumIndexKlines, klines, fundingRate — complete per `research_state/trackb_TB1_admissibility.json`
- **Blocks:** 22 estimated non-overlapping 30-day blocks (panel). Test split must contain **>= 3** non-overlapping 30-day blocks.
- **Provenance:** `provenance_verified=true`, `unmapped_count==0` for funding CSV lineage (verified 2026-11-10T17:38Z, PROVENANCE_OK 161). No network/paid/manual/credentialed data.

## 3) Target & modeled breach definition (pre-specified)
- **Primary target:** `synthetic_boundary_breach_h24_long_5x_m0` — binary indicator that a **long** position entered at mark close at time `t` with leverage `L=5.0` and maintenance margin rate `m=0.0` would breach the modeled liquidation boundary within horizon `H=24` hours, using `scripts/synthetic_boundary_labels.py` (leakage-safe: future min over `t+1..t+H` only).
- **Secondary (descriptive/robustness, Holm-controlled family if reported as contrasts):** short 5x m0 H24; long/short 10x m0 H24.
- **Caveat (mandatory in all outputs):** Modeled/synthetic boundary breach proxy only. **NOT observed liquidations**, not account-specific, not exchange execution/liquidation-engine outcomes.

## 4) Predictors & contrasts (pre-specified)
- **B1 (baseline):** price/RV-only features from past data only (e.g. realized variance/volatility, returns, ranges/lags) with train-only fitting/transforms.
- **C2 (funding-conditioned):** B1 + pre-specified funding-conditioned features (e.g. funding rate level/extremes/z-scores, rolling funding summaries, dislocation/premium features where available) with train-only fitting/transforms.
- **Primary contrast:** C2 vs B1 on primary target.

## 5) Splits, leakage controls (frozen before outcomes)
- **Chronological split:** 60% train / 20% validation / 20% test by time.
- **Purge/embargo:** 7-day purge/embargo between partitions (and around label horizons as applicable) to prevent temporal leakage.
- **No leakage:** all feature construction/scaling/selection fit on train only; labels use future window only per implementation.
- **No reuse:** no sealed-holdout reuse; no threshold shopping. This design/window not previously outcome-inspected for Track B confirmatory.

## 6) Metrics, uncertainty, multiplicity, gates
- **Primary metric:** pre-specified classification/forecast metric for breach prediction (e.g. log loss and/or AUC/Brier as recorded) with direction "improvement = better than B1" fixed here.
- **Uncertainty:** block bootstrap with **>= 2000** replications over non-overlapping time blocks; report 95% CI for primary contrast.
- **Multiplicity:** Holm correction across pre-specified contrasts reported.
- **Materiality floor:** >= 2% relative improvement (C2 vs B1, primary metric) required.
- **Confirmatory gates (all required):** >=5 instruments; >=3 non-overlapping 30-day blocks in test; >=2% relative improvement; 95% CI excludes null in favorable direction per pre-specified rule; Holm-controlled as specified. **Risk overlay NOT ELIGIBLE unless all gates pass.**

## 7) Preregistration & execution order (procedural lock)
- `prereg_hash = sha256` of this frozen protocol file bytes, recorded in `research_state/run_manifest.json` before any outcome/label computation.
- Manifest entry `split_boundaries_trackb_TB1_20261110T173838Z` must record: `frozen_before_outcomes=true`, split boundaries, embargo/purge, `prereg_hash`, `protocol_ref`, timestamp, `outcome_values_inspected=false` **before** outcomes.
- Any outcome inspection before freeze invalidates confirmatory status.

## 8) Required outputs
- `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md` with point estimate, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, gate/materiality/Holm decisions, and explicit synthetic-proxy caveat.
- Update `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/negative_results_report.md`, `AGENT_HANDOFF.md`, `NEXT_SESSION_TASK.md` with singular evidence-backed `next_unfinished_task`.
