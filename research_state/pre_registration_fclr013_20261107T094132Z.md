# PRE-REGISTRATION: FCLR-013 - Funding-conditioned volatility (2026 Q3 panel), confirmatory reopen
Experiment ID: FCLR-013
Hypothesis ID: FCLR-H001 (extension)
Protocol version: 1.0
Frozen before outcomes: true
Frozen at (UTC): 2026-11-07T09:41:32Z
Git SHA (frozen): af8c2eb2
Status: PROTOCOL_FROZEN (confirmatory)

## Hypothesis
Do funding extremes, realized volatility, and pre-specified price dislocation/smoothing features improve out-of-sample forecasts of next-24h realized variance of mark-price returns over RV-only baseline (B1)?

## Universe (cached, unauthenticated)
- Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT (5)
- Window: 2026-07-01T00:00:00Z .. 2026-09-30T23:00:00Z (92 days)
- Coverage audit: research_state/fclr013_coverage_audit_20261107T0936Z.json (coverage_only=true, outcomes_inspected=false, network_in_audit=false). markPriceKlines/indexPriceKlines/premiumIndexKlines/klines/funding present; 0 day-gaps reported.

## Splits (chronological, no reuse of inspected holdouts)
- Train: 2026-07-01T00:00:00Z .. 2026-08-05T23:00:00Z (36 days)
- Validation: 2026-08-06T00:00:00Z .. 2026-08-25T23:00:00Z (20 days)
- Test (sealed): 2026-08-26T00:00:00Z .. 2026-09-30T23:00:00Z (36 days)
- Purge/embargo at boundaries: >= 7 days (max horizon 24h; 7d margin)
- Split boundaries hashed/frozen before outcomes.

## Primary target
Next-24h realized variance of mark-price log returns (sum of squared log returns t+1..t+24), hourly mark prices. Units: variance (squared log returns). Epsilon 1e-12 for log(RV+eps).

## Predictors (causal, t only)
- RV1h, RV24h, RV168h (trailing realized variances from mark-price log returns)
- Signed funding (latest funding observation with availability <= t)
- Funding extremeness: percentile rank of |funding| vs trailing 90d for contract (>=30 obs required)
- Premium: mark/index minus 1 (contemporaneous alignment under frozen tolerance)
- Smoothing/dislocation: mark/EMA24 minus 1 (EMA from prior/current closed bars only)

## Models (fixed form)
- B0: persistence (preceding RV24h) - descriptive
- B1 (vol baseline): log-linear HAR on log RV1h,log RV24h,log RV168h
- C1: B1 + signed funding + |funding| 90d percentile
- C2 (candidate): C1 + mark/index premium + mark/EMA24

## Evaluation
- Primary contrast: C2 vs B1, 24h OOS QLIKE (lower better). Paired origins/rows.
- Train-only normalization (means/stds) and smearing correction for back-transform.
- Missing != 0; missing features dropped from comparison or handled by common panel.
- Block bootstrap (24h blocks) across symbols, >=2000 reps, deterministic seed.
- Multiplicity: Holm across pre-registered family (B0/C1/C2 vs B1, primary+secondaries).
- Materiality: >=2% relative QLIKE reduction required; CI must support improvement.
- Claim-worthiness: >=5 instruments in paired panel, >=3 non-overlapping 30d test blocks (or equivalent coverage).

## Gates (forecast)
NOT_MET if any fail: CI crosses 0 OR relative reduction < 2% OR multiplicity fails OR insufficient coverage/blocks OR unresolved leakage/label issues.

## Guardrails
- No look-ahead, no train-only violation, purge/embargo enforced.
- No tuning on sealed test; protocol frozen before outcomes.
- Track separation: modeled breaches != observed liquidations.
- No overlays/threshold shopping; preserve negatives.
- No credentials/paid/manual/API keys/auth bypass; network disabled in claim runs if cached.
- Reproducible: manifests/hashes/audits required.

## Data provenance
Source: Binance public data archive (data.binance.vision), unauthenticated. Cached under research_state/data_cache (existing layout). License/terms as in registry; acceptance pending full schema check in run if needed but coverage audit shows required series present.

## Expected artifacts
research_state/run_manifest_fclr013_*.json, research_state/evaluation_summary_FCLR013*.md, research_state/leakage_audit.md (update), research_state/negative_results_report.md (update if inconclusive/negative), research_state/result_ledger entries.
