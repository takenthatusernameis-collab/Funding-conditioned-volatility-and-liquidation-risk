# AGENT HANDOFF — 2026-11-16T04:15:00Z (sole durable handoff)

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION
**Priority (repo: Funding-conditioned-volatility-and-liquidation-risk):** FCLR-RCA-011 bounded reproducibility/integrity campaign (B1/B2/B3/B4 + synthesis) is complete on cached data with no trigger fired. The session is **not** clean-finish until you (1) confirm the full regression suite is green end-to-end, (2) record the exact result in this handoff, and (3) hold `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (TRIGGER_ONLY). Do not start a new confirmatory estimand, do not re-run concluded/sealed cells, do not mutate sealed artifacts, do not edit `.github/workflows/*`, do not fabricate data/outcomes.

### Step 0 — environment (already satisfied in 2026-11-16T035833Z session; verify)
```bash
python3 -c "import numpy, pandas, pyarrow, scipy, statsmodels; print('deps OK')"
```
`pip install -r requirements.txt statsmodels -q` was run successfully and deps were present (`deps OK`). If missing in your runtime, reinstall from `requirements.txt` + `statsmodels` before gates.

### Step 1 — deterministic gates (required; full discover must be recorded)
```bash
python3 scripts/check_tracka_scope_registry_drift.py
python3 -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_117 tests.test_tracka_hardening_118
python3 -m unittest discover -q
```
**Recorded 2026-11-16T035833Z session:** drift PASS (`scripts=195 registry=195 reason=OK`). Targeted gate PASS: `Ran 38 tests in 0.393s` / `OK` (`tests.test_active_campaign_gate`, `tests.test_tracka_hardening_117`, `tests.test_tracka_hardening_118`). `python3 -m unittest discover -q` was started but **not confirmed complete** in that session's tool budget (long-running; no completion summary captured, no residual unittest process observed at handoff write). **Next session must run `discover -q` to completion and record pass/fail counts here.**

### Step 2 — RCA artifacts (done; read, do not redo unless inputs change)
Written to `research_state/session_20261116T035833Z/` (root md/json unchanged this session except this handoff update):
- `rca011_feature_attribution_20261116T035833Z.{json,md}` — B1 nested attribution on `session_20261116T0040Z/fclr011_recompute_panel_20261116T004150Z.parquet` (OLS log(RV+1e-12), train-only z-scaling, Duan smearing, 7d purge, 24h block bootstrap 2000/seed 20261114; train 152 / test 10,905). **Funding drives recompute harm:** B1_plus_funding vs B1 **-342.67%** (CI [-497.48,-221.27]); B1_plus_ema24 vs B1 **+9.75%** (CI [7.01,12.74]); joint vs B1 **-294.01%**; joint vs B1_plus_funding **+10.99%**; joint vs B1_plus_ema24 **-336.55%**.
- `rca011_impl_crosscheck_20261116T035833Z.json` — statsmodels.OLS vs numpy.linalg.lstsq parity (~1e-12–1e-17); **no solver/smearing artifact**.
- `rca011_sealed_bridge_ext_20261116T035833Z.md` — extends `session_20261116T023837Z/rca011_sealed_bridge_20261116T023837Z.md` (sealed +4.94%/+1.36%/+3.63% n=10,785 vs recompute -294.01%/-342.67%/+10.99% n=10,905; premium not computable from cached 2026 archive, +120-row eligibility delta, sealed panel LFS pointer unauditable here).
- `program_power_synthesis_20261116T035833Z.{json,md}` — **FCLR-011 classification: (c) feature/back-transform/artifact-driven integrity failure with underpowered/unstable training fit (152 complete train rows)**; sealed PASS not independently reproduced/not promotable. `next_action_heavy=null`.
- `prereg_template_trigger_gated_20261116T023837Z.json` (prior session) remains adequate; no B1/B2-driven refinement required beyond documenting train-completeness/power and premium/feature-availability audit before any future freeze.

### Step 3 — trigger discipline (no re-poll)
- Last performed: `research_state/session_20261116T023837Z/trigger_check_20261116T023837Z.json` (2026-11-16T02:40:53Z). **NO_TRIGGER_FIRED.** GATE4_BRANCH_1, NEW_OBSERVED_LIQUIDATION_SOURCE, HL_LABEL_EXTENSION, EXPANSION_ROBUSTNESS_REDO all OPEN. Ironflow data_through 2026-10; 2026-11..2027-01 absent. Do not re-probe/poll.

### Step 4 — update this handoff and stop cleanly
After `discover -q` completes, update this file in place with exact command, pass/fail/skip/error counts, and any failures with evidence. If all gates green and no trigger: hold TRIGGER_ONLY, no commit required. If a trigger fires in a future session, follow §16 admissibility audit + NEW pre-outcomes prereg (template minima: >=3 non-overlapping 30d blocks, MDE < 2% floor, Holm family, `outcome_data_inspected_before_freeze=false`, 7d purge/embargo, materially different estimand).

## What changed this session (2026-11-16T035833Z) & why
- **Unblocked env:** `pip install -r requirements.txt statsmodels -q` succeeded; `deps OK` (numpy/pandas/pyarrow/scipy/statsmodels).
- **Gates:** scope-registry drift PASS; targeted `active_campaign_gate`/`hardening_117`/`hardening_118` PASS (38 tests). Full `discover -q` not confirmed complete (see Step 1) — explicit bottleneck to close next session.
- **Phase B completed:** B1 nested feature attribution, B2 statsmodels-vs-lstsq cross-check, B3 sealed bridge extension, B4 template adequacy confirmed. **Phase C completed:** program power synthesis with FCLR-011 classified as feature/artifact-driven integrity failure + unstable sparse train fit (not promotable, not independently reproduced).
- No registries/run_manifests/hypotheses/frontier mutated; no sealed artifacts changed; no workflows touched.

## Current gate/program state (authoritative)
- **Frontier rank 0:** `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z`, TRIGGER_ONLY / BOUNDED_TRIGGER_ONLY, `all_terminal=true`, `next_action_heavy=null`.
- **FCLR-H001 / FCLR-009:** complete, **NOT_MET** (`research_state/evaluation_summary_FCLR-009.md`); do not rerun.
- **FCLR-011:** sealed PASS **not independently reproduced**; recompute harm attributable to funding augmentation on cached panel with no impl artifact (B1/B2). Fragile/non-promotable.
- **Track A:** no new admissible observed-liquidation data (ironflow through 2026-10). **Track B:** sealed NOT_SUPPORTED. **Track C:** terminal on cached confirmatory designs. **H2:** EXPLORATORY_ONLY, not promotable.
- **Gate 4 Branch 1:** blocked on human/legal attestation.

## Blockers & commands/results
- **Open blocker:** `python3 -m unittest discover -q` completion unconfirmed this session — rerun to completion and record counts (Step 1).
- **Structural (external):** all resume triggers OPEN; no agent-removable confirmatory estimand on cached data.
- **State constraints:** `research_state/` root md/json at/near capacity (498/500 noted previously) — write new artifacts to `research_state/session_<UTC>/` only. Never edit `.github/workflows/*`. Never fabricate data/outcomes.

## Next materially different free route
Hold TRIGGER_ONLY with fully green suite and finalized RCA/synthesis. Advance only on a satisfied external trigger with §16 admissibility audit + NEW pre-outcomes prereg (materially different estimand, >=3 non-overlapping 30d blocks, MDE below 2% floor, Holm family preregistered).

## Tombstones (no authority)
- `NEXT_SESSION_HANDOFF.md`, `NEXT_SESSION_TASK.md`: tombstoned 2026-11-15T22:57:29Z.
- `AGENT_HANDOFF_20261115T073240Z.md`: SUPERSEDED — ignore.
