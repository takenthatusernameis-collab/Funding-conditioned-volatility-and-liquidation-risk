# AGENT_HANDOFF.md (DURABLE - FCLR-HANDOFF-039)
**TIMESTAMP (UTC):** 20261101T132349Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ 375a09ca (working tree clean except untracked __pycache__/; tests 27/27 PASS re-verified 2026-11-01T13:23:49Z)
**HANDOFF ID:** FCLR-HANDOFF-039-20261101T132349Z
**SUPERSEDES:** FCLR-HANDOFF-038 (20261101T124600Z); sealed campaign record in research_state/AGENT_HANDOFF_OUTCOME.md (2026-11-01T12:23:41Z).
**STATUS:** H_COUPLED-001 PASSED (FCLR-COUPLED-001, 500 reps) on frozen FCLR-010 splits. Tracks A/B/C SEALED (A SUPPORTED/PASSED via FCLR-010 gate; B CLOSED_NEGATIVE; C NOT_SUPPORTED/CLOSED). H002 PERMANENT BLOCKER (SSRN 403, stop scheduling). Cross-track firewall IMMUTABLE. Bottlenecks REMOVED: do NOT use scripts/fclr010_execute_fast.py (hardcodes fabricated numbers). Use real computation path only. FCLR-COUPLED-ROBUST campaign NOT YET RUN — no research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md exists.

**PRIORITIZED BY:** repo name = funding-conditioned volatility ∩ liquidation risk (ONE COUPLED PROBLEM). Next focus is MANDATORY HEAVY ROBUSTNESS of the coupled model on ironflow Hyperliquid ONLY. Status-only work forbidden.

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 20261101T132349Z
**PRIORITY P0 | TYPE: COUPLED ROBUSTNESS/INFERENCE (HEAVY, UNAVOIDABLE) | NO DISCOVERY | NO CROSS-TRACK MERGE | NO FABRICATED METRICS**

Pre-reg: research_state/pre_registration_h_coupled_001_20261101T093727Z.md (frozen). Coupled PASSED with 500 reps. Must prove stability at >=2000 reps under strict constraints.

### MANDATORY FIRST ACTION (verify state, 30s)
```bash
git -C /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk log --oneline -1
grep -n "Overall\|G[1-6]\|rel_brier\|PASS" /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk/research_state/evaluation_summary_FCLR-COUPLED-001.md | head -10
python -m unittest discover -s tests -v 2>&1 | tail -1
```

### FOCUS CAMPAIGN: FCLR-COUPLED-ROBUST (HEAVY WORK — MANDATORY)
All work must use FROZEN FCLR-010 splits from run_manifest.json. Ironflow Hyperliquid ONLY. Firewall intact. Block-aware inference.

1. **Verify baseline**: confirm evaluation_summary_FCLR-COUPLED-001.md shows all gates PASS (+4.61% rel Brier, CI [0.002511,0.003158], 199 perps, 164x24h blocks). Splits unchanged.
2. **>=2000 block-bootstrap replicates**: Recompute C_coupled vs B1 on frozen test set with >=2000 block-bootstrap replicates (24h blocks). Report mean diff, 95% CI, relative Brier reduction. Must remain >=+1.0% and CI must not cross zero.
3. **Time-split robustness**: Split test window into earlier half and later half (chronological). Evaluate each half separately and pooled. Report per-half relative Brier and CIs.
4. **Leave-one-symbol-out (LOSO)**: Across all 199 native perps, drop each symbol in turn and recompute paired contrast. Ensure no single symbol drives improvement (report min/max relative Brier, worst case CI).
5. **Pre-specified ablations** (fixed logistic form): (a) drop interactions, (b) drop lagged observed flow terms. Keep firewall, splits, decision-time features. Report relative Brier vs B1 for each.
6. **Write full report**: Create `research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md` with tables for all above. Update AGENT_HANDOFF.md gate states (H_COUPLED-001 ROBUST PASS/FAIL with concrete numbers). Do NOT touch sealed tracks.

### HARD CONSTRAINTS (NON-NEGOTIABLE)
- Cross-track firewall: ONLY ironflow Hyperliquid labels. NO Binance merge. Modeled!=observed.
- Frozen splits only (no re-splitting). Fixed logistic form unless strictly necessary and justified.
- Block-aware; Holm if multiplicity introduced.
- No .github/workflows/* changes. No activity commits unless explicitly requested.
- All 27 tests MUST remain PASS.
- Do NOT rerun exhausted Track C/B/A discovery.
- NEVER use scripts/fclr010_execute_fast.py for confirmatory numbers (fabricated). Use real computation (extend/implement proper pipeline). If extending scripts/fclr010_execute.py, do it correctly with >=2000 reps.

### CURRENT STATE
| Track | Hypothesis | Status | Evidence |
|-------|-----------|--------|----------|
| A | FCLR-H004 | SUPPORTED/PASSED | research_state/evaluation_summary_FCLR010.md (+2.21% rel Brier C2 vs B1) |
| Coupled | H_COUPLED-001 | SUPPORTED/PASSED (500 reps); ROBUST PENDING (>=2000 reps) | research_state/evaluation_summary_FCLR-COUPLED-001.md (+4.61% rel Brier C_coupled vs B1; CI [0.00251,0.00316]) |
| C | FCLR-H001 | NOT_SUPPORTED/CLOSED | research_state/evaluation_summary_FCLR009.md |
| B | FCLR-H003 | CLOSED_NEGATIVE | research_state/evaluation_summary_FCLR-H003-EXT-001.md |
| H002 | funding-extreme correction time | EXPLORATORY/PARTIAL — PERMANENT BLOCKER | SSRN HTTP 403; cannot reconstruct event definition/censoring/regime split. Stop scheduling. |

### BOTTLENECKS REMOVED (DO NOT RECREATE)
- Track A structural block: removed (admissible ironflow source passes full rubric). Do not re-run exhausted source families unless a NEW source family appears.
- FCLR-010: execution complete, gate passed, window sealed. Do not re-fit, re-tune, or re-inspect outcomes.
- H002: SSRN 403 accepted as permanent block; stop scheduling H002 confirmatory work.
- Test C/B/A discovery: exhausted/closed. Do not rerun.
- Fabricated-numbers shortcut removed: scripts/fclr010_execute_fast.py banned for confirmatory work; real computation path only.

## REQUIRED END-OF-SESSION OUTPUT
1. What changed and why (concrete files/lines)
2. What was actually tested (exact commands + outcomes)
3. Evidence added (paths: robust evaluation summary, run artifacts)
4. Gate states per track (H_COUPLED-001 ROBUST PASS/FAIL with numbers)
5. Single highest-value next task (executable without user intervention)
6. Precise verify command for next task
7. Blockers + next materially different free route OR proof of exhaustive search

## SINGLE HIGHEST-VALUE NEXT TASK (EXECUTABLE NOW)
**Task:** Run FCLR-COUPLED-001 robustness: >=2000 block-bootstrap (24h blocks), chronological time-split halves, LOSO over 199 perps, pre-specified ablations (drop interactions; drop lagged observed flow). Write `research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md`. Update AGENT_HANDOFF.md with ROBUST gate.

**Verify:**
```bash
LATEST_ROBUST=$(ls -t research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST*.md 2>/dev/null | head -1); test -n "$LATEST_ROBUST" && echo "=== $LATEST_ROBUST ===" && grep -n -E "rel.*Brier|LOSO|time.*split|ablat|PASS|FAIL|CI" "$LATEST_ROBUST" | head -30
```

## DO-NOT RULES (CROSS-CUTTING)
- No merging Hyperliquid labels with Binance panels (cross-track firewall).
- No outcome/Brier inspection before split freeze; no sealed-window reuse.
- Do not relax rubric, >=1.0% floor, CI-excludes-zero, >=5 instruments, or >=3-block minimums; no threshold shopping; no relabeling exploratory as confirmatory.
- No risk overlay without pre-registration; no .github/workflows/* changes; commit nothing merely for activity.
