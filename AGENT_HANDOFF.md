# AGENT_HANDOFF.md — Durable Handoff Pointer

**Timestamp (UTC):** 2026-11-10T19:40:11Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Single durable handoff (authoritative initial task):** `NEXT_SESSION_TASK.md` — **execute immediately**.
**Program status:** `ACTIVE_TRACKB_MANDATORY` — NOT concluded.

## Current state (verified)
- **Priority 1 — Track B (modeled liquidation boundary breaches): ACTIVE.** TB1 (`TRACKB-MODELED-BREACH-TB1-20261110T173838Z`, 2025-01-01..2026-10-31, 5x/24h long) **DEGENERATE/INADMISSIBLE** (frozen test split had 0 synthetic breaches). Prior `TRACKB-20251110T154307Z` NOT_MET/NOT_SUPPORTED. **TB2 in progress:** 2024-01-01..2024-09-30 (BTC/ETH/BNB/SOL/XRP), label `synthetic_boundary_breach_h168_long_10x_m0` selected pre-freeze (test: 619/4925 positives, all 5 symbols >0; see `research_state/trackb_TB2_label_design_scan.json`). **FROZEN prereg** `research_state/research_protocol_trackb_TB2_20261110T190405Z.md` + `prereg_hash=9de16e7d2b2c80f6ac57d87b6eb150c145bfe9f3168d7ac3d94472f740f7b91f` recorded in `research_state/run_manifest.json` (`split_boundaries_trackb_TB2_20261110T190405Z.frozen_before_outcomes=true`, `outcome_values_inspected=false`) **BEFORE outcomes**. Splits: train 2024-01-01..2024-06-12 / val 2024-06-19..2024-08-06 / test 2024-08-13..2024-09-30 (7d purge/embargo).
- **Starting evidence (machine-verified):** `research_state/trackb_TB2_admissibility.json` (5 symbols, 274 days, 9 blocks, required_series_complete, provenance_verified=true, unmapped_count=0), `research_state/trackb_TB2_admissibility_2024q1q3.json`, `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`.
- **Priority 2 — Track C / H1:** concluded **NOT_SUPPORTED** on claim-worthy local panels; no untested claim-worthy panels with >=3 blocks remain (`next_unfinished_task (Track C): NONE`).
- **Priority 3 — Track A (observed liquidations):** **STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census).
- **Risk overlay:** **INELIGIBLE** until a forecast gate passes under frozen prereg.
- **Provenance:** `PROVENANCE_OK` verified for TB2 inputs (adjacent sha256 sidecars + manifest lineage). Re-verify for all TB2 inputs at confirmatory run.

## Bottlenecks removed
- TB1-stale/ambiguous routing replaced with single mandatory TB2 path; TB1 reframed as event-adequacy failure.
- Pre-freeze label/split selected with >0 frozen-test positives; prereg frozen + hash recorded before outcomes (unblocks confirmatory resume).
- No polling/status-only work; no relitigation of concluded tracks.

## `next_unfinished_task` (singular)
Execute Track B TB2 confirmatory evaluation on frozen panel 2024-01-01..2024-09-30 per `NEXT_SESSION_TASK.md`: run `scripts/run_trackb_evaluation.py` + `scripts/synthetic_boundary_labels.py` adapted to TB2 ID/window/label on the frozen splits (NO post-freeze tuning), write `research_state/evaluation_summary_trackb_TB2_20261110T190405.md` (point estimate, 95% CI, relative change, n_instruments, n_obs, n_test_blocks, Holm, gate verdict, synthetic-proxy caveat), then propagate verdict to `hypothesis_registry.json`, `experiment_frontier.json`, `negative_results_report.md`, `AGENT_HANDOFF.md`, `NEXT_SESSION_TASK.md`; state overlay eligibility (NOT ELIGIBLE unless gate passes); set singular next task. Fallback only if 2024Q1-Q3 proven inadmissible with evidence (pivot to next locally admissible uninspected route, new ID/prereg).

## Constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxies, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits. Heavy, verifiable progress only.

(End of file - total 25 lines)