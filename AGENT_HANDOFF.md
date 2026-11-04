# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T102149Z
Git SHA (HEAD): 789ae083afd09cdea6d8d8798bfddd9c0c42c5d0
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T102149Z | Priority: P0 - HEAVY-WORK (FORCED) | Mode: TRACK-C-FORWARD-REPLICATION-CAMPAIGN

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE AS FIRST ACTION)

```text
TASK ID: FCLR-NEXT-045-TRACK-C-EXTEND-TO-CONFIRMATORY
PRIORITY: P0 - HEAVY WORK ENFORCED (NO STATUS-ONLY | NO IDLE WAITING | NO DEFERRAL | NO DOCUMENTATION-ONLY SESSION)
CAMPAIGN: FCLR-NEXT-045-FUNDING-CONDITIONED-VOLATILITY-EXTENSION-CAMPAIGN
TIMESTAMP (UTC): 20261104T102149Z
REPO BINDING: Funding-conditioned-volatility-and-liquidation-risk (MUST prioritize per repo name)

OBJECTIVE: Get Track C (volatility/stress) to confirmatory capability. FCLR-012-V was INCONCLUSIVE/PILOT: C2_vs_B1 +15.19% QLIKE on 2026-10-29..2026-11-02 but only 5 test days (0x non-overlapping 30d blocks), CI [-0.360564,0.059434] spans zero. Gate requires >=3 non-overlapping 30d blocks. Current admissible 2026 panel ends 2026-11-02; 2026-10-28/29 mark days genuinely absent (404). No 2025/2026 zips in repo root.

MANDATORY HEAVY WORK (DO ALL 6 IN ORDER, EVERY TURN):
(1) INVENTORY - Run `python scripts/track_c_inventory_harden.py` and diff against last trigger_harden. Confirm root zips are all 2024; binance_root_contains_2025_2026 false. Write full diff.
(2) PREREG ENFORCEMENT - Verify evaluate_forward blocks without prereg. Read research_state/prereg/* and freeze any extension BEFORE examining outcomes. No snooping.
(3) ADMISSIBLE TRIGGER HUNT - Probe unauthenticated Binance public archive paths (data.binance.vision, github.com/binance/binance-public-data raw paths) and public APIs for BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT 1h klines/mark/index/premium/funding for dates > 2026-11-02. Try common patterns: klines, markPriceKlines, indexPriceKlines, premiumIndexKlines, fundingRate by year/month/day. Reject auth/payment/manual. Log every URL/method/status.
(4) EXECUTE - IF new admissible panel found extending to >=3x30d non-overlapping blocks AND passes quality gates: prereg extension (splits/embargo/purge/metrics/gates/Holm/block-bootstrap>=2000 seed12345), run forward replication, record full results. ELSE: do NOT fabricate. Extend ONLY within existing admissible 2026 data if strictly allowed by prereg without expanding test set via snooping; otherwise produce INCONCLUSIVE with concrete unauthenticated probe plan + exact commands to try next.
(5) INTEGRITY - `git diff --name-only .github/workflows` must be empty. Verify sealed FCLR-001/002/003/006/007/008/010/011 unchanged (compare hashes to manifests). Track firewall intact (no Binance-Hyperliquid merge). Tests >=117 green.
(6) PERSIST - Write research_state/watch/trigger_harden_<UTC>.json with all sections filled (inventory_diff, probes, prereg_status, execution/gap_analysis, gating_proof, hashes, IF-TRIGGER-FIRES-NOW, next_runnable_commands). Delete __pycache__, *.pyc, probe noise. Update this handoff only if strategy changes with evidence.

RULES: Prereg BEFORE outcomes. Block bootstrap>=2000 seed12345. Holm correction. No re-run sealed experiments. No workflow changes. No live/paper trading. Track C priority over B over A. Firewalls enforced. Preserve negative/inconclusive results.
```

## 1) Baseline (Verified 20261104T102149Z)
- Tests: 117/117 OK
- Git HEAD: 789ae083afd09cdea6d8d8798bfddd9c0c42c5d0
- LFS: research_state/run_manifest.json materialized
- Inventory: 463 root zips (all 2024). Ironflow 2026-10.parquet present (Track A). No 2025/2026 Binance zips. binance_root_contains_2025_2026=false
- FCLR-012-V: 2026 panel 2026-08-07..2026-11-02, test 5 days, INCONCLUSIVE/PILOT, gate NOT_MET
- Bottlenecks removed: LFS pointer fixed, __pycache__/pyc cleaned

## 2) Immediate Next Actions
1. `python -m unittest discover -s tests -v`
2. `python scripts/track_c_inventory_harden.py`
3. Execute unauthenticated probe hunt for >2026-11-02 (log all attempts)
4. Decide extend-or-gap with prereg enforcement
5. Integrity sweep + write new trigger_harden_<UTC>.json
6. Cleanup noise

## 3) Definition of Done
- New timestamped trigger_harden_<UTC>.json with full sections
- Tests >=117 green, no workflow changes
- Sealed experiments untouched, firewall intact
- Prereg existed before any outcomes OR explicit admissible gap with concrete probe plan
- No fabricated data; negative/inconclusive preserved
