# FCLR Design Feasibility — FCLR-DESIGN-FEASIBILITY-20261115T021249Z

- Generated (UTC): 2026-11-15T02:35:00Z
- Status: VALID_EXPLORATORY (EXPLORATORY_ONLY, promotable=false, audit_only=true)
- Overall verdict: **UNDECIDABLE_ON_CACHE**
- Prereg: `research_state/prereg_fclr_design_feasibility_2026-11-15T02:35:00Z.json`

## Method

- alpha=0.05, power_target=0.8, z_975=1.959963984540054, z_80=0.8416212335729143, z_95=1.6448536269514722, mde80_factor=2.8015852181129683
- SE_req = |floor| / mde80_factor; n_req = n_obs * (SE_obs / SE_req)^2 (1/sqrt(n) scaling).
- Verdict rule: {'DECIDABLE_ON_CACHE': 'n_req <= n_available', 'UNDECIDABLE_ON_CACHE': 'n_req > n_available', 'INCONCLUSIVE': 'unstable/missing/non-finite inputs'}

## Volatility track (forward 2025 disjoint, C2_vs_B1)

- Track verdict: **UNDECIDABLE_ON_CACHE** (primary h24_C2_vs_B1)
- Panel rows (max available): 30120; primary contrast n_available=10800
- Primary h24: n_obs=10800, SE_obs=0.01047, floor=0.00705232, SE_req=0.00251726, n_req=186834.7, n_available=10800.0 => **UNDECIDABLE_ON_CACHE**

| horizon | n_obs | SE_obs | floor | SE_req | n_req | n_avail | verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| h6 | 10800 | 0.0117212 | 0.013518 | 0.00482512 | 63730.5 | 10800.0 | UNDECIDABLE_ON_CACHE |
| h24 | 10800 | 0.01047 | 0.00705232 | 0.00251726 | 186834.7 | 10800.0 | UNDECIDABLE_ON_CACHE |
| h72 | 10560 | 0.00352186 | 0.00388991 | 0.00138847 | 67941.8 | 10560.0 | UNDECIDABLE_ON_CACHE |
| h168 | 10080 | 0.00314735 | 0.00290307 | 0.00103623 | 92991.3 | 10080.0 | UNDECIDABLE_ON_CACHE |

## Observed-liquidation track (xsec forward)

- Track verdict: **DECIDABLE_ON_CACHE** (analytic vs symmetry-robust reported)
- Panel rows / pooled n_available: 6634 / 6634
- Pooled analytic: n_obs=6634, SE_obs=0.0120894, floor=0.05, SE_req=0.017847, n_req=3044.0, n_available=6634.0 => **DECIDABLE_ON_CACHE**
- Pooled symmetry-robust: SE_robust=0.0126287, n_req=3321.7, n_available=6634.0 => **DECIDABLE_ON_CACHE**
- Symmetry instability: pass_1pct_persisted=False, abs_frac=0.022307243116526917, verdict_flips=False

### Per-block (approximate, pooled-null SE scaled)

| block | n_obs | IC | SE_obs_approx | n_req | n_avail | verdict_approx |
|---|---:|---:|---:|---:|---:|---|
| block_0 | 2996 | -0.0409224 | 0.0179895 | 3044.0 | 2996.0 | UNDECIDABLE_ON_CACHE |
| block_1 | 1605 | -0.0312473 | 0.0245784 | 3044.0 | 1605.0 | UNDECIDABLE_ON_CACHE |
| block_2 | 2033 | -0.00892202 | 0.0218385 | 3044.0 | 2033.0 | UNDECIDABLE_ON_CACHE |

## Known-answer self-test (NOT market evidence)

- recovered_80pct_within_tolerance=True (power_at_nreq=0.800000960562, n_req=872.097748)

## Inputs (sha256)

- power_calibration_eval: `research_state/evaluation_summary_FCLR-POWER-CALIBRATION-2026-11-15T01:34:12Z.json` sha256=90a9cb219e9c2c7d348e53f60c79e265ddaa746a5755aeb74111a11ac4594d4d
- power_calibration_prereg: `research_state/prereg_fclr_power_calibration_2026-11-15T01:34:12Z.json` sha256=1411461f8a65c9d169e6850c4680fdddc1edaf7e77969692347188112613579e
- vol_panel: `research_state/tracka_fwd_vol_2025_disjoint_cross_panel_20261114T191615Z.parquet` sha256=de0ca73e7d092a205e5f8c1163d56437384d1b15d65b4a27bc54a57e21738cba
- liq_panel: `research_state/tracka_liq_xsec_forward_panel_2026-11-13T22:31:55Z.parquet` sha256=990598685617b088344435ac8c3e318fcdb42ed5e342df82120a15340b91caac

## Sealed-artifact integrity

- sealed_artifacts_mutated: False
