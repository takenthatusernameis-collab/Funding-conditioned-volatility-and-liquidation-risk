# CAMPAIGN SWEEP (FCLR-NEXT-059) - 20261104T154000Z
Timestamp (UTC): 20261104T154000Z
Git SHA (HEAD): f128b157
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Priority: P0 - HEAVY WORK ENFORCED (REPO-NAME PRIORITIZED = TRACK C)

## State reconciliation (concrete evidence)
- AGENT_HANDOFF.md (20261104T153545Z): Track C gate PASSED (FCLR-011), deeper validation completed, Track C robustness required as next heavy focus. Track A on trigger only (no new >=2026-11). Caches cleaned, tests 164/164 green.
- research_state/run_manifest.json (current): FCLR-012-V INCONCLUSIVE/NOT_MET; FCLR-011 splits frozen (train 2026-01-01..2026-03-17, val 2026-03-25..2026-04-30, test 2026-05-08..2026-08-06), results show C2 vs B1 mean_diff -0.016458, CI [-0.032546,-0.001418], rel_reduction 4.94%, 5 instruments, 3 blocks. Gate PASS noted in handoff context.
- research_state/trackc_deeper_validation_20261104T153049Z.md: full ablations, bootstrap (block 24h, >=2000), interactions (I1_fund_x_rv, I2_fund_x_ema), funding-quartile stratification (monotonic Q1+3.84% -> Q4+11.40%), cross-symbol stability, Holm applied. All on frozen splits only.
- Tests: 164/164 passed (pytest 15.73s). __pycache__ cleaned (0 pyc, 0 dirs).
- Bottlenecks: no new schedulers/controllers/status-only files; sweep updated with evidence; mining cached Binance zips/data_cache as instructed.

## Contradictions / notes
- Handoff says "3 blocks (test 2026-05-08..2026-08-06)" while run_manifest shows test window spans to 2026-08-06; deeper validation reports test split as 10800 obs across 5 symbols (2160 each) over that window - consistent with frozen FCLR-011.
- Forward FCLR-012-V blocked on data (ends 2026-11-02, 0 non-overlapping 30d blocks) - remains blocked, do not probe for new downloads.
- Track A ironflow data through 2026-10 (last probe 304), no >=2026-11 files seen; remains trigger-only.

## Priority order (by repo name)
1. TRACK C (funding-conditioned volatility) - HIGHEST. Gate passed; do robustness/stability on frozen splits (leave-one-out, block sensitivity, lags/signs, winsor) as specified.
2. TRACK A (liquidation risk) - ON TRIGGER ONLY with preregistration before outcomes if >=2026-11 appears.
3. INFRA/BOTTLENECKS - only if enable 1 or 2, keep 164/164 green.

## Next heavy actions (this session)
- Step 2: Track C robustness on frozen FCLR-011/FCLR-002 splits only - leave-one-symbol out, leave-one-block out, funding sign/|funding| regime coefficients, funding lag (t-1/t-2), winsorization (1%/5%), block-bootstrap block sizes 12h/48h + stationary bootstrap (>=2000 reps, deterministic seeds). Write research_state/trackc_robustness_YYYYMMDDTHHMMSSZ.md with full tables, CIs, Holm.
- Step 3: Track A trigger probe (scripts/monitor_ironflow_liquidations.py --quick, scripts/deep_review_alt_sources.py). Record evidence; preregister if new >=2026-11 files.
- Step 4: Bottleneck elimination/checks, ensure green.

## Evidence file references
- AGENT_HANDOFF.md:5790 bytes
- research_state/run_manifest.json: present
- research_state/trackc_deeper_validation_20261104T153049Z.md: present
- tests/: 164 passed
