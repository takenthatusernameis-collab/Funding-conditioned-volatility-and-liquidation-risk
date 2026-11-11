# NEXT_SESSION_TASK.md — SINGLE DURABLE HANDOFF (INITIAL TASK MESSAGE)

**Timestamp (UTC):** 2026-11-11T02:37:44Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Program status:** `CONCLUDED_UNDER_CONSTRAINTS` — all admissible local routes exhausted with evidence. **No further initial task remains on current local data/design.**

## Initial message for the next agentic work session (execute first)

**SINGULAR NEXT TASK: `NONE` (pending a new admissible unauthenticated source).**

Immediate actions:
1. Read this file, `FOCUS_CAMPAIGN.md`, and `AGENT_HANDOFF.md` — this is the complete, non-contradictory handoff.
2. Do **not** poll, do **not** run status-only loops, do **not** relitigate concluded tracks, do **not** threshold-shop, do **not** reuse sealed holdouts, do **not** fabricate data/provenance.
3. Search only for a **new admissible unauthenticated** source/route (no payment/signup/API key/manual/credentialed/bypassed access) that could reopen an untested claim-worthy question for this repo. If none exists in-repo and no new source is provided, **stop cleanly with evidence** — `NONE` is the task.

## Repo-name prioritization (authoritative, both legs exhausted)

1. **Track C/H1 — funding-conditioned volatility:** **NOT_SUPPORTED** on all claim-worthy local panels (FCLR-003/008/009/012-V/013/014). Overlay INELIGIBLE. Primary contrast C2 vs B1 fails pre-registered forecast gate. Evidence: `research_state/final_confirmatory_verdict.md`, `research_state/evaluation_summary_FCLR003.md`, `research_state/hypothesis_registry.json`.
2. **Track B — modeled liquidation boundary breaches (modeled proxy only, not observed liquidations):** **CONFIRMATORY_COMPLETE, NOT_SUPPORTED.** TB1 degenerate/inadmissible (zero test breaches). TB2 frozen `trackb_TB2_20261110T190405Z` (2024-01-01..2024-09-30, BTC/ETH/BNB/SOL/XRP, `synthetic_boundary_breach_h168_long_10x_m0`): event-adequate (619/5040, 12.3%) but forecast gate NOT_MET — Log Loss B1=0.292447→C2=0.287540 (+1.68% < 2%), 95% CI [-0.010997,0.003094] crosses zero (p=0.488), Holm fails, 2 test blocks <3. Overlay NOT ELIGIBLE. Evidence: `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`, `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`.
3. **Track A — observed liquidations:** **STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census; Binance `liquidationSnapshot` 404, `fapi forceOrders` 451; no admissible unauthenticated census found). Not locally repairable. Evidence: `research_state/track_a_structural_block.md`, `research_state/liquidation_sources_enumeration.md`, `research_state/alt_source_scan_latest.json`.

## Reopen conditions — only path to significant heavy progress (ALL required)

1. **New admissible unauthenticated data/source** with verifiable provenance, schema, coverage, and terms evidence recorded in-repo (no payment/signup/API key/manual/credentialed/bypassed access).
2. **New experiment ID** and a clear claim (Track A observed liquidations, Track B modeled breaches, Track C/H1 volatility, or H2 Shek replication) not already concluded on that panel.
3. **New preregistration/protocol frozen BEFORE any outcome computation**, with hashes/boundaries recorded in `research_state/run_manifest.json`.

## Heavy-work mandate (future agents cannot avoid heavy work)

- Any resumed work must be **heavy, verifiable, pre-registered before outcomes**, and produce auditable artifacts/evidence.
- No status-only output, no polling, no relitigation, no threshold shopping, no sealed-holdout reuse.
- Deliver verifiable evidence or stop with evidence. `NONE` until reopen conditions are satisfied.

## Hard constraints (NON-NEGOTIABLE)

No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxy only, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits.

## Bottlenecks — current state

**None blocking.** Environment ready (numpy/pandas/scipy). Script-scope registry aligned (127/127). Root md+json bound (211). `research_state/experiment_frontier.json` valid concluded-state frontier. This file is the single durable initial task.

## Canonical verification (last recorded green, 2026-11-10T23:28Z)

```bash
python -m unittest discover tests            # 1124 tests, OK
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v   # 35 tests, OK
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"   # PROVENANCE_OK 161
python scripts/check_tracka_scope_registry_drift.py --json   # pass True, 127/127
```
