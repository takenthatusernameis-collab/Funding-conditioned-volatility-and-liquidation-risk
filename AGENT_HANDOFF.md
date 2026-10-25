# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-25
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Default branch: main

## Mission

Read and follow RESEARCH_PROMPT.md. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes.

No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify .github/workflows without explicit maintainer authorization.

## Current verified state

- Coverage audit extended for BTCUSDT: downloaded/verified 31 daily klines/mark/index/premium archives for 2024-01-01..2024-01-31 (cached under research_state/data_cache/btcusdt_jan2024/). Funding monthly (2024-01) remains sole funding source.
- ETHUSDT archive availability verified (funding monthly 2024-01 HTTP 200; klines daily 2024-01-01 HTTP 200); full download/ingest not yet executed.
- Protocol still frozen; split timestamps remain pending (insufficient instruments/coverage for acceptance: need >=5 instruments and >=3 non-overlapping 30-day blocks).
- Controller progress accounting script present; tests 6/6 passed.
- Direct liquidation labels: NOT VERIFIED.
- Synthetic hypothetical mark-price boundary labels: NOT IMPLEMENTED.
- Future realized-volatility target: NOT IMPLEMENTED.
- Funding-correction survival replication: NOT IMPLEMENTED.
- Out-of-sample result: NOT RUN.
- Risk-overlay phase: INELIGIBLE.

## Research gates

- Direct actual liquidation labels: NOT VERIFIED.
- Synthetic hypothetical mark-price boundary labels: NOT IMPLEMENTED.
- Future realized-volatility target: NOT IMPLEMENTED.
- Funding-correction survival replication: NOT IMPLEMENTED.
- Frozen research protocol: FROZEN (research_state/research_protocol.md v1.0); exact split timestamps pending coverage audit.
- Out-of-sample result: NOT RUN.
- Risk-overlay phase: INELIGIBLE.

## Unresolved blockers

- Only BTCUSDT covered; need >=5 instruments (e.g., ETHUSDT) with aligned daily archives across >=3 non-overlapping 30-day blocks to freeze 60/20/20 splits with 7-day embargo.
- Direct liquidation labels unavailable.

## Highest-value next task

**Extend coverage audit to >=5 instruments and freeze split boundaries.**
- Download/ingest daily archives for ETHUSDT (and additional UM perpetuals) for 2024-01..2024-03 (or equivalent), verify checksums, normalize UTC, validate schemas, record gaps.
- Freeze exact split timestamps in research_state/research_protocol.md section 6 and update run_manifest.json with split_boundaries (train/val/test UTC, embargo_days=7).
- Acceptance check: protocol section 6 non-pending; run_manifest.json contains frozen split_boundaries; coverage audit documents >=5 instruments paired OOS panel and >=3 non-overlapping 30-day blocks. No target outcomes computed.

## Initial task message for next agent

Extend coverage audit to >=5 instruments and freeze split boundaries. Download/ingest daily archives for ETHUSDT (and additional UM perpetuals) for 2024-01..2024-03, verify checksums, normalize UTC, validate schemas, record gaps. Freeze exact split timestamps in research_state/research_protocol.md section 6 and update run_manifest.json with split_boundaries (train/val/test UTC, embargo_days=7). Acceptance: protocol section 6 non-pending; run_manifest.json contains frozen split_boundaries; coverage audit documents >=5 instruments paired OOS panel and >=3 non-overlapping 30-day blocks. No target outcomes computed.

At the end of each session, replace this handoff with a concise update that preserves the verified state, summarizes only executed tests and evidence, records unresolved blockers, and names one highest-value next task with an exact acceptance check. Never claim an unexecuted command, unverified source, or incomplete workflow run succeeded.
