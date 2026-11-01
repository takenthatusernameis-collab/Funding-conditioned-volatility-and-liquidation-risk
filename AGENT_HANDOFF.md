# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-01T19:14:29Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Research program TERMINAL. H001 NOT_SUPPORTED (FCLR-003 confirmatory gate NOT_MET; C2 vs B1 +3.78% worse, CI [-0.020240,0.056734] crosses zero); risk overlay INELIGIBLE. Track A: FCLR-010 forecast gate PASSED + H_COUPLED-001 ROBUST PASS + FCLR-OVERLAY-001 EXECUTED (hypothetical, no profitability claim). Track B CLOSED_NEGATIVE. Track C closed negative (FCLR-006/008 NOT_MET). H002 permanent block (SSRN HTTP 403). No unsealed confirmatory window remains; no admissible unauthenticated new liquidation source; no new confirmatory experiment feasible on current data (RESEARCH_PROMPT.md §16). No new research; no re-open sealed outcomes; no re-pre-register; no new tracks.
**BRANCH/HEAD:** main @ 78ab2a3d (checkpoint); working tree clean except the intended AGENT_HANDOFF.md update (this session's durable-handoff deliverable); no __pycache__ noise, no stray artifacts
**HANDOFF ID:** FCLR-HANDOFF-052-20261101T191429Z
**SUPERSEDES:** FCLR-HANDOFF-051-20261101T183412Z
**PRIORITIZATION RATIONALE:** All gates resolved and sealed. FCLR-010 PASSED (C2 vs B1 −0.003077, 95% CI [−0.004892,−0.001263], rel −2.21%, n=199, 5 blocks). H_COUPLED-001 ROBUST PASS (+4.61% rel Brier reduction, CI [0.002511,0.003158], >=2000 reps). FCLR-OVERLAY-001 EXECUTED (exp-weighted event exposure reduction 43.985%, 95% CI [42.983%, 44.909%], 500 block reps, hypothetical only). H001 NOT_SUPPORTED; overlay INELIGIBLE; frontier fully terminal; no open experiment.

**STATUS:** Tests 27/27 PASS. Working tree clean. All artifacts present and sealed. PROJECT TERMINAL — no further research action required except the final reproducibility & archival focus campaign below.

## BOTTLENECKS REMOVED (THIS SESSION)
- `research_state/evaluation_summary_conflict.md` ambiguity: resolved as a documentation bottleneck, NOT by recomputation (no sealed holdout re-opened). The two conflicting pilot files (`evaluation_summary.md`, `evaluation_summary_FCLR002.md`) are annotated UNTRUSTED/SUPERSEDED; the canonical confirmatory numbers are `research_state/evaluation_summary_FCLR003.md` per `research_state/final_confirmatory_verdict.md`. No recomputation performed because it would require opening/altering the sealed holdout or an unpre-registered configuration (both prohibited).
- Working-tree `__pycache__` noise (non-functional, from test runs): restored to HEAD; tree now clean.
- `run_manifest.json.bak_fclr001`: stale tracked backup left in place (annotated superseded/stale in this handoff); not a blocker to progress.

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T19:14:29Z
**PRIORITY: P0 | TYPE: TERMINAL-ARCHIVAL-VERIFY | FOCUS CAMPAIGN: FCLR-ARCHIVE-001 FINAL REPRODUCIBILITY & ARCHIVAL | BLOCK ALL NEW RESEARCH | NO RE-OPENING SEALED OUTCOMES | NO NEW PRE-REGISTRATIONS | NO CROSS-TRACK MERGE | NO THRESHOLD SHOPPING**

**MANDATE:** Execute the final reproducibility & archival focus campaign (FCLR-ARCHIVE-001), then stop. The research program is terminal (H001 NOT_SUPPORTED; forecast gate NOT_MET; overlay INELIGIBLE). No new experiment, no holdout re-inspection, no threshold tuning, no new pre-registration. The only remaining heavy work is independent verification from stored input hashes plus archival cleanup; the future agent must not skip this verification.

**FOCUS CAMPAIGN FCLR-ARCHIVE-001 (FINAL REPRODUCIBILITY & ARCHIVAL) — EXECUTE IN ORDER:**
1. Independent recomputation of canonical confirmatory results (FCLR-003) from stored input hashes: `FCLR_EXPERIMENT=FCLR-003 timeout 1800 python scripts/run_evaluation.py`; compare headline QLIKE table and paired contrasts to `research_state/evaluation_summary_FCLR003.md` and `research_state/final_confirmatory_verdict.md` (must match within declared numerical tolerance). This verifies the terminal verdict independently — it does NOT re-open or re-tune the holdout.
2. Verify all sealed artifacts present and intact: `research_state/evaluation_summary_FCLR010.md`, `research_state/evaluation_summary_tracka_overlay_001.md`, `research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/final_confirmatory_verdict.md`, `research_state/pre_registration_tracka_overlay_*.md`, `research_state/research_protocol_fclr010.md`, `research_state/run_manifest.json`, `research_state/sealed_holdout_integrity.md`, `research_state/experiment_frontier.json`.
3. Verify `research_state/experiment_frontier.json` shows every campaign terminal (no unblocked/unfinished research task); frontier has no open experiment.
4. Verify cross-track firewall intact (only ironflow Hyperliquid for Track A; NO Binance merge; Modeled != Observed; overlay hypothetical only, no profitability claim).
5. Confirm `research_state/evaluation_summary_conflict.md` states both conflicting pilot files UNTRUSTED/SUPERSEDED and cites the canonical verdict; do NOT recompute them.
6. Confirm tests `python -m unittest discover -s tests -v` pass 27/27.
7. Confirm working tree clean (`git status --short` empty).
8. Record the final archival result (what changed/why, exact commands + outputs, evidence paths, gate states) in this AGENT_HANDOFF.md and then STOP — project complete.

**VERIFY IN ORDER (MANDATORY):**
```bash
git -C <repo> log --oneline -1
git -C <repo> status --short   # only AGENT_HANDOFF.md modified (intended deliverable); no __pycache__/noise
FCLR_EXPERIMENT=FCLR-003 timeout 1800 python scripts/run_evaluation.py   # independent recompute; diff vs canonical evaluation_summary_FCLR003.md / final_confirmatory_verdict.md
python -m unittest discover -s tests -v 2>&1 | tail -1   # 27/27 PASS
test -f research_state/evaluation_summary_FCLR003.md && echo "FCLR-003 OK"
test -f research_state/final_confirmatory_verdict.md && echo "VERDICT OK"
test -f research_state/evaluation_summary_FCLR010.md && echo "FCLR-010 OK"
test -f research_state/evaluation_summary_tracka_overlay_001.md && echo "OVERLAY OK"
test -f research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md && echo "COUPLED-ROBUST OK"
test -f research_state/sealed_holdout_integrity.md && echo "HOLDOUT-INTEGRITY OK"
grep -nE "H001.*NOT_SUPPORTED|FORECAST_GATE.*NOT_MET|overlay.*INELIGIBLE|PROJECT TERMINAL" research_state/final_confirmatory_verdict.md AGENT_HANDOFF.md | head
```

## HARD CONSTRAINTS (NON-NEGOTIABLE)
- Cross-track firewall: ONLY ironflow Hyperliquid for Track A. NO Binance merge. Modeled != observed.
- Frozen splits only. No re-splitting, no threshold tuning on test, no re-inspecting sealed FCLR-010/FCLR-003 outcomes.
- All 27 tests MUST remain PASS.
- Do not rerun Track C/B/H002 or any closed campaign.
- No .github/workflows/* changes. No activity commits.
- Overlay is hypothetical only - no live/paper trading. Explicit "no profitability claim".
- No new pre-registrations or experiment IDs; frontier is terminal. FCLR-ARCHIVE-001 is verification/archival only, not research.
- Independent recompute (step 1) must not alter any frozen artifact, split, or holdout; it only reads stored hashes and recomputes for comparison.

## REQUIRED END-OF-SESSION OUTPUT
1. What changed and why (concrete files/lines)
2. Exact tests run + results
3. Evidence added (paths to sealed evaluation summaries)
4. Gate states: FCLR-010 PASSED (numbers), H_COUPLED-001 ROBUST PASS (numbers), FCLR-OVERLAY-001 EXECUTED (metrics/CIs/gates), H001 NOT_SUPPORTED / forecast gate NOT_MET (numbers), overlay INELIGIBLE
5. Single highest-value next task (verification/archival only — no research work)
6. Precise verify command
7. Blockers or proof of exhaustive search (all tracks terminal; H002 permanent block documented; no admissible new source)

## SINGLE HIGHEST-VALUE NEXT TASK (EXECUTABLE NOW — VERIFICATION/ARCHIVAL ONLY)
**Task:** FCLR-ARCHIVE-001 — independently recompute canonical FCLR-003 confirmatory results from stored input hashes, verify all sealed artifacts present, confirm conflict annotated SUPERSEDED, confirm tree clean + 27/27 tests pass, record archival result, then stop — project complete.

**Verify:**
```bash
git -C <repo> log --oneline -1
git -C <repo> status --short   # only AGENT_HANDOFF.md modified (intended deliverable)
FCLR_EXPERIMENT=FCLR-003 timeout 1800 python scripts/run_evaluation.py
python -m unittest discover -s tests -v 2>&1 | tail -1
test -f research_state/evaluation_summary_FCLR003.md && echo "CANONICAL OK"
grep -n "NOT_SUPPORTED\|NOT_MET\|INELIGIBLE" research_state/final_confirmatory_verdict.md | head -5
```
