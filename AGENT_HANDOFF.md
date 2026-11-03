# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 2026-11-03T14:05:57Z
Git SHA (HEAD): a9794e7c
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261103T140557Z | Priority: HEAVY-WORK (do not do status-only) | Mode: BLOCKED-FORWARD-PIVOT-TO-HEAVY-RESEARCH

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (copy/paste as first action)
```
TASK ID: FCLR-NEXT-013-HEAVY
PRIORITY: P0 - HEAVY WORK ENFORCED (no status-only, no waiting)
CAMPAIGN: FCLR-HEAVY-RESEARCH-013 (recomputation + adversarial audit + alternative Track A source discovery)
REPO FOCUS: Funding-conditioned volatility and liquidation risk (Track A = Hyperliquid ironflow observed liquidation labels; Track V = funding-conditioned volatility on Binance perpetual panel)
TIMESTAMP (UTC): 2026-11-03T14:05:57Z
OBJECTIVE: Forward validation FCLR-NEXT-012 is BLOCKED on new admissible data (no ironflow parquet > 2026-10-31; no unsealed 2026 Binance panel beyond 2026-05-08..2026-08-06). Do NOT wait. Execute heavy work that requires NO new data: (1) independent recomputation of FCLR-010/FCLR-011 sealed results from stored hashes, (2) adversarial leakage audit on sealed panels, (3) alternative Track A liquidation-label source discovery without new ironflow data, (4) deepen funding-conditioning validation on frozen FCLR-002 splits. Every session must ship one verifiable artifact.
HARD RULES: Pre-register BEFORE inspecting outcomes. Freeze splits/metrics/gates. Enforce embargoes (>=7d). Block-bootstrap (>=2000 reps). No tuning. Separate experiments. NEVER reuse sealed holdouts. IMMUTABLE cross-track firewall (no Binance<->Hyperliquid merge). Overlay HYPOTHETICAL_ONLY. Do not relax thresholds. No status-only files. Do not re-run sealed panels as forward validation.
ADMISSIBLE TRIGGERS (forward FCLR-NEXT-012, monitor-only):
- Track A (FCLR-012-A): new Hyperliquid ironflow monthly parquet > 2026-10-31 at research_state/data_cache/ironflow_events/*.parquet
- Track V (FCLR-012-V): new unsealed 2026 Binance panel beyond 2026-05-08..2026-08-06 for BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT (1h/funding/index/mark/premium)

MANDATORY ACTION SEQUENCE:
1) VERIFY: python -m pytest tests/test_fclr010_harness.py -v (must be green). Confirm ONLY AGENT_HANDOFF.md exists as durable handoff (no NEXT_AGENT_HANDOFF_*.md).
2) RECOMPUTE: Independent recomputation of FCLR-010 sealed Brier result (C2 vs B1) and FCLR-011 sealed QLIKE result (C2 vs B1) from research_state/run_manifest.json hashes + cached inputs. Write results to research_state/recompute_fclr010_<UTC>.md and research_state/recompute_fclr011_<UTC>.md. Acceptance: metrics match sealed values within numerical tolerance.
3) AUDIT: Run adversarial leakage audit on sealed FCLR-010/FCLR-011 panels (timestamp order, target non-overlap after purge/embargo, funding sign/timing, mark/index alignment, missing-not-zero). Write to research_state/leakage_audit_heavy_<UTC>.md.
4) ALTERNATIVE TRACK A: Execute one new admissible unauthenticated liquidation-label source probe NOT already covered by existing source_probe_FCLR-NEXT-002_* files. Document exact URL, no-auth result, schema, coverage, hash. Write to research_state/source_probe_heavy_tracka_<UTC>.md. Do not merge tracks.
5) DEEPEN: Regime-stratified QLIKE by funding quartile per symbol/time on frozen FCLR-002 splits (no new data, no outcome peek beyond frozen test). Write evaluation_summary_heavy_regime_<UTC>.md.
6) IF FORWARD TRIGGER APPEARS: pre-register fresh FCLR-012 experiment via scripts/fclr010_harness.py pre_register_forward_experiment() BEFORE inspecting outcomes; then run evaluate_forward().

FAILURE = merge tracks / retune / re-run sealed / status-only / fabricate data / wait-for-data without shipping heavy work.
```

## 1) Bottlenecks removed (this session)
- Duplicate NEXT_AGENT_HANDOFF_*.md: NONE (only AGENT_HANDOFF.md remains).
- Stale handoffs: cleaned.
- Harness hardened: pre_register_forward_experiment() locks prereg; evaluate_forward() requires prereg, frozen config only.
- Preregs/consolidation/synthesis/manifest/frontier all in place.
- Forward validation pivot: FCLR-NEXT-012 blocked on data; replaced with FCLR-NEXT-013 heavy-work campaign requiring no new data.

## 2) Verified state (tests/evidence)
- tests/test_fclr010_harness.py: 4/4 PASS (2026-11-03T14:00:07Z)
- FCLR-010: FORECAST_GATE_PASSED (C2 vs B1 Brier -0.003077, rel -2.21%, sealed)
- FCLR-011: FORECAST_GATE_PASSED (C2 vs B1 QLIKE -0.016458, rel -4.94%, CI [-0.032546,-0.001418], sealed)
- Track A latest: research_state/data_cache/ironflow_events/2026-10.parquet (no >2026-10-31)
- Track V: sealed 2026-05-08..2026-08-06 only; root has 2024 zips only
- Forward FCLR-NEXT-012: BLOCKED (concrete blocker at blockers_FCLR-012_20261103T140313Z.md)

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

## 5) Next focus campaign (heavy work, no new data required)
Campaign: FCLR-HEAVY-RESEARCH-013 — ship one verifiable artifact per session.
1) Independent recomputation of sealed FCLR-010/FCLR-011 results from stored hashes.
2) Adversarial leakage audit on sealed panels.
3) One alternative Track A liquidation-label source probe (no new ironflow data needed).
4) Regime-stratified QLIKE by funding quartile on frozen FCLR-002 splits.

**NEXT AGENT: FORWARD FCLR-NEXT-012 IS BLOCKED ON DATA — DO NOT WAIT. EXECUTE FCLR-NEXT-013 HEAVY WORK CAMPAIGN. SHIP ONE VERIFIABLE ARTIFACT. IF NEW ADMISSIBLE DATA APPEARS FOR FCLR-012, PRE-REGISTER BEFORE INSPECTING OUTCOMES. NO DEVIATION.**
