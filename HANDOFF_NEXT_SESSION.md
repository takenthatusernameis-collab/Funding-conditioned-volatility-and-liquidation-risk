# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk — repo-name-prioritized)
**Handoff timestamp (UTC):** 2026-11-12T00:53:23Z (supersedes 2026-11-12T00:51:11Z; this file remains the sole authoritative handoff)
**Status:** AUTHORITATIVE — execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects. No competing root handoff files.

## Immediate task (heavy, in-session now)
Do not produce a status-only response. Execute the Focus Campaign below now.

**(A) REPO-PRIORITY: LIQUIDATION-RISK ROBUSTNESS/FALSIFICATION CAMPAIGN** (volatility family completed NOT_MET)
The volatility multiplicity family for `TRACKA-VOL-20261111T234918Z` is now **COMPLETE** with verdict **NOT_MET** (family-wise Holm correction across 12 comparisons; no horizon passes primary gate). All secondary horizons (6h, 72h, 168h) evaluated on frozen panel `research_state/tracka_vol_panel_20261111T234918Z.parquet` with identical causal features and splits. Family evaluation summary: `research_state/evaluation_summary_TRACKA-VOL-FAMILY-20261112T005111Z.md`. State updates atomic: `experiment_frontier.json`, `hypothesis_registry.json` (`H_tracka_hl_funding_conditioned_volatility_forecast` = NOT_MET), `run_manifest.json` (run `FAMILY-EVAL-20261112T005111Z`), `final_confirmatory_verdict.md`.

**Pivot in-session to (B):** TRACKA expansion robustness/falsification campaign on sealed PASS panel `TRACKA-HL-EXPANSION-20261111T195500Z` (8-coin expansion universe ZEC/NEAR/UNI/AAVE/CRV/ADA/LTC/BCH, 2026-05..2026-10, cached Hyperliquid funding + candles + ironflow observed labels).

Steps for this session:
1. **Freeze new prereg BEFORE any robustness outcome computation** at `research_state/tracka_prereg_expansion_robust_<UTC>.json/.md` specifying ex-ante checks with pass/falsification criteria:
   - Leave-one-instrument-out (LOIO) sensitivity: re-evaluate C2 vs B1 on each 7-instrument subset; pass if ≥6/8 LOIO runs show rel QLIKE reduction ≥2% and CI excludes zero favoring C2.
   - Placebo/permutation on funding features: permute `fundingRate` and `abs_funding` across time within each instrument (fixed seed 20261112); recompute C2 vs B1; pass if true rel reduction > 95th percentile of placebo distribution.
   - Alternative block/bootstrap settings: re-evaluate with (a) block_size=48h, (b) stationary bootstrap mean_block=24h, (c) 5000 reps; pass if all settings yield rel reduction ≥2% and CI excludes zero.
   - Overall verdict: ROBUST if all three checks pass; FRAGILE if any check fails; INCONCLUSIVE if computational infeasibility.
2. Run all checks on cached panel `research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet` (sha256 verify via build report `research_state/tracka_hl_expansion_panel_build_report_20261111T202344Z.json`).
3. Emit verdict `research_state/evaluation_summary_TRACKA-EXP-ROBUST-<UTC>.md` (ROBUST/FRAGILE/INCONCLUSIVE) with per-check results, raw/adjusted metrics, and gate assessment.
4. Atomic state updates (MANDATORY): update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json` (add `H_tracka_hl_expansion_robustness` status), `research_state/run_manifest.json` (run `EXP-ROBUST-<UTC>`), append addendum to `research_state/final_confirmatory_verdict.md`. Preserve all sealed/closed records; never mutate closed verdicts.
5. If any check fails (FRAGILE): document exact failure mode; preregister and attempt next best admissible untested claim in-session (e.g., alternate volatility design on cached HL 2025-11..2026-10 with different pre-specified horizon/features/splits) repeating Steps 1–4. Do not stop at the first failure.

**(B) Gate 4 Branch 1 (only if valid trigger appears):** If `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` exists with `status=RESOLVED_VERIFIED`, `fabricated=false`, and human/legal attestation → deterministic promotion+validators → on all-green confirmatory Track C multi-split ablation + verdict + state updates. **Verified absent; do not wait/poll.**

## BOTTLENECK CHECK (THIS SESSION)
- Gate 4 Branch 1 trigger: **NOT PRESENT** — `research_state/fclr016_local_audit/` contains no `fclr016_v5_terms_evidence_RESOLVED_*` with required RESOLVED_VERIFIED/legal attestation/fabricated=false; only `_BLOCKED`/`_UNRESOLVED`/`_partial`/probe artifacts exist. **Do not wait/poll; proceed with liquidation robustness campaign.** Never guess, never set `fabricated=true`, never bypass.
- Stale/competing handoff surfaces: **REMOVED** — root `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` redirect to this file. Single durable handoff only.
- Volatility multiplicity family: **COMPLETED NOT_MET** — `research_state/evaluation_summary_TRACKA-VOL-FAMILY-20261112T005111Z.md` (12 comparisons, Holm correction, no horizon passes primary gate). Immutable.
- Liquidation expansion PASS: **SEALED** — `TRACKA-HL-EXPANSION-20261111T195500Z` PASS (C2 vs B1 rel QLIKE -19.04%, 95% CI [-5.088,-0.478], n=593, 8 instruments, 3 blocks, 2026-05..2026-10). Immutable, do not relitigate.
- Volatility primary 24h: **NOT_MET** — `TRACKA-VOL-20261111T234918Z` (C2 vs B1 rel QLIKE -1.37%, CI crosses zero, n=19233, 9 instruments, 3 blocks). Immutable.

## FOCUS CAMPAIGN (REPO-NAME-PRIORITIZED)
**Objective (inferred from repo name + protocol):** execute the pre-registered robustness/falsification campaign for the sealed Track A liquidation expansion PASS (`TRACKA-HL-EXPANSION-20261111T195500Z`) on the cached 8-coin Hyperliquid panel. Freeze prereg BEFORE outcomes specifying ex-ante leave-one-instrument-out sensitivity, placebo/permutation on funding features (fixed seed), and alternative block/bootstrap settings with pass/falsification criteria. Run all checks; emit ROBUST/FRAGILE/INCONCLUSIVE verdict + atomic state updates. Every session must deliver prereg + (build+eval or documented infeasibility+next-attempt) + state updates.

**Execute in this exact order:** Steps 1–4 above, then Step 5 as applicable.

## BOTTLENECKS — STATUS & REMOVAL
| Bottleneck | Status | Removal/action |
|---|---|---|
| Gate 4 Branch 1 (external/legal Binance terms) | BLOCKED, not agent-removable | **Do not wait.** Run Branch 1 only if `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` exists with all required fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, and human/legal attestation → deterministic promotion+validators → on all-green confirmatory Track C multi-split ablation + verdict + state. Verified absent now. |
| Volatility multiplicity family incomplete (secondary horizons unevaluated) | **REMOVED** | Completed: `research_state/evaluation_summary_TRACKA-VOL-FAMILY-20261112T005111Z.md` (NOT_MET). |
| No robustness/falsification on sealed TRACKA expansion PASS | **REMOVABLE NOW** | Steps 1–4 of this task. Panel exists, sealed PASS, new prereg required pre-outcomes. |
| Competing root handoff docs / session ambiguity | REMOVED | This file is sole durable root handoff; redirect files in place. |

## COMPLETED / SEALED — DO NOT REOPEN, RETUNE, OR RELITIGATE
- Track A liquidation expansion `TRACKA-HL-EXPANSION-20261111T195500Z` = **PASS** (C2 vs B1 rel QLIKE -19.04%, 95% CI [-5.088,-0.478], n=593, 8 instruments, 3 blocks, 2026-05..2026-10). Sealed.
- Track A volatility primary 24h `TRACKA-VOL-20261111T234918Z` = **NOT_MET** (C2 vs B1 rel QLIKE -1.37%, CI crosses zero, n=19233, 9 instruments, 3 blocks, 2026-05..2026-10). Sealed.
- Track A volatility multiplicity family `TRACKA-VOL-FAMILY-20261112T005111Z` = **NOT_MET** (family-wise Holm across 12 comparisons; no horizon passes primary gate). Sealed.
- Track A 9-symbol 2026-05..2026-10 liquidation = **NOT_MET** (closed). Track A early 2025-11..2026-04 = **INADMISSIBLE** (closed).
- Track B/C 2024 and H1/FCLR-002/003 contexts sealed/closed negative; H1 primary NOT_SUPPORTED on tested panels. Immutable.
- 2024 Binance confirmatory FCLR-003 = **NOT_SUPPORTED** (final_confirmatory_verdict.md executive verdict). Immutable.

## HARD BANS (BINDING)
- No outcome inspection before prereg freeze. No threshold-shopping. No sealed-holdout reuse.
- No Binance/2024 conflation; Hyperliquid-only venue for this campaign with matching artifacts.
- No modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No redundant network polling. No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- **No status-only output.** Every session must deliver prereg + (build+eval or documented infeasibility+next-attempt) + state updates.

## KEY REFERENCES
- Handoff/state: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md`, `research_state/fclr016_local_audit/`
- Caches: `research_state/data_cache/hyperliquid_candles/` (17 coins, 2025-11..2026-10 for 9 core; 2026-05..2026-10 for 8 expansion), `research_state/data_cache/hyperliquid_funding/` (17 coins, ~2025-11..2026-10), `research_state/data_cache/ironflow_events/` (2025-05..2026-10, 432 markets)
- Liquidation expansion panel: `research_state/tracka_hl_expansion_panel_20261111T202344Z.parquet`, `research_state/tracka_hl_expansion_panel_build_report_20261111T202344Z.json`
- Liquidation expansion prereg (template): `research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json`
- Evaluation scripts: `scripts/run_trackc_robustness_fclr011.py`, `src/volatility/eval.py`, `src/volatility/block_bootstrap.py`, `src/volatility/features_ext.py`

**Execute Step 1 now (freeze robustness prereg).**