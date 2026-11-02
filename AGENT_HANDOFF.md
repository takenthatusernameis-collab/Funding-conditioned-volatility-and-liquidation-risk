# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-02T00:13:12Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Funding-conditioned volatility → liquidation risk. The repo name is the directive.
**BRANCH/HEAD:** main @ fb5ebec8
**HANDOFF ID:** FCLR-HANDOFF-070-20261102T001312Z
**SUPERSEDES:** FCLR-HANDOFF-068-20261102T000726Z (AGENT_HANDOFF_OUTCOME.md narrative consolidated here; its HEAD a0135068 does not exist in git — that parallel session's artifacts are recorded below and retired).

**STATUS:** Tests 27/27 PASS at HEAD fb5ebec8. Working tree clean except `__pycache__` (harmless). All heavy confirmatory work from both parallel sessions is complete and artifacted; neither session closed out. Dual-handoff bottleneck removed — this file is now the single source of truth.

## CAMPAIGN FCLR-LIQMICRO-002 — COMPLETE (all steps done)
Real Hyperliquid funding integrated (9 coins x 8668 records, fundingRate.std()>0 confirmed). Degenerate zeroed-funding bug FIXED in `src/analysis/liqmicro/features.py` (now merges on symbol+hour UTC, no silent zeroing). D1-D3 TESTED on 93,504 symbol-hour obs x 199 symbols; panel.funding_rate std 6.98e-06 > 0; D2 funding_abs non-zero; D3 clustering_by_decile populated; BH FDR 4 significant. NO H001 reversal, NO H001 re-test opened. Artifacts: `results/liqmicro_v2/`, `research_state/evaluation_summary_FCLR-LIQMICRO-002.md`, `research_state/pre_registration_FCLR-LIQMICRO-002.md`, `research_state/liqmicro_funding_audit_002.md`.

## CAMPAIGN FCLR-LIQMICRO-003 — ADVERSARIAL RE-AUDIT + ROBUSTNESS (STEPS 1-4 DONE, STEP 5 CLOSEOUT PENDING)
**PRIORITY: P0 | TYPE: HEAVY FUNDING-CONDITIONED RESEARCH | CAMPAIGN: FCLR-LIQMICRO-003 | FIREWALLS ENFORCED**

- Step 1 Sanity: tests 27/27 PASS. Tree clean except `__pycache__`.
- Step 2 Leakage audit: `research_state/leakage_audit_liqmicro_002.md` — VERDICT PASS (no look-ahead, trailing-only funding zscore, funding merge fixed without zeroing, UTC alignment, no censoring-as-negatives). D1 numerical instability and D3 decile sparsity noted as specification/sparsity concerns, not leakage.
- Step 3 Robustness: `research_state/robustness_liqmicro_002.md` — alternative zscore windows, merge strategies, coin/time subsample stability, placebo shifts documented; D3 decile sparsity (median funding_abs=0, funding_sign 80% zero) explained; core fix stable, no leakage.
- Step 4 Cross-track decision log: `research_state/cross_track_decision_log.md` updated 2026-11-02T00:08:30Z "FCLR-LIQMICRO-003 STARTED"; firewall intact (Hyperliquid-only, no Binance, no H001/FCLR-003/FCLR-010 re-test).
- Step 5 Report + next task: **PENDING** — mark `research_state/experiment_frontier.json` FCLR-LIQMICRO-003 status COMPLETE with final artifacts + gate states; verify sealed artifacts unchanged; record final gate states; leave next task below.

## OTHER TRACKS — FINAL STATES (all confirmatory work complete)
| Track | Hypothesis | Status | Basis |
|-------|------------|--------|-------|
| C | FCLR-H001 funding-conditioned volatility | NOT_SUPPORTED — CONFIRMATORY CLOSED | FCLR-001..009 exhausted; FCLR-008 C2 vs B1 +4.30% rel QLIKE but CI crosses zero; gate NOT_MET; overlay INELIGIBLE. No reopen without new admissible data + pre-registration. |
| A | FCLR-H004 observed liquidations | REOPENED — FCLR-010 GATE PASSED | `ironflow_hyperliquid_liquidation_events` census admissible (rubric passed). FCLR-010 executed: C2 vs B1 mean diff -0.003077, CI approx [-0.004892,-0.001263] excludes zero, rel reduction 2.21% >= 2% floor, n=199, 5 blocks. Artifacts: `research_state/evaluation_summary_FCLR010.md`, `research_state/independent_recompute_audit_FCLR010.md`, `research_state/fclr010_leakage_audit.md`, `research_state/fclr010_diagnostics.md`. Overlay ELIGIBLE but remains HYPOTHETICAL ONLY (no profitability claim) — `research_state/evaluation_summary_tracka_overlay_001.md`, `research_state/pre_registration_tracka_overlay_20261101T165900Z.md`. Test window sealed; no re-inspection/tuning. |
| B | FCLR-H003 modeled boundary breaches | CLOSED_NEGATIVE | No incremental skill after Holm (FCLR-H003-EXT-001); codepath separation irrefutable; Track B != observed liquidations. |
| H002 | funding-extreme correction time | PERMANENT BLOCK | SSRN HTTP 403; full methodology not reconstructible from admissible sources. No reopen unless SSRN accessible + pre-registration before outcome inspection. |

## HARD CONSTRAINTS
- NO Binance merge; NO reopening H001/FCLR-003/FCLR-010; NO Track A/B/C label merging.
- All 27 tests must PASS. No changes to `.github/workflows/`.
- Only admissible data: ironflow liquidations (Hyperliquid) + Hyperliquid fundingHistory API.
- Never silently zero missing funding — drop/flag with justification.
- Sealed artifacts unchanged; write only new `*_003*` artifacts.

## NEXT FOCUS CAMPAIGN — FCLR-LIQMICRO-003 STEP 5 CLOSEOUT (IMMEDIATE NEXT TASK)
**Deadline:** complete this session. This is heavy verification work, not status-only reporting. Every step produces a concrete artifact.

Run in strict order:
1. `git log --oneline -1 && git status --short && python -m unittest discover -s tests -v` → must remain 27/27 PASS; tree clean except `__pycache__`.
2. Update `research_state/experiment_frontier.json`: set FCLR-LIQMICRO-003 status `COMPLETE`, record final artifacts (`leakage_audit_liqmicro_002.md`, `robustness_liqmicro_002.md`) and gate states (all tracks above); bump `updated_at`.
3. Verify sealed artifacts unchanged: confirm `results/liqmicro_v2/panel_liqmicro_v2.{csv,parquet}` and `results/liqmicro_v2/descriptive_stats_v2.csv` untouched since FCLR-LIQMICRO-002 (no rewrites; produce only new `*_003*` artifacts if any).
4. Update `research_state/cross_track_decision_log.md` with FCLR-LIQMICRO-003 completion + final gate states + firewall compliance.
5. Leave explicit next task in this file (below) — after closeout, NO further confirmatory work is possible without a NEW admissible unauthenticated liquidation/funding data source passing the rubric AND a new protocol pre-registered before outcome inspection (RESEARCH_PROMPT §16). Record that trigger as the resume condition.

## SINGLE HIGHEST-VALUE NEXT TASK (after closeout)
None within current admissible data — all confirmatory gates resolved (Track C NOT_SUPPORTED closed; Track A FCLR-010 gate PASSED / overlay hypothetical-only; Track B CLOSED_NEGATIVE; H002 permanent block; FCLR-LIQMICRO-002/003 complete). Resume only on: (a) new admissible unauthenticated liquidation/funding source passing the source rubric (≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness, license OK), or (b) SSRN H002 methodology becoming accessible. In either case: pre-register a new experiment ID BEFORE outcome inspection, then execute. Until then, this handoff is the stable closeout point.
