# AGENT_HANDOFF.md — Single Durable Handoff (next session MUST continue from here)

**Updated:** 2026-11-10T05:33:09Z — **P0 = FINAL SYNTHESIS & FORMAL CONCLUSION CAMPAIGN (HEAVY WORK, UNAVOIDABLE).**
**Repo priority (from name `Funding-conditioned-volatility-and-liquidation-risk`):** Funding-conditioned volatility + liquidation risk — all three tracks (A liquidation labels, B boundary breaches, C volatility forecasting) have been exhaustively investigated with no admissible confirmatory evidence. Structural stop is final under current constraints (no network, no paid data, no manual inputs). Next session **MUST** produce a complete, auditable synthesis.

## 0) INITIAL TASK MESSAGE — 2026-11-10T05:33:09Z — MANDATORY HEAVY WORK (NEXT SESSION, CANNOT BE AVOIDED)

**START HERE. DO NOT restart experiments. DO NOT scan for new data. DO NOT probe liquidation sources.**

All confirmatory gates are exhausted or structurally blocked:
- **Track C (H001, funding-conditioned volatility):** NOT_SUPPORTED across 7+ claim-worthy panels (FCLR-001, 003, 008, 009, 011, 012-V, 013, GATE4 v3 30d). Best C2 vs B1 = **-0.43% QLIKE** (FCLR-009, 95% CI crosses zero, << 2% floor). Multiplicity not passed.
- **Track B (H003, boundary breaches):** NOT_SUPPORTED (FCLR-H003-EXT-001). No robust skill after Holm correction across tested cells/horizons.
- **H002 (Shek 2026 replication):** PARTIAL_REPLICATION — direction reproduced (high-RV 16h > low-RV 8h) but **not significant (p=0.079)**, magnitude differs (paper 27h/3h vs reconstructed 16h/8h), smaller universe (5 vs 18), paper methodology inaccessible.
- **Track A (observed liquidations):** STRUCTURALLY BLOCKED — no admissible unauthenticated source (Hyperliquid-only; required history 2026-11..2027-02 absent). Cannot be repaired locally.

**Bottlenecks already removed:** scoped deep audits (`--window-hint`) avoid full-cache scans; provenance-lineage integrated and tested (48/48 dep-light). Remaining structural blockers are unrepairable without admissible external data (network prohibited).

### Do in order (heavy, auditable work)

1. **Dep-light gate (record exact):**
   ```bash
   python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator tests.test_trackc_provenance_lineage -v
   ```
   → expect **48/48 OK**.

2. **Confirm structural stop (evidence):**
   ```bash
   python scripts/trackc_panel_deep_audit_orchestrator.py --cache research_state/data_cache --repo-root . --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --window-hint 2024_10,2024_11,2024_12 --min-symbols 5 --min-blocks 3 --out research_state/trackc_deep_audit_orchestrator_latest.json
   python scripts/trackc_panel_deep_audit_orchestrator.py --cache research_state/data_cache --repo-root . --symbols BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT --window-hint 2026_11 --min-symbols 5 --min-blocks 3 --out research_state/trackc_deep_audit_orchestrator_2026_11.json
   ```
   Both must show `confirmatory_resume_ready=false`, `provenance_verified=false`, `network_used=false`, `outcomes_computed=false`.

3. **FINAL SYNTHESIS (MANDATORY HEAVY WORK):** Create/update `research_state/final_synthesis_report.md` with:
   - **Family-wide multiplicity:** Holm/Bonferroni across ALL tested contrasts (H001: 8 experiments × 3+ primary contrasts = 24+; H002: 1; H003: 16×2 = 32). Report raw and adjusted p-values/CIs.
   - **Per-hypothesis verdicts:** H001 NOT_SUPPORTED; H002 PARTIAL_REPLICATION (p=0.079, direction only, magnitude differs, methodology inaccessible); H003 NOT_SUPPORTED; Track A STRUCTURALLY_BLOCKED.
   - **Blockers & provenance:** Document structural blockers (no network/paid/manual), local gaps (2024-10/11/12 series, 2026-11 funding), provenance not machine-verifiable (0 adjacent sha256 sidecars).
   - **Formal conclusion:** Confirmatory program complete. Null results preserved. No risk overlay eligible. Future work requires new admissible unauthenticated data source(s).

4. **Update registries:** Update `research_state/hypothesis_registry.json` (H1_primary/H2_shek_replication final verdicts + evidence). Add/update `research_state/experiment_frontier.json` to mark all confirmatory tracks CONCLUDED/EXHAUSTED with `next_action: "requires_new_admissible_data_source"`.

5. **Finalize handoff:** Update this file with UTC timestamp, exact commands, test counts, artifact paths+hashes. Set `next_unfinished_task: "NONE — CONFIRMATORY PROGRAM CONCLUDED. Future sessions only if new admissible unauthenticated data source becomes available (network prohibited in this environment)."`

### Hard constraints
- No new confirmatory experiments, threshold shopping, sealed-holdout reuse, prereg/estimand changes after outcomes.
- No Track A probing/scans/wrappers/report families (structurally blocked).
- Never conflate observed liquidations with modeled/synthetic boundary breaches or correction time.
- No `.github/workflows` edits; no schedulers/pollers/controllers; no credentials/paid data/access-control bypass; no network/downloads; no live/paper trading.
- No fabricated provenance/outcomes; do not relabel PARTIAL/INCONCLUSIVE as confirmatory.

### Bottleneck status
- **B1 (full-cache scan timeout): REMOVED** — scoped orchestrator in place.
- **B2 (2026-11 funding month missing, all 5 symbols): STRUCTURAL** — not repairable locally (no network).
- **B3 (2024-10/11/12 series gaps): STRUCTURAL** for those windows.
- **B4 (provenance): NOT machine-verifiable locally** — 0 adjacent `*.sha256` sidecars; manifests present but unmapped; no fabrication.

### Completed heavy work (evidence — FINAL STATE)
1. Track C reproducibility + audit hardening (48/48, scoped audits, provenance lineage integrated/tested)
2. Frozen confirmatory preregs (FCLR-009, FCLR-014, FCLR-H003-EXT-001, GATE4 v3/v4) before outcomes
3. All claim-worthy confirmatory experiments executed (FCLR-001/003/008/009/011/012-V/013, GATE4 v3 30d) — all null/inconclusive/not_met
4. H002 Shek replication — PARTIAL_REPLICATION (p=0.079)
5. Track A liquidation source hunt — EXHAUSTED/STRUCTURALLY BLOCKED
6. Structural stop recorded with evidence

## 1) VERIFIED (2026-11-10T05:33:09Z)

| Check | Result |
|---|---|
| Dep-light gate | `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator tests.test_trackc_provenance_lineage -v` → **Ran 48 tests — OK** (core 39 + provenance lineage 9) |
| Deep audit 2024-10..12 | `research_state/trackc_deep_audit_orchestrator_latest.json`: `symbols_ok=0/5`, `panel_blocks_estimate=0`, `confirmatory_resume_ready=false`, `provenance_verified=false`, blockers include gaps/funding missing/provenance not verified |
| Deep audit 2026-11 | `research_state/trackc_deep_audit_orchestrator_2026_11.json`: `symbols_ok=5/5`, `panel_blocks_estimate=0`, `confirmatory_resume_ready=false`, `provenance_verified=false`, blockers include funding missing/provenance not verified/insufficient blocks |
| FCLR-009 (widest) | `evaluation_summary_FCLR009.md`: C2 vs B1 = -0.43% QLIKE, 95% CI crosses zero, 6 non-overlapping 30d blocks, 5 symbols — **NOT_MET** |
| GATE4 v3 30d | `evaluation_summary_funding_v3_30d.md`: primary +0.49%, CI crosses zero — **INCONCLUSIVE** |
| FCLR-H003-EXT-001 | `evaluation_summary_FCLR-H003-EXT-001.md`: no robust skill after Holm — **NOT_SUPPORTED** |
| H002 | `h002_replication_report.md`: p=0.079, direction only — **PARTIAL_REPLICATION** |
| Track A | `liquidation_sources_enumeration.md` / `experiment_frontier.json`: **STRUCTURALLY BLOCKED** |

**Conclusion:** CONFIRMATORY PROGRAM COMPLETE. Null results preserved. No further confirmatory work possible without admissible external data (network prohibited).

## 2) KEY ARTIFACTS
- `scripts/trackc_panel_deep_audit_orchestrator.py`, `scripts/trackc_provenance_lineage.py`, `scripts/trackc_panel_window_planner.py`
- `research_state/trackc_deep_audit_orchestrator_latest.json`, `research_state/trackc_deep_audit_orchestrator_2026_11.json`
- `research_state/evaluation_summary_FCLR009.md`, `research_state/evaluation_summary_funding_v3_30d.md`, `research_state/evaluation_summary_FCLR-H003-EXT-001.md`
- `research_state/h002_replication_report.md`, `research_state/negative_results_report.md`, `research_state/research_protocol.md` (frozen)
- `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`
- `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`

## 3) DO NOT DO
- Any new confirmatory experiment/forecast gate/risk overlay
- Threshold shopping; sealed-holdout reuse; protocol/estimand changes after outcomes
- Track A probing/scans/wrappers (structurally blocked)
- Conflate observed liquidations with modeled/synthetic boundary breaches/correction time
- `.github/workflows` edits; schedulers/pollers/controllers; credentials/paid data/bypass; network/downloads; live/paper trading
- Fabricate provenance/outcomes; relabel PARTIAL/INCONCLUSIVE as confirmatory

## 4) SESSION START (MANDATORY)
1. Read `RESEARCH_PROMPT.md` + this file; `git status --short`
2. Run dep-light gate (48/48), record counts
3. Confirm structural stop evidence (both scoped deep audits) — must be `confirmatory_resume_ready=false`
4. **Execute FINAL SYNTHESIS CAMPAIGN (§0)** — create/update `final_synthesis_report.md`, update registries/frontier
5. Update this file with exact evidence/hashes/commands/timestamp and set `next_unfinished_task: NONE`

---
**END OF SINGLE DURABLE HANDOFF. START AT §0 — FINAL SYNTHESIS HEAVY WORK REQUIRED.**
**Updated: 2026-11-10T05:33:09Z**
