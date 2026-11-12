# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk)
**Handoff timestamp (UTC):** 2026-11-12T07:54:28Z (supersedes 2026-11-12T07:52:10Z; this file is the sole authoritative handoff)
**Status:** AUTHORITATIVE — execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. No competing root handoff files.

## Verified state (this handoff session)
- **Gate 4 Branch 1 trigger:** ABSENT (verified `research_state/fclr016_local_audit/` has no `*RESOLVED*` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). External/legal; not agent-removable. Do not wait/poll.
- **Bounded monitor probe:** `research_state/new_data_monitor_probe_20261112T073159Z.{md,json}` — ineligible now (`new_claim_worthy_experiment_eligible_now=false`): ironflow/hyperliquid-liquidations `lastModified=2026-11-07T10:18:25Z`, latest event month `2026-10`, no verified post-2026-10-31 observed labels; HL 2026-11+ depth ~12.0d (<100d reprobe, <90d for ≥3×30d blocks).
- **FCLR-NEXT Step 2 (heavy work) COMPLETED prior session:** `research_state/alt_source_scan_latest.json` (generated_utc=20261112T075045Z, 22 candidates incl. live HF-discovered) and `research_state/alt_source_deep_review_latest.md` (TIMESTAMP=20261112T075134Z, 14 fresh probes, 0 cache hits). **Result: NO NEW GO sources identified.** Tested unauthenticated sources require auth, 404/403, are libraries/not datasets, or lack structured liquidation census data. Ironflow/hyperliquid-liquidations (HF, CC BY 4.0, unauthenticated) remains the only known admissible Track A source found so far but is EXHAUSTED for claim-worthy work (events through 2026-10; HL 2026-11+ ~12d).
- **Sealed/exhausted (do not reopen):** metpie 2025Q2 §16 INADMISSIBLE (~65d < 90d); TRACKA-HL-EARLY-4H INCONCLUSIVE_PILOT_SHORTFALL; Track A expansion PASS but robustness FRAGILE; volatility family/alt-vol/primary NOT_MET; Track B/C/H1 NOT_SUPPORTED as sealed; all cached-data designs exhausted. H2 `H2_shek_replication` is EXPLORATORY_ONLY/PARTIAL with evidence (`research_state/h002_replication_report.md`, `h002_run_record.json`) — no promotion/re-run.
- **Caches present:** `research_state/hf_search_cache.json` (generated_utc=2026-11-12T07:50:45.770102Z), `research_state/data_source_registry_alt_hunt.json`. Any candidate not materially new vs already-assessed probes/findings in `alt_source_deep_review_latest.md` and `alt_source_scan_latest.json` is not a basis for re-probing.

## Bottlenecks — status and removal
| Bottleneck | Status | Removal/action |
|---|---|---|
| Gate 4 Branch 1 (Binance terms evidence) | EXTERNAL/LEGAL, blocked | Execute Branch 1 only on valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). Agent must not create/attest/bypass. Isolated; no waiting/polling. |
| HL 2026-11+ depth & no post-2026-10-31 observed labels | Not eligible now (evidenced) | Re-check HL/ironflow only when plausibly eligible (HL ≥100d AND verified post-2026-10-31 observed labels). No polling. |
| Cached/sealed designs exhausted | Exhausted | No relitigation/retune/reopen. Only genuinely new admissible source/window per RESEARCH_PROMPT §16 can open claim-worthy work. |
| Alternative-source discovery (current cache/registry) | Completed for probed/assessed candidates | No re-run of `hunt_alternative_liquidation_sources.py` or `deep_review_alt_sources.py` unless a materially new, plausibly admissible liquidation-label candidate appears that is not already assessed in `alt_source_deep_review_latest.md` (20261112T075134Z) / `alt_source_scan_latest.json` (20261112T075045Z). |

## NEXT FOCUS CAMPAIGN — FCLR-NEXT-CHECKPOINT (execute in order; heavy work only when newly eligible)
Each session must deliver: (a) Gate 4 Branch 1 if triggered, OR (b) §16 admissibility audit (+ prereg/build/eval/verdict only if source passes) for a genuinely new source, OR (c) bounded eligibility evidence + clean stop, OR (d) timestamped checkpoint proving no new eligible work. No status-only output.

1. **Gate 4 check (first):** if valid RESOLVED trigger appears → execute Branch 1 immediately per protocol; record artifacts and atomic state updates. If absent → continue.
2. **Bounded eligibility re-check (only if plausible):** verify HL/ironflow only when wall-clock/new evidence makes eligibility plausible (HL ≥100d AND verified post-2026-10-31 observed labels). Use bounded probes; record timestamped evidence. If ineligible → do not poll.
3. **New-source triage (only if materially new candidate exists):** inspect `hf_search_cache.json` / `data_source_registry_alt_hunt.json` for a candidate that is (i) not already assessed in latest scan/deep-review artifacts, (ii) plausibly a perpetual/futures liquidation-label source relevant to repo focus, and (iii) potentially meeting §5/§16 minima (≥5 instruments, ≥1 complete month or ≥3 non-overlapping 30-day blocks, unauthenticated, provenance/license, observed labels, venue-consistent). If none → stop cleanly with checkpoint. If found → run bounded smoke/probe and full §16 admissibility audit BEFORE any preregistration or outcome computation; emit `research_state/<source>_admissibility_audit_<UTC>.{md,json}`.
4. **If admissible:** freeze prereg → build panel → evaluate → verdict → atomic state updates under a NEW experiment ID. Never inspect outcomes before prereg freeze. No threshold-shopping; no sealed-holdout reuse.
5. **If no trigger, no plausible eligibility, and no materially new admissible candidate:** emit timestamped checkpoint (this handoff + optional `research_state/session_checkpoint_<UTC>.md`) and STOP CLEANLY. No repeated no-op probes.

## Hard bans (binding)
- No outcome inspection before prereg freeze; no threshold-shopping; no sealed-holdout reuse.
- No Binance/2024 conflation; no modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No redundant polling. No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- No relitigation/retune of sealed verdicts. No status-only session output.

## Key references
- Monitor probe: `research_state/new_data_monitor_probe_20261112T073159Z.{md,json}`
- Source discovery: `research_state/alt_source_scan_latest.json`, `research_state/alt_source_deep_review_latest.md`, `research_state/hf_search_cache.json`, `research_state/data_source_registry_alt_hunt.json`
- Protocol/state: `RESEARCH_PROMPT.md` (§5, §16), `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/fclr016_local_audit/`
- H2 evidence: `research_state/h002_replication_report.md`, `research_state/h002_run_record.json`

## Execution contract (first action now)
Gate 4 check → absent → HL/ironflow plausibility check → not plausible now → triage caches for materially new, plausibly admissible unassessed candidate → if none, stop cleanly with this checkpoint. Before any network probe, run offline sanity: `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit -v`.
