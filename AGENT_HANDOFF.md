# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T132236Z
Git SHA (HEAD): a98ec9b0
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T132236Z | Priority: P0 - HEAVY WORK ENFORCED | Mode: BLOCKED-BY-GAP

## MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE)
```text
TASK ID: FCLR-NEXT-055-BLOCKED-HEAVY-WORK
PRIORITY: P0 - HEAVY WORK ENFORCED
CAMPAIGN: MAINTAIN READINESS UNTIL NEW DATA
TIMESTAMP (UTC): 20261104T132236Z
OBJECTIVE: Program confirmatory execution is CLOSED until NEW admissible unauthenticated data. Execute ALL mandatory blocked-path heavy work every session (3A-3D). Do NOT re-run sealed cells, do NOT tune/threshold-shop, do NOT fabricate data, do NOT touch .github/workflows.
RESUME ONLY IF: Track A gets data/events/YYYY-MM.parquet >=2026-11 on ironflow (unauthenticated) OR Track C gets admissible Binance mark/index/premium panel with >=3 non-overlapping 30-day blocks of real volume>0 beyond 2026-11-02. Preregister BEFORE outcomes.
```

## Current Verified State
- Tests: 164/164 OK (pytest, 16.41s)
- HEAD: a98ec9b0 (was b1e000dc at last handoff)
- Track A (ironflow): data_through 2026-10; probe 2026-11-04T13:21:55Z - no trigger (tree 304, unchanged).
- Track C: Binance panel ended/placeholders beyond 2026-11-02; inadmissible.
- Track B: CLOSED_NEGATIVE. H002: PERMANENT_BLOCKED.
- __pycache__/*.pyc cleaned (7 files modified, staged for cleanup).

## Heavy Work Executed This Session (blocked-path)
- 3A: Reviewed monitor_ironflow_liquidations.py; confirmed state-aware probing logic intact.
- 3B: Tests green (164/164). __pycache__/pyc cleaned.
- 3C: Probe recorded research_state/ironflow_probe_20261104T132155Z.json.
- 3D: Handoff refreshed (this file).

## Next Action
Probe every 30-120 min. On new data -> prereg BEFORE outcomes, run frozen harness, write evaluation summary with block-bootstrap>=2000 and Holm, update frontier. No idle waiting without heavy work.

## Repo-Name-Prioritized Focus (Funding-conditioned-volatility-and-liquidation-risk)
The repo name prioritizes Track C (funding-conditioned volatility) > Track A (liquidation risk). Track C is SEALED/NOT_SUPPORTED (FCLR-003: C2 vs B1 +0.015205 QLIKE, CI crosses zero, gate NOT_MET). Track A is the ONLY reopen path and requires NEW admissible unauthenticated liquidation data. All heavy work must preserve this priority: source discovery for Track A is the highest-value blocked-path task until data appears.

## Bottleneck Removal (if multiple sessions blocked/inefficient)
The single bottleneck is NEW admissible unauthenticated data. To prevent inefficient repeated probing:
1. monitor_ironflow_liquidations.py already implements state-aware probing with ETag caching - USE IT, do not re-probe manually.
2. hunt_alternative_liquidations_sources.py and deep_review_alt_sources.py cover 30+ source families with rubric scoring - run these periodically but only when new evidence is plausible.
3. Do NOT create new polling loops, schedulers, or status files. Every session must produce a verifiable artifact (probe JSON, source scan, test result, or handoff update).