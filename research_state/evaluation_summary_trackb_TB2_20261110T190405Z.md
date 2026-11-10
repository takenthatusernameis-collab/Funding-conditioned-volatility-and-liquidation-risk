# Evaluation Summary — Track B TB2 Confirmatory

Experiment: trackb_TB2_20261110T190405Z  (frozen prereg v1.0)
Repo: Funding-conditioned-volatility-and-liquidation-risk
Git SHA: 628f81018b73ce6b6063359a294eddbe84583ca0
Generated (UTC): 2026-11-10T20:00:21Z
Prereg hash: 46dcfb56c279e853230e75f6cb246ed878d765d2b399ea9a2e21c41581194adb
Frozen before outcomes: True
Outcome values inspected: False

## Design (frozen prereg trackb_TB2_20261110T190405Z)
- Track: B — modeled synthetic boundary-breach labels (proxy; never observed liquidations)
- Target: synthetic_boundary_breach_h168_long_10.0x_m0.0
- Window: 2024-01-01 .. 2024-09-30 (5 symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT)
- Splits (chronological, 7-day purge/embargo):
  - train: 2024-01-01T00:00:00Z .. 2024-06-12T00:00:00Z
  - validation: 2024-06-19T00:00:00Z .. 2024-08-06T00:00:00Z
  - test: 2024-08-13T00:00:00Z .. 2024-09-30T00:00:00Z
- Predictors (training-only standardization; missing remains missing):
  - B1 (RV-only): RV1h, RV24h, RV168h (trailing realized variance from mark-price log returns)
  - C2 (funding-conditioned): B1 + signed funding + abs funding percentile (prior 90d, >=30 obs)
    + mark/index premium + mark/EMA24 distance
- Metrics: Log Loss, Brier (lower better); primary contrast C2 vs B1, paired
- Materiality: >=2% relative Log Loss reduction vs B1
- Uncertainty: block bootstrap >=2000 deterministic-seed replicates, 30-day blocks
- Multiplicity: Holm across 2 pre-specified metrics (alpha=0.025/metric)

## Caveat
- synthetic proxy != observed liquidations; does not reconstruct account margin/engine/forced liquidations
- no risk overlay until forecast gate passes

## Event adequacy (frozen label, pre-freeze)
- Train origins: 19565, labeled: 19565
- Val origins: 5765, labeled: 5765
- Test origins: 5765, labeled: 5040
- Test positives: 619, negatives: 4421, prevalence=0.1228
  - per symbol test positives:
    - BTCUSDT: positives=64, negatives=944, labeled=1008
    - ETHUSDT: positives=205, negatives=803, labeled=1008
    - BNBUSDT: positives=96, negatives=912, labeled=1008
    - SOLUSDT: positives=184, negatives=824, labeled=1008
    - XRPUSDT: positives=70, negatives=938, labeled=1008

## Fit (training data only; no holdout tuning)
- Train C2-eligible origins: 7480 (B1 same common sample for paired parity)
- Logistic MLE (fixed 1e-6 ridge for numerical stability; not a tuned hyperparameter)
- B1 coefs (intercept, rv1h, rv24h, rv168h): -1.609992, 0.018363, 0.173258, -0.102380
- C2 coefs (intercept, rv1h, rv24h, rv168h, signed_funding, abs_fund_pct, prem, ema_dist): -1.654326, 0.022189, 0.163297, -0.081525, 0.054486, -0.256256, 0.385403, -0.015430

## Test-set results (frozen holdout, paired C2 vs B1)
- Test common-eligible origins: 5040
- Pooled B1 Log Loss: 0.292447
- Pooled C2 Log Loss: 0.287540
- Pooled B1 Brier: 0.073713
- Pooled C2 Brier: 0.072569
- Paired mean Log Loss diff (C2 - B1): -0.000932
- Paired mean Brier diff (C2 - B1): -0.000315
- Relative Log Loss reduction vs B1: 1.6781%  (materiality floor >=2%)

## Per-symbol test results (common-eligible sample)
- BTCUSDT: n=1008, positives=64, B1_LL=0.284733, C2_LL=0.273485, B1_Brier=0.070178, C2_Brier=0.067544, rel_LL_reduction=3.9504%
- ETHUSDT: n=1008, positives=205, B1_LL=0.509904, C2_LL=0.515295, B1_Brier=0.163439, C2_Brier=0.164928, rel_LL_reduction=-1.0573%
- BNBUSDT: n=1008, positives=96, B1_LL=0.336030, C2_LL=0.331935, B1_Brier=0.091395, C2_Brier=0.089680, rel_LL_reduction=1.2189%
- SOLUSDT: n=1008, positives=184, B1_LL=0.471881, C2_LL=0.482080, B1_Brier=0.148306, C2_Brier=0.150736, rel_LL_reduction=-2.1613%
- XRPUSDT: n=1008, positives=70, B1_LL=0.292447, C2_LL=0.287540, B1_Brier=0.073713, C2_Brier=0.072569, rel_LL_reduction=1.6781%

## Uncertainty — block bootstrap (test split)
- Bootstrap replicates: 2000 (deterministic seed 20261110)
- Block size: 30 days; non-overlapping test blocks: 2
- Log Loss paired diff mean: -0.000932
- Log Loss 95% CI (paired diff): [-0.010997, 0.003094]
- Log Loss p-value (two-sided): 0.488000
- Brier paired diff mean: -0.000315
- Brier 95% CI (paired diff): [-0.002612, 0.000604]
- Brier p-value (two-sided): 0.488000

## Multiplicity — Holm (2 pre-specified metrics, family alpha 0.05)
- Log Loss: p=0.488000, Holm alpha=0.0250, pass=False
- Brier: p=0.488000, Holm alpha=0.0500, pass=False

## Forecast gate assessment (all required for FORECAST_GATE_PASSED)
- >=5 instruments in paired OOS panel: PASS (5)
- >=3 non-overlapping 30-day test blocks: NOT_MET (2)
- >=2% relative Log Loss reduction vs B1: NOT_MET (1.6781%)
- Log Loss 95% CI excludes null in favorable direction: NOT_MET (CI [-0.010997, 0.003094])
- Holm multiplicity passes (2 metrics): NOT_MET
- Forecast gate (ALL criteria): NOT_MET

## Verdict
RESULT: FORECAST_GATE_NOT_MET — unmet criteria: test_blocks_ge3, ll_materiality_ge2pct, ll_ci_excludes_null_favorable, holm_pass.
No risk overlay is eligible. Preserve null result; do not threshold-shop or reuse holdout.

## Data & provenance
- Source: local research_state/data_cache (Binance UM perp archival mark/index/premium klines 1h, fundingRate 8h); adjacent sha256 sidecars; provenance_verified=true, unmapped_count==0
- No network / no paid / no manual / no credentialed data used in this run.
- Track B = modeled breach proxy only; never conflated with Track A observed liquidations.
