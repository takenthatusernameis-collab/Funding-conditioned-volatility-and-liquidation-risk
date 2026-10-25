# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-25
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Default branch: main

## Mission

Read and follow RESEARCH_PROMPT.md. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes.

No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify .github/workflows without explicit maintainer authorization.

## Current verified state

- On the initial repository tree inspection, the visible tracked contents were .github/workflows/main.yml and research_state/workflow_run_diagnostics.jsonl. The diagnostics ledger was empty. No README, research pipeline, scripts directory, tests directory, or prior research report was visible at that inspection. Recheck current HEAD rather than assuming nothing has changed.
- Added RESEARCH_PROMPT.md, the primary research protocol/agent instruction. Creation commit: cceedfc2dc32809a985bbef0f8a0b327d6a607ca.
- No data ingestion, model fitting, backtest, test suite, forecast evaluation, or liquidation-label verification has yet been performed as part of this setup. Do not describe the hypothesis as tested.
- The prompt cites the September 2026 SSRN working paper “Limits to Coordination: Funding Drag in Crypto Perpetual Funding Rates” as motivation and requires independent evaluation. The reported 27h vs 3h correction-time contrast is not itself evidence of liquidation forecasting.
- Public Binance market-data archives are a sensible first source for funding, futures klines, mark-price/index-price/premium-index data and public market metrics. Historical direct liquidation label availability must be verified against actual unauthenticated files; do not infer event-free intervals from missing records.
- The current workflow appears to call scripts/controller_progress.py during checkpoint/progress accounting, and push-only controller tests appear to reference tests/test_controller_progress_accounting.py, tests/test_workflow_diagnostics_scanner.py, tests/test_nonfinite_result_serialization.py, and tests/test_campaign_resume.py. Those ordinary code/test paths were not present in the initial recursive tree. Treat this as a high-priority audit item, not a proven runtime failure: inspect all call sites and semantics, verify the current tree, then implement only the minimum compatible non-workflow code and tests if required. Do not fabricate progress accounting or edit workflow files.

## Next task — do this first

1. Reinspect git status, current HEAD, recent commits, full current tree, RESEARCH_PROMPT.md, AGENT_HANDOFF.md, and .github/workflows/main.yml.
2. Audit every workflow reference to scripts, tests, controller progress, handoff, and persistence. Verify which missing paths are actually required on the scheduled path and which are only used on push/diagnostics paths.
3. If scripts/controller_progress.py is genuinely missing and needed for correct meaningful-progress accounting, implement the smallest correct ordinary script based on every caller and expected output/exit semantics. Add focused tests covering:
   - clean/no-change session is not credited as progress;
   - a meaningful project change is credited only for the intended base/head range;
   - workflow-only changes are never counted as project progress;
   - invalid/missing SHAs fail closed;
   - the verified remote SHA must match the head before durable progress is credited;
   - no status-only or marker-only commit can masquerade as research progress.
   Inspect whether the referenced tests are also missing; add coherent tests for real controller behavior rather than empty test stubs.
4. Run the focused tests and static checks, capture exact outcomes, and update the relevant research-state notes. Do not change .github/workflows.
5. Then make a small, bounded unauthenticated source probe of the official Binance archive for the first feasible pipeline: one or two liquid perpetual symbols with historical funding, mark-price, index/premium, and OHLCV data. Record exact URLs, dates, schema, checksums, units, gaps, and license/source terms. Separately probe whether historical forced-liquidation records are actually downloadable without credentials. Use small requests first.
6. Pick the next action based on observed evidence and update this file with the command/test that verifies the next step.

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
