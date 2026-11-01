# AGENT_HANDOFF.md (DURABLE - FCLR-008 CONFIRMATORY CAMPAIGN)
**TIMESTAMP (UTC):** 2026-11-01T00:45:47Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ 3ec7a8a5 (working tree: __pycache__ only)
**HANDOFF ID:** FCLR-HANDOFF-008-20261101T004547Z
**PRIORITY:** CAMPAIGN_FCLR_008 — powered confirmatory volatility forecast on unsealed 2026 Apr-Jul panel; remove closed-out bottleneck; heavy research work resumes.

## 1) WHAT CHANGED & WHY
The prior AGENT_HANDOFF.md declared the program CLOSED OUT (VERIFY_CLOSURE_ONLY, no heavy work). That verdict is superseded. RESEARCH_PROMPT.md §16 data-exhaustion claim was RETRACTED 2026-10-30T12:34:23Z: research_state/data_cache/ verified to hold unsealed 2026 Apr-Jul markPriceKlines/indexPriceKlines/fundingRate for all 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT) — ~128 common days = ~3072 common UTC hourly timestamps = 4 non-overlapping 30-day blocks (≥3 claim-worthy minimum met). This panel has NOT been confirmatory-tested; FCLR-006 ran a different underpowered window (2026-05-23..2026-08-06, 2 blocks, C2 vs B1 significantly WORSE), FCLR-007 ran an 11-day window (0 blocks). The genuine unsealed powered confirmatory path is 2026-04-01..2026-07-31. Bottleneck removed: "no unsealed confirmatory data remains" is false. No downloads or credentials required; all inputs cached and hashed.

Prior confirmatory record (preserved, sealed, NOT re-opened):
- FCLR-H001 NOT_SUPPORTED: FCLR-003 powered (2024-10-02..12-31, 3 blocks, 5 instr, n=10796), C2 vs B1 = -3.78% rel QLIKE, CI crosses zero → gate NOT_MET; overlay INELIGIBLE. FCLR-006/FCLR-007 worse on unsealed 2026 panels but underpowered (<3 blocks).
- FCLR-H002 PARTIAL_REPLICATION: direction matches paper (high-RV med 16.0h vs low-RV 8.0h) but log-rank p=0.0792, not significant at 5%; SSRN HTTP 403 blocks exact replication.
- FCLR-H003 NOT_SUPPORTED / COMPLETE_NEGATIVE: Track B boundary breach, no incremental skill after Holm (16 cells).
- FCLR-H004 BLOCKED (2024): no admissible unauthenticated liquidation census; FCLR-005 2026 pilot EXPLORATORY_ONLY, no incremental skill.
Tests: 27/27 PASS at HEAD 3ec7a8a5.

## 2) CURRENT STATE SNAPSHOT (EVIDENCE)
- **Tests:** `python -m unittest discover -s tests -v` → 27/27 PASS (verified at HEAD 3ec7a8a5)
- **Data:** local Binance archives + research_state/data_cache/ present; no network/auth needed for verified artifacts
- **Unsealed powered panel (candidate for FCLR-008):** 2026-04-01..2026-07-31, 5 symbols, 128 common days (~4 blocks), audit at research_state/fclr006_coverage_audit.md (window label FCLR-006 but covers Apr-Jul; all 5 symbols markPriceKlines/indexPriceKlines/funding present, hashes recorded)
- **Research gates (terminal unless new data/experiment):** H001 NOT_SUPPORTED; H002 PARTIAL_REPLICATION; H003 NOT_SUPPORTED; H004 BLOCKED; overlay INELIGIBLE
- **Key artifacts:** research_state/final_confirmatory_verdict.md, evaluation_summary_FCLR003.md, hypothesis_registry.json, experiment_frontier.json, run_manifest.json, research_protocol.md, leakage_audit.md, negative_results_report.md, fclr006_coverage_audit.md

## 3) SINGLE HIGHEST-VALUE NEXT TASK
**TASK ID:** FCLR-008-CONFIRMATORY | **TYPE:** CONFIRMATORY RESEARCH (HEAVY)
**GOAL:** Execute a properly powered confirmatory FCLR-H001 test on the unsealed 2026 Apr-Jul panel (all 5 symbols, ≥3 blocks ≥ claim-worthy minimum), pre-registered BEFORE outcome inspection, to determine whether funding + price-dislocation/smoothing features add out-of-sample QLIKE skill over the RV-only HAR baseline on genuinely unsealed data.

**Steps (in order):**
1. **Coverage-only audit (NO outcome/QLIKE inspection):** confirm ≥5 instruments and ≥90 common days on 2026-04-01..2026-07-31 using research_state/fclr006_coverage_audit.md (already verified: 128 days, 4 blocks). Record common timestamps/hash; do not compute model results.
2. **Pre-register protocol:** create research_state/research_protocol_fclr008.md v1.0 BEFORE any outcome inspection. Freeze: B0 persistence, B1 RV-HAR (log RV1h/24h/168h → log next-24h RV), C1 funding-augmented, C2 combined; primary contrast C2 vs B1 on 24h out-of-sample QLIKE; ≥2% relative QLIKE materiality floor; Holm multiplicity; block bootstrap ≥2000 deterministic-seed replicates; ≥5 instruments; ≥3 non-overlapping 30-day blocks; 7-day purge/embargo at split boundaries; chronological train/val/test by unique UTC timestamps; zero-variance column handling; training-only smearing correction; no regularization/model search/tuning. Freeze split boundaries and hash eligible panel before outcomes.
3. **Run frozen pipeline:** `FCLR_EXPERIMENT=FCLR-008 python scripts/run_evaluation.py` on frozen splits → research_state/evaluation_summary_FCLR008.md + gate assessment + research_state/run_manifest.json update (split_boundaries_fclr008, frozen_before_outcomes: true).
4. **Update registry & verify:** update research_state/hypothesis_registry.json (FCLR-H001 status on FCLR-008), research_state/experiment_frontier.json; `python -m unittest discover -s tests -v` → 27/27 PASS; byte-identical reproducibility re-run of FCLR-008 verified.

**ACCEPTANCE:**
- [ ] ≥5 instruments in paired out-of-sample panel (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT)
- [ ] ≥3 non-overlapping 30-day blocks in test window (Apr-Jul = 4 blocks → PASS)
- [ ] Forecast gate: C2 vs B1 ≥2% relative QLIKE reduction AND 95% CI excludes zero on improving side → FORECAST_GATE_PASSED; otherwise retain NOT_SUPPORTED and do not threshold-shop
- [ ] 27/27 tests pass; byte-identical reproducibility re-run
- [ ] Splits frozen_before_outcomes: true; no sealed holdout re-opened/tuned

## 4) BOTTLENECK REMOVAL PLAN
- **Closed-out bottleneck:** superseded. Data exhaustion claim retracted; unsealed powered panel (2026 Apr-Jul, 4 blocks) confirmed. CAMPAIGN FCLR-008 is the active focus; no more "verify closure only."
- **No threshold shopping:** prohibited by RESEARCH_PROMPT.md §16/§18. Do not re-tune/re-open sealed FCLR-001/002/003/005/006/007 holds. FCLR-008 is a NEW pre-registered experiment on a NEW unsealed window.
- **No doc-sprawl:** do not create empty status files, dashboards, orchestrators, or placeholder files. Every artifact must carry meaningful content (protocol, coverage audit, evaluation summary, gate assessment).
- **Track A (liquidations) remains structurally BLOCKED** and is NOT a prerequisite for Track C; continue Track C confirmatory work independently per RESEARCH_PROMPT.md §16.
- **Only valid Track A reopen:** NEW admissible unauthenticated liquidation data source (≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness/license) → pre-register new experiment ID before outcome inspection.

## 5) NEXT FOCUS CAMPAIGN (FOR FUTURE SESSIONS)
**CAMPAIGN NAME:** `FCLR-008-CONFIRMATORY` — "Powered confirmatory volatility forecast on unsealed 2026 Apr-Jul panel; pre-register before outcomes; ≥2% QLIKE floor; ≥3 blocks."

**MANDATE:** Future agents must not close out, mark verify-only, or declare no heavy work while an unsealed ≥3-block ≥5-symbol confirmatory panel exists untested. Execute Steps 1-4 above in order. If FCLR-008 gate passes (C2 vs B1 ≥2% rel QLIKE, CI excludes zero), risk-overlay becomes eligible only after a separate forward/holdout overlay evaluation (RESEARCH_PROMPT.md §9); do not use the FCLR-008 holdout to design an overlay. If the gate does not pass, retain NOT_SUPPORTED with exact shortfall documented; the only reopen path is NEW admissible data + fresh pre-registered experiment ID.

## 6) EXACT COMMANDS TO START (COPY/PASTE)
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
git log -1 --oneline && git status --short
python -m unittest discover -s tests -v
ls research_state/fclr006_coverage_audit.md research_state/final_confirmatory_verdict.md research_state/hypothesis_registry.json research_state/experiment_frontier.json
cat research_state/fclr006_coverage_audit.md
```
Then create research_state/research_protocol_fclr008.md v1.0 (pre-registration, BEFORE outcomes), run `FCLR_EXPERIMENT=FCLR-008 python scripts/run_evaluation.py`, verify 27/27 tests, update registry/frontier/manifest.

## 7) SESSION CHECKLIST (END OF SESSION MUST SATISFY)
- [ ] 27/27 tests pass with exact outcomes logged
- [ ] No sealed holdout (FCLR-001/002/003/005/006/007) reused, tuned, or re-opened
- [ ] No exploratory result relabeled confirmatory; no threshold shopping
- [ ] Next action unambiguous and executable without user input (FCLR-008 Steps 1-4)
- [ ] No placeholder files committed without content

## 8) PER-SESSION DEFINITION OF DONE (RESEARCH_PROMPT.md §19)
- **Evidence:** H001 NOT_SUPPORTED on sealed FCLR-003 powered panel and worse on undersealed FCLR-006/007; FCLR-008 pending on unsealed Apr-Jul panel (4 blocks, 5 symbols) — the decisive untested confirmatory cell.
- **Strongest alternative:** Apparent FCLR-002 edge (-9.28% rel QLIKE, CI excludes zero) flips on independent FCLR-003 (cross-window sign flip, -3.78%) and FCLR-006/007 (worse); estimate does not generalize.
- **Dominant uncertainty:** Whether funding + price features add OOS QLIKE skill on a properly powered UNSEALed ≥3-block panel (FCLR-008 resolves this; sealed panels already negative).
- **Falsifying test:** FCLR-008 C2 vs B1 on unsealed Apr-Jul 2026 panel; gate fails if relative QLIKE < +2% reduction or 95% CI crosses zero / favors worse.
- **Highest expected info gain per free compute:** FCLR-008 confirmatory run (cached data, no downloads, ~4 blocks, 5 instruments).
- **Demonstrating progress:** research_state/research_protocol_fclr008.md (pre-registered) + research_state/evaluation_summary_FCLR008.md + gate assessment + 27/27 PASS.

## SESSION LOG
**2026-11-01T00:45:47Z - HANDOFF REWRITTEN (CAMPAIGN FCLR-008, BOTTLENECK REMOVED)**
- Superseded VERIFY_CLOSURE_ONLY closeout; data-exhaustion claim retracted (unsealed 2026 Apr-Jul panel: 5 symbols, 128 common days, 4 blocks ≥ 3 minimum, cached, hashed, never confirmatory-tested)
- FCLR-006 ran different underpowered window (May-Aug, 2 blocks, C2 vs B1 significantly worse); FCLR-007 ran 11-day window (0 blocks) — neither is the powered Apr-Jul cell
- Clear initial task: FCLR-008 Steps 1-4 (coverage audit → pre-register → run → verify); no sealed holdout reuse; no doc-sprawl
- Prior sealed negative record preserved (H001 NOT_SUPPORTED, H002 PARTIAL, H003 NOT_SUPPORTED, H004 BLOCKED, overlay INELIGIBLE); 27/27 tests PASS
