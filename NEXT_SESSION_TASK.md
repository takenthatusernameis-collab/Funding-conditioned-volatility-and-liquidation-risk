# NEXT_SESSION_TASK — Single Durable Handoff (Initial Task Message)

**Timestamp (UTC):** 2026-11-11T04:35:48Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Program status:** `CONCLUDED_UNDER_CONSTRAINTS` for all three tracks (evidence-backed). This file is the **single durable handoff** and authoritative initial task message. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, and `HANDOFF_NEXT_SESSION.md` are pointers only.

## Initial message for the next agentic work session (execute first)

**SINGULAR NEXT TASK: `SOURCE_UNBLOCK_CAMPAIGN` — remove the Track A structural block so heavy research can continue.**

The repo name prioritizes liquidation risk. Track A (observed liquidations) is **STRUCTURALLY_BLOCKED**: Binance `liquidationSnapshot` 404 (UM/CM, daily/monthly), Binance `fapi forceOrders` HTTP 451 restricted, Bybit/OKX/Deribit no unauthenticated complete liquidation census, HF/Zenodo/GitHub exhausted for the frozen 2024 confirmatory windows; the only admissible source (HF `ochinimus/crypto-liquidation-ticks`, CC BY 4.0) covers 2026-07-08..2026-08-06 only (FCLR-005 pilot: exploratory_only, no incremental skill, <3 non-overlapping 30-day blocks, cannot clear the frozen gates). Track C/H1 **NOT_SUPPORTED** on all claim-worthy panels (FCLR-003/008/009/012-V/013/014); Track B **NOT_SUPPORTED** (TB1 degenerate/zero test breaches; TB2 forecast gate NOT_MET: Log Loss B1=0.292447→C2=0.287540, +1.68% < 2% floor, 95% CI crosses zero p=0.488, Holm fails, 2 test blocks <3). All local routes exhausted — the only path to significant heavy progress is a **new admissible unauthenticated data source**.

Do not poll, relitigate concluded tracks, threshold-shop, reuse sealed holdouts, fabricate data/provenance, conflate Track A/B/C, or produce status-only output. If the campaign finds no new admissible source, stop cleanly with evidence: `NONE`.

## Focus campaign — SOURCE_UNBLOCK_CAMPAIGN (heavy, bounded, executable)

Objective: discover, probe, and rubric-score new admissible unauthenticated observed-liquidation sources that could reopen Track A (or extend Track B/C to an untested claim-worthy panel). Every candidate gets a persisted GO/NO-GO evidence record; no candidate is re-probed without cache; no session ends without either a new GO candidate or an evidence-backed exhaustion record.

**Phase 1 — Enumerate (bounded, cached):**
- Re-run live Hugging Face `/api/datasets?search=` enumeration (queries: `liquidation`, `liquidations`, `crypto liquidation`, `perpetual liquidation`, `hyperliquid liquidation`, `funding liquidation`, `crypto perpetual liquidation`, `liquidation ticks`, `perpetual futures liquidation`) with **full-body scan** (no 200-byte preview truncation), dedup against `research_state/hf_search_cache.json` and prior `alt_source_scan_*.json`.
- Probe venue-native public archives: `data.binance.vision` liquidationSnapshot variants (UM/CM, daily/monthly), `public.bybit.com` (spot/trading/linear directories), OKX public data paths, Deribit public endpoints, CryptoDataDownload Binance directory, Laevitas.
- Probe academic/third-party archives: Zenodo API records (crypto/perpetual liquidation); HF datasets already surfaced: `ochinimus/crypto-liquidation-ticks`, `nick128373/crypto-liquidation-ticks`, `craftify2221/hyperliquid-builder-liquidation-panel`, `pCwOrM/werracle-oev-liquidation-dataset-2026`, `Chainticks/defi-liquidations`, `carrierone/verilex-defi-liquidations`, `PhysiAI/Bitcoin-Liquidation-Heatmapping`.
- Output: refreshed `research_state/alt_source_scan_latest.json` + `research_state/data_source_registry_alt_hunt.json`.

**Phase 2 — Probe + evidence (unauthenticated only):**
- For each candidate: unauthenticated GET/HEAD with retry/backoff (max 2 retries); record status, content-type, body preview, headers, pagination/download-path stability, earliest/latest timestamp, symbol coverage count, license/terms, requester-pays absence.
- Persist per-URL probe evidence in `research_state/url_probe_cache.json` (shared, deduped, TTL-bounded) so blocked sessions never re-GET the same URL.
- Never use payment, signup, API key, manual download, credentials, or bypassed access. Any candidate failing admissibility gets a documented NO-GO with evidence.

**Phase 3 — Rubric (GO requires ALL):**
- ≥5 instruments with usable coverage, AND (≥1 complete month with ≥5 symbols OR ≥3 non-overlapping 30-day blocks) in a claim-worthy window;
- Documented completeness/coverage (a capped sample is not a census);
- Research-compatible license, unauthenticated bulk download, no requester-pays;
- Schema compatible with FCLR-010/H004 (timestamp, symbol, side, price, qty/notional, venue) or clearly mappable with provenance;
- Provenance evidence recorded in-repo (URL, access date, hash/ETag where feasible, terms).

**Phase 4 — Reopen (only after a GO source):**
1. New experiment ID + clear claim not already concluded on that panel.
2. New preregistration/protocol frozen BEFORE any outcome computation (hashes/boundaries in `research_state/run_manifest.json`).
3. Run pre-registered evaluation with leakage/split/integrity checks; produce auditable verdict artifacts; atomically update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`.

## Bottleneck removal

**Root bottleneck: no admissible unauthenticated observed-liquidation source.** Everything else is green: track-a scope registry 127/127 pass, 161/161 funding-rate files provenance verified (unmapped_count=0), targeted tests 35/35 green, numpy/pandas/scipy ready. The campaign above is the concrete removal path. Root-level raw archive clutter is navigation inefficiency only — do not reorganize without explicit need.

## Reopen conditions (ALL required)

1. New admissible unauthenticated data/source with verifiable provenance, schema, coverage, and terms evidence recorded in-repo.
2. New experiment ID and clear claim (Track A/B/C or H2) not already concluded on that panel.
3. New preregistration/protocol frozen BEFORE any outcome computation.

## Forbidden (no exceptions)

Status-only output; polling loops; relitigating concluded tracks (A STRUCTURALLY_BLOCKED, B NOT_SUPPORTED gate NOT_MET, C/H1 NOT_SUPPORTED); threshold shopping; sealed-holdout reuse; Track A/B/C conflation; fabricated provenance; network/paid/manual/credentialed/bypassed data in research; overlay before forecast gate; `.github/workflows` edits.

## Acceptance / verification

Execute the campaign and report:
- `python scripts/hunt_alternative_liquidation_sources.py` → writes `research_state/alt_source_scan_latest.json` and `research_state/data_source_registry_alt_hunt.json`
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
