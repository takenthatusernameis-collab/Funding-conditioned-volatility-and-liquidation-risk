# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T083841Z
Git SHA (HEAD): 789ae083afd09cdea6d8d8798bfddd9c0c42c5d0
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T083841Z | Priority: P0 - HEAVY-WORK (FORCED) | Mode: TRACK-C-ZERO-LATENCY-CAMPAIGN

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE AS FIRST ACTION)

```text
TASK ID: FCLR-NEXT-042-TRACK-C-ZERO-LATENCY-FORCED
PRIORITY: P0 - HEAVY WORK ENFORCED (NO STATUS-ONLY | NO IDLE WAITING | NO DEFERRAL | NO DOCUMENTATION-ONLY SESSION)
CAMPAIGN: FCLR-NEXT-042-FUNDING-CONDITIONED-VOLATILITY-HEAVY-CONTINUOUS
TIMESTAMP (UTC): 20261104T083841Z

OBJECTIVE: Repo name is binding directive (Funding-conditioned-volatility-and-liquidation-risk). Track C >> Track B >> Track A. Maintain zero-latency readiness for admissible Track C trigger. NO admissible triggers now (root all-2024 zips 463; all 2026 zips zero-volume synthetic placeholders; ironflow 2026-10.parquet is Track-A only). Trigger definition: NEW admissible unauthenticated 2026 Binance panel beyond sealed FCLR-011 test window 2026-05-08..2026-08-06, for BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT (1h klines + markPriceKlines + indexPriceKlines + premiumIndexKlines + fundingRate), NON-ZERO volume/taker_buy, schema valid.

HEAVY WORK MANDATE (EXECUTE ALL 5 EVERY SESSION — NO EXCEPTION, NO IDLE):
(1) FULL INVENTORY HARDENING - enumerate root zips, scan data_cache/ironflow_events, diff vs latest trigger_harden_*.json, write successor trigger_harden_<UTC>.json
(2) PREREG GATING PROOF - evaluate_forward without prereg MUST return BLOCKED with explicit reason; capture output
(3) TRACK C READINESS - validate track_c_prereg_template_fclr012.json structure-only, trigger NOT_FIRED
(4) INTEGRITY SWEEP - hash firewall/seals/manifests; verify sealed FCLR-001/002/003/006/007/008/011 untouched; .github/workflows untouched
(5) TRIGGER ALERTING + ACTIONABLE ARTIFACT - write trigger_harden_<UTC>.json with diffs, gating proof, readiness, hashes, IF-TRIGGER-FIRES-NOW, next_runnable_commands

RULES: tests>=117 green; prereg BEFORE outcomes; block bootstrap>=2000 seed12345; Holm across family; no re-run sealed; structure-only for readiness; delete noise (__pycache__, *.pyc, ironflow_probe_*, duplicate trigger_harden_*, blocker files).
```

## 1) Current State (Verified 20261104T083841Z)
- Tests: 117/117 OK (python -m unittest discover -s tests -v)
- Git HEAD: 789ae083afd09cdea6d8d8798bfddd9c0c42c5d0 (main)
- Latest heavy artifact: research_state/watch/trigger_harden_20261104T083332Z.json
- Inventory: 463 root zips (all 2024). Ironflow has 2026-10.parquet (Track-A only). No admissible Track C trigger.
- Prereg gating enforced (evaluate_forward without prereg returns BLOCKED with explicit reason)
- Track C template: research_state/readiness/track_c_prereg_template_fclr012.json (STRUCTURE_ONLY_NO_OUTCOME_INSPECTION, trigger NOT_FIRED)
- Sealed experiments untouched; .github/workflows untouched
- Bottlenecks removed: __pycache__ directories and *.pyc noise deleted; ironflow_probe noise deleted this session

## 2) Immediate Next Actions
1) python -m unittest discover -s tests -v   (must be 117 OK)
2) python scripts/track_c_inventory_harden.py
3) Capture gating proof (expect BLOCKED with explicit prereg reason)
4) Validate track_c_prereg_template_fclr012.json (structure-only, NOT_FIRED)
5) Integrity sweep + verify sealed/firewall (sha256sum on sealed docs; git status --short .github/workflows)
6) Write successor trigger_harden_<UTC>.json
7) Delete noise: scripts/__pycache__/, tests/__pycache__/, src/**/__pycache__/, *.pyc, research_state/ironflow_probe_*

## 3) Bottleneck Removal (Done This Session)
- Deleted scripts/__pycache__/*, tests/__pycache__/*, src/**/__pycache__/* and all *.pyc files (git status showed modified/deleted noise)
- Deleted research_state/ironflow_probe_20261104T083242Z.json (probe noise artifact)
- No session idle: heavy work mandate executes every session regardless of trigger state

## 4) Definition of Done
New trigger_harden_<UTC>.json with all required sections, tests>=117, no workflow changes, no sealed touched, no new noise files, __pycache__ and ironflow_probe artifacts absent, prereg gating proof captured, Track C readiness NOT_FIRED documented.
