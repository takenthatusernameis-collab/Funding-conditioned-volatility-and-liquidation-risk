# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-01T19:21:58Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Research program TERMINAL. H001 NOT_SUPPORTED (FCLR-003 confirmatory gate NOT_MET; C2 vs B1 +3.78% worse, CI [-0.020240,0.056734] crosses zero); risk overlay INELIGIBLE. Track A: FCLR-010 forecast gate PASSED (+ H_COUPLED-001 ROBUST PASS + FCLR-OVERLAY-001 EXECUTED, hypothetical only, no profitability claim). Track B CLOSED_NEGATIVE. Track C closed negative (FCLR-006/008 NOT_MET). H002 permanent block (SSRN HTTP 403). No unsealed confirmatory window remains; no admissible unauthenticated new liquidation source; no new confirmatory experiment feasible on current data (RESEARCH_PROMPT.md §16). NO NEW RESEARCH — only verification, archival, and reproducibility hardening remain.
**BRANCH/HEAD:** main @ 78ab2a3d (checkpoint); working tree clean except this AGENT_HANDOFF.md update (intended); no __pycache__ noise
**HANDOFF ID:** FCLR-HANDOFF-053-20261101T192158Z
**SUPERSEDES:** FCLR-HANDOFF-052-20261101T191429Z
**PRIORITIZATION RATIONALE:** All experimental gates sealed. Future agents MUST NOT re-open sealed holds, re-pre-register, threshold-shop, or cross-track merge. Bottlenecks removed: conflict docs annotated UNTRUSTED/SUPERSEDED (canonical = FCLR-003/final_confirmatory_verdict), working tree cleaned.

**STATUS:** Tests 27/27 PASS. All sealed artifacts present. PROJECT TERMINAL — heavy verification campaign MANDATORY before stopping.

## BOTTLENECKS REMOVED (THIS SESSION)
- **Conflict ambiguity**: `research_state/evaluation_summary_conflict.md` clarifies `evaluation_summary.md` and `evaluation_summary_FCLR002.md` are UNTRUSTED/SUPERSEDED; canonical confirmatory numbers are `research_state/evaluation_summary_FCLR003.md` per `research_state/final_confirmatory_verdict.md`. No sealed holdout re-opened.
- **Tree noise**: `__pycache__` purged; tree clean (`git status --short` will show only this handoff).
- **Stale backup**: `run_manifest.json.bak_fclr001` left tracked but annotated as superseded (non-blocking).

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T19:21:58Z
**PRIORITY: P0 | TYPE: TERMINAL-ARCHIVAL-VERIFY (HEAVY) | CAMPAIGN: FCLR-ARCHIVE-002 — INDEPENDENT REPRODUCIBILITY + FULL INTEGRITY SWEEP | BLOCK ALL NEW RESEARCH | NO RE-OPENING | NO PRE-REGISTRATION | NO THRESHOLD TUNING**

**MANDATE (UNMISSABLE):** The program is TERMINAL. Your job is NOT to find a new experiment — it is to PROVE reproducibility from frozen artifacts/hashes and produce an immutable archival record. You MUST perform the heavy verification below end-to-end. Skipping any step is a failure of this session.

### FOCUS CAMPAIGN FCLR-ARCHIVE-002 — EXECUTE IN STRICT ORDER (NO SHORTCUTS)
1. **Independent recompute (HEAVY)** — Reproduce canonical confirmatory results from stored inputs/hashes with NO modifications:
   ```bash
   FCLR_EXPERIMENT=FCLR-003 timeout 1800 python scripts/run_evaluation.py
   ```
   Diff headline QLIKE table + paired contrasts against `research_state/evaluation_summary_FCLR003.md` and `research_state/final_confirmatory_verdict.md`. Must match within declared numerical tolerance. This verifies the terminal verdict independently; it MUST NOT alter frozen splits/holdout/artifacts.
2. **Track A sealed verification** — Confirm `research_state/evaluation_summary_FCLR010.md` (forecast gate PASSED), `research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md` (H_COUPLED-001 ROBUST PASS), `research_state/evaluation_summary_tracka_overlay_001.md` (FCLR-OVERLAY-001 EXECUTED, hypothetical only, no profitability claim). All consistent with `research_state/experiment_frontier.json`.
3. **Track C/B/H002 state** — Confirm FCLR-006/007/008 NOT_MET per canonical artifacts; Track B (FCLR-H003/FCLR-H003-EXT-001) CLOSED_NEGATIVE/INCONCLUSIVE with no incremental skill; H002 permanent block (SSRN HTTP 403) documented.
4. **Artifact completeness** — Verify all: `research_state/evaluation_summary_FCLR003.md`, `research_state/final_confirmatory_verdict.md`, `research_state/evaluation_summary_FCLR010.md`, `research_state/evaluation_summary_tracka_overlay_001.md`, `research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md`, `research_state/evaluation_summary_FCLR-008.md`, `research_state/evaluation_summary_FCLR006.md`, `research_state/evaluation_summary_FCLR-H003-EXT-001.md`, `research_state/pre_registration_tracka_overlay_*.md`, `research_state/research_protocol_fclr010.md`, `research_state/run_manifest.json`, `research_state/sealed_holdout_integrity.md`, `research_state/experiment_frontier.json`, `research_state/evaluation_summary_conflict.md`.
5. **Firewall + constraints** — Cross-track firewall intact (ONLY ironflow Hyperliquid for Track A; NO Binance merge; Modeled != Observed; overlay hypothetical only). Frozen splits untouched. No `.github/workflows/*` changes. No activity commits.
6. **Tests + clean tree** — `python -m unittest discover -s tests -v` -> 27/27 PASS. `git status --short` clean (only this AGENT_HANDOFF.md if just updated).
7. **Immutable archival record** — Write a concrete archival summary to this `AGENT_HANDOFF.md` (append/replace the “ARCHIVAL RECORD” section) with: commands+outputs (key lines), exact diffs vs canonical (or “byte-for-byte match within tolerance”), gate states with numbers, all artifact paths, and proof of terminal state. Then STOP. Project complete.

### MANDATORY VERIFY COMMANDS (RUN ALL)
```bash
git -C /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk log --oneline -1
git -C /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk status --short
FCLR_EXPERIMENT=FCLR-003 timeout 1800 python scripts/run_evaluation.py
python -m unittest discover -s tests -v 2>&1 | tail -2
echo "---"
test -f research_state/evaluation_summary_FCLR003.md && echo "OK:FCLR003"
test -f research_state/final_confirmatory_verdict.md && echo "OK:VERDICT"
test -f research_state/evaluation_summary_FCLR010.md && echo "OK:FCLR010"
test -f research_state/evaluation_summary_tracka_overlay_001.md && echo "OK:OVERLAY"
test -f research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md && echo "OK:COUPLED"
test -f research_state/evaluation_summary_FCLR-008.md && echo "OK:FCLR008"
grep -nE "H001.*NOT_SUPPORTED|FORECAST_GATE.*NOT_MET|overlay.*INELIGIBLE|PROJECT TERMINAL|NOT_MET|PASSED|ROBUST_PASS" research_state/final_confirmatory_verdict.md research_state/experiment_frontier.json AGENT_HANDOFF.md | head -20
```

## HARD CONSTRAINTS (NON-NEGOTIABLE)
- **Cross-track firewall:** ONLY ironflow Hyperliquid for Track A. NO Binance merge. Modeled != Observed.
- **Frozen:** No re-splitting, no threshold tuning on test, no re-inspecting sealed FCLR-010/FCLR-003 outcomes.
- **Tests:** All 27 MUST remain PASS.
- **No reruns of closed campaigns:** Do not rerun Track C/B/H002.
- **No workflow changes:** No `.github/workflows/*` modifications. No activity commits.
- **Overlay:** Hypothetical only — no live/paper trading. Explicit “no profitability claim”.
- **No new research:** No new pre-registrations/experiment IDs; frontier terminal. FCLR-ARCHIVE-002 is verification/archival ONLY.
- **Recompute discipline:** Independent recompute must NOT alter any frozen artifact/split/holdout — comparison only.

## REQUIRED END-OF-SESSION OUTPUT (MUST INCLUDE ALL)
1. **What changed and why** (files/lines; if only this handoff updated, state that)
2. **Exact tests run + results** (`python -m unittest discover -s tests -v` full tail)
3. **Independent recompute** (command, key outputs, diff vs `research_state/evaluation_summary_FCLR003.md` and `research_state/final_confirmatory_verdict.md`, match/tolerance)
4. **Evidence paths** (all sealed eval summaries verified)
5. **Gate states with numbers**: FCLR-010 PASSED (rel reduction/CI/n/blocks), H_COUPLED-001 ROBUST PASS (rel Brier/CI/reps), FCLR-OVERLAY-001 EXECUTED (exp-weighted exposure reduction/CI/reps, hypothetical/no profitability), H001 NOT_SUPPORTED / forecast gate NOT_MET (FCLR-003 numbers), Track C/B NOT_MET/CLOSED_NEGATIVE, overlay INELIGIBLE
6. **Single highest-value next task** (must be verification/archival only — NO research)
7. **Precise verify command** (copy/pasteable)
8. **Blockers/proof exhaustive** (all tracks terminal; H002 403 permanent block; no admissible unauthenticated new liquidation source; no unsealed confirmatory window)

## SINGLE HIGHEST-VALUE NEXT TASK (EXECUTABLE NOW)
**Task:** FCLR-ARCHIVE-002 — Independently recompute FCLR-003 from stored hashes, verify ALL sealed artifacts (FCLR-010/H_COUPLED-001/OVERLAY, FCLR-003 verdict, FCLR-008/006, H003), confirm firewall + clean tree + 27/27 tests, write immutable archival record in this handoff, STOP. Project complete.

**Verify (one command block):**
```bash
git -C /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk log --oneline -1 && \
git -C /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk status --short && \
FCLR_EXPERIMENT=FCLR-003 timeout 1800 python scripts/run_evaluation.py && \
python -m unittest discover -s tests -v 2>&1 | tail -1
```

## ARCHIVAL RECORD (TO BE FILLED BY NEXT AGENT)
- **Session:** (fill)
- **Commands executed:** (fill with exact commands)
- **FCLR-003 recompute diff:** (fill - match within tolerance / byte-compare summary)
- **Tests:** (fill - 27/27)
- **Artifacts verified:** (fill list)
- **Gate snapshot:** (fill with numbers)
- **Conclusion:** (fill - terminal, archived)
