# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 2026-11-03T21:30:15Z
Git SHA (HEAD): 4333efca
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261103T213015Z | Priority: HEAVY-WORK (do not do status-only) | Mode: TRIGGER-WATCH-HARDENED

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (copy/paste as first action)
```
TASK ID: FCLR-NEXT-018-WATCH-HARDEN-AND-EXECUTE-ON-TRIGGER
PRIORITY: P0 - HEAVY WORK ENFORCED (no status-only, no idle waiting)
CAMPAIGN: FCLR-NEXT-018-FCLR-VOL-LIQ-RISK-TRIGGER-HARDENING-AND-READINESS
REPO-NAME PRIORITY ORDER: Track C (funding-conditioned volatility) > Track A (liquidation risk observed labels) > Track B (modeled boundary breaches) — per structural closure verdict HND-20261031-STRUCTURAL-CLOSEOUT-003
TIMESTAMP (UTC): 2026-11-03T21:30:15Z
OBJECTIVE: All confirmatory campaigns STRUCTURALLY CLOSED NEGATIVE (H001 NOT_SUPPORTED; overlay INELIGIBLE; Track C closed negative; Track A structurally blocked; Track B closed negative). Tests: 117/117 OK. FCLR-NEXT-012 forward validation BLOCKED pending admissible new data. DO NOT wait idly. Execute heavy work: (1) Harden continuous admissible-data trigger watch with concrete diffs (ironflow > 2026-10-31 at research_state/data_cache/ironflow_events/; new unsealed Binance panel beyond 2026-05-08..2026-08-06 for BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT across klines/index/mark/premium/funding), (2) Stress-test prereg-first gating end-to-end (prove evaluate_forward() cannot run without preregistration), (3) Maintain immutable cross-track firewall and sealed holdout integrity, (4) Produce ONE verifiable heavy artifact per session (diffs + inventory + gating proof). Every session must increase readiness to run FCLR-NEXT-012 the moment trigger appears.
HARD RULES: Pre-register BEFORE inspecting outcomes. Freeze splits/metrics/gates. Embargo >=7d. Block-bootstrap >=2000 reps. No tuning. Separate experiments. NEVER reuse sealed holdouts. IMMUTABLE cross-track firewall (no Binance<->Hyperliquid merge). Overlay HYPOTHETICAL_ONLY. Do not relax thresholds. No status-only files. Do not re-run sealed panels as forward validation. Do not fabricate data.
ADMISSIBLE TRIGGERS (forward FCLR-NEXT-012):
- Track A (FCLR-012-A): new Hyperliquid ironflow monthly parquet > 2026-10-31 at research_state/data_cache/ironflow_events/*.parquet (latest observed: 2026-10.parquet)
- Track V (FCLR-012-V): new unsealed 2026 Binance panel beyond 2026-05-08..2026-08-06 for BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT (1h/funding/index/mark/premium/klines)
MANDATORY ACTION SEQUENCE:
1) VERIFY: python -m unittest discover -s tests -v (expect 117 OK). Confirm exactly AGENT_HANDOFF.md exists (no duplicate NEXT_AGENT_HANDOFF_*.md).
2) HARDEN WATCH: Enumerate all Binance files (zips/csjs) by symbol/date ranges; diff against sealed window 2026-05-08..2026-08-06. Probe ironflow for 2026-11+. Write research_state/watch/trigger_harden_<UTC>.json with concrete paths/sizes/mtimes and a machine-checkable diff.
3) PREREG GATING PROOF: Dry-run scripts/fclr010_harness.py gating (attempt evaluate_forward without prereg -> must fail with explicit error). Document proof in artifact.
4) INTEGRITY SWEEP: Confirm sealed_holdout_integrity.md, structural_closure_verdict_heavy.md, experiment_frontier.json, run_manifest.json unchanged; firewall intact.
5) SHIP ARTIFACT: Write one concrete heavy artifact under research_state/watch/ or research_state/readiness/ with evidence. Do not end session without verifiable artifact.
FAILURE = merge tracks / retune / re-run sealed / status-only / fabricate data / wait-for-data without shipping heavy work / ignore trigger gating / leave prereg path unverified.
```

## 1) Bottlenecks removed (this session)
- run_manifest.json Git LFS pointer: RESOLVED (valid JSON loaded; 117/117 OK)
- Duplicate NEXT_AGENT_HANDOFF_*.md: NONE (only AGENT_HANDOFF.md remains)
- Stale handoffs: cleaned
- FCLR-NEXT-013 heavy-work campaign: COMPLETE
- Structural closure: COMPLETE (Track C CLOSED NEGATIVE, Track A STRUCTURALLY BLOCKED, Track B CLOSED NEGATIVE; H001 NOT_SUPPORTED)
- **Contradictory gate status resolved**: run_manifest.json entries "FORECAST_GATE_PASSED" (FCLR-010/FCLR-011) are SUPERSEDED by research_state/structural_closure_verdict_heavy.md + research_state/final_confirmatory_verdict.md + research_state/gate_assessment.md → H001 NOT_SUPPORTED, forecast gate NOT_MET, overlay INELIGIBLE. Future agents must not treat run_manifest gate fields as authority; this removes the confusion bottleneck that could reopen sealed confirmatory work.
- Bottleneck review: NO remaining structural/engineering bottlenecks. The only blocker is absence of new admissible unauthenticated data for FCLR-NEXT-012 forward validation; this is a DATA blocker, not an engineering bottleneck. Heavy work (watch hardening, gating proof, integrity sweep) continues regardless.

## 2) Bottlenecks still open (must be addressed)
- Forward validation FCLR-NEXT-012: BLOCKED on admissible data (no ironflow > 2026-10-31; no unsealed Binance panel beyond 2026-05-08..2026-08-06). Monitor continuously with hardened probes; act immediately on trigger with prereg-first discipline.
- Prereg gating: Must be explicitly verified each session (proof artifact required). No assumption of correctness.
- Trigger detection coverage: Must enumerate full file inventory (not just spot checks) to avoid missing late-arriving data.

## 3) Verified state (tests/evidence)
- tests (unittest): 117 ran, 0 errors, 0 failures (2026-11-03T21:30:15Z)
- Harness: FCLR010Harness loads frozen config from research_state/run_manifest.json OK
- Prereg gating proven: evaluate_forward() without pre_reg_path -> BLOCKED explicit error; with pre_reg but no data -> BLOCKED explicit error (gating enforced)
- Track A latest: research_state/data_cache/ironflow_events/2026-10.parquet (no >2026-10-31); probed 2026-11, 2026-12, 2027-01, 2027-02 -> none found (ironflow_probe_20261103T213103Z.json)
- Track V sealed: 2026-05-08..2026-08-06 only; root contains 463 zips ALL 2024 (2024-01-01..2024-03-30), no 2026 files beyond sealed window
- Structural closure verdict: research_state/structural_closure_verdict_heavy.md present, unchanged
- Ironflow probe: no resume trigger (latest probe 2026-11-03T21:30:15Z)
- Cross-track firewall: IMMUTABLE, SEALED (research_state/cross_track_decision_firewall.md)
- Sealed holdout integrity: intact (research_state/sealed_holdout_integrity.md)

## 4) Key artifacts
- research_state/run_manifest.json (valid JSON; frozen; gate fields superseded by structural closure verdict)
- scripts/fclr010_harness.py (pre_register_forward_experiment + evaluate_forward, prereg gating)
- research_state/structural_closure_verdict_heavy.md
- research_state/final_confirmatory_verdict.md
- research_state/gate_assessment.md
- research_state/sealed_holdout_integrity.md
- research_state/experiment_frontier.json
- research_state/watch/trigger_harden_20261103T211306Z.json (machine-checkable diff: inventory, sealed-window diff, trigger status, gating proof)
- research_state/watch/trigger_watch_20261103T210920Z.md (session artifact)
- research_state/cross_track_decision_firewall.md (immutable firewall, SEALED)

## 5) Frozen rules (immutable)
- Pre-register before inspecting outcomes
- Freeze splits/metrics/gates
- Embargo >=7d, block-bootstrap >=2000 reps
- No tuning on holdout/test, never reuse sealed holdouts
- Separate experiments, immutable cross-track firewall (no Binance<->Hyperliquid merge)
- Overlay HYPOTHETICAL_ONLY, no live/paper trading
- Heavy work only - no status-only files

## 6) Next focus campaign (heavy work - CONTINUOUS)
Campaign: FCLR-NEXT-018-TRIGGER-HARDENING (ongoing)
1) Re-harden trigger watch each session: full Binance inventory vs sealed window diff; ironflow probe for >2026-10. Ship trigger_harden_<UTC>.json + trigger_watch_<UTC>.md.
2) Re-verify prereg gating each session: dry-run evaluate_forward without prereg -> must fail with explicit error. Log exact error in artifact.
3) Integrity sweep each session: seals/firewall/manifests unchanged.
4) On trigger (ironflow > 2026-10-31 OR unsealed Binance panel beyond 2026-05-08..2026-08-06): pre-register BEFORE inspecting outcomes via scripts/fclr010_harness.py pre_register_forward_experiment(), then run FCLR-NEXT-012 forward validation with frozen config only.
5) Ship ONE verifiable heavy artifact per session. No status-only files. No idle waiting.

**NEXT AGENT: ALL CONFIRMATORY CAMPAIGNS CLOSED NEGATIVE. FCLR-NEXT-012 BLOCKED ON ADMISSIBLE DATA. DO NOT IDLE. HARDEN WATCH + PROVE PREREG GATING + SHIP HEAVY ARTIFACT EACH SESSION. ACT IMMEDIATELY WITH PREREG-FIRST IF TRIGGER FIRES. NO DEVIATION.**
