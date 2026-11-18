# AGENT HANDOFF — 2026-11-18T02:32:59Z (sole durable handoff)

> **Authority:** this file only. Every other handoff-like file is tombstoned/historical and has no campaign authority. No duplicate authority remains.

## INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (timestamped 2026-11-18T02:32:59Z)

**State verified clean (2026-11-18T02:32:59Z). Program `ACTIVE_CAMPAIGN`. Heavy work is mandatory for the next session — do not stop cleanly.**

- Repo: `Funding-conditioned-volatility-and-liquidation-risk`. Repo-priority P0 = **Track C volatility/stress forecasting + Track B modeled liquidation-boundary labels**, using only admissible public price/mark-price data already on disk (no network, no parquet engine, no new root artifacts). This is the core mission: do funding extremes + realized volatility improve out-of-sample forecasts of future volatility and liquidation-boundary stress vs an RV-only baseline?
- Program: `ACTIVE_CAMPAIGN` — `FCLR-VOL-LIQ-FORECAST-01-20261118T023259Z`. Rank-0: `FCLR-BOUNDED-TRIGGER-ONLY-20261115T220000Z` (`TRIGGER_ONLY`, `next_action_heavy=null` — triggers remain OPEN; campaign proceeds on Track C/B cached-data work, not trigger-gated outcomes).
- Campaign `FCLR-LEDGER-INTEGRITY-02-20261118T004445Z` is **COMPLETE** (`research_state/session_20261118T004445Z/`). Frontier closed: `n_individually_feasible=1` (`2025-01`), `max_mutually_non_overlapping=1`, `campaign_feasible_non_overlapping=False`.
- Gates (verified this session): `check_handoff_heavywork_gate.py --json` **PASS** (`reason_code=OK`, `handoff_stale=false`, `failures=[]`, latest `session_20261118T004445Z`); `check_tracka_scope_registry_drift.py --json` **PASS** (196/196).
- Triggers all `OPEN`, none fired — no trigger-gated work. Campaign runs on non-trigger Track C/B heavy work instead.
- RV baseline: complete for 2024 Q1 (4 instruments: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT). Funding ablations PILOT/INCONCLUSIVE — data sufficiency not met: instruments=4 < 5, 0/3 required 30-day non-overlapping test blocks. **Next campaign must close these gaps.**

## Next session first/only action (run once, then stop only if blocked with recorded evidence)

**Step 1 — Run gate checks (read-only, no network):**
```bash
python3 scripts/check_handoff_heavywork_gate.py --json | jq '{pass,reason_code,handoff_stale,latest_session_id,failures,root_count,root_count_cap}'
python3 scripts/check_tracka_scope_registry_drift.py --json | jq '{pass,reason_code}'
python3 scripts/next_campaign_status.py --json | jq '.markfund_frontier | {n_individually_feasible,max_mutually_non_overlapping,campaign_feasible_non_overlapping,individually_feasible_months}'
```

**Step 2 — Execute heavy work (choose one, must produce new artifacts in `research_state/session_<UTC>/` only — root is at 500/500):**
- **Track C (primary):** Extend volatility forecasting beyond 2024 Q1 using existing cached ZIP/CSV data on disk. Add additional instruments/splits to close the `instruments=4 < 5` and `ok_30d=0 < 3` sufficiency gaps. Compare funding+RV features vs RV-only baseline with QLIKE/MAE/RMSE. Output: `research_state/session_<UTC>/trackc_vol_forecast_extend_<UTC>.{md,json}` + evaluation summary.
- **Track B (secondary):** Build modeled liquidation-boundary-breach labels from public mark-price data on disk (ZIP/CSV twins only — no parquet). Predefine hypothetical leverage/margin scenarios; calculate whether observed mark-price paths cross the modeled boundary. Clearly label as synthetic/modeled, not observed liquidation. Output: `research_state/session_<UTC>/trackb_boundary_labels_<UTC>.{md,json}`.

**Step 3 — Record results and update handoff:**
- Create `research_state/session_<UTC>/` (real UTC) with all new artifacts. **Record its id in this handoff before final gate capture.**
- Re-run Step 1 gate checks; confirm `handoff_stale=false`, `pass=true`.
- Targeted tests: `python3 -m unittest discover tests -q` (record count/errors/failures/EXIT; missing-`numpy` errors are environmental, not green).
- Update only `AGENT_HANDOFF.md`; preserve sole-handoff contract.

## If and only if a reopen trigger becomes machine-satisfied (outcome-gated heavy work)

1. Create `research_state/session_<UTC>/` (real UTC) and record its id in this handoff **before** final gate capture. Root `research_state/` is at 500/500 — put all new artifacts in the session dir only.
2. **GATE4_BRANCH_1:** only on `research_state/fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` with `status=RESOLVED_VERIFIED` and `fabricated=false` (human/legal attestation only). Execute Gate 4 Branch 1 protocol per `RESEARCH_PROMPT.md` §16 with outcome-blind prereg before outcomes.
3. **NEW_OBSERVED_LIQUIDATION_SOURCE:** only on `research_state/<source>_admissibility_audit_<UTC>.{md,json}` proving `status=ADMISSIBLE`, `observed_labels=true`, unauthenticated, provenance/license/venue-consistent, ≥5 instruments and (≥3 blocks or ≥1 complete month). Do admissibility audit BEFORE prereg/outcomes.
4. **HL_LABEL_EXTENSION:** only on verified post-2026-10-31 observed ironflow labels (≥100 days) with `research_state/hl_label_extension_audit_<UTC>.{md,json}`; then run a newly preregistered design per §17.
5. **EXPANSION_ROBUSTNESS_REDO:** only a newly preregistered design (`research_state/expansion_robustness_redo_prereg_<UTC>.json`) achieving LOIO≥6/8 AND placebo>95th null — **re-scoring sealed 19.04% is forbidden**.
6. For any triggered path: produce outcome-blind prereg, leakage/overlap audit against consumed windows, execution artifacts, evaluation summary, and gate captures in-session; do not weaken §17.

## Read first

1. `RESEARCH_PROMPT.md` §1–§5 (mission, constraints, source tracks A/B/C) and §16–§17 (gates).
2. `research_state/evaluation_summary.md` (RV baseline complete; funding ablations inconclusive; data-sufficiency gaps).
3. `research_state/fclr_final_structural_closure_20261116T114626.{md,json}` and `research_state/resume_trigger_registry.json`.
4. `research_state/session_20261118T004445Z/{ledger_audit,frontier_recompute,closure_ledger_backfill,trigger_check,trigger_activation_readiness,evidence_audit}_20261118T004445Z.*`.
5. `research_state/data_source_registry.json` (Binance ZIPs Track B/C concluded NOT_SUPPORTED for Track A; Hyperliquid alignment untested).

## Bottlenecks removed / prevented

- **Root churn cap (500/500):** all new artifacts go in `research_state/session_<UTC>/` only. No root-level `research_state/*.md|json`. Do not add root files.
- **Parquet engine absent:** use ZIP/CSV/JSON twins only. `.parquet`-only tasks blocked unless a CSV/JSON/ZIP twin exists. Do not run `git lfs pull` or `pip install` for parquet engines.
- **Data sufficiency (instruments=4 < 5; ok_30d=0 < 3):** Track C extension must add instruments and 30-day non-overlapping test blocks to close these gaps before any confirmatory claim.
- **Tested-window ledger omission fixed** (`FCLR-003` 2024-10-02..2024-12-31 in `TESTED_WINDOWS`); frontier honestly closed. Do not regress.
- **Closure-ledger backfill plan recorded** (`session_20261118T004445Z/closure_ledger_backfill_20261118T004445Z.*`); sealed closure JSON not mutated.
- **Ledger-integrity campaign 02 complete**; no pending integrity heavy work.
- **Sole durable handoff authority maintained**; no competing handoff. No empty/phantom sessions required.

## Prohibitions

- Do not start or re-run any sealed cached-data confirmatory estimand (FCLR-014, replication synthesis, design-frontier certificates, FCLR-013/010/002/003/009/006/008, frontier verify-06/07/08+, sealed 19.04% re-score).
- Do not poll, re-probe HuggingFace, use paid/credentialed/manual outcome data, or run network installs/data fetches (`git lfs pull`).
- Do not mutate sealed artifacts, closure JSON, `.github/workflows/*`, or add root-level `research_state/*.md|json` (root 500/500 cap).
- Do not add `statsmodels` or unpinned heavy deps to core path.
- Do not run `scripts/fclr_liq_010_confirm.py` (parquet-only; no engine installed).
- No parquet engine installed; `.parquet`-only tasks blocked unless CSV/JSON/ZIP twin exists (use ZIP-aware readers where applicable). Unresolved Git-LFS pointers remain unresolved — do not block on them.
- Do not treat environment-dependent missing-`numpy` discovery errors as green; discovery baseline was EXIT 1 in prior capture.
- Never inspect outcome data while producing outcome-blind trigger artifacts/preregs.
- Record any new session id in this handoff before final gate capture to keep `handoff_stale=false`.

## Reopen triggers (machine-checkable — all currently OPEN)

- `GATE4_BRANCH_1`: `research_state/fclr016_v5_terms_evidence_RESOLVED_*.json` (`status: RESOLVED_VERIFIED`, `fabricated: false`) — human/legal only.
- `NEW_OBSERVED_LIQUIDATION_SOURCE`: `research_state/<source>_admissibility_audit_<UTC>.{md,json}` (`status: ADMISSIBLE`, `observed_labels: true`, ≥5 instruments, ≥3 blocks or ≥1 complete month).
- `HL_LABEL_EXTENSION`: `research_state/hl_label_extension_audit_<UTC>.{md,json}` (post-2026-10-31 observed ironflow labels, ≥100-day depth).
- `EXPANSION_ROBUSTNESS_REDO`: `research_state/expansion_robustness_redo_prereg_<UTC>.json` + `evaluation_summary_*.json` (LOIO≥6/8 AND placebo>95th null; no sealed re-score).

## Verification record — 2026-11-18T02:32:59Z

- `check_handoff_heavywork_gate.py --json`: PASS (`reason_code=OK`, `handoff_stale=false`, `failures=[]`, latest `session_20261118T004445Z`, root_count=500/500).
- `check_tracka_scope_registry_drift.py --json`: PASS (196/196).
- `next_campaign_status.py --json`: `markfund_frontier` closed (`n_individually_feasible=1`, `individually_feasible_months=["2025-01"]`, `max_mutually_non_overlapping=1`, `campaign_feasible_non_overlapping=false`); `disjoint_block_frontier.n_feasible=0`.
- Triggers: all OPEN, `data_through=2026-10`, `consecutive_absent=3`, 2026-11/12 & 2027-01 `CONFIRMED_ABSENT`. No machine-satisfied reopen condition. Campaign proceeds on Track C/B cached-data heavy work.
- `AGENT_HANDOFF.md` remains sole durable handoff; no sealed artifacts/workflows/registries modified. Program state: `ACTIVE_CAMPAIGN` (heavy work mandatory, not optional).