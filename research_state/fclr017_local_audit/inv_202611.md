# FCLR-017 Gate 4 cache coverage audit (20261111T005051Z)

- method: deterministic local filesystem inventory; read-only; no network; no model-outcome computation
- cache_root: `research_state/data_cache`
- symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
- months: 2026-11
- global_all_months_ok: **False**
- v3_30d_calendar_consistency: **GAPS_OR_ANOMALIES_DOCUMENTED**
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
- months_present: 1/1
- missing_month_dirs: `[]`
- missing_days_by_kind: `{"indexPriceKlines": 22, "klines": 23, "markPriceKlines": 22, "premiumIndexKlines": 22}`
- canonical_zip_days_by_kind: `{"indexPriceKlines": 7, "klines": 7, "markPriceKlines": 7, "premiumIndexKlines": 7}`
- funding_months_with_expected_source: 0/6
- quarantine_or_placeholder_anomaly_count: 0
- all_months_ok: **False**

### ETHUSDT
- months_present: 1/1
- missing_month_dirs: `[]`
- missing_days_by_kind: `{"indexPriceKlines": 22, "klines": 23, "markPriceKlines": 22, "premiumIndexKlines": 22}`
- canonical_zip_days_by_kind: `{"indexPriceKlines": 7, "klines": 7, "markPriceKlines": 7, "premiumIndexKlines": 7}`
- funding_months_with_expected_source: 0/6
- quarantine_or_placeholder_anomaly_count: 0
- all_months_ok: **False**

### BNBUSDT
- months_present: 1/1
- missing_month_dirs: `[]`
- missing_days_by_kind: `{"indexPriceKlines": 22, "klines": 23, "markPriceKlines": 22, "premiumIndexKlines": 22}`
- canonical_zip_days_by_kind: `{"indexPriceKlines": 7, "klines": 7, "markPriceKlines": 7, "premiumIndexKlines": 7}`
- funding_months_with_expected_source: 0/6
- quarantine_or_placeholder_anomaly_count: 0
- all_months_ok: **False**

### SOLUSDT
- months_present: 1/1
- missing_month_dirs: `[]`
- missing_days_by_kind: `{"indexPriceKlines": 22, "klines": 23, "markPriceKlines": 22, "premiumIndexKlines": 22}`
- canonical_zip_days_by_kind: `{"indexPriceKlines": 7, "klines": 7, "markPriceKlines": 7, "premiumIndexKlines": 7}`
- funding_months_with_expected_source: 0/6
- quarantine_or_placeholder_anomaly_count: 0
- all_months_ok: **False**

### XRPUSDT
- months_present: 1/1
- missing_month_dirs: `[]`
- missing_days_by_kind: `{"indexPriceKlines": 22, "klines": 23, "markPriceKlines": 22, "premiumIndexKlines": 22}`
- canonical_zip_days_by_kind: `{"indexPriceKlines": 7, "klines": 7, "markPriceKlines": 7, "premiumIndexKlines": 7}`
- funding_months_with_expected_source: 0/6
- quarantine_or_placeholder_anomaly_count: 0
- all_months_ok: **False**

## v3-30d calendar consistency checks
- total: 55, failed: 45
- FAIL {"check": "no_missing_days", "detail": 23, "kind": "klines", "pass": false, "symbol": "BTCUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "klines", "pass": false, "symbol": "BTCUSDT"}
- FAIL {"check": "no_missing_days", "detail": 22, "kind": "markPriceKlines", "pass": false, "symbol": "BTCUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "markPriceKlines", "pass": false, "symbol": "BTCUSDT"}
- FAIL {"check": "no_missing_days", "detail": 22, "kind": "indexPriceKlines", "pass": false, "symbol": "BTCUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "indexPriceKlines", "pass": false, "symbol": "BTCUSDT"}
- FAIL {"check": "no_missing_days", "detail": 22, "kind": "premiumIndexKlines", "pass": false, "symbol": "BTCUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "premiumIndexKlines", "pass": false, "symbol": "BTCUSDT"}
- FAIL {"check": "funding_expected_source_each_requested_month", "detail": {"expected": 1, "have": 0}, "pass": false, "symbol": "BTCUSDT"}
- FAIL {"check": "no_missing_days", "detail": 23, "kind": "klines", "pass": false, "symbol": "ETHUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "klines", "pass": false, "symbol": "ETHUSDT"}
- FAIL {"check": "no_missing_days", "detail": 22, "kind": "markPriceKlines", "pass": false, "symbol": "ETHUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "markPriceKlines", "pass": false, "symbol": "ETHUSDT"}
- FAIL {"check": "no_missing_days", "detail": 22, "kind": "indexPriceKlines", "pass": false, "symbol": "ETHUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "indexPriceKlines", "pass": false, "symbol": "ETHUSDT"}
- FAIL {"check": "no_missing_days", "detail": 22, "kind": "premiumIndexKlines", "pass": false, "symbol": "ETHUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "premiumIndexKlines", "pass": false, "symbol": "ETHUSDT"}
- FAIL {"check": "funding_expected_source_each_requested_month", "detail": {"expected": 1, "have": 0}, "pass": false, "symbol": "ETHUSDT"}
- FAIL {"check": "no_missing_days", "detail": 23, "kind": "klines", "pass": false, "symbol": "BNBUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "klines", "pass": false, "symbol": "BNBUSDT"}
- FAIL {"check": "no_missing_days", "detail": 22, "kind": "markPriceKlines", "pass": false, "symbol": "BNBUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "markPriceKlines", "pass": false, "symbol": "BNBUSDT"}
- FAIL {"check": "no_missing_days", "detail": 22, "kind": "indexPriceKlines", "pass": false, "symbol": "BNBUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "indexPriceKlines", "pass": false, "symbol": "BNBUSDT"}
- FAIL {"check": "no_missing_days", "detail": 22, "kind": "premiumIndexKlines", "pass": false, "symbol": "BNBUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "premiumIndexKlines", "pass": false, "symbol": "BNBUSDT"}
- FAIL {"check": "funding_expected_source_each_requested_month", "detail": {"expected": 1, "have": 0}, "pass": false, "symbol": "BNBUSDT"}
- FAIL {"check": "no_missing_days", "detail": 23, "kind": "klines", "pass": false, "symbol": "SOLUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "klines", "pass": false, "symbol": "SOLUSDT"}
- FAIL {"check": "no_missing_days", "detail": 22, "kind": "markPriceKlines", "pass": false, "symbol": "SOLUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "markPriceKlines", "pass": false, "symbol": "SOLUSDT"}
- FAIL {"check": "no_missing_days", "detail": 22, "kind": "indexPriceKlines", "pass": false, "symbol": "SOLUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "indexPriceKlines", "pass": false, "symbol": "SOLUSDT"}
- FAIL {"check": "no_missing_days", "detail": 22, "kind": "premiumIndexKlines", "pass": false, "symbol": "SOLUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "premiumIndexKlines", "pass": false, "symbol": "SOLUSDT"}
- FAIL {"check": "funding_expected_source_each_requested_month", "detail": {"expected": 1, "have": 0}, "pass": false, "symbol": "SOLUSDT"}
- FAIL {"check": "no_missing_days", "detail": 23, "kind": "klines", "pass": false, "symbol": "XRPUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "klines", "pass": false, "symbol": "XRPUSDT"}
- FAIL {"check": "no_missing_days", "detail": 22, "kind": "markPriceKlines", "pass": false, "symbol": "XRPUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "markPriceKlines", "pass": false, "symbol": "XRPUSDT"}
- FAIL {"check": "no_missing_days", "detail": 22, "kind": "indexPriceKlines", "pass": false, "symbol": "XRPUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "indexPriceKlines", "pass": false, "symbol": "XRPUSDT"}
- FAIL {"check": "no_missing_days", "detail": 22, "kind": "premiumIndexKlines", "pass": false, "symbol": "XRPUSDT"}
- FAIL {"check": "canonical_zip_covers_calendar_days", "detail": {"expected": 0, "have": 7}, "kind": "premiumIndexKlines", "pass": false, "symbol": "XRPUSDT"}
- FAIL {"check": "funding_expected_source_each_requested_month", "detail": {"expected": 1, "have": 0}, "pass": false, "symbol": "XRPUSDT"}
