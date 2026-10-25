# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-25
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Default branch: main

## Mission

Read and follow RESEARCH_PROMPT.md. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes.

No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify .github/workflows without explicit maintainer authorization.

## Current verified state

- On the initial repository tree inspection, the visible tracked contents were .github/workflows/main.yml and research_state/workflow_run_diagnostics.jsonl. The diagnostics ledger was empty. No README, research pipeline, scripts directory, tests directory, or prior research report was visible at that inspection. Recheck current HEAD rather than assuming nothing has changed.
- Added RESEARCH_PROMPT.md, the primary research protocol/agent instruction. Initial creation commit: cceedfc2dc32809a985bbef0f8a0b327d6a607ca. Upgraded and expanded prompt commit: 4f501d5478cd593f95640ea9afb83e8e37a5c720.
- No data ingestion, model fitting, backtest, test suite, forecast evaluation, or liquidation-label verification has yet been performed as part of this setup. Do not describe the hypothesis as tested.
- The prompt cites the September 2026 SSRN working paper “Limits to Coordination: Funding Drag in Crypto Perpetual Funding Rates” as motivation and requires independent evaluation. The reported 27h vs 3h correction-time contrast is not itself evidence of liquidation forecasting.
- Public Binance market-data archives are a sensible first source for funding, futures klines, mark-price/index-price/premium-index data and public market metrics. Historical direct liquidation label availability must be verified against actual unauthenticated files; do not infer event-free intervals from missing records.
- The current workflow appears to call scripts/controller_progress.py during checkpoint/progress accounting, and push-only controller tests appear to reference tests/test_controller_progress_accounting.py, tests/test_workflow_diagnostics_scanner.py, tests/test_nonfinite_result_serialization.py, and tests/test_campaign_resume.py. Those ordinary code/test paths were not present in the initial recursive tree. Treat this as a high-priority audit item, not a proven runtime failure: inspect all call sites and semantics, verify the current tree, then implement only the minimum compatible non-workflow code and tests if required. Do not fabricate progress accounting or edit workflow files.


## Prompt-quality review and verified upgrade

A repository-quality review compared the initial prompt against a mature continuous quantitative research workflow with frozen hypotheses, point-in-time expanding-universe controls, complete expected-versus-observed result accounting, adaptive feasibility gates, negative-result preservation, immutable holdouts, and deterministic validation. The initial prompt was strong on scientific caution but left too much of the first experiment and long-running evidence governance unspecified.

RESEARCH_PROMPT.md now includes sections 13–20 adding:
- Stable hypothesis/experiment IDs and immutable source/config/result lineage.
- A concrete FCLR-001 starter design: hourly panel, primary 24-hour forward realized-variance target, B0/B1 volatility baselines, funding-augmented C1, combined C2, and a declared primary contrast.
- Chronological 60/20/20 default splits, a 7-day purge/embargo, minimum instrument/time-block evidence requirements, QLIKE, fixed inference, and a practical effect-size gate.
- Separate observed-liquidation, modeled-boundary, volatility, and funding-correction research tracks.
- An adaptive feasibility trigger that permits new, separately registered pilot/alternative tracks without loosening hard scientific constraints.
- Whole-family multiple-testing treatment, sequential alpha spending, complete terminal result ledgers, idempotent resume, adversarial tests, independent result recomputation, and a per-session research feedback contract.

This is a prompt/protocol upgrade only. It has not executed ingestion, tests, model fitting, or a backtest. It must not be reported as empirical validation. The protected workflow has not been edited.

## Next task — do this first

Binance source probe completed and saved to `research_state/binance_source_probe.md` (exact URLs, date ranges, schema, checksums, forced-liquidation verdict: not directly downloadable). Next: freeze FCLR-001 research protocol in `research_state/research_protocol.md` with symbol universe, hourly panel, 24h forward realized-variance target, chronological 60/20/20 splits, 7-day purge/embargo, baselines C0/C1/C2, primary contrast, QLIKE and fixed inference, minimum evidence requirements. Acceptance check: `test -s research_state/research_protocol.md` and file contains frozen split dates, target definition, baselines, and primary contrast.
## Research gates

- Direct actual liquidation labels: NOT VERIFIED.
- Synthetic hypothetical mark-price boundary labels: NOT IMPLEMENTED.
- Future realized-volatility target: NOT IMPLEMENTED.
- Funding-correction survival replication: NOT IMPLEMENTED.
- Frozen research protocol: specified in RESEARCH_PROMPT.md; detailed parameter values, exact splits, and primary endpoints must be frozen in research_state/research_protocol.md before holdout evaluation.
- Out-of-sample result: NOT RUN.
- Risk-overlay phase: INELIGIBLE.

Keep these states accurate. Engineering scaffolding is not performance evidence.

## Durable handoff requirement

At the end of each session, replace this handoff with a concise update that preserves the verified state, summarizes only executed tests and evidence, records unresolved blockers, and names one highest-value next task with an exact acceptance check. Never claim an unexecuted command, unverified source, or incomplete workflow run succeeded.
