# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T122514Z
Git SHA (HEAD): dd188ea1
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T122514Z | Priority: P0 - HEAVY-WORK (FORCED) | Mode: TRACK-C-DATA-BOTTLENECK-REMOVAL

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE AS FIRST ACTION)

```text
TASK ID: FCLR-NEXT-051-TRACK-C-BOTTLENECK-REMOVAL-AND-EXECUTION
PRIORITY: P0 - HEAVY WORK ENFORCED (NO STATUS-ONLY | NO IDLE WAITING | NO DEFERRAL | NO DOCUMENTATION-ONLY)
CAMPAIGN: FCLR-NEXT-051-FUNDING-CONDITIONED-VOLATILITY-DATA-UNBLOCK
TIMESTAMP (UTC): 20261104T122514Z
REPO BINDING: Funding-conditioned-volatility-and-liquidation-risk (Track C volatility/stress FIRST by repo name - funding-conditioned volatility is the core hypothesis)

OBJECTIVE: REMOVE THE DATA BOTTLENECK for Track C. Do NOT fabricate/admit zero-volume synthetic data. Treat absence as HARD GAP requiring concrete remediation. Execute forward replication ONLY if admissible unauthenticated Binance panel > 2026-11-02 exists with real volume>0.

KEY FINDING FROM PRIOR SESSION (20261104T113550Z): Regular klines/1h (NOT markPriceKlines/indexPriceKlines/premiumIndexKlines) for 2026-11-03 carries REAL volume on data.binance.vision for all 5 symbols (BTC 109K, ETH 2.4M, BNB 342K, SOL 11M, XRP 436M). Cached under research_state/data_cache/*_2026_11/klines-2026-11-03/. Forward panel now 2026-08-07..2026-11-03 = 89 days = 2 non-overlapping 30-day blocks. STILL SHORT: need 2026-11-04 and 2026-11-05 klines (1-2 days) to reach 3 blocks (90 days). markPriceKlines/indexPriceKlines/premiumIndexKlines 2026-11-03 = zero-volume placeholders (inadmissible). 2026-11-04/05/06 = HTTP 404 on both data.binance.vision and github mirror.

MANDATORY HEAVY WORK (EXECUTE ALL IN STRICT ORDER, EVERY TURN - NO SKIPPING):
(1) INVENTORY HARDEN
    - Run: python scripts/track_c_inventory_harden.py
    - Diff against latest research_state/watch/trigger_harden_*.json (latest: trigger_harden_20261104T113550Z.json)
    - Assert: root zips are 2024-only, ironflow isolated to Track A, binance_root_contains_2025_2026 == false
    - If ANY 2025/2026 root zips appear -> quarantine immediately, log with hashes, DO NOT consume

(2) GATING PROOF (PREREG BEFORE OUTCOMES)
    - Verify evaluate_forward() BLOCKS without preregistration (prove it explicitly) [CONFIRMED in prior session]
    - Read research_state/readiness/track_c_prereg_template_fclr012.json
    - DO NOT read outcome summaries. Preserve prereg-before-outcomes rule strictly

(3) EXHAUSTIVE UNAUTHENTICATED PROBE (ELIMINATE BOTTLENECK)
    - Probe: https://data.binance.vision/ and https://github.com/binance/binance-public-data
    - Targets: BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT
    - Types: klines/1h (PRIORITY - real volume found here), markPriceKlines/1h, indexPriceKlines/1h, premiumIndexKlines/1h, fundingRate
    - Dates: > 2026-11-02 (focus 2026-11-04, 2026-11-05, 2026-11-06 - these are the missing days)
    - For EVERY candidate: method, URL, HTTP status, bytes, Content-Type, parsed first/last timestamps
    - CRITICAL VALIDATION: sum(volume, taker_buyQuoteVolume, taker_buyBaseVolume) > 0 for klines. Reject all-zero/placeholders. Reject HTTP 206 partials without full validation.
    - Build complete probe table with rejection rationale for each attempt

(4) EXECUTE OR WRITE CONCRETE GAP REMEDIATION (NO IDLE)
    - IF admissible panel with >=3 non-overlapping 30d blocks exists with real volume>0:
      -> Create prereg BEFORE outcomes (new version), freeze splits from coverage only, embargo >=7d, block bootstrap >=2000 seed=12345, Holm correction, contrasts B0/B1/C1/C2, primary C2_vs_B1 QLIKE. Execute FCLR-012-V v2. Write evaluation_summary_FCLR-012-V-v2_*.md
    - ELSE:
      -> UPDATE CONCRETE GAP ANALYSIS (research_state/watch/gap_analysis_fclr012v_blocked_20261104T113000Z.md) with: exact curl/wget commands tried (full), alternate paths/mirrors checked, required fields to verify, next probe schedule (every 30-120 min), data acquisition plan with validation checks, estimated time to unblock. EXECUTE ALTERNATIVE HEAVY WORK (e.g. deep mechanism ablation on frozen FCLR-002 splits, funding-extreme replication refinement [FCLR-002 PARTIAL already executed], leakage audit hardening) - DO NOT fabricate data, DO NOT expand test set, preserve inconclusive

(5) INTEGRITY ENFORCEMENT
    - git diff --name-only .github/workflows MUST be empty (no workflow changes)
    - Verify sealed experiments unchanged: FCLR-001/002/003/006/007/008/011 (hash-check against manifests)
    - Firewall intact (no Binance<->Hyperliquid mixing)
    - Tests >=117 green
    - No sealed re-runs, no threshold-shopping

(6) PERSIST ARTIFACTS (MANDATORY)
    - Write research_state/watch/trigger_harden_<UTC>.json with: inventory_diff, probes_table (with rejection rationale), prereg_status, execution_status (FIRED|BLOCKED_BY_GAP), gap_analysis (if blocked), gating_proof, integrity_hashes, IF-TRIGGER-FIRES-NOW checklist, next_runnable_commands, bottleneck_remediation_plan
    - Update AGENT_HANDOFF.md if state changed (keep this as single durable handoff)
    - Delete __pycache__/*.pyc

RULES: Prereg BEFORE outcomes. Block bootstrap>=2000 seed12345. Holm correction. No sealed re-runs. No workflow changes. No trading. Track C >> B >> A by repo name. Firewalls enforced. Negative/inconclusive preserved. Bottlenecks MUST be removed via concrete actions, not status updates. Every session MUST produce measurable progress.
```

## 1) Current Verified State (20261104T113550Z)
- Tests: 117/117 OK
- Git HEAD: dd188ea1
- Repo focus: Funding-conditioned-volatility-and-liquidation-risk -> Track C (funding-conditioned volatility) PRIORITY
- Inventory: 463 root zips all 2024; no 2025/2026 root zips. binance_root_contains_2025_2026=false
- Ironflow: 2026-10.parquet present (Track A isolated/blocked)
- **NEW DATA FOUND:** klines/1h for 2026-11-03 has REAL volume for all 5 symbols on data.binance.vision (BTC 109K, ETH 2.4M, BNB 342K, SOL 11M, XRP 436M). Cached under research_state/data_cache/*_2026_11/klines-2026-11-03/. markPriceKlines/indexPriceKlines/premiumIndexKlines 2026-11-03 = zero-volume placeholders (inadmissible).
- Track C forward panel: 2026-08-07 .. 2026-11-03 = 89 days = 2 non-overlapping 30-day blocks. NEED 3 blocks (90 days through 2026-11-05). Missing: 2026-11-04, 2026-11-05 klines (HTTP 404 on both data.binance.vision and GitHub mirror).
- Track C: FCLR-012-V INCONCLUSIVE/PILOT (5 test days, 0 non-overlapping 30-day blocks). Trigger NOT_FIRED.
- Prereg enforcement: evaluate_forward BLOCKED without prereg (verified)
- Latest artifacts: research_state/watch/trigger_harden_20261104T113550Z.json, exhaustive_binance_probe_20261104T112954Z.json, gap_analysis_fclr012v_blocked_20261104T113000Z.md, fclr002_replication_summary_20261104T113000Z.json

## 2) Bottleneck & Remediation
- **BOTTLENECK:** Need 2026-11-04 and 2026-11-05 klines (1-2 days) to reach 3 non-overlapping 30-day blocks (90 days). Currently at 89 days = 2 blocks. Binance archive returns 404 for 2026-11-04+; GitHub mirror also 404. FundingRate monthly 2026-11 not yet published (404).
- **REMEDIATION:** Probe data.binance.vision klines/1h + fundingRate monthly for 2026-11-04/05/06 every 60 minutes. Binance typically publishes with 24-48h delay. Alternative heavy work already executed: FCLR-002 funding-correction replication (PARTIAL - high-RV median 16h vs low-RV 8h, direction matches paper, p=0.079 not significant).

## 3) Definition of Done
- New timestamped trigger_harden artifact with complete probe table
- Tests >=117 green, no workflow changes, sealed unchanged, firewall intact
- Either: prereg+execution of FCLR-012-V v2 if 3-block data found, OR updated gap analysis + alternative heavy work executed if blocked
- No fabricated data; inconclusive preserved
- Measurable progress recorded with exact commands and evidence