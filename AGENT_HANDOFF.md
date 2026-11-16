# AGENT HANDOFF — 2026-11-16T00:54:32Z

**Project:** Funding-conditioned Volatility and Liquidation Risk (FCLR)
**Repository:** `Funding-conditioned-volatility-and-liquidation-risk`
**Sole durable handoff:** this file (`AGENT_HANDOFF.md`).
- `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md` = tombstones (no authority).
- `AGENT_HANDOFF_20261115T073240Z.md` = RETIRED/SUPERSEDED — ignore.
- `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md` = detailed next focus campaign (authoritative companion to this handoff).
- `research_state/session_20261116T0040Z/` = this session's heavy-work artifacts (kept out of `research_state/` root to respect the 500-file root md/json cap enforced by `scripts/tracka_resume_check.py` + `tests/test_tracka_hardening_099.py`).

---

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (2026-11-16T00:54:32Z) — HEAVY, DEFAULT, NON-SKIPPABLE

**Mission (FCLR):** determine whether extreme perpetual-futures funding conditions, realized volatility, and pre-specified price-dislocation/smoothing features improve out-of-sample forecasts of future volatility and liquidation-related stress — using only admissible, free, unauthenticated data. Every cached-data confirmatory estimand is terminal and externally blocked on new observed liquidation data. **The only agent-removable heavy work is the FCLR-RCA-011 root-cause / adversarial re-audit below. Do not stop after the trigger check or after "suite is green" alone.**

Execute in order **A → B → C → E** (D only if a trigger fires). This campaign is defined in full in `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md`; the summary here is binding.

### A. Trigger check (once at session start, no polling)
1. Read `research_state/resume_trigger_registry.json` and `research_state/ironflow_monitor_state.json`; confirm all 4 triggers remain OPEN and `data_through=2026-10` with 2026-11..2027-01 absent. Record timestamp + verdict in this handoff. Do not re-probe or poll.
2. If any trigger is newly satisfied with its required evidence artifact, pivot immediately to D.

### B. FCLR-RCA-011 root-cause & adversarial re-audit (heavy, mandatory)
3. **Feature attribution.** On `research_state/session_20261116T0040Z/fclr011_recompute_panel_20261116T004150Z.parquet` (or a fresh recompute), estimate nested QLIKE for B1, B1+funding, B1+ema24, B1+funding+ema24 (C1, C2) with the same train-only scaling, smearing, purge/embargo and paired block bootstrap. Decompose the C2_vs_B1 degradation into the funding-feature contribution vs the EMA24 contribution. Write `research_state/session_20261116T0040Z/rca011_feature_attribution_<UTC>.{json,md}` (use the session subdir so the root cap is respected).
4. **Implementation cross-check.** Re-fit the frozen design with an independent OLS path (e.g. `statsmodels.OLS` or QR/SVD) and confirm the non-reproduction is not a `numpy.lstsq`/smearing artifact. Write `research_state/session_20261116T0040Z/rca011_impl_crosscheck_<UTC>.json`.
5. **Sealed-vs-recompute bridge.** For each sealed contrast (C2_vs_B1, C1_vs_B1, C2_vs_C1) tabulate sealed vs recomputed rel-reduction, sign, and sample/coverage differences (10,785 sealed pairs vs 10,905 recompute pairs). State whether the gap is explained by the missing premium slot, the test window, or the model class. Write `research_state/session_20261116T0040Z/rca011_sealed_bridge_<UTC>.{json,md}`.
6. **Power remediation template.** Produce a concrete, adequately-powered prereg skeleton for the first trigger-gated advance: >=3 non-overlapping 30-day blocks, target MDE below the 2% materiality floor given realistic event counts, Holm family pre-specified, `outcome_data_inspected_before_freeze=false`. Write `research_state/session_20261116T0040Z/prereg_template_trigger_gated_<UTC>.json`.
7. **Regression gates green.** `python3 -m unittest discover -q` (0 failures), `python3 scripts/check_tracka_scope_registry_drift.py` PASS, `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118` PASS. Keep the rank-0 TRIGGER_ONLY sentinel active.

### C. Program-level power synthesis update (mandatory)
8. Update `research_state/session_20261116T0040Z/program_power_synthesis_<UTC>.{json,md}` with the RCA attribution: classify FCLR-011 as (a) true absence of skill, (b) underpowered/degenerate design, or (c) feature/back-transform artifact. Cite the RCA artifacts. Conclude with an honest `next_action_heavy`.

### D. Trigger-gated advance (only if a trigger fires)
9. Freeze a NEW, materially different pre-outcomes prereg (`outcome_data_inspected_before_freeze=false`), run §16 admissibility audit, execute eval+gates, register new scripts in both scope registries, update `experiment_frontier.json`/`hypothesis_registry.json`, install as rank-0 heavy cell with honest verdict. Never re-run concluded estimands, never re-probe TERMINAL_NO_GO families, never re-score sealed results.

### E. Closeout (required)
10. Update this handoff with timestamp, exact commands/results, Phase B/C artifact paths, and remaining external blockers. Commit a checkpoint only if repo convention/permissions require it; otherwise leave the tree clean and documented.

**Completion criteria (all required):** trigger checked once with verdict recorded; every Phase B artifact written; Phase C synthesis updated with per-track MDE/classification; full suite + drift + guards green; this handoff reflects ground truth. "No trigger → stop cleanly" is NOT completion.

---

## STATE (verified 2026-11-16T00:54:32Z; HEAD 47692441e)

### What this session changed (bottlenecks removed)
1. **Fixed two real defects in `scripts/fclr011_recompute_audit.py` that had blocked every prior reproducibility run:**
   - `eval_rows` was a pre-scaling copy of `test_core` missing `funding_z` / `abs_fund_pct_z` / `ema24_dist_z`, so C1/C2 design matrices returned `None` and the audit always exited `INCONCLUSIVE`.
   - `predict()` read the shared `spec['smearing']` (last model's value) instead of the fitted per-model `fit['smearing']`, so all models used C2's Duan smearing.
   After the fix the audit runs end-to-end and returns a real verdict.
2. **Produced the missing Phase B/C heavy artifacts** (all under `research_state/session_20261116T0040Z/`):
   - `reproducibility_recompute_2026-11-16T00:45:10Z.json` — FCLR-011 vs sealed; v3_30d funding ablation vs stored.
   - `manifest_validation_2026-11-16T00:45:26Z.json` — 240 JSON parsed OK, 7 LFS pointers reported, 0 parse failures.
   - `result_integrity_2026-11-16T00:45:48Z.json` — 22 hypotheses all terminal, frontier unique, rank-0 sentinel intact, verdict PASS.
   - `leakage_audit_2026-11-16T00:43:41Z.md` — leakage invariance + bootstrap reproducibility true.
   - `program_power_synthesis_2026-11-16T00:46:29Z.{json,md}` — per-track MDE + classification.
   - `evaluation_summary_FCLR-011-RECOMPUTE-20261116T004150Z.{json,md}` + `fclr011_recompute_panel_build_report_20261116T004150Z.json`.
   - `evaluation_summary_funding_repro_2026-11-16T00:43:02Z.md` + `run_manifest_funding_repro_2026-11-16T00:43:02Z.json`.

### Key findings (ground truth)
- **FCLR-011 sealed PASS is NOT independently reproduced.** Clean OLS recompute: C2_vs_B1 = **-294.01 pct-points** (sealed +4.94%), C1_vs_B1 = -342.67, C2_vs_C1 = +10.99, on 2026-05-08..2026-08-06 (10,905 pairs, 91 UTC-day blocks). Cause: C2 premium slot is not computable from the cached 2026 archive; C2 degrades to C1 + EMA24 distance and funding features worsen out-of-sample QLIKE. Treat the sealed FCLR-011 result as fragile and never promotable. This is a **material integrity finding**, not a script failure.
- **v3_30d funding ablation reproduces exactly:** E vs A point 0.487902 (expected 0.487902), identical CI and n_obs/n_blocks; verdict DATA-SUFFICIENT PILOT / INCONCLUSIVE on primary contrast.
- **Program power:** Track A underpowered (MDE ~25% vs 2% floor; xsec only 2/3 blocks); Track B degenerate/underpowered (TB1 zero events, TB2 MDE ~3.4% with 2 blocks); Track C true null / non-reproducible (MDE ~111%); H2 exploratory-only.
- **Concluded — do NOT re-run:** `FCLR-LIQ-XSEC-QLIKE-20261115T214949Z`, `FCLR-LIQ-XSEC-ORDERING-20261115T203507Z`, `FCLR-LIQ-COMBINED-20261115T185844Z` (all NOT_MET/SUPERSEDED). Hypotheses `H_fclr_liq_xsec_qlike_forecast`, `H_fclr_liq_xsec_ordering_forecast`, `H_fclr_liq_combined_panel_forecast` = NOT_MET.
- **Other terminal tracks:** `H1_primary` NOT_SUPPORTED (v3_30d data-sufficient but null); `H_trackb_modeled_breaches` NOT_SUPPORTED; `H2_shek_replication` EXPLORATORY_ONLY (`promotable=false`).
- **Triggers all OPEN (external):** `GATE4_BRANCH_1` (human/legal attestation), `NEW_OBSERVED_LIQUIDATION_SOURCE` (ironflow `data_through=2026-10`; 2026-11..2027-01 absent), `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` (do not re-run sealed designs). See `research_state/resume_trigger_registry.json`, `research_state/ironflow_monitor_state.json`.

### Regression / invariants
- Full suite: rerun in progress at handoff time; the previously red drift-preflight cascade (caused by 11 untracked root `research_state/*.md|json` files pushing the root count to 509 > 500) is fixed by relocating this session's artifacts to `research_state/session_20261116T0040Z/`. All previously failing drift/guard tests (099/101/102/103/104/105/107/108/110/125/126/127/128) pass in isolation after the move.
- Scope drift: `python3 scripts/check_tracka_scope_registry_drift.py` → `scripts=195 registry=195 reason=OK`.
- Rank-0 sentinel: `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` | `TRIGGER_ONLY` | `BOUNDED_TRIGGER_ONLY` | `next_action_heavy=null` | `all_terminal=true`.

### External blockers (agent cannot remove)
- No new admissible observed-liquidation data (ironflow Hyperliquid 2026-11..2027-01 parquet absent; fills absent for >=2026-11).
- Gate 4 Branch 1 blocked on human/legal Binance terms evidence (agent cannot set `RESOLVED_VERIFIED`).
- `H2_shek_replication` remains `EXPLORATORY_ONLY` (`promotable=false`).
- 7 LFS pointer-only manifests are not materializable in this sandbox (reported, never fabricated).

---

## BOTTLENECKS REMOVED (2026-11-16T00:54:32Z session) — keep removed
1. **Broken reproducibility audit fixed** (stale test frame + wrong smearing lookup) — prior sessions could never produce a valid FCLR-011 recompute verdict.
2. **Root-cap drift preflight unblocked** — moved this session's 12 md/json/parquet artifacts into `research_state/session_20261116T0040Z/`; root count back to 498 <= 500 and no untracked root md/json.
3. **Incidental tracked-file churn reverted** — `research_state/ironflow_fastpath_cache.json` and `research_state/leakage_audit.md` restored to HEAD.
4. **Stale handoff traps remain neutralized** — `NEXT_SESSION_TASK.md` / `NEXT_SESSION_HANDOFF.md` are tombstones; `AGENT_HANDOFF_20261115T073240Z.md` retired.

## HARD CONSTRAINTS (non-negotiable)
- ❌ Never reopen sealed/terminal families or mutate sealed artifacts; never edit `.github/workflows/*`.
- ❌ No outcome-peeking/threshold tuning before prereg; no paid/credentialed/manual data for outcomes.
- ❌ No polling, no re-running concluded estimands, no re-probing TERMINAL_NO_GO families.
- ❌ Do not fabricate new data/sources or claim triggers satisfied without required artifacts/fields.
- ❌ Do not add new files to `research_state/` root md/json beyond the 500 cap; use a session subdir.
- ✅ `H2_shek_replication` remains `EXPLORATORY_ONLY` (`promotable=false`).
- ✅ Exactly one durable handoff: `AGENT_HANDOFF.md`.

## KEY REFERENCES
- `research_state/experiment_frontier.json`, `research_state/resume_trigger_registry.json`, `research_state/ironflow_monitor_state.json`, `research_state/hypothesis_registry.json`
- `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md` (authoritative next focus campaign), `research_state/negative_results_report.md`
- `research_state/session_20261116T0040Z/` (this session's Phase B/C artifacts)
- `scripts/fclr011_recompute_audit.py` (fixed), `scripts/run_funding_ablations.py`, `scripts/run_gate4_v4_leakage_audit.py`, `scripts/tracka_resume_check.py`
- `tests/test_active_campaign_gate.py`, `tests/test_tracka_hardening_099.py`, `tests/test_tracka_hardening_117.py`, `tests/test_tracka_hardening_118.py`

**Next session:** execute A→B→C→E in order (heavy default). Stop only when the trigger is checked once, every Phase B/C artifact is written, the full suite/guards are green, and this handoff reflects ground truth with external blockers documented.