# FCLR-017 Gate 4 cache coverage audit (20261108T124022Z)

- method: deterministic local filesystem inventory; read-only; no network; no model-outcome computation
- cache_root: `research_state/data_cache`
- symbols: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT
- months: 2024-04, 2024-05, 2024-06, 2024-07, 2024-08, 2024-09
- global_all_months_ok: **True**
- v3_30d_calendar_consistency: **CONSISTENT**
- no_confirmatory_outcomes: **True**
- exploratory_only: **True**
- no_network: **True**

## Caveats / gates
- Audit/planning evidence only — **not GO for confirmatory outcomes**.
- v5 admissibility/terms blocker remains unresolved (`all_go=false`, terms `EXPLICIT_BLOCKER_UNRESOLVED`; `fabricated=false` per campaign state). This audit does not change that status.
- 2024-04..09 identity/provenance context: FCLR-015 bounded Binance Vision identity verification applies only where separately evidenced; this audit records local lineage/coverage, not remote identity.
- Confirmatory outcomes require fresh frozen prereg before outcomes and admissibility guards; 2024-04..09 confirmatory bounded by `PROVENANCED_CONFIRMATORY_RANGES` with manifest/terms evidence as required.
- Sealed v3-30d artifacts are untouched by this audit.

## Per-symbol summary
### BTCUSDT
- months_present: 6/6
- missing_month_dirs: `[]`
- missing_days_by_kind: `{"indexPriceKlines": 0, "klines": 0, "markPriceKlines": 0, "premiumIndexKlines": 0}`
- canonical_zip_days_by_kind: `{"indexPriceKlines": 183, "klines": 183, "markPriceKlines": 183, "premiumIndexKlines": 183}`
- funding_months_with_expected_source: 6/6
- quarantine_or_placeholder_anomaly_count: 0
- all_months_ok: **True**

### ETHUSDT
- months_present: 6/6
- missing_month_dirs: `[]`
- missing_days_by_kind: `{"indexPriceKlines": 0, "klines": 0, "markPriceKlines": 0, "premiumIndexKlines": 0}`
- canonical_zip_days_by_kind: `{"indexPriceKlines": 183, "klines": 183, "markPriceKlines": 183, "premiumIndexKlines": 183}`
- funding_months_with_expected_source: 6/6
- quarantine_or_placeholder_anomaly_count: 0
- all_months_ok: **True**

### SOLUSDT
- months_present: 6/6
- missing_month_dirs: `[]`
- missing_days_by_kind: `{"indexPriceKlines": 0, "klines": 0, "markPriceKlines": 0, "premiumIndexKlines": 0}`
- canonical_zip_days_by_kind: `{"indexPriceKlines": 183, "klines": 183, "markPriceKlines": 183, "premiumIndexKlines": 183}`
- funding_months_with_expected_source: 6/6
- quarantine_or_placeholder_anomaly_count: 0
- all_months_ok: **True**

### XRPUSDT
- months_present: 6/6
- missing_month_dirs: `[]`
- missing_days_by_kind: `{"indexPriceKlines": 0, "klines": 0, "markPriceKlines": 0, "premiumIndexKlines": 0}`
- canonical_zip_days_by_kind: `{"indexPriceKlines": 183, "klines": 183, "markPriceKlines": 183, "premiumIndexKlines": 183}`
- funding_months_with_expected_source: 6/6
- quarantine_or_placeholder_anomaly_count: 0
- all_months_ok: **True**

### BNBUSDT
- months_present: 6/6
- missing_month_dirs: `[]`
- missing_days_by_kind: `{"indexPriceKlines": 0, "klines": 0, "markPriceKlines": 0, "premiumIndexKlines": 0}`
- canonical_zip_days_by_kind: `{"indexPriceKlines": 183, "klines": 183, "markPriceKlines": 183, "premiumIndexKlines": 183}`
- funding_months_with_expected_source: 6/6
- quarantine_or_placeholder_anomaly_count: 0
- all_months_ok: **True**

## v3-30d calendar consistency checks
- total: 55, failed: 0
- All calendar/coverage checks passed for requested scope.
