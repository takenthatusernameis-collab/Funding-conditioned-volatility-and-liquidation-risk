# HANDOFF — Funding-conditioned-volatility-and-liquidation-risk
**Single durable handoff / initial task message for next agentic work session**
**Timestamp (UTC):** 2026-11-11T07:26:05Z
**Repo:** `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk`

## Repo-priority state (evidence-backed, do not relitigate)
- **Track A — Observed liquidations (repo-name priority): STRUCTURALLY_BLOCKED.** No admissible unauthenticated liquidation census for frozen/claim-worthy windows (Binance liquidationSnapshot 404, forceOrders 451; Bybit/OKX/Deribit no unauthenticated complete census). Prior admissible `ochinimus/crypto-liquidation-ticks` (CC BY 4.0) covers only 2026-07-08..2026-08-06 (FCLR-005 exploratory_only, no incremental skill, <3 blocks). `research_state/track_a_structural_block.md`, `research_state/final_confirmatory_verdict.md`.
- **Track B — Modeled breach proxy:** CONFIRMATORY_COMPLETE, NOT_SUPPORTED (TB1 degenerate/zero test breaches; TB2 gate NOT_MET: LogLoss B1=0.292447→C2=0.287540 +1.68% <2%, 95% CI crosses zero p=0.488, Holm fails, 2 test blocks <3). Not observed liquidations. `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`.
- **Track C/H1 — Funding-conditioned volatility:** NOT_SUPPORTED on all claim-worthy local panels (FCLR-003/008/009/012-V/013/014). `research_state/final_confirmatory_verdict.md`, `research_state/hypothesis_registry.json`.
- **Program:** `CONCLUDED_UNDER_CONSTRAINTS`. Environment green (last recorded): scope registry 127/127 pass, provenance 161/161 verified unmapped_count=0, targeted tests 35/35 OK.

## Bottleneck (only path to significant heavy progress)
**No adjudicated admissible unauthenticated observed-liquidation source for a claim-worthy Track A reopen.** All local routes exhausted; new admissible unauthenticated data/source is required.

## GO-pending unblock candidate (empirical evidence present locally)
**HF `ironflow/hyperliquid-liquidations`** (`ironflow`, CC BY 4.0, unauthenticated HF bulk parquet, no requester-pays indicated). Local cache: `research_state/data_cache/ironflow_events/2025-05..2026-10.parquet` (18 event-month files). Empirical inspection (2026-11-11, pyarrow/pandas) confirms:
- Schema (events): `timestamp[ms,UTC], market, issuer, wallet, position_side, size, notional_usd, avg_price, fills, block, tx_hash` — mappable to FCLR-010/H004-style fields (timestamp,symbol/market,side,price/avg_price,qty/notional).
- Complete months with ≥5 symbols: 2025-06..2026-10 all full calendar coverage in-file with 171–353 distinct markets; 2025-05 partial (starts 2025-05-25, 164 markets) — exclude as incomplete month. Rows range ~61k–257k/month (complete months). README/monitor evidence documents replayed Hyperliquid S3 archive + sampled `userFillsByTime` match (see `research_state/ironflow_probe_*`, monitor state).
- Provenance anchors: tree/probe HEADs show unauthenticated access; `research_state/url_probe_cache.json` records `data/events/2025-10.parquet` 302→CDN with `x-linked-etag "e5382066e77c383e..."`, `x-xet-hash 104aecc4586f4cb0...`; README probe cached.
- **Venue/scope caveat (must not be conflated):** Hyperliquid-native markets (`*-PERP`), not Binance USDT-margined futures; coverage 2025-05-25..2026-10-31 does **not** overlap frozen 2024 confirmatory panels. Any reopen is a **NEW experiment/panel** with explicit symbol/venue mapping and new preregistration — never a continuation of sealed FCLR-002/003/Track B/C conclusions.

## SINGULAR NEXT TASK — `SOURCE_UNBLOCK_CAMPAIGN` (heavy, execute immediately)
Objective: finalize adjudication of `ironflow/hyperliquid-liquidations` and remaining unprobed candidates with persisted rubric evidence; if GO, move to Phase 4 preregistered heavy work on a NEW Track A experiment.

### Phase 1 — Enumerate (DONE, cached)
HF live enumeration completed 20261111T044041Z (`research_state/alt_source_scan_latest.json`, `research_state/hf_search_cache.json`, 9 queries). **Do not re-run HF enumeration within 24h TTL; do not re-GET cached URLs within 6h TTL.**

### Phase 2 — Probe/adjudicate (pending formalization, heavy where needed)
1. **Ironflow (primary):** Produce a bounded, auditable rubric record using existing local parquet cache + cached probes (no unnecessary redownload). Compute/record per complete month: file, rows, distinct markets, ts_min/ts_max, sha256 of local parquet (and cite cached CDN etag/xet-hash), license/terms, unauthenticated/no-requester-pays evidence, schema, completeness note, and venue-mismatch caveat. Treat as **GO for Track A source-admissibility (Hyperliquid liquidation census, 2025-06..2026-10, ≥5 symbols/month)** only if evidence supports documented completeness; otherwise NO-GO/REVIEW with reasons.
2. **Secondary (bounded):** score remaining unprobed/review HF-discovered candidates from scan/cache (`Gopher-Lab` DeFi/podcast transcript?, `french-open-data` retirement-liquidation datasets = wrong domain, `tanod_base-lending-liquidations` DeFi, `PhysiAI_*` heatmapping/derived not census, `carrierone_verilex-defi-liquidations` x402/requester-pays, `Chainticks_defi-liquidations` DeFi) with quick unauthenticated evidence where cheap; record explicit NO-GO reasons. Reuse `url_probe_cache.json`.
3. Persist: update `research_state/data_source_registry_alt_hunt.json` with per-candidate GO/NO-GO/REVIEW + evidence; update `research_state/alt_source_scan_latest.json` if needed; append probe evidence without duplicate fetches.

### Phase 3 — Rubric (GO requires ALL)
≥5 instruments AND (≥1 complete month with ≥5 symbols OR ≥3 non-overlapping 30-day blocks) in claim-worthy window; documented completeness/census (sample≠census); research-compatible license; unauthenticated bulk download; no requester-pays; schema compatible/mappable to FCLR-010/H004; provenance in-repo (URL, access date, hash/ETag where feasible, terms).

### Phase 4 — Reopen only on GO (heavy, preregistered)
1. Define **new Track A experiment** (e.g. Hyperliquid observed-liquidation modeling) with explicit claim, panel, symbols, and venue; do not claim Binance/2024 continuity.
2. **Freeze preregistration/protocol BEFORE outcomes** (hashes/boundaries in `research_state/run_manifest.json`; new experiment/frontier/hypothesis entries as needed).
3. Build aligned analysis panel (liquidation events + compatible Hyperliquid market/funding/price context from admissible unauthenticated sources, with provenance) or document blocker if alignment data inadmissible — do not fabricate.
4. Run pre-registered evaluation with leakage/split/integrity checks; produce auditable verdict artifacts; atomically update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`.

## Execution checklist (next session)
- [ ] Score/adjudicate ironflow with in-repo evidence record (GO/NO-GO) and update `data_source_registry_alt_hunt.json`.
- [ ] Close out secondary candidates with evidence-backed NO-GO/REVIEW where applicable (no polling/redundant GETs).
- [ ] If **GO**: draft/freeze Track A prereg spec + run manifest boundaries for a new Hyperliquid liquidation experiment before any outcome computation; then execute heavy panel build/eval.
- [ ] If **no GO** after adjudication: stop cleanly with evidence `NONE` (no status-only loop).
- [ ] Keep verification green before/after substantive changes:
  - `python scripts/check_tracka_scope_registry_drift.py --json` (pass True)
  - provenance check on `research_state/data_cache/*-fundingRate-*.csv` via `scripts.trackc_provenance_lineage.verify_paths_with_manifests` (verified, unmapped_count==0)
  - `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v`

## Forbidden
No polling, no status-only output, no HF re-enumeration within 24h TTL, no cached-URL re-GET within 6h TTL, no relitigating concluded tracks, no threshold shopping, no sealed-holdout reuse, no Track A/B/C conflation, no fabricated provenance, no paid/signup/API-key/manual/credentialed/bypassed data, no overlay before forecast gate, no `.github/workflows` edits.

## Canonical artifacts
`HANDOFF_NEXT_SESSION.md` (this file), `NEXT_SESSION_TASK.md`, `FOCUS_CAMPAIGN.md`, `AGENT_HANDOFF.md`, `research_state/experiment_frontier.json`, `research_state/final_confirmatory_verdict.md`, `research_state/final_record_closure_audit.md`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/alt_source_scan_latest.json`, `research_state/data_source_registry_alt_hunt.json`, `research_state/url_probe_cache.json`, `research_state/hf_search_cache.json`.

(End of file - total 56 lines)