# BLOCKER EVIDENCE - LIQUIDATION_SOURCE_REOPEN_HEAVY-001
**TIMESTAMP:** 20261103T070800Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**CAMPAIGN:** LIQUIDATION_SOURCE_REOPEN_HEAVY-001

## SUMMARY
All REVIEW_REQUIRED alternative liquidation sources deep-reviewed. No new admissible unauthenticated source passes full FCLR rubric.

## IRONFLOW STATUS (Track A baseline)
- monitor_ironflow_liquidations.py --quick: data_through=2026-10, consec_absent=3 (2026-11,12,2027-01,02 all 404), resume_trigger_met=false
- Cached through 2026-10 intact (18 month pairs, content_hash_complete=True)
- FCLR-010 (Hyperliquid census 2025-11..2026-10) COMPLETE, gate PASSED, sealed

## DEEP REVIEW RESULTS
All candidates tested unauthenticated only. Full rubric checks performed.
- NO-GO: hyperliquid_public_api_info (405 GET), github_raw_search_hyperliquid_liquidations (404), github_api_repos (404), github_code_search_unauth (401), theblock_research, glassnode_public_docs (403)
- REVIEW_REQUIRED deep-tested: huggingface_other_datasets (ironflow/hyperliquid-liquidations exists - this IS the known source, already FCLR-010), huggingface_liquidation_search_broad, zenodo, osf, arxiv, data_commoncrawl, kaggle (metadata/auth-gated), github_repos_search, coinglass_public (auth required per API response), hyblock_public, coinank_public, paradigm_research, coinglass_public_liquidations, laevitas_public (site exists, no obvious unauthenticated historical liquidation census parquet/API), hyblock/coinank/paradigm variants
- Tested endpoints: Hyperliquid API info (POST works for market metadata but no liquidation census), Bybit public dirs 404, OKX instruments 200 (metadata only), Deribit instruments 200 (metadata), Coinglass API returns auth error, Tardis 404, CoinAPI 401, Glassnode 403, cryptodatadownload.com has files but liquidation snapshots not obvious unauthenticated census matching FCLR-010 schema, Binance vision no liquidationSnapshot dir

**Verdict:** NO NEW GO SOURCE FOUND. Structural blocker remains.

## RESUME TRIGGERS (unchanged)
- Ironflow: GET https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/YYYY-MM.parquet and /data/fills/YYYY-MM.parquet return 200 for YYYY-MM >= 2026-11
- OR new source passes GO: >=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage/license OK, unauthenticated only, schema compatible with frozen FCLR-010

## EVIDENCE ARTIFACTS
- research_state/data_source_registry_alt_hunt.json (refreshed)
- research_state/alt_source_scan_20261103T070646Z.json
- research_state/alt_source_deep_review_20261103T070705Z.md (full rubric evidence)
- research_state/ironflow_probe_20261103T070739Z.json (keep-alive)

## TESTS
python -m unittest discover -s tests -v: 111/111 PASS (maintained)
