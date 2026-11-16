# AGENT HANDOFF — 2026-11-16T02:05:42Z

**Project:** Funding-conditioned Volatility and Liquidation Risk (FCLR)
**Repository:** `Funding-conditioned-volatility-and-liquidation-risk`
**Sole durable handoff:** this file (`AGENT_HANDOFF.md`). Nothing else has campaign authority.
- `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md` = tombstones (no authority).
- `AGENT_HANDOFF_20261115T073240Z.md` = RETIRED/SUPERSEDED — ignore.
- `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md` = detailed next focus campaign (binding companion to this handoff).
- New artifacts this session go in a NEW session subdir `research_state/session_<UTC>/`, never in the `research_state/` root (root cap 500 md/json; currently 498 — only 2 slots of slack).

---

## INITIAL TASK MESSAGE FOR THE NEXT AGENTIC WORK SESSION (2026-11-16T02:05:42Z) — HEAVY, DEFAULT, NON-SKIPPABLE

**Mission (inferred from the repository name — funding-conditioned volatility and liquidation risk):** determine whether extreme perpetual-futures funding conditions, realized volatility, and pre-specified price-dislocation/smoothing features improve out-of-sample forecasts of future volatility and liquidation-related stress, using only admissible, free, unauthenticated data. Every cached-data confirmatory estimand is terminal and externally blocked on new observed liquidation data. **The only agent-removable heavy work is the FCLR-RCA-011 root-cause / adversarial re-audit below. Running the trigger check or the unit suite is NOT completion.**

Execute in order **A → B → C → E** (D only if a trigger fires). Full detail is in `research_state/FCLR_HEAVY_CAMPAIGN_NEXT.md`; the summary here is binding.

### A. Trigger check (once at session start; no polling, no re-probe)
1. Read `research_state/resume_trigger_registry.json` and `research_state/ironflow_monitor_state.json`. Confirm all 4 triggers remain OPEN and `data_through=2026-10` with 2026-11..2027-01 absent. Record timestamp + verdict in this handoff.
2. If any trigger is newly satisfied **with its required evidence artifact**, pivot immediately to D.
3. Verified at handoff time (2026-11-16T02:05:42Z): all 4 OPEN; `data_through=2026-10`; `consecutive_absent=3`; `GATE4_BRANCH_1` OPEN (human/legal); `HL_LABEL_EXTENSION` OPEN; `EXPANSION_ROBUSTNESS_REDO` OPEN (do not re-run sealed designs).

### B. FCLR-RCA-011 root-cause & adversarial re-audit (heavy, mandatory)
Create `research_state/session_<UTC>/` for every artifact in this phase.

4. **Feature attribution.** On `research_state/session_20261116T0040Z/fclr011_recompute_panel_20261116T004150Z.parquet` (or a fresh recompute via `python3 scripts/fclr011_recompute_audit.py --out-utc <UTC>`), estimate nested QLIKE for B1, B1+funding, B1+ema24, B1+funding+ema24 (C1, C2) with the same train-only scaling, smearing, purge/embargo and paired block bootstrap. Decompose the C2_vs_B1 degradation into the funding-feature contribution vs the EMA24 contribution. Write `rca011_feature_attribution_<UTC>.{json,md}`.
5. **Implementation cross-check.** Re-fit the frozen design with an independent OLS path (`statsmodels.OLS` or QR/SVD) and confirm the non-reproduction is not a `numpy.lstsq`/smearing artifact. Write `rca011_impl_crosscheck_<UTC>.json`.
6. **Sealed-vs-recompute bridge.** For each sealed contrast (C2_vs_B1, C1_vs_B1, C2_vs_C1) tabulate sealed rel-reduction, recomputed rel-reduction, sign, and sample/coverage differences (10,785 sealed pairs vs 10,905 recompute pairs). State whether the gap is explained by the missing premium slot, the test window, or the model class. Write `rca011_sealed_bridge_<UTC>.{json,md}`.
7. **Power remediation template.** Produce a concrete, adequately-powered prereg skeleton for the first trigger-gated advance: >=3 non-overlapping 30-day blocks, target MDE below the 2% materiality floor given realistic event counts, Holm family pre-specified, `outcome_data_inspected_before_freeze=false`. Write `prereg_template_trigger_gated_<UTC>.json`.
8. **Regression gates green.** `python3 -m unittest discover -q` (0 failures), `python3 scripts/check_tracka_scope_registry_drift.py` PASS, `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118` PASS. Keep the rank-0 TRIGGER_ONLY sentinel active.

### C. Program-level power synthesis update (mandatory)
9. Update `research_state/session_<UTC>/program_power_synthesis_<UTC>.{json,md}` with the RCA attribution: classify FCLR-011 as (a) true absence of skill, (b) underpowered/degenerate design, or (c) feature/back-transform artifact. Cite the RCA artifacts. Conclude with an honest `next_action_heavy`.

### D. Trigger-gated advance (only if a trigger fires)
10. Freeze a NEW, materially different pre-outcomes prereg (`outcome_data_inspected_before_freeze=false`), run the §16 admissibility audit, execute eval+gates, register new scripts in both scope registries, update `experiment_frontier.json`/`hypothesis_registry.json`, install as rank-0 heavy cell with an honest verdict. Never re-run concluded estimands, never re-probe TERMINAL_NO_GO families, never re-score sealed results.

### E. Closeout (required)
11. Update this handoff with timestamp, exact commands/results, Phase B/C artifact paths, and remaining external blockers. Commit a checkpoint only if repo convention/permissions require it; otherwise leave the tree clean and documented.

**Completion criteria (all required):** trigger checked once with verdict recorded; every Phase B artifact written; Phase C synthesis updated with per-track MDE/classification; full suite + drift + guards green; this handoff reflects ground truth. "No trigger → stop cleanly" is NOT completion.

---

## STATE (verified 2026-11-16T02:05:42Z; HEAD a2f827e67)

### Verified now (this session)
- Full suite: `python3 -m unittest discover -q` → **Ran 1341 tests, OK (skipped=1)**, exit 0.
- Scope drift: `python3 scripts/check_tracka_scope_registry_drift.py` → `[PASS] scripts=195 registry=195 reason=OK`.
- Guards: `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118` → **38 tests, OK**.
- Triggers: all 4 OPEN; ironflow `data_through=2026-10`; 2026-11..2027-01 CONFIRMED_ABSENT.
- Root `research_state/*.{md,json}` count = **498 / 500**. All new artifacts MUST go to a session subdir.
- FCLR-RCA-011 artifacts are **absent** (`research_state/session_20261116T0040Z/rca011_*` does not exist) → Phase B is genuinely pending and is the next heavy work.

### Key findings (ground truth, do not re-litigate)
- **FCLR-011 sealed PASS is NOT independently reproduced.** Clean OLS recompute: C2_vs_B1 = **-294.01 pct-points** (sealed +4.94%), C1_vs_B1 = -342.67, C2_vs_C1 = +10.99, on 2026-05-08..2026-08-06 (10,905 pairs, 91 UTC-day blocks). Cause: the C2 premium slot is not computable from the cached 2026 archive; C2 degrades to C1 + EMA24 distance and funding features worsen out-of-sample QLIKE. Treat the sealed FCLR-011 result as fragile and never promotable. Artifact: `research_state/session_20261116T0040Z/reproducibility_recompute_2026-11-16T00:45:10Z.json`.
- **v3_30d funding ablation reproduces exactly:** E vs A point 0.487902 (expected 0.487902), identical CI and n_obs/n_blocks; DATA-SUFFICIENT PILOT / INCONCLUSIVE on the primary contrast. Artifact: `research_state/session_20261116T0040Z/evaluation_summary_funding_repro_2026-11-16T00:43:02Z.md`.
- **Program power:** Track A underpowered (MDE ~25% vs 2% floor; xsec only 2/3 blocks); Track B degenerate/underpowered (TB1 zero events, TB2 MDE ~3.4% with 2 blocks); Track C true null / non-reproducible (MDE ~111%); H2 exploratory-only. Artifact: `research_state/session_20261116T0040Z/program_power_synthesis_2026-11-16T00:46:29Z.{json,md}`.
- **Concluded — do NOT re-run:** `FCLR-LIQ-XSEC-QLIKE-20261115T214949Z`, `FCLR-LIQ-XSEC-ORDERING-20261115T203507Z`, `FCLR-LIQ-COMBINED-20261115T185844Z` (all NOT_MET/SUPERSEDED). Hypotheses `H_fclr_liq_xsec_qlike_forecast`, `H_fclr_liq_xsec_ordering_forecast`, `H_fclr_liq_combined_panel_forecast` = NOT_MET.
- **Other terminal tracks:** `H1_primary` NOT_SUPPORTED (v3_30d data-sufficient but null); `H_trackb_modeled_breaches` NOT_SUPPORTED; `H2_shek_replication` EXPLORATORY_ONLY (`promotable=false`).
- **Triggers all OPEN (external):** `GATE4_BRANCH_1` (human/legal attestation), `NEW_OBSERVED_LIQUIDATION_SOURCE` (ironflow `data_through=2026-10`; 2026-11..2027-01 absent), `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` (do not re-run sealed designs). See `research_state/resume_trigger_registry.json`, `research_state/ironflow_monitor_state.json`.
- **Rank-0 sentinel:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` | `TRIGGER_ONLY` | `BOUNDED_TRIGGER_ONLY` | `next_action_heavy=null` | `all_terminal=true`.

### External blockers (agent cannot remove)
- No new admissible observed-liquidation data (ironflow Hyperliquid 2026-11..2027-01 parquet absent; fills absent for >=2026-11).
- Gate 4 Branch 1 blocked on human/legal Binance terms evidence (agent cannot set `RESOLVED_VERIFIED`).
- `H2_shek_replication` remains `EXPLORATORY_ONLY` (`promotable=false`).
- 7 LFS pointer-only manifests are not materializable in this sandbox (reported, never fabricated).

---

## BOTTLENECKS REMOVED (2026-11-16T02:05:42Z session) — keep removed
1. **Verified the tree is green and unblocked:** 1341 tests OK, drift PASS (195/195), guards 38 OK. No red cascade remains.
2. **Reverted incidental churn** in `research_state/ironflow_fastpath_cache.json` (timestamp-only diff) → tree clean at handoff.
3. **Confirmed the heavy work is genuinely pending, not silently done:** `rca011_*` artifacts are absent; the next session cannot mistake a green suite for campaign completion.
4. **Kept the root cap safe:** 498/500 root md/json; all new RCA artifacts are directed to a session subdir.
5. **Stale handoff traps remain neutralized:** `NEXT_SESSION_TASK.md` / `NEXT_SESSION_HANDOFF.md` are tombstones; `AGENT_HANDOFF_20261115T073240Z.md` retired.

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
- `research_state/session_20261116T0040Z/` (prior session Phase B/C artifacts), `research_state/session_20261116T0040Z/fclr011_recompute_panel_20261116T004150Z.parquet`
- `scripts/fclr011_recompute_audit.py` (fixed), `scripts/run_funding_ablations.py`, `scripts/run_gate4_v4_leakage_audit.py`, `scripts/tracka_resume_check.py`
- `tests/test_active_campaign_gate.py`, `tests/test_tracka_hardening_099.py`, `tests/test_tracka_hardening_117.py`, `tests/test_tracka_hardening_118.py`

**Next session:** execute A→B→C→E in order (heavy default). Stop only when the trigger is checked once, every Phase B/C artifact is written, the full suite/guards are green, and this handoff reflects ground truth with external blockers documented.