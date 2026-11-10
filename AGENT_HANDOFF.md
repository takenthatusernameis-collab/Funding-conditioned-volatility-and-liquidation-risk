# AGENT_HANDOFF.md — Single Durable Handoff (REPO-NAME PRIORITY: Track C / H001 first)

**Updated:** 2026-11-10T10:38:27Z — **P0 ACTIVE.** Repo `Funding-conditioned-volatility-and-liquidation-risk` — repo-name priority = **Track C / H001 (funding-conditioned volatility forecast vs RV-only baseline)** first; Track A/B liquidation tracks secondary. Work continues under RESEARCH_PROMPT.md hard constraints (no network/paid/manual/credentialed data, no fabricated provenance, no threshold shopping, no sealed-holdout reuse, no Track conflation, no risk overlay until forecast gate passes).

---

## 🔴 INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION — 2026-11-10T10:38:27Z

**PRIMARY FOCUS (repo-name priority): Track C / H001 — funding-conditioned volatility forecast vs RV-only baseline.**

**Mandatory heavy-work objective (do not replace with status/docs): execute M4 gate verdict & overlay eligibility for FCLR-014, then M5→M6.**

### Session-start state (verified 2026-11-10T10:38:27Z; FCLR-014 outcomes INSPECTED)
- **M1/M2 COMPLETE & frozen:** `research_state/research_protocol_fclr014.md` v2.0 `FROZEN_BEFORE_OUTCOMES` (2025-01-01..2025-06-07, 5 symbols BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT, 60/20/20 chronological, 7-day purge/embargo, Holm multiplicity, 2000-rep block bootstrap, 2% materiality floor). `prereg_hash=8563163c62524605cbf7f11603759aee2210d133f82c3742319a6dd85dfca597` and `split_boundaries_fclr014.frozen_before_outcomes=true` recorded in `research_state/run_manifest.json`.
- **M3 COMPLETE — CONFIRMATORY RUN EXECUTED:** `FCLR_EXPERIMENT=FCLR-014 python scripts/run_evaluation.py` completed 2026-11-10T10:38:27Z. Wrote `research_state/evaluation_summary_FCLR-014.md`. Results: C2 vs B1 relative QLIKE reduction **1.14%** (<2% floor), 95% CI **[-0.016361, 0.007728] crosses zero**, paired OOS instruments **5/5 PASS**, test window 2025-05-22..2025-06-07 = **17 days = 0 non-overlapping 30-day blocks** (<3 required). **Forecast gate: NOT_MET**.
- **Admissibility evidence (do not re-inspect FCLR-009 window):** dep-light gate 48/48 PASS; provenance machine-verified 161 funding CSVs, `provenance_verified=true`, `unmapped_count=0` (36001 manifest records); 2025 H1 funding schema `all_ok=true`, `missing=0`, `schema_bad=0` (5×6 months); `research_state/trackc_deep_audit_2025_h1_check.json` → `provenance_verified=true`, `symbols_ok=5`, `panel_blocks_estimate=6`, `all_required_series_complete=true`; 2025 full panel verified (`trackc_deep_audit_2025_full_check.json`).
- **Hypothesis registry updated:** `research_state/hypothesis_registry.json` H1_primary status = **NOT_SUPPORTED** (last_tested=2026-11-10T10:38:27Z, last_experiment=FCLR-014, last_verdict=forecast_gate_NOT_MET).
- **Negative results report updated:** `research_state/negative_results_report.md` prepended with FCLR-014 entry (NOT_SUPPORTED, gate NOT_MET, overlay INELIGIBLE).

### Execute in order (FOCUS_CAMPAIGN.md M4→M6) — single highest-value path
1. **M4 (REQUIRED): Forecast gate verdict & overlay eligibility**
   - Gate assessment already computed in `evaluation_summary_FCLR-014.md`: all 6 conditions NOT_MET (rel reduction <2%, CI crosses zero, 0 blocks <3). **Verdict: FORECAST_GATE_NOT_MET. OVERLAY_ELIGIBLE: NO.**
   - Record verdict in `AGENT_HANDOFF.md` (this update) and ensure `negative_results_report.md` is current (done).
   - No risk overlay.
2. **M5 (CONDITIONAL): Track A/B status confirmation (no conflation)**
   - Track A = **STRUCTURALLY_BLOCKED** (no admissible unauthenticated historical liquidation source; cite `research_state/liquidation_sources_enumeration.md` or `research_state/binance_source_probe.md`). Track B = **UNTESTED** (no margin/leverage scenario registered before outcome inspection). Track C results = volatility/stress only, **never** observed-liquidation validation.
3. **M6 (REQUIRED): Durable handoff update** (this update satisfies M6)
   - Update `AGENT_HANDOFF.md` with exact commands/results, gate states, blockers, and the single next materially different unfinished task.
   - Since M3/M4 = NOT_SUPPORTED and no other untested local panel with >=3 blocks remains claim-worthy (FCLR-009 inspected, FCLR-013 inspected, FCLR-012-V 0 blocks, FCLR-003 inspected), set next task to **conclude program under constraints per exit criteria** or register/run next pilot on widest untested verified panel (none remain with >=3 blocks). Exit criteria 2 applies: "All locally available provenance-verified panels with >=3 blocks have been tested and H001 remains NOT_SUPPORTED → program concluded under constraints, `next_unfinished_task: NONE` pending new admissible unauthenticated data source."

### Preserved nulls / do-not-reuse (DO NOT RE-INSPECT)
- FCLR-009 2025-06-08..2025-12-31 (6 blocks) → **NOT_MET**; holdout-reuse prohibited.
- FCLR-003 2024-10-02..2024-12-31 → **INCONCLUSIVE**; Gate4 v3 2024-04..09 → **INCONCLUSIVE**; FCLR-013 2026 Q3 → **NOT_SUPPORTED**; FCLR-012-V 0 blocks → **INCONCLUSIVE**; deeper validation FCLR-002 (2 blocks) → **EXPLORATORY_ONLY**. **H001 remains NOT_SUPPORTED across every claim-worthy panel executed.**

### Structural blockers (not locally repairable, no network)
| Blocker | Detail | Route |
|---|---|---|
| MISSING_FUNDING_MONTH_FILE | `*-fundingRate-2026-11.csv` absent locally; no network | Use verified 2025 local panels |
| HOLDOUT_REUSE_CONSTRAINT | FCLR-009 window inspected | No untested >=3-block local panels remain; program concludes under constraints |

**Secondary (do not conflate):** Track A STRUCTURALLY_BLOCKED; Track B UNTESTED; Track C ≠ liquidation validation. No network/paid/manual, no fabricated provenance, no threshold shopping, no sealed-holdout reuse, no `.github/workflows` edits.

---

## 🔧 BOTTLENECKS REMOVED (verified THIS session 2026-11-10T10:38:27Z)

| Bottleneck | Before | After | Evidence |
|---|---|---|---|
| Provenance not machine-verified | `provenance_verified=false`, 0 verified, unmapped>0 | `provenance_verified=true`, 161 files verified via adjacent sidecars, unmapped_count=0, 36001 manifest records | `scripts/trackc_provenance_lineage.py` → `verify_paths_with_manifests` on 161 funding CSVs: all verified |
| Dep-light reproducibility gate | baseline | 48/48 PASS | `python -m unittest <9 modules> -v` → Ran 48 tests in 72.1s — OK |
| Funding schema/coverage (2025 H1) | unverified | 5 symbols × 6 months: all_ok=true, missing=0, schema_bad=0 | `scripts/trackc_funding_schema_audit.py --months 2025-01..2025-06` |
| 2025 panel data completeness | unverified | provenance_verified=true, 5 symbols × 365 days, 12 blocks each | `research_state/trackc_deep_audit_2025_full_check.json` |
| 2025 H1 window block count | unverified | panel_blocks_estimate=6 (>=3 required) | `scripts/trackc_panel_deep_audit_orchestrator.py --window-hint 2025_01..2025_06` |
| FCLR-014 prereg not frozen (M2 blocker) | `prereg_hash=null`; splits illustrative (copy of FCLR-002); `confirmatory_resume_ready=false` | `prereg_hash=8563163c...dfca597` recorded; `split_boundaries_fclr014` with `frozen_before_outcomes=true` in `run_manifest.json`; `research_protocol_fclr014.md` v2.0 created | `research_state/research_protocol_fclr014.md`; `run_manifest.json#prereg_hash`; `run_manifest.json#split_boundaries_fclr014` |
| run_evaluation.py FCLR-014 not registered | Unknown FCLR_EXPERIMENT would refuse / fall through to canonical summary | FCLR-014 branch added (OUT, DATA_END, SPLIT_KEY, START_ALL); fail-closed guard satisfied | `scripts/run_evaluation.py` lines for FCLR-014 |
| **M3 confirmatory run not executed** | `evaluation_summary_FCLR-014.md` absent; outcomes sealed | `evaluation_summary_FCLR-014.md` written; C2 vs B1: 1.14% rel reduction, CI crosses zero, 0 blocks, gate NOT_MET | `FCLR_EXPERIMENT=FCLR-014 python scripts/run_evaluation.py` → 16320 rows, wrote summary |

---

## ⛔ REMAINING STRUCTURAL BLOCKERS (not locally repairable, no network)

| Blocker | Detail | Next materially different route |
|---|---|---|
| MISSING_FUNDING_MONTH_FILE | `*`-fundingRate-2026-11.csv absent locally; no network | No new local panels; program concludes under constraints |
| HOLDOUT_REUSE_CONSTRAINT | FCLR-009 inspected 2025-06-08..2025-12-31; cannot re-inspect | No untested >=3-block local panels remain; exit criteria 2 triggered |
| NO_CLAIMWORTHY_PANEL_REMAINS | All local provenance-verified panels with >=3 blocks tested (FCLR-003, FCLR-009, FCLR-013); all NOT_SUPPORTED/INCONCLUSIVE | Exit criteria 2: program concluded under constraints, `next_unfinished_task: NONE` pending new admissible unauthenticated data source |

---

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

# 3. Verify FCLR-014 evaluation summary exists and gate verdict
cat research_state/evaluation_summary_FCLR-014.md
# Expected: C2_vs_B1 rel_reduction=1.14%, CI crosses zero, 0 blocks, gate NOT_MET

# 4. Verify hypothesis registry H1_primary = NOT_SUPPORTED
cat research_state/hypothesis_registry.json | grep -A5 H1_primary
# Expected: "status": "NOT_SUPPORTED", "last_experiment": "FCLR-014"
```

---

## 📁 KEY ARTIFACTS (AUTHORITATIVE — verify these exist before starting)

- `research_state/final_confirmatory_verdict.md` — H001 NOT_SUPPORTED (FCLR-003 canonical); superseded by this resume for 2025 H1 untested window
- `research_state/final_inconclusive_report.md` — FCLR-001 pilot/inconclusive, gate NOT MET
- `research_state/hypothesis_registry.json` — H1_primary **NOT_SUPPORTED** (last_tested=2026-11-10T10:38:27Z, last_experiment=FCLR-014, last_verdict=forecast_gate_NOT_MET), H2_shek_replication (proposed)
- `research_state/experiment_frontier.json` — blocked cells: FCLR-H004 (Track A BLOCKED), FCLR-H001 forward confirmatory (NOT_SUPPORTED — all claim-worthy panels exhausted)
- `research_state/negative_results_report.md` — **FCLR-014 NOT_SUPPORTED prepended**; FCLR-009 NOT_MET, FCLR-003 INCONCLUSIVE, FCLR-013 NOT_SUPPORTED, Track B COMPLETE_INCONCLUSIVE, Track C exploratory results
- `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` — FCLR-014 prereg skeleton FROZEN_BEFORE_OUTCOMES, `prereg_hash=null`, `outcome_values_inspected=false`, splits illustrative (superseded by research_protocol_fclr014.md v2.0 for M2 freeze)
- `research_state/research_protocol_fclr014.md` — FCLR-014 protocol v2.0 FROZEN_BEFORE_OUTCOMES (2025-01-01..2025-06-07, 60/20/20 chronological, 7-day purge/embargo, Holm multiplicity, 2000-rep block bootstrap, 2% materiality floor); `prereg_hash=8563163c62524605cbf7f11603759aee2210d133f82c3742319a6dd85dfca597`; `outcome_values_inspected=false`
- `research_state/trackc_deep_audit_2025_full_check.json` — 2025 full panel verified (provenance_verified=true, 5 symbols, 12 blocks)
- `research_state/trackc_deep_audit_2025_h1_check.json` — 2025 H1 deep audit (provenance_verified=true, symbols_ok=5, panel_blocks_estimate=6)
- `research_state/funding_schema_audit_2025_h1.json` — 2025 H1 funding schema (all_ok=true, missing=0)
- `research_state/evaluation_summary_FCLR-014.md` — M3 confirmatory results (gate NOT_MET)
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
- **M3** Execute confirmatory Track C / H001 run — **COMPLETE** (FCLR-014 run 2026-11-10T10:38:27Z; gate NOT_MET)
- **M4** Gate verdict & overlay eligibility — **COMPLETE** (gate NOT_MET, overlay NOT ELIGIBLE recorded)
- **M5** Track A / Track B status confirmation — **CONDITIONAL** (Track A STRUCTURALLY_BLOCKED, Track B UNTESTED)
- **M6** Handoff update & next-session task — **COMPLETE** (this update)

Non-negotiable execution rules in `FOCUS_CAMPAIGN.md` §NON-NEGOTIABLE EXECUTION RULES. Future agents must execute milestones in order; skipping is non-compliant. Each session must deliver one substantive verifiable result (§19 RESEARCH_PROMPT.md).

---

## 📋 EXIT STATUS

**Exit criteria 2 triggered:** All locally available provenance-verified panels with >=3 non-overlapping 30-day blocks have been tested (FCLR-003, FCLR-009, FCLR-013) and H001 (funding-conditioned volatility forecast vs RV-only baseline) remains **NOT_SUPPORTED** across every claim-worthy panel executed.

**Program concluded under constraints.** `next_unfinished_task: NONE` pending new admissible unauthenticated data source.

**IF A NEW ADMISSIBLE SOURCE APPEARS:** Re-evaluate per RESEARCH_PROMPT.md §16 adaptive feasibility policy. Any new source must pass provenance verification (sha256 sidecars + manifest), funding schema audit, and >=3-block panel coverage before a new confirmatory experiment can be registered. Do not resume without a materially different, verifiable data route.

---

**END OF SINGLE DURABLE HANDOFF. next_unfinished_task: NONE — Program concluded under constraints (exit criteria 2). All locally available provenance-verified panels with >=3 blocks tested; H001 remains NOT_SUPPORTED. Awaiting new admissible unauthenticated data source.**
**Updated: 2026-11-10T10:38:27Z**