# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-27T20:00:08Z
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Default branch: main
Current HEAD: 5d26bd00 (chore(kilo): checkpoint agent session — handoff HEAD field was stale at 23c09954; corrected to actual repository HEAD)

## Mission (unchanged)

Read and follow RESEARCH_PROMPT.md. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes.

No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify .github/workflows without explicit maintainer authorization.

## Prior agent task — COMPLETED (this session)

Task: Read the prior agent task from the durable handoff and complete it. Then update the handoff and write a clear initial task message for the next agent.

Completion summary:
- Prior agent task verified complete: re-read AGENT_HANDOFF.md; confirmed tests `python3 -m pytest tests/ -q` — 25 passed, no frozen artifacts modified; tracked tree clean except untracked `__pycache__` under `scripts/`, `tests/`.
- Corrected stale handoff HEAD field: was `23c09954`, actual repository HEAD is `5d26bd00` (one newer checkpoint commit not reflected in the prior handoff). No substantive code changes between `23c09954` and `5d26bd00` beyond AGENT_HANDOFF.md metadata.
- Handoff task complete; initial task message for the next agent recorded below.

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
- FCLR-002 coverage (independently re-verified): 5 instruments (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), 4392 common hourly timestamps, single contiguous window 2024-04-01T00:00:00Z..2024-09-30T23:00:00Z (~183 days). Sufficient in principle for >=3 non-overlapping 30-day blocks, but NOT executed and its holdout NOT opened.

## Initial task message for next agent

State: INCONCLUSIVE. Forecast gate NOT_MET (PILOT/INCONCLUSIVE). Risk-overlay phase INELIGIBLE. Track A BLOCKED — no complete unauthenticated public liquidation census found; documented in `research_state/liquidation_sources_enumeration.md`. FCLR-001 frozen (BTCUSDT-only panel per coverage recheck; sealed holdout NOT reused/retrained/re-evaluated; OOS window and splits must NOT change). FCLR-H003 pre-registered in `research_state/fclr_h003_pre_registration.md` and executed on the frozen test block; results in `research_state/evaluation_summary_h003.md` — synthetic modeled boundary breaches only, no risk-overlay implications. Evaluation summaries reconciled canonically; headline C2 vs B1 on FCLR-001 is -2.50% relative with CI crossing zero; forecast gate NOT_MET either way. FCLR-002 coverage sufficient in principle (5 symbols, 4392 common hourly timestamps, 2024-04-01T00:00:00Z..2024-09-30T23:00:00Z, ~183 days) but NOT executed and NOT authorized unless explicitly requested with pre-registered FCLR-002 v1.0 (splits + acceptance criteria BEFORE outcomes) and an adversarial leakage audit before opening its holdout (rank 5). Verified this session: HEAD 5d26bd00 (prior handoff claimed 23c09954 — stale by one checkpoint commit; corrected), tracked tree clean except untracked `__pycache__` under `scripts/`, `tests/`; `python3 -m pytest tests/ -q` — 25 passed, no frozen artifacts modified.

Authorized next work: if FCLR-002 is explicitly requested, pre-register FCLR-002 v1.0 with splits and acceptance criteria BEFORE computing any outcomes, then run walk-forward evaluation on the 2024-04..2024-09 panel and an adversarial leakage audit before opening its holdout. Otherwise no new runs are authorized — document/clarify only without touching splits, protocol, evaluation logic, or reported results; never claim unexecuted runs succeeded. Leave risk-overlay INELIGIBLE.

Acceptance: state remains inconclusive with gates documented; no holdout leakage; all tests pass (25/25); no new results from the sealed holdout; HEAD unchanged except authorized checkpoint/documentation commits. Blocker evidence: Track A enumeration complete across Binance/Bybit/OKX/Deribit/academic/vendors — no materially different free route remains.
