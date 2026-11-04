# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T000101Z
Git SHA (HEAD): 89c84064
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T000101Z | Priority: HEAVY-WORK (FORCED) | Mode: TRACK-C-PRIORITIZED-TRIGGER-LOCKDOWN

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (copy/paste as first action)
```
TASK ID: FCLR-NEXT-022-TRACK-C-FUNDING-VOL-TRIGGER-HARDENING-LOCKDOWN
PRIORITY: P0 - HEAVY WORK ENFORCED (no status-only, no idle waiting, no deferring)
CAMPAIGN: FCLR-NEXT-022-FUNDING-CONDITIONED-VOL-CONTINUOUS-EXECUTION-READINESS
REPO-NAME PRIORITY ORDER: Track C (funding-conditioned volatility) >> Track A (liquidation risk observed labels) >> Track B (modeled boundary breaches)
TIMESTAMP (UTC): 20261104T000101Z
OBJECTIVE: All confirmatory campaigns are STRUCTURALLY CLOSED NEGATIVE. Tests: 117/117 OK. FCLR-NEXT-012 forward validation remains BLOCKED pending admissible new data (no ironflow > 2026-10-31; no unsealed 2026 Binance panel beyond sealed window 2026-05-08..2026-08-06). Treat the repo name as directive: maximize Track C readiness and build an execution path that can fire the moment a trigger appears. Do NOT idle. Every session must ship one verifiable heavy artifact.
HEAVY WORK MANDATE (NON-NEGOTIABLE, ALL FIVE EACH SESSION):
(1) Full inventory hardening: ironflow >2026-10-31 at research_state/data_cache/ironflow_events/; full Binance inventory vs sealed window 2026-05-08..2026-08-06 across BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT klines/index/mark/premium/funding zips.
(2) Prereg-first gating proof every session: dry-run scripts/fclr010_harness.py evaluate_forward without prereg -> must fail with explicit error; log exact error.
(3) Track C prereg template maintain/validate under research_state/readiness/ (structure only, NO outcome inspection, NO tuning).
(4) Immutable cross-track firewall + sealed holdout integrity sweep: verify sealed_holdout_integrity.md, structural_closure_verdict_heavy.md, cross_track_decision_firewall.md, experiment_frontier.json, run_manifest.json unchanged.
(5) Ship ONE verifiable heavy artifact (trigger_harden_<UTC>.json) with diffs + inventory + gating proof + Track-C readiness. Do not end session without it.
ADMISSIBLE TRIGGERS (forward FCLR-NEXT-012):
- Track A: new Hyperliquid ironflow monthly parquet > 2026-10-31
- Track V: new unsealed 2026 Binance panel beyond 2026-05-08..2026-08-06
MANDATORY ACTION SEQUENCE:
1) VERIFY: python -m unittest discover -s tests -v (expect 117 OK)
2) FULL INVENTORY: enumerate root zips + ironflow
3) PREREG GATING PROOF: dry-run evaluate_forward without prereg -> BLOCKED with explicit error
4) TRACK C READINESS: maintain track_c_prereg_template_fclr012_draft.json (structure only)
5) INTEGRITY SWEEP: verify seals/firewall/manifests
6) SHIP HEAVY ARTIFACT: write trigger_harden_<UTC>.json
```

## 1) Bottlenecks removed (this session)
- Tests re-verified: 117/117 OK
- Inventory hardened (root + ironflow + Binance zips)
- Prereg gating explicitly proven (evaluate_forward without prereg -> BLOCKED)
- Track C prereg template maintained (structure only)
- Integrity sweep performed
- Single heavy artifact shipped

## 2) Bottlenecks still open
- Forward validation FCLR-NEXT-012: BLOCKED on admissible data (no ironflow > 2026-10-31; no unsealed 2026 Binance panel beyond sealed window)
- Must re-verify gating + inventory + integrity each session

## 3) Verified state (this session)
- Tests: 117/117 OK
- Ironflow latest: 2026-10.parquet (no > 2026-10-31)
- Root zips: 463 total, 0 zips in 2026
- Sealed window: 2026-05-08..2026-08-06 only
- Prereg gating: BLOCKED without prereg with explicit error
- Integrity: all seals/firewall/manifests present
- Artifact: research_state/watch/trigger_harden_20261104T000101Z.json
- Track C prereg template: research_state/readiness/track_c_prereg_template_fclr012_draft.json

## 4) Next focus campaign
FCLR-NEXT-022-TRACK-C-FUNDING-VOL-TRIGGER-HARDENING - harden watch, prove prereg gating, integrity sweep, maintain Track C readiness, ship heavy artifact each session. On trigger, pre-register BEFORE inspecting outcomes and run frozen config only.
