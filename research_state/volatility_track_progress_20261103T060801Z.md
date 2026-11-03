# VOLATILITY FORECASTING TRACK (Track B) - Progress Report
**TIMESTAMP:** 20261103T060801Z
**STATUS:** UNBLOCKED - HEAVY EXECUTION IN PROGRESS

## Data Availability
- Klines (1h), markPriceKlines (1h), funding rates present for BTC/ETH/SOL/XRP Jan-Mar 2024
- Broader cached data in research_state/data_cache/ (many symbols/months 2024-2025)
- Fully viable for funding-conditioned volatility forecasting per RESEARCH_PROMPT

## Infrastructure Built
- Created src/volatility/features.py (RV, trailing/forward RV, log returns)
- Created src/volatility/splits.py (chronological split utilities)
- Following leakage-resistant design (trailing-only features)

## Next Steps
- [ ] Build full feature pipeline with funding features (signed/abs, percentiles, time-to-funding)
- [ ] Add price-dislocation features (premium/basis, mark-index, MA deviations)
- [ ] Implement chronological evaluation with frozen protocol
- [ ] Run baselines (persistence, RV-only HAR) vs funding-conditioned models
- [ ] Document results with proper metrics and uncertainty

## Compliance
- Chronological splits only (no random splits)
- Trailing features only (no lookahead)
- Normalize on train only
- Preserve negative results
- Separate from Track A (liquidation labels)