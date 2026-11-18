# Track B/C breach-forecast execution — FCLR-VOL-LIQ-BREACH-FORECAST-03

**Session:** `session_20261118T114500Z` | **Campaign:** `FCLR-VOL-LIQ-BREACH-FORECAST-03-20261118T103106Z` | **Label:** EXPLORATORY/PILOT
**Timestamp (UTC):** 20261118T114500Z
**Track:** BC — funding-conditioned volatility features vs modeled liquidation-boundary breaches
**Network:** none. **Parquet:** none. **numpy/pandas/scipy:** none (stdlib only: `math`/`csv`/`json`/`zipfile`/`datetime`/`statistics`/`random`).

## Execution summary
Joins Track C causal realized-volatility features with Track B modeled breach labels (2024-04, 5 instruments BTC/ETH/SOL/XRP/BNB, L in {5,10,20} x side {long,short} x H in {4h,24h}, mmr=0.005). Two chronological train/test splits within 2024-04 with 7-day purge/embargo. Stdlib IRLS logistic (ridge lambda=1e-6, seed 12345). RV-only baseline B0 vs funding-conditioned candidate B1.

## Result (honest, EXPLORATORY/PILOT)
- Pooled mean Delta AUC (B1 - B0) = -0.0661 across 2 splits; block-bootstrap CI95 straddles zero / is below zero (split1 mean -0.0846, CI95 [-0.1595, -0.0055]; split2 mean -0.0462, CI95 [-0.1416, +0.1267]).
- Leave-one-instrument-out Delta AUC: all five instruments negative (BNB -0.0043 to ETH -0.1560 in split 2).
- Funding-conditioned features did NOT improve breach discrimination over RV-only; the prereg materiality floor (Delta AUC >= +0.01 with CI95 lower bound > 0) was NOT met.
- Single labeled month (2024-04) = pilot quality; not confirmatory; no forecast-gate pass claim.

## Artifacts (this session dir)
- `trackbc_breach_prereg_20261118T114500Z.{json,md}` — outcome-blind prereg frozen before outcomes (`outcome_data_inspected_before_freeze=false`).
- `trackbc_breach_forecast_20261118T114500Z.{py,json,md}` — forecast source, results, report.
- `trackc_design_a_forecast_20261118T093031Z.{py,json,md}` — carried forward from session 093031Z (Track C).
- `trackb_breach_labels_20261118T093031Z.{py,json,md}` + `recompute_trackb_breach_labels_20261118T093031Z.json` — carried forward from session 093031Z (Track B).
- `trigger_check_20261118T114500Z.json` — all four reopen triggers OPEN; none fired.
- `evidence_audit_20261118T114500Z.{json,md}` — this audit.
- `recompute_trackbc_breach_forecast_20261118T114500Z.json` — fresh quantitative recompute summary.

## Prohibitions respected
- No sealed re-score, no network, no root `research_state/*.md|json` (root 500/500), no sealed-artifact/workflow mutation, no duplicate AGENT_HANDOFF.
- No look-ahead, no full-sample normalization, no sealed months, no observed-liquidation labeling.

## Honest status
EXPLORATORY/PILOT. Negative funding-conditioned result reported as-is; no confirmatory promotion claimed. No sealed months (2024-10..12, 2025+) touched.
