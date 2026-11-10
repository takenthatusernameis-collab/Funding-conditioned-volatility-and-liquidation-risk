# FOCUS_CAMPAIGN.md — Heavy-Work Execution Plan

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Priority (per repo name):** 1) Track B liquidation boundary risk (modeled, synthetic breaches) — **ACTIVE/MANDATORY**; 2) Track C/H1 funding-conditioned volatility forecast — concluded NOT_SUPPORTED; 3) Track A observed liquidations — STRUCTURALLY_BLOCKED.
**Campaign timestamp:** 2026-11-10T20:00:21Z (program CONCLUDED_UNDER_CONSTRAINTS — TB2 confirmatory executed, gate NOT_MET, all admissible local routes exhausted)
**Single durable handoff (authoritative initial task):** `NEXT_SESSION_TASK.md` — program concluded; singular next task is `NONE — pending a new admissible unauthenticated source`.
**Hard constraints (NON-NEGOTIABLE):** no network/paid/manual/credentialed data; no fabricated provenance/outcomes; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled breach proxy only, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits.

## Mission
Advance to a reproducible, auditable, out-of-sample verdict using only local verified data: (a) funding-conditioned volatility vs RV-only baseline — **concluded NOT_SUPPORTED**; (b) liquidation risk via **Track B modeled boundary breaches** — **MANDATORY NEXT (TB2 confirmatory)**, or record evidence-backed inadmissibility only after exhausting admissible local routes. Future agents must not idle on status docs, polling, or re-litigation of concluded tracks. Every session delivers heavy verifiable work.

## Current state (verified)
- **Track C / H1:** CONCLUDED, **NOT_SUPPORTED**. No untested claim-worthy panels with >=3 blocks remain locally. Risk overlay INELIGIBLE.
- **Track A:** **STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census). Not locally repairable.
- **Track B:** **CONFIRMATORY_COMPLETE, verdict NOT_SUPPORTED.** TB1 degenerate/inadmissible (0 test breaches). **TB2 confirmatory executed on frozen prereg (2024-01-01..2024-09-30, h168_long_10x_m0): event-adequate (test 619/5040 positives, all 5 symbols >0) but forecast gate NOT_MET — pooled Log Loss B1=0.292447 → C2=0.287540 = +1.68% (<2% floor), 95% CI [-0.010997, 0.003094] crosses zero, Holm FAILS (p=0.488), only 2 test blocks (<3). Overlay INELIGIBLE. Null result preserved; no threshold shopping.**

## Bottlenecks removed
- Replaced TB1-stale routing with single mandatory TB2 path in `NEXT_SESSION_TASK.md`.
- Pre-freeze label/split selected with >0 frozen-test positives; prereg frozen + hash recorded before outcomes (unblocks confirmatory resume).
- Prereg freeze-integrity mismatch resolved: manifest hash corrected to canonical file sha256 before outcomes.
- Stale `run_trackb_evaluation.py` (wrong window/label/fabricated `rel_reduction`) replaced by `scripts/run_trackb_tb2_evaluation.py` implementing the frozen TB2 protocol.
- Event-adequacy rule enforced; confirmatory run executed with no post-freeze tuning.
- Consolidated handoffs; eliminated poll/status-only and Track A/C relitigation loops. All admissible local routes exhausted.

## Milestones
- **M1–M4 (Track C):** COMPLETE — concluded NOT_SUPPORTED.
- **M5 (Track B TB2, EXECUTED):**
  1. M5.1 Admissibility+provenance lock — DONE.
  2. M5.2 Event-adequate design + freeze BEFORE outcomes — DONE (hash-integrity blocker resolved step 0).
  3. **M5.3 Execute — DONE:** ran frozen TB2 pipeline (B1 vs C2, LogLoss/Brier, block bootstrap >=2000/30d, Holm, 95% CI) -> `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`. NO post-freeze tuning. Result: gate NOT_MET, verdict NOT_SUPPORTED.
  4. **M5.4 Verdict/propagation — DONE:** updated registries + manifest + handoffs; overlay eligibility NOT ELIGIBLE; singular `next_unfinished_task` set to NONE.
- **M6 (Conditional):** gate NOT_MET and all admissible local routes exhausted (Track A blocked, Track C concluded, Track B TB1 degenerate + TB2 gate NOT_MET). Program **CONCLUDED_UNDER_CONSTRAINTS** pending a new admissible unauthenticated source. `next_unfinished_task: NONE`. No new prereg/overlay without a new admissible source + new experiment ID + freeze before outcomes.

## Execution rules
1. Prereg/freeze before outcomes. 2. No threshold shopping/holdout reuse. 3. Track B = modeled breach proxy only. 4. No fabricated provenance, no network/paid/manual data. 5. Preserve null/inconclusive results. 6. Program concluded under constraints; future sessions reopen only with new admissible unauthenticated source + new ID + new frozen prereg. 7. Keep `AGENT_HANDOFF.md` + `NEXT_SESSION_TASK.md` synchronized with singular `next_unfinished_task`.

## Canonical verification
```bash
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"
```
