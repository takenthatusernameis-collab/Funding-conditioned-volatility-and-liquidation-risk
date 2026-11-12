# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk — repo-name-prioritized)
**Handoff timestamp (UTC):** 2026-11-12T06:39:45Z (supersedes 2026-11-12T06:31:39Z; this file is the sole authoritative handoff)
**Status:** AUTHORITATIVE — execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. No competing root handoff files.

## Progress snapshot (this session — heavy work completed)
- **Gate 4 Branch 1 trigger:** ABSENT (verified 2026-11-12T06:31:39Z; no `fclr016_v5_terms_evidence_RESOLVED_*` with `status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). **Do not wait/poll.** Branch 1 executes only on a valid RESOLVED trigger.
- **TRACKA-HL-EARLY-4H-20261112T054737Z (PRIMARY) — EVALUATED, verdict emitted.** Prereg was frozen pre-outcomes (`tracka_prereg_hyperliquid_early_4h_20261112T054737Z.{json,md}`, 05:47:37Z). 4h candles cached+complete 2025-11..2026-04, 9 symbols. Panel built (`tracka_hl_early_4h_panel_20261112T054737Z.parquet`, build report `tracka_hl_early_4h_panel_build_report_20261112T054737Z.json`, 1629 buckets, 9 symbols, 2 test blocks with data). Evaluation per prereg (C2 vs B1, QLIKE next-24h liquidation intensity, block bootstrap 2000 reps seed 20261112, 7d embargo, training-only standardization) via `scripts/tracka_hl_evaluate_early_4h.py`.
  - **Verdict:** `INCONCLUSIVE_PILOT_SHORTFALL` (primary gate cannot be satisfied). B1 mean QLIKE 76.507, C2 100.714 (n_pairs=362, 9 instruments), mean diff +24.207, 95% CI [22.037,25.408] (wrong direction), rel reduction -31.64%. Gate: materiality NOT_MET, CI_excludes_zero_better NOT_MET, ≥5 paired instruments PASS (9), ≥3 non-overlapping 30d test blocks **NOT_MET** (2: [0,1]; block 2 extends beyond 2026-04-30 window). Results reported for transparency only — **not confirmatory PASS**. Artifacts: `research_state/evaluation_summary_TRACKA-HL-EARLY-4H-20261112T054737Z.{md,json}`.
  - **State updated:** `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json` (H_tracka_hl_early_liquidation_forecast → INCONCLUSIVE_PILOT_SHORTFALL), addendum in `research_state/final_confirmatory_verdict.md`. Sealed records unchanged.
- **Cached 4h early-window design exhausted** under this prereg (block-count shortfall is a data/window constraint, not a retunable parameter). Do not reopen or retune sealed designs/verdicts.

## Immediate task (heavy, in-session now) — PRIMARY route
Do not produce a status-only response. Execute the Focus Campaign below now. Every session must deliver concrete heavy work or, only if infeasible, a concrete timestamped evidence artifact — never a status-only memo.

1. **Gate 4 check:** if valid `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` appears (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation), execute Branch 1 immediately per campaign rules.
2. **If no trigger (default): full §16 admissibility audit — metpie historical window (heavy).**
   - Target: `metpie/hyperliquid-liquidation-events` (historical observed Hyperliquid liquidation events, 2025-03-22..2025-05-25 per prior probe) joined to cached/admissible Hyperliquid funding+candles for that **exact** window.
   - Audit concretely (timestamped artifact): data availability & fetchability (unauthenticated, provenance, license/terms), venue consistency (Hyperliquid-only), observed-label integrity (no modeled/proxy/synthetic), schema/coverage per symbol, and feasibility of ≥5 symbols and ≥3 non-overlapping 30-day OOS test blocks with 7d embargo (compute exact blockability in that ~65d window) plus RV/context features computable from admissible candles.
   - Emit `research_state/admissibility_audit_metpie_2025Q2_<UTC>.{md,json}` with explicit ADMISSIBLE / INADMISSIBLE / NEEDS_MORE_DATA determination and evidence.
   - **If ADMISSIBLE:** freeze a new prereg **BEFORE** any outcome inspection, then build deterministic panel, evaluate pre-registered funding-conditioned vs RV-only baseline, emit verdict + atomic state updates (frontier, hypothesis_registry, run_manifest note if applicable, final_confirmatory_verdict addendum if confirmatory-relevant). No threshold-shopping.
   - **If INADMISSIBLE / insufficient:** emit timestamped evidence (exact failing minima) and advance to (3).
3. **Bounded reprobe/monitor (only when plausibly eligible):** HL 2026-11+ candles+funding when ≥100 days available **AND** verifiable post-2026-10-31 observed liquidation labels exist (e.g. ironflow HF). Emit timestamped probe/audit artifact with evidence; if newly admissible, freeze prereg before outcomes then build/eval+verdict. **No polling** if ineligible (current state: HL post-2026-10-31 ~11.2d, no verified post-2026-10-31 observed labels).

## FOCUS CAMPAIGN (EXECUTE IN ORDER, HEAVY WORK REQUIRED)
1. Gate 4 trigger check: absent (verified). Execute Branch 1 only on valid RESOLVED trigger.
2. **PRIMARY:** §16 admissibility audit of metpie 2025-03-22..2025-05-25 joined to HL features (step 2) → if admissible prereg+build+eval+verdict; if not, evidenced infeasibility then bounded eligible reprobe (step 3).
3. State hygiene: keep this file the single durable root handoff; keep redirects aligned. Preserve all sealed records/verdicts/manifests exactly as immutable.

## BOTTLENECKS — STATUS & REQUIRED ACTION (2026-11-12T06:39:45Z)
| Bottleneck | Status | Removal/action |
|---|---|---|
| Gate 4 Branch 1 (external/legal Binance terms) | BLOCKED, not agent-removable | Execute Branch 1 only on valid RESOLVED_VERIFIED trigger (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation). |
| 4h early-window liquidation forecast (TRACKA-HL-EARLY-4H-20261112T054737Z) | **COMPLETED — INCONCLUSIVE_PILOT_SHORTFALL** | 2/3 test blocks feasible in window; gate unsatisfiable per prereg. Do not reopen/retune. Evidence: `evaluation_summary_TRACKA-HL-EARLY-4H-20261112T054737Z.{md,json}`. |
| Cached-data exhaustion on prior tested designs (1h/24h/4h/volatility/expansion/alt-vol) | **EXHAUSTED/SEALED** | No relitigation. Only new pre-specified admissible designs on genuinely new/admissible data/windows. |
| metpie 2025-03-22..2025-05-25 admissibility unknown | **OPEN — PRIMARY ACTION** | Full §16 audit joined to HL funding+candles (step 2); timestamped ADMISSIBLE/INADMISSIBLE artifact with block-feasibility evidence. |
| Post-2026-10-31 HL window too short (~11.2d) / no verified post-2026-10-31 observed labels | OPEN (secondary) | Bounded reprobe only when plausibly eligible (HL ≥100d AND verifiable post-2026-10-31 observed labels); emit evidence. No polling. |

## COMPLETED / SEALED — DO NOT REOPEN, RETUNE, OR RELITIGATE
- `TRACKA-HL-EARLY-20261111T191958Z` = **INADMISSIBLE** (1h candles). Sealed.
- `TRACKA-HL-EARLY-4H-20261112T054737Z` = **INCONCLUSIVE_PILOT_SHORTFALL** (<3 test blocks in window). Sealed.
- Track A liquidation expansion `TRACKA-HL-EXPANSION-20261111T195500Z` = **PASS** (robustness **FRAGILE**, `TRACKA-EXP-ROBUST-20261112T015119Z`). Sealed.
- Track A alternate volatility `TRACKA-ALT-VOL-20261112T020322Z` = **NOT_MET**. Sealed.
- Track A volatility primary 24h `TRACKA-VOL-20261111T234918Z` = **NOT_MET**; volatility family `TRACKA-VOL-FAMILY-20261112T005111Z` = **NOT_MET**. Sealed.
- Track A 9-symbol 2026-05..2026-10 liquidation = **NOT_MET** (closed). Track B/C 2024 and H1/FCLR-002/003 contexts sealed/closed negative; H1 primary NOT_SUPPORTED on tested panels. 2024 Binance confirmatory FCLR-003 = **NOT_SUPPORTED** (`research_state/final_confirmatory_verdict.md`). Immutable.

## HARD BANS (BINDING)
- **No outcome inspection before prereg freeze** for any new claim. No threshold-shopping. No sealed-holdout reuse.
- No Binance/2024 conflation; venue-consistent artifacts only. No modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No redundant network polling. No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- **No status-only output.** Every session must deliver: Gate 4 Branch 1 if triggered, OR a concrete §16 admissibility audit / prereg+build+eval+verdict, OR evidenced infeasibility + state updates.
- Do not relitigate or retune sealed verdicts.

## KEY REFERENCES
- This session verdict: `research_state/evaluation_summary_TRACKA-HL-EARLY-4H-20261112T054737Z.{md,json}`, `research_state/tracka_hl_early_4h_panel_20261112T054737Z.parquet`, `research_state/tracka_hl_early_4h_panel_build_report_20261112T054737Z.json`, `scripts/tracka_hl_evaluate_early_4h.py`, prereg `research_state/tracka_prereg_hyperliquid_early_4h_20261112T054737Z.{json,md}`.
- External probes/prior audit: `research_state/new_data_external_probe_audit_20261112T044425Z.{md,json}`, `research_state/external_probe_raw_20261112T044425Z.json`, `research_state/new_data_admissibility_audit_20261112T042738Z.md`.
- Handoff/state: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/final_confirmatory_verdict.md`, `research_state/fclr016_local_audit/`.
- Protocol: `RESEARCH_PROMPT.md` (§16 admissible new data).

---
**Execute now:** Gate 4 check (absent) → full §16 admissibility audit of metpie 2025-03-22..2025-05-25 joined to HL funding+candles (timestamped ADMISSIBLE/INADMISSIBLE artifact with exact block-feasibility). If ADMISSIBLE, freeze prereg before outcomes then build/eval+verdict+atomic state updates. If INADMISSIBLE, emit timestamped evidence and run bounded eligible reprobe only if plausibly eligible (else evidence). No status-only output.
