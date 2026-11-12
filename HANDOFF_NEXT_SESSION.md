# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk — repo-name-prioritized)
**Handoff timestamp (UTC):** 2026-11-12T07:31:59Z (supersedes 2026-11-12T07:30:28Z; this file is the sole authoritative handoff)
**Status:** AUTHORITATIVE — execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. No competing root handoff files.

## Progress snapshot (this session — heavy work completed)

- **Gate 4 Branch 1 trigger:** ABSENT (rechecked 2026-11-12T07:31:59Z; no `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_*` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). **Do not wait/poll.** Branch 1 executes only on a valid RESOLVED trigger.
- **Bounded new-data monitor probe EXECUTED (2026-11-12T07:31:59Z)** — evidence: `research_state/new_data_monitor_probe_20261112T073159Z.{md,json}` (live HF API + HL info probes).
  - **ironflow/hyperliquid-liquidations:** `lastModified=2026-11-07T10:18:25.000Z`, `sha=65bad6c39c63ee24eae920753f05303020e549fa`, 38 siblings; latest event month `2026-10` (no post-2026-10-31 / no 2026-11 event file). **No verified post-2026-10-31 observed liquidation labels.**
  - **Hyperliquid 2026-11+ depth (from 2026-11-01):** BTC 1d candles 12 (2026-11-01..2026-11-12, ~12.0d), BTC funding 272 rows (~11.29d). **Far below 100-day reprobe threshold and << 90 days required for ≥3×30d test blocks.**
  - **Eligibility now:** `new_claim_worthy_experiment_eligible_now=false` (evidenced). No polling.
- **Prior sealed determinations unchanged:** metpie 2025-03-22..2025-05-25 §16 audit = INADMISSIBLE (block-feasibility shortfall ~65d < 90d for ≥3×30d test blocks), `research_state/admissibility_audit_metpie_2025Q2_20261112T070000Z.{md,json}` (sealed). TRACKA-HL-EARLY-4H-20261112T054737Z = INCONCLUSIVE_PILOT_SHORTFALL (sealed).

## Immediate task (heavy, in-session now)

Do not produce a status-only response. Every session must deliver concrete heavy work or, only if infeasible, a concrete timestamped evidence artifact — never a status-only memo.

1. **Gate 4 check:** if valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears in `research_state/fclr016_local_audit/` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation), execute Branch 1 immediately per campaign rules.
2. **If no trigger (default):** pursue bounded new-data discovery per RESEARCH_PROMPT.md §16. The only routes to a new claim-worthy experiment are (a) Gate 4 Branch 1 trigger (external/legal, not agent-removable, do not wait/poll), OR (b) a genuinely new admissible data source/window verified with evidence (≥5 instruments, ≥3 non-overlapping 30-day test blocks, unauthenticated, provenance/license, observed labels where Track A, venue-consistent, not Binance/2024 conflation).
3. **If neither (a) nor (b):** execute bounded monitoring reprobes only when plausibly eligible (HL 2026-11+ depth approaching/≥100d AND verifiable post-2026-10-31 observed liquidation labels, or other evidenced new source). If not eligible, emit a timestamped probe/audit artifact with evidence, document exact ineligibility minima, update this handoff, and stop cleanly. **No polling/repeated no-op probes.**

## FOCUS CAMPAIGN (EXECUTE IN ORDER, HEAVY WORK REQUIRED)

1. Gate 4 trigger check — absent; execute Branch 1 only on valid RESOLVED trigger.
2. §16 admissibility audits of any genuinely new candidate source/window — emit timestamped determination+artifacts before any prereg/eval (metpie 2025Q2 already INADMISSIBLE/sealed).
3. Bounded monitor reprobes (HL 2026-11+ depth, ironflow HF extension beyond 2026-10-31, or other evidenced sources) with timestamped evidence when plausibly eligible; otherwise documented ineligibility + clean stop (this session: `research_state/new_data_monitor_probe_20261112T073159Z.{md,json}`, ineligible).
4. State hygiene: keep this file the single durable root handoff; keep redirects aligned. Preserve all sealed records/verdicts/manifests exactly as immutable.

## BOTTLENECKS — STATUS & REQUIRED ACTION (2026-11-12T07:31:59Z)

| Bottleneck | Status | Removal/action |
|---|---|---|
| Gate 4 Branch 1 (external/legal Binance terms) | BLOCKED, not agent-removable | Execute Branch 1 only on valid RESOLVED_VERIFIED trigger (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). |
| 4h early-window liquidation forecast (TRACKA-HL-EARLY-4H-20261112T054737Z) | COMPLETED — INCONCLUSIVE_PILOT_SHORTFALL | Sealed. Do not reopen/retune. |
| Cached-data exhaustion on prior tested designs (1h/24h/4h/volatility/expansion/alt-vol) | EXHAUSTED/SEALED | No relitigation. Only new pre-specified admissible designs on genuinely new/admissible data/windows. |
| metpie 2025-03-22..2025-05-25 admissibility | RESOLVED — INADMISSIBLE | Block-feasibility shortfall (~65d < 90d). `admissibility_audit_metpie_2025Q2_20261112T070000Z.{md,json}`. Sealed. |
| Post-2026-10-31 HL window too short (~12.0d) / no verified post-2026-10-31 observed labels | OPEN, **not eligible now** (evidenced) | Reprobe only when plausibly eligible (HL ≥100d AND verifiable post-2026-10-31 observed labels). Latest: `new_data_monitor_probe_20261112T073159Z.{md,json}`. No polling. |
| No untested admissible cached-data experiment | EXHAUSTED | `new_data_admissibility_audit_20261112T042738Z.md`. New claim requires NEW admissible source/window per §16. |

## COMPLETED / SEALED — DO NOT REOPEN, RETUNE, OR RELITIGATE

- `TRACKA-HL-EARLY-20261111T191958Z` = INADMISSIBLE (1h candles). Sealed.
- `TRACKA-HL-EARLY-4H-20261112T054737Z` = INCONCLUSIVE_PILOT_SHORTFALL (<3 test blocks). Sealed.
- Track A liquidation expansion `TRACKA-HL-EXPANSION-20261111T195500Z` = PASS (robustness FRAGILE, `TRACKA-EXP-ROBUST-20261112T015119Z`). Sealed.
- Track A alternate volatility `TRACKA-ALT-VOL-20261112T020322Z` = NOT_MET. Sealed.
- Track A volatility primary 24h `TRACKA-VOL-20261111T234918Z` = NOT_MET; volatility family `TRACKA-VOL-FAMILY-20261112T005111Z` = NOT_MET. Sealed.
- Track A 9-symbol 2026-05..2026-10 liquidation = NOT_MET (closed). Track B/C 2024 and H1/FCLR-002/003 contexts sealed/closed negative; H1 primary NOT_SUPPORTED on tested panels. 2024 Binance confirmatory FCLR-003 = NOT_SUPPORTED (`research_state/final_confirmatory_verdict.md`). Immutable.
- metpie 2025-03-22..2025-05-25 §16 audit = INADMISSIBLE. Sealed.

## HARD BANS (BINDING)

- **No outcome inspection before prereg freeze** for any new claim. No threshold-shopping. No sealed-holdout reuse.
- No Binance/2024 conflation; venue-consistent artifacts only. No modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No redundant network polling. No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- **No status-only output.** Every session must deliver: Gate 4 Branch 1 if triggered, OR a concrete §16 admissibility audit/prereg+build+eval+verdict, OR evidenced infeasibility + state updates, OR bounded probe/monitor evidence + ineligibility documentation (as this session).
- Do not relitigate or retune sealed verdicts.

## KEY REFERENCES

- This-session probe (evidence): `research_state/new_data_monitor_probe_20261112T073159Z.{md,json}`.
- Prior probe: `research_state/new_data_monitor_probe_20261112T073028Z.json`.
- Metpie §16 audit (sealed, INADMISSIBLE): `research_state/admissibility_audit_metpie_2025Q2_20261112T070000Z.{md,json}`.
- Early-4h verdict (sealed): `research_state/evaluation_summary_TRACKA-HL-EARLY-4H-20261112T054737Z.{md,json}`.
- External/admissibility probes: `research_state/new_data_external_probe_audit_20261112T044425Z.{md,json}`, `research_state/new_data_admissibility_audit_20261112T042738Z.md`.
- Handoff/state: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/final_confirmatory_verdict.md`, `research_state/fclr016_local_audit/`.
- Protocol: `RESEARCH_PROMPT.md` (§16 admissible new data).

---

**Execute now:** Gate 4 check (absent) → if no trigger and no newly-eligible source/window, perform bounded discovery/probe only with plausible eligibility; otherwise emit timestamped evidence of ineligibility (done this session), update handoff, and stop cleanly. No polling. No status-only output.
