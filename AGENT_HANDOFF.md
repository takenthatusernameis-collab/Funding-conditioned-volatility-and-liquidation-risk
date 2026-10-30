# AGENT HANDOFF — Funding-Conditioned Volatility and Liquidation Risk

UPDATED: 2026-10-30T10:20:00Z
HEAD: 5655c6ca (main) — working tree has uncommitted manifest edit (do NOT commit unless explicitly asked)
REPO: Funding-conditioned-volatility-and-liquidation-risk

## INITIAL TASK MESSAGE (TIMESTAMPED) — MANDATORY FOR NEXT AGENTIC WORK SESSION

**PRIORITY (repo name): FUNDING-CONDITIONED VOLATILITY + LIQUIDATION RISK.**

### Confirmatory verdict (decisive, FCLR-003)
FCLR-003 — the adequately-powered confirmatory test (frozen splits; test 2024-10-02..2024-12-31 = 91 days = 3 non-overlapping 30-day blocks PASS; 5 instruments BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT; n=10,796 paired rows; block bootstrap 2000 reps) — is COMPLETE and NEGATIVE:
- C2 (funding + price-dislocation/smoothing) vs B1 (RV-only HAR): mean diff +0.015205 QLIKE, relative change -3.78% (worse), 95% CI [-0.020240, 0.056734] crosses zero -> PRIMARY CONTRAST C2 vs B1 FAILS.
- C1 (funding only) vs B1: +8.09% relative (secondary contrast), but C2 vs C1 = +0.0477 QLIKE (adding price features to C1 HURTS).
- Forecast gate: NOT_MET. Risk-overlay phase: INELIGIBLE.
- H001 (funding extremes + price-dislocation/smoothing improve OOS volatility forecasts over RV-only baseline): NOT_SUPPORTED on current data.
Artifact: research_state/evaluation_summary_FCLR003.md. Split registered (frozen before outcomes, matches executed run): research_state/run_manifest.json key split_boundaries_fclr003.

### Data exhaustion (structural bottleneck — no fresh confirmatory window)
No unsealed, contiguous >=5-symbol confirmatory window remains:
- 2024-04..12 (all 5 symbols) fully committed to sealed FCLR-002 / FCLR-003.
- 2025: mark price only for BTCUSDT, ETHUSDT (2 symbols); BNBUSDT/SOLUSDT/XRPUSDT absent.
- 2026: partial (BTCUSDT Jan-Aug; ETHUSDT Jan + Apr-Aug; BNBUSDT/SOLUSDT/XRPUSDT Apr-Aug only).
=> No fresh >=5-instrument, >=3-block window exists for a new confirmatory experiment (FCLR-004+) without a NEW admissible data source (RESEARCH_PROMPT.md §16). None currently available.

### Track A (observed liquidations)
STRUCTURALLY BLOCKED, exhausted (Binance liquidationSnapshot HTTP 404; fapi forceOrders HTTP 451 restricted location; no Bybit/OKX/Deribit unauthenticated census; FCLR-005 2026 pilot complete = exploratory only; FCLR-H004 BLOCKED for 2024).

### Track B (hypothetical boundary breach)
FCLR-H003 INCONCLUSIVE on both panels, no incremental skill (research_state/evaluation_summary_h003.md / _FCLR002.md). Extensions (72h/168h horizons, lower MMR tiers, event-intensity target) require fresh pre-registration AND fresh data (none available for >=5 symbols) — do NOT run on sealed holdouts.

## NEXT FOCUS CAMPAIGN: FCLR-CLOSEOUT-001 (verify & close the confirmatory program)

Because the confirmatory gate is negative and no fresh >=5-symbol data exists, do NOT launch further model/hyperparameter searches on sealed holdouts (prohibited: threshold shopping / holdout reuse / exploratory rescue of a failed confirmatory test, RESEARCH_PROMPT.md §16-17). Execute instead:

1. **Verify independent recomputation (in progress):** `FCLR_EXPERIMENT=FCLR-003 python scripts/run_evaluation.py` — confirm it reproduces research_state/evaluation_summary_FCLR003.md (QLIKE B0=0.487674 / B1=0.401884 / C1=0.369366 / C2=0.417089; C2_vs_B1 diff +0.015205, 95% CI [-0.020240, 0.056734], rel -3.78%). May take several minutes; check research_state/evaluation_summary_FCLR003.md mtime.
2. **Finalize registry verdict:** research_state/hypothesis_registry.json FCLR-H001 status -> NOT_SUPPORTED (evidence: FCLR-003); research_state/experiment_frontier.json current_status -> CONFIRMATORY_COMPLETE (negative); mark frontier tasks FCLR-002 / FCLR-003 complete.
3. **Write definitive conclusion:** record final negative-result verdict (research_state/final_confirmatory_verdict.md or append to final_inconclusive_report.md) citing FCLR-003, H001 NOT_SUPPORTED, data exhaustion, Track A blocked, overlay ineligible.
4. **Regression check:** `python -m unittest discover -s tests -v` (14 tests must pass).

## BOTTLENECKS REMOVED / NOTED
- split_boundaries_fclr003 registered in run_manifest.json (frozen, matches executed FCLR-003 splits) — unblocks reproducible FCLR-003 recomputation.
- Verified research_state/data_cache holds contiguous mark price for all 5 symbols 2024-04..12 (Oct/Nov/Dec = 31/30/31 daily CSVs each symbol); no fresh >=5-symbol window beyond 2024-12.
- Stale background process: an FCLR-002 recomputation (started ~09:48) spinning ~30+ min at 100% CPU with no output written — FCLR-002 result already on record (independently reproduced per hypothesis_registry). Do NOT launch redundant slow recomputations; results already on record.
- Do NOT: re-run sealed holdouts for tuning/selection; change .github/workflows; build a risk/risk-reduction overlay; fabricate observed-liquidation labels; threshold-shop to rescue H001.

## VERIFICATION COMMANDS
```bash
python -m unittest discover -s tests -v
# FCLR-003 independent recomputation verification (may take several minutes):
FCLR_EXPERIMENT=FCLR-003 python scripts/run_evaluation.py
```

## CURRENT STATE (GROUND TRUTH)
- FCLR-001: sealed, gate NOT_MET (single-instrument BTCUSDT coverage defect; single ~4-day block). PILOT/INCONCLUSIVE.
- FCLR-002: sealed, gate NOT_MET (70 days = 2 blocks < 3); C2 vs B1 numerically +9.28% rel QLIKE, CI excludes zero, but underpowered -> NOT claim-worthy.
- FCLR-003: sealed & COMPLETE, gate NOT_MET (powered: 3 blocks, 5 instruments, n=10796); C2 vs B1 -3.78%, CI crosses zero -> confirmatory NEGATIVE.
- FCLR-H001: NOT_SUPPORTED. FCLR-H002: PARTIAL (SSRN 403 blocks full methodology). FCLR-H003: INCONCLUSIVE. FCLR-H004: BLOCKED (2024) / EXPLORATORY_ONLY (2026 FCLR-005).
- All 14 tests pass. Risk overlay INELIGIBLE.

## WHAT THE EVIDENCE SUPPORTED / CONTRADICTED / LEFT UNKNOWN
- Supported: RV-only persistence (B1) is a strong baseline; funding-only (C1) adds modest in-window skill in FCLR-002/FCLR-003 but price-dislocation features (C2) do not improve over B1 when adequately powered.
- Contradicted: H001 claim that funding+price jointly improve OOS 24h volatility forecasts over RV-only (FCLR-003 negative).
- Unknown: whether any out-of-sample edge exists on data beyond 2024-12-31 (no unsealed >=5-symbol window); Track A observed liquidation predictability (no admissible census).
