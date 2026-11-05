# Campaign Sweep Track A (FCLR-NEXT-079) - Step 1
Timestamp (UTC): 20261105T012634Z
Git SHA (HEAD): 012474144be8a963421f0eae52cb89d79f485d2a
Branch: main

## Repo-name prioritization (inferred)
Repository name: "Funding-conditioned-volatility-and-liquidation-risk"
- Funding-conditioned VOLATILITY component = Track C (FCLR-011) — COMPLETE/SEALED/LOCKED. Forecast gate PASSED on frozen splits. DO NOT retune/re-run sealed cells.
- Liquidation RISK component = Track A (FCLR-010) — BLOCKED on admissible unauthenticated liquidation data. UNFULFILLED HALF - HIGHEST ACTIVE PRIORITY.

## State files read (evidence)
- RESEARCH_PROMPT.md: read (mission/constraints, Track A/B/C separation, gates)
- AGENT_HANDOFF.md: read (single durable handoff, campaign FCLR-NEXT-079)
- research_state/experiment_frontier.json: last_checked 2026-11-04T23:31:18Z, Track A blocked on ironflow >=2026-11; resume conditions listed
- research_state/run_manifest.json: FCLR-010 sealed/gate passed (test 2026-05-28..2026-10-31, 5 blocks), FCLR-011 sealed/passed, FCLR-012-V inconclusive (0 blocks)
- scripts/monitor_ironflow_liquidations.py: hardened (ETag/tree cache, HEAD fast-path, baseline-drift, per-file ETag/LM, fastpath, forward-edge probe, backoff/retries)
- scripts/hunt_alternative_liquidation_sources.py: hardened (HF search cache 24h, per-URL probe cache 6h, dedup, merged DEEP_REVIEW_URLS)
- scripts/deep_review_alt_sources.py: reuses hunt shared probe cache

## Current verified bottlenecks removed (baseline to NOT regress)
- Consolidated alt_source_scan_*.json -> single latest
- Consolidated alt_source_deep_review_*.md -> single latest
- monitor_ironflow_liquidations.py has ETag/tree cache, HEAD-404 fast path, forward-edge-only resume probe, baseline-drift state-only skip on 304, per-file ETag/LM caching, fastpath cache
- hunt_alternative_liquidation_sources.py has 24h HF search cache, 6h per-URL probe cache, URL dedup, merged DEEP_REVIEW_URLS
- deep_review_alt_sources.py reuses hunt's shared URL probe cache
- No schedulers/pollers/status-only files/repeated wrappers
- Suite regression fixed (restored cache APIs) - currently 179 passed

## Redundant/status-only artifacts check
Scanning for new redundant schedulers/pollers/status-only files/repeated wrappers added since last handoff - none observed. Will verify explicitly during probe step.

## Diff vs "latest sweep"
No prior campaign_sweep_tracka_*.md found in research_state/ at start of this session - this is the first sweep for FCLR-NEXT-079 (establishing baseline).

## Next
Proceed to Step 2: trigger probe with full tables.
