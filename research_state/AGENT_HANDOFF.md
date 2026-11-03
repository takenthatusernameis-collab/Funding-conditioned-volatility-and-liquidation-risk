# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T115607Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY (by repo name):** 1) LIQUIDATION RISK (Track A/H004) 2) FUNDING-CONDITIONED VOLATILITY (Track C/H001/H002)
**MODE:** HEAVY_ANALYSIS_CAMPAIGN - NO IDLE TIME - EVERY TURN MUST PRODUCE DURABLE ARTIFACTS

---

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (CLEAR & MANDATORY)

**START HERE. DO NOT DEVIATE.**

You have been handed a repo that explicitly prioritizes "Funding-conditioned-volatility-and-liquidation-risk". The highest leverage path forward is:

1. **ELIMINATE THE BLOCKER**: FCLR-002 only has 2 non-overlapping 30-day blocks (< 3 required). You MUST build FCLR-011 from the 2026 Jan-Aug archives that are already on disk (markPriceKlines, indexPriceKlines, premiumIndexKlines, fundingRate zips). This is heavy computable work with all inputs present.
2. **CONSOLIDATE LIQUIDATION INTELLIGENCE**: FCLR-010 passed the forecast gate (C2 vs B1 Brier rel reduction 2.21%, CI excludes zero) but new liquidation labels have not arrived (ironflow 404). Build the liquidation feature pipeline from cached ironflow data through 2026-10 now - do NOT wait for new labels.
3. **PROVE OR DISPROVE**: Either produce a confirmatory FCLR-011 run that meets all gates, OR produce a machine-checkable impossibility proof with exact symbol/day/block counts and hash anchors.

**IF YOU ARE TEMPTED TO POLL OR WAIT:** You cannot. Track A only resumes on concrete HTTP 200 for YYYY-MM >= 2026-11. All other work must proceed in parallel with monitoring (quick check only).

---

## VERIFIED TRUTH (current state)

- **Track A (observed liquidations, ironflow/Hyperliquid):** FCLR-010 COMPLETE, FORECAST_GATE_PASSED (C2 vs B1 Brier rel reduction 2.21%, CI [-0.004892,-0.001263] excludes zero, 199 instruments, 5x30-day blocks). SEALED. Forward months 2026-11,12,2027-01,02 all return 404 (consec_absent=3). All admissible unauthenticated alternatives deep-reviewed - NO-GO. Structural data blocker: no new liquidation labels exist yet. Overlay executed (hypothetical only, no profitability claim).
- **Track B (modeled boundary breaches/H003):** CLOSED_NEGATIVE, NOT_SUPPORTED (sealed).
- **Track C (volatility forecasting/H001):** INCONCLUSIVE. FCLR-003 sealed (-3.78%, CI crosses), FCLR-006 (-69.90%), FCLR-007 (-3.42%), FCLR-008 (+4.30% but CI crosses). No confirmatory pass.
- **H002 (funding-extreme correction):** PARTIAL_REPLICATION (direction matches, p=0.0792, SSRN 403 blocks exact).
- **H004:** SUPPORTED via FCLR-010.
- **BOTTLENECK:** FCLR-002 has only 2 non-overlapping 30-day blocks (<3 required). Must resolve via FCLR-011 from raw archives OR impossibility proof.
- **Tests:** 117/117 PASS at HEAD. No workflow changes.
- **Data:** 2026 Jan-Aug mark/index/premium/funding data cached. 2024 Q1 present. 2026 Oct ironflow cached through end of month.

---

## BOTTLENECK REMOVAL (enforced)

- **NO POLLING LOOPS:** `monitor_ironflow_liquidations.py --quick` only (<60s). Never cron/poll. Resume Track A work only if HTTP 200 for >=2026-11.
- **SEALED EXPERIMENTS FROZEN:** FCLR-001/002/003/005/006/007/008/009/H003-EXT. Analysis-only. No re-runs.
- **MANDATORY BLOCK-COUNT RESOLUTION:** FCLR-002 bottleneck cannot be worked around. Build FCLR-011 panel from 2026 archives OR produce impossibility proof with machine-checkable counts.
- **NO IDLE SESSIONS:** If Track A has no new data, you MUST execute Campaign 1 or Campaign 3. There is always heavy work available.

---

## NEXT FOCUS CAMPAIGN (EXECUTE IN ORDER - UNAVOIDABLE HEAVY WORK)

### CAMPAIGN 1: FCLR-011 CONFIRMATORY CELL BUILD (REPO-NAME PRIMARY - HIGHEST PRIORITY)
**Goal:** Resolve the FCLR-002 block-count bottleneck with verifiable evidence.

1. **PRE-REGISTER FIRST (BEFORE ANY OUTCOME PEEK)**
   Create `research_state/pre_registration_fclr011_$(date -u +%Y%m%dT%H%M%SZ).md`. Use `research_protocol_fclr008.md` v1.0 as template with new version. Freeze: hypothesis FCLR-H001, universe (>=5 symbols), train/val/test splits by timestamp, embargo (>=7 days), primary contrast C2 vs B1 on 24h QLIKE, block bootstrap (>=2000 reps), materiality floor >=2%, Holm multiplicity, block structure requirement >=3 non-overlapping 30-day test blocks. **Splits frozen BEFORE any results computed.**

2. **BUILD LEAKAGE-RESISTANT PANEL (HEAVY COMPUTATION)**
   Ingest from root raw archives: `markPriceKlines-1h-2024-*`, `indexPriceKlines-1h-2024-*`, `premiumIndexKlines-1h-2024-*`, `klines-1h-2024-*`, and all `*fundingRate*` zips for 2026 Jan-Aug. Enforce: forecast timestamp t only uses data available <= t, trailing-only features, training-only normalization (store means/stds), purge/embargo, common paired panel across >=5 symbols, UTC alignment. Output: `research_state/data_cache/fclr011_panel.json` (with schema + hashes) and `research_state/fclr011_coverage_audit.json` (per-symbol coverage, common timestamps, block structure).

3. **VALIDATE CRITERIA**
   If `fclr011_coverage_audit.json` shows >=5 symbols AND >=3 non-overlapping 30-day test blocks: proceed to step 4. Else: proceed to step 5.

4. **EXECUTE CONFIRMATORY RUN (IF CRITERIA MET)**
   Run FCLR-011 with frozen protocol. Compute block bootstrap CIs. Write `research_state/evaluation_summary_FCLR-011_$(date -u +%Y%m%dT%H%M%SZ).md` with full metrics, uncertainty, multiplicity, leakage checklist. Assess forecast gate (>=2% rel QLIKE reduction, CI excludes zero). Update `run_manifest.json`.

5. **IF INFEASIBLE - IMPOSSIBILITY PROOF (IF CRITERIA NOT MET)**
   Write `research_state/block_count_resolution_fclr011_$(date -u +%Y%m%dT%H%M%SZ).md` with machine-checkable tables: symbols examined, days available per symbol, common-day intersection, possible 30-day block partitions, exact shortfall, file hashes of all inputs used, and conclusion with evidence. This is a valid completion of the bottleneck removal - do NOT fabricate data.

### CAMPAIGN 2: TRACK A LIQUIDATION INTELLIGENCE (LIQUIDATION-FIRST - PARALLEL)
**Goal:** Maximize liquidation-track value while waiting for new labels.

1. **CONSOLIDATE EVIDENCE**
   Create `research_state/track_a_fclr010_consolidated.md` merging FCLR-010 results, coverage, leakage audit, gate decision, and overlay status into a single auditable bundle.

2. **BUILD LIQUIDATION FEATURE PIPELINE (HEAVY)**
   From cached ironflow data (`research_state/data_cache/` ironflow artifacts), build leakage-resistant features: liquidation intensity (count/notional), concentration, burst metrics, time-of-day, funding regime conditioning, volatility regime. All computed with trailing-only windows. Output `research_state/data_cache/track_a_liq_features.json` + schema.

3. **MONITOR ONLY (NON-POLLING)**
   Run `python scripts/monitor_ironflow_liquidations.py --quick` once. Append to `research_state/ironflow_watch_log.jsonl`. If HTTP 200 for YYYY-MM >= 2026-11 appears, ONLY THEN pre-register Track A window extension and run frozen harness - do NOT loop.

### CAMPAIGN 3: INFRASTRUCTURE & REPRODUCIBILITY (HARDENING - PARALLEL)
**Goal:** Make everything reproducible and keep tests green.

1. **TESTS**: Ensure `python -m unittest discover -s tests -v` passes (must stay >=117/117). Add minimal tests only if new code paths lack coverage.
2. **REPRODUCIBILITY**: Update `research_state/run_manifest.json` with git SHA, timestamps, artifact hashes for any new heavy files.
3. **DOCUMENTATION**: Update `research_state/research_protocol.md` with a brief "data exhaustion" note reflecting 2026 Jan-Aug coverage; keep all gates frozen.

---

## EXECUTION RULES (STRICT - ENFORCED)
- **PRE-REGISTER BEFORE PEEK:** For any new confirmatory experiment (FCLR-011), pre-register splits BEFORE computing outcomes.
- **NO SEALED RE-RUNS:** FCLR-001/002/003/005/006/007/008/009/H003-EXT are analysis-only.
- **NO POLLING:** Track A resume ONLY on concrete data arrival (HTTP 200 for >=2026-11). Monitor via --quick once per session.
- **NO WORKFLOW CHANGES:** Do not modify `.github/workflows/*`. All changes outside workflows.
- **TESTS MUST PASS:** >=117/117. Run after changes.
- **COMMIT DISCIPLINE:** Commit only coherent units of progress with clear messages. No empty/activity commits.
- **EVERY SESSION UPDATES HANDOFF:** Leave `research_state/AGENT_HANDOFF.md` updated with concrete next actions, files created, and evidence.

---

## IMMEDIATE NEXT ACTIONS (RUN NOW)
```bash
# 1) Read truth
cat research_state/AGENT_HANDOFF.md | head -60

# 2) Health check (non-polling)
python scripts/monitor_ironflow_liquidations.py --quick
python -m unittest discover -s tests -v 2>&1 | tail -2

# 3) START HEAVY WORK - CAMPAIGN 1 STEP 1
# Create pre-registration for FCLR-011 NOW (before looking at results)
date -u +%Y%m%dT%H%M%SZ  # note timestamp for filenames
```

**DEFAULT:** Start Campaign 1 immediately. If you finish Campaign 1 step 1, move to step 2 (build panel). Do not wait. Do not poll. Produce files.
