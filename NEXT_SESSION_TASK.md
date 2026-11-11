# NEXT_SESSION_TASK — Single Durable Handoff (Initial Task Message)

**Timestamp (UTC):** 2026-11-11T03:38:37Z (refreshed; evidence/state unchanged)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Program status:** `CONCLUDED_UNDER_CONSTRAINTS` — all admissible local routes exhausted with evidence. This is the **single durable handoff**; treat `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, and `HANDOFF_NEXT_SESSION.md` as pointers only.

## Initial message for the next agentic work session (execute first)

**SINGULAR NEXT TASK: `NONE` (pending a new admissible unauthenticated source).**

1. Read this file, then `FOCUS_CAMPAIGN.md` and `AGENT_HANDOFF.md` for context. This file is authoritative.
2. **Do not** poll, run status-only loops, relitigate concluded tracks, threshold-shop, reuse sealed holdouts, fabricate data/provenance, or conflate Track A/B/C.
3. Search only for a **new admissible unauthenticated** source/route (no payment, signup, API key, manual download, credentialed, or bypassed access) that could reopen an untested claim-worthy question for this repo. If none exists in-repo and no new admissible source is provided, **stop cleanly with evidence** — `NONE` is the task.

## Repo-name-prioritized state (both legs exhausted)

1. **Funding-conditioned volatility (Track C/H1):** **NOT_SUPPORTED** on all claim-worthy local panels (FCLR-003/008/009/012-V/013/014). Overlay ineligible; C2 vs B1 fails pre-registered forecast gate. Evidence: `research_state/final_confirmatory_verdict.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/hypothesis_registry.json`.

2. **Modeled liquidation boundary breaches (Track B, proxy only — not observed liquidations):** **CONFIRMATORY_COMPLETE, NOT_SUPPORTED.** TB1 degenerate/inadmissible (zero test breaches). TB2 frozen `trackb_TB2_20261110T190405Z` (2024-01-01..2024-09-30, BTC/ETH/BNB/SOL/XRP, `synthetic_boundary_breach_h168_long_10x_m0`): event-adequate (619/5040, 12.3%) but forecast gate NOT_MET (Log Loss B1=0.292447→C2=0.287540, +1.68% < 2%; 95% CI crosses zero, p=0.488; Holm fails; <3 test blocks). Overlay not eligible. Evidence: `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`, `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`.

3. **Observed liquidations (Track A):** **STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census; Binance `liquidationSnapshot` 404, `fapi forceOrders` 451; no admissible unauthenticated census found). Not locally repairable. Evidence: `research_state/track_a_structural_block.md`, `research_state/liquidation_sources_enumeration.md`, `research_state/alt_source_scan_latest.json`.

## Bottlenecks

**None blocking.** Bottlenecks cleared with evidence: script-scope registry aligned (127/127, `pass=true`, no drift); provenance verified (161/161 funding-rate files, unmapped_count=0); environment ready (numpy/pandas/scipy). Handoffs consolidated here. Known inefficiency: large volume of raw data zips/dirs at repo root (from ingested Binance archives) clutters navigation; not a program blocker — avoid reorganizing without explicit need.

## Reopen conditions — only path to significant heavy progress (ALL required)

1. **New admissible unauthenticated data/source** with verifiable provenance, schema, coverage, and terms evidence recorded in-repo.
2. **New experiment ID** and a clear claim (Track A/B/C or H2) not already concluded on that panel.
3. **New preregistration/protocol frozen BEFORE any outcome computation**, with hashes/boundaries recorded in `research_state/run_manifest.json`.

## Heavy-work mandate (if reopened)

- Work must be **heavy, verifiable, and pre-registered before outcomes**, producing auditable artifacts/evidence.
- **Forbidden:** status-only output, polling, relitigation, threshold shopping, sealed-holdout reuse, Track A/B/C conflation, fabricated provenance, network/paid/manual/credentialed/bypassed data, overlay before forecast gate, `.github/workflows` edits.
- Deliver verifiable evidence or stop with evidence. **`NONE` until reopen conditions are satisfied.**

## Canonical artifacts

`NEXT_SESSION_TASK.md` (this file), `FOCUS_CAMPAIGN.md`, `AGENT_HANDOFF.md`, `research_state/experiment_frontier.json`, `research_state/final_confirmatory_verdict.md`, `research_state/final_record_closure_audit.md`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`.

## Last recorded verification (green, 2026-11-11T02:54Z)

```bash
python scripts/check_tracka_scope_registry_drift.py --json   # pass True, 127/127, no drift
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"   # PROVENANCE_OK 161
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v   # 35 tests, OK
```
Full `unittest discover tests` exceeds practical timeout (>5 min) without failure output; targeted Track C provenance suite is green (35/35). No bottleneck remains blocking; program stays `CONCLUDED_UNDER_CONSTRAINTS`.

(End of file - total 48 lines)