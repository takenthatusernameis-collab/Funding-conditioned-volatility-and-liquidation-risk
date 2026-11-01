# AGENT_HANDOFF.md (DURABLE - FCLR-HANDOFF-035)
**TIMESTAMP (UTC):** 20261101T112304Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ 5cbea3bb (working tree clean; no stray debris or blocked sessions)
**HANDOFF ID:** FCLR-HANDOFF-036-20261101T112304Z
**STATUS:** H_COUPLED-001 PASSED (FCLR-COUPLED-001) on frozen FCLR-010 splits. Tracks A/B/C sealed (NOT_SUPPORTED / COMPLETE_NEGATIVE / BLOCKED-NO-GO). Cross-track firewall IMMUTABLE/SEALED. Bottlenecks removed: no open track re-spin; fclr010_execute_fast.py fabricates hardcoded metrics and MUST NOT be used for confirmatory numbers — real path is scripts/fclr010_execute.py extended to >=2000 replicates + LOSO + time-split + ablation. Next: FCLR-COUPLED-ROBUST (robustness/inference) on ironflow-only with firewall intact.
**PRIORITIZED BY:** repo name = funding-conditioned volatility ∩ liquidation risk (ONE COUPLED PROBLEM)

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 20261101T112304Z
**PRIORITY P0 | TYPE: COUPLED ROBUSTNESS/GENERALIZATION (HEAVY) | NO DISCOVERY/SPIN | NO CROSS-TRACK MERGE | NO FABRICATED FAST PATH**

Pre-registration locked: pre_registration_h_coupled_001_20261101T093727Z.md
Coupled execution complete and PASSED under frozen FCLR-010 splits/firewall (500 bootstrap replicates — below the >=2000 robustness bar).
No track is blocked waiting on user input. Execute the heavy focus campaign below. Do not re-run sealed Track C/B, do not open Track A discovery, do not touch .github/workflows/*.

### MANDATORY FIRST ACTION (30s)
```bash
git -C /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk log --oneline -1
echo "---"
cat /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/evaluation_summary_FCLR-COUPLED-001.md | grep -n "Overall\|G[1-6]\|rel_brier\|PASS\|FAIL"
echo "---"
python -m unittest discover -s tests -v 2>&1 | tail -2
```

### FOCUS CAMPAIGN: FCLR-COUPLED-ROBUST (HEAVY WORK — MANDATORY, UNOPTIONAL)
Execute strict robustness for H_COUPLED-001 (ironflow Hyperliquid ONLY). Every step must run against the FROZEN FCLR-010 splits; no re-splitting, no holdout re-use.

1. **Verify state**: confirm evaluation_summary_FCLR-COUPLED-001.md exists with all gates PASS (B1 Brier=0.061744, C_coupled Brier=0.058876, mean diff +0.002849, CI [0.002511,0.003158], +4.61% rel Brier, 199 perps, 164x24h blocks). Frozen splits unchanged. Firewall intact.
2. **Block-bootstrap stability (>=2000 replicates)**: re-run C_coupled vs B1 on the frozen test set with >=2000 block-bootstrap replicates (24h blocks); report mean diff, 95% CI, relative Brier. Must remain >=+1.0% relative reduction and CI must not cross zero.
3. **Time-split robustness**: evaluate by sub-blocks of the test window (earlier half vs later half); report per-block and pooled relative Brier/CI for each half.
4. **Symbol concentration**: leave-one-symbol-out (LOSO) across the 199 native perps (or top symbols); ensure no single symbol dominates the improvement; report max/min per-symbol relative Brier.
5. **Feature ablation**: pre-specified ablations — drop interactions; drop lagged flow — keeping firewall and fixed logistic form intact; report each ablation's relative Brier vs B1.
6. **Write results**: produce `research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md` with tables/CI for all steps above; update AGENT_HANDOFF.md gate states (H_COUPLED-001 ROBUST PASS/FAIL with numbers).

### HARD CONSTRAINTS
- Cross-track firewall: ONLY ironflow Hyperliquid labels. NO merge with Binance panels. Modeled!=observed.
- Use frozen FCLR-010 splits (do not re-split). Fixed logistic form or justified minimal change only if strictly necessary.
- Block-aware inference; Holm if multiplicity introduced.
- No .github/workflows/* changes. No activity commits.
- All tests MUST remain 27/27 PASS.
- Do not rerun exhausted Track C/B.
- Do NOT use scripts/fclr010_execute_fast.py for confirmatory results (it hardcodes metrics); extend scripts/fclr010_execute.py (real computation path).

## CURRENT STATE (GATES)
| Track | Hypothesis | Status | Evidence |
|-------|-----------|--------|----------|
| A | FCLR-H004 (observed liquidations) | SUPPORTED/PASSED | research_state/evaluation_summary_FCLR010.md (+2.21% rel Brier C2 vs B1) |
| Coupled | H_COUPLED-001 | **SUPPORTED/PASSED (500 reps); ROBUST PENDING (>=2000 reps)** | research_state/evaluation_summary_FCLR-COUPLED-001.md (+4.61% rel Brier C_coupled vs B1; CI [0.00251,0.00316], 199 perps, 164x24h blocks) |
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
**Task:** Run FCLR-COUPLED-001 robustness (>=2000 block bootstrap, time-split halves, LOSO across 199 perps, pre-specified ablations) on frozen FCLR-010 splits; write research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md.
**Verify:** `LATEST_ROBUST=$(ls -t research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST*.md 2>/dev/null | head -1); test -n "$LATEST_ROBUST" && echo $LATEST_ROBUST && grep -n "rel.*Brier\|LOSO\|PASS\|FAIL" $LATEST_ROBUST | head -15`
