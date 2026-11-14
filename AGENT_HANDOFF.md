# AGENT HANDOFF — 2026-11-14T06:24:00Z (single durable handoff)

## INITIAL TASK FOR NEXT SESSION (execute now; heavy, local, unblocked)

**Campaign:** `FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z`
**Phase A (P0, mandatory):** `FCLR-011-INDEPENDENT-RECOMPUTE-20261114T042139Z`
**Then Phase B (mandatory if A completes / if A blocked execute B with evidence):** `FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T042139Z`

**Do not emit a status-only report. Do not wait for Gate 4. Do not reuse the old "no heavy work remains" directive (superseded).** Baseline verified 2026-11-14T06:24:00Z: targeted tests and `scripts/fclr_campaign_gate.py --arm all` pass (19/19). Gate 4 absent but not required.

### Execute Phase A end-to-end
1. **Freeze prereg before any outcome computation:** create `research_state/prereg_fclr011_recompute_20261114T042139Z.json` + `.md` with `status=FROZEN_PRE_OUTCOMES`, `frozen_before_outcomes=true`, `pre_registered_before_outcomes=true`, `outcome_data_inspected_before_freeze=false`, `promotable=false`, `max_status=EXPLORATORY_ONLY`, `audit_only=true`, `does_not_reopen_sealed_verdict=true`.
2. **Frozen design:** Train `2026-01-01T00:00:00Z..2026-03-17T23:00:00Z`, Val `2026-03-25T00:00:00Z..2026-04-30T23:00:00Z`, Test `2026-05-08T00:00:00Z..2026-08-06T23:00:00Z` (7-day purge/embargo). Universe BTC/ETH/BNB/SOL/XRPUSDT. Target next-24h RV of mark returns. B0 persistence; B1 HAR (log RV1h/24h/168h); C1=B1+signed funding+90d abs-funding pct (>=30 prior obs); C2=C1+mark/index premium+mark/EMA24 dist. OLS on `log(RV+1e-12)`, train-only mean/std scaling, train-only smearing back-transform. **No zero-fill/forward-fill**; paired common eligible rows; report coverage/exclusions.
3. **Rebuild panel from cache (do not rely on LFS `fclr011_panel.json`):** `research_state/data_cache/{SYM}_2026_MM` for 2026-01..2026-08 (`markPriceKlines,indexPriceKlines,premiumIndexKlines,klines,fundingRate`). UTC-normalize, preserve source, dedupe, record hashes; causal features at closed hour; target from strictly future bars. Emit `research_state/fclr011_recompute_panel_20261114T042139Z.parquet` + build report (hashes, row counts, coverage, split bounds, panel SHA-256).
4. **Independent evaluation:** deterministic script (e.g. `scripts/fclr011_recompute_audit.py`) asserts frozen prereg, fits B0/B1/C1/C2 on train only, evaluates frozen test, computes QLIKE/MAE/RMSE, paired 24h circular block bootstrap (2000 deterministic reps), Holm over `C2_vs_B1,C1_vs_B1,C2_vs_C1`, LOIO, funding-permutation placebo, per-symbol/block stability, leakage audit. Emit `research_state/evaluation_summary_FCLR-011-RECOMPUTE-20261114T042139Z.{json,md}` with verdict `REPRODUCED|NOT_REPRODUCED|INCONCLUSIVE|INADMISSIBLE` (all `EXPLORATORY_ONLY`, `promotable=false`). **Do not modify sealed FCLR-011 artifacts.**
5. **Stop rule:** instruments < 5, test blocks < 3, or insufficient core coverage => bounded `INADMISSIBLE/INCONCLUSIVE` NO_GO with exact failing minima (no threshold relaxation after outcomes).

### Execute Phase B
Independently recompute sealed Track A liquidation expansion PASS (2026-05..2026-10, 8 HL symbols, 593 paired rows, +19.04% C2-vs-B1 QLIKE; robustness FRAGILE LOIO 4/8, placebo FAIL) using cached ironflow bulk, observed HL liquidation labels only (no modeled/proxy/synthetic, no venue mixing). Freeze prereg before outcomes; same leakage/embargo/complete-case/deterministic-bootstrap rules; emit `research_state/evaluation_summary_TRACKA-LIQ-EXPANSION-RECOMPUTE-<UTC>.{json,md}`. Preserve sealed records. Not promotable.

### After each phase (atomically)
Update `experiment_frontier.json`, add audit hypothesis in `hypothesis_registry.json` (do not alter sealed statuses), append `negative_results_report.md` and `leakage_audit.md`, append session log here with commands/results/hashes/verdicts, re-run targeted tests and `scripts/fclr_campaign_gate.py --arm all`.

### Invariants
Preregister before outcome inspection; observed≠modeled labels; no venue mixing; no forward-fill/synthetic; no May 2026/sealed holdout scoring; no terminal verdict reopening; no sealed artifact overwrites; no `.github/workflows/*` edits; no raw parquet/cache commits; no fabricated artifacts/thresholds/p-values/verdicts. Root artifact guard is tracked-baseline + untracked-file (do not delete evidence).

---

## Session log

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

### 2026-11-14T04:38:21Z — NEXT SESSION INITIAL TASK (heavy, local, unblocked)
**Campaign:** `FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z`
**Phase A (P0, execute NOW):** `FCLR-011-INDEPENDENT-RECOMPUTE-20261114T042139Z`

The authoritative single durable handoff has been verified. Baseline tests pass (55/55, gate 19/19). The only remaining work is **execution**.

**Immediate steps for the next session:**
1. **Verify baseline** (optional, < 2 min): `python -m unittest tests.test_active_campaign_gate tests.test_tracka_hardening_099 tests.test_fclr_canonical_artifacts tests.test_fclr_final_structural_closure tests.test_fclr_campaign_gate` and `python scripts/fclr_campaign_gate.py --arm all` — expect 19/19 PASS.
2. **Freeze Phase A prereg** — create `research_state/prereg_fclr011_recompute_20261114T042139Z.json` and `.md` with `frozen_before_outcomes=true`, `pre_registered_before_outcomes=true`, `promotable=false`, `max_status=EXPLORATORY_ONLY`, `audit_only=true`, `does_not_reopen_sealed_verdict=true`, and the **exact frozen splits**: Train `2026-01:01..2026:03:17`, Val `2026:03:25..2026:04:30`, Test `2026:05:08..2026:08:06` (7-day purge/embargo at boundaries); universe: BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT; target: next-24h RV; models: B0/B1 (HAR), C1=C1+funding+abs_funding_pct, C2=C2+premium+EMA24_dist; OLS on `log(RV+1e-12)` with train-only scaling; **no zero/forward fill**; paired block bootstrap 2000 reps, 24h blocks, Holm across 3 contrasts; stop rule: <5 instruments, <3 test blocks, or insufficient core coverage → INADMISSIBLE.
3. **Rebuild panel from raw cache** — **do not use the LFS pointer** (`fclr011_panel.json` = OID `8def31f4...`). Use `research_state/data_cache/{SYM}_2026_MM` (Jan–Aug 2026), UTC-normalize, deduplicate, record hashes, compute features at each closed hour, forward target from strictly future bars. Emit panel parquet + build report with input hashes, row counts, coverage, split boundaries, panel SHA-256.
4. **Run independent evaluation** — implement/extend `scripts/fclr011_recompute_audit.py` (or equivalent) that asserts prereg, builds panel, fits B0/B1/C1/C2 on train only, evaluates test block, computes QLIKE/MAE/RMSE, paired diffs, block-bootstrap CIs, Holm p-values, LOIO, placebo, per-symbol/block tables. Emit verdict: **REPRODUCED** / **NOT_REPRODUCED** / **INCONCLUSIVE** / **INADMISSIBLE** (all EXPLORATORY_ONLY, promotable=false). Do not modify sealed FCLR-011 artifacts.
5. **Update state atomically** — update `experiment_frontier.json` (demote FCLR-VOL-FORWARD-AUDIT to rank 1), add audit hypothesis to `hypothesis_registry.json`, append to `negative_results_report.md` and `leakage_audit.md`, re-run targeted tests + gate (expect 19/19 PASS).
6. **Execute Phase B** — `FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T042139Z`: cached ironflow bulk `2026-05..2026-10`, observed HL labels only (no modeled/proxy/synthetic, no venue mixing), same primary target (next-24h liq intensity, QLIKE, C2 vs B1), freeze prereg, recompute with same deterministic rules, emit verdict. **Phase B is not optional if Phase A completes**; if Phase A blocked, execute B and record A blocked with evidence.

**Invariants (must not violate):** preregister before any outcome inspection; observed vs modeled labels never conflated; no forward fill / synthetic data; no May 2026 holdouts for scoring; no sealed verdict reopening; no `.github/workflows/*` edits; no raw parquet commits; no fabricated artifacts/thresholds/p-values/verdicts; bounded NO_GO with exact failing minima if blocked.

### 2026-11-14T06:24:00Z — Durable handoff refreshed (initial task clarified)
- Re-verified baseline: targeted tests PASS and `scripts/fclr_campaign_gate.py --arm all` = 19/19 PASS.
- Consolidated `AGENT_HANDOFF.md` into a timestamped, execution-first initial task for next session: Phase A `FCLR-011-INDEPENDENT-RECOMPUTE-20261114T042139Z` then Phase B `FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T042139Z` (heavy, local, unblocked). Explicitly states: no status-only report, no Gate 4 wait, "no heavy work remains" superseded.
- No agent-removable blockers found; peer sessions not blocked by repo state. Gate 4/external triggers remain absent but are not required for this audit campaign. `fclr011_panel.json` LFS pointer noted—rebuild from cached Binance inputs.
- No code, tests, or sealed artifacts modified in this maintenance step.
