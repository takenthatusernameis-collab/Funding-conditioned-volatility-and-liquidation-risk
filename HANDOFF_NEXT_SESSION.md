# INITIAL TASK MESSAGE — NEXT AGENTIC WORK SESSION (SINGLE DURABLE HANDOFF)
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk` (priority: funding-conditioned volatility AND liquidation risk — repo-name-prioritized)
**Handoff timestamp (UTC):** 2026-11-12T00:36:38Z (supersedes 2026-11-12T00:01:29Z content; this file remains the sole authoritative handoff)
**Status:** AUTHORITATIVE — execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects.

## Immediate task (heavy, in-session now)
Do not produce a status-only response. Execute the Focus Campaign below now:

**(A) Repo-priority: complete the declared multiplicity family for frozen `TRACKA-VOL-20261111T234918Z` (funding-conditioned volatility):**
1. Load frozen prereg `research_state/tracka_prereg_volatility_20261111T234918Z.json` (frozen pre-outcomes) and cached panel `research_state/tracka_vol_panel_20261111T234918Z.parquet` (39744 rows, 9 coins AVAX/BNB/BTC/DOGE/ETH/LINK/SOL/SUI/XRP, 2026-05..2026-10, causal features). Verify panel sha256 `bd6b9924e2f76dfa9ea5cecd9737e62f32c0a76b663695bd9fc161cc1257b837` matches build report.
2. Construct secondary targets causally for each horizon H ∈ {6h, 72h, 168h}: forward realized variance over next H hourly log returns from same panel, using only future closes in horizon for label; identical causal features (RV1h/RV24h/RV168h, funding_rate, abs_funding, premium, ema_dist); identical chronological splits with 7-day embargo, 3×30-day test blocks, identical train/validation/test boundaries from build report.
3. Run pre-registered model comparisons per horizon. For each H, evaluate B0 (persistence), B1 (RV-only HAR-style OLS on log(y+eps)), C1 (B1 + funding_rate + abs_funding), C2 (C1 + premium + ema_dist) with train-only fit, standardized predictors, smearing correction, clipped positive predictions. Primary contrast per horizon: C2 vs B1 on QLIKE (lower better). Secondary contrasts: C1 vs B1, C2 vs C1.
4. Apply multiplicity correction. Declared family = {primary 24h, secondary 6h, secondary 72h, secondary 168h} × {primary contrast C2vsB1, secondary C1vsB1, secondary C2vsC1} = 12 comparisons. Apply Holm correction (or pre-registered alternative) to the full family. Report raw and adjusted results for every cell.
5. Emit family evaluation summary `research_state/evaluation_summary_TRACKA-VOL-FAMILY-20261112T003638Z.md` with: per-horizon results (n, instruments, blocks, QLIKE per model, paired diffs, 95% block-bootstrap CIs, relative reductions), family-wise adjusted verdict per contrast, overall gate assessment (materiality ≥2% rel reduction + CI excludes zero favoring C2 for primary contrast on ANY horizon after correction). Record experiment id, prereg path, panel/build artifacts, all results.
6. Atomic state updates (MANDATORY): update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json` (H_tracka_hl_funding_conditioned_volatility_forecast status), `research_state/run_manifest.json` (run FAMILY-EVAL-20261112T003638Z), and append addendum to `research_state/final_confirmatory_verdict.md`. Preserve all sealed/closed records; never mutate closed verdicts.
7. If any secondary horizon passes family-wise gate: note it in verdict but do not promote post-hoc — primary 24h target was pre-registered as the single primary outcome. A secondary-only pass after correction is registered as EXPLORATORY_ONLY with new experiment ID if pursued.
8. If infeasible at any step: emit concrete infeasibility artifact with exact evidence, update state, then immediately preregister and attempt the next best admissible untested claim in-session (e.g., liquidation-intensity robustness on 8-coin expansion universe ZEC/NEAR/UNI/AAVE/CRV/ADA/LTC/BCH for 2026-05..2026-10 with new prereg, or alternate volatility window on cached data) repeating Steps 1–6 in-session. Do not stop at the first failure.

**(B) Liquidation-risk fallback (repo-priority, if (A) completes NOT_MET/INCONCLUSIVE/infeasible):** preregister + run liquidation-intensity robustness on the 8-coin expansion universe (cached ironflow observed labels + Hyperliquid funding + candles, 2026-05..2026-10, ZEC/NEAR/UNI/AAVE/CRV/ADA/LTC/BCH), same materiality (≥2%) + inference (≥5 instruments, ≥3 non-overlapping 30-day blocks, 7-day embargo, block bootstrap 2000 reps) gates; emit verdict + atomic state updates.

## BOTTLENECK CHECK (THIS SESSION)
- Gate 4 Branch 1 trigger: **NOT PRESENT** — `research_state/fclr016_local_audit/` contains no `fclr016_v5_terms_evidence_RESOLVED_*` with required RESOLVED_VERIFIED/legal attestation/fabricated=false; only `_BLOCKED`/`_UNRESOLVED`/`_partial`/probe artifacts exist. **Do not wait/poll; proceed Branch 2.** Never guess, never set `fabricated=true`, never bypass.
- Stale/competing handoff surfaces: **REMOVED** — root `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` redirect to this file. Single durable handoff only.
- Volatility secondary horizons: **NOT EVALUATED** — removable now. Panel exists, prereg frozen, splits fixed. Evaluate 6h/72h/168h now (Steps 1–5).
- Liquidation expansion PASS: **SEALED** — `TRACKA-HL-EXPANSION-20261111T195500Z` PASS (C2 vs B1 rel QLIKE -19.04%, 95% CI [-5.088,-0.478], n=593, 8 instruments, 3 blocks, 2026-05..2026-10). Immutable, do not relitigate.
- Volatility primary 24h: **NOT_MET** — `TRACKA-VOL-20261111T234918Z` (C2 vs B1 rel QLIKE -1.37%, CI [-0.014, 0.002] crosses zero, n=19233, 9 instruments, 3 blocks). Immutable.

## FOCUS CAMPAIGN (REPO-NAME-PRIORITIZED)
**Objective (inferred from repo name + protocol §17):** finish the pre-registered multiplicity family for the frozen volatility experiment by evaluating the three secondary target horizons (6h, 72h, 168h realized variance) on the existing admissible cached Hyperliquid panel, apply pre-declared multiplicity correction, and emit a family-wise verdict artifact — completing the confirmatory test for `TRACKA-VOL-20261111T234918Z` before any new experiment. If the volatility family cannot confirm funding-conditioned volatility skill, pivot in-session to the liquidation-risk robustness campaign on the 8-coin expansion universe (sealed PASS design, new prereg required before outcomes). Every session must deliver prereg + (build+eval or documented infeasibility+next-attempt) + state updates.

**Execute in this exact order:** Steps 1–6 above, then Step 7 or Step 8 as applicable.

## BOTTLENECKS — STATUS & REMOVAL
| Bottleneck | Status | Removal/action |
|---|---|---|
| Gate 4 Branch 1 (external/legal Binance terms) | BLOCKED, not agent-removable | **Do not wait.** Run Branch 1 only if `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` exists with all required fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, and human/legal attestation → deterministic promotion+validators → on all-green confirmatory Track C multi-split ablation + verdict + state. Verified absent now. |
| Volatility multiplicity family incomplete (secondary horizons unevaluated) | REMOVABLE NOW | Steps 1–5 of this task. Panel exists, prereg frozen, splits fixed. |
| No frozen prereg for untested admissible liquidation robustness claim | REMOVABLE IF NEEDED | If volatility family completes NOT_MET/INCONCLUSIVE/infeasible, next campaign: new prereg for liquidation-intensity robustness on 8-coin expansion universe (cached ironflow labels + funding + candles) or alternate volatility window. |
| Competing root handoff docs / session ambiguity | REMOVED | This file is sole durable root handoff; redirect files in place. |

## COMPLETED / SEALED — DO NOT REOPEN, RETUNE, OR RELITIGATE
- Track A liquidation expansion `TRACKA-HL-EXPANSION-20261111T195500Z` = **PASS** (C2 vs B1 rel QLIKE -19.04%, 95% CI [-5.088,-0.478], n=593, 8 instruments, 3 blocks, 2026-05..2026-10). Sealed.
- Track A volatility primary 24h `TRACKA-VOL-20261111T234918Z` = **NOT_MET** (C2 vs B1 rel QLIKE -1.37%, CI crosses zero, n=19233, 9 instruments, 3 blocks, 2026-05..2026-10). Sealed.
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
- Volatility panel: `research_state/tracka_vol_panel_20261111T234918Z.parquet` (sha256 `bd6b9924...`), `research_state/tracka_vol_panel_build_report_20261111T234918Z.json`
- Volatility prereg: `research_state/tracka_prereg_volatility_20261111T234918Z.json` (frozen pre-outcomes)
- Evaluation scripts: `scripts/run_volatility_funding_eval.py`, `src/volatility/eval.py`, `src/volatility/block_bootstrap.py`, `src/volatility/features_ext.py`
- Templates: `research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json`, `research_state/evaluation_summary_TRACKA-HL-expansion-20261111T202344Z.md`

**Execute Step 1 now.**
