# FCLR-006 COVERAGE-ONLY AUDIT (NO OUTCOME INSPECTION)

Audit timestamp: 2026-10-30T12:52:01Z
Repo: /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
Window: 2026-04-01 through 2026-07-31
Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT

## Symbol-Month Coverage

### BTCUSDT
- 2026_04: exists, markPriceKlines_dirs=30, indexPriceKlines_dirs=30, funding_files=2
- 2026_05: exists, markPriceKlines_dirs=31, indexPriceKlines_dirs=31, funding_files=2
- 2026_06: exists, markPriceKlines_dirs=30, indexPriceKlines_dirs=30, funding_files=2
- 2026_07: exists, markPriceKlines_dirs=37, indexPriceKlines_dirs=37, funding_files=4

### ETHUSDT
- 2026_04: exists, markPriceKlines_dirs=30, indexPriceKlines_dirs=30, funding_files=2
- 2026_05: exists, markPriceKlines_dirs=31, indexPriceKlines_dirs=31, funding_files=2
- 2026_06: exists, markPriceKlines_dirs=30, indexPriceKlines_dirs=30, funding_files=2
- 2026_07: exists, markPriceKlines_dirs=37, indexPriceKlines_dirs=37, funding_files=4

### BNBUSDT
- 2026_04: exists, markPriceKlines_dirs=30, indexPriceKlines_dirs=30, funding_files=2
- 2026_05: exists, markPriceKlines_dirs=31, indexPriceKlines_dirs=31, funding_files=2
- 2026_06: exists, markPriceKlines_dirs=30, indexPriceKlines_dirs=30, funding_files=2
- 2026_07: exists, markPriceKlines_dirs=37, indexPriceKlines_dirs=37, funding_files=4

### SOLUSDT
- 2026_04: exists, markPriceKlines_dirs=30, indexPriceKlines_dirs=30, funding_files=2
- 2026_05: exists, markPriceKlines_dirs=31, indexPriceKlines_dirs=31, funding_files=2
- 2026_06: exists, markPriceKlines_dirs=30, indexPriceKlines_dirs=30, funding_files=2
- 2026_07: exists, markPriceKlines_dirs=37, indexPriceKlines_dirs=37, funding_files=4

### XRPUSDT
- 2026_04: exists, markPriceKlines_dirs=30, indexPriceKlines_dirs=30, funding_files=2
- 2026_05: exists, markPriceKlines_dirs=31, indexPriceKlines_dirs=31, funding_files=2
- 2026_06: exists, markPriceKlines_dirs=30, indexPriceKlines_dirs=30, funding_files=2
- 2026_07: exists, markPriceKlines_dirs=37, indexPriceKlines_dirs=37, funding_files=4

## Common Timestamps (markPriceKlines presence across all 5 symbols)

Common dates count: 128
Estimated common UTC hours (24h/day): 3072
First common date: 2026-04-01
Last common date: 2026-08-06

## Coverage Assessment

- SUFFICIENT: >=5 symbols and >=90 common days confirmed.

## Proposed Frozen Chronological Splits (COVERAGE-ONLY)

Proposed: 60/20/20 chronological split with 7-day purge/embargo boundaries.
Based on 128 common days from 2026-04-01 to 2026-08-06.
Split boundaries to be frozen in research_protocol_fclr006.md BEFORE outcome inspection.

## Source File Hashes (key files)

- research_state/data_cache/BTCUSDT_2026_04/markPriceKlines-2026-04-01/BTCUSDT-1h-2026-04-01.csv: 1edd33e2057082a81966c1764120662a4990b1cc982eac64379d0ac3932661be
- research_state/data_cache/BTCUSDT_2026_04/markPriceKlines-2026-04-02/BTCUSDT-1h-2026-04-02.csv: 856ee99bc425d39952354cf02854f746f9254d4621a93e89b4e371376d9f5bc1
- research_state/data_cache/ETHUSDT_2026_04/markPriceKlines-2026-04-01/ETHUSDT-1h-2026-04-01.csv: 0ae5a966d1d73b5f6188d4b0b350f576c1d84a53edd8ae3dcfff4733c91436ed
- research_state/data_cache/ETHUSDT_2026_04/markPriceKlines-2026-04-02/ETHUSDT-1h-2026-04-02.csv: bb530b20261b4130fa85dd136f54f7400fe791da23fe392443044cafd29a5da1
