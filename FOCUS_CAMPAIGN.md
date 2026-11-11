# FOCUS_CAMPAIGN — Heavy-Work Execution Plan (Pointer)

**Timestamp (UTC):** 2026-11-11T04:35:48Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Program status:** `CONCLUDED_UNDER_CONSTRAINTS`
**Single durable handoff (authoritative initial task):** `NEXT_SESSION_TASK.md` → **SINGULAR NEXT TASK: `SOURCE_UNBLOCK_CAMPAIGN`** pending a new admissible unauthenticated source.

## Repo-name-prioritized outcome (closed under constraints)

1. **Funding-conditioned volatility (Track C/H1):** NOT_SUPPORTED on all claim-worthy local panels. `research_state/final_confirmatory_verdict.md`
2. **Modeled liquidation boundary breaches (Track B, proxy only):** CONFIRMATORY_COMPLETE, NOT_SUPPORTED (TB1 degenerate; TB2 gate NOT_MET). `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`
3. **Observed liquidations (Track A):** STRUCTURALLY_BLOCKED. `research_state/track_a_structural_block.md`

## Bottleneck to remove

**Root bottleneck: no admissible unauthenticated observed-liquidation source.** Track A is the repo-name-prioritized leg (liquidation risk) and is structurally blocked, not inefficient: Binance liquidationSnapshot 404, forceOrders 451; Bybit/OKX/Deribit no unauthenticated complete census; HF/Zenodo/GitHub exhausted for frozen 2024 windows; the only admissible source (HF `ochinimus/crypto-liquidation-ticks`) covers 2026-07..08 only (FCLR-005 exploratory, no incremental skill, <3 blocks). Everything else is green (registry/provenance/environment), so the campaign below is the concrete removal path — not status work.

## Next campaign — SOURCE_UNBLOCK_CAMPAIGN (heavy, bounded; execute only per NEXT_SESSION_TASK.md)

**Phase 1 — Enumerate (bounded, cached):** live HF `/api/datasets?search=` full-body enumeration across 9 liquidation queries, deduped against `hf_search_cache.json` and prior scans; venue-native archive probes (Binance liquidationSnapshot UM/CM daily/monthly, Bybit public.bybit.com spot/trading/linear, OKX, Deribit, CryptoDataDownload, Laevitas); academic/archive probes (Zenodo API, surfaced HF datasets incl. hyperliquid-builder panel, werracle-oev, Chainticks defi, verilex, PhysiAI). Output: refreshed `research_state/alt_source_scan_latest.json` + `data_source_registry_alt_hunt.json`.

**Phase 2 — Probe + evidence (unauthenticated only):** per-candidate GET/HEAD with retry/backoff; record status, content-type, body preview, headers, pagination/path stability, timestamps, symbol coverage, license/terms, requester-pays absence. Persist in shared `url_probe_cache.json` so blocked sessions never re-GET the same URL. Documented NO-GO with evidence for every inadmissible candidate.

**Phase 3 — Rubric (GO requires ALL):** ≥5 instruments AND (≥1 complete month with ≥5 symbols OR ≥3 non-overlapping 30-day blocks) in a claim-worthy window; documented completeness (capped sample ≠ census); research-compatible license; unauthenticated bulk download; no requester-pays; schema compatible with FCLR-010/H004 or mappable with provenance; provenance evidence in-repo (URL, access date, hash/ETag, terms).

**Phase 4 — Reopen (only after a GO source):** new experiment ID + clear claim not already concluded; new preregistration/protocol frozen BEFORE any outcome computation; run pre-registered evaluation with leakage/split/integrity checks; auditable verdict artifacts; atomically update `experiment_frontier.json`, `hypothesis_registry.json`, `run_manifest.json`.

**Forbidden:** status-only work, polling, relitigation, threshold shopping, sealed-holdout reuse, Track A/B/C conflation, fabricated provenance, network/paid/manual/credentialed/bypassed data, overlay before forecast gate, `.github/workflows` edits. If no GO candidate after the campaign: stop cleanly with evidence (`NONE`). No exceptions.

## Canonical artifacts

`NEXT_SESSION_TASK.md` (authoritative), `FOCUS_CAMPAIGN.md`, `AGENT_HANDOFF.md`, `research_state/experiment_frontier.json`, `research_state/final_confirmatory_verdict.md`, `research_state/final_record_closure_audit.md`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/alt_source_scan_latest.json`, `research_state/data_source_registry_alt_hunt.json`, `research_state/url_probe_cache.json`, `research_state/hf_search_cache.json`.
