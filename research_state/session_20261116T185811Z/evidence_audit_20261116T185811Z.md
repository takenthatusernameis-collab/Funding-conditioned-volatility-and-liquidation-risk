# Evidence Audit — 2026-11-16T18:58:11Z

## Carried-forward bundle
- Bundle path: `research_state/session_20261116T100533Z/` (complete Phase-B/C bundle, carried forward unmodified from `session_20261116T035833Z/`).
- Five required artifact families verified present and unmodified:
  1. `rca011_feature_attribution_*` — funding increment -342.67%, EMA24 +9.75%, joint -294.01%.
  2. `rca011_impl_crosscheck_*` — OLS/lstsq agree ~1e-12 to 1e-17.
  3. `rca011_sealed_bridge_*` — sealed +4.94% vs clean recompute -294.01%; 120-row eligibility delta; sealed panel is unavailable/LFS-pointer artifact.
  4. `prereg_template_trigger_gated_*` — power-remediation prereg skeleton.
  5. `program_power_synthesis_*` — FCLR-011 fragile/non-promotable; `next_action_heavy=null` on cached data.
- Latest prior heavy session `session_20261116T125624Z/` verified present with exactly four files: `recompute_fclr009_20261116T125624Z.{py,json,md}` + `evidence_audit_20261116T125624Z.md` (FCLR-009 independently reproduced, `all_within_tolerance=true`). No discovery-suite capture was saved there (corrected earlier claim).

## New quantitative artifact (this session)
- `research_state/session_20261116T185811Z/recompute_fclr006_20261116T185811Z.py` + `.json` + `.md`.
- Independent recompute of FCLR-006 (sealed-2026 volatility-forecast panel; queue item 2) from cached 2026 data with hardcoded frozen splits (no manifest/LFS dependency).
- Protocol: `research_state/research_protocol_fclr006.md` (FCLR-006 v1.0, frozen 2026-10-30T13:45:00Z). Published results: `research_state/evaluation_summary_FCLR006.md`. Errata: `research_state/reporting_errata_FCLR006.md`.
- Frozen splits: train 2026-04-01..2026-04-24; 7d embargo 2026-04-25..2026-05-01; val 2026-05-02..2026-05-15; 7d embargo 2026-05-16..2026-05-22; test 2026-05-23..2026-08-06 (76 days = 2 blocks; block criterion NOT_MET by design — not relaxed).
- Universe: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT. Data: `research_state/data_cache/{SYM}_2026_0{1,4,5,6,7,8}/` (markPriceKlines 1h, indexPriceKlines, premiumIndexKlines, fundingRate). Funding loaded from 2026-01 to support 90-day lookback percentile. Coverage: `research_state/fclr006_coverage_audit.md` (128 common days, ~3072 common UTC hours).
- Models: B0 persistence; B1 HAR-style OLS on log RV1h/RV24h/RV168h; C1 = B1 + signed funding + past-only 90-day |funding| percentile; C2 = C1 + mark/index premium + mark/EMA24 distance. OLS on log(RV+1e-12), raw predictors + intercept + 1e-12 ridge, block bootstrap ~24h blocks, 2000 deterministic-seed replicates (seed 12345).
- Counts: collected 12,720; train 2,040; val 1,680; test 9,000.
- Result vs published (tolerances: QLIKE abs <= 1e-6; mean diff abs <= 1e-6; rel reduction <= 0.01 pct-points):
  - B0: recomputed 0.518169 (n=9,000) vs published 0.518169 (n=9,000) — abs_diff 2.0e-7 ✓
  - B1: recomputed 0.527290 (n=8,987) vs published 0.527290 (n=8,987) — abs_diff 3.7e-7 ✓
  - C1: recomputed 0.620158 (n=8,987) vs published 0.620158 (n=8,987) — abs_diff 2.3e-7 ✓
  - C2: recomputed 0.882279 (n=8,987) vs published 0.882279 (n=8,987) — abs_diff 1.5e-7 ✓
  - C2_vs_B1: recomputed mean diff 0.354989, rel -67.32%, n_pairs 8,987 vs published 0.354989, -67.32%, 8,987 — abs_diff 2.2e-7 ✓, rel diff 0.0032 pct-points ✓
- `all_within_tolerance=true`. Independent recompute corroborates the FCLR-006 NOT_MET terminal headline via an independent code path.
- Formal gate remains NOT_MET (test window = 76 days = 2 blocks < 3 required); FCLR-H001 remains NOT_SUPPORTED. Relative reduction -67.32% is negative (C2 worse than B1) — direction is harm, not improvement.

## Integrity conclusion
- Triggers: all four OPEN; Ironflow data_through=2026-10; 2026-11/12/2027-01 CONFIRMED_ABSENT. NO_TRIGGER_FIRED.
- RCA-011 complete: FCLR-011 sealed PASS (+4.94%) is not reproducible (clean recompute -294.01%); triple-confirmed; fragile/non-promotable.
- FCLR-009 NOT_MET corroborated independently (previous heavy session). FCLR-006 NOT_MET corroborated independently (this session).
- All cached-data confirmatory estimands remain terminal. `next_action_heavy=null` on cached data.
- No sealed artifact mutated. No root-level additions (all artifacts in session subdirectory).

## Gates
- `python3 scripts/check_handoff_heavywork_gate.py --json`: recorded below.
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: recorded below.
- Targeted unittests + full discovery suite: recorded below.
