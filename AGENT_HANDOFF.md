# AGENT_HANDOFF.md (DURABLE - FCLR-HANDOFF-022)
**TIMESTAMP (UTC):** 2026-11-01T04:44:56Z
**REPO:** Funding-conditioned-volatility-and-liquidation-risk
**BRANCH/HEAD:** main @ 676fe7d3 (working tree: clean)
**HANDOFF ID:** FCLR-HANDOFF-022-20261101T044456Z
**STATUS:** OPEN — HEAVY WORK PENDING (Track A reopen probe + coupled integration synthesis fallback)
**PRIORITIZED BY:** repo name = funding-conditioned volatility ∩ liquidation risk as ONE coupled problem

## INITIAL TASK MESSAGE (FOR NEXT AGENTIC SESSION) — TIMESTAMPED 2026-11-01T04:44:56Z
**PRIORITY P0 | TYPE: HEAVY DATA DISCOVERY + COUPLED SYNTHESIS (FALLBACK)**

**REPO NAME IS THE SPEC:** Couple funding-conditioned volatility (Track C) with liquidation risk (Track A). Do NOT re-run sealed confirmatory panels (FCLR-001/002/003/006/007/008) — all exhausted, byte-identical reproducibility already verified. Do NOT re-probe Track A source families already in `track_a_final_block_proof.md` / `track_a_deadend_map.md` / `liquidation_sources_enumeration.md` — irrefutable structural block.

The ONLY path to reopen confirmatory work: find ONE NEW admissible unauthenticated source (no keys) meeting ALL rubric items, OR produce the coupled integration analysis fallback (below).

### MANDATORY FIRST ACTION (30s)
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
git log -1 --oneline && git status --short
python -m unittest discover -s tests -v  # MUST remain 27/27 PASS
cat research_state/track_a_final_block_proof.md | tail -20   # confirm structural block is irrefutable
```

## FOCUS CAMPAIGN: `FCLR-COUPLED-REOPEN-OR-SYNTHESIZE`
Execute in order. "Exhausted" only if BOTH sub-campaigns done with concrete evidence.

### SUB-CAMPAIGN 1: TRACK A NEW-SOURCE DISCOVERY (REOPEN PATH) — HEAVY, UNAVOIDABLE
**Goal:** Find ONE NEW admissible unauthenticated observed-liquidation source meeting the verbatim rubric (from `track_a_final_block_proof.md`, do not relax):
`unauthenticated==true AND no_keys==true AND symbols>=5 AND blocks>=3 (non-overlapping 30-day) AND completeness_doc==true AND license_ok==true AND census_or_defensible==true`
ALL must pass; ANY failure → NO-GO.

**Probe (5+ materially distinct families, do NOT repeat enumerated dead ends):**
1. Binance alt archive paths NOT already probed (monthly/ liquidationHistory/, forceLiquidation/, quarterly/ naming variants) — unauthenticated GET only.
2. Bybit public archive locations beyond the single FCLR-005 window (linear/liquidation/, trading/liquidation/, other CDN) — unauthenticated.
3. OKX static.okx.com CDN historical liquidation records — unauthenticated.
4. Deribit historical.deribit.com liquidation history — unauthenticated.
5. HuggingFace datasets API (unauthenticated GET) for perp liquidation census beyond ochinimus single window.
6. Zenodo/OSF/arXiv supplements with downloadable liquidation event records (no signup).
7. GitHub raw CSV/Parquet in public repos for liquidationSnapshot/forceOrders census.
8. CryptoDataDownload and other academic/market-data mirrors with unauthenticated liquidation history.

**Rubric (ALL MUST PASS before GO):** unauthenticated + no_keys + >=5 perp symbols + >=3 non-overlapping 30-day blocks + documented completeness (census vs capped sample explicitly stated) + license/ToS OK for research + defensible records.

**If ANY pass:** Add to `data_source_registry.json` with hashes/vintages, PRE-REGISTER protocol BEFORE inspecting outcomes, freeze splits, new experiment ID (e.g. FCLR-009+). Do not inspect outcomes before pre-registration.
**If NONE pass:** Write `research_state/track_a_discovery_gap_YYYYMMDDTHHMMSSZ.md` with EVERY URL probed, HTTP status/headers, paths tried, errors, and 3-5 SPECIFIC next probes (different families/mirrors/formats). Then proceed to SUB-CAMPAIGN 2.

### SUB-CAMPAIGN 2: COUPLED INTEGRATION SYNTHESIS (FALLBACK — FORCE PROGRESS NO MATTER WHAT)
**Trigger:** Sub-campaign 1 finds NO new admissible data (expected, given structural block).
**Goal:** Test the coupled hypothesis (funding-conditioned volatility → liquidation risk) on the evidence that EXISTS, without fabricating observed liquidation labels.
**You MUST produce:** `research_state/coupled_integration_analysis_YYYYMMDDTHHMMSSZ.md` synthesizing:
- FCLR-008: +4.30% relative QLIKE (C2 vs B1), 95% CI [-0.029938, 0.000524] crosses zero → first unsealed panel with positive direction, gate NOT_MET.
- Track A: structurally blocked (irrefutable proof) → no observed liquidation census for confirmatory.
- H002 partial: direction matches paper (high-RV median 16.0h vs low-RV 8.0h, log-rank p=0.0792) but not significant, SSRN blocked → exploratory only.
- Track B: CLOSED_NEGATIVE (no robust incremental skill after Holm), strictly separated from observed liquidations.

The analysis must: preserve Track B modeled ≠ Track A observed separation; propose SPECIFIC testable coupled hypotheses with concrete data needs and an EXACT probe plan (URLs, methods, rubric); label clearly what is modeled/synthetic vs observed; NO status-only report. Make it actionable for the next agent.

### BOTTLENECK REMOVAL (ENFORCED)
- Do NOT re-litigate sealed confirmatory panels (FCLR-001/002/003/006/007/008) — exhausted, reproducibility verified. Re-running is busywork, forbidden.
- Do NOT re-probe Track A source families in the final block proof / deadend map / enumeration — irrefutable structural block. Only NEW materially distinct families count.
- Do NOT threshold-shop, relax the >=2% floor or CI criterion, or relabel exploratory as confirmatory.
- No dashboards/orchestrators/wrappers/polling/status-only files. No `.github/workflows/*` changes. Commit nothing merely for activity.
- Integrity: preserve negatives, Holm correction, block-aware inference, chronological leakage-resistant evaluation.
- Efficiency: remove bottlenecks. Only this file is the durable handoff.

## CURRENT STATE (DO NOT RE-LITIGATE)
- Tests: 27/27 PASS (`python -m unittest discover -s tests -v`)
- Track C (FCLR-H001): NOT_SUPPORTED — CONFIRMATORY CLOSED. FCLR-008 +4.30% rel QLIKE, CI [-0.029938, 0.000524] crosses zero → gate NOT_MET. All panels exhausted (FCLR-003 -3.78%, FCLR-006 -69.90%, FCLR-007 -3.42%, FCLR-008 +4.30% CI crosses zero). Overlay INELIGIBLE. Evidence: `track_c_final_synthesis_dossier.md`, `evaluation_summary_FCLR008.md`, `gate_assessment.md`.
- Track A (FCLR-H004): STRUCTURALLY BLOCKED — NO admissible unauthenticated source passes rubric. Irrefutable machine-checkable proof. Evidence: `track_a_final_block_proof.md`, `data_source_registry.json` (all liquidation sources inadmissible).
- Track B (FCLR-H003): CLOSED_NEGATIVE — no robust incremental skill after Holm (16 cells), separation from observed liquidations proven. Evidence: `evaluation_summary_FCLR-H003-EXT-001.md`, `track_b_separation_proof_hardened.md`.
- H002 (correction-time replication): PARTIAL — 88 events Jan-Mar 2024, p=0.0792 direction matches paper, not significant, SSRN HTTP 403 blocks methodology → not promotable. Evidence: `h002_replication_report.md`, `hypothesis_registry.json`.
- Sealed holdout integrity: preserved (no reuse/tuning). Evidence: `sealed_holdout_integrity.md`.

## GATE STATES PER TRACK (with evidence)
| Track | Hypothesis | Status | Evidence |
|-------|-----------|--------|----------|
| C | FCLR-H001 | NOT_SUPPORTED / CONFIRMATORY CLOSED | `evaluation_summary_FCLR008.md`, `track_c_final_synthesis_dossier.md` |
| A | FCLR-H004 | STRUCTURALLY BLOCKED | `track_a_final_block_proof.md`, `data_source_registry.json` |
| B | FCLR-H003 | CLOSED_NEGATIVE | `evaluation_summary_FCLR-H003-EXT-001.md` |
| H002 | correction-time | PARTIAL / EXPLORATORY | `h002_replication_report.md`, `hypothesis_registry.json` |
| Overlay | — | INELIGIBLE (gate never passed) | `gate_assessment.md`, `research_protocol.md` §9 |

## REQUIRED END-OF-SESSION OUTPUT
1. What changed and why (concrete files/lines)
2. What was actually tested (exact commands + outcomes)
3. Evidence added (probes with URLs/status/headers/paths tried, hashes if data found)
4. Gate states per track (A/B/C/H002/overlay) with evidence
5. Single highest-value next task (executable without user intervention)
6. Precise verify command for next task
7. Blockers + next materially different free route OR proof of exhaustive search with concrete next probes

## SINGLE HIGHEST-VALUE NEXT TASK + VERIFY COMMAND
**Task:** Execute Sub-campaign 1 Track A discovery (probe 5+ NEW materially distinct unauthenticated liquidation-source families against the verbatim rubric). If none pass, write `track_a_discovery_gap_*.md` AND produce `coupled_integration_analysis_*.md` (Sub-campaign 2).
**Verify command:**
```bash
cd /home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk
python -m unittest discover -s tests -v   # 27/27 PASS
ls research_state/track_a_discovery_gap_*.md research_state/coupled_integration_analysis_*.md 2>/dev/null || echo "PENDING: discovery gap + coupled synthesis not yet written"
cat research_state/track_a_final_block_proof.md | grep -c "NO candidate passes ALL rubric items"   # expect 1 (irrefutable block confirmed)
```

**MANDATE:** Prioritize by repo name — COUPLE funding-conditioned volatility with liquidation risk. Do heavy discovery. Never avoid heavy working.
