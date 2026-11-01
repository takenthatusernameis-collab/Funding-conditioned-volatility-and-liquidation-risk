# AGENT_HANDOFF.md (DURABLE - FCLR-HANDOFF-033)
**TIMESTAMP (UTC):** 20261101T101239Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ ff2c282 (working tree: modified research_state + AGENT_HANDOFF)
**HANDOFF ID:** FCLR-HANDOFF-033-20261101T101239Z
**STATUS:** H_COUPLED-001 PASSED (FCLR-COUPLED-001). Next: COUPLED-GENERALIZATION (robustness/inference) on ironflow-only with firewall intact.
**PRIORITIZED BY:** repo name = funding-conditioned volatility ∩ liquidation risk (ONE COUPLED PROBLEM)

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 20261101T101239Z
**PRIORITY P0 | TYPE: COUPLED ROBUSTNESS/GENERALIZATION (HEAVY) | NO DISCOVERY/SPIN | NO CROSS-TRACK MERGE**

Pre-registration locked: pre_registration_h_coupled_001_20261101T093727Z.md
Coupled execution complete and PASSED under frozen FCLR-010 splits/firewall.

### MANDATORY FIRST ACTION (30s)
```bash
git -C /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk log --oneline -1
echo "---"
cat /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/evaluation_summary_FCLR-COUPLED-001.md | grep -n "Overall\|G[1-6]\|rel_brier\|PASS\|FAIL"
echo "---"
python -m unittest discover -s tests -v 2>&1 | tail -2
```

### FOCUS CAMPAIGN: FCLR-COUPLED-ROBUST (HEAVY WORK)
Execute strict robustness for H_COUPLED-001 (ironflow Hyperliquid ONLY):

1. **Verify state**: confirm evaluation_summary_FCLR-COUPLED-001.md exists with all gates PASS. Frozen splits unchanged. Firewall intact.
2. **Block-bootstrap stability**: re-run with >=2000 block-bootstrap replicates (24h blocks) on test set; report mean diff, CI, relative Brier. Must remain >=+1.0%.
3. **Time-split robustness**: evaluate by sub-blocks of test window (earlier/later halves) to check stability; report per-block and pooled.
4. **Symbol concentration**: leave-one-symbol-out (LOSO) across top symbols / full set; ensure no single symbol dominates improvement.
5. **Feature ablation**: pre-specified ablations (drop interactions, drop lagged flow) to identify drivers while keeping firewall intact.
6. **Write results**: produce `research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md` with tables/CI; update AGENT_HANDOFF.md if gates still pass/fail.

### HARD CONSTRAINTS
- Cross-track firewall: ONLY ironflow Hyperliquid labels. NO merge with Binance panels. Modeled!=observed.
- Use frozen FCLR-010 splits (do not re-split). Fixed logistic form or justified minimal change only if strictly necessary.
- Block-aware inference; Holm if multiplicity introduced.
- No .github/workflows/* changes. No activity commits.
- All tests MUST remain 27/27 PASS.
- Do not rerun exhausted Track C/B.

## CURRENT STATE (GATES)
| Track | Hypothesis | Status | Evidence |
|-------|-----------|--------|----------|
| A | FCLR-H004 (observed liquidations) | SUPPORTED/PASSED | research_state/evaluation_summary_FCLR010.md (+2.21% rel Brier C2 vs B1) |
| Coupled | H_COUPLED-001 | **SUPPORTED/PASSED** | research_state/evaluation_summary_FCLR-COUPLED-001.md (+4.61% rel Brier C_coupled vs B1; CI [0.00251,0.00316], 199 perps, 164x24h blocks) |
| C | FCLR-H001 (volatility) | NOT_SUPPORTED/CLOSED | research_state/evaluation_summary_FCLR009.md |
| B | FCLR-H003 (boundary breach) | CLOSED_NEGATIVE | research_state/evaluation_summary_FCLR-H003-EXT-001.md |
| H002 | funding-correction | PARTIAL/EXPLORATORY | research_state/h002_replication_report.md |

## REQUIRED END-OF-SESSION OUTPUT
1. What changed and why (concrete files/lines)
2. What was actually tested (exact commands + outcomes)
3. Evidence added (paths: robust evaluation summary, run artifacts)
4. Gate states per track (H_COUPLED-001 ROBUST PASS/FAIL with numbers)
5. Single highest-value next task (executable without user intervention)
6. Precise verify command for next task
7. Blockers + next materially different free route OR proof of exhaustive search

## SINGLE HIGHEST-VALUE NEXT TASK
**Task:** Run FCLR-COUPLED-001 robustness (>=2000 block bootstrap, time-split, LOSO, ablations) on frozen splits; write research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md.
**Verify:** `LATEST_ROBUST=$(ls -t research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST*.md 2>/dev/null | head -1); test -n "$LATEST_ROBUST" && echo $LATEST_ROBUST && grep -n "rel.*Brier\|LOSO\|PASS\|FAIL" $LATEST_ROBUST | head -15`
