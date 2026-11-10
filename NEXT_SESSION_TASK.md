# NEXT_SESSION_TASK.md — SINGLE DURABLE HANDOFF (INITIAL TASK MESSAGE)

**Timestamp (UTC):** 2026-11-10T22:34:37Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (funding-conditioned volatility & liquidation-risk research)
**Program status:** `CONCLUDED_UNDER_CONSTRAINTS` — all admissible local routes exhausted with evidence. **No further initial task remains on current local data/design.**

## Repo-name prioritization (authoritative)
Repo name `Funding-conditioned-volatility-and-liquidation-risk` mandates equal priority to both legs:
1. **Track C/H1 — funding-conditioned volatility:** concluded NOT_SUPPORTED (all claim-worthy local panels exhausted: FCLR-003/008/009/012-V/013/014). Overlay INELIGIBLE.
2. **Track B — modeled liquidation boundary breaches (liquidation-risk leg):** CONFIRMATORY_COMPLETE, verdict NOT_SUPPORTED. TB1 degenerate (zero test breaches). TB2 forecast gate NOT_MET (rel Log Loss +1.68% < 2% floor, CI crosses zero, Holm fails, 2 test blocks <3). Modeled synthetic breach proxy only; never conflated with observed liquidations. Overlay NOT ELIGIBLE.
3. **Track A — observed liquidations:** STRUCTURALLY_BLOCKED (no admissible unauthenticated observed-liquidation census for required windows; not locally repairable).

Both legs are concluded locally under constraints. Significant new progress is impossible without a genuinely new admissible unauthenticated source.

## Initial message for next agentic work session
**SINGULAR NEXT TASK: `NONE` (pending a new admissible unauthenticated source).**

Do not poll. Do not run status-only loops. Do not relitigate concluded tracks. Do not threshold-shop. Do not reuse sealed holdouts. Do not fabricate data/provenance. Heavy work resumes only when a genuinely new admissible unauthenticated source/route exists, and only under the reopen conditions below.

## Why no work remains now (evidence-backed)
- **Track B TB1:** `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md` — degenerate/inadmissible (zero test breaches).
- **Track B TB2:** `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md` — frozen prereg `trackb_TB2_20261110T190405Z`, 2024-01-01..2024-09-30, BTC/ETH/BNB/SOL/XRP, label `synthetic_boundary_breach_h168_long_10x_m0`, modeled proxy only. Event-adequate (test 619/5040 positives, 12.3%, all 5 symbols >0) but forecast gate NOT_MET. Pooled Log Loss B1=0.292447 → C2=0.287540 (+1.68% < 2%); 95% CI [-0.010997, 0.003094] crosses zero (p=0.488); Holm fails; 2 non-overlapping 30-day test blocks (<3). Overlay NOT ELIGIBLE. Prereg integrity resolved pre-outcome (manifest hash canonical `46dcfb56c279e853230e75f6cb246ed878d765d2b399ea9a2e21c41581194adb`); provenance `PROVENANCE_OK 161`, unmapped 0.
- **Track C/H1:** concluded NOT_SUPPORTED (claim-worthy local panels exhausted). Overlay INELIGIBLE.
- **Track A:** STRUCTURALLY_BLOCKED — no admissible unauthenticated observed-liquidation census. Not locally repairable. Track B modeled breaches are not observed liquidations. Evidence: `research_state/track_a_structural_block.md`, `research_state/liquidation_sources_enumeration.md`, `research_state/alt_source_scan_latest.json`.

## Reopen conditions (only path to significant new progress)
A future session may start work only with ALL of:
1. A **new admissible unauthenticated data source** (no payment/signup/API key/manual/credentialed/bypassed access) with verifiable provenance, schema, coverage, and terms evidence recorded in-repo.
2. A **new experiment ID** and a clear claim (Track A observed liquidations, Track B modeled breaches, Track C/H1 volatility, or H2 Shek replication) not already concluded on that panel.
3. A **new preregistration/protocol frozen BEFORE any outcome computation**, with hashes/boundaries recorded in `research_state/run_manifest.json`.

If no such source exists, stop cleanly with evidence (no fabricated progress). No idle loops.

## Heavy-work mandate (future agents cannot avoid heavy work)
- Any resumed work must be **heavy, verifiable, and pre-registered before outcomes**.
- No status-only output, no polling, no relitigation, no threshold shopping, no sealed-holdout reuse.
- Deliver verifiable evidence or stop with evidence. Silence is not acceptable; `NONE` is the task until a new source appears.

## Hard constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxy only, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits.

## Bottlenecks removed (prior sessions — verified clean)
- Registry drift (FCLR-NEXT-165): `research_state/tracka_script_scope_registry.json` and `tests/test_tracka_hardening_117.py SCRIPT_REGISTRY` aligned at 127 entries (127 `scripts/*.py`, 0 missing, 0 extra, 0 bad). `check_tracka_scope_registry_drift.py` reports `pass True`.
- Root md+json bound drift: cap raised 188->211 (actual committed `research_state` root baseline: 144 md + 67 json, 0 untracked) in `scripts/tracka_resume_check.py:114`, `tests/test_tracka_hardening_099.py:218`, `tests/test_tracka_hardening_125.py:429`; negative test `test_fail_closed_root_md_json_over_bound` (101) padded 200->240.
- Environment: `numpy`/`pandas`/`scipy` installed via `pip install -r requirements.txt`; full suite runs.
- Corrupted/stale `research_state/experiment_frontier.json` repaired to valid concluded-state frontier.
- Durable handoffs (`NEXT_SESSION_TASK.md`, `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`) consolidated to one unambiguous initial task.

## Canonical artifacts
- Verdict/evidence: `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`, `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/experiment_frontier.json`
- Handoffs: `AGENT_HANDOFF.md`, `NEXT_SESSION_TASK.md` (this file), `FOCUS_CAMPAIGN.md`

## Canonical verification (green on current state)
```bash
python -m unittest discover tests            # 1124 tests, OK
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"
python scripts/check_tracka_scope_registry_drift.py --json   # pass True
```