# SINGLE DURABLE HANDOFF — INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Handoff timestamp (UTC):** 2026-11-11T23:41:47Z
**Status:** AUTHORITATIVE. Execute this file only. `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` are redirects.

## BOTTLENECK CHECK (THIS SESSION)
- Gate 4 Branch 1 trigger: **NOT PRESENT** — `research_state/fclr016_local_audit/` contains no `fclr016_v5_terms_evidence_RESOLVED_*` with required RESOLVED_VERIFIED/legal attestation/fabricated=false; only `_BLOCKED`/`_UNRESOLVED`/`_partial`/probe artifacts exist. **Do not wait/poll; proceed Branch 2.**
- Stale/competing handoff surfaces: **REMOVED** — root `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` redirect to this file.
- Volatility campaign artifacts: **NOT STARTED** (no `tracka_prereg_volatility_*`, `tracka_vol_panel_*`, or `evaluation_summary_TRACKA-VOL-*` in `research_state/`).

## INITIAL TASK (START NOW — HEAVY WORK, NO STATUS-ONLY OUTPUT)
**Objective (inferred from repo name):** produce a pre-registered, evidence-backed result for **funding-conditioned volatility forecasting** on an **admissible, untested Hyperliquid panel** (cached data). This session must end with substantive artifacts and atomic state updates, not a status summary.

**Execute in this exact order:**
1. **Freeze prereg BEFORE any outcome computation (REQUIRED).** Create `research_state/tracka_prereg_volatility_20261111T234147Z.json` (+ matching `.md` summary) defining: new hypothesis id, Hyperliquid-only venue, estimand = next-24h realized volatility/variance from 1h mark-price candles (causal), ex-ante symbol universe/selection rule from cached-admissible coins, B1 (RV-only) vs C2 (RV+funding; optionally premium/ema_dist as pre-specified in C2) primary contrast, metric QLIKE, materiality **>=2% relative reduction** with **95% block-bootstrap CI excluding zero** in favor of C2, **>=5 paired instruments** and **>=3 non-overlapping 30-day test blocks** with **>=7-day embargo**, split scheme/seed, and hard INADMISSIBLE rule. **No outcome peeking, no threshold-shopping, no post-outcome prereg edits.**
2. **Bounded data audit/build (cache-first).** Use cached admissible inputs only unless a frozen prereg gap requires a bounded first-time unauthenticated fetch with provenance (`.accessed.json`+`.sha256`). Recommended admissible core: 10 coins with full 12-month candle+funding cache **AVAX,BNB,BTC,DOGE,ETH,LINK,SOL,SUI,XRP,ADA? verify ex ante** (candle months `2025-11..2026-10` in `research_state/data_cache/hyperliquid_candles/`, funding in `research_state/data_cache/hyperliquid_funding/`). Emit `research_state/tracka_vol_panel_20261111T234147Z.parquet` and `research_state/tracka_vol_panel_build_report_20261111T234147Z.json` (hashes, coverage by symbol/period, RV/funding completeness, leakage/embargo notes). All features causal/trailing-only.
3. **Pre-registered evaluation.** Run B1 vs C2 per frozen prereg (fixed bootstrap seed). Emit `research_state/evaluation_summary_TRACKA-VOL-20261111T234147Z.md` with verdict **MET / NOT_MET / INADMISSIBLE** and full evidence (n, instruments, blocks, point estimates, CI, relative reduction, per-criterion pass/fail).
4. **Atomic state updates (MANDATORY).** Update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, and append addendum to `research_state/final_confirmatory_verdict.md`. Preserve all sealed/closed records; **never mutate closed verdicts**. Record experiment id, prereg path, panel/build/eval artifacts, verdict.
5. **If INADMISSIBLE or blocked at any step:** emit concrete infeasibility artifact with exact evidence, update state, then **immediately preregister and attempt the next best admissible untested claim** (e.g. alternate volatility window/universe or admissible liquidation claim on cached observed data) repeating Steps 1–4 in-session. Do not stop at the first failure.

## BOTTLENECKS — STATUS & REMOVAL
| Bottleneck | Status | Removal/action |
|---|---|---|
| Gate 4 Branch 1 (external/legal Binance terms) | BLOCKED, not agent-removable | **Do not wait.** Run Branch 1 **only** if `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` exists with all required fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, and human/legal attestation → deterministic promotion+validators → on all-green confirmatory Track C multi-split ablation + verdict + state. **Verified absent now.** Never guess, never set `fabricated=true`, never bypass. |
| No frozen prereg for untested admissible funding-conditioned volatility claim | REMOVABLE NOW | **Step 1 of this task.** |
| Data availability for volatility core | REMOVED (cached) | Use caches: `research_state/data_cache/hyperliquid_candles/` (17 coins, 2025-11..2026-10), `research_state/data_cache/hyperliquid_funding/` (17 coins, ~2025-11..2026-10). Cache-first; no redundant polling. |
| Competing root handoff docs / session ambiguity | REMOVED | This file is sole durable root handoff; redirect files in place. |

## COMPLETED / SEALED — DO NOT REOPEN, RETUNE, OR RELITIGATE
- Track A liquidation expansion `TRACKA-HL-EXPANSION-20261111T195500Z` = **PASS** (C2 vs B1 rel QLIKE -19.04%, 95% CI [-5.088,-0.478], n=593, 8 instruments, 3 blocks, 2026-05..2026-10). Sealed.
- Track A 9-symbol 2026-05..2026-10 = **NOT_MET** (closed). Track A early 2025-11..2026-04 = **INADMISSIBLE** (closed).
- Track B/C 2024 and H1/FCLR-002/003 contexts sealed/closed negative; H1 primary NOT_SUPPORTED on tested panels. **Immutable.**

## HARD BANS (BINDING)
- No outcome inspection before prereg freeze. No threshold-shopping. No sealed-holdout reuse.
- No Binance/2024 conflation; Hyperliquid-only venue for this campaign with matching artifacts.
- No modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No redundant network polling. No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- **No status-only output.** Every session must deliver prereg + (build+eval or documented infeasibility+next-attempt) + state updates.

## KEY REFERENCES
- Handoff/state: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md`, `research_state/fclr016_local_audit/`
- Caches: `research_state/data_cache/hyperliquid_candles/`, `research_state/data_cache/hyperliquid_funding/`, `research_state/data_cache/ironflow_events/`
- Patterns/scripts: `scripts/run_volatility_funding_eval.py`, `scripts/tracka_hl_build_panel_with_rv.py`, `scripts/tracka_hl_evaluate_successor.py`, `scripts/run_gate4_v4_exploratory_diag.py`, `src/volatility/features_ext.py`, `src/volatility/eval.py`, `src/volatility/block_bootstrap.py`
- Templates: `research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json`, `research_state/tracka_prereg_hyperliquid_successor_20261111T133430Z.json`

**Execute Step 1 now.**
