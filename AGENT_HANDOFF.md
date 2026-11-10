# AGENT_HANDOFF.md — Single Durable Handoff (next session MUST continue from here)

**Updated:** 2026-11-10T05:26:53Z — **P0 = FINAL SYNTHESIS & FORMAL CONCLUSION CAMPAIGN.** Repository name `Funding-conditioned-volatility-and-liquidation-risk` resolves priority: **ALL CONFIRMATORY TRACKS EXHAUSTED/NULL.** Track C (volatility forecasting): H001 NOT_SUPPORTED across 7+ claim-worthy panels (FCLR-001, 003, 008, 009, 011, 012-V, 013, GATE4 v3 30d). Track B (boundary breach): H003 NOT_SUPPORTED (FCLR-H003-EXT-001, Holm-adjusted, no robust skill). Track A (observed liquidation): STRUCTURALLY BLOCKED — no admissible unauthenticated source (Hyperliquid-only, 2026-11..2027-02 absent). H002 (Shek replication): PARTIAL_REPLICATION — direction reproduced (high-RV 16h > low-RV 8h) but NOT significant (p=0.079), magnitude differs (paper 27h/3h vs reconstructed 16h/8h), smaller universe (5 vs 18 contracts), paper methodology inaccessible (SSRN 403). **No network. No new data. No confirmatory gate met. Structural stop is final for confirmatory program.**

## 0) INITIAL TASK MESSAGE — 2026-11-10T05:26:53Z — MANDATORY HEAVY WORK (NEXT SESSION, UNAVOIDABLE)

**START HERE. FINAL SYNTHESIS CAMPAIGN.** All confirmatory tracks exhausted. No further confirmatory experiments possible without admissible external data (network prohibited). The only remaining scientifically honest heavy work is **comprehensive final synthesis** documenting the exhaustive null results with proper multiplicity correction across the entire tested family.

### Do in order

1. **Verify current state (dep-light gate):**
   `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator tests.test_trackc_provenance_lineage -v` → expect **48/48 OK** (core 39 + provenance lineage 9).

2. **Confirm structural stop evidence is current (re-audit):**
   - `python scripts/trackc_panel_deep_audit_orchestrator.py --cache research_state/data_cache --repo-root . --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --window-hint 2024_10,2024_11,2024_12 --min-symbols 5 --min-blocks 3 --out research_state/trackc_deep_audit_orchestrator_latest.json`
   - `python scripts/trackc_panel_deep_audit_orchestrator.py --cache research_state/data_cache --repo-root . --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --window-hint 2026_11 --min-symbols 5 --min-blocks 3 --out research_state/trackc_deep_audit_orchestrator_2026_11.json`
   Confirm both emit `confirmatory_resume_ready=false`, `provenance_verified=false`, `network_used=false`, `outcomes_computed=false`.

3. **Execute FINAL SYNTHESIS CAMPAIGN (heavy work):**
   Create `research_state/final_synthesis_report.md` with:
   - **Family-wide multiplicity correction**: Apply Holm/Bonferroni across ALL tested contrasts (H001: 8 experiments × 3+ primary contrasts = 24+ tests; H002: 1 contrast; H003: 16 cells × 2 horizons = 32 tests). Report raw and adjusted p-values/CIs.
   - **Per-hypothesis verdicts with evidence**:
     - H001 (Track C volatility): NOT_SUPPORTED — all claim-worthy panels null; best C2 vs B1 = -0.43% QLIKE (FCLR-009, CI crosses zero, << 2% floor).
     - H002 (Shek replication): PARTIAL_REPLICATION — direction reproduced, NOT significant (p=0.079), magnitude differs, paper methodology inaccessible.
     - H003 (Track B boundary breach): NOT_SUPPORTED — no cell significant after Holm (FCLR-H003-EXT-001).
     - Track A (observed liquidation): STRUCTURALLY_BLOCKED — no admissible unauthenticated source.
   - **Structural blockers documented**: No network, no paid data, no manual inputs, all local panels exhausted, no admissible liquidation source.
   - **Data provenance audit summary**: Local cache coverage, gaps (2024-10/11/12 series, 2026-11 funding), provenance not machine-verifiable (0 adjacent sha256 sidecars).
   - **Formal conclusion**: Confirmatory program complete. Null results preserved. No risk overlay eligible. Future work requires new admissible data source(s).

4. **Update hypothesis_registry.json** with final statuses:
   - H1_primary: NOT_SUPPORTED (frozen_at unchanged, add `final_verdict: NOT_SUPPORTED`, `evidence_summary: "7+ claim-worthy panels, all null, max -0.43% QLIKE improvement, CI crosses zero"`)
   - H2_shek_replication: PARTIAL_REPLICATION (add `final_verdict: PARTIAL_REPLICATION`, `evidence_summary: "direction reproduced p=0.079, magnitude differs, paper methodology inaccessible"`)

5. **Create final experiment_frontier.json entry** marking all confirmatory tracks as CONCLUDED/EXHAUSTED with `next_action: "requires_new_admissible_data_source"`.

6. **Update AGENT_HANDOFF.md** with UTC timestamp, exact commands, test counts, artifact paths/hashes, and `next_unfinished_task: "NONE — CONFIRMATORY PROGRAM CONCLUDED. Future sessions only if new admissible unauthenticated data source becomes available (network prohibited in this environment)."`

### Hard constraints
- No new confirmatory experiments, no threshold shopping, no sealed-holdout reuse.
- No Track A probing/scans (structurally blocked).
- No network/downloads/credentials/paid data/access-control bypass.
- No fabricated outcomes/provenance. No conflation of observed vs modeled vs correction-time.
- No `.github/workflows` edits; no schedulers/pollers/controllers.
- No live/paper trading.

### Bottleneck status (ALL STRUCTURAL, NONE REMOVABLE WITHOUT NETWORK)
- **B1 (full-cache scan timeout): REMOVED** — scoped orchestrator (`--window-hint`) verified.
- **B2 (2026-11 funding month missing all 5 symbols): STRUCTURAL** — not repairable locally.
- **B3 (2024-10/11/12 required-series gaps): STRUCTURAL** — not repairable locally.
- **B4 (provenance not machine-verifiable): STRUCTURAL** — 0 adjacent sha256 sidecars; manifests loaded but files unmapped.
- **B5 (Track A liquidation source): STRUCTURAL** — no admissible unauthenticated source exists.
- **B6 (H001 confirmatory gate): EXHAUSTED** — 7+ claim-worthy panels tested, all null.
- **B7 (H003 Track B gate): EXHAUSTED** — FCLR-H003-EXT-001 null after Holm.
- **B8 (H002 exact replication): BLOCKED** — paper methodology inaccessible (SSRN 403).

### Completed heavy work (evidence — FINAL STATE)
1. **Track C reproducibility + audit hardening** — COMPLETE (48/48 dep-light, scoped audits, provenance lineage integrated).
2. **Frozen confirmatory prereg skeletons** — COMPLETE (FCLR-009, FCLR-014, FCLR-H003-EXT-001, GATE4 v3/v4, all before outcomes).
3. **All claim-worthy confirmatory experiments executed** — COMPLETE:
   - FCLR-001 (2024 Q1): PILOT/INCONCLUSIVE (1 symbol, ~4 day test)
   - FCLR-003 (2024 Q4): NOT_SUPPORTED
   - FCLR-008 (unsealed 2024 Q4): directionally positive, inconclusive
   - **FCLR-009 (2025 full year, 5 symbols, 6 non-overlapping 30-day blocks): NOT_MET** — C2 vs B1 -0.43% QLIKE, CI crosses zero, << 2% floor
   - FCLR-011 (2026 Q3): NOT_SUPPORTED
   - FCLR-012-V (2026 forward, 5 days): INCONCLUSIVE/PILOT (0 30-day blocks)
   - FCLR-013 (2026 Q3): NOT_SUPPORTED
   - GATE4-FUND-VOL-ABLATIONS-MSPLIT-V3-30D (2024 Q2-Q3, 5 symbols, 4 non-overlapping 30-day blocks): INCONCLUSIVE, CI crosses zero
   - FCLR-H003-EXT-001 (Track B, unsealed 2026): NOT_SUPPORTED — no robust skill after Holm
4. **H002 Shek replication** — PARTIAL_REPLICATION (88 events, 5 symbols, p=0.079, direction reproduced, magnitude differs, paper methodology inaccessible).
5. **Track A liquidation source hunt** — EXHAUSTED (Hyperliquid-only, recent months absent, no unauthenticated source).
6. **Provenance-lineage ingestion (G3)** — COMPLETE (integrated, tested, evaluated = not machine-verifiable locally).
7. **Structural stop recorded with evidence** — CONFIRMED.

### Next focus campaign
**Campaign: FINAL SYNTHESIS & FORMAL CONCLUSION (local-only, no network, no outcomes, no new experiments).**
- **G1 (entry): GREEN** — dep-light 48/48, all structural stop evidence current.
- **G2 (synthesis): MANDATORY HEAVY WORK** — compile family-wide multiplicity correction, per-hypothesis verdicts, structural blockers, formal conclusion.
- **G3 (registry updates): MANDATORY** — hypothesis_registry.json final statuses, experiment_frontier.json CONCLUDED.
- **Exit:** Confirmatory program complete. Null results preserved. `next_unfinished_task: NONE` unless new admissible data source appears (network prohibited).

## 1) VERIFIED (2026-11-10T05:26:53Z)

| Check | Result |
|---|---|
| Dep-light gate | `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator tests.test_trackc_provenance_lineage -v` → **Ran 48 tests — OK** (core 39 + provenance lineage 9) |
| Deep audit 2024-10..12 | `research_state/trackc_deep_audit_orchestrator_latest.json` SHA256 `a28f952a…` (2026-11-10T05:21:41Z): `symbols_ok=0/5`, `panel_blocks_estimate=0`, `confirmatory_resume_ready=false`, `provenance_verified=false`, blockers: `REQUIRED_SERIES_GAPS_OR_MISSING`, `MISSING_FUNDING_MONTH_FILE`, `INSUFFICIENT_SYMBOLS_FOR_CONFIRMATORY`, `INSUFFICIENT_30D_BLOCKS_FOR_CONFIRMATORY`, `PROVENANCE_NOT_MACHINE_VERIFIED`, `CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES`, `CONFIRMATORY_REQUIRES_VERIFIED_PROVENANCE_CHECKSUMS` |
| Deep audit 2026-11 | `research_state/trackc_deep_audit_orchestrator_2026_11.json` SHA256 `40b4c3ae…` (2026-11-10T05:21:41Z): `symbols_ok=5/5`, `panel_blocks_estimate=0`, `confirmatory_resume_ready=false`, `provenance_verified=false`, blockers: `MISSING_FUNDING_MONTH_FILE`, `INSUFFICIENT_30D_BLOCKS_FOR_CONFIRMATORY`, `PROVENANCE_NOT_MACHINE_VERIFIED`, `CONFIRMATORY_REQUIRES_FROZEN_PREREG_BEFORE_OUTCOMES`, `CONFIRMATORY_REQUIRES_VERIFIED_PROVENANCE_CHECKSUMS` |
| Local provenance sidecars | Adjacent `*.sha256` under `research_state/data_cache/`: **0**. Manifest metadata present but cache files unmapped → no unambiguous lineage match. |
| FCLR-009 (widest claim-worthy panel) | `evaluation_summary_FCLR009.md`: C2 vs B1 = -0.43% QLIKE, 95% CI [-0.003120, 0.006165] crosses zero, 5 symbols, 6 non-overlapping 30-day blocks. **NOT_MET** (gate requires >=2% floor, CI support improvement, multiplicity pass). |
| GATE4 v3 30d (2024 Q2-Q3) | `evaluation_summary_funding_v3_30d.md`: Primary E vs A = +0.49%, 95% CI [-0.042, 1.197] crosses zero. **INCONCLUSIVE** (data-sufficient pilot, no skill). |
| FCLR-H003-EXT-001 (Track B) | `evaluation_summary_FCLR-H003-EXT-001.md`: After block bootstrap + LOO + Holm (m=16), **no cell significant**, C2 no robust skill over B0. **NOT_SUPPORTED**. |
| H002 Shek replication | `h002_replication_report.md`: 88 events, 5 symbols, high-RV median 16h vs low-RV 8h, log-rank p=0.079. **PARTIAL_REPLICATION** (direction reproduced, NOT significant, magnitude differs, paper methodology inaccessible). |
| Track A liquidation source | `experiment_frontier.json`, `liquidation_sources_enumeration.md`: **STRUCTURALLY BLOCKED** — Hyperliquid-only, 2026-11..2027-02 absent, no unauthenticated source. |
| Binding prereg skeletons | `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json` SHA256 `4adf609e…`, `protocol_FCLR-H003-EXT-001.md`, `h002_pre_registration.md` — all frozen BEFORE outcomes. |

**Admissibility conclusion:** CONFIRMATORY PROGRAM COMPLETE. All gates NOT_MET/EXHAUSTED. Null results preserved. No further confirmatory work possible without admissible external data (network prohibited). Next session: FINAL SYNTHESIS only.

## 2) KEY ARTIFACTS (paths/hashes as recorded)
- `scripts/trackc_panel_window_planner.py` `895b7abc…`, `tests/test_trackc_panel_window_planner.py` `e4fe0502…`, `research_state/trackc_panel_window_plan_latest.json` `3c2bae46…`
- `scripts/trackc_panel_deep_audit_orchestrator.py` `8500a773…`, `tests/test_trackc_panel_deep_audit_orchestrator.py` `ae45a716…`
- `scripts/trackc_provenance_lineage.py` `7236 bytes`, `tests/test_trackc_provenance_lineage.py` `fca4453b…` (9 tests)
- `scripts/trackc_panel_admissibility_audit.py` `45e2982c…`, `scripts/trackc_gap_repair_manifest.py` `51fd6b72…`, `scripts/trackc_funding_schema_audit.py` `78cbcd00…`
- `research_state/trackc_deep_audit_orchestrator_latest.json` `a28f952a…`, `research_state/trackc_deep_audit_orchestrator_2026_11.json` `40b4c3ae…`
- `research_state/evaluation_summary_FCLR009.md` (widest claim-worthy panel, NOT_MET)
- `research_state/evaluation_summary_funding_v3_30d.md` (GATE4 v3 30d, INCONCLUSIVE)
- `research_state/evaluation_summary_FCLR-H003-EXT-001.md` (Track B, NOT_SUPPORTED)
- `research_state/h002_replication_report.md` (PARTIAL_REPLICATION)
- `research_state/negative_results_report.md` (all null results preserved)
- `research_state/final_inconclusive_report.md` (FCLR-001 stop decision)
- `research_state/research_protocol.md` (FROZEN 2026-11-06T20:36:32Z)
- `research_state/hypothesis_registry.json` (H1_primary, H2_shek_replication — to be updated with final verdicts)

## 3) DO NOT DO
- ❌ Any new confirmatory experiment, forecast gate attempt, or risk overlay
- ❌ Threshold shopping; sealed-holdout reuse; protocol/estimand changes after seeing outcomes
- ❌ Track A probing/scans/wrappers/report families (structurally blocked)
- ❌ Conflate observed liquidations with modeled boundary breaches or correction time
- ❌ `.github/workflows` edits; schedulers/pollers/controllers
- ❌ Download/probe/network for missing files; bypass access controls
- ❌ Fabricate provenance/outcomes; relabel PARTIAL/INCONCLUSIVE as confirmatory
- ❌ Live/paper trading, order endpoints, credentials

## 4) SESSION START (mandatory)
1. Read this file + `RESEARCH_PROMPT.md`; `git status --short`.
2. Run dep-light gate (48/48) and record counts.
3. Confirm structural stop evidence current (re-run both scoped deep audits; confirm `confirmatory_resume_ready=false`, `provenance_verified=false`, `network_used=false`, `outcomes_computed=false`).
4. Execute FINAL SYNTHESIS CAMPAIGN (§0 item 3-5) — this is the ONLY remaining heavy work.
5. Update this file with exact evidence, hashes, commands, test counts, UTC timestamp, and `next_unfinished_task: NONE`.

---
**END OF SINGLE DURABLE HANDOFF. START AT §0 — FINAL SYNTHESIS HEAVY WORK REQUIRED.** All confirmatory tracks exhausted. Null results preserved. Structural stop final. `confirmatory_resume_ready=false`, `provenance_verified=false`. **Updated: 2026-11-10T05:26:53Z**