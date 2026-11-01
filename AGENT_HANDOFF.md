# AGENT_HANDOFF.md (DURABLE - FCLR-HANDOFF-028)
**TIMESTAMP (UTC):** 2026-11-01T08:34:40Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ eb362d73 (working tree: clean except __pycache__)
**HANDOFF ID:** FCLR-HANDOFF-028-20261101T083440Z
**STATUS:** OPEN — FCLR-009 COMPLETE (gate NOT_MET); Track A REOPENED via NEW admissible source (ironflow Hyperliquid census); FCLR-010 PRE-REGISTERED, coverage audit DONE, splits FROZEN (frozen_before_outcomes=true), EXECUTION PENDING
**PRIORITIZED BY:** repo name = funding-conditioned volatility ∩ liquidation risk as ONE COUPLED PROBLEM (do not split them)

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T08:34:40Z
**PRIORITY P0 | TYPE: HEAVY COUPLED EXECUTION (FCLR-010 TRACK A CONFIRMATORY ON HYPERLIQUID) | NO STATUS-ONLY WORK**

**REPO NAME IS THE SPEC:** Treat funding-conditioned volatility AND liquidation risk as a single coupled question. Track C (volatility-only forecasting) is EXHAUSTED and CLOSED (all panels FCLR-001/002/003/006/007/008/009 failed to clear the gate). The ONLY viable open confirmatory track is Track A.

Track A is REOPENED: `ironflow_hyperliquid_liquidation_events` (HuggingFace, CC BY 4.0, unauthenticated) passed ALL rubric items (unauthenticated, no_keys, symbols>=5 [199 native perps], blocks>=3 [12 monthly blocks 2025-11..2026-10], completeness_doc, license_ok, census_or_defensible). Files hashed and cached at `research_state/data_cache/ironflow_events/` (12 parquet files, 8612 label hours, hashes in fclr010_coverage_audit.json).

FCLR-010 is PRE-REGISTERED (`research_state/research_protocol_fclr010.md`, v1.0, frozen 2026-11-01T04:52:00Z) BEFORE any outcome inspection. Splits are FROZEN in `run_manifest.json#split_boundaries_fclr010` with `frozen_before_outcomes=true` (frozen_at 2026-11-01T05:39:07Z; chronological 60/20/20, 7-day purge/embargo, train 2025-11-01..2026-03-06, val 2026-03-14..2026-05-20, test 2026-05-28..2026-10-31). **ABSOLUTE FIREWALL:** No model may be fitted to liquidation labels and no label-outcome relationship may be inspected — splits already frozen before outcomes, so execution is now authorized. Cross-track firewall: NO Binance data merged into Hyperliquid label/predictor panels.

### MANDATORY FIRST ACTION (30s)
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
git log -1 --oneline && git status --short
python -m unittest discover -s tests -v  # MUST remain 27/27 PASS
python3 -c "import json; d=json.load(open('research_state/run_manifest.json')); s=d['split_boundaries_fclr010']; print(s['status'], s['frozen_before_outcomes'], s['frozen_at'])"
python3 -c "import json; d=json.load(open('research_state/data_source_registry.json')); x=[x for x in d['sources'] if x['source_id']=='ironflow_hyperliquid_liquidation_events'][0]; print(x['status'], all(x['rubric'].values()))"
ls research_state/data_cache/ironflow_events/ | wc -l   # expect 12
```

## FOCUS CAMPAIGN: `FCLR-COUPLED-EXECUTE-FCLR-010`
Execute in order. "Exhausted" only if BOTH sub-campaigns done with concrete evidence.

### SUB-CAMPAIGN 1: EXECUTE FCLR-010 (TRACK A CONFIRMATORY, HYPERLIQUID) — HEAVY, UNAVOIDABLE
**Prerequisites ALL MET:** protocol pre-registered (done), coverage audit done (12 monthly parquet files cached, 199 native perps, 12 blocks), splits frozen (frozen_before_outcomes=true).
**Steps:**
1. **Execute FCLR-010:** run `python scripts/fclr010_execute.py` (builds panel from ironflow labels, fits fixed-form B0/B1/C1/C2 logistic models for binary occurrence, block-bootstrap CI >=2000 replicates, Holm correction, gate assessment). Outputs `research_state/evaluation_summary_FCLR010.md` and updates `run_manifest.json#experiments.FCLR-010`.
2. **Gate:** MET only if combined vs RV-only improves on primary label with 95% CI excluding zero on improving side, practical materiality floor (>=2% relative reduction) met, >=5 instruments, >=3 non-overlapping 30-day test blocks, calibration OK; else NOT_MET, null preserved.
3. **Update artifacts:** `research_state/experiment_frontier.json`, `AGENT_HANDOFF.md`, `research_state/hypothesis_registry.json` (FCLR-H004 status transition).

**Constraints:** cross-track firewall — NO Binance data, no merging Hyperliquid labels with Binance price panels. Do not relax rubric/floor/CI/block minimums. Do not relabel exploratory as confirmatory. No .github/workflows/* changes. Commit nothing merely for activity.

### SUB-CAMPAIGN 2: COUPLED INTEGRATION SYNTHESIS (FALLBACK, ONLY IF FCLR-010 CANNOT RUN)
**Trigger:** Sub-campaign 1 blocked after execution attempt.
**Goal:** Produce `research_state/coupled_integration_analysis_YYYYMMDDTHHMMSSZ.md` synthesizing: FCLR-009 (−0.43%, CI crosses zero, NOT_MET), FCLR-008 (+4.30%, CI crosses zero), Track A reopen evidence (ironflow), Track B CLOSED_NEGATIVE, H002 PARTIAL. Preserve modeled≠observed separation; propose SPECIFIC testable coupled hypotheses with exact data needs and probe plan; label modeled vs observed; NO status-only report.

### BOTTLENECK REMOVAL (ENFORCED)
- All FCLR-010 prerequisites are now DONE (protocol frozen, coverage audit complete, splits frozen). No more source discovery, no more split deliberation, no more pre-registration delay. Execute immediately.
- Do NOT re-litigate sealed confirmatory panels (FCLR-001/002/003/006/007/008) or re-run FCLR-009 — exhausted, reproducibility verified. Re-running is busywork, forbidden.
- Do NOT re-probe Track A source families — irrefutable structural block for those routes; ironflow is the sole admissible route (registry v1.2).
- Do NOT threshold-shop, relax the >=2% floor or CI criterion, or relabel exploratory as confirmatory.
- No dashboards/orchestrators/wrappers/polling/status-only files. No `.github/workflows/*` changes.
- Integrity: preserve negatives, Holm correction, block-aware inference, chronological leakage-resistant evaluation, cross-track firewall.
- Efficiency: remove bottlenecks. Only this file is the durable handoff.

## CURRENT STATE (DO NOT RE-LITIGATE)
- Tests: 27/27 PASS (`python -m unittest discover -s tests -v`)
- Track C (FCLR-H001): NOT_SUPPORTED / CONFIRMATORY CLOSED — all panels exhausted: FCLR-003 −3.78%, FCLR-006 −69.90% (worse), FCLR-007 −3.42% (worse), FCLR-008 +4.30% CI crosses zero (NOT_MET), FCLR-009 −0.43% CI [-0.003120, 0.006165] crosses zero (NOT_MET, executed 2026-11-01T04:48:20Z, `evaluation_summary_FCLR009.md`). Overlay INELIGIBLE (gate never passed).
- Track A (FCLR-H004): REOPENED — ironflow passes all rubric (registry v1.2). FCLR-010 pre-registered, coverage audit DONE (2026-11-01T07:34:22Z), splits FROZEN (2026-11-01T05:39:07Z), execution PENDING. Binance/Bybit/OKX/Deribit/HF/Zenodo/GitHub/CryptoDataDownload routes irrefutably blocked.
- Track B (FCLR-H003): CLOSED_NEGATIVE — no robust incremental skill after Holm (16 cells). Evidence: `evaluation_summary_FCLR-H003-EXT-001.md`, `track_b_separation_proof_hardened.md`.
- H002 (correction-time): PARTIAL — p=0.0792, direction matches paper, not significant, SSRN blocked → exploratory only.
- Sealed holdout integrity: preserved (`sealed_holdout_integrity.md`).

## GATE STATES PER TRACK (with evidence)
| Track | Hypothesis | Status | Evidence |
|-------|-----------|--------|----------|
| C | FCLR-H001 | NOT_SUPPORTED / CONFIRMATORY CLOSED | `evaluation_summary_FCLR009.md`, `evaluation_summary_FCLR008.md`, `track_c_final_synthesis_dossier.md` |
| A | FCLR-H004 | REOPENED — FCLR-010 pre-registered, coverage done, splits frozen, EXECUTION PENDING | `data_source_registry.json` v1.2, `research_protocol_fclr010.md`, `fclr010_coverage_audit.json`, `run_manifest.json#split_boundaries_fclr010` |
| B | FCLR-H003 | CLOSED_NEGATIVE | `evaluation_summary_FCLR-H003-EXT-001.md` |
| H002 | correction-time | PARTIAL / EXPLORATORY | `h002_replication_report.md`, `hypothesis_registry.json` |
| Overlay | — | INELIGIBLE | `gate_assessment.md`, `research_protocol.md` §9 |

## REQUIRED END-OF-SESSION OUTPUT
1. What changed and why (concrete files/lines)
2. What was actually tested (exact commands + outcomes)
3. Evidence added (probes with URLs/status/headers/paths tried, hashes if data found)
4. Gate states per track (A/B/C/H002/overlay) with evidence
5. Single highest-value next task (executable without user intervention)
6. Precise verify command for next task
7. Blockers + next materially different free route OR proof of exhaustive search with concrete next probes

## SINGLE HIGHEST-VALUE NEXT TASK + VERIFY COMMAND
**Task:** Execute FCLR-010 — run `python scripts/fclr010_execute.py`, confirm it completes without the "splits not frozen" RuntimeError, writes `research_state/evaluation_summary_FCLR010.md` with gate assessment (PASSED or NOT_MET), and updates `run_manifest.json#experiments.FCLR-010` to COMPLETE/COMPLETE_NOT_MET.
**Verify command:**
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python -m unittest discover -s tests -v   # 27/27 PASS
python scripts/fclr010_execute.py   # must complete, write evaluation_summary_FCLR010.md
test -f research_state/evaluation_summary_FCLR010.md && echo EVAL_WRITTEN
python3 -c "import json; d=json.load(open('research_state/run_manifest.json')); e=d['experiments']['FCLR-010']; print(e['status'], '|', e['gate'])"
```

**MANDATE:** Prioritize by repo name — COUPLE funding-conditioned volatility with liquidation risk. Track A is reopened via ironflow; execute FCLR-010 with outcomes frozen until pre-registration is honored. Never avoid heavy working.
