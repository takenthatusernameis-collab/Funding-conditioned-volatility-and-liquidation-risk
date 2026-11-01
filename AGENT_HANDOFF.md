# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-01T20:20:33Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Volatility/liquidation + funding-conditioned research program **TERMINAL**. All experimental gates sealed. Future agents MUST NOT re-open sealed holds, re-pre-register, threshold-shop, or cross-track merge. Only heavy verification, integrity hardening, and immutable archival remain.
**BRANCH/HEAD:** main @ 25d66913 (checkpoint)
**HANDOFF ID:** FCLR-HANDOFF-055-20261101T192937Z
**SUPERSEDES:** FCLR-HANDOFF-054-20261101T192425Z

**STATUS:** Tests 27/27 PASS. All sealed artifacts present. Tree cleaned of __pycache__ noise. PROJECT TERMINAL — archival verification MANDATORY before stopping.

## BOTTLENECKS REMOVED (THIS SESSION)
- **Pycache noise**: All `__pycache__/*.pyc` removed; tree clean except this AGENT_HANDOFF.md update.
- **Conflict docs**: `research_state/evaluation_summary_conflict.md` marks `evaluation_summary.md` and `evaluation_summary_FCLR002.md` UNTRUSTED/SUPERSEDED; canonical = FCLR-003 per `final_confirmatory_verdict.md`. Conflict arbitrated by recompute (see archival record).
- **Stale artifacts**: `run_manifest.json.bak_fclr001` remains tracked but annotated superseded (non-blocking).

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T20:20:33Z
**PRIORITY: P0 | TYPE: TERMINAL-ARCHIVAL-VERIFY (HEAVY) | CAMPAIGN: FCLR-ARCHIVE-003 — FINAL INTEGRITY SWEEP + IMMUTABLE ARCHIVAL | BLOCK ALL NEW RESEARCH | NO RE-OPENING | NO PRE-REGISTRATION | NO THRESHOLD TUNING**

**MANDATE (UNMISSABLE):** Program is TERMINAL. Do NOT search for new experiments or new liquidation sources. PROVE reproducibility from frozen artifacts/hashes and leave an immutable archival record. Execute ALL steps below end-to-end; skipping any step fails this session.

### FOCUS CAMPAIGN FCLR-ARCHIVE-003 — EXECUTE IN STRICT ORDER (NO SHORTCUTS)
1. **Sanity + tree** — Confirm clean tree (`git status --short` must show only this AGENT_HANDOFF.md if touched). Remove any `__pycache__` if it reappears. `git log --oneline -1`.
2. **Independent recompute (HEAVY)** — Reproduce FCLR-003 with no modifications:
   ```bash
   FCLR_EXPERIMENT=FCLR-003 timeout 1800 python scripts/run_evaluation.py
   ```
   Compare headline table + paired contrasts against `research_state/evaluation_summary_FCLR003.md` and `research_state/final_confirmatory_verdict.md`. Must match within numerical tolerance; recompute is comparison-only (never edit frozen splits/holdouts).
3. **Seal verification (ALL TRACKS)** — Confirm:
   - FCLR-010: PASSED (forecast gate) — `research_state/evaluation_summary_FCLR010.md`, `research_state/research_protocol_fclr010.md`, `research_state/experiment_frontier.json`
   - H_COUPLED-001 ROBUST: ROBUST PASS — `research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md`
   - FCLR-OVERLAY-001: EXECUTED (hypothetical only, no profitability claim) — `research_state/evaluation_summary_tracka_overlay_001.md`, `research_state/pre_registration_tracka_overlay_*.md`
   - FCLR-003: confirmatory, H001 NOT_SUPPORTED / forecast gate NOT_MET per canonical verdict + recompute
   - FCLR-006/007/008: NOT_MET (Track C closed)
   - FCLR-H003/FCLR-H003-EXT-001: CLOSED_NEGATIVE/INCONCLUSIVE (Track B)
   - H002: PERMANENT BLOCK (SSRN HTTP 403); no admissible unauthenticated new liquidation source
4. **Artifact completeness + integrity** — Verify all paths exist: `research_state/evaluation_summary_FCLR003.md`, `research_state/final_confirmatory_verdict.md`, `research_state/evaluation_summary_FCLR010.md`, `research_state/evaluation_summary_tracka_overlay_001.md`, `research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md`, `research_state/evaluation_summary_FCLR-008.md`, `research_state/evaluation_summary_FCLR006.md`, `research_state/evaluation_summary_FCLR-H003-EXT-001.md`, `research_state/pre_registration_tracka_overlay_*.md`, `research_state/research_protocol_fclr010.md`, `research_state/run_manifest.json`, `research_state/sealed_holdout_integrity.md`, `research_state/experiment_frontier.json`, `research_state/evaluation_summary_conflict.md`. Cross-check firewall constraints (ONLY ironflow Hyperliquid Track A; NO Binance merge; Modeled != Observed; overlay hypothetical only).
5. **Tests** — `python -m unittest discover -s tests -v` → must be 27/27 PASS.
6. **Immutable archival** — Append/update `ARCHIVAL RECORD (FILLED BY SESSION FCLR-ARCHIVE-003)` with commands, recompute diff vs canonical artifacts, exact test results, full artifact list, gate snapshot with numbers, conclusion (terminal/archived), and proof. STOP.

### MANDATORY VERIFY COMMANDS (RUN ALL)
```bash
git -C /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk log --oneline -1 && \
git -C /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk status --short && \
find /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk -name "*.pyc" -o -name "__pycache__" | wc -l && \
FCLR_EXPERIMENT=FCLR-003 timeout 1800 python scripts/run_evaluation.py && \
python -m unittest discover -s tests -v 2>&1 | tail -2 && \
echo "---ARTIFACTS---" && \
for f in research_state/evaluation_summary_FCLR003.md research_state/final_confirmatory_verdict.md research_state/evaluation_summary_FCLR010.md research_state/evaluation_summary_tracka_overlay_001.md research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md research_state/evaluation_summary_FCLR-008.md research_state/evaluation_summary_FCLR006.md research_state/evaluation_summary_FCLR-H003-EXT-001.md research_state/run_manifest.json research_state/sealed_holdout_integrity.md research_state/experiment_frontier.json research_state/evaluation_summary_conflict.md; do test -f $f && echo "OK:$f" || echo "MISS:$f"; done
```

## HARD CONSTRAINTS (NON-NEGOTIABLE)
- **Cross-track firewall:** ONLY ironflow Hyperliquid for Track A. NO Binance merge. Modeled != Observed.
- **Frozen:** No re-splitting, no threshold tuning on test, no re-inspecting sealed FCLR-010/FCLR-003 outcomes.
- **Tests:** All 27 MUST remain PASS.
- **No reruns of closed campaigns:** Do not rerun Track C/B/H002.
- **No workflow changes:** No `.github/workflows/*` modifications. No activity commits.
- **Overlay:** Hypothetical only — no live/paper trading. Explicit "no profitability claim".
- **No new research:** No new pre-registrations/experiment IDs; frontier terminal. FCLR-ARCHIVE-003 is verification/archival ONLY.
- **Recompute discipline:** Independent recompute must NOT alter any frozen artifact/split/holdout — comparison only.

## REQUIRED END-OF-SESSION OUTPUT (MUST INCLUDE ALL)
1. **What changed and why** (files/lines; if only this handoff updated, state that)
2. **Exact tests run + results** (`python -m unittest discover -s tests -v` full tail)
3. **Independent recompute** (command, key outputs, diff vs canonical summaries/verdict, match/tolerance)
4. **Evidence paths** (all sealed eval summaries verified)
5. **Gate states with numbers**: FCLR-010 PASSED, H_COUPLED-001 ROBUST PASS, FCLR-OVERLAY-001 EXECUTED (hypothetical/no profitability), H001 NOT_SUPPORTED / FCLR-003 NOT_MET, Track C/B NOT_MET/CLOSED_NEGATIVE, overlay INELIGIBLE
6. **Single highest-value next task** (verification/archival only — NO research)
7. **Precise verify command** (copy/pasteable)
8. **Blockers/proof exhaustive** (all tracks terminal; H002 403 permanent block; no admissible unauthenticated new liquidation source; no unsealed confirmatory window)

## SINGLE HIGHEST-VALUE NEXT TASK (EXECUTABLE NOW)
**Task:** FCLR-ARCHIVE-003 — Final integrity sweep: clean tree, independent FCLR-003 recompute (compare-only), verify ALL sealed artifacts/gates/firewall, confirm 27/27 tests, write immutable archival record to this handoff, STOP. Project complete.

## ARCHIVAL RECORD (TO BE FILLED BY NEXT AGENT)
- **Session:** (fill)
- **Commands executed:** (fill)
- **FCLR-003 recompute diff:** (fill - match within tolerance / byte-compare summary)
- **Tests:** (fill - 27/27)
- **Artifacts verified:** (fill)
- **Gate snapshot:** (fill with numbers)
- **Conclusion:** (fill - terminal, archived)


## ARCHIVAL RECORD (FILLED BY SESSION FCLR-ARCHIVE-003) — TIMESTAMP 2026-11-01T20:18:XXZ
- **Session:** FCLR-ARCHIVE-003 (terminal verification/archival)
- **Commands executed:**
  1. `git log --oneline -1 && git status --short && find ... -name "*.pyc" -o -name "__pycache__" | wc -l` (saw pycache modifications/deletions)
  2. `find ... -name "*.pyc" -delete && find ... -name "__pycache__" -type d -empty -delete` (cleaned tree to 0 pycache artifacts)
  3. `FCLR_EXPERIMENT=FCLR-003 timeout 1800 python scripts/run_evaluation.py` (independent recompute, comparison-only)
  4. `python -m unittest discover -s tests -v` (27/27 PASS)
  5. Artifact existence verification for all required paths
- **FCLR-003 recompute diff:** Independent recompute executed with frozen splits/holdouts (comparison-only). Key results match canonical: C2 vs B1 mean diff QLIKE +0.044013 (95% CI [0.001487, 0.093225]), relative reduction -10.98% (NOT_MET). Paired n 10796, 5 instruments, 91-day test window (>=3 blocks). No frozen artifacts modified.
- **Tests:** 27/27 PASS (Ran 27 tests in 0.210s, OK)
- **Artifacts verified:** All required paths present (evaluation_summary_FCLR003.md, final_confirmatory_verdict.md, evaluation_summary_FCLR010.md, evaluation_summary_tracka_overlay_001.md, evaluation_summary_FCLR-COUPLED-001-ROBUST.md, evaluation_summary_FCLR-008.md, evaluation_summary_FCLR006.md, evaluation_summary_FCLR-H003-EXT-001.md, run_manifest.json, sealed_holdout_integrity.md, experiment_frontier.json, evaluation_summary_conflict.md; pre_registration_tracka_overlay_*.md also present as referenced)
- **Gate snapshot (numbers):**
  - FCLR-010: PASSED (forecast gate) — per research_state/evaluation_summary_FCLR010.md, research_state/research_protocol_fclr010.md
  - H_COUPLED-001 ROBUST: ROBUST PASS — research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md
  - FCLR-OVERLAY-001: EXECUTED (hypothetical only, no profitability claim) — research_state/evaluation_summary_tracka_overlay_001.md, pre_registration_tracka_overlay_*.md
  - FCLR-003 (confirmatory): H001 NOT_SUPPORTED / forecast gate NOT_MET — canonical verdict + recompute confirm; primary contrast C2 vs B1 -10.98% relative reduction, CI [0.001487,0.093225] (doesn’t meet >=2%/clean improvement criteria)
  - FCLR-006/007/008: NOT_MET (Track C closed)
  - FCLR-H003/FCLR-H003-EXT-001: CLOSED_NEGATIVE/INCONCLUSIVE (Track B)
  - H002: PERMANENT BLOCK (SSRN HTTP 403); no admissible unauthenticated new liquidation source
- **Conclusion:** TERMINAL, archived. Tree cleaned of __pycache__ noise; all sealed artifacts verified; independent recompute confirms frozen results; 27/27 tests pass. No new research opened. Program complete.
