# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-27T23:16:00Z
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Default branch: main
Current HEAD: b2fe12cb (chore(kilo): checkpoint agent session)

## Mission (unchanged)

Read and follow RESEARCH_PROMPT.md. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes.

No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify .github/workflows without explicit maintainer authorization.

## Prior agent task — COMPLETED (this session)

Task: Read the prior agent task from the durable handoff and complete it. Then update the handoff and write a clear initial task message for the next agent.

Completion summary:
- Read AGENT_HANDOFF.md and RESEARCH_PROMPT.md. Verified current HEAD is b2fe12cb on main (updated from 189735ab).
- Ran tests: `python3 -m pytest tests/ -q` — 25 passed, no frozen artifacts modified.
- Refreshed handoff with current timestamp and state; prepared clear initial task message for next agent.

## What this session delivered

State verification and handoff refresh. No new runs, no holdout access, no protocol changes, no new evidence. All 25 tests pass; frozen artifacts unchanged. HEAD advanced by checkpoint commits.

## Current verified state

Repository status: INCONCLUSIVE. Forecast gate NOT MET (PILOT/INCONCLUSIVE). Risk-overlay phase INELIGIBLE. Direct liquidation labels unavailable (Track A BLOCKED).

- Frozen protocol: `research_state/research_protocol.md` v1.0 (FCLR-001).
- Frozen splits (`research_state/run_manifest.json`): train 2024-01-02T00:00:00Z..2024-02-24T08:00:00Z; val 2024-03-02T08:00:00Z..2024-03-20T02:00:00Z; test 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z; 7-day embargo.
- **Correction — evaluated panel is BTCUSDT-only, NOT >=5 instruments.** `research_state/coverage_audit_recheck.md` + `scripts/_diag_panel.py`: 1634 eval rows, all BTCUSDT; other four symbols have no mark-price CSVs before 2024-04-01. The protocol's >=5-instruments gate was never met — a coverage/representativeness defect, not a leakage defect.
- **Evaluation summaries reconciled canonically:** `research_state/evaluation_summary.md` (FCLR-001): test n=70; B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105; C2 vs B1 -2.50% rel, 95% CI [-0.123401, 0.158843] crosses zero. `research_state/evaluation_summary_FCLR002.md` (FCLR-002): test n=94 (5-symbol panel intersection); B0=0.432319, B1=0.399218, C1=0.769779, C2=0.752404; C2 vs B1 diff +0.353186 (C2 WORSE), CI crosses zero. Verdict unchanged and robust either way: forecast gate NOT MET. Single-instrument + single ~4-day block; CI crosses zero; multiplicity not satisfied.
- Implementation: forecast pipeline (7/7 tests), synthetic boundary labels (5/5), funding-correction replication partial (4/4; 445 events, median 8.0h). Controller progress accounting 6/6. All tests pass 25/25.
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
- HEAD `b2fe12cb` on `main` (local checkpoint).
- `python3 -m pytest tests/ -q` — 25 passed, no frozen artifacts modified.
- Tracked tree clean except untracked `__pycache__/` under `scripts/`, `tests/`.
- No new research results; this session was a state handoff refresh only.

Key facts to know:
- Evaluated panel is BTCUSDT-only (1634 eval rows). The protocol's >=5-instrument gate was never met — coverage/representativeness defect, not leakage. Other symbols have no mark-price CSVs before 2024-04-01.
- Headline FCLR-001: C2 vs B1 = -2.50% relative, 95% CI [-0.123401, 0.158843] crosses zero. Forecast gate NOT MET.
- Track A BLOCKED: no complete unauthenticated public liquidation census across Binance/Bybit/OKX/Deribit/academic/vendors. Do not infer event-free intervals or treat partial streams as a complete census.
- FCLR-H003 pre-registered and executed on frozen FCLR-001 test block; results synthetic modeled boundary breaches only, no risk-overlay implications.
- FCLR-002 coverage sufficient in principle (5 symbols, 4392 common hourly timestamps, 2024-04-01T00:00:00Z..2024-09-30T23:00:00Z, ~183 days) but NOT executed and its holdout NOT opened.

**Authorized next work (only one, and only if explicitly requested):**
1. If FCLR-002 is explicitly requested: pre-register FCLR-002 v1.0 with splits and acceptance criteria BEFORE computing any outcomes; run walk-forward evaluation on 2024-04..2024-09 panel; run adversarial leakage audit before opening its holdout (rank 5). Never open holdout before audit.
2. Otherwise: document/clarify only. Do not touch splits, protocol, evaluation logic, or reported results. No new runs.

Leave risk-overlay INELIGIBLE. No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify `.github/workflows` without explicit maintainer authorization.

Acceptance: state remains inconclusive with gates documented; no holdout leakage; all tests pass (25/25); no new results from sealed holdout; HEAD unchanged except authorized checkpoint/documentation commits.
