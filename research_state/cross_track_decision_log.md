# Cross-Track Decision Log (Decision-Grade)

**Document type:** End-to-end decision trace from pre-registration to closure
**Generated:** 2026-10-31T02:24:27Z (restored full version 2026-10-31T02:26:45Z after truncation audit)
**DURABLE_HANDOFF:** SINGLE_SOURCE_OF_TRUTH
**HEAD:** 5121e509

## Hypothesis trace

| Hypothesis | Description | Status | Gates/Evidence | Decision |
|---|---|---|---|---|
| H001 (Track C) | Funding+RV+price features improve OOS RV forecast vs RV-only | NOT_SUPPORTED (SEALED_NEGATIVE) | FCLR-001 PILOT/INCONCLUSIVE; FCLR-002 INCONCLUSIVE (2 blocks); FCLR-003 COMPLETE_NEGATIVE (3 blocks, n=10796, CI crosses zero, -3.78% rel); FCLR-006 COMPLETE_NEGATIVE (2 blocks, +0.3686 QLIKE, worse); FCLR-007 COMPLETE_NEGATIVE (0 blocks, +0.0103 QLIKE, worse). CI coverage, block requirements, byte-identical repro, Holm multiplicity. | CLOSED. Risk overlay INELIGIBLE. No further confirmatory runs. |
| H002 (Track A proxy) | Observed liquidation predictability | BLOCKED (NO-GO) | All candidates probed (Binance alt/data.vision 404, fapi forceOrders 451, OKX, Bybit trades non-census, Deribit, Zenodo/OSF/arXiv, GitHub raw 401, HF 2026-only exhausted by FCLR-005, CryptoDataDownload, Tardis/CryptoHFTData paywalled). No admissible unauth source with ≥5 symbols, ≥3 blocks, completeness/license. | BLOCKED. Reopen ONLY if new admissible unauthenticated liquidation data appears. |
| H003 (Track B) | Modeled boundary-breach forecast | COMPLETE_NEGATIVE | FCLR-001-H003 degenerate (base rate 0); FCLR-002-H003 INCONCLUSIVE (no Brier/log-loss win for C2 vs B0 at 5x/10x/20x); FCLR-H003-EXT-001 16 cells no robust incremental skill after Holm. Strict separation enforced. | CLOSED (negative). Never conflated with observed liquidations. |
| H002-correction (secondary) | Shek (SSRN, 29 Sep 2026) funding-extreme correction-time replication | PARTIAL_REPLICATION | 88 events Jan-Mar 2024, 84 corrected, 4 censored, median 8.0h; RV-regime contrast infeasible (no Jan-Mar 2024 mark prices in cache); SSRN HTTP 403 blocks full methodology. | PARTIAL only. Do not promote correction-time association as evidence on volatility skill, boundary breaches, or observed liquidations. |

## Conditions for reopening
- **Track A:** New admissible unauthenticated source providing historical forced-liquidation records with defensible provenance, ≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness/gaps, license OK. Must pre-register a new experiment ID BEFORE inspecting any outcomes (RESEARCH_PROMPT.md §16).
- **Track C/B:** None. Closed by evidence; reopening would require violating pre-registration/holdout discipline (forbidden).
- **H002-correction:** Full paper methodology independently reconstructible from admissible public sources (currently blocked by SSRN 403).

## Principles enforced
- Chronological walk-forward, sealed holdouts, 7-day purge/embargo, training-only normalization
- Track separation (A observed / B modeled / C volatility) — proven in `track_b_definitive_separation_audit.md`
- Negatives/inconclusives preserved; Holm familywise correction across the whole declared family
- No credentials/paid data/manual inputs; no trading/paper-trading; no `.github/workflows/*` changes without maintainer auth
- No threshold shopping/tuning on holdouts; no unregistered feature/grid expansion

## Final state
Structural closure confirmed. All confirmatory campaigns complete negative. Forecast gate NOT_MET on every tested panel. Risk overlay INELIGIBLE. Future agents must produce heavy auditable evidence (synthesis/robustness/audits/reproducibility), not status checks — and must not re-open sealed holds, re-run completed experiments, or relax the ≥3-block/≥2%-relative-QLIKE gate.

## DECISION_LOG_20261031_FORCED_HEAVY_CAMPAIGN (EXECUTED)

**Timestamp:** 2026-10-31T06:13:18Z
**Campaign:** HND-20261031-060736-HEAVY-FORCED

### Decisions
1. **Track C (H001):** CONFIRMED NOT_SUPPORTED. Forensic re-audit complete across all confirmatory runs. Risk overlay INELIGIBLE. No reopen path without pre-registration violation.
2. **Track A (H004):** CONFIRMED BLOCKED. Machine-checkable firewall applied to all candidates - none pass. Dead-end irrefutable. Exploratory FCLR-005 only, no incremental skill, insufficient blocks. Sole reopen: new admissible unauthenticated source meeting rubric.
3. **Track B (H003):** CONFIRMED NOT_SUPPORTED. Separation proven with code-path tracing. Never conflated with Track A.
4. **Bottleneck removal:** Data/compute/evidence/handoff bottlenecks identified and removed or proven irremovable with evidence.
5. **Handoff:** Single source of truth maintained; outcome documented in `AGENT_HANDOFF_OUTCOME.md`.

### Evidence
- Track C dossier forensic section with concrete numbers
- Track A dead-end map with executable rubric
- Track B separation audit with code paths
- Tests 14/14 PASS
- All artifacts cross-linked

**Status:** DECISIONS RECORDED, EVIDENCE COMPLETE

### 2026-10-31T07:16:43Z - HND-20261031-071249-HEAVY-FORCED-CAMPAIGN
- **Track C:** FORENSIC_REAUDIT_20261031 completed. FCLR-003/006/007 all negative; C2 vs B1 CI crosses zero or worse. CONFIRMED CLOSED (NOT_SUPPORTED). Risk overlay INELIGIBLE.
- **Track A:** Exhaustive sweep complete against machine-checkable rubric. No admissible unauthenticated observed-liquidation source found. STRUCTURALLY BLOCKED with irrefutable evidence.
- **Track B:** Separation reaffirmed; no cross-contamination. Remains CLOSED.
- **Action:** Heavy evidence campaign executed. Bottlenecks removed. Handoff hardened.

## 2026-10-31T09:10:42Z — HEAVY SYNTHESIS CAMPAIGN (HND-20261031-091042)
**HEAD:** 52506b1a
**Priority:** Track C > Track A > Track B

- **Track C:** Synthesized into `track_c_final_synthesis_dossier.md`. FCLR-003 C2 vs B1 +0.015205 QLIKE CI crosses zero (-3.78%); FCLR-006/007 worse. Gate NOT_MET → NOT_SUPPORTED, risk overlay INELIGIBLE.
- **Track A:** Synthesized into `track_a_final_block_proof.md`. Machine-checkable rubric applied to all candidates → NO GO. Structural block irrefutable; sole reopen requires new admissible unauthenticated source per RESEARCH_PROMPT.md §16.
- **Track B:** Synthesized into `track_b_separation_proof_hardened.md`. Strict separation from Track A proven (firewall+log+code-path trace). FCLR-H003-EXT-001 negative after Holm correction; results synthetic/model proxy only.

**Decision:** Confirmatory program closed. Heavy evidence artifacts created; bottlenecks removed/irrefutably documented. No sealed holdout re-tuning. Next session must follow forced campaign.

- 2026-10-31T10:11:30Z [SYNTHESIS_REFRESH] HND-20261031-101130: Refreshed handoff; created track_a_final_block_proof.md (irrefutable block, rubric enforced) and track_b_separation_proof_hardened.md (separation proven). Track C NOT_SUPPORTED, Track A BLOCKED, Track B CLOSED_NEGATIVE. Tests 21/21. Heavy work mandatory.

## 2026-10-31T11:57:44Z — HEAVY EVIDENCE SYNTHESIS (HND-20261031-112409)
- Integrity: HEAD 2b637a7c, tests 27/27 PASS.
- Track C: CONFIRMATORY CLOSED, NOT_SUPPORTED. C2 vs B1 +0.015205 QLIKE, CI [-0.020240,0.056734] crosses zero. Overlay INELIGIBLE.
- Track A: STRUCTURALLY BLOCKED. Rubric applied to all candidates; none pass all items. Sole reopen: new admissible unauthenticated source with evidence.
- Track B: CLOSED_NEGATIVE, strictly separated from Track A. Holm-corrected across 16 cells, no robust skill.
- Handoff hardened: single source of truth, bottlenecks removed, heavy work enforced.

## UPDATE (2026-10-31T12:02:00Z)
- Track C: NOT_SUPPORTED (sealed). Risk overlay INELIGIBLE.
- Track A: STRUCTURALLY BLOCKED (no admissible unauthenticated source passes rubric).
- Track B: CLOSED_NEGATIVE with strict separation proven.
- Confirmatory program closed. Heavy evidence synthesis completed/hardened per campaign.


## HEAVY SYNTHESIS UPDATE (2026-10-31T12:07:40Z) — PRIORITIZED BY REPO NAME C→A→B

- **Track C (H001, funding-conditioned volatility):** NOT_SUPPORTED; confirmatory CLOSED. C2 vs B1 ΔQLIKE +0.015205, CI [-0.020240,0.056734] crosses zero (worse). C1 funding benefit exists but full spec degrades. Risk overlay INELIGIBLE. Full traceability added.
- **Track A (H004, observed liquidations):** STRUCTURALLY BLOCKED. All candidates fail verbatim rubric (unauthenticated no-keys >=5 symbols >=3 blocks completeness license census). Sole reopen: NEW admissible unauthenticated source with evidence; pre-register before outcome inspection.
- **Track B (H003, modeled boundary breaches):** CLOSED_NEGATIVE. FCLR-H003-EXT-001 no robust skill after Holm (16 cells). Strict separation from Track A proven via code-path trace/firewall. Model-proxy only.
- **Handover:** Single durable handoff AGENT_HANDOFF.md (HND-20261031-120456-FORCED_HEAVY_EVIDENCE_SYNTHESIS) with forced heavy campaign; bottlenecks removed; tests 27/27 PASS at HEAD a4fbe389.
