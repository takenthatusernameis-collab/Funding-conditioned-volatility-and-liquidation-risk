# AGENT HANDOFF — 2026-11-16T02:40:53Z (sole durable handoff)

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION
**Priority (repo: Funding-conditioned-volatility-and-liquidation-risk):** Execute the mandatory FCLR-RCA-011 heavy campaign on cached data (no triggers fired). Do **not** stop after trigger checks or unit tests alone.

1. **Install/ensure compute deps** in this environment (`pip install -r requirements.txt` and `statsmodels` if needed) so `numpy/pandas/pyarrow` imports and the full test suite can run. This is the current execution bottleneck.
2. **Phase B (FCLR-RCA-011, write to `research_state/session_<UTC>/`, root is at capacity 498/500):**
   - **Nested feature attribution:** on `research_state/session_20261116T0040Z/fclr011_recompute_panel_20261116T004150Z.parquet` (or fresh `python3 scripts/fclr011_recompute_audit.py --out-utc <UTC>`), estimate nested QLIKE for B1, B1+funding, B1+ema24, B1+funding+ema24 (C1,C2) with same train-only scaling, smearing, purge/embargo and paired block bootstrap. Decompose C2_vs_B1 degradation into funding-feature vs EMA24 contribution. Emit `rca011_feature_attribution_<UTC>.{json,md}`.
   - **Implementation cross-check:** re-fit frozen design with independent OLS path (e.g. `statsmodels.OLS` or QR/SVD) to rule out `numpy.lstsq`/smearing artifacts. Emit `rca011_impl_crosscheck_<UTC>.json`.
   - **Complete/extend sealed bridge:** `research_state/session_20261116T023837Z/rca011_sealed_bridge_20261116T023837Z.{json,md}` already tabulates sealed vs recompute contrasts and attributes gap (premium slot + 120-row eligibility delta; sealed not independently reproduced). Extend with attribution/cross-check findings and any panel-diff evidence if available.
   - **Power remediation template:** `research_state/session_20261116T023837Z/prereg_template_trigger_gated_20261116T023837Z.json` exists (>=3 non-overlapping 30d blocks, MDE below 2% floor, Holm, `outcome_data_inspected_before_freeze=false`, §16 audit before freeze). Refine if RCA implies specific design constraints.
3. **Phase C:** write/update `program_power_synthesis_<UTC>.{json,md}` in the session dir with RCA attribution — classify FCLR-011 as (a) true absence of skill, (b) underpowered/degenerate, or (c) feature/back-transform/artifact-driven — citing RCA artifacts. State honest `next_action_heavy`.
4. **Regression gates (must be green):** `python3 -m unittest discover -q` (0 failures), `python3 scripts/check_tracka_scope_registry_drift.py` PASS, `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118` PASS. Keep rank-0 TRIGGER_ONLY sentinel active; never mutate sealed artifacts; never edit `.github/workflows/*`.
5. **Stop cleanly only** when trigger checked once (record verdict), Phase B RCA artifacts complete, Phase C synthesis updated, gates green, and this handoff updated with exact commands/results/blockers.

## Trigger check (performed once, 2026-11-16T02:40:53Z)
- Sources: `research_state/resume_trigger_registry.json`, `research_state/ironflow_monitor_state.json` (no polling/re-probe). Artifact: `research_state/session_20261116T023837Z/trigger_check_20261116T023837Z.json`.
- **Verdict: NO_TRIGGER_FIRED.** `GATE4_BRANCH_1` OPEN (human/legal). `NEW_OBSERVED_LIQUIDATION_SOURCE` OPEN. `HL_LABEL_EXTENSION` OPEN. `EXPANSION_ROBUSTNESS_REDO` OPEN.
- Ironflow: `data_through=2026-10`; event/fill parquet months available through 2026-10; 2026-11..2027-01 not present as available data.

## What changed this session & why
- **Corrected stale/bottlenecked handoff:** prior handoff claimed FCLR-009 evaluation “never run”. Verified `research_state/evaluation_summary_FCLR-009.md` (2026-11-10T00:18:07Z) exists and is **NOT_MET** (C2 vs B1 -0.43%, 95% CI [-0.003120, 0.006165] crosses zero; 5 instruments, 6 non-overlapping 30d test blocks). **Do not re-run FCLR-009.** Reconciled direction to frontier rank-0 `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` and `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md`.
- **Phase B progress (cached, no outcomes fabricated):** authored `research_state/session_20261116T023837Z/rca011_sealed_bridge_20261116T023837Z.{json,md}` and `research_state/session_20261116T023837Z/prereg_template_trigger_gated_20261116T023837Z.json`; recorded `session_progress_20261116T023837Z.md`.
- **Key integrity fact (from existing artifacts):** independent recompute (`session_20261116T0040Z/reproducibility_recompute_2026-11-16T00:45:10Z.json`) shows sealed FCLR-011 PASS **not independently reproduced** (C2_vs_B1 -294.01% vs sealed +4.94%; C1_vs_B1 -342.67%; C2_vs_C1 +10.99%; n_pairs 10,905 vs 10,785; same test window). Recompute premium slot not computable from cached 2026 archive (C2 degrades to C1+EMA24). FCLR-011 is fragile/non-promotable pending attribution/cross-check.

## Current gate/program state (authoritative)
- **Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z`, status TRIGGER_ONLY / BOUNDED_TRIGGER_ONLY, `all_terminal=true`, `next_action_heavy=null` (agent-removable heavy work = bounded RCA/hardening campaign in `FCLR_HEAVY_CAMPAIGN_NEXT.md`).
- **FCLR-H001 / FCLR-009:** evaluation complete, **NOT_MET** (see `research_state/evaluation_summary_FCLR-009.md`); do not rerun.
- **FCLR-011:** sealed PASS not independently reproduced (integrity finding); RCA pending.
- **Track A:** no new admissible observed-liquidation data (ironflow through 2026-10). **Track B:** sealed NOT_SUPPORTED. **Track C:** terminal on cached confirmatory designs. **H2:** EXPLORATORY_ONLY, not promotable.
- **Gate 4 Branch 1:** blocked on human/legal attestation (agent cannot set).
- **Registries:** no run_manifest/hypothesis/frontier mutations made this session; FCLR-009 eval artifact exists but registry reconciliation should be done carefully/only if schema-consistent with evidence.

## Blockers & commands/results
- **Env blocker:** `numpy/pandas/pyarrow/statsmodels` absent (Python 3.12.3; `pip list` lacks them; `import numpy` fails). Prevents nested QLIKE attribution, implementation cross-check, and full suite.
- **Attempted gates (partial):** `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118` → **Ran 38 tests, 6 errors, 0 assertion failures** (all `ModuleNotFoundError: No module named 'numpy'` via `scripts.coupled_robust_eval` import in `tests/test_tracka_hardening_118`). `discover -q` and drift check not fully green due to missing deps.
- **State constraints:** `research_state/` root md/json = 498/500 (write new artifacts to `research_state/session_<UTC>/` only). Never edit `.github/workflows/*`. Never fabricate data/outcomes.

## Next materially different free route (if RCA completes and no trigger fires)
Hold TRIGGER_ONLY sentinel with green suite and finalized RCA/power synthesis documenting non-reproducible/fragile FCLR-011 and underpowered/terminal cached-data state. Advance only on a satisfied trigger with §16 admissibility audit + NEW pre-outcomes prereg (`outcome_data_inspected_before_freeze=false`), materially different estimand, >=3 non-overlapping 30d blocks, MDE below 2% floor, Holm family preregistered.
