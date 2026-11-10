# AGENT_HANDOFF.md — Durable Handoff Pointer

**Timestamp (UTC):** 2026-11-10T20:00:21Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Single durable handoff (authoritative initial task):** `NEXT_SESSION_TASK.md` — **execute immediately**.
**Program status:** `CONCLUDED_UNDER_CONSTRAINTS` — all admissible local routes exhausted with evidence. NOT concluded by user request; concluded by evidence.

## Current state (verified)
- **Priority 1 — Track B (modeled liquidation boundary breaches): CONFIRMATORY_COMPLETE, verdict NOT_SUPPORTED.**
  - TB1 degenerate/inadmissible (0 test breaches; `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`).
  - **TB2 confirmatory DONE:** `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md` on frozen panel 2024-01-01..2024-09-30 (BTC/ETH/BNB/SOL/XRP), label `synthetic_boundary_breach_h168_long_10x_m0`. Event-adequate: test 619/5040 positives (12.3%), all 5 symbols >0. Prereg freeze-integrity RESOLVED: manifest `prereg_hash` corrected to canonical file sha256 `46dcfb56c279e853230e75f6cb246ed878d765d2b399ea9a2e21c41581194adb` (was `9de16e7d...`); `frozen_before_outcomes=true`, `outcome_values_inspected=false`; provenance `PROVENANCE_OK 161`, unmapped 0.
  - Results: pooled Log Loss B1=0.292447 → C2=0.287540 = **+1.68% relative reduction (<2% materiality floor, NOT_MET)**; 95% CI [-0.010997, 0.003094] crosses zero (NOT_MET); p=0.488; Holm across 2 metrics FAILS; only 2 non-overlapping 30-day test blocks (<3, NOT_MET). **Forecast gate: NOT_MET.**
  - **Overlay: NOT ELIGIBLE.** Null result preserved; no threshold shopping; no sealed-holdout reuse; Track B = modeled synthetic breach proxy only, never observed liquidations.
- **Priority 2 — Track C / H1:** concluded **NOT_SUPPORTED** (all claim-worthy local panels exhausted; FCLR-003/008/009/012-V/013/014). Overlay INELIGIBLE.
- **Priority 3 — Track A (observed liquidations):** **STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census). Not locally repairable.

## Bottlenecks removed / surfaced
- Removed: TB1-stale routing, missing event-adequate design, missing pre-outcome prereg record, handoff fragmentation/polling, prereg hash-integrity mismatch (resolved step 0), stale `run_trackb_evaluation.py` (wrong window/label/fabricated metric) replaced by `scripts/run_trackb_tb2_evaluation.py` implementing the frozen TB2 protocol.
- No remaining uninspected admissible local route. All Track A/B/C routes executed or structurally blocked/concluded.

## `next_unfinished_task` (singular)
**NONE — program concluded under constraints pending a new admissible unauthenticated source.**
Evidence: Track A STRUCTURALLY_BLOCKED; Track C/H1 concluded NOT_SUPPORTED; Track B TB2 confirmatory gate NOT_MET (rel Log Loss +1.68% < 2% floor, CI crosses zero, Holm fails, 2 test blocks <3); Track B TB1 degenerate/inadmissible. No threshold shopping or sealed-holdout reuse permitted. Do not poll; do not produce status-only output; do not relitigate concluded tracks. A future session may reopen only with a new admissible unauthenticated data source, a new experiment ID, and a new prereg frozen before outcomes.

## Constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxies only, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits. Heavy, verifiable progress only.
