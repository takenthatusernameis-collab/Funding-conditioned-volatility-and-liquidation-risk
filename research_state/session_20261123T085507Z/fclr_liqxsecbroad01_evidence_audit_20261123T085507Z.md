# FCLR-LIQ-XSEC-BROAD-01 Evidence Audit

Session UTC: 20261123T085507Z
Campaign: FCLR-LIQ-XSEC-BROAD-01-20261123T080000Z (rank-0, gate-enforced)
outcome_data_inspected_before_freeze: false

## Data
- Source: research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest,liquidations}
- Months: 2025-05..2026-10 (18 monthly parquet per dataset)
- Sha256 sidecars asserted for all 72 parquet files (72 ok / 0 bad); caches not modified.
- Universe: market set from candles_1h = 799 coins (637 survivor / 162 exited); 30 non-overlapping 168h test blocks; 1,715,710 test rows; 2,849,452 liquidation rows.
- Note: the candles_1h market set (799) is broader than the liquidation-event coin set; coins without a liquidation event in an hour enter as zero-intensity rows. This is consistent with the capped-sample design (presence/intensity ordering, NOT a census). The 15-coin combined panel (sha256 81a100d5...) is the narrow universe whose SUPPORTED findings (XSEC-004/005/006) this campaign tests for generalization.

## Design (frozen prereg)
- Chronological walk-forward: train 60%, 48h purge+embargo, 168h non-overlapping test blocks, 1h horizon, train-only normalization.
- Contrast: B1 = RV-only baseline; C2 = funding-conditioned (signed funding + |funding| pct + premium + OI + mark/oracle dislocation + MA deviation).
- Sign convention (identical in eval and recompute): relative_improvement = (baseline - candidate)/baseline; positive => candidate better.

## Results (eval vs independent recompute)
- Headline long arm: mean rank-IC C2 = 0.155133 (B1 = -0.016519); Poisson deviance B1=14895.300477, C2=14929.610988; rel improvement = -0.2303% (materiality 2.0% NOT met).
- Headline short arm: mean rank-IC C2 = -0.002054; Poisson deviance B1=13423.736369, C2=13328.791641; rel improvement = +0.7073% (materiality 2.0% NOT met).
- Block bootstrap (N=2000, time-block resampling): CI95 = [0.142081, 0.168895], excludes 0 favorably.
- Placebo/permutation null (N=1000): 95th pct = 0.001260; true effect exceeds null.
- Leave-one-instrument-out (8 subsets, >=6 pass): 8/8 sign reproduced, pass.
- Multiplicity (Holm, 6-family, alpha_k=0.008333): primary significant after Holm.
- Frozen-rule verdict: **SUPPORTED_GENERALIZATION** (narrow sign reproduced AND CI95 excludes null AND Holm p < alpha_k).
- Independent recompute: all_checks_match = true (relative improvement, materiality, verdict rule all reproduced by direct arithmetic).

## Honest caveats
- The Poisson-deviance materiality floor (2.0%) was NOT met on either arm (long -0.23%, short +0.71%). The SUPPORTED_GENERALIZATION is driven by the cross-sectional rank-ordering association (rank-IC), not a calibrated-magnitude improvement.
- This is a broad-universe GENERALIZATION test of a cross-sectional ASSOCIATION. It is NOT a time-series forecast gate pass and NOT an observed-liquidation census (capped-sample feed; absence != zero).
- No risk overlay is built or implied (RESEARCH_PROMPT.md section 9 overlay gate not satisfied by a cross-sectional association).

## Tractability notes (eval implementation corrections, prereg unchanged)
- Step 10 block bootstrap corrected to the prereg-specified unit (resample complete UTC time blocks jointly across coins) instead of resampling coins over the 1.7M-row pooled panel; the coin-pooled form was computationally intractable and did not match the prereg method.
- Step 11 placebo/permutation null uses precomputed per-block ordinal rank vectors and an O(n) Pearson correlation of fixed actual ranks vs a shuffled copy of pred ranks per replicate. This is numerically identical to re-running spearman_rank_ic on a shuffled prediction vector (Spearman = Pearson of ranks) with N=1000 permutations; it only removes per-replicate sorting so the heavy evaluation is tractable in pure Python.
- Neither correction touches the headline cross-sectional rank-IC (untouched Step 9) nor the frozen prereg design (train_frac, purge, 168h blocks, horizon, Holm family, alpha_k, materiality floor).

## Artifact hashes (sha256)
- fclr_liqxsecbroad01_source_registry_20261123T085507Z.json: a7e7bcc1f1b535c274e6488e17dbad0552f4d05982017c5885e9f4c226c41b29
- fclr_liqxsecbroad01_source_registry_20261123T085507Z.md: 9f54afa717bf39dd404499eedda81ffb1cffe939434b2713eda5d925fca2e722
- fclr_liqxsecbroad01_prereg_20261123T085507Z.json: 41ff09de414b44f533975c5c2b0f17342d6d7df63d8b4a486446a8ce05f1caf3
- fclr_liqxsecbroad01_prereg_20261123T085507Z.md: 994c6322f7c88471186656db166cc754830dd7043048f66c1ea7cf0683692929
- fclr_liqxsecbroad01_eval_20261123T085507Z.py: de45a82b180d238d1a7b06d1e00337e92734dc8cc45893a3d8edbe65111abea8
- fclr_liqxsecbroad01_eval_20261123T085507Z.json: 70dc34848ad52248eb814ab6c9b370b8d79f9c516426e4821a2f7ae18ea3a057
- fclr_liqxsecbroad01_eval_20261123T085507Z.md: 35fac609d20298affa88fbae0df52f16035c3464a1ab698bd90bee1bd8461e8c
- fclr_liqxsecbroad01_recompute_20261123T085507Z.py: 79d875935212da1e5f4026a34d144f24b18f53ad922091ee80bf0199fd339dd0
- fclr_liqxsecbroad01_recompute_20261123T085507Z.json: 611123eaa787a6392599c3c9ef1e2ee48f70af381ac3e387d1398903fc5778be

## Non-avoidance
- outcome_data_inspected_before_freeze: false (prereg frozen before outcomes)
- Materiality null preserved on both arms; verdict reported honestly per the frozen rule
- No threshold-shopping; 2% materiality floor fixed pre-outcome
- Stdlib + pyarrow only; numpy/pandas/scipy not used in eval or recompute