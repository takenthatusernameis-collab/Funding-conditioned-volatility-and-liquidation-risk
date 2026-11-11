# HANDOFF — Funding-conditioned-volatility-and-liquidation-risk
**Single durable handoff / initial task message for next agentic work session**
**Timestamp (UTC):** 2026-11-11T07:30:00Z
**Repo:** `/home/runner/work/Funding-conditioned-volatility-and-liquidation-risk/Funding-conditioned-volatility-and-liquidation-risk`

## Repo-priority state (evidence-backed, do not relitigate)
- **Track A — Observed liquidations (repo-name priority): UNBLOCKED_GO_SOURCE.** `ironflow/hyperliquid-liquidations` adjudicated GO per Phase 3 rubric (CC BY 4.0, unauthenticated HF bulk parquet, no requester-pays, complete months 2025-06..2026-10 with 164–353 *-PERP markets/month, schema mappable to FCLR-010/H004, provenance in-repo). New experiment `TRACKA-HL-20261111T073000Z` preregistered pre-outcomes at `research_state/tracka_prereg_hyperliquid_2026.json`. Split boundaries frozen in `research_state/run_manifest.json`. Hyperliquid-native only; no Binance/2024 conflation; no sealed-holdout reuse.
- **Track B — Modeled breach proxy:** CONFIRMATORY_COMPLETE, NOT_SUPPORTED (TB1 degenerate/zero test breaches; TB2 gate NOT_MET: LogLoss B1=0.292447→C2=0.287540 +1.68% <2%, 95% CI crosses zero, Holm fails, 2 test blocks <3). Not observed liquidations. `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`.
- **Track C/H1 — Funding-conditioned volatility:** NOT_SUPPORTED on all claim-worthy local panels (FCLR-003/008/009/012-V/013/014). `research_state/final_confirmatory_verdict.md`, `research_state/hypothesis_registry.json`.
- **Program:** `ACTIVE` (Track A unblocked by ironflow GO). Last recorded verification green: scope registry 127/127 pass, provenance 161/161 verified unmapped_count=0, targeted tests 35/35 OK.

## Singular next task — TRACKA-HL Phase 4 (heavy, execute immediately)
Objective: build aligned Hyperliquid liquidation + market/funding/price panel from admissible unauthenticated sources, run pre-registered evaluation per `research_state/tracka_prereg_hyperliquid_2026.json`, produce auditable verdict artifact.

### Immediate steps (in order)
1. **Verify prereg freeze is intact** — confirm `research_state/tracka_prereg_hyperliquid_2026.json` and `research_state/run_manifest.json#TRACKA-HL-20261111T073000Z` split boundaries are unchanged and `frozen_before_outcomes: true`. Do NOT inspect outcomes before this check.
2. **Build aligned analysis panel** — ironflow observed liquidation events (2025-06..2026-10) + compatible Hyperliquid market/funding/price context from admissible unauthenticated sources, with provenance (URL, access date, hash/ETag, terms). If alignment data is inadmissible, document the blocker in `research_state/tracka_hl_alignment_blocker.md` and stop cleanly — do not fabricate.
3. **Run pre-registered evaluation** — leakage/split/integrity checks per prereg; QLIKE on observed liquidation intensity; primary contrast C2 vs B1; materiality gate: ≥2% relative reduction, 95% CI excludes zero, ≥5 paired instruments, ≥3 non-overlapping 30-day test blocks.
4. **Atomically update state** — `research_state/experiment_frontier.json`, `research_state/hypothesis_registry.json` (H_tracka_hl_liquidation_forecast), `research_state/run_manifest.json` (TRACKA-HL entry). Write verdict artifact `research_state/evaluation_summary_TRACKA-HL-20261111T073000Z.md`.

### Forbidden
No threshold-shopping on test set; no sealed-holdout reuse (FCLR-002/FCLR-003/Track B/C test sets sealed); no Binance/2024 conflation (Hyperliquid only, 2025-06..2026-10 panel); no modeled/proxy/synthetic liquidation labels (observed ironflow events only); no outcome inspection before prereg freeze; no risk overlay before forecast gate met; no network polling or redundant GETs beyond cached provenance; no `.github/workflows` edits; no status-only output.

### Canonical artifacts
`HANDOFF_NEXT_SESSION.md` (this file), `NEXT_SESSION_TASK.md`, `FOCUS_CAMPAIGN.md`, `AGENT_HANDOFF.md`, `research_state/experiment_frontier.json`, `research_state/final_confirmatory_verdict.md`, `research_state/hypothesis_registry.json`, `research_state/run_manifest.json`, `research_state/data_source_registry_alt_hunt.json`, `research_state/tracka_prereg_hyperliquid_2026.json`, `research_state/ironflow_probe_20261111T015524Z.json`, `research_state/ironflow_probe_digest_latest.json`, `research_state/ironflow_monitor_state.json`.

## Verification checklist (run before/after substantive changes)
- `python scripts/check_tracka_scope_registry_drift.py --json` (pass True)
- provenance check: `python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"`
- `python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v`
