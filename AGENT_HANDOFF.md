# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-29T15:51:17Z
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Default branch: main
Current HEAD (verified this session): `a40e0b5e7bc1c43f12494318b1c2d1c35a065e4f` on `main` (branch up to date with origin/main). Previous checkpoint `921cb8d0` was superseded by `a40e0b5` ("chore(kilo): checkpoint agent session"); working tree clean apart from untracked `__pycache__` under `scripts/` and `tests/`. No frozen-split/protocol/frozen-artifact changes this session.
Note: This session read the prior agent task from the durable handoff, verified the actual repo state against documented gates (FCLR-001/FCLR-002/Track A/FCLR-H003/H004), confirmed blockers remain, and refreshed the handoff for the next agent.

## Mission (unchanged)

Read and follow RESEARCH_PROMPT.md. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes.

No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify .github/workflows without explicit maintainer authorization.

## Current session — COMPLETED

Task: Read the prior agent task from the durable handoff and complete it. Then update the handoff and write a clear initial task message for the next agent.

Completion summary:
- Read prior handoff task from AGENT_HANDOFF.md (instructions for this session).
- Verified actual repo state: `git rev-parse HEAD` = `a40e0b5e7bc1c43f12494318b1c2d1c35a065e4f` on `main` (branch up to date with origin/main); `git status` clean apart from untracked `__pycache__` under `scripts/` and `tests/`. HEAD advanced from `921cb8d0` to `a40e0b5` ("chore(kilo): checkpoint agent session") since prior handoff. The only commit diff vs the documented checkpoint is the handoff file itself (`git diff --stat 921cb8d0 a40e0b5` → AGENT_HANDOFF.md).
- Re-confirmed gates from artifacts (all unchanged; no new evidence encountered):
  - FCLR-001 forecast gate NOT_MET (PILOT/INCONCLUSIVE; CI crosses zero, single ~4-day test block, BTCUSDT-only panel per `coverage_audit_recheck.md` — >=5 instruments gate NOT met). `research_state/evaluation_summary.md` flagged untrusted pending independent recomputation.
  - FCLR-002 gate NOT_MET / INCONCLUSIVE: primary contrast C2 vs B1 numerically passes (-9.28% relative QLIKE, 95% CI [-0.097648, -0.008788] excludes zero) and was independently reproduced byte-identical 2026-10-28 (`research_state/evaluation_summary_FCLR002_REPRO.md`, `scripts/_repro_run_evaluation.py`), BUT the minimum claim-worthy test (>=3 non-overlapping 30-day evaluation blocks across >=5 instruments) is NOT met — test window 2024-07-23..2024-09-30 = 70 days = only 2 non-overlapping 30-day blocks (+10-day remainder). Do NOT claim a verified FCLR-002 gate pass; do NOT recompute beyond the frozen repro already done; protocol §6/§9 holdout handling unchanged.
  - FCLR-H003 (hypothetical boundary-breach forecast): INCONCLUSIVE on both panels, no incremental skill over volatility-only baseline.
  - FCLR-H002 (Shek funding-correction replication): PARTIAL_REPLICATION — full paper methodology not independently reconstructible from public sources alone.
  - FCLR-H004 (observed liquidation outcomes): BLOCKED — direct liquidation labels unavailable from admissible public sources.
  - Risk-overlay phase INELIGIBLE (no forecast gate passes). Track A BLOCKED/NOT VIABLE (`research_state/liquidation_sources_enumeration.md`: no complete unauthenticated public liquidation census).
- Tests: `python3 -m pytest tests/ -q` — 51 passed in 1.11s (Python 3.12.3, /usr/bin/python3). Verified this session.
- No new experiments registered/executed. No holdout leakage for selection/tuning. No frozen artifacts/splits changed. No commit made (working-tree update only).
- Acknowledged all blockers. No valid next research step exists without touching frozen artifacts/splits/evaluations or opening sealed holdouts (both prohibited by protocol).
- Refreshed this handoff for current session state (HEAD `a40e0b5e7bc1c43f12494318b1c2d1c35a065e4f` on `main`; test result confirmed 51 passed in 1.11s; gates updated; next-agent task message written below).

## Current verified state

Repository status: INCONCLUSIVE. FCLR-001 forecast gate NOT_MET (PILOT/INCONCLUSIVE; single-instrument BTCUSDT panel, CI crosses zero). FCLR-002 gate NOT_MET / INCONCLUSIVE (numbers reproduced byte-identical; primary contrast numerically met and CI supports improvement, but >=3-block minimum-claim-worthy test NOT met). Risk-overlay phase INELIGIBLE. Track A (liquidation labels) BLOCKED/NOT VIABLE.

- Frozen protocol: `research_state/research_protocol.md` v1.0 (FCLR-001). FCLR-002 pre-registered v1.0 with frozen splits; holdout NOT opened per protocol §6/§9.
- Frozen splits FCLR-002: train 2024-04-01T00:00:00Z..2024-06-08T23:00:00Z; val 2024-06-16T00:00:00Z..2024-07-15T23:00:00Z; test 2024-07-23T00:00:00Z..2024-09-30T23:00:00Z; 7-day embargo. FCLR-001 window 2024-01-01..2024-03-31 (BTCUSDT-only mark-price coverage; other four symbols have zero mark-price rows there).
- Coverage: 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), 4392 common hourly timestamps for FCLR-002 panel (2024-04-01..2024-09-30). `research_state/fclr002_coverage_audit.json` present; FCLR-001 common-panel figure of 2136 timestamps in run_manifest.json is NOT reproducible from the current tree (`coverage_audit_recheck.md`).
- Evaluation summaries: `research_state/evaluation_summary.md` (FCLR-001) gate NOT_MET; `research_state/evaluation_summary_FCLR002.md` + `research_state/evaluation_summary_FCLR002_REPRO.md` (FCLR-002, byte-identical reproduction) — gate NOT_MET on block-count criterion; conflict documented in `evaluation_summary_conflict.md` (superseded in part by the byte-identical reproduction, but gate criteria still unmet).
- Implementation: tests exist and pass. `python3 -m pytest tests/ -q` → 51 passed, 1.11s this session.
- Track A: `research_state/liquidation_sources_enumeration.md` — NOT VIABLE/BLOCKED.
- Verified HEAD: `a40e0b5e7bc1c43f12494318b1c2d1c35a065e4f` on `main`.
- Tests: `python3 -m pytest tests/ -q` → 51 passed, 1.11s (Python 3.12.3, /usr/bin/python3).

## Initial task message for next agent

Hello. This is the durable handoff for the "Funding-Conditioned Volatility and Liquidation Risk" research repo. Read this file and `RESEARCH_PROMPT.md` first, then `research_state/research_protocol.md` (FCLR-001/FCLR-002) before doing anything else.

**Current state: INCONCLUSIVE. FCLR-001 forecast gate NOT MET (PILOT/INCONCLUSIVE). FCLR-002 gate NOT_MET / INCONCLUSIVE — primary contrast C2 vs B1 numerically passes (-9.28% relative QLIKE, 95% CI [-0.097648, -0.008788] excludes zero, independently reproduced byte-identical 2026-10-28) but the minimum claim-worthy test (>=3 non-overlapping 30-day evaluation blocks across >=5 instruments) is NOT met — test window 70 days = only 2 blocks. Do NOT claim a verified FCLR-002 gate pass. Risk-overlay phase INELIGIBLE. Track A (liquidation labels) BLOCKED/NOT VIABLE.**

IMPORTANT — FCLR-002: the conflicting evaluation summaries were independently reproduced byte-identical (`research_state/evaluation_summary_FCLR002_REPRO.md`, `scripts/_repro_run_evaluation.py`), so the numeric conflict is resolved, but the gate is still NOT_MET because the >=3 non-overlapping 30-day block requirement is not satisfied. Do not claim a verified pass. Do not recompute beyond the frozen repro already done (would require opening/altering the sealed holdout or unpre-registered configuration, both prohibited). Treat FCLR-002 as NOT_MET/INCONCLUSIVE.

Also note: `research_state/evaluation_summary.md` (FCLR-001) shows C2 vs B1 -2.50% with CI crossing zero and a single ~4-day test block; `research_state/gate_assessment.md` concludes NOT_MET/PILOT/INCONCLUSIVE. `research_state/coverage_audit_recheck.md` shows the FCLR-001 evaluated panel is BTCUSDT-only (1634 eval rows; ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT = 0), so the >=5-instruments gate was never met. None of these numbers are independently verified.

Hypothesis statuses (from `research_state/hypothesis_registry.json`):
- FCLR-H001 (incremental 24h volatility forecasting): INCONCLUSIVE — FCLR-001 gate NOT_MET.
- FCLR-H002 (Shek funding-correction replication): PARTIAL_REPLICATION.
- FCLR-H003 (hypothetical boundary-breach forecast): INCONCLUSIVE — no incremental skill on either panel.
- FCLR-H004 (observed liquidation outcomes): BLOCKED.

What is frozen and must NOT change:
- FCLR-001 protocol, splits, and OOS window. Sealed holdout NOT reused/retrained/re-evaluated.
- FCLR-002 pre-registered protocol/splits; holdout NOT opened; do not re-register or reuse FCLR-001 holdout.
- All reported evaluation results. Never claim an unexecuted run succeeded. Do not treat untrusted summaries as verified. FCLR-H003/H004 cells are untested/blocked — do not report them as completed or null.

Your tasks (do not expand scope):
1. Verify repo state: `git rev-parse HEAD` → `a40e0b5e7bc1c43f12494318b1c2d1c35a065e4f` (current on `main`); run `python3 -m pytest tests/ -q` (expect 51 passed; Python 3.12.3, /usr/bin/python3). Confirm gates remain as documented including the FCLR-002 NOT_MET/INCONCLUSIVE status.
2. Acknowledge blockers: FCLR-001 NOT_MET; FCLR-002 NOT_MET/INCONCLUSIVE (do not claim pass); risk-overlay INELIGIBLE; Track A BLOCKED/NOT VIABLE; FCLR-H003/H004 not claimable. Do NOT fabricate results, open sealed holdouts, or change frozen artifacts/splits/evaluations.
3. If and only if a genuinely new, pre-registrable analysis becomes possible without touching frozen artifacts, document it as a new pre-registration before execution. Otherwise state clearly that no valid next step exists and list concrete blockers.
4. Update this handoff at the end of your session with: HEAD, test result/environment note, what you did/did not do, and a clear initial task message for the next agent. Do not leave the handoff stale.

**No valid next step exists** under current constraints. Concrete blockers:
- Forecast gate FCLR-001 not met; risk-overlay ineligible until forecast gate passes (protocol constraint).
- FCLR-002 gate NOT_MET: >=3 non-overlapping 30-day block requirement not satisfied (only 2 blocks); holdout not opened and must not be reopened/recomputed per protocol §6/§9.
- Track A (liquidation labels) blocked/not viable - no complete unauthenticated public liquidation census found.
- All core artifacts (protocol, splits, evaluations) are frozen. No pre-registrable analysis path identified that avoids touching frozen artifacts or sealed holdouts.

Leave risk-overlay INELIGIBLE. No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify `.github/workflows` without explicit maintainer authorization.

**Acceptance:** state remains inconclusive with gates documented (FCLR-001 NOT_MET; FCLR-002 NOT_MET/INCONCLUSIVE — reproduced but block-count gate unmet); no holdout leakage; no fabricated results; verified HEAD `a40e0b5e7bc1c43f12494318b1c2d1c35a065e4f` on `main`; tests pass (51/51). `AGENT_HANDOFF.md` refreshed (working-tree update; no commit made — commit checkpoint only if explicitly requested).
