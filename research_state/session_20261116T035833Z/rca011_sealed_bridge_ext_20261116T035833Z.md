# RCA011 Sealed Bridge — Extension 2026-11-16T03:58:33Z

Extends `research_state/session_20261116T023837Z/rca011_sealed_bridge_20261116T023837Z.md` with B1/B2 attribution and implementation cross-check findings (cached recompute panel; sealed panel unavailable as LFS pointer).

## B1 — Nested feature attribution (recompute panel)
Artifact: `rca011_feature_attribution_20261116T035833Z.{json,md}` (panel `session_20261116T0040Z/fclr011_recompute_panel_20261116T004150Z.parquet`, train 152 rows after 7d purge/dropna, test 10,905, 24h block bootstrap 2000, seed 20261114).

| Contrast | rel% | 95% CI | Read |
|---|---:|---:|---|
| B1_plus_funding vs B1 | -342.67% | [-497.48, -221.27] | funding features strongly harmful OOS |
| B1_plus_ema24 vs B1 | +9.75% | [7.01, 12.74] | ema24_dist helps vs B1 |
| B1_plus_funding_plus_ema24 vs B1 | -294.01% | [-429.62, -186.56] | joint (C2-analogue w/o premium) harmful |
| joint vs B1_plus_funding | +10.99% | [9.43, 12.44] | ema24 helps conditional on funding |
| joint vs B1_plus_ema24 | -336.55% | [-495.81, -210.33] | funding harms conditional on ema24 |

**Decomposition:** recompute degradation is attributable to **funding augmentation** (signed_funding + trailing |funding| percentile), not ema24_dist and not premium-slot absence alone (ema24_dist positive). Joint harm tracks funding.

## B2 — Implementation cross-check
Artifact: `rca011_impl_crosscheck_20261116T035833Z.json`. statsmodels.OLS vs numpy.linalg.lstsq (independent fit/predict + Duan smearing) agree to ~1e-12–1e-17 on contrasts/predictions. **No lstsq/smearing implementation artifact.**

## B3 — Panel-diff / sealed-gap status (without LFS)
- Sealed `fclr011_panel.json` remains a Git-LFS pointer here: byte/row diff vs recompute panel not possible.
- Evidence-backed gap remains: recompute premium not computable from cached 2026 archive (C2→C1+ema24_dist), **+120-row eligibility delta** (10,905 vs 10,785), identical test window/universe.
- Combined with B1/B2, reversal is best explained by **panel/feature construction & availability divergence plus unstable funding fit on sparse complete train rows (152)**, not by numerical solver error.

## B4 — Power template
`session_20261116T023837Z/prereg_template_trigger_gated_20261116T023837Z.json` remains adequate (>=3 non-overlapping 30d blocks, MDE < 2% floor, Holm, `outcome_data_inspected_before_freeze=false`, §16 audit before freeze). No refinement required by B1/B2 beyond noting: any future funding-volatility prereg must justify train completeness/power for added funding features and audit premium/feature availability against sealed definitions before freeze.
