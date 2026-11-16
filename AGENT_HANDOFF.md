# AGENT HANDOFF — 2026-11-16T02:47:42Z (sole durable handoff)

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION
**Priority (repo: Funding-conditioned-volatility-and-liquidation-risk):** Execute the mandatory FCLR-RCA-011 heavy reproducibility/integrity campaign on cached data (no trigger fired). Do **not** stop after trigger checks or partial unit tests alone — the session is incomplete until the RCA attribution and implementation cross-check artifacts are written and the full regression gate is green.

### Step 0 — unblock the environment bottleneck (do this first)
`numpy/pandas/scipy/pyarrow/statsmodels` are listed in `requirements.txt` but are absent from this runtime. Install them before any RCA work:
```bash
pip install -r requirements.txt statsmodels
python3 -c "import numpy, pandas, pyarrow, scipy, statsmodels; print('deps OK')"
```
If `pip install` fails (no network / no wheel), record the exact pip error in the session progress note and fall back to the cached-panel diagnostics that do not require a fresh fit (Phase B1 below still needs a working OLS — if impossible, document the precise blocker and proceed to Phase C with `INCONCLUSIVE` for the attribution sub-question only). Do not fabricate attribution results.

### Step 1 — run the cheapest deterministic gates first
```bash
python3 -m unittest discover -q
python3 scripts/check_tracka_scope_registry_drift.py
python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118
```
All must be green (0 failures, 0 errors) before claiming completion. The last time these ran, 6 of 38 tests errored solely on `ModuleNotFoundError: numpy` via the `scripts.coupled_robust_eval` import chain in `tests/test_tracka_hardening_118` — confirm that is now resolved.

### Step 2 — Phase B (FCLR-RCA-011, write only to `research_state/session_<UTC>/`)
The `research_state/` root is at capacity 498/500 — every new artifact goes in a fresh `research_state/session_<UTC>/` subdirectory.

**B1. Nested feature attribution** — decompose the C2-vs-B1 recompute degradation into funding-feature vs EMA24-feature contributions. On `research_state/session_20261116T0040Z/fclr011_recompute_panel_20261116T004150Z.parquet` (or fresh `python3 scripts/fclr011_recompute_audit.py --out-utc <UTC>`), estimate nested QLIKE for B1, B1+funding, B1+ema24, B1+funding+ema24 with identical train-only scaling, Duan smearing, 7-day purge/embargo and paired 24h block bootstrap (2000 reps). Emit `rca011_feature_attribution_<UTC>.{json,md}`.
**B2. Implementation cross-check** — re-fit the frozen design with an independent OLS path (`statsmodels.OLS` or QR/SVD) to rule out `numpy.lstsq`/smearing artifacts. Emit `rca011_impl_crosscheck_<UTC>.json` with per-contrast diffs vs the canonical recompute.
**B3. Sealed bridge extension** — extend `research_state/session_20261116T023837Z/rca011_sealed_bridge_20261116T023837Z.{json,md}` (already tabulates sealed +4.94%/+1.36%/+3.63% at n=10,785 vs recompute -294.01%/-342.67%/+10.99% at n=10,905, attributing the gap to premium-slot unavailability + a 120-row eligibility delta) with the B1/B2 attribution and cross-check findings, plus any panel-diff evidence obtainable without the sealed LFS pointer.
**B4. Power template** — `research_state/session_20261116T023837Z/prereg_template_trigger_gated_20261116T023837Z.json` already encodes >=3 non-overlapping 30d blocks, MDE below 2% floor, Holm, `outcome_data_inspected_before_freeze=false`, §16 audit before freeze. Refine only if B1/B2 imply a specific design constraint.

### Step 3 — Phase C synthesis
Write/update `program_power_synthesis_<UTC>.{json,md}` in the session dir. Classify FCLR-011 as (a) true absence of skill, (b) underpowered/degenerate, or (c) feature/back-transform/artifact-driven — citing the B1/B2 artifacts. State an honest `next_action_heavy`.

### Step 4 — update this handoff and stop cleanly
Update `AGENT_HANDOFF.md` in place with: exact commands run, exact results (pass/fail counts, artifact paths), any blockers with evidence, and the single highest-value next task. Do not commit merely to show activity. Do not mutate sealed artifacts, do not edit `.github/workflows/*`, do not fabricate data or outcomes, keep the rank-0 `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` TRIGGER_ONLY sentinel active.

## Trigger check (performed once at 2026-11-16T02:40:53Z; do not re-poll)
- Sources read once: `research_state/resume_trigger_registry.json`, `research_state/ironflow_monitor_state.json`. No re-probe, no polling.
- Artifact: `research_state/session_20261116T023837Z/trigger_check_20261116T023837Z.json`.
- **Verdict: NO_TRIGGER_FIRED.** All four triggers OPEN: `GATE4_BRANCH_1` (human/legal), `NEW_OBSERVED_LIQUIDATION_SOURCE`, `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO`.
- Ironflow: `data_through=2026-10`; event/fill parquet months available through 2026-10; 2026-11..2027-01 confirmed absent as available data. No trigger-gated advance is permitted.

## What changed this session & why
- **Corrected stale/bottlenecked handoff:** prior handoff claimed FCLR-009 evaluation "never run". Verified `research_state/evaluation_summary_FCLR-009.md` (2026-11-10T00:18:07Z) exists and is **NOT_MET** (C2 vs B1 -0.43%, 95% CI [-0.003120, 0.006165] crosses zero; 5 instruments, 6 non-overlapping 30d test blocks). **Do not re-run FCLR-009.** Direction reconciled to frontier rank-0 `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` and `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md`.
- **Phase B progress (cached, no outcomes fabricated):** authored `research_state/session_20261116T023837Z/rca011_sealed_bridge_20261116T023837Z.{json,md}` and `research_state/session_20261116T023837Z/prereg_template_trigger_gated_20261116T023837Z.json`; recorded `session_progress_20261116T023837Z.md`.
- **Key integrity fact (from existing artifacts):** independent recompute (`session_20261116T0040Z/reproducibility_recompute_2026-11-16T00:45:10Z.json`) shows sealed FCLR-011 PASS **not independently reproduced** (C2_vs_B1 -294.01% vs sealed +4.94%; C1_vs_B1 -342.67%; C2_vs_C1 +10.99%; n_pairs 10,905 vs 10,785; same 2026-05-08..2026-08-06 test window). Recompute premium slot not computable from cached 2026 archive (C2 degrades to C1+EMA24). FCLR-011 is fragile/non-promotable pending attribution/cross-check.

## Current gate/program state (authoritative)
- **Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z`, status TRIGGER_ONLY / BOUNDED_TRIGGER_ONLY, `all_terminal=true`, `next_action_heavy=null` (agent-removable heavy work = bounded RCA/hardening campaign in `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md`).
- **FCLR-H001 / FCLR-009:** evaluation complete, **NOT_MET** (see `research_state/evaluation_summary_FCLR-009.md`); do not rerun.
- **FCLR-011:** sealed PASS not independently reproduced (integrity finding); RCA pending.
- **Track A:** no new admissible observed-liquidation data (ironflow through 2026-10). **Track B:** sealed NOT_SUPPORTED. **Track C:** terminal on cached confirmatory designs. **H2:** EXPLORATORY_ONLY, not promotable.
- **Gate 4 Branch 1:** blocked on human/legal attestation (agent cannot set).
- **Registries:** no run_manifest/hypothesis/frontier mutations made this session; FCLR-009 eval artifact exists but registry reconciliation should be done carefully/only if schema-consistent with evidence.

## Blockers & commands/results
- **Env blocker:** `numpy/pandas/scipy/pyarrow/statsmodels` absent (Python 3.12.3; `pip list` lacks them; `import numpy` fails). Prevents nested QLIKE attribution, implementation cross-check, and full suite. See Step 0 for the install + fallback.
- **Attempted gates (partial, prior session):** `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118` → **Ran 38 tests, 6 errors, 0 assertion failures** (all `ModuleNotFoundError: No module named 'numpy'` via `scripts.coupled_robust_eval` import in `tests/test_tracka_hardening_118`). `discover -q` and drift check must be re-run to completion after deps installed.
- **State constraints:** `research_state/` root md/json = 498/500 (write new artifacts to `research_state/session_<UTC>/` only). Never edit `.github/workflows/*`. Never fabricate data/outcomes.

## Next materially different free route (if RCA completes and no trigger fires)
Hold TRIGGER_ONLY sentinel with green suite and finalized RCA/power synthesis documenting non-reproducible/fragile FCLR-011 and underpowered/terminal cached-data state. Advance only on a satisfied trigger with §16 admissibility audit + NEW pre-outcomes prereg (`outcome_data_inspected_before_freeze=false`), materially different estimand, >=3 non-overlapping 30d blocks, MDE below 2% floor, Holm family preregistered.

## Tombstones (no authority — retained to block stale instructions)
- `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`: tombstoned 2026-11-15T22:57:29Z.
- `AGENT_HANDOFF_20261115T073240Z.md`: SUPERSEDED — ignore.