# AGENT_HANDOFF.md — Durable Handoff Pointer

**Timestamp (UTC):** 2026-11-10T19:45:07Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Single durable handoff (authoritative initial task):** `NEXT_SESSION_TASK.md` — **execute immediately**.
**Program status:** `ACTIVE_TRACKB_MANDATORY` — NOT concluded.

## Current state (verified)
- **Priority 1 — Track B (modeled liquidation boundary breaches): ACTIVE.** TB1 degenerate/inadmissible (0 test breaches). **TB2 confirmatory DUE:** 2024-01-01..2024-09-30 (BTC/ETH/BNB/SOL/XRP), label `synthetic_boundary_breach_h168_long_10x_m0` (pre-freeze test: 619/4925 positives, all 5 symbols >0), splits train 2024-01-01..2024-06-12 / val 2024-06-19..2024-08-06 / test 2024-08-13..2024-09-30 (7d purge/embargo). Prereg: `research_state/research_protocol_trackb_TB2_20261110T190405Z.md`; manifest: `split_boundaries_trackb_TB2_20261110T190405Z` in `research_state/run_manifest.json`. Admissibility/provenance: `research_state/trackb_TB2_admissibility.json` (provenance_verified true). Funding cache provenance recheck: `PROVENANCE_OK 161` (unmapped 0).
- **Integrity blocker (must resolve before outcomes):** protocol sha256 `46dcfb56c279e853230e75f6cb246ed878d765d2b399ea9a2e21c41581194adb` != manifest `prereg_hash` `9de16e7d2b2c80f6ac57d87b6eb150c145bfe9f3168d7ac3d94472f740f7b91f`. Reconcile transparently (correct hash with evidence or refreeze with new ID/hash) before confirmatory outcome computation.
- **Priority 2 — Track C / H1:** concluded **NOT_SUPPORTED** (all claim-worthy local panels exhausted). Overlay INELIGIBLE.
- **Priority 3 — Track A (observed liquidations):** **STRUCTURALLY_BLOCKED**.

## Bottlenecks removed / surfaced
- Removed: TB1-stale routing, missing event-adequate design, missing pre-outcome prereg record, handoff fragmentation/polling.
- Surfaced for immediate fix: prereg hash-integrity mismatch (explicit step 0 in `NEXT_SESSION_TASK.md`).

## `next_unfinished_task` (singular)
Resolve TB2 prereg freeze-integrity (step 0), then execute TB2 confirmatory evaluation on frozen panel per `NEXT_SESSION_TASK.md` (B1 vs C2, LogLoss/Brier, block bootstrap >=2000/30d, Holm, 95% CI, breach counts), write evaluation summary + manifest entry, propagate verdict to registries/handoffs, state overlay eligibility, and set singular next task (or conclude under constraints with evidence if all local routes exhausted/inadmissible).

## Constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxies, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits. Heavy, verifiable progress only.
