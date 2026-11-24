# FCLR-VOL-BROAD-01 Evidence Audit

experiment_id: FCLR-VOL-BROAD-01
campaign: FCLR-VOL-BROAD-01-20261124T035500Z
session_utc: 20261124T120000Z
session_id: session_20261124T120000Z
phase: EVIDENCE_AUDIT
source: fclr_volbroad01_evidence_audit

audit_pass: true
unresolved_blockers: []
outcome_data_inspected_before_freeze: false

Data source: research_state/data_cache/ironflow_bulk/{candles_1h,funding,open_interest}
Data months: 2025-05 .. 2026-10 (18 monthly parquet per dataset)
sha256 sidecars asserted: 54/54 ok, 0 bad

Universe:
- n_coins_candles_1h: 342; n_coins_funding_oi: 198
- n_analysis_ready_coins: 377; n_analysis_ready_rows: 2,411,886
- n_timestamps: 12,419; n_test_blocks_168h: 23; n_forecasts: 684,301
- broad 342+ coin universe; panel uses the intersection of coins with funding/OI coverage.

Design: walk_forward, train_frac=0.60, purge_embargo_h=48, block_h=168, horizon_h=[1,24],
train-only normalization, models: baseline_rv_only_fe / candidate_funding_conditioned_fe,
inference: DM HAC + cluster-robust CR1 by coin + Driscoll-Kraay HAC + Holm,
materiality_floor_rel_qlike: 0.02

Results (next-hour RV, primary target):
- QLIKE baseline: 7.3145; QLIKE candidate: 7.1729; diff: -0.1415
- Relative QLIKE improvement: +1.93%
- MSE baseline: 0.0450; MSE candidate: 0.0095
- Materiality met: false (1.93% < 2.0%)
- Verdict: NOT_SUPPORTED

Results recompute:
- all_checks_match: true; n_checks: 31
- materiality_met_recompute: false; verdict_recompute: NOT_SUPPORTED

Agreement: eval and independent recompute agree (all_checks_match=true).
Sign convention: (baseline - candidate) / baseline, positive = candidate better.

Honest caveats:
- The 2% relative QLIKE materiality floor was NOT met (1.93% relative improvement).
  Verdict NOT_SUPPORTED is a valid, publishable negative result that closes Half 1
  (funding-conditioned volatility) at broad scale for the first time.
- MSE values are near-zero due to small magnitude of squared log returns; QLIKE is primary.
- No risk overlay is built or implied (RESEARCH_PROMPT.md section 9 overlay gate not passed).
- No threshold shopping; no floor relaxation after outcomes; symmetric verdict rule.

Artifact hashes (sha256):
- fclr_volbroad01_source_registry_20261124T120000Z.json: 2a085fb9...
- fclr_volbroad01_source_registry_20261124T120000Z.md: 2753a3bc...
- fclr_volbroad01_prereg_20261124T120000Z.json: 86f11e48...
- fclr_volbroad01_prereg_20261124T120000Z.md: 0acb0955...
- fclr_volbroad01_eval_20261124T120000Z.py: efacbd4b...
- fclr_volbroad01_eval_20261124T120000Z.json: 7f7d48f0...
- fclr_volbroad01_eval_20261124T120000Z.md: 30a7951d...
- fclr_volbroad01_recompute_20261124T120000Z.py: 55998db5...
- fclr_volbroad01_recompute_20261124T120000Z.json: 800fff46...

sha256_asserted: true
no_threshold_shopping: true
software: stdlib + numpy + pandas + pyarrow only; no network; read-only caches

audit_verdict: CONSISTENT - eval and independent recompute agree (all_checks_match=true).
Broad-panel funding-conditioned RV forecast returns NOT_SUPPORTED: the candidate does
not clear the frozen 2% relative QLIKE materiality floor (1.93% < 2.0%). Null preserved
honestly.

generated_utc: 2026-11-24T12:00:00Z
