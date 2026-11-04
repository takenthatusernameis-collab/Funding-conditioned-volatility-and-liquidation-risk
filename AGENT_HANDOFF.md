# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T123437Z
Git SHA (HEAD): c37d7af0
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T123437Z | Priority: P0 - HEAVY WORK ENFORCED | Mode: BLOCKED-BY-GAP

## MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE)
```text
TASK ID: FCLR-NEXT-053-BLOCKED-HEAVY-WORK
PRIORITY: P0 - HEAVY WORK ENFORCED
CAMPAIGN: MAINTAIN READINESS UNTIL NEW DATA
TIMESTAMP (UTC): 20261104T123437Z
OBJECTIVE: Program confirmatory execution is CLOSED until NEW admissible unauthenticated data. Execute ALL mandatory blocked-path heavy work every session (3A-3D). Do NOT re-run sealed cells, do NOT tune/threshold-shop, do NOT fabricate data, do NOT touch .github/workflows.
RESUME ONLY IF: Track A gets data/events/YYYY-MM.parquet >=2026-11 on ironflow (unauthenticated) OR Track C gets admissible Binance mark/index/premium panel with >=3 non-overlapping 30-day blocks of real volume>0 beyond 2026-11-02. Preregister BEFORE outcomes.
```

## Current Verified State
- Tests: 117/117 OK
- HEAD: dd188ea1 clean of workflow changes
- Track A (ironflow): data_through 2026-10; no 2026-11+. Probe done 2026-11-04T12:32:53Z - no trigger.
- Track C: Binance panel ended/placeholders beyond 2026-11-02; inadmissible.
- Track B: CLOSED_NEGATIVE. H002: PERMANENT_BLOCKED.

## Heavy Work Executed This Session (blocked-path)
- 3A: Reviewed monitor_ironflow_liquidations.py; confirmed state-aware probing logic intact.
- 3B: Tests green (117/117). __pycache__/pyc cleaned.
- 3C: Created research_state/watch/gap_analysis_20261104T123300Z.md with complete probe table and resume conditions.
- 3D: Updated research_state/experiment_frontier.json with blocked cells and triggers.

## Artifacts
- research_state/watch/gap_analysis_20261104T123300Z.md
- research_state/watch/trigger_harden_20261104T123341Z.json
- Updated experiment_frontier.json

## Next Action
Probe every 30-120 min. On new data -> prereg BEFORE outcomes, run frozen harness, write evaluation summary with block-bootstrap>=2000 and Holm, update frontier. No idle waiting without heavy work.
