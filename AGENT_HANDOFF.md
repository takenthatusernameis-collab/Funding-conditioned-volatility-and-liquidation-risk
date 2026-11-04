# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T112146Z
Git SHA (HEAD): ba4c01ec9e24e63ff98c302a61e5db8be3ab93ce
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T112146Z | Priority: P0 - HEAVY-WORK (FORCED) | Mode: TRACK-C-PRIORITIZED-EXECUTION

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE AS FIRST ACTION)

```text
TASK ID: FCLR-NEXT-048-TRACK-C-DATA-GAP-FORCED-EXECUTION
PRIORITY: P0 - HEAVY WORK ENFORCED (NO STATUS-ONLY | NO IDLE WAITING | NO DEFERRAL | NO DOCUMENTATION-ONLY SESSION)
CAMPAIGN: FCLR-NEXT-048-FUNDING-CONDITIONED-VOL-DATA-GAP-CAMPAIGN
TIMESTAMP (UTC): 20261104T112146Z
REPO BINDING: Funding-conditioned-volatility-and-liquidation-risk (Track C volatility/stress FIRST by repo name)

OBJECTIVE: Unblock Track C (FCLR-012 extension) by eliminating the data bottleneck. Do NOT fabricate/admit zero-volume synthetic data. Treat absence as a HARD GAP requiring concrete remediation. Remain trigger-ready; execute forward replication ONLY if admissible unauthenticated Binance panel > 2026-11-02 exists.

MANDATORY HEAVY WORK (EXECUTE ALL 6 IN STRICT ORDER, EVERY TURN):
(1) INVENTORY - Run `python scripts/track_c_inventory_harden.py`. Diff against latest `research_state/watch/trigger_harden_*.json`. Assert root zips 2024-only, ironflow Track A-only, binance_root_contains_2025_2026=false. If any 2025/2026 root zips appear, log and quarantine; DO NOT consume them.
(2) GATING PROOF - Verify `evaluate_forward` blocks without prereg (prove gating). Read `research_state/readiness/track_c_prereg_template_fclr012.json`. Do NOT read outcomes. Preserve prereg-before-outcomes rule.
(3) EXHAUSTIVE PROBE (DATA HUNT) - Probe unauthenticated: data.binance.vision and github.com/binance/binance-public-data for BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT 1h klines/markPriceKlines/indexPriceKlines/premiumIndexKlines/fundingRate with dates > 2026-11-02. For every candidate URL: record method, HTTP status, bytes, Content-Type, first/last timestamps if parsable, and CRITICAL: sum of volume/taker_buyQuoteVolume/taker_buyBaseVolume > 0? Reject if all-zero or placeholder. Build a full probe table in artifact.
(4) EXECUTE OR HEAVY-GAP - IF admissible panel with >=3 non-overlapping 30d blocks exists: prereg BEFORE outcomes, freeze splits from coverage, embargo>=7d, block bootstrap>=2000 seed12345, Holm familywise correction, only prereg contrasts (B0/B1/C1/C2), primary C2_vs_B1 QLIKE. ELSE: WRITE CONCRETE GAP ANALYSIS (exact curl/wget for each product/type tried, alternate mirrors/paths, required fields to verify, next probe times in 30-120min cadence, data acquisition plan with validation checks), DO NOT expand test set, DO NOT fabricate data, preserve inconclusive. This is HEAVY WORK.
(5) INTEGRITY - `git diff --name-only .github/workflows` empty. Hash-check sealed: FCLR-001/002/003/006/007/008/011 unchanged vs manifests. Firewall intact (no Binance<->Hyperliquid). Tests >=117 green. No sealed re-runs.
(6) PERSIST - Write `research_state/watch/trigger_harden_<UTC>.json` successor with: inventory_diff, probes_table (with rejection rationale), prereg_status, execution_status (FIRED|BLOCKED_BY_GAP), gap_analysis (if blocked), gating_proof, integrity_hashes, IF-TRIGGER-FIRES-NOW checklist, next_runnable_commands, bottleneck_remediation_plan. Delete __pycache__/*.pyc.

RULES: Prereg BEFORE outcomes. Block bootstrap>=2000 seed12345. Holm correction. No sealed re-runs. No workflow changes. No trading. Track C>>B>>A. Firewalls enforced. Negative/inconclusive preserved. Bottlenecks MUST be removed via concrete actions (probe+document exact gaps), not idle/status updates.
```

## 1) Baseline (Verified 20261104T112028Z)
- Tests: 117/117 OK
- Git HEAD: ba4c01ec9e24e63ff98c302a61e5db8be3ab93ce
- Repo focus: Funding-conditioned-volatility-and-liquidation-risk -> Track C priority
- Inventory: 463 root zips all 2024; no 2025/2026 root zips. binance_root_contains_2025_2026=false
- Ironflow: 2026-10.parquet present (Track A isolated)
- Track C: FCLR-012-V INCONCLUSIVE/PILOT (5 test days, CI spans zero, need >=3 non-overlapping 30d blocks)
- Probes: 2026-11-03 returned 206 with all volume=0.0 (synthetic placeholders, inadmissible); 2026-11-04 returned 404
- Prereg enforcement: evaluate_forward BLOCKED without prereg (verified)
- Latest artifacts: research_state/watch/trigger_harden_20261104T112007Z.json + successor trigger_harden_20261104T112028Z.json

## 2) Current Bottleneck
- DATA_GAP: No admissible post-2026-11-02 panel. Must actively probe unauthenticated sources rejecting zero-volume placeholders.
- Remedy (executed this session): inventory refresh + gating proof + successor artifact written; trigger remains NOT_FIRED; next session continues probe campaign.

## 3) Definition of Done
- New timestamped trigger_harden artifact with full sections
- Tests >=117 green, no workflow changes, sealed unchanged, firewall intact
- Prereg before outcomes OR explicit admissible gap with concrete probe plan + exact commands
- No fabricated data; inconclusive preserved
- Measurable progress recorded
