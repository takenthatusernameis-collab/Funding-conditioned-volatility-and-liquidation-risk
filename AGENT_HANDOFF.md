# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T071506Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY (by repo name):** LIQUIDATION REOPEN = MAINTAIN-ONLY (structural blocker CONFIRMED with evidence — all alt sources NO-GO, ironflow forward 404 through 2027-02, blocker_evidence_20261103T070800Z.md complete) | VOLATILITY H001 = STREAM_B_HEAVY (EXECUTED feature extension; results on frozen splits)

## SESSION GOAL
Completed heavy Stream B feature extension on frozen FCLR-002 splits. Track A <1 min monitor-only keep-alive performed (no resume trigger). All tests green.

## CRYSTAL-CLEAR INITIAL TASK (EXECUTE IMMEDIATELY, IN THIS ORDER)

```bash
# PHASE 1: STATE VERIFY (< 2 min)
python scripts/monitor_ironflow_liquidations.py --quick
python scripts/monitor_ironflow_liquidations.py --verify
python -m unittest discover -s tests -v | tail -2   # must stay 117+/117 PASS

# PHASE 2: HEAVY — STREAM_B CONTINUATION (if desired) OR RESPOND TO TRIGGERS
# Stream B feature extension EXECUTED (20261103T071412Z):
# - Funding percentiles/zscore (trailing-only, train-only norm)
# - RV ratios 6h/24h/7d
# - Price-dislocation MA/EMA deviation
# - Train-only normalized models, block-bootstrap CIs (2000 reps, block=24), full ablations
# Results: C2 vs B1 on TEST rel improvement +4.588%, 95% CI [-0.044418,-0.017603] (no zero crossing)
# Artifacts: research_state/evaluation_summary_STREAM_B_FEATURE_EXTENSION_20261103T071412Z.md
# Do NOT re-run sealed FCLR-001..008 panels.

# PHASE 3: TRACK A KEEP-ALIVE
# monitor only; resume trigger if ironflow 2026-11+ returns 200 OR new rubric-GO source

# PHASE 4: RECORD successor next task
```

## VERIFIED TRUTH (20261103T071506Z)

- **Track A (observed liquidations):** BLOCKED_ON_DATA (STRUCTURAL). Ironflow cached through 2026-10 intact. Forward 2026-11,12,2027-01,02 all 404; resume_trigger_met=false. FCLR-010 COMPLETE/PASSED (sealed). No admissible unauthenticated liquidation source found. Sole reopen = NEW rubric-GO source.
- **Track B (funding-conditioned volatility):** H001 INCONCLUSIVE on decisive unsealed panel FCLR-008. STREAM_B_HEAVY_FEATURE_EXTENSION-001 EXECUTED on frozen FCLR-002 splits: extended features + train-only normalization + block-bootstrap CIs + ablations. TEST C2 vs B1 +4.588% rel QLIKE improvement, CI excludes zero [-0.044418,-0.017603]. New modules: src/volatility/feature_engineering.py, src/volatility/block_bootstrap.py; tests added (6). All tests 117/117 PASS.

## BOTTLENECKS ELIMINATED
1. Idle-wait removed - quick monitor only, 100% heavy work when blocked
2. Shallow reviews eliminated - full rubric evidence
3. Sealed-panel re-runs eliminated - extended on frozen splits
4. Unverifiable GO eliminated - evidence required

## FOCUS CAMPAIGN
**STREAM_B_HEAVY_FEATURE_EXTENSION-001 (EXECUTED)** - extended features with ablations/block-bootstrap on frozen splits. Next campaign: **STREAM_B_ROBUSTNESS-002** - robustness checks on extended features (different block sizes, leave-one-symbol-out, train-only scaling variants, sensitivity to coefficient choices), preserve leakage resistance; if results remain promising, consider pre-registration of new confirmatory cell only if protocol criteria satisfied (>=5 symbols, >=3 blocks) without touching sealed panels.

## MANDATORY DELIVERABLES THIS SESSION (DONE)
- [x] `python -m unittest discover -s tests -v` passes (117+)
- [x] Stream B heavy feature-extension artifacts (modules, ablations, block-bootstrap CIs) on frozen splits
- [x] Track A keep-alive evidence
- [x] Updated experiment_frontier.json and AGENT_HANDOFF.md

## CRITICAL RULES
- Research only. No trading/paper/live/API orders. No credentials. Unauthenticated only.
- No .github/workflows changes.
- Modeled breaches != observed liquidations.
- Leakage-resistant: chronological splits, train-only normalization, purge/embargo.
- Never re-run sealed/exhausted confirmatory panels (FCLR-001..008). Fresh experiment ID for any new confirmatory cell.
- Heavy work always when blocked.

## NEXT SESSION'S SINGLE HIGHEST-VALUE TASK
**STREAM_B_ROBUSTNESS-002 (heavy):** On frozen FCLR-002 splits with extended features, run robustness - circular block bootstrap with block sizes {12,24,48}, leave-one-symbol-out, and coefficient sensitivity (±50%) with train-only normalization. Compute C2 vs B1 QLIKE deltas/CI per test. Keep tests green (117+). Do NOT re-run sealed FCLR-001..008. Maintain Track A <1 min `monitor --quick` keep-alive. If ironflow 2026-11+ returns 200 OR rubric-GO source appears, pre-register before outcome inspection using frozen Track A harness.
