# HANDOFF — Funding-conditioned-volatility-and-liquidation-risk
**Initial task message for next agentic work session (single durable handoff)**
**Timestamp (UTC):** 2026-11-11T05:23:17Z
**Repo:** `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk`
**Authoritative task spec:** `NEXT_SESSION_TASK.md` (execute it; this file is the entry point)

## Repo-priority outcome (non-negotiable)
- **Track A — Observed liquidations (repo-name priority): STRUCTURALLY_BLOCKED.** No admissible unauthenticated liquidation census for frozen/claim-worthy windows (Binance liquidationSnapshot 404, forceOrders 451; Bybit/OKX/Deribit no unauthenticated complete census; HF/Zenodo/GitHub exhausted for 2024 windows; only previously admissible HF `ochinimus/crypto-liquidation-ticks` CC BY 4.0 covers 2026-07-08..2026-08-06 — FCLR-005 exploratory_only, no incremental skill, <3 non-overlapping 30-day blocks). Evidence: `research_state/track_a_structural_block.md`, `research_state/alt_source_scan_latest.json`, `research_state/data_source_registry_alt_hunt.json`.
- **Track B — Modeled breach proxy:** CONFIRMATORY_COMPLETE, NOT_SUPPORTED (TB1 degenerate; TB2 gate NOT_MET: Log Loss B1=0.292447→C2=0.287540 +1.68% < 2%, 95% CI crosses zero p=0.488, Holm fails, 2 test blocks < 3). `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`
- **Track C/H1 — Funding-conditioned volatility:** NOT_SUPPORTED on all claim-worthy local panels (FCLR-003/008/009/012-V/013/014). `research_state/final_confirmatory_verdict.md`

## Bottleneck (remove this, nothing else moves Track A)
**No admissible unauthenticated observed-liquidation source.** Registry/provenance/environment are green (127/127 scope registry, 161/161 provenance verified, 35/35 targeted tests). The only path to significant heavy progress is a **new admissible unauthenticated data source**.

**Removal candidate (heavy work):** HF `ironflow/hyperliquid-liquidations` — CC BY 4.0, unauthenticated bulk parquet, coverage 25 May 2025–31 Oct 2026, 468 markets, $58.7B notional, documented completeness (replayed from Hyperliquid S3 archive, sampled events match `userFillsByTime`). HEAD probe confirmed unauthenticated CDN access (etag `e5382066e77c383e0abe0b5f337242f11997e33e57b674f669465aa7915adca8`, xet-hash `104aecc4586f4cb05473fd303e37c1b63588e94a8198136e0b364be35e3cb025`). Pending Phase 2: empirical parquet inspection (≥5 symbols, complete month, schema) → Phase 4 preregistration if GO.

## SINGULAR NEXT TASK — `SOURCE_UNBLOCK_CAMPAIGN` (heavy, execute immediately)
Objective: discover/probe/rubric-score new admissible unauthenticated observed-liquidation sources (or an untested claim-worthy panel for B/C). Persist GO/NO-GO evidence per candidate; reuse caches; do not re-probe without need. End with either a GO candidate or evidence-backed exhaustion `NONE`.

**Phase 1 — Enumerate (cached/bounded):** DONE live 20261111T044041Z; do not re-run HF `/api/datasets?search=` within 24h cache TTL. Refresh `alt_source_scan_latest.json`, `data_source_registry_alt_hunt.json` only on a fresh enumeration outside TTL.

**Phase 2 — Probe (unauthenticated only):** Primary heavy task = empirically inspect `ironflow/hyperliquid-liquidations` parquet unauthenticated (`data/events/2025-10.parquet`, ~9MB); verify schema, timestamp range, ≥5 symbols per complete month, completeness; record URL, access date, hash/ETag, terms. Also probe remaining unprobed live-discovered HF candidates (Gopher-Lab, french-open-data x2, tanod, PhysiAI x3). GET/HEAD with retry/backoff; record status, content-type, body/headers, pagination/path stability, timestamps, symbol coverage, license/terms, requester-pays. Persist per-URL evidence in `research_state/url_probe_cache.json`. No payment/signup/API key/manual download/credentials/bypass.

**Phase 3 — GO rubric (ALL required):** ≥5 instruments AND (≥1 complete month with ≥5 symbols OR ≥3 non-overlapping 30-day blocks) in claim-worthy window; documented completeness/census (sample≠census); research-compatible license, unauthenticated bulk download, no requester-pays; schema compatible/mappable to FCLR-010/H004 (timestamp,symbol,side,price,qty/notional,venue); in-repo provenance evidence (URL, access date, hash/ETag, terms).

**Phase 4 — Reopen only on GO:** new experiment ID + claim not already concluded; preregister/protocol frozen BEFORE outcomes (hashes/boundaries in `research_state/run_manifest.json`); run pre-registered eval with leakage/split/integrity checks; produce auditable verdict artifacts; atomically update `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`.

## Execute (run in order)
```bash
# Phase 2 heavy work: empirically inspect ironflow parquet unauthenticated, then rubric-score.
# If GO -> Phase 4 (new experiment ID, preregistration frozen before outcomes, heavy eval).
# If no GO -> stop cleanly with evidence: NONE

# Verification (must stay green)
python scripts/check_tracka_scope_registry_drift.py --json
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v
```

## Forbidden
No status-only output, polling, relitigating concluded tracks (A STRUCTURALLY_BLOCKED, B NOT_SUPPORTED gate NOT_MET, C/H1 NOT_SUPPORTED), threshold shopping, sealed-holdout reuse, Track A/B/C conflation, fabricated provenance, network/paid/manual/credentialed/bypassed research data, overlay before forecast gate, `.github/workflows` edits. Do not re-run HF enumeration within the 24h cache TTL or re-GET URLs within the 6h probe-cache TTL.

## Canonical artifacts
`NEXT_SESSION_TASK.md` (authoritative), `FOCUS_CAMPAIGN.md`, `AGENT_HANDOFF.md`, `research_state/experiment_frontier.json`, `research_state/final_confirmatory_verdict.md`, `research_state/final_record_closure_audit.md`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/alt_source_scan_latest.json`, `research_state/data_source_registry_alt_hunt.json`, `research_state/url_probe_cache.json`, `research_state/hf_search_cache.json`.

(End of file)
