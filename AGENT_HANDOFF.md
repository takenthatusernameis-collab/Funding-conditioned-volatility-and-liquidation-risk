# AGENT_HANDOFF.md — Single Durable Handoff (REPO-NAME PRIORITY: liquidation risk Track B first, then volatility Track C; Track A observed liquidations STRUCTURALLY_BLOCKED)

**Updated:** 2026-11-10T18:05:00Z — **SINGLE DURABLE HANDOFF (PROGRAM NOT CONCLUDED).** TB1 (2025-01-01..2026-10-31, 5 symbols, 22 est. 30d blocks) **executed but DEGENERATE**: frozen test split 2026-06-26..2026-10-31 has ZERO synthetic boundary breaches across all 5 symbols (5x/24h long). Gate NOT_MET — test set inadmissible for confirmatory evaluation with this label definition. Track C H1_primary NOT_SUPPORTED (claim-worthy panels exhausted); Track A STRUCTURALLY_BLOCKED; risk overlay INELIGIBLE. Provenance `PROVENANCE_OK 161`.

**Session preflight (last verified 2026-11-10T18:05:00Z):** `PROVENANCE_OK 161` (funding CSV lineage, unmapped=0). TB1 evaluation complete with explicit degenerate-test-set finding. Remaining local Track B routes: (1) 2024-01-01..2024-09-30 panel (~9 est. blocks) requires deep re-audit + NEW frozen prereg + confirmatory; (2) redesign label + select window with events + NEW frozen prereg + confirmatory. No network/paid/manual/credentialed data required.

**Correction vs prior handoff:** The TB1 window (2025-01-01..2026-10-31) was admissibility-verified but the frozen test split produces zero events for the 5x/24h long label. Full-window breach rates: ETH 0.166%, XRP 0.303%, others <0.06%. This is a label/window mismatch, not a data issue. The prior experiment TRACKB-20251110T154307Z (2025-01-01..2025-10-31) also NOT_MET (1.50% < 2%, CI crosses zero).

---

## 🔴 INITIAL TASK MESSAGE FOR NEXT AGENTIC SESSION — 2026-11-10T18:05:00Z (supersedes prior; see NEXT_SESSION_TASK.md)

**Campaign:** `TRACKB-MODELED-BREACH-TB1-20261110T173838Z` — Track B modeled liquidation boundary-breach confirmatory (repo-name priority #1). **TB1 EXECUTED: DEGENERATE TEST SET (zero events).** M5.3 complete with explicit finding; M5.4 verdict propagated. Next: M5 repeat on admissible route.

**Completed (verified):**
- Admissibility: `research_state/trackb_TB1_admissibility.json` (2025-01-01..2026-10-31, 5 symbols, contiguous, 22 est. 30d blocks, provenance OK).
- Freeze-before-outcomes: `research_state/research_protocol_trackb_TB1_20261110T173838Z.md`; `run_manifest.json` `split_boundaries_trackb_TB1_20261110T173838Z` `frozen_before_outcomes=true`, `prereg_hash=5e075968e5958471530d0618cdba1410f8fb3d5afdb31c3be13f99aa07d27c92`.
- **Execution (M5.3):** `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md` — frozen test split 2026-06-26..2026-10-31 has ZERO synthetic breaches (5x/24h long) across all 5 symbols. Classification degenerate. Gate NOT_MET.
- **Verdict & propagation (M5.4):** hypothesis_registry, experiment_frontier, negative_results_report updated. Track B status: `PARTIALLY_TESTED_TB1_DEGENERATE_FALLBACK_REQUIRES_REAUDIT`.

**Mandatory next (in order, non-optional):**
- **M5 repeat on next admissible route:** Choose ONE:
  1. **Deep re-audit 2024-01-01..2024-09-30 panel** (~9 est. blocks, completeness 1.0 in `trackb_window_candidates_fast.json`): run full admissibility + gap + funding-schema audit + provenance lineage → if admissible, freeze NEW prereg (new ID) → execute confirmatory.
  2. **Redesign label + select test window with events**: e.g., leverage=10x or 20x, or short side, or longer horizon; pick a test window (from full-window breach audit above) that has >0 events. Freeze NEW prereg → execute confirmatory.
- **No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation; no `.github/workflows` edits.**

**Current `next_unfinished_task`:** Track B — TB1 window INADMISSIBLE (zero test events with 5x/24h long). Options: (1) Deep re-audit 2024-01-01..2024-09-30 panel + NEW frozen prereg + confirmatory execution; (2) Redesign label (leverage/horizon/side) + select test window with events + NEW frozen prereg + confirmatory execution. Track C concluded NOT_SUPPORTED. Track A STRUCTURALLY_BLOCKED. Risk overlay INELIGIBLE.

**Verification commands:**
- `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v`
- Provenance: `python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"`
- Check breach rates by window: `python -c "from scripts.synthetic_boundary_labels import synthetic_boundary_label; ...` (see evaluation_summary for full-window rates)