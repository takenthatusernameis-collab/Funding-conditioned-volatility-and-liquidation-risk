# FCLR-007 COVERAGE-ONLY AUDIT (NO OUTCOME INSPECTION)

Audit timestamp: 2026-10-30T23:59:19Z
Repo: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
Window: 2026-04-01 through 2026-07-31 (~122 days)
Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT

## Symbol-Month Coverage
### BTCUSDT
- markPriceKlines rows: 2928
- first: 2026-04-01T00:00:00+00:00
- last: 2026-07-31T23:00:00+00:00
### ETHUSDT
- markPriceKlines rows: 2928
- first: 2026-04-01T00:00:00+00:00
- last: 2026-07-31T23:00:00+00:00
### BNBUSDT
- markPriceKlines rows: 2928
- first: 2026-04-01T00:00:00+00:00
- last: 2026-07-31T23:00:00+00:00
### SOLUSDT
- markPriceKlines rows: 2928
- first: 2026-04-01T00:00:00+00:00
- last: 2026-07-31T23:00:00+00:00
### XRPUSDT
- markPriceKlines rows: 2928
- first: 2026-04-01T00:00:00+00:00
- last: 2026-07-31T23:00:00+00:00

## Common Timestamps (markPriceKlines presence across all 5 symbols)
- Common dates/timestamps count: 2928
- First common timestamp: 2026-04-01T00:00:00+00:00
- Last common timestamp: 2026-07-31T23:00:00+00:00
- Common gaps (non-hourly steps): 0

## Coverage Assessment
- >=5 symbols: PASS (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT)
- >=90 common days: data window is 122 days; common hourly timestamps span the full window subject to gaps above
- Block claim-worthy test under proposed splits: test window 11 days = 0 blocks -> NOT_MET (documented shortfall; do not relax after outcomes)

## Proposed Frozen Chronological Splits (60/20/20, 7-day purge/embargo)
- Train: 2026-04-01T00:00:00Z .. 2026-06-12T23:00:00Z (73 days)
- Embargo: 2026-06-13T00:00:00Z .. 2026-06-19T23:00:00Z (7 days)
- Validation: 2026-06-20T00:00:00Z .. 2026-07-13T23:00:00Z (24 days)
- Embargo: 2026-07-14T00:00:00Z .. 2026-07-20T23:00:00Z (7 days)
- Test/holdout: 2026-07-21T00:00:00Z .. 2026-07-31T23:00:00Z (11 days)

## Funding Rate Coverage
- BTCUSDT: 366 rows; missing months: []
- ETHUSDT: 366 rows; missing months: []
- BNBUSDT: 366 rows; missing months: []
- SOLUSDT: 366 rows; missing months: []
- XRPUSDT: 366 rows; missing months: []

## Source File Hashes (key markPriceKlines files)
- research_state/data_cache/BTCUSDT_2026_04/markPriceKlines-2026-04-01/BTCUSDT-1h-2026-04-01.csv: 1edd33e2057082a81966c1764120662a4990b1cc982eac64379d0ac3932661be
- research_state/data_cache/ETHUSDT_2026_04/markPriceKlines-2026-04-01/ETHUSDT-1h-2026-04-01.csv: 0ae5a966d1d73b5f6188d4b0b350f576c1d84a53edd8ae3dcfff4733c91436ed
- research_state/data_cache/BNBUSDT_2026_04/markPriceKlines-2026-04-01/BNBUSDT-1h-2026-04-01.csv: 4bc76dac063b0ee9fe3d845706b3fa1bea724c681e28d1aaa4aff98e704c662f
- research_state/data_cache/SOLUSDT_2026_04/markPriceKlines-2026-04-01/SOLUSDT-1h-2026-04-01.csv: 67135ca8d51f6af3035da40b00ea40f9c127d09bee054900d03d4c2365b4122e
- research_state/data_cache/XRPUSDT_2026_04/markPriceKlines-2026-04-01/XRPUSDT-1h-2026-04-01.csv: b6ad944e6319dbecf2076ec043e0c099ce3311a268c4b545d70e79162c70a006
- research_state/data_cache/BTCUSDT_2026_04/markPriceKlines-2026-04-02/BTCUSDT-1h-2026-04-02.csv: 856ee99bc425d39952354cf02854f746f9254d4621a93e89b4e371376d9f5bc1
- research_state/data_cache/ETHUSDT_2026_04/markPriceKlines-2026-04-02/ETHUSDT-1h-2026-04-02.csv: bb530b20261b4130fa85dd136f54f7400fe791da23fe392443044cafd29a5da1
- research_state/data_cache/BNBUSDT_2026_04/markPriceKlines-2026-04-02/BNBUSDT-1h-2026-04-02.csv: 4519571daeacb81acfa26717b3fd81a0095f959d005b658237a6b8ee7105cf3b
(first 8 of 610 hashed files shown; full hashes available on re-run)

## Constraints
- Coverage-only audit: no outcome, QLIKE, or model result inspected in this step.
- Splits frozen in this audit BEFORE any outcome computation; pre-registration follows in research_state/research_protocol_fclr007.md v1.0.
- No reuse of sealed FCLR-001/002/003/005/006 holdouts.
