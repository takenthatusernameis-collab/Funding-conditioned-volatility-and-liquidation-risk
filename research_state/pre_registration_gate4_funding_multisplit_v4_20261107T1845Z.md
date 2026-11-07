# Pre-Registration: Gate 4 Funding Multi-Split v4 (identity-verified 2024-04..09 slice)

**Experiment ID:** GATE4-FUND-VOL-ABLATIONS-MSPLIT-V4-30D
**Version:** v4 (bounded exploratory run allowed only after this freeze; confirmatory claim remains gated)
**Status:** FROZEN BEFORE OUTCOMES — 2026-11-07T18:45:00Z
**frozen_before_outcomes:** true
**git_sha:** 1ddb7d6c57e2cf10ace9fb11b9ddda26a6bcb428
**Authoring context:** Local admissible cache files only for outcome work; FCLR-015 identity/manifest used unauthenticated HTTPS to data.binance.vision for source comparison only (no auth, no paid data, no bypass). No outcome inspection/metrics before this freeze.
**Supersedes for execution only:** v3 design is reused structurally; v1/v2/v3 remain preserved and never overwritten. This v4 prereg governs only future runs that cite it explicitly.

## Objective
Evaluate, on an identity-verified local slice, whether funding features improve 24h forward realized-variance forecasts (QLIKE primary) beyond a direct-variance RV-only baseline under chronological splits with purge/embargo. Any run before this file was committed/frozen is not governed by v4. **Confirmatory claim = NO-GO by default** until all claim-worthiness, leakage, stability, and prereg criteria are satisfied and outputs are explicitly promoted under a separate authorized decision.

## Data (local, identity-verified, provenance recorded)
- **Instruments (5):** BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, BNBUSDT.
- **Slice:** 2024-04-01..2024-09-30 (calendar-day daily 1h Binance-archive-layout files + monthly fundingRate for 2024-04..09).
- **Cache location:** `research_state/data_cache/<SYM>_2024_MM/` (klines/index/mark/premium daily 1h zip/CSV files and fundingRate monthly files) — local files only for outcome computation.
- **Input manifest (source-of-truth for identity):** `research_state/fclr015_local_audit/fclr015_input_manifest_2024_04_09_20261107T180626Z.json`
  - **manifest_sha256:** `3e6ac26ce645b8b2f0c2fb495288c4880aa74b5b7e457e1e7c88fb7eb3f5406c`
  - **manifest_bytes:** 2842335
  - **files checked:** 3690
  - **identity result:** 3690/3690 MATCH vs Binance Vision; mismatch=0, missing_local=0, missing_remote=0, remote_error=0 (unauthenticated HTTPS, 2026-11-07T18:06Z run recorded in artifact). `cache_identity_vs_binance_vision=GO_SAMPLED_OR_PARTIAL` (scope complete for checked 2024-04..09); `confirmatory_claim_go=NO_GO` until this prereg freeze + admissibility/leakage/sufficiency gates.
- **Missing handling:** missing/unaligned observations remain NaN; never zero-filled. Basis/premium omitted unless an aligned admissible local series is verified and added by addendum before outcomes.
- **No outcome inspection before freeze:** no QLIKE/MAE/RMSE/CI/ablation outcome metrics were computed or inspected for v4 prior to this file.

## Boundary admissibility vs sealed anchors (non-consumed / non-confounded rationale)
- **FCLR-002 (sealed):** panel 2024-01-01..2024-09-30; **test 2024-07-23T00:00Z..2024-09-30T23:00Z** (7d embargo), 2×30d blocks → NOT_MET for claim-worthy. Anchor sha256 recorded in `AGENT_HANDOFF.md`/sealed records.
- **FCLR-003 (sealed):** panel 2024-01-01..2024-12-31; **test 2024-10-02T00:00Z..2024-12-31T23:00Z** (7d embargo), 3×30d blocks PASS for block count but forecast/confirmatory NOT_MET/CLOSED NEGATIVE per handoff. Anchor sha256 `a623d098caaa01404dcef22bd703eb2476a63f4602b789c81c4d56fa688f9ec2`.
- **FCLR-013 (sealed):** 2026-08-26..2026-09-30 test, 1×30d block NOT_MET; anchor sha256 `107bc981ebb6f519205b42f94ce778e14b445036f4758995914dabb0ef6bd08a`. Different calendar regime; not overlapped by 2024-04..09 slice.
- **v3 Gate 4 (preserved, exploratory/pilot lineage):** 2024-04..09 local cache with 4 expanding 30-day test blocks starting 2024-05-15; v3 outputs/manifests preserved, not overwritten.
- **v4 admissibility decision (this prereg):** The 2024-04..09 cache slice is the same calendar domain family used by FCLR-002/v3. Therefore **v4 may be used only as EXPLORATORY/NOT CONFIRMATORY/NOT PROMOTABLE** on this slice unless a future admissible boundary is preregistered that is materially non-overlapping/non-confounded with sealed confirmatory holdouts and claim-worthy. **Do not treat any v4 result on this slice as confirmatory, promotable, or as overlay/Track-A evidence.** If confirmatory evidence is later sought, preregister a distinct admissible boundary/window with explicit non-overlap proof vs FCLR-002/003/013/v3 sealed test windows before outcomes.

## Horizon / Target
- 24h forward realized variance target from 1h close-to-close returns; no lookahead.
- **Primary metric:** QLIKE (lower is better).
- **Secondary metrics:** MAE, RMSE (reported; not claim-bearing for primary unless pre-specified addendum).

## Splits (frozen, chronological, non-overlapping 30-day tests; reuse v3 structure for exploratory comparability)
All timestamps UTC. Purge/embargo >= 7 calendar days between train end and test start. Expanding train anchored at 2024-04-01.

| id | train_start | train_end | purge_gap_days | test_start | test_end | test_days |
|---:|---|---|---:|---|---|---:|
| 0 | 2024-04-01 | 2024-05-07 | 7 | 2024-05-15 | 2024-06-13 | 30 |
| 1 | 2024-04-01 | 2024-06-06 | 7 | 2024-06-14 | 2024-07-13 | 30 |
| 2 | 2024-04-01 | 2024-07-06 | 7 | 2024-07-14 | 2024-08-12 | 30 |
| 3 | 2024-04-01 | 2024-08-05 | 7 | 2024-08-13 | 2024-09-11 | 30 |

No tuning on test. Any chronology/leakage bug invalidates affected results.

## Ablations (pre-registered)
- **A_rv_only (baseline):** direct-variance OLS HAR on trailing RV features (rv_trail_24, rv_trail_168, rv_trail_6).
- **B_rv_signed:** A + funding_signed (last known at/before hour).
- **C_rv_abs:** A + funding_abs.
- **D_rv_signed_abs:** A + funding_signed + funding_abs.
- **E_rv_signed_abs_roll:** A + funding_signed + funding_abs + trailing/rolling funding stats (past-only).

## Contrasts / Uncertainty
- **Primary contrast (pre-registered):** E vs A, ΔQLIKE (alt-base) by split and aggregate exploratory summary; **not confirmatory** on this slice.
- **Secondary contrasts:** B/C/D vs A.
- **Uncertainty:** block bootstrap ΔQLIKE CIs, resampling whole UTC time blocks jointly across instruments (24h blocks primary; seed/reps in run manifest). MAE/RMSE reported with the same block logic where feasible.

## Leakage controls
- Chronological splits only; purge/embargo >= 7d.
- Train-only normalization/statistics per split.
- Funding merge uses last-known value at/before hour; no future funding.
- Targets forward-looking; evaluation uses realized targets only in designated windows.
- No random splits, no test tuning, no outcome-conditioned split changes.

## Sufficiency / verdict rules (frozen)
- **Exploratory smoke (authorized after this freeze):** bounded deterministic run, tmp/output-isolated, labeled `EXPLORATORY / NOT CONFIRMATORY / NOT PROMOTABLE`; may report metrics only under that label.
- **Confirmatory claim-worthy (NOT authorized on this slice by this prereg):** requires distinct admissible non-confounded boundary preregistered before outcomes, >=5 instruments, >=3 non-overlapping 30-day test blocks, clean leakage audit, stable pre-registered uncertainty, and no overlap/confounding with sealed confirmatory holdouts. If not met: verdict **PILOT/INCONCLUSIVE/NO-GO**.

## Outputs (versioned; never overwrite sealed anchors)
- Future exploratory run artifacts must include `v4`, `EXPLORATORY`, UTC timestamp, git SHA, and manifest sha256 in filename/metadata; store under non-canonical exploratory paths (e.g., `research_state/exploratory_v4_*` or `results/exploratory_v4_*`) unless explicitly authorized otherwise.
- **Never overwrite:** `research_state/evaluation_summary_FCLR002.md`, `evaluation_summary_FCLR003.md`, `evaluation_summary_FCLR-013.md`, `run_manifest.json`, `run_manifest_FCLR002.json`, `run_manifest_funding_v3_30d.json` sealed contents, or any file whose sha256 is recorded as a sealed anchor without explicit authorization.

## Deviations
Any deviation from instruments, slice, manifest, splits, ablations, metrics, leakage controls, or labeling must be recorded in the run manifest and treated as non-confirmatory.
