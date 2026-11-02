# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-02T00:07:26Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Funding-conditioned volatility → liquidation risk. The repo name is the directive. Funding-conditioned analysis is #1.
**BRANCH/HEAD:** main @ 2841cebf
**HANDOFF ID:** FCLR-HANDOFF-068-20261102T000726Z
**SUPERSEDES:** FCLR-HANDOFF-067-20261102T000402Z

**STATUS:** Tests 27/27 PASS. FCLR-LIQMICRO-002 COMPLETE. Real Hyperliquid funding integrated (9 coins x 8668 records, fundingRate.std()>0 confirmed in research_state/liqmicro_funding_audit_002.md). Degenerate zeroed-funding bug FIXED in src/analysis/liqmicro/features.py (was zeroing funding_rate/funding_abs; now merges on symbol+hour UTC). D1-D3 TESTED on 93,504 symbol-hour obs x 199 symbols; panel.funding_rate std 6.98e-06 > 0; D2 funding_abs non-zero (was 0.0); D3 clustering_by_decile populated (was {}); BH FDR 4 significant. NO H001 reversal, NO H001 re-test opened. Sealed artifacts intact. Working tree has only `__pycache__` modifications (harmless).

## CAMPAIGN FCLR-LIQMICRO-002 — COMPLETE (all 4 steps done)

**Step 1 Sanity:** DONE — `git log --oneline -1 && git status --short && python -m unittest discover -s tests -v` → 27/27 PASS at HEAD 2841cebf. Working tree clean except `__pycache__`.

**Step 2 Fetch real funding:** DONE — `scripts/hyperliquid_funding_fetch.py` fetched 9 coins (BTC, ETH, SOL, BNB, XRP, AVAX, DOGE, LINK, SUI), 8668 records each, 2025-11-01..2026-10-30, cached to `research_state/data_cache/hyperliquid_funding/*.json`. Audit: `research_state/liqmicro_funding_audit_002.md` — fundingRate.std() > 0 for all, SHA-256 recorded. GATE PASSED: >=5 overlapping symbols, fundingRate.std() > 0.

**Step 3 Wire funding into pipeline:** DONE — `src/analysis/liqmicro/features.py::add_funding_features` already merges funding_df on symbol+hour (UTC), computes funding_rate/sign/abs/zscore, no silent zeroing. `src/analysis/liqmicro/ingest.py::HyperliquidFundingIngestor` loads JSON cache. GATE PASSED: panel['funding_rate'].std() > 0, no column all zeros.

**Step 4 Re-run with real funding:** DONE — `scripts/run_liqmicro_v2.py` executed 2026-11-02T00:05:31Z. Output to `results/liqmicro_v2/` (panel_liqmicro_v2.csv/.parquet, descriptive_stats_v2.csv). Pre-registration written: `research_state/pre_registration_FCLR-LIQMICRO-002.md`. Evaluation summary: `research_state/evaluation_summary_FCLR-LIQMICRO-002.md`. D1-D3 results with BH FDR (4 significant). GATE PASSED: funding features show variation (std>0), all tests 27/27.

**Step 5 Validate, integrate, report:** PARTIAL — `research_state/experiment_frontier.json` updated with FCLR-LIQMICRO-002 entry (status COMPLETE). `research_state/cross_track_decision_log.md` NOT yet updated with FCLR-LIQMICRO-002 decision. Next session should complete Step 5.

## NEXT FOCUS CAMPAIGN — FCLR-LIQMICRO-003 (ADVERSarial RE-AUDIT + DEEPER ROBUSTNESS)

**PRIORITY: P0 | TYPE: HEAVY FUNDING-CONDITIONED RESEARCH | CAMPAIGN: FCLR-LIQMICRO-003 | FIREWALLS ENFORCED**

**MANDATE:** Subject the FCLR-LIQMICRO-002 panel to adversarial leakage/quality audits and deeper robustness checks before any result is treated as reliable. Do NOT reopen H001/FCLR-003/FCLR-010. Do NOT merge Binance. Only ironflow liquidations + Hyperliquid funding. Every action must produce concrete artifacts with file:line, provenance, computed values, and acceptance checks. Do heavy verification work — do not shortcut.

### EXECUTE IN STRICT ORDER

#### Step 1: Sanity (2-5 min)
- [ ] `git log --oneline -1 && git status --short && python -m unittest discover -s tests -v` → must remain 27/27 PASS
- [ ] Working tree clean except `__pycache__`

#### Step 2: Leakage audit on FCLR-LIQMICRO-002 panel (HEAVY)
- [ ] Write `research_state/leakage_audit_liqmicro_002.md` covering: future-row perturbation cannot change earlier features/forecasts; funding publication/settlement times and sign handled correctly; no look-ahead in funding zscore (trailing-only); mark/index alignment if used; delisted contracts and symbol migrations retain correct identity; duplicate/out-of-order/missing pages detected; censored events not treated as completed negatives.
- [ ] Check for look-ahead: verify `hour` timestamp in panel only uses data available at or before that hour; funding rate at hour h must have publication time <= h.
- [ ] Document file:line for each check + computed values.

#### Step 3: Robustness / sensitivity (HEAVY)
- [ ] Re-run D1-D3 with alternative specifications: different rolling windows for funding zscore (e.g., 30d, 90d, 180d); different funding merge strategies (drop vs forward-fill with justification); subsample stability (split by coin, by time block); placebo funding shifts (±1-2 periods).
- [ ] Write `research_state/robustness_liqmicro_002.md` with results for each specification, file:line references, computed values.
- [ ] **GATE:** Core D1-D3 direction/magnitude stable across specifications; no single coin or time block drives the result.

#### Step 4: Cross-track decision log update
- [ ] Update `research_state/cross_track_decision_log.md` documenting FCLR-LIQMICRO-002 completion and FCLR-LIQMICRO-003 audit decision, firewall compliance (Hyperliquid-only, no Binance, no H001 re-test).

#### Step 5: Report + next task
- [ ] Confirm `git log --oneline -1 && git status --short && python -m unittest discover -s tests -v` → 27/27 PASS
- [ ] Update `research_state/experiment_frontier.json` with FCLR-LIQMICRO-003 status
- [ ] Leave explicit next task in AGENT_HANDOFF.md

## HARD CONSTRAINTS
- NO Binance merge
- NO reopening H001/FCLR-003/FCLR-010
- All 27 tests must PASS
- No changes to `.github/workflows/`
- Only admissible data: ironflow liquidations (Hyperliquid) + Hyperliquid fundingHistory API
- Never silently zero missing funding - drop/flag with justification
- Sealed artifacts unchanged; write only new `*_003*` artifacts
- Hyperliquid-only cross-track firewall

## REQUIRED END-OF-SESSION OUTPUT
1. `git log --oneline -1 && git status --short && python -m unittest discover -s tests -v` (must be 27/27)
2. `research_state/leakage_audit_liqmicro_002.md` path + findings
3. `research_state/robustness_liqmicro_002.md` path + results
4. Code changes (files + key diffs/line refs) for any audit/robustness additions
5. Updated `research_state/cross_track_decision_log.md`
6. Updated `research_state/experiment_frontier.json` with FCLR-LIQMICRO-003

## SINGLE HIGHEST-VALUE NEXT TASK
**FCLR-LIQMICRO-003:** Adversarial leakage/quality audit + robustness sensitivity on the FCLR-LIQMICRO-002 panel. This directly matches the repo name (funding-conditioned), prevents premature promotion of preliminary results, and is the only path to making the funding-conditioned finding trustworthy before any further work.
