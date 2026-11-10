# AGENT_HANDOFF.md — Single Durable Handoff (REPO-NAME PRIORITY: Track C / H001 first)

**Updated:** 2026-11-10T09:42:00Z — **P0 ACTIVE.** Repo `Funding-conditioned-volatility-and-liquidation-risk` — repo-name priority = **Track C / H001 (funding-conditioned volatility forecast vs RV-only baseline)** first; Track A/B liquidation tracks secondary. Work continues under RESEARCH_PROMPT.md hard constraints (no network/paid/manual/credentialed data, no fabricated provenance, no threshold shopping, no sealed-holdout reuse, no Track conflation, no risk overlay until forecast gate passes).

---

## 🔴 INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION — 2026-11-10T09:42:00Z

**PRIMARY FOCUS (repo-name priority): Track C / H001 — funding-conditioned volatility forecast vs RV-only baseline.**

**Current state (verified this session):** dep-light gate 48/48 OK; provenance machine-verified=true (36001 records, unmapped_count=0); 2025 local panel (2025-01-01..2025-12-31) fully verified — 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), 365 days each, mark/index/premium/klines + funding complete, 12 non-overlapping 30-day blocks per symbol, all funding schema OK (`research_state/trackc_deep_audit_2025_full_check.json`).

**Already tested (preserved nulls, no re-use):** FCLR-009 on 2025-06-08..2025-12-31 (6 blocks) → NOT_MET (-0.43% QLIKE, CI crosses zero); FCLR-003 on 2024-10-02..2024-12-31 (3 blocks) → INCONCLUSIVE (CI crosses zero); FCLR-013 on 2026 Q3 (1 block) → NOT_SUPPORTED; FCLR-012-V on 2026-08-07..2026-11-02 (0 blocks) → INCONCLUSIVE. H001 remains NOT_SUPPORTED across every claim-worthy panel executed.

**Initial task:** Execute **FCLR-014 confirmatory** (C2 vs B1, next-24h realized variance QLIKE) on the **untested verified 2025 H1 window 2025-01-01..2025-06-07** (~158 days, >=3 non-overlapping 30-day blocks, 5 symbols paired). This window is provenance-verified and has NOT been inspected by FCLR-009 (which used 2025-06-08..12-31), so there is **no sealed-holdout reuse**.

**Prereg-before-outcomes (MANDATORY):** `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` is skeleton-frozen (FROZEN_BEFORE_OUTCOMES, outcome_values_inspected=false) but `prereg_hash=null` and splits are illustrative/copy of FCLR-002. Before computing any outcome:
1. Run deep audit on 2025 H1 window → confirm `confirmatory_resume_ready=true`, symbols_ok=5, series complete, provenance_verified=true.
2. Finalize `research_state/research_protocol_fclr014.md` (new protocol version, frozen splits for 2025-01-01..2025-06-07 with 7-day purge/embargo, 60/20/20 chronological, materiality floor >=2% relative QLIKE, Holm multiplicity, 2000-rep block bootstrap).
3. Record `prereg_hash` (sha256 of prereg file) and `split_boundaries_fclr014` with `frozen_before_outcomes=true` in `run_manifest.json`.
4. Only then run `FCLR_EXPERIMENT=FCLR-014 python scripts/run_evaluation.py` and write `research_state/evaluation_summary_FCLR-014.md`.

**If the 2025 H1 window fails the deep audit (series gaps / insufficient blocks / provenance gaps):** register a new pilot protocol version (new ID) on the widest untested local panel satisfying >=3 blocks + >=5 instruments, run it as a PILOT (not confirmatory), and report INCONCLUSIVE/NOT_SUPPORTED with preserved null. Do not relax gates, do not threshold-shop, do not promote.

**Secondary:** Track A (observed liquidations) remains STRUCTURALLY_BLOCKED (no admissible unauthenticated historical source). Track B (modeled boundary breaches) is UNTESTED — no margin/leverage scenario registered before outcome inspection. Never conflate tracks. Track C results are volatility/stress only, never observed-liquidation validation.

---

## 🔧 BOTTLENECKS REMOVED (verified this session)

| Bottleneck | Before | After | Evidence |
|---|---|---|---|
| Provenance not machine-verified | `provenance_verified=false`, 0 verified, 25 unmapped | `provenance_verified=true`, 36001 records indexed, unmapped_count=0 | `scripts/trackc_provenance_lineage.py` + adjacent `.sha256` sidecars; `verify_paths_with_manifests` → True, 0 |
| Dep-light reproducibility gate | baseline | 48/48 OK | `python -m unittest <9 dep-light test modules> -v` → Ran 48 tests in ~71s — OK |
| Funding schema/coverage (2024 Q1) | unverified | all 15 symbol-months schema OK, 0 missing, 0 bad | `scripts/trackc_funding_schema_audit.py --months 2024-01,2024-02,2024-03` → all_ok=true |
| 2025 panel data completeness | unverified | provenance_verified=true, 5 symbols × 365 days, 12 blocks each, required_series_complete=true | `research_state/trackc_deep_audit_2025_full_check.json` |

## ⛔ REMAINING STRUCTURAL BLOCKERS (not locally repairable, no network)

| Blocker | Detail | Next materially different route |
|---|---|---|
| MISSING_FUNDING_MONTH_FILE | `*`-fundingRate-2026-11.csv absent locally; no network | Use 2025 local panel (12 funding month files present per symbol) |
| CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES | `prereg_hash=null`; FCLR-014 splits illustrative only | Finalize protocol + splits for 2025 H1 window, record prereg_hash, `frozen_before_outcomes=true` BEFORE outcomes |
| HOLDOUT_REUSE_CONSTRAINT | FCLR-009 inspected 2025-06-08..2025-12-31; cannot re-inspect | Use untested 2025-01-01..2025-06-07 window for FCLR-014; never reuse FCLR-009 window |

## 📋 VERIFICATION COMMANDS FOR NEXT SESSION

```bash
# 1. Dep-light gate (must pass 48/48)
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator tests.test_trackc_provenance_lineage -v
# Expected: Ran 48 tests — OK

# 2. Provenance machine-verified on local funding data
python -c "
from scripts.trackc_provenance_lineage import verify_paths_with_manifests
from pathlib import Path
res = verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').glob('*-fundingRate-*.csv')], repo_root=Path('.'))
assert res['provenance_verified'] is True and res['unmapped_count'] == 0, res
print('PROVENANCE_VERIFIED_OK', res)
"

# 3. Deep audit on the untested 2025 H1 confirmatory window (must show symbols_ok=5, series complete, confirmatory_resume_ready=true)
python scripts/trackc_panel_deep_audit_orchestrator.py --cache research_state/data_cache --repo-root . --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --window-hint 2025_01,2025_02,2025_03,2025_04,2025_05,2025_06 --min-symbols 5 --min-blocks 3 --out research_state/trackc_deep_audit_2025_h1_check.json
# Expected: confirmatory_resume_ready=true, all_required_series_complete=true, provenance_verified=true, panel_blocks_estimate>=3

# 4. Funding schema audit for 2025 H1 window
python scripts/trackc_funding_schema_audit.py --repo-root . --cache research_state/data_cache --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --months 2025-01,2025-02,2025-03,2025-04,2025-05,2025-06 --out research_state/funding_schema_audit_2025_h1.json
# Expected: all_ok=true, missing=0
```

---

## 📁 KEY ARTIFACTS (AUTHORITATIVE)

- `research_state/final_confirmatory_verdict.md` — H001 NOT_SUPPORTED (FCLR-003 canonical); program closeout under prior constraints; superseded by this resume for the 2025 H1 untested window
- `research_state/final_inconclusive_report.md` — FCLR-001 pilot/inconclusive, gate NOT MET
- `research_state/hypothesis_registry.json` — H1_primary (proposed), H2_shek_replication (proposed)
- `research_state/experiment_frontier.json` — blocked cells: FCLR-H004 (Track A BLOCKED), FCLR-H001 forward confirmatory (INCONCLUSIVE)
- `research_state/negative_results_report.md` — FCLR-009 NOT_MET, FCLR-003 INCONCLUSIVE, FCLR-013 NOT_SUPPORTED, Track B COMPLETE_INCONCLUSIVE, Track C exploratory results
- `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` — FCLR-014 prereg skeleton FROZEN_BEFORE_OUTCOMES, prereg_hash=null, outcome_values_inspected=false
- `research_state/trackc_deep_audit_2025_full_check.json` — 2025 panel fully verified (provenance_verified=true, 5 symbols, 12 blocks)
- `research_state/run_manifest.json` — run IDs, split boundaries, frozen_before_outcomes flags
- `scripts/trackc_provenance_lineage.py`, `scripts/trackc_funding_schema_audit.py`, `scripts/trackc_gap_repair_manifest.py`, `scripts/trackc_panel_deep_audit_orchestrator.py`, `scripts/run_evaluation.py`, `scripts/freeze_fclr009_splits.py` — audit/repair/eval tooling

---

## ⛔ DO NOT DO (future sessions)

- No network/downloads, no paid/manual/credentialed data, no workflow/scheduler/poller additions
- No fabricated provenance/outcomes, no threshold shopping, no sealed-holdout reuse
- Do not relabel PARTIAL/INCONCLUSIVE/NOT_SUPPORTED as confirmatory
- Do not re-inspect the FCLR-009 window (2025-06-08..2025-12-31); holdout-reuse prohibited
- Do not conflate Track A (observed liquidations, blocked) with Track B (modeled breaches) or Track C (volatility)
- No `.github/workflows` edits; no live/paper trading; no risk overlay until forecast gate passes

---

## 🟢 FOCUS CAMPAIGN — SEE `FOCUS_CAMPAIGN.md`

Heavy-work milestones M1→M6 (execute in order; do not skip):
- M1 Provenance & data admissibility lock (REQUIRED, unblocked)
- M2 Freeze protocol v2 + prereg-before-outcomes (REQUIRED)
- M3 Execute confirmatory Track C / H001 run (REQUIRED)
- M4 Gate verdict & overlay eligibility (REQUIRED)
- M5 Track A / Track B status confirmation (CONDITIONAL)
- M6 Handoff update & next-session task (REQUIRED, every session)

Non-negotiable execution rules are in `FOCUS_CAMPAIGN.md` §NON-NEGOTIABLE EXECUTION RULES. Future agents must execute milestones in order; skipping milestones is non-compliant. Each session must deliver one substantive verifiable result (§19 RESEARCH_PROMPT.md).

---

**END OF SINGLE DURABLE HANDOFF. next_unfinished_task: FCLR-014 confirmatory on untested verified 2025 H1 window (2025-01-01..2025-06-07, 5 symbols, >=3 blocks) — finalize frozen prereg, record prereg_hash, then run C2 vs B1 BEFORE any outcome inspection.**
**Updated: 2026-11-10T09:42:00Z**
