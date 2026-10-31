# H002 Replication Blocker

**Status: PARTIAL_REPLICATION (RV-regime contrast RESOLVED 2026-10-31; still PARTIAL overall)**

## Blocker removed (2026-10-31)
- **What blocked:** RV-regime contrast was uncomputable because no Jan–Mar 2024 mark prices were cached (h002_replication_report.md §4, this file prior version).
- **Removal:** `scripts/h002_download_2024_q1.py` executed against the free unauthenticated `data.binance.vision` daily archive (HTTP 200 verified on a probe). 1,365/1,365 files downloaded: 5 symbols x 91 days x 3 kinds (markPriceKlines, indexPriceKlines, premiumIndexKlines); Feb 2024 = 29 days as expected. Written to `research_state/data_cache/{SYM}_{YYYY}_{MM}/`. `load_errors: []`.
- **Result:** RV-regime contrast now computed. High-RV median 16.0 h vs low-RV 8.0 h; log-rank chi2=3.08, two-sided p=0.0792; direction_lower_hazard_high_rv = true. Direction matches the paper's claimed direction but is NOT statistically significant at the 5% level, and magnitude differs from the paper (27 h / 3 h).

## Remaining blocker (NOT removed)
- SSRN 7529458 returns HTTP 403, blocking access to the paper's full methodology, event definition, censoring rules, RV-regime split, survival model, and contract selection. H002 therefore remains **PARTIAL** — it cannot be promoted to exact replication, confirmatory, volatility-forecast-skill, or liquidation evidence.

## What must not be repeated
- Do not treat the p=0.079 directional result as a confirmation of the paper's claim.
- Do not conflate correction time with volatility forecast skill, hypothetical boundary-breach prediction, or observed liquidation outcomes (RESEARCH_PROMPT.md §15).
- Do not re-attempt SSRN access; it is blocked by HTTP 403 in this environment.
- Do not re-run the sealed FCLR-001/002/003/004/005/006/007 forecast gates or the risk overlay (INELIGIBLE).