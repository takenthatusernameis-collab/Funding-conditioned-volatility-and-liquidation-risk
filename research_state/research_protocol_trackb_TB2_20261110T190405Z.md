# Research Protocol (FROZEN_BEFORE_OUTCOMES) — Track B TB2

Experiment ID: trackb_TB2_20261110T190405Z
Generated (UTC): 2026-11-10T19:04:05Z
Repo: Funding-conditioned-volatility-and-liquidation-risk
Status: FROZEN_BEFORE_OUTCOMES — no outcome/label computation may follow this freeze without a new experiment ID.

## 1. Track and target (modeled proxy only)
Track: B — modeled synthetic boundary-breach labels (NEVER observed liquidations).
Target: synthetic_boundary_breach_h168_long_10x_m0.0
- leverage = 10.0x, side = long, maintenance_margin_rate = 0.0, horizon = 168h
- Boundary price: long = entry*(1 - 1/lev + mmr); short = entry*(1 + 1/lev - mmr)
- Label uses mark-closes strictly after t (t+1..t+168h); no look-ahead/leakage.
- synthetic proxy != observed liquidation; does not reconstruct account margin/engine/forced liquidations.

## 2. Data panel (verified admissible, provenance locked)
Window: 2024-01-01 .. 2024-09-30 (inclusive)
Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
Required series: markPriceKlines, indexPriceKlines, premiumIndexKlines (1h) + fundingRate (8h)
Coverage: 5 symbols x 273 days; >=3 non-overlapping 30-day test blocks estimated.
Provenance: adjacent sha256 sidecars + manifest path+sha256 lineage; provenance_verified=true, unmapped_count==0.
Data hash provenance recorded per-file in run_manifest.json / data_cache manifests.
No network / no paid / no manual / no credentialed data.

## 3. Splits (chronological, frozen before outcomes; 7-day purge/embargo)
Rule: chronological 60/20/20 split by unique UTC timestamps across the common 5-symbol panel;
7-day purge/embargo at all boundaries; no target interval overlaps train/val/test.
- train: 2024-01-01T00:00:00Z .. 2024-06-12T00:00:00Z
- validation: 2024-06-19T00:00:00Z .. 2024-08-06T00:00:00Z
- test: 2024-08-13T00:00:00Z .. 2024-09-30T00:00:00Z
embargo_days: 7
split_boundaries_trackb_TB2_20261110T190405Z.frozen_before_outcomes: true

## 4. Predictors (causal, training-only normalization)
B1 baseline (price/RV-only): trailing realized variance RV1h/RV24h/RV168h from mark-price log returns.
C2 candidate (funding-conditioned): B1 + signed funding rate + abs funding percentile (prior 90d, >=30 obs)
  + mark/index premium + mark/EMA24 distance.
Feature standardization/fitting parameters from training data only. Missing features remain missing (no fill).

## 5. Metrics (primary contrast C2 vs B1)
Primary metrics: Log Loss, Brier score (lower is better); reported per-symbol and pooled.
Relative improvement vs B1; materiality floor >= 2% relative reduction.
Uncertainty: block bootstrap, >=2000 deterministic-seed replicates, block size 30 days (720h).
Multiplicity: Holm correction across the 2 pre-specified metrics (alpha=0.025/metric).
CI: two-sided 95% for paired loss difference; must exclude null in favorable direction.

## 6. Gates (all required for FORECAST_GATE_PASSED)
- >=5 instruments in paired OOS panel; >=3 non-overlapping 30-day test blocks
- >=2% relative improvement (Log Loss) AND CI excludes null in favorable direction
- Holm-adjusted multiplicity passes
- No unresolved leakage/label/source/timestamp defect; synthetic-proxy caveat stated

## 7. Event adequacy (pre-freeze, from local data)
Frozen test split must contain >0 positive synthetic breach labels (report counts per split/symbol/overall).
No threshold shopping after this freeze. If this design yields 0 test positives, the window is inadmissible
and a new experiment ID/prereg is required (no holdout reuse).

## 8. Constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping;
no sealed-holdout reuse; no Track A/B/C conflation; preregister/freeze before outcomes;
no risk overlay until forecast gate passes; no .github/workflows edits.

prereg_hash: 9de16e7d2b2c80f6ac57d87b6eb150c145bfe9f3168d7ac3d94472f740f7b91f
