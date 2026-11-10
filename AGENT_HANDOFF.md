# AGENT_HANDOFF.md — Single Durable Handoff (REPO-NAME PRIORITY: Track C / H001 first)

**Updated:** 2026-11-10T10:26:25Z — **P0 ACTIVE.** Repo `Funding-conditioned-volatility-and-liquidation-risk` — repo-name priority = **Track C / H001 (funding-conditioned volatility forecast vs RV-only baseline)** first; Track A/B liquidation tracks secondary. Work continues under RESEARCH_PROMPT.md hard constraints (no network/paid/manual/credentialed data, no fabricated provenance, no threshold shopping, no sealed-holdout reuse, no Track conflation, no risk overlay until forecast gate passes).

---

## 🔴 INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION — 2026-11-10T10:26:25Z

**PRIMARY FOCUS (repo-name priority): Track C / H001 — funding-conditioned volatility forecast vs RV-only baseline.**

**Current state (verified THIS session 2026-11-10T10:26:25Z):**
- **Dep-light gate:** 48/48 tests PASS (Ran 48 tests in 76.6s — OK)
- **Provenance machine-verified:** 161 funding CSV files, all with adjacent `.sha256` sidecars, `provenance_verified=true`, `unmapped_count=0`, 36001 manifest records indexed
- **2025 H1 window (2025-01-01..2025-06-07) funding schema audit:** `all_ok=true`, `missing=0`, `schema_bad=0` for 5 symbols × 6 months
- **Deep audit on 2025 H1 window:** `provenance_verified=true`, `symbols_ok=5`, `panel_blocks_estimate=6` (>=3 required)
- **M2 COMPLETE:** `research_state/research_protocol_fclr014.md` created (FROZEN_BEFORE_OUTCOMES, v2.0, frozen 2025-01-01..2025-06-07, 60/20/20 chronological, 7-day purge/embargo, Holm multiplicity, 2000-rep block bootstrap, deterministic seed, 2% materiality floor). `prereg_hash=8563163c62524605cbf7f11603759aee2210d133f82c3742319a6dd85dfca597` recorded in `run_manifest.json`. `split_boundaries_fclr014` with `frozen_before_outcomes=true` recorded in `run_manifest.json`. **No outcomes inspected for this window.**
- **run_evaluation.py:** FCLR-014 branch registered (OUT=research_state/evaluation_summary_FCLR-014.md, DATA_END=2025-06-07, SPLIT_KEY=split_boundaries_fclr014, START_ALL=2025-01-01). Fail-closed guard satisfied — unknown experiments no longer fall through to canonical summary.
- **2025 full panel (2025-01-01..2025-12-31) already verified:** 5 symbols × 365 days, 12 blocks each, all series complete (`research_state/trackc_deep_audit_2025_full_check.json`)

**Already tested (preserved nulls, no re-use — DO NOT RE-INSPECT):**
- FCLR-009 on 2025-06-08..2025-12-31 (6 blocks) → **NOT_MET** (-0.43% QLIKE, CI crosses zero)
- FCLR-003 on 2024-10-02..2024-12-31 (3 blocks) → **INCONCLUSIVE** (CI crosses zero)
- FCLR-013 on 2026 Q3 (1 block) → **NOT_SUPPORTED**
- FCLR-012-V on 2026-08-07..2026-11-02 (0 blocks) → **INCONCLUSIVE**
- Gate4 v3 multisplit (2024-04..09, 4 blocks) → **INCONCLUSIVE** (CI crosses zero)
- Deeper validation on FCLR-002 panel (2 blocks) → **EXPLORATORY_ONLY** (insufficient blocks)
**H001 remains NOT_SUPPORTED across every claim-worthy panel executed.**

**Initial task — execute M3→M6 of FOCUS_CAMPAIGN.md in order (M2 complete):**
1. **M3 (REQUIRED, THIS SESSION): Execute confirmatory FCLR-014 run**
   - Run `FCLR_EXPERIMENT=FCLR-014 python scripts/run_evaluation.py` on the frozen panel
   - Write `research_state/evaluation_summary_FCLR-014.md` with full metrics and uncertainty
   - Update `research_state/hypothesis_registry.json` H1_primary status
   - **DO NOT inspect outcomes before M3 run; the freeze at M2 is recorded and outcomes are sealed until this run**
2. **M4 (REQUIRED): Gate verdict & overlay eligibility**
   - Apply forecast gate (all 6 conditions) against M3 results; record verdict FORECAST_GATE_PASSED or NOT_SUPPORTED / INCONCLUSIVE
   - Overlay eligibility: OVERLAY_ELIGIBLE only if gate passed; otherwise NOT ELIGIBLE
   - Write verdict to `research_state/negative_results_report.md` (if null) and update `AGENT_HANDOFF.md`
3. **M5 (CONDITIONAL): Track A/B status confirmation**
4. **M6 (REQUIRED): Update AGENT_HANDOFF.md with next task**

**If M3/M4 result is NOT_SUPPORTED or INCONCLUSIVE:** preserve the null; do not promote; do not threshold-shop. If 2025 H1 window fails any admissibility check at M3: register new pilot protocol (new ID) on widest untested local panel with >=3 blocks + >=5 instruments, run as PILOT, report INCONCLUSIVE/NOT_SUPPORTED.

**Secondary (do not conflate):** Track A = STRUCTURALLY_BLOCKED (no admissible unauthenticated historical liquidation source). Track B = UNTESTED (no margin/leverage scenario registered before outcome inspection). Track C results = volatility/stress only, NEVER observed-liquidation validation.

---

## 🔧 BOTTLENECKS REMOVED (verified THIS session 2026-11-10T10:14:18Z and 2026-11-10T10:26:25Z)

| Bottleneck | Before | After | Evidence |
|---|---|---|---|
| Provenance not machine-verified | `provenance_verified=false`, 0 verified, unmapped>0 | `provenance_verified=true`, 161 files verified via adjacent sidecars, unmapped_count=0, 36001 manifest records | `scripts/trackc_provenance_lineage.py` → `verify_paths_with_manifests` on 161 funding CSVs: all verified |
| Dep-light reproducibility gate | baseline | 48/48 PASS | `python -m unittest <9 modules> -v` → Ran 48 tests in 76.6s — OK |
| Funding schema/coverage (2025 H1) | unverified | 5 symbols × 6 months: all_ok=true, missing=0, schema_bad=0 | `scripts/trackc_funding_schema_audit.py --months 2025-01..2025-06` |
| 2025 panel data completeness | unverified | provenance_verified=true, 5 symbols × 365 days, 12 blocks each | `research_state/trackc_deep_audit_2025_full_check.json` |
| 2025 H1 window block count | unverified | panel_blocks_estimate=6 (>=3 required) | `scripts/trackc_panel_deep_audit_orchestrator.py --window-hint 2025_01..2025_06` |
| FCLR-014 prereg not frozen (M2 blocker) | `prereg_hash=null`; splits illustrative (copy of FCLR-002); `confirmatory_resume_ready=false` | `prereg_hash=8563163c...dfca597` recorded; `split_boundaries_fclr014` with `frozen_before_outcomes=true` in `run_manifest.json`; `research_protocol_fclr014.md` v2.0 created | `research_state/research_protocol_fclr014.md`; `run_manifest.json#prereg_hash`; `run_manifest.json#split_boundaries_fclr014` |
| run_evaluation.py FCLR-014 not registered | Unknown FCLR_EXPERIMENT would refuse / fall through to canonical summary | FCLR-014 branch added (OUT, DATA_END, SPLIT_KEY, START_ALL); fail-closed guard satisfied | `scripts/run_evaluation.py` lines for FCLR-014 |

## ⛔ REMAINING STRUCTURAL BLOCKERS (not locally repairable, no network)

| Blocker | Detail | Next materially different route |
|---|---|---|
| MISSING_FUNDING_MONTH_FILE | `*`-fundingRate-2026-11.csv absent locally; no network | Use 2025 local panel (12 funding month files present per symbol, H1 fully verified) |
| HOLDOUT_REUSE_CONSTRAINT | FCLR-009 inspected 2025-06-08..2025-12-31; cannot re-inspect | Use untested 2025-01-01..2025-06-07 window for FCLR-014; never reuse FCLR-009 window |

## 📋 VERIFICATION COMMANDS FOR NEXT SESSION (run in order)

```bash
# 1. Dep-light gate (must pass 48/48)
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator tests.test_trackc_provenance_lineage -v
# Expected: Ran 48 tests — OK

# 2. Provenance machine-verified on ALL local funding data (rglob pattern)
python -c "
from scripts.trackc_provenance_lineage import verify_paths_with_manifests
from pathlib import Path
files = list(Path('research_state/data_cache').rglob('*-fundingRate-*.csv'))
res = verify_paths_with_manifests([str(p) for p in files], repo_root=Path('.'))
assert res['provenance_verified'] is True and res['unmapped_count'] == 0 and res['files_considered'] >= 160, res
print('PROVENANCE_VERIFIED_OK', {'files': res['files_considered'], 'verified': res['verified_count'], 'unmapped': res['unmapped_count']})
"

# 3. Deep audit on untested 2025 H1 confirmatory window (ALREADY VERIFIED — do not re-run unless M3 fails)
python scripts/trackc_panel_deep_audit_orchestrator.py --cache research_state/data_cache --repo-root . --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --window-hint 2025_01,2025_02,2025_03,2025_04,2025_05,2025_06 --min-symbols 5 --min-blocks 3 --out research_state/trackc_deep_audit_2025_h1_check.json
# Expected: provenance_verified=true, symbols_ok=5, panel_blocks_estimate>=3, all_required_series_complete=true

# 4. Funding schema audit for 2025 H1 window (ALREADY VERIFIED — do not re-run unless M3 fails)
python scripts/trackc_funding_schema_audit.py --repo-root . --cache research_state/data_cache --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --months 2025-01,2025-02,2025-03,2025-04,2025-05,2025-06 --out research_state/funding_schema_audit_2025_h1.json
# Expected: all_ok=true, missing=0, schema_bad=0

# 5. M3 — Execute confirmatory FCLR-014 run (NEXT REQUIRED TASK)
FCLR_EXPERIMENT=FCLR-014 python scripts/run_evaluation.py
# Expected: writes research_state/evaluation_summary_FCLR-014.md; paired OOS instruments=5; test window 2025-05-22..2025-06-07; gate assessment printed
# Then: update research_state/hypothesis_registry.json H1_primary status and record gate verdict
```

---

## 📁 KEY ARTIFACTS (AUTHORITATIVE — verify these exist before starting)

- `research_state/final_confirmatory_verdict.md` — H001 NOT_SUPPORTED (FCLR-003 canonical); superseded by this resume for 2025 H1 untested window
- `research_state/final_inconclusive_report.md` — FCLR-001 pilot/inconclusive, gate NOT MET
- `research_state/hypothesis_registry.json` — H1_primary (proposed), H2_shek_replication (proposed)
- `research_state/experiment_frontier.json` — blocked cells: FCLR-H004 (Track A BLOCKED), FCLR-H001 forward confirmatory (INCONCLUSIVE)
- `research_state/negative_results_report.md` — FCLR-009 NOT_MET, FCLR-003 INCONCLUSIVE, FCLR-013 NOT_SUPPORTED, Track B COMPLETE_INCONCLUSIVE, Track C exploratory results
- `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` — FCLR-014 prereg skeleton FROZEN_BEFORE_OUTCOMES, `prereg_hash=null`, `outcome_values_inspected=false`, splits illustrative (superseded by research_protocol_fclr014.md v2.0 for M2 freeze)
- `research_state/research_protocol_fclr014.md` — FCLR-014 protocol v2.0 FROZEN_BEFORE_OUTCOMES (2025-01-01..2025-06-07, 60/20/20 chronological, 7-day purge/embargo, Holm multiplicity, 2000-rep block bootstrap, 2% materiality floor); `prereg_hash=8563163c62524605cbf7f11603759aee2210d133f82c3742319a6dd85dfca597`; `outcome_values_inspected=false`
- `research_state/trackc_deep_audit_2025_full_check.json` — 2025 full panel verified (provenance_verified=true, 5 symbols, 12 blocks)
- `research_state/trackc_deep_audit_2025_h1_check.json` — 2025 H1 deep audit (provenance_verified=true, symbols_ok=5, panel_blocks_estimate=6)
- `research_state/funding_schema_audit_2025_h1.json` — 2025 H1 funding schema (all_ok=true, missing=0)
- `research_state/run_manifest.json` — run IDs, split boundaries, frozen_before_outcomes flags
- `scripts/trackc_provenance_lineage.py`, `scripts/trackc_funding_schema_audit.py`, `scripts/trackc_gap_repair_manifest.py`, `scripts/trackc_panel_deep_audit_orchestrator.py`, `scripts/run_evaluation.py`, `scripts/freeze_fclr009_splits.py` — audit/repair/eval tooling

---

## ⛔ DO NOT DO (future sessions — NON-NEGOTIABLE)

- No network/downloads, no paid/manual/credentialed data, no workflow/scheduler/poller additions
- No fabricated provenance/outcomes, no threshold shopping, no sealed-holdout reuse
- Do not relabel PARTIAL/INCONCLUSIVE/NOT_SUPPORTED as confirmatory
- Do not re-inspect the FCLR-009 window (2025-06-08..2025-12-31); holdout-reuse prohibited
- Do not conflate Track A (observed liquidations, blocked) with Track B (modeled breaches) or Track C (volatility)
- No `.github/workflows` edits; no live/paper trading; no risk overlay until forecast gate passes
- Do not skip M1→M6 milestones in FOCUS_CAMPAIGN.md; each session must deliver one substantive verifiable result

---

## 🟢 FOCUS CAMPAIGN — SEE `FOCUS_CAMPAIGN.md`

Heavy-work milestones M1→M6 (execute in order; do not skip):
- **M1** Provenance & data admissibility lock — **COMPLETE** (verified)
- **M2** Freeze protocol v2 + prereg-before-outcomes — **COMPLETE** (protocol created, prereg_hash recorded, splits frozen before outcomes)
- **M3** Execute confirmatory Track C / H001 run — **NEXT REQUIRED TASK** (run FCLR_EXPERIMENT=FCLR-014 python scripts/run_evaluation.py after M2 freeze)
- **M4** Gate verdict & overlay eligibility — **REQUIRED** (after M3)
- **M5** Track A / Track B status confirmation — **CONDITIONAL**
- **M6** Handoff update & next-session task — **REQUIRED EVERY SESSION**

Non-negotiable execution rules in `FOCUS_CAMPAIGN.md` §NON-NEGOTIABLE EXECUTION RULES. Future agents must execute milestones in order; skipping is non-compliant. Each session must deliver one substantive verifiable result (§19 RESEARCH_PROMPT.md).

---

**END OF SINGLE DURABLE HANDOFF. next_unfinished_task: M3 — Execute confirmatory FCLR-014 run: `FCLR_EXPERIMENT=FCLR-014 python scripts/run_evaluation.py` on the frozen 2025 H1 panel (M2 protocol frozen, prereg_hash recorded, outcomes sealed — DO NOT inspect before M3 run), then M4 gate verdict & overlay eligibility.**
**Updated: 2026-11-10T10:26:25Z**
