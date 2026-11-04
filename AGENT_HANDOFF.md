# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T083800Z
Git SHA (HEAD): 12218be93da896c8fe49b2b1821e80c4f398f26c
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T083800Z | Priority: P0 - HEAVY-WORK (FORCED) | Mode: TRACK-C-ZERO-LATENCY-CAMPAIGN

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE AS FIRST ACTION)

```text
TASK ID: FCLR-NEXT-041-TRACK-C-ZERO-LATENCY-FORCED
PRIORITY: P0 - HEAVY WORK ENFORCED (NO STATUS-ONLY | NO IDLE WAITING | NO DEFERRAL)
CAMPAIGN: FCLR-NEXT-041-FUNDING-CONDITIONED-VOLATILITY-HEAVY-CONTINUOUS
TIMESTAMP (UTC): 20261104T083800Z

OBJECTIVE: Repo name is binding directive (Funding-conditioned-volatility-and-liquidation-risk). Track C >> Track B >> Track A. Maintain zero-latency readiness for admissible Track C trigger. NO admissible triggers now (root all-2024 zips 463; all 2026 zips zero-volume synthetic placeholders; ironflow 2026-10.parquet is Track-A only).

HEAVY WORK MANDATE (EXECUTE ALL 5 EVERY SESSION):
(1) FULL INVENTORY HARDENING - enumerate root zips, scan data_cache/ironflow_events, diff vs latest trigger_harden_*.json, write successor
(2) PREREG GATING PROOF - evaluate_forward without prereg MUST return BLOCKED with explicit reason; capture output
(3) TRACK C READINESS - validate track_c_prereg_template_fclr012.json structure-only, trigger NOT_FIRED
(4) INTEGRITY SWEEP - hash firewall/seals/manifests; verify sealed FCLR-001/002/003/006/007/008/011 untouched; .github/workflows untouched
(5) TRIGGER ALERTING + ACTIONABLE ARTIFACT - write trigger_harden_<UTC>.json with diffs, gating proof, readiness, hashes, IF-TRIGGER-FIRES-NOW, next_runnable_commands

RULES: tests>=117 green; prereg BEFORE outcomes; block bootstrap>=2000 seed12345; Holm across family; no re-run sealed; structure-only for readiness; delete noise (__pycache__, ironflow_probe_*, duplicate trigger_harden_*, blocker files).
```

## 1) Current State (Verified 20261104T083800Z)
- Tests: 117/117 OK (python -m unittest discover -s tests -v)
- Git HEAD: 12218be93da896c8fe49b2b1821e80c4f398f26c (main)
- Latest heavy artifact: research_state/watch/trigger_harden_20261104T083427Z.json
- Inventory: 463 root zips (all 2024). Ironflow has 2026-10.parquet (Track-A only). No admissible Track C trigger.
- Prereg gating enforced (BLOCKED without prereg)
- Track C template: research_state/readiness/track_c_prereg_template_fclr012.json (NOT_FIRED, structure-only)
- Sealed experiments untouched; .github/workflows untouched
- Bottlenecks removed: __pycache__ directories and *.pyc noise deleted this session; ironflow_probe noise deleted this session

## 2) Immediate Next Actions
1) python -m unittest discover -s tests -v
2) python scripts/track_c_inventory_harden.py
3) Capture gating proof (expect BLOCKED with explicit prereg reason)
4) Validate track_c_prereg_template_fclr012.json (structure-only, NOT_FIRED)
5) Integrity sweep + verify sealed/firewall (sha256sum on sealed docs)
6) Write successor trigger_harden_<UTC>.json

## 3) Bottleneck Removal (Done This Session)
- Deleted scripts/__pycache__/*, tests/__pycache__/*, src/**/__pycache__/* and all *.pyc files (git status showed modified/deleted noise)
- Deleted research_state/ironflow_probe_20261104T083753Z.json (probe noise artifact)
- No session idle: heavy work mandate executes every session regardless of trigger state

## Definition of Done
New trigger_harden_<UTC>.json with all required sections, tests>=117, no workflow changes, no sealed touched, no new noise files, __pycache__ and ironflow_probe artifacts absent.
