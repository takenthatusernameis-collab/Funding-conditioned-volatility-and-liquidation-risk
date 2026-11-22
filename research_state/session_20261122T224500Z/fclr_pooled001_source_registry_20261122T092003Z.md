# FCLR-POOLED-001 Source Registry

Session UTC: 20261122T092003Z
Campaign: FCLR-POOLED-001-20261122T040000Z (rank-0, gate-enforced)
Source: ironflow_bulk on-disk data cache (research_state/data_cache/ironflow_bulk/)
Sha256: asserted from .parquet.sha256 sidecars before reading; caches not modified.

## Summary

- candles_1h: 18 monthly parquet files, 3,283,274 rows, max_coins=799
  Schema: timestamp, market, coin, dex, market_class, open, high, low, close, volume, trades
- funding: 18 monthly parquet files, 3,753,147 rows, max_coins=494
  Schema: timestamp, market, coin, dex, funding_rate, premium
- open_interest: 18 monthly parquet files, 3,653,015 rows, max_coins=553
  Schema: timestamp, market, coin, dex, mark_price, oracle_price, open_interest, open_interest_usd
- liquidations: 18 monthly parquet files, 2,526,739 rows, max_coins=n/a
  Schema: timestamp, market, issuer, wallet, position_side, size, notional_usd, avg_price, fills, block, tx_hash

## File-level registry

| dataset | month | path | sha256 | rows |
|---------|-------|------|--------|------|
| candles_1h | 2025-05 | research_state/data_cache/ironflow_bulk/candles_1h/2025-05.parquet | 9bd24cf774076f753f9692a663837f815853f755890434ba9a08e73600a86aef | 35,550 |
| candles_1h | 2025-06 | research_state/data_cache/ironflow_bulk/candles_1h/2025-06.parquet | f8eef410c8e21881e8511fec10a1a032b5ad37b21f94deef96b6f2f8cdc8131b | 154,237 |
| candles_1h | 2025-07 | research_state/data_cache/ironflow_bulk/candles_1h/2025-07.parquet | 466c6ebc277045f231cbe18583d3aa41488bd27aed57a5effd118712b603d647 | 156,492 |
| candles_1h | 2025-08 | research_state/data_cache/ironflow_bulk/candles_1h/2025-08.parquet | bb5f2c85f874688f6fc154c576d0cc483445fa81bfcb28aa4024119aea248229 | 154,531 |
| candles_1h | 2025-09 | research_state/data_cache/ironflow_bulk/candles_1h/2025-09.parquet | ab22becbad69206cc01b4279604fabaaafb870bc54b2998c0bc243247db5f0f1 | 155,796 |
| candles_1h | 2025-10 | research_state/data_cache/ironflow_bulk/candles_1h/2025-10.parquet | f30ee1b41fe0c7405c4f5f0dba12adce2d19bdaa60f96bc31d1c1cc30395fad1 | 173,905 |
| candles_1h | 2026-01 | research_state/data_cache/ironflow_bulk/candles_1h/2026-01.parquet | a42260c697b59853b9321061ee03e146ac461708ead63a10c249839fca05b6ed | 211,494 |
| candles_1h | 2026-02 | research_state/data_cache/ironflow_bulk/candles_1h/2026-02.parquet | 94e1bbbd3791b5b9770c5d9708974386aa1cb854c5e18d4eb25ca809113fe091 | 216,575 |
| candles_1h | 2026-03 | research_state/data_cache/ironflow_bulk/candles_1h/2026-03.parquet | 6a34df24c25e4ecc147bc70e8d72df811df9ca1542cab4c523320f62616adf5b | 248,859 |
| candles_1h | 2026-04 | research_state/data_cache/ironflow_bulk/candles_1h/2026-04.parquet | 6cab3cc3d6d3d8418d0c0dbbcff85c76d504008357a1695b39e12c57e2578180 | 246,842 |
| candles_1h | 2026-05 | research_state/data_cache/ironflow_bulk/candles_1h/2026-05.parquet | f8f0e158bdd4b47a3a522115297364194c56ef0ab5953b5f70b4f524ffb33a82 | 259,642 |
| candles_1h | 2026-06 | research_state/data_cache/ironflow_bulk/candles_1h/2026-06.parquet | 1aabd11fdad5eadb7db7c7779c859ec6294d7c69e97b1f0782175b035036d4af | 244,727 |
| candles_1h | 2026-07 | research_state/data_cache/ironflow_bulk/candles_1h/2026-07.parquet | 7b90e976c56a325875c86aeb8b5558a182d264c1e89e64d73356afafcda417b7 | 234,715 |
| candles_1h | 2026-08 | research_state/data_cache/ironflow_bulk/candles_1h/2026-08.parquet | 3a48dfe803ffe46a30e598952d5e1c25557c7a6eb6bb7391c2cd2d5adea68759 | 253,467 |
| candles_1h | 2026-09 | research_state/data_cache/ironflow_bulk/candles_1h/2026-09.parquet | 36ef6d8a476a526c2f8c12c3376405b7fab48939467d3bc40c0c673078541e59 | 259,199 |
| candles_1h | 2026-10 | research_state/data_cache/ironflow_bulk/candles_1h/2026-10.parquet | 26f359c5c930e02020298faeeda04025d017b283610b9a2c97660385dc199324 | 277,243 |
| funding | 2025-05 | research_state/data_cache/ironflow_bulk/funding/2025-05.parquet | 26005d5d1bfd0719e8eeb5e4d4c0750dadfa63d0c8161ad476a6a55170455058 | 145,771 |
| funding | 2025-06 | research_state/data_cache/ironflow_bulk/funding/2025-06.parquet | bb6b8878b6491961fbfbcb168b9906a0cc8b4c82586357f42424cac11733c729 | 143,163 |
| funding | 2025-07 | research_state/data_cache/ironflow_bulk/funding/2025-07.parquet | ad9d01aa425af412fce534c83c7a4f3ee5997dc3f533a07681b2ad4e679522ee | 149,324 |
| funding | 2025-08 | research_state/data_cache/ironflow_bulk/funding/2025-08.parquet | 2cb155ad80289355fc96344316309fd48a4cccbef062a3c1e508cdb9f4152d27 | 150,859 |
| funding | 2025-09 | research_state/data_cache/ironflow_bulk/funding/2025-09.parquet | f06b49dd307a7922a3e429bd9a06e0ddb4febe0d2556d7f232ce6a040f9db205 | 149,815 |
| funding | 2025-10 | research_state/data_cache/ironflow_bulk/funding/2025-10.parquet | 51c9ebd47a36afc31ae7907b539c1256e456132671f133be488ef3596c9e0a3d | 161,650 |
| funding | 2026-01 | research_state/data_cache/ironflow_bulk/funding/2026-01.parquet | 349a01e2f6518f63f18a8f7b55b168f563ee68faa16176b1f5e817edebea06e1 | 212,211 |
| funding | 2026-02 | research_state/data_cache/ironflow_bulk/funding/2026-02.parquet | 9fc4b300ba79dd79afe52823c805752d463b119e56afb9b2dc2732dbb67ed789 | 221,707 |
| funding | 2026-03 | research_state/data_cache/ironflow_bulk/funding/2026-03.parquet | cc8dc6e57e6d512605f48d0f19039871829318c3a0632ed995b769d957490f2a | 258,164 |
| funding | 2026-04 | research_state/data_cache/ironflow_bulk/funding/2026-04.parquet | 008ca1c6864e5a48de61133a8ea4ddb8123be0db9cc291be1a4368e57710998a | 261,864 |
| funding | 2026-05 | research_state/data_cache/ironflow_bulk/funding/2026-05.parquet | 4340ecd686296a7b785ffb77570bd7e07254cc600fea7bb321721d386b7c57c0 | 283,853 |
| funding | 2026-06 | research_state/data_cache/ironflow_bulk/funding/2026-06.parquet | 467131e7320a3d568d289d6d10fcee3f4a0e1dde13b8a73bb04977035ab01678 | 286,045 |
| funding | 2026-07 | research_state/data_cache/ironflow_bulk/funding/2026-07.parquet | 98860209990f26f30786ffb4d8f21cf97002a7035e71a147c915d7af35da23df | 308,381 |
| funding | 2026-08 | research_state/data_cache/ironflow_bulk/funding/2026-08.parquet | c067fcca81a1b6a5aaa0d636de16b99804d7de683ef90cde8ecd5c176db1bff0 | 325,975 |
| funding | 2026-09 | research_state/data_cache/ironflow_bulk/funding/2026-09.parquet | d8e43faa444e64c263a078b855d8c1edb9ef73fba5b63ef908fc5aa9314ec7bc | 334,762 |
| funding | 2026-10 | research_state/data_cache/ironflow_bulk/funding/2026-10.parquet | b081c40f350d3982d1279cd7d019a2d645aabd548cd30358a90e77d4b0e37d8e | 359,603 |
| open_interest | 2025-05 | research_state/data_cache/ironflow_bulk/open_interest/2025-05.parquet | 4490a320456fe0f416f5320f9419bd01c65236b877546c30966b287b9c60dea6 | 145,775 |
| open_interest | 2025-06 | research_state/data_cache/ironflow_bulk/open_interest/2025-06.parquet | 309346d25013e7ccb5ad753d8362ea91354209b9637bca254e99182213b9bdce | 143,165 |
| open_interest | 2025-07 | research_state/data_cache/ironflow_bulk/open_interest/2025-07.parquet | 09116f78552bbfc3a0cc640e1a44c31a0322f6e2f1018974cc0a9ede18c3a16d | 149,325 |
| open_interest | 2025-08 | research_state/data_cache/ironflow_bulk/open_interest/2025-08.parquet | dce8b1320d0b9f7627f649988432e63cc393ffe4a7006c687f94d23f608aa665 | 150,863 |
| open_interest | 2025-09 | research_state/data_cache/ironflow_bulk/open_interest/2025-09.parquet | 53a5b1cab586fee5f207f51046e525595713b3efd52697e7e8352e67d61c1de3 | 149,823 |
| open_interest | 2025-10 | research_state/data_cache/ironflow_bulk/open_interest/2025-10.parquet | 5fd20253a69b689591fd987af85a706714788ae75d06912879a95b22258c5fc8 | 161,213 |
| open_interest | 2026-01 | research_state/data_cache/ironflow_bulk/open_interest/2026-01.parquet | ac9ba48be4bedeac3ac2b7cf8a2defd8f5d334f19c57f7b2ede788212e4d01db | 167,960 |
| open_interest | 2026-02 | research_state/data_cache/ironflow_bulk/open_interest/2026-02.parquet | c346cb2a4f333da88da7f2ab93a6540eb435b802144d4e0c803bf2fbbd0307f7 | 153,616 |
| open_interest | 2026-03 | research_state/data_cache/ironflow_bulk/open_interest/2026-03.parquet | 1855bccbeca65a34573bb35580d32cb5de978fc565a0110699ddd00cd07452b3 | 170,376 |
| open_interest | 2026-04 | research_state/data_cache/ironflow_bulk/open_interest/2026-04.parquet | c05681575420102d6da681b6e11d6dec77f239266b2a52d1917b5f2b1b46c237 | 169,798 |
| open_interest | 2026-05 | research_state/data_cache/ironflow_bulk/open_interest/2026-05.parquet | ace2357114fa5947f1bc34ecef904e00a7bf61b1a3cc0fc42450a688f89d0e60 | 301,758 |
| open_interest | 2026-06 | research_state/data_cache/ironflow_bulk/open_interest/2026-06.parquet | 3be5f12eab4bf3a3e611b16f5bf7f6857f9a9bd1216ba7afc8e60fa6291d5075 | 307,283 |
| open_interest | 2026-07 | research_state/data_cache/ironflow_bulk/open_interest/2026-07.parquet | da3ffccb4a96159a637320ee7f073db95b92fec4badbaf43947fd2d35b7311f9 | 342,269 |
| open_interest | 2026-08 | research_state/data_cache/ironflow_bulk/open_interest/2026-08.parquet | 7ca39997d3a3566d69bf0c8ea87de3a065e467cf0bbe002a2b418073b9927fde | 364,299 |
| open_interest | 2026-09 | research_state/data_cache/ironflow_bulk/open_interest/2026-09.parquet | 7cb39a7d8ff30c51ce9caf0a6c361e9237e36054d11165032fc5b407e80f1f73 | 373,659 |
| open_interest | 2026-10 | research_state/data_cache/ironflow_bulk/open_interest/2026-10.parquet | 8f12370664f576bacf6ff1bca6fc17655f014a0a200da67823b14d215a7a94b6 | 401,833 |
| liquidations | 2025-05 | research_state/data_cache/ironflow_bulk/liquidations/2025-05.parquet | 840bc18b1ec0df9c559e0bf2bff042c36642308f038268922c3dff6c8edb99f3 | 15,621 |
| liquidations | 2025-06 | research_state/data_cache/ironflow_bulk/liquidations/2025-06.parquet | 737908e4568ca903370e6bfc8bf9792d70102ddafa0161b48598dc3dd1b2e338 | 60,589 |
| liquidations | 2025-07 | research_state/data_cache/ironflow_bulk/liquidations/2025-07.parquet | 4ad6e10a5e34c329040a92d05942c8f0862ff97353120dba9efeed76429b4f22 | 104,176 |
| liquidations | 2025-08 | research_state/data_cache/ironflow_bulk/liquidations/2025-08.parquet | b21bd8ce70fc9f8ef131afadef2185bcdf473e5df1f283f80e9dab5901ba8aac | 131,150 |
| liquidations | 2025-09 | research_state/data_cache/ironflow_bulk/liquidations/2025-09.parquet | 63bfe5cc8f57176a7f0e5a91d990c224bbddb9e28854b6535b4e8cd2e72cb2bc | 111,148 |
| liquidations | 2025-10 | research_state/data_cache/ironflow_bulk/liquidations/2025-10.parquet | e5382066e77c383e0abe0b5f337242f11997e33e57b674f669465aa7915adca8 | 256,803 |
| liquidations | 2026-01 | research_state/data_cache/ironflow_bulk/liquidations/2026-01.parquet | 489f5d9d747c3d58f0af515c925c9d2625eafbfbc33570e1c8ba4c8ca7ce7248 | 154,506 |
| liquidations | 2026-02 | research_state/data_cache/ironflow_bulk/liquidations/2026-02.parquet | 8e27c2e1ca90baebbc768ea74a105f4547f85d2a85c81b67927f9c32d02ec18f | 173,549 |
| liquidations | 2026-03 | research_state/data_cache/ironflow_bulk/liquidations/2026-03.parquet | b2240b9ecc40ca27c34a4f3f18fd8b17f18f4dd3e9f83c91ca7040ecd2240e6d | 145,298 |
| liquidations | 2026-04 | research_state/data_cache/ironflow_bulk/liquidations/2026-04.parquet | 3d84969be4e65fea8abbc9c8b5950160e835c39ed0906d155cbefe46d23fd9b4 | 108,755 |
| liquidations | 2026-05 | research_state/data_cache/ironflow_bulk/liquidations/2026-05.parquet | 3ebbb27119bb0912f180a6c4ea8c70c5477706a21535f4452a3e0d1e2fdaa300 | 128,616 |
| liquidations | 2026-06 | research_state/data_cache/ironflow_bulk/liquidations/2026-06.parquet | 9e8e4469ff14b0f1c03fd4ce8dad5acfba41588bd8d2c5e6ee2ef1a1e5a02d1b | 255,078 |
| liquidations | 2026-07 | research_state/data_cache/ironflow_bulk/liquidations/2026-07.parquet | ba2699261986c13dc023d95a987ed01ee9115f08fc435161ad06f5addb6c769c | 218,529 |
| liquidations | 2026-08 | research_state/data_cache/ironflow_bulk/liquidations/2026-08.parquet | 2e1089f1072bbafb05da82465ff36e5ca321dd88bb8b37fccd366cb3eda5913c | 215,835 |
| liquidations | 2026-09 | research_state/data_cache/ironflow_bulk/liquidations/2026-09.parquet | 35430b107244388721be20026d00b035b2df389035ac790ced0c6c37c4bb502e | 195,244 |
| liquidations | 2026-10 | research_state/data_cache/ironflow_bulk/liquidations/2026-10.parquet | 182e0e1dfea6c28955dde3da1f14c4473e16fbe6d4577fa1aa6bacad175a2c15 | 251,842 |