# AGENT HANDOFF — 2026-11-18T09:23:38Z (sole durable handoff)

> **Authority:** this file only. Every other handoff-like file is tombstoned/historical and has no campaign authority. No duplicate authority remains.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-18T09:23:38Z)

**Repo (P0):** `Funding-conditioned-volatility-and-liquidation-risk` — **Track C volatility/stress forecasting** (funding extremes + RV vs RV-only baseline, QLIKE/MAE/RMSE, leakage-resistant OOS) and **Track B modeled liquidation-boundary labels** from public mark-price data. Use only admissible local/public data already on disk (ZIP/CSV/JSON/dir twins in `research_state/data_cache/` and `data/raw/`). **No network, no parquet engine, no `git lfs pull`, no installs, no new root `research_state/*.md|json` (root 500/500 at cap).**

**State: `ACTIVE_CAMPAIGN` / GATE GREEN, BOTTLENECKS CLEARED, NEXT HEAVY CAMPAIGN BOUND.** Latest recorded heavy session: `research_state/session_20261118T091852Z`. The next session must NOT idle, re-audit, or emit another gate-only note. It must execute the mandatory execution campaign below and record its new session id in this handoff before final gate capture.

**Program lineage:** parent `FCLR-VOL-LIQ-FORECAST-01-20261118T023259Z`. **Active execution campaign: `FCLR-VOL-LIQ-EXECUTION-01-20261118T092338Z`** (Track C Design A stdlib forecast + Track B modeled breach labels). Rank-0 trigger state remains `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY`, `next_action_heavy=null`); all triggers OPEN, none fired.

### Gates (verify first — CURRENT STATE: ALL PASS)
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **pass=true**, `handoff_stale=false`, root=500/500 (at cap). The gate now binds the new execution campaign: a post-start latest session must contain the exact Track C and Track B artifacts below and a non-empty `trigger_check_*.json`; audit-only, empty-file, and gate-only sessions fail closed.
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`, 196/196).
- `python3 scripts/next_campaign_status.py --json`: confirmatory multi-block cached design remains **BLOCKED** (contiguous runs too short; disjoint 30-day blocks `n_feasible=0`; `max_mutually_non_overlapping=1 < 3`). Ready funding-backed cache months: 2024-04, 2024-05, 2025-01. No actionable frozen preregs. This blocker is **overcome for Track C single-window Design A** by the stdlib leakage audit: 3 disjoint 30d splits fit 2024-04..09 with 5 instruments.
- `python3 -m unittest tests.test_tracka_hardening_143 -v`: **PASS (32 tests)** after the handoff/gate hardening. Full `unittest discover` remains environmental/hanging in this runtime; use targeted tests and record that limitation, not a green full suite.

### Bottlenecks resolved in this handoff (2026-11-18T09:23:38Z)
- **Empty-session bypass (CLEARED):** `session_20261118T050304Z` had zero-byte `evidence_audit_*` + `recompute_*` files. The new execution-campaign gate rejects zero-byte required artifacts by name and size, so empty placeholders can no longer satisfy the heavy-work contract.
- **Audit-only / gate-only non-avoidance (CLEARED):** the previous gate accepted a generic audit + recompute. `FCLR-VOL-LIQ-EXECUTION-01-20261118T092338Z` now requires the exact Track C forecast triad and Track B breach-label triad plus a trigger check in the latest post-start session.
- **Failing real-repo regression (CLEARED):** `tests/test_tracka_hardening_143.py::test_real_repo_heavy_session_self_contained` failed because the gate reported Phase-B gaps for an accepted new-style session. The gate now reports `heavy_session_mode=new_style_audit_quant` with `heavy_session_missing=[]`; the targeted suite passes.
- **Estimand-execution blocker (`numpy`/`pandas`/`scipy` absent, installs prohibited):** remains an environment constraint, not a data/design constraint. Do not wait for numpy. Implement the required stdlib fallback (`math`/`csv`/`json`/`zipfile`) and label results EXPLORATORY/PILOT.

### Progress recorded at 2026-11-18T09:18:52Z (`session_20261118T091852Z`, read-only cache, no network)
- **Track C Design A data-completeness + leakage audit (stdlib-only, executed):** 5 instruments (BTC/ETH/SOL/XRP/BNB) × 6 months (2024-04..09).
  - Funding files: **30/30 present**, 549 rows/symbol, strictly monotonic timestamps.
  - 1h klines (plain/mark/index/premium): **24 rows/day, zero missing days** across all 5×6.
  - 3 disjoint 30d test splits (7d purge/embargo, expanding train) fit within 183 days (last test ends day 111); pairwise disjoint.
  - Tested-window non-conflict: tested months 2024-05/06/07 all inside the provenanced window; **zero sealed/holdout months touched**.
  - **Verdict: PASS.**
- Artifacts: `recompute_trackc_leakage_audit_20261118T091852Z.py`, `evidence_audit_20261118T091852Z.json`, `evidence_audit_20261118T091852Z.md`, `recompute_trackc_leakage_audit_20261118T091852Z.json`.

## Next session — REQUIRED heavy-work campaign (non-avoidable; do not stop cleanly)

Create a new `research_state/session_<UTC>/` directory. Produce **both** mandatory tracks, the evidence audit, and the trigger check. The gate will reject the session if any required artifact is missing, empty, or replaced by another generic recompute. Record the new session id in this handoff **before** final gate capture.

### Track C — Design A exploratory forecast (stdlib OLS HAR, REQUIRED)
Use the verified-complete 2024-04..09 cache for BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT. Read-only ZIP/CSV/dir twins only.

**Frozen splits (from `trackc_extension_design_20261118T030427Z.json`, Design A):**
- Split 1: train `2024-04-01..2024-05-15` (45d); embargo `2024-05-16..2024-05-22` (7d); test `2024-05-23..2024-06-21` (30d).
- Split 2: train `2024-04-01..2024-06-21` (82d); embargo `2024-06-22..2024-06-28` (7d); test `2024-06-29..2024-07-28` (30d).
- Split 3: train `2024-04-01..2024-07-28` (119d); embargo `2024-07-29..2024-08-04` (7d); test `2024-08-05..2024-09-03` (30d).

**Target:** next-24h realized variance from 1h mark-price close-to-close log returns over `t+1..t+24` (`markPriceKlines`, 1h). Record exact mark field and units.

**Features (outcome-blind, causal at t):**
- `RV1h`, `RV24h`, `RV168h` trailing realized variances; `log(RV + 1e-12)` target/features.
- Signed funding: latest funding observation with `calc_time <= t`; retain sign.
- Absolute funding as a separate feature.
- Funding trails: trailing-only funding mean/EWMA and, if available, past-only percentile; require a minimum history and record counts.
- Do not use future bars, full-sample normalization, or sealed months. Train-only means/stds; document zero-variance handling and smearing back-transformation.

**Models (fixed, no search):**
- A: RV-only HAR direct-variance OLS.
- B: A + signed funding.
- C: A + absolute funding.
- D: A + signed + absolute funding.
- E: D + funding trails/EWMA.

**Estimation:** stdlib only (`math`/`csv`/`json`/`zipfile`). Build normal equations and solve by Gaussian elimination with partial pivoting; no numpy/pandas/scipy/statsmodels. Fit per split on expanding train; evaluate on the 30d test block. Use identical forecast origins and common eligible rows for paired comparisons.

**Metrics:** QLIKE primary; MAE/RMSE on the stated variance target. Compute paired ΔQLIKE for each candidate vs A. Use a deterministic block bootstrap (2000 reps, seed `12345`) resampling complete UTC time blocks jointly across instruments; report percentile CIs. Also report leave-one-instrument-out and per-split metrics.

**Required artifacts (exact prefixes; all non-empty):**
- `trackc_design_a_forecast_<UTC>.py`
- `trackc_design_a_forecast_<UTC>.json`
- `trackc_design_a_forecast_<UTC>.md`
- `evidence_audit_<UTC>.json`
- `evidence_audit_<UTC>.md`
- `trigger_check_<UTC>.json`

Label the output **EXPLORATORY/PILOT**. Do not claim confirmatory/promotion or a forecast-gate pass.

### Track B — Modeled boundary-breach labels (stdlib, REQUIRED)
Use one funded month, `2024-04`, and all 5 instruments with dense mark-price 1h klines. Read-only cached data only.

**Frozen scenarios (outcome-blind):**
- Leverage `L ∈ {5, 10, 20}`; side `long`/`short`; horizon `H ∈ {4h, 24h}`.
- Entry at the close of bar `t` (known at t); evaluate hourly mark path `t+1..t+H`.
- Illustrative isolated-margin approximation only: maintenance-margin rate `mmr = 0.005` (0.5%), no funding carry, no fees, no account-specific engine.
- Long boundary: `P0 * (1 - 1/L) / (1 - mmr)`.
- Short boundary: `P0 * (1 + 1/L) / (1 + mmr)`.
- Breach if any mark in `t+1..t+H` crosses the boundary; record first-breach time and distance. Keep long/short labels separate.

**Label semantics:** `label_type=synthetic_modeled_boundary_breach`; `observed_liquidation_labels=false`. Never call these observed liquidations. State that this does not reconstruct account-specific liquidation engines, portfolio margin, insurance-fund behavior, or forced-liquidation records.

**Required artifacts (exact prefixes; all non-empty):**
- `trackb_breach_labels_<UTC>.py`
- `trackb_breach_labels_<UTC>.json`
- `trackb_breach_labels_<UTC>.md`
- `evidence_audit_<UTC>.json`
- `evidence_audit_<UTC>.md`
- `trigger_check_<UTC>.json`

### Record, verify, hand off
1. Create `research_state/session_<UTC>/` with all artifacts above.
2. Update this handoff's latest session id to the new session before running the final gate.
3. Run targeted tests only: `python3 -m unittest tests.test_tracka_hardening_143 tests.test_tracka_hardening_125 -v` (bounded; full discover hangs in this env).
4. Re-run all three gates; confirm PASS and paste the exact outcomes into the verification record.
5. Update only `AGENT_HANDOFF.md` and the new session directory. Do not modify sealed artifacts, closure JSON, registries, or `.github/workflows/*`.

## Upgrade path (only if numerical runtime becomes available)
Freeze an outcome-blind exploratory prereg for Design A using the `trackc_extension_design` schema, verify per-symbol bar completeness and tested-window non-conflict (already PASS), then run per-split metrics + evaluation summary. Label EXPLORATORY/PILOT until all §17 gates pass.

## If and only if a reopen trigger becomes machine-satisfied (outcome-gated)
1. Create `research_state/session_<UTC>/` and record id in handoff before final gate capture.
2. **GATE4_BRANCH_1:** `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal). Outcome-blind prereg before outcomes.
3. **NEW_OBSERVED_LIQUIDATION_SOURCE:** `<source>_admissibility_audit_<UTC>.{md,json}` proving `status=ADMISSIBLE`, `observed_labels=true`, unauthenticated, provenance/license/venue-consistent, ≥5 instruments and (≥3 blocks or ≥1 complete month). Admissibility audit BEFORE prereg/outcomes.
4. **HL_LABEL_EXTENSION:** verified post-2026-10-31 observed ironflow labels (≥100 days) + `hl_label_extension_audit_<UTC>.{md,json}` + newly preregistered design.
5. **EXPANSION_ROBUSTNESS_REDO:** newly preregistered design achieving LOIO≥6/8 AND placebo>95th null — **re-scoring sealed 19.04% forbidden**.

## Read first
1. `RESEARCH_PROMPT.md` §1–§6, §16–§17.
2. `research_state/session_20261118T091852Z/{evidence_audit,recompute_trackc_leakage_audit}_20261118T091852Z.*` (feasibility foundation).
3. `research_state/session_20261118T030427Z/{trackc_extension_design,data_coverage_audit,trackc_vol_forecast_extend,trackb_boundary_labels,evidence_audit}_20261118T030427Z.*` (design specs + Track B protocol).
4. `research_state/evaluation_summary.md`, `research_state/data_source_registry.json`, `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`, `research_state/resume_trigger_registry.json`.

## Prohibitions
- Do not re-run sealed cached-data confirmatory estimands or re-score sealed results (FCLR-014, replication synthesis, design-frontier certs, FCLR-013/010/002/003/009/006/008, frontier verify-06/07/08+, sealed 19.04%).
- No polling/HF re-probe, no paid/credentialed/manual outcome data, no network installs/fetches, no `git lfs pull`.
- No mutation of sealed artifacts/closure JSON/`.github/workflows/*`; no root-level `research_state/*.md|json` (root 500/500 cap).
- No `statsmodels` or unpinned heavy deps in core path. Do not run parquet-only scripts without a CSV/JSON/ZIP twin.
- Do not treat missing-numpy/environmental discovery errors as green. Never inspect outcomes while producing outcome-blind preregs. **Do not emit empty/zero-byte artifacts; content is mandatory.**
- Do not leave a session recorded in this handoff without its `evidence_audit_*` + `recompute_*`/required execution artifacts present and non-empty on disk.

## Reopen triggers (machine-checkable — all OPEN)
- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`).
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status=ADMISSIBLE`, `observed_labels=true`, ≥5 instruments, ≥3 blocks or ≥1 complete month).
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` (post-2026-10-31 observed ironflow labels, ≥100-day depth).
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary (LOIO≥6/8 AND placebo>95th null).

## Verification record — 2026-11-18T09:23:38Z
- `python3 scripts/check_handoff_heavywork_gate.py --json`: **PASS** after this refresh (`pass=true`, `reason_code=OK`, root=500/500, latest `session_20261118T091852Z`; `heavy_session_mode=new_style_audit_quant`, `heavy_session_missing=[]`). The new `FCLR-VOL-LIQ-EXECUTION-01-20261118T092338Z` requirement is grandfathered for the pre-start latest session and binds the next post-start session.
- `python3 scripts/check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`, 196/196).
- `python3 scripts/next_campaign_status.py --json`: confirmatory multi-block cached design BLOCKED (`n_feasible=0`, `max_mutually_non_overlapping=1<3`); Track C single-window Design A feasible via stdlib audit (3 disjoint splits, 5 instruments, 2024-04..09).
- `python3 -m unittest tests.test_tracka_hardening_143 -v`: **PASS (32 tests)**, including new fail-closed coverage for audit-only, empty-file, missing-trigger, full-package, and pre-start grandfathering.
- Full `python3 -m unittest discover -q`: not green; pre-existing environmental hang >120s in this runtime. Record as environmental, not a gate substitute.
- No sealed artifacts/workflows/registries modified. `AGENT_HANDOFF.md` remains the sole durable handoff; this refresh records the next heavy campaign and the exact non-avoidance contract.