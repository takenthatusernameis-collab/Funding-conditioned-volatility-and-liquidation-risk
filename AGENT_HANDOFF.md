# AGENT HANDOFF — Durable Single Source of Truth for the Next Session

**Generated (UTC):** 2026-11-27T16:55:15Z
**Repository priority (from repo name `Funding-conditioned-volatility-and-liquidation-risk`):** the **funding-conditioned-volatility** half was the primary estimand and is **CLOSED with a real verdict** (campaign-07, `NOT_SUPPORTED`, independently reproduced). The next highest-value unfinished work is the **liquidation-risk** half of the repo name: a Track-B modeled boundary-breach forecast (campaign-08). This is the ONLY task the next session may execute.
**Active rank-0:** `FCLR-LIVE-ARCHIVE-08-20261127T131654Z` — status `READY_EXECUTE` in `research_state/experiment_frontier.json` (program_status `ACTIVE`).
**HEAD:** the latest `chore(kilo): checkpoint agent session` commit (was `ca2e0da91` at generation; **the hash advances on every checkpoint and is NOT a durable anchor — do not rely on it**). **Working tree:** clean. The durable anchor is the last COMPLETE heavy session on disk: `research_state/session_20261127T065600Z/` (campaign-07, full 15-artifact set, `all_checks_match=true`). The newest on-disk session id is `20261127T065600Z`; no aborted `20261127T132836Z` directory exists and no session id in the forbidden range `(20261127T065600Z, 20261127T131654Z]` exists (re-verified 2026-11-27T16:55:15Z).
**Gate (re-verified this pass, 2026-11-27T16:55:15Z):** top-level `pass=true`, `reason_code=OK`, `failures=[]`; `live_archive.required=false` (grandfathered: newest on-disk session `20261127T065600Z` ≤ campaign-08 start `20261127T131654Z`), `live_archive.pass=true`, `live_archive.campaign_id="FCLR-LIVE-ARCHIVE-08-20261127T131654Z"`, `artifact_family=null`, empty missing/empty lists. The gate flips to `live_archive.required=true` and demands the full `fclr_live_archive08_*` set the instant a session with id > `20261127T131654Z` exists (see §1). Six-module unittest suite = **122 tests OK**; `py_compile` of the campaign-07 template OK; `experiment_frontier.json` valid JSON; `git diff --check` clean. Root `research_state/` is at **exactly 500** md+json files (zero headroom) — do NOT add any root-level `research_state/*.md`/`*.json` (one root write makes 501 and fails the gate).

> **This file is the ONLY durable handoff.** Do not create a root `INITIAL_TASK_MESSAGE_*` file, a second handoff, or any root-level `research_state/*.md`/`*.json`. Read §1 and execute it.

---

## 0. BOTTLENECK STATUS — nothing is blocked; the path is real and validated

**Two recurring bottlenecks removed this pass (2026-11-27T16:55:15Z):**
1. **Stale HEAD reference.** Prior handoffs pinned an exact `HEAD` hash (`c4786e37d`) that goes stale on every `chore(kilo): checkpoint` commit (HEAD is already `ca2e0da91`). The handoff now anchors to the durable `session_20261127T065600Z/` directory and explicitly states the hash is not an anchor — no more chasing a moving commit id.
2. **Residual grandfathered avoidance range.** The gate grandfathers any session id `<= 20261127T131654Z`, leaving the half-open range `(20261127T065600Z, 20261127T131654Z]` as a silent green-with-no-work path. §1 PRE-FLIGHT SELF-AUDIT now forces the next agent to prove no session sits in that range and to mint an id strictly `> 20261127T131654Z` before any other action.

**No session is blocked and there is no re-curation trap.** Prior passes handed the next session a mathematically broken QLIKE template (uncentred, non-negative-violating form) that produced 10^11% LOO artifacts; that was fixed in `session_20261127T065600Z` to the standard non-negative QLIKE `mean(exp(y−p) − (y−p) − 1)`, the full heavy evaluation was executed, and the verdict was reproduced by an independent stdlib recompute (`all_checks_match=true`). The next session starts from real, validated artifacts — not a template.

**Aborted-attempt bottleneck removed:** a later campaign-08 attempt stamped `20261127T132836Z` committed only `fclr_live_archive08_eval_*.py` + `fclr_live_archive08_recompute_*.py` and was then deleted (no source registry, prereg, evidence audit, trigger check, or headline; **no on-disk session directory remains**). That incomplete attempt is gone and is **not** evidence. The newest on-disk session is still the complete `session_20261127T065600Z`.

**Cross-file bound inconsistency removed (2026-11-27T15:15:48Z; re-verified 2026-11-27T15:26:11Z):** `experiment_frontier.json` rank-0 previously said the next session id must be `> 20261127T065600Z`, while this handoff requires `> 20261127T131654Z` (the campaign-08 start). That mismatch was a real bottleneck: an agent following the frontier could mint a session id in `(20261127T065600Z, 20261127T131654Z]`, which the gate **grandfathers** (stays green with NO heavy artifacts) — a silent non-avoidance hole. The frontier rank-0 `next_action_heavy` / `next_unfinished_task` / `blockers` are now aligned to the single rule below. **The next fresh session id MUST be lexicographically greater than the campaign-08 start `20261127T131654Z`** (NOT merely `20261127T065600Z`). Do not reuse the `20261127T132836Z` id.

**Two corrections carried forward (both verified in the 065600Z pass):**
1. **`|S| = 22608`, not 22584.** All-five mark-price common support is **22,608** (BNBUSDT = BTCUSDT = ETHUSDT = SOLUSDT = XRPUSDT = 22,608). The "XRP binds / |S|=22584" claim was a measurement artifact: `XRPUSDT_2025_10/markPriceKlines-2025-10-19/` has a corrupt `.csv` (24 rows, `close<=0`, correctly dropped) AND a valid `.zip` of the same day (real prices ~2.35) that restores full support. No zero-fill, repair, or substitution was performed.
2. **Secondary realigned** to frozen design §3.3: next-24h downside realized-semivariance **level** `log(RV_minus_next + eps)`, MSE.

**Cache layout heterogeneity (handled; do NOT re-discover):** a file is mark price **iff ANY path component starts with `markPriceKlines-`** (walk to any depth), then dedup by `open_time` and drop `close<=0`. Top-level `<SYM>-1h-*.zip` are **regular klines (price), NOT mark price** and are excluded. `.sha256` sidecars are hash-only; `research_state/cached_inputs_hashes.json` nests 20,694 hashes under `d["hashes"][path]`.

---

## 1. INITIAL TASK MESSAGE FOR NEXT AGENTIC WORK SESSION (UTC 2026-11-27T16:55:15Z)

### REPOSITORY PRIORITY (from repo name `Funding-conditioned-volatility-and-liquidation-risk`)
The **funding-conditioned-volatility** half is **CLOSED** (Campaign-07 `FCLR-LIVE-ARCHIVE-07`, verdict `NOT_SUPPORTED`, independently reproduced). The **liquidation-risk** half is the **single highest-value unfinished task** and the **only task** the next session may execute: **Campaign-08 `FCLR-LIVE-ARCHIVE-08`** — a Track-B modeled boundary-breach forecast.

### CURRENT STATE (verified 2026-11-27T16:55:15Z)
- **HEAD**: latest `chore(kilo): checkpoint` commit (clean working tree; hash advances on every checkpoint — anchor to the session dir, not the hash)
- **Last COMPLETE heavy session**: `research_state/session_20261127T065600Z/` (Campaign-07, full 15-artifact set, `all_checks_match=true`)
- **Active rank-0 in `experiment_frontier.json`**: `FCLR-LIVE-ARCHIVE-08-20261127T131654Z` — status `READY_EXECUTE`
- **Gate status**: `pass=true`, `reason_code=OK`, `live_archive.required=false` (grandfathered: newest on-disk session `20261127T065600Z` ≤ Campaign-08 start `20261127T131654Z`)
- **Root `research_state/` count**: **exactly 500** md+json files (zero headroom — do NOT add any root-level files)
- **Tests**: 6-module unittest suite = **122 tests OK**

### PRE-FLIGHT SELF-AUDIT (MANDATORY — run FIRST, report the output; closes the residual avoidance hole)
The gate grandfathers any session id `<= 20261127T131654Z` (gate line `if latest_utc <= campaign_start: return`). That leaves ONE narrow silent-avoidance path: a session id in the half-open range `(20261127T065600Z, 20261127T131654Z]` would keep the gate green with **no** heavy artifacts. You MUST close it yourself before doing anything else:
```bash
# 1. Confirm NO session already sits in the forbidden range (must print nothing):
ls -d research_state/session_* 2>/dev/null | awk -F'session_' '{print $2}' \
  | awk '$1>"20261127T065600Z" && $1<="20261127T131654Z"'
# 2. Mint a fresh id and ASSERT it is strictly greater than the campaign-08 start:
export UTC=$(date -u +%Y%m%dT%H%M%SZ)
python3 -c "import os,sys; u=os.environ['UTC']; sys.exit(0 if u>'20261127T131654Z' else 'FATAL: session id '+u+' is grandfathered; wait/retry')"
echo "PRE-FLIGHT OK: fresh session id $UTC > 20261127T131654Z"
```
If step 1 prints any id, or step 2 aborts, STOP and do not proceed — you are on the forbidden grandfathered path. Only a session id **strictly greater than `20261127T131654Z`** flips the gate to `live_archive.required=true` and forces the full heavy artifact set.

### BOTTLENECKS REMOVED (all verified this pass)
1. **Broken QLIKE template** → fixed in `session_20261127T065600Z` to standard non-negative QLIKE `mean(exp(y−p) − (y−p) − 1)`
2. **Aborted Campaign-08 attempt `20261127T132836Z`** → deleted; no on-disk session directory remains; not evidence
3. **Cross-file bound inconsistency** → `experiment_frontier.json` rank-0 `next_action_heavy` now correctly requires session id **> `20261127T131654Z`** (Campaign-08 start), NOT merely `> 20261127T065600Z`. A session id in `(20261127T065600Z, 20261127T131654Z]` is **grandfathered by the gate and forbidden**.
4. **`|S| = 22608`** (not 22584) — all-five mark-price common support confirmed; XRPUSDT 2025-10-19 corrupt CSV dropped by `close>0`, valid ZIP restores full support

### MANDATORY EXECUTION SEQUENCE (machine-enforced by `scripts/check_handoff_heavywork_gate.py`)

#### 1. CREATE FRESH SESSION DIRECTORY
```bash
export UTC=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p research_state/session_$UTC
```
**Constraint**: Session id MUST be lexicographically **> `20261127T131654Z`** (Campaign-08 start). Do NOT reuse `20261127T132836Z`.

#### 2. COPY & ADAPT TEMPLATE
Copy `research_state/session_20261127T065600Z/fclr_live_archive07_eval_20261127T065600Z.py` as structural template. Set:
- `SESSION = "<fresh_UTC_id>"`
- `EXPERIMENT = "FCLR-LIVE-ARCHIVE-08"`
- `CAMPAIGN_START = "<fresh_UTC_id>"` (for cleanliness; gate binds to session id > `20261127T131654Z`)

**Adapt ONLY**:
- (a) Target → Track-B boundary-breach label (long/short separate) under disclosed constant margin/leverage scenarios
- (b) Metrics → AUC / log-loss / Brier (out-of-sample)
- (c) Prereg → add margin/leverage scenarios, horizon, long/short labels

**Do NOT re-derive**: cache reader, common support `S` filter, thresholds, split logic. The template already handles all 3 mark-price layouts, dedups by `open_time`, drops `close<=0`, computes `S` correctly.

#### 3. REUSE READ-ONLY CACHE
`research_state/data_cache/<SYM>_<YYYY_MM>/` — confirm `|S| = 22,608`. Source registry must include per-file sha256 vs `.sha256` sidecar AND `cached_inputs_hashes.json["hashes"][path]`, coverage/layout per symbol/month, XRPUSDT 2025-10-19 provenance. No zero-fill, no re-download.

#### 4. PRODUCE COMPLETE ARTIFACT SET (same fresh session directory)
All files non-empty; every JSON carries real `session_id` and experiment id:
- `fclr_live_archive08_source_registry_<UTC>.{json,md}`
- `fclr_live_archive08_prereg_<UTC>.{json,md}` — **outcome-blind**, `outcome_data_inspected_before_freeze:false`, hash-bound to source registry
- `fclr_live_archive08_eval_<UTC>.{py,json,md}` — heavy 3-block evaluation, ≥2,000 block-bootstrap, per-block + leave-one-symbol-out
- `fclr_live_archive08_recompute_<UTC>.{py,json}` — **independent stdlib recompute** (separate cache reader, panel build, solver), `all_checks_match:true`, rebuilds `S` (mark-price only, `close>0`), confirms all 5 symbols in every block/fold with `n_test >= 500`
- `fclr_live_archive08_evidence_audit_<UTC>.{json,md}` — leakage/evidence audit, `audit_pass=true`, `unresolved_blockers=[]`
- `evidence_audit_<UTC>.{json,md}` — gate-critical alias matching verdict
- `trigger_check_<UTC>.json` — `external_trigger_required:false`, `trigger_source:"BINANCE_PUBLIC_ARCHIVE"`, `fired:false`
- `_headline_<UTC>.json` — concise headline metrics

#### 5. VERIFY & UPDATE
After artifacts exist, run verification commands. Only then update `experiment_frontier.json` and this handoff:
- Set rank-0 to `COMPLETED_VALIDATED`, record reproduced verdict
- Demote Campaign-08 to non-zero rank
- **Update handoff so FIRST `FCLR-LIVE-ARCHIVE-<NN>-<start>` token is `09`** (archive 08 completion below it) → gate ratchets to `live_archive09_*` family

### FROZEN DESIGN (carry forward — do not re-derive or threshold-shop)
1. **Cohort/Support**: 2024-04-01..2026-10-31 UTC; 5 symbols; restricted to mark-price common support `S` = UTC hourly timestamps where all 5 have `markPriceKlines` close>0 (`|S| = 22,608` frozen)
2. **Split**: 60/20/20 by unique UTC timestamp on `S`, 168h purge/embargo, 3 chronological test blocks; all 5 symbols in every block/fold
3. **Models**: Fixed-form deterministic stdlib OLS only; no regularization, model-family search, feature search, threshold tuning; train-only scaling
4. **Inference**: ≥2,000 fixed-seed block-bootstrap replicates (preserve complete UTC blocks jointly across symbols); per-block + leave-one-symbol-out
5. **Campaign-08 Target**: Track-B modeled boundary-breach indicator (long/short separate) under disclosed constant margin/leverage scenarios; metrics AUC/log-loss/Brier; funding-conditioned vs mark-price-only baseline. **NOT a risk overlay; NOT observed liquidations**

### VERIFICATION COMMANDS (run at start AND end)
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

**Gate must report**: top-level `pass=true`, `reason_code=OK`, `failures=[]`, `live_archive.required=true`, `live_archive.pass=true`, `artifact_family="live_archive08"`, empty missing/empty artifact lists. Unittest command must pass.

### NON-AVOIDANCE CONSTRAINTS (machine-enforced)
- **Trigger-only, prose-only, audit-only, prereg-only, source-registry-only, verify-and-stop, or zero-byte-placeholder sessions FAIL CLOSED**
- **Closed & not re-runnable**: Campaigns 01/03/04/05/06/**07**; VOL-BROAD/VOL-CORR/VOL-STRESS/VOL-JUMP arms; terminal liquidation-risk program on frozen ironflow panel
- **NO risk overlay** (Campaign-07 forecast gate did NOT pass — §9 RESEARCH_PROMPT)
- **NO external trigger wait** (Campaign-08 needs no network/new source)
- **NO modifications** to `.github/workflows`, sealed protocols, raw caches, prior frozen artifacts
- **Stdlib only**; no package installation
- **NO second handoff**, **NO status-only session**, **NO root-level `research_state/*.md`/`*.json`** (root at exactly 500)

### CONCRETE FALSIFICATION TEST
The funding-conditioned model improves out-of-sample boundary-breach discrimination (AUC / log-loss / Brier) over the mark-price-only baseline with frozen uncertainty on the untouched balanced mark-price cohort.

### DOMINANT LIMITATION TO DISCLOSE
Three heterogeneous cache layouts + separate regular-klines stream + XRPUSDT 2025-10-19 corrupt CSV (valid ZIP restores support) — template handles all (mark-price only, dedup `open_time`, `close>0`); per-block + leave-one-symbol-out diagnostics mandatory.

---

**THIS IS THE ONLY TASK. DO NOT WRITE PROSE. RUN THE EVAL TO COMPLETION.**

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

- **Machine-enforced non-avoidance:** the gate binds the active campaign to the `fclr_live_archive<NN>_*` artifact family plus `evidence_audit_<UTC>.{json,md}` and `trigger_check_<UTC>.json` in the latest session. Trigger-only, prose-only, audit-only, prereg-only, source-registry-only, verify-and-stop, or zero-byte-placeholder sessions fail closed.
- Closed and not re-runnable: campaigns 01/03/04/05/06/**07**; broad ironflow VOL-BROAD/VOL-CORR/VOL-STRESS/VOL-JUMP arms; the terminal liquidation-risk program on the frozen ironflow panel.
- **Do NOT build a risk overlay** (the campaign-07 forecast gate did not pass). Do NOT wait for an external trigger (campaign-08 needs no network/new source). Do NOT modify `.github/workflows`, sealed protocols, raw caches, or prior frozen artifacts. Stdlib only; no package installation.
- Do not create a second active handoff or a status-only session. Update this file and `research_state/experiment_frontier.json` only after the heavy artifacts exist and verify. Do not create root-level `research_state/*.md`/`*.json` (root at **exactly 500**, zero headroom).

**Highest-value next action:** copy the campaign-07 eval script as a structural template into a fresh `session_<UTC>/` (id > `20261127T131654Z`), set `SESSION`/`EXPERIMENT="FCLR-LIVE-ARCHIVE-08"`, swap the target to the boundary-breach label and metrics to AUC/log-loss/Brier, and run it; then produce the recompute + evidence audit + trigger check and verify.
**Dominant limitation to disclose:** three heterogeneous cache layouts + a separate regular-klines stream + XRPUSDT 2025-10-19 corrupt CSV (valid ZIP restores support) — the template handles all of these (mark-price only, dedup `open_time`, `close>0`); per-block + leave-one-symbol-out diagnostics remain mandatory.
**Concrete falsification test:** the funding-conditioned model improves out-of-sample boundary-breach discrimination (AUC / log-loss / Brier) over the mark-price-only baseline with the frozen uncertainty on the untouched balanced mark-price cohort.

**END OF HANDOFF — 2026-11-27T16:55:15Z**
