# HANDOFF_NEXT_SESSION — Single Durable Initial Task Message

**Timestamp (UTC):** 2026-11-11T04:38:13Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Authoritative initial task:** `NEXT_SESSION_TASK.md` — **SINGULAR NEXT TASK: `SOURCE_UNBLOCK_CAMPAIGN`**

---

## CONTEXT (evidence-backed, non-negotiable)

| Track | Status | Evidence |
|-------|--------|----------|
| **Track A — Observed liquidations** | **STRUCTURALLY_BLOCKED** | Binance `liquidationSnapshot` 404, `forceOrders` 451; Bybit/OKX/Deribit no unauthenticated complete census; HF/Zenodo/GitHub exhausted for frozen 2024 windows; only admissible source (`ochinimus/crypto-liquidation-ticks`, CC BY 4.0) covers 2026-07-08..2026-08-06 only — FCLR-005 exploratory_only, no incremental skill, <3 non-overlapping 30-day blocks |
| **Track B — Modeled breach proxy** | **CONFIRMATORY_COMPLETE, NOT_SUPPORTED** | TB1 degenerate (zero test breaches); TB2 gate NOT_MET: Log Loss B1=0.292447→C2=0.287540 (+1.68% < 2% floor), 95% CI crosses zero (p=0.488), Holm fails, 2 test blocks < 3 |
| **Track C/H1 — Funding-conditioned volatility** | **NOT_SUPPORTED** | All claim-worthy local panels exhausted (FCLR-003/008/009/012-V/013/014) |

**Root bottleneck:** No admissible unauthenticated observed-liquidation source. Registry/provenance/environment all green (127/127 scope registry pass, 161/161 provenance verified, 35/35 targeted tests green). The `SOURCE_UNBLOCK_CAMPAIGN` in `NEXT_SESSION_TASK.md` is the **only** concrete removal path.

---

## SINGULAR NEXT TASK: `SOURCE_UNBLOCK_CAMPAIGN` (execute immediately)

**Objective:** Discover, probe, and rubric-score new admissible unauthenticated observed-liquidation sources that could reopen Track A (or extend Track B/C to an untested claim-worthy panel). Every candidate gets a persisted GO/NO-GO evidence record; no candidate is re-probed without cache; no session ends without either a new GO candidate or an evidence-backed exhaustion record.

### Phase 1 — Enumerate (bounded, cached)
- **Re-run live HF `/api/datasets?search=` enumeration** (9 queries: `liquidation`, `liquidations`, `crypto liquidation`, `perpetual liquidation`, `hyperliquid liquidation`, `funding liquidation`, `crypto perpetual liquidation`, `liquidation ticks`, `perpetual futures liquidation`) with **full-body scan** (no 200-byte preview truncation), dedup against `research_state/hf_search_cache.json` and prior `alt_source_scan_*.json`.
- **Probe venue-native public archives:** `data.binance.vision` liquidationSnapshot (UM/CM daily/monthly), `public.bybit.com` (spot/trading/linear), OKX public data, Deribit public endpoints, CryptoDataDownload Binance directory, Laevitas.
- **Probe academic/third-party archives:** Zenodo API (crypto/perpetual liquidation); HF datasets already surfaced: `ochinimus/crypto-liquidation-ticks`, `nick128373/crypto-liquidation-ticks`, `craftify2221/hyperliquid-builder-liquidation-panel`, `pCwOrM/werracle-oev-liquidation-dataset-2026`, `Chainticks/defi-liquidations`, `carrierone/verilex-defi-liquidations`, `PhysiAI/Bitcoin-Liquidation-Heatmapping`.
- **Output:** Refreshed `research_state/alt_source_scan_latest.json` + `research_state/data_source_registry_alt_hunt.json`.

### Phase 2 — Probe + Evidence (unauthenticated only)
- For each candidate: unauthenticated GET/HEAD with retry/backoff (max 2 retries); record status, content-type, body preview, headers, pagination/download-path stability, earliest/latest timestamp, symbol coverage count, license/terms, requester-pays absence.
- Persist per-URL probe evidence in `research_state/url_probe_cache.json` (shared, deduped, TTL-bounded) so blocked sessions never re-GET the same URL.
- **Never** use payment, signup, API key, manual download, credentials, or bypassed access. Any candidate failing admissibility gets a documented NO-GO with evidence.

### Phase 3 — Rubric (GO requires **ALL**)
1. ≥5 instruments with usable coverage, **AND** (≥1 complete month with ≥5 symbols **OR** ≥3 non-overlapping 30-day blocks) in a claim-worthy window
2. Documented completeness/coverage (a capped sample is **not** a census)
3. Research-compatible license, unauthenticated bulk download, no requester-pays
4. Schema compatible with FCLR-010/H004 (timestamp, symbol, side, price, qty/notional, venue) or clearly mappable with provenance
5. Provenance evidence recorded in-repo (URL, access date, hash/ETag where feasible, terms)

### Phase 4 — Reopen (only after a GO source)
1. New experiment ID + clear claim not already concluded on that panel
2. New preregistration/protocol frozen **BEFORE** any outcome computation (hashes/boundaries in `research_state/run_manifest.json`)
3. Run pre-registered evaluation with leakage/split/integrity checks; produce auditable verdict artifacts; atomically update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`

---

## EXECUTION COMMANDS (run these)

```bash
# 1) Run the heavy enumeration/probe campaign (writes alt_source_scan_latest.json + data_source_registry_alt_hunt.json)
python scripts/hunt_alternative_liquidation_sources.py

# 2) Rubric review: any GO candidate? If yes → Phase 4 reopen. If no → stop cleanly with evidence: NONE.

# 3) Environment verification (must all pass):
python scripts/check_tracka_scope_registry_drift.py --json                                    # pass True, 127/127, no drift
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"   # PROVENANCE_OK 161
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v   # 35 tests, OK
```

---

## FORBIDDEN (no exceptions)
- Status-only output; polling loops; relitigating concluded tracks (A STRUCTURALLY_BLOCKED, B NOT_SUPPORTED gate NOT_MET, C/H1 NOT_SUPPORTED)
- Threshold shopping; sealed-holdout reuse; Track A/B/C conflation; fabricated provenance
- Network/paid/manual/credentialed/bypassed data in research; overlay before forecast gate; `.github/workflows` edits

---

## CANONICAL ARTIFACTS (read/write these)
`NEXT_SESSION_TASK.md` (authoritative), `FOCUS_CAMPAIGN.md`, `AGENT_HANDOFF.md`, `research_state/experiment_frontier.json`, `research_state/final_confirmatory_verdict.md`, `research_state/final_record_closure_audit.md`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/alt_source_scan_latest.json`, `research_state/data_source_registry_alt_hunt.json`, `research_state/url_probe_cache.json`, `research_state/hf_search_cache.json`.

---

**If the campaign finds no new admissible source, stop cleanly with evidence: `NONE`.** Do not produce status work. Do not poll. Do not relitigate. The only path to significant heavy progress is a new admissible unauthenticated data source.