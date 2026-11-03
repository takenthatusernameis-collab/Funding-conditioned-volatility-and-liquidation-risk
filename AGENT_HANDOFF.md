# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T061422Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY:** FUNDING-CONDITIONED VOLATILITY FORECASTING (TRACK B) - MAXIMUM NOW | LIQUIDATION TRACK A - MONITOR-ONLY, NEVER IDLE-WAIT
**CAMPAIGN:** FUNDING_CONDITIONED_FCVR_HEAVY-007 - TRACK-B HEAVY, UNSEALED-PANEL CONFIRMATORY

## IMMEDIATE MANDATE (DO THIS FIRST - IN THIS EXACT ORDER)

The repo name is "Funding-conditioned-volatility-and-liquidation-risk". Track A (observed liquidations) is STRUCTURALLY BLOCKED: Ironflow forward months 2026-11,12,2027-01,02 return 404; consec_absent=3; last data 2026-10; all 8 alt-source families probed COMPLETE_NO-GO; no admissible unauthenticated liquidation source exists. FCLR-010 (Hyperliquid census, 2025-11..2026-10) gate PASSED and is sealed. DO NOT wait on Track A. Every minute goes to measurable Track B progress.

Track B is UNBLOCKED and has unsealed data verified present in research_state/data_cache/ (2026-01..2026-08, all 5 symbols BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT, markPriceKlines + indexPriceKlines + fundingRate). All prior confirmatory panels (FCLR-001/002/003/006/007/008) are exhausted/sealed. H001 INCONCLUSIVE on FCLR-008 (+4.30% rel QLIKE, CI crosses zero). Overlay INELIGIBLE. No untested Track B cell remains under current admissible data WITHOUT a fresh pre-registered experiment ID on NEW unsealed data.

The next session MUST run a fresh pre-registered Track B confirmatory experiment on the unsealed 2026 panel — frozen protocol BEFORE outcomes, train-only normalization, block bootstrap CIs, full ablations. This is heavy, non-optional work.

```bash
# PHASE 1: CONFIRM STATE (2 min)
python scripts/monitor_ironflow_liquidations.py --verify
python -m unittest discover -s tests -v | tail -5

# PHASE 2: TRACK B HEAVY - PRE-REGISTER + EXECUTE ON UNSEALED 2026 PANEL (90%+ of effort)
# Step A: coverage-only audit on unsealed 2026-01-01..2026-08-06 panel (>=5 symbols, >=3 non-overlapping 30-day blocks) - NO outcome inspection
ls research_state/data_cache/ | grep -E '2026_(04|05|06|07|08)' | head
# Step B: freeze protocol + splits BEFORE outcomes (research_protocol_fclr_next.md, frozen_before_outcomes=true)
# Step C: extend features per RESEARCH_PROMPT §7 (trailing-only funding percentiles/zscore, RV ratios 6h/24h/7d, mark/index premium, mark/EMA24 distance)
# Step D: train-only normalized OLS models B0/B1/C1/C2; block bootstrap CIs; full ablations C2 vs B1 on frozen test split
# Step E: write research_state/evaluation_summary_VOLATILITY_YYYYMMDDTHHMMSSZ.md + gate assessment
# Step F: update experiment_frontier.json + this AGENT_HANDOFF.md with successor task

# PHASE 3: TRACK A KEEP-ALIVE (<1 min, monitor only)
python scripts/monitor_ironflow_liquidations.py --quick
python scripts/hunt_alternative_liquidation_sources.py 2>&1 | tail -15
```

## VERIFIED TRUTH (20261103T061422Z)

- **Track A (liquidations):** BLOCKED_ON_DATA. Ironflow cached through 2026-10 intact. Forward months 404. consec_absent=3, baseline_drift=False, content_hash_complete=True, resume_trigger_met=false. Alt sources: 12 REVIEW_REQUIRED, 0 GO after deep review. No admissible unauthenticated source found. FCLR-010 COMPLETE, gate PASSED, sealed. MONITOR ONLY — never idle-wait.
- **Track B (funding-conditioned volatility):** UNBLOCKED_HEAVY_EXECUTION. fclr002_panel.json has 19488 rows (5 symbols, 2024-04-01..2024-09-30). Unsealed 2026-01..2026-08 panel verified present in data_cache/ (~122 days = 4 non-overlapping 30-day blocks, >=5 instruments) — NOT yet used for a confirmatory Track B experiment. Infrastructure: src/volatility/features.py, features_ext.py, eval.py, splits.py; scripts/forecast_pipeline.py. All confirmatory panels exhausted; H001 INCONCLUSIVE; overlay INELIGIBLE. Fresh pre-registered experiment on unsealed 2026 data required for any further confirmatory Track B cell.
- **Tests:** 111/111 PASS. Keep green.
- **Repo state:** Clean, tons of data, automation ready. No credentials needed.

## DUAL-TRACK WORKSTREAMS (RUN IN PARALLEL)

### STREAM B: FUNDING-CONDITIONED VOLATILITY FORECASTING (PRIORITY #1 - HEAVY, NON-OPTIONAL)
- [ ] **B1) Coverage-only audit on unsealed 2026 panel** - research_state/data_cache/ (2026-01..2026-08, 5 symbols). Confirm >=5 symbols, >=3 non-overlapping 30-day blocks, mark-price intersection. NO outcome/QLIKE inspection before pre-registration.
- [ ] **B2) Fresh pre-registered protocol** - research_state/research_protocol_fclr_next.md v1.0 frozen BEFORE outcomes (FCLR-001/002 design: B0 persistence, B1 RV-HAR, C1 funding-augmented, C2 combined; primary contrast C2 vs B1 on QLIKE; >=2% relative QLIKE floor; Holm multiplicity; block bootstrap >=2000 replicates). Frozen splits + eligible panel hashed before outcomes.
- [ ] **B3) Feature extension per RESEARCH_PROMPT §7** - trailing-only funding percentile/zscore (90-day, >=30 obs), signed funding separate, RV ratios 6h/24h/7d, mark/index premium, mark/EMA24 distance. All causal, trailing-only, no leakage. Extend src/volatility/features_ext.py as needed.
- [ ] **B4) Train-only normalized OLS + block bootstrap** - standardization from training info only; purge/embargo by horizon; chronological walk-forward only; no random splits. QLIKE/MAE/RMSE + block-bootstrap CIs.
- [ ] **B5) Full ablations on frozen test split** - B0 vs B1 vs C1 vs C2 vs B0; paired forecast origins; identical eligible rows; Holm across declared family.
- [ ] **B6) Document everything** - research_state/evaluation_summary_VOLATILITY_YYYYMMDDTHHMMSSZ.md with full metrics, CI, ablations, gaps. Update run_manifest/hypothesis_registry/experiment_frontier.

### STREAM A: LIQUIDATION ACQUISITION (KEEP ALIVE - MONITOR ONLY, NO IDLE)
- [ ] **A1) Ironflow hardening** - monitor_ironflow_liquidations.py --quick at session start; track probe diffs; detect 404->200 flips.
- [ ] **A2) Alt-source verification** - Re-probe REVIEW_REQUIRED only with new evidence; IPFS/Arweave/Zenodo/HF academic liquidation datasets. Document with full evidence.
- [ ] **A3) Blocker evidence fresh** - research_state/blocker_evidence_*.md with timestamps/commands.

### STREAM C: TESTS & INFRASTRUCTURE (PARALLEL)
- [ ] **C1) Add tests** - Unit tests for new volatility features/eval/splits. Keep all 111+ passing.
- [ ] **C2) Checkpointing/resume** - Everything idempotent; restartable from checkpoints.
- [ ] **C3) Update manifests** - run_manifest.json, hypothesis_registry.json, experiment_frontier.json current.

## BOTTLENECKS ELIMINATED NOW
1. **Track A idle-wait removed** - Track A is structurally blocked; session starts with <1 min monitor check, then 100% Track B. No polling loops without new evidence.
2. **Track B cell exhaustion addressed** - All prior confirmatory panels sealed/exhausted. Next heavy work = fresh pre-registered experiment on unsealed 2026 panel with new experiment ID. Do NOT re-run FCLR-001/002/003/006/007/008; do NOT threshold-shop; do NOT relax >=2% floor or CI criterion.
3. **Shallow evaluation removed** - Follow RESEARCH_PROMPT gates religiously: freeze protocol before holdout, train-only normalization, purge/embargo, block bootstrap, Holm multiplicity, correct comparisons.
4. **Missing feature coverage removed** - Implement ALL pre-registered §7 features before evaluation. No shortcuts, no zero-fill/forward-fill.

## RESUME TRIGGERS
- **Track A:** Ironflow returns 200 for >=2026-11 with liquidation events/fills matching FCLR-010 schema OR new unauthenticated source passes FULL rubric (>=5 symbols or equivalent, >=complete month/>=3 non-overlapping 30-day blocks, schema mappable, no keys/signed/requester-pays).
- **Track B:** Runs whenever unblocked — it IS unblocked now. No gate blocking it. Fresh pre-registered experiment on unsealed 2026 panel is the next heavy task.

## MANDATORY DELIVERABLES THIS SESSION
- [ ] Coverage-only audit of unsealed 2026 panel (no outcome inspection)
- [ ] Fresh pre-registered research_protocol_fclr_next.md frozen BEFORE outcomes
- [ ] Feature extensions + train-only normalized models + block bootstrap CIs + full ablations
- [ ] Concrete Track B evaluation run with numbers (QLIKE/MAE/RMSE, baselines+ablations, CIs)
- [ ] Fresh research_state/evaluation_summary_VOLATILITY_YYYYMMDDTHHMMSSZ.md + gate assessment
- [ ] Updated research_state/experiment_frontier.json reflecting Track B heavy + concrete next steps
- [ ] Updated this AGENT_HANDOFF.md with successor's exact next task
- [ ] All tests passing (111+)
- [ ] Track A monitoring updated with fresh evidence (<1 min)

## CRITICAL RULES
- **Research only. No trading/paper/live/API orders.**
- **No credentials. Unauthenticated only.**
- **No .github/workflows changes.**
- **Leakage-resistant: chronological splits, train-only normalization, purge/embargo, freeze before holdout.**
- **Separate tracks: modeled breaches != observed liquidations.**
- **Heavy work always. If Track A blocked, 3x effort on Track B.**
- **Evidence-based. Timestamp everything.**
- **Never re-run sealed/exhausted confirmatory panels. Fresh experiment ID required for any new confirmatory cell.**

## NEXT SESSION'S SINGLE HIGHEST-VALUE TASK
Execute B1-B6 on the unsealed 2026 panel: coverage audit → frozen pre-registration → feature extension → train-only normalized OLS + block bootstrap → full ablations → evaluation summary + gate assessment. Verify command: `python -m unittest discover -s tests -v` (must pass 111+) and fresh `research_state/evaluation_summary_VOLATILITY_*.md` present with C2 vs B1 QLIKE + 95% CI.