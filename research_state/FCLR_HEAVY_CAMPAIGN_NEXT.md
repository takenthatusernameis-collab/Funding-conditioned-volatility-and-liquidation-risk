# FCLR Focus Campaign (Trigger-Only) — revised 2026-11-16T00:47:00Z

**Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (TRIGGER_ONLY / BOUNDED_TRIGGER_ONLY, `next_action_heavy=null`, `all_terminal=true`).
**Sole handoff:** `AGENT_HANDOFF.md`. This file is the detailed, non-skippable campaign note referenced by the frontier and the handoff.
**Governing rules:** `RESEARCH_PROMPT.md`. Never re-run concluded estimands, never re-score sealed results, never fabricate data, never edit `.github/workflows/*`, no polling, no paid/credentialed/manual outcome data.

## Ground truth (verified 2026-11-16T00:47:00Z)
Every cached-data confirmatory estimand is terminal. New this session:
- **The independent FCLR-011 reproducibility audit was BROKEN and is now FIXED.** Two implementation defects made it exit `INCONCLUSIVE` on every prior run (`scripts/fclr011_recompute_audit.py`): (1) the test frame was a pre-scaling copy missing `funding_z` / `abs_fund_pct_z` / `ema24_dist_z`, so C1/C2 design matrices returned `None`; (2) `predict()` read a shared `spec['smearing']` (last model's value) instead of the fitted per-model `fit['smearing']`. After the fix the audit runs end-to-end.
- **Result: the sealed FCLR-011 PASS is NOT independently reproduced.** Independent clean OLS recompute gives C2_vs_B1 = **-294.01 pct-points** (sealed **+4.94%**), C1_vs_B1 = -342.67, C2_vs_C1 = +10.99, on the 2026-05-08..2026-08-06 test window (10,905 paired rows, 91 UTC-day blocks). The C2 premium slot is not computable from the cached 2026 archive; C2 degrades to C1 + EMA24 distance and funding features materially worsen out-of-sample QLIKE. This is a genuine integrity finding: the sealed FCLR-011 result is fragile and never promotable. Artifact: `research_state/session_20261116T0040Z/reproducibility_recompute_2026-11-16T00:45:10Z.json`.
- **The v3_30d funding ablation reproduces exactly** (E vs A point 0.487902 vs expected 0.487902; CI and n_obs/n_blocks identical). Artifact: `research_state/session_20261116T0040Z/evaluation_summary_funding_repro_2026-11-16T00:43:02Z.md`.
- **Program power synthesis** written: `research_state/program_power_synthesis_2026-11-16T00:46:29Z.{json,md}` — Tracks A/B are underpowered/degenerate (MDEs 25% / 3.4% / undefined vs a 2% floor), Track C is a true null / non-reproducible, H2 is exploratory-only.

## Resume triggers (all OPEN unless evidenced)
Check **once** per session start via `research_state/resume_trigger_registry.json` + `research_state/ironflow_monitor_state.json` (no polling, no re-probe): `GATE4_BRANCH_1` (human/legal attestation; agent cannot set), `NEW_OBSERVED_LIQUIDATION_SOURCE` (ironflow `data_through=2026-10`, 2026-11+ absent), `HL_LABEL_EXTENSION`, `EXPANSION_ROBUSTNESS_REDO` (only a NEW prereg meeting stated conditions; never re-run/re-score sealed designs).

## Mandatory heavy work (default; do NOT stop after the trigger check)
A session that only runs the trigger check and the unit suite is **incomplete**. The next focus campaign is **FCLR-RCA-011** below: a root-cause / adversarial re-audit of the FCLR-011 non-reproduction. It is heavy, uses only cached data, is agent-removable, and does not create or promote any new confirmatory claim.

### Phase A — Trigger check (once)
1. Read the two trigger files above; confirm `data_through=2026-10` and 2026-11..2027-01 absent. Record the check (timestamp + verdict) in `AGENT_HANDOFF.md`. Do not poll or re-probe.
2. If a trigger is satisfied with its required evidence artifact, jump to Phase D.

### Phase B — FCLR-RCA-011 root-cause & adversarial re-audit (heavy, mandatory)
3. **Feature attribution.** On `research_state/session_20261116T0040Z/fclr011_recompute_panel_20261116T004150Z.parquet` (or a fresh recompute), estimate nested QLIKE for B1, B1+funding, B1+ema24, B1+funding+ema24 (C1, C2) with the same train-only scaling, smearing, purge/embargo and paired block bootstrap. Decompose the C2_vs_B1 degradation into the funding-feature contribution vs the EMA24 contribution. Write `research_state/rca011_feature_attribution_<UTC>.{json,md}`.
4. **Implementation cross-check.** Re-fit the same frozen design with an independent OLS path (e.g., `statsmodels.OLS` or a QR/SVD solve) and confirm the non-reproduction is not a `numpy.lstsq`/smearing artifact. Write `research_state/rca011_impl_crosscheck_<UTC>.json`.
5. **Sealed-vs-recompute bridge.** For each sealed contrast (C2_vs_B1, C1_vs_B1, C2_vs_C1) tabulate sealed rel-reduction, recomputed rel-reduction, sign, and the sample/coverage differences (10,785 sealed pairs vs 10,905 recompute pairs). State whether the gap is explained by the missing premium slot, the test window, or the model class. Write `research_state/rca011_sealed_bridge_<UTC>.{json,md}`.
6. **Power remediation template.** Produce a concrete, adequately-powered prereg skeleton for the first trigger-gated advance: >=3 non-overlapping 30-day blocks, target MDE below the 2% materiality floor given realistic event counts, Holm family pre-specified, `outcome_data_inspected_before_freeze=false`. Write `research_state/prereg_template_trigger_gated_<UTC>.json`.
7. **Regression gates green.** `python3 -m unittest discover -q` (0 failures), `python3 scripts/check_tracka_scope_registry_drift.py` PASS, `python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118` PASS. Keep the rank-0 TRIGGER_ONLY sentinel active — never delete it.

### Phase C — Synthesis update (heavy)
8. Update `research_state/program_power_synthesis_<UTC>.{json,md}` with the RCA attribution: state whether FCLR-011 is (a) a true absence of skill, (b) an underpowered/degenerate design, or (c) a feature/back-transform artifact. Cite the RCA artifacts. Conclude with an honest `next_action_heavy`.

### Phase D — Trigger-gated advance (only if a trigger fires)
Pre-outcomes prereg first (`outcome_data_inspected_before_freeze=false`); §16 admissibility audit; materially different estimand only; execute eval+gates; register new scripts in both scope registries; update `experiment_frontier.json` / `hypothesis_registry.json`; install as rank-0 active heavy cell with an honest verdict. Forbidden: re-run concluded estimands, re-probe TERMINAL_NO_GO families, mutate sealed artifacts, edit `.github/workflows/*`, paid/credentialed/manual outcome data, polling.

## Session closeout (all boxes required)
- [ ] Trigger checked once, verdict recorded.
- [ ] Phase B RCA artifacts written: `rca011_feature_attribution_<UTC>.{json,md}`, `rca011_impl_crosscheck_<UTC>.json`, `rca011_sealed_bridge_<UTC>.{json,md}`, `prereg_template_trigger_gated_<UTC>.json`.
- [ ] Phase C `program_power_synthesis_<UTC>.{json,md}` updated with RCA attribution.
- [ ] Full suite + drift + guards green.
- [ ] `AGENT_HANDOFF.md` updated with exact commands/results and remaining blockers.
Stop cleanly ONLY when all boxes are checked. Never leave the suite red, never delete the rank-0 sentinel, never claim completion from prose alone.