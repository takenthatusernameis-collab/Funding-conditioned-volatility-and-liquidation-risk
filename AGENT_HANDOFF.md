# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T132155Z
Git SHA (HEAD): b1e000dc
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T132155Z | Priority: P0 - HEAVY WORK ENFORCED | Mode: BLOCKED-BY-GAP

## MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE)
```text
TASK ID: FCLR-NEXT-054-BLOCKED-HEAVY-WORK
PRIORITY: P0 - HEAVY WORK ENFORCED
CAMPAIGN: MAINTAIN READINESS UNTIL NEW DATA
TIMESTAMP (UTC): 20261104T132155Z
OBJECTIVE: Program confirmatory execution is CLOSED until NEW admissible unauthenticated data. Execute ALL mandatory blocked-path heavy work every session (3A-3D). Do NOT re-run sealed cells, do NOT tune/threshold-shop, do NOT fabricate data, do NOT touch .github/workflows.
RESUME ONLY IF: Track A gets data/events/YYYY-MM.parquet >=2026-11 on ironflow (unauthenticated) OR Track C gets admissible Binance mark/index/premium panel with >=3 non-overlapping 30-day blocks of real volume>0 beyond 2026-11-02. Preregister BEFORE outcomes.
```

## Current Verified State
- Tests: 164/164 OK
- HEAD: b1e000dc
- Track A (ironflow): data_through 2026-10; probe 2026-11-04T13:21:55Z - no trigger (tree 304).
- Track C: Binance panel ended/placeholders beyond 2026-11-02; inadmissible.
- Track B: CLOSED_NEGATIVE. H002: PERMANENT_BLOCKED.

## Heavy Work Executed This Session (blocked-path)
- 3A: Reviewed monitor_ironflow_liquidations.py; confirmed state-aware probing logic intact.
- 3B: Tests green (164/164). __pycache__/pyc cleaned.
- 3C: Probe recorded research_state/ironflow_probe_20261104T132155Z.json.
- 3D: Handoff refreshed.

## Next Action
Probe every 30-120 min. On new data -> prereg BEFORE outcomes, run frozen harness, write evaluation summary with block-bootstrap>=2000 and Holm, update frontier. No idle waiting without heavy work.
