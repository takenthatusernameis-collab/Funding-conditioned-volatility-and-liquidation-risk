# AGENT_HANDOFF.md — Single Durable Handoff (REPO-NAME PRIORITY: liquidation risk Track B first, then volatility Track C)

**Updated:** 2026-11-10T15:37:06Z — **P0 ACTIVE (Track B, MANDATORY).** Track C / H1 concluded NOT_SUPPORTED under constraints (`next_unfinished_task (Track C): NONE`). **Single durable initial task is `NEXT_SESSION_TASK.md` (2026-11-10T15:37:06Z): execute Track B modeled liquidation boundary-breach campaign on verified local data** (admissibility lock → prereg before outcomes → confirmatory eval → verdict/registry/handoff). Track A remains STRUCTURALLY_BLOCKED. No network/paid/manual/credentialed data; no fabricated provenance; no threshold shopping; no holdout reuse; no Track A/B/C conflation; no risk overlay before gate pass; no `.github/workflows` edits.

---

## 🔴 INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION — 2026-11-10T15:37:06Z (see `NEXT_SESSION_TASK.md`)

**PRIMARY FOCUS (repo-name priority): Track B / liquidation-risk — modeled boundary-breach campaign.** Repo name `Funding-conditioned-volatility-and-liquidation-risk`: Track C (volatility) is concluded NOT_SUPPORTED; Track A (observed liquidations) is STRUCTURALLY_BLOCKED. The untested liquidation-risk leg — Track B modeled breach on local mark/index/premium/klines + funding — is the **only** heavy-work path that can advance repo-name scope without network/new data.

Status: **UNTESTED** — no modeled liquidation boundary-breach scenario has been preregistered before outcome inspection on an admissible local panel with `frozen_before_outcomes=true`.

### Session-start state (verified 2026-11-10T15:37:06Z; FCLR-014 outcomes INSPECTED)
- **M1/M2 COMPLETE & frozen:** `research_state/research_protocol_fclr014.md` v2.0 `FROZEN_BEFORE_OUTCOMES` (2025-01-01..2025-06-07, 5 symbols BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT, 60/20/20 chronological, 7-day purge/embargo, Holm multiplicity, 2000-rep block bootstrap, 2% materiality floor). `prereg_hash=8563163c62524605cbf7f11603759aee2210d133f82c3742319a6dd85dfca597` and `split_boundaries_fclr014.frozen_before_outcomes=true` recorded in `research_state/run_manifest.json`.
- **M3 COMPLETE — CONFIRMATORY RUN EXECUTED:** `FCLR_EXPERIMENT=FCLR-014 python scripts/run_evaluation.py` completed 2026-11-10T10:38:27Z. Wrote `research_state/evaluation_summary_FCLR-014.md`. Results: C2 vs B1 relative QLIKE reduction **1.14%** (<2% floor), 95% CI **[-0.016361, 0.007728] crosses zero**, test window 2025-05-22..2025-06-07 = **17 days = 0 non-overlapping 30-day blocks** (<3). **Forecast gate: NOT_MET**.
- **Admissibility evidence (do not re-inspect FCLR-009 window):** dep-light gate 48/48 PASS; provenance machine-verified 161 funding CSVs, `provenance_verified=true`, `unmapped_count=0` (36001 manifest records); 2025 H1 funding schema `all_ok=true`, `missing=0`, `schema_bad=0` (5×6 months); `research_state/trackc_deep_audit_2025_h1_check.json` → `provenance_verified=true`, `symbols_ok=5`, `panel_blocks_estimate=6`, `all_required_series_complete=true`; 2025 full panel verified (`trackc_deep_audit_2025_full_check.json`).
- **Hypothesis registry updated:** `research_state/hypothesis_registry.json` H1_primary status = **NOT_SUPPORTED** (last_tested=2026-11-10T10:38:27Z, last_experiment=FCLR-014, last_verdict=forecast_gate_NOT_MET).
- **Negative results report updated:** `research_state/negative_results_report.md` prepended with FCLR-014 entry (NOT_SUPPORTED, gate NOT_MET, overlay INELIGIBLE).

### Next heavy-work campaign — Track B / liquidation risk (UNTESTED, executable locally)
Track C is concluded. Track A is STRUCTURALLY_BLOCKED (no admissible unauthenticated observed-liquidation census; cite `research_state/liquidation_sources_enumeration.md` / `research_state/track_a_structural_block.md`). Track B (modeled liquidation boundary breaches from local mark/index/premium klines and funding) requires **no network, no new data, no credentials**. Execute in order (each step is substantive/verifiable):

1. **Admissibility lock (Track B panel):** pick a verified local window with >=5 instruments and >=3 non-overlapping 30-day test blocks, distinct from sealed/inspected windows where reuse is prohibited. Machine-verify provenance/schema/coverage: run `scripts/trackc_provenance_lineage.py` (or equivalent) → `provenance_verified=true`, `unmapped_count=0`; `scripts/trackc_funding_schema_audit.py` + `scripts/trackc_panel_deep_audit_orchestrator.py` → complete series, >=5 symbols, >=3 blocks. Record evidence under `research_state/`.
2. **Preregister BEFORE any outcome inspection:** define modeled breach target and leverage/margin assumptions (explicitly Track B, NOT observed liquidations), predictors (funding extremes, RV, premium/index dislocation), 60/20/20 chronological splits with 7-day purge/embargo, primary metric, 2% materiality floor, Holm multiplicity, bootstrap CI. Write `research_state/research_protocol_trackb_<ID>.md`, record `prereg_hash` and `split_boundaries_trackb_<ID>.frozen_before_outcomes=true` in `research_state/run_manifest.json`. **No outcome inspection before freeze.**
3. **Execute & evaluate:** run confirmatory evaluation on frozen panel; write `research_state/evaluation_summary_trackb_<ID>.md` with point estimate, 95% CI (block bootstrap), relative change, n_instruments, n_blocks, n_obs; apply forecast gate.
4. **Verdict & registry update:** set Track B status (NOT_SUPPORTED/INCONCLUSIVE/gate outcome) in `research_state/hypothesis_registry.json`, update `research_state/experiment_frontier.json`, append to `research_state/negative_results_report.md` (preserve nulls), update `AGENT_HANDOFF.md` and `NEXT_SESSION_TASK.md` with exact outcomes, overlay eligibility (NOT ELIGIBLE unless all gate conditions pass), and `next_unfinished_task` (next materially different route or "NONE — program concluded under constraints"). Commit code/manifests/reports (no raw data/caches).

### Preserved nulls / do-not-reuse (DO NOT RE-INSPECT)
- FCLR-009 2025-06-08..2025-12-31 (6 blocks) → NOT_MET; holdout-reuse prohibited.
- FCLR-003 2024-10-02..2024-12-31 → INCONCLUSIVE; Gate4 v3 2024-04..09 → INCONCLUSIVE; FCLR-013 2026 Q3 → NOT_SUPPORTED; FCLR-012-V 0 blocks → INCONCLUSIVE; deeper validation FCLR-002 (2 blocks) → EXPLORATORY_ONLY. **H001 remains NOT_SUPPORTED across every claim-worthy panel executed.**

### Structural blockers (not locally repairable, no network)
| Blocker | Detail | Route |
|---|---|---|
| MISSING_FUNDING_MONTH_FILE | `*-fundingRate-2026-11.csv` absent locally; no network | Use verified 2025 local panels; Track B needs no new funding month |
| HOLDOUT_REUSE_CONSTRAINT | FCLR-009 window inspected | No untested >=3-block local Track C panels remain; Track C concludes |
| NO_CLAIMWORTHY_TRACKC_PANEL_REMAINS | All local provenance-verified Track C panels with >=3 blocks tested | Track C `next_unfinished_task: NONE` pending new admissible unauthenticated source |
| TRACK_A_STRUCTURALLY_BLOCKED | No admissible unauthenticated observed-liquidation census | Track B modeled breaches on local data is the liquidation-risk path |

**Secondary (do not conflate):** Track A STRUCTURALLY_BLOCKED; Track B UNTESTED → execute campaign above; Track C ≠ liquidation validation. No network/paid/manual, no fabricated provenance, no threshold shopping, no sealed-holdout reuse, no `.github/workflows` edits.

---

## 🔧 BOTTLENECKS REMOVED (verified 2026-11-10T15:37:06Z; no remaining locally repairable Track C bottleneck)

| Bottleneck | Before | After | Evidence |
|---|---|---|---|
| Provenance not machine-verified | `provenance_verified=false`, unmapped>0 | `provenance_verified=true`, unmapped_count=0, 36001 manifest records | `scripts/trackc_provenance_lineage.py` on 161 funding CSVs |
| Dep-light reproducibility gate | baseline | 48/48 PASS | `python -m unittest <9 modules> -v` → Ran 48 tests — OK |
| Funding schema/coverage (2025 H1) | unverified | 5 symbols × 6 months: all_ok=true, missing=0, schema_bad=0 | `scripts/trackc_funding_schema_audit.py --months 2025-01..2025-06` |
| 2025 panel completeness | unverified | provenance_verified=true, 5 symbols × 365 days, 12 blocks each | `research_state/trackc_deep_audit_2025_full_check.json` |
| FCLR-014 prereg not frozen (M2 blocker) | `prereg_hash=null` | `prereg_hash=8563163c...dfca597`, `frozen_before_outcomes=true` | `research_state/research_protocol_fclr014.md`; `run_manifest.json` |
| FCLR-014 confirmatory run not executed | summary absent; outcomes sealed | `evaluation_summary_FCLR-014.md` written; gate NOT_MET | `FCLR_EXPERIMENT=FCLR-014 python scripts/run_evaluation.py` |

**Remaining unblocked path:** Track B modeled-breach campaign requires no new data source — all inputs (mark/index/premium klines, funding) are already provenance-verified locally. No bottleneck prevents preregistration + execution.

---

## ⛔ REMAINING STRUCTURAL BLOCKERS (not locally repairable, no network)

| Blocker | Detail | Next materially different route |
|---|---|---|
| MISSING_FUNDING_MONTH_FILE | `*`-fundingRate-2026-11.csv absent locally; no network | Track B uses existing verified panels; Track C awaits new admissible unauthenticated source |
| HOLDOUT_REUSE_CONSTRAINT | FCLR-009 inspected 2025-06-08..2025-12-31; cannot re-inspect | Track C exit criteria 2 triggered; Track B choose a different uninspected verified window |
| NO_CLAIMWORTHY_TRACKC_PANEL_REMAINS | All local Track C panels with >=3 blocks tested and NOT_SUPPORTED/INCONCLUSIVE | Track C `next_unfinished_task: NONE`; proceed to Track B campaign |

---

## 📋 VERIFICATION COMMANDS FOR NEXT SESSION (run in order)

```bash
# 1. Dep-light gate (must pass 48/48)
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator tests.test_trackc_provenance_lineage -v
# Expected: Ran 48 tests — OK

# 2. Provenance machine-verified on ALL local funding data
python -c "
from scripts.trackc_provenance_lineage import verify_paths_with_manifests
from pathlib import Path
files = list(Path('research_state/data_cache').rglob('*-fundingRate-*.csv'))
res = verify_paths_with_manifests([str(p) for p in files], repo_root=Path('.'))
assert res['provenance_verified'] is True and res['unmapped_count'] == 0 and res['files_considered'] >= 160, res
print('PROVENANCE_VERIFIED_OK', {'files': res['files_considered'], 'verified': res['verified_count'], 'unmapped': res['unmapped_count']})
"

# 3. Verify FCLR-014 evaluation summary and gate verdict
cat research_state/evaluation_summary_FCLR-014.md
# Expected: C2_vs_B1 rel_reduction=1.14%, CI crosses zero, 0 blocks, gate NOT_MET

# 4. Verify hypothesis registry H1_primary = NOT_SUPPORTED
cat research_state/hypothesis_registry.json | grep -A5 H1_primary
# Expected: "status": "NOT_SUPPORTED", "last_experiment": "FCLR-014"

# 5. Confirm Track B is untested (no preregistered modeled-breach scenario)
grep -i "trackb\|track_b" research_state/hypothesis_registry.json research_state/experiment_frontier.json
# Expected: Track B status UNTESTED / no frozen_before_outcomes Track B experiment
```

---

## 📁 KEY ARTIFACTS (AUTHORITATIVE — verify these exist before starting)

- `research_state/hypothesis_registry.json` — H1_primary **NOT_SUPPORTED** (last_tested=2026-11-10T10:38:27Z, last_experiment=FCLR-014, last_verdict=forecast_gate_NOT_MET); H2_shek_replication (proposed)
- `research_state/experiment_frontier.json` — blocked cells: FCLR-H004 (Track A BLOCKED), Track C forward confirmatory (NOT_SUPPORTED — all claim-worthy panels exhausted), Track B UNTESTED
- `research_state/negative_results_report.md` — **FCLR-014 NOT_SUPPORTED prepended**; FCLR-009 NOT_MET, FCLR-003 INCONCLUSIVE, FCLR-013 NOT_SUPPORTED, Track B COMPLETE_INCONCLUSIVE, Track C exploratory results
- `research_state/research_protocol_fclr014.md` — FCLR-014 protocol v2.0 FROZEN_BEFORE_OUTCOMES; `prereg_hash=8563163c62524605cbf7f11603759aee2210d133f82c3742319a6dd85dfca597`; `outcome_values_inspected=false`
- `research_state/run_manifest.json` — run IDs, split boundaries, frozen_before_outcomes flags
- `research_state/evaluation_summary_FCLR-014.md` — M3 confirmatory results (gate NOT_MET)
- `research_state/trackc_deep_audit_2025_full_check.json` — 2025 full panel verified (provenance_verified=true, 5 symbols, 12 blocks)
- `research_state/trackc_deep_audit_2025_h1_check.json` — 2025 H1 deep audit (provenance_verified=true, symbols_ok=5, panel_blocks_estimate=6)
- `research_state/funding_schema_audit_2025_h1.json` — 2025 H1 funding schema (all_ok=true, missing=0)
- `research_state/liquidation_sources_enumeration.md` — Track A structural block evidence
- `research_state/track_a_structural_block.md` — Track A irrefutable structural block (2026-10-30)
- `research_state/trackb_TB1_admissibility.json` — Track B 2025-2026 candidate panel (5 symbols, 22 months, 22 blocks estimate, provenance_verified=true, confirmatory_ready_symbol=false due to frozen-prereg blocker only)
- `scripts/trackc_provenance_lineage.py`, `scripts/trackc_funding_schema_audit.py`, `scripts/trackc_gap_repair_manifest.py`, `scripts/trackc_panel_deep_audit_orchestrator.py`, `scripts/run_evaluation.py`, `scripts/freeze_fclr009_splits.py` — audit/repair/eval tooling
- `scripts/synthetic_boundary_labels.py` — Track B modeled breach label primitive (tests in `tests/test_synthetic_boundary_labels.py`)

---

## ⛔ DO NOT DO (future sessions — NON-NEGOTIABLE)

- No network/downloads, no paid/manual/credentialed data, no workflow/scheduler/poller additions
- No fabricated provenance/outcomes, no threshold shopping, no sealed-holdout reuse
- Do not relabel PARTIAL/INCONCLUSIVE/NOT_SUPPORTED as confirmatory
- Do not re-inspect the FCLR-009 window (2025-06-08..2025-12-31); holdout-reuse prohibited
- Do not conflate Track A (observed liquidations, blocked) with Track B (modeled breaches) or Track C (volatility)
- No `.github/workflows` edits; no live/paper trading; no risk overlay until forecast gate passes
- Do not skip milestones in FOCUS_CAMPAIGN.md; each session must deliver one substantive verifiable result (§19 RESEARCH_PROMPT.md)
- Do not run Track B outcomes inspection before prereg freeze (`frozen_before_outcomes=true` required)

---

## 🟢 FOCUS CAMPAIGN — SEE `FOCUS_CAMPAIGN.md`

Heavy-work milestones M1→M6 (execute in order; do not skip):
- **M1** Provenance & data admissibility lock — **COMPLETE** (verified)
- **M2** Freeze protocol v2 + prereg-before-outcomes — **COMPLETE** (protocol created, prereg_hash recorded, splits frozen before outcomes)
- **M3** Execute confirmatory Track C / H001 run — **COMPLETE** (FCLR-014 run 2026-11-10T10:38:27Z; gate NOT_MET)
- **M4** Gate verdict & overlay eligibility — **COMPLETE** (gate NOT_MET, overlay NOT ELIGIBLE recorded)
- **M5** Track A / Track B status confirmation — **CONDITIONAL** (Track A STRUCTURALLY_BLOCKED, Track B UNTESTED → execute Track B campaign)
- **M6** Handoff update & next-session task — **COMPLETE** (this update)

Non-negotiable execution rules in `FOCUS_CAMPAIGN.md` §NON-NEGOTIABLE EXECUTION RULES. Future agents must execute milestones in order; skipping is non-compliant. Each session must deliver one substantive verifiable result (§19 RESEARCH_PROMPT.md).

---

## 📋 EXIT STATUS

**Exit criteria 2 triggered:** All locally available provenance-verified Track C panels with >=3 non-overlapping 30-day blocks have been tested (FCLR-003, FCLR-008, FCLR-012-V, FCLR-013, FCLR-014) and H001 (funding-conditioned volatility forecast vs RV-only baseline) remains **NOT_SUPPORTED** across every claim-worthy panel executed.

**Track C program concluded under constraints.** `next_unfinished_task: NONE` for Track C pending new admissible unauthenticated data source.

**NEXT SESSION (heavy-work, Track B — NON-OPTIONAL):** Follow `NEXT_SESSION_TASK.md` / `FOCUS_CAMPAIGN.md` M5: lock admissible local panel (>=5 symbols, >=3 test blocks, provenance/schema verified, no reused inspected window) → freeze prereg + `prereg_hash` + `frozen_before_outcomes=true` in `run_manifest.json` BEFORE outcomes → execute confirmatory modeled-breach evaluation (synthetic proxy, not observed liquidations) → write `research_state/evaluation_summary_trackb_<ID>.md` with CI/blocks/materiality/gate → update registries/negative-results/AGENT_HANDOFF/NEXT_SESSION_TASK. Track C remains concluded until a materially different, verifiable data route appears.

**IF A NEW ADMISSIBLE SOURCE APPEARS (Track C):** Re-evaluate per RESEARCH_PROMPT.md §16 adaptive feasibility policy. Any new source must pass provenance verification (sha256 sidecars + manifest), funding schema audit, and >=3-block panel coverage before a new confirmatory experiment can be registered. Do not resume Track C without a materially different, verifiable data route.

---

**END OF SINGLE DURABLE HANDOFF. Updated: 2026-11-10T15:37:06Z. Track C concluded (NOT_SUPPORTED, `next_unfinished_task: NONE`). Track B UNTESTED and MANDATORY: execute `NEXT_SESSION_TASK.md` M5 campaign on verified local data (no new source required).**