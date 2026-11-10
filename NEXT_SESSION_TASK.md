# NEXT_SESSION_TASK.md — SINGLE DURABLE HANDOFF (INITIAL TASK MESSAGE)

**Timestamp (UTC):** 2026-11-10T20:00:21Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Program status:** `CONCLUDED_UNDER_CONSTRAINTS` — all admissible local routes exhausted with evidence. **This session's mandatory work is COMPLETE; no further initial task remains on the current frozen design.**

## STATUS — TRACK B TB2 CONFIRMATORY COMPLETE (verdict NOT_SUPPORTED)

Executed **Track B TB2 confirmatory evaluation** on the frozen local panel **2024-01-01..2024-09-30** (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT), label `synthetic_boundary_breach_h168_long_10x_m0` (leverage=10.0, side=long, mmr=0.0, horizon=168h).

**Step 0 — prereg freeze-integrity blocker: RESOLVED.** Manifest `prereg_hash` corrected to canonical protocol-file sha256 `46dcfb56c279e853230e75f6cb246ed878d765d2b399ea9a2e21c41581194adb` (prior `9de16e7d...` did not match the file; corrected before any outcome computation). `frozen_before_outcomes=true`, `outcome_values_inspected=false`. Provenance `PROVENANCE_OK 161`, unmapped 0. Documented in `research_state/run_manifest.json#split_boundaries_trackb_TB2_20261110T190405Z` (prereg_integrity_resolution) and `#tb2_confirmatory_run`.

**Step 1 — confirmatory evaluation: COMPLETE.** Pipeline `scripts/run_trackb_tb2_evaluation.py` implements the frozen protocol (B1 RV-only vs C2 funding-conditioned; Log Loss + Brier; training-only standardization; missing remains missing; block bootstrap 2000 reps / 30-day blocks; Holm across 2 metrics; >=2% Log-Loss materiality). Output: `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md`.

**Verdict: FORECAST_GATE_NOT_MET / NOT_SUPPORTED.**
- Event-adequate: test 619/5040 positives (12.3%), all 5 symbols >0 (matches pre-freeze scan).
- Pooled Log Loss B1=0.292447 → C2=0.287540 = **+1.68% relative reduction (<2% floor, NOT_MET)**.
- 95% CI for paired Log Loss diff [-0.010997, 0.003094] crosses zero (NOT_MET); p=0.488; Holm FAILS.
- Only 2 non-overlapping 30-day test blocks (<3 required, NOT_MET); >=5 instruments PASS (5).
- **C2 funding-conditioned model shows no established incremental forecast skill over B1 RV-only baseline. Overlay NOT ELIGIBLE. Null result preserved; no threshold shopping; no sealed-holdout reuse.**

## ALL ADMISSIBLE LOCAL ROUTES EXHAUSTED
- **Track A (observed liquidations):** STRUCTURALLY_BLOCKED — no admissible unauthenticated observed-liquidation census. Not locally repairable.
- **Track C / H1:** concluded NOT_SUPPORTED (all claim-worthy local panels: FCLR-003/008/009/012-V/013/014). Overlay INELIGIBLE.
- **Track B:** TB1 degenerate/inadmissible (0 test breaches); TB2 confirmatory gate NOT_MET (this session). No uninspected admissible local route remains.

## SINGULAR NEXT TASK
**NONE — program concluded under constraints pending a new admissible unauthenticated source.**
A future session may reopen only with: (a) a new admissible unauthenticated data source, (b) a new experiment ID, and (c) a new prereg frozen **before** any outcome computation. Do not poll, do not relitigate concluded tracks, do not produce status-only output, do not threshold-shop, do not reuse sealed holdouts.

## Hard constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled breach proxy only, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits.

## Verification commands (still green)
```bash
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"
```
