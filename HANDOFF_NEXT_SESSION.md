# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk — repo-name-prioritized; neither track subordinated to the other)
**Handoff timestamp (UTC):** 2026-11-12T07:47:40Z (supersedes 2026-11-12T07:38:10Z; this file is the sole authoritative handoff)
**Status:** AUTHORITATIVE — execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. No competing root handoff files.

## Progress snapshot (prior session — heavy work completed, sealed)

- **Offline verification:** `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit -v` → 103 tests OK. Codebase in working order before any network work.
- **Gate 4 Branch 1 trigger:** ABSENT (rechecked 2026-11-12T07:31:59Z; no `research_state/fclr016_local_audit/*RESOLVED*` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). External/legal blocker — not agent-removable. Do not wait/poll. Branch 1 executes only on a valid RESOLVED trigger.
- **Bounded new-data monitor probe EXECUTED (2026-11-12T07:31:59Z):** `research_state/new_data_monitor_probe_20261112T073159Z.{md,json}` — ineligible now, evidenced; `new_claim_worthy_experiment_eligible_now=false`.
  - ironflow/hyperliquid-liquidations: `lastModified=2026-11-07T10:18:25Z`, latest event month `2026-10`, no verified post-2026-10-31 observed liquidation labels.
  - Hyperliquid 2026-11+ depth: BTC 1d candles 12 rows (~12.0d), BTC funding 272 rows (~11.29d). << 100d reprobe threshold and << 90d for ≥3×30d test blocks.
- **Sealed determinations unchanged:** metpie 2025Q2 §16 audit = INADMISSIBLE (block-feasibility ~65d < 90d); TRACKA-HL-EARLY-4H = INCONCLUSIVE_PILOT_SHORTFALL; all cached-data Track A/B/C/H1 designs sealed/exhausted (Track A expansion PASS but robustness FRAGILE; vol family NOT_MET; alt vol NOT_MET; Track B TB1/TB2 NOT_SUPPORTED; Track C/H1 NOT_SUPPORTED).

## Bottlenecks — status and removal action (2026-11-12T07:47:40Z)

| Bottleneck | Status | Removal/action |
|---|---|---|
| Gate 4 Branch 1 (external/legal Binance terms evidence) | BLOCKED, not agent-removable | ISOLATED: execute Branch 1 only on valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). Agent does NOT create/attest it. Do NOT wait/poll. All other work proceeds without it. No session is held up by this. |
| HL 2026-11+ ~12d; no verified post-2026-10-31 observed labels | OPEN, not eligible now (evidenced) | REMOVED as blocking path: do NOT re-probe HL/ironflow endpoints. Attack exclusively via NEW source discovery (campaign step 2 below). Reprobe HL/ironflow only when plausibly eligible (HL ≥100d AND verified post-2026-10-31 observed labels). No polling. |
| Cached-data designs exhausted/sealed | EXHAUSTED | REMOVED as candidate path: no relitigation/retune of sealed verdicts. Only a genuinely new admissible source/window per RESEARCH_PROMPT §16 can open a claim-worthy experiment. |
| Contradictory frontier next-task entries (multiple rank-0 stale tasks incl. sealed NOT_MET/FRAGILE campaigns) | INEFFICIENT | REMOVED: replaced by single authoritative FCLR-NEXT campaign below; prior sealed entries preserved as history, not relitigated. `experiment_frontier.json` rank-0 entries superseded by `FCLR_NEXT_ALTERNATIVE_LIQUIDATION_SOURCE_DISCOVERY`. |
| H2_shek_replication registry status "proposed" although `research_state/h002_replication_report.md` documents completed PARTIAL replication | INCONSISTENT | REMOVED: registry corrected to EXPLORATORY_ONLY/PARTIAL with evidence pointer; no re-run, no promotion. |

## NEXT FOCUS CAMPAIGN — FCLR-NEXT: bounded liquidation-label source discovery → §16 admissibility → prereg → eval → verdict (HEAVY, execute in order — UNAVOIDABLE)

**This campaign is the sole heavy work for every session.** No status-only output. Every session must deliver ONE of: (a) Gate 4 Branch 1 (if triggered), OR (b) a §16 admissibility audit (+ prereg/build/eval/verdict if a source passes), OR (c) evidenced infeasibility + state update + clean stop, OR (d) bounded probe evidence + ineligibility documentation. Future agents cannot skip this campaign; each probe must add new evidence or stop.

1. **Gate 4 check (FIRST, every session):** if valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears → execute Branch 1 immediately per campaign rules. (Absent now. Absence is not a reason to stop — proceed to step 2.)
2. **Bounded alternative liquidation-label source discovery (RESEARCH_PROMPT §5):** enumerate/test/rank ≥1 additional unauthenticated public source family for observed perpetual liquidation labels beyond `ironflow/hyperliquid-liquidations`, using existing scaffolding (`scripts/hunt_alternative_liquidation_sources.py` → `research_state/data_source_registry_alt_hunt.json`; `research_state/alt_source_deep_review_latest.md`; `research_state/url_probe_cache.json`; `research_state/hf_search_cache.json`). For each source record: exact URL/endpoint, access date, test method, no-auth result (HTTP + body sample), license/terms, fields, earliest/latest timestamp, cadence, symbol coverage, gaps, hashes/ETags where feasible, rejection reason if inadmissible. Claim-worthy consideration requires: ≥5 instruments, ≥1 complete month or ≥3 non-overlapping 30-day blocks, unauthenticated, provenance/license, observed labels only (not modeled/synthetic), venue-consistent (no Binance/2024 conflation).
3. **If a source passes smoke test:** run full §16 admissibility audit → emit timestamped determination + artifacts (`research_state/<source>_admissibility_audit_<UTC>.{md,json}`) BEFORE any preregistration or outcome computation. If admissible → freeze prereg (frozen event definition, censoring, eligible contracts, volatility split, metrics, multiplicity, gate) → build panel → evaluate → verdict → atomic state updates (`hypothesis_registry.json`, `experiment_frontier.json`, run manifest) under a NEW experiment ID. Never inspect outcomes before prereg freeze.
4. **If no source passes:** emit timestamped probe evidence documenting exact failing minima per source, update `experiment_frontier.json`, and stop cleanly. No repeated no-op probes; each probe must add new evidence or stop.
5. **HL/ironflow monitor reprobe:** only when plausibly eligible (HL 2026-11+ depth ≥100d AND verifiable post-2026-10-31 observed liquidation labels, or other evidenced new source). Not eligible now (~12.0d). Do not poll; re-check only when wall-clock time or new evidence makes eligibility plausible.

## COMPLETED / SEALED — DO NOT REOPEN, RETUNE, OR RELITIGATE

- `TRACKA-HL-EARLY-20261111T191958Z` = INADMISSIBLE (1h candles). Sealed.
- `TRACKA-HL-EARLY-4H-20261112T054737Z` = INCONCLUSIVE_PILOT_SHORTFALL (<3 test blocks). Sealed.
- Track A liquidation expansion `TRACKA-HL-EXPANSION-20261111T195500Z` = PASS; robustness `TRACKA-EXP-ROBUST-20261112T015119Z` = FRAGILE (LOIO 4/8 < 6; placebo FAIL; bootstrap PASS). Sealed.
- Track A alternate volatility `TRACKA-ALT-VOL-20261112T020322Z` = NOT_MET. Sealed.
- Track A volatility primary 24h `TRACKA-VOL-20261111T234918Z` = NOT_MET; volatility family `TRACKA-VOL-FAMILY-20261112T005111Z` = NOT_MET (Holm, 12 comparisons). Sealed.
- Track A 9-symbol 2026-05..2026-10 liquidation = NOT_MET (closed). Track B/C 2024 and H1/FCLR-002/003 contexts sealed/closed negative; H1 primary NOT_SUPPORTED. 2024 Binance confirmatory FCLR-003 = NOT_SUPPORTED (`research_state/final_confirmatory_verdict.md`). Immutable.
- metpie 2025-03-22..2025-05-25 §16 audit = INADMISSIBLE. Sealed.
- H2 Shek correction-time replication = PARTIAL/exploratory (`research_state/h002_replication_report.md`; SSRN 403; direction reproduced p=0.079, not significant; correction time ≠ forecast skill/liquidation evidence). No promotion.

## HARD BANS (BINDING)

- No outcome inspection before prereg freeze; no threshold-shopping; no sealed-holdout reuse.
- No Binance/2024 conflation; no modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No redundant network polling. No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- **No status-only output.** Every session delivers concrete heavy work or evidenced ineligibility + clean stop (per campaign rule above).
- Do not relitigate or retune sealed verdicts.

## KEY REFERENCES

- Eligibility evidence (this session): `research_state/new_data_monitor_probe_20261112T073159Z.{md,json}`.
- Alternative-source scaffolding: `scripts/hunt_alternative_liquidation_sources.py`; `research_state/data_source_registry_alt_hunt.json`; `research_state/alt_source_deep_review_latest.md`; `research_state/url_probe_cache.json`; `research_state/hf_search_cache.json`.
- H2 completed PARTIAL: `research_state/h002_replication_report.md`; `research_state/h002_replication_blocker.md`.
- Protocol: `RESEARCH_PROMPT.md` (§5 source families; §16 admissibility/adaptive feasibility).
- State: `research_state/experiment_frontier.json`; `research_state/hypothesis_registry.json`; `research_state/fclr016_local_audit/`.

## Execution contract

- First action: Gate 4 check → absent → proceed to campaign step 2.
- Deliverable: timestamped source-probe evidence (§5 rubric) and/or §16 admissibility audit, plus atomic state updates; or documented ineligibility + clean stop.
- Verification: inspect `research_state/data_source_registry_alt_hunt.json` for newly added source entries with test results; any §16 audit carries `generated_utc`, endpoint evidence, and acceptance/rejection rationale. Offline check before network probes: `python -m unittest tests.test_monitor_ironflow tests.test_trackc_panel_admissibility_audit -v`.