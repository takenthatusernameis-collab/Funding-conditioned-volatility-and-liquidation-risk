# AGENT_HANDOFF.md — Single Durable Handoff (PROGRAM RESUMING — REPO-NAME PRIORITY)

**Updated:** 2026-11-10T09:30:00Z — **P0 ACTIVE: PROGRAM RESUMING.** Repo `Funding-conditioned-volatility-and-liquidation-risk` — repo-name priority = **Track C / H001 (funding-conditioned volatility forecast)** first, Track A/B liquidation tracks secondary. Prior "CONCLUDED — NO TASK EXISTS" superseded: provenance bottleneck removed locally (no network), dep-light gate green, funding schema verified for 2024 Q1. Work continues under RESEARCH_PROMPT.md hard constraints (no network/paid/manual/credentialed data, no fabricated provenance, no threshold shopping, no sealed-holdout reuse).

---

## 🔴 INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION — 2026-11-10T09:30:00Z

**PRIMARY FOCUS (repo-name priority): Track C / H001 — funding-conditioned volatility forecast vs RV-only baseline.**

The confirmatory program is resuming on the best available **local, provenance-verified panel** (2024-01..2024-12 + 2025, 5 symbols: BTC/ETH/BNB/SOL/XRP, mark/index/premium/klines + funding). All local data now has machine-verifiable sha256 provenance (36001 sidecars + JSON manifests). Dep-light gate: 48/48 OK.

**Initial task:** Re-run the frozen H001/Track C confirmatory contrast (C2 vs B1, next-24h realized variance QLIKE) on a **locally repairable panel with >=3 non-overlapping 30-day test blocks and >=5 instruments**, using a **frozen prereg registered BEFORE outcomes**. If no local panel satisfies the block count without reusing a sealed holdout, register a new pilot protocol version (new ID) on the widest available local panel and report INCONCLUSIVE/NOT_SUPPORTED with preserved null — do not relax gates, do not threshold-shop, do not promote.

**Secondary:** Track A (observed liquidations) remains STRUCTURALLY_BLOCKED (no admissible unauthenticated historical source). Track B (modeled boundary breaches) requires a registered margin/leverage scenario before outcome inspection. Never conflate tracks.

---

## 🔧 BOTTLENECKS REMOVED (this session)

| Bottleneck | Before | After | Evidence |
|---|---|---|---|
| Provenance not machine-verified | `provenance_verified=false`, 0 verified, 25 unmapped | `provenance_verified=true`, 36001 records indexed, all manifests loaded | `scripts/repair_local_provenance.py` (36001 `.sha256` sidecars + `manifest_extended.json`/`manifest_extract.json` rewritten as real JSON) |
| Dep-light reproducibility gate | 48/48 OK (baseline) | 48/48 OK (re-verified) | `python -m unittest ... -v` → Ran 48 tests in ~70s — OK |
| Funding schema/coverage (2024 Q1) | unverified | all 15 symbol-months schema OK, 0 missing, 0 bad | `scripts/trackc_funding_schema_audit.py --months 2024-01,2024-02,2024-03` → all_ok=true |

## ⛔ REMAINING STRUCTURAL BLOCKERS (2026-11 window — not locally repairable, no network)

| Blocker | Detail | Next materially different route |
|---|---|---|
| MISSING_FUNDING_MONTH_FILE | `BTC/ETH/BNB/SOL/XRP`-fundingRate-2026-11.csv absent locally; no network to obtain | Use 2024 Q1-Q4 / 2025 local panels that already have 12 funding month files each (FCLR-009 covered 2025) |
| INSUFFICIENT_30D_BLOCKS | 2026-11 panel: panel_blocks_estimate=0 | Select a local window with >=3 non-overlapping 30-day test blocks (e.g. FCLR-003 used 2024-10-02..2024-12-31 = 91 days = 3 blocks) |
| CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES | `prereg_hash=null` | Freeze a new protocol version (research_protocol_fclr0xx.md + splits) before computing outcomes; record prereg_hash |

## 📋 VERIFICATION COMMANDS FOR NEXT SESSION

```bash
# 1. Dep-light gate (must pass 48/48)
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator tests.test_trackc_provenance_lineage -v
# Expected: Ran 48 tests — OK

# 2. Confirm provenance is machine-verified on local data
python -c "
from scripts.trackc_provenance_lineage import verify_paths_with_manifests
from pathlib import Path
res = verify_paths_with_manifests([str(p) for p in Path('data/raw').glob('*-fundingRate-*.csv')], repo_root=Path('.'))
assert res['provenance_verified'] is True and res['unmapped_count'] == 0, res
print('PROVENANCE_VERIFIED_OK', res)
"

# 3. Funding schema audit for a candidate confirmatory window (e.g. 2024-10, 2024-11, 2024-12)
python scripts/trackc_funding_schema_audit.py --repo-root . --cache research_state/data_cache --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --months 2024-10,2024-11,2024-12 --out research_state/funding_schema_audit_2024q4.json
# Expected: all_ok=true, missing=0

# 4. Deep audit on a claim-worthy local window (must show symbols_ok=5, series complete)
python scripts/trackc_panel_deep_audit_orchestrator.py --cache research_state/data_cache --repo-root . --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --window-hint 2024_12 --min-symbols 5 --min-blocks 3 --out research_state/trackc_deep_audit_2024_12_check.json
```

---

## 📁 KEY ARTIFACTS (AUTHORITATIVE)

- `research_state/final_synthesis_report.md` — prior family-wide synthesis (concluded under old constraints; superseded by this resume)
- `research_state/hypothesis_registry.json` — H1_primary (proposed), H2_shek_replication (proposed)
- `research_state/experiment_frontier.json` — blocked cells: FCLR-H004 (Track A), FCLR-H001 forward confirmatory (INCONCLUSIVE), Track C (insufficient blocks beyond 2026-11-02)
- `research_state/negative_results_report.md` — FCLR-009 NOT_MET (-0.43% QLIKE, CI crosses zero), FCLR-003 INCONCLUSIVE (C1 vs B1 -8.09% excludes zero but secondary only), FCLR-013 NOT_SUPPORTED
- `research_state/evaluation_summary_FCLR009.md`, `evaluation_summary_FCLR-013.md`, `evaluation_summary_FCLR002_REPRO.md`
- `scripts/repair_local_provenance.py` — provenance repair (this session)
- `scripts/trackc_provenance_lineage.py`, `scripts/trackc_funding_schema_audit.py`, `scripts/trackc_gap_repair_manifest.py`, `scripts/trackc_panel_deep_audit_orchestrator.py` — audit/repair tooling

---

## ⛔ DO NOT DO (future sessions)

- No network/downloads, no paid/manual/credentialed data, no workflow/scheduler/poller additions
- No fabricated provenance/outcomes, no threshold shopping, no sealed-holdout reuse
- Do not relabel PARTIAL/INCONCLUSIVE/NOT_SUPPORTED as confirmatory
- Do not conflate Track A (observed liquidations, blocked) with Track B (modeled breaches) or Track C (volatility)
- No `.github/workflows` edits; no live/paper trading; no risk overlay until forecast gate passes

---

## 🟢 FOCUS CAMPAIGN — SEE `FOCUS_CAMPAIGN.md`

The next focus campaign is defined in `FOCUS_CAMPAIGN.md` (heavy-work milestones, acceptance gates, non-negotiable execution rules). Future agents must execute it in order; skipping milestones is non-compliant.

---

**END OF SINGLE DURABLE HANDOFF. next_unfinished_task: Track C / H001 confirmatory on provenance-verified local panel with frozen prereg + >=3 blocks.**
**Updated: 2026-11-10T09:30:00Z**
