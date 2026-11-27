# AGENT HANDOFF — Durable Single Source of Truth for Next Session

**Generated (UTC):** 2026-11-27T03:55:00Z
**Program status:** ACTIVE — `FCLR-LIVE-ARCHIVE-07-20261126T153244Z` is rank-0 `READY_EXECUTE`.
**HEAD:** `156d64aea`
**Working tree:** clean; this header refresh (generated time + HEAD only) is the only intended diff. The durable body below (§0–§6) is unchanged.
**Single source of truth:** this file is the ONLY durable handoff. The former root `INITIAL_TASK_MESSAGE_20261127T021343Z.md` and `INITIAL_TASK_MESSAGE_20261127T025859Z.md` were duplicates of §1 and have been moved to `handoff_archive/` — do not resurrect them; read §1 below.
**Latest completed heavy session:** `session_20261126T133828Z` (campaign-06, `NOT_SUPPORTED`, `all_checks_match=true`)
**Heavy-work gate at this refresh:** `pass=true`, `reason_code=OK`, `failures=[]`, `handoff_stale=false`, `live_archive.required=false`, `live_archive.pass=true`, `live_archive.campaign_id=FCLR-LIVE-ARCHIVE-07-20261126T153244Z` (green ONLY because the newest on-disk session `20261126T133828Z` predates the campaign start `20261126T153244Z`; the first post-start session that lacks the full heavy set fails closed — the gate is armed).

> This is the sole durable handoff. A timestamp-only rewrite, a new empty session directory, a prereg-only run, an audit-only run, a trigger-only run, a source-registry-only run, or a verify-and-stop run is a failed next session. The next session must execute the heavy campaign in §1–§3.

---

## 0. BOTTLENECK STATUS (read first — no open bottleneck at this refresh; one prior bottleneck stays removed, one number stays corrected)

**No session is blocked and no setup/gate-repair step is required at 2026-11-27T03:53:23Z.** The heavy-work gate is green (and armed), `experiment_frontier.json` rank-0 is `READY_EXECUTE`, the five-symbol 2024-04..2026-10 mark-price cache is on disk, and the stdlib recovery template compiles (`py_compile` OK). The only open item is the un-started campaign-07 heavy session itself; that is the work, not a bottleneck.

**Bottleneck removed at the 2026-11-27T03:06:12Z refresh (ambiguity, not compute, still in force):** two competing root-level `INITIAL_TASK_MESSAGE_*.md` files duplicated §1 and created a "which message is authoritative?" stall for the next agent. Both are archived in `handoff_archive/` and this file is the single durable handoff. There is exactly one initial task message (§1); do not create another.

**One implementation trap is removed here so the next session cannot stall or silently build an unbalanced panel:** the recovery template's price loop is zip-only and predates the three on-disk layouts. Replace that loop with a recursive `markPriceKlines-*` CSV/ZIP reader (any depth, dedup by `open_time`, `close>0`), and apply the all-five-symbol support `S` to the aligned raw mark/index series **before** computing returns, rolling history, or forward targets. Merely filtering the final pooled rows is insufficient: a lookback or next-24h target window could still cross the XRPUSDT 2025-10-19 gap. This is an implementation clarification of the frozen common-support design, not a new estimand or threshold.

**The prior handoff's central number was WRONG and is corrected here by direct measurement of the on-disk cache.** Prior handoffs claimed `|S| = 22,608` with "all five symbols IDENTICAL / balanced / none binds." Independent recompute (mark-price only, all three layouts, deduped by `open_time`, restricted to the campaign window `2024-04-01 00:00 .. 2026-10-31 23:00 UTC`) gives:

- **BNBUSDT = BTCUSDT = ETHUSDT = SOLUSDT = 22,608** one-hour mark-price closes each in-window.
- **XRPUSDT = 22,584** — it is the **binding series, short by exactly 24 hours**.
- **True common support `|S| = 22,584`** (the all-five-symbol hourly intersection). Freeze this exact value in the outcome-blind prereg; do NOT hard-code 22,608.
- **Cause of the 24h shortfall (verified, not a missing file):** `research_state/data_cache/XRPUSDT_2025_10/markPriceKlines-2025-10-19/XRPUSDT-1h-2025-10-19.csv` contains **24 rows with NEGATIVE close values** (e.g. `-0.00054414`) for `2025-10-19 00:00..23:00 UTC`. Mark price cannot be negative; this is corrupt source data. **Quarantine and record it with provenance; do NOT zero-fill, repair, or silently substitute.** Excluding `close<=0` (already required) removes exactly those 24 hours, so `S` is the clean intersection.
- **The panel is still effectively balanced:** every 60/20/20 block and every leave-one-symbol-out fold contains all five symbols; the only effect of the XRP gap is that one UTC day is absent from the common support. There is **no degenerate-split risk**.
- **Embargoed 60/20/20 split on `S` (168h purge), `|S| = 22,584`:** train ≈ 13,550 ts / val ≈ 4,517 ts / test ≈ 4,517 ts ≈ **22,585 test rows across all five symbols**; three chronological test blocks of ≈1,500 ts (≈7,500 rows) each, all five symbols present in every block.

**Do NOT hard-code 22,608 and do NOT claim "all five identical." Recompute `S` from the cache (mark-price only) and freeze the real `|S| = 22,584`, the per-symbol counts (four at 22,608, XRPUSDT at 22,584), and the split sizes in the prereg.**

**Independent re-verification recorded at 2026-11-27T02:56:07Z and carried forward unchanged at this 2026-11-27T03:09:26Z refresh (stdlib, mark-price-only, all three layouts, dedup by `open_time`, `close>0`, window 2024-04-01 00:00 .. 2026-10-31 23:00 UTC):** BNBUSDT=BTCUSDT=ETHUSDT=SOLUSDT=**22,608** clean 1h closes each; XRPUSDT=**22,584** (exactly 24 nonpositive closes, all on `2025-10-19`); all-five intersection **`|S| = 22,584`**. This reproduces the numbers above from the raw cache and supersedes every earlier `|S|=8976` / "BNBUSDT binds" / "all five identical 22,608" claim. The next agent must still recompute `S` in-session and freeze the exact value in the prereg; do not treat this note as a substitute for the in-session recompute.

### Cache layout heterogeneity — the one rule the next agent MUST follow

The mark-price 1h data is stored in **three different layouts** across the window, and the month directories ALSO contain a **separate regular-klines stream** that must NOT be confused with mark price:

1. `2024_04`..`2024_09`: extracted nested CSVs at `markPriceKlines-<date>/<SYM>-1h-<date>/<SYM>-1h-<date>.csv`.
2. `2024_10`..`2024_12`: extracted CSVs at `markPriceKlines-<date>/<SYM>-1h-<date>.csv` (one level flatter; a same-day `.zip` duplicate also sits beside the `.csv`).
3. `2025_01`..`2026_10`: extracted CSVs under `markPriceKlines-<date>/...` **plus** top-level `<SYM>-1h-<date>.zip` files.

**Critical:** the top-level `<SYM>-1h-<date>.zip` files are **regular klines (price)**, NOT mark price — verified: for `BNBUSDT 2025-01-01` the top-level zip close is `709.15170927` while the `markPriceKlines` CSV close is `709.01083122`. **Use ONLY `markPriceKlines-*` mark-price CSVs (any depth). Never fold the top-level `<SYM>-1h-*.zip` klines into the mark-price panel.** Dedup by `open_time` (ms) so the same-day `.zip`/`.csv` duplicates and any overlapping hours do not double-count (measured ~2,352 duplicate `open_time` overwrites per symbol across the full cache — dedup is mandatory).

### Two verification-format facts the source registry MUST record

- **`.sha256` sidecars are hash-only** (a single 64-hex line, no filename). `sha256sum -c <sidecar>` fails with "no properly formatted checksum lines." Verify each consumed file by computing `sha256sum <file>` and comparing the digest to the sidecar's single line (and to `research_state/cached_inputs_hashes.json`).
- **`research_state/cached_inputs_hashes.json` is nested:** top-level `{count, derivation_notes, generated_at, hashes}` with **20,694 entries under `hashes`** keyed by repo-relative path. Look up `d["hashes"][path]`, not `path in d`.

The prior quarantined attempts (`20261126T153717Z` → `handoff_archive/quarantine_20261126T163207Z/`, and `20261126T144850Z` → `handoff_archive/quarantine_20261126T144850Z/`) are invalid evidence — do not reuse their outputs. The recovery template at `handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py` compiles and is the correct starting point; **copy it into the fresh session and add the mark-price-only `S` filter (with the `close>0` / XRP 2025-10-19 quarantine) before pooling.**

**Do not** zero-fill, silently substitute, re-download, or inspect outcomes before the prereg is frozen. The cache is sufficient as-is; no network and no package installation are required.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (UTC 2026-11-27T03:55:00Z)

**EXECUTE `FCLR-LIVE-ARCHIVE-07-20261126T153244Z` NOW under one fresh `session_<UTC>/` (id lexicographically > `20261126T153244Z`), using the corrected balanced common-support design in §0 and §3.** The repository name leads with **Funding-conditioned-volatility**, so the highest-value unfinished work is the pre-registered disjoint-cohort replication of the repo-name primary estimand: **next-24h mean log-realized-variance QLIKE, C2 versus B1**, on the untouched 2024-04 through 2026-10 cohort for `BNBUSDT`, `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT`. This is sequential confirmatory look `k=2` with frozen `alpha_2 = 0.05/(2*3) = 0.008333`. The declared Holm secondary is the campaign-06 estimand: next-24h downside realized-semivariance level, judged by MSE. Do not substitute another estimand, cohort, threshold, or model search.

**No setup or gate-repair step is required first.** `scripts/next_campaign_status.py` may still print its obsolete "no feasible 3-block design in ANY domain" line; that message is a known non-blocker and does **not** block campaign-07, which uses a feasible 60/20/20 chronological split with three test blocks on the balanced mark-price cache. Do not let that legacy line stall the run.

### Mandatory execution sequence

1. Create exactly one fresh `research_state/session_<UTC>/` whose id is lexicographically greater than `20261126T153244Z`. Do not reuse or cite any aborted attempt (the quarantined `20261126T153717Z` and `20261126T144850Z` attempts are invalid evidence).
2. Copy `handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py` into that new session directory. Set `SESSION` to the fresh UTC id and `CAMPAIGN_START` to `20261126T153244Z`. Running it from the quarantine directory is invalid (wrong relative cache path); running the copied script from `research_state/session_<UTC>/` resolves `../data_cache` correctly.
3. **Apply the §0 mark-price-only common-support filter to the aligned raw series before feature/target construction, not merely to the final pooled rows:** read ONLY `markPriceKlines-*` mark-price CSVs/ZIPs (any of the three layouts), dedup by `open_time`, drop `close<=0` (this removes the corrupt XRPUSDT 2025-10-19 day), then retain only rows whose timestamp `t` is in the all-five-symbol hourly intersection `S`. **Do not** read the top-level `<SYM>-1h-*.zip` klines. Recompute `S` from the cache; record `|S| = 22,584`, per-symbol 1h counts (four at 22,608; XRPUSDT 22,584; XRPUSDT binds by 24h on 2025-10-19), and the resulting train/val/test timestamp and row counts.
4. Reuse `research_state/data_cache/<SYM>_<YYYY_MM>/` read-only. Verify every consumed file by computing its sha256 and comparing to the hash-only `.sha256` sidecar AND `research_state/cached_inputs_hashes.json["hashes"][path]`; record exact coverage, layout (which of the three layouts each month used), the XRPUSDT 2025-10-19 corrupt-day quarantine, and any shortfall. Do not zero-fill, silently substitute, re-download, or inspect outcomes before the prereg is frozen.
5. Produce the complete artifact set in §2 under that one fresh session directory. Every file must be non-empty; every JSON must carry the real `session_id` and experiment id. No root-level `research_state/*.md` or `*.json` files: the root is at its 500-file cap.
6. Run the heavy evaluation and an independent stdlib recompute. The recompute must reproduce the verdict with `all_checks_match=true`; the evidence audit must have `audit_pass=true` and no unresolved blocker. A valid `NOT_SUPPORTED` result is acceptable; placeholders and fabricated agreement are not. The recompute must independently rebuild `S` (mark-price only, `close>0`, XRP 2025-10-19 excluded) and confirm the test set contains all five symbols with `n_test >= 500`.
7. Only after the artifacts exist, update `research_state/experiment_frontier.json` and this handoff. Set rank-0 to `COMPLETED_VALIDATED`, record the reproduced verdict and completed session, demote campaign-07 to a non-zero rank, and promote the next materially distinct unfinished task without reopening a closed arm.
8. Finish only when the verification in §4 passes. If any required artifact is missing or empty, the session is incomplete.

---

## 2. REQUIRED HEAVY ARTIFACTS — SAME FRESH SESSION

- `fclr_live_archive07_source_registry_<UTC>.{json,md}` — exact cache paths, per-file SHA-256 results (hash-only sidecar + `cached_inputs_hashes.json["hashes"]`), coverage per symbol/dataset, layout notes (which of the three layouts per month), the XRPUSDT 2025-10-19 negative-close quarantine, the mark-price-only common-support `S` definition and `|S| = 22,584`, and read-only reuse statement.
- `fclr_live_archive07_prereg_<UTC>.{json,md}` — outcome-blind, hash-bound to the source registry, with `outcome_data_inspected_before_freeze:false`, look `k=2`, `alpha_2=0.008333`, and the frozen `|S| = 22,584` / split sizes.
- `fclr_live_archive07_eval_<UTC>.{py,json,md}` — heavy three-block evaluation implementing the frozen design on the balanced mark-price support, at least 2,000 deterministic block-bootstrap replicates, per-block diagnostics, and leave-one-symbol-out diagnostics (all five symbols present in every fold).
- `fclr_live_archive07_recompute_<UTC>.{py,json}` — independent stdlib recompute with `all_checks_match:true` and reproduced verdict; independently rebuilds `S` (mark-price only, `close>0`).
- `fclr_live_archive07_evidence_audit_<UTC>.{json,md}` — leakage/evidence audit with `audit_pass`, verdict, and `unresolved_blockers`.
- `evidence_audit_<UTC>.{json,md}` — substantive gate-critical alias matching the verdict.
- `trigger_check_<UTC>.json` — `external_trigger_required:false`, `trigger_source:"BINANCE_PUBLIC_ARCHIVE"`, `fired:false`.
- `_headline_<UTC>.json` — concise headline metrics for independent gate validation.

---

## 3. FROZEN DESIGN — DO NOT RE-DERIVE OR THRESHOLD-SHOP

1. **Cohort / support:** 2024-04-01 through 2026-10-31 UTC; exactly the five symbols above; **restricted to the mark-price common support `S`** = UTC hourly timestamps where all five symbols have a `markPriceKlines` close > 0 (the §0 correction; `|S| = 22,584` balanced-for-four / XRPUSDT-binds-by-24h at this refresh, to be recomputed and frozen in the prereg). This is disjoint from the 2021-2024 cohort used by campaigns 01–06.
2. **Primary target:** `y = log(RV_24h_next + 1e-09)` from one-hour mark-price log returns; metric is out-of-sample QLIKE.
3. **Declared secondary:** `log(RV_minus_next24h + 1e-09)`; metric is MSE. The Holm family is exactly these two targets.
4. **B1:** fixed signed-HAR history set used by campaigns 05/06: log RV1h/RV24h/RV168h plus log RV_plus/RV_minus at 24h/168h.
5. **C2:** B1 plus signed funding(24h), trailing 90-day absolute-funding percentile, mark/index premium, and mark/EMA24 distance. All scaling is train-only.
6. **Split:** 60/20/20 by unique UTC timestamp **on `S`**, 168-hour purge/embargo, three chronological test blocks.
7. **Models:** fixed-form deterministic stdlib OLS only. No regularization, model-family search, feature search, or threshold tuning.
8. **Inference:** at least 2,000 fixed-seed block-bootstrap replicates, preserving complete UTC blocks jointly across symbols; report per-block and leave-one-symbol-out concentration diagnostics.
9. **Verdict:** `PROMOTED` requires primary C2-versus-B1 relative QLIKE reduction of at least 2%, a 95% bootstrap CI lower bound above zero at the look-`k=2` alpha, and a consistent Holm-adjusted secondary direction. Otherwise preserve `NOT_SUPPORTED`; use `INCONCLUSIVE` only when the evidence supports neither conclusion.

The cache and numerical template are feasible today. Campaign-06 completed the full stdlib-only heavy set with `all_checks_match=true`; campaign-07 uses the same numerical approach on the balanced mark-price disjoint cohort and later regime.

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

## 6. FOCUS CAMPAIGN AND NON-AVOIDANCE CONSTRAINTS

**Focus campaign (repo-name priority): Funding-conditioned next-24h volatility forecasting.** The repo name leads with **Funding-conditioned-volatility**, so the confirmatory campaign-07 contrast (C2 vs B1 on next-24h log-RV QLIKE, balanced mark-price disjoint 2024-04..2026-10 cohort) is the single highest-value unfinished task and the only task this session may execute. Heavy compute is mandatory: full three-block evaluation + ≥2,000-replicate block bootstrap + leave-one-symbol-out + independent stdlib recompute that rebuilds `S` (mark-price only, `close>0`).

- **Machine-enforced non-avoidance:** `scripts/check_handoff_heavywork_gate.py` binds campaign-07 to the `fclr_live_archive07_*` artifact family plus `evidence_audit_<UTC>.{json,md}` and `trigger_check_<UTC>.json` in the newest session. A trigger-only, prose-only, audit-only, prereg-only, source-registry-only, verify-and-stop, or zero-byte-placeholder session fails closed. The gate is green now only because the newest on-disk session predates the campaign start; the first post-start session that lacks the full heavy set will fail.
- Closed and not re-runnable: campaigns 01/03/04/05/06 on the five-symbol archive; broad ironflow VOL-BROAD/VOL-CORR/VOL-STRESS/VOL-JUMP arms; the terminal liquidation-risk program on the frozen ironflow panel.
- Do not build a risk overlay: the forecast gate has not passed.
- Do not wait for an external trigger; campaign-07 requires no network and no new source.
- Do not modify `.github/workflows`, sealed protocols, raw caches, or prior frozen artifacts.
- Stdlib only for campaign-07. No package installation.
- Do not create a second active handoff or a status-only session. The next session's purpose is the complete heavy evaluation, independent reproduction, and synchronized frontier.
- **Single durable handoff:** update this file and `research_state/experiment_frontier.json` only after the heavy artifacts exist and verify. Do not create root-level `research_state/*.md`/`*.json` files (root at 500-file cap).

**Highest-value next action:** execute campaign-07 exactly as frozen above, on the balanced mark-price common support `S` (`|S| = 22,584`; recompute and freeze exact; XRPUSDT binds by 24h on the corrupt 2025-10-19 day).
**Dominant limitation to disclose:** the mark-price cache is stored in three heterogeneous layouts, the month dirs also carry a separate regular-klines stream, and XRPUSDT 2025-10-19 has 24 negative (corrupt) mark-price closes — the recompute must use mark-price only, dedup by `open_time`, drop `close<=0`, and quarantine the XRP day; per-block + leave-one-symbol-out diagnostics remain mandatory.
**Concrete falsification test:** C2 improves relative test QLIKE by at least 2% with the frozen uncertainty and Holm conditions on the untouched balanced mark-price cohort.

**END OF HANDOFF — 2026-11-27T03:54:33Z**