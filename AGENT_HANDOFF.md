# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T103933Z
Git SHA (HEAD): 42dd83287
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T103826Z | Priority: P0 - HEAVY-WORK (FORCED) | Mode: TRACK-C-PRIORITIZED-EXECUTION

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE AS FIRST ACTION)

```text
TASK ID: FCLR-NEXT-047-TRACK-C-TRIGGER-READY-EXECUTE-ON-FIRE
PRIORITY: P0 - HEAVY WORK ENFORCED (NO STATUS-ONLY | NO IDLE WAITING | NO DEFERRAL | NO DOCUMENTATION-ONLY SESSION)
CAMPAIGN: FCLR-NEXT-047-FUNDING-CONDITIONED-VOL-TRIGGER-CAMPAIGN
TIMESTAMP (UTC): 20261104T103826Z
REPO BINDING: Funding-conditioned-volatility-and-liquidation-risk (Track C volatility/stress FIRST per repo name)

OBJECTIVE: Remain trigger-ready for Track C forward replication (FCLR-012 extension). Do NOT fabricate/admit zero-volume synthetic data. Execute ONLY if admissible unauthenticated Binance panel > 2026-11-02 exists.

MANDATORY HEAVY WORK (DO ALL 6 IN ORDER, EVERY TURN):
(1) INVENTORY - Run `python scripts/track_c_inventory_harden.py`. Compare against latest `research_state/watch/trigger_harden_*.json`. Confirm root zips are 2024-only, ironflow is Track A only, no 2025/2026 root zips.
(2) PREREG ENFORCEMENT - Verify `evaluate_forward` blocks without prereg (run the gating proof). Read `research_state/readiness/track_c_prereg_template_fclr012.json`. Do NOT inspect outcomes.
(3) ADMISSIBLE TRIGGER HUNT - Probe unauthenticated: data.binance.vision and github.com/binance/binance-public-data for BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT 1h klines/markPriceKlines/indexPriceKlines/premiumIndexKlines/fundingRate for dates > 2026-11-02. For each candidate: HTTP status, bytes, check volume/taker_buy > 0 (reject all-zero placeholders). Log full probe table.
(4) EXECUTE OR DOCUMENT GAP - IF admissible with >=3 non-overlapping 30d blocks: prereg BEFORE outcomes, freeze splits from coverage, embargo>=7d, block bootstrap>=2000 seed12345, Holm familywise correction, only prereg contrasts (B0/B1/C1/C2), primary C2_vs_B1 QLIKE. ELSE: write concrete gap analysis with exact curl/wget commands, next probe times, and DO NOT expand test set. Preserve inconclusive.
(5) INTEGRITY - `git diff --name-only .github/workflows` must be empty. Hash-check sealed: FCLR-001/002/003/006/007/008/011 unchanged vs manifests. Firewall intact (no Binance<->Hyperliquid). Tests >=117 green.
(6) PERSIST - Write `research_state/watch/trigger_harden_20261104T103826Z.json` successor (or newer) with inventory_diff, probes table, prereg_status, execution/gap_analysis, gating_proof, integrity_hashes, IF-TRIGGER-FIRES-NOW checklist, next_runnable_commands. Delete __pycache__/*.pyc.

RULES: Prereg BEFORE outcomes. Block bootstrap>=2000 seed12345. Holm correction. No sealed re-runs. No workflow changes. No trading. Track C>>B>>A. Firewalls enforced. Negative/inconclusive preserved. Bottlenecks: if data unavailable after exhaustive admissible probes, do HEAVY WORK documenting exact gap + probe commands (not idle).
```

## 1) Baseline (Verified 20261104T103826Z)
- Tests: 117/117 OK
- Git HEAD: 42dd83287 (chore: add heavy Track C trigger-ready successor handoff artifact)
- Repo focus: Funding-conditioned-volatility-and-liquidation-risk -> Track C priority
- Inventory: 463 root zips all 2024; no 2025/2026 root zips. binance_root_contains_2025_2026=false
- Ironflow: 2026-10.parquet present (Track A isolated)
- Track C: FCLR-012-V INCONCLUSIVE/PILOT (5 test days, CI spans zero, need >=3 non-overlapping 30d blocks)
- Probes: 2026-11-03 returned 206 with all volume=0.0 (synthetic placeholders, inadmissible); 2026-11-04 returned 404
- Prereg enforcement: evaluate_forward BLOCKED without prereg (verified)

## 2) Current Bottleneck
- DATA_GAP: No admissible post-2026-11-02 panel. Must actively probe unauthenticated sources rejecting zero-volume placeholders.

## 3) Definition of Done
- New timestamped trigger_harden artifact with full sections
- Tests >=117 green, no workflow changes, sealed unchanged, firewall intact
- Prereg before outcomes OR explicit admissible gap with concrete probe plan + exact commands
- No fabricated data; inconclusive preserved
- Measurable progress recorded
