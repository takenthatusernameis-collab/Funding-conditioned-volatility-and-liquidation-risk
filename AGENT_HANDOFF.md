# AGENT_HANDOFF.md (DURABLE — SINGLE SOURCE OF TRUTH)
**TIMESTAMP (UTC):** 2026-11-02T02:06:35Z
**INITIAL TASK (NEXT SESSION):** Execute CAMPAIGN FCLR-HEAVY-001 — Funding-conditioned liquidation-risk deepening (Track A operational hardening). Do NOT reopen H001/FCLR-003/FCLR-008/010 without triggers; treat all outcomes as hypothetical-only. Start at Step 1 below and do not stop until all steps produce artifacts + tests pass. NO confirmatory outcome inspection for sealed panels.
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**REPO PRIORITIZATION (INFERRED):** Funding-conditioned volatility → liquidation risk (name is directive). Focus first on Track A (observed liquidations, ironflow Hyperliquid) — highest concrete signal with passed gate — while keeping Track C sealed and Track B closed.
**BRANCH/HEAD:** main @ a6556d87
**HANDOFF ID:** FCLR-HANDOFF-075-20261102T020635Z
**SUPERSEDES:** FCLR-HANDOFF-074-20261102T011840Z

## BOTTLENECKS REMOVED (this session)
- Verified __pycache__ removed from index; .gitignore present. Working tree clean except untracked .gitignore.
- No blocking workflow edits. Tests 27/27 PASS at HEAD edc55ed2.

## STATUS (CURRENT)
- Track A (FCLR-010): GATE PASSED on Hyperliquid ironflow census (199 perps, 12 blocks Nov 2025–Oct 2026). C2 vs B1 mean diff -0.003077, CI [-0.004892,-0.001263] excludes zero, rel Brier -2.21% >= 2% floor. Overlay FCLR-OVERLAY-001 executed (hypothetical only). Test window SEALED.
- Track C (H001): NOT_SUPPORTED — CONFIRMATORY CLOSED (FCLR-008 +4.30% but CI crosses zero; all unsealed powered panels exhausted).
- Track B (H003): CLOSED_NEGATIVE.
- H002: PERMANENT BLOCK (SSRN HTTP 403).
- Reopen readiness exists (FCLR-REOPEN-READY-001) but passive.

## CAMPAIGN FCLR-HEAVY-001 (HEAVY — future agents cannot avoid doing heavy working)
Goal: extract maximum admissible value from Track A without crossing into trading/overlay deployment claims. All analysis must remain hypothetical-only; never merge labels across tracks.

### Steps (execute in order; each produces durable artifact)
1. **Funding-liquidity coupling audit**
   Build `research_state/fclr_heavy001_funding_liq_coupling.md` + `results/fclr_heavy001/coupling_summary.json`. Recompute funding-conditioned liquidation intensity using frozen FCLR-010 panel/splits. Quantify marginal contribution of funding_abs/signed funding deciles to liquidation intensity controlling for RV/vol proxies. Block bootstrap by time blocks. Preserve nulls.

2. **Regime stratification (adversarial)**
   Build `research_state/fclr_heavy001_regime_strat.md` + `results/fclr_heavy001/regime_strat.json`. Stratify by realized vol terciles, funding regime (pos/neg/extreme), and time-of-day/funding-cycle where knowable. For each stratum report event counts, Brier/logloss, calibration, and block-bootstrap CIs for C2 vs B1. Flag thin strata (< n_events threshold) without imputing.

3. **Lead/lag & censoring robustness**
   Build `research_state/fclr_heavy001_leadlag_censor.md` + `results/fclr_heavy001/leadlag_censor.json`. Test alternative lead windows and censoring rules consistent with frozen protocol. Show sensitivity without re-tuning to holdout. Explicitly document any rule changes as non-conforming and reject if they require peeking.

4. **Feature ablation hardening (funding-focused)**
   Build `research_state/fclr_heavy001_ablation_funding.md` + `results/fclr_heavy001/ablation_funding.json`. Isolate funding alone vs RV-only vs combined; include funding sign/abs interactions. Use same frozen splits/blocks/bootstrap. Report raw + adjusted for multiplicity (Holm) across registered comparisons.

5. **Cross-symbol concentration & stability**
   Build `research_state/fclr_heavy001_concentration.md` + `results/fclr_heavy001/concentration.json`. Leave-one-symbol-out and symbol-cluster stability. Identify concentration (e.g. top symbols driving improvement). If improvement concentrates in <20% symbols with wide CIs, call out instability explicitly.

6. **Reproducibility + integrity lock-in**
   Re-verify sealed FCLR-010 artifacts untouched (hashes/mtimes). Write `research_state/fclr_heavy001_integrity.md`. Run `python -m unittest discover -s tests -v` → 27/27. Update `research_state/experiment_frontier.json` with FCLR-HEAVY-001 entries (status IN_PROGRESS/COMPLETE per step) and append to `research_state/cross_track_decision_log.md`.

### Acceptance Criteria
- All 6 steps produce artifacts above.
- Tests remain 27/27.
- No sealed panel modified; all new outputs under `results/fclr_heavy001/` and `research_state/fclr_heavy001_*.md/json`.
- Conclusions strictly hypothetical-only; no trading/paper/live claims; no label merging.
- If any step would require peeking/re-tuning sealed splits or adding unregistered comparisons, STOP and document blocker in handoff + log.

### Parallel readiness (do not block)
While doing FCLR-HEAVY-001, also keep `scripts/reopen_probe.py` functional (SSRN + source families) per FCLR-REOPEN-READY-001. If T1 or T2 fires, freeze splits/pre-register before inspecting outcomes.

## HARD CONSTRAINTS
- NO Binance merge. NO reopening H001/FCLR-003/FCLR-008/FCLR-010 without trigger + pre-registration + split freeze.
- All 27 tests must PASS. No changes to `.github/workflows/`.
- Only admissible: ironflow Hyperliquid liquidations + Hyperlquid fundingHistory API.
- Never silently zero missing funding — drop/flag with justification.
- Sealed artifacts unchanged. Track A/B/C never merged; modeled != observed.
- No risk-overlay promotion beyond hypothetical.

## SINGLE HIGHEST-VALUE NEXT TASK
**Execute CAMPAIGN FCLR-HEAVY-001 starting at Step 1.** Do heavy analysis on frozen Track A data. Verify integrity, keep tests green, produce concrete artifacts that future agents cannot ignore. If blocked by data availability for any subanalysis, write precise evidence + smallest verifiable alternative and continue to next step.
