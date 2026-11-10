# NEXT_SESSION_TASK.md — SINGLE DURABLE HANDOFF (INITIAL TASK MESSAGE)

**Timestamp (UTC):** 2026-11-10T21:04:08Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility & liquidation-risk research)
**Program status:** `CONCLUDED_UNDER_CONSTRAINTS` — all admissible local routes exhausted with evidence. **No further initial task remains on current local data/design.**

## Initial message for next agentic work session
**SINGULAR NEXT TASK: `NONE` (pending a new admissible unauthenticated source).**
Do not poll, do not run status-only loops, do not relitigate concluded tracks, do not threshold-shop, and do not reuse sealed holdouts. Heavy work resumes only when a genuinely new admissible unauthenticated source/route exists.

## Why no work remains now (evidence-backed)
- **Track B — modeled liquidation boundary breaches (repo priority #1): CONFIRMATORY_COMPLETE, verdict NOT_SUPPORTED.**
  - TB1: degenerate/inadmissible (zero test breaches) — `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`.
  - TB2 confirmatory (frozen prereg `trackb_TB2_20261110T190405Z`, 2024-01-01..2024-09-30, BTC/ETH/BNB/SOL/XRP, label `synthetic_boundary_breach_h168_long_10x_m0`, modeled proxy only): event-adequate (test 619/5040 positives, 12.3%, all 5 symbols >0) but **forecast gate NOT_MET**. Pooled Log Loss B1=0.292447 → C2=0.287540 = +1.68% rel reduction (<2% floor); 95% CI [-0.010997, 0.003094] crosses zero (p=0.488); Holm fails; 2 non-overlapping 30d test blocks (<3). **Overlay NOT ELIGIBLE.** Artifact: `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`. Prereg integrity resolved pre-outcome (manifest hash corrected to canonical `46dcfb56c279e853230e75f6cb246ed878d765d2b399ea9a2e21c41581194adb`); provenance `PROVENANCE_OK 161`, unmapped 0.
- **Track C / H1 — funding-conditioned volatility:** concluded **NOT_SUPPORTED** (claim-worthy local panels exhausted: FCLR-003/008/009/012-V/013/014). Overlay INELIGIBLE.
- **Track A — observed liquidations:** **STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census). Not locally repairable. Track B modeled breaches are not observed liquidations.

## Reopen conditions (only path to significant new progress)
A future session may start work only with ALL of:
1. A **new admissible unauthenticated data source** (no payment/signup/API key/manual/credentialed/bypassed access) with verifiable provenance, schema, coverage, and terms evidence recorded in-repo.
2. A **new experiment ID** and a clear claim (Track A observed liquidations, Track B modeled breaches, Track C/H1 volatility, or H2 Shek replication) not already concluded on that panel.
3. A **new preregistration/protocol frozen BEFORE any outcome computation**, with hashes/boundaries recorded in `research_state/run_manifest.json`.

If no such source exists, stop cleanly with evidence (no fabricated progress).

## Hard constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxy only, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits.

## Canonical artifacts
- Verdict/evidence: `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`, `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/experiment_frontier.json`
- Handoffs: `AGENT_HANDOFF.md`, `NEXT_SESSION_TASK.md` (this file), `FOCUS_CAMPAIGN.md`

## Canonical verification (green on current state)
```bash
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"
```
