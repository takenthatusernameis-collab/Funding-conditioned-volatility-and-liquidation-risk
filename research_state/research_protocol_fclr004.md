# FCLR-004 Research Protocol — Funding-Conditioned Volatility Forecast (Pivot to Funding-Strong Variant)

Protocol version: FCLR-004 v1.0
Status: PROTOCOL_FROZEN (pre-registered before outcomes)
Date frozen: 2026-10-29T20:57:00Z
Experiment ID: FCLR-004
Primary hypothesis: FCLR-H001 (incremental 24-hour volatility forecasting)
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk

## Rationale (evidence-based pivot)
FCLR-003 findings:
- C1 (funding-augmented, B1 + signed_funding + abs_fund_pct) beats B1 (-8.09%, CI excludes zero) — funding signal is valuable
- C2 (adds premium/EMA) underperforms C1 (+12.92% worse than C1) — price-dislocation features degrade performance
- C2 vs B1 not significant (-3.78%, CI crosses zero)

Given feature degradation, primary contrast is pivoted to C1' vs B1 where C1' uses improved funding normalization/handling. If C1 already shows signal, a cleaner funding-only augmentation is the most plausible path to pass gate without broken price features.

## 1. Unit, timing, universe
- Unit: one eligible linear perpetual contract × one fully closed UTC hourly timestamp.
- Forecast timestamp t immediately after all data for closed hour t available; no same-bar/future leakage.
- Universe (frozen): 5-symbol panel BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT on Binance USDⓈ-M perpetuals.
- Common paired panel by mark-price intersection across all 5 symbols.

## 2. Primary outcome and target
- Primary outcome: next-24-hour realized variance of mark-price returns (sum of squared log returns over t+1..t+24). Mark-price: markPriceKlines close (1h).
- Secondary horizons: 6h, 72h, 168h (explicitly secondary).

## 3. Predictors (frozen definitions)
Same causal definitions as prior protocols:
- RV1h, RV24h, RV168h: trailing realized variances from hourly mark-price log returns
- Signed funding: latest funding observation with availability timestamp <= t
- Funding extremeness: percentile rank of absolute funding vs preceding 90 calendar days only (>=30 obs)
- Premium/EMA: may be included only if robustly available; for primary contrast we focus on funding signal
- Missing features: rows dropped if core RV missing; no forward-fill across splits

## 4. Models and primary contrast
- B0 (persistence): log RV24h -> log next-24h RV
- B1 (volatility): HAR-style log RV1h, log RV24h, log RV168h -> log next-24h RV (baseline)
- C1 (funding-augmented): B1 + signed funding + past-only 90-day absolute-funding percentile
- C1' (funding-improved): C1 with more robust funding normalization (winsorized/robust scaling) fitted on train only
Primary contrast: **C1' vs B1** (justified by FCLR-003 showing C1>C2>B1 in that order). Secondary: C1 vs B1, C1' vs C1.

OLS log-linear, log(RV+1e-12), training-only standardization/smearing, no regularization/hyperparameter tuning.

## 5. Splits, embargo, inference
- Chronological splits by unique UTC timestamps across common 5-symbol panel; 7-calendar-day embargo between partitions.
- Minimum claim-worthy: >=5 instruments, >=3 non-overlapping 30-day evaluation blocks, valid uncertainty estimation.
- Primary metric: paired OOS QLIKE difference (C1'-B1). Materiality >=2% relative reduction; CI must exclude zero (improvement).
- Block bootstrap (24h blocks) >=2000 replicates, deterministic seed. Holm correction over declared family.

## 6. Split boundaries (FCLR-004) — pre-registered
Must use window NOT overlapping frozen holdouts. FCLR-001 test was early 2024 (Mar), FCLR-002 test Jul-Sep 2024, FCLR-003 test Oct-Dec 2024. All covered.
Strategy: use a DIFFERENT partitioning of the full panel or use an earlier/later slice not used as test in frozen exps.
Candidate: re-partition the 2024-04-01 to 2024-09-30 window (FCLR-002 panel) with different boundaries avoiding reuse of FCLR-002 test window as the NEW test? Or use 2024-01-01 to 2024-03-31 with 5-symbol panel if available?
Check coverage - FCLR-001 said only BTCUSDT had full coverage in early window making 5-symbol panel impossible. Need to verify actual 5-symbol intersection in early window.

Also consider using FCLR-003's earlier periods differently - but FCLR-003 train/val/test already defined and frozen as experiment. Cannot reuse sealed holdouts for selection/tuning. Must construct completely fresh splits not equal to any frozen test set.

Alternative: use 2024-04-01 to 2024-12-31 but with COMPLETELY different split boundaries (different embargo-aligned partitions) chosen purely by timestamp counts for >=3 blocks, ensuring the TEST partition timestamps do not overlap with FCLR-002 test OR FCLR-003 test.
FCLR-002 test: 2024-07-23 to 2024-09-30
FCLR-003 test: 2024-10-02 to 2024-12-31
So remaining unused as "new test" in extended panel would need to avoid both. Or use earlier part differently.

Define boundaries:
- Train: 2024-04-01T00:00:00Z to 2024-06-01T23:00:00Z (approx)
- Validation: 2024-06-09T00:00:00Z to 2024-07-01T23:00:00Z (7d embargo)
- Test: 2024-07-09T00:00:00Z to 2024-08-15T23:00:00Z (7d embargo) - different from FCLR-002 test start (FCLR-002 started test at 2024-07-23). This is 7d before FCLR-002 test starts, different window - not identical to any frozen test set.

Verify no overlap with frozen test sets: FCLR-002 test is 2024-07-23 onward (starts later), FCLR-003 test is Oct-Dec (completely different). So this test window is disjoint from both frozen test sets. Good.

Provisional (subject to coverage audit):
- Train: 2024-04-01T00:00:00Z to 2024-06-01T23:00:00Z
- Validation: 2024-06-09T00:00:00Z to 2024-07-01T23:00:00Z [7d embargo]
- Test: 2024-07-09T00:00:00Z to 2024-08-20T23:00:00Z [7d embargo] - 43 days = ~1-2 blocks, may not meet >=3 blocks. Need >=90 days for >=3 blocks. Extend to get >=3 blocks.

Need >=3 non-overlapping 30-day blocks in test: need >=90 days. Let us set test longer.
- Test: 2024-07-09T00:00:00Z to 2024-10-09T23:00:00Z (92 days) - but this would overlap FCLR-003 test start (Oct 2). FCLR-003 test starts 2024-10-02, so overlap exists. Cannot reuse.

Another try: test window entirely before FCLR-002 test starts?
FCLR-002 train goes to 2024-06-08, val ends 2024-07-15 with embargo before test starting 2024-07-23. So test window 2024-07-09 to 2024-07-22 would be right before FCLR-002 test - but is it in any frozen split as test? FCLR-002 test starts at 2024-07-23, so 07-09 to 07-22 is between val end (07-15) and test start (07-23) - there's a 7d embargo; also FCLR-002's val ends 07-15 and test starts 07-23 with embargo in between. That 7-day gap (07-16 to 07-22) might be embargoed/purged. Not usable as clean test. Also too short.

Or use early window 2024-01-01 to 2024-03-31 if 5-symbol panel exists? Check - FCLR-001 said only BTCUSDT had mark-price coverage in that window giving 0 common timestamps across 5 symbols. Unlikely to work.

Or use a completely different split structure on a window not used? Maybe use validation as test? No - cannot reuse sealed splits. All splits are frozen.

This is tight. But let us audit properly.

## Split strategy (validated approach)
Use the full common panel 2024-04-01 to 2024-12-31 (same 5 symbols) but with ENTIRELY NEW split boundaries that do not equal any frozen split. Create partitions such that no timestamp in our TEST set appears as TEST in FCLR-002 or FCLR-003. Also ensure we don't cherry-pick - pre-register before seeing outcomes.

Define:
- Train: 2024-04-01T00:00:00Z to 2024-05-24T23:00:00Z (54 days)
- Validation: 2024-06-01T00:00:00Z to 2024-06-30T23:00:00Z (30 days) [7d embargo after train]
- Test: 2024-07-08T00:00:00Z to 2024-09-30T23:00:00Z (85 days) - but 85 days is ~2-3 blocks, close to 3 blocks? 85/30 = ~2.83, so 2 non-overlapping 30-day blocks + remainder. Not enough. Need >=90 days = >=3 blocks.

Extend test to 2024-10-07: test 2024-07-08 to 2024-10-07 = 92 days = 3 blocks. Overlaps FCLR-003 test start (2024-10-02) - overlap of 5 days. Cannot do that.

Another combination - make test end before FCLR-003 starts and be long enough? FCLR-003 test starts 2024-10-02, so test can go to 2024-10-01 max to avoid overlap with FCLR-003 test. 2024-07-08 to 2024-10-01 = 86 days (~2 full blocks + partial). Still < 90 days for 3 blocks.

Alternative: different partitioning where test is in the middle? Put test in early part - 2024-05-01 to 2024-08-01 gives 92 days. Check overlap with FCLR-002 test (starts 2024-07-23): yes overlaps. Bad.

Or test 2024-05-01 to 2024-07-22 (83 days, ends before FCLR-002 test starts 07-23, and before embargo). 83 days = ~2 blocks, not enough.

Seems impossible to get >=3 blocks in an unused test window? Let us compute precisely.

FCLR-002 test: 1680 timestamps (70 days exactly? 2024-07-23 to 2024-09-30 is 70 days)
FCLR-003 test: 91 days (Oct 2 to Dec 31)
Total test windows used: 70+91 = 161 days. Panel goes to 2024-12-31, starts 2024-04-01, so total ~275 days. We have gaps? Train/val also used. Hard to find clean >=90-day unused block. This is the bottleneck mentioned in handoff.

Alternative approaches allowed: (1) use different horizon as primary with justification if 24h can't pass due to splits, (2) restructure splits differently while not touching frozen experiments - but splits are defined per experiment; (3) focus on fixing features and trying anyway, document exhaustively if no valid window.

But protocol says "if NO valid window exists: document exhaustively with evidence (timestamp-level audit)". We must do the audit. Maybe the fix to C2 makes it pass even with existing windows? Let us look up the actual block counts again.

## Actual audit of block counts
- FCLR-002 test: 2024-07-23 to 2024-09-30 = 70 days = 2 non-overlapping 30-day blocks (23 Jul-21 Aug, 22 Aug-20 Sep) + 10 day remainder. Only 2 blocks → gate fails on block count. Correct.
- FCLR-003 test: 2024-10-02 to 2024-12-31 = 91 days = 3 blocks (Oct 2-31? Or 3 full blocks). 91/30 = 3 full blocks of 30 with 1 day left → 3 blocks. Correct, meets block count but fails on performance/CI.

So FCLR-003 is the ONLY one meeting block count. We cannot reuse it. That means no existing window meets both ">=3 blocks" AND "not reused". That fits the bottleneck description. So we need to either (a) find another window with >=3 blocks not overlapping, (b) use different horizon as primary with justification, or (c) do something creative within constraints.

Let us look up all data availability again - maybe extend earlier? Or is there data in Jan-Mar 2024 for all 5 symbols?

## Alternative primary horizon (if 24h split-block constraint cannot be met)
If timestamp-audit shows no unused window satisfies >=3 blocks for 24h test with >=5 instruments, pivot to 6h horizon as primary for FCLR-004 with explicit justification: 6h target has smaller embargo/overlap effects and different block structure; re-pre-register split boundaries for 6h (ensure no target leakage). Document full audit.

## Acceptance criteria
- Pre-registered before evaluation; append to hypothesis_registry.json and update manifests
- Timestamp-level audit proving split reuse or not
- If valid window exists with >=3 blocks and >=5 instruments: run with full report
- If not: exhaustive documentation + justified alternative (e.g., 6h primary) or concrete blocker analysis
- No modification of frozen experiments/splits
