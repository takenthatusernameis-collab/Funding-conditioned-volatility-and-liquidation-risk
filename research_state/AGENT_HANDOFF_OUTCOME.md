# AGENT HANDOFF OUTCOME — SINGLE DURABLE HANDOFF (source of truth)

Generated: 2026-11-02T00:07:51Z
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

## NEXT SESSION — INITIAL TASK (timestamped 2026-11-02T00:07:51Z)
**Priority by repo name (funding-conditioned volatility → liquidation risk):** Track C (CLOSED) → Track A (REOPENED, gate PASSED) → Track B (CLOSED) → H002 (PERMANENT BLOCK).

**Campaign directive:** NO status-only reporting. Every step below requires concrete artifacts with file:line/provenance, computed values, and explicit acceptance checks. Do heavy verification work first (recomputation + audits). Do not proceed to later steps until the acceptance gates for earlier steps are satisfied.

Run in strict order; record outcomes against acceptance gates as you go.

### Step 1: Baseline (must pass)
- [ ] `python -m unittest discover -s tests -v` → **27/27 PASS** at HEAD a0135068. Record exact output + HEAD in `research_state/AGENT_HANDOFF_OUTCOME.md` (update verification section).
- [ ] Working tree clean except `__pycache__/`. If dirty, explain and revert non-essential changes.

### Step 2: Independent recomputation audit of FCLR-010 (HEAVY VERIFICATION - required)
From cached inputs only (`research_state/data_cache/`, hashes in `research_state/data_source_registry.json`, manifests) with no new downloads, no outcome re-inspection:
- [ ] Reproduce B0/B1/C1/C2 Brier scores and paired C2 vs B1 difference.
- [ ] Reproduce 95% CI for paired difference (must be approx [-0.004892, -0.001263], excluding zero).
- [ ] Reproduce relative reduction (must be >= 2.21%), n=199 paired OOS instruments, 5 non-overlapping 30-day blocks, 7-day embargoes.
- [ ] Write full audit with per-block tables, hashes used, code paths exercised → `research_state/independent_recompute_audit_FCLR010.md`. Must match `evaluation_summary_FCLR010.md` within declared tolerance. **Gate:** values within tolerance or explain deviation with evidence; any mismatch blocks promotion.

### Step 3: FCLR-010 leakage / label-history audit (HARD GATE)
- [ ] Audit every predictor used in FCLR-010 for future-label leakage. Document per-feature provenance (source file + logic) and whether it uses only information available at prediction time given 7-day embargoes.
- [ ] Explicitly check "causal proxies from label history where needed" are admissible under embargoes and protocol.
- [ ] Fix/remove any leaking feature before any promotion claim.
- [ ] Record audit → `research_state/fclr010_leakage_audit.md`. **Gate:** ZERO unresolved leaking features. Block promotion if any unresolved.

### Step 4: Calibration + subgroup diagnostics (PROMOTION REQUIREMENT)
- [ ] Per-symbol Brier/log-loss for all 199 instruments (show min/max/mean, outliers).
- [ ] Per-month/block Brier/log-loss across the 5 blocks.
- [ ] Check dominance: no single coin/venue/time block accounts for >40% of total skill (or justify if different).
- [ ] Calibration assessment for probability forecast (reliability diagram data + summary).
- [ ] Write → `research_state/fclr010_diagnostics.md`. **Gate:** no single-coin/venue/block dominance; acceptable calibration. Block promotion if dominated or miscalibrated.

### Step 5: Track A risk-overlay decision (ELIGIBILITY NOW MET)
Forecast gate PASSED → liquidation-risk overlay eligible. You MUST do one of:
- [ ] **(a) PRE-REGISTER overlay spec BEFORE any overlay outcome inspection.** Draft `research_state/track_a_risk_overlay_spec.md` with: hypothesis, instruments (Hyperliquid only, firewall to Binance), features, split boundaries frozen before outcomes, test window proposal (must be >=5 symbols, >=3 blocks, with embargoes), metrics (e.g. PnL/turnover/capital efficiency with liquidation-adjusted metrics), null, acceptance criteria, pre-registration timestamp. Do NOT build/tune/run overlay outcomes until spec exists and is committed to state.
- [ ] **(b) FORMALLY CLOSE Track A with overlay rationale.** If no admissible pre-registrable overlay exists, write `research_state/track_a_closure_rationale.md` explaining why ineligible despite gate pass, with evidence.

**Gate:** Decision documented with evidence. No overlay outcomes computed without (a).

### Step 6: Seal campaign (CLEAN CLOSEOUT)
- [ ] Update `experiment_frontier.json` (FCLR-010: COMPLETE/gate PASSED; Track A: REOPENED→EXECUTED or CLOSED with rationale; record timestamps/HEAD).
- [ ] Update `research_state/cross_track_decision_log.md` with all decisions above (Track A status, FCLR-010 audits, gates).
- [ ] Update this file (`research_state/AGENT_HANDOFF_OUTCOME.md`) with verification results, artifact paths, gate outcomes, and HEAD.
- [ ] Ensure single source of truth maintained. Tree clean except `__pycache__/`. Do not commit merely for activity.

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
