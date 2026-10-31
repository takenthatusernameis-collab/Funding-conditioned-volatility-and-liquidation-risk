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
