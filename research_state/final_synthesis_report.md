# Final Synthesis Report — Funding-conditioned Volatility and Liquidation Risk
**Generated (UTC):** 2026-11-10T07:15:52Z
**Scope:** Confirmatory program synthesis from repository evidence (no new experiments, no network, no outcomes recomputed).

## 1. Executive conclusion
The confirmatory research program for `Funding-conditioned-volatility-and-liquidation-risk` is **concluded under current constraints**. Across all pre-specified/admissible confirmatory evaluations executed in-repo, there is **no confirmatory evidence** that extreme funding conditions and pre-specified dislocation/smoothing features deliver robust out-of-sample improvement for volatility/liquidation-stress forecasting beyond baselines, and the secondary replication (Shek 2026) is partial and non-confirmatory. **Track A (observed liquidations)** remains structurally blocked due to lack of an admissible unauthenticated historical source in this environment. No risk overlay is eligible.

## 2. Structural stop / environment constraints (verified 2026-11-10)
- Dep-light reproducibility gate: **48/48 OK**
  `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_gap_repair_manifest tests.test_trackc_funding_schema_audit tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_contiguous_sequences tests.test_trackc_panel_window_planner.TestPanelWindowPlanner.test_cli_smoke tests.test_trackc_panel_deep_audit_orchestrator tests.test_trackc_provenance_lineage -v`
- Scoped deep audit (2024-10/11/12 hint): `confirmatory_resume_ready=false`, `provenance_verified=false`, `symbols_ok=0/5`, `panel_blocks_estimate=0`, `network_used=false`, `outcomes_computed=false`
  → `research_state/trackc_deep_audit_orchestrator_latest.json`
- Scoped deep audit (2026-11 hint): `confirmatory_resume_ready=false`, `provenance_verified=false`, `symbols_ok=5/5`, `panel_blocks_estimate=0`, `network_used=false`, `outcomes_computed=false` (missing funding month / insufficient blocks / provenance not machine-verified)
  → `research_state/trackc_deep_audit_orchestrator_2026_11.json`
- Hard constraints: no network/downloads, no paid/manual/credentialed data, no workflow/scheduler/poller additions, no fabricated provenance or outcomes, no threshold shopping or sealed-holdout reuse.

## 3. Family-wide multiplicity (evidence-based synthesis)
Multiplicity control was pre-specified at experiment level where applicable (e.g. Holm/Bonferroni in Track B extensions and confirmatory protocols). A family-wide view across the full confirmatory program shows no surviving confirmatory positive:

| Hypothesis / Track | Evidence family (from repo artifacts) | Nominal highlights | Multiplicity-adjusted outcome | Family verdict |
|---|---|---|---|---|
| **H001 / Track C** (funding-conditioned volatility) | 8+ confirmatory/claim-worthy panels/experiments (FCLR-001, 003, 008, 009, 011, 012-V, 013, GATE4 v3 30d), multiple primary contrasts each (≥24+ contrasts total) | Best reported C2 vs B1 = **-0.43% QLIKE** (FCLR-009, 95% CI crosses zero, below 2% floor); GATE4 v3 30d primary **+0.49%**, CI crosses zero | No contrast meets pre-specified improvement floor with robust CI/multiplicity support across blocks/symbols; no confirmatory gate passed | **NOT_SUPPORTED** |
| **H002** (Shek 2026 replication) | 1 replication study | Direction reproduced (high-RV 16h > low-RV 8h) but **p=0.079** (not significant), magnitude differs (paper 27h/3h vs reconstructed 16h/8h), smaller universe (5 vs 18), methodology not fully accessible | Not significant at conventional thresholds; cannot claim exact/confirmatory replication | **PARTIAL_REPLICATION (non-confirmatory)** |
| **H003 / Track B** (boundary breaches, modeled) | 16 cells × 2 horizons (32 tests) in FCLR-H003-EXT-001; baseline H003 variants | No robust predictive skill | **No cells survive Holm correction** (and baseline non-robust) | **NOT_SUPPORTED** |
| **Track A** (observed liquidations) | Source enumeration/probing campaign (Hyperliquid-focused), no admissible unauthenticated historical coverage for required window | N/A (no admissible outcome labels) | N/A | **STRUCTURALLY_BLOCKED** |

**Multiplicity conclusion:** Even before aggressive family-wise pooling, no primary confirmatory contrast demonstrates robust, practically meaningful OOS improvement; adjusted results (where computed, notably H003 Holm) are null. Family-wide confirmatory claim: **rejected / unsupported**.

## 4. Per-hypothesis verdicts and evidence
### H001 — Primary (funding extremes + RV + dislocation improve OOS volatility/stress forecast)
- **Verdict:** **NOT_SUPPORTED**
- **Key artifacts:** `research_state/evaluation_summary_FCLR009.md` (widest panel, NOT_MET), `research_state/evaluation_summary_funding_v3_30d.md` (INCONCLUSIVE), `research_state/evaluation_summary.md`, `research_state/negative_results_report.md`, confirmatory preregs (e.g. `research_state/pre_registration_fclr014_confirmatory_funding_vol_20261109T181124Z.json`, GATE4 v3/v4 materials in `research_state/`).
- **Interpretation:** Incremental funding/dislocation features do not provide confirmatory, generalizable OOS gains vs RV-only baselines under frozen protocols.

### H002 — Secondary (Shek 2026 funding-correction pattern replication)
- **Verdict:** **PARTIAL_REPLICATION (non-confirmatory)**
- **Key artifact:** `research_state/h002_replication_report.md`
- **Evidence:** Directional pattern present (high-RV correction slower: 16h vs 8h) but **p=0.079**, magnitudes differ from paper (27h/3h), universe smaller (5 vs 18), full methodology inaccessible; replication partial by necessity.

### H003 / Track B — Modeled boundary-breach predictability
- **Verdict:** **NOT_SUPPORTED**
- **Key artifacts:** `research_state/evaluation_summary_FCLR-H003-EXT-001.md`, `research_state/evaluation_summary_h003.md`, `research_state/evaluation_summary_h003_FCLR002.md`
- **Interpretation:** Modeled/synthetic breach proxies show no robust out-of-sample skill after multiplicity control. **Observed liquidations were not forecast and must not be conflated with Track B.**

### Track A — Observed liquidation labels/outcomes
- **Verdict:** **STRUCTURALLY_BLOCKED**
- **Key artifacts:** `research_state/liquidation_sources_enumeration.md`, `research_state/experiment_frontier.json`, Track A blocker/probe histories in `research_state/`
- **Interpretation:** No admissible unauthenticated historical liquidation source with required coverage (notably 2026-11..2027-02 context per frontier history; Hyperliquid-only constraints in prior campaigns). Cannot be repaired locally without prohibited network/paid/manual access.

## 5. Provenance, data, and integrity notes
- Local cached market/funding artifacts exist under `research_state/data_cache/` and root zip/csv extracts, but provenance is **not machine-verified end-to-end** (0 adjacent `*.sha256` sidecars; manifests present but unmapped per deep-audit lineage blockers).
- Deep audits report **no outcomes computed** and **no network used**; confirmatory resume prerequisites unmet (frozen prereg-before-outcomes + verified provenance + sufficient contiguous blocks/symbols).
- Null/inconclusive results preserved across `research_state/evaluation_summary*.md` and `research_state/negative_results_report.md`.

## 6. Formal closure statement
- **Confirmatory program status:** **COMPLETE / CONCLUDED** for claims testable with admissible in-repo data under current constraints.
- **Risk overlay eligibility:** **NOT ELIGIBLE** (no passed out-of-sample forecasting gate).
- **Track separation:** Observed liquidations (Track A, blocked) ≠ modeled boundary breaches (Track B, null) ≠ volatility/stress forecasts (Track C, null/inconclusive).
- **Future work (only if environment changes):** Requires **new admissible unauthenticated data source(s)** with verifiable provenance and sufficient coverage (especially for Track A historical observed liquidations and/or confirmatory Track C panel repair). In this environment, network/downloads/credentials/paid data remain prohibited.

## 7. Artifact index (primary)
- Handoff/protocol: `AGENT_HANDOFF.md`, `RESEARCH_PROMPT.md`, `research_state/research_protocol.md`
- Registries/frontier: `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`
- Stop evidence: `research_state/trackc_deep_audit_orchestrator_latest.json`, `research_state/trackc_deep_audit_orchestrator_2026_11.json`
- Core results: `research_state/evaluation_summary_FCLR009.md`, `research_state/evaluation_summary_funding_v3_30d.md`, `research_state/evaluation_summary_FCLR-H003-EXT-001.md`, `research_state/h002_replication_report.md`, `research_state/negative_results_report.md`
- Track A: `research_state/liquidation_sources_enumeration.md`
