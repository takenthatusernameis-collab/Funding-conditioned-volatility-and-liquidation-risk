# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk — repo-name-prioritized)
**Handoff timestamp (UTC):** 2026-11-12T07:00:00Z (supersedes 2026-11-12T06:39:45Z; this file is the sole authoritative handoff)
**Status:** AUTHORITATIVE — execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. No competing root handoff files.

## Progress snapshot (this session — heavy work completed)

- **Gate 4 Branch 1 trigger:** ABSENT (verified 2026-11-12T06:31:39Z; still absent 2026-11-12T07:00:00Z; no `fclr016_v5_terms_evidence_RESOLVED_*` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). **Do not wait/poll.** Branch 1 executes only on a valid RESOLVED trigger.
- **TRACKA-HL-EARLY-4H-20261112T054737Z (PRIMARY) — EVALUATED, verdict emitted.** INCONCLUSIVE_PILOT_SHORTFALL (2/3 test blocks; C2 worse than B1). Sealed. Do not reopen/retune.
- **§16 admissibility audit of metpie 2025-03-22..2025-05-25 joined to HL funding+candles — COMPLETED, determination emitted.**
  - Target: `metpie/hyperliquid-liquidation-events` (346,130 observed liquidation events, 179 coins, 2025-03-22..2025-05-25, CC BY 4.0, unauthenticated GitHub API) joined to Hyperliquid funding+candles for the exact window.
  - Evidence: HL 4h candles fetchable (390 rows/symbol, complete window, all 11 top symbols). HL fundingHistory paginatable (BTC: 1,548 rows across 4 chunks, full window). Metpie ≥5 instruments PASS (11 coins ≥5,000 events). RV/context features computable.
  - **Determination: INADMISSIBLE.** Primary failing criterion: block feasibility. Window ~64.1 days < 90 days minimum for ≥3 non-overlapping 30-day OOS test blocks. Structurally infeasible under any split configuration, with or without 7-day embargo or train/val. Artifacts: `research_state/admissibility_audit_metpie_2025Q2_20261112T070000Z.{md,json}`.
- **Bounded reprobe/monitor (step 3): NOT currently eligible.** HL 2026-11+ window ~11.2 days (<100-day threshold). No verified post-2026-10-31 observed liquidation labels (ironflow HF lastModified 2026-11-07T10:18:25Z, event files through 2026-10 only). **No polling.**

## Immediate task (heavy, in-session now)

Do not produce a status-only response. Every session must deliver concrete heavy work or, only if infeasible, a concrete timestamped evidence artifact — never a status-only memo.

1. **Gate 4 check:** if valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation), execute Branch 1 immediately per campaign rules.
2. **If no trigger (default):** bounded new-data discovery per RESEARCH_PROMPT.md §16 and HANDOFF_NEXT_SESSION.md step 3. The metpie audit is complete (INADMISSIBLE) and all cached-data designs are exhausted/sealed. The only remaining routes to a new claim-worthy experiment are:
   - (a) Gate 4 Branch 1 trigger appears (external/legal, not agent-removable, do not wait/poll); OR
   - (b) A genuinely new admissible data source/window is verified (≥5 instruments, ≥3 non-overlapping 30-day test blocks, unauthenticated, provenance/license, observed labels where Track A, venue-consistent, not Binance/2024 conflation).
3. **If neither (a) nor (b) is available this session:** execute bounded monitoring probes (HL API 2026-11+ candle/funding depth; ironflow HF lastModified/event files for extension beyond 2026-10-31), emit timestamped probe/audit artifact with evidence, document exact ineligibility minima, and stop cleanly. Do not poll repeatedly.

## FOCUS CAMPAIGN (EXECUTE IN ORDER, HEAVY WORK REQUIRED)

1. Gate 4 trigger check: absent (verified). Execute Branch 1 only on valid RESOLVED trigger.
2. §16 admissibility audit of metpie 2025-03-22..2025-05-25 joined to HL features — **COMPLETED: INADMISSIBLE** (block-feasibility shortfall, ~65d < 90d required). Artifacts emitted. No prereg/eval on this window.
3. Bounded new-data discovery / monitor probes (step 3 above): HL 2026-11+ depth, ironflow HF extension beyond 2026-10-31. Emit timestamped evidence. No polling if ineligible.
4. State hygiene: keep this file the single durable root handoff; keep redirects aligned. Preserve all sealed records/verdicts/manifests exactly as immutable.

## BOTTLENECKS — STATUS & REQUIRED ACTION (2026-11-12T07:00:00Z)

| Bottleneck | Status | Removal/action |
|---|---|---|
| Gate 4 Branch 1 (external/legal Binance terms) | BLOCKED, not agent-removable | Execute Branch 1 only on valid RESOLVED_VERIFIED trigger (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). |
| 4h early-window liquidation forecast (TRACKA-HL-EARLY-4H-20261112T054737Z) | COMPLETED — INCONCLUSIVE_PILOT_SHORTFALL | Sealed. Do not reopen/retune. |
| Cached-data exhaustion on prior tested designs (1h/24h/4h/volatility/expansion/alt-vol) | EXHAUSTED/SEALED | No relitigation. Only new pre-specified admissible designs on genuinely new/admissible data/windows. |
| metpie 2025-03-22..2025-05-25 admissibility | **RESOLVED — INADMISSIBLE** | §16 audit complete. Block feasibility NOT_MET (~65d < 90d required for ≥3×30d test blocks). Artifacts: `admissibility_audit_metpie_2025Q2_20261112T070000Z.{md,json}`. Do not reopen. |
| Post-2026-10-31 HL window too short (~11.2d) / no verified post-2026-10-31 observed labels | OPEN (secondary, not currently eligible) | Bounded reprobe only when plausibly eligible (HL ≥100d AND verifiable post-2026-10-31 observed labels); emit evidence. No polling. |
| No untested admissible cached-data experiment | EXHAUSTED | Inventory complete (new_data_admissibility_audit_20261112T042738Z). New claim requires NEW admissible source/window per §16. |

## COMPLETED / SEALED — DO NOT REOPEN, RETUNE, OR RELITIGATE

- `TRACKA-HL-EARLY-20261111T191958Z` = INADMISSIBLE (1h candles). Sealed.
- `TRACKA-HL-EARLY-4H-20261112T054737Z` = INCONCLUSIVE_PILOT_SHORTFALL (<3 test blocks in window). Sealed.
- Track A liquidation expansion `TRACKA-HL-EXPANSION-20261111T195500Z` = PASS (robustness FRAGILE, `TRACKA-EXP-ROBUST-20261112T015119Z`). Sealed.
- Track A alternate volatility `TRACKA-ALT-VOL-20261112T020322Z` = NOT_MET. Sealed.
- Track A volatility primary 24h `TRACKA-VOL-20261111T234918Z` = NOT_MET; volatility family `TRACKA-VOL-FAMILY-20261112T005111Z` = NOT_MET. Sealed.
- Track A 9-symbol 2026-05..2026-10 liquidation = NOT_MET (closed). Track B/C 2024 and H1/FCLR-002/003 contexts sealed/closed negative; H1 primary NOT_SUPPORTED on tested panels. 2024 Binance confirmatory FCLR-003 = NOT_SUPPORTED (`research_state/final_confirmatory_verdict.md`). Immutable.
- metpie 2025-03-22..2025-05-25 §16 audit = INADMISSIBLE (block-feasibility shortfall). Sealed. Do not reopen.

## HARD BANS (BINDING)

- **No outcome inspection before prereg freeze** for any new claim. No threshold-shopping. No sealed-holdout reuse.
- No Binance/2024 conflation; venue-consistent artifacts only. No modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No redundant network polling. No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- **No status-only output.** Every session must deliver: Gate 4 Branch 1 if triggered, OR a concrete §16 admissibility audit / prereg+build+eval+verdict, OR evidenced infeasibility + state updates, OR bounded new-data probe/monitor evidence + ineligibility documentation.
- Do not relitigate or retune sealed verdicts.

## KEY REFERENCES

- Metpie §16 audit: `research_state/admissibility_audit_metpie_2025Q2_20261112T070000Z.{md,json}` (determination: INADMISSIBLE).
- Prior session verdict: `research_state/evaluation_summary_TRACKA-HL-EARLY-4H-20261112T054737Z.{md,json}`, `scripts/tracka_hl_evaluate_early_4h.py`, prereg `research_state/tracka_prereg_hyperliquid_early_4h_20261112T054737Z.{json,md}`.
- External probes: `research_state/new_data_external_probe_audit_20261112T044425Z.{md,json}`, `research_state/new_data_admissibility_audit_20261112T042738Z.md`.
- Handoff/state: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/final_confirmatory_verdict.md`, `research_state/fclr016_local_audit/`.
- Protocol: `RESEARCH_PROMPT.md` (§16 admissible new data).

---

**Execute now:** Gate 4 check (absent) → metpie §16 audit COMPLETE (INADMISSIBLE, artifacts emitted) → bounded new-data discovery/monitor probes (HL 2026-11+ depth, ironflow HF extension) with timestamped evidence if eligible, else documented ineligibility + clean stop. No status-only output.
