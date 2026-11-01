# AGENT_HANDOFF.md (DURABLE - FCLR-HANDOFF-023)
**TIMESTAMP (UTC):** 2026-11-01T04:52:00Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ ab926bc1 (working tree: clean except untracked research_state/evaluation_summary_FCLR009.md pending commit decision)
**HANDOFF ID:** FCLR-HANDOFF-023-20261101T045200Z
**STATUS:** OPEN — FCLR-009 COMPLETE (gate NOT_MET); Track A REOPENED via NEW admissible source (ironflow Hyperliquid census); FCLR-010 PRE-REGISTERED BEFORE OUTCOMES, awaiting execution
**PRIORITIZED BY:** repo name = funding-conditioned volatility ∩ liquidation risk as ONE coupled problem

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T04:52:00Z
**PRIORITY P0 | TYPE: HEAVY COUPLED EXECUTION (FCLR-010 TRACK A CONFIRMATORY ON HYPERLIQUID)**

**REPO NAME IS THE SPEC:** Couple funding-conditioned volatility with liquidation risk. Track A is now REOPENED: `ironflow_hyperliquid_liquidation_events` (HuggingFace, CC BY 4.0, unauthenticated) passed ALL rubric items (unauthenticated, no_keys, symbols>=5 [185 native perps], blocks>=3 [12 monthly blocks 2025-11..2026-10], completeness_doc, license_ok, census_or_defensible). Files hashed and cached at `research_state/data_cache/ironflow_events/`.

FCLR-010 is PRE-REGISTERED (`research_state/research_protocol_fclr010.md`, v1.0, frozen 2026-11-01T04:52:00Z) BEFORE any outcome inspection. **No model may be fitted to liquidation labels and no label-outcome relationship may be inspected until splits are frozen in `run_manifest.json#split_boundaries_fclr010` (frozen_before_outcomes=true).**

### MANDATORY FIRST ACTION (30s)
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
git log -1 --oneline && git status --short
python -m unittest discover -s tests -v  # MUST remain 27/27 PASS
cat research_state/run_manifest.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['experiments']['FCLR-009']['status'], '|', d['experiments']['FCLR-009']['gate'])"
cat research_state/data_source_registry.json | python3 -c "import json,sys; d=json.load(sys.stdin); s=[x for x in d['sources'] if x['source_id']=='ironflow_hyperliquid_liquidation_events'][0]; print(s['status'], '|', all(s['rubric'].values()))"
```

## FOCUS CAMPAIGN: `FCLR-COUPLED-EXECUTE-FCLR-010`
Execute in order. "Exhausted" only if BOTH sub-campaigns done with concrete evidence.

### SUB-CAMPAIGN 1: EXECUTE FCLR-010 (TRACK A CONFIRMATORY, HYPERLIQUID) — HEAVY, UNAVOIDABLE
**Steps:**
1. **Coverage-only audit (OUTCOMES STILL FROZEN):** verify Hyperliquid public funding/mark API endpoints (api.hyperliquid.xyz/info, unauthenticated) — history depth, cadence, auth requirements, symbol coverage vs 185 native perps; label/predictor overlap audit vs ironflow census. Record URLs, statuses, headers, coverage. Do NOT fit models or inspect label-outcome relationships.
2. **Freeze splits:** write `run_manifest.json#split_boundaries_fclr010` with `frozen_before_outcomes=true`, chronological 60/20/20, 7-day purge/embargo, >=5 instruments, >=3 non-overlapping 30-day blocks.
3. **Execute:** run FCLR-010 (funding-augmented vs RV-only baseline on liquidation occurrence/intensity), write `research_state/evaluation_summary_FCLR010.md` + gate assessment, block bootstrap CI, Holm correction.
4. **Gate:** MET only if combined vs RV-only improves on primary label with 95% CI excluding zero on improving side, floor met, >=5 instruments, >=3 blocks, calibration OK; else NOT_MET, null preserved.

**Constraints:** cross-track firewall — NO Binance data, no merging Hyperliquid labels with Binance price panels. Do not relax rubric/floor/CI/block minimums. Do not relabel exploratory as confirmatory. No .github/workflows/* changes. Commit nothing merely for activity.

### SUB-CAMPAIGN 2: COUPLED INTEGRATION SYNTHESIS (FALLBACK, ONLY IF FCLR-010 CANNOT RUN)
**Trigger:** Sub-campaign 1 blocked on Hyperliquid predictor access after the coverage audit.
**Goal:** Produce `research_state/coupled_integration_analysis_YYYYMMDDTHHMMSSZ.md` synthesizing: FCLR-009 (−0.43%, CI crosses zero, NOT_MET), FCLR-008 (+4.30%, CI crosses zero), Track A reopen evidence (ironflow), Track B CLOSED_NEGATIVE, H002 PARTIAL. Preserve modeled≠observed separation; propose SPECIFIC testable coupled hypotheses with exact data needs and probe plan; label modeled vs observed; NO status-only report.

### BOTTLENECK REMOVAL (ENFORCED)
- Do NOT re-litigate sealed confirmatory panels (FCLR-001/002/003/006/007/008) or re-run FCLR-009 — exhausted, reproducibility verified (FCLR-009 byte-identical rerun verified 2026-11-01). Re-running is busywork, forbidden.
- Do NOT re-probe Track A source families in the final block proof / deadend map / enumeration — irrefutable structural block for THOSE routes; ironflow is the NEW admissible route (registry v1.2).
- Do NOT threshold-shop, relax the >=2% floor or CI criterion, or relabel exploratory as confirmatory.
- No dashboards/orchestrators/wrappers/polling/status-only files. No `.github/workflows/*` changes.
- Integrity: preserve negatives, Holm correction, block-aware inference, chronological leakage-resistant evaluation, cross-track firewall.
- Efficiency: remove bottlenecks. Only this file is the durable handoff.

## CURRENT STATE (DO NOT RE-LITIGATE)
- Tests: 27/27 PASS (`python -m unittest discover -s tests -v`)
- Track C (FCLR-H001): NOT_SUPPORTED / CONFIRMATORY CLOSED — all panels exhausted: FCLR-003 −3.78%, FCLR-006 −69.90% (worse), FCLR-007 −3.42% (worse), FCLR-008 +4.30% CI crosses zero (NOT_MET), FCLR-009 −0.43% CI [-0.003120, 0.006165] crosses zero (NOT_MET, executed 2026-11-01T04:48:20Z, `evaluation_summary_FCLR009.md`). Overlay INELIGIBLE (gate never passed).
- Track A (FCLR-H004): REOPENED — Binance/Bybit/OKX/Deribit/HF/Zenodo/GitHub/CryptoDataDownload routes irrefutably blocked (see track_a_final_block_proof.md / track_a_deadend_map.md). NEW admissible source `ironflow_hyperliquid_liquidation_events` passes all rubric items (data_source_registry.json v1.2). FCLR-010 pre-registered, splits NOT yet frozen, outcome inspection frozen.
- Track B (FCLR-H003): CLOSED_NEGATIVE — no robust incremental skill after Holm (16 cells). Evidence: `evaluation_summary_FCLR-H003-EXT-001.md`, `track_b_separation_proof_hardened.md`.
- H002 (correction-time): PARTIAL — p=0.0792, direction matches paper, not significant, SSRN blocked → exploratory only.
- Sealed holdout integrity: preserved (`sealed_holdout_integrity.md`).

## GATE STATES PER TRACK (with evidence)
| Track | Hypothesis | Status | Evidence |
|-------|-----------|--------|----------|
| C | FCLR-H001 | NOT_SUPPORTED / CONFIRMATORY CLOSED | `evaluation_summary_FCLR009.md`, `evaluation_summary_FCLR008.md`, `track_c_final_synthesis_dossier.md` |
| A | FCLR-H004 | REOPENED — new admissible source, FCLR-010 pre-registered | `data_source_registry.json` v1.2, `research_protocol_fclr010.md`, `track_a_final_block_proof.md` |
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
**Task:** FCLR-010 Step 1 — coverage-only audit of Hyperliquid public funding/mark API (api.hyperliquid.xyz/info) + label/predictor overlap audit vs ironflow census (OUTCOMES FROZEN); then freeze splits in run_manifest.json#split_boundaries_fclr010 and execute FCLR-010.
**Verify command:**
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python -m unittest discover -s tests -v   # 27/27 PASS
python3 -c "import json; d=json.load(open('research_state/run_manifest.json')); print(d['experiments']['FCLR-009'])"
python3 -c "import json; d=json.load(open('research_state/data_source_registry.json')); s=[x for x in d['sources'] if x['source_id']=='ironflow_hyperliquid_liquidation_events'][0]; print(s['status'], all(s['rubric'].values()))"
ls research_state/data_cache/ironflow_events/ | wc -l   # expect 12
test -f research_state/research_protocol_fclr010.md && echo PROTOCOL_PREREGISTERED
```

**MANDATE:** Prioritize by repo name — COUPLE funding-conditioned volatility with liquidation risk. Track A is reopened via ironflow; execute FCLR-010 with outcomes frozen until pre-registration is honored. Never avoid heavy working.
