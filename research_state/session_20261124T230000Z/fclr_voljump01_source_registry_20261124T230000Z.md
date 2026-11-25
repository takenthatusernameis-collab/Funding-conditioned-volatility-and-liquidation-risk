# FCLR-VOL-JUMP-01 Source Registry (20261124T230000Z)

- experiment_id: FCLR-VOL-JUMP-01
- session_id: session_20261124T230000Z
- campaign: FCLR-VOL-JUMP-01-20261124T223000Z
- generated_utc: 2026-11-24T23:00:00Z
- source: ironflow_bulk (frozen on-disk cache; read-only; no network)
- cache_root: research_state/data_cache/ironflow_bulk
- month_span: 2025-05 .. 2026-10 (18 months)
- n_coins_universe_intersection: 466
- source_registry_json_sha256: e8d3bb5eb4ebde9439d3753c3241742f4f9e9239d90c817c2ab809fc519ef01b

## input_integrity
- sha256_all_match: True
- sha256_verified_bad: 0
- n_files: 54
- n_sidecars_checked: 54

## datasets
### candles_1h
- months: 18 (2025-05 .. 2026-10)
- total_rows: 3643742
- parquet_count: 18
- schema: timestamp, market, coin, dex, market_class, open, high, low, close, volume, trades
### funding
- months: 18 (2025-05 .. 2026-10)
- total_rows: 4104648
- parquet_count: 18
- schema: timestamp, market, coin, dex, funding_rate, premium
### open_interest
- months: 18 (2025-05 .. 2026-10)
- total_rows: 3977432
- parquet_count: 18
- schema: timestamp, market, coin, dex, mark_price, oracle_price, open_interest, open_interest_usd

## files (sha256-asserted)

- candles_1h/2025-05: rows=35550 sha256=9bd24cf774076f753f9692a663837f815853f755890434ba9a08e73600a86aef sha_match=True
- candles_1h/2025-06: rows=154237 sha256=f8eef410c8e21881e8511fec10a1a032b5ad37b21f94deef96b6f2f8cdc8131b sha_match=True
- candles_1h/2025-07: rows=156492 sha256=466c6ebc277045f231cbe18583d3aa41488bd27aed57a5effd118712b603d647 sha_match=True
- candles_1h/2025-08: rows=154531 sha256=bb5f2c85f874688f6fc154c576d0cc483445fa81bfcb28aa4024119aea248229 sha_match=True
- candles_1h/2025-09: rows=155796 sha256=ab22becbad69206cc01b4279604fabaaafb870bc54b2998c0bc243247db5f0f1 sha_match=True
- candles_1h/2025-10: rows=173905 sha256=f30ee1b41fe0c7405c4f5f0dba12adce2d19bdaa60f96bc31d1c1cc30395fad1 sha_match=True
- candles_1h/2025-11: rows=170678 sha256=bb2af7f07763589da702776c68880671e53dba2ab89d3281242ba41588920294 sha_match=True
- candles_1h/2025-12: rows=189790 sha256=3eb12fc5312276df6a1a8508b162dbf8e6a4b505713ccb1a372e954fe5b713db sha_match=True
- candles_1h/2026-01: rows=211494 sha256=a42260c697b59853b9321061ee03e146ac461708ead63a10c249839fca05b6ed sha_match=True
- candles_1h/2026-02: rows=216575 sha256=94e1bbbd3791b5b9770c5d9708974386aa1cb854c5e18d4eb25ca809113fe091 sha_match=True
- candles_1h/2026-03: rows=248859 sha256=6a34df24c25e4ecc147bc70e8d72df811df9ca1542cab4c523320f62616adf5b sha_match=True
- candles_1h/2026-04: rows=246842 sha256=6cab3cc3d6d3d8418d0c0dbbcff85c76d504008357a1695b39e12c57e2578180 sha_match=True
- candles_1h/2026-05: rows=259642 sha256=f8f0e158bdd4b47a3a522115297364194c56ef0ab5953b5f70b4f524ffb33a82 sha_match=True
- candles_1h/2026-06: rows=244727 sha256=1aabd11fdad5eadb7db7c7779c859ec6294d7c69e97b1f0782175b035036d4af sha_match=True
- candles_1h/2026-07: rows=234715 sha256=7b90e976c56a325875c86aeb8b5558a182d264c1e89e64d73356afafcda417b7 sha_match=True
- candles_1h/2026-08: rows=253467 sha256=3a48dfe803ffe46a30e598952d5e1c25557c7a6eb6bb7391c2cd2d5adea68759 sha_match=True
- candles_1h/2026-09: rows=259199 sha256=36ef6d8a476a526c2f8c12c3376405b7fab48939467d3bc40c0c673078541e59 sha_match=True
- candles_1h/2026-10: rows=277243 sha256=26f359c5c930e02020298faeeda04025d017b283610b9a2c97660385dc199324 sha_match=True
- funding/2025-05: rows=145771 sha256=26005d5d1bfd0719e8eeb5e4d4c0750dadfa63d0c8161ad476a6a55170455058 sha_match=True
- funding/2025-06: rows=143163 sha256=bb6b8878b6491961fbfbcb168b9906a0cc8b4c82586357f42424cac11733c729 sha_match=True
- funding/2025-07: rows=149324 sha256=ad9d01aa425af412fce534c83c7a4f3ee5997dc3f533a07681b2ad4e679522ee sha_match=True
- funding/2025-08: rows=150859 sha256=2cb155ad80289355fc96344316309fd48a4cccbef062a3c1e508cdb9f4152d27 sha_match=True
- funding/2025-09: rows=149815 sha256=f06b49dd307a7922a3e429bd9a06e0ddb4febe0d2556d7f232ce6a040f9db205 sha_match=True
- funding/2025-10: rows=161650 sha256=51c9ebd47a36afc31ae7907b539c1256e456132671f133be488ef3596c9e0a3d sha_match=True
- funding/2025-11: rows=163714 sha256=8a41b57b7ed53096127c27768e18b1516dff28522012f8d08159f6d2f577c640 sha_match=True
- funding/2025-12: rows=187787 sha256=b962029567cc5831d300cf7c4a947b255fc20469c48b2deebe1daf1804fa02f7 sha_match=True
- funding/2026-01: rows=212211 sha256=349a01e2f6518f63f18a8f7b55b168f563ee68faa16176b1f5e817edebea06e1 sha_match=True
- funding/2026-02: rows=221707 sha256=9fc4b300ba79dd79afe52823c805752d463b119e56afb9b2dc2732dbb67ed789 sha_match=True
- funding/2026-03: rows=258164 sha256=cc8dc6e57e6d512605f48d0f19039871829318c3a0632ed995b769d957490f2a sha_match=True
- funding/2026-04: rows=261864 sha256=008ca1c6864e5a48de61133a8ea4ddb8123be0db9cc291be1a4368e57710998a sha_match=True
- funding/2026-05: rows=283853 sha256=4340ecd686296a7b785ffb77570bd7e07254cc600fea7bb321721d386b7c57c0 sha_match=True
- funding/2026-06: rows=286045 sha256=467131e7320a3d568d289d6d10fcee3f4a0e1dde13b8a73bb04977035ab01678 sha_match=True
- funding/2026-07: rows=308381 sha256=98860209990f26f30786ffb4d8f21cf97002a7035e71a147c915d7af35da23df sha_match=True
- funding/2026-08: rows=325975 sha256=c067fcca81a1b6a5aaa0d636de16b99804d7de683ef90cde8ecd5c176db1bff0 sha_match=True
- funding/2026-09: rows=334762 sha256=d8e43faa444e64c263a078b855d8c1edb9ef73fba5b63ef908fc5aa9314ec7bc sha_match=True
- funding/2026-10: rows=359603 sha256=b081c40f350d3982d1279cd7d019a2d645aabd548cd30358a90e77d4b0e37d8e sha_match=True
- open_interest/2025-05: rows=145775 sha256=4490a320456fe0f416f5320f9419bd01c65236b877546c30966b287b9c60dea6 sha_match=True
- open_interest/2025-06: rows=143165 sha256=309346d25013e7ccb5ad753d8362ea91354209b9637bca254e99182213b9bdce sha_match=True
- open_interest/2025-07: rows=149325 sha256=09116f78552bbfc3a0cc640e1a44c31a0322f6e2f1018974cc0a9ede18c3a16d sha_match=True
- open_interest/2025-08: rows=150863 sha256=dce8b1320d0b9f7627f649988432e63cc393ffe4a7006c687f94d23f608aa665 sha_match=True
- open_interest/2025-09: rows=149823 sha256=53a5b1cab586fee5f207f51046e525595713b3efd52697e7e8352e67d61c1de3 sha_match=True
- open_interest/2025-10: rows=161213 sha256=5fd20253a69b689591fd987af85a706714788ae75d06912879a95b22258c5fc8 sha_match=True
- open_interest/2025-11: rows=158703 sha256=f3c20d2c8b68339e4194e5984481246235678f52d19139e26c6c8f0f084be2cf sha_match=True
- open_interest/2025-12: rows=165714 sha256=584160f9a23f9dbe64ff248152bca0056831a40765cbb7f619af33c56283a59e sha_match=True
- open_interest/2026-01: rows=167960 sha256=ac9ba48be4bedeac3ac2b7cf8a2defd8f5d334f19c57f7b2ede788212e4d01db sha_match=True
- open_interest/2026-02: rows=153616 sha256=c346cb2a4f333da88da7f2ab93a6540eb435b802144d4e0c803bf2fbbd0307f7 sha_match=True
- open_interest/2026-03: rows=170376 sha256=1855bccbeca65a34573bb35580d32cb5de978fc565a0110699ddd00cd07452b3 sha_match=True
- open_interest/2026-04: rows=169798 sha256=c05681575420102d6da681b6e11d6dec77f239266b2a52d1917b5f2b1b46c237 sha_match=True
- open_interest/2026-05: rows=301758 sha256=ace2357114fa5947f1bc34ecef904e00a7bf61b1a3cc0fc42450a688f89d0e60 sha_match=True
- open_interest/2026-06: rows=307283 sha256=3be5f12eab4bf3a3e611b16f5bf7f6857f9a9bd1216ba7afc8e60fa6291d5075 sha_match=True
- open_interest/2026-07: rows=342269 sha256=da3ffccb4a96159a637320ee7f073db95b92fec4badbaf43947fd2d35b7311f9 sha_match=True
- open_interest/2026-08: rows=364299 sha256=7ca39997d3a3566d69bf0c8ea87de3a065e467cf0bbe002a2b418073b9927fde sha_match=True
- open_interest/2026-09: rows=373659 sha256=7cb39a7d8ff30c51ce9caf0a6c361e9237e36054d11165032fc5b407e80f1f73 sha_match=True
- open_interest/2026-10: rows=401833 sha256=8f12370664f576bacf6ff1bca6fc17655f014a0a200da67823b14d215a7a94b6 sha_match=True
