# PRE-REGISTRATION: FCLR-LIQMICRO-001
**TIMESTAMP (UTC):** 2026-11-01T22:16:37Z
**CAMPAIGN:** FCLR-LIQMICRO-001 (Track D: Liquidation Microstructure)
**DATA SOURCE:** ironflow Hyperliquid liquidation events ONLY (admissible Track A)
**FIREWALLS:** NO Binance merge, NO re-opening FCLR-003, NO H001 threshold tuning
**STATUS:** PRE-REGISTERED BEFORE ANALYSIS

## MOTIVATION
Primary hypothesis H001 NOT_SUPPORTED (FCLR-003 gate NOT_MET). Confirmatory panels exhausted on admissible data. Shift to mechanistic mapping of funding-conditioned liquidation intensity using ONLY the single admissible source (ironflow Hyperliquid).

## HYPOTHESES (FALSIFIABLE)

### D1 (Funding asymmetry)
**Question:** Does funding rate sign predict liquidation intensity asymmetry (long vs short liquidations) in the next 1-4h?

**Estimand:** Effect of funding sign on ratio of long/short liquidations (or difference in liquidation rates) over horizon h ∈ {1,2,4} hours, with market/time fixed effects.

**Null:** |ΔL/L| < 2% or 95% CI crosses 0 for all horizons h∈{1,2,4}.
**Alternative:** Significant asymmetry with consistent sign across horizons.

**Test:** Clustered regression by symbol and time, controls for lagged liquidations, volatility, volume/liquidity proxies.

### D2 (Volatility interaction)
**Question:** Is funding-conditioned liquidation intensity higher when realized volatility is in the top tercile vs bottom tercile, controlling for funding level?

**Estimand:** Interaction between funding measures (level, |funding|, sign) and realized volatility terciles on liquidation intensity.

**Null:** Interaction term coefficient not significant at p>=0.05 with Benjamini-Hochberg FDR correction across all tests.
**Alternative:** Significant positive interaction in top tercile with economically meaningful magnitude.

**Test:** Include interaction terms with tercile dummies, full controls, clustered standard errors.

### D3 (Cascade/clustering)
**Question:** Does liquidation clustering (autocorrelation) increase with |funding| after controlling for vol/volume?

**Estimand:** Change in liquidation autocorrelation (AR(1)/clustering metrics) across |funding| deciles.

**Null:** No significant increase in top |funding| decile relative to bottom deciles; difference CI crosses 0.
**Alternative:** Systematic increase in clustering with funding magnitude, robust to controls.

**Test:** Compare clustering metrics by |funding| deciles, bootstrap CIs, FDR correction.

## METHODOLOGY

**Unit of observation:** Symbol × hour (or appropriate granularity based on data)
**Data:** ironflow Hyperliquid events only, aggregated to panel
**Clustering:** By symbol and by time (double-clustering where feasible)
**Controls:** Lagged liquidations (1h,4h,24h), realized volatility, funding level/history, time effects
**Multiple testing:** Benjamini-Hochberg FDR at q=0.05 across D1-D3 family
**Robustness:** Placebo funding shifts (±1-2 periods), subsample stability, alternative volatility measures
**No look-ahead:** All features lagged appropriately

## STOPPING RULES
- If all nulls hold AND robustness passes → "NO MECHANISM FOUND (D1-D3 all null)" with full evidence
- If any survives FDR → report mechanism with magnitudes, EXPLICITLY state "does NOT imply H001 reversal" and "no confirmatory re-test of H001"
- Do NOT spin up new hypotheses if all nulls hold

## ARTIFACTS REQUIRED
- `research_state/liqmicro_data_audit_001.md` (data audit)
- `src/analysis/liqmicro/` modules (ingest.py, features.py, models.py, stats.py)
- `research_state/pre_registration_FCLR-LIQMICRO-001.md` (this document)
- `results/liqmicro/` tables (CSV/LaTeX) and figures (PNG/PDF)
- `research_state/evaluation_summary_FCLR-LIQMICRO-001.md`
- Update `research_state/experiment_frontier.json`
