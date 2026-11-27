# AGENT HANDOFF — Durable Single Source of Truth for the Next Session

**Generated (UTC):** 2026-11-27T13:16:54Z
**Repository priority (from repo name `Funding-conditioned-volatility-and-liquidation-risk`):** the funding-conditioned-volatility half was the primary estimand and is **CLOSED with a real verdict** (campaign-07, `NOT_SUPPORTED`, independently reproduced). The next highest-value unfinished work is the **liquidation-risk** half of the repo name: a Track-B modeled boundary-breach forecast (campaign-08). This is the ONLY task the next session may execute.
**Program status:** ACTIVE — `FCLR-LIVE-ARCHIVE-08` is rank-0 `READY_EXECUTE` in `research_state/experiment_frontier.json`.
**HEAD:** working tree clean at `b0552fc52`; this handoff refresh is the only pending edit. **Working tree:** the last COMPLETE heavy session is `research_state/session_20261127T065600Z/` (campaign-07, full 15-artifact set). No incomplete/aborted session directory exists on disk. The newest on-disk session id is `20261127T065600Z`.
**Gate (verified this pass, 2026-11-27T13:16:54Z):** `pass=true`, `reason_code=OK`, `failures=[]`, `live_archive.required=true`, `live_archive.pass=true`, `artifact_family="live_archive07"`, empty missing/empty lists. Six-module unittest suite = 122 tests OK; `py_compile` of the campaign-07 template OK; `experiment_frontier.json` valid JSON; `git diff --check` clean. Root `research_state/` is at **exactly 500** md+json files (zero headroom) — do NOT add any root-level `research_state/*.md`/`*.json` (one root write makes 501 and fails the gate).

> **This file is the ONLY durable handoff.** Do not create a root `INITIAL_TASK_MESSAGE_*` file, a second handoff, or any root-level `research_state/*.md`/`*.json`. Read §1 and execute it.

---

## 0. BOTTLENECK STATUS — nothing is blocked; the path is real and validated

**No session is blocked and there is no re-curation trap.** Prior passes handed the next session a mathematically broken QLIKE template (uncentred, non-negative-violating form) that produced 10^11% LOO artifacts; that was fixed in `session_20261127T065600Z` to the standard non-negative QLIKE `mean(exp(y−p) − (y−p) − 1)`, the full heavy evaluation was executed, and the verdict was reproduced by an independent stdlib recompute (`all_checks_match=true`). The next session starts from real, validated artifacts — not a template.

**Stale-handoff bottleneck removed:** the prior handoff referenced an incomplete `20261127T070655Z` attempt on disk; that directory no longer exists. The newest on-disk session is the complete `session_20261127T065600Z`. The next fresh session id MUST be lexicographically greater than `20261127T065600Z`.

**Two corrections carried forward (both verified in the 065600Z pass):**
1. **`|S| = 22608`, not 22584.** All-five mark-price common support is **22,608** (BNBUSDT = BTCUSDT = ETHUSDT = SOLUSDT = XRPUSDT = 22,608). The "XRP binds / |S|=22584" claim was a measurement artifact: `XRPUSDT_2025_10/markPriceKlines-2025-10-19/` has a corrupt `.csv` (24 rows, `close<=0`, correctly dropped) AND a valid `.zip` of the same day (real prices ~2.35) that restores full support. No zero-fill, repair, or substitution was performed.
2. **Secondary realigned** to frozen design §3.3: next-24h downside realized-semivariance **level** `log(RV_minus_next + eps)`, MSE.

**Cache layout heterogeneity (handled; do NOT re-discover):** a file is mark price **iff ANY path component starts with `markPriceKlines-`** (walk to any depth), then dedup by `open_time` and drop `close<=0`. Top-level `<SYM>-1h-*.zip` are **regular klines (price), NOT mark price** and are excluded. `.sha256` sidecars are hash-only; `research_state/cached_inputs_hashes.json` nests 20,694 hashes under `d["hashes"][path]`.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (UTC 2026-11-27T13:16:54Z)

**NON-AVOIDANCE (machine-enforced):** `scripts/check_handoff_heavywork_gate.py` binds the active live-archive campaign to the `fclr_live_archive<NN>_*` artifact family plus `evidence_audit_<UTC>.{json,md}` and `trigger_check_<UTC>.json` in the newest session. A trigger-only, prose-only, audit-only, prereg-only, source-registry-only, verify-and-stop, or zero-byte-placeholder session **fails closed**. **This task message is the initial task for the next session — there is no other task. Do NOT write prose; run the eval to completion.**

**EXECUTE `FCLR-LIVE-ARCHIVE-08-20261127T131654Z` NOW under exactly one fresh `research_state/session_<UTC>/` whose id is lexicographically greater than `20261127T065600Z`.**

**Highest-value unfinished work (repo-name secondary estimand — liquidation risk):** a **Track-B modeled hypothetical boundary-breach forecast** on the **same frozen balanced mark-price common support `S` (`|S| = 22,608`; 2024-04..2026-10; BNBUSDT/BTCUSDT/ETHUSDT/SOLUSDT/XRPUSDT)** and the **same 60/20/20 by unique UTC timestamp + 168h purge/embargo + three chronological test blocks**. Pre-register hypothetical long/short liquidation boundaries from **disclosed constant margin/leverage scenarios** (state them explicitly; they are synthetic modeled breaches, **not** observed liquidations and **not** a risk overlay). Target = whether the future mark-price path breaches the boundary within a fixed horizon; **keep long and short labels separate**. Compare a **funding-conditioned model** vs a **mark-price-only baseline** by out-of-sample **AUC / log-loss / Brier**, with ≥2,000 fixed-seed block-bootstrap replicates and leave-one-symbol-out. This is **forecast validation**, permitted under RESEARCH_PROMPT §9; **no risk overlay is authorized** because the campaign-07 forecast gate did **not** pass.

**No setup or gate-repair step is required first.** The mark-price cache is on disk and read-only reusable. `scripts/next_campaign_status.py` may print a legacy "no feasible 3-block design" line — known non-blocker; do not let it stall the run.

### Mandatory execution sequence

1. Create exactly one fresh `research_state/session_<UTC>/` (id > `20261127T065600Z`). Do not reuse or cite any aborted attempt.
2. Copy `research_state/session_20261127T065600Z/fclr_live_archive07_eval_20261127T065600Z.py` as the **structural template**. It already: reads all three on-disk layouts mark-price-only, dedups by `open_time`, drops `close<=0`, computes the all-five common support `S`, restricts every symbol to `S` before feature/target construction, uses the standard non-negative QLIKE, and emits source_registry + prereg + eval + headline. Adapt ONLY: (a) set `SESSION` to the fresh id and `EXPERIMENT="FCLR-LIVE-ARCHIVE-08"`, `CAMPAIGN_START` to the fresh id; (b) swap the **target** to the Track-B boundary-breach label (long/short separate) and the **metrics** to AUC / log-loss / Brier; (c) add the disclosed constant margin/leverage scenarios and horizon to the prereg. **Do NOT re-derive the cache reader or the `S` filter. Do NOT re-derive thresholds.**
3. Reuse `research_state/data_cache/<SYM>_<YYYY_MM>/` read-only. Confirm `|S| = 22,608` and record it. Supplement the source registry with per-file sha256 vs the hash-only `.sha256` sidecar AND `cached_inputs_hashes.json["hashes"][path]`, coverage per symbol, layout per month, and the XRPUSDT 2025-10-19 corrupt-CSV / valid-ZIP provenance. Do not zero-fill, substitute, re-download, or inspect outcomes before the prereg is frozen.
4. Produce the complete artifact set in §2 under that one fresh session directory. Every file non-empty; every JSON carries the real `session_id` and experiment id. No root-level `research_state/*.md`/`*.json` (root is at **exactly 500**).
5. Run an independent stdlib recompute (separate code path — own cache reader, own panel build, different solver) that reproduces the verdict with `all_checks_match=true`; evidence audit with `audit_pass=true` and no unresolved blocker. The recompute must independently rebuild `S` (mark-price only, `close>0`) and confirm all five symbols in every block/fold with `n_test >= 500`. A valid `NOT_SUPPORTED` is acceptable; placeholders and fabricated agreement are not.
6. Only after the artifacts exist, update `research_state/experiment_frontier.json` and this handoff. Set rank-0 to `COMPLETED_VALIDATED`, record the reproduced verdict and completed session, demote campaign-08 to a non-zero rank, and **update this handoff so the FIRST `FCLR-LIVE-ARCHIVE-<NN>-<start>` token is `09`** (archive the 08 completion record below it) so the gate ratchets to the 09 artifact family.
7. Finish only when §4 verification passes. Any missing/empty required artifact ⇒ session incomplete.

---

## 2. REQUIRED HEAVY ARTIFACTS — SAME FRESH SESSION (campaign-08)

- `fclr_live_archive08_source_registry_<UTC>.{json,md}` — exact cache paths, per-file SHA-256 (hash-only sidecar + `cached_inputs_hashes.json["hashes"]`), coverage per symbol, layout per month, XRPUSDT 2025-10-19 provenance, mark-price-only `S` definition and `|S| = 22,608`, read-only reuse statement.
- `fclr_live_archive08_prereg_<UTC>.{json,md}` — outcome-blind, hash-bound to the source registry, `outcome_data_inspected_before_freeze:false`, frozen `|S| = 22,608` / split sizes / margin-leverage scenarios / horizon.
- `fclr_live_archive08_eval_<UTC>.{py,json,md}` — heavy three-block evaluation, ≥2,000 deterministic block-bootstrap replicates, per-block + leave-one-symbol-out diagnostics (all five symbols in every fold).
- `fclr_live_archive08_recompute_<UTC>.{py,json}` — independent stdlib recompute, `all_checks_match:true`, reproduced verdict; independently rebuilds `S` (mark-price only, `close>0`).
- `fclr_live_archive08_evidence_audit_<UTC>.{json,md}` — leakage/evidence audit with `audit_pass`, verdict, `unresolved_blockers`.
- `evidence_audit_<UTC>.{json,md}` — substantive gate-critical alias matching the verdict.
- `trigger_check_<UTC>.json` — `external_trigger_required:false`, `trigger_source:"BINANCE_PUBLIC_ARCHIVE"`, `fired:false`.
- `_headline_<UTC>.json` — concise headline metrics.

---

## 3. FROZEN DESIGN — CARRY FORWARD (do not re-derive or threshold-shop)

1. **Cohort / support:** 2024-04-01 through 2026-10-31 UTC; exactly the five symbols; **restricted to the mark-price common support `S`** = UTC hourly timestamps where all five symbols have a `markPriceKlines` close > 0 (`|S| = 22,608`, recompute and freeze exact). Disjoint from the 2021-2024 cohort used by campaigns 01–06.
2. **Split:** 60/20/20 by unique UTC timestamp on `S`, 168h purge/embargo, three chronological test blocks; all five symbols in every block/fold.
3. **Models:** fixed-form deterministic stdlib OLS only. No regularization, model-family search, feature search, or threshold tuning. Train-only scaling.
4. **Inference:** ≥2,000 fixed-seed block-bootstrap replicates, preserving complete UTC blocks jointly across symbols; per-block + leave-one-symbol-out diagnostics.
5. **Campaign-08 target (new):** Track-B modeled boundary-breach indicator (long/short separate) under disclosed constant margin/leverage scenarios; metrics AUC / log-loss / Brier; funding-conditioned vs mark-price-only baseline. **Not** a risk overlay; **not** observed liquidations.

---

## 4. VERIFICATION COMMANDS — RUN AT START AND END

```bash
export UTC=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p research_state/session_$UTC
python3 -m py_compile research_state/session_20261127T065600Z/fclr_live_archive07_eval_20261127T065600Z.py
python3 scripts/check_handoff_heavywork_gate.py --json
python3 -m unittest \
  tests.test_vol_jump_campaign_gate tests.test_vol_stress_campaign_gate \
  tests.test_vol_corr_campaign_gate tests.test_vol_broad_campaign_gate \
  tests.test_tracka_hardening_143 tests.test_active_campaign_gate
python3 -m json.tool research_state/experiment_frontier.json >/dev/null
git diff --check
```

After the heavy session the gate must report top-level `pass=true`, `reason_code=OK`, `failures=[]`, and `live_archive.required=true`, `live_archive.pass=true`, `artifact_family="live_archive08"`, with empty missing/empty artifact lists. The six-module unittest command must pass. Do not chase the pre-existing legacy Track A modules that require absent numpy/pandas/pyarrow; package installation is forbidden.

---

## 5. COMPLETED SESSION RECORD — `session_20261127T065600Z` (do not re-run)

**Campaign:** `FCLR-LIVE-ARCHIVE-07-20261126T153244Z` — **Verdict:** `NOT_SUPPORTED`.
**Primary (next-24h mean log-RV, QLIKE, C2 vs B1):** relative reduction **−0.704%** (C2 is *worse*), 95% block-bootstrap CI **[−1.218%, −0.190%]** (entirely below 0), floor +2%. QLIKE B1 = 0.426669, C2 = 0.429672.
**Secondary (next-24h downside semivariance level, MSE, Holm 2-family):** C2 vs B1 relative MSE reduction +1.24% (direction consistent) but the primary fails, so the family does not promote.
**Leave-one-symbol-out (rel QLIKE C2 vs B1):** BNBUSDT +1.32%, BTCUSDT +0.37%, ETHUSDT −0.75%, SOLUSDT −1.55%, XRPUSDT −3.18%.
**Support:** `|S| = 22,608`; `n_test = 23,260`; `n_unique_timestamps = 22,416`; per-symbol rows 22,416; `n_train = 66,405`, `n_val = 22,415`.
**Independent recompute:** `all_checks_match=true` (separate cache reader + Cholesky/standardized solver). Evidence audit `audit_pass=true`, `unresolved_blockers=[]`. Complete artifact set under `research_state/session_20261127T065600Z/`.
**Template fix disclosed:** standard non-negative QLIKE replaced the broken uncentred form; `|S|=22608` supersedes 22584.

---

## 6. FOCUS CAMPAIGN AND NON-AVOIDANCE CONSTRAINTS

**Focus campaign (repo-name priority): liquidation-risk via a Track-B modeled boundary-breach forecast (campaign-08).** The funding-conditioned-volatility primary (campaign-07) is closed `NOT_SUPPORTED`; the liquidation-risk half is the single highest-value unfinished task and the only task the next session may execute. Heavy compute is mandatory: full three-block evaluation + ≥2,000-replicate block bootstrap + leave-one-symbol-out + independent stdlib recompute that rebuilds `S` (mark-price only, `close>0`).

- **Machine-enforced non-avoidance:** the gate binds the active campaign to the `fclr_live_archive<NN>_*` artifact family plus `evidence_audit_<UTC>.{json,md}` and `trigger_check_<UTC>.json` in the newest session. Trigger-only, prose-only, audit-only, prereg-only, source-registry-only, verify-and-stop, or zero-byte-placeholder sessions fail closed.
- Closed and not re-runnable: campaigns 01/03/04/05/06/**07**; broad ironflow VOL-BROAD/VOL-CORR/VOL-STRESS/VOL-JUMP arms; the terminal liquidation-risk program on the frozen ironflow panel.
- **Do NOT build a risk overlay** (the campaign-07 forecast gate did not pass). Do NOT wait for an external trigger (campaign-08 needs no network/new source). Do NOT modify `.github/workflows`, sealed protocols, raw caches, or prior frozen artifacts. Stdlib only; no package installation.
- Do not create a second active handoff or a status-only session. Update this file and `research_state/experiment_frontier.json` only after the heavy artifacts exist and verify. Do not create root-level `research_state/*.md`/`*.json` (root at **exactly 500**, zero headroom).

**Highest-value next action:** copy the campaign-07 eval script as a structural template into a fresh `session_<UTC>/` (id > `20261127T065600Z`), set `SESSION`/`EXPERIMENT="FCLR-LIVE-ARCHIVE-08"`, swap the target to the boundary-breach label and metrics to AUC/log-loss/Brier, and run it; then produce the recompute + evidence audit + trigger check and verify.
**Dominant limitation to disclose:** three heterogeneous cache layouts + a separate regular-klines stream + XRPUSDT 2025-10-19 corrupt CSV (valid ZIP restores support) — the template handles all of these (mark-price only, dedup `open_time`, `close>0`); per-block + leave-one-symbol-out diagnostics remain mandatory.
**Concrete falsification test:** the funding-conditioned model improves out-of-sample boundary-breach discrimination (AUC / log-loss / Brier) over the mark-price-only baseline with the frozen uncertainty on the untouched balanced mark-price cohort.

**END OF HANDOFF — 2026-11-27T13:16:54Z**