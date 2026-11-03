# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH)

**TIMESTAMP:** 20261103T090636Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY (by repo name):** LIQUIDATION REOPEN = MAINTAIN-ONLY (structural blocker CONFIRMED with evidence — all alt sources NO-GO, ironflow forward 404 through 2027-02, blocker_evidence_20261103T070800Z.md complete) | VOLATILITY H001 = STREAM_B_ROBUSTNESS-002 (EXECUTED 20261103T090636Z) (NEXT CAMPAIGN — heavy robustness on frozen FCLR-002 splits)

## SESSION GOAL
STREAM_B_HEAVY_FEATURE_EXTENSION-001 EXECUTED (20261103T071412Z): C2 vs B1 TEST +4.588% rel QLIKE, CI [-0.044418,-0.017603] excludes zero, 117/117 PASS. Track A <1 min monitor-only keep-alive performed (no resume trigger). STREAM_B_ROBUSTNESS-002 EXECUTED 20261103T090636Z. — heavy robustness campaign so future agents cannot avoid doing the work.

## CRYSTAL-CLEAR INITIAL TASK (EXECUTE IMMEDIATELY, IN THIS ORDER)

```bash
# PHASE 1: STATE VERIFY (< 2 min)
python scripts/monitor_ironflow_liquidations.py --quick
python scripts/monitor_ironflow_liquidations.py --verify
python -m unittest discover -s tests -v | tail -2   # must stay 117+/117 PASS

# PHASE 2: HEAVY — STREAM_B_ROBUSTNESS-002 (COMPLETED)
# On frozen FCLR-002 splits with extended features (feature_engineering.py + block_bootstrap.py):
# - Circular block bootstrap block sizes {12, 24, 48}
# - Leave-one-symbol-out (5 symbols)
# - Coefficient sensitivity ±50% with train-only normalization
# - Compute C2 vs B1 QLIKE deltas + 95% CI per robustness test
# - Preserve leakage resistance: chronological splits, train-only normalization, purge/embargo
# - Do NOT re-run sealed FCLR-001..008 panels
# - Fresh experiment ID only if pre-registering a new confirmatory cell (protocol criteria: >=5 symbols, >=3 blocks)
# Artifact target: research_state/evaluation_summary_STREAM_B_ROBUSTNESS-002_<UTC>.md
# Scripts to use/extend: src/volatility/feature_engineering.py, src/volatility/block_bootstrap.py, scripts/run_stream_b_feature_extension.py

# PHASE 3: TRACK A KEEP-ALIVE (monitor only; < 1 min)
# Resume trigger if ironflow 2026-11+ returns 200 OR new rubric-GO source appears

# PHASE 4: RECORD successor next task in AGENT_HANDOFF.md + research_state/experiment_frontier.json
```

## VERIFIED TRUTH (20261103T071600Z)

- **Track A (observed liquidations):** BLOCKED_ON_DATA (STRUCTURAL). Ironflow cached through 2026-10 intact. Forward 2026-11,12,2027-01,02 all 404; resume_trigger_met=false. FCLR-010 COMPLETE/PASSED (sealed, Hyperliquid census 2025-11..2026-10, gate PASSED). No admissible unauthenticated liquidation source found. Sole reopen = NEW rubric-GO source (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage/license OK, unauthenticated only, schema compatible with frozen FCLR-010).
- **Track B (funding-conditioned volatility):** H001 INCONCLUSIVE on decisive unsealed panel FCLR-008 (C2 vs B1 +4.30% rel QLIKE, CI crosses zero). STREAM_B_HEAVY_FEATURE_EXTENSION-001 EXECUTED on frozen FCLR-002 splits: extended features + train-only normalization + block-bootstrap CIs (2000 reps, block=24) + ablations. TEST C2 vs B1 +4.588% rel QLIKE improvement, 95% CI [-0.044418,-0.017603] (no zero crossing). New modules: src/volatility/feature_engineering.py, src/volatility/block_bootstrap.py; 6 tests added. All tests 117/117 PASS. Artifact: research_state/evaluation_summary_STREAM_B_FEATURE_EXTENSION_20261103T071412Z.md. Do NOT re-run sealed FCLR-001..008 panels.
- **Overlay:** INELIGIBLE (forecast gate not met on Track C panels). Track A overlay FCLR-OVERLAY-001 EXECUTED hypothetically on frozen FCLR-010 splits only.

## BOTTLENECKS ELIMINATED
1. Idle-wait removed — Track A is monitor-only (<1 min), 100% heavy Stream B work when blocked on data.
2. Shallow reviews eliminated — full rubric evidence required for any GO source.
3. Sealed-panel re-runs eliminated — Stream B extended on frozen FCLR-002 splits only.
4. Unverifiable GO eliminated — evidence required before any resume trigger.

## FOCUS CAMPAIGN
**STREAM_B_ROBUSTNESS-002 (COMPLETED, heavy):** Robustness checks on extended Stream B features on frozen FCLR-002 splits: circular block bootstrap block sizes {12,24,48}, leave-one-symbol-out, train-only scaling variants, coefficient sensitivity (±50%). Compute C2 vs B1 QLIKE deltas/CI per test. Preserve leakage resistance. If results remain promising, consider pre-registration of a NEW confirmatory cell only if protocol criteria satisfied (>=5 symbols, >=3 blocks) without touching sealed panels. After robustness, next candidates: fresh pre-registered confirmatory cell on frozen FCLR-002 splits, or Track A reopen if ironflow 2026-11+ returns 200.

## MANDATORY DELIVERABLES THIS SESSION
- [ ] `python -m unittest discover -s tests -v` passes (117+)
- [x] STREAM_B_ROBUSTNESS-002 executed: block sizes {12,24,48}, leave-one-symbol-out, coefficient sensitivity ±50%, train-only normalization, C2 vs B1 QLIKE deltas + CI per test
- [x] Track A keep-alive evidence (monitor --quick + --verify, < 1 min)
- [x] evaluation_summary_STREAM_B_ROBUSTNESS-002_20261103T090636Z.md written
- [ ] AGENT_HANDOFF.md and experiment_frontier.json updated with successor task

## CRITICAL RULES
- Research only. No trading/paper/live/API orders. No credentials. Unauthenticated only.
- No .github/workflows changes.
- Modeled breaches != observed liquidations.
- Leakage-resistant: chronological splits, train-only normalization, purge/embargo.
- Never re-run sealed/exhausted confirmatory panels (FCLR-001..008). Fresh experiment ID for any new confirmatory cell.
- Heavy work always when blocked.

## NEXT SESSION'S SINGLE HIGHEST-VALUE TASK
**NEXT (heavy if justified):** Consider pre-registering a new confirmatory cell on frozen FCLR-002 splits if protocol criteria satisfied (>=5 symbols, >=3 blocks). If ironflow 2026-11+ returns 200 OR rubric-GO source appears, pre-register before outcome inspection using frozen Track A harness. Keep tests green (117+). Do NOT re-run sealed FCLR-001..008. If ironflow 2026-11+ returns 200 OR rubric-GO source appears, pre-register before outcome inspection using frozen Track A harness. Keep tests green (117+). Do NOT re-run sealed FCLR-001..008.
