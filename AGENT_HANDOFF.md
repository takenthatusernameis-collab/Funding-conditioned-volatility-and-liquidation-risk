# AGENT HANDOFF — 2026-11-18T04:59:43Z (sole durable handoff)

> **Authority:** this file only. Every other handoff-like file is tombstoned/historical and has no campaign authority. No duplicate authority remains.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-18T04:59:43Z)

**State: `ACTIVE_CAMPAIGN` / `GATE_REQUIRES_HEAVY_SESSION`. Heavy work is mandatory — do not stop cleanly.** Latest session recorded: `research_state/session_20261118T040400Z` (TRACKC Design A exploratory + Design C RV baseline; real quantitative pilot run, INCONCLUSIVE on primary contrast; BUT it emitted NO gate-mandated heavy artifacts — see gate state below).

**Repo (P0):** `Funding-conditioned-volatility-and-liquidation-risk` — **Track C volatility/stress forecasting** (funding extremes + RV vs RV-only baseline, QLIKE/MAE/RMSE, leakage-resistant OOS) and **Track B modeled liquidation-boundary labels** from public mark-price data. Use only admissible local/public data already on disk (ZIP/CSV/JSON/dir twins). **No network, no parquet engine, no `git lfs pull`, no installs, no new root `research_state/*.md|json` (root 500/500).**

- **Program:** `ACTIVE_CAMPAIGN` — `FCLR-VOL-LIQ-FORECAST-01-20261118T023259Z`. Rank-0: `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY`, `next_action_heavy=null`).
- **Frontier/ledger:** CLOSED/recorded (`session_20261118T004445Z` complete). Triggers all `OPEN`, none fired (no trigger-gated work). Campaign proceeds on non-trigger Track C/B cached-data heavy work.
- **Carried-forward complete Phase-B/C heavy bundle:** `research_state/session_20261116T100533Z/` (self-contained; referenced for gate continuity). Latest heavy session: `research_state/session_20261118T030427Z/`.

### Gates (verify first — CURRENT STATE: GATE FAILS, bottleneck identified below)
- `check_handoff_heavywork_gate.py --json` currently: **pass=false**, `reason_code=HANDOFF_HEAVYWORK_GATE_FAILED`, failure `HEAVY_SESSION_ARTIFACTS_MISSING:session_20261118T040400Z` — the latest session did real research but left no gate-mandated artifacts (no `rca011_*` Phase-B/C bundle, no `evidence_audit_*`, no `recompute_*` quant artifact). **This is the active bottleneck: the handoff cannot be considered green until a new session dir emits the mandatory stdlib-only evidence-audit + recompute pair.** `handoff_stale=false` (latest disk session == latest handoff session). Root=500/500 (at cap, not exceeding).
- `check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`, 196/196).
- `next_campaign_status.py --json`: confirmatory Binance cached design is **BLOCKED**: contiguous runs too short (61d/31d < 127d min), disjoint 30-day blocks `n_feasible=0` (train months 2024-02/03 and 2024-11/12 missing funding; Q1 2024 has no funding files), mark+funding-only `max_mutually_non_overlapping=1 < 3`. Hyperliquid bulk/extended frontiers exhausted (prior capture). No actionable frozen preregs (`actionable_preregs: []`). Ready funding-backed cache months: 2024-04, 2024-05, 2025-01 (complete but cannot host a 3-block confirmatory design from cache alone).

### Progress this session (2026-11-18T04:04:27Z → 04:04:37Z, `session_20261118T040400Z`, read-only cache, no network)
- TRACKC Design A exploratory (5 instruments BTC/ETH/SOL/XRP/BNB, 2024-04-01..2024-09-30, 4 pre-registered walk-forward splits, 7d purge/embargo, OLS HAR direct-variance, block bootstrap 2000 reps seed 12345): **DATA-SUFFICIENT PILOT / INCONCLUSIVE on primary contrast (E vs A CI spans 0; no improvement claim)**. Artifacts: `evaluation_summary_funding_TRACKC_DESIGN_A_EXPLORATORY.md`, `run_manifest_funding_TRACKC_DESIGN_A_EXPLORATORY.json` (+ Design C RV baseline manifest).
- **No gate-mandated artifacts emitted** (`evidence_audit_*`, `recompute_*`, Phase-B/C bundle missing) → heavy-work gate FAILS on this session.

### Bottlenecks removed / reinforced in this handoff
- **Gate bottleneck (ACTIVE):** latest session lacks mandatory heavy artifacts. Not removable by wish; removed by executing Step 2 below in a new `research_state/session_<UTC>/` dir: stdlib-only `evidence_audit_<UTC>.json+.md` + `recompute_trackc_leakage_audit_<UTC>.py+.json` (Track C leakage/data-completeness audit) and `recompute_trackb_breach_labels_<UTC>.py+.json` (Track B breach-label generator), then record the new session id in this handoff **before** final gate capture (`handoff_stale=false`).
- **Estimand-execution blocker (`numpy`/`pandas`/`scipy` absent, installs prohibited):** removed as a *blocker* by mandatory stdlib-only substitution. Session must not stall on it. A session that waits for numpy is stalled; a session that emits the stdlib artifacts has done heavy work.
- **Root churn cap at exactly 500/500:** `research_state/` root md+json count is at the cap (verified 500). All new artifacts go into `research_state/session_<UTC>/` only. Zero root `research_state/*.md|json` additions — any root addition breaches the cap and fails the gate.
- **Handoff freshness:** latest session id recorded before final gate capture; `handoff_stale=false` required. If a newer `session_*` directory exists on disk than is recorded in the handoff, the handoff is stale and must be updated before completion.
- **Heavy-work non-avoidance:** gate captures alone do NOT satisfy heavy work. A session producing only `check_*` outputs with no new `evidence_audit_*` + `recompute_*` artifact pair has not done heavy work and must not report completion. The gate machine-checks this (`check_handoff_heavywork_gate.py`).

## Next session — first/only actions (run once; produce NEW artifacts in a new session dir, then stop only if blocked with recorded evidence)

**Step 1 — Gates/status (read-only):**
```bash
python3 scripts/check_handoff_heavywork_gate.py --json
python3 scripts/check_tracka_scope_registry_drift.py --json
python3 scripts/next_campaign_status.py --json
```

**Step 2 — Execute heavy work (MANDATORY; no skipping. Choose highest-value feasible path; write ALL new artifacts to `research_state/session_<UTC>/` only):**

The numerical estimand (Design A Track C confirmatory) is **blocked** (missing `numpy`/`pandas`/`scipy`, installs prohibited; AND cached confirmatory design has <3 mutually non-overlapping 30-day blocks). It cannot run confirmatorily in this environment. The fallback heavy work below is stdlib-only and **required** — a session that produces only gate captures without a new quantitative/leakage artifact has not done heavy work.

- **Primary fallback (REQUIRED):** produce a **stdlib-only** zip/csv data-completeness & leakage-audit artifact for Design A (bar counts per symbol/month/kind, gaps, split boundary integrity, funding alignment checks, tested-window non-conflict verification for 2024-04..2024-09), using only cached ZIP/CSV/dir. Emit `evidence_audit_<UTC>.json` + `.md` **and** a deterministic stdlib recompute driver `recompute_trackc_leakage_audit_<UTC>.py` + `.json` in session dir. Both are mandatory: `evidence_audit_*` satisfies the gate's audit prefix; `recompute_trackc_leakage_audit_*` satisfies the gate's `recompute_*` quant prefix. No numpy/pandas/scipy imports allowed.
- **Secondary fallback (REQUIRED):** implement a **stdlib Track B** mark-price breach-label generator for a frozen scenario set (leverage [5,10,20] × long/short × horizon [4h,24h] over a small cached window, e.g. one funded month in 2024-04..09), emitting `recompute_trackb_breach_labels_<UTC>.py` + `.json` (session-local label CSV/JSON inside session dir). Clearly label synthetic/modeled, not observed. No numpy/pandas/scipy imports allowed.
- **If numerical runtime becomes available (upgrade path):** freeze an outcome-blind exploratory prereg in session dir for **Design A** (`trackc_extension_design_20261118T030427Z.json`: 5 instruments BTC/ETH/SOL/XRP/BNB, 2024-04-01..2024-09-30, 3 splits × 30d non-overlapping tests, 7d purge/embargo, expanding train, A_rv_only/B_rv_signed/C_rv_abs/D_rv_signed_abs/E_rv_funding_trails, QLIKE/MAE/RMSE, block-bootstrap ΔQLIKE CIs). Verify per-symbol bar completeness and tested-window/leakage non-conflict, then run and emit per-split metrics + evaluation summary in session dir. Label **EXPLORATORY/PILOT**; do not claim confirmatory/promotion.

**Step 3 — Record, verify, hand off:**
- Create `research_state/session_<UTC>/` with the artifacts above and gate captures. Record its id in this handoff **before** final gate capture (`handoff_stale=false`).
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
- **Confirmatory design infeasible from cache:** <3 mutually non-overlapping 30-day blocks; Q1 2024 no funding; train months missing funding → Step 2 stdlib fallback is the only executable heavy path; do not declare the campaign closed on this.
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

## Verification record — 2026-11-18T04:59:43Z
- `check_handoff_heavywork_gate.py --json`: **FAIL** `pass=false`, `reason_code=HANDOFF_HEAVYWORK_GATE_FAILED`, failure `HEAVY_SESSION_ARTIFACTS_MISSING:session_20261118T040400Z`; `handoff_stale=false`; root=500/500. This FAIL is the recorded bottleneck; the next session clears it via Step 2 (new session dir with `evidence_audit_*` + `recompute_*` pair, id recorded in handoff before final capture).
- `check_tracka_scope_registry_drift.py --json`: **PASS** (`reason_code=OK`, 196/196) — `session_20261118T030427Z/scope_drift.json`.
- `next_campaign_status.py --json`: confirmatory Binance cached design BLOCKED (`n_feasible=0` disjoint blocks; `max_mutually_non_overlapping=1 < 3`; contiguous runs 61d/31d < 127d); no actionable preregs; ready cache months 2024-04/05, 2025-01 design-infeasible from cache.
- `python3 -m unittest discover -q`: not green (environmental missing-numpy baseline pre-existing; 1126/62 errors/9 failures/14 skipped/EXIT 1 recorded previously). Not re-run as gate substitute.
- Artifacts (session-only): TRACKC Design A exploratory evaluation + run manifest (`session_20261118T040400Z`). No sealed artifacts/workflows/registries modified. `AGENT_HANDOFF.md` sole durable handoff refreshed; session id recorded.
