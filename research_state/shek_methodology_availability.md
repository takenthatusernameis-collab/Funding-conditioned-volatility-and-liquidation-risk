# Shek (SSRN, posted 29 Sep 2026) methodology — availability record

Source requested: Helvin Shek, "Limits to Coordination: Funding Drag in Crypto Perpetual Funding Rates," SSRN, posted 29 September 2026. URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7529458 (abstract id 7529458).

## Access attempt

- Abstract page: HTTP 403 (blocked in this environment).
- PDF delivery URL (https://papers.ssrn.com/sol3/Delivery.cfm/7529458.pdf?abstractid=7529458&mirid=1): HTTP 403.
- Web search snippet recovered partial abstract text only.

## Recoverable details (from search snippet, not independently verified)

- 1,696 events across 18 Binance perpetual contracts.
- Median time to funding-extreme correction: 27.0 hours in high-volatility conditions vs 3.0 hours in low-volatility conditions.
- Test reported: log-rank chi-square 147.25, p < (truncated in snippet).
- Keywords: Perpetual Futures, Funding Rates, Limits to Arbitrage, Survival Analysis, Realized Volatility.
- Author page lists a related paper: "Conditional Arbitrage Capacity: Evidence from Crypto Perpetual Funding Rates" (abstract id 7520320), 274 funding-rate extreme events across BTC/ETH/SOL 2021-2026, +1.88% reversal over 24h on up days vs -1.74% continuation on down days.

## Full methodology not recoverable

The following items needed for exact replication are not available from public sources without the paper PDF:

- Funding-extreme event definition (threshold on funding rate, percentile, or z-score; lookback window; deduplication/censoring of overlapping events).
- Realized-volatility regime split (window length, annualization, high/low cutoff, whether regime is pre-event or rolling).
- Correction/censoring rule: what constitutes "correction" (funding rate crossing back to median/zero, price parity restoration), censoring of uncorrected events, maximum follow-up horizon.
- Survival model specification (Kaplan-Meier, Cox, or parametric; covariates; clustering by contract; bootstrap procedure).
- Sample period and contract selection criteria for the 18 contracts.
- Any fee, funding, or price-reference adjustments.

## Conclusion

FCLR-H002 remains PARTIAL_REPLICATION. The Shek paper's full event-definition and censoring rules could not be obtained from admissible public sources in this environment (SSRN 403). The replication in scripts/funding_correction_replication.py stands as an independent reconstruction (445 events, 5 symbols, Jan-Mar 2024, median correction time 8.0h among corrected events) and must not be promoted to exact replication or to volatility-forecast/liquidation evidence. Correction time must not be conflated with forecast skill. Risk-overlay phase remains INELIGIBLE.
