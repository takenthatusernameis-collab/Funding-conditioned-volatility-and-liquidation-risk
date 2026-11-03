# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 2026-11-03T14:04:06Z
Git SHA (HEAD): c399cd19
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261103T140406Z | Priority: HEAVY-WORK (do not do status-only) | Mode: EXECUTION-ONLY-IF-DATA-ELSE-BLOCKER

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (copy/paste as first action)
```
TASK ID: FCLR-NEXT-012-EXEC
PRIORITY: P0 - EXECUTION PHASE (heavy work enforced)
CAMPAIGN: CONSOLIDATE-TRACKA-AND-FUNDING-INCREMENTAL
REPO FOCUS: Funding-conditioned volatility and liquidation risk (Track A = Hyperliquid ironflow observed liquidation labels; Track V = funding-conditioned volatility on Binance perpetual panel)
TIMESTAMP (UTC): 2026-11-03T14:04:06Z
OBJECTIVE: Execute forward validation ONLY if new admissible data exists. Otherwise write a CONCRETE BLOCKER with evidence and STOP. Do heavy work, not status summaries.
HARD RULES: Pre-register BEFORE inspecting outcomes. Freeze splits/metrics/gates. Enforce embargoes (>=7d). Block-bootstrap (>=2000 reps). No tuning. Separate experiments. NEVER reuse sealed holdouts. IMMUTABLE cross-track firewall (no Binance<->Hyperliquid merge). Overlay HYPOTHETICAL_ONLY. Do not relax thresholds. No status-only files.
ADMISSIBLE TRIGGERS:
- Track A (FCLR-012-A): new Hyperliquid ironflow monthly parquet > 2026-10-31 at research_state/data_cache/ironflow_events/*.parquet
- Track V (FCLR-012-V): new unsealed 2026 Binance panel beyond 2026-05-08..2026-08-06 for BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT (1h/funding/index/mark/premium)

MANDATORY ACTION SEQUENCE:
1) VERIFY: python -m pytest tests/test_fclr010_harness.py -v (must be green). Check frontier/manifest/prereg/consolidated/synthesis exist. Confirm ONLY AGENT_HANDOFF.md exists as durable handoff (no NEXT_AGENT_HANDOFF_*.md).
2) SCAN: Check ironflow_events for files > 2026-10-31; check for new unsealed 2026 Binance data beyond sealed window (root 2024 zips only, no new found).
3) IF TRIGGER: pre-register fresh experiment via scripts/fclr010_harness.py pre_register_forward_experiment() BEFORE inspecting outcomes; run evaluate_forward() with frozen config; write results to research_state/ with cross-links.
4) IF NO TRIGGER: Write concrete BLOCKER to research_state/blockers_FCLR-012_<YYYYMMDDTHHMMSSZ>.md with exact paths checked, last timestamps, why insufficient, next unauthenticated routes. DO NOT re-run sealed panels, tune, merge tracks, or create status-only files. STOP.

FAILURE = merge tracks / retune / re-run sealed / status-only / fabricate data.
```

## 1) Bottlenecks removed (this session)
- Duplicate NEXT_AGENT_HANDOFF_*.md: NONE (only AGENT_HANDOFF.md remains).
- Stale handoffs: cleaned.
- Harness hardened: pre_register_forward_experiment() locks prereg; evaluate_forward() requires prereg, frozen config only.
- Preregs/consolidation/synthesis/manifest/frontier all in place.
- Existing blockers present (blockers_FCLR-012_20261103T120855Z.md, blockers_FCLR-012_20261103T140313Z.md) - evidence-based, not status-only.

## 2) Verified state (tests/evidence)
- tests/test_fclr010_harness.py: 4/4 PASS (2026-11-03T14:00:07Z)
- FCLR-010: FORECAST_GATE_PASSED (C2 vs B1 Brier -0.003077, rel -2.21%)
- FCLR-011: FORECAST_GATE_PASSED (C2 vs B1 QLIKE -0.016458, rel -4.94%, CI [-0.032546,-0.001418])
- Track A latest: research_state/data_cache/ironflow_events/2026-10.parquet (no >2026-10-31)
- Track V: sealed 2026-05-08..2026-08-06 only; root has 2024 zips only

## 3) Key artifacts
- research_state/track_a_fclr010_consolidated.md
- research_state/funding_incremental_synthesis_20261103T115630Z.md
- research_state/forward_campaign_fclr012_prereg.md
- research_state/run_manifest.json, research_state/experiment_frontier.json (FCLR-012 present)
- scripts/fclr010_harness.py (hardened)
- research_state/blockers_FCLR-012_20261103T140313Z.md (concrete blocker with evidence)

## 4) Frozen rules (immutable)
- Pre-register before inspecting outcomes
- Freeze splits/metrics/gates
- Embargo >=7d, block-bootstrap >=2000 reps
- No tuning on holdout/test, never reuse sealed holdouts
- Separate experiments, immutable cross-track firewall (no Binance<->Hyperliquid merge)
- Overlay HYPOTHETICAL_ONLY, no live/paper trading
- Heavy work only - no status-only files

**NEXT AGENT: EXECUTE FCLR-NEXT-012 ONLY IF NEW ADMISSIBLE DATA APPEARS. ELSE WRITE CONCRETE BLOCKER WITH EVIDENCE AND WAIT. NO DEVIATION.**
