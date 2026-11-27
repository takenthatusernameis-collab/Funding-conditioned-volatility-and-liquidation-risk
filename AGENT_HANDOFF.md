# AGENT HANDOFF — Durable Single Source of Truth for the Next Session

**Generated (UTC):** 2026-11-27T06:03:18Z
**Repository priority (from repo name `Funding-conditioned-volatility-and-liquidation-risk`):** Funding-conditioned next-24h volatility forecasting is the single highest-value unfinished task. The repo name leads with **Funding-conditioned-volatility**, so the confirmatory campaign-07 contrast (C2 vs B1 on next-24h log-RV QLIKE, balanced mark-price disjoint 2024-04..2026-10 cohort) is the only task this session may execute.
**Program status:** ACTIVE — `FCLR-LIVE-ARCHIVE-07-20261126T153244Z` is rank-0 `READY_EXECUTE` in `research_state/experiment_frontier.json`.
**HEAD:** `e2e26c0c9` (verified this pass). **Working tree:** clean except the new `scripts/fclr_live_archive07_eval_ready.py` (the corrected base, see §0).
**Gate (verified this pass):** `pass=true`, `reason_code=OK`, `failures=[]`, `live_archive.required=false` (newest on-disk session `20261126T133828Z` predates campaign start `20261126T153244Z`; the first post-start session flips it to required). Root `research_state/` is at **exactly 500** md+json files (zero headroom). XRPUSDT 2025-10-19 corrupt day re-verified this pass: 24/24 rows have `close<=0` (e.g. `-0.00054414`).

> **This file is the ONLY durable handoff.** Do not create a root `INITIAL_TASK_MESSAGE_*` file, a second handoff, or any root-level `research_state/*.md`/`*.json` (a single root write makes 501 and fails the gate). Read §1 and execute it.

---

## 0. BOTTLENECK STATUS — the re-curation loop is now physically broken

**No session is blocked and no setup/gate-repair step is required at 2026-11-27T06:03:18Z.** The gate is green and armed; the five-symbol 2024-04..2026-10 mark-price cache is on disk; `|S| = 22,584` is the carried-forward independently re-derived value and must be recomputed in-session.

**THE bottleneck was the re-curation loop itself — this pass removes its root cause.** Prior refreshes (04:54, 04:58, 05:52, 05:56, 05:57, 05:58) re-verified readiness but handed the next session a template with two real defects that forced a rewrite every time:

1. The old recovery template (`handoff_archive/quarantine_20261126T144850Z/fclr_live_archive07_eval_20261126T144850Z.py`) globbed only `*.zip` per day dir, so it **silently dropped the 2024-04..2024-09 nested-CSV layout and the 2024-10..2024-12 flat-CSV layout** (false `|S|` / false coverage).
2. Its `main()` pooled per-symbol panels **without enforcing the all-five common support `S`**.

**Both are now fixed in `scripts/fclr_live_archive07_eval_ready.py`** (compiles clean; smoke-tested this pass: nested 2024-04 CSV parsed, XRP 2025-10-19 yields 0 positive closes, top-level `<SYM>-1h-*.zip` regular klines correctly excluded). **The next session's job is now copy → set `SESSION` → run, not rewrite.** A further timestamp-only or verification-only refresh is itself the bottleneck and a failed session; do not do it.

**Gate consequence (armed):** the first session whose `research_state/session_<UTC>/` lacks the complete non-empty `fclr_live_archive07_*` set plus an independent recompute with `all_checks_match=true` and `audit_pass=true` **fails the gate closed**. No trigger-only, prose-only, audit-only, prereg-only, source-registry-only, or verify-and-stop session can pass.

**Authoritative common-support number (recompute in-session; freeze exact value in prereg — do NOT hard-code, do NOT claim "all five identical"):**

- **BNBUSDT = BTCUSDT = ETHUSDT = SOLUSDT = 22,608** clean 1h mark-price closes in-window.
- **XRPUSDT = 22,584** — the binding series, short by exactly 24 hours.
- **True common support `|S| = 22,584`** (all-five-symbol hourly intersection, mark-price `close>0`).
- **Cause of the 24h shortfall:** `research_state/data_cache/XRPUSDT_2025_10/markPriceKlines-2025-10-19/XRPUSDT-1h-2025-10-19.csv` has 24 rows with negative `close` (all that day). **Quarantine and record provenance; do NOT zero-fill, repair, or silently substitute.** `close>0` removes exactly those 24 hours (the ready template does this).
- **Embargoed 60/20/20 split on `S` (168h purge):** train ≈ 13,550 ts / val ≈ 4,517 ts / test ≈ 4,517 ts ≈ **22,585 test rows across all five symbols**; three chronological test blocks of ≈1,500 ts (≈7,500 rows) each, all five symbols in every block.

### Cache layout heterogeneity — handled by the ready template (do not re-discover)

Three layouts + a separate regular-klines stream that must NOT be confused with mark price:

1. `2024_04`..`2024_09`: nested CSVs at `markPriceKlines-<date>/<SYM>-1h-<date>/<SYM>-1h-<date>.csv`.
2. `2024_10`..`2024_12`: flatter CSVs at `markPriceKlines-<date>/<SYM>-1h-<date>.csv` (+ same-day `.zip` duplicate).
3. `2025_01`..`2026_10`: CSVs under `markPriceKlines-<date>/...` **plus** top-level `<SYM>-1h-<date>.zip`.

**Rule (implemented in the ready template):** a file is mark price **iff ANY path component starts with `markPriceKlines-`** (walk to any depth), then dedup by `open_time` (ms) and drop `close<=0`. Top-level `<SYM>-1h-*.zip` are **regular klines (price), NOT mark price** and are excluded. The old immediate-parent-only reader yields a false `|S| = 20,400` — do not re-discover that artifact.

### Two verification-format facts the source registry MUST record

- **`.sha256` sidecars are hash-only** (single 64-hex line). `sha256sum -c <sidecar>` fails; compute `sha256sum <file>` and compare to the sidecar line AND to `research_state/cached_inputs_hashes.json`.
- **`research_state/cached_inputs_hashes.json` is nested:** top-level `{count, derivation_notes, generated_at, hashes}` with **20,694 entries under `hashes`** keyed by repo-relative path. Look up `d["hashes"][path]`, not `path in d`.

Prior quarantined attempts (`20261126T153717Z`, `20261126T144850Z`) are **invalid evidence — do not reuse their outputs.**

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (UTC 2026-11-27T06:03:18Z)

**NON-AVOIDANCE (machine-enforced):** `scripts/check_handoff_heavywork_gate.py` binds campaign-07 to the `fclr_live_archive07_*` artifact family plus `evidence_audit_<UTC>.{json,md}` and `trigger_check_<UTC>.json` in the newest session. A trigger-only, prose-only, audit-only, prereg-only, source-registry-only, verify-and-stop, or zero-byte-placeholder session fails closed. The gate is green now only because the newest on-disk session predates the campaign start; the first post-start session that lacks the full heavy set will fail closed. **This task message is the initial task for the next session — there is no other task. Do NOT write prose; run the eval.**

**EXECUTE `FCLR-LIVE-ARCHIVE-07-20261126T153244Z` NOW under one fresh `session_<UTC>/` (id lexicographically > `20261126T153244Z`).**

**Highest-value unfinished work (repo-name primary estimand):** pre-registered disjoint-cohort replication of **next-24h mean log-realized-variance QLIKE, C2 versus B1**, on the untouched 2024-04 through 2026-10 cohort for `BNBUSDT`, `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT`. Sequential confirmatory look `k=2` with frozen `alpha_2 = 0.05/(2*3) = 0.008333`. Declared Holm secondary: campaign-06 estimand (next-24h downside realized-semivariance level, MSE). Do not substitute another estimand, cohort, threshold, or model search.

**No setup or gate-repair step is required first.** `scripts/next_campaign_status.py` may still print its obsolete "no feasible 3-block design in ANY domain" line (`next_campaign_status.py:1017`); that is a known non-blocker and does **not** block campaign-07, which uses a feasible 60/20/20 chronological split on the balanced mark-price cache. Do not let that legacy line stall the run.

### Mandatory execution sequence

1. Create exactly one fresh `research_state/session_<UTC>/` whose id is lexicographically greater than `20261126T153244Z`. Do not reuse or cite any aborted attempt.
2. Copy `scripts/fclr_live_archive07_eval_ready.py` into that new session directory. Set `SESSION` to the fresh UTC id and `CAMPAIGN_START` to `20261126T153244Z`. Run it **from that session directory** (it resolves `../data_cache` correctly). Do NOT run the old quarantine template.
3. The ready template already: reads all three layouts mark-price-only (any depth, CSV+zip), dedups by `open_time`, drops `close<=0` (XRP 2025-10-19 quarantine), computes the all-five common support `S`, and restricts every symbol's series to `S` **before** feature/target construction. **Do not re-derive or re-filter by hand.** It prints `|S|` and per-symbol raw/in-common counts; confirm `|S| = 22,584` and record it.
4. Reuse `research_state/data_cache/<SYM>_<YYYY_MM>/` read-only. The template discloses gaps; supplement the source registry with per-file sha256 vs the hash-only `.sha256` sidecar AND `cached_inputs_hashes.json["hashes"][path]`, coverage per symbol, layout per month, and the XRPUSDT 2025-10-19 quarantine. Do not zero-fill, substitute, re-download, or inspect outcomes before the prereg is frozen.
5. Produce the complete artifact set in §2 under that one fresh session directory. Every file non-empty; every JSON carries the real `session_id` and experiment id. No root-level `research_state/*.md`/`*.json` (root is at **exactly 500**).
6. Run an independent stdlib recompute that reproduces the verdict with `all_checks_match=true`; evidence audit with `audit_pass=true` and no unresolved blocker. The recompute must independently rebuild `S` (mark-price only, `close>0`, XRP 2025-10-19 excluded) and confirm the test set contains all five symbols with `n_test >= 500`. A valid `NOT_SUPPORTED` is acceptable; placeholders and fabricated agreement are not.
7. Only after the artifacts exist, update `research_state/experiment_frontier.json` and this handoff. Set rank-0 to `COMPLETED_VALIDATED`, record the reproduced verdict and completed session, demote campaign-07 to a non-zero rank, promote the next materially distinct unfinished task without reopening a closed arm.
8. Finish only when §4 verification passes. Any missing/empty required artifact ⇒ session incomplete.

---

## 2. REQUIRED HEAVY ARTIFACTS — SAME FRESH SESSION

- `fclr_live_archive07_source_registry_<UTC>.{json,md}` — exact cache paths, per-file SHA-256 (hash-only sidecar + `cached_inputs_hashes.json["hashes"]`), coverage per symbol, layout per month, XRPUSDT 2025-10-19 quarantine, mark-price-only `S` definition and `|S| = 22,584`, read-only reuse statement. (Template emits a base version; enrich per step 4.)
- `fclr_live_archive07_prereg_<UTC>.{json,md}` — outcome-blind, hash-bound to the source registry, `outcome_data_inspected_before_freeze:false`, look `k=2`, `alpha_2=0.008333`, frozen `|S| = 22,584` / split sizes.
- `fclr_live_archive07_eval_<UTC>.{py,json,md}` — heavy three-block evaluation (the copied ready script), ≥2,000 deterministic block-bootstrap replicates, per-block + leave-one-symbol-out diagnostics (all five symbols in every fold).
- `fclr_live_archive07_recompute_<UTC>.{py,json}` — independent stdlib recompute, `all_checks_match:true`, reproduced verdict; independently rebuilds `S` (mark-price only, `close>0`).
- `fclr_live_archive07_evidence_audit_<UTC>.{json,md}` — leakage/evidence audit with `audit_pass`, verdict, `unresolved_blockers`.
- `evidence_audit_<UTC>.{json,md}` — substantive gate-critical alias matching the verdict.
- `trigger_check_<UTC>.json` — `external_trigger_required:false`, `trigger_source:"BINANCE_PUBLIC_ARCHIVE"`, `fired:false`.
- `_headline_<UTC>.json` — concise headline metrics (template emits).

---

## 3. FROZEN DESIGN — DO NOT RE-DERIVE OR THRESHOLD-SHOP

1. **Cohort / support:** 2024-04-01 through 2026-10-31 UTC; exactly the five symbols; **restricted to the mark-price common support `S`** = UTC hourly timestamps where all five symbols have a `markPriceKlines` close > 0 (`|S| = 22,584`, recompute and freeze exact). Disjoint from the 2021-2024 cohort used by campaigns 01–06.
2. **Primary target:** `y = log(RV_24h_next + 1e-09)` from 1h mark-price log returns; metric out-of-sample QLIKE.
3. **Declared secondary:** `log(RV_minus_next24h + 1e-09)`; metric MSE. Holm family is exactly these two targets.
4. **B1:** log RV1h/RV24h/RV168h + log RV_plus/RV_minus at 24h/168h (7 feats).
5. **C2:** B1 + signed funding(24h) + trailing 90-day absolute-funding percentile + mark/index premium + mark/EMA24 distance (11 feats). Train-only scaling.
6. **Split:** 60/20/20 by unique UTC timestamp on `S`, 168h purge/embargo, three chronological test blocks.
7. **Models:** fixed-form deterministic stdlib OLS only. No regularization, model-family search, feature search, or threshold tuning.
8. **Inference:** ≥2,000 fixed-seed block-bootstrap replicates, preserving complete UTC blocks jointly across symbols; per-block + leave-one-symbol-out diagnostics.
9. **Verdict:** `PROMOTED` requires primary C2-vs-B1 relative QLIKE reduction ≥2%, 95% bootstrap CI lower bound > 0 at look-`k=2` alpha, and consistent Holm-adjusted secondary direction. Otherwise `NOT_SUPPORTED`; `INCONCLUSIVE` only when evidence supports neither.

---

## 4. VERIFICATION COMMANDS — RUN AT START AND END

```bash
export UTC=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p research_state/session_$UTC
python3 -m py_compile scripts/fclr_live_archive07_eval_ready.py
python3 scripts/check_handoff_heavywork_gate.py --json
python3 -m unittest \
  tests.test_vol_jump_campaign_gate tests.test_vol_stress_campaign_gate \
  tests.test_vol_corr_campaign_gate tests.test_vol_broad_campaign_gate \
  tests.test_tracka_hardening_143 tests.test_active_campaign_gate
python3 -m json.tool research_state/experiment_frontier.json >/dev/null
git diff --check
```

After the heavy session the gate must report top-level `pass=true`, `reason_code=OK`, `failures=[]`, and `live_archive.required=true`, `live_archive.pass=true`, `artifact_family="live_archive07"`, with empty missing/empty artifact lists. The six-module unittest command must pass. Do not chase the pre-existing legacy Track A modules that require absent numpy/pandas/pyarrow; package installation is forbidden.

---

## 5. COMPLETED SESSION RECORD — `session_20261126T133828Z` (do not re-run)

**Campaign:** `FCLR-LIVE-ARCHIVE-06-20261126T083526Z` — **Verdict:** `NOT_SUPPORTED` (C2 vs B1 relative test-MSE reduction `0.716%`, 95% CI `[0.419%, 1.020%]`, below 2% floor). Independent recompute `all_checks_match=true`; `n_test=35715`; `n_unique_timestamps=34872`; evidence audit `audit_pass=true`, `unresolved_blockers=[]`. Complete artifact set under `research_state/session_20261126T133828Z/`.

---

## 6. FOCUS CAMPAIGN AND NON-AVOIDANCE CONSTRAINTS

**Focus campaign (repo-name priority): Funding-conditioned next-24h volatility forecasting.** The confirmatory campaign-07 contrast (C2 vs B1 on next-24h log-RV QLIKE, balanced mark-price disjoint 2024-04..2026-10 cohort) is the single highest-value unfinished task and the only task this session may execute. Heavy compute is mandatory: full three-block evaluation + ≥2,000-replicate block bootstrap + leave-one-symbol-out + independent stdlib recompute that rebuilds `S` (mark-price only, `close>0`).

- **Machine-enforced non-avoidance:** `scripts/check_handoff_heavywork_gate.py` binds campaign-07 to the `fclr_live_archive07_*` artifact family plus `evidence_audit_<UTC>.{json,md}` and `trigger_check_<UTC>.json` in the newest session. Trigger-only, prose-only, audit-only, prereg-only, source-registry-only, verify-and-stop, or zero-byte-placeholder sessions fail closed.
- Closed and not re-runnable: campaigns 01/03/04/05/06; broad ironflow VOL-BROAD/VOL-CORR/VOL-STRESS/VOL-JUMP arms; the terminal liquidation-risk program on the frozen ironflow panel.
- Do not build a risk overlay (forecast gate has not passed). Do not wait for an external trigger (campaign-07 needs no network/new source). Do not modify `.github/workflows`, sealed protocols, raw caches, or prior frozen artifacts. Stdlib only; no package installation.
- Do not create a second active handoff or a status-only session. Update this file and `research_state/experiment_frontier.json` only after the heavy artifacts exist and verify. Do not create root-level `research_state/*.md`/`*.json` (root at **exactly 500**, zero headroom).

**Highest-value next action:** copy `scripts/fclr_live_archive07_eval_ready.py` into a fresh `session_<UTC>/`, set `SESSION`, and run it; then produce the recompute + evidence audit + trigger check and verify.
**Dominant limitation to disclose:** three heterogeneous cache layouts + a separate regular-klines stream + XRPUSDT 2025-10-19 corrupt day — the ready template handles all three (mark-price only, dedup `open_time`, `close>0`, quarantine); per-block + leave-one-symbol-out diagnostics remain mandatory.
**Concrete falsification test:** C2 improves relative test QLIKE by ≥2% with the frozen uncertainty and Holm conditions on the untouched balanced mark-price cohort.

**END OF HANDOFF — 2026-11-27T06:03:18Z**