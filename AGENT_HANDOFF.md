# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-27T15:12:00Z
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Default branch: main

## Mission (unchanged)

Read and follow RESEARCH_PROMPT.md. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes.

No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify .github/workflows without explicit maintainer authorization.

## Prior agent task — COMPLETED (this session, 2026-10-27T15:12:00Z)

Task: Read the prior agent task from the durable handoff and complete it. Then update the handoff and write a clear initial task message for the next agent.

Completion summary (this session):
- Re-verified state from AGENT_HANDOFF.md and repo: HEAD cb206636 (checkpoint), tracked tree clean (only untracked __pycache__ caches), all tests pass 25/25.
- Completed highest-value authorized task (rank 2 in experiment_frontier.json): enumerated and tested additional admissible public liquidation sources for Track A (Binance data.binance.vision, Bybit public.bybit.com, OKX/Deribit, academic/GitHub/HF/Zenodo, vendors). Documented findings in `research_state/liquidation_sources_enumeration.md`. Conclusion: Track A NOT VIABLE with admissible unauthenticated public sources (Binance liquidationSnapshot 404, forceOrders 451; no complete census found elsewhere; partial streams cannot satisfy completeness requirement). No event-free intervals inferred.
- Confirmed prior agent's corrections remain in place: FCLR-001 evaluated panel BTCUSDT-only (not >=5 instruments), evaluation summaries flagged untrusted/conflicting, FCLR-002 coverage sufficient in principle but not executed/authorized.
- Verified frozen artifacts unchanged: research_protocol.md v1.0, run_manifest.json splits/embargo intact, final_inconclusive_report.md and gate_assessment.md remain consistent.
- Updated handoff timestamp and added this session's completion record; preserved all constraints (no holdout reuse, no protocol/split changes, no unexecuted runs claimed).
- Wrote clear initial task message for next agent below. No network activity beyond read-only probes, no frozen artifacts modified.

## Current verified state (corrected 2026-10-27T14:20Z — supersedes earlier handoff figures)

- Repository status: INCONCLUSIVE. Forecast gate NOT MET (PILOT/INCONCLUSIVE). Risk-overlay phase INELIGIBLE. Direct liquidation labels unavailable (Track A BLOCKED).
- Frozen protocol: research_state/research_protocol.md v1.0 (FCLR-001).
- Frozen splits (research_state/run_manifest.json): train 2024-01-02T00:00:00Z..2024-02-24T08:00:00Z; val 2024-03-02T08:00:00Z..2024-03-20T02:00:00Z; test 2024-03-27T02:00:00Z..2024-03-30T23:00:00Z; 7-day embargo.
- **CORRECTION — evaluated panel is BTCUSDT-only, NOT >=5 instruments.** `research_state/coverage_audit_recheck.md` (2026-10-26T20:45Z) shows mark-price CSVs for ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT begin at 2024-04-01; inside the frozen FCLR-001 window (2024-01..2024-03) their intersection is 0 timestamps. `scripts/_diag_panel.py` confirms FCLR-001 eval rows = 1634, all BTCUSDT. The protocol's ">=5 instruments" gate was therefore NEVER MET. This is a coverage/representativeness defect, not a leakage defect.
- **CORRECTION — headline QLIKE figures.** The earlier handoff's n=70 values (B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105) do not match any artifact in the tree. The only evaluation summaries present are:
  - `research_state/evaluation_summary.md` — FCLR-001, test n=70: B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105; C2 vs B1 -2.50% rel, 95% CI [-0.123401, 0.158843] crosses zero.
  - `research_state/evaluation_summary_FCLR002.md` — labeled "FCLR-001" in heading but experiment FCLR-002, data range 2024-01-01..2024-06-30, test n=94: B0=0.432319, B1=0.399218, C1=0.769779, C2=0.752404; C2 vs B1 diff +0.353186 (CI [-0.078192, 1.037320]) i.e. C2 WORSE than B1, -88.47% "reduction" is a sign-convention artifact. This file is internally inconsistent (heading says FCLR-001, body says FCLR-002) and its numbers contradict evaluation_summary.md. Treat both summaries as untrusted until independently recomputed; do not cite either as verified.
- Verdict unchanged and robust either way: forecast gate NOT MET. Single-instrument + single ~4-day block; CI crosses zero; multiplicity not satisfied.
- Implementation: forecast pipeline (7/7 tests), synthetic boundary labels (5/5), funding-correction replication partial (4/4; 445 events, median 8.0h). Controller progress accounting 6/6.
- Registry present: hypothesis_registry.json, experiment_frontier.json, negative_results_report.md, leakage_audit.md, gate_assessment.md, final_inconclusive_report.md, fclr002_coverage_audit.json.
- FCLR-002 coverage (independently re-verified this session via `python scripts/fclr002_coverage_audit.py --out /tmp/x.json`): 5 symbols, 4392 common hourly timestamps, single contiguous window 2024-04-01T00:00:00Z..2024-09-30T23:00:00Z (~183 days). Sufficient in principle for >=3 non-overlapping 30-day blocks, but NOT executed and its holdout NOT opened. Data present in research_state/data_cache (4174 zips / 7350 extracted CSVs, 87M). scripts/fclr002_download.py idempotent; no network activity performed.

## Initial task message for next agent

**Current state (do not alter):** Repository is INCONCLUSIVE. Forecast gate NOT MET (PILOT/INCONCLUSIVE). Risk-overlay phase INELIGIBLE. Direct liquidation labels unavailable (Track A BLOCKED — enumerated and confirmed unviable with admissible unauthenticated public sources; see `research_state/liquidation_sources_enumeration.md`). Frozen protocol: research_state/research_protocol.md v1.0 (FCLR-001). FCLR-001 sealed holdout must NOT be retrained, re-tuned, or re-evaluated. The OOS window must NOT be extended and splits/protocol must NOT be changed.

**Two corrections to earlier handoff figures (verified):**
1. The FCLR-001 evaluated panel is **BTCUSDT-only**, not >=5 instruments. `research_state/coverage_audit_recheck.md` + `scripts/_diag_panel.py`: 1634 eval rows, all BTCUSDT; the other four symbols have no mark-price CSVs before 2024-04-01. The protocol's >=5-instruments gate was never met.
2. Two conflicting evaluation summaries exist and both are flagged untrusted: `research_state/evaluation_summary.md` (FCLR-001, n=70: B0=0.140791, B1=0.147800, C1=0.145083, C2=0.144105; C2 vs B1 -2.50%, CI [-0.123401, 0.158843]) and `research_state/evaluation_summary_FCLR002.md` (heading says FCLR-001, body says experiment FCLR-002, data range 2024-01-01..2024-06-30, n=94: B0=0.432319, B1=0.399218, C1=0.769779, C2=0.752404, C2 vs B1 diff +0.353186 — C2 WORSE; its "-88.47% relative reduction" is a sign-convention artifact). Do not cite either as verified until independently recomputed.

**FCLR-002 status:** Coverage audit (research_state/fclr002_coverage_audit.json) confirms 5 instruments (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), 4392 common hourly timestamps, single contiguous window 2024-04-01T00:00:00Z..2024-09-30T23:00:00Z (~183 days), sufficient in principle for >=3 non-overlapping 30-day blocks. Coverage sufficient, but FCLR-002 execution is NOT authorized unless explicitly requested with a pre-registered protocol version (FCLR-002 v1.0) specifying splits and acceptance criteria BEFORE computing any outcomes. Do not run scripts/fclr002_download.py or scripts/fclr002_coverage_audit.py (the latter writes to the tracked artifact unless --out is given) unless explicitly instructed. Do not reuse the FCLR-001 sealed holdout for selection/tuning.

**What to do:**
1. Read RESEARCH_PROMPT.md, AGENT_HANDOFF.md, research_state/research_protocol.md, research_state/final_inconclusive_report.md, research_state/gate_assessment.md, research_state/liquidation_sources_enumeration.md to confirm current state.
2. Confirm repository remains in verified state: clean tracked tree (or only untracked caches), all tests pass (25 passed), no holdout leakage introduced.
3. Track A enumeration complete (rank 2 done). Next highest-value authorized task (rank 3 in experiment_frontier.json): register margin/leverage scenarios and run out-of-sample hypothetical boundary-breach forecast (FCLR-H003). Prerequisite: pre-register scenarios in a new protocol/version or clearly documented pre-registration BEFORE outcome inspection; synthetic boundary labels already implemented (scripts/synthetic_boundary_labels.py, 5/5 tests). Acceptance: pre-registered scenarios; Brier/log-loss/calibration/precision-recall reported; long and short labels kept separate; funding/fee/price-reference assumptions disclosed. Do NOT describe modeled boundary breaches as observed liquidations. FCLR-001 forecast gate not met; boundary forecast is separate and does not unblock risk-overlay phase.
4. If FCLR-002 is explicitly requested, first pre-register a new protocol version (FCLR-002 v1.0) with split/acceptance criteria BEFORE computing any outcomes; run walk-forward evaluation on the 2024-04..2024-09 panel; run leakage audit on the new panel before opening its holdout.
5. Documentation/cleanup acceptable only if it improves clarity without modifying evaluation logic, splits, protocol, or reported results. Never claim unexecuted runs succeeded. Resolve the evaluation_summary.md vs evaluation_summary_FCLR002.md contradiction (either recompute canonically or annotate both as untrusted) before citing either.
6. Leave risk-overlay phase INELIGIBLE.

**Acceptance check:** State remains inconclusive with gates documented; no holdout leakage introduced; all existing tests pass (25 passed). No new model results reported from the current holdout. HEAD unchanged except for authorized checkpoint/documentation commits.

## Update (2026-10-27T15:12:XXZ) — Track A enumeration
- Enumerated admissible public liquidation sources for Track A (Binance data.binance.vision, Bybit public.bybit.com, OKX/Deribit, academic/GitHub/HF/Zenodo, vendors). 
- Binance liquidationSnapshot daily/monthly archives return 404; fapi forceOrders returns 451 in this environment. No unauthenticated complete public liquidation census found for required symbols/window.
- Bybit public trading data exists but contains per-trade data, not a liquidation event census; no liquidation directory found. Converting trades is not a complete census.
- No other obvious unauthenticated complete public liquidation archives identified. 
- Documented findings in `research_state/liquidation_sources_enumeration.md`. Track A remains BLOCKED (unviable with admissible unauthenticated public sources). Do not infer event-free intervals; do not use partial streams as complete census.
