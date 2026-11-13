# Prereg — FCLR-LIQ-010-CONFIRM-20261113T063000Z (Track A, P1)

**Status:** `FROZEN_PRE_OUTCOMES`
**Frozen (UTC):** 2026-11-13T06:30:00Z
**Outcome data inspected before freeze:** false
**Campaign:** `FCLR-NEXT-CAMPAIGN-20261113T063000Z`
**Cell:** `LIQ-010-CONFIRM`

## Claim
The sealed FCLR-010 observed-liquidation PASS (combined C2 vs RV-only B1, Brier
contrast −0.003077, 95% CI [−0.004892, −0.001263], 2.21%) replicates in direction
and significance under an independent recompute on the cached Hyperliquid ironflow
census restricted to the 17 symbols with cached funding.

## Disclosure
The sealed FCLR-010 used 199 instruments via live Hyperliquid access. Only 17 symbols
retain cached funding offline. This is a narrower but honest independent recompute,
not a re-score. The 17-symbol test grid holds ~12.5k events (vs sealed 12,450).

## Universe (fixed by cache)
AAVE, ADA, AVAX, BCH, BNB, BTC, CRV, DOGE, ETH, LINK, LTC, NEAR, SOL, SUI, UNI, XRP, ZEC.

## Data (cached only)
- Labels: `research_state/data_cache/ironflow_events/*.parquet` (18 months) and
  `results/liqmicro_v2/panel_liqmicro_v2.parquet` (hourly `liq_count`).
- Funding: `research_state/data_cache/hyperliquid_funding/{SYM}.json` (`time`,
  `fundingRate`, `premium`).

## Label and grid
- Unit: symbol × fully closed UTC hour.
- Occurrence: `1` if `liq_count >= 1`, else `0` on the complete hourly grid.
- Test window 2026-05-28..2026-10-31, 30-day blocks, 7-day embargo.

## Models (fixed)
- B1 (RV-only): `log_rv24h`, `log_rv168h`.
- C1: B1 + `signed_funding`, `abs_funding_pct`.
- C2 (combined): C1 + `premium`.

## Inference
- Primary contrast C2 vs B1 on Brier.
- 2000-replicate block bootstrap, seed 20261113.
- Holm across {C2_vs_B1, C1_vs_B1, C2_vs_C1}.
- Placebo: 200 funding permutations, seed 20261113.
- LOIO: 5 holdouts, ≥4/5 must pass.
- Leakage audit: causal features, embargo enforced.

## Verdict rules
- `CONFIRMED`: all checks pass.
- `FRAGILE`: primary passes, ≥1 robustness check fails.
- `NOT_REPLICATED`: primary CI includes zero or rel reduction < 2%.
- `INCONCLUSIVE`: insufficient valid rows / data defect.

## Artifacts
- `research_state/fclr_liq_010_confirm_panel_<UTC>.parquet`
- `research_state/fclr_liq_010_confirm_build_report_<UTC>.json`
- `research_state/evaluation_summary_FCLR-LIQ-010-CONFIRM-<UTC>.{md,json}`
- Gate: `scripts/fclr_liq_010_confirm_gate.py` → `GATE: PASS`.

## Bans
No network; no mutation of sealed FCLR-010; no threshold shopping; no core-feature
fill (funding ffill is causal and disclosed); no paid/credentialed data; do not expand
the 17-symbol universe with live data.