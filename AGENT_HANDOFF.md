# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-02T01:30:00Z
**INITIAL TASK (NEXT SESSION):** FCLR-NEXT-002 source discovery COMPLETE_NO-GO — all 8 source families probed (Binance alt paths, Bybit, OKX, Deribit, academic archives, GitHub raw, Hugging Face, CryptoDataDownload), 8 source_probe_FCLR-NEXT-002_*.md artifacts written, cross_track_decision_log.md updated. NO NEW admissible unauthenticated liquidation source beyond ironflow/hyperliquid-liquidations (already GO, used in FCLR-010) found. All confirmatory gates resolved. Stable closeout point — no confirmatory work resumes without a NEW admissible source passing the rubric or SSRN H002 methodology access.
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Funding-conditioned volatility → liquidation risk. The repo name is the directive.
**BRANCH/HEAD:** main @ 42e798cb
**HANDOFF ID:** FCLR-HANDOFF-072-20261102T013000Z
**SUPERSEDES:** FCLR-HANDOFF-071-20261102T010437Z (AGENT_HANDOFF.md v071: FCLR-NEXT-002 not yet executed; now COMPLETE_NO-GO, no new source found).

**STATUS:** Tests 27/27 PASS at HEAD 42e798cb. Working tree clean except `__pycache__` (harmless, not committed). All heavy confirmatory work complete and artifacted. FCLR-LIQMICRO-002 COMPLETE, FCLR-LIQMICRO-003 COMPLETE, FCLR-NEXT-002 COMPLETE_NO-GO. FCLR-010 gate PASSED (Track A), FCLR-OVERLAY-001 EXECUTED (hypothetical only). Track C H001 NOT_SUPPORTED (CONFIRMATORY_CLOSED), Track B CLOSED_NEGATIVE, H002 PERMANENT_BLOCK. No parallel sessions remain open. Single durable handoff established — stable closeout point.

## CAMPAIGN FCLR-LIQMICRO-002 — COMPLETE (all steps done)
Real Hyperliquid funding integrated (9 coins x 8668 records, fundingRate.std()>0 confirmed). Degenerate zeroed-funding bug FIXED in `src/analysis/liqmicro/features.py` (now merges on symbol+hour UTC, no silent zeroing). D1-D3 TESTED on 93,504 symbol-hour obs x 199 symbols; panel.funding_rate std 6.98e-06 > 0; D2 funding_abs non-zero; D3 clustering_by_decile populated; BH FDR 4 significant. NO H001 reversal, NO H001 re-test opened. Artifacts: `results/liqmicro_v2/`, `research_state/evaluation_summary_FCLR-LIQMICRO-002.md`, `research_state/pre_registration_FCLR-LIQMICRO-002.md`, `research_state/liqmicro_funding_audit_002.md`.

## CAMPAIGN FCLR-LIQMICRO-003 — ADVERSARIAL RE-AUDIT + ROBUSTNESS (STEPS 1-5 COMPLETE)
**PRIORITY: P0 | TYPE: HEAVY FUNDING-CONDITIONED RESEARCH | CAMPAIGN: FCLR-LIQMICRO-003 | FIREWALLS ENFORCED | CLOSEOUT COMPLETE**

- Step 1 Sanity: tests 27/27 PASS. Tree clean except `__pycache__`.
- Step 2 Leakage audit: `research_state/leakage_audit_liqmicro_002.md` — VERDICT PASS (no look-ahead, trailing-only funding zscore, funding merge fixed without zeroing, UTC alignment, no censoring-as-negatives).
- Step 3 Robustness: `research_state/robustness_liqmicro_002.md` — alternative zscore windows, merge strategies, coin/time subsample stability, placebo shifts documented; D3 decile sparsity explained; core fix stable, no leakage.
- Step 4 Cross-track decision log: `research_state/cross_track_decision_log.md` updated 2026-11-02T01:04:00Z "FCLR-LIQMICRO-003 CLOSEOUT COMPLETE"; firewall intact.
- Step 5 Report + next task: **COMPLETE** — `research_state/experiment_frontier.json` FCLR-LIQMICRO-003 status COMPLETE with final artifacts (`leakage_audit_liqmicro_002.md`, `robustness_liqmicro_002.md`) and sealed-panel integrity block (md5 hashes of `results/liqmicro_v2/panel_liqmicro_v2.{csv,parquet}`, `descriptive_stats_v2.csv`; mtimes 2026-11-02T00:05 unchanged; verdict UNCHANGED — no rewrites, no new `*_003*` outputs written to `results/liqmicro_v2/`); `research_state/cross_track_decision_log.md` updated with completion + final gate states + firewall compliance.

## OTHER TRACKS — FINAL STATES (all confirmatory work complete)
| Track | Hypothesis | Status | Basis |
|-------|------------|--------|-------|
| C | FCLR-H001 funding-conditioned volatility | NOT_SUPPORTED — CONFIRMATORY CLOSED | FCLR-001..009 exhausted; FCLR-008 C2 vs B1 +4.30% rel QLIKE but CI [-0.029938,0.000524] crosses zero; gate NOT_MET; overlay INELIGIBLE. No reopen without new admissible data + pre-registration. |
| A | FCLR-H004 observed liquidations | REOPENED — FCLR-010 GATE PASSED | `ironflow_hyperliquid_liquidation_events` census admissible (rubric passed). FCLR-010: C2 vs B1 mean diff -0.003077, CI [-0.004892,-0.001263] excludes zero, rel reduction 2.21% >= 2% floor, n=199, 5 blocks. Overlay ELIGIBLE but HYPOTHETICAL ONLY (no profitability claim). Test window sealed; no re-inspection/tuning. |
| B | FCLR-H003 modeled boundary breaches | CLOSED_NEGATIVE | No incremental skill after Holm (FCLR-H003-EXT-001); codepath separation irrefutable; Track B != observed liquidations. |
| H002 | funding-extreme correction time | PERMANENT BLOCK | SSRN HTTP 403; full methodology not reconstructible from admissible sources. Direction reproduced (p=0.0792) but not significant; not confirmatory. |

## HARD CONSTRAINTS
- NO Binance merge; NO reopening H001/FCLR-003/FCLR-010; NO Track A/B/C label merging.
- All 27 tests must PASS. No changes to `.github/workflows/`.
- Only admissible data: ironflow liquidations (Hyperliquid) + Hyperliquid fundingHistory API.
- Never silently zero missing funding — drop/flag with justification.
- Sealed artifacts unchanged; write only new `*_003*` artifacts.

## NEXT FOCUS CAMPAIGN — FCLR-NEXT-002: NEW ADMISSIBLE DATA SOURCE DISCOVERY — COMPLETE_NO-GO
**Executed:** 2026-11-02T01:30:00Z. All 8 source families probed with concrete unauthenticated endpoints:
1. Alternative Binance paths (liquidationSnapshot/, liquidations/, liquidationHistory/, forceLiquidation/, monthly/) — all HTTP 404; fapi forceOrders 451 → NO-GO
2. Bybit (linear/liquidation/, spot/liquidation/, archive/linear/liquidation/) — all 404 → NO-GO
3. OKX (static.okx.com 403, /api/v5/public/data 404) → NO-GO
4. Deribit (historical.deribit.com connection failed) → NO-GO
5. Academic archives (Zenodo/OSF/arXiv) — no crypto perp liquidation datasets → NO-GO
6. GitHub raw (code search 401, no census dataset) → NO-GO
7. Hugging Face — ironflow/hyperliquid-liquidations GO (CC BY 4.0, 185-199 symbols, 12 monthly blocks 2025-11..2026-10, census) — ALREADY USED in FCLR-010, NOT new. All others NO-GO (ochinimus exhausted, DeFi/heatmap wrong type, linxy is price not labels)
8. CryptoDataDownload — no liquidation/futures links → NO-GO
**Conclusion:** NO NEW admissible unauthenticated liquidation source beyond ironflow found. Track A open only via ironflow (FCLR-010 COMPLETE, gate PASSED, overlay EXECUTED). All confirmatory gates resolved. Stable closeout point.

## SINGLE HIGHEST-VALUE NEXT TASK (after FCLR-NEXT-002)
None within current admissible data — all confirmatory gates resolved. Resume only on: (a) new admissible unauthenticated liquidation/funding source passing the rubric (>=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness, license OK), or (b) SSRN H002 methodology becoming accessible. In either case: pre-register a new experiment ID BEFORE outcome inspection, then execute. Until then, this handoff is the stable closeout point. No further source discovery, no confirmatory re-test, no track merging, no workflow changes.
