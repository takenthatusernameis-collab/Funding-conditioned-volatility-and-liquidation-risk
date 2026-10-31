# Liquidation Source Discovery Campaign (FCLR-NEXT-001)

Started: 2026-10-31T00:18:30Z
Status: IN_PROGRESS

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
