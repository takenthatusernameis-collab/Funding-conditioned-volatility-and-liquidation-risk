# FOCUS_CAMPAIGN.md — Heavy-Work Execution Plan

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Priority (per repo name):** 1) Track C/H1 funding-conditioned volatility — **CONCLUDED NOT_SUPPORTED**; 2) Track B liquidation boundary risk (modeled synthetic breaches) — **CONCLUDED NOT_SUPPORTED**; 3) Track A observed liquidations — **STRUCTURALLY_BLOCKED**.
**Campaign timestamp:** 2026-11-11T02:34:17Z
**Program status:** `CONCLUDED_UNDER_CONSTRAINTS` — all admissible local routes exhausted with evidence.
**Single durable handoff (authoritative initial task):** `NEXT_SESSION_TASK.md` — `next_unfinished_task: NONE` pending a new admissible unauthenticated source.

## Hard constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated provenance/outcomes; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxy only, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits.

## Mission (current)
Preserve an auditable, reproducible terminal state and ensure future agents cannot idle or relitigate: the singular next action is **NONE** unless a genuinely new admissible unauthenticated source/route appears. Any resumed work must be heavy, verifiable, and pre-registered before outcomes.

## Heavy-work mandate (future agents cannot avoid heavy work)
- Any resumed work must be **heavy, verifiable, and pre-registered before outcomes**.
- No status-only output, no polling loops, no relitigation of concluded tracks, no threshold shopping, no sealed-holdout reuse.
- Deliver verifiable evidence or stop cleanly with evidence. Fabricated progress is prohibited.

## Current state (verified evidence)
- **Track B:** CONFIRMATORY_COMPLETE, gate NOT_MET / NOT_SUPPORTED. TB1 degenerate (0 test breaches). TB2 (frozen `trackb_TB2_20261110T190405Z`, 2024-01-01..2024-09-30, h168_long_10x_m0, 5 symbols): event-adequate test positives 619/5040 (12.3%) but pooled Log Loss B1=0.292447→C2=0.287540 (+1.68% < 2%), 95% CI [-0.010997,0.003094] crosses zero (p=0.488), Holm fails, 2 test blocks <3. Overlay INELIGIBLE. `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`.
- **Track C/H1:** concluded NOT_SUPPORTED on all claim-worthy local panels (FCLR-003/008/009/012-V/013/014). Overlay INELIGIBLE.
- **Track A:** STRUCTURALLY_BLOCKED (no admissible unauthenticated observed-liquidation census). Not locally repairable.

## Bottlenecks removed (verified clean)
- Registry drift aligned at 127 entries (127 `scripts/*.py`, 0 missing/extra/bad). `check_tracka_scope_registry_drift.py` reports `pass True`.
- Root md+json bound 211 (baseline 144 md + 67 json). Environment: `numpy`/`pandas`/`scipy` installed.
- Corrupted `research_state/experiment_frontier.json` repaired to valid concluded-state frontier.
- Durable handoffs consolidated to one unambiguous initial task (`NONE` pending new admissible source, with explicit reopen gates).

## Execution rules (for any future reopen)
1. New admissible unauthenticated source only (no network-paid/manual/credentialed). 2. New experiment ID. 3. Prereg/freeze before outcomes. 4. No threshold shopping/holdout reuse. 5. Track B = modeled breach proxy only. 6. No fabricated provenance. 7. No status-only output; deliver heavy verifiable work or stop with evidence.

## Canonical verification (re-run 2026-11-10T23:28Z, all green)
```bash
python -m unittest discover tests            # 1124 tests, OK (exit 0)
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v   # 35 tests, OK
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"   # PROVENANCE_OK 161
python scripts/check_tracka_scope_registry_drift.py --json   # pass True, 127/127
```
