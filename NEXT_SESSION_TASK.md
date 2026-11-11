# NEXT_SESSION_TASK.md — SINGLE DURABLE HANDOFF (INITIAL TASK MESSAGE)

**Timestamp (UTC):** 2026-11-11T01:23:53Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Program status:** `CONCLUDED_UNDER_CONSTRAINTS` — all admissible local routes exhausted with evidence. **No further initial task remains on current local data/design.**

## Repo-name prioritization (authoritative)
Per repo name `Funding-conditioned-volatility-and-liquidation-risk`, both legs are equal priority and both locally concluded under constraints:
1. **Track C/H1 — funding-conditioned volatility:** **NOT_SUPPORTED** (all claim-worthy local panels exhausted: FCLR-003/008/009/012-V/013/014). Overlay INELIGIBLE.
2. **Track B — modeled liquidation boundary breaches (liquidation-risk leg):** **CONFIRMATORY_COMPLETE, NOT_SUPPORTED**. TB1 degenerate (zero test breaches). TB2 (frozen `trackb_TB2_20261110T190405Z`, 2024-01-01..2024-09-30, BTC/ETH/BNB/SOL/XRP, `synthetic_boundary_breach_h168_long_10x_m0`, modeled proxy only): event-adequate but forecast gate NOT_MET (rel Log Loss +1.68% < 2%, 95% CI [-0.010997,0.003094] crosses zero, Holm fails, 2 test blocks <3). Overlay NOT ELIGIBLE. Not observed liquidations.
3. **Track A — observed liquidations:** **STRUCTURALLY_BLOCKED** (no admissible unauthenticated observed-liquidation census). Not locally repairable.

## Initial message for next agentic work session
**SINGULAR NEXT TASK: `NONE` (pending a new admissible unauthenticated source).**

Do not poll. Do not run status-only loops. Do not relitigate concluded tracks. Do not threshold-shop. Do not reuse sealed holdouts. Do not fabricate data/provenance. Heavy work resumes only when a genuinely new admissible unauthenticated source/route exists, and only under the reopen conditions below.

## Reopen conditions (only path to significant new progress)
Start work only with ALL of:
1. **New admissible unauthenticated data source** (no payment/signup/API key/manual/credentialed/bypassed access) with verifiable provenance, schema, coverage, and terms evidence recorded in-repo.
2. **New experiment ID** and a clear claim (Track A observed liquidations, Track B modeled breaches, Track C/H1 volatility, or H2 Shek replication) not already concluded on that panel.
3. **New preregistration/protocol frozen BEFORE any outcome computation**, with hashes/boundaries recorded in `research_state/run_manifest.json`.

If no such source exists, stop cleanly with evidence (no fabricated progress). `NONE` is the task until a new source appears.

## Heavy-work mandate (future agents cannot avoid heavy work)
- Any resumed work must be **heavy, verifiable, and pre-registered before outcomes**.
- No status-only output, no polling, no relitigation, no threshold shopping, no sealed-holdout reuse.
- Deliver verifiable evidence or stop with evidence.

## Hard constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxy only, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits.

## Bottlenecks — current state
**None blocking.** Environment ready (numpy/pandas/scipy installed). Script-scope registry aligned 127/127 (0 missing/extra/bad). Root md+json bound 211 (baseline 144 md + 67 json). `experiment_frontier.json` valid concluded-state. Handoffs consolidated. Canonical verification green (re-run 2026-11-10T23:28Z: 1124 tests OK; 35-test subset OK; PROVENANCE_OK 161, unmapped 0; registry pass True).

## Canonical evidence/artifacts
- Track B: `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`, `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`
- State: `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/experiment_frontier.json`
- Track A block: `research_state/track_a_structural_block.md`, `research_state/liquidation_sources_enumeration.md`, `research_state/alt_source_scan_latest.json`
- Final verdicts: `research_state/final_confirmatory_verdict.md`, `research_state/final_record_closure_audit.md`
- Handoffs: `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` (this file)