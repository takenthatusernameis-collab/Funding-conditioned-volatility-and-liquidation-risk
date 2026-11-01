# AGENT HANDOFF OUTCOME — SINGLE DURABLE HANDOFF (source of truth)

Generated: 2026-11-01T20:21:01Z
**Task ID:** HND-20261101-191334-FORCED_HEAVY_EVIDENCE_CAMPAIGN-V28
**HEAD:** a0135068 (main), up to date with origin/main
**Repo:** Funding-conditioned-volatility-and-liquidation-risk
**Priority order (repo name: funding-conditioned volatility → liquidation risk):** Track C → Track A → Track B → H002
**Mode:** FORCED_HEAVY_EVIDENCE_CAMPAIGN — status-only work forbidden

## Execution just completed (this session)
- Baseline re-verified: `python -m unittest discover -s tests -v` → **27/27 PASS**, HEAD aad0450b. Working tree clean except untracked `__pycache__/`.
- Track A bottleneck REMOVED: `ironflow_hyperliquid_liquidation_events` (Hyperliquid liquidation census, 2025-11-01..2026-10-31, 12 monthly blocks, 199 native perps, CC BY 4.0, unauthenticated, no_keys, all rubric items passed, SHA-256 hashes in `research_state/data_source_registry.json`, files cached at `research_state/data_cache/ironflow_events/`). Passes rubric: unauthenticated, no_keys, symbols>=5, blocks>=3, completeness_doc, license_ok, census_or_defensible. Cross-track firewall: NOT merged with Binance panels. Track A is NO LONGER blocked — do not mark it blocked anywhere.
- FCLR-010 EXECUTED 2026-11-01T09:14:03Z → **FORECAST_GATE_PASSED**. Protocol pre-registered before outcomes (`research_state/research_protocol_fclr010.md` v1.0, 2026-11-01T04:52:00Z); splits frozen (`run_manifest.json#split_boundaries_fclr010`, frozen_before_outcomes=true, frozen_at 2026-11-01T05:39:07Z). Test QLIKE→Brier (occurrence): C2 vs B1 mean diff -0.003077, 95% CI approx [-0.004892, -0.001263] (excludes zero), relative reduction 2.21% (>=2% floor PASS), paired OOS instruments 199 (PASS), test window 2026-05-28..2026-10-31 = 157 days = 5 non-overlapping 30-day blocks (PASS). Artifact: `research_state/evaluation_summary_FCLR010.md` (Git SHA f79c9767). Test window SEALED — no outcome re-inspection, no threshold tuning.

## Track status (current, authoritative)
| Track | Hypothesis | Status | Basis |
|-------|------------|--------|-------|
| C | FCLR-H001 funding-conditioned volatility | NOT_SUPPORTED — CONFIRMATORY CLOSED | FCLR-003 C2 vs B1 +0.015205 QLIKE, CI [-0.020240, 0.056734] crosses zero, -3.78%; all Binance confirmatory panels FCLR-001..009 exhausted; no unsealed >=5-symbol >=3-block window on admissible data (RESEARCH_PROMPT §16). Risk overlay INELIGIBLE. No reopen without new admissible data + pre-registration. |
| A | FCLR-H004 observed liquidations | REOPENED — FCLR-010 GATE PASSED | ironflow Hyperliquid census admissible; FCLR-010 executed, gate PASSED (see above). Overlay now ELIGIBLE only via pre-registered overlay protocol. |
| B | FCLR-H003 modeled boundary breaches | CLOSED_NEGATIVE | Codepath separation irrefutable (grep evidence); no incremental skill after Holm (FCLR-H003-EXT-001). |
| H002 | funding-extreme correction time | EXPLORATORY/PARTIAL (88/84/4) — PERMANENT BOTTLENECK | SSRN HTTP 403 blocks full methodology; cannot reconstruct event definition/censoring/regime split from admissible sources. No promotion, no speculative pre-registration. Revisit only if SSRN becomes accessible, with pre-registration BEFORE outcome inspection. |

## NEXT SESSION — INITIAL TASK (timestamped 2026-11-01T20:21:01Z)
Run in order; do not skip to later items before earlier acceptance is recorded.

1. **Re-verify baseline:** `python -m unittest discover -s tests -v` → 27/27 PASS at HEAD aad0450b; record result here.
2. **Independent recomputation audit of FCLR-010 headline** (heavy verification, from cached inputs + SHA-256 hashes only — no new downloads, no outcome re-inspection): reproduce B0/B1/C1/C2 Brier, paired C2 vs B1 diff -0.003077, CI approx [-0.004892, -0.001263], relative reduction 2.21%, n=199, 5 blocks, 7-day embargoes → `research_state/independent_recompute_audit_FCLR010.md`. Must match `evaluation_summary_FCLR010.md` within declared tolerance.
3. **FCLR-010 leakage / label-history audit:** protocol note states features are "causal proxies from label history where needed" — audit every predictor for future-label leakage; document per-feature provenance; fix/remove any leaking feature before any promotion claim. Zero unresolved leaking features is a hard acceptance gate.
4. **Calibration + subgroup diagnostics** (promotion requirement, research_protocol.md §7): per-symbol and per-month Brier/log-loss; confirm skill is not dominated by one coin/venue/time block; acceptable calibration for probability forecast → record in `research_state/fclr010_diagnostics.md`.
5. **Track A risk-overlay eligibility decision:** forecast gate MET → overlay now eligible. Either (a) draft liquidation-risk overlay / position-sizing specification and pre-register it BEFORE any overlay outcome inspection, or (b) formally close Track A with overlay rationale documented. No overlay building or tuning without pre-registration.
6. **Seal campaign:** update `experiment_frontier.json` (FCLR-010 COMPLETE/gate PASSED, Track A REOPENED→EXECUTED), `research_state/cross_track_decision_log.md` (Track A status), and this file. Keep this handoff the single source of truth; tree clean except `__pycache__/`.

## Bottlenecks removed (do not recreate)
- Track A structural block: removed (admissible ironflow source passes full rubric). Do not re-run the exhausted next_data_discovery_plan source families unless a NEW source family appears.
- FCLR-010: execution complete, gate passed, window sealed. Do not re-fit, re-tune, or re-inspect outcomes.
- H002: SSRN 403 accepted as permanent block; stop scheduling H002 confirmatory work.

## Do-not rules (cross-cutting)
- No merging Hyperliquid labels with Binance panels (cross-track firewall).
- No outcome/QLIKE/Brier inspection before split freeze; no sealed-window reuse.
- Do not relax rubric, >=2% floor, CI-excludes-zero, >=5 instruments, or >=3-block minimums; no threshold shopping; no relabeling exploratory as confirmatory.
- No risk overlay without pre-registration; no .github/workflows/* changes; commit nothing merely for activity.
- FCLR-003 recompute audit is archive verification only — it does NOT reopen Track C.

## Acceptance (campaign complete only when all hold)
- Tests 27/27 PASS, HEAD recorded.
- `independent_recompute_audit_FCLR010.md` written and consistent with `evaluation_summary_FCLR010.md`.
- Leakage audit documented; zero unresolved leaking features.
- `fclr010_diagnostics.md` written; no single-coin/venue/block dominance.
- Track A overlay decision documented (pre-registered spec or formal close).
- `experiment_frontier.json`, `cross_track_decision_log.md`, this handoff updated; single source of truth maintained.

## Verification
- Tests: 27/27 PASS (just re-verified)
- HEAD: a0135068 (main)
- Priority enforced by repo name; status-only work forbidden.
