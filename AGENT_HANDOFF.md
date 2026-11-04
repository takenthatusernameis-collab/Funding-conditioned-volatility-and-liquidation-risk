# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T103535Z
Git SHA (HEAD): 1d14ab04
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T103535Z | Priority: P0 - HEAVY-WORK (FORCED) | Mode: TRACK-C-FORWARD-REPLICATION-CAMPAIGN

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE AS FIRST ACTION)

```text
TASK ID: FCLR-NEXT-046-TRACK-C-EXTEND-TO-CONFIRMATORY
PRIORITY: P0 - HEAVY WORK ENFORCED (NO STATUS-ONLY | NO IDLE WAITING | NO DEFERRAL | NO DOCUMENTATION-ONLY SESSION)
CAMPAIGN: FCLR-NEXT-046-FUNDING-CONDITIONED-VOLATILITY-EXTENSION-CAMPAIGN
TIMESTAMP (UTC): 20261104T103535Z
REPO BINDING: Funding-conditioned-volatility-and-liquidation-risk (MUST prioritize per repo name - Track C volatility/stress first)

OBJECTIVE: Get Track C (volatility/stress) to confirmatory capability. FCLR-012-V was INCONCLUSIVE/PILOT: C2_vs_B1 +15.19% QLIKE on 2026-10-29..2026-11-02 but only 5 test days (0x non-overlapping 30d blocks), CI [-0.360564,0.059434] spans zero. Gate requires >=3 non-overlapping 30d blocks. Current admissible 2026 panel ends 2026-11-02; 2026-10-28/29 mark days genuinely absent (404). Root zips are all 2024 only. Binance archive previously probed: 2026-11-03 returned 206 with 24 rows all volume=0.0 (synthetic placeholders, inadmissible). 2026-11-04 returned 404.

MANDATORY HEAVY WORK (DO ALL 6 IN ORDER, EVERY TURN):
(1) INVENTORY - Run `python scripts/track_c_inventory_harden.py` and write diff vs latest trigger_harden_*.json. Confirm no 2025/2026 root zips. Note current panel boundaries.
(2) PREREG ENFORCEMENT - Verify evaluate_forward blocks without prereg. Read research_state/prereg/* and freeze any extension BEFORE examining outcomes. No snooping of results.
(3) ADMISSIBLE TRIGGER HUNT - Probe unauthenticated Binance public archive (data.binance.vision) and github.com/binance/binance-public-data raw paths for BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT 1h klines/markPriceKlines/indexPriceKlines/premiumIndexKlines/fundingRate for dates > 2026-11-02 (focus 2026-11-03+). For each candidate file check HTTP status AND volume/taker_buy > 0 (reject zero-volume placeholders). Log every URL/method/status/bytes/volume.
(4) EXECUTE - IF new admissible panel found extending to >=3x30d non-overlapping blocks AND passes quality gates: prereg extension (splits/embargo/purge/metrics/gates/Holm/block-bootstrap>=2000 seed12345), run forward replication, record full results. ELSE: do NOT fabricate. Do NOT expand test set by snooping. Produce INCONCLUSIVE with concrete unauthenticated probe plan + exact commands + next checkpoint time.
(5) INTEGRITY - `git diff --name-only .github/workflows` must be empty. Verify sealed FCLR-001/002/003/006/007/008/011 unchanged (hash vs manifests). Track firewall intact (no Binance-Hyperliquid merge). Tests >=117 green.
(6) PERSIST - Write research_state/watch/trigger_harden_20261104T103535Z.json with inventory_diff, probes, prereg_status, execution/gap_analysis, gating_proof, hashes, IF-TRIGGER-FIRES-NOW checklist, next_runnable_commands. Delete __pycache__, *.pyc. Update this handoff only if strategy changes with evidence.

RULES: Prereg BEFORE outcomes. Block bootstrap>=2000 seed12345. Holm correction. No re-run sealed experiments. No workflow changes. No live/paper trading. Track C priority over B over A. Firewalls enforced. Preserve negative/inconclusive results. Bottlenecks: if data unavailable after exhaustive admissible probes, do NOT idle - document precise gap and next probe commands; do NOT do documentation-only session.
```

## 1) Baseline (Verified 20261104T103535Z)
- Tests: 117/117 OK (last verified)
- Git HEAD: 1d14ab04 (chore(kilo): checkpoint agent session); tree clean
- Repo focus: Funding-conditioned-volatility-and-liquidation-risk -> Track C (volatility/stress) priority
- Inventory: Root zips all 2024 (463 files). No 2025/2026 zips in root. binance_root_contains_2025_2026=false
- Ironflow 2026-10.parquet present (Track A isolated)
- FCLR-012-V: 2026 panel 2026-08-07..2026-11-02, test 5 days, INCONCLUSIVE/PILOT, gate NOT_MET (need >=3 non-overlapping 30d blocks)
- Previous probe: 2026-11-03 mark/index/premium returned 206 but 24 rows all volume=0.0 (synthetic placeholders, inadmissible). 2026-11-04 returned 404.

## 2) Bottlenecks Removed / Current State
- LFS pointer fixed, run_manifest materialized, __pycache__/pyc cleaned
- Prereg/evaluate_forward enforcement in place
- Sealed experiments protected, track firewall enforced

## 3) Blocker Status (DATA_GAP - must actively probe, not idle)
- Type: DATA_GAP
- Impact: Cannot reach >=3 non-overlapping 30d blocks for confirmatory gate
- Required action: Exhaustive unauthenticated probe of post-2026-11-02 Binance public data; reject zero-volume placeholders
- IF TRIGGER FIRES NOW: any admissible unauthenticated file with HTTP 200/206 AND non-zero volume/taker_buy for dates > 2026-11-02 -> prereg BEFORE outcomes, run forward replication with block bootstrap>=2000 seed12345 + Holm correction

## 4) Definition of Done
- New timestamped trigger_harden_20261104T103535Z.json with all required sections
- Tests >=117 green, no workflow changes (git diff --name-only .github/workflows empty)
- Sealed experiments untouched, firewall intact
- Prereg existed before any outcomes OR explicit admissible gap with concrete probe plan + exact commands
- No fabricated data; negative/inconclusive preserved
- Measurable research progress (probe results + decision) recorded

## 5) Protected Artifacts (DO NOT MODIFY)
- .github/workflows/*
- research_state/cross_track_decision_firewall.md
- research_state/sealed_holdout_integrity.md
- research_state/structural_closure_verdict_heavy.md
- research_state/experiment_frontier.json
- research_state/run_manifest.json
- research_state/hypothesis_registry.json
- Sealed: FCLR-001/002/003/006/007/008/011
- Track firewall: Binance-only Track C; no Binance<->Hyperliquid merge; Track A isolated
