# AGENT_HANDOFF.md (SINGLE DURABLE SOURCE OF TRUTH — mirrors root)

**TIMESTAMP:** 20261103T070210Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**PRIORITY (by repo name):** LIQUIDATION REOPEN = MAXIMUM (Track A observed-liquidation labels are the single gating missing piece; H004 BLOCKED) | VOLATILITY H001 = MAINTAIN-GREEN-ONLY (INCONCLUSIVE on all exhausted confirmatory panels, CI crosses zero, overlay INELIGIBLE — do NOT re-run sealed panels)
**CAMPAIGN:** LIQUIDATION_SOURCE_REOPEN_HEAVY-001 — deep rubric verification of every REVIEW_REQUIRED alt source until a GO source is found or the blocker is re-proven with evidence

## SESSION GOAL
Remove the Track A idle-wait bottleneck. Ironflow forward months 2026-11,12,2027-01,02 all return 404 (consec_absent=3, data_through=2026-10, resume_trigger_met=false). Do NOT poll the blocked forward edge. Every session: <1 min monitor check, then 100% effort on deep-rubric verification of the 12 REVIEW_REQUIRED alternative liquidation sources. A GO source -> fresh pre-registered experiment ID -> confirmatory Track A run -> unblocks H004 / overlay eligibility. Heavy work is mandatory; no coasting.

## CRYSTAL-CLEAR INITIAL TASK (EXECUTE IMMEDIATELY, IN THIS ORDER)

```bash
# PHASE 1: STATE VERIFY (< 2 min) — bounded, never idle-wait
python scripts/monitor_ironflow_liquidations.py --quick
python scripts/monitor_ironflow_liquidations.py --verify
python -m unittest discover -s tests -v | tail -3   # must stay 111/111 PASS

# PHASE 2: HEAVY — DEEP RUBRIC VERIFICATION OF ALL REVIEW_REQUIRED SOURCES (this session's main work)
python scripts/hunt_alternative_liquidation_sources.py   # refreshes research_state/data_source_registry_alt_hunt.json
# Then, for EVERY candidate with rubric_assessment == REVIEW_REQUIRED, run a full FCLR rubric check:
#   unauthenticated path? >=5 symbols OR >=1 complete month OR >=3 non-overlapping 30-day blocks?
#   schema mappable to FCLR-010 liquidation events/fills? completeness documented? license OK? no keys/signed/requester-pays?
# Write one evidence artifact per source: research_state/alt_source_deep_review_YYYYMMDDTHHMMSSZ.md
#   with exact URL, method, status code, headers, body sample, rubric pass/fail, and verdict GO / NO-GO / REVIEW_REQUIRED.

# PHASE 3: DECIDE & RECORD
#   If ANY source = GO: create fresh pre-registration BEFORE outcome inspection (new experiment ID),
#     freeze splits, run frozen harness, write evaluation_summary + gate assessment.
#   If ALL = NO-GO: write fresh research_state/blocker_evidence_YYYYMMDDTHHMMSSZ.md (all commands, URLs, timestamps),
#     update resume triggers, keep ironflow --quick as the sole <1 min keep-alive.
#   Update experiment_frontier.json + this AGENT_HANDOFF.md with the successor's exact next task.
#   Keep tests green (111+). Add tests for any new probe/rubric logic.
```

## VERIFIED TRUTH (20261103T070210Z)

- **Track A (observed liquidations):** BLOCKED_ON_DATA (STRUCTURAL). Ironflow cached through 2026-10 intact (18 month pairs, content_hash_complete=True, baseline_drift=False). Forward months 2026-11,12,2027-01,02 all 404; consec_absent=3; resume_trigger_met=false. FCLR-010 (Hyperliquid census 2025-11..2026-10) COMPLETE, gate PASSED, sealed. Alt sources: 12 REVIEW_REQUIRED, 0 GO. No admissible unauthenticated liquidation source found. Sole reopen path = NEW admissible unauthenticated source passing FULL rubric (>=5 symbols or equivalent, >=1 complete month OR >=3 non-overlapping 30-day blocks, schema mappable to FCLR-010 events/fills, unauthenticated, no keys/signed/requester-pays, license OK, completeness documented).
- **Track B (funding-conditioned volatility):** H001 INCONCLUSIVE on decisive unsealed panel FCLR-008 (2026-01-01..2026-08-06, 5 symbols, 218 days, 7 blocks, n=10785; C2 vs B1 +4.30% rel QLIKE, CI [-0.029938, 0.000524] crosses zero). All confirmatory panels exhausted (FCLR-001/002/003/006/007/008). Overlay INELIGIBLE. No untested Track B confirmatory cell under current admissible data without NEW admissible data + fresh pre-registered experiment ID. Do NOT re-run sealed panels. Tests: 111/111 PASS. Keep green.

## BOTTLENECKS ELIMINATED NOW

1. **Idle-wait on Track A removed** — Session starts with <1 min `monitor --quick` / `--verify`; then 100% deep alt-source rubric verification. No polling loops, no repeated re-probes of dead routes (Binance 404/451, Bybit 404, OKX 403/404, Deribit connect-fail, GitHub 401, CCD, paywalled Tardis/CryptoHFT).
2. **Shallow source review removed** — Every REVIEW_REQUIRED source gets a full FCLR rubric check with concrete evidence (URL, status, headers, body sample, pass/fail) in a timestamped `alt_source_deep_review_*.md`. No "REVIEW_REQUIRED" left unevaluated.
3. **Track B sealed-panel re-run removed** — H001 INCONCLUSIVE; all confirmatory panels exhausted. No threshold-shopping, no relaxing the >=2% floor or CI criterion, no relabeling exploratory as confirmatory.
4. **Unverifiable "GO" removed** — A source is GO only after full rubric evidence is written; HTTP 200 / green CI / model convergence is NOT acceptance.

## FOCUS CAMPAIGN: LIQUIDATION_SOURCE_REOPEN_HEAVY-001 (NON-OPTIONAL, HEAVY)

Objective: find a new admissible unauthenticated observed-liquidation source with a confirmatory-feasible window, or re-prove the structural blocker with complete evidence.

REVIEW_REQUIRED candidates to deep-verify (from research_state/alt_source_scan_*.json and alt_source_deep_review_20261103T060340Z.md):
- huggingface_other_datasets (ironflow/hyperliquid-liquidations metadata — already GO via FCLR-010, NOT new; check for additional liquidation datasets)
- huggingface_liquidation_search_broad (Gopher-Lab/bankless..., ochinimus/crypto-liquidation-ticks exhausted 2026-07-08..2026-08-06)
- zenodo (hyperliquid liquidations / crypto liquidation perpetual records)
- osf (OSF API root)
- arxiv (hyperliquid liquidations / crypto liquidation perpetual)
- data_commoncrawl (index root probe)
- kaggle (metadata-only mirror; download auth-gated — trigger only, not a data source)
- github_code_search_unauth (401 — NO-GO, do not repeat)
- github_repos_search (hyperliquid liquidations repos)
- coinglass_public (LiquidationData HTML — no unauthenticated historical census)
- hyblock_public, coinank_public, paradigm_research (public-site probes)

Acceptance (one of):
- GO source found: research_state/alt_source_deep_review_*.md with full rubric pass + evidence; fresh pre-registered experiment ID; frozen splits; evaluation_summary + gate assessment; tests green.
- All NO-GO: research_state/blocker_evidence_YYYYMMDDTHHMMSSZ.md with every command/URL/timestamp; updated resume triggers; AGENT_HANDOFF.md successor task.

Resume triggers (Track A):
- Ironflow: GET https://huggingface.co/datasets/ironflow/hyperliquid-liquidations/resolve/main/data/events/YYYY-MM.parquet and /data/fills/YYYY-MM.parquet return 200 for YYYY-MM >= 2026-11 (via `scripts/monitor_ironflow_liquidations.py --quick` / `--decision` / `--scan`).
- OR new source passes GO: >=5 symbols, >=1 complete month OR >=3 non-overlapping 30-day blocks, documented completeness/coverage/license OK, unauthenticated only, schema compatible with frozen FCLR-010 (Hyperliquid-only for Track A).

## MANDATORY DELIVERABLES THIS SESSION

- [ ] `research_state/data_source_registry_alt_hunt.json` refreshed (hunt script)
- [ ] `research_state/alt_source_deep_review_YYYYMMDDTHHMMSSZ.md` — full rubric pass/fail + evidence for EVERY REVIEW_REQUIRED source
- [ ] `research_state/blocker_evidence_YYYYMMDDTHHMMSSZ.md` if all NO-GO (or fresh pre-reg + evaluation if GO)
- [ ] Updated `research_state/experiment_frontier.json` and this `AGENT_HANDOFF.md` with successor's exact next task
- [ ] `python -m unittest discover -s tests -v` passes (111+); add tests for new probe/rubric logic
- [ ] Track A keep-alive: `monitor_ironflow_liquidations.py --quick` evidence (< 1 min)

## CRITICAL RULES

- Research only. No trading / paper / live / API orders. No credentials. Unauthenticated sources only.
- No .github/workflows changes (protected control plane).
- Track separation: modeled boundary breaches != observed liquidations. Never label a modeled proxy as observed.
- Leakage-resistant: chronological splits, train-only normalization, purge/embargo, freeze protocol before holdout.
- Never re-run sealed/exhausted confirmatory panels (FCLR-001..008). Fresh experiment ID required for any new confirmatory cell.
- Heavy work always. If Track A blocked, full effort on the reopen campaign. Never idle.
- Evidence-based. Timestamp everything. No placeholder "REVIEW_REQUIRED" without a dated artifact.

## NEXT SESSION'S SINGLE HIGHEST-VALUE TASK

Complete LIQUIDATION_SOURCE_REOPEN_HEAVY-001 Phase 2: deep-rubric verify every REVIEW_REQUIRED alt source with timestamped evidence artifacts; if GO, pre-register + run confirmatory Track A; if NO-GO, write fresh blocker evidence and keep ironflow --quick as the sole keep-alive. Verify: `python -m unittest discover -s tests -v` (111+) and a dated `research_state/alt_source_deep_review_*.md` covering all REVIEW_REQUIRED sources.
