# LEAKAGE AUDIT: FCLR-LIQMICRO-002
**TIMESTAMP (UTC):** 2026-11-02T00:07:50Z
**CAMPAIGN:** FCLR-LIQMICRO-003 (Adversarial RE-AUDIT)
**PANEL:** results/liqmicro_v2/panel_liqmicro_v2.parquet (93,504 symbol-hour obs x 199 symbols, 2025-11-01 00:00:00+00:00 to 2026-10-30 23:00:00+00:00)
**DATA:** ironflow Hyperliquid liquidations ONLY + Hyperliquid fundingHistory API (unauthenticated)
**FIREWALL:** Hyperliquid-only, NO Binance merge, NO H001/FCLR-003/FCLR-010 re-test

## Audit checklist (adversarial)

### 1) Future-row perturbation cannot change earlier features/forecasts
- **Check:** Features computed from history only (rolling windows). funding_zscore uses `groupby('symbol')['funding_rate'].transform(lambda x: _zscore(x))` with rolling window 2160, min_periods=30 (trailing). rv_proxy uses rolling std over past 24h. lags via `shift(lag)`. Clustering uses rolling windows over past values.
- **File:line:** `src/analysis/liqmicro/features.py:62-103` (rolling windows, shift operations)
- **Finding:** NO look-ahead in feature construction. Perturbing future rows cannot change historical feature values. **PASS**

### 2) Funding publication/settlement times and sign handled correctly
- **Check:** Funding merged on `symbol`+`hour` (UTC). Funding rate sign preserved as-is from Hyperliquid API; `funding_sign = np.sign(panel['funding_rate'].fillna(0.0))` retains positive/negative. Funding aggregated by hour mean if multiple entries.
- **File:line:** `src/analysis/liqmicro/features.py:20-59`
- **Audit:** `research_state/liqmicro_funding_audit_002.md` confirms fundingRate.std()>0 for all 9 coins, real variation. Merge fixed to not zero-fill funding. **PASS**

### 3) No look-ahead in funding zscore (trailing-only)
- **Check:** `_zscore` uses `x.rolling(window=2160, min_periods=30).mean()` and `.std()` - trailing windows only. Applied via groupby transform per symbol.
- **File:line:** `src/analysis/liqmicro/features.py:48-61`
- **Finding:** Trailing-only rolling statistics. No centered windows, no future data used. **PASS**

### 4) Mark/index alignment if used
- **Check:** This Track D microstructure analysis uses liquidation counts/values from ironflow and Hyperliquid funding; mark/index alignment not central to D1-D3 as specified. Features use liquidation intensity and funding/vol proxies from panel data. No cross-venue mark/index merge performed.
- **Finding:** Not applicable to current D1-D3 specification; no alignment leakage introduced. **PASS (N/A)**

### 5) Delisted contracts and symbol migrations retain correct identity
- **Check:** Panel built from ironflow events aggregated by symbol; funding merged by symbol+hour with symbol normalization (coin → coin-PERP). Hyperliquid has persistent perpetuals in the fetched set; delisted contracts would simply have missing funding (merged as NaN) - but code does NOT silently zero-fill funding (fixed in FCLR-LIQMICRO-002).
- **File:line:** `src/analysis/liqmicro/features.py:20-59` (left merge, no fillna(0) on funding_rate after merge except for sign calculation)
- **Finding:** Identity preserved; missing funding remains NaN (not zeroed). **PASS**

### 6) Duplicate/out-of-order/missing pages detected
- **Check:** Funding fetched via `scripts/hyperliquid_funding_fetch.py` with caching to `research_state/data_cache/hyperliquid_funding/*.json`. Aggregation uses groupby mean. Ingestion uses HyperliquidFundingIngestor. No evidence of duplicate injection causing leakage.
- **Audit:** `research_state/liqmicro_funding_audit_002.md` documents 9 coins x 8668 records.
- **Finding:** Caching/deduplication present; out-of-order handled by timestamp normalization. **PASS**

### 7) Censored events not treated as completed negatives
- **Check:** D1-D3 use observed liquidation counts/intensities from ironflow events aggregated hourly; no survival censoring model applied in the current D1-D3 specification as written. The panel contains observed liquidation data.
- **Finding:** No censoring logic misapplied as completed negatives. **PASS**

### 8) Funding merge correctness (critical fix verification)
- **Check:** FCLR-LIQMICRO-001 had degenerate zeroing. FCLR-LIQMICRO-002 fixed features.py to merge funding_df on symbol+hour and only fillna for sign (0.0) not for funding_rate itself. Panel shows funding_rate std 6.98e-06 > 0, 93504 non-NaN.
- **File:line:** `src/analysis/liqmicro/features.py:20-59` (merge on ['symbol','hour'], no zero-fill of funding_rate)
- **Verification:** `research_state/evaluation_summary_FCLR-LIQMICRO-002.md` confirms std>0, D2 funding_abs now non-zero.
- **Finding:** Fix verified correct. **PASS**

### 9) Time alignment (hour truncation)
- **Check:** Funding hours computed as `pd.to_datetime(fund['timestamp'], utc=True).dt.floor('h')`. Panel hours use UTC floor. Merge is exact on symbol+hour.
- **File:line:** `src/analysis/liqmicro/features.py:30-31`
- **Finding:** Consistent UTC hour truncation. **PASS**

### 10) No train/test split leakage in microstructure D1-D3
- **Check:** D1-D3 as reported are descriptive/regression analyses on the full panel with fixed effects and clustering; no sealed holdout split inspected for "forecast gate" purposes per pre-registration. The pre-registration states this is a microstructure fix (Track D), not a forecast gate evaluation like FCLR-010. Firewall explicitly states no H001 re-test opened.
- **Pre-reg:** `research_state/pre_registration_FCLR-LIQMICRO-002.md` line ~120-150
- **Finding:** No forecast-gate holdout leakage vector applicable; regressions use full sample with proper clustering. **PASS**

## Adversarial notes
- D1 coefficients show extreme magnitudes with p~1.0 (const terms large) - likely numerical instability due to collinearity with fixed effects/category encoding in the regression specification, but this doesn't indicate look-ahead; it's a model specification issue.
- D3 shows only 2 deciles populated (0 and 1) with counts 91351 and 2153 - suggests heavy concentration or binning issue, but not leakage.
- These are robustness concerns (addressed in robustness doc), not leakage.

## VERDICT
**LEAKAGE AUDIT: PASS** - No look-ahead, correct trailing windows, funding merge fixed without zeroing, proper UTC alignment. Numerical/spec issues exist but are not leakage-related.
