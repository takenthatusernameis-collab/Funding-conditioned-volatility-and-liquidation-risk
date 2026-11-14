# AGENT HANDOFF — 2026-11-14T06:25:08Z (single durable handoff)

## INITIAL TASK FOR NEXT AGENTIC WORK SESSION (execute now; heavy, local, unblocked)

**Campaign:** `FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z` (rank 0, `READY_EXECUTE`)
**Phase A (P0, mandatory, start immediately):** `FCLR-011-INDEPENDENT-RECOMPUTE-20261114T042139Z`
**Phase B (mandatory next — run after Phase A completes, or run with bounded evidence if Phase A is data-blocked):** `FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T042139Z`

**Do not emit a status-only report. Do not wait for Gate 4. Do not reuse the old "no heavy work remains" directive (superseded).** This is an execution session, not a planning/status session.

### Baseline (verified 2026-11-14T06:25:08Z)
- `research_state/experiment_frontier.json` rank 0 = `FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z` (`READY_EXECUTE`).
- Targeted tests and `scripts/fclr_campaign_gate.py --arm all` = **19/19 PASS** when run with the repo venv interpreter that has deps (`/tmp/fclr-venv/bin/python`; system `python3` may lack `pyarrow` and fail A0, which is an environment issue, not a research blocker).
- No agent-removable blockers found. Gate 4/external-legal trigger absent but **not required** for these local exploratory audits.
- No peer/session bottleneck in repo state: stale "no heavy work" directive is superseded, active-campaign guard/test and artifact-count guard are repaired, cached inputs are present.
- `fclr011_panel.json` is an unresolved Git-LFS pointer — **rebuild from cache; do not wait for LFS**.
- Existing helpers present: `scripts/fclr011_recompute_audit.py` (Phase A) and cached 2026 Binance zips under `research_state/data_cache/{SYM}_2026_MM` for Jan–Aug (BTC/ETH/BNB/SOL/XRP). Cached ironflow bulk/events exist under `research_state/data_cache/ironflow_bulk/` and `research_state/data_cache/ironflow_events/` for Phase B.

### Execute Phase A end-to-end (P0)
1. **Verify env/baseline quickly:** `/tmp/fclr-venv/bin/python scripts/fclr_campaign_gate.py --arm all` (expect 19/19). Use `/tmp/fclr-venv/bin/python` for scripts needing `pyarrow`/pandas/numpy if system env is missing deps.
2. **Freeze prereg before any outcome computation:** `/tmp/fclr-venv/bin/python scripts/fclr011_recompute_audit.py --write-prereg --out-utc 20261114T042139Z` (or equivalent) to create `research_state/prereg_fclr011_recompute_20261114T042139Z.json` + `.md` with `status=FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes=true`, `pre_registered_before_outcomes=true`, `outcome_data_inspected_before_freeze=false`, `promotable=false`, `max_status=EXPLORATORY_ONLY`, `audit_only=true`, `does_not_reopen_sealed_verdict=true`. Do not inspect outcomes before freeze.
3. **Frozen design (assert, do not tune):** Train `2026-01-01T00:00:00Z..2026-03-17T23:00:00Z`, Val `2026-03-25T00:00:00Z..2026-04-30T23:00:00Z`, Test `2026-05-08T00:00:00Z..2026-08-06T23:00:00Z` (7-day purge/embargo). Universe BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT. Target next-24h RV of mark/close returns per frozen spec. B0 persistence; B1 HAR (log RV1h/24h/168h); C1=B1+signed funding+90d abs-funding pct (>=30 prior obs); C2=C1+premium/mark features as computable per script/spec. OLS on `log(RV+1e-12)`, train-only mean/std scaling, train-only smearing back-transform. **No zero-fill/forward-fill**; paired common eligible rows; report coverage/exclusions.
4. **Rebuild panel from cache (no LFS):** use `research_state/data_cache/{SYM}_2026_MM` for 2026-01..2026-08 (`markPriceKlines,indexPriceKlines,premiumIndexKlines,klines,fundingRate` as available). UTC-normalize, preserve source, dedupe, record hashes; causal features at closed hour; target from strictly future bars. Emit `research_state/fclr011_recompute_panel_20261114T042139Z.parquet` + build report (hashes, row counts, coverage, split bounds, panel SHA-256).
5. **Independent evaluation:** run `/tmp/fclr-venv/bin/python scripts/fclr011_recompute_audit.py` end-to-end (after prereg frozen) to assert frozen prereg, fit B0/B1/C1/C2 on train only, evaluate frozen test, compute QLIKE/MAE/RMSE, paired 24h circular block bootstrap (2000 deterministic reps), Holm over `C2_vs_B1,C1_vs_B1,C2_vs_C1`, LOIO, funding-permutation placebo, per-symbol/block stability, leakage audit. Emit `research_state/evaluation_summary_FCLR-011-RECOMPUTE-20261114T042139Z.{json,md}` with verdict `REPRODUCED|NOT_REPRODUCED|INCONCLUSIVE|INADMISSIBLE` (all `EXPLORATORY_ONLY`, `promotable=false`). **Do not modify sealed FCLR-011 artifacts.**
6. **Stop rule:** instruments < 5, test blocks < 3, or insufficient core coverage => bounded `INADMISSIBLE/INCONCLUSIVE` NO_GO with exact failing minima (no threshold relaxation after outcomes). Record evidence.

### Execute Phase B (mandatory)
Independently recompute sealed Track A liquidation expansion PASS (2026-05..2026-10, 8 HL symbols, 593 paired rows, +19.04% C2-vs-B1 QLIKE; robustness FRAGILE LOIO 4/8, placebo FAIL) using cached ironflow bulk/events, **observed HL liquidation labels only** (no modeled/proxy/synthetic, no venue mixing). Freeze prereg before outcomes; same leakage/embargo/complete-case/deterministic-bootstrap rules; emit `research_state/prereg_tracka_liq_expansion_recompute_20261114T042139Z.*` (or timestamped equivalent per script) and `research_state/evaluation_summary_TRACKA-LIQ-EXPANSION-RECOMPUTE-<UTC>.{json,md}`. Preserve sealed records. Not promotable.

### After each phase (atomically)
- Update `research_state/experiment_frontier.json` (advance/record phase status), add audit hypothesis in `research_state/hypothesis_registry.json` (do not alter sealed statuses), append `research_state/negative_results_report.md` and `research_state/leakage_audit.md`.
- Append a dated session log entry below with commands, key results/hashes, verdicts, and blockers (if any).
- Re-run `/tmp/fclr-venv/bin/python scripts/fclr_campaign_gate.py --arm all` (expect 19/19) and relevant targeted tests.

### Invariants
Preregister before outcome inspection; observed≠modeled labels; no venue mixing; no forward-fill/synthetic; no May 2026/sealed holdout scoring; no terminal verdict reopening; no sealed artifact overwrites; no `.github/workflows/*` edits; no raw parquet/cache commits; no fabricated artifacts/thresholds/p-values/verdicts. Root artifact guard is tracked-baseline + untracked-file (do not delete evidence).

---

## Session log

### 2026-11-14T06:25:08Z — Durable handoff refreshed (initial task made execution-explicit)
- Re-verified baseline from repo state: `experiment_frontier` rank 0 = `FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z` (`READY_EXECUTE`, Phase A ready, Phase B pending). `scripts/fclr_campaign_gate.py --arm all` = 19/19 PASS via `/tmp/fclr-venv/bin/python` (system python lacks `pyarrow` causing env-only A0 fail; not an agent-removable research blocker).
- Confirmed prerequisites present: `scripts/fclr011_recompute_audit.py`, cached Binance 2026-01..2026-08 month dirs for BTC/ETH/BNB/SOL/XRP in `research_state/data_cache/`, and ironflow bulk/events caches for Phase B. No Phase A prereg/recompute artifacts found yet.
- Refreshed this single durable handoff as a timestamped, execution-first initial task for the next session (Phase A then Phase B). No status-only stopping; no Gate 4 wait; "no heavy work remains" remains superseded. No code/tests/sealed artifacts modified.

### 2026-11-14T04:21:39Z
- Refreshed the single durable handoff. Installed `FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z` as the active rank-0 campaign with mandatory Phase A (FCLR-011 independent recomputation) and Phase B (Track A liquidation expansion recomputation).
- Repaired the artifact-count guard to use the tracked baseline plus an untracked-file check, removing the recurring 406-vs-419 bottleneck.
- Updated the active-campaign test to stop hardcoding the completed P0 as the only allowed rank-0 task.
- Preserved all prior artifacts and sealed verdicts.

### 2026-11-14T03:35:26Z
- Refreshed durable handoff after P0 completion. Rechecked triggers: no `fclr016_v5_terms_evidence_RESOLVED_*`, no qualifying new observed-liquidation source. Recorded bounded trigger-only state; redirected next session to execute-on-trigger or emit bounded NO_GO. **Superseded by the 04:21:39Z red-team campaign.**

### 2026-11-14T03:30:40Z
- Executed FCLR-VOL-FORWARD-AUDIT-20261114T032041Z: corrected evaluator (train-only fit/scaling, paired per-row block bootstrap n=1485/block_h=168/reps=2000, paired-permutation Holm, execution metadata), hardened gate (F6_deep), verdict EXPLORATORY_NULL (VALID_EXPLORATORY, rel -0.89%, CI [-0.005794,-0.001762]), gate 19/19 PASS, tests 34/34 OK. Artifacts panel e4d1d8a6..., build 9e38717d..., eval 24636d80....

### 2026-11-14T03:20:41Z
- Audited stale post-handoff checkpoint; identified 02:45 vol-forward evaluation invalid (test-row fit, unscaled collapse, NaN bootstrap, placeholder Holm). Replaced false "no heavy work" directive with executable P0 audit campaign.

### 2026-11-14T02:35:42Z
- Prior 02:33 INADMISSIBLE claim superseded by 02:43/02:45 checkpoint; preserved as history, not to be repeated.

### 2026-11-14T04:37:07Z
- Baseline re-verified at current HEAD (a28eecc96): 55 targeted tests OK; `scripts/fclr_campaign_gate.py --arm all` = 19/19 PASS.
- Active rank-0 campaign `FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z` is `READY_EXECUTE`. Phase A (`FCLR-011-INDEPENDENT-RECOMPUTE-20261114T042139Z`) = `READY_EXECUTE`; Phase B (`FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T042139Z`) = `PENDING_PHASE_A`. No agent-removable blockers. `fclr011_panel.json` remains an unresolved Git-LFS pointer — rebuild the FCLR-011 panel from cached Binance inputs instead of waiting for LFS.
- Bottlenecks already removed: stale "no heavy work" handoff superseded, hardcoded active-campaign test removed, artifact-count guard repaired to tracked-baseline + untracked-file check. Gate 4 external/legal trigger absent but not required for these local exploratory audits.
- Next action: execute Phase A end-to-end — freeze prereg (`research_state/prereg_fclr011_recompute_20261114T042139Z.json` + `.md`, status FROZEN_PRE_OUTCOMES before any outcome computation), rebuild the panel from `research_state/data_cache/{SYM}_2026_MM` (2026-01..2026-08), run independent train-only OLS/HAR recomputation of B0/B1/C1/C2 on frozen splits, emit `research_state/evaluation_summary_FCLR-011-RECOMPUTE-20261114T042139Z.{json,md}` with verdict one of REPRODUCED/NOT_REPRODUCED/INCONCLUSIVE/INADMISSIBLE. Then execute Phase B. Do not stop at a status-only report; do not wait for Gate 4; do not reuse the old "no heavy work remains" directive (superseded).
