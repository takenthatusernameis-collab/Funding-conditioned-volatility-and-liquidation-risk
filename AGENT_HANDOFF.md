# AGENT_HANDOFF.md (SINGLE DURABLE HANDOFF)
Timestamp (UTC): 20261104T084000Z
Git SHA (HEAD): 789ae083afd09cdea6d8d8798bfddd9c0c42c5d0
Branch: main
Repo: Funding-conditioned-volatility-and-liquidation-risk
Handoff ID: FCLR-HANDOFF-20261104T084000Z | Priority: P0 - HEAVY-WORK (FORCED) | Mode: TRACK-C-FORWARD-REPLICATION-CAMPAIGN

## 0) MANDATORY INITIAL MESSAGE FOR NEXT AGENT (COPY/PASTE AS FIRST ACTION)

```text
TASK ID: FCLR-NEXT-043-TRACK-C-FORWARD-REPLICATION-HEAVY
PRIORITY: P0 - HEAVY WORK ENFORCED (NO STATUS-ONLY | NO IDLE WAITING | NO DEFERRAL | NO DOCUMENTATION-ONLY SESSION)
CAMPAIGN: FCLR-NEXT-043-FUNDING-CONDITIONED-VOLATILITY-FORWARD-REPLICATION-CONTINUOUS
TIMESTAMP (UTC): 20261104T084000Z
REPO BINDING: Funding-conditioned-volatility-and-liquidation-risk (MUST prioritize per repo name)

OBJECTIVE: Drive Track C (volatility/stress) forward replication to a confirmatory-capable state WITHOUT touching sealed experiments. FCLR-012-V showed +15.19% QLIKE vs B1 (C2) on 2026-10-29..2026-11-02 but test window only 5 days (0x30d blocks), CI [-0.360564, 0.059434] spans zero -> INCONCLUSIVE/PILOT. Need to (a) hunt for any admissible NEW unauthenticated Binance panel data (beyond sealed 2026-05-08..2026-08-06 for FCLR-011, beyond current 2026-08-07..2026-11-02 window already tested) that extends test window to >=3 non-overlapping 30d blocks, (b) if none exists, execute the preregistered "forward replication extension plan" with strict leakage control, expanding universe/time coverage ONLY if admissible, (c) do NOT relax block-count/gating. Track B modeled breach is secondary; Track A (observed liquidations, Hyperliquid ironflow) is separate and must remain firewall-isolated.

HEAVY WORK MANDATE (EXECUTE ALL 6 EVERY SESSION — NO EXCEPTION):
(1) INVENTORY SWEEP - root zips, data_cache/, research_state/, check for any new 2026 zips/dates not in FCLR-012-V coverage. Write inventory diff.
(2) PREREG ENFORCEMENT - verify evaluate_forward blocks without prereg; capture proof. Do NOT inspect holdout before prereg updates.
(3) ADMISSIBLE TRIGGER HUNT - test unauthenticated Binance public data paths (archive + public APIs) for new dates/symbols. Reject anything requiring auth/payment/manual download. Document probes.
(4) FORWARD REPLICATION EXECUTION - if admissible extended panel found AND passes gates, prereg before outcomes. If not found, run the preregistered extension analysis within existing admissible data with proper embargo/purge, block bootstrap>=2000, Holm, only where counts allow. Never fabricate.
(5) INTEGRITY SWEEP - verify sealed FCLR-001/002/003/006/007/008/010/011 untouched; .github/workflows untouched; firewall rules intact; hashes match manifests.
(6) DURABLE ARTIFACT - write trigger_harden_<UTC>.json + update AGENT_HANDOFF.md with exact commands/results/blockers/next_runnable. Delete noise (__pycache__, *.pyc, probe artifacts).

RULES: tests>=117 green. Prereg BEFORE outcomes. Block bootstrap>=2000 seed12345. Holm correction across family. No re-run sealed experiments. No workflow changes. No live/paper trading. Track C priority over B over A. Keep tracks firewalled. Preserve negative/inconclusive results.
```

## 1) Current State (Verified 20261104T084000Z)
- Tests: 117/117 OK (`python -m unittest discover -s tests -v`)
- Git HEAD: 789ae083afd09cdea6d8d8798bfddd9c0c42c5d0 (main)
- Latest heavy artifact: research_state/watch/trigger_harden_20261104T083332Z.json
- Inventory: 463 root zips (all 2024). Ironflow 2026-10.parquet exists (Track A only). FCLR-012-V panel is 2026 BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT 1h klines/mark/index/premium/funding covering 2026-08-07..2026-11-02 (train/val/test as preregistered). 2026-10-28/29 mark days genuinely absent (404); not imputed.
- Status: FCLR-012-V INCONCLUSIVE/PILOT - gate NOT_MET (test window 5 days = 0 non-overlapping 30d blocks, CI spans zero). FCLR-011 PASSED (Track C). FCLR-010 PASSED (Track A).
- Prereg enforcement active. Track C template structure-only. Sealed/firewall intact. Bottlenecks removed (pycache/pyc/noise cleaned).

## 2) Bottleneck Removal (This Session)
- Deleted scripts/__pycache__/*, tests/__pycache__/*, src/**/__pycache__/* and all *.pyc files
- Deleted research_state/ironflow_probe_20261104T083242Z.json (probe noise)
- Ensured no idle paths; heavy mandate enforced every session

## 3) Immediate Next Actions (Run in Order)
1. `python -m unittest discover -s tests -v` (must stay >=117 green)
2. `python scripts/track_c_inventory_harden.py` (full inventory diff vs latest trigger_harden_*.json)
3. Hunt admissible new data: probe Binance public archive paths for dates beyond 2026-11-02 for required symbols/series (1h klines, markPriceKlines, indexPriceKlines, premiumIndexKlines, fundingRate). Document every probe with method/result/auth/status. Reject if needs auth/payment/manual.
4. If new admissible panel found: create prereg BEFORE outcomes (freeze splits/embargo/purge/metrics/gates), run forward replication with block bootstrap>=2000 seed12345, Holm across family. If none found: extend analysis within existing admissible 2026 panel only if prereg allows without data snooping; otherwise report INCONCLUSIVE with concrete data gap and exact next probe.
5. Integrity sweep: `git diff --name-only .github/workflows` (must be empty), verify sealed files unchanged (hashes), confirm firewall intact.
6. Write `research_state/watch/trigger_harden_<UTC>.json` with inventory diff, probe results, gating proof, prereg status, execution results (or gap analysis), hashes, and `IF-TRIGGER-FIRES-NOW` + `next_runnable_commands`.
7. Cleanup: remove any new `__pycache__`, `*.pyc`, `ironflow_probe_*`, duplicate `trigger_harden_*` artifacts.

## 4) Definition of Done
- New timestamped `trigger_harden_<UTC>.json` committed to artifacts (not just written) with all sections filled
- Tests >=117 green
- No changes to `.github/workflows`
- No sealed experiments modified (FCLR-001/002/003/006/007/008/010/011)
- Prereg enforcement proof captured; if outcomes generated, prereg existed before them
- Either (a) admissible extended panel preregistered+executed with full gates OR (b) explicit admissible data gap documented with concrete unauthenticated probe plan and no fabricated data
- Track firewall respected (no Binance-Hyperliquid merge)
- Noise artifacts removed
