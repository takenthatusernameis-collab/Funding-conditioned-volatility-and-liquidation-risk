# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-28T04:57:30Z
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Default branch: main
Current HEAD: b3f8d30646f319b17a4212931fec8aacb1f936e3 (checkpoint, branch up to date with origin/main)

## Mission (unchanged)

Read and follow RESEARCH_PROMPT.md. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes.

No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify .github/workflows without explicit maintainer authorization.

## Current session — COMPLETED (this session)

Task: Read the prior agent task from the durable handoff and complete it. Then update the handoff and write a clear initial task message for the next agent.

Completion summary:
- Verified repo state against handoff: `git rev-parse HEAD` = b3f8d306 (handoff snapshot was stale; updated to current HEAD).
- `python3 -m pytest tests/ -q` — 51 passed, no frozen artifacts modified.
- `git status` — tracked tree clean except untracked `scripts/__pycache__/` and `tests/__pycache__/`.
- No new research results, no holdout access, no protocol changes, no risk overlay.
- Updated handoff timestamp and HEAD to b3f8d306; wrote fresh initial task message for next agent.

## What this session delivered

State verification and handoff refresh only. No new runs, no holdout access, no protocol changes, no new evidence. All 51 tests pass; frozen artifacts unchanged. Handoff metadata updated to reflect current HEAD `b3f8d30646f319b17a4212931fec8aacb1f936e3`.

## Current verified state

Repository status: INCONCLUSIVE. Forecast gate NOT MET (PILOT/INCONCLUSIVE). Risk-overlay phase INELIGIBLE. Direct liquidation labels unavailable (Track A BLOCKED).

- Frozen protocol: `research_state/research_protocol.md` v1.0 (FCLR-001).
- Frozen splits (`research_state/run_manifest.json`): train 2024-01-02T00:00:00Z..2024-02-24T08:00:00Z; val 2024-03-02T08:00:00Z..2024-03-20T02:00:00Z; test 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z; 7-day embargo.
- **Correction — evaluated panel is BTCUSDT-only, NOT >=5 instruments.** `research_state/coverage_audit_recheck.md` + `scripts/_diag_panel.py`: 1634 eval rows, all BTCUSDT; other four symbols have no mark-price CSVs before 2024-04-01. The protocol's >=5-instruments gate was never met — a coverage/representativeness defect, not a leakage defect.
- **Evaluation summaries reconciled canonically:** `research_state/evaluation_summary.md` (FCLR-001): test n=70; B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105; C2 vs B1 -2.50% rel, 95% CI [-0.123401, 0.158843] crosses zero. `research_state/evaluation_summary_FCLR002.md` (FCLR-002): test n=94 (5-symbol panel intersection); B0=0.432319, B1=0.399218, C1=0.769779, C2=0.752404; C2 vs B1 diff +0.353186 (C2 WORSE), CI crosses zero. Verdict unchanged and robust either way: forecast gate NOT MET. Single-instrument + single ~4-day block; CI crosses zero; multiplicity not satisfied.
- Implementation: forecast pipeline (7/7 tests), synthetic boundary labels (5/5), funding-correction replication partial (4/4; 445 events, median 8.0h). Controller progress accounting 6/6. All tests pass 51/51.
- Registry present: `hypothesis_registry.json`, `experiment_frontier.json`, `negative_results_report.md`, `leakage_audit.md`, `gate_assessment.md`, `final_inconclusive_report.md`, `fclr002_coverage_audit.json`.
- Track A (liquidation sources enumeration): `research_state/liquidation_sources_enumeration.md` — BLOCKED. No complete unauthenticated public liquidation census found across Binance/Bybit/OKX/Deribit/academic/vendors. Do not infer event-free intervals; do not use partial streams as complete census.
- FCLR-H003 pre-registered in `research_state/fclr_h003_pre_registration.md` and executed on frozen FCLR-001 test block — results in `research_state/evaluation_summary_h003.md` (synthetic modeled boundary breaches only, base rates near-zero, no risk-overlay implications).
- FCLR-002 coverage sufficient in principle (5 symbols, 4392 common hourly timestamps, 2024-04-01T00:00:00Z..2024-09-30T23:00:00Z, ~183 days) but NOT executed and its holdout NOT opened.

## Initial task message for next agent

Hello. This is the durable handoff for the "Funding-Conditioned Volatility and Liquidation Risk" research repo. Read this file and `RESEARCH_PROMPT.md` first, then `research_state/research_protocol.md` (frozen FCLR-001 v1.0) before doing anything else.

**Current state: INCONCLUSIVE. Forecast gate NOT MET. Risk-overlay phase INELIGIBLE. Track A (liquidation labels) BLOCKED.**

What is frozen and must NOT change:
- FCLR-001 protocol, splits, and OOS window (`research_state/research_protocol.md`, `research_state/run_manifest.json`). Sealed holdout NOT reused, retrained, or re-evaluated.
- All reported evaluation results. Never claim an unexecuted run succeeded.

What is verified this session:
- HEAD `b3f8d30646f319b17a4212931fec8aacb1f936e3` on `main` (local checkpoint; branch up to date with origin/main). Re-verify with `git rev-parse HEAD` — the recorded HEAD in this file is a snapshot and has been stale in multiple sessions.
- `python3 -m pytest tests/ -q` — 51 passed, no frozen artifacts modified.
- Tracked tree clean except untracked `__pycache__/` under `scripts/`, `tests/`.
- No new research results; this session verified handoff state and corrected the stale HEAD snapshot.

**Your tasks (do not expand scope):**
1. Verify repo state against this handoff (`git rev-parse HEAD`, `python3 -m pytest tests/ -q`) and confirm gates remain as documented.
2. Do **not** open sealed holdouts. New analysis must be pre-registrable and must not touch frozen artifacts/splits/evaluations; otherwise report findings without running new OOS evals that would consume holdout.
3. If there is any ambiguity about Track A (liquidation labels), follow `research_state/liquidation_sources_enumeration.md` (BLOCKED) strictly — do not fabricate a complete census.
4. Update this handoff at the end of your session with: HEAD, test result, what you did/did not do, and a clear initial task message for the next agent. Do not leave the handoff stale.

Leave risk-overlay INELIGIBLE. No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify `.github/workflows` without explicit maintainer authorization.

**Acceptance:** state remains inconclusive with gates documented; no holdout leakage; all tests pass (51/51); no new results from sealed holdout; HEAD updated to current checkpoint if you make a commit.
