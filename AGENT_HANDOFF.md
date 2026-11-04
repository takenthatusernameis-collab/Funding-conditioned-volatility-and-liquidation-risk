# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T102330Z
Git SHA (HEAD): f366e788 (latest checkpoint); tree clean except deleted __pycache__/*.pyc
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T102330Z | Priority: P0 - HEAVY-WORK (FORCED) | Mode: TRACK-C-FORWARD-REPLICATION-CAMPAIGN

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE AS FIRST ACTION)

```text
TASK ID: FCLR-NEXT-045-TRACK-C-EXTEND-TO-CONFIRMATORY
PRIORITY: P0 - HEAVY WORK ENFORCED (NO STATUS-ONLY | NO IDLE WAITING | NO DEFERRAL | NO DOCUMENTATION-ONLY SESSION)
CAMPAIGN: FCLR-NEXT-045-FUNDING-CONDITIONED-VOLATILITY-EXTENSION-CAMPAIGN
TIMESTAMP (UTC): 20261104T102330Z
REPO BINDING: Funding-conditioned-volatility-and-liquidation-risk (MUST prioritize per repo name)

OBJECTIVE: Get Track C (volatility/stress) to confirmatory capability. FCLR-012-V was INCONCLUSIVE/PILOT: C2_vs_B1 +15.19% QLIKE on 2026-10-29..2026-11-02 but only 5 test days (0x non-overlapping 30d blocks), CI [-0.360564,0.059434] spans zero. Gate requires >=3 non-overlapping 30d blocks. Current admissible 2026 panel ends 2026-11-02; 2026-10-28/29 mark days genuinely absent (404). No 2025/2026 zips in repo root. Binance archive probed and ends 2026-11-02.

MANDATORY HEAVY WORK (DO ALL 6 IN ORDER, EVERY TURN):
(1) INVENTORY - Run `python scripts/track_c_inventory_harden.py` and diff against last trigger_harden. Confirm root zips are all 2024; binance_root_contains_2025_2026 false. Write full diff.
(2) PREREG ENFORCEMENT - Verify evaluate_forward blocks without prereg. Read research_state/prereg/* and freeze any extension BEFORE examining outcomes. No snooping.
(3) ADMISSIBLE TRIGGER HUNT - Probe unauthenticated Binance public archive paths (data.binance.vision, github.com/binance/binance-public-data raw paths) and public APIs for BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT 1h klines/mark/index/premium/funding for dates > 2026-11-02. Try common patterns: klines, markPriceKlines, indexPriceKlines, premiumIndexKlines, fundingRate by year/month/day. Reject auth/payment/manual. Log every URL/method/status.
(4) EXECUTE - IF new admissible panel found extending to >=3x30d non-overlapping blocks AND passes quality gates: prereg extension (splits/embargo/purge/metrics/gates/Holm/block-bootstrap>=2000 seed12345), run forward replication, record full results. ELSE: do NOT fabricate. Extend ONLY within existing admissible 2026 data if strictly allowed by prereg without expanding test set via snooping; otherwise produce INCONCLUSIVE with concrete unauthenticated probe plan + exact commands to try next.
(5) INTEGRITY - `git diff --name-only .github/workflows` must be empty. Verify sealed FCLR-001/002/003/006/007/008/011 unchanged (compare hashes to manifests). Track firewall intact (no Binance-Hyperliquid merge). Tests >=117 green.
(6) PERSIST - Write research_state/watch/trigger_harden_<UTC>.json with all sections filled (inventory_diff, probes, prereg_status, execution/gap_analysis, gating_proof, hashes, IF-TRIGGER-FIRES-NOW, next_runnable_commands). Delete __pycache__, *.pyc, probe noise. Update this handoff only if strategy changes with evidence.

RULES: Prereg BEFORE outcomes. Block bootstrap>=2000 seed12345. Holm correction. No re-run sealed experiments. No workflow changes. No live/paper trading. Track C priority over B over A. Firewalls enforced. Preserve negative/inconclusive results.
```

## 1) Baseline (Verified 20261104T102330Z)
- Tests: 117/117 OK (`python -m unittest discover -s tests -v`)
- Git HEAD: f366e788; tree clean except deleted __pycache__/*.pyc (cleanup done, not a blocker)
- LFS: research_state/run_manifest.json materialized
- Inventory: 463 root zips (all 2024). Ironflow 2026-10.parquet present (Track A). No 2025/2026 Binance zips. binance_root_contains_2025_2026=false
- FCLR-012-V: 2026 panel 2026-08-07..2026-11-02, test 5 days, INCONCLUSIVE/PILOT, gate NOT_MET
- Bottlenecks removed: LFS pointer fixed, __pycache__/pyc cleaned, run_manifest materialized

## 2) Immediate Next Actions
1. `python -m unittest discover -s tests -v` (expect 117 OK)
2. `python scripts/track_c_inventory_harden.py` (refresh inventory + diff vs latest trigger_harden_*.json)
3. `python scripts/probe_fclr012v_extend.py` (probe Binance archive for 2026-11-03/04 mark/index/premium klines, log all attempts)
4. `python scripts/write_trigger_harden_successor.py` (write trigger_harden artifact with IF-TRIGGER-FIRES-NOW checklist)
5. Decide extend-or-gap with prereg enforcement (no outcomes before prereg)
6. Integrity sweep: `git diff --name-only .github/workflows` (expect empty), sha256 sealed docs vs manifests, tests >=117 green
7. Cleanup noise: delete __pycache__, *.pyc, probe JSON noise

## 3) Blocker Status (DATA_GAP - not idle)
- Type: DATA_GAP
- Description: FCLR-012-V forward replication blocked — test window 5 days = 0 non-overlapping 30d blocks; CI spans zero; Binance archive probed as ending 2026-11-02 with no newer admissible unauthenticated panel.
- CONFIRMED PROBE RESULT (20261104): data.binance.vision returns HTTP 206 for 2026-11-03 markPriceKlines/indexPriceKlines/premiumIndexKlines for ALL 5 symbols (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT), but each file has 24 rows with volume=0.0 — ZERO-VOLUME SYNTHETIC PLACEHOLDERS, NOT admissible real market data. Trigger NOT fired. 2026-11-04 returns 404 for all series.
- Next materially-different free route: continuous probe cadence on data.binance.vision for post-2026-11-02 klines/mark/index/premium/funding for BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT. Check volume/taker_buy > 0 for admissibility (not just HTTP 200/206). Document every probe result with URL/method/status/volume. If none admissible: report INCONCLUSIVE with exact gap + next probe commands.
- IF TRIGGER FIRES NOW: any probe returning HTTP 200/206 for a date > 2026-11-02 on an admissible unauthenticated path with NON-ZERO volume/taker_buy -> immediately create prereg (freeze splits/embargo/purge/metrics/gates) BEFORE inspecting outcomes, then run forward replication with block bootstrap>=2000 seed12345 + Holm correction.

## 4) Definition of Done
- New timestamped trigger_harden_<UTC>.json with full sections
- Tests >=117 green, no workflow changes
- Sealed experiments untouched, firewall intact
- Prereg existed before any outcomes OR explicit admissible gap with concrete probe plan
- No fabricated data; negative/inconclusive preserved

## 5) Protected Artifacts (DO NOT MODIFY)
- .github/workflows/* (git diff --name-only must be empty)
- research_state/cross_track_decision_firewall.md
- research_state/sealed_holdout_integrity.md
- research_state/structural_closure_verdict_heavy.md
- research_state/experiment_frontier.json
- research_state/run_manifest.json
- research_state/hypothesis_registry.json
- Sealed experiments: FCLR-001/002/003/006/007/008/011 (hash-verified, never re-run)
- Track firewall: Binance-only Track C; no Binance<->Hyperliquid merge; Track A (Hyperliquid/ironflow) isolated