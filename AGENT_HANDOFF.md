# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T061200Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY:** FUNDING-CONDITIONED VOLATILITY FORECASTING (TRACK B) - MAXIMIZE NOW | LIQUIDATION TRACK A - KEEP ALIVE IN PARALLEL
**CAMPAIGN:** FUNDING_CONDITIONED_FCVR_HEAVY-006 - DUAL-TRACK RELENTLESS EXECUTION

## IMMEDIATE MANDATE (DO THIS FIRST)
The repo is "Funding-conditioned-volatility-and-liquidation-risk". Both halves matter - but Track A (observed liquidations) remains structurally blocked on Ironflow forward edge (2026-11,12,2027-01,02 return 404; consec_absent>=3; last data 2026-10). DO NOT wait idle. Run BOTH tracks concurrently with Track B receiving the bulk of compute/time until Track A unblocks.

## CRYSTAL-CLEAR INITIAL TASK (EXECUTE IN THIS EXACT ORDER)

```bash
# PHASE 1: CONFIRM STATE (2 min)
python scripts/monitor_ironflow_liquidations.py --verify
python -m unittest discover -s tests -v | tail -5

# PHASE 2: BUILD TRACK B TO PRODUCTION QUALITY (HEAVY - 90% of effort until unblocked)
# Audit existing pipeline, extend features per RESEARCH_PROMPT, run leakage-resistant eval
ls src/volatility/ src/features/ scripts/forecast_pipeline.py 2>&1 | head -20

# PHASE 3: KEEP TRACK A ALIVE (10% effort)
python scripts/monitor_ironflow_liquidations.py --quick
python scripts/hunt_alternative_liquidation_sources.py 2>&1 | tail -15
```

## VERIFIED TRUTH (20261103T061200Z)
- **Track A (liquidations):** Ironflow cached through 2026-10 intact (18 month pairs). Forward months 404. consec_absent=3, baseline_drift=False, content_hash_complete=True, resume_trigger_met=false. Alt sources: 12 REVIEW_REQUIRED, 0 GO after deep review. No admissible unauthenticated source found yet. MONITOR ONLY.
- **Track B (funding-conditioned volatility):** Massive unexploited data. Cached panels exist (fclr002_panel.json has 19488 rows). Klines/funding/mark/index/premium for BTC/ETH/SOL/XRP Jan-Mar 2024 + extensive cache 2024-2026 present. Infrastructure exists (src/volatility/, scripts/forecast_pipeline.py). MUST HARDEN TO MEET ALL RESEARCH_PROMPT GATES.
- **Tests:** 111/111 PASS. Keep green.
- **Repo state:** Clean, tons of data, automation ready. No credentials needed.

## DUAL-TRACK WORKSTREAMS (RUN IN PARALLEL)

### STREAM B: FUNDING-CONDITIONED VOLATILITY FORECASTING (PRIORITY #1 - HEAVY)
- [ ] **B1) Feature completeness audit** - Compare current features vs RESEARCH_PROMPT §7 (funding: signed/abs, trailing percentiles/standards, time-to-funding; RV: 6h/24h/7d, ratios; price-dislocation: premium/basis, mark-index, MA/EMA deviations). Fill ALL gaps. All trailing-only, no leakage.
- [ ] **B2) Build robust pipeline in src/** - Create/extend modules: `src/volatility/features_ext.py` (funding-conditioned features), `src/volatility/targets.py`, `src/volatility/eval.py`. Make reusable, tested, restartable.
- [ ] **B3) Leakage-resistant evaluation** - Chronological walk-forward ONLY. Freeze protocol in research_state before holdout. Purge/embargo by horizon. Normalize on train only. No random splits.
- [ ] **B4) Rigorous baselines+ablations** - B0/persistence, B1/RV-only (HAR-style), C1/RV+funding, C2/RV+funding+price features. All vs frozen splits. Block bootstrap for uncertainty.
- [ ] **B5) Run on ALL available admissible data** - Use cached panels + extract from raw cached data. Maximize coverage across symbols/time. Compute QLIKE, MAE/RMSE, calibration if binary targets.
- [ ] **B6) Document everything** - Write `research_state/evaluation_summary_VOLATILITY_YYYYMMDDTHHMMSSZ.md` with full metrics, CI, ablations, gaps. Update run_manifest/hypothesis_registry.

### STREAM A: LIQUIDATION ACQUISITION (KEEP ALIVE - NO IDLE)
- [ ] **A1) Ironflow hardening** - Enhance monitoring, track probe diffs, maintain evidence. Test on every session start.
- [ ] **A2) Deep alt-source verification** - Re-probe REVIEW_REQUIRED with actual HTTP/rubric checks. Look for IPFS/Arweave/Zenodo/HF academic liquidation datasets. Document with full evidence.
- [ ] **A3) Blocker evidence fresh** - Maintain up-to-date `research_state/blocker_evidence_*.md` with timestamps/commands.

### STREAM C: TESTS & INFRASTRUCTURE (PARALLEL)
- [ ] **C1) Add tests** - Unit tests for new volatility features/eval/splits. Keep all 111+ passing.
- [ ] **C2) Checkpointing/resume** - Make everything idempotent.
- [ ] **C3) Update manifests** - Keep run_manifest.json, hypothesis_registry.json, experiment_frontier.json current.

## BOTTLENECKS TO ELIMINATE NOW
1. **Underutilizing Track B** - Repo has funding+volatility in name; build the full funding-conditioned volatility pipeline to publication-quality with strict leakage control.
2. **Idle waiting on Track A** - Never wait. Every minute goes to measurable progress on B or hardening A monitoring.
3. **Shallow evaluation** - Follow RESEARCH_PROMPT gates religiously. Freeze protocol, block bootstrap, purge horizons, correct for comparisons.
4. **Missing feature coverage** - Implement ALL pre-registered features from §7. No shortcuts.

## RESUME TRIGGERS
- **Track A:** Ironflow returns 200 for >=2026-11 with liquidation events/fills matching FCLR-010 schema OR new unauthenticated source passes FULL rubric (>=5 symbols or equivalent, >=complete month, schema mappable, no keys/signed/requester-pays).
- **Track B:** Runs whenever unblocked - it IS unblocked now. No gate blocking it.

## MANDATORY DELIVERABLES THIS SESSION
- [ ] Concrete Track B feature extensions + evaluation run with numbers (QLIKE/MAE/RMSE, baselines+ablations)
- [ ] Fresh `research_state/evaluation_summary_VOLATILITY_YYYYMMDDTHHMMSSZ.md`
- [ ] Updated `research_state/experiment_frontier.json` reflecting dual-track + concrete next steps
- [ ] Updated this `AGENT_HANDOFF.md` with successor's exact next task
- [ ] All tests passing
- [ ] Track A monitoring updated with fresh evidence

## CRITICAL RULES
- **Research only. No trading/paper/live/API orders.**
- **No credentials. Unauthenticated only.**
- **No .github/workflows changes.**
- **Leakage-resistant: chronological splits, train-only normalization, purge/embargo, freeze before holdout.**
- **Separate tracks: modeled breaches != observed liquidations.**
- **Heavy work always. If Track A blocked, 3x effort on Track B.**
- **Evidence-based. Timestamp everything.**

## UPDATE (20261103T061400Z) - TRACK B EVALUATION RUN
- Created volatility modules: src/volatility/features_ext.py, src/volatility/eval.py
- Ran leakage-resistant evaluation on frozen panel (19488 rows, 5 symbols) with splits train/val/test per manifest
- Results written to research_state/evaluation_summary_VOLATILITY_20261103T061321Z.md
- Test split: B1 (RV-only) QLIKE~0.66255, C1 (RV+funding) very similar/slightly better in this naive form, C2 mixed - need proper train-only normalization + rigorous ablations + block bootstrap
- Stream A: Ironflow still blocked (forward 404, consec_absent=3). Monitoring active.
- Tests still passing (111/111)
