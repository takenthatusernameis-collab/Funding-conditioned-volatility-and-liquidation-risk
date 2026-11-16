# Evidence Audit — 2026-11-16T12:56:24Z

## Carried-forward bundle
- Bundle path: `research_state/session_20261116T100533Z/` (complete Phase-B/C bundle, carried forward unmodified from `session_20261116T035833Z/`).
- Five required artifact families verified present and unmodified:
  1. `rca011_feature_attribution_*` — funding increment -342.67%, EMA24 +9.75%, joint -294.01%.
  2. `rca011_impl_crosscheck_*` — OLS/lstsq agree ~1e-12 to 1e-17.
  3. `rca011_sealed_bridge_*` — sealed +4.94% vs clean recompute -294.01%; 120-row eligibility delta; sealed panel is unavailable/LFS-pointer artifact.
  4. `prereg_template_trigger_gated_*` — power-remediation prereg skeleton.
  5. `program_power_synthesis_*` — FCLR-011 fragile/non-promotable; `next_action_heavy=null` on cached data.
- Latest prior heavy session `session_20261116T115028Z/` (independent numpy-only FCLR-011 recompute, `all_within_tolerance=true`; trigger check `NO_TRIGGER_FIRED`; evidence audit present) carried forward unmodified.

## New quantitative artifact (this session)
- `research_state/session_20261116T125624Z/recompute_fclr009_20261116T125624Z.py` + `.json` + `.md`.
- Independent numpy/pandas recompute of FCLR-009 (the only adequately powered Track C null, n=24,495, 6 blocks, MDE 1.95%) from cached 2025 data with hardcoded frozen splits (no manifest/LFS dependency).
- Result: B0 0.367906 (n=24,648), B1 0.340756 (n=24,495), C1 0.339628, C2 0.342205; C2-vs-B1 mean diff 0.001449, relative -0.425%, 95% CI [-0.003120, 0.006165], n_pairs 24,495. All within tolerance (QLIKE abs <= 1e-6; rel <= 0.01 pct-points). `all_within_tolerance=true`.
- Corroborates the FCLR-009 NOT_MET terminal headline via a second independent code path. No sealed artifact mutated.

## Integrity conclusion
- RCA-011 complete: FCLR-011 sealed PASS (+4.94%) is not reproducible (clean recompute -294.01%); triple-confirmed by numpy-only path; funding augmentation drives the harm; only 152 complete training rows. FCLR-011 fragile/non-promotable.
- FCLR-009 NOT_MET corroborated independently. All cached-data confirmatory estimands remain terminal.
- Triggers: all four OPEN; Ironflow data_through=2026-10; 2026-11/12/2027-01 CONFIRMED_ABSENT.
- `next_action_heavy` on cached data: independent reproducibility audit of the next terminal headline in the queue (FCLR-006 — sealed 2026 May-Aug underpowered panel, n=...), then FCLR-002/003/007/008. No trigger fired; no new confirmatory estimand.

## Gates
- `python3 scripts/check_handoff_heavywork_gate.py --json`: PASS (heavy_session=session_20261116T100533Z, latest_session=session_20261116T125624Z, has_audit=true, has_new_quant=true, root_count=500/500).
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: PASS.
- Targeted unittests + full discovery: recorded below after run.