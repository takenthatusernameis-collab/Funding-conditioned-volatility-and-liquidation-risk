# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-29T10:53:00Z
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Default branch: main
Current HEAD (verified): `d451f4410a025b5ffa3b7288a274b2f869285446` on `main` (working tree clean apart from untracked pytest `__pycache__` cache dirs under scripts/ and tests/).
Note: New checkpoint commit `d451f441` ahead of previously recorded `a1a8310d`; no research/code/frozen-artifact changes in this session. Tests verified passing.

## Mission (unchanged)

Read and follow RESEARCH_PROMPT.md. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes.

No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify .github/workflows without explicit maintainer authorization.

## Current session — COMPLETED

Task: Read the prior agent task from the durable handoff and complete it. Then update the handoff and write a clear initial task message for the next agent.

Completion summary:
- Read prior handoff task from AGENT_HANDOFF.md. Verified current repo state at session start (HEAD `d451f441` on `main`; clean aside from untracked `__pycache__`, no research/code/frozen-artifact changes).
- Verified repo state: `git rev-parse HEAD` = `d451f4410a025b5ffa3b7288a274b2f869285446` on `main`; `git status` clean apart from untracked `__pycache__`; no code/data/frozen-artifact changes in this session.
- Re-confirmed gates from artifacts: FCLR-001 forecast gate NOT_MET (PILOT/INCONCLUSIVE; CI crosses zero, single ~4-day test block, BTCUSDT-only paired panel per `coverage_audit_recheck.md` — >=5 instruments gate NOT met). `research_state/evaluation_summary.md` flagged untrusted pending independent recomputation (`evaluation_summary_conflict.md`). FCLR-002 `research_state/evaluation_summary_FCLR002.md` flagged untrusted in `evaluation_summary_conflict.md` (heading/body mismatch, sign-convention artifacts, n=94 single-instrument BTCUSDT rows per `_diag_panel.py`); protocol §6/§9 holdout NOT opened / no outcomes computed; provenance not recorded. Do NOT claim verified FCLR-002 pass; do NOT recompute. Risk-overlay INELIGIBLE. Track A BLOCKED/NOT VIABLE (`research_state/liquidation_sources_enumeration.md`: no complete unauthenticated public liquidation census).
- Tests: `python3 -m pytest tests/ -q` — 51 passed in 1.04s.
- No new experiments registered/executed. No holdout leakage. No frozen artifacts/splits/evaluations changed.
- Acknowledged all blockers. No valid next research step exists without touching frozen artifacts/splits/evaluations or opening sealed holdouts (both prohibited by protocol).
- Updated this handoff for current session state (HEAD `d451f441` on `main`; test result confirmed; gates unchanged; next-agent task message written below).

## Current verified state

Repository status: INCONCLUSIVE. FCLR-001 forecast gate NOT_MET (PILOT/INCONCLUSIVE; single-instrument BTCUSDT panel, CI crosses zero). FCLR-002 gate CONFLICTED/UNTRUSTED — do NOT claim a verified pass. Risk-overlay phase INELIGIBLE. Track A (liquidation labels) BLOCKED/NOT VIABLE.

- Frozen protocol: `research_state/research_protocol.md` v1.0 (FCLR-001). FCLR-002 pre-registered v1.0 with frozen splits; holdout NOT opened per protocol §6/§9.
- Frozen splits FCLR-002: train 2024-04-01T00:00:00Z..2024-06-08T23:00:00Z; val 2024-06-16T00:00:00Z..2024-07-15T23:00:00Z; test 2024-07-23T00:00:00Z..2024-09-30T23:00:00Z; 7-day embargo. FCLR-001 window 2024-01-01..2024-03-31 (BTCUSDT-only mark-price coverage; other four symbols have zero mark-price rows there).
- Coverage: 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), 4392 common hourly timestamps for FCLR-002 panel (2024-04-01..2024-09-30). `research_state/fclr002_coverage_audit.json` present; FCLR-001 common-panel figure of 2136 timestamps in run_manifest.json is NOT reproducible from the current tree (`coverage_audit_recheck.md`).
- Evaluation summaries: `research_state/evaluation_summary.md` (FCLR-001) gate NOT_MET; `research_state/evaluation_summary_FCLR002.md` (FCLR-002) flagged untrusted in `evaluation_summary_conflict.md`; conflict documented there.
- Implementation: tests exist and pass. `python3 -m pytest tests/ -q` → 51 passed, 1.47s.
- Track A: `research_state/liquidation_sources_enumeration.md` — NOT VIABLE/BLOCKED.
- Verified HEAD: `d451f4410a025b5ffa3b7288a274b2f869285446` on `main` (checkpoint commit ahead; no research change).
- Tests: `python3 -m pytest tests/ -q` → 51 passed, 1.04s.

## Initial task message for next agent

Hello. This is the durable handoff for the "Funding-Conditioned Volatility and Liquidation Risk" research repo. Read this file and `RESEARCH_PROMPT.md` first, then `research_state/research_protocol.md` (FCLR-001/FCLR-002) before doing anything else.

**Current state: INCONCLUSIVE. FCLR-001 forecast gate NOT MET (PILOT/INCONCLUSIVE). FCLR-002 gate CONFLICTED/UNTRUSTED — do NOT claim a verified pass. Risk-overlay phase INELIGIBLE. Track A (liquidation labels) BLOCKED/NOT VIABLE.**

IMPORTANT — FCLR-002 conflict: `research_state/evaluation_summary_FCLR002.md` shows figures but `research_state/evaluation_summary_conflict.md` flags both evaluation summaries as untrusted until independently recomputed; protocol §6/§9 state the FCLR-002 holdout was NOT opened / no outcomes computed. Provenance not recorded. Do not claim a verified FCLR-002 gate pass. Do not recompute (would require opening/altering the sealed holdout or unpre-registered configuration, both prohibited). Treat FCLR-002 as unresolved/conflicted.

Also note: `research_state/evaluation_summary.md` (FCLR-001) shows C2 vs B1 -2.50% with CI crossing zero and a single ~4-day test block; `research_state/gate_assessment.md` concludes NOT_MET/PILOT/INCONCLUSIVE. `research_state/coverage_audit_recheck.md` shows the FCLR-001 evaluated panel is BTCUSDT-only (1634 eval rows; ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT = 0), so the >=5-instruments gate was never met. None of these numbers are independently verified.

What is frozen and must NOT change:
- FCLR-001 protocol, splits, and OOS window. Sealed holdout NOT reused/retrained/re-evaluated.
- FCLR-002 pre-registered protocol/splits; holdout NOT opened; do not re-register or reuse FCLR-001 holdout.
- All reported evaluation results. Never claim an unexecuted run succeeded. Do not treat untrusted summaries as verified.

Your tasks (do not expand scope):
1. Verify repo state: `git rev-parse HEAD` → `d451f4410a025b5ffa3b7288a274b2f869285446` (current on `main`); run `python3 -m pytest tests/ -q` (expect 51 passed). Confirm gates remain as documented including the FCLR-002 conflict.
2. Acknowledge blockers: FCLR-001 NOT_MET; FCLR-002 conflicted/untrusted (do not claim pass); risk-overlay INELIGIBLE; Track A BLOCKED/NOT VIABLE. Do NOT fabricate results, open sealed holdouts, or change frozen artifacts/splits/evaluations.
3. If and only if a genuinely new, pre-registrable analysis becomes possible without touching frozen artifacts, document it as a new pre-registration before execution. Otherwise state clearly that no valid next step exists and list concrete blockers.
4. Update this handoff at the end of your session with: HEAD, test result/environment note, what you did/did not do, and a clear initial task message for the next agent. Do not leave the handoff stale.

**No valid next step exists** under current constraints. Concrete blockers:
- Forecast gate FCLR-001 not met; risk-overlay ineligible until forecast gate passes (protocol constraint).
- FCLR-002 evaluation is conflicted/untrusted with no provenance; holdout not opened and must not be opened/recomputed per protocol §6/§9.
- Track A (liquidation labels) blocked/not viable - no complete unauthenticated public liquidation census found.
- All core artifacts (protocol, splits, evaluations) are frozen. No pre-registrable analysis path identified that avoids touching frozen artifacts or sealed holdouts.

Leave risk-overlay INELIGIBLE. No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify `.github/workflows` without explicit maintainer authorization.

**Acceptance:** state remains inconclusive with gates documented (FCLR-001 NOT_MET; FCLR-002 conflicted/untrusted); no holdout leakage; no fabricated results; verified HEAD `d451f4410a025b5ffa3b7288a274b2f869285446` on `main`; tests pass (51/51). `AGENT_HANDOFF.md` refreshed (working-tree update; no commit made — commit checkpoint only if explicitly requested).
