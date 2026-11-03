# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 2026-11-03T16:47:13Z
Git SHA (HEAD): 27219c7b
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261103T164713Z | Priority: HEAVY-WORK (do not do status-only) | Mode: STRUCTURAL-CLOSEOUT-DATA-TRIGGERED-WATCH

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (copy/paste as first action)
```
TASK ID: FCLR-NEXT-014-WATCH
PRIORITY: P0 - HEAVY WORK ENFORCED (no status-only, no waiting without shipping)
CAMPAIGN: FCLR-NEXT-014-DATA-TRIGGERED-REOPEN-WATCH (manifest LFS fix + trigger monitoring + structural integrity + pre-registration readiness)
REPO FOCUS: Funding-conditioned volatility and liquidation risk (Track A = Hyperliquid ironflow observed liquidation labels; Track C = funding-conditioned volatility on Binance perpetual panel; Track B = modeled boundary breaches)
TIMESTAMP (UTC): 2026-11-03T16:47:13Z
OBJECTIVE: All confirmatory campaigns are STRUCTURALLY CLOSED NEGATIVE (H001 NOT_SUPPORTED; overlay INELIGIBLE; Track A structurally blocked; Track B closed negative). FCLR-NEXT-012 forward validation BLOCKED on new admissible data (no ironflow parquet > 2026-10-31; no unsealed 2026 Binance panel beyond 2026-05-08..2026-08-06). FCLR-NEXT-013 heavy-work campaign (recompute FCLR-010/011, leakage audit, Track A source probe, regime-stratified QLIKE) is COMPLETE. Do NOT wait idly. Execute heavy work: (1) FIX the run_manifest.json Git LFS pointer bottleneck causing 4 TestFCLR010Harness errors, (2) run continuous admissible-data trigger watch (ironflow > 2026-10-31; new unsealed Binance panel), (3) preserve structural integrity (no duplicate handoffs, no stale artifacts, tests green), (4) pre-register readiness so forward experiment can launch immediately when a trigger fires. Every session must ship one verifiable artifact.
HARD RULES: Pre-register BEFORE inspecting outcomes. Freeze splits/metrics/gates. Enforce embargoes (>=7d). Block-bootstrap (>=2000 reps). No tuning. Separate experiments. NEVER reuse sealed holdouts. IMMUTABLE cross-track firewall (no Binance<->Hyperliquid merge). Overlay HYPOTHETICAL_ONLY. Do not relax thresholds. No status-only files. Do not re-run sealed panels as forward validation. Do not fabricate data.
ADMISSIBLE TRIGGERS (forward FCLR-NEXT-012, monitor-only):
- Track A (FCLR-012-A): new Hyperliquid ironflow monthly parquet > 2026-10-31 at research_state/data_cache/ironflow_events/*.parquet (latest: 2026-10.parquet; none newer)
- Track V (FCLR-012-V): new unsealed 2026 Binance panel beyond 2026-05-08..2026-08-06 for BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT (1h/funding/index/mark/premium)

MANDATORY ACTION SEQUENCE:
1) VERIFY: python -m unittest discover -s tests -v (117 tests; 4 errors in TestFCLR010Harness due to run_manifest.json Git LFS pointer — MUST FIX). Confirm ONLY AGENT_HANDOFF.md exists as durable handoff (no NEXT_AGENT_HANDOFF_*.md).
2) FIX BOTTLENECK: research_state/run_manifest.json is a 129-byte Git LFS pointer (oid sha256:ac27b18c...), not parseable JSON. Resolve so _load_frozen_splits() can read it. Acceptance: 0 errors in TestFCLR010Harness.
3) TRIGGER WATCH: Run ironflow/resume scan probing 2026-11, 2026-12, 2027-01, 2027-02. Document probe_diff, baseline_drift, kaggle_mirror state. Write to research_state/trigger_watch_<UTC>.md. No new data = no forward run; record evidence and continue watch.
4) STRUCTURAL INTEGRITY: Verify no duplicate/stale handoff files, no unreconciled registries, sealed holdouts untouched. Confirm research_state/structural_closure_verdict_heavy.md remains unchanged.
5) PREREG READINESS: Confirm scripts/fclr010_harness.py pre_register_forward_experiment() and evaluate_forward() are intact and require prereg + frozen config. If a trigger appears in step 3, pre-register fresh FCLR-012 experiment BEFORE inspecting outcomes; then run evaluate_forward().
6) IF NO TRIGGER: Ship one verifiable artifact (manifest fix + trigger watch evidence + integrity report). Do not mark session complete without an artifact.

FAILURE = merge tracks / retune / re-run sealed / status-only / fabricate data / wait-for-data without shipping heavy work / ignore manifest LFS bottleneck.
```

## 1) Bottlenecks removed (this session)
- Duplicate NEXT_AGENT_HANDOFF_*.md: NONE (only AGENT_HANDOFF.md remains).
- Stale handoffs: cleaned.
- FCLR-NEXT-013 heavy-work campaign: ALL COMPLETE (recompute_fclr010_20261103T140815Z.md, recompute_fclr011_20261103T140832Z.md, leakage_audit_heavy_20261103T140910Z.md, source_probe_heavy_tracka_20261103T140935Z.md, evaluation_summary_heavy_regime_20261103T140953Z.md).
- Structural closure verdict: COMPLETE (research_state/structural_closure_verdict_heavy.md, 2026-10-31).

## 2) Bottlenecks still open (must be addressed)
- run_manifest.json Git LFS pointer (129 bytes) → 4 errors in TestFCLR010Harness (test_frozen_config_loaded, test_gates, test_split_boundaries_frozen, test_bootstrap_reps). _load_frozen_splits() cannot parse LFS pointer as JSON. THIS IS THE PRIMARY BLOCKER.
- pytest not installed; unittest is the available runner (117 tests, 4 errors all from manifest LFS issue).

## 3) Verified state (tests/evidence)
- tests (unittest): 117 ran, 4 errors (all TestFCLR010Harness manifest LFS), rest PASS (2026-11-03T16:49:16Z).
- Structural closure: Track C CLOSED NEGATIVE (FCLR-003 C2 vs B1 +0.015205 QLIKE, CI crosses zero, -3.78%); Track A STRUCTURALLY BLOCKED NO-GO; Track B CLOSED NEGATIVE. H001 NOT_SUPPORTED. Risk overlay INELIGIBLE.
- Track A latest: research_state/data_cache/ironflow_events/2026-10.parquet (no >2026-10-31).
- Track V: sealed 2026-05-08..2026-08-06 only; root has 2024 zips only.
- Forward FCLR-NEXT-012: BLOCKED (blockers_FCLR-012_20261103T140313Z.md).
- Ironflow trigger watch (20261103T164916Z): no new data; data_through=2026-10; baseline_drift intact, regressions=0.

## 4) Key artifacts
- research_state/structural_closure_verdict_heavy.md (structural closeout)
- research_state/final_confirmatory_verdict.md (H001 NOT_SUPPORTED)
- research_state/gate_assessment.md (forecast gate NOT_MET)
- research_state/recompute_fclr010_20261103T140815Z.md (heavy work complete)
- research_state/recompute_fclr011_20261103T140832Z.md (heavy work complete)
- research_state/leakage_audit_heavy_20261103T140910Z.md (heavy work complete)
- research_state/source_probe_heavy_tracka_20261103T140935Z.md (heavy work complete)
- research_state/evaluation_summary_heavy_regime_20261103T140953Z.md (heavy work complete)
- research_state/run_manifest.json (Git LFS pointer — NEEDS FIX)
- research_state/experiment_frontier.json (FCLR-012 present)
- scripts/fclr010_harness.py (hardened; pre_register_forward_experiment + evaluate_forward)
- research_state/blockers_FCLR-012_20261103T140313Z.md (concrete blocker with evidence)
- research_state/sealed_holdout_integrity.md (preserved, no reuse)

## 5) Frozen rules (immutable)
- Pre-register before inspecting outcomes
- Freeze splits/metrics/gates
- Embargo >=7d, block-bootstrap >=2000 reps
- No tuning on holdout/test, never reuse sealed holdouts
- Separate experiments, immutable cross-track firewall (no Binance<->Hyperliquid merge)
- Overlay HYPOTHETICAL_ONLY, no live/paper trading
- Heavy work only - no status-only files

## 6) Next focus campaign (heavy work, no new data required unless trigger fires)
Campaign: FCLR-NEXT-014-DATA-TRIGGERED-REOPEN-WATCH — ship one verifiable artifact per session.
1) Fix run_manifest.json Git LFS pointer bottleneck so TestFCLR010Harness passes (0 errors).
2) Continuous admissible-data trigger watch (ironflow > 2026-10-31; new unsealed Binance panel).
3) Structural integrity preservation (no duplicate/stale handoffs, sealed holdouts untouched).
4) Pre-registration readiness for immediate forward experiment launch on trigger.

**NEXT AGENT: ALL CONFIRMATORY CAMPAIGNS STRUCTURALLY CLOSED NEGATIVE. FCLR-NEXT-012 FORWARD VALIDATION BLOCKED ON DATA — DO NOT WAIT. EXECUTE FCLR-NEXT-014 WATCH: FIX MANIFEST LFS BOTTLENECK, RUN TRIGGER WATCH, PRESERVE STRUCTURAL INTEGRITY, SHIP ONE VERIFIABLE ARTIFACT. IF NEW ADMISSIBLE DATA APPEARS, PRE-REGISTER BEFORE INSPECTING OUTCOMES. NO DEVIATION.**
