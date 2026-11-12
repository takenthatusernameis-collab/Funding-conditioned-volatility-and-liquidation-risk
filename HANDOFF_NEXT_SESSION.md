# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk)
**Handoff timestamp (UTC):** 2026-11-12T08:32:31Z (supersedes prior handoffs; this file is the sole authoritative handoff)
**Status:** AUTHORITATIVE — execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. No competing root handoff files.

## Non-negotiable execution contract
Do real, heavy, claim-advancing work in every session: (a) execute Gate 4 Branch 1 if a valid RESOLVED trigger exists, OR (b) perform §16 admissibility audit (+ prereg/build/eval/verdict if admissible) for a genuinely new liquidation-label source/window, OR (c) produce bounded eligibility evidence that rules in/out new heavy work, OR (d) emit a timestamped checkpoint proving no new eligible work and STOP CLEANLY. **No status-only output. No polling. No repeated no-op probes/hunts.**

## Verified state (as of 2026-11-12T08:31:02Z)
- **Gate 4 Branch 1 trigger:** ABSENT (verified: no `*RESOLVED*` artifact in `research_state/fclr016_local_audit/` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). External/legal; not agent-removable. Do not wait.
- **Monitor/eligibility:** `research_state/new_data_monitor_probe_20261112T073159Z.{md,json}` — `new_claim_worthy_experiment_eligible_now=false`. Ironflow/hyperliquid-liquidations `lastModified=2026-11-07T10:18:25Z`, latest event month `2026-10`, no verified post-2026-10-31 observed labels; HL 2026-11+ depth ~12.0d (<100d reprobe, <90d for ≥3×30d blocks).
- **Alt-source discovery (Step 2) completed:** `research_state/alt_source_scan_latest.json` (20261112T075045Z, 22 candidates incl. live HF-discovered) and `research_state/alt_source_deep_review_latest.md` (20261112T075134Z, 14 fresh probes). **Result: NO NEW GO sources.** Probed unauthenticated sources require auth, 404/403, are libraries/not datasets, or lack structured liquidation census data. Ironflow/hyperliquid-liquidations (HF, CC BY 4.0, unauthenticated) remains the only known admissible Track A source found but is EXHAUSTED for claim-worthy work (events through 2026-10).
- **Caches/registry:** `research_state/hf_search_cache.json`, `research_state/data_source_registry_alt_hunt.json`, `research_state/ironflow_fastpath_cache.json`, `research_state/ironflow_monitor_state.json`. Any candidate not materially new vs assessed findings in latest scan/deep-review is not a basis for re-probing.
- **Sealed/exhausted (do not reopen):** metpie 2025Q2 §16 INADMISSIBLE (~65d < 90d); TRACKA-HL-EARLY-4H INCONCLUSIVE_PILOT_SHORTFALL; Track A expansion PASS but robustness FRAGILE; volatility family/alt-vol/primary NOT_MET; Track B/C/H1 NOT_SUPPORTED as sealed; cached-data designs exhausted. H2 `H2_shek_replication` EXPLORATORY_ONLY/PARTIAL with evidence (`research_state/h002_replication_report.md`, `h002_run_record.json`) — no promotion/re-run.

## Bottlenecks and removal (what to do instead of stalling)
| Bottleneck | Status | Required action |
|---|---|---|
| Gate 4 Branch 1 (Binance terms evidence) | EXTERNAL/LEGAL | Execute Branch 1 immediately only on valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). Never create/attest/bypass. |
| HL 2026-11+ depth / post-2026-10-31 labels | Ineligible now (evidenced) | Re-check only when plausibly eligible (HL ≥100d AND verified post-2026-10-31 observed labels). Bounded probe + timestamped evidence; no polling. |
| Sealed/cached designs | Exhausted | No relitigation/retune/reopen. Claim-worthy work requires a genuinely new admissible source/window per RESEARCH_PROMPT §16. |
| Alt-source discovery for assessed candidates | Completed | Do NOT re-run `hunt_alternative_liquidation_sources.py` or `deep_review_alt_sources.py` unless a materially new, plausibly admissible liquidation-label candidate appears unassessed in latest artifacts. |

## NEXT FOCUS CAMPAIGN — execute in strict order
1. **Gate 4 check (first):** valid RESOLVED trigger present → execute Branch 1 per protocol, record artifacts, update state atomically. Absent → continue.
2. **Bounded eligibility re-check (only if plausible):** if wall-clock/evidence suggests HL ≥100d and post-2026-10-31 observed labels, run bounded HL/ironflow probe and record `research_state/new_data_monitor_probe_<UTC>.{md,json}` (or equivalent). If still ineligible → do not poll.
3. **Materially-new-source triage:** inspect caches for a candidate not already assessed AND plausibly meeting §5/§16 (perpetual/futures liquidation labels, ≥5 instruments, ≥1 complete month or ≥3×30d blocks, unauthenticated, provenance/license, observed labels, venue-consistent). If none → step 5.
4. **If new candidate found:** bounded smoke/probe, then full §16 admissibility audit BEFORE any prereg/outcome computation; emit `research_state/<source>_admissibility_audit_<UTC>.{md,json}`. If admissible: freeze prereg → build panel → evaluate → verdict → atomic state updates under a NEW experiment ID. Never inspect outcomes before prereg freeze. No threshold-shopping; no sealed-holdout reuse.
5. **If no trigger, no plausible eligibility, and no materially new admissible candidate:** emit timestamped checkpoint (`research_state/session_checkpoint_<UTC>.md` or update handoff state) documenting evidence reviewed and STOP CLEANLY.

## Hard bans (binding)
- No outcome inspection before prereg freeze; no threshold-shopping; no sealed-holdout reuse.
- No Binance/2024 conflation; no modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No redundant polling/waiting.
- No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- No relitigation/retune of sealed verdicts. No status-only sessions.

## Key references
- Protocol/state: `RESEARCH_PROMPT.md` (§5, §16), `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`
- Gate 4: `research_state/fclr016_local_audit/`, `research_state/fclr016_v5_terms_evidence_BLOCKED_20261108T014835Z.json`
- Monitor/probes: `research_state/new_data_monitor_probe_20261112T073159Z.{md,json}`
- Source discovery: `research_state/alt_source_scan_latest.json`, `research_state/alt_source_deep_review_latest.md`, `research_state/hf_search_cache.json`, `research_state/data_source_registry_alt_hunt.json`
- H2 evidence: `research_state/h002_replication_report.md`, `research_state/h002_run_record.json`

## Immediate first action
Gate 4 check → absent. HL/ironflow plausibility → ineligible now per latest probe. Triage caches for materially new unassessed admissible candidate; if none exists, write timestamped checkpoint evidence and STOP CLEANLY. Before any network probe run offline sanity: `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit -v`.
