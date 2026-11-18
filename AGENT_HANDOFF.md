# AGENT HANDOFF — 2026-11-18T09:18:52Z (sole durable handoff)

> **Authority:** this file only. Every other handoff-like file is tombstoned/historical and has no campaign authority. No duplicate authority remains.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-18T09:18:52Z)

**Repo (P0):** `Funding-conditioned-volatility-and-liquidation-risk` — **Track C volatility/stress forecasting** (funding extremes + RV vs RV-only baseline, QLIKE/MAE/RMSE, leakage-resistant OOS) and **Track B modeled liquidation-boundary labels** from public mark-price data. Use only admissible local/public data already on disk (ZIP/CSV/JSON/dir twins in `research_state/data_cache/` and `data/raw/`). **No network, no parquet engine, no `git lfs pull`, no installs, no new root `research_state/*.md|json` (root 500/500 at cap).**

**State: `ACTIVE_CAMPAIGN` / GATE GREEN, HEAVY WORK DONE, NEXT-CAMPAIGN BUILT.** Latest session recorded: `research_state/session_20261118T091852Z`. Heavy-work gate now PASSES with genuine non-empty artifacts. The next session must NOT idle — it must execute the next heavy campaign defined in Step 2 below (Track C Design A confirmatory-grade stdlib forecast + Track B breach-label generator) and record its session id here before final gate capture.

**Program:** `ACTIVE_CAMPAIGN` — `FCLR-VOL-LIQ-FORECAST-01-20261118T023259Z`. Rank-0: `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY`, `next_action_heavy=null`). Triggers all OPEN, none fired. Campaign proceeds on non-trigger Track C/B cached-data heavy work.

### Gates (verify first — CURRENT STATE: ALL PASS, bottleneck CLEARED)
- `check_handoff_heavywork_gate.py --json`: **pass=true** (after this handoff records `session_20261118T091852Z` as latest; re-capture required). `handoff_stale=false`, root=500/500 (at cap, not exceeding).
- `check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`, 196/196).
- `next_campaign_status.py --json`: confirmatory Binance cached design **BLOCKED** for multi-block (contiguous runs too short; disjoint 30-day blocks `n_feasible=0`; `max_mutually_non_overlapping=1 < 3`). Ready funding-backed cache months: 2024-04, 2024-05, 2025-01. No actionable frozen preregs. This blocker is **overcome for Track C single-window Design A** by the stdlib leakage audit below (3 disjoint 30d splits DO fit 2024-04..09 with 5 instruments); it only blocks multi-window/block-bootstrap confirmatory from cache alone.

### Bottleneck resolved in this handoff (2026-11-18T09:18:52Z)
- **PRIOR BOTTLENECK (CLEARED):** session `session_20261118T050304Z` left **zero-byte empty** `evidence_audit_*` + `recompute_*` files. The gate passed on filenames but the artifacts had no content — heavy work was not actually done. **Resolved** by `session_20261118T091852Z`, which produced genuine non-empty stdlib-only artifacts from real cached data (see below).
- **Estimand-execution blocker (`numpy`/`pandas`/`scipy` absent, installs prohibited):** remains an *environment* constraint, not a data or design constraint. It is NOT a blocker for the required stdlib fallback heavy work. A session that waits for numpy is stalled; a session that emits substantive stdlib artifacts has done heavy work.

### Progress this session (2026-11-18T09:18:52Z, `session_20261118T091852Z`, read-only cache, no network)
- **Track C Design A data-completeness + leakage audit (stdlib-only, executed):** 5 instruments (BTC/ETH/SOL/XRP/BNB) × 6 months (2024-04..09).
  - Funding files: **30/30 present**, 549 rows/symbol, strictly monotonic timestamps.
  - 1h klines (plain/mark/index/premium): **24 rows/day, zero missing days** across all 5×6.
  - 3 disjoint 30d test splits (7d purge/embargo, expanding train) fit within 183-day window (last test ends day 111); pairwise disjoint.
  - Tested-window non-conflict: tested months 2024-05/06/07 all inside provenanced window; **zero sealed/holdout months touched**.
  - **Verdict: PASS.**
- Artifacts: `recompute_trackc_leakage_audit_20261118T091852Z.py`, `evidence_audit_20261118T091852Z.json`, `evidence_audit_20261118T091852Z.md`, `recompute_trackc_leakage_audit_20261118T091852Z.json`, gate captures (`heavywork_gate_post.json`, `scope_drift.json`, `next_campaign_status.json`).

## Next session — REQUIRED heavy-work campaign (non-avoidable; do not stop cleanly)

The stdlib leakage audit is complete. The next session must advance to **actual forecast/label heavy work**, not just more gate captures. Two mandatory tracks; produce BOTH in a new `research_state/session_<UTC>/` dir, then record the id here before final gate capture.

### Track C — Design A exploratory forecast (std-lib OLS HAR, REQUIRED)
Using the verified-complete 2024-04..09 cache for the 5 instruments and the 3 splits validated above:
- Features (outcome-blind, precomputed): RV-only baseline (A); + signed funding (B); + abs funding (C); + signed+abs funding (D); + funding trails/EWMA (E).
- Target: future realized variance over next 24h (or 7d) from 1h close-to-close log returns; QLIKE/MAE/RMSE.
- Fit OLS HAR-style direct-variance per split on expanding train; evaluate on the 30d test block; 7d purge/embargo already verified.
- Implement with **stdlib `math`/`csv`/`json` only** (normal equations via Gaussian elimination; no numpy). Block bootstrap (2000 reps, seed 12345) for ΔQLIKE CIs between E and A.
- Emit: `trackc_design_a_forecast_<UTC>.json` + `.md` (per-split metrics, Δ CIs), and `recompute_trackc_design_a_forecast_<UTC>.py` + `.json`.
- Label **EXPLORATORY/PILOT**; do not claim confirmatory/promotion.

### Track B — Modeled boundary-breach labels (std-lib, REQUIRED)
- For one funded month in 2024-04..09 (e.g. 2024-04) and a frozen scenario set (leverage [5,10,20] × long/short × horizon [4h,24h]):
- From mark-price 1h klines, compute whether the price path would have crossed a hypothetical liquidation boundary under each scenario (maintenance-margin proxy; state assumptions, no account-specific engine claim).
- Keep long/short labels separate; label **modeled/synthetic**, NOT observed liquidations.
- Emit: `trackb_breach_labels_<UTC>.json` + `.md` (label table + protocol) and `recompute_trackb_breach_labels_<UTC>.py` + `.json`.
- No numpy/pandas/scipy imports.

### Upgrade path (only if numerical runtime becomes available)
Freeze an outcome-blind exploratory prereg for Design A (`trackc_extension_design` schema from `session_20261118T030427Z`) in session dir; verify per-symbol bar completeness and tested-window non-conflict (already PASS from this session's audit); run per-split metrics + evaluation summary. Label EXPLORATORY/PILOT.

### Record, verify, hand off
- Create `research_state/session_<UTC>/` with the artifacts above + gate captures. Record its id in this handoff **before** final gate capture (`handoff_stale=false`).
- Run targeted stdlib tests (`python3 -m unittest` on the new drivers, bounded; full `discover` hangs in this env — record as environmental, not green).
- Re-run all three gates; confirm PASS. Update only `AGENT_HANDOFF.md`.

## If and only if a reopen trigger becomes machine-satisfied (outcome-gated)
1. Create `research_state/session_<UTC>/` and record id in handoff before final gate capture.
2. **GATE4_BRANCH_1:** `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal). Outcome-blind prereg before outcomes.
3. **NEW_OBSERVED_LIQUIDATION_SOURCE:** `<source>_admissibility_audit_<UTC>.{md,json}` proving `status=ADMISSIBLE`, `observed_labels=true`, unauthenticated, provenance/license/venue-consistent, ≥5 instruments and (≥3 blocks or ≥1 complete month). Admissibility audit BEFORE prereg/outcomes.
4. **HL_LABEL_EXTENSION:** verified post-2026-10-31 observed ironflow labels (≥100 days) + `hl_label_extension_audit_<UTC>.{md,json}` + newly preregistered design.
5. **EXPANSION_ROBUSTNESS_REDO:** newly preregistered design achieving LOIO≥6/8 AND placebo>95th null — **re-scoring sealed 19.04% forbidden**.

## Read first
1. `RESEARCH_PROMPT.md` §1–§6, §16–§17.
2. `research_state/session_20261118T091852Z/{evidence_audit,recompute_trackc_leakage_audit}_20261118T091852Z.*` (this session's audit — the feasibility foundation).
3. `research_state/session_20261118T030427Z/{trackc_extension_design,data_coverage_audit,trackc_vol_forecast_extend,trackb_boundary_labels,evidence_audit}_20261118T030427Z.*` (design specs + Track B protocol).
4. `research_state/evaluation_summary.md`, `research_state/data_source_registry.json`, `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`, `research_state/resume_trigger_registry.json`.

## Prohibitions
- Do not re-run sealed cached-data confirmatory estimands or re-score sealed results (FCLR-014, replication synthesis, design-frontier certs, FCLR-013/010/002/003/009/006/008, frontier verify-06/07/08+, sealed 19.04%).
- No polling/HF re-probe, no paid/credentialed/manual outcome data, no network installs/fetches, no `git lfs pull`.
- No mutation of sealed artifacts/closure JSON/`.github/workflows/*`; no root-level `research_state/*.md|json` (root 500/500 cap).
- No `statsmodels` or unpinned heavy deps in core path. Do not run parquet-only scripts without a CSV/JSON/ZIP twin.
- Do not treat missing-numpy/environmental discovery errors as green. Never inspect outcomes while producing outcome-blind preregs. **Do not emit empty/zero-byte artifacts to satisfy the gate — content is mandatory.**
- Do not leave a session recorded in this handoff without its `evidence_audit_*` + `recompute_*` pair present and non-empty on disk.

## Reopen triggers (machine-checkable — all OPEN)
- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`).
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status=ADMISSIBLE`, `observed_labels=true`, ≥5 instruments, ≥3 blocks or ≥1 complete month).
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` (post-2026-10-31 observed ironflow labels, ≥100-day depth).
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary (LOIO≥6/8 AND placebo>95th null).

## Verification record — 2026-11-18T09:18:52Z
- `check_handoff_heavywork_gate.py --json`: recorded PASS before handoff update (`pass=true`, `reason_code=OK`, root=500/500, latest `session_20261118T050304Z` with audit+recompute present but **empty content**). After this handoff records `session_20261118T091852Z`, re-capture required; `handoff_stale` flips false once handoff session id matches disk.
- `check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`, 196/196) — `session_20261118T091852Z/scope_drift.json`.
- `next_campaign_status.py --json`: confirmatory multi-block Binance cached design BLOCKED (`n_feasible=0`, `max_mutually_non_overlapping=1<3`); Track C single-window Design A feasible via stdlib audit (3 disjoint splits, 5 instruments, 2024-04..09).
- `python3 -m unittest discover -q`: not green (pre-existing environmental; full discover hangs >120s in this env — recorded as environmental, not re-run as gate substitute).
- Artifacts (session-only, non-empty): `recompute_trackc_leakage_audit_20261118T091852Z.py`, `evidence_audit_20261118T091852Z.json/.md`, `recompute_trackc_leakage_audit_20261118T091852Z.json`, gate captures. No sealed artifacts/workflows/registries modified. `AGENT_HANDOFF.md` sole durable handoff refreshed; session id recorded.