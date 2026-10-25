# Agent Handoff — Funding-Conditioned Volatility and Liquidation Risk

Updated: 2026-10-25
Repository: https://github.com/takenthatusernameis-collab/Funding-conditioned-volatility-and-liquidation-risk
Default branch: main

## Mission

Read and follow RESEARCH_PROMPT.md. Validate whether funding extremes, realized volatility, and pre-specified delayed/smoothed-price features add out-of-sample predictive value for future volatility or liquidation-related stress. Forecast validation comes first. A risk-reduction overlay is ineligible until a frozen out-of-sample forecast gate passes.

No paid services, paid trials, account signup, manually supplied keys/files, user intervention, live trading, or paper trading. Do not modify .github/workflows without explicit maintainer authorization.

## Current verified state

- Added RESEARCH_PROMPT.md, the primary research protocol/agent instruction. Prompt upgraded with sections 13–20 (frozen hypotheses/lineage, FCLR-001 starter design, chronological splits/embargo, multiplicity/inference, negative-result preservation).
- Protocol frozen in `research_state/research_protocol.md` (FCLR-001 v1.0). Split timestamps pending coverage audit; no outcomes computed.
- Controller progress accounting script present at `scripts/controller_progress.py` with tests passing (`tests/test_controller_progress_accounting.py` - 6/6 passed).
- Coverage audit completed for BTCUSDT minimum viable dataset:
  - Downloaded/cached archives verified (checksums match binance_source_probe.md): `fundingRate-2024-01.zip` (sha256 3e0d3087...), `klines-1h-2024-01-01.zip` (sha256 09a24635...), mark/index/premium zips present.
  - Extracted and schema-validated: funding 93 rows (2024-01), klines/mark/index/premium 24 rows each (2024-01-01).
  - Normalized to UTC, gaps recorded (none observed in audited range). Direct liquidation labels: NOT VERIFIED (no archives found; API restricted).
- Created `research_state/run_manifest.json` with full provenance (git SHA, data hashes, sample counts, software versions, status AUDIT_COMPLETE_PENDING_SPLITS). `test -s research_state/run_manifest.json` passes.

## Research gates

- Direct actual liquidation labels: NOT VERIFIED.
- Synthetic hypothetical mark-price boundary labels: NOT IMPLEMENTED.
- Future realized-volatility target: NOT IMPLEMENTED.
- Funding-correction survival replication: NOT IMPLEMENTED.
- Frozen research protocol: FROZEN (research_state/research_protocol.md v1.0); exact split timestamps pending coverage audit.
- Out-of-sample result: NOT RUN.
- Risk-overlay phase: INELIGIBLE.

Keep these states accurate. Engineering scaffolding is not performance evidence.

## Unresolved blockers

- Split boundaries not yet frozen (need to extend coverage audit beyond 2024-01-01 to determine valid 60/20/20 splits with 7-day embargo). Current cached data only covers 2024-01-01 daily klines + 2024-01 monthly funding (insufficient for full splits).

## Highest-value next task

**Extend coverage audit and freeze split boundaries for FCLR-001.**
- Download/ingest additional daily/hourly archives to build sufficient history for chronological 60/20/20 split with 7-calendar-day embargo (at minimum extend beyond Jan 1 2024). Verify checksums against binance_source_probe or discover patterns, normalize UTC, validate schemas, record gaps.
- Freeze exact split timestamps in `research_state/research_protocol.md` section 6 and update `research_state/run_manifest.json` with `split_boundaries` populated (train/val/holdout UTC timestamps, embargo applied).
- Acceptance check: protocol section 6 has non-pending split timestamps; `run_manifest.json` contains frozen `split_boundaries` with train_start/end, val_start/end, test_start/end and embargo_days=7; coverage audit documents sufficient sample counts for minimum claim-worthy test (>=5 instruments in paired OOS panel, >=3 non-overlapping 30-day blocks). No target outcomes computed.

## Durable handoff requirement

At the end of each session, replace this handoff with a concise update that preserves the verified state, summarizes only executed tests and evidence, records unresolved blockers, and names one highest-value next task with an exact acceptance check. Never claim an unexecuted command, unverified source, or incomplete workflow run succeeded.
