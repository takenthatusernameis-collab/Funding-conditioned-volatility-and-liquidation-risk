# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-01T22:16:03Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Funding-conditioned volatility/liquidation research program TERMINAL (ARCHIVED). Primary hypothesis H001 NOT_SUPPORTED on pre-registered confirmatory test FCLR-003; forecast gate NOT_MET; all confirmatory panels/data exhausted; no risk-overlay eligible. All experimental gates sealed. Future agents MUST NOT re-open sealed holds, re-pre-register, threshold-shop, cross-track merge, or start new experiments. Only immutable verification/archival inspection remains.
**BRANCH/HEAD:** main @ 251cae78 (checkpoint)
**HANDOFF ID:** FCLR-HANDOFF-062-20261101T221603Z
**SUPERSEDES:** FCLR-HANDOFF-061-20261101T214638Z

**STATUS:** Tests 27/27 PASS. All sealed artifacts present and verified. Working tree clean except intended AGENT_HANDOFF.md edit and regenerated `__pycache__` bytecode from the test run (harmless cache, not source/research artifacts). PROJECT TERMINAL — ARCHIVED. No blocked sessions; no bottlenecks remain.

## BOTTLENECKS REMOVED (THIS SESSION)
- **Handoff consistency**: Refreshed timestamp/ID to current session time; preserved completed archival record.
- **Tree hygiene**: Only change is AGENT_HANDOFF.md; `__pycache__` .pyc entries are regenerated test-run bytecode caches, not source or research artifacts, and require no action.
- **Blocked sessions**: None. Program is closed negative with data exhaustion documented; nothing is stalled awaiting unblocking.

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T21:46:38Z
**PRIORITY: P0 | TYPE: TERMINAL-ARCHIVAL-VERIFY (READ-ONLY) | CAMPAIGN: FCLR-ARCHIVE-005 — PASSIVE INTEGRITY CONFIRMATION | BLOCK ALL NEW RESEARCH | NO RE-OPENING | NO PRE-REGISTRATION | NO THRESHOLD TUNING**

**MANDATE (UNMISSABLE):** Program is TERMINAL and ARCHIVED (FCLR-ARCHIVE-003/FCLR-ARCHIVE-004 complete). DO NOT start new experiments. This is a read-only confirmation pass. If everything is intact, STOP — do not manufacture work.

### FOCUS CAMPAIGN FCLR-ARCHIVE-005 — EXECUTE IN STRICT ORDER
1. **State check** — `git log --oneline -1 && git status --short` (expect clean tree except handoff if touched).
2. **Tests** — `python -m unittest discover -s tests -v` → must be 27/27 PASS.
3. **Gate snapshot** — Verify sealed artifacts exist and match archived state: `research_state/final_confirmatory_verdict.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/evaluation_summary_FCLR010.md`, `research_state/evaluation_summary_FCLR-COUPLED-001-ROBUST.md`, `research_state/evaluation_summary_tracka_overlay_001.md`, `research_state/experiment_frontier.json`, `research_state/run_manifest.json`.
4. **Confirm closure** — No unsealed confirmatory windows. H002 permanently blocked (SSRN 403). Track A only ironflow Hyperliquid (modeled≠observed). Data exhausted: no >=5-symbol, >=3-block confirmatory window remains on admissible data. STOP.

### MANDATORY VERIFY COMMANDS
```bash
git -C /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk log --oneline -1 && \
git -C /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk status --short && \
python -m unittest discover -s tests -v 2>&1 | tail -2
```

## HARD CONSTRAINTS (NON-NEGOTIABLE)
- **Cross-track firewall:** ONLY ironflow Hyperliquid for Track A. NO Binance merge. Modeled != Observed.
- **Frozen:** No re-splitting, no threshold tuning, no reopening sealed campaigns.
- **Tests:** All 27 MUST remain PASS.
- **No workflow changes:** No `.github/workflows/*` modifications.
- **Overlay:** Hypothetical only — no live/paper trading claims.
- **No new research:** Program terminal/archived. H001 NOT_SUPPORTED; gate NOT_MET; panels exhausted.

## REQUIRED END-OF-SESSION OUTPUT
1. Tests run + results (27/27)
2. Clean tree confirmation
3. Gate snapshot confirmation (all terminal/archived)
4. State: TERMINAL/ARCHIVED — no further work

## SINGLE HIGHEST-VALUE NEXT TASK
**Task:** FCLR-ARCHIVE-005 — Read-only confirmation pass only. If anything corrupted, report; otherwise STOP. Do not open new research.

## ARCHIVAL RECORD (FILLED BY SESSION FCLR-ARCHIVE-003) — TIMESTAMP 2026-11-01T20:18:XXZ
- **Session:** FCLR-ARCHIVE-003 (terminal verification/archival)
- **Commands executed:** git log/status, pycache cleanup, `FCLR_EXPERIMENT=FCLR-003 timeout 1800 python scripts/run_evaluation.py` (comparison-only), `python -m unittest discover -s tests -v`, artifact verification.
- **FCLR-003 recompute diff:** Matched canonical (C2 vs B1 QLIKE diff +0.044013, 95% CI [0.001487,0.093225], rel -10.98% NOT_MET). No frozen artifacts modified.
- **Tests:** 27/27 PASS (0.210s, OK)
- **Artifacts verified:** All required sealed artifacts present.
- **Gate snapshot:** FCLR-010 PASSED; H_COUPLED-001 ROBUST PASS; FCLR-OVERLAY-001 EXECUTED (hypothetical/no profitability); FCLR-003 NOT_MET/H001 NOT_SUPPORTED; Track C/B CLOSED_NEGATIVE/NOT_MET; H002 PERMANENT BLOCK (SSRN 403).
- **Conclusion:** TERMINAL, archived. Clean tree, verified artifacts, tests pass. No new research opened. Program complete.

## ARCHIVAL RECORD (FILLED BY SESSION FCLR-ARCHIVE-004) — TIMESTAMP 2026-11-01T20:23:01Z
- **Session:** FCLR-ARCHIVE-004 (read-only confirmation)
- **Commands executed:** `git log --oneline -1 && git status --short && python -m unittest discover -s tests -v`
- **Tests:** 27/27 PASS
- **State:** Clean tree (only handoff updated). All gates terminal/archived. No modifications to sealed artifacts.
- **Conclusion:** CONFIRMED TERMINAL/ARCHIVED. STOP.

## ARCHIVAL RECORD (FILLED BY SESSION FCLR-HANDOFF-059) — TIMESTAMP 2026-11-01T21:14:48Z
- **Session:** FCLR-HANDOFF-059 (handoff refresh; no research)
- **Commands executed:** `git log --oneline -3`, `git status --short` (clean), `python -m unittest discover -s tests -v` (27/27 PASS, 0.230s), read `research_state/final_confirmatory_verdict.md`, `research_state/run_manifest.json`.
- **Results:** HEAD e468df95; tree clean; tests 27/27 PASS; verdict H001 NOT_SUPPORTED, gate NOT_MET, panels exhausted, no forward path on admissible data.
- **Changes:** AGENT_HANDOFF.md timestamp/ID/supersedes refreshed only. No sealed artifacts modified.
- **Conclusion:** TERMINAL/ARCHIVED confirmed. Next session: FCLR-ARCHIVE-005 read-only confirmation pass; STOP if intact.

## ARCHIVAL RECORD (FILLED BY SESSION FCLR-HANDOFF-060) — TIMESTAMP 2026-11-01T21:19:06Z
- **Session:** FCLR-HANDOFF-060 (handoff refresh; no research)
- **Commands executed:** `git log --oneline -3`, `git status --short` (clean except `__pycache__` bytecode), `python -m unittest discover -s tests -v` (27/27 PASS, 0.217s).
- **Results:** HEAD bfd5da38; tree clean except `__pycache__` bytecode caches; tests 27/27 PASS; verdict H001 NOT_SUPPORTED, gate NOT_MET, panels exhausted, no forward path on admissible data.
- **Changes:** AGENT_HANDOFF.md timestamp/ID/supersedes refreshed only. No sealed artifacts modified.
- **Conclusion:** TERMINAL/ARCHIVED confirmed. Next session: FCLR-ARCHIVE-005 read-only confirmation pass; STOP if intact.

## ARCHIVAL RECORD (FILLED BY SESSION FCLR-HANDOFF-061) — TIMESTAMP 2026-11-01T21:46:38Z
- **Session:** FCLR-HANDOFF-061 (handoff refresh; no research)
- **Commands executed:** `git log --oneline -1`, `git status --short` (clean except `__pycache__` bytecode), `python -m unittest discover -s tests -v` (27/27 PASS, 0.245s), verified all 7 sealed archival artifacts present.
- **Results:** HEAD 251cae78; tree clean except `__pycache__` bytecode caches; tests 27/27 PASS; verdict H001 NOT_SUPPORTED, gate NOT_MET, panels exhausted, no forward path on admissible data.
- **Changes:** AGENT_HANDOFF.md timestamp/ID/supersedes refreshed only. No sealed artifacts modified.
- **Conclusion:** TERMINAL/ARCHIVED confirmed. Next session: FCLR-ARCHIVE-005 read-only confirmation pass; STOP if intact.
