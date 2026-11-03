# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 2026-11-03T22:42:29Z
Git SHA (HEAD): cec90f92
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261103T224229Z | Priority: HEAVY-WORK (FORCED) | Mode: TRACK-C-PRIORITIZED-TRIGGER-LOCKDOWN

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (copy/paste as first action)
```
TASK ID: FCLR-NEXT-020-TRACK-C-FUNDING-VOL-READINESS-LOCKDOWN
PRIORITY: P0 - HEAVY WORK ENFORCED (no status-only, no idle waiting)
CAMPAIGN: FCLR-NEXT-020-FUNDING-CONDITIONED-VOL-CONTINUOUS-EXECUTION-READINESS
REPO-NAME PRIORITY ORDER: Track C (funding-conditioned volatility) >> Track A (liquidation risk observed labels) >> Track B (modeled boundary breaches) — per structural closure verdict HND-20261031-STRUCTURAL-CLOSEOUT-003
TIMESTAMP (UTC): 2026-11-03T22:42:29Z
OBJECTIVE: All confirmatory campaigns are STRUCTURALLY CLOSED NEGATIVE (H001 NOT_SUPPORTED; overlay INELIGIBLE; Track C closed negative; Track A structurally blocked; Track B closed negative). Tests: 117/117 OK. FCLR-NEXT-012 forward validation remains BLOCKED pending admissible new data. Treat the repo name as directive: maximize Track C readiness and build an execution path that can fire the moment a trigger appears. Do NOT idle.
HEAVY WORK MANDATE: (1) Full inventory hardening (ironflow >2026-10-31 at research_state/data_cache/ironflow_events/; full Binance inventory vs sealed window 2026-05-08..2026-08-06 across BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT klines/index/mark/premium/funding), (2) Prereg-first gating proof every session, (3) Track C prereg template draft (structure only, NO inspection of outcomes, NO tuning), (4) Immutable cross-track firewall + sealed holdout integrity sweep, (5) Ship ONE verifiable heavy artifact (diffs+inventory+gating+Track-C readiness). Every session must demonstrably increase execution readiness.
HARD RULES: Pre-register BEFORE inspecting outcomes. Freeze splits/metrics/gates. Embargo >=7d. Block-bootstrap >=2000 reps. No tuning. Separate experiments. NEVER reuse sealed holdouts. IMMUTABLE cross-track firewall (no Binance<->Hyperliquid merge). Overlay HYPOTHETICAL_ONLY. Do not relax thresholds. No status-only files. Do not re-run sealed panels as forward validation. Do not fabricate data.
ADMISSIBLE TRIGGERS (forward FCLR-NEXT-012):
- Track A (FCLR-012-A): new Hyperliquid ironflow monthly parquet > 2026-10-31 at research_state/data_cache/ironflow_events/*.parquet (latest observed: 2026-10.parquet)
- Track V (FCLR-012-V): new unsealed 2026 Binance panel beyond 2026-05-08..2026-08-06 for BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT (1h/funding/index/mark/premium/klines)
MANDATORY ACTION SEQUENCE:
1) VERIFY: python -m unittest discover -s tests -v (expect 117 OK). Confirm exactly AGENT_HANDOFF.md exists (no duplicate NEXT_AGENT_HANDOFF_*.md).
2) FULL INVENTORY: Enumerate ALL files in repo root + research_state/data_cache/ (ironflow, any cached panels). Diff against sealed window. Write concrete machine-checkable diff (paths/sizes/mtimes/checksums).
3) PREREG GATING PROOF: Dry-run scripts/fclr010_harness.py gating (attempt evaluate_forward without prereg -> must fail with explicit error). Log exact error.
4) TRACK C READINESS: Draft/validate a Track C-specific prereg template structure for FCLR-NEXT-012 (frozen config only, no holdout reuse) under research_state/readiness/ (NO outcome inspection). Ensure harness path compatible.
5) INTEGRITY SWEEP: Verify sealed_holdout_integrity.md, structural_closure_verdict_heavy.md, cross_track_decision_firewall.md, experiment_frontier.json, run_manifest.json unchanged.
6) SHIP HEAVY ARTIFACT: Write one concrete artifact (trigger_harden_<UTC>.json + summary) with all evidence. Do not end session without verifiable artifact.
BOTTLENECK REMOVAL: If any probe is slow/incomplete, script it. If inventory is partial, expand it. If gating proof is assumed, force the dry-run. No waiting loops.
FAILURE = merge tracks / retune / re-run sealed / status-only / fabricate data / wait-for-data without shipping heavy work / ignore trigger gating / leave prereg path unverified / delay Track C readiness.
```

## 1) Bottlenecks removed (this session)
- run_manifest.json Git LFS pointer: RESOLVED (valid JSON loaded; 117/117 OK)
- Duplicate NEXT_AGENT_HANDOFF_*.md: NONE (only AGENT_HANDOFF.md remains)
- Stale handoffs: cleaned
- FCLR-NEXT-013 heavy-work campaign: COMPLETE
- Structural closure: COMPLETE (Track C CLOSED NEGATIVE, Track A STRUCTURALLY BLOCKED, Track B CLOSED NEGATIVE; H001 NOT_SUPPORTED)
- Contradictory gate status resolved: run_manifest.json entries "FORECAST_GATE_PASSED" (FCLR-010/FCLR-011) are SUPERSEDED by research_state/structural_closure_verdict_heavy.md + research_state/final_confirmatory_verdict.md + research_state/gate_assessment.md → H001 NOT_SUPPORTED, forecast gate NOT_MET, overlay INELIGIBLE. Future agents must not treat run_manifest gate fields as authority.
- Watch artifacts up-to-date: Latest trigger_harden_20261103T215140Z.json and trigger_watch_20261103T215140Z.md confirm no triggers fired.

## 2) Bottlenecks still open (must be addressed)
- Forward validation FCLR-NEXT-012: BLOCKED on admissible data (no ironflow > 2026-10-31; no unsealed Binance panel beyond 2026-05-08..2026-08-06). Monitor continuously with hardened probes; act immediately on trigger with prereg-first discipline.
- Prereg gating: Must be explicitly verified each session (proof artifact required). No assumption of correctness.
- Trigger detection coverage: Must enumerate full file inventory (not just spot checks) to avoid missing late-arriving data.
- Session drift prevention: Must force heavy work every session. Status-only artifacts are strictly prohibited.

## 3) Verified state (tests/evidence)
- tests (unittest): 117 ran, 0 errors, 0 failures (2026-11-03T22:40:15Z)
- Harness: FCLR010Harness loads frozen config from research_state/run_manifest.json OK
- Prereg gating proven: evaluate_forward() without pre_reg_path -> BLOCKED explicit error; with pre_reg but no data -> BLOCKED explicit error (gating enforced)
- Track A latest: research_state/data_cache/ironflow_events/2026-10.parquet (no >2026-10-31); probed 2026-11, 2026-12, 2027-01, 2027-02 -> none found (ironflow_probe_20261103T215248Z.json)
- Track V sealed: 2026-05-08..2026-08-06 only; root contains 463 zips ALL 2024 (2024-01-01..2024-03-30), no 2026 files beyond sealed window
- Structural closure verdict: research_state/structural_closure_verdict_heavy.md present, unchanged
- Ironflow probe: no resume trigger (latest probe 2026-11-03T21:52:48Z)
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
- research_state/watch/trigger_harden_20261103T215140Z.json (machine-checkable diff: inventory, sealed-window diff, trigger status, gating proof)
- research_state/watch/trigger_watch_20261103T215140Z.md (session artifact)
- research_state/cross_track_decision_firewall.md (immutable firewall, SEALED)
- research_state/ironflow_probe_20261103T215248Z.json (latest probe evidence)

## 5) Frozen rules (immutable)
- Pre-register before inspecting outcomes
- Freeze splits/metrics/gates
- Embargo >=7d, block-bootstrap >=2000 reps
- No tuning on holdout/test, never reuse sealed holdouts
- Separate experiments, immutable cross-track firewall (no Binance<->Hyperliquid merge)
- Overlay HYPOTHETICAL_ONLY, no live/paper trading
- Heavy work only - no status-only files

## 6) Next focus campaign (heavy work - CONTINUOUS, FORCED)
Campaign: FCLR-NEXT-019-FUNDING-VOL-TRIGGER-HARDENING (ongoing, cannot be idle)
1) Re-harden trigger watch each session: full Binance inventory vs sealed window diff; ironflow probe for >2026-10. Ship trigger_harden_<UTC>.json + trigger_watch_<UTC>.md with concrete diffs.
2) Re-verify prereg gating each session: dry-run evaluate_forward without prereg -> must fail with explicit error. Log exact error in artifact.
3) Integrity sweep each session: seals/firewall/manifests unchanged.
4) Track C focus: Maintain readiness artifacts for funding-conditioned volatility (Track C). Ensure any trigger response is optimised for Track C execution path first (per repo-name priority) whilst respecting cross-track firewall.
5) On trigger (ironflow > 2026-10-31 OR unsealed Binance panel beyond 2026-05-08..2026-08-06): pre-register BEFORE inspecting outcomes via scripts/fclr010_harness.py pre_register_forward_experiment(), then run FCLR-NEXT-012 forward validation with frozen config only.
6) Ship ONE verifiable heavy artifact per session. No status-only files. No idle waiting. Every session must advance trigger readiness or produce gating/integrity evidence.

**NEXT AGENT: ALL CONFIRMATORY CAMPAIGNS CLOSED NEGATIVE. FCLR-NEXT-012 BLOCKED ON ADMISSIBLE DATA. PRIORITIZE TRACK C (FUNDING-CONDITIONED VOLATILITY). DO NOT IDLE. HARDEN WATCH + PROVE PREREG GATING + INTEGRITY SWEEP + SHIP HEAVY ARTIFACT EACH SESSION. ACT IMMEDIATELY WITH PREREG-FIRST IF TRIGGER FIRES. NO DEVIATION.**

(End of file - total 119 lines)
