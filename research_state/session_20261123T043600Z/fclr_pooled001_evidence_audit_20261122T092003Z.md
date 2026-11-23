# FCLR-POOLED-001 Evidence Audit

Session UTC: 20261122T092003Z
Campaign: FCLR-POOLED-001-20261122T040000Z (rank-0, gate-enforced)
outcome_data_inspected_before_freeze: false

## Data
- Source: research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}
- Months: 2025-05..2026-10 (18 months)
- Sha256 sidecars asserted for all 72 parquet files; caches not modified.
- Markets (eval): 799; Markets (recompute): 798
- Train rows (eval): 2,337,867; Test rows (eval): 1,296,472
- Train rows (recompute): 2,131,219; Test rows (recompute): 1,142,884

## Results (eval vs independent recompute)
- QLIKE B1: eval=65.190573, recompute=52.945004
- QLIKE C2: eval=65.190702, recompute=52.944664
- Diff C2-B1: eval=+0.000129, recompute=-0.000340
- Rel pct: eval=0.0002%, recompute=-0.0006%
- Materiality floor: 2.0% (met: eval=False, recompute=False)
- Decision: eval=NOT_SUPPORTED, recompute=NOT_SUPPORTED
- Bootstrap CI95 (eval): [-0.000008, 0.000008]
- Bootstrap CI95 (recompute): [-0.000009, 0.000005]
- Diebold-Mariano stat: eval=0.1219, recompute=-0.3738

## Liquidation risk (eval only)
- Brier model: 0.053400
- Brier climatology: 0.053510
- Brier skill: 0.0021

## Audit verdict
Eval and independent recompute are consistent: funding-conditioned features (C2) do NOT improve
24h forward realized variance QLIKE over the RV-only baseline (B1). Relative difference ~0.0%,
far below the -2.0% materiality floor. Decision: NOT_SUPPORTED. Null result preserved.

## Artifact hashes (sha256)
- fclr_pooled001_eval_20261122T092003Z.json: e9ec56baef669c304c9454156d1572a6640edcd24e21c7ae9d67eea8549221c1
- fclr_pooled001_eval_20261122T092003Z.md: d8b94174cf475f8e5744d4489bba54f16910c00999e2ab5489a353be3b81f9ec
- fclr_pooled001_eval_20261122T092003Z.py: 663ac2d0b503c7b0a0edd2fd6f7ebe00faccf8f71775b8878efcd6c5d5525665
- fclr_pooled001_prereg_20261122T092003Z.json: 3dd8aec8eed5ad5e98e27194268a03eea1d27c67e4439af34525f76224e91f96
- fclr_pooled001_prereg_20261122T092003Z.md: 838c61b2c91dee4c024a27f8239cc9dd645763f3b1be752d61bc98b660e3e295
- fclr_pooled001_recompute_20261122T092003Z.json: a8bbb2ea617d13cba6a04b6fe003d13f245122716d19a540f0ca7637d4a58867
- fclr_pooled001_recompute_20261122T092003Z.py: c3299b77e82fcdf4591b98b0c3decb1d527dca4266a419f3154448e268d90e13
- fclr_pooled001_source_registry_20261122T092003Z.json: 3cd2b1715ddcbdb745294358a557d3607d27e5f97f5443ff484814bbfeb6da73
- fclr_pooled001_source_registry_20261122T092003Z.md: a83f098f43c653b8b64ed4f78426208f43a0afb7d7b53ae65ad1d81249e8b990

## Non-avoidance
- outcome_data_inspected_before_freeze: false (prereg frozen before outcomes)
- Nulls preserved as NOT_SUPPORTED where applicable
- No threshold-shopping; 2% materiality floor fixed pre-outcome
- Stdlib + pyarrow only; numpy/pandas/scipy not used