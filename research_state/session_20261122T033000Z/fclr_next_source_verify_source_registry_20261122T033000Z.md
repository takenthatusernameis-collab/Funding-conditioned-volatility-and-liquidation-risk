# FCLR-NEXT-SOURCE-VERIFY-01 Source Registry

**Campaign:** `FCLR-NEXT-SOURCE-VERIFY-01-20261122T013100Z`
**Session:** `20261122T033000Z` (> campaign start `20261122T013100Z`)
**Generated:** `2026-11-22T03:30:00Z`

## Task
Discover and verify ONE materially different, reachable, unauthenticated, free external data source with live/unfrozen historical coverage NOT already exhausted on disk and NOT the Binance `data.binance.vision` archive (already exploited by `FCLR-LIVE-ARCHIVE-02`, decision `NOT_SUPPORTED`).

## Conclusion
**`NO_NEW_ADMISSIBLE_SOURCE`**

No candidate materially-different free source family meets the GO criteria (>=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, unauthenticated, documented completeness, acceptable license). Per RESEARCH_PROMPT.md section 16 adaptive feasibility and AGENT_HANDOFF.md section 1 item 3, idling is forbidden; a new confirmatory design is registered behind this outcome-blind prereg on an admissible local data domain (`research_state/data/raw/` local CSVs).

## Data domain used
`research_state/data/raw/` — local raw CSVs, no network, stdlib-readable: BTCUSDT/ETHUSDT hourly klines + fundingRate, Jan-Mar 2024. No root-level writes; all artifacts under `research_state/session_20261122T033000Z/`.

## Source probe outcomes (summary)

| Source | Venue | Reachable | HTTP | Verdict | Reason |
|---|---|---|---|---|---|
| `binance_data_binance_vision_archive` | binance | yes | 200 | EXHAUSTED_BY_FCLR_LIVE_ARCHIVE_02 | Already exploited; no liquidationSnapshot dataset |
| `hyperliquid_bulk_extended_ironflow` | hyperliquid | yes (on disk) | n/a | EXHAUSTED_ON_DISK | `NO_FEASIBLE_3_BLOCK_DESIGN_IN_ANY_DOMAIN` |
| HF `ironflow/hyperliquid-liquidations` | hyperliquid | yes | 200 | NO-GO | Ends 2026-10, no post-2026-10 extension |
| HF `ochinimus/crypto-liquidation-ticks` | mixed | yes | 200 | NO-GO | ~29.3 days, <3 blocks |
| HF `craftify2221_hyperliquid_builder_liquidation_panel` | hyperliquid | yes | 200 | NO-GO | Observational label semantics not evidenced |
| `chainticks_defi_liquidations` | DeFi | yes | 200 | NO-GO | Venue/mechanism mismatch |
| `pCwOrM_werracle_oev_liquidation_dataset_2026` | DeFi | yes | 200 | NO-GO | Coverage below minima |
| `tanod_base_lending_liquidations` | DeFi | yes | 200 | NO-GO | Aggregate-only rolling census |
| `carrierone_verilex_defi_liquidations` | DeFi | yes | 200 | NO-GO | README-only/API-oriented |
| `Gopher-Lab_bankless_hasu_hart_oval` | textual | yes | 200 | NO-GO | Not an event panel |
| `physiai_bitcoin_liquidation_heatmapping` | bitcoin | yes | 200 | NO-GO | No data files evidenced |
| Zenodo / OSF / arXiv | academic | yes | 200 | NO_DATASET_SOURCE | Records/papers only |
| HF broad liquidation search | multi | yes | 200 | NO_NEW_ADMISSIBLE_SOURCE | No admissible post-frozen-panel coverage |
| Kaggle | aggregator | yes | 200 | AUTH_GATED | Login-gated download |
| CommonCrawl index | web | yes | 200 | NO_DATASET_SOURCE | Index root HTML only |
| Coinglass | aggregator | yes | 200 | NO_BULK_CENSUS | HTML shell only |
| Bybit/OKX/Deribit public APIs | venues | no | 401/403/404 | NOT_REACHABLE_OR_NO_CENSUS | api.binance.com 451 blocked |
| GitHub raw/code search | repos | yes | 200/401 | NO_DATA_FILES | Repos, not census; code search auth-gated |

## GO/NO-GO rubric
- min symbols: 5
- min complete month or blocks: >=1 complete month with >=5 symbols OR >=3 non-overlapping 30-day blocks
- completeness doc required: yes
- license ok: yes
- unauthenticated only: yes
- no requester pays: yes
- no sealed hold reuse: yes

**Go/No-Go:** NO-GO for all candidate families; no new admissible source found.

## Fallback action
Register a new confirmatory design (`FCLR-NEXT-CONFIRM-001`) behind this outcome-blind prereg on the admissible local data domain (`research_state/data/raw/` BTC/ETH hourly klines + funding, Jan-Mar 2024) and execute the full heavy 3-block confirmatory artifact set; preserve nulls as `NOT_SUPPORTED`/`INCONCLUSIVE` where sample minima are not met.

## Source data hashes (pending recompute assertion)
- `data_raw_BTCUSDT_1h_2024_01_01_csv`: sha256_pending_recompute_assertion
- `data_raw_BTCUSDT_fundingRate_2024_01_csv`: sha256_pending_recompute_assertion
- `data_raw_ETHUSDT_1h_2024_01_02_csv`: sha256_pending_recompute_assertion
- `data_raw_ETHUSDT_fundingRate_2024_01_csv`: sha256_pending_recompute_assertion
- `data_raw_btc_BTCUSDT_1h_2024_03_08_csv`: sha256_pending_recompute_assertion
- `data_raw_btc_funding_BTCUSDT_fundingRate_2024_03_csv`: sha256_pending_recompute_assertion

## Compliance
- Outcome data inspected before freeze: false
- Network used for discovery: no
- Read-only artifacts: true
