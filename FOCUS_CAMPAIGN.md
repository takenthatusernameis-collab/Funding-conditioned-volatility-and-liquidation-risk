# FOCUS_CAMPAIGN.md — Heavy-Work Execution Plan (Funding-conditioned Volatility & Liquidation Risk)

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Priority (per repo name):** 1) Track B liquidation boundary risk (modeled) — **ACTIVE/MANDATORY**, 2) Track C / H1 funding-conditioned volatility forecast — concluded NOT_SUPPORTED, 3) Track A observed liquidations — STRUCTURALLY_BLOCKED.
**Campaign timestamp:** 2026-11-10T19:04:05Z (program NOT concluded — TB1 degenerate; TB2 prereg frozen, confirmatory run due)
**Single durable handoff (authoritative initial task):** `NEXT_SESSION_TASK.md` (also pointed to by `AGENT_HANDOFF.md`). Execute it immediately.
**Hard constraints (NON-NEGOTIABLE):** no network/paid/manual/credentialed data; no fabricated provenance/outcomes; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation; preregister before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits.

## Mission (non-optional)
Advance to a reproducible, auditable, out-of-sample verdict using only local verified data: (a) funding-conditioned volatility vs RV-only baseline — **concluded NOT_SUPPORTED**, (b) liquidation risk via **Track B modeled boundary breaches** — **MANDATORY NEXT (TB2 confirmatory)**, or record evidence-backed inadmissibility only after exhausting admissible local routes. Future agents must not idle on status docs, polling, or re-litigation of concluded tracks. Every session delivers heavy verifiable work.

## Current state (verified)
- **Track C / H1_primary:** CONCLUDED UNDER CONSTRAINTS, **NOT_SUPPORTED**. No untested claim-worthy panels with >=3 blocks remain locally. `next_unfinished_task (Track C): NONE`.
- **Track A:** **STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census). Not locally repairable.
- **Track B:** **ACTIVE.** `TRACKB-20251110T154307Z` NOT_MET/NOT_SUPPORTED; `TRACKB-MODELED-BREACH-TB1-20261110T173838Z` (2025-01-01..2026-10-31, 5x/24h long) **DEGENERATE/INADMISSIBLE** (0 synthetic breaches in frozen test split). **TB2 confirmatory READY:** 2024-01-01..2024-09-30 admissible (5 symbols, 274 days, 9 blocks, provenance verified); label h168_long_10x_m0 selected pre-freeze (>0 frozen-test positives); prereg frozen + hash recorded before outcomes. Next: execute confirmatory evaluation + propagate verdict.

## Bottlenecks removed (significant progress unblocked)
- Replaced TB1-stale/ambiguous routing with one mandatory TB2 path in `NEXT_SESSION_TASK.md`.
- Pre-freeze label/split selected with >0 frozen-test positives; prereg frozen + hash recorded before outcomes (unblocks confirmatory resume; removes the missing-prereg bottleneck).
- Enforced event-adequacy rule: no confirmatory run without >0 frozen-test synthetic breaches and pre-freeze label/split justification.
- Consolidated handoffs; eliminated poll/status-only and Track A/C relitigation loops.

## Execution milestones

### M1–M4 — Track C — COMPLETE
Concluded NOT_SUPPORTED; overlay INELIGIBLE.

### M5 — Track B TB2 modeled breach campaign — **ACTIVE / MANDATORY**
Execute per `NEXT_SESSION_TASK.md`:
1. **M5.1 Admissibility+provenance lock:** DONE — `research_state/trackb_TB2_admissibility.json` (machine-verified: 5 symbols, 274 days, 9 blocks, provenance_verified=true, unmapped_count=0).
2. **M5.2 Event-adequate design + freeze BEFORE outcomes:** DONE — label h168_long_10x_m0 (>0 frozen-test positives, all 5 symbols); `research_state/research_protocol_trackb_TB2_20261110T190405Z.md` FROZEN_BEFORE_OUTCOMES; `prereg_hash` + `frozen_before_outcomes=true` + `outcome_values_inspected=false` in `run_manifest.json`.
3. **M5.3 Execute (heavy, DUE NOW):** run frozen Track B pipeline -> `research_state/evaluation_summary_trackb_TB2_20261110T190405.md` (CI, rel change, n_instruments, n_obs, n_test_blocks, gate, Holm, synthetic-proxy caveat). NO post-freeze tuning.
4. **M5.4 Verdict/propagation:** update `hypothesis_registry.json`, `experiment_frontier.json`, `negative_results_report.md`, `AGENT_HANDOFF.md`, `NEXT_SESSION_TASK.md`; state overlay eligibility (NOT ELIGIBLE unless all gates pass); set singular `next_unfinished_task`.

**Acceptance:** frozen prereg+hash before outcomes (DONE); machine-verified admissibility/provenance (DONE); evaluation summary with CIs/blocks and explicit gate verdict (or evidence-backed inadmissibility); registries+handoffs updated.

### M6 — Conclusion or next route — CONDITIONAL
- Gate pass: preregister next confirmatory/overlay-eligibility step (no premature overlay).
- 2024Q1-Q3 and all admissible local routes exhausted/inadmissible with evidence: set `next_unfinished_task: NONE — program concluded under constraints pending new admissible unauthenticated source`; Track A remains STRUCTURALLY_BLOCKED, Track C concluded.
- Another materially different admissible local uninspected route remains: repeat M5 (new ID, new prereg).

## Execution rules
1. Prereg before outcomes. 2. No threshold shopping/holdout reuse. 3. Track B = modeled breach proxy only (never observed liquidations). 4. No fabricated provenance, no network/paid/manual data. 5. Preserve null/inconclusive results. 6. Every session delivers heavy verifiable work. 7. Keep `AGENT_HANDOFF.md` + `NEXT_SESSION_TASK.md` synchronized with one `next_unfinished_task`.

## Canonical verification
```bash
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"
```

## Exit criteria
Only: (1) gate-passing Track B/C result with full evidence and eligible next step preregistered, OR (2) all admissible local Track B/C routes exhausted with preserved results and `next_unfinished_task: NONE` pending new admissible unauthenticated source (Track A structural block documented).
