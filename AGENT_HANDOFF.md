# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-02T01:12:00Z
**INITIAL TASK (NEXT SESSION):** Execute CAMPAIGN FCLR-REOPEN-READY-001 — build the reopen-trigger watch + sealed-integrity infrastructure so the program resumes correctly and immediately when either reopen condition fires; verify with `python -m unittest discover -s tests -v` (expect 27/27 OK) and the sealed-panel md5 check. NO confirmatory outcome inspection until a trigger fires AND a new experiment is pre-registered AND splits are frozen.
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Funding-conditioned volatility → liquidation risk. The repo name is the directive.
**BRANCH/HEAD:** main @ edc55ed2
**HANDOFF ID:** FCLR-HANDOFF-073-20261102T011200Z
**SUPERSEDES:** FCLR-HANDOFF-072-20261102T013000Z (AGENT_HANDOFF.md v072: stable closeout; superseded to install the reopen-readiness campaign and remove the __pycache__ bottleneck).

## BOTTLENECKS REMOVED (this session)
- Removed 18 tracked `**/__pycache__/*.pyc` files from the git index (scripts/, tests/, src/analysis/liqmicro/). Compiled cache was polluting the working tree and staging area.
- Added `.gitignore` (`__pycache__/`, `*.py[cod]`, `*.pyc`, `.env`, `.DS_Store`) so cache files can never be re-tracked.
- Working tree now clean except untracked `.gitignore` (staged `__pycache__` deletions intentionally left uncommitted — no commit requested).

## STATUS
Tests 27/27 PASS at HEAD edc55ed2. All confirmatory work complete and artifacted. FCLR-LIQMICRO-002 COMPLETE, FCLR-LIQMICRO-003 COMPLETE, FCLR-NEXT-002 COMPLETE_NO-GO. FCLR-010 gate PASSED (Track A), FCLR-OVERLAY-001 EXECUTED (hypothetical only). Track C H001 NOT_SUPPORTED (CONFIRMATORY_CLOSED), Track B CLOSED_NEGATIVE, H002 PERMANENT_BLOCK (SSRN HTTP 403). No parallel sessions open. Single durable handoff — stable closeout point; resume only on a reopen trigger.

## CAMPAIGN FCLR-LIQMICRO-002 — COMPLETE
Real Hyperliquid funding integrated (9 coins x 8668 records, fundingRate.std()>0). Degenerate zeroed-funding bug FIXED in `src/analysis/liqmicro/features.py:29` (merges on symbol+hour UTC, no silent zeroing). D1-D3 TESTED on 93,504 symbol-hour obs x 199 symbols; panel.funding_rate std 6.98e-06 > 0; D2 funding_abs non-zero; D3 clustering_by_decile populated; BH FDR 4 significant. NO H001 reversal, NO H001 re-test opened. Artifacts: `results/liqmicro_v2/`, `research_state/evaluation_summary_FCLR-LIQMICRO-002.md`, `research_state/pre_registration_FCLR-LIQMICRO-002.md`, `research_state/liqmicro_funding_audit_002.md`.

## CAMPAIGN FCLR-LIQMICRO-003 — COMPLETE (adversarial re-audit + robustness)
Steps 1-5 COMPLETE. Leakage audit PASS; robustness documented; sealed-panel integrity block sealed (md5 of `results/liqmicro_v2/panel_liqmicro_v2.{csv,parquet}`, `descriptive_stats_v2.csv`; mtimes 2026-11-02T00:05; verdict UNCHANGED). `research_state/experiment_frontier.json` FCLR-LIQMICRO-003 status COMPLETE. Closeout complete 2026-11-02T00:13:00Z.

## OTHER TRACKS — FINAL STATES
| Track | Hypothesis | Status | Basis |
|-------|------------|--------|-------|
| C | FCLR-H001 funding-conditioned volatility | NOT_SUPPORTED — CONFIRMATORY CLOSED | FCLR-001..009 exhausted; FCLR-008 C2 vs B1 +4.30% rel QLIKE (first positive direction) but CI [-0.029938,0.000524] crosses zero; gate NOT_MET; overlay INELIGIBLE. No reopen without new admissible data + pre-registration. |
| A | FCLR-H004 observed liquidations | REOPENED — FCLR-010 GATE PASSED | ironflow Hyperliquid census admissible. C2 vs B1 mean diff -0.003077, CI [-0.004892,-0.001263] excludes zero, rel Brier reduction 2.21% >= 2% floor, n=199, 5 blocks. Overlay ELIGIBLE but HYPOTHETICAL ONLY. Test window sealed. |
| B | FCLR-H003 modeled boundary breaches | CLOSED_NEGATIVE | No incremental skill after Holm (FCLR-H003-EXT-001); Track B != observed liquidations. |
| H002 | funding-extreme correction time | PERMANENT BLOCK | SSRN HTTP 403; methodology not reconstructible from admissible sources. |

## HARD CONSTRAINTS
- NO Binance merge; NO reopening H001/FCLR-003/FCLR-010 without a reopen trigger + new pre-registration + split freeze.
- All 27 tests must PASS. No changes to `.github/workflows/`.
- Only admissible data: ironflow liquidations (Hyperliquid) + Hyperliquid fundingHistory API.
- Never silently zero missing funding — drop/flag with justification.
- Sealed artifacts unchanged; write only new campaign artifacts.

## NEXT FOCUS CAMPAIGN — FCLR-REOPEN-READY-001 (HEAVY — future agents cannot skip it)
**Reopen triggers (either one resumes confirmatory work; outcome inspection ONLY after pre-registration + split freeze):**
- T1: SSRN H002 methodology accessible (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7529458 returns HTTP 200 with full event definition, censoring rules, volatility-regime split, contract set).
- T2: NEW admissible unauthenticated liquidation/funding source passes the rubric (>=5 symbols, >=3 non-overlapping 30-day blocks, documented completeness, license OK) — ironflow already exploited via FCLR-010 is NOT new.

**Steps (execute all in this session; each produces an artifact):**
- Step 1: Write bounded probe routine `scripts/reopen_probe.py` for T1 (SSRN GET, timeout, exponential backoff, max retry budget) and T2 (re-probe the 8 FCLR-NEXT-002 source families, changed-evidence only — do NOT repeat identical failed endpoints). Record probe outcomes in `research_state/reopen_probe_*.md`.
- Step 2: Pre-write frozen pre-registration template `research_state/pre_registration_REOPEN_TEMPLATE.md` (hypothesis ID, estimand, features, splits, metrics, gate, multiplicity correction, block bootstrap) so no outcome is inspected before pre-registration.
- Step 3: Re-verify sealed-panel integrity (md5 of `results/liqmicro_v2/panel_liqmicro_v2.{csv,parquet}`, `descriptive_stats_v2.csv` vs recorded hashes; mtimes unchanged) each session; record in `research_state/sealed_holdout_integrity.md`.
- Step 4: Acceptance gate — run `python -m unittest discover -s tests -v` (expect 27/27 OK); tree clean except `__pycache__`.

**Acceptance:** `scripts/reopen_probe.py` present; `research_state/pre_registration_REOPEN_TEMPLATE.md` present; sealed-panel integrity verified unchanged; tests 27/27 PASS; `research_state/experiment_frontier.json` and `research_state/cross_track_decision_log.md` updated with campaign status; `AGENT_HANDOFF.md` updated.

**Do NOT:** repeat same failed endpoints; relax the >=2% floor / CI criterion / >=3-block minimum; reopen H001/FCLR-003/FCLR-010 without trigger+pre-registration+split-freeze; merge Track A/B/C labels; describe modeled/synthetic breaches as observed liquidations; change `.github/workflows/`; write another blocker memo and wait — if no trigger fires, execute the next valid independent task (probe/integrity/test) and preserve blocked status.

## SINGLE HIGHEST-VALUE NEXT TASK
Execute CAMPAIGN FCLR-REOPEN-READY-001 Steps 1-4 in this session. Verify: `python -m unittest discover -s tests -v` → 27/27 OK; `md5sum results/liqmicro_v2/panel_liqmicro_v2.csv results/liqmicro_v2/panel_liqmicro_v2.parquet results/liqmicro_v2/descriptive_stats_v2.csv` match recorded hashes; `git status` clean except `.gitignore`. Until T1 or T2 fires, no confirmatory work resumes — this campaign is the standing next task.

## PREVIOUS COMPLETE CAMPAIGNS (record, do not reopen)
- FCLR-010 COMPLETE, FORECAST_GATE_PASSED — Track A observed-liquidation forecast on Hyperliquid ironflow census (199 perps, 12 monthly blocks 2025-11..2026-10).
- FCLR-OVERLAY-001 EXECUTED — hypothetical overlay on frozen FCLR-010 splits (H_COUPLED-001), exp-weighted event exposure reduction 43.985%, no profitability claim.
- FCLR-008 COMPLETE, FORECAST_GATE_NOT_MET — decisive volatility panel 2026-01-01..2026-08-06, C2 vs B1 +4.30% rel QLIKE, CI crosses zero → H001 INCONCLUSIVE.
- FCLR-NEXT-002 COMPLETE_NO-GO — all 8 source families probed, no NEW admissible source beyond ironflow.
