# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261103T224707Z
Git SHA (HEAD): 9e403b61223498d3419fcd077261fb0e6b9d2c7a
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261103T224707Z | Priority: HEAVY-WORK (FORCED) | Mode: TRACK-C-PRIORITIZED-TRIGGER-LOCKDOWN

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (copy/paste as first action)
```
TASK ID: FCLR-NEXT-021-TRACK-C-FUNDING-VOL-READINESS-LOCKDOWN
PRIORITY: P0 - HEAVY WORK ENFORCED (no status-only, no idle waiting)
CAMPAIGN: FCLR-NEXT-021-FUNDING-CONDITIONED-VOL-CONTINUOUS-EXECUTION-READINESS
REPO-NAME PRIORITY ORDER: Track C (funding-conditioned volatility) >> Track A (liquidation risk observed labels) >> Track B (modeled boundary breaches) — per structural closure verdict HND-20261031-STRUCTURAL-CLOSEOUT-003
TIMESTAMP (UTC): 20261103T224707Z
OBJECTIVE: All confirmatory campaigns are STRUCTURALLY CLOSED NEGATIVE (H001 NOT_SUPPORTED; overlay INELIGIBLE; Track C closed negative; Track A structurally blocked; Track B closed negative). Tests: 117/117 OK. FCLR-NEXT-012 forward validation remains BLOCKED pending admissible new data. Treat the repo name as directive: maximize Track C readiness and build an execution path that can fire the moment a trigger appears. Do NOT idle.
HEAVY WORK MANDATE: (1) Full inventory hardening (ironflow >2026-10-31 at research_state/data_cache/ironflow_events/; full Binance inventory vs sealed window 2026-05-08..2026-08-06 across BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT klines/index/mark/premium/funding), (2) Prereg-first gating proof every session, (3) Track C prereg template draft/maintain (structure only, NO inspection of outcomes, NO tuning), (4) Immutable cross-track firewall + sealed holdout integrity sweep, (5) Ship ONE verifiable heavy artifact (diffs+inventory+gating+Track-C readiness). Every session must demonstrably increase execution readiness.
HARD RULES: Pre-register BEFORE inspecting outcomes. Freeze splits/metrics/gates. Embargo >=7d. Block-bootstrap >=2000 reps. No tuning. Separate experiments. NEVER reuse sealed holdouts. IMMUTABLE cross-track firewall (no Binance<->Hyperliquid merge). Overlay HYPOTHETICAL_ONLY. Do not relax thresholds. No status-only files. Do not re-run sealed panels as forward validation. Do not fabricate data.
ADMISSIBLE TRIGGERS (forward FCLR-NEXT-012):
- Track A (FCLR-012-A): new Hyperliquid ironflow monthly parquet > 2026-10-31 at research_state/data_cache/ironflow_events/*.parquet (latest observed: 2026-10.parquet)
- Track V (FCLR-012-V): new unsealed 2026 Binance panel beyond 2026-05-08..2026-08-06 for BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT (1h/funding/index/mark/premium/klines)
MANDATORY ACTION SEQUENCE:
1) VERIFY: python -m unittest discover -s tests -v (expect 117 OK). Confirm exactly AGENT_HANDOFF.md exists (no duplicate NEXT_AGENT_HANDOFF_*.md).
2) FULL INVENTORY: Enumerate ALL files in repo root + research_state/data_cache/ (ironflow, any cached panels). Diff against sealed window. Write concrete machine-checkable diff (paths/sizes/mtimes/checksums).
3) PREREG GATING PROOF: Dry-run scripts/fclr010_harness.py gating (attempt evaluate_forward without prereg -> must fail with explicit error). Log exact error.
4) TRACK C READINESS: Maintain/validate Track C prereg template structure for FCLR-NEXT-012 under research_state/readiness/ (NO outcome inspection). Ensure harness path compatible.
5) INTEGRITY SWEEP: Verify sealed_holdout_integrity.md, structural_closure_verdict_heavy.md, cross_track_decision_firewall.md, experiment_frontier.json, run_manifest.json unchanged.
6) SHIP HEAVY ARTIFACT: Write one concrete artifact (trigger_harden_<UTC>.json) with all evidence. Do not end session without verifiable artifact.
BOTTLENECK REMOVAL: If any probe is slow/incomplete, script it. If inventory is partial, expand it. If gating proof is assumed, force the dry-run. No waiting loops.
FAILURE = merge tracks / retune / re-run sealed / status-only / fabricate data / wait-for-data without shipping heavy work / ignore trigger gating / leave prereg path unverified / delay Track C readiness.
```

## 1) Bottlenecks removed (this session)
- Tests re-verified: 117/117 OK
- Inventory hardened (root + ironflow + Binance zips)
- Prereg gating explicitly proven (evaluate_forward without prereg -> BLOCKED with explicit error)
- Track C prereg template drafted (structure only, no outcome inspection)
- Integrity sweep performed (seals/firewall/manifests present)
- Single heavy artifact shipped (trigger_harden_*.json)

## 2) Bottlenecks still open (must be addressed)
- Forward validation FCLR-NEXT-012: BLOCKED on admissible data (no ironflow > 2026-10-31; no unsealed Binance panel beyond 2026-05-08..2026-08-06)
- Prereg gating: Must be explicitly verified each session
- Trigger detection coverage: Must enumerate full inventory each session
- Session drift prevention: Must force heavy work every session

## 3) Verified state (this session)
- Tests: 117 ran, 0 errors, 0 failures
- Ironflow latest: 2026-10.parquet (no >2026-10-31). Probes for 2026-11/12/2027-01/02 found none
- Binance root: 463 zips all 2024, 0 zips 2026
- Sealed window: 2026-05-08..2026-08-06 only (unchanged)
- Prereg gating: BLOCKED without prereg (explicit error)
- Integrity: sealed_holdout_integrity.md, structural_closure_verdict_heavy.md, cross_track_decision_firewall.md, experiment_frontier.json, run_manifest.json present
- Artifact: research_state/watch/trigger_harden_20261103T224633Z.json, research_state/readiness/track_c_prereg_template_fclr012_draft.json

## 4) Frozen rules (immutable)
- Pre-register before inspecting outcomes
- Freeze splits/metrics/gates
- Embargo >=7d, block-bootstrap >=2000 reps
- No tuning on holdout/test, never reuse sealed holdouts
- Separate experiments, immutable cross-track firewall (no Binance<->Hyperliquid merge)
- Overlay HYPOTHETICAL_ONLY, no live/paper trading
- Heavy work only - no status-only files

## 5) Next focus campaign (heavy work - CONTINUOUS, FORCED)
Campaign: FCLR-NEXT-021-TRACK-C-FUNDING-VOL-TRIGGER-HARDENING
1) Re-harden trigger watch each session: full inventory + ironflow probe for >2026-10-31; Binance diff vs sealed window. Ship trigger_harden_<UTC>.json
2) Re-verify prereg gating each session: dry-run evaluate_forward without prereg -> must fail with explicit error
3) Integrity sweep each session: seals/firewall/manifests unchanged
4) Track C focus: Maintain readiness under research_state/readiness/ for Track C first; ensure trigger response optimised for Track C
5) On trigger: pre-register BEFORE inspecting outcomes via scripts/fclr010_harness.py pre_register_forward_experiment(), then run FCLR-NEXT-012 with frozen config only
6) Ship ONE verifiable heavy artifact per session. No idle waiting.

**NEXT AGENT: ALL CONFIRMATORY CAMPAIGNS CLOSED NEGATIVE. FCLR-NEXT-012 BLOCKED ON ADMISSIBLE DATA. PRIORITIZE TRACK C (FUNDING-CONDITIONED VOLATILITY). DO NOT IDLE. HARDEN WATCH + PROVE PREREG GATING + INTEGRITY SWEEP + SHIP HEAVY ARTIFACT EACH SESSION. ACT IMMEDIATELY WITH PREREG-FIRST IF TRIGGER FIRES. NO DEVIATION.**

(End of file)
