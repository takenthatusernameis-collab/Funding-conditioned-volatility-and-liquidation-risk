# AGENT_HANDOFF.md (DURABLE - FCLR-HANDOFF-032)
**TIMESTAMP (UTC):** 20261101T093752Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ f79c9767 (working tree: clean except __pycache__)
**HANDOFF ID:** FCLR-HANDOFF-032-20261101T093752Z
**STATUS:** H_COUPLED-001 PRE-REGISTERED. Next: EXECUTE FCLR-COUPLED-001 on frozen FCLR-010 protocol.
**PRIORITIZED BY:** repo name = funding-conditioned volatility ∩ liquidation risk (ONE COUPLED PROBLEM)

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 20261101T093752Z
**PRIORITY P0 | TYPE: COUPLED EXECUTION (HEAVY) | NO DISCOVERY/SPIN**

Pre-registration locked: pre_registration_h_coupled_001_20261101T093727Z.md
Coupled synthesis complete. FCLR-010 (Track A) PASSED (+2.21% rel Brier C2 vs B1). Track C closed negative; Track B closed negative. Next is to test coupling on observed liquidations only.

### MANDATORY FIRST ACTION (30s)
ee273344 chore(kilo): checkpoint agent session
 M AGENT_HANDOFF.md
 M scripts/__pycache__/campaign_resume.cpython-312.pyc
 M scripts/__pycache__/diagnostics_scanner.cpython-312.pyc
 M scripts/__pycache__/fclr006_block_audit.cpython-312.pyc
 M scripts/__pycache__/forecast_pipeline.cpython-312.pyc
 M scripts/__pycache__/funding_correction_replication.cpython-312.pyc
 M scripts/__pycache__/nonfinite_serialization.cpython-312.pyc
 M scripts/__pycache__/synthetic_boundary_labels.cpython-312.pyc
 M tests/__pycache__/test_campaign_resume.cpython-312.pyc
 M tests/__pycache__/test_controller_progress_accounting.cpython-312.pyc
 M tests/__pycache__/test_fclr002_coverage_audit.cpython-312.pyc
 M tests/__pycache__/test_fclr006_block_audit.cpython-312.pyc
 M tests/__pycache__/test_forecast_pipeline.cpython-312.pyc
 M tests/__pycache__/test_funding_correction_replication.cpython-312.pyc
 M tests/__pycache__/test_funding_correction_robustness.cpython-312.pyc
 M tests/__pycache__/test_nonfinite_result_serialization.cpython-312.pyc
 M tests/__pycache__/test_synthetic_boundary_labels.cpython-312.pyc
 M tests/__pycache__/test_workflow_diagnostics_scanner.cpython-312.pyc
?? research_state/pre_registration_h_coupled_001_20261101T093727Z.md
---
154:  "frozen_before_outcomes": true,
178:  "frozen_before_outcomes": true
---
-rw------- 1 runner runner 5.7K Nov  1 09:37 /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/pre_registration_h_coupled_001_20261101T093727Z.md

### FOCUS CAMPAIGN: FCLR-COUPLED-EXEC (HEAVY WORK)
Execute H_COUPLED-001 per pre-registration with firewall intact:

1. **Verify state**: confirm FCLR-010 splits frozen in run_manifest.json (train/val/test, embargo). Confirm ironflow cache present. Confirm no Binance merge.
2. **Build coupled features**: implement minimal feature builder for ironflow panel (funding×vol×lagged observed flow + interactions). Decision-time only; lags use history up to t-ε. No tuning.
3. **Fit fixed logistic**: B1 = FCLR-010 C2 (locked). C_coupled = fixed logistic with pre-specified features. No regularization search/hyperparams.
4. **Evaluate OOS**: test set only. Paired block-bootstrap (~24h blocks, >=2000 reps). Compute Brier/logloss/calibration/AUPRC.
5. **Gate**: check G1>=+1.0% rel Brier (C_coupled vs B1), G2>=5 perps, G3>=3 blocks, G4 firewall, G5 calibration. Write `research_state/evaluation_summary_FCLR-COUPLED-001.md`.
6. **Update state**: set experiment in `research_state/experiment_frontier.json` (H_COUPLED-001), update AGENT_HANDOFF.md outcome if needed.

### HARD CONSTRAINTS
- Cross-track firewall: ONLY ironflow Hyperliquid labels. NO merge with Binance panels. Modeled!=observed.
- No re-running exhausted Track C/B panels. No broad data discovery.
- Use frozen FCLR-010 splits (do not re-split). Fixed logistic, no tuning.
- Block-aware inference; Holm if multiplicity introduced.
- No .github/workflows/* changes. No activity commits.
- All tests MUST remain 27/27 PASS.

## CURRENT STATE (GATES)
| Track | Hypothesis | Status | Evidence |
|-------|-----------|--------|----------|
| A | FCLR-H004 (observed liquidations) | SUPPORTED/PASSED | research_state/evaluation_summary_FCLR010.md (+2.21% rel Brier C2 vs B1) |
| Coupled | H_COUPLED-001 | PRE-REGISTERED | /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/pre_registration_h_coupled_001_20261101T093727Z.md |
| C | FCLR-H001 (volatility) | NOT_SUPPORTED/CLOSED | research_state/evaluation_summary_FCLR009.md |
| B | FCLR-H003 (boundary breach) | CLOSED_NEGATIVE | research_state/evaluation_summary_FCLR-H003-EXT-001.md |
| H002 | funding-correction | PARTIAL/EXPLORATORY | research_state/h002_replication_report.md |

## REQUIRED END-OF-SESSION OUTPUT
1. What changed and why (concrete files/lines)
2. What was actually tested (exact commands + outcomes)
3. Evidence added (paths: evaluation summary, run artifacts)
4. Gate states per track (H_COUPLED-001 PASS/FAIL with numbers)
5. Single highest-value next task (executable without user intervention)
6. Precise verify command for next task
7. Blockers + next materially different free route OR proof of exhaustive search

## SINGLE HIGHEST-VALUE NEXT TASK
**Task:** Execute FCLR-COUPLED-001 per pre-registration against frozen FCLR-010 splits; produce evaluation_summary_FCLR-COUPLED-001.md with paired block-bootstrap vs B1.
**Verify:** `LATEST_COUPLED_EVAL=$(ls -t research_state/evaluation_summary_FCLR-COUPLED-001*.md 2>/dev/null | head -1); test -n "$LATEST_COUPLED_EVAL" && echo $LATEST_COUPLED_EVAL && grep -n "rel.*Brier\|G[1-6]\|PASS\|FAIL" $LATEST_COUPLED_EVAL | head -12`
