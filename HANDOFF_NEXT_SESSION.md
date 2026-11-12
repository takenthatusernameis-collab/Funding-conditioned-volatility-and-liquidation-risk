# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Authoritative handoff timestamp (UTC):** 2026-11-12T08:53:05Z (supersedes prior handoffs; this file is the sole durable handoff)
**Message time (UTC):** 2026-11-12T08:53:05Z

## Repo-priority P0 (inferred from repository name)
The repository name is `Funding-conditioned-volatility-and-liquidation-risk`. Priority order per the name: **volatility forecasting (Track C) first, then observed liquidation risk (Track A), then modeled boundary breaches (Track B)**. Advance the core claim — funding-conditioned volatility and liquidation risk — with **heavy, claim-advancing work only**: (a) execute Gate 4 Branch 1 on a valid RESOLVED trigger, (b) run §16 admissibility audit (+ prereg/build/eval/verdict if admissible) for a genuinely new liquidation-label source/window, (c) produce bounded eligibility evidence ruling new heavy work in/out, or (d) emit a timestamped checkpoint proving no new eligible work and STOP CLEANLY. Status files, polling, re-probes of already-assessed sources, and cosmetic engineering are NOT heavy work and are banned.

## Consolidated verified state (single source of truth; all redundant session checkpoints and checkpoint commits collapsed into this handoff)
- **Gate 4 Branch 1 trigger:** ABSENT (`research_state/fclr016_local_audit/` contains only `fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json` and `fclr016_v5_terms_evidence_UNRESOLVED_20261108T204000Z.json`; no `*RESOLVED*` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). External/legal blocker — not agent-removable; do not create/attest/fabricate/bypass; do not wait/poll.
- **Eligibility/monitor:** `research_state/new_data_monitor_probe_20261112T073159Z.{md,json}` → `new_claim_worthy_experiment_eligible_now=false` (ironflow/hyperliquid-liquidations `lastModified=2026-11-07T10:18:25Z`, latest event month `2026-10`, no verified post-2026-10-31 observed labels; HL 2026-11+ depth ~12.0d, <100d reprobe/<90d for ≥3×30d blocks). Just-executed ineligible probe — not a re-probe target.
- **Alt-source discovery completed (do not rerun without new unassessed candidate):** `research_state/alt_source_scan_latest.json` (20261112T075045Z, 22 candidates) and `research_state/alt_source_deep_review_latest.md` (20261112T075134Z, 14 probes) — **no new GO sources**. Ironflow HF (CC BY 4.0) is the only known admissible Track A source but is exhausted for claim-worthy work (events through 2026-10).
- **Caches/registry:** `research_state/hf_search_cache.json`, `research_state/data_source_registry_alt_hunt.json`, `research_state/ironflow_fastpath_cache.json`, `research_state/ironflow_monitor_state.json`. Candidates materially covered by latest scan/deep-review are not re-probe targets.
- **Sealed/exhausted (no reopening/relitigation/retune):** metpie 2025Q2 §16 INADMISSIBLE (~65d); TRACKA-HL-EARLY-4H INCONCLUSIVE_PILOT_SHORTFALL; Track A expansion PASS but robustness FRAGILE; volatility family/alt-vol/primary NOT_MET; Track B/C/H1 NOT_SUPPORTED as sealed. H2 `H2_shek_replication` EXPLORATORY_ONLY/PARTIAL with evidence — no promotion/re-run.
- **Frontier:** `research_state/experiment_frontier.json` (single authoritative entry generated 20261112T073418Z) — FCLR-NEXT campaign installed as sole authoritative next task; stale rank-0 entries preserved as history only. Not relitigated.
- **Offline sanity check (re-run 2026-11-12T08:50:05Z):** `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit -v` → **103 tests OK**. No resume trigger; `data_through=2026-10`; probe diff zero; baseline drift intact.

## Bottlenecks and required removal (execute, do not stall)
| Bottleneck | Nature | Removal action |
|---|---|---|
| Gate 4 Branch 1 (Binance terms evidence) | External/legal, absent | Execute Branch 1 immediately only on valid RESOLVED trigger (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). Agent cannot create/attest/fabricate. If absent, proceed to next step; never poll/wait/bypass. **Not agent-removable — requires resume trigger.** |
| HL 2026-11+ depth / post-2026-10-31 labels | Ineligible now (evidenced) | Re-check only when plausibly eligible (HL ≥100d AND verified post-2026-10-31 observed labels) with a bounded probe + timestamped evidence; if still ineligible, no polling, no status-only. **Not agent-removable now — requires resume trigger.** |
| Assessed alt-source space | Completed, no GO | Do not rerun `hunt_alternative_liquidation_sources.py` / `deep_review_alt_sources.py` unless a materially new, plausibly admissible liquidation-label candidate appears unassessed in latest artifacts/caches. |
| Redundant session checkpoints / checkpoint commits | Inefficiency, noise | Collapsed into this single durable handoff. Prior session_checkpoint_*.md and `chore(kilo): checkpoint agent session` commits are superseded; do not recreate. |

All bottlenecks are currently **unremovable by the agent**; the correct session behavior is the evidenced clean stop below, not idle polling.

## NEXT FOCUS CAMPAIGN — FCLR-NEXT-HEAVY-OR-CHECKPOINT (strict order, heavy-work mandate)
1. **Gate 4 check (first):** valid RESOLVED trigger present → execute Branch 1 per protocol, record artifacts, update state atomically. Absent → continue.
2. **Bounded eligibility re-check (only if plausible):** if wall-clock/evidence suggests HL ≥100d and post-2026-10-31 observed labels, run bounded HL/ironflow probe and record `research_state/new_data_monitor_probe_<UTC>.{md,json}` (or equivalent). If ineligible → continue (no polling).
3. **Materially-new-source triage:** inspect caches/artifacts for a candidate not already assessed AND plausibly meeting §5/§16 (perpetual/futures liquidation labels, ≥5 instruments, ≥1 complete month or ≥3×30d blocks, unauthenticated, provenance/license, observed labels, venue-consistent). If none → step 5.
4. **New candidate only:** bounded smoke/probe, then full §16 admissibility audit BEFORE any prereg/outcome computation; emit `research_state/<source>_admissibility_audit_<UTC>.{md,json}`. If admissible: freeze prereg → build panel → evaluate → verdict → atomic state updates under a NEW experiment ID. Never inspect outcomes before prereg freeze.
5. **No eligible path:** emit `research_state/session_checkpoint_<UTC>.md` documenting evidence reviewed (Gate 4 absent, latest monitor ineligible, no materially new unassessed admissible candidate) and STOP CLEANLY. **Every session must end in heavy progress or an evidenced clean stop — never status-only.**

## Hard bans (no exceptions)
- No outcome inspection before prereg freeze; no threshold-shopping; no sealed-holdout reuse.
- No Binance/2024 conflation; no modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No polling/waiting. No status-only sessions.
- No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- No reopening/relitigation/retune of sealed verdicts.
- No redundant controllers, schedulers, agents, polling loops, status-only files, repeated wrappers, or endless retry loops. Every iteration must create measurable research, data, testing, or engineering progress.

## Key references
- `RESEARCH_PROMPT.md` (§5, §16), `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`
- Gate 4: `research_state/fclr016_local_audit/`, `research_state/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`
- Monitor: `research_state/new_data_monitor_probe_20261112T073159Z.{md,json}`
- Source discovery: `research_state/alt_source_scan_latest.json`, `research_state/alt_source_deep_review_latest.md`, `research_state/hf_search_cache.json`, `research_state/data_source_registry_alt_hunt.json`
- H2 evidence: `research_state/h002_replication_report.md`, `research_state/h002_run_record.json`
- Structural closure: `research_state/structural_closure_verdict_heavy.md`
- Track C dossier: `research_state/track_c_consolidated_dossier.md`

## Immediate first action (now)
Gate 4 absent → eligibility ineligible (evidenced) → no materially new unassessed §16-admissible candidate → all five campaign steps executed → write `research_state/session_checkpoint_20261112T085305Z.md` (evidence: Gate 4 absent, probe 20261112T073159Z ineligible, alt-source scan/review no new GO, offline sanity 103 tests OK) and STOP CLEANLY. No network probes needed; offline sanity already verified.

## Session entry conditions (resume triggers only)
Resume ONLY when a materially different condition obtains:
- Gate 4 `RESOLVED_VERIFIED` trigger appears (human/legal attestation, `fabricated=false`)
- HL depth ≥100d AND verifiable post-2026-10-31 observed liquidation labels appear
- A genuinely new, unassessed, plausibly §16-admissible liquidation-label source is evidenced (perpetual/futures, ≥5 instruments, ≥1 complete month or ≥3×30d blocks, unauthenticated, provenance/license, observed labels, venue-consistent)

Until then: **no session should run**. Every session must produce heavy progress or an evidenced clean stop.

## Redirects (single durable handoff)
`AGENT_HANDOFF.md`, `NEXT_SESSION_TASK.md`, and `FOCUS_CAMPAIGN.md` are redirects to this file. Read and execute this file only.