# FOCUS_CAMPAIGN.md — Heavy-Work Execution Plan

**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Priority (per repo name):** 1) Track B liquidation boundary risk (modeled, synthetic breaches) — **ACTIVE/MANDATORY**; 2) Track C/H1 funding-conditioned volatility forecast — concluded NOT_SUPPORTED; 3) Track A observed liquidations — STRUCTURALLY_BLOCKED.
**Campaign timestamp:** 2026-11-10T19:45:07Z (program NOT concluded — TB2 confirmatory run due)
**Single durable handoff (authoritative initial task):** `NEXT_SESSION_TASK.md` — execute immediately.
**Hard constraints (NON-NEGOTIABLE):** no network/paid/manual/credentialed data; no fabricated provenance/outcomes; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled breach proxy only, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits.

## Mission
Advance to a reproducible, auditable, out-of-sample verdict using only local verified data: (a) funding-conditioned volatility vs RV-only baseline — **concluded NOT_SUPPORTED**; (b) liquidation risk via **Track B modeled boundary breaches** — **MANDATORY NEXT (TB2 confirmatory)**, or record evidence-backed inadmissibility only after exhausting admissible local routes. Future agents must not idle on status docs, polling, or re-litigation of concluded tracks. Every session delivers heavy verifiable work.

## Current state (verified)
- **Track C / H1:** CONCLUDED, **NOT_SUPPORTED**. No untested claim-worthy panels with >=3 blocks remain locally. Risk overlay INELIGIBLE.
- **Track A:** **STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census). Not locally repairable.
- **Track B:** **ACTIVE.** TB1 degenerate/inadmissible (0 test breaches). **TB2 READY for confirmatory execution:** 2024-01-01..2024-09-30 (5 symbols, 274 days, provenance verified), label `h168_long_10x_m0` pre-freeze with >0 frozen-test positives (619/4925, all symbols >0), prereg frozen + hash recorded before outcomes (`research_state/research_protocol_trackb_TB2_20261110T190405Z.md`).

## Bottlenecks removed
- Replaced TB1-stale routing with single mandatory TB2 path in `NEXT_SESSION_TASK.md`.
- Pre-freeze label/split selected with >0 frozen-test positives; prereg frozen + hash recorded before outcomes (unblocks confirmatory resume).
- Event-adequacy rule enforced: no confirmatory run without >0 frozen-test synthetic breaches and pre-freeze label/split justification.
- Consolidated handoffs; eliminated poll/status-only and Track A/C relitigation loops.

## Milestones
- **M1–M4 (Track C):** COMPLETE — concluded NOT_SUPPORTED.
- **M5 (Track B TB2, ACTIVE/MANDATORY):**
  1. M5.1 Admissibility+provenance lock — DONE.
  2. M5.2 Event-adequate design + freeze BEFORE outcomes — DONE.
  3. **M5.3 Execute (DUE NOW, heavy):** run frozen TB2 pipeline (B1 vs C2, LogLoss/Brier, block bootstrap >=2000/30d, Holm, 95% CI) -> `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`. NO post-freeze tuning.
  4. M5.4 Verdict/propagation: update registries + handoffs, state overlay eligibility, set singular `next_unfinished_task`.
- **M6 (Conditional):** gate pass -> preregister next confirmatory/overlay-eligibility step (no premature overlay). All admissible local routes exhausted/inadmissible with evidence -> conclude under constraints (`next_unfinished_task: NONE`, pending new admissible unauthenticated source). Otherwise repeat M5 on next admissible uninspected route (new ID/prereg).

## Execution rules
1. Prereg/freeze before outcomes. 2. No threshold shopping/holdout reuse. 3. Track B = modeled breach proxy only. 4. No fabricated provenance, no network/paid/manual data. 5. Preserve null/inconclusive results. 6. Every session delivers heavy verifiable work. 7. Keep `AGENT_HANDOFF.md` + `NEXT_SESSION_TASK.md` synchronized with one `next_unfinished_task`.

## Canonical verification
```bash
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"
```
