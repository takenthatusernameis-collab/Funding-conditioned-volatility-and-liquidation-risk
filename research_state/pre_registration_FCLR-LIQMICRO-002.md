# PRE-REGISTRATION: FCLR-LIQMICRO-002
**TIMESTAMP (UTC):** 2026-11-02T00:04:02Z
**CAMPAIGN:** FCLR-LIQMICRO-002 (Track D: Liquidation Microstructure — REAL FUNDING INTEGRATION)
**DATA SOURCE:** ironflow Hyperliquid liquidation events ONLY + Hyperliquid fundingHistory API (unauthenticated)
**FIREWALLS:** NO Binance merge, NO re-opening FCLR-003/FCLR-010/H001, NO H001 threshold tuning
**STATUS:** PRE-REGISTERED BEFORE ANALYSIS
**SUPERSEDES:** pre_registration_FCLR-LIQMICRO-001.md (same D1-D3, but with REAL funding variation instead of degenerate zeroed funding)

## MOTIVATION
FCLR-LIQMICRO-001 ran with degenerate funding: `src/analysis/liqmicro/features.py::add_funding_features` zeroed `funding_rate`/`funding_abs`, yielding D2 `funding_abs=0.0` with NaN p-values and empty D3 clustering_by_decile. That invalidated D2/D3. Repo name "Funding-conditioned-volatility-and-liquidation-risk" makes funding-conditioned analysis the #1 priority. FCLR-LIQMICRO-002 re-runs D1-D3 with REAL Hyperliquid funding variation (9 coins x 8668 records, fundingRate.std() > 0 confirmed in research_state/liqmicro_funding_audit_002.md).

## HYPOTHESES (FALSIFIABLE, SAME AS FCLR-LIQMICRO-001)

### D1 (Funding asymmetry)
**Question:** Does funding rate sign predict liquidation intensity asymmetry (long vs short liquidations) in the next 1-4h?

**Estimand:** Effect of funding sign on ratio of long/short liquidations over horizon h ∈ {1,2,4} hours, with market/time fixed effects.

**Null:** |ΔL/L| < 2% or 95% CI crosses 0 for all horizons h∈{1,2,4}.
**Alternative:** Significant asymmetry with consistent sign across horizons.

**Test:** Clustered regression by symbol and time, controls for lagged liquidations, volatility.

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

**Unit of observation:** Symbol × hour.
**Data:** ironflow Hyperliquid events only (Track A, admissible) aggregated to hourly panel + Hyperliquid fundingHistory (unauthenticated) aligned on symbol+hour UTC.
**Funding alignment:** Hyperliquid coins mapped by stripping `-PERP` suffix (BTC-PERP → BTC). Funding merged on `symbol`+`hour` (UTC). Missing funding for a symbol-hour is NOT silently zeroed: either dropped with explicit flag or forward-fill only with justification logged.
**Clustering:** By symbol and by time.
**Controls:** Lagged liquidations (1h,4h,24h), realized volatility, funding level/history, time effects.
**Multiple testing:** Benjamini-Hochberg FDR at q=0.05 across D1-D3 family.
**No look-ahead:** All features lagged appropriately; funding zscore is trailing-only (rolling window by symbol, no future data).
**Pre-registration timestamp:** Before running run_liqmicro_v2.py and before inspecting D1-D3 outcomes.

## STOPPING RULES
- If all nulls hold AND robustness passes → "NO MECHANISM FOUND (D1-D3 all null)" with full evidence.
- If any survives FDR → report mechanism with magnitudes, EXPLICITLY state "does NOT imply H001 reversal" and "no confirmatory re-test of H001 opened."
- Do NOT spin up new hypotheses if all nulls hold.
- Do NOT re-open H001, FCLR-003, or FCLR-010. This is a Track D microstructure fix only.

## ARTIFACTS REQUIRED
- `research_state/pre_registration_FCLR-LIQMICRO-002.md` (this document)
- `research_state/liqmicro_funding_audit_002.md` (already written: 9 coins, fundingRate.std() > 0)
- `results/liqmicro_v2/panel_liqmicro_v2.csv`, `.parquet`, `descriptive_stats_v2.csv`
- `research_state/evaluation_summary_FCLR-LIQMICRO-002.md` (D1-D3 + BH FDR + verdict)
- Updated `research_state/experiment_frontier.json` with FCLR-LIQMICRO-002 entry
- `src/analysis/liqmicro/` modules (features.py funding merge fix verified)
- Tests: `python -m unittest discover -s tests -v` must remain 27/27 PASS

## ACCEPTANCE GATES
- panel['funding_rate'].std() > 0 across non-NaN rows (no all-zero column)
- >=5 overlapping symbols between ironflow and Hyperliquid funding
- All 27 tests pass
- No changes to .github/workflows/
- Only new *_002* artifacts and results/liqmicro_v2/ written; sealed artifacts unchanged
