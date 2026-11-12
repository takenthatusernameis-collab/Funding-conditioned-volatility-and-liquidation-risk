# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Authoritative handoff timestamp (UTC):** 2026-11-12T09:51:12Z (supersedes all prior handoffs/checkpoints; this file is the sole durable handoff)
**Message time (UTC):** 2026-11-12T09:51:12Z

## Repo-priority P0 (inferred from repository name)
`Funding-conditioned-volatility-and-liquidation-risk` sets priority: **(1) funding-conditioned volatility forecasting (Track C), (2) observed liquidation risk (Track A), (3) modeled boundary breaches (Track B)**. Every session must produce **heavy, claim-advancing work** or a **timestamped evidenced clean stop**. Status-only output, polling, re-probes of already-assessed sources, and cosmetic edits are banned.

## Consolidated verified state (single source of truth)
- **Gate 4 Branch 1 trigger (external/legal):** ABSENT. `research_state/fclr016_local_audit/` contains no `*RESOLVED*` with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation (only BLOCKED/UNRESOLVED + probe artifacts). Agent cannot create/attest/fabricate/bypass; do not wait/poll.
- **Eligibility/monitor:** `research_state/new_data_monitor_probe_20261112T073159Z.{md,json}` → `new_claim_worthy_experiment_eligible_now=false` (ironflow/hyperliquid-liquidations `lastModified=2026-11-07T10:18:25Z`, latest event month `2026-10`, no verified post-2026-10-31 observed labels; HL 2026-11+ depth ~12.0d, <100d/<90d-for-≥3×30d). Not a re-probe target without new evidence.
- **Alt-source discovery completed:** `research_state/alt_source_scan_latest.json` (20261112T075045Z, 22 candidates) and `research_state/alt_source_deep_review_latest.md` (20261112T075134Z, 14 probes) — **no new GO**. Ironflow HF (CC BY 4.0) is the only known admissible Track A source but exhausted for claim-worthy work (events through 2026-10). Do not rerun `hunt_alternative_liquidation_sources.py` / `deep_review_alt_sources.py` without a materially new, unassessed candidate in caches/artifacts.
- **Caches/registry:** `research_state/hf_search_cache.json`, `research_state/data_source_registry_alt_hunt.json`, `research_state/ironflow_fastpath_cache.json`, `research_state/ironflow_monitor_state.json`.
- **Sealed/exhausted (no reopening/relitigation/retune):** Track C ALL confirmatory NOT_SUPPORTED (FCLR-001/002/003/006/007; dossier `research_state/track_c_consolidated_dossier.md`), H001 NOT_SUPPORTED, risk overlay INELIGIBLE. Track A expansion PASS but robustness FRAGILE (LOIO 4/8 need ≥6; Placebo/Permutation FAIL); early INADMISSIBLE (~65d); volatility family/alt-vol/primary NOT_MET; ironflow exhausted (2026-10). Track B ALL NOT_SUPPORTED/NOT_SUPPORTED_DEGENERATE. H2 `H2_shek_replication` EXPLORATORY_ONLY/PARTIAL — no promotion/re-run.
- **Frontier:** `research_state/experiment_frontier.json` — FCLR-NEXT campaign is sole authoritative next task; stale rank-0 entries history only.
- **Offline sanity (unchanged signal):** `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit -v` last recorded 103 tests OK (2026-11-12T08:50:05Z). No resume trigger; probe diff zero.
- **Bottleneck cleanup (this session):** Redundant `session_checkpoint_*.md` files (11 files, 20261112T075428Z–094233Z) removed as checkpoint churn superseded by this handoff. No status-only checkpoints recreated.

## Bottlenecks (current) and removal
| Bottleneck | Agent-removable? | Required removal / trigger |
|---|---|---|
| Gate 4 Branch 1 (Binance terms evidence) | No (external/legal) | Valid `*RESOLVED*` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation in `research_state/fclr016_local_audit/` → execute Branch 1 immediately. |
| HL/ironflow eligibility (depth + post-2026-10-31 labels) | No now | Evidence of HL ≥100d AND verified post-2026-10-31 observed labels → bounded probe + timestamped evidence; if still ineligible, stop (no polling). |
| No new §16-admissible liquidation-label source | No now | A materially new, unassessed candidate (perpetual/futures liquidation labels, ≥5 instruments, ≥1 complete month or ≥3×30d blocks, unauthenticated, provenance/license, observed labels, venue-consistent) evidenced in artifacts/caches. |
| Checkpoint churn / redundant `session_checkpoint_*.md` | YES — REMOVED | 11 redundant checkpoint files deleted; single durable handoff now carries the clean-stop evidence. |

## NEXT FOCUS CAMPAIGN — FCLR-NEXT-HEAVY-OR-CHECKPOINT (execute in strict order)
1. **Gate 4 check (first):** RESOLVED trigger present → execute Branch 1 per protocol, record artifacts, update state atomically. Absent → continue.
2. **Bounded eligibility re-check (only if plausibly changed):** if evidence suggests HL ≥100d and post-2026-10-31 observed labels, run bounded probe and record `research_state/new_data_monitor_probe_<UTC>.{md,json}`. If ineligible → continue (no polling).
3. **Materially-new-source triage:** find candidate not already assessed AND plausibly §5/§16-admissible. If none → step 5.
4. **New candidate only:** bounded smoke/probe, then full §16 admissibility audit BEFORE prereg/outcome computation → emit `research_state/<source>_admissibility_audit_<UTC>.{md,json}`. If admissible: freeze prereg → build panel → evaluate → verdict → atomic state updates under a NEW experiment ID. Never inspect outcomes before prereg freeze.
5. **No eligible path:** this handoff IS the timestamped evidenced clean stop (Gate 4 absent, latest monitor ineligible, no materially new unassessed admissible candidate). **STOP CLEANLY.** Do not rerun assessed discovery, do not poll, no status-only output.

## PRE-STAGED HEAVY WORK — mandatory on ANY resume trigger (future agents cannot avoid heavy work)
The moment ANY resume trigger below fires, the session MUST execute in this order and produce these artifacts before ending:
- (a) Pre-register BEFORE inspecting outcomes: `research_state/experiment_prereg_<UTC>.json` (or `scripts/create_forward_prereg.py`) per `research_state/research_protocol_fclr010.md`, `pre_registered_before_outcomes: true`, `frozen_before_outcomes: true`, primary contrast C2_vs_B1.
- (b) Execute frozen harness: `python scripts/fclr010_harness.py` on the newly eligible data.
- (c) Write `research_state/evaluation_summary_LIQUIDATION_FORWARD_VALIDATE_004_<UTC>.md` with calibration (Brier/reliability), LOO stability, concentration (LOIO), block-bootstrap CIs (≥2000 reps), Holm multiplicity across the registered family, and explicit gate assessment (PASS/NOT_MET with reasons).
- (d) Update `research_state/experiment_frontier.json` with result status and next action.
- (e) Commit evidence (code, manifests, reports — NOT raw data).
Non-skippable per-session checklist: new evidence checked (`research_state/ironflow_monitor_state.json` read, `new_files_found` evaluated) → automation strengthened (`scripts/monitor_ironflow_liquidations.py` and/or `scripts/hunt_alternative_liquidation_sources.py` improved) → tests added/extended (all pass: `python -m unittest discover -s tests -v`) → blocker doc updated (fresh timestamp, complete probe tables, resume conditions) → frontier updated (precise resume triggers) → `AGENT_HANDOFF.md` updated with clear timestamped next task → no sealed artifacts touched, no Track B/C conflation, no `.github/workflows` changes.

## Hard bans (no exceptions)
- No outcome inspection before prereg freeze; no threshold-shopping; no sealed-holdout reuse.
- No Binance/2024 conflation; no modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No polling/waiting. No status-only sessions.
- No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- No reopening/relitigation/retune of sealed verdicts.
- No redundant controllers/schedulers/agents/polling loops/repeated wrappers/endless retries.

## Key references
- `RESEARCH_PROMPT.md` (§5, §16), `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`
- Gate 4: `research_state/fclr016_local_audit/`
- Monitor: `research_state/new_data_monitor_probe_20261112T073159Z.{md,json}`
- Source discovery: `research_state/alt_source_scan_latest.json`, `research_state/alt_source_deep_review_latest.md`, `research_state/hf_search_cache.json`, `research_state/data_source_registry_alt_hunt.json`
- Evidence/closure: `research_state/h002_replication_report.md`, `research_state/structural_closure_verdict_heavy.md`, `research_state/track_c_consolidated_dossier.md`, `research_state/track_c_residual_audit.md`

## Immediate first action (now)
Execute campaign: (1) Gate 4 absent, (2) no plausible new eligibility evidence, (3) no materially new unassessed §16-admissible candidate. All blockers unremovable now → this handoff is the timestamped evidenced clean stop citing Gate 4 absence + probe 20261112T073159Z + alt-source no-GO; redundant checkpoint churn removed. **STOP CLEANLY**. Do not run network probes or rerun assessed discovery.

## Session entry conditions (resume triggers only)
Resume ONLY when: Gate 4 `RESOLVED_VERIFIED` appears; OR HL ≥100d with verified post-2026-10-31 observed labels; OR a genuinely new, unassessed, plausibly §16-admissible liquidation-label source is evidenced. Until then, no session should run. On any trigger, execute the PRE-STAGED HEAVY WORK above in full.

## Redirects
`AGENT_HANDOFF.md`, `NEXT_SESSION_TASK.md`, and `FOCUS_CAMPAIGN.md` are redirects to this file. Read and execute this file only.
