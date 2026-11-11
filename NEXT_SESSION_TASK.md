# NEXT_SESSION_TASK — Single Durable Handoff (Initial Task Message)

**Timestamp (UTC):** 2026-11-11T05:23:17Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Program status:** `CONCLUDED_UNDER_CONSTRAINTS` for all three tracks (evidence-backed). This file is the **single durable handoff** and authoritative initial task message. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, and `HANDOFF_NEXT_SESSION.md` are pointers only.

## Initial message for the next agentic work session (execute first)

**SINGULAR NEXT TASK: `SOURCE_UNBLOCK_CAMPAIGN` — remove the Track A structural block so heavy research can continue.**

The repo name prioritizes liquidation risk. Track A (observed liquidations) is **STRUCTURALLY_BLOCKED**: Binance `liquidationSnapshot` 404 (UM/CM, daily/monthly), Binance `fapi forceOrders` HTTP 451 restricted, Bybit/OKX/Deribit no unauthenticated complete liquidation census, HF/Zenodo/GitHub exhausted for frozen 2024 confirmatory windows; the only previously admissible source (HF `ochinimus/crypto-liquidation-ticks`, CC BY 4.0) covers 2026-07-08..2026-08-06 only (FCLR-005 pilot: exploratory_only, no incremental skill, <3 non-overlapping 30-day blocks). Track C/H1 **NOT_SUPPORTED** on all claim-worthy panels (FCLR-003/008/009/012-V/013/014); Track B **NOT_SUPPORTED** (TB1 degenerate; TB2 forecast gate NOT_MET: Log Loss B1=0.292447→C2=0.287540 +1.68% < 2% floor, 95% CI crosses zero p=0.488, Holm fails, 2 test blocks <3). All local routes exhausted — the only path to significant heavy progress is a **new admissible unauthenticated data source**.

Do not poll, relitigate concluded tracks, threshold-shop, reuse sealed holdouts, fabricate data/provenance, conflate Track A/B/C, or produce status-only output. If the campaign finds no new admissible source, stop cleanly with evidence: `NONE`.

## State this session inherits (evidence-backed)

- **Phase 1 enumeration COMPLETE (live):** `python scripts/hunt_alternative_liquidation_sources.py` ran live at 20261111T044041Z, wrote `research_state/alt_source_scan_latest.json` and `research_state/hf_search_cache.json` (source=live, 9 queries, 0 errors). Do NOT re-run HF enumeration within the 24h cache TTL — that is polling, not progress.
- **Deep review COMPLETE (20261111T044105Z):** 14 venue/archive URLs probed via GET; NO NEW GO sources from venue archives (Binance liquidationSnapshot 404, Bybit spot/linear 404, OKX instruments 200 but no liquidation census, Deribit instruments 200, CoinAPI 401 auth-gated, Coinglass 30001 API key missing, Kaiko demo DNS fail, Glassnode 403, Laevitas/CryptoDataDownload HTML only). Reuse `research_state/url_probe_cache.json` (6h TTL); do not re-GET cached URLs within TTL.
- **NEW unblock candidate identified (NOT yet rubric-verified):** HF `ironflow/hyperliquid-liquidations` (author `ironflow`, commit `65bad6c39c63ee24eae920753f05303020e549fa`). README documents: CC BY 4.0; unauthenticated HF bulk parquet; coverage 25 May 2025–31 Oct 2026; 2,849,452 liquidated positions across 468 markets and 506,975 wallets, $58.7B notional; monthly `data/events/YYYY-MM.parquet` + `data/fills/YYYY-MM.parquet`; schema `timestamp(ms UTC), market, issuer, wallet, position_side(long/short), size, notional_usd, avg_price, fills, block, tx_hash`; completeness documented (Ironflow nodes, replayed from Hyperliquid S3 archive hour-by-hour, sampled events match `userFillsByTime` exactly).
- **HEAD probe (2026-11-11T05:25:36Z) confirms unauthenticated access:** `https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/2025-10.parquet` → HTTP 302 to signed HF CDN, `x-linked-size: 9430899`, `x-linked-etag: "e5382066e77c383e0abe0b5f337242f11997e33e57b674f669465aa7915adca8"`, `x-xet-hash: 104aecc4586f4cb05473fd303e37c1b63588e94a8198136e0b364be35e3cb025`, `accept-ranges: bytes`, `x-hf-warning: unauthenticated` (rate-limit warning only, not a block). No HF_TOKEN/signup/payment required.
- Other live-discovered HF candidates still unprobed: `Gopher-Lab/bankless_Hasu__Hart_on_Oval__The_Recapturing_of_Billions_in_DeFi_Liquidations`, `french-open-data_caracteristiques-des-retraites-age-de-liquidation`, `french-open-data_caracteristiques-des-retraites-conditions-de-liquidation`, `tanod_base-lending-liquidations`, `PhysiAI_Bitcoin-Liquidation-Heatmapping(-5m/-1h)`, `carrierone_verilex-defi-liquidations` (x402 requester-pays → NO-GO), `Chainticks_defi-liquidations` (DeFi, not perp futures → likely NO-GO).
- Environment green: track-a scope registry 127/127 pass, 161/161 funding-rate files provenance verified (unmapped_count=0), targeted tests 35/35 green.

## Focus campaign — SOURCE_UNBLOCK_CAMPAIGN (heavy, bounded, executable)

**Phase 1 — Enumerate (bounded, cached):** ALREADY DONE this session (live). Reuse `research_state/hf_search_cache.json` (24h TTL) + `alt_source_scan_latest.json`. Do not re-enumerate HF search within TTL.

**Phase 2 — Probe + evidence (unauthenticated only) — THIS IS THE PENDING HEAVY WORK:**
1. **Primary target:** `ironflow/hyperliquid-liquidations`. Download + inspect at least one parquet (e.g. `data/events/2025-10.parquet`, ~9MB) unauthenticated; empirically verify schema fields, timestamp range, distinct `market`/symbol count (≥5 per complete month), completeness of a full calendar month, and that rows are actual liquidation fills (not a capped sample). Record URL, access date, hash/ETag (`x-linked-etag` / `x-xet-hash`), license (CC BY 4.0), requester-pays absence.
2. **Secondary targets:** probe remaining unprobed live-discovered HF candidates (Gopher-Lab, french-open-data x2, tanod, PhysiAI x3) unauthenticated; score each against the rubric; document NO-GO with evidence for any failure (esp. verilex = requester-pays NO-GO; DeFi/chainticks/PhysiAI = wrong scope → NO-GO for Track A).
3. Persist per-URL probe evidence in `research_state/url_probe_cache.json` (shared, deduped, 6h TTL) so blocked sessions never re-GET the same URL.
4. Never use payment, signup, API key, manual download, credentials, or bypassed access.

**Phase 3 — Rubric (GO requires ALL):**
- ≥5 instruments with usable coverage, AND (≥1 complete month with ≥5 symbols OR ≥3 non-overlapping 30-day blocks) in a claim-worthy window;
- Documented completeness/coverage (a capped sample is not a census);
- Research-compatible license, unauthenticated bulk download, no requester-pays;
- Schema compatible with FCLR-010/H004 (timestamp, symbol, side, price, qty/notional, venue) or clearly mappable with provenance;
- Provenance evidence recorded in-repo (URL, access date, hash/ETag where feasible, terms).
- **Caveat to document if GO:** ironflow is Hyperliquid-native, not Binance; symbol mapping (`BTC-PERP` vs `BTCUSDT`) and venue mismatch vs the repo's Binance mark-price/funding data must be recorded, not conflated; coverage window (2025-05..2026-10) does not overlap the frozen 2024 confirmatory panels → any reopen is a NEW experiment/panel, not a continuation of sealed FCLR-002/003.

**Phase 4 — Reopen (only after a GO source):**
1. New experiment ID + clear claim not already concluded on that panel.
2. New preregistration/protocol frozen BEFORE any outcome computation (hashes/boundaries in `research_state/run_manifest.json`).
3. Run pre-registered evaluation with leakage/split/integrity checks; produce auditable verdict artifacts; atomically update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`.

## Bottleneck removal

**Root bottleneck: no admissible unauthenticated observed-liquidation source.** `ironflow/hyperliquid-liquidations` is the concrete removal path — it appears to meet the GO rubric (CC BY 4.0, unauthenticated bulk, ≥5 symbols, complete months, documented completeness, mappable schema). Everything else is green. Remove the bottleneck by completing Phase 2 empirical parquet inspection of ironflow, then (if GO) Phase 4 preregistration. Do not reorganize raw archive clutter without explicit need.

## Reopen conditions (ALL required)

1. New admissible unauthenticated data/source with verifiable provenance, schema, coverage, and terms evidence recorded in-repo.
2. New experiment ID and clear claim (Track A/B/C or H2) not already concluded on that panel.
3. New preregistration/protocol frozen BEFORE any outcome computation.

## Forbidden (no exceptions)

Status-only output; polling loops; re-running HF enumeration within the 24h cache TTL; re-GETting URLs cached within the 6h TTL; relitigating concluded tracks (A STRUCTURALLY_BLOCKED, B NOT_SUPPORTED gate NOT_MET, C/H1 NOT_SUPPORTED); threshold shopping; sealed-holdout reuse; Track A/B/C conflation; fabricated provenance; network/paid/manual/credentialed/bypassed data in research; overlay before forecast gate; `.github/workflows` edits.

## Acceptance / verification

Execute Phase 2 rubric scoring and report:
- `research_state/url_probe_cache.json` updated with per-URL evidence for ironflow parquet README + at least one parquet file (no duplicates within TTL), plus NO-GO records for any failed secondary candidates.
- `research_state/data_source_registry_alt_hunt.json` refreshed with GO/NO-GO rubric assessment per candidate; ironflow marked GO only after empirical parquet inspection confirms ≥5 symbols, a complete month, schema, license, unauthenticated bulk, no requester-pays.
- Rubric review: any GO candidate? If yes → Phase 4 reopen (new experiment ID, preregistration frozen before outcomes, heavy pre-registered evaluation). If no → stop cleanly with evidence: `NONE`.
- Environment verification (green): `python scripts/check_tracka_scope_registry_drift.py --json` (pass True, 127/127, no drift); `python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"` (PROVENANCE_OK 161); `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v` (35 tests, OK).

## Canonical artifacts

`NEXT_SESSION_TASK.md` (this file, authoritative), `FOCUS_CAMPAIGN.md`, `AGENT_HANDOFF.md`, `research_state/experiment_frontier.json`, `research_state/final_confirmatory_verdict.md`, `research_state/final_record_closure_audit.md`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/alt_source_scan_latest.json`, `research_state/data_source_registry_alt_hunt.json`, `research_state/url_probe_cache.json`, `research_state/hf_search_cache.json`.

## Last recorded verification (green, 2026-11-11T02:54Z)

```bash
python scripts/check_tracka_scope_registry_drift.py --json   # pass True, 127/127, no drift
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"   # PROVENANCE_OK 161
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v   # 35 tests, OK
```
