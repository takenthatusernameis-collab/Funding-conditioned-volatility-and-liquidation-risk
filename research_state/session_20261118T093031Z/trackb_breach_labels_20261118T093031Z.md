# Track B — Modeled Liquidation-Boundary-Breach Labels (stdlib)

**Session:** session_20261118T093031Z
**Timestamp (UTC):** 20261118T093031Z
**Track:** B — modeled liquidation-boundary-breach labels
**Label type:** `synthetic_modeled_boundary_breach` — **observed_liquidation_labels=false**.
**Network:** none. **Parquet:** none. **numpy/pandas/scipy:** none (stdlib only).

## Design (outcome-blind, frozen ex ante)
- Month: 2024-04; instruments: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT
- Leverage L in {5, 10, 20}; side in {long, short}; horizon H in {4, 24} hours
- Entry at close of bar t (known at t); evaluate hourly mark path t+1..t+H.
- Maintenance-margin rate mmr=0.005 (0.5%); no funding carry, no fees, no account engine.
- Long boundary: `P0*(1 - 1/L)/(1 - mmr)`; short boundary: `P0*(1 + 1/L)/(1 + mmr)`.
- Breach if any mark in t+1..t+H crosses the boundary; record first-breach hour and signed clearance ratio.

## Results
- Total label rows: 41760; breached rows: 1418; overall breach rate: 0.03395593869731801

### Aggregate by scenario (breach rate / mean hours-to-breach)
| Scenario | n | breached | breach_rate | mean_hours_to_breach | min_clearance |
|---|---|---|---|---|---|
| L5|long|H4 | 3480 | 0 | 0.0 | None | 0.0036229576588381776 |
| L5|long|H24 | 3480 | 19 | 0.005459770114942529 | 14.263157894736842 | -0.017531260701477775 |
| L5|short|H4 | 3480 | 0 | 0.0 | None | 0.057839694126737944 |
| L5|short|H24 | 3480 | 0 | 0.0 | None | 0.034050571518981734 |
| L10|long|H4 | 3480 | 18 | 0.005172413793103448 | 3.0 | -0.09687955490397579 |
| L10|long|H24 | 3480 | 166 | 0.04770114942528736 | 13.457831325301205 | -0.11803377326429179 |
| L10|short|H4 | 3480 | 2 | 0.0005747126436781609 | 2.0 | -0.04166279343545103 |
| L10|short|H24 | 3480 | 24 | 0.006896551724137931 | 13.666666666666666 | -0.06545191604320724 |
| L20|long|H4 | 3480 | 60 | 0.017241379310344827 | 2.8333333333333335 | -0.14713081118538288 |
| L20|long|H24 | 3480 | 683 | 0.19626436781609197 | 13.572474377745241 | -0.1682850295456986 |
| L20|short|H4 | 3480 | 40 | 0.011494252873563218 | 3.0 | -0.09141403721654574 |
| L20|short|H24 | 3480 | 406 | 0.11666666666666667 | 14.071428571428571 | -0.11520315982430195 |

### Per-instrument breach rate (L10|long|H24 headline)

- BTCUSDT: 0.0
- ETHUSDT: 0.04597701149425287
- SOLUSDT: 0.09626436781609195
- XRPUSDT: 0.06752873563218391
- BNBUSDT: 0.028735632183908046

## Honest status
- EXPLORATORY/PILOT. Synthetic modeled boundary breaches only; not observed liquidations.
- No account-specific liquidation engine, portfolio margin, insurance fund, or forced-liquidation records reconstructed.
- No sealed months touched; no network; stdlib fallback for missing numpy/pandas/scipy.
