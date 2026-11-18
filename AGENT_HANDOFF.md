# AGENT HANDOFF — 2026-11-18T04:07:09Z (sole durable handoff)

> **Authority:** this file only. Every other handoff-like file is tombstoned/historical and has no campaign authority. No duplicate authority remains.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-18T04:07:09Z)

**State: `ACTIVE_CAMPAIGN`. Heavy work is mandatory — do not stop cleanly.** Latest session recorded: `research_state/session_20261118T040400Z` (read-only data audit + Design A/B/C gap-closure designs + Track B modeled-boundary protocol; gate post-capture PASS with `handoff_stale=false`).

- **Repo (P0):** `Funding-conditioned-volatility-and-liquidation-risk` — **Track C volatility/stress forecasting** (funding extremes + RV vs RV-only baseline, QLIKE/MAE/RMSE, leakage-resistant OOS) and **Track B modeled liquidation-boundary labels** from public mark-price data. Use only admissible local/public data already on disk (ZIP/CSV/JSON/dir twins). **No network, no parquet engine, no `git lfs pull`, no installs, no new root `research_state/*.md|json` (root 500/500).**
- **Program:** `ACTIVE_CAMPAIGN` — `FCLR-VOL-LIQ-FORECAST-01-20261118T023259Z`. Rank-0: `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY`, `next_action_heavy=null`).
- **Frontier/ledger:** CLOSED/recorded (`session_20261118T004445Z` complete). Triggers all `OPEN`, none fired (no trigger-gated work). Campaign proceeds on non-trigger Track C/B cached-data heavy work.
- **Carried-forward complete Phase-B/C heavy bundle:** `research_state/session_20261116T100533Z/` (self-contained; referenced for gate continuity). Latest heavy session: `research_state/session_20261118T030427Z/`.
- **Gates (verify first):** `check_handoff_heavywork_gate.py --json` must show `pass=true`, `reason_code=OK`, `handoff_stale=false`, latest = `session_20261118T040400Z`; `check_tracka_scope_registry_drift.py --json` PASS (196/196).

### Progress this session (2026-11-18T03:04:27Z, `session_20261118T030427Z`, read-only data audit, no network)
- **Data-sufficiency bottleneck mapped to cached data (concrete):** 5 instruments (BTC/ETH/SOL/XRP/BNB) have funding + mark/index/plain-1h kline caches on disk for **2024-04..2024-12** (`data_coverage_audit_20261118T030427Z.json`). Prior ablation gaps closeable in design: `instruments 4→5` (add BNBUSDT) and `ok_30d blocks 0→3` (proposed 3x30d chronological tests with 7d purge/embargo in 2024-04..09 window) — see `trackc_extension_design_20261118T030427Z.json` / `trackc_vol_forecast_extend_20261118T030427Z.md`.
- **Provenance constraint:** `scripts/run_funding_ablations.py` confirmatory-provenanced range = 2024-04-01..2024-09-30 (FCLR-015). 2024-10..12 funded but outside that range and overlapping sealed FCLR-003 test context → **exploratory-only with explicit audit/caveat**; confirmatory-intent paths refuse unprovenanced ranges. Q1 2024 has no funding files (RV-only extension feasible only).
- **Track B (modeled boundaries):** feasibility/protocol documented for synthetic breach labels from cached mark-price ZIP/CSV/dir (no parquet, no observed liquidations) — `trackb_boundary_labels_20261118T030427Z.{md,json}`.
- **Execution blocker (environmental):** `numpy`/`pandas`/`scipy` absent; forecast/ablation scripts import at module level. **Estimand execution not completed this session** (no installs permitted). Full unittest discovery is environment-dependent (missing-numpy errors pre-existing; not green).

### Bottlenecks removed / reinforced in this handoff
- **Estimand-execution blocker (numpy/pandas/scipy missing, installs prohibited):** cannot be removed by install, so it is removed as a *blocker* by mandatory stdlib-only substitution. Session must not stall on it. The stdlib-only fallback paths below (evidence_audit + recompute_trackc_leakage_audit + recompute_trackb_breach_labels) produce real quantitative/leakage artifacts without the numerical stack. A session that waits for numpy is stalled; a session that emits the stdlib artifacts has done heavy work.
- **Root churn cap at exactly 500/500:** `research_state/` root md+json count is at the cap. All new artifacts go into `research_state/session_<UTC>/` only. Zero root `research_state/*.md|json` additions — any root addition breaches the cap and fails the gate.
- **Handoff freshness:** latest session id recorded before final gate capture; `handoff_stale=false` required. If a newer `session_*` directory exists on disk than is recorded in the handoff, the handoff is stale and must be updated before completion.
- **Heavy-work non-avoidance:** gate captures alone do NOT satisfy heavy work. A session producing only `check_*` outputs with no new `evidence_audit_*` + `recompute_*` artifact pair has not done heavy work and must not report completion. The gate machine-checks this (`check_handoff_heavywork_gate.py`).

## Next session — first/only actions (run once; produce NEW artifacts in a new session dir, then stop only if blocked with recorded evidence)

**Step 1 — Gates/status (read-only):**
```bash
python3 scripts/check_handoff_heavywork_gate.py --json | jq '{pass,reason_code,handoff_stale,latest_session_id,failures,root_count,root_count_cap}'
python3 scripts/check_tracka_scope_registry_drift.py --json | jq '{pass,reason_code}'
python3 scripts/next_campaign_status.py --json | jq '{markfund_frontier,disjoint_block_frontier,actionable_preregs}'
```

**Step 2 — Execute heavy work (MANDATORY; no skipping. Choose highest-value feasible path; write ALL new artifacts to `research_state/session_<UTC>/` only):**

The numerical estimand (Design A Track C) is **blocked** by missing `numpy`/`pandas`/`scipy` (environmental, installs prohibited). It cannot run in this environment. The fallback heavy work below is stdlib-only and **required** — a session that produces only gate captures without a new quantitative/leakage artifact has not done heavy work.

- **Primary fallback (REQUIRED):** produce a **stdlib-only** zip/csv data-completeness & leakage-audit artifact for Design A (bar counts per symbol/month/kind, gaps, split boundary integrity, funding alignment checks, tested-window non-conflict verification for 2024-04..2024-09), using only cached ZIP/CSV/dir. Emit `evidence_audit_<UTC>.json` + `.md` **and** a deterministic stdlib recompute driver `recompute_trackc_leakage_audit_<UTC>.py` + `.json` in session dir. Both are mandatory: `evidence_audit_*` satisfies the gate's audit prefix; `recompute_trackc_leakage_audit_*` satisfies the gate's `recompute_*` quant prefix. No numpy/pandas/scipy imports allowed.
- **Secondary fallback (REQUIRED):** implement a **stdlib Track B** mark-price breach-label generator for a frozen scenario set (leverage [5,10,20] × long/short × horizon [4h,24h] over a small cached window, e.g. one funded month in 2024-04..09), emitting `recompute_trackb_breach_labels_<UTC>.py` + `.json` (session-local label CSV/JSON inside session dir). Clearly label synthetic/modeled, not observed. No numpy/pandas/scipy imports allowed.
- **If numerical runtime becomes available (upgrade path):** freeze an outcome-blind exploratory prereg in session dir for **Design A** (`trackc_extension_design_20261118T030427Z.json`: 5 instruments BTC/ETH/SOL/XRP/BNB, 2024-04-01..2024-09-30, 3 splits × 30d non-overlapping tests, 7d purge/embargo, expanding train, A_rv_only/B_rv_signed/C_rv_abs/D_rv_signed_abs/E_rv_funding_trails, QLIKE/MAE/RMSE, block-bootstrap ΔQLIKE CIs). Verify per-symbol bar completeness and tested-window/leakage non-conflict, then run and emit per-split metrics + evaluation summary in session dir. Label **EXPLORATORY/PILOT**; do not claim confirmatory/promotion.

**Step 3 — Record, verify, hand off:**
- Create `research_state/session_<UTC>/` with `evidence_audit_<UTC>.md`, outputs, and gate captures. Record its id in this handoff **before** final gate capture (`handoff_stale=false`).
- Run targeted tests and/or `python3 -m unittest discover -q` (record counts/errors/failures/EXIT; missing-numpy/environmental errors are not green). Re-run gates; confirm PASS. Update only `AGENT_HANDOFF.md`.

## If and only if a reopen trigger becomes machine-satisfied (outcome-gated)
1. Create `research_state/session_<UTC>/` and record id in handoff before final gate capture.
2. **GATE4_BRANCH_1:** `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal). Outcome-blind prereg before outcomes.
3. **NEW_OBSERVED_LIQUIDATION_SOURCE:** `<source>_admissibility_audit_<UTC>.{md,json}` proving `status=ADMISSIBLE`, `observed_labels=true`, unauthenticated, provenance/license/venue-consistent, ≥5 instruments and (≥3 blocks or ≥1 complete month). Admissibility audit BEFORE prereg/outcomes.
4. **HL_LABEL_EXTENSION:** verified post-2026-10-31 observed ironflow labels (≥100 days) + `hl_label_extension_audit_<UTC>.{md,json}` + newly preregistered design.
5. **EXPANSION_ROBUSTNESS_REDO:** newly preregistered design achieving LOIO≥6/8 AND placebo>95th null — **re-scoring sealed 19.04% forbidden**.

## Read first
1. `RESEARCH_PROMPT.md` §1–§6, §16–§17.
2. `research_state/session_20261118T030427Z/{trackc_extension_design,data_coverage_audit,trackc_vol_forecast_extend,trackb_boundary_labels,evidence_audit}_20261118T030427Z.*`.
3. `research_state/evaluation_summary.md`, `research_state/data_source_registry.json`, `research_state/fclr_final_structural_closure_20261116T114626.{md,json}`, `research_state/resume_trigger_registry.json`.
4. `research_state/session_20261118T004445Z/*` (frontier/ledger closed).

## Bottlenecks removed / prevented
- **Instrument/block planning gap:** concrete 5-instrument, 3x30d-split Design A/B/C specified against cached data (closes planning blocker for stated sufficiency gaps).
- **Provenance/sealed-window hazard surfaced:** 2024-10..12 and 2025+ confirmatory guards/sealed overlaps explicitly flagged; Design A constrained to provenanced 2024-04..09 window.
- **Root churn (500/500):** all new artifacts in session dir only. **No parquet engine:** zip/csv/dir only. **No network/installs/LFS.**
- **Handoff freshness:** this session id recorded here before final gate capture.
- **Sole durable handoff maintained.**
- **Heavy-work non-avoidance:** Step 2 fallback paths (stdlib-only leakage audit + Track B breach-label generator) are mandatory when numpy/pandas/scipy unavailable; gate captures alone do not satisfy heavy-work requirement.

## Prohibitions
- Do not re-run sealed cached-data confirmatory estimands or re-score sealed results (FCLR-014, replication synthesis, design-frontier certs, FCLR-013/010/002/003/009/006/008, frontier verify-06/07/08+, sealed 19.04%).
- No polling/HF re-probe, no paid/credentialed/manual outcome data, no network installs/fetches, no `git lfs pull`.
- No mutation of sealed artifacts/closure JSON/`.github/workflows/*`; no root-level `research_state/*.md|json`.
- No `statsmodels` or unpinned heavy deps in core path. Do not run parquet-only scripts without a CSV/JSON/ZIP twin.
- Do not treat missing-numpy/environmental discovery errors as green. Never inspect outcomes while producing outcome-blind preregs.

## Reopen triggers (machine-checkable — all OPEN)
- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`).
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status=ADMISSIBLE`, `observed_labels=true`, ≥5 instruments, ≥3 blocks or ≥1 complete month).
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` (post-2026-10-31 observed ironflow labels, ≥100-day depth).
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + evaluation summary (LOIO≥6/8 AND placebo>95th null).

## Verification record — 2026-11-18T03:26:00Z
- `check_handoff_heavywork_gate.py --json` (pre-handoff-update): **PASS** `pass=true`, `reason_code=OK`, `handoff_stale=false`, latest=`session_20261118T030427Z`; post-update capture: see `session_20261118T030427Z/heavywork_gate_post.json`.
- `check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`, 196/196) — `session_20261118T030427Z/scope_drift.json`.
- `next_campaign_status.py --json`: captured in `session_20261118T030427Z/next_campaign_status.json` (frontier closed, no actionable preregs; Hyperliquid bulk/extended frontiers exhausted; mark+funding-only n_feasible=0, max_mutually_non_overlapping=1 < 3).
- `python3 -m unittest discover -q`: not run to completion in-session (environmental missing-numpy baseline; prior recorded 1126/62 errors/9 failures/14 skipped/EXIT 1). No targeted tests executed beyond gates; estimand scripts blocked by missing numpy/pandas/scipy.
- Artifacts (session-only): data inventory/coverage audit, Track C extension designs + status, Track B boundary protocol/feasibility, evidence audit, gate/status captures. No sealed artifacts/workflows/registries modified. `AGENT_HANDOFF.md` sole durable handoff updated; session id recorded.

(End of file - total 89 lines)