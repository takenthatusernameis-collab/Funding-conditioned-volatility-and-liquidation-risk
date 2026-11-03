# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 2026-11-03T17:55:00Z
Git SHA (HEAD): 385a1073
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261103T175500Z | Priority: HEAVY-WORK (do not do status-only) | Mode: TRIGGER-WATCH-HARDENED

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (copy/paste as first action)
```
TASK ID: FCLR-NEXT-016-WATCH-HARDEN
PRIORITY: P0 - HEAVY WORK ENFORCED (no status-only, no idle waiting)
CAMPAIGN: FCLR-NEXT-016-FUNDING-CONDITIONED-VOL-LIQ-RISK-TRIGGER-HARDENING
REPO FOCUS: Funding-conditioned volatility and liquidation risk (Track A = Hyperliquid ironflow observed liquidation labels; Track C = funding-conditioned volatility on Binance perpetual panel; Track B = modeled boundary breaches)
TIMESTAMP (UTC): 2026-11-03T17:55:00Z
OBJECTIVE: All confirmatory campaigns STRUCTURALLY CLOSED NEGATIVE (H001 NOT_SUPPORTED; overlay INELIGIBLE; Track A structurally blocked; Track B closed negative). Tests: 117/117 OK. FCLR-NEXT-012 forward validation BLOCKED pending admissible new data. DO NOT wait idly. Execute heavy work: (1) Harden continuous admissible-data trigger watch with concrete diffs (ironflow > 2026-10-31 at research_state/data_cache/ironflow_events/; new unsealed Binance panel beyond 2026-05-08..2026-08-06 for BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT across klines/index/mark/premium/funding), (2) Stress-test prereg-first gating end-to-end (prove evaluate_forward() cannot run without preregistration), (3) Maintain immutable cross-track firewall and sealed holdout integrity, (4) Produce ONE verifiable heavy artifact per session (diffs + inventory + gating proof). Every session must increase readiness to run FCLR-012 the moment trigger appears.
HARD RULES: Pre-register BEFORE inspecting outcomes. Freeze splits/metrics/gates. Embargo >=7d. Block-bootstrap >=2000 reps. No tuning. Separate experiments. NEVER reuse sealed holdouts. IMMUTABLE cross-track firewall (no Binance<->Hyperliquid merge). Overlay HYPOTHETICAL_ONLY. Do not relax thresholds. No status-only files. Do not re-run sealed panels as forward validation. Do not fabricate data.
ADMISSIBLE TRIGGERS (forward FCLR-NEXT-012):
- Track A (FCLR-012-A): new Hyperliquid ironflow monthly parquet > 2026-10-31 at research_state/data_cache/ironflow_events/*.parquet (latest observed: 2026-10.parquet)
- Track V (FCLR-012-V): new unsealed 2026 Binance panel beyond 2026-05-08..2026-08-06 for BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT (1h/funding/index/mark/premium/klines)
MANDATORY ACTION SEQUENCE:
1) VERIFY: python -m unittest discover -s tests -v (expect 117 OK). Confirm exactly AGENT_HANDOFF.md exists (no duplicate NEXT_AGENT_HANDOFF_*.md).
2) HARDEN WATCH: Enumerate all Binance files (zips/csvs) by symbol/date ranges; diff against sealed window 2026-05-08..2026-08-06. Probe ironflow for 2026-11+. Write research_state/watch/trigger_harden_<UTC>.json with concrete paths/sizes/mtimes and a machine-checkable diff.
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

## 2) Bottlenecks still open (must be addressed)
- Forward validation FCLR-NEXT-012: BLOCKED on admissible data (no ironflow > 2026-10-31; no unsealed Binance panel beyond 2026-05-08..2026-08-06). Monitor continuously with hardened probes; act immediately on trigger with prereg-first discipline.
- Prereg gating: Must be explicitly verified each session (proof artifact required). No assumption of correctness.
- Trigger detection coverage: Must enumerate full file inventory (not just spot checks) to avoid missing late-arriving data.

## 3) Verified state (tests/evidence)
- tests (unittest): 117 ran, 0 errors, 0 failures (2026-11-03T17:51:16Z)
- Harness: FCLR010Harness loads frozen config from research_state/run_manifest.json OK
- Track A latest: research_state/data_cache/ironflow_events/2026-10.parquet (no >2026-10-31)
- Track V sealed: 2026-05-08..2026-08-06 only (root contains 2024 zips only)
- Structural closure verdict: research_state/structural_closure_verdict_heavy.md present
- Ironflow probe: no resume trigger (latest probe 2026-11-03T17:51:16Z)

## 4) Key artifacts
- research_state/run_manifest.json (valid JSON; frozen)
- scripts/fclr010_harness.py (pre_register_forward_experiment + evaluate_forward, prereg gating)
- research_state/structural_closure_verdict_heavy.md
- research_state/final_confirmatory_verdict.md
- research_state/gate_assessment.md
- research_state/blockers_FCLR-012_20261103T140313Z.md
- research_state/sealed_holdout_integrity.md
- research_state/experiment_frontier.json

## 5) Frozen rules (immutable)
- Pre-register before inspecting outcomes
- Freeze splits/metrics/gates
- Embargo >=7d, block-bootstrap >=2000 reps
- No tuning on holdout/test, never reuse sealed holdouts
- Separate experiments, immutable cross-track firewall (no Binance<->Hyperliquid merge)
- Overlay HYPOTHETICAL_ONLY, no live/paper trading
- Heavy work only - no status-only files

## 6) Next focus campaign (heavy work)
Campaign: FCLR-NEXT-016-TRIGGER-HARDENING
1) Harden trigger watch: full inventory of all Binance files vs sealed window with diffs (paths/sizes/mtimes); ironflow probe for >2026-10. Machine-checkable evidence required.
2) Prereg gating proof: deterministic dry-run showing evaluate_forward blocked without preregistration; log exact error.
3) Integrity sweep: re-verify seals/firewall/manifests unchanged.
4) Ship heavy artifact per session: concrete diffs + proof + readiness. No status summaries alone.

**NEXT AGENT: ALL CONFIRMATORY CAMPAIGNS CLOSED NEGATIVE. FCLR-NEXT-012 BLOCKED ON ADMISSIBLE DATA. DO NOT IDLE. HARDEN WATCH + PROVE PREREG GATING + SHIP HEAVY ARTIFACT. ACT IMMEDIATELY WITH PREREG-FIRST IF TRIGGER FIRES. NO DEVIATION.**
