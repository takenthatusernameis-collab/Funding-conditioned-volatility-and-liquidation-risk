# AGENT HANDOFF — Durable Single Source of Truth for Next Session

**Generated (UTC):** 2026-11-26T22:00:21Z
**Program status:** ACTIVE — `FCLR-LIVE-ARCHIVE-07-20261126T153244Z` is rank-0 `READY_EXECUTE` with the CORRECTED, verified-feasible common-support design (see §0).
**HEAD:** `39eee67a1`
**Working tree:** clean
**Latest completed heavy session:** `session_20261126T133828Z` (campaign-06, `NOT_SUPPORTED`, `all_checks_match=true`)
**Heavy-work gate at this refresh:** `pass=true`, `reason_code=OK`, `failures=[]` (green only because the newest on-disk session `20261126T133828Z` predates the campaign start `20261126T153244Z`; the first post-start session that lacks the full heavy set fails closed).

> This is the sole durable handoff. A timestamp-only rewrite, a new empty session directory, a prereg-only run, an audit-only run, a trigger-only run, a source-registry-only run, or a verify-and-stop run is a failed next session. The next session must execute the heavy campaign in §1–§3.

---

## 0. BOTTLENECK RESOLVED AT THIS REFRESH (read first)

The previous campaign-07 attempt at `20261126T153717Z` was **quarantined intact** to `handoff_archive/quarantine_20261126T163207Z/` (do not reuse its outputs). Its failure was **not** a missing cache and **not** a missing template. It was a **degenerate split** caused by unequal per-symbol 1h coverage interacting with the frozen *pooled* "60/20/20 by unique UTC timestamp" rule:

- The 2024-04..2026-10 five-symbol cache is complete in **date range** (all five symbols span 2024-04-01..2026-11-07) but **gappy in 1h density**: BNBUSDT/SOLUSDT/XRPUSDT carry ~8,976 one-hour mark rows each, ETHUSDT ~16,272, BTCUSDT ~21,360.
- The frozen pooled split takes the latest ~20% of the **BTCUSDT-dominated** pooled timestamp axis as the test block. In that window only BTCUSDT is dense, so the test set collapsed to BTCUSDT only (`n_test=4368`, leave-one-symbol-out contained only BTCUSDT), the block bootstrap produced absurd intervals (`[-1.8e12%, …]`), the independent recompute reported `all_checks_match=false`, and required audit/trigger artifacts were absent. That is why it was quarantined.

**Resolution (the single design correction, verified feasible on the real cache):** restrict the pooled panel to the **common support** `S` = the set of UTC hourly timestamps at which **all five** symbols have a mark-price close > 0, *before* applying the frozen split. On the current cache `|S| = 8,976` (BNBUSDT/SOLUSDT/XRPUSDT are the binding 8,976-row series; BTCUSDT/ETHUSDT are supersets on `S`). Under the unchanged 60/20/20 + 168h embargo this yields **train≈5,217 / val≈1,795 / test≈1,964 timestamps ≈ 9,820 test rows across all five symbols** — non-degenerate, every block and every leave-one-symbol-out fold contains all five symbols. This changes **only the cohort support**, not the estimand, models, floor, alpha, Holm family, bootstrap, or verdict rule. The next session must recompute `S` from the cache and freeze `|S|` and the split sizes in the outcome-blind prereg.

**Do not** re-run the unfiltered pooled split (that is the quarantined failure mode). **Do not** zero-fill, silently substitute, re-download, or inspect outcomes before the prereg is frozen. The cache is sufficient as-is; no network and no package installation are required.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (UTC 2026-11-26T22:00:21Z)

**EXECUTE `FCLR-LIVE-ARCHIVE-07-20261126T153244Z` NOW under one fresh session_<UTC>/ (id lexicographically > `20261126T153244Z`), using the corrected common-support design in §0 and §3.** The repository name leads with **Funding-conditioned-volatility**, so the highest-value unfinished work is the pre-registered disjoint-cohort replication of the repo-name primary estimand: **next-24h mean log-realized-variance QLIKE, C2 versus B1**, on the untouched 2024-04 through 2026-10 cohort for `BNBUSDT`, `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT`. This is sequential confirmatory look `k=2` with frozen `alpha_2 = 0.05/(2*3) = 0.008333`. The declared Holm secondary is the campaign-06 estimand: next-24h downside realized-semivariance level, judged by MSE. Do not substitute another estimand, cohort, threshold, or model search.

**No setup or gate-repair step is required first.** The heavy-work gate passed at this refresh (`pass=true`, `reason_code=OK`, `failures=[]`); `research_state/experiment_frontier.json` rank-0 is `READY_EXECUTE`; the five-symbol 2024-04..2026-10 cache and the stdlib template are on disk. `scripts/next_campaign_status.py` may still print its obsolete "no feasible 3-block design in ANY domain" line; that message is a known non-blocker and does **not** block campaign-07, which uses a feasible 60/20/20 chronological split with three test blocks on the common-support cache. Do not let that legacy line stall the run.

### Mandatory execution sequence

1. Create exactly one fresh `research_state/session_<UTC>/` whose id is lexicographically greater than `20261126T153244Z`. Do not reuse or cite any aborted attempt (the quarantined `20261126T153717Z` and `20261126T144850Z` attempts are invalid evidence).
2. Copy `handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py` into that new session directory. Set `SESSION` to the fresh UTC id and `CAMPAIGN_START` to `20261126T153244Z`. Running it from the quarantine directory is invalid (wrong relative cache path); running the copied script from `research_state/session_<UTC>/` resolves `../data_cache` correctly.
3. **Apply the §0/§3 common-support filter in `build_symbol_panel` (or immediately after panel assembly, before pooling):** retain only rows whose timestamp `t` is in the all-five-symbol hourly intersection `S`. Recompute `S` from the cache; record `|S|`, per-symbol 1h counts, and the resulting train/val/test timestamp and row counts.
4. Reuse `research_state/data_cache/<SYM>_<YYYY_MM>/` read-only. Verify every consumed zip against its `.sha256` sidecar and `research_state/cached_inputs_hashes.json`; record exact coverage, layout, and any shortfall. Do not zero-fill, silently substitute, re-download, or inspect outcomes before the prereg is frozen.
5. Produce the complete artifact set in §2 under that one fresh session directory. Every file must be non-empty; every JSON must carry the real `session_id` and experiment id. No root-level `research_state/*.md` or `*.json` files: the root is at its 500-file cap.
6. Run the heavy evaluation and an independent stdlib recompute. The recompute must reproduce the verdict with `all_checks_match=true`; the evidence audit must have `audit_pass=true` and no unresolved blocker. A valid `NOT_SUPPORTED` result is acceptable; placeholders and fabricated agreement are not. The recompute must independently rebuild `S` and confirm the test set contains all five symbols with `n_test >= 500`.
7. Only after the artifacts exist, update `research_state/experiment_frontier.json` and this handoff. Set rank-0 to `COMPLETED_VALIDATED`, record the reproduced verdict and completed session, demote campaign-07 to a non-zero rank, and promote the next materially distinct unfinished task without reopening a closed arm.
8. Finish only when the verification in §4 passes. If any required artifact is missing or empty, the session is incomplete.

---

## 2. REQUIRED HEAVY ARTIFACTS — SAME FRESH SESSION

- `fclr_live_archive07_source_registry_<UTC>.{json,md}` — exact cache paths, per-file SHA-256 results, coverage per symbol/dataset, layout notes, the common-support `S` definition and `|S|`, and read-only reuse statement.
- `fclr_live_archive07_prereg_<UTC>.{json,md}` — outcome-blind, hash-bound to the source registry, with `outcome_data_inspected_before_freeze:false`, look `k=2`, `alpha_2=0.008333`, and the frozen `|S|` / split sizes.
- `fclr_live_archive07_eval_<UTC>.{py,json,md}` — heavy three-block evaluation implementing the frozen design on the common support, at least 2,000 deterministic block-bootstrap replicates, per-block diagnostics, and leave-one-symbol-out diagnostics (all five symbols present in every fold).
- `fclr_live_archive07_recompute_<UTC>.{py,json}` — independent stdlib recompute with `all_checks_match:true` and reproduced verdict; independently rebuilds `S`.
- `fclr_live_archive07_evidence_audit_<UTC>.{json,md}` — leakage/evidence audit with `audit_pass`, verdict, and `unresolved_blockers`.
- `evidence_audit_<UTC>.{json,md}` — substantive gate-critical alias matching the verdict.
- `trigger_check_<UTC>.json` — `external_trigger_required:false`, `trigger_source:"BINANCE_PUBLIC_ARCHIVE"`, `fired:false`.
- `_headline_<UTC>.json` — concise headline metrics for independent gate validation.

---

## 3. FROZEN DESIGN — DO NOT RE-DERIVE OR THRESHOLD-SHOP

1. **Cohort / support:** 2024-04-01 through 2026-10-31 UTC; exactly the five symbols above; **restricted to the common support `S`** = UTC hourly timestamps where all five symbols have a mark-price close > 0 (the §0 correction; `|S|=8,976` at this refresh, to be recomputed and frozen in the prereg). This is disjoint from the 2021-2024 cohort used by campaigns 01–06.
2. **Primary target:** `y = log(RV_24h_next + 1e-09)` from one-hour mark-price log returns; metric is out-of-sample QLIKE.
3. **Declared secondary:** `log(RV_minus_next24h + 1e-09)`; metric is MSE. The Holm family is exactly these two targets.
4. **B1:** fixed signed-HAR history set used by campaigns 05/06: log RV1h/RV24h/RV168h plus log RV_plus/RV_minus at 24h/168h.
5. **C2:** B1 plus signed funding(24h), trailing 90-day absolute-funding percentile, mark/index premium, and mark/EMA24 distance. All scaling is train-only.
6. **Split:** 60/20/20 by unique UTC timestamp **on `S`**, 168-hour purge/embargo, three chronological test blocks.
7. **Models:** fixed-form deterministic stdlib OLS only. No regularization, model-family search, feature search, or threshold tuning.
8. **Inference:** at least 2,000 fixed-seed block-bootstrap replicates, preserving complete UTC blocks jointly across symbols; report per-block and leave-one-symbol-out concentration diagnostics.
9. **Verdict:** `PROMOTED` requires primary C2-versus-B1 relative QLIKE reduction of at least 2%, a 95% bootstrap CI lower bound above zero at the look-`k=2` alpha, and a consistent Holm-adjusted secondary direction. Otherwise preserve `NOT_SUPPORTED`; use `INCONCLUSIVE` only when the evidence supports neither conclusion.

The cache and numerical template are feasible today. Campaign-06 completed the full stdlib-only heavy set with `all_checks_match=true`; campaign-07 uses the same numerical approach on the common-support disjoint cohort and later regime.

---

## 4. VERIFICATION COMMANDS — RUN AT START AND END

```bash
export UTC=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p research_state/session_$UTC
python3 scripts/check_handoff_heavywork_gate.py --json
python3 -m py_compile scripts/check_handoff_heavywork_gate.py
python3 -m unittest \
  tests.test_vol_jump_campaign_gate tests.test_vol_stress_campaign_gate \
  tests.test_vol_corr_campaign_gate tests.test_vol_broad_campaign_gate \
  tests.test_tracka_hardening_143 tests.test_active_campaign_gate
python3 -m json.tool research_state/experiment_frontier.json >/dev/null
git diff --check
```

After the heavy session, the gate must report top-level `pass=true`, `reason_code=OK`, `failures=[]`, and `live_archive.required=true`, `live_archive.pass=true`, `artifact_family="live_archive07"`, with empty missing/empty artifact lists. The six-module unittest command must pass. Do not chase the pre-existing legacy Track A modules that require absent numpy/pandas/pyarrow; package installation is forbidden.

---

## 5. COMPLETED SESSION RECORD — `session_20261126T133828Z`

**Campaign:** `FCLR-LIVE-ARCHIVE-06-20261126T083526Z`
**Verdict:** `NOT_SUPPORTED` — C2 versus B1 relative test-MSE reduction `0.716%`, 95% block-bootstrap CI `[0.419%, 1.020%]`, below the frozen 2% floor.
**Independent recompute:** `all_checks_match=true`; `n_test=35715`; `n_unique_timestamps=34872`.
**Evidence audit:** `audit_pass=true`; `unresolved_blockers=[]`.

Complete artifact set (under `research_state/session_20261126T133828Z/`; do not re-run campaign-06):

- `fclr_live_archive06_source_registry_20261126T133828Z.{json,md}`
- `fclr_live_archive06_prereg_20261126T133828Z.{json,md}`
- `fclr_live_archive06_eval_20261126T133828Z.{py,json,md}`
- `fclr_live_archive06_recompute_20261126T133828Z.{py,json}`
- `fclr_live_archive06_evidence_audit_20261126T133828Z.{json,md}`
- `evidence_audit_20261126T133828Z.{json,md}`
- `trigger_check_20261126T133828Z.json`
- `_headline_20261126T133828Z.json`

---

## 6. FRONTIER AND NON-AVOIDANCE CONSTRAINTS

- Closed and not re-runnable: campaigns 01/03/04/05/06 on the five-symbol archive; broad ironflow VOL-BROAD/VOL-CORR/VOL-STRESS/VOL-JUMP arms; the terminal liquidation-risk program on the frozen ironflow panel.
- Do not build a risk overlay: the forecast gate has not passed.
- Do not wait for an external trigger; campaign-07 requires no network and no new source.
- Do not modify `.github/workflows`, sealed protocols, raw caches, or prior frozen artifacts.
- Stdlib only for campaign-07. No package installation.
- Do not create a second active handoff or a status-only session. The next session's purpose is the complete heavy evaluation, independent reproduction, and synchronized frontier.
- **Machine-enforced non-avoidance:** `scripts/check_handoff_heavywork_gate.py` binds campaign-07 to the `fclr_live_archive07_*` artifact family plus `evidence_audit_<UTC>.{json,md}` and `trigger_check_<UTC>.json` in the newest session. A trigger-only, prose-only, audit-only, prereg-only, source-registry-only, verify-and-stop, or zero-byte-placeholder session fails closed. The gate is green now only because the newest on-disk session predates the campaign start; the first post-start session that lacks the full heavy set will fail.
- **Single durable handoff:** update this file and `research_state/experiment_frontier.json` only after the heavy artifacts exist and verify. Do not create root-level `research_state/*.md`/`*.json` files (root at 500-file cap).

**Highest-value next action:** execute campaign-07 exactly as frozen above, on the common support `S`.
**Dominant limitation to disclose:** only five symbols are available in the disjoint cohort and their 1h coverage is unequal, so the common-support restriction and per-block + leave-one-symbol-out diagnostics are mandatory.
**Concrete falsification test:** C2 improves relative test QLIKE by at least 2% with the frozen uncertainty and Holm conditions on the untouched common-support cohort.

**END OF HANDOFF — 2026-11-26T22:00:21Z**