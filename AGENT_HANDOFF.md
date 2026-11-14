# AGENT HANDOFF — 2026-11-14T04:21:39Z (single durable handoff)

## INITIAL TASK FOR NEXT SESSION — EXECUTE PHASE A NOW (HEAVY, LOCAL, UNBLOCKED)

**Campaign:** `FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z`
**Phase A (P0, mandatory):** `FCLR-011-INDEPENDENT-RECOMPUTE-20261114T042139Z`

**Do not emit a status-only report. Do not wait for Gate 4. Do not reuse the old "no heavy work remains" directive; it is superseded.** The next session must execute Phase A end-to-end, then Phase B. If a phase is genuinely blocked, emit a bounded NO_GO with the exact failing minimum and proceed to the other phase; do not stop at a narrative.

### Why this is the highest-value task

The repository is *Funding-conditioned Volatility and Liquidation Risk*. The program has exactly two positive results:

1. **FCLR-011 volatility PASS** — C2 vs B1 relative QLIKE reduction **4.94%**, 95% CI **[-0.032546, -0.001418]**, 5 instruments, 3 non-overlapping 30-day blocks, test **2026-05-08..2026-08-06**.
2. **Track A liquidation expansion PASS** — C2 vs B1 **19.04%** QLIKE reduction on 8 Hyperliquid symbols, 2026-05..2026-10, 593 paired rows; robustness is **FRAGILE** (LOIO 4/8, placebo FAIL).

FCLR-011 is the sole volatility gate PASS, but it failed every later out-of-sample test: 2024 H2 -20.77%, 2025 H2 -8.97%, 2025 Q1-Q2 +0.23%, 2026 Q1-Q2 -0.89%, and forward 2026-08..10 -5.55%. The 2026-11-04 "recompute audit" is not a clean independent check: it used the heuristic `run_trackc_*` scripts, reported +6.86% rather than the sealed +4.94%, and `research_state/data_cache/fclr011_panel.json` is now an unresolved Git-LFS pointer. The sole positive therefore remains unresolved. This is a local, unblocked, high-information task that cannot be satisfied by another trigger-only NO_GO.

### Step 0 — Verify the baseline (cheap; do not redo heavy cells)

```bash
git status --porcelain
python3 -m venv /tmp/fclr-venv          # only if missing
/tmp/fclr-venv/bin/pip install -r requirements.txt
/tmp/fclr-venv/bin/python -m unittest \
  tests.test_active_campaign_gate tests.test_tracka_hardening_099 \
  tests.test_fclr_canonical_artifacts tests.test_fclr_final_structural_closure \
  tests.test_fclr_campaign_gate
/tmp/fclr-venv/bin/python scripts/fclr_campaign_gate.py --arm all
```

Expected after this handoff: targeted tests pass, campaign gate **19/19 PASS**. Record the exact output in the session log. Do not edit `.github/workflows/*`.

Record SHA-256 of the sealed inputs before touching anything:

```bash
sha256sum research_state/evaluation_summary_FCLR-011.md \
          research_state/evaluation_summary_FCLR-011_20261103T111743Z.md \
          research_state/pre_registration_fclr011_20261103T111501Z.md
```

### Step 1 — Freeze the Phase A prereg before any outcome computation

Create `research_state/prereg_fclr011_recompute_20261114T042139Z.json` (and a matching `.md`) with:

- `experiment_id = FCLR-011-INDEPENDENT-RECOMPUTE-20261114T042139Z`
- `campaign = FCLR-FUND-VOL-LIQ-REDTEAM-20261114T042139Z`
- `status = FROZEN_PRE_OUTCOMES`
- `frozen_before_outcomes = true`, `pre_registered_before_outcomes = true`, `outcome_data_inspected_before_freeze = false`
- `promotable = false`, `max_status = EXPLORATORY_ONLY`, `audit_only = true`
- `does_not_reopen_sealed_verdict = true`

Freeze these exact splits (from the sealed FCLR-011 summary):

- Train: `2026-01-01T00:00:00Z .. 2026-03-17T23:00:00Z`
- Validation: `2026-03-25T00:00:00Z .. 2026-04-30T23:00:00Z`
- Test: `2026-05-08T00:00:00Z .. 2026-08-06T23:00:00Z`
- 7-day purge/embargo at both boundaries.

Freeze the design:

- Universe: `BTCUSDT, ETHUSDT, BNBUSDT, SOLUSDT, XRPUSDT`.
- Target: next-24h realized variance of mark-price returns, sum of squared log returns over `t+1..t+24`.
- Models: B0 persistence (`log RV24h`); B1 HAR (`log RV1h`, `log RV24h`, `log RV168h`); C1 = B1 + signed funding + trailing 90-day absolute-funding percentile (minimum 30 prior observations); C2 = C1 + mark/index premium + mark/EMA24 distance.
- Fit: OLS on `log(RV + 1e-12)`, training-only mean/std scaling, documented training-only smearing back-transform.
- Missing data: **no zero-fill and no forward-fill**. Use explicit missingness rules; paired comparisons use the common eligible rows; report coverage and exclusions by symbol/feature.
- Primary metric: paired out-of-sample QLIKE, C2 vs B1; secondary MAE/RMSE.
- Inference: paired circular block bootstrap over complete UTC time blocks, 24h blocks, 2,000 deterministic replicates; Holm across the three registered contrasts (`C2_vs_B1`, `C1_vs_B1`, `C2_vs_C1`); LOIO; funding-permutation placebo; per-symbol and per-block stability; leakage audit.
- Stop rule: if instruments < 5, test blocks < 3, or core coverage is insufficient, emit a bounded `INADMISSIBLE`/`INCONCLUSIVE` NO_GO with exact failing minima; do not relax thresholds after seeing outcomes.

### Step 2 — Rebuild the panel from raw cached inputs

Do not rely on the LFS pointer `research_state/data_cache/fclr011_panel.json`. Rebuild from the cached Binance archive:

- `research_state/data_cache/{SYM}_2026_MM` for `2026-01..2026-08`.
- Use `markPriceKlines`, `indexPriceKlines`, `premiumIndexKlines`, `klines`, and `fundingRate` as available.
- UTC-normalize timestamps; preserve source values; deduplicate; record input file hashes.
- Compute causal features at each closed hour; compute the forward target only from strictly future bars.
- Emit `research_state/fclr011_recompute_panel_20261114T042139Z.parquet` plus `research_state/fclr011_recompute_panel_build_report_20261114T042139Z.json` with input hashes, row counts before/after each filter, coverage by symbol/feature, split boundaries, and panel SHA-256.

If the LFS object is available, also verify its hash against the recorded OID and report whether the rebuilt panel matches; do not silently overwrite it.

### Step 3 — Run the independent evaluation and emit the verdict

Implement or extend a deterministic script (for example `scripts/fclr011_recompute_audit.py`) that:

1. Asserts the frozen prereg fields.
2. Builds the panel from the cached inputs.
3. Fits B0/B1/C1/C2 on train only.
4. Evaluates the frozen test block.
5. Computes QLIKE, MAE/RMSE, paired differences, block-bootstrap CIs, Holm-adjusted p-values, LOIO, placebo/permutation, and per-symbol/per-block tables.
6. Emits `research_state/evaluation_summary_FCLR-011-RECOMPUTE-20261114T042139Z.json` and `.md`.

The verdict must be one of:

- `REPRODUCED` — independent recomputation is directionally and materially consistent with the sealed +4.94% result under the frozen design.
- `NOT_REPRODUCED` — the independent recomputation fails to reproduce the sealed result.
- `INCONCLUSIVE` — data, coverage, or numerical limits prevent a clean verdict.
- `INADMISSIBLE` — frozen minimums are not met.

Every verdict is `EXPLORATORY_ONLY` / `promotable=false`; this is an audit, not a promotion. Do not modify, overwrite, or re-score the sealed FCLR-011 artifacts. If the audit contradicts the sealed result, record the contradiction as a new finding in `hypothesis_registry.json`, `negative_results_report.md`, and this handoff; leave the sealed record intact.

### Step 4 — Phase B: liquidation expansion red-team (required after Phase A)

Campaign ID: `FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T042139Z`.

Independently recompute the sealed Track A liquidation expansion PASS and its FRAGILE robustness result:

- Data: cached ironflow bulk `2026-05..2026-10`, observed Hyperliquid liquidation labels only; no modeled/proxy/synthetic labels; no venue mixing.
- Primary target: next-24h observed liquidation intensity, QLIKE, C2 vs B1, matching the sealed expansion design for direct comparability.
- Freeze a new prereg before any outcome computation, with the same leakage, embargo, complete-case, and deterministic-bootstrap rules.
- Emit `research_state/evaluation_summary_TRACKA-LIQ-EXPANSION-RECOMPUTE-<UTC>.json` and `.md` with QLIKE, CI, LOIO (minimum 6/8), placebo, per-symbol/per-block stability, and exact failing minima.
- Preserve the sealed expansion PASS and the prior FRAGILE robustness record. Do not promote. If the recomputation fails, record `NOT_REPRODUCED` or `FRAGILE`; if it passes, it remains `EXPLORATORY_ONLY` because the prior robustness gate failed.

Phase B is not optional if Phase A completes. If Phase A is blocked by data, execute Phase B and record Phase A as blocked with evidence.

### Step 5 — Update state atomically

After each phase:

- Update `research_state/experiment_frontier.json`: rank-0 entry reflects the active campaign; demote the completed `FCLR-VOL-FORWARD-AUDIT-20261114T032041Z` to rank 1; record exact artifact paths/hashes and verdicts.
- Add a new audit hypothesis to `research_state/hypothesis_registry.json` (do not alter sealed FCLR-011 or Track A expansion statuses).
- Append to `research_state/negative_results_report.md` and `research_state/leakage_audit.md`.
- Update this handoff with a timestamped session log, exact commands, results, and the next action.
- Re-run the targeted tests and `scripts/fclr_campaign_gate.py --arm all`; record exact outcomes.

## NEXT FOCUS CAMPAIGN (ordered, no skipping)

1. **Phase A — `FCLR-011-INDEPENDENT-RECOMPUTE-20261114T042139Z`:** freeze prereg, rebuild panel from cache, independent OLS/HAR recomputation, emit verdict. Mandatory.
2. **Phase B — `FCLR-LIQ-EXPANSION-RECOMPUTE-20261114T042139Z`:** freeze prereg, recompute the sealed liquidation expansion PASS and FRAGILE robustness, emit verdict. Mandatory after A.
3. **Only after both phases:** if a valid Gate 4 `fclr016_v5_terms_evidence_RESOLVED_<UTC>.json` (`status=RESOLVED_VERIFIED`, `fabricated=false`, human/legal attestation) or a materially new admissible observed-liquidation source appears, execute the corresponding trigger-only path. Do not wait or poll for triggers.

## Invariants

- Preregister before any outcome inspection or evaluated-target build for a new cell.
- Observed labels and modeled/proxy labels are never conflated; no venue mixing; no forward fill or synthetic data.
- Do not read May 2026 or sealed holdouts for scoring/decisions; do not reopen terminal verdicts; do not overwrite sealed artifacts.
- No `.github/workflows/*` edits; do not commit raw parquet/caches.
- Do not fabricate artifacts, thresholds, p-values, or verdicts. Bounded NO_GO with exact failing minima if blocked.
- The root artifact guard is now tracked-baseline + untracked-file based; do not delete evidence to make a count pass. If the count grows, commit durable artifacts and update the hard cap with evidence.

## Current state summary (verified 2026-11-14T04:21:39Z)

- Baseline targeted tests pass after the guard repair; campaign gate 19/19 PASS.
- `FCLR-VOL-FORWARD-AUDIT-20261114T032041Z` is complete/validated (`EXPLORATORY_NULL`, `VALID_EXPLORATORY`) and is demoted to rank 1.
- The old trigger-only directive is superseded: there is unblocked local heavy work (Phase A/B).
- Gate 4 external/legal trigger remains absent; it is not required for this exploratory audit.
- No peer sessions are blocked. Bottlenecks removed: stale "no heavy work" handoff, hardcoded active-campaign test, and the artifact-count guard.

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