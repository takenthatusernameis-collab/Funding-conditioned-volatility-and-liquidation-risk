# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-02T01:06:28Z
**INITIAL TASK (NEXT SESSION):** Execute Campaign FCLR-NEXT-002 source discovery — run steps 1-8 unauthenticated probes across 8 source families, write one artifact per family to research_state/source_probe_FCLR-NEXT-002_<source>.md, record GO/NO-GO per rubric; update cross_track_decision_log.md; leave explicit next task. No confirmatory work resumes until a source passes the rubric.
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Funding-conditioned volatility → liquidation risk. The repo name is the directive.
**BRANCH/HEAD:** main @ 42e798cb
**HANDOFF ID:** FCLR-HANDOFF-071-20261102T010437Z
**SUPERSEDES:** FCLR-HANDOFF-070-20261102T010400Z (AGENT_HANDOFF.md v070: stale HEAD fb5ebec8, FCLR-LIQMICRO-003 Step 5 left PENDING despite cross_track_decision_log.md recording COMPLETE at 2026-11-02T01:04:00Z; dual-handoff/parallel-session artifacts retired here — this file is now the single source of truth).

**STATUS:** Tests 27/27 PASS at HEAD 42e798cb. Working tree clean except `__pycache__` (harmless, not committed). All heavy confirmatory work is complete and artifacted; FCLR-LIQMICRO-003 closeout (Step 5) now COMPLETE. No parallel sessions remain open. Single durable handoff established.

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

## NEXT FOCUS CAMPAIGN — FCLR-NEXT-002: NEW ADMISSIBLE DATA SOURCE DISCOVERY (HEAVY VERIFICATION WORK)
**Deadline:** execute this session; do not mark complete without concrete probe artifacts per source family. This is heavy verification work, not status-only reporting. Every step produces a concrete artifact.

Resume condition (RESEARCH_PROMPT §16): confirmatory program remains BLOCKED until a NEW admissible unauthenticated liquidation/funding source passes the rubric (>=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness, license OK) OR SSRN H002 methodology becomes accessible. Until then, no further confirmatory cell exists. The heavy work now is systematic source discovery across materially distinct source families/methods — repeating the same failed endpoint is NOT a distinct route.

Run in strict order:
1. `git log --oneline -1 && git status --short && python -m unittest discover -s tests -v` → must remain 27/27 PASS; tree clean except `__pycache__`.
2. For each candidate source family below, execute one unauthenticated probe (bounded download, exponential backoff, max retry budget, honor rate limits). Record: exact URL/endpoint, access date, test method, no-auth result (HTTP 200 / 404 / 451 / etc.), license/terms, fields, earliest/latest timestamp, observed cadence, symbol/venue coverage, known gaps, file hashes or ETags where feasible, rejection reason if inadmissible. Write one artifact per source family to `research_state/source_probe_FCLR-NEXT-002_<source>.md`.
   - **#1 Alternative Binance paths:** `data.binance.vision` — liquidationHistory/, liquidations/, forceLiquidation/, monthly/ (beyond the 404 liquidationSnapshot already ruled out).
   - **#2 Bybit:** public archive/linear/liquidation/ trading/liquidation/ locations.
   - **#3 OKX:** public data endpoints, static.okx.com CDN historical liquidation/klines.
   - **#4 Deribit:** historical.deribit.com/ historical perp data.
   - **#5 Academic/institutional archives:** Zenodo, OSF, arXiv supplements (dataset files, unauthenticated GET).
   - **#6 GitHub raw:** public repos containing CSV/Parquet liquidation or perp mark-price data (raw content, unauthenticated).
   - **#7 Hugging Face datasets:** unauthenticated HF API search + download for liquidation/perp datasets.
   - **#8 CryptoDataDownload / other venue-native archives:** all products, unauthenticated downloads.
3. Acceptance per source: GO only if concrete download path confirmed (HTTP 200, no key/account) AND coverage >=5 symbols AND >=3 non-overlapping 30-day blocks AND documented completeness (census vs sample characterized) AND license OK AND no sealed-hold reuse.
4. If ANY source reaches GO: pre-register a NEW experiment ID (`FCLR-NEXT-XXX`) BEFORE inspecting outcomes; then execute the frozen protocol on that source. Document pre-registration in `research_state/pre_registration_FCLR-NEXT-*.md`; update `experiment_frontier.json`; do not inspect label-outcome relationships before split freeze.
5. If ALL routes exhausted: document a structural blocker with evidence per route in `research_state/liquidation_source_campaign.md` and `research_state/track_a_final_block_proof.md`; update `experiment_frontier.json` blocked_cells; leave this handoff as the stable closeout point. Do NOT write another blocker memo and wait if a valid bounded free-data/diagnostic task remains — execute it.
6. Update `research_state/cross_track_decision_log.md` with probe outcomes + firewall compliance + resume condition.
7. Leave explicit next task in this file (below).

## SINGLE HIGHEST-VALUE NEXT TASK (after source discovery)
None within current admissible data — all confirmatory gates resolved. Resume only on: (a) new admissible unauthenticated liquidation/funding source passing the rubric (>=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness, license OK), or (b) SSRN H002 methodology becoming accessible. In either case: pre-register a new experiment ID BEFORE outcome inspection, then execute. Until then, this handoff is the stable closeout point.
