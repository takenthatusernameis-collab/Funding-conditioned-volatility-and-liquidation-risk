# SINGLE DURABLE HANDOFF — NEXT AGENTIC WORK SESSION
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Handoff timestamp (UTC):** 2026-11-11T21:12:58Z
**Status:** AUTHORITATIVE. Execute this file only. Treat `AGENT_HANDOFF.md`, `FOCUS_CAMPAIGN.md`, `NEXT_SESSION_TASK.md` as redirects.

## INITIAL TASK MESSAGE (EXECUTE NOW — NO STATUS-ONLY)
**Priority (inferred from repo name):** advance **funding-conditioned volatility forecasting** on an admissible, untested Hyperliquid panel (co-priority liquidation-risk only where admissible). Produce substantive artifacts + atomic state updates this session. Do **not** idle, do **not** relitigate closed/sealed results.

**Remove bottlenecks now:**
- **Gate 4 (external/legal, BLOCKED):** only if `research_state/fclr016_local_audit/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` exists with all 8 fields, `fabricated=false`, `status=RESOLVED_VERIFIED`, and human/legal attestation → run Branch 1 deterministically (promotion + `--expect-go` validators → on all-green GO run confirmatory Track C multi-split ablation, emit verdict, atomic state updates). Verified absent now (only `_partial`/probe/BLOCKED/UNRESOLVED artifacts). **Do not guess, do not set `fabricated=true`.**
- **Primary blocker to real progress:** no frozen prereg for an **untested admissible funding-conditioned volatility** claim. **Default = Branch 2 below.**
- **Avoid churn:** reuse `research_state/data_cache/` (Hyperliquid funding/candles, ironflow). No redundant polling; bounded first-time unauthenticated fetches only if strictly required by frozen prereg, with `.accessed.json` + `.sha256`.

## BRANCH 2 — MANDATORY CAMPAIGN: `GAP-VOLATILITY-UNTESTED-ADMISSIBLE-PANELS`
Execute in strict order. **No outcome inspection before prereg freeze.**

1. **Freeze volatility prereg (REQUIRED, before outcomes):** create `research_state/tracka_prereg_volatility_<UTC>.json` and `.md`.
   - New hypothesis `H_tracka_hl_volatility_forecast_<UTC>` (distinct from sealed H1/Track B/C). Venue `hyperliquid_perpetuals`, no Binance/2024 conflation.
   - Use cached admissible Hyperliquid candles/funding (and observed ironflow labels only if explicitly needed and admissible; no modeled/proxy/synthetic labels). Choose **untested** universe/window/symbols not exhausted by closed liquidation designs.
   - Target: pre-registered next-24h realized volatility from 1h candles (causal formula, no leakage/lookahead). State computability preconditions.
   - Contrast: **B1 (RV-only baseline)** vs **C2 (funding-conditioned)** or justified prereg alternative. Metric e.g. QLIKE (pre-registered), min materiality/rel improvement, 95% block-bootstrap CI.
   - Splits: chronological with **>=7d embargo**, **>=3 non-overlapping 30d test blocks**, **>=5 paired instruments** (or explicit hard infeasibility if minima cannot be met).
   - Hard infeasibility rule + forbidden actions: no threshold-shopping, no sealed-holdout reuse, no outcome peeking.
2. **Bounded acquisition (only if missing):** cache-first audit; fetch only strictly required missing inputs with provenance + acquisition/gap report.
3. **Deterministic panel build:** emit `research_state/tracka_vol_panel_<UTC>.parquet` + `research_state/tracka_vol_panel_build_report_<UTC>.json` (hashes, coverage by symbol/period, embargo/leakage notes). No evaluation before panel matches prereg.
4. **Pre-registered evaluation:** run B1 vs C2 per prereg (bootstrap seed/CI, minima/materiality). Emit `research_state/evaluation_summary_TRACKA-VOL-<UTC>.md` with verdict **MET / NOT_MET / INADMISSIBLE** and full evidence.
5. **Atomic state update (MANDATORY):** update `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md` (addendum). Preserve all sealed/closed records; never mutate closed verdicts.
6. **If INADMISSIBLE — do NOT stop:** emit concrete infeasibility artifact with exact evidence, update state, then **immediately preregister and execute the next best admissible untested volatility (or liquidation) claim** in-session with Steps 1–5. Continuous heavy work, not status.

## DO NOT RELITIGATE (CLOSED/SEALED)
- Track A liquidation: 9-symbol 2026-05..2026-10 **NOT_MET** (`evaluation_summary_TRACKA-HL-20261111T160124Z.md`); early 2025-11..2026-04 **INADMISSIBLE** (`evaluation_summary_TRACKA-HL-early-infeasible-20261111T193500Z.md`). Expansion **PASS** recorded (`TRACKA-HL-EXPANSION-20261111T195500Z`, 8 symbols, 2026-05..2026-10) — do not rerun/retune.
- Track B/C 2024 and H1/FCLR-002/003 sealed/closed negative contexts remain immutable.

## HARD BANS (BINDING)
- No outcome inspection before freeze/prereg. No threshold-shopping. No sealed-holdout reuse.
- No Binance/2024 conflation; venue/source must match artifacts.
- No modeled/proxy/synthetic liquidation labels as observed.
- No `.github/workflows` edits. No redundant network polling.
- No agent-set `RESOLVED_VERIFIED`/`fabricated=true`; no Gate 4 bypass.
- **No status-only output.**

## KEY REFS
- Caches: `research_state/data_cache/hyperliquid_candles/`, `research_state/data_cache/hyperliquid_funding/`, `research_state/data_cache/ironflow_events/`
- State: `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/final_confirmatory_verdict.md`
- Gate 4 audit dir: `research_state/fclr016_local_audit/`
- Example Track A eval/panel patterns: `scripts/tracka_hl_evaluate_successor.py`, `scripts/tracka_hl_build_panel_with_rv.py`, `research_state/tracka_prereg_hyperliquid_expansion_20261111T195500Z.json`

**Execute now:** Branch 1 only if Gate 4 RESOLVED trigger present; else begin Branch 2 at Step 1 (freeze volatility prereg) immediately.
