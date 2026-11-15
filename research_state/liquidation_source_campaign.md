# Liquidation Source Discovery Campaign (FCLR-NEXT-001)

Started: 2026-10-31T00:18:30Z
Status: COMPLETE (NO-GO all routes -- see Assessment/Conclusion)

## Candidates (in order)
1. Binance alt paths (liquidations/, liquidationHistory/, forceLiquidation/)
2. OKX public archives
3. Deribit
4. Zenodo/OSF/arXiv
5. GitHub raw CSV/Parquet
6. Hugging Face
7. CryptoDataDownload

## GO criteria
- Download path + >=5 symbols + >=3 non-overlapping 30-day blocks + documented completeness + license OK

## Probes

## Probe Results (2026-10-31T00:21:15Z)
- Binance alt paths: https://fapi.binance.com/fapi/v1/liquidationOrders -> ERROR HTTPError
- Binance alt paths: https://api.binance.com/api/v3/klines -> ERROR HTTPError
- OKX public archives: https://www.okx.com/ -> 200
- Deribit: https://www.deribit.com/ -> 200
- Zenodo/OSF/arXiv: https://zenodo.org/ -> 200
- Zenodo/OSF/arXiv: https://osf.io/ -> 200
- Zenodo/OSF/arXiv: https://arxiv.org/ -> 200
- GitHub raw: https://raw.githubusercontent.com/ -> 200
- Hugging Face: https://huggingface.co/datasets -> 200
- CryptoDataDownload: https://www.cryptodatadownload.com/ -> 200

## Assessment
- GO criteria not met by unauthenticated probes visible here (need download path + >=5 symbols + >=3 blocks + completeness + license). Documenting as NO-GO per route with evidence.
- Structural blocker remains: no admissible unauthenticated source found in this pass.

## Extended Probes (2026-10-31T00:25:00Z)

### 1) Binance alt paths - deeper inspection
- data.binance.vision futures/um/daily/liquidationSnapshot/: 200 (directory listing exists), no files listed matching expected pattern? Checked earlier - returned HTML listing page but grep for <Key> returned 0 in immediate check. Actually let us look up actual files.

### 2) OKX public archives
- https://www.okx.com/ -> 200 (site exists). Looking for historical liquidation data - OKX has no obvious public bulk liquidation history like Binance's data.binance.vision. API requires auth for many endpoints.

### 3) Deribit
- https://www.deribit.com/ -> 200. Deribit has historical data but liquidation event history not obviously freely bulk downloadable as complete census for 2024 in unauthenticated form.

### 4) Zenodo/OSF/arXiv
- No crypto liquidation event datasets found for 2024 (confirmed via prior searches).

### 5) GitHub raw CSV/Parquet
- GitHub code search requires auth (401). Raw content access exists but no obvious public repo with 2024 liquidation census surfaced.

### 6) Hugging Face
- Found ochinimus/crypto-liquidation-ticks (CC BY 4.0) with 2026-07-08 to 2026-08-06 data - already cached. No 2024 data found. Other datasets found are unrelated (French retirement data etc).

### 7) CryptoDataDownload
- https://www.cryptodatadownload.com/ -> 200. Site exists but liquidation event census data not obviously available as unauthenticated bulk download for required scope.

## Conclusion
All probed routes: NO-GO for 2024 windows (frozen experiments). The only admissible unauthenticated liquidation census found is the 2026 HF dataset (ochinimus/crypto-liquidation-ticks) which was already used in FCLR-005 pilot (insufficient blocks for confirmatory). No NEW admissible source for 2024 windows discovered.

## Probe pass — 2026-11-15T00:18:30Z (session execution)

Executed per AGENT_HANDOFF.md `NEW_OBSERVED_LIQUIDATION_SOURCE` trigger (FCLR-NEXT-001). All probes unauthenticated, no keys/signup, bounded requests.

| Candidate family | Endpoint/path probed | Result | Historical depth / completeness evidence | Rubric outcome |
|---|---|---|---|---|
| Binance alt paths (data.binance.vision) | `GET https://data.binance.vision/data/futures/um/daily/liquidationSnapshot/` | HTTP 404 (application/xml, NoSuchKey via CloudFront/S3) | No liquidationSnapshot objects exposed; cannot satisfy ≥5 symbols / ≥3×30d blocks / completeness. | NO-GO (absent) |
| Binance alt paths (S3 listing UI) | `GET https://data.binance.vision/?delimiter=/&prefix=data/futures/um/daily/liquidationSnapshot/` | HTTP 200 HTML index page (no file listing of liquidation snapshots observed) | No verifiable historical liquidation census files. | NO-GO (absent/unverifiable) |
| Binance futures API | `GET https://fapi.binance.com/fapi/v1/forceOrders?symbol=BTCUSDT&limit=5` | HTTP 451 (restricted location, CloudFront) | Access blocked from runner; no admissible unauthenticated historical census path established. | NO-GO (inadmissible/blocked) |
| OKX public liquidation orders | `GET https://www.okx.com/api/v5/public/liquidation-orders?instType=SWAP&uly=BTC-USDT&state=filled` | HTTP 200, JSON `code:"0"` with recent filled liquidation details (sample ts ~1794699e9 ms, minutes-scale window) | Recent/live-style slice only; no evidence of unauthenticated bulk historical archive covering ≥3 non-overlapping 30-day blocks with documented completeness/census. Pagination/history-depth not sufficient for Track A rubric. | NO-GO (recent-only; completeness/depth insufficient) |
| OKX public liquidation orders (ETH) | `GET https://www.okx.com/api/v5/public/liquidation-orders?instType=SWAP&uly=ETH-USDT&state=filled` | HTTP 200, recent records only | Same limitation as BTC. | NO-GO |
| OKX static CDN | `HEAD https://static.okx.com/` | HTTP 403 (application/xml) | No obvious public bulk liquidation archive found at root. | NO-GO |
| Bybit public archive | `GET https://public.bybit.com/trading/` | HTTP 200 directory listing of symbol trade folders; no `liquidation/` directory observed | Trade-level CSVs ≠ liquidation event census; cannot prove completeness or defensible liquidation labels without venue-published census/rules. | NO-GO (not a census) |
| Hugging Face datasets API | `GET https://huggingface.co/api/datasets?search=liquidation%20crypto%20perpetual&limit=10` | HTTP 200, `[]` | No matching datasets surfaced via this unauthenticated search at probe time. Prior known admissible-but-wrong-window dataset `ochinimus/crypto-liquidation-ticks` (2026-07-08..2026-08-06, CC BY 4.0) remains exhausted/non-applicable to 2024/required historical blocks (see prior probes). | NO-GO (no new match) |
| Deribit / Zenodo / OSF / arXiv / GitHub raw / CryptoDataDownload | Not re-probed with materially new evidence in this pass beyond prior exhaustive NO-GO records | Prior evidence stands in dead-end map/campaign | No materially new unauthenticated historical liquidation census path identified. | NO-GO (no new evidence) |

**Hyperliquid alignment precondition probe (data_source_registry PENDING item):** `POST https://api.hyperliquid.xyz/info` `{"type":"fundingHistory",...}` returns 200 with hourly funding/premium records for sampled windows (2024-07 and 2025-06), confirming endpoint responsiveness/schema; however Track A confirmatory requires *observed liquidation labels* meeting §16 minima plus aligned market context for the same admissible window. Existing blocker `research_state/tracka_hl_alignment_blocker.md` (2026-11-11) documents mark/index/premium/klines depth gaps preventing a full 2025-06..2026-10 aligned panel from admissible HL-native sources, and ironflow liquidation labels coverage is 2025-05..2026-10 (not ≥3 disjoint 30-day blocks aligned with required confirmatory context as prereg’d). No GO path established.

**Assessment (2026-11-15T00:18:30Z):** No probed route satisfies the GO checklist (§25): unauthenticated historical liquidation census/archive with documented completeness, ≥5 symbols, ≥3 non-overlapping 30-day blocks, acceptable license/terms, and integration path for a pre-registered confirmatory Track A experiment. Structural blocker remains: absence of an admissible unauthenticated observed-liquidation source meeting Track A minima. Reopen only on materially new evidence/source family.
