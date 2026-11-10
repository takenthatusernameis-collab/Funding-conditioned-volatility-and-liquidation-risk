# NEXT_SESSION_TASK.md — SINGLE DURABLE HANDOFF (INITIAL TASK MESSAGE)

**Timestamp (UTC):** 2026-11-10T19:45:07Z
**Repo:** `Funding-conditioned-volatility-and-liquidation-risk`
**Program status:** `ACTIVE_TRACKB_MANDATORY` — NOT concluded. **This is the single authoritative initial task message for the next agentic session. Execute it before any other work.** Do not relitigate concluded tracks, do not poll, and do not produce status-only output.

## IMMEDIATE MANDATORY TASK (heavy, verifiable — start now)

Execute **Track B TB2 confirmatory evaluation** on the frozen local panel **2024-01-01..2024-09-30** (BTCUSDT/ETHUSDT/BNBUSDT/SOLUSDT/XRPUSDT). **TB1 is DEGENERATE/INADMISSIBLE** (frozen test 2026-06-26..2026-10-31 had 0 synthetic breaches at 5x/24h long; `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`) — **do not rerun TB1 unchanged**.

### Frozen pre-conditions (must be satisfied/verified before outcomes)
- **Admissibility/provenance:** `research_state/trackb_TB2_admissibility.json` + `_2024q1q3.json` (5 symbols, 274 days, >=3 test blocks, `required_series_complete`, `provenance_verified=true`, `unmapped_count=0`). Re-verify provenance for all TB2 inputs at confirmatory run (funding cache provenance currently `PROVENANCE_OK 161`, unmapped 0).
- **Event-adequate design (pre-freeze, >0 frozen-test positives):** `synthetic_boundary_breach_h168_long_10x_m0` (leverage=10.0, side=long, maintenance_margin_rate=0.0, horizon=168h). Test: 619/4925 positives (12.6%), all 5 symbols >0. Evidence: `research_state/trackb_TB2_label_design_scan.json`. **No threshold shopping after freeze.**
- **Prereg/splits (freeze-before-outcomes):** `research_state/research_protocol_trackb_TB2_20261110T190405Z.md` + `split_boundaries_trackb_TB2_20261110T190405Z` in `research_state/run_manifest.json` (train `2024-01-01T00:00:00Z..2024-06-12T00:00:00Z` / val `2024-06-19T00:00:00Z..2024-08-06T00:00:00Z` / test `2024-08-13T00:00:00Z..2024-09-30T00:00:00Z`, 7-day purge/embargo). **Integrity blocker (must resolve first):** current `sha256(protocol file)=46dcfb56c279e853230e75f6cb246ed878d765d2b399ea9a2e21c41581194adb` but manifest records `prereg_hash=9de16e7d2b2c80f6ac57d87b6eb150c145bfe9f3168d7ac3d94472f740f7b91f` (mismatch). **Do not compute confirmatory outcomes until freeze integrity is unambiguous:** determine canonical hash (and when text last changed), then reconcile transparently by either (a) correcting manifest hash with evidence that content predates outcomes, or (b) issuing a new frozen prereg version (new ID/hash recorded before outcomes) preserving the same defensible design. Document the resolution in `run_manifest.json`/evaluation summary.
- **Data:** required series (markPriceKlines, indexPriceKlines, premiumIndexKlines 1h; fundingRate 8h) for all 5 symbols in `research_state/data_cache` with adjacent sha256 sidecars.

**Objective:** produce a preregistered, leakage-resistant Track B verdict (or evidence-backed inadmissibility) using **modeled synthetic boundary breaches only** (never observed liquidations). Report counts per split/symbol/overall with rationale.

## Execution steps (complete in order; heavy work only)

### 0) Resolve prereg freeze-integrity blocker (mandatory, before outcomes)
- Reconcile the protocol/manifest hash mismatch with auditable evidence. Ensure `prereg_hash`, `frozen_before_outcomes`, and `outcome_values_inspected=false` are consistent and recorded **before** any confirmatory outcome computation. If a new freeze is required, use a new experiment/protocol ID and update refs; do not alter past results.

### 1) Run confirmatory evaluation on frozen TB2 panel (heavy)
- Implement/adapt and execute the Track B pipeline for TB2 (reference: `scripts/run_trackb_evaluation.py`, `scripts/synthetic_boundary_labels.py`) on the frozen splits/config. **No post-freeze tuning/threshold shopping. No holdout reuse for selection.**
- **Configuration (must match frozen prereg):**
  - Window: `2024-01-01T00:00:00Z .. 2024-09-30T23:00:00Z`; Symbols: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT
  - Label: `synthetic_boundary_breach_h168_long_10x_m0` (leverage=10.0, side=long, mmr=0.0, horizon=168h; labels use mark-closes strictly after t: t+1..t+168h)
  - Predictors (causal, **training-only** normalization/fitting): **B1** (price/RV-only) = trailing RV1h/RV24h/RV168h from mark-price log returns; **C2** (funding-conditioned) = B1 + signed funding rate + abs funding percentile (prior 90d, >=30 obs) + mark/index premium + mark/EMA24 distance. Missing features remain missing.
  - Primary contrast/metrics: C2 vs B1 on **Log Loss** and **Brier score** (lower better), per-symbol and pooled. Materiality floor: **>=2% relative reduction in Log Loss vs B1**.
  - Uncertainty/multiplicity: block bootstrap **>=2000 deterministic-seed replicates**, block size **30 days (720h)**, resampling complete UTC blocks; two-sided **95% CI** for paired loss difference (must exclude null in favorable direction). **Holm correction** across the 2 pre-specified metrics (alpha=0.025/metric).
- **Outputs:** `research_state/evaluation_summary_trackb_TB2_20261110T190405Z.md` (or successor ID if refrozen) with point estimates (B1/C2), paired deltas, 95% CIs, relative change, n_instruments, n_obs (train/val/test), n_test_blocks, per-split/symbol/overall breach counts, materiality/Holm/gate decision, and caveat `synthetic proxy ≠ observed liquidations; no risk overlay until gate passes`. Update `research_state/run_manifest.json` with run record (git SHA, timestamps, config, data hashes/refs, status).

### 2) Propagate verdict and set singular next task
- Update `research_state/hypothesis_registry.json`, `research_state/experiment_frontier.json`, `research_state/negative_results_report.md`, `AGENT_HANDOFF.md`, and this file with the timestamped outcome.
- State overlay eligibility (**NOT ELIGIBLE unless all forecast gates pass** under frozen prereg).
- Set exactly one singular, evidence-backed `next_unfinished_task`: gate pass → preregister next confirmatory/overlay-eligibility step (no premature overlay). Gate NOT_MET/NOT_SUPPORTED → if all admissible local routes exhausted with evidence: `NONE — program concluded under constraints pending new admissible unauthenticated source` (Track A STRUCTURALLY_BLOCKED, Track C concluded); else define single next admissible uninspected route (new ID, new prereg, freeze before outcomes).

## Fallback (only with evidence)
If 2024-01-01..2024-09-30 is proven inadmissible (cannot achieve >0 frozen-test breaches under frozen defensible design, or provenance/schema/coverage fails): document evidence-backed inadmissibility and immediately pivot to the next locally admissible uninspected route with new ID and new prereg (do not stop at planning). **Track C concluded NOT_SUPPORTED. Track A STRUCTURALLY_BLOCKED. Overlay INELIGIBLE.**

## Acceptance (incomplete without all)
- Freeze-integrity blocker resolved and documented before outcomes.
- Confirmatory evaluation run on frozen TB2 splits with no post-freeze tuning/threshold shopping.
- Evaluation summary with CIs, blocks, breach counts, explicit gate verdict (or evidence-backed inadmissibility).
- Registries + manifest + handoffs updated; singular `next_unfinished_task` set.

## Verification commands
```bash
python -m unittest tests.test_volatility_features_splits tests.test_synthetic_boundary_labels tests.test_trackc_panel_admissibility_audit tests.test_trackc_funding_schema_audit tests.test_trackc_provenance_lineage -v
python -c "from scripts.trackc_provenance_lineage import verify_paths_with_manifests; from pathlib import Path; res=verify_paths_with_manifests([str(p) for p in Path('research_state/data_cache').rglob('*-fundingRate-*.csv')], repo_root=Path('.')); assert res['provenance_verified'] and res['unmapped_count']==0; print('PROVENANCE_OK', res['files_considered'])"
```

## Hard constraints (NON-NEGOTIABLE)
No network/paid/manual/credentialed data; no fabricated data/provenance; no threshold shopping; no sealed-holdout reuse; no Track A/B/C conflation (Track B = modeled synthetic breach proxies only, never observed liquidations); preregister/freeze before outcomes; no risk overlay until forecast gate passes; no `.github/workflows` edits. Heavy, verifiable progress only.

## State summary (evidence-backed)
- **Track B (priority 1, ACTIVE):** TB2 confirmatory run DUE NOW on frozen prereg (after resolving documented hash-integrity blocker).
- **Track C / H1 (priority 2):** CONCLUDED `NOT_SUPPORTED` on all claim-worthy local panels. Overlay INELIGIBLE.
- **Track A (priority 3):** `STRUCTURALLY_BLOCKED` (no admissible unauthenticated observed-liquidation census). Not locally repairable.
- **Key refs:** `research_state/research_protocol_trackb_TB2_20261110T190405Z.md`, `research_state/trackb_TB2_admissibility.json`, `research_state/trackb_TB2_label_design_scan.json`, `research_state/run_manifest.json`, `research_state/evaluation_summary_trackb_TB1_20261110T173838Z.md`, `scripts/synthetic_boundary_labels.py`, `scripts/run_trackb_evaluation.py`.
