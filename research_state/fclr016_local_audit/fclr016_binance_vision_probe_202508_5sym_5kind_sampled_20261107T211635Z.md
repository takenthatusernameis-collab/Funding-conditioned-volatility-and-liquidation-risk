# FCLR-016 Binance Vision provenance probe 2025+ (20261107T211635Z_202508_5sym_5kind_sampled)

- method: bounded unauthenticated GET vs local cached zip sha256/etag (FCLR-016, 2025+ probe)
- cache_identity_vs_binance_vision: **NO_GO**
- confirmatory_claim_go: **NO_GO** (identity evidence only; prereg/leakage/license/completeness required)
- summary: `{"match": 49, "mismatch": 36, "missing_local": 0, "missing_remote": 0, "new_this_run": 85, "remote_error": 0, "total": 85}`

## FCLR-014 context
2025+ cache provenance UNVERIFIED per fclr014_provenance_decision_20261107T133102Z.md; identity match is necessary but not sufficient (license/terms/completeness/leakage/prereg still required).

## Result counts
- MATCH: 49
- MISMATCH: 36

## Non-MATCH (first 60)
- MISMATCH BNBUSDT 2025-08 klines 2025-08-01 local=72f4e3cde1c2808d remote=cef24b77002b6e96
- MISMATCH BNBUSDT 2025-08 klines 2025-08-15 local=e86b1fcc5520ef36 remote=b09357a2b31d052b
- MISMATCH BNBUSDT 2025-08 klines 2025-08-28 local=de86d0ca6f011e29 remote=e3f2cdc316eb5647
- MISMATCH BNBUSDT 2025-08 klines 2025-08-31 local=2cdba848a4f43401 remote=6e30848d415be2cb
- MISMATCH BNBUSDT 2025-08 markPriceKlines 2025-08-01 local=72f4e3cde1c2808d remote=4ca39c1cdb198a1a
- MISMATCH BNBUSDT 2025-08 markPriceKlines 2025-08-15 local=e86b1fcc5520ef36 remote=a8dd2eec18922a45
- MISMATCH BNBUSDT 2025-08 markPriceKlines 2025-08-28 local=de86d0ca6f011e29 remote=f2584040354d7561
- MISMATCH BNBUSDT 2025-08 indexPriceKlines 2025-08-15 local=e86b1fcc5520ef36 remote=6e6c29f192305759
- MISMATCH BNBUSDT 2025-08 indexPriceKlines 2025-08-31 local=2cdba848a4f43401 remote=1a46b397db77edc1
- MISMATCH BNBUSDT 2025-08 premiumIndexKlines 2025-08-01 local=72f4e3cde1c2808d remote=449eb700005e6c9f
- MISMATCH BNBUSDT 2025-08 premiumIndexKlines 2025-08-28 local=de86d0ca6f011e29 remote=eb67c60756f8ff56
- MISMATCH BNBUSDT 2025-08 premiumIndexKlines 2025-08-31 local=2cdba848a4f43401 remote=ecf59d71d741a904
- MISMATCH SOLUSDT 2025-08 klines 2025-08-01 local=d6eb6eb1aa37cde9 remote=9cc469984d1e5344
- MISMATCH SOLUSDT 2025-08 klines 2025-08-15 local=c8b60141ef9b048e remote=339a887c89512415
- MISMATCH SOLUSDT 2025-08 klines 2025-08-28 local=42dcae69c5fc9235 remote=ad6266fd9b5042e1
- MISMATCH SOLUSDT 2025-08 klines 2025-08-31 local=fd2be2bc2146c9f3 remote=ba29d3640d8c7301
- MISMATCH SOLUSDT 2025-08 markPriceKlines 2025-08-15 local=c8b60141ef9b048e remote=c081006e7fae600e
- MISMATCH SOLUSDT 2025-08 markPriceKlines 2025-08-28 local=42dcae69c5fc9235 remote=c0cda60e2136b618
- MISMATCH SOLUSDT 2025-08 indexPriceKlines 2025-08-01 local=d6eb6eb1aa37cde9 remote=0e44a62c0d74c685
- MISMATCH SOLUSDT 2025-08 indexPriceKlines 2025-08-15 local=c8b60141ef9b048e remote=3394d291829441e0
- MISMATCH SOLUSDT 2025-08 indexPriceKlines 2025-08-28 local=42dcae69c5fc9235 remote=82abb914d7ad1273
- MISMATCH SOLUSDT 2025-08 indexPriceKlines 2025-08-31 local=fd2be2bc2146c9f3 remote=4ce1188228f2929a
- MISMATCH SOLUSDT 2025-08 premiumIndexKlines 2025-08-01 local=d6eb6eb1aa37cde9 remote=d3a67502f2a17fa7
- MISMATCH SOLUSDT 2025-08 premiumIndexKlines 2025-08-31 local=fd2be2bc2146c9f3 remote=519b605931f9d9da
- MISMATCH XRPUSDT 2025-08 klines 2025-08-01 local=01ee1e93387c2102 remote=f3f883671fec8d44
- MISMATCH XRPUSDT 2025-08 klines 2025-08-15 local=ea5d5311956a7c51 remote=e419b1745dfba5e6
- MISMATCH XRPUSDT 2025-08 klines 2025-08-28 local=7d5cd512dbadb578 remote=9903d4943516dffa
- MISMATCH XRPUSDT 2025-08 klines 2025-08-31 local=7e9287396fa9697c remote=e89a8ccaa2fbd1f8
- MISMATCH XRPUSDT 2025-08 markPriceKlines 2025-08-01 local=01ee1e93387c2102 remote=5bfcf5807d09c309
- MISMATCH XRPUSDT 2025-08 markPriceKlines 2025-08-15 local=ea5d5311956a7c51 remote=be38f176e82a5794
- MISMATCH XRPUSDT 2025-08 markPriceKlines 2025-08-28 local=7d5cd512dbadb578 remote=9a60a64485e66ddf
- MISMATCH XRPUSDT 2025-08 markPriceKlines 2025-08-31 local=7e9287396fa9697c remote=7276b331de019c68
- MISMATCH XRPUSDT 2025-08 indexPriceKlines 2025-08-01 local=01ee1e93387c2102 remote=f39a7fe1323b2c98
- MISMATCH XRPUSDT 2025-08 indexPriceKlines 2025-08-15 local=ea5d5311956a7c51 remote=13e532cf5a9e628e
- MISMATCH XRPUSDT 2025-08 indexPriceKlines 2025-08-31 local=7e9287396fa9697c remote=46e73c69cf188b90
- MISMATCH XRPUSDT 2025-08 premiumIndexKlines 2025-08-28 local=7d5cd512dbadb578 remote=f7d58698bb956ddc
