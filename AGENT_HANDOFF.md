# AGENT_HANDOFF.md — Durable Handoff Pointer

**Timestamp (UTC):** 2026-11-10T23:28:23Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Single durable handoff (authoritative initial task):** `NEXT_SESSION_TASK.md` — **execute/read immediately**.
**Program status:** `CONCLUDED_UNDER_CONSTRAINTS` — all admissible local routes exhausted with evidence (not concluded by request).

## Current state (verified)
- **Priority 1 — Track C / H1 (funding-conditioned volatility, repo-name leg):** concluded **NOT_SUPPORTED** (FCLR-003/008/009/012-V/013/014 exhausted). Overlay INELIGIBLE.
- **Priority 2 — Track B (modeled liquidation boundary breaches, repo-name liquidation-risk leg): CONFIRMATORY_COMPLETE, verdict NOT_SUPPORTED.**
  - TB1 degenerate/inadmissible (zero test breaches) — `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`.
  - TB2 confirmatory (frozen prereg `trackb_TB2_20261110T190405Z`, 2024-01-01..2024-09-30, BTC/ETH/BNB/SOL/XRP, `synthetic_boundary_breach_h168_long_10x_m0`, modeled proxy only): event-adequate (test 619/5040, 12.3%, all 5 symbols >0) but forecast gate **NOT_MET** — Log Loss B1=0.292447→C2=0.287540 (+1.68% < 2%), 95% CI [-0.010997,0.003094] crosses zero (p=0.488), Holm fails, 2 test blocks <3. **Overlay NOT ELIGIBLE.** `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`.
- **Priority 3 — Track A (observed liquidations):** **STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census). Not locally repairable. Track B ≠ observed liquidations.

## `next_unfinished_task` (singular)
**NONE — pending a new admissible unauthenticated source.**
Reopen only with: (a) new admissible unauthenticated source + verifiable provenance/coverage/terms, (b) new experiment ID, (c) new prereg frozen **before** outcomes. No polling, status-only work, relitigation, threshold shopping, or sealed-holdout reuse.

## Bottlenecks addressed this session
- Repaired consolidated durable handoffs (`NEXT_SESSION_TASK.md`, `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`) to a single timestamped (2026-11-10T23:28:23Z) unambiguous initial task: `NONE` under constraints, with explicit reopen conditions, evidence pointers, and heavy-work mandate.
- Confirmed all prior bottleneck removals remain clean: registry drift (127==127, pass True), root md+json bound (211), environment (numpy/pandas/scipy installed), `experiment_frontier.json` valid concluded-state frontier.
- Re-ran canonical verification at handoff time: full suite 1124 tests OK (exit 0), 35-test canonical subset OK, PROVENANCE_OK 161 (unmapped 0), registry drift pass True.

## Constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxy only); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits.

## Canonical verification (re-run 2026-11-10T23:28Z, all green)
```bash
python -m unittest discover tests            # 1124 tests, OK (exit 0)
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v   # 35 tests, OK
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"   # PROVENANCE_OK 161
python scripts/check_tracka_scope_registry_drift.py --json   # pass True, 127/127
```

## Heavy-work mandate (future agents cannot avoid heavy work)
Any resumed work must be heavy, verifiable, and pre-registered before outcomes. No status-only output, no polling, no relitigation, no threshold shopping, no sealed-holdout reuse. Deliver verifiable evidence or stop cleanly with evidence. `NONE` is the task until a new admissible unauthenticated source appears.