# FOCUS_CAMPAIGN — Heavy-Work Execution Plan (Pointer)

**Timestamp (UTC):** 2026-11-11T04:34:40Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Program status:** `CONCLUDED_UNDER_CONSTRAINTS`
**Single durable handoff (authoritative initial task):** `NEXT_SESSION_TASK.md` → **SINGULAR NEXT TASK: `NONE`** pending a new admissible unauthenticated source.

## Repo-name prioritized outcome (closed under constraints)

1. **Funding-conditioned volatility (Track C/H1):** NOT_SUPPORTED on all claim-worthy local panels. `research_state/final_confirmatory_verdict.md`
2. **Modeled liquidation boundary breaches (Track B, proxy only):** CONFIRMATORY_COMPLETE, NOT_SUPPORTED (TB1 degenerate; TB2 gate NOT_MET). `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`
3. **Observed liquidations (Track A):** STRUCTURALLY_BLOCKED. `research_state/track_a_structural_block.md`

## Bottlenecks

**None blocking.** Registry/provenance/environment green; handoffs consolidated to `NEXT_SESSION_TASK.md`.

## Next campaign — only if reopened (heavy work required)

Execute only when **all** reopen conditions in `NEXT_SESSION_TASK.md` hold:
- Ingest/verify new admissible unauthenticated source with provenance/schema/coverage/terms evidence in-repo.
- Define new experiment ID and non-concluded claim; freeze preregistration/protocol (hashes/boundaries in `research_state/run_manifest.json`) **before any outcome computation**.
- Run pre-registered evaluation with leakage/split/integrity checks; produce auditable verdict artifacts and atomically update frontier/registry/manifest.

**Forbidden:** status-only work, polling, relitigation, threshold shopping, sealed-holdout reuse, Track A/B/C conflation, fabricated provenance, network/paid/manual/credentialed/bypassed data, overlay before forecast gate, `.github/workflows` edits.

If reopen conditions are not met: **stop with evidence (`NONE`).** No exceptions.
