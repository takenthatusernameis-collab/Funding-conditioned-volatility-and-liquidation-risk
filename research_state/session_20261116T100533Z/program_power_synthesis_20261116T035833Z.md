# Program Power Synthesis — 2026-11-16T03:58:33Z (FCLR-RCA-011)

**Program:** FCLR (Funding-conditioned Volatility and Liquidation Risk)
**Active frontier:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (TRIGGER_ONLY / BOUNDED_TRIGGER_ONLY), `all_terminal=true` on cached-data confirmatory estimands.
**Trigger check:** `research_state/session_20261116T023837Z/trigger_check_20261116T023837Z.json` — **NO_TRIGGER_FIRED** (GATE4_BRANCH_1, NEW_OBSERVED_LIQUIDATION_SOURCE, HL_LABEL_EXTENSION, EXPANSION_ROBUSTNESS_REDO all OPEN).

## FCLR-011 classification
**Classification: (c) feature/back-transform/artifact-driven (integrity failure), with an underpowered/unstable training fit — not a clean sealed PASS and not evidence of a general true absence of skill.**

### Evidence
- **Sealed:** `evaluation_summary_FCLR-011.md` (2026-11-03T21:22:07Z) reports C2 vs B1 **+4.94%** (95% CI [-0.032546,-0.001418], n=10,785), C1 vs B1 +1.36%, C2 vs C1 +3.63% (CI crosses 0) on 2026-05-08..2026-08-06.
- **Independent recompute (cached 2026 archive, same window/universe, 7d purge, train-only scaling+smearing, 24h block bootstrap 2000):** `session_20261116T0040Z/reproducibility_recompute_2026-11-16T00:45:10Z.json` — **NOT_REPRODUCED**. C2 vs B1 **-294.01%** (n=10,905), C1 vs B1 **-342.67%**, C2 vs C1 **+10.99%**. Premium slot not computable from cache (C2 = C1+ema24_dist in recompute); eligibility differs by +120 paired rows; sealed panel unavailable (LFS pointer).
- **Nested feature attribution** (`session_20261116T035833Z/rca011_feature_attribution_20261116T035833Z.{json,md}`), identical design on recompute panel (152 train rows after purge/dropna, 10,905 test rows):
  - B1_plus_funding vs B1 (funding_increment): **-342.67%** (CI [-497.48, -221.27]) — funding features catastrophically harmful OOS.
  - B1_plus_ema24 vs B1 (ema24_increment): **+9.75%** (CI [7.01, 12.74]) — ema24_dist helps vs B1.
  - B1_plus_funding_plus_ema24 vs B1 (joint): **-294.01%** (CI [-429.62, -186.56]).
  - B1_plus_funding_plus_ema24 vs B1_plus_funding (ema24_over_funding): **+10.99%** (CI [9.43, 12.44]).
  - B1_plus_funding_plus_ema24 vs B1_plus_ema24 (funding_over_ema24): **-336.55%** (CI [-495.81, -210.33]).
- **Implementation cross-check** (`session_20261116T035833Z/rca011_impl_crosscheck_20261116T035833Z.json`): statsmodels.OLS vs numpy.linalg.lstsq predictions/contrasts match to ~1e-12–1e-17; **no solver/smearing artifact** explains the degradation.

### Interpretation
- The recompute degradation is driven by the **signed_funding + trailing-|funding| percentile** augmentation on this panel/window/fit, not by ema24_dist and not by numerical implementation. Joint C2-like harm tracks funding harm.
- The sealed-vs-recompute reversal is consistent with **feature/panel availability and construction divergence** (premium not computable from cache; +120-row eligibility delta; sealed panel not auditable here) rather than a reproducible funding edge.
- The attribution fit relies on only **152 complete train rows** after purge/dropna, so funding coefficients are likely unstable — this supports an integrity/instability finding but prevents claiming a definitive general "true absence of skill" from this recompute alone.
- **Integrity conclusion:** sealed FCLR-011 PASS is **not independently reproduced and not promotable**. Treat as fragile/non-confirmatory pending any trigger-gated, pre-registered re-test with auditable inputs and adequate power.

## Power / next heavy action
- `next_action_heavy = null` (no agent-removable confirmatory estimand on cached data). Hold `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z`.
- On external trigger only: follow `research_state/session_20261116T023837Z/prereg_template_trigger_gated_20261116T023837Z.json` — §16 admissibility audit, NEW pre-outcomes prereg (`outcome_data_inspected_before_freeze=false`), >=3 non-overlapping 30d blocks, MDE < 2% floor, Holm family, 7d purge/embargo, materially different estimand. Never re-run concluded/sealed cells.
