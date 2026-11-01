# AGENT_HANDOFF.md (DURABLE — FCLR-TERMINAL / HANDOFF-009)
**TIMESTAMP (UTC):** 2026-11-01T01:41:24Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ 6c58534e (working tree: __pycache__ only)
**HANDOFF ID:** FCLR-HANDOFF-009-20261101T014124Z
**STATUS:** TERMINAL — all confirmatory cells exhausted; no unsealed powered confirmatory panel remains untested

## 1) WHAT CHANGED & WHY
The prior HANDOFF-008 declared CAMPAIGN FCLR-008 as pending heavy work (Steps 1-4). That work is now DONE and superseded. FCLR-008 executed 2026-11-01T00:50-00:54Z: pre-registered research_state/research_protocol_fclr008.md v1.0 BEFORE outcomes; coverage-only audit research_state/fclr008_coverage_audit.json; splits frozen_before_outcomes=true in run_manifest.json#split_boundaries_fclr008; ran `FCLR_EXPERIMENT=FCLR-008 python scripts/run_evaluation.py`; byte-identical reproducibility re-run verified; 27/27 tests PASS.

Result (research_state/evaluation_summary_FCLR-008.md, gate_assessment.md):
- Panel: 2026-01-01..2026-08-06, 5 symbols (BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT), 218 common days, 7 non-overlapping 30-day blocks, 5232 common hourly timestamps, n=10785 paired (C1/C2).
- Test QLIKE: B0=0.330127, B1=0.333314, C1=0.330164, C2=0.318996.
- Primary contrast C2 vs B1: mean diff -0.014318, 95% CI [-0.029938, 0.000524], relative reduction +4.30% (improvement).
- Gate: materiality floor PASS (4.30% ≥ 2%), ≥5 instruments PASS, ≥3 blocks PASS, but 95% CI CROSSES ZERO → FORECAST_GATE_NOT_MET. H001 INCONCLUSIVE (first unsealed panel with positive direction; FCLR-006/007 were significantly worse). Overlay INELIGIBLE.

All confirmatory panels exhausted: FCLR-001 (pilot/inconclusive), FCLR-002 (inconclusive, 2 blocks), FCLR-003 (complete negative, -3.78%), FCLR-006 (complete negative, -69.90%), FCLR-007 (complete negative, -3.42%), FCLR-008 (inconclusive, +4.30% but CI crosses zero).
Track A (observed liquidations): STRUCTURALLY BLOCKED — no admissible unauthenticated liquidation census with ≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness/license (research_state/liquidation_source_campaign.md, liquidation_sources_enumeration.md, binance_source_probe.md, track_a_deadend_map.md). Executed: COMPLETE_NO-GO.
Track B (modeled boundary breaches): COMPLETE_NEGATIVE (FCLR-H003-EXT-001, 16 cells, Holm).
H002 (correction-time replication): PARTIAL_REPLICATION — SSRN HTTP 403 blocks exact replication; RV-regime contrast computed (high-RV med 16.0h vs low-RV 8.0h, log-rank p=0.0792, not significant at 5%).
Tests: 27/27 PASS at HEAD 6c58534e (verified 2026-11-01T01:41:24Z).

## 2) CURRENT STATE SNAPSHOT (EVIDENCE)
- Tests: `python -m unittest discover -s tests -v` → 27/27 PASS (verified at HEAD 6c58534e)
- Data: local Binance archives + research_state/data_cache/ present; no network/auth needed for verified artifacts
- Research gates (terminal unless NEW data/experiment): H001 INCONCLUSIVE; H002 PARTIAL_REPLICATION; H003 NOT_SUPPORTED; H004 BLOCKED; overlay INELIGIBLE
- Key artifacts: research_state/final_inconclusive_report.md, evaluation_summary_FCLR-008.md, gate_assessment.md, hypothesis_registry.json, experiment_frontier.json, run_manifest.json, research_protocol_fclr008.md, fclr008_coverage_audit.json, leakage_audit.md, negative_results_report.md

## 3) SINGLE HIGHEST-VALUE NEXT TASK
**TASK ID:** FCLR-TERMINAL-NEXT | **TYPE:** TERMINAL STATE / REOPEN GATE
**GOAL:** Do NOT fabricate heavy work. The confirmatory program has no remaining untested ≥3-block ≥5-symbol unsealed panel. The only legitimate path to reopen is NEW admissible unauthenticated data + a fresh pre-registered experiment ID BEFORE any outcome inspection (RESEARCH_PROMPT.md §16).

**Steps (in order):**
1. Confirm terminal state: `git log -1 --oneline && git status --short`; `python -m unittest discover -s tests -v` → 27/27 PASS; read research_state/gate_assessment.md (FCLR-008 section) and research_state/evaluation_summary_FCLR-008.md.
2. Accept the verdict: H001 INCONCLUSIVE, forecast gate NOT_MET, overlay INELIGIBLE, all confirmatory panels exhausted. Do NOT re-run FCLR-001/002/003/005/006/007/008. Do NOT threshold-shop. Do NOT relax the ≥2% floor or CI criterion. Do NOT relabel exploratory as confirmatory.
3. Reopen path (only if new data appears): find ONE NEW admissible unauthenticated source (≥5 symbols, ≥3 non-overlapping 30-day blocks, documented completeness/license, no signup/key/payment per RESEARCH_PROMPT §1) → pre-register a NEW experiment ID BEFORE outcome inspection → execute frozen protocol. Document in research_state/liquidation_source_campaign.md or a new protocol version. Track A reopen requires a NEW observed-liquidation source; Track C reopen requires NEW price/funding history.
4. If no new source: stop cleanly with this terminal handoff; record no heavy work remaining.

**ACCEPTANCE:**
- [ ] 27/27 tests pass; no sealed holdout reused/tuned/re-opened
- [ ] Terminal state honestly recorded (no false "heavy work remains" claims)
- [ ] Reopen path documented (NEW data + fresh pre-registered experiment ID)
- [ ] No placeholder/dashboards/orchestrators/doc-sprawl created

## 4) BOTTLENECK REMOVAL PLAN
- **"FCLR-008 pending" bottleneck:** REMOVED — FCLR-008 is COMPLETE; HANDOFF-008's pending-task framing is superseded by this terminal handoff.
- **Track A structural block:** remains BLOCKED and is NOT a prerequisite for Track C; Track C is complete/inconclusive. Only valid Track A reopen: NEW admissible unauthenticated liquidation data source (≥5 symbols, ≥3 blocks, documented completeness/license) + pre-registered new experiment ID before outcomes.
- **No doc-sprawl:** do not create empty status files, dashboards, orchestrators, or placeholder files. Every artifact must carry meaningful content.
- **No threshold shopping:** prohibited by RESEARCH_PROMPT.md §16/§18. Do not re-tune/re-open sealed holds.

## 5) NEXT FOCUS CAMPAIGN (FOR FUTURE SESSIONS)
**CAMPAIGN NAME:** `FCLR-TERMINAL` — "Confirmatory program complete; H001 INCONCLUSIVE on the decisive unsealed powered panel FCLR-008; forecast gate NOT_MET; overlay INELIGIBLE; reopen only via NEW admissible unauthenticated data + fresh pre-registered experiment ID."

**MANDATE:** Future agents must not claim untested heavy confirmatory work remains (none exists), must not re-run sealed experiments, must not threshold-shop or relax gates, and must not create doc-sprawl. If a NEW admissible data source satisfying RESEARCH_PROMPT §1 minimums (≥5 symbols, ≥3 non-overlapping 30-day blocks, unauthenticated, documented completeness/license) is discovered, pre-register a new experiment ID BEFORE inspecting outcomes and execute. Otherwise, this is the terminal handoff: stop cleanly.

## 6) EXACT COMMANDS TO START (COPY/PASTE)
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
git log -1 --oneline && git status --short
python -m unittest discover -s tests -v
cat research_state/gate_assessment.md
cat research_state/evaluation_summary_FCLR-008.md
cat research_state/experiment_frontier.json | head -40
```

## 7) SESSION CHECKLIST (END OF SESSION MUST SATISFY)
- [ ] 27/27 tests pass with exact outcomes logged
- [ ] No sealed holdout (FCLR-001/002/003/005/006/007/008) reused, tuned, or re-opened
- [ ] No exploratory result relabeled confirmatory; no threshold shopping
- [ ] Terminal state unambiguous; reopen path = NEW admissible data + fresh pre-registered experiment ID
- [ ] No placeholder files committed without content

## 8) PER-SESSION DEFINITION OF DONE (RESEARCH_PROMPT.md §19)
- **Evidence:** H001 INCONCLUSIVE on FCLR-008 (decisive unsealed powered panel, 2026-01-01..2026-08-06, 5 symbols, 218 days, 7 blocks, n=10785; C2 vs B1 +4.30% rel QLIKE, CI crosses zero). All prior confirmatory panels sealed negative/inconclusive.
- **Strongest alternative:** FCLR-002 apparent edge (-9.28% rel QLIKE, CI excludes zero) flips on independent FCLR-003 (-3.78%) and FCLR-006/007 (worse); estimate does not generalize.
- **Dominant uncertainty:** Whether funding + price features add OOS QLIKE skill — resolved as INCONCLUSIVE on the widest unsealed powered panel; no further unsealed powered cell exists without NEW data.
- **Falsifying test:** none remaining without NEW admissible data + fresh pre-registered experiment ID.
- **Highest expected info gain per free compute:** none for confirmatory Track C; Track A source discovery already NO-GO.
- **Demonstrating progress:** this terminal handoff; 27/27 PASS; FCLR-008 artifacts complete and byte-identical reproducible.

## SESSION LOG
**2026-11-01T01:41:24Z - HANDOFF REWRITTEN (FCLR-TERMINAL / HANDOFF-009)**
- Superseded HANDOFF-008's "FCLR-008 pending heavy work" framing; FCLR-008 COMPLETE 2026-11-01T00:50-00:54Z, gate NOT_MET, H001 INCONCLUSIVE
- All confirmatory panels exhausted (FCLR-001/002/003/006/007/008); Track A BLOCKED (structural, executed NO-GO); Track B COMPLETE_NEGATIVE; H002 PARTIAL (SSRN 403); overlay INELIGIBLE
- 27/27 tests PASS at HEAD 6c58534e; byte-identical FCLR-008 reproducibility verified
- Clear initial task: accept terminal state; reopen only via NEW admissible unauthenticated data + fresh pre-registered experiment ID before outcomes; otherwise stop cleanly
